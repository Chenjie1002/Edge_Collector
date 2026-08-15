# P1-G4 Repair Cache-Baseline Control-Plane Recovery

## 1. Terminal result and boundary

```text
TERMINAL_RESULT = PASS / CONTROL_PLANE_CACHE_BASELINE_RECONCILED
MVP_PATH = MVP-ALIGNED
GOAL_ID = P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1
CURRENT_GATE = P1-G4-R_FOCUSED_RELIABILITY
PRODUCT_REPAIR_GATES_USED = 1/3
CONTROL_PLANE_RECOVERY_GATES_USED_BEFORE = 0
CONTROL_PLANE_RECOVERY_GATES_USED_AFTER = 1
```

This pass reconciled preserved API cache/bytecode evidence only. It did not
repair, accept, deploy, activate, or reliability-verify the candidate.

## 2. Task and report identity

```text
TASK_PATH = docs/thread_handoff/pm_task_20260811T1615Z_p1_g4_repair_cache_baseline_recovery.md
TASK_NAME = P1_G4_REPAIR_CACHE_BASELINE_RECOVERY_20260811T1615Z
TASK_ROLE = Shadow control-plane evidence recovery reviewer
TASK_CLASS = CONTROL_PLANE_RECOVERY_GATE_1_OF_1
TASK_TYPE = regular non-symlink
TASK_BYTES = 9858
TASK_SHA256 = 0f862442b411710523d909c4be1f23b702fcf3a579dd75fdf7b523189754baee
TASK_SELF_IDENTITY = PASS
REPORT_PATH = docs/reports/p1_g4_repair_cache_baseline_recovery_20260811T1615Z.md
REPORT_ENTRY = ABSENT before the authorized report write
```

The report is the only child-owned output. Its final bytes and SHA-256 are
returned in the terminal manifest after this write.

## 3. Authority identities

All six post-gate inputs were regular non-symlink files and matched the task
bindings. No substitute authority was used.

| artifact | bytes | SHA-256 |
| --- | ---: | --- |
| `docs/thread_handoff/pm_operating_rules.md` | 69697 | `45d4be226d2c4754fb2b21b55fce6f4086cb24e643b170f1ad1ab475a596bf9f` |
| `docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_charter.md` | 20025 | `cfc05c53ef03f890cf5be2228f47369c2042457294384b82db9bd85b8c348dd3` |
| `docs/contracts/production_process_kpi_contract.md` | 28427 | `776e744314f9ec33884765c20f8d88dab45afeda74354cf7e10e7fc226809252` |
| `docs/thread_handoff/pm_task_20260811T1605Z_p1_g4_repair_accepted_fact_lineage_nok_detail.md` | 11473 | `160754b047259ad0e37086ac20b0fc46f6e5a3f17c7c7fbebb4a569f2edcfc11` |
| `docs/reports/p1_g4_repair_accepted_fact_lineage_nok_detail_20260811T1605Z.md` | 9073 | `e9b07c1b4585302a2aa1291fe7fed28eb8cb4334213d1283755e49420f03d0ba` |
| `docs/reports/p1_g4_r_focused_reliability_review_20260811T1555Z.md` | 12543 | `11c85624f2ef2d4943434b19bbbeaa5cdbc333fdc7f9eb73a796c0f0936a5c6e` |

## 4. Candidate and protected identities

The live repaired candidate identities matched the task bindings at the
recovery entry and final audit. No candidate or protected file was written by
this recovery.

| path | bytes | SHA-256 | recovery result |
| --- | ---: | --- | --- |
| `api/app/routes/process_metrics.py` | 19771 | `a7313117776e6ba8255bf2f60755bfad5a6bcf510767f0129720f8425984f1cb` | unchanged |
| `api/tests/test_process_metrics_api.py` | 23821 | `6eb1e0ced1cb745755f94b3719c1a91923ca7f6ffe4d538b21004b2a9432566a` | unchanged |
| `api/app/main.py` | 524 | `038f7ea2c900f8288742586fe38430f6f5e0ce352fd1e4d7117d0e467f811dad` | unchanged/protected |
| `docs/contracts/production_process_kpi_contract.md` | 28427 | `776e744314f9ec33884765c20f8d88dab45afeda74354cf7e10e7fc226809252` | unchanged/protected |
| `docs/contracts/production_metrics_contract.md` | 8229 | `2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e` | unchanged/protected |
| `api/app/routes/quality_trace.py` | 9538 | `6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a` | unchanged/protected |
| `api/tests/test_quality_trace_api.py` | 13296 | `bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c` | unchanged/protected |

## 5. Pre-existing API cache/bytecode reconciliation

```text
REPAIR_TASK_START_UTC = 2026-08-11T16:05:00Z
REPAIR_TASK_START_LOCAL = 2026-08-12T00:05:00+0800
API_CACHE_SNAPSHOT_SHA256 = 6f6274909b4746818f1b0b4ab82a66c718a660b708ea2c4135c2cfe50ed67209
LIVE_SNAPSHOT_COMPARISON = MATCH
INVENTORY_SCOPE = api/.pytest_cache (recursive), api/**/__pycache__, api/**/*.pyc
INVENTORY_ROWS = 26
LATEST_API_ARTIFACT_MTIME = 2026-07-05T21:16:01+0800
API_CACHE_BASELINE = PRE-EXISTING_AND_UNCHANGED
```

The parent-bound full path/bytes/mtime snapshot identity matched the live
read-only inventory. Every observed API cache/bytecode artifact is older than
the repair-task boundary; the latest is `2026-07-05T21:16:01+0800`. Existing
cache presence is reconciled state, not a global cache-free claim.

| path | bytes | mtime |
| --- | ---: | --- |
| `api/.pytest_cache` | 192 | `2026-06-19T22:24:49+0800` |
| `api/.pytest_cache/.gitignore` | 37 | `2026-06-19T22:24:49+0800` |
| `api/.pytest_cache/CACHEDIR.TAG` | 191 | `2026-06-19T22:24:49+0800` |
| `api/.pytest_cache/README.md` | 302 | `2026-06-19T22:24:49+0800` |
| `api/.pytest_cache/v` | 96 | `2026-06-19T22:24:49+0800` |
| `api/.pytest_cache/v/cache` | 96 | `2026-06-19T22:24:49+0800` |
| `api/.pytest_cache/v/cache/nodeids` | 629 | `2026-06-21T20:38:20+0800` |
| `api/app/__pycache__` | 128 | `2026-07-04T09:16:15+0800` |
| `api/app/__pycache__/db.cpython-313.pyc` | 951 | `2026-06-14T13:53:12+0800` |
| `api/app/__pycache__/main.cpython-313.pyc` | 941 | `2026-07-04T09:16:15+0800` |
| `api/app/routes/__pycache__` | 288 | `2026-07-05T13:49:44+0800` |
| `api/app/routes/__pycache__/accepted_station_events.cpython-313.pyc` | 12498 | `2026-07-05T13:49:44+0800` |
| `api/app/routes/__pycache__/events.cpython-313.pyc` | 1162 | `2026-06-14T13:53:12+0800` |
| `api/app/routes/__pycache__/health.cpython-313.pyc` | 865 | `2026-06-14T13:53:12+0800` |
| `api/app/routes/__pycache__/kpi.cpython-313.pyc` | 10183 | `2026-06-15T12:03:43+0800` |
| `api/app/routes/__pycache__/machines.cpython-313.pyc` | 1864 | `2026-06-14T13:53:12+0800` |
| `api/app/routes/__pycache__/sync.cpython-313.pyc` | 1050 | `2026-06-14T13:53:12+0800` |
| `api/app/routes/__pycache__/trace.cpython-313.pyc` | 31413 | `2026-06-19T21:46:24+0800` |
| `api/tests/__pycache__` | 288 | `2026-07-05T21:16:01+0800` |
| `api/tests/__pycache__/test_accepted_station_events_api.cpython-313-pytest-9.1.1.pyc` | 53887 | `2026-07-05T13:49:21+0800` |
| `api/tests/__pycache__/test_accepted_station_events_api_db_backed.cpython-313-pytest-9.1.1.pyc` | 86668 | `2026-07-05T21:16:01+0800` |
| `api/tests/__pycache__/test_accepted_station_events_api_db_backed.cpython-313.pyc` | 46093 | `2026-07-05T21:16:01+0800` |
| `api/tests/__pycache__/test_trace_by_cycle.cpython-313-pytest-9.1.1.pyc` | 9088 | `2026-06-19T22:24:40+0800` |
| `api/tests/__pycache__/test_trace_by_cycle.cpython-313.pyc` | 8932 | `2026-06-19T14:42:39+0800` |
| `api/tests/__pycache__/test_trace_recent.cpython-313-pytest-9.1.1.pyc` | 7684 | `2026-06-19T22:24:40+0800` |
| `api/tests/__pycache__/test_trace_recent.cpython-313.pyc` | 7528 | `2026-06-19T22:24:21+0800` |

The root `.pytest_cache` directory is a separate older ignored workspace
artifact (`192` bytes, `2026-06-19T22:24:40+0800`) and is outside the API
snapshot scope. No cache or bytecode path was deleted, normalized, or opened
for write.

## 6. Required local validation

Focused suite:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -m pytest -p no:cacheprovider -q api/tests/test_process_metrics_api.py
RESULT = 34 passed in 0.16s
```

Focused plus predecessor regression suite:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -m pytest -p no:cacheprovider -q api/tests/test_process_metrics_api.py api/tests/test_quality_trace_api.py
RESULT = 50 passed in 0.20s
```

In-memory compile and route registration:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -c 'from pathlib import Path; import app.main; files=(Path("api/app/routes/process_metrics.py"),Path("api/tests/test_process_metrics_api.py"),Path("api/app/main.py")); [compile(p.read_text(encoding="utf-8"),str(p),"exec") for p in files]; routes=[(r.path,tuple(sorted(r.methods or ()))) for r in app.main.app.routes if r.path == "/api/v2/process-metrics"]; assert routes == [("/api/v2/process-metrics",("GET",))], routes; print("IN_MEMORY_COMPILE_ROUTE=PASS")'
RESULT = IN_MEMORY_COMPILE_ROUTE=PASS
```

The tests use their fake connection boundary; no real DB connection or DB
runtime action was made. The required commands disabled both Python bytecode
writes and the pytest cache provider.

## 7. Read-only semantic spot checks

```text
SEMANTIC_SPOT_CHECKS = PASS
ROUTE = exact GET /api/v2/process-metrics registration
ACCEPTED_NOK_FIELDS = nok_code,nok_origin,nok_detail_code,nok_detail_source_event_id,nok_detail_evidence_fact_key
```

The repaired route has no `SINGLE_RESOLVED` emission; a single tuple without
an independently resolved historical authority remains `UNRESOLVED`, and
ideal CT has no numeric value. All five accepted NOK detail fields are
selected and checked; incomplete NOK detail produces `PARTIAL` with
`QUALITY_NOK_DETAIL_INCOMPLETE` while retaining the permitted denominator rate
value. Fully bound NOK remains `SUPPORTED` from the accepted-fact source.

The route remains accepted-fact-only, `BEGIN READ ONLY`, half-open
`[from,to)` SQL, deterministic `(event_ts, accepted_at, fact_key)` ordering,
and no data fallback (response metadata explicitly records `fallback: none`).
No numeric unsupported OEE, Performance, Availability, line, terminal, or
ideal-CT claim was introduced.

## 8. Changed-path and staged evidence

Execution root was verified read-only:

```text
pwd -P = /Users/chenjie/Documents/MES/edge-mes-demo
git rev-parse --show-toplevel = /Users/chenjie/Documents/MES/edge-mes-demo
```

Pre-report-write live Git evidence:

```text
git status --short --untracked-files=all = 882 lines
status SHA-256 = 2f3139cf37ef6520f165be0ed30c9f69364054440dedc5b43df443d79b858d6b
task-owned pre-existing status:
 M api/app/main.py
?? api/app/routes/process_metrics.py
?? api/tests/test_process_metrics_api.py
report path = absent
git diff --name-only = api/app/main.py, docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
git diff --cached --name-only = empty
git diff --check -- api/app/main.py = PASS
```

The candidate files, protected files, task files, prior reports, Ledger, and
all cache/bytecode paths were not modified. The only recovery-owned write is
the exact report path in Section 2. Existing dirty/untracked continuity was
not cleaned, staged, adopted, or otherwise changed.

## 9. State and counters

```text
WRITTEN = yes (this exact report)
REVIEWED = yes (authority, identity, cache, test, compile, route, and semantic audit)
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
CONTROL_PLANE_RECOVERY = 1
DB_RUNTIME_ACTION = 0
REMOTE_ACTION = 0
DOCKER_COMPOSE_ACTION = 0
PLC_VPLC_ACTION = 0
PRODUCTION_STIMULUS = 0
GIT_MUTATION = 0
```

This report establishes only local `WRITTEN` and `REVIEWED`. It does not
establish repaired-candidate acceptance, fresh Reliability acceptance,
Verification, deployment, activation, runtime loading, or production
acceptance. The prior G4-R HOLD report cannot be reused as fresh acceptance
for the changed candidate identities.

## 10. Parent intake boundary

```text
PARENT_INTAKE_BOUNDARY = PARENT_INDEPENDENT_RECOVERY_REPORT_INTAKE_ONLY
```

Parent must independently read/hash this report and every bound artifact,
verify the cache path/bytes/mtime snapshot and continuity evidence, and decide
whether the product-repair candidate can be accepted as a new identity. If the
parent accepts it, a fresh G4-R reliability re-review must be generated under
new authority. This report does not update the Ledger or authorize any later
gate.
