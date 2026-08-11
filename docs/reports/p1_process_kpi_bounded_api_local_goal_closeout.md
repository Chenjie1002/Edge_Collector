# P1 Process KPI + Bounded API Local Goal Closeout

## 1. Final PM intake

```text
GOAL_ID = P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1
FINAL_PM_INTAKE = PASS
GOAL_STATUS = COMPLETE
SHADOW_PM_GOAL_STARTED = YES
SHADOW_PM_STOP = YES
GOAL_TERMINAL = PASS / P1_PROCESS_KPI_BOUNDED_API_LOCAL_MVP_AUTONOMOUS_GOAL_COMPLETE
CURRENT_GATE = PM_FINAL_INTAKE
CURRENT_GATE_STATUS = GOAL_TERMINAL
P1_G5_EXECUTION_AUTHORIZED = NO
NEXT_ACTION = STOP
```

本报告是本 Goal 的最终本地 closeout。它只接受 bounded local Process Metrics API 的静态、fake-DB、compile、review 和 Verification 证据；不把任何 local evidence 提升为 DB-backed runtime、RUNTIME_LOADED、deployment、activation 或 production acceptance。

## 2. Goal authority and final scope

启动前已读取并核对用户指定的 Goal objective：

```text
/Users/chenjie/.codex/attachments/179d025c-c356-4bf7-8303-3cbc03969949/goal-objective.md
bytes = 11053
SHA-256 = f20fa65e2777c6f01ee8a8f5b3e37a0929999f4aa136e85ef85884d50a28a130
```

本 Goal 的 scope 仅为：先冻结 G3 Process KPI/OEE data-sufficiency contract，再实现 bounded station-scoped read-only API，最后完成本地 Reliability、Data Quality、Verification 和 parent final intake。禁止 P1-G5、remote/RPi、DB migration/runtime、Collector/config/PLC/V-PLC、frontend、Docker、生产 stimulus、Git publication 和所有 A5 外部/不可逆动作。

Final accepted semantic boundary：

```text
production_accepted_station_event_fact = sole accepted production truth
LEGACY_KPI_FALLBACK = NO
LEGACY_TRACE_FALLBACK = NO
FIXED_WS03_PRODUCTION_AUTHORITY = NO
TIME_PROXIMITY_CYCLE_PAIRING = NO
CURRENT_YAML_AS_HISTORICAL_AUTHORITY = NO
FULL_OEE_NUMERIC_CLAIM = NO
```

## 3. Final accepted authorities

```text
CAPSULE = docs/reports/p1_process_kpi_bounded_api_accepted_state_capsule.md
CAPSULE = bytes=8201,SHA-256=643b2c39e1e37da542cf077be71d511e75035c0da08e6471f86a610e290a2b3a
CHARTER = docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_charter.md
CHARTER = bytes=20025,SHA-256=cfc05c53ef03f890cf5be2228f47369c2042457294384b82db9bd85b8c348dd3
G3_CONTRACT = docs/contracts/production_process_kpi_contract.md
G3_CONTRACT = bytes=28427,SHA-256=776e744314f9ec33884765c20f8d88dab45afeda74354cf7e10e7fc226809252
```

G3 的非继承边界已保留：本版本没有 historical config registry，也没有 Performance、Availability、Full OEE numeric、line/terminal authority 或 cycle pairing authority。

## 4. Final candidate identity set

Final local candidate is exactly:

| path | bytes | SHA-256 |
| --- | ---: | --- |
| `api/app/main.py` | 524 | `038f7ea2c900f8288742586fe38430f6f5e0ce352fd1e4d7117d0e467f811dad` |
| `api/app/routes/process_metrics.py` | 19771 | `a7313117776e6ba8255bf2f60755bfad5a6bcf510767f0129720f8425984f1cb` |
| `api/tests/test_process_metrics_api.py` | 23821 | `6eb1e0ced1cb745755f94b3719c1a91923ca7f6ffe4d538b21004b2a9432566a` |

`api/app/main.py` only adds the `process_metrics` import and `app.include_router(process_metrics.router)` registration. Protected predecessor identities remained unchanged:

```text
docs/contracts/production_metrics_contract.md = bytes=8229,SHA-256=2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e
api/app/routes/quality_trace.py = bytes=9538,SHA-256=6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a
api/tests/test_quality_trace_api.py = bytes=13296,SHA-256=bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c
```

## 5. Gate sequence and parent intake results

| Gate | Durable result | Parent intake / durable report |
| --- | --- | --- |
| `CAPABILITY_CHECK` | PASS | `docs/reports/p1_process_kpi_bounded_api_capability_check_20260811T1456Z.md` — bytes 8733, SHA `4ab4872609c9ecfd771031f9f0c73d38b99ffbd2fd3497b72c06480b726e5b3c` |
| `P1-G3_PROCESS_KPI_CONTRACT` | PASS WITH RECOMMENDATIONS; accepted | `docs/reports/p1_g3_process_kpi_contract_20260811T1505Z.md` — bytes 20348, SHA `306824e4e4326001f835ca759e2e0bc3ece12d999f0a1a8f990542992a6b8ff3` |
| `P1-G4-I_BOUNDED_PRODUCTION_METRICS_API` | PASS; accepted | `docs/reports/p1_g4_i_bounded_production_metrics_api_20260811T1525Z.md` — bytes 14056, SHA `32d041fc243041be87ee7d43339237e7fa7a5aa53c0be904ed35a0afedab0482` |
| `P1-G4-R_FOCUSED_RELIABILITY` | HOLD: two real fail-closed defects | `docs/reports/p1_g4_r_focused_reliability_review_20260811T1555Z.md` — bytes 12543, SHA `11c85624f2ef2d4943434b19bbbeaa5cdbc333fdc7f9eb73a796c0f0936a5c6e` |
| bounded product repair | F1/F2 repaired; child HOLD only on pre-existing cache audit boundary | `docs/reports/p1_g4_repair_accepted_fact_lineage_nok_detail_20260811T1605Z.md` — bytes 9073, SHA `e9b07c1b4585302a2aa1291fe7fed28eb8cb4334213d1283755e49420f03d0ba` |
| control-plane recovery | PASS: cache baseline reconciled | `docs/reports/p1_g4_repair_cache_baseline_recovery_20260811T1615Z.md` — bytes 11639, SHA `0c9bfbabf6e14e7baefa13883c58e8c6d81ce3907ea12ba75690a042f50b5aee` |
| fresh `P1-G4-R` | PASS; Reliability accepted | `docs/reports/p1_g4_fresh_reliability_review_20260811T1635Z.md` — bytes 11287, SHA `9cbeadce9563c7b5e7c42e2a3b47d4312e9875c7c227bf56c3be294e5534e8e4` |
| `P1-G4-DQ_FOCUSED_DATA_QUALITY` | PASS; Data Quality accepted | `docs/reports/p1_g4_dq_focused_data_quality_review_20260811T1645Z.md` — bytes 15342, SHA `80cc2d38d8be1b009f167dbaa5897d05ff9bbbe394605e41b26d2ed248c2d770` |
| `P1-G4-V_FOCUSED_VERIFICATION` | PASS; parent final intake pending at report write | `docs/reports/p1_g4_v_focused_verification_20260811T1700Z.md` — bytes 14084, SHA `f1d362e4d49e1b9b32cab6e75ca91cb40a71f6af4df8dc23c7681e58372f8a52` |

The first Reliability HOLD was not hidden or downgraded. Its F1/F2 findings were repaired within the exact route/test scope, the pre-existing cache audit boundary was reconciled with the single control-plane recovery budget, and fresh Reliability/DQ/V reviews all bound the new candidate identity set above.

## 6. Product truth and fail-closed outcome

The final route:

- serves exactly `GET /api/v2/process-metrics` with four required query parameters and strict bounded `[from,to)` RFC3339 windows;
- reads only `production_accepted_station_event_fact` inside `BEGIN READ ONLY` with bounded timeouts and deterministic `(event_ts, accepted_at, fact_key)` order;
- fails closed for missing/duplicate/conflicting `fact_key`, unknown result, source failure, invalid requests, and unsupported authority;
- leaves a single config tuple `UNRESOLVED` without an accepted historical resolver and leaves mixed tuples `MIXED`;
- checks `nok_code`, `nok_origin`, `nok_detail_code`, `nok_detail_source_event_id`, and `nok_detail_evidence_fact_key`, returning `QUALITY_NOK_DETAIL_INCOMPLETE`/`PARTIAL` when any required detail is missing;
- keeps valid empty windows distinct from source unavailable and does not zero-fallback unsupported metrics;
- does not emit numeric unit count, station CT, ideal CT, line/terminal count, Performance, Availability, or Full OEE claims.

## 7. Independent final local validation

Final bound local validation, independently repeated by Reliability, DQ, and Verification, is:

```text
focused Process Metrics suite = 34 passed
Process Metrics + predecessor Quality/Trace regression = 50 passed
in-memory compile and exact route registration = PASS
real DB connection = 0
```

The approved project runtime was Python 3.13.3 arm64, pytest 9.1.1, FastAPI 0.115.6, psycopg 3.2.3, base interpreter bytes 119328, SHA `f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5`.

The API cache/bytecode baseline is preserved rather than cleaned:

```text
inventory scope = api/.pytest_cache (recursive), api/**/__pycache__, api/**/*.pyc
inventory paths = 26
hashed file rows = 20
API_CACHE_SNAPSHOT_SHA256 = 6f6274909b4746818f1b0b4ab82a66c718a660b708ea2c4135c2cfe50ed67209
latest pre-existing mtime = 2026-07-05T21:16:01+0800
pre/post path-bytes-mtime = MATCH
```

## 8. Repository and Git boundary

Final pre-closeout read-only state:

```text
cwd = /Users/chenjie/Documents/MES/edge-mes-demo
git root = /Users/chenjie/Documents/MES/edge-mes-demo
branch = main
HEAD = cf4eac54d3f365b0addfaae13f5e7292e3233641
origin/main = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
origin/main...HEAD = 0<TAB>2
cached/staged = empty
git diff --check = PASS
status lines before this closeout report = 889
status SHA before this closeout report = e7178d862331b5e145318f12757ab0afdc98df3e43f7fa3c6b8a632e825d7b6e
tracked dirty continuity = api/app/main.py, docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
```

The large pre-existing untracked corpus and unrelated dirty files were preserved with path-scoped accounting. No stage, commit, push, tag, reset, stash, restore, checkout, rebase, merge or clean was performed. The closeout report's own SHA-256 is emitted after this write and recorded in the final Ledger; it is not embedded self-referentially here.

## 9. Budgets and action counters

```text
PRODUCT_REPAIR_GATES_USED = 1 / 3
CONTROL_PLANE_RECOVERY_GATES_USED = 1 / 1
TOTAL_DISPATCHED_GATES = 8 / 9
NO_PRODUCT_PROGRESS_STREAK = 0
MAX_NORMAL_CHILDREN_ACTIVE = 0 at terminal
NESTED_CHILDREN = 0

DB_RUNTIME_ACTIONS = 0
DB_MIGRATIONS = 0
REMOTE_ACTIONS = 0
DOCKER_ACTIONS = 0
PLC_VPLC_ACTIONS = 0
PRODUCTION_STIMULUS_ACTIONS = 0
GIT_MUTATIONS = 0
UNAUTHORIZED_ACTIONS = 0
```

## 10. State distinctions and stop boundary

```text
WRITTEN = YES for all durable task/report artifacts
REVIEWED = YES by child-local reviews and parent independent intake
ACCEPTED = YES for G3, G4 implementation, fresh Reliability, DQ, V and final Goal
VERIFIED = YES only for this local Verification/final evidence chain
RUNTIME_LOADED = NO
STAGED = NO
COMMITTED = NO
PUSHED = NO
DEPLOYED = NO
ACTIVATED = NO
PRODUCTION_ACCEPTED = NO
```

`VERIFIED=YES` here means the bounded local Verification gate and final PM evidence chain only. It does not mean runtime or production verification. The exact stop boundary is reached: no P1-G5 task, remote action, runtime action, production stimulus, Git publication or additional child may be created from this Goal.

## 11. Closeout terminal

```text
PASS / P1_PROCESS_KPI_BOUNDED_API_LOCAL_MVP_AUTONOMOUS_GOAL_COMPLETE
```

This is the final report for the local Goal. After its identity is recorded in the Ledger, the parent stops and leaves owner review of any future Git publication or later Goal outside this task.
