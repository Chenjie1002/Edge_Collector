# Edge MES Demo — ChatGPT PM Handoff — 2026-07-30 12:03 UTC+8

## 1. Handoff identity

- Project：Edge MES Demo
- Handoff type：ChatGPT PM window transition before local runtime-loaded observability implementation
- Project absolute path：`/Users/chenjie/Documents/MES/edge-mes-demo`
- Handoff file：`docs/thread_handoff/chatgpt_pm_handoff_260730-1203.md`
- Authoring timezone：China Standard Time / UTC+8
- Authoring authority：current ChatGPT PM under the user-requested PM handoff workflow
- Delivery state：`WRITTEN / UNSTAGED / UNCOMMITTED / UNPUSHED`
- MVP classification：`MVP-ALIGNED WITH BACKLOG ITEMS`

This handoff closes the current PM planning window after final acceptance of the process-bound `RUNTIME-LOADED` implementation contract. It does not grant implementation、Git、network、SSH、Docker、build、deployment、Collector lifecycle、runtime validation、production accepted-fact、cleanup or archive authority.

## 2. Live repository baseline at handoff

Fresh read-only recovery established：

```text
root: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: ce22ca71eff0548aa064129c160f7041603855e7
origin/main: ce22ca71eff0548aa064129c160f7041603855e7
HEAD^: 35c50b1eb0f76d8b3361e8c122448ad03899559b
ahead / behind: 0 / 0
tracked dirty: empty
cached index: empty
git diff --check: PASS
git diff --cached --check: PASS
untracked before this handoff: 309
untracked after this handoff: expected 310
```

Recent commit chain：

```text
ce22ca7 Add ChatGPT PM handoff after authority-chain closeout
35c50b1 Materialize current Collector activation authority chain
2d7ff45 Materialize repository governance and hygiene inventory
ac33e6b Add PM handoff after image load gate closeout
6656367 Accept exact loaded Collector image gate
ca68dd4 Add PM handoff before Collector activation
1fac3ee Add PM handoff after R30 reliability cleanup holds
63d3cc7 Close D2-R7B R29 observation and cleanup documentation
```

Live Git facts override historical baselines in older reports、`docs/current_status.md`、`docs/roadmap.md` and older handoffs.

## 3. PM operating model that must be preserved

The new ChatGPT PM must continue to enforce：

1. Architecture / Integration、Reliability、Data Quality and Verification are separate core Threads.
2. The PM controls authority、exact allowlists、gate order、Git and remote/runtime operations.
3. A prior PASS never authorizes the next phase automatically.
4. Every Thread result returns to ChatGPT PM durable intake for independent path/hash/Git/evidence verification.
5. Source/test implementation、Git closeout、build、deployment、runtime validation and production acceptance are separate authorities.
6. Never use broad staging or cleanup such as `git add .`、`git add -A`、`git add docs/`、`git clean -fd` or broad stash/reset.
7. Historical HOLD records remain durable history unless explicitly superseded by an accepted later contract.
8. Evidence states remain distinct：`WRITTEN`、`PM-REVIEWED`、`PM-VERIFIED`、`PM-ACCEPTED`、`IMPLEMENTED`、`TESTED`、`STAGED`、`COMMITTED`、`PUSHED`、`BUILT`、`DEPLOYED`、`ACTIVATED`、`RUNTIME-LOADED` and `PRODUCTION-ACCEPTED`.
9. Validation scope must remain proportional to the MVP. Diagnostic completeness、long-term retention、generic audit/forensics and telemetry are not blocker authority without a concrete false-PASS or safety consequence.

Primary governance authority：

```text
docs/thread_handoff/pm_operating_rules.md
49170 bytes
SHA-256 a692fdafbdea8c63d184cb11548e73731aefccd3110818004b028ba7ee9fe7f5
```

## 4. Current PM-accepted product and gate state

Current product state：

```text
ACTIVATED: YES
STATIC_MAPPING_INITIALIZED: YES
RUNTIME-LOADED: NO
PRODUCTION-ACCEPTED: NO
```

Current planning state：

```text
Architecture contract: PASS
Reliability planning review: PASS
Data Quality planning review: PASS after bounded scope reset
Verification planning review: PASS
Final planning-contract acceptance: YES
Implementation: NOT STARTED
Local implementation tests: NOT RUN
Git closeout: NOT AUTHORIZED
Build/deploy: NOT AUTHORIZED
Runtime validation: NOT AUTHORIZED
```

The final PM-accepted implementation contract is the combined authority：

```text
R42 base contract
+
R45 bounded addendum
```

R43 remains the accepted Reliability review. R46 remains the accepted focused Data Quality re-review. R47 remains the accepted Verification planning review. R44 is preserved as historical Data Quality blocker origin only.

## 5. R35/R36 durable baseline that remains relevant

R35 accepted product boundary：

```text
ACTIVATED = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED = NO
PRODUCTION-ACCEPTED = NO
```

Primary R35 report：

```text
docs/reports/sprint4_d2_r7b_i1_r35_phase5_post_activation_validation.md
3002 bytes
SHA-256 133c303e6a556b4be9e2c9535a10ff3b5a9dd06bf5b6f3fca1f272d707b75ee0
```

R35 is historical bounded read-only evidence. Its image/config hashes must not be reused as future freshness authority for a new implementation or runtime validation.

R36 working-tree classification authority：

```text
docs/reports/sprint4_d2_r7b_i1_r36_working_tree_hygiene_authority_materialization_plan.md
12643 bytes
SHA-256 56ee171f9639ad36a8f4dc23f3098c89047bc3f58932b1b3b0a893df55ee1ecd

docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/authority_materialization_plan.json
122377 bytes
SHA-256 4d73092bb058ff2643ce9092327846ec41e2c12b10468e86ff6739cb514f8705
```

R36 backlog classification remains：

```text
Batch D historical manual review: 300 paths
Batch E frontend/next-env.d.ts: 1 path
```

Batch D has no `SAFE_TO_DELETE` conclusion. Batch D/E do not block product work, but they must be excluded from implementation and Git allowlists unless separately authorized.

## 6. R40–R47 runtime-loaded planning chain

All files below are current regular UTF-8、NON-SYMLINK、UNTRACKED、UNSTAGED and not committed.

| Gate | Path | Bytes | SHA-256 | Current classification |
| --- | --- | ---: | --- | --- |
| R40 | `docs/reports/sprint4_d2_r7b_i1_r40_process_bound_runtime_loaded_observability_plan.md` | 23337 | `280cb553f5fc8bf81c92e689493782749534293de4876a05d88063080caabb91` | historical initial Architecture plan; superseded for implementation subjects |
| R41 | `docs/reports/sprint4_d2_r7b_i1_r41_process_bound_runtime_loaded_observability_reliability_review.md` | 25111 | `6dc2c7a11ea2e6c4723bda69ed270b2e9a6cb7e3f4f75d13673599640adb5bb1` | historical Reliability HOLD / blocker origin |
| R42 | `docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md` | 32319 | `dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165` | final base application contract |
| R43 | `docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md` | 30244 | `95b2e63c4879fb5af6920b262300566c577612dd1753b13bf59928c1417338e8` | accepted Reliability PASS |
| R44 | `docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md` | 43036 | `3b4d1f3451d0b0036e5530bc83eb35b90ee2b6d140b0a2799b82df1ada035bfa` | historical Data Quality HOLD / DQ-B1–B3 origin |
| R45 | `docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md` | 13786 | `8fd646f24565bbcb27aa9063038774fee3b5398d66566f961bee296ffff02ef2` | final bounded addendum |
| R46 | `docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md` | 23703 | `f460fef43d975de41ed624fa49d8a1a8dcd5246b4ae55b222189f40703914b81` | accepted focused Data Quality PASS |
| R47 | `docs/reports/sprint4_d2_r7b_i1_r47_runtime_loaded_observability_verification_planning_review.md` | 34592 | `4de247e350eb595077219856cf63b0319ee83d14026b6beaaf7c5d83211a0ae4` | accepted Verification planning PASS |

Final contract interpretation：

```text
R42 controls the base application contract.

R45 supersedes R42 only for:
- canonical line_id authority and selected routing-line equality;
- later source/image/config/process terminal binding;
- later raw-log/payload/parsed-evidence artifact identity.

All other R42 clauses remain unchanged.
```

## 7. Final implementation contract summary

The new PM must not broaden the contract. The minimum accepted source behavior is：

1. `app.main.main()` creates one mandatory startup context at its first executable boundary, before `load_config()`.
2. Context contains RFC3339 UTC `Z` main-entry time and current `os.getpid()`, is mandatory/no-default and single-use.
3. `load_edge_mapping()` reads exact raw bytes once, hashes the same bytes, explicitly UTF-8 decodes them, parses the same content and binds raw path/SHA to the returned mapping.
4. Worker constructor preserves configured IDs、expected scopes and generated scopes in list form before dict conversion; duplicate/missing/extra/reserved/count/one-to-one failures fail closed.
5. Canonical record `line_id` is the hash-bound resolved/runtime snapshot line; selected first-PLC line remains routing projection and must equal canonical before success.
6. Record has exactly 11 fields and exact application grammar：

```text
collector_runtime_loaded_json=<JSON_OBJECT>
```

7. Serialization is deterministic、compact、one-line and fail-propagating.
8. Success emission is the final required constructor action and occurs before constructor return、`Thread.start()` and all PLC/DB/accepted-fact/ACK activity.
9. The record proves required mapping/resolved/read-plan initialization only. It does not prove worker health、PLC、DB、persistence、ACK/read_done or production acceptance.
10. Future runtime validation must separately bind accepted source → full image ID → active container/process → fresh container-visible config bytes → raw log/payload/parsed record evidence.

## 8. Frozen future implementation allowlist

Only these current application source paths may be modified by a future separately authorized implementation task：

```text
collector/app/main.py
collector/app/services/event_collector.py
collector/app/plc/mapping.py
```

Only these test paths may be modified：

```text
collector/tests/test_event_collector_reliability.py
tests/test_collector_station_event_runtime_source.py
```

Current clean identities at handoff：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `collector/app/main.py` | 2073 | `a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090` |
| `collector/app/services/event_collector.py` | 16342 | `eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f` |
| `collector/app/plc/mapping.py` | 17433 | `c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098` |
| `collector/tests/test_event_collector_reliability.py` | 12774 | `462656c9d9146e492b52296ca2b40a1f37fe40cba95a2068e4c6317fd33c2472` |
| `tests/test_collector_station_event_runtime_source.py` | 30571 | `7d9d894eaa784e36c729e824ee87de73a863765089fd12e388bc926164229fd7` |

Protected paths that must remain unchanged during implementation include：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `collector/app/config.py` | 764 | `4f01689a34fb494f7ea84cf74b303ce8aed0957d1dd9c05fc7773563cd577afc` |
| `collector/app/services/resolved_config_registry.py` | 17337 | `1844449a3f99e9ca53bddc8063c151fb0f889920597bccb170f5e62f3715db2c` |
| `collector/app/plc/read_plan.py` | 1482 | `fd5f675501444ed8378d6a296c3ed3d8769af97a1f19d1e95f3c00d76d4b02d6` |
| `collector/tests/test_snap7_reliability_integration.py` | 8025 | `5cc75a9cd37eeee6f3a80e29d186b55b3aab3a335898d77e204a9d653f686b54` |
| `tests/test_collector_container_packaging.py` | 941 | `351e80a76a53f742258e91196b109172de7b43dc3fa359e63ef44c9e7ad9c26e` |
| `collector/Dockerfile` | 218 | `e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839` |
| `docker-compose.yml` | 5698 | `c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66` |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` |

## 9. R48 authority status at handoff

The old PM window drafted and displayed an R48 implementation prompt with authority ID：

```text
PM-D2-R7B-I1-R48-RUNTIME-LOADED-OBSERVABILITY-IMPLEMENTATION-260730-1149
```

Live recovery at handoff proves：

```text
all five implementation paths remain clean relative to HEAD
tracked dirty: empty
cached: empty
R48 report path: absent
```

Therefore no repository evidence shows that R48 implementation began.

Handoff decision：

```text
OLD-WINDOW R48 AUTHORITY: EXPIRED / MUST NOT BE REUSED
R48 IMPLEMENTATION: NOT STARTED
```

The new PM must not tell a Thread to continue under the old authority ID. After read-only takeover, the new PM may issue a fresh R48 implementation prompt with a new authority ID and the same final R42+R45 contract, exact three-source/two-test allowlist and local-only evidence boundary.

If live recovery in the new window unexpectedly shows any of the five implementation files changed or an R48 report present, do not issue a duplicate task. Treat that as an in-flight or returned implementation result and perform PM durable intake first.

## 10. Current untracked backlog and exclusions

Before this handoff：

```text
untracked count: 309
Batch D: 300
Batch E: 1
R40–R47: 8
```

After creating this handoff：

```text
expected untracked count: 310
Batch D: 300
Batch E: 1
R40–R47: 8
new handoff: 1
```

Interpretation：

- These are classified paths, not unknown contamination.
- R40–R47 are current durable planning/review authority files but remain untracked/uncommitted.
- The new handoff is also untracked until separately authorized Git closeout.
- Do not run `git clean`.
- Do not broad-stage `docs/` or all untracked files.
- Batch D requires separate manual keep/archive/local-only review.
- Batch E requires a separate keep-or-ignore decision.
- None of these paths automatically belongs to a future implementation commit.

## 11. Status and roadmap authoring-time warning

Current identities：

```text
docs/current_status.md
150180 bytes
SHA-256 ee7126fd20f1774f54cee9b238cab4e3e0943bce854402b1594060212f88cc23

docs/roadmap.md
12079 bytes
SHA-256 77f94dd507f0a8b7be30f0042878ff0818c36f6dcbd74b1cd415331b502e6f13
```

They were not updated during R40–R47 and contain historical authoring-time sections. This handoff records the live accepted gate state instead. No status/roadmap write authority was granted in the current window.

Authority precedence for takeover：

1. live Git recovery；
2. this handoff；
3. R42 + R45 combined contract；
4. R43、R46、R47 accepted reviews；
5. R35/R36 durable evidence；
6. recent commits；
7. old status/roadmap sections as historical context.

## 12. Consumed, expired and non-authorized authority register

Consumed or terminalized：

```text
R42 Architecture contract-writing authority: consumed
R43 Reliability re-review authority: consumed
R44 Data Quality review authority: consumed
R45 Architecture scope-reset authority: consumed
R46 Data Quality re-review authority: consumed
R47 Verification planning review authority: consumed
old-window R48 implementation authority: expired on handoff and not reusable
```

No current authority exists for：

- source/test modification；
- test execution；
- Git stage、commit、push or tag；
- build or image acceptance；
- network、SSH or remote read；
- Docker/Compose inspection or mutation；
- Collector restart/recreate/rollback；
- runtime-loaded validation or A–H evidence generation；
- PM acceptance of `RUNTIME-LOADED`；
- production accepted-fact generation or validation；
- Batch D/E mutation；
- status/roadmap update；
- cleanup、delete、move or archive actions.

Any approval request remaining in an old Thread is stale and must not be accepted by momentum.

## 13. Recommended reading order for the new ChatGPT PM

Read in this order：

1. `docs/thread_handoff/pm_operating_rules.md`
2. `docs/thread_handoff/chatgpt_pm_handoff_260730-1203.md`
3. `docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md`
4. `docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md`
5. `docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md`
6. `docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md`
7. `docs/reports/sprint4_d2_r7b_i1_r47_runtime_loaded_observability_verification_planning_review.md`
8. `docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md`
9. `docs/reports/sprint4_d2_r7b_i1_r35_phase5_post_activation_validation.md`
10. `docs/reports/sprint4_d2_r7b_i1_r36_working_tree_hygiene_authority_materialization_plan.md`
11. `docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/authority_materialization_plan.json`
12. `collector/app/main.py`
13. `collector/app/services/event_collector.py`
14. `collector/app/plc/mapping.py`
15. `collector/tests/test_event_collector_reliability.py`
16. `tests/test_collector_station_event_runtime_source.py`
17. `docs/current_status.md`
18. `docs/roadmap.md`

Status and roadmap are intentionally last because their current-state sections predate R40–R47.

## 14. First read-only recovery for the new ChatGPT PM

Before issuing any new Thread task, run only：

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git status -sb --untracked-files=no
git log -8 --oneline --decorate
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git rev-parse origin/main
git rev-parse HEAD^
git rev-list --left-right --count HEAD...origin/main
git diff --name-only
git diff --cached --name-only
git diff --check
git diff --cached --check
git -c core.quotePath=false ls-files --others --exclude-standard
```

Expected baseline after this handoff is written：

```text
HEAD == origin/main == ce22ca71eff0548aa064129c160f7041603855e7
HEAD^ == 35c50b1eb0f76d8b3361e8c122448ad03899559b
ahead / behind == 0 / 0
tracked dirty == empty
cached == empty
untracked == 310
```

Then verify：

```text
R42–R47 exact identities match this handoff
five implementation source/test paths remain clean
R48 report is absent
this handoff is regular UTF-8, non-symlink, untracked and unstaged
```

If live facts differ, live recovery overrides this snapshot only after the new PM identifies and explains the drift. Do not automatically mutate the repository.

## 15. Recommended next sequence

### 15.1 Handoff governance closeout

Current handoff-writing step authorizes only the new file write. It does not authorize Git.

Recommended governance sequence：

```text
new PM read-only takeover
→ verify this handoff path/bytes/SHA and exact working-tree composition
→ optionally request exact single-file stage/commit/push authority for this handoff
→ do not bundle R40–R47, Batch D/E or source changes without separate authority
```

Suggested future handoff commit subject, only if explicitly authorized：

```text
Add PM handoff before runtime-loaded implementation
```

### 15.2 First product-facing action

After read-only takeover, if the five implementation paths remain clean and R48 report remains absent, the smallest next product action is：

```text
issue a fresh R48 local implementation authority
```

That task should：

- modify only the exact three source and two test paths；
- write one exact implementation report；
- run local `py_compile` and the two complete focused pytest commands；
- establish a local implementation lock；
- forbid Git、build、Docker、remote and runtime evidence；
- stop at ChatGPT PM durable intake.

After a local implementation PASS, the likely chain remains：

```text
PM durable intake
→ focused implementation reviews as separately authorized
→ PM final implementation acceptance
→ exact Git closeout
→ accepted build/image gate
→ deployment/lifecycle gate
→ bounded runtime-loaded validation with A–H evidence
→ PM acceptance of RUNTIME-LOADED
→ separate production accepted-fact planning
```

No later stage is authorized by this handoff.

## 16. Carry-forward recommendations and stopping rule

Non-blocking carry-forward items：

1. Implementation tests should assert that the first startup-context consumer remains consumed even if a later constructor action fails.
2. Future runtime helper should keep transport adapter、application-message extraction and strict JSON parsing as separate reviewable stages.
3. Keep `record_emitted_at` and sorted scope list out of v1 unless a concrete false-PASS risk is later identified.
4. Keep source/image/config/process binding and A–H evidence in later authority prompts; do not add those identities to the application record.
5. Do not reopen generic telemetry、long-term log retention、audit/forensics or production accepted-fact work inside the runtime-loaded implementation branch.

Stopping rule：once the final accepted terminal invariants are implemented and focused tests pass without a credible false-PASS or safety blocker, new diagnostic-completeness findings move to recommendations/backlog rather than creating another unlimited repair cycle.

## 17. Copyable prompt for the new ChatGPT PM window

```text
你是 Edge MES Demo 项目的新任 ChatGPT PM。

项目绝对路径：
/Users/chenjie/Documents/MES/edge-mes-demo

你的职责是按照项目 PM Rule 管理 Architecture / Integration、Reliability、Data Quality、Verification 四个独立核心 Thread，控制 authority、exact allowlist、review gate、Git 和 remote/runtime 操作。不要直接混合不同角色，也不要继承旧 Thread 或旧 PM window 的权限。

请先按顺序读取：

1. docs/thread_handoff/pm_operating_rules.md
2. docs/thread_handoff/chatgpt_pm_handoff_260730-1203.md
3. docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md
4. docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md
5. docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md
6. docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md
7. docs/reports/sprint4_d2_r7b_i1_r47_runtime_loaded_observability_verification_planning_review.md
8. docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md
9. docs/reports/sprint4_d2_r7b_i1_r35_phase5_post_activation_validation.md
10. docs/reports/sprint4_d2_r7b_i1_r36_working_tree_hygiene_authority_materialization_plan.md
11. docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/authority_materialization_plan.json
12. collector/app/main.py
13. collector/app/services/event_collector.py
14. collector/app/plc/mapping.py
15. collector/tests/test_event_collector_reliability.py
16. tests/test_collector_station_event_runtime_source.py
17. docs/current_status.md
18. docs/roadmap.md

然后执行只读 recovery：

cd /Users/chenjie/Documents/MES/edge-mes-demo

git status -sb --untracked-files=no
git log -8 --oneline --decorate
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git rev-parse origin/main
git rev-parse HEAD^
git rev-list --left-right --count HEAD...origin/main
git diff --name-only
git diff --cached --name-only
git diff --check
git diff --cached --check
git -c core.quotePath=false ls-files --others --exclude-standard

Handoff baseline：

HEAD == origin/main == ce22ca71eff0548aa064129c160f7041603855e7
HEAD^ == 35c50b1eb0f76d8b3361e8c122448ad03899559b
ahead/behind == 0/0
tracked dirty == empty
cached == empty
untracked == 310

当前 PM-accepted 产品状态：

ACTIVATED = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED = NO
PRODUCTION-ACCEPTED = NO

当前 planning 状态：

- R42 + R45 是 final PM-accepted implementation contract
- R43 Reliability PASS accepted
- R46 focused Data Quality PASS accepted
- R47 Verification planning PASS accepted
- R44 仅为 historical blocker origin
- implementation 尚未开始

旧 PM window 中曾生成 R48 implementation Prompt，但 handoff 时五个 implementation paths 仍 clean，R48 report 不存在。旧 authority ID `PM-D2-R7B-I1-R48-RUNTIME-LOADED-OBSERVABILITY-IMPLEMENTATION-260730-1149` 已过期，不得复用。

如果 recovery 仍显示五个 implementation paths clean 且 R48 report absent，请使用新的 authority ID 重新发布最小 R48 local implementation task。Exact allowlist 只能是：

Source:
- collector/app/main.py
- collector/app/services/event_collector.py
- collector/app/plc/mapping.py

Tests:
- collector/tests/test_event_collector_reliability.py
- tests/test_collector_station_event_runtime_source.py

Report:
- docs/reports/sprint4_d2_r7b_i1_r48_runtime_loaded_observability_implementation.md

R48 只允许 local source/test implementation、py_compile、两个完整 focused pytest commands 和 durable report。不得授权 Git、build、Docker、remote、runtime validation、A–H evidence 或 production accepted-fact。

当前 untracked 310 项应由以下组成：

- Batch D historical review：300
- Batch E frontend/next-env.d.ts：1
- R40–R47 reports：8
- current handoff：1

这些路径已分类，不是 unknown contamination。禁止 git clean、git add .、git add -A、broad docs staging或批量删除。Batch D没有SAFE_TO_DELETE结论。

请先返回：

1. read-only recovery结果；
2. this handoff exact bytes/SHA/file/index identity；
3. R42–R47 identity和final contract状态；
4. tracked/untracked exact composition；
5. old R48 authority expired确认；
6. 推荐的最小下一步。

不要自动执行source modification、tests、Git、Docker、remote、Batch D/E处理或runtime validation。
```

## 18. Handoff completion state

```text
handoff: WRITTEN
staged: NO
committed: NO
pushed: NO
status/roadmap updated: NO — not authorized; this handoff records the current gate state
```

Only next gate：

```text
ChatGPT PM durable intake in the new PM window
```

After new PM intake, any handoff stage/commit/push or R48 implementation requires separate exact authority.
