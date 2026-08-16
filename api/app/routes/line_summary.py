from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from app import db
from app.services.scope_catalog import load_scope_catalog


router = APIRouter(prefix="/api/v2/production", tags=["production"])
QUERY_PARAMS = {"line_id", "start_time", "end_time"}
MAX_WINDOW = timedelta(days=31)
STATEMENT_TIMEOUT = "3s"
IDLE_TRANSACTION_TIMEOUT = "3s"


def _validate_query_params(request: Request) -> None:
    names = set(request.query_params.keys())
    if names - QUERY_PARAMS:
        raise HTTPException(status_code=422, detail="unsupported query parameter")
    if any(len(request.query_params.getlist(name)) != 1 for name in names):
        raise HTTPException(status_code=422, detail="duplicate query parameter")


def _required_text(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise HTTPException(status_code=422, detail=f"invalid {field_name}")
    return value.strip()


def _parse_iso_utc(value: str, field_name: str) -> datetime:
    if "T" not in value:
        raise HTTPException(status_code=422, detail=f"invalid {field_name}")
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=f"invalid {field_name}") from exc
    if parsed.tzinfo is None:
        raise HTTPException(status_code=422, detail=f"invalid {field_name}")
    return parsed.astimezone(timezone.utc)


def _parse_window(start_time: str | None, end_time: str | None) -> tuple[datetime, datetime]:
    start = _parse_iso_utc(_required_text(start_time, "start_time"), "start_time")
    end = _parse_iso_utc(_required_text(end_time, "end_time"), "end_time")
    if start >= end or end - start > MAX_WINDOW:
        raise HTTPException(status_code=422, detail="invalid time window")
    return start, end


def _iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _load_topology(line_id: str) -> tuple[str, str, list[str], str, str | None, str | None]:
    try:
        catalog = load_scope_catalog()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="scope catalog unavailable") from exc
    lines = catalog.get("lines")
    if not isinstance(lines, list):
        raise HTTPException(status_code=503, detail="scope catalog unavailable")
    line = next(
        (candidate for candidate in lines if isinstance(candidate, dict) and candidate.get("line_id") == line_id),
        None,
    )
    if not isinstance(line, dict):
        raise HTTPException(status_code=422, detail="line_id is not available")
    raw_stations = line.get("stations")
    if not isinstance(raw_stations, list) or not raw_stations:
        raise HTTPException(status_code=503, detail="scope catalog unavailable")
    station_ids = [
        str(station["station_id"])
        for station in raw_stations
        if isinstance(station, dict) and isinstance(station.get("station_id"), str)
    ]
    if len(station_ids) != len(raw_stations) or len(set(station_ids)) != len(station_ids):
        raise HTTPException(status_code=503, detail="scope catalog unavailable")
    line_name = str(line.get("name") or line_id)
    authority = catalog.get("authority") if isinstance(catalog.get("authority"), dict) else {}
    mapping_sha256 = authority.get("content_sha256") if isinstance(authority.get("content_sha256"), str) else None
    config_version = authority.get("config_version") if isinstance(authority.get("config_version"), str) else None
    return station_ids[0], station_ids[-1], station_ids, line_name, mapping_sha256, config_version


def _read_cohort_rows(
    *,
    line_id: str,
    terminal_station_id: str,
    start: datetime,
    end: datetime,
) -> list[dict[str, Any]]:
    query = """
        WITH terminal_cohort AS (
            SELECT DISTINCT ON (se.unit_id, se.plc_id, ce.plc_boot_id)
                se.unit_id AS cohort_unit_id,
                se.plc_id AS cohort_plc_id,
                se.line_id AS cohort_line_id,
                ce.plc_boot_id AS cohort_plc_boot_id,
                se.plc_end_time AS cohort_completed_at
            FROM station_event se
            JOIN cycle_event ce ON ce.id = se.cycle_event_id
            WHERE se.line_id = %s
              AND se.station_id = %s
              AND se.unit_id IS NOT NULL
              AND se.plc_end_time IS NOT NULL
              AND se.plc_end_time >= %s
              AND se.plc_end_time < %s
              AND ce.route_state IN ('COMPLETED_OK', 'COMPLETED_NOK')
            ORDER BY se.unit_id, se.plc_id, ce.plc_boot_id, se.plc_end_time DESC, se.id DESC
        ), route_events AS (
            SELECT
                se.id AS station_event_id,
                se.unit_id,
                se.plc_id,
                se.line_id,
                ce.plc_boot_id,
                se.station_id,
                se.route_step,
                se.process_status,
                se.result,
                se.skip_reason,
                se.defect_origin_station,
                se.defect_code,
                ce.route_state,
                ce.cycle_time_ms,
                ce.ack_status,
                ce.dmc,
                ce.child_dmc,
                ce.label_code,
                ce.reject_id,
                se.plc_end_time
            FROM station_event se
            JOIN cycle_event ce ON ce.id = se.cycle_event_id
        )
        SELECT
            c.cohort_unit_id,
            c.cohort_plc_id,
            c.cohort_line_id,
            c.cohort_plc_boot_id,
            c.cohort_completed_at,
            e.station_event_id,
            e.unit_id,
            e.plc_id,
            e.line_id,
            e.plc_boot_id,
            e.station_id,
            e.route_step,
            e.process_status,
            e.result,
            e.skip_reason,
            e.defect_origin_station,
            e.defect_code,
            e.route_state,
            e.cycle_time_ms,
            e.ack_status,
            e.dmc,
            e.child_dmc,
            e.label_code,
            e.reject_id,
            e.plc_end_time
        FROM terminal_cohort c
        LEFT JOIN route_events e
          ON e.unit_id = c.cohort_unit_id
         AND e.plc_id = c.cohort_plc_id
         AND e.line_id = c.cohort_line_id
         AND e.plc_boot_id = c.cohort_plc_boot_id
        ORDER BY c.cohort_completed_at, c.cohort_unit_id, e.route_step, e.station_id, e.station_event_id
    """
    with db.get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("BEGIN READ ONLY")
            cur.execute(f"SET LOCAL statement_timeout = '{STATEMENT_TIMEOUT}'")
            cur.execute(f"SET LOCAL idle_in_transaction_session_timeout = '{IDLE_TRANSACTION_TIMEOUT}'")
            try:
                cur.execute(query, (line_id, terminal_station_id, start, end))
                rows = cur.fetchall()
                cur.execute("COMMIT")
                return [dict(row) for row in rows]
            except Exception:
                cur.execute("ROLLBACK")
                raise


def _upper(value: object) -> str:
    return str(value or "").strip().upper()


def _positive_int(value: object) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _classify_event(row: dict[str, Any], station_id: str) -> tuple[str, str, bool, bool] | str:
    result = _upper(row.get("result"))
    status = _upper(row.get("process_status"))
    skip_reason = _upper(row.get("skip_reason"))
    origin = str(row.get("defect_origin_station") or "").strip()
    defect_code = _positive_int(row.get("defect_code"))
    legacy_skip = False

    if result == "SKIPPED":
        if status != "SKIPPED" or skip_reason != "UPSTREAM_NOK" or not origin or defect_code <= 0:
            return "legacy SKIPPED lacks proven UPSTREAM_NOK/origin/code evidence"
        result = "NOK"
        legacy_skip = True

    if result not in {"OK", "NOK"}:
        return "result must be OK or NOK"
    if status not in {"PROCESSED", "SKIPPED"}:
        return "process_status must be PROCESSED or SKIPPED"
    if result == "OK" and status != "PROCESSED":
        return "OK evidence cannot be SKIPPED"
    if result == "NOK" and defect_code <= 0:
        return "NOK evidence is missing defect_code"
    if result == "NOK" and not origin:
        return "NOK evidence is missing defect_origin_station"
    if result == "NOK" and status == "PROCESSED" and origin != station_id:
        return "new NOK origin does not match station"
    if result == "NOK" and status == "SKIPPED" and skip_reason != "UPSTREAM_NOK":
        return "inherited NOK is missing UPSTREAM_NOK skip_reason"
    return result, status, legacy_skip, origin == station_id and status == "PROCESSED"


def _build_station_summary(
    *,
    rows: list[dict[str, Any]],
    station_id: str,
    cohort_unit_ids: set[str],
) -> tuple[dict[str, object], list[str]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        cohort_unit_id = row.get("cohort_unit_id")
        if cohort_unit_id in cohort_unit_ids and row.get("station_id") == station_id:
            grouped[str(cohort_unit_id)].append(row)

    total = len(cohort_unit_ids)
    ok = nok = processed = skipped = new_nok = 0
    legacy_skip_count = 0
    invalid_count = 0
    duplicate_count = 0
    valid_unit_ids: set[str] = set()
    errors: list[str] = []

    for unit_id in sorted(cohort_unit_ids):
        events = grouped.get(unit_id, [])
        if not events:
            continue
        if len(events) != 1:
            duplicate_count += 1
            continue
        classified = _classify_event(events[0], station_id)
        if isinstance(classified, str):
            invalid_count += 1
            continue
        result, status, legacy_skip, is_new_nok = classified
        valid_unit_ids.add(unit_id)
        ok += result == "OK"
        nok += result == "NOK"
        processed += status == "PROCESSED"
        skipped += status == "SKIPPED"
        new_nok += is_new_nok
        legacy_skip_count += legacy_skip

    missing_count = total - len(valid_unit_ids)
    if missing_count:
        errors.append(f"{missing_count} completed units are missing trusted {station_id} station evidence")
    if duplicate_count:
        errors.append(f"{duplicate_count} completed units have duplicate trusted {station_id} station evidence")
    if invalid_count:
        errors.append(f"{invalid_count} {station_id} station records have invalid result/status semantics")
    if ok + nok != total:
        errors.append(f"{station_id} OK + NOK does not equal cohort total")
    if processed + skipped != total:
        errors.append(f"{station_id} PROCESSED + SKIPPED does not equal cohort total")

    reconciliation_status = "PASS" if not errors else "FAIL"
    return {
        "station_id": station_id,
        "total": total,
        "ok": ok,
        "nok": nok,
        "new_nok": new_nok,
        "skipped": skipped,
        "processed": processed,
        "reconciliation_status": reconciliation_status,
        "evidence_count": len(valid_unit_ids),
        "missing_unit_count": missing_count,
        "duplicate_unit_count": duplicate_count,
        "invalid_record_count": invalid_count,
        "result_compatibility": (
            "legacy_skipped_classified_as_inherited_nok"
            if legacy_skip_count
            else "native_nok_process_status_split"
        ),
    }, errors


def _read_operational_context(line_id: str, station_ids: list[str]) -> dict[str, object]:
    fallback = {
        "active_profile": "UNAVAILABLE",
        "collector_state": "UNAVAILABLE",
        "collector_connected_stations": 0,
        "collector_stations": [],
        "runtime_status": "UNAVAILABLE",
        "runtime_authority": "collector_runtime_status",
    }
    try:
        with db.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("BEGIN READ ONLY")
                cur.execute(f"SET LOCAL statement_timeout = '{STATEMENT_TIMEOUT}'")
                cur.execute(f"SET LOCAL idle_in_transaction_session_timeout = '{IDLE_TRANSACTION_TIMEOUT}'")
                cur.execute(
                    """
                    SELECT DISTINCT ON (station_id)
                           station_id, collector_state, plc_connection_state, station_status, updated_at
                    FROM collector_runtime_status
                    WHERE line_id = %s
                      AND station_id = ANY(%s)
                    ORDER BY station_id, updated_at DESC
                    """,
                    (line_id, station_ids),
                )
                collector_rows = [dict(row) for row in cur.fetchall()]
                cur.execute(
                    """
                    WITH current_boot AS (
                        SELECT plc_boot_id
                        FROM collector_runtime_status
                        WHERE line_id = %s
                          AND station_id = ANY(%s)
                          AND plc_boot_id IS NOT NULL
                          AND plc_boot_id <> ''
                        ORDER BY updated_at DESC
                        LIMIT 1
                    )
                    SELECT vps.profile, vps.captured_at
                    FROM vplc_parameter_snapshot vps
                    JOIN current_boot cb ON cb.plc_boot_id = vps.plc_boot_id
                    ORDER BY vps.captured_at DESC
                    LIMIT 1
                    """,
                    (line_id, station_ids),
                )
                profile_rows = [dict(row) for row in cur.fetchall()]
                cur.execute("COMMIT")
    except Exception:
        return fallback

    stations = []
    connected = 0
    now = datetime.now(timezone.utc)
    freshness_limit = timedelta(seconds=45)
    for row in collector_rows:
        station_id = row.get("station_id")
        if station_id not in station_ids or not row.get("collector_state"):
            continue
        updated_at = row.get("updated_at")
        fresh = isinstance(updated_at, datetime) and updated_at.tzinfo is not None and now - updated_at.astimezone(timezone.utc) <= freshness_limit
        raw_plc_state = str(row.get("plc_connection_state") or "UNKNOWN")
        raw_collector_state = str(row.get("collector_state") or "UNKNOWN")
        plc_state = raw_plc_state if fresh else "STALE"
        collector_station_state = raw_collector_state if fresh else "STALE"
        if fresh and raw_plc_state.upper() in {"CONNECTED", "ONLINE", "OK"}:
            connected += 1
        stations.append(
            {
                "station_id": str(station_id),
                "collector_state": collector_station_state,
                "plc_connection_state": plc_state,
                "station_status": str(row.get("station_status") or "UNKNOWN") if fresh else "STALE",
                "updated_at": updated_at.isoformat() if isinstance(updated_at, datetime) else str(updated_at or ""),
            }
        )
    collector_state = "UNAVAILABLE"
    if stations:
        states = {str(row["collector_state"]).upper() for row in stations}
        collector_state = "RUNNING" if states <= {"RUNNING", "HEALTHY", "OK"} and len(stations) == len(station_ids) else "DEGRADED"
    runtime_status = "UNAVAILABLE"
    if stations:
        running_collector = {"RUNNING", "HEALTHY", "OK"}
        running_plc = {"CONNECTED", "ONLINE", "OK"}
        stopped_collector = {"STOPPED", "OFFLINE"}
        stopped_plc = {"DISCONNECTED", "OFFLINE"}
        complete = len(stations) == len(station_ids)
        if complete and all(
            str(row["collector_state"]).upper() in running_collector
            and str(row["plc_connection_state"]).upper() in running_plc
            for row in stations
        ):
            runtime_status = "RUNNING"
        elif complete and all(
            str(row["collector_state"]).upper() in stopped_collector
            or str(row["plc_connection_state"]).upper() in stopped_plc
            or str(row["station_status"]).upper() in {"STOPPED", "OFFLINE"}
            for row in stations
        ):
            runtime_status = "STOPPED"
        else:
            runtime_status = "DEGRADED"
    profile = "UNAVAILABLE"
    if profile_rows and profile_rows[0].get("profile"):
        profile = str(profile_rows[0]["profile"])
    return {
        "active_profile": profile,
        "collector_state": collector_state,
        "collector_connected_stations": connected,
        "collector_stations": stations,
        "runtime_status": runtime_status,
        "runtime_authority": "collector_runtime_status",
    }


def _valid_route_events(
    rows: list[dict[str, Any]],
    station_ids: list[str],
    cohort_unit_ids: set[str],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        unit_id = row.get("cohort_unit_id")
        station_id = row.get("station_id")
        if unit_id in cohort_unit_ids and station_id in station_ids:
            grouped[(str(unit_id), str(station_id))].append(row)
    valid: list[dict[str, Any]] = []
    for (unit_id, station_id), events in grouped.items():
        if len(events) != 1:
            continue
        classified = _classify_event(events[0], station_id)
        if isinstance(classified, str):
            continue
        event = dict(events[0])
        result, process_status, _legacy_skip, is_new_nok = classified
        event["normalized_result"] = result
        event["normalized_process_status"] = process_status
        event["is_new_nok"] = is_new_nok
        event["cohort_unit_id"] = unit_id
        valid.append(event)
    return valid


def _bucket_start(value: datetime, start: datetime, end: datetime) -> datetime:
    duration = max((end - start).total_seconds(), 1.0)
    width = max(duration / 12.0, 60.0)
    index = max(0, min(11, int((value - start).total_seconds() // width)))
    return start + timedelta(seconds=index * width)


def _average_cycle_seconds(events: list[dict[str, Any]]) -> float | None:
    values = [
        float(row["cycle_time_ms"]) / 1000.0
        for row in events
        if row.get("normalized_process_status") == "PROCESSED"
        and isinstance(row.get("cycle_time_ms"), (int, float))
        and float(row["cycle_time_ms"]) >= 0
    ]
    return round(sum(values) / len(values), 3) if values else None


def _activity_trend(
    events: list[dict[str, Any]],
    *,
    start: datetime,
    end: datetime,
) -> list[dict[str, object]]:
    buckets: dict[datetime, Counter[str]] = defaultdict(Counter)
    for row in events:
        when = row.get("plc_end_time")
        if not isinstance(when, datetime):
            continue
        counter = buckets[_bucket_start(when, start, end)]
        counter["processed"] += row.get("normalized_process_status") == "PROCESSED"
        counter["skipped"] += row.get("normalized_process_status") == "SKIPPED"
        counter["new_nok"] += bool(row.get("is_new_nok"))
    return [
        {
            "bucket_start": _iso_z(bucket),
            "processed": counts["processed"],
            "skipped": counts["skipped"],
            "new_nok": counts["new_nok"],
        }
        for bucket, counts in sorted(buckets.items())
    ]


def _enrich_station_summary(
    station: dict[str, object],
    events: list[dict[str, Any]],
    *,
    start: datetime,
    end: datetime,
) -> dict[str, object]:
    station_id = str(station["station_id"])
    station_events = [row for row in events if row.get("station_id") == station_id]
    processed = int(station["processed"])
    new_nok = int(station["new_nok"])
    code_counts = Counter(
        int(row["defect_code"])
        for row in station_events
        if row.get("is_new_nok") and _positive_int(row.get("defect_code")) > 0
    )
    recent = sorted(
        (row for row in station_events if isinstance(row.get("plc_end_time"), datetime)),
        key=lambda row: row["plc_end_time"],
        reverse=True,
    )[:8]
    return {
        **station,
        "average_cycle_seconds": _average_cycle_seconds(station_events),
        "local_nok_rate": round(new_nok / processed, 6) if processed else None,
        "activity_trend": _activity_trend(station_events, start=start, end=end),
        "nok_codes": [{"code": code, "count": count} for code, count in sorted(code_counts.items())],
        "recent_records": [
            {
                "unit_id": str(row.get("cohort_unit_id") or ""),
                "result": str(row.get("normalized_result") or ""),
                "process_status": str(row.get("normalized_process_status") or ""),
                "completed_at": _iso_z(row["plc_end_time"]),
                "cycle_seconds": round(float(row["cycle_time_ms"]) / 1000.0, 3)
                if isinstance(row.get("cycle_time_ms"), (int, float))
                else None,
                "defect_code": _positive_int(row.get("defect_code")) or None,
            }
            for row in recent
        ],
    }


def _product_sections(
    *,
    rows: list[dict[str, Any]],
    valid_events: list[dict[str, Any]],
    station_ids: list[str],
    terminal_station_id: str,
    stations: list[dict[str, object]],
    cohort_unit_ids: set[str],
    route_status: str,
    start: datetime,
    end: datetime,
) -> tuple[dict[str, object], dict[str, object], dict[str, object], list[dict[str, object]]]:
    terminal_summary = next(station for station in stations if station["station_id"] == terminal_station_id)
    completed = len(cohort_unit_ids)
    terminal_total_reconciles = int(terminal_summary["ok"]) + int(terminal_summary["nok"]) == completed
    final_yield = round(int(terminal_summary["ok"]) / completed, 6) if completed and terminal_total_reconciles else None
    ack_pending = sum(str(row.get("ack_status") or "").upper() not in {"ACK_OK", "ACKED", "OK"} for row in valid_events)
    overview = {
        "completed_units": completed,
        "final_ok": int(terminal_summary["ok"]),
        "final_nok": int(terminal_summary["nok"]),
        "final_yield": final_yield,
        "ack_pending_events": ack_pending,
        "average_cycle_seconds": _average_cycle_seconds(valid_events),
        "route_conservation": route_status,
    }

    production_buckets: dict[datetime, Counter[str]] = defaultdict(Counter)
    terminal_events = [row for row in valid_events if row.get("station_id") == terminal_station_id]
    for row in terminal_events:
        when = row.get("cohort_completed_at") or row.get("plc_end_time")
        if not isinstance(when, datetime):
            continue
        bucket = production_buckets[_bucket_start(when, start, end)]
        bucket["completed"] += 1
        bucket[str(row.get("normalized_result") or "").lower()] += 1
    production_trend = [
        {
            "bucket_start": _iso_z(bucket),
            "completed": counts["completed"],
            "ok": counts["ok"],
            "nok": counts["nok"],
        }
        for bucket, counts in sorted(production_buckets.items())
    ]

    cycle_buckets: dict[tuple[datetime, str], list[float]] = defaultdict(list)
    for row in valid_events:
        when = row.get("plc_end_time")
        station_id = row.get("station_id")
        cycle_time_ms = row.get("cycle_time_ms")
        if row.get("normalized_process_status") != "PROCESSED" or not isinstance(when, datetime) or station_id not in station_ids:
            continue
        if not isinstance(cycle_time_ms, (int, float)) or float(cycle_time_ms) < 0:
            continue
        cycle_buckets[(_bucket_start(when, start, end), str(station_id))].append(float(cycle_time_ms) / 1000.0)
    cycle_trend = [
        {
            "bucket_start": _iso_z(bucket),
            "station_id": station_id,
            "average_cycle_seconds": round(sum(values) / len(values), 3),
            "samples": len(values),
        }
        for (bucket, station_id), values in sorted(cycle_buckets.items())
    ]
    trends = {"production": production_trend, "cycle_time": cycle_trend}

    code_counts = Counter(
        _positive_int(row.get("defect_code"))
        for row in valid_events
        if row.get("is_new_nok") and _positive_int(row.get("defect_code")) > 0
    )
    quality = {
        "nok_accumulation": [{"station_id": str(station["station_id"]), "count": int(station["nok"])} for station in stations],
        "new_nok_by_station": [{"station_id": str(station["station_id"]), "count": int(station["new_nok"])} for station in stations],
        "nok_code_distribution": [{"code": code, "count": count} for code, count in sorted(code_counts.items())],
    }

    recent_terminal = sorted(
        (row for row in terminal_events if isinstance(row.get("cohort_completed_at"), datetime)),
        key=lambda row: row["cohort_completed_at"],
        reverse=True,
    )[:12]
    recent_completed = [
        {
            "unit_id": str(row.get("cohort_unit_id") or ""),
            "result": str(row.get("normalized_result") or ""),
            "completed_at": _iso_z(row["cohort_completed_at"]),
            "defect_origin_station": str(row.get("defect_origin_station") or "") or None,
            "defect_code": _positive_int(row.get("defect_code")) or None,
            "label_code": str(row.get("label_code") or "") or None,
            "reject_id": str(row.get("reject_id") or "") or None,
        }
        for row in recent_terminal
    ]
    return overview, trends, quality, recent_completed


@router.get("/line-summary")
def line_summary(request: Request) -> dict[str, object]:
    _validate_query_params(request)
    line_id = _required_text(request.query_params.get("line_id"), "line_id")
    start, end = _parse_window(
        request.query_params.get("start_time"),
        request.query_params.get("end_time"),
    )
    entry_station_id, terminal_station_id, station_ids, line_name, mapping_sha256, config_version = _load_topology(line_id)
    operational = _read_operational_context(line_id, station_ids)
    try:
        rows = _read_cohort_rows(
            line_id=line_id,
            terminal_station_id=terminal_station_id,
            start=start,
            end=end,
        )
    except Exception as exc:
        raise HTTPException(status_code=503, detail="line summary source unavailable") from exc

    cohort_unit_ids = {
        str(row["cohort_unit_id"])
        for row in rows
        if row.get("cohort_unit_id") is not None
    }
    stations: list[dict[str, object]] = []
    reconciliation_errors: list[str] = []
    for station_id in station_ids:
        summary, errors = _build_station_summary(
            rows=rows,
            station_id=station_id,
            cohort_unit_ids=cohort_unit_ids,
        )
        stations.append(summary)
        reconciliation_errors.extend(errors)

    route_status = "PASS" if not reconciliation_errors else "FAIL"
    valid_events = _valid_route_events(rows, station_ids, cohort_unit_ids)
    stations = [
        _enrich_station_summary(station, valid_events, start=start, end=end)
        for station in stations
    ]
    overview, trends, quality, recent_completed = _product_sections(
        rows=rows,
        valid_events=valid_events,
        station_ids=station_ids,
        terminal_station_id=terminal_station_id,
        stations=stations,
        cohort_unit_ids=cohort_unit_ids,
        route_status=route_status,
        start=start,
        end=end,
    )
    return {
        "contract_version": "production-line-summary/v1",
        "scope": {
            "line_id": line_id,
            "start_time": _iso_z(start),
            "end_time": _iso_z(end),
            "cohort_basis": "terminal_completed",
        },
        "line": {
            "line_id": line_id,
            "name": line_name,
            "station_count": len(station_ids),
            "route": station_ids,
            "entry_station_id": entry_station_id,
            "terminal_station_id": terminal_station_id,
            "active_profile": operational["active_profile"],
            "collector_state": operational["collector_state"],
            "collector_connected_stations": operational["collector_connected_stations"],
            "runtime_status": operational["runtime_status"],
            "runtime_authority": operational["runtime_authority"],
            "mapping_content_sha256": mapping_sha256,
            "config_version": config_version,
        },
        "topology": {
            "entry_station_id": entry_station_id,
            "terminal_station_id": terminal_station_id,
            "stations": station_ids,
        },
        "cohort": {
            "unit_count": len(cohort_unit_ids),
            "reconciliation_status": route_status,
            "errors": reconciliation_errors,
        },
        "overview": overview,
        "trends": trends,
        "quality": quality,
        "collector_runtime": operational["collector_stations"],
        "recent_completed_units": recent_completed,
        "stations": stations,
    }
