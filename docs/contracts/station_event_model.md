# Generic Station Event Model Contract

状态：Sprint 2 planning contract revision；Reliability N8 定向复验
`PASS WITH RECOMMENDATIONS`，N8 CLOSED；implementation 尚未开始

更新时间：2026-06-21

适用范围：Phase-2 Sprint 2 Generic Station Event Model

## 1. 设计目标

本合同冻结一个独立、通用、可验证的工站事件表示，作为后续 V-PLC、Collector、DB、
API 与 Dashboard 接入的共同语义基础。

Sprint 2 MVP 应做到：

- 用同一 envelope 表达不同工站类型的周期、结果、NOK 与 Skip 事实。
- 保留 PLC 事实、配置血缘、boot/profile 隔离和原始数据追溯。
- 对 envelope 严格校验，对受控 payload 做有边界扩展。
- 提供稳定 canonical JSON，支持快照比较、确定性 event identity 和测试。
- 不反向修改 Sprint 1 `line_configuration` 合同。

## 2. 非目标与控制边界

- PLC 仍是设备控制大脑。
- HMI / PLC 决定 Hold、Release、Rework、Skip、Manual NOK 和现场放行。
- Edge 只采集、解析、校验、存储、追溯、计算和展示事实。
- Edge 不根据测量值阈值自行将 OK 改为 NOK。
- Sprint 2 planning 不接入 V-PLC、Collector、DB、API 或 Dashboard。
- Sprint 2 MVP 不做 migration、runtime adapter、远程部署或 rollback drill。
- 不创建 per-station 业务模型或 `ws01_event` 一类专用表。

## 3. Event envelope

建议 canonical envelope：

```json
{
  "schema_version": "1.0",
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "station_result",
  "event_ts": "2026-06-20T10:15:30.123Z",
  "line_id": "LINE-01",
  "plc_id": "PLC-01",
  "station_id": "WS02",
  "station_type": "screw",
  "config_version": "2026.06.20-1",
  "config_hash": "50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1",
  "plc_boot_id": "01J10C2SZM4T2R8K6V2YDR45VH",
  "profile_id": "normal_screwdriving",
  "cycle_id": "LINE-01/PLC-01/WS02/01J10C2SZM4T2R8K6V2YDR45VH/42",
  "cycle_counter": 42,
  "unit_id": "UNIT-000042",
  "dmc": "DMC-000042",
  "result": "ok",
  "source": "vplc",
  "actor": "simulator",
  "payload": {
    "torque_nm": 4.8,
    "angle_deg": 132.5
  },
  "correlation": {
    "source_event_id": "PLC-01:WS02:42:result",
    "fact_key": "sha256:b08052bccb4d32c97b2c5da96540cb7a64f1a63a9bcedc7e0c418a9bc6542b7e",
    "event_role": "production_result",
    "mapping_id": "ws02_result",
    "payload_template": "screw_result_v1"
  }
}
```

`created_at` 不属于 source canonical envelope。它由未来的存储层生成，不能覆盖
`event_ts`。

## 4. MVP 通用字段与逐事件字段矩阵

所有 Sprint 2 MVP event 的 common required fields：

| 字段 | 类型 | 来源 | 语义 |
| --- | --- | --- | --- |
| `schema_version` | string | model | envelope 合同版本，MVP 为 `1.0` |
| `event_id` | string | source 或 normalizer | 单事件不可变 ID |
| `event_type` | enum | PLC/V-PLC 事实映射 | 事件语义 |
| `event_ts` | RFC 3339 UTC string | PLC/V-PLC source | source fact / heartbeat observation 时间 |
| `line_id` | string | resolved line config | 产线身份 |
| `plc_id` | string | resolved line config | PLC 身份 |
| `station_id` | string | resolved line config | 工站身份 |
| `station_type` | string | resolved line config snapshot | 事件发生时工站类型 |
| `config_version` | string | resolved line config | 配置可读版本 |
| `config_hash` | 64-char lowercase hex | resolved line config | resolved config SHA-256 |
| `source` | enum | authority context | 原始事实权威；不是传输/ingress 通道 |
| `actor` | enum | source metadata | 触发事实的主体 |
| `correlation` | object | source/normalizer | 确定性追溯信息 |

### 4.1 通用 required fields

五类 MVP event 都必须包含第 4 节表中的通用字段。`correlation` 必须符合第 12 节
strict schema，且至少包含稳定的 `source_event_id`、`fact_key` 和 `event_role`。

以下是 common optional fields，不属于 common required：

| 字段 | 规则 |
| --- | --- |
| `payload` | optional；存在时必须是第 11 节定义的 normalized JSON object，禁止 null |
| `raw_payload` | optional；存在时必须是 JSON object 或 UTF-8 string，禁止 null |
| `observed_at` | optional；Collector/observer 首次观察时间，必须为 UTC `Z` timestamp |

### 4.2 Per-event required / optional / forbidden matrix

`common` 表示第 4 节 common required fields。除 optional 列明确允许的字段外，其余
事件专用字段均 fail closed。

| `event_type` | required | optional | forbidden / not applicable |
| --- | --- | --- | --- |
| `station_cycle_start` | common、`plc_boot_id`、`profile_id`、`cycle_id`、`cycle_counter` | `unit_id`、`dmc`、`payload`、`raw_payload`、`observed_at` | `result`、`nok_code`、`nok_origin`、`diagnostic_context`、`correlation.parent_event_id`、全部 upstream evidence fields、`created_at` |
| `station_cycle_complete` | common、`plc_boot_id`、`profile_id`、`cycle_id`、`cycle_counter` | `unit_id`、`dmc`、`payload`、`raw_payload`、`observed_at` | `result`、`nok_code`、`nok_origin`、`diagnostic_context`、`correlation.parent_event_id`、全部 upstream evidence fields、`created_at` |
| `station_result` | common、`plc_boot_id`、`profile_id`、`cycle_id`、`cycle_counter`、`result` | `unit_id`、`dmc`、`payload`、`raw_payload`、`observed_at`；`result=nok` 时 `nok_code/nok_origin` conditional required | `diagnostic_context`、`correlation.parent_event_id`、全部 upstream evidence fields、`created_at` |
| `station_nok` | common、`plc_boot_id`、`profile_id`、`cycle_id`、`cycle_counter`、`nok_code`、`nok_origin`、`correlation.parent_event_id`、`correlation.parent_fact_key`、`correlation.detail_role` | `unit_id`、`dmc`、`payload`、`raw_payload`、`observed_at`；仅 code `30003` 时 `correlation.upstream_evidence` conditional required | `result`、`diagnostic_context`、`created_at` |
| `station_heartbeat` | common、`plc_boot_id`、`diagnostic_context` | `result=unknown/not_applicable`、`profile_id`、`payload`、`raw_payload`、`observed_at` | `cycle_id`、`cycle_counter`、`unit_id`、`dmc`、`nok_code`、`nok_origin`、`correlation.parent_event_id`、全部 upstream evidence fields、`created_at` |

补充规则：

- `station_heartbeat` 是 diagnostic-only，不产生 cycle、unit、production result、OEE、
  Quality、FPY、NOK count 或控制投影。
- heartbeat 的 `correlation.source_event_id` 必须来自 PLC/V-PLC heartbeat sequence；
  禁止由 system/Collector/validator 以接收时间或随机数生成。
- MVP heartbeat 只接受 `plc/plc` 或 `vplc/simulator` authority。`plc_boot_id` 必须来自
  被观察的 PLC/V-PLC/simulator 明确 source fact；system 不得伪造、继承或猜测该值。
- disabled station 只允许 `station_heartbeat`，且
  `diagnostic_context.category=disabled_station`；禁止周期、结果和 NOK 事件。
- future event type 不属于 Sprint 2 validator accepted enum，即使第 7 节保留了词汇。

### 4.3 Presence、absent、null 与 forbidden

MVP presence 规则固定为：

| 字段状态 | 输入 | 结果 |
| --- | --- | --- |
| required | missing | reject：`REQUIRED_FIELD_MISSING` |
| required | explicit null | reject：`FIELD_NULL_FORBIDDEN` |
| optional | absent | accept |
| optional | explicit null | reject，除非本合同逐字段明确允许 null；当前 envelope 无此例外 |
| forbidden | absent | accept |
| forbidden | present，包括 explicit null | reject：`FIELD_FORBIDDEN` |

- absent 表示 key 完全不存在；不得把 explicit null 静默转换为 absent。
- canonical source envelope 省略所有 absent optional fields。
- `created_at` 在所有 source envelope 中 forbidden；未来 DB projection 可在 envelope
  外部增加该存储字段。
- 第 3 节 canonical example 是必须通过上述规则的 positive fixture。

## 5. MVP 可选字段与延后字段

| 字段 | MVP 状态 | 规则 |
| --- | --- | --- |
| `unit_id` | optional | 已有稳定 unit identity 时填写 |
| `dmc` | optional | PLC/HMI 提供的 DMC；不能由时间猜测 |
| `payload` | optional | normalized JSON object；存在时禁止 null |
| `nok_code` | conditional | `result=nok` 或 `event_type=station_nok` 时必需 |
| `nok_origin` | conditional | NOK 事件/结果的受控来源；普通非 NOK 事件禁止携带 |
| `raw_payload` | optional | 原始 JSON object 或 UTF-8 text 的有界表示；binary 延后 |
| `diagnostic_context` | heartbeat required | strict diagnostic object；仅 heartbeat 使用 |
| `observed_at` | optional, Collector-only | Collector 实际观察时间；未来 adapter 使用 |
| `created_at` | deferred, DB-only | 存储层生成，不参与 source canonical JSON |
| `route_id` / `route_step` | deferred | Sprint 2 不实现 route execution |
| Hold/Rework relation fields | deferred | 后续合同增量定义 |

`unit_id`、`dmc`、`cycle_id` 不是可互换字段。`cycle_id` 标识一次工站周期；
`unit_id` 标识 MES 工件实体；`dmc` 是现场可读/可扫描身份。

## 6. 字段类型与基本语义

- ID 字段必须是非空、trim 后不变的 UTF-8 string，最大 128 字符。
- `event_id` 必须是 UUIDv4 并唯一标识 accepted MVP envelope；MVP 不依赖 DB 自增 ID。
- UUIDv4 只作为 envelope identity，不承担事实幂等。
- UUIDv5 仅允许作为不进入 validator 的 deterministic snapshot/helper identity；需要通过
  accepted-event validator 的 fixtures 必须使用固定 UUIDv4。validator 不依赖外部
  `test_mode` 放宽 UUID version。
- 本轮不实现 UUID 生成；后续 helper 可提供 UUIDv4 默认生成。
- serializer 不得重新生成或改写已有 `event_id`。
- `cycle_counter` 是 `0..2^63-1` integer，禁止 boolean 和 float。
- `nok_code` 是正 integer，禁止 string、boolean 和 float；与 Sprint 1 `NokCode.code`
  类型一致。
- `profile_id` 使用 Sprint 1 resolved station 的 `cycle_profile` 引用值，例如
  `normal_screwdriving`；它不是 `mode=normal/fast/test/stress`。
- 若 future 需要保存 profile mode，必须增加独立 `profile_mode` 字段和合同；不得把
  mode 写入 `profile_id`。
- `result`、`source`、`actor` 和 `event_type` 使用小写 snake_case。
- 存在的 `payload` 与 required `correlation` 必须是 JSON object；不能是 array、scalar
  或 null。
- 数值禁止 NaN、Infinity 和 `-Infinity`。
- envelope 顶层未知字段 fail closed。

## 7. `event_type` 分层与投影角色

### 7.1 Sprint 2 MVP 必须支持

- `station_cycle_start`
- `station_cycle_complete`
- `station_result`
- `station_nok`
- `station_heartbeat`

五类 event 的固定投影角色：

| `event_type` | canonical role | 是否进入 production result / Quality 统计 |
| --- | --- | --- |
| `station_cycle_start` | 周期开始事实 | 否 |
| `station_cycle_complete` | 周期完成事实，不承载结果 | 否 |
| `station_result` | 唯一 canonical production result carrier | 是，每个 cycle 最多一个 accepted canonical result |
| `station_nok` | `station_result` 的 NOK/route detail companion | 否，不额外增加 outcome、NOK count、FPY 或 OEE Quality |
| `station_heartbeat` | diagnostic liveness fact | 否 |

`station_nok` 不能独立成为生产结果。它必须通过 `correlation.parent_event_id` 引用同一
`cycle_id` 的 canonical `station_result`：

- 普通 NOK detail 的 parent 必须为 `station_result(result=nok)`。
- `30003 UPSTREAM_NOK_SKIPPED` 的 parent 必须为 `station_result(result=skip)`。
- 两者的 line/plc/station/boot/counter/cycle、unit/DMC（若存在）必须一致。
- parent `station_result(result=nok)` 的 `nok_origin` 必须与普通 detail 一致。
- parent 的单数 `nok_code` 是 canonical primary defect code。
- 普通 `station_nok` 必须显式设置 `correlation.detail_role=primary/secondary`：
  - primary：`nok_code/nok_origin` 必须与 parent 完全一致；每个 parent 最多一个。
  - secondary：`nok_code` 必须不同于 parent primary code，`nok_origin` 必须与 parent
    一致，且 state index 中必须已经存在 accepted primary detail；可有多个不同 code。
- `30003` 固定使用 `correlation.detail_role=system_reserved`，不属于普通 primary/
  secondary defect set；每个 skip parent 最多一个。
- `station_result(result=nok)` 本身已是完整 canonical outcome，不要求最终一定出现
  `station_nok`。若出现普通 detail，必须先 primary 后 secondary；MVP 不需要 batch
  finalization 或“最终至少一个 detail”集合断言。
- required parent 字段缺失、parent 未找到、跨 cycle 或内容不匹配一律 reject；只有同一
  业务唯一槽位已经有 accepted event 且 fingerprint 不同时才是 conflict。
- DB/API/Dashboard future projection 只以 accepted `station_result` 作为 production
  result、Quality、FPY 和 NOK outcome 的统计入口；`station_nok` 仅进入 detail/Pareto
  evidence 投影，并且 `30003` 必须排除 Quality NOK/Pareto。
- 普通 NOK Pareto 指标固定命名为 `defect_detail_count`：统计 accepted、distinct
  `station_nok_detail_key` 的 primary + secondary、non-system-reserved defect details。
  相同 detail duplicate 不增加计数；一个 NOK unit/cycle 可贡献多个 defect details。
  `NOK unit/cycle count` 只由 canonical `station_result(result=nok)` 计算，不得与
  `defect_detail_count` 混用。

### 7.2 Sprint 2 可定义、但 MVP 不实现 adapter

- `station_skip`
- `station_fault`
- `buffer_enter`
- `buffer_exit`

这些名称仅冻结词汇和未来兼容性。本轮不定义运行触发、DB 投影或 Dashboard 指标。
`station_skip` 延后是为了避免在 Sprint 2 绑定 PLC/HMI route decision；Buffer event
延后是为了避免过早绑定 route graph 与 `tracking_mode` runtime。

### 7.3 后续 Sprint 延后

- `station_hold`
- `station_release`
- `station_rework`

Hold/Release/Rework 必须由 PLC/HMI 明确产生，需独立业务合同、状态投影与关系模型；
不能因本合同预留名称而视为已实现。

## 8. `result`、status 与 NOK 语义

MVP `result` 枚举：

- `ok`
- `nok`
- `skip`
- `unknown`
- `not_applicable`

本合同不另设含义重叠的通用 `status`。设备状态、处理状态和验证状态以后使用明确命名
字段，避免将 `running`、`accepted`、`ok` 混入同一枚举。

合法组合：

| `event_type` | 允许的 `result` | `nok_code/nok_origin` | diagnostic rule |
| --- | --- | --- | --- |
| `station_cycle_start` | absent | absent | absent |
| `station_cycle_complete` | absent | absent | absent |
| `station_result` | required: `ok/nok/skip/not_applicable` | 仅 `nok` 时 required；其他 result forbidden | absent |
| `station_nok` | absent | required | absent；必须关联 canonical result |
| `station_heartbeat` | absent / `unknown` / `not_applicable` | absent | `diagnostic_context` required |

规则：

- `result=nok` 必须有在工站 NOK template 中可解释的 `nok_code`。
- `result=nok` 与 `station_nok` 必须有 `nok_origin`。
- 非 NOK result 禁止携带普通 NOK code。
- `30003` 固定表示 `UPSTREAM_NOK_SKIPPED`，mode 为 `system_reserved`。
- `30003` 只能与 `nok_origin=system_reserved` 组合。
- MVP 中 `30003` 是 system-reserved、detail-only 的 route diagnostic。只有第 12.1 节
  strict upstream business evidence 已解析为 accepted upstream NOK fact 时，才能使用
  `UPSTREAM_NOK_SKIPPED` 名称；其当前站 parent 必须为
  `station_result(result=skip)`。
- `30003` 禁止用于 random、forced、simulator、plc 或 future manual NOK。
- `30003` 不是现场工艺缺陷、operator/process defect 或 business NOK outcome；不产生
  production result、Quality、FPY、NOK unit/cycle count 或 defect Pareto。
- `validation_failure/malformed_payload/rejected_payload/missing_required_field/
  payload_limit_exceeded/schema_error/parse_error` 以及 timeout、ACK、config、clock、
  counter、storage 等技术失败只能形成 reject/disposition 或 future technical
  diagnostic；不得自动生成 `30003`、business NOK、production outcome 或 Skip
  attribution。
- 缺少、无法解析或不匹配 upstream business evidence 时，
  `station_nok(30003)` 在 MVP 必须 reject；不得降级为 accepted diagnostic station
  event，不得凭空生成 production attribution。
- global NOK fallback 和 station-level NOK override 只决定 V-PLC 仿真生成概率；事件合同
  记录已发生事实，不重新计算 NOK。
- `nok_origin` 是独立业务语义字段，不得放入 `correlation`。
- MVP `nok_origin` accepted enum 为
  `random/forced/plc/system_reserved/simulator`。
- `manual/hmi/operator/unknown` 保留为 future vocabulary，不进入 Sprint 2 validator
  accepted enum。
- `correlation` 只承担 trace / event 关联，不承担 NOK 来源语义。
- forced/random/simulator/plc 等 origin 只解释已发生事实；Edge 不据此改写 result。
- 缺失或 malformed result 必须拒绝，不能静默映射为 `unknown`。
- `unknown` 只允许 `station_heartbeat`，且必须有可验证的 `diagnostic_context`。
- `station_result` 与 `station_cycle_complete` 一律禁止 `unknown`；fixture/test mode
  不能放宽业务组合。
- future fault/incomplete event 必须先定义独立 event contract 和可验证字段，不能通过
  validator 外部布尔开关绕过本合同。

### 8.1 Diagnostic context strict schema

`diagnostic_context` 只允许以下字段：

| 字段 | 状态 | 规则 |
| --- | --- | --- |
| `category` | required | 见下方 accepted enum 与 authority mapping |
| `reason_code` | required | ASCII 小写 snake_case，正则 `^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$`，1~64 UTF-8 bytes |
| `message` | optional | UTF-8 string，最大 256 bytes，不得含凭据或个人数据 |
| `incomplete_reason` | conditional | `category=source_incomplete` 时 required；非空 UTF-8 string，最大 128 bytes |

accepted category：

- source fact diagnostic：`heartbeat/source_incomplete/clock_anomaly/disabled_station`。

heartbeat 使用 `result=unknown` 时：

- `source=plc/vplc` 只允许
  `source_incomplete/clock_anomaly/disabled_station`。
普通 heartbeat 可省略 result 或使用 `not_applicable`。未知字段、缺失 reason、空
`incomplete_reason` 或不合法 source/category 组合全部 reject。

## 9. `source`、`actor`、`event_type` 与 `nok_origin` authority matrix

MVP accepted `source`：

- `plc`
- `vplc`
- `system`

MVP accepted `actor`：

- `plc`
- `simulator`
- `system`

validator 必须逐行 allow，未列出的组合一律 reject：

| `event_type` | allowed `source` | allowed `actor` | allowed `nok_origin` | notes |
| --- | --- | --- | --- | --- |
| `station_cycle_start` | `plc` | `plc` | absent | PLC 现场周期事实 |
| `station_cycle_start` | `vplc` | `simulator` | absent | 仿真周期事实 |
| `station_cycle_complete` | `plc` | `plc` | absent | 只表达周期完成 |
| `station_cycle_complete` | `vplc` | `simulator` | absent | 只表达周期完成 |
| `station_result` | `plc` | `plc` | result=nok 时必须为 `plc`；其他 result 必须 absent | canonical result |
| `station_result` | `vplc` | `simulator` | result=nok 时必须为 `random/forced/simulator`；其他 result 必须 absent | canonical simulated result |
| `station_nok` | `plc` | `plc` | 仅 `plc` | 普通 production defect detail；必须引用 canonical NOK result |
| `station_nok` | `vplc` | `simulator` | `random/forced/simulator` | 普通 simulated defect detail；必须引用 canonical NOK result |
| `station_nok` | `system` | `system` | 仅 `system_reserved` 且 code 必须为 `30003` | 仅有 strict upstream evidence 时允许；引用 canonical skip result；diagnostic/quarantine-style detail |
| `station_heartbeat` | `plc` | `plc` | absent | diagnostic-only |
| `station_heartbeat` | `vplc` | `simulator` | absent | diagnostic-only |

硬边界：

- Collector 可以观察、规范化和传输 envelope，但不得把 `source/actor` 改写为
  `collector`，也不得作为五类 MVP event 的 authority。ingestion、validation、
  quarantine 元数据属于 future technical event contract。
- `system` 只能产生表中明确的 diagnostic、reserved 或 internal 语义；不得产生
  `ok/nok` 现场结果，不得伪装 PLC。
- `nok_origin=system_reserved` 与 `nok_code=30003` 双向绑定：任一出现时另一项必须出现。
- `system_reserved/30003` 必须存在 `correlation.upstream_evidence`；缺失、state index
  不可用、证据未找到或证据不匹配时均 reject。
- V-PLC `nok_origin=forced` 只表示测试队列执行模式，`actor` 仍为 `simulator`；它不表示
  operator authority。未来请求者审计使用独立 metadata。
- `manual_import`、`api`、`hmi`、`operator`、manual NOK 均为 future/non-MVP；Sprint 2
  validator 必须拒绝。后续接入需增加 evidence 字段和独立 authority review。

### 9.1 Heartbeat authority

- `station_heartbeat` 永远 diagnostic-only；不得伪造或替代 cycle start、cycle complete、
  station result、NOK detail 或现场控制事实。
- MVP 只接受 PLC heartbeat (`source=plc, actor=plc`) 和 V-PLC heartbeat
  (`source=vplc, actor=simulator`)。
- heartbeat `event_ts` 是 PLC/V-PLC source observation timestamp，不是 cycle authority；
  heartbeat 不进入 cycle/result/NOK/OEE/Quality 统计。
- heartbeat `plc_boot_id` 必须由同一 PLC/V-PLC source 明确提供。system、Collector、
  validator 或 storage 不得创建或猜测 PLC boot identity。
- system/Collector/validator/config/storage health 进入 future technical diagnostic
  contract；不使用 Sprint 2 `station_heartbeat`。

## 10. 与 line configuration / `config_hash` 的关联

- 每个有效 MVP station event 必须携带 `config_version` 和 `config_hash`；正常生产事件
  不允许缺失。
- `line_id`、`plc_id`、`station_id`、`station_type` 必须与该 hash 对应的 resolved config
  一致。
- `station_id` 必须存在且属于 `plc_id`；`station_type` 必须匹配配置快照。
- disabled station 不能产生正常周期事实，只允许第 4.2/8.1 节定义的 diagnostic
  heartbeat。
- Buffer event 必须匹配 Buffer `enabled` 与 `tracking_mode`，但 Buffer adapter 延后。
- cycle/result/NOK event 的 `profile_id` 必须等于该 station 在 resolved config 中引用的
  `cycle_profile` ID；heartbeat 的 optional `profile_id` 若存在也必须如此校验。
- mapping/template identity 放入 `correlation`，用于追溯 DB mapping 与 payload schema。
- hash 缺失：MVP model validation 失败。
- `config_hash` 格式固定为 64 位 lowercase SHA-256 hex。
- hash 格式合法但 resolved config lookup 不存在：MVP reject `CONFIG_NOT_FOUND`；不得
  defer、猜测或套用当前配置。
- hash 与 identity mismatch：MVP reject `CONFIG_HASH_MISMATCH`，不得重写 source fact。
  future Collector 可在独立 runtime contract 中 quarantine rejected envelope。
- Sprint 2 MVP 只实现离线 model/config correlation 校验，不实现 runtime config registry。

## 11. `payload` / `raw_payload` 资源合同

### 共同 JSON 安全规则

- 大小按 canonical compact JSON 的 UTF-8 encoded bytes 计算；string 型 raw payload
  按其 UTF-8 encoded bytes 计算。
- 只允许 JSON 值：string、finite number、boolean、null、object、array。
- 禁止 Python/语言原生 bytes、binary blob、自定义对象、set/tuple、循环引用、NaN、
  Infinity、图片、无界日志、凭据、secret、token 和未脱敏个人数据。
- 最大嵌套深度为 6（root object 计为第 1 层）。
- 单个 object 最多 64 keys；整个 payload tree 最多 128 keys。
- key 必须是 UTF-8 string，最大 64 bytes。
- array 最多 128 items。
- normalized payload 单个 string value 最大 4096 UTF-8 bytes。
- validator 必须先做有界、循环安全的结构遍历，再做 canonical serialization 和总大小
  检查；不得靠序列化异常兜底。

### Normalized payload

- 必须是 JSON object。
- canonical UTF-8 JSON 最大 16 KiB（16384 bytes）。
- payload template 已声明字段按 template 严格校验。
- template 未声明的字段默认拒绝；显式 `extensions` object 可作为受控扩展槽。
- torque、angle、pressure、test value 等工站特有测量值放在 payload。
- 单位应编码在 schema/template 中，不在字段名中任意漂移。

### Raw payload

- MVP 只允许 JSON object 或 UTF-8 string；不支持 bytes、binary 或 base64。
- `raw_payload` 存在时 `correlation.raw_encoding` conditional required：
  object 必须为 `json`，string 必须为 `utf8_text`。
- raw JSON object 沿用深度/key/array 限制，单个 nested string value 最大 16384 UTF-8
  bytes；顶层 UTF-8 text 只受 64 KiB 总上限约束。
- canonical/UTF-8 表示最大 64 KiB（65536 bytes）。
- 不得包含凭据、密钥或未脱敏个人数据。
- raw 与 normalized 必须通过同一 `event_id`、mapping/template version 追溯。
- raw 不参与业务 result 决策；它是审计与重放证据。
- `raw_payload` 不得替代 normalized payload。
- binary/base64/image encoding 延后到 future contract；必须同时定义 decoded/encoded
  双重上限后才能接入。
- MVP 对 payload 或 raw payload 超限直接 reject；future runtime 可在独立合同中改为
  quarantine，但不得静默截断。

## 12. Correlation、时间、顺序与幂等

### 12.1 Correlation strict schema

`correlation` 只允许：

| 字段 | 状态 | 规则 |
| --- | --- | --- |
| `source_event_id` | required | source 在 retry/replay 间稳定复用的 1~128 byte ID |
| `fact_key` | required | `sha256:<64 lowercase hex>` |
| `event_role` | required | 与 event type 固定映射：`cycle_start/cycle_complete/production_result/nok_detail/heartbeat` |
| `mapping_id` | optional | 必须匹配同 config hash 的 mapping |
| `payload_template` | conditional | payload 非空时 required，并匹配同 config hash |
| `raw_encoding` | conditional | raw 存在时 required：`json/utf8_text` |
| `parent_event_id` | station_nok required | UUID，必须引用同 cycle canonical station_result |
| `parent_fact_key` | station_nok required | 必须等于 parent canonical station_result 的 `fact_key` |
| `detail_role` | station_nok required | `primary/secondary/system_reserved` |
| `upstream_evidence` | code `30003` required | 第 12.1.1 节 strict object；其他事件 forbidden |

未知 correlation field fail closed。

#### 12.1.1 Upstream business evidence strict schema

`correlation.upstream_evidence` 只允许：

| 字段 | 状态 | 规则 |
| --- | --- | --- |
| `evidence_type` | required | `canonical_station_result/validated_nok_detail` |
| `source_event_id` | required | cited PLC/V-PLC source fact identity，1~128 UTF-8 bytes |
| `parent_event_id` | required | cited accepted upstream event UUIDv4 |
| `parent_fact_key` | required | cited accepted upstream event `fact_key` |
| `upstream_station_id` | required | 当前 station 的 direct enabled predecessor |
| `upstream_plc_id` | required | cited upstream PLC identity |
| `upstream_plc_boot_id` | required | cited source boot identity |
| `upstream_event_type` | required | 与 evidence type 固定匹配的 `station_result/station_nok` |
| `upstream_result` | required | 固定为 `nok`；按 evidence type 与 cited result 或其 canonical parent 比较 |
| `upstream_nok_code` | required | cited positive integer NOK code；不得为 `30003` |
| `upstream_config_hash` | required | 与当前 event 相同的 64-char lowercase SHA-256 |

证据解析与 comparison 必须按 `evidence_type` 分开执行：

| `evidence_type` | cited record | `upstream_result` 比较对象 | 必须满足 |
| --- | --- | --- | --- |
| `canonical_station_result` | accepted、`source=plc/vplc`、`event_type=station_result` | cited result 自身的 `result` | cited result 的 `result=nok`；其 event/source/fact/station/PLC/boot/code/config 与 evidence object 一致 |
| `validated_nok_detail` | accepted、`source=plc/vplc`、`event_type=station_nok`、`detail_role=primary/secondary` | cited detail 所绑定的 accepted canonical parent `station_result.result` | cited detail 自身必须没有 `result`；parent 的 `result=nok`；detail 与 parent 的 station/PLC/source authority/route/unit-DMC/boot/config/cycle-role 关系一致 |

`canonical_station_result` comparison：

- cited record 的 `event_id/fact_key/source_event_id/station/plc/boot/event_type/result/
  nok_code/config_hash` 必须与 evidence object 逐字段相等。
- `upstream_result` 必须等于 cited record 自身的 `result`，且固定为 `nok`。

`validated_nok_detail` comparison：

- cited detail 的 `event_id/fact_key/source_event_id/station/plc/boot/event_type/nok_code/
  config_hash` 必须与 evidence object 逐字段相等。
- cited detail 自身不得存在 `result`，包括 explicit null；若存在，按第 4.2/4.3 节
  `FIELD_FORBIDDEN` reject。
- state index 必须用 cited detail 的 `parent_event_id/parent_fact_key` 唯一解析到 accepted
  canonical `station_result`；parent 的 `result` 必须为 `nok`。
- evidence object 的 `upstream_result=nok` 与 canonical parent result 比较，不与 cited
  detail 自身比较。
- cited detail 的 canonical `nok_code/nok_origin/detail_role` 只证明 NOK detail 语义，
  不替代、不生成也不改写 canonical parent result。
- parent result 与 cited detail 必须属于同一 upstream station、PLC/V-PLC authority、
  `plc_boot_id`、`config_hash`、cycle role 和 subject identity；其 unit/DMC、route 与
  current skip event 仍须满足下方共同关联规则。

两种 evidence type 的共同关联规则：

- upstream station 必须是 resolved route 中当前 station 的 direct enabled predecessor；
  不允许用任意祖先、station order 或时间邻近推断。
- 上下游必须存在逐字节相同的 `unit_id` 或 `dmc`。若只有 `counter_only` 且无显式工件
  关联，MVP 不允许生成 `30003`。
- 同一 `plc_id` 时 upstream/current `plc_boot_id` 必须相同；跨 PLC 时各自 boot ID
  必须来自 cited source，但 boot ID 不单独证明工件关联。
- `validation_failure/malformed_payload/rejected_payload/missing_required_field/
  payload_limit_exceeded/schema_error/parse_error` 以及 Collector/validator/system record
  不是 upstream business evidence，不能出现在该 object 或支持 `30003`。
- evidence object 缺失、字段缺失、state index 不可用、record 未找到或任何字段不匹配：
  MVP 一律 reject；future async ingestion 才可在独立 runtime contract 中定义 defer/
  quarantine，但不得先接受或投影 `30003`。

#### 12.1.2 N8 official evidence examples

Positive — accepted `validated_nok_detail` evidence：

```text
cited detail:
  event_type=station_nok
  accepted=true
  result=absent
  detail_role=primary
  nok_code=20001
  nok_origin=plc
  parent_event_id=upstream-result-event-id
  parent_fact_key=upstream-result-fact-key

resolved canonical parent:
  event_type=station_result
  accepted=true
  result=nok
  nok_code=20001
  nok_origin=plc

upstream_evidence:
  evidence_type=validated_nok_detail
  upstream_event_type=station_nok
  upstream_result=nok
  upstream_nok_code=20001
```

当 cited detail、canonical parent、evidence object 与 current skip event 的
station/PLC-or-V-PLC/route/unit-or-DMC/boot/config/cycle-role 关系全部一致时，evidence
comparison 通过。这里 `upstream_result=nok` 比较的是 canonical parent result。

Negative 1 — detail 非法携带 result：

```text
cited station_nok detail contains result=nok
=> reject FIELD_FORBIDDEN at result
```

Negative 2 — detail parent 不是 NOK：

```text
cited detail is accepted and result is absent
resolved canonical parent is station_result(result=ok)
=> reject UPSTREAM_EVIDENCE_INVALID
```

Negative 3 — technical failure impersonation：

```text
malformed/rejected/schema/parse/validation/payload-limit failure
is supplied as evidence for 30003 / UPSTREAM_NOK_SKIPPED
=> reject UPSTREAM_EVIDENCE_INVALID
```

上述技术失败不得生成 business NOK、operator/process defect、production outcome、
Skip attribution 或 defect Pareto entry；`30003` 仍只占用 system-reserved detail slot。

### 12.2 时间与顺序

- production event 与 heartbeat 的 `event_ts` 都来自 PLC/V-PLC source fact/observation
  时间，必须是带 `Z` 的 RFC 3339 UTC。
- `observed_at` 由未来 Collector 填写，表示 Edge 首次观察时间。
- `created_at` 由未来 DB 生成，表示落库时间。
- 三种时间不可互相覆盖。
- `event_ts` 不得早于 `2000-01-01T00:00:00Z`。
- `observed_at` 存在时，`event_ts` 最多可晚于 `observed_at` 5 分钟；超出返回
  `EVENT_TS_FUTURE`，不得改写 source timestamp。无 observed_at 的离线 MVP 只做格式与
  下限校验；future runtime clock policy 另行定义。
- out-of-order event 允许进入验证/隔离流程；不得改写 `event_ts` 以制造顺序。
- 同 station/boot 内优先使用 `cycle_counter` 排序，时间作为辅助。
- `cycle_id` 推荐确定性格式：
  `line_id/plc_id/station_id/plc_boot_id/cycle_counter`。
- 同一 cycle 内事件角色顺序为 start → complete → production_result；`nok_detail` 关联
  production_result。该顺序用于一致性检查，不得用时间邻近推断缺失事件。

### 12.3 三类 identity

| identity | 职责 | 是否参与 production result uniqueness |
| --- | --- | --- |
| `event_id` | immutable envelope identity；runtime UUIDv4；retry/replay 必须复用 | 否 |
| `source_event_id` | upstream source identity；用于采集来源追溯和 source retry 对照 | 否 |
| `fact_key` | deterministic business fact identity；用于 duplicate/conflict 检测 | 是 |

- `event_id` 是不可变 envelope identity，可使用 UUIDv4。首次 normalizing 后必须持久
  复用；retry/replay 不得重新生成。
- UUIDv5 只用于 validator 外部的 deterministic helper/snapshot；UUIDv7 保持 future
  recommendation，均不承担业务幂等。
- `source_event_id` 是 source fact identity，所有 MVP event required。PLC/V-PLC 应优先
  使用 source 原生 sequence/identity；没有原生 ID 时必须由 source 按 boot-scoped
  event role/sequence 稳定生成，不能使用随机数或接收时间。
- `source_event_id` 不进入 production result 或 NOK detail 的 business uniqueness
  object；source 使用不同 ID 不能绕过业务去重。
- source 无原生 ID 时：
  - cycle start/complete/result/NOK 使用
    `line_id/plc_id/station_id/plc_boot_id/cycle_counter/event_role/<source sequence>`；
  - heartbeat 使用 source 持久化的 boot-scoped heartbeat sequence；
  - sequence 必须由 source 生成并跨 retry/replay 复用，normalizer 不得以接收时间替代。

### 12.4 Cycle-role 与 detail-set business uniqueness

`fact_key` 不单独承担 physical cycle-role uniqueness。stateful validator 必须另外构造：

```text
cycle_role_key =
(line_id, plc_id, station_id, plc_boot_id, cycle_counter, event_role)
```

适用规则：

| role | uniqueness |
| --- | --- |
| `cycle_start` | 每个 `cycle_role_key` 最多一个 accepted start |
| `cycle_complete` | 每个 `cycle_role_key` 最多一个 accepted complete |
| `production_result` | `production_result_key = cycle_role_key`；最多一个 accepted canonical result |
| `nok_detail` | 不使用 cycle role slot；使用下方 detail key |
| `heartbeat` | diagnostic-only，不创建 production cycle role |

- `cycle_role_key` 明确排除 `cycle_id/config_hash/config_version/unit_id/dmc/source_event_id`。
  这些字段属于 content consistency；同一 physical boot/counter/role 下出现不同值必须
  由 content fingerprint 判为 conflict，不能创建第二个 accepted role。
- disabled station diagnostic heartbeat 不创建任何 production cycle role。

NOK detail keys：

```text
station_nok_detail_key =
(parent_fact_key, detail_role, nok_code, nok_origin)

primary_nok_detail_key =
(parent_fact_key, "primary")

system_reserved_detail_key =
(parent_fact_key, "system_reserved")
```

- 每个 `station_nok_detail_key` 最多一个 accepted detail。
- 每个 `primary_nok_detail_key` 最多一个 accepted primary。
- secondary 可有多个不同 `nok_code`，但必须已有 accepted primary；相同 detail key
  fingerprint 相同为 duplicate，不同为 conflict。
- 每个 `system_reserved_detail_key` 最多一个 accepted `30003` detail。

### 12.5 Fact key canonical byte algorithm

`fact_key` 格式固定为 `sha256:<64 lowercase hex>`。计算步骤：

1. 按 event role 构造下表规定的 JSON object。字段名必须完全匹配，不能增加可选字段。
2. ID/config 值使用通过 validation 后的原始 UTF-8 字符串；trim 前后必须一致；不做大小写
   改写或 Unicode normalization。enum 值按合同 lowercase。
3. object 不允许缺字段或 null；integer 使用 JSON decimal integer，禁止 boolean/float。
4. 使用 UTF-8、`ensure_ascii=false`、lexicographic key sort、紧凑 separators
   `(',', ':')`、禁止 NaN/Infinity，末尾不加换行。
5. 对上述 bytes 计算 SHA-256，输出 lowercase hex 并加 `sha256:` 前缀。

config-aware fact identity objects：

| event role | 固定字段 |
| --- | --- |
| `cycle_start` / `cycle_complete` / `production_result` | `config_hash,cycle_counter,cycle_id,event_role,line_id,plc_boot_id,plc_id,station_id` |
| `nok_detail` | `config_hash,detail_role,event_role,line_id,nok_code,nok_origin,parent_event_id,parent_fact_key,plc_id,station_id` |
| `heartbeat` | `config_hash,event_role,line_id,plc_boot_id,plc_id,source_event_id,station_id` |

- `fact_key` 用于 config-aware deterministic fact identity、防御性重算和 trace；它不替代
  第 12.4 节的 physical cycle-role/detail-set uniqueness lookup。
- `production_result` fact object 不包含
  `source_event_id/result/nok_code/nok_origin/unit_id/dmc`。
- `nok_detail` fact object不包含 source ID；不同 code 是可保留的独立 detail，但不能改变
  parent result。
- `heartbeat` 没有 cycle business role，因此使用 source 提供的稳定 heartbeat identity。

official test vectors：

```text
station_result canonical bytes:
{"config_hash":"50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1","cycle_counter":42,"cycle_id":"LINE-01/PLC-01/WS02/01J10C2SZM4T2R8K6V2YDR45VH/42","event_role":"production_result","line_id":"LINE-01","plc_boot_id":"01J10C2SZM4T2R8K6V2YDR45VH","plc_id":"PLC-01","station_id":"WS02"}

station_result fact_key:
sha256:b08052bccb4d32c97b2c5da96540cb7a64f1a63a9bcedc7e0c418a9bc6542b7e

station_nok canonical bytes:
{"config_hash":"50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1","detail_role":"primary","event_role":"nok_detail","line_id":"LINE-01","nok_code":20001,"nok_origin":"plc","parent_event_id":"550e8400-e29b-41d4-a716-446655440000","parent_fact_key":"sha256:b08052bccb4d32c97b2c5da96540cb7a64f1a63a9bcedc7e0c418a9bc6542b7e","plc_id":"PLC-01","station_id":"WS02"}

station_nok fact_key:
sha256:61dda2995f339952e040fcbd69f4aceaf6f1ac6c2d846d389c9de8c0b10c9ed4
```

### 12.6 Content fingerprint official algorithm

职责固定：

- `fact_key`：标识 config-aware deterministic fact identity。
- `cycle_role_key/station_nok_detail_key`：占用业务唯一槽位。
- `content_fingerprint`：判断占用同一槽位的事实内容是否相同。

输入是通过 stateless validation、fact-key 重算和 canonical serialization 的 source
envelope。只删除以下精确 JSON Pointer paths，不递归删除其他同名字段：

```text
/event_id
/observed_at
/raw_payload
/correlation/source_event_id
/correlation/raw_encoding
```

`received_at/ingested_at/created_at` 不属于 source envelope；future projection wrapper
即使存在也必须排除。其余实际存在字段全部 included，包括：

- `event_type/event_ts/source/actor`。
- line/plc/station/boot/cycle/unit/DMC/config/profile identity。
- `result/nok_code/nok_origin`。
- normalized `payload` 完整内容。
- `correlation.fact_key/event_role/detail_role/mapping_id/payload_template/
  parent_event_id/upstream_evidence`。

算法：

1. absent field 保持 absent；MVP explicit null 已由第 4.3 节 reject。
2. enum 使用合同 lowercase；timestamp 使用 validator 输出的 RFC 3339 UTC `Z` canonical
   string，不增加小数精度。
3. 使用 UTF-8、`ensure_ascii=false`、lexicographic key sort、紧凑 separators
   `(',', ':')`、禁止 NaN/Infinity、末尾不加换行。
4. `content_fingerprint = "sha256:" + lowercase SHA-256(canonical bytes)`。

official content-fingerprint vectors：

```text
station_result fingerprint bytes:
{"actor":"plc","config_hash":"50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1","config_version":"2026.06.20-1","correlation":{"event_role":"production_result","fact_key":"sha256:b08052bccb4d32c97b2c5da96540cb7a64f1a63a9bcedc7e0c418a9bc6542b7e","mapping_id":"ws02_result","payload_template":"screw_result_v1"},"cycle_counter":42,"cycle_id":"LINE-01/PLC-01/WS02/01J10C2SZM4T2R8K6V2YDR45VH/42","dmc":"DMC-000042","event_ts":"2026-06-20T10:15:30.123Z","event_type":"station_result","line_id":"LINE-01","nok_code":20001,"nok_origin":"plc","payload":{"angle_deg":132.5,"torque_nm":4.8},"plc_boot_id":"01J10C2SZM4T2R8K6V2YDR45VH","plc_id":"PLC-01","profile_id":"normal_screwdriving","result":"nok","schema_version":"1.0","source":"plc","station_id":"WS02","station_type":"screw","unit_id":"UNIT-000042"}

station_result content_fingerprint:
sha256:4759aa7e6b81da994006afd8edc1e9ccc9286863dfc43d47b0d610406fce5f44

station_nok fingerprint bytes:
{"actor":"plc","config_hash":"50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1","config_version":"2026.06.20-1","correlation":{"detail_role":"primary","event_role":"nok_detail","fact_key":"sha256:61dda2995f339952e040fcbd69f4aceaf6f1ac6c2d846d389c9de8c0b10c9ed4","mapping_id":"ws02_result","parent_event_id":"550e8400-e29b-41d4-a716-446655440000","parent_fact_key":"sha256:b08052bccb4d32c97b2c5da96540cb7a64f1a63a9bcedc7e0c418a9bc6542b7e","payload_template":"screw_result_v1"},"cycle_counter":42,"cycle_id":"LINE-01/PLC-01/WS02/01J10C2SZM4T2R8K6V2YDR45VH/42","dmc":"DMC-000042","event_ts":"2026-06-20T10:15:30.124Z","event_type":"station_nok","line_id":"LINE-01","nok_code":20001,"nok_origin":"plc","payload":{"defect_axis":"torque"},"plc_boot_id":"01J10C2SZM4T2R8K6V2YDR45VH","plc_id":"PLC-01","profile_id":"normal_screwdriving","schema_version":"1.0","source":"plc","station_id":"WS02","station_type":"screw","unit_id":"UNIT-000042"}

station_nok content_fingerprint:
sha256:794e28acb185ef403a41ed560932de7d1f26708f25c698b33b47655fb5600dd8
```

修改仅 `/event_id`、`/observed_at` 或 `/correlation/source_event_id` 时 fingerprint 必须
不变。修改 result、config、cycle identity、normalized payload、detail role、parent 或
upstream evidence 时 fingerprint 必须变化。

### 12.7 Duplicate / conflict disposition

- 相同 `event_id` 且 `content_fingerprint` 相同：`duplicate`，保留首次 accepted identity，
  不重复投影。
- 相同 `event_id` 但 `content_fingerprint` 不同：`conflict` +
  `EVENT_ID_CONFLICT`，MVP reject。
- 相同 `fact_key` 且 `content_fingerprint` 相同：`duplicate`，不重复投影或 Pareto。
- 相同 `fact_key` 但 `content_fingerprint` 不同：`conflict` +
  `FACT_KEY_CONFLICT`，MVP reject，不自动合并、不 last-write-wins。
- 相同 `cycle_role_key/production_result_key/station_nok_detail_key/primary_nok_detail_key/
  system_reserved_detail_key` 且 fingerprint 相同：duplicate；fingerprint 不同：conflict。
- conflict MVP reject，不自动 merge、不进入生产指标或 defect Pareto。
- conflict 的 future runtime 可以保存到 quarantine，但 quarantine 不等于 accepted；
  本合同不实现 quarantine storage。
- Sprint 2 MVP 定义并测试上述规则，不实施 DB unique constraint 或 Collector retry。

## 13. Validation rules

### 13.1 Stateless validation

`validate_event(event, resolved_config=None)` 不依赖历史事件，检查：

1. strict top-level allowed keys。
2. required / conditional required fields。
3. string、integer、object、timestamp 与全部结构/size limit。
4. 所有枚举 fail closed。
5. per-event required/optional/forbidden 与 `event_type/result/nok_code` 组合矩阵。
6. `nok_origin` enum、conditional required 与 `30003` reserved protection。
7. station/plc/type/`profile_id` 与 resolved config 一致性。
8. `config_hash` 为 64 位 lowercase SHA-256 hex，且与传入 resolved config 一致。
9. cycle event 的 `plc_boot_id`、`cycle_counter`、`cycle_id` 一致。
10. payload template 与 unknown-field policy。
11. correlation strict schema 与 fact key 重算；不在本阶段查 parent/history。
12. raw payload 类型、编码声明、结构与大小。
13. payload 16 KiB / raw payload 64 KiB 上限，超限 reject。
14. source/actor/event/nok_origin authority matrix。
15. UUIDv4 accepted identity、retry reuse、UUIDv5 validator-external-only 与 UUIDv7
    future 规则。
16. UTC timestamp、合理下限、observed-at tolerance 与禁止 NaN/Infinity。
17. heartbeat diagnostic-only、disabled station 和 projection exclusion。

stateless 失败统一返回 `reject` 和稳定 error code/path。

### 13.2 Stateful validation

抽象接口：

```text
validate_event_stateful(event, state_index) -> ValidationDecision
```

`state_index` 至少提供只读 lookup：

```text
lookup_by_event_id(event_id)
lookup_by_fact_key(fact_key)
lookup_cycle_role(cycle_role_key)
lookup_parent_result(parent_event_id, parent_fact_key)
lookup_upstream_evidence(upstream_evidence)
lookup_detail_set(parent_fact_key)
lookup_detail_key(station_nok_detail_key)
lookup_resolved_config(config_hash)
```

每个 lookup 返回：

```text
LookupResult:
  status: found | not_found | unavailable
  record: only when found
```

- MVP 不使用含糊的 `pending/unresolved` 状态。
- `lookup_detail_set()` 至少返回 accepted primary detail、accepted
  `station_nok_detail_key` 集合和 accepted system-reserved detail。
- `lookup_cycle_role()` 必须按第 12.4 节不含 config/cycle_id 的 key 查询。

`ValidationDecision`：

| disposition | accepted | 规则 |
| --- | --- | --- |
| `accept` | yes | stateless 与全部 relation/uniqueness checks 通过 |
| `reject` | no | envelope/parent/evidence 无效；MVP 不持久化为 accepted fact |
| `duplicate` | no new projection | 与首次 accepted fact 内容相同；ignore/dedupe |
| `conflict` | no | 同 event/fact key 不同内容；MVP reject |
| `defer` | future-only | 不属于 MVP accepted validator；仅 future async runtime contract 可定义 |
| `future_quarantine` | future-only | 仅供 future adapter；Sprint 2 不实现 |

stateful 检查：

1. `event_id` duplicate/conflict。
2. `fact_key` 与 content fingerprint duplicate/conflict。
3. `cycle_role_key/production_result_key` uniqueness。
4. `station_nok_detail_key/primary_nok_detail_key/system_reserved_detail_key` uniqueness。
5. `station_nok` parent 存在、已 accepted、类型/result/cycle/identity 一致。
6. secondary detail 已有 accepted primary；primary/system-reserved 槽位未被不同内容占用。
7. `30003` upstream business evidence 存在、accepted 且与当前 skip cycle 关联。
8. disabled station 只允许 source heartbeat。
9. resolved config lookup 存在且 identity/profile/hash 一致。

MVP disposition 唯一规则：

| condition | disposition / error |
| --- | --- |
| required parent/evidence/config field missing | `reject / REQUIRED_FIELD_MISSING` |
| state index 未提供或 `unavailable` | `reject / STATE_INDEX_UNAVAILABLE` |
| parent lookup `not_found` | `reject / PARENT_NOT_FOUND` |
| upstream evidence lookup `not_found` | `reject / UPSTREAM_EVIDENCE_NOT_FOUND` |
| resolved config 不存在/unknown hash | `reject / CONFIG_NOT_FOUND` |
| record found 但 type/result/cycle/identity/route/subject 不匹配 | `reject / PARENT_EVENT_INVALID` 或 `UPSTREAM_EVIDENCE_INVALID` |
| 同业务唯一槽位 fingerprint 相同 | `duplicate` |
| 同业务唯一槽位 fingerprint 不同 | `conflict`，MVP reject |
| secondary 在 accepted primary 之前 | `reject / PRIMARY_DETAIL_REQUIRED` |

`conflict` 只用于 accepted event 已占据相同 event/fact/cycle-role/detail 槽位但
fingerprint 不同；不得用于一般 missing parent/evidence/config。

future async ingestion 可以在独立 runtime contract 中把“尚未到达”建模为 defer/
quarantine；该能力不属于 Sprint 2 MVP，且在 relation 完成前不得 accepted 或投影。

validator 应返回稳定、可测试的错误码和字段路径；至少冻结：

`REQUIRED_FIELD_MISSING`、`FIELD_FORBIDDEN`、`AUTHORITY_FORBIDDEN`、
`FIELD_NULL_FORBIDDEN`、`FACT_KEY_INVALID`、`CONTENT_FINGERPRINT_INVALID`、
`CYCLE_ROLE_CONFLICT`、`DETAIL_KEY_CONFLICT`、`STATE_INDEX_UNAVAILABLE`、
`PARENT_NOT_FOUND`、`UPSTREAM_EVIDENCE_NOT_FOUND`、`PRIMARY_DETAIL_REQUIRED`、
`UPSTREAM_EVIDENCE_INVALID`、
`RESULT_COMBINATION_INVALID`、`RESULT_CONFLICT`、`PARENT_EVENT_INVALID`、
`CONFIG_NOT_FOUND`、`CONFIG_HASH_MISMATCH`、`RESERVED_NOK_FORBIDDEN`、
`DIAGNOSTIC_CONTEXT_INVALID`、
`PAYLOAD_TOO_LARGE`、`PAYLOAD_TOO_DEEP`、`PAYLOAD_KEY_LIMIT`、
`PAYLOAD_TYPE_FORBIDDEN`、`RAW_ENCODING_INVALID`、`EVENT_ID_CONFLICT`、
`FACT_KEY_CONFLICT`、`EVENT_TS_FUTURE`。

不得用宽泛 exception 吞掉具体原因。

错误顺序固定为：presence/unknown field → type/format/resource → enum/combination →
authority/reserved evidence schema → config correlation/fact-key recompute → stateful
duplicate/conflict/parent/evidence。stateless 失败时不继续 stateful lookup。

字段路径使用 JSON-style dotted path 与 array index，例如
`correlation.upstream_evidence.parent_event_id`、`payload.measurements[0]`。同一阶段
多个错误按字段路径 lexicographic order 返回，保证 snapshot 稳定。

## 14. Canonical representation / serialization

PM 已批准后续 Sprint 2 implementation 路径：

```text
common/station_event/
  __init__.py
  models.py
  validator.py
  serializer.py
  errors.py
```

- 使用 frozen Python dataclass、标准库 enum 和显式 semantic validator。
- 不引入 Pydantic，不引入重型 schema 依赖。
- validator 与 serializer 保持独立。
- model construction 不应绕过 validator。
- canonical dict 省略 absent optional fields。MVP envelope 不允许 explicit null；required、
  optional 或 forbidden 字段的 null 均按第 4.3 节 reject。
- canonical JSON 使用 UTF-8、key 排序、紧凑 separators、禁止 NaN。
- timestamp 统一序列化为 UTC `Z`，小数秒精度不凭空增加。
- `event_id` 不由 canonical hash 替代。content fingerprint 使用第 12.6 节规定的排除
  字段，且不得与 `fact_key` 混用。
- tests 应覆盖 dict/JSON round-trip、stable snapshot、field order independence 和 mutation
  isolation。

## 15. Backward compatibility

- Sprint 1 `common/line_config/`、三份 YAML 和 hash 算法保持不变。
- Phase-1 DB100、DB101/102/103、现有 Collector/API/DB/Dashboard 行为保持不变。
- Sprint 2 package 在接入前是独立离线模块，不成为 runtime source of truth。
- 后续 adapter 必须 additive，并保留 WS01/WS02/WS03 compatibility。
- 本合同不授权 migration、旧字段重命名或删除。

## 16. 与 Sprint 1 的关系

`docs/contracts/line_configuration.md` 负责定义“有哪些 line/PLC/station/Buffer/mapping/
template/profile”；本合同负责定义“在某个 resolved config 身份下发生了什么 station
fact”。

关系固定为：

```text
line YAML
  -> resolved config
  -> config_version + config_hash
  -> station event identity / validation context
```

event 不复制完整 resolved config，但必须携带身份与必要快照字段。未来存储层负责按
`config_hash` 关联不可变配置快照。

## 17. Sprint 2 MVP

MVP 只交付：

- 独立 `common/station_event/` model / validator / serializer / errors；该路径已获 PM
  批准，但 planning freeze 本身不创建 package。
- 受控 enum 与组合矩阵。
- resolved line config correlation validator。
- representative fixtures / sample events。
- positive、negative、round-trip、snapshot、isolation tests。
- 合同、实现报告和 Gate 证据。

## 18. 延后范围

- V-PLC / real PLC event emission。
- Collector normalization、quarantine 和 retry。
- PostgreSQL migration、unique constraint、retention 和 partition。
- API endpoint、pagination、Trace Explorer 和 Dashboard。
- Buffer runtime adapter。
- Hold/Release/Rework 完整业务闭环。
- fault/heartbeat KPI 与设备状态模型。
- remote deploy、rollback drill 和 Phase-2 tag。

以上内容必须在后续独立 Sprint 中经合同、风险和 Verification Gate 后再实施。
