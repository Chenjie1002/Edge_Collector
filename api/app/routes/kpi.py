from datetime import datetime, timedelta
from html import escape

from fastapi import APIRouter, Query, Response

from app.db import get_conn

router = APIRouter(prefix="/kpi", tags=["kpi"])


def _parse_ts(value: str) -> datetime:
    text = value.strip()
    if len(text) == 16:
        return datetime.strptime(text, "%Y-%m-%d %H:%M")
    return datetime.fromisoformat(text)


def _resolve_window(
    start: str | None,
    end: str | None,
    date: str | None,
    start_time: str | None,
    end_time: str | None,
    start_custom: str | None,
    end_custom: str | None,
) -> tuple[datetime, datetime]:
    if start and end:
        return _parse_ts(start), _parse_ts(end)
    if not date:
        raise ValueError("date is required when start/end are not provided")
    effective_start = (start_custom or "").strip() or (start_time or "00:00")
    effective_end = (end_custom or "").strip() or (end_time or "23:30")
    start_dt = _parse_ts(f"{date} {effective_start}")
    if effective_end == "24:00":
        end_dt = _parse_ts(f"{date} 00:00") + timedelta(days=1)
    else:
        end_dt = _parse_ts(f"{date} {effective_end}")
    return start_dt, end_dt


def _window_metrics(machine_id: str, start: datetime, end: datetime) -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                WITH windowed AS (
                    SELECT
                        ts,
                        total_count,
                        good_count,
                        ng_count,
                        lag(total_count) OVER (ORDER BY ts) AS prev_total,
                        lag(good_count) OVER (ORDER BY ts) AS prev_good,
                        lag(ng_count) OVER (ORDER BY ts) AS prev_ng
                    FROM production_snapshot
                    WHERE machine_id = %s
                      AND ts >= %s
                      AND ts <= %s
                    ORDER BY ts
                )
                    SELECT
                        COALESCE(sum(greatest(total_count - COALESCE(prev_total, total_count), 0)), 0)::int AS actual_output,
                        COALESCE(sum(greatest(good_count - COALESCE(prev_good, good_count), 0)), 0)::int AS good_count,
                        COALESCE(sum(greatest(ng_count - COALESCE(prev_ng, ng_count), 0)), 0)::int AS ng_count
                    FROM windowed
                """,
                (machine_id, start, end),
            )
            row = cur.fetchone() or {}
    row["total_count"] = int(row.get("good_count") or 0) + int(row.get("ng_count") or 0)
    return row


def _svg_response(svg: str) -> Response:
    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": "no-store, max-age=0"},
    )


@router.get("/{machine_id}/output-card.svg")
def output_card(
    machine_id: str,
    start: str | None = None,
    end: str | None = None,
    date: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    start_custom: str | None = None,
    end_custom: str | None = None,
    cycle_seconds: float = 30.0,
) -> Response:
    start_dt, end_dt = _resolve_window(start, end, date, start_time, end_time, start_custom, end_custom)
    metrics = _window_metrics(machine_id, start_dt, end_dt)
    actual = int(metrics.get("actual_output") or 0)
    theoretical = max(0, round((end_dt - start_dt).total_seconds() / cycle_seconds))
    diff = actual - theoretical
    if theoretical <= 0:
        actual_color = "#73bf69"
    elif actual < theoretical * 0.95:
        actual_color = "#f2495c"
    elif actual > theoretical * 1.05:
        actual_color = "#b877d9"
    else:
        actual_color = "#73bf69"
    diff_text = f"{diff:+d}"
    diff_color = "#f2495c" if diff < 0 else "#73bf69"
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="240" height="100" viewBox="0 0 240 100">
  <text x="42" y="66" text-anchor="middle" font-family="EdgeMESCustom, PingFang SC, Microsoft YaHei, Arial" font-size="35" font-weight="800" fill="{actual_color}">{actual}</text>
  <text x="121" y="66" text-anchor="middle" font-family="EdgeMESCustom, PingFang SC, Microsoft YaHei, Arial" font-size="35" font-weight="800" fill="#5794f2">({theoretical})</text>
  <text x="205" y="63" text-anchor="middle" font-family="EdgeMESCustom, PingFang SC, Microsoft YaHei, Arial" font-size="25" font-weight="700" font-style="italic" fill="{diff_color}">{diff_text}</text>
</svg>
"""
    return _svg_response(svg)


@router.get("/{machine_id}/quality-card.svg")
def quality_card(
    machine_id: str,
    start: str | None = None,
    end: str | None = None,
    date: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    start_custom: str | None = None,
    end_custom: str | None = None,
) -> Response:
    start_dt, end_dt = _resolve_window(start, end, date, start_time, end_time, start_custom, end_custom)
    metrics = _window_metrics(machine_id, start_dt, end_dt)
    good = int(metrics.get("good_count") or 0)
    total = int(metrics.get("total_count") or 0)
    rate = 0.0 if total == 0 else round(good / total * 100, 2)
    color = "#73bf69" if rate >= 98 else "#ff9830" if rate >= 95 else "#f2495c"
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="240" height="100" viewBox="0 0 240 100">
  <rect x="162" y="12" width="62" height="20" rx="10" fill="#1f2937" opacity="0.92"/>
  <text x="193" y="26" text-anchor="middle" font-family="EdgeMESCustom, PingFang SC, Microsoft YaHei, Arial" font-size="9" font-weight="700" fill="#9ec8ff">{good}/{total}</text>
  <text x="18" y="68" font-family="EdgeMESCustom, PingFang SC, Microsoft YaHei, Arial" font-size="43" font-weight="800" fill="{color}">{rate:.2f}%</text>
</svg>
"""
    return _svg_response(svg)


@router.get("/{machine_id}/summary")
def summary(machine_id: str) -> dict:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                WITH windowed AS (
                    SELECT *
                    FROM production_snapshot
                    WHERE machine_id = %s
                      AND ts >= now() - interval '24 hours'
                    ORDER BY ts
                ),
                bounds AS (
                    SELECT
                        (array_agg(total_count ORDER BY ts))[1] AS first_total,
                        (array_agg(total_count ORDER BY ts DESC))[1] AS last_total,
                        (array_agg(good_count ORDER BY ts))[1] AS first_good,
                        (array_agg(good_count ORDER BY ts DESC))[1] AS last_good,
                        (array_agg(ng_count ORDER BY ts))[1] AS first_ng,
                        (array_agg(ng_count ORDER BY ts DESC))[1] AS last_ng,
                        avg(cycle_time_ms) AS avg_cycle_time_ms
                    FROM windowed
                )
                SELECT
                    COALESCE(last_total - first_total, 0) AS output_24h,
                    COALESCE(last_good - first_good, 0) AS good_24h,
                    COALESCE(last_ng - first_ng, 0) AS ng_24h,
                    CASE
                        WHEN COALESCE((last_good - first_good) + (last_ng - first_ng), 0) = 0 THEN 0
                        ELSE round(((last_good - first_good)::numeric / ((last_good - first_good) + (last_ng - first_ng))) * 100, 2)
                    END AS quality_rate,
                    round(avg_cycle_time_ms, 2) AS avg_cycle_time_ms
                FROM bounds
                """,
                (machine_id,),
            )
            return cur.fetchone() or {}
