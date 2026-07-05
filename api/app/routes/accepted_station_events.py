from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
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

CURSOR_VERSION = 1
CURSOR_DIRECTION = "asc"
MAX_LIMIT = 500
DEFAULT_LIMIT = 50
MAX_WINDOW = timedelta(days=31)
STATEMENT_TIMEOUT = "3s"
IDLE_TRANSACTION_TIMEOUT = "3s"
ALLOWED_QUERY_PARAMS = {"line_id", "start_time", "end_time", "limit", "cursor"}


def _fail_closed(detail: str) -> None:
    raise HTTPException(status_code=422, detail=detail)


def _validate_query_params(request: Request) -> None:
    unsupported = set(request.query_params) - ALLOWED_QUERY_PARAMS
    if unsupported:
        _fail_closed("unsupported query parameter")


def _parse_limit(value: str | None) -> int:
    if value is None:
        return DEFAULT_LIMIT
    if not value.isdigit():
        _fail_closed("invalid limit")
    limit = int(value)
    if limit < 1 or limit > MAX_LIMIT:
        _fail_closed("invalid limit")
    return limit


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


def _iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _json_default(value: Any) -> Any:
    if isinstance(value, datetime):
        return _iso_z(value)
    raise TypeError(f"unsupported cursor value: {type(value)!r}")


def _cursor_key() -> bytes:
    return os.environ.get(
        "ACCEPTED_STATION_EVENTS_CURSOR_SECRET",
        "edge-mes-accepted-station-events-cursor-v1",
    ).encode("utf-8")


def _encode_part(payload: dict[str, Any]) -> str:
    return base64.urlsafe_b64encode(
        json.dumps(
            payload,
            default=_json_default,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).decode("ascii").rstrip("=")


def _sign(encoded_payload: str) -> str:
    return hmac.new(
        _cursor_key(),
        encoded_payload.encode("ascii"),
        hashlib.sha256,
    ).hexdigest()


def _encode_cursor(payload: dict[str, Any]) -> str:
    encoded_payload = _encode_part(payload)
    return f"{encoded_payload}.{_sign(encoded_payload)}"


def _decode_cursor(value: str) -> dict[str, Any]:
    try:
        encoded_payload, signature = value.split(".", 1)
        expected = _sign(encoded_payload)
        if not hmac.compare_digest(signature, expected):
            _fail_closed("invalid cursor")
        padded = encoded_payload + "=" * (-len(encoded_payload) % 4)
        payload = json.loads(
            base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8")
        )
    except HTTPException:
        raise
    except Exception:
        _fail_closed("invalid cursor")
    if not isinstance(payload, dict):
        _fail_closed("invalid cursor")
    return payload


def _parse_cursor(
    value: str | None,
    *,
    line_id: str,
    start_time: str,
    end_time: str,
    limit: int,
) -> tuple[datetime, datetime, str] | None:
    if value is None:
        return None
    payload = _decode_cursor(value)
    required_shape = {
        "v",
        "line_id",
        "start_time",
        "end_time",
        "limit",
        "direction",
        "order",
    }
    if set(payload) != required_shape:
        _fail_closed("invalid cursor")
    if (
        payload.get("v") != CURSOR_VERSION
        or payload.get("line_id") != line_id
        or payload.get("start_time") != start_time
        or payload.get("end_time") != end_time
        or payload.get("limit") != limit
        or payload.get("direction") != CURSOR_DIRECTION
    ):
        _fail_closed("invalid cursor")
    order = payload.get("order")
    if not isinstance(order, list) or len(order) != 3 or not all(isinstance(item, str) for item in order):
        _fail_closed("invalid cursor")
    return (
        _parse_iso_utc(order[0], "cursor"),
        _parse_iso_utc(order[1], "cursor"),
        order[2],
    )


def _cursor_payload(
    *,
    line_id: str,
    start_time: str,
    end_time: str,
    limit: int,
    row: dict[str, Any],
) -> dict[str, Any]:
    return {
        "v": CURSOR_VERSION,
        "line_id": line_id,
        "start_time": start_time,
        "end_time": end_time,
        "limit": limit,
        "direction": CURSOR_DIRECTION,
        "order": [
            _iso_z(row["event_ts"]),
            _iso_z(row["accepted_at"]),
            row["fact_key"],
        ],
    }


def _format_row(row: dict[str, Any]) -> dict[str, Any]:
    item = {field: row.get(field) for field in DTO_FIELDS}
    for field in ("event_ts", "accepted_at"):
        value = item[field]
        if isinstance(value, datetime):
            item[field] = _iso_z(value)
    return item


def _read_rows(
    *,
    line_id: str,
    start: datetime,
    end: datetime,
    limit: int,
    cursor_tuple: tuple[datetime, datetime, str] | None,
) -> list[dict[str, Any]]:
    columns = ", ".join(DTO_FIELDS)
    params: list[Any] = [line_id, start, end]
    cursor_clause = ""
    if cursor_tuple is not None:
        cursor_clause = """
                  AND (event_ts, accepted_at, fact_key) > (%s, %s, %s)
        """
        params.extend(cursor_tuple)
    params.append(limit + 1)

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
                      AND event_ts >= %s
                      AND event_ts < %s
                    {cursor_clause}
                    ORDER BY event_ts ASC, accepted_at ASC, fact_key ASC
                    LIMIT %s
                    """,
                    tuple(params),
                )
                rows = cur.fetchall()
                cur.execute("COMMIT")
                return rows
            except Exception:
                cur.execute("ROLLBACK")
                raise


@router.get("/accepted-station-events")
def list_accepted_station_events(
    request: Request,
    line_id: str = Query(..., min_length=1),
    start_time: str = Query(..., min_length=1),
    end_time: str = Query(..., min_length=1),
    limit: str | None = Query(default=None),
    cursor: str | None = Query(default=None),
) -> dict[str, Any]:
    _validate_query_params(request)
    parsed_limit = _parse_limit(limit)
    start = _parse_iso_utc(start_time, "start_time")
    end = _parse_iso_utc(end_time, "end_time")
    if start >= end or end - start > MAX_WINDOW:
        _fail_closed("invalid time window")
    cursor_tuple = _parse_cursor(
        cursor,
        line_id=line_id,
        start_time=start_time,
        end_time=end_time,
        limit=parsed_limit,
    )

    try:
        rows = _read_rows(
            line_id=line_id,
            start=start,
            end=end,
            limit=parsed_limit,
            cursor_tuple=cursor_tuple,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="accepted fact source unavailable",
        ) from exc
    page_rows = rows[:parsed_limit]
    next_cursor = None
    if len(rows) > parsed_limit:
        next_cursor = _encode_cursor(
            _cursor_payload(
                line_id=line_id,
                start_time=start_time,
                end_time=end_time,
                limit=parsed_limit,
                row=page_rows[-1],
            )
        )
    return {
        "data": {"items": [_format_row(row) for row in page_rows]},
        "page": {"next_cursor": next_cursor, "limit": parsed_limit},
    }
