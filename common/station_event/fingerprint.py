from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Any

from .serialization import canonical_json_bytes


def _sha256(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def fact_identity(event: Mapping[str, Any]) -> dict[str, Any]:
    correlation = event["correlation"]
    role = correlation["event_role"]
    if role in {"cycle_start", "cycle_complete", "production_result"}:
        fields = (
            "config_hash",
            "cycle_counter",
            "cycle_id",
            "line_id",
            "plc_boot_id",
            "plc_id",
            "station_id",
        )
        identity = {field: event[field] for field in fields}
        identity["event_role"] = role
        return identity
    if role == "nok_detail":
        identity = {
            "config_hash": event["config_hash"],
            "detail_role": correlation["detail_role"],
            "event_role": role,
            "line_id": event["line_id"],
            "nok_code": event["nok_code"],
            "nok_origin": event["nok_origin"],
            "parent_event_id": correlation["parent_event_id"],
            "parent_fact_key": correlation["parent_fact_key"],
            "plc_id": event["plc_id"],
            "station_id": event["station_id"],
        }
        return identity
    if role == "heartbeat":
        return {
            "config_hash": event["config_hash"],
            "event_role": role,
            "line_id": event["line_id"],
            "plc_boot_id": event["plc_boot_id"],
            "plc_id": event["plc_id"],
            "source_event_id": correlation["source_event_id"],
            "station_id": event["station_id"],
        }
    raise ValueError(f"unsupported event role: {role}")


def compute_fact_key(event: Mapping[str, Any]) -> str:
    return _sha256(fact_identity(event))


def compute_content_fingerprint(event: Mapping[str, Any]) -> str:
    content = {key: _copy(value) for key, value in event.items()}
    for key in ("event_id", "observed_at", "raw_payload"):
        content.pop(key, None)
    correlation = dict(content["correlation"])
    correlation.pop("source_event_id", None)
    correlation.pop("raw_encoding", None)
    content["correlation"] = correlation
    return _sha256(content)


def compute_raw_evidence_fingerprint(raw_payload: Mapping[str, Any] | None) -> str | None:
    return None if raw_payload is None else _sha256(raw_payload)


def _copy(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _copy(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_copy(item) for item in value]
    return value


def cycle_role_key(event: Mapping[str, Any]) -> tuple[Any, ...]:
    return (
        event["line_id"],
        event["plc_id"],
        event["station_id"],
        event["plc_boot_id"],
        event["cycle_counter"],
        event["correlation"]["event_role"],
    )


def production_result_key(event: Mapping[str, Any]) -> tuple[Any, ...]:
    return cycle_role_key(event)


def station_nok_detail_key(event: Mapping[str, Any]) -> tuple[Any, ...]:
    correlation = event["correlation"]
    return (
        correlation["parent_fact_key"],
        correlation["detail_role"],
        event["nok_code"],
        event["nok_origin"],
    )
