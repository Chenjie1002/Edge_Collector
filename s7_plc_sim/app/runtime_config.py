from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


STATION_IDS = ("WS01", "WS02", "WS03")

SAFE_DEFAULTS: dict[str, Any] = {
    "profile": "normal",
    "stations": {
        "WS01": {"base_cycle_s": 30.4, "jitter_s": 1.2, "nok_rate": 0.02},
        "WS02": {"base_cycle_s": 29.8, "jitter_s": 1.0, "nok_rate": 0.015},
        "WS03": {"base_cycle_s": 29.2, "jitter_s": 0.9, "nok_rate": 0.01},
    },
    "profiles": {
        "normal": {"cycle_scale": 1.0, "allow_runtime_cycle_edit": False},
        "fast": {"cycle_scale": 0.1, "allow_runtime_cycle_edit": True},
        "test": {"cycle_scale": 0.05, "allow_runtime_cycle_edit": True},
    },
}


@dataclass(frozen=True)
class StationParameters:
    base_cycle_s: float
    jitter_s: float
    nok_rate: float


@dataclass(frozen=True)
class ResolvedRuntimeConfig:
    profile: str
    cycle_scale: float
    allow_runtime_cycle_edit: bool
    stations: dict[str, StationParameters]
    source: str
    config_hash: str

    def station_dict(self) -> dict[str, dict[str, float]]:
        return {station_id: asdict(params) for station_id, params in self.stations.items()}

    def as_dict(self) -> dict[str, object]:
        return {
            "profile": self.profile,
            "cycle_scale": self.cycle_scale,
            "allow_runtime_cycle_edit": self.allow_runtime_cycle_edit,
            "stations": self.station_dict(),
            "source": self.source,
            "config_hash": self.config_hash,
        }


def load_runtime_config(
    path: str | Path = "/app/config/vplc.yaml",
    *,
    profile_override: str | None = None,
    cycle_scale_override: float | None = None,
) -> ResolvedRuntimeConfig:
    config_path = Path(path)
    if config_path.exists():
        raw = yaml.safe_load(config_path.read_text()) or {}
        source = str(config_path)
    else:
        raw = SAFE_DEFAULTS
        source = "built-in-safe-defaults"

    profile = str(profile_override or raw.get("profile") or "normal").lower()
    profiles = raw.get("profiles") or {}
    if profile not in profiles:
        raise ValueError(f"unsupported V-PLC profile: {profile}")
    profile_data = profiles[profile] or {}
    cycle_scale = float(
        cycle_scale_override
        if cycle_scale_override is not None
        else profile_data.get("cycle_scale", SAFE_DEFAULTS["profiles"][profile]["cycle_scale"])
    )
    allow_runtime_cycle_edit = bool(profile_data.get("allow_runtime_cycle_edit", False))

    raw_stations = raw.get("stations") or {}
    stations: dict[str, StationParameters] = {}
    for station_id in STATION_IDS:
        if station_id not in raw_stations:
            raise ValueError(f"missing V-PLC station configuration: {station_id}")
        item = raw_stations[station_id] or {}
        params = StationParameters(
            base_cycle_s=float(item["base_cycle_s"]),
            jitter_s=float(item["jitter_s"]),
            nok_rate=float(item["nok_rate"]),
        )
        _validate_station(station_id, params, profile)
        stations[station_id] = params

    if profile == "normal" and cycle_scale != 1.0:
        raise ValueError("normal profile requires cycle_scale=1.0")
    if cycle_scale <= 0:
        raise ValueError("cycle_scale must be greater than zero")

    resolved_payload = {
        "profile": profile,
        "cycle_scale": cycle_scale,
        "allow_runtime_cycle_edit": allow_runtime_cycle_edit,
        "stations": {key: asdict(value) for key, value in stations.items()},
        "source": source,
    }
    config_hash = hashlib.sha256(
        json.dumps(resolved_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return ResolvedRuntimeConfig(
        profile=profile,
        cycle_scale=cycle_scale,
        allow_runtime_cycle_edit=allow_runtime_cycle_edit,
        stations=stations,
        source=source,
        config_hash=config_hash,
    )


def _validate_station(station_id: str, params: StationParameters, profile: str) -> None:
    if not 0 <= params.jitter_s <= 60:
        raise ValueError(f"{station_id} jitter_s must be between 0 and 60")
    if not 0 <= params.nok_rate <= 1:
        raise ValueError(f"{station_id} nok_rate must be between 0 and 1")
    if not 1 <= params.base_cycle_s <= 300:
        raise ValueError(f"{station_id} base_cycle_s must be between 1 and 300")
    if profile == "normal":
        if not 20 <= params.base_cycle_s <= 60:
            raise ValueError(f"{station_id} base_cycle_s is unsafe for normal profile")
        if not 0 <= params.jitter_s <= 10:
            raise ValueError(f"{station_id} jitter_s is unsafe for normal profile")
