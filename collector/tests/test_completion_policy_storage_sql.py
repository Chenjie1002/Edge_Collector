from __future__ import annotations

from app.services.resolved_config_registry import CompletionPolicy
from app.services.storage import Storage


class _Cursor:
    def __init__(self) -> None:
        self.sql = ""
        self.params: tuple[object, ...] = ()

    def __enter__(self) -> "_Cursor":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def execute(self, sql: str, params: tuple[object, ...]) -> None:
        self.sql = sql
        self.params = tuple(params)


class _Connection:
    def __init__(self) -> None:
        self.cursor_instance = _Cursor()

    def cursor(self) -> _Cursor:
        return self.cursor_instance


def test_storage_completion_sql_binds_projected_terminal_without_ws03_literal() -> None:
    storage = Storage.__new__(Storage)
    connection = _Connection()
    storage.conn = connection

    policy = CompletionPolicy(
        line_id="LINE_DEMO_10",
        config_hash="demo-hash",
        entry_station_id="WS01",
        terminal_station_id="WS10",
    )
    storage.upsert_production_unit_for_event(41, completion_policy=policy)

    assert "'WS03'" not in connection.cursor_instance.sql
    assert connection.cursor_instance.params == ("WS10",) * 6 + (41,)
