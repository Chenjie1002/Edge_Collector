from __future__ import annotations

from app.models import MachineState
from app.services.storage import Storage


class EventDetector:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self.previous: MachineState | None = None
        self.open_alarm_event_id: str | None = None
        self.open_stop_event_id: str | None = None

    def process(self, state: MachineState) -> None:
        prev = self.previous
        if prev is None:
            if state.alarm_active:
                self.open_alarm_event_id = self.storage.open_alarm(state)
                self.storage.insert_event(state, "alarm_started", state.alarm_code)
            else:
                self.storage.close_open_alarms(state)
            if not state.running or state.stop_reason_code != 0:
                self.open_stop_event_id = self.storage.open_stop(state, state.stop_reason_code)
                self.storage.insert_event(state, "stop_started", state.stop_reason_code)
            else:
                self.storage.close_open_stops(state)
            self.previous = state
            return

        cycle_delta = state.cycle_counter - prev.cycle_counter
        if cycle_delta > 0:
            self.storage.insert_event(
                state,
                "cycle_completed",
                None,
                {"cycle_delta": cycle_delta, "cycle_time_ms": state.cycle_time_ms},
            )

        if not prev.alarm_active and state.alarm_active:
            self.open_alarm_event_id = self.storage.open_alarm(state)
            self.storage.insert_event(state, "alarm_started", state.alarm_code)
        elif prev.alarm_active and not state.alarm_active:
            if self.open_alarm_event_id:
                self.storage.close_alarm(self.open_alarm_event_id, state)
            else:
                self.storage.close_open_alarms(state)
            self.storage.insert_event(state, "alarm_ended", prev.alarm_code)
            self.open_alarm_event_id = None

        prev_stopped = (not prev.running) or prev.stop_reason_code != 0
        now_stopped = (not state.running) or state.stop_reason_code != 0
        if not prev_stopped and now_stopped:
            reason = state.stop_reason_code or 999
            self.open_stop_event_id = self.storage.open_stop(state, reason)
            self.storage.insert_event(state, "stop_started", reason)
        elif prev_stopped and not now_stopped:
            if self.open_stop_event_id:
                self.storage.close_stop(self.open_stop_event_id, state)
            else:
                self.storage.close_open_stops(state)
            self.storage.insert_event(state, "stop_ended", prev.stop_reason_code)
            self.open_stop_event_id = None

        if prev.product_type != state.product_type:
            self.storage.insert_event(state, "product_changed", None, {"from": prev.product_type, "to": state.product_type})

        if prev.shift_id != state.shift_id:
            self.storage.insert_event(state, "shift_changed", None, {"from": prev.shift_id, "to": state.shift_id})

        self.previous = state
