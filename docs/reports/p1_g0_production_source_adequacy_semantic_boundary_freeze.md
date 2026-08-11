# P1-G0 Production Source Adequacy & Semantic Boundary Freeze Report

状态：`PASS WITH RECOMMENDATIONS`

## 1. 报告与任务

- 报告名称：P1-G0 Production Source Adequacy & Semantic Boundary Freeze Report
- 任务名称：P1-G0 Production Source Adequacy & Semantic Boundary Freeze
- 执行 Thread：Architecture / Integration
- Report delivery mode：`REPOSITORY_DURABLE_REPORT`
- 精确报告路径：`docs/reports/p1_g0_production_source_adequacy_semantic_boundary_freeze.md`
- Exact artifact paths：none
- 本报告仅表示 `WRITTEN`；不表示 `REVIEWED`、`ACCEPTED`、`VERIFIED`、`STAGED`、`COMMITTED`、`PUSHED`、`DEPLOYED` 或 `ACTIVATED`。

## 2. Terminal conclusion

P1-G0 通过 source adequacy 与 semantic boundary 冻结，结论为 `PASS WITH RECOMMENDATIONS`。

结论边界：

- accepted station-event facts 足以支持一个 accepted-fact-only 的 Quality + 基础 Trace vertical slice，不需要为该 slice 新增 DB migration；
- 该结论不把当前 YAML 当作历史配置真源，不把 `cycle_event`、`production_snapshot`、`production_unit`、adapter diagnostics 或 raw evidence 提升为 P1 production authority；
- dynamic terminal、dynamic station order、ideal cycle time 和 line-level output 只有在 `config_hash/config_version` 能解析到对应 immutable historical config 时才可使用，当前 required-reading surface 未证明这一历史解析链；
- station cycle time 缺少被当前 authority 明确冻结的 start/complete 同周期 pairing key，不能用时间接近推断；
- Performance、Availability、Full OEE 当前不能形成生产真值；应显式返回 `PARTIAL`/`UNAVAILABLE`，不得计算假 OEE；
- 本 Gate 没有阻塞 G1 contract planning。下一 Gate 只有一个：`PM Independent Intake — P1-G0 Production Source Adequacy & Semantic Boundary Freeze`。

## 3. Scope、authority 与排除

本轮只执行 task file 授权的本地只读 Architecture / Integration 分析，以及该 exact report path 的 durable report 写入。

没有授权、也没有执行：

- 产品代码、schema、config、API、frontend、Collector 或 V-PLC 修改；
- DB 连接、DB 读写、API runtime request、测试/build/lint/formatter；
- SSH、网络、Docker/Compose、remote/runtime/PLC/V-PLC action、production stimulus；
- B1 execution、第二次 B1 reassessment、P0 reopen、sub-agent；
- Git stage、commit、push、tag、reset、stash、restore、checkout、rebase、merge、clean。

## 4. Task self-identity 与 fresh Git baseline

### 4.1 Authoritative task file

task self-identity gate 在任何其他 repository content、Git、Python、测试、probe、sub-agent 或写入之前完成：

- path：`docs/thread_handoff/pm_task_20260811T0856Z_p1_g0_production_source_adequacy_semantic_boundary_freeze.md`
- type：regular / non-symlink
- bytes：`18862`
- SHA-256：`956734b3462bfafbfc7fe40a669ed842b5cb18fb89dcc8644508877acc1cc614`
- launcher 与 task file 的 path/type/bytes/SHA-256/authority 一致；无 launcher mismatch。

### 4.2 Fresh local/Git facts

| check | observed fact |
| --- | --- |
| physical cwd | `/Users/chenjie/Documents/MES/edge-mes-demo`，与 task declared project root 相同 |
| Git top-level | `/Users/chenjie/Documents/MES/edge-mes-demo`，与 cwd/root 相同 |
| branch | `main` |
| HEAD | `dbe5706e4b01387101f2a4666e73f3c13ffeb0e` |
| origin/main | `2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35` |
| `origin/main...HEAD` | raw count `0<TAB>1`；即 HEAD ahead 1、behind 0 |
| cached diff | empty |
| tracked worktree diff | only `docs/current_status.md` and `docs/thread_handoff/pm_operating_rules.md` |
| exact-path prestate | task file `??`、P1 plan `??`；sole report absent and non-symlink；two protected docs `M` |

受保护的 `docs/current_status.md` 与 `docs/thread_handoff/pm_operating_rules.md` 未被编辑、规范化或 stage。task/plan 的 untracked planning-artifact 状态未被清理、采用或改写。

## 5. Required-reading completion

以下 24 项按 authoritative task file 的固定顺序完成；所有语义证据均来自这些 exact paths，未使用 conversational memory 作为产品证据：

1. `docs/thread_handoff/pm_task_20260811T0856Z_p1_g0_production_source_adequacy_semantic_boundary_freeze.md`
2. `docs/thread_handoff/pm_operating_rules.md`
3. `docs/thread_handoff/chatgpt_pm_handoff_260811-1412.md`
4. `docs/reports/p1_production_truth_semantics_trusted_consumption_plan.md`
5. `docs/reports/shadow_pm_p0_remote_closure_ledger.md`
6. `docs/reports/sprint4_d2_r7b_p0_rc_production_path_revalidation_accepted_fact.md`
7. `docs/current_status.md`
8. `docs/roadmap.md`
9. `docs/reports/next_architecture_plan.md`
10. `docs/kpi_definitions.md`
11. `db/migrations/007_accepted_station_event_visibility.sql`
12. `collector/app/services/storage.py`
13. `api/app/routes/accepted_station_events.py`
14. `api/tests/test_accepted_station_events_api.py`
15. `api/tests/test_accepted_station_events_api_db_backed.py`
16. `api/app/routes/kpi.py`
17. `api/app/routes/trace.py`
18. `config/lines/demo_3_station.yaml`
19. `common/line_config/models.py`
20. `common/line_config/schema.py`
21. `common/line_config/loader.py`
22. `common/line_config/resolver.py`
23. `common/line_config/validator.py`
24. `tests/test_line_config.py`

## 6. Accepted P0 input与证据分类

### 6.1 Accepted P0 remote production evidence（历史语义输入）

`docs/reports/sprint4_d2_r7b_p0_rc_production_path_revalidation_accepted_fact.md` 记录的 accepted fact 为：

- `station_id=WS01`
- `production_result=ok`
- `cycle_counter=113095`
- `source_event_id=sha256:993ab6991534339db39c14180ebf6d1349a870035db7a3d5ed336147479ded8a`
- `fact_key=sha256:a8c7322bb96a6858aff226d25c23c731bb5cfcfa059a47b2ecefbea78efc8422`
- `content_fingerprint=sha256:36426c0d264fc4a14a531596844751cf13643019658ed4aaee7921f4872181f9`
- `event_ts=2026-08-11T05:44:25.000000Z`
- `accepted_at=2026-08-11T05:44:25.728731Z`
- `config_hash=0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38`
- `config_version=2026.06.26-slice-a`

这是已接受的 P0 生产事实，不是本轮 fresh remote observation。本轮没有重新 probe、remote call、DB query 或 production stimulus。

### 6.2 Repository/static evidence

- schema/constraints：`db/migrations/007_accepted_station_event_visibility.sql`；
- accepted-fact persistence：`collector/app/services/storage.py::insert_accepted_station_event_fact_no_commit`；
- bounded production read projection：`api/app/routes/accepted_station_events.py`；
- API source/DTO/window/cursor/no-fallback guards：对应两份 `api/tests/test_accepted_station_events_api*.py`；
- current route/profile config：`config/lines/demo_3_station.yaml` 及 `common/line_config/*`；
- legacy contrast：`api/app/routes/kpi.py`、`api/app/routes/trace.py`、`docs/kpi_definitions.md`。

### 6.3 Unsupported inference

以下不能从 current YAML、字段存在或 legacy behavior 推断：

- `config_hash/config_version` 对历史 resolved route/profile 的可逆查询；
- start/complete 事件的稳定同周期 pairing；
- planned production time、planned downtime、machine-state timeline；
- legacy `cycle_event` 的时间近邻结果等同于 accepted production fact；
- 自然 query window elapsed time 等同于 OEE planned/operating denominator。

## 7. P1 semantic source authority taxonomy

| authority class | 本轮定义 |
| --- | --- |
| `PRODUCTION_AUTHORITY` | 已通过 accepted decision、业务结果约束、稳定身份与 production-only projection 的事实；P1 数字与事实只能从此类 source 读取。 |
| `CONDITIONAL_AUXILIARY_AUTHORITY` | immutable config lineage 等辅助业务 source；只有 queried fact 的 `config_hash/config_version` 可精确绑定时才成立，current file 本身不能替代历史绑定。 |
| `COMPATIBILITY_OR_DIAGNOSTIC_ONLY` | legacy consumer、raw/normalized/candidate、ACK/runtime/adapter diagnostic 或旧表；可以保留兼容/调查用途，不能静默成为 P1 truth 或 fallback。 |
| `UNSUPPORTED_SOURCE` | 当前 required-reading surface 中不存在，或语义无法被稳定关联的 source；指标必须显式 unavailable/unsupported。 |

具体 source 归类：

- `production_accepted_station_event_fact`：`PRODUCTION_AUTHORITY`，且仅限 accepted station-event business facts；表注释和 constraints 排除 non-accepted/diagnostic/raw payload authority。
- `api/app/routes/accepted_station_events.py`：accepted fact 的 bounded read projection；不创建新的事实 authority，也不允许 fallback。
- `config/lines/demo_3_station.yaml` + loader/resolver/validator：`CONDITIONAL_AUXILIARY_AUTHORITY`；可为当前 config 提供 route/order/profile 值，但只有 immutable historical lineage match 后才可用于历史 query。
- `production_snapshot`、`cycle_event`、`station_event`、`production_unit`、`quality_event`、raw/adapter diagnostics：`COMPATIBILITY_OR_DIAGNOSTIC_ONLY`。
- planned schedule、planned downtime、authoritative machine-state timeline、explicit cycle-instance pairing：当前为 `UNSUPPORTED_SOURCE`。

## 8. Source Adequacy Matrix

分类只表示本行定义的严格 product meaning 是否已经被当前 source authority 支持；`SUPPORTED` 不表示所有 scope、历史配置或完整 OEE 都可用。

| # / semantic | intended product meaning | exact source fields / objects | authority class | required correlation / key / window semantics | historical-config requirement | failure / absence behavior | current classification | minimum missing prerequisite when not SUPPORTED |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Station OK/NOK | 在明确 station scope/window 内展示 accepted station result 的 OK/NOK；`skip`/`not_applicable` 不伪装成 OK/NOK。 | `production_accepted_station_event_fact.event_type='station_result'`; `production_result`; `line_id`, `plc_id`, `station_id`, `cycle_counter`, `event_ts`, `accepted_at`, `fact_key`。 | `PRODUCTION_AUTHORITY` | 只算 accepted `station_result`；`event_ts >= start AND event_ts < end`；按 `fact_key` 去重/稳定分页；不读 legacy result。 | station-level result 本身不需要 route config；line terminal aggregation 另受 rows 6/9 约束。 | source unavailable 503；invalid scope/window 422；缺 result 的非-`station_result` row 不计入；不以零代替 unavailable。 | `SUPPORTED` | none for the explicitly scoped station-result meaning。 |
| 2. accepted NOK code | 展示 accepted business NOK code 与其 origin；仅 accepted NOK business evidence 可进入质量事实。 | `production_result='nok'` 时的 `nok_code`, `nok_origin`；`event_type='station_nok'` 的 `nok_detail_code`, `nok_detail_source_event_id`, `nok_detail_evidence_fact_key`；migration constraints `ck_production_accepted_station_result_nok_authority`、`ck_production_accepted_station_nok_detail_authority`。 | `PRODUCTION_AUTHORITY` | `station_result` NOK 必须有 code/origin；detail 必须绑定 accepted upstream evidence fact key；window 与 line/station scope 明确；adapter reason/raw comparison 不可替代。 | code meaning 可由 accepted row 使用；config/NOK template 仅在需要解释历史 code 名称时按 matching lineage 使用。 | missing code/detail evidence fail closed or mark detail unavailable；diagnostic reason 不升格为 NOK code；不从 legacy `quality_event` 补写。 | `SUPPORTED` | none for accepted business code/detail fields; future label catalog lineage is optional auxiliary, not a fallback。 |
| 3. accepted event timeline | 按 accepted event facts 展示时间顺序的 station-event timeline，不合成未证明的 lifecycle。 | `event_type` ∈ `station_cycle_start`, `station_cycle_complete`, `station_result`, `station_nok`; `event_ts`, `accepted_at`, `fact_key`; station/line/plc/cycle/source identities。 | `PRODUCTION_AUTHORITY` | bounded half-open event window；stable order `(event_ts ASC, accepted_at ASC, fact_key ASC)`；同一 cycle 的 grouping 只有显式共享 identity 才允许。 | route/order only needed for route-shaped presentation；raw event timeline can be shown without current route。 | missing/duplicate/ambiguous identity remains an explicit data gap；不按相邻 event 或时间近邻合并；source unavailable fail closed。 | `SUPPORTED` | none for event-level timeline; per-cycle lifecycle pairing remains the separate CT limitation in row 8。 |
| 4. `unit_id` Trace | 按 accepted `unit_id` 查看该 identity 下可见的 accepted station events/results，并明确缺站，不声称 genealogy。 | accepted fact `unit_id`, `station_id`, `event_type`, `production_result`, `nok_*`, `cycle_counter`, `source_event_id`, `event_ts`, `config_hash`, `config_version`。 | `PRODUCTION_AUTHORITY` for non-null accepted rows；legacy trace is not an authority。 | exact equality on non-null `unit_id`；same line/plc/config lineage where required；bounded window；station completeness must be computed only from observed accepted rows. | route/order and terminal presentation require matching immutable config; raw identity lookup does not. | nullable `unit_id` means row is not discoverable by unit query；missing stations shown as missing/unknown, not inferred; no `production_unit` fallback。 | `PARTIAL` | G1 must freeze missing-unit/missing-station presentation and the minimum identity completeness contract; no synthetic fill or genealogy inference。 |
| 5. DMC Trace | 按 accepted DMC 查找 station-event facts；DMC 的 station-local/line-level meaning must be explicit, not guessed as parent-child genealogy。 | accepted fact `dmc`, plus `unit_id`, `station_id`, `event_type`, `cycle_counter`, `source_event_id`, `event_ts`, `fact_key`。 | `PRODUCTION_AUTHORITY` for non-null accepted DMC fields；config is conditional auxiliary for route display。 | exact DMC equality and explicit scope/window; no `cycle_event` join; no nearest-time match; no parent/child relation inferred from string or order。 | matching config required for dynamic route/order, not for direct field equality。 | nullable/ambiguous DMC returns partial trace/data gap；do not substitute `child_dmc`, `production_unit` or `cycle_event` silently；unsupported relation remains unavailable。 | `PARTIAL` | G1 must freeze DMC identity scope and relation semantics, or keep cross-station DMC trace explicitly partial；full genealogy is out of scope。 |
| 6. dynamic terminal station | 对 queried accepted facts 使用 config-resolved terminal station，定义 line output/terminal result；禁止固定 `WS03`。 | config `route_graph.terminal_station_id`, `route_graph.edges`, enabled stations；accepted fact `config_hash`, `config_version`, `line_id`, `station_id`, `event_type`, `production_result`。 | accepted rows `PRODUCTION_AUTHORITY` + config `CONDITIONAL_AUXILIARY_AUTHORITY`。 | resolve config by exact fact lineage first；then select accepted `station_result` at resolved terminal; bounded half-open window; no current-config substitution。 | required for every historical line-level query. `demo_3_station.yaml` has terminal `WS03` but version `2026.06.20-demo3-v1`; accepted P0 fact says `2026.06.26-slice-a`, so current YAML is not proof of historical mapping。 | missing/mismatched lineage => terminal/output `PARTIAL` or `UNAVAILABLE`; fail closed rather than silently using WS03/current YAML。 | `PARTIAL` | immutable config registry/snapshot lookup keyed by `config_hash` and `config_version`, containing route graph, is the minimum prerequisite。 |
| 7. dynamic station order | 按 queried fact 对应的 historical route/order 展示 stations，避免固定三列或 current order。 | config `stations[].station_order`, `station_id`, `station_enabled`, `route_graph.edges`; accepted `config_hash`, `config_version`, `station_id`。 | config `CONDITIONAL_AUXILIARY_AUTHORITY` + accepted facts `PRODUCTION_AUTHORITY`。 | exact config lineage match; route membership/order stable within query; observed accepted event identities only; no filesystem order as evidence。 | required for historical trace route presentation and completeness. | unresolved historical config => order/route unknown; preserve accepted facts but show route metadata unavailable; never reorder with current YAML silently。 | `PARTIAL` | same immutable historical config lineage lookup as row 6; G1 must define behavior for mixed config versions in one window。 |
| 8. station cycle time | 精确计算同一 station/cycle 的 `complete.event_ts - start.event_ts`，不使用时间接近猜测。 | accepted event types `station_cycle_start` / `station_cycle_complete`, `event_ts`, `cycle_counter`, `source_event_id`, line/plc/station/config identity。 | event facts are `PRODUCTION_AUTHORITY`; exact pairing source is currently `UNSUPPORTED_SOURCE`。 | requires producer-authoritative cycle-instance key shared by start/complete and uniqueness/duplicate rules; `cycle_counter` alone is not proven boot-safe; no ±N-second nearest match。 | matching config may be needed for station semantics, but it does not create a pairing key。 | absent/duplicate/mismatched pair => CT unavailable; do not average, subtract neighboring rows or use `cycle_event.cycle_time_ms` as fallback。 | `PARTIAL` | freeze a producer-owned `cycle_instance_id` or an explicitly boot-scoped start/complete identity contract with fail-closed duplicate/missing handling。 |
| 9. throughput/output | 统计 bounded window 内 resolved terminal 的 accepted result-event output；good 与 total 分开，不声称 legacy snapshot delta。 | accepted `station_result`, `station_id`, `production_result`, `unit_id`, `cycle_counter`, `fact_key`, `event_ts`; config terminal route。 | accepted fact `PRODUCTION_AUTHORITY` + config `CONDITIONAL_AUXILIARY_AUTHORITY`。 | terminal must be resolved by historical lineage; count accepted terminal result events in `[start,end)`; define whether count is event-count or unit-count; no fixed WS03, no `production_snapshot` delta。 | required for historical line output. | missing terminal lineage => output status partial/unavailable; missing unit means event-count may be available but unit-count is not; no zero fallback。 | `PARTIAL` | G1 must freeze terminal-output counting unit and historical config lookup; if unit-count is required, require stable accepted unit/cycle identity。 |
| 10. ideal cycle time | 读取 queried fact 对应 station/profile/config lineage 的 production ideal CT；不把 simulation timing 当 production ideal CT。 | config `stations[].cycle_profile`, `stations[].cycle_time_s`, `cycle_profiles[].ideal_cycle_time_s`; accepted `profile_id`, `config_hash`, `config_version`。 | config `CONDITIONAL_AUXILIARY_AUTHORITY`; accepted profile/lineage fields `PRODUCTION_AUTHORITY` as references only。 | exact `profile_id` plus exact config hash/version resolution; value must come from historical resolved config; no default `30s` and no current YAML substitution。 | mandatory. Current config availability is not historical-query authority。 | unresolved profile/hash/version => ideal CT unavailable; never use `docs/kpi_definitions.md` default 30s。 | `PARTIAL` | durable config snapshot/registry keyed by fact lineage and profile, or an equivalent accepted historical value binding, must be established before using it for Performance。 |
| 11. Quality component | 在明确 station/terminal scope 内以 accepted result evidence 计算 `Q = good_count / total_count`，并保留 denominator/data-sufficiency。 | accepted `station_result.production_result`, `station_id`, `event_ts`, `fact_key`; accepted NOK code/detail fields for defect evidence; line/window scope。 | `PRODUCTION_AUTHORITY`; config only conditional for line terminal selection。 | explicit scope and half-open window; good=`ok`, NOK=`nok`; define treatment of skip/not_applicable; count accepted result facts only; no raw/diagnostic/legacy fallback。 | station-scoped Q 不需要 route config；line-level terminal Q requires row 6 lineage。 | empty denominator is `UNAVAILABLE`/not a numeric zero-quality claim; missing terminal lineage makes line Q partial/unavailable; invalid source 503。 | `SUPPORTED` for explicit accepted-result station scope; line-level Q remains conditional on row 6。 | none for station-scoped Quality MVP; G1 must freeze terminal/skip denominator semantics for line Q。 |
| 12. Performance component | OEE Performance needs ideal CT and an authoritative runtime/operating denominator; it is not a raw event-rate cosmetic。 | ideal CT from row 10; accepted terminal/total result counts; required runtime denominator is not present in accepted fact/API/config sources。 | accepted/config are conditional inputs; denominator is `UNSUPPORTED_SOURCE`。 | requires same scope/window, historical ideal CT, and authoritative operating/run time; natural elapsed window is not sufficient by itself。 | historical ideal CT binding mandatory。 | missing denominator or lineage => `UNAVAILABLE`; do not calculate from `(end-start)` or neighboring event timestamps。 | `UNSUPPORTED` | authoritative operating-time source bound to the production window, plus historical ideal CT resolution, must be accepted; this is a later planning prerequisite, not a G0 repair。 |
| 13. Availability component | OEE Availability needs planned production time, planned downtime and authoritative machine-state/run-stop timeline。 | required sources: planned schedule/calendar, planned downtime facts, authoritative machine-state timeline; none exists in the accepted fact schema/current required source set。 | `UNSUPPORTED_SOURCE`。 | must correlate schedule/state to line/station and query window; distinguish planned, unplanned, unknown and unavailable; natural query-window elapsed time is explicitly rejected。 | historical schedule/state authority required。 | absent source => `UNAVAILABLE`; no substitute with API window duration, collector health, ACK, `production_snapshot` or current runtime state。 | `UNSUPPORTED` | establish an explicit Level-2 production state/schedule authority and contract; do not add it implicitly to G1/G2。 |
| 14. Full OEE | Only compute `A × P × Q` when all components are semantically available under the same scope/window and lineage。 | Quality row 11; Performance row 12; Availability row 13; same line/station/window/config authority。 | `PRODUCTION_AUTHORITY` only after all component authorities are independently accepted; currently unavailable。 | exact same scope/window/terminal/config; no component may be synthesized from a legacy source or natural elapsed time。 | route/profile/schedule/state historical lineage required。 | `A/P` missing => `Full OEE=UNAVAILABLE`; `PARTIAL` may expose component sufficiency states but must not expose a misleading percentage。 | `UNSUPPORTED` | independently accepted A/P sources and G1/G3 `AVAILABLE/PARTIAL/UNAVAILABLE` contract; no false OEE rule。 |

## 9. `production_accepted_station_event_fact` authority proof

不能只依据表名判断 authority。三层证据共同成立：

1. **Schema semantics**：`event_type` 只允许四类 accepted station-event；`station_result` 才能带非空 `production_result`；`production_result='nok'` 需要 `nok_code` 与 `nok_origin`；`station_nok` detail 需要 `nok_detail_code`、`nok_detail_source_event_id` 与 `nok_detail_evidence_fact_key`；`fact_key` 和 source identity 有唯一约束。
2. **Persistence semantics**：`collector/app/services/storage.py::insert_accepted_station_event_fact_no_commit` 按 `fact_key` 与 source identity 做同内容幂等、异内容冲突；写入字段直接来自 `AcceptedStationEventFact`，不是从 raw/legacy projection 推导；`config_hash/config_version`、event/source/fact/content identities 与 timestamps 被持久化。
3. **API semantics**：`api/app/routes/accepted_station_events.py` 的 `DTO_FIELDS` 逐字段来自该表；SQL 只读该表，绑定 `line_id` 与 `[start,end)`，cursor 绑定 scope/window/limit/order；测试明确禁止 legacy joins/fallback、raw/diagnostic leakage、ACK/read_done side effect，并在 source failure 时返回 503。

因此该表是 P1 accepted business fact 的 `PRODUCTION_AUTHORITY`，但不是自动提供 route registry、cycle pairing、schedule/state 或完整 OEE 的万能事实表。

## 10. Quality + Trace vertical slice 与 migration decision

### Decision

`NO_NEW_DB_MIGRATION_REQUIRED_FOR_P1_QUALITY_TRACE_VERTICAL_SLICE = YES`。

理由：当前表已经具备 Quality + accepted-fact Trace 所需的 accepted event/result/detail/identity surface：

- event：四类 accepted `event_type` 与 `event_ts/accepted_at`；
- result：`station_result.production_result` 的明确枚举与 station-result authority constraint；
- detail：accepted NOK code/origin 与 upstream evidence-bound detail；
- identity：line/plc/station/profile/config lineage reference、cycle counter、source event、fact key、content fingerprint、unit_id、dmc；
- read projection：bounded production API 已证明 no-fallback、same-source、read-only、window/cursor semantics。

G1/G2 可在不新增 migration 的前提下先冻结并消费：

- accepted station OK/NOK counts；
- accepted NOK code/detail distribution；
- accepted event timeline；
- non-null `unit_id`/`dmc` fact trace，配合 explicit missing identity/station presentation；
- station-scoped Quality component。

必要条件与限制：

- `unit_id`/`dmc` 是 nullable，不能把缺失 identity 补成 legacy identity；
- dynamic route/order/terminal/ideal CT 必须以 historical config lineage 解析，否则只展示 accepted facts 和 `data sufficiency` 状态；
- full Genealogy、parent/child/rework、exact station CT、Performance、Availability、Full OEE 不属于本 vertical slice 的已支持语义；
- 如果 G1 需要把 historical route/profile 作为强 production claim，而现有 config lineage 无法提供 exact lookup，最小补充 planning slice 是“immutable config lineage lookup keyed by `config_hash/config_version`”，不是立即新增 migration。

## 11. Cycle-time、terminal output 与 historical config decisions

### 11.1 Station cycle time

accepted fact surface 有 start/complete event types 与 timestamps，但没有在 required sources 中冻结的 cycle-instance id、boot-scoped identity 或 start/complete relational constraint。`cycle_counter` 是 accepted business field，不能在本轮额外推断它跨事件、跨 reboot 永远构成稳定 pair。

结论：`Station cycle time = PARTIAL`。只有 future accepted contract 明确证明同一 cycle key 的 start/complete 才能做 subtraction；当前不允许按相邻 counter、最近时间或 `cycle_event.cycle_time_ms` fallback。

### 11.2 Dynamic terminal 与 output

`config/lines/demo_3_station.yaml` 的 `route_graph.terminal_station_id=WS03`、edges `WS01→WS02→WS03`，loader/resolver/validator 也对 route reachability、station order 与 config hash 做当前文件级验证。但该文件 `config_version=2026.06.20-demo3-v1`，P0 accepted fact 的 `config_version=2026.06.26-slice-a`；required sources 没有可查询的 historical config registry/snapshot。

结论：不能把 current `WS03` 静默套到所有历史 facts。`Throughput/output` 与 line-level Quality 在 lineage 可解析时可按 resolved terminal 计算；否则必须 `PARTIAL/UNAVAILABLE`。G1 应冻结“terminal resolution failure = no numeric line output”，并禁止 fixed WS03。

### 11.3 Ideal cycle time / Performance

当前 YAML 的 `cycle_profiles[].ideal_cycle_time_s` 与 `stations[].cycle_time_s` 存在，validator 强制二者一致；loader 会为当前 `LineConfig` 生成 canonical `config_hash`。这只证明当前 config 内部一致，不证明 queried accepted fact 已绑定到该 historical profile value。

结论：ideal CT 为 `PARTIAL`；Performance 为 `UNSUPPORTED`。不得复制 legacy 默认 `30s`，也不得用 current YAML 或 query-window elapsed time冒充历史 ideal/runtime denominator。

## 12. Availability 与 OEE sufficiency

当前 production-truth surface 没有：

- planned production time / shift calendar；
- planned downtime intervals；
- authoritative machine-state run/stop/unknown timeline；
- 与 queried accepted facts 同 scope/window 的 operating-time denominator。

`api/app/routes/kpi.py` 的 natural window 与 `cycle_seconds=30.0`、`docs/kpi_definitions.md` 的 fixed WS03/default 30s、`api/app/routes/trace.py` 的 runtime/legacy state 都不能替代这些 source。

OEE sufficiency decision：

| component | current state | permitted product claim |
| --- | --- | --- |
| Quality | `SUPPORTED` for explicit accepted-result station scope; line terminal scope conditional | show accepted counts/rate with scope and denominator |
| Performance | `UNSUPPORTED` | show unavailable/data-insufficient; no percentage |
| Availability | `UNSUPPORTED` | show unavailable/data-insufficient; no natural-window substitute |
| Full OEE | `UNSUPPORTED` | no `A×P×Q` numeric claim; expose component sufficiency only |

## 13. Legacy KPI/Trace audit：不得复制的行为

### `api/app/routes/kpi.py` / `docs/kpi_definitions.md`

- reads `production_snapshot`, not accepted station-event facts；
- computes cumulative counter deltas using `machine_id` and an inclusive `ts <= end` window；
- `output-card.svg` defaults `cycle_seconds=30.0`，`summary` uses a natural last-24-hours window；
- historical document fixes line output/quality to `WS03` and uses legacy `cycle_event`/`production_snapshot`/`quality_event` vocabulary；
- empty/absent data is normalized toward zero/zero-rate rather than explicit source-unavailable semantics。

New P1 production APIs must not copy this source, fixed terminal, default CT, inclusive-window or zero-fallback behavior。

### `api/app/routes/trace.py`

- primary queries read `cycle_event`；`recent_traces` reads `production_unit` and a latest `cycle_event` lateral join；
- response is fixed to `{"WS01": ..., "WS02": ..., "WS03": ...}` and includes legacy `payload`/`ack_status` surfaces；
- `_fill_upstream_by_time` / `_find_upstream_event` can select a nearest event within ±90 seconds when explicit DMC is unavailable；
- `trace_query` seeds from legacy identifiers and `_current_cycle_identity` consults `collector_runtime_status`；
- these can be compatibility/diagnostic behavior, but cannot be P1 production authority, fallback, cycle pairing, genealogy or missing-station fill。

## 14. Minimum G1 contract input

### Ready to freeze

1. `production_accepted_station_event_fact` is the only P1 production fact source for accepted station business facts。
2. Accepted station OK/NOK uses `event_type='station_result'` and `production_result`；accepted NOK code/detail must remain evidence-bound。
3. Accepted event timeline is an ordered fact stream using `(event_ts, accepted_at, fact_key)` and bounded half-open windows。
4. Quality station scope can use accepted result facts only；good/NOK/denominator, skip/not_applicable and empty denominator must be explicit。
5. `unit_id`/`dmc` trace is exact-field lookup only when non-null；missing identity/station is visible data sufficiency, never legacy/time-near fill。
6. New P1 read APIs remain bounded/read-only/fail-closed and must not reuse `/kpi/*` or `/trace/*` source semantics。

### Must remain explicit PARTIAL/UNSUPPORTED

- historical terminal station and station order：`PARTIAL` until exact config lineage resolution；
- terminal output/line-level Quality：`PARTIAL` until terminal and counting-unit semantics are bound；
- station cycle time：`PARTIAL` with no pairing heuristic；
- ideal CT：`PARTIAL` until historical profile binding；
- Performance：`UNSUPPORTED` without ideal CT + authoritative runtime denominator；
- Availability：`UNSUPPORTED` without planned time/downtime/state timeline；
- Full OEE：`UNSUPPORTED` while A/P are unsupported；
- full Genealogy、unit relation、Hold/Rework、Data Gap/Missing Unit inference：out of scope。

### Smallest prerequisite planning slice

G1 本身可以继续，因为 unresolved items 可安全地保持显式 PARTIAL/UNSUPPORTED，不阻塞 Quality + Trace contract。若 G1 要把动态路线/terminal/ideal CT 作为强 product claim，唯一最小补充 planning slice 是：

`Immutable historical config lineage lookup keyed by accepted fact config_hash + config_version`

该 slice 只解决历史 route/order/profile lookup 与 fail-closed behavior；不自动授权 migration、API implementation、remote validation 或 Git mutation。

## 15. Blockers 与 recommendations

### Current-gate blockers

none。task self-identity、live Git baseline、required reading、matrix、authority taxonomy 与 zero-action boundary 均满足；没有需要 HOLD 的 contradiction。

### Recommendations carried to G1/G3

- G1 将 `SUPPORTED/PARTIAL/UNSUPPORTED`、data-sufficiency response 与 no-fallback 规则固化为 production semantics contract；
- G1 明确 line-level terminal/output 的 historical config resolution 和 mixed-config window behavior；
- G1 保留 station CT `PARTIAL`，不批准 time-proximity pairing；
- G3 单独处理 Performance/Availability/Full OEE，未建立 A/P source 前不得输出 Full OEE 百分比；
- 不修改 legacy `/kpi/*`、`/trace/*` 作为本 Gate 的修复动作，也不把 legacy compatibility cleanup 变成 G1 blocker；
- 若未来需要历史 config lookup，先做最小 planning slice，再由 PM 独立决定是否需要 model/migration。

## 16. MVP 路径一致性

分类：`MVP-ALIGNED WITH BACKLOG ITEMS`。

- approved MVP claim：把已经成立的 accepted production facts 可信消费为 Quality + Trace / bounded production semantics；
- minimum invariant：数字只能由 accepted facts 与明确的 immutable lineage 得出，不能由 legacy、synthetic、raw/diagnostic 或时间猜测补齐；
- newly introduced capability：本轮只新增 source decision/report，不新增 product capability、runtime topology、audit platform、retention model 或 threat model；
- complexity check：矩阵与 evidence 直接服务于防止 false PASS/stale truth；没有引入 generic evidence framework、Full Genealogy 或 OEE-first implementation；
- next smallest MVP action：PM independent intake G0，再由 PM 明确授权 G1 contract planning；不得从本报告推断 G1 implementation 或后续 phase authority。

## 17. Action counters 与 validation boundary

| counter | value |
| --- | ---: |
| Python | 0 |
| test/build/lint/formatter | 0 |
| DB read/write/client | 0 |
| API runtime request | 0 |
| network | 0 |
| SSH | 0 |
| Docker/Compose | 0 |
| remote | 0 |
| PLC/V-PLC | 0 |
| production stimulus | 0 |
| sub-agent | 0 |
| Git mutation | 0 |
| product/source/config/schema mutation | 0 |

Executed checks were limited to task identity stat/hash, physical cwd/Git metadata, exact-path Git status/diff checks, bounded navigation, and static reads of the 24 allowlisted paths. No tests are required or authorized for this static planning Gate。

## 18. Changed paths、protected continuity 与 report identity

Task-owned changed path is only:

- created: `docs/reports/p1_g0_production_source_adequacy_semantic_boundary_freeze.md`

The task file and P1 plan remain pre-existing untracked/unstaged planning artifacts；`docs/current_status.md` and `docs/thread_handoff/pm_operating_rules.md` remain pre-existing tracked dirty protected docs；cached diff remains empty。Post-write exact-path status and report identity are captured in the final window manifest after this file is materialized。

Report self-identity is intentionally not self-embedded: a report cannot contain its own final SHA-256 without changing those bytes. Final report bytes/SHA-256 are recorded by the post-write read-only audit in the Chat manifest。

## 19. Next gate 与 Thread output/context assessment

唯一 next gate：`PM Independent Intake — P1-G0 Production Source Adequacy & Semantic Boundary Freeze`。

该 next gate 只负责 PM 独立读取/核验本 durable report、判断 G0 acceptance 与 recommendations；本报告不创建 G1 task，不授权 implementation、DB/API/schema/frontend、remote、Git 或 later phase。

Thread context assessment：

- current output is a bounded durable report plus concise chat manifest；
- this Architecture / Integration Thread has completed its assigned scope and does not need to open/switch/create another top-level Thread；
- next work should be manually dispatched by Owner according to PM authority and may use a fresh task file；
- task-file sub-agent recommendation was `no` / exact scope `none`；actual sub-agent usage was `0`；no variance。

## 20. Final state distinctions

```text
WRITTEN=YES
REVIEWED=NO
ACCEPTED=NO
VERIFIED=NO
STAGED=NO
COMMITTED=NO
PUSHED=NO
DEPLOYED=NO
ACTIVATED=NO
```

本报告终止于 report write/manifest boundary。 

## 21. Post-write final changed-path audit

Materialization and final exact-path audit completed without any other write:

- report path is regular/non-symlink and exists;
- `git diff --cached --name-only` is empty;
- `git diff --name-only` contains only the two pre-existing protected tracked docs: `docs/current_status.md` and `docs/thread_handoff/pm_operating_rules.md`;
- exact-path `git status --porcelain=v1 --` shows only `M docs/current_status.md`, `M docs/thread_handoff/pm_operating_rules.md`, `?? docs/reports/p1_g0_production_source_adequacy_semantic_boundary_freeze.md`, `?? docs/reports/p1_production_truth_semantics_trusted_consumption_plan.md`, and `?? docs/thread_handoff/pm_task_20260811T0856Z_p1_g0_production_source_adequacy_semantic_boundary_freeze.md`;
- therefore the task-owned changed-path set is exactly the sole report path; the task/plan are preserved pre-existing untracked artifacts and the two tracked dirty docs remain unchanged.
