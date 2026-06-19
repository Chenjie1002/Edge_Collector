from __future__ import annotations

import unittest
from contextlib import contextmanager
from datetime import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


CURRENT_BOOT = "6266e5ac-d8aa-4e8b-b82e-32c9b87fe499"


class FakeCursor:
    def __init__(self, database: "FakeDatabase") -> None:
        self.database = database
        self.rows: list[dict] = []

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def execute(self, sql: str, params: tuple | list | None = None) -> None:
        self.database.sql = sql
        self.database.params = tuple(params or ())
        base = {
            "unit_id": self.database.unit_id,
            "station_id": self.database.station_id,
            "dmc": "SUB-001287",
            "child_dmc": "SUB-001287",
            "label_code": self.database.label_code,
            "part_id": self.database.unit_id,
            "result": self.database.result,
            "nok_codes": [],
            "ack_status": self.database.current_state,
            "plc_end_time": datetime.fromisoformat("2026-06-19T21:09:37+08:00"),
            "reject_id": None,
            "disposition": self.database.disposition,
            "defect_origin_station": None,
            "defect_code": 0,
        }

        if "station_cycle_counter" in sql:
            base.update(
                {
                    "plc_id": "PLC_001",
                    "line_id": "LINE_001",
                    "plc_boot_id": (
                        CURRENT_BOOT if self.database.has_cycle_event else None
                    ),
                    "cycle_counter": (
                        self.database.station_cycle_counter
                        if self.database.has_cycle_event
                        else None
                    ),
                    "station_cycle_counter": (
                        self.database.station_cycle_counter
                        if self.database.has_cycle_event
                        else None
                    ),
                    "route_step": self.database.route_step,
                }
            )
        else:
            # Reproduce the bug: current_route_step is mislabeled as a PLC
            # cycle counter.
            base["cycle_counter"] = self.database.route_step
        self.rows = [base]

    def fetchall(self) -> list[dict]:
        return list(self.rows)


class FakeConnection:
    def __init__(self, database: "FakeDatabase") -> None:
        self.database = database

    def cursor(self) -> FakeCursor:
        return FakeCursor(self.database)


class FakeDatabase:
    def __init__(self, *, has_cycle_event: bool = True) -> None:
        self.has_cycle_event = has_cycle_event
        self.unit_id = (
            "U-20260619-001287" if has_cycle_event else "LEGACY-INCOMPLETE-001"
        )
        self.station_id = "WS03" if has_cycle_event else "WS02"
        self.label_code = "ASM-001287" if has_cycle_event else None
        self.result = "OK" if has_cycle_event else None
        self.current_state = "COMPLETED_OK" if has_cycle_event else "IN_PROGRESS"
        self.disposition = "SHIPPING" if has_cycle_event else None
        self.route_step = 3 if has_cycle_event else 2
        self.station_cycle_counter = 1287
        self.sql = ""
        self.params: tuple = ()

    @contextmanager
    def get_conn(self):
        yield FakeConnection(self)


class RecentTraceCounterSemanticsTest(unittest.TestCase):
    def request_recent(self, database: FakeDatabase, status: str) -> dict:
        with patch("app.routes.trace.get_conn", database.get_conn):
            response = TestClient(app).get(
                "/trace/api/recent",
                params={"status": status, "limit": 1},
            )
        self.assertEqual(200, response.status_code)
        return response.json()[0]

    def test_returns_real_station_counter_separately_from_route_step(self) -> None:
        database = FakeDatabase()

        row = self.request_recent(database, "completed_ok")

        self.assertEqual(1287, row["station_cycle_counter"])
        self.assertEqual(1287, row["cycle_counter"])
        self.assertEqual(3, row["route_step"])
        self.assertEqual("WS03", row["station_id"])
        self.assertEqual(CURRENT_BOOT, row["plc_boot_id"])
        self.assertNotIn(
            "current_route_step AS cycle_counter",
            database.sql,
        )

    def test_does_not_substitute_route_step_when_cycle_event_is_missing(self) -> None:
        database = FakeDatabase(has_cycle_event=False)

        row = self.request_recent(database, "in_progress")

        self.assertIsNone(row["station_cycle_counter"])
        self.assertIsNone(row["cycle_counter"])
        self.assertEqual(2, row["route_step"])


if __name__ == "__main__":
    unittest.main()
