from __future__ import annotations

from collections import defaultdict
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


def _load_topology(line_id: str) -> tuple[str, str, list[str]]:
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
    return station_ids[0], station_ids[-1], station_ids


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


@router.get("/line-summary")
def line_summary(request: Request) -> dict[str, object]:
    _validate_query_params(request)
    line_id = _required_text(request.query_params.get("line_id"), "line_id")
    start, end = _parse_window(
        request.query_params.get("start_time"),
        request.query_params.get("end_time"),
    )
    entry_station_id, terminal_station_id, station_ids = _load_topology(line_id)
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
    return {
        "contract_version": "production-line-summary/v1",
        "scope": {
            "line_id": line_id,
            "start_time": _iso_z(start),
            "end_time": _iso_z(end),
            "cohort_basis": "terminal_completed",
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
        "stations": stations,
    }
