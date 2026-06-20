# Phase-2 Flexible Line Architecture Plan

更新时间：2026-06-19
状态：正式架构规划，尚未实施
范围：单线柔性化优先，预留 Multi-Line
控制边界：非侵入式 Edge MES / Traceability / OEE

## 1. 规划结论

Phase-2 的核心不是“把固定 WS01~WS03 改成更多 if/else”，而是建立一条配置驱动、
可验证、可观测的柔性产线数据链：

```text
Line Configuration
→ Configurable V-PLC / Real PLC
→ Config-driven Collector
→ Shared PostgreSQL Event Model
→ Bounded FastAPI Query Layer
→ Custom Management Dashboard + Grafana Engineering View
```

Phase-1 的 WS01~WS03 是默认兼容配置，不是 Phase-2 数据模型的上限。目标能力：

- 简单线：WS01~WS03。
- 中等线：WS01~WS10。
- 较高负载线：WS01~WS20。
- 超过 20 站：合同允许表达，必须先完成硬件 sizing 和专项验收。
- 一条线可包含多个 PLC，每个 PLC 下挂不同数量工站。
- 工站可混合基础状态、复杂 payload、人工确认、测试、视觉、标签等类型。
- 支持 Buffer 拓扑和观测，但不让 Edge 控制 Buffer 或设备流转。
- Multi-Line 在模块化单线稳定后规划，不作为 Phase-2 第一实施目标。

## 2. 不可改变的系统边界

| 责任 | PLC / HMI | Edge |
| --- | --- | --- |
| 设备动作、安全、互锁 | 决定并执行 | 不介入 |
| Hold / Release | 定义流程、时机、原因 | 记录、展示、统计 |
| Rework | 定义对象、路线、完成条件 | 记录轮次与 Genealogy |
| Skip / Bypass | 决定是否跳站 | 保存状态和原因 |
| Manual NOK | 操作员/HMI 确认 | 保存来源和证据 |
| Cycle / payload | 产生事实 | 采集、解析、落库 |
| OEE / Quality / Trace | 提供事实 | 计算、查询、展示 |

Edge 不根据测量值自行将 OK 改为 NOK，不主动 Hold/Release，不决定 Rework 路线，也不
把“没有采到事件”直接解释为现场执行了某种流程。

## 3. Flexible Line Architecture

详细合同：

- [`../contracts/line_configuration.md`](../contracts/line_configuration.md)
- [`../contracts/dynamic_station_model.md`](../contracts/dynamic_station_model.md)

### 3.1 标准维度

所有配置、事件、API 和 Dashboard 使用：

```text
line_id
plc_id
station_id
station_order
station_type
station_enabled
plc_boot_id
profile
config_hash
```

`station_order` 只表示默认路线顺序，不替代 `station_id`。API 响应统一使用
`station_enabled`，存储与 YAML 规范字段为 `enabled`。

### 3.2 配置层

```text
YAML 人工真源
→ JSON Schema 结构校验
→ semantic validator 语义校验
→ resolved JSON
→ config hash / snapshot
→ V-PLC 与 Collector 加载
```

配置包括 line、PLC、station、Buffer、DB mapping、payload template、NOK template、
cycle profile、station-level cycle time、station-level NOK rate 和 simulation seed。

### 3.3 负载分级

| 场景 | 工站 | PLC | payload | 目的 |
| --- | ---: | ---: | --- | --- |
| Default | 3 | 1 | Phase-1 payload | 兼容回归 |
| Medium | 10 | 1~2 | 基础与复杂混合 | 常规扩展 |
| High | 20 | 2+ | 多 mapping、Buffer | Raspberry Pi 边界 |

工站数不是唯一容量指标；必须综合 polling、read size、cycle rate、写入批量、API 查询和
磁盘增长。

## 4. V-PLC 参数化路线

### 4.1 Phase-2 定位

V-PLC 是配置驱动的产线数据发生器、异常发生器和性能验证工具：

- 模拟产线结构与 Buffer。
- 生成 cycle、payload、NOK、Skip 和 identity。
- 生成 normal/fast/test Profile。
- 生成可复现的异常和高频压力负载。
- 为 Collector、DB、API、Dashboard 提供长稳与回归输入。

它不是 PLC 控制算法替代品，不模拟安全回路、运动控制、真实互锁、设备保护、HMI 审批
和未经定义的现场流程。

### 4.2 目标运行结构

```text
LineSimulator
  ├─ PlcRuntime[]
  ├─ StationRuntime[]
  ├─ BufferRuntime[]
  ├─ RouteGraph
  ├─ PayloadGenerator
  ├─ NokGenerator
  ├─ ProfileResolver
  └─ AuditSnapshotWriter
```

每个 StationRuntime 从配置读取：

- `station_type`、`station_order`、mapping 和 payload template。
- base/jitter/ideal cycle time。
- station NOK rate 与 NOK template。
- global NOK fallback。
- 独立 RNG stream。

### 4.3 可复现与治理

- 使用固定 random seed：全局 `random_seed` + station offset 生成稳定随机序列。
- 启动、reload、profile 切换、参数变更均保存 snapshot。
- 参数变更记录 actor、reason、request_id、old/new 和 accepted/rejected。
- 同一 config hash、seed、Profile 和场景必须产生可解释的重复结果。
- fast/test 只改变仿真速度，不改变 OEE ideal cycle time。

### 4.4 压测与长稳

支持：

- 3/10/20 工站。
- 不同 polling 与 cycle rate。
- 基础 payload、复杂 JSONB payload、多 DB mapping。
- burst、PLC disconnect/reconnect、ACK delay、DB slow write。
- 1 小时 smoke、8 小时稳定性、24 小时 soak。

压测数据必须标记 `profile=test` 或独立 `test_run_id`，不得进入 normal OEE。

## 5. Collector 配置化路线

### 5.1 目标结构

```text
ConfigLoader
→ PlcRuntime[]
  → MappingRuntime[]
    → ReadPlan[]
      → Decoder
      → PayloadValidator
      → EventNormalizer
      → In-memory Queue
      → Batch Writer
      → ACK Writer
```

Collector 从 line configuration 获取采集目标，按 DB mapping 读取，按 station type 和
payload template 解码，生成通用 raw/cycle/station/quality 事件。

### 5.2 可靠性延续

- PLC 断连采用有界指数退避，恢复后先重新读取 runtime identity。
- `plc_boot_id` 变化时切换 counter namespace。
- 同 boot counter 回绕按错误处理，不 ACK 不可信 payload。
- 重复 cycle 依靠唯一键幂等，不重复生成业务事件。
- Profile 必须随事件落库或通过 boot snapshot 无歧义关联。
- ACK 只能在 raw sample 与业务事件事务成功后写回。
- 不补造不存在的 cycle event。

### 5.3 队列、批量与 Backpressure

首版采用进程内有界队列：

- 每 PLC 独立采集任务，避免慢 PLC 阻塞其他 PLC。
- EventNormalizer 后进入有界写库队列。
- Batch Writer 按条数或最大等待时间 flush。
- 队列达到 warning 阈值时降低非关键诊断采样频率。
- 队列达到 hard limit 时停止读取新 payload 或保持 PLC payload 未 ACK；不得丢弃已确认
  需要持久化的 cycle。
- raw diagnostic sample 可按合同降采样，cycle/station/quality 事实不可静默丢弃。

### 5.4 可观测指标

预留 Prometheus：

```text
collector_plc_connected
collector_last_sample_timestamp_seconds
collector_poll_latency_seconds
collector_decode_errors_total
collector_queue_depth
collector_queue_capacity
collector_db_batch_size
collector_db_write_latency_seconds
collector_ack_latency_seconds
collector_ack_failures_total
collector_events_total{line,plc,station,result}
collector_config_hash_info
```

Cardinality 规则：不把 `unit_id`、`cycle_counter`、原始错误文本放入 metric label。

## 6. PostgreSQL 动态模型

核心原则：

- 配置表 + 通用事件表 + JSONB payload。
- 不为每个工站建表。
- 稳定过滤、关联、排序、唯一约束字段结构化。
- 工站专有测量值留在版本化 payload。
- boot/profile isolation 是查询默认条件，不是可选修饰。

主要实体：

```text
production_line
plc_config
station_config
station_type
station_payload_schema
station_nok_template
buffer_config
plc_db_mapping
cycle_event
station_event
quality_event
hold_event (reserved)
rework_event (reserved)
production_unit
unit_relation (reserved)
```

整线聚合读取 terminal station 配置，不再固定 WS03。

## 7. API 演进

API 不再假设三工站。所有列表和聚合必须支持有界时间窗、分页、过滤和最大返回限制。

查询能力：

- by-cycle：完整 boot identity。
- by-unit / DMC / UID。
- by-station / station_type。
- by-NOK-code。
- by-time-window。
- OEE summary。
- Quality summary。
- Dashboard summary。
- raw payload drilldown。

防护：

- 默认时间窗不超过 8 小时，最大同步窗口 31 天。
- cursor pagination 优先于大 offset。
- 聚合 API 使用允许的维度和粒度，禁止任意 SQL。
- 大报告走异步导出和预聚合。
- 响应返回 `profile_scope`、`config_version`、`data_completeness` 和口径版本。

## 8. Trace / Genealogy

Trace Explorer 支持：

- cycle、DMC、UID、station、NOK code、时间窗。
- 一个 unit 经过的动态工站列表。
- 每站 PASS/NOK/SKIPPED、时间、counter、boot。
- raw payload 和 quality event 下钻。
- skipped chain、defect origin、Hold/Rework 预留。

Genealogy 只使用明确 `unit_relation`：

- `ASSEMBLED_FROM`
- `PACKED_IN`
- `REPLACED_BY`
- `REWORK_OF`

禁止按时间邻近猜测父子件。

## 9. OEE / Quality 优先级

OEE 是 Phase-2 高优先级，但必须区分“完整 OEE”和“数据不足”：

```text
Availability = Run Time / Planned Production Time
Performance = Ideal Cycle Time × Total Count / Run Time
Quality = Good Count / Total Count
OEE = A × P × Q
```

缺少 production calendar、planned stop 或 equipment state 时，不生成伪完整
Availability。

OEE 页面：

- line/station OEE。
- A/P/Q cards 和趋势。
- NOK loss。
- downtime/hold loss 预留。
- 时间窗、Profile、station filter。
- 异常原因下钻。

Quality 页面：

- NOK trend、station ranking、NOK distribution/Pareto。
- FPY/pass rate。
- payload drilldown。
- DMC/UID 查询。
- 报告导出预留。

## 10. Grafana 与自研 Dashboard 分工

Grafana 保留工程视角：

- 主机、容器、DB、Collector、PLC、ACK。
- queue、latency、error、Profile 和 Prometheus metrics。
- 工程诊断 SQL。

自研 Dashboard 面向管理层、Demo 和质量分析：

- OEE、Quality、Trace、Genealogy。
- 动态工站拓扑。
- 低术语、可下钻、可品牌化。

Grafana 不作为最终管理层首页或质量追溯主界面。

## 11. Hold / Rework / Data Gap / Missing Unit

| 能力 | Phase-2 决策 | 原因 |
| --- | --- | --- |
| Hold event model | 模型预留；Sprint 6 实施 | PLC/HMI 定义，Edge 记录 |
| Rework | 模型预留；feature flag 默认关闭 | 业务复杂，非首要价值 |
| Data Gap | 保留现有合同，不作为核心 MVP | 依赖 PLC bypass/identity 事实 |
| Missing Unit | 暂不做自动判断 | Edge 无法区分 PLC 跳号 bug 与真实缺件 |

未来 UID 建议由 PLC 在托盘进入新循环时，结合受控服务器/NTP 时间源生成。Edge 只验证
和保存，不自行修正 UID。

## 12. Raspberry Pi 性能边界评估

测试矩阵：

| 维度 | 值 |
| --- | --- |
| 工站 | 3 / 10 / 20 |
| PLC | 1 / 2 / 4 |
| cycle | normal / fast / test / burst |
| payload | 0.5 KB / 2 KB / 8 KB |
| mapping | 1 / 2 / 4 per station |
| DB condition | normal / 100ms delay / 500ms delay |
| network | normal / jitter / disconnect |
| duration | 1h / 8h / 24h |

建议起始验收阈值，最终由实测校准：

- 无 cycle 事实丢失、无重复 identity。
- ACK 非 OK 不持续积压。
- queue 平稳可回落，不触及 hard limit。
- Collector poll p95 小于最短 poll interval 的 80%。
- DB write p95 小于 batch flush interval。
- API summary p95 < 1s，Trace detail p95 < 2s。
- CPU 持续值、内存、温度、磁盘增长在硬件安全范围。
- 24 小时后 config hash、boot isolation、Profile isolation 不漂移。

Verification 必须输出“通过的 envelope”，例如“2 PLC × 20 stations × 2 KB payload ×
500ms poll”，而不是笼统声称支持 20 站。

## 13. Phase-2 MVP

进入 MVP：

1. Flexible Line Configuration。
2. Generic Station Event Model。
3. Configurable V-PLC / Collector。
4. OEE API and Dashboard MVP。
5. Quality Dashboard / Trace Explorer。

模型预留：

- Hold。
- Rework。
- Genealogy relation。
- downtime / hold loss。
- report export。

暂不做：

- Multi-Line 实施。
- Data Gap 作为核心功能。
- Missing Unit 自动判断。
- Oracle / ERP。
- Edge 控制 PLC。
- 3D 数字孪生。

## 14. 实施门禁

```text
contract
→ tests and migration plan
→ implementation
→ local verification
→ controlled remote deploy
→ rollback drill when stateful/risky
→ report and handoff
```

本规划阶段不修改业务代码、migration、API/Collector/V-PLC/Dashboard 实现，不远程部署。
