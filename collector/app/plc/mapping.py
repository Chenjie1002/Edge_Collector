from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from app.plc.address import S7Address, parse_s7_address


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


@dataclass(frozen=True)
class EdgeMapping:
    version: int
    timezone: str
    plcs: tuple[dict[str, Any], ...]
    line_id: str
    line_fields: tuple[FieldMapping, ...]
    stations: tuple[StationMapping, ...]
    code_tables: dict[str, dict[Any, Any]]


def load_edge_mapping(path: str | Path = "/app/config/mapping.yaml") -> EdgeMapping:
    raw = yaml.safe_load(Path(path).read_text()) or {}
    return parse_edge_mapping(raw)


def parse_edge_mapping(raw: dict[str, Any]) -> EdgeMapping:
    template_header = raw.get("station_template", {}).get("header", {})
    line = raw.get("line", {})

    line_fields = tuple(
        _parse_field(name, cfg, group="line")
        for name, cfg in (line.get("fields") or {}).items()
    )

    stations: list[StationMapping] = []
    for station_raw in raw.get("stations", []):
        db_number = int(station_raw["db_number"])
        db_token = f"DB{db_number}"
        fields: list[FieldMapping] = []

        for name, cfg in template_header.items():
            fields.extend(_parse_field_or_array(name, cfg, db_token, group="header"))

        for name, cfg in (station_raw.get("payload") or {}).items():
            fields.extend(_parse_field_or_array(name, cfg, db_token, group="payload"))

        stations.append(
            StationMapping(
                station_id=str(station_raw["station_id"]),
                name=str(station_raw.get("name", station_raw["station_id"])),
                db_number=db_number,
                upstream_station_id=station_raw.get("upstream_station_id"),
                dmc_role=station_raw.get("dmc_role"),
                fields=tuple(fields),
            )
        )

    return EdgeMapping(
        version=int(raw.get("version", 1)),
        timezone=str(raw.get("timezone", "Asia/Shanghai")),
        plcs=tuple(raw.get("plcs", [])),
        line_id=str(line.get("line_id", "LINE_001")),
        line_fields=line_fields,
        stations=tuple(stations),
        code_tables=raw.get("code_tables", {}),
    )


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
