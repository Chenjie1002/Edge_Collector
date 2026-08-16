from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def _volume_entries(service: dict[str, object]) -> list[str]:
    return [str(item) for item in service.get("volumes", [])]


def test_vplc_and_collector_share_read_only_active_mapping_mount() -> None:
    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
    services = compose["services"]

    assert "./data/deployment-config:/app/data/deployment-config:ro" in _volume_entries(
        services["s7-plc-sim"]
    )
    assert "./data/deployment-config:/app/data/deployment-config:ro" in _volume_entries(
        services["collector"]
    )
    assert "./data/deployment-config:/app/data/deployment-config" in _volume_entries(
        services["api"]
    )
    assert services["s7-plc-sim"]["environment"]["VPLC_MAPPING_PATH"] == (
        "/app/data/deployment-config/active/mapping.yaml"
    )
    assert "SNAP7_HOST" not in services["collector"]["environment"]
    assert "SNAP7_PORT" not in services["collector"]["environment"]


def test_compose_does_not_expose_docker_socket_to_runtime_services() -> None:
    compose_text = (ROOT / "docker-compose.yml").read_text()
    assert "/var/run/docker.sock" not in compose_text
