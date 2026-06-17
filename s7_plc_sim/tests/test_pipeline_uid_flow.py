from __future__ import annotations

import time
import unittest

from snap7 import util

from app.pipeline import (
    PROCESS_SKIPPED,
    RESULT_NOK,
    RESULT_OK,
    RESULT_SKIPPED,
    ThreeStationPipeline,
)
from app.plc_db import get_s7_string


def run_until(predicate, pipeline: ThreeStationPipeline, dbs: dict[int, bytearray], timeout_s: float = 7.0) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        pipeline.tick(dbs, True)
        if predicate():
            return
        time.sleep(0.02)
    raise AssertionError("condition was not reached before timeout")


def run_one_unit_to_ws03(pipeline: ThreeStationPipeline, dbs: dict[int, bytearray]) -> dict[str, bytearray]:
    ws01_started = False
    ws02_started = False
    ws03_started = False
    snapshots: dict[str, bytearray] = {}

    def first_unit_completed() -> bool:
        nonlocal ws01_started, ws02_started, ws03_started
        ws01 = pipeline.stations["WS01"]
        ws02 = pipeline.stations["WS02"]
        ws03 = pipeline.stations["WS03"]

        if ws01.current_job:
            ws01_started = True
        if ws01_started:
            ws01.paused = True

        if ws02.current_job:
            ws02_started = True
        if ws02_started:
            ws02.paused = True

        if ws03.current_job:
            ws03_started = True
        if ws03_started:
            ws03.paused = True

        for station_id, db_number in (("WS01", 101), ("WS02", 102), ("WS03", 103)):
            if station_id not in snapshots and pipeline.stations[station_id].cycle_counter >= 1:
                snapshots[station_id] = bytearray(dbs[db_number])

        return ws03.cycle_counter >= 1

    run_until(first_unit_completed, pipeline, dbs)
    return snapshots


class PipelineUidFlowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pipeline = ThreeStationPipeline(scale=0.05, require_ack=False, ack_hold_s=0.05)
        for station in self.pipeline.stations.values():
            station.nok_rate = 0.0
        self.dbs = {101: bytearray(512), 102: bytearray(512), 103: bytearray(512)}

    def test_ws01_ok_flows_with_same_unit_id_to_ws03(self) -> None:
        snapshots = run_one_unit_to_ws03(self.pipeline, self.dbs)

        unit_ids = {get_s7_string(snapshots[station_id], 200, 48) for station_id in ("WS01", "WS02", "WS03")}
        self.assertEqual(1, len(unit_ids))
        self.assertTrue(next(iter(unit_ids)).startswith("U-"))
        self.assertEqual(RESULT_OK, util.get_int(snapshots["WS01"], 16))
        self.assertEqual(RESULT_OK, util.get_int(snapshots["WS02"], 16))
        self.assertEqual(RESULT_OK, util.get_int(snapshots["WS03"], 16))

    def test_station_does_not_start_next_job_until_payload_is_acknowledged(self) -> None:
        pipeline = ThreeStationPipeline(scale=0.05, require_ack=True, ack_hold_s=10.0)
        for station in pipeline.stations.values():
            station.nok_rate = 0.0

        run_until(lambda: pipeline.stations["WS01"].cycle_counter >= 1, pipeline, self.dbs)
        self.assertTrue(util.get_bool(self.dbs[101], 6, 0))

        time.sleep(2.0)
        pipeline.tick(self.dbs, True)

        self.assertEqual(1, pipeline.stations["WS01"].cycle_counter)
        self.assertEqual(1, pipeline.serial_no)
        self.assertIsNone(pipeline.stations["WS01"].current_job)

    def test_ws01_nok_is_skipped_by_downstream_with_same_unit_id(self) -> None:
        self.pipeline.force_nok("WS01", 10001)

        snapshots = run_one_unit_to_ws03(self.pipeline, self.dbs)

        unit_ids = {get_s7_string(snapshots[station_id], 200, 48) for station_id in ("WS01", "WS02", "WS03")}
        self.assertEqual(1, len(unit_ids))
        self.assertTrue(next(iter(unit_ids)).startswith("U-"))

        self.assertEqual(RESULT_NOK, util.get_int(snapshots["WS01"], 16))
        self.assertEqual(RESULT_SKIPPED, util.get_int(snapshots["WS02"], 16))
        self.assertEqual(RESULT_SKIPPED, util.get_int(snapshots["WS03"], 16))
        self.assertEqual(PROCESS_SKIPPED, util.get_int(snapshots["WS02"], 254))
        self.assertEqual(PROCESS_SKIPPED, util.get_int(snapshots["WS03"], 254))
        self.assertEqual(1, util.get_int(snapshots["WS02"], 258))
        self.assertEqual(1, util.get_int(snapshots["WS03"], 258))
        self.assertEqual(10001, util.get_int(snapshots["WS02"], 260))
        self.assertEqual(10001, util.get_int(snapshots["WS03"], 260))
        self.assertTrue(get_s7_string(snapshots["WS03"], 304, 40).startswith("NG-"))


if __name__ == "__main__":
    unittest.main()
