# Sprint 4 D2-R7B T0-R2 Focused Reliability Transport Planning Review

结论：HOLD

## 1. Review identity and authority boundary

- 报告名称：Sprint 4 D2-R7B T0-R2 Focused Reliability Transport Planning Review
- 任务名称：D2-R7B-T0-R2 — Focused Reliability Review of Accepted Local-Image Transport Planning
- Authority ID：`PM-D2-R7B-T0-R2-FOCUSED-RELIABILITY-TRANSPORT-PLANNING-REVIEW-260801-1658`
- 执行 Thread：Reliability
- delivery：`REPOSITORY_DURABLE_REPORT`
- exact report path：`docs/reports/sprint4_d2_r7b_t0_r2_focused_reliability_transport_planning_review.md`
- 仅审查 original T0 + repaired T0-R1 的 precedence-resolved planning contract；不继承 Architecture 的 PASS、PM acceptance 或任何后续 Gate authority。
- precedence：T0-R1 明确 supersede 的 SSH argv、local stream、W0/S0 workspace、A0/T1 no-overwrite publication、durable paths 和 future allowlists 以 T0-R1 为准；其余未明确冲突的 T0 identity、archive validation、phase separation、failure protection 和 MVP 条款保留。
- 写入 authority：仅创建本 exact report；不修改任何输入、PM Rules、status/roadmap、handoff 或证据。

## 2. Frozen identities and live baseline

| input | bytes | SHA-256 |
|---|---:|---|
| T0-R2 task | 24243 | `5674518ebbf5c24dccc0ac8b979c08295597b24213e481c7e7b2d68f66c770da` |
| original T0 task | 27120 | `07aae9bded474e3b6d5942e0e6516aa13d9e70e8d3ceab3014692b39b1e0c2c3` |
| original T0 report | 24513 | `9e462dc30b5c4f92645a7f06cd79bb48ffe838072277c04ab962acba3091a77c` |
| T0-R1 task | 31660 | `1b24958de2dc82af80a00996b90b2f8cbbc20d8817d5a603baf1e0aba81982e5` |
| repaired T0-R1 report | 23486 | `2ac3e90d50c6252a35cd2445a29615b0ca7c31cc7643cfdace657aa035d2a937` |
| T0-R1-C1 task | 21432 | `a64c97de444801d00bb04aba1af77688e217b0f5bf76510656542f63b89e0777` |
| PM Rules snapshot | 56385 | `4de2fcc7d20a08c3bc33e18a7f2e94861e006a80bce1a76be3781547e6477528` |

All frozen files were regular, non-symlink, link count `1`, and matched bytes/SHA-256. The six untracked task/report inputs each had exactly one exact `??` membership, were unstaged, not indexed and not ignored. The target report was absent and non-symlink before creation.

Fresh Git baseline:

```text
repository   = /Users/chenjie/Documents/MES/edge-mes-demo
branch       = main
HEAD         = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
origin/main  = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
ahead/behind = 0/0
tracked diff = docs/thread_handoff/pm_operating_rules.md only
cached diff  = empty
git diff --check = PASS
git diff --cached --check = PASS
```

The PM Rules modification and unrelated untracked artifacts are pre-existing excluded dirt; they were not inspected beyond the required PM Rules sections and were not modified, staged, cleaned or absorbed. The accepted candidate remains a planning input only; no candidate, Docker daemon, local transport directory or remote target was inspected.

## 3. Review coverage and phase model

Reviewed sequence:

```text
T0 → T0-R1 → W0 → A0 → R0 → S0 → T1 → L0
```

| area | Reliability result |
|---|---|
| phase ownership, PM/Owner separation, no inheritance | Labels and claim separation are present; cross-phase terminal evidence is blocked by `REL-R2-X-001`. |
| W0 | `BLOCKER`: `REL-R2-W0-001` |
| A0 | `BLOCKER`: `REL-R2-A0-001` |
| R0 | `BLOCKER`: `REL-R2-R0-001`, `REL-R2-R0-002` |
| S0 | `BLOCKER`: `REL-R2-S0-001` |
| T1 | `BLOCKER`: `REL-R2-T1-001` |
| L0 | `BLOCKER`: `REL-R2-L0-001` |
| C0/D0/B0/A1/R1/P0/B1/C1 separation | `NO RELIABILITY FINDING` on the written no-inheritance boundary; no later authority is granted here. |
| candidate full-ID, Config/RootFS/archive identity retention | `NO RELIABILITY FINDING` on the retained identity contract; the A0 publication terminal gap remains a blocker. |

### REL-R2-W0-001

- ID: `REL-R2-W0-001`
- classification: `BLOCKER`
- affected Gate / contract section: W0; T0-R1 task §§10.4, 10.9, 11; T0-R1 report §§7, 10, 11; review §§10.3, 10.9.
- concrete failure scenario: W0 creates the base directory, then task-directory creation, chmod/fsync, final lstat or report persistence fails or is interrupted. The next W0 attempt sees an exact pre-existing directory and must HOLD, but the plan does not record whether it is the task-owned partial object or a foreign object, nor define a bounded recovery/reuse/cleanup Gate. `A0` cannot safely consume it and the directory can remain stranded without a durable terminal state.
- exact planning evidence: T0-R1 says W0 may create missing exact components one at a time, while “If either exact directory already exists at W0 start, W0 must fail closed” and provides no reuse authority. Its general §11 rule says only that other cleanup needs exact authority; it does not define W0 retained-state names, evidence or re-entry conditions.
- Reliability judgment: The create mutation can occur without an attributable terminal record or deterministic next action. The no-reuse rule prevents unsafe adoption but does not by itself make the stranded task-owned state recoverable or independently reviewable.
- minimum required correction or no-change rationale: Add an explicit W0 terminal ladder: any post-create/pre-PASS failure is `W0=HOLD / RETAINED_RECOVERY_REQUIRED`, with exact path, attempt ID, owner/device/inode/mode/link/empty state and mutation count persisted before the next phase. Require a separate PM/Owner recovery authority to either bind and reuse the exact task-owned object or clean it; foreign/ambiguous objects remain untouched. No W0 PASS or A0 authority may follow the failure.
- scope classification: `current-gate necessary repair`
- blocks Verification: `YES`

### REL-R2-S0-001

- ID: `REL-R2-S0-001`
- classification: `BLOCKER`
- affected Gate / contract section: R0/S0; T0-R1 task/report §10.5 and §10.9; review §§10.5–10.6.
- concrete failure scenario: R0 observes a safe pre-existing `/opt/edge-mes-demo/.transport` and accepts it, but S0 is described as creating `.transport` only when R0 proved it absent. S0 therefore has no explicit branch for safe parent reuse: it may fail on `mkdir`, silently adopt a parent without a frozen reuse decision, or treat a task-owned partial parent as foreign. If S0 creates `.transport` and child creation then fails, the next attempt has the same unresolved state.
- exact planning evidence: T0-R1 explicitly says “`.transport` may be absent or may pre-exist” and defines safe pre-existing acceptance in R0, then says S0 may create `.transport` “only when R0 proved it absent and eligible”; its report repeats that pre-existing acceptance and “only if R0 proved it absent” creation rule without a reuse/partial-state matrix.
- Reliability judgment: R0 and S0 give conflicting ownership of a legitimate pre-existing parent. The remote directory mutation and re-entry behavior are not deterministic, and an unreviewed prior partial directory could be adopted by a later attempt.
- minimum required correction or no-change rationale: Define separate branches: a safe R0-accepted pre-existing `.transport` is reused without creation and only the absent task child may be created; a pre-existing task child is always HOLD; a parent created by a failed S0 attempt is retained and cannot be reused or cleaned without a new exact recovery authority. Recheck parent identity immediately before child creation and in final evidence.
- scope classification: `current-gate necessary repair`
- blocks Verification: `YES`

### REL-R2-R0-001

- ID: `REL-R2-R0-001`
- classification: `BLOCKER`
- affected Gate / contract section: R0→S0/T1 freshness; T0-R1 task/report §§10.5, 10.9, 11; review §§10.5, 10.6, 10.7.
- concrete failure scenario: R0 accepts the host identity, staging-parent device/inode/owner/mode and active-deployment separation. Before S0 or T1, the SSH target mapping or stable host identity changes, or the parent is replaced. S0 checks creation-time state, while T1 consumes “accepted R0 identity” and checks only the exact temporary/final archive objects; it can stream bytes into a replaced or foreign staging tree without proving the current host/parent is the R0 object.
- exact planning evidence: T0-R1 requires R0 to observe current identity and `.transport` state, but the T1 allowlist only requires accepted A0/R0/S0 identities and the publication script only binds temp/final lstat/hash transitions. No consuming Gate freezes a fresh host identity plus parent device/inode/owner/mode recheck immediately before remote mutation.
- Reliability judgment: R0 is a one-shot eligibility observation, not a durable lease. Consuming its mutable path and target facts without a fresh binding creates a TOCTOU path to protected-object or wrong-target mutation.
- minimum required correction or no-change rationale: Require S0 and T1 to re-observe or otherwise bind the current stable host identity and exact staging-parent identity immediately before their mutations; abort on any drift. T1 must recheck parent device/inode/owner/mode and active-tree separation, not only child archive identity. A stale R0 must not authorize transport.
- scope classification: `current-gate necessary repair`
- blocks Verification: `YES`

### REL-R2-R0-002

- ID: `REL-R2-R0-002`
- classification: `BLOCKER`
- affected Gate / contract section: R0 terminal evidence; T0-R1 task §10.5 and §10.10; T0-R1 report §§6, 11; review §10.5 and §10.10.
- concrete failure scenario: The one R0 SSH call prints hostname and architecture, then disconnects or exceeds an output bound before staging, free-space, tool, Collector or daemon fields are complete. The plan has no required complete-record marker, exact size cap, EOF rule or malformed/partial-output terminal state, so a runner could persist/use a partial observation or combine it with stale fields.
- exact planning evidence: The plan says the probe “records” the required fields and that stdout/stderr are bounded/hashable in the evidence list, but it does not freeze a complete schema, required-field set at parse time, numeric bound, single-record/EOF rule or `NOT_OBSERVED` result for truncation and parse failure.
- Reliability judgment: A partial one-shot observation can be mistaken for target eligibility. This permits false R0 PASS and unsafe S0/T1 entry even though the required current state was never coherently observed.
- minimum required correction or no-change rationale: Freeze a versioned persisted R0 result with all required fields, `complete=true`, one record, SSH exit `0`, clean EOF and raw/normalized hashes. Any missing field, extra/malformed/truncated output, nonzero/timeout or parser exception must terminalize `R0=HOLD / NOT_OBSERVED`; no stale-field merge or later-Gate authority is allowed.
- scope classification: `current-gate necessary repair`
- blocks Verification: `YES`

### REL-R2-A0-001

- ID: `REL-R2-A0-001`
- classification: `BLOCKER`
- affected Gate / contract section: A0; original T0 §§5.2–5.3 and 10.8; T0-R1 task/report §§10.6, 10.9, 11; review §§10.4, 10.9.
- concrete failure scenario: `os.link(temp, final)` succeeds, then final fsync, parent fsync, lstat/hash proof or report write fails before temp unlink; or temp unlink succeeds and the second parent fsync/final evidence write fails. A final object may coexist with temp at link count `2`, or an accepted-looking final may remain without a completed durable proof. A new A0 attempt cannot distinguish this task-owned state from a foreign collision and has no explicit reconciliation/cleanup terminal.
- exact planning evidence: T0-R1 gives the success sequence “link → fsync/stat/hash → unlink temp → fsync → final proof” and says errors are terminal, but its failure matrix only generally retains an ambiguous temp and says other cleanup needs exact authority. It does not define the final+temp, final-only-after-proof-failure, or report-write-failure states and their non-retry/recovery authority.
- Reliability judgment: The local no-overwrite primitive prevents replacement, but it does not by itself prove what a terminally interrupted attempt means. A later Gate could mistake a durable object for accepted archive or an operator could retry into a collision without a durable state decision.
- minimum required correction or no-change rationale: Add an A0 state table for every post-link boundary. Until the final post-unlink proof is durably recorded, `ARCHIVE ACCEPTED` remains `NO`; persist `A0=HOLD / RETAINED_RECOVERY_REQUIRED` with both path identities and bytes/SHA/link counts; prohibit retry/reuse/removal under A0; authorize only a separate exact reconciliation/cleanup Gate, including report-write failure handling.
- scope classification: `current-gate necessary repair`
- blocks Verification: `YES`

### REL-R2-T1-001

- ID: `REL-R2-T1-001`
- classification: `BLOCKER`
- affected Gate / contract section: T1; original T0 §7 and 10.8; T0-R1 task/report §§10.3, 10.7, 10.9, 11; review §10.7 and §10.9.
- concrete failure scenario: The first SSH stream exits or times out after remote `dd` created a complete temporary object, or the second SSH completes `ln`/`rm` and then disconnects before the caller receives final evidence. Remote state may be temp-only, temp+final with link count `2`, or final-only. The plan says no retry and retain ambiguity, but does not define a durable `NOT_OBSERVED` terminal result that prevents L0 or a new attempt from treating a pathname as accepted.
- exact planning evidence: T1 is fixed at exactly two SSH calls; any local exception/nonzero is HOLD; the remote script performs `ln`, proof and `rm` in sequence. The general matrix says to retain a partial/ambiguous object and obtain new authority, but does not bind the unobserved call outcome, exact remote state, or L0 entry prohibition to a durable terminal record.
- Reliability judgment: A remote mutation can complete without a durable, independently reviewable transport terminal state. This is an unsafe ambiguity at the boundary where `TRANSPORTED=YES` must not be inferred from a path or command exit alone.
- minimum required correction or no-change rationale: Freeze T1 terminal states for local-open/hash failure, SSH-unobserved, remote partial, publication-complete-but-unobserved and verified PASS. Record call count, exit/timeout, observed remote inode/device/link/bytes/SHA or `NOT_OBSERVED`; any uncertainty is `T1=HOLD`, blocks L0 and retry, retains objects, and requires a separate exact reconciliation/cleanup authority.
- scope classification: `current-gate necessary repair`
- blocks Verification: `YES`

### REL-R2-L0-001

- ID: `REL-R2-L0-001`
- classification: `BLOCKER`
- affected Gate / contract section: L0; original T0 §8 and 10.8; T0-R1 task/report §§10.9, 11; review §10.8–10.10.
- concrete failure scenario: L0 proves the exact image absent, executes one `docker image load`, then the post-load inspect, script output, SSH call or durable report fails. The daemon may now contain an image or additional names, but Config/RootFS equality and terminal completion are unproven. A retry encounters a pre-existing exact image and needs explicit reuse authority, while the plan provides no exact-ID reconciliation state; an output/tag-based shortcut could create false `REMOTE IMAGE ACCEPTED`.
- exact planning evidence: The plan permits one SSH script containing pre-inspect, one load and post-inspect; it requires retaining archive/object and no removal on failure, but gives no `LOAD_STATE_UNCERTAIN` terminal record, complete post-state schema or separate full-ID reconciliation Gate before retry/cleanup.
- Reliability judgment: L0 can mutate Docker state without durable terminal evidence of what was loaded. Retention alone protects against deletion but does not prevent an unsafe retry or false load acceptance.
- minimum required correction or no-change rationale: Add an L0 terminal ladder with pre-state, load exit, complete post-state and report-write outcome. Any post-load/SSH/parser/report uncertainty is `L0=HOLD / LOAD_STATE_UNCERTAIN`; prohibit retry/load/tag/remove and later Gate entry until a separately authorized exact-ID reconciliation/cleanup Gate proves the object state.
- scope classification: `current-gate necessary repair`
- blocks Verification: `YES`

### REL-R2-X-001

- ID: `REL-R2-X-001`
- classification: `BLOCKER`
- affected Gate / contract section: all future W0/A0/R0/S0/T1/L0 execution locks and durable terminalization; PM Rules §§3 and 11; T0-R1 task/report §§9–11; review §10.10.
- concrete failure scenario: A future runner/script is tested and its bytes/SHA are stated to be locked, but no declared exact `EXECUTION_LOCK` record is persisted before the SSH/Docker/archive mutation. Alternatively, the mutation completes or partially completes and writing the report/JSON fails. The next Thread then cannot prove the exact helper/argv/call budget used or whether authority was consumed, and may retry or let a later Gate rely on an unproven state.
- exact planning evidence: T0-R1 requires script bytes/SHA/argv to be “locked” and provides report/JSON/script paths, but its durable path table declares no lock artifact or required lock fields. Its failure rules do not state that report-write failure after mutation is terminal HOLD with no retry. PM Rules require a persisted `EXECUTION_LOCK` before external authority and distinguish `WRITTEN` from later states.
- Reliability judgment: The planning contract does not make authority consumption and post-mutation terminal state durable under the very failures the Gate is meant to contain. This is a cross-phase false-retry and evidence-identity blocker.
- minimum required correction or no-change rationale: Each future Gate must declare an exact lock location (or exact required fields in its bounded JSON), persist pre-task facts, artifact bytes/SHA, argv, budget, authority and validation count before mutation, and record mutation outcome even when final report writing fails. Report-write failure is `HOLD`, never a retry signal; retained state requires PM-authorized reconciliation/cleanup.
- scope classification: `current-gate necessary repair`
- blocks Verification: `YES`

## 4. Findings count and Verification eligibility

```text
BLOCKER          = 8
RECOMMENDATION   = 0
NOTE             = 0
Verification eligible = NO
```

The phase labels and retained full-ID/config/RootFS claims are not independently defective, but the eight blockers prevent a safe, deterministic entry to Verification. No material recommendation is separated from the required current-gate repairs.

## 5. Action counters and changed-file boundary

```text
Python executed                         = 0 / NO
Docker action                           = 0 / NO
Archive creation/validation             = 0 / NO
Local or remote workspace mutation      = 0 / NO
SSH/network/remote command              = 0 / NO
Deployment/activation/service lifecycle = 0 / NO
Git stage/commit/push/tag/reset/restore = 0 / NO
Authorized report create                = 1
```

Task-owned changed/created set is exactly the one report path above. The pre-existing PM Rules tracked diff, task/report inputs and unrelated external untracked paths are excluded and unchanged. No helper, JSON, archive, backup, workspace, second report or temporary artifact was created.

## 6. MVP, next Gate and non-inheritance

- MVP classification：`MVP-ALIGNED`
- product claim served：accepted local image → reliable archive/transport/remote-object planning
- scope drift：`NO`
- single next Gate after PM intake：`PM Independent Intake — D2-R7B-T0-R2 HOLD`
- PM must choose a narrowly scoped Architecture / Integration planning correction after intake; this report does not publish Verification or W0/A0/R0/S0/T1/L0 tasks.
- No outcome here authorizes archive/workspace mutation, Docker, SSH/network/remote, deployment, activation, runtime, production, rollback or Git action.

## 7. Final terminal record

The durable report contains exactly two identical terminal conclusion fields; both are `HOLD`. It contains no provisional terminal wording. The final window manifest supplies this report's bytes/SHA-256 after the final checks.

结论：HOLD
