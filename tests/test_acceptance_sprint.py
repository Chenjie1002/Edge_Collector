from __future__ import annotations

import inspect
import unittest
from unittest.mock import patch

from scripts.run_acceptance_sprint import (
    AcceptanceClient,
    collect_by_cycle_boot_regression,
    normalize_int_array,
    raw_nok_codes,
    trace_for_identity,
    validate_profiles,
)


class NormalizeIntArrayTest(unittest.TestCase):
    def test_accepts_postgres_and_json_array_shapes(self) -> None:
        self.assertEqual([10001], normalize_int_array("{10001}"))
        self.assertEqual([10001, 10002], normalize_int_array("[10001, 10002]"))
        self.assertEqual([10001], normalize_int_array([10001]))
        self.assertEqual([], normalize_int_array("{}"))


class FakeAcceptanceClient:
    def __init__(self) -> None:
        self.trace_query = ""

    def sql(self, sql: str) -> list[dict]:
        self.trace_query = sql
        return [{"unit_id": "U-20260619-000089"}]

    def trace(self, query: str) -> dict:
        return {"unit_id": query, "found": True}


class TraceForIdentityTest(unittest.TestCase):
    def test_scopes_cycle_lookup_by_plc_boot_identity(self) -> None:
        client = FakeAcceptanceClient()

        trace = trace_for_identity(
            client,
            "WS01",
            "6266e5ac-d8aa-4e8b-b82e-32c9b87fe499",
            89,
        )

        self.assertEqual("U-20260619-000089", trace["unit_id"])
        self.assertIn("plc_boot_id = '6266e5ac-d8aa-4e8b-b82e-32c9b87fe499'", client.trace_query)
        self.assertIn("cycle_counter = 89", client.trace_query)


class RawNokCodesTest(unittest.TestCase):
    def test_reads_mapping_shaped_raw_payload_fields(self) -> None:
        self.assertEqual(
            [10001],
            raw_nok_codes(
                {
                    "nok_code_count": "1",
                    "nok_codes_1": "10001",
                    "nok_codes_2": "0",
                    "nok_codes_3": "0",
                }
            ),
        )


class AcceptanceClientTraceByCycleTest(unittest.TestCase):
    def test_includes_explicit_boot_plc_and_line_identity(self) -> None:
        client = AcceptanceClient("10.0.0.217")

        with patch(
            "scripts.run_acceptance_sprint.http_json",
            return_value={"found": True},
        ) as request:
            client.trace_by_cycle(
                "WS01",
                89,
                plc_boot_id="6266e5ac-d8aa-4e8b-b82e-32c9b87fe499",
                plc_id="PLC_001",
                line_id="LINE_001",
            )

        url = request.call_args.args[0]
        self.assertIn("station_id=WS01", url)
        self.assertIn("cycle_counter=89", url)
        self.assertIn(
            "plc_boot_id=6266e5ac-d8aa-4e8b-b82e-32c9b87fe499",
            url,
        )
        self.assertIn("plc_id=PLC_001", url)
        self.assertIn("line_id=LINE_001", url)


class FakeByCycleRegressionClient:
    def sql(self, sql: str) -> list[dict]:
        return [
            {
                "plc_id": "PLC_001",
                "line_id": "LINE_001",
                "station_id": "WS01",
                "cycle_counter": 89,
                "current_boot_id": "current-boot",
                "current_unit_id": "U-current-000089",
                "old_boot_id": "old-boot",
                "old_unit_id": "U-old-000089",
            }
        ]

    def trace_by_cycle(
        self,
        station: str,
        counter: int,
        *,
        plc_boot_id: str | None = None,
        plc_id: str | None = None,
        line_id: str | None = None,
    ) -> dict:
        boot_id = plc_boot_id or "current-boot"
        unit_id = "U-current-000089" if boot_id == "current-boot" else "U-old-000089"
        return {
            "unit_id": unit_id,
            "events": [{"plc_boot_id": boot_id}],
        }


class ByCycleBootRegressionTest(unittest.TestCase):
    def test_limits_current_boot_candidates_before_historical_pairing(self) -> None:
        source = inspect.getsource(collect_by_cycle_boot_regression)

        self.assertIn("WITH current_candidates AS MATERIALIZED", source)
        self.assertIn("LIMIT 200", source)
        self.assertIn("FROM current_candidates current_event", source)

    def test_default_current_and_old_boot_queries_remain_isolated(self) -> None:
        result = collect_by_cycle_boot_regression(FakeByCycleRegressionClient())

        self.assertEqual("PASS", result["status"])
        self.assertEqual("U-current-000089", result["default_query"]["unit_id"])
        self.assertEqual("U-current-000089", result["explicit_current"]["unit_id"])
        self.assertEqual("U-old-000089", result["explicit_old"]["unit_id"])


class FakeProfileClient:
    def state(self) -> dict:
        return {"profile": "normal", "scale": 1.0}

    def snapshots(self, limit: int = 100) -> list[dict]:
        return [
            {
                "profile": "normal",
                "plc_boot_id": "current-normal-boot",
                "captured_at": "2026-06-19T15:00:00+08:00",
            }
        ]

    def sql(self, sql: str) -> list[dict]:
        if "FROM vplc_parameter_snapshot" in sql:
            return [
                {"profile": "normal", "cycle_scale": 1.0, "plc_boot_id": "current-normal-boot"},
                {"profile": "fast", "cycle_scale": 0.1, "plc_boot_id": "fast-boot"},
                {"profile": "test", "cycle_scale": 0.05, "plc_boot_id": "test-boot"},
            ]
        return [
            {"station_id": "WS01", "rows": 10},
            {"station_id": "WS02", "rows": 9},
            {"station_id": "WS03", "rows": 8},
        ]


class ProfileHistoryValidationTest(unittest.TestCase):
    def test_uses_database_history_when_recent_snapshot_window_is_only_normal(self) -> None:
        result = validate_profiles(FakeProfileClient())

        self.assertEqual("PASS", result["status"])
        self.assertEqual({"normal", "fast", "test"}, set(result["startup_profiles"]))


if __name__ == "__main__":
    unittest.main()
