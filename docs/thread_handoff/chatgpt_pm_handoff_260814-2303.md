# ChatGPT Mainline PM Handoff — Edge MES Demo — 2026-08-14 23:03 CST

> Handoff objective: transfer Mainline PM control after the VP2-G5 data-path RCA has reached an accepted exact product defect, while the first minimal local repair attempt has terminalized HOLD on a **test-command environment-binding defect**, not on product logic.
>
> Owner direction at handoff: **enter PM Handoff now because the current chat context is too long for safe continued repair iteration**. This handoff is therefore the current task. It does not itself authorize the pending R1 PYTHONPATH-corrected repair successor, Git publication, remote/runtime verification, G5 acceptance, UI continuation, A1-S2, or any independent branch action.

---

## 1. Project identity / outgoing workspace

Project: `Edge MES Demo`

Absolute root:

`/Users/chenjie/Documents/MES/edge-mes-demo`

Current branch at handoff creation:

`main`

Current Git publication baseline:

```text
HEAD = 1d63d2febdb05a8177e2b64acd9850a88d87c255
origin/main = 1d63d2febdb05a8177e2b64acd9850a88d87c255
ahead/behind = 0/0
staged = EMPTY
git diff --check = PASS
git diff --cached --check = PASS
```

Outgoing PM Devspace workspace:

```text
workspaceId = ws_94468c0332
root = /Users/chenjie/Documents/MES/edge-mes-demo
mode = checkout
```

A successor PM should reopen/reuse the same checkout through the available local workspace connector and independently re-establish live facts. Do not assume the workspaceId itself is durable across product sessions.

### Critical current working-tree fact

The repository is **not tracked-clean** at this handoff.

Exactly one tracked file is dirty:

`tests/test_collector_station_event_runtime_source.py`

The diff is authorized work-in-progress from the failed minimal repair attempt:

```text
37 insertions
0 deletions
```

The product source remains unchanged.

Current untracked non-ignored corpus count at handoff creation:

```text
1211
```

This is the long-lived project corpus plus current task/report/handoff artifacts. Preserve it. Do not broad-clean, reset, stash, stage, adopt, or normalize it.

---

## 2. Mandatory successor takeover order

The successor PM's first action must be **strict read-only PM takeover**.

Required order:

1. mechanically verify this handoff path/type/bytes/SHA-256 against the Owner takeover launcher;
2. read this handoff completely to EOF;
3. read `docs/thread_handoff/pm_operating_rules.md` sufficiently to restore current governance requirements;
4. re-establish current physical root, branch, HEAD, origin/main, ahead/behind, staged state, exact tracked dirty paths, and both diff checks;
5. mechanically verify the exact current dirty test file and unchanged product source identities listed below;
6. read the accepted exact-cause Mainline intake;
7. read the failed minimal repair Controller report and its Mainline parent intake;
8. reconcile immutable historical terminals versus current accepted state;
9. stop at Owner decision.

Do **not** automatically start the pending R1 PYTHONPATH-corrected repair successor during takeover.

This handoff transfers context and accepted state. It does not create successor execution authority.

---

## 3. PM Rules / governance authority

Authoritative PM Rules:

`docs/thread_handoff/pm_operating_rules.md`

Current identity:

```text
type = regular / non-symlink
bytes = 69697
SHA-256 = 45d4be226d2c4754fb2b21b55fce6f4086cb24e643b170f1ad1ab475a596bf9f
```

Important rules to restore before dispatching anything:

- Mainline independent intake is mandatory when a Thread returns a governed result. Actually read durable artifacts; do not accept pasted summaries alone.
- `WRITTEN / REVIEWED / ACCEPTED / VERIFIED / STAGED / COMMITTED / PUSHED / DEPLOYED / ACTIVATED / RUNTIME_LOADED / PRODUCTION_ACCEPTED / OWNER_VISUAL_ACCEPTED` are independent states.
- Historical terminals are immutable. A later recovery does not rewrite a prior HOLD.
- Owner authority is explicit, current and scope-bounded. No earlier PASS automatically grants a later phase.
- Goal mode requires Owner manual start. Ordinary Threads/PM must not self-start a Goal.
- New governed core tasks default to unique repository-backed 16-section task files.
- Task self-identity is the first hard gate.
- Exact write allowlists, execution locks, attempt budgets, retry rules and state separation must be explicit.
- Post-lock retry/reconnect/fallback/budget increase is forbidden without fresh authority.
- Out-of-allowlist mutation is a real terminal violation even if later cleaned up.
- Local/static/synthetic evidence must not be promoted into remote/runtime/DB/production evidence.
- Git stage/commit/push/tag each require separate authority and do not imply deployment/runtime state.
- Preserve unrelated dirty/untracked state; no broad cleanup.
- Independent workstream `FIELD-VALIDATION-COLLECTOR-DB` remains isolated unless Owner grants fresh cross-workstream authority.

### Governance Skill v1

Published at current baseline under:

`.agents/skills/edge-mes-pm-governance/`

It is an explicit-only procedural helper and grants **no authority**. Recent R3/cause-isolation/repair tasks did not rely on Skill invocation. Do not infer Skill use from its existence.

---

## 4. Product/UI state entering this handoff

The project remains on the A1 / VP2-G5 data-first path.

Important UI history:

- A1-S1 Trusted Station Summary was accepted as the current UI slice, but Owner visual acceptance for G5 is **NO**.
- Owner observed a usable prototype but not finished product quality.
- Known visual defects included Scope control overlap and layout/overflow issues.
- More importantly, broad query counts showed major cross-station data asymmetry:
  - WS01: 3126 OK / 67 NOK
  - WS02: 8 OK / 0 NOK
  - WS03: 8 OK / 0 NOK
- Those broad counts were initially outside a frozen visual-only authority and therefore were only an RCA trigger, not accepted technical truth.
- Owner explicitly chose **data first, UI later**. shadcn/ui is acceptable later, but UI work is currently deferred.
- `A1-S2 = NOT AUTHORIZED`.

Do not resume shadcn/UI polishing until the data-path repair is completed and separately verified.

---

## 5. Accepted G5 data-path diagnosis — R3

After two broad DB RCA harness failures, Mainline scope-reset to a four-point focus at the exact stall boundary.

Accepted Mainline R3 intake:

`docs/reports/mainline_pm_a1_vp2_g5_cross_station_focus_only_db_rca_r3_parent_independent_intake_20260814T1327Z.md`

Identity:

```text
bytes = 9406
SHA-256 = fe85332451c150b1f26fb338508953cfc757426dff5892710203fd758657ed7a
```

Accepted R3 terminal lineage:

```text
PASS / VP2_G5_CROSS_STATION_FOCUS_ONLY_DB_RCA_R3_SCOPE_RESET
PASS / MAINLINE_PM_ACCEPTS_A1_VP2_G5_CROSS_STATION_FOCUS_ONLY_DB_RCA_R3
```

Accepted classification:

```text
PRIMARY_CLASSIFICATION = C
CLASSIFICATION = ADAPTER_REJECTION_STALL / DOWNSTREAM_STARVATION
DIVERGENCE_BEGINS_AT = COLLECTOR_ADAPTER_GATE_BEFORE_ACCEPTED_STORAGE_AND_ACK
```

Exact control/failure shape:

```text
WS02 / 112921
errors = 0
cycle_count = 1
fact_count = 1
ACK = ACK_OK

WS02 / 112922
ADAPTER_DECISION_NOT_ACCEPTED = 91
disposition = rejected
adapter_error_code = RESULT_COMBINATION_INVALID
cycle_count = 0
fact_count = 0

WS03 / 112921
errors = 0
cycle_count = 1
fact_count = 1
ACK = ACK_OK

WS03 / 112922
ADAPTER_DECISION_NOT_ACCEPTED = 37
disposition = rejected
adapter_error_code = RESULT_COMBINATION_INVALID
cycle_count = 0
fact_count = 0
```

This established that the missing downstream data was not a PostgreSQL post-write loss and not a UI-only problem. The divergence occurred before accepted storage and before ACK.

Historical R1/R2 RCA HOLDs remain immutable:

- R1: Controller package SQL syntax defect (`ORDER BY` output ordinal mismatch).
- R2: multi-statement DB batch timed out; exact timed-out statement not isolated.

Do not rerun broad 48-hour RCA.

---

## 6. Exact product cause — now Mainline accepted

The next investigation isolated the generic `RESULT_COMBINATION_INVALID` down to one exact validator field.

Accepted exact-cause Mainline intake:

`docs/reports/mainline_pm_a1_vp2_g5_adapter_result_combination_invalid_cause_isolation_r2_order_unambiguous_dependency_free_parent_independent_intake_20260814T1438Z.md`

Identity:

```text
bytes = 11015
SHA-256 = 8f5bce19d45e36a7575035e217c11292ac145d60af9c9e9ece634f72d1a176ca
```

Mainline accepted state:

```text
MAINLINE_PM_INDEPENDENT_INTAKE = ACCEPT PASS

EXACT_CAUSE = RESULT_VOCABULARY_NORMALIZATION_MISMATCH
VALIDATION_FIELD = result
VALIDATION_CODE = RESULT_COMBINATION_INVALID
SOURCE_RESULT_CODE = 3
MAPPING_TOKEN = SKIPPED
RUNTIME_NORMALIZED_TOKEN = skipped
CANONICAL_TOKEN = skip

PRODUCT_DEFECT_ESTABLISHED = YES
PRODUCT_DEFECT = COLLECTOR_RUNTIME_SOURCE_RESULT_CANONICALIZATION_DEFECT

MINIMAL_REPAIR_BOUNDARY = RUNTIME_SOURCE_RESULT_CANONICALIZATION_BEFORE_ADAPTER_VALIDATION
PRIMARY_REPAIR_TARGET = collector/app/services/station_event_runtime_source.py::_decode_result

VALIDATOR_CONTRACT_CHANGE_REQUIRED = NO
VPLC_RESULT_CODE_CHANGE_REQUIRED = NO
```

### Exact accepted failure chain

```text
V-PLC result code 3
→ config/mapping.yaml token SKIPPED
→ station_event_runtime_source._decode_result
→ str(decoded).lower()
→ "skipped"
→ canonical station_result validator allows {ok, nok, skip, not_applicable}
→ "skipped" rejected as result:RESULT_COMBINATION_INVALID
→ adapter rejects before accepted storage and ACK
→ downstream station stalls/starves
```

### Exact local cause-isolation controls

The accepted dependency-free helper proved for both WS02 and WS03:

```text
skipped → result:RESULT_COMBINATION_INVALID
skip    → no validation error
ok      → no validation error
```

Therefore this is no longer a hypothesis.

Do not reopen RCA unless a future repair/verification produces contradictory evidence.

---

## 7. Important cause-isolation HOLD history — governance noise vs product truth

Several local cause-isolation iterations HOLDed before the exact cause was accepted. Their terminals remain immutable, but they are **not evidence that the product cause is uncertain**.

### First local cause-isolation HOLD

Terminal:

`HOLD / ADAPTER_CAUSE_ISOLATION_LOCAL_DIAGNOSTIC_FAILED`

Cause:

- helper imported `app.plc.mapping`;
- package init imported `app.plc.decoder`;
- host Python 3.14 lacked `snap7`;
- helper failed before diagnostic frame.

Mainline classification:

`CONTROLLER_PACKAGE_HELPER_DEPENDENCY_SURFACE_DEFECT / ENVIRONMENT_BINDING_OR_CAPABILITY_DENIAL`

Product hypothesis was not disproved.

### R1 dependency-free HOLD

Terminal:

`HOLD / REQUIRED_READING_ORDER_VIOLATION`

Mainline parent classification:

```text
PRIMARY_R1_BLOCKER_CLASS = CONTROLLER_PACKAGE_TASK_ORDER_CONTRACT_DEFECT
DETAIL = SECTION_7_REQUIRED_READING_VS_SECTION_10_SOURCE_PREMISE_ORDER_AMBIGUITY
CONTROLLER_FAIL_CLOSED_RESPONSE = CORRECT
```

The task itself had ambiguous ordering between source identity and source content reads.

### R2 dependency-free PASS

The order contract was rewritten as a single A→I state machine; helper executed once and exact cause was established.

Do not waste successor time re-litigating these historical harness HOLDs.

---

## 8. First minimal repair attempt — current historical HOLD

Owner approved the first minimal repair Gate.

Task:

`docs/thread_handoff/pm_task_20260814T1445Z_a1_vp2_g5_runtime_source_skip_result_canonicalization_minimal_repair.md`

Identity:

```text
bytes = 17206
SHA-256 = 46d11d10ae4b202afa15a9d0c1467bc6d20f04b5afbf1f08585e6aa5edcc3959
```

The task authorized only:

- one product source file;
- one test file;
- one repair report;
- local TDD RED → minimal source change → focused GREEN → bounded regression;
- no SSH/DB/V-PLC/Docker/UI/Git publication.

Controller terminal:

`HOLD / RUNTIME_SOURCE_SKIP_REPAIR_TDD_RED_NOT_BOUND_TO_ACCEPTED_DEFECT`

Controller report:

`docs/reports/mainline_pm_a1_vp2_g5_runtime_source_skip_result_canonicalization_minimal_repair_report.md`

Identity:

```text
bytes = 7249
SHA-256 = 663d482b7ffdc4f36617b69d50f8ad4b85841e891e04f679c8dd8d539db34595
```

What actually happened:

1. Controller correctly added the two authorized regression tests.
2. Source was still untouched.
3. Mandatory TDD RED was run exactly once.
4. pytest exited 4 during collection/import:
   `ModuleNotFoundError: No module named 'app'`.
5. The RED therefore was not bound to `expected skip / actual skipped`.
6. Per frozen task, Controller did not retry and did not modify product source.
7. Green and bounded regression were not run.

Historical HOLD remains immutable.

---

## 9. Mainline intake of failed minimal repair

Latest Mainline repair intake:

`docs/reports/mainline_pm_a1_vp2_g5_runtime_source_skip_result_canonicalization_minimal_repair_parent_independent_intake_20260814T1454Z.md`

Identity:

```text
bytes = 9382
SHA-256 = 956a951d8ac8e4fd0605d1bc478ec1bf77fe10c2c9e47be2b0588fba3ec97fae
```

Accepted Mainline terminal/state:

```text
MAINLINE_PM_INDEPENDENT_INTAKE = ACCEPT HOLD
```

Mainline blocker classification:

```text
PRIMARY_REPAIR_BLOCKER_CLASS = CONTROLLER_PACKAGE_TEST_COMMAND_ENVIRONMENT_BINDING_DEFECT
DETAIL = REQUIRED_PYTEST_COMMAND_OMITTED_PYTHONPATH_COLLECTOR_DOT
CONTROLLER_FAIL_CLOSED_RESPONSE = CORRECT
```

This is a task/harness defect, not a product repair logic failure.

The exact frozen pytest command omitted:

`PYTHONPATH=collector:.`

But this project historically runs the exact runtime-source test with:

```text
PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_station_event_runtime_source.py
```

Repository docs/contracts and historical reports contain multiple examples of the same required binding.

The current correct future command family therefore needs:

```text
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=collector:.
.venv/bin/python -B -m pytest ...
```

Do not install dependencies and do not change Python simply to fix this import error.

---

## 10. Current controlled work-in-progress test diff

Current tracked dirty file:

`tests/test_collector_station_event_runtime_source.py`

Original pre-edit identity before the failed repair attempt:

```text
bytes = 36408
SHA-256 = 5419dcb1e2fb5819e63c9891937cfe96a29becc21bf9be89f7602d0c3aa650d2
```

Current handoff identity after authorized test additions:

```text
bytes = 37617
SHA-256 = afdadc6f7c1fd6e5f3971a108d5a5d2667763bcef653d4a54bed892691cd059f
```

Current exact diff consists of 37 insertions only:

1. import `_decode_result`;
2. add:
   `test_runtime_result_code_table_canonicalizes_skipped_to_skip`;
3. add:
   `test_downstream_skipped_result_builds_canonical_skip_source_payload`, parameterized for WS02 and WS03.

Semantics of first test:

```text
0 → unknown
1 → ok
2 → nok
3 → skip
```

Semantics of second test:

```text
real mapping + real source builder
WS02 result code 3 → payload result == "skip" and != "skipped"
WS03 result code 3 → payload result == "skip" and != "skipped"
```

Mainline intake did **not** establish a test-design defect.

Successor recommendation:

- inherit this exact current test diff as controlled WIP;
- do not delete/recreate it;
- do not reset it;
- verify its identity/diff before granting successor repair execution.

---

## 11. Product source is still completely unrepaired

Current product source:

`collector/app/services/station_event_runtime_source.py`

Current identity:

```text
bytes = 7723
SHA-256 = 4251c44ce8def3acc99f519ff8ae5e10246916b61abe50a4669a04e6daa65bf3
```

It still contains the original logic:

```python
def _decode_result(value, code_tables):
    if value is None:
        return None
    table = code_tables.get("result", {})
    decoded = table.get(value, table.get(str(value), value))
    return str(decoded).lower()
```

Therefore:

```text
SOURCE_REPAIRED_LOCALLY = NO
LOCAL_PRODUCT_REPAIR = NOT PASS
TEST_REGRESSION = NOT ESTABLISHED
```

The intended minimal repair remains semantically equivalent to:

```python
normalized = str(decoded).lower()
return "skip" if normalized == "skipped" else normalized
```

Required behavior to preserve:

```text
None -> None
OK -> ok
NOK -> nok
SKIPPED -> skip
UNKNOWN -> unknown
other fallback values -> existing lowercase behavior, except exact skipped alias
```

Do not change:

- `config/mapping.yaml` business token `SKIPPED`;
- canonical validator vocabulary;
- V-PLC result code 3;
- adapter gate behavior;
- storage/transaction/ACK behavior;
- reserved NOK 30003 semantics.

---

## 12. Local Python / pytest environment binding

Project repair tests should use the project venv, not host Python 3.14.

Bound environment observed before the failed repair:

```text
ENTRYPOINT = .venv/bin/python
Python = 3.13.3
architecture = arm64
pytest = 9.1.1
snap7 import = AVAILABLE
```

Resolved interpreter:

`/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13`

Identity:

```text
type = regular / non-symlink
bytes = 119328
SHA-256 = f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5
```

The previous host Python 3.14 identity remains historical context only. Do not reuse host 3.14 for this repair test path unless a future task explicitly and safely binds its site-packages/import path.

### Missing check in prior repair task

The prior environment capability precheck proved pytest + snap7 availability but did **not** prove that the actual target test module can be collected with the frozen command.

A successor should add a no-pytest or non-budget-consuming bounded import/collection-path capability gate before consuming its single TDD RED, for example by verifying that the selected test import graph resolves under:

`PYTHONPATH=collector:.`

Exact mechanism must be frozen in the new task before execution; do not improvise after lock.

---

## 13. Recommended next technical successor — NOT YET AUTHORIZED

Current recommended next gate:

`OWNER_DECISION_FOR_A1_VP2_G5_RUNTIME_SOURCE_SKIP_RESULT_CANONICALIZATION_MINIMAL_REPAIR_R1_PYTHONPATH_CORRECTED`

At this handoff, this Gate is **not automatically authorized**. The Owner asked for PM Handoff instead of continuing repair iteration.

If the Owner later explicitly approves it, the smallest successor should:

1. mechanically verify the new task, current exact-cause intake and this handoff state;
2. verify current source remains at the unrepaired identity above;
3. verify current test WIP is exactly the accepted 37-line focused diff above and no extra tracked dirty files exist;
4. bind `.venv` and `PYTHONPATH=collector:.` before consuming pytest;
5. perform a bounded import/test-collection capability smoke that does not modify the repo;
6. freeze a new repair execution lock;
7. execute a **fresh** TDD RED using the existing two tests and corrected `PYTHONPATH=collector:.`;
8. require the RED to reach assertions and show the accepted defect (`expected "skip" / actual "skipped"`);
9. only then edit `_decode_result` with the exact minimal canonicalization alias;
10. run one focused GREEN using the same two tests;
11. run one bounded regression covering the full runtime-source test file plus the existing canonical `result="skip"` adapter control;
12. write one new repair report and stop for Mainline independent intake.

Suggested corrected focused command family:

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -B -m pytest -q -p no:cacheprovider \
tests/test_collector_station_event_runtime_source.py::test_runtime_result_code_table_canonicalizes_skipped_to_skip \
tests/test_collector_station_event_runtime_source.py::test_downstream_skipped_result_builds_canonical_skip_source_payload
```

Suggested bounded regression family after source repair:

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -B -m pytest -q -p no:cacheprovider \
tests/test_collector_station_event_runtime_source.py \
tests/test_collector_station_event_adapter.py::test_route_predecessor_mismatch_rejects_system_reserved_detail_without_adapter_synthesis
```

These are handoff recommendations, not executable authority.

---

## 14. Successor repair authority must remain minimal

If Owner approves the successor, recommended write allowlist remains exactly:

```text
1. collector/app/services/station_event_runtime_source.py
2. tests/test_collector_station_event_runtime_source.py
3. one new successor repair report
```

The test file is already dirty from the predecessor and should be treated as inherited authorized WIP, not a clean pre-edit file.

Recommended external/runtime budgets:

```text
NETWORK = 0
SSH = 0
DB_QUERY = 0
DB_WRITE = 0
VPLC_STATE_OR_ACTION = 0
PLC_ACTION = 0
COLLECTOR_RUNTIME_OR_LOG = 0
QUALITY/TRACE/PROCESS_METRICS_API = 0
DOCKER = 0
REMOTE_FS_WRITE = 0
UI_WRITE = 0
```

Recommended Git budgets:

```text
GIT_STAGE = 0
GIT_COMMIT = 0
GIT_PUSH = 0
GIT_TAG = 0
GIT_RESET/STASH/CLEAN/CHECKOUT_MUTATION = 0
```

Do not combine local source repair, Git publication and remote runtime verification into one inferred phase.

---

## 15. State separation at handoff

Current accepted states:

```text
R3_ADAPTER_DIVERGENCE_LAYER = ESTABLISHED / MAINLINE ACCEPTED
EXACT_CAUSE = ESTABLISHED / MAINLINE ACCEPTED
PRODUCT_DEFECT = ESTABLISHED

REGRESSION_TESTS_ADDED = YES / current tracked WIP
SOURCE_REPAIRED_LOCALLY = NO
LOCAL_PRODUCT_REPAIR_PASS = NO
TEST_REGRESSION_PASS = NO

RUNTIME_LOADED = NO / not claimed
REMOTE_VERIFIED = NO / not claimed
PRODUCTION_ACCEPTED = NO / not claimed
G5_ACCEPTED = NO
OWNER_VISUAL_ACCEPTED = NO / unchanged
A1_S2 = NOT AUTHORIZED
UI_REBASE/SHADCN = DEFERRED
```

Do not collapse these states.

A future local repair PASS would still **not** imply remote/runtime/G5 acceptance.

---

## 16. Git / publication state at handoff

Current baseline:

```text
branch = main
HEAD = 1d63d2febdb05a8177e2b64acd9850a88d87c255
origin/main = 1d63d2febdb05a8177e2b64acd9850a88d87c255
ahead/behind = 0/0
staged = EMPTY
tracked dirty = tests/test_collector_station_event_runtime_source.py
git diff --check = PASS
git diff --cached --check = PASS
```

No source repair/test work from the current WIP has been staged, committed or pushed.

The current exact-cause and repair reports/tasks/handoffs are primarily untracked durable evidence in the local repository corpus. Do not mistake `WRITTEN` for `COMMITTED` or `PUSHED`.

Git publication must be separately authorized after a local repair is independently accepted.

---

## 17. Remote/runtime state — do not infer from local repair work

No remote action occurred in the cause-isolation R2 or failed minimal repair.

The failed repair counters included:

```text
NETWORK = 0
SSH = 0
DB_QUERY = 0
DB_WRITE = 0
VPLC_ACTION = 0
COLLECTOR_RUNTIME = 0
DOCKER = 0
```

Therefore no statement can currently be made that a repair is loaded on Raspberry Pi or active in production.

If local repair eventually passes, a later fresh Owner Gate will still be required for:

- code publication if desired;
- controlled remote deployment/activation;
- runtime verification that skip cycles are accepted/ACKed and WS02/WS03 progress resumes;
- any production acceptance/G5 acceptance decision.

Do not pre-authorize those steps in the repair task.

---

## 18. Expected future runtime verification shape after local repair — planning context only

Once a local repair has been independently accepted and separately published/deployed, the highest-value runtime proof should target the exact established defect boundary rather than another broad 48-hour scan.

A good future runtime verification should prove a new downstream skip/bypass cycle has:

```text
source result code = 3
canonical result = skip
adapter accepted
cycle persisted
accepted fact persisted
ACK/read_done progression occurs
next cycle progresses
```

and should confirm both WS02 and WS03 no longer remain stuck on an adapter-rejected `RESULT_COMBINATION_INVALID` boundary.

This section is only planning context. No runtime authority exists at handoff.

---

## 19. Independent FIELD workstream isolation

Independent branch/workstream:

`FIELD-VALIDATION-COLLECTOR-DB`

Its responsibility is real-device Collector + PostgreSQL field validation.

It remains independent from Mainline VP2-G5 unless Owner grants fresh cross-workstream authority.

Do not:

- absorb its state;
- stage its files;
- use its runtime actions as Mainline evidence;
- allow it to mutate Mainline repair paths merely because both workstreams share the same repository directory.

If the successor detects foreign dirty files beyond the exact current Mainline test WIP, stop and classify before mutation.

---

## 20. Key durable artifact ledger for successor intake

### PM Rules

`docs/thread_handoff/pm_operating_rules.md`

```text
69697
45d4be226d2c4754fb2b21b55fce6f4086cb24e643b170f1ad1ab475a596bf9f
```

### Accepted R3 focus-only RCA Mainline intake

`docs/reports/mainline_pm_a1_vp2_g5_cross_station_focus_only_db_rca_r3_parent_independent_intake_20260814T1327Z.md`

```text
9406
fe85332451c150b1f26fb338508953cfc757426dff5892710203fd758657ed7a
```

### Accepted exact-cause R2 Mainline intake

`docs/reports/mainline_pm_a1_vp2_g5_adapter_result_combination_invalid_cause_isolation_r2_order_unambiguous_dependency_free_parent_independent_intake_20260814T1438Z.md`

```text
11015
8f5bce19d45e36a7575035e217c11292ac145d60af9c9e9ece634f72d1a176ca
```

### Failed first minimal repair task

`docs/thread_handoff/pm_task_20260814T1445Z_a1_vp2_g5_runtime_source_skip_result_canonicalization_minimal_repair.md`

```text
17206
46d11d10ae4b202afa15a9d0c1467bc6d20f04b5afbf1f08585e6aa5edcc3959
```

### Failed first minimal repair Controller report

`docs/reports/mainline_pm_a1_vp2_g5_runtime_source_skip_result_canonicalization_minimal_repair_report.md`

```text
7249
663d482b7ffdc4f36617b69d50f8ad4b85841e891e04f679c8dd8d539db34595
```

### Mainline intake of failed first repair

`docs/reports/mainline_pm_a1_vp2_g5_runtime_source_skip_result_canonicalization_minimal_repair_parent_independent_intake_20260814T1454Z.md`

```text
9382
956a951d8ac8e4fd0605d1bc478ec1bf77fe10c2c9e47be2b0588fba3ec97fae
```

### Current unrepaired product source

`collector/app/services/station_event_runtime_source.py`

```text
7723
4251c44ce8def3acc99f519ff8ae5e10246916b61abe50a4669a04e6daa65bf3
```

### Current controlled dirty test file

`tests/test_collector_station_event_runtime_source.py`

```text
37617
afdadc6f7c1fd6e5f3971a108d5a5d2667763bcef653d4a54bed892691cd059f
```

Successor must independently remeasure these before relying on them if current live state differs from this handoff.

---

## 21. What the successor must NOT do on takeover

Until fresh Owner authority after takeover, do not:

- execute the pending repair tests;
- edit product source;
- edit the current dirty test file;
- reset or clean the current test diff;
- create a successor task automatically;
- invoke Goal mode;
- stage/commit/push/tag;
- SSH to Raspberry Pi;
- access PostgreSQL, API, V-PLC or Collector runtime;
- restart Docker/services;
- resume UI/shadcn work;
- authorize A1-S2;
- merge or consume FIELD branch state.

The successor PM should finish read-only takeover, report the accepted current state, and wait for Owner direction.

---

## 22. Highest-priority successor decision after takeover

If the Owner asks what should happen next, the outgoing PM recommendation is:

`approve a fresh R1 PYTHONPATH-corrected minimal repair successor`

Reason:

- exact product defect is already established;
- regression tests are already written and scope-appropriate;
- source remains pristine/unrepaired;
- only blocker was the frozen pytest command omitting the repository's required `PYTHONPATH=collector:.` binding;
- another RCA round would not materially advance the MVP.

The successor task should explicitly treat the inherited test diff as an allowed current prestate and should freeze the corrected environment before consuming its one TDD RED.

Again: this is a recommendation, not inherited authority.

---

## 23. Final handoff state

```text
MAINLINE_PM_HANDOFF = READY
PROJECT_ROOT = /Users/chenjie/Documents/MES/edge-mes-demo
BRANCH = main
HEAD = origin/main = 1d63d2febdb05a8177e2b64acd9850a88d87c255
AHEAD_BEHIND = 0/0
STAGED = EMPTY
TRACKED_DIRTY = tests/test_collector_station_event_runtime_source.py
UNTRACKED_NON_IGNORED = 1212 / includes this handoff file
DIFF_CHECKS = PASS

R3_ADAPTER_BOUNDARY = ACCEPTED
EXACT_CAUSE = ACCEPTED
PRODUCT_DEFECT = ESTABLISHED
CURRENT_TEST_WIP = AUTHORIZED / NOT VERIFIED GREEN
PRODUCT_SOURCE_REPAIR = NOT PERFORMED
LOCAL_REPAIR_PASS = NO
REMOTE_RUNTIME_REPAIR = NO
G5_ACCEPTED = NO
A1_S2 = NOT AUTHORIZED

PENDING_RECOMMENDATION = R1 PYTHONPATH-corrected minimal repair successor
PENDING_REPAIR_AUTHORITY = NOT GRANTED BY THIS HANDOFF
```

The outgoing PM stops here. No further task is dispatched from this handoff window.
