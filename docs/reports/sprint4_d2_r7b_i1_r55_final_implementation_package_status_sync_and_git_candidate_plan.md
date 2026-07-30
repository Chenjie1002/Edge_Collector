# Sprint 4 D2-R7B-I1 R55 Final Implementation Package Status Sync and Git Candidate Plan

## 1. 报告、任务、Thread、authority 与结论

- 报告名称：Sprint 4 D2-R7B-I1 R55 Final Implementation Package Status Sync and Git Candidate Plan
- 任务名称：D2-R7B-I1 R55 — Synchronize Final Package Status and Materialize Exact Git Candidate
- 执行 Thread：Architecture / Integration
- 项目绝对路径：`/Users/chenjie/Documents/MES/edge-mes-demo`
- Report delivery mode：`REPOSITORY_REPORT_WITH_ARTIFACTS`
- Exact report path：`docs/reports/sprint4_d2_r7b_i1_r55_final_implementation_package_status_sync_and_git_candidate_plan.md`
- Exact artifact path：`docs/thread_handoff/chatgpt_pm_handoff_260730-1621.md`
- Authority source / ID：`PM-D2-R7B-I1-R55-FINAL-PACKAGE-STATUS-SYNC-GIT-CANDIDATE-260730-1621`
- Authority：one-shot；第一次 task-owned write 时消费；只授权 exact report、handoff、`docs/current_status.md` 与 `docs/roadmap.md`

### Terminal conclusion

```text
PASS / R55 STATUS SYNC WRITTEN / EXACT 24-PATH GIT CANDIDATE MATERIALIZED
```

本结论只表示本轮四个 authorized docs/artifact paths 已完成状态同步、handoff 与 exact
Git candidate plan 已写入，并完成授权的本地验证与写后 detached audit。它不表示
`GIT-CANDIDATE-ACCEPTED`、`STAGED`、`COMMITTED`、`PUSHED`、build、Docker、
deployment、lifecycle、runtime validation、`RUNTIME-LOADED` 或
`PRODUCTION-ACCEPTED`。

## 2. Initial live Git recovery

在任何 task-owned write 前，先在真实 checkout 执行了 Prompt 指定的只读 recovery：

```text
repository root: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 4a733d7995a94398ade693822662ebd2b22f9d3d
origin/main: 4a733d7995a94398ade693822662ebd2b22f9d3d
ahead / behind: 0 / 0
cached: empty
git diff --check: PASS
git diff --cached --check: PASS
R55 report before write: ABSENT / NON-SYMLINK
new handoff before write: ABSENT / NON-SYMLINK
```

Initial tracked dirty set exactly matched the expected five paths:

```text
collector/app/main.py
collector/app/plc/mapping.py
collector/app/services/event_collector.py
collector/tests/test_event_collector_reliability.py
tests/test_collector_station_event_runtime_source.py
```

Initial untracked observation was retained as a raw NUL-delimited observation and classified
using repository-relative full-path UTF-8 stable sort plus the R36 JSON exact Batch D/E lists:

```text
Batch D = 300
Batch E = 1
R40–R54 reports = 15
total = 316
unknown = 0
missing = 0
```

No reset, restore, checkout, stash, clean, delete, move or other mutation was used for
recovery. Batch D/E content was not opened.

## 3. Exact input identities and protected-path audit

### 3.1 Initial governance identities

These initial identities matched the authority Prompt before any task-owned write:

| Path | Initial bytes | Initial SHA-256 | Initial state |
| --- | ---: | --- | --- |
| `docs/current_status.md` | 150180 | `ee7126fd20f1774f54cee9b238cab4e3e0943bce854402b1594060212f88cc23` | tracked regular |
| `docs/roadmap.md` | 12079 | `77f94dd507f0a8b7be30f0042878ff0818c36f6dcbd74b1cd415331b502e6f13` | tracked regular |
| `docs/thread_handoff/chatgpt_pm_handoff_260730-1203.md` | 26183 | `c9a7ed7283d4574578e1608fc6891bdb91373d97bac3191740863917af3ad8e1` | untracked regular |

The protected non-candidate baselines captured before writing were:

| Path | Bytes | SHA-256 | Final audit |
| --- | ---: | --- | --- |
| `docs/thread_handoff/pm_operating_rules.md` | 49170 | `a692fdafbdea8c63d184cb11548e73731aefccd3110818004b028ba7ee9fe7f5` | IDENTICAL |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` | IDENTICAL |
| old PM handoff above | 26183 | `c9a7ed7283d4574578e1608fc6891bdb91373d97bac3191740863917af3ad8e1` | IDENTICAL |

### 3.2 Frozen source/test identities

The three authorized local validations were executed before the source/test execution lock.
The final detached audit confirmed every identity below remained byte-identical:

| Path | Bytes | SHA-256 | Final state | Accepted authority |
| --- | ---: | --- | --- | --- |
| `collector/app/main.py` | 2525 | `d1a461294c91f9f86cde4af87b21bb1147bed5561d64028e8462a8f57d46de80` | tracked dirty | R48/R49 implementation + R50/R51/R54 review chain |
| `collector/app/services/event_collector.py` | 24313 | `02cab6ea15572ae0b2f6059462f9cd6856cd483ab0dcc37c87d39267aad1e8e2` | tracked dirty | R48/R49 implementation + R50/R51/R54 review chain |
| `collector/app/plc/mapping.py` | 18876 | `ba39583a699f8347c0ff5eaec2e7c807dad909c815269de607a36e8b93c023a7` | tracked dirty | R48/R49 implementation + R50/R51/R54 review chain |
| `collector/tests/test_event_collector_reliability.py` | 38392 | `9af7658577ea16344a000e00eb3e346464944eeb15d223f74b7cc690d2f46af3` | tracked dirty | R48/R49 implementation + R53 oracle repair + R54 review |
| `tests/test_collector_station_event_runtime_source.py` | 36408 | `5419dcb1e2fb5819e63c9891937cfe96a29becc21bf9be89f7602d0c3aa650d2` | tracked dirty | R48/R49 implementation + R53 oracle repair + R54 review |

No source, test, config, PM Rules or old handoff mutation was observed.

## 4. PM final implementation-package acceptance

R54 independently confirmed that R52 historical Verification blockers V-B1–V-B4 were closed
by the persisted source and R53 test-only oracle repair. R50 and R51 remain accepted
independent Reliability and Data Quality implementation reviews. The current PM final
implementation-package acceptance is:

```text
PM FINAL IMPLEMENTATION-PACKAGE ACCEPTANCE = YES
GIT-CANDIDATE-ELIGIBLE                  = YES
GIT-CANDIDATE-ACCEPTED                  = NO
STAGED                                  = NO
COMMITTED                               = NO
PUSHED                                  = NO
```

Product/evidence status remains:

```text
ACTIVATED                  = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED             = NO
PRODUCTION-ACCEPTED        = NO
```

The R54 result is not silently upgraded into Git candidate acceptance. User authorization is
still required separately for exact-path stage, commit and push.

## 5. R40–R54 authority chain summary

| Gate | Authority ID suffix | Result and durable role |
| --- | --- | --- |
| R40 | `...PLAN-260730-0849` | PASS planning; process-bound Candidate A contract |
| R41 | `...RELIABILITY-REVIEW-260730-0904` | Historical HOLD; B1–B3 Reliability blockers |
| R42 | `...ARCHITECTURE-REPAIR-260730-0923` | PASS consolidated Architecture repair |
| R43 | `...RELIABILITY-REREVIEW-260730-0940` | PASS accepts R42 contract |
| R44 | `...DATA-QUALITY-REVIEW-260730-0958` | Historical HOLD; DQ-B1–B3 blocker origin |
| R45 | `...SCOPE-RESET-260730-1036` | PASS bounded DQ evidence scope reset |
| R46 | `...DATA-QUALITY-REREVIEW-260730-1053` | PASS focused DQ review of R42 + R45 |
| R47 | `...VERIFICATION-PLANNING-REVIEW-260730-1120` | PASS deterministic Verification plan |
| R48 | `...IMPLEMENTATION-260730-1256` | WRITTEN / TESTED local implementation |
| R49 | `...ORDERING-REPAIR-260730-1321` | WRITTEN / TESTED pre-record DB ordering repair |
| R50 | `...REVIEW-260730-1423` | PASS WITH RECOMMENDATIONS Reliability review |
| R51 | `...REVIEW-260730-1446` | PASS WITH RECOMMENDATIONS Data Quality review |
| R52 | `...REVIEW-260730-1507` | Historical Verification HOLD |
| R53 | `...REPAIR-260730-1534` | WRITTEN / TESTED V-B1–V-B4 oracle closure |
| R54 | `...REREVIEW-260730-1607` | PASS WITH RECOMMENDATIONS; no current blocker |

The effective closure sequence is `R52 HOLD → R53 oracle closure → R54 independent
Verification re-review`. The R40–R47 bounded contract and the R48–R54 implementation/review
chain remain separate gates.

## 6. Current status and roadmap synchronization

### 6.1 `docs/current_status.md`

Minimal changes:

- updated the authoring date to 2026-07-30;
- added the current R55 control block recording R40–R54 terminal states;
- recorded PM final implementation-package acceptance and
  `GIT-CANDIDATE-ELIGIBLE = YES` while preserving candidate accepted/staged/committed/pushed
  as `NO`;
- preserved `ACTIVATED = YES`, `STATIC_MAPPING_INITIALIZED = YES`,
  `RUNTIME-LOADED = NO`, `PRODUCTION-ACCEPTED = NO`;
- retained the old 0I image-load/activation section as historical state;
- changed the current unique next step to local implementation-package exact-path Git closeout;
- retained Oracle/ERP real synchronization and `sync-worker` as Phase-2 Out of Scope.

Final status identity:

```text
bytes: 152834
SHA-256: 4d85463d87b8fd435545db36eabbaefd2d6d71c2a22417a65853d92390508f7a
state: tracked dirty / candidate
```

### 6.2 `docs/roadmap.md`

Minimal changes:

- updated the authoring date and current status line;
- added the D2-R7B-I1 runtime-loaded observability implementation package acceptance section;
- recorded R50/R51/R54 reviews and the R52→R53→R54 closure;
- kept runtime evidence, A–H, deployment/lifecycle and production acceptance as future gates;
- updated the only current next step to exact-path Git candidate intake/closeout;
- did not change Phase-2 functional priority;
- retained Oracle/ERP real synchronization in the delayed/out-of-scope range.

Final roadmap identity:

```text
bytes: 13648
SHA-256: e933d4125a56df1624eeeb69693eff944f44108b5207a2e4cf67a1796592fef3
state: tracked dirty / candidate
```

## 7. New handoff identity and content audit

```text
path: docs/thread_handoff/chatgpt_pm_handoff_260730-1621.md
state: untracked / regular / non-symlink
bytes: 12398
SHA-256: 2c651618a1dec485b9d354c1a0bc9107aec2b1df88c9f6e65c441aab8d54cfe2
```

The handoff contains the absolute checkout, live HEAD/origin and status, R40–R54 authority
chain, product/evidence boundary, exact 24-path candidate, tracked/untracked grouping, Batch
D/E exclusions, frozen commit message, separate user stage/commit/push authorization, the
post-closeout sequence, and a copyable next ChatGPT PM prompt. It does not authorize any
remote, runtime, production or Git mutation.

## 8. Exact 24-path Git candidate identity table

The following table is the complete frozen candidate. The table is intentionally path-exact;
untracked historical material is not expanded or opened.

| # | Candidate path | State | Final bytes | Final SHA-256 | Task role | Accepted authority |
| ---: | --- | --- | ---: | --- | --- | --- |
| 1 | `collector/app/main.py` | tracked dirty | 2525 | `d1a461294c91f9f86cde4af87b21bb1147bed5561d64028e8462a8f57d46de80` | accepted implementation source | R48/R49 + R50/R51/R54 |
| 2 | `collector/app/plc/mapping.py` | tracked dirty | 18876 | `ba39583a699f8347c0ff5eaec2e7c807dad909c815269de607a36e8b93c023a7` | accepted mapping source | R48/R49 + R50/R51/R54 |
| 3 | `collector/app/services/event_collector.py` | tracked dirty | 24313 | `02cab6ea15572ae0b2f6059462f9cd6856cd483ab0dcc37c87d39267aad1e8e2` | accepted collector source | R48/R49 + R50/R51/R54 |
| 4 | `collector/tests/test_event_collector_reliability.py` | tracked dirty | 38392 | `9af7658577ea16344a000e00eb3e346464944eeb15d223f74b7cc690d2f46af3` | focused Reliability/oracle test | R48/R49 + R53 + R54 |
| 5 | `tests/test_collector_station_event_runtime_source.py` | tracked dirty | 36408 | `5419dcb1e2fb5819e63c9891937cfe96a29becc21bf9be89f7602d0c3aa650d2` | focused runtime-source/oracle test | R48/R49 + R53 + R54 |
| 6 | `docs/current_status.md` | tracked dirty | 152834 | `4d85463d87b8fd435545db36eabbaefd2d6d71c2a22417a65853d92390508f7a` | current governance/status sync | R55 |
| 7 | `docs/roadmap.md` | tracked dirty | 13648 | `e933d4125a56df1624eeeb69693eff944f44108b5207a2e4cf67a1796592fef3` | current roadmap sync | R55 |
| 8 | `docs/thread_handoff/chatgpt_pm_handoff_260730-1621.md` | untracked | 12398 | `2c651618a1dec485b9d354c1a0bc9107aec2b1df88c9f6e65c441aab8d54cfe2` | durable PM handoff | R55 |
| 9 | `docs/reports/sprint4_d2_r7b_i1_r40_process_bound_runtime_loaded_observability_plan.md` | untracked | 23337 | `280cb553f5fc8bf81c92e689493782749534293de4876a05d88063080caabb91` | accepted planning contract | R40 / PM-accepted input |
| 10 | `docs/reports/sprint4_d2_r7b_i1_r41_process_bound_runtime_loaded_observability_reliability_review.md` | untracked | 25111 | `6dc2c7a11ea2e6c4723bda69ed270b2e9a6cb7e3f4f75d13673599640adb5bb1` | historical Reliability blocker origin | R41 / retained history |
| 11 | `docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md` | untracked | 32319 | `dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165` | accepted Architecture contract | R42 / R43 |
| 12 | `docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md` | untracked | 30243 | `bc9844c2be0a31412c798f8681f919badcb83173f4033554f18f3a2f1ee3f3df` | accepted Reliability re-review | R43 |
| 13 | `docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md` | untracked | 43035 | `fd5df4b03fefa98338610d72ddbee25271a0ed0270185dbf0d2c50bbbd688003` | historical DQ blocker origin | R44 / retained history |
| 14 | `docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md` | untracked | 13786 | `8fd646f24565bbcb27aa9063038774fee3b5398d66566f961bee296ffff02ef2` | bounded DQ scope reset | R45 / R46 |
| 15 | `docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md` | untracked | 23703 | `f460fef43d975de41ed624fa49d8a1a8dcd5246b4ae55b222189f40703914b81` | accepted focused DQ review | R46 |
| 16 | `docs/reports/sprint4_d2_r7b_i1_r47_runtime_loaded_observability_verification_planning_review.md` | untracked | 34592 | `4de247e350eb595077219856cf63b0319ee83d14026b6beaaf7c5d83211a0ae4` | accepted Verification planning | R47 |
| 17 | `docs/reports/sprint4_d2_r7b_i1_r48_runtime_loaded_observability_implementation.md` | untracked | 15691 | `e9dc748970a9db44ae83d83135139407260039ce54417a68f1a9b9eea86a8621` | implementation durable report | R48 |
| 18 | `docs/reports/sprint4_d2_r7b_i1_r49_pre_record_db_connection_ordering_repair.md` | untracked | 11749 | `5d09732094f3266eccc34a002b0203a3889f33be1c6b56568c43b42c50618dde` | ordering repair durable report | R49 |
| 19 | `docs/reports/sprint4_d2_r7b_i1_r50_independent_reliability_implementation_review.md` | untracked | 34023 | `bda18fea7f938a2307d87c2001dd64f055cd74bc9b017916d0096f2c41c45837` | independent Reliability review | R50 |
| 20 | `docs/reports/sprint4_d2_r7b_i1_r51_independent_data_quality_implementation_review.md` | untracked | 42261 | `a0bbeae8108070d641214eca17e1791755c4e72ec5c0f9f8f05dd50e457302ff` | independent Data Quality review | R51 |
| 21 | `docs/reports/sprint4_d2_r7b_i1_r52_independent_verification_implementation_review.md` | untracked | 47886 | `633bf9e619e080d4be0bd99390486243dda8cc8f385f77bf7589dd63623f45f8` | historical Verification HOLD | R52 / retained history |
| 22 | `docs/reports/sprint4_d2_r7b_i1_r53_focused_verification_oracle_closure_repair.md` | untracked | 13871 | `10f6a8b5d95c52e493835dcd2e250ec14fc5b22b58791576cd94f4f62730b03e` | focused oracle repair report | R53 |
| 23 | `docs/reports/sprint4_d2_r7b_i1_r54_independent_verification_implementation_rereview.md` | untracked | 18572 | `5db542357b870d4a31b120a0410b4c4c81f2220a1900ee50835a93c16ea156a5` | final Verification re-review | R54 |
| 24 | `docs/reports/sprint4_d2_r7b_i1_r55_final_implementation_package_status_sync_and_git_candidate_plan.md` | untracked | post-write audit | post-write audit | final status sync and candidate plan | R55 |

The R55 row is intentionally not self-referenced. Its final bytes/SHA-256 are returned by the
post-write detached audit and this Chat manifest.

## 9. Candidate exclusions and exact commit message

Explicitly not candidates:

```text
Batch D: 300 paths
Batch E: frontend/next-env.d.ts
other historical untracked reports
old PM handoff: docs/thread_handoff/chatgpt_pm_handoff_260730-1203.md
.gitignore
docs/thread_handoff/pm_operating_rules.md
config/mapping.yaml
Docker / Compose / frontend / DB / PLC / API / runtime artifacts
```

Frozen proposed commit message:

```text
Accept runtime-loaded observability implementation
```

No broad staging or Git mutation was authorized or executed.

## 10. Exact authorized validation results

### 10.1 py_compile

Executed exactly:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile \
  collector/app/main.py \
  collector/app/services/event_collector.py \
  collector/app/plc/mapping.py \
  collector/tests/test_event_collector_reliability.py \
  tests/test_collector_station_event_runtime_source.py
```

Result: `PASS`, exit code `0`.

### 10.2 Pytest A

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -m pytest \
collector/tests/test_event_collector_reliability.py \
-q
```

Result: `PASS`, `25 passed, 11 subtests passed in 0.23s`, exit code `0`.

### 10.3 Pytest B

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -m pytest \
tests/test_collector_station_event_runtime_source.py \
-q
```

Result: `PASS`, `59 passed in 0.16s`, exit code `0`.

No `-k`, skip, xfail, reduced selection, broad suite, coverage, application startup,
Docker/Compose, network, SSH, remote or runtime command was used.

## 11. Source/test no-mutation and changed-path audit

After the three validations and before the R55 report write:

```text
source/test final identity drift: 0
config/mapping.yaml drift: 0
PM Rules drift: 0
old PM handoff drift: 0
R40–R54 report identity drift: 0
post-validation source/test mutation: 0
cached paths: empty
git diff --check: PASS
git diff --cached --check: PASS
```

Final tracked dirty set from the post-write detached audit is exactly:

```text
collector/app/main.py
collector/app/plc/mapping.py
collector/app/services/event_collector.py
collector/tests/test_event_collector_reliability.py
tests/test_collector_station_event_runtime_source.py
docs/current_status.md
docs/roadmap.md
```

No other tracked path is dirty and the index remains empty.

## 12. Raw/normalized untracked evidence

The pre-write task entry observation was:

```text
raw count 316
Batch D 300 / Batch E 1 / R40–R54 15
unknown 0 / missing 0
```

After the status documents and handoff, before writing R55, the detached read-only observation
was:

```text
raw count: 317
raw NUL digest: 576dad02558946af2c6a0cc3d403a14cd7eff86ee9a83165a252e7dc145a8cda
normalized UTF-8 stable-sort digest: 60500d817e41b189073f535315fb7263e116d9b6f53d527239cb9622ea064495
duplicates: 0
Batch D 300 / Batch E 1 / R40–R54 15 / new handoff 1
unknown 0 / missing 0
```

The expected post-R55 composition is:

```text
raw count 318
Batch D 300 / Batch E 1 / R40–R55 16 / new handoff 1
unknown 0 / missing 0
```

The final raw/normalized counts, digests and membership are returned by the post-write
detached audit in the Chat manifest. Batch D/E content was not opened, deleted, moved,
reclassified, staged or otherwise operated on.

## 13. Forbidden-action counters

| Forbidden category | Count |
| --- | ---: |
| source/test/config/PM Rules/old handoff/R40–R54 mutation | 0 |
| Git add/stage/commit/push/tag | 0 |
| reset/restore/checkout/stash/clean/delete/move | 0 |
| build/package/dependency installation | 0 |
| Docker/Compose/lifecycle/deployment/restart | 0 |
| network/SSH/curl/remote | 0 |
| DB/Oracle/ERP/API/PLC/V-PLC/ACK/read_done/production fact | 0 |
| application startup/runtime validation/A–H evidence | 0 |
| Batch D/E content operation | 0 |
| extra manifest/JSON/sidecar/evidence directory/helper creation | 0 |

The only task-owned writes were the two authorized status docs, the exact handoff and this
exact R55 report.

## 14. Blockers, recommendations and product/evidence boundary

Blockers: none for this docs/status synchronization and exact candidate-plan gate.

Recommendations:

1. ChatGPT PM should intake this durable R55 report and handoff independently.
2. If and only if PM accepts R55, mark the candidate `PM-ACCEPTED`; do not infer staging or
   commit authorization.
3. Obtain separate user authorization for exact-path stage, commit and push using the frozen
   24-path set and exact proposed message.
4. Keep strict RFC3339 and direct line-plan/station-runtime fixture as bounded non-blocking
   backlog; keep DQ-B2/DQ-B3 as later runtime gates.

Product/evidence boundary:

```text
ACTIVATED                  = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED             = NO
PRODUCTION-ACCEPTED        = NO
```

No local compile/test/review result is represented as deployed process evidence, active image
identity, remote state, DB/API/PLC evidence, runtime A–H evidence or production truth.
Oracle/ERP real synchronization remains Phase-2 Out of Scope.

## 15. MVP path consistency

```text
MVP-ALIGNED
```

This task directly supports the current MVP by closing the governance/status handoff around
the already reviewed minimal process-bound runtime-loaded observability implementation. It
adds no product capability, DB/API schema, PLC behavior, runtime topology, telemetry or
production truth. The minimum invariant is exact accepted source/test/report identity with no
false transition from local package review to Git, runtime or production acceptance.

## 16. Thread output and context assessment

This is a long durable report; the Chat response remains a concise PM Rules Section 11
manifest. The current Architecture / Integration Thread should not continue. R55 authority
is terminalized after the four authorized docs are written and detached-audited. A new
ChatGPT PM durable-intake Thread is required; it may not inherit R55 to perform Git,
build/image, remote, runtime or production actions.

## 17. Exact next gate and stop point

```text
R55 docs/status sync and Git candidate plan WRITTEN
→ ChatGPT PM durable intake
→ only if PM accepts R55: GIT-CANDIDATE-ACCEPTED
→ only after separate user authorization: exact-path stage
→ exact-path commit
→ exact-path push
→ accepted build/image gate
→ deployment/lifecycle gate
→ bounded runtime-loaded A–H validation
→ PM acceptance of RUNTIME-LOADED
→ separate production accepted-fact work
```

No automatic authority follows R55. Stop after the required post-write detached audit.

## 18. Post-write detached artifact identities

The final R55 report identity and the final handoff identity are intentionally returned by the
post-write detached audit rather than self-referenced in R55. The handoff identity is also
repeated in the Chat manifest for independent intake:

```text
R55 report bytes/SHA-256: returned by post-write detached audit
handoff bytes: 12398
handoff SHA-256: 2c651618a1dec485b9d354c1a0bc9107aec2b1df88c9f6e65c441aab8d54cfe2
```
