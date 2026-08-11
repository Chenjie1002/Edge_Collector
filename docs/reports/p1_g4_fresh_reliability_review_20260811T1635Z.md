# P1-G4-R Fresh Reliability Review After Bounded Repair

REPORT_NAME = P1_G4_R_FRESH_RELIABILITY_REVIEW_20260811T1635Z
REPORT_PATH = docs/reports/p1_g4_fresh_reliability_review_20260811T1635Z.md
TASK_NAME = P1_G4_R_FRESH_RELIABILITY_REVIEW_20260811T1635Z
TASK_ROLE = Shadow Mainline Reliability reviewer
GOAL_ID = P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1
CURRENT_GATE = P1-G4-R_FOCUSED_RELIABILITY
REVIEW_SCOPE = P1-G4-R_FOCUSED_RELIABILITY / repaired candidate
MVP_PATH = MVP-ALIGNED
TERMINAL_RESULT = PASS
NEXT_GATE = PARENT_INDEPENDENT_FRESH_RELIABILITY_INTAKE

## 1. Task self-identity gate

The exact task authority was read before any other repository read/action.

TASK_PATH = /Users/chenjie/Documents/MES/edge-mes-demo/docs/thread_handoff/pm_task_20260811T1635Z_p1_g4_r_fresh_reliability_review.md
TASK_TYPE = regular non-symlink
TASK_BYTES = 9601
TASK_SHA256 = 8a54fc70bd37f2d28220a962c734a8929b35b17cad404a787ad22ff4325eefad
TASK_NAME = P1_G4_R_FRESH_RELIABILITY_REVIEW_20260811T1635Z
TASK_ROLE = Shadow Mainline Reliability reviewer
TASK_SCOPE = P1-G4-R_FOCUSED_RELIABILITY / repaired candidate
TASK_SELF_IDENTITY = PASS

The task file is the sole authority. This review is local-only and does not
authorize runtime loading, production acceptance, remote/RPi, P1-G5, Git
publication, or any external action.

## 2. Authority identities

All listed authorities were regular files and matched the task-bound paths and
identities. The old G4-R report was used only as causal context; it was not
used as acceptance for the repaired bytes.

| authority | bytes | SHA-256 |
| --- | ---: | --- |
| docs/thread_handoff/pm_operating_rules.md | 69697 | 45d4be226d2c4754fb2b21b55fce6f4086cb24e643b170f1ad1ab475a596bf9f |
| docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_charter.md | 20025 | cfc05c53ef03f890cf5be2228f47369c2042457294384b82db9bd85b8c348dd3 |
| docs/contracts/production_process_kpi_contract.md | 28427 | 776e744314f9ec33884765c20f8d88dab45afeda74354cf7e10e7fc226809252 |
| docs/reports/p1_g4_i_bounded_production_metrics_api_20260811T1525Z.md | 14056 | 32d041fc243041be87ee7d43339237e7fa7a5aa53c0be904ed35a0afedab0482 |
| docs/reports/p1_g4_r_focused_reliability_review_20260811T1555Z.md | 12543 | 11c85624f2ef2d4943434b19bbbeaa5cdbc333fdc7f9eb73a796c0f0936a5c6e |
| docs/reports/p1_g4_repair_accepted_fact_lineage_nok_detail_20260811T1605Z.md | 9073 | e9b07c1b4585302a2aa1291fe7fed28eb8cb4334213d1283755e49420f03d0ba |
| docs/reports/p1_g4_repair_cache_baseline_recovery_20260811T1615Z.md | 11639 | 0c9bfbabf6e14e7baefa13883c58e8c6d81ce3907ea12ba75690a042f50b5aee |

## 3. Candidate and protected identity binding

The exact repaired candidate identities matched Section 4 of the task before
and after the required local checks:

| candidate | bytes | SHA-256 |
| --- | ---: | --- |
| api/app/main.py | 524 | 038f7ea2c900f8288742586fe38430f6f5e0ce352fd1e4d7117d0e467f811dad |
| api/app/routes/process_metrics.py | 19771 | a7313117776e6ba8255bf2f60755bfad5a6bcf510767f0129720f8425984f1cb |
| api/tests/test_process_metrics_api.py | 23821 | 6eb1e0ced1cb745755f94b3719c1a91923ca7f6ffe4d538b21004b2a9432566a |

Protected predecessor identities also remained exact:

| protected artifact | bytes | SHA-256 |
| --- | ---: | --- |
| docs/contracts/production_metrics_contract.md | 8229 | 2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e |
| api/app/routes/quality_trace.py | 9538 | 6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a |
| api/tests/test_quality_trace_api.py | 13296 | bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c |

REPORT_ENTRY_BEFORE_WRITE = ABSENT. No bound candidate or protected file
drifted during review.

## 4. Repaired F1/F2 semantic review

### F1: historical config lineage is fail-closed

The route derives config_window_state at
api/app/routes/process_metrics.py:382-393. An empty/missing tuple is
UNRESOLVED; multiple tuples are MIXED; a single non-null tuple without an
independent historical resolver is also UNRESOLVED. There is no
SINGLE_RESOLVED emission in the repaired route. The unsupported-metric builder
at api/app/routes/process_metrics.py:163-199 keeps ideal CT non-numeric and
uses HISTORICAL_CONFIG_AUTHORITY_MISSING or
MIXED_HISTORICAL_CONFIG_WINDOW; all other config-dependent metrics remain
unsupported/non-numeric. Focused regression cases at
api/tests/test_process_metrics_api.py:502-566 cover mixed and
single-tuple-without-authority behavior.

F1 = PASS.

### F2: NOK detail incompleteness is fail-closed

The accepted-fact SELECT includes all required fields at
api/app/routes/process_metrics.py:345-350:

nok_code, nok_origin, nok_detail_code, nok_detail_source_event_id,
nok_detail_evidence_fact_key

REQUIRED_NOK_DETAIL_FIELDS is bound at
api/app/routes/process_metrics.py:37-43. NULL/blank detection is applied to
every required field for each production_result=nok row at
api/app/routes/process_metrics.py:438-442. A non-empty denominator with
incomplete detail emits quality_rate.status=PARTIAL, reason
QUALITY_NOK_DETAIL_INCOMPLETE, and the contract-permitted numeric rate; a
fully bound accepted NOK remains SUPPORTED at
api/app/routes/process_metrics.py:519-534. Focused cases at
api/tests/test_process_metrics_api.py:272-319 cover both paths.

F2 = PASS.

## 5. Earlier reliability and boundary invariants

The repaired route remains accepted-fact-only and read-only:

- GET /api/v2/process-metrics is the exact route registration, verified by the
  in-memory route assertion and api/app/main.py:1-14.
- SQL selects only production_accepted_station_event_fact, restricts
  event_type='station_result', uses half-open event_ts >= %s and event_ts < %s,
  and orders by event_ts ASC, accepted_at ASC, fact_key ASC at
  api/app/routes/process_metrics.py:340-360.
- BEGIN READ ONLY, bounded statement/idle-in-transaction timeouts, and
  commit/rollback handling are present. No INSERT/UPDATE/DELETE, ACK,
  read_done, legacy/current-YAML/WS03/fallback source, join, migration, or DB
  write path is present in the route. Source metadata fixes fallback to none
  at api/app/routes/process_metrics.py:70-76.
- Fact-key missing, duplicate/conflict, and unknown-result handling occurs
  before counting at api/app/routes/process_metrics.py:395-432 and returns
  unavailable metrics without numeric values.
- The fixed 14-metric matrix omits numeric values for unit count, cycle time,
  ideal CT, line/terminal output, Performance, Availability, and Full OEE.
  Calendar event rate remains explicitly named and is not used as an OEE
  denominator.
- The exact four-query-parameter, exact-once, empty-body, method, strict
  RFC3339/timezone, UTC canonicalization, from < to, and 31-day checks are
  implemented at api/app/routes/process_metrics.py:89-130 and the endpoint
  body boundary at api/app/routes/process_metrics.py:326-333. Invalid
  requests return 422 before SELECT; unsupported methods remain 405.

EARLIER_RELIABILITY_INVARIANTS = PASS

## 6. Required local validation

Execution root:

pwd -P = /Users/chenjie/Documents/MES/edge-mes-demo
git rev-parse --show-toplevel = /Users/chenjie/Documents/MES/edge-mes-demo

Required commands were run exactly with bytecode and pytest cache writes
disabled:

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -m pytest -p no:cacheprovider -q api/tests/test_process_metrics_api.py
RESULT = 34 passed in 0.17s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -m pytest -p no:cacheprovider -q api/tests/test_process_metrics_api.py api/tests/test_quality_trace_api.py
RESULT = 50 passed in 0.19s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -c 'from pathlib import Path; import app.main; files=(Path("api/app/routes/process_metrics.py"),Path("api/tests/test_process_metrics_api.py"),Path("api/app/main.py")); [compile(p.read_text(encoding="utf-8"),str(p),"exec") for p in files]; routes=[(r.path,tuple(sorted(r.methods or ()))) for r in app.main.app.routes if r.path == "/api/v2/process-metrics"]; assert routes == [("/api/v2/process-metrics",("GET",))], routes; print("IN_MEMORY_COMPILE_ROUTE=PASS")'
RESULT = IN_MEMORY_COMPILE_ROUTE=PASS

The tests patch app.db.get_conn with fake connections; no real DB connection
or DB runtime action was made.

## 7. Cache baseline and continuity evidence

The preserved API cache/bytecode snapshot matched the control-plane recovery
baseline before and after the required checks:

API_CACHE_SNAPSHOT_SHA256 = 6f6274909b4746818f1b0b4ab82a66c718a660b708ea2c4135c2cfe50ed67209
INVENTORY_SCOPE = api/.pytest_cache (recursive), api/**/__pycache__, api/**/*.pyc
PRE_INVENTORY_ROWS = 26
POST_INVENTORY_ROWS = 26
PRE_POST_PATH_BYTES_MTIME = MATCH
LATEST_PREEXISTING_MTIME = 2026-07-05T21:16:01+0800
API_CACHE_BASELINE = PRE-EXISTING_AND_UNCHANGED

No cache/bytecode was deleted, normalized, touched, or written by this
review. The snapshot hash above is the task-bound identity; the live 26-entry
path/bytes/mtime projection matched the recovery report's bound snapshot.

Read-only Git/continuity checks before the report write:

git status --short --untracked-files=all = 884 lines
status SHA-256 = 44d308952b0d3cf1ea47daca6cb49a49833878f00ff0ac2cce3b3dbce1324b83
git diff --name-only = api/app/main.py, docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
git ls-files -m = api/app/main.py, docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
git diff --cached --name-only = empty
git diff --check = PASS

The task-owned pre-report status was only:

 M api/app/main.py
?? api/app/routes/process_metrics.py
?? api/tests/test_process_metrics_api.py
report path = absent

The tracked dirty paths and the broader dirty/untracked corpus were
pre-existing continuity and were not cleaned, staged, adopted, or otherwise
modified. The only child-owned write is this exact report path.

## 8. State and action counters

This child establishes only local WRITTEN and REVIEWED; parent intake is
required for Reliability acceptance.

WRITTEN = yes
REVIEWED = yes
ACCEPTED = no
VERIFIED = no
STAGED = no
COMMITTED = no
PUSHED = no
DEPLOYED = no
ACTIVATED = no
RUNTIME_LOADED = no
PRODUCTION_ACCEPTED = no

PRODUCT_REPAIR = 0
CONTROL_PLANE_RECOVERY = 0
DB_RUNTIME_ACTION = 0
REMOTE_ACTION = 0
DOCKER_COMPOSE_ACTION = 0
PLC_VPLC_ACTION = 0
PRODUCTION_STIMULUS = 0
GIT_MUTATION = 0

## 9. Result, MVP path, and parent boundary

PASS is used because all repaired semantics, required local checks,
continuity, cache baseline, and reliability invariants passed. This is
MVP-ALIGNED: the bounded station-scoped read-only Process Metrics API
provides truthful accepted-fact count/rate/Quality output and explicit
unsupported sufficiency states without adding runtime, DB, remote, or
production scope.

The parent must independently read and hash this report and every bound
artifact, verify that the claims bind the repaired candidate identities, and
then decide whether to set RELIABILITY_ACCEPTED=YES. This report does not
authorize Data Quality, Verification, runtime loading, deployment, activation,
production acceptance, Ledger update, P1-G5, or Goal completion.

After parent independent PASS intake only, the parent may generate the exact
P1-G4-DQ focused Data Quality task. This child stops at the stated next gate.
