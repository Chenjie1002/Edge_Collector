from __future__ import annotations

import json
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from typing import Any

import psycopg
from psycopg.types.json import Jsonb

from app.models import MachineState
from app.plc.mapping import StationMapping
from app.services.accepted_station_event_fact import AcceptedStationEventFact


class Storage:
    def __init__(self, dsn: str) -> None:
        self.conn = psycopg.connect(dsn, autocommit=False)

    @contextmanager
    def transaction(self) -> Iterator[None]:
        try:
            yield
        except Exception:
            self.conn.rollback()
            raise
        try:
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def ensure_machine(self, state: MachineState) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO machines (machine_id, machine_name, line_name, plc_name)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (machine_id) DO NOTHING
                """,
                (state.machine_id, state.machine_id, "Demo Production Line", "PLC_01"),
            )
        self.conn.commit()

    def insert_snapshot(self, state: MachineState) -> int:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO production_snapshot (
                    ts, machine_id, running, auto_mode, product_type, shift_id,
                    cycle_counter, good_count, ng_count, total_count, cycle_time_ms,
                    alarm_active, alarm_code, stop_reason_code
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    state.ts,
                    state.machine_id,
                    state.running,
                    state.auto_mode,
                    state.product_type,
                    state.shift_id,
                    state.cycle_counter,
                    state.good_count,
                    state.ng_count,
                    state.total_count,
                    state.cycle_time_ms,
                    state.alarm_active,
                    state.alarm_code,
                    state.stop_reason_code,
                ),
            )
            snapshot_id = cur.fetchone()[0]
        self.insert_outbox("production_snapshot", str(snapshot_id), "MES_EDGE_SNAPSHOT", state.as_dict(), commit=False)
        self.conn.commit()
        return snapshot_id

    def insert_event(self, state: MachineState, event_type: str, event_code: int | None = None, payload: dict | None = None) -> str:
        event_id = str(uuid.uuid4())
        event_payload = payload or {}
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO production_events (event_id, ts, machine_id, event_type, event_code, payload)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (event_id, state.ts, state.machine_id, event_type, event_code, Jsonb(event_payload)),
            )
        outbox_payload = {
            "event_id": event_id,
            "ts": state.ts.isoformat(),
            "machine_id": state.machine_id,
            "event_type": event_type,
            "event_code": event_code,
            "payload": event_payload,
        }
        self.insert_outbox("production_events", event_id, "MES_EDGE_EVENT", outbox_payload, commit=False)
        self.conn.commit()
        return event_id

    def open_alarm(self, state: MachineState) -> str:
        alarm_event_id = str(uuid.uuid4())
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO alarm_events (alarm_event_id, machine_id, alarm_code, started_at, status, payload)
                VALUES (%s, %s, %s, %s, 'open', %s)
                """,
                (alarm_event_id, state.machine_id, state.alarm_code, state.ts, Jsonb(state.as_dict())),
            )
        self.insert_outbox("alarm_events", alarm_event_id, "MES_EDGE_ALARM_EVENT", {"alarm_event_id": alarm_event_id, **state.as_dict()}, commit=False)
        self.conn.commit()
        return alarm_event_id

    def close_alarm(self, alarm_event_id: str, state: MachineState) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE alarm_events
                SET ended_at = %s,
                    duration_seconds = EXTRACT(EPOCH FROM (%s - started_at))::integer,
                    status = 'closed'
                WHERE alarm_event_id = %s
                """,
                (state.ts, state.ts, alarm_event_id),
            )
        self.insert_outbox("alarm_events", alarm_event_id, "MES_EDGE_ALARM_EVENT", {"alarm_event_id": alarm_event_id, "closed_at": state.ts.isoformat()}, commit=False)
        self.conn.commit()

    def close_open_alarms(self, state: MachineState) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE alarm_events
                SET ended_at = %s,
                    duration_seconds = EXTRACT(EPOCH FROM (%s - started_at))::integer,
                    status = 'closed'
                WHERE machine_id = %s
                  AND status = 'open'
                RETURNING alarm_event_id
                """,
                (state.ts, state.ts, state.machine_id),
            )
            closed_ids = [str(row[0]) for row in cur.fetchall()]
        for alarm_event_id in closed_ids:
            self.insert_outbox(
                "alarm_events",
                alarm_event_id,
                "MES_EDGE_ALARM_EVENT",
                {"alarm_event_id": alarm_event_id, "closed_at": state.ts.isoformat()},
                commit=False,
            )
        self.conn.commit()

    def open_stop(self, state: MachineState, reason_code: int) -> str:
        stop_event_id = str(uuid.uuid4())
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO stop_events (stop_event_id, machine_id, stop_reason_code, started_at, status, payload)
                VALUES (%s, %s, %s, %s, 'open', %s)
                """,
                (stop_event_id, state.machine_id, reason_code, state.ts, Jsonb(state.as_dict())),
            )
        self.insert_outbox("stop_events", stop_event_id, "MES_EDGE_STOP_EVENT", {"stop_event_id": stop_event_id, **state.as_dict()}, commit=False)
        self.conn.commit()
        return stop_event_id

    def close_stop(self, stop_event_id: str, state: MachineState) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE stop_events
                SET ended_at = %s,
                    duration_seconds = EXTRACT(EPOCH FROM (%s - started_at))::integer,
                    status = 'closed'
                WHERE stop_event_id = %s
                """,
                (state.ts, state.ts, stop_event_id),
            )
        self.insert_outbox("stop_events", stop_event_id, "MES_EDGE_STOP_EVENT", {"stop_event_id": stop_event_id, "closed_at": state.ts.isoformat()}, commit=False)
        self.conn.commit()

    def close_open_stops(self, state: MachineState) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE stop_events
                SET ended_at = %s,
                    duration_seconds = EXTRACT(EPOCH FROM (%s - started_at))::integer,
                    status = 'closed'
                WHERE machine_id = %s
                  AND status = 'open'
                RETURNING stop_event_id
                """,
                (state.ts, state.ts, state.machine_id),
            )
            closed_ids = [str(row[0]) for row in cur.fetchall()]
        for stop_event_id in closed_ids:
            self.insert_outbox(
                "stop_events",
                stop_event_id,
                "MES_EDGE_STOP_EVENT",
                {"stop_event_id": stop_event_id, "closed_at": state.ts.isoformat()},
                commit=False,
            )
        self.conn.commit()

    def insert_outbox(self, source_table: str, source_id: str, target_table: str, payload: dict[str, Any], commit: bool = True) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sync_outbox (source_table, source_id, target_table, payload)
                VALUES (%s, %s, %s, %s)
                """,
                (source_table, source_id, target_table, Jsonb(payload)),
            )
        if commit:
            self.conn.commit()

    def insert_raw_plc_sample(
        self,
        *,
        plc_id: str,
        line_id: str,
        station_id: str,
        db_number: int,
        read_start: int,
        read_size: int,
        raw_hex: str,
        decoded_json: dict[str, Any],
        commit: bool = True,
    ) -> int:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO raw_plc_sample (
                    plc_id, line_id, station_id, db_number, read_start, read_size,
                    raw_hex, decoded_json
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (plc_id, line_id, station_id, db_number, read_start, read_size, raw_hex, Jsonb(decoded_json)),
            )
            raw_sample_id = int(cur.fetchone()[0])
        if commit:
            self.conn.commit()
        return raw_sample_id

    def persist_cycle(
        self,
        *,
        plc_id: str,
        line_id: str,
        station: StationMapping,
        plc_boot_id: str,
        cycle_counter: int,
        decoded: dict[str, Any],
        db_number: int,
        read_start: int,
        read_size: int,
        raw_hex: str,
        code_tables: dict[str, dict[Any, Any]],
    ) -> int:
        event_id = self.persist_cycle_no_commit(
            plc_id=plc_id,
            line_id=line_id,
            station=station,
            plc_boot_id=plc_boot_id,
            cycle_counter=cycle_counter,
            decoded=decoded,
            db_number=db_number,
            read_start=read_start,
            read_size=read_size,
            raw_hex=raw_hex,
            code_tables=code_tables,
        )
        self.conn.commit()
        return event_id

    def persist_cycle_no_commit(
        self,
        *,
        plc_id: str,
        line_id: str,
        station: StationMapping,
        plc_boot_id: str,
        cycle_counter: int,
        decoded: dict[str, Any],
        db_number: int,
        read_start: int,
        read_size: int,
        raw_hex: str,
        code_tables: dict[str, dict[Any, Any]],
    ) -> int:
        raw_sample_id = self.insert_raw_plc_sample(
            plc_id=plc_id,
            line_id=line_id,
            station_id=station.station_id,
            db_number=db_number,
            read_start=read_start,
            read_size=read_size,
            raw_hex=raw_hex,
            decoded_json=decoded,
            commit=False,
        )
        event_id = self.upsert_cycle_event_no_commit(
            plc_id=plc_id,
            line_id=line_id,
            station=station,
            plc_boot_id=plc_boot_id,
            cycle_counter=cycle_counter,
            decoded=decoded,
            raw_sample_id=raw_sample_id,
            code_tables=code_tables,
        )
        self.insert_quality_event_for_cycle(event_id, commit=False)
        return event_id

    def insert_accepted_station_event_fact_no_commit(self, fact: AcceptedStationEventFact) -> str:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT content_fingerprint
                FROM production_accepted_station_event_fact
                WHERE fact_key = %s
                """,
                (fact.fact_key,),
            )
            row = cur.fetchone()
            if row is not None:
                if row[0] == fact.content_fingerprint:
                    return "existing"
                raise ValueError("accepted station-event fact conflict: fact_key content differs")

            cur.execute(
                """
                SELECT content_fingerprint
                FROM production_accepted_station_event_fact
                WHERE line_id = %s
                  AND plc_id = %s
                  AND station_id = %s
                  AND config_hash = %s
                  AND source_event_id = %s
                  AND event_type = %s
                """,
                fact.source_identity,
            )
            row = cur.fetchone()
            if row is not None:
                if row[0] == fact.content_fingerprint:
                    return "existing"
                raise ValueError("accepted station-event fact conflict: source identity content differs")

            cur.execute(
                """
                INSERT INTO production_accepted_station_event_fact (
                    line_id, plc_id, station_id, station_type, profile_id,
                    config_hash, config_version, event_type, production_result,
                    unit_id, dmc, cycle_counter, source_event_id, event_ts,
                    fact_key, content_fingerprint, nok_code, nok_origin,
                    nok_detail_code, nok_detail_source_event_id,
                    nok_detail_evidence_fact_key
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s
                )
                """,
                (
                    fact.line_id,
                    fact.plc_id,
                    fact.station_id,
                    fact.station_type,
                    fact.profile_id,
                    fact.config_hash,
                    fact.config_version,
                    fact.event_type,
                    fact.production_result,
                    fact.unit_id,
                    fact.dmc,
                    fact.cycle_counter,
                    fact.source_event_id,
                    fact.event_ts,
                    fact.fact_key,
                    fact.content_fingerprint,
                    fact.nok_code,
                    fact.nok_origin,
                    fact.nok_detail_code,
                    fact.nok_detail_source_event_id,
                    fact.nok_detail_evidence_fact_key,
                ),
            )
        return "inserted"

    def rollback(self) -> None:
        self.conn.rollback()

    def get_max_cycle_counter(
        self,
        *,
        plc_id: str,
        station_id: str,
        plc_boot_id: str,
    ) -> int | None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT MAX(cycle_counter)
                FROM cycle_event
                WHERE plc_id = %s
                  AND station_id = %s
                  AND plc_boot_id = %s
                """,
                (plc_id, station_id, plc_boot_id),
            )
            row = cur.fetchone()
        return int(row[0]) if row and row[0] is not None else None

    def upsert_cycle_event(
        self,
        *,
        plc_id: str,
        line_id: str,
        station: StationMapping,
        plc_boot_id: str,
        cycle_counter: int,
        decoded: dict[str, Any],
        raw_sample_id: int,
        code_tables: dict[str, dict[Any, Any]],
    ) -> int:
        event_id = self.upsert_cycle_event_no_commit(
            plc_id=plc_id,
            line_id=line_id,
            station=station,
            plc_boot_id=plc_boot_id,
            cycle_counter=cycle_counter,
            decoded=decoded,
            raw_sample_id=raw_sample_id,
            code_tables=code_tables,
        )
        self.conn.commit()
        return event_id

    def upsert_cycle_event_no_commit(
        self,
        *,
        plc_id: str,
        line_id: str,
        station: StationMapping,
        plc_boot_id: str,
        cycle_counter: int,
        decoded: dict[str, Any],
        raw_sample_id: int,
        code_tables: dict[str, dict[Any, Any]],
    ) -> int:
        result_code = int(decoded.get("result") or 0)
        result = str(code_tables.get("result", {}).get(result_code, result_code))
        nok_codes = self._nok_codes_from_decoded(decoded)
        station_dmc = str(decoded.get("station_dmc") or "")
        upstream_child_dmc = str(decoded.get("upstream_child_dmc") or "")
        upstream_ws02_dmc = str(decoded.get("upstream_ws02_dmc") or "")
        unit_id = str(decoded.get("unit_id") or "")
        route_step = int(decoded.get("route_step") or 0) or None
        route_state = self._code_label(code_tables, "route_state", decoded.get("route_state"))
        process_status = self._code_label(code_tables, "process_status", decoded.get("process_status"))
        skip_reason = self._code_label(code_tables, "skip_reason", decoded.get("skip_reason"))
        defect_origin_station = self._code_label(code_tables, "station_code", decoded.get("defect_origin_station"))
        defect_code = int(decoded.get("defect_code") or 0)
        final_label_code = str(decoded.get("final_label_code") or "")
        reject_id = str(decoded.get("reject_id") or "")
        label_code = final_label_code or (station_dmc if station.dmc_role == "label_code" else None)
        child_dmc = upstream_child_dmc or (station_dmc if station.dmc_role == "child_dmc" else None)
        final_product_id = label_code if station.dmc_role == "label_code" else None
        part_id = child_dmc or station_dmc or None
        trace_key = unit_id or label_code or reject_id or child_dmc or upstream_ws02_dmc or station_dmc or f"{station.station_id}-{cycle_counter}"
        start_time = decoded.get("plc_start_time")
        end_time = decoded.get("plc_end_time")
        cycle_time_ms = self._cycle_time_ms(start_time, end_time)
        payload = {
            key: value
            for key, value in decoded.items()
            if key
            not in {
                "station_status",
                "cycle_counter",
                "payload_ready",
                "read_done",
                "ack_timeout",
                "cycle_valid",
                "plc_start_time",
                "plc_end_time",
                "result",
                "nok_code_count",
                "nok_codes_1",
                "nok_codes_2",
                "nok_codes_3",
                "alarm_code",
                "downtime_type",
                "pallet_id_numeric",
                "station_dmc",
                "unit_id",
                "route_step",
                "route_state",
                "process_status",
                "skip_reason",
                "defect_origin_station",
                "defect_code",
                "final_label_code",
                "reject_id",
            }
        }

        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cycle_event (
                    plc_id, line_id, station_id, plc_boot_id, cycle_counter,
                    trace_key, pallet_id, dmc, child_dmc, label_code, final_product_id, part_id,
                    unit_id, route_step, route_state, process_status, skip_reason,
                    defect_origin_station, defect_code, final_label_code, reject_id,
                    plc_start_time, plc_end_time, cycle_time_ms, result, nok_codes,
                    alarm_code, downtime_type, payload, ack_status, raw_sample_id
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, 'PENDING', %s
                )
                ON CONFLICT (plc_id, station_id, plc_boot_id, cycle_counter)
                DO UPDATE SET
                    trace_key = EXCLUDED.trace_key,
                    pallet_id = EXCLUDED.pallet_id,
                    dmc = EXCLUDED.dmc,
                    child_dmc = EXCLUDED.child_dmc,
                    label_code = EXCLUDED.label_code,
                    final_product_id = EXCLUDED.final_product_id,
                    part_id = EXCLUDED.part_id,
                    unit_id = EXCLUDED.unit_id,
                    route_step = EXCLUDED.route_step,
                    route_state = EXCLUDED.route_state,
                    process_status = EXCLUDED.process_status,
                    skip_reason = EXCLUDED.skip_reason,
                    defect_origin_station = EXCLUDED.defect_origin_station,
                    defect_code = EXCLUDED.defect_code,
                    final_label_code = EXCLUDED.final_label_code,
                    reject_id = EXCLUDED.reject_id,
                    plc_start_time = EXCLUDED.plc_start_time,
                    plc_end_time = EXCLUDED.plc_end_time,
                    cycle_time_ms = EXCLUDED.cycle_time_ms,
                    result = EXCLUDED.result,
                    nok_codes = EXCLUDED.nok_codes,
                    alarm_code = EXCLUDED.alarm_code,
                    downtime_type = EXCLUDED.downtime_type,
                    raw_sample_id = EXCLUDED.raw_sample_id,
                    payload = EXCLUDED.payload,
                    updated_at = now()
                RETURNING id
                """,
                (
                    plc_id,
                    line_id,
                    station.station_id,
                    plc_boot_id,
                    cycle_counter,
                    trace_key,
                    str(decoded.get("pallet_id_numeric") or ""),
                    station_dmc,
                    child_dmc,
                    label_code,
                    final_product_id,
                    part_id,
                    unit_id or None,
                    route_step,
                    route_state,
                    process_status,
                    skip_reason,
                    defect_origin_station,
                    defect_code,
                    final_label_code or None,
                    reject_id or None,
                    start_time,
                    end_time,
                    cycle_time_ms,
                    result,
                    nok_codes,
                    int(decoded.get("alarm_code") or 0),
                    int(decoded.get("downtime_type") or 0),
                    Jsonb(payload),
                    raw_sample_id,
                ),
            )
            event_id = int(cur.fetchone()[0])
        self.insert_outbox(
            "cycle_event",
            str(event_id),
            "MES_EDGE_CYCLE_EVENT",
            {
                "id": event_id,
                "plc_id": plc_id,
                "line_id": line_id,
                "station_id": station.station_id,
                "plc_boot_id": plc_boot_id,
                "cycle_counter": cycle_counter,
                "trace_key": trace_key,
                "dmc": station_dmc,
                "child_dmc": child_dmc,
                "label_code": label_code,
                "final_product_id": final_product_id,
                "part_id": part_id,
                "unit_id": unit_id or None,
                "route_step": route_step,
                "route_state": route_state,
                "process_status": process_status,
                "skip_reason": skip_reason,
                "defect_origin_station": defect_origin_station,
                "defect_code": defect_code,
                "final_label_code": final_label_code or None,
                "reject_id": reject_id or None,
                "result": result,
                "nok_codes": nok_codes,
                "plc_start_time": start_time,
                "plc_end_time": end_time,
                "payload": payload,
            },
            commit=False,
        )
        if unit_id:
            self.upsert_station_event_for_cycle(event_id)
            self.upsert_production_unit_for_event(event_id)
        return event_id

    def upsert_station_event_for_cycle(self, cycle_event_id: int) -> int | None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO station_event (
                    cycle_event_id, unit_id, plc_id, line_id, station_id, route_step,
                    process_status, result, skip_reason, defect_origin_station, defect_code,
                    nok_codes, station_dmc, child_dmc, final_label_code, reject_id,
                    plc_start_time, plc_end_time, cycle_time_ms, payload, raw_sample_id
                )
                SELECT
                    id, unit_id, plc_id, line_id, station_id, route_step,
                    COALESCE(NULLIF(process_status, ''), 'UNKNOWN'), result,
                    NULLIF(skip_reason, 'NONE'), NULLIF(defect_origin_station, 'UNKNOWN'), defect_code,
                    nok_codes, dmc, child_dmc, COALESCE(final_label_code, label_code), reject_id,
                    plc_start_time, plc_end_time, cycle_time_ms, payload, raw_sample_id
                FROM cycle_event
                WHERE id = %s
                  AND unit_id IS NOT NULL
                ON CONFLICT (cycle_event_id)
                DO UPDATE SET
                    route_step = EXCLUDED.route_step,
                    process_status = EXCLUDED.process_status,
                    result = EXCLUDED.result,
                    skip_reason = EXCLUDED.skip_reason,
                    defect_origin_station = EXCLUDED.defect_origin_station,
                    defect_code = EXCLUDED.defect_code,
                    nok_codes = EXCLUDED.nok_codes,
                    station_dmc = EXCLUDED.station_dmc,
                    child_dmc = EXCLUDED.child_dmc,
                    final_label_code = EXCLUDED.final_label_code,
                    reject_id = EXCLUDED.reject_id,
                    plc_start_time = EXCLUDED.plc_start_time,
                    plc_end_time = EXCLUDED.plc_end_time,
                    cycle_time_ms = EXCLUDED.cycle_time_ms,
                    payload = EXCLUDED.payload,
                    raw_sample_id = EXCLUDED.raw_sample_id
                RETURNING id
                """,
                (cycle_event_id,),
            )
            row = cur.fetchone()
        return int(row[0]) if row else None

    def upsert_production_unit_for_event(self, cycle_event_id: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                WITH event AS (
                    SELECT
                        se.id AS station_event_id,
                        se.unit_id,
                        se.plc_id,
                        se.line_id,
                        se.station_id,
                        se.route_step,
                        se.process_status,
                        se.result,
                        se.defect_origin_station,
                        se.defect_code,
                        se.child_dmc,
                        se.final_label_code,
                        se.reject_id,
                        se.plc_end_time,
                        CASE
                            WHEN se.station_id = 'WS03' AND se.result = 'OK' AND se.process_status = 'PROCESSED'
                                THEN 'COMPLETED_OK'
                            WHEN se.station_id = 'WS03' AND (se.result <> 'OK' OR se.process_status = 'SKIPPED')
                                THEN 'COMPLETED_NOK'
                            WHEN se.process_status = 'SKIPPED'
                                THEN 'BYPASSING'
                            ELSE 'WAITING_NEXT_STATION'
                        END AS unit_state,
                        CASE
                            WHEN se.station_id = 'WS03' AND se.result = 'OK' AND se.process_status = 'PROCESSED'
                                THEN 'OK'
                            WHEN se.station_id = 'WS03' AND (se.result <> 'OK' OR se.process_status = 'SKIPPED')
                                THEN 'NOK'
                            ELSE NULL
                        END AS final_result,
                        CASE
                            WHEN se.station_id = 'WS03' AND se.result = 'OK' AND se.process_status = 'PROCESSED'
                                THEN 'SHIPPING'
                            WHEN se.station_id = 'WS03' AND (se.result <> 'OK' OR se.process_status = 'SKIPPED')
                                THEN 'NONCONFORMING_HANDLING'
                            ELSE NULL
                        END AS disposition
                    FROM station_event se
                    WHERE se.cycle_event_id = %s
                ), upserted AS (
                    INSERT INTO production_unit (
                        unit_id, line_id, plc_id, child_dmc, final_label_code, reject_id,
                        current_station_id, current_route_step, current_state, final_result,
                        disposition, defect_origin_station, defect_code, completed_at, updated_at
                    )
                    SELECT
                        unit_id, line_id, plc_id, child_dmc, final_label_code, reject_id,
                        station_id, route_step, unit_state, final_result,
                        disposition, defect_origin_station, defect_code,
                        CASE WHEN final_result IS NOT NULL THEN plc_end_time ELSE NULL END,
                        now()
                    FROM event
                    ON CONFLICT (unit_id)
                    DO UPDATE SET
                        child_dmc = COALESCE(production_unit.child_dmc, EXCLUDED.child_dmc),
                        final_label_code = COALESCE(EXCLUDED.final_label_code, production_unit.final_label_code),
                        reject_id = COALESCE(EXCLUDED.reject_id, production_unit.reject_id),
                        current_station_id = EXCLUDED.current_station_id,
                        current_route_step = EXCLUDED.current_route_step,
                        current_state = EXCLUDED.current_state,
                        final_result = COALESCE(EXCLUDED.final_result, production_unit.final_result),
                        disposition = COALESCE(EXCLUDED.disposition, production_unit.disposition),
                        defect_origin_station = COALESCE(EXCLUDED.defect_origin_station, production_unit.defect_origin_station),
                        defect_code = CASE WHEN EXCLUDED.defect_code > 0 THEN EXCLUDED.defect_code ELSE production_unit.defect_code END,
                        completed_at = COALESCE(EXCLUDED.completed_at, production_unit.completed_at),
                        updated_at = now()
                    RETURNING unit_id
                )
                INSERT INTO unit_state_history (unit_id, station_event_id, state, station_id, route_step, note)
                SELECT unit_id, station_event_id, unit_state, station_id, route_step, process_status
                FROM event
                WHERE NOT EXISTS (
                    SELECT 1 FROM unit_state_history WHERE station_event_id = event.station_event_id
                )
                """
                ,
                (cycle_event_id,),
            )

    def _code_label(self, code_tables: dict[str, dict[Any, Any]], table: str, value: object) -> str:
        table_map = code_tables.get(table, {})
        try:
            return str(table_map.get(int(value or 0), value or "UNKNOWN"))
        except (TypeError, ValueError):
            return str(value or "UNKNOWN")

    def insert_quality_event_for_cycle(self, cycle_event_id: int, *, commit: bool = True) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO quality_event (
                    cycle_event_id, plc_id, line_id, station_id, dmc, label_code,
                    result, nok_codes, nok_source
                )
                SELECT id, plc_id, line_id, station_id, dmc, label_code, result, nok_codes, 'PLC'
                FROM cycle_event
                WHERE id = %s
                  AND NOT EXISTS (
                    SELECT 1 FROM quality_event WHERE cycle_event_id = %s
                  )
                """,
                (cycle_event_id, cycle_event_id),
            )
        if commit:
            self.conn.commit()

    def mark_cycle_ack_ok(self, *, plc_id: str, station_id: str, plc_boot_id: str, cycle_counter: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE cycle_event
                SET ack_status = 'ACK_OK',
                    edge_write_time = now(),
                    updated_at = now()
                WHERE plc_id = %s
                  AND station_id = %s
                  AND plc_boot_id = %s
                  AND cycle_counter = %s
                """,
                (plc_id, station_id, plc_boot_id, cycle_counter),
            )
        self.conn.commit()

    def mark_cycle_ack_failed(
        self,
        *,
        plc_id: str,
        station_id: str,
        plc_boot_id: str,
        cycle_counter: int,
    ) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE cycle_event
                SET ack_status = 'ACK_WRITE_FAILED',
                    retry_count = retry_count + 1,
                    updated_at = now()
                WHERE plc_id = %s
                  AND station_id = %s
                  AND plc_boot_id = %s
                  AND cycle_counter = %s
                """,
                (plc_id, station_id, plc_boot_id, cycle_counter),
            )
        self.conn.commit()

    def insert_collector_error(
        self,
        *,
        plc_id: str,
        line_id: str,
        station_id: str | None,
        error_type: str,
        error_message: str,
        plc_boot_id: str | None = None,
        cycle_counter: int | None = None,
        raw_context: dict[str, Any] | None = None,
    ) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO collector_error_log (
                    plc_id, line_id, station_id, error_type, error_message,
                    plc_boot_id, cycle_counter, raw_context
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    plc_id,
                    line_id,
                    station_id,
                    error_type,
                    error_message,
                    plc_boot_id,
                    cycle_counter,
                    Jsonb(raw_context or {}),
                ),
            )
        self.conn.commit()

    def upsert_collector_runtime_status(
        self,
        *,
        plc_id: str,
        line_id: str,
        station_id: str,
        collector_state: str,
        plc_connection_state: str,
        station_status: str,
        payload_ready: bool,
        read_done: bool,
        last_cycle_counter: int,
        last_success_time: datetime,
        last_error_code: str | None,
        last_error_message: str | None,
        plc_boot_id: str | None = None,
        ack_timeout: bool = False,
    ) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO collector_runtime_status (
                    plc_id, line_id, station_id, collector_state, plc_connection_state,
                    station_status, payload_ready, read_done, last_cycle_counter,
                    last_success_time, last_error_code, last_error_message,
                    plc_boot_id, ack_timeout, updated_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
                ON CONFLICT (plc_id, station_id)
                DO UPDATE SET
                    collector_state = EXCLUDED.collector_state,
                    plc_connection_state = EXCLUDED.plc_connection_state,
                    station_status = EXCLUDED.station_status,
                    payload_ready = EXCLUDED.payload_ready,
                    read_done = EXCLUDED.read_done,
                    last_cycle_counter = EXCLUDED.last_cycle_counter,
                    last_success_time = EXCLUDED.last_success_time,
                    last_error_code = EXCLUDED.last_error_code,
                    last_error_message = EXCLUDED.last_error_message,
                    plc_boot_id = EXCLUDED.plc_boot_id,
                    ack_timeout = EXCLUDED.ack_timeout,
                    updated_at = now()
                """,
                (
                    plc_id,
                    line_id,
                    station_id,
                    collector_state,
                    plc_connection_state,
                    station_status,
                    payload_ready,
                    read_done,
                    last_cycle_counter,
                    last_success_time,
                    last_error_code,
                    last_error_message,
                    plc_boot_id,
                    ack_timeout,
                ),
            )
        self.conn.commit()

    def _nok_codes_from_decoded(self, decoded: dict[str, Any]) -> list[int]:
        count = int(decoded.get("nok_code_count") or 0)
        values = [
            int(decoded.get("nok_codes_1") or 0),
            int(decoded.get("nok_codes_2") or 0),
            int(decoded.get("nok_codes_3") or 0),
        ]
        return [value for value in values[:count] if value > 0]

    def _cycle_time_ms(self, start_time: Any, end_time: Any) -> int | None:
        if not start_time or not end_time:
            return None
        start = datetime.fromisoformat(str(start_time))
        end = datetime.fromisoformat(str(end_time))
        return max(0, int((end - start).total_seconds() * 1000))
