from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import struct
import uuid
from zoneinfo import ZoneInfo

import yaml
from snap7 import util


TZ = ZoneInfo("Asia/Shanghai")


def load_mapping(path: str = "/app/config/plc_mapping.yaml") -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text()) or {}


def _code(table: dict, value: str, default: int = 0) -> int:
    return int(table.get(value, default))


def write_state_to_db(db: bytearray, payload: dict, mapping: dict) -> None:
    code_tables = mapping.get("code_tables", {})
    product_codes = code_tables.get("product_type", {})
    shift_codes = code_tables.get("shift", {})
    scenario_codes = code_tables.get("scenario", {})

    util.set_bool(db, 0, 0, bool(payload.get("running")))
    util.set_bool(db, 0, 1, bool(payload.get("auto_mode")))
    util.set_bool(db, 0, 2, bool(payload.get("alarm_active")))
    util.set_dint(db, 4, int(payload.get("cycle_counter", 0)))
    util.set_dint(db, 8, int(payload.get("good_count", 0)))
    util.set_dint(db, 12, int(payload.get("ng_count", 0)))
    util.set_dint(db, 16, int(payload.get("total_count", 0)))
    util.set_dint(db, 20, int(payload.get("cycle_time_ms", 0)))
    util.set_int(db, 24, int(payload.get("alarm_code", 0)))
    util.set_int(db, 26, int(payload.get("stop_reason_code", 0)))
    util.set_byte(db, 28, _code(product_codes, str(payload.get("product_type", ""))))
    util.set_byte(db, 29, _code(shift_codes, str(payload.get("shift_id", ""))))
    util.set_byte(db, 30, _code(scenario_codes, str(payload.get("scenario_id", "normal"))))

    ts_text = payload.get("ts")
    ts = datetime.now(TZ)
    if ts_text:
        ts = datetime.fromisoformat(str(ts_text))
    util.set_dint(db, 32, int(ts.timestamp()))


def set_s7_string(db: bytearray, offset: int, value: str, max_length: int) -> None:
    encoded = value.encode("ascii", errors="ignore")[:max_length]
    db[offset] = max_length
    db[offset + 1] = len(encoded)
    db[offset + 2 : offset + 2 + max_length] = b"\x00" * max_length
    db[offset + 2 : offset + 2 + len(encoded)] = encoded


def get_s7_string(db: bytearray, offset: int, max_length: int) -> str:
    declared_max = int(db[offset])
    actual_length = int(db[offset + 1])
    if 0 < declared_max <= max_length and actual_length <= declared_max:
        return bytes(db[offset + 2 : offset + 2 + actual_length]).decode("ascii", errors="ignore")
    raw = bytes(db[offset : offset + max_length])
    return raw.split(b"\x00", 1)[0].decode("ascii", errors="ignore")


def set_real(db: bytearray, offset: int, value: float) -> None:
    db[offset : offset + 4] = struct.pack(">f", float(value))


def clear_station_handshake(db: bytearray) -> None:
    util.set_bool(db, 6, 0, False)
    util.set_bool(db, 6, 1, False)
    util.set_bool(db, 6, 2, False)
    util.set_bool(db, 6, 3, False)


@dataclass
class LineRuntimeIdentity:
    state_path: Path
    plc_restart_counter: int
    plc_boot_id: str

    @classmethod
    def load_or_start(cls, state_path: str | Path) -> "LineRuntimeIdentity":
        path = Path(state_path)
        restart_counter = 0
        if path.exists():
            try:
                restart_counter = int(json.loads(path.read_text()).get("plc_restart_counter", 0))
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                restart_counter = 0
        identity = cls(
            state_path=path,
            plc_restart_counter=restart_counter + 1,
            plc_boot_id=str(uuid.uuid4()),
        )
        identity._persist()
        return identity

    def rotate_boot_id(self) -> None:
        self.plc_restart_counter += 1
        self.plc_boot_id = str(uuid.uuid4())
        self._persist()

    def _persist(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.state_path.with_suffix(f"{self.state_path.suffix}.tmp")
        temporary_path.write_text(
            json.dumps(
                {
                    "plc_restart_counter": self.plc_restart_counter,
                    "plc_boot_id": self.plc_boot_id,
                }
            )
        )
        temporary_path.replace(self.state_path)


def write_line_runtime_to_db(
    db: bytearray,
    *,
    protocol_version: int,
    heartbeat_counter: int,
    plc_restart_counter: int,
    plc_boot_id: str,
) -> None:
    util.set_int(db, 0, int(protocol_version))
    util.set_dint(db, 4, int(heartbeat_counter))
    util.set_dint(db, 8, int(plc_restart_counter))
    set_s7_string(db, 12, plc_boot_id, 36)


def write_station_header(
    db: bytearray,
    *,
    station_status: int,
    cycle_counter: int,
    payload_ready: bool,
    ack_timeout: bool,
    cycle_valid: bool,
    plc_start_time: datetime | None,
    plc_end_time: datetime | None,
    result: int,
    nok_codes: list[int],
    alarm_code: int,
    downtime_type: int,
    pallet_id_numeric: int,
    station_dmc: str,
) -> None:
    util.set_int(db, 0, int(station_status))
    util.set_dint(db, 2, int(cycle_counter))
    util.set_bool(db, 6, 0, bool(payload_ready))
    util.set_bool(db, 6, 2, bool(ack_timeout))
    util.set_bool(db, 6, 3, bool(cycle_valid))
    util.set_dint(db, 8, int(plc_start_time.timestamp()) if plc_start_time else 0)
    util.set_dint(db, 12, int(plc_end_time.timestamp()) if plc_end_time else 0)
    util.set_int(db, 16, int(result))
    util.set_int(db, 18, min(len(nok_codes), 3))
    for index, offset in enumerate((20, 22, 24)):
        util.set_int(db, offset, int(nok_codes[index]) if index < len(nok_codes) else 0)
    util.set_int(db, 26, int(alarm_code))
    util.set_int(db, 28, int(downtime_type))
    util.set_dint(db, 30, int(pallet_id_numeric))
    set_s7_string(db, 40, station_dmc, 40)
