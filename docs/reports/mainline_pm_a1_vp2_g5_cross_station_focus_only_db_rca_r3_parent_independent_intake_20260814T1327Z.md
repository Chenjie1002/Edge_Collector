# Mainline PM Independent Intake — A1 VP2-G5 Cross-Station Focus-Only DB RCA R3 Scope Reset

## 1. Intake terminal

```text
MAINLINE_PM_INDEPENDENT_INTAKE = ACCEPT PASS
R3_TERMINAL = PASS / VP2_G5_CROSS_STATION_FOCUS_ONLY_DB_RCA_R3_SCOPE_RESET
PRIMARY_CLASSIFICATION = C / ADAPTER_REJECTION_STALL / DOWNSTREAM_STARVATION
DIVERGENCE_BEGINS_AT = COLLECTOR_ADAPTER_GATE_BEFORE_ACCEPTED_STORAGE_AND_ACK
R3_DIAGNOSTIC_ACCEPTED = YES
PRODUCT_REPAIR_ACCEPTED = NO
G5_ACCEPTED = NO
OWNER_VISUAL_ACCEPTED = NO / unchanged
A1_S2 = NOT AUTHORIZED
```

Mainline accepts the R3 diagnostic PASS and its classification. The focus-only scope reset successfully established the earliest supported divergence for WS02/WS03 cycle 112922 without broad 48-hour scans, V-PLC/log/API rereads, mutation, retry or fallback.

## 2. Mechanically verified durable identities

Controller report:

```text
PATH = docs/reports/mainline_pm_a1_vp2_g5_cross_station_focus_only_db_rca_r3_scope_reset_report.md
TYPE = regular / non-symlink
BYTES = 10852
SHA-256 = 2d9601773049817caa763680962771ef1ae4d82ec68a88655e14d55466f8369b
```

Owner terminal result:

```text
PATH = docs/reports/mainline_pm_a1_vp2_g5_cross_station_focus_only_db_rca_r3_scope_reset_owner_terminal_result.txt
TYPE = regular / non-symlink
BYTES = 958
SHA-256 = 55b134dfc74fbf61606341cd3d94e53f0a2c3dd74b82fc8701aae80bb06bdbea
```

Owner observation:

```text
PATH = docs/reports/mainline_pm_a1_vp2_g5_cross_station_focus_only_db_rca_r3_scope_reset_observation.txt
TYPE = regular / non-symlink
BYTES = 2647
SHA-256 = 9d0bebd5e2e777677c3d850804fd94a2cba208cf61b8643c9e891b4d21e87586
```

Frozen R3 task:

```text
PATH = docs/thread_handoff/pm_task_20260814T1250Z_a1_vp2_g5_cross_station_focus_only_db_rca_r3_scope_reset.md
TYPE = regular / non-symlink
BYTES = 18123
SHA-256 = a16ce9b910f576067d53132af3cae4a64b4f83010dcbab40e808ef156641035b
```

Frozen Owner runner:

```text
PATH = docs/thread_handoff/mainline_pm_a1_vp2_g5_cross_station_focus_only_db_rca_r3_scope_reset_owner_terminal_runner.zsh
TYPE = regular / non-symlink
BYTES = 19119
SHA-256 = dadecadfce999f1b4f869ccb5eea941254019f831818b3d049bf04a99cb41365
```

The result's declared observation bytes/SHA match the independently measured observation identity.

## 3. Owner runner and execution contract accepted

The exact all-terminal result establishes:

```text
RUNNER_TERMINAL = PASS / RCA_R3_FOCUS_ONLY_DB_OWNER_RUNNER
FAILURE_PHASE = NONE
FAILURE_CODE = NONE
SSH_STARTED = 1
SSH_EXIT_CODE = 0
REMOTE_FRAME_BEGIN_SEEN = 1
REMOTE_FRAME_END_SEEN = 1
POSTGRES_EXEC_STARTED = 1
POSTGRES_EXEC_SUCCEEDED = 1
POSTGRES_EXIT_CODE = 0
DB_ERROR_SUMMARY = NONE
OBSERVATION_WRITTEN = 1
SQL_STATEMENT_COUNT = 1
```

The scope-reset budget is respected:

```text
OWNER_RUNNER_INVOCATION = 1
SSH_PARENT = 1
POSTGRES_EXEC = 1 successful read-only statement
VPLC_STATE_GET = 0
VPLC_LOG_READ = 0
COLLECTOR_LOG_READ = 0
QUALITY_GET = 0
TRACE_GET = 0
PROCESS_METRICS_GET = 0
DB_WRITE = 0
VPLC_ACTION = 0
PLC_WRITE = 0
PRODUCTION_STIMULUS = 0
DOCKER_LIFECYCLE = 0
REMOTE_FS_WRITE = 0
PRODUCT_WRITE = 0
UI_WRITE = 0
GIT_MUTATION = 0
RETRY = 0
RECONNECT = 0
FALLBACK = 0
SECOND_SSH = 0
SECOND_RUNNER = 0
SUB_AGENT = 0
```

## 4. Four-row focus evidence

The observation contains exactly four FOCUS rows under the exact 95-second focus window:

```text
FOCUS_WINDOW = [2026-08-11T04:14:45Z, 2026-08-11T04:16:20Z)
FOCUS = WS02/112921, WS02/112922, WS03/112921, WS03/112922
RCA_FOCUS_ROW_COUNT = 4
```

Mechanically parsed evidence:

```text
WS02 / 112921
  error_count = 0
  cycle_count = 1
  cycle_result = OK
  ack_status = ACK_OK
  fact_count = 1
  fact_result = ok
  config_version = 2026.06.26-slice-a

WS02 / 112922
  error_count = 91
  error_type = ADAPTER_DECISION_NOT_ACCEPTED
  adapter_disposition = rejected
  adapter_error_code = RESULT_COMBINATION_INVALID
  cycle_count = 0
  fact_count = 0
  runtime_last_cycle_counter = 112922
  runtime_collector_state = ADAPTER_REJECTED
  runtime_last_error_code = ADAPTER_DECISION_NOT_ACCEPTED

WS03 / 112921
  error_count = 0
  cycle_count = 1
  cycle_result = OK
  ack_status = ACK_OK
  fact_count = 1
  fact_result = ok
  config_version = 2026.06.26-slice-a

WS03 / 112922
  error_count = 37
  error_type = ADAPTER_DECISION_NOT_ACCEPTED
  adapter_disposition = rejected
  adapter_error_code = RESULT_COMBINATION_INVALID
  cycle_count = 0
  fact_count = 0
  runtime_last_cycle_counter = 112922
  runtime_collector_state = ADAPTER_REJECTED
  runtime_last_error_code = ADAPTER_DECISION_NOT_ACCEPTED
```

The preceding 112921 controls demonstrate that the same two stations immediately before the failure could pass accepted cycle/fact storage and ACK. The next focus cycle 112922 fails before both persisted cycle and accepted production fact creation.

## 5. Classification acceptance

The R3 task's Section 13 classification C requires focus adapter-rejection evidence with disposition/error code, `cycle_count = 0`, `fact_count = 0`, and directionally consistent runtime/error state.

Both WS02/112922 and WS03/112922 satisfy this matrix exactly. Mainline therefore accepts:

```text
PRIMARY_CLASSIFICATION = C
CLASSIFICATION = ADAPTER_REJECTION_STALL / DOWNSTREAM_STARVATION
DIVERGENCE_BEGINS_AT = COLLECTOR_ADAPTER_GATE_BEFORE_ACCEPTED_STORAGE_AND_ACK
```

Alternative classifications are not supported:

- A: rejected because no 112922 accepted cycle/fact storage exists before an ACK failure;
- B: no focus read/decode failure is present;
- D: no `STORAGE_WRITE_FAILED` or equivalent storage-transaction evidence exists;
- E: no unexplained cycle/fact persistence mismatch exists;
- F: the four-row evidence is complete and internally consistent.

This establishes an adapter-gate data-path defect boundary. It does not establish the exact validation field or source-level repair yet.

## 6. Exact repair-cause boundary remains one step narrower than the R3 classification

Local read-only source inspection after accepting the R3 evidence confirms that `collector/app/services/station_event_adapter.py` returns only the first stateless validation error code as `final_error_code`. `RESULT_COMBINATION_INVALID` is a shared validation code used by multiple field/combination checks in `common/station_event/validation.py`, including basic required-string/type checks, event/cycle identity combinations, timestamps, result value checks and other combinations.

The R3 durable observation therefore establishes the adapter gate but does not durably identify which validation field produced `RESULT_COMBINATION_INVALID` for WS02/WS03 cycle 112922.

Static V-PLC source context shows downstream bypass cycles intentionally use a skipped result path (`RESULT_SKIPPED`, `PROCESS_SKIPPED`, `SKIP_UPSTREAM_NOK`), making skip-related runtime normalization a high-value hypothesis. However Mainline does not promote that hypothesis into the repair cause without exact field-level reproduction/isolation.

Accordingly, direct broadening of validation semantics or blindly allowing `skip` is not yet authorized or recommended.

## 7. Git and state continuity

At Mainline intake:

```text
BRANCH = main
HEAD = 1d63d2febdb05a8177e2b64acd9850a88d87c255
ORIGIN_MAIN = 1d63d2febdb05a8177e2b64acd9850a88d87c255
AHEAD_BEHIND = 0/0
STAGED = EMPTY
TRACKED_DIRTY = EMPTY
GIT_DIFF_CHECK = PASS
GIT_DIFF_CACHED_CHECK = PASS
```

The pre-existing untracked corpus remains preserved. This intake creates only this exact Mainline report and does not stage, commit, push, clean, reset or adopt unrelated paths.

## 8. State separation

```text
R1_HISTORICAL_HOLD = IMMUTABLE
R2_HISTORICAL_HOLD = IMMUTABLE
R3_DIAGNOSTIC_PASS = MAINLINE ACCEPTED
ADAPTER_GATE_DEFECT_BOUNDARY = ESTABLISHED
EXACT_VALIDATION_FIELD_CAUSE = NOT YET ESTABLISHED
REPAIR_PASS = NO
PRODUCT_REPAIRED = NO
PRODUCTION_ACCEPTED = NOT CLAIMED
G5_ACCEPTED = NO
OWNER_VISUAL_ACCEPTED = NO
UI_REBASE = DEFERRED
SHADCN_UI_DIRECTION = RETAINED / NOT IMPLEMENTATION AUTHORITY
A1_S2 = NOT AUTHORIZED
```

## 9. MVP alignment and proportional next action

```text
MVP_PATH = MVP-ALIGNED
DATA_FIRST_PRIORITY = PRESERVED
```

The broad data-completeness question is no longer unresolved: the immediate downstream stall begins at the Collector adapter gate on cycle 112922. The smallest remaining data action is not another broad runtime RCA. It is an exact adapter-validation cause isolation focused on the rejected 112922 shape, followed—only if the exact field/combination is proven—by a minimal repair and bounded revalidation.

Recommended next authority shape:

```text
A1-VP2-G5-ADAPTER-RESULT-COMBINATION-INVALID-CAUSE-ISOLATION

local/source-first + exact focus evidence
no broad DB scan
no UI
no production stimulus
no product mutation during isolation phase
```

The isolation should determine the exact validation error path/field behind `RESULT_COMBINATION_INVALID` for the downstream skipped/bypass payload shape and identify whether the defect belongs to runtime source normalization, adapter event construction, shared validation semantics, or V-PLC payload semantics. Only after that evidence should Mainline authorize a repair successor.

## 10. Sole next gate

```text
NEXT_GATE = OWNER_DECISION_FOR_A1_VP2_G5_ADAPTER_RESULT_COMBINATION_INVALID_CAUSE_ISOLATION
```

No repair, UI rebase, shadcn/ui implementation, Git publication, runtime action, visual acceptance retry or A1-S2 authority is inherited from this intake.
