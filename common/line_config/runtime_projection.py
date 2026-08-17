from __future__ import annotations

import copy
import hashlib
import json
import re
from collections.abc import Mapping
from typing import Any

from .debug_contract import (
    debug_contract_content_hash,
    debug_contract_from_candidate,
)
from .models import LineConfig, StationConfig
from .runtime_layout import RuntimeLayoutRegistry, default_runtime_layout_registry


class RuntimeProjectionError(ValueError):
    def __init__(self, message: str, *, classification: str = "RUNTIME_PROJECTION_INVALID") -> None:
        self.classification = classification
        super().__init__(message)


class RuntimeMappingProjection:
    def __init__(
        self,
        document: dict[str, object],
        projection_hash: str,
        line_config_hash: str,
    ) -> None:
        self.document = document
        self.projection_hash = projection_hash
        self.line_config_hash = line_config_hash


def compile_runtime_mapping(
    config: LineConfig,
    connectivity: Mapping[str, object],
    layout_registry: RuntimeLayoutRegistry | None = None,
    *,
    line_config_source: str | None = None,
    debug_contract: Mapping[str, object] | None = None,
) -> RuntimeMappingProjection:
    registry = layout_registry or default_runtime_layout_registry()
    plc = _validate_runtime_scope(config)
    connection = _normalize_connectivity(connectivity)
    ordered_stations = [station for station in config.stations if station.station_enabled]
    _validate_linear_route(config, ordered_stations, plc.plc_id)

    db_by_station: dict[str, int] = {}
    for station in ordered_stations:
        db_by_station[station.station_id] = _station_db_number(station, plc.runtime_db)
    if len(set(db_by_station.values())) != len(db_by_station):
        raise RuntimeProjectionError("station DB allocation is not unique")

    route_ids = [station.station_id for station in ordered_stations]
    edges = [
        {
            "from_station_id": from_station,
            "to_station_id": to_station,
        }
        for from_station, to_station in zip(route_ids, route_ids[1:])
    ]
    predecessor = {edge["to_station_id"]: edge["from_station_id"] for edge in edges}

    line_config_hash = f"sha256:{config.config_hash}"
    decoder_registry_hash = _decoder_registry_content_hash(registry, ordered_stations)
    station_documents = [
        _station_document(
            config,
            station,
            ordinal,
            db_by_station[station.station_id],
            predecessor.get(station.station_id),
            registry,
        )
        for ordinal, station in enumerate(ordered_stations, start=1)
    ]
    document: dict[str, object] = {
        "schema_version": "runtime-mapping/v1",
        "config_version": config.config_version,
        "authoritative_source": line_config_source or "LineConfig",
        "line_id": config.line_id,
        "line_config_hash": line_config_hash,
        "hash_algorithm": "sha256",
        "timezone": config.timezone,
        "version": 1,
        "plc_identity_namespace": f"vplc-db{plc.runtime_db}",
        "decoder_registry": {
            "snapshot_id": registry.snapshot_id,
            "content_hash": decoder_registry_hash,
        },
        "layout_registry": {
            "snapshot_id": registry.snapshot_id,
            "content_hash": registry.content_hash,
        },
        "runtime_defaults": {
            "station_enabled": True,
            "plc_id": plc.plc_id,
            "raw_policy": "raw_capable",
            "decoder_id": registry.decoder_id,
            "decoder_version": registry.decoder_version,
            "source_namespace": f"vplc-db{min(db_by_station.values())}-db{max(db_by_station.values())}",
        },
        "plcs": [
            {
                "plc_id": plc.plc_id,
                "name": "Virtual S7 Line PLC",
                "host": connection["host"],
                "port": connection["port"],
                "rack": connection["rack"],
                "slot": connection["slot"],
                "connection_timeout_ms": connection["connection_timeout_ms"],
                "poll_interval_ms": connection["poll_interval_ms"],
                "runtime_db": plc.runtime_db,
                "line_id": config.line_id,
            }
        ],
        "line": {
            "line_id": config.line_id,
            "name": config.name,
            "db_number": plc.runtime_db,
            "fields": {
                "protocol_version": {
                    "address": f"DB{plc.runtime_db}.DBW0",
                    "type": "word",
                },
                "heartbeat_counter": {
                    "address": f"DB{plc.runtime_db}.DBD4",
                    "type": "dint",
                },
                "plc_restart_counter": {
                    "address": f"DB{plc.runtime_db}.DBD8",
                    "type": "dint",
                },
                "plc_boot_id": {
                    "address": f"DB{plc.runtime_db}.DBB12",
                    "type": "string",
                    "max_length": 36,
                },
                "ignore_edge": {
                    "address": f"DB{plc.runtime_db}.DBX52.3",
                    "type": "bool",
                },
            },
        },
        "station_template": {"header": copy.deepcopy(registry.common_header)},
        "entry_station_id": config.route_graph.entry_station_id,
        "terminal_station_id": config.route_graph.terminal_station_id,
        "topology": {
            "entry_station_id": config.route_graph.entry_station_id,
            "terminal_station_id": config.route_graph.terminal_station_id,
            "station_ids": route_ids,
            "edges": copy.deepcopy(edges),
        },
        "route_graph": edges,
        "stations": station_documents,
        "code_tables": _code_tables(config, registry, route_ids),
        "execution_profile": {
            # Scenario semantics remain LineConfig metadata.  V-PLC execution
            # policy is deliberately limited to the profiles owned by
            # vplc.yaml; the normal projection is the safe runtime baseline.
            "mode": "normal",
            "cycle_scale": 1.0,
            "edit_policy": "projection_owned",
        },
    }
    if debug_contract is not None:
        contract = debug_contract_from_candidate(debug_contract)
        selected_ids = _debug_scope_station_ids(contract, route_ids)
        station_by_id = {station.station_id: station for station in ordered_stations}
        selected_stations = [station_by_id.get(station_id) for station_id in selected_ids]
        if any(station is None for station in selected_stations):
            raise RuntimeProjectionError(
                "debug contract scope references a station outside the selected line"
            )
        selected_config_stations = [station for station in selected_stations if station is not None]
        document["base_topology"] = {
            "line_id": config.line_id,
            "entry_station_id": config.route_graph.entry_station_id,
            "terminal_station_id": config.route_graph.terminal_station_id,
            "station_ids": copy.deepcopy(route_ids),
            "edges": copy.deepcopy(edges),
        }
        document["decoder_registry"] = {
            "snapshot_id": registry.snapshot_id,
            "content_hash": _decoder_registry_content_hash(registry, selected_config_stations),
        }
        document["runtime_defaults"] = {
            **document["runtime_defaults"],
            "source_namespace": (
                f"vplc-db{min(db_by_station[station_id] for station_id in selected_ids)}-"
                f"db{max(db_by_station[station_id] for station_id in selected_ids)}"
            ),
        }
        document["code_tables"] = _code_tables(config, registry, selected_ids)
        _apply_debug_contract(document, contract)
        document["debug_contract"] = copy.deepcopy(contract)
        document["debug_contract_hash"] = f"sha256:{debug_contract_content_hash(contract)}"
    projection_digest = _canonical_hash(document)
    projection_hash = f"sha256:{projection_digest}"
    document["projection_hash"] = projection_hash
    return RuntimeMappingProjection(document, projection_hash, line_config_hash)


def _apply_debug_contract(
    document: dict[str, object],
    contract: Mapping[str, object],
) -> None:
    raw_stations = contract.get("stations")
    if not isinstance(raw_stations, list):
        raise RuntimeProjectionError("debug contract stations must be a list")
    contract_by_station = {
        str(item.get("station_id")): item
        for item in raw_stations
        if isinstance(item, Mapping)
    }
    raw_documents = document.get("stations")
    if not isinstance(raw_documents, list):
        raise RuntimeProjectionError("runtime projection has no station documents")
    base_station_ids = [
        str(station.get("station_id", ""))
        for station in raw_documents
        if isinstance(station, Mapping)
    ]
    runtime_by_station = {
        str(item.get("station_id")): item
        for item in raw_documents
        if isinstance(item, Mapping)
    }
    selected_ids = _debug_scope_station_ids(contract, base_station_ids)
    selected_documents: list[dict[str, object]] = []
    for ordinal, station_id in enumerate(selected_ids, start=1):
        source_station = runtime_by_station.get(station_id)
        if not isinstance(source_station, Mapping):
            raise RuntimeProjectionError(
                f"debug contract does not define runtime station {station_id}"
            )
        station = copy.deepcopy(dict(source_station))
        selected = contract_by_station.get(station_id)
        assert selected is not None
        db_number = selected.get("db_number")
        read_start = selected.get("read_start")
        read_length = selected.get("read_length")
        if type(db_number) is not int or type(read_start) is not int or type(read_length) is not int:
            raise RuntimeProjectionError(
                f"debug contract range is invalid for runtime station {station_id}"
            )
        signals = selected.get("signals")
        if not isinstance(signals, list) or not signals:
            raise RuntimeProjectionError(
                f"debug contract has no signals for runtime station {station_id}"
            )
        header: dict[str, dict[str, object]] = {}
        payload: dict[str, dict[str, object]] = {}
        all_fields: dict[str, dict[str, object]] = {}
        for signal in signals:
            if not isinstance(signal, Mapping):
                raise RuntimeProjectionError(
                    f"debug contract signal is invalid for runtime station {station_id}"
                )
            field_name = str(signal.get("field_name", ""))
            address = str(signal.get("address", ""))
            data_type = str(signal.get("type", ""))
            direction = str(signal.get("direction", "PLC_TO_EDGE"))
            if direction == "EDGE_TO_PLC" and field_name != "read_done":
                raise RuntimeProjectionError(
                    "debug contract permits only read_done as an Edge-to-PLC field"
                )
            runtime_direction = {
                "PLC_TO_EDGE": "read",
                "READ_WRITE": "read_write",
                "EDGE_TO_PLC": "read_write",
            }.get(direction)
            if runtime_direction is None:
                raise RuntimeProjectionError(
                    f"debug contract direction is invalid for {field_name}"
                )
            field: dict[str, object] = {
                "address": address,
                "type": data_type,
                "direction": runtime_direction,
                "required": bool(signal.get("required", True)),
            }
            if signal.get("max_length") is not None:
                field["max_length"] = signal.get("max_length")
            all_fields[field_name] = field
            group = str(signal.get("group", "header"))
            if group == "payload":
                payload[field_name] = field
            else:
                header[field_name] = field
        if "read_done" not in all_fields:
            raise RuntimeProjectionError(
                f"debug contract has no read_done field for runtime station {station_id}"
            )
        station["db_number"] = db_number
        station["station_order"] = ordinal
        station["upstream_station_id"] = selected_ids[ordinal - 2] if ordinal > 1 else None
        station["source_namespace"] = f"vplc-db{db_number}"
        station["debug_read_start"] = read_start
        station["debug_read_length"] = read_length
        station["effective_read_size_bytes"] = read_length
        station["header"] = header
        # The current Collector mapping loader consumes the shared
        # station_template plus each station payload.  Keeping the complete
        # candidate field set in the station payload makes per-station edits
        # executable without changing Collector source.
        station["payload"] = all_fields
        station["db_read_layout"] = sorted(all_fields)
        selected_documents.append(station)
    if not selected_documents:
        raise RuntimeProjectionError("debug contract scope must select at least one runtime station")
    edges = [
        {
            "from_station_id": from_station,
            "to_station_id": to_station,
        }
        for from_station, to_station in zip(selected_ids, selected_ids[1:])
    ]
    document["stations"] = selected_documents
    document["entry_station_id"] = selected_ids[0]
    document["terminal_station_id"] = selected_ids[-1]
    document["topology"] = {
        "entry_station_id": selected_ids[0],
        "terminal_station_id": selected_ids[-1],
        "station_ids": copy.deepcopy(selected_ids),
        "edges": copy.deepcopy(edges),
    }
    document["route_graph"] = edges
    document["debug_scope"] = {"station_ids": copy.deepcopy(selected_ids)}
    document["station_template"] = {"header": {}}


def _debug_scope_station_ids(
    contract: Mapping[str, object],
    fallback_station_ids: list[str],
) -> list[str]:
    raw_scope = contract.get("debug_scope")
    if isinstance(raw_scope, Mapping):
        raw_scope = raw_scope.get("station_ids")
    if not isinstance(raw_scope, list) or not raw_scope:
        return list(fallback_station_ids)
    selected_ids = [str(item) for item in raw_scope]
    if len(set(selected_ids)) != len(selected_ids):
        raise RuntimeProjectionError("debug contract scope contains duplicate stations")
    fallback_order = {station_id: index for index, station_id in enumerate(fallback_station_ids)}
    if any(station_id not in fallback_order for station_id in selected_ids):
        raise RuntimeProjectionError("debug contract scope references an unknown station")
    return sorted(selected_ids, key=lambda station_id: fallback_order[station_id])


def _validate_runtime_scope(config: LineConfig):
    if len(config.plcs) != 1:
        raise RuntimeProjectionError(
            "MULTI_PLC_RUNTIME_UNSUPPORTED: R3 requires exactly one PLC",
            classification="MULTI_PLC_RUNTIME_UNSUPPORTED",
        )
    if len([station for station in config.stations if station.station_enabled]) not in {3, 10}:
        raise RuntimeProjectionError(
            "UNSUPPORTED_RUNTIME_STATION_COUNT: R3 supports only 3WS and 10WS",
            classification="UNSUPPORTED_RUNTIME_STATION_COUNT",
        )
    return config.plcs[0]


def _validate_linear_route(config: LineConfig, stations: list[StationConfig], plc_id: str) -> None:
    station_ids = [station.station_id for station in stations]
    if config.route_graph.entry_station_id != station_ids[0]:
        raise RuntimeProjectionError("route entry is not the first enabled station")
    if config.route_graph.terminal_station_id != station_ids[-1]:
        raise RuntimeProjectionError("route terminal is not the last enabled station")
    expected_edges = list(zip(station_ids, station_ids[1:]))
    actual_edges = [
        (edge.from_station_id, edge.to_station_id) for edge in config.route_graph.edges
    ]
    if actual_edges != expected_edges:
        raise RuntimeProjectionError(
            "NON_LINEAR_ROUTE_UNSUPPORTED: route edges must be the ordered single linear path",
            classification="NON_LINEAR_ROUTE_UNSUPPORTED",
        )
    if any(station.plc_id != plc_id for station in stations):
        raise RuntimeProjectionError("all enabled stations must belong to the single PLC")


def _normalize_connectivity(connectivity: Mapping[str, object]) -> dict[str, object]:
    required = ("host", "port", "rack", "slot", "connection_timeout_ms", "poll_interval_ms")
    missing = [key for key in required if key not in connectivity]
    if missing:
        raise RuntimeProjectionError(f"PLC connectivity missing fields: {', '.join(missing)}")
    host = connectivity["host"]
    if not isinstance(host, str) or not host.strip():
        raise RuntimeProjectionError("PLC connectivity host must be non-empty text")
    normalized: dict[str, object] = {"host": host.strip()}
    for key in required[1:]:
        value = connectivity[key]
        if type(value) is not int:
            raise RuntimeProjectionError(f"PLC connectivity {key} must be an integer")
        normalized[key] = value
    return normalized


def _station_db_number(station: StationConfig, runtime_db: int) -> int:
    candidates = [
        mapping
        for mapping in station.db_mappings
        if mapping.usage in {"event", "status"}
    ]
    mapping = sorted(candidates or list(station.db_mappings), key=lambda item: item.mapping_id)[0]
    if mapping.db_number == runtime_db:
        raise RuntimeProjectionError(
            f"station {station.station_id} DB {runtime_db} conflicts with runtime DB"
        )
    return mapping.db_number


def _station_document(
    config: LineConfig,
    station: StationConfig,
    ordinal: int,
    db_number: int,
    upstream_station_id: str | None,
    registry: RuntimeLayoutRegistry,
) -> dict[str, object]:
    try:
        payload = copy.deepcopy(registry.payload_for(station.payload_template))
    except KeyError as exc:
        raise RuntimeProjectionError(str(exc)) from exc
    payload = {
        name: _replace_db_token(field, db_number)
        for name, field in payload.items()
    }
    header = {
        name: _replace_db_token(field, db_number)
        for name, field in registry.common_header.items()
        if field.get("type") != "array"
    }
    effective_read_size = _max_field_end(registry.common_header, db_number)
    effective_read_size = max(effective_read_size, _max_field_end(payload, db_number))
    mapping_id = sorted(station.db_mappings, key=lambda item: item.mapping_id)[0].mapping_id
    return {
        "station_id": station.station_id,
        "line_id": config.line_id,
        "name": station.station_id,
        "db_number": db_number,
        "station_order": ordinal,
        "line_config_station_order": station.station_order,
        "mapping_id": mapping_id,
        "station_type": station.station_type,
        "station_enabled": station.station_enabled,
        "plc_id": station.plc_id,
        "cycle_profile": station.cycle_profile,
        "cycle_time_s": station.cycle_time_s,
        "nok_rate": station.effective_nok_rate,
        "payload_template": station.payload_template,
        "nok_template": station.nok_template,
        "raw_policy": "raw_capable",
        "decoder_id": registry.decoder_id,
        "decoder_version": registry.decoder_version,
        "source_namespace": f"vplc-db{db_number}",
        "upstream_station_id": upstream_station_id,
        "header": header,
        "payload": payload,
        "effective_read_size_bytes": effective_read_size,
        "db_read_layout": sorted([*header, *payload]),
    }


def _replace_db_token(field: dict[str, Any], db_number: int) -> dict[str, Any]:
    replaced = copy.deepcopy(field)
    if "address" in replaced:
        replaced["address"] = str(replaced["address"]).format(db=f"DB{db_number}")
    if replaced.get("type") == "array":
        replaced["items"] = [_replace_db_token(item, db_number) for item in replaced.get("items", [])]
    return replaced


def _max_field_end(fields: Mapping[str, Any], db_number: int) -> int:
    max_end = 0
    for field in fields.values():
        if field.get("type") == "array":
            max_end = max(max_end, _max_field_end({str(index): item for index, item in enumerate(field["items"])}, db_number))
            continue
        address = str(field.get("address", ""))
        match = re.search(r"\.DB([BWD])([0-9]+)", address)
        if not match:
            continue
        offset = int(match.group(2))
        data_type = str(field.get("type"))
        size = {
            "bool": 1,
            "word": 2,
            "dint": 4,
            "real": 4,
            "unix_time_seconds": 4,
            "string": int(field.get("max_length", 40)),
            "bytes": int(field.get("length", 1)),
        }.get(data_type, 1)
        max_end = max(max_end, offset + size)
    return max_end


def _code_tables(
    config: LineConfig,
    registry: RuntimeLayoutRegistry,
    station_ids: list[str],
) -> dict[str, dict[int, str]]:
    tables = copy.deepcopy(registry.code_tables)
    tables["station_code"] = {index: station_id for index, station_id in enumerate(station_ids, start=1)}
    nok_codes: dict[int, str] = {}
    for template in config.nok_templates:
        for code in template.codes:
            nok_codes[code.code] = code.name
    tables["nok_codes"] = nok_codes
    return tables


def _decoder_registry_content_hash(
    registry: RuntimeLayoutRegistry,
    stations: list[StationConfig],
) -> str:
    decoders = sorted(
        {
            (
                registry.decoder_id,
                registry.decoder_version,
                station.payload_template or "",
            )
            for station in stations
        }
    )
    content = {
        "schema_version": "decoder-registry/v1",
        "registry_snapshot_id": registry.snapshot_id,
        "hash_algorithm": "sha256",
        "decoders": [
            {
                "decoder_id": decoder_id,
                "decoder_version": decoder_version,
                "callable_ref": registry.decoder_id,
                "payload_template": payload_template,
            }
            for decoder_id, decoder_version, payload_template in decoders
        ],
    }
    return _canonical_hash(content)


def _canonical_hash(content: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        content,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
