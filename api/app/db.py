import os
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row


def dsn() -> str:
    return os.environ.get("DATABASE_URL", "postgresql://edge_mes:edge_mes_password@localhost:5432/edge_mes")


@contextmanager
def get_conn():
    conn = psycopg.connect(dsn(), row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()

