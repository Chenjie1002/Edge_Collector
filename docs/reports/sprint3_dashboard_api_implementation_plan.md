# Sprint 3 Dashboard/API implementation planning gate report

Date: 2026-07-06
Thread: Architecture / Integration
Status: PASS WITH RECOMMENDATIONS

This gate is planning only. It does not authorize Dashboard/frontend
implementation, API changes, DB schema changes, DB-backed execution, Postgres
connections, Docker / docker compose lifecycle actions, broad pytest, staging,
commit, push, deploy, tag, rollback or real PLC pilot work.

## 1. Report identity

报告名称：
Sprint 3 Dashboard/API implementation planning gate report

任务名称：
Sprint 3 Dashboard/API implementation planning gate

执行 Thread：
Architecture / Integration

结论：
PASS WITH RECOMMENDATIONS

Rationale: live Git matches the PM baseline, the required DB-backed API
validation rerun gate is closed, the known external artifacts are excluded, and
the minimal Dashboard/API consumer implementation can be planned without
touching code, API contract, DB schema, tests or status files.

## 2. Read-only recovery summary

Read-only recovery was performed before this planning edit.

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
ba02249 Sync DB-backed API validation rerun status
a0042fb Add PM handoff after DB-backed repair
1d040a6 Align DB-backed API failure assertion
78ce29b Plan DB-backed API validation
1012d71 Add PM handoff after API implementation closeout
029a735 Sync accepted station events API status
97dc4d5 Harden accepted station events API contract
2dc4b4d Add API consumer implementation planning

git log -1 --format='%H %s':
ba0224972f18e097307310039c27f29259b3a0cc Sync DB-backed API validation rerun status

git rev-parse origin/main:
ba0224972f18e097307310039c27f29259b3a0cc

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
ba0224972f18e097307310039c27f29259b3a0cc`, matching the PM-provided baseline.
The dirty working tree contains only the known external artifacts before this
planning file was added. No cached changes were present.

## 3. Scope

Reviewed files:

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_api_consumer_implementation_plan.md`
- `docs/reports/sprint3_db_api_dashboard_consumer_plan.md`

Changed files:

- `docs/reports/sprint3_dashboard_api_implementation_plan.md`

Explicitly not touched:

- `.gitignore`
- `docs/current_status.md`
- `docs/contracts/dashboard_api_contract.md`
- API route files
- Dashboard/frontend files
- tests
- DB migrations / schema files
- runtime / collector / storage files
- README
- PM handoff files
- all untracked external artifacts listed in the read-only recovery summary

## 4. Current gate basis

The current branch is eligible for this planning gate because:

- DB-backed API validation execution rerun is CLOSED / PASS WITH
  RECOMMENDATIONS with focused pytest `88 passed in 12.94s`.
- DB-backed API validation post-execution docs/status sync is committed and
  pushed at `ba02249`.
- DB/API/Dashboard consumer planning, API consumer contract freeze, API
  implementation planning, accepted station events API implementation and
  DB-backed API validation planning/repair/rerun are closed.
- The next eligible branch is Dashboard/API implementation planning as a
  separate Level 2 planning branch after explicit PM authorization.

This planning gate does not claim live DB validation beyond the already closed
DB-backed API validation rerun. It does not claim actual timeout failure
induction proof.

## 5. Minimal Dashboard page / component scope

Future Dashboard implementation should start with one read-only production
consumer page backed only by:

- endpoint: `GET /api/v2/production/accepted-station-events`
- production fact source: `production_accepted_station_event_fact`

Minimum page/component set:

| Page / component | Purpose | Allowed consumed fields | Required non-happy states |
| --- | --- | --- | --- |
| Accepted events page shell | Provides bounded line/time query state and pagination controls | `line_id`, `event_ts`, `accepted_at`, `fact_key` | loading, empty, error, unavailable |
| Accepted events table | Lists accepted station-event facts at row grain | DTO allowlist in section 9 only | loading rows, empty rows, invalid query message, source unavailable message |
| Station/result summary strip | Computes client-side counts from the returned page only, not global totals | `station_id`, `station_type`, `event_type`, `production_result` | incomplete/page-limited label, empty state |
| NOK/detail evidence panel | Shows accepted NOK/detail evidence for the selected accepted fact row | `production_result`, `nok_code`, `nok_origin`, `nok_detail_code`, `nok_detail_source_event_id`, `nok_detail_evidence_fact_key`, `fact_key`, `source_event_id` | absent evidence, unknown detail, unavailable source |
| Trace reference panel | Shows accepted fact identity and trace references only | `unit_id`, `dmc`, `cycle_counter`, `source_event_id`, `event_ts`, `accepted_at`, `fact_key`, `content_fingerprint`, line/PLC/station/profile/config fields | missing unit/DMC, partial trace fields |

Out of the first implementation slice:

- OEE denominator synthesis;
- Quality/Pareto charts;
- work order / product display;
- raw payload or raw hex viewer;
- debug/review diagnostics view;
- collector health, ACK/read_done or PLC control status;
- DB-backed execution or schema verification UI.

## 6. API consumer data flow

Planned read-only flow:

```text
Dashboard route state
-> query model: line_id, start_time, end_time, limit, cursor
-> GET /api/v2/production/accepted-station-events
-> response envelope validation against DTO allowlist
-> page-level render model built only from response data.items[] and page
-> components render accepted fact rows, page-level counts and selected-row evidence
```

Consumer code must not read from DB tables directly and must not call any other
production, trace, quality, raw, station, summary or diagnostics endpoint to
fill this page.

Derived client-side values allowed in this first slice:

- page-local count by `production_result`;
- page-local count by `station_id`;
- visible page range and `next_cursor` state;
- selected accepted fact row display state.

Derived values forbidden in this first slice:

- line-wide OEE/A/P/Q;
- schedule/runtime denominator values;
- global quality rate or Pareto;
- production totals beyond the returned page;
- synthetic defect/detail values;
- stale collector status from `accepted_at`;
- any fallback-filled value from legacy/current/raw/diagnostic surfaces.

## 7. Endpoint and query parameter boundary

The only allowed endpoint is:

- `GET /api/v2/production/accepted-station-events`

The first Dashboard/API consumer implementation may send only these query
parameters:

- `line_id`
- `start_time`
- `end_time`
- `limit`
- `cursor`

Boundary rules:

- `line_id` is required from Dashboard state unless a future PM-authorized gate
  establishes an explicit audited single-line default; the consumer should not
  make implicit cross-line requests.
- `start_time` and `end_time` are required and must be timezone-aware
  ISO-8601 strings.
- `limit` should default to 50; max accepted contract value is 500. The UI
  should offer only bounded choices such as 25, 50, 100, 250 and 500.
- `cursor` must be treated as opaque. Dashboard must not decode, mutate,
  persist as authority or construct cursor payloads.
- Unsupported query params must not be sent by this first slice.

## 8. Time window and timezone handling

Dashboard state should separate:

- display timezone: operator-facing timezone label and formatted timestamps;
- API query instants: ISO-8601 timezone-aware `start_time` / `end_time`;
- API response instants: `event_ts` and `accepted_at` displayed as instants,
  not collector freshness, ACK time, station freshness or read_done time.

Planning decisions:

- Default UI window proposal: recent 8 hours, aligned to the selected display
  timezone, then converted to timezone-aware ISO-8601 instants for the API
  request.
- Maximum UI selectable window: 31 days, matching the current contract.
- The UI must fail closed before request for missing start/end, invalid time,
  inverted range or range greater than 31 days.
- Server 4xx for invalid or over-large windows must render as invalid query,
  not as empty production truth.
- Empty response within a valid window means no accepted facts in that bounded
  scope, not line stopped, collector stale or quality OK.

## 9. DTO field allowlist

Dashboard production consumer code may read only:

```text
line_id
plc_id
station_id
station_type
profile_id
config_hash
config_version
event_type
production_result
unit_id
dmc
cycle_counter
source_event_id
event_ts
accepted_at
fact_key
content_fingerprint
nok_code
nok_origin
nok_detail_code
nok_detail_source_event_id
nok_detail_evidence_fact_key
```

Every field must be treated as sourced from
`production_accepted_station_event_fact` through the accepted-station-events API
DTO. Fallback is forbidden for every field.

`work_order` and `product` remain excluded until a later schema/contract
authority gate.

## 10. Pagination behavior

Dashboard pagination must be cursor-forward and API-owned:

- initial request sends no `cursor`;
- next-page request sends the returned `page.next_cursor` unchanged;
- changing `line_id`, `start_time`, `end_time` or `limit` clears cursor and
  starts a new first-page request;
- `next_cursor == null` disables next-page action;
- cursor errors render as invalid or expired page state and require restarting
  at page 1 with the current filters;
- the UI must not infer total count from page length or cursor absence;
- the UI must not construct previous-page cursors unless a future contract
  explicitly authorizes backward pagination.

## 11. Loading / empty / error / unavailable states

The first Dashboard/API slice must distinguish:

| State | Trigger | Required display semantics |
| --- | --- | --- |
| Loading | request in flight | keep prior committed data visually distinct from loading state; do not show stale data as fresh |
| Empty | successful response with zero `data.items[]` for a valid bounded query | "no accepted facts in this scope"; not a health, quality or production-good claim |
| Invalid query | client validation failure or server 4xx for invalid time/window/limit/cursor | explain that query bounds must be corrected; do not widen silently |
| Error | non-4xx unexpected response or malformed DTO envelope | block production interpretation; show retry affordance |
| Unavailable | API reports accepted fact source unavailable / DB unavailable / missing table / missing schema / missing authority | show source unavailable/unknown; never fallback to legacy/raw/current/diagnostic sources |
| Partial / page-limited | response page is valid but not all matching rows are loaded | label page-level aggregates as current page only |

## 12. NOK / detail evidence boundary

NOK/detail display is allowed only from accepted fact DTO fields:

- `production_result`
- `nok_code`
- `nok_origin`
- `nok_detail_code`
- `nok_detail_source_event_id`
- `nok_detail_evidence_fact_key`
- `fact_key`
- `source_event_id`

Rules:

- If `production_result` is not NOK-like or NOK/detail fields are null, the UI
  must show absent/unknown detail rather than synthesizing detail.
- NOK/detail fields must not be filled from adapter reason code, raw mismatch,
  decoder error, diagnostic context, non-accepted disposition or Quality/Pareto
  helpers.
- `nok_detail_source_event_id` and `nok_detail_evidence_fact_key` are evidence
  references only, not authorization to fetch raw/debug payloads in this slice.

## 13. Forbidden leakage negative checklist

Future implementation and focused tests should prove the Dashboard production
consumer does not import, render, log as production state, derive from or query:

- `raw_payload`, `raw_hex`, `raw_sample_id` or raw bytes;
- decoded/source normalized candidate payloads before accepted decision;
- adapter disposition, adapter reason, adapter phase or candidate context;
- raw/normalized comparison context;
- decoder errors;
- diagnostic/review/audit payloads;
- `ack_status`, `read_done` or `collector_state`;
- `quality_pareto_input` or `dashboard_state`;
- bare `result`, `defect`, `quality` or `pareto` production-looking keys;
- `work_order` or `product`;
- legacy/current fallback sources:
  `raw_plc_sample`, `cycle_event`, `station_event`, `production_unit`,
  `quality_event`, `production_snapshot`, `production_events`;
- any non-accepted disposition as a production fact.

## 14. No-side-effect boundary

Dashboard/API consumer implementation must remain read-only:

- no DB connection from Dashboard/frontend code;
- no `INSERT`, `UPDATE`, `DELETE` or migration;
- no API route changes unless PM separately authorizes an API implementation
  gate;
- no ACK/read_done mutation;
- no Collector, PLC, V-PLC, runtime, storage.py, config or Docker side effect;
- no deploy/tag/rollback/real PLC pilot action;
- no broad pytest or DB-backed execution in this planning gate.

Preserve exact downstream boundary: no ACK/read_done mutation for the current
non-accepted payload.

## 15. Future implementation allowlist proposal

Candidate allowlist for a later PM-authorized Dashboard/API implementation
gate:

- Dashboard route/page file for the accepted events page.
- Dashboard API client module for
  `GET /api/v2/production/accepted-station-events`.
- Dashboard DTO/schema validation module for the accepted fact allowlist.
- Dashboard component files for accepted events table, query controls,
  page-local summary strip, selected-row NOK/detail evidence and trace
  reference panel.
- Focused Dashboard tests for query construction, state rendering, DTO
  allowlist, forbidden leakage and no-side-effect behavior.

Files intentionally excluded from the default future allowlist:

- `api/app/routes/accepted_station_events.py`
- `api/app/main.py`
- `api/app/db.py`
- `api/tests/test_accepted_station_events_api.py`
- `api/tests/test_accepted_station_events_api_db_backed.py`
- DB migrations / schema files
- Collector/runtime/storage.py
- config/mapping.yaml
- Docker / docker compose files
- optional debug/review diagnostics view files
- README, PM handoff and status files unless PM later gives exact-path docs
  sync authorization

If the future Dashboard implementation discovers that the existing endpoint or
contract is insufficient, it should stop and report HOLD or request a separate
API/contract authority gate; it must not modify API or contract files inside
the Dashboard consumer slice by default.

## 16. Focused test plan proposal

Future tests should be non-DB by default and limited to Dashboard/API consumer
behavior unless PM separately authorizes API, DB-backed or broad tests.

Proposed focused coverage:

| Test area | Required assertions |
| --- | --- |
| Query construction | sends only `line_id`, `start_time`, `end_time`, `limit`, `cursor`; clears cursor when scope/time/limit changes |
| Time/window validation | rejects missing, invalid, inverted or >31 day ranges before request |
| Timezone display | formats `event_ts` and `accepted_at` in the selected display timezone while preserving API instants |
| Pagination | treats cursor as opaque, sends returned cursor unchanged, disables next when null |
| DTO allowlist | accepted row model contains only section 9 fields |
| Forbidden leakage | fixture payloads containing raw/debug/diagnostic/legacy fields do not render or enter production model |
| Loading/empty/error/unavailable | distinct render states with no fallback or stale-as-fresh display |
| NOK/detail evidence | uses only accepted NOK/detail DTO fields and shows absent/unknown when missing |
| No side effect | consumer code does not import DB clients, API route modules, Collector/runtime/storage modules or Docker/deploy helpers |

Execution proposal for the later implementation gate:

- run only the focused Dashboard unit/component tests relevant to changed files;
- run type/lint/build command only if already standard for the Dashboard package
  and scoped to the frontend;
- do not run broad pytest;
- do not run DB-backed tests;
- do not set `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`;
- do not connect to Postgres.

## 17. Review handoff questions

Reliability review questions:

- Does the Dashboard consumer preserve API read-only semantics and avoid DB,
  Collector, PLC, V-PLC, runtime, storage, ACK/read_done and Docker side
  effects?
- Are loading/error/unavailable states clear enough to prevent stale or
  unavailable accepted fact data from being interpreted as fresh production
  truth?
- Does pagination keep cursor opaque and fail closed when scope changes or the
  cursor is invalid?
- Are client-side query bounds sufficient to avoid widening invalid requests?

Data Quality review questions:

- Does every displayed field map to the accepted fact API DTO allowlist and no
  other source?
- Are page-level counts clearly marked as page-local rather than line-wide
  production totals?
- Does NOK/detail visibility bind only to accepted NOK/detail evidence fields?
- Are `accepted_at`, `event_ts`, `fact_key`, `content_fingerprint` and
  `source_event_id` presented with the correct meaning and no freshness or
  mutation authority?
- Are `work_order` and `product` still excluded?

Verification review questions:

- Is the future implementation allowlist exact enough for PM authorization?
- Do tests cover DTO allowlist, forbidden leakage, query params, time/window,
  timezone display, pagination, loading/empty/error/unavailable states and
  no-side-effect assertions?
- Does the test plan avoid broad pytest, DB-backed execution, Postgres, Docker,
  API route edits and status/contract edits?
- Are external dirty artifacts excluded from any future stage/commit path?

## 18. Blockers

None for this planning gate.

## 19. Recommendations

- Keep the next implementation slice Dashboard-only and read-only, using the
  existing accepted-station-events endpoint as-is.
- Require PM exact-path authorization before any Dashboard/frontend edit.
- If endpoint behavior or contract wording appears insufficient during
  implementation, stop and open a separate API/contract gate instead of mixing
  API changes into the Dashboard consumer branch.
- Carry forward a focused leakage-negative test matrix for raw/debug/diagnostic
  fields, legacy source fallback, NOK/detail synthesis and no-side-effect
  imports.
- Treat page-level summaries as current-page indicators only until a separate
  summary/aggregation contract exists.

## 20. Next gate

Eligible for:

- Reliability focused planning review.
- Data Quality focused planning review.
- Verification focused planning review / exact future Dashboard implementation
  allowlist audit.

PM approval required before:

- Dashboard/frontend implementation;
- API route or contract modification;
- DB migration or schema change;
- tests, especially broad pytest or DB-backed tests;
- Postgres connection or `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`;
- Docker / docker compose;
- stage, commit or push;
- deploy, tag, rollback or real PLC pilot.

## 21. Thread output / context assessment

本次输出长度：中

当前 Thread 是否建议继续：no

下一轮是否建议新开 Thread：yes

理由：本 Thread 已完成 Dashboard/API implementation planning gate 的 durable
planning artifact。下一步应进入 Reliability / Data Quality / Verification
focused planning reviews，或在 PM 明确授权后进入新的 Dashboard implementation
Thread。继续在当前 Thread 执行实现容易把 planning-only 上下文误扩展为
implementation authorization。
