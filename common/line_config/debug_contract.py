from __future__ import annotations

import copy
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any


FieldError = dict[str, str]

CONFIRMATION_STATES = ("PLANNED", "CONFIRMED")
WRITE_MODE = "READ_DONE_ONLY"
WRITE_DISABLED_FIELDS = (
    "parameter_writes_enabled",
    "machine_control_writes_enabled",
    "safety_writes_enabled",
    "arbitrary_db_writes_enabled",
)
SUPPORTED_TYPES = {
    "bool",
    "byte",
    "word",
    "int",
    "dword",
    "dint",
    "real",
    "unix_time_seconds",
    "string",
}
_ADDRESS_RE = re.compile(
    r"^DB(?P<db>[0-9]+)\.DB(?P<area>[XBWDL])(?P<byte>[0-9]+)(?:\.(?P<bit>[0-7]))?$"
)
_DIRECTION_ALIASES = {
    "read": "PLC_TO_EDGE",
    "read_only": "PLC_TO_EDGE",
    "plc_to_edge": "PLC_TO_EDGE",
    "plc-to-edge": "PLC_TO_EDGE",
    "inbound": "PLC_TO_EDGE",
    "read_write": "READ_WRITE",
    "read-write": "READ_WRITE",
    "bidirectional": "READ_WRITE",
    "write": "EDGE_TO_PLC",
    "edge_to_plc": "EDGE_TO_PLC",
    "edge-to-plc": "EDGE_TO_PLC",
    "outbound": "EDGE_TO_PLC",
}


class DebugContractError(ValueError):
    """Raised when a candidate cannot be represented as a safe debug contract."""

    def __init__(self, errors: Sequence[FieldError] | str) -> None:
        if isinstance(errors, str):
            self.errors = [{"field": "debug_contract", "message": errors}]
        else:
            self.errors = list(errors)
        super().__init__("; ".join(error["message"] for error in self.errors))


def normalize_debug_candidate(
    raw: Mapping[str, Any],
    *,
    seed_contract: Mapping[str, Any] | None = None,
    expected_station_ids: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Return a canonical candidate shell before field-level validation.

    The legacy deployment API accepts connection-only payloads.  When stations
    are omitted, the caller supplies a seed from the current effective mapping
    or from a freshly compiled line projection.  This keeps the existing
    candidate endpoint backward-compatible while making the persisted object a
    complete contract.
    """

    candidate: dict[str, Any] = {
        key: copy.deepcopy(raw.get(key))
        for key in (
            "host",
            "port",
            "rack",
            "slot",
            "connection_timeout_ms",
            "poll_interval_ms",
            "line_config",
        )
        if key in raw
    }
    nested = raw.get("debug_contract")
    if isinstance(nested, Mapping):
        for key in ("debug_scope", "stations", "write_allowlist"):
            if key in nested and key not in raw:
                candidate[key] = copy.deepcopy(nested[key])
    for key in ("debug_scope", "stations", "write_allowlist"):
        if key in raw:
            candidate[key] = copy.deepcopy(raw[key])
    if "stations" not in candidate and seed_contract is not None:
        candidate["stations"] = copy.deepcopy(seed_contract.get("stations", []))
    if "write_allowlist" not in candidate and seed_contract is not None:
        candidate["write_allowlist"] = copy.deepcopy(
            seed_contract.get("write_allowlist", _default_write_allowlist([]))
        )
    explicit_scope = "debug_scope" in candidate
    if explicit_scope:
        scope_ids = _scope_station_ids(candidate.get("debug_scope"))
    elif expected_station_ids is not None:
        scope_ids = [str(item) for item in expected_station_ids]
    elif isinstance(seed_contract, Mapping):
        scope_ids = _scope_station_ids(seed_contract.get("debug_scope"))
        if not scope_ids:
            scope_ids = _station_ids_from_contract(seed_contract)
    else:
        scope_ids = _station_ids_from_contract(candidate)
    candidate["debug_scope"] = {"station_ids": copy.deepcopy(scope_ids)}
    if explicit_scope and isinstance(candidate.get("stations"), list):
        station_by_id = {
            str(item.get("station_id")): item
            for item in candidate["stations"]
            if isinstance(item, Mapping) and item.get("station_id") is not None
        }
        candidate["stations"] = [
            copy.deepcopy(station_by_id[station_id])
            for station_id in scope_ids
            if isinstance(station_id, str) and station_id in station_by_id
        ]
    if explicit_scope and isinstance(candidate.get("write_allowlist"), Mapping):
        allowlist = copy.deepcopy(dict(candidate["write_allowlist"]))
        entries = allowlist.get("edge_to_plc")
        if isinstance(entries, list):
            selected = set(scope_ids)
            allowlist["edge_to_plc"] = [
                entry
                for entry in entries
                if isinstance(entry, Mapping) and str(entry.get("station_id")) in selected
            ]
        candidate["write_allowlist"] = allowlist
    candidate["stations"] = _normalize_station_list(candidate.get("stations"))
    candidate["write_allowlist"] = _normalize_write_allowlist(
        candidate.get("write_allowlist"),
        candidate["stations"],
    )
    return candidate


def parse_debug_candidate(
    raw: Mapping[str, Any],
    *,
    expected_station_ids: Sequence[str] | None = None,
    seed_contract: Mapping[str, Any] | None = None,
) -> tuple[dict[str, Any] | None, list[FieldError]]:
    candidate = normalize_debug_candidate(
        raw,
        seed_contract=seed_contract,
        expected_station_ids=expected_station_ids,
    )
    errors: list[FieldError] = []
    _validate_connection_shape(candidate, errors)

    expected_order = [str(item) for item in expected_station_ids or ()]
    scope_ids, scope_errors = _canonical_debug_scope(
        candidate.get("debug_scope"),
        expected_order if expected_station_ids is not None else None,
    )
    errors.extend(scope_errors)
    candidate["debug_scope"] = {"station_ids": scope_ids}
    selected_scope = set(scope_ids)
    stations = candidate.get("stations")
    if not isinstance(stations, list) or not stations:
        errors.append({"field": "stations", "message": "At least one debug station mapping is required."})
        return None, errors

    station_ids: list[str] = []
    station_dbs: list[int] = []
    station_signal_names: dict[str, set[str]] = {}
    for index, station in enumerate(stations):
        prefix = f"stations[{index}]"
        if not isinstance(station, dict):
            errors.append({"field": prefix, "message": "Station mapping must be an object."})
            continue
        station_id = station.get("station_id")
        if not isinstance(station_id, str) or not station_id.strip():
            errors.append({"field": f"{prefix}.station_id", "message": "Station identity is required."})
            continue
        station_id = station_id.strip()
        station["station_id"] = station_id
        station_ids.append(station_id)
        db_number = _bounded_int(
            station.get("db_number"),
            f"{prefix}.db_number",
            1,
            65535,
            errors,
        )
        if db_number is not None:
            station["db_number"] = db_number
            station_dbs.append(db_number)
        read_start = _bounded_int(
            station.get("read_start"),
            f"{prefix}.read_start",
            0,
            65535,
            errors,
        )
        read_length = _bounded_int(
            station.get("read_length"),
            f"{prefix}.read_length",
            1,
            65536,
            errors,
        )
        if read_start is not None and read_length is not None:
            station["read_start"] = read_start
            station["read_length"] = read_length
            if read_start + read_length > 65536:
                errors.append(
                    {
                        "field": f"{prefix}.read_length",
                        "message": "Station read range must end at or before byte 65536.",
                    }
                )
        _validate_confirmation(station, f"{prefix}.confirmation_state", errors)
        signals = station.get("signals")
        station_signal_names[station_id] = set()
        if not isinstance(signals, list) or not signals:
            errors.append({"field": f"{prefix}.signals", "message": "Station signals are required."})
            continue
        addresses: set[str] = set()
        for signal_index, signal in enumerate(signals):
            signal_prefix = f"{prefix}.signals[{signal_index}]"
            if not isinstance(signal, dict):
                errors.append({"field": signal_prefix, "message": "Signal mapping must be an object."})
                continue
            field_name = signal.get("field_name", signal.get("name"))
            if not isinstance(field_name, str) or not field_name.strip():
                errors.append({"field": f"{signal_prefix}.field_name", "message": "Signal field name is required."})
                continue
            field_name = field_name.strip()
            signal["field_name"] = field_name
            if field_name in station_signal_names[station_id]:
                errors.append({"field": f"{signal_prefix}.field_name", "message": "Signal field name is duplicated."})
            station_signal_names[station_id].add(field_name)
            address = signal.get("address")
            address_parts = _parse_address(address)
            if address_parts is None:
                errors.append({"field": f"{signal_prefix}.address", "message": "Siemens address is malformed or out of range."})
            else:
                signal["address"] = address_parts["canonical"]
            data_type = str(signal.get("type", signal.get("data_type", ""))).strip().lower()
            signal["type"] = data_type
            if data_type not in SUPPORTED_TYPES:
                errors.append({"field": f"{signal_prefix}.type", "message": f"Unsupported signal type: {data_type or '(empty)'}"})
            direction = _normalize_direction(signal.get("direction"), field_name)
            if direction is None:
                errors.append({"field": f"{signal_prefix}.direction", "message": "Signal direction is invalid."})
            else:
                signal["direction"] = direction
            confirmation = _validate_confirmation(signal, f"{signal_prefix}.confirmation_state", errors)
            if confirmation is not None:
                signal["confirmation_state"] = confirmation
            if data_type == "string":
                length = signal.get("max_length", signal.get("length"))
                bounded_length = _bounded_int(length, f"{signal_prefix}.max_length", 1, 65534, errors)
                if bounded_length is not None:
                    signal["max_length"] = bounded_length
            elif "max_length" in signal or "length" in signal:
                errors.append({"field": f"{signal_prefix}.max_length", "message": "Only string signals may declare max_length."})
            if "required" in signal and type(signal["required"]) is not bool:
                errors.append({"field": f"{signal_prefix}.required", "message": "required must be a boolean."})
            else:
                signal["required"] = bool(signal.get("required", True))
            group = str(signal.get("group", "header")).strip().lower()
            if group not in {"header", "payload"}:
                errors.append({"field": f"{signal_prefix}.group", "message": "Signal group must be header or payload."})
            signal["group"] = group
            for text_key in ("unit", "description"):
                if text_key in signal and signal[text_key] is not None and not isinstance(signal[text_key], str):
                    errors.append({"field": f"{signal_prefix}.{text_key}", "message": f"{text_key} must be text when provided."})
                elif signal.get(text_key) is not None:
                    signal[text_key] = str(signal[text_key]).strip()
            if address_parts is not None and db_number is not None:
                _validate_signal_address(
                    signal,
                    address_parts,
                    db_number,
                    read_start,
                    read_length,
                    signal_prefix,
                    errors,
                )
            if field_name == "read_done" and direction != "READ_WRITE":
                errors.append({"field": f"{signal_prefix}.direction", "message": "read_done must remain READ_WRITE."})
            if direction == "EDGE_TO_PLC" and field_name != "read_done":
                errors.append({"field": f"{signal_prefix}.direction", "message": "Only read_done may have Edge-to-PLC write semantics."})
            if address_parts is not None:
                if address_parts["canonical"] in addresses:
                    errors.append({"field": f"{signal_prefix}.address", "message": "Signal address is duplicated within the station."})
                addresses.add(address_parts["canonical"])

    if len(set(station_ids)) != len(station_ids):
        errors.append({"field": "stations", "message": "Station identity is duplicated."})
    if len(set(station_dbs)) != len(station_dbs):
        errors.append({"field": "stations", "message": "Station DB number is duplicated."})
    if set(station_ids) != selected_scope:
        errors.append(
            {
                "field": "stations",
                "message": "Debug stations must exactly match the selected Debug Pilot scope.",
            }
        )
    if expected_station_ids is not None and not selected_scope.issubset(set(expected_order)):
        errors.append(
            {
                "field": "debug_scope.station_ids",
                "message": "Debug scope contains an unknown or disabled station.",
            }
        )

    required_by_station = _required_signal_names_by_station(seed_contract)
    for station in stations:
        if not isinstance(station, dict):
            continue
        station_id = str(station.get("station_id", ""))
        names = {str(signal.get("field_name")) for signal in station.get("signals", []) if isinstance(signal, dict)}
        required = required_by_station.get(station_id, set()) | {
            "cycle_counter",
            "payload_ready",
            "cycle_valid",
            "read_done",
            "station_dmc",
            "unit_id",
            "plc_start_time",
            "plc_end_time",
            "result",
            "nok_code_count",
            "nok_codes_1",
        }
        missing = sorted(required - names)
        for field_name in missing:
            errors.append(
                {
                    "field": f"stations[{station_id}].signals",
                    "message": f"Required debug signal is missing: {field_name}.",
                }
            )

    _validate_write_allowlist(candidate.get("write_allowlist"), stations, errors)
    if errors:
        return None, errors
    canonical = _canonical_candidate(candidate)
    return canonical, []


def debug_contract_from_mapping(mapping: Mapping[str, Any]) -> dict[str, Any]:
    """Seed an editable contract from an effective or projected runtime mapping."""

    template = mapping.get("station_template")
    template_header = template.get("header", {}) if isinstance(template, Mapping) else {}
    raw_stations = mapping.get("stations")
    if not isinstance(raw_stations, list):
        raw_stations = []
    stations: list[dict[str, Any]] = []
    for ordinal, raw_station in enumerate(
        sorted(
            (item for item in raw_stations if isinstance(item, Mapping)),
            key=lambda item: (int(item.get("station_order", 2**31 - 1)), str(item.get("station_id", ""))),
        ),
        start=1,
    ):
        station_id = str(raw_station.get("station_id", "")).strip()
        db_number = int(raw_station.get("db_number", 0))
        if not station_id or db_number <= 0:
            continue
        signals: list[dict[str, Any]] = []
        source_header = template_header
        if not source_header and isinstance(raw_station.get("header"), Mapping):
            source_header = raw_station["header"]
        for name, field in _iter_runtime_fields(source_header, group="header", db_number=db_number):
            signals.append(_seed_signal(name, field, group="header"))
        payload = raw_station.get("payload")
        if isinstance(payload, Mapping):
            for name, field in _iter_runtime_fields(payload, group="payload", db_number=db_number):
                signals.append(_seed_signal(name, field, group="payload"))
        read_start = _as_int(raw_station.get("debug_read_start", raw_station.get("read_start", 0)), 0)
        declared_length = _as_int(
            raw_station.get("debug_read_length", raw_station.get("read_length", raw_station.get("effective_read_size_bytes", 0))),
            0,
        )
        calculated_end = max(
            (_signal_end(signal) for signal in signals if isinstance(signal, Mapping)),
            default=read_start + 1,
        )
        # Preserve an accepted mapping's declared range.  The Collector's
        # S7 string decoder adds its two-byte framing to the physical read
        # plan; the engineering contract range remains the accepted payload
        # range and is validated against the declared mapping convention.
        read_length = max(1, declared_length) if declared_length > 0 else max(1, calculated_end - read_start)
        stations.append(
            {
                "station_id": station_id,
                "db_number": db_number,
                "station_order": _as_int(raw_station.get("station_order"), ordinal),
                "read_start": read_start,
                "read_length": read_length,
                "confirmation_state": "PLANNED",
                "signals": sorted(signals, key=lambda item: (str(item["field_name"]), str(item["address"]))),
            }
        )
    station_ids = [str(station["station_id"]) for station in stations]
    allowlist = _default_write_allowlist(stations)
    return {
        "schema_version": "plc-debug-contract/v1",
        "debug_scope": {"station_ids": station_ids},
        "stations": stations,
        "write_allowlist": allowlist,
    }


def debug_contract_from_candidate(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return _canonical_contract(
        {
            "schema_version": "plc-debug-contract/v1",
            "debug_scope": copy.deepcopy(candidate.get("debug_scope")),
            "stations": copy.deepcopy(candidate.get("stations", [])),
            "write_allowlist": copy.deepcopy(
                candidate.get("write_allowlist", _default_write_allowlist([]))
            ),
        }
    )


def debug_contract_to_dict(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return debug_contract_from_candidate(candidate)


def debug_candidate_to_dict(candidate: Mapping[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(_canonical_candidate(candidate))


def debug_contract_content_hash(contract: Mapping[str, Any]) -> str:
    canonical = _canonical_contract(contract)
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def debug_candidate_content_hash(candidate: Mapping[str, Any], line_config_hash: str) -> str:
    content = {
        "candidate": _canonical_candidate(candidate),
        "line_config_hash": line_config_hash,
    }
    encoded = json.dumps(
        content,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def engineering_rows(candidate: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for station in _canonical_contract(candidate).get("stations", []):
        read_start = int(station["read_start"])
        read_end = read_start + int(station["read_length"])
        for signal in station["signals"]:
            rows.append(
                {
                    "station_id": station["station_id"],
                    "db_number": station["db_number"],
                    "read_range": f"DB{station['db_number']}[{read_start}:{read_end})",
                    "field_name": signal["field_name"],
                    "address": signal["address"],
                    "type": signal["type"],
                    "direction": signal["direction"],
                    "unit": signal.get("unit", ""),
                    "description": signal.get("description", ""),
                    "confirmation_state": signal["confirmation_state"],
                    "write_semantic": "Read_Done only" if signal["field_name"] == "read_done" else "PLC_TO_EDGE",
                }
            )
    return rows


def engineering_export(
    candidate: Mapping[str, Any],
    *,
    candidate_hash: str | None = None,
    base_topology: Mapping[str, Any] | None = None,
) -> str:
    contract = _canonical_contract(candidate)
    topology = _export_topology(base_topology, contract)
    scope_ids = contract["debug_scope"]["station_ids"]
    lines = [
        "# PLC Debug Communication Contract",
        "",
        "- Schema: `plc-debug-contract/v1`",
        f"- Contract hash: `sha256:{debug_contract_content_hash(contract)}`",
        f"- Candidate hash: `{candidate_hash or '(computed after line-config binding)'}`",
        "- Candidate state: separate from Active; persistence does not activate Collector configuration.",
        f"- Base line/topology: `{topology['line_id']}` / `{topology['entry_station_id']} -> {topology['terminal_station_id']}` / stations `{', '.join(topology['station_ids'])}`",
        f"- Debug Pilot scope: `{', '.join(scope_ids)}` ({len(scope_ids)} / {len(topology['station_ids'])})",
        "",
        "## Write allowlist",
        "",
        f"- Mode: `{contract['write_allowlist']['mode']}`",
        "- Edge-to-PLC semantic: `Read_Done` only",
        "- Parameter writes: disabled",
        "- Machine-control writes: disabled",
        "- Safety writes: disabled",
        "- Arbitrary DB writes: disabled",
        "",
        "## Station and signal map",
        "",
        "| Station | Read range | Field | PLC address | Type | Direction | Unit | Confirmation |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in engineering_rows(contract):
        values = [
            row["station_id"],
            row["read_range"],
            row["field_name"],
            row["address"],
            row["type"],
            row["direction"],
            row["unit"] or "—",
            row["confirmation_state"],
        ]
        lines.append("| " + " | ".join(_markdown_cell(value) for value in values) + " |")
    return "\n".join(lines) + "\n"


def _validate_connection_shape(candidate: Mapping[str, Any], errors: list[FieldError]) -> None:
    host = candidate.get("host")
    if not isinstance(host, str) or not host.strip():
        errors.append({"field": "host", "message": "PLC host is required."})
    elif len(host.strip()) > 253:
        errors.append({"field": "host", "message": "PLC host must be at most 253 characters."})
    for field, minimum, maximum in (
        ("port", 1, 65535),
        ("rack", 0, 7),
        ("slot", 0, 31),
        ("connection_timeout_ms", 100, 5000),
        ("poll_interval_ms", 100, 60000),
    ):
        _bounded_int(candidate.get(field), field, minimum, maximum, errors)
    line_config = candidate.get("line_config")
    if not isinstance(line_config, str) or not line_config.strip():
        errors.append({"field": "line_config", "message": "Line configuration is required."})


def _validate_confirmation(value: Mapping[str, Any], field: str, errors: list[FieldError]) -> str | None:
    state = str(value.get("confirmation_state", value.get("status", "PLANNED"))).strip().upper()
    if state not in CONFIRMATION_STATES:
        errors.append({"field": field, "message": "Confirmation state must be PLANNED or CONFIRMED."})
        return None
    value["confirmation_state"] = state
    return state


def _validate_signal_address(
    signal: Mapping[str, Any],
    parts: Mapping[str, Any],
    station_db: int,
    read_start: int | None,
    read_length: int | None,
    field: str,
    errors: list[FieldError],
) -> None:
    if parts["db"] != station_db:
        errors.append({"field": f"{field}.address", "message": "Signal address DB must match the station DB number."})
    data_type = str(signal.get("type", ""))
    area = str(parts["area"])
    expected_areas = {
        "bool": {"X"},
        "byte": {"B"},
        "word": {"W"},
        "int": {"W"},
        "dword": {"D"},
        "dint": {"D"},
        "real": {"D"},
        "unix_time_seconds": {"D"},
        "string": {"B"},
    }
    if area not in expected_areas.get(data_type, set()):
        errors.append({"field": f"{field}.address", "message": f"{data_type} signals require a compatible Siemens DB area."})
    if data_type == "bool" and parts["bit"] is None:
        errors.append({"field": f"{field}.address", "message": "bool signals require a DBX bit address."})
    if data_type != "bool" and parts["bit"] is not None:
        errors.append({"field": f"{field}.address", "message": "Only bool signals may include a DBX bit offset."})
    size = _signal_size(signal)
    offset = int(parts["byte"])
    if offset + size > 65536:
        errors.append({"field": f"{field}.address", "message": "Signal address exceeds the maximum S7 DB byte range."})
    if read_start is not None and read_length is not None and (
        offset < read_start or offset + size > read_start + read_length
    ):
        errors.append({"field": f"{field}.address", "message": "Signal address is outside the candidate station read range."})


def _validate_write_allowlist(
    value: object,
    stations: list[Any],
    errors: list[FieldError],
) -> None:
    if not isinstance(value, dict):
        errors.append({"field": "write_allowlist", "message": "An explicit Read_Done-only write allowlist is required."})
        return
    if value.get("mode") != WRITE_MODE:
        errors.append({"field": "write_allowlist.mode", "message": "Write allowlist mode must be READ_DONE_ONLY."})
    for field in WRITE_DISABLED_FIELDS:
        if value.get(field) is not False:
            errors.append({"field": f"write_allowlist.{field}", "message": f"{field} must be false for FV1A."})
    entries = value.get("edge_to_plc")
    if not isinstance(entries, list):
        errors.append({"field": "write_allowlist.edge_to_plc", "message": "edge_to_plc must list only the station Read_Done mappings."})
        return
    expected = {
        str(station.get("station_id")): next(
            (
                signal
                for signal in station.get("signals", [])
                if isinstance(signal, dict) and signal.get("field_name") == "read_done"
            ),
            None,
        )
        for station in stations
        if isinstance(station, dict)
    }
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"write_allowlist.edge_to_plc[{index}]"
        if not isinstance(entry, dict):
            errors.append({"field": prefix, "message": "Write allowlist entry must be an object."})
            continue
        station_id = str(entry.get("station_id", ""))
        field_name = str(entry.get("field_name", ""))
        if field_name != "read_done":
            errors.append({"field": f"{prefix}.field_name", "message": "Read_Done is the only allowed Edge-to-PLC field."})
        if station_id in seen:
            errors.append({"field": f"{prefix}.station_id", "message": "A station may have only one Read_Done write entry."})
        seen.add(station_id)
        signal = expected.get(station_id)
        if signal is None:
            errors.append({"field": prefix, "message": "Write allowlist station must declare a matching read_done signal."})
            continue
        if entry.get("address") != signal.get("address"):
            errors.append({"field": f"{prefix}.address", "message": "Read_Done allowlist address does not match the station signal mapping."})
        if str(entry.get("type", "")).lower() != str(signal.get("type", "")).lower():
            errors.append({"field": f"{prefix}.type", "message": "Read_Done allowlist type does not match the station signal mapping."})
        entry["direction"] = "EDGE_TO_PLC"
        entry["confirmation_state"] = str(entry.get("confirmation_state", entry.get("status", "PLANNED"))).upper()
    for station_id in expected:
        if station_id not in seen:
            errors.append({"field": "write_allowlist.edge_to_plc", "message": f"Read_Done allowlist entry is missing for {station_id}."})


def _normalize_station_list(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [_normalize_station(item) if isinstance(item, Mapping) else item for item in value]


def _normalize_station(value: Mapping[str, Any]) -> dict[str, Any]:
    station = copy.deepcopy(dict(value))
    station.setdefault("confirmation_state", station.get("status", "PLANNED"))
    station.setdefault("read_length", station.get("read_size"))
    raw_signals = station.get("signals", [])
    station["signals"] = [_normalize_signal(item) if isinstance(item, Mapping) else item for item in raw_signals] if isinstance(raw_signals, list) else raw_signals
    return station


def _normalize_signal(value: Mapping[str, Any]) -> dict[str, Any]:
    signal = copy.deepcopy(dict(value))
    if "field_name" not in signal and "name" in signal:
        signal["field_name"] = signal["name"]
    if "type" not in signal and "data_type" in signal:
        signal["type"] = signal["data_type"]
    if "max_length" not in signal and "length" in signal:
        signal["max_length"] = signal["length"]
    signal.setdefault("confirmation_state", signal.get("status", "PLANNED"))
    if "direction" in signal:
        signal["direction"] = _normalize_direction(signal.get("direction"), str(signal.get("field_name", ""))) or signal.get("direction")
    return signal


def _normalize_write_allowlist(value: object, stations: list[Any]) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return _default_write_allowlist(stations)
    allowlist = copy.deepcopy(dict(value))
    allowlist.setdefault("mode", WRITE_MODE)
    for field in WRITE_DISABLED_FIELDS:
        allowlist.setdefault(field, False)
    entries = allowlist.get("edge_to_plc")
    if not isinstance(entries, list):
        return _default_write_allowlist(stations)
    allowlist["edge_to_plc"] = [
        _normalize_allowlist_entry(item) if isinstance(item, Mapping) else item
        for item in entries
    ]
    return allowlist


def _normalize_allowlist_entry(value: Mapping[str, Any]) -> dict[str, Any]:
    entry = copy.deepcopy(dict(value))
    entry.setdefault("field_name", entry.get("name", ""))
    entry.setdefault("type", entry.get("data_type", "bool"))
    entry.setdefault("confirmation_state", entry.get("status", "PLANNED"))
    entry["direction"] = "EDGE_TO_PLC"
    return entry


def _default_write_allowlist(stations: Sequence[Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for station in stations:
        if not isinstance(station, Mapping):
            continue
        for signal in station.get("signals", []):
            if isinstance(signal, Mapping) and signal.get("field_name") == "read_done":
                entries.append(
                    {
                        "station_id": station.get("station_id"),
                        "field_name": "read_done",
                        "address": signal.get("address"),
                        "type": signal.get("type", "bool"),
                        "direction": "EDGE_TO_PLC",
                        "confirmation_state": signal.get("confirmation_state", "PLANNED"),
                    }
                )
                break
    return {
        "mode": WRITE_MODE,
        "edge_to_plc": entries,
        **{field: False for field in WRITE_DISABLED_FIELDS},
    }


def _canonical_candidate(candidate: Mapping[str, Any]) -> dict[str, Any]:
    contract = _canonical_contract(candidate)
    result = {
        key: copy.deepcopy(candidate.get(key))
        for key in (
            "host",
            "port",
            "rack",
            "slot",
            "connection_timeout_ms",
            "poll_interval_ms",
            "line_config",
        )
        if key in candidate
    }
    result["debug_scope"] = copy.deepcopy(contract.get("debug_scope", {"station_ids": []}))
    result["stations"] = contract.get("stations", [])
    result["write_allowlist"] = contract.get("write_allowlist", _default_write_allowlist([]))
    return result


def _canonical_contract(contract: Mapping[str, Any]) -> dict[str, Any]:
    raw_stations = contract.get("stations", [])
    stations = [copy.deepcopy(item) for item in raw_stations if isinstance(item, Mapping)] if isinstance(raw_stations, list) else []
    raw_scope_ids = _scope_station_ids(contract.get("debug_scope"))
    if raw_scope_ids:
        selected_ids = set(raw_scope_ids)
        stations = [
            station
            for station in stations
            if str(station.get("station_id", "")) in selected_ids
        ]
    for station in stations:
        station.pop("status", None)
        station["confirmation_state"] = str(station.get("confirmation_state", "PLANNED")).upper()
        station["signals"] = [copy.deepcopy(item) for item in station.get("signals", []) if isinstance(item, Mapping)]
        for signal in station["signals"]:
            signal.pop("name", None)
            signal.pop("data_type", None)
            signal.pop("length", None)
            signal.pop("status", None)
            signal["confirmation_state"] = str(signal.get("confirmation_state", "PLANNED")).upper()
            signal["direction"] = _normalize_direction(signal.get("direction"), str(signal.get("field_name", ""))) or signal.get("direction")
        station["signals"].sort(key=lambda item: (str(item.get("field_name", "")), str(item.get("address", ""))))
    stations.sort(key=lambda item: (_as_int(item.get("station_order"), 2**31 - 1), str(item.get("station_id", ""))))
    station_ids = [str(station.get("station_id", "")) for station in stations]
    station_order = {station_id: index for index, station_id in enumerate(station_ids)}
    scope_ids = raw_scope_ids or station_ids
    scope_ids = sorted(
        {str(station_id) for station_id in scope_ids},
        key=lambda station_id: (station_order.get(station_id, 2**31 - 1), station_id),
    )
    allowlist = copy.deepcopy(contract.get("write_allowlist", _default_write_allowlist(stations)))
    if not isinstance(allowlist, dict):
        allowlist = _default_write_allowlist(stations)
    allowlist.setdefault("mode", WRITE_MODE)
    allowlist.setdefault("edge_to_plc", [])
    selected_scope = set(scope_ids)
    for field in WRITE_DISABLED_FIELDS:
        allowlist.setdefault(field, False)
    if isinstance(allowlist.get("edge_to_plc"), list):
        allowlist["edge_to_plc"] = [
            copy.deepcopy(item) for item in allowlist["edge_to_plc"] if isinstance(item, Mapping)
            and str(item.get("station_id", "")) in selected_scope
        ]
        allowlist["edge_to_plc"].sort(key=lambda item: (str(item.get("station_id", "")), str(item.get("field_name", "")), str(item.get("address", ""))))
        for entry in allowlist["edge_to_plc"]:
            entry["direction"] = "EDGE_TO_PLC"
            entry["confirmation_state"] = str(entry.get("confirmation_state", "PLANNED")).upper()
    return {
        "schema_version": str(contract.get("schema_version", "plc-debug-contract/v1")),
        "debug_scope": {"station_ids": scope_ids},
        "stations": stations,
        "write_allowlist": allowlist,
    }


def _scope_station_ids(value: object) -> list[Any]:
    if isinstance(value, Mapping):
        value = value.get("station_ids")
    if not isinstance(value, list):
        return []
    return copy.deepcopy(value)


def _station_ids_from_contract(contract: Mapping[str, Any]) -> list[str]:
    stations = contract.get("stations", [])
    if not isinstance(stations, list):
        return []
    ordered = [item for item in stations if isinstance(item, Mapping)]
    ordered.sort(
        key=lambda item: (
            _as_int(item.get("station_order"), 2**31 - 1),
            str(item.get("station_id", "")),
        )
    )
    return [str(item.get("station_id", "")) for item in ordered if item.get("station_id")]


def _canonical_debug_scope(
    value: object,
    expected_station_ids: Sequence[str] | None,
) -> tuple[list[str], list[FieldError]]:
    raw_ids = _scope_station_ids(value)
    errors: list[FieldError] = []
    if not raw_ids:
        errors.append(
            {
                "field": "debug_scope.station_ids",
                "message": "Debug Pilot scope must select at least one station.",
            }
        )
    seen: set[str] = set()
    valid_ids: list[str] = []
    expected = [str(item) for item in expected_station_ids] if expected_station_ids is not None else []
    expected_set = set(expected)
    for index, raw_id in enumerate(raw_ids):
        if not isinstance(raw_id, str) or not raw_id.strip():
            errors.append(
                {
                    "field": f"debug_scope.station_ids[{index}]",
                    "message": "Debug scope station IDs must be non-empty text.",
                }
            )
            continue
        station_id = raw_id.strip()
        if station_id in seen:
            errors.append(
                {
                    "field": f"debug_scope.station_ids[{index}]",
                    "message": "Debug scope station IDs must be unique.",
                }
            )
            continue
        seen.add(station_id)
        if expected_station_ids is not None and station_id not in expected_set:
            errors.append(
                {
                    "field": f"debug_scope.station_ids[{index}]",
                    "message": f"Debug scope station is unknown or disabled: {station_id}.",
                }
            )
            continue
        valid_ids.append(station_id)
    if expected_station_ids is not None:
        canonical = [station_id for station_id in expected if station_id in seen and station_id in expected_set]
    else:
        canonical = sorted(valid_ids)
    return canonical, errors


def _export_topology(
    base_topology: Mapping[str, Any] | None,
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    station_ids = _station_ids_from_contract(contract)
    if isinstance(base_topology, Mapping):
        raw_station_ids = base_topology.get("station_ids")
        if isinstance(raw_station_ids, list) and raw_station_ids:
            station_ids = [str(item) for item in raw_station_ids]
        return {
            "line_id": str(base_topology.get("line_id", "(selected line)")),
            "entry_station_id": str(base_topology.get("entry_station_id", station_ids[0] if station_ids else "(none)")),
            "terminal_station_id": str(base_topology.get("terminal_station_id", station_ids[-1] if station_ids else "(none)")),
            "station_ids": station_ids,
        }
    return {
        "line_id": "(selected line)",
        "entry_station_id": station_ids[0] if station_ids else "(none)",
        "terminal_station_id": station_ids[-1] if station_ids else "(none)",
        "station_ids": station_ids,
    }


def _required_signal_names_by_station(seed_contract: Mapping[str, Any] | None) -> dict[str, set[str]]:
    if not isinstance(seed_contract, Mapping):
        return {}
    result: dict[str, set[str]] = {}
    stations = seed_contract.get("stations", [])
    if isinstance(stations, list):
        for station in stations:
            if isinstance(station, Mapping):
                result[str(station.get("station_id", ""))] = {
                    str(signal.get("field_name", signal.get("name", "")))
                    for signal in station.get("signals", [])
                    if isinstance(signal, Mapping)
                }
    return result


def _iter_runtime_fields(value: object, *, group: str, db_number: int) -> list[tuple[str, dict[str, Any]]]:
    if not isinstance(value, Mapping):
        return []
    result: list[tuple[str, dict[str, Any]]] = []
    for name, raw_field in value.items():
        if not isinstance(raw_field, Mapping):
            continue
        field = copy.deepcopy(dict(raw_field))
        if field.get("type") == "array":
            items = field.get("items", [])
            if isinstance(items, list):
                for index, item in enumerate(items, start=1):
                    if not isinstance(item, Mapping):
                        continue
                    expanded = copy.deepcopy(dict(item))
                    expanded["address"] = _replace_db_token(expanded.get("address"), db_number)
                    result.append((f"{name}_{index}", expanded))
            continue
        field["address"] = _replace_db_token(field.get("address"), db_number)
        result.append((str(name), field))
    return result


def _seed_signal(name: str, field: Mapping[str, Any], *, group: str) -> dict[str, Any]:
    data_type = str(field.get("type", "")).lower()
    signal: dict[str, Any] = {
        "field_name": name,
        "address": str(field.get("address", "")),
        "type": data_type,
        "direction": _normalize_direction(field.get("direction"), name) or "PLC_TO_EDGE",
        "group": group,
        "required": bool(field.get("required", True)),
        "confirmation_state": "PLANNED",
        "unit": _default_unit(name),
        "description": _default_description(name),
    }
    if data_type == "string":
        signal["max_length"] = int(field.get("max_length", 40))
    return signal


def _replace_db_token(value: object, db_number: int) -> str:
    return str(value or "").replace("{db}", f"DB{db_number}")


def _default_unit(field_name: str) -> str:
    lowered = field_name.lower()
    for suffix, unit in (
        ("torque_nm", "Nm"),
        ("angle_deg", "deg"),
        ("current_a", "A"),
        ("voltage_v", "V"),
        ("time_ms", "ms"),
        ("time", "epoch seconds"),
    ):
        if lowered.endswith(suffix):
            return unit
    return ""


def _default_description(field_name: str) -> str:
    descriptions = {
        "cycle_counter": "PLC cycle identity counter",
        "payload_ready": "PLC indicates decoded payload is ready",
        "cycle_valid": "PLC cycle validity flag",
        "read_done": "Edge confirmation write for an accepted cycle",
        "station_dmc": "Station DMC identity",
        "unit_id": "Unit or product identity",
        "result": "PLC station result code",
        "nok_code_count": "Number of NOK codes",
        "nok_codes_1": "Primary NOK code",
    }
    return descriptions.get(field_name, "Editable debug communication signal")


def _parse_address(value: object) -> dict[str, Any] | None:
    if not isinstance(value, str):
        return None
    match = _ADDRESS_RE.fullmatch(value.strip().upper())
    if not match:
        return None
    db_number = int(match.group("db"))
    byte_offset = int(match.group("byte"))
    bit = match.group("bit")
    if not 1 <= db_number <= 65535 or not 0 <= byte_offset <= 65535:
        return None
    area = match.group("area")
    if area == "X" and bit is None:
        return None
    if area != "X" and bit is not None:
        return None
    return {
        "db": db_number,
        "area": area,
        "byte": byte_offset,
        "bit": int(bit) if bit is not None else None,
        "canonical": f"DB{db_number}.DB{area}{byte_offset}" + (f".{bit}" if bit is not None else ""),
    }


def _normalize_direction(value: object, field_name: str) -> str | None:
    if value is None or str(value).strip() == "":
        return "READ_WRITE" if field_name == "read_done" else "PLC_TO_EDGE"
    return _DIRECTION_ALIASES.get(str(value).strip().lower())


def _bounded_int(value: object, field: str, minimum: int, maximum: int, errors: list[FieldError]) -> int | None:
    if type(value) is not int:
        errors.append({"field": field, "message": f"{field} must be an integer."})
        return None
    if not minimum <= value <= maximum:
        errors.append({"field": field, "message": f"{field} must be between {minimum} and {maximum}."})
        return None
    return value


def _signal_size(signal: Mapping[str, Any]) -> int:
    data_type = str(signal.get("type", "")).lower()
    if data_type in {"bool", "byte"}:
        return 1
    if data_type in {"word", "int"}:
        return 2
    if data_type in {"dword", "dint", "real", "unix_time_seconds"}:
        return 4
    if data_type == "string":
        return int(signal.get("max_length", signal.get("length", 0)))
    return 1


def _signal_end(signal: Mapping[str, Any]) -> int:
    address = _parse_address(signal.get("address"))
    if address is None:
        return 0
    return int(address["byte"]) + _signal_size(signal)


def _as_int(value: object, default: int) -> int:
    return value if type(value) is int else default


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")
