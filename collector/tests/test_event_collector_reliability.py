from __future__ import annotations

import unittest
from dataclasses import dataclass
from datetime import datetime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from snap7 import util

from app.plc.mapping import StationMapping, load_edge_mapping
from app.plc.read_plan import ReadPlan, build_read_plans
from app.services.event_collector import EventCollectorWorker, StationRuntime


BOOT_ID = "12345678-1234-1234-1234-123456789abc"


class FakeClient:
    def __init__(self, fail_writes: int = 0, reads: dict[int, bytes | bytearray] | None = None) -> None:
        self.fail_writes = fail_writes
        self.writes: list[tuple[int, int, bytes]] = []
        self.reads = reads or {}

    def db_write(self, db_number: int, start: int, data: bytearray) -> None:
        if self.fail_writes > 0:
            self.fail_writes -= 1
            raise RuntimeError("simulated ACK write failure")
        self.writes.append((db_number, start, bytes(data)))

    def get_connected(self) -> bool:
        return True

    def db_read(self, db_number: int, start: int, size: int) -> bytearray:
        data = bytearray(self.reads[db_number])
        return data[start : start + size]


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


def make_worker(storage: FakeStorage, client: FakeClient) -> EventCollectorWorker:
    worker = EventCollectorWorker.__new__(EventCollectorWorker)
    worker.storage = storage
    worker.client = client
    worker.plc_id = "PLC_001"
    worker.line_id = "LINE_001"
    worker.timezone = ZoneInfo("Asia/Shanghai")
    worker.mapping = type("Mapping", (), {"code_tables": {}})()
    worker._adapt_station_runtime_payload = lambda *args, **kwargs: SimpleNamespace(
        disposition="accepted",
        final_error_code=None,
    )
    return worker


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
    }


class EventCollectorReliabilityTest(unittest.TestCase):
    def test_reads_boot_identity_from_db104_mapping(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        runtime_db = bytearray(64)
        util.set_int(runtime_db, 0, 1)
        util.set_dint(runtime_db, 4, 25)
        util.set_dint(runtime_db, 8, 3)
        runtime_db[12] = 36
        runtime_db[13] = len(BOOT_ID)
        runtime_db[14 : 14 + len(BOOT_ID)] = BOOT_ID.encode("ascii")
        worker = EventCollectorWorker.__new__(EventCollectorWorker)
        worker.mapping = mapping
        worker.line_plan = {plan.scope: plan for plan in build_read_plans(mapping)}["line"]
        worker.client = FakeClient(reads={104: runtime_db})

        self.assertEqual(BOOT_ID, worker._read_plc_boot_id())

    def test_invalid_db104_identity_is_rejected(self) -> None:
        mapping = load_edge_mapping("config/mapping.yaml")
        runtime_db = bytearray(64)
        util.set_int(runtime_db, 0, 1)
        worker = EventCollectorWorker.__new__(EventCollectorWorker)
        worker.mapping = mapping
        worker.line_plan = {plan.scope: plan for plan in build_read_plans(mapping)}["line"]
        worker.client = FakeClient(reads={104: runtime_db})

        with self.assertRaises(ValueError):
            worker._read_plc_boot_id()

    def test_database_failure_never_writes_ack_and_is_logged(self) -> None:
        storage = FakeStorage(fail_persist=True)
        client = FakeClient()
        worker = make_worker(storage, client)

        worker._process_station(make_runtime(), bytearray(64), ready_payload(), BOOT_ID)

        self.assertEqual([], client.writes)
        self.assertEqual(0, storage.ack_ok_calls)
        self.assertEqual("STORAGE_WRITE_FAILED", storage.errors[-1]["error_type"])

    def test_ack_write_failure_is_marked_then_retried_on_same_payload(self) -> None:
        storage = FakeStorage()
        client = FakeClient(fail_writes=1)
        worker = make_worker(storage, client)
        runtime = make_runtime()
        data = bytearray(64)

        worker._process_station(runtime, data, ready_payload(), BOOT_ID)
        worker._process_station(runtime, data, ready_payload(), BOOT_ID)

        self.assertEqual(2, storage.persist_calls)
        self.assertEqual(1, storage.ack_failed_calls)
        self.assertEqual(1, storage.ack_ok_calls)
        self.assertEqual(1, len(client.writes))
        self.assertEqual("ACK_WRITE_FAILED", storage.errors[-1]["error_type"])

    def test_counter_reset_is_logged_without_persist_or_ack(self) -> None:
        storage = FakeStorage(max_counter=8)
        client = FakeClient()
        worker = make_worker(storage, client)

        worker._process_station(make_runtime(), bytearray(64), ready_payload(counter=1), BOOT_ID)

        self.assertEqual(0, storage.persist_calls)
        self.assertEqual([], client.writes)
        self.assertEqual("PLC_COUNTER_RESET", storage.errors[-1]["error_type"])
        self.assertEqual("COUNTER_RESET", storage.runtime_updates[-1]["collector_state"])

    def test_existing_read_done_repairs_database_ack_status_without_second_write(self) -> None:
        storage = FakeStorage(max_counter=5)
        client = FakeClient()
        worker = make_worker(storage, client)

        worker._process_station(
            make_runtime(),
            bytearray(64),
            ready_payload(counter=5, read_done=True),
            BOOT_ID,
        )

        self.assertEqual([], client.writes)
        self.assertEqual(1, storage.ack_ok_calls)


if __name__ == "__main__":
    unittest.main()
