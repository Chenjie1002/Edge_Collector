from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import os
from pathlib import Path
from unittest.mock import patch

import yaml

from app.routes import trace


class _Cursor:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self.rows = rows

    def __enter__(self) -> "_Cursor":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def execute(self, *_args: object) -> None:
        return None

    def fetchall(self) -> list[dict[str, object]]:
        return self.rows


class _Connection:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self.rows = rows

    def cursor(self) -> _Cursor:
        return _Cursor(self.rows)


def _event(
    station_id: str,
    route_step: int,
    *,
    unit_id: str = "U-10WS-000001",
    plc_id: str = "PLC_001",
    line_id: str = "LINE_DEMO_10",
    plc_boot_id: str = "BOOT_10",
    result: str = "OK",
    route_state: str = "NORMAL",
    process_status: str = "PROCESSED",
    skip_reason: str = "NONE",
    defect_origin_station: str = "UNKNOWN",
    defect_code: int = 0,
    payload: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "id": route_step,
        "plc_id": plc_id,
        "line_id": line_id,
        "station_id": station_id,
        "plc_boot_id": plc_boot_id,
        "cycle_counter": route_step,
        "unit_id": unit_id,
        "route_step": route_step,
        "result": result,
        "route_state": route_state,
        "process_status": process_status,
        "skip_reason": skip_reason,
        "defect_origin_station": defect_origin_station,
        "defect_code": defect_code,
        "plc_start_time": datetime(2026, 8, 16, tzinfo=timezone.utc),
        "plc_end_time": datetime(2026, 8, 16, tzinfo=timezone.utc),
        "payload": payload or {"status_word": 1, "process_value": 2.5},
    }


def _mapping_document(*, line_id: str, station_count: int, config_version: str) -> dict[str, object]:
    station_ids = [f"WS{index:02d}" for index in range(1, station_count + 1)]
    return {
        "config_version": config_version,
        "line_id": line_id,
        "line": {"name": line_id},
        "plcs": [{"plc_id": "PLC_001"}],
        "stations": [
            {"station_id": station_id, "station_order": index}
            for index, station_id in enumerate(station_ids, start=1)
        ],
        "route_graph": {
            "entry_station_id": station_ids[0],
            "terminal_station_id": station_ids[-1],
            "edges": [
                {"from_station_id": left, "to_station_id": right}
                for left, right in zip(station_ids, station_ids[1:])
            ],
        },
        "entry_station_id": station_ids[0],
        "terminal_station_id": station_ids[-1],
    }


def _write_history_fixture(tmp_path: Path) -> Path:
    baseline = tmp_path / "config" / "mapping.yaml"
    active = tmp_path / "data" / "deployment-config" / "active" / "mapping.yaml"
    backup = tmp_path / "data" / "deployment-config" / "backups" / "historical-10ws.yaml"
    baseline.parent.mkdir(parents=True)
    active.parent.mkdir(parents=True)
    backup.parent.mkdir(parents=True)
    three_ws = _mapping_document(
        line_id="LINE_001",
        station_count=3,
        config_version="current-3ws",
    )
    ten_ws = _mapping_document(
        line_id="LINE_DEMO_10",
        station_count=10,
        config_version="historical-10ws",
    )
    for path, document in ((baseline, three_ws), (active, three_ws), (backup, ten_ws)):
        path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return baseline


class _ScopedCursor(_Cursor):
    def __init__(self, rows: list[dict[str, object]]) -> None:
        super().__init__(rows)
        self.all_rows = rows

    def execute(self, sql: str, params: tuple | list | None = None) -> None:
        values = tuple(params or ())
        requested_scope = {
            value
            for value in values
            if value in {"PLC_A", "LINE_DEMO_10", "LINE_001", "BOOT_A", "BOOT_B"}
        }
        if "FROM cycle_event" in sql and "WHERE unit_id = %s" in sql and requested_scope:
            self.rows = [
                row
                for row in self.all_rows
                if row.get("plc_id") in requested_scope
                or row.get("line_id") in requested_scope
                or row.get("plc_boot_id") in requested_scope
            ]
        else:
            self.rows = list(self.all_rows)


class _ScopedConnection(_Connection):
    def cursor(self) -> _ScopedCursor:
        return _ScopedCursor(self.rows)


def test_trace_uses_ordered_active_10ws_topology_and_explicit_gap() -> None:
    topology = trace.TraceTopology(
        station_ids=tuple(f"WS{index:02d}" for index in range(1, 11)),
        entry_station_id="WS01",
        terminal_station_id="WS10",
        edges=tuple(
            (f"WS{index:02d}", f"WS{index + 1:02d}")
            for index in range(1, 10)
        ),
    )
    rows = [_event(f"WS{index:02d}", index) for index in range(1, 11) if index != 6]

    @contextmanager
    def get_conn():
        yield _Connection(rows)

    with patch.object(trace, "_load_trace_topology", return_value=topology), patch.object(
        trace, "get_conn", get_conn
    ):
        result = trace._trace_by_unit("U-10WS-000001", "U-10WS-000001")

    assert list(result["stations"]) == [f"WS{index:02d}" for index in range(1, 11)]
    assert result["stations"]["WS06"] is None
    assert [event["station_id"] for event in result["events"]] == [
        f"WS{index:02d}" for index in range(1, 11) if index != 6
    ]
    assert result["stations"]["WS10"]["payload"] == {
        "process_value": 2.5,
        "status_word": 1,
    }


def test_trace_page_renders_station_ids_from_response_not_fixed_three_station_list() -> None:
    assert "const stations = [\"WS01\", \"WS02\", \"WS03\"]" not in trace.TRACE_HTML
    assert "Object.keys(data.stations || {})" in trace.TRACE_HTML


def test_trace_page_places_recent_records_before_one_continuous_selected_unit_trace() -> None:
    recent_index = trace.TRACE_HTML.index('id="recentPanel"')
    selected_index = trace.TRACE_HTML.index('id="selectedTrace"')
    assert recent_index < selected_index
    assert 'id="unitSummary"' in trace.TRACE_HTML
    assert 'class="trace-route"' in trace.TRACE_HTML
    assert "Technical details" in trace.TRACE_HTML
    assert "scrollIntoView" in trace.TRACE_HTML
    assert 'class="timeline"' not in trace.TRACE_HTML


def test_historical_10ws_trace_survives_current_3ws_topology(tmp_path: Path) -> None:
    baseline = _write_history_fixture(tmp_path)
    seed = _event("WS10", 10, unit_id="U-HIST-10", line_id="LINE_DEMO_10", plc_boot_id="BOOT_10")
    rows = [
        _event(
            f"WS{index:02d}",
            index,
            unit_id="U-HIST-10",
            line_id="LINE_DEMO_10",
            plc_boot_id="BOOT_10",
        )
        for index in range(1, 11)
    ]

    @contextmanager
    def get_conn():
        yield _ScopedConnection(rows)

    history_store = baseline.parent.parent / "data" / "deployment-config"
    with patch.dict(os.environ, {"DEPLOYMENT_CONFIG_DIR": str(history_store)}), patch.object(
        trace, "_trace_mapping_path", return_value=baseline
    ), patch.object(
        trace, "_find_seed_event", return_value=seed
    ), patch.object(trace, "get_conn", get_conn):
        result = trace.trace_query("U-HIST-10")

    assert list(result["stations"]) == [f"WS{index:02d}" for index in range(1, 11)]
    assert result["stations"]["WS10"]["route_state"] == "NORMAL"


def test_historical_10ws_nok_skip_chain_survives_current_3ws_topology(tmp_path: Path) -> None:
    baseline = _write_history_fixture(tmp_path)
    unit_id = "U-HIST-NOK-10"
    seed = _event("WS10", 10, unit_id=unit_id, line_id="LINE_DEMO_10", plc_boot_id="BOOT_10")
    rows = []
    for index in range(1, 11):
        nok = index == 5
        skipped = index >= 6
        rows.append(
            _event(
                f"WS{index:02d}",
                index,
                unit_id=unit_id,
                line_id="LINE_DEMO_10",
                plc_boot_id="BOOT_10",
                result="NOK" if nok else ("SKIPPED" if skipped else "OK"),
                route_state="COMPLETED_NOK" if index == 10 else ("BYPASSING" if nok or skipped else "NORMAL"),
                process_status="SKIPPED" if skipped else "PROCESSED",
                skip_reason="UPSTREAM_NOK" if skipped else "NONE",
                defect_origin_station="WS05" if nok or skipped else "UNKNOWN",
                defect_code=11001 if nok or skipped else 0,
            )
        )

    @contextmanager
    def get_conn():
        yield _ScopedConnection(rows)

    history_store = baseline.parent.parent / "data" / "deployment-config"
    with patch.dict(os.environ, {"DEPLOYMENT_CONFIG_DIR": str(history_store)}), patch.object(
        trace, "_trace_mapping_path", return_value=baseline
    ), patch.object(
        trace, "_find_seed_event", return_value=seed
    ), patch.object(trace, "get_conn", get_conn):
        result = trace.trace_query(unit_id)

    assert [event["station_id"] for event in result["events"]] == [
        f"WS{index:02d}" for index in range(1, 11)
    ]
    assert result["stations"]["WS05"]["result"] == "NOK"
    assert result["stations"]["WS10"]["result"] == "SKIPPED"
    assert result["stations"]["WS10"]["route_state"] == "COMPLETED_NOK"


def test_duplicate_unit_scopes_are_not_silently_merged(tmp_path: Path) -> None:
    baseline = _write_history_fixture(tmp_path)
    unit_id = "U-COLLISION"
    seed = _event(
        "WS10",
        10,
        unit_id=unit_id,
        plc_id="PLC_001",
        line_id="LINE_DEMO_10",
        plc_boot_id="BOOT_A",
    )
    scope_a = [
        _event(
            f"WS{index:02d}",
            index,
            unit_id=unit_id,
            plc_id="PLC_001",
            line_id="LINE_DEMO_10",
            plc_boot_id="BOOT_A",
        )
        for index in range(1, 11)
    ]
    scope_b = [
        _event(
            f"WS{index:02d}",
            index,
            unit_id=unit_id,
            plc_id="PLC_B",
            line_id="LINE_001",
            plc_boot_id="BOOT_B",
        )
        for index in range(1, 4)
    ]

    @contextmanager
    def get_conn():
        yield _ScopedConnection(scope_a + scope_b)

    history_store = baseline.parent.parent / "data" / "deployment-config"
    with patch.dict(os.environ, {"DEPLOYMENT_CONFIG_DIR": str(history_store)}), patch.object(
        trace, "_trace_mapping_path", return_value=baseline
    ), patch.object(
        trace, "_find_seed_event", return_value=seed
    ), patch.object(trace, "get_conn", get_conn):
        result = trace.trace_query(unit_id)

    assert len(result["events"]) == 10
    assert {event["line_id"] for event in result["events"]} == {"LINE_DEMO_10"}
    assert {event["plc_boot_id"] for event in result["events"]} == {"BOOT_A"}


def test_current_3ws_trace_keeps_rich_payload() -> None:
    topology = trace.TraceTopology(
        station_ids=("WS01", "WS02", "WS03"),
        entry_station_id="WS01",
        terminal_station_id="WS03",
        edges=(("WS01", "WS02"), ("WS02", "WS03")),
    )
    rows = [
        _event(
            "WS01",
            1,
            line_id="LINE_001",
            plc_boot_id="BOOT_3",
            payload={"screw_1_torque_nm": 1.52, "screw_1_angle_deg": 93.0},
        ),
        _event(
            "WS02",
            2,
            line_id="LINE_001",
            plc_boot_id="BOOT_3",
            payload={"avg_current_a": 2.57, "avg_voltage_v": 23.8},
        ),
        _event(
            "WS03",
            3,
            line_id="LINE_001",
            plc_boot_id="BOOT_3",
            payload={"serial_no": 14001, "product_model_code": 1},
        ),
    ]

    @contextmanager
    def get_conn():
        yield _Connection(rows)

    with patch.object(trace, "_load_trace_topology", return_value=topology), patch.object(
        trace, "get_conn", get_conn
    ):
        result = trace._trace_by_unit("U-10WS-000001", "U-10WS-000001")

    assert result["stations"]["WS01"]["payload"]["screw_1_torque_nm"] == 1.52
    assert result["stations"]["WS02"]["payload"]["avg_voltage_v"] == 23.8
    assert result["stations"]["WS03"]["payload"]["serial_no"] == 14001
