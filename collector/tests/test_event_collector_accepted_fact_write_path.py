from __future__ import annotations

from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest

from app.plc.mapping import StationMapping
from app.plc.read_plan import ReadPlan
from app.services.accepted_station_event_fact import build_accepted_station_event_fact
from app.services.event_collector import EventCollectorWorker, StationRuntime


BOOT_ID = "12345678-1234-1234-1234-123456789abc"


class FakeTransaction:
    def __init__(self, storage: "WritePathStorage") -> None:
        self.storage = storage

    def __enter__(self) -> "FakeTransaction":
        self.storage.events.append("begin")
        return self

    def __exit__(self, exc_type, exc, _tb) -> bool:
        if exc_type is not None:
            self.storage.rollback()
            return False
        if self.storage.fail_commit:
            self.storage.rollback()
            raise RuntimeError("simulated commit failure")
        self.storage.events.append("commit")
        return False


class WritePathStorage:
    def __init__(
        self,
        *,
        adapter_disposition: str = "accepted",
        fail_production: bool = False,
        fail_legacy: bool = False,
        fail_commit: bool = False,
    ) -> None:
        self.adapter_disposition = adapter_disposition
        self.fail_production = fail_production
        self.fail_legacy = fail_legacy
        self.fail_commit = fail_commit
        self.events: list[str] = []
        self.production_facts: list[object] = []
        self.legacy_rows: list[dict] = []
        self.errors: list[dict] = []
        self.runtime_updates: list[dict] = []
        self.ack_ok_calls = 0
        self.ack_failed_calls = 0

    def upsert_collector_runtime_status(self, **kwargs) -> None:
        self.runtime_updates.append(kwargs)

    def get_max_cycle_counter(self, **_kwargs) -> int | None:
        return None

    def transaction(self) -> FakeTransaction:
        return FakeTransaction(self)

    def insert_accepted_station_event_fact_no_commit(self, fact) -> str:
        self.events.append("production_fact")
        if self.fail_production:
            raise RuntimeError("simulated production fact failure")
        self.production_facts.append(fact)
        return "inserted"

    def persist_cycle_no_commit(self, **kwargs) -> int:
        self.events.append("legacy_current")
        if self.fail_legacy:
            raise RuntimeError("simulated legacy failure")
        self.legacy_rows.append(kwargs)
        return 41

    def persist_cycle(self, **_kwargs) -> int:
        raise AssertionError("internal-commit persist_cycle must not be called in Slice 2 atomic path")

    def rollback(self) -> None:
        self.events.append("rollback")
        self.production_facts.clear()
        self.legacy_rows.clear()

    def mark_cycle_ack_ok(self, **_kwargs) -> None:
        self.events.append("ack_ok")
        self.ack_ok_calls += 1

    def mark_cycle_ack_failed(self, **_kwargs) -> None:
        self.events.append("ack_failed")
        self.ack_failed_calls += 1

    def insert_collector_error(self, **kwargs) -> None:
        self.errors.append(kwargs)


class FakeClient:
    def __init__(self) -> None:
        self.writes: list[tuple[int, int, bytes]] = []

    def db_write(self, db_number: int, start: int, data: bytearray) -> None:
        self.writes.append((db_number, start, bytes(data)))

    def get_connected(self) -> bool:
        return True


def make_runtime() -> StationRuntime:
    station = StationMapping(
        station_id="WS01",
        name="Screw Station",
        db_number=101,
        upstream_station_id=None,
        dmc_role="child_dmc",
        fields=(),
    )
    return StationRuntime(station=station, plan=ReadPlan(scope="WS01", db_number=101, read_start=0, read_size=64, fields=()))


def ready_payload(*, read_done: bool = False) -> dict[str, object]:
    return {
        "station_status": 1,
        "cycle_counter": 5,
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


def accepted_decision() -> SimpleNamespace:
    return SimpleNamespace(
        disposition="accepted",
        final_error_code=None,
        normalized_event={
            "line_id": "LINE_001",
            "plc_id": "PLC_001",
            "station_id": "WS01",
            "station_type": "screw",
            "profile_id": "normal_screwdriving",
            "config_hash": "a" * 64,
            "config_version": "2026.06.20-1",
            "event_type": "station_result",
            "result": "ok",
            "unit_id": "U-20260618-000005",
            "dmc": "SUB-000005",
            "cycle_counter": 5,
            "event_ts": "2026-06-26T10:00:30Z",
            "correlation": {
                "source_event_id": "PLC_001:WS01:5:station_result",
                "fact_key": "sha256:" + "1" * 64,
            },
            "raw_payload": {"raw_hex": "must-not-enter-production-fact"},
            "diagnostic_context": {"reason_code": "must-not-enter-production-fact"},
        },
        fact_key="sha256:" + "1" * 64,
        content_fingerprint="sha256:" + "2" * 64,
        projection_metadata=SimpleNamespace(production_outcome="ok", defect_detail=None),
    )


def test_accepted_fact_helper_excludes_raw_and_diagnostic_context() -> None:
    fact = build_accepted_station_event_fact(accepted_decision())

    assert fact.event_type == "station_result"
    assert fact.production_result == "ok"
    assert fact.fact_key == "sha256:" + "1" * 64
    assert fact.content_fingerprint == "sha256:" + "2" * 64
    assert not hasattr(fact, "raw_payload")
    assert not hasattr(fact, "raw_hex")
    assert not hasattr(fact, "diagnostic_context")
    assert not hasattr(fact, "adapter_disposition")
    assert not hasattr(fact, "adapter_reason_code")


def test_accepted_station_nok_requires_accepted_upstream_business_evidence() -> None:
    decision = accepted_decision()
    decision.normalized_event["event_type"] = "station_nok"
    decision.normalized_event.pop("result")
    decision.normalized_event["nok_code"] = 20001
    decision.normalized_event["nok_origin"] = "plc"
    decision.projection_metadata = SimpleNamespace(defect_detail=None)

    with pytest.raises(ValueError, match="accepted defect detail projection"):
        build_accepted_station_event_fact(decision)


def test_station_result_nok_requires_accepted_business_nok_evidence() -> None:
    decision = accepted_decision()
    decision.normalized_event["result"] = "nok"
    decision.normalized_event.pop("nok_code", None)
    decision.normalized_event.pop("nok_origin", None)
    decision.projection_metadata = SimpleNamespace(production_outcome="nok", defect_detail=None)

    with pytest.raises(ValueError, match="station_result NOK requires accepted business NOK evidence"):
        build_accepted_station_event_fact(decision)


def make_worker(storage: WritePathStorage) -> tuple[EventCollectorWorker, FakeClient]:
    client = FakeClient()
    worker = EventCollectorWorker.__new__(EventCollectorWorker)
    worker.storage = storage
    worker.client = client
    worker.plc_id = "PLC_001"
    worker.line_id = "LINE_001"
    worker.timezone = ZoneInfo("Asia/Shanghai")
    worker.mapping = SimpleNamespace(code_tables={})
    worker._adapt_station_runtime_payload = lambda *_args, **_kwargs: (
        accepted_decision()
        if storage.adapter_disposition == "accepted"
        else SimpleNamespace(disposition=storage.adapter_disposition, final_error_code=storage.adapter_disposition.upper())
    )
    return worker, client


def test_accepted_write_path_commits_production_and_legacy_before_ack() -> None:
    storage = WritePathStorage()
    worker, client = make_worker(storage)

    worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

    assert storage.events == ["begin", "production_fact", "legacy_current", "commit", "ack_ok"]
    assert len(storage.production_facts) == 1
    assert len(storage.legacy_rows) == 1
    assert len(client.writes) == 1
    assert storage.ack_ok_calls == 1


@pytest.mark.parametrize(
    ("failure", "events"),
    [
        ("fail_production", ["begin", "production_fact", "rollback"]),
        ("fail_legacy", ["begin", "production_fact", "legacy_current", "rollback"]),
        ("fail_commit", ["begin", "production_fact", "legacy_current", "rollback"]),
    ],
)
def test_write_path_failures_roll_back_and_prevent_ack(failure: str, events: list[str]) -> None:
    storage = WritePathStorage(**{failure: True})
    worker, client = make_worker(storage)

    worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

    assert storage.events == events
    assert storage.production_facts == []
    assert storage.legacy_rows == []
    assert client.writes == []
    assert storage.ack_ok_calls == 0
    assert storage.ack_failed_calls == 0
    assert storage.errors[-1]["error_type"] == "STORAGE_WRITE_FAILED"


@pytest.mark.parametrize("disposition", ["rejected", "deferred", "quarantined", "duplicate", "conflict", "raw_variant"])
def test_non_accepted_dispositions_create_zero_production_rows_and_no_ack(disposition: str) -> None:
    storage = WritePathStorage(adapter_disposition=disposition)
    worker, client = make_worker(storage)

    worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

    assert storage.production_facts == []
    assert storage.legacy_rows == []
    assert storage.events == []
    assert client.writes == []
    assert storage.ack_ok_calls == 0
    assert storage.ack_failed_calls == 0
    assert storage.errors[-1]["error_type"] == "ADAPTER_DECISION_NOT_ACCEPTED"
