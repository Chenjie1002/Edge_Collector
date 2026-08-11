# P1-G4-DQ Focused Data Quality Review

## 1. Terminal result and boundary

```text
REPORT_NAME = P1_G4_DQ_FOCUSED_DATA_QUALITY_REVIEW_20260811T1645Z
REPORT_PATH = docs/reports/p1_g4_dq_focused_data_quality_review_20260811T1645Z.md
TASK_NAME = P1_G4_DQ_FOCUSED_DATA_QUALITY_REVIEW_20260811T1645Z
TASK_ROLE = Shadow Mainline Data Quality reviewer
GOAL_ID = P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1
CURRENT_GATE = P1-G4-DQ_FOCUSED_DATA_QUALITY
TERMINAL_RESULT = PASS
MVP_PATH = MVP-ALIGNED
NEXT_GATE = PARENT_INDEPENDENT_DQ_INTAKE
```

This is a local, read-only data-quality review of the bound repaired candidate.
It does not authorize DB/runtime, remote/RPi, production stimulus, deployment,
activation, P1-G4-V, P1-G5, Git publication, Ledger mutation, or Goal
completion. Fake-DB tests are synthetic implementation evidence only; they are
not production observations or DB-backed acceptance evidence.

## 2. Task self-identity gate

The exact authority file was verified before any other repository read/action:

```text
TASK_PATH = docs/thread_handoff/pm_task_20260811T1645Z_p1_g4_dq_focused_data_quality_review.md
TASK_TYPE = regular non-symlink
TASK_BYTES = 10211
TASK_SHA256 = dfbdcbcdc01e39953d6d2021c401ae8cb9df55f97ead2fad85a9ff9581ef7d7e
TASK_SELF_IDENTITY = PASS
```

The entry report path was absent and non-symlink before review work:

```text
REPORT_ENTRY_BEFORE_WRITE = ABSENT
```

## 3. Authority identities

All seven task-listed authorities were read at their exact paths. The two
task-required hard identities and all causal/context identities matched the
live files:

| authority | bytes | SHA-256 |
| --- | ---: | --- |
| `docs/thread_handoff/pm_operating_rules.md` | 69697 | `45d4be226d2c4754fb2b21b55fce6f4086cb24e643b170f1ad1ab475a596bf9f` |
| `docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_charter.md` | 20025 | `cfc05c53ef03f890cf5be2228f47369c2042457294384b82db9bd85b8c348dd3` |
| `docs/contracts/production_process_kpi_contract.md` | 28427 | `776e744314f9ec33884765c20f8d88dab45afeda74354cf7e10e7fc226809252` |
| `docs/reports/p1_g4_i_bounded_production_metrics_api_20260811T1525Z.md` | 14056 | `32d041fc243041be87ee7d43339237e7fa7a5aa53c0be904ed35a0afedab0482` |
| `docs/reports/p1_g4_repair_accepted_fact_lineage_nok_detail_20260811T1605Z.md` | 9073 | `e9b07c1b4585302a2aa1291fe7fed28eb8cb4334213d1283755e49420f03d0ba` |
| `docs/reports/p1_g4_repair_cache_baseline_recovery_20260811T1615Z.md` | 11639 | `0c9bfbabf6e14e7baefa13883c58e8c6d81ce3907ea12ba75690a042f50b5aee` |
| `docs/reports/p1_g4_fresh_reliability_review_20260811T1635Z.md` | 11287 | `9cbeadce9563c7b5e7c42e2a3b47d4312e9875c7c227bf56c3be294e5534e8e4` |

The causal reports were used as context and continuity evidence, not as a
substitute for this independent candidate/contract review.

## 4. Candidate and protected identities

The repaired candidate matched the bound identity set before and after local
validation:

| candidate | bytes | SHA-256 |
| --- | ---: | --- |
| `api/app/main.py` | 524 | `038f7ea2c900f8288742586fe38430f6f5e0ce352fd1e4d7117d0e467f811dad` |
| `api/app/routes/process_metrics.py` | 19771 | `a7313117776e6ba8255bf2f60755bfad5a6bcf510767f0129720f8425984f1cb` |
| `api/tests/test_process_metrics_api.py` | 23821 | `6eb1e0ced1cb745755f94b3719c1a91923ca7f6ffe4d538b21004b2a9432566a` |

Protected predecessor identities remained unchanged:

| protected artifact | bytes | SHA-256 |
| --- | ---: | --- |
| `docs/contracts/production_metrics_contract.md` | 8229 | `2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e` |
| `api/app/routes/quality_trace.py` | 9538 | `6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a` |
| `api/tests/test_quality_trace_api.py` | 13296 | `bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c` |

## 5. Data-quality evidence review

### Accepted fact source and raw/normalized boundary

- The G3 contract names `production_accepted_station_event_fact` as the sole
  accepted production truth source. The route declares the same source at
  `api/app/routes/process_metrics.py:16-18` and its only SELECT reads that
  relation at `:343-360`, bounded by exact `line_id`, `station_id`,
  `event_type='station_result'`, and `[from,to)` event time.
- No legacy KPI/Trace object, snapshot, cycle/station event, production unit,
  quality event, raw payload/hex, adapter diagnostic, current YAML, fallback,
  join, ACK/read_done, or write SQL is read or used as a numeric source.
  `source.fallback` is fixed to `none` at `:70-76` and metric source lineage
  remains explicit.
- `content_fingerprint` is selected as accepted-row evidence but is not used
  to choose a version or substitute a normalized/raw source. Duplicate
  `fact_key` rows fail closed; no raw/normalized payload is promoted to
  production truth.

### Deterministic identity, duplicate/conflict, and result validity

- The route checks missing/blank `fact_key`, repeated `fact_key`, and unknown
  `production_result` before `accepted_event_count` or Quality counts at
  `:395-432`. It never applies `DISTINCT`, first/last selection, synthetic
  identity, counter identity, time proximity, or adjacent-row pairing.
- SQL ordering is deterministic `(event_ts ASC, accepted_at ASC, fact_key
  ASC)` at `:354-356`. A repeated key, including the focused conflicting
  `content_fingerprint` fixture, returns `UNAVAILABLE` metrics without
  numeric values. Missing key and unknown result are likewise fail-closed.
- Focused tests cover duplicate/conflict, missing identity, and unknown result
  at `api/tests/test_process_metrics_api.py:419-499`; the SQL test also proves
  read-only transaction setup and no write/ACK/read_done path at `:393-416`.

### Config/hash lineage and NOK completeness

- The route selects accepted `config_hash` and `config_version` at
  `:345-349`. Missing/blank tuples are `UNRESOLVED`; multiple tuples are
  `MIXED`; a single tuple without an independently accepted historical
  resolver remains `UNRESOLVED` at `:382-393`. There is no current-YAML,
  default, profile, or implicit historical resolver in the candidate.
- Config-dependent metrics do not become numeric. `ideal_cycle_time` is
  `PARTIAL` without historical authority and uses the mixed-window reason when
  applicable; line/terminal output, Performance, Availability, and Full OEE
  remain unsupported/non-numeric at `:163-249`. Calendar event rate remains a
  separately named `observed_accepted_event_rate`, never Performance or an OEE
  denominator.
- All five accepted NOK fields are selected and checked:
  `nok_code`, `nok_origin`, `nok_detail_code`,
  `nok_detail_source_event_id`, and `nok_detail_evidence_fact_key` at
  `:37-43`, `:347-349`, and `:438-442`. Any missing/blank field makes
  `quality_rate` `PARTIAL` with `QUALITY_NOK_DETAIL_INCOMPLETE` while keeping
  only the contract-permitted denominator rate; a fully bound accepted NOK may
  be `SUPPORTED`. Focused tests cover incomplete and fully bound paths at
  `api/tests/test_process_metrics_api.py:272-319`.

## 6. Metric/status matrix and state separation

The exact fixed 14-metric DTO is declared at
`api/app/routes/process_metrics.py:19-34` and emitted in that order. The
focused suite asserts the exact tuple at
`api/tests/test_process_metrics_api.py:207-269`.

| state/metric class | observed behavior | evidence |
| --- | --- | --- |
| accepted event count/rate | Numeric only from accepted fact rows; rate is calendar-window event rate | route `:434-469`; tests `:166-205` |
| Quality | `ok`/`nok` are the denominator; `skip`/`not_applicable` are accepted events but excluded from Quality denominator | route `:434-437, :471-499`; test `:207-269` |
| incomplete NOK detail | `quality_rate=PARTIAL`, reason `QUALITY_NOK_DETAIL_INCOMPLETE`, numeric rate allowed only when denominator > 0 | route `:438-442, :501-534`; tests `:272-319` |
| valid empty | HTTP 200; only accepted event/rate/three Quality counts are zero; empty Quality rate is `UNAVAILABLE` with no value; unsupported metrics are not zero-filled | route `:443-446, :501-553`; test `:322-355` |
| source failure | HTTP 503, top-level `UNAVAILABLE`, accepted-fact source reason, empty metrics, no zero fallback | route `:365-380`; test `:358-390` |
| identity failure | HTTP 200 envelope with top-level/affected metrics `UNAVAILABLE` and no value; unsupported metrics remain unsupported | route `:395-432`; tests `:419-499` |
| unsupported authority | Unit count, station CT, ideal CT, line/terminal count, Performance, Availability, and Full OEE omit numeric `value` | route `:163-249`; test `:255-266` |

The response's `numeric_value_allowed` is derived from actual value presence and
the `value` key is omitted when no numeric claim is allowed at
`:133-160`. This preserves the distinction between valid empty, source
unavailable, identity-invalid, mixed/unresolved config, partial NOK detail,
and unsupported authority.

## 7. Request/data boundary

- Exactly four query names are required once: `line_id`, `station_id`, `from`,
  `to`; unknown, duplicate, missing, blank, forbidden aggregation/terminal/
  metric/limit fields fail as `INVALID_REQUEST` before SELECT at
  `api/app/routes/process_metrics.py:102-130`.
- The endpoint is GET-only at `:326`; non-empty bodies are rejected before
  query parsing/SELECT at `:328-332`. RFC3339 requires a timezone offset or
  `Z`, inputs are canonicalized to UTC `Z`, `from < to` is required, and the
  maximum duration is 31 days at `:44-46, :89-99, :120-130`.
- Parameterized tests cover exact-once/forbidden inputs and no SELECT at
  `api/tests/test_process_metrics_api.py:577-661`, UTC and half-open boundary
  behavior at `:664-704`, body rejection at `:707-723`, and non-GET 405/no
  SELECT behavior at `:726-734`.
- Invalid request envelopes contain `INVALID_REQUEST` and no
  `numeric_value`; identity/source-unavailable responses contain no metric
  numeric value where the contract forbids it.

## 8. Required local validation

Approved project runtime was fresh-verified as Python `3.13.3` on `arm64`.
All required commands used `PYTHONDONTWRITEBYTECODE=1`, `-B`, and
`-p no:cacheprovider`; the fake-DB boundary was retained and no real DB
connection was used.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -m pytest -p no:cacheprovider -q api/tests/test_process_metrics_api.py
RESULT = 34 passed in 0.16s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -m pytest -p no:cacheprovider -q api/tests/test_process_metrics_api.py api/tests/test_quality_trace_api.py
RESULT = 50 passed in 0.19s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -c 'from pathlib import Path; import app.main; files=(Path("api/app/routes/process_metrics.py"),Path("api/tests/test_process_metrics_api.py"),Path("api/app/main.py")); [compile(p.read_text(encoding="utf-8"),str(p),"exec") for p in files]; routes=[(r.path,tuple(sorted(r.methods or ()))) for r in app.main.app.routes if r.path == "/api/v2/process-metrics"]; assert routes == [("/api/v2/process-metrics",("GET",))], routes; print("IN_MEMORY_COMPILE_ROUTE=PASS")'
RESULT = IN_MEMORY_COMPILE_ROUTE=PASS
```

The tests and compile check are local/synthetic/static evidence only. They do
not establish DB-backed runtime, deployment, activation, or production
acceptance.

## 9. Cache and continuity evidence

The preserved API cache/bytecode inventory was read-only before and after the
required checks:

```text
INVENTORY_SCOPE = api/.pytest_cache (recursive), api/**/__pycache__, api/**/*.pyc
PRE_INVENTORY_PATHS = 26
POST_INVENTORY_PATHS = 26
PRE_HASH_PROJECTION_FILES = 20
POST_HASH_PROJECTION_FILES = 20
API_CACHE_SNAPSHOT_SHA256 = 6f6274909b4746818f1b0b4ab82a66c718a660b708ea2c4135c2cfe50ed67209
PRE_POST_PATH_BYTES_MTIME = MATCH
LATEST_PREEXISTING_MTIME = 2026-07-05T21:16:01+0800
API_CACHE_BASELINE = PRE-EXISTING_AND_UNCHANGED
```

The hash projection was recomputed with the bound recovery form:

```text
for p in $(rg --files -uu api | rg '(^|/)(__pycache__/|.*\.pyc$|\.pytest_cache/)'); do stat -f '%Sm %z %N' -t '%Y-%m-%dT%H:%M:%S%z' "$p"; done | sort | shasum -a 256
```

The 26-path inventory includes directory entries; the bound hash command hashes
the 20 matching file rows. No cache/bytecode path was deleted, normalized,
touched, or opened for write.

Read-only continuity before this report write:

```text
PWD_P = /Users/chenjie/Documents/MES/edge-mes-demo
GIT_ROOT = /Users/chenjie/Documents/MES/edge-mes-demo
git diff --cached --name-only = empty
git diff --check = PASS
git diff --name-only = api/app/main.py, docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
git ls-files -m = api/app/main.py, docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
REPORT_ENTRY = ABSENT
STATUS_LINES_PRE_REPORT = 886
STATUS_SHA256_PRE_REPORT = 56f7a602d9b96a0d8994bf5a6b8b9cec625a0898b5818766aaa3fe3a659cfe1a
```

The status corpus, repaired candidate/test paths, earlier reports/tasks, and
pre-existing dirty/untracked continuity were not cleaned, staged, adopted, or
otherwise modified by this child. The only authorized child-owned write is this
exact report path.

## 10. State, counters, and allowlist

```text
PRODUCT_REPAIR = 0
CONTROL_PLANE_RECOVERY = 0
DB_RUNTIME_ACTION = 0
REMOTE_ACTION = 0
DOCKER_COMPOSE_ACTION = 0
PLC_VPLC_ACTION = 0
PRODUCTION_STIMULUS = 0
GIT_MUTATION = 0

WRITTEN = yes (this exact local report)
REVIEWED = yes (independent authority, identity, semantic, test, cache, and continuity review)
ACCEPTED = no (parent intake only)
VERIFIED = no (P1-G4-V not run)
STAGED = no
COMMITTED = no
PUSHED = no
DEPLOYED = no
ACTIVATED = no
RUNTIME_LOADED = no
PRODUCTION_ACCEPTED = no
```

No nested child, sub-agent, self-intake, repair, task/report outside the exact
report path, DB/runtime, remote, Docker/Compose, PLC/V-PLC, production, or Git
mutation was performed.

## 11. MVP path consistency

```text
MVP_CLASSIFICATION = MVP-ALIGNED
```

This review directly supports the approved MVP deliverable: a bounded,
station-scoped, read-only Process Metrics API that reports truthful accepted
event/rate/Quality facts and explicitly refuses unsupported unit, cycle, config,
line, terminal, Performance, Availability, and Full OEE numeric claims.

The minimum truth invariant is accepted-fact-only lineage plus fail-closed
identity/source behavior. No new product capability, historical registry,
retention/audit/forensics framework, infrastructure layer, runtime topology, or
broader evidence system was introduced. Validation complexity remains
proportional to the concrete false-PASS risks in this gate.

## 12. Parent-only next boundary and thread output

The single next gate is:

```text
NEXT_GATE = PARENT_INDEPENDENT_DQ_INTAKE
```

Parent must independently read/hash this report and all bound artifacts, verify
the exact candidate/contract identities, changed paths, tests, cache evidence,
and synthetic-versus-production boundary, then decide whether to set
`DATA_QUALITY_ACCEPTED=YES`. Only after that independent intake may parent
generate the exact P1-G4-V task bound to the same candidate identities.

This report establishes only local `WRITTEN` and `REVIEWED`; it does not
establish DQ `ACCEPTED`, `VERIFIED`, runtime loading, deployment, activation,
production acceptance, or Goal completion. This disposable child stops here.
