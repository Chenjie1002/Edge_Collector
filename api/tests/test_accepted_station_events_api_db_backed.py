from __future__ import annotations

import base64
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pytest
from fastapi.testclient import TestClient

from app.main import app


DB_BACKED_ENABLE_ENV = "EDGE_MES_ENABLE_DB_BACKED_TESTS"
DB_BACKED_TARGET_DSN_ENV = "EDGE_MES_DB_BACKED_TEST_DSN"
DB_BACKED_MAINTENANCE_DSN_ENV = "EDGE_MES_DB_BACKED_MAINTENANCE_DSN"
LOCAL_TEST_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
PROTECTED_DATABASE_NAMES = frozenset({"edge_mes", "postgres", "prod", "production"})
TEST_DATABASE_RE = re.compile(r"^edge_mes_test_[A-Za-z0-9_]+$")

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

ACCEPTED_FACT_TABLE = "production_accepted_station_event_fact"
MUTATION_SQL_RE = re.compile(r"\b(INSERT|UPDATE|DELETE)\b", re.IGNORECASE)
ACK_READ_DONE_SQL_RE = re.compile(r"\b(ACK_STATUS|READ_DONE)\b", re.IGNORECASE)
RUNTIME_TABLE_SQL_RE = re.compile(
    r"\b(COLLECTOR_RUNTIME_STATUS|RAW_PLC_SAMPLE|PLC_RUNTIME_STATE|RUNTIME_STATE)\b",
    re.IGNORECASE,
)
EXPECTED_UNIQUE_CONSTRAINTS = frozenset(
    {
        "uq_production_accepted_station_event_fact_key",
        "uq_production_accepted_station_event_source",
    }
)
EXPECTED_CHECK_CONSTRAINTS = frozenset(
    {
        "ck_production_accepted_station_event_type",
        "ck_production_accepted_station_event_result",
        "ck_production_accepted_station_result_authority",
        "ck_production_accepted_station_result_nok_authority",
        "ck_production_accepted_station_nok_detail_authority",
    }
)
EXPECTED_ACCEPTED_FACT_COLUMNS = {
    "line_id": False,
    "plc_id": False,
    "station_id": False,
    "station_type": False,
    "profile_id": False,
    "config_hash": False,
    "config_version": False,
    "event_type": False,
    "production_result": True,
    "unit_id": True,
    "dmc": True,
    "cycle_counter": False,
    "source_event_id": False,
    "event_ts": False,
    "accepted_at": False,
    "fact_key": False,
    "content_fingerprint": False,
    "nok_code": True,
    "nok_origin": True,
    "nok_detail_code": True,
    "nok_detail_source_event_id": True,
    "nok_detail_evidence_fact_key": True,
}

FORBIDDEN_SOURCE_TABLES = {
    "raw_plc_sample",
    "cycle_event",
    "station_event",
    "production_unit",
    "quality_event",
    "production_snapshot",
    "production_events",
}

FORBIDDEN_SURFACE_TOKENS = {
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
    "legacy_payload",
    "raw_sample_id",
    "ack_status",
    "read_done",
    "collector_state",
    "result",
    "defect",
    "quality",
    "pareto",
    "RAW_NORMALIZED_MISMATCH",
}

pytestmark = [
    pytest.mark.db_backed,
    pytest.mark.postgres_local,
]


class DsnSafetyError(ValueError):
    pass


@dataclass(frozen=True)
class SafeDsn:
    raw: str
    host: str
    database: str


@dataclass(frozen=True)
class TempDbPlan:
    target: SafeDsn
    maintenance: SafeDsn
    database_name: str
    migration_files: tuple[Path, ...]


class QueryRecorder:
    def __init__(self, *, fail_select: bool = False) -> None:
        self.fail_select = fail_select
        self.statements: list[tuple[str, tuple[Any, ...]]] = []
        self.select_sql = ""
        self.write_seen = False
        self.ack_read_done_seen = False
        self.runtime_side_effect_seen = False

    def record(self, sql: str, params: tuple[Any, ...]) -> None:
        self.statements.append((sql, params))
        mutation_seen = MUTATION_SQL_RE.search(sql) is not None
        if mutation_seen:
            self.write_seen = True
        if mutation_seen and ACK_READ_DONE_SQL_RE.search(sql):
            self.ack_read_done_seen = True
        if mutation_seen or RUNTIME_TABLE_SQL_RE.search(sql):
            self.runtime_side_effect_seen = True
        if "FROM PRODUCTION_ACCEPTED_STATION_EVENT_FACT" in sql.upper():
            self.select_sql = sql

    @property
    def joined_sql(self) -> str:
        return "\n".join(sql for sql, _ in self.statements)


class RecordingCursor:
    def __init__(self, cursor: Any, recorder: QueryRecorder) -> None:
        self._cursor = cursor
        self._recorder = recorder

    def __enter__(self) -> "RecordingCursor":
        self._cursor.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb) -> Any:
        return self._cursor.__exit__(exc_type, exc, tb)

    def execute(self, sql: str, params: tuple[Any, ...] | list[Any] | None = None) -> Any:
        values = tuple(params or ())
        self._recorder.record(sql, values)
        if self._recorder.fail_select and "FROM production_accepted_station_event_fact" in sql:
            raise RuntimeError("controlled query failure")
        return self._cursor.execute(sql, values if params is not None else None)

    def fetchall(self) -> Any:
        return self._cursor.fetchall()

    def fetchone(self) -> Any:
        return self._cursor.fetchone()


class RecordingConnection:
    def __init__(self, conn: Any, recorder: QueryRecorder) -> None:
        self._conn = conn
        self._recorder = recorder

    def __enter__(self) -> "RecordingConnection":
        self._conn.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb) -> Any:
        return self._conn.__exit__(exc_type, exc, tb)

    def cursor(self, *args: Any, **kwargs: Any) -> RecordingCursor:
        return RecordingCursor(self._conn.cursor(*args, **kwargs), self._recorder)

    def execute(
        self,
        sql: str,
        params: tuple[Any, ...] | list[Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        values = tuple(params or ())
        self._recorder.record(sql, values)
        return self._conn.execute(sql, values if params is not None else None, *args, **kwargs)

    def close(self) -> Any:
        return self._conn.close()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._conn, name)


def db_backed_tests_enabled(env: dict[str, str] | None = None) -> bool:
    env = os.environ if env is None else env
    return env.get(DB_BACKED_ENABLE_ENV) == "1"


def _parse_postgres_dsn(dsn: str) -> SafeDsn:
    parsed = urlparse(dsn)
    if parsed.scheme not in {"postgresql", "postgres"}:
        raise DsnSafetyError(f"DSN scheme must be postgresql/postgres: {parsed.scheme}")
    if not parsed.hostname:
        raise DsnSafetyError("DSN host is required")
    database = parsed.path.lstrip("/")
    if not database:
        raise DsnSafetyError("DSN database name is required")
    return SafeDsn(raw=dsn, host=parsed.hostname, database=database)


def validate_test_target_dsn(dsn: str) -> SafeDsn:
    parts = _parse_postgres_dsn(dsn)
    if parts.host not in LOCAL_TEST_HOSTS:
        raise DsnSafetyError(f"test target DSN host is not local/test-only: {parts.host}")
    if parts.database in PROTECTED_DATABASE_NAMES or not TEST_DATABASE_RE.fullmatch(parts.database):
        raise DsnSafetyError(f"test target DSN database must match edge_mes_test_*: {parts.database}")
    return parts


def validate_maintenance_dsn(dsn: str) -> SafeDsn:
    parts = _parse_postgres_dsn(dsn)
    if parts.host not in LOCAL_TEST_HOSTS:
        raise DsnSafetyError(f"maintenance DSN host is not local/test-only: {parts.host}")
    if parts.database not in {"postgres", "template1"}:
        raise DsnSafetyError("maintenance DSN must point to postgres or template1 only")
    return parts


def migration_files_for_api_read(repo_root: Path | None = None) -> tuple[Path, ...]:
    root = repo_root or Path(__file__).resolve().parents[2]
    return (root / "db" / "migrations" / "007_accepted_station_event_visibility.sql",)


def build_temp_db_plan(target_dsn: str, maintenance_dsn: str) -> TempDbPlan:
    target = validate_test_target_dsn(target_dsn)
    maintenance = validate_maintenance_dsn(maintenance_dsn)
    if target.database == maintenance.database:
        raise DsnSafetyError("test-target DSN and maintenance DSN must be distinct")
    if not TEST_DATABASE_RE.fullmatch(target.database):
        raise DsnSafetyError(f"refusing unsafe temp DB name: {target.database}")
    return TempDbPlan(
        target=target,
        maintenance=maintenance,
        database_name=target.database,
        migration_files=migration_files_for_api_read(),
    )


def _quoted_database_name(database_name: str) -> str:
    if not TEST_DATABASE_RE.fullmatch(database_name):
        raise DsnSafetyError(f"refusing unsafe temp DB name: {database_name}")
    return '"' + database_name.replace('"', '""') + '"'


def create_temp_database_statement(database_name: str) -> str:
    return f"CREATE DATABASE {_quoted_database_name(database_name)}"


def drop_temp_database_statement(database_name: str) -> str:
    return f"DROP DATABASE IF EXISTS {_quoted_database_name(database_name)} WITH (FORCE)"


def plan_from_env(env: dict[str, str] | None = None) -> TempDbPlan:
    env = os.environ if env is None else env
    if not db_backed_tests_enabled(env):
        pytest.skip(f"DB-backed API read validation requires {DB_BACKED_ENABLE_ENV}=1")
    target_dsn = env.get(DB_BACKED_TARGET_DSN_ENV)
    maintenance_dsn = env.get(DB_BACKED_MAINTENANCE_DSN_ENV)
    if not target_dsn or not maintenance_dsn:
        pytest.skip(
            f"DB-backed API read validation requires {DB_BACKED_TARGET_DSN_ENV} "
            f"and {DB_BACKED_MAINTENANCE_DSN_ENV}"
        )
    return build_temp_db_plan(target_dsn, maintenance_dsn)


def _sql_string_literals(values: set[str] | frozenset[str]) -> str:
    return ", ".join(f"'{value}'" for value in sorted(values))


def accepted_fact_schema_verification_queries() -> tuple[str, ...]:
    expected_column_names = _sql_string_literals(set(EXPECTED_ACCEPTED_FACT_COLUMNS))
    expected_constraint_names = _sql_string_literals(EXPECTED_UNIQUE_CONSTRAINTS | EXPECTED_CHECK_CONSTRAINTS)
    return (
        f"SELECT to_regclass('public.{ACCEPTED_FACT_TABLE}')",
        f"""
        SELECT column_name, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = '{ACCEPTED_FACT_TABLE}'
          AND column_name IN ({expected_column_names})
        """,
        f"""
        SELECT conname, contype
        FROM pg_constraint
        WHERE conrelid = 'public.{ACCEPTED_FACT_TABLE}'::regclass
          AND conname IN ({expected_constraint_names})
        """,
    )


def _schema_verification_failure(message: str) -> AssertionError:
    return AssertionError(
        f"schema/constraint verification failure for {ACCEPTED_FACT_TABLE}: {message}"
    )


def verify_accepted_fact_schema(conn: Any) -> None:
    table_query, columns_query, constraints_query = accepted_fact_schema_verification_queries()
    with conn.cursor() as cur:
        cur.execute(table_query)
        table_row = cur.fetchone()
        if table_row is None or table_row[0] is None:
            raise _schema_verification_failure("expected table is missing")

        cur.execute(columns_query)
        observed_columns = {
            str(column_name): str(is_nullable).upper() == "YES"
            for column_name, is_nullable in cur.fetchall()
        }
        missing_columns = sorted(set(EXPECTED_ACCEPTED_FACT_COLUMNS) - set(observed_columns))
        if missing_columns:
            raise _schema_verification_failure(
                f"expected columns are missing: {', '.join(missing_columns)}"
            )
        nullability_mismatches = sorted(
            column_name
            for column_name, expected_nullable in EXPECTED_ACCEPTED_FACT_COLUMNS.items()
            if observed_columns[column_name] != expected_nullable
        )
        if nullability_mismatches:
            raise _schema_verification_failure(
                "column nullability mismatch: " + ", ".join(nullability_mismatches)
            )

        cur.execute(constraints_query)
        observed_unique_constraints = set()
        observed_check_constraints = set()
        for constraint_name, constraint_type in cur.fetchall():
            if constraint_type == "u":
                observed_unique_constraints.add(str(constraint_name))
            elif constraint_type == "c":
                observed_check_constraints.add(str(constraint_name))

        missing_unique_constraints = sorted(EXPECTED_UNIQUE_CONSTRAINTS - observed_unique_constraints)
        if missing_unique_constraints:
            raise _schema_verification_failure(
                "expected unique constraints are missing: "
                + ", ".join(missing_unique_constraints)
            )
        missing_check_constraints = sorted(EXPECTED_CHECK_CONSTRAINTS - observed_check_constraints)
        if missing_check_constraints:
            raise _schema_verification_failure(
                "expected check constraints are missing: "
                + ", ".join(missing_check_constraints)
            )


def accepted_fact_row(**overrides: Any) -> dict[str, Any]:
    row = {
        "line_id": "LINE_001",
        "plc_id": "PLC_001",
        "station_id": "WS01",
        "station_type": "ASSEMBLY",
        "profile_id": "normal",
        "config_hash": "sha256:config-api-read",
        "config_version": "2026.07.04.1",
        "event_type": "station_result",
        "production_result": "ok",
        "unit_id": "U-API-001",
        "dmc": "DMC-API-001",
        "cycle_counter": 301,
        "source_event_id": "PLC_001:WS01:301:station_result",
        "event_ts": datetime(2026, 7, 4, 10, 0, tzinfo=timezone.utc),
        "accepted_at": datetime(2026, 7, 4, 10, 0, 1, tzinfo=timezone.utc),
        "fact_key": "sha256:api-read-fact-001",
        "content_fingerprint": "sha256:api-read-content-001",
        "nok_code": None,
        "nok_origin": None,
        "nok_detail_code": None,
        "nok_detail_source_event_id": None,
        "nok_detail_evidence_fact_key": None,
    }
    row.update(overrides)
    return row


def insert_accepted_fact(conn: Any, row: dict[str, Any]) -> None:
    fields = tuple(row)
    placeholders = ", ".join(["%s"] * len(fields))
    columns = ", ".join(fields)
    values = tuple(row[field] for field in fields)
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO production_accepted_station_event_fact ({columns}) VALUES ({placeholders})",
            values,
        )


def decode_cursor(cursor: str) -> dict[str, Any]:
    encoded_payload = cursor.split(".", 1)[0]
    padded = encoded_payload + "=" * (-len(encoded_payload) % 4)
    return json.loads(base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8"))


def encode_unsigned_cursor(payload: dict[str, Any]) -> str:
    encoded = base64.urlsafe_b64encode(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).decode("ascii").rstrip("=")
    return f"{encoded}.unsigned"


def assert_no_forbidden_surfaces(payload: dict[str, Any]) -> None:
    serialized = json.dumps(payload, sort_keys=True)
    assert not (set(serialized.split('"')) & FORBIDDEN_SURFACE_TOKENS)
    assert "adapter" not in serialized.lower()
    assert "candidate" not in serialized.lower()
    assert "diagnostic" not in serialized.lower()
    assert "review" not in serialized.lower()
    assert "audit" not in serialized.lower()
    assert "legacy" not in serialized.lower()


def assert_select_source_is_isolated(sql: str) -> None:
    normalized = sql.lower()
    assert re.search(r"\bfrom\s+production_accepted_station_event_fact\b", normalized)
    assert not any(
        re.search(rf"\b(from|join)\s+{re.escape(source)}\b", normalized)
        for source in FORBIDDEN_SOURCE_TABLES
    )


def test_query_recorder_ignores_read_only_plc_fields_and_rollback() -> None:
    recorder = QueryRecorder()

    recorder.record(
        """
        SELECT line_id, plc_id, source_event_id
        FROM production_accepted_station_event_fact
        WHERE line_id = %s
        """,
        ("LINE_001",),
    )
    recorder.record("ROLLBACK", ())

    assert recorder.select_sql
    assert not recorder.write_seen
    assert not recorder.ack_read_done_seen
    assert not recorder.runtime_side_effect_seen


def test_recording_connection_proxies_context_manager() -> None:
    class ContextConnection:
        def __init__(self) -> None:
            self.entered = False
            self.exited = False
            self.executed: list[tuple[str, tuple[Any, ...] | None]] = []

        def __enter__(self) -> "ContextConnection":
            self.entered = True
            return self

        def __exit__(self, exc_type, exc, tb) -> None:
            self.exited = True
            return None

        def cursor(self) -> Any:
            raise AssertionError("cursor is not used by this proxy test")

        def close(self) -> None:
            return None

        def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> str:
            self.executed.append((sql, params))
            return "cursor-result"

    wrapped = ContextConnection()
    recorder = QueryRecorder()

    with RecordingConnection(wrapped, recorder) as conn:
        assert conn is not wrapped
        assert wrapped.entered
        assert conn.execute("DROP DATABASE IF EXISTS edge_mes_test_api_read") == "cursor-result"

    assert wrapped.exited
    assert wrapped.executed == [("DROP DATABASE IF EXISTS edge_mes_test_api_read", None)]
    assert recorder.statements == [("DROP DATABASE IF EXISTS edge_mes_test_api_read", ())]


@pytest.fixture
def db_backed_temp_db_plan() -> TempDbPlan:
    return plan_from_env()


@pytest.fixture
def db_backed_api_database(db_backed_temp_db_plan: TempDbPlan, monkeypatch: pytest.MonkeyPatch):
    import psycopg

    plan = db_backed_temp_db_plan
    with psycopg.connect(plan.maintenance.raw, autocommit=True) as admin_conn:
        admin_conn.execute(drop_temp_database_statement(plan.database_name))
        admin_conn.execute(create_temp_database_statement(plan.database_name))
    try:
        with psycopg.connect(plan.target.raw, autocommit=True) as conn:
            for migration_file in plan.migration_files:
                conn.execute(migration_file.read_text(encoding="utf-8"))
            verify_accepted_fact_schema(conn)
        monkeypatch.setenv("DATABASE_URL", plan.target.raw)
        yield plan
    finally:
        with psycopg.connect(plan.maintenance.raw, autocommit=True) as admin_conn:
            admin_conn.execute(drop_temp_database_statement(plan.database_name))


@pytest.fixture
def recorder(monkeypatch: pytest.MonkeyPatch) -> QueryRecorder:
    from app import db as api_db

    query_recorder = QueryRecorder()
    original_connect = api_db.psycopg.connect

    def connect_recording(*args: Any, **kwargs: Any) -> RecordingConnection:
        return RecordingConnection(original_connect(*args, **kwargs), query_recorder)

    monkeypatch.setattr(api_db.psycopg, "connect", connect_recording)
    return query_recorder


@pytest.fixture
def failing_recorder(monkeypatch: pytest.MonkeyPatch) -> QueryRecorder:
    from app import db as api_db

    query_recorder = QueryRecorder(fail_select=True)
    original_connect = api_db.psycopg.connect

    def connect_recording(*args: Any, **kwargs: Any) -> RecordingConnection:
        return RecordingConnection(original_connect(*args, **kwargs), query_recorder)

    monkeypatch.setattr(api_db.psycopg, "connect", connect_recording)
    return query_recorder


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def error_client() -> TestClient:
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def seeded_rows(db_backed_api_database: TempDbPlan) -> list[dict[str, Any]]:
    import psycopg

    rows = [
        accepted_fact_row(
            fact_key="sha256:api-read-fact-002",
            content_fingerprint="sha256:api-read-content-002",
            source_event_id="PLC_001:WS01:302:station_result",
            cycle_counter=302,
            event_ts=datetime(2026, 7, 4, 10, 0, tzinfo=timezone.utc),
            accepted_at=datetime(2026, 7, 4, 10, 0, 1, tzinfo=timezone.utc),
        ),
        accepted_fact_row(
            fact_key="sha256:api-read-fact-001",
            content_fingerprint="sha256:api-read-content-001",
            source_event_id="PLC_001:WS01:301:station_result",
            cycle_counter=301,
            event_ts=datetime(2026, 7, 4, 10, 0, tzinfo=timezone.utc),
            accepted_at=datetime(2026, 7, 4, 10, 0, 1, tzinfo=timezone.utc),
        ),
        accepted_fact_row(
            fact_key="sha256:api-read-fact-003",
            content_fingerprint="sha256:api-read-content-003",
            source_event_id="PLC_001:WS01:303:station_result",
            cycle_counter=303,
            event_ts=datetime(2026, 7, 4, 10, 0, 2, tzinfo=timezone.utc),
            accepted_at=datetime(2026, 7, 4, 10, 0, 3, tzinfo=timezone.utc),
        ),
        accepted_fact_row(
            fact_key="sha256:api-read-other-line",
            content_fingerprint="sha256:api-read-other-line-content",
            line_id="LINE_999",
            source_event_id="PLC_999:WS01:301:station_result",
        ),
        accepted_fact_row(
            fact_key="sha256:api-read-nok-detail",
            content_fingerprint="sha256:api-read-nok-detail-content",
            event_type="station_nok",
            production_result=None,
            source_event_id="PLC_001:WS02:401:station_nok",
            cycle_counter=401,
            event_ts=datetime(2026, 7, 4, 10, 5, tzinfo=timezone.utc),
            accepted_at=datetime(2026, 7, 4, 10, 5, 1, tzinfo=timezone.utc),
            nok_code=30003,
            nok_origin="validated_nok_detail",
            nok_detail_code=30003,
            nok_detail_source_event_id="PLC_001:WS02:401:nok",
            nok_detail_evidence_fact_key="sha256:accepted-upstream-business-fact",
        ),
    ]
    with psycopg.connect(db_backed_api_database.target.raw, autocommit=True) as conn:
        for row in rows:
            insert_accepted_fact(conn, row)
    return rows


def request_events(client: TestClient, **params: Any):
    query = {
        "line_id": "LINE_001",
        "start_time": "2026-07-04T09:00:00Z",
        "end_time": "2026-07-04T11:00:00Z",
    }
    query.update(params)
    return client.get("/api/v2/production/accepted-station-events", params=query)


@pytest.mark.parametrize(
    "dsn",
    [
        "postgresql://edge_mes:pw@localhost:5432/edge_mes_test_api_read",
        "postgresql://edge_mes:pw@127.0.0.1:5432/edge_mes_test_api_read",
        "postgresql://edge_mes:pw@[::1]:5432/edge_mes_test_api_read",
    ],
)
def test_safety_guard_allows_only_local_test_target_dsns(dsn: str) -> None:
    assert validate_test_target_dsn(dsn).database == "edge_mes_test_api_read"


@pytest.mark.parametrize(
    "dsn",
    [
        "postgresql://edge_mes:pw@postgres:5432/edge_mes_test_api_read",
        "postgresql://edge_mes:pw@192.168.1.10:5432/edge_mes_test_api_read",
        "postgresql://edge_mes:pw@db.example.com:5432/edge_mes_test_api_read",
        "postgresql://edge_mes:pw@localhost:5432/edge_mes",
        "postgresql://edge_mes:pw@localhost:5432/postgres",
        "postgresql://edge_mes:pw@localhost:5432/prod",
        "postgresql://edge_mes:pw@localhost:5432/production",
        "postgresql://edge_mes:pw@localhost:5432/edge_mes",
        "postgresql://edge_mes:pw@localhost:5432/edge_mes_api_read",
    ],
)
def test_safety_guard_rejects_compose_remote_and_protected_target_dsns(dsn: str) -> None:
    with pytest.raises(DsnSafetyError):
        validate_test_target_dsn(dsn)


def test_safety_guard_requires_distinct_maintenance_dsn_and_revalidates_drop_statements() -> None:
    plan = build_temp_db_plan(
        "postgresql://edge_mes:pw@localhost:5432/edge_mes_test_api_read",
        "postgresql://edge_mes:pw@localhost:5432/postgres",
    )

    assert plan.target.database == "edge_mes_test_api_read"
    assert plan.maintenance.database == "postgres"
    assert create_temp_database_statement(plan.database_name) == 'CREATE DATABASE "edge_mes_test_api_read"'
    assert drop_temp_database_statement(plan.database_name) == (
        'DROP DATABASE IF EXISTS "edge_mes_test_api_read" WITH (FORCE)'
    )

    for unsafe_name in ("edge_mes", "postgres", "prod", "production", "edge_mes_test-unsafe"):
        with pytest.raises(DsnSafetyError):
            create_temp_database_statement(unsafe_name)
        with pytest.raises(DsnSafetyError):
            drop_temp_database_statement(unsafe_name)
    with pytest.raises(DsnSafetyError):
        build_temp_db_plan(
            "postgresql://edge_mes:pw@localhost:5432/edge_mes_test_api_read",
            "postgresql://edge_mes:pw@localhost:5432/edge_mes_test_api_read",
        )


def test_schema_verification_matrix_is_default_safe_and_complete(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(DB_BACKED_ENABLE_ENV, raising=False)
    queries = accepted_fact_schema_verification_queries()
    joined = "\n".join(queries)

    assert db_backed_tests_enabled() is False
    assert "information_schema.columns" in joined
    assert "pg_constraint" in joined
    assert "to_regclass" in joined
    assert ACCEPTED_FACT_TABLE in joined
    assert EXPECTED_UNIQUE_CONSTRAINTS == {
        "uq_production_accepted_station_event_fact_key",
        "uq_production_accepted_station_event_source",
    }
    assert EXPECTED_CHECK_CONSTRAINTS == {
        "ck_production_accepted_station_event_type",
        "ck_production_accepted_station_event_result",
        "ck_production_accepted_station_result_authority",
        "ck_production_accepted_station_result_nok_authority",
        "ck_production_accepted_station_nok_detail_authority",
    }
    assert set(EXPECTED_ACCEPTED_FACT_COLUMNS) == DTO_FIELDS
    assert EXPECTED_ACCEPTED_FACT_COLUMNS["line_id"] is False
    assert EXPECTED_ACCEPTED_FACT_COLUMNS["event_ts"] is False
    assert EXPECTED_ACCEPTED_FACT_COLUMNS["production_result"] is True
    assert EXPECTED_ACCEPTED_FACT_COLUMNS["nok_detail_evidence_fact_key"] is True
    assert not any(token in joined.upper() for token in ("INSERT", "UPDATE", "DELETE"))


def test_live_api_returns_only_accepted_fact_dto_allowlist_and_no_forbidden_surfaces(
    client: TestClient,
    seeded_rows: list[dict[str, Any]],
    recorder: QueryRecorder,
) -> None:
    response = request_events(client)

    assert response.status_code == 200
    payload = response.json()
    assert [item["line_id"] for item in payload["data"]["items"]] == ["LINE_001"] * 4
    for item in payload["data"]["items"]:
        assert set(item) == DTO_FIELDS
    assert_no_forbidden_surfaces(payload)
    assert payload["page"]["limit"] == 50
    assert_select_source_is_isolated(recorder.select_sql)


def test_live_api_applies_line_window_limit_and_stable_pagination_replay(
    client: TestClient,
    seeded_rows: list[dict[str, Any]],
    recorder: QueryRecorder,
) -> None:
    first = request_events(client, limit="2")

    assert first.status_code == 200
    first_payload = first.json()
    assert [item["fact_key"] for item in first_payload["data"]["items"]] == [
        "sha256:api-read-fact-001",
        "sha256:api-read-fact-002",
    ]
    assert first_payload["page"]["next_cursor"] is not None
    cursor_payload = decode_cursor(first_payload["page"]["next_cursor"])
    assert set(cursor_payload) == {"v", "line_id", "start_time", "end_time", "limit", "direction", "order"}
    assert_no_forbidden_surfaces({"cursor": cursor_payload})

    second = request_events(client, limit="2", cursor=first_payload["page"]["next_cursor"])

    assert second.status_code == 200
    assert [item["fact_key"] for item in second.json()["data"]["items"]] == [
        "sha256:api-read-fact-003",
        "sha256:api-read-nok-detail",
    ]
    statements = recorder.joined_sql.lower()
    assert "where line_id = %s" in statements
    assert "event_ts >= %s" in statements
    assert "event_ts < %s" in statements
    assert "order by event_ts asc, accepted_at asc, fact_key asc" in statements


@pytest.mark.parametrize(
    ("mutation", "request_params"),
    [
        ({"line_id": "LINE_999"}, {}),
        ({}, {"line_id": "LINE_999"}),
        ({}, {"start_time": "2026-07-04T08:00:00Z"}),
        ({}, {"end_time": "2026-07-04T12:00:00Z"}),
        ({}, {"limit": "3"}),
        ({"direction": "desc"}, {}),
    ],
)
def test_live_api_rejects_tampered_or_cross_scope_cursor_before_query(
    client: TestClient,
    seeded_rows: list[dict[str, Any]],
    mutation: dict[str, Any],
    request_params: dict[str, Any],
) -> None:
    first = request_events(client, limit="2")
    assert first.status_code == 200
    cursor = first.json()["page"]["next_cursor"]
    if mutation:
        payload = decode_cursor(cursor)
        payload.update(mutation)
        cursor = encode_unsigned_cursor(payload)

    replay_params = {"limit": "2", "cursor": cursor}
    replay_params.update(request_params)
    response = request_events(client, **replay_params)

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("limit", "expected_status"),
    [
        (None, 200),
        ("1", 200),
        ("500", 200),
        ("0", 422),
        ("-1", 422),
        ("abc", 422),
        ("501", 422),
        ("1.5", 422),
    ],
)
def test_live_api_limit_default_max_and_invalid_behavior(
    client: TestClient,
    seeded_rows: list[dict[str, Any]],
    limit: str | None,
    expected_status: int,
) -> None:
    params = {} if limit is None else {"limit": limit}

    response = request_events(client, **params)

    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json()["page"]["limit"] == (50 if limit is None else int(limit))


def test_live_api_nok_detail_fields_are_sourced_from_accepted_fact_row_only(
    client: TestClient,
    seeded_rows: list[dict[str, Any]],
) -> None:
    response = request_events(client, limit="10")

    assert response.status_code == 200
    item = next(row for row in response.json()["data"]["items"] if row["fact_key"] == "sha256:api-read-nok-detail")
    assert item["nok_code"] == 30003
    assert item["nok_origin"] == "validated_nok_detail"
    assert item["nok_detail_code"] == 30003
    assert item["nok_detail_source_event_id"] == "PLC_001:WS02:401:nok"
    assert item["nok_detail_evidence_fact_key"] == "sha256:accepted-upstream-business-fact"
    assert_no_forbidden_surfaces({"item": item})


def test_live_api_uses_actual_read_only_transaction_timeouts_and_no_mutation_statements(
    client: TestClient,
    seeded_rows: list[dict[str, Any]],
    recorder: QueryRecorder,
) -> None:
    response = request_events(client)

    assert response.status_code == 200
    statements = recorder.joined_sql.upper()
    assert "BEGIN READ ONLY" in statements
    assert "SET LOCAL STATEMENT_TIMEOUT" in statements
    assert "SET LOCAL IDLE_IN_TRANSACTION_SESSION_TIMEOUT" in statements
    assert "COMMIT" in statements
    assert not recorder.write_seen
    assert not recorder.ack_read_done_seen
    assert not recorder.runtime_side_effect_seen


def test_live_api_rolls_back_on_controlled_query_failure_only(
    error_client: TestClient,
    seeded_rows: list[dict[str, Any]],
    failing_recorder: QueryRecorder,
) -> None:
    response = request_events(error_client)

    assert response.status_code == 503
    assert response.json() == {"detail": "accepted fact source unavailable"}
    statements = failing_recorder.joined_sql.upper()
    assert "BEGIN READ ONLY" in statements
    assert "ROLLBACK" in statements
    assert "COMMIT" not in statements
    assert not failing_recorder.write_seen
    assert not failing_recorder.ack_read_done_seen
    assert not failing_recorder.runtime_side_effect_seen
