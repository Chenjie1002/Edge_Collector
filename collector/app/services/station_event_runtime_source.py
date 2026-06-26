from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any
from uuid import UUID


RAW_POLICIES_ALLOWING_NORMALIZED_ONLY = {"raw_not_provided"}
RAW_POLICIES_REQUIRING_EVIDENCE = {"raw_required", "raw_capable"}


class RuntimeSourcePayloadError(ValueError):
    pass


def build_runtime_source_payload(
    *,
    decoded_fields: Mapping[str, Any],
    raw_bytes: bytes | bytearray | None,
    station_snapshot: Any,
    resolved_config_hash: str,
    plc_boot_id: str,
    observed_at: str,
    code_tables: Mapping[str, Mapping[Any, Any]],
    event_type: str | None = None,
    source_kind: str = "plc",
    actor: str = "plc",
    parent_event_id: str | None = None,
    parent_fact_key: str | None = None,
    detail_role: str | None = None,
) -> dict[str, Any]:
    _validate_snapshot_policy(station_snapshot, decoded_fields, raw_bytes)
    resolved_event_type = event_type or _derive_event_type(decoded_fields)
    cycle_counter = int(decoded_fields["cycle_counter"])
    result = _decode_result(decoded_fields.get("result"), code_tables)
    event_ts = decoded_fields.get("plc_end_time") or decoded_fields.get("plc_start_time")
    if not event_ts:
        raise RuntimeSourcePayloadError("EVENT_TS_MISSING")

    base_identity = {
        "source_kind": source_kind,
        "line_id": station_snapshot.line_id,
        "plc_id": station_snapshot.plc_id,
        "station_id": station_snapshot.station_id,
        "plc_boot_id": plc_boot_id,
        "cycle_counter": cycle_counter,
        "mapping_id": station_snapshot.mapping_id,
        "payload_template": station_snapshot.payload_template,
        "event_type": resolved_event_type,
    }
    if resolved_event_type == "station_nok":
        nok_code = _first_nok_code(decoded_fields)
        if parent_event_id is None or parent_fact_key is None or detail_role is None:
            raise RuntimeSourcePayloadError("NOK_PARENT_CONTEXT_MISSING")
        base_identity.update(
            parent_event_id=parent_event_id,
            parent_fact_key=parent_fact_key,
            detail_role=detail_role,
            nok_code=nok_code,
            nok_origin="plc",
        )
    else:
        nok_code = _first_nok_code(decoded_fields) if result == "nok" else None

    source_event_id = _stable_id("runtime-source", base_identity)
    event_id = _stable_uuid4("runtime-event", base_identity)
    payload: dict[str, Any] = {
        "config_hash": resolved_config_hash,
        "event_id": event_id,
        "event_type": resolved_event_type,
        "event_ts": _utc_z(event_ts),
        "observed_at": _utc_z(observed_at),
        "station_id": station_snapshot.station_id,
        "mapping_id": station_snapshot.mapping_id,
        "payload_template": station_snapshot.payload_template,
        "source_event_id": source_event_id,
        "plc_boot_id": plc_boot_id,
        "cycle_counter": cycle_counter,
        "unit_id": decoded_fields.get("unit_id"),
        "dmc": decoded_fields.get("station_dmc") or decoded_fields.get("dmc"),
        "source": source_kind,
        "actor": actor,
        "payload": _normalized_payload(decoded_fields),
    }
    if result is not None and resolved_event_type != "station_nok":
        payload["result"] = result
    if nok_code is not None:
        payload["nok_code"] = nok_code
        payload["nok_origin"] = "plc"
    if raw_bytes is not None:
        payload["raw_payload"] = {"raw_hex": bytes(raw_bytes).hex()}
    if resolved_event_type == "station_nok":
        payload.update(
            parent_event_id=parent_event_id,
            parent_fact_key=parent_fact_key,
            detail_role=detail_role,
            nok_code=nok_code,
            nok_origin="plc",
        )
        payload.pop("result", None)
    return payload


def _validate_snapshot_policy(
    station_snapshot: Any,
    decoded_fields: Mapping[str, Any],
    raw_bytes: bytes | bytearray | None,
) -> None:
    if raw_bytes is None and station_snapshot.raw_policy in RAW_POLICIES_REQUIRING_EVIDENCE:
        raise RuntimeSourcePayloadError("RAW_EVIDENCE_MISSING")
    if raw_bytes is None and station_snapshot.raw_policy not in RAW_POLICIES_ALLOWING_NORMALIZED_ONLY:
        raise RuntimeSourcePayloadError("RAW_EVIDENCE_MISSING")
    if (
        decoded_fields.get("payload_template") is not None
        and decoded_fields["payload_template"] != station_snapshot.payload_template
    ):
        raise RuntimeSourcePayloadError("PAYLOAD_TEMPLATE_MISMATCH")
    if (
        decoded_fields.get("station_type") is not None
        and decoded_fields["station_type"] != station_snapshot.station_type
    ):
        raise RuntimeSourcePayloadError("STATION_TYPE_MISMATCH")
    if (
        decoded_fields.get("cycle_profile") is not None
        and decoded_fields["cycle_profile"] != station_snapshot.cycle_profile
    ):
        raise RuntimeSourcePayloadError("CYCLE_PROFILE_MISMATCH")


def _derive_event_type(decoded_fields: Mapping[str, Any]) -> str:
    if decoded_fields.get("cycle_valid") is False:
        raise RuntimeSourcePayloadError("CYCLE_INVALID")
    return "station_result"


def _decode_result(value: Any, code_tables: Mapping[str, Mapping[Any, Any]]) -> str | None:
    if value is None:
        return None
    table = code_tables.get("result", {})
    decoded = table.get(value, table.get(str(value), value))
    return str(decoded).lower()


def _first_nok_code(decoded_fields: Mapping[str, Any]) -> int | None:
    count = int(decoded_fields.get("nok_code_count") or 0)
    if count <= 0:
        return None
    for key in ("nok_codes_1", "nok_code_1", "nok_code"):
        if decoded_fields.get(key):
            return int(decoded_fields[key])
    codes = decoded_fields.get("nok_codes")
    if isinstance(codes, (list, tuple)) and codes:
        return int(codes[0])
    raise RuntimeSourcePayloadError("NOK_CODE_MISSING")


def _normalized_payload(decoded_fields: Mapping[str, Any]) -> dict[str, Any]:
    excluded = {
        "cycle_counter",
        "cycle_valid",
        "result",
        "unit_id",
        "station_dmc",
        "dmc",
        "plc_start_time",
        "plc_end_time",
        "nok_code_count",
        "nok_codes",
        "nok_codes_1",
        "nok_code_1",
        "nok_code",
        "station_type",
        "cycle_profile",
        "payload_template",
    }
    return {
        str(key): value
        for key, value in decoded_fields.items()
        if key not in excluded and value is not None
    }


def _stable_id(namespace: str, content: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        {"namespace": namespace, "content": content},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _stable_uuid4(namespace: str, content: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        {"namespace": namespace, "content": content},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return str(UUID(bytes=hashlib.sha256(encoded).digest()[:16], version=4))


def _utc_z(value: Any) -> str:
    if isinstance(value, datetime):
        timestamp = value
    else:
        text = str(value)
        if text.endswith("Z"):
            timestamp = datetime.fromisoformat(text[:-1] + "+00:00")
        else:
            timestamp = datetime.fromisoformat(text)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
