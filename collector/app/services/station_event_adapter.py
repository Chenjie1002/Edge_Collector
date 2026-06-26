from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Any

from common.station_event import (
    AuditSubtype,
    LifecycleDerivedOutput,
    Projection,
    StationEvent,
    canonical_json_bytes,
    compute_content_fingerprint,
    compute_fact_key,
    compute_raw_evidence_fingerprint,
    cycle_role_key,
    derive_lifecycle,
    parse_event,
    production_result_key,
    projection_for,
    station_nok_detail_key,
    validate_event,
    validate_event_stateful,
)

from .resolved_config_registry import ConfigNotFound, ResolvedConfigSnapshot


EVENT_ROLES = {
    "station_cycle_start": "cycle_start",
    "station_cycle_complete": "cycle_complete",
    "station_result": "production_result",
    "station_nok": "nok_detail",
    "station_heartbeat": "heartbeat",
}
DIAGNOSTIC_DISPOSITIONS = {"deferred", "quarantined"}
RAW_POLICIES_ALLOWING_NORMALIZED_ONLY = {"raw_not_provided"}
RAW_POLICIES_REQUIRING_EVIDENCE = {"raw_required", "raw_capable"}


@dataclass(frozen=True)
class AdapterDecision:
    disposition: str
    final_error_code: str | None = None
    normalized_event: dict[str, Any] | None = None
    canonical_bytes: bytes | None = None
    fact_key: str | None = None
    content_fingerprint: str | None = None
    raw_evidence_fingerprint: str | None = None
    lifecycle: LifecycleDerivedOutput | None = None
    projection_metadata: Projection | None = None
    audit_subtype: AuditSubtype = AuditSubtype.NONE
    state_index: "OfflineAdapterStateIndex | None" = None


@dataclass(frozen=True)
class _Record:
    record: StationEvent
    disposition: str = "accepted"
    accepted: bool = True
    status: str = "found"


class OfflineAdapterStateIndex:
    def __init__(
        self,
        registry: Any,
        records: tuple[_Record, ...] = (),
    ) -> None:
        self._registry = registry
        self._records = records

    def with_record(self, decision: AdapterDecision) -> "OfflineAdapterStateIndex":
        if decision.disposition != "accepted" or decision.normalized_event is None:
            return self
        return OfflineAdapterStateIndex(
            self._registry,
            self._records + (_Record(parse_event(decision.normalized_event, validate=False)),),
        )

    def lookup_resolved_config(self, config_hash: str) -> Any:
        return self._registry.lookup_resolved_config(config_hash)

    def lookup_by_event_id(self, key: str) -> _Record | None:
        return next((record for record in self._records if record.record.event_id == key), None)

    def lookup_by_fact_key(self, key: str) -> _Record | None:
        return next(
            (
                record
                for record in self._records
                if record.record.correlation.get("fact_key") == key
            ),
            None,
        )

    def lookup_cycle_role(self, key: tuple[Any, ...]) -> _Record | None:
        return next(
            (
                record
                for record in self._records
                if record.record.event_type not in {"station_nok", "station_heartbeat"}
                and cycle_role_key(record.record.to_dict()) == key
            ),
            None,
        )

    def lookup_parent_result(self, event_id: str, fact_key: str) -> _Record | None:
        return next(
            (
                record
                for record in self._records
                if record.record.event_id == event_id
                and record.record.correlation.get("fact_key") == fact_key
            ),
            None,
        )

    def lookup_upstream_evidence(self, evidence: Mapping[str, Any]) -> _Record | None:
        return next(
            (
                record
                for record in self._records
                if record.record.event_id == evidence.get("parent_event_id")
                and record.record.correlation.get("fact_key") == evidence.get("parent_fact_key")
            ),
            None,
        )

    def lookup_detail_key(self, key: tuple[Any, ...]) -> _Record | None:
        return next(
            (
                record
                for record in self._records
                if record.record.event_type == "station_nok"
                and station_nok_detail_key(record.record.to_dict()) == key
            ),
            None,
        )

    def lookup_detail_set(self, parent_fact_key: str) -> dict[str, Any]:
        details: dict[str, Any] = {
            "primary": None,
            "system_reserved": None,
            "details": set(),
        }
        for record in self._records:
            raw = record.record.to_dict()
            if raw.get("event_type") != "station_nok":
                continue
            correlation = raw["correlation"]
            if correlation.get("parent_fact_key") != parent_fact_key:
                continue
            if correlation.get("detail_role") == "primary":
                details["primary"] = record.record
            elif correlation.get("detail_role") == "system_reserved":
                details["system_reserved"] = record.record
            else:
                details["details"].add(station_nok_detail_key(raw))
        return details


def adapt_source_payload(
    source_payload: Mapping[str, Any],
    registry: Any,
    state_index: OfflineAdapterStateIndex | None = None,
) -> AdapterDecision:
    diagnostic = source_payload.get("diagnostic_decision")
    if diagnostic in DIAGNOSTIC_DISPOSITIONS:
        return AdapterDecision(disposition=str(diagnostic), final_error_code=str(diagnostic).upper())

    config_hash = str(source_payload.get("config_hash", ""))
    resolved = registry.lookup_resolved_config(config_hash)
    if isinstance(resolved, ConfigNotFound) or getattr(resolved, "status", None) == "not_found":
        return _reject("CONFIG_NOT_FOUND")
    if not isinstance(resolved, ResolvedConfigSnapshot):
        return _reject("CONFIG_HASH_MISMATCH")
    if resolved.config_hash != config_hash:
        return _reject("CONFIG_HASH_MISMATCH")
    if not resolved.content_hash_matches():
        return _reject("CONFIG_HASH_MISMATCH")

    station = _station_for(resolved, str(source_payload.get("station_id", "")))
    if station is None:
        return _reject("CONFIG_NOT_FOUND")
    lineage_error = _adapter_lineage_error(source_payload, station)
    if lineage_error is not None:
        return _reject(lineage_error)
    raw_error = _raw_authority_error(source_payload, station)
    if raw_error is not None:
        return _reject(raw_error)

    event = _build_event(source_payload, resolved, station)
    event["correlation"]["fact_key"] = compute_fact_key(event)
    _business_identity_key(event)
    canonical = canonical_json_bytes(event)
    content = compute_content_fingerprint(event)
    raw_fingerprint = compute_raw_evidence_fingerprint(event.get("raw_payload"))

    stateless = validate_event(event, resolved)
    if not stateless.is_valid:
        return _reject(
            stateless.errors[0].code,
            event=event,
            canonical=canonical,
            fact_key=event["correlation"]["fact_key"],
            content=content,
            raw_fingerprint=raw_fingerprint,
        )

    index = state_index or OfflineAdapterStateIndex(registry)
    shared = validate_event_stateful(event, index)
    station_event = parse_event(event, validate=False)
    lifecycle = derive_lifecycle(station_event, shared, _accepted_cycle_roles(index, event), None)
    if shared.disposition == "accept":
        projection = projection_for(station_event, shared)
        decision = AdapterDecision(
            disposition="accepted",
            normalized_event=event,
            canonical_bytes=canonical,
            fact_key=event["correlation"]["fact_key"],
            content_fingerprint=content,
            raw_evidence_fingerprint=raw_fingerprint,
            lifecycle=lifecycle,
            projection_metadata=projection,
            audit_subtype=shared.audit_subtype,
        )
        return replace(decision, state_index=index.with_record(decision))
    if shared.disposition in {"duplicate", "conflict"}:
        return AdapterDecision(
            disposition=shared.disposition,
            final_error_code=shared.final_error_code,
            normalized_event=event,
            canonical_bytes=canonical,
            fact_key=event["correlation"]["fact_key"],
            content_fingerprint=content,
            raw_evidence_fingerprint=raw_fingerprint,
            lifecycle=lifecycle,
            projection_metadata=None,
            audit_subtype=shared.audit_subtype,
            state_index=index,
        )
    return _reject(
        shared.final_error_code,
        event=event,
        canonical=canonical,
        fact_key=event["correlation"]["fact_key"],
        content=content,
        raw_fingerprint=raw_fingerprint,
        state_index=index,
    )


def _reject(
    code: str | None,
    *,
    event: dict[str, Any] | None = None,
    canonical: bytes | None = None,
    fact_key: str | None = None,
    content: str | None = None,
    raw_fingerprint: str | None = None,
    state_index: OfflineAdapterStateIndex | None = None,
) -> AdapterDecision:
    return AdapterDecision(
        disposition="rejected",
        final_error_code=code,
        normalized_event=event,
        canonical_bytes=canonical,
        fact_key=fact_key,
        content_fingerprint=content,
        raw_evidence_fingerprint=raw_fingerprint,
        projection_metadata=None,
        state_index=state_index,
    )


def _station_for(resolved: Any, station_id: str) -> Any:
    station_for = getattr(resolved, "station_for", None)
    if callable(station_for):
        return station_for(station_id)
    return next(
        (station for station in getattr(resolved, "stations", ()) if station.station_id == station_id),
        None,
    )


def _adapter_lineage_error(source_payload: Mapping[str, Any], station: Any) -> str | None:
    if source_payload.get("mapping_id") != station.mapping_id:
        return "EVENT_LINEAGE_INVALID"
    if source_payload.get("payload_template") != station.payload_template:
        return "EVENT_LINEAGE_INVALID"
    if "profile_id" in source_payload and source_payload["profile_id"] != station.cycle_profile:
        return "EVENT_LINEAGE_INVALID"
    if "station_type" in source_payload and source_payload["station_type"] != station.station_type:
        return "EVENT_LINEAGE_INVALID"
    return None


def _raw_authority_error(source_payload: Mapping[str, Any], station: Any) -> str | None:
    raw_present = "raw_payload" in source_payload
    normalized_present = "payload" in source_payload
    if raw_present and not normalized_present:
        return "RAW_ONLY_UNSUPPORTED"
    if not raw_present and station.raw_policy in RAW_POLICIES_REQUIRING_EVIDENCE:
        return "RAW_EVIDENCE_MISSING"
    if not raw_present and station.raw_policy not in RAW_POLICIES_ALLOWING_NORMALIZED_ONLY:
        return "RAW_EVIDENCE_MISSING"
    return None


def _build_event(
    source_payload: Mapping[str, Any],
    resolved: Any,
    station: Any,
) -> dict[str, Any]:
    event_type = str(source_payload["event_type"])
    event = {
        "schema_version": "1.0",
        "event_id": source_payload["event_id"],
        "event_type": event_type,
        "event_ts": source_payload["event_ts"],
        "line_id": resolved.line_id,
        "plc_id": station.plc_id,
        "station_id": station.station_id,
        "station_type": station.station_type,
        "config_version": resolved.config_version,
        "config_hash": resolved.config_hash,
        "plc_boot_id": source_payload["plc_boot_id"],
        "source": source_payload.get("source", "plc"),
        "actor": source_payload.get("actor", "plc"),
        "correlation": {
            "source_event_id": source_payload["source_event_id"],
            "fact_key": "pending",
            "event_role": EVENT_ROLES[event_type],
            "mapping_id": source_payload["mapping_id"],
        },
    }
    if "observed_at" in source_payload:
        event["observed_at"] = source_payload["observed_at"]
    if event_type != "station_heartbeat":
        event.update(
            profile_id=station.cycle_profile,
            cycle_counter=source_payload["cycle_counter"],
            cycle_id=(
                f"{resolved.line_id}/{station.plc_id}/{station.station_id}/"
                f"{source_payload['plc_boot_id']}/{source_payload['cycle_counter']}"
            ),
        )
        for field in ("unit_id", "dmc", "result", "nok_code", "nok_origin"):
            if field in source_payload:
                event[field] = source_payload[field]
    else:
        event["diagnostic_context"] = dict(source_payload["diagnostic_context"])
    if "payload" in source_payload:
        event["payload"] = dict(source_payload["payload"])
        event["correlation"]["payload_template"] = source_payload["payload_template"]
    if "raw_payload" in source_payload:
        event["raw_payload"] = dict(source_payload["raw_payload"])
        event["correlation"]["payload_template"] = source_payload["payload_template"]
        event["correlation"]["raw_encoding"] = "json"
    if event_type == "station_nok":
        event["correlation"].update(
            parent_event_id=source_payload["parent_event_id"],
            parent_fact_key=source_payload["parent_fact_key"],
            detail_role=source_payload["detail_role"],
        )
        if "upstream_evidence" in source_payload:
            event["correlation"]["upstream_evidence"] = dict(source_payload["upstream_evidence"])
    return event


def _accepted_cycle_roles(index: OfflineAdapterStateIndex, event: Mapping[str, Any]) -> dict[str, Any]:
    roles = {}
    for role in ("cycle_start", "cycle_complete"):
        key = (
            event["line_id"],
            event["plc_id"],
            event["station_id"],
            event["plc_boot_id"],
            event.get("cycle_counter"),
            role,
        )
        found = index.lookup_cycle_role(key)
        if found is not None:
            roles[role] = found.record.to_dict()
    return roles


def _business_identity_key(event: Mapping[str, Any]) -> tuple[Any, ...] | str | None:
    if event["event_type"] in {"station_cycle_start", "station_cycle_complete"}:
        return cycle_role_key(event)
    if event["event_type"] == "station_result":
        return production_result_key(event)
    if event["event_type"] == "station_nok":
        return station_nok_detail_key(event)
    return None
