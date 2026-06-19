#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_HOST = "10.0.0.217"
STATION_CODES = {"WS01": 10001, "WS02": 20001, "WS03": 30001}


def normalize_int_array(value: Any) -> list[int]:
    if value is None:
        return []
    if isinstance(value, list):
        return [int(item) for item in value]
    text = str(value).strip()
    if text in {"", "{}", "[]"}:
        return []
    if text.startswith("{") and text.endswith("}"):
        text = f"[{text[1:-1]}]"
    parsed = json.loads(text)
    return [int(item) for item in parsed]


def raw_nok_codes(row: dict[str, Any]) -> list[int]:
    count = int(row.get("nok_code_count") or 0)
    values = [
        int(row.get("nok_codes_1") or 0),
        int(row.get("nok_codes_2") or 0),
        int(row.get("nok_codes_3") or 0),
    ]
    return [value for value in values[:count] if value]


def http_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 15,
) -> Any:
    data = json.dumps(payload).encode() if payload is not None else None
    request_headers = {"Content-Type": "application/json"}
    request_headers.update(headers or {})
    request = urllib.request.Request(url, data=data, method=method, headers=request_headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise RuntimeError(f"{method} {url} failed: HTTP {exc.code}: {body}") from exc


class AcceptanceClient:
    def __init__(self, host: str) -> None:
        self.vplc = f"http://{host}:8200"
        self.api = f"http://{host}:8000"
        self.grafana = f"http://{host}:3000"

    def state(self) -> dict[str, Any]:
        return http_json(f"{self.vplc}/vplc/state")

    def trace(self, query: str) -> dict[str, Any]:
        return http_json(f"{self.api}/trace/api?q={urllib.parse.quote(query)}")

    def trace_by_cycle(
        self,
        station: str,
        counter: int,
        *,
        plc_boot_id: str | None = None,
        plc_id: str | None = None,
        line_id: str | None = None,
    ) -> dict[str, Any]:
        params = {
            "station_id": station,
            "cycle_counter": counter,
        }
        if plc_boot_id:
            params["plc_boot_id"] = plc_boot_id
        if plc_id:
            params["plc_id"] = plc_id
        if line_id:
            params["line_id"] = line_id
        query = urllib.parse.urlencode(params)
        return http_json(f"{self.api}/trace/api/by-cycle?{query}")

    def recent(self, status: str, limit: int = 20) -> list[dict[str, Any]]:
        query = urllib.parse.urlencode({"status": status, "limit": limit})
        return http_json(f"{self.api}/trace/api/recent?{query}")

    def update_station(self, station: str, payload: dict[str, Any]) -> dict[str, Any]:
        return http_json(
            f"{self.vplc}/vplc/stations/{station}",
            method="POST",
            payload=payload,
            headers={"X-VPLC-Actor": "verification-sprint"},
        )

    def force_nok(self, station: str, code: int) -> dict[str, Any]:
        return http_json(
            f"{self.vplc}/vplc/stations/{station}/force-nok",
            method="POST",
            payload={
                "nok_code": code,
                "count": 1,
                "reason": f"acceptance sprint {station} NOK",
            },
            headers={"X-VPLC-Actor": "verification-sprint"},
        )

    def snapshots(self, limit: int = 100) -> list[dict[str, Any]]:
        return http_json(f"{self.vplc}/vplc/audit/snapshots?limit={limit}")["items"]

    def grafana_health(self) -> dict[str, Any]:
        return http_json(f"{self.grafana}/api/health")

    def dashboards(self) -> list[dict[str, Any]]:
        return http_json(f"{self.grafana}/api/search?query=Edge%20MES")

    def sql(self, sql: str) -> list[dict[str, Any]]:
        response = http_json(
            f"{self.grafana}/api/ds/query",
            method="POST",
            payload={
                "queries": [
                    {
                        "refId": "A",
                        "datasource": {
                            "uid": "edge-mes-postgres",
                            "type": "grafana-postgresql-datasource",
                        },
                        "rawSql": sql,
                        "format": "table",
                    }
                ],
                "from": "now-24h",
                "to": "now",
            },
        )
        result = response["results"]["A"]
        if result.get("status") != 200:
            raise RuntimeError(f"Grafana SQL failed: {result}")
        frames = result.get("frames") or []
        if not frames:
            return []
        frame = frames[0]
        fields = [field["name"] for field in frame["schema"]["fields"]]
        values = frame.get("data", {}).get("values", [])
        if not values:
            return []
        return [dict(zip(fields, row)) for row in zip(*values)]


def wait_for_station_nok(
    client: AcceptanceClient,
    station: str,
    start_counter: int,
    *,
    timeout: float = 180,
) -> tuple[int, dict[str, Any]]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        state = client.state()
        station_state = state["stations"][station]
        if station_state["cycle_counter"] > start_counter and station_state["last_result"] == 2:
            return int(station_state["cycle_counter"]), state
        time.sleep(2)
    raise TimeoutError(f"{station} did not produce forced NOK within {timeout}s")


def trace_for_identity(
    client: AcceptanceClient,
    station: str,
    plc_boot_id: str,
    counter: int,
) -> dict[str, Any]:
    rows = client.sql(
        f"""
        SELECT unit_id
        FROM cycle_event
        WHERE station_id = '{station}'
          AND plc_boot_id = '{plc_boot_id}'
          AND cycle_counter = {counter}
        ORDER BY id DESC
        LIMIT 1
        """
    )
    if not rows:
        raise LookupError(f"cycle event not found for {station}/{plc_boot_id}/{counter}")
    return client.trace(str(rows[0]["unit_id"]))


def wait_for_trace(
    client: AcceptanceClient,
    station: str,
    plc_boot_id: str,
    counter: int,
    *,
    require_ws03: bool,
    timeout: float = 180,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_error = ""
    while time.monotonic() < deadline:
        try:
            trace = trace_for_identity(client, station, plc_boot_id, counter)
            if trace.get("found") and (not require_ws03 or trace["stations"].get("WS03")):
                return trace
        except (LookupError, RuntimeError) as exc:
            last_error = str(exc)
        time.sleep(2)
    raise TimeoutError(f"trace not complete for {station}:{counter}; last_error={last_error}")


def validate_normal_flow(client: AcceptanceClient) -> dict[str, Any]:
    recent = client.recent("completed_ok", 20)
    if not recent:
        raise AssertionError("no completed OK unit available")
    selected = recent[0]
    trace = client.trace(selected["unit_id"])
    events = trace["events"]
    assert len(events) == 3, trace
    assert [event["station_id"] for event in events] == ["WS01", "WS02", "WS03"], trace
    assert len({event["unit_id"] for event in events}) == 1, trace
    assert len({event["cycle_counter"] for event in events}) == 1, trace
    assert all(event["result"] == "OK" for event in events), trace
    assert all(event["ack_status"] == "ACK_OK" for event in events), trace
    return {
        "status": "PASS",
        "unit_id": trace["unit_id"],
        "cycle_counter": events[0]["cycle_counter"],
        "events": events,
    }


def validate_nok_trace(station: str, code: int, trace: dict[str, Any]) -> None:
    stations = trace["stations"]
    target = stations[station]
    assert target["result"] == "NOK", trace
    assert target["nok_codes"] == [code], trace
    assert target["defect_origin_station"] == station, trace
    assert target["defect_code"] == code, trace
    assert target["ack_status"] == "ACK_OK", trace
    if station == "WS01":
        downstream = ("WS02", "WS03")
    elif station == "WS02":
        assert stations["WS01"]["result"] == "OK", trace
        downstream = ("WS03",)
    else:
        assert stations["WS01"]["result"] == "OK", trace
        assert stations["WS02"]["result"] == "OK", trace
        downstream = ()
    for downstream_station in downstream:
        event = stations[downstream_station]
        assert event["result"] == "SKIPPED", trace
        assert event["process_status"] == "SKIPPED", trace
        assert event["skip_reason"] == "UPSTREAM_NOK", trace
        assert event["defect_origin_station"] == station, trace
        assert event["defect_code"] == code, trace


def validate_nok_scenario(client: AcceptanceClient, station: str, code: int) -> dict[str, Any]:
    before = client.state()
    plc_boot_id = client.snapshots(1)[0]["plc_boot_id"]
    start_counter = int(before["stations"][station]["cycle_counter"])
    client.force_nok(station, code)
    counter, nok_state = wait_for_station_nok(client, station, start_counter)
    trace = wait_for_trace(client, station, plc_boot_id, counter, require_ws03=True)
    validate_nok_trace(station, code, trace)
    unit_id = trace["unit_id"]
    identity_event = trace["stations"][station]
    current_boot_trace = client.trace_by_cycle(station, counter)
    explicit_boot_trace = client.trace_by_cycle(
        station,
        counter,
        plc_boot_id=plc_boot_id,
        plc_id=identity_event["plc_id"],
        line_id=identity_event["line_id"],
    )
    assert current_boot_trace["unit_id"] == unit_id, current_boot_trace
    assert explicit_boot_trace["unit_id"] == unit_id, explicit_boot_trace
    quality_rows = client.sql(
        f"""
        SELECT q.station_id, q.result, q.nok_codes, q.nok_source, c.unit_id, c.cycle_counter
        FROM quality_event q
        JOIN cycle_event c ON c.id = q.cycle_event_id
        WHERE c.unit_id = '{unit_id}' AND q.station_id = '{station}'
        ORDER BY q.id DESC
        """
    )
    assert quality_rows, f"quality_event missing for {unit_id} {station}"
    quality = quality_rows[0]
    assert quality["result"] == "NOK", quality
    assert normalize_int_array(quality["nok_codes"]) == [code], quality
    raw_rows = client.sql(
        f"""
        SELECT station_id,
               decoded_json ->> 'result' AS result,
               decoded_json ->> 'nok_code_count' AS nok_code_count,
               decoded_json ->> 'nok_codes_1' AS nok_codes_1,
               decoded_json ->> 'nok_codes_2' AS nok_codes_2,
               decoded_json ->> 'nok_codes_3' AS nok_codes_3,
               decoded_json ->> 'cycle_counter' AS cycle_counter
        FROM raw_plc_sample
        WHERE station_id = '{station}'
          AND decoded_json ->> 'cycle_counter' = '{counter}'
        ORDER BY id DESC
        LIMIT 1
        """
    )
    assert raw_rows, f"raw PLC payload missing for {station}:{counter}"
    raw = raw_rows[0]
    assert str(raw["result"]) in {"2", "NOK"}, raw
    assert raw_nok_codes(raw) == [code], raw
    dashboard_rows = client.sql(
        f"""
        SELECT station_id, cycle_counter, unit_id, result, nok_codes, ack_status,
               process_status, skip_reason, defect_origin_station, defect_code
        FROM cycle_event
        WHERE unit_id = '{unit_id}'
        ORDER BY route_step
        """
    )
    assert len(dashboard_rows) == 3, dashboard_rows
    return {
        "status": "PASS",
        "station": station,
        "code": code,
        "counter": counter,
        "unit_id": unit_id,
        "state_after_nok": nok_state["stations"][station],
        "trace": trace,
        "by_cycle_current_boot": current_boot_trace,
        "by_cycle_explicit_boot": explicit_boot_trace,
        "quality_event": quality,
        "raw_payload": raw,
        "dashboard_source_rows": dashboard_rows,
    }


def validate_profiles(client: AcceptanceClient) -> dict[str, Any]:
    current = client.state()
    assert current["profile"] == "normal", current
    assert current["scale"] == 1.0, current
    profile_rows = client.sql(
        """
        SELECT DISTINCT ON (profile)
               profile, cycle_scale, plc_boot_id, captured_at
        FROM vplc_parameter_snapshot
        WHERE profile IN ('normal', 'fast', 'test')
        ORDER BY profile, captured_at DESC
        """
    )
    startup_profiles = {
        str(row["profile"]): row
        for row in profile_rows
        if row.get("profile") in {"normal", "fast", "test"}
    }
    assert set(startup_profiles) == {"normal", "fast", "test"}, startup_profiles
    current_snapshot = client.snapshots(1)
    normal_boot = (
        str(current_snapshot[0]["plc_boot_id"])
        if current_snapshot and current_snapshot[0].get("profile") == "normal"
        else str(startup_profiles["normal"]["plc_boot_id"])
    )
    cycle_rows = client.sql(
        f"""
        SELECT station_id, count(*) AS rows,
               round(avg(cycle_time_ms) / 1000.0, 2) AS avg_cycle_s,
               min(cycle_counter) AS min_counter,
               max(cycle_counter) AS max_counter
        FROM cycle_event
        WHERE plc_boot_id = '{normal_boot}'
        GROUP BY station_id
        ORDER BY station_id
        """
    )
    assert len(cycle_rows) == 3, cycle_rows
    return {
        "status": "PASS",
        "current": current,
        "startup_profiles": startup_profiles,
        "database_profiles": profile_rows,
        "dashboard_cycle_source": cycle_rows,
    }


def collect_observation(client: AcceptanceClient) -> dict[str, Any]:
    state = client.state()
    plc_boot_id = client.snapshots(1)[0]["plc_boot_id"]
    return {
        "captured_at": datetime.now().astimezone().isoformat(),
        "vplc": state,
        "api_health": http_json(f"{client.api}/health"),
        "grafana_health": client.grafana_health(),
        "dashboards": client.dashboards(),
        "collector": client.sql(
            """
            SELECT station_id, collector_state, plc_connection_state, last_cycle_counter,
                   plc_boot_id, ack_timeout, updated_at
            FROM collector_runtime_status
            ORDER BY station_id
            """
        ),
        "counter_integrity": client.sql(
            f"""
            SELECT station_id, min(cycle_counter) AS min_counter,
                   max(cycle_counter) AS max_counter, count(*) AS rows,
                   count(DISTINCT cycle_counter) AS unique_counters,
                   count(*) FILTER (WHERE ack_status <> 'ACK_OK') AS non_ack_ok
            FROM cycle_event
            WHERE plc_boot_id = '{plc_boot_id}'
            GROUP BY station_id
            ORDER BY station_id
            """
        ),
        "duplicate_event_keys": client.sql(
            """
            SELECT plc_id, station_id, plc_boot_id, cycle_counter, count(*) AS rows
            FROM cycle_event
            GROUP BY plc_id, station_id, plc_boot_id, cycle_counter
            HAVING count(*) > 1
            LIMIT 20
            """
        ),
        "uid_integrity": client.sql(
            f"""
            SELECT count(*) AS ws03_rows, count(DISTINCT unit_id) AS distinct_uids,
                   min((payload ->> 'serial_no')::int) AS min_serial,
                   max((payload ->> 'serial_no')::int) AS max_serial
            FROM cycle_event
            WHERE plc_boot_id = '{plc_boot_id}'
              AND station_id = 'WS03'
            """
        ),
        "collector_errors": client.sql(
            """
            SELECT error_type, count(*) AS rows,
                   min(created_at) AS first_seen,
                   max(created_at) AS last_seen,
                   (array_agg(error_message ORDER BY created_at DESC))[1] AS latest_message
            FROM collector_error_log
            WHERE created_at >= now() - interval '2 hours'
            GROUP BY error_type
            ORDER BY rows DESC
            """
        ),
        "recent_completed_ok": client.recent("completed_ok", 10),
    }


def collect_by_cycle_boot_regression(client: AcceptanceClient) -> dict[str, Any]:
    samples = client.sql(
        """
        WITH current_candidates AS MATERIALIZED (
            SELECT current_event.plc_id,
                   current_event.line_id,
                   current_event.station_id,
                   current_event.cycle_counter,
                   current_event.plc_boot_id,
                   current_event.unit_id,
                   current_event.plc_end_time,
                   current_event.id
            FROM collector_runtime_status runtime
            JOIN cycle_event current_event
              ON current_event.plc_id = runtime.plc_id
             AND current_event.line_id = runtime.line_id
             AND current_event.station_id = runtime.station_id
             AND current_event.plc_boot_id = runtime.plc_boot_id
            WHERE runtime.plc_boot_id IS NOT NULL
              AND runtime.plc_boot_id <> ''
              AND current_event.unit_id IS NOT NULL
            ORDER BY current_event.plc_end_time DESC NULLS LAST,
                     current_event.id DESC
            LIMIT 200
        )
        SELECT current_event.plc_id,
               current_event.line_id,
               current_event.station_id,
               current_event.cycle_counter,
               current_event.plc_boot_id AS current_boot_id,
               current_event.unit_id AS current_unit_id,
               old_event.plc_boot_id AS old_boot_id,
               old_event.unit_id AS old_unit_id
        FROM current_candidates current_event
        JOIN LATERAL (
            SELECT plc_boot_id, unit_id
            FROM cycle_event
            WHERE plc_id = current_event.plc_id
              AND line_id = current_event.line_id
              AND station_id = current_event.station_id
              AND cycle_counter = current_event.cycle_counter
              AND plc_boot_id <> current_event.plc_boot_id
            ORDER BY plc_end_time DESC NULLS LAST, id DESC
            LIMIT 1
        ) old_event ON TRUE
        ORDER BY current_event.plc_end_time DESC NULLS LAST, current_event.id DESC
        LIMIT 1
        """
    )
    if not samples:
        raise AssertionError("no current/old boot pair with the same station counter")
    sample = samples[0]
    station = str(sample["station_id"])
    counter = int(sample["cycle_counter"])
    plc_id = str(sample["plc_id"])
    line_id = str(sample["line_id"])
    current_boot = str(sample["current_boot_id"])
    old_boot = str(sample["old_boot_id"])
    current_unit = str(sample["current_unit_id"])
    old_unit = str(sample["old_unit_id"])

    default_query = client.trace_by_cycle(station, counter)
    explicit_current = client.trace_by_cycle(
        station,
        counter,
        plc_boot_id=current_boot,
        plc_id=plc_id,
        line_id=line_id,
    )
    explicit_old = client.trace_by_cycle(
        station,
        counter,
        plc_boot_id=old_boot,
        plc_id=plc_id,
        line_id=line_id,
    )

    checks = {
        "sample_units_are_distinct": current_unit != old_unit,
        "default_returns_current_unit": default_query.get("unit_id") == current_unit,
        "explicit_current_returns_current_unit": explicit_current.get("unit_id") == current_unit,
        "explicit_old_returns_old_unit": explicit_old.get("unit_id") == old_unit,
        "default_events_match_current_boot": bool(default_query.get("events"))
        and all(
            event.get("plc_boot_id") == current_boot
            for event in default_query["events"]
        ),
        "explicit_current_events_match_current_boot": bool(explicit_current.get("events"))
        and all(
            event.get("plc_boot_id") == current_boot
            for event in explicit_current["events"]
        ),
        "explicit_old_events_match_old_boot": bool(explicit_old.get("events"))
        and all(
            event.get("plc_boot_id") == old_boot
            for event in explicit_old["events"]
        ),
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "captured_at": datetime.now().astimezone().isoformat(),
        "sample": sample,
        "checks": checks,
        "default_query": default_query,
        "explicit_current": explicit_current,
        "explicit_old": explicit_old,
    }


def run(client: AcceptanceClient) -> dict[str, Any]:
    started_at = datetime.now().astimezone().isoformat()
    original_state = client.state()
    original_rates = {
        station: values["nok_rate"] for station, values in original_state["stations"].items()
    }
    result: dict[str, Any] = {
        "started_at": started_at,
        "host": urllib.parse.urlparse(client.vplc).hostname,
        "baseline": {
            "vplc": original_state,
            "api_health": http_json(f"{client.api}/health"),
            "grafana_health": client.grafana_health(),
            "dashboards": client.dashboards(),
            "collector": client.sql(
                """
                SELECT station_id, collector_state, plc_connection_state, last_cycle_counter,
                       plc_boot_id, ack_timeout, updated_at
                FROM collector_runtime_status
                ORDER BY station_id
                """
            ),
        },
    }
    try:
        for station in STATION_CODES:
            client.update_station(
                station,
                {"nok_rate": 0.0, "reason": "acceptance sprint deterministic NOK setup"},
            )
        result["normal_flow"] = validate_normal_flow(client)
        result["nok_flows"] = {}
        for station, code in STATION_CODES.items():
            result["nok_flows"][station] = validate_nok_scenario(client, station, code)
        result["profiles"] = validate_profiles(client)
        result["status"] = "PASS"
    finally:
        restore_errors = []
        for station, nok_rate in original_rates.items():
            try:
                client.update_station(
                    station,
                    {"nok_rate": nok_rate, "reason": "acceptance sprint restore baseline"},
                )
            except Exception as exc:  # noqa: BLE001
                restore_errors.append(f"{station}: {exc}")
        result["restored_nok_rates"] = original_rates
        result["restore_errors"] = restore_errors
        result["final_state"] = client.state()
        result["finished_at"] = datetime.now().astimezone().isoformat()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/tmp/edge_mes_acceptance_sprint.json"),
    )
    parser.add_argument("--snapshot-only", action="store_true")
    parser.add_argument("--by-cycle-only", action="store_true")
    args = parser.parse_args()
    client = AcceptanceClient(args.host)
    if args.by_cycle_only:
        result = collect_by_cycle_boot_regression(client)
    elif args.snapshot_only:
        result = collect_observation(client)
    else:
        result = run(client)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    print(json.dumps({"status": result.get("status"), "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
