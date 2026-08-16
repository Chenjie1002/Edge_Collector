from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import re
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


LINE_ID = "LINE_001"
START = datetime(2026, 8, 16, 10, 0, tzinfo=timezone.utc)
END = datetime(2026, 8, 16, 11, 0, tzinfo=timezone.utc)
STATION_IDS = ("WS01", "WS02", "WS03")


def scope_catalog() -> dict[str, object]:
    return {
        "lines": [
            {
                "line_id": LINE_ID,
                "name": "Demo Line",
                "stations": [
                    {"station_id": station_id, "name": station_id, "station_order": index}
                    for index, station_id in enumerate(STATION_IDS, start=1)
                ],
            }
        ]
    }


def station_row(
    unit_id: str,
    station_id: str,
    route_step: int,
    *,
    result: str = "OK",
    process_status: str = "PROCESSED",
    skip_reason: str = "NONE",
    defect_origin_station: str = "",
    defect_code: int = 0,
    terminal: bool = False,
) -> dict[str, object]:
    return {
        "cohort_unit_id": unit_id,
        "cohort_plc_id": "PLC_001",
        "cohort_line_id": LINE_ID,
        "cohort_plc_boot_id": "BOOT_001",
        "cohort_completed_at": START,
        "station_event_id": f"event-{unit_id}-{station_id}",
        "unit_id": unit_id,
        "plc_id": "PLC_001",
        "line_id": LINE_ID,
        "plc_boot_id": "BOOT_001",
        "station_id": station_id,
        "route_step": route_step,
        "process_status": process_status,
        "result": result,
        "skip_reason": skip_reason,
        "defect_origin_station": defect_origin_station or None,
        "defect_code": defect_code,
        "route_state": "COMPLETED_NOK" if terminal and result != "OK" else "COMPLETED_OK" if terminal else "NORMAL",
        "plc_end_time": START,
        "cycle_time_ms": 30000 if process_status == "PROCESSED" else 4000,
        "ack_status": "ACK_OK",
        "label_code": f"ASM-{unit_id[-6:]}" if terminal else None,
        "reject_id": f"NG-{unit_id[-6:]}" if terminal and result != "OK" else None,
    }


def unit_rows(
    unit_id: str,
    *,
    first_nok_station: str | None = None,
    legacy_skip: bool = False,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    defect_code = 0
    for index, station_id in enumerate(STATION_IDS, start=1):
        if first_nok_station is None:
            rows.append(station_row(unit_id, station_id, index, terminal=station_id == "WS03"))
            continue
        if station_id == first_nok_station:
            defect_code = 10001 if station_id == "WS01" else 20001
            rows.append(
                station_row(
                    unit_id,
                    station_id,
                    index,
                    result="NOK",
                    defect_origin_station=station_id,
                    defect_code=defect_code,
                    terminal=station_id == "WS03",
                )
            )
            continue
        if index > STATION_IDS.index(first_nok_station) + 1:
            rows.append(
                station_row(
                    unit_id,
                    station_id,
                    index,
                    result="SKIPPED" if legacy_skip else "NOK",
                    process_status="SKIPPED",
                    skip_reason="UPSTREAM_NOK",
                    defect_origin_station=first_nok_station,
                    defect_code=defect_code,
                    terminal=station_id == "WS03",
                )
            )
            continue
        rows.append(station_row(unit_id, station_id, index, terminal=station_id == "WS03"))
    return rows


class FakeCursor:
    def __init__(self, database: "FakeDatabase") -> None:
        self.database = database
        self.rows: list[dict[str, object]] = []

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def execute(self, sql: str, params: tuple | list | None = None) -> None:
        values = tuple(params or ())
        self.database.queries.append((sql, values))
        upper_sql = sql.upper()
        if re.search(r"\b(?:INSERT|UPDATE|DELETE)\b", upper_sql):
            self.database.write_seen = True
        if "SELECT" not in upper_sql:
            return
        if self.database.fail_on_select is not None:
            raise self.database.fail_on_select
        self.database.select_sql = sql
        self.database.select_params = values
        if "FROM COLLECTOR_RUNTIME_STATUS" in upper_sql:
            self.rows = deepcopy(self.database.runtime_rows)
        elif "FROM VPLC_PARAMETER_SNAPSHOT" in upper_sql:
            self.rows = deepcopy(self.database.profile_rows)
        else:
            self.rows = deepcopy(self.database.rows)

    def fetchall(self) -> list[dict[str, object]]:
        return list(self.rows)


class FakeConnection:
    def __init__(self, database: "FakeDatabase") -> None:
        self.database = database

    def cursor(self) -> FakeCursor:
        return FakeCursor(self.database)


class FakeDatabase:
    def __init__(
        self,
        rows: list[dict[str, object]],
        *,
        runtime_rows: list[dict[str, object]] | None = None,
        profile_rows: list[dict[str, object]] | None = None,
        fail_on_select: Exception | None = None,
    ) -> None:
        self.rows = rows
        self.runtime_rows = runtime_rows or []
        self.profile_rows = profile_rows or []
        self.fail_on_select = fail_on_select
        self.queries: list[tuple[str, tuple]] = []
        self.select_sql = ""
        self.select_params: tuple = ()
        self.write_seen = False

    @contextmanager
    def get_conn(self):
        yield FakeConnection(self)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def request_summary(client: TestClient, database: FakeDatabase, **params: object):
    query = {
        "line_id": LINE_ID,
        "start_time": "2026-08-16T10:00:00Z",
        "end_time": "2026-08-16T11:00:00Z",
    }
    query.update(params)
    with patch("app.db.get_conn", database.get_conn), patch(
        "app.routes.line_summary.load_scope_catalog", return_value=scope_catalog()
    ):
        return client.get("/api/v2/production/line-summary", params=query)


@pytest.mark.parametrize(
    "rows",
    [
        unit_rows("U-ALL-OK"),
        unit_rows("U-WS01-NOK", first_nok_station="WS01"),
        unit_rows("U-WS02-NOK", first_nok_station="WS02"),
        unit_rows("U-MIXED-OK") + unit_rows("U-MIXED-NOK", first_nok_station="WS02"),
    ],
    ids=["all_ok", "ws01_nok", "middle_nok", "mixed"],
)
def test_line_summary_uses_one_terminal_completed_cohort_and_conserves_units(
    client: TestClient,
    rows: list[dict[str, object]],
) -> None:
    database = FakeDatabase(rows)

    response = request_summary(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["scope"]["cohort_basis"] == "terminal_completed"
    assert payload["topology"]["stations"] == list(STATION_IDS)
    assert payload["cohort"]["unit_count"] == len({row["cohort_unit_id"] for row in rows})
    assert payload["cohort"]["reconciliation_status"] == "PASS"
    assert [station["station_id"] for station in payload["stations"]] == list(STATION_IDS)
    for station in payload["stations"]:
        assert station["total"] == payload["cohort"]["unit_count"]
        assert station["ok"] + station["nok"] == station["total"]
        assert station["processed"] + station["skipped"] == station["total"]
        assert station["reconciliation_status"] == "PASS"
    assert database.write_seen is False
    assert "FROM station_event" in database.select_sql
    assert "terminal_cohort" in database.select_sql
    assert "ce.route_state" in database.select_sql
    assert "se.route_state" not in database.select_sql


def test_line_summary_exposes_product_overview_trends_and_station_local_metrics(
    client: TestClient,
) -> None:
    rows = unit_rows("U-000001") + unit_rows("U-000002", first_nok_station="WS02")
    database = FakeDatabase(rows)

    response = request_summary(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["line"] == {
        "line_id": LINE_ID,
        "name": "Demo Line",
        "station_count": 3,
        "route": list(STATION_IDS),
        "entry_station_id": "WS01",
        "terminal_station_id": "WS03",
        "active_profile": "UNAVAILABLE",
        "collector_state": "UNAVAILABLE",
        "collector_connected_stations": 0,
        "runtime_status": "UNAVAILABLE",
        "runtime_authority": "collector_runtime_status",
        "mapping_content_sha256": None,
        "config_version": None,
    }
    assert payload["overview"]["completed_units"] == 2
    assert payload["overview"]["final_ok"] == 1
    assert payload["overview"]["final_nok"] == 1
    assert payload["overview"]["final_yield"] == 0.5
    assert payload["overview"]["ack_pending_events"] == 0
    assert payload["overview"]["average_cycle_seconds"] == 30.0
    assert payload["trends"]["production"]
    assert payload["trends"]["production_by_station"] == [
        {"bucket_start": "2026-08-16T10:00:00Z", "station_id": "WS01", "completed": 2, "ok": 2, "nok": 0},
        {"bucket_start": "2026-08-16T10:00:00Z", "station_id": "WS02", "completed": 2, "ok": 1, "nok": 1},
        {"bucket_start": "2026-08-16T10:00:00Z", "station_id": "WS03", "completed": 2, "ok": 1, "nok": 1},
    ]
    assert payload["trends"]["cycle_time"]
    assert payload["quality"]["new_nok_by_station"] == [
        {"station_id": "WS01", "count": 0},
        {"station_id": "WS02", "count": 1},
        {"station_id": "WS03", "count": 0},
    ]
    assert payload["quality"]["nok_code_distribution"] == [{"code": 20001, "count": 1}]
    assert payload["recent_completed_units"][0]["unit_id"] in {"U-000001", "U-000002"}
    ws02 = payload["stations"][1]
    assert ws02["average_cycle_seconds"] == 30.0
    assert ws02["local_nok_rate"] == 0.5
    assert ws02["activity_trend"]
    assert ws02["recent_records"]


def test_line_summary_classifies_legacy_proven_upstream_skip_as_inherited_nok(
    client: TestClient,
) -> None:
    database = FakeDatabase(unit_rows("U-LEGACY-SKIP", first_nok_station="WS01", legacy_skip=True))

    response = request_summary(client, database)

    assert response.status_code == 200
    ws02 = response.json()["stations"][1]
    assert ws02["result_compatibility"] == "legacy_skipped_classified_as_inherited_nok"
    assert ws02["nok"] == 1
    assert ws02["skipped"] == 1
    assert ws02["new_nok"] == 0


def test_line_summary_keeps_total_at_cohort_size_and_reports_missing_evidence(
    client: TestClient,
) -> None:
    rows = unit_rows("U-COMPLETE") + unit_rows("U-MISSING", first_nok_station="WS01")
    rows = [row for row in rows if not (row["cohort_unit_id"] == "U-MISSING" and row["station_id"] == "WS02")]
    database = FakeDatabase(rows)

    response = request_summary(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["cohort"]["unit_count"] == 2
    assert payload["cohort"]["reconciliation_status"] == "FAIL"
    ws02 = payload["stations"][1]
    assert ws02["total"] == 2
    assert ws02["missing_unit_count"] == 1
    assert ws02["reconciliation_status"] == "FAIL"
    assert "missing trusted WS02 station evidence" in payload["cohort"]["errors"][0]


def test_line_summary_rejects_unsupported_query_without_db_access(client: TestClient) -> None:
    database = FakeDatabase([])

    response = request_summary(client, database, station_id="WS01")

    assert response.status_code == 422
    assert database.queries == []


def test_line_summary_returns_unavailable_when_read_source_fails(client: TestClient) -> None:
    database = FakeDatabase([], fail_on_select=RuntimeError("database unavailable"))

    response = request_summary(client, database)

    assert response.status_code == 503
    assert response.json() == {"detail": "line summary source unavailable"}


def test_line_summary_exposes_line_runtime_state_from_collector_authority(client: TestClient) -> None:
    runtime_now = datetime.now(timezone.utc)
    database = FakeDatabase(
        unit_rows("U-RUNTIME-STATE"),
        runtime_rows=[
            {
                "station_id": station_id,
                "collector_state": "RUNNING",
                "plc_connection_state": "CONNECTED",
                "station_status": "RUNNING",
                "updated_at": runtime_now,
            }
            for station_id in STATION_IDS
        ],
    )

    response = request_summary(client, database)

    assert response.status_code == 200
    assert response.json()["line"]["runtime_status"] == "RUNNING"
    assert response.json()["line"]["runtime_authority"] == "collector_runtime_status"


def test_line_summary_exposes_stopped_runtime_state_without_using_recent_data(client: TestClient) -> None:
    runtime_now = datetime.now(timezone.utc)
    database = FakeDatabase(
        unit_rows("U-RECENT-DATA-BUT-STOPPED"),
        runtime_rows=[
            {
                "station_id": station_id,
                "collector_state": "STOPPED",
                "plc_connection_state": "DISCONNECTED",
                "station_status": "OFFLINE",
                "updated_at": runtime_now,
            }
            for station_id in STATION_IDS
        ],
    )

    response = request_summary(client, database)

    assert response.status_code == 200
    assert response.json()["line"]["runtime_status"] == "STOPPED"
