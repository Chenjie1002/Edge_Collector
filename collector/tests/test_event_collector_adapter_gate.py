from __future__ import annotations

from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest

from app.plc.mapping import StationMapping
from app.plc.read_plan import ReadPlan
from app.services.resolved_config_registry import ResolvedStationSnapshot
from app.services.event_collector import EventCollectorWorker, StationRuntime


BOOT_ID = "12345678-1234-1234-1234-123456789abc"


class FakeClient:
    def __init__(self, *, fail_writes: int = 0) -> None:
        self.fail_writes = fail_writes
        self.writes: list[tuple[int, int, bytes]] = []

    def db_write(self, db_number: int, start: int, data: bytearray) -> None:
        if self.fail_writes > 0:
            self.fail_writes -= 1
            raise RuntimeError("simulated ACK write failure")
        self.writes.append((db_number, start, bytes(data)))

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

    def upsert_collector_runtime_status(self, **kwargs) -> None:
        self.runtime_updates.append(kwargs)

    def get_max_cycle_counter(self, **kwargs) -> int | None:
        return self.max_counter

    def persist_cycle(self, **kwargs) -> int:
        self.persist_calls += 1
        if self.fail_persist:
            raise RuntimeError("simulated database failure")
        self.max_counter = max(self.max_counter or 0, int(kwargs["cycle_counter"]))
        return 41

    def rollback(self) -> None:
        return None

    def mark_cycle_ack_ok(self, **kwargs) -> None:
        self.ack_ok_calls += 1

    def mark_cycle_ack_failed(self, **kwargs) -> None:
        self.ack_failed_calls += 1

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


def make_worker(
    *,
    storage: FakeStorage | None = None,
    client: FakeClient | None = None,
    adapter_disposition: str = "accepted",
    adapter_error_code: str | None = None,
    adapter_exception: Exception | None = None,
) -> tuple[EventCollectorWorker, FakeStorage, FakeClient]:
    storage = storage or FakeStorage()
    client = client or FakeClient()
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


def test_accepted_adapter_decision_enters_existing_persist_and_ack_path() -> None:
    worker, storage, client = make_worker(adapter_disposition="accepted")

    worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

    assert storage.persist_calls == 1
    assert storage.ack_ok_calls == 1
    assert len(client.writes) == 1


@pytest.mark.parametrize(
    "disposition",
    ["rejected", "deferred", "quarantined", "duplicate", "conflict", "raw_variant"],
)
def test_non_accepted_adapter_decisions_do_not_persist_or_ack(disposition: str) -> None:
    worker, storage, client = make_worker(adapter_disposition=disposition)

    worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

    assert storage.persist_calls == 0
    assert storage.ack_ok_calls == 0
    assert storage.ack_failed_calls == 0
    assert client.writes == []
    assert storage.errors[-1]["error_type"] == "ADAPTER_DECISION_NOT_ACCEPTED"
    context = storage.errors[-1]["raw_context"]
    assert context["adapter_phase"] == "adapter_decision"
    assert context["adapter_disposition"] == disposition
    assert context["adapter_error_code"] == disposition.upper()
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
