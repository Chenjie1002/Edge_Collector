from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlcConfig:
    plc_id: str
    runtime_db: int
    max_stations: int
    max_db_mappings_per_station: int


@dataclass(frozen=True)
class DbMapping:
    mapping_id: str
    plc_id: str
    station_id: str
    db_number: int
    usage: str
    direction: str
    mapping_type: str
    read_start: int
    read_size_bytes: int
    poll_interval_ms: int


@dataclass(frozen=True)
class StationConfig:
    station_id: str
    station_order: int
    station_type: str
    station_enabled: bool
    plc_id: str
    db_mappings: tuple[DbMapping, ...]
    payload_template: str | None
    nok_template: str
    cycle_profile: str
    cycle_time_s: float
    nok_rate: float | None
    effective_nok_rate: float


@dataclass(frozen=True)
class BufferConfig:
    buffer_id: str
    from_station_id: str
    to_station_id: str
    buffer_position: int
    buffer_type: str
    capacity: int | None
    enabled: bool
    tracking_mode: str


@dataclass(frozen=True)
class PayloadField:
    name: str
    field_type: str
    offset: int
    length: int
    required: bool
    direction: str


@dataclass(frozen=True)
class PayloadTemplate:
    template_id: str
    version: int
    template_type: str
    compatible_station_types: tuple[str, ...]
    approximate_size_bytes: int
    fields: tuple[PayloadField, ...]


@dataclass(frozen=True)
class NokCode:
    code: int
    name: str
    category: str
    severity: str
    mode: str
    allow_random: bool
    allow_force: bool


@dataclass(frozen=True)
class NokTemplate:
    template_id: str
    version: int
    template_type: str
    compatible_station_types: tuple[str, ...]
    codes: tuple[NokCode, ...]


@dataclass(frozen=True)
class SimulationTiming:
    base_cycle_s: float
    jitter_s: float
    cycle_scale: float
    stress_cycle_time_s: float | None


@dataclass(frozen=True)
class CycleProfile:
    profile_id: str
    mode: str
    ideal_cycle_time_s: float
    simulation: SimulationTiming


@dataclass(frozen=True)
class ScenarioConfig:
    name: str
    scenario_type: str
    test_run_id: str
    random_seed: int
    global_nok_rate: float
    production: bool


@dataclass(frozen=True)
class RouteEdge:
    from_station_id: str
    to_station_id: str


@dataclass(frozen=True)
class RouteGraph:
    entry_station_id: str
    terminal_station_id: str
    edges: tuple[RouteEdge, ...]


@dataclass(frozen=True)
class HardwareEnvelope:
    target_hardware_class: str
    intended_load_class: str


@dataclass(frozen=True)
class LoadEstimate:
    station_count: int
    mapping_count: int
    reads_per_second: float
    estimated_read_bytes_per_second: float
    estimated_event_rate_per_second: float
    estimated_payload_bytes_per_second: float


@dataclass(frozen=True)
class LineConfig:
    schema_version: int
    config_version: str
    config_hash: str
    line_id: str
    name: str
    timezone: str
    scenario: ScenarioConfig
    hardware_envelope: HardwareEnvelope
    route_graph: RouteGraph
    plcs: tuple[PlcConfig, ...]
    stations: tuple[StationConfig, ...]
    buffers: tuple[BufferConfig, ...]
    payload_templates: tuple[PayloadTemplate, ...]
    nok_templates: tuple[NokTemplate, ...]
    cycle_profiles: tuple[CycleProfile, ...]
