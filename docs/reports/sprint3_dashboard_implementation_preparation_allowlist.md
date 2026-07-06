# Sprint 3 Dashboard implementation exact-file allowlist discovery / implementation preparation report

Date: 2026-07-06
Thread: Architecture / Integration
Status: PASS WITH RECOMMENDATIONS

This gate is preparation / allowlist discovery only. It does not authorize
Dashboard/frontend implementation, API route changes, API contract changes, DB
schema changes, tests, Postgres connections, Docker / docker compose lifecycle
actions, staging, commit, push, deploy, tag, rollback or real PLC pilot work.

## 1. Report identity

报告名称：
Sprint 3 Dashboard implementation exact-file allowlist discovery / implementation preparation report

任务名称：
Sprint 3 Dashboard implementation exact-file allowlist discovery / implementation preparation gate

执行 Thread：
Architecture / Integration

结论：
PASS WITH RECOMMENDATIONS

Rationale: read-only recovery matches the PM-provided live baseline
`39ec2351d1e3df7adccb064af4f5b0910f533687`, the governing contract and planning
docs are consistent, the repository currently has no implemented
Dashboard/frontend package, and the category-level Dashboard future allowlist can
be converted into an exact proposed file allowlist for a later PM-authorized
implementation gate. Recommendations remain because future implementation must
create a new frontend package under an exact allowlist and must stop with HOLD if
the existing accepted-station-events API or contract proves insufficient.

## 2. Scope

Reviewed files:

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`
- `docs/reports/dashboard_tech_stack_plan.md`
- `docs/custom_dashboard_plan.md`
- repository file/directory listing for Dashboard/frontend/package discovery

Changed files:

- `docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md`

Explicitly not touched:

- `.gitignore`
- `docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`
- `docs/reports/phase1_to_sprint2_management_keynote_10p.html`
- `docs/reports/sprint3_db_backed_api_validation_reliability_review.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260624.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260625.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`
- `api/app/routes/accepted_station_events.py`
- `api/app/main.py`
- `api/app/db.py`
- `api/tests/test_accepted_station_events_api.py`
- `api/tests/test_accepted_station_events_api_db_backed.py`
- DB migrations / schema files
- Collector/runtime/storage.py
- `config/mapping.yaml`
- `config/grafana/**`
- `docker-compose.yml`
- `README.md`

## 3. Evidence

### 3.1 Read-only recovery

Read-only recovery was performed first.

```text
git status -sb:
## main...origin/main
 M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

git log --oneline -8:
39ec235 Add PM handoff after Dashboard planning sync
843e0b5 Sync Dashboard planning status
4fcdd66 Plan Dashboard API implementation
ba02249 Sync DB-backed API validation rerun status
a0042fb Add PM handoff after DB-backed repair
1d040a6 Align DB-backed API failure assertion
78ce29b Plan DB-backed API validation
1012d71 Add PM handoff after API implementation closeout

git log -1 --format='%H %s':
39ec2351d1e3df7adccb064af4f5b0910f533687 Add PM handoff after Dashboard planning sync

git rev-parse origin/main:
39ec2351d1e3df7adccb064af4f5b0910f533687

git diff --name-only:
.gitignore

git diff --cached --name-only:
<empty>

git status --short --untracked-files=all:
 M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

Baseline decision: `HEAD == origin/main ==
39ec2351d1e3df7adccb064af4f5b0910f533687`, matching the PM-provided live
baseline. Cached diff was empty before this preparation report was created.
The existing dirty/untracked files are external excluded artifacts, not
authority for this gate.

### 3.2 Dashboard/frontend structure discovery

Read-only discovery found no current Dashboard/frontend package:

```text
package/config discovery:
<empty for package.json, lockfiles, vite.config.*, next.config.*, tsconfig.json,
vitest.config.*, playwright.config.*, jest.config.*>

frontend/dashboard/web/ui directory discovery:
<empty for frontend, dashboard, web, ui>

app/page/component/test directory discovery:
./api/app
./collector/app
./s7_plc_sim/app
./simulator/app
./sync_worker/app
```

Existing Dashboard-adjacent files are docs and Grafana configuration only:

```text
config/grafana/custom/README.md
config/grafana/custom/grafana-custom-font.css
config/grafana/custom/grafana-custom.ttf
config/grafana/dashboards/dashboard.yaml
config/grafana/dashboards/edge_mes_overview.json
config/grafana/dashboards/edge_mes_station_traceability.json
config/grafana/dashboards/raspberry_pi_host_monitor.json
config/grafana/datasources/postgres.yaml
config/grafana/datasources/prometheus.yaml
docs/contracts/dashboard_api_contract.md
docs/custom_dashboard_plan.md
docs/reports/dashboard_tech_stack_plan.md
docs/reports/grafana_profile_mixing_fix_report.md
docs/reports/next_architecture_plan.md
docs/reports/sprint3_dashboard_api_implementation_plan.md
docs/reports/sprint3_db_api_dashboard_consumer_plan.md
```

Structure decision:

- Existing `frontend/` package: not present.
- Existing Next.js / React / Vite package: not present.
- Existing Dashboard route/page file: not present.
- Existing Dashboard API client module: not present.
- Existing Dashboard DTO/schema validation module: not present.
- Existing Dashboard components directory: not present.
- Existing Dashboard focused tests directory: not present.
- Existing Grafana dashboards: present, but out of scope for this custom
  Dashboard/frontend implementation lane.

### 3.3 Allowlist compliance

The governing planning report's category-level future allowlist contains:

- Dashboard route/page file for the accepted events page.
- Dashboard API client module for
  `GET /api/v2/production/accepted-station-events`.
- Dashboard DTO/schema validation module for the accepted fact allowlist.
- Dashboard component files for accepted events table, query controls,
  page-local summary strip, selected-row NOK/detail evidence and trace reference
  panel.
- Focused Dashboard tests for query construction, state rendering, DTO
  allowlist, forbidden leakage and no-side-effect behavior.

This report converts that category-level list into exact file paths under a new
`frontend/` package proposal without authorizing those edits in the current
gate.

### 3.4 Git status

Observed final working tree after this preparation report:

```text
 M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

git diff --name-only:
.gitignore

git diff --cached --name-only:
<empty>
```

No tests were run. No DB connection, Docker action, staging, commit or push was
performed.

## 4. Proposed exact implementation allowlist

Existing files that future implementation may modify:

- None found. There is no existing custom Dashboard/frontend package, route/page,
  API client, DTO/schema validation module, component directory or focused test
  directory in the current repository.

New files that future Dashboard implementation may create, if PM separately
authorizes implementation:

- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/next.config.ts`
- `frontend/tsconfig.json`
- `frontend/src/app/layout.tsx`
- `frontend/src/app/accepted-events/page.tsx`
- `frontend/src/app/accepted-events/loading.tsx`
- `frontend/src/app/accepted-events/error.tsx`
- `frontend/src/lib/acceptedStationEvents/apiClient.ts`
- `frontend/src/lib/acceptedStationEvents/query.ts`
- `frontend/src/lib/acceptedStationEvents/schema.ts`
- `frontend/src/lib/acceptedStationEvents/viewModel.ts`
- `frontend/src/components/accepted-events/AcceptedEventsTable.tsx`
- `frontend/src/components/accepted-events/AcceptedEventsQueryControls.tsx`
- `frontend/src/components/accepted-events/PageSummaryStrip.tsx`
- `frontend/src/components/accepted-events/NokDetailEvidencePanel.tsx`
- `frontend/src/components/accepted-events/TraceReferencePanel.tsx`
- `frontend/src/components/accepted-events/AcceptedEventsStates.tsx`
- `frontend/src/styles/globals.css`

Implementation boundary for those files:

- Use only `GET /api/v2/production/accepted-station-events`.
- Dashboard query may send only `line_id`, `start_time`, `end_time`, `limit`
  and `cursor`.
- DTO allowlist must remain limited to accepted fact fields from
  `production_accepted_station_event_fact`.
- No raw/debug/diagnostic/candidate/legacy fallback fields.
- No `work_order` or `product`.
- `accepted_at` is accepted fact timestamp only, not collector freshness, ACK
  time, station freshness or read_done time.
- Page-level summaries must be labelled current page only, not line-wide or
  global totals.
- Loading/error/unavailable states must not render stale prior data as fresh
  production truth.
- Cursor must remain opaque and fail closed for invalid, expired or cross-scope
  cases.
- If the implementation needs API route, API contract or DB schema changes,
  stop and open a separate API/contract/schema gate.

## 5. Proposed exact focused test allowlist

Focused Dashboard tests that may be added later, if PM separately authorizes
tests/implementation:

- `frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts`
- `frontend/src/components/accepted-events/__tests__/AcceptedEventsTable.test.tsx`
- `frontend/src/components/accepted-events/__tests__/AcceptedEventsQueryControls.test.tsx`
- `frontend/src/components/accepted-events/__tests__/PageSummaryStrip.test.tsx`
- `frontend/src/components/accepted-events/__tests__/NokDetailEvidencePanel.test.tsx`
- `frontend/src/components/accepted-events/__tests__/TraceReferencePanel.test.tsx`
- `frontend/src/app/accepted-events/__tests__/page.test.tsx`

Focused test assertions should cover:

- query construction sends only `line_id`, `start_time`, `end_time`, `limit`,
  `cursor`;
- missing, invalid, inverted and `>31 days` windows fail closed before request;
- cursor is opaque, sent unchanged and cleared on scope/time/limit changes;
- DTO validation admits only accepted fact fields;
- raw/debug/diagnostic/candidate/legacy fallback fields do not enter the
  production render model;
- `work_order` and `product` remain excluded;
- `accepted_at` is not rendered as freshness, ACK time, station freshness or
  read_done time;
- loading, empty, invalid query, error and unavailable states are distinct;
- prior data cannot appear as fresh production truth during loading/error;
- page-level summaries are labelled current page only;
- no imports from DB clients, FastAPI route modules, Collector/runtime/storage,
  Docker/deploy helpers or Grafana datasource/dashboard files.

Later execution should be limited to the frontend package's focused unit /
component tests and package-local type/lint/build commands only if that package
has already defined them. Do not run broad pytest, DB-backed tests, Postgres,
Docker or `EDGE_MES_ENABLE_DB_BACKED_TESTS=1` for this Dashboard lane.

## 6. Explicitly excluded files

Excluded dirty/local artifacts:

- `.gitignore`
- `docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`
- `docs/reports/phase1_to_sprint2_management_keynote_10p.html`
- `docs/reports/sprint3_db_backed_api_validation_reliability_review.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260624.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260625.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md`

Excluded API / contract / DB files:

- `api/app/routes/accepted_station_events.py`
- `api/app/main.py`
- `api/app/db.py`
- `api/tests/test_accepted_station_events_api.py`
- `api/tests/test_accepted_station_events_api_db_backed.py`
- `docs/contracts/dashboard_api_contract.md`
- DB migrations / schema files

Excluded runtime / infrastructure / observability files:

- Collector/runtime/storage.py and other Collector runtime files
- `config/mapping.yaml`
- `docker-compose.yml`
- Dockerfiles
- `config/grafana/**`
- deploy, tag, rollback and real PLC pilot artifacts

Excluded docs/status unless PM later gives exact-path docs authorization:

- `README.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`
- PM handoff files

## 7. Blockers

None for this preparation / allowlist gate.

Potential HOLD conditions for the later implementation gate:

- future implementation needs API route behavior not already provided by
  `GET /api/v2/production/accepted-station-events`;
- future implementation needs DTO fields outside the accepted fact allowlist;
- future implementation needs `work_order`, `product`, raw/debug/diagnostic,
  candidate or legacy fallback fields;
- future implementation needs API contract wording changes;
- future implementation needs DB schema/migration changes;
- future implementation cannot keep loading/error/unavailable states from
  rendering stale data as fresh production truth.

## 8. Recommendations

- Authorize the next implementation only as a new Dashboard-only/read-only
  Level 2 implementation gate with the exact file paths in sections 4 and 5.
- Keep the first slice focused on the accepted events page, not broader Overview,
  OEE, Quality/Pareto, trace search, Grafana, diagnostics or raw payload surfaces.
- Keep `frontend/` as a standalone custom Dashboard package boundary so future
  staging can remain exact and auditable.
- Require Reliability, Data Quality and Verification focused implementation
  reviews before any stage/commit/push.
- If package manager choice changes from npm/package-lock to another tool, stop
  and update the exact package-file allowlist before implementation.

## 9. Next gate

Eligible next gate:

- Dashboard implementation exact-path authorization in a new
  Architecture / Integration implementation Thread, using this report as the
  exact future allowlist input.

Still not authorized:

- Dashboard/frontend implementation in this Thread;
- API/contract changes;
- DB migration/schema changes;
- tests;
- Postgres / DB-backed execution;
- `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`;
- Docker / docker compose;
- deploy / tag / rollback;
- real PLC pilot;
- stage / commit / push.

## 10. Thread output / context assessment

本次输出长度：中

当前 Thread 是否建议继续：no

下一轮是否建议新开 Thread：yes

理由：本 Thread 已完成 Dashboard implementation 前的 Level 2 preparation /
allowlist discovery gate，并生成了 exact future implementation allowlist。
后续若进入 implementation，应新开 Thread 并显式授权 exact files，避免把本轮
preparation-only 结论误扩展为 Dashboard/frontend implementation authorization。
