from __future__ import annotations

import json
from pathlib import Path
import unittest


DASHBOARD_PATH = Path(
    "config/grafana/dashboards/edge_mes_station_traceability.json"
)


class GrafanaProfileFilterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dashboard = json.loads(DASHBOARD_PATH.read_text())

    def test_profile_filter_defaults_to_normal_and_supports_all_profiles(self) -> None:
        variables = {
            item["name"]: item
            for item in self.dashboard["templating"]["list"]
        }

        profile = variables["profile"]

        self.assertEqual("normal", profile["current"]["value"])
        self.assertTrue(profile["includeAll"])
        self.assertEqual("all", profile["allValue"])
        self.assertIn("normal", profile["query"])
        self.assertIn("fast", profile["query"])
        self.assertIn("test", profile["query"])
        self.assertIn("unknown", profile["query"])

    def test_cycle_event_panels_apply_profile_scope(self) -> None:
        affected_panels = []
        for panel in self.dashboard["panels"]:
            if panel["title"] == "时间窗 Profile 构成":
                continue
            for target in panel.get("targets", []):
                sql = target.get("rawSql", "")
                if "cycle_event" not in sql:
                    continue
                affected_panels.append(panel["title"])
                self.assertIn(
                    "${profile}",
                    sql,
                    f"{panel['title']} does not use the Profile filter",
                )
                self.assertIn(
                    "vplc_parameter_snapshot",
                    sql,
                    f"{panel['title']} does not map boot identity to Profile",
                )

        self.assertGreaterEqual(len(affected_panels), 10)

    def test_dashboard_exposes_current_profile_and_mixed_window_status(self) -> None:
        panels = {panel["title"]: panel for panel in self.dashboard["panels"]}

        current_profile_sql = panels["当前 V-PLC Profile"]["targets"][0]["rawSql"]
        window_scope_sql = panels["时间窗 Profile 构成"]["targets"][0]["rawSql"]

        self.assertIn("collector_runtime_status", current_profile_sql)
        self.assertIn("vplc_parameter_snapshot", current_profile_sql)
        self.assertIn("MIXED", window_scope_sql)
        self.assertIn("$__timeFilter", window_scope_sql)
        self.assertIn("vplc_parameter_snapshot", window_scope_sql)
        self.assertNotIn("${profile}", window_scope_sql)

    def test_recent_trace_table_respects_dashboard_time_window(self) -> None:
        panel = next(
            panel
            for panel in self.dashboard["panels"]
            if panel["title"] == "最近产品追溯记录"
        )
        sql = panel["targets"][0]["rawSql"]

        self.assertIn("$__timeFilter", sql)


if __name__ == "__main__":
    unittest.main()
