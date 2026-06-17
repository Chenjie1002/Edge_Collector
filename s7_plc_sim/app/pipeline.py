from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
import random
import time
from zoneinfo import ZoneInfo

from snap7 import util

from app.plc_db import clear_station_handshake, set_real, set_s7_string, write_station_header


TZ = ZoneInfo("Asia/Shanghai")

STATUS_IDLE = 1
STATUS_RUNNING = 2
STATUS_WAITING = 3
STATUS_BLOCKED = 4

RESULT_UNKNOWN = 0
RESULT_OK = 1
RESULT_NOK = 2
RESULT_SKIPPED = 3

ROUTE_UNKNOWN = 0
ROUTE_NORMAL = 1
ROUTE_BYPASSING = 2
ROUTE_COMPLETED_OK = 3
ROUTE_COMPLETED_NOK = 4

PROCESS_UNKNOWN = 0
PROCESS_PROCESSED = 1
PROCESS_SKIPPED = 2

SKIP_NONE = 0
SKIP_UPSTREAM_NOK = 1

STATION_CODES = {
    "WS01": 1,
    "WS02": 2,
    "WS03": 3,
}


@dataclass
class Part:
    serial_no: int
    unit_id: str
    child_dmc: str
    label_code: str = ""
    reject_id: str = ""
    route_state: int = ROUTE_NORMAL
    defect_origin_station: str = ""
    defect_code: int = 0
    ws01_end_time: datetime | None = None
    ws01_result: int = RESULT_UNKNOWN
    ws02_end_time: datetime | None = None
    ws02_result: int = RESULT_UNKNOWN


@dataclass
class StationJob:
    part: Part
    started_at: datetime
    finish_monotonic: float
    cycle_time_s: float


@dataclass
class StationState:
    station_id: str
    db_number: int
    base_cycle_s: float
    jitter_s: float
    nok_rate: float
    cycle_counter: int = 0
    current_job: StationJob | None = None
    payload_ready_since: float | None = None
    last_payload_cycle: int = 0
    paused: bool = False
    force_next_nok_code: int | None = None
    last_result: int = RESULT_UNKNOWN
    last_nok_codes: list[int] = field(default_factory=list)
    last_dmc: str = ""
    last_end_time: datetime | None = None
    rng: random.Random = field(default_factory=random.Random)

    def next_cycle_time(self, scale: float) -> float:
        value = self.rng.gauss(self.base_cycle_s, self.jitter_s)
        return max(4.0, value) * scale


@dataclass
class ProductionPlan:
    mode: str = "continuous"
    active: bool = True
    started_at_mono: float | None = None
    started_at: datetime | None = None
    target_end_mono: float | None = None
    target_quantity: int | None = None
    target_shifts: int | None = None
    shift_hours: float | None = None
    completed_quantity_at_start: int = 0
    stop_reason: str = ""


class ThreeStationPipeline:
    def __init__(self, *, scale: float = 1.0, require_ack: bool = False, ack_hold_s: float = 10.0) -> None:
        seed = int(time.time())
        self.scale = max(0.05, scale)
        self.require_ack = require_ack
        self.ack_hold_s = ack_hold_s
        self.serial_no = 0
        self.completed_quantity = 0
        self.external_running = True
        self.q12: deque[Part] = deque()
        self.q23: deque[Part] = deque()
        self.plan = ProductionPlan(started_at_mono=time.monotonic(), started_at=datetime.now(TZ))
        self.stations = {
            "WS01": StationState("WS01", 101, 30.4, 1.2, 0.02, rng=random.Random(seed + 1)),
            "WS02": StationState("WS02", 102, 29.8, 1.0, 0.015, rng=random.Random(seed + 2)),
            "WS03": StationState("WS03", 103, 29.2, 0.9, 0.01, rng=random.Random(seed + 3)),
        }

    def tick(self, dbs: dict[int, bytearray], running: bool) -> None:
        now_mono = time.monotonic()
        now = datetime.now(TZ)
        self.external_running = running
        self._update_plan(now_mono)
        # DB101/102/103 are controlled by the V-PLC production plan. The legacy
        # business simulator still drives DB100, but its random stops should not
        # silently pause the station-level S7 simulation.
        line_running = self.plan.active

        for station in self.stations.values():
            self._handle_ack(station, dbs[station.db_number], now_mono)

        if line_running:
            self._start_jobs(now, now_mono, dbs)

        for station in self.stations.values():
            if station.current_job and now_mono >= station.current_job.finish_monotonic:
                self._finish_job(station, dbs[station.db_number], now)
            elif station.current_job:
                self._write_running(station, dbs[station.db_number])
            elif not util.get_bool(dbs[station.db_number], 6, 0):
                self._write_idle_or_waiting(station, dbs[station.db_number], line_running)

    def _start_jobs(self, now: datetime, now_mono: float, dbs: dict[int, bytearray]) -> None:
        ws01 = self.stations["WS01"]
        if self._can_start(ws01, dbs[ws01.db_number]):
            self.serial_no += 1
            part = Part(
                serial_no=self.serial_no,
                unit_id=f"U-{now:%Y%m%d}-{self.serial_no:06d}",
                child_dmc=f"SUB-{self.serial_no:06d}",
            )
            self._start_station(ws01, part, now, now_mono)

        ws02 = self.stations["WS02"]
        if self._can_start(ws02, dbs[ws02.db_number]) and self.q12:
            self._start_station(ws02, self.q12.popleft(), now, now_mono)

        ws03 = self.stations["WS03"]
        if self._can_start(ws03, dbs[ws03.db_number]) and self.q23:
            self._start_station(ws03, self.q23.popleft(), now, now_mono)

    def _can_start(self, station: StationState, db: bytearray) -> bool:
        return station.current_job is None and not station.paused and not util.get_bool(db, 6, 0)

    def _start_station(self, station: StationState, part: Part, now: datetime, now_mono: float) -> None:
        station.current_job = StationJob(
            part=part,
            started_at=now,
            finish_monotonic=now_mono + station.next_cycle_time(self.scale),
            cycle_time_s=0.0,
        )
        station.current_job.cycle_time_s = station.current_job.finish_monotonic - now_mono

    def _finish_job(self, station: StationState, db: bytearray, now: datetime) -> None:
        job = station.current_job
        if not job:
            return

        station.cycle_counter += 1
        part = job.part
        result, nok_codes, process_status, skip_reason = self._result_for(station.station_id, part)
        dmc = part.child_dmc
        alarm_code = 0
        downtime_type = 0

        if station.station_id == "WS01":
            part.ws01_end_time = now
            part.ws01_result = result
            if result == RESULT_NOK:
                part.route_state = ROUTE_BYPASSING
                part.defect_origin_station = "WS01"
                part.defect_code = nok_codes[0] if nok_codes else 0
            self.q12.append(part)
            self._write_ws01_payload(db, job)
        elif station.station_id == "WS02":
            part.ws02_end_time = now
            part.ws02_result = result
            if result == RESULT_NOK:
                part.route_state = ROUTE_BYPASSING
                part.defect_origin_station = "WS02"
                part.defect_code = nok_codes[0] if nok_codes else 0
            self.q23.append(part)
            self._write_ws02_payload(db, job)
        elif station.station_id == "WS03":
            part.label_code = f"ASM-{part.serial_no:06d}"
            dmc = part.label_code
            if result == RESULT_OK:
                part.route_state = ROUTE_COMPLETED_OK
                self.completed_quantity += 1
            else:
                part.route_state = ROUTE_COMPLETED_NOK
                if not part.reject_id:
                    part.reject_id = f"NG-{part.serial_no:06d}"
                if result == RESULT_NOK and nok_codes:
                    part.defect_origin_station = "WS03"
                    part.defect_code = nok_codes[0]
            self._write_ws03_payload(db, job)

        write_station_header(
            db,
            station_status=STATUS_IDLE,
            cycle_counter=station.cycle_counter,
            payload_ready=True,
            ack_timeout=False,
            cycle_valid=True,
            plc_start_time=job.started_at,
            plc_end_time=now,
            result=result,
            nok_codes=nok_codes,
            alarm_code=alarm_code,
            downtime_type=downtime_type,
            pallet_id_numeric=part.serial_no,
            station_dmc=dmc,
        )
        self._write_station_context(db, station, part, process_status, skip_reason)
        util.set_bool(db, 6, 1, False)
        station.payload_ready_since = time.monotonic()
        station.last_payload_cycle = station.cycle_counter
        station.last_result = result
        station.last_nok_codes = nok_codes
        station.last_dmc = dmc
        station.last_end_time = now
        station.current_job = None

    def _handle_ack(self, station: StationState, db: bytearray, now_mono: float) -> None:
        payload_ready = util.get_bool(db, 6, 0)
        read_done = util.get_bool(db, 6, 1)
        if not payload_ready:
            station.payload_ready_since = None
            return
        if read_done or (not self.require_ack and station.payload_ready_since and now_mono - station.payload_ready_since > self.ack_hold_s):
            clear_station_handshake(db)
            station.payload_ready_since = None

    def _write_running(self, station: StationState, db: bytearray) -> None:
        job = station.current_job
        if not job:
            return
        write_station_header(
            db,
            station_status=STATUS_RUNNING,
            cycle_counter=station.cycle_counter,
            payload_ready=False,
            ack_timeout=False,
            cycle_valid=False,
            plc_start_time=job.started_at,
            plc_end_time=None,
            result=RESULT_UNKNOWN,
            nok_codes=[],
            alarm_code=0,
            downtime_type=0,
            pallet_id_numeric=job.part.serial_no,
            station_dmc=job.part.child_dmc,
        )
        self._write_station_context(
            db,
            station,
            job.part,
            PROCESS_UNKNOWN,
            SKIP_NONE,
            clear_terminal_ids=False,
        )

    def _write_idle_or_waiting(self, station: StationState, db: bytearray, running: bool) -> None:
        status = STATUS_IDLE
        if running and station.station_id == "WS02" and not self.q12:
            status = STATUS_WAITING
        if running and station.station_id == "WS03" and not self.q23:
            status = STATUS_WAITING
        if station.paused or not running:
            status = STATUS_BLOCKED
        write_station_header(
            db,
            station_status=status,
            cycle_counter=station.cycle_counter,
            payload_ready=False,
            ack_timeout=False,
            cycle_valid=False,
            plc_start_time=None,
            plc_end_time=None,
            result=RESULT_UNKNOWN,
            nok_codes=[],
            alarm_code=0,
            downtime_type=0,
            pallet_id_numeric=0,
            station_dmc="",
        )

    def _result_for(self, station_id: str, part: Part) -> tuple[int, list[int], int, int]:
        if station_id != "WS01" and part.route_state == ROUTE_BYPASSING:
            return RESULT_SKIPPED, [30003], PROCESS_SKIPPED, SKIP_UPSTREAM_NOK

        station = self.stations[station_id]
        if station.force_next_nok_code is not None:
            nok_code = station.force_next_nok_code
            station.force_next_nok_code = None
            return RESULT_NOK, [nok_code], PROCESS_PROCESSED, SKIP_NONE

        roll = random.random()
        if station_id == "WS01" and roll < station.nok_rate:
            return RESULT_NOK, [random.choice([10001, 10002, 10003, 10004])], PROCESS_PROCESSED, SKIP_NONE
        if station_id == "WS02" and roll < station.nok_rate:
            return RESULT_NOK, [random.choice([20001, 20002, 20003, 20004, 20005])], PROCESS_PROCESSED, SKIP_NONE
        if station_id == "WS03" and roll < station.nok_rate:
            return RESULT_NOK, [random.choice([30001, 30002])], PROCESS_PROCESSED, SKIP_NONE
        return RESULT_OK, [], PROCESS_PROCESSED, SKIP_NONE

    def _write_station_context(
        self,
        db: bytearray,
        station: StationState,
        part: Part,
        process_status: int,
        skip_reason: int,
        *,
        clear_terminal_ids: bool = True,
    ) -> None:
        set_s7_string(db, 200, part.unit_id, 48)
        util.set_int(db, 250, STATION_CODES[station.station_id])
        util.set_int(db, 252, part.route_state)
        util.set_int(db, 254, process_status)
        util.set_int(db, 256, skip_reason)
        util.set_int(db, 258, STATION_CODES.get(part.defect_origin_station, 0))
        util.set_int(db, 260, part.defect_code)
        set_s7_string(db, 262, part.label_code if clear_terminal_ids else "", 40)
        set_s7_string(db, 304, part.reject_id if clear_terminal_ids else "", 40)

    def snapshot(self) -> dict:
        line_running = self.plan.active
        return {
            "scale": self.scale,
            "require_ack": self.require_ack,
            "serial_no": self.serial_no,
            "completed_quantity": self.completed_quantity,
            "line": {
                "running": line_running,
                "external_running": self.external_running,
                "plan_active": self.plan.active,
                "plan_mode": self.plan.mode,
                "stop_reason": self.plan.stop_reason,
                "started_at": self.plan.started_at.isoformat() if self.plan.started_at else None,
                "elapsed_seconds": self._elapsed_seconds(),
                "remaining_seconds": self._remaining_seconds(),
                "target_quantity": self.plan.target_quantity,
                "target_shifts": self.plan.target_shifts,
                "shift_hours": self.plan.shift_hours,
                "target_end_time": self._target_end_time(),
            },
            "wip": {
                "ws01_to_ws02": len(self.q12),
                "ws02_to_ws03": len(self.q23),
            },
            "stations": {
                station_id: {
                    "station_id": station.station_id,
                    "db_number": station.db_number,
                    "base_cycle_s": station.base_cycle_s,
                    "jitter_s": station.jitter_s,
                    "nok_rate": station.nok_rate,
                    "paused": station.paused,
                    "cycle_counter": station.cycle_counter,
                    "current_dmc": station.current_job.part.child_dmc if station.current_job else "",
                    "last_dmc": station.last_dmc,
                    "last_result": station.last_result,
                    "last_nok_codes": station.last_nok_codes,
                    "last_end_time": station.last_end_time.isoformat() if station.last_end_time else None,
                    "payload_ready": station.payload_ready_since is not None,
                }
                for station_id, station in self.stations.items()
            },
        }

    def update_station(self, station_id: str, params: dict) -> dict:
        station = self._station_or_raise(station_id)
        if "base_cycle_s" in params:
            station.base_cycle_s = max(1.0, float(params["base_cycle_s"]))
        if "jitter_s" in params:
            station.jitter_s = max(0.0, float(params["jitter_s"]))
        if "nok_rate" in params:
            station.nok_rate = min(1.0, max(0.0, float(params["nok_rate"])))
        if "paused" in params:
            station.paused = bool(params["paused"])
        return self.snapshot()

    def force_nok(self, station_id: str, nok_code: int) -> dict:
        station = self._station_or_raise(station_id)
        station.force_next_nok_code = int(nok_code)
        return self.snapshot()

    def reset(self) -> dict:
        self.serial_no = 0
        self.completed_quantity = 0
        self.q12.clear()
        self.q23.clear()
        for station in self.stations.values():
            station.cycle_counter = 0
            station.current_job = None
            station.payload_ready_since = None
            station.last_payload_cycle = 0
            station.last_result = RESULT_UNKNOWN
            station.last_nok_codes = []
            station.last_dmc = ""
            station.last_end_time = None
            station.force_next_nok_code = None
        return self.snapshot()

    def start_plan(self, params: dict) -> dict:
        mode = str(params.get("mode", "continuous")).lower()
        now_mono = time.monotonic()
        now = datetime.now(TZ)
        duration_hours = float(params.get("duration_hours") or 0)
        target_quantity = int(params.get("quantity") or 0)
        target_shifts = int(params.get("shift_count") or 0)
        shift_hours = float(params.get("shift_hours") or 8.5)

        target_end_mono: float | None = None
        plan_quantity: int | None = None
        plan_shifts: int | None = None
        plan_shift_hours: float | None = None

        if mode == "duration":
            target_end_mono = now_mono + max(0.01, duration_hours) * 3600
        elif mode == "quantity":
            plan_quantity = max(1, target_quantity)
        elif mode == "shifts":
            plan_shifts = max(1, target_shifts)
            plan_shift_hours = max(0.1, shift_hours)
            target_end_mono = now_mono + plan_shifts * plan_shift_hours * 3600
        elif mode != "continuous":
            raise ValueError(f"unsupported plan mode: {mode}")

        self.plan = ProductionPlan(
            mode=mode,
            active=True,
            started_at_mono=now_mono,
            started_at=now,
            target_end_mono=target_end_mono,
            target_quantity=plan_quantity,
            target_shifts=plan_shifts,
            shift_hours=plan_shift_hours,
            completed_quantity_at_start=self.completed_quantity,
        )
        return self.snapshot()

    def stop_plan(self, reason: str = "manual_stop") -> dict:
        self.plan.active = False
        self.plan.stop_reason = reason
        return self.snapshot()

    def _station_or_raise(self, station_id: str) -> StationState:
        station_key = station_id.upper()
        if station_key not in self.stations:
            raise KeyError(f"unknown station_id: {station_id}")
        return self.stations[station_key]

    def _update_plan(self, now_mono: float) -> None:
        if not self.plan.active:
            return
        if self.plan.target_end_mono is not None and now_mono >= self.plan.target_end_mono:
            self.stop_plan("target_time_reached")
            return
        if self.plan.target_quantity is not None:
            produced = self.completed_quantity - self.plan.completed_quantity_at_start
            if produced >= self.plan.target_quantity:
                self.stop_plan("target_quantity_reached")

    def _elapsed_seconds(self) -> int:
        if self.plan.started_at_mono is None:
            return 0
        return max(0, int(time.monotonic() - self.plan.started_at_mono))

    def _remaining_seconds(self) -> int | None:
        if self.plan.target_end_mono is None:
            return None
        return max(0, int(self.plan.target_end_mono - time.monotonic()))

    def _target_end_time(self) -> str | None:
        remaining = self._remaining_seconds()
        if remaining is None:
            return None
        return datetime.fromtimestamp(time.time() + remaining, TZ).isoformat()

    def _write_ws01_payload(self, db: bytearray, job: StationJob) -> None:
        set_real(db, 100, random.uniform(1.20, 1.55))
        set_real(db, 104, random.uniform(88.0, 95.0))
        set_real(db, 108, random.uniform(1.18, 1.54))
        set_real(db, 112, random.uniform(87.0, 96.0))
        set_real(db, 116, random.uniform(1.19, 1.56))
        set_real(db, 120, random.uniform(88.0, 95.5))

    def _write_ws02_payload(self, db: bytearray, job: StationJob) -> None:
        part = job.part
        set_real(db, 100, random.uniform(2.1, 2.8))
        set_real(db, 104, random.uniform(23.7, 24.4))
        util.set_dint(db, 108, int(random.uniform(850, 1250)))
        util.set_dint(db, 112, int(random.uniform(820, 1180)))
        set_real(db, 116, random.uniform(3.0, 3.8))
        util.set_dint(db, 120, int(random.uniform(120, 240)))
        util.set_dint(db, 124, int(part.ws01_end_time.timestamp()) if part.ws01_end_time else 0)
        util.set_int(db, 128, part.ws01_result)
        set_s7_string(db, 130, part.child_dmc, 40)

    def _write_ws03_payload(self, db: bytearray, job: StationJob) -> None:
        part = job.part
        util.set_dint(db, 100, part.serial_no)
        util.set_int(db, 104, 1)
        util.set_dint(db, 106, int(part.ws02_end_time.timestamp()) if part.ws02_end_time else 0)
        util.set_int(db, 110, part.ws02_result)
        set_s7_string(db, 112, part.child_dmc, 40)
        set_s7_string(db, 154, part.child_dmc, 40)
