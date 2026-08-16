from __future__ import annotations

from dataclasses import dataclass
import os
import re
from html import escape
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse

from common.runtime_mapping import EffectiveMappingUnavailable, read_effective_mapping
from app.db import get_conn


router = APIRouter(prefix="/trace", tags=["trace"])


@dataclass(frozen=True)
class TraceTopology:
    station_ids: tuple[str, ...]
    entry_station_id: str
    terminal_station_id: str
    edges: tuple[tuple[str, str], ...]

    @property
    def predecessor(self) -> dict[str, str]:
        return {to_station: from_station for from_station, to_station in self.edges}


def _trace_mapping_path() -> Path:
    configured = os.environ.get("EDGE_MES_MAPPING_PATH")
    if configured:
        return Path(configured)
    container_path = Path("/app/config/mapping.yaml")
    if container_path.is_file():
        return container_path
    return Path(__file__).resolve().parents[3] / "config" / "mapping.yaml"


def _load_trace_topology() -> TraceTopology:
    try:
        root = read_effective_mapping(_trace_mapping_path()).root
    except EffectiveMappingUnavailable as exc:
        raise HTTPException(status_code=503, detail="active trace topology unavailable") from exc
    raw_stations = root.get("stations")
    if not isinstance(raw_stations, list):
        raise HTTPException(status_code=503, detail="active trace topology has no stations")
    ordered_stations = sorted(
        (
            (index, station)
            for index, station in enumerate(raw_stations)
            if isinstance(station, dict) and station.get("station_enabled", True) is not False
        ),
        key=lambda item: (int(item[1].get("station_order", item[0] + 1)), item[0]),
    )
    station_ids = tuple(str(station["station_id"]) for _index, station in ordered_stations)
    if not station_ids or len(set(station_ids)) != len(station_ids):
        raise HTTPException(status_code=503, detail="active trace topology station identity is invalid")
    route_raw = root.get("route_graph")
    topology_raw = root.get("topology") if isinstance(root.get("topology"), dict) else {}
    edges_raw = route_raw.get("edges", []) if isinstance(route_raw, dict) else (route_raw or [])
    edges = tuple(
        (str(edge["from_station_id"]), str(edge["to_station_id"]))
        for edge in edges_raw
        if isinstance(edge, dict)
    )
    station_set = set(station_ids)
    if any(left not in station_set or right not in station_set for left, right in edges):
        raise HTTPException(status_code=503, detail="active trace topology edge identity is invalid")
    explicit_entry = root.get("entry_station_id") or topology_raw.get("entry_station_id")
    explicit_terminal = root.get("terminal_station_id") or topology_raw.get("terminal_station_id")
    if isinstance(route_raw, dict):
        explicit_entry = explicit_entry or route_raw.get("entry_station_id")
        explicit_terminal = explicit_terminal or route_raw.get("terminal_station_id")
    predecessor = {right: left for left, right in edges}
    successor = {left: right for left, right in edges}
    entry = str(explicit_entry) if explicit_entry else next(
        (station_id for station_id in station_ids if station_id not in predecessor),
        station_ids[0],
    )
    terminal = str(explicit_terminal) if explicit_terminal else next(
        (station_id for station_id in reversed(station_ids) if station_id not in successor),
        station_ids[-1],
    )
    if entry not in station_set or terminal not in station_set:
        raise HTTPException(status_code=503, detail="active trace topology entry/terminal is invalid")
    return TraceTopology(
        station_ids=station_ids,
        entry_station_id=entry,
        terminal_station_id=terminal,
        edges=edges,
    )


def _serial_from_text(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"(\d+)$", value.strip())
    return int(match.group(1)) if match else None


def _serial_from_event(row: dict[str, Any] | None) -> int | None:
    if not row:
        return None
    for key in ("label_code", "dmc", "child_dmc", "trace_key"):
        serial = _serial_from_text(row.get(key))
        if serial is not None:
            return serial
    try:
        payload = row.get("payload") or {}
        if isinstance(payload, dict) and payload.get("serial_no"):
            return int(payload["serial_no"])
    except Exception:
        return None
    return None


def _station_payload_summary(row: dict[str, Any]) -> dict[str, Any]:
    payload = row.get("payload") or {}
    if not isinstance(payload, dict):
        return {}
    return {key: payload[key] for key in sorted(payload)}


def _format_event(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if not row:
        return None
    return {
        "id": row["id"],
        "plc_id": row.get("plc_id"),
        "line_id": row.get("line_id"),
        "station_id": row["station_id"],
        "plc_boot_id": row.get("plc_boot_id"),
        "cycle_counter": row["cycle_counter"],
        "trace_key": row.get("trace_key"),
        "dmc": row.get("dmc"),
        "child_dmc": row.get("child_dmc"),
        "label_code": row.get("label_code"),
        "unit_id": row.get("unit_id"),
        "route_step": row.get("route_step"),
        "route_state": row.get("route_state"),
        "process_status": row.get("process_status"),
        "skip_reason": row.get("skip_reason"),
        "defect_origin_station": row.get("defect_origin_station"),
        "defect_code": row.get("defect_code"),
        "final_label_code": row.get("final_label_code"),
        "reject_id": row.get("reject_id"),
        "plc_start_time": row["plc_start_time"].isoformat() if row.get("plc_start_time") else None,
        "plc_end_time": row["plc_end_time"].isoformat() if row.get("plc_end_time") else None,
        "cycle_time_ms": row.get("cycle_time_ms"),
        "result": row.get("result"),
        "nok_codes": row.get("nok_codes") or [],
        "ack_status": row.get("ack_status"),
        "payload": _station_payload_summary(row),
    }


def _empty_trace(query: str, serial_no: int | None) -> dict[str, Any]:
    topology = _load_trace_topology()
    return {
        "query": query,
        "serial_no": serial_no,
        "found": False,
        "stations": {station_id: None for station_id in topology.station_ids},
        "events": [],
    }


def _trace_by_unit(
    query: str,
    unit_id: str,
    serial_no: int | None = None,
    *,
    plc_id: str | None = None,
    line_id: str | None = None,
    plc_boot_id: str | None = None,
) -> dict[str, Any]:
    topology = _load_trace_topology()
    scope_sql, scope_params = _identity_scope_sql(
        plc_id=plc_id,
        line_id=line_id,
        plc_boot_id=plc_boot_id,
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT *
                FROM cycle_event
                WHERE unit_id = %s
                {scope_sql}
                ORDER BY route_step NULLS LAST, plc_end_time NULLS LAST, id
                """,
                (unit_id, *scope_params),
            )
            rows = cur.fetchall()

    stations: dict[str, dict[str, Any] | None] = {
        station_id: None for station_id in topology.station_ids
    }
    for row in rows:
        if row["station_id"] in stations:
            stations[row["station_id"]] = _format_event(row)
    return {
        "query": query,
        "unit_id": unit_id,
        "serial_no": serial_no,
        "found": any(stations.values()),
        "stations": stations,
        "events": [stations[station_id] for station_id in topology.station_ids if stations[station_id]],
    }


def _trace_by_serial(
    query: str,
    serial_no: int,
    *,
    plc_id: str | None = None,
    line_id: str | None = None,
    plc_boot_id: str | None = None,
) -> dict[str, Any]:
    topology = _load_trace_topology()
    serial6 = f"{serial_no:06d}"
    candidates = (f"SUB-{serial6}", f"ASM-{serial6}")
    scope_sql, scope_params = _identity_scope_sql(
        plc_id=plc_id,
        line_id=line_id,
        plc_boot_id=plc_boot_id,
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT *
                FROM cycle_event
                WHERE (
                      dmc = ANY(%s)
                   OR child_dmc = ANY(%s)
                   OR label_code = ANY(%s)
                   OR final_product_id = ANY(%s)
                   OR part_id = ANY(%s)
                   OR trace_key = ANY(%s)
                   OR payload ->> 'upstream_child_dmc' = ANY(%s)
                   OR payload ->> 'upstream_ws02_dmc' = ANY(%s)
                   OR payload ->> 'serial_no' = %s
                )
                {scope_sql}
                ORDER BY plc_end_time NULLS LAST, id
                """,
                (
                    list(candidates),
                    list(candidates),
                    list(candidates),
                    list(candidates),
                    list(candidates),
                    list(candidates),
                    list(candidates),
                    list(candidates),
                    str(serial_no),
                    *scope_params,
                ),
            )
            rows = cur.fetchall()

    stations: dict[str, dict[str, Any] | None] = {
        station_id: None for station_id in topology.station_ids
    }
    for row in rows:
        if row["station_id"] in stations:
            stations[row["station_id"]] = _format_event(row)
    _fill_upstream_by_identity(
        stations,
        topology,
        plc_id=plc_id,
        line_id=line_id,
        plc_boot_id=plc_boot_id,
    )
    return {
        "query": query,
        "serial_no": serial_no,
        "found": any(stations.values()),
        "stations": stations,
        "events": [stations[station_id] for station_id in topology.station_ids if stations[station_id]],
    }


def _fill_upstream_by_identity(
    stations: dict[str, dict[str, Any] | None],
    topology: TraceTopology,
    *,
    plc_id: str | None = None,
    line_id: str | None = None,
    plc_boot_id: str | None = None,
) -> None:
    for station_id in reversed(topology.station_ids):
        row = stations.get(station_id)
        predecessor = topology.predecessor.get(station_id)
        if not row or not predecessor or stations.get(predecessor):
            continue
        payload = row.get("payload") or {}
        explicit_dmc = (
            payload.get(f"upstream_{predecessor.lower()}_dmc")
            or payload.get("upstream_child_dmc")
            or row.get("child_dmc")
            or row.get("dmc")
        ) if isinstance(payload, dict) else (row.get("child_dmc") or row.get("dmc"))
        stations[predecessor] = _find_upstream_event(
            predecessor,
            explicit_dmc,
            plc_id=plc_id,
            line_id=line_id,
            plc_boot_id=plc_boot_id,
        )


def _find_upstream_event(
    station_id: str,
    child_dmc: str | None,
    *,
    plc_id: str | None = None,
    line_id: str | None = None,
    plc_boot_id: str | None = None,
) -> dict[str, Any] | None:
    if not child_dmc:
        return None
    scope_sql, scope_params = _identity_scope_sql(
        plc_id=plc_id,
        line_id=line_id,
        plc_boot_id=plc_boot_id,
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            if child_dmc:
                cur.execute(
                    f"""
                    SELECT *
                    FROM cycle_event
                    WHERE station_id = %s
                      AND (dmc = %s OR child_dmc = %s OR part_id = %s OR trace_key = %s)
                    {scope_sql}
                    ORDER BY plc_end_time DESC NULLS LAST, id DESC
                    LIMIT 1
                    """,
                    (
                        station_id,
                        child_dmc,
                        child_dmc,
                        child_dmc,
                        child_dmc,
                        *scope_params,
                    ),
                )
                row = cur.fetchone()
                if row:
                    return _format_event(row)
                return None
    return None


def _identity_scope_sql(
    *,
    plc_id: str | None,
    line_id: str | None,
    plc_boot_id: str | None,
) -> tuple[str, list[str]]:
    clauses: list[str] = []
    params: list[str] = []
    for column, value in (
        ("plc_id", plc_id),
        ("line_id", line_id),
        ("plc_boot_id", plc_boot_id),
    ):
        if value:
            clauses.append(f"AND {column} = %s")
            params.append(value)
    return "\n".join(clauses), params


def _current_cycle_identity(
    station_id: str,
    *,
    plc_id: str | None,
    line_id: str | None,
) -> dict[str, Any]:
    clauses = [
        "station_id = %s",
        "plc_boot_id IS NOT NULL",
        "plc_boot_id <> ''",
    ]
    params: list[str] = [station_id]
    if plc_id:
        clauses.append("plc_id = %s")
        params.append(plc_id)
    if line_id:
        clauses.append("line_id = %s")
        params.append(line_id)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT plc_id, line_id, station_id, plc_boot_id
                FROM collector_runtime_status
                WHERE {' AND '.join(clauses)}
                ORDER BY updated_at DESC
                LIMIT 1
                """,
                tuple(params),
            )
            row = cur.fetchone()
    if not row:
        raise HTTPException(
            status_code=404,
            detail="current PLC boot identity not found",
        )
    return row


def _find_cycle_event(
    *,
    station_id: str,
    cycle_counter: int,
    plc_boot_id: str,
    plc_id: str | None,
    line_id: str | None,
) -> dict[str, Any] | None:
    clauses = [
        "station_id = %s",
        "cycle_counter = %s",
        "plc_boot_id = %s",
    ]
    params: list[Any] = [station_id, cycle_counter, plc_boot_id]
    if plc_id:
        clauses.append("plc_id = %s")
        params.append(plc_id)
    if line_id:
        clauses.append("line_id = %s")
        params.append(line_id)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT *
                FROM cycle_event
                WHERE {' AND '.join(clauses)}
                ORDER BY id DESC
                LIMIT 1
                """,
                tuple(params),
            )
            return cur.fetchone()


def _find_seed_event(query: str) -> dict[str, Any] | None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM cycle_event
                WHERE label_code = %s
                   OR dmc = %s
                   OR child_dmc = %s
                   OR trace_key = %s
                   OR unit_id = %s
                   OR final_label_code = %s
                   OR reject_id = %s
                ORDER BY id DESC
                LIMIT 1
                """,
                (query, query, query, query, query, query, query),
            )
            return cur.fetchone()


@router.get("", response_class=HTMLResponse)
def trace_page() -> str:
    return TRACE_HTML


@router.get("/api")
def trace_query(q: str = Query(..., min_length=1, description="label_code, DMC, or trace key")) -> dict[str, Any]:
    query = q.strip()
    seed = _find_seed_event(query)
    serial_no = _serial_from_event(seed) or _serial_from_text(query)
    if seed and seed.get("unit_id"):
        return _trace_by_unit(query, str(seed["unit_id"]), serial_no)
    if serial_no is None:
        return _empty_trace(query, None)
    return _trace_by_serial(query, serial_no)


@router.get("/api/by-cycle")
def trace_by_cycle(
    station_id: str,
    cycle_counter: int,
    plc_boot_id: str | None = Query(default=None),
    plc_id: str | None = Query(default=None),
    line_id: str | None = Query(default=None),
) -> dict[str, Any]:
    station = station_id.upper()
    if plc_boot_id is None:
        current_identity = _current_cycle_identity(
            station,
            plc_id=plc_id,
            line_id=line_id,
        )
        plc_boot_id = str(current_identity["plc_boot_id"])
        plc_id = str(current_identity["plc_id"])
        line_id = str(current_identity["line_id"])

    row = _find_cycle_event(
        station_id=station,
        cycle_counter=cycle_counter,
        plc_boot_id=plc_boot_id,
        plc_id=plc_id,
        line_id=line_id,
    )
    if not row:
        raise HTTPException(status_code=404, detail="cycle event not found")
    serial_no = _serial_from_event(row)
    if row.get("unit_id"):
        return _trace_by_unit(
            f"{station}:{cycle_counter}",
            str(row["unit_id"]),
            serial_no,
            plc_id=str(row["plc_id"]),
            line_id=str(row["line_id"]),
            plc_boot_id=str(row["plc_boot_id"]),
        )
    if serial_no is None:
        return _empty_trace(f"{station}:{cycle_counter}", None)
    return _trace_by_serial(
        f"{station}:{cycle_counter}",
        serial_no,
        plc_id=str(row["plc_id"]),
        line_id=str(row["line_id"]),
        plc_boot_id=str(row["plc_boot_id"]),
    )


@router.get("/api/recent")
def recent_traces(
    limit: int = Query(default=20, ge=1, le=100),
    status: str | None = Query(default=None, description="completed_ok, in_progress, nok"),
) -> list[dict[str, Any]]:
    if status == "completed_ok":
        where = "pu.current_state = 'COMPLETED_OK'"
    elif status == "nok":
        where = "pu.current_state = 'COMPLETED_NOK'"
    elif status == "in_progress":
        where = "pu.current_state IN ('CREATED', 'WAITING_NEXT_STATION', 'BYPASSING')"
    else:
        where = "TRUE"
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT
                       pu.unit_id,
                       COALESCE(latest_event.station_id, pu.current_station_id) AS station_id,
                       latest_event.cycle_counter AS cycle_counter,
                       latest_event.cycle_counter AS station_cycle_counter,
                       pu.current_route_step AS route_step,
                       pu.plc_id,
                       pu.line_id,
                       latest_event.plc_boot_id,
                       pu.child_dmc AS dmc,
                       pu.child_dmc,
                       pu.final_label_code AS label_code,
                       pu.unit_id AS part_id,
                       pu.final_result AS result,
                       ARRAY[]::INTEGER[] AS nok_codes,
                       pu.current_state AS ack_status,
                       pu.updated_at AS plc_end_time,
                       pu.reject_id,
                       pu.disposition,
                       pu.defect_origin_station,
                       pu.defect_code
                FROM production_unit pu
                LEFT JOIN LATERAL (
                    SELECT
                           ce.station_id,
                           ce.plc_boot_id,
                           ce.cycle_counter
                    FROM cycle_event ce
                    WHERE ce.unit_id = pu.unit_id
                      AND ce.plc_id = pu.plc_id
                      AND ce.line_id = pu.line_id
                    ORDER BY
                           ce.route_step DESC NULLS LAST,
                           ce.plc_end_time DESC NULLS LAST,
                           ce.id DESC
                    LIMIT 1
                ) latest_event ON TRUE
                WHERE {where}
                ORDER BY pu.updated_at DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
    return [
        {
            **row,
            "plc_end_time": row["plc_end_time"].isoformat() if row.get("plc_end_time") else None,
        }
        for row in rows
    ]


TRACE_HTML = f"""
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>动态生产追溯</title>
  <style>
    :root {{
      --bg: #f4f6f8; --surface: #fff; --line: #d8dee7; --text: #17202c;
      --muted: #667085; --blue: #1959c8; --green: #16815a; --red: #bd2b26;
      font-family: Inter, "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--bg); color: var(--text); font-size: 14px; }}
    header {{ height: 64px; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; background: var(--surface); border-bottom: 1px solid var(--line); }}
    h1 {{ margin: 0; font-size: 19px; }}
    main {{ width: min(1240px, calc(100vw - 28px)); margin: 18px auto 28px; display: grid; gap: 14px; }}
    .panel {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 16px; }}
    .search {{ display: grid; grid-template-columns: 1fr auto auto; gap: 10px; }}
    input, select, button {{ height: 38px; border: 1px solid var(--line); border-radius: 6px; padding: 0 10px; font: inherit; background: #fff; }}
    button {{ cursor: pointer; }}
    button.primary {{ background: var(--blue); color: white; border-color: var(--blue); }}
    .timeline {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }}
    .station {{ border: 1px solid var(--line); border-radius: 8px; padding: 14px; min-height: 260px; }}
    .station h2 {{ margin: 0 0 10px; font-size: 16px; }}
    .badge {{ display: inline-flex; align-items: center; justify-content: center; min-width: 54px; height: 24px; border-radius: 999px; font-size: 12px; font-weight: 750; }}
    .ok {{ background: #e9f8f1; color: var(--green); }}
    .nok {{ background: #fff0ef; color: var(--red); }}
    .muted {{ color: var(--muted); }}
    dl {{ display: grid; grid-template-columns: 120px 1fr; gap: 7px 10px; margin: 0; }}
    dt {{ color: var(--muted); }}
    dd {{ margin: 0; overflow-wrap: anywhere; }}
    pre {{ margin: 10px 0 0; background: #111827; color: #e5e7eb; padding: 10px; border-radius: 8px; overflow: auto; max-height: 180px; font-size: 12px; }}
    .recent-head {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }}
    .recent-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }}
    .recent-card {{ border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }}
    .recent-card h3 {{ margin: 0; padding: 10px 12px; font-size: 14px; background: #fbfcfd; border-bottom: 1px solid var(--line); }}
    .recent-list {{ max-height: 360px; overflow: auto; }}
    .recent-item {{ width: 100%; height: auto; display: grid; grid-template-columns: 1fr auto; gap: 4px 10px; padding: 9px 12px; border: 0; border-bottom: 1px solid var(--line); border-radius: 0; text-align: left; }}
    .recent-item:hover {{ background: #f3f6fb; }}
    .recent-title {{ font-weight: 750; }}
    .recent-meta {{ color: var(--muted); font-size: 12px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 9px 8px; border-bottom: 1px solid var(--line); text-align: left; }}
    th {{ color: var(--muted); font-size: 12px; background: #fbfcfd; }}
    @media (max-width: 900px) {{ .timeline, .search, .recent-grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>动态生产追溯</h1>
    <a href="/docs" target="_blank">API Docs</a>
  </header>
  <main>
    <section class="panel">
      <div class="search">
        <input id="query" placeholder="输入 ASM-000025、SUB-000025、NG-000025、UID 或序号 25">
        <button class="primary" onclick="searchTrace()">查询</button>
        <button onclick="loadRecent()">最近记录</button>
      </div>
      <p class="muted" id="summary">输入最终 label_code 或子件 DMC 后查询。</p>
    </section>
    <section class="timeline" id="timeline"></section>
    <section class="panel">
      <div class="recent-head">
        <h2 style="margin:0;font-size:16px">最近记录</h2>
        <select id="recentLimit" onchange="loadRecent()">
          <option value="10">最近 10 条</option>
          <option value="20" selected>最近 20 条</option>
          <option value="30">最近 30 条</option>
        </select>
      </div>
      <div class="recent-grid">
        <article class="recent-card">
          <h3>已完成合格</h3>
          <div class="recent-list" id="recentOk"></div>
        </article>
        <article class="recent-card">
          <h3>进行中</h3>
          <div class="recent-list" id="recentProgress"></div>
        </article>
        <article class="recent-card">
          <h3>不合格</h3>
          <div class="recent-list" id="recentNok"></div>
        </article>
      </div>
    </section>
  </main>
  <script>
    const stations = [];
    function setStations(data) {{
      stations.splice(0, stations.length, ...Object.keys(data.stations || {{}}));
    }}
    function esc(v) {{ return String(v ?? "").replace(/[&<>"']/g, s => ({{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","'":"&#39;"}}[s])); }}
    function badge(result) {{ const cls = result === "NOK" ? "nok" : "ok"; return `<span class="badge ${{cls}}">${{esc(result || "-")}}</span>`; }}
    function stationCard(id, row) {{
      if (!row) return `<article class="station"><h2>${{id}}</h2><p class="muted">无记录</p></article>`;
      return `<article class="station">
        <h2>${{id}} ${{badge(row.result)}}</h2>
        <dl>
          <dt>UID</dt><dd>${{esc(row.unit_id || "-")}}</dd>
          <dt>Counter</dt><dd>${{esc(row.cycle_counter)}}</dd>
          <dt>DMC</dt><dd>${{esc(row.dmc || row.child_dmc || "-")}}</dd>
          <dt>子件 DMC</dt><dd>${{esc(row.child_dmc || row.payload?.upstream_child_dmc || "-")}}</dd>
          <dt>Label</dt><dd>${{esc(row.label_code || row.final_label_code || "-")}}</dd>
          <dt>Reject</dt><dd>${{esc(row.reject_id || "-")}}</dd>
          <dt>Process</dt><dd>${{esc(row.process_status || "-")}}</dd>
          <dt>Skip</dt><dd>${{esc(row.skip_reason || "-")}}</dd>
          <dt>缺陷源站</dt><dd>${{esc(row.defect_origin_station || "-")}}</dd>
          <dt>缺陷代码</dt><dd>${{esc(row.defect_code || "-")}}</dd>
          <dt>开始</dt><dd>${{esc(row.plc_start_time || "-")}}</dd>
          <dt>结束</dt><dd>${{esc(row.plc_end_time || "-")}}</dd>
          <dt>Cycle Time</dt><dd>${{row.cycle_time_ms ? (row.cycle_time_ms / 1000).toFixed(2) + " s" : "-"}}</dd>
          <dt>NOK Code</dt><dd>${{esc((row.nok_codes || []).join(", ") || "-")}}</dd>
          <dt>ACK</dt><dd>${{esc(row.ack_status || "-")}}</dd>
        </dl>
        <pre>${{esc(JSON.stringify(row.payload || {{}}, null, 2))}}</pre>
      </article>`;
    }}
    async function searchTrace() {{
      const q = document.getElementById("query").value.trim();
      if (!q) return;
      const res = await fetch(`/trace/api?q=${{encodeURIComponent(q)}}`);
      const data = await res.json();
      setStations(data);
      document.getElementById("summary").textContent = data.found ? `序号 ${{data.serial_no}}，找到 ${{data.events.length}} 条工站事件。` : "没有找到匹配追溯记录。";
      document.getElementById("timeline").innerHTML = stations.map(id => stationCard(id, data.stations[id])).join("");
    }}
    function traceId(r) {{ return r.label_code || r.reject_id || r.unit_id || r.child_dmc || r.dmc || r.part_id || r.cycle_counter; }}
    function rowButton(r) {{
      const q = esc(traceId(r));
      const stationCounter = r.station_cycle_counter ?? r.cycle_counter ?? "-";
      const routeStep = r.route_step ?? "-";
      return `<button class="recent-item" onclick="pick('${{q}}')">
        <span class="recent-title">${{q}}</span><span>${{badge(r.result)}}</span>
        <span class="recent-meta">${{esc(r.plc_end_time || "-")}}</span>
        <span class="recent-meta">${{esc(r.station_id)}} · #${{esc(stationCounter)}} · Step ${{esc(routeStep)}}</span>
      </button>`;
    }}
    async function loadRecentGroup(status, targetId) {{
      const limit = document.getElementById("recentLimit").value;
      const rows = await (await fetch(`/trace/api/recent?status=${{status}}&limit=${{limit}}`)).json();
      document.getElementById(targetId).innerHTML = rows.length ? rows.map(rowButton).join("") : `<p class="muted" style="padding:12px">暂无记录</p>`;
    }}
    async function loadRecent() {{
      await Promise.all([
        loadRecentGroup("completed_ok", "recentOk"),
        loadRecentGroup("in_progress", "recentProgress"),
        loadRecentGroup("nok", "recentNok"),
      ]);
    }}
    function pick(q) {{ document.getElementById("query").value = q; searchTrace(); }}
    const initial = new URLSearchParams(window.location.search).get("q");
    if (initial) {{
      document.getElementById("query").value = initial;
      searchTrace();
    }}
    loadRecent();
  </script>
</body>
</html>
"""
