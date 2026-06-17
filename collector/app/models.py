from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class MachineState:
    machine_id: str
    ts: datetime
    running: bool
    auto_mode: bool
    product_type: str
    shift_id: str
    cycle_counter: int
    good_count: int
    ng_count: int
    total_count: int
    cycle_time_ms: int
    alarm_active: bool
    alarm_code: int
    stop_reason_code: int

    @classmethod
    def from_payload(cls, payload: dict) -> "MachineState":
        return cls(
            machine_id=payload["machine_id"],
            ts=datetime.fromisoformat(payload["ts"]),
            running=bool(payload["running"]),
            auto_mode=bool(payload["auto_mode"]),
            product_type=str(payload.get("product_type") or ""),
            shift_id=str(payload.get("shift_id") or ""),
            cycle_counter=int(payload["cycle_counter"]),
            good_count=int(payload["good_count"]),
            ng_count=int(payload["ng_count"]),
            total_count=int(payload["total_count"]),
            cycle_time_ms=int(payload["cycle_time_ms"]),
            alarm_active=bool(payload["alarm_active"]),
            alarm_code=int(payload["alarm_code"]),
            stop_reason_code=int(payload["stop_reason_code"]),
        )

    def as_dict(self) -> dict:
        return {
            "machine_id": self.machine_id,
            "ts": self.ts.isoformat(),
            "running": self.running,
            "auto_mode": self.auto_mode,
            "product_type": self.product_type,
            "shift_id": self.shift_id,
            "cycle_counter": self.cycle_counter,
            "good_count": self.good_count,
            "ng_count": self.ng_count,
            "total_count": self.total_count,
            "cycle_time_ms": self.cycle_time_ms,
            "alarm_active": self.alarm_active,
            "alarm_code": self.alarm_code,
            "stop_reason_code": self.stop_reason_code,
        }

