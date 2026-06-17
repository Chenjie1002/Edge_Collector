from __future__ import annotations

import os
from pathlib import Path

import yaml


def load_config() -> dict:
    path = Path("/app/config/app.yaml")
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def database_url() -> str:
    return os.environ.get("DATABASE_URL", "postgresql://edge_mes:edge_mes_password@localhost:5432/edge_mes")


def simulator_url() -> str:
    return os.environ.get("SIMULATOR_URL", "http://localhost:8100")


def snap7_host() -> str:
    return os.environ.get("SNAP7_HOST", "s7-plc-sim")


def snap7_port() -> int:
    return int(os.environ.get("SNAP7_PORT", "1102"))


def event_collector_enabled() -> bool:
    return os.environ.get("EVENT_COLLECTOR_ENABLED", "true").lower() == "true"
