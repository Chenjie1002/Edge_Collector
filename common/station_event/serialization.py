from __future__ import annotations

import json
import math
from collections.abc import Mapping
from typing import Any


def _number(value: int | float) -> str:
    if isinstance(value, bool):
        raise TypeError("boolean is not a JSON number")
    if isinstance(value, int):
        return str(value)
    if not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if value == 0:
        return "0"
    absolute = abs(value)
    if value.is_integer() and absolute < 1e21:
        return str(int(value))
    if 1e-6 <= absolute < 1e21:
        rendered = format(value, ".15f").rstrip("0").rstrip(".")
        if float(rendered) == value:
            return rendered
        return repr(value)
    rendered = repr(value).lower()
    if "e" in rendered:
        mantissa, exponent = rendered.split("e")
        sign = "+"
        if exponent.startswith(("+", "-")):
            sign = exponent[0]
            exponent = exponent[1:]
        exponent = exponent.lstrip("0") or "0"
        rendered = f"{mantissa}e{sign}{exponent}"
    return rendered


def canonical_json(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int | float):
        return _number(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, Mapping):
        items = []
        for key in sorted(value):
            if not isinstance(key, str):
                raise TypeError("JSON object keys must be strings")
            items.append(f"{canonical_json(key)}:{canonical_json(value[key])}")
        return "{" + ",".join(items) + "}"
    if isinstance(value, list | tuple):
        return "[" + ",".join(canonical_json(item) for item in value) + "]"
    raise TypeError(f"unsupported JSON type: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("utf-8")
