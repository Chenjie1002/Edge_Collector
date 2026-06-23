from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .constants import AuditSubtype
from .errors import ValidationError


def freeze_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): freeze_json(item) for key, item in value.items()})
    if isinstance(value, list | tuple):
        return tuple(freeze_json(item) for item in value)
    return value


def thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw_json(item) for item in value]
    return value


@dataclass(frozen=True)
class StationEvent:
    schema_version: str
    event_id: str
    event_type: str
    event_ts: str
    line_id: str
    plc_id: str
    station_id: str
    station_type: str
    config_version: str
    config_hash: str
    source: str
    actor: str
    correlation: Mapping[str, Any]
    plc_boot_id: str | None = None
    profile_id: str | None = None
    cycle_id: str | None = None
    cycle_counter: int | None = None
    unit_id: str | None = None
    dmc: str | None = None
    result: str | None = None
    nok_code: int | None = None
    nok_origin: str | None = None
    payload: Mapping[str, Any] | None = None
    raw_payload: Mapping[str, Any] | None = None
    diagnostic_context: Mapping[str, Any] | None = None
    observed_at: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "correlation", freeze_json(self.correlation))
        for name in ("payload", "raw_payload", "diagnostic_context"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, freeze_json(value))

    def to_dict(self) -> dict[str, Any]:
        data = {
            field_.name: thaw_json(getattr(self, field_.name))
            for field_ in self.__dataclass_fields__.values()
            if getattr(self, field_.name) is not None
        }
        return data


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[ValidationError, ...] = ()

    @property
    def is_valid(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class LifecycleDerivedOutput:
    cycle_completeness: str
    traceability_status: str
    timeline_status: str
    projection_eligible: bool
    parent_relation_status: str
    detail_relation_status: str
    late_status: str
    lifecycle_state: str


@dataclass(frozen=True)
class ValidationDecision:
    disposition: str
    final_error_code: str | None = None
    matched_key_type: str | None = None
    matched_key_value: Any = None
    existing_event_id: str | None = None
    existing_content_fingerprint: str | None = None
    incoming_content_fingerprint: str | None = None
    existing_raw_evidence_fingerprint: str | None = None
    incoming_raw_evidence_fingerprint: str | None = None
    additional_matched_keys: tuple[Any, ...] = ()
    audit_subtype: AuditSubtype = AuditSubtype.NONE
    lifecycle: LifecycleDerivedOutput | None = None


@dataclass(frozen=True)
class Projection:
    projection_eligible: bool
    authoritative: bool
    production_result_key: tuple[Any, ...] | None = None
    production_outcome: str | None = None
    defect_detail: Mapping[str, Any] | None = None
    compatibility_projection: Mapping[str, Any] | None = None
