from __future__ import annotations

from datetime import datetime
from pathlib import Path
import time

from snap7 import util

from app.pipeline import (
    PROCESS_SKIPPED,
    RESULT_OK,
    RESULT_NOK,
    ROUTE_COMPLETED_NOK,
    Part,
    StationJob,
    ThreeStationPipeline,
    SingleLinearRoutePipeline,
)
from app.runtime_config import load_runtime_config


REPO_ROOT = Path(__file__).resolve().parents[2]


def _mapping10() -> dict[str, object]:
    station_ids = [f"WS{i:02d}" for i in range(1, 11)]
    return {
        "line_id": "LINE_DEMO_10",
        "entry_station_id": "WS01",
        "terminal_station_id": "WS10",
        "route_graph": [
            {"from_station_id": left, "to_station_id": right}
            for left, right in zip(station_ids, station_ids[1:])
        ],
        "execution_profile": {"mode": "test", "cycle_scale": 1.0},
        "stations": [
            {
                "station_id": station_id,
                "station_order": index,
                "db_number": 100 + index + (1 if index >= 4 else 0),
                "station_type": "generic",
                "cycle_profile": "test",
                "cycle_time_s": 1.0,
                "jitter_s": 0.0,
                "nok_rate": 0.0,
                "payload_template": "generic_status_v1",
                "nok_template": "flexible_nok_v1",
                "allow_force": True,
                "nok_codes": [11001],
            }
            for index, station_id in enumerate(station_ids, start=1)
        ],
    }


def _ack_ready_payloads(dbs: dict[int, bytearray]) -> None:
    for db in dbs.values():
        if util.get_bool(db, 6, 0):
            util.set_bool(db, 6, 1, True)


def _run_until(
    pipeline: SingleLinearRoutePipeline,
    dbs: dict[int, bytearray],
    predicate,
    timeout_s: float = 8.0,
) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        _ack_ready_payloads(dbs)
        pipeline.tick(dbs, True)
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("condition was not reached before timeout")


def test_single_linear_route_builds_dynamic_topology_and_edge_queues() -> None:
    pipeline = SingleLinearRoutePipeline.from_mapping(_mapping10(), scale=0.05)

    assert pipeline.topology.station_ids == tuple(f"WS{i:02d}" for i in range(1, 11))
    assert pipeline.topology.entry_station_id == "WS01"
    assert pipeline.topology.terminal_station_id == "WS10"
    assert len(pipeline.edge_queues) == 9
    assert set(pipeline.edge_queues) == {
        (f"WS{i:02d}", f"WS{i + 1:02d}") for i in range(1, 10)
    }


def test_snapshot_exposes_real_buffer_identity_and_current_cycle_progress() -> None:
    pipeline = SingleLinearRoutePipeline.from_mapping(_mapping10(), scale=1.0)
    waiting = Part(serial_no=101, unit_id="U-000101", child_dmc="SUB-000101")
    pipeline.edge_queues[("WS01", "WS02")].append(waiting)
    now_mono = time.monotonic()
    running = Part(serial_no=102, unit_id="U-000102", child_dmc="SUB-000102")
    pipeline.stations["WS02"].current_job = StationJob(
        part=running,
        started_at=datetime.now(),
        finish_monotonic=now_mono + 10.0,
        cycle_time_s=20.0,
    )

    state = pipeline.snapshot()

    first_buffer = state["buffers"][0]
    assert first_buffer == {
        "from_station_id": "WS01",
        "to_station_id": "WS02",
        "wip": 1,
        "status": "WAITING",
        "waiting_unit_id": "U-000101",
        "waiting_dmc": "SUB-000101",
    }
    current_cycle = state["stations"]["WS02"]["current_cycle"]
    assert current_cycle["unit_id"] == "U-000102"
    assert current_cycle["dmc"] == "SUB-000102"
    assert current_cycle["planned_cycle_seconds"] == 20.0
    assert 9.0 <= current_cycle["remaining_seconds"] <= 10.0
    assert 49.0 <= current_cycle["progress_percent"] <= 55.0
    assert current_cycle["elapsed_seconds"] > 9.0


def test_runtime_update_keeps_inflight_sample_and_changes_next_job_timing() -> None:
    config = load_runtime_config(REPO_ROOT / "config" / "vplc.yaml")
    pipeline = ThreeStationPipeline(
        scale=config.cycle_scale,
        profile=config.profile,
        allow_runtime_cycle_edit=config.allow_runtime_cycle_edit,
        station_parameters=config.station_dict(),
    )
    station = pipeline.stations["WS01"]
    started_mono = time.monotonic()
    in_flight = Part(serial_no=101, unit_id="U-000101", child_dmc="SUB-000101")
    station.current_job = StationJob(
        part=in_flight,
        started_at=datetime.now(),
        finish_monotonic=started_mono + 17.5,
        cycle_time_s=17.5,
    )

    pipeline.update_station(
        "WS01",
        {"base_cycle_s": 44.0, "jitter_s": 0.0, "nok_rate": 0.125},
        audit_context={"reason": "timing boundary test"},
    )

    assert station.current_job is not None
    assert station.current_job.part.unit_id == "U-000101"
    assert station.current_job.cycle_time_s == 17.5
    assert station.current_job.finish_monotonic == started_mono + 17.5

    station.current_job = None
    next_part = Part(serial_no=102, unit_id="U-000102", child_dmc="SUB-000102")
    pipeline._start_station(station, next_part, datetime.now(), time.monotonic())
    assert station.current_job is not None
    assert station.current_job.cycle_time_s == 44.0


def test_single_linear_route_accepts_explicit_test_serial_start() -> None:
    pipeline = SingleLinearRoutePipeline.from_mapping(
        _mapping10(),
        scale=0.05,
        initial_serial_no=13000,
    )

    assert pipeline.serial_no == 13000


def test_single_linear_route_ok_unit_reaches_only_configured_terminal() -> None:
    pipeline = SingleLinearRoutePipeline.from_mapping(_mapping10(), scale=0.05)
    dbs = {station.db_number: bytearray(512) for station in pipeline.stations.values()}

    _run_until(pipeline, dbs, lambda: pipeline.stations["WS10"].cycle_counter >= 1)

    assert pipeline.completed_quantity == 1
    assert util.get_int(dbs[pipeline.stations["WS10"].db_number], 16) == RESULT_OK
    assert util.get_int(dbs[pipeline.stations["WS03"].db_number], 252) != ROUTE_COMPLETED_NOK
    assert all(station.cycle_counter >= 1 for station in pipeline.stations.values())


def test_single_linear_route_mid_route_nok_preserves_origin_and_skips_downstream() -> None:
    pipeline = SingleLinearRoutePipeline.from_mapping(_mapping10(), scale=0.05)
    dbs = {station.db_number: bytearray(512) for station in pipeline.stations.values()}
    pipeline.force_nok("WS05", 11001, audit_context={"reason": "deterministic route test"})

    _run_until(pipeline, dbs, lambda: pipeline.stations["WS10"].cycle_counter >= 1)

    nok_events = [
        event for event in pipeline.event_history
        if event["station_id"] == "WS05" and event["result"] != RESULT_OK
    ]
    assert nok_events
    unit_id = nok_events[0]["unit_id"]
    unit_events = [event for event in pipeline.event_history if event["unit_id"] == unit_id]
    by_station = {event["station_id"]: event for event in unit_events}
    for station_id in ("WS06", "WS07", "WS08", "WS09"):
        assert by_station[station_id]["result"] == RESULT_NOK
        assert by_station[station_id]["process_status"] == PROCESS_SKIPPED
        assert by_station[station_id]["defect_origin_station"] == "WS05"
        assert by_station[station_id]["defect_code"] == 11001
    assert by_station["WS10"]["result"] == RESULT_NOK
    assert by_station["WS10"]["route_state"] == ROUTE_COMPLETED_NOK
    assert pipeline.completed_quantity == 0
