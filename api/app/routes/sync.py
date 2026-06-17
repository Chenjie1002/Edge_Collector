from fastapi import APIRouter

from app.db import get_conn

router = APIRouter(prefix="/sync", tags=["sync"])


@router.get("/status")
def status() -> list[dict]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT status, count(*) AS count
                FROM sync_outbox
                GROUP BY status
                ORDER BY status
                """
            )
            return cur.fetchall()

