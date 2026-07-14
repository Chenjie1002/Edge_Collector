# Sprint 3 Dashboard production URL-resolution runtime evidence capture STARTING signal cleanup focused HOLD repair round 7 report

> **SUPERSEDED FOR EXECUTION — 2026-07-14 PM SCOPE RESET**
>
> 本文件保留为历史 planning/review lineage。Section 14 及其 private-parent、manifest、
> 57/76-field retained-record protocol 不再是当前可执行 authority，不得运行或继续按
> D7/D8 完整关系闭包扩展。当前目标、blocker 规则、执行边界和验收条件以
> `docs/reports/sprint3_dashboard_production_url_resolution_scope_reset_design.md`
> 为准。任何恢复旧 assurance target 的动作都需要新的 PM 明确授权。

报告名称：Sprint 3 Dashboard production URL-resolution runtime evidence capture STARTING signal cleanup focused HOLD repair round 7 report

任务名称：Repair capture STARTING-to-TERMINATING transition and ensure signal state-write failure cannot block process cleanup

执行 Thread：Architecture / Integration

结论：**PASS WITH RECOMMENDATIONS**

## 1. Authority、范围与继承状态

本文件是未来、一次性的 local runtime-evidence runbook；本次只修复 planning authority，
没有执行其中任何命令。它不授权 runtime execution、build、tests、typecheck、Next、capture、
curl/browser、lsof、端口绑定、API/DB/Docker、任何 review、deployment/config 或 Git write。

唯一可修改路径为本文件。Reliability review report 保持原样；该 review 的 HOLD 是本次
repair 的直接 authority，而不是本次已完成的 re-review。下列状态不因本文件而关闭：

```text
Architecture runtime-evidence planning: Round-7 signal-cleanup repair; PASS WITH RECOMMENDATIONS
Focused Reliability round 4: HOLD, preserved; this report is not a Reliability re-review
Data Quality planning review: HOLD, preserved; this repair does not close the Data Quality gate
Verification planning review: NOT AUTHORIZED
runtime execution: NOT AUTHORIZED
VER-URL-V3: OPEN
DQ-URL-D2: HOLD / pending Data Quality re-review
DQ-URL-D3: CARRY FORWARD
REL-URL-R6: CARRY FORWARD
same-origin no-DB mock capability: independent HOLD
Global Gate: HOLD
Real production-fact evidence: NOT EXECUTED / NOT CLAIMED
```

PM intake findings for this round:

```text
PM-RUNTIME-R6-1: SIGTERM during capture STARTING cannot reach reliable TERMINATING/TERMINATED cleanup.
PM-RUNTIME-R6-2: TERMINATING state-write failure currently returns before best-effort server close/process exit.
```

Authority precedence remains: live Git → latest PM handoff → focused Reliability round 4 HOLD
→ Round-5 planning authority → Data Quality HOLD report → prior Reliability lineage → prior URL
authority/reviews → `docs/current_status.md`.

## 2. Frozen evidence boundary

The future run is local-only transport and synthetic strict-contract evidence. It fixes the
ports and topology below and preserves the existing implementation boundary: `page.tsx`
validates the query and trusted origin before `fetchAcceptedStationEvents`; the client issues
one absolute `GET /api/v2/production/accepted-station-events`; the parser remains strict.

| Item | Frozen value |
| --- | --- |
| capture listener | `127.0.0.1:3100` |
| Next listener | `127.0.0.1:3101` |
| private parent | pre-created `/tmp/edge-mes-dashboard-url-runtime-evidence-runs`, current UID, exact mode `0700`, marker-bound |
| physical evidence root | retained `run-<64-lowercase-hex nonce>` child under the verified private parent |
| logical evidence mapping | per-run `run-<nonce>.manifest.json`; no fixed-root symlink pointer |
| capture implementation | inline Node standard library only |
| build | one fresh build; same artifact; six `BUILD_ID`/`server.js` SHA-256 checkpoints |
| phases | A: active capture and zero target requests; B: new Next PID and exactly one target request |
| query | exact five name/value pairs, including opaque cursor forwarding |
| fixture | strict 22-key synthetic item |
| shutdown | TERM only; ten one-second checks; no KILL |
| final proof | dual-port release, A/B/C evidence classification plus D filesystem-boundary statement |

It must not claim production DNS, TLS, egress, deployment readiness, real API, DB-backed
facts, or real production facts.

## 3. One canonical lifecycle and control-flow contract

Section 14 is the **only executable authority**. Sections 1--13 intentionally contain no
copyable future-run command sequence. Any illustrative text in these sections is a
**non-executable explanatory excerpt** and has no independent lifecycle meaning.

The canonical lifecycle is:

```text
define helpers and common failure dispatcher
install INT/TERM/HUP traps before root/process creation
→ runtime_evidence_main
  → preflight/root/fixture/state/capture candidate
  → build and six artifact-identity checkpoints
  → Phase A, independent cleanup of A
  → Phase B, independent cleanup of B
  → capture cleanup, final ports, terminal evidence
→ top-level five-phase success finalization OR common failure dispatcher
→ final exit
```

`runtime_evidence_main` never uses ordinary `exit`; every ordinary failure records a stable
code/reason through `runtime_hold` and returns nonzero to the top-level dispatcher. The only
ordinary nonzero `exit` is after `runtime_common_failure_dispatch` completes. A signal handler
may exit only after that same dispatcher completes. No operator may manually append a failure
block; no second direct-exit sequence exists.

## 4. Process lifecycle and ownership model

Each role (`capture`, `phase_a_next`, `phase_b_next`) has this lifecycle:

```text
NOT_STARTED → LAUNCHED_CANDIDATE → IDENTITY_CAPTURED → LISTENER_VERIFIED → READY
→ STOPPING → STOPPED → REAPED
                    ↘ UNRESOLVED
```

Immediately after every background launch, the control shell stores `$!`, role, its own PID,
the current run nonce, the monotonically increasing role launch generation, the exact role
marker carried as the final child argv token, and `LAUNCHED_CANDIDATE`. These current-shell
variables are **candidate cleanup
identity** and are recorded before identity collection, evidence append, PID-file writes,
readiness/listener checks, or requests. `process-identities.txt` and per-role PID files are
audit evidence only; neither is a candidate-cleanup prerequisite.

There are two non-interchangeable identities. **Candidate cleanup identity** is permitted only
before a complete snapshot and before that role has entered a request phase; it requires the
original `$!`, the original control-shell PPID, the current role launch generation, the current
run nonce, a recomputed marker equal to the stored marker, and the role-specific command
structure with the marker as the exact final argv token. **Fully verified runtime identity** is the `/bin/ps -ww -p
<pid>` snapshot using `pid=`, `ppid=`, `lstart=`, and `command=`; its digest covers those exact
observations. A PID alone, marker substring, listener, or PID file is never authority.

Immediately before TERM, cleanup uses fully verified identity when it exists; otherwise it may
use the bounded candidate identity described above. PID evidence files are never read as a TERM
precondition. An absent exact child is reaped with `wait <exact PID>` and its actual wait status
is recorded; `127` is always `WAIT_NOT_CHILD` / `WAIT_FAILURE`, never success. Every successful
TERM or already-exited child is waited by the original control shell exactly once; `reaped=yes`
freezes the outcome and prevents a duplicate signal/wait.

## 5. Listener evidence is separate from process ownership

`/usr/sbin/lsof -nP` is evidence for expected listener state, never an authority to select a
TERM target. `record_listener_state` returns only through current-shell
`listener_state_result` and `listener_evidence_write_result`: `PRESENT`, `ABSENT`, or
`LSOF_FAILURE` are valid only when the evidence append succeeds; any append failure is
`EVIDENCE_WRITE_FAILURE`. Runtime phases HOLD on that failure. Cleanup records it as final HOLD
evidence but still TERM's a separately confirmed owned process. It never kills by port and
never kills an unknown listener. An identity mismatch with a busy port is `unknown-listener
HOLD` while cleanup safely continues for the other roles.

## 6. Common cleanup and result aggregation

The common failure dispatcher always attempts, in this order: Phase B Next, Phase A Next,
capture, Next-port release proof, capture-port release proof. It never uses `cleanup || exit`,
and a TERM failure, timeout, wait failure, listener loss, or identity mismatch for one role
does not prevent the next attempt. It retains the exact evidence root and every build artifact.

`cleanup_role` is always invoked in the current control shell. It returns its result only in
`cleanup_role_result`; callers assign that global after checking the function return. No
pipeline, subshell, or command substitution invokes it. Each role returns one of:
`NOT_STARTED`, `ALREADY_EXITED`, `TERM_SENT_AND_EXITED`, `TERM_TIMEOUT`,
`IDENTITY_UNRESOLVED`, `WAIT_NOT_CHILD`, `WAIT_FAILURE`, `LISTENER_LOST_BUT_TERMINATED`, or
`UNRESOLVED`. The dispatcher writes all role and port results to `failure-state.txt`, prints
them, and returns `HOLD` after every safe attempt.

## 7. Artifact ownership, concurrency model and symlink boundary

### 7.1 Declared filesystem concurrency model

The task-owned artifact safety model is intentionally narrower than host-level security. Within
the declared model, the canonical lifecycle is the only authorized writer for these exact
generated source paths and their fixed quarantine paths:

```text
frontend/.next
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
frontend/.edge-mes-runtime-evidence-next.quarantine
frontend/.edge-mes-runtime-evidence-next-env.quarantine
frontend/.edge-mes-runtime-evidence-tsbuildinfo.quarantine
```

The same canonical lifecycle does not retry, relaunch or start a second cleanup actor. The
evidence root provides one-run isolation. Any external filesystem drift discovered at a task
command boundary is a `HOLD`; the task neither guesses recovery nor continues deletion. No path
may be deleted unless it has passed the task-owned identity handoff recorded for that artifact.
An ownership or quarantine mismatch is retained as evidence; the task never guesses a restore
or deletes the mismatched object.

The frozen filesystem threat boundary is explicit:

```text
DEFENDS:
T1 — accidental filesystem drift
T2 — other-user interference within sticky-directory, current-UID ownership,
     exact 0700 private-parent/root modes and non-privileged assumptions
T3 — same-UID non-malicious concurrency

DOES NOT CLAIM:
T4 — deliberate same-UID adversarial races between pathname operations
T5 — privileged/root filesystem or process manipulation
```

The authority makes no atomic mkdir-and-open claim and no kernel-enforced sandbox claim. The
private parent and unpredictable per-run basename materially isolate stale artifacts, different
UIDs and accidental concurrent runs, but they are not represented as a defense against a same-UID
actor deliberately racing every lookup. Observed drift is `HOLD`; uncertain objects are retained
and never guessed, adopted, repaired or deleted.

### 7.2 Exact generated-path ownership

Before any future run, the separately prepared private parent must already exist as a non-symlink
Directory owned by the current effective UID with exact mode `0700`, logical/canonical same-object
identity, and an exact `.edge-mes-private-parent-authority.json` marker. Section 14 never creates,
repairs, chmods, empties or deletes that parent. Parent absence or any metadata/marker mismatch is
`HOLD` pending an independent workspace-preparation gate.

For the current run only, the derived `run-<nonce>` root basename, matching manifest and manifest
tmp must each be absent and non-link before exclusive creation/publication. Existing roots or
manifests from other nonces are retained immutable audit evidence and do not block a new run. The
legacy `/tmp/edge-mes-dashboard-url-runtime-evidence` root is outside this namespace, is never
adopted or modified, and does not block Option C root creation. `.next`, `next-env.d.ts`,
`tsconfig.tsbuildinfo` and all three fixed quarantine paths retain their existing absent/non-link
preflight.

Before build, `artifact-prestate.txt` records all three generated source paths and all three
quarantine paths as absent/not-link. A successful build classifies each source path as
`CREATED_REGULAR_FILE`, `CREATED_DIRECTORY`, `NOT_CREATED`, or `TYPE_OR_LINK_MISMATCH`. `.next`
must be `CREATED_DIRECTORY`; the two auxiliary paths may be `NOT_CREATED`. For every created
artifact, the canonical macOS identity command is:

```zsh
/usr/bin/stat -f 'device=%d%ninode=%i%ntype=%HT%nsymlink_target=%Y' -- "$artifact_path"
```

`artifact-ownership.txt` records `path`, `classification`, `device`, `inode`, `type`,
`symlink_status` and `record_stage`. Created `.next` records directory type, not-link status and
the exact device/inode; a created auxiliary records regular-file type, not-link status and the
exact device/inode. A `NOT_CREATED` auxiliary records `classification=NOT_CREATED`,
`device=absent`, `inode=absent`, `type=absent`, `symlink_status=not-link`; it never fabricates
an inode identity. A nonzero build or any abnormal classification retains all partial artifacts
and never enters success cleanup.

`runtime_success_finalize` has five explicit phases: Phase 1 validates source state and the
recorded identity; Phase 2 atomically renames each created source into its fixed same-parent
quarantine path; Phase 3 verifies source absence and quarantine identity; Phase 4 deletes only
verified quarantine objects; Phase 5 proves all six source/quarantine paths are absent and not
links. Success deletion removes no source path directly. A mid-handoff, pre-delete or deletion
failure stops further success deletion, retains every existing source/quarantine artifact and
follows the common failure result.

## 8. Capture state and evidence commit model

Exact root artifacts are:

```text
.root-ownership.json
fixture.json
fixture-identity.json
fixture-identity.tmp
capture-response-evidence.json
capture-response-evidence.tmp
capture-state.json
capture-state.tmp
capture-ready.txt
capture.log
capture-requests.jsonl
process-identities.txt
artifact-prestate.txt
artifact-ownership.txt
build-identity.txt
failure-state.txt
evidence-summary.txt
next-phase-a.pid
next-phase-b.pid
capture.pid
phase-a-next.log
phase-b-next.log
phase-a-page.headers
phase-a-page.html
phase-b-page.headers
phase-b-page.html
```

The three fixed quarantine paths are task-created temporary artifacts in the same `frontend`
parent directory as their source paths, so each source-to-quarantine handoff is an atomic
same-filesystem rename. They are never wildcarded, dynamically named, overwritten or restored
by guessing. `failure-state.txt` retains source and quarantine states, handoff stage, ownership
verification, deletion stage and final postcondition result; the failure dispatcher never
deletes a quarantine.

The private parent additionally contains one per-run mapping file outside the physical root:

```text
run-<nonce>.manifest.json
.run-<nonce>.manifest.json.tmp
```

The manifest exact schema binds the logical evidence identity, nonce, logical/canonical physical
root paths, root device/inode/type, start timestamp, gate purpose, expected/final state, threat
boundary, non-claims, creation model, cleanup state and legacy-root disposition. Publication uses
one `wx` tmp, checked full write, fsync, close and atomic rename. The allowed lifecycle is
`NOT_PUBLISHED → ACTIVE → SUCCESS|FAILURE`; a direct `NOT_PUBLISHED → FAILURE` is permitted only
when a bound root exists but ACTIVE publication did not complete. A collision, residual tmp,
wrong inode, wrong schema or illegal transition is `HOLD`. The manifest is mapping authority; it
cannot substitute for fixture, response, process, UI or root-content evidence and is never a root
mutation or cleanup target. Multiple terminal manifests and retained roots may coexist.

The capture root exact artifact allowlist therefore includes `.root-ownership.json`, whose exact
run nonce, first-observed run-root device/inode/type, T1–T3 boundary and T4/T5/atomic non-claims
are bound to the current run. It is created with exclusive `wx` semantics and is never sufficient
without matching created-path and adopted-CWD identity under the approved T1–T3 model. The
allowlist also includes the existing ownership evidence, state, logs, PID and page evidence. The
future runtime exact artifact allowlist additionally includes these fixed frontend paths:

```text
frontend/.edge-mes-runtime-evidence-next.quarantine
frontend/.edge-mes-runtime-evidence-next-env.quarantine
frontend/.edge-mes-runtime-evidence-tsbuildinfo.quarantine
```

`fixture-identity.json` is a regular, non-link, atomic tmp/write/fsync/close/rename record of
the sole generated fixture body: `record_stage=FIXTURE_GENERATED`, SHA-256, exact byte count,
one item, 22 item own keys, and exact `data,page` / `items` / `next_cursor,limit` key sets.
The current shell parses and validates its 64-lowercase-hex digest and positive decimal byte
count before capture launch. These values are integrity evidence, not credentials or secrets.

`capture-response-evidence.json` is likewise a regular, non-link atomic response-completion
record. It cannot be created before the exact `responseBody` Buffer reaches the successful
`res.end(responseBody, callback)` completion callback. The single success writer checks terminal,
current-state, response-error, duplicate and final/tmp guards, then checked-full-writes and
fsyncs this evidence before it advances counts or state to `TARGET_REQUEST_COMPLETE`; any
evidence write failure takes the capture to `ERROR`, retains all lineage evidence and makes the
run `HOLD`. It is synthetic response-byte lineage evidence only, never production evidence.

`process-identities.txt` records the current run nonce together with each role, launch
generation, marker, candidate PID, control-shell PID and lifecycle state. The nonce is a
per-run process-identity value only; it is not a credential or security secret and is never
reused across runs.

The capture's atomic `capture-state.json` contains `state`, `target_count`,
`request_log_count`, `last_stage`, `error_code`, `error_message`, `terminal`, `accepting`,
`response_error_seen`, `response_completion_committed`, and `response_write_started`; it contains
no cookie, authorization, credentials, or secret environment value. Its fixed `.tmp` is opened,
written, fsynced/closed, then renamed to the exact final path. Dynamic temporary names and
wildcards are forbidden.

States are `STARTING`, `LISTENING`, `TARGET_REQUEST_IN_PROGRESS`,
`TARGET_REQUEST_COMPLETE`, `ERROR`, `TERMINATING`, and `TERMINATED`. The one request is valid
only at the commit point: target state in progress → same-Buffer fixture read/digest/shape
validation → exact JSONL append → HTTP `res.end(responseBody, callback)` completion → atomic
response-evidence write/fsync/close/rename → `responseCompletionCommitted=true` → counts equal
one → atomic `TARGET_REQUEST_COMPLETE`. Any partial operation writes/attempts `ERROR`, stops
accepting requests, retains evidence, and makes the overall run `HOLD`. TERM writes or
attempts `TERMINATING`, closes or prevents the server listener, attempts `TERMINATED`, and
exits. The capture-local `terminationStarted` and `terminationCompleted` flags distinguish
signal intent from completed cleanup; a state-write failure records stderr and sets
`process.exitCode=1`, but never returns before the best-effort close/no-listener path. A
terminal-state write failure remains `HOLD` without stopping the other cleanup attempts.

### 8.1 Capture state-transition matrix

The capture process has one fail-closed transition authority, `canTransition(current, next)`,
used by every `set()` call. Same-state writes are permitted only to retain an error/evidence
field without changing the state; success logic never uses a same-state write as a completion
substitute.

```text
Allowed normal path:
STARTING → LISTENING → TARGET_REQUEST_IN_PROGRESS → TARGET_REQUEST_COMPLETE
TARGET_REQUEST_COMPLETE → TERMINATING → TERMINATED

Allowed failure paths:
STARTING/LISTENING/TARGET_REQUEST_IN_PROGRESS/TARGET_REQUEST_COMPLETE → ERROR

Allowed signal cleanup:
STARTING/LISTENING/TARGET_REQUEST_IN_PROGRESS/TARGET_REQUEST_COMPLETE → TERMINATING → TERMINATED
ERROR → TERMINATING → TERMINATED only for post-fatal signal cleanup

Forbidden success-overwrite transitions:
ERROR → TARGET_REQUEST_COMPLETE
TERMINATING → TARGET_REQUEST_COMPLETE
TERMINATED → TARGET_REQUEST_COMPLETE

Forbidden listener recovery transitions:
ERROR → LISTENING
TERMINATING → LISTENING
TERMINATED → LISTENING
```

`set()` rejects every non-listed transition and never replaces an existing `ERROR`,
`TERMINATING` or `TERMINATED` state with success. A fatal response/error path sets
`terminal=true` and `accepting=false` before attempting the `ERROR` state write; if a
terminal state is already committed, it retains that state and records the error fields
without attempting a forbidden transition. A signal path sets
`terminationStarted=true`, then `terminal=true` and `accepting=false` before any server close
callback, attempts `TERMINATING`, and continues cleanup even if that write fails.
`terminationCompleted=true` is set only after the no-listener path or the listening server's
close callback has returned and the `TERMINATED` write has been attempted. A pending response
success writer and a pending listen callback can only return through their terminal/current-state
guards.

## 9. Phase assertions and success boundary

Phase A requires exact capture launch identity, `LISTENING`, target count zero, request-log
count zero, no error state, and an active capture listener. Phase B requires
`TARGET_REQUEST_COMPLETE`, both counts one, an exact request entry, no error state, completed
response evidence, one item/22-key proof, and frozen expected = capture-read = served Buffer =
post-request fixture SHA-256 and byte-count equality. Checking a count, JSONL line, HTML marker
or one digest alone cannot pass.

Success is reachable only after both phases pass, all identities remain valid, all TERM and
wait operations finish, both ports release, all six build checkpoints pass, capture state is
consistent, generated/quarantine cleanup completes, terminal evidence is emitted and the per-run
manifest atomically reaches `SUCCESS`. The physical run root and manifest are retained; only the
separately verified frontend generated/quarantine artifacts enter success deletion. Failure never
cleans Git, the private parent, a run root, a manifest, the legacy root or evidence.

## 10. A/B/C evidence classification plus D filesystem boundary and REL-URL-R6

| Class | May prove | Must not claim |
| --- | --- | --- |
| A. Transport | local method/path/host/query, request cardinality, same artifact/restart behavior | DNS, TLS, egress, deployment |
| B. Frozen synthetic fixture | generated/capture-read/exact-served/post-request body equality plus strict parser/view/UI and explicitly checked HTML markers | exact aggregation, pagination behavior, API producer correctness, database validity, adapter/collector lineage, production facts |
| C. Real production facts | nothing in this run; remains `NOT EXECUTED / NOT CLAIMED` | any production-fact conclusion |
| D. Filesystem evidence boundary | defense against T1, T2 within the owner/0700/non-privileged assumptions, and T3 ordinary concurrency | T4 deliberate same-UID race resistance, T5 privileged/root resistance, atomic mkdir-and-open, kernel sandbox |

`REL-URL-R6` remains **CARRY FORWARD**.

## 11. Future execution allowlist and non-goals

The future run may create only one derived `run-<64-lowercase-hex nonce>` root, its exact
`.root-ownership.json`, the root artifacts listed in section 8, one matching
`run-<nonce>.manifest.json` and fixed `.run-<nonce>.manifest.json.tmp`, the three task-created
generated source paths and the three fixed quarantine paths stated above. The dynamic names are
not user/query/timestamp inputs; they are exact derivatives of one cryptographic nonce. The
private parent and its marker must pre-exist and are never created by Section 14.

The run may not create helper `.sh`/`.js` files, package scripts, sourced helpers, configs,
symlink pointers, predictable counter/timestamp-only roots or wildcard cleanup targets. The
quarantine target is always the fixed path for the matching source artifact; no run root,
manifest, private parent, legacy root or other path may become a deletion target.

## 12. Shell option policy

The canonical block starts with `unsetopt errexit err_return local_traps` and does not rely on
`set -e`, `pipefail`, `nounset`, `ERR_RETURN`, or `LOCAL_TRAPS`. Every material command checks
its return explicitly and transfers ordinary failure by `return` from `runtime_evidence_main`.

## 13. Literal-command reading rule

Section 14 is a future execution authority only. It must not be run in this planning task.
Its inline Node programs are part of the one zsh lifecycle, not helper files. Literal paths,
ports, query values, fixture keys, TERM-only policy, and evidence labels are frozen. The
single `full_write_helper` definition is injected into the fixture generator and capture
process; no helper file or second write implementation is authorized.

## 14. Exact future execution command sequence

```zsh
# Canonical future-run authority. Do not run during planning/review.
unsetopt errexit err_return local_traps

repo_root=/Users/chenjie/Documents/MES/edge-mes-demo
frontend_root="$repo_root/frontend"
legacy_fixed_root=/tmp/edge-mes-dashboard-url-runtime-evidence
private_parent=/tmp/edge-mes-dashboard-url-runtime-evidence-runs
private_parent_marker=.edge-mes-private-parent-authority.json
private_parent_effective_uid=
private_parent_owner_uid=
private_parent_mode=
private_parent_path=$private_parent
canonical_private_parent_path=NOT_AVAILABLE
private_parent_device=NOT_AVAILABLE
private_parent_inode=NOT_AVAILABLE
private_parent_type=NOT_AVAILABLE
private_parent_marker_digest=NOT_AVAILABLE
logical_root=UNASSIGNED
evidence_root=UNBOUND
logical_parent="$private_parent"
canonical_parent=
canonical_root=NOT_AVAILABLE
root_basename=
logical_manifest_report_path=UNASSIGNED
canonical_manifest_report_path=UNASSIGNED
manifest_basename=
manifest_tmp_basename=
manifest_confirmed_digest=NOT_PUBLISHED
manifest_confirmed_state=NOT_PUBLISHED
manifest_publication_result=NOT_STARTED
manifest_reconciliation_state=NOT_RUN
manifest_parent_fsync_result=NOT_CHECKED
terminal_commit_state=PRE_TERMINAL
terminal_pass_line=
terminal_pass_line_prefix=
logical_evidence_identity=UNASSIGNED
run_start_timestamp=NOT_RECORDED
gate_purpose=DASHBOARD_PRODUCTION_URL_RESOLUTION_RUNTIME_EVIDENCE
expected_final_state=SUCCESS_OR_FAILURE_RETAINED
threat_boundary_version=ROOT_IDENTITY_OPTION_C_V1
filesystem_threat_boundary=T1_T2_T3
strict_same_uid_race_proof=NOT_CLAIMED
privileged_root_adversary_proof=NOT_CLAIMED
atomic_mkdir_open_claim=NOT_CLAIMED
run_root_creation_model=EXCLUSIVE_UNPREDICTABLE_BASENAME_WITH_CWD_OBJECT_BINDING
logical_parent_device=
logical_parent_inode=
logical_parent_type=
canonical_parent_device=
canonical_parent_inode=
canonical_parent_type=
created_root_device=
created_root_inode=
created_root_type=
created_root_ownership_digest=
root_ownership_marker_digest=NOT_AVAILABLE
root_ownership_marker=.root-ownership.json
root_device=NOT_AVAILABLE
root_inode=NOT_AVAILABLE
root_type=NOT_AVAILABLE
root_cwd_bound=no
retained_root_visibility_result=NOT_CHECKED
logical_root_visibility=NOT_CHECKED
canonical_root_visibility=NOT_CHECKED
retained_root_identity_equality=NOT_CHECKED
retained_parent_identity=NOT_CHECKED
capture_port=3100
next_port=3101
quarantine_next="$frontend_root/.edge-mes-runtime-evidence-next.quarantine"
quarantine_next_env="$frontend_root/.edge-mes-runtime-evidence-next-env.quarantine"
quarantine_tsbuildinfo="$frontend_root/.edge-mes-runtime-evidence-tsbuildinfo.quarantine"

runtime_failure_code=
runtime_failure_reason=
runtime_interrupted=no
runtime_signal_handling=no
runtime_signal_exit_code=0
runtime_dispatch_started=no
runtime_root_created=no
runtime_success_ready=no
runtime_run_nonce=
created_root_capture_result=NOT_STARTED
expected_fixture_sha256=NOT_RECORDED
expected_fixture_bytes=NOT_RECORDED
post_request_fixture_sha256=NOT_RECORDED
post_request_fixture_bytes=NOT_RECORDED
fixture_lineage_result=NOT_CHECKED
capture_response_evidence_state=NOT_CHECKED
capture_last_state=NOT_READ_FROM_SHELL
capture_terminal_flag=NOT_READ_FROM_SHELL
capture_response_error_seen=NOT_READ_FROM_SHELL
capture_response_completion_committed=NOT_READ_FROM_SHELL
capture_response_write_started=NOT_READ_FROM_SHELL
completion_wait_result=NOT_STARTED
completion_wait_attempts=10
completion_wait_interval=1

# One checked Buffer full-write helper for all Round-5 lineage writes.
# It converts input to Buffer, starts at offset 0, rejects every non-positive or
# non-integer write, verifies the final offset, and is never followed by fsync,
# close/rename or capture launch after a write failure.
full_write_helper='(fd,input,writeSync) => { const buffer=Buffer.isBuffer(input) ? input : Buffer.from(input); let offset=0; while (offset < buffer.length) { const remaining=buffer.length-offset; const written=writeSync(fd,buffer,offset,remaining); if (!Number.isInteger(written) || written <= 0) throw new Error("FULL_WRITE_FAILURE"); offset += written; } if (offset !== buffer.length) throw new Error("FULL_WRITE_MISMATCH"); return offset; }'

capture_state=NOT_STARTED
phase_a_state=NOT_STARTED
phase_b_state=NOT_STARTED
capture_pid=
phase_a_pid=
phase_b_pid=
capture_ppid=
phase_a_ppid=
phase_b_ppid=
capture_start=
phase_a_start=
phase_b_start=
capture_argv=
phase_a_argv=
phase_b_argv=
capture_digest=
phase_a_digest=
phase_b_digest=
capture_role=
phase_a_role=
phase_b_role=
capture_candidate_pid=
phase_a_candidate_pid=
phase_b_candidate_pid=
capture_candidate_ppid=
phase_a_candidate_ppid=
phase_b_candidate_ppid=
capture_candidate_generation=
phase_a_candidate_generation=
phase_b_candidate_generation=
capture_candidate_run_nonce=
phase_a_candidate_run_nonce=
phase_b_candidate_run_nonce=
capture_candidate_role=
phase_a_candidate_role=
phase_b_candidate_role=
capture_candidate_marker=
phase_a_candidate_marker=
phase_b_candidate_marker=
capture_launch_generation=
phase_a_launch_generation=
phase_b_launch_generation=
capture_reaped=no
phase_a_reaped=no
phase_b_reaped=no
capture_wait_status=NOT_WAITED
phase_a_wait_status=NOT_WAITED
phase_b_wait_status=NOT_WAITED
capture_request_phase=UNREGISTERED
phase_a_request_phase=UNREGISTERED
phase_b_request_phase=UNREGISTERED
runtime_launch_generation=0

cleanup_result_phase_b=NOT_STARTED
cleanup_result_phase_a=NOT_STARTED
cleanup_result_capture=NOT_STARTED
cleanup_role_result=NOT_STARTED
cleanup_call_rc=0
port_release_result_next=NOT_CHECKED
port_release_result_capture=NOT_CHECKED
port_release_result=NOT_CHECKED
listener_state_result=NOT_CHECKED
listener_evidence_write_result=NOT_CHECKED
build_artifact_next=NOT_CREATED
build_artifact_next_env=NOT_CREATED
build_artifact_tsbuildinfo=NOT_CREATED
ownership_handoff_stage=NOT_STARTED
ownership_verification_result=NOT_STARTED
deletion_stage=NOT_STARTED
postcondition_result=NOT_STARTED
handoff_next=NOT_STARTED
handoff_next_env=NOT_STARTED
handoff_tsbuildinfo=NOT_STARTED
ownership_next_device=
ownership_next_inode=
ownership_next_type=
ownership_next_symlink_status=
ownership_next_env_device=
ownership_next_env_inode=
ownership_next_env_type=
ownership_next_env_symlink_status=
ownership_tsbuildinfo_device=
ownership_tsbuildinfo_inode=
ownership_tsbuildinfo_type=
ownership_tsbuildinfo_symlink_status=

runtime_hold() {
  runtime_failure_code=$1
  runtime_failure_reason=$2
  printf 'HOLD[%s]: %s\n' "$runtime_failure_code" "$runtime_failure_reason" >&2
  return 1
}

no_path_or_link() {
  test ! -e "$1" && test ! -L "$1"
}

# `logical_root` is used only to find a directory before it is bound. After
# `bind_root_cwd` succeeds, all evidence operations are relative to the shell's
# current working-directory object (`.`), never to `logical_root` or
# `canonical_root`. macOS may map /tmp to /private/tmp for the same object.
# Node has no supported macOS `openat`/`unlinkat`/`renameat` API. This literal
# therefore deliberately does not pretend to have descriptor-relative pathname
# mutation. The supported equivalent here is a verified directory CWD inherited
# by every evidence child: pathname replacement cannot retarget `./artifact`.
read_root_stat() {
  root_stat_path=$1
  root_stat_values=$(/usr/bin/stat -f '%d|%i|%HT|%u|%Lp' -- "$root_stat_path") || return 1
  IFS='|' read -r root_stat_device root_stat_inode root_stat_type root_stat_owner root_stat_mode <<EOF
$root_stat_values
EOF
  test -n "$root_stat_device" && test -n "$root_stat_inode" && test -n "$root_stat_type" && test -n "$root_stat_owner" && test -n "$root_stat_mode"
}

read_cwd_stat() {
  read_root_stat . || return 1
}

same_directory_object() {
  test "$1" = "$3" && test "$2" = "$4" && test "$5" = Directory && test "$6" = Directory
}

validate_private_parent_marker_path() {
  private_parent_marker_path="$private_parent/$private_parent_marker"
  private_parent_marker_value=$(PRIVATE_PARENT_MARKER_PATH="$private_parent_marker_path" PRIVATE_PARENT="$private_parent" CANONICAL_PARENT="$canonical_parent" EFFECTIVE_UID="$private_parent_effective_uid" PARENT_DEVICE="$logical_parent_device" PARENT_INODE="$logical_parent_inode" GATE_PURPOSE="$gate_purpose" node --input-type=module --eval '
import {createHash} from "node:crypto";import {lstatSync,readFileSync} from "node:fs";
const path=process.env.PRIVATE_PARENT_MARKER_PATH,st=lstatSync(path,{bigint:true});
if(!st.isFile()||String(st.uid)!==process.env.EFFECTIVE_UID||Number(st.mode&0o777n)!==0o600)throw new Error("PRIVATE_PARENT_MARKER_METADATA");
const raw=readFileSync(path),value=JSON.parse(raw.toString("utf8")),keys=["schema_version","record_stage","gate_purpose","private_parent","canonical_private_parent","parent_device","parent_inode","parent_type","owner_uid","mode"];
if(Object.keys(value).length!==keys.length||keys.some(key=>!Object.prototype.hasOwnProperty.call(value,key)))throw new Error("PRIVATE_PARENT_MARKER_SCHEMA");
if(value.schema_version!=="1"||value.record_stage!=="PRIVATE_PARENT_PREPARED"||value.gate_purpose!==process.env.GATE_PURPOSE||value.private_parent!==process.env.PRIVATE_PARENT||value.canonical_private_parent!==process.env.CANONICAL_PARENT||value.parent_device!==process.env.PARENT_DEVICE||value.parent_inode!==process.env.PARENT_INODE||value.parent_type!=="Directory"||value.owner_uid!==process.env.EFFECTIVE_UID||value.mode!=="0700")throw new Error("PRIVATE_PARENT_MARKER_CONTENT");
process.stdout.write(createHash("sha256").update(raw).digest("hex"));
') || return 1
  printf '%s\n' "$private_parent_marker_value" | /usr/bin/grep -Eq '^[0-9a-f]{64}$' || return 1
  printf '%s' "$private_parent_marker_value"
}

validate_private_parent_marker_cwd() {
  PRIVATE_PARENT_MARKER="./$private_parent_marker" PRIVATE_PARENT="$private_parent" CANONICAL_PARENT="$canonical_parent" EFFECTIVE_UID="$private_parent_effective_uid" PARENT_DEVICE="$logical_parent_device" PARENT_INODE="$logical_parent_inode" EXPECTED_DIGEST="$private_parent_marker_digest" GATE_PURPOSE="$gate_purpose" node --input-type=module --eval '
import {createHash} from "node:crypto";import {lstatSync,readFileSync} from "node:fs";
const cwd=lstatSync(".",{bigint:true});if(!cwd.isDirectory()||String(cwd.dev)!==process.env.PARENT_DEVICE||String(cwd.ino)!==process.env.PARENT_INODE||String(cwd.uid)!==process.env.EFFECTIVE_UID||Number(cwd.mode&0o777n)!==0o700)throw new Error("PRIVATE_PARENT_CWD_METADATA");
const st=lstatSync(process.env.PRIVATE_PARENT_MARKER,{bigint:true});if(!st.isFile()||String(st.uid)!==process.env.EFFECTIVE_UID||Number(st.mode&0o777n)!==0o600)throw new Error("PRIVATE_PARENT_MARKER_METADATA");
const raw=readFileSync(process.env.PRIVATE_PARENT_MARKER),digest=createHash("sha256").update(raw).digest("hex"),value=JSON.parse(raw.toString("utf8")),keys=["schema_version","record_stage","gate_purpose","private_parent","canonical_private_parent","parent_device","parent_inode","parent_type","owner_uid","mode"];
if(digest!==process.env.EXPECTED_DIGEST||Object.keys(value).length!==keys.length||keys.some(key=>!Object.prototype.hasOwnProperty.call(value,key)))throw new Error("PRIVATE_PARENT_MARKER_SCHEMA");
if(value.schema_version!=="1"||value.record_stage!=="PRIVATE_PARENT_PREPARED"||value.gate_purpose!==process.env.GATE_PURPOSE||value.private_parent!==process.env.PRIVATE_PARENT||value.canonical_private_parent!==process.env.CANONICAL_PARENT||value.parent_device!==process.env.PARENT_DEVICE||value.parent_inode!==process.env.PARENT_INODE||value.parent_type!=="Directory"||value.owner_uid!==process.env.EFFECTIVE_UID||value.mode!=="0700")throw new Error("PRIVATE_PARENT_MARKER_CONTENT");
' || return 1
}

validate_private_parent_paths() {
  private_parent_effective_uid=$(/usr/bin/id -u) || return 1
  printf '%s\n' "$private_parent_effective_uid" | /usr/bin/grep -Eq '^[0-9]+$' || return 1
  test -d "$private_parent" && test ! -L "$private_parent" || return 1
  canonical_parent=$(cd -P "$private_parent" && /bin/pwd -P) || return 1
  test -d "$canonical_parent" && test ! -L "$canonical_parent" || return 1
  read_root_stat "$private_parent" || return 1
  logical_parent_device=$root_stat_device; logical_parent_inode=$root_stat_inode; logical_parent_type=$root_stat_type; private_parent_owner_uid=$root_stat_owner; private_parent_mode=$root_stat_mode
  read_root_stat "$canonical_parent" || return 1
  canonical_parent_device=$root_stat_device; canonical_parent_inode=$root_stat_inode; canonical_parent_type=$root_stat_type
  same_directory_object "$logical_parent_device" "$logical_parent_inode" "$canonical_parent_device" "$canonical_parent_inode" "$logical_parent_type" "$canonical_parent_type" || return 1
  test "$private_parent_owner_uid" = "$private_parent_effective_uid" && test "$private_parent_mode" = 700 || return 1
  test "$root_stat_owner" = "$private_parent_effective_uid" && test "$root_stat_mode" = 700 || return 1
  private_parent_marker_digest=$(validate_private_parent_marker_path) || return 1
  private_parent_path=$logical_parent
  canonical_private_parent_path=$canonical_parent
  private_parent_device=$logical_parent_device
  private_parent_inode=$logical_parent_inode
  private_parent_type=$logical_parent_type
  return 0
}

validate_parent_cwd() {
  read_cwd_stat || return 1
  same_directory_object "$root_stat_device" "$root_stat_inode" "$logical_parent_device" "$logical_parent_inode" "$root_stat_type" "$logical_parent_type" || return 1
  same_directory_object "$root_stat_device" "$root_stat_inode" "$canonical_parent_device" "$canonical_parent_inode" "$root_stat_type" "$canonical_parent_type" || return 1
  test "$root_stat_owner" = "$private_parent_effective_uid" && test "$root_stat_mode" = 700 || return 1
  validate_private_parent_marker_cwd
}

create_and_capture_run_root() {
  # Under the approved T1-T3 boundary, one Node process performs exclusive
  # unpredictable-basename creation, immediate non-following identity capture,
  # and exclusive ownership-marker creation. This is not an atomic mkdir/open
  # claim and does not claim defense against a deliberate same-UID race (T4).
  validate_parent_cwd || return 1
  test -n "$runtime_run_nonce" && test "$root_basename" = "run-$runtime_run_nonce" || return 1
  created_root_values=$(FULL_WRITE_HELPER="$full_write_helper" PARENT_DEVICE="$logical_parent_device" PARENT_INODE="$logical_parent_inode" EFFECTIVE_UID="$private_parent_effective_uid" ROOT_BASENAME="$root_basename" ROOT_OWNERSHIP_MARKER="$root_ownership_marker" RUN_NONCE="$runtime_run_nonce" FILESYSTEM_THREAT_BOUNDARY="$filesystem_threat_boundary" STRICT_SAME_UID_RACE_PROOF="$strict_same_uid_race_proof" PRIVILEGED_ROOT_ADVERSARY_PROOF="$privileged_root_adversary_proof" ATOMIC_MKDIR_OPEN_CLAIM="$atomic_mkdir_open_claim" RUN_ROOT_CREATION_MODEL="$run_root_creation_model" node --input-type=module --eval '
import {closeSync,fsyncSync,lstatSync,mkdirSync,openSync,writeSync} from "node:fs";
import {createHash} from "node:crypto";
const parent=lstatSync(".",{bigint:true});
if(!parent.isDirectory()||String(parent.dev)!==process.env.PARENT_DEVICE||String(parent.ino)!==process.env.PARENT_INODE||String(parent.uid)!==process.env.EFFECTIVE_UID||Number(parent.mode&0o777n)!==0o700)throw new Error("PRIVATE_PARENT_CWD_IDENTITY");
const basename=process.env.ROOT_BASENAME,marker=process.env.ROOT_OWNERSHIP_MARKER,nonce=process.env.RUN_NONCE;
if(!(/^[0-9a-f]{64}$/).test(nonce)||basename!==`run-${nonce}`||basename.includes("/")||!marker||marker.includes("/"))throw new Error("RUN_ROOT_CREATE_INPUT");
try{lstatSync(basename);throw new Error("RUN_ROOT_EXISTS");}catch(error){if(error?.code!=="ENOENT")throw error;}
mkdirSync(basename,{mode:0o700});
const created=lstatSync(basename,{bigint:true});
if(!created.isDirectory()||String(created.uid)!==process.env.EFFECTIVE_UID||Number(created.mode&0o777n)!==0o700)throw new Error("RUN_ROOT_CREATED_METADATA");
const createdDevice=String(created.dev),createdInode=String(created.ino),createdType="Directory";
const value={schema_version:"1",record_stage:"RUN_ROOT_CREATED_CAPTURED",run_nonce:nonce,root_basename:basename,root_device:createdDevice,root_inode:createdInode,root_type:createdType,filesystem_threat_boundary:process.env.FILESYSTEM_THREAT_BOUNDARY,strict_same_uid_race_proof:process.env.STRICT_SAME_UID_RACE_PROOF,privileged_root_adversary_proof:process.env.PRIVILEGED_ROOT_ADVERSARY_PROOF,atomic_mkdir_open_claim:process.env.ATOMIC_MKDIR_OPEN_CLAIM,run_root_creation_model:process.env.RUN_ROOT_CREATION_MODEL};
const payload=Buffer.from(JSON.stringify(value)+"\n"),markerPath=`${basename}/${marker}`,writeFully=eval(process.env.FULL_WRITE_HELPER);let fd=-1;
try{fd=openSync(markerPath,"wx",0o600);writeFully(fd,payload,writeSync);fsyncSync(fd);closeSync(fd);fd=-1;}catch(error){if(fd>=0)try{closeSync(fd);}catch{}throw error;}
const after=lstatSync(basename,{bigint:true}),markerStat=lstatSync(markerPath,{bigint:true});
if(!after.isDirectory()||String(after.dev)!==createdDevice||String(after.ino)!==createdInode||String(after.uid)!==process.env.EFFECTIVE_UID||Number(after.mode&0o777n)!==0o700||!markerStat.isFile()||String(markerStat.uid)!==process.env.EFFECTIVE_UID||Number(markerStat.mode&0o777n)!==0o600)throw new Error("RUN_ROOT_REPLACED_DURING_CAPTURE");
process.stdout.write(`${createdDevice}|${createdInode}|${createdType}|${createHash("sha256").update(payload).digest("hex")}`);
')
  created_root_capture_rc=$?
  test "$created_root_capture_rc" -eq 0 || { created_root_capture_result=UNCERTAIN; return 1; }
  IFS='|' read -r created_root_device created_root_inode created_root_type created_root_ownership_digest <<EOF
$created_root_values
EOF
  test -n "$created_root_device" && test -n "$created_root_inode" && test "$created_root_type" = Directory || { created_root_capture_result=INVALID; return 1; }
  printf '%s\n' "$created_root_ownership_digest" | /usr/bin/grep -Eq '^[0-9a-f]{64}$' || { created_root_capture_result=INVALID; return 1; }
  created_root_capture_result=FROZEN
}

validate_created_root_path() {
  test "$created_root_capture_result" = FROZEN || return 1
  validate_parent_cwd || return 1
  PARENT_DEVICE="$logical_parent_device" PARENT_INODE="$logical_parent_inode" EFFECTIVE_UID="$private_parent_effective_uid" ROOT_BASENAME="$root_basename" ROOT_OWNERSHIP_MARKER="$root_ownership_marker" RUN_NONCE="$runtime_run_nonce" CREATED_ROOT_DEVICE="$created_root_device" CREATED_ROOT_INODE="$created_root_inode" CREATED_ROOT_TYPE="$created_root_type" CREATED_ROOT_OWNERSHIP_DIGEST="$created_root_ownership_digest" FILESYSTEM_THREAT_BOUNDARY="$filesystem_threat_boundary" STRICT_SAME_UID_RACE_PROOF="$strict_same_uid_race_proof" PRIVILEGED_ROOT_ADVERSARY_PROOF="$privileged_root_adversary_proof" ATOMIC_MKDIR_OPEN_CLAIM="$atomic_mkdir_open_claim" RUN_ROOT_CREATION_MODEL="$run_root_creation_model" node --input-type=module --eval '
import {createHash} from "node:crypto";import {lstatSync,readFileSync} from "node:fs";
const parent=lstatSync(".",{bigint:true});if(!parent.isDirectory()||String(parent.dev)!==process.env.PARENT_DEVICE||String(parent.ino)!==process.env.PARENT_INODE||String(parent.uid)!==process.env.EFFECTIVE_UID||Number(parent.mode&0o777n)!==0o700)throw new Error("PRIVATE_PARENT_CWD_IDENTITY");
const child=lstatSync(process.env.ROOT_BASENAME,{bigint:true});if(!child.isDirectory()||String(child.dev)!==process.env.CREATED_ROOT_DEVICE||String(child.ino)!==process.env.CREATED_ROOT_INODE||String(child.uid)!==process.env.EFFECTIVE_UID||Number(child.mode&0o777n)!==0o700||process.env.CREATED_ROOT_TYPE!=="Directory")throw new Error("RUN_ROOT_CREATED_PATH_IDENTITY");
const markerPath=`${process.env.ROOT_BASENAME}/${process.env.ROOT_OWNERSHIP_MARKER}`,marker=lstatSync(markerPath,{bigint:true});if(!marker.isFile()||String(marker.uid)!==process.env.EFFECTIVE_UID||Number(marker.mode&0o777n)!==0o600)throw new Error("ROOT_OWNERSHIP_MARKER_TYPE");
const raw=readFileSync(markerPath),digest=createHash("sha256").update(raw).digest("hex"),value=JSON.parse(raw.toString("utf8")),keys=["schema_version","record_stage","run_nonce","root_basename","root_device","root_inode","root_type","filesystem_threat_boundary","strict_same_uid_race_proof","privileged_root_adversary_proof","atomic_mkdir_open_claim","run_root_creation_model"];
if(Object.keys(value).length!==keys.length||keys.some(key=>!Object.prototype.hasOwnProperty.call(value,key))||digest!==process.env.CREATED_ROOT_OWNERSHIP_DIGEST||value.schema_version!=="1"||value.record_stage!=="RUN_ROOT_CREATED_CAPTURED"||value.run_nonce!==process.env.RUN_NONCE||value.root_basename!==process.env.ROOT_BASENAME||value.root_device!==process.env.CREATED_ROOT_DEVICE||value.root_inode!==process.env.CREATED_ROOT_INODE||value.root_type!==process.env.CREATED_ROOT_TYPE||value.filesystem_threat_boundary!==process.env.FILESYSTEM_THREAT_BOUNDARY||value.strict_same_uid_race_proof!==process.env.STRICT_SAME_UID_RACE_PROOF||value.privileged_root_adversary_proof!==process.env.PRIVILEGED_ROOT_ADVERSARY_PROOF||value.atomic_mkdir_open_claim!==process.env.ATOMIC_MKDIR_OPEN_CLAIM||value.run_root_creation_model!==process.env.RUN_ROOT_CREATION_MODEL)throw new Error("ROOT_OWNERSHIP_MARKER_CONTENT");
' || return 1
}

validate_root_ownership_marker() {
  validate_root_binding || return 1
  ROOT_DEVICE="$root_device" ROOT_INODE="$root_inode" EFFECTIVE_UID="$private_parent_effective_uid" ROOT_BASENAME="$root_basename" ROOT_OWNERSHIP_MARKER="./$root_ownership_marker" RUN_NONCE="$runtime_run_nonce" CREATED_ROOT_OWNERSHIP_DIGEST="$created_root_ownership_digest" FILESYSTEM_THREAT_BOUNDARY="$filesystem_threat_boundary" STRICT_SAME_UID_RACE_PROOF="$strict_same_uid_race_proof" PRIVILEGED_ROOT_ADVERSARY_PROOF="$privileged_root_adversary_proof" ATOMIC_MKDIR_OPEN_CLAIM="$atomic_mkdir_open_claim" RUN_ROOT_CREATION_MODEL="$run_root_creation_model" node --input-type=module --eval '
import {createHash} from "node:crypto";import {lstatSync,readFileSync} from "node:fs";
const root=lstatSync(".",{bigint:true});if(!root.isDirectory()||String(root.dev)!==process.env.ROOT_DEVICE||String(root.ino)!==process.env.ROOT_INODE||String(root.uid)!==process.env.EFFECTIVE_UID||Number(root.mode&0o777n)!==0o700)throw new Error("ROOT_CWD_IDENTITY");
const marker=lstatSync(process.env.ROOT_OWNERSHIP_MARKER,{bigint:true});if(!marker.isFile()||String(marker.uid)!==process.env.EFFECTIVE_UID||Number(marker.mode&0o777n)!==0o600)throw new Error("ROOT_OWNERSHIP_MARKER_TYPE");
const raw=readFileSync(process.env.ROOT_OWNERSHIP_MARKER),digest=createHash("sha256").update(raw).digest("hex"),value=JSON.parse(raw.toString("utf8")),keys=["schema_version","record_stage","run_nonce","root_basename","root_device","root_inode","root_type","filesystem_threat_boundary","strict_same_uid_race_proof","privileged_root_adversary_proof","atomic_mkdir_open_claim","run_root_creation_model"];
if(digest!==process.env.CREATED_ROOT_OWNERSHIP_DIGEST||Object.keys(value).length!==keys.length||keys.some(key=>!Object.prototype.hasOwnProperty.call(value,key))||value.schema_version!=="1"||value.record_stage!=="RUN_ROOT_CREATED_CAPTURED"||value.run_nonce!==process.env.RUN_NONCE||value.root_basename!==process.env.ROOT_BASENAME||value.root_device!==process.env.ROOT_DEVICE||value.root_inode!==process.env.ROOT_INODE||value.root_type!=="Directory"||value.filesystem_threat_boundary!==process.env.FILESYSTEM_THREAT_BOUNDARY||value.strict_same_uid_race_proof!==process.env.STRICT_SAME_UID_RACE_PROOF||value.privileged_root_adversary_proof!==process.env.PRIVILEGED_ROOT_ADVERSARY_PROOF||value.atomic_mkdir_open_claim!==process.env.ATOMIC_MKDIR_OPEN_CLAIM||value.run_root_creation_model!==process.env.RUN_ROOT_CREATION_MODEL)throw new Error("ROOT_OWNERSHIP_MARKER_CONTENT");
' || return 1
}

bind_root_cwd() {
  # Under T1-T3, the current run basename and marker must still match the first
  # observed run-root identity, then the adopted CWD must equal that identity.
  # This does not claim atomic mkdir-and-open or T4 resistance.
  validate_created_root_path || return 1
  cd -P "$root_basename" || return 1
  read_cwd_stat || return 1
  same_directory_object "$root_stat_device" "$root_stat_inode" "$created_root_device" "$created_root_inode" "$root_stat_type" "$created_root_type" || return 1
  test "$root_stat_owner" = "$private_parent_effective_uid" && test "$root_stat_mode" = 700 || return 1
  root_device=$created_root_device
  root_inode=$created_root_inode
  root_type=$created_root_type
  root_cwd_bound=yes
  evidence_root=.
  canonical_root=$(pwd -P) || return 1
  test "${canonical_root%/*}" = "$canonical_parent" && test "${canonical_root##*/}" = "$root_basename" || return 1
  validate_root_binding || return 1
  validate_root_ownership_marker
}

validate_root_binding() {
  test "$root_cwd_bound" = yes && test "$evidence_root" = . && test -n "$root_device" && test -n "$root_inode" && test "$root_type" = Directory || return 1
  read_cwd_stat || return 1
  same_directory_object "$root_stat_device" "$root_stat_inode" "$root_device" "$root_inode" "$root_stat_type" "$root_type" || return 1
  test "$root_stat_owner" = "$private_parent_effective_uid" && test "$root_stat_mode" = 700
}

root_artifact_path() {
  # A root artifact name is never an absolute, parent-traversing, or nested path.
  # The returned path is relative to the already verified CWD directory object.
  validate_root_binding || return 1
  case "$1" in
    ''|.|..|*/*|*'\\'*|*'..'*) return 1 ;;
    *) printf './%s' "$1" ;;
  esac
}

root_write_atomic_stdin() {
  root_artifact_name=$1
  root_artifact_final=$(root_artifact_path "$root_artifact_name") || return 1
  root_artifact_tmp=$(root_artifact_path ".${root_artifact_name}.tmp") || return 1
  ROOT_ARTIFACT_FINAL="$root_artifact_final" ROOT_ARTIFACT_TMP="$root_artifact_tmp" ROOT_DEVICE="$root_device" ROOT_INODE="$root_inode" node --input-type=module --eval '
import {closeSync,fsyncSync,lstatSync,openSync,renameSync,writeSync} from "node:fs";
const st=lstatSync("."); if(!st.isDirectory()||String(st.dev)!==process.env.ROOT_DEVICE||String(st.ino)!==process.env.ROOT_INODE) throw new Error("ROOT_CWD_IDENTITY");
const finalPath=process.env.ROOT_ARTIFACT_FINAL,tmpPath=process.env.ROOT_ARTIFACT_TMP; try{lstatSync(finalPath);throw new Error("ROOT_ARTIFACT_EXISTS");}catch(error){if(error?.code!=="ENOENT")throw error;}
const chunks=[];for await(const chunk of process.stdin)chunks.push(Buffer.from(chunk));const data=Buffer.concat(chunks);let fd=-1;try{fd=openSync(tmpPath,"wx",0o600);let offset=0;while(offset<data.length){const wrote=writeSync(fd,data,offset,data.length-offset);if(!Number.isInteger(wrote)||wrote<=0)throw new Error("FULL_WRITE_FAILURE");offset+=wrote;}fsyncSync(fd);closeSync(fd);fd=-1;renameSync(tmpPath,finalPath);}catch(error){if(fd>=0)try{closeSync(fd);}catch{}throw error;}
' || return 1
}

freeze_root_precreate() {
  # The private parent is provisioned only by a separate workspace-preparation
  # gate. This runtime validates and adopts it; it never creates, repairs,
  # chmods, renames, empties, or deletes the parent.
  logical_parent=$private_parent
  test "$logical_parent" = /tmp/edge-mes-dashboard-url-runtime-evidence-runs || return 1
  validate_private_parent_paths
}

freeze_root_postcreate() {
  # Parent CWD, pre-adoption basename identity, ownership evidence, and adopted
  # CWD must all agree with the first child identity captured after creation.
  validate_parent_cwd || return 1
  bind_root_cwd
}

validate_root_identity() {
  # This is an object check on `.`. It intentionally never resolves logical or
  # canonical root paths again for evidence I/O authority.
  validate_root_binding
}

validate_retained_root_visibility() {
  # Read-only success/failure retention proof for the run-specific physical
  # root and verified private parent. Declared paths are never mutation targets.
  retained_root_visibility_result=FAIL
  logical_root_visibility=FAIL
  canonical_root_visibility=FAIL
  retained_root_identity_equality=FAIL
  retained_parent_identity=FAIL
  validate_root_binding || return 1
  validate_private_parent_paths || return 1
  LOGICAL_ROOT="$logical_root" CANONICAL_ROOT="$canonical_root" LOGICAL_PARENT="$logical_parent" CANONICAL_PARENT="$canonical_parent" ROOT_BASENAME="$root_basename" ROOT_DEVICE="$root_device" ROOT_INODE="$root_inode" EFFECTIVE_UID="$private_parent_effective_uid" LOGICAL_PARENT_DEVICE="$logical_parent_device" LOGICAL_PARENT_INODE="$logical_parent_inode" CANONICAL_PARENT_DEVICE="$canonical_parent_device" CANONICAL_PARENT_INODE="$canonical_parent_inode" node --input-type=module --eval '
import {basename,dirname} from "node:path";import {lstatSync} from "node:fs";
const cwd=lstatSync(".",{bigint:true}),logical=lstatSync(process.env.LOGICAL_ROOT,{bigint:true}),canonical=lstatSync(process.env.CANONICAL_ROOT,{bigint:true}),logicalParent=lstatSync(process.env.LOGICAL_PARENT,{bigint:true}),canonicalParent=lstatSync(process.env.CANONICAL_PARENT,{bigint:true});
const sameRoot=(value)=>value.isDirectory()&&String(value.dev)===process.env.ROOT_DEVICE&&String(value.ino)===process.env.ROOT_INODE&&String(value.uid)===process.env.EFFECTIVE_UID&&Number(value.mode&0o777n)===0o700;
const sameParent=(value,device,inode)=>value.isDirectory()&&String(value.dev)===device&&String(value.ino)===inode&&String(value.uid)===process.env.EFFECTIVE_UID&&Number(value.mode&0o777n)===0o700;
if(!sameRoot(cwd))throw new Error("ROOT_CWD_IDENTITY");
if(!sameRoot(logical))throw new Error("LOGICAL_ROOT_VISIBILITY");
if(!sameRoot(canonical))throw new Error("CANONICAL_ROOT_VISIBILITY");
if(String(logical.dev)!==String(canonical.dev)||String(logical.ino)!==String(canonical.ino))throw new Error("DECLARED_ROOT_DIVERGENCE");
if(!sameParent(logicalParent,process.env.LOGICAL_PARENT_DEVICE,process.env.LOGICAL_PARENT_INODE)||!sameParent(canonicalParent,process.env.CANONICAL_PARENT_DEVICE,process.env.CANONICAL_PARENT_INODE)||String(logicalParent.dev)!==String(canonicalParent.dev)||String(logicalParent.ino)!==String(canonicalParent.ino))throw new Error("ROOT_PARENT_VISIBILITY");
if(dirname(process.env.CANONICAL_ROOT)!==process.env.CANONICAL_PARENT||basename(process.env.CANONICAL_ROOT)!==process.env.ROOT_BASENAME||dirname(process.env.LOGICAL_ROOT)!==process.env.LOGICAL_PARENT||basename(process.env.LOGICAL_ROOT)!==process.env.ROOT_BASENAME)throw new Error("RUN_ROOT_SHAPE");
' || return 1
  validate_root_ownership_marker || return 1
  logical_root_visibility=PASS
  canonical_root_visibility=PASS
  retained_root_identity_equality=PASS
  retained_parent_identity=PASS
  retained_root_visibility_result=PASS
}

manifest_parent_cwd_preflight() {
  (
    cd -P "$private_parent" || exit 1
    PARENT_DEVICE="$logical_parent_device" PARENT_INODE="$logical_parent_inode" EFFECTIVE_UID="$private_parent_effective_uid" PARENT_MARKER="$private_parent_marker" EXPECTED_MARKER_DIGEST="$private_parent_marker_digest" LOGICAL_PARENT="$private_parent" CANONICAL_PARENT="$canonical_parent" GATE_PURPOSE="$gate_purpose" MANIFEST_BASENAME="$manifest_basename" MANIFEST_TMP_BASENAME="$manifest_tmp_basename" node --input-type=module <<'NODE'
import {createHash} from "node:crypto";
import {lstatSync,readFileSync} from "node:fs";
const parent=lstatSync(".",{bigint:true});
if(!parent.isDirectory()||String(parent.dev)!==process.env.PARENT_DEVICE||String(parent.ino)!==process.env.PARENT_INODE||String(parent.uid)!==process.env.EFFECTIVE_UID||Number(parent.mode&0o777n)!==0o700)throw new Error("MANIFEST_PARENT_CWD_IDENTITY");
const markerName=process.env.PARENT_MARKER;
if(!/^[A-Za-z0-9._-]+$/.test(markerName)||markerName.includes("/"))throw new Error("MANIFEST_PARENT_MARKER_NAME");
const markerPath="./"+markerName,marker=lstatSync(markerPath,{bigint:true});
if(!marker.isFile()||String(marker.uid)!==process.env.EFFECTIVE_UID||Number(marker.mode&0o777n)!==0o600)throw new Error("MANIFEST_PARENT_MARKER_METADATA");
const markerRaw=readFileSync(markerPath),markerDigest=createHash("sha256").update(markerRaw).digest("hex"),markerValue=JSON.parse(markerRaw.toString("utf8"));
const markerKeys=["schema_version","record_stage","gate_purpose","private_parent","canonical_private_parent","parent_device","parent_inode","parent_type","owner_uid","mode"];
if(markerDigest!==process.env.EXPECTED_MARKER_DIGEST||Object.keys(markerValue).length!==markerKeys.length||markerKeys.some(key=>!Object.prototype.hasOwnProperty.call(markerValue,key)))throw new Error("MANIFEST_PARENT_MARKER_SCHEMA");
if(markerValue.schema_version!=="1"||markerValue.record_stage!=="PRIVATE_PARENT_PREPARED"||markerValue.gate_purpose!==process.env.GATE_PURPOSE||markerValue.private_parent!==process.env.LOGICAL_PARENT||markerValue.canonical_private_parent!==process.env.CANONICAL_PARENT||markerValue.parent_device!==String(parent.dev)||markerValue.parent_inode!==String(parent.ino)||markerValue.parent_type!=="Directory"||markerValue.owner_uid!==process.env.EFFECTIVE_UID||markerValue.mode!=="0700")throw new Error("MANIFEST_PARENT_MARKER_CONTENT");
const finalName=process.env.MANIFEST_BASENAME,tmpName=process.env.MANIFEST_TMP_BASENAME;
if(!/^run-[0-9a-f]{64}\.manifest\.json$/.test(finalName)||tmpName!=="."+finalName+".tmp")throw new Error("MANIFEST_BASENAME");
const absent=name=>{try{lstatSync("./"+name);return false;}catch(error){if(error?.code==="ENOENT")return true;throw error;}};
if(!absent(finalName)||!absent(tmpName))throw new Error("MANIFEST_COLLISION");
NODE
  )
}

publish_run_manifest() {
  manifest_target_state=$1
  case "$manifest_target_state" in ACTIVE|SUCCESS|FAILURE) ;;
    *) return 1 ;;
  esac
  validate_root_binding || return 1
  validate_retained_root_visibility || return 1
  test "$logical_manifest_report_path" = "$private_parent/$manifest_basename" && test "$canonical_manifest_report_path" = "$canonical_parent/$manifest_basename" && test "$manifest_tmp_basename" = ".$manifest_basename.tmp" || return 1
  # The control shell remains bound to the evidence-root CWD. This helper enters
  # the private parent in a separate process, verifies . immediately, and
  # performs every manifest operation through ./fixed-basename.
  manifest_parent_publish_output=$(
    (
      cd -P "$private_parent" || exit 1
      FULL_WRITE_HELPER="$full_write_helper" MANIFEST_FINAL="./$manifest_basename" MANIFEST_TMP="./$manifest_tmp_basename" MANIFEST_BASENAME="$manifest_basename" MANIFEST_TMP_BASENAME="$manifest_tmp_basename" PARENT_DEVICE="$logical_parent_device" PARENT_INODE="$logical_parent_inode" EFFECTIVE_UID="$private_parent_effective_uid" PARENT_MARKER="$private_parent_marker" EXPECTED_MARKER_DIGEST="$private_parent_marker_digest" LOGICAL_PARENT="$private_parent" CANONICAL_PARENT="$canonical_parent" PRIVATE_PARENT_PATH="$private_parent_path" CANONICAL_PRIVATE_PARENT_PATH="$canonical_private_parent_path" PRIVATE_PARENT_DEVICE="$private_parent_device" PRIVATE_PARENT_INODE="$private_parent_inode" PRIVATE_PARENT_TYPE="$private_parent_type" PRIVATE_PARENT_OWNER_UID="$private_parent_owner_uid" PRIVATE_PARENT_MODE="$private_parent_mode" PRIVATE_PARENT_MARKER_DIGEST="$private_parent_marker_digest" ROOT_OWNERSHIP_MARKER_DIGEST="$root_ownership_marker_digest" GATE_PURPOSE="$gate_purpose" EXPECTED_CURRENT_STATE="$manifest_confirmed_state" EXPECTED_CURRENT_DIGEST="$manifest_confirmed_digest" TARGET_STATE="$manifest_target_state" LOGICAL_IDENTITY="$logical_evidence_identity" RUN_NONCE="$runtime_run_nonce" PHYSICAL_ROOT="$logical_root" CANONICAL_ROOT="$canonical_root" ROOT_DEVICE="$root_device" ROOT_INODE="$root_inode" ROOT_TYPE="$root_type" RUN_START_TIMESTAMP="$run_start_timestamp" EXPECTED_FINAL_STATE="$expected_final_state" THREAT_BOUNDARY_VERSION="$threat_boundary_version" FILESYSTEM_THREAT_BOUNDARY="$filesystem_threat_boundary" STRICT_SAME_UID_RACE_PROOF="$strict_same_uid_race_proof" PRIVILEGED_ROOT_ADVERSARY_PROOF="$privileged_root_adversary_proof" ATOMIC_MKDIR_OPEN_CLAIM="$atomic_mkdir_open_claim" RUN_ROOT_CREATION_MODEL="$run_root_creation_model" LEGACY_FIXED_ROOT="$legacy_fixed_root" node --input-type=module <<'NODE'
import {createHash} from "node:crypto";
import {closeSync,fsyncSync,lstatSync,openSync,readFileSync,renameSync,writeSync} from "node:fs";
const finalPath=process.env.MANIFEST_FINAL,tmpPath=process.env.MANIFEST_TMP,finalName=process.env.MANIFEST_BASENAME,tmpName=process.env.MANIFEST_TMP_BASENAME,current=process.env.EXPECTED_CURRENT_STATE,target=process.env.TARGET_STATE,expectedDigest=process.env.EXPECTED_CURRENT_DIGEST;
const parent=lstatSync(".");
if(!parent.isDirectory()||String(parent.dev)!==process.env.PARENT_DEVICE||String(parent.ino)!==process.env.PARENT_INODE||String(parent.uid)!==process.env.EFFECTIVE_UID||Number(parent.mode&0o777)!==0o700)throw new Error("MANIFEST_PARENT_CWD_IDENTITY");
const markerPath="./"+process.env.PARENT_MARKER,marker=lstatSync(markerPath);
if(!marker.isFile()||String(marker.uid)!==process.env.EFFECTIVE_UID||Number(marker.mode&0o777)!==0o600)throw new Error("MANIFEST_PARENT_MARKER_METADATA");
const markerRaw=readFileSync(markerPath),markerDigest=createHash("sha256").update(markerRaw).digest("hex"),markerValue=JSON.parse(markerRaw.toString("utf8"));
const markerKeys=["schema_version","record_stage","gate_purpose","private_parent","canonical_private_parent","parent_device","parent_inode","parent_type","owner_uid","mode"];
if(markerDigest!==process.env.EXPECTED_MARKER_DIGEST||Object.keys(markerValue).length!==markerKeys.length||markerKeys.some(key=>!Object.prototype.hasOwnProperty.call(markerValue,key)))throw new Error("MANIFEST_PARENT_MARKER_SCHEMA");
if(markerValue.schema_version!=="1"||markerValue.record_stage!=="PRIVATE_PARENT_PREPARED"||markerValue.gate_purpose!==process.env.GATE_PURPOSE||markerValue.private_parent!==process.env.LOGICAL_PARENT||markerValue.canonical_private_parent!==process.env.CANONICAL_PARENT||markerValue.parent_device!==String(parent.dev)||markerValue.parent_inode!==String(parent.ino)||markerValue.parent_type!=="Directory"||markerValue.owner_uid!==process.env.EFFECTIVE_UID||markerValue.mode!=="0700")throw new Error("MANIFEST_PARENT_MARKER_CONTENT");
if(process.env.MANIFEST_FINAL!=="./"+finalName||process.env.MANIFEST_TMP!=="./"+tmpName||!/^run-[0-9a-f]{64}\.manifest\.json$/.test(finalName)||tmpName!=="."+finalName+".tmp")throw new Error("MANIFEST_BASENAME");
const keys=["schema_version","record_stage","logical_runtime_evidence_identity","run_nonce","physical_root_path","canonical_physical_root_path","root_device","root_inode","root_type","private_parent_path","canonical_private_parent_path","private_parent_device","private_parent_inode","private_parent_type","private_parent_owner_uid","private_parent_mode","private_parent_marker_digest","root_ownership_marker_digest","run_start_timestamp","gate_purpose","expected_final_state","current_state","threat_boundary_version","filesystem_threat_boundary","strict_same_uid_race_proof","privileged_root_adversary_proof","atomic_mkdir_open_claim","run_root_creation_model","cleanup_state","legacy_fixed_root","legacy_fixed_root_disposition"];
const exact=value=>Object.keys(value).length===keys.length&&keys.every(key=>Object.prototype.hasOwnProperty.call(value,key));
const expectedBase={schema_version:"1",record_stage:"RUN_MANIFEST",logical_runtime_evidence_identity:process.env.LOGICAL_IDENTITY,run_nonce:process.env.RUN_NONCE,physical_root_path:process.env.PHYSICAL_ROOT,canonical_physical_root_path:process.env.CANONICAL_ROOT,root_device:process.env.ROOT_DEVICE,root_inode:process.env.ROOT_INODE,root_type:process.env.ROOT_TYPE,private_parent_path:process.env.PRIVATE_PARENT_PATH,canonical_private_parent_path:process.env.CANONICAL_PRIVATE_PARENT_PATH,private_parent_device:process.env.PRIVATE_PARENT_DEVICE,private_parent_inode:process.env.PRIVATE_PARENT_INODE,private_parent_type:process.env.PRIVATE_PARENT_TYPE,private_parent_owner_uid:process.env.PRIVATE_PARENT_OWNER_UID,private_parent_mode:process.env.PRIVATE_PARENT_MODE,private_parent_marker_digest:process.env.PRIVATE_PARENT_MARKER_DIGEST,root_ownership_marker_digest:process.env.ROOT_OWNERSHIP_MARKER_DIGEST,run_start_timestamp:process.env.RUN_START_TIMESTAMP,gate_purpose:process.env.GATE_PURPOSE,expected_final_state:process.env.EXPECTED_FINAL_STATE,threat_boundary_version:process.env.THREAT_BOUNDARY_VERSION,filesystem_threat_boundary:process.env.FILESYSTEM_THREAT_BOUNDARY,strict_same_uid_race_proof:process.env.STRICT_SAME_UID_RACE_PROOF,privileged_root_adversary_proof:process.env.PRIVILEGED_ROOT_ADVERSARY_PROOF,atomic_mkdir_open_claim:process.env.ATOMIC_MKDIR_OPEN_CLAIM,run_root_creation_model:process.env.RUN_ROOT_CREATION_MODEL,cleanup_state:"NOT_EXECUTED_NOT_AUTHORIZED",legacy_fixed_root:process.env.LEGACY_FIXED_ROOT,legacy_fixed_root_disposition:"OUTSIDE_OPTION_C_NAMESPACE_CLEANUP_NOT_AUTHORIZED"};
const present=path=>{try{return lstatSync(path);}catch(error){if(error?.code==="ENOENT")return null;throw error;}};
const tmpStat=present(tmpPath);if(tmpStat!==null)throw new Error("MANIFEST_TMP_PRESENT");
const finalStat=present(finalPath);
if(current==="NOT_PUBLISHED"){if(finalStat!==null)throw new Error("MANIFEST_UNEXPECTED_FINAL");if(target!=="ACTIVE"&&target!=="FAILURE")throw new Error("MANIFEST_INITIAL_TRANSITION");}
else if(current==="ACTIVE"){if(target!=="SUCCESS"&&target!=="FAILURE")throw new Error("MANIFEST_TERMINAL_TRANSITION");if(finalStat===null||!finalStat.isFile()||String(finalStat.uid)!==process.env.EFFECTIVE_UID||Number(finalStat.mode&0o777)!==0o600)throw new Error("MANIFEST_CURRENT_METADATA");const raw=readFileSync(finalPath),digest=createHash("sha256").update(raw).digest("hex"),value=JSON.parse(raw.toString("utf8"));if(digest!==expectedDigest||!exact(value)||value.current_state!=="ACTIVE")throw new Error("MANIFEST_CURRENT_AUTHORITY");for(const [key,expected] of Object.entries(expectedBase))if(value[key]!==expected)throw new Error("MANIFEST_CURRENT_MAPPING_"+key);}
else throw new Error("MANIFEST_ALREADY_TERMINAL");
const value={...expectedBase,current_state:target},payload=Buffer.from(JSON.stringify(value)+"\n"),writeFully=eval(process.env.FULL_WRITE_HELPER);let fd=-1;
try{fd=openSync(tmpPath,"wx",0o600);writeFully(fd,payload,writeSync);fsyncSync(fd);closeSync(fd);fd=-1;renameSync(tmpPath,finalPath);}catch(error){if(fd>=0)try{closeSync(fd);}catch{}throw error;}
let parentDurability="RECOMMENDATION:parent-directory-fsync-unproven",parentFd=-1;
try{parentFd=openSync(".","r");fsyncSync(parentFd);parentDurability="PASS";}catch(error){parentDurability="RECOMMENDATION:parent-directory-fsync:"+String(error?.code??"UNAVAILABLE");}finally{if(parentFd>=0)try{closeSync(parentFd);}catch(error){parentDurability="RECOMMENDATION:parent-directory-close:"+String(error?.code??"UNAVAILABLE");}}
const after=lstatSync(finalPath);if(!after.isFile()||String(after.uid)!==process.env.EFFECTIVE_UID||Number(after.mode&0o777)!==0o600||present(tmpPath)!==null)throw new Error("MANIFEST_PUBLISH_METADATA");
const finalRaw=readFileSync(finalPath),finalValue=JSON.parse(finalRaw.toString("utf8"));if(!exact(finalValue)||finalValue.current_state!==target)throw new Error("MANIFEST_PUBLISH_SCHEMA");for(const [key,expected] of Object.entries(expectedBase))if(finalValue[key]!==expected)throw new Error("MANIFEST_PUBLISH_MAPPING_"+key);
const digest=createHash("sha256").update(finalRaw).digest("hex");process.stdout.write((target==="SUCCESS"?"SUCCESS_COMMITTED":"PUBLISHED")+"|"+target+"|"+digest+"|"+parentDurability);
NODE
    )
  )
  manifest_helper_rc=$?
  if test "$manifest_helper_rc" -ne 0; then
    manifest_publication_result=UNCERTAIN
    return 2
  fi
  IFS='|' read -r manifest_helper_result manifest_helper_state manifest_helper_digest manifest_parent_fsync_result <<EOF
$manifest_parent_publish_output
EOF
  printf '%s\n' "$manifest_helper_digest" | /usr/bin/grep -Eq '^[0-9a-f]{64}$' || { manifest_publication_result=UNCERTAIN; return 2; }
  if test "$manifest_target_state" = SUCCESS; then
    test "$manifest_helper_result" = SUCCESS_COMMITTED && test "$manifest_helper_state" = SUCCESS || { manifest_publication_result=UNCERTAIN; return 2; }
  else
    test "$manifest_helper_result" = PUBLISHED && test "$manifest_helper_state" = "$manifest_target_state" || { manifest_publication_result=UNCERTAIN; return 2; }
  fi
  manifest_confirmed_digest=$manifest_helper_digest
  manifest_confirmed_state=$manifest_target_state
  manifest_publication_result=PASS
}

validate_manifest_mapping() {
  expected_manifest_state=$1
  case "$expected_manifest_state" in ACTIVE|SUCCESS|FAILURE) ;;
    *) return 1 ;;
  esac
  validate_root_binding || return 1
  validate_retained_root_visibility || return 1
  manifest_parent_validate_output=$(
    (
      cd -P "$private_parent" || exit 1
      MANIFEST_FINAL="./$manifest_basename" MANIFEST_TMP="./$manifest_tmp_basename" MANIFEST_BASENAME="$manifest_basename" MANIFEST_TMP_BASENAME="$manifest_tmp_basename" PARENT_DEVICE="$logical_parent_device" PARENT_INODE="$logical_parent_inode" EFFECTIVE_UID="$private_parent_effective_uid" PARENT_MARKER="$private_parent_marker" EXPECTED_MARKER_DIGEST="$private_parent_marker_digest" LOGICAL_PARENT="$private_parent" CANONICAL_PARENT="$canonical_parent" PRIVATE_PARENT_PATH="$private_parent_path" CANONICAL_PRIVATE_PARENT_PATH="$canonical_private_parent_path" PRIVATE_PARENT_DEVICE="$private_parent_device" PRIVATE_PARENT_INODE="$private_parent_inode" PRIVATE_PARENT_TYPE="$private_parent_type" PRIVATE_PARENT_OWNER_UID="$private_parent_owner_uid" PRIVATE_PARENT_MODE="$private_parent_mode" PRIVATE_PARENT_MARKER_DIGEST="$private_parent_marker_digest" ROOT_OWNERSHIP_MARKER_DIGEST="$root_ownership_marker_digest" GATE_PURPOSE="$gate_purpose" EXPECTED_STATE="$expected_manifest_state" EXPECTED_DIGEST="$manifest_confirmed_digest" LOGICAL_IDENTITY="$logical_evidence_identity" RUN_NONCE="$runtime_run_nonce" PHYSICAL_ROOT="$logical_root" CANONICAL_ROOT="$canonical_root" ROOT_DEVICE="$root_device" ROOT_INODE="$root_inode" ROOT_TYPE="$root_type" RUN_START_TIMESTAMP="$run_start_timestamp" EXPECTED_FINAL_STATE="$expected_final_state" THREAT_BOUNDARY_VERSION="$threat_boundary_version" FILESYSTEM_THREAT_BOUNDARY="$filesystem_threat_boundary" STRICT_SAME_UID_RACE_PROOF="$strict_same_uid_race_proof" PRIVILEGED_ROOT_ADVERSARY_PROOF="$privileged_root_adversary_proof" ATOMIC_MKDIR_OPEN_CLAIM="$atomic_mkdir_open_claim" RUN_ROOT_CREATION_MODEL="$run_root_creation_model" LEGACY_FIXED_ROOT="$legacy_fixed_root" node --input-type=module <<'NODE'
import {createHash} from "node:crypto";
import {lstatSync,readFileSync} from "node:fs";
const parent=lstatSync(".",{bigint:true});
if(!parent.isDirectory()||String(parent.dev)!==process.env.PARENT_DEVICE||String(parent.ino)!==process.env.PARENT_INODE||String(parent.uid)!==process.env.EFFECTIVE_UID||Number(parent.mode&0o777)!==0o700)throw new Error("MANIFEST_PARENT_CWD_IDENTITY");
const markerPath="./"+process.env.PARENT_MARKER,marker=lstatSync(markerPath,{bigint:true});
if(!marker.isFile()||String(marker.uid)!==process.env.EFFECTIVE_UID||Number(marker.mode&0o777)!==0o600)throw new Error("MANIFEST_PARENT_MARKER_METADATA");
const markerRaw=readFileSync(markerPath),markerDigest=createHash("sha256").update(markerRaw).digest("hex"),markerValue=JSON.parse(markerRaw.toString("utf8"));
const markerKeys=["schema_version","record_stage","gate_purpose","private_parent","canonical_private_parent","parent_device","parent_inode","parent_type","owner_uid","mode"];
if(markerDigest!==process.env.EXPECTED_MARKER_DIGEST||Object.keys(markerValue).length!==markerKeys.length||markerKeys.some(key=>!Object.prototype.hasOwnProperty.call(markerValue,key)))throw new Error("MANIFEST_PARENT_MARKER_SCHEMA");
if(markerValue.schema_version!=="1"||markerValue.record_stage!=="PRIVATE_PARENT_PREPARED"||markerValue.gate_purpose!==process.env.GATE_PURPOSE||markerValue.private_parent!==process.env.LOGICAL_PARENT||markerValue.canonical_private_parent!==process.env.CANONICAL_PARENT||markerValue.parent_device!==String(parent.dev)||markerValue.parent_inode!==String(parent.ino)||markerValue.parent_type!=="Directory"||markerValue.owner_uid!==process.env.EFFECTIVE_UID||markerValue.mode!=="0700")throw new Error("MANIFEST_PARENT_MARKER_CONTENT");
if(process.env.MANIFEST_FINAL!=="./"+process.env.MANIFEST_BASENAME||process.env.MANIFEST_TMP!=="./"+process.env.MANIFEST_TMP_BASENAME||!/^run-[0-9a-f]{64}\.manifest\.json$/.test(process.env.MANIFEST_BASENAME)||process.env.MANIFEST_TMP_BASENAME!=="."+process.env.MANIFEST_BASENAME+".tmp")throw new Error("MANIFEST_BASENAME");
const finalStat=lstatSync(process.env.MANIFEST_FINAL,{bigint:true});if(!finalStat.isFile()||String(finalStat.uid)!==process.env.EFFECTIVE_UID||Number(finalStat.mode&0o777n)!==0o600)throw new Error("MANIFEST_METADATA");
try{lstatSync(process.env.MANIFEST_TMP);throw new Error("MANIFEST_TMP_PRESENT");}catch(error){if(error?.code!=="ENOENT")throw error;}
const raw=readFileSync(process.env.MANIFEST_FINAL),digest=createHash("sha256").update(raw).digest("hex"),value=JSON.parse(raw.toString("utf8")),keys=["schema_version","record_stage","logical_runtime_evidence_identity","run_nonce","physical_root_path","canonical_physical_root_path","root_device","root_inode","root_type","private_parent_path","canonical_private_parent_path","private_parent_device","private_parent_inode","private_parent_type","private_parent_owner_uid","private_parent_mode","private_parent_marker_digest","root_ownership_marker_digest","run_start_timestamp","gate_purpose","expected_final_state","current_state","threat_boundary_version","filesystem_threat_boundary","strict_same_uid_race_proof","privileged_root_adversary_proof","atomic_mkdir_open_claim","run_root_creation_model","cleanup_state","legacy_fixed_root","legacy_fixed_root_disposition"];
if(digest!==process.env.EXPECTED_DIGEST||Object.keys(value).length!==keys.length||keys.some(key=>!Object.prototype.hasOwnProperty.call(value,key)))throw new Error("MANIFEST_SCHEMA_OR_DIGEST");
const expected={schema_version:"1",record_stage:"RUN_MANIFEST",logical_runtime_evidence_identity:process.env.LOGICAL_IDENTITY,run_nonce:process.env.RUN_NONCE,physical_root_path:process.env.PHYSICAL_ROOT,canonical_physical_root_path:process.env.CANONICAL_ROOT,root_device:process.env.ROOT_DEVICE,root_inode:process.env.ROOT_INODE,root_type:process.env.ROOT_TYPE,private_parent_path:process.env.PRIVATE_PARENT_PATH,canonical_private_parent_path:process.env.CANONICAL_PRIVATE_PARENT_PATH,private_parent_device:process.env.PRIVATE_PARENT_DEVICE,private_parent_inode:process.env.PRIVATE_PARENT_INODE,private_parent_type:process.env.PRIVATE_PARENT_TYPE,private_parent_owner_uid:process.env.PRIVATE_PARENT_OWNER_UID,private_parent_mode:process.env.PRIVATE_PARENT_MODE,private_parent_marker_digest:process.env.PRIVATE_PARENT_MARKER_DIGEST,root_ownership_marker_digest:process.env.ROOT_OWNERSHIP_MARKER_DIGEST,run_start_timestamp:process.env.RUN_START_TIMESTAMP,gate_purpose:process.env.GATE_PURPOSE,expected_final_state:process.env.EXPECTED_FINAL_STATE,current_state:process.env.EXPECTED_STATE,threat_boundary_version:process.env.THREAT_BOUNDARY_VERSION,filesystem_threat_boundary:process.env.FILESYSTEM_THREAT_BOUNDARY,strict_same_uid_race_proof:process.env.STRICT_SAME_UID_RACE_PROOF,privileged_root_adversary_proof:process.env.PRIVILEGED_ROOT_ADVERSARY_PROOF,atomic_mkdir_open_claim:process.env.ATOMIC_MKDIR_OPEN_CLAIM,run_root_creation_model:process.env.RUN_ROOT_CREATION_MODEL,cleanup_state:"NOT_EXECUTED_NOT_AUTHORIZED",legacy_fixed_root:process.env.LEGACY_FIXED_ROOT,legacy_fixed_root_disposition:"OUTSIDE_OPTION_C_NAMESPACE_CLEANUP_NOT_AUTHORIZED"};
for(const [key,expectedValue] of Object.entries(expected))if(value[key]!==expectedValue)throw new Error("MANIFEST_MAPPING_"+key);
process.stdout.write("VALID|"+value.current_state+"|"+digest);
NODE
    )
  )
  manifest_validate_rc=$?
  test "$manifest_validate_rc" -eq 0 || return 1
  IFS='|' read -r manifest_validate_result manifest_validate_state manifest_observed_digest <<EOF
$manifest_parent_validate_output
EOF
  test "$manifest_validate_result" = VALID && test "$manifest_validate_state" = "$expected_manifest_state" && test "$manifest_observed_digest" = "$manifest_confirmed_digest" || return 1
}

reconcile_manifest_after_publication_failure() {
  manifest_reconciliation_state=UNKNOWN
  manifest_reconcile_output=$(
    (
      cd -P "$private_parent" || exit 1
      MANIFEST_FINAL="./$manifest_basename" MANIFEST_TMP="./$manifest_tmp_basename" MANIFEST_BASENAME="$manifest_basename" MANIFEST_TMP_BASENAME="$manifest_tmp_basename" PARENT_DEVICE="$logical_parent_device" PARENT_INODE="$logical_parent_inode" EFFECTIVE_UID="$private_parent_effective_uid" PARENT_MARKER="$private_parent_marker" EXPECTED_MARKER_DIGEST="$private_parent_marker_digest" LOGICAL_PARENT="$private_parent" CANONICAL_PARENT="$canonical_parent" PRIVATE_PARENT_PATH="$private_parent_path" CANONICAL_PRIVATE_PARENT_PATH="$canonical_private_parent_path" PRIVATE_PARENT_DEVICE="$private_parent_device" PRIVATE_PARENT_INODE="$private_parent_inode" PRIVATE_PARENT_TYPE="$private_parent_type" PRIVATE_PARENT_OWNER_UID="$private_parent_owner_uid" PRIVATE_PARENT_MODE="$private_parent_mode" PRIVATE_PARENT_MARKER_DIGEST="$private_parent_marker_digest" ROOT_OWNERSHIP_MARKER_DIGEST="$root_ownership_marker_digest" GATE_PURPOSE="$gate_purpose" LOGICAL_IDENTITY="$logical_evidence_identity" RUN_NONCE="$runtime_run_nonce" PHYSICAL_ROOT="$logical_root" CANONICAL_ROOT="$canonical_root" ROOT_DEVICE="$root_device" ROOT_INODE="$root_inode" ROOT_TYPE="$root_type" RUN_START_TIMESTAMP="$run_start_timestamp" EXPECTED_FINAL_STATE="$expected_final_state" THREAT_BOUNDARY_VERSION="$threat_boundary_version" FILESYSTEM_THREAT_BOUNDARY="$filesystem_threat_boundary" STRICT_SAME_UID_RACE_PROOF="$strict_same_uid_race_proof" PRIVILEGED_ROOT_ADVERSARY_PROOF="$privileged_root_adversary_proof" ATOMIC_MKDIR_OPEN_CLAIM="$atomic_mkdir_open_claim" RUN_ROOT_CREATION_MODEL="$run_root_creation_model" LEGACY_FIXED_ROOT="$legacy_fixed_root" node --input-type=module <<'NODE'
import {createHash} from "node:crypto";
import {lstatSync,readFileSync} from "node:fs";
const parent=lstatSync(".",{bigint:true});
if(!parent.isDirectory()||String(parent.dev)!==process.env.PARENT_DEVICE||String(parent.ino)!==process.env.PARENT_INODE||String(parent.uid)!==process.env.EFFECTIVE_UID||Number(parent.mode&0o777)!==0o700)throw new Error("MANIFEST_PARENT_CWD_IDENTITY");
const markerPath="./"+process.env.PARENT_MARKER,marker=lstatSync(markerPath,{bigint:true});
if(!marker.isFile()||String(marker.uid)!==process.env.EFFECTIVE_UID||Number(marker.mode&0o777)!==0o600)throw new Error("MANIFEST_PARENT_MARKER_METADATA");
const markerRaw=readFileSync(markerPath),markerDigest=createHash("sha256").update(markerRaw).digest("hex"),markerValue=JSON.parse(markerRaw.toString("utf8"));
const markerKeys=["schema_version","record_stage","gate_purpose","private_parent","canonical_private_parent","parent_device","parent_inode","parent_type","owner_uid","mode"];
if(markerDigest!==process.env.EXPECTED_MARKER_DIGEST||Object.keys(markerValue).length!==markerKeys.length||markerKeys.some(key=>!Object.prototype.hasOwnProperty.call(markerValue,key)))throw new Error("MANIFEST_PARENT_MARKER_SCHEMA");
if(markerValue.schema_version!=="1"||markerValue.record_stage!=="PRIVATE_PARENT_PREPARED"||markerValue.gate_purpose!==process.env.GATE_PURPOSE||markerValue.private_parent!==process.env.LOGICAL_PARENT||markerValue.canonical_private_parent!==process.env.CANONICAL_PARENT||markerValue.parent_device!==String(parent.dev)||markerValue.parent_inode!==String(parent.ino)||markerValue.parent_type!=="Directory"||markerValue.owner_uid!==process.env.EFFECTIVE_UID||markerValue.mode!=="0700")throw new Error("MANIFEST_PARENT_MARKER_CONTENT");
if(process.env.MANIFEST_FINAL!=="./"+process.env.MANIFEST_BASENAME||process.env.MANIFEST_TMP!=="./"+process.env.MANIFEST_TMP_BASENAME||!/^run-[0-9a-f]{64}\.manifest\.json$/.test(process.env.MANIFEST_BASENAME)||process.env.MANIFEST_TMP_BASENAME!=="."+process.env.MANIFEST_BASENAME+".tmp")throw new Error("MANIFEST_BASENAME");
const present=path=>{try{return lstatSync(path,{bigint:true});}catch(error){if(error?.code==="ENOENT")return null;throw error;}};
const tmp=present(process.env.MANIFEST_TMP);if(tmp!==null)process.stdout.write("UNKNOWN|MANIFEST_TMP_PRESENT");
else{
  const final=present(process.env.MANIFEST_FINAL);
  if(final===null||!final.isFile()||String(final.uid)!==process.env.EFFECTIVE_UID||Number(final.mode&0o777n)!==0o600)process.stdout.write("UNKNOWN|MANIFEST_FINAL_MISSING_OR_METADATA");
  else{
    try{
      const raw=readFileSync(process.env.MANIFEST_FINAL),digest=createHash("sha256").update(raw).digest("hex"),value=JSON.parse(raw.toString("utf8")),keys=["schema_version","record_stage","logical_runtime_evidence_identity","run_nonce","physical_root_path","canonical_physical_root_path","root_device","root_inode","root_type","private_parent_path","canonical_private_parent_path","private_parent_device","private_parent_inode","private_parent_type","private_parent_owner_uid","private_parent_mode","private_parent_marker_digest","root_ownership_marker_digest","run_start_timestamp","gate_purpose","expected_final_state","current_state","threat_boundary_version","filesystem_threat_boundary","strict_same_uid_race_proof","privileged_root_adversary_proof","atomic_mkdir_open_claim","run_root_creation_model","cleanup_state","legacy_fixed_root","legacy_fixed_root_disposition"];
      const exact=Object.keys(value).length===keys.length&&keys.every(key=>Object.prototype.hasOwnProperty.call(value,key));
      const expected={schema_version:"1",record_stage:"RUN_MANIFEST",logical_runtime_evidence_identity:process.env.LOGICAL_IDENTITY,run_nonce:process.env.RUN_NONCE,physical_root_path:process.env.PHYSICAL_ROOT,canonical_physical_root_path:process.env.CANONICAL_ROOT,root_device:process.env.ROOT_DEVICE,root_inode:process.env.ROOT_INODE,root_type:process.env.ROOT_TYPE,private_parent_path:process.env.PRIVATE_PARENT_PATH,canonical_private_parent_path:process.env.CANONICAL_PRIVATE_PARENT_PATH,private_parent_device:process.env.PRIVATE_PARENT_DEVICE,private_parent_inode:process.env.PRIVATE_PARENT_INODE,private_parent_type:process.env.PRIVATE_PARENT_TYPE,private_parent_owner_uid:process.env.PRIVATE_PARENT_OWNER_UID,private_parent_mode:process.env.PRIVATE_PARENT_MODE,private_parent_marker_digest:process.env.PRIVATE_PARENT_MARKER_DIGEST,root_ownership_marker_digest:process.env.ROOT_OWNERSHIP_MARKER_DIGEST,run_start_timestamp:process.env.RUN_START_TIMESTAMP,gate_purpose:process.env.GATE_PURPOSE,expected_final_state:process.env.EXPECTED_FINAL_STATE,threat_boundary_version:process.env.THREAT_BOUNDARY_VERSION,filesystem_threat_boundary:process.env.FILESYSTEM_THREAT_BOUNDARY,strict_same_uid_race_proof:process.env.STRICT_SAME_UID_RACE_PROOF,privileged_root_adversary_proof:process.env.PRIVILEGED_ROOT_ADVERSARY_PROOF,atomic_mkdir_open_claim:process.env.ATOMIC_MKDIR_OPEN_CLAIM,run_root_creation_model:process.env.RUN_ROOT_CREATION_MODEL,cleanup_state:"NOT_EXECUTED_NOT_AUTHORIZED",legacy_fixed_root:process.env.LEGACY_FIXED_ROOT,legacy_fixed_root_disposition:"OUTSIDE_OPTION_C_NAMESPACE_CLEANUP_NOT_AUTHORIZED"};
      const mapping=exact&&digest.length===64&&["ACTIVE","SUCCESS","FAILURE"].includes(value.current_state)&&Object.entries(expected).every(entry=>value[entry[0]]===entry[1]);
      process.stdout.write(mapping?"RECONCILED|"+value.current_state+"|"+digest:"UNKNOWN|MANIFEST_SCHEMA_OR_MAPPING");
    }catch(error){process.stdout.write("UNKNOWN|MANIFEST_READ_OR_PARSE");}
  }
}
NODE
    )
  )
  manifest_reconcile_rc=$?
  if test "$manifest_reconcile_rc" -ne 0; then
    manifest_confirmed_state=UNKNOWN
    manifest_confirmed_digest=UNKNOWN
    manifest_reconciliation_state=UNKNOWN
    return 1
  fi
  IFS='|' read -r manifest_reconcile_result manifest_reconcile_state manifest_reconcile_digest <<EOF
$manifest_reconcile_output
EOF
  case "$manifest_reconcile_result" in
    RECONCILED)
      printf '%s\n' "$manifest_reconcile_digest" | /usr/bin/grep -Eq '^[0-9a-f]{64}$' || { manifest_confirmed_state=UNKNOWN; manifest_confirmed_digest=UNKNOWN; manifest_reconciliation_state=UNKNOWN; return 1; }
      manifest_confirmed_state=$manifest_reconcile_state
      manifest_confirmed_digest=$manifest_reconcile_digest
      manifest_reconciliation_state=$manifest_reconcile_state
      return 0
      ;;
    UNKNOWN)
      manifest_confirmed_state=UNKNOWN
      manifest_confirmed_digest=UNKNOWN
      manifest_reconciliation_state=UNKNOWN
      return 1
      ;;
    *) manifest_confirmed_state=UNKNOWN; manifest_confirmed_digest=UNKNOWN; manifest_reconciliation_state=UNKNOWN; return 1 ;;
  esac
}

set_role_state() {
  case "$1" in
    capture) capture_state=$2 ;;
    phase_a_next) phase_a_state=$2 ;;
    phase_b_next) phase_b_state=$2 ;;
    *) return 1 ;;
  esac
}

record_wait_status() {
  wait_role=$1
  wait_status_value=$2
  case "$wait_role" in
    capture) capture_wait_status=$wait_status_value ;;
    phase_a_next) phase_a_wait_status=$wait_status_value ;;
    phase_b_next) phase_b_wait_status=$wait_status_value ;;
    *) return 1 ;;
  esac
  printf 'cleanup role=%s wait_status=%s\n' "$wait_role" "$wait_status_value" >> "$(root_artifact_path process-identities.txt)"
}

register_candidate() {
  candidate_role=$1
  candidate_launch_pid=$2
  candidate_marker=$3
  candidate_generation=$4
  test -n "$runtime_run_nonce" || return 1
  case "$candidate_role" in
    capture)
      capture_pid=$candidate_launch_pid; capture_candidate_pid=$candidate_launch_pid; capture_ppid=$$; capture_candidate_ppid=$$; capture_role=capture; capture_candidate_role=capture; capture_candidate_generation=$candidate_generation; capture_launch_generation=$candidate_generation; capture_candidate_run_nonce=$runtime_run_nonce; capture_candidate_marker=$candidate_marker; capture_request_phase=no; capture_state=LAUNCHED_CANDIDATE ;;
    phase_a_next)
      phase_a_pid=$candidate_launch_pid; phase_a_candidate_pid=$candidate_launch_pid; phase_a_ppid=$$; phase_a_candidate_ppid=$$; phase_a_role=phase_a_next; phase_a_candidate_role=phase_a_next; phase_a_candidate_generation=$candidate_generation; phase_a_launch_generation=$candidate_generation; phase_a_candidate_run_nonce=$runtime_run_nonce; phase_a_candidate_marker=$candidate_marker; phase_a_request_phase=no; phase_a_state=LAUNCHED_CANDIDATE ;;
    phase_b_next)
      phase_b_pid=$candidate_launch_pid; phase_b_candidate_pid=$candidate_launch_pid; phase_b_ppid=$$; phase_b_candidate_ppid=$$; phase_b_role=phase_b_next; phase_b_candidate_role=phase_b_next; phase_b_candidate_generation=$candidate_generation; phase_b_launch_generation=$candidate_generation; phase_b_candidate_run_nonce=$runtime_run_nonce; phase_b_candidate_marker=$candidate_marker; phase_b_request_phase=no; phase_b_state=LAUNCHED_CANDIDATE ;;
    *) return 1 ;;
  esac
  printf 'candidate_role=%s\ncandidate_pid=%s\nlaunch_parent_shell_pid=%s\nlaunch_generation=%s\nrun_nonce=%s\nexact_argv_marker=%s\ncandidate_state=LAUNCHED_CANDIDATE\nrequest_phase=no\n' \
    "$candidate_role" "$candidate_launch_pid" "$$" "$candidate_generation" "$runtime_run_nonce" "$candidate_marker" >> "$(root_artifact_path process-identities.txt)"
}

construct_launch_marker() {
  marker_role=$1
  marker_generation=$2
  test -n "$runtime_run_nonce" || return 1
  case "$marker_role" in
    capture|phase_a_next|phase_b_next) ;;
    *) return 1 ;;
  esac
  constructed_marker="edge-mes-dashboard-url-runtime-evidence.${runtime_run_nonce}.${marker_role}.${marker_generation}"
  case "$constructed_marker" in
    *[[:space:]]*) return 1 ;;
  esac
  return 0
}

observed_argv_matches_role() {
  observed_role=$1
  observed_argv_value=$2
  expected_marker=$3
  observed_last_argv_token=${observed_argv_value##* }
  test "$observed_last_argv_token" = "$expected_marker" || return 1
  observed_argv_without_last=${observed_argv_value% *}
  test "${observed_argv_without_last##* }" = "--" || return 1
  case "$observed_role" in
    capture)
      case "$observed_argv_without_last" in
        node\ --input-type=module\ --eval\ *) return 0 ;;
        */node\ --input-type=module\ --eval\ *) return 0 ;;
        *) return 1 ;;
      esac
      ;;
    phase_a_next|phase_b_next)
      case "$observed_argv_without_last" in
        node\ server.js\ --) return 0 ;;
        */node\ server.js\ --) return 0 ;;
        *) return 1 ;;
      esac
      ;;
    *) return 1 ;;
  esac
}

read_identity() {
  observed_pid=$(/bin/ps -p "$1" -o pid= 2>/dev/null | /usr/bin/tr -d ' ')
  observed_ppid=$(/bin/ps -p "$1" -o ppid= 2>/dev/null | /usr/bin/tr -d ' ')
  observed_start=$(/bin/ps -ww -p "$1" -o lstart= 2>/dev/null | /usr/bin/sed 's/^ *//;s/ *$//')
  observed_argv=$(/bin/ps -ww -p "$1" -o command= 2>/dev/null | /usr/bin/sed 's/^ *//;s/ *$//')
  test "$observed_pid" = "$1" && test -n "$observed_ppid" && test -n "$observed_start" && test -n "$observed_argv" || return 1
  observed_digest=$(printf 'pid=%s\nppid=%s\nstart=%s\nargv=%s\n' "$observed_pid" "$observed_ppid" "$observed_start" "$observed_argv" | /usr/bin/shasum -a 256 | /usr/bin/awk '{print $1}')
  test -n "$observed_digest"
}

record_identity() {
  role=$1
  candidate_pid=$2
  read_identity "$candidate_pid" || return 1
  test "$observed_ppid" = "$$" || return 1
  case "$role" in
    capture)
      capture_pid=$observed_pid; capture_ppid=$observed_ppid; capture_start=$observed_start; capture_argv=$observed_argv; capture_digest=$observed_digest; capture_state=IDENTITY_CAPTURED ;;
    phase_a_next)
      phase_a_pid=$observed_pid; phase_a_ppid=$observed_ppid; phase_a_start=$observed_start; phase_a_argv=$observed_argv; phase_a_digest=$observed_digest; phase_a_state=IDENTITY_CAPTURED ;;
    phase_b_next)
      phase_b_pid=$observed_pid; phase_b_ppid=$observed_ppid; phase_b_start=$observed_start; phase_b_argv=$observed_argv; phase_b_digest=$observed_digest; phase_b_state=IDENTITY_CAPTURED ;;
    *) return 1 ;;
  esac
  printf 'role=%s\nlaunch_parent_shell_pid=%s\npid=%s\nppid=%s\nstart=%s\nargv=%s\ndigest=%s\n' \
    "$role" "$$" "$observed_pid" "$observed_ppid" "$observed_start" "$observed_argv" "$observed_digest" >> "$(root_artifact_path process-identities.txt)" || return 1
  return 0
}

candidate_identity_matches() {
  candidate_role=$1
  case "$candidate_role" in
    capture) candidate_pid=$capture_candidate_pid; candidate_ppid=$capture_candidate_ppid; candidate_generation=$capture_candidate_generation; current_role_generation=$capture_launch_generation; candidate_run_nonce=$capture_candidate_run_nonce; candidate_role_name=$capture_candidate_role; candidate_marker=$capture_candidate_marker; candidate_state=$capture_state; candidate_request_phase=$capture_request_phase ;;
    phase_a_next) candidate_pid=$phase_a_candidate_pid; candidate_ppid=$phase_a_candidate_ppid; candidate_generation=$phase_a_candidate_generation; current_role_generation=$phase_a_launch_generation; candidate_run_nonce=$phase_a_candidate_run_nonce; candidate_role_name=$phase_a_candidate_role; candidate_marker=$phase_a_candidate_marker; candidate_state=$phase_a_state; candidate_request_phase=$phase_a_request_phase ;;
    phase_b_next) candidate_pid=$phase_b_candidate_pid; candidate_ppid=$phase_b_candidate_ppid; candidate_generation=$phase_b_candidate_generation; current_role_generation=$phase_b_launch_generation; candidate_run_nonce=$phase_b_candidate_run_nonce; candidate_role_name=$phase_b_candidate_role; candidate_marker=$phase_b_candidate_marker; candidate_state=$phase_b_state; candidate_request_phase=$phase_b_request_phase ;;
    *) return 2 ;;
  esac
  test "$candidate_state" = LAUNCHED_CANDIDATE || test "$candidate_state" = UNRESOLVED || return 2
  test "$candidate_request_phase" = no && test "$candidate_role_name" = "$candidate_role" && test "$candidate_generation" = "$current_role_generation" && test "$candidate_run_nonce" = "$runtime_run_nonce" && test -n "$candidate_pid" && test -n "$candidate_marker" || return 2
  construct_launch_marker "$candidate_role" "$current_role_generation" || return 2
  test "$candidate_marker" = "$constructed_marker" || return 2
  kill -0 "$candidate_pid" 2>/dev/null || return 3
  read_identity "$candidate_pid" || return 1
  test "$observed_pid" = "$candidate_pid" && test "$observed_ppid" = "$candidate_ppid" && \
    observed_argv_matches_role "$candidate_role" "$observed_argv" "$constructed_marker"
}

identity_matches() {
  role=$1
  case "$role" in
    capture) expected_pid=$capture_pid; expected_ppid=$capture_ppid; expected_start=$capture_start; expected_argv=$capture_argv; expected_digest=$capture_digest ;;
    phase_a_next) expected_pid=$phase_a_pid; expected_ppid=$phase_a_ppid; expected_start=$phase_a_start; expected_argv=$phase_a_argv; expected_digest=$phase_a_digest ;;
    phase_b_next) expected_pid=$phase_b_pid; expected_ppid=$phase_b_ppid; expected_start=$phase_b_start; expected_argv=$phase_b_argv; expected_digest=$phase_b_digest ;;
    *) return 2 ;;
  esac
  kill -0 "$expected_pid" 2>/dev/null || return 3
  read_identity "$expected_pid" || return 1
  test "$observed_pid" = "$expected_pid" && test "$observed_ppid" = "$expected_ppid" && \
    test "$observed_start" = "$expected_start" && test "$observed_argv" = "$expected_argv" && \
    test "$observed_digest" = "$expected_digest"
}

record_listener_state() {
  role=$1
  pid=$2
  port=$3
  listener_state_result=NOT_CHECKED
  listener_evidence_write_result=NOT_CHECKED
  listener_output=$(/usr/sbin/lsof -nP -a -p "$pid" -iTCP:"$port" -sTCP:LISTEN 2>&1)
  listener_rc=$?
  if test "$listener_rc" -eq 0; then listener_state_result=PRESENT
  elif test "$listener_rc" -eq 1 && test -z "$listener_output"; then listener_state_result=ABSENT
  else listener_state_result=LSOF_FAILURE
  fi
  printf 'listener role=%s state=%s rc=%s output=%s\n' "$role" "$listener_state_result" "$listener_rc" "$listener_output" >> "$(root_artifact_path process-identities.txt)"
  listener_append_rc=$?
  if test "$listener_append_rc" -ne 0; then
    listener_evidence_write_result=EVIDENCE_WRITE_FAILURE
    listener_state_result=EVIDENCE_WRITE_FAILURE
    return 1
  fi
  listener_evidence_write_result=EVIDENCE_WRITE_SUCCESS
  return 0
}

record_line_value_safe() {
  case "$1" in
    *$'\n'*|*$'\r'*) return 1 ;;
    *) return 0 ;;
  esac
}

emit_evidence_summary_expected_record() {
  test "$summary_expected_frozen" = yes || return 1
  printf 'schema_version=%s\n' "$summary_expected_schema_version"
  printf 'record_stage=%s\n' "$summary_expected_record_stage"
  printf 'summary_state=%s\n' "$summary_expected_summary_state"
  printf 'logical_runtime_evidence_identity=%s\nrun_nonce=%s\nrun_start_timestamp=%s\ngate_purpose=%s\n' "$summary_expected_logical_runtime_evidence_identity" "$summary_expected_run_nonce" "$summary_expected_run_start_timestamp" "$summary_expected_gate_purpose"
  printf 'logical_root=%s\ncanonical_root=%s\nroot_device=%s\nroot_inode=%s\nroot_type=%s\n' "$summary_expected_logical_root" "$summary_expected_canonical_root" "$summary_expected_root_device" "$summary_expected_root_inode" "$summary_expected_root_type"
  printf 'private_parent=%s\ncanonical_private_parent=%s\nprivate_parent_device=%s\nprivate_parent_inode=%s\nprivate_parent_type=%s\nprivate_parent_owner_uid=%s\nprivate_parent_mode=%s\n' "$summary_expected_private_parent" "$summary_expected_canonical_private_parent" "$summary_expected_private_parent_device" "$summary_expected_private_parent_inode" "$summary_expected_private_parent_type" "$summary_expected_private_parent_owner_uid" "$summary_expected_private_parent_mode"
  printf 'private_parent_marker_digest=%s\nroot_ownership_marker_digest=%s\n' "$summary_expected_private_parent_marker_digest" "$summary_expected_root_ownership_marker_digest"
  printf 'manifest_report_path=%s\nmanifest_state_at_summary=%s\nmanifest_digest_at_summary=%s\nmanifest_publication_result=%s\nmanifest_reconciliation_state_at_summary=%s\n' "$summary_expected_manifest_report_path" "$summary_expected_manifest_state_at_summary" "$summary_expected_manifest_digest_at_summary" "$summary_expected_manifest_publication_result" "$summary_expected_manifest_reconciliation_state_at_summary"
  printf 'filesystem_threat_boundary=%s\nstrict_same_uid_race_proof=%s\nprivileged_root_adversary_proof=%s\natomic_mkdir_open_claim=%s\nrun_root_creation_model=%s\n' "$summary_expected_filesystem_threat_boundary" "$summary_expected_strict_same_uid_race_proof" "$summary_expected_privileged_root_adversary_proof" "$summary_expected_atomic_mkdir_open_claim" "$summary_expected_run_root_creation_model"
  printf 'cleanup_state=%s\nlegacy_fixed_root=%s\nlegacy_fixed_root_disposition=%s\n' "$summary_expected_cleanup_state" "$summary_expected_legacy_fixed_root" "$summary_expected_legacy_fixed_root_disposition"
  printf 'A_evidence_boundary=%s\nB_evidence_boundary=%s\nC_evidence_boundary=%s\nD_evidence_boundary=%s\n' "$summary_expected_A_evidence_boundary" "$summary_expected_B_evidence_boundary" "$summary_expected_C_evidence_boundary" "$summary_expected_D_evidence_boundary"
  printf 'phase_a_capture_state=%s\nphase_b_capture_state=%s\nrequest_method_path_host_query=%s\n' "$summary_expected_phase_a_capture_state" "$summary_expected_phase_b_capture_state" "$summary_expected_request_method_path_host_query"
  printf 'phase_a_pid=%s\nphase_b_pid=%s\ncapture_pid=%s\nnext_port_release=%s\ncapture_port_release=%s\n' "$summary_expected_phase_a_pid" "$summary_expected_phase_b_pid" "$summary_expected_capture_pid" "$summary_expected_next_port_release" "$summary_expected_capture_port_release"
  printf 'build_id=%s\nserver_js_sha256=%s\nfixture_sha256=%s\nserved_body_sha256=%s\npost_request_fixture_sha256=%s\nfixture_lineage_result=%s\nresponse_completion_evidence=%s\nitem_count=%s\nitem_key_count=%s\nartifact_ownership=%s\nartifact_postcondition=%s\n' "$summary_expected_build_id" "$summary_expected_server_js_sha256" "$summary_expected_fixture_sha256" "$summary_expected_served_body_sha256" "$summary_expected_post_request_fixture_sha256" "$summary_expected_fixture_lineage_result" "$summary_expected_response_completion_evidence" "$summary_expected_item_count" "$summary_expected_item_key_count" "$summary_expected_artifact_ownership" "$summary_expected_artifact_postcondition"
}

freeze_evidence_summary_values() {
  summary_expected_frozen=no
  validate_root_identity || return 1
  test "$manifest_confirmed_state" = ACTIVE && test "$manifest_publication_result" = PASS && test "$manifest_reconciliation_state" = NOT_RUN || return 1
  test "$gate_purpose" = DASHBOARD_PRODUCTION_URL_RESOLUTION_RUNTIME_EVIDENCE || return 1
  test "$run_root_creation_model" = EXCLUSIVE_UNPREDICTABLE_BASENAME_WITH_CWD_OBJECT_BINDING || return 1
  test "$legacy_fixed_root" = /tmp/edge-mes-dashboard-url-runtime-evidence || return 1
  test "$filesystem_threat_boundary" = T1_T2_T3 && test "$strict_same_uid_race_proof" = NOT_CLAIMED && test "$privileged_root_adversary_proof" = NOT_CLAIMED && test "$atomic_mkdir_open_claim" = NOT_CLAIMED || return 1
  for summary_digest_value in "$manifest_confirmed_digest" "$private_parent_marker_digest" "$root_ownership_marker_digest" "$expected_server_sha" "$expected_fixture_sha256" "$post_request_fixture_sha256"; do
    printf '%s\n' "$summary_digest_value" | /usr/bin/grep -Eq '^[0-9a-f]{64}$' || return 1
  done
  test "$post_request_fixture_sha256" = "$expected_fixture_sha256" && test "$fixture_lineage_result" = PASS && test "$capture_response_evidence_state" = RESPONSE_COMPLETE || return 1
  test "$port_release_result_next" = released && test "$port_release_result_capture" = released || return 1
  test "$ownership_verification_result" = PASS && test "$postcondition_result" = PASS || return 1
  for summary_pid_value in "$phase_a_pid" "$phase_b_pid" "$capture_pid"; do
    printf '%s\n' "$summary_pid_value" | /usr/bin/grep -Eq '^[1-9][0-9]*$' || return 1
  done
  test "$phase_a_pid" != "$phase_b_pid" && test "$phase_a_pid" != "$capture_pid" && test "$phase_b_pid" != "$capture_pid" || return 1

  summary_expected_schema_version=1
  summary_expected_record_stage=PRE_TERMINAL_SUCCESS_EVIDENCE
  summary_expected_summary_state=READY_TO_COMMIT_SUCCESS
  summary_expected_logical_runtime_evidence_identity=$logical_evidence_identity
  summary_expected_run_nonce=$runtime_run_nonce
  summary_expected_run_start_timestamp=$run_start_timestamp
  summary_expected_gate_purpose=$gate_purpose
  summary_expected_logical_root=$logical_root
  summary_expected_canonical_root=$canonical_root
  summary_expected_root_device=$root_device
  summary_expected_root_inode=$root_inode
  summary_expected_root_type=$root_type
  summary_expected_private_parent=$private_parent_path
  summary_expected_canonical_private_parent=$canonical_private_parent_path
  summary_expected_private_parent_device=$private_parent_device
  summary_expected_private_parent_inode=$private_parent_inode
  summary_expected_private_parent_type=$private_parent_type
  summary_expected_private_parent_owner_uid=$private_parent_owner_uid
  summary_expected_private_parent_mode=$private_parent_mode
  summary_expected_private_parent_marker_digest=$private_parent_marker_digest
  summary_expected_root_ownership_marker_digest=$root_ownership_marker_digest
  summary_expected_manifest_report_path=$logical_manifest_report_path
  summary_expected_manifest_state_at_summary=ACTIVE
  summary_expected_manifest_digest_at_summary=$manifest_confirmed_digest
  summary_expected_manifest_publication_result=PASS
  summary_expected_manifest_reconciliation_state_at_summary=NOT_RUN
  summary_expected_filesystem_threat_boundary=$filesystem_threat_boundary
  summary_expected_strict_same_uid_race_proof=$strict_same_uid_race_proof
  summary_expected_privileged_root_adversary_proof=$privileged_root_adversary_proof
  summary_expected_atomic_mkdir_open_claim=$atomic_mkdir_open_claim
  summary_expected_run_root_creation_model=$run_root_creation_model
  summary_expected_cleanup_state=NOT_EXECUTED_NOT_AUTHORIZED
  summary_expected_legacy_fixed_root=$legacy_fixed_root
  summary_expected_legacy_fixed_root_disposition=OUTSIDE_OPTION_C_NAMESPACE_CLEANUP_NOT_AUTHORIZED
  summary_expected_A_evidence_boundary=TRANSPORT_REQUEST_ONLY
  summary_expected_B_evidence_boundary=FROZEN_SYNTHETIC_FIXTURE_BYTE_LINEAGE_ONLY
  summary_expected_C_evidence_boundary=NOT_EXECUTED_NOT_CLAIMED
  summary_expected_D_evidence_boundary=FILESYSTEM_T1_T3_ONLY_T4_T5_NON_CLAIM
  summary_expected_phase_a_capture_state='LISTENING count=0 log=0 PASS'
  summary_expected_phase_b_capture_state='TARGET_REQUEST_COMPLETE count=1 log=1 PASS'
  summary_expected_request_method_path_host_query='GET /api/v2/production/accepted-station-events host=127.0.0.1:3100 five_decoded_query_pairs'
  summary_expected_phase_a_pid=$phase_a_pid
  summary_expected_phase_b_pid=$phase_b_pid
  summary_expected_capture_pid=$capture_pid
  summary_expected_next_port_release=$port_release_result_next
  summary_expected_capture_port_release=$port_release_result_capture
  summary_expected_build_id=$expected_build_id
  summary_expected_server_js_sha256=$expected_server_sha
  summary_expected_fixture_sha256=$expected_fixture_sha256
  summary_expected_served_body_sha256=$expected_fixture_sha256
  summary_expected_post_request_fixture_sha256=$post_request_fixture_sha256
  summary_expected_fixture_lineage_result=$fixture_lineage_result
  summary_expected_response_completion_evidence=$capture_response_evidence_state
  summary_expected_item_count=1
  summary_expected_item_key_count=22
  summary_expected_artifact_ownership=$ownership_verification_result
  summary_expected_artifact_postcondition=$postcondition_result

  for summary_line_value in \
    "$summary_expected_logical_runtime_evidence_identity" "$summary_expected_run_nonce" "$summary_expected_run_start_timestamp" "$summary_expected_gate_purpose" \
    "$summary_expected_logical_root" "$summary_expected_canonical_root" "$summary_expected_root_device" "$summary_expected_root_inode" \
    "$summary_expected_private_parent" "$summary_expected_canonical_private_parent" "$summary_expected_private_parent_device" "$summary_expected_private_parent_inode" "$summary_expected_private_parent_owner_uid" "$summary_expected_private_parent_mode" \
    "$summary_expected_private_parent_marker_digest" "$summary_expected_root_ownership_marker_digest" "$summary_expected_manifest_report_path" "$summary_expected_manifest_digest_at_summary" \
    "$summary_expected_legacy_fixed_root" "$summary_expected_phase_a_pid" "$summary_expected_phase_b_pid" "$summary_expected_capture_pid" "$summary_expected_build_id" \
    "$summary_expected_server_js_sha256" "$summary_expected_fixture_sha256" "$summary_expected_served_body_sha256" "$summary_expected_post_request_fixture_sha256"
  do
    record_line_value_safe "$summary_line_value" || return 1
  done
  summary_expected_frozen=yes
  summary_expected_payload=$(emit_evidence_summary_expected_record) || { summary_expected_frozen=no; return 1; }
  case "$summary_expected_payload" in *$'\r'*) summary_expected_frozen=no; return 1 ;; esac
  test "$(printf '%s\n' "$summary_expected_payload" | /usr/bin/awk 'END { print NR }')" = 57 || { summary_expected_frozen=no; return 1; }
  return 0
}

write_evidence_summary() {
  freeze_evidence_summary_values || return 1
  printf '%s\n' "$summary_expected_payload" | root_write_atomic_stdin evidence-summary.txt
}

validate_evidence_summary_readback() {
  test "$summary_expected_frozen" = yes && test -n "$summary_expected_payload" || return 1
  summary_path=$(root_artifact_path evidence-summary.txt) || return 1
  SUMMARY_PATH="$summary_path" SUMMARY_EXPECTED_PAYLOAD="$summary_expected_payload" node --input-type=module --eval '
import {lstatSync,readFileSync} from "node:fs";import {basename,dirname} from "node:path";
const path=process.env.SUMMARY_PATH,st=lstatSync(path,{bigint:true});
if(!st.isFile()||Number(st.mode&0o777n)!==0o600)throw new Error("SUMMARY_METADATA");
const raw=readFileSync(path,"utf8"),expectedRaw=process.env.SUMMARY_EXPECTED_PAYLOAD+"\n",forbidden=["final run state: "+"SUCCESS","manifest terminal state: "+"SUCCESS","runtime "+"SUCCESS"];
if(raw!==expectedRaw)throw new Error("SUMMARY_FROZEN_SOURCE_MISMATCH");
if(!raw.endsWith("\n")||forbidden.some(token=>raw.includes(token)))throw new Error("SUMMARY_TERMINAL_PROJECTION");
const keys=["schema_version","record_stage","summary_state","logical_runtime_evidence_identity","run_nonce","run_start_timestamp","gate_purpose","logical_root","canonical_root","root_device","root_inode","root_type","private_parent","canonical_private_parent","private_parent_device","private_parent_inode","private_parent_type","private_parent_owner_uid","private_parent_mode","private_parent_marker_digest","root_ownership_marker_digest","manifest_report_path","manifest_state_at_summary","manifest_digest_at_summary","manifest_publication_result","manifest_reconciliation_state_at_summary","filesystem_threat_boundary","strict_same_uid_race_proof","privileged_root_adversary_proof","atomic_mkdir_open_claim","run_root_creation_model","cleanup_state","legacy_fixed_root","legacy_fixed_root_disposition","A_evidence_boundary","B_evidence_boundary","C_evidence_boundary","D_evidence_boundary","phase_a_capture_state","phase_b_capture_state","request_method_path_host_query","phase_a_pid","phase_b_pid","capture_pid","next_port_release","capture_port_release","build_id","server_js_sha256","fixture_sha256","served_body_sha256","post_request_fixture_sha256","fixture_lineage_result","response_completion_evidence","item_count","item_key_count","artifact_ownership","artifact_postcondition"];
if(keys.length!==57)throw new Error("SUMMARY_DECLARED_FIELD_COUNT");
const lines=raw.slice(0,-1).split("\n");if(lines.length!==keys.length)throw new Error("SUMMARY_KEY_COUNT");
const value={};for(let i=0;i<lines.length;i++){const at=lines[i].indexOf("=");if(at<1)throw new Error("SUMMARY_LINE");const key=lines[i].slice(0,at);if(key!==keys[i]||Object.prototype.hasOwnProperty.call(value,key))throw new Error("SUMMARY_KEY_ORDER");value[key]=lines[i].slice(at+1);}
if(Object.keys(value).length!==57)throw new Error("SUMMARY_VALUE_COVERAGE");
const digest=/^[0-9a-f]{64}$/,positive=/^[1-9][0-9]*$/;
for(const key of ["private_parent_marker_digest","root_ownership_marker_digest","manifest_digest_at_summary","server_js_sha256","fixture_sha256","served_body_sha256","post_request_fixture_sha256"])if(!digest.test(value[key]))throw new Error("SUMMARY_DIGEST_"+key);
for(const key of ["phase_a_pid","phase_b_pid","capture_pid"])if(!positive.test(value[key]))throw new Error("SUMMARY_PID_"+key);
if(new Set([value.phase_a_pid,value.phase_b_pid,value.capture_pid]).size!==3)throw new Error("SUMMARY_PID_ROLE_RELATION");
if(value.manifest_state_at_summary!=="ACTIVE"||value.manifest_publication_result!=="PASS"||value.manifest_reconciliation_state_at_summary!=="NOT_RUN")throw new Error("SUMMARY_MANIFEST_RELATION");
if(!digest.test(value.run_nonce)||value.logical_runtime_evidence_identity!==`dashboard-production-url-resolution-runtime-evidence/${value.run_nonce}`)throw new Error("SUMMARY_RUN_IDENTITY_RELATION");
if(dirname(value.logical_root)!==value.private_parent||dirname(value.canonical_root)!==value.canonical_private_parent||basename(value.logical_root)!==`run-${value.run_nonce}`||basename(value.canonical_root)!==`run-${value.run_nonce}`)throw new Error("SUMMARY_ROOT_PARENT_RELATION");
if(dirname(value.manifest_report_path)!==value.private_parent||basename(value.manifest_report_path)!==`run-${value.run_nonce}.manifest.json`)throw new Error("SUMMARY_MANIFEST_PATH_RELATION");
if(!/^[0-9]+$/.test(value.root_device)||!/^[0-9]+$/.test(value.root_inode)||!/^[0-9]+$/.test(value.private_parent_device)||!/^[0-9]+$/.test(value.private_parent_inode)||!/^[0-9]+$/.test(value.private_parent_owner_uid)||value.root_type!=="Directory"||value.private_parent_type!=="Directory"||value.private_parent_mode!=="700")throw new Error("SUMMARY_OBJECT_IDENTITY_FORMAT");
if(value.gate_purpose!=="DASHBOARD_PRODUCTION_URL_RESOLUTION_RUNTIME_EVIDENCE"||value.run_root_creation_model!=="EXCLUSIVE_UNPREDICTABLE_BASENAME_WITH_CWD_OBJECT_BINDING"||value.legacy_fixed_root!=="/tmp/edge-mes-dashboard-url-runtime-evidence"||value.legacy_fixed_root_disposition!=="OUTSIDE_OPTION_C_NAMESPACE_CLEANUP_NOT_AUTHORIZED")throw new Error("SUMMARY_FIXED_AUTHORITY_RELATION");
if(value.build_id.length===0||/[\r\n]/.test(value.build_id))throw new Error("SUMMARY_BUILD_ID");
if(value.A_evidence_boundary!=="TRANSPORT_REQUEST_ONLY"||value.B_evidence_boundary!=="FROZEN_SYNTHETIC_FIXTURE_BYTE_LINEAGE_ONLY"||value.C_evidence_boundary!=="NOT_EXECUTED_NOT_CLAIMED"||value.D_evidence_boundary!=="FILESYSTEM_T1_T3_ONLY_T4_T5_NON_CLAIM")throw new Error("SUMMARY_BOUNDARY_RELATION");
if(value.phase_a_capture_state!=="LISTENING count=0 log=0 PASS"||value.phase_b_capture_state!=="TARGET_REQUEST_COMPLETE count=1 log=1 PASS"||value.request_method_path_host_query!=="GET /api/v2/production/accepted-station-events host=127.0.0.1:3100 five_decoded_query_pairs")throw new Error("SUMMARY_PHASE_REQUEST_RELATION");
if(value.next_port_release!=="released"||value.capture_port_release!=="released")throw new Error("SUMMARY_PORT_RELATION");
if(value.fixture_sha256!==value.served_body_sha256||value.fixture_sha256!==value.post_request_fixture_sha256)throw new Error("SUMMARY_FIXTURE_DIGEST_RELATION");
if(value.fixture_lineage_result!=="PASS"||value.response_completion_evidence!=="RESPONSE_COMPLETE"||value.item_count!=="1"||value.item_key_count!=="22")throw new Error("SUMMARY_FIXTURE_RESULT_RELATION");
if(value.artifact_ownership!=="PASS"||value.artifact_postcondition!=="PASS"||value.cleanup_state!=="NOT_EXECUTED_NOT_AUTHORIZED")throw new Error("SUMMARY_ARTIFACT_RETENTION_RELATION");
if(value.filesystem_threat_boundary!=="T1_T2_T3"||value.strict_same_uid_race_proof!=="NOT_CLAIMED"||value.privileged_root_adversary_proof!=="NOT_CLAIMED"||value.atomic_mkdir_open_claim!=="NOT_CLAIMED")throw new Error("SUMMARY_THREAT_BOUNDARY_RELATION");
'
}

emit_failure_state_expected_record() {
  test "$failure_expected_frozen" = yes || return 1
  printf 'schema_version=%s\nrecord_stage=%s\n' "$failure_expected_schema_version" "$failure_expected_record_stage"
  printf 'failure_code=%s\nfailure_reason=%s\ninterrupted=%s\nrun_nonce=%s\nlogical_runtime_evidence_identity=%s\nrun_start_timestamp=%s\ngate_purpose=%s\n' "$failure_expected_failure_code" "$failure_expected_failure_reason" "$failure_expected_interrupted" "$failure_expected_run_nonce" "$failure_expected_logical_runtime_evidence_identity" "$failure_expected_run_start_timestamp" "$failure_expected_gate_purpose"
  printf 'root_state=%s\nphysical_root_path=%s\ncanonical_physical_root_path=%s\nroot_device=%s\nroot_inode=%s\nroot_type=%s\n' "$failure_expected_root_state" "$failure_expected_physical_root_path" "$failure_expected_canonical_physical_root_path" "$failure_expected_root_device" "$failure_expected_root_inode" "$failure_expected_root_type"
  printf 'private_parent=%s\ncanonical_private_parent=%s\nprivate_parent_device=%s\nprivate_parent_inode=%s\nprivate_parent_type=%s\nprivate_parent_owner_uid=%s\nprivate_parent_mode=%s\nprivate_parent_marker_digest=%s\nroot_ownership_marker_digest=%s\n' "$failure_expected_private_parent" "$failure_expected_canonical_private_parent" "$failure_expected_private_parent_device" "$failure_expected_private_parent_inode" "$failure_expected_private_parent_type" "$failure_expected_private_parent_owner_uid" "$failure_expected_private_parent_mode" "$failure_expected_private_parent_marker_digest" "$failure_expected_root_ownership_marker_digest"
  printf 'logical_manifest_report_path=%s\ncanonical_manifest_report_path=%s\nmanifest_confirmed_state=%s\nmanifest_confirmed_digest=%s\nmanifest_publication_result=%s\nmanifest_reconciliation_state=%s\nmanifest_parent_fsync_result=%s\nterminal_commit_state=%s\nterminal_disposition=%s\ncleanup_state=%s\n' "$failure_expected_logical_manifest_report_path" "$failure_expected_canonical_manifest_report_path" "$failure_expected_manifest_confirmed_state" "$failure_expected_manifest_confirmed_digest" "$failure_expected_manifest_publication_result" "$failure_expected_manifest_reconciliation_state" "$failure_expected_manifest_parent_fsync_result" "$failure_expected_terminal_commit_state" "$failure_expected_terminal_disposition" "$failure_expected_cleanup_state"
  printf 'threat_boundary_version=%s\nfilesystem_threat_boundary=%s\nstrict_same_uid_race_proof=%s\nprivileged_root_adversary_proof=%s\natomic_mkdir_open_claim=%s\nrun_root_creation_model=%s\n' "$failure_expected_threat_boundary_version" "$failure_expected_filesystem_threat_boundary" "$failure_expected_strict_same_uid_race_proof" "$failure_expected_privileged_root_adversary_proof" "$failure_expected_atomic_mkdir_open_claim" "$failure_expected_run_root_creation_model"
  printf 'legacy_fixed_root=%s\nlegacy_fixed_root_disposition=%s\nevidence_root_cleanup=%s\n' "$failure_expected_legacy_fixed_root" "$failure_expected_legacy_fixed_root_disposition" "$failure_expected_evidence_root_cleanup"
  printf 'cleanup_result_phase_b=%s\ncleanup_result_phase_a=%s\ncleanup_result_capture=%s\nwait_status_phase_b=%s\nwait_status_phase_a=%s\nwait_status_capture=%s\nport_release_result_next=%s\nport_release_result_capture=%s\n' "$failure_expected_cleanup_result_phase_b" "$failure_expected_cleanup_result_phase_a" "$failure_expected_cleanup_result_capture" "$failure_expected_wait_status_phase_b" "$failure_expected_wait_status_phase_a" "$failure_expected_wait_status_capture" "$failure_expected_port_release_result_next" "$failure_expected_port_release_result_capture"
  printf 'partial_build_retained=%s\nnext_source_state=%s\nnext_quarantine_state=%s\nnext-env_source_state=%s\nnext-env_quarantine_state=%s\ntsbuildinfo_source_state=%s\ntsbuildinfo_quarantine_state=%s\n' "$failure_expected_partial_build_retained" "$failure_expected_next_source_state" "$failure_expected_next_quarantine_state" "$failure_expected_next_env_source_state" "$failure_expected_next_env_quarantine_state" "$failure_expected_tsbuildinfo_source_state" "$failure_expected_tsbuildinfo_quarantine_state"
  printf 'ownership_handoff_stage=%s\nhandoff_next=%s\nhandoff_next_env=%s\nhandoff_tsbuildinfo=%s\nownership_verification_result=%s\ndelete_stage=%s\npostcondition_result=%s\n' "$failure_expected_ownership_handoff_stage" "$failure_expected_handoff_next" "$failure_expected_handoff_next_env" "$failure_expected_handoff_tsbuildinfo" "$failure_expected_ownership_verification_result" "$failure_expected_delete_stage" "$failure_expected_postcondition_result"
  printf 'expected_fixture_sha256=%s\nexpected_fixture_bytes=%s\npost_request_fixture_sha256=%s\npost_request_fixture_bytes=%s\nfixture_lineage_result=%s\ncapture_response_evidence_state=%s\nresponse_error_seen=%s\nresponse_completion_committed=%s\nresponse_write_started=%s\ncapture_terminal_flag=%s\ncapture_last_state=%s\n' "$failure_expected_expected_fixture_sha256" "$failure_expected_expected_fixture_bytes" "$failure_expected_post_request_fixture_sha256" "$failure_expected_post_request_fixture_bytes" "$failure_expected_fixture_lineage_result" "$failure_expected_capture_response_evidence_state" "$failure_expected_response_error_seen" "$failure_expected_response_completion_committed" "$failure_expected_response_write_started" "$failure_expected_capture_terminal_flag" "$failure_expected_capture_last_state"
}

freeze_failure_state_values() {
  failure_expected_frozen=no
  validate_root_identity || return 1
  printf '%s\n' "$runtime_failure_code" | /usr/bin/grep -Eq '^[A-Z][A-Z0-9_]*$' || return 1
  test -n "$runtime_failure_reason" && record_line_value_safe "$runtime_failure_reason" || return 1
  case "$runtime_interrupted" in yes|no) ;;
    *) return 1 ;;
  esac
  case "$manifest_confirmed_state" in NOT_PUBLISHED|ACTIVE|FAILURE|UNKNOWN) ;;
    *) return 1 ;;
  esac
  case "$manifest_confirmed_state" in
    ACTIVE|FAILURE) printf '%s\n' "$manifest_confirmed_digest" | /usr/bin/grep -Eq '^[0-9a-f]{64}$' || return 1 ;;
    NOT_PUBLISHED) test "$manifest_confirmed_digest" = NOT_PUBLISHED || return 1 ;;
    UNKNOWN) test "$manifest_confirmed_digest" = UNKNOWN || return 1 ;;
  esac
  case "$manifest_publication_result" in NOT_STARTED|PASS|UNCERTAIN) ;;
    *) return 1 ;;
  esac
  case "$manifest_reconciliation_state" in NOT_RUN|ACTIVE|FAILURE|UNKNOWN) ;;
    *) return 1 ;;
  esac
  case "$terminal_commit_state" in PRE_TERMINAL|TERMINAL_COMMITTING|TERMINAL_FAILURE_COMMITTED|TERMINAL_UNKNOWN) ;;
    *) return 1 ;;
  esac
  test "$gate_purpose" = DASHBOARD_PRODUCTION_URL_RESOLUTION_RUNTIME_EVIDENCE || return 1
  test "$threat_boundary_version" = ROOT_IDENTITY_OPTION_C_V1 || return 1
  test "$filesystem_threat_boundary" = T1_T2_T3 && test "$strict_same_uid_race_proof" = NOT_CLAIMED && test "$privileged_root_adversary_proof" = NOT_CLAIMED && test "$atomic_mkdir_open_claim" = NOT_CLAIMED || return 1
  test "$run_root_creation_model" = EXCLUSIVE_UNPREDICTABLE_BASENAME_WITH_CWD_OBJECT_BINDING || return 1
  test "$legacy_fixed_root" = /tmp/edge-mes-dashboard-url-runtime-evidence || return 1

  failure_expected_terminal_disposition=HOLD_NONZERO
  test "$manifest_confirmed_state" = FAILURE && failure_expected_terminal_disposition=FAILURE_NONZERO
  if test "$manifest_confirmed_state" = UNKNOWN || test "$manifest_reconciliation_state" = UNKNOWN; then failure_expected_terminal_disposition=UNKNOWN_NONZERO; fi

  failure_expected_schema_version=1
  failure_expected_record_stage=RUNTIME_FAILURE_STATE
  failure_expected_failure_code=$runtime_failure_code
  failure_expected_failure_reason=$runtime_failure_reason
  failure_expected_interrupted=$runtime_interrupted
  failure_expected_run_nonce=$runtime_run_nonce
  failure_expected_logical_runtime_evidence_identity=$logical_evidence_identity
  failure_expected_run_start_timestamp=$run_start_timestamp
  failure_expected_gate_purpose=$gate_purpose
  failure_expected_root_state=BOUND
  failure_expected_physical_root_path=$logical_root
  failure_expected_canonical_physical_root_path=$canonical_root
  failure_expected_root_device=$root_device
  failure_expected_root_inode=$root_inode
  failure_expected_root_type=$root_type
  failure_expected_private_parent=$private_parent_path
  failure_expected_canonical_private_parent=$canonical_private_parent_path
  failure_expected_private_parent_device=$private_parent_device
  failure_expected_private_parent_inode=$private_parent_inode
  failure_expected_private_parent_type=$private_parent_type
  failure_expected_private_parent_owner_uid=$private_parent_owner_uid
  failure_expected_private_parent_mode=$private_parent_mode
  failure_expected_private_parent_marker_digest=$private_parent_marker_digest
  failure_expected_root_ownership_marker_digest=$root_ownership_marker_digest
  failure_expected_logical_manifest_report_path=$logical_manifest_report_path
  failure_expected_canonical_manifest_report_path=$canonical_manifest_report_path
  failure_expected_manifest_confirmed_state=$manifest_confirmed_state
  failure_expected_manifest_confirmed_digest=$manifest_confirmed_digest
  failure_expected_manifest_publication_result=$manifest_publication_result
  failure_expected_manifest_reconciliation_state=$manifest_reconciliation_state
  failure_expected_manifest_parent_fsync_result=UNKNOWN
  case "$manifest_parent_fsync_result" in
    NOT_CHECKED|PASS|RECOMMENDATION:parent-directory-fsync-unproven|RECOMMENDATION:parent-directory-fsync:*|RECOMMENDATION:parent-directory-close:*) failure_expected_manifest_parent_fsync_result=$manifest_parent_fsync_result ;;
    *) : ;;
  esac
  failure_expected_terminal_commit_state=$terminal_commit_state
  failure_expected_cleanup_state=NOT_EXECUTED_NOT_AUTHORIZED
  failure_expected_threat_boundary_version=$threat_boundary_version
  failure_expected_filesystem_threat_boundary=$filesystem_threat_boundary
  failure_expected_strict_same_uid_race_proof=$strict_same_uid_race_proof
  failure_expected_privileged_root_adversary_proof=$privileged_root_adversary_proof
  failure_expected_atomic_mkdir_open_claim=$atomic_mkdir_open_claim
  failure_expected_run_root_creation_model=$run_root_creation_model
  failure_expected_legacy_fixed_root=$legacy_fixed_root
  failure_expected_legacy_fixed_root_disposition=OUTSIDE_OPTION_C_NAMESPACE_CLEANUP_NOT_AUTHORIZED
  failure_expected_evidence_root_cleanup=NOT_EXECUTED_NOT_AUTHORIZED
  failure_expected_cleanup_result_phase_b=$cleanup_result_phase_b
  failure_expected_cleanup_result_phase_a=$cleanup_result_phase_a
  failure_expected_cleanup_result_capture=$cleanup_result_capture
  failure_expected_wait_status_phase_b=$phase_b_wait_status
  failure_expected_wait_status_phase_a=$phase_a_wait_status
  failure_expected_wait_status_capture=$capture_wait_status
  failure_expected_port_release_result_next=$port_release_result_next
  failure_expected_port_release_result_capture=$port_release_result_capture
  failure_expected_partial_build_retained="$build_artifact_next:$build_artifact_next_env:$build_artifact_tsbuildinfo"
  failure_expected_next_source_state=$(filesystem_state "$frontend_root/.next") || return 1
  failure_expected_next_quarantine_state=$(filesystem_state "$quarantine_next") || return 1
  failure_expected_next_env_source_state=$(filesystem_state "$frontend_root/next-env.d.ts") || return 1
  failure_expected_next_env_quarantine_state=$(filesystem_state "$quarantine_next_env") || return 1
  failure_expected_tsbuildinfo_source_state=$(filesystem_state "$frontend_root/tsconfig.tsbuildinfo") || return 1
  failure_expected_tsbuildinfo_quarantine_state=$(filesystem_state "$quarantine_tsbuildinfo") || return 1
  failure_expected_ownership_handoff_stage=$ownership_handoff_stage
  failure_expected_handoff_next=$handoff_next
  failure_expected_handoff_next_env=$handoff_next_env
  failure_expected_handoff_tsbuildinfo=$handoff_tsbuildinfo
  failure_expected_ownership_verification_result=$ownership_verification_result
  failure_expected_delete_stage=$deletion_stage
  failure_expected_postcondition_result=$postcondition_result
  failure_expected_expected_fixture_sha256=$expected_fixture_sha256
  failure_expected_expected_fixture_bytes=$expected_fixture_bytes
  failure_expected_post_request_fixture_sha256=$post_request_fixture_sha256
  failure_expected_post_request_fixture_bytes=$post_request_fixture_bytes
  failure_expected_fixture_lineage_result=$fixture_lineage_result
  failure_expected_capture_response_evidence_state=$capture_response_evidence_state
  failure_expected_response_error_seen=$capture_response_error_seen
  failure_expected_response_completion_committed=$capture_response_completion_committed
  failure_expected_response_write_started=$capture_response_write_started
  failure_expected_capture_terminal_flag=$capture_terminal_flag
  failure_expected_capture_last_state=$capture_last_state

  failure_expected_frozen=yes
  failure_expected_payload=$(emit_failure_state_expected_record) || { failure_expected_frozen=no; return 1; }
  case "$failure_expected_payload" in *$'\r'*) failure_expected_frozen=no; return 1 ;; esac
  test "$(printf '%s\n' "$failure_expected_payload" | /usr/bin/awk 'END { print NR }')" = 76 || { failure_expected_frozen=no; return 1; }
  return 0
}

write_failure_state() {
  test "$runtime_root_created" = yes || return 0
  freeze_failure_state_values || return 1
  printf '%s\n' "$failure_expected_payload" | root_write_atomic_stdin failure-state.txt || return 1
  validate_failure_state_readback
}

validate_failure_state_readback() {
  test "$failure_expected_frozen" = yes && test -n "$failure_expected_payload" || return 1
  failure_state_path=$(root_artifact_path failure-state.txt) || return 1
  FAILURE_STATE_PATH="$failure_state_path" FAILURE_EXPECTED_PAYLOAD="$failure_expected_payload" node --input-type=module --eval '
import {lstatSync,readFileSync} from "node:fs";import {basename,dirname} from "node:path";
const st=lstatSync(process.env.FAILURE_STATE_PATH,{bigint:true});
if(!st.isFile()||Number(st.mode&0o777n)!==0o600)throw new Error("FAILURE_STATE_METADATA");
const raw=readFileSync(process.env.FAILURE_STATE_PATH,"utf8"),expectedRaw=process.env.FAILURE_EXPECTED_PAYLOAD+"\n";
if(raw!==expectedRaw)throw new Error("FAILURE_STATE_FROZEN_SOURCE_MISMATCH");
if(!raw.endsWith("\n"))throw new Error("FAILURE_STATE_NEWLINE");
const keys=["schema_version","record_stage","failure_code","failure_reason","interrupted","run_nonce","logical_runtime_evidence_identity","run_start_timestamp","gate_purpose","root_state","physical_root_path","canonical_physical_root_path","root_device","root_inode","root_type","private_parent","canonical_private_parent","private_parent_device","private_parent_inode","private_parent_type","private_parent_owner_uid","private_parent_mode","private_parent_marker_digest","root_ownership_marker_digest","logical_manifest_report_path","canonical_manifest_report_path","manifest_confirmed_state","manifest_confirmed_digest","manifest_publication_result","manifest_reconciliation_state","manifest_parent_fsync_result","terminal_commit_state","terminal_disposition","cleanup_state","threat_boundary_version","filesystem_threat_boundary","strict_same_uid_race_proof","privileged_root_adversary_proof","atomic_mkdir_open_claim","run_root_creation_model","legacy_fixed_root","legacy_fixed_root_disposition","evidence_root_cleanup","cleanup_result_phase_b","cleanup_result_phase_a","cleanup_result_capture","wait_status_phase_b","wait_status_phase_a","wait_status_capture","port_release_result_next","port_release_result_capture","partial_build_retained","next_source_state","next_quarantine_state","next-env_source_state","next-env_quarantine_state","tsbuildinfo_source_state","tsbuildinfo_quarantine_state","ownership_handoff_stage","handoff_next","handoff_next_env","handoff_tsbuildinfo","ownership_verification_result","delete_stage","postcondition_result","expected_fixture_sha256","expected_fixture_bytes","post_request_fixture_sha256","post_request_fixture_bytes","fixture_lineage_result","capture_response_evidence_state","response_error_seen","response_completion_committed","response_write_started","capture_terminal_flag","capture_last_state"];
if(keys.length!==76)throw new Error("FAILURE_STATE_DECLARED_FIELD_COUNT");
const lines=raw.slice(0,-1).split("\n");if(lines.length!==keys.length)throw new Error("FAILURE_STATE_KEY_COUNT");
const value={};for(let i=0;i<lines.length;i++){const at=lines[i].indexOf("=");if(at<1)throw new Error("FAILURE_STATE_LINE");const key=lines[i].slice(0,at);if(key!==keys[i]||Object.prototype.hasOwnProperty.call(value,key))throw new Error("FAILURE_STATE_KEY_ORDER");value[key]=lines[i].slice(at+1);}
if(Object.keys(value).length!==76)throw new Error("FAILURE_STATE_VALUE_COVERAGE");
const digest=/^[0-9a-f]{64}$/,positive=/^[1-9][0-9]*$/,waitValue=/^(NOT_WAITED|[0-9]+)$/;
if(!/^[A-Z][A-Z0-9_]*$/.test(value.failure_code)||value.failure_reason.length===0||/[\r\n]/.test(value.failure_reason))throw new Error("FAILURE_STATE_FAILURE_CLASSIFICATION");
if(!["yes","no"].includes(value.interrupted))throw new Error("FAILURE_STATE_INTERRUPTED");
for(const key of ["private_parent_marker_digest","root_ownership_marker_digest"])if(!digest.test(value[key]))throw new Error("FAILURE_STATE_MARKER_DIGEST_"+key);
if(!digest.test(value.run_nonce)||value.logical_runtime_evidence_identity!==`dashboard-production-url-resolution-runtime-evidence/${value.run_nonce}`)throw new Error("FAILURE_STATE_RUN_IDENTITY_RELATION");
if(dirname(value.physical_root_path)!==value.private_parent||dirname(value.canonical_physical_root_path)!==value.canonical_private_parent||basename(value.physical_root_path)!==`run-${value.run_nonce}`||basename(value.canonical_physical_root_path)!==`run-${value.run_nonce}`)throw new Error("FAILURE_STATE_ROOT_PARENT_RELATION");
if(dirname(value.logical_manifest_report_path)!==value.private_parent||dirname(value.canonical_manifest_report_path)!==value.canonical_private_parent||basename(value.logical_manifest_report_path)!==`run-${value.run_nonce}.manifest.json`||basename(value.canonical_manifest_report_path)!==`run-${value.run_nonce}.manifest.json`)throw new Error("FAILURE_STATE_MANIFEST_PATH_RELATION");
if(!/^[0-9]+$/.test(value.root_device)||!/^[0-9]+$/.test(value.root_inode)||!/^[0-9]+$/.test(value.private_parent_device)||!/^[0-9]+$/.test(value.private_parent_inode)||!/^[0-9]+$/.test(value.private_parent_owner_uid)||value.root_type!=="Directory"||value.private_parent_type!=="Directory"||value.private_parent_mode!=="700")throw new Error("FAILURE_STATE_OBJECT_IDENTITY_FORMAT");
if(value.gate_purpose!=="DASHBOARD_PRODUCTION_URL_RESOLUTION_RUNTIME_EVIDENCE"||value.threat_boundary_version!=="ROOT_IDENTITY_OPTION_C_V1"||value.run_root_creation_model!=="EXCLUSIVE_UNPREDICTABLE_BASENAME_WITH_CWD_OBJECT_BINDING"||value.legacy_fixed_root!=="/tmp/edge-mes-dashboard-url-runtime-evidence"||value.legacy_fixed_root_disposition!=="OUTSIDE_OPTION_C_NAMESPACE_CLEANUP_NOT_AUTHORIZED")throw new Error("FAILURE_STATE_FIXED_AUTHORITY_RELATION");
const manifestStates=["NOT_PUBLISHED","ACTIVE","FAILURE","UNKNOWN"],reconcileStates=["NOT_RUN","ACTIVE","FAILURE","UNKNOWN"];
if(!manifestStates.includes(value.manifest_confirmed_state)||!reconcileStates.includes(value.manifest_reconciliation_state))throw new Error("FAILURE_STATE_MANIFEST_ENUM");
if(["ACTIVE","FAILURE"].includes(value.manifest_confirmed_state)){if(!digest.test(value.manifest_confirmed_digest))throw new Error("FAILURE_STATE_MANIFEST_DIGEST");}
else if(value.manifest_confirmed_digest!==value.manifest_confirmed_state)throw new Error("FAILURE_STATE_MANIFEST_SENTINEL");
if(value.manifest_reconciliation_state!=="NOT_RUN"&&value.manifest_reconciliation_state!==value.manifest_confirmed_state)throw new Error("FAILURE_STATE_RECONCILIATION_RELATION");
if(!["NOT_STARTED","PASS","UNCERTAIN"].includes(value.manifest_publication_result))throw new Error("FAILURE_STATE_PUBLICATION_RESULT");
if(!/^(NOT_CHECKED|PASS|UNKNOWN|RECOMMENDATION:parent-directory-(fsync-unproven|fsync:[A-Za-z0-9_.-]+|close:[A-Za-z0-9_.-]+))$/.test(value.manifest_parent_fsync_result))throw new Error("FAILURE_STATE_PARENT_FSYNC_RESULT");
if(!["PRE_TERMINAL","TERMINAL_COMMITTING","TERMINAL_FAILURE_COMMITTED","TERMINAL_UNKNOWN"].includes(value.terminal_commit_state))throw new Error("FAILURE_STATE_TERMINAL_COMMIT_STATE");
let expectedDisposition="HOLD_NONZERO";if(value.manifest_confirmed_state==="FAILURE")expectedDisposition="FAILURE_NONZERO";if(value.manifest_confirmed_state==="UNKNOWN"||value.manifest_reconciliation_state==="UNKNOWN")expectedDisposition="UNKNOWN_NONZERO";
if(value.terminal_disposition!==expectedDisposition)throw new Error("FAILURE_STATE_TERMINAL_DISPOSITION_RELATION");
if(value.terminal_commit_state==="TERMINAL_FAILURE_COMMITTED"&&value.manifest_confirmed_state!=="FAILURE")throw new Error("FAILURE_STATE_FAILURE_COMMIT_RELATION");
if(value.terminal_commit_state==="TERMINAL_UNKNOWN"&&value.manifest_confirmed_state!=="UNKNOWN"&&value.manifest_reconciliation_state!=="UNKNOWN")throw new Error("FAILURE_STATE_UNKNOWN_COMMIT_RELATION");
if(value.cleanup_state!=="NOT_EXECUTED_NOT_AUTHORIZED"||value.evidence_root_cleanup!=="NOT_EXECUTED_NOT_AUTHORIZED")throw new Error("FAILURE_STATE_CLEANUP_AUTHORITY");
if(value.filesystem_threat_boundary!=="T1_T2_T3"||value.strict_same_uid_race_proof!=="NOT_CLAIMED"||value.privileged_root_adversary_proof!=="NOT_CLAIMED"||value.atomic_mkdir_open_claim!=="NOT_CLAIMED")throw new Error("FAILURE_STATE_THREAT_BOUNDARY");
const cleanupAllowed=new Set(["NOT_STARTED","REAPED","ALREADY_EXITED","TERM_SENT_AND_EXITED","TERM_SENT_AND_EXITED_EVIDENCE_WRITE_FAILURE","LISTENER_LOST_BUT_TERMINATED","TERM_TIMEOUT","IDENTITY_UNRESOLVED","WAIT_NOT_CHILD","WAIT_FAILURE","UNRESOLVED"]);
const cleanupSuccess=new Set(["REAPED","ALREADY_EXITED","TERM_SENT_AND_EXITED","TERM_SENT_AND_EXITED_EVIDENCE_WRITE_FAILURE","LISTENER_LOST_BUT_TERMINATED"]);
for(const [cleanupKey,waitKey] of [["cleanup_result_phase_b","wait_status_phase_b"],["cleanup_result_phase_a","wait_status_phase_a"],["cleanup_result_capture","wait_status_capture"]]){const cleanup=value[cleanupKey],wait=value[waitKey];if(!cleanupAllowed.has(cleanup)||!waitValue.test(wait))throw new Error("FAILURE_STATE_WAIT_CLEANUP_ENUM_"+cleanupKey);if(cleanupSuccess.has(cleanup)&&wait!=="0")throw new Error("FAILURE_STATE_WAIT_SUCCESS_"+cleanupKey);if(cleanup==="NOT_STARTED"&&wait!=="NOT_WAITED")throw new Error("FAILURE_STATE_WAIT_NOT_STARTED_"+cleanupKey);if(cleanup==="WAIT_NOT_CHILD"&&wait!=="127")throw new Error("FAILURE_STATE_WAIT_NOT_CHILD_"+cleanupKey);if(wait==="127"&&!new Set(["WAIT_NOT_CHILD","WAIT_FAILURE"]).has(cleanup))throw new Error("FAILURE_STATE_WAIT_127_HIDDEN_"+cleanupKey);}
const portAllowed=new Set(["NOT_CHECKED","released","unknown_listener","lsof_failure"]);if(!portAllowed.has(value.port_release_result_next)||!portAllowed.has(value.port_release_result_capture))throw new Error("FAILURE_STATE_PORT_ENUM");
const buildAllowed=new Set(["NOT_CREATED","CREATED_DIRECTORY","CREATED_REGULAR_FILE","TYPE_OR_LINK_MISMATCH"]),buildParts=value.partial_build_retained.split(":");if(buildParts.length!==3||buildParts.some(part=>!buildAllowed.has(part)))throw new Error("FAILURE_STATE_PARTIAL_BUILD_GRAMMAR");
const fsAllowed=new Set(["ABSENT_NOT_LINK","SYMLINK_OR_DANGLING_SYMLINK","DIRECTORY","REGULAR_FILE","OTHER_FILESYSTEM_OBJECT"]);for(const key of ["next_source_state","next_quarantine_state","next-env_source_state","next-env_quarantine_state","tsbuildinfo_source_state","tsbuildinfo_quarantine_state"])if(!fsAllowed.has(value[key]))throw new Error("FAILURE_STATE_FILESYSTEM_STATE_"+key);
if(!["NOT_STARTED","PHASE_2_IN_PROGRESS","PHASE_2_COMPLETE"].includes(value.ownership_handoff_stage))throw new Error("FAILURE_STATE_HANDOFF_STAGE");
for(const key of ["handoff_next","handoff_next_env","handoff_tsbuildinfo"])if(!["NOT_STARTED","NOT_CREATED_SKIPPED","RENAMED_TO_QUARANTINE","DELETED"].includes(value[key]))throw new Error("FAILURE_STATE_HANDOFF_"+key);
if(!["NOT_STARTED","PHASE_3_IN_PROGRESS","PASS","FAIL"].includes(value.ownership_verification_result)||!["NOT_STARTED","PHASE_4_IN_PROGRESS","PHASE_4_FAILED","PHASE_4_COMPLETE"].includes(value.delete_stage)||!["NOT_STARTED","PHASE_5_IN_PROGRESS","PASS","FAIL"].includes(value.postcondition_result))throw new Error("FAILURE_STATE_ARTIFACT_STAGE_RELATION");
const digestOrNotRecorded=value=>value==="NOT_RECORDED"||digest.test(value),bytesOrNotRecorded=value=>value==="NOT_RECORDED"||positive.test(value);
if(!digestOrNotRecorded(value.expected_fixture_sha256)||!bytesOrNotRecorded(value.expected_fixture_bytes)||!digestOrNotRecorded(value.post_request_fixture_sha256)||!bytesOrNotRecorded(value.post_request_fixture_bytes))throw new Error("FAILURE_STATE_FIXTURE_FORMAT");
if((value.expected_fixture_sha256==="NOT_RECORDED")!==(value.expected_fixture_bytes==="NOT_RECORDED")||(value.post_request_fixture_sha256==="NOT_RECORDED")!==(value.post_request_fixture_bytes==="NOT_RECORDED"))throw new Error("FAILURE_STATE_FIXTURE_SENTINEL_RELATION");
if(!["NOT_CHECKED","PASS","FAIL"].includes(value.fixture_lineage_result)||!["NOT_CHECKED","RESPONSE_COMPLETE","NOT_COMPLETE"].includes(value.capture_response_evidence_state))throw new Error("FAILURE_STATE_FIXTURE_RESULT_ENUM");
for(const key of ["response_error_seen","response_completion_committed","response_write_started","capture_terminal_flag"])if(!["NOT_READ_FROM_SHELL","true","false"].includes(value[key]))throw new Error("FAILURE_STATE_BOOLEAN_SENTINEL_"+key);
if(!["NOT_READ_FROM_SHELL","STARTING","LISTENING","TARGET_REQUEST_IN_PROGRESS","TARGET_REQUEST_COMPLETE","ERROR","TERMINATING","TERMINATED"].includes(value.capture_last_state))throw new Error("FAILURE_STATE_CAPTURE_STATE_ENUM");
if(value.fixture_lineage_result==="PASS"){if(!digest.test(value.expected_fixture_sha256)||!digest.test(value.post_request_fixture_sha256)||value.expected_fixture_sha256!==value.post_request_fixture_sha256||!positive.test(value.expected_fixture_bytes)||value.expected_fixture_bytes!==value.post_request_fixture_bytes||value.capture_response_evidence_state!=="RESPONSE_COMPLETE")throw new Error("FAILURE_STATE_FIXTURE_LINEAGE_RELATION");}
if(value.capture_response_evidence_state==="RESPONSE_COMPLETE"&&(value.response_error_seen!=="false"||value.response_completion_committed!=="true"||value.response_write_started!=="true"))throw new Error("FAILURE_STATE_RESPONSE_COMPLETION_RELATION");
'
}

cleanup_role() {
  cleanup_role_name=$1
  cleanup_port=$2
  cleanup_role_result=UNRESOLVED
  case "$cleanup_role_name" in
    capture) cleanup_pid=$capture_pid; cleanup_state=$capture_state; cleanup_reaped=$capture_reaped ;;
    phase_a_next) cleanup_pid=$phase_a_pid; cleanup_state=$phase_a_state; cleanup_reaped=$phase_a_reaped ;;
    phase_b_next) cleanup_pid=$phase_b_pid; cleanup_state=$phase_b_state; cleanup_reaped=$phase_b_reaped ;;
    *) cleanup_role_result=IDENTITY_UNRESOLVED; return 1 ;;
  esac
  if test "$cleanup_reaped" = yes; then cleanup_role_result=REAPED; return 0; fi
  if test "$cleanup_state" = NOT_STARTED || test -z "$cleanup_pid"; then cleanup_role_result=NOT_STARTED; return 0; fi
  if ! kill -0 "$cleanup_pid" 2>/dev/null; then
    wait "$cleanup_pid" 2>/dev/null; wait_rc=$?
    record_wait_status "$cleanup_role_name" "$wait_rc" || { cleanup_role_result=WAIT_FAILURE; return 1; }
    if test "$wait_rc" -eq 127; then cleanup_role_result=WAIT_NOT_CHILD; return 1; fi
    if test "$wait_rc" -ne 0; then cleanup_role_result=WAIT_FAILURE; return 1; fi
    case "$cleanup_role_name" in capture) capture_reaped=yes ;; phase_a_next) phase_a_reaped=yes ;; phase_b_next) phase_b_reaped=yes ;; esac
    set_role_state "$cleanup_role_name" REAPED || { cleanup_role_result=UNRESOLVED; return 1; }
    cleanup_role_result=ALREADY_EXITED; return 0
  fi
  cleanup_identity=verified
  identity_matches "$cleanup_role_name"; identity_rc=$?
  if test "$identity_rc" -ne 0; then
    candidate_identity_matches "$cleanup_role_name"; candidate_identity_rc=$?
    if test "$candidate_identity_rc" -ne 0; then
      set_role_state "$cleanup_role_name" UNRESOLVED
      cleanup_role_result=IDENTITY_UNRESOLVED
      return 1
    fi
    cleanup_identity=candidate
  fi
  record_listener_state "$cleanup_role_name" "$cleanup_pid" "$cleanup_port"
  listener_record_rc=$?
  kill -TERM "$cleanup_pid" 2>/dev/null
  if test $? -ne 0; then cleanup_role_result=UNRESOLVED; return 1; fi
  set_role_state "$cleanup_role_name" STOPPING || { cleanup_role_result=UNRESOLVED; return 1; }
  for cleanup_attempt in 1 2 3 4 5 6 7 8 9 10; do
    kill -0 "$cleanup_pid" 2>/dev/null || break
    sleep 1
  done
  if kill -0 "$cleanup_pid" 2>/dev/null; then cleanup_role_result=TERM_TIMEOUT; return 1; fi
  wait "$cleanup_pid" 2>/dev/null; wait_rc=$?
  record_wait_status "$cleanup_role_name" "$wait_rc" || { cleanup_role_result=WAIT_FAILURE; return 1; }
  if test "$wait_rc" -eq 127; then set_role_state "$cleanup_role_name" UNRESOLVED; cleanup_role_result=WAIT_NOT_CHILD; return 1; fi
  if test "$wait_rc" -ne 0; then set_role_state "$cleanup_role_name" UNRESOLVED; cleanup_role_result=WAIT_FAILURE; return 1; fi
  case "$cleanup_role_name" in capture) capture_reaped=yes ;; phase_a_next) phase_a_reaped=yes ;; phase_b_next) phase_b_reaped=yes ;; esac
  set_role_state "$cleanup_role_name" STOPPED || { cleanup_role_result=UNRESOLVED; return 1; }
  set_role_state "$cleanup_role_name" REAPED || { cleanup_role_result=UNRESOLVED; return 1; }
  if test "$listener_record_rc" -ne 0 || test "$listener_evidence_write_result" = EVIDENCE_WRITE_FAILURE; then
    cleanup_role_result=TERM_SENT_AND_EXITED_EVIDENCE_WRITE_FAILURE
    return 1
  fi
  if test "$listener_state_result" = PRESENT; then cleanup_role_result=TERM_SENT_AND_EXITED
  else cleanup_role_result=LISTENER_LOST_BUT_TERMINATED
  fi
  return 0
}

port_release_check() {
  release_role=$1
  release_port=$2
  release_output=$(/usr/sbin/lsof -nP -iTCP:"$release_port" -sTCP:LISTEN 2>&1)
  release_rc=$?
  if test "$release_rc" -eq 1 && test -z "$release_output"; then port_release_result=released; return 0; fi
  if test "$release_rc" -eq 0; then port_release_result=unknown_listener; return 1; fi
  port_release_result=lsof_failure
  return 1
}

classify_generated_artifact() {
  artifact_path=$1
  artifact_kind=$2
  artifact_classification=NOT_CREATED
  if test -L "$artifact_path"; then artifact_classification=TYPE_OR_LINK_MISMATCH
  elif test ! -e "$artifact_path"; then artifact_classification=NOT_CREATED
  elif test "$artifact_kind" = directory && test -d "$artifact_path"; then artifact_classification=CREATED_DIRECTORY
  elif test "$artifact_kind" = regular && test -f "$artifact_path"; then artifact_classification=CREATED_REGULAR_FILE
  else artifact_classification=TYPE_OR_LINK_MISMATCH
  fi
  return 0
}

filesystem_state() {
  filesystem_state_path=$1
  if test -L "$filesystem_state_path"; then
    printf 'SYMLINK_OR_DANGLING_SYMLINK'
  elif test ! -e "$filesystem_state_path"; then
    printf 'ABSENT_NOT_LINK'
  elif test -d "$filesystem_state_path"; then
    printf 'DIRECTORY'
  elif test -f "$filesystem_state_path"; then
    printf 'REGULAR_FILE'
  else
    printf 'OTHER_FILESYSTEM_OBJECT'
  fi
}

read_stat_identity() {
  identity_path=$1
  identity_stat=$(/usr/bin/stat -f 'device=%d%ninode=%i%ntype=%HT%nsymlink_target=%Y' -- "$identity_path") || return 1
  identity_device=$(printf '%s\n' "$identity_stat" | /usr/bin/awk -F= '$1 == "device" { print substr($0, index($0, "=") + 1) }')
  identity_inode=$(printf '%s\n' "$identity_stat" | /usr/bin/awk -F= '$1 == "inode" { print substr($0, index($0, "=") + 1) }')
  identity_type=$(printf '%s\n' "$identity_stat" | /usr/bin/awk -F= '$1 == "type" { print substr($0, index($0, "=") + 1) }')
  identity_symlink_status=not-link
  test ! -L "$identity_path" || identity_symlink_status=symlink
  test -n "$identity_device" && test -n "$identity_inode" && test -n "$identity_type" && test "$identity_symlink_status" = not-link
}

record_artifact_ownership() {
  ownership_role=$1
  ownership_path=$2
  ownership_classification=$3
  ownership_record_stage=$4
  case "$ownership_role" in
    next|next_env|tsbuildinfo) : ;;
    *) return 1 ;;
  esac
  if test "$ownership_classification" = NOT_CREATED; then
    no_path_or_link "$ownership_path" || return 1
    ownership_device=absent
    ownership_inode=absent
    ownership_type=absent
    ownership_symlink_status=not-link
  else
    case "$ownership_classification" in
      CREATED_DIRECTORY) test -d "$ownership_path" && test ! -L "$ownership_path" || return 1 ;;
      CREATED_REGULAR_FILE) test -f "$ownership_path" && test ! -L "$ownership_path" || return 1 ;;
      *) return 1 ;;
    esac
    read_stat_identity "$ownership_path" || return 1
    ownership_device=$identity_device
    ownership_inode=$identity_inode
    ownership_type=$identity_type
    ownership_symlink_status=$identity_symlink_status
  fi
  case "$ownership_role" in
    next) ownership_next_device=$ownership_device; ownership_next_inode=$ownership_inode; ownership_next_type=$ownership_type; ownership_next_symlink_status=$ownership_symlink_status ;;
    next_env) ownership_next_env_device=$ownership_device; ownership_next_env_inode=$ownership_inode; ownership_next_env_type=$ownership_type; ownership_next_env_symlink_status=$ownership_symlink_status ;;
    tsbuildinfo) ownership_tsbuildinfo_device=$ownership_device; ownership_tsbuildinfo_inode=$ownership_inode; ownership_tsbuildinfo_type=$ownership_type; ownership_tsbuildinfo_symlink_status=$ownership_symlink_status ;;
  esac
  {
    printf 'path=%s\n' "$ownership_path"
    printf 'classification=%s\n' "$ownership_classification"
    printf 'device=%s\n' "$ownership_device"
    printf 'inode=%s\n' "$ownership_inode"
    printf 'type=%s\n' "$ownership_type"
    printf 'symlink_status=%s\n' "$ownership_symlink_status"
    printf 'record_stage=%s\n' "$ownership_record_stage"
  } >> "$(root_artifact_path artifact-ownership.txt)" || return 1
}

validate_recorded_ownership() {
  validation_role=$1
  validation_path=$2
  case "$validation_role" in
    next) validation_classification=$build_artifact_next; validation_device=$ownership_next_device; validation_inode=$ownership_next_inode; validation_type=$ownership_next_type; validation_symlink_status=$ownership_next_symlink_status ;;
    next_env) validation_classification=$build_artifact_next_env; validation_device=$ownership_next_env_device; validation_inode=$ownership_next_env_inode; validation_type=$ownership_next_env_type; validation_symlink_status=$ownership_next_env_symlink_status ;;
    tsbuildinfo) validation_classification=$build_artifact_tsbuildinfo; validation_device=$ownership_tsbuildinfo_device; validation_inode=$ownership_tsbuildinfo_inode; validation_type=$ownership_tsbuildinfo_type; validation_symlink_status=$ownership_tsbuildinfo_symlink_status ;;
    *) return 1 ;;
  esac
  if test "$validation_classification" = NOT_CREATED; then
    no_path_or_link "$validation_path"
    return $?
  fi
  test -e "$validation_path" && test ! -L "$validation_path" || return 1
  case "$validation_classification" in
    CREATED_DIRECTORY) test -d "$validation_path" || return 1 ;;
    CREATED_REGULAR_FILE) test -f "$validation_path" || return 1 ;;
    *) return 1 ;;
  esac
  read_stat_identity "$validation_path" || return 1
  test "$identity_device" = "$validation_device" && test "$identity_inode" = "$validation_inode" && \
    test "$identity_type" = "$validation_type" && test "$identity_symlink_status" = "$validation_symlink_status"
}

atomic_artifact_handoff() {
  handoff_role=$1
  case "$handoff_role" in
    next) handoff_source_path="$frontend_root/.next"; handoff_quarantine_path="$quarantine_next"; handoff_classification=$build_artifact_next ;;
    next_env) handoff_source_path="$frontend_root/next-env.d.ts"; handoff_quarantine_path="$quarantine_next_env"; handoff_classification=$build_artifact_next_env ;;
    tsbuildinfo) handoff_source_path="$frontend_root/tsconfig.tsbuildinfo"; handoff_quarantine_path="$quarantine_tsbuildinfo"; handoff_classification=$build_artifact_tsbuildinfo ;;
    *) runtime_hold OWNERSHIP_HANDOFF_ROLE "unknown artifact handoff role: $handoff_role"; return 1 ;;
  esac
  test "${handoff_source_path%/*}" = "${handoff_quarantine_path%/*}" || { runtime_hold OWNERSHIP_HANDOFF_PARENT "source and quarantine are not same-parent paths"; return 1; }
  validate_recorded_ownership "$handoff_role" "$handoff_source_path" || { runtime_hold OWNERSHIP_SOURCE_MISMATCH "source identity changed before handoff: $handoff_source_path"; return 1; }
  no_path_or_link "$handoff_quarantine_path" || { runtime_hold QUARANTINE_PREFLIGHT "quarantine target is present or linked: $handoff_quarantine_path"; return 1; }
  case "$handoff_classification" in
    NOT_CREATED)
      case "$handoff_role" in
        next) handoff_next=NOT_CREATED_SKIPPED ;;
        next_env) handoff_next_env=NOT_CREATED_SKIPPED ;;
        tsbuildinfo) handoff_tsbuildinfo=NOT_CREATED_SKIPPED ;;
      esac
      ;;
    CREATED_DIRECTORY|CREATED_REGULAR_FILE)
      /bin/mv -n "$handoff_source_path" "$handoff_quarantine_path" || { runtime_hold OWNERSHIP_HANDOFF_RENAME "atomic quarantine rename failed: $handoff_source_path"; return 1; }
      case "$handoff_role" in
        next) handoff_next=RENAMED_TO_QUARANTINE ;;
        next_env) handoff_next_env=RENAMED_TO_QUARANTINE ;;
        tsbuildinfo) handoff_tsbuildinfo=RENAMED_TO_QUARANTINE ;;
      esac
      ;;
    *) runtime_hold OWNERSHIP_SOURCE_CLASSIFICATION "source classification changed before handoff: $handoff_source_path"; return 1 ;;
  esac
}

verify_artifact_handoff() {
  verification_role=$1
  case "$verification_role" in
    next) verification_source_path="$frontend_root/.next"; verification_quarantine_path="$quarantine_next"; verification_classification=$build_artifact_next ;;
    next_env) verification_source_path="$frontend_root/next-env.d.ts"; verification_quarantine_path="$quarantine_next_env"; verification_classification=$build_artifact_next_env ;;
    tsbuildinfo) verification_source_path="$frontend_root/tsconfig.tsbuildinfo"; verification_quarantine_path="$quarantine_tsbuildinfo"; verification_classification=$build_artifact_tsbuildinfo ;;
    *) runtime_hold OWNERSHIP_HANDOFF_ROLE "unknown artifact verification role: $verification_role"; return 1 ;;
  esac
  no_path_or_link "$verification_source_path" || { runtime_hold OWNERSHIP_HANDOFF_MISMATCH "source remained or changed after handoff: $verification_source_path"; return 1; }
  if test "$verification_classification" = NOT_CREATED; then
    no_path_or_link "$verification_quarantine_path" || { runtime_hold OWNERSHIP_HANDOFF_MISMATCH "NOT_CREATED quarantine appeared: $verification_quarantine_path"; return 1; }
  else
    validate_recorded_ownership "$verification_role" "$verification_quarantine_path" || { runtime_hold OWNERSHIP_HANDOFF_MISMATCH "quarantine identity mismatch: $verification_quarantine_path"; return 1; }
  fi
}

delete_verified_quarantine() {
  deletion_role=$1
  case "$deletion_role" in
    next)
      validate_recorded_ownership next "$frontend_root/.edge-mes-runtime-evidence-next.quarantine" || { runtime_hold PRE_DELETE_OWNERSHIP_MISMATCH "quarantine identity changed before recursive deletion: $frontend_root/.edge-mes-runtime-evidence-next.quarantine"; return 1; }
      /bin/rm -rf -- "$frontend_root/.edge-mes-runtime-evidence-next.quarantine" || { runtime_hold DELETE_QUARANTINE_NEXT "verified .next quarantine deletion failed"; return 1; }
      handoff_next=DELETED
      ;;
    next_env)
      validate_recorded_ownership next_env "$frontend_root/.edge-mes-runtime-evidence-next-env.quarantine" || { runtime_hold PRE_DELETE_OWNERSHIP_MISMATCH "quarantine identity changed before deletion: $frontend_root/.edge-mes-runtime-evidence-next-env.quarantine"; return 1; }
      /bin/rm -- "$frontend_root/.edge-mes-runtime-evidence-next-env.quarantine" || { runtime_hold DELETE_QUARANTINE_NEXT_ENV "verified next-env.d.ts quarantine deletion failed"; return 1; }
      handoff_next_env=DELETED
      ;;
    tsbuildinfo)
      validate_recorded_ownership tsbuildinfo "$frontend_root/.edge-mes-runtime-evidence-tsbuildinfo.quarantine" || { runtime_hold PRE_DELETE_OWNERSHIP_MISMATCH "quarantine identity changed before deletion: $frontend_root/.edge-mes-runtime-evidence-tsbuildinfo.quarantine"; return 1; }
      /bin/rm -- "$frontend_root/.edge-mes-runtime-evidence-tsbuildinfo.quarantine" || { runtime_hold DELETE_QUARANTINE_TSB "verified tsbuildinfo quarantine deletion failed"; return 1; }
      handoff_tsbuildinfo=DELETED
      ;;
    *) runtime_hold DELETE_QUARANTINE_ROLE "unknown quarantine deletion role: $deletion_role"; return 1 ;;
  esac
}

emit_hold_output() {
  hold_run_nonce=$runtime_run_nonce; test -n "$hold_run_nonce" || hold_run_nonce=NOT_ASSIGNED
  case "$runtime_root_created" in
    yes) hold_root_state=BOUND; hold_root_device=$root_device; hold_root_inode=$root_inode; hold_root_type=$root_type ;;
    uncertain) hold_root_state=CREATED_UNCERTAIN; hold_root_device=$created_root_device; hold_root_inode=$created_root_inode; hold_root_type=$created_root_type ;;
    *) hold_root_state=NOT_CREATED; hold_root_device=NOT_AVAILABLE; hold_root_inode=NOT_AVAILABLE; hold_root_type=NOT_AVAILABLE ;;
  esac
  test -n "$hold_root_device" || hold_root_device=NOT_AVAILABLE
  test -n "$hold_root_inode" || hold_root_inode=NOT_AVAILABLE
  test -n "$hold_root_type" || hold_root_type=NOT_AVAILABLE
  hold_logical_root=$logical_root; test -n "$hold_logical_root" && test "$hold_logical_root" != UNASSIGNED || hold_logical_root=NOT_ASSIGNED
  hold_canonical_root=$canonical_root; test -n "$hold_canonical_root" && test "$hold_canonical_root" != NOT_AVAILABLE || hold_canonical_root=NOT_AVAILABLE
  hold_manifest_path=$logical_manifest_report_path; test -n "$hold_manifest_path" && test "$hold_manifest_path" != UNASSIGNED || hold_manifest_path=NOT_ASSIGNED
  hold_canonical_manifest_path=$canonical_manifest_report_path; test -n "$hold_canonical_manifest_path" && test "$hold_canonical_manifest_path" != UNASSIGNED || hold_canonical_manifest_path=NOT_AVAILABLE
  hold_manifest_state=$manifest_confirmed_state; test -n "$hold_manifest_state" || hold_manifest_state=NOT_PUBLISHED
  hold_manifest_digest=$manifest_confirmed_digest; test -n "$hold_manifest_digest" || hold_manifest_digest=NOT_PUBLISHED
  hold_reconciliation_state=$manifest_reconciliation_state; test -n "$hold_reconciliation_state" || hold_reconciliation_state=NOT_RUN
  hold_parent_path=$private_parent_path; test -n "$hold_parent_path" || hold_parent_path=NOT_ASSIGNED
  hold_canonical_parent=$canonical_private_parent_path; test -n "$hold_canonical_parent" || hold_canonical_parent=NOT_AVAILABLE
  hold_parent_device=$private_parent_device; test -n "$hold_parent_device" || hold_parent_device=NOT_AVAILABLE
  hold_parent_inode=$private_parent_inode; test -n "$hold_parent_inode" || hold_parent_inode=NOT_AVAILABLE
  hold_parent_type=$private_parent_type; test -n "$hold_parent_type" || hold_parent_type=NOT_AVAILABLE
  hold_parent_marker_digest=$private_parent_marker_digest; test -n "$hold_parent_marker_digest" || hold_parent_marker_digest=NOT_AVAILABLE
  hold_root_marker_digest=$root_ownership_marker_digest; test -n "$hold_root_marker_digest" || hold_root_marker_digest=NOT_AVAILABLE
  printf 'run_nonce=%s\nroot_state=%s\n' "$hold_run_nonce" "$hold_root_state"
  printf 'logical_root=%s\ncanonical_root=%s\nroot_device=%s\nroot_inode=%s\nroot_type=%s\n' "$hold_logical_root" "$hold_canonical_root" "$hold_root_device" "$hold_root_inode" "$hold_root_type"
  printf 'logical_manifest_report_path=%s\nmanifest_confirmed_state=%s\nmanifest_confirmed_digest=%s\nmanifest_reconciliation_state=%s\n' "$hold_manifest_path" "$hold_manifest_state" "$hold_manifest_digest" "$hold_reconciliation_state"
  printf 'private_parent=%s\ncanonical_private_parent=%s\nprivate_parent_device=%s\nprivate_parent_inode=%s\nprivate_parent_type=%s\nprivate_parent_marker_digest=%s\nroot_ownership_marker_digest=%s\n' "$hold_parent_path" "$hold_canonical_parent" "$hold_parent_device" "$hold_parent_inode" "$hold_parent_type" "$hold_parent_marker_digest" "$hold_root_marker_digest"
  printf 'cleanup_state=NOT_EXECUTED_NOT_AUTHORIZED\nterminal_disposition=HOLD_NONZERO\n'
  printf 'filesystem_threat_boundary=%s\nstrict_same_uid_race_proof=%s\nprivileged_root_adversary_proof=%s\natomic_mkdir_open_claim=%s\n' "$filesystem_threat_boundary" "$strict_same_uid_race_proof" "$privileged_root_adversary_proof" "$atomic_mkdir_open_claim"
}

emit_terminal_pass() {
  test "$terminal_commit_state" = SUCCESS_COMMITTED || return 1
  if test -z "$terminal_pass_line_prefix"; then terminal_pass_line_prefix="PASS: run-specific evidence root retained; run_nonce=$runtime_run_nonce logical=$logical_root canonical=$canonical_root dev=$root_device inode=$root_inode manifest=$logical_manifest_report_path private_parent_marker_digest=$private_parent_marker_digest root_ownership_marker_digest=$root_ownership_marker_digest defends=T1,T2,T3 does_not_claim=T4,T5 atomic_mkdir_open=$atomic_mkdir_open_claim cleanup=NOT_EXECUTED_NOT_AUTHORIZED"; fi
  terminal_pass_line="$terminal_pass_line_prefix manifest_state=SUCCESS manifest_digest=$manifest_confirmed_digest"
  printf '%s\n' "$terminal_pass_line" >&2
}

runtime_common_failure_dispatch() {
  test "$terminal_commit_state" = SUCCESS_COMMITTED && return 0
  test "$runtime_dispatch_started" = yes && return 0
  runtime_dispatch_started=yes
  cleanup_role phase_b_next "$next_port"; cleanup_call_rc=$?; cleanup_result_phase_b=$cleanup_role_result
  cleanup_role phase_a_next "$next_port"; cleanup_call_rc=$?; cleanup_result_phase_a=$cleanup_role_result
  cleanup_role capture "$capture_port"; cleanup_call_rc=$?; cleanup_result_capture=$cleanup_role_result
  port_release_check next "$next_port"; cleanup_call_rc=$?; port_release_result_next=$port_release_result
  port_release_check capture "$capture_port"; cleanup_call_rc=$?; port_release_result_capture=$port_release_result
  if test "$runtime_root_created" = yes && test "$root_cwd_bound" = yes; then
    if test "$manifest_publication_result" = UNCERTAIN; then
      reconcile_manifest_after_publication_failure || printf 'HOLD: manifest reconciliation is UNKNOWN; manual review required\n' >&2
    fi
    if test "$manifest_confirmed_state" = SUCCESS; then
      terminal_commit_state=SUCCESS_COMMITTED
      return 0
    fi
    failure_publication_needed=no
    if test "$manifest_confirmed_state" = NOT_PUBLISHED && test "$manifest_publication_result" = NOT_STARTED; then
      failure_publication_needed=yes
    elif test "$manifest_confirmed_state" = ACTIVE; then
      failure_publication_needed=yes
    fi
    if test "$failure_publication_needed" = yes; then
      publish_run_manifest FAILURE
      failure_manifest_publish_rc=$?
      if test "$failure_manifest_publish_rc" -eq 0; then
        validate_manifest_mapping FAILURE || printf 'HOLD: FAILURE manifest mapping validation failed\n' >&2
      elif test "$manifest_publication_result" = UNCERTAIN; then
        reconcile_manifest_after_publication_failure || printf 'HOLD: FAILURE publication reconciliation is UNKNOWN; manual review required\n' >&2
      fi
    elif test "$manifest_confirmed_state" = UNKNOWN; then
      printf 'HOLD: terminal manifest state UNKNOWN; no overwrite/no cleanup; manual review required\n' >&2
    fi
  fi
  write_failure_state || printf 'HOLD: failure-state evidence write failed\n' >&2
  printf 'HOLD: cleanup phase_b=%s phase_a=%s capture=%s next_port=%s capture_port=%s\n' \
    "$cleanup_result_phase_b" "$cleanup_result_phase_a" "$cleanup_result_capture" "$port_release_result_next" "$port_release_result_capture" >&2
  emit_hold_output >&2
  printf 'HOLD: filesystem boundary defends=T1,T2,T3 does_not_claim=T4,T5 atomic_mkdir_open=%s cleanup=NOT_EXECUTED_NOT_AUTHORIZED\n' "$atomic_mkdir_open_claim" >&2
  printf 'HOLD: legacy root remains outside Option C namespace: %s cleanup=NOT_AUTHORIZED\n' "$legacy_fixed_root" >&2
  printf 'HOLD: build/generated artifacts retained; success cleanup and Git cleanup not run\n' >&2
  return 0
}

runtime_signal() {
  signal_name=$1
  signal_exit=$2
  runtime_signal_exit_code=$signal_exit
  if test "$runtime_signal_handling" = yes || test "$runtime_dispatch_started" = yes; then
    runtime_interrupted=yes
    runtime_hold "SIGNAL_$signal_name" "control shell received $signal_name during cleanup" >/dev/null 2>&1
    return 0
  fi
  runtime_signal_handling=yes
  runtime_interrupted=yes
  runtime_hold "SIGNAL_$signal_name" "control shell received $signal_name" >/dev/null 2>&1
  runtime_common_failure_dispatch
  trap - INT TERM HUP
  exit "$signal_exit"
}

runtime_install_failure_traps() {
  trap 'runtime_signal INT 130' INT
  trap 'runtime_signal TERM 143' TERM
  trap 'runtime_signal HUP 129' HUP
}

runtime_ignore_terminal_traps() {
  trap '' INT TERM HUP
  runtime_signal_handling=no
}

# The dispatcher and signal functions exist before this point; traps are installed before
# evidence-root creation or any launch.
runtime_install_failure_traps

runtime_evidence_main() {
  cd "$repo_root" || { runtime_hold PREFLIGHT_REPO "repository root unavailable"; return 1; }
  freeze_root_precreate || { runtime_hold PRIVATE_PARENT_PREFLIGHT "pre-created private parent ownership, mode, marker, or object identity invalid"; return 1; }
  test ! -e "$frontend_root/.next" && test ! -L "$frontend_root/.next" || { runtime_hold PREFLIGHT_PATH "present or symlink: $frontend_root/.next"; return 1; }
  test ! -e "$frontend_root/next-env.d.ts" && test ! -L "$frontend_root/next-env.d.ts" || { runtime_hold PREFLIGHT_PATH "present or symlink: $frontend_root/next-env.d.ts"; return 1; }
  test ! -e "$frontend_root/tsconfig.tsbuildinfo" && test ! -L "$frontend_root/tsconfig.tsbuildinfo" || { runtime_hold PREFLIGHT_PATH "present or symlink: $frontend_root/tsconfig.tsbuildinfo"; return 1; }
  test ! -e "$quarantine_next" || { runtime_hold PREFLIGHT_QUARANTINE_PATH "quarantine path present: $quarantine_next"; return 1; }
  test ! -L "$quarantine_next" || { runtime_hold PREFLIGHT_QUARANTINE_LINK "quarantine path linked: $quarantine_next"; return 1; }
  test ! -e "$quarantine_next_env" || { runtime_hold PREFLIGHT_QUARANTINE_PATH "quarantine path present: $quarantine_next_env"; return 1; }
  test ! -L "$quarantine_next_env" || { runtime_hold PREFLIGHT_QUARANTINE_LINK "quarantine path linked: $quarantine_next_env"; return 1; }
  test ! -e "$quarantine_tsbuildinfo" || { runtime_hold PREFLIGHT_QUARANTINE_PATH "quarantine path present: $quarantine_tsbuildinfo"; return 1; }
  test ! -L "$quarantine_tsbuildinfo" || { runtime_hold PREFLIGHT_QUARANTINE_LINK "quarantine path linked: $quarantine_tsbuildinfo"; return 1; }
  preflight_next=$(/usr/sbin/lsof -nP -iTCP:"$next_port" -sTCP:LISTEN 2>&1); preflight_next_rc=$?
  preflight_capture=$(/usr/sbin/lsof -nP -iTCP:"$capture_port" -sTCP:LISTEN 2>&1); preflight_capture_rc=$?
  test "$preflight_next_rc" -eq 1 && test -z "$preflight_next" && test "$preflight_capture_rc" -eq 1 && test -z "$preflight_capture" || { runtime_hold PREFLIGHT_PORT "port listener or lsof failure"; return 1; }
  # Bind the separately prepared private-parent object before run-root creation.
  # Parent absence, marker mismatch, wrong owner, non-0700 mode, symlink, or
  # logical/canonical identity drift is HOLD. Existing retained run roots are
  # allowed and are never enumerated, adopted, modified, or deleted here.
  test ! -L "$logical_parent" && test ! -L "$canonical_parent" || { runtime_hold PRIVATE_PARENT_LINK "private parent path became a symlink before object binding"; return 1; }
  cd -P "$logical_parent" || { runtime_hold PRIVATE_PARENT_BIND "cannot enter verified private parent"; return 1; }
  validate_parent_cwd || { runtime_hold PRIVATE_PARENT_IDENTITY "private parent ownership, mode, marker, or object identity changed before run-root creation"; return 1; }
  runtime_run_nonce=$(
    node --input-type=module --eval \
      'import { randomBytes } from "node:crypto"; process.stdout.write(randomBytes(32).toString("hex"));'
  )
  nonce_rc=$?
  test "$nonce_rc" -eq 0 || { runtime_hold RUN_NONCE_GENERATION "unable to generate runtime nonce"; return 1; }
  test "${#runtime_run_nonce}" -eq 64 || { runtime_hold RUN_NONCE_LENGTH "runtime nonce length invalid"; return 1; }
  printf '%s\n' "$runtime_run_nonce" | /usr/bin/grep -Eq '^[0-9a-f]{64}$' || { runtime_hold RUN_NONCE_FORMAT "runtime nonce format invalid"; return 1; }
  root_basename="run-$runtime_run_nonce"
  logical_root="$private_parent/$root_basename"
  logical_evidence_identity="dashboard-production-url-resolution-runtime-evidence/$runtime_run_nonce"
  manifest_basename="$root_basename.manifest.json"
  manifest_tmp_basename=".$manifest_basename.tmp"
  logical_manifest_report_path="$private_parent/$manifest_basename"
  canonical_manifest_report_path="$canonical_parent/$manifest_basename"
  run_start_timestamp=$(/bin/date -u '+%Y-%m-%dT%H:%M:%SZ') || { runtime_hold RUN_START_TIMESTAMP "unable to record run start timestamp"; return 1; }
  test "$root_basename" = "run-$runtime_run_nonce" && test "$manifest_basename" = "$root_basename.manifest.json" && test "$manifest_tmp_basename" = ".$manifest_basename.tmp" || { runtime_hold RUN_ID_DERIVATION "run-root or manifest basename derivation invalid"; return 1; }
  no_path_or_link "$root_basename" || { runtime_hold RUN_ROOT_COLLISION "current-run root basename already exists or is linked"; return 1; }
  manifest_parent_cwd_preflight || { runtime_hold MANIFEST_NAMESPACE_PREFLIGHT "private-parent CWD or current-run manifest namespace is invalid"; return 1; }
  validate_parent_cwd || { runtime_hold PRIVATE_PARENT_IDENTITY "private parent changed immediately before exclusive run-root creation"; return 1; }
  runtime_root_created=uncertain
  create_and_capture_run_root || { runtime_hold RUN_ROOT_CREATED_CAPTURE "run-specific root identity/ownership capture failed or remained uncertain"; return 1; }
  root_ownership_marker_digest=$created_root_ownership_digest
  freeze_root_postcreate || { runtime_hold ROOT_IDENTITY "run-specific root path, ownership marker, or adopted CWD identity invalid"; return 1; }
  runtime_root_created=yes
  publish_run_manifest ACTIVE || { runtime_hold MANIFEST_ACTIVE_PUBLISH "ACTIVE run manifest publication failed"; return 1; }
  validate_manifest_mapping ACTIVE || { runtime_hold MANIFEST_ACTIVE_MAPPING "ACTIVE run manifest mapping invalid"; return 1; }
  : > "$(root_artifact_path process-identities.txt)" || { runtime_hold IDENTITY_ARTIFACT "cannot create identity artifact"; return 1; }
  validate_root_identity || { runtime_hold ROOT_IDENTITY "root identity changed after initialization"; return 1; }
  {
    printf 'schema_version=1\nrecord_stage=RUNTIME_PROCESS_IDENTITY_SNAPSHOT\nmanifest_state_at_snapshot=ACTIVE\nmanifest_digest_at_snapshot=%s\nsnapshot_is_terminal=false\n' "$manifest_confirmed_digest"
    printf 'run_nonce=%s\n' "$runtime_run_nonce"
    printf 'logical_runtime_evidence_identity=%s\n' "$logical_evidence_identity"
    printf 'physical_root_path=%s\ncanonical_physical_root_path=%s\n' "$logical_root" "$canonical_root"
    printf 'root_device=%s\nroot_inode=%s\nroot_type=%s\n' "$root_device" "$root_inode" "$root_type"
    printf 'logical_manifest_report_path=%s\ncanonical_manifest_report_path=%s\nmanifest_confirmed_state=%s\nmanifest_confirmed_digest=%s\nmanifest_publication_result=%s\n' "$logical_manifest_report_path" "$canonical_manifest_report_path" "$manifest_confirmed_state" "$manifest_confirmed_digest" "$manifest_publication_result"
    printf 'filesystem_threat_boundary=%s\nstrict_same_uid_race_proof=%s\nprivileged_root_adversary_proof=%s\natomic_mkdir_open_claim=%s\n' "$filesystem_threat_boundary" "$strict_same_uid_race_proof" "$privileged_root_adversary_proof" "$atomic_mkdir_open_claim"
  } >> "$(root_artifact_path process-identities.txt)" || {
    runtime_hold RUN_IDENTITY_EVIDENCE "run identity/manifest/threat-boundary evidence write failed"
    return 1
  }
  validate_root_identity || { runtime_hold ROOT_IDENTITY "root identity changed before root artifact creation"; return 1; }
  {
    printf '.next=absent-not-link\n'
    printf 'next-env.d.ts=absent-not-link\n'
    printf 'tsconfig.tsbuildinfo=absent-not-link\n'
    printf 'quarantine-next=absent-not-link\n'
    printf 'quarantine-next-env.d.ts=absent-not-link\n'
    printf 'quarantine-tsconfig.tsbuildinfo=absent-not-link\n'
  } > "$(root_artifact_path artifact-prestate.txt)" || { runtime_hold PRESTATE_WRITE "cannot record generated pre-state"; return 1; }
  for exact_path in "$evidence_root/capture-state.json" "$evidence_root/capture-state.tmp" "$evidence_root/capture-ready.txt" "$evidence_root/capture.log" "$evidence_root/capture-requests.jsonl" "$evidence_root/fixture.json" "$evidence_root/fixture-identity.json" "$evidence_root/fixture-identity.tmp" "$evidence_root/capture-response-evidence.json" "$evidence_root/capture-response-evidence.tmp" "$evidence_root/capture.pid" "$evidence_root/next-phase-a.pid" "$evidence_root/next-phase-b.pid" "$evidence_root/artifact-ownership.txt" "$evidence_root/evidence-summary.txt" "$evidence_root/failure-state.txt"; do
    no_path_or_link "$exact_path" || { runtime_hold ROOT_ARTIFACT_PREFLIGHT "present or symlink: $exact_path"; return 1; }
  done
  : > "$(root_artifact_path artifact-ownership.txt)" || { runtime_hold OWNERSHIP_ARTIFACT "cannot create artifact ownership evidence"; return 1; }
  test -f "$evidence_root/artifact-ownership.txt" && test ! -L "$evidence_root/artifact-ownership.txt" || { runtime_hold OWNERSHIP_ARTIFACT "artifact ownership evidence is not a regular non-link file"; return 1; }
  FULL_WRITE_HELPER="$full_write_helper" ROOT_DEVICE="$root_device" ROOT_INODE="$root_inode" CAPTURE_STATE="$evidence_root/capture-state.json" CAPTURE_STATE_TMP="$evidence_root/capture-state.tmp" node --input-type=module --eval '
import { closeSync, fsyncSync, lstatSync, openSync, renameSync, writeSync } from "node:fs";
const rootObject=lstatSync(".");if(!rootObject.isDirectory()||String(rootObject.dev)!==process.env.ROOT_DEVICE||String(rootObject.ino)!==process.env.ROOT_INODE)throw new Error("ROOT_CWD_IDENTITY");
const writeFully=eval(process.env.FULL_WRITE_HELPER),value=Buffer.from(JSON.stringify({state:"STARTING",target_count:0,request_log_count:0,last_stage:"initialization",error_code:null,error_message:null,terminal:false,accepting:true,response_error_seen:false,response_completion_committed:false,response_write_started:false})+"\\n");let fd=-1;try{fd=openSync(process.env.CAPTURE_STATE_TMP,"wx",0o600);writeFully(fd,value,writeSync);fsyncSync(fd);closeSync(fd);fd=-1;renameSync(process.env.CAPTURE_STATE_TMP,process.env.CAPTURE_STATE);}catch(error){if(fd>=0){try{closeSync(fd);}catch{}}throw error;}
' || { runtime_hold CAPTURE_STATE_INIT "cannot atomically initialize capture state"; return 1; }
  validate_root_identity || { runtime_hold ROOT_IDENTITY "root identity changed before fixture creation"; return 1; }
  FULL_WRITE_HELPER="$full_write_helper" ROOT_DEVICE="$root_device" ROOT_INODE="$root_inode" FIXTURE_PATH="$evidence_root/fixture.json" FIXTURE_IDENTITY="$evidence_root/fixture-identity.json" FIXTURE_IDENTITY_TMP="$evidence_root/fixture-identity.tmp" node --input-type=module --eval '
import { closeSync, existsSync, fsyncSync, lstatSync, openSync, renameSync, writeSync } from "node:fs";
import { createHash } from "node:crypto";
const rootObject=lstatSync(".");if(!rootObject.isDirectory()||String(rootObject.dev)!==process.env.ROOT_DEVICE||String(rootObject.ino)!==process.env.ROOT_INODE)throw new Error("ROOT_CWD_IDENTITY");
const item={line_id:"LINE_RUNTIME_001",plc_id:"PLC_RUNTIME_001",station_id:"STATION_RUNTIME_001",station_type:"inspection",profile_id:"business-profile-runtime-fixture",config_hash:"sha256:runtime-fixture-config",config_version:"runtime-fixture-v1",event_type:"station_completed",production_result:"NOK",unit_id:"UNIT-RUNTIME-FIXTURE-001",dmc:"DMC-RUNTIME-FIXTURE-001",cycle_counter:42,source_event_id:"runtime-source-event-001",event_ts:"2026-07-05T00:30:00Z",accepted_at:"2026-07-05T00:30:01Z",fact_key:"sha256:runtime-fixture-fact",content_fingerprint:"sha256:runtime-fixture-content",nok_code:"RUNTIME_NOK",nok_origin:"station",nok_detail_code:"RUNTIME_DETAIL",nok_detail_source_event_id:"runtime-detail-source-001",nok_detail_evidence_fact_key:"sha256:runtime-detail-evidence"};
const itemKeys=["line_id","plc_id","station_id","station_type","profile_id","config_hash","config_version","event_type","production_result","unit_id","dmc","cycle_counter","source_event_id","event_ts","accepted_at","fact_key","content_fingerprint","nok_code","nok_origin","nok_detail_code","nok_detail_source_event_id","nok_detail_evidence_fact_key"];
const exact=(value,keys,label)=>{ if(value===null||typeof value!=="object"||Array.isArray(value)) throw new Error(`${label} object`); const actual=Object.keys(value); if(actual.length!==keys.length||actual.some(key=>!keys.includes(key))||keys.some(key=>!Object.prototype.hasOwnProperty.call(value,key))) throw new Error(`${label} exact keys`); };
const fixture={data:{items:[item]},page:{next_cursor:"runtime-next-cursor-001",limit:50}};
exact(fixture,["data","page"],"envelope"); exact(fixture.data,["items"],"data"); exact(fixture.page,["next_cursor","limit"],"page"); if(fixture.data.items.length!==1) throw new Error("fixture item count"); exact(fixture.data.items[0],itemKeys,"item"); if(typeof item.cycle_counter!=="number"||typeof fixture.page.limit!=="number") throw new Error("fixture number type");
const responseBody=Buffer.from(JSON.stringify(fixture)); const fixtureSha256=createHash("sha256").update(responseBody).digest("hex"); const fixtureBytes=responseBody.byteLength;
const fullWrite=eval(process.env.FULL_WRITE_HELPER); let fixtureFd=-1; try { fixtureFd=openSync(process.env.FIXTURE_PATH,"wx",0o600); fullWrite(fixtureFd,responseBody,writeSync); fsyncSync(fixtureFd); closeSync(fixtureFd); fixtureFd=-1; } catch(error) { if(fixtureFd>=0) { try { closeSync(fixtureFd); } catch {} } throw error; }
if(existsSync(process.env.FIXTURE_IDENTITY)) throw new Error("fixture identity exists"); const identity=JSON.stringify({record_stage:"FIXTURE_GENERATED",fixture_sha256:fixtureSha256,fixture_bytes:fixtureBytes,item_count:1,item_key_count:22,envelope_keys:["data","page"],data_keys:["items"],page_keys:["next_cursor","limit"]})+"\\n"; let identityFd=-1; try { identityFd=openSync(process.env.FIXTURE_IDENTITY_TMP,"wx",0o600); fullWrite(identityFd,identity,writeSync); fsyncSync(identityFd); closeSync(identityFd); identityFd=-1; renameSync(process.env.FIXTURE_IDENTITY_TMP,process.env.FIXTURE_IDENTITY); } catch(error) { if(identityFd>=0) { try { closeSync(identityFd); } catch {} } throw error; }
' || { runtime_hold FIXTURE_GENERATION "frozen fixture/identity generation failed"; return 1; }
  test -f "$evidence_root/fixture.json" && test ! -L "$evidence_root/fixture.json" && test -f "$evidence_root/fixture-identity.json" && test ! -L "$evidence_root/fixture-identity.json" || { runtime_hold FIXTURE_ARTIFACT_TYPE "fixture identity artifact missing, linked or non-regular"; return 1; }
  fixture_identity_values=$(ROOT_DEVICE="$root_device" ROOT_INODE="$root_inode" FIXTURE_IDENTITY="$evidence_root/fixture-identity.json" node --input-type=module --eval '
import {lstatSync,readFileSync} from "node:fs"; const rootObject=lstatSync(".");if(!rootObject.isDirectory()||String(rootObject.dev)!==process.env.ROOT_DEVICE||String(rootObject.ino)!==process.env.ROOT_INODE)throw new Error("ROOT_CWD_IDENTITY"); const value=JSON.parse(readFileSync(process.env.FIXTURE_IDENTITY,"utf8")); const exact=(actual,keys)=>Object.keys(actual).length===keys.length&&keys.every(key=>Object.prototype.hasOwnProperty.call(actual,key)); if(value.record_stage!=="FIXTURE_GENERATED"||!exact(value,["record_stage","fixture_sha256","fixture_bytes","item_count","item_key_count","envelope_keys","data_keys","page_keys"])||!Array.isArray(value.envelope_keys)||value.envelope_keys.join(",")!=="data,page"||!Array.isArray(value.data_keys)||value.data_keys.join(",")!=="items"||!Array.isArray(value.page_keys)||value.page_keys.join(",")!=="next_cursor,limit"||value.item_count!==1||value.item_key_count!==22||!(/^[0-9a-f]{64}$/).test(value.fixture_sha256)||!Number.isInteger(value.fixture_bytes)||value.fixture_bytes<=0) throw new Error("fixture identity shape"); process.stdout.write(`${value.fixture_sha256} ${value.fixture_bytes}`);'
  ) || { runtime_hold FIXTURE_IDENTITY_READ "fixture identity parse/validation failed"; return 1; }
  IFS=' ' read -r expected_fixture_sha256 expected_fixture_bytes <<EOF
$fixture_identity_values
EOF
  printf '%s\n' "$expected_fixture_sha256" | /usr/bin/grep -Eq '^[0-9a-f]{64}$' && printf '%s\n' "$expected_fixture_bytes" | /usr/bin/grep -Eq '^[1-9][0-9]*$' || { runtime_hold FIXTURE_IDENTITY_FORMAT "fixture identity digest/bytes invalid"; return 1; }

  runtime_launch_generation=$((runtime_launch_generation + 1))
  capture_launch_generation=$runtime_launch_generation
  construct_launch_marker capture "$capture_launch_generation" || { runtime_hold CAPTURE_MARKER_CONSTRUCTION "capture marker construction failed"; return 1; }
  capture_launch_marker=$constructed_marker
  validate_root_identity || { runtime_hold ROOT_IDENTITY "root identity changed before capture launch"; return 1; }
  FULL_WRITE_HELPER="$full_write_helper" CAPTURE_ROOT="$evidence_root" ROOT_DEVICE="$root_device" ROOT_INODE="$root_inode" CAPTURE_PORT="$capture_port" EXPECTED_FIXTURE_SHA256="$expected_fixture_sha256" EXPECTED_FIXTURE_BYTES="$expected_fixture_bytes" CAPTURE_RESPONSE_EVIDENCE="$evidence_root/capture-response-evidence.json" CAPTURE_RESPONSE_EVIDENCE_TMP="$evidence_root/capture-response-evidence.tmp" node --input-type=module --eval '
import { appendFileSync, closeSync, existsSync, fsyncSync, lstatSync, openSync, readFileSync, renameSync, writeFileSync, writeSync } from "node:fs";
import { createHash } from "node:crypto"; import { createServer } from "node:http";
const root=process.env.CAPTURE_ROOT,statePath=`${root}/capture-state.json`,tmpPath=`${root}/capture-state.tmp`,readyPath=`${root}/capture-ready.txt`,logPath=`${root}/capture-requests.jsonl`,fixturePath=`${root}/fixture.json`,responseEvidence=process.env.CAPTURE_RESPONSE_EVIDENCE,responseEvidenceTmp=process.env.CAPTURE_RESPONSE_EVIDENCE_TMP,expectedSha256=process.env.EXPECTED_FIXTURE_SHA256,expectedBytes=Number(process.env.EXPECTED_FIXTURE_BYTES);
const rootObject=lstatSync(".");if(!rootObject.isDirectory()||String(rootObject.dev)!==process.env.ROOT_DEVICE||String(rootObject.ino)!==process.env.ROOT_INODE)throw new Error("ROOT_CWD_IDENTITY");
const itemKeys=["line_id","plc_id","station_id","station_type","profile_id","config_hash","config_version","event_type","production_result","unit_id","dmc","cycle_counter","source_event_id","event_ts","accepted_at","fact_key","content_fingerprint","nok_code","nok_origin","nok_detail_code","nok_detail_source_event_id","nok_detail_evidence_fact_key"];
const exact=(value,keys,label)=>{ if(value===null||typeof value!=="object"||Array.isArray(value)) throw new Error(`${label} object`); const actual=Object.keys(value); if(actual.length!==keys.length||actual.some(key=>!keys.includes(key))||keys.some(key=>!Object.prototype.hasOwnProperty.call(value,key))) throw new Error(`${label} exact keys`); };
const transitionTargets=Object.freeze({STARTING:new Set(["LISTENING","ERROR","TERMINATING"]),LISTENING:new Set(["TARGET_REQUEST_IN_PROGRESS","ERROR","TERMINATING"]),TARGET_REQUEST_IN_PROGRESS:new Set(["TARGET_REQUEST_COMPLETE","ERROR","TERMINATING"]),TARGET_REQUEST_COMPLETE:new Set(["ERROR","TERMINATING"]),ERROR:new Set(["TERMINATING"]),TERMINATING:new Set(["TERMINATED"]),TERMINATED:new Set([])});
const canTransition=(current,next)=>current===next||transitionTargets[current]?.has(next)===true;
let responseErrorSeen=false,responseCompletionCommitted=false,responseWriteStarted=false;
let state={state:"STARTING",target_count:0,request_log_count:0,last_stage:"boot",error_code:null,error_message:null,terminal:false,accepting:true,response_error_seen:false,response_completion_committed:false,response_write_started:false},accepting=true,terminal=false,server,listenCalled=false,listenPending=false,listenCallbackCommitted=false,closeRequested=false,closeStarted=false,closeCompleted=false,closeError=null,terminationStarted=false,terminationCompleted=false;
const closeWaiters=[];
function atom(next){const text=Buffer.from(JSON.stringify(next)+"\\n");let fd=-1;try{fd=openSync(tmpPath,"wx",0o600);writeFully(fd,text,writeSync);fsyncSync(fd);closeSync(fd);fd=-1;renameSync(tmpPath,statePath);state=next;}catch(error){if(fd>=0){try{closeSync(fd);}catch{}}throw error;}}
function set(next,stage,code=null,message=null){if(!canTransition(state.state,next))throw new Error("INVALID_STATE_TRANSITION:"+state.state+"->"+next);atom({state:next,target_count:state.target_count,request_log_count:state.request_log_count,last_stage:stage,error_code:code,error_message:message,terminal,accepting,response_error_seen:responseErrorSeen,response_completion_committed:responseCompletionCommitted,response_write_started:responseWriteStarted});}
function noteCloseError(stage,error){if(error){process.stderr.write("capture "+stage+" close failed: "+error+"\\n");process.exitCode=1;}}
function deliverClose(error=null){if(closeCompleted===true)return;closeCompleted=true;closeError=error??null;if(closeError!==null)noteCloseError("server",closeError);for(const waiter of closeWaiters.splice(0)){waiter(closeError);}}
function joinClose(onClosed){if(typeof onClosed!=="function")return;if(closeCompleted===true){onClosed(closeError);return;}closeWaiters.push(onClosed);}
function requestServerClose(stage,onClosed){closeRequested=true;joinClose(onClosed);if(closeCompleted===true)return;if(!server||listenCalled===false){deliverClose(null);return;}if(listenPending===true&&server.listening!==true)return;if(server.listening!==true){deliverClose(closeError);return;}if(closeStarted===true)return;closeStarted=true;try{server.close(error=>deliverClose(error??null));}catch(error){deliverClose(error);}}
function finishTermination(stage,closedError=null){const noHandle=listenCalled===false&&listenPending===false&&server?.listening!==true;if(closeCompleted!==true&&!noHandle)return;if(terminationCompleted===true)return;if(closedError!==null)noteCloseError(stage,closedError);try{set("TERMINATED",stage,closedError===null?null:"SERVER_CLOSE_FAILURE",closedError===null?null:String(closedError));}catch(stateError){process.stderr.write("capture TERMINATED state write failed: "+stateError+"\\n");process.exitCode=1;}terminationCompleted=true;process.exit(process.exitCode??0);}
function beginTermination(stage){if(terminationCompleted===true)return;if(terminationStarted===true){requestServerClose(stage);return;}terminationStarted=true;terminal=true;accepting=false;try{set("TERMINATING",stage);}catch(error){process.stderr.write("capture TERMINATING state write failed: "+error+"\\n");process.exitCode=1;}requestServerClose(stage,closedError=>finishTermination(closedError===null?stage:stage+"-close-error",closedError));}
function fatal(code,error){terminal=true;accepting=false;process.exitCode=1;const current=state.state;const errorState=current==="ERROR"||current==="TERMINATING"||current==="TERMINATED"?current:"ERROR";try{set(errorState,"error",code,String(error));}catch(writeError){process.stderr.write("capture ERROR state write failed: "+writeError+"\\n");process.exitCode=1;}beginTermination("fatal");}
function terminate(){beginTermination("signal");}
const pathPresent=(candidate)=>{try{lstatSync(candidate);return true;}catch(error){if(error?.code==="ENOENT")return false;throw error;}};
const writeFully=eval(process.env.FULL_WRITE_HELPER);
function writeResponseEvidence(value){if(pathPresent(responseEvidence)||pathPresent(responseEvidenceTmp))throw new Error("response evidence final/tmp exists");const text=Buffer.from(JSON.stringify(value)+"\\n");let fd=-1;try{fd=openSync(responseEvidenceTmp,"wx",0o600);writeFully(fd,text,writeSync);fsyncSync(fd);closeSync(fd);fd=-1;renameSync(responseEvidenceTmp,responseEvidence);}catch(error){if(fd>=0){try{closeSync(fd);}catch{}}throw error;}}
function commitResponseComplete(payload){
  if(terminal===true)return;
  const finalPresent=pathPresent(responseEvidence),tmpPresent=pathPresent(responseEvidenceTmp);
  const guardOk=terminal===false&&responseErrorSeen===false&&responseCompletionCommitted===false&&responseWriteStarted===false&&state.state==="TARGET_REQUEST_IN_PROGRESS"&&state.target_count===0&&state.request_log_count===0&&accepting===false&&!finalPresent&&!tmpPresent;
  if(!guardOk){fatal("RESPONSE_COMPLETION_INVALID_STATE","response completion guard failed");return;}
  responseWriteStarted=true;
  try{
    writeResponseEvidence(payload);
    responseCompletionCommitted=true;
    state.target_count=1;
    state.request_log_count=1;
    try{set("TARGET_REQUEST_COMPLETE","response-complete-evidence-committed");}
    catch(error){responseCompletionCommitted=false;state.target_count=0;state.request_log_count=0;fatal("RESPONSE_COMPLETE_STATE_WRITE_FAILURE",error);}
  }catch(error){responseCompletionCommitted=false;state.target_count=0;state.request_log_count=0;fatal("RESPONSE_EVIDENCE_OR_STATE_WRITE_FAILURE",error);}
}
server=createServer((req,res)=>{
  try{
    const url=new URL(req.url,"http://"+(req.headers.host??"127.0.0.1"));
    if(req.method!=="GET"||url.pathname!=="/api/v2/production/accepted-station-events"){fatal("UNEXPECTED_METHOD_OR_PATH",req.method+" "+url.pathname);try{res.destroy();}catch{}return;}
    const invalidAdmission=terminal!==false||accepting!==true||state.state!=="LISTENING"||state.target_count!==0||state.request_log_count!==0||responseErrorSeen!==false||responseCompletionCommitted!==false;
    if(invalidAdmission){fatal("REQUEST_ADMISSION_INVALID_STATE","target admission guard failed");try{res.destroy();}catch{}return;}
    set("TARGET_REQUEST_IN_PROGRESS","target-request-begin");
    const fixtureBytes=readFileSync(fixturePath);
    const captureReadSha256=createHash("sha256").update(fixtureBytes).digest("hex"),captureReadBytes=fixtureBytes.byteLength;
    if(captureReadSha256!==expectedSha256||captureReadBytes!==expectedBytes)throw new Error("fixture identity mismatch");
    const parsed=JSON.parse(fixtureBytes.toString("utf8"));
    exact(parsed,["data","page"],"envelope");exact(parsed.data,["items"],"data");exact(parsed.page,["next_cursor","limit"],"page");
    if(!Array.isArray(parsed.data.items)||parsed.data.items.length!==1)throw new Error("response item count");
    exact(parsed.data.items[0],itemKeys,"item");
    const responseBody=fixtureBytes,servedBodySha256=createHash("sha256").update(responseBody).digest("hex"),servedBodyBytes=responseBody.byteLength;
    if(servedBodySha256!==expectedSha256||servedBodyBytes!==expectedBytes)throw new Error("served identity mismatch");
    const entry={method:req.method,pathname:url.pathname,host:req.headers.host??"",target:true,query_entries:[...url.searchParams.entries()],fixture_sha256_expected:expectedSha256,capture_read_sha256:captureReadSha256,served_body_sha256:servedBodySha256,served_body_bytes:servedBodyBytes};
    appendFileSync(logPath,JSON.stringify(entry)+"\n");
    accepting=false;
    res.once("error",error=>{responseErrorSeen=true;fatal("RESPONSE_WRITE_FAILURE",error);});
    res.setHeader("content-type","application/json");
    res.end(responseBody,()=>{
      if(terminal===true)return;
      commitResponseComplete({record_stage:"RESPONSE_COMPLETE",response_completed:true,fixture_sha256_expected:expectedSha256,fixture_bytes_expected:expectedBytes,capture_read_sha256:captureReadSha256,capture_read_bytes:captureReadBytes,served_body_sha256:servedBodySha256,served_body_bytes:servedBodyBytes,item_count:1,item_key_count:22,target_request_ordinal:1});
    });
  }catch(error){fatal("REQUEST_HANDLER_FAILURE",error);try{if(!res.writableEnded)res.destroy(error);}catch{}}
});
process.on("uncaughtException",error=>fatal("UNCAUGHT_EXCEPTION",error));process.on("unhandledRejection",error=>fatal("UNHANDLED_REJECTION",error));process.on("SIGTERM",terminate);
server.once("error",error=>{if(listenPending===true){listenPending=false;closeError=error;}fatal("SERVER_ERROR",error);});
function beginListen(){
  if(terminal!==false||accepting!==true||state.state!=="STARTING"){terminate();return;}
  listenCalled=true;
  listenPending=true;
  try{server.listen(Number(process.env.CAPTURE_PORT),"127.0.0.1",()=>{listenPending=false;const listenCallbackGuard=terminal===false&&accepting===true&&state.state==="STARTING";if(!listenCallbackGuard){requestServerClose("listen-callback-rejected");return;}try{set("LISTENING","listener-ready");listenCallbackCommitted=true;writeFileSync(readyPath,"LISTENING\\n",{flag:"wx"});}catch(error){fatal("READY_OR_STATE_WRITE_FAILURE",error);}});}catch(error){listenPending=false;closeError=error;fatal("LISTEN_CALL_FAILURE",error);}
}
if(terminal===false&&accepting===true&&state.state==="STARTING"){beginListen();}else{terminate();}
' -- "$capture_launch_marker" > "$(root_artifact_path capture.log)" 2>&1 &
  capture_pid=$!; register_candidate capture "$capture_pid" "$capture_launch_marker" "$capture_launch_generation" || { runtime_hold CAPTURE_CANDIDATE_REGISTER "capture candidate registration evidence failed"; return 1; }
  record_identity capture "$capture_pid" || { capture_state=UNRESOLVED; runtime_hold CAPTURE_CANDIDATE_IDENTITY "capture identity unavailable"; return 1; }
  printf '%s\n' "$capture_pid" > "$(root_artifact_path capture.pid)" || { runtime_hold CAPTURE_PID_WRITE "capture PID evidence write failed"; return 1; }
  test "$(/bin/cat "$evidence_root/capture.pid")" = "$capture_pid" || { runtime_hold CAPTURE_PID_REREAD "capture PID evidence reread failed"; return 1; }
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    test "$runtime_interrupted" = no || { runtime_hold SIGNAL_PENDING "signal received during capture readiness"; return 1; }
    capture_ready_state=$(node --input-type=module --eval 'import {readFileSync} from "node:fs"; const s=JSON.parse(readFileSync(process.argv[1],"utf8")); process.stdout.write(`${s.state}:${s.target_count}:${s.request_log_count}:${s.error_code}`);' "$evidence_root/capture-state.json" 2>/dev/null)
    if test "$capture_ready_state" = LISTENING:0:0:null && test "$(/bin/cat "$evidence_root/capture-ready.txt" 2>/dev/null)" = LISTENING; then
      record_listener_state capture "$capture_pid" "$capture_port"; listener_call_rc=$?
      test "$listener_call_rc" -eq 0 && test "$listener_state_result" = PRESENT && break
      test "$listener_evidence_write_result" != EVIDENCE_WRITE_FAILURE || { runtime_hold CAPTURE_LISTENER_EVIDENCE "capture listener evidence write failed"; return 1; }
    fi
    identity_matches capture || break
    sleep 1
  done
  identity_matches capture || { capture_state=UNRESOLVED; runtime_hold CAPTURE_READINESS_IDENTITY "capture exited or identity changed"; return 1; }
  record_listener_state capture "$capture_pid" "$capture_port"; listener_call_rc=$?
  test "$listener_evidence_write_result" != EVIDENCE_WRITE_FAILURE || { runtime_hold CAPTURE_LISTENER_EVIDENCE "capture listener evidence write failed"; return 1; }
  test "$listener_call_rc" -eq 0 && test "$listener_state_result" = PRESENT || { runtime_hold CAPTURE_LISTENER "capture alive but listener missing or lsof failed"; return 1; }
  capture_state=READY

  # Do not leave the verified evidence-root CWD in the control shell. Build
  # runs in a child subshell, so later relative evidence I/O remains object-bound.
  ( cd "$frontend_root" && /usr/bin/env -u EDGE_MES_DASHBOARD_API_ORIGIN -u EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE npm run build )
  build_rc=$?
  test "$build_rc" -eq 0 || { runtime_hold BUILD_FAILED "partial build retained"; return 1; }
  test -d "$frontend_root/.next" && test ! -L "$frontend_root/.next" && test -f "$frontend_root/.next/BUILD_ID" && test -f "$frontend_root/.next/standalone/server.js" || { runtime_hold BUILD_OUTPUT "expected build output missing or linked"; return 1; }
  classify_generated_artifact "$frontend_root/.next" directory; build_artifact_next=$artifact_classification
  classify_generated_artifact "$frontend_root/next-env.d.ts" regular; build_artifact_next_env=$artifact_classification
  classify_generated_artifact "$frontend_root/tsconfig.tsbuildinfo" regular; build_artifact_tsbuildinfo=$artifact_classification
  test "$build_artifact_next" = CREATED_DIRECTORY || { runtime_hold BUILD_OUTPUT "required .next classification: $build_artifact_next"; return 1; }
  test "$build_artifact_next_env" != TYPE_OR_LINK_MISMATCH && test "$build_artifact_tsbuildinfo" != TYPE_OR_LINK_MISMATCH || { runtime_hold BUILD_ARTIFACT_TYPE "auxiliary artifact type/link mismatch"; return 1; }
  record_artifact_ownership next "$frontend_root/.next" "$build_artifact_next" post-build-classification || { runtime_hold OWNERSHIP_RECORD "cannot record .next task-owned identity"; return 1; }
  record_artifact_ownership next_env "$frontend_root/next-env.d.ts" "$build_artifact_next_env" post-build-classification || { runtime_hold OWNERSHIP_RECORD "cannot record next-env.d.ts task-owned identity"; return 1; }
  record_artifact_ownership tsbuildinfo "$frontend_root/tsconfig.tsbuildinfo" "$build_artifact_tsbuildinfo" post-build-classification || { runtime_hold OWNERSHIP_RECORD "cannot record tsconfig.tsbuildinfo task-owned identity"; return 1; }
  expected_build_id=$(/bin/cat "$frontend_root/.next/BUILD_ID")
  expected_server_sha=$(/usr/bin/shasum -a 256 "$frontend_root/.next/standalone/server.js" | /usr/bin/awk '{print $1}')
  test -n "$expected_build_id" && test -n "$expected_server_sha" || { runtime_hold BUILD_IDENTITY "initial build identity unavailable"; return 1; }
  : > "$(root_artifact_path build-identity.txt)" || { runtime_hold BUILD_IDENTITY_WRITE "cannot create identity evidence"; return 1; }
  record_checkpoint() { checkpoint=$1; current_build_id=$(/bin/cat "$frontend_root/.next/BUILD_ID" 2>/dev/null); current_server_sha=$(/usr/bin/shasum -a 256 "$frontend_root/.next/standalone/server.js" 2>/dev/null | /usr/bin/awk '{print $1}'); printf 'label=%s\nBUILD_ID=%s\nserver.js SHA-256=%s\n' "$checkpoint" "$current_build_id" "$current_server_sha" >> "$(root_artifact_path build-identity.txt)" || return 1; test "$current_build_id" = "$expected_build_id" && test "$current_server_sha" = "$expected_server_sha"; }
  record_checkpoint post-build || { runtime_hold CHECKPOINT_POST_BUILD "same-artifact checkpoint failed"; return 1; }

  runtime_launch_generation=$((runtime_launch_generation + 1))
  phase_a_launch_generation=$runtime_launch_generation
  construct_launch_marker phase_a_next "$phase_a_launch_generation" || { runtime_hold PHASE_A_MARKER_CONSTRUCTION "Phase A marker construction failed"; return 1; }
  phase_a_launch_marker=$constructed_marker
  validate_root_identity || { runtime_hold ROOT_IDENTITY "root identity changed before Phase A launch"; return 1; }
  ( cd "$frontend_root/.next/standalone" && exec /usr/bin/env -u EDGE_MES_DASHBOARD_API_ORIGIN -u EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE HOSTNAME=127.0.0.1 PORT="$next_port" node server.js -- "$phase_a_launch_marker" ) > "$(root_artifact_path phase-a-next.log)" 2>&1 &
  phase_a_pid=$!; register_candidate phase_a_next "$phase_a_pid" "$phase_a_launch_marker" "$phase_a_launch_generation" || { runtime_hold PHASE_A_CANDIDATE_REGISTER "Phase A candidate registration evidence failed"; return 1; }
  record_identity phase_a_next "$phase_a_pid" || { phase_a_state=UNRESOLVED; runtime_hold PHASE_A_CANDIDATE_IDENTITY "Phase A identity unavailable"; return 1; }
  printf '%s\n' "$phase_a_pid" > "$(root_artifact_path next-phase-a.pid)" || { runtime_hold PHASE_A_PID_WRITE "Phase A PID write failed"; return 1; }
  test "$(/bin/cat "$evidence_root/next-phase-a.pid")" = "$phase_a_pid" || { runtime_hold PHASE_A_PID_REREAD "Phase A PID reread failed"; return 1; }
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    record_listener_state phase_a_next "$phase_a_pid" "$next_port"; listener_call_rc=$?
    test "$listener_evidence_write_result" != EVIDENCE_WRITE_FAILURE || { runtime_hold PHASE_A_LISTENER_EVIDENCE "Phase A listener evidence write failed"; return 1; }
    test "$listener_call_rc" -eq 0 && test "$listener_state_result" = PRESENT && break
    identity_matches phase_a_next || break
    sleep 1
  done
  identity_matches phase_a_next || { runtime_hold PHASE_A_READINESS "Phase A identity failed"; return 1; }
  record_listener_state phase_a_next "$phase_a_pid" "$next_port"; listener_call_rc=$?
  test "$listener_evidence_write_result" != EVIDENCE_WRITE_FAILURE || { runtime_hold PHASE_A_LISTENER_EVIDENCE "Phase A listener evidence write failed"; return 1; }
  test "$listener_call_rc" -eq 0 && test "$listener_state_result" = PRESENT || { runtime_hold PHASE_A_READINESS "Phase A readiness failed"; return 1; }
  phase_a_state=READY
  record_checkpoint phase-a-pre-request || { runtime_hold CHECKPOINT_PHASE_A_PRE "identity mismatch"; return 1; }
  phase_a_capture=$(node --input-type=module --eval 'import {readFileSync} from "node:fs"; const s=JSON.parse(readFileSync(process.argv[1],"utf8")); process.stdout.write(`${s.state}:${s.target_count}:${s.request_log_count}:${s.error_code}`);' "$evidence_root/capture-state.json" 2>/dev/null)
  record_listener_state capture "$capture_pid" "$capture_port"; listener_call_rc=$?
  test "$listener_evidence_write_result" != EVIDENCE_WRITE_FAILURE || { runtime_hold PHASE_A_CAPTURE_LISTENER_EVIDENCE "capture listener evidence write failed"; return 1; }
  test "$phase_a_capture" = LISTENING:0:0:null && identity_matches capture && test "$listener_call_rc" -eq 0 && test "$listener_state_result" = PRESENT || { runtime_hold PHASE_A_CAPTURE_ASSERT "capture precondition failed"; return 1; }
  phase_a_request_phase=yes
  curl --fail --silent --show-error --request GET --connect-timeout 5 --max-time 20 -H 'Accept: text/html' -D "$evidence_root/phase-a-page.headers" -o "$evidence_root/phase-a-page.html" 'http://127.0.0.1:3101/accepted-events?line_id=LINE_RUNTIME_001&start_time=2026-07-05T00%3A00%3A00Z&end_time=2026-07-05T01%3A00%3A00Z&limit=50&cursor=runtime-opaque-cursor' || { runtime_hold PHASE_A_REQUEST "Phase A request failed"; return 1; }
  /usr/bin/grep -Fq 'Accepted events service is not configured.' "$evidence_root/phase-a-page.html" || { runtime_hold PHASE_A_SAFE_PAGE "safe page absent"; return 1; }
  for forbidden_value in '<table' 'runtime-next-cursor-001' 'sha256:runtime-fixture-fact' 'RUNTIME_NOK' 'RUNTIME_DETAIL' 'UNIT-RUNTIME-FIXTURE-001' 'DMC-RUNTIME-FIXTURE-001'; do ! /usr/bin/grep -Fq "$forbidden_value" "$evidence_root/phase-a-page.html" || { runtime_hold PHASE_A_LEAK "fixture leaked: $forbidden_value"; return 1; }; done
  phase_a_capture=$(node --input-type=module --eval 'import {readFileSync} from "node:fs"; const s=JSON.parse(readFileSync(process.argv[1],"utf8")); process.stdout.write(`${s.state}:${s.target_count}:${s.request_log_count}:${s.error_code}`);' "$evidence_root/capture-state.json" 2>/dev/null)
  test "$phase_a_capture" = LISTENING:0:0:null || { runtime_hold PHASE_A_CAPTURE_POST "capture was contacted or errored"; return 1; }
  cleanup_role phase_a_next "$next_port"; cleanup_call_rc=$?; cleanup_result_phase_a=$cleanup_role_result
  test "$cleanup_result_phase_a" = TERM_SENT_AND_EXITED || test "$cleanup_result_phase_a" = LISTENER_LOST_BUT_TERMINATED || { runtime_hold PHASE_A_TERM "$cleanup_result_phase_a"; return 1; }
  port_release_check next "$next_port"; cleanup_call_rc=$?; port_release_result_next=$port_release_result; test "$port_release_result_next" = released || { runtime_hold PHASE_A_PORT "$port_release_result_next"; return 1; }
  record_checkpoint phase-a-post-stop || { runtime_hold CHECKPOINT_PHASE_A_POST "identity mismatch"; return 1; }

  runtime_launch_generation=$((runtime_launch_generation + 1))
  phase_b_launch_generation=$runtime_launch_generation
  construct_launch_marker phase_b_next "$phase_b_launch_generation" || { runtime_hold PHASE_B_MARKER_CONSTRUCTION "Phase B marker construction failed"; return 1; }
  phase_b_launch_marker=$constructed_marker
  validate_root_identity || { runtime_hold ROOT_IDENTITY "root identity changed before Phase B launch"; return 1; }
  ( cd "$frontend_root/.next/standalone" && exec env EDGE_MES_DASHBOARD_API_ORIGIN=http://127.0.0.1:3100 EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=local HOSTNAME=127.0.0.1 PORT="$next_port" node server.js -- "$phase_b_launch_marker" ) > "$(root_artifact_path phase-b-next.log)" 2>&1 &
  phase_b_pid=$!; register_candidate phase_b_next "$phase_b_pid" "$phase_b_launch_marker" "$phase_b_launch_generation" || { runtime_hold PHASE_B_CANDIDATE_REGISTER "Phase B candidate registration evidence failed"; return 1; }
  record_identity phase_b_next "$phase_b_pid" || { phase_b_state=UNRESOLVED; runtime_hold PHASE_B_CANDIDATE_IDENTITY "Phase B identity unavailable"; return 1; }
  printf '%s\n' "$phase_b_pid" > "$(root_artifact_path next-phase-b.pid)" || { runtime_hold PHASE_B_PID_WRITE "Phase B PID write failed"; return 1; }
  test "$(/bin/cat "$evidence_root/next-phase-b.pid")" = "$phase_b_pid" && test "$phase_b_pid" != "$phase_a_pid" || { runtime_hold PHASE_B_PID_REREAD "Phase B PID reread/reuse failed"; return 1; }
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    record_listener_state phase_b_next "$phase_b_pid" "$next_port"; listener_call_rc=$?
    test "$listener_evidence_write_result" != EVIDENCE_WRITE_FAILURE || { runtime_hold PHASE_B_LISTENER_EVIDENCE "Phase B listener evidence write failed"; return 1; }
    test "$listener_call_rc" -eq 0 && test "$listener_state_result" = PRESENT && break
    identity_matches phase_b_next || break
    sleep 1
  done
  identity_matches phase_b_next || { runtime_hold PHASE_B_READINESS "Phase B identity failed"; return 1; }
  record_listener_state phase_b_next "$phase_b_pid" "$next_port"; listener_call_rc=$?
  test "$listener_evidence_write_result" != EVIDENCE_WRITE_FAILURE || { runtime_hold PHASE_B_LISTENER_EVIDENCE "Phase B listener evidence write failed"; return 1; }
  test "$listener_call_rc" -eq 0 && test "$listener_state_result" = PRESENT || { runtime_hold PHASE_B_READINESS "Phase B readiness failed"; return 1; }
  phase_b_state=READY
  record_checkpoint phase-b-pre-request || { runtime_hold CHECKPOINT_PHASE_B_PRE "identity mismatch"; return 1; }
  capture_request_phase=yes
  phase_b_request_phase=yes
  curl --fail --silent --show-error --request GET --connect-timeout 5 --max-time 20 -H 'Accept: text/html' -D "$evidence_root/phase-b-page.headers" -o "$evidence_root/phase-b-page.html" 'http://127.0.0.1:3101/accepted-events?line_id=LINE_RUNTIME_001&start_time=2026-07-05T00%3A00%3A00Z&end_time=2026-07-05T01%3A00%3A00Z&limit=50&cursor=runtime-opaque-cursor' || { runtime_hold PHASE_B_REQUEST "Phase B request failed"; return 1; }
  completion_wait_result=TIMEOUT
  for completion_attempt in 1 2 3 4 5 6 7 8 9 10; do
    test "$runtime_interrupted" = no || { runtime_hold PHASE_B_COMPLETION_SIGNAL "signal received during bounded completion wait"; return 1; }
    identity_matches capture || { runtime_hold PHASE_B_COMPLETION_IDENTITY "capture identity lost during bounded completion wait"; return 1; }
    test -f "$evidence_root/capture-state.json" && test ! -L "$evidence_root/capture-state.json" || { runtime_hold PHASE_B_COMPLETION_STATE_ARTIFACT "capture-state is absent, linked or non-regular"; return 1; }
    capture_completion_snapshot=$(node --input-type=module --eval 'import {readFileSync} from "node:fs"; const s=JSON.parse(readFileSync(process.argv[1],"utf8")); process.stdout.write([s.state,s.target_count,s.request_log_count,String(s.error_code),String(s.terminal),String(s.accepting),String(s.response_error_seen),String(s.response_completion_committed),String(s.response_write_started)].join("|"));' "$evidence_root/capture-state.json" 2>/dev/null)
    capture_completion_snapshot_rc=$?
    test "$capture_completion_snapshot_rc" -eq 0 || { runtime_hold PHASE_B_COMPLETION_STATE_READ "capture-state read/parse failed during bounded completion wait"; return 1; }
    IFS='|' read -r capture_last_state capture_last_target_count capture_last_log_count capture_last_error_code capture_terminal_flag capture_accepting_flag capture_response_error_seen capture_response_completion_committed capture_response_write_started <<EOF
$capture_completion_snapshot
EOF
    response_evidence_final_state=ABSENT_OR_INVALID
    test -f "$evidence_root/capture-response-evidence.json" && test ! -L "$evidence_root/capture-response-evidence.json" && response_evidence_final_state=REGULAR_NON_LINK
    response_evidence_tmp_state=ABSENT_NOT_LINK
    if test -e "$evidence_root/capture-response-evidence.tmp" || test -L "$evidence_root/capture-response-evidence.tmp"; then
      response_evidence_tmp_state=PRESENT_OR_LINK
    fi
    case "$capture_last_state" in
      ERROR|TERMINATING|TERMINATED)
        runtime_hold PHASE_B_COMPLETION_TERMINAL "capture entered $capture_last_state during bounded completion wait"
        return 1
        ;;
    esac
    if test "$capture_last_state" = TARGET_REQUEST_COMPLETE && test "$response_evidence_final_state" != REGULAR_NON_LINK; then
      runtime_hold PHASE_B_COMPLETION_EVIDENCE "complete state exists without regular non-link response evidence"
      return 1
    fi
    if test "$capture_last_state" = TARGET_REQUEST_COMPLETE && test "$response_evidence_tmp_state" != ABSENT_NOT_LINK; then
      runtime_hold PHASE_B_COMPLETION_TMP "response evidence tmp remains after complete state"
      return 1
    fi
    if test "$capture_last_state" = TARGET_REQUEST_COMPLETE && \
      test "$capture_last_target_count" = 1 && \
      test "$capture_last_log_count" = 1 && \
      test "$capture_last_error_code" = null && \
      test "$capture_terminal_flag" = false && \
      test "$capture_accepting_flag" = false && \
      test "$capture_response_error_seen" = false && \
      test "$capture_response_completion_committed" = true && \
      test "$capture_response_write_started" = true && \
      test "$response_evidence_final_state" = REGULAR_NON_LINK && \
      test "$response_evidence_tmp_state" = ABSENT_NOT_LINK; then
      completion_wait_result=COMPLETE
      break
    fi
    if test "$completion_attempt" -lt "$completion_wait_attempts"; then sleep "$completion_wait_interval"; fi
  done
  test "$completion_wait_result" = COMPLETE || { runtime_hold PHASE_B_COMPLETION_TIMEOUT "bounded response-completion wait timed out"; return 1; }
phase_b_lineage_values=$(EXPECTED_FIXTURE_SHA256="$expected_fixture_sha256" EXPECTED_FIXTURE_BYTES="$expected_fixture_bytes" PHASE_B_STATE="$evidence_root/capture-state.json" PHASE_B_LOG="$evidence_root/capture-requests.jsonl" PHASE_B_FIXTURE="$evidence_root/fixture.json" PHASE_B_RESPONSE_EVIDENCE="$evidence_root/capture-response-evidence.json" PHASE_B_RESPONSE_EVIDENCE_TMP="$evidence_root/capture-response-evidence.tmp" node --input-type=module --eval '
import {lstatSync,readFileSync} from "node:fs"; import {createHash} from "node:crypto";
const expectedSha256=process.env.EXPECTED_FIXTURE_SHA256,expectedBytes=Number(process.env.EXPECTED_FIXTURE_BYTES),s=JSON.parse(readFileSync(process.env.PHASE_B_STATE,"utf8")),response=JSON.parse(readFileSync(process.env.PHASE_B_RESPONSE_EVIDENCE,"utf8")); const exactOwn=(value,keys)=>Object.keys(value).length===keys.length&&keys.every(key=>Object.prototype.hasOwnProperty.call(value,key)); const stateKeys=["state","target_count","request_log_count","last_stage","error_code","error_message","terminal","accepting","response_error_seen","response_completion_committed","response_write_started"]; if(!exactOwn(s,stateKeys)||s.state!=="TARGET_REQUEST_COMPLETE"||s.target_count!==1||s.request_log_count!==1||s.error_code!==null||s.terminal!==false||s.accepting!==false||s.response_error_seen!==false||s.response_completion_committed!==true||s.response_write_started!==true)throw new Error("capture terminal state"); const responseTmpPresent=(()=>{try{lstatSync(process.env.PHASE_B_RESPONSE_EVIDENCE_TMP);return true;}catch(error){if(error?.code==="ENOENT")return false;throw error;}})(); if(responseTmpPresent||!lstatSync(process.env.PHASE_B_RESPONSE_EVIDENCE).isFile())throw new Error("response evidence path state"); const lines=readFileSync(process.env.PHASE_B_LOG,"utf8").trim().split("\n");if(lines.length!==1||!lines[0])throw new Error("log cardinality");const e=JSON.parse(lines[0]),expectedQuery=new Map([["line_id","LINE_RUNTIME_001"],["start_time","2026-07-05T00:00:00Z"],["end_time","2026-07-05T01:00:00Z"],["limit","50"],["cursor","runtime-opaque-cursor"]]);if(e.method!=="GET"||e.pathname!=="/api/v2/production/accepted-station-events"||e.host!=="127.0.0.1:3100"||e.target!==true||!Array.isArray(e.query_entries)||e.query_entries.length!==5)throw new Error("request shape");const actual=new Map(e.query_entries);if(actual.size!==expectedQuery.size)throw new Error("query cardinality");for(const [key,value] of expectedQuery)if(actual.get(key)!==value)throw new Error("query "+key);for(const key of actual.keys())if(!expectedQuery.has(key))throw new Error("unknown "+key);const fixture=readFileSync(process.env.PHASE_B_FIXTURE),postSha256=createHash("sha256").update(fixture).digest("hex"),postBytes=fixture.byteLength;const responseKeys=["record_stage","response_completed","fixture_sha256_expected","fixture_bytes_expected","capture_read_sha256","capture_read_bytes","served_body_sha256","served_body_bytes","item_count","item_key_count","target_request_ordinal"];if(!exactOwn(response,responseKeys)||response.record_stage!=="RESPONSE_COMPLETE"||response.response_completed!==true||response.item_count!==1||response.item_key_count!==22||response.target_request_ordinal!==1)throw new Error("response evidence shape");const digests=[expectedSha256,response.fixture_sha256_expected,response.capture_read_sha256,response.served_body_sha256,postSha256,e.fixture_sha256_expected,e.capture_read_sha256,e.served_body_sha256];const bytes=[expectedBytes,response.fixture_bytes_expected,response.capture_read_bytes,response.served_body_bytes,postBytes,e.served_body_bytes];if(digests.some(value=>value!==expectedSha256)||bytes.some(value=>value!==expectedBytes))throw new Error("fixture lineage mismatch");process.stdout.write(postSha256+" "+postBytes);
  ')
  phase_b_lineage_rc=$?
  test "$phase_b_lineage_rc" -eq 0 || { fixture_lineage_result=FAIL; capture_response_evidence_state=NOT_COMPLETE; runtime_hold FIXTURE_LINEAGE_MISMATCH "post-request fixture/response/request lineage assertion failed"; return 1; }
  IFS=' ' read -r post_request_fixture_sha256 post_request_fixture_bytes <<EOF
$phase_b_lineage_values
EOF
  fixture_lineage_result=PASS
  capture_response_evidence_state=RESPONSE_COMPLETE
  identity_matches capture || { runtime_hold PHASE_B_CAPTURE_IDENTITY "capture identity changed"; return 1; }
  for ready_value in '<table' 'Accepted events page summary' 'Accepted NOK detail evidence' 'Accepted fact trace references' 'UNIT-RUNTIME-FIXTURE-001' 'DMC-RUNTIME-FIXTURE-001' 'business-profile-runtime-fixture' 'sha256:runtime-fixture-fact' 'RUNTIME_NOK' 'RUNTIME_DETAIL'; do /usr/bin/grep -Fq "$ready_value" "$evidence_root/phase-b-page.html" || { runtime_hold PHASE_B_READY_PAGE "ready value absent: $ready_value"; return 1; }; done
  cleanup_role phase_b_next "$next_port"; cleanup_call_rc=$?; cleanup_result_phase_b=$cleanup_role_result
  test "$cleanup_result_phase_b" = TERM_SENT_AND_EXITED || test "$cleanup_result_phase_b" = LISTENER_LOST_BUT_TERMINATED || { runtime_hold PHASE_B_TERM "$cleanup_result_phase_b"; return 1; }
  port_release_check next "$next_port"; cleanup_call_rc=$?; port_release_result_next=$port_release_result; test "$port_release_result_next" = released || { runtime_hold PHASE_B_PORT "$port_release_result_next"; return 1; }
  record_checkpoint phase-b-post-stop || { runtime_hold CHECKPOINT_PHASE_B_POST "identity mismatch"; return 1; }

  cleanup_role capture "$capture_port"; cleanup_call_rc=$?; cleanup_result_capture=$cleanup_role_result
  test "$cleanup_result_capture" = TERM_SENT_AND_EXITED || test "$cleanup_result_capture" = LISTENER_LOST_BUT_TERMINATED || { runtime_hold CAPTURE_TERM "$cleanup_result_capture"; return 1; }
  port_release_check capture "$capture_port"; cleanup_call_rc=$?; port_release_result_capture=$port_release_result
  port_release_check next "$next_port"; cleanup_call_rc=$?; port_release_result_next=$port_release_result
  test "$port_release_result_capture" = released && test "$port_release_result_next" = released || { runtime_hold FINAL_PORT_RELEASE "capture=$port_release_result_capture next=$port_release_result_next"; return 1; }
  record_checkpoint pre-success-cleanup || { runtime_hold CHECKPOINT_PRE_CLEANUP "identity mismatch"; return 1; }
  test "$(/usr/bin/grep -c '^label=' "$evidence_root/build-identity.txt")" = 6 || { runtime_hold CHECKPOINT_CARDINALITY "six checkpoint records absent"; return 1; }
  validate_retained_root_visibility || { runtime_hold RETAINED_ROOT_VISIBILITY "run-specific root or private parent identity invalid before success finalization"; return 1; }
  validate_manifest_mapping ACTIVE || { runtime_hold MANIFEST_ACTIVE_MAPPING "ACTIVE manifest mapping changed before success finalization"; return 1; }
  runtime_success_ready=yes
  return 0
}

runtime_success_finalize() {
  test "$runtime_success_ready" = yes || return 1
  validate_root_identity || { runtime_hold ROOT_IDENTITY "root identity changed before success finalizer"; return 1; }
  validate_retained_root_visibility || { runtime_hold RETAINED_ROOT_VISIBILITY "run-specific root or private parent changed at success-finalizer entry"; return 1; }
  validate_manifest_mapping ACTIVE || { runtime_hold MANIFEST_ACTIVE_MAPPING "ACTIVE manifest mapping invalid at success-finalizer entry"; return 1; }

  # Phase 1: validate source state and recorded task-owned identity. No rename or deletion is allowed here.
  /usr/bin/grep -Fxq '.next=absent-not-link' "$evidence_root/artifact-prestate.txt" || { runtime_hold SUCCESS_PRESTATE_NEXT ".next pre-state changed"; return 1; }
  /usr/bin/grep -Fxq 'next-env.d.ts=absent-not-link' "$evidence_root/artifact-prestate.txt" || { runtime_hold SUCCESS_PRESTATE_NEXT_ENV "next-env.d.ts pre-state changed"; return 1; }
  /usr/bin/grep -Fxq 'tsconfig.tsbuildinfo=absent-not-link' "$evidence_root/artifact-prestate.txt" || { runtime_hold SUCCESS_PRESTATE_TSB "tsconfig.tsbuildinfo pre-state changed"; return 1; }
  /usr/bin/grep -Fxq 'quarantine-next=absent-not-link' "$evidence_root/artifact-prestate.txt" || { runtime_hold SUCCESS_PRESTATE_QUARANTINE_NEXT "next quarantine pre-state changed"; return 1; }
  /usr/bin/grep -Fxq 'quarantine-next-env.d.ts=absent-not-link' "$evidence_root/artifact-prestate.txt" || { runtime_hold SUCCESS_PRESTATE_QUARANTINE_NEXT_ENV "next-env quarantine pre-state changed"; return 1; }
  /usr/bin/grep -Fxq 'quarantine-tsconfig.tsbuildinfo=absent-not-link' "$evidence_root/artifact-prestate.txt" || { runtime_hold SUCCESS_PRESTATE_QUARANTINE_TSB "tsbuildinfo quarantine pre-state changed"; return 1; }
  validate_recorded_ownership next "$frontend_root/.next" || { runtime_hold SUCCESS_SOURCE_IDENTITY_NEXT "current .next source is not the recorded task-owned artifact"; return 1; }
  validate_recorded_ownership next_env "$frontend_root/next-env.d.ts" || { runtime_hold SUCCESS_SOURCE_IDENTITY_NEXT_ENV "current next-env.d.ts source is not the recorded task-owned artifact"; return 1; }
  validate_recorded_ownership tsbuildinfo "$frontend_root/tsconfig.tsbuildinfo" || { runtime_hold SUCCESS_SOURCE_IDENTITY_TSB "current tsconfig.tsbuildinfo source is not the recorded task-owned artifact"; return 1; }

  # Phase 2: atomically hand off only created artifacts to their fixed same-parent quarantine.
  ownership_handoff_stage=PHASE_2_IN_PROGRESS
  atomic_artifact_handoff next || return 1
  atomic_artifact_handoff next_env || return 1
  atomic_artifact_handoff tsbuildinfo || return 1
  ownership_handoff_stage=PHASE_2_COMPLETE

  # Phase 3: verify source absence and the exact recorded identity at every quarantine.
  ownership_verification_result=PHASE_3_IN_PROGRESS
  verify_artifact_handoff next || { ownership_verification_result=FAIL; return 1; }
  verify_artifact_handoff next_env || { ownership_verification_result=FAIL; return 1; }
  verify_artifact_handoff tsbuildinfo || { ownership_verification_result=FAIL; return 1; }
  ownership_verification_result=PASS

  # Phase 4: delete only quarantines that passed Phase 3 and a fresh pre-delete identity check.
  deletion_stage=PHASE_4_IN_PROGRESS
  delete_verified_quarantine next || { deletion_stage=PHASE_4_FAILED; return 1; }
  case "$build_artifact_next_env" in
    CREATED_REGULAR_FILE) delete_verified_quarantine next_env || { deletion_stage=PHASE_4_FAILED; return 1; } ;;
    NOT_CREATED) : ;;
    *) runtime_hold DELETE_QUARANTINE_NEXT_ENV_CLASSIFICATION "next-env.d.ts classification changed before deletion"; return 1 ;;
  esac
  case "$build_artifact_tsbuildinfo" in
    CREATED_REGULAR_FILE) delete_verified_quarantine tsbuildinfo || { deletion_stage=PHASE_4_FAILED; return 1; } ;;
    NOT_CREATED) : ;;
    *) runtime_hold DELETE_QUARANTINE_TSB_CLASSIFICATION "tsconfig.tsbuildinfo classification changed before deletion"; return 1 ;;
  esac
  deletion_stage=PHASE_4_COMPLETE

  # Phase 5: all source and quarantine paths must be absent and not links before success.
  postcondition_result=PHASE_5_IN_PROGRESS
  test ! -e "$frontend_root/.next" && test ! -L "$frontend_root/.next" || { postcondition_result=FAIL; runtime_hold FINAL_SOURCE_POSTCONDITION_NEXT ".next source postcondition failed"; return 1; }
  test ! -e "$frontend_root/next-env.d.ts" && test ! -L "$frontend_root/next-env.d.ts" || { postcondition_result=FAIL; runtime_hold FINAL_SOURCE_POSTCONDITION_NEXT_ENV "next-env.d.ts source postcondition failed"; return 1; }
  test ! -e "$frontend_root/tsconfig.tsbuildinfo" && test ! -L "$frontend_root/tsconfig.tsbuildinfo" || { postcondition_result=FAIL; runtime_hold FINAL_SOURCE_POSTCONDITION_TSB "tsconfig.tsbuildinfo source postcondition failed"; return 1; }
  test ! -e "$quarantine_next" && test ! -L "$quarantine_next" || { postcondition_result=FAIL; runtime_hold FINAL_QUARANTINE_POSTCONDITION_NEXT ".next quarantine postcondition failed"; return 1; }
  test ! -e "$quarantine_next_env" && test ! -L "$quarantine_next_env" || { postcondition_result=FAIL; runtime_hold FINAL_QUARANTINE_POSTCONDITION_NEXT_ENV "next-env quarantine postcondition failed"; return 1; }
  test ! -e "$quarantine_tsbuildinfo" && test ! -L "$quarantine_tsbuildinfo" || { postcondition_result=FAIL; runtime_hold FINAL_QUARANTINE_POSTCONDITION_TSB "tsbuildinfo quarantine postcondition failed"; return 1; }
  postcondition_result=PASS

  # Success retains the run-specific physical root. There is no evidence-root
  # rm loop, rmdir, recursive deletion, legacy-root mutation, or private-parent
  # cleanup in the canonical runtime. Cleanup requires a separate exact gate.
  validate_root_identity || { runtime_hold ROOT_IDENTITY "root CWD identity changed before success retention"; return 1; }
  validate_retained_root_visibility || { runtime_hold RETAINED_ROOT_VISIBILITY "run-specific root or private parent changed before success summary"; return 1; }
  validate_manifest_mapping ACTIVE || { runtime_hold MANIFEST_ACTIVE_MAPPING "ACTIVE manifest mapping changed before success summary"; return 1; }
  write_evidence_summary || { runtime_hold SUMMARY_WRITE "pre-terminal evidence summary write failed"; return 1; }
  validate_evidence_summary_readback || { runtime_hold SUMMARY_READBACK "pre-terminal evidence summary exact readback failed"; return 1; }
  validate_retained_root_visibility || { runtime_hold RETAINED_ROOT_VISIBILITY "run-specific root or private parent changed before terminal evidence output"; return 1; }
  validate_manifest_mapping ACTIVE || { runtime_hold MANIFEST_ACTIVE_MAPPING "ACTIVE manifest mapping changed before terminal evidence output"; return 1; }
  /bin/cat "$evidence_root/build-identity.txt" "$evidence_root/evidence-summary.txt" || { runtime_hold TERMINAL_EVIDENCE "cannot emit terminal evidence"; return 1; }
  validate_retained_root_visibility || { runtime_hold RETAINED_ROOT_VISIBILITY "run-specific root or private parent changed before SUCCESS manifest publication"; return 1; }
  terminal_pass_line_prefix="PASS: run-specific evidence root retained; run_nonce=$runtime_run_nonce logical=$logical_root canonical=$canonical_root dev=$root_device inode=$root_inode manifest=$logical_manifest_report_path private_parent_marker_digest=$private_parent_marker_digest root_ownership_marker_digest=$root_ownership_marker_digest defends=T1,T2,T3 does_not_claim=T4,T5 atomic_mkdir_open=$atomic_mkdir_open_claim cleanup=NOT_EXECUTED_NOT_AUTHORIZED"
  # From this boundary until terminal exit, INT/TERM/HUP cannot re-enter failure
  # dispatch. Any uncertain helper result is reconciled read-only before either
  # restoring failure traps or committing exit 0.
  runtime_ignore_terminal_traps
  terminal_commit_state=TERMINAL_COMMITTING
  publish_run_manifest SUCCESS
  terminal_publish_rc=$?
  if test "$terminal_publish_rc" -eq 0 && test "$manifest_publication_result" = PASS && test "$manifest_confirmed_state" = SUCCESS; then
    terminal_commit_state=SUCCESS_COMMITTED
    emit_terminal_pass
    exit 0
  fi
  reconcile_manifest_after_publication_failure
  terminal_reconcile_rc=$?
  if test "$terminal_reconcile_rc" -eq 0 && test "$manifest_reconciliation_state" = SUCCESS && test "$manifest_confirmed_state" = SUCCESS; then
    terminal_commit_state=SUCCESS_COMMITTED
    emit_terminal_pass
    exit 0
  fi
  case "$manifest_reconciliation_state" in
    ACTIVE)
      terminal_commit_state=PRE_TERMINAL
      runtime_failure_code=MANIFEST_SUCCESS_NOT_COMMITTED
      runtime_failure_reason="SUCCESS publication did not commit; reconciled manifest remains ACTIVE"
      runtime_install_failure_traps
      return 1
      ;;
    FAILURE)
      terminal_commit_state=TERMINAL_FAILURE_COMMITTED
      runtime_failure_code=MANIFEST_ALREADY_FAILURE
      runtime_failure_reason="manifest is already FAILURE after SUCCESS publication uncertainty"
      write_failure_state || printf 'HOLD: failure-state exact write/readback failed\n' >&2
      emit_hold_output >&2
      printf 'HOLD: manifest is already FAILURE; process exits nonzero and no SUCCESS overwrite is attempted\n' >&2
      exit 1
      ;;
    UNKNOWN|*)
      terminal_commit_state=TERMINAL_UNKNOWN
      runtime_failure_code=MANIFEST_RECONCILIATION_UNKNOWN
      runtime_failure_reason="terminal manifest state is UNKNOWN after SUCCESS publication uncertainty"
      write_failure_state || printf 'HOLD: failure-state exact write/readback failed\n' >&2
      emit_hold_output >&2
      printf 'HOLD: terminal manifest state UNKNOWN; no overwrite/no cleanup; manual review required\n' >&2
      exit 1
      ;;
  esac
}

runtime_evidence_main
runtime_rc=$?
if test "$runtime_rc" -ne 0; then
  runtime_common_failure_dispatch
  if test "$terminal_commit_state" = SUCCESS_COMMITTED; then
    emit_terminal_pass
    exit 0
  fi
  printf 'HOLD[%s]: %s\n' "$runtime_failure_code" "$runtime_failure_reason" >&2
  test "$runtime_signal_exit_code" -eq 0 || exit "$runtime_signal_exit_code"
  trap - INT TERM HUP
  exit 1
fi
runtime_success_finalize
success_cleanup_rc=$?
if test "$success_cleanup_rc" -ne 0; then
  test -n "$runtime_failure_code" || runtime_hold SUCCESS_CLEANUP "success cleanup failed; remaining artifacts retained"
  runtime_common_failure_dispatch
  if test "$terminal_commit_state" = SUCCESS_COMMITTED; then
    emit_terminal_pass
    exit 0
  fi
  test "$runtime_signal_exit_code" -eq 0 || exit "$runtime_signal_exit_code"
  trap - INT TERM HUP
  exit 1
fi
runtime_hold SUCCESS_FINALIZER_RETURN "terminal finalizer returned without a terminal commit"
runtime_common_failure_dispatch
trap - INT TERM HUP
exit 1
```

## 15. R2 finding closure

| Finding | Root cause | Planning repair and canonical location | Remaining risk | Status |
| --- | --- | --- | --- | --- |
| R2-P1 | A launch-bound candidate could be ignored when identity/evidence/PID-file/readiness work failed. | `register_candidate` records `$!`, control-shell PID, role, current run nonce, exact role marker, generation and `LAUNCHED_CANDIDATE` immediately; `candidate_identity_matches` permits TERM only before request phase when original PID, PPID, generation, recomputed marker and role command structure still match. PID-file read/write is evidence only. | Any mismatch is `IDENTITY_UNRESOLVED`, never signal; dispatcher still cleans the other roles. | **CLOSED IN PLANNING AUTHORITY** |
| R2-P2 | Command-substitution cleanup ran in a subshell, losing child/reap/state authority and accepting wait `127`. | Every `cleanup_role` and port-release call is a current-shell call with explicit `cleanup_call_rc` and global result; successful and already-exited children receive exact parent-shell `wait`; `127` is `WAIT_NOT_CHILD`; `REAPED` freezes repeat dispatches. | TERM timeout, wait failure, or unresolved identity remains HOLD after independent attempts. | **CLOSED IN PLANNING AUTHORITY** |
| R2-P3 | Listener evidence append failure could still be treated as listener success. | `record_listener_state` sets `listener_state_result` plus `listener_evidence_write_result`; append failure becomes `EVIDENCE_WRITE_FAILURE`, runtime phases HOLD, and cleanup records HOLD while still TERMing a separately verified process. | An evidence-write failure prevents PASS and retains evidence; it never becomes process ownership. | **CLOSED IN PLANNING AUTHORITY** |
| R2-P4 | Success cleanup required optional auxiliary build artifacts. | `classify_generated_artifact` records `CREATED_DIRECTORY`, `CREATED_REGULAR_FILE`, `NOT_CREATED`, or `TYPE_OR_LINK_MISMATCH`; created artifacts are handed off to fixed quarantines, auxiliaries are deleted only when their recorded quarantine identity verifies, and `NOT_CREATED` paths remain absent/not-link. | Build nonzero/type-link mismatch, handoff mismatch or postcondition drift retains partial artifacts and HOLDs. | **CLOSED IN PLANNING AUTHORITY** |

## 16. Round-3 and Round-4 finding closure

### REL-RUNTIME-RR1

- root cause: `NOT_CREATED` auxiliary classification was accepted by the success finalizer without a second `! -e` and `! -L` proof immediately before success deletion.
- literal repair location: section 14 `runtime_success_finalize`, explicit Phase 1 validation cases for `next-env.d.ts` and `tsconfig.tsbuildinfo`, before the Phase 2 deletion block.
- final `NOT_CREATED` guards: `next-env.d.ts` uses `test ! -e "$frontend_root/next-env.d.ts" && test ! -L "$frontend_root/next-env.d.ts"`; `tsconfig.tsbuildinfo` uses `test ! -e "$frontend_root/tsconfig.tsbuildinfo" && test ! -L "$frontend_root/tsconfig.tsbuildinfo"`.
- remaining risk: future runtime execution, build behavior and filesystem evidence remain unauthorized; this repair proves only the planning authority sequence.
- status: **CLOSED IN PLANNING AUTHORITY**

### REL-RUNTIME-RR2

- root cause: the prior candidate fallback depended on a repeatable per-role marker and argv substring matching, so a same-shell unknown child could satisfy a weak marker check.
- nonce generation: section 14 `runtime_evidence_main` generates one `randomBytes(32).toString("hex")` nonce, validates exit status, 64-character length and lowercase hexadecimal format, and stores it in current-shell state before any capture/Next launch.
- marker construction: `construct_launch_marker` freezes `edge-mes-dashboard-url-runtime-evidence.<nonce>.<role>.<generation>` with the exact role and current role launch generation; each marker is passed as the final independent child argv token and recorded in `process-identities.txt`.
- exact argv-token check: `observed_argv_matches_role` extracts `observed_last_argv_token=${observed_argv_value##* }`, requires exact equality with the recomputed marker, requires the preceding token to be `--`, and validates capture inline `node --input-type=module --eval` or phase-specific `node server.js` structure.
- generation equality: `candidate_identity_matches` requires stored generation == current role launch generation, stored nonce == current run nonce, stored marker == the recomputed nonce/role/generation marker, exact original `$!`, original control-shell PPID, `request_phase=no`, current lifecycle state and role-specific command match.
- remaining risk: runtime candidate fallback, PID reuse race and process identity evidence still require the separately authorized Reliability planning re-review and future runtime evidence.
- status: **CLOSED IN PLANNING AUTHORITY**

### REL-RUNTIME-RR3

- explicit registration invariant: each `register_candidate` role branch freezes candidate PID, control-shell PID, role, generation, current run nonce, marker, `state=LAUNCHED_CANDIDATE`, and its role-specific `request_phase=no` in one current-shell operation; no retry or relaunch behavior is added.
- status: **CLOSED IN PLANNING AUTHORITY**

### REL-RUNTIME-RR2-1

- root cause: Phase 1 generated-path validation was followed by direct source deletion without a
  task-owned identity handoff, so a source replacement could become the deletion target and a
  `NOT_CREATED` auxiliary could appear without a final postcondition failure.
- concurrency model: one canonical lifecycle is the only task writer, with no retry/relaunch or
  second cleanup actor and one isolated evidence root; external drift at a command boundary is
  `HOLD`. This is a task-owned safety model, not a claim against a higher-privilege malicious
  host actor.
- fixed quarantine paths: `frontend/.edge-mes-runtime-evidence-next.quarantine`,
  `frontend/.edge-mes-runtime-evidence-next-env.quarantine`, and
  `frontend/.edge-mes-runtime-evidence-tsbuildinfo.quarantine`; all are preflighted as
  `! -e && ! -L` and are same-parent rename targets.
- ownership identity: after classification, `artifact-ownership.txt` records exact path,
  classification, macOS `/usr/bin/stat -f 'device=%d%ninode=%i%ntype=%HT%nsymlink_target=%Y' -- "$artifact_path"`
  device, inode, type, symlink status and record stage. `NOT_CREATED` records `absent` fields
  and no fabricated inode.
- five-phase finalization: Phase 1 validates source identity; Phase 2 uses no-overwrite atomic
  source-to-quarantine handoff; Phase 3 verifies source absence and quarantine identity; Phase 4
  revalidates quarantine identity before deleting only verified quarantines; Phase 5 proves all
  six source/quarantine paths are absent and not links.
- partial handoff failure: the first quarantine remains retained, no quarantine deletion or
  rollback rename is attempted, current source/quarantine states are written to
  `failure-state.txt`, managed-process/port cleanup still runs, and the result is `HOLD`.
- status: **CLOSED IN PLANNING AUTHORITY**

## 17. Round-5 Data Quality finding closure

### DQ-RUNTIME-D2-1

- root cause: the former here-document fixture and capture path had no frozen pre-request body
  identity, no proof that the exact Buffer passed to `res.end` matched that fixture, no
  response-completion evidence, and no post-request equality check. A second item or a
  non-marker field replacement could therefore evade marker-only HTML checks.
- single authority: section 14 has exactly one inline Node standard-library fixture generator;
  it constructs the frozen object, validates exact envelope/data/page and 22 item own keys,
  serializes once to the only response-body bytes, creates `fixture.json` with checked full
  write, then writes the atomic `fixture-identity.json` evidence with the same checked helper.
- lineage: the current shell freezes validated SHA-256/byte values and passes them to capture;
  capture reads the fixture as a Buffer, validates digest/bytes and exact one-item/22-key JSON
  shape, freezes that same Buffer as `responseBody`, records its digest, waits for the single
  guarded response completion writer, atomically writes response evidence with checked full
  write, then and only then
  commits `TARGET_REQUEST_COMPLETE`.
- post-request proof: Phase B recomputes the fixture SHA-256/byte count and requires four-way
  expected/capture-read/served/post-request equality plus request-log/response-evidence equality.
  A changed byte or field fails digest equality; an added second item fails the explicit
  `items.length===1` assertion.
- remaining risk: this is a synthetic local fixture/body lineage only. It does not prove API
  producer correctness, DB validity, adapter/collector lineage, production facts, aggregation or
  pagination behavior.
- status: **CLOSED IN PLANNING AUTHORITY**; this does not close the Data Quality gate.

### DQ-RUNTIME-D2-2

- repair: the terminal summary now uses mutually exclusive A transport/request, B frozen
  synthetic fixture, and C real production-fact wording, and carries digest/byte/item/key
  evidence without treating a digest as a production-fact identifier.
- status: **ADDRESSED IN PLANNING AUTHORITY**

### DQ-RUNTIME-D2-3

- repair: Phase B retains only the exact documented marker/value loop. The B wording explicitly
  excludes summary aggregation and pagination behavior; markers are not full-body, producer or
  pagination proof.
- status: **ADDRESSED BY CLAIM NARROWING**

Failure retains `fixture.json`, `fixture-identity.json`, any completed
`capture-response-evidence.json`, `capture-response-evidence.tmp` when partial, request log,
capture state, HTML, process/build/ownership and failure-state evidence. Success cleanup may
start only after bounded wait, all final assertions, non-empty summary and terminal evidence
output succeed; it includes the exact inventory only and no wildcard. No failure dispatcher
deletes or rewrites lineage evidence.

## 17A. Prior Round-5 static audit (retained)

All counts are restricted to the single literal Section 14 authority; prose and this closure are
excluded. The block is syntax-checked with `zsh -n` only and is never executed in this task.

| Audit | Result |
| --- | --- |
| canonical executable authority fences | 1 |
| legacy fixture here-document writers | 0 |
| single inline fixture generator / fixture writers | 1 / 1 |
| fixture identity artifacts | 1 final + 1 tmp |
| capture response evidence artifacts | 1 final + 1 tmp |
| fixture / capture-read / served-body / post-request SHA-256 | present / present / present / present |
| four-way digest and byte-count equality | present / present |
| exact fixture and response `items.length===1` assertions | 1 / 1 |
| exact 22-key assertion | fixture and response present |
| response evidence atomic write before `TARGET_REQUEST_COMPLETE` | yes |
| request-log digest fields | present |
| Phase B lineage assertion | present |
| Phase B HTML marker list | exactly documented 10 values |
| exact aggregation claims / pagination proof claims | 0 / 0 |
| cleanup command substitutions | 0 |
| `wait 127` accepted as success | 0 |
| ordinary `exit` inside `runtime_evidence_main` | 0 |
| zsh syntax | PASS |
| runtime commands executed | none |

## 17B. Prior gate note (retained)

Gate conclusion: **PASS WITH RECOMMENDATIONS**.

The planning authority now closes the fixture-to-served-body lineage gap and narrows B-class
claims. It preserves candidate identity, current-shell cleanup, wait/reap, listener evidence,
Phase A zero/Phase B exactly-one topology, same build artifact, quarantine-only deletion,
six-path postcondition, TERM-only policy and dual-port proof. It is not a Reliability re-review,
Data Quality re-review, Verification review or runtime evidence execution.

Required next action: **PM intake → separately authorize focused Reliability planning re-review**.
Do not proceed directly to Data Quality review, Verification review, runtime execution, staging,
commit, or push.

## 18. Round-6 Reliability HOLD repair finding closure

This is the Architecture / Integration planning authority for the repair. It is not a focused
Reliability re-review and does not change the preserved Round-4 HOLD.

### REL-RUNTIME-RR4-1

- status: **CLOSED IN PLANNING AUTHORITY**.
- the only success authority is `commitResponseComplete(payload)`; the response callback only
  performs its terminal guard and then calls that function.
- the writer requires, in one pre-commit guard, `terminal===false`,
  `responseErrorSeen===false`, `responseCompletionCommitted===false`,
  `responseWriteStarted===false`, `state.state==="TARGET_REQUEST_IN_PROGRESS"`, counts `0/0`,
  `accepting===false`, and absent final/tmp response-evidence paths.
- `res.once("error")` sets `responseErrorSeen=true` before `fatal`. `fatal` first sets
  `terminal=true` and `accepting=false`, and the pending success writer returns immediately
  when terminal. The duplicate-success guard rejects a second commit.
- `canTransition(current,next)` is enforced by `set()`; `ERROR`, `TERMINATING` and
  `TERMINATED` have no success transition to `TARGET_REQUEST_COMPLETE`. A state-write
  failure is fatal and cannot be converted back to success.

### REL-RUNTIME-RR4-2

- status: **CLOSED IN PLANNING AUTHORITY**.
- one checked `full_write_helper` loops over the Buffer until the exact byte length is written,
  requiring every `writeSync` result to be a positive integer and requiring final offset
  equality.
- the helper is applied to `fixture.json`, `fixture-identity.tmp`, and
  `capture-response-evidence.tmp`. Fixture generation requires fixture full write plus
  fsync/close, identity full write plus fsync/close/rename, and shell identity validation before
  the capture launch boundary.
- any short write, non-positive/non-integer write, mismatch, fsync/close/rename failure or
  identity-validation failure fails closed, best-effort closes the descriptor, retains partial
  artifacts, and keeps capture launch at zero. No partial artifact is deleted or overwritten.

### REL-RUNTIME-RR4-3

- status: **ADDRESSED IN PLANNING AUTHORITY**.
- Phase B now uses a bounded completion wait of at most 10 attempts at 1 second intervals.
  Each attempt checks runtime interruption, capture PID/PPID/role/generation identity,
  capture-state readability and exact response-evidence final/tmp path status.
- `ERROR`, `TERMINATING`, `TERMINATED`, signal, identity loss, missing/non-regular/link
  response evidence, residual tmp evidence and timeout all fail closed to `HOLD`. Timeout
  cannot be accepted as success.

### REL-RUNTIME-RR4-4

- status: **ADDRESSED IN PLANNING AUTHORITY**.
- target admission requires non-terminal `LISTENING`, `accepting===true`, counts `0/0`,
  `responseErrorSeen===false`, and `responseCompletionCommitted===false` before fixture
  read, request-log append or synthetic response. Invalid admission invokes the common fatal
  path and performs none of those operations.
- the single-writer model remains bounded to the one target handler and the one
  `commitResponseComplete` authority; no query, port, fixture business value, identity,
  cleanup or topology redesign is introduced.

### State machine and response lifecycle

| Surface | Planning authority |
| --- | --- |
| allowed normal transitions | `STARTING → LISTENING → TARGET_REQUEST_IN_PROGRESS → TARGET_REQUEST_COMPLETE → TERMINATING → TERMINATED` |
| allowed failure transitions | `STARTING/LISTENING/TARGET_REQUEST_IN_PROGRESS/TARGET_REQUEST_COMPLETE → ERROR` |
| allowed signal cleanup | Round-6 baseline preserved; Round-7 adds `STARTING/LISTENING/TARGET_REQUEST_IN_PROGRESS/TARGET_REQUEST_COMPLETE → TERMINATING → TERMINATED` |
| forbidden transitions | `ERROR → TARGET_REQUEST_COMPLETE`; `TERMINATING → TARGET_REQUEST_COMPLETE`; `TERMINATED → TARGET_REQUEST_COMPLETE` |
| terminal monotonicity | terminal flag is set before error/signal close; `set()` rejects illegal transitions; terminal states cannot be overwritten by success |
| normal cleanup | only after complete lineage assertion, `TARGET_REQUEST_COMPLETE → TERMINATING → TERMINATED` |
| response flags | `responseErrorSeen=false`, `responseCompletionCommitted=false`, `responseWriteStarted=false` initially and persisted in capture state |
| completion hook claim | Node server-side `res.end(responseBody, callback)` completion callback only; no browser-byte/network-delivery claim |

Response success commit ordering is frozen as: all guards → `responseWriteStarted=true` →
atomic checked-full-write response evidence → `responseCompletionCommitted=true` → in-memory
counts `1/1` → atomic `TARGET_REQUEST_COMPLETE` state. Evidence-write failure leaves
completion false and counts `0/0`; complete-state failure is `ERROR` and remains HOLD even
if response evidence exists.

Response error before completion records the response-error flag, enters ERROR, and makes the
pending success writer return. SIGTERM before completion sets terminal and enters
TERMINATING, then TERMINATED, with no response evidence or complete state. Uncaught exception
or rejection uses the same fatal path. Completion first followed by normal cleanup TERM is
allowed only after lineage assertion and is not treated as a callback race.

## 19. Round-6 static audit

All counts below are restricted to the single literal Section 14 authority; prose and this
closure are excluded. The block is checked with `zsh -n` only and is never executed in this
task.

| Audit | Result |
| --- | --- |
| canonical authority fences | 1 |
| response success writers | 1 (`commitResponseComplete`) |
| request admission LISTENING guard | present |
| request admission terminal guard | present |
| request admission one-request guard | present |
| response error flag | present |
| response completion committed flag | present |
| callback/finish terminal guard | present |
| callback/finish current-state guard | present |
| callback/finish response-error guard | present |
| callback/finish duplicate-success guard | present |
| terminal transition guard | present |
| ERROR-to-COMPLETE path | 0 |
| TERMINATING-to-COMPLETE path | 0 |
| TERMINATED-to-COMPLETE path | 0 |
| full-write helper | 1 |
| fixture body checked full write | present |
| fixture identity checked full write | present |
| response evidence checked full write | present |
| capture launch after full fixture/identity validation | yes |
| bounded completion wait | present (10 attempts × 1 second) |
| timeout accepted as success | 0 |
| Phase B requires response evidence | yes |
| response evidence tmp rejected | yes |
| four-way digest equality | present |
| four-way byte-count equality | present |
| request log exactly one entry | present |
| post-request fixture equality | present |
| cleanup command substitutions | 0 for cleanup calls |
| cleanup pipeline/subshell | 0 |
| `wait 127` accepted as success | 0 |
| ordinary `exit` inside `runtime_evidence_main` | 0 |
| DQ-URL-D3 closed claims | 0 |
| candidate nonce/marker and PID/PPID/role/generation identity | preserved |
| current-shell cleanup and wait/reap | preserved |
| listener evidence and Phase A/B topology | preserved |
| six build checkpoints | preserved |
| quarantine-only deletion and six-path postcondition | preserved |
| TERM-only / no KILL and dual-port proof | preserved |
| zsh syntax | PASS |
| runtime commands executed | none |

## 20. Round-6 gate conclusion and required next action (retained)

Gate conclusion: **PASS WITH RECOMMENDATIONS** for this Architecture / Integration planning
repair only.

| Gate | State |
| --- | --- |
| Architecture planning | PASS WITH RECOMMENDATIONS |
| focused Reliability round 4 | HOLD, preserved |
| Data Quality | HOLD, preserved |
| Verification | NOT AUTHORIZED |
| runtime | NOT AUTHORIZED |
| DQ-URL-D2 | HOLD / pending Data Quality re-review |
| DQ-URL-D3 | CARRY FORWARD |
| REL-URL-R6 | CARRY FORWARD |
| global gate | HOLD |

All four requested findings are literalized in this planning authority, with no scope
expansion, no runtime execution and no Git write. This report does not claim Reliability
re-review, Data Quality re-review, Verification, runtime success, staging, commit or push.

Required next action: **PM intake → separately authorize a focused Reliability planning
re-review**. Do not proceed directly to Data Quality, Verification, runtime execution, staging,
commit or push.

## 21. Round-7 capture STARTING signal cleanup closure

本节只新增 signal-cleanup authority；Round 6 的 response completion、checked full-write、
bounded completion wait、fixture/body lineage、quarantine、candidate identity、parent-shell
cleanup、Data Quality wording 与 `DQ-URL-D3: CARRY FORWARD` 均保持不变。本节仍是
Architecture / Integration planning authority，不是 focused Reliability re-review。

### PM findings

#### PM-RUNTIME-R6-1

- status: **CLOSED IN PLANNING AUTHORITY**。
- `STARTING → TERMINATING → TERMINATED` 已加入唯一 `transitionTargets`；
  `ERROR → LISTENING`、`TERMINATING → LISTENING`、`TERMINATED → LISTENING` 仍不存在。
- `terminate()` 使用 `terminationStarted` / `terminationCompleted` 区分 signal intent 与
  cleanup 完成；第一次 TERM 继续执行 state write、listener/no-listener cleanup 和终止
  state attempt，后续 TERM 不重新写 success state，也不取消第一次 close。
- `server.listen` callback 在 `set("LISTENING")` 或 `capture-ready.txt` 前受
  `terminal===false && accepting===true && state.state==="STARTING"` guard 保护；不满足时
  不写 `LISTENING`、不写 ready file，并 best-effort close。
- `server.listening` 与 `listenPending` 明确区分已监听、pending listen 和尚未调用
  `listen`；未监听路径不等待不存在的 listener close，已监听路径等待 `server.close`
  callback。两条路径都到达 child exit；parent 仍只对 exact PID 做 wait/reap。

#### PM-RUNTIME-R6-2

- status: **CLOSED IN PLANNING AUTHORITY**。
- `set("TERMINATING")` 的 catch 只记录 stderr、设置 `process.exitCode=1`，没有 early
  return；随后一定继续 server close/no-listener path，并尝试 `set("TERMINATED")`。
- `set("TERMINATED")` failure、`server.close` throw 或 close callback error 都记录 stderr、
  设置 nonzero exit，并不阻止 child process 退出；证据/cleanup 结果仍为 `HOLD`。
- state evidence failure 与 actual process cleanup 已明确解耦；该修复不授权 runtime，也
  不声称 Reliability re-review 已通过。

### Terminate lifecycle

```text
first TERM
→ if terminationCompleted: safe return
→ if terminationStarted: safe return without interrupting existing close
→ terminationStarted=true
→ terminal=true; accepting=false
→ try set(TERMINATING); on failure: stderr + exitCode=1, continue
→ server.listening=true: server.close(callback), including callback-error path
→ server.listening=false: do not wait for nonexistent listener close; pending listen receives
  best-effort close attempt and callback guard
→ try set(TERMINATED); on failure: stderr + exitCode=1, continue exit
→ terminationCompleted=true; child exits; parent waits exact PID and records actual wait status
```

### Adversarial static scenarios

| Scenario | State transition | Server action | Ready-file behavior | Child exit / parent wait-reap | HOLD / PASS behavior |
| --- | --- | --- | --- | --- | --- |
| SIGTERM before `server.listen` call | `STARTING → TERMINATING → TERMINATED` when writes succeed | no listener exists; no listen call after the pre-listen guard | no write | child exits; parent waits exact PID once; `127` is not success | PASS in planning authority; state-write failure remains HOLD |
| SIGTERM after `server.listen` call but before callback | `STARTING → TERMINATING → TERMINATED` | `server.listening=false`, pending listen gets best-effort close without waiting; late callback is guarded | no `LISTENING`, no ready file | child exits; exact PID wait/reap; no listener remains after callback guard | PASS in planning authority; close/state failure is HOLD |
| SIGTERM while state is `STARTING` | `STARTING → TERMINATING → TERMINATED` | no-listener or pending-listen branch selected by `server.listening` / `listenPending` | no ready success state | child exits; parent wait/reap completes | PASS in planning authority; evidence failure is HOLD |
| SIGTERM while `LISTENING` | `LISTENING → TERMINATING → TERMINATED` | waits for `server.close(callback)` | existing ready evidence is not rewritten; no later success state | child exits after close callback; exact PID reaped | PASS in planning authority; close/state failure is HOLD |
| SIGTERM while `TARGET_REQUEST_IN_PROGRESS` | `TARGET_REQUEST_IN_PROGRESS → TERMINATING → TERMINATED` | closes listening server; pending response callback cannot commit success | no new ready file; no response success evidence from rejected callback | child exits; parent waits/reaps exact PID | PASS in planning authority; any cleanup/evidence failure is HOLD |
| SIGTERM after `TARGET_REQUEST_COMPLETE` | `TARGET_REQUEST_COMPLETE → TERMINATING → TERMINATED` | closes listening server through callback | ready file is not rewritten | child exits; exact PID wait/reap preserved | PASS in planning authority; cleanup proof failure is HOLD |
| `TERMINATING` state write failure | in-memory intent set; state write may remain prior state; `TERMINATED` is attempted | server cleanup still runs; no early return | no ready rewrite | child exits with nonzero code; parent wait/reap can complete | **HOLD** for evidence, not stranded process |
| `TERMINATED` state write failure | `TERMINATING` or prior state → attempted `TERMINATED` write failure | listener has already been closed or was never present | no ready rewrite | child exits with nonzero code; parent records wait/reap | **HOLD** for evidence, process exit proceeds |
| `server.close` throws | `TERMINATING → attempted TERMINATED` | synchronous throw is logged; termination state is still attempted | no ready rewrite | child exits with nonzero code; exact PID wait/reap | **HOLD** for cleanup proof, no early return |
| `server.close` callback returns error | `TERMINATING → attempted TERMINATED` | callback error is logged; `TERMINATED` is still attempted | no ready rewrite | child exits with nonzero code; parent wait/reap | **HOLD** for cleanup proof, no stranded listener claim |
| listen callback fires after `terminal=true` | remains `TERMINATING`/`TERMINATED` or `ERROR`; never `LISTENING` | callback guard rejects and best-effort closes if listener became active | no `LISTENING`, no ready file | child exits; parent waits/reaps exact PID | PASS if close/state evidence succeeds; otherwise HOLD |
| `fatal(ERROR)` before listen callback | `STARTING → ERROR`; later signal may use `ERROR → TERMINATING → TERMINATED` | fatal closes best effort; late listen callback is rejected | no ready file and no restored accepting state | child exits; parent waits/reaps | **HOLD** because fatal/error evidence is retained; no false success |
| second SIGTERM while close pending | first transition remains in progress; no second state success write | first `server.close` continues; second TERM returns only after confirming started/completed distinction | no ready rewrite | child exits from first cleanup; one exact PID wait/reap | PASS in planning authority; second TERM does not block cleanup |
| second SIGTERM after `TERMINATED` | remains `TERMINATED` | safe no-op | no write | process is already exiting/exited; parent wait/reap unchanged | PASS in planning authority |

### Round-7 static audit

Counts and presence checks are restricted to the one literal Section 14 authority; no canonical
runtime, build, tests, typecheck, Next/capture, curl/browser, lsof/port, API/DB/Postgres,
Docker or Git write was executed.

| Audit | Result |
| --- | --- |
| canonical authority fences | 1 |
| STARTING-to-TERMINATING transition | present |
| ERROR-to-LISTENING | 0 |
| TERMINATING-to-LISTENING | 0 |
| TERMINATED-to-LISTENING | 0 |
| listen callback terminal guard | present |
| listen callback STARTING/current-state guard | present |
| ready write after terminal | 0 |
| terminate state-write-failure early return | 0 |
| server cleanup after TERMINATING write failure | present |
| server-not-listening termination | present |
| server-listening termination | present |
| termination started flag | present (`terminationStarted`) |
| termination completed flag | present (`terminationCompleted`) |
| second TERM blocks cleanup | 0 |
| TERM only | yes |
| KILL signal (`-KILL`) | 0 |
| response success writers | 1 (`commitResponseComplete`) |
| full-write helper | 1 |
| bounded completion wait | present (10 attempts × 1 second) |
| wait 127 success | 0 |
| cleanup command substitutions | 0 |
| DQ-URL-D3 closed claim | 0; `CARRY FORWARD` preserved |
| zsh syntax | PASS (`zsh -n`, parse-only) |
| runtime commands executed | none |

## 22. Round-7 gate conclusion and required next action

结论：**PASS WITH RECOMMENDATIONS**。

| Gate | State |
| --- | --- |
| Architecture planning | PASS WITH RECOMMENDATIONS |
| focused Reliability round 4 | HOLD, preserved |
| Data Quality | HOLD, preserved |
| Verification | NOT AUTHORIZED |
| runtime | NOT AUTHORIZED |
| DQ-URL-D2 | HOLD / pending Data Quality re-review |
| DQ-URL-D3 | CARRY FORWARD |
| REL-URL-R6 | CARRY FORWARD |
| global gate | HOLD |

两项 PM findings 仅在本 planning authority 中关闭。不得声称 focused Reliability round 5
或任何 Reliability re-review 已通过；不得进入 Data Quality、Verification、runtime、stage、
commit 或 push。

Required next action:

```text
PM intake
→ focused Reliability planning re-review round 5
```

若下一独立 Reliability re-review 仍发现 literal authority 缺口，保持同一 signal-cleanup
blocker 的 `HOLD`；不得扩大到 fixture lineage、response completion、query/ports、candidate
identity、parent-shell cleanup、artifact quarantine 或 Data Quality semantics redesign。

## 23. Thread output / context assessment

- 本次输出长度：中（planning report 已保留完整静态矩阵；窗口报告保持短）。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：本轮已完成 Architecture / Integration docs-only HOLD repair；下一步是独立
  focused Reliability planning re-review round 5，必须重新确认 live baseline 并保持
  review-only、runtime、Verification、Data Quality 与 Git action 边界隔离。

## 24. Round-8 pending-listen, wait-status and state-evidence HOLD repair

本节取代本报告中与 pending listen close、`terminationCompleted`、parent `wait` acceptance
及 capture-state write 相关的 Round-7 explanatory prose；唯一可执行 authority 仍只在
Section 14 的 fenced literal command block。未修改 fixture business values、response success
writer、fixture/body digest lineage、query、Phase A/B topology、ports、candidate identity、artifact
quarantine 或 Data Quality evidence classes。

### Lifecycle and single close authority

The capture child freezes these independently meaningful flags:

- `listenCalled`: `server.listen` has been invoked.
- `listenPending`: the listen callback or error has not yet settled.
- `listenCallbackCommitted`: the guarded `LISTENING` callback path committed.
- `closeRequested`: fatal or termination has requested closure.
- `closeStarted`: the unique `server.close` call has started.
- `closeCompleted`: its callback, an explicit listen failure, or the never-listened no-handle path
  has completed.
- `closeError`: close/listen failure retained for final failure evidence and nonzero exit.
- `terminationStarted`: the first fatal or TERM registered the joined completion continuation.
- `terminationCompleted`: the `TERMINATED` write was attempted after joined closure and the child
  exit authority was invoked.

`requestServerClose(stage,onClosed)` is the only `server.close()` authority. It joins every
waiter to one `closeWaiters` completion list; pending listen merely records `closeRequested` and
waits. A late callback therefore starts the same authority, while a listen error settles the
same authority as a non-listening failure. There is no `closeWithoutWaiting`,
`closeAfterListening`, rejected-callback close, fatal close, or terminate close outside it.

`finishTermination()` requires `closeCompleted===true`, except for the explicitly proven
never-listened path (`listenCalled===false && listenPending===false && server.listening!==true`).
It then attempts the synchronous `TERMINATED` state write, sets `terminationCompleted=true`, and
uses explicit `process.exit(process.exitCode ?? 0)`. All state and log writes preceding that exit
are synchronous. A state or close failure sets nonzero exit and remains retained evidence; it
does not cancel actual listener close.

The existing admission expression remains literal and unchanged:

```javascript
state.state !== "LISTENING"
```

It remains part of the `invalidAdmission` guard before fixture read, request log append or
response success work.

### Parent wait authority

Both child-already-exited and post-TERM wait branches record the exact wait status. `0` is the
only successful wait status. `127` yields `WAIT_NOT_CHILD`; every other nonzero status yields
`WAIT_FAILURE`. Neither branch may set `REAPED`, `ALREADY_EXITED`, `TERM_SENT_AND_EXITED`, or
`LISTENER_LOST_BUT_TERMINATED` after a nonzero status. This applies uniformly to capture,
`phase_a_next`, and `phase_b_next`.

### Capture-state full-write authority

The initial `STARTING` operation and `atom(next)` both serialize to a `Buffer`, open
`capture-state.tmp` with `"wx"`, call the existing unique checked `full_write_helper`, fsync,
close, and rename only on success. `state=next` occurs only after rename. A short write, write
failure, fsync/close/rename failure, or pre-existing tmp leaves the tmp untouched/retained,
prevents in-memory success transition, causes nonzero child exit where capture is running, and
therefore makes parent cleanup HOLD.

### PM finding disposition

#### REL-RUNTIME-RR5-1

**CLOSED IN PLANNING AUTHORITY.** One joined `requestServerClose` authority covers never-listened,
pending, active, already-closing, closed, callback-error and listen-error cases. Pending listen
cannot write `TERMINATED` or set `terminationCompleted` before the callback/error path settles;
the late callback reuses the one close path. Repeated TERM returns only after the first call has
registered that joined continuation, and child exit is explicit after joined closure.

#### REL-RUNTIME-RR5-2

**CLOSED IN PLANNING AUTHORITY.** Both parent wait branches accept only `wait_rc == 0`, reject
`127` as `WAIT_NOT_CHILD`, classify all other nonzero values as `WAIT_FAILURE`, and prevent every
success cleanup result after such failure.

#### REL-RUNTIME-RR5-3

**CLOSED IN PLANNING AUTHORITY.** Initial `STARTING` and every `atom()` state use the one checked
full-write helper with `wx` tmp creation, retained partial tmp on failure, post-rename-only
in-memory update, nonzero child exit and parent HOLD.

#### REL-RUNTIME-RR5-4

**PM INTAKE DISPOSITION: NOT ACCEPTED AS A VALID LITERAL FINDING.**

The existing section-14 admission expression already contains
`state.state !== "LISTENING"`. No Architecture repair was required. This is not a claim that
Reliability formally closed RR5-4.

### Adversarial static scenarios

| Scenario | State | Listener/process state | Wait result | Evidence retained | False PASS possibility | Gate result |
| --- | --- | --- | --- | --- | --- | --- |
| SIGTERM after listen call before callback | `TERMINATING` until settlement | `listenPending=true`; joined close requested, not started | bounded TERM wait; timeout if callback never settles | capture log/state and failure state | none: no early `TERMINATED` | HOLD unless joined close then rc 0 |
| pending callback delayed | `TERMINATING` | no second close; callback later starts unique close | wait remains bounded | state/log | none | HOLD on timeout; otherwise rc 0 required |
| pending callback never fires | `TERMINATING`, never `TERMINATED` | no child-exit authority before completion | `TERM_TIMEOUT` | all runtime evidence root | none | HOLD |
| pending listen emits error | `ERROR → TERMINATING → TERMINATED` attempted | no listener; close completed with error | nonzero child / `WAIT_FAILURE` | state/tmp/log/failure evidence | none | HOLD |
| late callback after `ERROR` | terminal failure path | guard rejects `LISTENING`; unique close starts if active | nonzero child / `WAIT_FAILURE` | ERROR and close evidence | none | HOLD |
| late callback after `TERMINATING` | remains terminal | no ready or `LISTENING`; unique close starts | exact rc required | terminal state/log | none | rc 0 only if no failure; otherwise HOLD |
| second TERM while close pending | unchanged terminal state | joins existing continuation, no second close | first wait only | existing close evidence | none | original outcome only |
| fatal starts close then TERM arrives | `ERROR → TERMINATING → TERMINATED` attempted | TERM joins fatal close authority | nonzero child / `WAIT_FAILURE` | ERROR plus failure state | none | HOLD |
| active listener close callback error | terminal path | `closeCompleted=true`, `closeError` retained | nonzero child / `WAIT_FAILURE` | close/state/log | none | HOLD |
| `TERMINATING` state short write | write failure; closure still continues | unique close remains active | nonzero child / `WAIT_FAILURE` | partial tmp and failure state | none | HOLD |
| `TERMINATED` state short write | terminal write attempted | closure already proven; explicit nonzero exit | `WAIT_FAILURE` | partial tmp and failure state | none | HOLD |
| initial `STARTING` state short write | capture launch blocked | no child listener | no child success cleanup | partial `capture-state.tmp` | none | HOLD |
| capture-state tmp already exists | state write blocked by `wx` | no overwrite/rename/in-memory change | nonzero child if running | original tmp plus state/log | none | HOLD |
| child exits rc=1 before TERM | no new success state | child gone | `WAIT_FAILURE` | runtime evidence root | none | HOLD |
| child exits rc=1 after TERM | terminal attempt may exist | child gone | `WAIT_FAILURE` | runtime evidence root | none | HOLD |
| wait rc=127 | parent authority unresolved | no success reaped state | `WAIT_NOT_CHILD` | exact wait status | none | HOLD |
| wait rc=143 | parent records abnormal status | no success cleanup result | `WAIT_FAILURE` | exact wait status | none | HOLD |
| wait rc=1 | parent records child failure | no success cleanup result | `WAIT_FAILURE` | exact wait status | none | HOLD |
| port remains bound | no success finalizer | listener/process proof unavailable | no success cleanup | evidence root retained | none | HOLD |

### Round-8 static audit

All counts are restricted to the literal Section 14 authority. Static parsing only is authorized;
no canonical runtime sequence, build, tests, typecheck, Next/capture, curl/browser, lsof/port,
API/DB/Postgres/Docker, Reliability/Data Quality re-review, Verification, stage, commit, push,
tag, deploy or rollback was executed.

| Audit | Result |
| --- | --- |
| canonical authority fences | 1 |
| request admission LISTENING guard | present |
| pending-listen close authorities | 1 |
| unjoined `server.close` paths | 0 |
| `listenCalled` flag | present |
| `listenPending` flag | present |
| `closeRequested` flag | present |
| `closeStarted` flag | present |
| `closeCompleted` flag | present |
| `TERMINATED` before `closeCompleted` | 0 |
| `terminationCompleted` before `closeCompleted` | 0 |
| late-callback alternate close path | 0 |
| second TERM bypasses unresolved close | 0 |
| explicit child exit after joined close | present |
| wait success statuses | only 0 |
| wait 127 success | 0 |
| other nonzero wait success | 0 |
| state full-write helper | present (one definition) |
| initial state checked write | present |
| `atom()` checked write | present |
| state tmp overwrite | 0 (`wx`) |
| response success writers | 1 (`commitResponseComplete`) |
| full-write helper definitions | 1 |
| bounded completion wait | present (10 attempts x 1 second) |
| TERM only | yes |
| KILL | 0 |
| DQ-URL-D3 closed claim | 0; CARRY FORWARD preserved |
| zsh syntax | PASS (parse-only) |
| runtime commands executed | none |

## 25. Round-8 gate conclusion and required next action

结论：**PASS WITH RECOMMENDATIONS**（仅限 Architecture / Integration planning authority）。

| Gate | State |
| --- | --- |
| Architecture planning | PASS WITH RECOMMENDATIONS |
| Reliability round 5 | HOLD, preserved; no re-review claim |
| Data Quality | HOLD, preserved |
| Verification | NOT AUTHORIZED |
| runtime | NOT AUTHORIZED |
| DQ-URL-D2 | HOLD / pending Data Quality re-review |
| DQ-URL-D3 | CARRY FORWARD |
| REL-URL-R6 | CARRY FORWARD |
| global gate | HOLD |

Required next action:

```text
PM intake
→ independent focused Reliability planning re-review round 6
```

Do not proceed directly to Data Quality, Verification, runtime, staging, commit or push.

## 26. Round-9 joined close settlement repair — PM-RUNTIME-R8-1

This section supersedes only the Round-8 explanation of `beginTermination()` re-entry and the
corresponding pending-listen settlement path.  Section 14 remains the sole executable literal
authority, and the revised literal there is the authority for this repair.  It does not redesign
parent wait-status handling, checked capture-state writes, fixture/response lineage, response
completion, request admission, query/ports, artifact quarantine, or Data Quality wording.

### PM-RUNTIME-R8-1 disposition

**CLOSED IN PLANNING AUTHORITY.**

- Root cause: after an initial TERM set `terminationStarted=true`, a later listen error set
  `listenPending=false` and retained `closeError`, but `fatal()` reached the former
  already-started early return before `requestServerClose()` could re-evaluate that changed
  close state.  The first invocation's joined completion waiter therefore remained stranded.
- Repair: `beginTermination(stage)` still returns immediately only after
  `terminationCompleted===true`.  If termination has already started, it now calls
  `requestServerClose(stage)` with no callback and returns.  The first invocation alone
  registers `closedError => finishTermination(...)`.
- Listen error: `server.once("error")` first clears `listenPending` and retains `closeError`;
  `fatal()` preserves `terminal=true`, `accepting=false`, and nonzero `process.exitCode`, then
  the already-started branch re-enters `requestServerClose("fatal")`.  With no pending or
  listening handle, its one close authority calls `deliverClose(closeError)`, which delivers the
  original waiter and reaches `finishTermination(..., closeError)`.
- Listen success after terminal: the callback still fails its terminal/STARTING guard, writes no
  `LISTENING` or ready file, and calls `requestServerClose("listen-callback-rejected")` without
  adding a waiter.  That call starts or joins the one `server.close` operation; its callback
  settles the original waiter.
- Never-settled pending listen: while `listenPending===true` and `server.listening!==true`, the
  close authority returns without delivery.  `closeCompleted` and `terminationCompleted` remain
  false, `TERMINATED` is not attempted, no explicit child exit occurs, and the parent bounded
  TERM wait retains `TERM_TIMEOUT` / `HOLD`.

The lifecycle distinction is now literal: `terminationStarted` records that the unique
termination completion waiter was registered; it is not permission to skip a later close-state
reevaluation.  No independent close function, second close authority, or second termination
completion waiter is introduced.

### Re-entry and single-waiter authority

```text
first beginTermination(stage)
→ terminationStarted=true; terminal=true; accepting=false
→ attempt TERMINATING
→ requestServerClose(stage, original finishTermination waiter)

later beginTermination(stage), before completion
→ requestServerClose(stage) only
→ no waiter registration; no second server.close
→ re-evaluate listenPending / server.listening / closeError
→ deliverClose may settle the original waiter
```

`deliverClose()` retains its `closeCompleted` guard and drains `closeWaiters` once.  The unique
`server.close` call remains guarded by `closeStarted`; a later TERM, fatal, callback, or error
can stimulate the authority but cannot create a second close call.  `finishTermination()` retains
its `terminationCompleted` guard, so the `TERMINATED` attempt and explicit `process.exit` remain
single-delivery actions.

### Adversarial static scenarios

Counts below are the post-condition for the named path.  `1→0` means the one original waiter was
delivered and drained; `none` means no explicit `process.exit` has been called.

| Scenario | `terminationStarted` | `closeRequested` | `listenPending` | `closeCompleted` | waiter count | `server.close` calls | exit status | False PASS risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TERM → pending listen → success callback | true | true | false | true after close callback | `1→0` | 1 | explicit 0 when no close/state failure | none |
| TERM → pending listen → listen error | true | true | false | true by `deliverClose(closeError)` | `1→0` | 0 (no listening handle) | explicit nonzero | none; parent sees `WAIT_FAILURE` |
| TERM → pending listen → callback/error never fires | true | true | true | false | 1 | 0 | none | none; bounded `TERM_TIMEOUT` is HOLD |
| second TERM before settlement | true | true | unchanged true | false | 1 | 0 | none | none; it re-evaluates without cancelling/adding |
| second TERM after listen error settlement | true then completed | true | false | true | 0 | 0 | one earlier explicit nonzero exit | none; completed guard suppresses a second exit |
| fatal after `terminationStarted` while unresolved | true | true | depends on event | only if close authority can settle | 1 until delivery | at most 1 | none until settlement; nonzero after fatal settlement | none; no duplicate waiter/close |
| listen error before any TERM | true (from `fatal`) | true | false | true by `deliverClose(closeError)` | `1→0` | 0 (no listening handle) | explicit nonzero | none; error is retained |
| listen error after TERM | true | true | false | true by original-waiter delivery | `1→0` | 0 (no listening handle) | explicit nonzero | none; no natural-exit dependency |
| active-listener close callback error | true | true | false | true | `1→0` | 1 | explicit nonzero | none; parent rejects nonzero wait |
| `finishTermination()` is stimulated twice | true | true | false | true | 0 after first delivery | at most 1 | one explicit exit | none; `terminationCompleted` guard blocks duplicate |
| `process.exit` is stimulated twice | true | true | false | true | 0 | at most 1 | one explicit exit | none; only first joined completion reaches it |

### Round-9 static audit

Static parsing is limited to the Section 14 literal command and this planning authority.  No
canonical runtime, build, tests, typecheck, Next/capture, curl/browser/lsof, port binding,
API/DB/Postgres/Docker, Reliability/Data Quality review, staging, commit, push, tag, deploy or
rollback is authorized or executed by this repair.

| Audit | Result |
| --- | --- |
| canonical authority fences | 1 |
| `requestServerClose` authorities | 1 |
| `server.close` authorities | 1 |
| termination completion waiter registrations | 1 (first invocation only) |
| already-started termination close reevaluation | present |
| already-started termination immediate no-op | 0 |
| listen-error `deliverClose(closeError)` settlement path | present |
| listen-error explicit child exit | present |
| listen-error exit code | nonzero |
| success-callback terminal path | joined to the original waiter |
| never-settled pending listen success | 0 |
| duplicate waiter | 0 |
| duplicate close | 0 |
| duplicate `finishTermination` | 0 |
| duplicate `process.exit` | 0 |
| wait success statuses | only 0 |
| initial state checked write | present |
| `atom()` checked write | present |
| request admission `LISTENING` guard | present |
| zsh syntax | PASS (`zsh -n` parse-only) |
| runtime commands executed | none |

### Round-9 gate conclusion and required next action

结论：**PASS WITH RECOMMENDATIONS**（仅限 Architecture / Integration planning authority）。

Round-8 closures remain preserved: wait success is only rc 0; initial/`atom()` state writes use
the checked full-write path; the literal `LISTENING` admission guard, single response-success
writer, fixture/response digest lineage, Data Quality A/B/C boundaries, and `DQ-URL-D3: CARRY
FORWARD` are unchanged.  This is not a Reliability re-review approval.

| Gate | State |
| --- | --- |
| Architecture planning | PASS WITH RECOMMENDATIONS |
| Reliability round 5 | HOLD, preserved; no re-review claim |
| Data Quality | HOLD, preserved |
| Verification | NOT AUTHORIZED |
| runtime | NOT AUTHORIZED |
| DQ-URL-D2 | HOLD / pending Data Quality re-review |
| DQ-URL-D3 | CARRY FORWARD |
| REL-URL-R6 | CARRY FORWARD |
| global gate | HOLD |

Required next action:

```text
PM intake
→ focused Reliability planning re-review round 6
```

Do not proceed directly to Data Quality, Verification, runtime, or Git action.

## 27. ROOT_IDENTITY Reliability HOLD repair round 3 authority

This section and the revised Section 14 literal supersede only the Round-2 statements that the
mkdir-created child was proven before adoption and that CWD-only validation was sufficient for a
successful retained-path claim. All previously closed parent-CWD, CWD-relative evidence I/O,
atomic failure-state, process cleanup, generated/quarantine cleanup, no-root-delete, fixture,
query, ports and A/B/C controls remain unchanged.

### 27.1 Created-child capture model and conservative platform boundary

Section 14 now contains one `create_and_capture_root_child` authority. In one Node process, under
the already validated parent CWD, it checks child absence, calls the single `mkdirSync`, immediately
uses non-following `lstatSync` to capture `created_root_device`, `created_root_inode` and
`created_root_type`, creates `.root-ownership.json` with exclusive `wx` semantics, and rechecks
that the child and marker still belong to the captured object. `validate_created_root_path` then
requires the current basename object and marker digest/content to equal that captured identity;
`bind_root_cwd` adopts the child only if the resulting CWD object has the same device/inode/type,
and only then assigns `root_device`, `root_inode`, `root_type`, `root_cwd_bound=yes` and
`evidence_root=.`.

The ownership marker is corroborating evidence, not standalone authority. A replacement directory
with copied marker content cannot pass unless its device/inode also equal the first captured child
identity. A symlink, file, missing marker, different Directory inode, copied marker on a different
object, digest mismatch, nonce mismatch, or CWD mismatch is HOLD; no uncertain root is deleted.

However, macOS Node `mkdirSync` does not return a directory descriptor. The interval between its
successful return and the first `lstatSync(basename)` cannot identify whether the first observed
Directory is the exact object created by that mkdir. Neither an exclusive marker nor a second stat
can reconstruct that missing identity. Section 14 therefore freezes
`created_root_binding_proof=UNPROVEN_NODE_MKDIRSYNC_NO_DIRECTORY_DESCRIPTOR` and requires
`PROVEN_ATOMIC_DIRECTORY_DESCRIPTOR` before root creation/adoption. With the currently available
primitive this gate fails closed as `ROOT_CREATE_BINDING_UNAVAILABLE` before creating a root.
It must not be changed by a runtime operator or future review without a separately designed and
reviewed primitive that returns or otherwise binds the mkdir-created object atomically.

Disposition:

```text
REL-RUNTIME-ROOT-R3:
HOLD / NOT CLOSED

Reason:
replacement before first created-object stat remains indistinguishable on the authorized platform.
The literal prevents unsafe creation/adoption instead of claiming proof that does not exist.
```

### 27.2 Retained-path visibility repair

`validate_retained_root_visibility` is a read-only success gate. It uses non-following `lstatSync`
on the bound CWD, `logical_root`, `canonical_root`, `logical_parent` and `canonical_parent`, and
requires:

- both declared roots are visible non-symlink Directory objects;
- both declared roots equal the bound CWD device/inode/type;
- logical and canonical roots equal each other;
- both parent paths equal the frozen parent object;
- canonical dirname and basename equal the frozen canonical parent and basename.

The helper is invoked before `evidence-summary.txt`, before terminal evidence output, immediately
before `runtime_success_ready=yes`, at success-finalizer entry, and immediately before final PASS
output. It is never used for evidence I/O, adoption, rename, deletion or cleanup. If the original
root is unlinked while CWD remains open, a declared path disappears, either path becomes a symlink,
a same-basename new inode appears, the canonical path diverges, or the parent object changes, the
run is HOLD. It never recreates, relinks, renames or deletes either object.

The successful summary now records bound device/inode, both retained paths, logical visibility
PASS, canonical visibility PASS, logical/canonical/bound identity equality PASS, parent identity
PASS, `evidence root retained`, and `cleanup NOT EXECUTED / NOT AUTHORIZED`.

Disposition:

```text
REL-RUNTIME-ROOT-R4:
CLOSED IN PLANNING AUTHORITY
```

## 28. Round-3 adversarial disposition

| Scenario | Identity / ownership detection | Evidence I/O and process cleanup | Success claim | Decision |
| --- | --- | --- | --- | --- |
| child replacement immediately after mkdir, before first stat | no available descriptor proves which object was created | hard proof gate stops before root creation; no evidence I/O; dispatcher remains independent | none | HOLD / R3 |
| child replacement after captured identity | basename dev/inode or marker identity differs | no adoption; no uncertain cleanup | none | HOLD |
| child replacement before/during `cd` | adopted CWD dev/inode must equal captured child | no replacement-root I/O | none | HOLD |
| replacement is Directory with same basename | inode inequality rejects it | no adoption | none | HOLD |
| replacement carries copied marker | marker is insufficient; object identity must also match | no adoption | none | HOLD |
| basename becomes file or symlink | non-following type check rejects | no evidence I/O | none | HOLD |
| original root unlinked after bind | CWD evidence remains object-bound; final declared-path lstat fails | process/generated cleanup still runs; root is not deleted | prohibited | HOLD / R4 |
| logical path removed/replaced/symlinked after bind | final logical visibility or identity fails | relative evidence remains original CWD | prohibited | HOLD / R4 |
| canonical path or canonical parent diverges | final canonical/root-parent checks fail | no pathname mutation | prohibited | HOLD / R4 |
| replacement root contains valid-looking evidence | relative readers stay in original CWD; replacement identity fails visibility | replacement never adopted or deleted | prohibited | HOLD |
| visibility failure after process cleanup | process and ports are already handled independently | failure-state is attempted only in bound CWD; root retained | no PASS | HOLD |
| old retained failure root before rerun | existing-or-link preflight remains fail closed | no new root, process, cleanup or adoption | none | HOLD pending separate cleanup gate |

## 29. Round-3 gate and required next action

Static parse-only inspection of the revised Section 14 confirmed one executable authority, one
`runtime_evidence_main`, one build, one Node mkdir authority, one created-child capture helper,
one adoption helper/call, one ownership-marker verifier, one retained-visibility helper, five
visibility call sites, one `requestServerClose`, one `server.close`, no evidence-root rm/rmdir,
no KILL authority, and `zsh -n` PASS. No runtime command was executed.

Finding state:

```text
ARCH-RUNTIME-ROOT-1: ACCEPTED / CLOSED
REL-RUNTIME-ROOT-R1: ACCEPTED / CLOSED
REL-RUNTIME-ROOT-R2: ACCEPTED / CLOSED
REL-RUNTIME-ROOT-R3: HOLD / NOT CLOSED
REL-RUNTIME-ROOT-R4: CLOSED IN PLANNING AUTHORITY
REL-RUNTIME-RR6-1: OBSERVATION
```

Conclusion: **HOLD**. The current platform cannot prove the mkdir-created child before its first
pathname stat, so the canonical authority intentionally cannot create/adopt a new root. R4 is
literally repaired, R1/R2 are preserved, and no false PASS or root deletion is possible, but a
runtime-capable R3 closure requires PM intake and a separately authorized platform-primitive
design. Reliability focused re-review round 3, Data Quality, Verification, retained-root cleanup,
runtime rerun and Git write remain unauthorized until that design is completed.

## 30. Option C private run-specific root and T1–T3 authority

This section supersedes Sections 27–29 only for the current root architecture, threat boundary,
R3 treatment, future rerun behavior and required next gate. Those sections remain historical
lineage for the strict T4 interpretation and the earlier fail-closed proof gate. Section 14 is the
sole current executable literal authority.

### 30.1 PM-approved threat boundary

The current authority freezes:

```text
Filesystem threat boundary:
DEFENDS T1–T3
DOES NOT CLAIM T4–T5

T1 — stale roots, failed-run residue, ordinary unexpected files/directories,
     dangling symlinks, crash residue and cleanup failure
T2 — other-user path replacement/injection/deletion within sticky-directory,
     current-UID ownership, exact 0700 private-parent/root and non-privileged assumptions
T3 — accidental same-UID concurrent starts, ordinary tooling collision, nonce/manifest collision

T4 — deliberate same-UID adversarial race: NOT CLAIMED
T5 — privileged/root filesystem manipulation: NOT CLAIMED
atomic mkdir-and-open: NOT CLAIMED
kernel-enforced sandbox: NOT CLAIMED
```

This is an explicit system contract, not a claim that the strict T4 race has been technically
closed. The unpredictable name, exclusive creation and CWD binding are accepted only for T1–T3.

### 30.2 Private-parent preparation and adoption

The selected parent model is **pre-created only**:

```text
/tmp/edge-mes-dashboard-url-runtime-evidence-runs
```

A separately authorized workspace-preparation gate must create it and its fixed
`.edge-mes-private-parent-authority.json` marker. Section 14 requires:

- non-symlink Directory;
- owner UID equals current effective UID;
- exact mode `0700`, with no group/other access;
- logical and physical/canonical paths name the same device/inode/type;
- exact marker schema, owner `0600`, parent path, canonical path, UID, mode, device and inode;
- repeated checks at pre-run, immediately before run-root creation, before every manifest
  publication/validation and before terminal success.

Section 14 does not create, adopt by metadata alone, chmod, repair, empty, rename or delete an
unknown/missing parent. Parent absence or mismatch is `PRIVATE_PARENT_PREFLIGHT` / `HOLD` pending
the separate preparation gate. Once CWD-bound, parent pathname replacement cannot retarget the
relative run-root creation or root adoption within the declared T1–T3 model.

### 30.3 Run-specific root and object binding

Each run generates exactly one `randomBytes(32)` nonce, validated as 64 lowercase hexadecimal
characters, and derives only:

```text
root basename: run-<nonce>
logical identity: dashboard-production-url-resolution-runtime-evidence/<nonce>
physical path: <private-parent>/run-<nonce>
manifest: <private-parent>/run-<nonce>.manifest.json
manifest tmp: <private-parent>/.run-<nonce>.manifest.json.tmp
```

No user, query, fixture, timestamp-only value or predictable counter enters those names. Current
run root/manifest/tmp collisions, files, directories, dangling links or symlinks are `HOLD`; an
unknown object is never adopted or deleted. Existing objects belonging to other nonces are not
enumerated or modified and do not block a new run.

`create_and_capture_run_root` performs one exclusive `mkdirSync(..., 0700)`, immediate
non-following identity/owner/mode capture, exclusive `0600` ownership marker, checked full write,
fsync, recheck and CWD adoption. The adopted CWD must equal the first observed run-root identity;
all root evidence I/O remains basename-only relative to `evidence_root=.` with Node CWD
device/inode assertions and the atomic failure-state writer. This closes ordinary post-bind
retargeting and collision risks under T1–T3. It does not assert that mkdir and first observation
are atomic and does not defend a deliberate T4 replacement race.

### 30.4 Manifest mapping authority

The manifest is a mapping authority, not evidence-content authority. Its exact schema records:

```text
schema/version and RUN_MANIFEST stage
logical runtime evidence identity
run nonce
logical and canonical physical root paths
root device/inode/type
run start timestamp
gate purpose and expected final state
current state: ACTIVE, SUCCESS or FAILURE
threat-boundary version
T1–T3 boundary and T4/T5/atomic non-claims
run-root creation model
cleanup NOT_EXECUTED_NOT_AUTHORIZED
legacy fixed-root disposition
```

Publication requires private-parent and retained-root revalidation, absent non-link tmp, `wx`
`0600` tmp creation, checked full write, fsync, close, atomic rename and exact readback/digest.
Allowed transitions are:

```text
NOT_PUBLISHED → ACTIVE → SUCCESS
NOT_PUBLISHED → ACTIVE → FAILURE
NOT_PUBLISHED → FAILURE only when a bound root exists but ACTIVE publication did not complete
```

A final/tmp collision, illegal transition, wrong schema, wrong root inode, wrong nonce, symlink or
mapping mismatch is `HOLD`. The manifest cannot make transport, fixture, response, parser, UI or
production-fact evidence pass. No fixed-root symlink pointer is created.

### 30.5 Retention, rerun and legacy root

Every physical run root and per-run manifest is retained for both terminal states:

```text
SUCCESS: retained
FAILURE: retained
```

Section 14 contains no run-root rm loop, run-root rmdir, manifest deletion, private-parent cleanup,
legacy-root cleanup or wildcard cleanup. A later cleanup requires a separately authorized exact
identity gate.

Multiple retained terminal roots/manifests may coexist. `ACTIVE` identifies an incomplete/current
mapping; `SUCCESS` and `FAILURE` are terminal audit states. A future run rejects only its own nonce
collision, current-run root/manifest/tmp collision, private-parent authority failure, unknown path
condition or current-run mapping inconsistency. The private parent is not required to be empty.

The existing:

```text
/tmp/edge-mes-dashboard-url-runtime-evidence
```

is a legacy retained failure artifact outside the Option C namespace. This planning task does not
adopt, rename, migrate, copy, modify, index or delete it. It does not block creation of a new
run-specific root. Before any runtime rerun authorization, PM must separately record whether the
legacy artifact remains historical evidence, receives a legacy/migration record, or enters a
separate cleanup gate. Cleanup remains `NOT AUTHORIZED`.

### 30.6 Terminal evidence boundary

A/B/C semantics remain unchanged and a distinct D statement is added:

```text
A. local transport/request evidence only
B. frozen synthetic fixture/body/parser/view/UI markers only
C. real production-fact evidence: NOT EXECUTED / NOT CLAIMED
D. filesystem evidence boundary:
   defends T1–T3 within documented assumptions;
   does not claim T4/T5, atomic mkdir-and-open or kernel sandbox protection
```

Success summary records the nonce, logical identity, physical/canonical root, device/inode/type,
manifest identity and terminal state, private-parent UID/mode, threat boundary, non-claims, legacy
root disposition and `cleanup NOT EXECUTED / NOT AUTHORIZED`. Failure-state and dispatcher stderr
record the same boundary and retained-root/manifest identity where binding exists.

### 30.7 Preserved controls

The Option C update does not change ports `3100/3101`, endpoint/query, fixture values, one build,
Phase A/B semantics, one target request, one `requestServerClose`, one `server.close`, one joined
waiter, TERM-only cleanup, `KILL == 0`, wait rc semantics, response-completion authority,
fixture/body digest lineage, generated/quarantine ownership and frontend cleanup. It preserves:

```text
DQ-RUNTIME-D2-3: CARRY FORWARD
DQ-URL-D3: CARRY FORWARD
REL-URL-R6: CARRY FORWARD
REL-RUNTIME-RR6-1: OBSERVATION
```

### 30.8 Finding disposition and gate

```text
ARCH-RUNTIME-ROOT-1:
ACCEPTED / CLOSED

REL-RUNTIME-ROOT-R1:
ACCEPTED / CLOSED

REL-RUNTIME-ROOT-R2:
ACCEPTED / CLOSED

REL-RUNTIME-ROOT-R3:
PROPOSED RECLASSIFICATION UNDER T1–T3 THREAT BOUNDARY
pending independent Reliability review

strict T4 interpretation:
NOT CLAIMED

REL-RUNTIME-ROOT-R4:
CLOSED IN PLANNING AUTHORITY

REL-RUNTIME-RR6-1:
OBSERVATION
```

Architecture planning update conclusion: **PASS WITH RECOMMENDATIONS**. This does not close R3,
does not constitute Reliability acceptance and does not authorize private-parent preparation,
legacy-root cleanup, runtime rerun, Data Quality, Verification or Git action.

Required next action:

```text
PM intake
→ independent focused Reliability re-adjudication of R3 under the approved T1–T3 boundary
→ Data Quality manifest/evidence-lineage review
→ Verification static/negative-case review
→ separately authorized workspace-preparation and legacy-retention/cleanup decisions
→ separately authorized runtime rerun only after all gates pass
```
## 31. Option C manifest Reliability HOLD repair — current authority

This section is the current targeted planning-authority repair for
REL-RUNTIME-OPTIONC-R1 and REL-RUNTIME-OPTIONC-R2. It does not reopen the Option C design,
private-parent path, run nonce, run-specific root, root CWD evidence model, retention policy or
T1–T3 threat boundary.

### 31.1 Parent-object-bound manifest namespace

The control shell retains the run-specific root CWD and its root identity evidence. Manifest
operations run in a separate Node process whose subshell first binds CWD with
cd -P private_parent. The helper immediately validates stat(.) against the frozen private-parent
device, inode, directory type, owner UID and mode 0700, then validates the fixed authority marker
using a relative marker target. A successful cd is not treated as proof of object identity.

The helper accepts only:

~~~text
run-<64hex>.manifest.json
.run-<64hex>.manifest.json.tmp
~~~

Actual create, read, lstat, open, rename, validation and publication targets are only:

~~~text
./<manifest_basename>
./<manifest_tmp_basename>
~~~

logical_manifest_report_path and canonical_manifest_report_path are reporting identities only.
They are never passed to the helper as mutation or readback targets. This keeps root evidence CWD
and manifest parent CWD as different object namespaces and prevents a control-shell CWD change
from changing root evidence authority.

### 31.2 Publication and state authority

The parent-bound helper validates the parent object and marker, rejects pre-existing final/tmp
objects, symlinks, wrong metadata, wrong schema, wrong nonce and wrong mapping, validates the
current manifest state and digest, creates the temporary file with wx and mode 0600, checks full
write completion, fsyncs and closes it, renames relative tmp to relative final, attempts parent
directory fsync, reads back final and verifies metadata, schema, state, mapping and digest.
Parent-directory fsync failure is recorded as a non-durability recommendation; it is not presented
as completed directory-durability proof.

Disk manifest plus exact mapping is the source of truth. manifest_confirmed_state and
manifest_confirmed_digest are only the last confirmed shell view. A publication process failure,
stdout failure, command-substitution failure or shell assignment failure never permits the shell
to guess ACTIVE. It enters read-only reconciliation.

### 31.3 Terminal commit protocol

The terminal states are:

~~~text
PRE_TERMINAL
TERMINAL_COMMITTING
SUCCESS_COMMITTED
TERMINAL_FAILURE_COMMITTED
TERMINAL_UNKNOWN
~~~

Before terminal commit, validation, cleanup, port release proof, generated/quarantine cleanup,
evidence summary construction and the final root/private-parent/manifest checks complete while
the manifest remains ACTIVE. A fixed terminal PASS line is prepared before the commit boundary.
The shell then neutralizes INT, TERM and HUP, enters TERMINAL_COMMITTING, and performs the final
ACTIVE to SUCCESS publication in the validated parent CWD process. Only an exact
SUCCESS_COMMITTED result and digest may set SUCCESS_COMMITTED. After that point the shell only
prints the preconstructed PASS line and exits zero; it does not validate, clean up, wait, call
the failure dispatcher, write evidence, change the root or touch the manifest.

If SUCCESS publication is uncertain, read-only reconciliation decides the outcome. Exact
SUCCESS with exact mapping enters the non-fallible exit-zero path. Exact ACTIVE restores the
normal failure traps and allows the guarded FAILURE path. Exact FAILURE exits nonzero without
SUCCESS overwrite. Missing, malformed, inconsistent or unknown state exits nonzero with manual
review required and no overwrite or cleanup. This closes the SUCCESS-on-disk plus nonzero-process
split identified by REL-RUNTIME-OPTIONC-R1.

### 31.4 Failure finality and disposition

FAILURE publication is permitted only from NOT_PUBLISHED with no prior publication result or from
confirmed ACTIVE. A confirmed SUCCESS state is terminal and the failure dispatcher returns
without FAILURE publication. A confirmed FAILURE state cannot be changed to SUCCESS. Publication
uncertainty is reconciled before any state transition is assumed; unknown state is retained as
unknown with no overwrite and no false PASS claim.

Current planning disposition:

~~~text
REL-RUNTIME-OPTIONC-R1:
CLOSED IN PLANNING AUTHORITY

REL-RUNTIME-OPTIONC-R2:
CLOSED IN PLANNING AUTHORITY

REL-RUNTIME-ROOT-R3:
RECLASSIFIED AS DOCUMENTED T4 NON-CLAIM
ACCEPTED UNDER T1–T3 THREAT BOUNDARY

REL-RUNTIME-ROOT-R4:
ACCEPTED / CLOSED

REL-RUNTIME-RR6-1:
OBSERVATION
~~~

Architecture repair gate is PASS WITH RECOMMENDATIONS, subject to static verification of this
literal Section 14. Reliability focused re-review, Data Quality review, Verification review,
private-parent preparation, legacy-root cleanup, runtime rerun and Git write remain separately
pending or unauthorized. Global Gate remains HOLD.

## 32. Option C retained record value-validation repair authority

This section supersedes only earlier statements that the 57-field pre-terminal summary and the
76-field failure record had complete value-level readback. The current Section 14 literal is the
sole executable authority. Manifest mapping, D1 pre-terminal semantics, D3 HOLD sentinels,
Reliability terminal-commit controls and all carry-forward boundaries remain unchanged.

### 32.1 Data Quality HOLD intake

The independent Data Quality re-review accepted DQ-RUNTIME-OPTIONC-D1 and
DQ-RUNTIME-OPTIONC-D3, but found that key/order/count validation was being described as full
value validation. The exact gaps were:

~~~text
DQ-RUNTIME-OPTIONC-D5:
57 summary fields
37 exact values
4 source digests format-only
16 key/order-only values

DQ-RUNTIME-OPTIONC-D6:
76 failure-state fields
26 exact values
remaining manifest, cleanup, wait, port, artifact, fixture and response values key/order-only
~~~

The repair therefore does not add another terminal outcome record. It changes how the existing
summary and failure-state records obtain, serialize and verify their values.

### 32.2 Freeze-write-readback authority

Both retained records now follow one literal model:

~~~text
freeze named source values once
→ emit one canonical ordered expected payload
→ atomically write that exact payload
→ read the retained file
→ require byte-for-byte equality with the same frozen payload
→ parse fixed keys and validate formats, enums and relations
~~~

`emit_evidence_summary_expected_record` is the sole 57-field ordering/serialization authority.
`freeze_evidence_summary_values` creates exactly 57 named `summary_expected_*` field values and
freezes one `summary_expected_payload`. The writer and validator consume that payload; the
validator does not rebuild a second partial expected object.

`emit_failure_state_expected_record` is the sole 76-field ordering/serialization authority.
`freeze_failure_state_values` creates exactly 76 named `failure_expected_*` field values and
freezes one `failure_expected_payload`. The writer and validator consume that payload; the
validator does not query current process, port, fixture, manifest or filesystem state again.

A dynamic value containing CR/LF, a wrong line count, a duplicate/missing/reordered key, a changed
value or a byte-level mismatch fails closed. Raw equality is the full 57/57 and 76/76 source-value
check; the relation validators are additional semantic constraints, not substitutes for source
equality.

### 32.3 Summary 57/57 value contract

The frozen summary map includes every existing field, including the previous gaps:

~~~text
gate_purpose
run_root_creation_model
legacy_fixed_root
A_evidence_boundary
B_evidence_boundary
D_evidence_boundary
phase_a_capture_state
phase_b_capture_state
request_method_path_host_query
phase_a_pid
phase_b_pid
capture_pid
next_port_release
capture_port_release
build_id
server_js_sha256
fixture_sha256
served_body_sha256
post_request_fixture_sha256
fixture_lineage_result
~~~

The summary remains strictly pre-terminal:

~~~text
schema_version=1
record_stage=PRE_TERMINAL_SUCCESS_EVIDENCE
summary_state=READY_TO_COMMIT_SUCCESS
manifest_state_at_summary=ACTIVE
manifest_reconciliation_state_at_summary=NOT_RUN
~~~

The validator requires the exact current-run identity, root and parent object tuple, parent/root
marker digests, ACTIVE manifest path/digest, approved purpose, creation model, legacy-root
isolation, T1–T3/T4–T5 boundaries and cleanup non-authorization. It additionally requires:

- all three role PIDs are positive decimal values and pairwise distinct;
- both port results are exactly `released`;
- the request field is the approved method/path/host/five-query statement;
- the Phase A and B fields are the approved exact state statements;
- `build_id` is the frozen expected build ID;
- `server_js_sha256` is the frozen expected server digest;
- fixture, served-body and post-request fixture digests are 64 lowercase hex and equal under the
  approved byte-lineage relation;
- fixture lineage is `PASS`, response evidence is `RESPONSE_COMPLETE`, item count is 1 and item
  key count is 22;
- artifact ownership and final postcondition are both `PASS`.

A valid-format digest from another source, an invented port release, a substituted PID/build ID,
a widened A/B/D claim or a changed Phase/request value fails exact payload equality and cannot
reach terminal SUCCESS publication.

### 32.4 Failure-state 76/76 value contract

`freeze_failure_state_values` runs only for a bound current-run root. It freezes all 76 fields
before the atomic writer starts. The six generated/quarantine filesystem states are queried once
inside the freeze helper and assigned to named fields. `write_failure_state` and
`validate_failure_state_readback` contain zero `filesystem_state` queries.

The frozen map includes the exact failure code/reason/interrupted state; run/root/parent identity;
both marker digests; logical/canonical manifest paths; confirmed state/digest; publication,
reconciliation and parent-fsync classifications; terminal commit/disposition; cleanup/wait/port
results; build and filesystem states; handoff/deletion/postcondition states; fixture digests and
byte counts; response flags; and capture state.

`failure_reason` remains diagnostic prose, but its retained value must equal the frozen writer
value and contain no CR/LF. `failure_code` must equal the frozen value and match the approved
uppercase token grammar. Unsupported parent-directory durability telemetry is explicitly frozen
as `UNKNOWN`, rather than retained as an empty or arbitrary value.

### 32.5 Failure-state relation contract

The readback validator applies the following relations after byte-level source equality:

- canonical run identity, run-root basename, private-parent paths and both manifest paths derive
  from the same 64-lowercase-hex nonce;
- manifest `ACTIVE` or `FAILURE` requires its exact 64-hex confirmed digest;
- `NOT_PUBLISHED` and `UNKNOWN` require their exact named digest sentinels;
- a reconciliation state other than `NOT_RUN` must equal the confirmed state;
- failure-state cannot contain manifest `SUCCESS`, reconciliation `SUCCESS` or
  `SUCCESS_COMMITTED`;
- confirmed `FAILURE` maps to `FAILURE_NONZERO`;
- confirmed or reconciled `UNKNOWN` maps to `UNKNOWN_NONZERO`;
- all other non-success failure records map to `HOLD_NONZERO`;
- each cleanup result and wait status equals its frozen role value and belongs to the documented
  enum/grammar; successful cleanup requires wait status 0; wait 127 is never a success result;
- each port result equals its frozen value and belongs to `NOT_CHECKED`, `released`,
  `unknown_listener` or `lsof_failure`;
- the three build classifications and six frozen source/quarantine states follow their exact
  grammars;
- handoff, ownership-verification, deletion and postcondition values follow their exact stage
  enums;
- fixture digest/byte fields use either matching `NOT_RECORDED` sentinels or valid digest/positive
  numeric values;
- a `PASS` fixture lineage requires expected/post-request digest and byte equality plus completed
  response evidence;
- completed response evidence requires no response error and exact committed/write-started flags;
- response booleans/sentinels and the capture-state value belong to their documented enums.

These checks allow a failure record to retain real failure values; they do not require ports,
cleanup, fixture lineage or generated artifacts to look successful. They only prevent one frozen
failure value from being replaced by a different success-looking or failure-looking value.

### 32.6 D2 retained join

The manifest continues to provide 31/31 exact mapping. The failure record now preserves and
readbacks, at value level:

~~~text
run nonce and logical identity
physical and canonical root identity
private-parent identity and ownership/mode
private-parent and root-marker digests
logical and canonical manifest paths
confirmed manifest state and digest
publication and reconciliation classifications
terminal non-success disposition
cleanup, wait and port outcomes
fixture/response and generated-artifact outcomes
~~~

A pre-ACTIVE failure after the root is bound records either exact `NOT_PUBLISHED` state/digest or
an exact reconciled `ACTIVE`, `FAILURE` or `UNKNOWN` tuple. An uncertain, unbound root is still not
written through; it remains governed by the accepted D3 fixed HOLD sentinel contract. This closes
the failure-state retained-join portion of DQ-RUNTIME-OPTIONC-D2 in planning authority without
inventing an unknown-object record.

### 32.7 Preserved boundaries

The repair does not change:

~~~text
DQ-RUNTIME-OPTIONC-D1: ACCEPTED / CLOSED
DQ-RUNTIME-OPTIONC-D3: ACCEPTED / CLOSED
DQ-RUNTIME-OPTIONC-D4: RECOMMENDATION
DQ-RUNTIME-D2-3: CARRY FORWARD
DQ-URL-D3: CARRY FORWARD
~~~

It preserves manifest parent-CWD I/O, disk manifest source-of-truth, publication reconciliation,
trap/terminal commit ordering, SUCCESS_COMMITTED plus exit 0, UNKNOWN no-overwrite/no-cleanup,
FAILURE no-SUCCESS overwrite, no fallible filesystem/process operation after SUCCESS, root and
manifest retention, KILL zero, wait semantics, one requestServerClose, one server.close and one
joined waiter.

No retained namespace scan, historical cleanup, pagination/aggregation proof or production-fact
validation is added.

### 32.8 Static disposition and gate

The current literal statically establishes:

~~~text
manifest mapping coverage: 31/31
summary value coverage: 57/57 frozen-source exact raw equality
failure-state value coverage: 76/76 frozen-source exact raw equality
failure writer filesystem-state recomputation: 0
failure validator filesystem-state recomputation: 0
freeze-time filesystem-state observations: exactly 6
premature terminal SUCCESS wording: 0
root/private-parent/manifest deletion: 0
KILL: 0
zsh parse: PASS
~~~

Planning findings:

~~~text
DQ-RUNTIME-OPTIONC-D1: ACCEPTED / CLOSED
DQ-RUNTIME-OPTIONC-D2: CLOSED IN PLANNING AUTHORITY
DQ-RUNTIME-OPTIONC-D3: ACCEPTED / CLOSED
DQ-RUNTIME-OPTIONC-D4: RECOMMENDATION
DQ-RUNTIME-OPTIONC-D5: CLOSED IN PLANNING AUTHORITY
DQ-RUNTIME-OPTIONC-D6: CLOSED IN PLANNING AUTHORITY
DQ-RUNTIME-D2-3: CARRY FORWARD
DQ-URL-D3: CARRY FORWARD
~~~

Architecture repair gate: PASS WITH RECOMMENDATIONS. Independent Data Quality re-review remains
mandatory. Verification, private-parent preparation, legacy-root cleanup, runtime rerun and Git
write remain unauthorized. A PM handoff is required after the next Data Quality re-review,
regardless of that review's PASS or HOLD result. Global Gate remains HOLD.
