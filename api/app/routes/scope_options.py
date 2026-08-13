from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from app.services.scope_catalog import ScopeCatalogUnavailable, load_scope_catalog


router = APIRouter(prefix="/api/v2/production", tags=["production"])
UNSUPPORTED_REQUEST_DETAIL = "unsupported scope-options request"


@router.get("/scope-options")
async def scope_options(request: Request) -> dict[str, object]:
    if await request.body() or request.query_params:
        raise HTTPException(status_code=422, detail=UNSUPPORTED_REQUEST_DETAIL)
    try:
        return load_scope_catalog()
    except ScopeCatalogUnavailable as exc:
        raise HTTPException(
            status_code=503,
            detail="Scope catalog is not available.",
        ) from exc
