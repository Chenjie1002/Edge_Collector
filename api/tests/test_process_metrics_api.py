from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


FIXED_METRICS = (
    "accepted_event_count",
    "observed_accepted_event_rate",
    "accepted_unit_count",
    "quality_good_event_count",
    "quality_nok_event_count",
    "quality_denominator_event_count",
    "quality_rate",
    "station_cycle_time",
    "ideal_cycle_time",
    "line_accepted_event_count",
    "terminal_accepted_event_count",
    "performance",
    "availability",
    "full_oee",
)


def accepted_fact(
    *,
    fact_key: str | None,
    production_result: str,
    event_ts: datetime,
    **overrides: object,
) -> dict[str, object]:
    row: dict[str, object] = {
        "line_id": "LINE_001",
        "station_id": "WS01",
        "event_type": "station_result",
        "production_result": production_result,
        "fact_key": fact_key,
        "content_fingerprint": f"content:{fact_key}",
        "config_hash": "sha256:config",
        "config_version": "2026.07.03.1",
        "event_ts": event_ts,
        "accepted_at": event_ts,
        "nok_code": None,
        "nok_origin": None,
        "nok_detail_code": None,
        "nok_detail_source_event_id": None,
        "nok_detail_evidence_fact_key": None,
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
        self.database.statements.append((sql, values))
        upper_sql = sql.upper()
        if any(token in upper_sql for token in ("INSERT", "UPDATE", "DELETE")):
            self.database.write_seen = True
        if "ACK" in upper_sql or "READ_DONE" in upper_sql:
            self.database.ack_read_done_seen = True
        if "SELECT" not in upper_sql:
            return
        self.database.select_sql = sql
        self.database.select_params = values
        self.database.select_count += 1
        if self.database.fail_on_select is not None:
            raise self.database.fail_on_select
        line_id, station_id, start, end = values
        self.rows = [
            row
            for row in self.database.rows
            if row["line_id"] == line_id
            and row["station_id"] == station_id
            and row["event_type"] == "station_result"
            and row["event_ts"] >= start
            and row["event_ts"] < end
        ]

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
        fail_on_select: Exception | None = None,
    ) -> None:
        self.rows = rows
        self.fail_on_select = fail_on_select
        self.statements: list[tuple[str, tuple]] = []
        self.select_sql = ""
        self.select_params: tuple = ()
        self.select_count = 0
        self.write_seen = False
        self.ack_read_done_seen = False

    @contextmanager
    def get_conn(self):
        yield FakeConnection(self)


def request_process_metrics(
    client: TestClient,
    database: FakeDatabase,
    **overrides: object,
):
    query: dict[str, object] = {
        "line_id": "LINE_001",
        "station_id": "WS01",
        "from": "2026-07-03T09:00:00Z",
        "to": "2026-07-03T11:00:00Z",
    }
    query.update(overrides)
    with patch("app.db.get_conn", database.get_conn):
        return client.get("/api/v2/process-metrics", params=query)


def raw_process_request(
    client: TestClient,
    database: FakeDatabase,
    query: list[tuple[str, object]] | dict[str, object],
    *,
    method: str = "GET",
    content: bytes | None = None,
):
    with patch("app.db.get_conn", database.get_conn):
        return client.request(
            method,
            "/api/v2/process-metrics",
            params=query,
            content=content,
        )


def metric_map(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    return {metric["name"]: metric for metric in payload["metrics"]}


def test_process_metrics_returns_accepted_event_count_and_calendar_rate() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key="fact-ok",
                production_result="ok",
                event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
            ),
            accepted_fact(
                fact_key="fact-skip",
                production_result="skip",
                event_ts=datetime(2026, 7, 3, 10, 30, tzinfo=timezone.utc),
            ),
        ]
    )

    with patch("app.db.get_conn", database.get_conn):
        response = client.get(
            "/api/v2/process-metrics",
            params={
                "line_id": "LINE_001",
                "station_id": "WS01",
                "from": "2026-07-03T09:00:00+00:00",
                "to": "2026-07-03T11:00:00Z",
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["window"] == {
        "from": "2026-07-03T09:00:00Z",
        "to": "2026-07-03T11:00:00Z",
        "interval": "[from,to)",
        "duration_seconds": 7200.0,
    }
    metrics = {metric["name"]: metric for metric in payload["metrics"]}
    assert metrics["accepted_event_count"]["value"] == 2
    assert metrics["observed_accepted_event_rate"]["value"] == 2 / 7200


def test_process_metrics_exposes_fixed_matrix_and_reuses_quality_semantics() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key="fact-ok",
                production_result="ok",
                event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
            ),
            accepted_fact(
                fact_key="fact-nok",
                production_result="nok",
                event_ts=datetime(2026, 7, 3, 10, 1, tzinfo=timezone.utc),
            ),
            accepted_fact(
                fact_key="fact-skip",
                production_result="skip",
                event_ts=datetime(2026, 7, 3, 10, 2, tzinfo=timezone.utc),
            ),
            accepted_fact(
                fact_key="fact-na",
                production_result="not_applicable",
                event_ts=datetime(2026, 7, 3, 10, 3, tzinfo=timezone.utc),
            ),
        ]
    )

    response = request_process_metrics(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["contract_version"] == "P1-G3-PROCESS-KPI-1.0"
    assert payload["scope"] == {
        "line_id": "LINE_001",
        "station_id": "WS01",
        "aggregation": "station",
    }
    assert payload["status"] == "PARTIAL"
    metrics = metric_map(payload)
    assert tuple(metrics) == FIXED_METRICS
    assert metrics["accepted_event_count"]["value"] == 4
    assert metrics["observed_accepted_event_rate"]["value"] == 4 / 7200
    assert metrics["quality_good_event_count"]["value"] == 1
    assert metrics["quality_nok_event_count"]["value"] == 1
    assert metrics["quality_denominator_event_count"]["value"] == 2
    assert metrics["quality_rate"]["status"] == "PARTIAL"
    assert metrics["quality_rate"]["value"] == 0.5
    assert metrics["quality_rate"]["reason"]["code"] == "QUALITY_NOK_DETAIL_INCOMPLETE"
    for name in (
        "accepted_unit_count",
        "station_cycle_time",
        "ideal_cycle_time",
        "line_accepted_event_count",
        "terminal_accepted_event_count",
        "performance",
        "availability",
        "full_oee",
    ):
        assert metrics[name]["numeric_value_allowed"] is False
        assert "value" not in metrics[name]
    assert payload["source"]["authority"] == "production_accepted_station_event_fact"
    assert payload["source"]["fallback"] == "none"
    assert all(metric["source"]["fallback"] == "none" for metric in metrics.values())


def test_nok_code_without_bound_detail_evidence_remains_partial() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key="fact-nok-incomplete",
                production_result="nok",
                event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
                nok_code="NOK-001",
            )
        ]
    )

    response = request_process_metrics(client, database)

    assert response.status_code == 200
    quality_rate = metric_map(response.json())["quality_rate"]
    assert quality_rate["status"] == "PARTIAL"
    assert quality_rate["reason"]["code"] == "QUALITY_NOK_DETAIL_INCOMPLETE"
    assert quality_rate["numeric_value_allowed"] is True
    assert quality_rate["value"] == 0.0


def test_fully_bound_accepted_nok_detail_remains_supported() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key="fact-nok-complete",
                production_result="nok",
                event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
                nok_code="NOK-001",
                nok_origin="plc",
                nok_detail_code="DETAIL-001",
                nok_detail_source_event_id="source-event-001",
                nok_detail_evidence_fact_key="fact-nok-complete",
            )
        ]
    )

    response = request_process_metrics(client, database)

    assert response.status_code == 200
    quality_rate = metric_map(response.json())["quality_rate"]
    assert quality_rate["status"] == "SUPPORTED"
    assert quality_rate["reason"]["code"] == "QUALITY_PREDECESSOR_SEMANTICS"
    assert quality_rate["numeric_value_allowed"] is True
    assert quality_rate["value"] == 0.0


def test_valid_empty_window_is_200_and_separate_from_source_failure() -> None:
    client = TestClient(app)
    database = FakeDatabase([])

    response = request_process_metrics(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "PARTIAL"
    assert payload["reason"]["code"] == "EMPTY_ACCEPTED_WINDOW"
    metrics = metric_map(payload)
    for name in (
        "accepted_event_count",
        "observed_accepted_event_rate",
        "quality_good_event_count",
        "quality_nok_event_count",
        "quality_denominator_event_count",
    ):
        assert metrics[name]["value"] == 0
    assert metrics["quality_rate"]["status"] == "UNAVAILABLE"
    assert metrics["quality_rate"]["reason"]["code"] == "QUALITY_DENOMINATOR_EMPTY"
    assert "value" not in metrics["quality_rate"]
    assert all(
        "value" not in metrics[name]
        for name in FIXED_METRICS
        if name
        not in {
            "accepted_event_count",
            "observed_accepted_event_rate",
            "quality_good_event_count",
            "quality_nok_event_count",
            "quality_denominator_event_count",
        }
    )


def test_accepted_fact_source_failure_is_503_without_empty_or_zero_fallback() -> None:
    client = TestClient(app)
    database = FakeDatabase([], fail_on_select=RuntimeError("missing relation"))

    response = request_process_metrics(client, database)

    assert response.status_code == 503
    assert response.json() == {
        "contract_version": "P1-G3-PROCESS-KPI-1.0",
        "scope": {
            "line_id": "LINE_001",
            "station_id": "WS01",
            "aggregation": "station",
        },
        "window": {
            "from": "2026-07-03T09:00:00Z",
            "to": "2026-07-03T11:00:00Z",
            "interval": "[from,to)",
            "duration_seconds": 7200.0,
        },
        "status": "UNAVAILABLE",
        "reason": {
            "code": "ACCEPTED_FACT_SOURCE_UNAVAILABLE",
            "detail": "accepted fact source unavailable",
        },
        "source": {
            "authority": "production_accepted_station_event_fact",
            "identity": "fact_key",
            "config_window_state": "UNRESOLVED",
            "fallback": "none",
        },
        "metrics": [],
    }


def test_process_metrics_sql_is_read_only_and_uses_half_open_accepted_fact_source() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key="fact-ok",
                production_result="ok",
                event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
            )
        ]
    )

    response = request_process_metrics(client, database)

    assert response.status_code == 200
    statements = "\n".join(sql for sql, _ in database.statements).upper()
    assert "BEGIN READ ONLY" in statements
    assert "STATEMENT_TIMEOUT" in statements
    assert "IDLE_IN_TRANSACTION_SESSION_TIMEOUT" in statements
    assert "FROM PRODUCTION_ACCEPTED_STATION_EVENT_FACT" in database.select_sql.upper()
    assert "EVENT_TS >=" in database.select_sql.upper()
    assert "EVENT_TS <" in database.select_sql.upper()
    assert not database.write_seen
    assert not database.ack_read_done_seen


def test_duplicate_fact_key_fails_closed_without_distinct_or_numeric_claim() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key="duplicate-fact",
                production_result="ok",
                event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
            ),
            accepted_fact(
                fact_key="duplicate-fact",
                production_result="nok",
                event_ts=datetime(2026, 7, 3, 10, 1, tzinfo=timezone.utc),
                content_fingerprint="content:conflicting-row",
            ),
        ]
    )

    response = request_process_metrics(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "UNAVAILABLE"
    assert payload["reason"]["code"] == "FACT_IDENTITY_DUPLICATE_OR_CONFLICT"
    metrics = metric_map(payload)
    for name in (
        "accepted_event_count",
        "observed_accepted_event_rate",
        "quality_good_event_count",
        "quality_nok_event_count",
        "quality_denominator_event_count",
        "quality_rate",
    ):
        assert metrics[name]["status"] == "UNAVAILABLE"
        assert metrics[name]["numeric_value_allowed"] is False
        assert "value" not in metrics[name]
    assert "DISTINCT" not in database.select_sql.upper()
    assert database.select_count == 1


def test_missing_fact_key_fails_closed_without_synthetic_identity() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key=None,
                production_result="ok",
                event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
            )
        ]
    )

    response = request_process_metrics(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "UNAVAILABLE"
    assert payload["reason"]["code"] == "FACT_IDENTITY_MISSING"
    assert "value" not in metric_map(payload)["accepted_event_count"]


def test_unknown_production_result_fails_closed_instead_of_being_filtered() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key="unknown-result",
                production_result="rework",
                event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
            )
        ]
    )

    response = request_process_metrics(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "UNAVAILABLE"
    metrics = metric_map(payload)
    assert metrics["accepted_event_count"]["numeric_value_allowed"] is False
    assert metrics["quality_denominator_event_count"]["numeric_value_allowed"] is False


def test_mixed_config_keeps_config_independent_metrics_and_blocks_config_claims() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key="config-a",
                production_result="ok",
                event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
                config_hash="sha256:config-a",
                config_version="2026.07.03.1",
            ),
            accepted_fact(
                fact_key="config-b",
                production_result="ok",
                event_ts=datetime(2026, 7, 3, 10, 1, tzinfo=timezone.utc),
                config_hash="sha256:config-b",
                config_version="2026.07.04.1",
            ),
        ]
    )

    response = request_process_metrics(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["source"]["config_window_state"] == "MIXED"
    metrics = metric_map(payload)
    assert metrics["accepted_event_count"]["value"] == 2
    assert metrics["observed_accepted_event_rate"]["value"] == 2 / 7200
    assert metrics["ideal_cycle_time"]["reason"]["code"] == "MIXED_HISTORICAL_CONFIG_WINDOW"
    for name in (
        "ideal_cycle_time",
        "line_accepted_event_count",
        "terminal_accepted_event_count",
        "performance",
        "availability",
        "full_oee",
    ):
        assert metrics[name]["numeric_value_allowed"] is False
        assert "value" not in metrics[name]


def test_single_config_tuple_without_historical_authority_remains_unresolved() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key="single-config",
                production_result="ok",
                event_ts=datetime(2026, 7, 3, 10, 0, tzinfo=timezone.utc),
                config_hash="sha256:config",
                config_version="2026.07.03.1",
            )
        ]
    )

    response = request_process_metrics(client, database)

    assert response.status_code == 200
    payload = response.json()
    assert payload["source"]["config_window_state"] == "UNRESOLVED"
    ideal_cycle_time = metric_map(payload)["ideal_cycle_time"]
    assert ideal_cycle_time["numeric_value_allowed"] is False
    assert "value" not in ideal_cycle_time
    assert ideal_cycle_time["reason"]["code"] == "HISTORICAL_CONFIG_AUTHORITY_MISSING"


VALID_QUERY = [
    ("line_id", "LINE_001"),
    ("station_id", "WS01"),
    ("from", "2026-07-03T09:00:00Z"),
    ("to", "2026-07-03T11:00:00Z"),
]


@pytest.mark.parametrize(
    "query",
    [
        [
            ("line_id", "LINE_001"),
            ("station_id", "WS01"),
            ("to", "2026-07-03T11:00:00Z"),
        ],
        [
            ("line_id", "  "),
            ("station_id", "WS01"),
            ("from", "2026-07-03T09:00:00Z"),
            ("to", "2026-07-03T11:00:00Z"),
        ],
        [
            ("line_id", "LINE_001"),
            ("station_id", "WS01"),
            ("from", "2026-07-03T09:00:00"),
            ("to", "2026-07-03T11:00:00Z"),
        ],
        [
            ("line_id", "LINE_001"),
            ("station_id", "WS01"),
            ("from", "not-a-timestamp"),
            ("to", "2026-07-03T11:00:00Z"),
        ],
        [
            ("line_id", "LINE_001"),
            ("station_id", "WS01"),
            ("from", "2026-07-03T09:00:00+0000"),
            ("to", "2026-07-03T11:00:00Z"),
        ],
        [
            ("line_id", "LINE_001"),
            ("station_id", "WS01"),
            ("from", ""),
            ("to", "2026-07-03T11:00:00Z"),
        ],
        [
            ("line_id", "LINE_001"),
            ("station_id", "WS01"),
            ("from", "2026-07-03T09:00:00Z"),
            ("to", ""),
        ],
        [
            ("line_id", "LINE_001"),
            ("station_id", "WS01"),
            ("from", "2026-07-03T11:00:00Z"),
            ("to", "2026-07-03T09:00:00Z"),
        ],
        [
            ("line_id", "LINE_001"),
            ("station_id", "WS01"),
            ("from", "2026-07-03T09:00:00Z"),
            ("to", "2026-08-03T09:00:01Z"),
        ],
        VALID_QUERY + [("terminal_id", "WS03")],
        [
            ("line_id", "LINE_001"),
            ("line_id", "LINE_001"),
            ("station_id", "WS01"),
            ("from", "2026-07-03T09:00:00Z"),
            ("to", "2026-07-03T11:00:00Z"),
        ],
        VALID_QUERY + [("scope", "line")],
        VALID_QUERY + [("group_by", "line")],
        VALID_QUERY + [("aggregate", "line")],
        VALID_QUERY + [("metric", "performance")],
        VALID_QUERY + [("limit", "0")],
    ],
)
def test_invalid_query_returns_exact_422_without_db_select(
    query: list[tuple[str, object]],
) -> None:
    client = TestClient(app, raise_server_exceptions=False)
    database = FakeDatabase([])

    response = raw_process_request(client, database, query)

    assert response.status_code == 422
    payload = response.json()
    assert payload["contract_version"] == "P1-G3-PROCESS-KPI-1.0"
    assert payload["error"]["code"] == "INVALID_REQUEST"
    assert "numeric_value" not in payload
    assert database.select_count == 0


def test_half_open_window_and_utc_canonicalization_exclude_to_boundary() -> None:
    client = TestClient(app)
    database = FakeDatabase(
        [
            accepted_fact(
                fact_key="at-from",
                production_result="ok",
                event_ts=datetime(2026, 7, 3, 9, 0, tzinfo=timezone.utc),
            ),
            accepted_fact(
                fact_key="at-to",
                production_result="ok",
                event_ts=datetime(2026, 7, 3, 11, 0, tzinfo=timezone.utc),
            ),
        ]
    )

    response = raw_process_request(
        client,
        database,
        [
            ("line_id", "LINE_001"),
            ("station_id", "WS01"),
            ("from", "2026-07-03T17:00:00+08:00"),
            ("to", "2026-07-03T19:00:00+08:00"),
        ],
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["window"] == {
        "from": "2026-07-03T09:00:00Z",
        "to": "2026-07-03T11:00:00Z",
        "interval": "[from,to)",
        "duration_seconds": 7200.0,
    }
    assert metric_map(payload)["accepted_event_count"]["value"] == 1
    assert database.select_params[2:] == (
        datetime(2026, 7, 3, 9, 0, tzinfo=timezone.utc),
        datetime(2026, 7, 3, 11, 0, tzinfo=timezone.utc),
    )


def test_non_empty_request_body_returns_422_without_db_select() -> None:
    client = TestClient(app, raise_server_exceptions=False)
    database = FakeDatabase([])

    response = raw_process_request(
        client,
        database,
        VALID_QUERY,
        content=b"{}",
    )

    assert response.status_code == 422
    assert response.json()["error"] == {
        "code": "INVALID_REQUEST",
        "detail": "request body is not allowed",
    }
    assert database.select_count == 0


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE"])
def test_non_get_methods_are_405_and_do_not_select(method: str) -> None:
    client = TestClient(app, raise_server_exceptions=False)
    database = FakeDatabase([])

    response = raw_process_request(client, database, VALID_QUERY, method=method)

    assert response.status_code == 405
    assert database.select_count == 0
