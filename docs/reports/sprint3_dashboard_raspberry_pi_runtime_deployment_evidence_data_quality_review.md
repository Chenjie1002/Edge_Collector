# Sprint 3 Dashboard Raspberry Pi Runtime Deployment Evidence Data Quality Review

报告名称：

`Sprint 3 Dashboard Raspberry Pi Runtime Deployment Evidence Data Quality Review`

任务名称：

`Gate B — Raspberry Pi Runtime / Deployment Evidence Data Quality Focused Planning Review`

执行 Thread：

`Data Quality`

结论：`HOLD`

## 1. Reviewed baseline

- project: `/Users/chenjie/Documents/MES/edge-mes-demo`
- branch: `main`
- live `HEAD`: `29f02599447e4510209cd0ad419f70539f034507`
- live `origin/main`: `29f02599447e4510209cd0ad419f70539f034507`
- ahead/behind: `0 0`
- tracked diff: `.gitignore` only
- cached diff: empty
- Architecture planning report、Reliability review、Reliability re-review：均存在，且为本轮既有 untracked authority inputs
- proposed Data Quality report：recovery 时不存在

旧 PM handoff 的 authoring-time baseline 为历史记录，已由 live Git 事实 supersede；未发现与本轮 gate state、allowlist 或授权边界冲突。`M .gitignore`、frontend generated artifacts、历史 reports/handoffs 和 Keynote artifacts 均按 external/generated context 保留，未删除、restore、clean、整理或纳入本轮。

当前既有状态保持：

```text
Gate A Accepted-events Consumer Truth Hardening: CLOSED / PASS WITH RECOMMENDATIONS
Gate B Dashboard Raspberry Pi Docker Integration static implementation: CLOSED / PASS WITH RECOMMENDATIONS
Gate B Raspberry Pi Runtime / Deployment Architecture Planning: PASS WITH RECOMMENDATIONS
Gate B Raspberry Pi Runtime / Deployment Reliability Planning: CLOSED / PASS
B-R4-1: CLOSED
Docker/Compose/Pi/runtime/DB/API/real Case A/B/C: NOT EXECUTED / NOT CLAIMED
```

## 2. Exact scope and allowlist compliance

### Reviewed files

按用户指定 authority 顺序读取并静态复核：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/data_quality.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260715-0920.md`
- `docs/current_status.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_gate_status.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_review.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_rereview.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_review.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_rereview.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_rereview_round2.md`
- `docs/reports/sprint3_accepted_events_consumer_truth_hardening_data_quality_review.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_implementation_review.md`
- `docs/contracts/dashboard_api_contract.md`
- `db/migrations/007_accepted_station_event_visibility.sql`
- `collector/app/services/accepted_station_event_fact.py`
- `api/app/routes/accepted_station_events.py`
- `api/app/routes/health.py`
- `frontend/src/lib/acceptedStationEvents/schema.ts`
- `frontend/src/lib/acceptedStationEvents/apiClient.ts`
- `frontend/src/lib/acceptedStationEvents/viewModel.ts`
- `frontend/src/app/accepted-events/page.tsx`
- 对应 accepted-events focused tests：schema、apiClient、viewModel、page tests，仅用于确认当前 consumer truth boundary
- `docs/deployment/raspberry_pi.md`

### Created / changed

- created：`docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_data_quality_review.md`
- changed existing files：none
- staged files：none

本轮没有运行 tests、typecheck、build、Docker/Compose、SSH/Pi、port/firewall/resource commands、API/DB/browser runtime、PostgreSQL query、real Case A/B/C、rollback/cancellation 或任何 Git write。

## 3. DQ1–DQ10 review

### DQ1 — Production accepted-fact source authority

**HOLD（受 `DQ-RUNTIME-EMPTY-1` 限制）。**

`production_accepted_station_event_fact` 是 contract、migration、Collector accepted-fact builder 和 API route 共同确认的唯一 production fact source。Runtime plan Phase M 和 future execution allowlist 的 bounded PostgreSQL query category 均禁止 legacy/raw/diagnostic/Grafana/fixture/current-config fallback、join-derived filler、API mock、write、migration、ACK 或 `read_done` mutation。API `/health`、Dashboard `/health`、image identity 和 process health 也没有被定义为 fact authority。

Case candidate discovery、pagination key-set authority 和 mandatory Case A/B 的 read-only boundary 方向正确。但 Phase L 的 known-empty 没有把“bounded PostgreSQL scope 内无 accepted rows”写成明确的 authority record；该遗漏同时影响 source authority 与 known-empty closure，见 blocker `DQ-RUNTIME-EMPTY-1`。

### DQ2 — Historical identity and lineage

**PASS。**

Runtime plan 以 `fact_key` 为主 identity，并要求同时核对 `source_event_id`、`content_fingerprint`、`event_ts` 和 `accepted_at`。`config_hash`、`config_version` 与 line/PLC/station/station type/profile 字段均要求直接来自同一个 historical accepted fact row；没有 current config、Dashboard selection 或 latest config 覆盖路径。`event_ts` 与 `accepted_at` 保持 source event time 与 accepted-fact timestamp 的独立语义。未要求通用 lineage graph 或旧 strong-audit framework。

### DQ3 — Known-empty evidence

**HOLD — `DQ-RUNTIME-EMPTY-1`。**

Phase L 要求 bounded `line_id/start_time/end_time/limit`、API raw response、`data.items == []`、Dashboard explicit empty，并清除旧 table rows、summary、NOK/detail evidence 和 trace reference；Dashboard page/consumer tests 也保持 empty/error fail-closed boundary。

但 plan 只写“使用已知无 row 的 bounded window”，没有明确保存或复核同一 `line_id/start_time/end_time/limit` scope 在 `production_accepted_station_event_fact` 上的 bounded read-only zero-row result。若未来仅凭一个看起来为空的窗口、API empty 或 Dashboard screenshot 作为 known-empty authority，scope 错误、API query defect 或 stale/legacy data 被排除后仍可能被误报为 empty PASS。这是直接 false-empty PASS 路径。

Known-empty 只能证明该 bounded scope，不应扩大为数据库、整条产线或历史全量无事实。

### DQ4 — Opaque cursor pagination completeness

**PASS（planning boundary）。**

Phase L 冻结 same `line_id`、`start_time`、`end_time`、`limit`，要求 page 2 原样传入 page 1 `next_cursor`，cursor 保持 opaque，不 decode、修改或重建。计划要求保存 page 1/page 2 raw API response、各自 `fact_key` set、原始 cursor 和 bounded DB authority key set，并复核 stable order `event_ts, accepted_at, fact_key`、无重复、无遗漏、无 scope drift。当前页 summary 明确为 page-only；empty page 不得保留上一页 truth。

具体 request-count instrumentation 和 browser operation 属 Verification 记录面；本计划已把无法证明 request count、set 对齐或 stale truth 定义为 `HOLD`，不构成当前新增 blocker。

### DQ5 — Real Case A

**PASS（planning boundary；未执行）。**

Case A 被明确限定为 real accepted `station_result` 且 `production_result=ok`，同时要求 `nok_code`、`nok_origin` 和三个 `nok_detail_*` 均为 `null`。目标由真实 production fact row discovery，使用独立 bounded API request 成为 `items[0]`，claim 只限该 target first item；不得使用 cycle event、mock、fixture 或 synthetic row。无法取得真实且可隔离 target 时为 `HOLD`，不是 static evidence PASS。

当前状态：`NOT EXECUTED / NOT CLAIMED`。

### DQ6 — Real Case B

**PASS（planning boundary；未执行）。**

Case B 被明确限定为 real accepted `station_result`、`production_result=nok`、`nok_code` 与 `nok_origin` non-null，且三个 detail authority fields 全为 `null`。计划没有用 `station_nok`、cycle event 或仅有 `nok_code` 的 row 替代 production outcome；目标同样必须是独立 bounded request 的 `items[0]`。

当前状态：`NOT EXECUTED / NOT CLAIMED`。

### DQ7 — Real Case C conditional classification

**HOLD — `DQ-RUNTIME-CASE-C-REL-1`。**

Case C 的 row predicate、`production_result=null`、NOK/detail fields non-null、真实 row 缺失时 `NOT AVAILABLE / NOT VERIFIED`、不得用 Case B/cycle/mock/fixture 替代、target-first-item 限制均已正确冻结。

但 Phase M 只描述 `nok_detail_evidence_fact_key` “绑定 accepted upstream evidence”，没有定义一个可执行、read-only、bounded 的 relation proof：例如该 key 必须在同一 `production_accepted_station_event_fact` authority 中解析为存在的 accepted upstream row，并按本 Case C 需要的最小 identity/role 条件核对。当前 migration 为该字段提供非空约束和索引，但没有由 schema 本身完成该 relation closure；仅凭 Case C row 的 non-null value、API exact item 和 22-field 表，不能排除该 key 不存在、指向错误 accepted row 或语义错误的 upstream relation。

这会允许一个不存在或错误绑定的 upstream relation 被声明为 Case C PASS，属于直接 false-PASS blocker。该问题不是要求通用 relation graph、D7/D8 matrix 或旧 Option C forensic archive；只需要补齐 named `nok_detail_evidence_fact_key` 的最小 bounded relation proof。

当前真实 Case C 状态仍为：`NOT EXECUTED / NOT CLAIMED`。

### DQ8 — Exact 22-field DB/API/Dashboard reconciliation

**PASS（planning boundary；未执行）。**

Runtime plan Phase N 固定：

```text
PostgreSQL production_accepted_station_event_fact raw row
-> API raw JSON exact 22-field item
-> Dashboard display rule / visible value
```

逐字段表包含 exact 22 fields、DB raw value、API raw JSON value、display rule、Dashboard visible value 和 PASS/FAIL。`fact_key`、source/time/content identity、historical config fields 和所有 cross-field closure 均要求来自同一 target item；placeholder 不得写入 API raw value。Gate A 已关闭的 strict exact-envelope、field type/nullability、numeric source-preservation/safe-integer、cross-field validation、single-request/no-retry/no-fallback consumer boundary 可承载 malformed item fail-closed。

当前状态：真实 DB/API/Dashboard reconciliation `NOT EXECUTED / NOT CLAIMED`。任一字段不一致时该 case 不得 PASS。

### DQ9 — Raw/display/evidence classification separation

**PASS。**

计划和现有 consumer 明确分离 DB raw value、API raw JSON value、display rule、Dashboard visible value。`null`、empty string、number/string 及 human-readable placeholder 不可静默混写；placeholder 只允许在 display layer，并需对应 API 原始值。

证据分类同样保持：focused tests 为 synthetic/focused implementation evidence；TypeScript/Next build 为 local source/build evidence；Compose config 为 static parsing evidence；image inspect 为 image identity；Dashboard/API `/health` 为 process/API+DB readiness under current semantics；DB raw row + API raw item + Dashboard mapping 只证明 named target 的 real DB-backed three-layer evidence；缺失 Case C 只能为 `NOT AVAILABLE / NOT VERIFIED`。

### DQ10 — Claim scope and fail-closed terminal

**HOLD（由 `DQ-RUNTIME-EMPTY-1` 与 `DQ-RUNTIME-CASE-C-REL-1` 传播）。**

计划将 real claim 限定为独立 bounded request 的目标 `items[0]` 和 named Case A/B/C exact 22-field reconciliation，不扩大为整页、window、database、产线、历史配置或产品整体。mandatory Case A/B、known-empty、pagination 或对应 exact 22-field reconciliation 失败不得 overall PASS；Case C 缺失只写 `NOT AVAILABLE / NOT VERIFIED`，不伪造 PASS。

不过，在 known-empty 缺少 DB zero-row authority、Case C relation closure 缺少可执行 proof 的情况下，上述 terminal wording 仍无法关闭两个 false-PASS path。因此 overall 仍为 `HOLD`。

## 4. Focused Data Quality assessments

### Accepted-fact source assessment

除 known-empty authority omission 外，source boundary 通过：唯一来源是 `production_accepted_station_event_fact`；API `DTO_FIELDS` 逐字段读取该表；legacy/raw/diagnostic/fixture/current-config/API mock/fallback/join filler 均被排除；查询类别是 bounded read-only，禁止 DB write、migration、restore、ACK/read_done mutation。

### Known-empty assessment

UI stale-truth clearing 与 API empty shape 已有 planning/consumer support，但必须增加同一 bounded scope 的 PostgreSQL zero-row authority record，否则“empty”仍可能只是 API/UI empty，而非 accepted production fact authority 的 empty。

### Pagination assessment

Page 1/page 2 scope、opaque cursor、stable ordering、key-set completeness 与 page-only summary 已闭合；real execution 仍未发生。

### Case A/B/C assessment

- Case A：mandatory real accepted `station_result` OK，未执行。
- Case B：mandatory real accepted `station_result` NOK，未执行。
- Case C：conditional real accepted `station_nok` detail；缺失时必须 `NOT AVAILABLE / NOT VERIFIED`，但存在时的 upstream `fact_key` relation proof 尚未在 plan 中 executable 化。

### Exact 22-field assessment

22 个字段、same-target-item、DB/API/display 三层表和 FAIL-closed 规则均已定义；真实对账尚未执行。

### Raw/display separation assessment

Gate A raw-preserving parser、view model `raw/text/kind`、row-role display rule 和 empty/error clearing boundary 与本次 runtime plan 一致，未见 placeholder 冒充 API raw value 或 current-config 覆盖 historical value 的路径。

### Identity/config/time lineage assessment

`fact_key` 是主 identity；`source_event_id`、`content_fingerprint`、`event_ts`、`accepted_at` 独立核对；line/PLC/station/type/profile/config fields 来自同一 historical accepted row。未引入旧 Option C、manifest identity、D7/D8 matrix 或通用 lineage graph。

### Evidence classification assessment

当前静态、synthetic、local build、Compose parse、image/process/API health 证据均未被允许升级为 real DB-backed three-layer closure；真实 Case A/B/C 和 exact 22-field reconciliation 均保持 `NOT EXECUTED / NOT CLAIMED`。

## 5. Blockers

### `DQ-RUNTIME-EMPTY-1` — Known-empty 缺少 PostgreSQL bounded zero-row authority

- plan section：`Phase L — known-empty 与 pagination evidence`
- false-PASS path：未来 execution 仅以“known no row”叙述、API `items=[]` 或 Dashboard explicit empty/screenshot 判定 empty；实际 bounded `production_accepted_station_event_fact` scope 未被证明为零行，可能把错误 scope、source/query defect 或 stale/legacy exclusion 误报为当前 production empty。
- minimal Architecture planning repair allowlist：
  - `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`
  - 仅修订 `Phase L`，必要时同步 `Phase P` 的 known-empty terminal wording；要求保存同一 `line_id/start_time/end_time/limit` scope 的 bounded read-only PostgreSQL zero-row result，source 只能是 `production_accepted_station_event_fact`，并保持“只证明该 scope”的 claim。

### `DQ-RUNTIME-CASE-C-REL-1` — Case C upstream evidence relation proof 未 executable 化

- plan section：`Phase M — real Case A/B/C`、必要时 `Phase N — exact 22-field reconciliation`
- false-PASS path：Case C row 的 `nok_detail_evidence_fact_key` 仅为 non-null 且 API/22-field 对账通过，但该 key 不存在、指向错误 accepted row 或不满足最小 upstream relation；仍可能被报告为 valid Case C companion closure。
- minimal Architecture planning repair allowlist：
  - `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`
  - 仅修订 `Phase M`，必要时同步 `Phase N/P`；定义 named `nok_detail_evidence_fact_key` 的 bounded read-only relation proof 和其 PASS/FAIL/HOLD/NOT AVAILABLE classification，不引入通用 relation graph、D7/D8 matrix、retained archive 或 schema/code repair。

本轮不修改 Architecture plan，不修改 migration、Collector、API、Dashboard、deployment guide 或既有 Data Quality reports。

## 6. Recommendations

```text
Recommendations:
- none
```

当前 plan 中已存在的 exact 22-field、Case A/B/C、fact_key、historical config/time、known-empty、pagination、raw/display separation、no synthetic fallback 和 evidence classification 均不是本轮重复提出的 Recommendation；它们已作为 DQ review criteria 评估。待两个 blocker 修复后，后续 Verification/runtime record 仍按既有 planning authority执行。

## 7. Evidence and validation

- checks run：read-only Git recovery；指定 authority/docs/code/test 顺序的静态阅读；DQ1–DQ10 static cross-reference；current consumer truth boundary review；new report conflict-marker check；new report `git diff --no-index --check /dev/null <file>` whitespace check。
- tests/typecheck/build：not run
- Docker/Compose/SSH/Pi/port/firewall/resource/API/DB/browser/PostgreSQL/real Case A/B/C/rollback/cancellation：not run
- allowlist compliance：exactly one new Data Quality report created；no existing file changed；no staged file
- cached diff：empty

`git diff --no-index --check` 对新 untracked file 返回 rc `1` 且无 whitespace output 属正常差异结果；没有执行任何 Git write。

## 8. Overall conclusion and next gate

**HOLD**

Data Quality planning gate：`HOLD`

Eligible for：

- Architecture planning repair only after PM approval；
- 修复完成后由独立新 Data Quality Thread 进行 focused planning re-review。

PM approval is required before：

- 任何 plan repair 之外的 implementation/docs repair；
- Verification planning review；
- Docker/Compose、SSH/Pi、port/firewall/resource、API/DB/browser runtime；
- PostgreSQL query、real Case A/B/C、rollback/cancellation；
- stage、commit、push、tag、deploy、rollback。

## 9. Thread 输出 / 上下文评估

- 本次输出长度：长；两个 blocker、DQ1–DQ10 逐项结论和最小 repair allowlist 已写入本报告。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：本轮已是独立 Data Quality planning gate，且需与 Architecture repair、Reliability closure、已关闭 Gate A consumer implementation、已关闭 Gate B static implementation 和旧 Dashboard URL Option C/strong-audit 分支隔离；待 PM 批准最小 plan repair 后再开新 Thread 复验。
