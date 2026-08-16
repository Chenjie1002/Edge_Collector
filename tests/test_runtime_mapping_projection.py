from __future__ import annotations

from pathlib import Path

import pytest

from common.line_config import load_line_config
from common.line_config.runtime_layout import default_runtime_layout_registry
from common.line_config.runtime_projection import (
    RuntimeProjectionError,
    compile_runtime_mapping,
)


ROOT = Path(__file__).resolve().parents[1]
LINES = ROOT / "config" / "lines"


def _connectivity() -> dict[str, object]:
    return {
        "host": "s7-plc-sim",
        "port": 1102,
        "rack": 0,
        "slot": 1,
        "connection_timeout_ms": 2500,
        "poll_interval_ms": 500,
    }


def test_demo10_projection_is_deterministic_and_lineconfig_owned() -> None:
    config = load_line_config(LINES / "demo_10_station.yaml")
    registry = default_runtime_layout_registry()

    projection = compile_runtime_mapping(config, _connectivity(), registry)
    replay = compile_runtime_mapping(config, _connectivity(), registry)

    assert projection.document["line_id"] == "LINE_DEMO_10"
    assert projection.document["entry_station_id"] == "WS01"
    assert projection.document["terminal_station_id"] == "WS10"
    assert [station["station_id"] for station in projection.document["stations"]] == [
        f"WS{i:02d}" for i in range(1, 11)
    ]
    assert len(projection.document["route_graph"]) == 9
    assert projection.projection_hash == replay.projection_hash
    assert projection.projection_hash.startswith("sha256:")
    assert projection.document["line_config_hash"] == f"sha256:{config.config_hash}"

    stations = {station["station_id"]: station for station in projection.document["stations"]}
    assert stations["WS10"]["db_number"] == 111
    assert stations["WS10"]["payload_template"] == "generic_status_v1"
    assert "status_word" in stations["WS10"]["payload"]
    assert stations["WS10"]["effective_read_size_bytes"] > 32


def test_demo3_projection_preserves_rich_payload_profiles_and_db_allocations() -> None:
    config = load_line_config(LINES / "demo_3_station.yaml")
    projection = compile_runtime_mapping(
        config,
        _connectivity(),
        default_runtime_layout_registry(),
    )

    assert projection.document["entry_station_id"] == "WS01"
    assert projection.document["terminal_station_id"] == "WS03"
    assert [station["db_number"] for station in projection.document["stations"]] == [
        101,
        102,
        103,
    ]
    assert projection.document["stations"][0]["payload"]["screw_1_torque_nm"]["address"] == (
        "DB101.DBD100"
    )
    assert projection.document["stations"][1]["payload"]["avg_current_a"]["address"] == (
        "DB102.DBD100"
    )
    assert projection.document["stations"][2]["payload"]["serial_no"]["address"] == (
        "DB103.DBD100"
    )
    assert projection.document["plcs"][0]["runtime_db"] == 104


def test_multi_plc_stress_config_is_rejected_before_projection() -> None:
    config = load_line_config(LINES / "stress_20_station.yaml")

    with pytest.raises(RuntimeProjectionError, match="MULTI_PLC_RUNTIME_UNSUPPORTED"):
        compile_runtime_mapping(
            config,
            _connectivity(),
            default_runtime_layout_registry(),
        )
