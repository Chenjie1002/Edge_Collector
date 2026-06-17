from fastapi import APIRouter

from app.db import get_conn

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
def list_events(machine_id: str = "LINE_01", limit: int = 100) -> list[dict]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM production_events
                WHERE machine_id = %s
                ORDER BY ts DESC
                LIMIT %s
                """,
                (machine_id, limit),
            )
            return cur.fetchall()

