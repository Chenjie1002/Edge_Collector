from __future__ import annotations

import hashlib
import logging
import os
import stat
import threading
import time
from collections.abc import Mapping
from pathlib import Path

import httpx
import snap7
from snap7 import type as snap7_type
import uvicorn
import yaml

from app.control_api import create_control_app
from app.plc_db import LineRuntimeIdentity, load_mapping, write_line_runtime_to_db, write_state_to_db
from app.pipeline import SingleLinearRoutePipeline
from app.parameter_audit import ParameterAuditRecorder
from app.runtime_config import load_runtime_config


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("s7-plc-sim")
logging.getLogger("httpx").setLevel(logging.WARNING)


DEFAULT_ACTIVE_MAPPING_PATH = "/app/data/deployment-config/active/mapping.yaml"
DEFAULT_BASELINE_MAPPING_PATH = "/app/config/mapping.yaml"


def _runtime_db_number(mapping: Mapping[str, object]) -> int:
    plcs = mapping.get("plcs")
    if not isinstance(plcs, list) or len(plcs) != 1 or not isinstance(plcs[0], Mapping):
        raise ValueError("active runtime mapping must contain exactly one PLC")
    runtime_db = plcs[0].get("runtime_db")
    if type(runtime_db) is not int or runtime_db <= 0:
        runtime_db = (mapping.get("line") or {}).get("db_number") if isinstance(mapping.get("line"), Mapping) else None
    if type(runtime_db) is not int or runtime_db <= 0:
        raise ValueError("active runtime mapping runtime_db is invalid")
    return runtime_db


def _station_db_specs(mapping: Mapping[str, object]) -> dict[int, int]:
    raw_stations = mapping.get("stations")
    if not isinstance(raw_stations, list):
        raise ValueError("active runtime mapping stations must be a list")
    runtime_db = _runtime_db_number(mapping)
    specs: dict[int, int] = {}
    for station in raw_stations:
        if not isinstance(station, Mapping) or station.get("station_enabled", True) is False:
            continue
        db_number = station.get("db_number")
        if type(db_number) is not int or db_number <= 0:
            raise ValueError("active runtime mapping station db_number is invalid")
        if db_number == runtime_db:
            raise ValueError("active runtime mapping station DB conflicts with runtime DB")
        if db_number in specs:
            raise ValueError(f"duplicate active runtime station DB: {db_number}")
        read_size = station.get("effective_read_size_bytes", 512)
        if type(read_size) is not int or read_size <= 0:
            raise ValueError("active runtime mapping effective_read_size_bytes is invalid")
        specs[db_number] = max(512, read_size)
    if not specs:
        raise ValueError("active runtime mapping has no enabled stations")
    return specs


def _load_runtime_mapping(
    path: str | Path,
    *,
    fallback_path: str | Path = DEFAULT_BASELINE_MAPPING_PATH,
) -> tuple[dict[str, object], Path, str]:
    candidate = Path(path)
    fallback = Path(fallback_path)
    try:
        candidate_stat = candidate.lstat()
    except FileNotFoundError:
        selected = fallback
    except OSError as exc:
        raise ValueError(f"runtime mapping cannot be inspected: {candidate}") from exc
    else:
        selected = candidate
        if stat.S_ISLNK(candidate_stat.st_mode) or not stat.S_ISREG(candidate_stat.st_mode):
            raise ValueError("runtime mapping must be a regular non-symlink file")
    try:
        selected_stat = selected.lstat()
    except OSError as exc:
        raise ValueError(f"runtime mapping cannot be inspected: {selected}") from exc
    if stat.S_ISLNK(selected_stat.st_mode) or not stat.S_ISREG(selected_stat.st_mode):
        raise ValueError("runtime mapping must be a regular non-symlink file")
    selected = selected.resolve(strict=True)
    raw_bytes = selected.read_bytes()
    raw = yaml.safe_load(raw_bytes.decode("utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("runtime mapping root must be a mapping")
    return raw, selected, hashlib.sha256(raw_bytes).hexdigest()


def _runtime_plc_port(mapping: Mapping[str, object]) -> int:
    plcs = mapping.get("plcs")
    if not isinstance(plcs, list) or len(plcs) != 1 or not isinstance(plcs[0], Mapping):
        raise ValueError("active runtime mapping PLC selection is ambiguous")
    port = plcs[0].get("port")
    if type(port) is not int or not 1 <= port <= 65535:
        raise ValueError("active runtime mapping PLC port is invalid")
    return port


def main() -> None:
    legacy_mapping = load_mapping()
    legacy_plc_cfg = legacy_mapping.get("plc", {})
    runtime_mapping_path = os.environ.get("VPLC_MAPPING_PATH", DEFAULT_ACTIVE_MAPPING_PATH)
    active_mapping, active_mapping_file, active_mapping_sha256 = _load_runtime_mapping(
        runtime_mapping_path
    )
    runtime_db_number = _runtime_db_number(active_mapping)
    station_db_specs = _station_db_specs(active_mapping)
    db_number = int(legacy_plc_cfg.get("db_number", 100))
    db_size = max(int(legacy_plc_cfg.get("db_size", 64)), 64)
    port = _runtime_plc_port(active_mapping)
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
        active_mapping=active_mapping,
    )
    serial_start_text = os.environ.get("VPLC_SERIAL_START", "0")
    try:
        serial_start = int(serial_start_text)
    except ValueError as exc:
        raise ValueError("VPLC_SERIAL_START must be a non-negative integer") from exc
    if serial_start < 0:
        raise ValueError("VPLC_SERIAL_START must be a non-negative integer")
    if serial_start and runtime_config.profile != "test":
        raise ValueError("VPLC_SERIAL_START is only allowed with the test profile")
    ack_deadline_s = float(os.environ.get("VPLC_ACK_DEADLINE_SECONDS", "10"))
    runtime_state_path = os.environ.get("VPLC_RUNTIME_STATE_PATH", "/app/data/vplc_runtime.json")
    runtime_identity = LineRuntimeIdentity.load_or_start(runtime_state_path)
    audit_recorder = ParameterAuditRecorder(os.environ.get("DATABASE_URL"))

    db = bytearray(db_size)
    runtime_db = bytearray(64)
    station_dbs = {
        db_number: bytearray(read_size)
        for db_number, read_size in station_db_specs.items()
    }

    def reset_runtime_identity() -> None:
        runtime_identity.rotate_boot_id()
        runtime_db[:] = b"\x00" * len(runtime_db)
        for station_db in station_dbs.values():
            station_db[:] = b"\x00" * len(station_db)

    pipeline = SingleLinearRoutePipeline.from_mapping(
        active_mapping,
        scale=runtime_config.cycle_scale,
        ack_deadline_s=ack_deadline_s,
        on_counter_reset=reset_runtime_identity,
        profile=runtime_config.profile,
        allow_runtime_cycle_edit=runtime_config.allow_runtime_cycle_edit,
        station_parameters=runtime_config.station_dict(),
        config_source=str(active_mapping_file),
        config_hash=active_mapping_sha256,
        mapping_path=str(active_mapping_file),
        mapping_content_sha256=active_mapping_sha256,
        initial_serial_no=serial_start,
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
    registered_db_numbers = {db_number}
    if runtime_db_number not in registered_db_numbers:
        server.register_area(snap7_type.SrvArea.DB, runtime_db_number, runtime_db)
        registered_db_numbers.add(runtime_db_number)
    for station_db_number, station_db in station_dbs.items():
        if station_db_number in registered_db_numbers:
            raise ValueError(f"active station DB collides with registered DB: {station_db_number}")
        server.register_area(snap7_type.SrvArea.DB, station_db_number, station_db)
        registered_db_numbers.add(station_db_number)
    server.start(tcp_port=port)
    logger.info(
        "S7 PLC simulator started db=%s size=%s runtime_db=%s station_dbs=%s port=%s boot_id=%s restart_counter=%s ack_deadline_s=%s profile=%s scale=%s serial_start=%s mapping_path=%s mapping_sha256=%s config_hash=%s stations=%s",
        db_number,
        db_size,
        runtime_db_number,
        sorted(station_dbs),
        port,
        runtime_identity.plc_boot_id,
        runtime_identity.plc_restart_counter,
        ack_deadline_s,
        runtime_config.profile,
        runtime_config.cycle_scale,
        serial_start,
        active_mapping_file,
        active_mapping_sha256,
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
                write_state_to_db(db, payload, legacy_mapping)
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
                    "db%s legacy running=%s total=%s station_cycles=%s",
                    db_number,
                    payload.get("running"),
                    payload.get("total_count"),
                    ",".join(
                        f"{station_id}:{pipeline.stations[station_id].cycle_counter}"
                        for station_id in pipeline.topology.station_ids
                    ),
                )
            time.sleep(interval_ms / 1000)
    finally:
        server.stop()
        server.destroy()


if __name__ == "__main__":
    main()
