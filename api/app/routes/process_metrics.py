from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
import re
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app import db


router = APIRouter(tags=["process-metrics"])

CONTRACT_VERSION = "P1-G3-PROCESS-KPI-1.0"
SOURCE_AUTHORITY = "production_accepted_station_event_fact"
ALLOWED_RESULTS = {"ok", "nok", "skip", "not_applicable"}
FIXED_METRICS = (
    "accepted_event_count",
    "observed_accepted_event_rate",
    "accepted_unit_count",
    "quality_good_event_count",
    "quality_nok_event_count",
    "quality_denominator_event_count",
    "quality_rate",
    "station_cycle_time",
    "ideal_cycle_time",
    "line_accepted_event_count",
    "terminal_accepted_event_count",
    "performance",
    "availability",
    "full_oee",
)
REQUIRED_QUERY_PARAMS = {"line_id", "station_id", "from", "to"}
MAX_WINDOW = timedelta(days=31)
REQUIRED_NOK_DETAIL_FIELDS = (
    "nok_code",
    "nok_origin",
    "nok_detail_code",
    "nok_detail_source_event_id",
    "nok_detail_evidence_fact_key",
)
RFC3339_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)


def _iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _window(start: datetime, end: datetime) -> dict[str, object]:
    return {
        "from": _iso_z(start),
        "to": _iso_z(end),
        "interval": "[from,to)",
        "duration_seconds": (end - start).total_seconds(),
    }


def _scope(line_id: str, station_id: str) -> dict[str, str]:
    return {"line_id": line_id, "station_id": station_id, "aggregation": "station"}


def _missing_text(value: object) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _source(*, config_window_state: str) -> dict[str, str]:
    return {
        "authority": SOURCE_AUTHORITY,
        "identity": "fact_key",
        "config_window_state": config_window_state,
        "fallback": "none",
    }


def _invalid_request(detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "contract_version": CONTRACT_VERSION,
            "error": {"code": "INVALID_REQUEST", "detail": detail},
        },
    )


def _parse_rfc3339_utc(value: str, field_name: str) -> datetime:
    if not value or not RFC3339_PATTERN.fullmatch(value):
        raise ValueError(f"invalid {field_name}")
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ValueError(f"invalid {field_name}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"invalid {field_name}")
    return parsed.astimezone(timezone.utc)


def _validated_query(request: Request) -> tuple[str, str, datetime, datetime] | JSONResponse:
    items = list(request.query_params.multi_items())
    names = [name for name, _ in items]
    unknown = set(names) - REQUIRED_QUERY_PARAMS
    if unknown:
        return _invalid_request("unsupported query parameter")
    duplicates = [name for name, count in Counter(names).items() if count != 1]
    if duplicates:
        return _invalid_request("duplicate query parameter")
    if set(names) != REQUIRED_QUERY_PARAMS:
        return _invalid_request("missing required query parameter")
    values = dict(items)
    line_id = values["line_id"].strip()
    station_id = values["station_id"].strip()
    if not line_id:
        return _invalid_request("invalid line_id")
    if not station_id:
        return _invalid_request("invalid station_id")
    try:
        start = _parse_rfc3339_utc(values["from"], "from")
        end = _parse_rfc3339_utc(values["to"], "to")
    except ValueError as exc:
        return _invalid_request(str(exc))
    duration = end - start
    if start >= end:
        return _invalid_request("invalid time window")
    if duration > MAX_WINDOW:
        return _invalid_request("invalid time window")
    return line_id, station_id, start, end


def _metric(
    *,
    name: str,
    unit: str,
    counting_unit: str,
    status: str,
    reason_code: str,
    detail: str,
    authority: str,
    lineage: str,
    value: float | int | None = None,
) -> dict[str, object]:
    metric: dict[str, object] = {
        "name": name,
        "unit": unit,
        "counting_unit": counting_unit,
        "status": status,
        "reason": {"code": reason_code, "detail": detail},
        "source": {
            "authority": authority,
            "lineage": lineage,
            "fallback": "none",
        },
        "numeric_value_allowed": value is not None,
    }
    if value is not None:
        metric["value"] = value
    return metric


def _unsupported_metrics(*, config_window_state: str) -> list[dict[str, object]]:
    ideal_reason = (
        "MIXED_HISTORICAL_CONFIG_WINDOW"
        if config_window_state == "MIXED"
        else "HISTORICAL_CONFIG_AUTHORITY_MISSING"
    )
    return [
        _metric(
            name="accepted_unit_count",
            unit="units",
            counting_unit="unit-count",
            status="UNSUPPORTED",
            reason_code="UNIT_COUNTING_AUTHORITY_NOT_ACCEPTED",
            detail="station-result to unit one-to-one authority is not accepted",
            authority="not-accepted",
            lineage="accepted unit identity authority",
        ),
        _metric(
            name="station_cycle_time",
            unit="seconds",
            counting_unit="unavailable",
            status="PARTIAL",
            reason_code="CYCLE_INSTANCE_PAIRING_AUTHORITY_MISSING",
            detail="producer-authoritative cycle-instance pairing is not accepted",
            authority="not-accepted",
            lineage="cycle-instance start/complete pairing key",
        ),
        _metric(
            name="ideal_cycle_time",
            unit="seconds",
            counting_unit="unavailable",
            status="PARTIAL",
            reason_code=ideal_reason,
            detail="historical immutable config/profile authority is not resolved",
            authority="not-accepted",
            lineage="historical config_hash+config_version+profile",
        ),
        _metric(
            name="line_accepted_event_count",
            unit="events",
            counting_unit="unavailable",
            status="UNSUPPORTED",
            reason_code="LINE_OUTPUT_AUTHORITY_NOT_ACCEPTED",
            detail="station scope does not establish line output authority",
            authority="not-accepted",
            lineage="accepted line-output authority",
        ),
        _metric(
            name="terminal_accepted_event_count",
            unit="events",
            counting_unit="unavailable",
            status="UNSUPPORTED",
            reason_code="HISTORICAL_TERMINAL_LINEAGE_UNAVAILABLE",
            detail="historical terminal lineage is not resolved",
            authority="not-accepted",
            lineage="historical terminal resolution",
        ),
        _metric(
            name="performance",
            unit="ratio",
            counting_unit="unavailable",
            status="UNSUPPORTED",
            reason_code="PERFORMANCE_AUTHORITIES_NOT_ACCEPTED",
            detail="ideal cycle time and operating-time authority are absent",
            authority="not-accepted",
            lineage="historical ideal CT+authoritative operating/run-time",
        ),
        _metric(
            name="availability",
            unit="ratio",
            counting_unit="unavailable",
            status="UNSUPPORTED",
            reason_code="AVAILABILITY_AUTHORITIES_NOT_ACCEPTED",
            detail="planned time and authoritative run/stop timeline are absent",
            authority="not-accepted",
            lineage="planned time+downtime+run/stop timeline",
        ),
        _metric(
            name="full_oee",
            unit="ratio",
            counting_unit="unavailable",
            status="UNSUPPORTED",
            reason_code="FULL_OEE_REQUIRED_COMPONENTS_NOT_ACCEPTED",
            detail="Quality, Performance and Availability authorities are not all accepted",
            authority="not-accepted",
            lineage="accepted Quality+Performance+Availability components",
        ),
    ]


def _identity_failure_metrics(
    *,
    reason_code: str,
    detail: str,
    config_window_state: str,
) -> list[dict[str, object]]:
    unsupported = _unsupported_metrics(config_window_state=config_window_state)
    base = [
        _metric(
            name="accepted_event_count",
            unit="events",
            counting_unit="event-count",
            status="UNAVAILABLE",
            reason_code=reason_code,
            detail=detail,
            authority=SOURCE_AUTHORITY,
            lineage="fact_key",
        ),
        _metric(
            name="observed_accepted_event_rate",
            unit="events_per_second",
            counting_unit="event-count",
            status="UNAVAILABLE",
            reason_code=reason_code,
            detail=detail,
            authority=SOURCE_AUTHORITY,
            lineage="fact_key+calendar_window",
        ),
        unsupported[0],
        _metric(
            name="quality_good_event_count",
            unit="events",
            counting_unit="event-count",
            status="UNAVAILABLE",
            reason_code=reason_code,
            detail=detail,
            authority=SOURCE_AUTHORITY,
            lineage="fact_key",
        ),
        _metric(
            name="quality_nok_event_count",
            unit="events",
            counting_unit="event-count",
            status="UNAVAILABLE",
            reason_code=reason_code,
            detail=detail,
            authority=SOURCE_AUTHORITY,
            lineage="fact_key",
        ),
        _metric(
            name="quality_denominator_event_count",
            unit="events",
            counting_unit="event-count",
            status="UNAVAILABLE",
            reason_code=reason_code,
            detail=detail,
            authority=SOURCE_AUTHORITY,
            lineage="fact_key",
        ),
        _metric(
            name="quality_rate",
            unit="ratio",
            counting_unit="unavailable",
            status="UNAVAILABLE",
            reason_code=reason_code,
            detail=detail,
            authority=SOURCE_AUTHORITY,
            lineage="fact_key",
        ),
    ]
    return base + unsupported[1:]


@router.get("/api/v2/process-metrics", response_model=None)
async def process_metrics(request: Request) -> dict[str, Any] | JSONResponse:
    if await request.body():
        return _invalid_request("request body is not allowed")
    parsed_query = _validated_query(request)
    if isinstance(parsed_query, JSONResponse):
        return parsed_query
    line_id, station_id, start, end = parsed_query
    duration_seconds = (end - start).total_seconds()

    try:
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("BEGIN READ ONLY")
                    cur.execute("SET LOCAL statement_timeout = '3s'")
                    cur.execute("SET LOCAL idle_in_transaction_session_timeout = '3s'")
                    cur.execute(
                        """
                        SELECT line_id, station_id, event_type, production_result,
                               fact_key, content_fingerprint, config_hash, config_version,
                               event_ts, accepted_at, nok_code, nok_origin,
                               nok_detail_code, nok_detail_source_event_id,
                               nok_detail_evidence_fact_key
                        FROM production_accepted_station_event_fact
                        WHERE line_id = %s
                          AND station_id = %s
                          AND event_type = 'station_result'
                          AND event_ts >= %s
                          AND event_ts < %s
                        ORDER BY event_ts ASC, accepted_at ASC, fact_key ASC
                        """,
                        (line_id, station_id, start, end),
                    )
                    rows = cur.fetchall()
                    cur.execute("COMMIT")
                except Exception:
                    cur.execute("ROLLBACK")
                    raise
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "contract_version": CONTRACT_VERSION,
                "scope": _scope(line_id, station_id),
                "window": _window(start, end),
                "status": "UNAVAILABLE",
                "reason": {
                    "code": "ACCEPTED_FACT_SOURCE_UNAVAILABLE",
                    "detail": "accepted fact source unavailable",
                },
                "source": _source(config_window_state="UNRESOLVED"),
                "metrics": [],
            },
        )

    config_pairs = [
        (row.get("config_hash"), row.get("config_version")) for row in rows
    ]
    if not rows or any(
        _missing_text(config_hash) or _missing_text(config_version)
        for config_hash, config_version in config_pairs
    ):
        config_window_state = "UNRESOLVED"
    elif len(set(config_pairs)) > 1:
        config_window_state = "MIXED"
    else:
        config_window_state = "UNRESOLVED"

    seen_fact_keys: set[object] = set()
    identity_failure: tuple[str, str] | None = None
    for row in rows:
        fact_key = row.get("fact_key")
        if fact_key is None or (isinstance(fact_key, str) and not fact_key.strip()):
            identity_failure = (
                "FACT_IDENTITY_MISSING",
                "accepted fact_key is missing",
            )
            break
        if fact_key in seen_fact_keys:
            identity_failure = (
                "FACT_IDENTITY_DUPLICATE_OR_CONFLICT",
                "accepted fact_key is duplicated or conflicting",
            )
            break
        seen_fact_keys.add(fact_key)
        if row.get("production_result") not in ALLOWED_RESULTS:
            identity_failure = (
                "ACCEPTED_FACT_QUERY_FAILED",
                "accepted fact contains an unknown production_result",
            )
            break
    if identity_failure is not None:
        failure_code, failure_detail = identity_failure
        return {
            "contract_version": CONTRACT_VERSION,
            "scope": _scope(line_id, station_id),
            "window": _window(start, end),
            "status": "UNAVAILABLE",
            "reason": {"code": failure_code, "detail": failure_detail},
            "source": _source(config_window_state=config_window_state),
            "metrics": _identity_failure_metrics(
                reason_code=failure_code,
                detail=failure_detail,
                config_window_state=config_window_state,
            ),
        }

    accepted_event_count = len(rows)
    good_count = sum(row.get("production_result") == "ok" for row in rows)
    nok_count = sum(row.get("production_result") == "nok" for row in rows)
    denominator = good_count + nok_count
    missing_nok_detail = any(
        row.get("production_result") == "nok"
        and any(_missing_text(row.get(field)) for field in REQUIRED_NOK_DETAIL_FIELDS)
        for row in rows
    )
    empty = not rows
    count_reason = "EMPTY_ACCEPTED_WINDOW" if empty else "ACCEPTED_FACT_QUERY_OK"
    count_detail = "query succeeded; no accepted facts" if empty else "accepted facts selected"
    unsupported = _unsupported_metrics(config_window_state=config_window_state)
    metrics: list[dict[str, object]] = [
        _metric(
            name="accepted_event_count",
            unit="events",
            counting_unit="event-count",
            status="SUPPORTED",
            reason_code=count_reason,
            detail=count_detail,
            authority=SOURCE_AUTHORITY,
            lineage="fact_key",
            value=accepted_event_count,
        ),
        _metric(
            name="observed_accepted_event_rate",
            unit="events_per_second",
            counting_unit="event-count",
            status="SUPPORTED",
            reason_code="EMPTY_ACCEPTED_WINDOW" if empty else "CALENDAR_WINDOW_EVENT_RATE",
            detail="accepted event count divided by calendar window duration",
            authority=SOURCE_AUTHORITY,
            lineage="fact_key+calendar_window",
            value=accepted_event_count / duration_seconds,
        ),
        unsupported[0],
        _metric(
            name="quality_good_event_count",
            unit="events",
            counting_unit="event-count",
            status="SUPPORTED",
            reason_code="EMPTY_ACCEPTED_WINDOW" if empty else "QUALITY_PREDECESSOR_SEMANTICS",
            detail="accepted station_result production_result=ok",
            authority=SOURCE_AUTHORITY,
            lineage="fact_key",
            value=good_count,
        ),
        _metric(
            name="quality_nok_event_count",
            unit="events",
            counting_unit="event-count",
            status="SUPPORTED",
            reason_code="EMPTY_ACCEPTED_WINDOW" if empty else "QUALITY_PREDECESSOR_SEMANTICS",
            detail="accepted station_result production_result=nok",
            authority=SOURCE_AUTHORITY,
            lineage="fact_key",
            value=nok_count,
        ),
        _metric(
            name="quality_denominator_event_count",
            unit="events",
            counting_unit="event-count",
            status="SUPPORTED",
            reason_code="EMPTY_ACCEPTED_WINDOW" if empty else "QUALITY_PREDECESSOR_SEMANTICS",
            detail="accepted ok+nok events; skip/not_applicable excluded",
            authority=SOURCE_AUTHORITY,
            lineage="fact_key",
            value=denominator,
        ),
    ]
    if denominator == 0:
        metrics.append(
            _metric(
                name="quality_rate",
                unit="ratio",
                counting_unit="unavailable",
                status="UNAVAILABLE",
                reason_code="QUALITY_DENOMINATOR_EMPTY",
                detail="no accepted ok/nok denominator",
                authority=SOURCE_AUTHORITY,
                lineage="fact_key",
            )
        )
    else:
        metrics.append(
            _metric(
                name="quality_rate",
                unit="ratio",
                counting_unit="unavailable",
                status="PARTIAL" if missing_nok_detail else "SUPPORTED",
                reason_code=(
                    "QUALITY_NOK_DETAIL_INCOMPLETE"
                    if missing_nok_detail
                    else "QUALITY_PREDECESSOR_SEMANTICS"
                ),
                detail="NOK detail is incomplete" if missing_nok_detail else "good/denominator",
                authority=SOURCE_AUTHORITY,
                lineage="fact_key",
                value=good_count / denominator,
            )
        )
    metrics.extend(unsupported[1:])
    return {
        "contract_version": CONTRACT_VERSION,
        "scope": _scope(line_id, station_id),
        "window": {
            "from": _iso_z(start),
            "to": _iso_z(end),
            "interval": "[from,to)",
            "duration_seconds": duration_seconds,
        },
        "status": "PARTIAL",
        "reason": {
            "code": "EMPTY_ACCEPTED_WINDOW" if empty else "ACCEPTED_FACT_QUERY_OK",
            "detail": count_detail,
        },
        "source": _source(config_window_state=config_window_state),
        "metrics": metrics,
    }
