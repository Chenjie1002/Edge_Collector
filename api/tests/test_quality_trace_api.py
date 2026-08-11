from __future__ import annotations

import json
import re
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


DTO_FIELDS = {
    "line_id",
    "plc_id",
    "station_id",
    "station_type",
    "profile_id",
    "config_hash",
    "config_version",
    "event_type",
    "production_result",
    "unit_id",
    "dmc",
    "cycle_counter",
    "source_event_id",
    "event_ts",
    "accepted_at",
    "fact_key",
    "content_fingerprint",
    "nok_code",
    "nok_origin",
    "nok_detail_code",
    "nok_detail_source_event_id",
    "nok_detail_evidence_fact_key",
}

FORBIDDEN_SURFACES = {
    "raw_payload",
    "raw_hex",
    "disposition",
    "reason_code",
    "ack_status",
    "read_done",
    "payload",
    "quality_pareto_input",
    "dashboard_state",
}

FORBIDDEN_SOURCES = {
    "raw_plc_sample",
    "cycle_event",
    "station_event",
    "production_unit",
    "quality_event",
    "production_snapshot",
    "production_events",
}


def accepted_fact(**overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "line_id": "LINE_001",
        "plc_id": "PLC_001",
        "station_id": "WS01",
        "station_type": "ASSEMBLY",
        "profile_id": "normal",
        "config_hash": "sha256:config",
        "config_version": "2026.07.03.1",
        "event_type": "station_result",
        "production_result": "ok",
        "unit_id": "U-001",
        "dmc": "DMC-001",
        "cycle_counter": 301,
        "source_event_id": "PLC_001:WS01:301",
        "event_ts": datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
        "accepted_at": datetime(2026, 7, 3, 10, 0, 1, tzinfo=timezone.utc),
        "fact_key": "sha256:fact-001",
        "content_fingerprint": "sha256:content-001",
        "nok_code": None,
        "nok_origin": None,
        "nok_detail_code": None,
        "nok_detail_source_event_id": None,
        "nok_detail_evidence_fact_key": None,
        "raw_payload": {"raw_hex": "0001"},
        "raw_hex": "0001",
        "disposition": "accepted",
        "reason_code": "RAW_NORMALIZED_MISMATCH",
        "ack_status": "ACK_OK",
        "read_done": True,
        "quality_pareto_input": {"code": 30003},
        "dashboard_state": {"state": "leak"},
        "payload": {"legacy": True},
    }
    row.update(overrides)
    return row


class FakeCursor:
    def __init__(self, database: "FakeDatabase") -> None:
        self.database = database
        self.rows: list[dict[str, object]] = []

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def execute(self, sql: str, params: tuple | list | None = None) -> None:
        values = tuple(params or ())
        self.database.queries.append((sql, values))
        upper_sql = sql.upper()
        if any(token in upper_sql for token in ("INSERT", "UPDATE", "DELETE")):
            self.database.write_seen = True
        if "ACK" in upper_sql or "READ_DONE" in upper_sql:
            self.database.ack_read_done_seen = True
        if "SELECT" not in upper_sql:
            return
        if "FROM PRODUCTION_ACCEPTED_STATION_EVENT_FACT" not in upper_sql:
            self.rows = []
            return
        self.database.select_sql = sql
        self.database.select_params = values
        if self.database.fail_on_select is not None:
            raise self.database.fail_on_select
        if "PRODUCTION_RESULT, NOK_CODE, NOK_ORIGIN" in upper_sql:
            line_id, station_id, start_time, end_time = values
            self.rows = [
                deepcopy(row)
                for row in self.database.rows
                if row["line_id"] == line_id
                and row["station_id"] == station_id
                and row["event_type"] == "station_result"
                and row["event_ts"] >= start_time
                and row["event_ts"] < end_time
            ]
            return
        line_id, identity_value, start_time, end_time, limit = values
        identity_column = "dmc" if "DMC IS NOT NULL" in upper_sql else "unit_id"
        rows = [
            deepcopy(row)
            for row in self.database.rows
            if row["line_id"] == line_id
            and row[identity_column] is not None
            and row[identity_column] == identity_value
            and row["event_ts"] >= start_time
            and row["event_ts"] < end_time
        ]
        rows.sort(key=lambda row: (row["event_ts"], row["accepted_at"], row["fact_key"]))
        self.rows = rows[: int(limit)]

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
        rows: list[dict[str, object]] | None = None,
        *,
        fail_on_select: Exception | None = None,
    ) -> None:
        self.rows = rows or [accepted_fact()]
        self.fail_on_select = fail_on_select
        self.queries: list[tuple[str, tuple]] = []
        self.select_sql = ""
        self.select_params: tuple = ()
        self.write_seen = False
        self.ack_read_done_seen = False

    @contextmanager
    def get_conn(self):
        yield FakeConnection(self)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def request_quality(client: TestClient, database: FakeDatabase, **params: object):
    query = {
        "line_id": "LINE_001",
        "station_id": "WS01",
        "start_time": "2026-07-03T09:00:00Z",
        "end_time": "2026-07-03T11:00:00Z",
    }
    query.update(params)
    with patch("app.db.get_conn", database.get_conn):
        return client.get("/api/v2/production/quality", params=query)


def request_trace(client: TestClient, database: FakeDatabase, **params: object):
    query = {
        "line_id": "LINE_001",
        "unit_id": "U-001",
        "start_time": "2026-07-03T09:00:00Z",
        "end_time": "2026-07-03T11:00:00Z",
    }
    if "dmc" in params:
        query.pop("unit_id")
    query.update(params)
    with patch("app.db.get_conn", database.get_conn):
        return client.get("/api/v2/production/trace", params=query)


def test_quality_counts_rate_and_nok_distribution_use_accepted_station_results(
    client: TestClient,
) -> None:
    database = FakeDatabase(
        [
            accepted_fact(fact_key="fact-ok-1", production_result="ok"),
            accepted_fact(
                fact_key="fact-nok-1",
                production_result="nok",
                nok_code=30003,
                nok_origin="accepted_business",
            ),
            accepted_fact(
                fact_key="fact-nok-2",
                production_result="nok",
                nok_code=30003,
                nok_origin="accepted_business",
            ),
            accepted_fact(fact_key="fact-skip", production_result="skip"),
        ]
    )

    response = request_quality(client, database)

    assert response.status_code == 200
    assert response.json()["counts"] == {"ok": 1, "nok": 2, "denominator": 3}
    assert response.json()["quality_rate"] == pytest.approx(1 / 3)
    assert response.json()["nok_code_distribution"] == {"30003": 2}
    assert response.json()["data_sufficiency"] == "SUPPORTED"
    sql = database.select_sql.lower()
    assert "from production_accepted_station_event_fact" in sql
    assert "event_type = 'station_result'" in sql
    assert "event_ts >=" in sql and "event_ts <" in sql
    assert not any(re.search(rf"\b(from|join)\s+{source}\b", sql) for source in FORBIDDEN_SOURCES)


def test_quality_empty_denominator_is_unavailable_and_not_zero_quality(
    client: TestClient,
) -> None:
    database = FakeDatabase(
        [
            accepted_fact(fact_key="fact-skip", production_result="skip"),
            accepted_fact(fact_key="fact-na", production_result="not_applicable"),
        ]
    )

    response = request_quality(client, database)

    assert response.status_code == 200
    assert response.json()["counts"] == {"ok": 0, "nok": 0, "denominator": 0}
    assert response.json()["quality_rate"] is None
    assert response.json()["data_sufficiency"] == "UNAVAILABLE"


@pytest.mark.parametrize("identity", [{"unit_id": "U-001"}, {"dmc": "DMC-001"}])
def test_trace_exact_unit_or_dmc_lookup_and_stable_timeline_order(
    client: TestClient,
    identity: dict[str, str],
) -> None:
    rows = [
        accepted_fact(
            fact_key="fact-2",
            unit_id="U-001",
            dmc="DMC-001",
            station_id="WS02",
            event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
            accepted_at=datetime(2026, 7, 3, 10, 0, 2, tzinfo=timezone.utc),
        ),
        accepted_fact(
            fact_key="fact-1",
            unit_id="U-001",
            dmc="DMC-001",
            station_id="WS01",
            event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
            accepted_at=datetime(2026, 7, 3, 10, 0, 1, tzinfo=timezone.utc),
        ),
        accepted_fact(
            fact_key="other-unit",
            unit_id="U-999",
            dmc="DMC-999",
        ),
    ]

    response = request_trace(client, FakeDatabase(rows), **identity)

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert [item["fact_key"] for item in items] == ["fact-1", "fact-2"]
    sql = "\n".join(statement for statement, _ in FakeDatabase(rows).queries).lower()
    assert identity


@pytest.mark.parametrize(
    "params",
    [
        {"unit_id": ""},
        {"unit_id": "U-001", "dmc": "DMC-001"},
        {"unit_id": "  ", "dmc": "DMC-001"},
    ],
)
def test_trace_identity_is_xor_and_rejects_before_db_query(
    client: TestClient,
    params: dict[str, str],
) -> None:
    database = FakeDatabase()

    response = request_trace(client, database, **params)

    assert response.status_code == 422
    assert database.queries == []


def test_trace_exposes_observed_stations_without_filling_route_or_claiming_ws03(
    client: TestClient,
) -> None:
    database = FakeDatabase([accepted_fact(station_id="WS01")])

    response = request_trace(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["observed_station_ids"] == ["WS01"]
    assert payload["missing_station_status"] == "UNKNOWN"
    assert payload["route_data_sufficiency"] == "PARTIAL"
    assert payload["data_sufficiency"] == "PARTIAL"
    assert "WS03" not in payload["observed_station_ids"]


def test_trace_dto_has_only_accepted_fact_fields_and_no_forbidden_leakage(
    client: TestClient,
) -> None:
    database = FakeDatabase()

    response = request_trace(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert set(payload["data"]["items"][0]) == DTO_FIELDS
    assert not (set(json.dumps(payload).split('"')) & FORBIDDEN_SURFACES)
    sql = database.select_sql.lower()
    assert "from production_accepted_station_event_fact" in sql
    assert not any(re.search(rf"\b(from|join)\s+{source}\b", sql) for source in FORBIDDEN_SOURCES)


def test_both_endpoints_use_read_only_transaction_timeouts_and_no_ack_or_read_done(
    client: TestClient,
) -> None:
    for request_fn in (request_quality, request_trace):
        database = FakeDatabase()
        response = request_fn(client, database)
        assert response.status_code == 200
        statements = "\n".join(sql for sql, _ in database.queries).upper()
        assert "BEGIN READ ONLY" in statements
        assert "STATEMENT_TIMEOUT" in statements
        assert "IDLE_IN_TRANSACTION_SESSION_TIMEOUT" in statements
        assert not database.write_seen
        assert not database.ack_read_done_seen


@pytest.mark.parametrize(
    ("request_fn", "params"),
    [
        (request_quality, {"unexpected": "blocked"}),
        (request_trace, {"station_id": "WS01"}),
        (request_quality, {"start_time": "2026-07-03T11:00:00Z"}),
        (request_trace, {"end_time": "2026-08-04T11:00:01Z"}),
        (request_trace, {"limit": "501"}),
    ],
)
def test_unknown_params_windows_and_limit_fail_closed_before_db_query(
    client: TestClient,
    request_fn,
    params: dict[str, str],
) -> None:
    database = FakeDatabase()

    response = request_fn(client, database, **params)

    assert response.status_code == 422
    assert database.queries == []


def test_source_failure_returns_explicit_503_without_fallback(
    client: TestClient,
) -> None:
    database = FakeDatabase(fail_on_select=RuntimeError("missing relation"))
    client_without_raise = TestClient(app, raise_server_exceptions=False)

    quality_response = request_quality(client_without_raise, database)
    assert quality_response.status_code == 503
    assert quality_response.json() == {"detail": "accepted fact source unavailable"}
    trace_response = request_trace(client_without_raise, database)
    assert trace_response.status_code == 503
    assert trace_response.json() == {"detail": "accepted fact source unavailable"}
