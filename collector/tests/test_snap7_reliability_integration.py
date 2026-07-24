from __future__ import annotations

import socket
import time
import unittest
from contextlib import contextmanager
from zoneinfo import ZoneInfo

import snap7
from snap7 import type as snap7_type
from snap7 import util

from app.plc import build_read_plans, load_edge_mapping
from app.services.resolved_config_registry import (
    InMemoryResolvedConfigRegistry,
    build_resolved_config_snapshot_from_mapping,
)
from app.services.event_collector import EventCollectorWorker, StationRuntime


BOOT_ID = "12345678-1234-1234-1234-123456789abc"


class IntegrationStorage:
    def __init__(self) -> None:
        self.persisted: list[dict] = []
        self.persist_calls = 0
        self.accepted_facts: list[object] = []
        self.accepted_fact_calls = 0
        self.ack_ok = 0
        self.errors: list[dict] = []
        self.events: list[str] = []

    def upsert_collector_runtime_status(self, **kwargs) -> None:
        return None

    def get_max_cycle_counter(self, **kwargs) -> int | None:
        return None

    def persist_cycle(self, **_kwargs) -> int:
        raise AssertionError("internal-commit persist_cycle must not be called in atomic path")

    def persist_cycle_no_commit(self, **kwargs) -> int:
        self.persist_calls += 1
        self.events.append("persist_cycle")
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
        self.accepted_fact_calls += 1
        self.events.append("accepted_fact")
        for existing in self.accepted_facts:
            if existing.fact_key == fact.fact_key:
                if existing.content_fingerprint != fact.content_fingerprint:
                    raise ValueError("accepted station-event fact conflict: fact_key content differs")
                return "existing"
            if existing.source_identity == fact.source_identity:
                if existing.content_fingerprint != fact.content_fingerprint:
                    raise ValueError("accepted station-event fact conflict: source identity content differs")
                return "existing"
        self.accepted_facts.append(fact)
        return "inserted"

    def mark_cycle_ack_ok(self, **kwargs) -> None:
        self.ack_ok += 1
        self.events.append("ack_ok")

    def mark_cycle_ack_failed(self, **kwargs) -> None:
        raise AssertionError("ACK write should not fail")

    def insert_collector_error(self, **kwargs) -> None:
        self.errors.append(kwargs)

    def rollback(self) -> None:
        return None


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def set_s7_string(db: bytearray, offset: int, value: str, max_length: int) -> None:
    encoded = value.encode("ascii")
    db[offset] = max_length
    db[offset + 1] = len(encoded)
    db[offset + 2 : offset + 2 + len(encoded)] = encoded


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


class Snap7ReliabilityIntegrationTest(unittest.TestCase):
    def test_collector_reads_db104_persists_cycle_then_writes_ack(self) -> None:
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

        mapping = load_edge_mapping("config/mapping.yaml")
        plans = {plan.scope: plan for plan in build_read_plans(mapping)}
        storage = IntegrationStorage()
        worker = EventCollectorWorker.__new__(EventCollectorWorker)
        worker.storage = storage
        worker.host = "127.0.0.1"
        worker.port = port
        worker.mapping = mapping
        worker.plc = mapping.plcs[0]
        worker.plc_id = "PLC_001"
        worker.line_id = "LINE_001"
        worker.rack = 0
        worker.slot = 1
        worker.timezone = ZoneInfo(mapping.timezone)
        worker.resolved_config_snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
        worker.resolved_config_registry = InMemoryResolvedConfigRegistry(
            {worker.resolved_config_snapshot.config_hash: worker.resolved_config_snapshot}
        )
        client = TrackingSnap7Client(storage.events)
        worker.client = client
        worker.line_plan = plans["line"]
        worker.station_runtimes = [
            StationRuntime(station=station, plan=plans[station.station_id])
            for station in mapping.stations
        ]

        try:
            worker.poll_once()
            handshake = client.db_read(101, 6, 1)
        finally:
            worker._disconnect()
            server.stop()
            server.destroy()

        self.assertEqual(1, len(storage.persisted))
        self.assertEqual(1, storage.persist_calls)
        self.assertEqual(1, storage.accepted_fact_calls)
        self.assertEqual(1, len(storage.accepted_facts))
        fact = storage.accepted_facts[0]
        self.assertEqual("LINE_001", fact.line_id)
        self.assertEqual("PLC_001", fact.plc_id)
        self.assertEqual("WS01", fact.station_id)
        self.assertEqual(1, fact.cycle_counter)
        self.assertEqual("station_result", fact.event_type)
        self.assertEqual("ok", fact.production_result)
        self.assertTrue(fact.fact_key)
        self.assertTrue(fact.content_fingerprint)
        self.assertEqual(BOOT_ID, storage.persisted[0]["plc_boot_id"])
        self.assertEqual(1, storage.ack_ok)
        self.assertEqual([104, 101, 102, 103, 101], [db_number for db_number, _, _ in client.reads])
        self.assertEqual(1, len(client.writes))
        self.assertTrue(util.get_bool(handshake, 0, 1))
        self.assertEqual([], storage.errors)
        self.assertEqual(
            ["begin", "accepted_fact", "persist_cycle", "commit", "ack_write", "ack_ok"],
            storage.events,
        )


if __name__ == "__main__":
    unittest.main()
