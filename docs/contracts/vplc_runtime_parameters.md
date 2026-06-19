# V-PLC Runtime Parameter Contract

更新时间：2026-06-19  
适用范围：单机、单产线、三工站 V-PLC Demo。

## 1. 参数真源

参数解析优先级固定为：

```text
built-in safe defaults
  → config/vplc.yaml
  → VPLC_PROFILE / VPLC_CYCLE_SCALE
  → 受 profile 约束的 runtime update
```

每次启动必须生成 resolved configuration，至少包含 profile、scale、三站最终参数、
配置来源、配置 hash、加载时间和 PLC boot ID。

## 2. Profile

| Profile | 默认 scale | runtime cycle edit | 用途 |
| --- | ---: | --- | --- |
| `normal` | 1.0 | 禁止 | 现场演示和正常生产口径 |
| `fast` | 0.1 | 允许 | 人工快速演示 |
| `test` | 0.05 | 允许 | 自动化测试 |

`normal` profile 必须满足：

- `cycle_scale = 1.0`。
- 每站 `base_cycle_s` 在 20–60 秒。
- 每站 `jitter_s` 在 0–10 秒。
- runtime API 不得修改 `base_cycle_s` 或 `jitter_s`。

快速仿真只能通过 `fast/test` profile 或 `cycle_scale` 实现，不得把 process base
修改为 1 秒。

## 3. Station 基线

| Station | base_cycle_s | jitter_s | nok_rate |
| --- | ---: | ---: | ---: |
| WS01 | 30.4 | 1.2 | 0.020 |
| WS02 | 29.8 | 1.0 | 0.015 |
| WS03 | 29.2 | 0.9 | 0.010 |

三站配置必须完整；缺站、类型错误或越界时 V-PLC 启动失败。

## 4. Runtime Update

`POST /vplc/stations/{station_id}`：

- `normal` profile 可修改 `paused` 和 NOK 模拟参数，但不可修改 cycle base/jitter。
- `fast/test` profile 可修改 base/jitter。
- 参数修改必须携带非空 `reason`。
- 服务端生成或接收 `request_id`，记录 actor、client IP、old/new、profile、
  accepted 和 rejection reason。
- rejected update 不得改变运行参数。

## 5. 参数审计与快照

参数变更写入追加式 `vplc_parameter_change_log`。

完整参数快照写入 `vplc_parameter_snapshot`，至少在以下时点生成：

- V-PLC 启动。
- runtime 参数修改成功。
- pipeline reset。
- 周期性心跳。

审计或快照数据库暂时不可用时，V-PLC 生产模拟不得退出；必须写错误日志并保留内存中的
最近记录，待查询和故障诊断。

## 6. NOK 模拟

- station 只接受本工站定义的 NOK code。
- 强制 NOK 支持 `count=1..100`，按队列作用于后续实际加工的 cycle。
- 上游 NOK 后，下游 `SKIPPED` 不消费下游强制 NOK 队列。
- 可查询每站待执行强制 NOK 数量和 code。
- 可显式清除未执行的强制 NOK 队列。
- 随机 NOK 与强制 NOK 均不得改变 cycle identity、ACK 或下游 skip 语义。

## 7. 兼容性

- legacy DB100 Simulator 和 8100 场景控制保持原行为。
- DB101/102/103 PLC 地址不变。
- DB104 identity 与 strict ACK 契约不变。
- 测试仍可直接构造 `ThreeStationPipeline(scale=0.05)`。

## 8. Dashboard Profile 归属

Grafana 中基于 `cycle_event` 的产量、合格率、Cycle Time、NOK 和 ACK 指标，必须先按
`cycle_event.plc_boot_id` 关联 `vplc_parameter_snapshot.plc_boot_id`，再应用 Profile
过滤。

- Dashboard 默认 Profile 为 `normal`，用于正常生产和验收口径。
- `fast`、`test` 仅在用户明确选择对应 Profile 时计入 KPI。
- 找不到参数快照的历史 boot 归类为 `unknown`，不得推断为 `normal`。
- 用户选择 `All` 时允许跨 Profile 展示，但 Dashboard 必须显式显示时间窗内的 Profile
  构成；存在多个 Profile 时必须标记为 `MIXED`。
- Collector 当前状态和 Raw PLC Sample 属于实时采集诊断，不作为生产 KPI，不强制应用
  Profile 过滤。

该关联只使用现有 boot identity 和参数快照，不改变 cycle identity、ACK、PLC SIM 或
Collector 采集协议。
