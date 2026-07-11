# Sprint 3 Collector Ingestion Adapter Plan

Date: 2026-06-28

Status: Sprint 3 Collector Ingestion Adapter planning/status reference.
Dashboard accepted-events strict parser fail-closed hardening is CLOSED after the
separate docs authority commit `7824063 Clarify Dashboard strict parser contract`
(`7824063305cfaf4d44db6c8a01d095dd59586f10`) and exact three-file implementation
commit `2cf616d Harden Dashboard accepted-events parser`
(`2cf616d4dafbd497ec3db29ade826b1159e9025a`). The separately authorized
all-22-field explicit-null regression tests-only gate is CLOSED / PASS and
committed/pushed at `bdbcea0 Add explicit-null accepted event coverage`
(`bdbcea0707941b4ca98f3fe4393bbbfae98a3764`). The Dashboard accepted-events
UI/state stale-data planning gate is CLOSED / PASS WITH RECOMMENDATIONS and its
authority report is committed/pushed at `156a812 Plan Dashboard stale-data
regression coverage` (`156a812bf4529e198ca32373d7d109370a6e3e0d`). The
separately authorized tests-only Verification gate is CLOSED / PASS and
committed/pushed at `963218a Add Dashboard stale-data regression coverage`
(`963218a098e97b5d3c4993f2913e5f7f7355f98e`) with focused `page.test.tsx: 14
passed`. The Dashboard frontend typecheck/build validation planning gate is
CLOSED / PASS WITH RECOMMENDATIONS and its authority report is committed/pushed
at `2a88ffe Plan Dashboard frontend typecheck build validation`
(`2a88ffec6dd528b52e104f75f0395f7ecf0bfe2e`). The commands-only Verification
execution is CLOSED / PASS: `npm run typecheck` (`tsc --noEmit`) and `npm run
build` (`next build`) both exited 0, with zero tracked frontend drift; allowed
transient artifacts `frontend/tsconfig.tsbuildinfo`, `frontend/.next/` and
`frontend/next-env.d.ts` were precisely cleaned. No source/config/test/package
file changed and no implementation commit exists. The authoring-time baseline
for this docs/status sync is `HEAD == origin/main ==
2a88ffec6dd528b52e104f75f0395f7ecf0bfe2e`; it is a durable audit marker and
does not require a later docs-only HEAD to remain identical. The strict-parser
planning and exact-envelope Verification reviews had initial HOLDs, respectively
for generic Envelope `meta` conflict and item required/optional missing/null
ambiguity; contract clarification and required-key/null repair closed both.
Dashboard accepted-events nested/renamed leakage defense-in-depth fixture is also
CLOSED / PASS after the apiClient focused no-DB test branch. Dashboard accepted-events no-DB vertical validation
execution remains CLOSED / PASS WITH RECOMMENDATIONS after frontend dependency
environment prep, Architecture / Integration execution and Verification / Data
Quality / Reliability focused reviews. Dashboard accepted-events vertical
validation planning remains CLOSED / PASS WITH RECOMMENDATIONS and
committed/pushed at `dd6dc53`; the planning report is
`docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`.
The planning post-push docs/status sync is committed/pushed at `b7ce52b`, and
PM handoff after Dashboard vertical validation sync is committed/pushed at
`8b2e7a0`. The no-DB execution evidence is 4 focused frontend files / 19 tests
passed: `query.test.ts` 8, `schema.test.ts` 2, `viewModel.test.ts` 2 and
`page.test.tsx` 7. `frontend/node_modules/` exists only as a local dependency
artifact from the authorized `npm ci` environment prep and must be excluded from
staging. Dashboard accepted-events frontend implementation remains CLOSED / PASS
WITH RECOMMENDATIONS and committed/pushed at `896c2d1`; its post-push docs/status
sync is committed at `42ccd32`, and the PM handoff after Dashboard frontend
closeout is committed at `f433c92`.
DB/API/Dashboard accepted station events API implementation is CLOSED / PASS
WITH RECOMMENDATIONS and committed/pushed at `97dc4d5`; its Reliability, Data
Quality and Verification focused reviews are CLOSED / PASS WITH RECOMMENDATIONS
with no blockers. The changed files are `api/app/routes/accepted_station_events.py`
and `api/tests/test_accepted_station_events_api.py`. DB/API/Dashboard API
implementation planning is CLOSED / PASS WITH RECOMMENDATIONS and
committed/pushed at `2dc4b4d`; the planning file is
`docs/reports/sprint3_api_consumer_implementation_plan.md`. DB/API/Dashboard API
consumer contract freeze gate remains CLOSED / PASS WITH RECOMMENDATIONS and
committed/pushed at `f65a120`; its Reliability, Data Quality and Verification
focused reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers. The
changed file is `docs/contracts/dashboard_api_contract.md`. DB/API/Dashboard
consumer planning gate remains CLOSED / PASS WITH RECOMMENDATIONS and
committed/pushed at `f4de1c3`; its Reliability, Data Quality and Verification
focused reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers, and the
PM handoff after consumer planning is committed/pushed at `cd6dff8`.
DB-backed API validation harness repair is CLOSED / PASS and committed/pushed at
`8a8004c`; the repaired remote live DB-backed API validation rerun is CLOSED /
PASS with focused pytest `62 passed in 8.68s` and isolated test DB cleanup
`test_db_cleanup_ok edge_mes_test_api_read`; the PM handoff after DB-backed
validation harness repair is committed/pushed at `5543c87`. The later
DB-backed API validation planning gate is committed/pushed at `78ce29b`. The
first SSH-tunnel execution returned HOLD with focused pytest 1 failed / 87
passed because the controlled failure assertion expected 500 while the route
returned the contract-aligned 503. The focused repair is committed/pushed at
`1d040a6`, and the PM handoff after DB-backed repair is committed/pushed at
`a0042fb`. The DB-backed API validation execution rerun with SSH tunnel DSNs is
CLOSED / PASS WITH RECOMMENDATIONS with focused pytest `88 passed in 12.94s`.
The prior DB/API/Dashboard explicit DB opt-in/live local Postgres API Read
Validation Run Planning HOLD repair is committed/pushed at `2cfad5d` after
Verification B1 was closed by re-review. DB/API/Dashboard DB-backed/live
Postgres API Read Validation tests-only implementation remains CLOSED / PASS
WITH RECOMMENDATIONS and committed/pushed at `b30db5c`; the prior DB-backed API
read validation post-push docs/status sync is committed/pushed at `64d0e12`.
DB/API/Dashboard API read path implementation remains CLOSED / PASS WITH
RECOMMENDATIONS and committed/pushed at `763b248`. Dashboard/API implementation
planning is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at `4fcdd66`;
Architecture / Integration, Reliability, Data Quality and Verification focused
planning reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers.
Dashboard implementation, new migration, V-PLC/PLC pilot/deploy/tag/rollback,
future DB-backed reruns, Docker / docker compose lifecycle actions, actual
timeout failure proof, worker/runtime DB-backed gates and broad tests remain not
authorized.

Current PM intake live baseline for Dashboard accepted-events nested/renamed leakage defense-in-depth fixture docs/status sync:

- Branch: `main`.
- HEAD / `origin/main`: `244a6dd82b294f695aaf2bf6a6a849d7ad94dcb6`.
- Latest commit: `244a6dd Harden Dashboard leakage fixtures`.
- Current remaining dirty artifacts to exclude unless PM explicitly authorizes:
  `.gitignore`, `docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`,
  `docs/reports/phase1_to_sprint2_management_keynote_10p.html`,
  `docs/reports/sprint3_db_backed_api_validation_reliability_review.md`,
  `docs/thread_handoff/chatgpt_pm_handoff_20260624.md`,
  `docs/thread_handoff/chatgpt_pm_handoff_20260625.md`,
  `docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md`,
  `docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md`,
  `frontend/node_modules/`.
- Dashboard accepted-events no-DB vertical validation execution: CLOSED / PASS
  WITH RECOMMENDATIONS; Architecture execution PASS with 4 focused frontend files
  / 19 tests passed; Verification, Data Quality and Reliability focused reviews
  CLOSED / PASS WITH RECOMMENDATIONS, no blockers.
- Carry-forward recommendations: separately authorize `apiClient` focused tests
  for only-GET endpoint behavior, 4xx invalid/expired/cross-scope cursor mapping
  and 503 unavailable mapping; add explicit invalid `limit` executable coverage;
  expand forbidden leakage fixtures into a parameterized full matrix.
- Sprint 3 Slice J downstream planning-only gate: CLOSED / PASS WITH
  RECOMMENDATIONS.
- Sprint 3 Slice J tests-only hardening: CLOSED / PASS WITH RECOMMENDATIONS.
- Sprint 3 accepted production-fact visibility boundary: CLOSED / PASS WITH
  RECOMMENDATIONS; exact docs/status/PM-rule commit/push completed at `11cf077`.
- DB/API/Dashboard production visibility planning gate: CLOSED / PASS WITH
  RECOMMENDATIONS.
- Production-fact leakage negative tests planning gate: CLOSED / PASS WITH
  RECOMMENDATIONS.
- Tests-only adapter production-fact leakage negative implementation: CLOSED /
  PASS WITH RECOMMENDATIONS; committed at `fd3a799`.
- DB/API/Dashboard Slice 1 schema-only migration: CLOSED / PASS WITH
  RECOMMENDATIONS; committed at `e75f652`.
- DB/API/Dashboard Slice 2 DB write path: CLOSED / PASS WITH RECOMMENDATIONS;
  committed/pushed at `299d28a`.
- DB/API/Dashboard guarded DB-backed accepted fact tests: CLOSED / PASS WITH
  RECOMMENDATIONS; committed/pushed at `636ba37`.
- DB/API/Dashboard API read path planning gate: CLOSED / PASS TO REVIEW WITH
  RECOMMENDATIONS.
- DB/API/Dashboard API read path contract freeze: CLOSED / PASS WITH
  RECOMMENDATIONS; committed/pushed at `2d0918a`.
- DB/API/Dashboard API read path implementation: CLOSED / PASS WITH
  RECOMMENDATIONS; committed/pushed at `763b248`.
- DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only
  implementation: CLOSED / PASS WITH RECOMMENDATIONS; committed/pushed at
  `b30db5c`.
- DB/API/Dashboard DB-backed/live Postgres API Read Validation Reliability /
  Data Quality / Verification implementation reviews: CLOSED / PASS WITH
  RECOMMENDATIONS, no blocker.
- PM handoff after DB-backed API read validation tests: PASS; committed/pushed
  at `b817a9d`.
- DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push
  docs/status sync: PASS; committed/pushed at `64d0e12`.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning Gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning Reliability Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning Data Quality Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning Verification Review / Exact Future Run Allowlist Audit: CLOSED /
  HOLD, blocker B1.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning HOLD Repair: CLOSED / PASS, no blocker.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning HOLD Repair Verification Re-review: CLOSED / PASS WITH
  RECOMMENDATIONS, blocker B1 CLOSED.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning HOLD Repair exact-path commit/push: PASS; committed/pushed at
  `2cfad5d`.
- PM handoff after API DB-backed schema verification: PASS; committed/pushed at
  `99dfc26`.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning HOLD Repair post-push docs/status sync: PASS as local
  docs/status-only sync; not committed/pushed by this gate.
- DB-backed API validation harness repair: PASS; committed/pushed at `8a8004c`.
- Remote existing PostgreSQL DB-backed API validation rerun with repaired
  RecordingConnection proxy: PASS; focused pytest `62 passed in 8.68s`; test DB
  cleanup `test_db_cleanup_ok edge_mes_test_api_read`.
- PM handoff after DB-backed validation harness repair: PASS; committed/pushed
  at `5543c87`.
- DB-backed API validation planning exact-path commit/push: PASS; committed/pushed
  at `78ce29b`.
- DB-backed API validation first SSH-tunnel execution: CLOSED / HOLD; focused
  pytest 1 failed / 87 passed; controlled failure assertion expected 500 but
  route returned 503.
- DB-backed API validation focused repair: PASS; committed/pushed at `1d040a6`.
- PM handoff after DB-backed repair: PASS; committed/pushed at `a0042fb`.
- DB-backed API validation execution rerun with SSH tunnel DSNs: CLOSED / PASS
  WITH RECOMMENDATIONS; focused pytest `88 passed in 12.94s`; exact files were
  `api/tests/test_accepted_station_events_api.py` and
  `api/tests/test_accepted_station_events_api_db_backed.py`.
- DB-backed API validation rerun masked DSN facts: target host `localhost`,
  target port `5433`, target database `edge_mes_test_api_read`, maintenance
  database `postgres`, SSH tunnel Mac `localhost:5433` -> Pi `localhost:5432`.
- DB-backed API validation rerun cleanup: terse `-q` output did not print an
  explicit cleanup line; no pytest teardown/cleanup error was reported.
- DB-backed API validation post-execution docs/status sync: PASS;
  committed/pushed at `ba02249`.
- Dashboard/API implementation planning gate: CLOSED / PASS WITH
  RECOMMENDATIONS; committed/pushed at `4fcdd66`; changed file
  `docs/reports/sprint3_dashboard_api_implementation_plan.md`.
- Dashboard/API implementation planning Reliability / Data Quality /
  Verification focused reviews: CLOSED / PASS WITH RECOMMENDATIONS, no blocker;
  recommendations are carry-forward only.
- Dashboard implementation preparation / allowlist gate: CLOSED / PASS WITH
  RECOMMENDATIONS; committed/pushed at `4ad0e91`.
- Dashboard accepted-events frontend implementation: CLOSED / PASS WITH
  RECOMMENDATIONS; committed/pushed at `896c2d1`.
- Dashboard accepted-events frontend Reliability review: initial HOLD for B1
  missing query fallback and B2 package-local validation reproducibility;
  Architecture / Integration HOLD repair and re-review CLOSED / PASS WITH
  RECOMMENDATIONS, B1/B2 CLOSED.
- Dashboard accepted-events frontend Data Quality review: CLOSED / PASS WITH
  RECOMMENDATIONS, no blocker.
- Dashboard accepted-events frontend Verification review: initial HOLD for V-B1
  `npm run build` mutating `frontend/tsconfig.json` by adding `"incremental":
  true`; Architecture / Integration HOLD repair and re-review CLOSED / PASS
  WITH RECOMMENDATIONS, V-B1 CLOSED.
- Dashboard accepted-events frontend validation evidence: `npm ci` PASS; `npm
  test` PASS, 9 files / 24 tests; `npm run typecheck` PASS; `npm run build`
  PASS; generated artifacts cleaned; `git diff --check -- frontend` PASS. npm
  `allow-scripts` warning for `fsevents` / `sharp` is a CI/reproducibility
  note, not a blocker.
- Dashboard accepted-events frontend boundary: Dashboard/frontend only;
  read-only consumer; only `GET /api/v2/production/accepted-station-events`;
  query params only `line_id`, `start_time`, `end_time`, `limit`, `cursor`; DTO
  allowlist only accepted fact fields; no raw/debug/diagnostic/candidate/legacy
  fallback; no `work_order` / `product`; `accepted_at` means accepted fact
  timestamp only; page summaries are current-page-only.
- Dashboard accepted-events vertical validation planning gate: CLOSED / PASS WITH
  RECOMMENDATIONS; committed/pushed at `dd6dc53`; report
  `docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`.
- Dashboard accepted-events vertical validation planning review chain: Reliability
  PASS WITH RECOMMENDATIONS; Data Quality PASS WITH RECOMMENDATIONS;
  Verification initial HOLD for B1/B2/B3; Architecture / Integration HOLD repair
  PASS WITH RECOMMENDATIONS; Verification re-review PASS WITH RECOMMENDATIONS,
  B1/B2/B3 CLOSED.
- Dashboard accepted-events vertical validation planning boundaries: no
  validation execution; no tests; no DB-backed run; no browser/manual smoke; no
  Docker/runtime/server; no frontend/API/contract/package/DB edits; no
  docs/status sync execution. First future execution lane remains no-DB by
  default and exact-command scoped.
- Dashboard accepted-events frontend committed files in `896c2d1`: `frontend/next.config.ts`, `frontend/package-lock.json`, `frontend/package.json`, `frontend/src/app/accepted-events/__tests__/page.test.tsx`, `frontend/src/app/accepted-events/error.tsx`, `frontend/src/app/accepted-events/loading.tsx`, `frontend/src/app/accepted-events/page.tsx`, `frontend/src/app/layout.tsx`, `frontend/src/components/accepted-events/AcceptedEventsQueryControls.tsx`, `frontend/src/components/accepted-events/AcceptedEventsStates.tsx`, `frontend/src/components/accepted-events/AcceptedEventsTable.tsx`, `frontend/src/components/accepted-events/NokDetailEvidencePanel.tsx`, `frontend/src/components/accepted-events/PageSummaryStrip.tsx`, `frontend/src/components/accepted-events/TraceReferencePanel.tsx`, `frontend/src/components/accepted-events/__tests__/AcceptedEventsQueryControls.test.tsx`, `frontend/src/components/accepted-events/__tests__/AcceptedEventsTable.test.tsx`, `frontend/src/components/accepted-events/__tests__/NokDetailEvidencePanel.test.tsx`, `frontend/src/components/accepted-events/__tests__/PageSummaryStrip.test.tsx`, `frontend/src/components/accepted-events/__tests__/TraceReferencePanel.test.tsx`, `frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts`, `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`, `frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts`, `frontend/src/lib/acceptedStationEvents/apiClient.ts`, `frontend/src/lib/acceptedStationEvents/query.ts`, `frontend/src/lib/acceptedStationEvents/schema.ts`, `frontend/src/lib/acceptedStationEvents/viewModel.ts`, `frontend/src/styles/globals.css`, `frontend/tsconfig.json`.
- Dashboard/API implementation planning carry-forward recommendations: convert
  category-level future Dashboard implementation allowlist into exact file paths
  before implementation authorization; add invalid / expired / cross-scope cursor
  UI negative tests; keep page-level summary labelled as current page only; keep
  future implementation Dashboard-only/read-only unless PM opens a separate
  API/contract gate. The former stale-prior-data carry-forward is CLOSED by
  `156a812` and `963218a`.
- Dashboard accepted-events no-DB vertical validation execution: CLOSED / PASS
  WITH RECOMMENDATIONS; docs/status sync committed/pushed at `b413876`; PM
  handoff after the sync committed/pushed at `c103e90`.
- Dashboard accepted-events no-DB vertical validation evidence: Architecture /
  Integration executed four focused frontend commands with 4 files / 19 tests
  passed (`query.test.ts` 8, `schema.test.ts` 2, `viewModel.test.ts` 2,
  `page.test.tsx` 7); Reliability, Data Quality and Verification focused
  reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers.
- Dashboard accepted-events apiClient focused no-DB tests: planning CLOSED / PASS
  WITH RECOMMENDATIONS; implementation CLOSED / PASS; Reliability CLOSED / PASS;
  Data Quality CLOSED / PASS WITH RECOMMENDATIONS; Verification CLOSED / PASS
  WITH RECOMMENDATIONS; exact-path commit/push PASS at `96c0928` /
  `96c0928970d9917e0a4142569ebbc8459d67cc3d`.
- apiClient focused no-DB tests changed only five frontend test files:
  `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts`,
  `frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts`,
  `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`,
  `frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts` and
  `frontend/src/app/accepted-events/__tests__/page.test.tsx`.
- apiClient focused no-DB evidence: `apiClient.test.ts` 7 passed,
  `query.test.ts` 12 passed, `schema.test.ts` 26 passed, `viewModel.test.ts` 3
  passed and `page.test.tsx` 8 passed.
- Dashboard accepted-events nested/renamed leakage defense-in-depth fixture:
  implementation CLOSED / PASS; Reliability CLOSED / PASS WITH RECOMMENDATIONS;
  Data Quality CLOSED / PASS WITH RECOMMENDATIONS; Verification CLOSED / PASS
  WITH RECOMMENDATIONS; exact-path commit/push PASS at `244a6dd` /
  `244a6dd82b294f695aaf2bf6a6a849d7ad94dcb6`.
- Nested/renamed leakage fixture changed only two frontend test files:
  `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts` and
  `frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts`.
- Nested/renamed leakage fixture evidence: `schema.test.ts` 49 passed,
  `viewModel.test.ts` 4 passed and exact two-file `git diff --check` PASS.
- Its prior strict parser fail-closed carry-forward is CLOSED by the separate
  exact-envelope clarification and required-key/null repair authority branch,
  then implementation commit `2cf616d`; it is not a future unimplemented
  recommendation.
- Dashboard accepted-events strict parser planning: CLOSED / initial HOLD because
  generic Envelope `meta` conflicted with endpoint response shape; exact-envelope
  contract clarification: CLOSED / PASS. Exact-envelope Reliability and Data
  Quality contract reviews: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
  Exact-envelope Verification: CLOSED / initial HOLD for item required/optional
  and missing/null ambiguity; item required-key/null contract repair: CLOSED /
  PASS; targeted Data Quality re-review: CLOSED / PASS WITH RECOMMENDATIONS, no
  blocker; targeted Verification re-review: CLOSED / PASS WITH RECOMMENDATIONS,
  original blocker CLOSED.
- Strict parser docs authority commit is exactly `7824063` /
  `7824063305cfaf4d44db6c8a01d095dd59586f10`: `docs/contracts/dashboard_api_contract.md`,
  `docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md`,
  `docs/reports/sprint3_dashboard_accepted_events_envelope_contract_clarification_report.md`,
  `docs/reports/sprint3_dashboard_accepted_events_item_required_key_contract_repair_report.md`.
  Strict parser implementation is a separate exact three-file commit `2cf616d` /
  `2cf616d4dafbd497ec3db29ade826b1159e9025a`: `frontend/src/lib/acceptedStationEvents/schema.ts`,
  `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`, and
  `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts`.
- Contract closeout: the endpoint-specific exact envelope accepts only outer
  `data`/`page`, `data.items`, and `page.next_cursor`/`page.limit`; `meta` is
  unsupported. Unknown enumerable own keys at envelope/data/page/item and missing
  required own keys fail closed. All 22 DTO keys are required by presence, but
  nullable values must use explicit JSON `null`; missing is not explicit `null`.
  Missing or unknown malformed 2xx is client `kind: "error"`; silent strip,
  normalization, fallback, partial parsing and nested-field salvage are forbidden.
  The current API route stays compatible and no API change occurred.
- Implementation/review closeout: `schema.ts` adds outer/data/page/item exact
  own-key validation, required-presence checks and the 22-field missing matrix;
  it removes `?? null` and preserves explicit `null`. `apiClient.ts` is unchanged;
  existing parser throws remain `kind: "error"`, with no retry, second request or
  fallback endpoint. Strict parser implementation CLOSED / PASS; Reliability
  implementation review CLOSED / PASS; Data Quality and Verification implementation
  reviews CLOSED / PASS WITH RECOMMENDATIONS, no blockers. No API, DB, Collector,
  runtime, viewModel, page, store or cache changed. Fresh no-DB focused frontend
  evidence for the strict-parser implementation branch: `schema.test.ts: 143 passed`;
  `apiClient.test.ts: 12 passed`; focused diff check PASS. That branch did not run
  full frontend suite, typecheck, build, browser smoke, API tests or DB tests.
- Follow-on explicit-null regression closeout: the separately authorized Level 1
  tests-only gate changed only
  `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`. It
  parameterizes all 22 required DTO fields one at a time with explicit JSON
  `null` and proves own-key presence, unchanged 22-key cardinality, preserved
  `null`, and exact item round-trip. Focused evidence:
  `schema.test.ts: 165 passed`; exact target diff check PASS. Exact-path
  commit/push: `bdbcea0` /
  `bdbcea0707941b4ca98f3fe4393bbbfae98a3764`. No production code, API, DB,
  Collector, runtime, viewModel, page, store, cache, contract or package/config
  changed. Full frontend suite, `apiClient.test.ts`, typecheck, build, browser
  smoke, API tests and DB tests were not run by this follow-on gate.
- UI/state stale-data closeout: the Level 1 planning gate is CLOSED / PASS WITH
  RECOMMENDATIONS and committed/pushed at `156a812` /
  `156a812bf4529e198ca32373d7d109370a6e3e0d`. The tests-only Verification gate
  changed only `frontend/src/app/accepted-events/__tests__/page.test.tsx`, is
  CLOSED / PASS, and is committed/pushed at `963218a` /
  `963218a098e97b5d3c4993f2913e5f7f7355f98e`. Focused evidence:
  `page.test.tsx: 14 passed`; exact target diff check PASS. The matrix proves
  ready-to-loading/error/unavailable/invalid-query transitions clear prior table,
  summary, NOK/detail evidence, trace references and distinctive values; ready
  non-empty to ready empty clears prior selected truth and reports zero current
  counts; client error/unavailable results render no ready production surfaces.
  No production code, API, DB, Collector, runtime, contract, package/config,
  typecheck, build, browser smoke or API/DB tests changed or ran in this gate.
- Frontend typecheck/build validation closeout: planning is CLOSED / PASS WITH
  RECOMMENDATIONS and committed/pushed at `2a88ffe` /
  `2a88ffec6dd528b52e104f75f0395f7ecf0bfe2e`. Verification execution is CLOSED /
  PASS. Package-local `npm run typecheck` (`tsc --noEmit`) and `npm run build`
  (`next build`) both exited 0. Build produced `/_not-found` and
  `/accepted-events`. No tracked frontend file changed; package, lockfile,
  `tsconfig.json`, `next.config.ts` and `frontend/src/**` remained unchanged;
  cached diff stayed empty. Only `frontend/tsconfig.tsbuildinfo`,
  `frontend/.next/` and `frontend/next-env.d.ts` were generated, and all were
  precisely cleaned. Final frontend status was empty except pre-existing
  `frontend/node_modules/`. No tests, install, server, browser, API/DB, Docker,
  repair or Git write operation ran; no implementation commit exists.
- DB/API/Dashboard consumer planning gate: CLOSED / PASS WITH RECOMMENDATIONS,
  no blocker; planning doc committed/pushed at `f4de1c3`.
- DB/API/Dashboard consumer planning Reliability / Data Quality / Verification
  focused reviews: CLOSED / PASS WITH RECOMMENDATIONS, no blocker;
  recommendations are carry-forward only.
- PM handoff after consumer planning: PASS; committed/pushed at `cd6dff8`.
- DB/API/Dashboard API consumer contract freeze gate: CLOSED / PASS WITH
  RECOMMENDATIONS, no blocker; changed file
  `docs/contracts/dashboard_api_contract.md`; committed/pushed at `f65a120`.
- DB/API/Dashboard API consumer contract freeze Reliability / Data Quality /
  Verification focused reviews: CLOSED / PASS WITH RECOMMENDATIONS, no blocker;
  recommendations are carry-forward only.
- DB/API/Dashboard API implementation planning gate: CLOSED / PASS WITH
  RECOMMENDATIONS, no blocker; planning doc
  `docs/reports/sprint3_api_consumer_implementation_plan.md`; committed/pushed
  at `2dc4b4d`.
- DB/API/Dashboard API implementation planning Reliability / Data Quality /
  Verification focused reviews: CLOSED / PASS WITH RECOMMENDATIONS, no blocker;
  recommendations are carry-forward only.
- DB/API/Dashboard accepted station events API implementation: CLOSED / PASS
  WITH RECOMMENDATIONS, no blocker; changed files
  `api/app/routes/accepted_station_events.py` and
  `api/tests/test_accepted_station_events_api.py`; committed/pushed at
  `97dc4d5`.
- DB/API/Dashboard accepted station events API implementation Reliability /
  Data Quality / Verification focused reviews: CLOSED / PASS WITH
  RECOMMENDATIONS, no blocker; recommendations are carry-forward only.
- Focused non-DB validation for the API implementation: `PYTHONPATH=api
  .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py -q`
  -> 53 passed; `PYTHONPATH=api .venv/bin/python -m compileall api/app` ->
  PASS; `git diff --check -- api/app/routes/accepted_station_events.py
  api/tests/test_accepted_station_events_api.py` -> PASS.
- DB/API/Dashboard Slice 2 exact commit gate: PASS.
- DB/API/Dashboard Slice 2 exact push gate: PASS.
- Guarded DB-backed accepted fact tests exact commit/push gate: PASS.
- WS01 / WS02 / WS03 station-level `raw_policy`: `raw_capable`.
- Line-wide `runtime_defaults.raw_policy`: `raw_not_provided`.
- `raw_required`: not introduced.
- `api/tests/test_accepted_station_events_api_db_backed.py` now includes
  API-side pre-insert schema/constraint/column/nullability verification for the
  future DB-backed API run path.
- Schema verification runs after migration apply and before fixture insert.
- Remote live DB-backed API validation has completed for the focused harness
  lane, and the later SSH-tunnel DB-backed API validation execution rerun has
  completed for the focused API rerun lane. Future DB-backed reruns,
  `EDGE_MES_ENABLE_DB_BACKED_TESTS=1` outside an approved gate, actual timeout
  failure proof, new DB migration, Dashboard, V-PLC, config, Docker / docker
  compose lifecycle actions, deploy, tag, rollback and real PLC pilot remain not
  authorized by this docs/status sync closeout.
- Only production fact source for DB/API/Dashboard consumers:
  `production_accepted_station_event_fact`.
- `raw_plc_sample`, `cycle_event`, `station_event`, `production_unit`,
  `quality_event`, `production_snapshot` and `production_events` must not be
  treated as equivalent production fact sources, fallback sources, legacy
  compatibility sources or join-derived field fillers.
- raw payload/raw_hex, decoded/source normalized payload, adapter
  disposition/reason, candidate context, raw/normalized comparison and
  diagnostic/review/audit payloads are diagnostic/review/debug only and must not
  enter OEE or traceability main production facts.
- `quality_pareto_input`, `dashboard_state` and bare `result`, `defect`,
  `quality` or `pareto` keys are forbidden as production consumer sources.
- `work_order` and `product` remain excluded until a later schema/contract
  authority gate.
- `accepted_at` is an accepted fact timestamp, not collector freshness, ACK time
  or station freshness.
- Optional debug/review diagnostics view must be a separate Level 2 gate and
  pass leakage-negative review before implementation.
- API consumer contract freeze, API implementation planning, accepted station
  events API implementation, DB-backed API validation planning/repair,
  DB-backed API validation execution rerun, Dashboard/API implementation
  planning, Dashboard implementation preparation / allowlist, Dashboard
  accepted-events frontend implementation, Dashboard accepted-events no-DB
  vertical validation execution, Dashboard accepted-events apiClient focused
  no-DB tests and the all-22-field explicit-null regression tests-only gate are
  closed. The next eligible branch is exact-path commit/push of this three-file
  docs/status sync after PM approval, then PM handoff may be considered if
  thread/context is long. Future Dashboard/API/DB expansion remains Level 2 and
  cannot be auto-authorized as DB-backed tests, DB execution, API/contract
  changes, Docker, stage, commit or push.
- Future DB-backed API validation planning must freeze exact DB opt-in scope,
  DSN/test DB safety, schema/migration verification, allowed tests, cleanup,
  `EDGE_MES_ENABLE_DB_BACKED_TESTS=1` usage and review gates before execution.
  Future Dashboard/API implementation planning must preserve the accepted fact
  source boundary, DTO allowlist, forbidden leakage, invalid
  query/filter/cursor/time/window, Dashboard empty/error/unknown states and
  no-side-effect assertions.

The E1 authoring baseline below is retained as a historical audit marker. It is
not the live repository baseline for this post-Slice I status sync.

Live baseline at E1 docs/status sync authoring time:

- Branch: `main`.
- HEAD / `origin/main`: `2c73410281d1465db166b66ddc23e27d9337b90a`.
- Latest commit: `2c73410 Repair Sprint 3 Slice E1 runtime raw decoder`.
- Sprint 2 implementation commit: `17cf5d2 Implement Sprint 2 generic station event model`.
- Sprint 2 docs-only closeout commit: `82b2127 Close out Sprint 2 documentation state`.
- Phase-1 tag: `phase1-pass-20260619`.
- Phase-2 tag: not created.
- Runtime integration: not started.
- Deploy / rollback drill: not performed.

## 1. Purpose

This plan freezes the first Sprint 3 Collector ingestion adapter slice as an
offline fixture contract. It prepares Reliability, Data Quality and Verification
review without authorizing code or tests.

The companion contract is:

- `docs/contracts/collector_ingestion_adapter.md`

## 2. Scope and non-goals

In scope:

- define the offline ingestion adapter boundary;
- define resolved config snapshot lookup by immutable `config_hash`;
- define source payload, normalized envelope, raw evidence, validation,
  fingerprint, lifecycle and projection-metadata boundaries;
- define reject/defer/quarantine-style diagnostic wrapper semantics;
- propose future file ownership and required future test groups.

Non-goals:

- no runtime Collector connection;
- no DB write;
- no migration;
- no FastAPI endpoint;
- no Dashboard or Trace UI;
- no V-PLC behavior changes;
- no real PLC pilot;
- no deploy, tag or rollback;
- no commit/push in this drafting thread.

## 3. First implementation slice definition

Slice name: `Collector ingestion adapter offline fixtures`.

Inputs:

- frozen resolved config snapshot;
- PLC/V-PLC source payload fixture;
- mapping/template/profile/station snapshot;
- optional raw payload;
- state index fixture.

Outputs:

- normalized `station_event` envelope;
- canonical bytes / fingerprints;
- validation decision;
- lifecycle output;
- projection metadata;
- reject/defer/quarantine-style decision wrapper.

This slice produces no DB row and no API-visible production outcome.

## 4. Contract decisions

### 4.1 Collector ingestion adapter contract

The adapter maps source fixture data into a candidate `station_event` envelope,
then delegates station-event semantics to `common.station_event`.

Key decisions:

- source payload boundary is fixture input plus source context;
- normalized envelope boundary is the candidate passed to shared validators;
- field authority is split between source facts, resolved config snapshots and
  adapter metadata;
- `event_ts` is source event time;
- `observed_at` is Collector first-observed UTC time;
- `created_at` is future DB time and is not present in current envelope;
- future runtime clock skew, missing source timestamp, monotonicity and
  watermark policy are not implemented; current offline fixtures must not infer
  `late`, `observed_at` must not override `event_ts`, and `created_at` remains
  future DB time outside the envelope;
- `plc_boot_id`, `profile_id`, `station_type` and `config_hash` must preserve
  historical lineage;
- `source_event_id` must come from PLC/V-PLC/source fixture stable sequence or
  source-provided stable identity, not random values, receive time, retry time,
  Collector wrapper IDs or transport retry IDs;
- adapter must call shared validation helpers and must not duplicate
  station-event rules;
- adapter must use shared canonical serializer/fingerprint helpers and never use
  language-default JSON for identity;
- projection output is metadata only in this slice, with no persistence and no
  API-visible production outcome.
- Sprint 3 adapter does not modify Phase-1 ACK, `read_done` or write-back
  semantics; adapter retry/wrapper logic is not an ACK owner, and this offline
  slice does not change boot/profile/counter/ACK behavior.

### 4.2 Resolved config snapshot contract

Lookup input: `config_hash` from incoming envelope/source context.

Required snapshot contents:

- line;
- PLC;
- station;
- station_type;
- station_enabled;
- mapping;
- payload template reference/version;
- raw_policy;
- decoder registry reference;
- decoder id / decoder version / callable decoder;
- NOK template;
- profile/cycle_profile;
- route/direct predecessor;
- config_version/hash.

Historical snapshot rule:

- events must be interpreted only by their own immutable `config_hash` snapshot;
- adapter must never fallback to latest/current runtime config.

Fail-closed cases:

- `CONFIG_NOT_FOUND`;
- `CONFIG_HASH_MISMATCH`;
- `EVENT_LINEAGE_INVALID`;
- `RAW_PARSE_ERROR`;
- `RAW_NORMALIZED_MISMATCH`;
- `RAW_CONTENT_FORBIDDEN`;
- `RAW_EVIDENCE_MISSING`.

### 4.3 D2-A decoder authority planning outcome

D2-A is a docs/contract-only authority repair. It freezes contract language for
decoder registry authority, decoder id / decoder version / callable decoder
authority, immutable resolved config snapshot binding, fail-closed decoder
taxonomy and the no-fallback rule. D2-A does not implement code, tests, schema,
config, mapping, runtime Collector integration or raw runtime wiring.

D2 authority decisions now carried by the companion contract:

- decoder registry identity and registry snapshot/hash are selected only through
  the immutable resolved config snapshot for the event `config_hash`;
- decoder id, decoder version and callable decoder authority are selected only
  from that immutable snapshot and its referenced decoder registry snapshot;
- no fallback to latest/current runtime config, latest registry, current mapping
  file or environment defaults is allowed;
- unknown decoder id, missing decoder callable, decoder callable exception,
  decoder output mismatch and forbidden raw content fail closed;
- raw-only remains unsupported and fail-closed before identity, projection or
  fingerprint production;
- `raw_not_provided` is the only normalized-only authority; `raw_capable` and
  `raw_required` missing raw remain fail-closed unless PM later approves a
  contract change;
- raw evidence is evidence, not an independent production fact.

D2-B fixture/test-only hardening is implemented, reviewed, committed and pushed
at `dafbbf8`. It covers decoder authority negative cases and raw_policy
fixtures without production code changes.

D2-C minimal registry/schema implementation is implemented, reviewed, committed
and pushed at `5e5a617`.

D2-C committed files:

```text
collector/app/services/decoder_registry.py
collector/app/services/resolved_config_registry.py
tests/test_collector_station_event_adapter.py
```

D2-C validation evidence:

```text
PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_station_event_adapter.py -> 43 passed
PYTHONPATH=collector:. .venv/bin/python -m pytest collector/tests/test_event_collector_adapter_gate.py -> 22 passed
PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_station_event_runtime_source.py -> 35 passed
.venv/bin/python -m compileall collector/app/services -> PASS
git diff --check -> PASS
git diff --cached --check before commit -> PASS
```

D3 actual raw-capable/raw-required runtime wiring is implemented, reviewed,
committed and pushed at `c9e7c22`. D3 owns runtime raw evidence wiring, not the
D2-A contract repair, D2-B tests-only hardening or D2-C offline registry/schema
implementation.

D3 committed files:

```text
collector/app/plc/mapping.py
collector/app/services/event_collector.py
collector/app/services/resolved_config_registry.py
collector/tests/test_event_collector_adapter_gate.py
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

D3 implementation summary:

```text
runtime station db_read(...) bytes are passed as raw_bytes into runtime source.
build_runtime_source_payload() generates raw_payload={"raw_hex": ...}.
raw_payload enters adapt_source_payload().
raw evidence remains evidence, not production fact.
decoder output remains normalized candidate only.
accepted adapter decision remains required before persist/ACK.
config/mapping.yaml now carries decoder_version and decoder_registry snapshot id/content hash.
mapping.py parses, validates and hash-covers authority fields.
resolved_config_registry.py builds immutable decoder registry snapshot binding from runtime mapping.
No env/default/latest/ad hoc fallback is intended.
DB/API/Dashboard-visible behavior unchanged.
storage.py not touched.
V-PLC behavior unchanged.
Docker/deploy/tag/rollback not authorized.
ACK/read_done ownership unchanged.
```

E1 runtime raw decoder repair is implemented, reviewed, committed and pushed at
`2c73410`. E1 is a narrow repair after Slice E HOLD. It changes the runtime raw
decoder payload materialization so `decode_read_plan(...)` receives
`bytearray.fromhex(raw_hex)` as local mutable decode input, while canonical
`raw_hex` evidence remains unchanged. Nominal Snap7 raw path persists exactly
once and ACK/read_done side effect occurs exactly once. Malformed raw remains
`RAW_PARSE_ERROR` fail-closed, raw/normalized mismatch remains
`RAW_NORMALIZED_MISMATCH` fail-closed, non-accepted decisions still do not
persist/ACK, diagnostics remain diagnostics and raw evidence remains evidence,
not production fact.

E1 committed files:

```text
collector/app/services/resolved_config_registry.py
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_runtime_source.py
```

E1 preserves exclusions: `config/mapping.yaml`, `raw_policy`, `storage.py`,
DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy and ACK/read_done
ownership remain unchanged.

### 4.4 Slice F1 raw_policy authority docs/contracts edit

Slice F1 is a Level 2 authority planning/edit for docs/contracts only. It
freezes raw_policy authority semantics after D3 runtime raw wiring and E1
runtime raw decoder repair. F1 does not authorize runtime implementation, tests,
config/schema/mapping changes, `raw_policy` value changes, DB/API/Dashboard,
V-PLC, Docker/deploy, `storage.py`, ACK/read_done ownership, tag, rollback or
real PLC pilot work.

The key F1 planning decision is that runtime code-path capability is not the
same thing as a mapping/config authority upgrade. Current runtime code can carry
raw bytes because `event_collector.py` passes `raw_bytes=data` and
`station_event_runtime_source.py` can generate `raw_payload` / `raw_hex`.
However, the current mapping/config authority declaration remains the immutable
snapshot value from `config/mapping.yaml`, whose default is still
`raw_policy: raw_not_provided`. Runtime raw capability must not automatically
upgrade that declaration to `raw_capable` or `raw_required`.

F1 freezes these raw_policy definitions:

- `raw_not_provided`: normalized-only may enter shared validation only when the
  immutable resolved snapshot, mapping or payload template explicitly declares
  that the source does not produce raw. It is not a synonym for a missing
  runtime raw path.
- `raw_capable`: source/mapping authority declares that raw can be provided.
  Missing raw must fail closed as `RAW_EVIDENCE_MISSING` or a future
  PM-approved equivalent. It must not silently downgrade to `raw_not_provided`.
  Raw parse errors and raw/normalized mismatches remain fail-closed.
- `raw_required`: raw is required evidence. Missing raw must fail closed, with
  no projection, persist or ACK. It must not enter implementation until PM has
  explicitly accepted the production data-flow impact of missing raw at runtime.

raw_policy remains tied to mapping/config authority, decoder registry authority,
the immutable resolved snapshot, raw/normalized evidence comparison,
`RAW_PARSE_ERROR`, `RAW_NORMALIZED_MISMATCH`, `RAW_EVIDENCE_MISSING`,
accepted/rejected/diagnostic decisions, accepted-only persist/ACK side effects
and future DB/API/Dashboard visibility. Rejected or diagnostic decisions must
not project, persist, ACK or become visible production facts.

Minimum future gate for `raw_capable`:

- mapping/config immutable snapshot explicitly declares raw capability;
- decoder registry authority is complete;
- raw/normalized evidence gate is defined;
- negative cases cover missing raw, parse error, mismatch and no fallback;
- Reliability, Data Quality and Verification gates are explicit.

Minimum future gate for `raw_required`:

- PM separately authorizes the change;
- runtime missing-raw fail-closed impact on production data flow is explicit;
- Reliability, Data Quality and Verification gates are completed;
- exact implementation allowlist is frozen;
- the task does not default-touch `storage.py`, DB/API/Dashboard/V-PLC,
  Docker/deploy, ACK/read_done or unrelated runtime surfaces.

Future implementation candidate files remain candidates only. They do not
authorize edits without a later PM-approved implementation prompt with an exact
allowlist.

### 4.5 Raw / normalized authority matrix

The contract defines the matrix for:

- raw-only;
- normalized-only;
- raw + normalized match;
- raw + normalized conflict;
- unknown decoder id;
- decoder missing;
- decoder mismatch/exception;
- forbidden raw content;
- same content, different raw / raw_variant;
- future exact-byte fixture.

MVP decision: decoder missing with raw may be fail-closed rejected as
`RAW_PARSE_ERROR`. Future runtime may evolve this into deferred/quarantine
semantics, but current offline contract does not persist quarantine. Raw-only
cannot become production facts. Rejected, deferred or quarantined inputs never
project.

Raw-only must not produce a production fact, projection metadata, defect detail,
Quality/Pareto row, API-visible state or ACK. Normalized-only remains valid only
under immutable `raw_not_provided` authority. A source declared `raw_capable` or
`raw_required` with missing raw remains fail-closed unless PM later approves a
contract change.

Data Quality targeted repair for DQ-B1:

- `normalized-only` may enter shared validation only when immutable source
  protocol, mapping or payload template declares raw is not provided, for example
  `raw_not_provided` or an equivalent no-raw capability.
- The no-raw declaration must come from the immutable resolved snapshot, mapping
  or payload template, not from a temporary fixture field.
- If the source/mapping/template requires raw and raw is missing, the offline
  slice must fail closed as rejected. It must not be marked as a future deferred
  diagnostic in the current D2-A/D2-B/D2-C authority path unless PM later
  approves a contract change.
- Raw-required or raw-capable missing raw must not produce offline projection
  metadata, production outcome, defect detail, DB-visible state or API-visible
  state.
- Adapter logic must not use `normalized-only` to bypass raw evidence checks.
- Adapter logic must not synthesize `30003/system_reserved` upstream evidence;
  `30003` skip relation depends on accepted upstream business evidence validated
  by shared stateful validation. Rejected, non-authoritative or cross-config
  upstream evidence must not produce detail projection.

### 4.5 Reject / defer / quarantine contract

The contract defines accepted, rejected, deferred, quarantined, duplicate,
conflict and raw_variant diagnostic decisions.

Important constraints:

- quarantined in this slice means diagnostic decision semantics only;
- no quarantine persistence is implemented;
- DB write allowed in this stage: no for all decisions;
- API-visible production outcome: no for all decisions in this stage.

### 4.6 Slice J downstream adapter decision / diagnostic / projection boundary

Slice J name: `Sprint 3 Slice J -- Downstream Collector Adapter Decision /
Diagnostic / Projection Boundary`.

Objective: freeze the downstream boundary after station-level `raw_policy`
rollout so future implementation work cannot confuse adapter diagnostics,
candidate payloads or raw evidence with production facts. Slice J makes the
accepted adapter decision the only route into the existing persist/ACK path and
keeps all non-accepted dispositions out of persistence, ACK, projection, defect
detail and production visibility.

Proposed tier: Level 2 for any later implementation because the boundary
touches runtime safety, fact authority, ACK/read_done side-effect routing and
future DB/API/Dashboard visibility. This docs/contracts freeze itself is a
Level 1 docs/contracts planning edit with no runtime semantics change.

Future candidate implementation allowlist category: Collector adapter decision
gate, runtime source/adapter tests and diagnostic-only assertions. Candidate
runtime files and tests must remain a future PM-approved exact allowlist; this
section does not authorize edits. Future implementation must not default-include
`storage.py`, DB/API/Dashboard/frontend, V-PLC, Docker/deploy,
`config/mapping.yaml`, `raw_required` introduction, ACK/read_done ownership or
line-wide `raw_policy` changes.

Slice J boundary decisions:

- only `accepted` adapter decisions may reach the existing persist/ACK path;
- `rejected`, `deferred`, `quarantined`, `duplicate`, `conflict` and
  `raw_variant` decisions must not persist, ACK, project, write defect detail or
  become DB/API/Dashboard-visible production facts;
- diagnostic observability may record reason codes and candidate context for
  review, but remains non-owner of ACK/read_done and must not drive
  persistence;
- `raw_payload` / `raw_hex` is evidence only, not a production fact or defect
  detail authority;
- decoded or normalized payload remains a candidate until an accepted adapter
  decision exists;
- DB/API/Dashboard production visibility is deferred to a separate
  production-fact boundary planning gate.

Required review gates before later implementation:

- Architecture / Integration: confirm ownership, side-effect path and exact
  implementation allowlist.
- Reliability: confirm non-accepted decisions are fail-closed and cannot ACK or
  mutate read_done.
- Data Quality: confirm candidate/raw/diagnostic data cannot leak into
  production facts, defect detail, Quality/Pareto or Dashboard state.
- Verification: confirm accepted-only and non-accepted no-side-effect cases are
  testable with deterministic fixtures and runtime regression checks.
- PM authorization: explicitly authorize implementation, tests, exact staging,
  commit/push or any DB/API/Dashboard/V-PLC/deploy/tag/rollback expansion.

Explicit non-goals for Slice J docs freeze:

- no runtime/source code changes;
- no tests run and no test files changed;
- no `config/mapping.yaml` change;
- no `raw_required` introduction;
- no `storage.py` change;
- no DB/API/Dashboard/frontend/V-PLC/Docker/deploy change;
- no ACK/read_done ownership change;
- no real PLC pilot, tag, rollback, stage, commit or push.

Next eligible gate after docs freeze: Reliability focused review of the Slice J
docs/contracts boundary. Implementation remains ineligible until Architecture,
Reliability, Data Quality and Verification gates close and PM separately
authorizes an exact implementation allowlist.

Post-hardening note: the later Slice J tests-only hardening gate has since
closed at `ed9a61e` with Reliability, Data Quality and Verification focused
reviews all PASS WITH RECOMMENDATIONS and no blocker. This does not authorize
DB/API/Dashboard/V-PLC/deploy/runtime expansion.

### 4.7 Accepted production-fact visibility boundary freeze

Purpose: freeze future production-fact visibility rules before any
DB/API/Dashboard implementation. This is a docs/contracts planning boundary
only. It does not authorize schema, storage, API, Dashboard, Trace UI, V-PLC,
Collector runtime, `storage.py`, `config/mapping.yaml`, Docker/deploy,
ACK/read_done ownership, tests, staging, commit, push, tag, rollback or real PLC
pilot work.

Accepted production facts:

- future DB/API/Dashboard gates may consider only accepted station-event facts
  as production-visible facts;
- accepted requires immutable config authority, `raw_policy` / decoder
  authority, shared station-event validation, duplicate/conflict checks and an
  adapter decision of `accepted`;
- candidate future production-visible facts are limited to accepted
  station-event business facts under this contract's field authority, including
  line/PLC/station identity, station type, profile/config lineage, event
  type/result, legal NOK detail when bound to accepted upstream business
  evidence, unit/DMC, cycle counter, source event identity and source event
  time;
- raw evidence, diagnostic wrapper fields, rejected candidates and
  non-accepted dispositions are not production facts.

Diagnostic-only artifacts:

- adapter disposition, reason code, candidate context and raw/normalized
  comparison context remain diagnostic, review and debug material only;
- diagnostic artifacts must not become production facts, Quality/Pareto input,
  defect detail authority or ACK/read_done authority;
- diagnostic visibility must not drive persistence, projection, retry commit,
  Dashboard state or production side effects.

Raw evidence visibility:

- `raw_payload` / `raw_hex` is evidence, not a production fact;
- raw evidence may be proposed later as review-only or audit-only material, but
  it must not default into DB/API/Dashboard production visibility;
- raw evidence is not defect detail authority, Quality/Pareto input, Dashboard
  state or ACK/read_done authority.

Normalized candidate visibility:

- decoded raw output and source normalized payload are candidates until the
  adapter decision is accepted;
- non-accepted candidates are diagnostic-only and must not enter production
  facts, projection metadata, defect detail, Quality/Pareto input or Dashboard
  state;
- rejected, deferred, quarantined, duplicate, conflict and raw_variant payloads
  must not become production-visible facts.

Defect detail guard:

- non-accepted dispositions do not write defect detail;
- NOK/detail visibility must be bound to accepted upstream business evidence
  and shared station-event validation;
- rejected, deferred, quarantined, duplicate, conflict and raw_variant payloads
  must not generate defect detail, Quality/Pareto input or Dashboard defect
  state.

DB/API/Dashboard visibility deferral:

- this gate continues to defer DB/API/Dashboard implementation;
- the current freeze defines future visibility rules only and does not perform
  schema, DB write path, API, UI or runtime work;
- any future DB/API/Dashboard gate must restate exact allowlist, review gates
  and production-fact leakage negative tests before implementation.

ACK/read_done ownership:

- production-fact visibility planning does not change ACK/read_done ownership;
- visibility, diagnostic and review-only logic must not become ACK/read_done
  owner;
- the existing boundary remains: no ACK/read_done mutation for the current
  non-accepted payload.

Future hardening backlog:

- duplicate/conflict precedence;
- historical config replay;
- exact-byte canonical fixture vectors;
- raw error taxonomy;
- production-fact leakage negative tests.

### 4.8 DB schema field-name namespace contract freeze

Purpose: freeze field-name and namespace wording for future DB/API/Dashboard
schema/API/UI gates. This is a docs/contracts planning boundary only. It does
not authorize SQL, migration, storage, API, Dashboard, Trace UI, runtime
Collector, `storage.py`, tests, staging, commit, push, deploy, rollback, tag or
real PLC pilot work.

Production namespace:

- future production fact fields must use `production.*`;
- the frozen accepted station-event production names are
  `production.line_id`, `production.plc_id`, `production.station_id`,
  `production.station_type`, `production.profile_id`,
  `production.config_hash`, `production.config_version`,
  `production.event_type`, `production.production_result`,
  `production.unit_id`, `production.dmc`, `production.cycle_counter`,
  `production.source_event_id`, `production.event_ts`,
  `production.accepted_at`, `production.fact_key` and
  `production.content_fingerprint`;
- frozen NOK/detail production authority names are `production.nok_code`,
  `production.nok_origin`, `production.nok_detail_code`,
  `production.nok_detail_source_event_id` and
  `production.nok_detail_evidence_fact_key`;
- NOK/detail production visibility requires accepted upstream business evidence
  and shared station-event validation.

Diagnostics namespace:

- diagnostic, review and debug material must use isolated `diagnostics.*`
  names;
- frozen diagnostic names are `diagnostics.adapter_disposition`,
  `diagnostics.adapter_reason_code`, `diagnostics.adapter_phase`,
  `diagnostics.candidate_event_id`,
  `diagnostics.candidate_context_ref`,
  `diagnostics.raw_normalized_compare_status` and
  `diagnostics.decoder_error_code`;
- diagnostic payloads must not contain ambiguous production-looking keys:
  `result`, `defect`, `quality`, `pareto` or `dashboard_state`;
- `RAW_NORMALIZED_MISMATCH` may appear only as
  `diagnostics.adapter_reason_code = RAW_NORMALIZED_MISMATCH` or
  `diagnostics.raw_normalized_compare_status = mismatch`; it is forbidden from
  NOK/detail, defect origin, Quality/Pareto input and Dashboard defect state.

Audit and review namespaces:

- frozen audit names are `audit.raw_evidence_ref`,
  `audit.raw_evidence_fingerprint`, `audit.raw_hex_ref`,
  `audit.decoder_registry_snapshot_id` and
  `audit.decoder_registry_content_hash`;
- frozen review names are `review.candidate_payload_ref`,
  `review.raw_normalized_diff_ref` and `review.quarantine_ref`;
- `raw_payload` / `raw_hex` is only review-only or audit-only evidence
  reference/fingerprint material. It is not a production fact, not production
  fact table input and not KPI/OEE/Quality/Pareto/Grafana production query
  input.

Non-accepted disposition boundary:

- `rejected`, `deferred`, `quarantined`, `duplicate`, `conflict` and
  `raw_variant` may appear only as diagnostic/audit/review isolated material;
- non-accepted dispositions must not write production facts, NOK/detail rows,
  Quality/Pareto input, Dashboard state, Grafana production fields or
  ACK/read_done authority;
- preserve exact wording: no ACK/read_done mutation for the current
  non-accepted payload.

Future leakage assertions:

- future DB/API/Dashboard implementation gates must replace synthetic adapter
  leakage keys with real schema/API/UI assertions;
- future gates must assert diagnostic payloads do not contain `result`,
  `defect`, `quality`, `pareto` or `dashboard_state`;
- future gates must assert non-accepted dispositions have no production row, no
  NOK/detail row, no Quality/Pareto/Grafana production fields and no raw
  evidence in a production table;
- future gates must preserve exact wording: no ACK/read_done mutation for the
  current non-accepted payload.

### 4.9 Tests-only adapter production-fact leakage negative closeout

Tests-only adapter production-fact leakage negative implementation is
implemented, reviewed, committed and pushed at `fd3a799` /
`fd3a79901619c9afe664c709834b7e396187f8b2`.

Changed test files:

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
```

Implementation summary:

- strengthened runtime non-accepted adapter decision coverage so diagnostic
  context does not expose production projection, production outcome, defect
  detail, Quality/Pareto or Dashboard keys;
- added offline production-fact leakage summary assertions;
- added a negative matrix for `rejected`, `deferred`, `quarantined`,
  `duplicate`, `raw_variant` and `conflict`;
- added diagnostic reason-code coverage proving `RAW_NORMALIZED_MISMATCH` cannot
  become NOK/detail or Quality authority;
- preserved accepted positive control only to seed legal accepted state for
  duplicate/conflict/raw_variant checks.

Validation evidence:

```text
PYTHONPATH=collector:. .venv/bin/python -m pytest collector/tests/test_event_collector_adapter_gate.py -> 36 passed
PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_station_event_adapter.py -> 46 passed
Verification closeout: collector/tests/test_event_collector_adapter_gate.py -> 36 passed in 0.12s
Verification closeout: tests/test_collector_station_event_adapter.py -> 46 passed in 0.06s
git diff --check -> PASS
```

Review sequence closeout:

```text
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Verification exact allowlist audit / review-sequence closeout: PASS WITH RECOMMENDATIONS, no blocker
```

Boundary preserved:

- future production visibility is limited to accepted station-event business
  facts after immutable config authority, `raw_policy` / decoder authority,
  shared validation, duplicate/conflict checks and adapter decision `accepted`;
- adapter disposition, reason code, candidate context and raw/normalized
  comparison context remain diagnostic/review/debug only;
- `raw_payload` / `raw_hex` is evidence, not a production fact;
- decoded/source normalized payloads remain candidates until accepted;
- non-accepted dispositions do not write defect detail;
- NOK/detail visibility must bind to accepted upstream business evidence;
- ACK/read_done ownership is unchanged; preserve exact wording: no ACK/read_done
  mutation for the current non-accepted payload;
- DB/API/Dashboard remains not authorized by this tests-only gate.

Carry-forward recommendations:

- future DB/API/Dashboard implementation gates should replace current synthetic
  visibility-summary keys with real schema/API/UI field assertions once those
  surfaces are explicitly authorized;
- future DB/API/Dashboard gates must restate exact allowlist, review gates and
  production-fact leakage negative tests;
- this tests-only adapter coverage must not be treated as DB/API/Dashboard
  implementation authorization.

Next eligible gate: DB/API/Dashboard production visibility contract gate, or a
separately authorized hardening planning gate for duplicate/conflict precedence,
historical config replay, raw error taxonomy or exact-byte canonical fixture
vectors. No implementation is authorized automatically.

### 4.10 Offline fixture inventory

Required future fixture inventory:

- 3-station `cycle_start` / `cycle_complete` / `station_result OK`;
- `station_result NOK` + `station_nok` detail companion;
- heartbeat;
- disabled_station heartbeat-only as post-MVP/future fixture, without implying
  current runtime disabled-station behavior;
- unknown config hash;
- mapping mismatch;
- payload_template_mismatch;
- route_predecessor_mismatch;
- direct_predecessor_mismatch;
- profile mismatch;
- station_type mismatch;
- unknown decoder id;
- raw decoder missing;
- raw decoder mismatch;
- decoder output payload_template mismatch;
- forbidden raw content;
- normalized-only with source protocol/mapping declared no-raw;
- raw-required source with missing raw;
- raw-capable source missing raw;
- duplicate;
- conflict;
- raw_variant;
- historical resolved config snapshot;
- current config changed but historical event still uses old snapshot;
- multi-mapping station requiring exact `mapping_id`;
- future JCS exact-byte canonical JSON/fingerprint vectors.

## 5. Future ownership proposal

Proposal only, not authorized implementation.

Possible future code:

- `collector/app/services/station_event_adapter.py`
- `collector/app/services/resolved_config_registry.py`

Possible future tests:

- `tests/test_collector_station_event_adapter.py`
- dedicated adapter fixture JSON path;
- future cross-runtime canonical fixture tests.

Existing files read-only for first implementation:

- `common/station_event/*`
- `common/line_config/*`

Explicitly excluded:

- untracked PM handoff artifacts;
- DB migrations;
- FastAPI routes;
- Dashboard/frontend;
- V-PLC runtime;
- Docker/deploy files.

## 6. Required future tests

| Test group | Acceptance criteria |
| --- | --- |
| Adapter nominal tests | nominal 3-station/result/NOK/heartbeat fixtures normalize and validate through shared helpers |
| Lineage tests | config hash, mapping, profile, station type and route/predecessor mismatches fail closed |
| Raw authority tests | raw-only, normalized-only declared no-raw from immutable snapshot/mapping/template, raw-required missing raw, raw-capable missing raw, decoder missing, decoder exception, `RAW_PARSE_ERROR`, `RAW_NORMALIZED_MISMATCH`, `RAW_CONTENT_FORBIDDEN` and `RAW_EVIDENCE_MISSING` never produce facts and remain distinguishable |
| Decoder authority tests | decoder registry snapshot, decoder id, decoder version and callable decoder are immutable-snapshot-bound; unknown decoder id, missing callable, callable exception, decoded output mismatch, forbidden raw content and no-fallback-to-latest/current cases fail closed |
| Decision tests | accepted/rejected/deferred/quarantined/duplicate/conflict/raw_variant wrappers are deterministic and non-persistent |
| Projection tests | wrapper decision and `projection_for()` metadata are asserted together; only accepted envelopes produce offline projection metadata; non-accepted decisions never project or leak rejected detail into Pareto/defect rows |
| Phase-1 regression tests | current 3-station runtime behavior remains unchanged |
| Future JCS exact-byte boundary tests | canonical bytes and fingerprints match approved vectors before JavaScript/PostgreSQL/API/DB integration |
| Future duplicate/conflict precedence tests | multi-key duplicate/conflict precedence covers `event_id`, `fact_key`, cycle role / production result key and detail key, not only a single `fact_key` |
| Future historical config replay tests | historical config replay is covered, including current config changed but historical event still uses old snapshot |

## 7. Review gates

| Gate | Required review question |
| --- | --- |
| Architecture gate | Are boundaries, field authority, ownership and non-goals clear enough for review? |
| Reliability gate | Are runtime safety, config snapshot, decoder failure and future quarantine semantics acceptable? |
| Data Quality gate | Do raw/normalized authority and projection rules preserve production fact integrity? |
| Verification gate | Is the fixture matrix testable without runtime side effects? |
| PM authorization gate | Has PM explicitly authorized implementation, tests, commit/push or any runtime surface? |

## 8. Current control conclusion

Conclusion: `PASS` for DB-backed API validation harness repair + remote live
validation docs/status reference sync.

Current control status: DB-backed API validation harness repair is CLOSED / PASS
and committed/pushed at `8a8004c`. The repaired remote live DB-backed API
validation rerun is CLOSED / PASS with focused pytest `62 passed in 8.68s` and
test DB cleanup `test_db_cleanup_ok edge_mes_test_api_read`. The latest PM
handoff after DB-backed validation harness repair is committed/pushed at
`5543c87`. The prior DB/API/Dashboard explicit DB opt-in/live local Postgres API
Read Validation Run Planning HOLD Repair is CLOSED / PASS and committed/pushed
at `2cfad5d` after Verification B1 was closed by re-review. The previous PM
handoff after API DB-backed schema verification is committed/pushed at `99dfc26`.
DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only
implementation remains CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed
at `b30db5c`; the prior post-push docs/status sync is committed at `64d0e12`.
The HOLD repair updated
`api/tests/test_accepted_station_events_api_db_backed.py` with API-side
pre-insert schema/constraint/column/nullability verification. The schema
verification runs after migration apply and before fixture insert in the
DB-backed API run path. The harness repair fixed duplicate cursor limit
handling, QueryRecorder false positives and RecordingConnection proxy
completeness including execute delegation. DB-backed API tests remain default
skipped unless a PM-authorized DB opt-in run sets
`EDGE_MES_ENABLE_DB_BACKED_TESTS=1`. This docs/status sync does not authorize a
new DB opt-in rerun, actual timeout failure proof, Dashboard/UI, migration,
Collector runtime changes, Docker / docker compose lifecycle action,
deploy/tag/rollback or real PLC pilot work. The API read path source boundary
remains only `production_accepted_station_event_fact` while preserving the
production-fact visibility boundary. The prior API read path implementation
remains CLOSED / PASS WITH RECOMMENDATIONS at `763b248`; the prior guarded
DB-backed accepted fact tests remain CLOSED / PASS WITH RECOMMENDATIONS at
`636ba37`; and the prior Slice 2 DB write path remains CLOSED / PASS WITH
RECOMMENDATIONS at `299d28a`: accepted decisions may write the production fact
plus legacy/current persistence in one transaction, ACK/read_done mutation
happens only after successful transaction commit, and non-accepted dispositions
create zero production rows and no ACK/read_done mutation for the current
payload. Preserve exact wording: no ACK/read_done mutation for the current
non-accepted payload.

Current PM intake live baseline:

```text
HEAD / origin/main:
5543c877e85c2d77c0a7f67bec1d36d2a206ca76
Latest commit:
5543c87 Add PM handoff after DB-backed validation harness repair
```

Historical authoring baselines in this document, including the E1
`2c73410281d1465db166b66ddc23e27d9337b90a` marker, remain audit markers only.
They must not be read as the current live baseline after later Slice F1/F2/G/H/I,
Slice J, production-fact visibility boundary, PM handoff, adapter leakage tests,
DB schema field-name contract, Slice 1 schema-only migration, Slice 2 DB write
path, guarded DB-backed accepted fact test commits, API read path contract freeze
commit `2d0918a`, API read path implementation commit `763b248`, DB-backed API
read validation tests commit `b30db5c`, handoff commit `b817a9d`, post-push
status sync commit `64d0e12`, API DB-backed schema verification HOLD repair
commit `2cfad5d`, PM handoff commit `99dfc26`, DB-backed API validation harness
repair commit `8a8004c`, or PM handoff commit `5543c87`.

Architecture initial planning: `PASS WITH RECOMMENDATIONS`, no blocker.

Reliability first planning review: `HOLD`, later closed by Architecture planning repair.

Architecture planning repair: `PASS WITH RECOMMENDATIONS`, no blocker.

Reliability planning re-review: `PASS WITH RECOMMENDATIONS`, no blocker.

Data Quality planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

Verification planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

Architecture implementation + focused tests: `PASS WITH RECOMMENDATIONS`, no blocker.

Reliability focused implementation review: `PASS WITH RECOMMENDATIONS`, no blocker.

Data Quality focused implementation review: `PASS WITH RECOMMENDATIONS`, no blocker.

Verification focused implementation review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test planning gate: `PASS TO REVIEW WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Reliability planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Data Quality planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Verification planning review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test implementation: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Reliability implementation review: `HOLD`, later closed by Architecture HOLD repair and Reliability re-review.

Guarded DB-backed accepted fact test HOLD repair: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Reliability HOLD repair re-review: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Data Quality implementation review: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Verification implementation review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

Exact commit gate for guarded DB-backed accepted fact tests: `PASS`.

Exact push gate for guarded DB-backed accepted fact tests: `PASS`.

API read path planning gate: `PASS TO REVIEW WITH RECOMMENDATIONS`, no blocker.

API read path Reliability planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path Data Quality planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path Verification planning review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path contract freeze docs-only edit: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path contract freeze Reliability review: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path contract freeze Data Quality review: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path contract freeze Verification review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

Exact commit/push gate for API read path contract freeze: `PASS`, commit `2d0918a`.

Eligible for docs/status sync closeout decision: closed by this status sync.

D2-A decoder authority docs/contract-only repair: recorded. D2-A adds no code,
tests, config, schema, mapping, runtime Collector integration or raw runtime
wiring. D2-B fixture/test-only hardening is recorded at `dafbbf8`. D2-C minimal
registry/schema implementation is recorded at `5e5a617`. D3 runtime raw wiring
is recorded at `c9e7c22`. E1 runtime raw decoder repair is recorded at
`2c73410` / `2c73410281d1465db166b66ddc23e27d9337b90a`. F1 raw_policy
authority docs/contracts freeze is recorded at `ac1838c`. F2 WS01
station-level raw_policy raw_capable authority is recorded at `829d5c7`. Slice
G WS01 post-commit sanity tests-only hardening is recorded at `398f11c`. Slice H
WS02 station-level raw_policy raw_capable authority is recorded at `c7e80e8`.
Slice I WS03 station-level raw_policy raw_capable authority is recorded at
`045d21c`. Slice J downstream adapter boundary tests-only hardening is recorded
at `ed9a61e` / `ed9a61ef2bd8e6be12ad786fd7846f2efcfb0cad`.

D2-C carry-forward recommendations:

```text
D3 runtime raw wiring remained a separate PM-authorized gate after D2-C and is now closed at c9e7c22.
D2-C PASS alone did not prove runtime raw support; D3 c9e7c22 is the runtime raw wiring closure.
Keep rejected-decision normalized_event/canonical_bytes/fact_key diagnostic-only, not production fact or Quality/Pareto/API-visible state.
Registry failures currently surface as RAW_PARSE_ERROR rather than dedicated decoder-authority public codes; this is non-blocking unless PM opens a future taxonomy gate.
```

D3 carry-forward recommendations:

```text
current config/mapping.yaml runtime default still uses raw_policy: raw_not_provided; D3 runtime code path always passes raw_bytes=data, so this is not a blocker.
If PM later wants runtime source policy explicitly changed to raw_capable/raw_required, it needs a separate mapping/config authority change and review.
Next technical gate should not expand DB/API/Dashboard/V-PLC/storage.py/ACK/deploy without separate PM authorization.
```

E1 carry-forward recommendations:

```text
E1 is closed at 2c73410 as a narrow runtime raw decoder repair after Slice E HOLD.
E1 does not authorize config/mapping.yaml, raw_policy, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy or ACK/read_done ownership changes.
Historical F1/F2/G/H/I gates have since moved WS01, WS02 and WS03 station-level raw_policy to raw_capable while keeping line-wide runtime_defaults.raw_policy as raw_not_provided.
Future raw_required introduction or any line-wide raw_policy default change still requires a separate Level 2 mapping/config authority gate.
Current eligible next step is downstream PM planning, not immediate DB/API/Dashboard/V-PLC/deploy.
```

Slice J downstream planning-only gate: CLOSED / PASS WITH RECOMMENDATIONS.
Slice J tests-only hardening implementation: CLOSED / PASS WITH
RECOMMENDATIONS. Reliability, Data Quality and Verification focused reviews:
PASS WITH RECOMMENDATIONS, no blocker. Focused tests: 80 passed. No production
code changed.

Adapter production-fact leakage negative tests implementation: CLOSED / PASS
WITH RECOMMENDATIONS at `fd3a799`. Reliability, Data Quality and Verification
focused reviews: PASS WITH RECOMMENDATIONS, no blocker. Focused tests: 36 passed
for `collector/tests/test_event_collector_adapter_gate.py` and 46 passed for
`tests/test_collector_station_event_adapter.py`. No production code changed.

DB/API/Dashboard Slice 2 DB write path implementation summary:

```text
Added accepted station-event fact write path for production_accepted_station_event_fact.
Added accepted_station_event_fact.py DTO/helper.
Added Storage.transaction() and no-internal-commit write variants.
Accepted path writes production fact + legacy/current persistence in one transaction.
ACK/read_done mutation happens only after successful transaction commit.
Non-accepted dispositions create zero production rows and no ACK/read_done mutation for the current payload.
Duplicate/conflict/raw_variant/idempotency behavior implemented and tested with focused fake/spy coverage.
No DB migration/API/Dashboard/V-PLC/config/deploy/tag/rollback changes in this slice.
```

Slice 2 validation evidence:

```text
Architecture implementation: collector/tests/test_event_collector_adapter_gate.py -> 36 passed; tests/test_collector_station_event_adapter.py -> 46 passed; collector/tests/test_event_collector_accepted_fact_write_path.py -> 12 passed; compileall collector/app/services -> PASS; git diff --check -> PASS.
Reliability reran focused commands: 36 passed; 46 passed; 12 passed; compileall PASS; git diff --check PASS.
Data Quality combined focused tests: 94 passed.
Verification final audit: 94 passed; compileall PASS; git diff --check PASS; cached empty; exact allowlist PASS.
```

Production-fact visibility boundary preserved:

```text
Future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.
Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
raw_payload/raw_hex is evidence, not a production fact.
Decoded/source normalized payloads remain candidates until accepted.
Non-accepted dispositions do not write defect detail.
NOK/detail visibility must bind to accepted upstream business evidence.
Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
```

Guarded DB-backed accepted fact tests summary:

```text
Commit: 636ba37 / 636ba375248987b26d4ae68bdbf952d47f398bc8.
Changed files: pytest.ini, collector/tests/conftest.py, collector/tests/test_db_backed_safety.py, collector/tests/test_event_collector_accepted_fact_db_backed.py, collector/tests/test_event_collector_accepted_fact_write_path.py, collector/app/services/accepted_station_event_fact.py.
Registered db_backed and postgres_local markers.
DB-backed tests are skipped by default unless EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
Pure-unit safety coverage validates test-target DSN, maintenance/admin DSN, protected DB name rejection, safe DROP DATABASE statement generation, deterministic migration ordering and schema verification query presence without connecting to DB.
DB-backed direct-storage opt-in tests are pytest-discovered but skipped by default; default focused run produced 33 passed, 7 skipped.
station_result NOK missing accepted business NOK evidence now fails closed in build_accepted_station_event_fact() before DB insert.
No DB opt-in tests were run, no DB connection was made and docker compose was not started.
No storage.py, migration 007, API, Dashboard/frontend, V-PLC, config/mapping.yaml, docker-compose.yml, deploy/tag/rollback or docs/status/handoff files changed in the implementation commit.
```

Guarded DB-backed accepted fact carry-forward recommendations:

```text
Future PM-authorized local Postgres harness remains required before claiming worker-level DB-backed accepted rollback, commit failure before ACK, non-accepted DB-backed zero rows + no ACK/read_done mutation, race / unique-violation-after-precheck, or post-unique-violation re-read semantics coverage.
Future DB/API/Dashboard gates must use real production accepted fact table assertions, not synthetic visibility assumptions.
Do not treat legacy/current raw_plc_sample, cycle_event, station_event, production_unit or quality_event as equivalent to production accepted fact surface.
DB opt-in local Postgres execution, API/Dashboard implementation, new migration, V-PLC/PLC pilot, deploy, tag, rollback and broad tests remain not authorized until separate PM gate.
```

API read path contract freeze summary:

```text
Commit: 2d0918a / 2d0918adebe5cd29e59177bc2159c7f447cb5c38.
Changed file: docs/contracts/dashboard_api_contract.md.
Future endpoint contract: GET /api/v2/production/accepted-station-events.
This is a future API contract only and does not claim current implementation.
Source table is limited to production_accepted_station_event_fact; no legacy/current fallback or equivalent production fact source is allowed.
Response fields must come only from production_accepted_station_event_fact; raw/diagnostic/candidate/review/audit/ACK/read_done/collector/Dashboard/Quality/Pareto leakage is forbidden.
Query contract requires bounded start_time/end_time, line_id or explicit server default scope, limit max 500, strict cursor parsing and stable pagination order.
NOK/detail fields must bind accepted upstream business evidence.
Future implementation must preserve no ACK/read_done mutation and no Collector/PLC/runtime side effect.
```

API read path implementation summary:

```text
Commit: 763b248 / 763b248ca835f59096e73aa5e199a4bf903ac946.
Commit message: Implement accepted station events read API.
Changed files: api/app/main.py, api/app/routes/accepted_station_events.py, api/tests/test_accepted_station_events_api.py.
Endpoint implemented: GET /api/v2/production/accepted-station-events.
Source table remains limited to production_accepted_station_event_fact; no legacy/current fallback or equivalent production fact source is allowed.
Response fields come only from production_accepted_station_event_fact and remain limited to the frozen DTO allowlist.
Query validation requires line_id, bounded start_time/end_time, strict timezone-aware ISO parsing, default limit 50, max limit 500 and fail-closed invalid limit/time/window behavior.
Cursor is HMAC signed, schema/version checked and binds line_id, start_time, end_time, limit, direction and ordering tuple; stable order is event_ts ASC, accepted_at ASC, fact_key ASC.
Read safety uses BEGIN READ ONLY, statement_timeout, idle_in_transaction_session_timeout, SELECT-only query and no write-path helper reuse.
NOK/detail fields are returned only from accepted fact row fields and must bind accepted upstream business evidence.
Focused validation: PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py -> 27 passed; git diff --check PASS.
Reliability implementation review: PASS WITH RECOMMENDATIONS, no blocker.
Data Quality implementation review: PASS WITH RECOMMENDATIONS, no blocker.
Verification implementation review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker.
api/app/db.py was not changed.
DB opt-in/local Postgres execution, new migration, storage.py, collector changes, Dashboard/frontend/Grafana, V-PLC, Docker/deploy/tag/rollback and broad tests remain unauthorized.
```

API read path implementation carry-forward recommendations:

```text
Before production deploy, ACCEPTED_STATION_EVENTS_CURSOR_SECRET must be managed as a real deployment secret rather than relying on the development fallback.
Future DB-backed/live Postgres API read validation remains separate PM-authorized work; this implementation was validated with focused mocked/stubbed API tests only and does not claim live schema/runtime coverage.
work_order/product remain excluded until a later schema/contract gate.
```

DB-backed/live Postgres API Read Validation tests-only implementation and explicit DB opt-in/live local Postgres run planning HOLD repair summary:

```text
Implementation commit: b30db5c / b30db5cd2bd1d109d83c8da1a222d5ad37517448.
Implementation post-push docs/status sync commit: 64d0e12 / 64d0e12dc76898a2da3ce09c2c0e94dbbf33ac80.
HOLD repair commit: 2cfad5d / 2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e.
Previous PM handoff commit: 99dfc26 / 99dfc265983d757de7c23f6a677cabbc05bc4f5a.
Harness repair commit: 8a8004c / 8a8004c53f5bca871610807ae1ec99650e759127.
Latest PM handoff commit: 5543c87 / 5543c877e85c2d77c0a7f67bec1d36d2a206ca76.
Commit message for implementation: Add DB-backed API read validation tests.
Commit message for HOLD repair: Add API DB-backed schema verification.
Commit message for harness repair: Fix DB-backed API validation harness.
Changed file: api/tests/test_accepted_station_events_api_db_backed.py.
The implementation added only api/tests/test_accepted_station_events_api_db_backed.py.
The HOLD repair added API-side pre-insert schema/constraint/column/nullability verification for production_accepted_station_event_fact.
The schema verification checks table existence, DTO/accepted fact columns, nullable / NOT NULL expectations, unique constraints and accepted-fact check constraints.
The schema verification runs after migration apply and before fixture insert in the live DB-backed execution path.
The harness repair fixed duplicate cursor limit handling, QueryRecorder false positives and RecordingConnection proxy completeness including execute delegation.
DB-backed API tests remain default skipped unless a PM-authorized DB opt-in run sets EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
Default non-DB focused run before HOLD repair: PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py api/tests/test_accepted_station_events_api_db_backed.py -q -> 27 passed, 32 skipped.
HOLD repair focused GREEN run: 41 passed, 19 skipped.
Collector DB safety focused run after HOLD repair: 20 passed.
git diff --check -> PASS in implementation and HOLD repair gates.
Harness repair default-safe focused tests: local 43 passed, 19 skipped; remote 43 passed, 19 skipped.
Remote live DB-backed API validation rerun after harness repair: 62 passed in 8.68s.
Remote live DB-backed API validation cleanup: test_db_cleanup_ok edge_mes_test_api_read.
DB-backed API validation execution rerun after focused repair: 88 passed in 12.94s.
DB-backed API validation rerun cleanup: no explicit cleanup line printed in terse `-q` output; no pytest teardown/cleanup error reported.
DB-backed API validation post-execution docs/status sync: PASS at ba02249 / ba0224972f18e097307310039c27f29259b3a0cc.
Dashboard/API implementation planning gate: CLOSED / PASS WITH RECOMMENDATIONS at 4fcdd66 / 4fcdd6623247aaf9d3d3df23fd7cadf49f5d662a.
Dashboard/API implementation planning report changed file: docs/reports/sprint3_dashboard_api_implementation_plan.md.
Dashboard/API implementation planning Architecture / Integration, Reliability, Data Quality and Verification focused planning reviews: CLOSED / PASS WITH RECOMMENDATIONS with no blockers.
Dashboard/API implementation planning carry-forward recommendations: convert category-level future Dashboard implementation allowlist into exact file paths before implementation authorization; add invalid / expired / cross-scope cursor UI negative tests; keep page-level summary labelled as current page only; keep future implementation Dashboard-only/read-only unless PM opens a separate API/contract gate. The former stale-prior-data carry-forward is CLOSED by `156a812` and `963218a`.
Dashboard implementation preparation / allowlist gate: CLOSED / PASS WITH RECOMMENDATIONS at 4ad0e91 / 4ad0e91b41c4595295140d32b6bc96aa41f81b35.
Dashboard accepted-events frontend implementation: CLOSED / PASS WITH RECOMMENDATIONS at 896c2d1 / 896c2d159ce9c934c53f62607d93475d5fffd681.
Dashboard accepted-events frontend Reliability review chain: initial HOLD B1/B2 repaired and CLOSED by re-review / PASS WITH RECOMMENDATIONS.
Dashboard accepted-events frontend Data Quality review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Dashboard accepted-events frontend Verification review chain: initial HOLD V-B1 repaired and CLOSED by re-review / PASS WITH RECOMMENDATIONS.
Dashboard accepted-events vertical validation planning: CLOSED / PASS WITH RECOMMENDATIONS at dd6dc53 / dd6dc53627c6e27b5ff206096a91d77dd76d4d23.
Dashboard accepted-events vertical validation planning review chain: Reliability PASS WITH RECOMMENDATIONS; Data Quality PASS WITH RECOMMENDATIONS; Verification initial HOLD B1/B2/B3; Architecture HOLD repair PASS WITH RECOMMENDATIONS; Verification re-review PASS WITH RECOMMENDATIONS, B1/B2/B3 CLOSED.
Dashboard accepted-events frontend validation evidence: npm ci PASS; npm test PASS, 9 files / 24 tests; npm run typecheck PASS; npm run build PASS; generated artifacts cleaned; git diff --check -- frontend PASS.
Dashboard accepted-events no-DB vertical validation execution: CLOSED / PASS WITH RECOMMENDATIONS at b413876 / b41387661d62f33971d39e83ec89152c0500e859 after four focused frontend commands produced 4 files / 19 tests passed and Reliability, Data Quality and Verification reviews closed with PASS WITH RECOMMENDATIONS.
PM handoff after Dashboard no-DB validation sync: PASS at c103e90 / c103e90eddd2252cd6f8d085f055de13e5584578.
Dashboard accepted-events apiClient focused no-DB tests: planning CLOSED / PASS WITH RECOMMENDATIONS; implementation CLOSED / PASS; Reliability CLOSED / PASS; Data Quality CLOSED / PASS WITH RECOMMENDATIONS; Verification CLOSED / PASS WITH RECOMMENDATIONS; exact-path commit/push PASS at 96c0928 / 96c0928970d9917e0a4142569ebbc8459d67cc3d.
apiClient focused no-DB tests changed only five frontend test files: frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts, frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts, frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts, frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts and frontend/src/app/accepted-events/__tests__/page.test.tsx.
apiClient focused no-DB test evidence: apiClient.test.ts 7 passed, query.test.ts 12 passed, schema.test.ts 26 passed, viewModel.test.ts 3 passed and page.test.tsx 8 passed.
Dashboard accepted-events nested/renamed leakage defense-in-depth fixture: implementation CLOSED / PASS; Reliability CLOSED / PASS WITH RECOMMENDATIONS; Data Quality CLOSED / PASS WITH RECOMMENDATIONS; Verification CLOSED / PASS WITH RECOMMENDATIONS; exact-path commit/push PASS at 244a6dd / 244a6dd82b294f695aaf2bf6a6a849d7ad94dcb6.
Nested/renamed leakage fixture changed only frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts and frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts. Evidence: schema.test.ts 49 passed, viewModel.test.ts 4 passed and exact two-file git diff --check PASS. Its former strict parser carry-forward is CLOSED by the exact-envelope/required-key-null contract repair and implementation commit 2cf616d.
Reliability implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Data Quality implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Verification implementation review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Explicit DB opt-in/live local Postgres API Read Validation Run Planning Gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Planning Reliability Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Planning Data Quality Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Planning Verification Review / Exact Future Run Allowlist Audit: CLOSED / HOLD, blocker B1.
HOLD repair: CLOSED / PASS, no blocker.
HOLD repair Verification re-review: CLOSED / PASS WITH RECOMMENDATIONS, B1 CLOSED.
EDGE_MES_ENABLE_DB_BACKED_TESTS=1 was set only in separately authorized DB-backed execution gates.
The authorized remote validation used loopback DSNs only, created/dropped isolated edge_mes_test_api_read, applied existing migrations, verified schema, inserted fixtures and completed API live DB read assertions. The later SSH-tunnel rerun used masked loopback DSNs with Mac `localhost:5433` tunneling to Pi `localhost:5432` and target database `edge_mes_test_api_read`.
Docker / docker compose lifecycle actions were not performed.
Live DB validation has completed for this focused DB-backed API validation harness lane and the later focused DB-backed API rerun lane.
Actual timeout failure proof has not completed.
Do not claim actual timeout failure proof completed.
Current tests prove timeout statements / read behavior and schema verification in the focused DB-backed API validation lane; they do not prove actual timeout failure induction.
```

DB-backed/live Postgres API Read Validation carry-forward recommendations:

```text
This focused remote live DB-backed API validation lane and the later focused SSH-tunnel DB-backed API validation rerun lane are CLOSED / PASS; future DB-backed reruns still require separate PM authorization before executing EDGE_MES_ENABLE_DB_BACKED_TESTS=1, connecting to Postgres, creating/dropping a temp DB, applying migrations against live DB or inserting fixtures into live DB.
Future actual timeout failure induction remains a separate PM-authorized gate; timeout setting verification alone is not actual timeout failure proof.
DB/API/Dashboard consumer planning gate is CLOSED / PASS WITH RECOMMENDATIONS at f4de1c3.
DB/API/Dashboard API consumer contract freeze gate is CLOSED / PASS WITH RECOMMENDATIONS at f65a120; changed file: docs/contracts/dashboard_api_contract.md.
DB/API/Dashboard API implementation planning gate is CLOSED / PASS WITH RECOMMENDATIONS at 2dc4b4d; changed file: docs/reports/sprint3_api_consumer_implementation_plan.md.
DB/API/Dashboard accepted station events API implementation is CLOSED / PASS WITH RECOMMENDATIONS at 97dc4d5; changed files: api/app/routes/accepted_station_events.py and api/tests/test_accepted_station_events_api.py.
Dashboard/API implementation planning gate is CLOSED / PASS WITH RECOMMENDATIONS at 4fcdd66; changed file: docs/reports/sprint3_dashboard_api_implementation_plan.md.
Dashboard implementation preparation / allowlist gate is CLOSED / PASS WITH RECOMMENDATIONS at 4ad0e91.
Dashboard accepted-events frontend implementation is CLOSED / PASS WITH RECOMMENDATIONS at 896c2d1.
Dashboard accepted-events vertical validation planning is CLOSED / PASS WITH RECOMMENDATIONS at dd6dc53.
API consumer contract freeze, API implementation planning, API implementation, DB-backed API validation rerun, Dashboard/API implementation planning, Dashboard implementation preparation / allowlist, Dashboard accepted-events frontend Reliability/Data Quality/Verification focused reviews and Dashboard accepted-events vertical validation planning Reliability/Data Quality/Verification reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers after the documented HOLD repairs.
Dashboard accepted-events no-DB vertical validation execution, Dashboard accepted-events apiClient focused no-DB tests, Dashboard accepted-events nested/renamed leakage defense-in-depth fixture, Dashboard accepted-events strict parser fail-closed hardening, the all-22-field explicit-null regression tests-only gate, the UI/state stale-data planning/tests-only gate and the frontend typecheck/build planning/execution gate are now closed. Strict parser planning, contract authority, implementation, Reliability/Data Quality/Verification reviews, docs authority commit/push, implementation commit/push, prior post-push docs/status sync, PM handoff, explicit-null regression commit/push, stale-data commits `156a812` / `963218a`, typecheck/build planning authority `2a88ffe` and commands-only Verification execution are CLOSED. The former optional all-fields explicit-null, stale-prior-data and current-baseline typecheck/build recommendations are closed. The next eligible branch is exact-path commit/push of this three-file docs/status sync after separate PM authorization, PM handoff if thread/context is long, or separately planned browser/manual smoke, API no-DB or API DB-backed validation.
Future DB-backed API validation rerun planning must freeze exact DB opt-in scope, DSN/test DB safety, schema/migration verification, allowed tests, cleanup and EDGE_MES_ENABLE_DB_BACKED_TESTS=1 usage before execution.
Worker/runtime DB-backed gates for unique-violation race, commit-before-ACK, non-accepted DB-backed zero-row/no ACK/read_done mutation, post-conflict re-read semantics and DB rollback remain future authorized work.
API read path source boundary remains only production_accepted_station_event_fact; raw_plc_sample, cycle_event, station_event, production_unit, quality_event, production_snapshot and production_events must not be described as equivalent production fact sources, fallback sources or join-derived field fillers.
Future production visibility remains limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.
Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
raw_payload/raw_hex is evidence, not a production fact.
Decoded/source normalized payloads remain candidates until accepted.
Non-accepted dispositions do not write defect detail.
NOK/detail visibility must bind to accepted upstream business evidence.
Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
Deploy/tag/rollback/real PLC pilot require separate PM authorization.
```

Current closed state: Dashboard accepted-events strict parser fail-closed
hardening, the all-22-field explicit-null regression tests-only gate, UI/state
stale-data planning/tests-only work and frontend typecheck/build planning/execution
are completed and must not be re-described as future implementation, test or
validation recommendations. The former stale-prior-data carry-forward is CLOSED
by `156a812` and `963218a`; the current-baseline typecheck/build recommendation is
CLOSED by planning authority `2a88ffe` and the completed commands-only
Verification execution. Remaining separately planned validation gates are
browser/manual smoke, API no-DB validation and API DB-backed validation.

Eligible for next PM gate: exact-path commit/push of this three-file docs/status
sync after separate PM authorization, then PM handoff may be considered if
thread/context is long. Browser/manual smoke, API no-DB/API DB-backed validation,
DB-backed reruns and actual timeout failure induction remain separate future
PM-authorized gates.

Eligible for implementation without PM approval: no. PM approval is required
before DB-backed API validation planning/execution, Dashboard implementation
expansion, optional debug/review diagnostics view,
future DB-backed reruns, EDGE_MES_ENABLE_DB_BACKED_TESTS=1 outside an approved
gate, Docker / docker compose lifecycle actions, tests beyond the authorized gate
scope, new migration, V-PLC/PLC pilot, storage/API/contract/DB/runtime expansion, deploy, tag,
rollback, broad tests, real PLC pilot, commit/push or any change outside the
approved docs allowlist.
