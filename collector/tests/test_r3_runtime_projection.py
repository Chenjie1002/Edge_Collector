from __future__ import annotations

from pathlib import Path

from app.plc.mapping import parse_edge_mapping
from app.plc.read_plan import build_read_plans
from app.services.resolved_config_registry import CompletionPolicy, build_resolved_config_snapshot_from_mapping
from common.line_config import load_line_config
from common.line_config.runtime_layout import default_runtime_layout_registry
from common.line_config.runtime_projection import compile_runtime_mapping


def _projection10() -> dict[str, object]:
    config = load_line_config(Path("config/lines/demo_10_station.yaml"))
    return compile_runtime_mapping(
        config,
        {
            "host": "s7-plc-sim",
            "port": 1102,
            "rack": 0,
            "slot": 1,
            "connection_timeout_ms": 2500,
            "poll_interval_ms": 500,
        },
        default_runtime_layout_registry(),
    ).document


def test_projected_10ws_mapping_builds_line_plus_ten_read_plans() -> None:
    mapping = parse_edge_mapping(_projection10())
    plans = build_read_plans(mapping)

    assert [plan.scope for plan in plans] == [
        "line",
        *[f"WS{index:02d}" for index in range(1, 11)],
    ]
    assert len(plans) == 11
    assert plans[-1].db_number == 111
    assert plans[-1].read_size > 32


def test_projected_10ws_terminal_policy_is_ws10() -> None:
    mapping = parse_edge_mapping(_projection10())
    resolved = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    policy = CompletionPolicy.from_snapshot(resolved)

    assert policy.entry_station_id == "WS01"
    assert policy.terminal_station_id == "WS10"


def test_projected_10ws_decoder_selects_generic_binding_by_payload_template() -> None:
    mapping = parse_edge_mapping(_projection10())
    resolved = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)
    ws10_plan = next(plan for plan in build_read_plans(mapping) if plan.scope == "WS10")

    decoded = resolved.decode_raw_payload(
        {"raw_hex": bytes(ws10_plan.read_size).hex()},
        {
            "station_id": "WS10",
            "correlation": {"payload_template": "generic_status_v1"},
        },
    )

    assert decoded["status_word"] == 0
