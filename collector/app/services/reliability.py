from __future__ import annotations

from enum import Enum
import uuid


class CounterDecision(str, Enum):
    ACCEPT = "ACCEPT"
    DUPLICATE = "DUPLICATE"
    RESET = "RESET"


def validate_plc_boot_id(value: object) -> str:
    boot_id = str(value or "").strip()
    if not boot_id or boot_id == "UNKNOWN" or boot_id.startswith("COLLECTOR-"):
        raise ValueError("PLC boot identity is missing or invalid")
    try:
        return str(uuid.UUID(boot_id))
    except ValueError as exc:
        raise ValueError("PLC boot identity must be a UUID") from exc


def classify_counter(last_counter: int | None, current_counter: int) -> CounterDecision:
    if last_counter is None or current_counter > last_counter:
        return CounterDecision.ACCEPT
    if current_counter == last_counter:
        return CounterDecision.DUPLICATE
    return CounterDecision.RESET
