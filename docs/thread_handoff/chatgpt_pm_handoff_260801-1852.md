# Edge MES Demo — ChatGPT PM Handoff — 2026-08-01 18:52 CST

## 1. Handoff identity

- Project: Edge MES Demo
- Project absolute path: `/Users/chenjie/Documents/MES/edge-mes-demo`
- Handoff file: `docs/thread_handoff/chatgpt_pm_handoff_260801-1852.md`
- Handoff time basis: China Standard Time / UTC+8
- Trigger: Owner instructed the current ChatGPT PM to enter the PM handoff workflow after PM independent acceptance of D2-R7B-T0-R3-C1-R1.
- Current handoff status: `WRITTEN / UNSTAGED / UNCOMMITTED / UNPUSHED`

This handoff freezes the accepted local Collector candidate identity, the full accepted-local-image transport-planning authority chain through T0-R3-C1-R1, the current Git and external-dirty boundary, the absence of execution authority, and the exact next review sequence.

This handoff supersedes `docs/thread_handoff/chatgpt_pm_handoff_260801-1400.md` for current ChatGPT PM takeover truth. The 14:00 handoff remains historical evidence for the accepted local-image state before the transport-planning branch. It must not be used to restore the transport branch to “not started,” to resume any terminal T0/T0-R1/T0-R2/T0-R3/T0-R3-C1 authority, or to skip the pending focused Reliability rereview.

This handoff does not publish a Reliability task and does not authorize W0, A0, R0, S0, T1, L0, any recovery category, Python, Docker, archive creation, external workspace creation, SSH/network/remote access, image load, deployment, activation, runtime validation, production acceptance, rollback or Git mutation.

At handoff time there is no active Architecture / Integration, Reliability, Data Quality, Verification, Python, Docker, Git, archive, local-external-filesystem, SSH, remote, deployment, activation, runtime, production or rollback authority.

## 2. Live Git baseline

Fresh read-only recovery immediately before this handoff established:

```text
repository:
/Users/chenjie/Documents/MES/edge-mes-demo

branch:
main

HEAD:
0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c

origin/main:
0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c

ahead / behind:
0 / 0

tracked diff:
docs/thread_handoff/pm_operating_rules.md only

cached diff:
empty

git diff --check:
PASS

git diff --cached --check:
PASS
```

Latest committed `HEAD`:

```text
commit:
0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c

subject:
Sync accepted local image governance status

changed paths:
docs/current_status.md
docs/reports/sprint4_d2_r7b_g0_governance_status_sync_execution.md
docs/roadmap.md
docs/thread_handoff/pm_task_20260801T0639Z_d2_r7b_g0_governance_status_sync.md
```

Recent committed history:

```text
0bbfef9 Sync accepted local image governance status
7ba7a05 Add PM handoff before Buildx environment repair gate
0e7544a Add PM handoff for build image execution preparation
796c87b Accept build image planning contract
c3acb33 Sync post-closeout status and PM handoff
934ced7 Accept runtime-loaded observability implementation
4a733d7 Add PM handoff before runtime-loaded implementation
ce22ca7 Add ChatGPT PM handoff after authority-chain closeout
```

Exact Collector product-source authority remains:

```text
934ced7b9659cb566628b1709cf6d73463a534d8
```

The docs/governance `HEAD` is not a substitute for the product-source identity.

Before this handoff was created, untracked accounting was:

```text
raw    = 403
unique = 403
duplicates = 0
```

After this handoff is created, expected informational accounting is:

```text
raw    = 404
unique = 404
duplicates = 0
```

Global untracked counts are informational only. They do not authorize inspection, cleanup, staging, adoption or deletion of unrelated paths.

## 3. PM Rules and external dirty boundary

The sole tracked modification remains:

```text
docs/thread_handoff/pm_operating_rules.md
```

Frozen local identity:

```text
bytes:
56385

SHA-256:
4de2fcc7d20a08c3bc33e18a7f2e94861e006a80bce1a76be3781547e6477528

state:
modified / unstaged / uncommitted / unpushed
```

Do not edit, restore, stage, commit, push, replace or absorb this file without an exact Owner-approved Git/governance authority.

Never use broad staging:

```text
git add .
git add -A
git add docs/
```

The repository also contains many pre-existing untracked task files, reports, evidence roots, prior handoffs, reporting artifacts and `frontend/next-env.d.ts`. Unless a future Prompt names an exact path, all remain external and excluded.

The T0 transport-planning tasks and reports named in this handoff are also currently untracked and unstaged. Their current durable role is planning/review evidence; this handoff does not grant Git candidate authority for them.

## 4. Committed governance status versus current Gate truth

The top current sections of `docs/current_status.md` and `docs/roadmap.md`, committed at `0bbfef9`, correctly freeze:

```text
PRODUCT SOURCE COMMIT        = 934ced7b9659cb566628b1709cf6d73463a534d8
LOCAL CANDIDATE IMAGE ID     = sha256:8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013
R67 local candidate chain    = CLOSED / PASS
EXISTING CANDIDATE VALIDATED = YES
LOCAL IMAGE ACCEPTED         = YES
REBUILD REQUIRED             = NO
TRANSPORTED                  = NO
ACTIVE AUTHORITY             = NONE
```

Those committed status documents predate the completed T0 planning/review/correction chain. They still name accepted local-image transport planning as the next eligible branch and do not contain T0-R1 through T0-R3-C1-R1 closure.

Current post-`0bbfef9` Gate truth is established by:

1. this handoff;
2. the original T0 planning report;
3. the repaired T0-R1 report and accepted T0-R1-C1 terminal correction;
4. the T0-R2 Reliability HOLD report and PM intake accepting its eight blockers;
5. the T0-R3 planning correction report;
6. the terminal procedural T0-R3-C1 HOLD report;
7. the corrected T0-R3-C1-R1 report;
8. PM independent intake accepting T0-R3-C1-R1 on 2026-08-01 before this handoff;
9. fresh live Git observations.

Do not silently update `docs/current_status.md`, `docs/roadmap.md`, README or PM Rules during Reliability rereview. A later governance sync requires its own exact task if the Owner chooses it.

## 5. Accepted local candidate identity

Current accepted candidate:

```text
sha256:8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013
```

Accepted product source:

```text
934ced7b9659cb566628b1709cf6d73463a534d8
```

Retained accepted facts:

```text
platform:
linux/arm64

Docker context:
colima

WorkingDir:
/app

Cmd:
["python", "-m", "app.main"]

ordered RootFS layers:
9
```

Current accepted claim:

```text
EXACT-COMMIT MATERIALIZATION = PASS
EXISTING CANDIDATE VALIDATED = YES
LOCAL IMAGE ACCEPTED         = YES
PM ACCEPTED                  = YES
REBUILD REQUIRED             = NO
```

This acceptance applies only to the exact full image ID. A tag, archive, remote pathname, remote Docker object, Compose service or running container must not inherit acceptance by name, history or similarity.

No new Docker inspection occurred in the T0 planning branch. Candidate facts are retained from the accepted local-image chain and must not be silently refreshed or changed by a docs-only review.

## 6. Transport-planning chain identity

### 6.1 Original T0

Task:

```text
path:
docs/thread_handoff/pm_task_20260801T0704Z_d2_r7b_t0_accepted_local_image_transport_planning.md

bytes:
27120

SHA-256:
07aae9bded474e3b6d5942e0e6516aa13d9e70e8d3ceab3014692b39b1e0c2c3
```

Report:

```text
path:
docs/reports/sprint4_d2_r7b_t0_accepted_local_image_transport_plan.md

bytes:
24513

SHA-256:
9e462dc30b5c4f92645a7f06cd79bb48ffe838072277c04ab962acba3091a77c
```

Original T0 established the base W0 → A0 → R0 → S0 → T1 → L0 planning sequence and retained candidate/archive/Config/ordered-RootFS identity separation. It was not PM-final accepted because B1–B6 required correction.

### 6.2 T0-R1 and T0-R1-C1

T0-R1 task:

```text
path:
docs/thread_handoff/pm_task_20260801T0751Z_d2_r7b_t0_r1_focused_transport_planning_executability_durable_path_correction.md

bytes:
31660

SHA-256:
1b24958de2dc82af80a00996b90b2f8cbbc20d8817d5a603baf1e0aba81982e5
```

T0-R1 report:

```text
path:
docs/reports/sprint4_d2_r7b_t0_r1_focused_transport_planning_executability_and_durable_path_correction.md

bytes:
23486

SHA-256:
2ac3e90d50c6252a35cd2445a29615b0ca7c31cc7643cfdace657aa035d2a937
```

T0-R1-C1 task:

```text
path:
docs/thread_handoff/pm_task_20260801T0818Z_d2_r7b_t0_r1_c1_terminal_state_reconciliation_size_compression.md

bytes:
21432

SHA-256:
a64c97de444801d00bb04aba1af77688e217b0f5bf76510656542f63b89e0777
```

PM intake accepted T0-R1-C1. T0-R1 is the controlling text for B1–B6 corrections:

```text
B1 SSH option terminator and command argv shape
B2 opened accepted-A0 FD as the sole local stream producer
B3 exact W0 local workspace materialization boundary
B4 exact R0/S0 remote preflight and workspace separation
B5 A0 hard-link no-overwrite publication
B6 T1 exclusive temp plus hard-link no-overwrite publication and repository-durable paths
```

### 6.3 T0-R2 Reliability review

Task:

```text
path:
docs/thread_handoff/pm_task_20260801T0858Z_d2_r7b_t0_r2_focused_reliability_transport_planning_review.md

bytes:
24243

SHA-256:
5674518ebbf5c24dccc0ac8b979c08295597b24213e481c7e7b2d68f66c770da
```

Report:

```text
path:
docs/reports/sprint4_d2_r7b_t0_r2_focused_reliability_transport_planning_review.md

bytes:
20240

SHA-256:
089b28fb82100ecadbf05f3fbf08a0ec5c4836e5cc2eb4fcbedd0faace2d5ec0

terminal conclusion:
HOLD

findings:
BLOCKER=8 / RECOMMENDATION=0 / NOTE=0
```

PM independent intake accepted all eight blocker classifications:

```text
REL-R2-W0-001  W0 partial-create retained-state and recovery terminal gap
REL-R2-S0-001  S0 parent reuse/creation/partial ownership matrix gap
REL-R2-R0-001  R0→S0/T1 freshness and target/parent rebinding gap
REL-R2-R0-002  R0 complete-record/schema/EOF/NOT_OBSERVED gap
REL-R2-A0-001  A0 post-link/post-unlink terminal-state gap
REL-R2-T1-001  T1 mutation-complete-but-unobserved terminal gap
REL-R2-L0-001  L0 load-state-uncertain reconciliation gap
REL-R2-X-001   pre-mutation EXECUTION_LOCK and post-mutation durable terminal gap
```

T0-R2 is a Reliability review result, not controlling planning text and not execution authority.

### 6.4 T0-R3 planning correction

Task:

```text
path:
docs/thread_handoff/pm_task_20260801T0926Z_d2_r7b_t0_r3_reliability_blocking_terminalization_freshness_recovery_contract_repair.md

bytes:
29504

SHA-256:
7ac5f7cae387692d8776f185f0bcc746d5c29fe851de562b32181e0c766fa2c6
```

Report:

```text
path:
docs/reports/sprint4_d2_r7b_t0_r3_reliability_blocking_terminalization_freshness_and_recovery_contract_repair.md

bytes:
24535

SHA-256:
0866247f79f2f0f125c211bc00324a9d97115e236c58f929304fda187f19b08b

reported conclusion:
PASS WITH RECOMMENDATIONS

PM acceptance:
NO as a standalone final correction
```

T0-R3 supplied substantive corrections for the eight Reliability blockers: Gate-specific execution locks, durable terminalization, failure-only recovery categories, W0/S0 ownership matrices, R0 complete-record behavior, same-call freshness rebinding and A0/T1/L0 uncertainty ladders.

PM intake found three additional planning defects in T0-R3:

```text
PM-R3-001 OpenSSH remote-command serialization ambiguity
PM-R3-002 recursive/self-referential evidence digest ambiguity
PM-R3-003 fixed durable paths conflicting with recovery and fresh attempts
```

T0-R3 remains controlling for its non-conflicting terminal, freshness, ownership, recovery and execution-lock clauses. Its three conflicting clauses are superseded by T0-R3-C1-R1.

### 6.5 T0-R3-C1 terminal procedural HOLD

Task:

```text
path:
docs/thread_handoff/pm_task_20260801T0956Z_d2_r7b_t0_r3_c1_ssh_serialization_nonrecursive_identity_attempt_scoped_paths.md

bytes:
31255

SHA-256:
c68b9a6ed3840c124704d34a771fa6910a39117642dbcf51d4c1f105887f1124
```

Report:

```text
path:
docs/reports/sprint4_d2_r7b_t0_r3_c1_ssh_serialization_nonrecursive_identity_and_attempt_scoped_paths_correction.md

bytes:
2423

SHA-256:
d1957b79ab582e9644d5ca4c63fc17e525b762c38a97231bf4119abbf8863d4e

terminal conclusion:
HOLD

substantive blocker closure:
0 / 3
```

The report described its failure as a required-reading-order violation. PM intake corrected the root-cause classification: the Thread read unauthorized original T0/T0-R1/T0-R2 task contents that were outside its Section 7 content-read allowlist. The HOLD remains valid and immutable. It is procedural terminal evidence only and provides no substantive correction authority.

Do not reopen, overwrite, reinterpret as PASS or use this HOLD report as the controlling correction.

### 6.6 T0-R3-C1-R1 accepted fresh retry

Task:

```text
path:
docs/thread_handoff/pm_task_20260801T1016Z_d2_r7b_t0_r3_c1_r1_corrected_read_boundary_fresh_retry.md

bytes:
32727

SHA-256:
b4196fc6704ff75b2b77bee1bd5d902ae3c9c9c6d955812945bfdeffb539f557
```

Report:

```text
path:
docs/reports/sprint4_d2_r7b_t0_r3_c1_r1_corrected_read_boundary_fresh_retry.md

bytes:
22655

SHA-256:
e68d64f15969cd2f32609e968b6f731e1d20cc4f876e4bd1674375b758fc08bf

reported conclusion:
PASS WITH RECOMMENDATIONS

PM independent intake:
PM REVIEWED = YES
PM VERIFIED = YES
PM ACCEPTED = YES
```

T0-R3-C1-R1 is the controlling text for:

```text
PM-R3-001 CLOSED:
OpenSSH is modeled as one server-side remote command string. T1 freezes exactly one local argv element after destination, a deterministic POSIX single-quote serializer and explicit /bin/sh -c $0/$1…$N semantics. The accepted A0 archive FD remains direct SSH stdin and the sole archive-byte producer.

PM-R3-002 CLOSED:
Execution-lock and terminal hashes cover RFC 8785/JCS payloads that exclude their own digest fields. The predecessor lock raw hash is measured externally. The final terminal JSON raw hash remains external and is not embedded in itself. R0 stdout/stderr raw hashes are computed locally after SSH completion.

PM-R3-003 CLOSED:
Every normal or recovery authority consumes a PM/Owner-prebound literal attempt ID and resolves unique attempt-scoped report/evidence/temp/helper paths. Terminalized predecessor evidence is immutable and cannot be overwritten, reopened, aliased or reused.
```

No new PM blocker was found during PM intake.

## 7. Controlling planning precedence

The next PM must apply this precedence model:

```text
1. Original T0 report
   Base candidate/archive identity and W0→A0→R0→S0→T1→L0 phase model.

2. Repaired T0-R1 report
   Supersedes original T0 for B1–B6 command, workspace, publication and durable-path clauses.

3. T0-R3 report
   Supersedes T0/T0-R1 for the eight Reliability-blocking execution-lock, terminalization,
   freshness, ownership/reuse and failure-only recovery clauses.

4. T0-R3-C1-R1 report
   Supersedes conflicting T0-R3 clauses for SSH serialization, non-recursive digest projection
   and attempt-scoped durable paths.

5. T0-R2 report
   Reliability findings and review criteria only; not controlling planning text.

6. T0-R3-C1 HOLD report
   Procedural terminal evidence only; not controlling correction text.
```

No task or report grants automatic execution authority merely because it is controlling planning text.

## 8. Current accepted transport-planning contract

### 8.1 Happy-path Gate sequence

```text
W0  local transport workspace materialization
A0  local archive generation and acceptance
R0  zero-mutation remote target preflight
S0  remote staging workspace materialization
T1  archive transport and integrity acceptance
L0  remote Docker load and exact object identity acceptance
```

Every Gate requires a separately published PM/Owner authority. A PASS never automatically authorizes the next Gate.

### 8.2 Common execution-lock and terminal rules

For every future normal attempt:

- a literal PM/Owner-bound attempt ID is published before execution;
- attempt-specific report, evidence JSON, temporary JSON and helper paths are resolved to exact literals before task publication;
- all repository output paths must be absent and non-symlink at attempt entry;
- the Gate-specific execution lock is durably persisted before the first external call or filesystem/Docker mutation;
- helper bytes, argv, budgets and authority fields become immutable after lock;
- terminal evidence is atomically persisted after execution;
- terminal-evidence persistence failure is HOLD, never retry eligibility;
- terminalized attempt evidence is immutable predecessor evidence;
- no `latest`, mutable index, alias, symlink, convenience copy, overwrite, truncate, relink, delete or reopen is allowed.

Attempt ID grammar:

```text
normal   = d2-r7b-<gate>-a<NN>
recovery = d2-r7b-<gate>-rc-a<NN>
gate     = w0 | a0 | r0 | s0 | t1 | l0
NN       = 01 through 99
```

Runners must consume the literal attempt ID. They must not generate, increment, infer, default or select it.

### 8.3 SSH serialization and T1 producer

OpenSSH must not be modeled as preserving independent remote argv after destination.

For each future T1 SSH call:

- there is exactly one complete serialized remote-command string local argv element after destination;
- serializer is the frozen 7-bit-ASCII POSIX single-quote model from T0-R3-C1-R1;
- `/bin/sh -c` `$0` and `$1…$N` positions are explicit;
- serialized command bytes/SHA and complete local SSH argv are recorded in the execution lock;
- zero-network local serializer fixtures pass before lock;
- the accepted A0 archive FD is opened with no-follow/fstat/hash/seek checks and passed directly as SSH stdin;
- guard source is not sent through stdin;
- no shell pipeline, `/bin/cat`, SCP, rsync, SFTP or second archive producer is allowed;
- both T1 calls independently rebind stable host/root/staging identity before mutation/publication.

### 8.4 Evidence digest model

Future evidence envelope semantics:

```text
execution_lock_payload_canonical_sha256
= SHA-256 of RFC 8785/JCS canonical execution_lock_payload only

predecessor_document_raw_sha256
= externally measured SHA-256 of the complete predecessor lock document

terminal_payload_canonical_sha256
= SHA-256 of RFC 8785/JCS canonical terminal_payload only

complete final terminal JSON raw SHA-256
= external report/window/inventory identity; never embedded in that same JSON
```

R0 remote output does not self-report the hash of its complete stdout/stderr. The local runner computes raw output hashes after SSH completion.

### 8.5 Failure-only recovery categories

Only these conditional categories exist:

```text
W0-RC
A0-RC
S0-RC
T1-RC
L0-RC
```

They are not happy-path Gates and are not published by this handoff. A failed normal Gate cannot self-authorize recovery, reuse or cleanup. Recovery requires a new PM/Owner authority, a fresh recovery attempt ID, exact retained-object identities and bounded paths. Foreign or ambiguous objects remain untouched. Recovery cannot grant the failed Gate PASS; a later normal retry requires another fresh normal authority and another attempt root.

R0 remains zero mutation and currently has no external recovery category; a fresh R0 uses another normal attempt ID/root after new authority.

## 9. Reliability state and pending rereview

The initial focused Reliability review ended in HOLD with eight accepted blockers. Architecture corrections now claim textual closure through T0-R3 plus T0-R3-C1-R1.

Current review state:

```text
T0-R2 RELIABILITY HOLD ACCEPTED          = YES
T0-R3 CORRECTION WRITTEN                 = YES
T0-R3 STANDALONE PM ACCEPTED             = NO
T0-R3-C1 PROCEDURAL HOLD ACCEPTED        = YES
T0-R3-C1-R1 PM ACCEPTED                  = YES

RELIABILITY BLOCKERS TEXTUALLY ADDRESSED = YES
RELIABILITY REREVIEW COMPLETED           = NO
RELIABILITY BLOCKER COUNT AFTER REPAIR   = UNKNOWN UNTIL REREVIEW
VERIFICATION ELIGIBLE                    = NO
```

The next Reliability Thread must independently determine whether all eight `REL-R2-*` blockers and the three `PM-R3-*` corrections are coherent, executable, non-duplicative and sufficiently fail-closed under the precedence model.

It must not inherit Architecture PASS statements or PM acceptance as Reliability PASS.

Data Quality review remains unnecessary unless a future change introduces product-data semantics. Current work concerns execution reliability and transport evidence only.

## 10. Claims not established

Current accepted local image and planning evidence do not establish:

```text
LOCAL TRANSPORT WORKSPACE MATERIALIZED = NO
ARCHIVE CREATED                        = NO
ARCHIVE ACCEPTED                       = NO
REMOTE TARGET VERIFIED                 = NO
REMOTE STAGING WORKSPACE MATERIALIZED  = NO
TRANSPORTED                            = NO
REMOTE STAGED ARCHIVE ACCEPTED         = NO
REMOTE IMAGE LOADED                    = NO
REMOTE IMAGE ACCEPTED                  = NO
DEPLOYED                               = NO
ACTIVATED                              = NO
RUNTIME-LOADED VALIDATED               = NO
PRODUCTION ACCEPTED                    = NO
ROLLBACK ACCEPTED                      = NO
D2-R7B END-TO-END CLOSED               = NO
```

No local transport directory or remote target was inspected during the T0 planning/review/correction chain. No Python, Docker, archive, workspace, SSH, network, remote or lifecycle action was executed by those Gates.

## 11. Current authority and non-authorized surfaces

Current authority:

```text
NONE
```

Current states:

```text
LOCAL IMAGE ACCEPTED                  = YES
REBUILD REQUIRED                      = NO
T0-R3-C1-R1 PM ACCEPTED              = YES
TRANSPORT PLANNING FINAL ACCEPTED     = NO
FOCUSED RELIABILITY REREVIEW WRITTEN  = NO
VERIFICATION REVIEW WRITTEN           = NO
W0 AUTHORIZED                         = NO
```

Not authorized:

- writing a Reliability report without a newly published exact Reliability task;
- publishing Verification before Reliability `BLOCKER=0`;
- W0/A0/R0/S0/T1/L0 or any recovery category;
- Python execution or helper generation;
- Docker inspect/save/load/tag/remove/build/buildx/Compose actions;
- creation, reuse, cleanup or inspection of `/Users/chenjie/Documents/MES/edge-mes-transport` or its children;
- SSH, SCP, rsync, SFTP, remote filesystem access, remote Docker or remote service access;
- deployment, activation, restart, runtime validation, production-fact validation or rollback;
- editing status, roadmap, README, PM Rules, old tasks/reports/handoffs or product source;
- staging, committing, pushing, tagging, restoring, resetting, stashing or cleaning.

Every later action requires a new exact task with its own authority ID, attempt identity where relevant, content-read boundary, exact write/read allowlist, command/mutation budget, stop conditions and non-inheritance statement.

## 12. Single eligible next branch

The only eligible next technical branch is:

```text
Focused Reliability Rereview of Accepted Local-Image Transport Planning
```

Required review inputs should be narrowly limited to:

1. the new Reliability task itself;
2. PM Rules sections needed for Reliability review, execution lock, terminal evidence, recovery and no inheritance;
3. this handoff;
4. original T0 report;
5. repaired T0-R1 report;
6. T0-R2 Reliability report;
7. T0-R3 task and report;
8. T0-R3-C1-R1 task and report;
9. T0-R3-C1 HOLD report only if needed to preserve terminal lineage, not as substantive correction authority.

The new Reliability task should be docs-only and should allow exactly one new Reliability rereview report. It must not run Python, Docker, SSH, network or external filesystem operations and must not modify predecessor inputs.

Required review coverage:

- precedence consistency across T0, T0-R1, T0-R3 and T0-R3-C1-R1;
- all eight `REL-R2-*` findings;
- all three `PM-R3-*` findings;
- W0/A0/R0/S0/T1/L0 execution-lock and terminal ladders;
- failure-only recovery and immutable attempt evidence;
- OpenSSH one-string serialization and archive-FD producer separation;
- non-recursive digest projections;
- attempt-ID and attempt-path grammar;
- command/call/mutation budgets;
- foreign-object protection, no retry and no inheritance;
- MVP proportionality and absence of product-scope inflation.

Reliability verdict rules:

```text
PASS:
BLOCKER=0 and no material recommendation.

PASS WITH RECOMMENDATIONS:
BLOCKER=0 and recommendations are genuinely non-blocking.

HOLD:
any blocker, authority/read/write violation, incomplete review, conflicting contract,
false retry path, unsafe mutation path or unverifiable execution identity.
```

If Reliability `BLOCKER=0`, the next branch is focused Verification review. If any blocker remains, PM must publish the smallest Architecture / Integration correction instead. Do not skip directly to Verification or W0.

## 13. Recommended first read-only action for the next ChatGPT PM

The next PM should not continue from conversation memory alone. First:

1. open `/Users/chenjie/Documents/MES/edge-mes-demo` as the existing checkout;
2. read `docs/thread_handoff/pm_operating_rules.md` first;
3. read this handoff: `docs/thread_handoff/chatgpt_pm_handoff_260801-1852.md`;
4. run read-only recovery: branch, HEAD, origin/main, ahead/behind, `git status -sb`, tracked diff names, cached diff names and both diff checks;
5. verify PM Rules remains the sole tracked diff with bytes `56385` and SHA-256 `4de2fcc7d20a08c3bc33e18a7f2e94861e006a80bce1a76be3781547e6477528`;
6. verify the exact candidate and transport-chain task/report identities listed in this handoff without inspecting unrelated files;
7. confirm the new handoff itself is regular, non-symlink, untracked, unstaged, not indexed and not ignored;
8. report takeover state only: accepted local candidate, controlling planning precedence, T0-R3-C1-R1 PM acceptance, pending Reliability rereview, no Verification eligibility, no W0 authority and no active authority;
9. wait for Owner approval before publishing the focused Reliability rereview task, unless the Owner’s new-window prompt explicitly authorizes that exact publication.

Do not inspect Docker, external transport paths or remote state as part of takeover.

## 14. Copyable prompt for the next ChatGPT PM window

```text
你是 Edge MES Demo 项目的新任 ChatGPT PM。

项目绝对路径：

/Users/chenjie/Documents/MES/edge-mes-demo

首先按顺序执行只读接管：

1. 读取 docs/thread_handoff/pm_operating_rules.md；
2. 读取 docs/thread_handoff/chatgpt_pm_handoff_260801-1852.md；
3. 检查 live Git：branch、HEAD、origin/main、ahead/behind、git status -sb、tracked diff name-only、cached diff name-only、git diff --check、git diff --cached --check；
4. 核验 PM Rules 仍是唯一 tracked diff，bytes=56385，SHA-256=4de2fcc7d20a08c3bc33e18a7f2e94861e006a80bce1a76be3781547e6477528；
5. 只核验 handoff 中列出的 T0/T0-R1/T0-R2/T0-R3/T0-R3-C1/T0-R3-C1-R1 exact paths、bytes、SHA-256 和 Git membership；不要枚举或读取无关 untracked 内容；
6. 不运行 Python、Docker、SSH、网络、archive/workspace、deployment、activation、runtime、production、rollback 或 Git mutation。

预期 live baseline：

branch = main
HEAD = origin/main = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
ahead/behind = 0/0
tracked diff = docs/thread_handoff/pm_operating_rules.md only
cached diff = empty

Exact product source authority：

934ced7b9659cb566628b1709cf6d73463a534d8

Accepted local candidate：

sha256:8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013
linux/arm64
WorkingDir=/app
Cmd=["python","-m","app.main"]
ordered RootFS layers=9
LOCAL IMAGE ACCEPTED=YES
REBUILD REQUIRED=NO

Current controlling planning precedence：

original T0 report
→ repaired T0-R1 report for B1–B6
→ T0-R3 report for terminal/freshness/ownership/recovery/execution-lock clauses
→ T0-R3-C1-R1 report for SSH serialization/non-recursive digest/attempt-scoped path clauses

T0-R3-C1 initial report is terminal procedural HOLD only and is not substantive correction authority。

Current accepted review state：

T0-R2 Reliability HOLD accepted = YES
T0-R3-C1-R1 PM accepted = YES
focused Reliability rereview completed = NO
Verification eligible = NO
transport planning final accepted = NO
W0 authorized = NO
ACTIVE AUTHORITY = NONE

唯一 eligible next branch：

Focused Reliability Rereview of Accepted Local-Image Transport Planning

该 review 必须独立审查 8 个 REL-R2 blockers 与 3 个 PM-R3 corrections，且必须保持 docs-only、单报告输出、无 Python/Docker/SSH/network/archive/workspace/Git mutation。

完成接管后先报告 takeover state。除非本窗口的 Owner 指令明确批准发布 Reliability rereview task，否则不要自行发布任何 task，也不要进入 Verification 或 W0。
```

## 15. Handoff Git boundary

This handoff creates only:

```text
docs/thread_handoff/chatgpt_pm_handoff_260801-1852.md
```

It does not modify any existing file and does not stage itself.

Expected post-write state:

```text
new handoff:
untracked / unstaged / uncommitted / unpushed

cached diff:
empty

tracked diff:
docs/thread_handoff/pm_operating_rules.md only
```

No Git closeout is authorized by the Owner’s handoff instruction. Do not stage or commit this handoff automatically. Exact-path stage/commit/push requires a separate explicit Owner instruction.

If later authorized, the minimum stage allowlist is this exact handoff path only unless the Owner explicitly names additional paths. PM Rules must not be bundled by inference.

## 16. Thread context assessment

```text
current PM context length: long
current PM should continue: no
new PM window recommended: yes
context completeness for takeover: sufficient
active execution authority: none
```

The next PM has enough durable context to publish a focused Reliability rereview task after explicit Owner approval. No additional Architecture repair or status sync is required before that review.

## 17. Final handoff state

```text
HANDOFF WRITTEN                          = YES
HANDOFF STAGED                           = NO
HANDOFF COMMITTED                        = NO
HANDOFF PUSHED                           = NO

LOCAL IMAGE ACCEPTED                     = YES
REBUILD REQUIRED                         = NO
T0-R3-C1-R1 PM ACCEPTED                 = YES
RELIABILITY REREVIEW ELIGIBLE            = YES, after explicit task publication
RELIABILITY REREVIEW COMPLETED           = NO
VERIFICATION ELIGIBLE                    = NO
TRANSPORT PLANNING FINAL ACCEPTED        = NO
W0 AUTHORIZED                            = NO
ARCHIVE CREATED                          = NO
REMOTE ACCESSED                          = NO
ACTIVE AUTHORITY                         = NONE
```

The single recommended next action is a new docs-only focused Reliability rereview task, published only after Owner approval in the new PM window.
