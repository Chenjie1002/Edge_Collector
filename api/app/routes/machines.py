from fastapi import APIRouter, HTTPException

from app.db import get_conn

router = APIRouter(prefix="/machines", tags=["machines"])


@router.get("")
def list_machines() -> list[dict]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM machines ORDER BY machine_id")
            return cur.fetchall()


@router.get("/{machine_id}/current")
def current(machine_id: str) -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM production_snapshot
                WHERE machine_id = %s
                ORDER BY ts DESC
                LIMIT 1
                """,
                (machine_id,),
            )
            row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="No snapshot found")
    return row

