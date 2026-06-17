from fastapi import APIRouter

from app.db import get_conn

router = APIRouter()


@router.get("/health")
def health() -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            cur.fetchone()
    return {"status": "ok"}

