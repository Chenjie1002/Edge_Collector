from __future__ import annotations

from .fingerprint import production_result_key, station_nok_detail_key
from .models import Projection, StationEvent, ValidationDecision


def projection_for(event: StationEvent, decision: ValidationDecision) -> Projection:
    if decision.disposition != "accept":
        return Projection(projection_eligible=False, authoritative=False)
    raw = event.to_dict()
    if event.event_type == "station_result":
        return Projection(
            projection_eligible=True,
            authoritative=True,
            production_result_key=production_result_key(raw),
            production_outcome=event.result,
            compatibility_projection={"result": event.result, "authoritative": False},
        )
    if event.event_type == "station_nok":
        if event.nok_code == 30003 or event.nok_origin == "system_reserved":
            return Projection(projection_eligible=False, authoritative=False)
        return Projection(
            projection_eligible=False,
            authoritative=False,
            defect_detail={
                "station_nok_detail_key": station_nok_detail_key(raw),
                "nok_code": event.nok_code,
                "nok_origin": event.nok_origin,
            },
        )
    return Projection(projection_eligible=False, authoritative=False)
