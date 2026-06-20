from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, replace
from typing import Any

from .models import LineConfig, LoadEstimate


def resolve_line_config(config: LineConfig) -> dict[str, Any]:
    return asdict(config)


def canonicalize_config(config: LineConfig) -> str:
    resolved = resolve_line_config(config)
    resolved.pop("config_hash", None)
    return json.dumps(
        resolved,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def compute_config_hash(config: LineConfig) -> str:
    hashless = replace(config, config_hash="")
    return hashlib.sha256(canonicalize_config(hashless).encode("utf-8")).hexdigest()


def estimate_config_load(config: LineConfig) -> LoadEstimate:
    mappings = [
        mapping for station in config.stations for mapping in station.db_mappings
    ]
    reads_per_second = sum(1000.0 / mapping.poll_interval_ms for mapping in mappings)
    estimated_read_bytes_per_second = sum(
        mapping.read_size_bytes * (1000.0 / mapping.poll_interval_ms)
        for mapping in mappings
    )
    profiles = {profile.profile_id: profile for profile in config.cycle_profiles}
    enabled_stations = [station for station in config.stations if station.station_enabled]
    event_rate = sum(
        1.0
        / (
            profiles[station.cycle_profile].simulation.stress_cycle_time_s
            or profiles[station.cycle_profile].simulation.base_cycle_s
        )
        for station in enabled_stations
    )
    payload_sizes = {
        template.template_id: template.approximate_size_bytes
        for template in config.payload_templates
    }
    payload_bytes = sum(
        (
            payload_sizes.get(station.payload_template, 0)
            * (
                1.0
                / (
                    profiles[station.cycle_profile].simulation.stress_cycle_time_s
                    or profiles[station.cycle_profile].simulation.base_cycle_s
                )
            )
        )
        for station in enabled_stations
    )
    return LoadEstimate(
        station_count=len(config.stations),
        mapping_count=len(mappings),
        reads_per_second=reads_per_second,
        estimated_read_bytes_per_second=estimated_read_bytes_per_second,
        estimated_event_rate_per_second=event_rate,
        estimated_payload_bytes_per_second=payload_bytes,
    )
