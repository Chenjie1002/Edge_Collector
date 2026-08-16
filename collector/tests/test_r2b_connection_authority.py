from __future__ import annotations

import hashlib
import os
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from app.services import event_collector as event_collector_module
from app.services.event_collector import CollectorStartupContext, EventCollectorWorker
from app.sources import snap7_source as snap7_source_module
from app.sources.snap7_source import Snap7Source


def _write_overlay(root: Path, **plc_overrides: object) -> Path:
    baseline = Path("config/mapping.yaml")
    document = yaml.safe_load(baseline.read_text(encoding="utf-8"))
    document["plcs"][0].update(plc_overrides)
    destination = root / "active" / "mapping.yaml"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return destination


class _ConnectionClient:
    def __init__(self) -> None:
        self.parameters: list[tuple[object, int]] = []
        self.connections: list[tuple[str, int, int, int]] = []

    def set_param(self, parameter: object, value: int) -> None:
        self.parameters.append((parameter, value))

    def get_connected(self) -> bool:
        return False

    def connect(self, host: str, rack: int, slot: int, *, tcp_port: int) -> None:
        self.connections.append((host, rack, slot, tcp_port))


def test_event_worker_uses_effective_mapping_tuple_and_loaded_overlay_identity(tmp_path: Path) -> None:
    overlay = _write_overlay(
        tmp_path,
        host="s7-plc-sim",
        port=1102,
        rack=0,
        slot=1,
        connection_timeout_ms=2500,
        poll_interval_ms=234,
    )
    client = _ConnectionClient()
    context = CollectorStartupContext(
        collector_main_started_at_utc="2026-08-16T03:00:00Z",
        process_pid=os.getpid(),
    )

    with patch.dict(os.environ, {"DEPLOYMENT_CONFIG_DIR": str(tmp_path)}, clear=False), patch.object(
        event_collector_module.snap7.client,
        "Client",
        return_value=client,
    ), patch.object(event_collector_module.logger, "info"):
        worker = EventCollectorWorker(
            dsn="postgresql://unused",
            host="environment-host-must-not-win",
            port=9999,
            mapping_path="config/mapping.yaml",
            startup_context=context,
        )
        worker._ensure_connected()

    assert worker.host == "s7-plc-sim"
    assert worker.port == 1102
    assert worker.rack == 0
    assert worker.slot == 1
    assert worker.connection_timeout_ms == 2500
    assert worker.poll_interval_ms == 234
    assert worker.mapping.mapping_path == str(overlay.resolve())
    assert worker.mapping.mapping_content_sha256 == hashlib.sha256(overlay.read_bytes()).hexdigest()
    assert client.connections == [("s7-plc-sim", 0, 1, 1102)]
    assert client.parameters
    assert client.parameters[-1][1] == 2500


def test_snap7_source_uses_effective_mapping_connection_authority(tmp_path: Path) -> None:
    _write_overlay(tmp_path, host="s7-plc-sim", port=1102, rack=0, slot=1)
    legacy_mapping = {
        "plc": {
            "host": "legacy-host-must-not-win",
            "port": 9999,
            "rack": 7,
            "slot": 7,
            "db_number": 100,
            "db_size": 64,
        },
        "code_tables": {"product_type": {}, "shift": {}},
    }

    with patch.dict(os.environ, {"DEPLOYMENT_CONFIG_DIR": str(tmp_path)}, clear=False), patch.object(
        snap7_source_module,
        "load_mapping",
        return_value=legacy_mapping,
    ), patch.object(snap7_source_module.snap7.client, "Client", return_value=object()):
        source = Snap7Source("environment-host-must-not-win", 9999)

    assert (source.host, source.port, source.rack, source.slot) == ("s7-plc-sim", 1102, 0, 1)
    assert (source.db_number, source.db_size) == (100, 64)


def test_invalid_active_mapping_prevents_collector_startup_instead_of_falling_back(tmp_path: Path) -> None:
    destination = tmp_path / "active" / "mapping.yaml"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("plcs: [", encoding="utf-8")

    context = CollectorStartupContext(
        collector_main_started_at_utc="2026-08-16T03:00:00Z",
        process_pid=os.getpid(),
    )
    with patch.dict(os.environ, {"DEPLOYMENT_CONFIG_DIR": str(tmp_path)}, clear=False):
        with pytest.raises(Exception):
            EventCollectorWorker(
                dsn="postgresql://unused",
                host="environment-host",
                port=9999,
                mapping_path="config/mapping.yaml",
                startup_context=context,
            )
