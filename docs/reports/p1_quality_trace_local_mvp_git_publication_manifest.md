# P1 Quality + Trace Local MVP — Exact Git Publication Manifest

状态：`PM-PREPARED / OWNER_GIT_AUTHORITY_REQUIRED`
日期：2026-08-11
目标：将已经完成 Mainline PM independent intake 的 `P1-SHADOW-PM-QUALITY-TRACE-LOCAL-MVP-V1` 最终 accepted local MVP 以一个精确、可审计、低噪声的 Git commit 固化为下一 Goal 的 durable baseline。

## 1. Publication boundary

本 manifest 只定义未来 Git publication 的 exact path allowlist；它本身不授权 `git add`、commit、push、tag、reset、checkout、clean 或任何其它 Git mutation。

本 publication 的产品状态已经完成：

```text
GOAL_STATUS = COMPLETE
GOAL_TERMINAL = PASS / P1_QUALITY_TRACE_LOCAL_MVP_AUTONOMOUS_GOAL_COMPLETE
G2_IMPLEMENTATION_ACCEPTED = YES
RELIABILITY_ACCEPTED = YES
DATA_QUALITY_ACCEPTED = YES
VERIFICATION_ACCEPTED = YES
FINAL_CANDIDATE_REVIEWS_BIND_SAME_STATE = YES
```

本 publication 不重新执行产品实现、repair、Reliability、Data Quality、Verification、DB/API runtime、Docker、remote、PLC/V-PLC 或 production stimulus。

## 2. Live Git baseline at manifest preparation

```text
branch = main
HEAD = dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
origin/main = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
origin/main...HEAD = 0<TAB>1
cached/staged = empty
git diff --check = PASS
```

Known protected tracked-dirty files remain excluded unless a later Owner authority explicitly names them:

```text
docs/current_status.md
docs/thread_handoff/pm_operating_rules.md
```

All unrelated pre-existing untracked artifacts, including historical P0/P1 `pm_task_*`, repair/recovery reports, capability dry-run artifacts and other external files, remain excluded.

## 3. Exact publication allowlist

Only the following paths are eligible for the future exact stage/commit operation.

### 3.1 Product / test candidate

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `api/app/routes/quality_trace.py` | 9538 | `6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a` |
| `api/app/main.py` | 464 | `2bdc34c1950654ca81d0041171a3c17d646c87e9655e79c3bac120baf47438ed` |
| `api/tests/test_quality_trace_api.py` | 13296 | `bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c` |
| `docs/contracts/production_metrics_contract.md` | 8229 | `2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e` |

### 3.2 Durable P1 planning / semantic / review evidence

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/reports/p1_production_truth_semantics_trusted_consumption_plan.md` | 15505 | `48a9d8af24ed4f106ef724634229055887ce71c74ffc38d208aa28bc2192d88e` |
| `docs/reports/p1_g0_production_source_adequacy_semantic_boundary_freeze.md` | 38063 | `10982b8a92d0c33bfd18812ec14879af9ea74f658a74ab046b4d71d2725ef87e` |
| `docs/reports/p1_g1_production_semantics_contract.md` | 12783 | `479639289eceb7938659ba3c487aa08110f19783c849f8cacd017cdd18c0e1f7` |
| `docs/reports/p1_g2_r_focused_reliability_review.md` | 7917 | `655bcd3ee79a7e55d93dd24a47a4abc41bcaecb756fddc8a0f6856e05fedabea` |
| `docs/reports/p1_g2_dq_focused_data_quality_review.md` | 11312 | `10e3410e5ddb99162e85c890cbc9e04295b96afae7f090ce38b05201ed3b630d` |
| `docs/reports/p1_g2_v_focused_verification_review.md` | 11954 | `881c87db5e5f147546affded575f983af4c56a55a1181b1076c57ab94d271c74` |
| `docs/reports/p1_quality_trace_local_mvp_goal_closeout.md` | 8778 | `5368aa3bb436841f0f9bfbbdcf0aefcce7982fc9b5184d5f08d85791b0c20010` |
| `docs/reports/shadow_pm_p1_quality_trace_local_mvp_ledger.md` | 31844 | `2d903acc176454e81721cd7d795b2cd8da583ca15a1132c585c68f9379045127` |

### 3.3 Durable Goal governance required to interpret the accepted baseline

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter.md` | 26966 | `0672cb1771eb7eedf1f6d3ecff65a975509efc7618e6164a8b7cfcb419456bfe` |
| `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter_amendment_001_project_test_runtime.md` | 5197 | `c8b558c75a926415041a90de5e8221e514e58cec80e48361c23480d83242c633` |

### 3.4 Publication record

The future commit should also include this exact manifest path:

```text
docs/reports/p1_quality_trace_local_mvp_git_publication_manifest.md
```

Its materialized identity is computed after write and must be verified immediately before any future staging authority is consumed.

## 4. Explicit exclusions

The future publication must not stage or commit any path outside Section 3.

Explicitly excluded categories include:

```text
docs/current_status.md
docs/thread_handoff/pm_operating_rules.md
all docs/thread_handoff/pm_task_* not explicitly listed
shadow_pm_p1_quality_trace_local_mvp_goal_prompt.md
shadow_pm_p1_quality_trace_local_mvp_bootstrap_dry_run.md
shadow_pm_p1_subagent_capability_dry_run.md
p1_g2_i_quality_trace_implementation.md
p1_g2_i_test_runtime_override_recovery.md
p1_g2_i_candidate_import_syntax_repair.md
p1_g2_i_duplicate_fact_key_test_repair.md
p1_g2_i_trace_test_helper_identity_repair.md
all unrelated P0 task/report artifacts
all unrelated external/untracked artifacts
```

Rationale：最终 product truth、contract、accepted reviews、closeout、final ledger 与 governing Charter 已足够建立 durable accepted baseline；中间 launcher、recovery mechanics 与 closed failure-family reports 保留在当前 worktree 即可，不把控制面噪声永久化到本 publication commit。

## 5. Pre-stage hard gates

未来 Owner 明确授权 exact stage/commit 后，PM 必须在任何 `git add` 前重新机械核验：

1. physical repo / Git root / branch；
2. live `HEAD` / `origin/main`；
3. cached/staged 仍为空；
4. Section 3.1–3.3 每个 authority-bearing path 的 current bytes/SHA 与本 manifest 一致；
5. 本 manifest 自身 exact identity；
6. protected dirty files 仍未进入 allowlist；
7. `git diff --check = PASS`。

任一 product/contract/review/closeout identity drift：

```text
HOLD / P1_PUBLICATION_ACCEPTED_BASELINE_IDENTITY_DRIFT
```

若只存在 unrelated external dirty/untracked artifacts，保持排除，不构成自动 HOLD。

## 6. Exact staging rule

获得 Owner stage authority 后，只允许对 Section 3 的 exact paths 执行显式 `git add <exact-path> ...`。

禁止：

```text
git add .
git add -A
git add docs/
git add api/
```

staging 后、commit 前必须核验：

```text
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

`git diff --cached --name-only` 必须与 Section 3 exact allowlist 完全一致；出现任何额外 path：立即 unstage 本 gate 新增 staging，并：

```text
HOLD / P1_PUBLICATION_STAGED_SET_MISMATCH
```

## 7. Commit boundary

建议 commit message：

```text
feat(p1): publish accepted-fact quality and trace local MVP
```

commit 只在 Owner 明确授权 commit 且 staged-set hard gate PASS 后执行。

commit PASS 只建立：

```text
P1_QUALITY_TRACE_LOCAL_MVP_GIT_COMMITTED = YES
```

它不自动建立：

```text
PUSHED
TAGGED
DEPLOYED
RUNTIME_LOADED
PRODUCTION_ACCEPTED_FOR_NEW_API
P1_G3_EXECUTION_AUTHORIZED
```

## 8. Push boundary

`git push` 不属于本 manifest 自动 authority。

如 Owner 后续单独授权 push，必须先机械确认：

- commit 已建立；
- live branch/head；
- staged/cached empty；
- push target/remote 明确；
- no unrelated commit unexpectedly entered publication lineage。

未获得单独 push authority前：

```text
PUSHED = NO
```

## 9. Next Goal baseline rule

下一 Goal：

```text
P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1
```

不得以当前 dirty worktree SHA identities 作为长期 genesis baseline。

应在本 publication commit 建立后，以 fresh live commit identity 作为 Genesis Git baseline，再物化：

```text
Accepted State Capsule
Goal Charter
Genesis Ledger
Goal Prompt
Bootstrap / capability procedure
```

下一 Goal 只覆盖 P1-G3 + P1-G4 local acceptance，不继承 Git、remote、DB mutation、Collector、config、PLC/V-PLC 或 P1-G5 authority。

## 10. PM decision

```text
P1_LOCAL_MVP_PM_ACCEPTED = YES
P1_LOCAL_MVP_GOAL_CLOSED = YES
PUBLICATION_MANIFEST = WRITTEN
STAGE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
NEXT_ACTION = OWNER_EXACT_STAGE_COMMIT_AUTHORITY
```
