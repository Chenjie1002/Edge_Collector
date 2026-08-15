# P1-G5 Local Verification Recovery — Mainline PM Intake

Status: `PASS / LOCAL_VERIFICATION_RECOVERY_AUTHORIZED`

Date: 2026-08-12

This report is the Mainline PM durable intake of the terminal P1-G5 Goal:

```text
GOAL_ID = P1-G5-REAL-RUNTIME-DB-API-RECONCILIATION-V1
HISTORICAL_GOAL_TERMINAL = HOLD / DURABLE_EVIDENCE_NOT_ACCESSIBLE
PARENT_RUNTIME_CANDIDATE = PASS / P1_G5_REAL_RUNTIME_RECONCILIATION_CANDIDATE
```

It does not rewrite the historical Goal terminal. It freezes the causal classification and authorizes one fresh local-only Verification recovery task. It grants no Goal, network, SSH, remote, Docker, Compose, HTTP, DB, production-stimulus, PLC/V-PLC or Git-mutation authority.

## 1. Accepted terminal inputs

The following final Goal artifacts are accepted as historical/durable facts for this recovery:

```text
AUTHORITY_CAPSULE = docs/reports/p1_g5_real_runtime_reconciliation_authority_capsule.md
15547 / df9cdc877f0835609ce66e53dc203bf015a6af949746e967e7648bfa19181010

FINAL_PARENT_EVIDENCE = docs/reports/p1_g5_real_runtime_reconciliation_parent_evidence.md
31316 / 13008b77d0cf28ec40d24b35ef1c0ccfe78bbe894a7fc6dd1b728c130fb0ac6e

FAILED_VERIFICATION_REPORT = docs/reports/p1_g5_real_runtime_reconciliation_verification_report.md
4935 / 5afffe704cbac0235b397edc8170d3b3292d171241b1980772e4016ce45008d4

GOAL_CLOSEOUT = docs/reports/p1_g5_real_runtime_reconciliation_goal_closeout.md
5606 / 2e9c5946d3f3452d308bd02cad94139770dc403fac6a6ea025eb5c4e9573a8d8

FINAL_LEDGER = docs/reports/mainline_pm_p1_g5_real_runtime_reconciliation_ledger.md
15022 / d8b36660ddc73ba99420e275369737b6abfa90a587bbf4869d1f00d2a2833967

FAILED_VERIFICATION_TASK = docs/thread_handoff/pm_task_20260812T074908Z_p1_g5_real_runtime_reconciliation_verification.md
6629 / 29d401e0412f48dfefd52ba89594e623de1ff1e9497b2f492c5d0c3c26b2e07d
```

The historical Goal remains stopped and non-reusable. No part of this report authorizes resuming that Goal.

## 2. Mainline PM causal classification

The failed Verification child behaved correctly under its task. The task itself froze a dispatch-time Ledger identity as if it were immutable, while the same controller state machine required the Ledger to change from `VERIFICATION_TASK_PUBLISHED` to `VERIFICATION_DISPATCHED` and to record the child ID/counter before the child read the Ledger.

Therefore the first causal defect is:

```text
ROOT_CAUSE = VERIFICATION_TASK_MUTABLE_LEDGER_IDENTITY_FREEZE
SPECIFIC_DEFECT = DISPATCH_TRANSITION_INVALIDATES_FROZEN_LEDGER_IDENTITY
VERIFICATION_CHILD_BEHAVIOR = CORRECT_FAIL_CLOSED
DURABLE_EVIDENCE_ACTUALLY_MISSING = NO
PARENT_EVIDENCE_ACCESSIBLE = YES
PARENT_EVIDENCE_TECHNICALLY_COMPLETE = YES
LEDGER_DRIFT = EXPECTED_CONTROLLER_MUTATION / NOT_RUNTIME_DRIFT
```

The historical terminal remains:

```text
HISTORICAL_GOAL_TERMINAL = HOLD / DURABLE_EVIDENCE_NOT_ACCESSIBLE
```

It must not be silently edited to PASS.

## 3. Preserved parent technical candidate

The final Parent Evidence durably records all load-bearing technical claims needed for independent local certification:

```text
RUNTIME_BINDING = PASS
REAL_STATION_ANCHOR = PASS
REAL_TRACE_ANCHOR = PASS
STABLE_DB_WINDOWS = PASS
QUALITY_DB_API_RECONCILIATION = PASS
PROCESS_METRICS_DB_API_RECONCILIATION = PASS
TRACE_DB_API_RECONCILIATION = PASS
READ_ONLY_COUNTER_AUDIT = PASS
PARENT_RUNTIME_CANDIDATE = PASS / P1_G5_REAL_RUNTIME_RECONCILIATION_CANDIDATE
```

Key stable-window evidence:

```text
STATION_DB_PRE_SHA256 = 15976c753e13e71f9f12c5261f483d1c713f8c0186b6d1726b2c13912194d63b
STATION_DB_POST_SHA256 = 15976c753e13e71f9f12c5261f483d1c713f8c0186b6d1726b2c13912194d63b
TRACE_DB_PRE_SHA256 = 4a0eb68c5942aeac32bee3ecf7f7fbdd66a1bc2cf696f9a589c51ba9c8c9cec7
TRACE_DB_POST_SHA256 = 4a0eb68c5942aeac32bee3ecf7f7fbdd66a1bc2cf696f9a589c51ba9c8c9cec7
```

The final Parent Evidence also records:

```text
QUALITY_HTTP_STATUS = 200
QUALITY_RECONCILIATION_RESULT = PASS

PROCESS_METRICS_HTTP_STATUS = 200
PROCESS_FIXED_METRIC_SET_EXACT = YES / 14 names / no duplicates
PROCESS_NO_FALSE_NUMERIC_METRICS = YES
PROCESS_RECONCILIATION_RESULT = PASS

TRACE_HTTP_STATUS = 200
TRACE_ITEMS_EXACT_EQUAL = YES / all 22 DTO fields / order preserved
TRACE_RECONCILIATION_RESULT = PASS
```

Read-only counters are durably bounded to one approval/launch/SSH/shell, six read-only psql calls and one GET for each Quality/Trace/Process Metrics endpoint, with retries/reconnects/second external transaction and all forbidden mutation counters at zero.

This recovery must not re-observe or replace those runtime facts.

## 4. Recovery design correction

The fresh recovery task shall use these identity classes:

### AUTHORITY_HARD_GATE

```text
current recovery task file itself
this Mainline PM intake report
final Parent Evidence
Authority Capsule
Goal Closeout
failed Verification Report
failed Verification Task
```

These objects are terminal/final for the historical Goal and are not expected to mutate during the recovery.

### HISTORICAL_OR_SEMANTIC_READ

```text
docs/thread_handoff/pm_operating_rules.md
docs/current_status.md
final Ledger
```

The final Ledger may be read to confirm the terminal/control narrative, but its hash is not a load-bearing runtime-evidence accessibility gate. Its current identity may be recorded diagnostically. A Ledger hash difference alone must not invalidate the final Parent Evidence unless semantic inspection shows that the runtime candidate, counters or terminal history were rewritten inconsistently.

## 5. Authorized recovery

Exactly one fresh normal Codex `Verification` Thread may be manually dispatched by the Owner to perform:

```text
LOCAL_ONLY_INDEPENDENT_VERIFICATION_RECOVERY
```

The Thread may independently verify the already-persisted Parent Evidence against the Authority Capsule and the terminal historical artifacts, then write exactly one report:

```text
docs/reports/p1_g5_local_verification_recovery_report.md
```

The recovery report may conclude:

```text
PASS
PASS WITH RECOMMENDATIONS
HOLD
```

A PASS/PASS WITH RECOMMENDATIONS means the final durable Parent Evidence independently supports the bounded P1-G5 technical candidate under the accepted read-only contract. It does not itself rewrite the historical Goal terminal and does not authorize any successor product/runtime/Git action. Mainline PM must intake the recovery report before deciding the P1-G5 gate.

## 6. Absolute exclusions

```text
GOAL_MODE = NOT AUTHORIZED
NETWORK = 0
SSH = 0
REMOTE = 0
DOCKER = 0
COMPOSE = 0
HTTP = 0
DB = 0
PRODUCTION_STIMULUS = 0
PLC_VPLC = 0
PROJECT_RUNTIME_TESTS = 0
SOURCE_MUTATION = 0
GIT_STAGE_COMMIT_PUSH_TAG = 0
RETRY_RECONNECT_RUNTIME_RESAMPLE = 0
SECOND_VERIFICATION_CHILD = 0
```

No recovery step may change Parent Evidence, the old Verification task/report, Closeout, Ledger, Capsule, PM Rules, current status or source/runtime files.

## 7. Mainline PM terminal for this intake

```text
P1_G5_HISTORICAL_GOAL_TERMINAL = HOLD / DURABLE_EVIDENCE_NOT_ACCESSIBLE
P1_G5_PARENT_TECHNICAL_RESULT = PASS / PRESERVED_CANDIDATE
P1_G5_LOCAL_VERIFICATION_RECOVERY_ELIGIBLE = YES
REMOTE_RECOVERY_REQUIRED = NO
SECOND_EXTERNAL_TRANSACTION_REQUIRED = NO
PRODUCT_DEFECT = NO
NEXT_GATE = OWNER_MANUAL_DISPATCH_OF_EXACT_LOCAL_VERIFICATION_RECOVERY_TASK
```
