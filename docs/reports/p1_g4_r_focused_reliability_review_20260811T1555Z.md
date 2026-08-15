# P1-G4-R Focused Reliability Review

REPORT_NAME = P1_G4_R_FOCUSED_RELIABILITY_REVIEW_20260811T1555Z
REPORT_PATH = docs/reports/p1_g4_r_focused_reliability_review_20260811T1555Z.md
TASK_NAME = P1_G4_R_FOCUSED_RELIABILITY_REVIEW_20260811T1555Z
TASK_ROLE = Shadow Mainline Reliability reviewer
GOAL_ID = P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1
REVIEW_SCOPE = P1-G4-R_FOCUSED_RELIABILITY / exact G4-I candidate only

## 1. Terminal result

TERMINAL_RESULT = HOLD
EARLIEST_CAUSAL_BOUNDARY = accepted-fact response lineage/sufficiency classification after the bounded SELECT and before DTO serialization
NEXT_GATE = PARENT_INDEPENDENT_G4_R_INTAKE

The candidate is not advanced to Data Quality. No repair was attempted and this child does not create a repair task or authorize a later gate.

## 2. Task self-identity gate

The exact task file was read first, before any other repository read or action:

```text
TASK_PATH = docs/thread_handoff/pm_task_20260811T1555Z_p1_g4_r_focused_reliability_review.md
absolute path = /Users/chenjie/Documents/MES/edge-mes-demo/docs/thread_handoff/pm_task_20260811T1555Z_p1_g4_r_focused_reliability_review.md
regular non-symlink = yes
bytes = 10310
SHA-256 = fadc1d172947de5fe22c7a2de40b59129526d8c39b3633f8d5cd62d772e26f13
TASK_NAME = P1_G4_R_FOCUSED_RELIABILITY_REVIEW_20260811T1555Z
TASK_ROLE = Shadow Mainline Reliability reviewer
TASK_REVIEW_SCOPE = P1-G4-R_FOCUSED_RELIABILITY
```

SELF_IDENTITY_GATE = PASS.

## 3. Authority and bound artifact identities

All required authorities were present, regular non-symlink files, and matched the task bindings. No substitute object was reviewed.

| artifact | bytes | SHA-256 |
| --- | ---: | --- |
| docs/thread_handoff/pm_operating_rules.md | 69697 | 45d4be226d2c4754fb2b21b55fce6f4086cb24e643b170f1ad1ab475a596bf9f |
| docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_charter.md | 20025 | cfc05c53ef03f890cf5be2228f47369c2042457294384b82db9bd85b8c348dd3 |
| docs/reports/p1_process_kpi_bounded_api_accepted_state_capsule.md | 8201 | 643b2c39e1e37da542cf077be71d511e75035c0da08e6471f86a610e290a2b3a |
| docs/contracts/production_process_kpi_contract.md | 28427 | 776e744314f9ec33884765c20f8d88dab45afeda74354cf7e10e7fc226809252 |
| docs/reports/p1_g4_i_bounded_production_metrics_api_20260811T1525Z.md | 14056 | 32d041fc243041be87ee7d43339237e7fa7a5aa53c0be904ed35a0afedab0482 |
| api/app/main.py | 524 | 038f7ea2c900f8288742586fe38430f6f5e0ce352fd1e4d7117d0e467f811dad |
| api/app/routes/process_metrics.py | 19270 | 94fae79a51646d5e360d3654db31190fdfd0abb7a76f2de5d02b4446a817e7f9 |
| api/tests/test_process_metrics_api.py | 21011 | 60f0c6b0c40d5d39f7020a94bd4ec00a5f28015d70e0069fdd0c3bb9e3bda083 |
| docs/contracts/production_metrics_contract.md | 8229 | 2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e |
| api/app/routes/quality_trace.py | 9538 | 6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a |
| api/tests/test_quality_trace_api.py | 13296 | bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c |

AUTHORITY_IDENTITY_GATE = PASS.
REPORT_SELF_HASH = emitted in the terminal manifest after this write; not embedded to avoid self-referential hashing.

## 4. Review commands and results

Execution root:

```text
pwd -P = /Users/chenjie/Documents/MES/edge-mes-demo
git rev-parse --show-toplevel = /Users/chenjie/Documents/MES/edge-mes-demo
```

Fresh project runtime check:

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -c 'import platform,sys; ...'
```

Result: `.venv/bin/python`, CPython 3.13.3, arm64, base prefix `/Library/Frameworks/Python.framework/Versions/3.13`.

Approved base identity:

```text
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13
bytes=119328
SHA-256=f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5
```

Required focused suite:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -m pytest -p no:cacheprovider -q api/tests/test_process_metrics_api.py
```

Result: `31 passed in 0.19s`.

Required focused plus predecessor regression suite:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -m pytest -p no:cacheprovider -q api/tests/test_process_metrics_api.py api/tests/test_quality_trace_api.py
```

Result: `47 passed in 0.22s`.

In-memory compile and exact route registration:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -c 'from pathlib import Path; import app.main; files=(Path("api/app/routes/process_metrics.py"),Path("api/tests/test_process_metrics_api.py"),Path("api/app/main.py")); [compile(p.read_text(encoding="utf-8"),str(p),"exec") for p in files]; routes=[(r.path,tuple(sorted(r.methods or ()))) for r in app.main.app.routes if r.path == "/api/v2/process-metrics"]; assert routes == [("/api/v2/process-metrics",("GET",))], routes; print("IN_MEMORY_COMPILE=PASS")'
```

Result: `IN_MEMORY_COMPILE=PASS`; route registration exactly `GET /api/v2/process-metrics`.

Read-only Git checks:

```text
git diff --cached --name-only
git diff --check -- api/app/main.py
git diff -- api/app/main.py
```

Results: staged names empty; diff check PASS; `main.py` has only the process_metrics import and `app.include_router(process_metrics.router)` registration. No Git mutation command was run.

Static bound-route review markers confirmed `BEGIN READ ONLY`, bounded statement and idle-in-transaction timeouts, explicit accepted-fact source, half-open predicates, deterministic `(event_ts, accepted_at, fact_key)` order, and no SQL INSERT/UPDATE/DELETE, ACK/read_done, legacy source, current-YAML, fixed-WS03, or numeric unsupported OEE/line/terminal/cycle-time claims.

## 5. Reliability review matrix

| invariant | result | evidence |
| --- | --- | --- |
| exact endpoint and fixed 14-metric DTO | PASS | bound route and focused suite |
| exactly four query parameters, forbidden extras/body/methods | PASS | parser and focused parameterized cases; invalid requests do not SELECT |
| strict timezone-aware RFC3339, UTC canonicalization, `[from,to)` and 31-day bound | PASS | parser/source predicates and focused cases |
| accepted-fact-only read path, read-only transaction, timeout and stable order | PASS | route SQL and fake cursor assertions; no DB connection made |
| source failure, identity failure and unknown result fail closed | PASS | 503 source envelope and focused missing/duplicate/unknown cases |
| valid empty-window separation and unsupported numeric suppression | PASS | focused empty/matrix cases |
| mixed/unresolved historical configuration state | HOLD | blocker F1 below |
| no false Performance/Availability/Full OEE/line/terminal/CT/ideal-CT numeric claim | PASS | fixed unsupported/partial metrics omit `value`; observed rate remains explicitly named |
| predecessor regression | PASS | 47-test combined suite and protected identities unchanged |
| in-memory compile/no API bytecode | PASS | exact route/test/main compile; `api` cache/bytecode audit NONE |
| exact `main.py` minimal diff | PASS | two-line registration diff; `git diff --check` PASS |
| exact task allowlist and Git staged state | PASS | candidate plus this report only; staged names empty |
| NOK detail sufficiency status | HOLD | blocker F2 below |

## 6. Reliability blockers

### F1 — `source.config_window_state` can falsely claim historical resolution

The G3 contract requires each config tuple to resolve through an independent accepted immutable historical config/profile authority; a tuple that cannot resolve must remain unresolved. The route derives the state at `api/app/routes/process_metrics.py:369-377` solely from whether rows have non-null `config_hash` and `config_version`, and emits `SINGLE_RESOLVED` whenever one tuple is present. It performs no historical authority resolution. The same response path describes the ideal-CT authority as “not resolved” at `api/app/routes/process_metrics.py:184-187` and returns no ideal-CT value, so the top-level source state and metric-level lineage state are contradictory.

This is a concrete fail-closed/production-truth defect: a consumer can treat the source window as historically resolved even though the candidate has not resolved the required authority. The focused suite covers `MIXED` but has no single-tuple-without-authority case. Earliest causal boundary is config state derivation after the accepted-fact SELECT. This remains a HOLD even though no config-dependent numeric value is emitted.

### F2 — NOK detail incompleteness is not fail-closed

The protected predecessor contract defines accepted NOK detail using accepted `nok_code`/`nok_origin` plus bound detail evidence. The route selects both `nok_code` and `nok_origin` at `api/app/routes/process_metrics.py:334-336`, but its completeness test at `api/app/routes/process_metrics.py:422-424` checks only `nok_code is None`; it does not validate `nok_origin` or the required detail-evidence binding. With a NOK row that has a code but lacks the remaining accepted detail evidence, the route reaches `api/app/routes/process_metrics.py:506-512` and emits `quality_rate.status=SUPPORTED` rather than the contract-required `PARTIAL`/explicit incomplete state.

This can overstate Quality sufficiency. The focused suite proves only the default fixture where `nok_code` is null and does not cover present-code/missing-origin-or-evidence. Earliest causal boundary is NOK detail classification before Quality DTO serialization.

No source/test/contract repair was attempted.

## 7. Changed-path and output evidence

Before the authorized report write, the exact task-owned status was:

```text
 M api/app/main.py
?? api/app/routes/process_metrics.py
?? api/tests/test_process_metrics_api.py
report path absent
```

The pre-report read-only audit recorded:

```text
git diff --name-only: 3 lines, SHA-256=f2fd1b5a4d5975281ef235dac03c33beea4ebec5db06e11ccb0e2827ee22f0bb
git ls-files -m: 3 lines, SHA-256=f2fd1b5a4d5975281ef235dac03c33beea4ebec5db06e11ccb0e2827ee22f0bb
git status --short --untracked-files=all: 878 lines, SHA-256=1df26938fef280773b9b740195b539de6fee56e4eb588093bad6ed948d1e80d1
cached/staged names: empty
```

The three candidate identities remained exact after tests/compile. The only child-owned write is this exact report path. Existing dirty/untracked repository continuity was not cleaned, staged, or adopted.

Cache/output audit: no `api` `.pyc`, `__pycache__`, or `.pytest_cache` was present before or after validation. A root `.pytest_cache/` was already present as an ignored directory with mtime `2026-06-19T22:24:40+0800`, prior to this task date; it was not touched or removed. The exact pytest commands disabled the cache provider and bytecode writes.

## 8. Action and state counters

```text
DB_RUNTIME_ACTION = 0
REMOTE_ACTION = 0
DOCKER_COMPOSE_ACTION = 0
PLC_VPLC_ACTION = 0
PRODUCTION_STIMULUS = 0
GIT_MUTATION = 0
PRODUCT_REPAIR = 0
```

The authorized report write establishes only local `WRITTEN`; it is not a Git mutation or product repair.

```text
WRITTEN = yes (this exact report)
REVIEWED = yes (local source/hash/compile/fake-boundary audit)
ACCEPTED = no (parent independent intake required)
VERIFIED = no
STAGED = no
COMMITTED = no
PUSHED = no
DEPLOYED = no
ACTIVATED = no
PRODUCTION_ACCEPTED = no
```

## 9. MVP path and thread assessment

MVP 路径一致性 = MVP-ALIGNED.

- Approved MVP deliverable: bounded station-scoped read-only Process Metrics API with truthful accepted-fact count/rate/Quality output and explicit unsupported sufficiency states.
- Minimum truth invariant: only accepted facts may produce numeric business metrics; unresolved identity/config/detail must not be represented as resolved or complete.
- No new product capability, threat model, evidence infrastructure, runtime topology, DB migration, remote action, or scope expansion was introduced.
- This HOLD is directly tied to preventing false historical-lineage and Quality-sufficiency claims; it is not a style or theoretical-completeness finding.

Thread output/context assessment: short durable report plus concise terminal manifest; disposable child scope is complete; parent should independently intake this report; no nested child/sub-agent was used or created.

## 10. Parent-only boundary

Parent PM must independently read and hash this report and all bound artifacts, classify F1/F2, verify continuity and decide the next exact authority. This child does not accept the candidate, update the Ledger, create a repair task, authorize Data Quality, authorize Verification, or claim Goal completion.
