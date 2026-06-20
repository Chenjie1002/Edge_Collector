# Phase-2 Sprint 1 Flexible Line Configuration Report

日期：2026-06-20
Thread：Architecture / Integration
状态：Sprint 1 Gate PASS，准备 final commit / push，未接入运行链路

## 1. Sprint 1 目标

建立一个独立、轻量、可本地验证的柔性产线配置层，能够描述 Phase-1 三工站默认线、
中等 10 工站示例和 20 工站压力配置，但不一次性重构 V-PLC、Collector、API、数据库
或 Dashboard。

## 2. 实现范围

```text
config/lines/*.yaml
→ common.line_config.load_line_config()
→ semantic validation
→ frozen dataclass objects
```

本 Sprint 没有把配置接入任何现有服务。当前配置是后续 Sprint 的输入和测试资产，不是
新的运行时真源。

## 3. 新增配置文件

### `demo_3_station.yaml`

表达 Phase-1 默认结构：

| Station | Type | PLC | DB | Cycle | NOK rate |
| --- | --- | --- | ---: | ---: | ---: |
| WS01 | `screwdriving` | PLC_001 | 101 | 30.4s | 0.02 |
| WS02 | `eol_test` | PLC_001 | 102 | 29.8s | 0.015 |
| WS03 | `manual_confirm` | PLC_001 | 103 | 29.2s | 0.01 |

保留 `LINE_001`、`PLC_001`、runtime DB104 和两个站间 FIFO Buffer。

### `demo_10_station.yaml`

- 10 个工站、一个 PLC。
- 混合 assembly、screwdriving、press、vision、test、label、manual、pack 和 generic。
- 两个 Buffer 示例。
- 包含复杂 payload template 和基础状态 template。

### `stress_20_station.yaml`

- WS01~WS20。
- 两个 PLC，每个 10 个工站。
- 四个 Buffer。
- 一个工站包含第二个 `payload_ext` DB mapping。
- WS20 使用 `station_enabled: false` 验证禁用配置表达。
- 全部 cycle profile 标记为 test 语义，仅用于未来配置/性能验证。

## 4. Loader / Validator

位置：

```text
common/line_config/
  __init__.py
  models.py
  loader.py
  validator.py
```

公共入口：

```python
from common.line_config import LineConfigError, load_line_config

config = load_line_config("config/lines/demo_3_station.yaml")
```

返回对象为 frozen dataclass tree：

- `LineConfig`
- `PlcConfig`
- `StationConfig`
- `DbMapping`
- `BufferConfig`
- `PayloadTemplate`
- `NokTemplate`
- `CycleProfile`

错误使用 `LineConfigError` 聚合返回，包含字段路径和具体原因。

## 5. 已实现校验规则

- `line_id` 必填。
- PLC 的 `plc_id`、runtime DB、station/mapping 限制必填且为正数。
- station 的 `station_id` 必填且唯一。
- `station_order` 必填、为正数且唯一。
- `station_type` 和 station `plc_id` 必填。
- station 引用的 PLC 必须存在。
- `station_enabled` 缺省为 `true`，显式值必须为 boolean。
- station-level `nok_rate` 必须在 0~1。
- station-level `cycle_time_s` 必须为正数。
- `payload_template` 可为空；非空时必须存在且兼容 station type。
- `nok_template` 必须存在且兼容 station type。
- `cycle_profile` 必须存在，mode 只能是 normal/fast/test。
- cycle profile 的 ideal cycle time 必须为正数。
- DB mapping 至少一项；mapping ID 全局唯一。
- 同 PLC 的 DB number 不得重复冲突。
- station DB 不得占用同 PLC 的 runtime DB。
- 每站 mapping 数不得超过 PLC 声明上限。
- 单 PLC 工站数不得超过 `max_stations`。
- Buffer ID 唯一、上下游 station 必须存在且不能相同。
- `buffer_position` 必须严格位于上下游 station order 之间。
- Buffer capacity 必须为正数或空。
- payload/NOK template 的 compatible station types 不得为空。
- NOK code 必须是非空、不重复的整数列表。
- YAML 文件不存在、YAML 语法错误、根节点非 mapping 时返回清晰错误。

## 6. 测试结果

目标命令：

```bash
.venv/bin/python -m pytest -q tests/test_line_config.py
```

结果：

```text
21 passed
```

覆盖：

- 三份示例加载。
- Phase-1 三工站身份、类型、DB、cycle 和 NOK rate。
- frozen dataclass。
- duplicate station ID/order。
- NOK rate、cycle time。
- 必填字段。
- Buffer position。
- PLC station limit。
- payload/NOK/cycle template。
- DB conflict 和 mapping limit。
- runtime DB reservation。
- `station_enabled` 默认值。
- nullable payload template。

完整本地验证：

```text
配置层 tests/test_line_config.py: 21 passed
根级 tests/: 32 passed
API tests: 5 passed
Collector tests: 12 passed, 3 subtests passed
V-PLC tests: 27 passed
Python compileall: PASS
三份 YAML 独立加载: PASS
git diff --check: PASS
```

## 7. 未修改的业务链路

本 Sprint 未修改：

- V-PLC。
- Collector。
- FastAPI / Trace。
- PostgreSQL schema 或 migration。
- Grafana / 自研 Dashboard。
- Docker Compose。
- `.env`。
- volume、日志、缓存。
- Raspberry Pi 远程环境。

现有运行代码没有导入 `common.line_config`，Phase-1 默认运行行为保持原样。

## 8. 后续影响

### V-PLC / Reliability

后续可将 `LineConfig` 转为 StationRuntime/BufferRuntime，但必须保持 strict ACK、boot、
Profile 和参数审计。

### Collector

后续可从 `LineConfig` 生成 PlcRuntime 和 read plan。本 Sprint 不替代
`config/mapping.yaml`。

### Data Quality

可使用 line/PLC/station/order/type 作为动态模型输入，但 migration 和事件表变化属于
Sprint 2。

### Verification

应继续扩展地址范围、route graph、runtime DB 冲突、负载 envelope 和 resolved config
稳定性负例。

## 9. Contract Hardening 更新

初始实现收到 Verification 与 Reliability 的 `HOLD / CHANGES REQUIRED` 后，已完成：

- strict unknown-field rejection 与集中 schema/enum registry。
- Profile mode preservation 与 production/simulation timing 分离。
- config version、resolved config、canonical JSON 和 stable SHA-256。
- scenario、seed、global NOK fallback 和 station override。
- 20 station / 4 mapping 不可由普通 YAML 放大的硬上限。
- mapping read range/size/poll/direction/usage/type。
- payload field layout 与 NOK code permission/reserved semantics。
- route entry/terminal/edge、Buffer 和 disabled station 校验。
- hardware envelope 与轻量静态负载估算。
- 77 项配置层测试全部通过。

详细证据：

- `docs/reports/sprint1_contract_hardening_report.md`

## 10. 已知限制

- 没有引入 JSON Schema。
- 没有将 resolved config/hash 持久化到数据库或配置快照仓库。
- 没有完整 field-level S7 overlap/PDU/read-plan 生成。
- 只校验同 PLC DB number 重复，不校验一个 DB 内字段区间。
- route graph 只实现 Sprint 1 线性基础引用、enabled 和可达性校验，不实现复杂分支、
  合流、循环和控制语义。
- 静态 load estimate 不是 Raspberry Pi 性能验收。
- YAML 是示例和未来输入，尚未成为现有服务运行时真源。

## 11. 下一步建议

1. Reliability 与 Verification 评审三份配置和负例矩阵。
2. 由后续配置治理生成 JSON Schema、快照持久化和只读验证 CLI。
3. Sprint 3 前补完整 field overlap、read plan 和复杂 route graph。
4. 在 Sprint 1 完整 gate 通过后，再由后续 Sprint 分别接入 V-PLC 和 Collector。

本轮不 push、不创建 tag，也不提交既有未跟踪旧进度报告。
