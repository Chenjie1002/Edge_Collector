from __future__ import annotations

import base64
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import UUID

import pytest

from common.station_event import (
    AuditSubtype,
    EventType,
    LifecycleDerivedOutput,
    StationEvent,
    StationEventValidationError,
    ValidationDecision,
    canonical_json,
    canonical_json_bytes,
    compute_content_fingerprint,
    compute_fact_key,
    compute_raw_evidence_fingerprint,
    cycle_role_key,
    derive_lifecycle,
    parse_event,
    projection_for,
    station_nok_detail_key,
    validate_duplicate_or_conflict,
    validate_event,
    validate_event_stateful,
)


CONFIG_HASH = "50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1"
BOOT_ID = "01J10C2SZM4T2R8K6V2YDR45VH"
RESULT_EVENT_ID = "550e8400-e29b-41d4-a716-446655440000"


def event_dict(
    event_type: str = "station_result",
    *,
    result: str | None = "ok",
    event_id: str = RESULT_EVENT_ID,
) -> dict:
    raw = {
        "schema_version": "1.0",
        "event_id": event_id,
        "event_type": event_type,
        "event_ts": "2026-06-20T10:15:30.123Z",
        "line_id": "LINE-01",
        "plc_id": "PLC-01",
        "station_id": "WS02",
        "station_type": "screw",
        "config_version": "2026.06.20-1",
        "config_hash": CONFIG_HASH,
        "plc_boot_id": BOOT_ID,
        "profile_id": "normal_screwdriving",
        "cycle_id": f"LINE-01/PLC-01/WS02/{BOOT_ID}/42",
        "cycle_counter": 42,
        "unit_id": "UNIT-000042",
        "dmc": "DMC-000042",
        "source": "plc",
        "actor": "plc",
        "correlation": {
            "source_event_id": "PLC-01:WS02:42:result",
            "fact_key": "pending",
            "event_role": "production_result",
            "mapping_id": "ws02_result",
        },
    }
    if result is not None:
        raw["result"] = result
    if event_type == "station_cycle_start":
        raw.pop("result", None)
        raw["correlation"]["event_role"] = "cycle_start"
        raw["correlation"]["source_event_id"] = "PLC-01:WS02:42:start"
    elif event_type == "station_cycle_complete":
        raw.pop("result", None)
        raw["correlation"]["event_role"] = "cycle_complete"
        raw["correlation"]["source_event_id"] = "PLC-01:WS02:42:complete"
    elif event_type == "station_heartbeat":
        for key in ("profile_id", "cycle_id", "cycle_counter", "unit_id", "dmc", "result"):
            raw.pop(key, None)
        raw["correlation"] = {
            "source_event_id": "PLC-01:heartbeat:9",
            "fact_key": "pending",
            "event_role": "heartbeat",
            "mapping_id": "plc01_diagnostic",
        }
        raw["diagnostic_context"] = {
            "category": "heartbeat",
            "reason_code": "periodic_heartbeat",
        }
    raw["correlation"]["fact_key"] = compute_fact_key(raw)
    return raw


def nok_result_dict() -> dict:
    raw = event_dict(result="nok")
    raw["nok_code"] = 20001
    raw["nok_origin"] = "plc"
    raw["correlation"]["fact_key"] = compute_fact_key(raw)
    return raw


def nok_detail_dict(parent: dict | None = None) -> dict:
    parent = parent or nok_result_dict()
    raw = event_dict(
        "station_nok",
        result=None,
        event_id="6ba7b810-9dad-41d1-80b4-00c04fd430c8",
    )
    raw["event_ts"] = "2026-06-20T10:15:30.124Z"
    raw["nok_code"] = 20001
    raw["nok_origin"] = "plc"
    raw["correlation"].update(
        event_role="nok_detail",
        source_event_id="PLC-01:WS02:42:nok:20001",
        parent_event_id=parent["event_id"],
        parent_fact_key=parent["correlation"]["fact_key"],
        detail_role="primary",
    )
    raw["correlation"]["fact_key"] = compute_fact_key(raw)
    return raw


def decision(disposition: str = "accept", code: str | None = None) -> ValidationDecision:
    return ValidationDecision(disposition=disposition, final_error_code=code)


def assert_rejected_event_has_no_projection(raw: dict, result: ValidationDecision) -> None:
    projection = projection_for(parse_event(raw, validate=False), result)

    assert result.disposition == "reject"
    assert projection.projection_eligible is False
    assert projection.authoritative is False
    assert projection.production_outcome is None
    assert projection.defect_detail is None
    assert projection.compatibility_projection is None


def historical_snapshot(
    *,
    station_id: str = "WS02",
    profile_id: str | None = "normal_screwdriving",
) -> SimpleNamespace:
    station_fields = {
        "station_id": station_id,
        "plc_id": "PLC-01",
        "station_type": "screw",
    }
    if profile_id is not None:
        station_fields["cycle_profile"] = profile_id
    upstream_station_fields = {
        "station_id": "WS01",
        "plc_id": "PLC-01",
        "station_type": "screw",
    }
    if profile_id is not None:
        upstream_station_fields["cycle_profile"] = profile_id
    return SimpleNamespace(
        config_hash=CONFIG_HASH,
        line_id="LINE-01",
        stations=(
            SimpleNamespace(**upstream_station_fields),
            SimpleNamespace(**station_fields),
        ),
        route_graph=SimpleNamespace(
            edges=(
                SimpleNamespace(from_station_id="WS01", to_station_id="WS02"),
            )
        ),
    )


def test_mvp_event_types_are_frozen_without_future_types() -> None:
    assert {item.value for item in EventType} == {
        "station_cycle_start",
        "station_cycle_complete",
        "station_result",
        "station_nok",
        "station_heartbeat",
    }


@pytest.mark.parametrize(
    "event_type",
    [
        "station_cycle_start",
        "station_cycle_complete",
        "station_result",
        "station_nok",
        "station_heartbeat",
    ],
)
def test_each_mvp_event_has_a_valid_minimum(event_type: str) -> None:
    if event_type == "station_nok":
        raw = nok_detail_dict()
    else:
        raw = event_dict(event_type)

    assert validate_event(raw).is_valid


def test_station_event_is_frozen_and_nested_payload_is_isolated() -> None:
    raw = event_dict()
    raw["payload"] = {"measurements": [1, {"value": 2}]}
    raw["correlation"]["payload_template"] = "screw_result_v1"
    raw["correlation"]["fact_key"] = compute_fact_key(raw)

    event = parse_event(raw)
    raw["payload"]["measurements"][1]["value"] = 99

    assert event.payload["measurements"][1]["value"] == 2
    with pytest.raises(FrozenInstanceError):
        event.line_id = "changed"  # type: ignore[misc]
    with pytest.raises(TypeError):
        event.payload["new"] = "value"  # type: ignore[index]


@pytest.mark.parametrize(
    ("mutation", "code", "path"),
    [
        (lambda raw: raw.pop("line_id"), "REQUIRED_FIELD_MISSING", "line_id"),
        (lambda raw: raw.update(unit_id=None), "FIELD_NULL_FORBIDDEN", "unit_id"),
        (lambda raw: raw.update(created_at="2026-06-20T10:15:31Z"), "FIELD_FORBIDDEN", "created_at"),
        (lambda raw: raw.update(unexpected=True), "FIELD_FORBIDDEN", "unexpected"),
        (lambda raw: raw.update(event_type="station_hold"), "RESULT_COMBINATION_INVALID", "event_type"),
    ],
)
def test_presence_and_unknown_fields_fail_closed(mutation, code: str, path: str) -> None:
    raw = event_dict()
    mutation(raw)

    result = validate_event(raw)

    assert not result.is_valid
    assert (result.errors[0].code, result.errors[0].path) == (code, path)


def test_cycle_complete_cannot_carry_result() -> None:
    raw = event_dict("station_cycle_complete")
    raw["result"] = "ok"

    result = validate_event(raw)

    assert result.errors[0].code == "FIELD_FORBIDDEN"
    assert result.errors[0].path == "result"


def test_non_detail_event_forbids_parent_and_upstream_correlation() -> None:
    raw = event_dict()
    raw["correlation"]["parent_event_id"] = RESULT_EVENT_ID
    raw["correlation"]["upstream_evidence"] = {}

    result = validate_event(raw)

    assert [(error.code, error.path) for error in result.errors[:2]] == [
        ("FIELD_FORBIDDEN", "correlation.parent_event_id"),
        ("FIELD_FORBIDDEN", "correlation.upstream_evidence"),
    ]


def test_station_result_nok_requires_code_and_origin() -> None:
    raw = event_dict(result="nok")

    result = validate_event(raw)

    assert [(error.code, error.path) for error in result.errors[:2]] == [
        ("REQUIRED_FIELD_MISSING", "nok_code"),
        ("REQUIRED_FIELD_MISSING", "nok_origin"),
    ]


def test_station_nok_forbids_authoritative_result() -> None:
    raw = nok_detail_dict()
    raw["result"] = "nok"

    result = validate_event(raw)

    assert result.errors[0].code == "FIELD_FORBIDDEN"
    assert result.errors[0].path == "result"


def test_technical_failure_cannot_become_reserved_nok() -> None:
    raw = nok_detail_dict()
    raw["nok_code"] = 30003
    raw["nok_origin"] = "system_reserved"
    raw["source"] = "system"
    raw["actor"] = "system"
    raw["correlation"]["detail_role"] = "system_reserved"
    raw["correlation"]["fact_key"] = compute_fact_key(raw)

    result = validate_event(raw)

    assert result.errors[0].code == "REQUIRED_FIELD_MISSING"
    assert result.errors[0].path == "correlation.upstream_evidence"


def test_reserved_nok_rejects_technical_failure_evidence_type() -> None:
    raw = nok_detail_dict(event_dict(result="skip"))
    raw["nok_code"] = 30003
    raw["nok_origin"] = "system_reserved"
    raw["source"] = "system"
    raw["actor"] = "system"
    raw["correlation"].update(
        detail_role="system_reserved",
        upstream_evidence={
            "evidence_type": "validation_failure",
            "source_event_id": "technical-error",
            "parent_event_id": RESULT_EVENT_ID,
            "parent_fact_key": raw["correlation"]["parent_fact_key"],
            "upstream_station_id": "WS01",
            "upstream_plc_id": "PLC-01",
            "upstream_plc_boot_id": BOOT_ID,
            "upstream_event_type": "station_result",
            "upstream_result": "nok",
            "upstream_nok_code": 20001,
            "upstream_config_hash": CONFIG_HASH,
        },
    )
    raw["correlation"]["fact_key"] = compute_fact_key(raw)

    result = validate_event(raw)

    assert result.errors[0].code == "UPSTREAM_EVIDENCE_INVALID"


@pytest.mark.parametrize(
    ("source", "actor"),
    [("system", "system"), ("plc", "simulator"), ("vplc", "plc")],
)
def test_production_authority_matrix_rejects_invalid_pairs(source: str, actor: str) -> None:
    raw = event_dict()
    raw["source"] = source
    raw["actor"] = actor

    result = validate_event(raw)

    assert result.errors[0].code == "AUTHORITY_FORBIDDEN"


def test_uuidv4_is_required_and_uuidv5_is_rejected() -> None:
    raw = event_dict(event_id="21f7f8de-8051-5b89-8680-0195ef798b6a")

    result = validate_event(raw)

    assert result.errors[0].code == "RESULT_COMBINATION_INVALID"
    assert result.errors[0].path == "event_id"


def test_timestamps_require_utc_z_and_future_tolerance() -> None:
    malformed = event_dict()
    malformed["event_ts"] = "2026-06-20T18:15:30+08:00"
    assert validate_event(malformed).errors[0].path == "event_ts"

    future = event_dict()
    future["event_ts"] = "2026-06-20T10:21:00Z"
    future["observed_at"] = "2026-06-20T10:15:00Z"
    result = validate_event(future)
    assert result.errors[0].code == "EVENT_TS_FUTURE"


def test_canonical_json_orders_keys_preserves_array_order_and_normalizes_numbers() -> None:
    value = {
        "z": None,
        "array": [3, 2, 1],
        "numbers": [-0.0, 0.0, 1.0, 1e30, 0.000001, 1.7976931348623157e308],
        "a": "é",
    }

    assert canonical_json(value) == (
        '{"a":"é","array":[3,2,1],"numbers":[0,0,1,1e+30,0.000001,'
        '1.7976931348623157e+308],"z":null}'
    )
    assert canonical_json_bytes(value) == canonical_json(value).encode("utf-8")


def test_canonical_serializer_omits_absent_fields_and_round_trips() -> None:
    event = parse_event(event_dict())

    serialized = event.to_dict()
    reparsed = parse_event(serialized)

    assert "payload" not in serialized
    assert "raw_payload" not in serialized
    assert reparsed == event


def test_fact_key_matches_official_result_vector() -> None:
    raw = event_dict()

    assert compute_fact_key(raw) == (
        "sha256:b08052bccb4d32c97b2c5da96540cb7a64f1a63a9bcedc7e0c418a9bc6542b7e"
    )


def test_fact_key_matches_official_nok_detail_vector() -> None:
    assert compute_fact_key(nok_detail_dict()) == (
        "sha256:61dda2995f339952e040fcbd69f4aceaf6f1ac6c2d846d389c9de8c0b10c9ed4"
    )


def test_content_fingerprint_matches_official_result_vector() -> None:
    raw = nok_result_dict()
    raw["payload"] = {"torque_nm": 4.8, "angle_deg": 132.5}
    raw["correlation"]["payload_template"] = "screw_result_v1"
    raw["correlation"]["fact_key"] = compute_fact_key(raw)

    assert compute_content_fingerprint(raw) == (
        "sha256:4759aa7e6b81da994006afd8edc1e9ccc9286863dfc43d47b0d610406fce5f44"
    )


def test_content_fingerprint_excludes_only_transport_identity_fields() -> None:
    raw = nok_result_dict()
    first = compute_content_fingerprint(raw)
    raw["event_id"] = "5a56d642-667f-4e7e-a7ad-55bf842f4a59"
    raw["observed_at"] = "2026-06-20T10:15:31Z"
    raw["correlation"]["source_event_id"] = "retry-source-id"

    assert compute_content_fingerprint(raw) == first

    raw["result"] = "ok"
    assert compute_content_fingerprint(raw) != first


def test_raw_fingerprint_is_deterministic_and_key_order_independent() -> None:
    assert compute_raw_evidence_fingerprint({"b": 2, "a": [1, 2]}) == (
        compute_raw_evidence_fingerprint({"a": [1, 2], "b": 2})
    )


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("payload", {"value": "x" * 4097}, "PAYLOAD_STRING_BYTES_LIMIT"),
        ("raw_payload", {"value": "x" * 16385}, "RAW_STRING_BYTES_LIMIT"),
        ("payload", {"values": list(range(129))}, "PAYLOAD_ARRAY_ITEMS_LIMIT"),
        ("payload", {"value": float("nan")}, "JSON_NUMBER_NON_FINITE"),
        ("payload", {"value": b"binary"}, "PAYLOAD_TYPE_FORBIDDEN"),
        ("payload", {"value": 9007199254740992}, "JSON_NUMBER_RANGE"),
    ],
)
def test_payload_resource_failures_have_unique_codes(field: str, value, code: str) -> None:
    raw = event_dict()
    raw[field] = value
    raw["correlation"]["payload_template"] = "screw_result_v1"
    if field == "raw_payload":
        raw["correlation"]["raw_encoding"] = "json"

    result = validate_event(raw)

    assert result.errors[0].code == code


def test_payload_and_raw_total_byte_limits() -> None:
    payload = event_dict()
    payload["payload"] = {"a": "x" * 16384}
    payload["correlation"]["payload_template"] = "screw_result_v1"
    assert validate_event(payload).errors[0].code == "PAYLOAD_TOTAL_BYTES_LIMIT"

    raw = event_dict()
    raw["raw_payload"] = {"a": "x" * 65536}
    raw["correlation"].update(payload_template="screw_result_v1", raw_encoding="json")
    assert validate_event(raw).errors[0].code == "RAW_TOTAL_BYTES_LIMIT"


def test_payload_error_precedence_is_deterministic() -> None:
    raw = event_dict()
    raw["payload"] = {"z": float("nan"), "a": b"binary"}
    raw["correlation"]["payload_template"] = "screw_result_v1"

    result = validate_event(raw)

    assert (result.errors[0].code, result.errors[0].path) == (
        "PAYLOAD_TYPE_FORBIDDEN",
        "payload.a",
    )


def test_whole_tree_node_limit_counts_keys_and_array_item_nodes() -> None:
    values = [{"b": 0} for _ in range(127)]
    values[0] = {"b": [0]}
    raw = event_dict()
    raw["payload"] = {"a": values}
    raw["correlation"]["payload_template"] = "screw_result_v1"

    result = validate_event(raw)

    assert result.errors[0].code == "PAYLOAD_TREE_NODE_LIMIT"


def test_config_lineage_matches_historical_snapshot_without_current_fallback() -> None:
    snapshot = historical_snapshot()
    assert validate_event(event_dict(), snapshot).is_valid

    wrong_hash = SimpleNamespace(
        config_hash="0" * 64,
        line_id="LINE-01",
        stations=snapshot.stations,
    )
    result = validate_event(event_dict(), wrong_hash)
    assert (result.errors[0].code, result.errors[0].path) == (
        "CONFIG_HASH_MISMATCH",
        "config_hash",
    )


@pytest.mark.parametrize(
    ("snapshot", "expected_code"),
    [
        (
            SimpleNamespace(
                config_hash=CONFIG_HASH,
                line_id="LINE-01",
                stations=(),
            ),
            "CONFIG_NOT_FOUND",
        ),
        (historical_snapshot(station_id="WS99"), "CONFIG_NOT_FOUND"),
        (historical_snapshot(profile_id=None), "EVENT_LINEAGE_INVALID"),
        (historical_snapshot(profile_id="different_profile"), "EVENT_LINEAGE_INVALID"),
    ],
)
def test_stateful_historical_snapshot_revalidates_station_and_profile_lineage(
    snapshot, expected_code: str
) -> None:
    result = validate_event_stateful(event_dict(), StateIndex(config=snapshot))

    assert (result.disposition, result.final_error_code) == ("reject", expected_code)


def test_stateful_historical_snapshot_accepts_matching_station_and_profile_lineage() -> None:
    result = validate_event_stateful(
        event_dict(),
        StateIndex(config=historical_snapshot()),
    )

    assert result.disposition == "accept"


def test_disabled_station_allows_heartbeat_but_rejects_production_event() -> None:
    station = SimpleNamespace(
        station_id="WS02",
        plc_id="PLC-01",
        station_type="screw",
        cycle_profile="normal_screwdriving",
        station_enabled=False,
    )
    snapshot = SimpleNamespace(
        config_hash=CONFIG_HASH,
        line_id="LINE-01",
        stations=(station,),
    )

    production = validate_event(event_dict(), snapshot)
    assert production.errors[0].code == "EVENT_LINEAGE_INVALID"

    heartbeat = event_dict("station_heartbeat")
    heartbeat["diagnostic_context"] = {
        "category": "disabled_station",
        "reason_code": "station_disabled",
    }
    assert validate_event(heartbeat, snapshot).is_valid


def test_raw_decoder_mismatch_is_rejected_without_production_semantics() -> None:
    station = SimpleNamespace(
        station_id="WS02",
        plc_id="PLC-01",
        station_type="screw",
        cycle_profile="normal_screwdriving",
    )

    class Snapshot:
        config_hash = CONFIG_HASH
        line_id = "LINE-01"
        stations = (station,)

        @staticmethod
        def decode_raw_payload(raw_payload, _event):
            assert raw_payload == {"register": 1}
            return {"value": 2}

    raw = event_dict()
    raw["payload"] = {"value": 1}
    raw["raw_payload"] = {"register": 1}
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )
    raw["correlation"]["fact_key"] = compute_fact_key(raw)

    validation = validate_event(raw, Snapshot())
    result = decision("reject", validation.errors[0].code)

    assert validation.errors[0].code == "RAW_NORMALIZED_MISMATCH"
    assert_rejected_event_has_no_projection(raw, result)


def test_raw_payload_requires_historical_decoder() -> None:
    raw = event_dict()
    raw["payload"] = {"value": 1}
    raw["raw_payload"] = {"register": 1}
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )
    raw["correlation"]["fact_key"] = compute_fact_key(raw)

    validation = validate_event(raw, historical_snapshot())
    result = decision("reject", validation.errors[0].code)

    assert validation.errors[0].code == "RAW_PARSE_ERROR"
    assert_rejected_event_has_no_projection(raw, result)


def test_raw_only_event_is_rejected_without_canonical_business_projection() -> None:
    raw = event_dict()
    raw["raw_payload"] = {"register": 1}
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )
    raw["correlation"]["fact_key"] = compute_fact_key(raw)

    validation = validate_event(raw, historical_snapshot())
    result = decision("reject", validation.errors[0].code)

    assert validation.errors[0].code == "RAW_PARSE_ERROR"
    assert_rejected_event_has_no_projection(raw, result)


def test_raw_decoder_exception_is_rejected_without_production_semantics() -> None:
    class Snapshot:
        config_hash = CONFIG_HASH
        line_id = "LINE-01"
        stations = historical_snapshot().stations

        @staticmethod
        def decode_raw_payload(_raw_payload, _event):
            raise RuntimeError("decoder failed")

    raw = event_dict()
    raw["payload"] = {"value": 1}
    raw["raw_payload"] = {"register": 1}
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )
    raw["correlation"]["fact_key"] = compute_fact_key(raw)

    validation = validate_event(raw, Snapshot())
    result = decision("reject", validation.errors[0].code)

    assert validation.errors[0].code == "RAW_PARSE_ERROR"
    assert_rejected_event_has_no_projection(raw, result)


def test_business_keys_are_config_independent_where_contract_requires() -> None:
    result = nok_result_dict()
    detail = nok_detail_dict(result)

    assert cycle_role_key(result) == (
        "LINE-01",
        "PLC-01",
        "WS02",
        BOOT_ID,
        42,
        "production_result",
    )
    assert station_nok_detail_key(detail) == (
        result["correlation"]["fact_key"],
        "primary",
        20001,
        "plc",
    )


@pytest.mark.parametrize(
    ("existing_content", "incoming_content", "existing_raw", "incoming_raw", "expected"),
    [
        ("same", "same", "raw", "raw", ("duplicate", AuditSubtype.NONE, None)),
        ("same", "same", "raw-a", "raw-b", ("duplicate", AuditSubtype.RAW_VARIANT, None)),
        ("old", "new", "raw-a", "raw-b", ("conflict", AuditSubtype.NONE, "CYCLE_ROLE_CONFLICT")),
    ],
)
def test_duplicate_raw_variant_and_conflict_rules(
    existing_content: str,
    incoming_content: str,
    existing_raw: str,
    incoming_raw: str,
    expected,
) -> None:
    result = validate_duplicate_or_conflict(
        matched_key_type="cycle_role_key",
        matched_key_value=("slot",),
        existing_event_id=RESULT_EVENT_ID,
        existing_content_fingerprint=existing_content,
        incoming_content_fingerprint=incoming_content,
        existing_raw_evidence_fingerprint=existing_raw,
        incoming_raw_evidence_fingerprint=incoming_raw,
    )

    assert (result.disposition, result.audit_subtype, result.final_error_code) == expected


class StateIndex:
    def __init__(
        self,
        *,
        parent=None,
        slot=None,
        unavailable: bool = False,
        config=...,
        upstream=None,
        detail_set=None,
        evidence_parent=...,
    ) -> None:
        self.parent = parent
        self.slot = slot
        self.unavailable = unavailable
        self.config = historical_snapshot() if config is ... else config
        self.upstream = upstream
        self.evidence_parent = parent if evidence_parent is ... else evidence_parent
        self.detail_set = detail_set or {
            "primary": None,
            "details": set(),
            "system_reserved": None,
        }

    def lookup_by_event_id(self, _key):
        return {"status": "unavailable"} if self.unavailable else None

    def lookup_by_fact_key(self, _key):
        return None

    def lookup_cycle_role(self, _key):
        return self.slot

    def lookup_parent_result(self, event_id, fact_key):
        if self.unavailable:
            return {"status": "unavailable"}
        if self.parent is not None:
            parent_raw = (
                self.parent.to_dict()
                if isinstance(self.parent, StationEvent)
                else self.parent.get("record", self.parent)
                if isinstance(self.parent, dict)
                else self.parent
            )
            if (
                isinstance(parent_raw, dict)
                and parent_raw.get("event_id") == event_id
                and parent_raw.get("correlation", {}).get("fact_key") == fact_key
            ):
                return self.parent
        return self.evidence_parent

    def lookup_upstream_evidence(self, _evidence):
        return self.upstream

    def lookup_detail_set(self, _parent_fact_key):
        return self.detail_set

    def lookup_detail_key(self, _key):
        return None

    def lookup_resolved_config(self, _config_hash):
        return self.config


def test_station_nok_requires_accepted_nok_parent() -> None:
    raw = nok_detail_dict()

    missing = validate_event_stateful(raw, StateIndex(parent=None))
    assert (missing.disposition, missing.final_error_code) == ("reject", "PARENT_NOT_FOUND")

    ok_parent = event_dict(result="ok")
    invalid = validate_event_stateful(raw, StateIndex(parent=ok_parent))
    assert (invalid.disposition, invalid.final_error_code) == (
        "reject",
        "PARENT_EVENT_INVALID",
    )

    accepted = validate_event_stateful(raw, StateIndex(parent=nok_result_dict()))
    assert accepted.disposition == "accept"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("profile_id", "alternate_profile"),
        ("station_type", "inspection"),
    ],
)
def test_station_nok_parent_requires_profile_and_station_type_lineage(
    field: str,
    value: str,
) -> None:
    parent = nok_result_dict()
    raw = nok_detail_dict(parent)
    parent[field] = value

    result = validate_event_stateful(raw, StateIndex(parent=parent))

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "PARENT_EVENT_INVALID",
    )
    assert_rejected_event_has_no_projection(raw, result)


def test_state_index_unavailable_is_not_misreported_as_missing_parent() -> None:
    result = validate_event_stateful(nok_detail_dict(), StateIndex(unavailable=True))

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "STATE_INDEX_UNAVAILABLE",
    )


def test_stateful_validation_requires_historical_config_snapshot() -> None:
    missing = validate_event_stateful(event_dict(), StateIndex(config=None))
    assert (missing.disposition, missing.final_error_code) == (
        "reject",
        "CONFIG_NOT_FOUND",
    )


def test_reserved_nok_requires_accepted_upstream_business_evidence() -> None:
    parent = event_dict(result="skip")
    raw = nok_detail_dict(parent)
    raw["nok_code"] = 30003
    raw["nok_origin"] = "system_reserved"
    raw["source"] = "system"
    raw["actor"] = "system"
    raw["correlation"].update(
        detail_role="system_reserved",
        upstream_evidence={
            "evidence_type": "canonical_station_result",
            "source_event_id": "PLC-01:WS01:41:result",
            "parent_event_id": "6dd98f06-35b3-4bcb-aa04-9f128f22ea94",
            "parent_fact_key": "sha256:" + "1" * 64,
            "upstream_station_id": "WS01",
            "upstream_plc_id": "PLC-01",
            "upstream_plc_boot_id": BOOT_ID,
            "upstream_event_type": "station_result",
            "upstream_result": "nok",
            "upstream_nok_code": 20001,
            "upstream_config_hash": CONFIG_HASH,
        },
    )
    raw["correlation"]["fact_key"] = compute_fact_key(raw)

    result = validate_event_stateful(raw, StateIndex(parent=parent, upstream=None))

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_NOT_FOUND",
    )


def reserved_nok_detail(parent: dict) -> dict:
    raw = nok_detail_dict(parent)
    raw["nok_code"] = 30003
    raw["nok_origin"] = "system_reserved"
    raw["source"] = "system"
    raw["actor"] = "system"
    raw["correlation"].update(
        detail_role="system_reserved",
        upstream_evidence={
            "evidence_type": "canonical_station_result",
            "source_event_id": "PLC-01:WS01:41:result",
            "parent_event_id": "6dd98f06-35b3-4bcb-aa04-9f128f22ea94",
            "parent_fact_key": "sha256:" + "1" * 64,
            "upstream_station_id": "WS01",
            "upstream_plc_id": "PLC-01",
            "upstream_plc_boot_id": BOOT_ID,
            "upstream_event_type": "station_result",
            "upstream_result": "nok",
            "upstream_nok_code": 20001,
            "upstream_config_hash": CONFIG_HASH,
        },
    )
    raw["correlation"]["fact_key"] = compute_fact_key(raw)
    return raw


@pytest.mark.parametrize("changed_field", ["station_id", "cycle_id", "cycle_counter"])
def test_reserved_nok_rejects_cross_station_or_cycle_parent(changed_field: str) -> None:
    parent = event_dict(result="skip")
    raw = reserved_nok_detail(parent)
    parent[changed_field] = {
        "station_id": "WS03",
        "cycle_id": f"LINE-01/PLC-01/WS02/{BOOT_ID}/41",
        "cycle_counter": 41,
    }[changed_field]

    result = validate_event_stateful(
        raw,
        StateIndex(parent=parent, upstream=nok_result_dict()),
    )

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "PARENT_EVENT_INVALID",
    )


def accepted_upstream_result_for(raw: dict) -> dict:
    evidence = nok_result_dict()
    evidence["station_id"] = "WS01"
    evidence["correlation"]["source_event_id"] = "PLC-01:WS01:41:result"
    evidence["event_id"] = raw["correlation"]["upstream_evidence"]["parent_event_id"]
    evidence["correlation"]["fact_key"] = raw["correlation"]["upstream_evidence"][
        "parent_fact_key"
    ]
    return evidence


def test_reserved_nok_same_station_cycle_skip_parent_is_non_production_isolated() -> None:
    parent = event_dict(result="skip")
    raw = reserved_nok_detail(parent)
    evidence = accepted_upstream_result_for(raw)

    result = validate_event_stateful(
        raw,
        StateIndex(parent=parent, upstream=evidence),
    )

    assert result.disposition == "accept"
    assert projection_for(parse_event(raw), result).defect_detail is None


def test_reserved_nok_rejects_same_cycle_parent_from_different_config() -> None:
    parent = event_dict(result="skip")
    raw = reserved_nok_detail(parent)
    parent["config_hash"] = "1" * 64

    result = validate_event_stateful(
        raw,
        StateIndex(parent=parent, upstream=accepted_upstream_result_for(raw)),
    )

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "PARENT_EVENT_INVALID",
    )
    assert projection_for(parse_event(raw), result).defect_detail is None


def test_reserved_nok_rejects_future_or_non_result_parent() -> None:
    parent = event_dict(result="skip")
    raw = reserved_nok_detail(parent)
    parent["event_type"] = "station_skip"

    result = validate_event_stateful(raw, StateIndex(parent=parent))

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "PARENT_EVENT_INVALID",
    )


def secondary_detail(parent: dict, code: int, event_id: str) -> dict:
    raw = nok_detail_dict(parent)
    raw["event_id"] = event_id
    raw["nok_code"] = code
    raw["correlation"]["detail_role"] = "secondary"
    raw["correlation"]["source_event_id"] = f"PLC-01:WS02:42:nok:{code}"
    raw["correlation"]["fact_key"] = compute_fact_key(raw)
    return raw


def test_secondary_codes_must_be_distinct_from_primary_and_each_other() -> None:
    parent = nok_result_dict()
    primary = parse_event(nok_detail_dict(parent))
    secondary_b = parse_event(
        secondary_detail(parent, 20002, "ab196728-c67b-4f98-b44d-cb56a4a14a01")
    )
    details = {
        "primary": primary,
        "details": {
            station_nok_detail_key(primary.to_dict()),
            station_nok_detail_key(secondary_b.to_dict()),
        },
        "system_reserved": None,
    }

    valid = validate_event_stateful(
        secondary_detail(parent, 20003, "238438f9-b7ce-4f9d-96f4-dc1c77f73818"),
        StateIndex(parent=parent, detail_set=details),
    )
    primary_duplicate = validate_event_stateful(
        secondary_detail(parent, 20001, "83ae22da-9117-4ac4-8f6b-a7f37c52b4fc"),
        StateIndex(parent=parent, detail_set=details),
    )
    secondary_duplicate = validate_event_stateful(
        secondary_detail(parent, 20002, "2e3a34a0-2310-4fbf-a6d7-dc07bb88b1e3"),
        StateIndex(parent=parent, detail_set=details),
    )

    assert valid.disposition == "accept"
    assert (primary_duplicate.disposition, primary_duplicate.final_error_code) == (
        "reject",
        "DETAIL_CODE_DUPLICATE",
    )
    assert (secondary_duplicate.disposition, secondary_duplicate.final_error_code) == (
        "reject",
        "DETAIL_CODE_DUPLICATE",
    )


def test_secondary_without_primary_is_rejected_and_absent_secondary_is_allowed() -> None:
    parent = nok_result_dict()
    missing_primary = validate_event_stateful(
        secondary_detail(parent, 20002, "32c2f35e-95b0-4d92-b10e-b583ea4f5f72"),
        StateIndex(parent=parent),
    )
    primary_only = validate_event_stateful(
        nok_detail_dict(parent),
        StateIndex(parent=parent),
    )

    assert (missing_primary.disposition, missing_primary.final_error_code) == (
        "reject",
        "PRIMARY_DETAIL_REQUIRED",
    )
    assert primary_only.disposition == "accept"


def validated_detail_evidence(detail: dict) -> dict:
    return {
        "evidence_type": "validated_nok_detail",
        "source_event_id": detail["correlation"]["source_event_id"],
        "parent_event_id": detail["event_id"],
        "parent_fact_key": detail["correlation"]["fact_key"],
        "upstream_station_id": detail["station_id"],
        "upstream_plc_id": detail["plc_id"],
        "upstream_plc_boot_id": detail["plc_boot_id"],
        "upstream_event_type": "station_nok",
        "upstream_result": "nok",
        "upstream_nok_code": detail["nok_code"],
        "upstream_config_hash": detail["config_hash"],
    }


def distinct_canonical_nok_parent() -> dict:
    parent = nok_result_dict()
    parent["event_id"] = "a9ce4748-f633-48e0-84be-03a9514bf32d"
    parent["station_id"] = "WS01"
    parent["cycle_id"] = f"LINE-01/PLC-01/WS01/{BOOT_ID}/42"
    return parent


def cited_detail_for(parent: dict) -> dict:
    detail = nok_detail_dict(parent)
    detail["station_id"] = parent["station_id"]
    detail["cycle_id"] = parent["cycle_id"]
    detail["correlation"]["fact_key"] = compute_fact_key(detail)
    return detail


def test_validated_nok_detail_requires_accepted_canonical_nok_parent() -> None:
    skip_parent = event_dict(result="skip")
    current = reserved_nok_detail(skip_parent)
    canonical_parent = distinct_canonical_nok_parent()
    cited_detail = cited_detail_for(canonical_parent)
    current["correlation"]["upstream_evidence"] = validated_detail_evidence(cited_detail)
    current["correlation"]["fact_key"] = compute_fact_key(current)

    accepted = validate_event_stateful(
        current,
        StateIndex(
            parent=skip_parent,
            upstream=cited_detail,
            evidence_parent=canonical_parent,
        ),
    )
    missing = validate_event_stateful(
        current,
        StateIndex(parent=skip_parent, upstream=cited_detail, evidence_parent=None),
    )
    ok_parent = event_dict(result="ok")
    invalid_ok = validate_event_stateful(
        current,
        StateIndex(
            parent=skip_parent,
            upstream=cited_detail,
            evidence_parent=ok_parent,
        ),
    )

    assert accepted.disposition == "accept"
    assert (missing.disposition, missing.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_NOT_FOUND",
    )
    assert (invalid_ok.disposition, invalid_ok.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_INVALID",
    )


@pytest.mark.parametrize("event_role", ["compatibility", "diagnostic", "cycle_complete"])
def test_validated_nok_detail_rejects_cited_detail_with_wrong_role(
    event_role: str,
) -> None:
    skip_parent = event_dict(result="skip")
    current = reserved_nok_detail(skip_parent)
    canonical_parent = distinct_canonical_nok_parent()
    cited_detail = cited_detail_for(canonical_parent)
    cited_detail["correlation"]["event_role"] = event_role
    current["correlation"]["upstream_evidence"] = validated_detail_evidence(
        cited_detail
    )
    current["correlation"]["fact_key"] = compute_fact_key(current)

    result = validate_event_stateful(
        current,
        StateIndex(
            parent=skip_parent,
            upstream=cited_detail,
            evidence_parent=canonical_parent,
        ),
    )

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_INVALID",
    )
    assert_rejected_event_has_no_projection(current, result)


def test_validated_nok_detail_rejects_cited_detail_without_role() -> None:
    skip_parent = event_dict(result="skip")
    current = reserved_nok_detail(skip_parent)
    canonical_parent = distinct_canonical_nok_parent()
    cited_detail = cited_detail_for(canonical_parent)
    cited_detail["correlation"].pop("event_role")
    current["correlation"]["upstream_evidence"] = validated_detail_evidence(
        cited_detail
    )
    current["correlation"]["fact_key"] = compute_fact_key(current)

    result = validate_event_stateful(
        current,
        StateIndex(
            parent=skip_parent,
            upstream=cited_detail,
            evidence_parent=canonical_parent,
        ),
    )

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_INVALID",
    )
    assert_rejected_event_has_no_projection(current, result)


@pytest.mark.parametrize(
    "mutation",
    [
        "config_mismatch",
        "authority_mismatch",
        "primary_code_mismatch",
        "origin_mismatch",
    ],
)
def test_validated_nok_detail_replays_full_canonical_parent_relation(
    mutation: str,
) -> None:
    skip_parent = event_dict(result="skip")
    current = reserved_nok_detail(skip_parent)
    canonical_parent = distinct_canonical_nok_parent()
    cited_detail = cited_detail_for(canonical_parent)
    if mutation == "config_mismatch":
        canonical_parent["config_hash"] = "1" * 64
    elif mutation == "authority_mismatch":
        canonical_parent["source"] = "vplc"
        canonical_parent["actor"] = "simulator"
        canonical_parent["nok_origin"] = "simulator"
    elif mutation == "primary_code_mismatch":
        canonical_parent["nok_code"] = 20002
    else:
        canonical_parent["nok_origin"] = "simulator"
    current["correlation"]["upstream_evidence"] = validated_detail_evidence(
        cited_detail
    )
    current["correlation"]["fact_key"] = compute_fact_key(current)

    result = validate_event_stateful(
        current,
        StateIndex(
            parent=skip_parent,
            upstream=cited_detail,
            evidence_parent=canonical_parent,
        ),
    )

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_INVALID",
    )
    assert projection_for(parse_event(current), result).defect_detail is None


@pytest.mark.parametrize("event_type", ["station_cycle_complete", "station_heartbeat"])
def test_validated_nok_detail_rejects_non_authoritative_parent_roles(
    event_type: str,
) -> None:
    skip_parent = event_dict(result="skip")
    current = reserved_nok_detail(skip_parent)
    canonical_parent = distinct_canonical_nok_parent()
    cited_detail = cited_detail_for(canonical_parent)
    canonical_parent["event_type"] = event_type
    current["correlation"]["upstream_evidence"] = validated_detail_evidence(
        cited_detail
    )
    current["correlation"]["fact_key"] = compute_fact_key(current)

    result = validate_event_stateful(
        current,
        StateIndex(
            parent=skip_parent,
            upstream=cited_detail,
            evidence_parent=canonical_parent,
        ),
    )

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_INVALID",
    )


@pytest.mark.parametrize(
    "event_role",
    ["cycle_complete", "diagnostic", "compatibility", None],
)
def test_validated_nok_detail_requires_production_result_parent_role(
    event_role: str | None,
) -> None:
    skip_parent = event_dict(result="skip")
    current = reserved_nok_detail(skip_parent)
    canonical_parent = distinct_canonical_nok_parent()
    cited_detail = cited_detail_for(canonical_parent)
    canonical_parent["correlation"]["event_role"] = event_role
    current["correlation"]["upstream_evidence"] = validated_detail_evidence(
        cited_detail
    )
    current["correlation"]["fact_key"] = compute_fact_key(current)

    result = validate_event_stateful(
        current,
        StateIndex(
            parent=skip_parent,
            upstream=cited_detail,
            evidence_parent=canonical_parent,
        ),
    )

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_INVALID",
    )
    projection = projection_for(parse_event(current), result)
    assert not projection.projection_eligible
    assert projection.production_outcome is None
    assert projection.defect_detail is None


def test_validated_nok_detail_rejects_missing_production_result_parent_role() -> None:
    skip_parent = event_dict(result="skip")
    current = reserved_nok_detail(skip_parent)
    canonical_parent = distinct_canonical_nok_parent()
    cited_detail = cited_detail_for(canonical_parent)
    canonical_parent["correlation"].pop("event_role")
    current["correlation"]["upstream_evidence"] = validated_detail_evidence(
        cited_detail
    )
    current["correlation"]["fact_key"] = compute_fact_key(current)

    result = validate_event_stateful(
        current,
        StateIndex(
            parent=skip_parent,
            upstream=cited_detail,
            evidence_parent=canonical_parent,
        ),
    )

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_INVALID",
    )


@pytest.mark.parametrize("parent_status", ["duplicate", "conflict", "reject"])
def test_validated_nok_detail_rejects_non_accepted_parent_status(parent_status: str) -> None:
    skip_parent = event_dict(result="skip")
    current = reserved_nok_detail(skip_parent)
    canonical_parent = distinct_canonical_nok_parent()
    cited_detail = cited_detail_for(canonical_parent)
    current["correlation"]["upstream_evidence"] = validated_detail_evidence(cited_detail)
    current["correlation"]["fact_key"] = compute_fact_key(current)

    result = validate_event_stateful(
        current,
        StateIndex(
            parent=skip_parent,
            upstream=cited_detail,
            evidence_parent={
                "status": "found",
                "record": canonical_parent,
                "disposition": parent_status,
            },
        ),
    )

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_INVALID",
    )


@pytest.mark.parametrize("mutation", ["wrong_predecessor", "subject_mismatch"])
def test_validated_nok_detail_requires_route_and_subject_lineage(mutation: str) -> None:
    skip_parent = event_dict(result="skip")
    current = reserved_nok_detail(skip_parent)
    canonical_parent = distinct_canonical_nok_parent()
    cited_detail = cited_detail_for(canonical_parent)
    if mutation == "wrong_predecessor":
        cited_detail["station_id"] = "WS03"
        canonical_parent["station_id"] = "WS03"
    else:
        cited_detail["unit_id"] = "UNIT-OTHER"
        cited_detail["dmc"] = "DMC-OTHER"
        canonical_parent["unit_id"] = "UNIT-OTHER"
        canonical_parent["dmc"] = "DMC-OTHER"
    current["correlation"]["upstream_evidence"] = validated_detail_evidence(cited_detail)
    current["correlation"]["fact_key"] = compute_fact_key(current)

    result = validate_event_stateful(
        current,
        StateIndex(
            parent=skip_parent,
            upstream=cited_detail,
            evidence_parent=canonical_parent,
        ),
    )

    assert (result.disposition, result.final_error_code) == (
        "reject",
        "UPSTREAM_EVIDENCE_INVALID",
    )


@pytest.mark.parametrize(
    "raw_payload",
    [
        {"blob": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"},
        {"payload": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"},
        {"image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"},
        {"binary": "R0lGODlhAQABAIAAAP"},
        {"file": "/9j/4AAQSkZJRgABAQAAAQABAAD"},
        {"message": ("2026-06-21 INFO repeated log line\n" * 300)},
    ],
)
def test_raw_binary_image_and_unbounded_log_content_is_rejected(raw_payload: dict) -> None:
    raw = event_dict()
    raw["raw_payload"] = raw_payload
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )

    result = validate_event(raw)

    assert result.errors[0].code == "RAW_CONTENT_FORBIDDEN"


@pytest.mark.parametrize(
    "raw_payload",
    [
        {
            "content": (
                "data:image/webp;base64,"
                "UklGRhQAAABXRUJQVlA4IAgAAAAwAQCdASoBAAEAAUAmJaQAA3AA/v89WAAAAA=="
            )
        },
        {
            "payload": (
                "UklGRhQAAABXRUJQVlA4IAgAAAAwAQCdASoBAAEAAUAmJaQAA3AA/v89WAAAAA=="
            )
        },
        {"raw": base64.b64encode(b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n1 0 obj\n").decode("ascii")},
        {
            "note": base64.b64encode(
                bytes(range(256)) + b"\x00\xff\x10\x80generic-binary"
            ).decode("ascii")
        },
        {"mime": "application/pdf"},
        {"content_type": "application/octet-stream"},
    ],
)
def test_raw_webp_pdf_and_generic_binary_base64_is_rejected(
    raw_payload: dict,
) -> None:
    raw = event_dict()
    raw["raw_payload"] = raw_payload
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )

    result = validate_event(raw)

    assert result.errors[0].code == "RAW_CONTENT_FORBIDDEN"


@pytest.mark.parametrize("key", ["pdf", "binary", "blob", "file"])
def test_encoded_payload_under_binary_key_hints_is_rejected(key: str) -> None:
    raw = event_dict()
    raw["raw_payload"] = {
        key: base64.b64encode(b"%PDF-1.7\nbinary attachment").decode("ascii")
    }
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )

    result = validate_event(raw)

    assert result.errors[0].code == "RAW_CONTENT_FORBIDDEN"


@pytest.mark.parametrize(
    "raw_payload",
    [
        {"message": "ERR " * 1792},
        {"content": "A" * 7168},
    ],
)
def test_seven_kib_single_line_repeated_raw_text_is_rejected(
    raw_payload: dict,
) -> None:
    raw = event_dict()
    raw["raw_payload"] = raw_payload
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )

    result = validate_event(raw)

    assert result.errors[0].code == "RAW_CONTENT_FORBIDDEN"


@pytest.mark.parametrize(
    "fragment",
    [
        "fault-code-17|station-WS02|",
        "station=WS1;cycle=C001;result=NOK;",
    ],
)
def test_seven_kib_periodic_raw_fragments_are_rejected(fragment: str) -> None:
    raw = event_dict()
    raw["raw_payload"] = {
        "message": (fragment * ((7168 // len(fragment)) + 1))[:7168]
    }
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )

    result = validate_event(raw)

    assert result.errors[0].code == "RAW_CONTENT_FORBIDDEN"


@pytest.mark.parametrize(
    "value",
    [
        base64.b64encode(b"%PDF-1.7\n" + (b"\x00binary-pdf" * 2048)).decode(
            "ascii"
        ),
        base64.b64encode(bytes(range(256)) * 64).decode("ascii"),
        "data:image/webp;base64," + ("A" * 17000),
        "data:application/pdf;base64," + ("A" * 17000),
    ],
)
def test_oversized_binary_base64_keeps_forbidden_content_precedence(
    value: str,
) -> None:
    raw = event_dict()
    raw["raw_payload"] = {"content": value}
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )

    result = validate_event(raw)

    assert result.errors[0].code == "RAW_CONTENT_FORBIDDEN"


def test_normal_short_raw_text_fields_are_accepted() -> None:
    raw = event_dict()
    raw["raw_payload"] = {
        "dmc": "DMC-000042",
        "station_note": "WS02 fixture seated; torque profile ready",
        "status_text": "fixture seated",
        "operator_note": "short diagnostic note",
        "message": "Cycle completed with stable torque and angle measurements.",
        "content_type": "text/plain",
        "trace_summary": " ".join(
            f"measurement-{index}=stable" for index in range(256)
        ),
    }
    raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )

    assert validate_event(raw).is_valid


def test_stateful_same_slot_uses_content_and_raw_fingerprints() -> None:
    raw = event_dict()
    existing = parse_event(raw)

    duplicate = validate_event_stateful(raw, StateIndex(slot=existing))
    assert duplicate.disposition == "duplicate"

    changed = event_dict()
    changed["event_ts"] = "2026-06-20T10:15:31Z"
    changed["correlation"]["fact_key"] = compute_fact_key(changed)
    conflict = validate_event_stateful(changed, StateIndex(slot=existing))
    assert (conflict.disposition, conflict.final_error_code) == (
        "conflict",
        "CYCLE_ROLE_CONFLICT",
    )


def test_stateful_raw_variant_is_duplicate_audit_only() -> None:
    class Snapshot:
        config_hash = CONFIG_HASH
        line_id = "LINE-01"
        stations = historical_snapshot().stations

        @staticmethod
        def decode_raw_payload(_raw_payload, _event):
            return {"value": 1}

    existing_raw = event_dict()
    existing_raw["payload"] = {"value": 1}
    existing_raw["raw_payload"] = {"register": 1}
    existing_raw["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )
    existing_raw["correlation"]["fact_key"] = compute_fact_key(existing_raw)
    incoming = event_dict()
    incoming["payload"] = {"value": 1}
    incoming["raw_payload"] = {"register": 2}
    incoming["correlation"].update(
        payload_template="screw_result_v1",
        raw_encoding="json",
    )
    incoming["correlation"]["fact_key"] = compute_fact_key(incoming)

    result = validate_event_stateful(
        incoming,
        StateIndex(slot=parse_event(existing_raw), config=Snapshot()),
    )

    assert (result.disposition, result.audit_subtype, result.final_error_code) == (
        "duplicate",
        AuditSubtype.RAW_VARIANT,
        None,
    )


def test_second_primary_detail_uses_independent_primary_slot() -> None:
    parent = nok_result_dict()
    existing = parse_event(nok_detail_dict(parent))
    incoming = nok_detail_dict(parent)
    incoming["event_id"] = "b31cc4ef-1717-4124-bad8-c17abf916c70"
    incoming["event_ts"] = "2026-06-20T10:15:30.999Z"
    incoming["correlation"]["fact_key"] = compute_fact_key(incoming)

    result = validate_event_stateful(
        incoming,
        StateIndex(
            parent=parent,
            detail_set={
                "primary": existing,
                "details": {station_nok_detail_key(existing.to_dict())},
                "system_reserved": None,
            },
        ),
    )

    assert (result.disposition, result.final_error_code) == (
        "conflict",
        "DETAIL_KEY_CONFLICT",
    )


@pytest.mark.parametrize(
    ("start", "complete", "expected"),
    [
        (True, True, "complete_cycle"),
        (False, True, "partial_cycle_missing_start"),
        (True, False, "partial_cycle_missing_complete"),
        (False, False, "partial_cycle_missing_start_and_complete"),
    ],
)
def test_lifecycle_completeness_asserts_all_eight_fields(
    start: bool, complete: bool, expected: str
) -> None:
    event = parse_event(event_dict())
    output = derive_lifecycle(
        event,
        decision(),
        accepted_cycle_roles={"cycle_start": start, "cycle_complete": complete},
        accepted_parent=None,
    )

    assert output == LifecycleDerivedOutput(
        cycle_completeness=expected,
        traceability_status="unit_traceable",
        timeline_status="in_order" if start and complete else ("result_only" if not start and not complete else "out_of_order_preserved"),
        projection_eligible=True,
        parent_relation_status="not_applicable",
        detail_relation_status="not_applicable",
        late_status="not_evaluated_future_runtime",
        lifecycle_state=expected,
    )


def test_lifecycle_heartbeat_and_cycle_only_are_non_ambiguous() -> None:
    heartbeat = derive_lifecycle(
        parse_event(event_dict("station_heartbeat")),
        decision(),
        accepted_cycle_roles={},
        accepted_parent=None,
    )
    assert heartbeat.lifecycle_state == "diagnostic_only"
    assert heartbeat.traceability_status == "diagnostic_only"
    assert heartbeat.projection_eligible is False

    raw = event_dict()
    raw.pop("unit_id")
    raw.pop("dmc")
    cycle_only = derive_lifecycle(
        parse_event(raw),
        decision(),
        accepted_cycle_roles={"cycle_start": False, "cycle_complete": False},
        accepted_parent=None,
    )
    assert cycle_only.traceability_status == "cycle_only"


def test_heartbeat_unknown_requires_source_diagnostic_category() -> None:
    raw = event_dict("station_heartbeat")
    raw["result"] = "unknown"

    result = validate_event(raw)

    assert result.errors[0].code == "DIAGNOSTIC_CONTEXT_INVALID"


def test_lifecycle_preserves_timestamp_reversal_as_diagnostic() -> None:
    event = parse_event(event_dict())
    output = derive_lifecycle(
        event,
        decision(),
        accepted_cycle_roles={
            "cycle_start": {"event_ts": "2026-06-20T10:15:32Z"},
            "cycle_complete": {"event_ts": "2026-06-20T10:15:31Z"},
        },
        accepted_parent=None,
    )

    assert output.timeline_status == "timestamp_reversal"
    assert output.projection_eligible is True


def test_lifecycle_reject_duplicate_conflict_and_detail_relations() -> None:
    event = parse_event(event_dict())
    assert derive_lifecycle(event, decision("reject", "FIELD_FORBIDDEN"), {}, None).lifecycle_state == (
        "not_evaluated_validation_rejected"
    )
    assert derive_lifecycle(event, decision("duplicate"), {}, None).lifecycle_state == "duplicate"
    assert derive_lifecycle(event, decision("conflict"), {}, None).lifecycle_state == "conflict"

    detail = parse_event(nok_detail_dict())
    missing = derive_lifecycle(detail, decision("reject", "PARENT_NOT_FOUND"), {}, None)
    assert (missing.parent_relation_status, missing.detail_relation_status) == (
        "missing",
        "rejected_missing_parent",
    )


def test_projection_has_one_authoritative_result_and_detail_only_rows() -> None:
    result_event = parse_event(nok_result_dict())
    result_projection = projection_for(result_event, decision())
    assert result_projection.production_outcome == "nok"
    assert result_projection.authoritative is True
    assert result_projection.projection_eligible is True

    detail_projection = projection_for(parse_event(nok_detail_dict()), decision())
    assert detail_projection.production_outcome is None
    assert detail_projection.defect_detail is not None
    assert detail_projection.authoritative is False

    reserved = nok_detail_dict()
    reserved["nok_code"] = 30003
    reserved["nok_origin"] = "system_reserved"
    reserved["source"] = "system"
    reserved["actor"] = "system"
    reserved["correlation"]["detail_role"] = "system_reserved"
    reserved["correlation"]["fact_key"] = compute_fact_key(reserved)
    assert projection_for(parse_event(reserved, validate=False), decision()).defect_detail is None


def test_rejected_duplicate_and_conflict_never_project() -> None:
    event = parse_event(nok_result_dict())
    for disposition in ("reject", "duplicate", "conflict"):
        projection = projection_for(event, decision(disposition))
        assert projection.projection_eligible is False
        assert projection.production_outcome is None


def test_parse_event_raises_typed_error_with_deterministic_errors() -> None:
    raw = event_dict()
    raw["line_id"] = None

    with pytest.raises(StationEventValidationError) as raised:
        parse_event(raw)

    assert raised.value.errors[0].code == "FIELD_NULL_FORBIDDEN"
    assert raised.value.errors[0].path == "line_id"
    assert UUID(RESULT_EVENT_ID).version == 4
    assert datetime.now(timezone.utc).tzinfo is timezone.utc
