from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import snap7
import yaml
from snap7 import util

from app.models import MachineState
from app.sources.base import Source


TZ = ZoneInfo("Asia/Shanghai")


def load_mapping(path: str = "/app/config/plc_mapping.yaml") -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text()) or {}


def reverse_lookup(table: dict, code: int, default: str) -> str:
    for key, value in table.items():
        if int(value) == code and "_" not in str(key):
            return str(key)
    return default


class Snap7Source(Source):
    def __init__(self, host: str, port: int = 1102) -> None:
        mapping = load_mapping()
        plc_cfg = mapping.get("plc", {})
        self.host = host
        self.port = port
        self.rack = int(plc_cfg.get("rack", 0))
        self.slot = int(plc_cfg.get("slot", 1))
        self.db_number = int(plc_cfg.get("db_number", 100))
        self.db_size = int(plc_cfg.get("db_size", 64))
        self.machine_id = "LINE_01"
        self.product_codes = mapping.get("code_tables", {}).get("product_type", {})
        self.shift_codes = mapping.get("code_tables", {}).get("shift", {})
        self.client = snap7.client.Client()

    def _ensure_connected(self) -> None:
        if self.client.get_connected():
            return
        self.client.connect(self.host, self.rack, self.slot, tcp_port=self.port)

    def read(self) -> MachineState:
        self._ensure_connected()
        try:
            data = self.client.db_read(self.db_number, 0, self.db_size)
        except Exception:
            self.client.disconnect()
            raise

        product_code = util.get_byte(data, 28)
        shift_code = util.get_byte(data, 29)
        unix_time = util.get_dint(data, 32)
        ts = datetime.fromtimestamp(unix_time, TZ) if unix_time > 0 else datetime.now(TZ)
        alarm_code = util.get_int(data, 24)
        return MachineState(
            machine_id=self.machine_id,
            ts=ts,
            running=util.get_bool(data, 0, 0),
            auto_mode=util.get_bool(data, 0, 1),
            product_type=reverse_lookup(self.product_codes, product_code, "TYPE_A"),
            shift_id=reverse_lookup(self.shift_codes, shift_code, "DAY"),
            cycle_counter=util.get_dint(data, 4),
            good_count=util.get_dint(data, 8),
            ng_count=util.get_dint(data, 12),
            total_count=util.get_dint(data, 16),
            cycle_time_ms=util.get_dint(data, 20),
            alarm_active=util.get_bool(data, 0, 2),
            alarm_code=alarm_code,
            stop_reason_code=util.get_int(data, 26),
        )
