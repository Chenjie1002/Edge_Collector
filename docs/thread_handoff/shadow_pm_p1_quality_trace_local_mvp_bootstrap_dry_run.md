# Shadow Mainline PM P1 Quality + Trace Local MVP — Owner Manual Bootstrap and Capability Dry Run

Status: `READY_FOR_OWNER_MANUAL_START`

This file is a bootstrap procedure only. It does not start Codex, does not itself execute P1-G1/G2, and does not grant product、Git、DB-runtime、remote or later-phase authority. The Owner manually starts the Goal in the macOS Codex client.

## 1. Owner manual start

The Owner performs activation locally:

1. Open the macOS Codex client.
2. Select/open the project folder `/Users/chenjie/Documents/MES/edge-mes-demo`.
3. Start a new Goal-mode session.
4. Paste the complete content of `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_goal_prompt.md` into the Goal.
5. Start the Goal manually.

Until Step 5 occurs:

```text
SHADOW_PM_GOAL_STARTED = NO
P1_AUTONOMOUS_EXECUTION_STARTED = NO
REMOTE_AUTHORITY_CONSUMED = NO
GIT_MUTATION_AUTHORIZED = NO
```

ChatGPT/Mainline PM must not start or control the Owner's local Codex Goal on the Owner's behalf.

## 2. Bootstrap authority identities

### Immutable Goal Charter

```text
path = docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter.md
regular / non-symlink
bytes = 26966
SHA-256 = 0672cb1771eb7eedf1f6d3ecff65a975509efc7618e6164a8b7cfcb419456bfe
```

The Charter is immutable delegated authority for this Goal. The Goal controller may not edit or self-expand it.

### Genesis continuity Ledger

```text
path = docs/reports/shadow_pm_p1_quality_trace_local_mvp_ledger.md
regular / non-symlink
bytes at manual-bootstrap preparation = 8001
SHA-256 at manual-bootstrap preparation = 9af50a2a18c9f9f480d9a1a96bd204f954f4238c31273d428d5803d971ff3cb6
```

This SHA is an entry identity only. The Ledger is intentionally mutable after Owner starts the Goal. Once the parent/controller begins durable capability state transitions, the bootstrap SHA is not a permanent hash pin and must not be used to reject legitimate parent Ledger updates.

### Final Owner Goal Prompt

```text
path = docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_goal_prompt.md
regular / non-symlink
bytes = 9645
SHA-256 = 6b64417c5e3cf8ad7f5d5602c57332ea7fa8c53e6ec2e8cbaf0fd736d081e8e9
```

The Goal Prompt is Owner-facing bootstrap text. PM Rules + Charter remain the authority envelope.

### Accepted P1-G0 baseline

```text
path = docs/reports/p1_g0_production_source_adequacy_semantic_boundary_freeze.md
regular / non-symlink
bytes = 38063
SHA-256 = 10982b8a92d0c33bfd18812ec14879af9ea74f658a74ab046b4d71d2725ef87e
executor terminal = PASS WITH RECOMMENDATIONS
Mainline PM intake = ACCEPTED
P1_G0_PM_ACCEPTED = YES
P1_G0_VERIFIED = NO
```

### P1 PM plan

```text
path = docs/reports/p1_production_truth_semantics_trusted_consumption_plan.md
regular / non-symlink
bytes = 15505
SHA-256 = 48a9d8af24ed4f106ef724634229055887ce71c74ffc38d208aa28bc2192d88e
```

## 3. Prepared capability child task

Before any real P1-G1 task, the current Goal parent/controller must delegate exactly this prepared task to one disposable child:

```text
path = docs/thread_handoff/pm_task_20260811T0957Z_shadow_pm_p1_subagent_capability_dry_run.md
regular / non-symlink
bytes = 13331
SHA-256 = 401651a646817768ec4360549d657e679e7300d1fe212674228a6fc1a691e25d
```

Expected sole child report:

```text
path = docs/reports/shadow_pm_p1_subagent_capability_dry_run.md
prestate at bootstrap preparation = ABSENT
```

The parent must pass the exact task path/type/bytes/SHA-256 above to the child. The child must complete task self-identity before any other repository action.

The capability task is not P1-G1 and does not consume `TOTAL_DISPATCHED_GATES`.

## 4. Parent pre-dispatch recovery

Immediately after Owner starts the Goal, the parent must remain the long-lived Shadow Mainline PM controller and perform read-only recovery before dispatching the child:

1. read current `docs/thread_handoff/pm_operating_rules.md`;
2. mechanically verify the immutable Charter identity from Section 2;
3. read this Bootstrap;
4. read current Ledger and confirm it is a legitimate descendant of the genesis state, or the exact genesis entry identity if this is the first start;
5. mechanically verify the Goal Prompt, accepted P1-G0 report and P1 plan identities from Section 2;
6. recover physical cwd、Git top-level、branch、HEAD、origin/main、left/right count、cached/staged state and tracked dirty paths;
7. confirm the accepted genesis baseline is still reconstructable and no authority contradiction exists;
8. confirm the capability report has not already been accepted for the current parent session/epoch.

Accepted genesis Git baseline for first start:

```text
branch = main
HEAD = dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
origin/main = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
origin/main...HEAD = 0<TAB>1
cached/staged = empty
tracked dirty = docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
```

If live facts differ, the parent must classify whether the change is a legitimate prior Goal continuation, an external repository change or authority drift. It may not silently rewrite genesis or clean unrelated work.

## 5. Capability epoch and durable dispatch intent

For a first Owner start, before creating the child the parent updates the Ledger to record at least:

```text
SHADOW_PM_GOAL_STARTED = YES
CAPABILITY_EPOCH = 1
CAPABILITY_DRY_RUN_ACCEPTED = NO
CURRENT_GATE = CAPABILITY_DRY_RUN
CURRENT_GATE_STATUS = DISPATCH_INTENT_RECORDED
LAST_TASK = docs/thread_handoff/pm_task_20260811T0957Z_shadow_pm_p1_subagent_capability_dry_run.md
LAST_EXECUTOR_REPORT = NONE
LAST_DURABLE_PHASE = DISPATCH_INTENT_RECORDED
NEXT_ACTION = DISPATCH_PREPARED_CAPABILITY_CHILD
```

This parent Ledger update is a control-plane continuity action. It is not product mutation and does not consume a P1 dispatched Gate.

For a fresh parent Goal session recovering an already-progressed Goal, increment `CAPABILITY_EPOCH` rather than resetting counters or accepted product Gates. Do not replay accepted G1/G2/review work merely because the parent session changed.

## 6. Child dispatch

The parent must:

1. mechanically verify the prepared task identity from Section 3 immediately before dispatch;
2. create exactly one disposable child/sub-agent;
3. dispatch only the exact capability task and expected identity;
4. remain the parent/controller and do not execute the child task itself;
5. do not create G1 while capability is pending;
6. wait for/receive the child terminal and durable report;
7. never instruct the child to update the Ledger or self-advance.

The child task itself forbids child sub-agents、product mutation、Git mutation、DB/API runtime、tests、Python、network/SSH、Docker、PLC/V-PLC、production action and successor-task creation.

## 7. Parent independent capability intake

The child report can prove only child-side capability facts. It cannot prove parent-side facts by assertion.

Parent acceptance requires the parent to independently establish all of:

```text
SUBAGENT_DELEGATION_AVAILABLE = YES
PARENT_CONTROLLER_RETAINS_CONTEXT = YES
ONE_CHILD_ONE_TASK_SCOPE = YES
CHILD_CANNOT_SELF_ADVANCE = YES
CHILD_DURABLE_REPORT_AVAILABLE = YES
PARENT_CAN_INDEPENDENTLY_INTAKE = YES
LEDGER_CAN_BE_UPDATED_BY_PARENT_ONLY = YES
PRODUCT_MUTATION = 0
GIT_MUTATION = 0
DB_RUNTIME_ACTION = 0
REMOTE_ACTION = 0
```

Required parent intake checks include:

- child report exists at the exact expected path and is regular/non-symlink;
- child report identity is mechanically recorded;
- child task identity in report matches the prepared task;
- child report terminal is consistent with exact changed-path/Git evidence;
- child used zero sub-agents and created zero successor tasks;
- child did not mutate the Ledger;
- child task-owned changed path is only its exact report;
- protected dirty docs and pre-existing Goal-control files are preserved;
- cached/staged state remains empty unless an unrelated external actor changed it, in which case capability acceptance must fail closed pending reconciliation;
- parent is still present as controller and can perform this intake after child termination.

A child PASS is a candidate result only. Capability becomes accepted only after parent intake.

## 8. Successful capability transition

On parent-accepted capability PASS, update the Ledger to:

```text
GOAL_STATUS = ACTIVE_P1_QUALITY_TRACE_LOCAL_AUTONOMY
SHADOW_PM_GOAL_STARTED = YES
CAPABILITY_DRY_RUN_ACCEPTED = YES
CURRENT_GATE = P1-G1_PRODUCTION_SEMANTICS_CONTRACT
CURRENT_GATE_STATUS = READY_TO_ISSUE
CURRENT_FAILURE_FAMILY = NONE
CURRENT_FAILURE_FAMILY_ATTEMPTS_USED = 0
TOTAL_DISPATCHED_GATES = 0
PRODUCT_REPAIR_GATES_USED = 0
CONTROL_PLANE_RECOVERY_GATES_USED = 0
NO_PRODUCT_PROGRESS_STREAK = 0
LAST_EXECUTOR_REPORT = docs/reports/shadow_pm_p1_subagent_capability_dry_run.md
LAST_PM_INTAKE = P1_CAPABILITY_DRY_RUN_PARENT_ACCEPTED
LAST_DURABLE_PHASE = PM_INTAKE_ACCEPTED
NEXT_ACTION = GENERATE_EXACT_P1_G1_TASK
```

Then, and only then, the parent may generate the first real P1-G1 repository-backed task under the Charter.

Do not pre-create G2、Reliability、Data Quality or Verification tasks.

## 9. Capability failure terminals

If parent/child separation cannot be proven:

```text
GOAL_STATUS = HOLD
CURRENT_GATE_STATUS = HOLD / SHADOW_PM_SUBAGENT_CAPABILITY_UNAVAILABLE
SHADOW_PM_STOP = YES
```

If the child creates unauthorized repository mutation:

`HOLD / CAPABILITY_DRY_RUN_UNAUTHORIZED_MUTATION`

Do not auto-clean, reset or restore the mutation.

If task/report/dispatch state is ambiguous and cannot be reconciled read-only:

`HOLD / CAPABILITY_DRY_RUN_STATE_AMBIGUOUS`

If repository/authority baseline cannot be reconstructed:

`HOLD / REPOSITORY_AUTHORITY_DRIFT`

No capability failure grants G1 execution authority.

## 10. Restart behavior during capability

The parent must use durable phase state rather than chat memory.

If restart occurs after `DISPATCH_INTENT_RECORDED`:

- if capability report exists, do not redispatch; intake the existing report first;
- if report does not exist and child completion state cannot be proven, reconcile bounded repository state before considering a fresh capability epoch;
- never infer `child did not run` solely from a missing chat transcript;
- if any mutation ambiguity exists, stop fail-closed.

A new parent Goal session requires a new capability epoch before issuing future specialist tasks. This does not reset P1 failure/product/control-plane/total counters and does not replay already accepted product Gates.

## 11. First real Gate boundary

After successful capability intake, the first real Gate is exactly:

`P1-G1 Production Semantics Contract`

The parent must create a fresh repository-backed 16-section task whose purpose is to freeze the minimum production semantics contract for station-scoped Quality + accepted-fact Trace while preserving the P1-G0 `PARTIAL/UNSUPPORTED` boundaries.

G1 must not be broadened into implementation、historical config registry、DB migration、Performance/Availability/OEE、Frontend or remote work.

When G1 is dispatched:

`TOTAL_DISPATCHED_GATES = 1`

The G1 specialist must stop after its own durable result. The parent then independently intakes before any G2 task exists.

## 12. Manual-start readiness statement

This Bootstrap package is ready for Owner manual Codex Goal start only when all fixed artifacts remain regular/non-symlink and mechanically match the Section 2/3 identities, the capability report remains absent before first execution, and no stage/commit/push/tag has been inferred from materialization.

Materializing this Bootstrap does not itself mean:

```text
SHADOW_PM_GOAL_STARTED = YES
CAPABILITY_DRY_RUN_ACCEPTED = YES
P1_G1_STARTED = YES
PRODUCT_MUTATION_OCCURRED = YES
REMOTE_AUTHORITY_CONSUMED = YES
GIT_MUTATION_AUTHORIZED = YES
```
