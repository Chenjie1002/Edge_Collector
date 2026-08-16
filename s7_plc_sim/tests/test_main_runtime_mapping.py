from __future__ import annotations

import unittest

from app.main import _runtime_db_number, _station_db_specs


class MainRuntimeMappingTest(unittest.TestCase):
    def test_projected_station_dbs_are_dynamic_and_sized_from_layout(self) -> None:
        mapping = {
            "line": {"db_number": 104},
            "plcs": [{"runtime_db": 104}],
            "stations": [
                {
                    "station_id": f"WS{index:02d}",
                    "db_number": 100 + index if index <= 3 else 101 + index,
                    "effective_read_size_bytes": 512 if index == 1 else 320,
                    "station_enabled": True,
                }
                for index in range(1, 11)
            ],
        }

        self.assertEqual(104, _runtime_db_number(mapping))
        self.assertEqual(
            {
                (100 + index if index <= 3 else 101 + index): 512
                for index in range(1, 11)
            },
            _station_db_specs(mapping),
        )

    def test_disabled_station_is_not_registered(self) -> None:
        mapping = {
            "plcs": [{"runtime_db": 204}],
            "stations": [
                {"station_id": "WS01", "db_number": 201, "station_enabled": True},
                {"station_id": "WS02", "db_number": 202, "station_enabled": False},
            ],
        }

        self.assertEqual({201: 512}, _station_db_specs(mapping))


if __name__ == "__main__":
    unittest.main()
