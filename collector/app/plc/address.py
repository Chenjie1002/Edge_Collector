from __future__ import annotations

import re
from dataclasses import dataclass


_ADDRESS_RE = re.compile(r"^DB(?P<db>\d+)\.DB(?P<area>[XBWDL])(?P<byte>\d+)(?:\.(?P<bit>[0-7]))?$")


@dataclass(frozen=True)
class S7Address:
    raw: str
    db_number: int
    area: str
    byte_offset: int
    bit_offset: int | None = None

    @property
    def is_bit(self) -> bool:
        return self.area == "X"


def parse_s7_address(address: str) -> S7Address:
    match = _ADDRESS_RE.match(address.strip())
    if not match:
        raise ValueError(f"Unsupported S7 address: {address}")

    area = match.group("area")
    bit_value = match.group("bit")
    if area == "X" and bit_value is None:
        raise ValueError(f"Bit address requires bit offset: {address}")
    if area != "X" and bit_value is not None:
        raise ValueError(f"Only DBX addresses can include bit offset: {address}")

    return S7Address(
        raw=address,
        db_number=int(match.group("db")),
        area=area,
        byte_offset=int(match.group("byte")),
        bit_offset=int(bit_value) if bit_value is not None else None,
    )


def byte_size_for_type(data_type: str, max_length: int | None = None) -> int:
    normalized = data_type.lower()
    if normalized in {"bool", "byte"}:
        return 1
    if normalized in {"word", "int"}:
        return 2
    if normalized in {"dword", "dint", "real", "unix_time_seconds"}:
        return 4
    if normalized == "string":
        if not max_length:
            raise ValueError("S7 string mapping requires max_length")
        return max_length + 2
    raise ValueError(f"Unsupported S7 data type: {data_type}")
