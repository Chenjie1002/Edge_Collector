from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import snap7

from app.plc import EdgeMapping, ReadPlan, build_read_plans, decode_read_plan, load_edge_mapping
from app.plc.mapping import StationMapping
from app.services.reliability import CounterDecision, classify_counter, validate_plc_boot_id
from app.services.resolved_config_registry import (
    InMemoryResolvedConfigRegistry,
    build_resolved_config_snapshot_from_mapping,
)
from app.services.station_event_adapter import adapt_source_payload
from app.services.station_event_runtime_source import build_runtime_source_payload
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
        self.resolved_config_snapshot = build_resolved_config_snapshot_from_mapping(self.mapping.runtime_snapshot)
        self.resolved_config_registry = InMemoryResolvedConfigRegistry(
            {self.resolved_config_snapshot.config_hash: self.resolved_config_snapshot}
        )
        self.client = snap7.client.Client()
        plans = {plan.scope: plan for plan in build_read_plans(self.mapping)}
        self.line_plan = plans.get("line")
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
        try:
            self._ensure_connected()
        except Exception as exc:
            self._record_global_error("PLC_CONNECTION_FAILED", exc)
            raise
        try:
            plc_boot_id = self._read_plc_boot_id()
        except Exception as exc:
            self._record_global_error("PLC_IDENTITY_INVALID", exc)
            return
        for runtime in self.station_runtimes:
            try:
                data = self.client.db_read(runtime.plan.db_number, runtime.plan.read_start, runtime.plan.read_size)
                decoded = decode_read_plan(data, runtime.plan, self.mapping.timezone)
            except Exception as exc:
                self._record_station_error(runtime, "PLC_READ_DECODE_FAILED", exc, plc_boot_id=plc_boot_id)
                continue
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
        ack_timeout = bool(decoded.get("ack_timeout"))
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
            plc_boot_id=plc_boot_id,
            ack_timeout=ack_timeout,
        )

        if not payload_ready or not cycle_valid or cycle_counter <= 0:
            return

        last_counter = self.storage.get_max_cycle_counter(
            plc_id=self.plc_id,
            station_id=station_id,
            plc_boot_id=plc_boot_id,
        )
        counter_decision = classify_counter(last_counter, cycle_counter)
        if counter_decision is CounterDecision.RESET:
            message = (
                f"cycle counter decreased within boot identity: "
                f"last={last_counter} current={cycle_counter}"
            )
            self._record_station_error(
                runtime,
                "PLC_COUNTER_RESET",
                RuntimeError(message),
                plc_boot_id=plc_boot_id,
                cycle_counter=cycle_counter,
                decoded=decoded,
                collector_state="COUNTER_RESET",
            )
            return

        try:
            adapter_decision = self._adapt_station_runtime_payload(runtime, data, decoded, plc_boot_id)
        except Exception as exc:
            context = self._adapter_diagnostic_context(
                decoded,
                adapter_phase="adapter_exception",
                adapter_error_code=exc.__class__.__name__,
                adapter_reason=str(exc),
            )
            self._record_station_error(
                runtime,
                "ADAPTER_GATE_FAILED",
                exc,
                plc_boot_id=plc_boot_id,
                cycle_counter=cycle_counter,
                decoded=context,
                collector_state="ADAPTER_REJECTED",
            )
            return
        if adapter_decision.disposition != "accepted":
            message = (
                f"adapter decision not accepted: disposition={adapter_decision.disposition} "
                f"error={adapter_decision.final_error_code}"
            )
            context = self._adapter_diagnostic_context(
                decoded,
                adapter_phase="adapter_decision",
                adapter_disposition=adapter_decision.disposition,
                adapter_error_code=adapter_decision.final_error_code,
                adapter_reason=message,
            )
            self._record_station_error(
                runtime,
                "ADAPTER_DECISION_NOT_ACCEPTED",
                RuntimeError(message),
                plc_boot_id=plc_boot_id,
                cycle_counter=cycle_counter,
                decoded=context,
                collector_state="ADAPTER_REJECTED",
            )
            return

        try:
            event_id = self.storage.persist_cycle(
                plc_id=self.plc_id,
                line_id=self.line_id,
                station=runtime.station,
                plc_boot_id=plc_boot_id,
                cycle_counter=cycle_counter,
                decoded=decoded,
                db_number=runtime.plan.db_number,
                read_start=runtime.plan.read_start,
                read_size=runtime.plan.read_size,
                raw_hex=bytes(data).hex(),
                code_tables=self.mapping.code_tables,
            )
            logger.info(
                "cycle event stored station=%s counter=%s id=%s decision=%s",
                station_id,
                cycle_counter,
                event_id,
                counter_decision.value,
            )
        except Exception as exc:
            try:
                self.storage.rollback()
            except Exception:
                logger.debug("storage rollback failed", exc_info=True)
            self._record_station_error(
                runtime,
                "STORAGE_WRITE_FAILED",
                exc,
                plc_boot_id=plc_boot_id,
                cycle_counter=cycle_counter,
                decoded=decoded,
                collector_state="STORAGE_ERROR",
            )
            return

        if read_done:
            self.storage.mark_cycle_ack_ok(
                plc_id=self.plc_id,
                station_id=station_id,
                plc_boot_id=plc_boot_id,
                cycle_counter=cycle_counter,
            )
            return

        current_handshake_byte = bytes(data)[6 - runtime.plan.read_start]
        try:
            self.client.db_write(runtime.plan.db_number, 6, bytearray([current_handshake_byte | 0b00000010]))
        except Exception as exc:
            self.storage.mark_cycle_ack_failed(
                plc_id=self.plc_id,
                station_id=station_id,
                plc_boot_id=plc_boot_id,
                cycle_counter=cycle_counter,
            )
            self._record_station_error(
                runtime,
                "ACK_WRITE_FAILED",
                exc,
                plc_boot_id=plc_boot_id,
                cycle_counter=cycle_counter,
                decoded=decoded,
                collector_state="ACK_RETRY",
            )
            return
        self.storage.mark_cycle_ack_ok(
            plc_id=self.plc_id,
            station_id=station_id,
            plc_boot_id=plc_boot_id,
            cycle_counter=cycle_counter,
        )

    def _adapt_station_runtime_payload(
        self,
        runtime: StationRuntime,
        data: bytes | bytearray,
        decoded: dict[str, object],
        plc_boot_id: str,
    ):
        station_snapshot = self.resolved_config_snapshot.station_for(runtime.station.station_id)
        if station_snapshot is None:
            raise ValueError(f"resolved station snapshot missing: {runtime.station.station_id}")
        source_payload = build_runtime_source_payload(
            decoded_fields=decoded,
            raw_bytes=None,
            station_snapshot=station_snapshot,
            resolved_config_hash=self.resolved_config_snapshot.config_hash,
            plc_boot_id=plc_boot_id,
            observed_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            code_tables=self.mapping.code_tables,
        )
        return adapt_source_payload(source_payload, self.resolved_config_registry)

    def _adapter_diagnostic_context(
        self,
        decoded: dict[str, object],
        *,
        adapter_phase: str,
        adapter_disposition: str | None = None,
        adapter_error_code: str | None = None,
        adapter_reason: str | None = None,
    ) -> dict[str, object]:
        context = dict(decoded)
        context["adapter_phase"] = adapter_phase
        if adapter_disposition is not None:
            context["adapter_disposition"] = adapter_disposition
        if adapter_error_code is not None:
            context["adapter_error_code"] = adapter_error_code
        if adapter_reason:
            context["adapter_reason"] = adapter_reason
        return context

    def _read_plc_boot_id(self) -> str:
        if self.line_plan is None:
            raise ValueError("line runtime read plan is missing")
        data = self.client.db_read(
            self.line_plan.db_number,
            self.line_plan.read_start,
            self.line_plan.read_size,
        )
        decoded = decode_read_plan(data, self.line_plan, self.mapping.timezone)
        if int(decoded.get("protocol_version") or 0) != 1:
            raise ValueError(f"unsupported PLC runtime protocol version: {decoded.get('protocol_version')}")
        return validate_plc_boot_id(decoded.get("plc_boot_id"))

    def _record_global_error(self, error_type: str, exc: Exception) -> None:
        self._insert_error(
            station_id=None,
            error_type=error_type,
            exc=exc,
            plc_boot_id=None,
            cycle_counter=None,
            raw_context={"host": self.host, "port": self.port},
        )
        for runtime in self.station_runtimes:
            self._update_runtime_error(runtime, error_type, str(exc), "ERROR", 0, None)

    def _record_station_error(
        self,
        runtime: StationRuntime,
        error_type: str,
        exc: Exception,
        *,
        plc_boot_id: str | None,
        cycle_counter: int | None = None,
        decoded: dict[str, object] | None = None,
        collector_state: str = "ERROR",
    ) -> None:
        self._insert_error(
            station_id=runtime.station.station_id,
            error_type=error_type,
            exc=exc,
            plc_boot_id=plc_boot_id,
            cycle_counter=cycle_counter,
            raw_context=decoded or {},
        )
        self._update_runtime_error(
            runtime,
            error_type,
            str(exc),
            collector_state,
            cycle_counter or 0,
            plc_boot_id,
        )

    def _insert_error(
        self,
        *,
        station_id: str | None,
        error_type: str,
        exc: Exception,
        plc_boot_id: str | None,
        cycle_counter: int | None,
        raw_context: dict[str, object],
    ) -> None:
        try:
            self.storage.insert_collector_error(
                plc_id=self.plc_id,
                line_id=self.line_id,
                station_id=station_id,
                error_type=error_type,
                error_message=str(exc),
                plc_boot_id=plc_boot_id,
                cycle_counter=cycle_counter,
                raw_context=raw_context,
            )
        except Exception:
            logger.exception("failed to persist collector error type=%s station=%s", error_type, station_id)

    def _update_runtime_error(
        self,
        runtime: StationRuntime,
        error_type: str,
        message: str,
        collector_state: str,
        cycle_counter: int,
        plc_boot_id: str | None,
    ) -> None:
        try:
            self.storage.upsert_collector_runtime_status(
                plc_id=self.plc_id,
                line_id=self.line_id,
                station_id=runtime.station.station_id,
                collector_state=collector_state,
                plc_connection_state="CONNECTED" if self.client.get_connected() else "DISCONNECTED",
                station_status="UNKNOWN",
                payload_ready=False,
                read_done=False,
                last_cycle_counter=cycle_counter,
                last_success_time=datetime.now(self.timezone),
                last_error_code=error_type,
                last_error_message=message,
                plc_boot_id=plc_boot_id,
                ack_timeout=False,
            )
        except Exception:
            logger.exception(
                "failed to update collector runtime error type=%s station=%s",
                error_type,
                runtime.station.station_id,
            )

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
