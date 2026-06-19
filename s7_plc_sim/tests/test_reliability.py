from __future__ import annotations

import tempfile
import time
import unittest
from pathlib import Path

from snap7 import util

from app.pipeline import ThreeStationPipeline
from app.plc_db import LineRuntimeIdentity, get_s7_string, write_line_runtime_to_db


class LineRuntimeIdentityTest(unittest.TestCase):
    def test_db104_contains_stable_boot_identity_and_runtime_counters(self) -> None:
        db = bytearray(64)

        write_line_runtime_to_db(
            db,
            protocol_version=1,
            heartbeat_counter=27,
            plc_restart_counter=4,
            plc_boot_id="12345678-1234-1234-1234-123456789abc",
        )

        self.assertEqual(1, util.get_int(db, 0))
        self.assertEqual(27, util.get_dint(db, 4))
        self.assertEqual(4, util.get_dint(db, 8))
        self.assertEqual(
            "12345678-1234-1234-1234-123456789abc",
            get_s7_string(db, 12, 36),
        )

    def test_restart_counter_persists_and_manual_reset_rotates_boot_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            state_path = Path(temp_dir) / "runtime.json"
            first = LineRuntimeIdentity.load_or_start(state_path)
            first_boot_id = first.plc_boot_id

            first.rotate_boot_id()
            reset_boot_id = first.plc_boot_id
            second = LineRuntimeIdentity.load_or_start(state_path)

        self.assertNotEqual(first_boot_id, reset_boot_id)
        self.assertNotEqual(reset_boot_id, second.plc_boot_id)
        self.assertEqual(3, second.plc_restart_counter)


class StrictAckPipelineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dbs = {101: bytearray(512), 102: bytearray(512), 103: bytearray(512)}

    def test_default_mode_keeps_payload_and_sets_timeout_until_ack(self) -> None:
        pipeline = ThreeStationPipeline(ack_deadline_s=0.01)
        station = pipeline.stations["WS01"]
        station.payload_ready_since = time.monotonic() - 1
        util.set_bool(self.dbs[101], 6, 0, True)
        util.set_bool(self.dbs[101], 6, 3, True)
        util.set_dint(self.dbs[101], 2, 9)

        pipeline.tick(self.dbs, False)

        self.assertTrue(util.get_bool(self.dbs[101], 6, 0))
        self.assertTrue(util.get_bool(self.dbs[101], 6, 2))
        self.assertTrue(util.get_bool(self.dbs[101], 6, 3))
        self.assertEqual(9, util.get_dint(self.dbs[101], 2))

    def test_read_done_clears_all_handshake_bits(self) -> None:
        pipeline = ThreeStationPipeline(ack_deadline_s=10)
        station = pipeline.stations["WS01"]
        station.payload_ready_since = time.monotonic()
        for bit in range(4):
            util.set_bool(self.dbs[101], 6, bit, True)

        pipeline.tick(self.dbs, False)

        self.assertFalse(util.get_bool(self.dbs[101], 6, 0))
        self.assertFalse(util.get_bool(self.dbs[101], 6, 1))
        self.assertFalse(util.get_bool(self.dbs[101], 6, 2))
        self.assertFalse(util.get_bool(self.dbs[101], 6, 3))

    def test_manual_reset_rotates_runtime_identity(self) -> None:
        rotations: list[str] = []
        pipeline = ThreeStationPipeline(on_counter_reset=lambda: rotations.append("rotated"))

        pipeline.reset()

        self.assertEqual(["rotated"], rotations)


if __name__ == "__main__":
    unittest.main()
