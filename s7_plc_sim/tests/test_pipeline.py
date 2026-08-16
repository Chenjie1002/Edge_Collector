from __future__ import annotations

import time

from snap7 import util

from app.pipeline import (
    PROCESS_SKIPPED,
    RESULT_OK,
    RESULT_SKIPPED,
    ROUTE_COMPLETED_NOK,
    SingleLinearRoutePipeline,
)


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
        assert by_station[station_id]["result"] == RESULT_SKIPPED
        assert by_station[station_id]["process_status"] == PROCESS_SKIPPED
        assert by_station[station_id]["defect_origin_station"] == "WS05"
        assert by_station[station_id]["defect_code"] == 11001
    assert by_station["WS10"]["result"] == RESULT_SKIPPED
    assert by_station["WS10"]["route_state"] == ROUTE_COMPLETED_NOK
    assert pipeline.completed_quantity == 0
