from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any

from .models import LifecycleDerivedOutput, StationEvent, ValidationDecision


LATE = "not_evaluated_future_runtime"


def derive_lifecycle(
    event: StationEvent,
    validation_decision: ValidationDecision,
    accepted_cycle_roles: Mapping[str, Any],
    accepted_parent: Any,
) -> LifecycleDerivedOutput:
    if validation_decision.disposition == "reject":
        if event.event_type == "station_nok" and validation_decision.final_error_code == "PARENT_NOT_FOUND":
            return _output(
                "detail_rejected_missing_parent",
                parent="missing",
                detail="rejected_missing_parent",
            )
        if event.event_type == "station_nok" and validation_decision.final_error_code == "PARENT_EVENT_INVALID":
            return _output(
                "detail_rejected_parent_ok",
                parent="parent_ok_invalid",
                detail="rejected_parent_ok",
            )
        return _output("not_evaluated_validation_rejected")
    if validation_decision.disposition == "duplicate":
        detail = "duplicate" if event.event_type == "station_nok" else "not_applicable"
        return _output("duplicate", detail=detail)
    if validation_decision.disposition == "conflict":
        detail = "conflict" if event.event_type == "station_nok" else "not_applicable"
        return _output("conflict", detail=detail)
    if event.event_type == "station_heartbeat":
        return LifecycleDerivedOutput(
            cycle_completeness="not_applicable",
            traceability_status="diagnostic_only",
            timeline_status="diagnostic_only",
            projection_eligible=False,
            parent_relation_status="not_applicable",
            detail_relation_status="not_applicable",
            late_status=LATE,
            lifecycle_state="diagnostic_only",
        )
    if event.event_type == "station_nok":
        return LifecycleDerivedOutput(
            cycle_completeness="not_applicable",
            traceability_status="unit_traceable" if event.unit_id or event.dmc else "cycle_only",
            timeline_status="not_applicable",
            projection_eligible=False,
            parent_relation_status="attached",
            detail_relation_status="attached",
            late_status=LATE,
            lifecycle_state="detail_attached",
        )

    start = bool(accepted_cycle_roles.get("cycle_start"))
    complete = bool(accepted_cycle_roles.get("cycle_complete"))
    if start and complete:
        completeness = "complete_cycle"
        timeline = "in_order"
    elif not start and complete:
        completeness = "partial_cycle_missing_start"
        timeline = "out_of_order_preserved"
    elif start and not complete:
        completeness = "partial_cycle_missing_complete"
        timeline = "out_of_order_preserved"
    else:
        completeness = "partial_cycle_missing_start_and_complete"
        timeline = "result_only" if event.event_type == "station_result" else "out_of_order_preserved"
    if _timestamp_reversal(event, accepted_cycle_roles):
        timeline = "timestamp_reversal"
    return LifecycleDerivedOutput(
        cycle_completeness=completeness,
        traceability_status="unit_traceable" if event.unit_id or event.dmc else "cycle_only",
        timeline_status=timeline,
        projection_eligible=event.event_type == "station_result",
        parent_relation_status="not_applicable",
        detail_relation_status="not_applicable",
        late_status=LATE,
        lifecycle_state=completeness,
    )


def _timestamp_reversal(
    event: StationEvent,
    accepted_cycle_roles: Mapping[str, Any],
) -> bool:
    ordered_values = [
        accepted_cycle_roles.get("cycle_start"),
        accepted_cycle_roles.get("cycle_complete"),
        {"event_ts": event.event_ts} if event.event_type == "station_result" else None,
    ]
    timestamps = []
    for value in ordered_values:
        if not isinstance(value, Mapping):
            continue
        timestamp = value.get("event_ts")
        if isinstance(timestamp, str):
            timestamps.append(datetime.fromisoformat(timestamp.replace("Z", "+00:00")))
    return any(left > right for left, right in zip(timestamps, timestamps[1:]))


def _output(
    state: str,
    *,
    parent: str = "not_applicable",
    detail: str = "not_applicable",
) -> LifecycleDerivedOutput:
    return LifecycleDerivedOutput(
        cycle_completeness="not_applicable",
        traceability_status="not_applicable",
        timeline_status="not_applicable",
        projection_eligible=False,
        parent_relation_status=parent,
        detail_relation_status=detail,
        late_status=LATE,
        lifecycle_state=state,
    )
