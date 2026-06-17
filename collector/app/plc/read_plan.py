from __future__ import annotations

from dataclasses import dataclass

from app.plc.address import byte_size_for_type
from app.plc.mapping import EdgeMapping, FieldMapping


@dataclass(frozen=True)
class ReadPlan:
    scope: str
    db_number: int
    read_start: int
    read_size: int
    fields: tuple[FieldMapping, ...]

    @property
    def read_end(self) -> int:
        return self.read_start + self.read_size


def build_read_plans(mapping: EdgeMapping) -> list[ReadPlan]:
    plans: list[ReadPlan] = []
    if mapping.line_fields:
        plans.append(_build_plan("line", mapping.line_fields))
    for station in mapping.stations:
        plans.append(_build_plan(station.station_id, station.fields))
    return plans


def _build_plan(scope: str, fields: tuple[FieldMapping, ...]) -> ReadPlan:
    if not fields:
        raise ValueError(f"No fields found for read plan scope {scope}")

    db_numbers = {field.address.db_number for field in fields}
    if len(db_numbers) != 1:
        raise ValueError(f"Read plan scope {scope} spans multiple DB blocks: {sorted(db_numbers)}")

    read_start = min(field.address.byte_offset for field in fields)
    read_end = max(
        field.address.byte_offset + byte_size_for_type(field.data_type, field.max_length)
        for field in fields
    )
    return ReadPlan(
        scope=scope,
        db_number=db_numbers.pop(),
        read_start=read_start,
        read_size=read_end - read_start,
        fields=fields,
    )
