from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request

from app import db


router = APIRouter(prefix="/api/v2/production", tags=["production"])

DTO_FIELDS = (
    "line_id",
    "plc_id",
    "station_id",
    "station_type",
    "profile_id",
    "config_hash",
    "config_version",
    "event_type",
    "production_result",
    "unit_id",
    "dmc",
    "cycle_counter",
    "source_event_id",
    "event_ts",
    "accepted_at",
    "fact_key",
    "content_fingerprint",
    "nok_code",
    "nok_origin",
    "nok_detail_code",
    "nok_detail_source_event_id",
    "nok_detail_evidence_fact_key",
)

MAX_WINDOW = timedelta(days=31)
MAX_LIMIT = 500
DEFAULT_LIMIT = 50
STATEMENT_TIMEOUT = "3s"
IDLE_TRANSACTION_TIMEOUT = "3s"
QUALITY_QUERY_PARAMS = {"line_id", "station_id", "start_time", "end_time"}
TRACE_QUERY_PARAMS = {
    "line_id",
    "unit_id",
    "dmc",
    "start_time",
    "end_time",
    "limit",
}


def _fail_closed(detail: str) -> None:
    raise HTTPException(status_code=422, detail=detail)


def _validate_query_params(request: Request, allowed: set[str]) -> None:
    names = set(request.query_params.keys())
    if names - allowed:
        _fail_closed("unsupported query parameter")
    if any(len(request.query_params.getlist(name)) != 1 for name in names):
        _fail_closed("duplicate query parameter")


def _required_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        _fail_closed(f"invalid {field_name}")
    return normalized


def _parse_iso_utc(value: str, field_name: str) -> datetime:
    if "T" not in value:
        _fail_closed(f"invalid {field_name}")
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        _fail_closed(f"invalid {field_name}")
    if parsed.tzinfo is None:
        _fail_closed(f"invalid {field_name}")
    return parsed.astimezone(timezone.utc)


def _parse_window(start_time: str, end_time: str) -> tuple[datetime, datetime]:
    start = _parse_iso_utc(start_time, "start_time")
    end = _parse_iso_utc(end_time, "end_time")
    if start >= end or end - start > MAX_WINDOW:
        _fail_closed("invalid time window")
    return start, end


def _parse_limit(value: str | None) -> int:
    if value is None:
        return DEFAULT_LIMIT
    if not value.isdigit():
        _fail_closed("invalid limit")
    limit = int(value)
    if limit < 1 or limit > MAX_LIMIT:
        _fail_closed("invalid limit")
    return limit


def _iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _format_fact(row: dict[str, Any]) -> dict[str, Any]:
    item = {field: row.get(field) for field in DTO_FIELDS}
    for field in ("event_ts", "accepted_at"):
        if isinstance(item[field], datetime):
            item[field] = _iso_z(item[field])
    return item


def _read_quality_rows(
    *,
    line_id: str,
    station_id: str,
    start: datetime,
    end: datetime,
) -> list[dict[str, Any]]:
    with db.get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("BEGIN READ ONLY")
            cur.execute(f"SET LOCAL statement_timeout = '{STATEMENT_TIMEOUT}'")
            cur.execute(
                f"SET LOCAL idle_in_transaction_session_timeout = '{IDLE_TRANSACTION_TIMEOUT}'"
            )
            try:
                cur.execute(
                    """
                    SELECT production_result, nok_code, nok_origin
                    FROM production_accepted_station_event_fact
                    WHERE line_id = %s
                      AND station_id = %s
                      AND event_type = 'station_result'
                      AND event_ts >= %s
                      AND event_ts < %s
                    """,
                    (line_id, station_id, start, end),
                )
                rows = cur.fetchall()
                cur.execute("COMMIT")
                return rows
            except Exception:
                cur.execute("ROLLBACK")
                raise


def _read_trace_rows(
    *,
    line_id: str,
    identity_column: str,
    identity_value: str,
    start: datetime,
    end: datetime,
    limit: int,
) -> list[dict[str, Any]]:
    columns = ", ".join(DTO_FIELDS)
    with db.get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("BEGIN READ ONLY")
            cur.execute(f"SET LOCAL statement_timeout = '{STATEMENT_TIMEOUT}'")
            cur.execute(
                f"SET LOCAL idle_in_transaction_session_timeout = '{IDLE_TRANSACTION_TIMEOUT}'"
            )
            try:
                cur.execute(
                    f"""
                    SELECT {columns}
                    FROM production_accepted_station_event_fact
                    WHERE line_id = %s
                      AND {identity_column} IS NOT NULL
                      AND {identity_column} = %s
                      AND event_ts >= %s
                      AND event_ts < %s
                    ORDER BY event_ts ASC, accepted_at ASC, fact_key ASC
                    LIMIT %s
                    """,
                    (line_id, identity_value, start, end, limit),
                )
                rows = cur.fetchall()
                cur.execute("COMMIT")
                return rows
            except Exception:
                cur.execute("ROLLBACK")
                raise


def _source_unavailable(exc: Exception) -> HTTPException:
    return HTTPException(
        status_code=503,
        detail="accepted fact source unavailable",
    )


@router.get("/quality")
def quality(
    request: Request,
    line_id: str = Query(..., min_length=1),
    station_id: str = Query(..., min_length=1),
    start_time: str = Query(..., min_length=1),
    end_time: str = Query(..., min_length=1),
) -> dict[str, Any]:
    _validate_query_params(request, QUALITY_QUERY_PARAMS)
    line_id = _required_text(line_id, "line_id")
    station_id = _required_text(station_id, "station_id")
    start, end = _parse_window(start_time, end_time)
    try:
        rows = _read_quality_rows(
            line_id=line_id,
            station_id=station_id,
            start=start,
            end=end,
        )
    except Exception as exc:
        raise _source_unavailable(exc) from exc

    good_count = sum(row.get("production_result") == "ok" for row in rows)
    nok_count = sum(row.get("production_result") == "nok" for row in rows)
    denominator = good_count + nok_count
    missing_nok_code = any(
        row.get("production_result") == "nok" and row.get("nok_code") is None
        for row in rows
    )
    nok_distribution = Counter(
        str(row["nok_code"])
        for row in rows
        if row.get("production_result") == "nok" and row.get("nok_code") is not None
    )
    if denominator == 0:
        data_sufficiency = "UNAVAILABLE"
        quality_rate = None
    elif missing_nok_code:
        data_sufficiency = "PARTIAL"
        quality_rate = good_count / denominator
    else:
        data_sufficiency = "SUPPORTED"
        quality_rate = good_count / denominator
    return {
        "scope": {
            "line_id": line_id,
            "station_id": station_id,
            "start_time": _iso_z(start),
            "end_time": _iso_z(end),
        },
        "counts": {
            "ok": good_count,
            "nok": nok_count,
            "denominator": denominator,
        },
        "quality_rate": quality_rate,
        "nok_code_distribution": dict(sorted(nok_distribution.items())),
        "data_sufficiency": data_sufficiency,
    }


@router.get("/trace")
def trace(
    request: Request,
    line_id: str = Query(..., min_length=1),
    unit_id: str | None = Query(default=None),
    dmc: str | None = Query(default=None),
    start_time: str = Query(..., min_length=1),
    end_time: str = Query(..., min_length=1),
    limit: str | None = Query(default=None),
) -> dict[str, Any]:
    _validate_query_params(request, TRACE_QUERY_PARAMS)
    line_id = _required_text(line_id, "line_id")
    unit_value = _required_text(unit_id, "unit_id") if unit_id is not None else None
    dmc_value = _required_text(dmc, "dmc") if dmc is not None else None
    if (unit_value is None) == (dmc_value is None):
        _fail_closed("exactly one of unit_id or dmc is required")
    start, end = _parse_window(start_time, end_time)
    parsed_limit = _parse_limit(limit)
    identity_column, identity_value = (
        ("unit_id", unit_value) if unit_value is not None else ("dmc", dmc_value)
    )
    try:
        rows = _read_trace_rows(
            line_id=line_id,
            identity_column=identity_column,
            identity_value=identity_value,
            start=start,
            end=end,
            limit=parsed_limit,
        )
    except Exception as exc:
        raise _source_unavailable(exc) from exc

    items = [_format_fact(row) for row in rows]
    observed_station_ids = sorted(
        {item["station_id"] for item in items if item.get("station_id") is not None}
    )
    return {
        "data": {"items": items, "limit": parsed_limit},
        "observed_station_ids": observed_station_ids,
        "missing_station_status": "UNKNOWN",
        "route_data_sufficiency": "PARTIAL",
        "data_sufficiency": "PARTIAL" if items else "UNAVAILABLE",
    }
