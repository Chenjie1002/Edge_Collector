from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
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


@dataclass(frozen=True)
class ConfigNotFound:
    config_hash: str
    status: str = "not_found"


class InMemoryResolvedConfigRegistry:
    def __init__(self, snapshots: Mapping[str, ResolvedConfigSnapshot]) -> None:
        self._snapshots = dict(snapshots)

    def lookup_resolved_config(self, config_hash: str) -> ResolvedConfigSnapshot | ConfigNotFound:
        return self._snapshots.get(config_hash) or ConfigNotFound(config_hash)
