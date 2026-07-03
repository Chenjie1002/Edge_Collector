from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

import conftest as db_test_conftest
from conftest import (
    DB_BACKED_ENABLE_ENV,
    DsnSafetyError,
    build_temp_db_plan,
    db_backed_tests_enabled,
    drop_temp_database_statement,
    migration_files_for_accepted_fact,
    pytest_collection_modifyitems,
    accepted_fact_schema_verification_queries,
    validate_maintenance_dsn,
    validate_test_target_dsn,
)


@pytest.mark.parametrize(
    "dsn",
    [
        "postgresql://edge_mes:pw@localhost:5432/edge_mes_test_slice2",
        "postgresql://edge_mes:pw@127.0.0.1:5432/edge_mes_test_slice2",
        "postgresql://edge_mes:pw@[::1]:5432/edge_mes_test_slice2",
        "postgresql://edge_mes:pw@postgres:5432/edge_mes_test_slice2",
    ],
)
def test_test_target_dsn_allows_only_local_test_hosts_and_test_db_names(dsn: str) -> None:
    parts = validate_test_target_dsn(dsn, allow_compose_host=True)

    assert parts.database == "edge_mes_test_slice2"


@pytest.mark.parametrize(
    "dsn",
    [
        "postgresql://edge_mes:pw@192.168.1.10:5432/edge_mes_test_slice2",
        "postgresql://edge_mes:pw@db.example.com:5432/edge_mes_test_slice2",
        "postgresql://edge_mes:pw@postgres:5432/edge_mes_test_slice2",
        "postgresql://edge_mes:pw@localhost:5432/edge_mes",
        "postgresql://edge_mes:pw@localhost:5432/postgres",
        "postgresql://edge_mes:pw@localhost:5432/prod",
        "postgresql://edge_mes:pw@localhost:5432/production",
        "postgresql://edge_mes:pw@localhost:5432/edge_mes_slice2",
    ],
)
def test_test_target_dsn_rejects_external_hosts_and_non_test_db_names(dsn: str) -> None:
    with pytest.raises(DsnSafetyError):
        validate_test_target_dsn(dsn)


def test_maintenance_dsn_is_guarded_and_distinct_from_test_target() -> None:
    target = "postgresql://edge_mes:pw@localhost:5432/edge_mes_test_slice2"
    maintenance = "postgresql://edge_mes:pw@localhost:5432/postgres"

    plan = build_temp_db_plan(target, maintenance, run_id="run_001")

    assert plan.target.database == "edge_mes_test_slice2"
    assert plan.maintenance.database == "postgres"
    assert plan.database_name.startswith("edge_mes_test_")


def test_maintenance_dsn_rejects_remote_hosts_and_test_target_db_names() -> None:
    with pytest.raises(DsnSafetyError):
        validate_maintenance_dsn("postgresql://edge_mes:pw@db.example.com:5432/postgres")
    with pytest.raises(DsnSafetyError):
        validate_maintenance_dsn("postgresql://edge_mes:pw@localhost:5432/edge_mes_test_slice2")


def test_drop_statement_is_only_generated_for_proven_test_database_names() -> None:
    assert drop_temp_database_statement("edge_mes_test_run_001") == (
        'DROP DATABASE IF EXISTS "edge_mes_test_run_001" WITH (FORCE)'
    )

    for protected_name in ("edge_mes", "postgres", "prod", "production", "edge_mes_test-unsafe"):
        with pytest.raises(DsnSafetyError):
            drop_temp_database_statement(protected_name)


def test_migration_loading_order_is_deterministic_and_includes_visibility_migration() -> None:
    files = migration_files_for_accepted_fact()

    assert [path.name for path in files[:4]] == [
        "001_schema.sql",
        "002_seed.sql",
        "003_event_schema.sql",
        "004_unit_trace_schema.sql",
    ]
    assert files[-1].as_posix().endswith("db/migrations/007_accepted_station_event_visibility.sql")


def test_schema_verification_queries_check_table_unique_constraints_and_ck_constraints() -> None:
    joined = "\n".join(accepted_fact_schema_verification_queries())

    assert "production_accepted_station_event_fact" in joined
    assert "uq_production_accepted_station_event_fact_key" in joined
    assert "uq_production_accepted_station_event_source" in joined
    assert "ck_production_accepted_station_%" in joined


def test_db_backed_default_skip_marker_is_added_before_fixture_setup(monkeypatch) -> None:
    monkeypatch.delenv(DB_BACKED_ENABLE_ENV, raising=False)
    item = SimpleNamespace(
        iter_markers=lambda: iter([SimpleNamespace(name="db_backed")]),
        add_marker=lambda marker: setattr(item, "skip_marker", marker),
    )

    pytest_collection_modifyitems(config=None, items=[item])

    assert db_backed_tests_enabled() is False
    assert item.skip_marker.kwargs["reason"].startswith("DB-backed tests require")


def test_db_backed_opt_in_env_is_explicit(monkeypatch) -> None:
    monkeypatch.setenv(DB_BACKED_ENABLE_ENV, "1")

    assert db_backed_tests_enabled() is True


def test_future_db_authorized_scenarios_are_not_placeholder_pytest_coverage() -> None:
    placeholder_fixture_names = {
        "simulate_unique_violation_after_precheck",
        "db_backed_worker",
        "fail_next_production_fact_write",
        "fail_next_legacy_current_write",
        "fail_next_commit",
    }
    discovered_fixture_names = placeholder_fixture_names & set(vars(db_test_conftest))

    db_backed_test_source = Path(__file__).with_name("test_event_collector_accepted_fact_db_backed.py").read_text(
        encoding="utf-8"
    )

    assert discovered_fixture_names == set()
    assert "FUTURE_DB_AUTHORIZED_SCENARIOS" in db_backed_test_source
    assert "def test_db_backed_unique_violation_after_precheck" not in db_backed_test_source
    assert "def test_db_backed_production_fact_failure_rolls_back_legacy_current" not in db_backed_test_source
    assert "def test_db_backed_legacy_current_failure_rolls_back_production_fact" not in db_backed_test_source
    assert "def test_db_backed_commit_failure_rolls_back_before_ack" not in db_backed_test_source
    assert "def test_db_backed_non_accepted_writes_zero_production_rows_and_no_ack" not in db_backed_test_source
    assert (
        "def test_db_backed_non_accepted_read_done_preserves_no_ack_read_done_mutation_for_current_payload"
        not in db_backed_test_source
    )
