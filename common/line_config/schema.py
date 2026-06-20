from __future__ import annotations


HARD_MAX_STATIONS = 20
HARD_MAX_DB_MAPPINGS_PER_STATION = 4

TOP_LEVEL_KEYS = {
    "schema_version",
    "config_version",
    "line_id",
    "name",
    "timezone",
    "scenario",
    "hardware_envelope",
    "route_graph",
    "plcs",
    "stations",
    "buffers",
    "payload_templates",
    "nok_templates",
    "cycle_profiles",
}
PLC_KEYS = {
    "plc_id",
    "runtime_db",
    "max_stations",
    "max_db_mappings_per_station",
}
STATION_KEYS = {
    "station_id",
    "station_order",
    "station_type",
    "station_enabled",
    "plc_id",
    "db_mappings",
    "payload_template",
    "nok_template",
    "cycle_profile",
    "cycle_time_s",
    "nok_rate",
}
MAPPING_KEYS = {
    "mapping_id",
    "plc_id",
    "station_id",
    "db_number",
    "usage",
    "direction",
    "mapping_type",
    "read_start",
    "read_size_bytes",
    "poll_interval_ms",
}
BUFFER_KEYS = {
    "buffer_id",
    "from_station_id",
    "to_station_id",
    "buffer_position",
    "buffer_type",
    "capacity",
    "enabled",
    "tracking_mode",
}
PAYLOAD_TEMPLATE_KEYS = {
    "version",
    "template_type",
    "compatible_station_types",
    "approximate_size_bytes",
    "fields",
}
PAYLOAD_FIELD_KEYS = {"name", "field_type", "offset", "length", "required", "direction"}
NOK_TEMPLATE_KEYS = {
    "version",
    "template_type",
    "compatible_station_types",
    "codes",
}
NOK_CODE_KEYS = {
    "code",
    "name",
    "category",
    "severity",
    "mode",
    "allow_random",
    "allow_force",
}
PROFILE_KEYS = {"mode", "ideal_cycle_time_s", "simulation"}
SIMULATION_KEYS = {
    "base_cycle_s",
    "jitter_s",
    "cycle_scale",
    "stress_cycle_time_s",
}
SCENARIO_KEYS = {
    "name",
    "scenario_type",
    "test_run_id",
    "random_seed",
    "global_nok_rate",
    "production",
}
HARDWARE_KEYS = {"target_hardware_class", "intended_load_class"}
ROUTE_KEYS = {"entry_station_id", "terminal_station_id", "edges"}
ROUTE_EDGE_KEYS = {"from_station_id", "to_station_id"}

STATION_TYPES = {
    "generic",
    "assembly",
    "screwdriving",
    "press",
    "test",
    "eol_test",
    "leak_test",
    "vision",
    "label",
    "pack",
    "manual_confirm",
}
BUFFER_TYPES = {"fifo", "pallet", "conveyor", "virtual"}
BUFFER_TRACKING_MODES = {"unit_id", "pallet_id", "counter_only"}
PROFILE_MODES = {"normal", "demo", "fast", "test", "stress", "synthetic"}
SCENARIO_TYPES = {"demo", "test", "stress", "synthetic"}
MAPPING_USAGES = {"status", "event", "payload", "payload_ext", "parameter", "diagnostic"}
MAPPING_DIRECTIONS = {"read", "read_write"}
MAPPING_TYPES = {"status", "event", "payload", "runtime"}
PAYLOAD_TEMPLATE_TYPES = {"status", "event_payload", "measurement_payload"}
PAYLOAD_FIELD_TYPES = {"bool", "int16", "int32", "uint16", "uint32", "float32", "string", "bytes"}
NOK_TEMPLATE_TYPES = {"quality", "process", "route_semantic"}
NOK_CATEGORIES = {"quality", "process", "system", "route"}
NOK_SEVERITIES = {"info", "warning", "error", "critical"}
NOK_MODES = {"random_simulated_nok", "forced_test_nok", "system_reserved"}
HARDWARE_CLASSES = {"local_dev", "raspberry_pi_5", "generic_edge"}
LOAD_CLASSES = {"demo", "medium", "stress"}

RESERVED_NOK_CODES = {30003}
