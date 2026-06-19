from __future__ import annotations

import socket
import time
import unittest
from zoneinfo import ZoneInfo

import snap7
from snap7 import type as snap7_type
from snap7 import util

from app.plc import build_read_plans, load_edge_mapping
from app.services.event_collector import EventCollectorWorker, StationRuntime


BOOT_ID = "12345678-1234-1234-1234-123456789abc"


class IntegrationStorage:
    def __init__(self) -> None:
        self.persisted: list[dict] = []
        self.ack_ok = 0
        self.errors: list[dict] = []

    def upsert_collector_runtime_status(self, **kwargs) -> None:
        return None

    def get_max_cycle_counter(self, **kwargs) -> int | None:
        return None

    def persist_cycle(self, **kwargs) -> int:
        self.persisted.append(kwargs)
        return 1

    def mark_cycle_ack_ok(self, **kwargs) -> None:
        self.ack_ok += 1

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
        worker.client = snap7.client.Client()
        worker.line_plan = plans["line"]
        worker.station_runtimes = [
            StationRuntime(station=station, plan=plans[station.station_id])
            for station in mapping.stations
        ]

        try:
            worker.poll_once()
            handshake = worker.client.db_read(101, 6, 1)
        finally:
            worker._disconnect()
            server.stop()
            server.destroy()

        self.assertEqual(1, len(storage.persisted))
        self.assertEqual(BOOT_ID, storage.persisted[0]["plc_boot_id"])
        self.assertEqual(1, storage.ack_ok)
        self.assertTrue(util.get_bool(handshake, 0, 1))
        self.assertEqual([], storage.errors)


if __name__ == "__main__":
    unittest.main()
