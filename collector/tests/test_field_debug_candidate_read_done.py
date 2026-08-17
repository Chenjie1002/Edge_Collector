from __future__ import annotations

import socket
import time
import unittest
from contextlib import contextmanager
from pathlib import Path
from zoneinfo import ZoneInfo

import snap7
import yaml
from snap7 import type as snap7_type
from snap7 import util

from app.plc import build_read_plans
from app.plc.mapping import parse_edge_mapping
from app.services.event_collector import EventCollectorWorker, StationRuntime
from app.services.resolved_config_registry import (
    InMemoryResolvedConfigRegistry,
    build_resolved_config_snapshot_from_mapping,
)
from common.line_config import (
    compile_runtime_mapping,
    debug_contract_from_mapping,
    load_line_config,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BOOT_ID = "12345678-1234-1234-1234-123456789abc"


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def set_s7_string(db: bytearray, offset: int, value: str, max_length: int) -> None:
    encoded = value.encode("ascii")
    db[offset] = max_length
    db[offset + 1] = len(encoded)
    db[offset + 2 : offset + 2 + len(encoded)] = encoded


class DebugStorage:
    def __init__(self, *, fail_persist: bool = False) -> None:
        self.fail_persist = fail_persist
        self.persisted: list[dict] = []
        self.accepted_facts: list[object] = []
        self.ack_ok = 0
        self.errors: list[dict] = []
        self.events: list[str] = []

    def upsert_collector_runtime_status(self, **kwargs) -> None:
        return None

    def get_max_cycle_counter(self, **kwargs) -> int | None:
        return None

    def persist_cycle(self, **_kwargs) -> int:
        raise AssertionError("the atomic collector path must not call persist_cycle")

    def persist_cycle_no_commit(self, **kwargs) -> int:
        self.events.append("persist_cycle")
        if self.fail_persist:
            raise RuntimeError("synthetic storage failure")
        self.persisted.append(kwargs)
        return 1

    @contextmanager
    def transaction(self):
        accepted_snapshot = list(self.accepted_facts)
        persisted_snapshot = list(self.persisted)
        self.events.append("begin")
        try:
            yield
        except Exception:
            self.accepted_facts = accepted_snapshot
            self.persisted = persisted_snapshot
            self.events.append("rollback")
            raise
        self.events.append("commit")

    def insert_accepted_station_event_fact_no_commit(self, fact) -> str:
        self.events.append("accepted_fact")
        self.accepted_facts.append(fact)
        return "inserted"

    def mark_cycle_ack_ok(self, **kwargs) -> None:
        self.ack_ok += 1
        self.events.append("ack_ok")

    def mark_cycle_ack_failed(self, **kwargs) -> None:
        self.events.append("ack_failed")

    def insert_collector_error(self, **kwargs) -> None:
        self.errors.append(kwargs)

    def rollback(self) -> None:
        return None


class TrackingSnap7Client:
    def __init__(self, events: list[str]) -> None:
        self.client = snap7.client.Client()
        self.events = events
        self.reads: list[tuple[int, int, int]] = []
        self.writes: list[tuple[int, int, bytes]] = []

    def get_connected(self) -> bool:
        return self.client.get_connected()

    def connect(self, *args, **kwargs) -> None:
        self.client.connect(*args, **kwargs)

    def db_read(self, db_number: int, start: int, size: int) -> bytearray:
        self.reads.append((db_number, start, size))
        return self.client.db_read(db_number, start, size)

    def db_write(self, db_number: int, start: int, data: bytearray) -> None:
        self.client.db_write(db_number, start, data)
        self.writes.append((db_number, start, bytes(data)))
        self.events.append("ack_write")

    def disconnect(self) -> None:
        self.client.disconnect()


def _projected_mapping():
    active_root = yaml.safe_load(
        (PROJECT_ROOT / "data/deployment-config/active/mapping.yaml").read_text(
            encoding="utf-8"
        )
    )
    contract = debug_contract_from_mapping(active_root)
    line_config = load_line_config(PROJECT_ROOT / "config/lines/demo_3_station.yaml")
    projection = compile_runtime_mapping(
        line_config,
        {
            "host": "127.0.0.1",
            "port": 1102,
            "rack": 0,
            "slot": 1,
            "connection_timeout_ms": 3000,
            "poll_interval_ms": 500,
        },
        line_config_source="config/lines/demo_3_station.yaml",
        debug_contract=contract,
    )
    mapping = parse_edge_mapping(projection.document)
    plans = {plan.scope: plan for plan in build_read_plans(mapping)}
    return mapping, plans, contract


def _build_worker(mapping, plans, storage, client):
    worker = EventCollectorWorker.__new__(EventCollectorWorker)
    worker.storage = storage
    worker.host = "127.0.0.1"
    worker.port = client.port
    worker.mapping = mapping
    worker.plc = mapping.plcs[0]
    worker.plc_id = "PLC_001"
    worker.line_id = "LINE_001"
    worker.rack = 0
    worker.slot = 1
    worker.timezone = ZoneInfo(mapping.timezone)
    worker.resolved_config_snapshot = build_resolved_config_snapshot_from_mapping(
        mapping.runtime_snapshot
    )
    worker.resolved_config_registry = InMemoryResolvedConfigRegistry(
        {worker.resolved_config_snapshot.config_hash: worker.resolved_config_snapshot}
    )
    worker.client = client
    worker.line_plan = plans["line"]
    worker.station_runtimes = [
        StationRuntime(station=station, plan=plans[station.station_id])
        for station in mapping.stations
    ]
    return worker


class FieldDebugCandidateReadDoneTest(unittest.TestCase):
    def _run_fixture(self, *, fail_persist: bool = False):
        mapping, plans, contract = _projected_mapping()
        runtime_db = bytearray(64)
        util.set_int(runtime_db, 0, 1)
        util.set_dint(runtime_db, 4, 11)
        util.set_dint(runtime_db, 8, 2)
        set_s7_string(runtime_db, 12, BOOT_ID, 36)

        station_dbs = {number: bytearray(512) for number in (101, 102, 103)}
        ws01 = station_dbs[101]
        util.set_int(ws01, 0, 1)
        util.set_dint(ws01, 2, 1)
        util.set_bool(ws01, 6, 0, True)
        util.set_bool(ws01, 6, 3, True)
        util.set_dint(ws01, 8, 1782448800)
        util.set_dint(ws01, 12, 1782448830)
        util.set_int(ws01, 16, 1)
        set_s7_string(ws01, 40, "SUB-000001", 40)
        set_s7_string(ws01, 200, "U-20260618-000001", 48)

        port = free_port()
        server = snap7.server.Server()
        server.register_area(snap7_type.SrvArea.DB, 104, runtime_db)
        for db_number, db in station_dbs.items():
            server.register_area(snap7_type.SrvArea.DB, db_number, db)
        server.start(tcp_port=port)
        time.sleep(0.05)

        storage = DebugStorage(fail_persist=fail_persist)
        client = TrackingSnap7Client(storage.events)
        client.port = port
        worker = _build_worker(mapping, plans, storage, client)
        try:
            worker.poll_once()
        finally:
            worker._disconnect()
            server.stop()
            server.destroy()
        return mapping, plans, contract, storage, client

    def test_candidate_projection_is_consumed_and_read_done_follows_commit(self) -> None:
        mapping, plans, contract, storage, client = self._run_fixture()

        read_done = next(
            field
            for field in mapping.stations[0].fields
            if field.name == "read_done"
        )
        allowlist = next(
            entry
            for entry in contract["write_allowlist"]["edge_to_plc"]
            if entry["station_id"] == "WS01"
        )
        self.assertEqual("DB101.DBX6.1", read_done.address.raw)
        self.assertEqual(read_done.address.raw, allowlist["address"])
        self.assertEqual(("WS01", 0, 346), (plans["WS01"].scope, plans["WS01"].read_start, plans["WS01"].read_size))
        self.assertEqual(1, len(storage.persisted))
        self.assertEqual(1, len(storage.accepted_facts))
        self.assertEqual(1, storage.ack_ok)
        self.assertEqual([(101, 6, b"\x0b")], client.writes)
        self.assertEqual(
            ["begin", "accepted_fact", "persist_cycle", "commit", "ack_write", "ack_ok"],
            storage.events,
        )

    def test_storage_failure_never_emits_read_done_write(self) -> None:
        _mapping, _plans, _contract, storage, client = self._run_fixture(fail_persist=True)

        self.assertEqual([], client.writes)
        self.assertEqual(0, storage.ack_ok)
        self.assertEqual([], storage.persisted)
        self.assertEqual(["begin", "accepted_fact", "persist_cycle", "rollback"], storage.events)
        self.assertTrue(storage.errors)


if __name__ == "__main__":
    unittest.main()
