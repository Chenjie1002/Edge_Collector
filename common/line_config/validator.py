from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Mapping
from typing import Any

from . import schema


def validate_line_config(raw: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    _unknown(raw, schema.TOP_LEVEL_KEYS, "", errors)

    _positive_int(raw, "schema_version", "schema_version", errors)
    _required_text(raw, "config_version", "config_version", errors)
    _required_text(raw, "line_id", "line_id", errors)
    _required_text(raw, "name", "name", errors)
    _required_text(raw, "timezone", "timezone", errors)

    scenario = _mapping(raw, "scenario", "scenario", errors)
    hardware = _mapping(raw, "hardware_envelope", "hardware_envelope", errors)
    route = _mapping(raw, "route_graph", "route_graph", errors)
    plcs = _list(raw, "plcs", "plcs", errors)
    stations = _list(raw, "stations", "stations", errors)
    buffers = _list(raw, "buffers", "buffers", errors)
    payload_templates = _mapping(raw, "payload_templates", "payload_templates", errors)
    nok_templates = _mapping(raw, "nok_templates", "nok_templates", errors)
    cycle_profiles = _mapping(raw, "cycle_profiles", "cycle_profiles", errors)

    _validate_scenario(scenario, errors)
    _validate_hardware(hardware, errors)

    plc_by_id: dict[str, Mapping[str, Any]] = {}
    runtime_dbs: set[tuple[str, int]] = set()
    for index, plc in enumerate(plcs):
        path = f"plcs[{index}]"
        if not isinstance(plc, Mapping):
            errors.append(f"{path} must be a mapping")
            continue
        _unknown(plc, schema.PLC_KEYS, path, errors)
        plc_id = _required_text(plc, "plc_id", f"{path}.plc_id", errors)
        runtime_db = _positive_int(plc, "runtime_db", f"{path}.runtime_db", errors)
        max_stations = _positive_int(plc, "max_stations", f"{path}.max_stations", errors)
        max_mappings = _positive_int(
            plc,
            "max_db_mappings_per_station",
            f"{path}.max_db_mappings_per_station",
            errors,
        )
        if max_stations is not None and max_stations > schema.HARD_MAX_STATIONS:
            errors.append(
                f"{path}.max_stations exceeds hard maximum {schema.HARD_MAX_STATIONS}"
            )
        if max_mappings is not None and max_mappings > schema.HARD_MAX_DB_MAPPINGS_PER_STATION:
            errors.append(
                f"{path}.max_db_mappings_per_station exceeds hard maximum "
                f"{schema.HARD_MAX_DB_MAPPINGS_PER_STATION}"
            )
        if plc_id:
            if plc_id in plc_by_id:
                errors.append(f"duplicate plc_id '{plc_id}'")
            plc_by_id[plc_id] = plc
            if runtime_db is not None:
                runtime_dbs.add((plc_id, runtime_db))

    _validate_payload_templates(payload_templates, errors)
    _validate_nok_templates(nok_templates, errors)
    _validate_profiles(cycle_profiles, errors)

    station_ids: list[str] = []
    station_orders: list[int] = []
    station_by_id: dict[str, Mapping[str, Any]] = {}
    stations_by_plc: dict[str, int] = defaultdict(int)
    mapping_ids: set[str] = set()
    db_owners: dict[tuple[str, int], str] = {}

    if len(stations) > schema.HARD_MAX_STATIONS:
        errors.append(
            f"station count {len(stations)} exceeds hard maximum {schema.HARD_MAX_STATIONS}"
        )

    global_nok_rate = scenario.get("global_nok_rate")
    for index, station in enumerate(stations):
        path = f"stations[{index}]"
        if not isinstance(station, Mapping):
            errors.append(f"{path} must be a mapping")
            continue
        _unknown(station, schema.STATION_KEYS, path, errors)
        station_id = _required_text(station, "station_id", f"{path}.station_id", errors)
        station_order = _positive_int(
            station, "station_order", f"{path}.station_order", errors
        )
        station_type = _enum(
            station, "station_type", f"{path}.station_type", schema.STATION_TYPES, errors
        )
        plc_id = _required_text(station, "plc_id", f"{path}.plc_id", errors)
        enabled = station.get("station_enabled", True)
        if not isinstance(enabled, bool):
            errors.append(f"{path}.station_enabled must be a boolean")

        if station_id:
            station_ids.append(station_id)
            station_by_id[station_id] = station
        if station_order is not None:
            station_orders.append(station_order)
        if plc_id:
            stations_by_plc[plc_id] += 1
            if plc_id not in plc_by_id:
                errors.append(f"{path}.plc_id '{plc_id}' does not exist")

        cycle_time = station.get("cycle_time_s")
        if not _is_positive_number(cycle_time):
            errors.append(f"{path}.cycle_time_s must be positive")
        nok_rate = station.get("nok_rate")
        if nok_rate is not None and not _rate(nok_rate):
            errors.append(f"{path}.nok_rate must be between 0 and 1")
        if nok_rate is None and not _rate(global_nok_rate):
            errors.append(f"{path}.nok_rate has no valid scenario.global_nok_rate fallback")

        payload_ref = station.get("payload_template")
        if payload_ref is not None:
            if not isinstance(payload_ref, str) or not payload_ref.strip():
                errors.append(f"{path}.payload_template must be text or null")
            elif payload_ref not in payload_templates:
                errors.append(f"{path}.payload_template '{payload_ref}' does not exist")
            elif station_type and not _template_supports(
                payload_templates[payload_ref], station_type
            ):
                errors.append(
                    f"{path}.payload_template '{payload_ref}' is not compatible "
                    f"with station_type '{station_type}'"
                )

        nok_ref = _required_text(station, "nok_template", f"{path}.nok_template", errors)
        if nok_ref:
            if nok_ref not in nok_templates:
                errors.append(f"{path}.nok_template '{nok_ref}' does not exist")
            elif station_type and not _template_supports(nok_templates[nok_ref], station_type):
                errors.append(
                    f"{path}.nok_template '{nok_ref}' is not compatible "
                    f"with station_type '{station_type}'"
                )

        profile_ref = _required_text(
            station, "cycle_profile", f"{path}.cycle_profile", errors
        )
        if profile_ref:
            if profile_ref not in cycle_profiles:
                errors.append(f"{path}.cycle_profile '{profile_ref}' does not exist")
            elif _is_positive_number(cycle_time):
                ideal = cycle_profiles[profile_ref].get("ideal_cycle_time_s")
                if _is_positive_number(ideal) and float(cycle_time) != float(ideal):
                    errors.append(
                        f"{path}.cycle_time_s must equal production ideal cycle time "
                        f"{float(ideal)}; simulation timing belongs in cycle_profiles"
                    )

        mappings = station.get("db_mappings")
        if not isinstance(mappings, list) or not mappings:
            errors.append(f"{path}.db_mappings must contain at least one mapping")
            continue
        if len(mappings) > schema.HARD_MAX_DB_MAPPINGS_PER_STATION:
            errors.append(
                f"{path}.db_mappings count {len(mappings)} exceeds hard maximum "
                f"{schema.HARD_MAX_DB_MAPPINGS_PER_STATION}"
            )
        declared_limit = plc_by_id.get(plc_id, {}).get("max_db_mappings_per_station")
        if isinstance(declared_limit, int) and len(mappings) > declared_limit:
            errors.append(
                f"{path}.db_mappings count {len(mappings)} exceeds "
                f"max_db_mappings_per_station {declared_limit}"
            )

        for mapping_index, db_mapping in enumerate(mappings):
            mapping_path = f"{path}.db_mappings[{mapping_index}]"
            if not isinstance(db_mapping, Mapping):
                errors.append(f"{mapping_path} must be a mapping")
                continue
            _unknown(db_mapping, schema.MAPPING_KEYS, mapping_path, errors)
            mapping_id = _required_text(
                db_mapping, "mapping_id", f"{mapping_path}.mapping_id", errors
            )
            mapping_plc = _required_text(
                db_mapping, "plc_id", f"{mapping_path}.plc_id", errors
            )
            mapping_station = _required_text(
                db_mapping, "station_id", f"{mapping_path}.station_id", errors
            )
            db_number = _positive_int(
                db_mapping, "db_number", f"{mapping_path}.db_number", errors
            )
            _enum(db_mapping, "usage", f"{mapping_path}.usage", schema.MAPPING_USAGES, errors)
            _enum(
                db_mapping,
                "direction",
                f"{mapping_path}.direction",
                schema.MAPPING_DIRECTIONS,
                errors,
            )
            _enum(
                db_mapping,
                "mapping_type",
                f"{mapping_path}.mapping_type",
                schema.MAPPING_TYPES,
                errors,
            )
            _nonnegative_int(
                db_mapping, "read_start", f"{mapping_path}.read_start", errors
            )
            _positive_int(
                db_mapping,
                "read_size_bytes",
                f"{mapping_path}.read_size_bytes",
                errors,
            )
            _positive_int(
                db_mapping,
                "poll_interval_ms",
                f"{mapping_path}.poll_interval_ms",
                errors,
            )
            if mapping_id:
                if mapping_id in mapping_ids:
                    errors.append(f"duplicate mapping_id '{mapping_id}'")
                mapping_ids.add(mapping_id)
            if mapping_plc:
                if mapping_plc not in plc_by_id:
                    errors.append(f"{mapping_path}.plc_id '{mapping_plc}' does not exist")
                if plc_id and mapping_plc != plc_id:
                    errors.append(
                        f"{mapping_path}.plc_id '{mapping_plc}' must match station plc_id '{plc_id}'"
                    )
            if mapping_station and station_id and mapping_station != station_id:
                errors.append(
                    f"{mapping_path}.station_id '{mapping_station}' must match '{station_id}'"
                )
            if mapping_plc and db_number is not None:
                if (mapping_plc, db_number) in runtime_dbs:
                    errors.append(
                        f"DB {db_number} on PLC '{mapping_plc}' conflicts with runtime_db"
                    )
                key = (mapping_plc, db_number)
                owner = db_owners.get(key)
                if owner:
                    errors.append(
                        f"DB {db_number} conflicts on PLC '{mapping_plc}' between "
                        f"'{owner}' and '{mapping_id or mapping_path}'"
                    )
                else:
                    db_owners[key] = mapping_id or mapping_path

    for station_id, count in Counter(station_ids).items():
        if count > 1:
            errors.append(f"duplicate station_id '{station_id}'")
    for station_order, count in Counter(station_orders).items():
        if count > 1:
            errors.append(f"duplicate station_order {station_order}")
    for plc_id, count in stations_by_plc.items():
        if count > schema.HARD_MAX_STATIONS:
            errors.append(
                f"PLC '{plc_id}' station count {count} exceeds hard maximum "
                f"{schema.HARD_MAX_STATIONS}"
            )
        limit = plc_by_id.get(plc_id, {}).get("max_stations")
        if isinstance(limit, int) and count > limit:
            errors.append(
                f"PLC '{plc_id}' station count {count} exceeds max_stations {limit}"
            )

    _validate_buffers(buffers, station_by_id, errors)
    _validate_route(route, station_by_id, errors)
    return errors


def _validate_scenario(value: Mapping[str, Any], errors: list[str]) -> None:
    _unknown(value, schema.SCENARIO_KEYS, "scenario", errors)
    _required_text(value, "name", "scenario.name", errors)
    _enum(value, "scenario_type", "scenario.scenario_type", schema.SCENARIO_TYPES, errors)
    _required_text(value, "test_run_id", "scenario.test_run_id", errors)
    seed = value.get("random_seed")
    if not isinstance(seed, int) or isinstance(seed, bool) or seed < 0:
        errors.append("scenario.random_seed must be a non-negative integer")
    if not _rate(value.get("global_nok_rate")):
        errors.append("scenario.global_nok_rate must be between 0 and 1")
    if not isinstance(value.get("production"), bool):
        errors.append("scenario.production must be a boolean")
    if value.get("scenario_type") in {"stress", "synthetic"} and value.get("production") is not False:
        errors.append("scenario.production must be false for stress/synthetic scenarios")


def _validate_hardware(value: Mapping[str, Any], errors: list[str]) -> None:
    _unknown(value, schema.HARDWARE_KEYS, "hardware_envelope", errors)
    _enum(
        value,
        "target_hardware_class",
        "hardware_envelope.target_hardware_class",
        schema.HARDWARE_CLASSES,
        errors,
    )
    _enum(
        value,
        "intended_load_class",
        "hardware_envelope.intended_load_class",
        schema.LOAD_CLASSES,
        errors,
    )


def _validate_payload_templates(
    templates: Mapping[str, Any], errors: list[str]
) -> None:
    for template_id, template in templates.items():
        path = f"payload_templates.{template_id}"
        if not isinstance(template, Mapping):
            errors.append(f"{path} must be a mapping")
            continue
        _unknown(template, schema.PAYLOAD_TEMPLATE_KEYS, path, errors)
        _positive_int(template, "version", f"{path}.version", errors)
        _enum(
            template,
            "template_type",
            f"{path}.template_type",
            schema.PAYLOAD_TEMPLATE_TYPES,
            errors,
        )
        compatibles = template.get("compatible_station_types")
        if not isinstance(compatibles, list) or not compatibles:
            errors.append(f"{path}.compatible_station_types must not be empty")
        else:
            for index, station_type in enumerate(compatibles):
                if station_type not in schema.STATION_TYPES:
                    errors.append(
                        f"{path}.compatible_station_types[{index}] must be a supported station_type"
                    )
        approximate_size = _positive_int(
            template,
            "approximate_size_bytes",
            f"{path}.approximate_size_bytes",
            errors,
        )
        fields = template.get("fields")
        if not isinstance(fields, list) or not fields:
            errors.append(f"{path}.fields must contain at least one field")
            continue
        names: set[str] = set()
        max_end = 0
        for index, field in enumerate(fields):
            field_path = f"{path}.fields[{index}]"
            if not isinstance(field, Mapping):
                errors.append(f"{field_path} must be a mapping")
                continue
            _unknown(field, schema.PAYLOAD_FIELD_KEYS, field_path, errors)
            name = _required_text(field, "name", f"{field_path}.name", errors)
            _enum(
                field,
                "field_type",
                f"{field_path}.field_type",
                schema.PAYLOAD_FIELD_TYPES,
                errors,
            )
            offset = _nonnegative_int(field, "offset", f"{field_path}.offset", errors)
            length = _positive_int(field, "length", f"{field_path}.length", errors)
            if not isinstance(field.get("required"), bool):
                errors.append(f"{field_path}.required must be a boolean")
            _enum(
                field,
                "direction",
                f"{field_path}.direction",
                schema.MAPPING_DIRECTIONS,
                errors,
            )
            if name:
                if name in names:
                    errors.append(f"{path}.fields contains duplicate name '{name}'")
                names.add(name)
            if offset is not None and length is not None:
                max_end = max(max_end, offset + length)
        if approximate_size is not None and max_end > approximate_size:
            errors.append(f"{path}.fields exceed approximate_size_bytes")


def _validate_nok_templates(templates: Mapping[str, Any], errors: list[str]) -> None:
    for template_id, template in templates.items():
        path = f"nok_templates.{template_id}"
        if not isinstance(template, Mapping):
            errors.append(f"{path} must be a mapping")
            continue
        _unknown(template, schema.NOK_TEMPLATE_KEYS, path, errors)
        _positive_int(template, "version", f"{path}.version", errors)
        _enum(
            template,
            "template_type",
            f"{path}.template_type",
            schema.NOK_TEMPLATE_TYPES,
            errors,
        )
        compatibles = template.get("compatible_station_types")
        if not isinstance(compatibles, list) or not compatibles:
            errors.append(f"{path}.compatible_station_types must not be empty")
        codes = template.get("codes")
        if not isinstance(codes, list) or not codes:
            errors.append(f"{path}.codes must not be empty")
            continue
        seen: set[int] = set()
        for index, code_config in enumerate(codes):
            code_path = f"{path}.codes[{index}]"
            if not isinstance(code_config, Mapping):
                errors.append(f"{code_path} must be a mapping")
                continue
            _unknown(code_config, schema.NOK_CODE_KEYS, code_path, errors)
            code = _positive_int(code_config, "code", f"{code_path}.code", errors)
            _required_text(code_config, "name", f"{code_path}.name", errors)
            _enum(
                code_config, "category", f"{code_path}.category", schema.NOK_CATEGORIES, errors
            )
            _enum(
                code_config, "severity", f"{code_path}.severity", schema.NOK_SEVERITIES, errors
            )
            mode = _enum(
                code_config, "mode", f"{code_path}.mode", schema.NOK_MODES, errors
            )
            allow_random = code_config.get("allow_random")
            allow_force = code_config.get("allow_force")
            if not isinstance(allow_random, bool):
                errors.append(f"{code_path}.allow_random must be a boolean")
            if not isinstance(allow_force, bool):
                errors.append(f"{code_path}.allow_force must be a boolean")
            if code is not None:
                if code in seen:
                    errors.append(f"{path}.codes contains duplicate code {code}")
                seen.add(code)
                if code in schema.RESERVED_NOK_CODES and (
                    mode != "system_reserved" or allow_random or allow_force
                ):
                    errors.append(
                        f"{code_path} reserved code {code} cannot be used by random or forced NOK"
                    )
            if mode == "forced_test_nok" and allow_force is not True:
                errors.append(f"{code_path} forced_test_nok requires allow_force=true")
            if mode == "random_simulated_nok" and allow_random is not True:
                errors.append(f"{code_path} random_simulated_nok requires allow_random=true")


def _validate_profiles(profiles: Mapping[str, Any], errors: list[str]) -> None:
    for profile_id, profile in profiles.items():
        path = f"cycle_profiles.{profile_id}"
        if not isinstance(profile, Mapping):
            errors.append(f"{path} must be a mapping")
            continue
        _unknown(profile, schema.PROFILE_KEYS, path, errors)
        mode = _enum(profile, "mode", f"{path}.mode", schema.PROFILE_MODES, errors)
        ideal = profile.get("ideal_cycle_time_s")
        if not _is_positive_number(ideal):
            errors.append(f"{path}.ideal_cycle_time_s must be positive")
        simulation = profile.get("simulation")
        if not isinstance(simulation, Mapping):
            errors.append(f"{path}.simulation must be a mapping")
            continue
        _unknown(simulation, schema.SIMULATION_KEYS, f"{path}.simulation", errors)
        base = simulation.get("base_cycle_s")
        jitter = simulation.get("jitter_s")
        scale = simulation.get("cycle_scale")
        stress = simulation.get("stress_cycle_time_s")
        if not _is_positive_number(base):
            errors.append(f"{path}.simulation.base_cycle_s must be positive")
        if not _is_number(jitter) or float(jitter) < 0:
            errors.append(f"{path}.simulation.jitter_s must be non-negative")
        if not _is_positive_number(scale):
            errors.append(f"{path}.simulation.cycle_scale must be positive")
        if stress is not None and not _is_positive_number(stress):
            errors.append(f"{path}.simulation.stress_cycle_time_s must be positive or null")
        if mode in {"stress", "synthetic"} and stress is None:
            errors.append(f"{path}.simulation.stress_cycle_time_s is required for {mode}")


def _validate_buffers(
    buffers: list[Any],
    station_by_id: Mapping[str, Mapping[str, Any]],
    errors: list[str],
) -> None:
    ids: set[str] = set()
    for index, buffer_config in enumerate(buffers):
        path = f"buffers[{index}]"
        if not isinstance(buffer_config, Mapping):
            errors.append(f"{path} must be a mapping")
            continue
        _unknown(buffer_config, schema.BUFFER_KEYS, path, errors)
        buffer_id = _required_text(
            buffer_config, "buffer_id", f"{path}.buffer_id", errors
        )
        if buffer_id:
            if buffer_id in ids:
                errors.append(f"duplicate buffer_id '{buffer_id}'")
            ids.add(buffer_id)
        from_id = _required_text(
            buffer_config, "from_station_id", f"{path}.from_station_id", errors
        )
        to_id = _required_text(
            buffer_config, "to_station_id", f"{path}.to_station_id", errors
        )
        position = _positive_int(
            buffer_config, "buffer_position", f"{path}.buffer_position", errors
        )
        _enum(
            buffer_config,
            "buffer_type",
            f"{path}.buffer_type",
            schema.BUFFER_TYPES,
            errors,
        )
        enabled = buffer_config.get("enabled", True)
        if not isinstance(enabled, bool):
            errors.append(f"{path}.enabled must be a boolean")
        tracking_mode = buffer_config.get("tracking_mode", "counter_only")
        if tracking_mode not in schema.BUFFER_TRACKING_MODES:
            errors.append(
                f"{path}.tracking_mode must be one of "
                f"{sorted(schema.BUFFER_TRACKING_MODES)}"
            )
        capacity = buffer_config.get("capacity")
        if capacity is not None and (
            not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0
        ):
            errors.append(f"{path}.capacity must be positive or null")
        for field, station_id in (
            ("from_station_id", from_id),
            ("to_station_id", to_id),
        ):
            if station_id and station_id not in station_by_id:
                errors.append(f"{path}.{field} '{station_id}' does not exist")
            elif station_id and station_by_id[station_id].get("station_enabled", True) is False:
                errors.append(f"{path}.{field} '{station_id}' references disabled station")
        if from_id and to_id and from_id == to_id:
            errors.append(f"{path} cannot connect a station to itself")
        if position is not None and from_id in station_by_id and to_id in station_by_id:
            from_order = station_by_id[from_id].get("station_order")
            to_order = station_by_id[to_id].get("station_order")
            if (
                isinstance(from_order, int)
                and isinstance(to_order, int)
                and not from_order < position < to_order
            ):
                errors.append(
                    f"{path}.buffer_position must be between station orders "
                    f"{from_order} and {to_order}"
                )


def _validate_route(
    route: Mapping[str, Any],
    station_by_id: Mapping[str, Mapping[str, Any]],
    errors: list[str],
) -> None:
    _unknown(route, schema.ROUTE_KEYS, "route_graph", errors)
    entry = _required_text(
        route, "entry_station_id", "route_graph.entry_station_id", errors
    )
    terminal = _required_text(
        route, "terminal_station_id", "route_graph.terminal_station_id", errors
    )
    for field, station_id in (
        ("entry_station_id", entry),
        ("terminal_station_id", terminal),
    ):
        if station_id and station_id not in station_by_id:
            errors.append(f"route_graph.{field} '{station_id}' does not exist")
        elif station_id and station_by_id[station_id].get("station_enabled", True) is False:
            errors.append(f"route_graph.{field} '{station_id}' must reference an enabled station")
    edges = route.get("edges")
    if not isinstance(edges, list) or not edges:
        errors.append("route_graph.edges must contain at least one edge")
        return
    adjacency: dict[str, set[str]] = defaultdict(set)
    for index, edge in enumerate(edges):
        path = f"route_graph.edges[{index}]"
        if not isinstance(edge, Mapping):
            errors.append(f"{path} must be a mapping")
            continue
        _unknown(edge, schema.ROUTE_EDGE_KEYS, path, errors)
        from_id = _required_text(edge, "from_station_id", f"{path}.from_station_id", errors)
        to_id = _required_text(edge, "to_station_id", f"{path}.to_station_id", errors)
        for field, station_id in (("from_station_id", from_id), ("to_station_id", to_id)):
            if station_id and station_id not in station_by_id:
                errors.append(f"{path}.{field} '{station_id}' does not exist")
            elif station_id and station_by_id[station_id].get("station_enabled", True) is False:
                errors.append(f"{path}.{field} '{station_id}' references disabled station")
        if from_id and to_id:
            if from_id == to_id:
                errors.append(f"{path} cannot connect a station to itself")
            adjacency[from_id].add(to_id)
    if entry in station_by_id and terminal in station_by_id:
        reachable = {entry}
        pending = [entry]
        while pending:
            current = pending.pop()
            for next_id in adjacency.get(current, set()):
                if next_id not in reachable:
                    reachable.add(next_id)
                    pending.append(next_id)
        if terminal not in reachable:
            errors.append(
                f"route_graph terminal '{terminal}' is not reachable from entry '{entry}'"
            )


def _unknown(
    raw: Mapping[str, Any], allowed: set[str], path: str, errors: list[str]
) -> None:
    for key in raw:
        if key not in allowed:
            errors.append(f"{path + '.' if path else ''}{key} is not allowed")


def _list(
    raw: Mapping[str, Any], key: str, path: str, errors: list[str]
) -> list[Any]:
    value = raw.get(key)
    if not isinstance(value, list):
        errors.append(f"{path} must be a list")
        return []
    return value


def _mapping(
    raw: Mapping[str, Any], key: str, path: str, errors: list[str]
) -> Mapping[str, Any]:
    value = raw.get(key)
    if not isinstance(value, Mapping):
        errors.append(f"{path} must be a mapping")
        return {}
    return value


def _required_text(
    raw: Mapping[str, Any], key: str, path: str, errors: list[str]
) -> str | None:
    value = raw.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path} is required")
        return None
    return value.strip()


def _enum(
    raw: Mapping[str, Any],
    key: str,
    path: str,
    allowed: set[str],
    errors: list[str],
) -> str | None:
    value = raw.get(key)
    if value is None:
        errors.append(f"{path} is required")
        return None
    if not isinstance(value, str) or value not in allowed:
        errors.append(f"{path} must be one of {sorted(allowed)}")
        return None
    return value


def _positive_int(
    raw: Mapping[str, Any], key: str, path: str, errors: list[str]
) -> int | None:
    value = raw.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        errors.append(f"{path} must be positive")
        return None
    return value


def _nonnegative_int(
    raw: Mapping[str, Any], key: str, path: str, errors: list[str]
) -> int | None:
    value = raw.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        errors.append(f"{path} must be a non-negative integer")
        return None
    return value


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_positive_number(value: Any) -> bool:
    return _is_number(value) and float(value) > 0


def _rate(value: Any) -> bool:
    return _is_number(value) and 0 <= float(value) <= 1


def _template_supports(template: Any, station_type: str) -> bool:
    if not isinstance(template, Mapping):
        return False
    compatible = template.get("compatible_station_types")
    return isinstance(compatible, list) and station_type in compatible
