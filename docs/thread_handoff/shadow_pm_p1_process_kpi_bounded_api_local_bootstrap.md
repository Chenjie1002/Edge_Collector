# Shadow Mainline PM P1 Process KPI + Bounded API Local — Owner Manual Bootstrap

Status: `READY_FOR_OWNER_MANUAL_START`

Goal ID: `P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1`

This file is the manual bootstrap procedure for the bounded G3+G4 local Goal. It does not start Codex, execute G3/G4, mutate product code, stage/commit/push Git, access DB runtime/remote or authorize P1-G5.

## 1. Owner manual start

Owner activation:

1. Open macOS Codex client.
2. Open project folder `/Users/chenjie/Documents/MES/edge-mes-demo`.
3. Start a **new Goal-mode session**.
4. Paste the complete content of `docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_goal_prompt.md`.
5. Start the Goal manually.

Until Step 5:

```text
SHADOW_PM_GOAL_STARTED = NO
P1_G3_G4_AUTONOMOUS_EXECUTION_STARTED = NO
REMOTE_AUTHORITY_CONSUMED = NO
GIT_MUTATION_AUTHORIZED = NO
```

The predecessor Quality+Trace Goal is closed and must not be reopened. This is a new Goal with a new Ledger and budget, based on the published predecessor commit.

## 2. Immutable bootstrap identities

### Accepted State Capsule

```text
path = docs/reports/p1_process_kpi_bounded_api_accepted_state_capsule.md
regular / non-symlink
bytes = 8201
SHA-256 = 643b2c39e1e37da542cf077be71d511e75035c0da08e6471f86a610e290a2b3a
```

The Capsule is compact accepted context, not executable authority.

### Goal Charter

```text
path = docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_charter.md
regular / non-symlink
bytes = 20025
SHA-256 = cfc05c53ef03f890cf5be2228f47369c2042457294384b82db9bd85b8c348dd3
```

The Charter is immutable Owner-delegated authority for this Goal. Controller may not edit or self-expand it.

### Genesis Ledger

```text
path = docs/reports/shadow_pm_p1_process_kpi_bounded_api_local_ledger.md
regular / non-symlink
bytes at manual-bootstrap preparation = 8176
SHA-256 at manual-bootstrap preparation = 041cc2bebaffa6d98216cc21a464c647a1786399015bad8eb0106cf8bf4f4f9e
```

This SHA is entry identity only. The Ledger is intentionally mutable after Goal start; legitimate parent updates must not be rejected because the Genesis SHA later changes.

### Owner Goal Prompt

```text
path = docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_goal_prompt.md
regular / non-symlink
bytes = 11054
SHA-256 = 7f8c3698da2a7112c6e81c35b74d3c3ee07715b5a69be8cf697b723c0db12d6d
```

PM Rules + Charter remain superior authority; Goal Prompt is stable Owner-facing bootstrap text.

## 3. Genesis repository identity

Expected first-start baseline:

```text
branch = main
HEAD = cf4eac54d3f365b0addfaae13f5e7292e3233641
parent = dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
origin/main = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
origin/main...HEAD = 0<TAB>2
cached/staged = empty
tracked dirty = docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
```

Genesis commit is the exact Git publication of the closed predecessor Quality+Trace local MVP:

`feat(p1): publish accepted-fact quality and trace local MVP`

Protected tracked dirty docs must remain external unless future Owner authority explicitly names them. Pre-existing untracked artifacts must not be cleaned/adopted by convenience.

If first-start live branch/HEAD/cached differs, controller performs read-only classification. It may continue only if Charter restart/repository rules make the state unambiguous; otherwise HOLD. Do not rewrite Genesis to match convenience.

## 4. Parent bootstrap recovery

Immediately after Owner starts Goal, parent remains long-lived Shadow Mainline PM and performs:

1. read `docs/thread_handoff/pm_operating_rules.md`;
2. mechanically verify Charter exact identity from Section 2;
3. read this Bootstrap;
4. mechanically verify Capsule identity and read it;
5. read current Ledger; on first start verify Genesis Ledger entry identity;
6. mechanically verify Goal Prompt identity;
7. recover physical cwd, Git root, branch, HEAD, origin/main, left/right, cached/staged and tracked dirty state;
8. confirm predecessor publication commit/candidate is reconstructable from repository;
9. confirm G3 contract path is absent at first start or is a legitimate descendant after restart;
10. confirm final closeout path is absent unless recovering a terminal Goal;
11. preserve all counters/accepted states if this is a restart rather than first start.

Planned first-created G3 contract path:

`docs/contracts/production_process_kpi_contract.md`

Expected first-start prestate: `ABSENT`.

Planned Goal final closeout path:

`docs/reports/p1_process_kpi_bounded_api_local_goal_closeout.md`

Expected first-start prestate: `ABSENT`.

## 5. Capability check — dynamic and small

Unlike the predecessor Goal, no large prepared capability task is materialized at bootstrap. After recovery, parent dynamically creates exactly one compact repository-backed 16-section capability task under PM Rules naming.

Capability task requirements:

- assigned role may be Architecture / Integration for local capability proof;
- A0 control-plane + read-only A4 only;
- exact task output = one capability report;
- no product/test/contract mutation;
- no project-test-runtime pytest;
- no Git mutation;
- no DB/API runtime;
- no Docker/network/SSH/remote/PLC/V-PLC;
- no nested sub-agent;
- no Ledger mutation by child;
- no successor task creation by child;
- minimal required reading: exact task, task-relevant PM Rules, new Charter, Capsule;
- do not read predecessor repair history.

The child must prove only:

```text
SUBAGENT_DELEGATION_AVAILABLE = YES
PARENT_CONTROLLER_RETAINS_CONTEXT = YES
ONE_CHILD_ONE_TASK_SCOPE = YES
CHILD_CANNOT_SELF_ADVANCE = YES
CHILD_DURABLE_REPORT_AVAILABLE = YES
PARENT_CAN_INDEPENDENTLY_INTAKE = YES
PRODUCT_MUTATION = 0
GIT_MUTATION = 0
DB_RUNTIME_ACTION = 0
REMOTE_ACTION = 0
```

Capability check does not consume `TOTAL_DISPATCHED_GATES`.

Before dispatch, parent Ledger transition:

```text
SHADOW_PM_GOAL_STARTED = YES
SHADOW_PM_STOP = NO
GOAL_STATUS = CAPABILITY_CHECK
CAPABILITY_EPOCH = 1 on first start
CAPABILITY_CHECK_ACCEPTED = NO
CURRENT_GATE = CAPABILITY_CHECK
CURRENT_GATE_STATUS = DISPATCH_INTENT_RECORDED
LAST_TASK = <new exact capability task path>
LAST_DURABLE_PHASE = DISPATCH_INTENT_RECORDED
NEXT_ACTION = DISPATCH_CAPABILITY_CHILD
```

## 6. Parent independent capability intake

Child PASS is only candidate evidence. Parent must independently verify:

- task self-identity and task immutability;
- exact sole report identity;
- child changed paths exactly equal task-owned report only;
- cached/staged remains empty;
- protected dirty docs preserved;
- child did not update Ledger or create successor task;
- child used no child agent;
- parent still retains controller context and can perform this intake;
- no product/test/contract/Git/DB/remote action occurred.

If accepted:

```text
GOAL_STATUS = ACTIVE_P1_PROCESS_KPI_BOUNDED_API_LOCAL_AUTONOMY
CAPABILITY_CHECK_ACCEPTED = YES
CURRENT_GATE = P1-G3_PROCESS_KPI_CONTRACT
CURRENT_GATE_STATUS = READY_TO_ISSUE
CURRENT_FAILURE_FAMILY = NONE
TOTAL_DISPATCHED_GATES = 0
PRODUCT_REPAIR_GATES_USED = 0
CONTROL_PLANE_RECOVERY_GATES_USED = 0
NO_PRODUCT_PROGRESS_STREAK = 0
LAST_PM_INTAKE = P1_PROCESS_KPI_CAPABILITY_PARENT_ACCEPTED
LAST_DURABLE_PHASE = PM_INTAKE_ACCEPTED
NEXT_ACTION = GENERATE_EXACT_P1_G3_TASK
```

If delegation/independence is unavailable or capability state is ambiguous, stop with the most specific Charter HOLD. Do not substitute parent self-execution for independent specialist model.

## 7. First real Gate: P1-G3

After capability acceptance, parent generates exactly one fresh repository-backed G3 task assigned to Data Quality.

G3 task purpose:

- freeze additive Process KPI + OEE data-sufficiency semantics;
- prefer exact new contract `docs/contracts/production_process_kpi_contract.md`;
- consume accepted Capsule instead of rerunning G0;
- preserve predecessor `production_metrics_contract.md` unless Owner review is required;
- produce no API implementation;
- define exact G4 contract including scope/window/status/reason and endpoint/DTO semantics;
- preserve no-fallback and no-false-OEE boundaries.

G3 is the first dispatched progress Gate and, after `DISPATCH_INTENT_RECORDED`, increments `TOTAL_DISPATCHED_GATES` to 1.

## 8. G4 and review continuation

After parent accepts G3:

```text
G4-I -> Architecture / Integration
G4-R -> Reliability
G4-DQ -> Data Quality
G4-V -> Verification
```

Each task is generated only after predecessor parent intake. Do not pre-generate future tasks because exact paths/contract identities depend on accepted current state.

G4 implementation exact paths must be the minimum required by accepted G3. Prefer focused new route/test modules and only modify `api/app/main.py` if route registration requires it.

Every review binds exact final candidate identities + exact G3 contract identity.

## 9. Project test runtime authority

This Goal starts with durable Owner-approved local test-runtime authority; no separate one-shot amendment is required.

Control-plane:

```text
/opt/homebrew/opt/python@3.14/bin/python3.14
Python 3.14.6
arm64
resolved bytes = 52448
SHA-256 = b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf
```

Project local validation:

```text
<project-root>/.venv/bin/python
Python 3.13.3
arm64
resolved base = /Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13
base bytes = 119328
base SHA-256 = f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5
pytest = 9.1.1
fastapi = 0.115.6
psycopg = 3.2.3
```

Fresh task verifies runtime identity before use. No install/update/recreate/fallback. Project venv is test execution only; control-plane hashing/parsing/evidence stays on frozen Python 3.14.

## 10. Repair/autonomy behavior

Within Charter scope and budget, ordinary local contract/product/test failures are automatically handled by parent with smallest fresh exact repair task. Do not request Owner permission merely because a local syntax, fixture, assertion or bounded implementation defect appears.

Owner is required only when Charter Section 17 conditions are reached: non-goal authority, source-model expansion, predecessor accepted contract semantic change, architecture/MVP redesign, budget exhaustion, ambiguity/ownership conflict, lost independent delegation or similar hard boundary.

## 11. Budget quick reference

```text
planned progress Gates = 5
MAX_PRODUCT_REPAIR_GATES_PER_GOAL = 3
MAX_CONTROL_PLANE_RECOVERY_GATES_PER_GOAL = 1
MAX_TOTAL_DISPATCHED_GATES = 9
MAX_NORMAL_ATTEMPTS_PER_FAILURE_FAMILY = 2
ABSOLUTE_MAX_ATTEMPTS_PER_FAILURE_FAMILY = 3
```

Two consecutive no-product-progress dispatched Gates trigger mandatory governance-inflation review. A third consecutive no-progress mechanics Gate cannot auto-dispatch.

## 12. Hard stop boundaries

Throughout this Goal:

```text
DB_MIGRATION = 0
HISTORICAL_CONFIG_REGISTRY_IMPLEMENTATION = 0
COLLECTOR_CHANGE = 0
CONFIG_CHANGE = 0
FRONTEND_CHANGE = 0
REMOTE_ACTION = 0
DOCKER_ACTION = 0
PLC_VPLC_ACTION = 0
PRODUCTION_STIMULUS = 0
GIT_MUTATION = 0
P1_G5_EXECUTION = 0
```

Successful local terminal:

```text
GOAL_STATUS = COMPLETE
SHADOW_PM_STOP = YES
GOAL_TERMINAL = PASS / P1_PROCESS_KPI_BOUNDED_API_LOCAL_MVP_AUTONOMOUS_GOAL_COMPLETE
P1_G5_EXECUTION_AUTHORIZED = NO
REMOTE_AUTHORITY_CONSUMED = NO
GIT_MUTATION_AUTHORIZED = NO
NEXT_ACTION = STOP / OWNER_REVIEW_EXACT_GIT_PUBLICATION_THEN_P1_G5
```

After this terminal, do not generate Git publication or P1-G5 tasks. Return control to Owner/Mainline PM.
