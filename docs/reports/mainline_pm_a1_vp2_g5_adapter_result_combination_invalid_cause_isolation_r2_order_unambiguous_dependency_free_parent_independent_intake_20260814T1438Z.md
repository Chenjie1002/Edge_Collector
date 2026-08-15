# Mainline PM Independent Intake — A1 VP2-G5 Adapter RESULT_COMBINATION_INVALID Cause Isolation R2 Order-Unambiguous Dependency-Free

## 1. Intake terminal

```text
MAINLINE_PM_INDEPENDENT_INTAKE = ACCEPT PASS
R2_TERMINAL = PASS / VP2_G5_ADAPTER_RESULT_COMBINATION_INVALID_CAUSE_ISOLATION_R2_ORDER_UNAMBIGUOUS_DEPENDENCY_FREE
R2_CAUSE_ISOLATION_PASS = YES
EXACT_CAUSE_ESTABLISHED = YES
PRODUCT_DEFECT_ESTABLISHED = YES / COLLECTOR_RUNTIME_SOURCE_RESULT_CANONICALIZATION_DEFECT
REPAIR_AUTHORITY = NO
```

Mainline independently accepts the R2 diagnostic PASS. The R2 report identity, task identity, unchanged dependency-free helper identity, predecessor intake identity, Git continuity, A→I order ledger, one-shot helper execution counters, and exact stdout marker frame are internally consistent and match the frozen package.

This intake establishes the exact cause and repair boundary. It does not perform or authorize the repair, tests, runtime action, DB/API access, deployment, Git publication, G5 acceptance, visual acceptance, or A1-S2.

## 2. Mechanically verified identities

R2 Controller report:

```text
PATH = docs/reports/mainline_pm_a1_vp2_g5_adapter_result_combination_invalid_cause_isolation_r2_order_unambiguous_dependency_free_report.md
TYPE = regular / non-symlink
BYTES = 13502
SHA-256 = 839c17995b9295e7cb60c90b8bcc7c842a836e6160d93b627e0898b3b68a41c6
```

R2 task:

```text
PATH = docs/thread_handoff/pm_task_20260814T1420Z_a1_vp2_g5_adapter_result_combination_invalid_cause_isolation_r2_order_unambiguous_dependency_free.md
TYPE = regular / non-symlink
BYTES = 19291
SHA-256 = 59b47245adb4846157926f55ae33edb1f0aafcf2dd3b38ea186d1b6031bd54c0
```

Frozen dependency-free helper, unchanged from R1:

```text
PATH = docs/thread_handoff/mainline_pm_a1_vp2_g5_adapter_result_combination_invalid_cause_isolation_r1_dependency_free_local_runner.py
TYPE = regular / non-symlink
BYTES = 5709
SHA-256 = 280d8328d4219ab2b46030a181dc5cda244437bc97add629f9c2862b05de73b6
```

Accepted R1 parent intake:

```text
PATH = docs/reports/mainline_pm_a1_vp2_g5_adapter_result_combination_invalid_cause_isolation_r1_dependency_free_parent_independent_intake_20260814T1412Z.md
TYPE = regular / non-symlink
BYTES = 8123
SHA-256 = 0a46526fc4d6521e8cac21e4e5a99f496e422c872edcbe1175472538c375a253
```

All identities match the R2 package ledger.

## 3. A→I order contract acceptance

The R2 report establishes the corrected single authoritative state machine:

```text
A TASK_SELF_IDENTITY = PASS
B PM_RULES_PREDECESSOR_INTAKE_HOLD_REPORT = PASS / READ IN REQUIRED ORDER
C FROZEN_SOURCE_IDENTITY_GATES = PASS / IDENTITY ONLY
C_SOURCE_CONTENT_READ = 0
D_ROOT_GIT_BASELINE_REPORT_PRESTATE = PASS
E_HELPER_PYTHON_IDENTITY = PASS
E_HELPER_AST_PARSE_PRECHECK = PASS / EXACTLY 1
E_DEPENDENCY_SURFACE_STATIC_GATE = PASS
F_SOURCE_PREMISE_READS = PASS / FIRST SOURCE CONTENT READ
G_CAUSE_ISOLATION_R2_EXECUTION_LOCK = FROZEN
H_LOCAL_DIAGNOSTIC_HELPER = PASS / EXACTLY 1 / EXIT 0
I_MARKER_VALIDATION_REPORT_READBACK_FINAL_GIT = PASS
ORDER_A_TO_I = PASS
```

The previous R1 task-order ambiguity is therefore closed for this successor. Source identity was separated from source-content authority as required; no compensating reread or order repair occurred after execution.

## 4. Accepted frozen source premises

Mainline independently rechecked the relevant current source boundary and the R2 report's frozen source identities. The accepted premise chain is:

```text
config/mapping.yaml result code 3 = SKIPPED
collector runtime source _decode_result:
  decoded = table.get(value, table.get(str(value), value))
  return str(decoded).lower()
canonical station_result vocabulary = ok / nok / skip / not_applicable
canonical station_result vocabulary excludes skipped
adapter stateless validation failure surfaces stateless.errors[0].code
```

Therefore the static candidate chain is:

```text
producer result code 3
→ mapping token SKIPPED
→ runtime source token skipped
→ canonical station_result expects skip
→ result / RESULT_COMBINATION_INVALID
```

This static chain is not the sole basis for acceptance; the R2 helper controls below deterministically reproduce it.

## 5. Accepted helper execution and exact controls

The R2 report durably records exactly one helper invocation after the execution lock:

```text
HELPER_EXIT = 0
LOCAL_DIAGNOSTIC_HELPER_INVOCATIONS = 1
POST_LOCK_PYTHON_PROCESSES = 1
RETRY = 0
FALLBACK = 0
SECOND_HELPER = 0
```

The frozen helper emitted the required frame:

```text
MAPPING_RESULT_CODE_3=SKIPPED
RUNTIME_DECODED_RESULT_3=skipped
RUNTIME_DECODED_RESULT_1=ok

WS02_SKIPPED_ERRORS=result:RESULT_COMBINATION_INVALID
WS02_SKIP_CONTROL_ERRORS=NONE
WS02_OK_CONTROL_ERRORS=NONE

WS03_SKIPPED_ERRORS=result:RESULT_COMBINATION_INVALID
WS03_SKIP_CONTROL_ERRORS=NONE
WS03_OK_CONTROL_ERRORS=NONE

EXACT_CAUSE=RESULT_VOCABULARY_NORMALIZATION_MISMATCH
VALIDATION_FIELD=result
VALIDATION_CODE=RESULT_COMBINATION_INVALID
PRODUCER_CODE=3
MAPPING_TOKEN=SKIPPED
RUNTIME_TOKEN=skipped
CANONICAL_TOKEN=skip
VALIDATOR_CONTRACT_CHANGE_REQUIRED=NO
VPLC_RESULT_CODE_CHANGE_REQUIRED=NO
PRIMARY_REPAIR_TARGET=collector/app/services/station_event_runtime_source.py::_decode_result
CAUSE_ISOLATION_R1_PASS=YES
```

The helper marker retains `R1` naming because the helper was intentionally reused unchanged. R2 acceptance derives from the R2 order-compliance ledger plus this frozen helper output.

The important discriminator is the paired control: for both WS02 and WS03, the only validation error on the candidate is `result:RESULT_COMBINATION_INVALID`; replacing only the result token `skipped` with canonical `skip` removes the error, and the `ok` control also remains valid. No additional validation error is present.

## 6. Exact cause and product defect classification

Mainline accepts:

```text
EXACT_CAUSE = RESULT_VOCABULARY_NORMALIZATION_MISMATCH
VALIDATION_FIELD = result
VALIDATION_CODE = RESULT_COMBINATION_INVALID
SOURCE_RESULT_CODE = 3
MAPPING_TOKEN = SKIPPED
RUNTIME_NORMALIZED_TOKEN = skipped
CANONICAL_TOKEN = skip
```

Combined with the previously accepted R3 runtime/data diagnosis:

```text
PRIMARY_CLASSIFICATION = C — ADAPTER_REJECTION_STALL / DOWNSTREAM_STARVATION
DIVERGENCE_BEGINS_AT = COLLECTOR_ADAPTER_GATE_BEFORE_ACCEPTED_STORAGE_AND_ACK
```

Mainline now establishes the concrete product defect:

```text
PRODUCT_DEFECT = COLLECTOR_RUNTIME_SOURCE_RESULT_CANONICALIZATION_DEFECT
DEFECT_MECHANISM = result code 3 maps to SKIPPED, generic lowercasing emits skipped, canonical station_result contract requires skip
FAILURE_EFFECT = adapter rejects focus cycle before accepted cycle/fact storage and ACK path
```

The accepted boundary does not support changing the canonical validator contract or V-PLC result code:

```text
VALIDATOR_CONTRACT_CHANGE_REQUIRED = NO
VPLC_RESULT_CODE_CHANGE_REQUIRED = NO
MAPPING_BUSINESS_TOKEN_CHANGE_REQUIRED = NO REPAIR NEED ESTABLISHED
```

## 7. Minimal repair boundary

Mainline accepts the smallest repair boundary:

```text
MINIMAL_REPAIR_BOUNDARY = RUNTIME_SOURCE_RESULT_CANONICALIZATION_BEFORE_ADAPTER_VALIDATION
PRIMARY_REPAIR_TARGET = collector/app/services/station_event_runtime_source.py::_decode_result
```

The repair should be narrowly semantic: after table lookup and normalization, canonicalize the specific mapping/business token `skipped` to the station-event canonical token `skip`. It should not broaden accepted result vocabulary, alter mapping code 3, alter V-PLC result code 3, or change unrelated unknown/NOK/OK semantics.

Recommended implementation shape, not yet authority:

```text
decoded token → lower-case token
if token == "skipped": return "skip"
otherwise preserve existing normalized token
```

This keeps the translation responsibility at the runtime-source boundary where external/mapping vocabulary is converted to the canonical station-event contract.

## 8. Minimal regression surface

Independent source/test intake found an existing suitable test surface in:

```text
tests/test_collector_station_event_runtime_source.py
```

It already contains:

```text
result code table: 0 UNKNOWN / 1 OK / 2 NOK / 3 SKIPPED
real mapping source-builder fixtures for WS01 / WS02 / WS03
build_runtime_source_payload coverage
```

The minimum repair verification should therefore add focused assertions without new infrastructure:

1. direct or source-builder regression proving result code `3` becomes canonical `skip`;
2. controls preserving code `1 → ok` and `2 → nok` (and existing `None` behavior if directly testing `_decode_result`);
3. at least WS02 and WS03 source-builder/adapter focused coverage proving code `3` no longer reaches `result:RESULT_COMBINATION_INVALID` and is accepted by the existing adapter path;
4. focused existing station-event runtime-source and adapter tests only, then a bounded related regression set if required by the task.

No DB-backed, remote, Docker, frontend, or broad product test is required to prove the local repair itself.

## 9. No mutation / state separation

R2 accepted counters:

```text
NETWORK = 0
SSH = 0
DB_QUERY = 0
DB_WRITE = 0
VPLC_STATE_OR_ACTION = 0
PLC_ACTION = 0
COLLECTOR_RUNTIME_OR_LOG = 0
QUALITY_GET = 0
TRACE_GET = 0
PROCESS_METRICS_GET = 0
DOCKER = 0
PRODUCT_WRITE = 0
CONFIG_WRITE = 0
TEST_WRITE = 0
UI_WRITE = 0
REMOTE_FS_WRITE = 0
GIT_MUTATION = 0
PYTEST = 0
DEPENDENCY_INSTALL = 0
RETRY = 0
FALLBACK = 0
SUB_AGENT = 0
```

State separation remains:

```text
R3_DIAGNOSTIC_PASS = IMMUTABLE / MAINLINE ACCEPTED
R2_EXACT_CAUSE_ISOLATION = MAINLINE ACCEPTED
PRODUCT_DEFECT_ESTABLISHED = YES
REPAIR_AUTHORITY = NO
REPAIR_PASS = NO
PRODUCT_REPAIRED = NO
RUNTIME_LOADED = NOT CLAIMED
PRODUCTION_ACCEPTED = NOT CLAIMED
G5_ACCEPTED = NO
OWNER_VISUAL_ACCEPTED = NO / UNCHANGED
A1_S2 = NOT AUTHORIZED
```

## 10. Git continuity

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

The large historical untracked corpus remains preserved. Mainline performed no cleanup, adoption, stage, commit, push, reset, stash, checkout mutation, source edit, test edit, runtime action or external action.

## 11. MVP alignment and next gate

```text
MVP_PATH = MVP-ALIGNED
DATA_FIRST_PRIORITY = PRESERVED
EXACT_CAUSE_DIAGNOSTIC_PHASE = COMPLETE
NEW_PRODUCT_CAPABILITY = NONE
NEW_RUNTIME_TOPOLOGY = NONE
```

The next task should transition from diagnosis to a minimal local repair. It should authorize only the runtime-source canonicalization and focused tests needed to prove the defect is fixed locally. Runtime deployment/remote verification must remain a separate later authority.

Recommended next gate:

`OWNER_DECISION_FOR_A1_VP2_G5_RUNTIME_SOURCE_SKIP_RESULT_CANONICALIZATION_MINIMAL_REPAIR`

No repair, Git publication, deployment, runtime activation, visual acceptance retry, G5 acceptance or A1-S2 authority is inherited from this intake.
