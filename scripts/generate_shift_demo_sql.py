from __future__ import annotations

import argparse
import json
import random
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable
from zoneinfo import ZoneInfo


TZ = ZoneInfo("Asia/Shanghai")
MACHINE_ID = "LINE_01"


@dataclass(frozen=True)
class Window:
    start: datetime
    end: datetime
    code: int
    kind: str
    label: str


@dataclass(frozen=True)
class ShiftSpec:
    shift_id: str
    start: datetime
    end: datetime
    target_cycle_seconds: float
    cycle_sigma_seconds: float
    ng_rate: float
    breaks: list[Window]
    stops: list[Window]


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=TZ)


DAY = ShiftSpec(
    shift_id="20260612_DAY",
    start=dt("2026-06-12T08:30:00"),
    end=dt("2026-06-12T17:00:00"),
    target_cycle_seconds=30.6,
    cycle_sigma_seconds=2.4,
    ng_rate=0.025,
    breaks=[
        Window(dt("2026-06-12T08:30:00"), dt("2026-06-12T08:35:00"), 901, "setup", "startup warm-up"),
        Window(dt("2026-06-12T10:30:00"), dt("2026-06-12T10:40:00"), 902, "break", "operator rest break"),
        Window(dt("2026-06-12T12:00:00"), dt("2026-06-12T12:30:00"), 903, "meal", "lunch break"),
        Window(dt("2026-06-12T14:30:00"), dt("2026-06-12T14:40:00"), 902, "break", "operator rest break"),
        Window(dt("2026-06-12T16:55:00"), dt("2026-06-12T17:00:00"), 904, "cleanup", "end-of-shift cleaning"),
    ],
    stops=[
        Window(
            dt("2026-06-12T09:46:00"),
            dt("2026-06-12T10:04:00"),
            101,
            "fault",
            "cylinder position sensor failure after cylinder signal loss",
        ),
        Window(
            dt("2026-06-12T14:02:00"),
            dt("2026-06-12T14:24:00"),
            201,
            "material",
            "station 1 material shortage due to delayed material delivery",
        ),
    ],
)

NIGHT = ShiftSpec(
    shift_id="20260612_NIGHT",
    start=dt("2026-06-12T20:30:00"),
    end=dt("2026-06-13T05:00:00"),
    target_cycle_seconds=29.2,
    cycle_sigma_seconds=1.35,
    ng_rate=0.014,
    breaks=[
        Window(dt("2026-06-12T20:30:00"), dt("2026-06-12T20:35:00"), 901, "setup", "startup warm-up"),
        Window(dt("2026-06-12T22:30:00"), dt("2026-06-12T22:40:00"), 902, "break", "operator rest break"),
        Window(dt("2026-06-13T00:00:00"), dt("2026-06-13T00:30:00"), 903, "meal", "night meal break"),
        Window(dt("2026-06-13T02:30:00"), dt("2026-06-13T02:40:00"), 902, "break", "operator rest break"),
        Window(dt("2026-06-13T04:55:00"), dt("2026-06-13T05:00:00"), 904, "cleanup", "end-of-shift cleaning"),
    ],
    stops=[],
)


def sql_literal(value: object) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace("'", "''")
    return f"'{text}'"


def json_sql(value: dict) -> str:
    return sql_literal(json.dumps(value, ensure_ascii=False, separators=(",", ":"))) + "::jsonb"


def window_at(now: datetime, windows: Iterable[Window]) -> Window | None:
    for window in windows:
        if window.start <= now < window.end:
            return window
    return None


def normal_cycle(spec: ShiftSpec) -> float:
    cycle = random.gauss(spec.target_cycle_seconds, spec.cycle_sigma_seconds)
    return max(24.0, min(38.0, cycle))


def generate_snapshots(specs: list[ShiftSpec]) -> tuple[list[tuple], list[tuple], list[tuple], list[tuple]]:
    snapshots: list[tuple] = []
    stop_events: list[tuple] = []
    alarm_events: list[tuple] = []
    production_events: list[tuple] = []

    cycle_counter = 0
    total_count = 0
    good_count = 0
    ng_count = 0
    accumulated_seconds = 0.0
    last_cycle_seconds = 30.0
    product_type = "TYPE_A"

    for spec in specs:
        for stop in spec.stops:
            stop_id = str(uuid.uuid4())
            payload = {
                "shift_id": spec.shift_id,
                "reason": stop.label,
                "stop_kind": stop.kind,
                "demo_note": "planned historical demo event",
            }
            stop_events.append(
                (
                    stop_id,
                    MACHINE_ID,
                    stop.code,
                    stop.start.isoformat(),
                    stop.end.isoformat(),
                    int((stop.end - stop.start).total_seconds()),
                    "closed",
                    json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                )
            )
            if stop.code == 101:
                alarm_id = str(uuid.uuid4())
                alarm_events.append(
                    (
                        alarm_id,
                        MACHINE_ID,
                        1001,
                        stop.start.isoformat(),
                        stop.end.isoformat(),
                        int((stop.end - stop.start).total_seconds()),
                        "closed",
                        json.dumps(
                            {
                                "shift_id": spec.shift_id,
                                "alarm_name": "cylinder signal lost",
                                "root_cause": "cylinder position sensor failure",
                            },
                            ensure_ascii=False,
                            separators=(",", ":"),
                        ),
                    )
                )

        now = spec.start
        while now <= spec.end:
            planned_break = window_at(now, spec.breaks)
            unplanned_stop = window_at(now, spec.stops)
            producing = planned_break is None and unplanned_stop is None
            alarm_active = unplanned_stop is not None and unplanned_stop.code == 101
            stop_code = unplanned_stop.code if unplanned_stop else (planned_break.code if planned_break else 0)

            if producing:
                accumulated_seconds += 30.0
                while accumulated_seconds >= last_cycle_seconds:
                    accumulated_seconds -= last_cycle_seconds
                    cycle_counter += 1
                    total_count += 1
                    if random.random() < spec.ng_rate:
                        ng_count += 1
                    else:
                        good_count += 1
                    if cycle_counter % 350 == 0:
                        product_type = {"TYPE_A": "TYPE_B", "TYPE_B": "TYPE_C", "TYPE_C": "TYPE_A"}[product_type]
                    last_cycle_seconds = normal_cycle(spec)
            else:
                accumulated_seconds = min(accumulated_seconds, 5.0)

            cycle_time_ms = int(last_cycle_seconds * 1000)
            snapshots.append(
                (
                    now.isoformat(),
                    MACHINE_ID,
                    producing,
                    True,
                    product_type,
                    spec.shift_id,
                    cycle_counter,
                    good_count,
                    ng_count,
                    total_count,
                    cycle_time_ms,
                    alarm_active,
                    1001 if alarm_active else 0,
                    stop_code,
                )
            )

            if producing and random.random() < 0.09:
                production_events.append(
                    (
                        str(uuid.uuid4()),
                        now.isoformat(),
                        MACHINE_ID,
                        "cycle_completed",
                        None,
                        json.dumps({"shift_id": spec.shift_id, "cycle_counter": cycle_counter}, separators=(",", ":")),
                    )
                )

            now += timedelta(seconds=30)

    return snapshots, stop_events, alarm_events, production_events


def emit_sql() -> str:
    random.seed(20260612)
    snapshots, stop_events, alarm_events, production_events = generate_snapshots([DAY, NIGHT])
    start = min(DAY.start, NIGHT.start).isoformat()
    end = max(DAY.end, NIGHT.end).isoformat()
    lines: list[str] = [
        "BEGIN;",
        "INSERT INTO machines (machine_id, machine_name, line_name, plc_name)",
        "VALUES ('LINE_01', 'LINE_01', 'Demo Production Line', 'PLC_01')",
        "ON CONFLICT (machine_id) DO UPDATE SET machine_name = EXCLUDED.machine_name, line_name = EXCLUDED.line_name, plc_name = EXCLUDED.plc_name;",
        f"DELETE FROM sync_outbox WHERE source_table = 'production_snapshot' AND source_id IN (SELECT id::text FROM production_snapshot WHERE machine_id = 'LINE_01' AND ts >= {sql_literal(start)}::timestamptz AND ts <= {sql_literal(end)}::timestamptz);",
        f"DELETE FROM sync_outbox WHERE source_table = 'production_events' AND source_id IN (SELECT event_id::text FROM production_events WHERE machine_id = 'LINE_01' AND ts >= {sql_literal(start)}::timestamptz AND ts <= {sql_literal(end)}::timestamptz);",
        f"DELETE FROM sync_outbox WHERE source_table = 'alarm_events' AND source_id IN (SELECT alarm_event_id::text FROM alarm_events WHERE machine_id = 'LINE_01' AND started_at >= {sql_literal(start)}::timestamptz AND started_at <= {sql_literal(end)}::timestamptz);",
        f"DELETE FROM sync_outbox WHERE source_table = 'stop_events' AND source_id IN (SELECT stop_event_id::text FROM stop_events WHERE machine_id = 'LINE_01' AND started_at >= {sql_literal(start)}::timestamptz AND started_at <= {sql_literal(end)}::timestamptz);",
        f"DELETE FROM production_events WHERE machine_id = 'LINE_01' AND ts >= {sql_literal(start)}::timestamptz AND ts <= {sql_literal(end)}::timestamptz;",
        f"DELETE FROM alarm_events WHERE machine_id = 'LINE_01' AND started_at >= {sql_literal(start)}::timestamptz AND started_at <= {sql_literal(end)}::timestamptz;",
        f"DELETE FROM stop_events WHERE machine_id = 'LINE_01' AND started_at >= {sql_literal(start)}::timestamptz AND started_at <= {sql_literal(end)}::timestamptz;",
        f"DELETE FROM production_snapshot WHERE machine_id = 'LINE_01' AND ts >= {sql_literal(start)}::timestamptz AND ts <= {sql_literal(end)}::timestamptz;",
        "INSERT INTO stop_events (stop_event_id, machine_id, stop_reason_code, started_at, ended_at, duration_seconds, status, payload) VALUES",
    ]

    lines.extend(
        ",\n".join(
            "("
            + ", ".join(
                [
                    sql_literal(row[0]),
                    sql_literal(row[1]),
                    sql_literal(row[2]),
                    sql_literal(row[3]),
                    sql_literal(row[4]),
                    sql_literal(row[5]),
                    sql_literal(row[6]),
                    sql_literal(row[7]) + "::jsonb",
                ]
            )
            + ")"
            for row in stop_events
        ).splitlines()
    )
    lines[-1] += ";"

    lines.append("INSERT INTO alarm_events (alarm_event_id, machine_id, alarm_code, started_at, ended_at, duration_seconds, status, payload) VALUES")
    lines.extend(
        ",\n".join(
            "("
            + ", ".join(
                [
                    sql_literal(row[0]),
                    sql_literal(row[1]),
                    sql_literal(row[2]),
                    sql_literal(row[3]),
                    sql_literal(row[4]),
                    sql_literal(row[5]),
                    sql_literal(row[6]),
                    sql_literal(row[7]) + "::jsonb",
                ]
            )
            + ")"
            for row in alarm_events
        ).splitlines()
    )
    lines[-1] += ";"

    lines.append(
        "INSERT INTO production_events (event_id, ts, machine_id, event_type, event_code, payload) VALUES"
    )
    lines.extend(
        ",\n".join(
            "("
            + ", ".join(
                [
                    sql_literal(row[0]),
                    sql_literal(row[1]),
                    sql_literal(row[2]),
                    sql_literal(row[3]),
                    sql_literal(row[4]),
                    sql_literal(row[5]) + "::jsonb",
                ]
            )
            + ")"
            for row in production_events
        ).splitlines()
    )
    lines[-1] += ";"

    lines.append(
        "INSERT INTO production_snapshot (ts, machine_id, running, auto_mode, product_type, shift_id, cycle_counter, good_count, ng_count, total_count, cycle_time_ms, alarm_active, alarm_code, stop_reason_code) VALUES"
    )
    lines.extend(
        ",\n".join(
            "("
            + ", ".join(
                [
                    sql_literal(row[0]),
                    sql_literal(row[1]),
                    sql_literal(row[2]),
                    sql_literal(row[3]),
                    sql_literal(row[4]),
                    sql_literal(row[5]),
                    sql_literal(row[6]),
                    sql_literal(row[7]),
                    sql_literal(row[8]),
                    sql_literal(row[9]),
                    sql_literal(row[10]),
                    sql_literal(row[11]),
                    sql_literal(row[12]),
                    sql_literal(row[13]),
                ]
            )
            + ")"
            for row in snapshots
        ).splitlines()
    )
    lines[-1] += ";"

    lines.extend(
        [
            "INSERT INTO sync_outbox (source_table, source_id, target_table, payload, status)",
            "SELECT 'production_snapshot', id::text, 'MES_EDGE_SNAPSHOT', to_jsonb(production_snapshot), 'synced'",
            f"FROM production_snapshot WHERE machine_id = 'LINE_01' AND ts >= {sql_literal(start)}::timestamptz AND ts <= {sql_literal(end)}::timestamptz;",
            "INSERT INTO sync_outbox (source_table, source_id, target_table, payload, status)",
            "SELECT 'stop_events', stop_event_id::text, 'MES_EDGE_STOP_EVENT', to_jsonb(stop_events), 'synced'",
            f"FROM stop_events WHERE machine_id = 'LINE_01' AND started_at >= {sql_literal(start)}::timestamptz AND started_at <= {sql_literal(end)}::timestamptz;",
            "INSERT INTO sync_outbox (source_table, source_id, target_table, payload, status)",
            "SELECT 'alarm_events', alarm_event_id::text, 'MES_EDGE_ALARM_EVENT', to_jsonb(alarm_events), 'synced'",
            f"FROM alarm_events WHERE machine_id = 'LINE_01' AND started_at >= {sql_literal(start)}::timestamptz AND started_at <= {sql_literal(end)}::timestamptz;",
            "COMMIT;",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    sql = emit_sql()
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(sql)
    else:
        print(sql, end="")


if __name__ == "__main__":
    main()
