from __future__ import annotations

import base64
import binascii
import math
import re
import zlib
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from .constants import (
    AuditSubtype,
    EVENT_ROLES,
    MVP_EVENT_TYPES,
    PAYLOAD_LIMITS,
)
from .errors import StationEventValidationError, ValidationError
from .fingerprint import (
    compute_content_fingerprint,
    compute_fact_key,
    compute_raw_evidence_fingerprint,
    cycle_role_key,
    station_nok_detail_key,
)
from .models import StationEvent, ValidationDecision, ValidationResult
from .serialization import canonical_json_bytes


TOP_LEVEL_FIELDS = {
    "schema_version",
    "event_id",
    "event_type",
    "event_ts",
    "line_id",
    "plc_id",
    "station_id",
    "station_type",
    "config_version",
    "config_hash",
    "plc_boot_id",
    "profile_id",
    "cycle_id",
    "cycle_counter",
    "unit_id",
    "dmc",
    "result",
    "nok_code",
    "nok_origin",
    "source",
    "actor",
    "payload",
    "raw_payload",
    "diagnostic_context",
    "observed_at",
    "correlation",
}
COMMON_REQUIRED = {
    "schema_version",
    "event_id",
    "event_type",
    "event_ts",
    "line_id",
    "plc_id",
    "station_id",
    "station_type",
    "config_version",
    "config_hash",
    "source",
    "actor",
    "correlation",
}
PRODUCTION_REQUIRED = {"plc_boot_id", "profile_id", "cycle_id", "cycle_counter"}
CORRELATION_FIELDS = {
    "source_event_id",
    "fact_key",
    "event_role",
    "mapping_id",
    "payload_template",
    "raw_encoding",
    "parent_event_id",
    "parent_fact_key",
    "detail_role",
    "upstream_evidence",
}
UPSTREAM_EVIDENCE_FIELDS = {
    "evidence_type",
    "source_event_id",
    "parent_event_id",
    "parent_fact_key",
    "upstream_station_id",
    "upstream_plc_id",
    "upstream_plc_boot_id",
    "upstream_event_type",
    "upstream_result",
    "upstream_nok_code",
    "upstream_config_hash",
}
ERROR_PRECEDENCE = {
    "RAW_PARSE_ERROR": 1,
    "RAW_CONTENT_FORBIDDEN": 2,
    "PAYLOAD_TYPE_FORBIDDEN": 3,
    "JSON_NUMBER_NON_FINITE": 4,
    "JSON_NUMBER_RANGE": 4,
    "PAYLOAD_DEPTH_LIMIT": 5,
    "PAYLOAD_OBJECT_KEY_COUNT_LIMIT": 6,
    "PAYLOAD_KEY_BYTES_LIMIT": 7,
    "PAYLOAD_ARRAY_ITEMS_LIMIT": 8,
    "PAYLOAD_TREE_NODE_LIMIT": 9,
    "PAYLOAD_TOTAL_BYTES_LIMIT": 10,
    "RAW_TOTAL_BYTES_LIMIT": 11,
    "PAYLOAD_STRING_BYTES_LIMIT": 12,
    "RAW_STRING_BYTES_LIMIT": 13,
    "PAYLOAD_SCHEMA_MISMATCH": 14,
    "RAW_NORMALIZED_MISMATCH": 15,
}
RAW_BINARY_KEY_RE = re.compile(
    r"(?:^|_)(?:attachment|base64|binary|blob|file|image|image_base64|"
    r"opaque_log|pdf)(?:_|$)",
    re.IGNORECASE,
)
RAW_MIME_KEY_RE = re.compile(
    r"(?:^|_)(?:content_type|mime)(?:_|$)",
    re.IGNORECASE,
)
RAW_DATA_URI_RE = re.compile(
    r"^data:(?:image/[^;,]+|application/(?:octet-stream|pdf)|[^;,]*binary[^;,]*);base64,",
    re.IGNORECASE,
)
RAW_BINARY_MIME_RE = re.compile(
    r"^(?:image/[^;\s]+|application/(?:octet-stream|pdf)|[^;\s]*binary[^;\s]*)"
    r"(?:\s*;.*)?$",
    re.IGNORECASE,
)
RAW_BASE64_RE = re.compile(r"[A-Za-z0-9+/]+={0,2}")
RAW_LONG_TEXT_BYTES = 4096
RAW_BASE64_SAMPLE_CHARS = 4096
RAW_PERIODIC_COMPRESSED_BYTES = 512
RAW_PERIODIC_COMPRESSION_RATIO = 0.08


def validate_event(event: Mapping[str, Any] | StationEvent, resolved_config: Any = None) -> ValidationResult:
    raw = event.to_dict() if isinstance(event, StationEvent) else dict(event)
    errors: list[ValidationError] = []
    _presence(raw, errors)
    if errors:
        return ValidationResult(tuple(sorted(errors)))
    _basic_types(raw, errors)
    _payloads(raw, errors)
    if errors:
        return ValidationResult(tuple(_sort_errors(errors)))
    _combinations(raw, errors)
    _authority(raw, errors)
    _config(raw, resolved_config, errors)
    _fact_key(raw, errors)
    return ValidationResult(tuple(_sort_errors(errors)))


def parse_event(
    event: Mapping[str, Any],
    resolved_config: Any = None,
    *,
    validate: bool = True,
) -> StationEvent:
    if validate:
        result = validate_event(event, resolved_config)
        if not result.is_valid:
            raise StationEventValidationError(result.errors)
    values = {name: event[name] for name in StationEvent.__dataclass_fields__ if name in event}
    return StationEvent(**values)


def _presence(raw: dict[str, Any], errors: list[ValidationError]) -> None:
    for field in sorted(set(raw) - TOP_LEVEL_FIELDS):
        errors.append(_error(field, "FIELD_FORBIDDEN"))
    for field in sorted(COMMON_REQUIRED - set(raw)):
        errors.append(_error(field, "REQUIRED_FIELD_MISSING"))
    for field in sorted(field for field, value in raw.items() if value is None):
        errors.append(_error(field, "FIELD_NULL_FORBIDDEN"))
    event_type = raw.get("event_type")
    required = set()
    forbidden = set()
    if event_type in {"station_cycle_start", "station_cycle_complete"}:
        required |= PRODUCTION_REQUIRED
        forbidden |= {"result", "nok_code", "nok_origin", "diagnostic_context"}
    elif event_type == "station_result":
        required |= PRODUCTION_REQUIRED | {"result"}
        forbidden |= {"diagnostic_context"}
        if raw.get("result") == "nok":
            required |= {"nok_code", "nok_origin"}
        else:
            forbidden |= {"nok_code", "nok_origin"}
    elif event_type == "station_nok":
        required |= PRODUCTION_REQUIRED | {"nok_code", "nok_origin"}
        forbidden |= {"result", "diagnostic_context"}
    elif event_type == "station_heartbeat":
        required |= {"plc_boot_id", "diagnostic_context"}
        forbidden |= {"cycle_id", "cycle_counter", "unit_id", "dmc", "nok_code", "nok_origin"}
    for field in sorted(required - set(raw)):
        errors.append(_error(field, "REQUIRED_FIELD_MISSING"))
    for field in sorted(forbidden & set(raw)):
        errors.append(_error(field, "FIELD_FORBIDDEN"))
    if isinstance(raw.get("correlation"), Mapping):
        correlation = raw["correlation"]
        for field in sorted(set(correlation) - CORRELATION_FIELDS):
            errors.append(_error(f"correlation.{field}", "FIELD_FORBIDDEN"))
        for field in ("source_event_id", "fact_key", "event_role"):
            if field not in correlation:
                errors.append(_error(f"correlation.{field}", "REQUIRED_FIELD_MISSING"))
        if event_type == "station_nok":
            for field in ("parent_event_id", "parent_fact_key", "detail_role"):
                if field not in correlation:
                    errors.append(_error(f"correlation.{field}", "REQUIRED_FIELD_MISSING"))
            if raw.get("nok_code") == 30003 and "upstream_evidence" not in correlation:
                errors.append(
                    _error("correlation.upstream_evidence", "REQUIRED_FIELD_MISSING")
                )
            evidence = correlation.get("upstream_evidence")
            if evidence is not None:
                if not isinstance(evidence, Mapping):
                    errors.append(
                        _error("correlation.upstream_evidence", "UPSTREAM_EVIDENCE_INVALID")
                    )
                else:
                    for field in sorted(set(evidence) - UPSTREAM_EVIDENCE_FIELDS):
                        errors.append(
                            _error(
                                f"correlation.upstream_evidence.{field}",
                                "FIELD_FORBIDDEN",
                            )
                        )
                    for field in sorted(UPSTREAM_EVIDENCE_FIELDS - set(evidence)):
                        errors.append(
                            _error(
                                f"correlation.upstream_evidence.{field}",
                                "REQUIRED_FIELD_MISSING",
                            )
                        )
            if raw.get("nok_code") != 30003 and "upstream_evidence" in correlation:
                errors.append(
                    _error("correlation.upstream_evidence", "FIELD_FORBIDDEN")
                )
        else:
            for field in (
                "parent_event_id",
                "parent_fact_key",
                "detail_role",
                "upstream_evidence",
            ):
                if field in correlation:
                    errors.append(_error(f"correlation.{field}", "FIELD_FORBIDDEN"))
        if "raw_payload" in raw and "raw_encoding" not in correlation:
            errors.append(_error("correlation.raw_encoding", "REQUIRED_FIELD_MISSING"))
        if ("payload" in raw or "raw_payload" in raw) and "payload_template" not in correlation:
            errors.append(_error("correlation.payload_template", "REQUIRED_FIELD_MISSING"))


def _basic_types(raw: dict[str, Any], errors: list[ValidationError]) -> None:
    for field in COMMON_REQUIRED - {"correlation"}:
        if not isinstance(raw.get(field), str) or not raw[field]:
            errors.append(_error(field, "RESULT_COMBINATION_INVALID"))
    try:
        uuid = UUID(raw["event_id"])
        if uuid.version != 4:
            raise ValueError
    except (ValueError, TypeError, AttributeError):
        errors.append(_error("event_id", "RESULT_COMBINATION_INVALID"))
    if not re.fullmatch(r"[0-9a-f]{64}", raw["config_hash"]):
        errors.append(_error("config_hash", "RESULT_COMBINATION_INVALID"))
    _timestamp(raw, "event_ts", errors)
    if "observed_at" in raw:
        _timestamp(raw, "observed_at", errors)
        try:
            event_ts = _parse_ts(raw["event_ts"])
            observed_at = _parse_ts(raw["observed_at"])
            if (event_ts - observed_at).total_seconds() > 300:
                errors.append(_error("event_ts", "EVENT_TS_FUTURE"))
        except ValueError:
            pass
    if "cycle_counter" in raw and (
        not isinstance(raw["cycle_counter"], int)
        or isinstance(raw["cycle_counter"], bool)
        or not 0 <= raw["cycle_counter"] <= 2**63 - 1
    ):
        errors.append(_error("cycle_counter", "RESULT_COMBINATION_INVALID"))
    if "nok_code" in raw and (
        not isinstance(raw["nok_code"], int)
        or isinstance(raw["nok_code"], bool)
        or raw["nok_code"] <= 0
    ):
        errors.append(_error("nok_code", "RESULT_COMBINATION_INVALID"))
    if not isinstance(raw.get("correlation"), Mapping):
        errors.append(_error("correlation", "RESULT_COMBINATION_INVALID"))


def _timestamp(raw: dict[str, Any], field: str, errors: list[ValidationError]) -> None:
    try:
        value = raw[field]
        if not isinstance(value, str) or not value.endswith("Z"):
            raise ValueError
        timestamp = _parse_ts(value)
        if timestamp < datetime(2000, 1, 1, tzinfo=timezone.utc):
            raise ValueError
    except (ValueError, TypeError):
        errors.append(_error(field, "RESULT_COMBINATION_INVALID"))


def _parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value[:-1] + "+00:00")


def _payloads(raw: dict[str, Any], errors: list[ValidationError]) -> None:
    for field, is_raw in (("payload", False), ("raw_payload", True)):
        if field not in raw:
            continue
        value = raw[field]
        if not isinstance(value, Mapping):
            errors.append(_error(field, "PAYLOAD_TYPE_FORBIDDEN"))
            continue
        stats = {"keys": 0, "array_items": 0, "nodes": 0}
        seen: set[int] = set()
        _walk_json(value, field, 1, is_raw, stats, seen, errors)
        try:
            size = len(canonical_json_bytes(value))
        except (TypeError, ValueError):
            size = 0
        limit = PAYLOAD_LIMITS["raw_bytes" if is_raw else "normalized_bytes"]
        if size > limit:
            errors.append(
                _error(field, "RAW_TOTAL_BYTES_LIMIT" if is_raw else "PAYLOAD_TOTAL_BYTES_LIMIT")
            )
    correlation = raw.get("correlation", {})
    if "raw_payload" in raw and correlation.get("raw_encoding") != "json":
        errors.append(_error("correlation.raw_encoding", "RAW_ENCODING_INVALID"))


def _walk_json(
    value: Any,
    path: str,
    depth: int,
    is_raw: bool,
    stats: dict[str, int],
    seen: set[int],
    errors: list[ValidationError],
) -> None:
    stats["nodes"] += 1
    if stats["nodes"] > PAYLOAD_LIMITS["tree_nodes"]:
        errors.append(_error(path, "PAYLOAD_TREE_NODE_LIMIT"))
        return
    if depth > PAYLOAD_LIMITS["depth"]:
        errors.append(_error(path, "PAYLOAD_DEPTH_LIMIT"))
        return
    if isinstance(value, Mapping):
        identity = id(value)
        if identity in seen:
            errors.append(_error(path, "PAYLOAD_TYPE_FORBIDDEN"))
            return
        seen.add(identity)
        if len(value) > PAYLOAD_LIMITS["object_keys"]:
            errors.append(_error(path, "PAYLOAD_OBJECT_KEY_COUNT_LIMIT"))
        stats["keys"] += len(value)
        if stats["keys"] > PAYLOAD_LIMITS["tree_keys"]:
            errors.append(_error(path, "PAYLOAD_OBJECT_KEY_COUNT_LIMIT"))
        for key, item in value.items():
            stats["nodes"] += 1
            if stats["nodes"] > PAYLOAD_LIMITS["tree_nodes"]:
                errors.append(_error(f"{path}.{key}", "PAYLOAD_TREE_NODE_LIMIT"))
                return
            if not isinstance(key, str):
                errors.append(_error(path, "PAYLOAD_TYPE_FORBIDDEN"))
                continue
            key_path = f"{path}.{key}"
            if len(key.encode("utf-8")) > PAYLOAD_LIMITS["key_bytes"]:
                errors.append(_error(key_path, "PAYLOAD_KEY_BYTES_LIMIT"))
            if is_raw and _raw_content_forbidden(key, item):
                errors.append(_error(key_path, "RAW_CONTENT_FORBIDDEN"))
            _walk_json(item, key_path, depth + 1, is_raw, stats, seen, errors)
        seen.remove(identity)
        return
    if isinstance(value, list):
        identity = id(value)
        if identity in seen:
            errors.append(_error(path, "PAYLOAD_TYPE_FORBIDDEN"))
            return
        seen.add(identity)
        if len(value) > PAYLOAD_LIMITS["array_items"]:
            errors.append(_error(path, "PAYLOAD_ARRAY_ITEMS_LIMIT"))
        stats["array_items"] += len(value)
        if stats["array_items"] > PAYLOAD_LIMITS["tree_array_items"]:
            errors.append(_error(path, "PAYLOAD_ARRAY_ITEMS_LIMIT"))
        for index, item in enumerate(value):
            stats["nodes"] += 1
            if stats["nodes"] > PAYLOAD_LIMITS["tree_nodes"]:
                errors.append(_error(f"{path}[{index}]", "PAYLOAD_TREE_NODE_LIMIT"))
                return
            _walk_json(item, f"{path}[{index}]", depth + 1, is_raw, stats, seen, errors)
        seen.remove(identity)
        return
    if isinstance(value, tuple | set | bytes | bytearray):
        errors.append(_error(path, "PAYLOAD_TYPE_FORBIDDEN"))
        return
    if isinstance(value, str):
        limit = PAYLOAD_LIMITS["raw_string_bytes" if is_raw else "normalized_string_bytes"]
        if len(value.encode("utf-8")) > limit:
            errors.append(
                _error(path, "RAW_STRING_BYTES_LIMIT" if is_raw else "PAYLOAD_STRING_BYTES_LIMIT")
            )
        return
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int):
        if abs(value) > 9_007_199_254_740_991:
            errors.append(_error(path, "JSON_NUMBER_RANGE"))
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            errors.append(_error(path, "JSON_NUMBER_NON_FINITE"))
        return
    errors.append(_error(path, "PAYLOAD_TYPE_FORBIDDEN"))


def _raw_content_forbidden(key: str, value: Any) -> bool:
    if not isinstance(value, str):
        return bool(RAW_BINARY_KEY_RE.search(key) or RAW_MIME_KEY_RE.search(key))
    stripped = value.strip()
    if RAW_DATA_URI_RE.match(stripped):
        return True
    if RAW_BINARY_MIME_RE.fullmatch(stripped):
        return True
    if RAW_BINARY_KEY_RE.search(key) and stripped:
        return True
    value_bytes = len(value.encode("utf-8"))
    if _is_binary_base64(
        stripped,
        bounded=value_bytes > PAYLOAD_LIMITS["raw_string_bytes"],
    ):
        return True
    if value_bytes > PAYLOAD_LIMITS["raw_string_bytes"]:
        return False
    if _is_repeated_unbounded_text(value):
        return True
    return False


def _is_binary_base64(value: str, *, bounded: bool = False) -> bool:
    if len(value) < 24:
        return False
    encoded = value[:RAW_BASE64_SAMPLE_CHARS] if bounded else value
    encoded = encoded[: len(encoded) - (len(encoded) % 4)] if bounded else encoded
    if len(encoded) < 24 or not RAW_BASE64_RE.fullmatch(encoded):
        return False
    padded = encoded + ("=" * (-len(encoded) % 4))
    try:
        decoded = base64.b64decode(padded, validate=True)
    except (binascii.Error, ValueError):
        return False
    if len(decoded) < 12:
        return False
    if decoded.startswith(b"%PDF-"):
        return True
    if decoded.startswith(b"RIFF") and decoded[8:12] == b"WEBP":
        return True
    if decoded.startswith((b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff", b"GIF8", b"BM")):
        return True
    if len(set(encoded)) < 16 or len(set(decoded)) < 16:
        return False
    non_text_bytes = sum(
        byte not in (9, 10, 13) and not 32 <= byte <= 126 for byte in decoded
    )
    return non_text_bytes / len(decoded) >= 0.30


def _is_repeated_unbounded_text(value: str) -> bool:
    if len(value.encode("utf-8")) <= RAW_LONG_TEXT_BYTES:
        return False
    if (
        value.count("\n") >= 32
        and len(set(value.splitlines())) <= max(8, len(value.splitlines()) // 10)
    ):
        return True
    if "\n" in value or "\r" in value:
        return False
    tokens = re.findall(r"\S+", value)
    if len(tokens) >= 32 and len(set(tokens)) <= max(8, len(tokens) // 10):
        return True
    compact = re.sub(r"\s+", "", value)
    if len(set(compact)) <= 8:
        return True
    encoded = compact.encode("utf-8")
    compressed_size = len(zlib.compress(encoded, level=1))
    if (
        compressed_size <= RAW_PERIODIC_COMPRESSED_BYTES
        and compressed_size / len(encoded) <= RAW_PERIODIC_COMPRESSION_RATIO
    ):
        return True
    chunks = [compact[index : index + 32] for index in range(0, len(compact), 32)]
    if len(chunks) >= 32 and len(set(chunks)) <= max(8, len(chunks) // 10):
        return True
    return False


def _combinations(raw: dict[str, Any], errors: list[ValidationError]) -> None:
    event_type = raw["event_type"]
    if event_type not in MVP_EVENT_TYPES:
        errors.append(_error("event_type", "RESULT_COMBINATION_INVALID"))
        return
    correlation = raw["correlation"]
    if correlation.get("event_role") != EVENT_ROLES[event_type]:
        errors.append(_error("correlation.event_role", "RESULT_COMBINATION_INVALID"))
    if event_type != "station_heartbeat":
        expected_cycle = (
            f"{raw['line_id']}/{raw['plc_id']}/{raw['station_id']}/"
            f"{raw['plc_boot_id']}/{raw['cycle_counter']}"
        )
        if raw["cycle_id"] != expected_cycle:
            errors.append(_error("cycle_id", "RESULT_COMBINATION_INVALID"))
    if event_type == "station_result":
        if raw["result"] not in {"ok", "nok", "skip", "not_applicable"}:
            errors.append(_error("result", "RESULT_COMBINATION_INVALID"))
    if event_type == "station_heartbeat":
        if raw.get("result") not in {None, "unknown", "not_applicable"}:
            errors.append(_error("result", "RESULT_COMBINATION_INVALID"))
        _diagnostic(raw["diagnostic_context"], errors)
        if raw.get("result") == "unknown" and raw["diagnostic_context"].get("category") not in {
            "source_incomplete",
            "clock_anomaly",
            "disabled_station",
        }:
            errors.append(
                _error("diagnostic_context.category", "DIAGNOSTIC_CONTEXT_INVALID")
            )
    if event_type == "station_nok":
        if correlation.get("detail_role") not in {"primary", "secondary", "system_reserved"}:
            errors.append(_error("correlation.detail_role", "RESULT_COMBINATION_INVALID"))
        if raw["nok_code"] == 30003:
            if raw["nok_origin"] != "system_reserved" or correlation.get("detail_role") != "system_reserved":
                errors.append(_error("nok_code", "RESERVED_NOK_FORBIDDEN"))
            _upstream_evidence(correlation.get("upstream_evidence"), errors)
        elif raw["nok_origin"] == "system_reserved" or correlation.get("detail_role") == "system_reserved":
            errors.append(_error("nok_code", "RESERVED_NOK_FORBIDDEN"))
    if raw.get("nok_code") == 30003 and event_type != "station_nok":
        errors.append(_error("nok_code", "RESERVED_NOK_FORBIDDEN"))


def _diagnostic(value: Any, errors: list[ValidationError]) -> None:
    if not isinstance(value, Mapping):
        errors.append(_error("diagnostic_context", "DIAGNOSTIC_CONTEXT_INVALID"))
        return
    allowed = {"category", "reason_code", "message", "incomplete_reason"}
    if set(value) - allowed:
        errors.append(_error("diagnostic_context", "DIAGNOSTIC_CONTEXT_INVALID"))
    if value.get("category") not in {
        "heartbeat",
        "source_incomplete",
        "clock_anomaly",
        "disabled_station",
    }:
        errors.append(_error("diagnostic_context.category", "DIAGNOSTIC_CONTEXT_INVALID"))
    reason = value.get("reason_code")
    if not isinstance(reason, str) or not re.fullmatch(
        r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", reason
    ):
        errors.append(_error("diagnostic_context.reason_code", "DIAGNOSTIC_CONTEXT_INVALID"))
    if value.get("category") == "source_incomplete" and not value.get("incomplete_reason"):
        errors.append(_error("diagnostic_context.incomplete_reason", "DIAGNOSTIC_CONTEXT_INVALID"))


def _upstream_evidence(value: Any, errors: list[ValidationError]) -> None:
    if not isinstance(value, Mapping):
        return
    evidence_type = value.get("evidence_type")
    expected_event_type = {
        "canonical_station_result": "station_result",
        "validated_nok_detail": "station_nok",
    }.get(evidence_type)
    if (
        expected_event_type is None
        or value.get("upstream_event_type") != expected_event_type
        or value.get("upstream_result") != "nok"
        or value.get("upstream_nok_code") == 30003
        or not isinstance(value.get("upstream_nok_code"), int)
        or value.get("upstream_config_hash") is None
    ):
        errors.append(
            _error("correlation.upstream_evidence", "UPSTREAM_EVIDENCE_INVALID")
        )


def _authority(raw: dict[str, Any], errors: list[ValidationError]) -> None:
    event_type = raw["event_type"]
    pair = (raw["source"], raw["actor"])
    if event_type == "station_nok" and raw.get("nok_code") == 30003:
        allowed = {("system", "system")}
    else:
        allowed = {("plc", "plc"), ("vplc", "simulator")}
    if pair not in allowed:
        errors.append(_error("source", "AUTHORITY_FORBIDDEN"))
        return
    origin = raw.get("nok_origin")
    if raw.get("result") == "nok" or event_type == "station_nok":
        if pair == ("plc", "plc") and origin != "plc":
            errors.append(_error("nok_origin", "AUTHORITY_FORBIDDEN"))
        if pair == ("vplc", "simulator") and origin not in {"random", "forced", "simulator"}:
            errors.append(_error("nok_origin", "AUTHORITY_FORBIDDEN"))


def _config(raw: dict[str, Any], resolved_config: Any, errors: list[ValidationError]) -> None:
    if resolved_config is None:
        return
    config_hash = _attr(resolved_config, "config_hash")
    if config_hash != raw["config_hash"]:
        errors.append(_error("config_hash", "CONFIG_HASH_MISMATCH"))
        return
    if _attr(resolved_config, "line_id") != raw["line_id"]:
        errors.append(_error("line_id", "EVENT_LINEAGE_INVALID"))
    stations = _attr(resolved_config, "stations") or ()
    station = next((item for item in stations if _attr(item, "station_id") == raw["station_id"]), None)
    if station is None:
        errors.append(_error("station_id", "CONFIG_NOT_FOUND"))
        return
    if _attr(station, "station_enabled") is False:
        if raw["event_type"] != "station_heartbeat":
            errors.append(_error("station_id", "EVENT_LINEAGE_INVALID"))
        elif raw.get("diagnostic_context", {}).get("category") != "disabled_station":
            errors.append(
                _error("diagnostic_context.category", "EVENT_LINEAGE_INVALID")
            )
    checks = {
        "plc_id": _attr(station, "plc_id"),
        "station_type": _attr(station, "station_type"),
    }
    if raw["event_type"] != "station_heartbeat":
        checks["profile_id"] = _attr(station, "cycle_profile")
    for field, expected in checks.items():
        if raw.get(field) != expected:
            errors.append(_error(field, "EVENT_LINEAGE_INVALID"))
    payload_validator = getattr(resolved_config, "validate_payload", None)
    if callable(payload_validator) and "payload" in raw:
        if not payload_validator(raw["payload"], raw):
            errors.append(_error("payload", "PAYLOAD_SCHEMA_MISMATCH"))
    decoder = getattr(resolved_config, "decode_raw_payload", None)
    if "raw_payload" in raw and not callable(decoder):
        errors.append(_error("raw_payload", "RAW_PARSE_ERROR"))
    elif "raw_payload" in raw:
        try:
            decoded = decoder(raw["raw_payload"], raw)
        except Exception:
            errors.append(_error("raw_payload", "RAW_PARSE_ERROR"))
        else:
            if "payload" not in raw or canonical_json_bytes(decoded) != canonical_json_bytes(
                raw["payload"]
            ):
                errors.append(_error("payload", "RAW_NORMALIZED_MISMATCH"))


def _fact_key(raw: dict[str, Any], errors: list[ValidationError]) -> None:
    correlation = raw["correlation"]
    fact_key = correlation.get("fact_key")
    if not isinstance(fact_key, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", fact_key):
        errors.append(_error("correlation.fact_key", "FACT_KEY_INVALID"))
        return
    try:
        expected = compute_fact_key(raw)
    except (KeyError, ValueError):
        return
    if fact_key != expected:
        errors.append(_error("correlation.fact_key", "FACT_KEY_INVALID"))


def validate_duplicate_or_conflict(
    *,
    matched_key_type: str,
    matched_key_value: Any,
    existing_event_id: str,
    existing_content_fingerprint: str,
    incoming_content_fingerprint: str,
    existing_raw_evidence_fingerprint: str | None,
    incoming_raw_evidence_fingerprint: str | None,
) -> ValidationDecision:
    if existing_content_fingerprint == incoming_content_fingerprint:
        subtype = (
            AuditSubtype.RAW_VARIANT
            if existing_raw_evidence_fingerprint != incoming_raw_evidence_fingerprint
            else AuditSubtype.NONE
        )
        return ValidationDecision(
            disposition="duplicate",
            matched_key_type=matched_key_type,
            matched_key_value=matched_key_value,
            existing_event_id=existing_event_id,
            existing_content_fingerprint=existing_content_fingerprint,
            incoming_content_fingerprint=incoming_content_fingerprint,
            existing_raw_evidence_fingerprint=existing_raw_evidence_fingerprint,
            incoming_raw_evidence_fingerprint=incoming_raw_evidence_fingerprint,
            audit_subtype=subtype,
        )
    code = {
        "event_id": "EVENT_ID_CONFLICT",
        "fact_key": "FACT_KEY_CONFLICT",
        "cycle_role_key": "CYCLE_ROLE_CONFLICT",
        "production_result_key": "CYCLE_ROLE_CONFLICT",
    }.get(matched_key_type, "DETAIL_KEY_CONFLICT")
    return ValidationDecision(
        disposition="conflict",
        final_error_code=code,
        matched_key_type=matched_key_type,
        matched_key_value=matched_key_value,
        existing_event_id=existing_event_id,
        existing_content_fingerprint=existing_content_fingerprint,
        incoming_content_fingerprint=incoming_content_fingerprint,
        existing_raw_evidence_fingerprint=existing_raw_evidence_fingerprint,
        incoming_raw_evidence_fingerprint=incoming_raw_evidence_fingerprint,
    )


def validate_event_stateful(
    event: Mapping[str, Any] | StationEvent,
    state_index: Any,
) -> ValidationDecision:
    raw = event.to_dict() if isinstance(event, StationEvent) else dict(event)
    stateless = validate_event(raw)
    if not stateless.is_valid:
        return ValidationDecision("reject", stateless.errors[0].code)
    if state_index is None:
        return ValidationDecision("reject", "STATE_INDEX_UNAVAILABLE")
    config_lookup = state_index.lookup_resolved_config(raw["config_hash"])
    if _is_unavailable(config_lookup):
        return ValidationDecision("reject", "STATE_INDEX_UNAVAILABLE")
    config = _lookup_record(config_lookup)
    if config is None:
        return ValidationDecision("reject", "CONFIG_NOT_FOUND")
    if _attr(config, "config_hash") != raw["config_hash"]:
        return ValidationDecision("reject", "CONFIG_HASH_MISMATCH")
    config_validation = validate_event(raw, config)
    if not config_validation.is_valid:
        return ValidationDecision("reject", config_validation.errors[0].code)
    if raw["event_type"] == "station_nok":
        correlation = raw["correlation"]
        parent_lookup = state_index.lookup_parent_result(
            correlation["parent_event_id"], correlation["parent_fact_key"]
        )
        if _is_unavailable(parent_lookup):
            return ValidationDecision("reject", "STATE_INDEX_UNAVAILABLE")
        parent = _lookup_record(parent_lookup)
        if parent is None:
            return ValidationDecision("reject", "PARENT_NOT_FOUND")
        if not _lookup_is_accepted(parent_lookup):
            return ValidationDecision("reject", "PARENT_EVENT_INVALID")
        parent_raw = parent.to_dict() if isinstance(parent, StationEvent) else dict(parent)
        if not _parent_matches(raw, parent_raw):
            return ValidationDecision("reject", "PARENT_EVENT_INVALID")
        if raw["nok_code"] == 30003:
            evidence_lookup = state_index.lookup_upstream_evidence(
                correlation["upstream_evidence"]
            )
            if _is_unavailable(evidence_lookup):
                return ValidationDecision("reject", "STATE_INDEX_UNAVAILABLE")
            evidence_record = _lookup_record(evidence_lookup)
            if evidence_record is None:
                return ValidationDecision("reject", "UPSTREAM_EVIDENCE_NOT_FOUND")
            evidence_error = _evidence_error(
                correlation["upstream_evidence"],
                evidence_lookup,
                evidence_record,
                state_index,
                raw,
                config,
            )
            if evidence_error is not None:
                return ValidationDecision("reject", evidence_error)
    incoming_content = compute_content_fingerprint(raw)
    incoming_raw = compute_raw_evidence_fingerprint(raw.get("raw_payload"))
    lookups = [
        ("event_id", raw["event_id"], state_index.lookup_by_event_id(raw["event_id"])),
        (
            "fact_key",
            raw["correlation"]["fact_key"],
            state_index.lookup_by_fact_key(raw["correlation"]["fact_key"]),
        ),
    ]
    if raw["event_type"] not in {"station_nok", "station_heartbeat"}:
        key = cycle_role_key(raw)
        lookups.append(("cycle_role_key", key, state_index.lookup_cycle_role(key)))
    elif raw["event_type"] == "station_nok":
        key = station_nok_detail_key(raw)
        lookups.append(("station_nok_detail_key", key, state_index.lookup_detail_key(key)))
    for key_type, key_value, found in lookups:
        if _is_unavailable(found):
            return ValidationDecision("reject", "STATE_INDEX_UNAVAILABLE")
        record = _lookup_record(found)
        if record is None:
            continue
        existing = record.to_dict() if isinstance(record, StationEvent) else dict(record)
        return validate_duplicate_or_conflict(
            matched_key_type=key_type,
            matched_key_value=key_value,
            existing_event_id=existing["event_id"],
            existing_content_fingerprint=compute_content_fingerprint(existing),
            incoming_content_fingerprint=incoming_content,
            existing_raw_evidence_fingerprint=compute_raw_evidence_fingerprint(
                existing.get("raw_payload")
            ),
            incoming_raw_evidence_fingerprint=incoming_raw,
        )
    if raw["event_type"] == "station_nok":
        correlation = raw["correlation"]
        details = state_index.lookup_detail_set(correlation["parent_fact_key"])
        if _is_unavailable(details):
            return ValidationDecision("reject", "STATE_INDEX_UNAVAILABLE")
        details = details or {}
        if correlation["detail_role"] in {"primary", "system_reserved"}:
            field = (
                "primary"
                if correlation["detail_role"] == "primary"
                else "system_reserved"
            )
            existing = details.get(field)
            if existing is not None:
                existing_raw = (
                    existing.to_dict() if isinstance(existing, StationEvent) else dict(existing)
                )
                return validate_duplicate_or_conflict(
                    matched_key_type=f"{field}_nok_detail_key",
                    matched_key_value=(
                        correlation["parent_fact_key"],
                        correlation["detail_role"],
                    ),
                    existing_event_id=existing_raw["event_id"],
                    existing_content_fingerprint=compute_content_fingerprint(existing_raw),
                    incoming_content_fingerprint=incoming_content,
                    existing_raw_evidence_fingerprint=compute_raw_evidence_fingerprint(
                        existing_raw.get("raw_payload")
                    ),
                    incoming_raw_evidence_fingerprint=incoming_raw,
                )
        if correlation["detail_role"] == "secondary":
            if not details or not details.get("primary"):
                return ValidationDecision("reject", "PRIMARY_DETAIL_REQUIRED")
            if _detail_code_exists(raw["nok_code"], details):
                return ValidationDecision("reject", "DETAIL_CODE_DUPLICATE")
    return ValidationDecision("accept")


def _evidence_error(
    expected: Mapping[str, Any],
    lookup: Any,
    record: Any,
    state_index: Any,
    current: Mapping[str, Any],
    config: Any,
) -> str | None:
    if not _lookup_is_accepted(lookup):
        return "UPSTREAM_EVIDENCE_INVALID"
    raw = record.to_dict() if isinstance(record, StationEvent) else dict(record)
    comparisons = {
        "source_event_id": raw.get("correlation", {}).get("source_event_id"),
        "parent_event_id": raw.get("event_id"),
        "parent_fact_key": raw.get("correlation", {}).get("fact_key"),
        "upstream_station_id": raw.get("station_id"),
        "upstream_plc_id": raw.get("plc_id"),
        "upstream_plc_boot_id": raw.get("plc_boot_id"),
        "upstream_event_type": raw.get("event_type"),
        "upstream_nok_code": raw.get("nok_code"),
        "upstream_config_hash": raw.get("config_hash"),
    }
    if any(expected.get(field) != value for field, value in comparisons.items()):
        return "UPSTREAM_EVIDENCE_INVALID"
    if not _evidence_route_and_subject_match(raw, current, config):
        return "UPSTREAM_EVIDENCE_INVALID"
    if expected.get("evidence_type") == "canonical_station_result":
        return None if raw.get("result") == "nok" else "UPSTREAM_EVIDENCE_INVALID"
    if raw.get("event_type") != "station_nok" or "result" in raw:
        return "UPSTREAM_EVIDENCE_INVALID"
    correlation = raw.get("correlation", {})
    if correlation.get("event_role") != "nok_detail":
        return "UPSTREAM_EVIDENCE_INVALID"
    if not validate_event(raw, config).is_valid:
        return "UPSTREAM_EVIDENCE_INVALID"
    parent_event_id = correlation.get("parent_event_id")
    parent_fact_key = correlation.get("parent_fact_key")
    if not parent_event_id or not parent_fact_key:
        return "UPSTREAM_EVIDENCE_INVALID"
    parent_lookup = state_index.lookup_parent_result(parent_event_id, parent_fact_key)
    if _is_unavailable(parent_lookup):
        return "STATE_INDEX_UNAVAILABLE"
    parent = _lookup_record(parent_lookup)
    if parent is None:
        return "UPSTREAM_EVIDENCE_NOT_FOUND"
    if not _lookup_is_accepted(parent_lookup):
        return "UPSTREAM_EVIDENCE_INVALID"
    parent_raw = parent.to_dict() if isinstance(parent, StationEvent) else dict(parent)
    return None if _parent_matches(raw, parent_raw) else "UPSTREAM_EVIDENCE_INVALID"


def _evidence_route_and_subject_match(
    evidence: Mapping[str, Any],
    current: Mapping[str, Any],
    config: Any,
) -> bool:
    if evidence.get("config_hash") != current.get("config_hash"):
        return False
    if not (
        (evidence.get("unit_id") and evidence.get("unit_id") == current.get("unit_id"))
        or (evidence.get("dmc") and evidence.get("dmc") == current.get("dmc"))
    ):
        return False
    route_graph = _attr(config, "route_graph")
    edges = _attr(route_graph, "edges") or ()
    return any(
        _attr(edge, "from_station_id") == evidence.get("station_id")
        and _attr(edge, "to_station_id") == current.get("station_id")
        for edge in edges
    )


def _parent_matches(detail: dict[str, Any], parent: dict[str, Any]) -> bool:
    correlation = detail["correlation"]
    if parent.get("event_id") != correlation["parent_event_id"]:
        return False
    if parent.get("correlation", {}).get("fact_key") != correlation["parent_fact_key"]:
        return False
    if parent.get("event_type") != "station_result":
        return False
    if parent.get("correlation", {}).get("event_role") != "production_result":
        return False
    if not _production_result_authority(parent):
        return False
    common_fields = (
        "line_id",
        "plc_id",
        "station_id",
        "plc_boot_id",
        "cycle_id",
        "cycle_counter",
        "unit_id",
        "dmc",
        "config_hash",
        "profile_id",
        "station_type",
    )
    if any(detail.get(field) != parent.get(field) for field in common_fields):
        return False
    if detail.get("nok_code") == 30003:
        return parent.get("result") == "skip"
    if parent.get("result") != "nok":
        return False
    if (detail.get("source"), detail.get("actor")) != (
        parent.get("source"),
        parent.get("actor"),
    ):
        return False
    if correlation["detail_role"] == "primary":
        return (
            detail.get("nok_code") == parent.get("nok_code")
            and detail.get("nok_origin") == parent.get("nok_origin")
        )
    return detail.get("nok_origin") == parent.get("nok_origin")


def _production_result_authority(parent: Mapping[str, Any]) -> bool:
    return (parent.get("source"), parent.get("actor")) in {
        ("plc", "plc"),
        ("vplc", "simulator"),
    }


def _detail_code_exists(nok_code: int, details: Mapping[str, Any]) -> bool:
    primary = details.get("primary")
    if primary is not None:
        primary_raw = primary.to_dict() if isinstance(primary, StationEvent) else dict(primary)
        if primary_raw.get("nok_code") == nok_code:
            return True
    for detail_key in details.get("details", ()):
        if isinstance(detail_key, tuple) and len(detail_key) >= 3 and detail_key[2] == nok_code:
            return True
        if isinstance(detail_key, Mapping) and detail_key.get("nok_code") == nok_code:
            return True
    return False


def _lookup_record(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, Mapping) and "status" in value:
        if value["status"] == "unavailable":
            return None
        return value.get("record") if value["status"] == "found" else None
    status = getattr(value, "status", None)
    if status is not None:
        return getattr(value, "record", None) if status == "found" else None
    return value


def _is_unavailable(value: Any) -> bool:
    if isinstance(value, Mapping):
        return value.get("status") == "unavailable"
    return getattr(value, "status", None) == "unavailable"


def _lookup_is_accepted(value: Any) -> bool:
    if isinstance(value, Mapping):
        disposition = value.get("disposition")
        accepted = value.get("accepted")
    else:
        disposition = getattr(value, "disposition", None)
        accepted = getattr(value, "accepted", None)
    if accepted is False:
        return False
    return disposition in {None, "accept", "accepted"}


def _sort_errors(errors: list[ValidationError]) -> list[ValidationError]:
    return sorted(
        errors,
        key=lambda error: (
            ERROR_PRECEDENCE.get(error.code, 0),
            error.path,
            error.code,
        ),
    )


def _error(path: str, code: str) -> ValidationError:
    return ValidationError(path=path, code=code, message=code.replace("_", " ").lower())


def _attr(value: Any, name: str) -> Any:
    if isinstance(value, Mapping):
        return value.get(name)
    return getattr(value, name, None)
