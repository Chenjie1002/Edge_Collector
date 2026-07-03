from __future__ import annotations

import pytest


pytestmark = [pytest.mark.db_backed, pytest.mark.postgres_local]


FUTURE_DB_AUTHORIZED_SCENARIOS = (
    "race / unique-violation-after-precheck executable local Postgres harness",
    "worker-level DB-backed accepted path rollback",
    "worker-level commit failure before ACK",
    "worker-level non-accepted DB-backed zero rows + no ACK/read_done mutation",
    "post-unique-violation re-read semantics if PM later requires idempotent race behavior",
)


def test_db_backed_direct_insert_accepted_fact(db_backed_storage, accepted_station_result_fact):
    result = db_backed_storage.insert_accepted_station_event_fact_no_commit(accepted_station_result_fact)

    assert result == "inserted"


def test_db_backed_unique_fact_key_same_content_is_noop(db_backed_storage, accepted_station_result_fact):
    assert db_backed_storage.insert_accepted_station_event_fact_no_commit(accepted_station_result_fact) == "inserted"
    assert db_backed_storage.insert_accepted_station_event_fact_no_commit(accepted_station_result_fact) == "existing"


def test_db_backed_unique_fact_key_different_content_conflicts(
    db_backed_storage,
    accepted_station_result_fact,
    accepted_station_result_fact_with,
):
    db_backed_storage.insert_accepted_station_event_fact_no_commit(accepted_station_result_fact)
    conflicting = accepted_station_result_fact_with(content_fingerprint="sha256:" + "9" * 64)

    with pytest.raises(ValueError, match="fact_key content differs"):
        db_backed_storage.insert_accepted_station_event_fact_no_commit(conflicting)


def test_db_backed_unique_source_identity_same_content_is_noop(
    db_backed_storage,
    accepted_station_result_fact,
    accepted_station_result_fact_with,
):
    db_backed_storage.insert_accepted_station_event_fact_no_commit(accepted_station_result_fact)
    duplicate_source = accepted_station_result_fact_with(fact_key="sha256:" + "3" * 64)

    assert db_backed_storage.insert_accepted_station_event_fact_no_commit(duplicate_source) == "existing"


def test_db_backed_unique_source_identity_different_content_conflicts(
    db_backed_storage,
    accepted_station_result_fact,
    accepted_station_result_fact_with,
):
    db_backed_storage.insert_accepted_station_event_fact_no_commit(accepted_station_result_fact)
    conflicting = accepted_station_result_fact_with(
        fact_key="sha256:" + "4" * 64,
        content_fingerprint="sha256:" + "9" * 64,
    )

    with pytest.raises(ValueError, match="source identity content differs"):
        db_backed_storage.insert_accepted_station_event_fact_no_commit(conflicting)


def test_db_backed_transaction_body_exception_rolls_back(
    db_backed_storage,
    accepted_station_result_fact,
    accepted_fact_count,
):
    with pytest.raises(RuntimeError, match="simulated transaction body failure"):
        with db_backed_storage.transaction():
            db_backed_storage.insert_accepted_station_event_fact_no_commit(accepted_station_result_fact)
            raise RuntimeError("simulated transaction body failure")

    assert accepted_fact_count(db_backed_storage) == 0


def test_db_backed_connection_failure_uses_safe_local_test_dsn_only(safe_local_unreachable_test_dsn):
    from app.services.storage import Storage

    with pytest.raises(Exception):
        Storage(safe_local_unreachable_test_dsn)
