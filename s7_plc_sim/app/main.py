from __future__ import annotations

import logging
import os
import threading
import time
import uuid

import httpx
import snap7
from snap7 import type as snap7_type
import uvicorn

from app.control_api import create_control_app
from app.plc_db import load_mapping, write_state_to_db
from app.pipeline import ThreeStationPipeline


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
    pipeline_scale = float(os.environ.get("VPLC_CYCLE_SCALE", "1.0"))
    require_ack = os.environ.get("VPLC_REQUIRE_ACK", "false").lower() == "true"
    plc_boot_id = str(uuid.uuid4())

    db = bytearray(db_size)
    station_dbs = {
        101: bytearray(512),
        102: bytearray(512),
        103: bytearray(512),
    }
    pipeline = ThreeStationPipeline(scale=pipeline_scale, require_ack=require_ack)
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
    for station_db_number, station_db in station_dbs.items():
        server.register_area(snap7_type.SrvArea.DB, station_db_number, station_db)
    server.start(tcp_port=port)
    logger.info(
        "S7 PLC simulator started db=%s size=%s station_dbs=%s port=%s boot_id=%s require_ack=%s scale=%s",
        db_number,
        db_size,
        sorted(station_dbs),
        port,
        plc_boot_id,
        require_ack,
        pipeline_scale,
    )
    logger.info("V-PLC control API started port=%s path=/vplc", control_port)

    try:
        heartbeat = 0
        last_log_at = 0.0
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
            now = time.monotonic()
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
