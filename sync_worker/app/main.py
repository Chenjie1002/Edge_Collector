import logging
import os
import time

import psycopg
from psycopg.rows import dict_row

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("sync-worker")


def dsn() -> str:
    return os.environ.get("DATABASE_URL", "postgresql://edge_mes:edge_mes_password@localhost:5432/edge_mes")


def sync_batch() -> int:
    with psycopg.connect(dsn(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, target_table, payload
                FROM sync_outbox
                WHERE status = 'pending'
                ORDER BY id
                LIMIT 100
                FOR UPDATE SKIP LOCKED
                """
            )
            rows = cur.fetchall()
            if not rows:
                return 0
            ids = [row["id"] for row in rows]
            logger.info("mock synced %s records to Oracle staging tables", len(ids))
            cur.execute(
                """
                UPDATE sync_outbox
                SET status = 'synced', synced_at = now()
                WHERE id = ANY(%s)
                """,
                (ids,),
            )
        conn.commit()
        return len(ids)


def main() -> None:
    logger.info("sync worker started in mock mode")
    while True:
        try:
            count = sync_batch()
            if count == 0:
                time.sleep(10)
        except Exception:
            logger.exception("sync worker failed")
            time.sleep(10)


if __name__ == "__main__":
    main()

