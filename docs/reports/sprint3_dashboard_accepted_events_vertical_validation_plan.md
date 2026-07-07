# Sprint 3 Dashboard accepted-events vertical validation planning gate report

Date: 2026-07-07
Thread: Architecture / Integration
Status: PASS WITH RECOMMENDATIONS

This gate is planning only. It does not authorize Dashboard/frontend changes,
API/contract changes, DB migration/schema changes, tests, Postgres / DB-backed
execution, `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`, Docker / docker compose,
deploy, tag, rollback, real PLC pilot, staging, commit or push.

## 1. Report identity

报告名称：
Sprint 3 Dashboard accepted-events vertical validation planning gate report

任务名称：
Sprint 3 Dashboard accepted-events vertical validation planning gate

执行 Thread：
Architecture / Integration

结论：
PASS WITH RECOMMENDATIONS

Rationale: read-only recovery matches the PM-provided live baseline
`f433c92420e797106fae6cddcbd01787641b9432`, the remaining dirty artifacts match
the expected external exclusions with no staged files, current status /
contract docs do not conflict with this planning-only gate, and the existing
Dashboard frontend plus accepted-station-events API contract can support a
future exact, focused vertical validation path without modifying Dashboard,
API, contract, DB, test, package, status or handoff files in this gate.

Recommendations remain because execution must be split into later
PM-authorized validation gates, with separate review of Reliability, Data
Quality and Verification evidence before any stage/commit/push.

## 2. Read-only recovery evidence summary

Read-only recovery was performed first.

```text
branch:
main tracking origin/main

HEAD:
f433c92420e797106fae6cddcbd01787641b9432 Add PM handoff after Dashboard frontend closeout

origin/main:
f433c92420e797106fae6cddcbd01787641b9432

latest log:
f433c92 Add PM handoff after Dashboard frontend closeout
42ccd32 Sync Dashboard frontend status
896c2d1 Add accepted-events Dashboard frontend
4ad0e91 Prepare Dashboard implementation allowlist
39ec235 Add PM handoff after Dashboard planning sync
843e0b5 Sync Dashboard planning status
4fcdd66 Plan Dashboard API implementation
ba02249 Sync DB-backed API validation rerun status

git diff --name-only:
.gitignore

git diff --cached --name-only:
<empty>
```

Observed external dirty artifacts to exclude:

- `.gitignore`
- `docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`
- `docs/reports/phase1_to_sprint2_management_keynote_10p.html`
- `docs/reports/sprint3_db_backed_api_validation_reliability_review.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260624.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260625.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md`

Baseline decision: `HEAD == origin/main ==
f433c92420e797106fae6cddcbd01787641b9432`, matching the PM baseline. Cached
diff was empty before this report was created. The existing dirty/untracked
artifacts are external exclusions, not authority for this gate.

## 3. Scope

Reviewed files:

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260707-1829.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `frontend/package.json`
- `frontend/src/lib/acceptedStationEvents/apiClient.ts`
- `frontend/src/lib/acceptedStationEvents/query.ts`
- `frontend/src/lib/acceptedStationEvents/schema.ts`
- `frontend/src/lib/acceptedStationEvents/viewModel.ts`
- `frontend/src/app/accepted-events/page.tsx`
- `frontend/src/app/accepted-events/__tests__/page.test.tsx`
- `frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts`
- `api/app/routes/accepted_station_events.py`
- `api/tests/test_accepted_station_events_api.py`
- `api/tests/test_accepted_station_events_api_db_backed.py`

Changed files:

- `docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`

Explicitly not touched:

- `.gitignore`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`
- PM handoff files
- `frontend/**`
- `api/**`
- `collector/**`
- `db/**`
- `config/**`
- `README.md`
- package / lock / build config files
- Docker / deploy / tag / rollback surfaces

## 4. Current gate basis

Closed gate chain supporting this planning branch:

- Dashboard implementation preparation / allowlist gate: CLOSED / PASS WITH
  RECOMMENDATIONS, commit `4ad0e91`.
- Dashboard accepted-events frontend implementation: CLOSED / PASS WITH
  RECOMMENDATIONS, commit `896c2d1`.
- Dashboard accepted-events frontend Reliability review: initial HOLD for B1/B2,
  repaired and CLOSED by re-review.
- Dashboard accepted-events frontend Data Quality review: CLOSED / PASS WITH
  RECOMMENDATIONS.
- Dashboard accepted-events frontend Verification review: initial HOLD for V-B1,
  repaired and CLOSED by re-review.
- Dashboard accepted-events frontend post-push docs/status sync: PASS, commit
  `42ccd32`.
- PM handoff after Dashboard frontend closeout: PASS, commit `f433c92`.

Current implemented boundary to preserve in future validation:

- Dashboard/frontend only.
- Read-only consumer.
- Only `GET /api/v2/production/accepted-station-events`.
- Query params only `line_id`, `start_time`, `end_time`, `limit`, `cursor`.
- DTO allowlist only accepted fact fields from
  `production_accepted_station_event_fact`.
- No raw/debug/diagnostic/candidate/legacy fallback.
- No `work_order` / `product`.
- `accepted_at` means accepted fact timestamp only, not freshness / ACK /
  station freshness / read_done.
- Page summaries are labelled current page only.
- Missing `line_id` / `start_time` / `end_time` fail closed before request.
- Cursor remains opaque and clears on line/time/limit scope changes.

## 5. Proposed vertical validation goals

The next validation branch should prove that the accepted-events production
truth displayed in Dashboard can be traced through this minimum chain:

```text
Collector accepted fact
-> production_accepted_station_event_fact
-> GET /api/v2/production/accepted-station-events
-> Dashboard accepted-events frontend
```

Validation goals:

- Prove Dashboard calls only
  `GET /api/v2/production/accepted-station-events`.
- Prove Dashboard sends only `line_id`, `start_time`, `end_time`, `limit` and
  `cursor`.
- Prove missing `line_id`, `start_time` or `end_time` fails closed before any
  request.
- Prove cursor is opaque, sent unchanged when valid for the same scope, and
  cleared after `line_id`, time window or `limit` changes.
- Prove invalid, expired and cross-scope cursor cases fail closed.
- Prove Dashboard does not decode, mutate or construct cursor payloads.
- Prove unsupported query params cannot be emitted by Dashboard.
- Prove frontend schema and render model match the API DTO allowlist.
- Prove forbidden raw/debug/diagnostic/candidate/legacy fields, `work_order`
  and `product` cannot enter DTO, viewModel, render model, page summary or
  NOK/detail panel surfaces.
- Prove NOK/detail display uses only accepted fact DTO evidence fields.
- Prove loading, empty, invalid query, error and unavailable states remain
  distinct.
- Prove stale prior data cannot be rendered as fresh production truth.
- Prove page summaries are labelled current page only.
- Prove `accepted_at` is never interpreted as freshness, ACK, station freshness
  or read_done.
- Prove empty responses are not interpreted as line stopped, collector stale or
  quality OK.

## 6. Proposed validation lanes

### 6.1 Frontend mocked/API-client lane

Purpose: validate request construction and response classification without real
API, DB, Postgres or browser runtime.

Future assertions:

- `fetchAcceptedStationEvents()` builds a `GET` request only for
  `/api/v2/production/accepted-station-events`.
- Generated `URLSearchParams` keys are exactly `line_id`, `start_time`,
  `end_time`, `limit`, and optional `cursor`.
- Client validation returns `invalid-query` before request for missing
  `line_id`, missing `start_time`, missing `end_time`, invalid time, inverted
  range, over-31-day range or invalid `limit`.
- API 4xx is rendered as `invalid-query`, 503 as `unavailable`, malformed DTO as
  `error`.
- Invalid, expired or cross-scope cursor responses render as invalid query /
  expired page state that requires restarting at page 1 with the current
  filters.
- Dashboard sends returned cursor strings unchanged for same-scope next-page
  requests and never decodes, mutates or constructs cursor payloads.
- No unsupported query params are emitted from Dashboard client code.

Execution status in this gate: not run.

### 6.2 Frontend component/viewModel lane

Purpose: validate render model and visible semantics with mocked DTO envelopes.

Future assertions:

- `parseAcceptedStationEventsEnvelope()` rejects any field outside the accepted
  fact allowlist.
- `toAcceptedEventsViewModel()` emits only accepted fact render fields.
- Fixtures containing the full forbidden surface matrix from section 6.2.1 do
  not enter DTO, viewModel, render model, page summary or NOK/detail panel
  surfaces.
- `PageSummaryStrip` labels aggregates as current page only.
- Accepted event rows label `accepted_at` as accepted fact timestamp only.
- NOK/detail panel uses only `production_result`, `nok_code`, `nok_origin`,
  `nok_detail_code`, `nok_detail_source_event_id`,
  `nok_detail_evidence_fact_key`, `fact_key` and `source_event_id`.
- Page shell renders loading, empty, invalid query, error and unavailable states
  distinctly, with no stale prior rows presented as fresh truth.

Execution status in this gate: not run.

#### 6.2.1 Forbidden surface fixture matrix

Future mocked DTO, schema, viewModel and component fixtures must explicitly
include every forbidden source/surface below and assert exclusion from all
production Dashboard surfaces named in this subsection:

| Forbidden fixture surface | Required exclusion targets |
| --- | --- |
| `raw_payload` | DTO, viewModel, render model, page summary, NOK/detail panel |
| `raw_hex` | DTO, viewModel, render model, page summary, NOK/detail panel |
| `raw_sample_id` | DTO, viewModel, render model, page summary, NOK/detail panel |
| raw bytes | DTO, viewModel, render model, page summary, NOK/detail panel |
| decoded/source normalized candidate payloads | DTO, viewModel, render model, page summary, NOK/detail panel |
| normalized candidate payload | DTO, viewModel, render model, page summary, NOK/detail panel |
| adapter disposition | DTO, viewModel, render model, page summary, NOK/detail panel |
| adapter reason | DTO, viewModel, render model, page summary, NOK/detail panel |
| adapter phase | DTO, viewModel, render model, page summary, NOK/detail panel |
| candidate context | DTO, viewModel, render model, page summary, NOK/detail panel |
| raw/normalized comparison context | DTO, viewModel, render model, page summary, NOK/detail panel |
| decoder errors | DTO, viewModel, render model, page summary, NOK/detail panel |
| diagnostic payloads | DTO, viewModel, render model, page summary, NOK/detail panel |
| review payloads | DTO, viewModel, render model, page summary, NOK/detail panel |
| audit payloads | DTO, viewModel, render model, page summary, NOK/detail panel |
| `ack_status` | DTO, viewModel, render model, page summary, NOK/detail panel |
| `read_done` | DTO, viewModel, render model, page summary, NOK/detail panel |
| `collector_state` | DTO, viewModel, render model, page summary, NOK/detail panel |
| `quality_pareto_input` | DTO, viewModel, render model, page summary, NOK/detail panel |
| `dashboard_state` | DTO, viewModel, render model, page summary, NOK/detail panel |
| bare `result` | DTO, viewModel, render model, page summary, NOK/detail panel |
| bare `defect` | DTO, viewModel, render model, page summary, NOK/detail panel |
| bare `quality` | DTO, viewModel, render model, page summary, NOK/detail panel |
| bare `pareto` | DTO, viewModel, render model, page summary, NOK/detail panel |
| `work_order` | DTO, viewModel, render model, page summary, NOK/detail panel |
| `product` | DTO, viewModel, render model, page summary, NOK/detail panel |

The future validation matrix must fail if any of these fields or semantics are
accepted, renamed, normalized, summarized, nested under another production key
or shown as NOK/detail evidence. This matrix applies equally to DTO schema
validation, viewModel construction, component render models, `PageSummaryStrip`
aggregates and `NokDetailEvidencePanel` props.

### 6.3 API non-DB focused lane

Purpose: validate route contract, DTO allowlist, unsupported-query fail-closed,
cursor behavior and 503 mapping using the existing non-DB focused harness.

Future assertions:

- API reads only `production_accepted_station_event_fact`.
- Unsupported query params fail closed before DB query.
- Missing `line_id`, `start_time`, `end_time`, invalid time/window/limit and
  invalid, expired, malformed/tampered or cross-scope cursor fail closed.
- Cursor payload binds line/time/limit/direction/order and contains no forbidden
  surfaces.
- DTO response contains only accepted fact fields.
- DB/source failure maps to `503` with `{"detail": "accepted fact source unavailable"}`.

Execution status in this gate: not run.

### 6.4 DB-backed API validation lane, if needed later

Purpose: prove the live DB/API section of the chain against
`production_accepted_station_event_fact` with schema verification, fixture
insert, route read assertions and cleanup.

Boundary:

- Requires a separate Level 2 PM authorization.
- Requires explicit DB opt-in, loopback DSN safety, isolated
  `edge_mes_test_*` database, maintenance DB separation, cleanup proof and
  review gates.
- Must not be bundled with Dashboard/frontend changes.
- Must not claim new live DB evidence unless the future authorized execution
  actually runs and reports it.

Execution status in this gate: not run. No DB connection was made.

### 6.5 Browser/manual smoke lane, if needed later

Purpose: validate the user-visible Dashboard flow after non-DB/frontend and API
focused evidence is already green.

Future smoke scope:

- Start only the frontend dev/build preview surface that PM authorizes.
- Use mocked API or a separately authorized local API target.
- Verify accepted-events page can render invalid query, empty, unavailable,
  successful page, next cursor and scope-change reset states.
- Capture visible evidence that page summaries say current page only and
  `accepted_at` is not freshness / ACK / read_done.

Boundary:

- Requires separate PM authorization for server/browser execution.
- Does not authorize Postgres, DB-backed execution, Docker, deploy, tag,
  rollback or real PLC pilot.

Execution status in this gate: not run.

## 7. Exact future command allowlist proposal

These commands are proposals only. Do not execute without a later PM-approved
validation gate.

Frontend package-local commands, grounded in current `frontend/package.json`
scripts:

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm test
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm run typecheck
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm run build
```

Potential focused frontend test commands, if PM wants narrower first evidence:

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm test -- src/lib/acceptedStationEvents/__tests__/query.test.ts
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm test -- src/lib/acceptedStationEvents/__tests__/schema.test.ts
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm test -- src/lib/acceptedStationEvents/__tests__/viewModel.test.ts
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm test -- src/app/accepted-events/__tests__/page.test.tsx
```

API non-DB focused command:

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo && PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py -q
```

Optional static diff/format hygiene for future exact touched files:

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo && git diff --check -- frontend/src/lib/acceptedStationEvents/apiClient.ts frontend/src/lib/acceptedStationEvents/query.ts frontend/src/lib/acceptedStationEvents/schema.ts frontend/src/lib/acceptedStationEvents/viewModel.ts frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts frontend/src/app/accepted-events/page.tsx frontend/src/app/accepted-events/__tests__/page.test.tsx frontend/src/components/accepted-events/AcceptedEventsQueryControls.tsx frontend/src/components/accepted-events/AcceptedEventsStates.tsx frontend/src/components/accepted-events/AcceptedEventsTable.tsx frontend/src/components/accepted-events/PageSummaryStrip.tsx frontend/src/components/accepted-events/NokDetailEvidencePanel.tsx frontend/src/components/accepted-events/TraceReferencePanel.tsx frontend/src/components/accepted-events/__tests__/AcceptedEventsQueryControls.test.tsx frontend/src/components/accepted-events/__tests__/AcceptedEventsTable.test.tsx frontend/src/components/accepted-events/__tests__/NokDetailEvidencePanel.test.tsx frontend/src/components/accepted-events/__tests__/PageSummaryStrip.test.tsx frontend/src/components/accepted-events/__tests__/TraceReferencePanel.test.tsx api/app/routes/accepted_station_events.py api/tests/test_accepted_station_events_api.py
```

If a future PM prompt authorizes a narrower touched-file list, this hygiene
command must be regenerated from that exact list only. If PM has not supplied
an exact touched-file list, do not run static diff/format hygiene against a
broad directory such as `frontend`, `frontend/**` or `api/**`.

DB-backed validation command lane:

- Not included in the default allowlist.
- Requires separate Level 2 DB-backed validation authorization before any
  command containing `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`, Postgres DSNs,
  `api/tests/test_accepted_station_events_api_db_backed.py`, migration apply,
  fixture insert or cleanup execution.

Explicitly forbidden unless a later PM prompt separately authorizes them:

- broad `pytest`
- broad `npm` commands outside `frontend/`
- `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`
- Postgres / DB-backed execution
- Docker / docker compose
- deploy / tag / rollback
- real PLC pilot
- stage / commit / push

## 8. Exact future file/surface allowlist proposal

Frontend mocked/API-client and component/viewModel validation may inspect or, if
future repair is separately authorized, touch only exact Dashboard files
relevant to accepted-events:

- `frontend/package.json` for read-only script evidence / command grounding
  only; it is not a default future touch file unless PM separately authorizes a
  package/script change.
- `frontend/src/lib/acceptedStationEvents/apiClient.ts`
- `frontend/src/lib/acceptedStationEvents/query.ts`
- `frontend/src/lib/acceptedStationEvents/schema.ts`
- `frontend/src/lib/acceptedStationEvents/viewModel.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts`
- `frontend/src/app/accepted-events/page.tsx`
- `frontend/src/app/accepted-events/__tests__/page.test.tsx`
- `frontend/src/components/accepted-events/AcceptedEventsQueryControls.tsx`
- `frontend/src/components/accepted-events/AcceptedEventsStates.tsx`
- `frontend/src/components/accepted-events/AcceptedEventsTable.tsx`
- `frontend/src/components/accepted-events/PageSummaryStrip.tsx`
- `frontend/src/components/accepted-events/NokDetailEvidencePanel.tsx`
- `frontend/src/components/accepted-events/TraceReferencePanel.tsx`
- `frontend/src/components/accepted-events/__tests__/AcceptedEventsQueryControls.test.tsx`
- `frontend/src/components/accepted-events/__tests__/AcceptedEventsTable.test.tsx`
- `frontend/src/components/accepted-events/__tests__/NokDetailEvidencePanel.test.tsx`
- `frontend/src/components/accepted-events/__tests__/PageSummaryStrip.test.tsx`
- `frontend/src/components/accepted-events/__tests__/TraceReferencePanel.test.tsx`

Future repair/edit allowlists must remain exact accepted-events files. They
must not use `frontend`, `frontend/**` or directory-level allowlists such as
`frontend/src/components/accepted-events/__tests__/`.

API non-DB focused validation may inspect or, if future repair is separately
authorized, touch only:

- `api/app/routes/accepted_station_events.py`
- `api/tests/test_accepted_station_events_api.py`

DB-backed validation, if separately authorized later, must name its own exact
allowlist. The likely reviewed file is:

- `api/tests/test_accepted_station_events_api_db_backed.py`

Documentation/status sync, if needed after a future executed validation gate,
must be a separate exact docs authorization. This planning report does not
authorize edits to status, contract or handoff docs.

## 9. Explicit excluded files/surfaces

Excluded from this gate and from default future validation execution:

- `.gitignore`
- all old PM handoff external artifacts listed in read-only recovery
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- PM handoff files
- broad `frontend/**` outside exact accepted-events files
- broad `api/**` outside exact accepted-station-events route/test files
- `collector/**`
- `db/**`
- `config/**`
- `README.md`
- `docker-compose.yml`
- Dockerfiles
- deploy/tag/rollback scripts
- real PLC / V-PLC pilot surfaces
- Grafana dashboards/datasources

## 10. Risk / HOLD conditions

Report HOLD in any future review/execution gate if:

- live `HEAD` / `origin/main` no longer match the PM baseline for that gate.
- cached diff is non-empty before an exact validation/edit gate begins.
- dirty/staged files exceed the PM-approved expected external artifacts.
- Dashboard/API contract docs conflict on gate state, scope or authorization
  boundary.
- validation requires Dashboard/frontend, API, contract, DB, test or package
  changes before PM authorizes those exact files.
- existing Dashboard/API contract cannot support the minimum vertical validation
  without API/contract/schema change.
- future command allowlist cannot stay exact, focused and no-DB by default.
- future repair/edit allowlist uses broad `frontend`, `frontend/**`, `api/**`
  or directory-level test surfaces instead of exact files.
- Dashboard emits unsupported query params or any endpoint other than
  `GET /api/v2/production/accepted-station-events`.
- invalid, expired or cross-scope cursor does not fail closed.
- Dashboard decodes, mutates or constructs cursor payloads instead of treating
  cursor as opaque API-owned state.
- DTO/view model admits any forbidden surface from section 6.2.1, including
  raw/debug/diagnostic/candidate/legacy fields, `ack_status`, `collector_state`,
  `quality_pareto_input`, `dashboard_state`, bare `result` / `defect` /
  `quality` / `pareto`, `work_order` or `product`.
- loading/error/unavailable states can display stale prior data as fresh
  production truth.
- empty response is interpreted as line stopped, collector stale or quality OK.
- any DB-backed validation is attempted without separate Level 2 authorization.

## 11. Reliability review questions

- Does the proposed lane prove Dashboard remains a read-only consumer with no
  DB, Collector, PLC, V-PLC, runtime, storage.py, ACK/read_done or Docker side
  effect?
- Are missing scope/time inputs guaranteed to fail closed before request?
- Is cursor treated as opaque and cleared on line/time/limit scope changes, with
  invalid / expired / cross-scope cursor fail-closed behavior covered?
- Does Dashboard avoid decoding, mutating or constructing cursor payloads?
- Are invalid query, error and unavailable states distinct enough to prevent
  stale accepted fact data from being interpreted as fresh production truth?
- Does the future API non-DB lane cover 503 unavailable behavior without
  fallback to legacy/raw/current/diagnostic sources?

## 12. Data Quality review questions

- Does every Dashboard schema/viewModel field map one-to-one to the API DTO
  allowlist from `production_accepted_station_event_fact`?
- Do fixtures cover the full forbidden surface matrix in section 6.2.1 and
  prove those fields cannot enter DTO, viewModel, render model, page summary or
  NOK/detail panel surfaces?
- Are `work_order` and `product` still excluded?
- Is NOK/detail visible only from accepted fact DTO evidence fields?
- Are `event_ts`, `accepted_at`, `fact_key`, `content_fingerprint` and
  `source_event_id` presented as evidence/reference fields with no freshness or
  mutation authority?
- Are page summaries labelled current page only and never line-wide/global
  production truth?

## 13. Verification review questions

- Is the future command allowlist exact enough and no-DB by default?
- Are frontend tests scoped to package-local `npm test`, `npm run typecheck` and
  `npm run build` from current `frontend/package.json`?
- Is API non-DB validation limited to
  `api/tests/test_accepted_station_events_api.py`?
- Are broad pytest, DB-backed tests, Postgres, Docker, deploy/tag/rollback and
  real PLC pilot excluded unless separately authorized?
- Does the future validation matrix cover endpoint, query params, missing
  required inputs, unsupported params, DTO allowlist, forbidden leakage,
  cursor opacity/reset, invalid / expired / cross-scope cursor fail-closed
  behavior, state semantics and current-page-only summaries?
- Does the future validation plan prove Dashboard does not decode, mutate or
  construct cursor payloads?
- Are component test surfaces named as exact files rather than directory-level
  allowlists?
- Are external dirty artifacts excluded from any future stage/commit path?

## 14. Blockers

None for this planning gate.

No tests were run, no DB connection was made, and no runtime/server/browser
execution occurred in this gate.

## 15. Recommendations

- Open Reliability, Data Quality and Verification focused planning reviews
  before any validation execution.
- Keep the first execution lane frontend mocked/API-client plus
  component/viewModel focused, no DB by default.
- Run the API non-DB focused lane separately or in the same future validation
  gate only if PM explicitly authorizes the exact API command.
- Treat DB-backed API validation as a separate Level 2 branch if a fresh live
  vertical proof is needed.
- Require a separate browser/manual smoke authorization if UI runtime evidence
  is needed.
- Do not update status docs from this planning gate; perform any future
  docs/status sync only after executed validation evidence exists and PM gives
  an exact docs allowlist.

## 16. Next gate

Eligible for:

- Reliability planning review.
- Data Quality planning review.
- Verification planning review / exact future run allowlist audit.

PM approval required before:

- any validation execution;
- Dashboard/frontend changes;
- API/contract changes;
- DB migration/schema changes;
- Postgres / DB-backed execution;
- `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`;
- browser/manual smoke execution;
- Docker / docker compose;
- deploy / tag / rollback;
- real PLC pilot;
- stage / commit / push;
- docs/status sync.

## 17. Thread output / context assessment

本次输出长度：中

当前 Thread 是否建议继续：no

下一轮是否建议新开 Thread：yes

理由：本 Thread 已完成新的 Level 2 planning-only durable report。后续应进入
Reliability / Data Quality / Verification focused planning reviews，或在 PM 明确
授权后进入独立 validation execution Thread，避免把 planning gate 误扩展为
tests、DB、browser smoke、implementation、stage/commit/push 或 docs/status sync
authorization。
