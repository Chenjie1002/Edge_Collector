from __future__ import annotations

from app.control_api import CONTROL_HTML


def test_control_page_renders_station_and_nok_capabilities_from_state() -> None:
    assert 'const stations = ["WS01", "WS02", "WS03"]' not in CONTROL_HTML
    assert "state.topology.station_ids" in CONTROL_HTML
    assert "station.nok_codes" in CONTROL_HTML
    assert "station.allow_force" in CONTROL_HTML
    assert "topology.edges" in CONTROL_HTML
    assert "state.wip[key]" in CONTROL_HTML
