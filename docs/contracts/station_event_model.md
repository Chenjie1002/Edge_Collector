# Generic Station Event Model Contract

状态：Sprint 2 planning freeze；PM 决策已固化，等待三方 review

更新时间：2026-06-20

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
  "profile": "normal",
  "cycle_id": "LINE-01/PLC-01/WS02/01J10C2SZM4T2R8K6V2YDR45VH/42",
  "cycle_counter": 42,
  "unit_id": "UNIT-000042",
  "dmc": "DMC-000042",
  "result": "ok",
  "nok_code": null,
  "nok_origin": null,
  "source": "vplc",
  "actor": "simulator",
  "payload": {
    "torque_nm": 4.8,
    "angle_deg": 132.5
  },
  "raw_payload": null,
  "correlation": {
    "source_event_id": "PLC-01:WS02:42:result",
    "mapping_id": "ws02_result",
    "payload_template": "screw_result_v1"
  }
}
```

`created_at` 不属于 source canonical envelope。它由未来的存储层生成，不能覆盖
`event_ts`。

## 4. MVP 必需字段

所有 Sprint 2 MVP event 必须包含：

| 字段 | 类型 | 来源 | 语义 |
| --- | --- | --- | --- |
| `schema_version` | string | model | envelope 合同版本，MVP 为 `1.0` |
| `event_id` | string | source 或 normalizer | 单事件不可变 ID |
| `event_type` | enum | PLC/V-PLC 事实映射 | 事件语义 |
| `event_ts` | RFC 3339 UTC string | PLC/V-PLC | 原始事实时间 |
| `line_id` | string | resolved line config | 产线身份 |
| `plc_id` | string | resolved line config | PLC 身份 |
| `station_id` | string | resolved line config | 工站身份 |
| `station_type` | string | resolved line config snapshot | 事件发生时工站类型 |
| `config_version` | string | resolved line config | 配置可读版本 |
| `config_hash` | 64-char lowercase hex | resolved line config | resolved config SHA-256 |
| `source` | enum | ingress context | 事实进入模型的来源 |
| `actor` | enum | source metadata | 触发事实的主体 |
| `payload` | object | normalized mapping | 有边界的标准化扩展 |
| `correlation` | object | source/normalizer | 确定性追溯信息 |

周期相关事件还必须包含：

- `plc_boot_id`
- `profile`
- `cycle_id`
- `cycle_counter`

结果相关事件还必须包含 `result`；其合法组合见第 8 节。

## 5. MVP 可选字段与延后字段

| 字段 | MVP 状态 | 规则 |
| --- | --- | --- |
| `unit_id` | optional | 已有稳定 unit identity 时填写 |
| `dmc` | optional | PLC/HMI 提供的 DMC；不能由时间猜测 |
| `nok_code` | conditional | `result=nok` 或 `event_type=station_nok` 时必需 |
| `nok_origin` | conditional | NOK 事件/结果的受控来源；普通非 NOK 事件禁止携带 |
| `raw_payload` | optional | 原始 decoded bytes/object 的有界表示 |
| `observed_at` | optional, Collector-only | Collector 实际观察时间；未来 adapter 使用 |
| `created_at` | deferred, DB-only | 存储层生成，不参与 source canonical JSON |
| `route_id` / `route_step` | deferred | Sprint 2 不实现 route execution |
| Hold/Rework relation fields | deferred | 后续合同增量定义 |

`unit_id`、`dmc`、`cycle_id` 不是可互换字段。`cycle_id` 标识一次工站周期；
`unit_id` 标识 MES 工件实体；`dmc` 是现场可读/可扫描身份。

## 6. 字段类型与基本语义

- ID 字段必须是非空、trim 后不变的 UTF-8 string，最大 128 字符。
- `event_id` 必须存在并唯一标识事件，MVP 不依赖 DB 自增 ID。
- MVP runtime 默认允许 UUIDv4；未来推荐 UUIDv7，但 Sprint 2 不强制。
- UUIDv5 仅允许 deterministic test fixture / snapshot，禁止作为 runtime 默认。
- 本轮不实现 UUID 生成；后续 helper 可提供 UUIDv4 默认生成。
- serializer 不得重新生成或改写已有 `event_id`。
- `cycle_counter` 是 `0..2^63-1` integer，禁止 boolean 和 float。
- `profile` 使用 line configuration 已解析的 profile 名称。
- `result`、`source`、`actor` 和 `event_type` 使用小写 snake_case。
- `payload` 与 `correlation` 必须是 JSON object；不能是 array、scalar 或 null。
- 数值禁止 NaN、Infinity 和 `-Infinity`。
- envelope 顶层未知字段 fail closed。

## 7. `event_type` 分层

### 7.1 Sprint 2 MVP 必须支持

- `station_cycle_start`
- `station_cycle_complete`
- `station_result`
- `station_nok`
- `station_heartbeat`

其中 `station_result` 是规范结果事实；`station_nok` 是显式 NOK 事实，可与同周期
`station_result(result=nok)` 共存，适用于独立表达 `nok_code`、`nok_origin`、reserved
code 与 manual/forced/random/system_reserved 来源。两者必须通过 correlation 关联且
不得重复计数。`station_nok` 只记录和规范化 PLC / V-PLC / HMI / simulator / system
提供的 NOK 事实，不表示 Edge 做出质量或控制决策。

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

| `event_type` | 允许的 `result` | `nok_code` |
| --- | --- | --- |
| `station_cycle_start` | absent | absent |
| `station_cycle_complete` | optional: `ok/nok/skip/not_applicable` | 仅 `nok` 时允许/必需 |
| `station_result` | required: `ok/nok/skip/not_applicable`；受控 diagnostic context 才允许 `unknown` | 仅 `nok` 时必需 |
| `station_nok` | required: `nok`；`30003` 特例允许 `skip` | required |
| `station_heartbeat` | absent / `unknown` / `not_applicable` | absent |

规则：

- `result=nok` 必须有在工站 NOK template 中可解释的 `nok_code`。
- `result=nok` 与 `station_nok` 必须有 `nok_origin`。
- 非 NOK result 禁止携带普通 NOK code。
- `30003` 固定表示 `UPSTREAM_NOK_SKIPPED`，mode 为 `system_reserved`。
- `30003` 只能与 `nok_origin=system_reserved` 组合。
- MVP 中 `30003` 只允许显式 `station_nok(result=skip)` 表达“因上游 NOK 而跳过”的
  route semantic；未来 `station_skip` 接入后可由独立合同扩展。
- `30003` 禁止用于 random、forced 或 manual NOK。
- global NOK fallback 和 station-level NOK override 只决定 V-PLC 仿真生成概率；事件合同
  记录已发生事实，不重新计算 NOK。
- `nok_origin` 是独立业务语义字段，不得放入 `correlation`。
- `nok_origin` 枚举为
  `random/forced/manual/plc/hmi/system_reserved/simulator/unknown`。
- `correlation` 只承担 trace / event 关联，不承担 NOK 来源语义。
- manual/forced/random 等 origin 只解释已发生事实；Edge 不据此改写 result。
- 缺失或 malformed result 必须拒绝，不能静默映射为 `unknown`。
- `unknown` 只允许 `station_heartbeat`、未来 `station_fault`、明确 diagnostic/incomplete/
  explicitly-unknown context，以及专用 fixture 场景。
- 正常 `station_cycle_complete` 禁止 `unknown`。
- 正常 `station_result` 在应提供 OK/NOK/SKIP 时禁止 `unknown`；validator 默认拒绝，
  仅在明确 diagnostic validation context 下接受。

## 9. `source`、`actor` 与 authority

MVP `source`：

- `plc`
- `vplc`
- `collector`
- `manual_import`
- `system`

MVP `actor`：

- `plc`
- `hmi`
- `operator`
- `collector`
- `simulator`
- `system`

权限边界：

- `plc` / `vplc` 可提供所有 MVP 现场事实。
- `collector` 可生成 ingestion、validation、quarantine 等技术元数据，但不得凭测量值
  生成 OK/NOK/Skip/Hold/Rework 业务事实。
- `manual_import` 只表示可审计的历史导入，不等于现场 manual NOK。
- `system` 只用于明确的系统保留语义；不得伪装成 PLC 决策。
- `api` 作为未来 source 预留，不进入 MVP 枚举；API 不应成为现场业务事件权威。
- `actor=operator` 必须能关联 HMI/manual source evidence，不能由 Edge 推测。

## 10. 与 line configuration / `config_hash` 的关联

- 每个有效 MVP station event 必须携带 `config_version` 和 `config_hash`；正常生产事件
  不允许缺失。
- `line_id`、`plc_id`、`station_id`、`station_type` 必须与该 hash 对应的 resolved config
  一致。
- `station_id` 必须存在且属于 `plc_id`；`station_type` 必须匹配配置快照。
- disabled station 不能产生正常周期事实；诊断事件以后单独定义。
- Buffer event 必须匹配 Buffer `enabled` 与 `tracking_mode`，但 Buffer adapter 延后。
- mapping/template identity 放入 `correlation`，用于追溯 DB mapping 与 payload schema。
- hash 缺失：MVP model validation 失败。
- `config_hash` 格式固定为 64 位 lowercase SHA-256 hex。
- hash 格式合法但未知：未来 Collector 应 quarantine，不得猜测或套用当前配置。
- hash 与 identity mismatch：未来 Collector 应 quarantine 并告警，不得重写 source fact。
- Sprint 2 MVP 只实现离线 model/config correlation 校验，不实现 runtime config registry。

## 11. `payload` / `raw_payload` 策略

### Normalized payload

- 必须是 JSON object。
- canonical UTF-8 JSON 最大 16 KiB。
- payload template 已声明字段按 template 严格校验。
- template 未声明的字段默认拒绝；显式 `extensions` object 可作为受控扩展槽。
- torque、angle、pressure、test value 等工站特有测量值放在 payload。
- 单位应编码在 schema/template 中，不在字段名中任意漂移。

### Raw payload

- 可为 JSON object、UTF-8 string 或 base64 string；表示方式必须由
  `correlation.raw_encoding` 声明。
- canonical 表示最大 64 KiB。
- 不得包含凭据、密钥或未脱敏个人数据。
- raw 与 normalized 必须通过同一 `event_id`、mapping/template version 追溯。
- raw 不参与业务 result 决策；它是审计与重放证据。
- `raw_payload` 不得替代 normalized payload。
- MVP 对 payload 或 raw payload 超限直接 reject；future runtime 可在独立合同中改为
  quarantine，但不得静默截断。

## 12. 时间、顺序与幂等

- `event_ts` 来自 PLC/V-PLC 事实时间，必须是带 `Z` 的 RFC 3339 UTC。
- `observed_at` 由未来 Collector 填写，表示 Edge 首次观察时间。
- `created_at` 由未来 DB 生成，表示落库时间。
- 三种时间不可互相覆盖。
- out-of-order event 允许进入验证/隔离流程；不得改写 `event_ts` 以制造顺序。
- 同 station/boot 内优先使用 `cycle_counter` 排序，时间作为辅助。
- `cycle_id` 推荐确定性格式：
  `line_id/plc_id/station_id/plc_boot_id/cycle_counter`。
- 推荐幂等事实键：
  `(line_id, plc_id, station_id, plc_boot_id, cycle_counter, event_type, source_event_id)`。
- 相同 `event_id` 且 canonical content 相同视为重复；相同 `event_id` 内容不同视为冲突。
- Sprint 2 MVP 定义并测试上述规则，不实施 DB unique constraint 或 Collector retry。

## 13. Validation rules

validator 至少执行：

1. strict top-level allowed keys。
2. required / conditional required fields。
3. string、integer、object、timestamp 与 size limit。
4. 所有枚举 fail closed。
5. `event_type` / `result` / `nok_code` 组合矩阵。
6. `nok_origin` enum、conditional required 与 `30003` reserved protection。
7. station/plc/type/profile 与 resolved config 一致性。
8. `config_hash` 为 64 位 lowercase SHA-256 hex，且与传入 resolved config 一致。
9. cycle event 的 `plc_boot_id`、`cycle_counter`、`cycle_id` 一致。
10. payload template 与 unknown-field policy。
11. raw payload 类型、编码声明与大小。
12. payload 16 KiB / raw payload 64 KiB 上限，超限 reject。
13. source/actor authority 组合。
14. UUIDv4 runtime、UUIDv5 test-only 与 UUIDv7 future-compatible 规则。
15. UTC timestamp 与禁止 NaN/Infinity。

validator 应返回稳定、可测试的错误码和字段路径；不得用宽泛 exception 吞掉具体原因。

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
- canonical dict 省略 absent optional fields，但保留有语义的显式 `null`。
- canonical JSON 使用 UTF-8、key 排序、紧凑 separators、禁止 NaN。
- timestamp 统一序列化为 UTC `Z`，小数秒精度不凭空增加。
- `event_id` 不由 canonical hash 替代；可另提供 content fingerprint 用于 compare/snapshot。
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
