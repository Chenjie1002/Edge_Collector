from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from typing import Any


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


@dataclass(frozen=True)
class ResolvedConfigSnapshot:
    config_hash: str
    config_version: str
    line_id: str
    stations: tuple[ResolvedStationSnapshot, ...]
    route_graph: RouteGraphSnapshot

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
        "config_version": snapshot.config_version,
        "line_id": snapshot.line_id,
        "route_graph": {
            "edges": [
                {
                    "from_station_id": edge.from_station_id,
                    "to_station_id": edge.to_station_id,
                }
                for edge in snapshot.route_graph.edges
            ],
        },
        "stations": [
            {
                "station_id": station.station_id,
                "plc_id": station.plc_id,
                "station_type": station.station_type,
                "cycle_profile": station.cycle_profile,
                "mapping_id": station.mapping_id,
                "payload_template": station.payload_template,
                "raw_policy": station.raw_policy,
                "decoder": _decoder_identity(station.decoder),
                "station_enabled": station.station_enabled,
            }
            for station in snapshot.stations
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


class InMemoryResolvedConfigRegistry:
    def __init__(self, snapshots: Mapping[str, ResolvedConfigSnapshot]) -> None:
        self._snapshots = dict(snapshots)

    def lookup_resolved_config(self, config_hash: str) -> ResolvedConfigSnapshot | ConfigNotFound:
        return self._snapshots.get(config_hash) or ConfigNotFound(config_hash)
