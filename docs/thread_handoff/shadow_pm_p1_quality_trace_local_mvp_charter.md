# Edge MES Demo — Shadow Mainline PM P1 Quality + Trace Local MVP Charter

Status: `OWNER_DELEGATED / READY_FOR_MANUAL_GOAL_BOOTSTRAP`

Goal ID: `P1-SHADOW-PM-QUALITY-TRACE-LOCAL-MVP-V1`

This Charter is the immutable Owner-delegated authority envelope for one manually started Codex Goal-mode Shadow Mainline PM session family. It is not a product task, does not itself start Codex, does not execute a Gate, and does not grant authority outside the exact P1 local MVP scope below.

PM Rules remain superior to this Charter. A mutable ledger records continuity only and never grants executable authority. Every actual specialist action still requires one exact repository-backed 16-section task file.

## 1. Goal outcome

The sole Goal outcome is:

**Convert the Mainline-PM-accepted P1-G0 production-truth baseline into one locally review-accepted Quality + accepted-fact Trace MVP candidate, then stop before P1-G3.**

Normal product path:

```text
accepted P1-G0 source boundary
-> P1-G1 Production Semantics Contract
-> P1-G2 Quality + accepted-fact Trace implementation
-> focused Reliability
-> focused Data Quality
-> focused Verification
-> Shadow PM final local acceptance
-> STOP
```

Successful terminal:

`PASS / P1_QUALITY_TRACE_LOCAL_MVP_AUTONOMOUS_GOAL_COMPLETE`

This Goal does not mean all of P1 is complete and does not establish remote/runtime acceptance.

## 2. Success criteria

The Shadow Mainline PM may establish the successful terminal only when all of the following are independently accepted against one unchanged final candidate state:

```text
P1_G0_PM_ACCEPTED = YES
G1_PRODUCTION_SEMANTICS_CONTRACT_ACCEPTED = YES
QUALITY_ACCEPTED_FACT_ONLY = YES
TRACE_ACCEPTED_FACT_ONLY = YES
STATION_RESULT_OK_NOK_SUPPORTED = YES
ACCEPTED_NOK_EVIDENCE_SUPPORTED = YES
NULL_UNIT_ID_FAILS_PARTIAL = YES
NULL_DMC_FAILS_PARTIAL = YES
MISSING_STATION_VISIBLE = YES
TIME_PROXIMITY_TRACE_FILL = NO
LEGACY_TRACE_FALLBACK = NO
LEGACY_KPI_FALLBACK = NO
FIXED_WS03_PRODUCTION_AUTHORITY = NO
FULL_GENEALOGY_CLAIM = NO
FULL_OEE_NUMERIC_CLAIM = NO
DB_MIGRATION = 0
COLLECTOR_CHANGE = 0
FRONTEND_CHANGE = 0
REMOTE_ACTION = 0
RELIABILITY_ACCEPTED = YES
DATA_QUALITY_ACCEPTED = YES
VERIFICATION_ACCEPTED = YES
FINAL_CANDIDATE_REVIEWS_BIND_SAME_STATE = YES
UNAUTHORIZED_ACTION = 0
```

A successful candidate may still expose `PARTIAL` or `UNSUPPORTED` data-sufficiency states exactly where the accepted G0 baseline requires them. Success does not require historical route/order/terminal resolution, exact station cycle-time pairing, Performance, Availability or Full OEE.

## 3. Explicit non-goals

This Goal does not implement, validate or authorize:

- P1-G3 Process KPI / Partial OEE implementation;
- P1-G4 broader production metrics/API work beyond the Quality + accepted-fact Trace slice selected by G1/G2;
- P1-G5 Raspberry Pi DB/API/runtime reconciliation;
- Performance or Availability calculation;
- Full OEE numeric calculation;
- immutable historical config-registry implementation;
- DB migration or schema redesign;
- `unit_relation`, full Genealogy, parent-child assembly inference or rework genealogy;
- Hold, Rework, Data Gap or Missing Unit inference;
- Collector, decoder, ingestion, ACK/read_done, V-PLC or PLC changes;
- Docker/Compose, image build/load, deployment, SSH, remote/network or production stimulus;
- Frontend/Dashboard implementation;
- legacy `/kpi/*` or `/trace/*` cleanup merely for consistency;
- mutation or authority import from `FIELD-VALIDATION-COLLECTOR-DB`;
- Git stage, commit, push, tag, release, reset, stash, restore, checkout, rebase, merge or clean;
- modification of `docs/thread_handoff/pm_operating_rules.md`;
- self-expansion of this Charter.

If any non-goal becomes necessary to complete the current Goal, stop with `HOLD / SCOPE_RESET_REQUIRED / OWNER_REVIEW` or a more specific Owner-required terminal. Do not expand the Charter to make the action legal.

## 4. Genesis / accepted baseline

Owner-authorized genesis is the state independently intaken by Mainline PM immediately before this Charter was materialized.

Repository/Git genesis:

```text
branch = main
HEAD = dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
origin/main = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
origin/main...HEAD = 0<TAB>1
HEAD ahead = 1
HEAD behind = 0
cached/staged = empty
tracked dirty = docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
```

Protected dirty paths above must remain preserved unless a future exact Owner authority explicitly supersedes that protection. The large pre-existing untracked corpus is external continuity state and must not be cleaned, broad-staged, adopted or rewritten by convenience.

P1 plan baseline:

```text
path = docs/reports/p1_production_truth_semantics_trusted_consumption_plan.md
bytes = 15505
SHA-256 = 48a9d8af24ed4f106ef724634229055887ce71c74ffc38d208aa28bc2192d88e
```

P1-G0 accepted baseline:

```text
path = docs/reports/p1_g0_production_source_adequacy_semantic_boundary_freeze.md
bytes = 38063
SHA-256 = 10982b8a92d0c33bfd18812ec14879af9ea74f658a74ab046b4d71d2725ef87e
executor terminal = PASS WITH RECOMMENDATIONS
Mainline PM intake = ACCEPTED
P1_G0_PM_ACCEPTED = YES
P1_G0_VERIFIED = NO
MVP_ALIGNMENT = MVP-ALIGNED WITH BACKLOG ITEMS
```

Accepted semantic genesis:

```text
production_accepted_station_event_fact = sole P1 accepted station-business PRODUCTION_AUTHORITY
station-scoped Quality = SUPPORTED
accepted event timeline = SUPPORTED
unit_id Trace = PARTIAL
dmc Trace = PARTIAL
historical route/order/terminal = PARTIAL
throughput = PARTIAL
station cycle time = PARTIAL
ideal cycle time = PARTIAL
Performance = UNSUPPORTED
Availability = UNSUPPORTED
Full OEE = UNSUPPORTED
NO_NEW_DB_MIGRATION_REQUIRED_FOR_QUALITY_TRACE_VERTICAL_SLICE = YES
```

G0 recommendations are accepted carry-forward constraints, not current blockers. In particular, unresolved historical config lineage does not block a truthful station-scoped Quality + accepted-fact Trace MVP if the product explicitly preserves `PARTIAL/UNAVAILABLE` semantics.

## 5. Controller responsibilities

Only one long-lived controller exists: `Shadow Mainline PM`.

The controller must:

1. recover PM Rules, this Charter, mutable Ledger and live repository continuity;
2. determine exactly one smallest currently eligible Gate;
3. create one exact repository-backed task for that Gate;
4. select exactly one disposable specialist role appropriate to the task;
5. dispatch the child without executing the task itself;
6. receive the child terminal and durable report;
7. independently intake report identity, changed paths, Git state, tests/evidence, conclusion consistency and authority compliance;
8. classify PASS/HOLD and the earliest causal failure family;
9. invalidate only downstream acceptances whose claims depend on changed bytes/contracts;
10. update the mutable Ledger and counters;
11. perform budget/drift/governance-inflation checks before issuing another task;
12. either issue one next smallest Gate or stop with a terminal state.

The controller must not execute a specialist's task and then approve its own execution evidence as independent intake. It must not redefine P1-G0 truth, MVP scope, PM Rules or this Charter.

## 6. Specialist model

Use disposable specialists aligned to existing core ownership:

- `Architecture / Integration` — bounded integration design/implementation and contract-to-code boundary;
- `Reliability` — stale/failure behavior, consistency, bounded read behavior and runtime-safety implications within local scope;
- `Data Quality` — production truth, Quality/Trace semantics, source authority, partial/unavailable behavior and no-fallback constraints;
- `Verification` — independent contract/result recomputation, negative leakage, scope/window behavior and test adequacy.

Recommended normal ownership:

```text
P1-G1 Production Semantics Contract -> Data Quality
P1-G2-I Quality + Trace Implementation -> Architecture / Integration
P1-G2-R Focused Reliability -> Reliability
P1-G2-DQ Focused Data Quality -> Data Quality
P1-G2-V Focused Verification -> Verification
```

When root cause is unclear, the controller may issue one behaviorally read-only diagnostic task to an appropriate disposable specialist. A diagnostic receives no mutation authority even if its inherited client sandbox is technically workspace-write.

One child receives one task and may write only task-authorized outputs. Children may not spawn children, update the Shadow PM Ledger, consume their own terminal, create successor tasks or inherit authority from predecessor tasks.

Active concurrency invariants:

```text
MAX_NORMAL_OR_MUTATION_CHILDREN_ACTIVE = 1
MAX_DIAGNOSTIC_CHILDREN_ACTIVE = 1
MAX_MUTATION_WORKERS_ACTIVE = 1
```

No normal/mutation child and diagnostic child may operate concurrently against the same candidate state.

## 7. Gate state machine

Capability bootstrap precedes real product Gates and does not count as a P1 dispatched Gate.

Normal state machine:

```text
READY_FOR_CAPABILITY_DRY_RUN
-> CAPABILITY_DRY_RUN
-> P1-G1_PRODUCTION_SEMANTICS_CONTRACT
-> PM_INTAKE_G1
-> P1-G2-I_QUALITY_TRACE_IMPLEMENTATION
-> PM_INTAKE_G2_I
-> P1-G2-R_FOCUSED_RELIABILITY
-> PM_INTAKE_G2_R
-> P1-G2-DQ_FOCUSED_DATA_QUALITY
-> PM_INTAKE_G2_DQ
-> P1-G2-V_FOCUSED_VERIFICATION
-> PM_FINAL_INTAKE
-> COMPLETE / STOP
```

Executor transition rules:

```text
EXECUTOR_PASS -> CONTROLLER_PM_INTAKE -> ACCEPTED_PASS -> NEXT_SMALLEST_GATE
EXECUTOR_HOLD -> CONTROLLER_PM_INTAKE -> ACCEPTED_HOLD -> RCA/BUDGET/DRIFT -> REPAIR_OR_STOP
```

Forbidden:

`EXECUTOR_PASS -> EXECUTOR_CREATES_NEXT_TASK`.

A repair that changes a semantic contract invalidates every downstream acceptance that depends on that contract. A test-only or mechanically isolated repair invalidates only reviews whose claims depend on the changed object. Do not mechanically replay unchanged-lineage reviews.

## 8. Repository durable-state design

Fixed Goal-control artifacts:

```text
docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter.md
docs/reports/shadow_pm_p1_quality_trace_local_mvp_ledger.md
docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_goal_prompt.md
docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_bootstrap_dry_run.md
docs/reports/p1_quality_trace_local_mvp_goal_closeout.md
```

The Charter is immutable after Owner publication. A correction requires a new Owner-authorized Charter identity or explicit amendment; the controller may not edit it.

The Ledger is mutable continuity/index state only. It is never executable authority. Every task action requires a separate exact task file under the PM Rules repository-backed task format.

The Goal Prompt is stable Owner-facing bootstrap text. It points to the Charter/Bootstrap/Ledger rather than duplicating volatile state.

The Bootstrap records exact entry identities and capability procedure. The capability task is a separately materialized exact repository-backed task.

The final closeout report is absent at genesis and may be written only at successful Goal closure or an Owner-visible terminal requiring durable handoff, under the Charter's control-plane authority.

Dynamic specialist tasks follow:

`docs/thread_handoff/pm_task_<YYYYMMDDTHHMMZ>_<task-id>_<slug>.md`

Future product/review tasks must not be pre-created during bootstrap.

## 9. Authority envelope

The Owner delegates a bounded, non-self-expanding local authority sufficient only for this Goal.

### 9.1 Controller control-plane authority

The controller may create/update, subject to PM Rules exact-path governance:

- one next repository-backed specialist task at a time;
- the mutable Goal Ledger;
- controller PM-intake/decision records when durable intake is needed;
- the final Goal closeout report;
- one report-only recovery task when Section 14 permits it.

Control-plane authority never grants stage/commit/push/tag.

### 9.2 G1 contract authority

A fresh G1 task may authorize only the minimum exact docs/contract paths needed to freeze production semantics for the Quality + accepted-fact Trace MVP. G1 may explicitly preserve `PARTIAL/UNSUPPORTED` items instead of resolving them.

### 9.3 G2 local product authority

A fresh G2 implementation/repair task may authorize only exact source/test paths required for the accepted Quality + Trace slice, normally within `api/`, `api/tests/` and exact task-owned contract/test documentation. Directory-wide mutation is not implied. `api/app/main.py` may be authorized only if route registration is actually required.

Default excluded product roots include `db/`, `collector/`, `config/`, `frontend/`, `s7_plc_sim/` and deployment/runtime surfaces.

### 9.4 Validation authority

Fresh tasks may authorize bounded local tests/static checks and read-only Git inspection. Authority-bearing host-side Python must follow the frozen PM Rules runtime:

```text
entrypoint = /opt/homebrew/opt/python@3.14/bin/python3.14
version = Python 3.14.6
architecture = arm64
resolved bytes = 52448
resolved SHA-256 = b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf
```

No implicit/PATH Python fallback is permitted for authority-bearing use.

## 10. Mutation / action classes

Every generated task must classify its authorized actions using the smallest subset of:

```text
A0_CONTROL_PLANE = task/report/ledger/PM-intake/closeout writes
A1_CONTRACT = exact P1 semantics contract documentation
A2_LOCAL_PRODUCT = exact local API/product/test source mutation
A3_LOCAL_VALIDATION = local tests/static checks/read-only Git inspection
A4_DIAGNOSTIC = behaviorally read-only diagnosis/reconciliation
A5_EXTERNAL_OR_IRREVERSIBLE = Git mutation, DB runtime, Docker, remote, PLC, deploy, production action
```

`A0` through `A4` are only potentially delegable and still require an exact task allowlist. `A5` is forbidden by this Goal.

A task may combine `A2 + A3` when implementation and its focused local test cycle are one atomic product unit, but it must still name exact files/commands and stop before any later review authority.

## 11. Retry + failure-family budgets

Failure accounting is by earliest causal family, not filename or downstream symptom. Renaming/repackaging a task never resets a family.

Per failure family:

```text
MAX_NORMAL_ATTEMPTS_PER_FAILURE_FAMILY = 2
MANDATORY_DRIFT_REVIEW_BEFORE_ATTEMPT_3 = YES
MAX_POST_DRIFT_REDESIGNED_ATTEMPTS = 1
ABSOLUTE_MAX_ATTEMPTS_PER_FAILURE_FAMILY = 3
```

Goal-level budgets:

```text
MAX_PRODUCT_REPAIR_GATES_PER_GOAL = 3
MAX_CONTROL_PLANE_RECOVERY_GATES_PER_GOAL = 2
MAX_CONTROL_PLANE_RECOVERY_PER_FAMILY = 1
MAX_TOTAL_DISPATCHED_GATES = 10
```

The normal five progress Gates (`G1`, `G2-I`, `G2-R`, `G2-DQ`, `G2-V`) count toward total dispatched Gates. Product repair, diagnostic/recovery and independently dispatched review-repair Gates also count. Capability dry run, pure controller PM intake and ledger-only updates do not count.

A report-only recovery counts as control-plane recovery but must consume zero product mutation authority.

No counter resets after thread/client/process restart or a fresh parent Goal session.

## 12. Drift / governance-inflation rules

Every intake must classify whether the accepted result created real product progress. Product progress includes at least one of:

```text
new accepted contract truth
new accepted product behavior
new accepted focused test behavior
new accepted independent review state
closure of an actual product/data-truth blocker
```

Maintain `NO_PRODUCT_PROGRESS_STREAK`.

If two consecutive dispatched Gates only repair runner/report/launcher/hash/manifest/publication/tool mechanics without creating product progress, the controller must run a governance-inflation review before another dispatch. A third consecutive no-product-progress Gate is forbidden automatically.

Governance-inflation HOLD:

`HOLD / GOVERNANCE_OR_VALIDATION_INFLATION`

Drift review is also mandatory when work would require any of:

- DB migration/schema redesign;
- historical immutable config registry implementation;
- Collector/config/V-PLC change;
- Frontend/Dashboard implementation;
- Performance/Availability/Full OEE source implementation;
- remote/runtime/deployment action;
- a new generic evidence/audit framework;
- large helper infrastructure only to prove a simple bounded product fact;
- repeated renaming of the same blocker/recommendation.

Required drift questions:

```text
ROOT_CAUSE_STILL_IN_GOAL?
MVP_PATH_UNCHANGED?
GOAL_EXPANDED?
NEW_PRODUCT_CAPABILITY_REQUIRED?
EVIDENCE_WORK_GREATER_THAN_PRODUCT_WORK?
SIMPLER_MECHANICAL_PROOF_AVAILABLE?
CURRENT_AUTHORITY_SUFFICIENT?
```

Continuation after a mandatory drift review requires all of:

```text
MVP_ALIGNMENT = YES
GOAL_ALIGNMENT = YES
SCOPE_EXPANSION = NO
ARCHITECTURE_REDESIGN_REQUIRED = NO
ROOT_CAUSE_ACTIONABLE = YES
AUTHORITY_ENVELOPE_SUFFICIENT = YES
```

## 13. Owner-intervention conditions

The controller must stop for Owner intervention when any of the following becomes necessary or true:

```text
DB migration required
historical config registry implementation required for Goal success
Collector/config/VPLC change required
Frontend required
remote/runtime validation required
Git stage/commit/push/tag required
PM Rules modification required
parallel branch interaction required
Performance/Availability/Full OEE implementation required
architecture redesign or MVP redefinition required
failure-family budget exhausted
product-repair budget exhausted
control-plane recovery budget exhausted
global 10-Gate budget exhausted
ambiguous product mutation state cannot be reconciled read-only
repository ownership/dirty-state conflict with task-owned paths
controller/child independence unavailable
open spawned-thread capacity exhausted with no safe continuation
```

Use the most specific terminal available, otherwise `HOLD / OWNER_REVIEW_REQUIRED`.

## 14. Restart / ambiguous-state recovery

Every dispatched Gate must progress through durable controller states:

```text
TASK_PUBLISHED
DISPATCH_INTENT_RECORDED
EXECUTOR_TERMINAL_AVAILABLE
PM_INTAKE_ACCEPTED
```

On any controller/client/process restart:

1. read PM Rules;
2. read this Charter;
3. read Bootstrap and Ledger;
4. verify physical cwd, Git root, branch, HEAD/origin, cached/staged and protected dirty continuity;
5. inspect the last task/report exact identities and the Ledger phase;
6. restore all counters/failure families without reset;
7. continue only when current product and authority state are unambiguous.

Recovery rules:

- report exists but is not yet intaken -> do not rerun specialist; perform controller intake;
- task published and provably not dispatched -> if identity and prerequisites are unchanged, dispatch once;
- dispatch intent recorded but child state unknown -> first reconcile report presence and repository changed paths read-only;
- mutation task completion ambiguous -> never directly replay mutation; perform a bounded read-only reconciliation Gate if within Charter;
- if mutation state remains ambiguous -> `HOLD / AMBIGUOUS_MUTATION_STATE`;
- restart never resets budgets.

### Report-publication recovery

A product/test operation that completed and left durable unambiguous evidence is not automatically invalidated by a later report-writing/tooling failure.

The controller may issue at most one report-only recovery for that control-plane failure family when:

- the product state is independently reconstructable from durable repository/test/evidence state;
- no product/source/test mutation is needed to reconstruct the report;
- the recovery task writes only the exact report path and required control-plane evidence;
- action class is `A0_CONTROL_PLANE` plus read-only `A4_DIAGNOSTIC` only;
- the control-plane family has not already consumed its one recovery.

If durable evidence is insufficient, HOLD rather than replaying product mutation.

## 15. Terminal states

Successful terminal:

```text
GOAL_STATUS = COMPLETE
SHADOW_PM_STOP = YES
P1_G3_EXECUTION_AUTHORIZED = NO
REMOTE_AUTHORITY_CONSUMED = NO
GIT_MUTATION_AUTHORIZED = NO
GOAL_TERMINAL = PASS / P1_QUALITY_TRACE_LOCAL_MVP_AUTONOMOUS_GOAL_COMPLETE
```

Recognized Owner-visible HOLD terminals include:

```text
HOLD / SHADOW_PM_SUBAGENT_CAPABILITY_UNAVAILABLE
HOLD / CAPABILITY_DRY_RUN_UNAUTHORIZED_MUTATION
HOLD / CAPABILITY_DRY_RUN_STATE_AMBIGUOUS
HOLD / OWNER_AUTHORITY_REQUIRED
HOLD / OWNER_REVIEW_REQUIRED
HOLD / SCOPE_RESET_REQUIRED
HOLD / REPOSITORY_AUTHORITY_DRIFT
HOLD / AMBIGUOUS_MUTATION_STATE
HOLD / FAILURE_FAMILY_BUDGET_EXHAUSTED
HOLD / PRODUCT_REPAIR_BUDGET_EXHAUSTED
HOLD / CONTROL_PLANE_RECOVERY_BUDGET_EXHAUSTED
HOLD / P1_AUTONOMY_COMPLEXITY_BUDGET_EXHAUSTED
HOLD / GOVERNANCE_OR_VALIDATION_INFLATION
HOLD / AGENT_THREAD_CAPACITY_EXHAUSTED
```

A HOLD never grants cleanup/retry/repair authority beyond the exact bounded recovery already permitted by this Charter and a new task.

## 16. Final Goal Prompt contract

The Owner-facing Goal Prompt must remain compact and stable. It must instruct the manually started Codex Goal to:

- act only as the Shadow Mainline PM controller;
- read PM Rules, this Charter, Bootstrap and Ledger before real work;
- run a local-only parent/child capability dry run before real P1 work unless the same active parent session already has an accepted capability epoch;
- create exactly one repository-backed task at a time;
- delegate one disposable specialist per task;
- independently intake every specialist durable report;
- obey accepted P1-G0 truth, no-fallback constraints and `PARTIAL/UNSUPPORTED` semantics;
- obey failure/recovery/governance-inflation budgets;
- never expand into G3/G4/G5 or excluded authority;
- stop after local G2 acceptance.

The Goal Prompt itself is not independent executable authority. This Charter plus PM Rules bound every Goal action.

## 17. Bootstrap / capability dry run

Before any real G1 task, the manually started Goal must prove the current parent/controller session can safely orchestrate one disposable child.

Required parent-accepted capability facts:

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

The Bootstrap file freezes the exact capability task identity and procedure. The capability child may perform only bounded local read-only continuity plus its exact report write. It may not edit the Ledger or product files.

On accepted capability PASS, transition to:

```text
GOAL_STATUS = ACTIVE_P1_QUALITY_TRACE_LOCAL_AUTONOMY
CAPABILITY_DRY_RUN_ACCEPTED = YES
CURRENT_GATE = P1-G1_PRODUCTION_SEMANTICS_CONTRACT
CURRENT_GATE_STATUS = READY_TO_ISSUE
TOTAL_DISPATCHED_GATES = 0
PRODUCT_REPAIR_GATES_USED = 0
CONTROL_PLANE_RECOVERY_GATES_USED = 0
NO_PRODUCT_PROGRESS_STREAK = 0
NEXT_ACTION = GENERATE_EXACT_P1_G1_TASK
```

A new parent Goal session must establish a new capability epoch before issuing further specialist work, while restoring all product/recovery counters and accepted Gates from the Ledger. Accepted product Gates are never replayed solely because the parent session changed.

## 18. P1 truth invariants carried from G0

Every G1/G2 task and intake must preserve:

- accepted station-result truth originates from `production_accepted_station_event_fact` only;
- accepted NOK code/detail visibility stays tied to accepted business evidence;
- new P1 product paths may not fall back to legacy `cycle_event`, `production_snapshot`, `production_unit`, `quality_event`, raw/adapter diagnostics or time proximity;
- `unit_id` and DMC null/missing states remain explicit partial data, not silently repaired identities;
- missing stations remain visible missing/unknown facts;
- current YAML does not become historical config authority for facts with a different config lineage;
- fixed `WS03` is not P1 production authority;
- station cycle time remains partial unless a producer-authoritative exact pairing contract is independently established inside the accepted scope without expanding the Goal;
- Performance and Availability remain unsupported;
- Full OEE numeric output is forbidden in this Goal;
- Quality + accepted-fact Trace may proceed without a new DB migration.

## 19. Recommendation and blocker discipline

Every specialist recommendation must be classified by the controller as exactly one of:

```text
CURRENT_GOAL_BLOCKER
NEXT_REVIEW_CARRY_FORWARD
P1_G3_OR_LATER_BACKLOG
FIELD_VALIDATION_BRANCH_INPUT
UNNECESSARY_OR_SCOPE_EXPANSION
```

Only `CURRENT_GOAL_BLOCKER` may generate automatic repair. A recommendation cannot become a blocker merely because it improves completeness. G0 `PARTIAL/UNSUPPORTED` states are not blockers unless the Goal's explicit Quality + Trace success criteria cannot be met truthfully without changing them.

## 20. Git and repository isolation

This Goal grants zero Git mutation authority. Task/report/ledger files may exist untracked/unstaged. Product changes produced by authorized local tasks may also remain working-tree changes until the Goal stops; stage/commit is a later separate Owner decision.

The controller must preserve unrelated tracked dirty and untracked artifacts. Broad staging, broad cleanup, reset/stash/restore/rebase/merge/checkout are forbidden.

The parallel `FIELD-VALIDATION-COLLECTOR-DB` workstream remains governance-isolated. Its files/findings may only be imported into this Goal after explicit Owner authority; do not treat parallel branch state as implicit P1 Mainline truth.

## 21. Final closeout content

At successful terminal, the controller writes `docs/reports/p1_quality_trace_local_mvp_goal_closeout.md` and records at least:

- Goal ID and terminal;
- genesis and final live Git continuity;
- accepted P1-G0 baseline;
- accepted G1 contract report/task identity;
- final candidate changed paths and identities;
- accepted Reliability/Data Quality/Verification reports;
- exact tests/static validation used by the accepted final candidate;
- failure families and attempts;
- product repair/control-plane/total Gate counters;
- unauthorized-action counters;
- residual recommendations/backlog;
- MVP classification;
- `P1_G3_EXECUTION_AUTHORIZED = NO`;
- `REMOTE_AUTHORITY_CONSUMED = NO`;
- `GIT_MUTATION_AUTHORIZED = NO`;
- one next Owner recommendation only.

The closeout report cannot grant G3 or Git/remote authority.

## 22. Non-inheritance statement

Starting this Goal does not inherit authority from P0 Shadow PM, B1, historical deployment/runtime tasks, G0 specialist execution, or the parallel field-validation branch. P0 budgets are historical evidence only. P1 budgets, Gate state and authority are exactly those in this Charter.

A prior PASS authorizes only the accepted fact it established. Every new Gate still requires the controller to prove eligibility and issue one exact task.
