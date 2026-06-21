# Dynamic Station Model Contract

更新时间：2026-06-21
状态：Sprint 2 Data Quality projection/completeness 与 Verification V10 derived-output
docs-only revision；尚未实施、未创建 migration
适用范围：动态产线、工站、Buffer、PLC mapping、Trace、Quality 和 OEE

## 1. 目的

本合同定义下一阶段建议的数据实体、主键、共享事件模型和 JSONB 边界。本文只冻结
逻辑模型，不修改当前数据库，不提供 migration。

## 2. 核心决策

1. 使用共享事件表，不为 WS01、WS02、WS03 或未来 WS04~WS20+ 创建独立业务表。
2. 使用关系列保存稳定查询维度，使用 JSONB 保存工站特有 payload。
3. `line_id + station_id` 标识工站实例；`plc_id` 标识事件来源 PLC。
4. 当前 WS01/WS02/WS03 数据原位兼容，不进行一次性破坏迁移。
5. YAML 是部署配置真源；数据库配置表保存已发布版本、查询副本和审计快照。

## 3. 推荐配置表

### 3.1 `production_line`

建议使用。它表达 Edge 管理的产线实例：

| 字段 | 说明 |
| --- | --- |
| `line_id` | 主键 |
| `line_code` / `name` | 显示信息 |
| `enabled` | 是否启用 |
| `timezone` | 产线时区 |
| `config_version` | 当前发布版本 |
| `config_hash` | resolved config hash |
| `metadata JSONB` | 非核心扩展信息 |

不建议继续把 `machines.machine_id` 同时当设备、产线和 PLC 使用。legacy
`machines` 可保留，新增查询通过兼容视图或映射关联到 `production_line`。

### 3.2 `plc_config`

建议新增逻辑实体：

- `plc_id` 主键。
- `line_id` 外键。
- protocol、host、port、rack、slot。
- runtime mapping、poll policy、enabled。
- 不存密码或敏感凭据明文。

一条线可有多个 PLC，一个 PLC 在当前合同中只能归属一条线。

### 3.3 `station_config`

建议使用，主键推荐 `(line_id, station_id)`：

- `plc_id`
- `station_order`
- `station_type`
- `name`
- `enabled`
- `payload_template_id`
- `nok_template_id`
- `cycle_profile_id`
- `metadata JSONB`

`station_order` 用于默认路线、展示和完整性检查，不应硬编码 `WS03` 是最终站。
建议额外声明 `is_entry_station`、`is_terminal_station`，或由路线边关系推导。

### 3.4 `buffer_config`

建议使用：

- 主键 `(line_id, buffer_id)`。
- `from_station_id`、`to_station_id`。
- `buffer_position`，用于拓扑/UI 排序。
- `buffer_type`、`capacity`、`tracking_mode`、`enabled`。
- 只表达拓扑与观测配置，不承载 PLC 控制队列。

### 3.5 `plc_db_mapping`

建议使用：

- `mapping_id` 主键。
- `line_id`、`plc_id`、可空 `station_id`。
- `db_number`、`purpose`、`poll_interval_ms`。
- `template_refs JSONB` 或独立关联表。
- `direction` 和 `enabled`。

字段级 mapping 在配置文件中维护，数据库保存发布后的 resolved JSON 和 hash 即可。
首版不需要把每个 S7 字段拆成数据库行，以免过早构建复杂配置编辑器。

### 3.6 `station_type`

保存受控工站类型，不保存工站实例：

| 字段 | 说明 |
| --- | --- |
| `station_type_id` | 主键，如 `SCREW`、`TEST`、`VISION` |
| `name` | 展示名称 |
| `category` | `ASSEMBLY/TEST/INSPECTION/MANUAL/GENERIC` |
| `default_payload_schema_id` | 默认 payload schema |
| `enabled` | 是否允许新配置引用 |
| `metadata JSONB` | 低频展示属性 |

历史 station event 必须保留当时的 `station_type` 快照，不能因类型表改名而失去解释。

### 3.7 `station_payload_schema`

保存 payload 模板的发布镜像：

- `payload_schema_id`、`version` 组成唯一版本。
- `compatible_station_types`。
- `schema_json JSONB`：字段名、类型、单位、required、范围和展示提示。
- `config_hash`、`published_at`、`deprecated_at`。

它用于校验和历史解释，不替代 YAML 模板真源，也不允许 API 在线修改真实 PLC 地址。

### 3.8 `station_nok_template`

保存 NOK 模板的发布镜像：

- `nok_template_id`、`version`。
- `station_type_id`、code、name、category、severity。
- `simulation_allowed`、`manual_simulation_allowed`。
- `definition JSONB`、`config_hash`。

真实事件中的 NOK code 来自 PLC/HMI。模板只负责解释、校验和展示。

## 4. 事件表设计

保留并推广当前共享表：

- `raw_plc_sample`
- `cycle_event`
- `station_event`
- `quality_event`
- `production_unit`
- `unit_state_history`
- `collector_runtime_status`
- `collector_error_log`
- `data_gap_event`

所有新查询必须以 `line_id` 作为首要过滤维度。event role/detail identity 以
`station_event_model.md` 为权威：

```text
production_result_key:
line_id + plc_id + station_id + plc_boot_id + cycle_counter + production_result role

station_nok_detail_key:
parent_fact_key + detail_role + nok_code + nok_origin

Station instance:
line_id + station_id

Unit identity:
line_id + unit_id
```

### 4.1 `cycle_event`

作为工站一次有效 cycle 的事实表，至少结构化：

- `event_id`
- `line_id`、`plc_id`、`station_id`、`station_order`、`station_type`
- `plc_boot_id`、`cycle_counter`
- `unit_id`
- `profile`
- `plc_start_time`、`plc_end_time`、`edge_received_at`
- `result`、`process_status`、`skip_reason`
- `cycle_time_ms`、`ack_status`
- `payload_schema_id`、`payload_schema_version`
- `payload JSONB`

逻辑唯一键：

```text
(line_id, plc_id, station_id, plc_boot_id, cycle_counter)
```

`cycle_event.result` 若为兼容现有 schema 而保留，只能是从 accepted canonical
`station_result` 派生的 non-authoritative compatibility projection。它不得接收独立
result authority，也不得与 canonical result 分别计数。每个 `production_result_key`
只能投影一次 outcome。

### 4.2 `station_event`

保存工件经过工站的追加式履历。它与 `cycle_event` 可一对一或一对多，但不得仅靠时间
邻近关联。至少包含 `source_cycle_event_id` 或等价的确定性来源键。

### 4.3 `quality_event`

保存规范化质量事实：

- `quality_event_id`
- `source_cycle_event_id`
- line/PLC/station/unit/boot/counter 维度
- `station_nok_detail_key`、`nok_code`、`nok_category`、`severity`
- `source`：`PLC/HMI/IMPORT`
- `payload JSONB`

`quality_event` 是 detail-only projection，不是 production result authority。一个 cycle
多个 accepted ordinary NOK detail 时可按不同 `station_nok_detail_key` 一 detail 一行，
便于 Pareto；每行不得重复 `result` 或增加 NOK cycle/outcome count。duplicate、
conflict、`system_reserved/30003` detail 不进入 ordinary defect projection。原始 code
数组可保留为 evidence，但不能直接成为 ordinary defect row。

### 4.4 Projection authority 与 completeness

`docs/contracts/station_event_model.md` 是 production result、detail uniqueness、duplicate/
conflict 与 completeness 的权威合同：

- `station_result` 是唯一 canonical production result carrier。
- 每个 `production_result_key` 只允许一次 accepted outcome projection。
- `cycle_event.result` 仅兼容派生；`quality_event` 仅 defect detail。
- `station_cycle_complete`、raw evidence 和 `station_nok` 不创建第二个 outcome。
- duplicate/conflict 不投影；`30003` 不进入 ordinary NOK、Quality、FPY 或 Pareto。

Pareto 查询/聚合必须携带：

```text
nok_cycle_count
nok_cycles_with_primary_detail
missing_primary_detail_cycle_count
detail_coverage
pareto_status = complete | partial
```

accepted NOK result 没有 accepted primary detail 时，`pareto_status=partial`。不得从 parent
静默合成 detail，也不得把 partial Pareto 展示为完整分布。

未来 projection 若保存 lifecycle 派生元数据，字段语义必须直接复用
`station_event_model.md` 的 `LifecycleDerivedOutput`：

```text
cycle_completeness
traceability_status
timeline_status
projection_eligible
parent_relation_status
detail_relation_status
late_status
```

这些是 derived audit/query metadata，不是新的 source event、设备控制状态或本轮 DB
migration 要求。`late_status` 在 Sprint 2 MVP 固定为
`not_evaluated_future_runtime`。

### 4.5 `hold_event` 预留

追加式记录 `HOLD_PLACED/HOLD_RELEASED/HOLD_SCRAPPED/HOLD_REMOVED`。事件必须来自
PLC/HMI 或受控导入，Edge 不提供主动控制设备的命令语义。

### 4.6 `rework_event` 预留

追加式记录 `REQUESTED/STARTED/COMPLETED/FAILED/ROUTE_ENTERED`，包含 `rework_round`、
来源事件和 route reference。只有 feature flag 开启且来源事件明确时才形成业务投影。

### 4.7 事件关联键

每条事件应有不可变 `event_id`，并携带可审计关联键：

```text
event_id
correlation_id
source_event_id
line_id + plc_id + station_id + plc_boot_id + cycle_counter
unit_pk / unit_id
config_hash + payload_schema_version
```

`correlation_id` 用于把同一 PLC payload 产生的 cycle、station、quality 和 raw sample
关联起来；它不能替代数据库唯一约束。

当前 `production_unit.unit_id` 是单列主键。进入真实多产线前，应先确认 `unit_id`
是否全局唯一；若不能保证，下一阶段 migration 应改为复合唯一约束或引入内部
`unit_pk`。本次规划不执行该 migration。

建议的 identity 关系：

| 标识 | 语义 |
| --- | --- |
| `unit_pk` | Edge 内部不可变主键 |
| `unit_id` / UID | PLC 在托盘进入新循环时生成的业务主标识 |
| DMC / label / reject ID | 可查询别名，不作为唯一关联依据 |
| `cycle_counter` | 某 PLC boot、某工站内的事件序号，不是全局 unit ID |
| `plc_boot_id` | counter 命名空间，必须参与隔离 |

未来 UID 建议由 PLC 在新循环入口结合受控时间源生成；Edge 不通过 counter 跳号自行
创造 Missing Unit。

## 5. JSONB 边界

推荐继续使用 JSONB，但不能把所有字段都塞入 JSONB。

必须使用关系列的字段：

- `line_id`、`plc_id`、`station_id`
- `station_order` 或 `route_step`
- `unit_id`
- `plc_boot_id`、`cycle_counter`
- 事件时间
- `result`、`process_status`
- `ack_status`
- 常用 trace key、final label、reject ID
- NOK code 数组或规范化质量事件

适合 JSONB 的内容：

- 不同 `station_type` 的工艺 payload。
- 模板版本、解码元数据。
- 低频扩展属性。
- 原始 decoded snapshot。

原则：

- 高频筛选、关联、排序、唯一约束字段必须是列。
- 工站特有测量值默认放 `payload JSONB`。
- 当某个 payload 字段成为跨工站、跨产线稳定 KPI 时，再提升为关系列或派生表。
- 每条事件记录 `payload_template_id` 和 `payload_template_version`，保证历史可解释。

## 6. 路线与 Genealogy

当前线性 WS01→WS02→WS03 可由 `station_order` 表达。为了支持 Rework、分支、合流和
装配 Genealogy，后续建议增加：

### `route_edge_config`

- `line_id`
- `from_station_id`
- `to_station_id`
- `route_type`：`NORMAL`、`REWORK_RETURN`、`BYPASS`
- `enabled`

### `unit_relation`

用于 Quality Genealogy：

- `line_id`
- `parent_unit_id`
- `child_unit_id`
- `relation_type`：`ASSEMBLED_FROM`、`PACKED_IN`、`REPLACED_BY`、`REWORK_OF`
- `station_id`
- `event_time`
- `source_event_id`
- `metadata JSONB`

`unit_relation` 只记录 PLC/HMI/扫码系统提供或可证明的关系，Edge 不按时间邻近猜测。

## 7. Hold 与 Rework 事件模型

### Hold

建议建模为追加式 `unit_status_event` 或通用 `manufacturing_event`：

| 字段 | 说明 |
| --- | --- |
| `event_type` | `HOLD_PLACED`、`HOLD_RELEASED` |
| `line_id` / `plc_id` / `station_id` | 来源 |
| `unit_id` | 受影响工件 |
| `reason_code` | PLC/HMI 定义原因 |
| `source` | `PLC`、`HMI`、`IMPORT` |
| `event_time` | 原始事件时间 |
| `payload JSONB` | 扩展信息 |

Edge 不决定何时 Hold 或 Release。`production_unit.current_state` 可以由追加事件投影为
`HELD`，但历史事件不可覆盖。

### Rework

Rework 必须由配置 feature flag 和 PLC/HMI 事件同时满足：

```text
features.rework_enabled = true
AND source event indicates rework
```

关闭时：

- Collector 仍可保存原始 sample。
- 不生成 Rework 路线投影。
- 记录 `FEATURE_DISABLED_EVENT_IGNORED` 诊断，不 ACK 与 Rework 无关的控制命令。

开启时建议事件：

- `REWORK_REQUESTED`
- `REWORK_STARTED`
- `REWORK_COMPLETED`
- `REWORK_FAILED`
- `REWORK_ROUTE_ENTERED`

Rework 不应通过改写原始 `station_event` 实现；应追加事件，并通过
`unit_relation(REWORK_OF)` 或 route event 表达轮次。

## 8. OEE 数据模型边界

OEE 需要明确计划时间和设备状态，不能只用 cycle 数估算完整 OEE。

推荐后续逻辑实体：

- `production_calendar` / `shift_calendar`
- `planned_stop`
- `equipment_state_event`
- `ideal_cycle_time_config`
- `oee_fact_hourly` 或查询视图

计算层级：

```text
Edge Node → Line → Station → Shift/Hour → Product/Order（后续）
```

Availability、Performance、Quality 的源事件必须可追溯。没有计划生产时间或可靠状态
事件时，Dashboard 应显示“数据不足”，不能伪造完整 OEE。

## 9. 查询、聚合与隔离

### 9.1 Boot isolation

- by-cycle 查询必须要求或解析 `line_id/plc_id/station_id/plc_boot_id/cycle_counter`。
- 未指定 boot 时只能选择明确的当前 boot，并在响应中返回选择依据。
- 跨 boot 聚合必须显式分组或过滤，不能把相同 counter 合并。

### 9.2 Profile isolation

- `profile` 必须在 cycle 事实中可直接查询，或通过不可歧义的 boot snapshot 关联。
- OEE、Quality 和 CT 默认使用 `normal`。
- `fast/test/unknown/All` 必须由调用方显式选择；多 Profile 返回 `MIXED` 元数据。

### 9.3 时间窗查询

- 所有列表和聚合 API 必须要求有界时间窗。
- 默认窗口建议不超过 8 小时；最大同步查询窗口建议 31 天。
- 更大窗口或报告导出走异步任务/预聚合，不允许无界全表扫描。
- 时间字段明确区分 PLC event time、Edge received time 和 DB created time。

### 9.4 Station-level aggregation

按 `line_id + station_id + profile + time_bucket` 聚合：

- throughput、OK/NOK/SKIPPED。
- cycle time p50/p95/p99。
- NOK rate、FPY/pass rate。
- ACK failure、collector latency、data freshness。

### 9.5 Line-level aggregation

整线产出不能固定使用 WS03。必须读取当时生效配置的 terminal station 或产品路线。
多 terminal station 时按 route/product 口径分别计算，再按合同定义汇总。

## 10. 索引建议

首批逻辑索引：

```text
cycle_event:
  UNIQUE(line_id, plc_id, station_id, plc_boot_id, cycle_counter)
  (line_id, plc_end_time DESC)
  (line_id, station_id, plc_end_time DESC)
  (line_id, unit_id, plc_end_time)
  (line_id, profile, plc_end_time DESC)

station_event:
  (line_id, unit_id, event_time)
  (line_id, station_id, event_time DESC)

quality_event:
  (line_id, event_time DESC)
  (line_id, station_id, nok_code, event_time DESC)
  (line_id, unit_id, event_time)

raw_plc_sample:
  (line_id, plc_id, station_id, sample_time DESC)
```

JSONB 只对已证明高频使用的路径建立表达式或 GIN 索引。禁止“先给整个 payload 建 GIN”
替代查询设计；每个新增 JSONB 索引都要有查询计划和写入成本证据。

## 11. 数据保留策略

建议分层：

| 数据 | 热数据建议 | 后续处理 |
| --- | --- | --- |
| 配置、审计、cycle/station/quality/hold/rework | 长期保留 | 按月分区或归档 |
| 聚合事实 | 长期保留 | 可重算但保留口径版本 |
| raw decoded payload | 30~90 天 | 冷归档后可按 event_id 恢复 |
| 原始 bytes/高频诊断 | 7~30 天 | 按容量和故障调查策略 |
| Collector error/metrics | 30~90 天 | Prometheus retention 独立管理 |

实际天数必须以 SSD 容量、每日事件量、payload 大小和客户审计要求计算。删除策略必须先
确保 Trace 报告仍能声明证据是否已归档。

## 12. 当前兼容方案

- WS01、WS02、WS03 继续写共享 `cycle_event/station_event`。
- 当前硬编码 `WS03` 终站判断在实施 Sprint 中改为读取配置；本合同只记录目标。
- DB101/102/103 和 DB104 不变。
- DB100 legacy 表和 dashboard 保留，标记为 compatibility path。
- 新的配置表先作为发布配置镜像，不立即替代 YAML。
- API 可先增加 `line_id` 参数和动态 station 列表，再逐步移除固定三站响应结构。

## 13. 禁止事项

- 禁止创建 `ws01_event`、`ws02_event`、`ws03_event` 等独立业务表。
- 禁止根据工站名称决定工艺逻辑。
- 禁止由 Edge 根据测量值自行产生 Hold、Rework、Skip 或 NOK 决策。
- 禁止在没有稳定 `unit_id` 或明确关系事件时猜测 Genealogy。
- 禁止在合同未更新前实施数据库 migration 或公共 API 破坏性变更。

## 14. 验收条件

- 逻辑模型可表达 WS01~WS20+、多 PLC、Buffer 和未来多产线。
- 固定查询维度使用关系列，工站特有 payload 使用 JSONB。
- 当前 WS01/WS02/WS03 不需要独立表即可兼容。
- `station_type`、payload schema 和 NOK template 有版本化发布镜像。
- cycle/station/quality/hold/rework 的关联键和来源证据明确。
- boot/profile/time-window isolation 可由索引和 API 合同执行。
- production outcome、defect detail 与 Pareto completeness 遵守
  `station_event_model.md` 的唯一投影规则。
- station-level 与 line-level 聚合不依赖 WS03 硬编码。
- 保留策略区分事实、payload、raw bytes 和 metrics。
- Hold/Rework 是追加事件，不覆盖原始 cycle/station event。
- Genealogy 关系有来源事件，不依赖时间猜测。
- 实施 Thread 可据此编写 migration 计划，但本合同本身不包含或执行 migration。
