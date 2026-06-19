from __future__ import annotations

import threading
import unittest

from fastapi.testclient import TestClient

from app.control_api import create_control_app
from app.parameter_audit import ParameterAuditRecorder
from app.pipeline import ThreeStationPipeline


class ParameterAuditTest(unittest.TestCase):
    def test_recent_queries_prefer_persisted_history_and_fall_back_to_memory(self) -> None:
        class PersistedRecorder(ParameterAuditRecorder):
            def _persist_change(self, record):
                return None

            def _persist_snapshot(self, record):
                return None

            def _load_persisted_changes(self, limit: int):
                return [{"change_id": "persisted-change"}]

            def _load_persisted_snapshots(self, limit: int):
                return [{"snapshot_id": "persisted-snapshot"}]

        recorder = PersistedRecorder("postgresql://example")
        recorder.record_change(
            {
                "station_id": "WS01",
                "parameter_name": "nok_rate",
                "old_value": 0.02,
                "new_value": 0.03,
                "profile": "normal",
                "accepted": True,
            }
        )
        recorder.record_snapshot({"profile": "normal", "cycle_scale": 1.0})

        self.assertEqual("persisted-change", recorder.recent_changes()[0]["change_id"])
        self.assertEqual("persisted-snapshot", recorder.recent_snapshots()[0]["snapshot_id"])

    def test_accepted_update_records_old_new_metadata_and_snapshot(self) -> None:
        recorder = ParameterAuditRecorder()
        pipeline = ThreeStationPipeline(
            profile="fast",
            allow_runtime_cycle_edit=True,
            audit_recorder=recorder,
        )

        pipeline.update_station(
            "WS01",
            {"base_cycle_s": 12.0},
            audit_context={
                "reason": "fast demo",
                "actor": "operator-a",
                "client_ip": "10.0.0.8",
                "request_id": "req-1",
                "source": "API",
            },
        )

        change = recorder.recent_changes()[0]
        self.assertEqual("WS01", change["station_id"])
        self.assertEqual("base_cycle_s", change["parameter_name"])
        self.assertEqual(30.4, change["old_value"])
        self.assertEqual(12.0, change["new_value"])
        self.assertEqual("operator-a", change["actor"])
        self.assertEqual("fast demo", change["reason"])
        self.assertTrue(change["accepted"])
        self.assertEqual("runtime_update", recorder.recent_snapshots()[0]["snapshot_type"])

    def test_rejected_normal_cycle_edit_is_audited_without_mutation(self) -> None:
        recorder = ParameterAuditRecorder()
        pipeline = ThreeStationPipeline(
            profile="normal",
            allow_runtime_cycle_edit=False,
            audit_recorder=recorder,
        )

        with self.assertRaisesRegex(ValueError, "normal profile"):
            pipeline.update_station(
                "WS01",
                {"base_cycle_s": 1.0},
                audit_context={"reason": "speed up", "actor": "operator-b"},
            )

        self.assertEqual(30.4, pipeline.stations["WS01"].base_cycle_s)
        change = recorder.recent_changes()[0]
        self.assertFalse(change["accepted"])
        self.assertIn("normal profile", change["rejection_reason"])
        self.assertEqual([], recorder.recent_snapshots())

    def test_manual_snapshot_contains_resolved_parameters_and_boot_identity(self) -> None:
        recorder = ParameterAuditRecorder()
        pipeline = ThreeStationPipeline(
            profile="normal",
            allow_runtime_cycle_edit=False,
            audit_recorder=recorder,
            config_source="/app/config/vplc.yaml",
            config_hash="abc123",
        )

        pipeline.record_parameter_snapshot(
            "startup",
            plc_boot_id="12345678-1234-1234-1234-123456789abc",
        )

        snapshot = recorder.recent_snapshots()[0]
        self.assertEqual("startup", snapshot["snapshot_type"])
        self.assertEqual("normal", snapshot["profile"])
        self.assertEqual("abc123", snapshot["config_hash"])
        self.assertEqual(30.4, snapshot["parameters"]["stations"]["WS01"]["base_cycle_s"])
        self.assertEqual("12345678-1234-1234-1234-123456789abc", snapshot["plc_boot_id"])

    def test_runtime_audit_uses_current_plc_boot_identity_provider(self) -> None:
        recorder = ParameterAuditRecorder()
        pipeline = ThreeStationPipeline(
            profile="fast",
            allow_runtime_cycle_edit=True,
            audit_recorder=recorder,
            plc_boot_id_provider=lambda: "12345678-1234-1234-1234-123456789abc",
        )

        pipeline.update_station("WS01", {"nok_rate": 0.2})

        self.assertEqual(
            "12345678-1234-1234-1234-123456789abc",
            recorder.recent_changes()[0]["plc_boot_id"],
        )
        self.assertEqual(
            "12345678-1234-1234-1234-123456789abc",
            recorder.recent_snapshots()[0]["plc_boot_id"],
        )

    def test_api_requires_reason_and_captures_request_metadata(self) -> None:
        recorder = ParameterAuditRecorder()
        pipeline = ThreeStationPipeline(
            profile="fast",
            allow_runtime_cycle_edit=True,
            audit_recorder=recorder,
        )
        client = TestClient(create_control_app(pipeline, threading.RLock()))

        missing_reason = client.post("/vplc/stations/WS01", json={"base_cycle_s": 12.0})
        accepted = client.post(
            "/vplc/stations/WS01",
            json={"base_cycle_s": 12.0, "reason": "fast demo"},
            headers={"X-VPLC-Actor": "operator-c", "X-Request-ID": "req-api-1"},
        )

        self.assertEqual(422, missing_reason.status_code)
        self.assertEqual(200, accepted.status_code)
        change = recorder.recent_changes()[0]
        self.assertEqual("operator-c", change["actor"])
        self.assertEqual("req-api-1", change["request_id"])
        self.assertEqual("testclient", change["client_ip"])

    def test_audit_query_endpoints_return_recent_records(self) -> None:
        recorder = ParameterAuditRecorder()
        pipeline = ThreeStationPipeline(
            profile="fast",
            allow_runtime_cycle_edit=True,
            audit_recorder=recorder,
        )
        client = TestClient(create_control_app(pipeline, threading.RLock()))
        client.post(
            "/vplc/stations/WS01",
            json={"nok_rate": 0.2, "reason": "quality demo"},
        )

        changes = client.get("/vplc/audit/changes")
        snapshots = client.get("/vplc/audit/snapshots")

        self.assertEqual(200, changes.status_code)
        self.assertEqual(1, len(changes.json()["items"]))
        self.assertEqual(200, snapshots.status_code)
        self.assertEqual(1, len(snapshots.json()["items"]))


if __name__ == "__main__":
    unittest.main()
