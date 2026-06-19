# Dynamic Station Model Contract

更新时间：2026-06-19  
状态：下一阶段逻辑数据模型，尚未实施、未创建 migration  
适用范围：动态产线、工站、Buffer、PLC mapping、Trace、Quality 和 OEE

## 1. 目的

本合同定义下一阶段建议的数据实体、主键、共享事件模型和 JSONB 边界。本文只冻结
逻辑模型，不修改当前数据库，不提供 migration。

## 2. 核心决策

1. 使用共享事件表，不为 WS01、WS02、WS03 或未来 WS04~WS15 创建独立业务表。
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

所有新查询必须以 `line_id` 作为首要过滤维度。推荐逻辑唯一性：

```text
PLC event identity:
line_id + plc_id + station_id + plc_boot_id + cycle_counter

Station instance:
line_id + station_id

Unit identity:
line_id + unit_id
```

当前 `production_unit.unit_id` 是单列主键。进入真实多产线前，应先确认 `unit_id`
是否全局唯一；若不能保证，下一阶段 migration 应改为复合唯一约束或引入内部
`unit_pk`。本次规划不执行该 migration。

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

## 9. 当前兼容方案

- WS01、WS02、WS03 继续写共享 `cycle_event/station_event`。
- 当前硬编码 `WS03` 终站判断在实施 Sprint 中改为读取配置；本合同只记录目标。
- DB101/102/103 和 DB104 不变。
- DB100 legacy 表和 dashboard 保留，标记为 compatibility path。
- 新的配置表先作为发布配置镜像，不立即替代 YAML。
- API 可先增加 `line_id` 参数和动态 station 列表，再逐步移除固定三站响应结构。

## 10. 禁止事项

- 禁止创建 `ws01_event`、`ws02_event`、`ws03_event` 等独立业务表。
- 禁止根据工站名称决定工艺逻辑。
- 禁止由 Edge 根据测量值自行产生 Hold、Rework、Skip 或 NOK 决策。
- 禁止在没有稳定 `unit_id` 或明确关系事件时猜测 Genealogy。
- 禁止在合同未更新前实施数据库 migration 或公共 API 破坏性变更。

## 11. 验收条件

- 逻辑模型可表达 1~N 工站、多 PLC、Buffer 和多产线。
- 固定查询维度使用关系列，工站特有 payload 使用 JSONB。
- 当前 WS01/WS02/WS03 不需要独立表即可兼容。
- Hold/Rework 是追加事件，不覆盖原始 cycle/station event。
- Genealogy 关系有来源事件，不依赖时间猜测。
- 实施 Thread 可据此编写 migration 计划，但本合同本身不包含或执行 migration。
