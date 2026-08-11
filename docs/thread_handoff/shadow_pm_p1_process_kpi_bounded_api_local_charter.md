# Edge MES Demo — Shadow Mainline PM P1 Process KPI + Bounded API Local Charter

Status: `OWNER_DELEGATED / READY_FOR_MANUAL_GOAL_BOOTSTRAP`

Goal ID: `P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1`

This Charter is the immutable Owner-delegated authority envelope for one manually started Codex Goal-mode Shadow Mainline PM session family. It does not itself start Codex, execute a specialist Gate, stage/commit/push Git, access remote runtime or authorize any action beyond the bounded local G3/G4 scope below.

Authority precedence:

```text
PM Rules
> this Charter
> exact current repository-backed task
> accepted specialist report
> mutable Goal Ledger
```

`docs/reports/p1_process_kpi_bounded_api_accepted_state_capsule.md` is the compact accepted semantic baseline and reading-efficiency context. It does not grant executable authority.

## 1. Sole Goal outcome

Convert the already published P1 Quality + Trace accepted baseline into one locally review-accepted **Process KPI semantics + bounded production metrics API** candidate, then stop before P1-G5 remote reconciliation.

Normal path:

```text
published Quality + Trace baseline
-> capability check
-> P1-G3 Process KPI + OEE Data-Sufficiency Contract
-> P1-G4-I Bounded Production Metrics API Implementation
-> P1-G4-R Focused Reliability
-> P1-G4-DQ Focused Data Quality
-> P1-G4-V Focused Verification
-> Shadow PM final local acceptance
-> STOP
```

Successful terminal:

`PASS / P1_PROCESS_KPI_BOUNDED_API_LOCAL_MVP_AUTONOMOUS_GOAL_COMPLETE`

This terminal does not establish P1-G5 remote/runtime validation or final P1 PM acceptance.

## 2. Product truth principle

The Goal must preserve:

> 能算的必须算对；不能算的必须明确说不能算；不得为了 Dashboard 完整度制造业务真值。

Accepted production authority remains `production_accepted_station_event_fact` plus only explicitly accepted auxiliary authority. Legacy KPI/Trace objects are compatibility/diagnostic sources and may not silently become new production truth.

The Goal must fail closed rather than manufacture semantics from:

```text
production_snapshot
cycle_event
station_event
production_unit
quality_event
raw_plc_sample
adapter diagnostics
current YAML substituted for historical config
fixed WS03
adjacent-row / time-proximity / counter-only cycle pairing
natural query-window duration relabeled as operating time
```

## 3. Success criteria

The parent Shadow Mainline PM may establish Goal success only when one unchanged final G4 candidate state satisfies all applicable criteria below and all three focused reviews bind that same state:

```text
PREDECESSOR_P1_QUALITY_TRACE_BASELINE_PUBLISHED = YES
G3_PROCESS_KPI_CONTRACT_ACCEPTED = YES
G4_BOUNDED_PRODUCTION_METRICS_API_ACCEPTED = YES
PRODUCTION_ACCEPTED_FACT_ONLY = YES
LEGACY_KPI_FALLBACK = NO
LEGACY_TRACE_FALLBACK = NO
OUTPUT_COUNTING_UNIT_EXPLICIT = YES
DATA_SUFFICIENCY_EXPLICIT = YES
HALF_OPEN_WINDOW = YES
READ_ONLY_API = YES
FAIL_CLOSED_SOURCE_UNAVAILABLE = YES
STATION_CT_FALSE_CLAIM = NO
HISTORICAL_TERMINAL_FALSE_CLAIM = NO
IDEAL_CT_FALSE_CLAIM = NO
PERFORMANCE_FALSE_CLAIM = NO
AVAILABILITY_FALSE_CLAIM = NO
FULL_OEE_NUMERIC_CLAIM = NO
DB_MIGRATION = 0
HISTORICAL_CONFIG_REGISTRY_IMPLEMENTATION = 0
COLLECTOR_CHANGE = 0
CONFIG_CHANGE = 0
FRONTEND_CHANGE = 0
REMOTE_ACTION = 0
PRODUCTION_STIMULUS = 0
GIT_MUTATION = 0
RELIABILITY_ACCEPTED = YES
DATA_QUALITY_ACCEPTED = YES
VERIFICATION_ACCEPTED = YES
FINAL_REVIEWS_BIND_SAME_CANDIDATE = YES
UNAUTHORIZED_ACTIONS = 0
```

Success does **not** require turning predecessor `PARTIAL` or `UNSUPPORTED` states into numeric metrics. A truthful API that exposes explicit sufficiency/status/reason and refuses unsupported numeric claims may PASS.

## 4. G3 required semantic decisions

P1-G3 is a Data Quality-owned contract Gate. It consumes the accepted Capsule/G0/G1 facts and must not rerun G0 source adequacy simply to restate already accepted insufficiency.

G3 must freeze at least:

```text
1. station accepted-result event count semantics
2. explicit counting unit: event-count vs unit-count vs unavailable
3. station observed output-rate semantics, if product-worthy
4. line/terminal output sufficiency and terminal-resolution failure behavior
5. station cycle-time sufficiency and forbidden pairing heuristics
6. ideal cycle-time sufficiency and historical lineage requirement
7. Quality component reuse from accepted predecessor semantics
8. Performance sufficiency
9. Availability sufficiency
10. Full OEE sufficiency
11. mixed-config-window behavior
12. empty-window behavior
13. unsupported / partial / unavailable response semantics
14. source-unavailable behavior
15. bounded scope/window semantics
16. exact G4 endpoint/DTO contract sufficient for implementation
```

G3 must explicitly distinguish any calendar-window/event rate from OEE `Performance`. Query-window elapsed time is not an authoritative operating-time denominator unless fresh accepted authority proves otherwise.

Preferred additive contract path:

`docs/contracts/production_process_kpi_contract.md`

The existing published `docs/contracts/production_metrics_contract.md` is predecessor Quality + Trace contract and should remain unchanged unless a fresh contradiction makes modification unavoidable. If G3 concludes modifying that predecessor contract is necessary, stop with `HOLD / PREDECESSOR_ACCEPTED_CONTRACT_CHANGE_REQUIRES_OWNER_REVIEW` rather than silently invalidating the closed Goal.

## 5. G4 implementation boundary

P1-G4 may implement only the accepted G3 contract using bounded local API code/tests.

Preferred separation of responsibility:

```text
api/app/routes/quality_trace.py = accepted Quality + Trace neighbor
new focused Process KPI route module = G4 Process KPI / sufficiency API
new focused test module = G4 contract tests
api/app/main.py = route registration only if required by exact G4 task
```

The exact route/test path and endpoint names must be frozen by the G3 contract and exact G4 task. This Charter does not pre-authorize directory-wide mutation.

G4 must not clean up or migrate legacy `/kpi/*` or `/trace/*` merely for consistency. Legacy cleanup is not a success criterion.

## 6. Explicit non-goals

This Goal does not implement, mutate, validate remotely or authorize:

- P1-G5 Raspberry Pi DB/API reconciliation;
- P1-G6 final P1 PM acceptance;
- historical immutable config registry/snapshot implementation;
- DB migration or schema redesign;
- Collector, decoder, ingestion, ACK/read_done or storage changes;
- config file mutation or config publication;
- PLC / V-PLC;
- Docker/Compose, image build/load, deployment or activation;
- SSH/network/remote actions;
- production data stimulus;
- Frontend/Dashboard changes;
- Full Genealogy, Hold/Rework, parent-child inference or Missing Unit/Data Gap inference;
- Performance or Availability fabrication;
- Full OEE numeric implementation without independently accepted required source authority;
- parallel `FIELD-VALIDATION-COLLECTOR-DB` interaction;
- Git stage/commit/push/tag/reset/stash/restore/checkout/rebase/merge/clean;
- modification of `docs/thread_handoff/pm_operating_rules.md` or `docs/current_status.md`;
- self-expansion of this Charter.

If a non-goal becomes necessary to complete the product claim truthfully, stop for Owner review. Do not broaden scope by rewording the failure.

## 7. Genesis repository baseline

The Owner-authorized genesis baseline is the published predecessor commit:

```text
branch = main
HEAD = cf4eac54d3f365b0addfaae13f5e7292e3233641
parent = dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
origin/main = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
origin/main...HEAD = 0<TAB>2
cached/staged = empty
tracked dirty = docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
```

The two tracked-dirty docs are protected external continuity state. Pre-existing untracked artifacts remain external unless an exact task owns them. The Goal must never clean or broad-stage the worktree.

Fresh live repository checks override stale continuity observations but do not silently rewrite this Genesis. Unexpected branch/HEAD/staged changes require read-only classification before continuation.

## 8. Accepted-state context and reading economy

Default historical context is:

`docs/reports/p1_process_kpi_bounded_api_accepted_state_capsule.md`

Parent bootstrap performs the broader full-read once. Disposable children use bounded required reading:

1. their exact task file;
2. PM Rules sections needed by that task;
3. this Charter;
4. the Accepted State Capsule;
5. the current accepted G3 contract when applicable;
6. exact candidate/source/test files required for their Gate;
7. only the immediately preceding report when causally necessary.

Children must not routinely read old P0/P1 repair reports, predecessor Goal prompt/bootstrap, predecessor full Ledger or every historic task. Old evidence is read only when a fresh contradiction, identity question or root-cause investigation requires it.

This efficiency rule is subordinate to safety/authority facts: a task may read additional exact files when genuinely needed, but it must state why.

## 9. Controller responsibilities

Exactly one long-lived controller exists: `Shadow Mainline PM`.

The controller must:

1. recover PM Rules, Charter, Capsule, Ledger and live Git continuity;
2. establish/refresh one capability epoch before real Gate dispatch;
3. identify exactly one smallest eligible Gate;
4. materialize one immutable repository-backed 16-section task;
5. dispatch exactly one disposable specialist for that task;
6. never execute the specialist task and then self-accept it;
7. receive durable child terminal/report;
8. independently verify task/report identities, changed paths, tests/evidence, Git state and authority compliance;
9. classify earliest causal failure family;
10. update Ledger and only invalidate acceptances depending on changed objects;
11. check budgets, drift and governance inflation;
12. automatically issue the smallest next in-scope task or stop at a defined terminal.

A child may not update the Ledger, create successor tasks, spawn child agents, self-intake or self-advance.

## 10. Specialist ownership

Normal ownership:

```text
P1-G3 Process KPI Contract -> Data Quality
P1-G4-I Bounded Production Metrics API -> Architecture / Integration
P1-G4-R Focused Reliability -> Reliability
P1-G4-DQ Focused Data Quality -> Data Quality
P1-G4-V Focused Verification -> Verification
```

When root cause is genuinely unclear, the controller may dispatch one read-only diagnostic specialist within budget. Diagnostic work receives no source/test mutation authority.

Concurrency:

```text
MAX_NORMAL_OR_MUTATION_CHILDREN_ACTIVE = 1
MAX_DIAGNOSTIC_CHILDREN_ACTIVE = 1
MAX_MUTATION_WORKERS_ACTIVE = 1
```

No diagnostic and mutation child may work concurrently against the same candidate.

## 11. State machine

```text
BOOTSTRAP
-> CAPABILITY_CHECK
-> P1-G3_PROCESS_KPI_CONTRACT
-> PM_INTAKE_G3
-> P1-G4-I_BOUNDED_PRODUCTION_METRICS_API
-> PM_INTAKE_G4_I
-> P1-G4-R_FOCUSED_RELIABILITY
-> PM_INTAKE_G4_R
-> P1-G4-DQ_FOCUSED_DATA_QUALITY
-> PM_INTAKE_G4_DQ
-> P1-G4-V_FOCUSED_VERIFICATION
-> PM_INTAKE_G4_V
-> FINAL_PM_INTAKE
-> COMPLETE
```

Capability check is control-plane bootstrap and does not consume `TOTAL_DISPATCHED_GATES`.

No G5 task may be created from this Goal.

## 12. Action classes

Each exact task authorizes the smallest applicable subset:

```text
A0_CONTROL_PLANE = task/report/ledger/closeout/capability records
A1_CONTRACT = exact G3 contract docs
A2_LOCAL_PRODUCT = exact local API/test source mutation
A3_LOCAL_VALIDATION = exact local compile/import/test/static checks + read-only Git
A4_DIAGNOSTIC = behaviorally read-only diagnosis
A5_EXTERNAL_OR_IRREVERSIBLE = Git mutation, DB runtime/write, Docker, remote, PLC, deploy, production action
```

`A5_EXTERNAL_OR_IRREVERSIBLE` is forbidden for the entire Goal.

A2 never means directory authority. Every task must name exact mutable paths.

## 13. Runtime authority split

### 13.1 Control-plane Python

PM Rules control-plane runtime remains frozen:

```text
entrypoint = /opt/homebrew/opt/python@3.14/bin/python3.14
version = Python 3.14.6
architecture = arm64
resolved bytes = 52448
resolved SHA-256 = b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf
```

Use it for authority-bearing task/report hashing, parsing, identity verification, evidence generation and PM/control-plane helpers.

### 13.2 Owner-approved project test runtime

For this Goal only, the Owner explicitly authorizes the existing project venv for exact task-authorized local Python compile/import/test execution:

```text
entrypoint = <project-root>/.venv/bin/python
pyvenv.cfg version = 3.13.3
runtime = Python 3.13.3
architecture = arm64
resolved base = /Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13
resolved base bytes = 119328
resolved base SHA-256 = f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5
pytest = 9.1.1
fastapi = 0.115.6
psycopg = 3.2.3
```

Every task using this runtime must fresh-verify the applicable identity/version fields before the first test start. Drift is `HOLD / PROJECT_TEST_RUNTIME_DRIFT`.

Forbidden:

```text
venv mutation
pip/package install/update
venv recreation
runtime fallback
using project test runtime for PM/control-plane hashing or evidence authority
```

This is a durable Goal-level exact-runtime override for local validation only; it does not need a one-shot Owner amendment for every G4/R/DQ/V test.

## 14. Normal repair autonomy

Ordinary in-scope local `PRODUCT_DEFECT`, `TEST_DEFECT`, `CONTRACT_DEFECT`, `TASK_CONTRACT_DEFECT` or local evidence defect does not automatically require Owner intervention.

When all are true:

```text
current blocker belongs to this Goal
root cause is actionable
exact repair paths can be bounded
no non-goal authority is required
MVP/Goal scope is unchanged
architecture redesign is not required
relevant failure-family and Goal budgets remain
repository ownership is unambiguous
```

controller must:

```text
INDEPENDENT INTAKE
-> earliest causal family
-> smallest fresh repair task
-> one disposable child
-> independent intake
-> continue or stop
```

Do not stop for `OWNER_AUTHORITY_REQUIRED` merely because a bounded local code/test repair is needed and the Charter already delegates it.

A repair that changes G3 semantics invalidates G4 and all downstream reviews. A test-only mechanical repair invalidates only review claims that bind the changed test/candidate state. Never replay unchanged-lineage review work mechanically.

## 15. Failure-family and Goal budgets

Per earliest causal failure family:

```text
MAX_NORMAL_ATTEMPTS_PER_FAILURE_FAMILY = 2
MANDATORY_DRIFT_REVIEW_BEFORE_ATTEMPT_3 = YES
MAX_POST_DRIFT_REDESIGNED_ATTEMPTS = 1
ABSOLUTE_MAX_ATTEMPTS_PER_FAILURE_FAMILY = 3
```

Goal budgets:

```text
MAX_PRODUCT_REPAIR_GATES_PER_GOAL = 3
MAX_CONTROL_PLANE_RECOVERY_GATES_PER_GOAL = 1
MAX_TOTAL_DISPATCHED_GATES = 9
```

Planned dispatched progress Gates are G3, G4-I, G4-R, G4-DQ and G4-V = 5. Capability check, pure parent intake and Ledger-only updates do not count.

Restart never resets counters.

## 16. Governance-inflation and drift rules

Track `NO_PRODUCT_PROGRESS_STREAK`.

If two consecutive dispatched Gates only repair runner/report/launcher/hash/manifest/publication/control-plane mechanics without advancing contract/product/review/blocker truth, parent must perform a governance-inflation review before any further dispatch.

A third consecutive no-product-progress Gate is forbidden automatically:

`HOLD / GOVERNANCE_OR_VALIDATION_INFLATION`

Mandatory drift questions:

```text
MVP_ALIGNMENT = YES?
GOAL_ALIGNMENT = YES?
SCOPE_EXPANSION = NO?
ARCHITECTURE_REDESIGN_REQUIRED = NO?
ROOT_CAUSE_ACTIONABLE = YES?
AUTHORITY_ENVELOPE_SUFFICIENT = YES?
EVIDENCE_WORK_GREATER_THAN_PRODUCT_WORK = NO?
```

Triggers requiring Owner rather than automatic scope expansion include any apparent need for historical config registry, DB migration, Collector/config changes, remote/runtime, frontend, Full OEE source expansion, generic evidence platform or architecture redesign.

## 17. Owner-intervention conditions

Stop for Owner when any becomes necessary/true:

```text
DB migration/schema change
historical config registry implementation required for Goal success
Collector/config/VPLC/PLC change
frontend/dashboard change
remote/Raspberry Pi/runtime validation
Git stage/commit/push/tag
Performance/Availability source-model expansion
Full OEE source-model expansion
architecture redesign or MVP redefinition
predecessor accepted Quality/Trace contract semantic modification
parallel branch interaction
failure-family budget exhausted
product-repair budget exhausted
control-plane recovery budget exhausted
global 9-Gate budget exhausted
ambiguous product mutation state not reconcilable read-only
repository ownership/dirty-state conflict on task-owned paths
controller/child independence unavailable
sub-agent capacity exhaustion
```

Use the most specific HOLD terminal available.

## 18. Durable task / restart rules

Every dispatched Gate uses PM Rules repository-backed immutable task format and durable phase transitions:

```text
TASK_PUBLISHED
DISPATCH_INTENT_RECORDED
EXECUTOR_TERMINAL_AVAILABLE
PM_INTAKE_ACCEPTED
```

Restart procedure:

1. read PM Rules;
2. verify this Charter;
3. read Bootstrap, Capsule and current Ledger;
4. recover live Git root/branch/HEAD/origin/cached/protected dirty state;
5. inspect last task/report exact identity and current durable phase;
6. restore all counters/accepted Gates;
7. never replay a mutation-capable task until changed paths/report/evidence are reconciled.

If mutation state remains ambiguous: `HOLD / AMBIGUOUS_MUTATION_STATE`.

A completed product/test operation with a later report-publication failure may receive at most one exact report-only recovery for that control-plane family, within the Goal's single control-plane recovery budget, only when product state is independently reconstructable and zero product/test mutation is required.

## 19. Review acceptance

Each accepted G4 review must record:

```text
review role
report path / bytes / SHA-256
candidate changed-path set
candidate exact identity set
G3 contract identity
focused validation result
blockers
recommendations classification
parent PM intake
```

Final acceptance requires Reliability, Data Quality and Verification to bind one exact candidate/contract state.

Recommendations are not automatically work. Parent classifies each as blocker, carry-forward, future independent task or unnecessary scope expansion.

## 20. Terminal states

Success:

```text
GOAL_STATUS = COMPLETE
SHADOW_PM_STOP = YES
CURRENT_FAILURE_FAMILY = NONE
P1_G5_EXECUTION_AUTHORIZED = NO
REMOTE_AUTHORITY_CONSUMED = NO
GIT_MUTATION_AUTHORIZED = NO
GOAL_TERMINAL = PASS / P1_PROCESS_KPI_BOUNDED_API_LOCAL_MVP_AUTONOMOUS_GOAL_COMPLETE
NEXT_ACTION = STOP / OWNER_REVIEW_EXACT_GIT_PUBLICATION_THEN_P1_G5
```

Recognized HOLDs include:

```text
HOLD / SHADOW_PM_SUBAGENT_CAPABILITY_UNAVAILABLE
HOLD / OWNER_REVIEW_REQUIRED
HOLD / SCOPE_RESET_REQUIRED
HOLD / PREDECESSOR_ACCEPTED_CONTRACT_CHANGE_REQUIRES_OWNER_REVIEW
HOLD / PROJECT_TEST_RUNTIME_DRIFT
HOLD / REPOSITORY_AUTHORITY_DRIFT
HOLD / AMBIGUOUS_MUTATION_STATE
HOLD / FAILURE_FAMILY_BUDGET_EXHAUSTED
HOLD / PRODUCT_REPAIR_BUDGET_EXHAUSTED
HOLD / CONTROL_PLANE_RECOVERY_BUDGET_EXHAUSTED
HOLD / P1_AUTONOMY_COMPLEXITY_BUDGET_EXHAUSTED
HOLD / GOVERNANCE_OR_VALIDATION_INFLATION
HOLD / AGENT_THREAD_CAPACITY_EXHAUSTED
```

A HOLD preserves all previously accepted predecessor/G3/G4 facts and counters; it never grants cleanup or new authority.

## 21. Final stop boundary

This Goal must stop immediately after local G4 final intake. It may write its exact final closeout report and Ledger terminal under A0 authority, but it may not create P1-G5 tasks, stage/commit/push the candidate, access Raspberry Pi or consume production/runtime authority.
