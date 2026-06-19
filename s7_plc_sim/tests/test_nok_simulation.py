from __future__ import annotations

import threading
import unittest

from fastapi.testclient import TestClient

from app.control_api import create_control_app
from app.parameter_audit import ParameterAuditRecorder
from app.pipeline import (
    PROCESS_SKIPPED,
    RESULT_NOK,
    RESULT_OK,
    RESULT_SKIPPED,
    ROUTE_BYPASSING,
    Part,
    ThreeStationPipeline,
)


class NokSimulationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.recorder = ParameterAuditRecorder()
        self.pipeline = ThreeStationPipeline(audit_recorder=self.recorder)
        for station in self.pipeline.stations.values():
            station.nok_rate = 0.0

    def test_forced_nok_queue_consumes_requested_count(self) -> None:
        self.pipeline.force_nok("WS02", 20003, count=3, audit_context={"reason": "stall demo"})

        results = [
            self.pipeline._result_for("WS02", Part(serial_no=index, unit_id=f"U-{index}", child_dmc=f"D-{index}"))
            for index in range(1, 5)
        ]

        self.assertEqual([RESULT_NOK, RESULT_NOK, RESULT_NOK, RESULT_OK], [item[0] for item in results])
        self.assertEqual([20003], results[0][1])
        self.assertEqual(0, self.pipeline.snapshot()["stations"]["WS02"]["pending_forced_nok_count"])

    def test_station_rejects_nok_code_from_another_station(self) -> None:
        with self.assertRaisesRegex(ValueError, "not valid for WS01"):
            self.pipeline.force_nok("WS01", 20001, count=1, audit_context={"reason": "invalid code"})

        self.assertEqual(0, self.pipeline.snapshot()["stations"]["WS01"]["pending_forced_nok_count"])

    def test_upstream_skip_does_not_consume_downstream_forced_nok(self) -> None:
        self.pipeline.force_nok("WS02", 20001, count=1, audit_context={"reason": "next processed unit"})
        bypassed = Part(
            serial_no=1,
            unit_id="U-1",
            child_dmc="D-1",
            route_state=ROUTE_BYPASSING,
        )

        result, codes, process_status, _ = self.pipeline._result_for("WS02", bypassed)

        self.assertEqual(RESULT_SKIPPED, result)
        self.assertEqual([30003], codes)
        self.assertEqual(PROCESS_SKIPPED, process_status)
        self.assertEqual(1, self.pipeline.snapshot()["stations"]["WS02"]["pending_forced_nok_count"])

    def test_clear_forced_nok_removes_pending_queue(self) -> None:
        self.pipeline.force_nok("WS03", 30001, count=4, audit_context={"reason": "print demo"})

        self.pipeline.clear_forced_nok("WS03", audit_context={"reason": "cancel demo"})

        station = self.pipeline.snapshot()["stations"]["WS03"]
        self.assertEqual(0, station["pending_forced_nok_count"])
        self.assertEqual([], station["pending_forced_nok_codes"])

    def test_api_supports_count_and_clear_with_audit(self) -> None:
        client = TestClient(create_control_app(self.pipeline, threading.RLock()))

        queued = client.post(
            "/vplc/stations/WS01/force-nok",
            json={"nok_code": 10002, "count": 2, "reason": "torque demo"},
            headers={"X-VPLC-Actor": "quality-engineer"},
        )
        cleared = client.delete(
            "/vplc/stations/WS01/force-nok",
            params={"reason": "cancel torque demo"},
            headers={"X-VPLC-Actor": "quality-engineer"},
        )

        self.assertEqual(200, queued.status_code)
        self.assertEqual(2, queued.json()["stations"]["WS01"]["pending_forced_nok_count"])
        self.assertEqual(200, cleared.status_code)
        self.assertEqual(0, cleared.json()["stations"]["WS01"]["pending_forced_nok_count"])
        names = [item["parameter_name"] for item in self.recorder.recent_changes()]
        self.assertIn("forced_nok_queue", names)


if __name__ == "__main__":
    unittest.main()
