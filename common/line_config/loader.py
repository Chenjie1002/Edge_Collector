from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
from typing import Any

import yaml

from .models import (
    BufferConfig,
    CycleProfile,
    DbMapping,
    HardwareEnvelope,
    LineConfig,
    NokCode,
    NokTemplate,
    PayloadField,
    PayloadTemplate,
    PlcConfig,
    RouteEdge,
    RouteGraph,
    ScenarioConfig,
    SimulationTiming,
    StationConfig,
)
from .resolver import compute_config_hash
from .validator import validate_line_config


class LineConfigError(ValueError):
    """Raised when a line configuration cannot be loaded or validated."""


def load_line_config(path: str | Path) -> LineConfig:
    config_path = Path(path)
    if not config_path.is_file():
        raise LineConfigError(f"line config file does not exist: {config_path}")

    try:
        raw = yaml.safe_load(config_path.read_text())
    except yaml.YAMLError as exc:
        raise LineConfigError(f"invalid YAML in {config_path}: {exc}") from exc

    if not isinstance(raw, Mapping):
        raise LineConfigError("line config root must be a mapping")

    errors = validate_line_config(raw)
    if errors:
        raise LineConfigError("line config validation failed:\n- " + "\n- ".join(errors))

    config = _build_line_config(raw)
    return replace(config, config_hash=compute_config_hash(config))


def _build_line_config(raw: Mapping[str, Any]) -> LineConfig:
    scenario_raw = raw["scenario"]
    scenario = ScenarioConfig(
        name=scenario_raw["name"],
        scenario_type=scenario_raw["scenario_type"],
        test_run_id=scenario_raw["test_run_id"],
        random_seed=scenario_raw["random_seed"],
        global_nok_rate=float(scenario_raw["global_nok_rate"]),
        production=scenario_raw["production"],
    )
    hardware_raw = raw["hardware_envelope"]
    hardware = HardwareEnvelope(
        target_hardware_class=hardware_raw["target_hardware_class"],
        intended_load_class=hardware_raw["intended_load_class"],
    )
    route_raw = raw["route_graph"]
    route = RouteGraph(
        entry_station_id=route_raw["entry_station_id"],
        terminal_station_id=route_raw["terminal_station_id"],
        edges=tuple(
            RouteEdge(
                from_station_id=edge["from_station_id"],
                to_station_id=edge["to_station_id"],
            )
            for edge in route_raw["edges"]
        ),
    )
    payload_templates = tuple(
        PayloadTemplate(
            template_id=template_id,
            version=template["version"],
            template_type=template["template_type"],
            compatible_station_types=tuple(template["compatible_station_types"]),
            approximate_size_bytes=template["approximate_size_bytes"],
            fields=tuple(
                PayloadField(
                    name=field["name"],
                    field_type=field["field_type"],
                    offset=field["offset"],
                    length=field["length"],
                    required=field["required"],
                    direction=field["direction"],
                )
                for field in template["fields"]
            ),
        )
        for template_id, template in sorted(raw["payload_templates"].items())
    )
    nok_templates = tuple(
        NokTemplate(
            template_id=template_id,
            version=template["version"],
            template_type=template["template_type"],
            compatible_station_types=tuple(template["compatible_station_types"]),
            codes=tuple(
                NokCode(
                    code=code["code"],
                    name=code["name"],
                    category=code["category"],
                    severity=code["severity"],
                    mode=code["mode"],
                    allow_random=code["allow_random"],
                    allow_force=code["allow_force"],
                )
                for code in template["codes"]
            ),
        )
        for template_id, template in sorted(raw["nok_templates"].items())
    )
    cycle_profiles = tuple(
        CycleProfile(
            profile_id=profile_id,
            mode=profile["mode"],
            ideal_cycle_time_s=float(profile["ideal_cycle_time_s"]),
            simulation=SimulationTiming(
                base_cycle_s=float(profile["simulation"]["base_cycle_s"]),
                jitter_s=float(profile["simulation"]["jitter_s"]),
                cycle_scale=float(profile["simulation"]["cycle_scale"]),
                stress_cycle_time_s=(
                    float(profile["simulation"]["stress_cycle_time_s"])
                    if profile["simulation"].get("stress_cycle_time_s") is not None
                    else None
                ),
            ),
        )
        for profile_id, profile in sorted(raw["cycle_profiles"].items())
    )
    plcs = tuple(
        PlcConfig(
            plc_id=plc["plc_id"],
            runtime_db=plc["runtime_db"],
            max_stations=plc["max_stations"],
            max_db_mappings_per_station=plc["max_db_mappings_per_station"],
        )
        for plc in sorted(raw["plcs"], key=lambda item: item["plc_id"])
    )
    stations = tuple(
        StationConfig(
            station_id=station["station_id"],
            station_order=station["station_order"],
            station_type=station["station_type"],
            station_enabled=station.get("station_enabled", True),
            plc_id=station["plc_id"],
            db_mappings=tuple(
                DbMapping(
                    mapping_id=mapping["mapping_id"],
                    plc_id=mapping["plc_id"],
                    station_id=mapping["station_id"],
                    db_number=mapping["db_number"],
                    usage=mapping["usage"],
                    direction=mapping["direction"],
                    mapping_type=mapping["mapping_type"],
                    read_start=mapping["read_start"],
                    read_size_bytes=mapping["read_size_bytes"],
                    poll_interval_ms=mapping["poll_interval_ms"],
                )
                for mapping in sorted(
                    station["db_mappings"], key=lambda item: item["mapping_id"]
                )
            ),
            payload_template=station.get("payload_template"),
            nok_template=station["nok_template"],
            cycle_profile=station["cycle_profile"],
            cycle_time_s=float(station["cycle_time_s"]),
            nok_rate=(
                float(station["nok_rate"]) if station.get("nok_rate") is not None else None
            ),
            effective_nok_rate=(
                float(station["nok_rate"])
                if station.get("nok_rate") is not None
                else scenario.global_nok_rate
            ),
        )
        for station in sorted(raw["stations"], key=lambda item: item["station_order"])
    )
    buffers = tuple(
        BufferConfig(
            buffer_id=buffer["buffer_id"],
            from_station_id=buffer["from_station_id"],
            to_station_id=buffer["to_station_id"],
            buffer_position=buffer["buffer_position"],
            buffer_type=buffer["buffer_type"],
            capacity=buffer.get("capacity"),
            enabled=buffer.get("enabled", True),
            tracking_mode=buffer.get("tracking_mode", "counter_only"),
        )
        for buffer in sorted(raw["buffers"], key=lambda item: item["buffer_id"])
    )
    return LineConfig(
        schema_version=raw["schema_version"],
        config_version=raw["config_version"],
        config_hash="",
        line_id=raw["line_id"],
        name=raw["name"],
        timezone=raw["timezone"],
        scenario=scenario,
        hardware_envelope=hardware,
        route_graph=route,
        plcs=plcs,
        stations=stations,
        buffers=buffers,
        payload_templates=payload_templates,
        nok_templates=nok_templates,
        cycle_profiles=cycle_profiles,
    )
