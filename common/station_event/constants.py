from __future__ import annotations

from enum import Enum


class EventType(str, Enum):
    STATION_CYCLE_START = "station_cycle_start"
    STATION_CYCLE_COMPLETE = "station_cycle_complete"
    STATION_RESULT = "station_result"
    STATION_NOK = "station_nok"
    STATION_HEARTBEAT = "station_heartbeat"


class AuditSubtype(str, Enum):
    NONE = "none"
    RAW_VARIANT = "raw_variant"


MVP_EVENT_TYPES = frozenset(item.value for item in EventType)

FUTURE_RESERVED_EVENT_TYPES = frozenset(
    {
        "station_skip",
        "station_hold",
        "station_release",
        "station_rework",
        "station_fault",
        "buffer_enter",
        "buffer_exit",
    }
)

EVENT_ROLES = {
    "station_cycle_start": "cycle_start",
    "station_cycle_complete": "cycle_complete",
    "station_result": "production_result",
    "station_nok": "nok_detail",
    "station_heartbeat": "heartbeat",
}

PAYLOAD_LIMITS = {
    "normalized_bytes": 16_384,
    "raw_bytes": 65_536,
    "depth": 6,
    "object_keys": 64,
    "tree_keys": 128,
    "key_bytes": 64,
    "array_items": 128,
    "tree_array_items": 256,
    "tree_nodes": 512,
    "normalized_string_bytes": 4_096,
    "raw_string_bytes": 16_384,
}
