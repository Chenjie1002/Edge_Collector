from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from typing import Any

from app.plc.mapping import RuntimeMappingSnapshot, runtime_mapping_hash_content


RawDecoder = Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]]


@dataclass(frozen=True)
class RouteEdgeSnapshot:
    from_station_id: str
    to_station_id: str


@dataclass(frozen=True)
class RouteGraphSnapshot:
    edges: tuple[RouteEdgeSnapshot, ...]


@dataclass(frozen=True)
class ResolvedStationSnapshot:
    station_id: str
    plc_id: str
    station_type: str
    cycle_profile: str
    mapping_id: str
    payload_template: str
    raw_policy: str
    decoder: RawDecoder | None = None
    station_enabled: bool = True
    line_id: str | None = None
    station_order: int | None = None
    nok_template: str | None = None
    decoder_id: str | None = None
    source_namespace: str | None = None
    db_number: int | None = None
    db_read_layout: tuple[str, ...] = ()
    direct_predecessor_station_id: str | None = None


@dataclass(frozen=True)
class ResolvedConfigSnapshot:
    config_hash: str
    config_version: str
    line_id: str
    stations: tuple[ResolvedStationSnapshot, ...]
    route_graph: RouteGraphSnapshot
    schema_version: str = "runtime-mapping/v1"
    authoritative_source: str = "unknown"
    timezone: str = "Asia/Shanghai"
    hash_algorithm: str = "sha256"
    plc_identity_namespace: str = "default"
    interpretation_code_tables: dict[str, dict[str, Any]] | None = None

    def compute_content_hash(self) -> str:
        return compute_resolved_config_hash(self)

    def with_content_hash(self) -> "ResolvedConfigSnapshot":
        return replace(self, config_hash=self.compute_content_hash())

    def content_hash_matches(self) -> bool:
        return self.compute_content_hash() == self.config_hash

    def station_for(self, station_id: str) -> ResolvedStationSnapshot | None:
        return next((station for station in self.stations if station.station_id == station_id), None)

    def decode_raw_payload(
        self,
        raw_payload: Mapping[str, Any],
        event: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        station = self.station_for(str(event.get("station_id", "")))
        decoder = station.decoder if station is not None else None
        if decoder is None:
            raise ValueError("decoder missing")
        return decoder(raw_payload, event)


def compute_resolved_config_hash(snapshot: ResolvedConfigSnapshot) -> str:
    content = {
        "schema_version": snapshot.schema_version,
        "config_version": snapshot.config_version,
        "authoritative_source": snapshot.authoritative_source,
        "line_id": snapshot.line_id,
        "timezone": snapshot.timezone,
        "hash_algorithm": snapshot.hash_algorithm,
        "plc_identity_namespace": snapshot.plc_identity_namespace,
        "route_graph": [
            {
                "from_station_id": edge.from_station_id,
                "to_station_id": edge.to_station_id,
            }
            for edge in sorted(
                snapshot.route_graph.edges,
                key=lambda item: (item.from_station_id, item.to_station_id),
            )
        ],
        "interpretation_code_tables": snapshot.interpretation_code_tables or {},
        "stations": [
            {
                "station_id": station.station_id,
                "line_id": station.line_id,
                "station_order": station.station_order,
                "station_enabled": station.station_enabled,
                "plc_id": station.plc_id,
                "station_type": station.station_type,
                "cycle_profile": station.cycle_profile,
                "mapping_id": station.mapping_id,
                "payload_template": station.payload_template,
                "nok_template": station.nok_template,
                "raw_policy": station.raw_policy,
                "decoder_id": station.decoder_id or _decoder_identity(station.decoder),
                "source_namespace": station.source_namespace,
                "db_number": station.db_number,
                "db_read_layout": list(station.db_read_layout),
                "direct_predecessor_station_id": station.direct_predecessor_station_id,
            }
            for station in sorted(snapshot.stations, key=lambda item: item.station_id)
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


def build_resolved_config_snapshot_from_mapping(
    mapping_snapshot: RuntimeMappingSnapshot,
) -> ResolvedConfigSnapshot:
    if not mapping_snapshot.content_hash_matches():
        raise ValueError("CONFIG_HASH_MISMATCH")
    candidate = ResolvedConfigSnapshot(
        config_hash=mapping_snapshot.config_hash,
        config_version=mapping_snapshot.config_version,
        line_id=mapping_snapshot.line_id,
        stations=tuple(
            ResolvedStationSnapshot(
                station_id=station.station_id,
                line_id=station.line_id,
                plc_id=station.plc_id,
                station_type=station.station_type,
                cycle_profile=station.cycle_profile,
                mapping_id=station.mapping_id,
                payload_template=station.payload_template,
                raw_policy=station.raw_policy,
                station_enabled=station.station_enabled,
                station_order=station.station_order,
                nok_template=station.nok_template,
                decoder_id=station.decoder_id,
                source_namespace=station.source_namespace,
                db_number=station.db_number,
                db_read_layout=station.db_read_layout,
                direct_predecessor_station_id=station.direct_predecessor_station_id,
            )
            for station in mapping_snapshot.stations
        ),
        route_graph=RouteGraphSnapshot(
            edges=tuple(
                RouteEdgeSnapshot(
                    from_station_id=edge.from_station_id,
                    to_station_id=edge.to_station_id,
                )
                for edge in mapping_snapshot.route_graph
            )
        ),
        schema_version=mapping_snapshot.schema_version,
        authoritative_source=mapping_snapshot.authoritative_source,
        timezone=mapping_snapshot.timezone,
        hash_algorithm=mapping_snapshot.hash_algorithm,
        plc_identity_namespace=mapping_snapshot.plc_identity_namespace,
        interpretation_code_tables=dict(mapping_snapshot.interpretation_code_tables),
    )
    if candidate.compute_content_hash() != mapping_snapshot.config_hash:
        # Keep this construction coupled to the runtime mapping hash surface.
        mapping_content = runtime_mapping_hash_content(mapping_snapshot)
        resolved_content = json.loads(
            json.dumps(
                {
                    "schema_version": candidate.schema_version,
                    "config_version": candidate.config_version,
                    "authoritative_source": candidate.authoritative_source,
                    "line_id": candidate.line_id,
                    "timezone": candidate.timezone,
                    "hash_algorithm": candidate.hash_algorithm,
                    "plc_identity_namespace": candidate.plc_identity_namespace,
                    "route_graph": [
                        {
                            "from_station_id": edge.from_station_id,
                            "to_station_id": edge.to_station_id,
                        }
                        for edge in sorted(
                            candidate.route_graph.edges,
                            key=lambda item: (item.from_station_id, item.to_station_id),
                        )
                    ],
                    "interpretation_code_tables": candidate.interpretation_code_tables or {},
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
                            "source_namespace": station.source_namespace,
                            "db_number": station.db_number,
                            "db_read_layout": list(station.db_read_layout),
                            "direct_predecessor_station_id": station.direct_predecessor_station_id,
                        }
                        for station in sorted(candidate.stations, key=lambda item: item.station_id)
                    ],
                }
            )
        )
        if resolved_content != mapping_content:
            raise ValueError("CONFIG_HASH_MISMATCH")
    return candidate


def _decoder_identity(decoder: RawDecoder | None) -> str | None:
    if decoder is None:
        return None
    module = getattr(decoder, "__module__", "")
    qualname = getattr(decoder, "__qualname__", repr(decoder))
    return f"{module}.{qualname}"


@dataclass(frozen=True)
class ConfigNotFound:
    config_hash: str
    status: str = "not_found"


@dataclass(frozen=True)
class ConfigHashMismatch:
    requested_config_hash: str
    config_hash: str = ""
    status: str = "hash_mismatch"


class InMemoryResolvedConfigRegistry:
    def __init__(self, snapshots: Mapping[str, ResolvedConfigSnapshot]) -> None:
        self._snapshots = dict(snapshots)

    def lookup_resolved_config(
        self,
        config_hash: str,
    ) -> ResolvedConfigSnapshot | ConfigNotFound | ConfigHashMismatch:
        snapshot = self._snapshots.get(config_hash)
        if snapshot is None:
            return ConfigNotFound(config_hash)
        if not isinstance(snapshot, ResolvedConfigSnapshot):
            return ConfigHashMismatch(config_hash)
        if snapshot.config_hash != config_hash or not snapshot.content_hash_matches():
            return ConfigHashMismatch(config_hash)
        return snapshot
