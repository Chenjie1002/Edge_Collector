from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

TZ = ZoneInfo("Asia/Shanghai")


@dataclass
class TimedCondition:
    active: bool = False
    until: datetime | None = None
    code: int = 0

    def expired(self, now: datetime) -> bool:
        return self.active and self.until is not None and now >= self.until


@dataclass(frozen=True)
class ScenarioDefinition:
    id: str
    name: str
    description: str
    default_duration_seconds: int
    mode: str
    alarm_code: int = 0
    stop_reason_code: int = 0
    cycle_time_multiplier: float = 1.0
    ng_rate_multiplier: float = 1.0
    product_type: str | None = None


SCENARIOS: tuple[ScenarioDefinition, ...] = (
    ScenarioDefinition(
        id="normal",
        name="正常生产",
        description="清除手动停机/报警，恢复按配置随机扰动的正常生产。",
        default_duration_seconds=0,
        mode="normal",
    ),
    ScenarioDefinition(
        id="material_shortage",
        name="第1岗位缺料",
        description="模拟物料配送不及时导致工位缺料，PLC stop_reason_code=2。",
        default_duration_seconds=180,
        mode="stop",
        stop_reason_code=2,
    ),
    ScenarioDefinition(
        id="sensor_fault",
        name="气缸传感器故障",
        description="模拟气缸到位信号丢失，PLC alarm_code=1002。",
        default_duration_seconds=180,
        mode="alarm",
        alarm_code=1002,
    ),
    ScenarioDefinition(
        id="changeover",
        name="换型/调机",
        description="模拟产品换型和设备调整，PLC stop_reason_code=4。",
        default_duration_seconds=300,
        mode="stop",
        stop_reason_code=4,
        product_type="NEXT",
    ),
    ScenarioDefinition(
        id="maintenance",
        name="计划保养",
        description="模拟计划维护保养，PLC stop_reason_code=5。",
        default_duration_seconds=300,
        mode="stop",
        stop_reason_code=5,
    ),
    ScenarioDefinition(
        id="slow_cycle",
        name="节拍变慢",
        description="模拟设备轻微卡滞或人员节奏下降，节拍约放大35%。",
        default_duration_seconds=300,
        mode="profile",
        cycle_time_multiplier=1.35,
        ng_rate_multiplier=1.2,
    ),
    ScenarioDefinition(
        id="fast_run",
        name="熟练稳定生产",
        description="模拟员工熟练度提升，平均节拍更快且不良率更低。",
        default_duration_seconds=300,
        mode="profile",
        cycle_time_multiplier=0.93,
        ng_rate_multiplier=0.65,
    ),
)

SCENARIO_BY_ID = {scenario.id: scenario for scenario in SCENARIOS}


class ProductionSimulator:
    def __init__(self, config_path: str = "/app/config/simulator.yaml") -> None:
        self.config = self._load_config(config_path)
        sim = self.config.get("simulation", {})
        self.machine_id = self.config.get("machine_id", "LINE_01")
        self.base_cycle_time_ms = int(sim.get("base_cycle_time_ms", 1200))
        self.cycle_time_jitter_ms = int(sim.get("cycle_time_jitter_ms", 180))
        self.ng_rate = float(sim.get("ng_rate", 0.025))
        self.product_types = sim.get("product_types", ["TYPE_A"])

        self.cycle_counter = 0
        self.good_count = 0
        self.ng_count = 0
        self.total_count = 0
        self.product_type = self.product_types[0]
        self.last_tick = datetime.now(TZ)
        self.accumulated_ms = 0
        self.cycle_time_ms = self.base_cycle_time_ms
        self.alarm = TimedCondition()
        self.stop = TimedCondition()
        self.slowdown_until: datetime | None = None
        self.manual_scenario: ScenarioDefinition = SCENARIO_BY_ID["normal"]
        self.manual_scenario_until: datetime | None = None
        self.random_paused_until: datetime | None = None

    def _load_config(self, path: str) -> dict:
        p = Path(path)
        if not p.exists():
            return {}
        return yaml.safe_load(p.read_text()) or {}

    def tick(self) -> None:
        now = datetime.now(TZ)
        elapsed_ms = max(0, int((now - self.last_tick).total_seconds() * 1000))
        self.last_tick = now

        self._expire_manual_scenario(now)
        random_paused = self.random_paused_until is not None and now < self.random_paused_until
        if self.manual_scenario.id == "normal" and not random_paused:
            self._update_random_scenarios(now)
        if self.random_paused_until and now >= self.random_paused_until:
            self.random_paused_until = None

        if self.alarm.expired(now):
            self.alarm = TimedCondition()
        if self.stop.expired(now):
            self.stop = TimedCondition()
        if self.slowdown_until and now >= self.slowdown_until:
            self.slowdown_until = None

        running = not self.alarm.active and not self.stop.active
        if running:
            self.accumulated_ms += elapsed_ms
            while self.accumulated_ms >= self.cycle_time_ms:
                self.accumulated_ms -= self.cycle_time_ms
                self._complete_cycle()

    def _update_random_scenarios(self, now: datetime) -> None:
        scenarios = self.config.get("scenarios", {})
        stop_cfg = scenarios.get("random_short_stop", {})
        alarm_cfg = scenarios.get("random_alarm", {})
        slow_cfg = scenarios.get("cycle_slowdown", {})

        if (
            stop_cfg.get("enabled", True)
            and not self.stop.active
            and not self.alarm.active
            and random.random() < float(stop_cfg.get("probability_per_tick", 0.01))
        ):
            duration = random.randint(
                int(stop_cfg.get("min_duration_seconds", 30)),
                int(stop_cfg.get("max_duration_seconds", 120)),
            )
            self.stop = TimedCondition(True, now + timedelta(seconds=duration), random.choice([1, 2, 3, 5]))

        if (
            alarm_cfg.get("enabled", True)
            and not self.alarm.active
            and random.random() < float(alarm_cfg.get("probability_per_tick", 0.008))
        ):
            duration = random.randint(
                int(alarm_cfg.get("min_duration_seconds", 20)),
                int(alarm_cfg.get("max_duration_seconds", 90)),
            )
            self.alarm = TimedCondition(True, now + timedelta(seconds=duration), random.choice([1001, 1002, 1003, 1004]))

        if (
            slow_cfg.get("enabled", True)
            and self.slowdown_until is None
            and random.random() < float(slow_cfg.get("probability_per_tick", 0.02))
        ):
            self.slowdown_until = now + timedelta(seconds=random.randint(20, 90))

    def _expire_manual_scenario(self, now: datetime) -> None:
        if (
            self.manual_scenario.id != "normal"
            and self.manual_scenario_until is not None
            and now >= self.manual_scenario_until
        ):
            self.manual_scenario = SCENARIO_BY_ID["normal"]
            self.manual_scenario_until = None
            self.alarm = TimedCondition()
            self.stop = TimedCondition()

    def _complete_cycle(self) -> None:
        self.cycle_counter += 1
        self.total_count += 1
        if random.random() < self._effective_ng_rate():
            self.ng_count += 1
        else:
            self.good_count += 1

        self._sample_next_cycle_time()

        if self.cycle_counter > 0 and self.cycle_counter % 400 == 0:
            current_idx = self.product_types.index(self.product_type)
            self.product_type = self.product_types[(current_idx + 1) % len(self.product_types)]

    def _sample_next_cycle_time(self) -> None:
        jitter = random.randint(-self.cycle_time_jitter_ms, self.cycle_time_jitter_ms)
        multiplier = self._effective_cycle_time_multiplier()
        base = self.base_cycle_time_ms * multiplier
        self.cycle_time_ms = max(300, int(base + jitter))

    def _effective_cycle_time_multiplier(self) -> float:
        if self.manual_scenario.mode == "profile":
            return self.manual_scenario.cycle_time_multiplier
        if self.slowdown_until:
            return float(self.config.get("scenarios", {}).get("cycle_slowdown", {}).get("cycle_time_multiplier", 1.5))
        return 1.0

    def _effective_ng_rate(self) -> float:
        if self.manual_scenario.mode == "profile":
            return max(0.0, min(1.0, self.ng_rate * self.manual_scenario.ng_rate_multiplier))
        return self.ng_rate

    def _scenario_remaining_seconds(self, now: datetime) -> int:
        if self.manual_scenario_until is None:
            if self.random_paused_until is None:
                return 0
            return max(0, int((self.random_paused_until - now).total_seconds()))
        return max(0, int((self.manual_scenario_until - now).total_seconds()))

    def scenarios(self) -> list[dict]:
        return [
            {
                "id": scenario.id,
                "name": scenario.name,
                "description": scenario.description,
                "default_duration_seconds": scenario.default_duration_seconds,
            }
            for scenario in SCENARIOS
        ]

    def set_scenario(self, scenario_id: str, duration_seconds: int | None = None) -> dict:
        if scenario_id not in SCENARIO_BY_ID:
            raise ValueError(f"unknown scenario: {scenario_id}")

        now = datetime.now(TZ)
        scenario = SCENARIO_BY_ID[scenario_id]
        if scenario.id == "normal":
            self.manual_scenario = scenario
            self.manual_scenario_until = None
            self.alarm = TimedCondition()
            self.stop = TimedCondition()
            self.slowdown_until = None
            self.random_paused_until = None
            if duration_seconds and int(duration_seconds) > 0:
                self.random_paused_until = now + timedelta(seconds=int(duration_seconds))
            return self.state()

        duration = max(1, int(duration_seconds or scenario.default_duration_seconds))
        until = now + timedelta(seconds=duration)
        self.manual_scenario = scenario
        self.manual_scenario_until = until
        self.random_paused_until = None
        self.slowdown_until = None
        self.alarm = TimedCondition()
        self.stop = TimedCondition()

        if scenario.product_type == "NEXT" and self.product_types:
            current_idx = self.product_types.index(self.product_type)
            self.product_type = self.product_types[(current_idx + 1) % len(self.product_types)]

        if scenario.mode == "alarm":
            self.alarm = TimedCondition(True, until, scenario.alarm_code)
        elif scenario.mode == "stop":
            self.stop = TimedCondition(True, until, scenario.stop_reason_code)

        if scenario.mode == "profile":
            self._sample_next_cycle_time()

        return self.state()

    def trigger_custom_fault(self, name: str, fault_code: int, duration_seconds: int) -> dict:
        if not 1001 <= int(fault_code) <= 1199:
            raise ValueError("fault_code must be between 1001 and 1199")
        duration = max(1, int(duration_seconds))
        now = datetime.now(TZ)
        until = now + timedelta(seconds=duration)
        fault_type = "设备故障" if int(fault_code) <= 1099 else "非设备故障"
        self.manual_scenario = ScenarioDefinition(
            id="custom_fault",
            name=name.strip() or f"{fault_type} {fault_code}",
            description=f"{fault_type}，自定义故障代码 {fault_code}。",
            default_duration_seconds=duration,
            mode="alarm",
            alarm_code=int(fault_code),
        )
        self.manual_scenario_until = until
        self.random_paused_until = None
        self.slowdown_until = None
        self.stop = TimedCondition()
        self.alarm = TimedCondition(True, until, int(fault_code))
        return self.state()

    def reset_counts(self) -> dict:
        self.cycle_counter = 0
        self.good_count = 0
        self.ng_count = 0
        self.total_count = 0
        self.accumulated_ms = 0
        return self.state()

    def state(self) -> dict:
        now = datetime.now(TZ)
        cycle_progress = 0.0
        if self.cycle_time_ms > 0:
            cycle_progress = max(0.0, min(100.0, round(self.accumulated_ms / self.cycle_time_ms * 100.0, 1)))
        return {
            "machine_id": self.machine_id,
            "ts": now.isoformat(),
            "running": not self.alarm.active and not self.stop.active,
            "auto_mode": True,
            "product_type": self.product_type,
            "shift_id": "DAY" if 8 <= now.hour < 20 else "NIGHT",
            "cycle_counter": self.cycle_counter,
            "good_count": self.good_count,
            "ng_count": self.ng_count,
            "total_count": self.total_count,
            "cycle_time_ms": self.cycle_time_ms,
            "cycle_elapsed_ms": self.accumulated_ms,
            "cycle_progress_percent": cycle_progress,
            "alarm_active": self.alarm.active,
            "alarm_code": self.alarm.code if self.alarm.active else 0,
            "stop_reason_code": self.stop.code if self.stop.active else 0,
            "scenario_id": self.manual_scenario.id,
            "scenario_name": self.manual_scenario.name,
            "scenario_remaining_seconds": self._scenario_remaining_seconds(now),
        }

    def trigger_alarm(self, code: int = 1001, duration_seconds: int = 60) -> dict:
        self.manual_scenario = SCENARIO_BY_ID["normal"]
        self.manual_scenario_until = None
        self.alarm = TimedCondition(True, datetime.now(TZ) + timedelta(seconds=duration_seconds), code)
        return self.state()

    def trigger_stop(self, code: int = 2, duration_seconds: int = 60) -> dict:
        self.manual_scenario = SCENARIO_BY_ID["normal"]
        self.manual_scenario_until = None
        self.stop = TimedCondition(True, datetime.now(TZ) + timedelta(seconds=duration_seconds), code)
        return self.state()

    def clear(self) -> dict:
        return self.set_scenario("normal")
