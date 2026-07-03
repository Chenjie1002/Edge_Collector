from __future__ import annotations

import os
import re
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pytest


DB_BACKED_ENABLE_ENV = "EDGE_MES_ENABLE_DB_BACKED_TESTS"
DB_BACKED_TARGET_DSN_ENV = "EDGE_MES_DB_BACKED_TEST_DSN"
DB_BACKED_MAINTENANCE_DSN_ENV = "EDGE_MES_DB_BACKED_MAINTENANCE_DSN"
LOCAL_TEST_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
COMPOSE_LOCAL_HOST = "postgres"
PROTECTED_DATABASE_NAMES = frozenset({"edge_mes", "postgres", "prod", "production"})
TEST_DATABASE_RE = re.compile(r"^edge_mes_test_[A-Za-z0-9_]+$")


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


def db_backed_tests_enabled(env: dict[str, str] | None = None) -> bool:
    env = env if env is not None else os.environ
    return env.get(DB_BACKED_ENABLE_ENV) == "1"


def pytest_collection_modifyitems(config, items) -> None:
    if db_backed_tests_enabled():
        return
    skip = pytest.mark.skip(reason=f"DB-backed tests require {DB_BACKED_ENABLE_ENV}=1")
    for item in items:
        marker_names = {marker.name for marker in item.iter_markers()}
        if {"db_backed", "postgres_local"} & marker_names:
            item.add_marker(skip)


def validate_test_target_dsn(dsn: str, *, allow_compose_host: bool = False) -> SafeDsn:
    parts = _parse_postgres_dsn(dsn)
    allowed_hosts = set(LOCAL_TEST_HOSTS)
    if allow_compose_host:
        allowed_hosts.add(COMPOSE_LOCAL_HOST)
    if parts.host not in allowed_hosts:
        raise DsnSafetyError(f"test target DSN host is not local/test-only: {parts.host}")
    if parts.database in PROTECTED_DATABASE_NAMES or not TEST_DATABASE_RE.fullmatch(parts.database):
        raise DsnSafetyError(f"test target DSN database must match edge_mes_test_*: {parts.database}")
    return parts


def validate_maintenance_dsn(dsn: str, *, allow_compose_host: bool = False) -> SafeDsn:
    parts = _parse_postgres_dsn(dsn)
    allowed_hosts = set(LOCAL_TEST_HOSTS)
    if allow_compose_host:
        allowed_hosts.add(COMPOSE_LOCAL_HOST)
    if parts.host not in allowed_hosts:
        raise DsnSafetyError(f"maintenance DSN host is not local/test-only: {parts.host}")
    if TEST_DATABASE_RE.fullmatch(parts.database):
        raise DsnSafetyError("maintenance DSN must be distinct from test-target DSN")
    if parts.database not in {"postgres", "template1"}:
        raise DsnSafetyError("maintenance DSN must point to postgres or template1 only")
    return parts


def build_temp_db_plan(
    target_dsn: str,
    maintenance_dsn: str,
    *,
    run_id: str | None = None,
    allow_compose_host: bool = False,
) -> TempDbPlan:
    target = validate_test_target_dsn(target_dsn, allow_compose_host=allow_compose_host)
    maintenance = validate_maintenance_dsn(maintenance_dsn, allow_compose_host=allow_compose_host)
    if target.database == maintenance.database:
        raise DsnSafetyError("test-target DSN and maintenance DSN must be distinct")
    if run_id is not None and not TEST_DATABASE_RE.fullmatch(f"edge_mes_test_{run_id}"):
        raise DsnSafetyError(f"run_id would not produce a safe temp DB name: {run_id}")
    return TempDbPlan(
        target=target,
        maintenance=maintenance,
        database_name=target.database,
        migration_files=tuple(migration_files_for_accepted_fact()),
    )


def drop_temp_database_statement(database_name: str) -> str:
    if not TEST_DATABASE_RE.fullmatch(database_name):
        raise DsnSafetyError(f"refusing to drop non-test database: {database_name}")
    return f'DROP DATABASE IF EXISTS "{database_name}" WITH (FORCE)'


def migration_files_for_accepted_fact(repo_root: Path | None = None) -> tuple[Path, ...]:
    root = repo_root or Path(__file__).resolve().parents[2]
    init_files = tuple(sorted((root / "db" / "init").glob("*.sql")))
    return init_files + (root / "db" / "migrations" / "007_accepted_station_event_visibility.sql",)


def accepted_fact_schema_verification_queries() -> tuple[str, ...]:
    return (
        "SELECT to_regclass('public.production_accepted_station_event_fact') IS NOT NULL",
        """
        SELECT EXISTS (
            SELECT 1 FROM pg_constraint
            WHERE conname = 'uq_production_accepted_station_event_fact_key'
        )
        """,
        """
        SELECT EXISTS (
            SELECT 1 FROM pg_constraint
            WHERE conname = 'uq_production_accepted_station_event_source'
        )
        """,
        """
        SELECT COUNT(*) >= 4 FROM pg_constraint
        WHERE conname LIKE 'ck_production_accepted_station_%'
        """,
    )


@pytest.fixture
def db_backed_temp_db_plan() -> TempDbPlan:
    if not db_backed_tests_enabled():
        pytest.skip(f"DB-backed tests require {DB_BACKED_ENABLE_ENV}=1")
    target_dsn = os.environ.get(DB_BACKED_TARGET_DSN_ENV)
    maintenance_dsn = os.environ.get(DB_BACKED_MAINTENANCE_DSN_ENV)
    if not target_dsn or not maintenance_dsn:
        pytest.skip(f"DB-backed tests require {DB_BACKED_TARGET_DSN_ENV} and {DB_BACKED_MAINTENANCE_DSN_ENV}")
    return build_temp_db_plan(target_dsn, maintenance_dsn, allow_compose_host=True)


@pytest.fixture
def db_backed_temp_database(db_backed_temp_db_plan):
    import psycopg
    from psycopg import sql

    plan = db_backed_temp_db_plan
    with psycopg.connect(plan.maintenance.raw, autocommit=True) as admin_conn:
        admin_conn.execute(drop_temp_database_statement(plan.database_name))
        admin_conn.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(plan.database_name)))
    try:
        with psycopg.connect(plan.target.raw, autocommit=True) as conn:
            for migration_file in plan.migration_files:
                conn.execute(migration_file.read_text(encoding="utf-8"))
            verify_accepted_fact_schema(conn)
        yield plan
    finally:
        with psycopg.connect(plan.maintenance.raw, autocommit=True) as admin_conn:
            admin_conn.execute(drop_temp_database_statement(plan.database_name))


@pytest.fixture
def db_backed_storage(db_backed_temp_database):
    from app.services.storage import Storage

    storage = Storage(db_backed_temp_database.target.raw)
    try:
        verify_accepted_fact_schema(storage.conn)
        yield storage
    finally:
        storage.conn.close()


@pytest.fixture
def safe_local_unreachable_test_dsn() -> str:
    dsn = "postgresql://edge_mes:edge_mes_password@127.0.0.1:1/edge_mes_test_unreachable"
    validate_test_target_dsn(dsn)
    return dsn


@pytest.fixture
def accepted_fact_count():
    def count(storage) -> int:
        with storage.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM production_accepted_station_event_fact")
            return int(cur.fetchone()[0])

    return count


@pytest.fixture
def accepted_station_result_fact():
    from app.services.accepted_station_event_fact import AcceptedStationEventFact

    return AcceptedStationEventFact(
        line_id="LINE_001",
        plc_id="PLC_001",
        station_id="WS01",
        station_type="screw",
        profile_id="normal_screwdriving",
        config_hash="a" * 64,
        config_version="2026.06.20-1",
        event_type="station_result",
        production_result="ok",
        unit_id="U-20260618-000005",
        dmc="SUB-000005",
        cycle_counter=5,
        source_event_id="PLC_001:WS01:5:station_result",
        event_ts=datetime(2026, 6, 26, 10, 0, 30, tzinfo=timezone.utc),
        fact_key="sha256:" + "1" * 64,
        content_fingerprint="sha256:" + "2" * 64,
    )


@pytest.fixture
def accepted_station_result_fact_with(accepted_station_result_fact):
    def factory(**changes: Any):
        return replace(accepted_station_result_fact, **changes)

    return factory


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


def verify_accepted_fact_schema(conn) -> None:
    with conn.cursor() as cur:
        for query in accepted_fact_schema_verification_queries():
            cur.execute(query)
            row = cur.fetchone()
            if row is None or row[0] is not True:
                raise AssertionError("accepted station-event fact schema verification failed")
