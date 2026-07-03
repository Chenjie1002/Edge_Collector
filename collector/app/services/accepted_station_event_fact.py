from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.services.station_event_adapter import AdapterDecision


@dataclass(frozen=True)
class AcceptedStationEventFact:
    line_id: str
    plc_id: str
    station_id: str
    station_type: str
    profile_id: str
    config_hash: str
    config_version: str
    event_type: str
    production_result: str | None
    unit_id: str | None
    dmc: str | None
    cycle_counter: int
    source_event_id: str
    event_ts: datetime
    fact_key: str
    content_fingerprint: str
    nok_code: int | None = None
    nok_origin: str | None = None
    nok_detail_code: int | None = None
    nok_detail_source_event_id: str | None = None
    nok_detail_evidence_fact_key: str | None = None

    @property
    def source_identity(self) -> tuple[str, str, str, str, str, str]:
        return (
            self.line_id,
            self.plc_id,
            self.station_id,
            self.config_hash,
            self.source_event_id,
            self.event_type,
        )


def build_accepted_station_event_fact(decision: AdapterDecision) -> AcceptedStationEventFact:
    if decision.disposition != "accepted":
        raise ValueError("accepted station-event fact requires accepted adapter decision")
    if decision.normalized_event is None or decision.fact_key is None or decision.content_fingerprint is None:
        raise ValueError("accepted adapter decision is missing canonical fact identity")

    event = decision.normalized_event
    correlation = event.get("correlation") or {}
    event_type = str(event["event_type"])
    production_result = None
    nok_code = None
    nok_origin = None
    nok_detail_code = None
    nok_detail_source_event_id = None
    nok_detail_evidence_fact_key = None

    if event_type == "station_result":
        production_result = _normalize_result(event.get("result"))
        if production_result == "nok":
            nok_code = _optional_int(event.get("nok_code"))
            nok_origin = _optional_str(event.get("nok_origin"))
    elif event_type == "station_nok":
        nok_code = _optional_int(event.get("nok_code"))
        nok_origin = _optional_str(event.get("nok_origin"))
        detail = getattr(decision.projection_metadata, "defect_detail", None)
        if detail is None:
            raise ValueError("station_nok production detail requires accepted defect detail projection")
        nok_detail_code = _optional_int(detail.get("nok_code"))
        nok_detail_source_event_id = _optional_str(correlation.get("source_event_id"))
        nok_detail_evidence_fact_key = _optional_str(correlation.get("parent_fact_key"))
        if nok_detail_code is None or not nok_detail_source_event_id or not nok_detail_evidence_fact_key:
            raise ValueError("station_nok production detail requires accepted upstream business evidence")
    elif event_type not in {"station_cycle_start", "station_cycle_complete"}:
        raise ValueError(f"event type is not production-visible: {event_type}")

    return AcceptedStationEventFact(
        line_id=str(event["line_id"]),
        plc_id=str(event["plc_id"]),
        station_id=str(event["station_id"]),
        station_type=str(event["station_type"]),
        profile_id=str(event["profile_id"]),
        config_hash=str(event["config_hash"]),
        config_version=str(event["config_version"]),
        event_type=event_type,
        production_result=production_result,
        unit_id=_optional_str(event.get("unit_id")),
        dmc=_optional_str(event.get("dmc")),
        cycle_counter=int(event["cycle_counter"]),
        source_event_id=str(correlation["source_event_id"]),
        event_ts=_parse_event_ts(event["event_ts"]),
        fact_key=decision.fact_key,
        content_fingerprint=decision.content_fingerprint,
        nok_code=nok_code,
        nok_origin=nok_origin,
        nok_detail_code=nok_detail_code,
        nok_detail_source_event_id=nok_detail_source_event_id,
        nok_detail_evidence_fact_key=nok_detail_evidence_fact_key,
    )


def _normalize_result(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).lower()
    if text == "ok":
        return "ok"
    if text == "nok":
        return "nok"
    if text == "skip":
        return "skip"
    if text in {"not_applicable", "not applicable"}:
        return "not_applicable"
    return text


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text or None


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    number = int(value)
    return number if number else None


def _parse_event_ts(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
