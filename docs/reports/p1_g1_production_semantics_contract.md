# P1-G1 Production Semantics Contract Report

## 1. 结论

**PASS / P1_G1_PRODUCTION_SEMANTICS_CONTRACT_FROZEN**

本 child 已完成 G1 docs-only production semantics freeze。结论只覆盖 accepted-fact Quality + accepted-fact Trace MVP 的语义合同；不表示 PM intake、implementation、REVIEWED、ACCEPTED、VERIFIED、STAGED、COMMITTED、PUSHED、runtime 或 production acceptance。

`PARENT_PM_INTAKE_REQUIRED = YES`。本报告不接受 G2、Reliability、Data Quality rereview、Verification 或任何后续 Gate，也不创建 successor task。

## 2. Task / authority identity

| field | value |
| --- | --- |
| 报告名称 | P1-G1 Production Semantics Contract Report |
| 任务名称 | P1-G1 Production Semantics Contract |
| 执行 Thread | Data Quality |
| task path | `docs/thread_handoff/pm_task_20260811T1046Z_p1_g1_production_semantics_contract.md` |
| task type | regular / non-symlink |
| task bytes | 19916 |
| task SHA-256 | `2a2cd04e16c446e9360ac524fa36b71e24cc70fa53e702d5380c47bf71bf9532` |
| authority | task file 是完整且唯一 authority；不继承 predecessor、P0、G2、review、runtime、remote、DB 或 Git authority |

task self-identity 在读取任何其它 repository content、Git、Python、test、probe、sub-agent 或写入之前完成，四项与 parent launcher 完全匹配。

## 3. Ordered required-reading manifest

以下 16 项按 task 固定顺序完成。第 1 项为已独立核验的 authority-bearing task；其余为 semantic/protected reads，未被提升为新的 authority：

1. `docs/thread_handoff/pm_task_20260811T1046Z_p1_g1_production_semantics_contract.md`
2. `docs/thread_handoff/pm_operating_rules.md`
3. `docs/current_status.md`
4. `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter.md`
5. `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_bootstrap_dry_run.md`
6. `docs/reports/shadow_pm_p1_quality_trace_local_mvp_ledger.md`
7. `docs/reports/p1_g0_production_source_adequacy_semantic_boundary_freeze.md`
8. `docs/reports/p1_production_truth_semantics_trusted_consumption_plan.md`
9. `db/migrations/007_accepted_station_event_visibility.sql`
10. `api/app/routes/accepted_station_events.py`
11. `api/tests/test_accepted_station_events_api.py`
12. `api/tests/test_accepted_station_events_api_db_backed.py`
13. `api/app/routes/kpi.py`
14. `api/app/routes/trace.py`
15. `docs/kpi_definitions.md`
16. `config/lines/demo_3_station.yaml`

语义输入结论：migration 的 constraints/identities、accepted-events API 的 accepted-fact-only bounded read 与测试的 no-fallback/read-only/DTO assertions 支持 G1；legacy KPI/Trace 与 KPI 文档仅作为反例和兼容边界；当前 YAML 仅为 conditional auxiliary evidence。

## 4. Fresh live repository facts

| check | observed |
| --- | --- |
| physical cwd | `/Users/chenjie/Documents/MES/edge-mes-demo` |
| Git top-level | `/Users/chenjie/Documents/MES/edge-mes-demo` |
| branch | `main` |
| HEAD | `dbe5706e4b01387101f2a4666e73f3c13ffeb0e9` |
| origin/main | `2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35` |
| `origin/main...HEAD` | `0<TAB>1` |
| cached/staged diff | empty |
| tracked dirty set | exactly `docs/current_status.md`, `docs/thread_handoff/pm_operating_rules.md` |
| task path status | expected untracked Goal-control artifact; not staged/indexed/rewritten |

受保护 tracked docs 与 task artifact 均未修改；任何 Git mutation 均未执行。

## 5. Output prestate and exact contract binding

两个 task-owned outputs 在 child entry 均为 ABSENT、non-symlink；未采用既有同名文件。首个 output write 前已冻结 execution lock：task identity、ordered-read completion、fresh root/Git facts、两项 ABSENT prestate、exact write allowlist、contract invariants、Data Quality child role、zero nested-subagent intent、zero external/Git authority 与 fail-closed PASS/HOLD rules 均已固定。

### Contract artifact

| field | value |
| --- | --- |
| path | `docs/contracts/production_metrics_contract.md` |
| final type | regular / non-symlink |
| bytes | 8229 |
| SHA-256 | `2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e` |
| state | `WRITTEN`; PM `REVIEWED/ACCEPTED/VERIFIED` not established |

### Report artifact

| field | value |
| --- | --- |
| path | `docs/reports/p1_g1_production_semantics_contract.md` |
| prestate | ABSENT / non-symlink |
| final self-identity | post-write final audit and chat manifest record the regular type, bytes and SHA-256; self-hash is not embedded because changing it would change the report bytes |
| state | `WRITTEN`; PM `REVIEWED/ACCEPTED/VERIFIED` not established |

该 report 的 review/decision statements bind to the exact contract bytes above, not merely to its path or title。

## 6. Frozen production semantics

### 6.1 Authority and evidence boundary

`production_accepted_station_event_fact` is the sole P1 `PRODUCTION_AUTHORITY` for accepted station-business facts。`station_result.production_result` drives OK/NOK; accepted NOK code/detail remains bound to accepted business evidence fields and evidence fact key。raw/normalized candidate、raw payload/raw hex、adapter diagnostics、legacy rows、ACK/read_done 与 runtime state remain non-production evidence。

### 6.2 Quality

station-scoped Quality reads accepted `station_result` only：`ok` is good，`nok` is NOK，denominator is accepted `ok` + `nok`，`skip`/`not_applicable` are neither and are excluded from denominator。Empty denominator is `PARTIAL` or `UNAVAILABLE`，never numeric zero/0%。Station-scoped accepted-result Quality is `SUPPORTED`; line/terminal Quality is conditional on exact historical config lineage。

### 6.3 Timeline

Accepted timeline uses only accepted event facts with bounded half-open `[start,end)` windows and deterministic `(event_ts ASC, accepted_at ASC, fact_key ASC)` ordering。Grouping/pairing is allowed only with explicit shared producer identity。

### 6.4 unit_id / DMC Trace and missing station

Non-null accepted `unit_id` and DMC use exact equality。Null/missing identity is explicit `PARTIAL`，with no synthetic identity、legacy fallback、nearest-time fill or genealogy inference。Missing station is visible as `missing/unknown`，not inferred as OK/skip/present。

### 6.5 Historical lineage and dynamic route

Dynamic terminal/order/line output requires exact historical `config_hash` + `config_version` resolution。Current YAML is only conditional auxiliary evidence；it is not historical authority for mismatched facts。Fixed WS03 is forbidden。Unresolved/mixed lineage yields explicit `PARTIAL`/`UNAVAILABLE` and no numeric line claim。

### 6.6 Cycle time and ideal CT

Station cycle time remains `PARTIAL` without a producer-authoritative pairing key。Adjacent-row、counter-only、time-proximity、nearest-event and legacy `cycle_event` fallbacks are forbidden。Ideal CT remains `PARTIAL` without exact historical profile binding；current YAML or legacy 30s is not sufficient。

### 6.7 Performance / Availability / Full OEE

Performance is `UNSUPPORTED` without exact historical ideal CT and authoritative operating denominator。Availability is `UNSUPPORTED` without planned production time、planned downtime and authoritative machine-state timeline。Full OEE has no numeric claim while A/P are unsupported；`A × P × Q` must not be synthesized。

### 6.8 Status vocabulary

`SUPPORTED` means the declared scope/window/identity/source semantics are complete；`PARTIAL` means accepted facts are usable but completeness/identity/lineage/pairing is insufficient；`UNAVAILABLE` means a required source/lineage is absent for this query；`UNSUPPORTED` means the Goal has not established the required authority。None of these states permits a false numeric upgrade。

## 7. Explicit flags and migration boundary

```text
LEGACY_KPI_FALLBACK = NO
LEGACY_TRACE_FALLBACK = NO
TIME_PROXIMITY_TRACE_FILL = NO
FULL_GENEALOGY_CLAIM = NO
FULL_OEE_NUMERIC_CLAIM = NO
FIXED_WS03_PRODUCTION_AUTHORITY = NO
DB_MIGRATION = 0
PARENT_PM_INTAKE_REQUIRED = YES
```

G0 `PARTIAL/UNSUPPORTED` boundaries are preserved：`unit_id` Trace、DMC Trace、historical route/order/terminal、throughput、station cycle time 与 ideal CT remain `PARTIAL`; Performance、Availability、Full OEE remain `UNSUPPORTED`。No new migration is required or authorized。

## 8. Evidence classification and action counters

本 child 建立的是 local static/docs evidence only。未建立 runtime、DB、API runtime、remote 或 production evidence；历史 report/status 中的 accepted/runtime facts 只按其既有边界消费，不被本 child 重证明或升级。

| action / mutation class | count |
| --- | ---: |
| nested sub-agents | 0 |
| Ledger modification | 0 |
| task/Charter/Bootstrap/Goal Prompt/current_status modification | 0 |
| product/source/test/config/schema/frontend mutation | 0 |
| Collector / V-PLC / runtime mutation | 0 |
| DB migration | 0 |
| DB/API runtime | 0 |
| Python | 0 |
| tests/build/lint/formatter | 0 |
| network/SSH/Docker/remote | 0 |
| PLC/production stimulus | 0 |
| Git stage/commit/push/tag/reset/stash/restore/checkout/rebase/merge/clean | 0 |

Task-owned writes were exactly two A0/A1 durable outputs：one contract and one report。No other repository write occurred。

## 9. Validation and changed-path accounting

Completed or required final local checks are limited to task/output identity, physical cwd/Git metadata, exact-path prestate/status, exact output regular/non-symlink identity, exact-path text checks for required headings/flags/forbidden fallbacks, and `git diff --check` against the two outputs。No Python/test/build/lint/formatter/DB/API runtime/network/SSH/Docker/remote/PLC/production command was used。

Child-owned changed paths are exactly:

- `docs/contracts/production_metrics_contract.md`
- `docs/reports/p1_g1_production_semantics_contract.md`

The pre-existing tracked dirty docs remain protected and are not child changes；the task file remains a pre-existing Goal-control artifact and is not adopted or staged。`STAGED = NO`、`COMMITTED = NO`、`PUSHED = NO`。

## 10. Recommendations / MVP alignment

Recommendations are non-blocking carry-forward items, not G1 blockers：

- `NEXT_REVIEW_CARRY_FORWARD`: parent intake should preserve the exact contract bytes and re-check that G2, if separately authorized, does not add legacy/time-proximity/fixed-WS03/synthetic fallbacks。
- `P1_G3_OR_LATER_BACKLOG`: historical config registry/lineage lookup、producer pairing identity、Performance/Availability sources and Full OEE semantics require independent later authority。
- `FIELD_VALIDATION_BRANCH_INPUT`: field data may inform source adequacy only through parent independent intake；this child imported no parallel branch authority。

MVP 路径一致性：`MVP-ALIGNED WITH BACKLOG ITEMS`。本 Gate 新增的是 truthful semantic contract 与 durable report；没有 governance/validation inflation、product implementation、schema expansion 或 claim upgrade。

## 11. State distinctions and next gate

```text
WRITTEN = YES
REVIEWED = NO
ACCEPTED = NO
VERIFIED = NO
STAGED = NO
COMMITTED = NO
PUSHED = NO
RUNTIME_LOADED = NOT ESTABLISHED
PRODUCTION_ACCEPTED = NOT ESTABLISHED BY THIS CHILD
PARENT_PM_INTAKE_REQUIRED = YES
NEXT_GATE = PARENT_SHADOW_MAINLINE_PM_INDEPENDENT_INTAKE_OF_EXACT_G1_OUTPUTS
```

唯一 next gate 是 parent Shadow Mainline PM 独立 intake exact contract/report identities、changed paths、semantic claims、Git state 与 MVP alignment。只有 parent 对 unchanged G1 contract state 作出独立接受后，parent 才可另行生成 fresh P1-G2 task；该 child 不预创建、不接受、不推断 G2 或 review authority。

## 12. Thread terminal

```text
G1_TASK_SELF_IDENTITY_PASS = YES
G1_CONTRACT_PATH = docs/contracts/production_metrics_contract.md
G1_REPORT_PATH = docs/reports/p1_g1_production_semantics_contract.md
G1_OUTPUTS_PRESTATE = ABSENT
G1_CONTRACT_BYTES = 8229
G1_CONTRACT_SHA256 = 2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e
G1_REPORT_BYTES = <recorded by final audit and chat manifest>
G1_REPORT_SHA256 = <recorded by final audit and chat manifest>
G1_PRODUCT_SOURCE_MUTATIONS = 0
G1_DB_MIGRATIONS = 0
G1_COLLECTOR_CHANGES = 0
G1_FRONTEND_CHANGES = 0
G1_REMOTE_ACTIONS = 0
G1_GIT_MUTATIONS = 0
G1_MVP_ALIGNMENT = MVP-ALIGNED_WITH_BACKLOG_ITEMS
G1_CHILD_TERMINAL = PASS / P1_G1_PRODUCTION_SEMANTICS_CONTRACT_FROZEN
```

本 report 写入完成后必须执行 final exact-path audit；若 audit 发现非 regular/non-symlink output、bytes/hash mismatch、非 allowlist changed path、staged path、protected dirty drift 或 diff-check failure，结果应 fail-closed 为具体 HOLD，且不得 repair/retry/cleanup/rollback。

