from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from collector.app.services.resolved_config_registry import (
    InMemoryResolvedConfigRegistry,
    ResolvedConfigSnapshot,
    ResolvedStationSnapshot,
    RouteEdgeSnapshot,
    RouteGraphSnapshot,
)
from collector.app.services.station_event_adapter import adapt_source_payload
from common.station_event import AuditSubtype


CONFIG_HASH = "50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1"
OLD_CONFIG_HASH = "60b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1"
CURRENT_CONFIG_HASH = "70b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1"
BOOT_ID = "01J10C2SZM4T2R8K6V2YDR45VH"


def decoder(raw_payload, _event):
    return dict(raw_payload)


def snapshot(
    *,
    config_hash: str = CONFIG_HASH,
    mapping_id: str = "ws02_result",
    payload_template: str = "screw_result_v1",
    station_type: str = "screw",
    cycle_profile: str = "normal_screwdriving",
    raw_policy: str = "raw_not_provided",
    raw_decoder=decoder,
    route_from: str = "WS01",
    line_id: str = "LINE-01",
) -> ResolvedConfigSnapshot:
    return ResolvedConfigSnapshot(
        config_hash=config_hash,
        config_version="2026.06.20-1",
        line_id=line_id,
        stations=(
            ResolvedStationSnapshot(
                station_id="WS01",
                plc_id="PLC-01",
                station_type=station_type,
                cycle_profile=cycle_profile,
                mapping_id="ws01_result",
                payload_template=payload_template,
                raw_policy=raw_policy,
                decoder=raw_decoder,
            ),
            ResolvedStationSnapshot(
                station_id="WS02",
                plc_id="PLC-01",
                station_type=station_type,
                cycle_profile=cycle_profile,
                mapping_id=mapping_id,
                payload_template=payload_template,
                raw_policy=raw_policy,
                decoder=raw_decoder,
            ),
        ),
        route_graph=RouteGraphSnapshot(
            edges=(RouteEdgeSnapshot(from_station_id=route_from, to_station_id="WS02"),)
        ),
    )


def registry(*snapshots: ResolvedConfigSnapshot) -> InMemoryResolvedConfigRegistry:
    return InMemoryResolvedConfigRegistry({item.config_hash: item for item in snapshots})


def source(
    event_type: str = "station_result",
    *,
    result: str | None = "ok",
    config_hash: str = CONFIG_HASH,
    mapping_id: str = "ws02_result",
    payload_template: str = "screw_result_v1",
    raw_payload=None,
    normalized_payload=None,
    event_id: str | None = None,
    source_event_id: str | None = None,
    cycle_counter: int = 42,
    station_id: str = "WS02",
    parent=None,
    detail_role: str = "primary",
    nok_code: int = 20001,
    nok_origin: str = "plc",
    upstream_evidence=None,
    diagnostic_decision: str | None = None,
    profile_id: str | None = None,
    station_type: str | None = None,
) -> dict:
    payload = {
        "config_hash": config_hash,
        "event_id": event_id or str(uuid4()),
        "event_type": event_type,
        "event_ts": "2026-06-20T10:15:30.123Z",
        "observed_at": "2026-06-20T10:15:31.000Z",
        "station_id": station_id,
        "mapping_id": mapping_id,
        "payload_template": payload_template,
        "source_event_id": source_event_id or f"PLC-01:{station_id}:{cycle_counter}:{event_type}",
        "plc_boot_id": BOOT_ID,
        "cycle_counter": cycle_counter,
        "unit_id": "UNIT-000042",
        "dmc": "DMC-000042",
        "source": "plc",
        "actor": "plc",
    }
    if result is not None:
        payload["result"] = result
    if normalized_payload is not None:
        payload["payload"] = normalized_payload
    if raw_payload is not None:
        payload["raw_payload"] = raw_payload
    if event_type in {"station_cycle_start", "station_cycle_complete"}:
        payload.pop("result", None)
    if event_type == "station_heartbeat":
        for key in ("result", "cycle_counter", "unit_id", "dmc"):
            payload.pop(key, None)
        payload["diagnostic_context"] = {
            "category": "heartbeat",
            "reason_code": "periodic_heartbeat",
        }
    if event_type == "station_nok":
        payload.pop("result", None)
        payload["parent_event_id"] = (
            parent.normalized_event["event_id"]
            if parent is not None
            else "550e8400-e29b-41d4-a716-446655440000"
        )
        payload["parent_fact_key"] = parent.fact_key if parent is not None else "sha256:" + "1" * 64
        payload["detail_role"] = detail_role
        payload["nok_code"] = nok_code
        payload["nok_origin"] = nok_origin
        if upstream_evidence is not None:
            payload["upstream_evidence"] = upstream_evidence
    elif result == "nok":
        payload["nok_code"] = nok_code
        payload["nok_origin"] = nok_origin
    if diagnostic_decision is not None:
        payload["diagnostic_decision"] = diagnostic_decision
    if profile_id is not None:
        payload["profile_id"] = profile_id
    if station_type is not None:
        payload["station_type"] = station_type
    return payload


def assert_no_projection(decision) -> None:
    assert decision.projection_metadata is None
    assert decision.lifecycle is None or decision.disposition in {"duplicate", "conflict"}


@pytest.mark.parametrize(
    ("event_type", "result"),
    [
        ("station_cycle_start", None),
        ("station_cycle_complete", None),
        ("station_result", "ok"),
        ("station_heartbeat", None),
    ],
)
def test_nominal_station_events_are_accepted_offline(event_type: str, result: str | None) -> None:
    decision = adapt_source_payload(source(event_type, result=result), registry(snapshot()))

    assert decision.disposition == "accepted"
    assert decision.final_error_code is None
    assert decision.normalized_event["event_type"] == event_type
    assert decision.canonical_bytes
    assert decision.fact_key == decision.normalized_event["correlation"]["fact_key"]
    if event_type == "station_result":
        assert decision.projection_metadata.production_outcome == "ok"


def test_nominal_nok_result_and_primary_detail_are_accepted_without_projection_leak() -> None:
    reg = registry(snapshot())
    parent = adapt_source_payload(source(result="nok"), reg)
    detail = adapt_source_payload(source("station_nok", result=None, parent=parent), reg, parent.state_index)

    assert parent.disposition == "accepted"
    assert parent.projection_metadata.production_outcome == "nok"
    assert detail.disposition == "accepted"
    assert detail.projection_metadata.defect_detail["nok_code"] == 20001


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        (source(config_hash="f" * 64), "CONFIG_NOT_FOUND"),
        (source(mapping_id="wrong_mapping"), "EVENT_LINEAGE_INVALID"),
        (source(payload_template="wrong_template"), "EVENT_LINEAGE_INVALID"),
    ],
)
def test_lineage_identity_failures_reject_without_projection(payload: dict, expected: str) -> None:
    decision = adapt_source_payload(payload, registry(snapshot()))

    assert (decision.disposition, decision.final_error_code) == ("rejected", expected)
    assert_no_projection(decision)


@pytest.mark.parametrize(
    ("snap", "payload", "expected"),
    [
        (snapshot(), source(profile_id="wrong_profile"), "EVENT_LINEAGE_INVALID"),
        (snapshot(), source(station_type="inspection"), "EVENT_LINEAGE_INVALID"),
        (snapshot(route_from="WS99"), source("station_nok", result=None, parent=None), "PARENT_NOT_FOUND"),
    ],
)
def test_snapshot_profile_station_and_route_fail_closed(snap, payload, expected: str) -> None:
    if payload["event_type"] == "station_nok":
        reg = registry(snapshot(route_from="WS01"))
        parent = adapt_source_payload(source(result="nok"), reg)
        payload = source("station_nok", result=None, parent=parent)
        reg = registry(snap)
    else:
        reg = registry(snap)

    decision = adapt_source_payload(payload, reg)

    assert decision.disposition == "rejected"
    assert decision.final_error_code == expected
    assert_no_projection(decision)


def test_direct_predecessor_mismatch_rejects_system_reserved_detail_without_adapter_synthesis() -> None:
    reg = registry(snapshot())
    parent = adapt_source_payload(source(result="skip"), reg)
    evidence_parent = adapt_source_payload(
        source(result="nok", station_id="WS01", mapping_id="ws01_result"),
        reg,
    )
    upstream = {
        "evidence_type": "canonical_station_result",
        "source_event_id": evidence_parent.normalized_event["correlation"]["source_event_id"],
        "parent_event_id": evidence_parent.normalized_event["event_id"],
        "parent_fact_key": evidence_parent.fact_key,
        "upstream_station_id": "WS99",
        "upstream_plc_id": "PLC-01",
        "upstream_plc_boot_id": BOOT_ID,
        "upstream_event_type": "station_result",
        "upstream_result": "nok",
        "upstream_nok_code": 20001,
        "upstream_config_hash": CONFIG_HASH,
    }

    decision = adapt_source_payload(
        source(
            "station_nok",
            result=None,
            parent=parent,
            nok_code=30003,
            nok_origin="system_reserved",
            detail_role="system_reserved",
            upstream_evidence=upstream,
        )
        | {"source": "system", "actor": "system"},
        reg,
        parent.state_index.with_record(evidence_parent),
    )

    assert (decision.disposition, decision.final_error_code) == ("rejected", "UPSTREAM_EVIDENCE_INVALID")
    assert decision.projection_metadata is None


def test_config_hash_mismatch_from_lookup_record_is_distinguishable() -> None:
    class MismatchRegistry(InMemoryResolvedConfigRegistry):
        def lookup_resolved_config(self, _config_hash):
            return snapshot(config_hash="0" * 64)

    decision = adapt_source_payload(source(), MismatchRegistry({}))

    assert (decision.disposition, decision.final_error_code) == ("rejected", "CONFIG_HASH_MISMATCH")
    assert_no_projection(decision)


@pytest.mark.parametrize(
    ("snap", "payload", "expected"),
    [
        (snapshot(raw_policy="raw_required"), source(normalized_payload=None, raw_payload={"torque": 4.8}), "RAW_ONLY_UNSUPPORTED"),
        (snapshot(raw_policy="raw_required", raw_decoder=None), source(normalized_payload={"torque": 4.8}, raw_payload={"torque": 4.8}), "RAW_PARSE_ERROR"),
        (snapshot(raw_policy="raw_required", raw_decoder=lambda _raw, _event: (_ for _ in ()).throw(ValueError("bad"))), source(normalized_payload={"torque": 4.8}, raw_payload={"torque": 4.8}), "RAW_PARSE_ERROR"),
        (snapshot(raw_policy="raw_required"), source(normalized_payload={"torque": 4.8}, raw_payload={"torque": 4.9}), "RAW_NORMALIZED_MISMATCH"),
        (snapshot(raw_policy="raw_required"), source(normalized_payload={"torque": 4.8}), "RAW_EVIDENCE_MISSING"),
        (snapshot(raw_policy="raw_capable"), source(normalized_payload={"torque": 4.8}), "RAW_EVIDENCE_MISSING"),
        (snapshot(raw_policy="raw_required"), source(normalized_payload={"torque": 4.8}, raw_payload={"image_base64": "not-empty"}), "RAW_CONTENT_FORBIDDEN"),
    ],
)
def test_raw_authority_negative_cases_fail_closed_without_projection(snap, payload, expected: str) -> None:
    decision = adapt_source_payload(payload, registry(snap))

    assert (decision.disposition, decision.final_error_code) == ("rejected", expected)
    assert_no_projection(decision)


def test_raw_plus_normalized_match_and_declared_no_raw_normalized_only_can_validate() -> None:
    with_raw = adapt_source_payload(
        source(normalized_payload={"torque": 4.8}, raw_payload={"torque": 4.8}),
        registry(snapshot(raw_policy="raw_required")),
    )
    normalized_only = adapt_source_payload(
        source(normalized_payload={"torque": 4.8}),
        registry(snapshot(raw_policy="raw_not_provided")),
    )

    assert with_raw.disposition == "accepted"
    assert with_raw.raw_evidence_fingerprint is not None
    assert normalized_only.disposition == "accepted"
    assert normalized_only.raw_evidence_fingerprint is None


@pytest.mark.parametrize("diagnostic_decision", ["deferred", "quarantined"])
def test_diagnostic_deferred_and_quarantined_do_not_project(diagnostic_decision: str) -> None:
    decision = adapt_source_payload(
        source(diagnostic_decision=diagnostic_decision),
        registry(snapshot()),
    )

    assert decision.disposition == diagnostic_decision
    assert decision.normalized_event is None
    assert decision.projection_metadata is None


def test_duplicate_conflict_and_raw_variant_do_not_create_new_projection() -> None:
    def raw_variant_decoder(raw_payload, _event):
        return {"torque": raw_payload["torque"]}

    reg = registry(snapshot(raw_policy="raw_required", raw_decoder=raw_variant_decoder))
    accepted = adapt_source_payload(
        source(normalized_payload={"torque": 4.8}, raw_payload={"torque": 4.8}),
        reg,
    )
    duplicate = adapt_source_payload(
        source(
            event_id=str(uuid4()),
            normalized_payload={"torque": 4.8},
            raw_payload={"torque": 4.8},
        ),
        reg,
        accepted.state_index,
    )
    raw_variant = adapt_source_payload(
        source(
            event_id=str(uuid4()),
            normalized_payload={"torque": 4.8},
            raw_payload={"torque": 4.8, "note": "same normalized"},
        ),
        reg,
        accepted.state_index,
    )
    conflict = adapt_source_payload(
        source(event_id=str(uuid4()), result="nok", normalized_payload={"torque": 4.8}, raw_payload={"torque": 4.8}),
        reg,
        accepted.state_index,
    )

    assert duplicate.disposition == "duplicate"
    assert duplicate.audit_subtype == AuditSubtype.NONE
    assert duplicate.projection_metadata is None
    assert raw_variant.disposition == "duplicate"
    assert raw_variant.audit_subtype == AuditSubtype.RAW_VARIANT
    assert raw_variant.projection_metadata is None
    assert conflict.disposition == "conflict"
    assert conflict.projection_metadata is None


def test_rejected_nok_detail_does_not_leak_defect_projection() -> None:
    decision = adapt_source_payload(source("station_nok", result=None, parent=SimpleNamespace(normalized_event={"event_id": str(uuid4())}, fact_key="sha256:" + "1" * 64)), registry(snapshot()))

    assert decision.disposition == "rejected"
    assert decision.projection_metadata is None


def test_historical_config_uses_old_snapshot_and_never_falls_back_to_current() -> None:
    old = snapshot(config_hash=OLD_CONFIG_HASH, station_type="historical_screw")
    current = snapshot(config_hash=CURRENT_CONFIG_HASH, station_type="current_screw")
    payload = source(config_hash=OLD_CONFIG_HASH)

    decision = adapt_source_payload(payload, registry(old, current))
    missing_old = adapt_source_payload(payload, registry(current))

    assert decision.disposition == "accepted"
    assert decision.normalized_event["station_type"] == "historical_screw"
    assert (missing_old.disposition, missing_old.final_error_code) == ("rejected", "CONFIG_NOT_FOUND")
