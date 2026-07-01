from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest
from snap7 import util

from app.plc.decoder import decode_read_plan
from app.plc.mapping import StationMapping, load_edge_mapping
from app.plc.read_plan import ReadPlan, build_read_plans
from app.services.decoder_registry import DecoderRegistrySnapshot
from app.services.resolved_config_registry import (
    InMemoryResolvedConfigRegistry,
    ResolvedStationSnapshot,
    build_resolved_config_snapshot_from_mapping,
)
from app.services.event_collector import EventCollectorWorker, StationRuntime
from app.services.station_event_adapter import adapt_source_payload
from app.services.station_event_runtime_source import build_runtime_source_payload


BOOT_ID = "12345678-1234-1234-1234-123456789abc"


class FakeClient:
    def __init__(self, *, fail_writes: int = 0, events: list[str] | None = None) -> None:
        self.fail_writes = fail_writes
        self.writes: list[tuple[int, int, bytes]] = []
        self.events = events

    def db_write(self, db_number: int, start: int, data: bytearray) -> None:
        if self.fail_writes > 0:
            self.fail_writes -= 1
            raise RuntimeError("simulated ACK write failure")
        self.writes.append((db_number, start, bytes(data)))
        if self.events is not None:
            self.events.append("ack_write")

    def get_connected(self) -> bool:
        return True


class FakeStorage:
    def __init__(self, *, max_counter: int | None = None, fail_persist: bool = False) -> None:
        self.max_counter = max_counter
        self.fail_persist = fail_persist
        self.persist_calls = 0
        self.ack_ok_calls = 0
        self.ack_failed_calls = 0
        self.errors: list[dict] = []
        self.runtime_updates: list[dict] = []
        self.events: list[str] = []

    def upsert_collector_runtime_status(self, **kwargs) -> None:
        self.runtime_updates.append(kwargs)

    def get_max_cycle_counter(self, **kwargs) -> int | None:
        return self.max_counter

    def persist_cycle(self, **kwargs) -> int:
        self.persist_calls += 1
        self.events.append("persist_cycle")
        if self.fail_persist:
            raise RuntimeError("simulated database failure")
        self.max_counter = max(self.max_counter or 0, int(kwargs["cycle_counter"]))
        return 41

    def rollback(self) -> None:
        return None

    def mark_cycle_ack_ok(self, **kwargs) -> None:
        self.ack_ok_calls += 1
        self.events.append("ack_ok")

    def mark_cycle_ack_failed(self, **kwargs) -> None:
        self.ack_failed_calls += 1
        self.events.append("ack_failed")

    def insert_collector_error(self, **kwargs) -> None:
        self.errors.append(kwargs)


def make_runtime() -> StationRuntime:
    station = StationMapping(
        station_id="WS01",
        name="Screw Station",
        db_number=101,
        upstream_station_id=None,
        dmc_role="child_dmc",
        fields=(),
    )
    return StationRuntime(
        station=station,
        plan=ReadPlan(scope="WS01", db_number=101, read_start=0, read_size=64, fields=()),
    )


def ready_payload(counter: int = 5, *, read_done: bool = False) -> dict[str, object]:
    return {
        "station_status": 1,
        "cycle_counter": counter,
        "payload_ready": True,
        "read_done": read_done,
        "ack_timeout": False,
        "cycle_valid": True,
        "result": 1,
        "nok_code_count": 0,
        "station_dmc": "SUB-000005",
        "unit_id": "U-20260618-000005",
        "plc_start_time": "2026-06-26T10:00:00+08:00",
        "plc_end_time": "2026-06-26T10:00:30+08:00",
    }


def assert_no_ack_read_done_mutation_for_current_non_accepted_payload(
    storage: FakeStorage,
    client: FakeClient,
    *,
    prior_max_counter: int | None,
    disposition: str,
) -> None:
    message = f"{disposition}: no ACK/read_done mutation for the current non-accepted payload"
    assert storage.persist_calls == 0
    assert storage.max_counter == prior_max_counter
    assert storage.ack_ok_calls == 0, message
    assert storage.ack_failed_calls == 0, message
    assert client.writes == [], message
    assert storage.events == []


def make_worker(
    *,
    storage: FakeStorage | None = None,
    client: FakeClient | None = None,
    adapter_disposition: str = "accepted",
    adapter_error_code: str | None = None,
    adapter_exception: Exception | None = None,
) -> tuple[EventCollectorWorker, FakeStorage, FakeClient]:
    storage = storage or FakeStorage()
    client = client or FakeClient(events=storage.events)
    worker = EventCollectorWorker.__new__(EventCollectorWorker)
    worker.storage = storage
    worker.client = client
    worker.plc_id = "PLC_001"
    worker.line_id = "LINE_001"
    worker.timezone = ZoneInfo("Asia/Shanghai")
    worker.mapping = SimpleNamespace(code_tables={})

    def adapter(*args, **kwargs):
        if adapter_exception is not None:
            raise adapter_exception
        return SimpleNamespace(
            disposition=adapter_disposition,
            final_error_code=adapter_error_code
            if adapter_error_code is not None
            else None
            if adapter_disposition == "accepted"
            else adapter_disposition.upper(),
        )

    worker._adapt_station_runtime_payload = adapter
    return worker, storage, client


def make_real_runtime_worker() -> tuple[EventCollectorWorker, FakeStorage, FakeClient, StationRuntime, bytearray, dict]:
    mapping = load_edge_mapping("config/mapping.yaml")
    plans = {plan.scope: plan for plan in build_read_plans(mapping)}
    storage = FakeStorage()
    client = FakeClient(events=storage.events)
    worker = EventCollectorWorker.__new__(EventCollectorWorker)
    worker.storage = storage
    worker.client = client
    worker.plc_id = "PLC_001"
    worker.line_id = "LINE_001"
    worker.timezone = ZoneInfo(mapping.timezone)
    worker.mapping = mapping
    worker.resolved_config_snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    worker.resolved_config_registry = InMemoryResolvedConfigRegistry(
        {worker.resolved_config_snapshot.config_hash: worker.resolved_config_snapshot}
    )
    runtime = StationRuntime(
        station=mapping.stations[0],
        plan=plans[mapping.stations[0].station_id],
    )
    data = ws01_station_data(runtime.plan.read_size)
    decoded = decode_read_plan(data, runtime.plan, mapping.timezone)
    return worker, storage, client, runtime, data, decoded


def ws01_station_data(size: int) -> bytearray:
    data = bytearray(size)
    util.set_int(data, 0, 1)
    util.set_dint(data, 2, 5)
    util.set_bool(data, 6, 0, True)
    util.set_bool(data, 6, 1, False)
    util.set_bool(data, 6, 2, False)
    util.set_bool(data, 6, 3, True)
    util.set_dint(data, 8, 1782448800)
    util.set_dint(data, 12, 1782448830)
    util.set_int(data, 16, 1)
    set_s7_string(data, 40, "SUB-000005", 40)
    set_s7_string(data, 200, "U-20260618-000005", 48)
    return data


def set_s7_string(data: bytearray, offset: int, value: str, max_length: int) -> None:
    encoded = value.encode("ascii")
    data[offset] = max_length
    data[offset + 1] = len(encoded)
    data[offset + 2 : offset + 2 + len(encoded)] = encoded


def test_accepted_adapter_decision_enters_existing_persist_and_ack_path() -> None:
    worker, storage, client = make_worker(adapter_disposition="accepted")

    worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

    assert storage.persist_calls == 1
    assert storage.ack_ok_calls == 1
    assert len(client.writes) == 1
    assert storage.events == ["persist_cycle", "ack_write", "ack_ok"]


def test_accepted_read_done_path_persists_before_ack_status_repair() -> None:
    worker, storage, client = make_worker(adapter_disposition="accepted")

    worker._process_station(make_runtime(), bytearray(64), ready_payload(read_done=True), BOOT_ID)

    assert storage.persist_calls == 1
    assert client.writes == []
    assert storage.ack_ok_calls == 1
    assert storage.events == ["persist_cycle", "ack_ok"]


@pytest.mark.parametrize(
    "disposition",
    ["rejected", "deferred", "quarantined", "duplicate", "conflict", "raw_variant"],
)
@pytest.mark.parametrize("read_done", [False, True], ids=["read_done_false", "read_done_true"])
def test_non_accepted_adapter_decisions_do_not_persist_or_mutate_current_payload_ack_status(
    disposition: str,
    read_done: bool,
) -> None:
    prior_max_counter = 4
    worker, storage, client = make_worker(
        storage=FakeStorage(max_counter=prior_max_counter),
        adapter_disposition=disposition,
    )

    worker._process_station(
        make_runtime(),
        bytearray(64),
        ready_payload(counter=5, read_done=read_done),
        BOOT_ID,
    )

    assert_no_ack_read_done_mutation_for_current_non_accepted_payload(
        storage,
        client,
        prior_max_counter=prior_max_counter,
        disposition=disposition,
    )
    assert storage.errors[-1]["error_type"] == "ADAPTER_DECISION_NOT_ACCEPTED"
    context = storage.errors[-1]["raw_context"]
    assert context["adapter_phase"] == "adapter_decision"
    assert context["adapter_disposition"] == disposition
    assert context["adapter_error_code"] == disposition.upper()
    assert context["read_done"] is read_done
    assert "adapter decision not accepted" in context["adapter_reason"]
    assert storage.runtime_updates[-1]["collector_state"] == "ADAPTER_REJECTED"


def test_adapter_exception_records_distinct_diagnostic_context_without_persist_or_ack() -> None:
    worker, storage, client = make_worker(adapter_exception=RuntimeError("simulated adapter failure"))

    worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

    assert storage.persist_calls == 0
    assert storage.ack_ok_calls == 0
    assert storage.ack_failed_calls == 0
    assert client.writes == []
    assert storage.errors[-1]["error_type"] == "ADAPTER_GATE_FAILED"
    context = storage.errors[-1]["raw_context"]
    assert context["adapter_phase"] == "adapter_exception"
    assert context["adapter_error_code"] == "RuntimeError"
    assert context["adapter_reason"] == "simulated adapter failure"
    assert context["cycle_counter"] == 5
    assert storage.runtime_updates[-1]["collector_state"] == "ADAPTER_REJECTED"


@pytest.mark.parametrize(
    "raw_error_code",
    [
        "RAW_EVIDENCE_MISSING",
        "RAW_ONLY_UNSUPPORTED",
        "RAW_PARSE_ERROR",
        "RAW_NORMALIZED_MISMATCH",
        "RAW_CONTENT_FORBIDDEN",
    ],
)
def test_raw_boundary_non_accepted_decisions_do_not_persist_or_ack(raw_error_code: str) -> None:
    worker, storage, client = make_worker(
        adapter_disposition="rejected",
        adapter_error_code=raw_error_code,
    )

    worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

    assert storage.persist_calls == 0
    assert storage.ack_ok_calls == 0
    assert storage.ack_failed_calls == 0
    assert client.writes == []
    assert storage.errors[-1]["error_type"] == "ADAPTER_DECISION_NOT_ACCEPTED"
    context = storage.errors[-1]["raw_context"]
    assert context["adapter_phase"] == "adapter_decision"
    assert context["adapter_disposition"] == "rejected"
    assert context["adapter_error_code"] == raw_error_code
    assert storage.runtime_updates[-1]["collector_state"] == "ADAPTER_REJECTED"


@pytest.mark.parametrize(
    "decoder_error_code",
    [
        "RAW_PARSE_ERROR",
        "RAW_NORMALIZED_MISMATCH",
        "RAW_CONTENT_FORBIDDEN",
        "RAW_EVIDENCE_MISSING",
        "RAW_ONLY_UNSUPPORTED",
    ],
)
def test_decoder_authority_rejections_record_diagnostics_without_persist_or_ack(decoder_error_code: str) -> None:
    worker, storage, client = make_worker(
        adapter_disposition="rejected",
        adapter_error_code=decoder_error_code,
    )

    worker._process_station(make_runtime(), bytearray(64), ready_payload(read_done=False), BOOT_ID)

    assert storage.persist_calls == 0
    assert storage.ack_ok_calls == 0
    assert storage.ack_failed_calls == 0
    assert client.writes == []
    assert storage.errors[-1]["error_type"] == "ADAPTER_DECISION_NOT_ACCEPTED"
    context = storage.errors[-1]["raw_context"]
    assert context["adapter_phase"] == "adapter_decision"
    assert context["adapter_disposition"] == "rejected"
    assert context["adapter_error_code"] == decoder_error_code
    assert "adapter decision not accepted" in context["adapter_reason"]
    assert storage.runtime_updates[-1]["collector_state"] == "ADAPTER_REJECTED"


def test_storage_failure_after_accepted_adapter_decision_still_does_not_ack() -> None:
    worker, storage, client = make_worker(
        storage=FakeStorage(fail_persist=True),
        adapter_disposition="accepted",
    )

    worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

    assert storage.persist_calls == 1
    assert storage.ack_ok_calls == 0
    assert client.writes == []
    assert storage.errors[-1]["error_type"] == "STORAGE_WRITE_FAILED"


def test_ack_write_failure_after_accepted_adapter_decision_keeps_retry_semantics() -> None:
    worker, storage, client = make_worker(
        client=FakeClient(fail_writes=1),
        adapter_disposition="accepted",
    )
    runtime = make_runtime()
    data = bytearray(64)

    worker._process_station(runtime, data, ready_payload(), BOOT_ID)
    worker._process_station(runtime, data, ready_payload(), BOOT_ID)

    assert storage.persist_calls == 2
    assert storage.ack_failed_calls == 1
    assert storage.ack_ok_calls == 1
    assert len(client.writes) == 1
    assert storage.errors[-1]["error_type"] == "ACK_WRITE_FAILED"


def test_counter_reset_short_circuits_before_adapter_persist_or_ack() -> None:
    worker, storage, client = make_worker(
        storage=FakeStorage(max_counter=8),
        adapter_disposition="accepted",
    )
    adapter_calls = 0

    def adapter(*args, **kwargs):
        nonlocal adapter_calls
        adapter_calls += 1
        return SimpleNamespace(disposition="accepted", final_error_code=None)

    worker._adapt_station_runtime_payload = adapter

    worker._process_station(make_runtime(), bytearray(64), ready_payload(counter=1), BOOT_ID)

    assert adapter_calls == 0
    assert storage.persist_calls == 0
    assert client.writes == []
    assert storage.errors[-1]["error_type"] == "PLC_COUNTER_RESET"


def test_read_done_ack_status_repair_remains_after_accepted_adapter_decision() -> None:
    worker, storage, client = make_worker(
        storage=FakeStorage(max_counter=5),
        adapter_disposition="accepted",
    )

    worker._process_station(
        make_runtime(),
        bytearray(64),
        ready_payload(counter=5, read_done=True),
        BOOT_ID,
    )

    assert storage.persist_calls == 1
    assert client.writes == []
    assert storage.ack_ok_calls == 1


def test_runtime_adapter_source_receives_station_read_plan_raw_bytes(monkeypatch) -> None:
    worker = EventCollectorWorker.__new__(EventCollectorWorker)
    station_snapshot = ResolvedStationSnapshot(
        station_id="WS01",
        line_id="LINE_001",
        plc_id="PLC_001",
        station_type="screw",
        cycle_profile="normal_screwdriving",
        mapping_id="ws01_runtime_v1",
        payload_template="station_runtime_payload_v1",
        raw_policy="raw_capable",
        decoder_id="collector.app.plc.decoder.decode_read_plan",
        decoder_version="1.0.0",
    )
    worker.resolved_config_snapshot = SimpleNamespace(
        config_hash="config-hash-1",
        station_for=lambda station_id: station_snapshot if station_id == "WS01" else None,
    )
    worker.resolved_config_registry = object()
    worker.mapping = SimpleNamespace(code_tables={})
    captured: dict[str, object] = {}

    def fake_build_runtime_source_payload(**kwargs):
        captured.update(kwargs)
        return {
            "config_hash": "config-hash-1",
            "station_id": "WS01",
            "raw_payload": {"raw_hex": bytes(kwargs["raw_bytes"]).hex()},
        }

    def fake_adapt_source_payload(source_payload, registry):
        captured["source_payload"] = source_payload
        captured["registry"] = registry
        return SimpleNamespace(disposition="accepted", final_error_code=None)

    monkeypatch.setattr(
        "app.services.event_collector.build_runtime_source_payload",
        fake_build_runtime_source_payload,
    )
    monkeypatch.setattr(
        "app.services.event_collector.adapt_source_payload",
        fake_adapt_source_payload,
    )

    decision = worker._adapt_station_runtime_payload(
        make_runtime(),
        b"\x00\x06\x10\x20",
        ready_payload(),
        BOOT_ID,
    )

    assert decision.disposition == "accepted"
    assert captured["raw_bytes"] == b"\x00\x06\x10\x20"
    assert captured["source_payload"]["raw_payload"] == {"raw_hex": "00061020"}
    assert captured["registry"] is worker.resolved_config_registry


def test_real_runtime_raw_decode_accepts_and_persists_then_acks() -> None:
    worker, storage, client, runtime, data, decoded = make_real_runtime_worker()

    worker._process_station(runtime, data, decoded, BOOT_ID)

    assert storage.persist_calls == 1
    assert storage.ack_ok_calls == 1
    assert storage.ack_failed_calls == 0
    assert len(client.writes) == 1
    assert storage.events == ["persist_cycle", "ack_write", "ack_ok"]
    assert storage.errors == []


def test_resolved_station_missing_records_diagnostics_without_persist_or_ack() -> None:
    worker, storage, client, runtime, data, decoded = make_real_runtime_worker()
    worker.resolved_config_snapshot = SimpleNamespace(
        config_hash=worker.resolved_config_snapshot.config_hash,
        station_for=lambda _station_id: None,
    )

    worker._process_station(runtime, data, decoded, BOOT_ID)

    assert storage.persist_calls == 0
    assert storage.ack_ok_calls == 0
    assert storage.ack_failed_calls == 0
    assert client.writes == []
    assert storage.errors[-1]["error_type"] == "ADAPTER_GATE_FAILED"
    context = storage.errors[-1]["raw_context"]
    assert context["adapter_phase"] == "adapter_exception"
    assert context["adapter_error_code"] == "ValueError"
    assert "resolved station snapshot missing" in context["adapter_reason"]
    assert storage.runtime_updates[-1]["collector_state"] == "ADAPTER_REJECTED"


def test_runtime_source_build_failure_records_diagnostics_without_persist_or_ack() -> None:
    worker, storage, client, runtime, data, decoded = make_real_runtime_worker()
    decoded = dict(decoded)
    decoded["plc_end_time"] = None
    decoded["plc_start_time"] = None

    worker._process_station(runtime, data, decoded, BOOT_ID)

    assert storage.persist_calls == 0
    assert storage.ack_ok_calls == 0
    assert storage.ack_failed_calls == 0
    assert client.writes == []
    assert storage.errors[-1]["error_type"] == "ADAPTER_GATE_FAILED"
    context = storage.errors[-1]["raw_context"]
    assert context["adapter_phase"] == "adapter_exception"
    assert context["adapter_error_code"] == "RuntimeSourcePayloadError"
    assert context["adapter_reason"] == "EVENT_TS_MISSING"


def test_real_runtime_malformed_raw_hex_still_rejects_as_raw_parse_error() -> None:
    worker, _storage, _client, runtime, data, decoded = make_real_runtime_worker()
    decoded = dict(decoded)
    decoded["plc_start_time"] = "2026-06-26T10:00:00+08:00"
    decoded["plc_end_time"] = "2026-06-26T10:00:30+08:00"
    source_payload = build_runtime_source_payload(
        decoded_fields=decoded,
        raw_bytes=data,
        station_snapshot=worker.resolved_config_snapshot.station_for(runtime.station.station_id),
        resolved_config_hash=worker.resolved_config_snapshot.config_hash,
        plc_boot_id=BOOT_ID,
        observed_at="2026-06-26T02:00:31Z",
        code_tables=worker.mapping.code_tables,
    )
    source_payload["raw_payload"] = {"raw_hex": "not-hex"}

    decision = adapt_source_payload(source_payload, worker.resolved_config_registry)

    assert decision.disposition == "rejected"
    assert decision.final_error_code == "RAW_PARSE_ERROR"
    assert decision.projection_metadata is None


@pytest.mark.parametrize("expected_code", ["RAW_NORMALIZED_MISMATCH", "RAW_PARSE_ERROR"])
def test_real_runtime_adapter_failures_do_not_persist_or_ack(expected_code: str) -> None:
    worker, storage, client, runtime, data, decoded = make_real_runtime_worker()
    if expected_code == "RAW_NORMALIZED_MISMATCH":
        worker.resolved_config_snapshot = snapshot_with_decoder(
            worker.resolved_config_snapshot,
            lambda _raw_payload, _event: {"station_status": 999},
        )
        worker.resolved_config_registry = InMemoryResolvedConfigRegistry(
            {worker.resolved_config_snapshot.config_hash: worker.resolved_config_snapshot}
        )
    else:
        worker.resolved_config_snapshot = replace(
            worker.resolved_config_snapshot,
            decoder_registry=replace(
                worker.resolved_config_snapshot.decoder_registry,
                registry_snapshot_id="unexpected-registry",
            ),
        )
        worker.resolved_config_registry = InMemoryResolvedConfigRegistry(
            {worker.resolved_config_snapshot.config_hash: worker.resolved_config_snapshot}
        )

    worker._process_station(runtime, data, decoded, BOOT_ID)

    assert storage.persist_calls == 0
    assert storage.ack_ok_calls == 0
    assert storage.ack_failed_calls == 0
    assert client.writes == []
    assert storage.errors[-1]["error_type"] == "ADAPTER_DECISION_NOT_ACCEPTED"
    context = storage.errors[-1]["raw_context"]
    assert context["adapter_phase"] == "adapter_decision"
    assert context["adapter_disposition"] == "rejected"
    assert context["adapter_error_code"] == expected_code
    assert storage.runtime_updates[-1]["collector_state"] == "ADAPTER_REJECTED"


def snapshot_with_decoder(snapshot, decoder) -> object:
    bindings = snapshot.decoder_registry.decoders
    registry = replace(
        snapshot.decoder_registry,
        decoders=(replace(bindings[0], decoder=decoder),) + bindings[1:],
    )
    registry = DecoderRegistrySnapshot(
        registry_snapshot_id=registry.registry_snapshot_id,
        registry_content_hash=registry.registry_content_hash,
        decoders=registry.decoders,
        schema_version=registry.schema_version,
        hash_algorithm=registry.hash_algorithm,
    )
    return replace(snapshot, decoder_registry=registry)
