# P1 Process KPI + Bounded API Local MVP — Exact Git Publication Manifest

状态：`PM-PREPARED / OWNER_GIT_AUTHORITY_REQUIRED`
日期：2026-08-12

目标：将 Mainline PM 已独立接受的 `P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1` 最终本地候选，以一个精确、低噪声、可审计的 Git commit 固化为后续 P1-G5 Remote Readiness / DB-API Reconciliation 工作的 durable code baseline。

## 1. Publication boundary

本 manifest 只定义未来 exact Git stage/commit 的路径与 hard gates。写入本 manifest 本身不授权：

- `git add`；
- commit；
- push；
- tag；
- reset / restore / checkout / stash / rebase / merge / clean；
- 产品修改、测试修改、contract 修改；
- DB runtime / migration；
- Docker / remote / SSH；
- PLC / V-PLC；
- production stimulus；
- P1-G5 execution。

已接受本地终态：

```text
GOAL_ID = P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1
GOAL_STATUS = COMPLETE
GOAL_TERMINAL = PASS / P1_PROCESS_KPI_BOUNDED_API_LOCAL_MVP_AUTONOMOUS_GOAL_COMPLETE
G3_PROCESS_KPI_CONTRACT_ACCEPTED = YES
G4_IMPLEMENTATION_ACCEPTED = YES
RELIABILITY_ACCEPTED = YES
DATA_QUALITY_ACCEPTED = YES
VERIFICATION_ACCEPTED = YES
FINAL_REVIEWS_BIND_SAME_CANDIDATE = YES
P1_G5_EXECUTION_AUTHORIZED = NO
```

本 publication 不重新执行 G3/G4 implementation、repair、Reliability、Data Quality、Verification 或测试。它只固化已经接受的 exact bytes。

## 2. Live Git baseline at manifest preparation

```text
branch = main
HEAD = cf4eac54d3f365b0addfaae13f5e7292e3233641
origin/main = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
origin/main...HEAD = 0<TAB>2
cached/staged = empty
git diff --check = PASS
```

当前 tracked dirty continuity：

```text
api/app/main.py                      # current accepted G4 candidate change; eligible below
docs/current_status.md               # protected external dirty; excluded
docs/thread_handoff/pm_operating_rules.md  # protected external dirty; excluded
```

`docs/current_status.md` 与 `docs/thread_handoff/pm_operating_rules.md` 不属于本 publication authority。

大规模 pre-existing untracked corpus 继续视为 external continuity state；不得 broad-stage、clean、adopt 或顺手提交。

## 3. Exact publication allowlist

未来 stage/commit 只允许以下 exact paths。

### 3.1 Final product / test candidate

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `api/app/main.py` | 524 | `038f7ea2c900f8288742586fe38430f6f5e0ce352fd1e4d7117d0e467f811dad` |
| `api/app/routes/process_metrics.py` | 19771 | `a7313117776e6ba8255bf2f60755bfad5a6bcf510767f0129720f8425984f1cb` |
| `api/tests/test_process_metrics_api.py` | 23821 | `6eb1e0ced1cb745755f94b3719c1a91923ca7f6ffe4d538b21004b2a9432566a` |

`api/app/main.py` 的 accepted G4 change 仅用于注册 `process_metrics` route；未来 publication gate 不授权再修改其 bytes。

### 3.2 G3 accepted production semantics contract

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/contracts/production_process_kpi_contract.md` | 28427 | `776e744314f9ec33884765c20f8d88dab45afeda74354cf7e10e7fc226809252` |
| `docs/reports/p1_g3_process_kpi_contract_20260811T1505Z.md` | 20348 | `306824e4e4326001f835ca759e2e0bc3ece12d999f0a1a8f990542992a6b8ff3` |

该 contract 保持已接受的 truthful data-sufficiency boundary：Performance / Availability / Full OEE 不因 Git publication 自动升级为 supported 或 numeric。

### 3.3 Final same-candidate focused reviews

只保留最终绑定 repaired candidate 的 review evidence，不提交已被 supersede 的首轮 HOLD/recovery mechanics。

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/reports/p1_g4_fresh_reliability_review_20260811T1635Z.md` | 11287 | `9cbeadce9563c7b5e7c42e2a3b47d4312e9875c7c227bf56c3be294e5534e8e4` |
| `docs/reports/p1_g4_dq_focused_data_quality_review_20260811T1645Z.md` | 15342 | `80cc2d38d8be1b009f167dbaa5897d05ff9bbbe394605e41b26d2ed248c2d770` |
| `docs/reports/p1_g4_v_focused_verification_20260811T1700Z.md` | 14084 | `f1d362e4d49e1b9b32cab6e75ca91cb40a71f6af4df8dc23c7681e58372f8a52` |

这些 review 均绑定同一最终 candidate 与同一 G3 contract。

### 3.4 Final Goal state / compact provenance

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/reports/p1_process_kpi_bounded_api_local_goal_closeout.md` | 10426 | `86b5aaeba5316376fb1c0d7b11d12d84cf1f2aead93fcced8dc024f6016f6120` |
| `docs/reports/shadow_pm_p1_process_kpi_bounded_api_local_ledger.md` | 24440 | `405e4c9af9308064e9aa25e04bd697fc3cc32bab839c847fc576207dc2cf8dba` |
| `docs/reports/p1_process_kpi_bounded_api_accepted_state_capsule.md` | 8201 | `643b2c39e1e37da542cf077be71d511e75035c0da08e6471f86a610e290a2b3a` |
| `docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_charter.md` | 20025 | `cfc05c53ef03f890cf5be2228f47369c2042457294384b82db9bd85b8c348dd3` |

Rationale：Closeout + final Ledger 建立最终 accepted state 与 action counters；Capsule + Charter 足以解释 predecessor truth、scope、runtime split、repair/autonomy 和 P1-G5 stop boundary。Goal Prompt / Bootstrap 属于启动 mechanics，不属于长期产品 baseline 的必要组成。

### 3.5 Publication record

未来 commit 还应包含本 manifest：

```text
docs/reports/p1_process_kpi_bounded_api_local_git_publication_manifest.md
```

本文件写入后的 exact bytes/SHA-256 必须在未来任何 `git add` 前重新机械核验。

## 4. Explicit exclusions

不得 stage/commit Section 3 之外的任何路径。

明确排除：

```text
docs/current_status.md
docs/thread_handoff/pm_operating_rules.md

docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_goal_prompt.md
docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_bootstrap.md

all docs/thread_handoff/pm_task_* not explicitly listed

docs/reports/p1_process_kpi_bounded_api_capability_check_*.md
docs/reports/p1_g4_i_bounded_production_metrics_api_*.md
docs/reports/p1_g4_r_focused_reliability_review_*.md
docs/reports/p1_g4_repair_accepted_fact_lineage_nok_detail_*.md
docs/reports/p1_g4_repair_cache_baseline_recovery_*.md

all other intermediate HOLD / repair / recovery reports
all unrelated P0/P1 tasks and reports
all unrelated external/untracked artifacts
```

中间 Reliability HOLD 与 repair/recovery history 已被 final Ledger/Closeout 准确记录；Git publication 不需要把全部控制面过程文件永久化。

已在 predecessor commit `cf4eac54d3f365b0addfaae13f5e7292e3233641` 中 publication 的 Quality/Trace 产品、tests、contract、P1 plan、G0/G1/R/DQ/V、前序 Goal governance 不需要重复列入本次 stage allowlist；它们通过 Git ancestry 继续存在。

## 5. Accepted predecessor continuity hard gates

未来 Git publication 前，以下 predecessor accepted objects 必须保持 exact identity；它们是 protected continuity hard gates，但不是本次 staged paths：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `api/app/routes/quality_trace.py` | 9538 | `6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a` |
| `api/tests/test_quality_trace_api.py` | 13296 | `bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c` |
| `docs/contracts/production_metrics_contract.md` | 8229 | `2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e` |

若这些 predecessor identities 漂移，停止：

```text
HOLD / P1_G3_G4_PUBLICATION_PREDECESSOR_IDENTITY_DRIFT
```

## 6. Pre-stage hard gates

获得未来 Owner exact stage/commit authority 后，在任何 `git add` 前必须重新机械核验：

1. physical cwd 与 Git root；
2. branch = `main`；
3. live `HEAD`；
4. live `origin/main` 与 ahead/behind；
5. cached/staged 仍为空；
6. Section 3.1–3.4 每个 path 的 regular/non-symlink、bytes、SHA-256 与本 manifest 一致；
7. Section 5 predecessor continuity identities 一致；
8. 本 manifest 自身 exact identity；
9. protected dirty docs 未进入 allowlist；
10. `git diff --check = PASS` before staging。

任一 final candidate / G3 contract / final review / closeout / ledger / governance identity drift：

```text
HOLD / P1_G3_G4_PUBLICATION_ACCEPTED_BASELINE_IDENTITY_DRIFT
```

仅存在 unrelated dirty/untracked artifacts 时继续保持排除，不自动 HOLD。

## 7. Exact staging rule

只有 Owner 后续明确授权后，才能对 Section 3 exact paths 执行显式：

```text
git add <exact-path-1> <exact-path-2> ...
```

严格禁止：

```text
git add .
git add -A
git add api/
git add docs/
```

staging 后、commit 前必须运行并检查：

```text
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

`git diff --cached --name-only` 必须与 Section 3 exact publication allowlist 完全相等。

若有额外 path，撤回本 gate 新增 staging 并：

```text
HOLD / P1_G3_G4_PUBLICATION_STAGED_SET_MISMATCH
```

如果 `git diff --cached --check` 发现 accepted immutable Markdown 中既有 whitespace，仅报告 exact warning set 并停止；不得自行修改 accepted bytes。任何 waiver 必须由 Owner 在观察到 exact warning set 后单独授权，不能由本 manifest 预先授予。

## 8. Commit boundary

建议 commit message：

```text
feat(p1): publish process metrics bounded API local MVP
```

只有 Owner 明确授权 commit 且 Section 6/7 hard gates PASS 后才可 commit。

commit PASS 只建立：

```text
P1_PROCESS_KPI_BOUNDED_API_LOCAL_GIT_COMMITTED = YES
```

它不自动建立：

```text
PUSHED
TAGGED
DEPLOYED
ACTIVATED
RUNTIME_LOADED
PRODUCTION_ACCEPTED
P1_G5_EXECUTION_AUTHORIZED
```

## 9. Push boundary

`git push` 不属于本 manifest authority。

若 Owner 后续另行授权 push，必须 fresh verify commit/head/branch/remote/staged state 后执行。未获得 push authority 时：

```text
PUSHED = NO
```

## 10. Post-publication next-step rule

本 publication commit 建立后，下一动作不是直接假设 P1-G5 可运行。

Mainline PM 应首先以 fresh publication `HEAD` 为基线，规划一个独立、小型、read-only 的 Remote API Readiness / Deployment Delta Preflight，回答：

```text
远端 Raspberry Pi 当前 API image/container lineage 是什么？
远端是否已经包含 GET /api/v2/process-metrics？
远端 DB/API topology 与 read-only reconciliation prerequisites 是否存在？
本地新 publication commit 与远端 deployed state 的 delta 是什么？
是否必须先做 Controlled API Deployment Goal？
```

Preflight 本身默认：

```text
REMOTE_READ_ONLY = YES
REMOTE_MUTATION = 0
DB_WRITE = 0
PRODUCTION_STIMULUS = 0
P1_G5_RECONCILIATION_EXECUTION = 0
```

只有 readiness/preflight 建立 fresh evidence 后，PM 才决定直接进入 G5 reconciliation，还是先规划独立 deployment Goal。

## 11. PM decision

```text
P1_PROCESS_KPI_BOUNDED_API_LOCAL_PM_ACCEPTED = YES
P1_PROCESS_KPI_BOUNDED_API_LOCAL_GOAL_CLOSED = YES
PUBLICATION_MANIFEST = WRITTEN
STAGE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
P1_G5_EXECUTION_AUTHORIZED = NO
NEXT_ACTION = OWNER_EXACT_STAGE_COMMIT_AUTHORITY
```
