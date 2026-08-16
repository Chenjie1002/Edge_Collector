from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class PlcDeploymentCandidate:
    host: str
    port: int
    rack: int
    slot: int
    connection_timeout_ms: int
    poll_interval_ms: int
    line_config: str


FieldError = dict[str, str]


def parse_deployment_candidate(
    raw: Mapping[str, Any],
) -> tuple[PlcDeploymentCandidate | None, list[FieldError]]:
    errors: list[FieldError] = []

    host = raw.get("host")
    if not isinstance(host, str) or not host.strip():
        errors.append({"field": "host", "message": "PLC host is required."})
    elif len(host.strip()) > 253:
        errors.append({"field": "host", "message": "PLC host must be at most 253 characters."})

    port = _bounded_int(raw, "port", 1, 65535, errors)
    rack = _bounded_int(raw, "rack", 0, 7, errors)
    slot = _bounded_int(raw, "slot", 0, 31, errors)
    connection_timeout_ms = _bounded_int(
        raw,
        "connection_timeout_ms",
        100,
        5000,
        errors,
    )
    poll_interval_ms = _bounded_int(raw, "poll_interval_ms", 100, 60000, errors)

    line_config = raw.get("line_config")
    if not isinstance(line_config, str) or not line_config.strip():
        errors.append({"field": "line_config", "message": "Line configuration is required."})

    if errors:
        return None, errors

    assert isinstance(host, str)
    assert isinstance(port, int)
    assert isinstance(rack, int)
    assert isinstance(slot, int)
    assert isinstance(connection_timeout_ms, int)
    assert isinstance(poll_interval_ms, int)
    assert isinstance(line_config, str)
    return (
        PlcDeploymentCandidate(
            host=host.strip(),
            port=port,
            rack=rack,
            slot=slot,
            connection_timeout_ms=connection_timeout_ms,
            poll_interval_ms=poll_interval_ms,
            line_config=line_config.strip(),
        ),
        [],
    )


def candidate_content_hash(
    candidate: PlcDeploymentCandidate,
    line_config_hash: str,
) -> str:
    content = {
        "candidate": asdict(candidate),
        "line_config_hash": line_config_hash,
    }
    canonical = json.dumps(
        content,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def candidate_to_dict(candidate: PlcDeploymentCandidate) -> dict[str, object]:
    return asdict(candidate)


def _bounded_int(
    raw: Mapping[str, Any],
    field: str,
    minimum: int,
    maximum: int,
    errors: list[FieldError],
) -> int | None:
    value = raw.get(field)
    if type(value) is not int:
        errors.append({"field": field, "message": f"{field} must be an integer."})
        return None
    if not minimum <= value <= maximum:
        errors.append(
            {
                "field": field,
                "message": f"{field} must be between {minimum} and {maximum}.",
            }
        )
        return None
    return value
