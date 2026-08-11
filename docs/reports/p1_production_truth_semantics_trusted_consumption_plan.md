# Edge MES Demo — P1 Production Truth Semantics & Trusted Consumption PM Plan

状态：OWNER APPROVED / PLANNING BASELINE  
日期：2026-08-11  
Mainline baseline：`P0_PM_ACCEPTED=YES` / `PRODUCTION_ACCEPTED=YES` / Shadow P0 Goal closed  
Mainline source commit baseline：`dbe5706e4b01387101f2a4666e73f3c13ffeb0e9`

## 1. P1 目标

P1 的目标不是继续证明 Collector 能产生 accepted production fact，而是把已经成立的 production truth 转化为可被产品层可信消费、可复算、不会误导的 Quality / Trace / Process KPI 数据语义和 bounded API。

P1 需要回答：

1. 当前 accepted production fact 与历史配置 authority 已经足够支持哪些业务语义；
2. 哪些语义只能标记为 PARTIAL；
3. 哪些语义在当前数据条件下必须明确 UNSUPPORTED；
4. 如何让 DB raw accepted facts 与 API 输出在同一 scope/window 下独立复算一致；
5. 如何在不伪造 OEE 的前提下建立 Quality、Trace、Process KPI 与 OEE data-sufficiency contract；
6. 如何把真实 Raspberry Pi runtime 的 accepted facts 贯通到产品消费层，而不重新打开 P0 Collector closure。

P1 的产品原则：

> 能算的必须算对；不能算的必须明确说不能算；不得为了 Dashboard 完整度制造业务真值。

## 2. 已接受起点

P1 继承的是已接受事实，不继承 Shadow P0 execution authority：

- corrected source commit：`dbe5706e4b01387101f2a4666e73f3c13ffeb0e9`；
- accepted runtime Collector lineage 已建立；
- `P0_PM_ACCEPTED=YES`；
- `PRODUCTION_ACCEPTED=YES`；
- 已存在真实 accepted production fact：`WS01 / ok / cycle_counter 113095`；
- `production_accepted_station_event_fact` 已作为 production-only accepted fact landing surface；
- `/api/v2/production/accepted-station-events` 已直接读取该 production fact surface，并具有 bounded window、cursor、read-only transaction 与 fail-closed source-unavailable 行为；
- line configuration 已包含动态 `route_graph.terminal_station_id`、station order、cycle profile 与 `ideal_cycle_time_s`；
- P0 focused Reliability / Data Quality / Verification reviews 已在 unchanged lineage 上通过，不因 P1 planning 自动重跑。

P1 不继承：

- Shadow P0 Gate budget；
- B1 execution authority；
- 第二次 B1 eligibility reassessment authority；
- remote / Docker / lifecycle / V-PLC / DB mutation / Git mutation authority；
- parallel `FIELD-VALIDATION-COLLECTOR-DB` branch authority。

## 3. 当前结构性断层

现有生产真值与 legacy KPI/Trace 消费层之间存在明确断层：

- 新 production truth authority 已进入 `production_accepted_station_event_fact`；
- 现有 `api/app/routes/kpi.py` 仍主要从 `production_snapshot` 计算 output / quality；
- 现有 `docs/kpi_definitions.md` 仍大量使用 `cycle_event`、固定 `WS03`、默认 `30s` 理论节拍与自然时间窗简化口径；
- 现有 Trace 路径仍包含 legacy `cycle_event` / `production_unit` 语义；
- 当前配置已存在 `route_graph.terminal_station_id` 与 `ideal_cycle_time_s`，但这些配置事实尚未被正式裁决为历史 KPI authority；
- 完整 Availability 所需 planned production time / planned downtime / authoritative machine-state timeline 尚未建立可信 source authority。

因此 P1 不允许 Dashboard-first 或 OEE-first。第一步必须是 source adequacy 与 semantic boundary freeze。

## 4. 路线选择

Owner 接受路线：`Truth First + Vertical Slice`。

主路径：

```text
Accepted Production Facts
        ↓
Source Adequacy
        ↓
Production Semantics Contract
        ↓
Quality + Trace Vertical Slice
        ↓
Process KPI / Partial OEE Semantics
        ↓
Bounded Production API
        ↓
Real Runtime DB/API Reconciliation
        ↓
P1 PM Acceptance
```

不采用：

- OEE First：当前 Availability source 不足，容易制造虚假 OEE；
- Dashboard First：UI 不应先替数据层决定 KPI 真值与 fallback 规则。

## 5. P1 MVP 范围

### 5.1 Quality MVP

目标能力：

- total production-result count；
- good count；
- NOK count；
- yield / quality rate；
- NOK by station；
- accepted NOK code distribution；
- 所有数字可追溯到 accepted production facts；
- diagnostic reason、raw payload、adapter rejection 不得被提升为 Quality fact。

### 5.2 Trace MVP

目标能力：

- `unit_id` 查询；
- `dmc` 查询；
- station timeline；
- cycle counter；
- station result；
- accepted NOK/detail evidence；
- source event identity；
- config hash/version；
- dynamic route order / terminal station 只在 source adequacy PASS 后成为产品语义。

Trace MVP 不包含 Genealogy。不得通过时间接近推断父子件、装配、替换或 Rework 关系。

### 5.3 Process KPI MVP

目标能力：

- station cycle-time semantics；
- output / throughput semantics；
- station/line scope consistency；
- bounded time-window semantics；
- config-bound ideal cycle time 仅在 G0/G1 明确接受后用于 Performance；
- 所有 KPI 暴露 data sufficiency 状态。

### 5.4 OEE 边界

P1 不以完整 OEE 百分比为成功标准。

必须显式区分：

```text
AVAILABLE
PARTIAL
UNAVAILABLE
```

对 OEE component 至少分别裁决：

- Availability；
- Performance；
- Quality；
- Full OEE。

在缺少 planned production time / planned downtime / authoritative state timeline 时，不得把自然时间窗当作 Planned Production Time。

## 6. Production truth authority 原则

P1 新 production semantics 的优先 authority：

```text
production_accepted_station_event_fact
+ accepted immutable config lineage
+ explicitly accepted auxiliary business source, if a later Gate establishes one
```

以下对象默认只能是 compatibility / diagnostic / historical source，不能静默 fallback 成为新 P1 production truth：

```text
production_snapshot
cycle_event
quality_event
production_unit
raw_plc_sample
adapter diagnostics
```

如果某个 P1 指标必须依赖上述 legacy source，必须在 G0/G1 明确记录：

- 为什么 accepted fact surface 不足；
- 该 source 的 authority 等级；
- 是否只是兼容显示；
- 是否会污染 production truth；
- 是否需要新的 Level 2 数据模型计划。

禁止 silent fallback。

## 7. Gate 路线

### P1-G0 — Production Source Adequacy & Semantic Boundary Freeze

类型：Level 2 / Planning Only  
主责：Architecture / Integration  
核心 reviewer：Data Quality（后续独立 Gate，如 G0 改变 production semantic authority）

目标：

- 对 accepted fact、config route、cycle profile、legacy KPI/Trace source 做只读审计；
- 产出 Source Adequacy Matrix；
- 对每个业务语义裁决 `SUPPORTED / PARTIAL / UNSUPPORTED`；
- 明确哪些业务语义可直接进入 G1；
- 明确是否存在真正需要 DB/model expansion 的 blocker；
- 不修改产品代码、schema、API、KPI 文档。

G0 推荐最小矩阵：

| 语义 | 目标 source | G0 必须裁决 |
| --- | --- | --- |
| Station OK/NOK | accepted `station_result` | SUPPORTED/PARTIAL/UNSUPPORTED |
| Station NOK code | accepted NOK business evidence | SUPPORTED/PARTIAL/UNSUPPORTED |
| Event timeline | accepted event facts | SUPPORTED/PARTIAL/UNSUPPORTED |
| `unit_id` Trace | accepted fact `unit_id` | SUPPORTED/PARTIAL/UNSUPPORTED |
| DMC Trace | accepted fact `dmc` | SUPPORTED/PARTIAL/UNSUPPORTED |
| Dynamic terminal station | immutable config route authority | SUPPORTED/PARTIAL/UNSUPPORTED |
| Dynamic station order | immutable config route/station authority | SUPPORTED/PARTIAL/UNSUPPORTED |
| Station cycle time | accepted start/complete evidence | SUPPORTED/PARTIAL/UNSUPPORTED |
| Throughput/output | accepted terminal result evidence | SUPPORTED/PARTIAL/UNSUPPORTED |
| Ideal cycle time | config cycle profile lineage | SUPPORTED/PARTIAL/UNSUPPORTED |
| Quality component | accepted result evidence | SUPPORTED/PARTIAL/UNSUPPORTED |
| Performance component | ideal CT + authoritative runtime denominator | SUPPORTED/PARTIAL/UNSUPPORTED |
| Availability component | planned production + state timeline | SUPPORTED/PARTIAL/UNSUPPORTED |
| Full OEE | A × P × Q | SUPPORTED/PARTIAL/UNSUPPORTED |

G0 PASS 只表示“语义充分性边界已经被可信冻结”，不表示所有项目都 SUPPORTED。

### P1-G1 — Production Semantics Contract

类型：Level 2 / Contract Planning  
主责：Data Quality

输入：accepted P1-G0 Source Adequacy Matrix。

冻结：

- production count；
- good / NOK count；
- yield；
- terminal station semantics；
- station ordering；
- cycle-time pairing；
- throughput；
- trace completeness / missing-station presentation；
- data sufficiency；
- OEE component availability；
- legacy compatibility boundary；
- no-fallback rule。

首选新合同路径：`docs/contracts/production_metrics_contract.md`。旧 `docs/kpi_definitions.md` 作为 legacy engineering KPI 文档，是否修改由 G1 独立决定。

### P1-G2 — Quality + Trace Vertical Slice

类型：Level 2 / Implementation  
前置：G1 accepted。

目标：

- 先实现 Quality + Trace，不先实现完整 OEE；
- 优先复用 accepted fact surface；
- API 新 production truth 继续放在 `/api/v2/production/*`；
- legacy `/kpi/*` 与 `/trace/*` 默认保持兼容，不直接提升为 P1 authority；
- 不默认新增 DB table/migration；只有 G0/G1 建立明确 data-model blocker 才另开 migration planning Gate。

需要按 PM Rules 完成 focused Reliability / Data Quality / Verification review，但只审查 changed lineage/contract，不重开已通过的 P0 focused reviews。

### P1-G3 — Process KPI + Partial OEE Semantics

类型：Level 2 / Contract + Implementation Planning

目标：

- station CT；
- output rate / throughput；
- accepted Quality component；
- Performance source adequacy；
- Availability source adequacy；
- `AVAILABLE / PARTIAL / UNAVAILABLE` contract；
- 明确禁止假 OEE。

如果 Availability 仍不充分，P1 可以在 `Availability=UNAVAILABLE`、`Full OEE=UNAVAILABLE` 下继续 PASS，只要产品诚实显示数据不足。

### P1-G4 — Bounded Production API

类型：Level 2 / Implementation

目标：

- 为 P1 accepted semantics 提供 bounded read-only API；
- 保持 line/window/scope/cursor 合同明确；
- API 输出必须能够由同一窗口的 accepted facts 独立复算；
- source unavailable / invalid scope / unsupported metric fail closed；
- 不允许 legacy fallback 伪造 production truth。

Endpoint 名称由 G1/G3 contract 冻结，不在 PM plan 中提前把 URL 当作实现 authority。

### P1-G5 — Raspberry Pi Runtime DB/API Reconciliation

类型：Level 2 / Remote Read-only Validation by default

目标不是重新证明 Collector，而是证明：

```text
real accepted facts
→ production semantics
→ production API
```

同一真实窗口下：

- DB accepted fact recomputation；
- API output；
- Quality；
- Trace；
- Process KPI/data sufficiency；

一致。

默认 remote read-only；默认 production stimulus=0。只有没有可用事实且 Owner 另行授权时，才考虑 production stimulus。

### P1-G6 — P1 PM Acceptance

P1 建议 terminal criteria：

```text
PRODUCTION_TRUTH_SOURCE_ACCEPTED = YES
QUALITY_SEMANTICS_ACCEPTED = YES
TRACE_SEMANTICS_ACCEPTED = YES
PROCESS_KPI_SEMANTICS_ACCEPTED = YES
OEE_DATA_SUFFICIENCY_EXPLICIT = YES
FULL_OEE_FALSE_CLAIM = NO
BOUNDED_PRODUCTION_API_ACCEPTED = YES
DB_API_RECONCILIATION = PASS
LEGACY_FALLBACK = NO
REAL_RUNTIME_VALIDATED = YES
```

P1 PM acceptance 只由 Mainline PM independent intake 建立。

## 8. Thread 分工

### Architecture / Integration

负责：

- source adequacy；
- accepted fact ↔ config ↔ API boundary；
- dynamic route / terminal authority；
- module ownership；
- 是否真正需要 schema/model extension。

### Data Quality

P1 核心 semantic owner：

- KPI semantics；
- Quality truth；
- Trace truth；
- data sufficiency；
- production fact authority；
- no-fallback boundary。

### Reliability

只审查真正涉及：

- read consistency；
- stale/unavailable behavior；
- runtime/config identity；
- transaction/query safety；
- changed code path 的 failure semantics。

Reliability 不负责定义 KPI 业务口径。

### Verification

负责：

- independent recomputation；
- scope/window equality；
- negative leakage；
- DB/API reconciliation；
- changed contract/code path 的 regression proof。

禁止把 P1 再扩展为 generic evidence framework。

## 9. Parallel real-device branch 边界

`FIELD-VALIDATION-COLLECTOR-DB` 继续保持治理隔离，不是 P1 prerequisite。

允许通过 Mainline PM intake 接收其明确、可复核的 field finding，例如：

- real PLC timestamp semantics；
- cycle counter behavior；
- restart identity；
- field data 对某 KPI source adequacy 的实际限制。

branch finding 不自动修改 P1 contract，也不继承 branch execution authority。

## 10. P1 明确 Out of Scope

P1 不自动授权：

- B1 execution；
- 第二次 B1 eligibility reassessment；
- reopen P0 Remote Closure；
- Collector image rebuild/redeploy；
- Full Genealogy / `unit_relation`；
- Hold / Rework；
- Data Gap 自动推断；
- Missing Unit 自动推断；
- Multi-Line implementation；
- Oracle/ERP；
- AI；
- 3D；
- final Dashboard redesign；
- generic evidence normalization/audit platform；
- tamper-proof audit platform。

如某项 out-of-scope 能力被 fresh evidence 证明为 P1 MVP 的硬 prerequisite，必须先回 Mainline PM 重新做 MVP/risk classification，不能由 specialist 扩 scope。

## 11. Governance 策略

P1 吸取 P0 closure 的控制面教训：

1. 产品事实优先于 assurance machinery；
2. evidence 与风险成比例；
3. 本地报告写入失败不得自动升级为产品 defect；
4. immutable lock 仅用于真正 authority/mutation safety，不用于普通 report cosmetics；
5. unchanged lineage 不重复 focused review；
6. remote/runtime Gates 串行；
7. DB/schema mutation 与 API/code mutation 分开授权；
8. task/report Git stage、commit、push、tag 单独授权；
9. 每个 Gate 只有一个明确 next gate；
10. 若连续 evidence work 明显超过 product work，必须先做 MVP/governance inflation check。

## 12. P1 复杂度预算建议

P1 不继承 Shadow P0 的旧 dual-budget。

建议新的产品 Gate 正常路径预算：

```text
planned product gates = G0..G6
recovery gates are exceptional, not preallocated as normal work
```

若同一 Gate 连续出现 2 次非产品 mechanics HOLD，Mainline PM 在生成第 3 个 recovery task 前必须执行：

```text
PRODUCT_BLOCKER_OR_CONTROL_PLANE_DEFECT?
MVP_PATH_STILL_VALID?
CAN_SCOPE_BE_SIMPLIFIED?
```

若答案显示问题属于 tooling/report mechanics，不得继续用更多 validation layers 修产品不存在的 defect。

## 13. P1-G0 当前授权状态

Owner 已于 2026-08-11 明确认可本 PM plan。

当前仅授权 Mainline PM：

- 将本 P1 plan 持久化为 durable planning baseline；
- 发布 P1-G0 repository-backed Architecture / Integration planning task；
- P1-G0 只读执行仍须由 Owner 使用 exact launcher 手动 dispatch；
- task/result 不自动授权 G1、implementation、remote、DB mutation 或 Git mutation。

当前下一 Gate：

```text
P1-G0 — Production Source Adequacy & Semantic Boundary Freeze
Level 2 / Planning Only
```
