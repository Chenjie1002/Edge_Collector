from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from app.plc.address import S7Address, parse_s7_address


class RuntimeMappingContractError(ValueError):
    pass


@dataclass(frozen=True)
class FieldMapping:
    name: str
    address: S7Address
    data_type: str
    direction: str = "read"
    required: bool = True
    max_length: int | None = None
    group: str = "payload"


@dataclass(frozen=True)
class StationMapping:
    station_id: str
    name: str
    db_number: int
    upstream_station_id: str | None
    dmc_role: str | None
    fields: tuple[FieldMapping, ...]
    station_order: int | None = None
    station_enabled: bool = True
    plc_id: str | None = None
    mapping_id: str | None = None
    station_type: str | None = None
    cycle_profile: str | None = None
    payload_template: str | None = None
    nok_template: str | None = None
    raw_policy: str | None = None
    decoder_id: str | None = None
    decoder_version: str | None = None
    source_namespace: str | None = None


@dataclass(frozen=True)
class RouteEdgeMapping:
    from_station_id: str
    to_station_id: str


@dataclass(frozen=True)
class RuntimeStationMapping:
    station_id: str
    line_id: str
    station_order: int
    station_enabled: bool
    plc_id: str
    mapping_id: str
    station_type: str
    cycle_profile: str
    payload_template: str
    nok_template: str
    raw_policy: str
    decoder_id: str
    decoder_version: str
    source_namespace: str
    db_number: int
    db_read_layout: tuple[str, ...]
    db_read_fields: tuple[FieldMapping, ...] = ()
    direct_predecessor_station_id: str | None = None


@dataclass(frozen=True)
class RuntimeMappingSnapshot:
    schema_version: str
    config_version: str
    authoritative_source: str
    line_id: str
    timezone: str
    hash_algorithm: str
    plc_identity_namespace: str
    decoder_registry_snapshot_id: str
    decoder_registry_content_hash: str
    stations: tuple[RuntimeStationMapping, ...]
    route_graph: tuple[RouteEdgeMapping, ...]
    interpretation_code_tables: dict[str, dict[str, Any]]
    config_hash: str = ""

    def station_for(self, station_id: str) -> RuntimeStationMapping | None:
        return next((station for station in self.stations if station.station_id == station_id), None)

    def content_hash_matches(self) -> bool:
        return compute_runtime_mapping_hash(self) == self.config_hash


@dataclass(frozen=True)
class EdgeMapping:
    version: int
    timezone: str
    plcs: tuple[dict[str, Any], ...]
    line_id: str
    line_fields: tuple[FieldMapping, ...]
    stations: tuple[StationMapping, ...]
    code_tables: dict[str, dict[Any, Any]]
    schema_version: str = "runtime-mapping/v1"
    config_version: str = "legacy-runtime"
    authoritative_source: str = "config/mapping.yaml"
    hash_algorithm: str = "sha256"
    plc_identity_namespace: str = "default"
    decoder_registry_snapshot_id: str | None = None
    decoder_registry_content_hash: str | None = None
    runtime_snapshot: RuntimeMappingSnapshot | None = None


def load_edge_mapping(path: str | Path = "/app/config/mapping.yaml") -> EdgeMapping:
    raw = yaml.safe_load(Path(path).read_text()) or {}
    return parse_edge_mapping(raw)


def parse_edge_mapping(raw: dict[str, Any]) -> EdgeMapping:
    template_header = raw.get("station_template", {}).get("header", {})
    line = raw.get("line", {})
    runtime_defaults = raw.get("runtime_defaults") or {}
    schema_version = _required(raw, "schema_version")
    config_version = _required(raw, "config_version")
    authoritative_source = _required(raw, "authoritative_source")
    line_id = _required(raw, "line_id", line.get("line_id"))
    timezone = _required(raw, "timezone")
    hash_algorithm = _required(raw, "hash_algorithm")
    plc_identity_namespace = _required(raw, "plc_identity_namespace")
    if hash_algorithm != "sha256":
        raise RuntimeMappingContractError("hash_algorithm must be sha256")
    decoder_registry = raw.get("decoder_registry") or {}
    decoder_registry_snapshot_id = str(
        _required(decoder_registry, "snapshot_id", _missing_key="decoder_registry.snapshot_id")
    )
    decoder_registry_content_hash = str(
        _required(decoder_registry, "content_hash", _missing_key="decoder_registry.content_hash")
    )
    if len(decoder_registry_content_hash) != 64:
        raise RuntimeMappingContractError("decoder_registry.content_hash must be a sha256 hex digest")

    line_fields = tuple(
        _parse_field(name, cfg, group="line")
        for name, cfg in (line.get("fields") or {}).items()
    )

    stations: list[StationMapping] = []
    runtime_stations: list[RuntimeStationMapping] = []
    for station_raw in raw.get("stations", []):
        db_number = int(station_raw["db_number"])
        db_token = f"DB{db_number}"
        fields: list[FieldMapping] = []

        for name, cfg in template_header.items():
            fields.extend(_parse_field_or_array(name, cfg, db_token, group="header"))

        for name, cfg in (station_raw.get("payload") or {}).items():
            fields.extend(_parse_field_or_array(name, cfg, db_token, group="payload"))

        runtime_station = _parse_runtime_station(
            station_raw=station_raw,
            defaults=runtime_defaults,
            fields=fields,
            db_number=db_number,
            line_id=line_id,
        )
        runtime_stations.append(runtime_station)
        stations.append(
            StationMapping(
                station_id=str(station_raw["station_id"]),
                name=str(station_raw.get("name", station_raw["station_id"])),
                db_number=db_number,
                upstream_station_id=station_raw.get("upstream_station_id"),
                dmc_role=station_raw.get("dmc_role"),
                fields=tuple(fields),
                station_order=runtime_station.station_order,
                station_enabled=runtime_station.station_enabled,
                plc_id=runtime_station.plc_id,
                mapping_id=runtime_station.mapping_id,
                station_type=runtime_station.station_type,
                cycle_profile=runtime_station.cycle_profile,
                payload_template=runtime_station.payload_template,
                nok_template=runtime_station.nok_template,
                raw_policy=runtime_station.raw_policy,
                decoder_id=runtime_station.decoder_id,
                decoder_version=runtime_station.decoder_version,
                source_namespace=runtime_station.source_namespace,
            )
        )

    route_graph = _parse_route_graph(raw.get("route_graph"), runtime_stations)
    expected_decoder_registry_hash = _compute_runtime_decoder_registry_hash(
        decoder_registry_snapshot_id,
        runtime_stations,
    )
    if decoder_registry_content_hash != expected_decoder_registry_hash:
        raise RuntimeMappingContractError("decoder_registry.content_hash mismatch")
    runtime_snapshot = RuntimeMappingSnapshot(
        schema_version=schema_version,
        config_version=config_version,
        authoritative_source=authoritative_source,
        line_id=line_id,
        timezone=timezone,
        hash_algorithm=hash_algorithm,
        plc_identity_namespace=plc_identity_namespace,
        decoder_registry_snapshot_id=decoder_registry_snapshot_id,
        decoder_registry_content_hash=decoder_registry_content_hash,
        stations=tuple(runtime_stations),
        route_graph=route_graph,
        interpretation_code_tables=_interpretation_code_tables(raw.get("code_tables", {})),
    )
    runtime_snapshot = RuntimeMappingSnapshot(
        **{
            **runtime_snapshot.__dict__,
            "config_hash": compute_runtime_mapping_hash(runtime_snapshot),
        }
    )

    return EdgeMapping(
        version=int(raw.get("version", 1)),
        timezone=timezone,
        plcs=tuple(raw.get("plcs", [])),
        line_id=line_id,
        line_fields=line_fields,
        stations=tuple(stations),
        code_tables=raw.get("code_tables", {}),
        schema_version=schema_version,
        config_version=config_version,
        authoritative_source=authoritative_source,
        hash_algorithm=hash_algorithm,
        plc_identity_namespace=plc_identity_namespace,
        decoder_registry_snapshot_id=decoder_registry_snapshot_id,
        decoder_registry_content_hash=decoder_registry_content_hash,
        runtime_snapshot=runtime_snapshot,
    )


def compute_runtime_mapping_hash(snapshot: RuntimeMappingSnapshot) -> str:
    encoded = json.dumps(
        _runtime_hash_content(snapshot),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def runtime_mapping_hash_content(snapshot: RuntimeMappingSnapshot) -> dict[str, Any]:
    return _runtime_hash_content(snapshot)


def _runtime_hash_content(snapshot: RuntimeMappingSnapshot) -> dict[str, Any]:
    return {
        "schema_version": snapshot.schema_version,
        "config_version": snapshot.config_version,
        "authoritative_source": snapshot.authoritative_source,
        "line_id": snapshot.line_id,
        "timezone": snapshot.timezone,
        "hash_algorithm": snapshot.hash_algorithm,
        "plc_identity_namespace": snapshot.plc_identity_namespace,
        "decoder_registry_snapshot_id": snapshot.decoder_registry_snapshot_id,
        "decoder_registry_content_hash": snapshot.decoder_registry_content_hash,
        "route_graph": [
            {
                "from_station_id": edge.from_station_id,
                "to_station_id": edge.to_station_id,
            }
            for edge in sorted(
                snapshot.route_graph,
                key=lambda item: (item.from_station_id, item.to_station_id),
            )
        ],
        "interpretation_code_tables": snapshot.interpretation_code_tables,
        "stations": [
            {
                "station_id": station.station_id,
                "line_id": station.line_id,
                "station_order": station.station_order,
                "station_enabled": station.station_enabled,
                "plc_id": station.plc_id,
                "mapping_id": station.mapping_id,
                "station_type": station.station_type,
                "cycle_profile": station.cycle_profile,
                "payload_template": station.payload_template,
                "nok_template": station.nok_template,
                "raw_policy": station.raw_policy,
                "decoder_id": station.decoder_id,
                "decoder_version": station.decoder_version,
                "source_namespace": station.source_namespace,
                "db_number": station.db_number,
                "db_read_layout": list(station.db_read_layout),
                "db_read_fields": [
                    {
                        "name": field.name,
                        "address": field.address.raw,
                        "data_type": field.data_type,
                        "direction": field.direction,
                        "required": field.required,
                        "max_length": field.max_length,
                        "group": field.group,
                    }
                    for field in sorted(station.db_read_fields, key=lambda item: item.name)
                ],
                "direct_predecessor_station_id": station.direct_predecessor_station_id,
            }
            for station in sorted(snapshot.stations, key=lambda item: item.station_id)
        ],
    }


def _compute_runtime_decoder_registry_hash(
    registry_snapshot_id: str,
    stations: list[RuntimeStationMapping],
) -> str:
    content = {
        "schema_version": "decoder-registry/v1",
        "registry_snapshot_id": registry_snapshot_id,
        "hash_algorithm": "sha256",
        "decoders": [
            {
                "decoder_id": decoder_id,
                "decoder_version": decoder_version,
                "callable_ref": _runtime_decoder_callable_ref(),
                "payload_template": payload_template,
            }
            for decoder_id, decoder_version, payload_template in sorted(
                {
                    (station.decoder_id, station.decoder_version, station.payload_template)
                    for station in stations
                }
            )
        ],
    }
    encoded = json.dumps(
        content,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _runtime_decoder_callable_ref() -> str:
    return "collector.app.plc.decoder.decode_runtime_raw_hex_payload"


def _parse_runtime_station(
    *,
    station_raw: dict[str, Any],
    defaults: dict[str, Any],
    fields: list[FieldMapping],
    db_number: int,
    line_id: str,
) -> RuntimeStationMapping:
    station_id = str(_required(station_raw, "station_id"))
    return RuntimeStationMapping(
        station_id=station_id,
        line_id=line_id,
        station_order=int(_required(station_raw, "station_order", defaults.get("station_order"))),
        station_enabled=bool(_required(station_raw, "station_enabled", defaults.get("station_enabled"))),
        plc_id=str(_required(station_raw, "plc_id", defaults.get("plc_id"))),
        mapping_id=str(_required(station_raw, "mapping_id", defaults.get("mapping_id"))),
        station_type=str(_required(station_raw, "station_type", defaults.get("station_type"))),
        cycle_profile=str(_required(station_raw, "cycle_profile", defaults.get("cycle_profile"))),
        payload_template=str(_required(station_raw, "payload_template", defaults.get("payload_template"))),
        nok_template=str(_required(station_raw, "nok_template", defaults.get("nok_template"))),
        raw_policy=str(_required(station_raw, "raw_policy", defaults.get("raw_policy"))),
        decoder_id=str(_required(station_raw, "decoder_id", defaults.get("decoder_id"))),
        decoder_version=str(_required(station_raw, "decoder_version", defaults.get("decoder_version"))),
        source_namespace=str(_required(station_raw, "source_namespace", defaults.get("source_namespace"))),
        db_number=db_number,
        db_read_layout=tuple(sorted(field.name for field in fields)),
        db_read_fields=tuple(sorted(fields, key=lambda item: item.name)),
        direct_predecessor_station_id=station_raw.get("upstream_station_id"),
    )


def _interpretation_code_tables(raw_code_tables: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    tables: dict[str, dict[str, Any]] = {}
    for table_name in ("result", "nok_codes"):
        raw_table = raw_code_tables.get(table_name, {})
        tables[table_name] = {
            str(key): value
            for key, value in sorted(
                dict(raw_table).items(),
                key=lambda item: str(item[0]),
            )
        }
    return tables


def _parse_route_graph(
    raw_route_graph: Any,
    stations: list[RuntimeStationMapping],
) -> tuple[RouteEdgeMapping, ...]:
    if raw_route_graph is None:
        raw_route_graph = [
            {
                "from_station_id": station.direct_predecessor_station_id,
                "to_station_id": station.station_id,
            }
            for station in stations
            if station.direct_predecessor_station_id is not None
        ]
    edges = tuple(
        RouteEdgeMapping(
            from_station_id=str(_required(edge, "from_station_id")),
            to_station_id=str(_required(edge, "to_station_id")),
        )
        for edge in raw_route_graph
    )
    station_ids = {station.station_id for station in stations}
    for edge in edges:
        if edge.from_station_id not in station_ids or edge.to_station_id not in station_ids:
            raise RuntimeMappingContractError("route_graph references unknown station")
    return edges


def _required(raw: dict[str, Any], key: str, fallback: Any = None, *, _missing_key: str | None = None) -> Any:
    value = raw.get(key, fallback)
    if value is None or value == "":
        raise RuntimeMappingContractError(
            f"missing required runtime mapping field: {_missing_key or key}"
        )
    return value


def _parse_field_or_array(name: str, cfg: dict[str, Any], db_token: str, group: str) -> list[FieldMapping]:
    if cfg.get("type") != "array":
        return [_parse_field(name, cfg, group=group, db_token=db_token)]

    fields: list[FieldMapping] = []
    for index, item_cfg in enumerate(cfg.get("items", []), start=1):
        fields.append(_parse_field(f"{name}_{index}", item_cfg, group=group, db_token=db_token))
    return fields


def _parse_field(
    name: str,
    cfg: dict[str, Any],
    group: str,
    db_token: str | None = None,
) -> FieldMapping:
    raw_address = str(cfg["address"])
    if db_token:
        raw_address = raw_address.format(db=db_token)

    return FieldMapping(
        name=name,
        address=parse_s7_address(raw_address),
        data_type=str(cfg["type"]),
        direction=str(cfg.get("direction", "read")),
        required=bool(cfg.get("required", True)),
        max_length=int(cfg["max_length"]) if cfg.get("max_length") is not None else None,
        group=group,
    )
