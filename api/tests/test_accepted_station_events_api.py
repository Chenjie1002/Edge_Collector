from __future__ import annotations

import base64
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
    "reason",
    "reason_code",
    "phase",
    "candidate_context",
    "normalized_candidate_payload",
    "raw_normalized_comparison_context",
    "decoder_errors",
    "diagnostic_payload",
    "review_payload",
    "audit_payload",
    "quality_pareto_input",
    "dashboard_state",
    "payload",
    "legacy_payload",
    "raw_sample_id",
    "ack_status",
    "read_done",
    "collector_state",
    "result",
    "defect",
    "quality",
    "pareto",
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
        if "FROM PRODUCTION_ACCEPTED_STATION_EVENT_FACT" not in upper_sql:
            self.rows = []
            return

        self.database.select_sql = sql
        self.database.select_params = values
        line_id = values[0]
        start_time = values[1]
        end_time = values[2]
        limit = int(values[-1])
        cursor_tuple = values[3:6] if len(values) == 7 else None
        rows = [
            deepcopy(row)
            for row in self.database.rows
            if row["line_id"] == line_id
            and row["event_ts"] >= start_time
            and row["event_ts"] < end_time
        ]
        if cursor_tuple is not None:
            rows = [
                row
                for row in rows
                if (row["event_ts"], row["accepted_at"], row["fact_key"]) > cursor_tuple
            ]
        self.rows = sorted(
            rows,
            key=lambda row: (row["event_ts"], row["accepted_at"], row["fact_key"]),
        )[:limit]

    def fetchall(self) -> list[dict[str, object]]:
        return list(self.rows)


class FakeConnection:
    def __init__(self, database: "FakeDatabase") -> None:
        self.database = database

    def cursor(self) -> FakeCursor:
        return FakeCursor(self.database)


class FakeDatabase:
    def __init__(self, rows: list[dict[str, object]] | None = None) -> None:
        self.rows = rows or [accepted_fact()]
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


def request_events(
    client: TestClient,
    database: FakeDatabase,
    **params: object,
):
    query = {
        "line_id": "LINE_001",
        "start_time": "2026-07-03T09:00:00Z",
        "end_time": "2026-07-03T11:00:00Z",
    }
    query.update(params)
    with patch("app.db.get_conn", database.get_conn):
        return client.get("/api/v2/production/accepted-station-events", params=query)


def decode_unsigned_cursor(cursor: str) -> dict[str, object]:
    payload_part = cursor.split(".", 1)[0]
    padded = payload_part + "=" * (-len(payload_part) % 4)
    return json.loads(base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8"))


def encode_unsigned_cursor(payload: dict[str, object]) -> str:
    encoded = base64.urlsafe_b64encode(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).decode("ascii").rstrip("=")
    return f"{encoded}.unsigned"


def test_returns_only_dto_allowlist_and_excludes_forbidden_surfaces(client: TestClient) -> None:
    database = FakeDatabase()

    response = request_events(client, database)

    assert response.status_code == 200
    payload = response.json()
    item = payload["data"]["items"][0]
    assert set(item) == DTO_FIELDS
    assert not (set(json.dumps(payload).split('"')) & FORBIDDEN_SURFACES)
    assert payload["page"]["limit"] == 50


def test_query_uses_only_accepted_fact_source_and_no_legacy_fallback(client: TestClient) -> None:
    database = FakeDatabase()

    response = request_events(client, database)

    assert response.status_code == 200
    sql = database.select_sql.lower()
    assert "from production_accepted_station_event_fact" in sql
    assert not any(
        re.search(rf"\b(from|join)\s+{re.escape(source)}\b", sql)
        for source in FORBIDDEN_SOURCES
    )
    assert "event_ts asc" in sql
    assert "accepted_at asc" in sql
    assert "fact_key asc" in sql


@pytest.mark.parametrize("missing", ["line_id", "start_time", "end_time"])
def test_requires_line_id_and_bounded_time_window(
    client: TestClient,
    missing: str,
) -> None:
    database = FakeDatabase()
    params = {
        "line_id": "LINE_001",
        "start_time": "2026-07-03T09:00:00Z",
        "end_time": "2026-07-03T11:00:00Z",
    }
    params.pop(missing)
    with patch("app.db.get_conn", database.get_conn):
        response = client.get("/api/v2/production/accepted-station-events", params=params)

    assert response.status_code == 422
    assert database.queries == []


@pytest.mark.parametrize(
    ("limit", "expected_status"),
    [
        ("1", 200),
        ("500", 200),
        ("0", 422),
        ("-1", 422),
        ("abc", 422),
        ("501", 422),
        ("1.5", 422),
    ],
)
def test_limit_validation_fail_closed(
    client: TestClient,
    limit: str,
    expected_status: int,
) -> None:
    response = request_events(client, FakeDatabase(), limit=limit)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    ("start_time", "end_time"),
    [
        ("not-a-time", "2026-07-03T11:00:00Z"),
        ("2026-07-03T09:00:00Z", "not-a-time"),
        ("2026-07-03T11:00:00Z", "2026-07-03T09:00:00Z"),
        ("2026-07-03T09:00:00", "2026-07-03T11:00:00Z"),
    ],
)
def test_time_validation_fail_closed(
    client: TestClient,
    start_time: str,
    end_time: str,
) -> None:
    response = request_events(
        client,
        FakeDatabase(),
        start_time=start_time,
        end_time=end_time,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "cursor",
    [
        "not-base64",
        encode_unsigned_cursor({"v": 999}),
    ],
)
def test_malformed_or_stale_shape_cursor_fails_closed(
    client: TestClient,
    cursor: str,
) -> None:
    response = request_events(client, FakeDatabase(), cursor=cursor)

    assert response.status_code == 422


def test_tampered_cursor_fails_closed(client: TestClient) -> None:
    first = request_events(
        client,
        FakeDatabase(
            [
                accepted_fact(fact_key="sha256:fact-001"),
                accepted_fact(
                    fact_key="sha256:fact-002",
                    event_ts=datetime(2026, 7, 3, 10, 1, tzinfo=timezone.utc),
                    accepted_at=datetime(2026, 7, 3, 10, 1, 1, tzinfo=timezone.utc),
                ),
            ]
        ),
        limit="1",
    )
    assert first.status_code == 200
    cursor = first.json()["page"]["next_cursor"]
    payload = decode_unsigned_cursor(cursor)
    payload["line_id"] = "LINE_999"

    response = request_events(client, FakeDatabase(), cursor=encode_unsigned_cursor(payload))

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("mutation", "request_params"),
    [
        ({}, {"line_id": "LINE_999"}),
        ({}, {"start_time": "2026-07-03T08:00:00Z"}),
        ({}, {"end_time": "2026-07-03T12:00:00Z"}),
        ({}, {"limit": "2"}),
        ({"direction": "desc"}, {}),
    ],
)
def test_cross_scope_window_limit_or_direction_cursor_replay_fails_closed(
    client: TestClient,
    mutation: dict[str, object],
    request_params: dict[str, object],
) -> None:
    database = FakeDatabase(
        [
            accepted_fact(fact_key="sha256:fact-001"),
            accepted_fact(
                fact_key="sha256:fact-002",
                event_ts=datetime(2026, 7, 3, 10, 1, tzinfo=timezone.utc),
                accepted_at=datetime(2026, 7, 3, 10, 1, 1, tzinfo=timezone.utc),
            ),
        ]
    )
    first = request_events(client, database, limit="1")
    assert first.status_code == 200
    cursor = first.json()["page"]["next_cursor"]
    if mutation:
        payload = decode_unsigned_cursor(cursor)
        payload.update(mutation)
        cursor = encode_unsigned_cursor(payload)

    replay_params: dict[str, object] = {"cursor": cursor, "limit": "1"}
    replay_params.update(request_params)
    response = request_events(client, FakeDatabase(), **replay_params)

    assert response.status_code == 422


def test_cursor_stable_ordering_uses_event_ts_accepted_at_fact_key_tiebreaker(
    client: TestClient,
) -> None:
    rows = [
        accepted_fact(
            event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
            accepted_at=datetime(2026, 7, 3, 10, 0, 1, tzinfo=timezone.utc),
            fact_key="sha256:fact-002",
            source_event_id="PLC_001:WS01:302",
        ),
        accepted_fact(
            event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
            accepted_at=datetime(2026, 7, 3, 10, 0, 1, tzinfo=timezone.utc),
            fact_key="sha256:fact-001",
            source_event_id="PLC_001:WS01:301",
        ),
        accepted_fact(
            event_ts=datetime(2026, 7, 3, 10, 0, 2, tzinfo=timezone.utc),
            accepted_at=datetime(2026, 7, 3, 10, 0, 3, tzinfo=timezone.utc),
            fact_key="sha256:fact-003",
            source_event_id="PLC_001:WS01:303",
        ),
    ]
    database = FakeDatabase(rows)

    first = request_events(client, database, limit="2")
    assert first.status_code == 200
    assert [item["fact_key"] for item in first.json()["data"]["items"]] == [
        "sha256:fact-001",
        "sha256:fact-002",
    ]

    second = request_events(
        client,
        database,
        limit="2",
        cursor=first.json()["page"]["next_cursor"],
    )

    assert second.status_code == 200
    assert [item["fact_key"] for item in second.json()["data"]["items"]] == [
        "sha256:fact-003",
    ]
    assert second.json()["page"]["next_cursor"] is None


def test_nok_detail_fields_are_returned_only_from_accepted_fact_row(
    client: TestClient,
) -> None:
    database = FakeDatabase(
        [
            accepted_fact(
                event_type="station_nok",
                production_result=None,
                nok_code=30003,
                nok_origin="validated_nok_detail",
                nok_detail_code=30003,
                nok_detail_source_event_id="PLC_001:WS02:301:nok",
                nok_detail_evidence_fact_key="sha256:accepted-upstream-fact",
            )
        ]
    )

    response = request_events(client, database)

    assert response.status_code == 200
    item = response.json()["data"]["items"][0]
    assert item["nok_code"] == 30003
    assert item["nok_origin"] == "validated_nok_detail"
    assert item["nok_detail_code"] == 30003
    assert item["nok_detail_source_event_id"] == "PLC_001:WS02:301:nok"
    assert item["nok_detail_evidence_fact_key"] == "sha256:accepted-upstream-fact"
    assert "RAW_NORMALIZED_MISMATCH" not in json.dumps(response.json())


def test_read_only_transaction_timeout_and_no_ack_read_done_side_effect_guard(
    client: TestClient,
) -> None:
    database = FakeDatabase()

    response = request_events(client, database)

    assert response.status_code == 200
    statements = "\n".join(sql for sql, _ in database.queries).upper()
    assert "BEGIN READ ONLY" in statements
    assert "STATEMENT_TIMEOUT" in statements
    assert "IDLE_IN_TRANSACTION_SESSION_TIMEOUT" in statements
    assert not database.write_seen
    assert not database.ack_read_done_seen
