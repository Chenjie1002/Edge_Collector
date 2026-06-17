from pydantic import BaseModel


class ScenarioSummary(BaseModel):
    id: str
    name: str
    description: str
    default_duration_seconds: int


class ScenarioRequest(BaseModel):
    duration_seconds: int | None = None


class CustomFaultRequest(BaseModel):
    name: str
    fault_code: int
    duration_seconds: int


class MachineState(BaseModel):
    machine_id: str
    ts: str
    running: bool
    auto_mode: bool
    product_type: str
    shift_id: str
    cycle_counter: int
    good_count: int
    ng_count: int
    total_count: int
    cycle_time_ms: int
    cycle_elapsed_ms: int
    cycle_progress_percent: float
    alarm_active: bool
    alarm_code: int
    stop_reason_code: int
    scenario_id: str
    scenario_name: str
    scenario_remaining_seconds: int
