from __future__ import annotations

import unittest
from contextlib import contextmanager
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


CURRENT_BOOT = "6266e5ac-d8aa-4e8b-b82e-32c9b87fe499"
OLD_BOOT = "11111111-1111-1111-1111-111111111111"
PLC_ID = "PLC_001"
LINE_ID = "LINE_001"


def cycle_event(*, event_id: int, boot_id: str, unit_id: str) -> dict:
    return {
        "id": event_id,
        "plc_id": PLC_ID,
        "line_id": LINE_ID,
        "station_id": "WS01",
        "plc_boot_id": boot_id,
        "cycle_counter": 89,
        "unit_id": unit_id,
        "trace_key": unit_id,
        "plc_start_time": None,
        "plc_end_time": None,
        "result": "OK",
        "nok_codes": [],
        "ack_status": "ACK_OK",
        "payload": {},
    }


class FakeCursor:
    def __init__(self, database: "FakeDatabase") -> None:
        self.database = database
        self.rows: list[dict] = []

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def execute(self, sql: str, params: tuple | list | None = None) -> None:
        values = tuple(params or ())
        self.database.queries.append((sql, values))

        if "FROM collector_runtime_status" in sql:
            self.rows = [
                {
                    "plc_id": PLC_ID,
                    "line_id": LINE_ID,
                    "station_id": "WS01",
                    "plc_boot_id": CURRENT_BOOT,
                }
            ]
            return

        if "FROM cycle_event" not in sql:
            self.rows = []
            return

        if "WHERE unit_id = %s" in sql:
            unit_id = str(values[0])
            event = self.database.events_by_unit.get(unit_id)
            if event is None:
                self.rows = []
                return
            requested_boot = next(
                (value for value in values if value in {CURRENT_BOOT, OLD_BOOT}),
                None,
            )
            self.rows = [event] if requested_boot in {None, event["plc_boot_id"]} else []
            return

        requested_boot = next(
            (value for value in values if value in {CURRENT_BOOT, OLD_BOOT}),
            None,
        )
        if requested_boot is None:
            # This reproduces the production bug: station + counter alone can
            # select a historical row when counters are reused after a boot.
            self.rows = [self.database.old_event]
        else:
            self.rows = [self.database.events_by_boot[requested_boot]]

    def fetchone(self) -> dict | None:
        return self.rows[0] if self.rows else None

    def fetchall(self) -> list[dict]:
        return list(self.rows)


class FakeConnection:
    def __init__(self, database: "FakeDatabase") -> None:
        self.database = database

    def cursor(self) -> FakeCursor:
        return FakeCursor(self.database)


class FakeDatabase:
    def __init__(self) -> None:
        self.current_event = cycle_event(
            event_id=200,
            boot_id=CURRENT_BOOT,
            unit_id="U-20260619-000089",
        )
        self.old_event = cycle_event(
            event_id=100,
            boot_id=OLD_BOOT,
            unit_id="U-20260616-000089",
        )
        self.events_by_boot = {
            CURRENT_BOOT: self.current_event,
            OLD_BOOT: self.old_event,
        }
        self.events_by_unit = {
            self.current_event["unit_id"]: self.current_event,
            self.old_event["unit_id"]: self.old_event,
        }
        self.queries: list[tuple[str, tuple]] = []

    @contextmanager
    def get_conn(self):
        yield FakeConnection(self)


class TraceByCycleBootIsolationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.database = FakeDatabase()
        self.client = TestClient(app)
        self.get_conn_patch = patch(
            "app.routes.trace.get_conn",
            self.database.get_conn,
        )
        self.get_conn_patch.start()

    def tearDown(self) -> None:
        self.get_conn_patch.stop()

    def test_defaults_to_current_boot_when_counter_exists_in_multiple_boots(self) -> None:
        response = self.client.get(
            "/trace/api/by-cycle",
            params={"station_id": "WS01", "cycle_counter": 89},
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("U-20260619-000089", response.json()["unit_id"])
        self.assertEqual(
            CURRENT_BOOT,
            response.json()["events"][0]["plc_boot_id"],
        )

    def test_explicit_current_boot_never_returns_old_boot_unit(self) -> None:
        response = self.client.get(
            "/trace/api/by-cycle",
            params={
                "station_id": "WS01",
                "cycle_counter": 89,
                "plc_boot_id": CURRENT_BOOT,
                "plc_id": PLC_ID,
                "line_id": LINE_ID,
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("U-20260619-000089", response.json()["unit_id"])
        self.assertNotEqual("U-20260616-000089", response.json()["unit_id"])

    def test_explicit_old_boot_returns_the_old_boot_unit(self) -> None:
        response = self.client.get(
            "/trace/api/by-cycle",
            params={
                "station_id": "WS01",
                "cycle_counter": 89,
                "plc_boot_id": OLD_BOOT,
                "plc_id": PLC_ID,
                "line_id": LINE_ID,
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual("U-20260616-000089", response.json()["unit_id"])
        self.assertEqual(OLD_BOOT, response.json()["events"][0]["plc_boot_id"])


if __name__ == "__main__":
    unittest.main()
