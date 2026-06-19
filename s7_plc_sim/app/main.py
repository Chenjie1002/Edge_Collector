from __future__ import annotations

import logging
import os
import threading
import time

import httpx
import snap7
from snap7 import type as snap7_type
import uvicorn

from app.control_api import create_control_app
from app.plc_db import LineRuntimeIdentity, load_mapping, write_line_runtime_to_db, write_state_to_db
from app.pipeline import ThreeStationPipeline
from app.parameter_audit import ParameterAuditRecorder
from app.runtime_config import load_runtime_config


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("s7-plc-sim")
logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    mapping = load_mapping()
    plc_cfg = mapping.get("plc", {})
    db_number = int(plc_cfg.get("db_number", 100))
    db_size = max(int(plc_cfg.get("db_size", 64)), 64)
    port = int(os.environ.get("S7_PORT", plc_cfg.get("port", 1102)))
    interval_ms = int(os.environ.get("S7_UPDATE_INTERVAL_MS", "200"))
    simulator_url = os.environ.get("SIMULATOR_URL", "http://simulator:8100")
    control_port = int(os.environ.get("VPLC_CONTROL_PORT", "8200"))
    runtime_config_path = os.environ.get("VPLC_CONFIG_PATH", "/app/config/vplc.yaml")
    profile_override = os.environ.get("VPLC_PROFILE")
    cycle_scale_text = os.environ.get("VPLC_CYCLE_SCALE")
    runtime_config = load_runtime_config(
        runtime_config_path,
        profile_override=profile_override,
        cycle_scale_override=float(cycle_scale_text) if cycle_scale_text else None,
    )
    ack_deadline_s = float(os.environ.get("VPLC_ACK_DEADLINE_SECONDS", "10"))
    runtime_state_path = os.environ.get("VPLC_RUNTIME_STATE_PATH", "/app/data/vplc_runtime.json")
    runtime_identity = LineRuntimeIdentity.load_or_start(runtime_state_path)
    audit_recorder = ParameterAuditRecorder(os.environ.get("DATABASE_URL"))

    db = bytearray(db_size)
    runtime_db = bytearray(64)
    station_dbs = {
        101: bytearray(512),
        102: bytearray(512),
        103: bytearray(512),
    }

    def reset_runtime_identity() -> None:
        runtime_identity.rotate_boot_id()
        for station_db in station_dbs.values():
            station_db[:] = b"\x00" * len(station_db)

    pipeline = ThreeStationPipeline(
        scale=runtime_config.cycle_scale,
        ack_deadline_s=ack_deadline_s,
        on_counter_reset=reset_runtime_identity,
        profile=runtime_config.profile,
        allow_runtime_cycle_edit=runtime_config.allow_runtime_cycle_edit,
        station_parameters=runtime_config.station_dict(),
        config_source=runtime_config.source,
        config_hash=runtime_config.config_hash,
        audit_recorder=audit_recorder,
        plc_boot_id_provider=lambda: runtime_identity.plc_boot_id,
    )
    pipeline.record_parameter_snapshot("startup", plc_boot_id=runtime_identity.plc_boot_id)
    pipeline_lock = threading.RLock()
    control_app = create_control_app(pipeline, pipeline_lock)
    control_thread = threading.Thread(
        target=lambda: uvicorn.run(control_app, host="0.0.0.0", port=control_port, log_level="warning"),
        name="vplc-control-api",
        daemon=True,
    )
    control_thread.start()
    server = snap7.server.Server()
    server.register_area(snap7_type.SrvArea.DB, db_number, db)
    server.register_area(snap7_type.SrvArea.DB, 104, runtime_db)
    for station_db_number, station_db in station_dbs.items():
        server.register_area(snap7_type.SrvArea.DB, station_db_number, station_db)
    server.start(tcp_port=port)
    logger.info(
        "S7 PLC simulator started db=%s size=%s runtime_db=104 station_dbs=%s port=%s boot_id=%s restart_counter=%s ack_deadline_s=%s profile=%s scale=%s config_source=%s config_hash=%s stations=%s",
        db_number,
        db_size,
        sorted(station_dbs),
        port,
        runtime_identity.plc_boot_id,
        runtime_identity.plc_restart_counter,
        ack_deadline_s,
        runtime_config.profile,
        runtime_config.cycle_scale,
        runtime_config.source,
        runtime_config.config_hash,
        runtime_config.station_dict(),
    )
    logger.info("V-PLC control API started port=%s path=/vplc", control_port)

    try:
        heartbeat = 0
        last_log_at = 0.0
        last_snapshot_at = time.monotonic()
        while True:
            payload = {"running": True}
            try:
                payload = httpx.get(f"{simulator_url}/state", timeout=5).json()
                write_state_to_db(db, payload, mapping)
            except Exception:
                logger.exception("failed to update legacy DB100 from simulator")
            heartbeat += 1
            with pipeline_lock:
                pipeline.tick(station_dbs, bool(payload.get("running", True)))
                write_line_runtime_to_db(
                    runtime_db,
                    protocol_version=1,
                    heartbeat_counter=heartbeat,
                    plc_restart_counter=runtime_identity.plc_restart_counter,
                    plc_boot_id=runtime_identity.plc_boot_id,
                )
            now = time.monotonic()
            if now - last_snapshot_at >= 300:
                last_snapshot_at = now
                with pipeline_lock:
                    pipeline.record_parameter_snapshot(
                        "periodic",
                        plc_boot_id=runtime_identity.plc_boot_id,
                    )
            if now - last_log_at > 5:
                last_log_at = now
                logger.info(
                    "db%s legacy running=%s total=%s station_cycles=WS01:%s WS02:%s WS03:%s",
                    db_number,
                    payload.get("running"),
                    payload.get("total_count"),
                    pipeline.stations["WS01"].cycle_counter,
                    pipeline.stations["WS02"].cycle_counter,
                    pipeline.stations["WS03"].cycle_counter,
                )
            time.sleep(interval_ms / 1000)
    finally:
        server.stop()
        server.destroy()


if __name__ == "__main__":
    main()
