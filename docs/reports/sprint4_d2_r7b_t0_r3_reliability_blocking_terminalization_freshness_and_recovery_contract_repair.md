# Sprint 4 D2-R7B T0-R3 Reliability-Blocking Terminalization, Freshness and Recovery Contract Repair

结论：PASS WITH RECOMMENDATIONS

## 1. 身份、范围与权限边界

- 报告名称：Sprint 4 D2-R7B T0-R3 Reliability-Blocking Terminalization, Freshness and Recovery Contract Repair
- 任务名称：D2-R7B-T0-R3 — Reliability-Blocking Terminalization, Freshness and Recovery Contract Repair
- Authority ID：PM-D2-R7B-T0-R3-RELIABILITY-BLOCKING-TERMINALIZATION-FRESHNESS-RECOVERY-CONTRACT-REPAIR-260801-1726
- 执行 Thread：Architecture / Integration
- delivery：REPOSITORY_DURABLE_REPORT
- exact report path：docs/reports/sprint4_d2_r7b_t0_r3_reliability_blocking_terminalization_freshness_and_recovery_contract_repair.md
- exact artifact paths：none
- Docs write authority：仅限上述 exact report；Git stage/commit/push/tag 未授权。

T0-R3 只修复 Reliability blocker 的 durable lock、terminalization、freshness、ownership/
reuse 和 recovery contract；所有 T0/T0-R1/T0-R1-C1/T0-R2 inputs、PM Rules、status、roadmap
及 handoff 不变。写入只建立 T0-R3 CORRECTION WRITTEN = YES，不建立 rereview、Verification、
PM acceptance、W0 或任何执行/runtime/production 状态。

## 2. Authority/input identity 与 fresh baseline

T0-R3 task file 已先读到 EOF，并核验：

| item | bytes | SHA-256 |
|---|---:|---|---|
| T0-R3 task | 29504 | 7ac5f7cae387692d8776f185f0bcc746d5c29fe851de562b32181e0c766fa2c6 |
| original T0 task | 27120 | 07aae9bded474e3b6d5942e0e6516aa13d9e70e8d3ceab3014692b39b1e0c2c3 |
| original T0 report | 24513 | 9e462dc30b5c4f92645a7f06cd79bb48ffe838072277c04ab962acba3091a77c |
| T0-R1 task | 31660 | 1b24958de2dc82af80a00996b90b2f8cbbc20d8817d5a603baf1e0aba81982e5 |
| repaired T0-R1 report | 23486 | 2ac3e90d50c6252a35cd2445a29615b0ca7c31cc7643cfdace657aa035d2a937 |
| T0-R1-C1 task | 21432 | a64c97de444801d00bb04aba1af77688e217b0f5bf76510656542f63b89e0777 |
| T0-R2 task | 24243 | 5674518ebbf5c24dccc0ac8b979c08295597b24213e481c7e7b2d68f66c770da |
| T0-R2 Reliability report | 20240 | 089b28fb82100ecadbf05f3fbf08a0ec5c4836e5cc2eb4fcbedd0faace2d5ec0 |
| PM Rules | 56385 | 4de2fcc7d20a08c3bc33e18a7f2e94861e006a80bce1a76be3781547e6477528 |

All listed files were regular, non-symlink, link=1; T0-R3 and every untracked input had one
exact ?? membership, was untracked/unstaged/not indexed/not ignored. PM Rules was the sole tracked
diff. The T0-R3 report was absent and non-symlink before write.

Fresh live baseline：

    repository   = /Users/chenjie/Documents/MES/edge-mes-demo
    branch       = main
    HEAD         = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
    origin/main  = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
    ahead/behind = 0/0
    tracked diff = docs/thread_handoff/pm_operating_rules.md only
    cached diff  = empty
    git diff --check = PASS
    git diff --cached --check = PASS
    T0-R3 report before write = ABSENT, non-symlink

Other dirty/untracked paths remain excluded. Candidate image, Docker daemon, archive/workspace and
remote target were not inspected. The window manifest supplies report SHA-256.

## 3. Precedence、retained contract 与 MVP

T0-R3 supersedes only the clauses needed to close
REL-R2-W0-001, REL-R2-S0-001, REL-R2-R0-001, REL-R2-R0-002, REL-R2-A0-001,
REL-R2-T1-001, REL-R2-L0-001 and REL-R2-X-001. The original T0 and T0-R1 reports remain
historical written evidence; T0-R3 is the controlling planning text for the conflicting
terminal, freshness, ownership/reuse, execution-lock, evidence-path and recovery clauses.

The following are retained and not redesigned：accepted candidate full-ID authority；ordered RootFS
validation；Docker image-save TAR and full-ID input；archive bytes/SHA deferred to A0；SSH option
terminator before destination；opened accepted-A0 FD as the sole T1 byte producer；W0/A0/R0/S0/T1/L0
phase separation；A0/T1 hard-link no-overwrite publication；deployment, activation, runtime and
rollback separation；PLC/HMI control authority with Edge read-only collection；and MVP claim
proportionality. T1's former bare direct dd form is superseded only by the same-call locked guard
below; dd remains the final remote byte writer and the opened accepted-A0 FD remains the source.

MVP 路径一致性：

- classification：MVP-ALIGNED
- product claim served：accepted local image to reliable, identity-bound archive/transport/remote-object planning
- product claim unchanged：yes
- scope drift：NO
- scope inflation：NO
- no registry, SBOM, signing, generic evidence framework, telemetry, HA, orchestration,
  audit/forensics or retention is introduced.

## 4. 八个 Reliability blocker closure matrix

All rows are contractually closed by durable text for focused rereview; this is static evidence,
not execution/runtime/remote proof.

| blocker | T0-R3 closure | exact contract section | durable-text closure verifiable |
|---|---|---|---|
| REL-R2-W0-001 | W0 ownership branches, pre-create lock, retained ladder, exact identity and no normal reuse after partial creation | 6 W0, 5, 8 | YES |
| REL-R2-S0-001 | S0 parent reuse/creation/child collision/foreign matrix and same-call rebind | 6 S0, 8 | YES |
| REL-R2-R0-001 | S0/T1/L0 rebind stable host and mutable root/staging identity in the consuming SSH call before mutation | 6 S0/T1/L0 | YES |
| REL-R2-R0-002 | One-record R0 schema, bounds, EOF, parser rejection and NOT_OBSERVED terminal | 6 R0 | YES |
| REL-R2-A0-001 | Post-save/post-link/post-unlink state ladder; archive remains unaccepted until final-only proof and durable terminal JSON | 6 A0 | YES |
| REL-R2-T1-001 | Guarded stream, two-call outcomes, retained remote states and publication-complete-but-unobserved HOLD | 6 T1 | YES |
| REL-R2-L0-001 | Pre-load/load/post-load ladder, full-ID equality and LOAD_STATE_UNCERTAIN no-retry boundary | 6 L0 | YES |
| REL-R2-X-001 | Per-Gate immutable execution_lock, same-directory atomic JSON replacement and terminal-write failure HOLD | 5, 8 | YES |

Each row has a precondition, mutation boundary, terminal state, retained-object rule and next-Gate
prohibition; none is merely acknowledged.

## 5. Common durable execution-lock and terminal-evidence contract

Each future Gate uses its own bounded JSON in Section 8; there is no shared library, service,
database or generic framework. Before its first external call or filesystem/Docker mutation, it
must fsync an exact same-directory temporary JSON, atomically install the final path and fsync the
parent. These are future paths, not T0-R3 artifacts.

The immutable execution_lock must contain：schema version/Gate；authority ID/unique attempt ID；
exact input task/report identities；pre-task live facts；helper/script/runner paths, bytes and
SHA-256；exact argv/positional args, masked target identity and environment assumptions；budgets；
expected path/object pre-state；local validation and repair-cycle count；authority_consumed=false；
terminal_state=PENDING_EXTERNAL_AUTHORITY；lock timestamp；canonical/raw JSON SHA-256.

After persistence, helper/script/runner bytes and authority-bearing fields are immutable. Any local
failure is HOLD; no repair, retry, budget increase or argv change. After execution, the same
task-owned JSON is atomically replaced with the unchanged lock plus terminal. If replacement fails,
the pre-mutation lock remains evidence that authority may have been consumed and the Gate is
HOLD / TERMINAL_EVIDENCE_NOT_PERSISTED; later Gates and retry are forbidden and a separate
reconciliation authority is required. Markdown is secondary; its write failure cannot weaken JSON
terminal evidence.

Every terminal object records authority/call/mutation counts；exit/timeout/parser/report-write
outcomes；observability=COMPLETE, PARTIAL or NOT_OBSERVED；retained identities or UNKNOWN；
terminal_state/reason；claims established/not established；recovery；next Gate or NONE；timestamp；
and terminal JSON SHA-256. A future Gate may report PASS only after durable terminal JSON.

## 6. Corrected Gate contracts

### W0 — local transport workspace materialization

W0 is local workspace materialization only. Persist the lock before the first create; create one
component at a time, never mkdir -p. Entry matrix：

1. base /Users/chenjie/Documents/MES/edge-mes-transport absent and task workspace absent:
   create base, prove it, then create and prove task workspace;
2. base safely pre-exists as regular, non-symlink, link=1, authorized-user-owned, mode 0700,
   searchable/writable and on the expected filesystem, while task workspace is absent: reuse base
   without mutation and create only task workspace;
3. task workspace pre-exists: normal W0 HOLD regardless of contents;
4. base unsafe, foreign, ambiguous or mismatched: HOLD with zero mutation.

After each create, record path, attempt, device, inode, owner, mode, link, empty and mutation
count in terminal JSON. Ladder：precondition before mutation = W0 HOLD / NO_MUTATION；base created
but task unproven = W0 HOLD / RETAINED_RECOVERY_REQUIRED；task created but proof, JSON or report
fails = W0 HOLD / RETAINED_RECOVERY_REQUIRED or TERMINAL_EVIDENCE_NOT_PERSISTED；PASS requires
both identities, empty workspace and durable JSON. No A0 follows W0 HOLD.

### A0 — local archive generation and acceptance

Retain one full-ID Docker image-save TAR plus original manifest/Config/ordered RootFS/layer
validation. Measure archive bytes/SHA only in A0; persist the lock before the one exact save.
Retain macOS os.link(temp, final, follow_symlinks=False), fsync and no-overwrite proof, distinct
from JSON evidence replacement.

| boundary | required terminal state |
|---|---|
| save not invoked or precondition failure | A0 HOLD / NO_MUTATION |
| temp exists but validation incomplete/failed | A0 HOLD / RETAINED_RECOVERY_REQUIRED; bytes/SHA may be NOT_OBSERVED |
| temp validated, final absent, link not attempted | A0 HOLD / RETAINED_RECOVERY_REQUIRED |
| link failed and final absent | A0 HOLD / RETAINED_RECOVERY_REQUIRED |
| link succeeded, temp+final same device/inode, link=2, pre-unlink proof incomplete | A0 HOLD / RETAINED_RECOVERY_REQUIRED |
| pre-unlink proof complete but exact temp unlink unobserved | A0 HOLD / RETAINED_RECOVERY_REQUIRED |
| final-only exists after unlink but parent fsync/final proof/JSON/report incomplete | A0 HOLD / RETAINED_RECOVERY_REQUIRED |
| final-only archive bytes/SHA/mode/link=1, parent durability and terminal JSON fully proven | ARCHIVE ACCEPTED may be YES; A0 PASS |

Until the final row is durable, ARCHIVE ACCEPTED remains NO. Record both paths, identities, links
and known bytes/SHA or NOT_OBSERVED. Post-save/link uncertainty forbids retry, reuse, removal and
R0; only A0-RC may reconcile exact task-owned objects.

### R0 — one zero-mutation remote preflight

R0 is exactly one SSH call and zero mutation. Its result is one UTF-8 JSON object plus one newline,
clean EOF and no extra bytes; stdout <=65536 bytes and stderr <=16384 bytes. Required schema fields
include schema_version, complete=true,
host-key source, hostname, machine-id/stable identity, kernel, architecture, current user, Docker
client/server/daemon, deployment root and staging-parent identities, permissions/owner/device/free
bytes/required-space calculation, temp/final absence or collision, required executable identities,
current Collector identity and ambiguity result, raw stdout/stderr byte counts and SHA-256, and
normalized-record SHA-256.

Reject missing/unknown fields, duplicate keys, malformed UTF-8/JSON, wrong types, overflow,
truncation, extra records/bytes, nonzero/timeout/parser exception. No stale merge or predecessor
reuse. Any incomplete result is R0 HOLD / NOT_OBSERVED; REMOTE TARGET VERIFIED = NO; next Gate =
NONE. R0 PASS is eligibility only, not a lease.

### S0 — remote staging workspace materialization

S0 consumes R0 evidence but rebinds current stable host and /opt/edge-mes-demo plus .transport
parent identity/owner/mode/device in the same SSH call before mutation. Drift/ambiguity is HOLD
with zero mutation.

Entry matrix：

1. .transport safely pre-exists with exact R0-bound identity and task child is absent: reuse
   parent without creation and create only the task child;
2. .transport absent and task child absent: create parent, prove it, then create and prove task child;
3. task child pre-exists: normal S0 HOLD;
4. parent identity/mode/owner/device differs or ownership is ambiguous: HOLD with zero mutation.

The persisted /bin/sh -s -- script receives positional args with -- before destination, rebinds
before mkdir, uses one component at a time, immediate 0700, no mkdir -p/delete/chown/sudo/repair.
Partial creation or proof/JSON failure records exact identity and S0 HOLD /
RETAINED_RECOVERY_REQUIRED. Normal S0 cannot infer prior ownership or follow with T1.

### T1 — same-connection guarded transport and publication

The opened accepted-A0 final archive FD remains the sole byte producer. The runner uses
O_RDONLY | O_NOFOLLOW, fstat regular/link/device/inode/mode/bytes, hashes/seeks that FD and passes
it directly as stdin to shell-free subprocess.run; no cat, pipeline, SCP, rsync or SFTP.

The former bare remote dd is superseded by repository-persisted remote_stream_guard.sh. The local
runner passes its exact bytes as one argv element to:

    /usr/bin/ssh <frozen-options> -- <verified-target> /bin/sh -c <exact-script-text>
      d2-r7b-t1 <expected-machine-id>
      <expected-deployment-root-device/inode>
      <expected-staging-parent-device/inode/owner/mode>
      <exact-remote-temp-path>

The guard uses positional args, rebinds stable host/deployment-root/staging-parent and temp/final
absence in this connection, then execs /bin/dd of=<exact-temp> bs=1048576 conv=excl status=none.
No mutation precedes comparison. The second SSH uses remote_verify_publish.sh and independently
rebinds host/root/staging-parent before verify/link/publish/recheck. T1 has exactly two SSH calls.

Terminal ladder：FD open/fstat/hash/seek failure before SSH = T1 HOLD / NO_REMOTE_MUTATION；guard
rejection before dd = HOLD / NO_REMOTE_MUTATION；stream timeout/nonzero/disconnect with remote
outcome incomplete = HOLD / NOT_OBSERVED；temp-only observed or possibly created =
HOLD / RETAINED_RECOVERY_REQUIRED；temp+final link=2 or publication uncertain =
HOLD / RETAINED_RECOVERY_REQUIRED；final-only may exist but second call/response/terminal JSON
incomplete = HOLD / PUBLICATION_COMPLETE_BUT_NOT_OBSERVED；PASS requires final-only bytes/SHA/
device/inode/link/mode and both call outcomes completely observed with durable terminal JSON.
Any uncertainty blocks L0 and retry; only T1-RC may reconcile exact task-owned paths.

### L0 — same-call fresh remote load and exact object acceptance

L0 consumes only accepted T1 final archive. Its one SSH script rebinds host, deployment/staging
parent and exact archive path/bytes/SHA immediately before pre-load inspect/load; it records
complete pre-state, loads only after proven full-ID absence and records complete post-state.

Terminal ladder：precondition or pre-inspect failure before load = L0 HOLD / NO_DOCKER_MUTATION；
exact image pre-exists = L0 HOLD / EXPLICIT_REUSE_AUTHORITY_REQUIRED；load not proven invoked or
remote outcome uncertain = L0 HOLD / LOAD_STATE_UNCERTAIN；load invoked but post-state, SSH,
parser, terminal JSON or report is incomplete = L0 HOLD / LOAD_STATE_UNCERTAIN；complete post-state
mismatch = L0 HOLD / REMOTE_IMAGE_IDENTITY_MISMATCH；PASS requires full immutable image ID,
linux/arm64, Config, WorkingDir, Cmd and ordered RootFS equality plus durable terminal JSON.
Post-load uncertainty prohibits retry, second load, tag, remove, cleanup and C0 entry; only L0-RC
may reconcile the exact full-ID/object state. Retention is not acceptance.

Claims remain separated：W0/S0 workspace；A0 archive；R0 eligibility；T1 staged transport；L0
remote image；C0 read-only；D0 no activation；B0 before A1；A1 separate from R1；P0 separate
from runtime-loaded validation；B1 real rollback acceptance；C1 needs status sync and PM acceptance.
No Gate authorizes the next. PLC/HMI controls; Edge only collects read-only.

## 7. Failure-only recovery categories

Recovery is failure-only, absent from the happy path, unpublished by T0-R3 and never
self-authorized by a failed normal Gate：

| category | retained-state scope | boundary |
|---|---|---|
| W0-RC | exact local base/task identities | new PM/Owner authority, fresh attempt, bounded identity reads and exact reuse/cleanup decision |
| A0-RC | exact local temp/final archive identities | new authority; reconcile/cleanup only proven task-owned objects |
| S0-RC | exact remote parent/child identities | new authority and fresh remote identity binding; foreign/ambiguous objects untouched |
| T1-RC | exact remote temp/final inode/device/link states | new authority, bounded remote reconciliation; cannot infer transport acceptance |
| L0-RC | exact full-ID/image-object state | new authority, exact reconciliation/cleanup; cannot grant image PASS |

Each requires exact retained identities, bounded paths and a fresh attempt ID. Foreign/ambiguous
objects remain untouched; recovery cannot grant failed-Gate PASS or jump to the happy path. A new
normal Gate authority is required. This report grants none and grants no retry, reuse or cleanup.

## 8. Exact durable paths and future Gate allowlists

The following paths are frozen for future independent Gate Prompts only. T0-R3 creates none of
them. Each JSON temporary path is same-directory and is used only for atomic lock/terminal
replacement before parent fsync.

| Gate | report; JSON final; JSON temporary; helper/script/runner | exact reads/writes, budget and next Gate |
|---|---|---|
| W0 | docs/reports/sprint4_d2_r7b_w0_local_transport_workspace_materialization.md; docs/reports/evidence/d2_r7b_w0_local_transport_workspace_materialization/01_workspace_materialization.json; docs/reports/evidence/d2_r7b_w0_local_transport_workspace_materialization/01_workspace_materialization.json.tmp; docs/reports/evidence/d2_r7b_w0_local_transport_workspace_materialization/workspace_materializer.py | Read exact local ancestors and frozen runtime; write only external base/task dirs plus these declared repo paths; max two directory creates, no archive/Docker/network; next A0 only after new authority; forbidden reuse of unsafe/retained/foreign dirs, mkdir -p and Git mutation. |
| A0 | docs/reports/sprint4_d2_r7b_a0_local_archive_generation_and_acceptance.md; docs/reports/evidence/d2_r7b_a0_local_archive_generation_and_acceptance/01_archive_acceptance.json; docs/reports/evidence/d2_r7b_a0_local_archive_generation_and_acceptance/01_archive_acceptance.json.tmp; docs/reports/evidence/d2_r7b_a0_local_archive_generation_and_acceptance/archive_validator.py | Read W0 identity, exact external parent/temp/final and accepted full-ID; one docker image save, one hard-link publication; write only declared temp/final/repo paths; no remote, tag, overwrite, fallback or broad cleanup; next R0 only after new authority. |
| R0 | docs/reports/sprint4_d2_r7b_r0_remote_target_readonly_preflight.md; docs/reports/evidence/d2_r7b_r0_remote_target_readonly_preflight/01_remote_preflight.json; docs/reports/evidence/d2_r7b_r0_remote_target_readonly_preflight/01_remote_preflight.json.tmp; docs/reports/evidence/d2_r7b_r0_remote_target_readonly_preflight/remote_probe.sh; docs/reports/evidence/d2_r7b_r0_remote_target_readonly_preflight/remote_preflight_runner.py | Read owner-bound SSH config/known-hosts and exact remote root/staging/tool/Docker/Collector state; exactly one zero-mutation SSH; write only declared repo evidence; no mkdir/upload/load/tag/restart/cleanup; next S0 only after new authority. |
| S0 | docs/reports/sprint4_d2_r7b_s0_remote_staging_workspace_materialization.md; docs/reports/evidence/d2_r7b_s0_remote_staging_workspace_materialization/01_remote_workspace_materialization.json; docs/reports/evidence/d2_r7b_s0_remote_staging_workspace_materialization/01_remote_workspace_materialization.json.tmp; docs/reports/evidence/d2_r7b_s0_remote_staging_workspace_materialization/remote_workspace_materializer.sh; docs/reports/evidence/d2_r7b_s0_remote_staging_workspace_materialization/remote_workspace_materialization_runner.py | Same-call reads/rebinds host/root/.transport; write only eligible .transport and task child, max two creates, one SSH; no archive/Docker/service/config/lifecycle; next T1 only after new authority. |
| T1 | docs/reports/sprint4_d2_r7b_t1_archive_transport_and_integrity_acceptance.md; docs/reports/evidence/d2_r7b_t1_archive_transport_and_integrity_acceptance/01_transport_acceptance.json; docs/reports/evidence/d2_r7b_t1_archive_transport_and_integrity_acceptance/01_transport_acceptance.json.tmp; docs/reports/evidence/d2_r7b_t1_archive_transport_and_integrity_acceptance/transport_runner.py; docs/reports/evidence/d2_r7b_t1_archive_transport_and_integrity_acceptance/remote_stream_guard.sh; docs/reports/evidence/d2_r7b_t1_archive_transport_and_integrity_acceptance/remote_verify_publish.sh | Read accepted A0 FD and R0/S0-bound exact paths; exactly two SSH calls, guarded stream then verify/publish/recheck; write only exact remote temp/final and declared repo evidence; no active deployment/Docker/retry/foreign cleanup; next L0 only after new authority. |
| L0 | docs/reports/sprint4_d2_r7b_l0_remote_docker_load_and_exact_object_identity_acceptance.md; docs/reports/evidence/d2_r7b_l0_remote_docker_load_and_exact_object_identity_acceptance/01_remote_load_acceptance.json; docs/reports/evidence/d2_r7b_l0_remote_docker_load_and_exact_object_identity_acceptance/01_remote_load_acceptance.json.tmp; docs/reports/evidence/d2_r7b_l0_remote_docker_load_and_exact_object_identity_acceptance/remote_load_probe.sh; docs/reports/evidence/d2_r7b_l0_remote_docker_load_and_exact_object_identity_acceptance/remote_load_runner.py | Same-call reads/rebinds host/root/staging and exact accepted archive; one SSH and one docker image load only after proven full-ID absence; write only the exact load-created Docker object and declared repo evidence; no tag/remove/Compose/restart/cleanup; next C0 only after new authority. |

Every future allowlist freezes lock-before-call, exact args, reads/writes, budgets, terminal ladder,
recovery, next Gate and forbidden surfaces. The table authorizes none.

## 9. Review sequence、validation boundary 与 counters

Single next Gate：

    PM Independent Intake — D2-R7B-T0-R3 Reliability-Blocking Terminalization, Freshness and Recovery Contract Repair

After PM intake, only if independent Reliability rereview has zero blockers：

    focused Reliability rereview of original T0 + repaired T0-R1 + T0-R3
    -> focused Verification review
    -> PM final transport-planning acceptance
    -> Owner authorization of W0

T0-R3 authorizes none of W0/A0/R0/S0/T1/L0, recovery, Python, Docker, archive/workspace,
SSH/network/remote, deployment, activation, runtime, production, rollback or Git.

Action counters for this Architecture / Integration Gate：

    Python executed                         = 0 / NO
    Docker action                           = 0 / NO
    Archive/workspace mutation              = 0 / NO
    SSH/network/remote                      = 0 / NO
    Deployment/activation/runtime/rollback  = 0 / NO
    Git stage/commit/push/tag/reset/restore  = 0 / NO
    Task-owned report create                = 1
    Other files created or modified         = 0

Final validation requires regular/non-symlink exact path；bytes <=24576, hard maximum <=32768；
two matching terminal fields, no provisional wording, eight IDs, B1-B6 retention, paths, guard,
lock, R0 schema and recovery；this report only changed；cached empty；diff checks and frozen
identities pass. No prohibited command or mutation is needed.

Blockers：none for the T0-R3 planning correction; PM/Reliability acceptance remains a later state.
Recommendations：PM independent intake, then the focused Reliability rereview; Verification only
after Reliability blocker count is zero.

## 10. Final conclusion

T0-R3 closes all eight accepted Reliability blockers as explicit planning-contract corrections,
keeps the product claim and MVP path unchanged, and leaves all execution and later-phase authority
separate. The report is written only at the exact authorized path. It establishes no execution,
runtime, deployment, production or Git state.

结论：PASS WITH RECOMMENDATIONS
