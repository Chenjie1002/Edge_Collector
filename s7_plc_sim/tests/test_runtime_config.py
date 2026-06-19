from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.control_api import CONTROL_HTML
from app.pipeline import ThreeStationPipeline
from app.runtime_config import load_runtime_config


CONFIG = """
profile: normal
stations:
  WS01: {base_cycle_s: 30.4, jitter_s: 1.2, nok_rate: 0.02}
  WS02: {base_cycle_s: 29.8, jitter_s: 1.0, nok_rate: 0.015}
  WS03: {base_cycle_s: 29.2, jitter_s: 0.9, nok_rate: 0.01}
profiles:
  normal: {cycle_scale: 1.0, allow_runtime_cycle_edit: false}
  fast: {cycle_scale: 0.1, allow_runtime_cycle_edit: true}
  test: {cycle_scale: 0.05, allow_runtime_cycle_edit: true}
"""


class RuntimeConfigTest(unittest.TestCase):
    def _config_path(self, text: str = CONFIG) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp_dir = tempfile.TemporaryDirectory()
        path = Path(temp_dir.name) / "vplc.yaml"
        path.write_text(text)
        return temp_dir, path

    def test_normal_profile_loads_controlled_station_baseline(self) -> None:
        temp_dir, path = self._config_path()
        self.addCleanup(temp_dir.cleanup)

        config = load_runtime_config(path)

        self.assertEqual("normal", config.profile)
        self.assertEqual(1.0, config.cycle_scale)
        self.assertFalse(config.allow_runtime_cycle_edit)
        self.assertEqual(30.4, config.stations["WS01"].base_cycle_s)
        self.assertEqual(str(path), config.source)
        self.assertEqual(64, len(config.config_hash))

    def test_fast_profile_keeps_process_baseline_and_changes_only_scale(self) -> None:
        temp_dir, path = self._config_path()
        self.addCleanup(temp_dir.cleanup)

        config = load_runtime_config(path, profile_override="fast")

        self.assertEqual("fast", config.profile)
        self.assertEqual(0.1, config.cycle_scale)
        self.assertTrue(config.allow_runtime_cycle_edit)
        self.assertEqual(30.4, config.stations["WS01"].base_cycle_s)

    def test_normal_profile_rejects_non_unit_scale(self) -> None:
        temp_dir, path = self._config_path()
        self.addCleanup(temp_dir.cleanup)

        with self.assertRaisesRegex(ValueError, "normal profile requires cycle_scale=1.0"):
            load_runtime_config(path, cycle_scale_override=0.1)

    def test_normal_profile_rejects_unsafe_station_cycle(self) -> None:
        temp_dir, path = self._config_path(CONFIG.replace("base_cycle_s: 30.4", "base_cycle_s: 1.0"))
        self.addCleanup(temp_dir.cleanup)

        with self.assertRaisesRegex(ValueError, "WS01 base_cycle_s"):
            load_runtime_config(path)

    def test_pipeline_uses_resolved_config_and_blocks_normal_cycle_edit(self) -> None:
        temp_dir, path = self._config_path()
        self.addCleanup(temp_dir.cleanup)
        config = load_runtime_config(path)
        pipeline = ThreeStationPipeline(
            scale=config.cycle_scale,
            profile=config.profile,
            allow_runtime_cycle_edit=config.allow_runtime_cycle_edit,
            station_parameters=config.station_dict(),
            config_source=config.source,
            config_hash=config.config_hash,
        )

        self.assertEqual(30.4, pipeline.stations["WS01"].base_cycle_s)
        with self.assertRaisesRegex(ValueError, "normal profile"):
            pipeline.update_station("WS01", {"base_cycle_s": 1.0})
        self.assertEqual(30.4, pipeline.stations["WS01"].base_cycle_s)

    def test_fast_profile_allows_runtime_cycle_edit(self) -> None:
        temp_dir, path = self._config_path()
        self.addCleanup(temp_dir.cleanup)
        config = load_runtime_config(path, profile_override="fast")
        pipeline = ThreeStationPipeline(
            scale=config.cycle_scale,
            profile=config.profile,
            allow_runtime_cycle_edit=config.allow_runtime_cycle_edit,
            station_parameters=config.station_dict(),
        )

        pipeline.update_station("WS01", {"base_cycle_s": 5.0, "jitter_s": 0.0})

        self.assertEqual(5.0, pipeline.stations["WS01"].base_cycle_s)
        self.assertEqual(0.0, pipeline.stations["WS01"].jitter_s)

    def test_control_page_omits_locked_cycle_fields_from_normal_update(self) -> None:
        self.assertIn("if (currentState.allow_runtime_cycle_edit)", CONTROL_HTML)


if __name__ == "__main__":
    unittest.main()
