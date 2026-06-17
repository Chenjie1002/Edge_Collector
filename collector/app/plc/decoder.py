from __future__ import annotations

import struct
from datetime import datetime
from zoneinfo import ZoneInfo

from snap7 import util

from app.plc.mapping import FieldMapping
from app.plc.read_plan import ReadPlan


def decode_read_plan(data: bytes | bytearray, plan: ReadPlan, timezone: str = "Asia/Shanghai") -> dict[str, object]:
    decoded: dict[str, object] = {}
    for field in plan.fields:
        decoded[field.name] = decode_field(data, plan.read_start, field, timezone)
    return decoded


def decode_field(
    data: bytes | bytearray,
    read_start: int,
    field: FieldMapping,
    timezone: str = "Asia/Shanghai",
) -> object:
    offset = field.address.byte_offset - read_start
    data_type = field.data_type.lower()

    if data_type == "bool":
        if field.address.bit_offset is None:
            raise ValueError(f"Bool field {field.name} requires a bit address")
        return util.get_bool(data, offset, field.address.bit_offset)
    if data_type == "byte":
        return util.get_byte(data, offset)
    if data_type == "word":
        return util.get_int(data, offset)
    if data_type == "int":
        return util.get_int(data, offset)
    if data_type == "dint":
        return util.get_dint(data, offset)
    if data_type == "dword":
        return util.get_dword(data, offset)
    if data_type == "real":
        return round(struct.unpack(">f", bytes(data[offset : offset + 4]))[0], 4)
    if data_type == "unix_time_seconds":
        value = util.get_dint(data, offset)
        if value <= 0:
            return None
        return datetime.fromtimestamp(value, ZoneInfo(timezone)).isoformat()
    if data_type == "string":
        return _decode_s7_string(data, offset, field.max_length or 0)

    raise ValueError(f"Unsupported field type {field.data_type} for {field.name}")


def _decode_s7_string(data: bytes | bytearray, offset: int, max_length: int) -> str:
    if max_length <= 0:
        raise ValueError("S7 string decode requires max_length")

    declared_max = int(data[offset])
    actual_length = int(data[offset + 1])
    if 0 < declared_max <= max_length and actual_length <= declared_max:
        raw = bytes(data[offset + 2 : offset + 2 + actual_length])
        return raw.decode("ascii", errors="ignore").rstrip("\x00")

    raw = bytes(data[offset : offset + max_length])
    return raw.split(b"\x00", 1)[0].decode("ascii", errors="ignore")
