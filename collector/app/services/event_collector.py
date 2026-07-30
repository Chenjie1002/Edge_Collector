from __future__ import annotations

import json
import logging
import os
import re
import time
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import snap7

from app.plc import EdgeMapping, ReadPlan, build_read_plans, decode_read_plan, load_edge_mapping
from app.plc.mapping import StationMapping
from app.services.reliability import CounterDecision, classify_counter, validate_plc_boot_id
from app.services.accepted_station_event_fact import build_accepted_station_event_fact
from app.services.resolved_config_registry import (
    InMemoryResolvedConfigRegistry,
    ResolvedConfigSnapshot,
    build_resolved_config_snapshot_from_mapping,
)
from app.services.station_event_adapter import adapt_source_payload
from app.services.station_event_runtime_source import build_runtime_source_payload
from app.services.storage import Storage


logger = logging.getLogger("edge-collector.event")

RUNTIME_LOADED_EVIDENCE_SCHEMA_VERSION = "edge-mes/collector-runtime-loaded/v1"
RUNTIME_LOADED_EVENT_TYPE = "collector_runtime_loaded"
SHA256_HEX_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class StationRuntime:
    station: StationMapping
    plan: ReadPlan


@dataclass
class CollectorStartupContext:
    collector_main_started_at_utc: str
    process_pid: int
    _consumed: bool = field(default=False, init=False, repr=False)

    def consume(self) -> tuple[str, int]:
        if self._consumed:
            raise ValueError("startup context has already been consumed")
        self._consumed = True
        if not isinstance(self.collector_main_started_at_utc, str):
            raise ValueError("collector_main_started_at_utc must be a string")
        if not self.collector_main_started_at_utc.endswith("Z"):
            raise ValueError("collector_main_started_at_utc must use UTC Z suffix")
        try:
            parsed_started_at = datetime.fromisoformat(
                self.collector_main_started_at_utc[:-1] + "+00:00"
            )
        except ValueError as exc:
            raise ValueError("collector_main_started_at_utc must be RFC3339 UTC") from exc
        if parsed_started_at.tzinfo != timezone.utc:
            raise ValueError("collector_main_started_at_utc must be UTC")
        if (
            isinstance(self.process_pid, bool)
            or not isinstance(self.process_pid, int)
            or self.process_pid <= 0
        ):
            raise ValueError("process_pid must be a positive integer")
        if self.process_pid != os.getpid():
            raise ValueError("startup context PID does not match current process")
        return self.collector_main_started_at_utc, self.process_pid


class EventCollectorWorker:
    def __init__(
        self,
        *,
        dsn: str,
        host: str,
        port: int,
        startup_context: CollectorStartupContext,
        mapping_path: str = "/app/config/mapping.yaml",
    ) -> None:
        if not isinstance(startup_context, CollectorStartupContext):
            raise ValueError("mandatory startup context is missing")
        self.collector_main_started_at_utc, self.process_pid = startup_context.consume()
        self.dsn = dsn
        self.host = host
        self.port = port
        self.mapping: EdgeMapping = load_edge_mapping(mapping_path)
        self._validate_loaded_mapping_identity()
        if len(self.mapping.plcs) != 1:
            raise ValueError("PLC selection is missing or ambiguous")
        self.plc = self.mapping.plcs[0]
        if not isinstance(self.plc, Mapping):
            raise ValueError("selected PLC entry is not a mapping")
        selected_routing_line = self.plc.get("line_id")
        if not isinstance(selected_routing_line, str) or not selected_routing_line.strip():
            raise ValueError("selected PLC routing line_id is missing or empty")
        self.routing_line_id = selected_routing_line
        self.plc_id = str(self.plc.get("plc_id", "PLC_001"))
        self.line_id = self.resolved_config_snapshot.line_id
        if self.routing_line_id != self.line_id:
            raise ValueError("selected PLC routing line_id does not match canonical line_id")
        self.rack = int(self.plc.get("rack", 0))
        self.slot = int(self.plc.get("slot", 1))
        self.timezone = ZoneInfo(self.mapping.timezone)
        self.resolved_config_registry = InMemoryResolvedConfigRegistry(
            {self.resolved_config_snapshot.config_hash: self.resolved_config_snapshot}
        )
        resolved_lookup = self.resolved_config_registry.lookup_resolved_config(
            self.resolved_config_snapshot.config_hash
        )
        if not isinstance(resolved_lookup, ResolvedConfigSnapshot):
            raise ValueError("resolved config registry lookup failed")
        self.client = snap7.client.Client()
        plans_list = build_read_plans(self.mapping)
        self._validate_complete_read_plans(plans_list)
        plans = {plan.scope: plan for plan in plans_list}
        self.line_plan = plans["line"]
        self.station_runtimes = [
            StationRuntime(station=station, plan=plans[station.station_id])
            for station in self.mapping.stations
        ]
        if len(self.station_runtimes) != len(self.mapping.stations):
            raise ValueError("station runtime cardinality mismatch")
        self._emit_runtime_loaded_record(read_plan_count=len(plans_list))

    def _validate_loaded_mapping_identity(self) -> None:
        runtime_snapshot = self.mapping.runtime_snapshot
        if runtime_snapshot is None:
            raise ValueError("runtime mapping snapshot is missing")
        if not SHA256_HEX_RE.fullmatch(self.mapping.mapping_content_sha256):
            raise ValueError("mapping_content_sha256 is not a canonical SHA-256")
        if not runtime_snapshot.content_hash_matches():
            raise ValueError("runtime mapping snapshot hash mismatch")
        if not SHA256_HEX_RE.fullmatch(runtime_snapshot.config_hash):
            raise ValueError("runtime mapping config hash is not canonical")
        self.resolved_config_snapshot = build_resolved_config_snapshot_from_mapping(runtime_snapshot)
        if not isinstance(self.resolved_config_snapshot, ResolvedConfigSnapshot):
            raise ValueError("resolved config snapshot is missing")
        if self.resolved_config_snapshot.config_hash != runtime_snapshot.config_hash:
            raise ValueError("resolved/runtime config hash mismatch")
        if not self.resolved_config_snapshot.content_hash_matches():
            raise ValueError("resolved config snapshot hash mismatch")
        for attribute in (
            "schema_version",
            "config_version",
            "line_id",
            "authoritative_source",
            "timezone",
            "hash_algorithm",
            "plc_identity_namespace",
        ):
            mapping_value = getattr(self.mapping, attribute)
            runtime_value = getattr(runtime_snapshot, attribute)
            resolved_value = getattr(self.resolved_config_snapshot, attribute)
            if mapping_value != runtime_value or runtime_value != resolved_value:
                raise ValueError(f"mapping snapshot projection mismatch: {attribute}")
        if not self.mapping.mapping_path:
            raise ValueError("mapping path identity is missing")
        mapping_path = Path(self.mapping.mapping_path)
        if (
            not mapping_path.is_absolute()
            or mapping_path.is_symlink()
            or not mapping_path.is_file()
            or str(mapping_path.resolve(strict=True)) != self.mapping.mapping_path
        ):
            raise ValueError("mapping path identity is not canonical")

    def _validate_complete_read_plans(self, plans_list: list[ReadPlan]) -> None:
        configured_station_ids = [station.station_id for station in self.mapping.stations]
        expected_scopes = ["line", *configured_station_ids]
        generated_scopes = [plan.scope for plan in plans_list]
        if "line" in configured_station_ids:
            raise ValueError("configured station ID collides with reserved line scope")
        if len(configured_station_ids) != len(set(configured_station_ids)):
            raise ValueError("duplicate configured station ID")
        if len(generated_scopes) != len(set(generated_scopes)):
            raise ValueError("duplicate generated read-plan scope")
        if len(generated_scopes) != len(expected_scopes):
            raise ValueError("read-plan cardinality mismatch")
        if Counter(generated_scopes) != Counter(expected_scopes):
            raise ValueError("read-plan scope mismatch")
        if generated_scopes.count("line") != 1:
            raise ValueError("read-plan must contain exactly one line scope")
        if len(plans_list) <= 0:
            raise ValueError("read-plan list must be positive")

    def _emit_runtime_loaded_record(self, *, read_plan_count: int) -> None:
        if isinstance(read_plan_count, bool) or not isinstance(read_plan_count, int) or read_plan_count <= 0:
            raise ValueError("read_plan_count must be a positive integer")
        record = {
            "evidence_schema_version": RUNTIME_LOADED_EVIDENCE_SCHEMA_VERSION,
            "event_type": RUNTIME_LOADED_EVENT_TYPE,
            "mapping_path": self.mapping.mapping_path,
            "mapping_content_sha256": self.mapping.mapping_content_sha256,
            "mapping_schema_version": self.mapping.schema_version,
            "config_version": self.mapping.config_version,
            "line_id": self.resolved_config_snapshot.line_id,
            "read_plan_count": read_plan_count,
            "resolved_config_hash": self.resolved_config_snapshot.config_hash,
            "collector_main_started_at_utc": self.collector_main_started_at_utc,
            "process_pid": self.process_pid,
        }
        serialized = json.dumps(
            record,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        if "\r" in serialized or "\n" in serialized:
            raise ValueError("runtime-loaded record must be one line")
        logger.info(f"collector_runtime_loaded_json={serialized}")

    def run_forever(self, poll_interval_ms: int = 500) -> None:
        self.storage = Storage(self.dsn)
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
            accepted_fact = build_accepted_station_event_fact(adapter_decision)
            with self.storage.transaction():
                self.storage.insert_accepted_station_event_fact_no_commit(accepted_fact)
                event_id = self.storage.persist_cycle_no_commit(
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
            raw_bytes=data,
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
