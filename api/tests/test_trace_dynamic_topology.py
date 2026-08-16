from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from unittest.mock import patch

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


def _event(station_id: str, route_step: int) -> dict[str, object]:
    return {
        "id": route_step,
        "station_id": station_id,
        "cycle_counter": route_step,
        "unit_id": "U-10WS-000001",
        "route_step": route_step,
        "result": "OK",
        "process_status": "PROCESSED",
        "plc_start_time": datetime(2026, 8, 16, tzinfo=timezone.utc),
        "plc_end_time": datetime(2026, 8, 16, tzinfo=timezone.utc),
        "payload": {"status_word": 1, "process_value": 2.5},
    }


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
