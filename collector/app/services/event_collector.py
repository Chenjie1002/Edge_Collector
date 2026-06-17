from __future__ import annotations

import logging
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

import snap7

from app.plc import EdgeMapping, ReadPlan, build_read_plans, decode_read_plan, load_edge_mapping
from app.plc.mapping import StationMapping
from app.services.storage import Storage


logger = logging.getLogger("edge-collector.event")


@dataclass(frozen=True)
class StationRuntime:
    station: StationMapping
    plan: ReadPlan


class EventCollectorWorker:
    def __init__(
        self,
        *,
        dsn: str,
        host: str,
        port: int,
        mapping_path: str = "/app/config/mapping.yaml",
    ) -> None:
        self.storage = Storage(dsn)
        self.host = host
        self.port = port
        self.mapping: EdgeMapping = load_edge_mapping(mapping_path)
        self.plc = self.mapping.plcs[0] if self.mapping.plcs else {"plc_id": "PLC_001", "line_id": self.mapping.line_id}
        self.plc_id = str(self.plc.get("plc_id", "PLC_001"))
        self.line_id = str(self.plc.get("line_id", self.mapping.line_id))
        self.rack = int(self.plc.get("rack", 0))
        self.slot = int(self.plc.get("slot", 1))
        self.timezone = ZoneInfo(self.mapping.timezone)
        self.client = snap7.client.Client()
        self.collector_boot_id = f"COLLECTOR-{uuid.uuid4()}"
        plans = {plan.scope: plan for plan in build_read_plans(self.mapping)}
        self.station_runtimes = [
            StationRuntime(station=station, plan=plans[station.station_id])
            for station in self.mapping.stations
            if station.station_id in plans
        ]

    def run_forever(self, poll_interval_ms: int = 500) -> None:
        logger.info(
            "event collector started host=%s port=%s stations=%s",
            self.host,
            self.port,
            [runtime.station.station_id for runtime in self.station_runtimes],
        )
        while True:
            try:
                self.poll_once()
            except Exception:
                logger.exception("event collector loop failed")
                self._disconnect()
                time.sleep(3)
            time.sleep(poll_interval_ms / 1000)

    def poll_once(self) -> None:
        self._ensure_connected()
        plc_boot_id = self._read_plc_boot_id()
        for runtime in self.station_runtimes:
            data = self.client.db_read(runtime.plan.db_number, runtime.plan.read_start, runtime.plan.read_size)
            decoded = decode_read_plan(data, runtime.plan, self.mapping.timezone)
            self._process_station(runtime, data, decoded, plc_boot_id)

    def _process_station(
        self,
        runtime: StationRuntime,
        data: bytes | bytearray,
        decoded: dict[str, object],
        plc_boot_id: str,
    ) -> None:
        station_id = runtime.station.station_id
        payload_ready = bool(decoded.get("payload_ready"))
        cycle_valid = bool(decoded.get("cycle_valid"))
        read_done = bool(decoded.get("read_done"))
        cycle_counter = int(decoded.get("cycle_counter") or 0)
        station_status = self._code_label("station_status", decoded.get("station_status"))

        self.storage.upsert_collector_runtime_status(
            plc_id=self.plc_id,
            line_id=self.line_id,
            station_id=station_id,
            collector_state="RUNNING",
            plc_connection_state="CONNECTED",
            station_status=station_status,
            payload_ready=payload_ready,
            read_done=read_done,
            last_cycle_counter=cycle_counter,
            last_success_time=datetime.now(self.timezone),
            last_error_code=None,
            last_error_message=None,
        )

        if not payload_ready or not cycle_valid or cycle_counter <= 0:
            return

        raw_sample_id = self.storage.insert_raw_plc_sample(
            plc_id=self.plc_id,
            line_id=self.line_id,
            station_id=station_id,
            db_number=runtime.plan.db_number,
            read_start=runtime.plan.read_start,
            read_size=runtime.plan.read_size,
            raw_hex=bytes(data).hex(),
            decoded_json=decoded,
        )
        event_id = self.storage.upsert_cycle_event(
            plc_id=self.plc_id,
            line_id=self.line_id,
            station=runtime.station,
            plc_boot_id=plc_boot_id,
            cycle_counter=cycle_counter,
            decoded=decoded,
            raw_sample_id=raw_sample_id,
            code_tables=self.mapping.code_tables,
        )
        if event_id:
            self.storage.insert_quality_event_for_cycle(event_id)
            logger.info("cycle event stored station=%s counter=%s id=%s", station_id, cycle_counter, event_id)

        if not read_done:
            current_handshake_byte = bytes(data)[6 - runtime.plan.read_start]
            self.client.db_write(runtime.plan.db_number, 6, bytearray([current_handshake_byte | 0b00000010]))
            self.storage.mark_cycle_ack_ok(
                plc_id=self.plc_id,
                station_id=station_id,
                plc_boot_id=plc_boot_id,
                cycle_counter=cycle_counter,
            )

    def _read_plc_boot_id(self) -> str:
        try:
            data = self.client.db_read(100, 20, 38)
            max_len = int(data[0])
            actual_len = int(data[1])
            if 0 < max_len <= 36 and actual_len <= max_len:
                return bytes(data[2 : 2 + actual_len]).decode("ascii", errors="ignore") or "UNKNOWN"
        except Exception:
            logger.debug("failed to read plc_boot_id", exc_info=True)
        return self.collector_boot_id

    def _ensure_connected(self) -> None:
        if self.client.get_connected():
            return
        self.client.connect(self.host, self.rack, self.slot, tcp_port=self.port)

    def _disconnect(self) -> None:
        try:
            self.client.disconnect()
        except Exception:
            logger.debug("failed to disconnect snap7 client", exc_info=True)

    def _code_label(self, table: str, value: object) -> str:
        table_map = self.mapping.code_tables.get(table, {})
        return str(table_map.get(int(value or 0), value or "UNKNOWN"))
