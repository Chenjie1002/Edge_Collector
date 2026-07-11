# Sprint 3 Dashboard accepted-events exact envelope contract clarification report

Date: 2026-07-10

报告名称：
Sprint 3 Dashboard accepted-events exact envelope contract clarification report

任务名称：
Clarify accepted-station-events endpoint-specific exact response envelope

执行 Thread：
Architecture / Integration

风险等级：
Level 2 — docs-only contract clarification

结论：PASS

## Baseline

- HEAD: `885a09423997f9dfc3ad597607509fb37372717e`
- origin/main: `885a09423997f9dfc3ad597607509fb37372717e`
- latest commit: `885a094 Add PM handoff after leakage fixture closeout`
- cached diff: empty
- read-only recovery decision: committed baseline matches the PM-provided expected baseline. Existing dirty state is limited to the listed external exclusions and the authorized prior untracked planning artifact `docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md`.

## Reviewed files

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260710-1659.md`
- `docs/current_status.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`
- `docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`
- `frontend/src/lib/acceptedStationEvents/schema.ts`
- `frontend/src/lib/acceptedStationEvents/apiClient.ts`
- `api/app/routes/accepted_station_events.py`

## Changed files

- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_accepted_events_envelope_contract_clarification_report.md`

## Explicitly not touched

- `docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md`
- `docs/current_status.md`
- `docs/thread_handoff/**`
- `frontend/**`
- `api/**`
- `common/**`, `collector/**`, `tests/**`, `docker*`, `package*.json`, `.gitignore`
- all listed external dirty artifacts, including `frontend/node_modules/`

## Previous blockers

- B1: CLOSED. The contract now states that endpoint-specific exact response envelopes override the generic Envelope, and that this endpoint does not inherit generic `meta`.
- B2: CLOSED. The endpoint exact outer/data/page keys are frozen as `{data, page}`, `{items}`, and `{next_cursor, limit}`; `data` and `page` are required.
- B3: CLOSED. Unsupported envelope/data/page/item keys in a 2xx response are explicitly classified as malformed successful responses and must fail closed as client `kind: "error"`.

## Contract decision

- generic envelope precedence rule: the generic response Envelope remains the default; an endpoint-specific declared exact response envelope takes precedence.
- endpoint exact outer keys: required and only `data`, `page`.
- endpoint exact data keys: required and only `items`.
- endpoint exact page keys: required and only `next_cursor`, `limit`.
- meta decision: `meta` is unsupported for this endpoint; it does not inherit generic `meta`, and no `meta` schema is introduced.
- malformed 2xx classification: an unsupported envelope/data/page/item key is a malformed successful response; consumer parser must fail closed and Dashboard client classification is `kind: "error"`, not `invalid-query` or `unavailable`.

## Compatibility assessment

- current API route compatible: yes; it currently returns only `data` and `page` with the frozen nested shapes.
- current endpoint example compatible: yes; it remains the normative accepted shape.
- API change required: no.
- frontend implementation performed: no.
- production authority changed: no; `production_accepted_station_event_fact`, the existing DTO item allowlist, accepted fact/NOK/detail boundaries, and `accepted_at` semantics are unchanged.

## Exact diff assessment

Only the exact two-file allowlist is changed/created by this gate: the contract is modified and this clarification report is new. No API route, response producer, query parameter, cursor, DTO item allowlist, production authority, raw/debug/diagnostic/candidate surface, accepted fact/NOK/detail, or `accepted_at` semantic is changed. The pre-existing strict-parser planning report remains unmodified.

## Validation performed

- Required read-only Git recovery completed before editing.
- No frontend/API tests, typecheck, build, browser/manual smoke, server/runtime, DB/Postgres or Docker command was run.
- `git diff --check -- docs/contracts/dashboard_api_contract.md docs/reports/sprint3_dashboard_accepted_events_envelope_contract_clarification_report.md`: PASS.
- `git diff -- docs/contracts/dashboard_api_contract.md`: reviewed; change is limited to generic-vs-endpoint-specific precedence and the accepted-station-events exact envelope/fail-closed semantics.
- `git diff --name-only`: only the pre-existing `.gitignore` and this gate's tracked contract modification are listed; the new report is verified directly because it is untracked.
- `git diff --cached --name-only`: empty.
- `git status --short --untracked-files=all`: confirms the modified contract, this new report, the authorized prior strict-parser planning report and the stated external exclusions; no staged file.
- Direct read plus targeted `rg` assertions confirmed the precedence rule, exact envelope section, `meta` prohibition, malformed 2xx → client `kind: "error"`, and all required report sections.

## Blockers

None within this docs-only clarification allowlist.

## Recommendations

- PM should intake this report and decide whether focused Reliability, Data Quality and Verification contract reviews are needed.
- Do not treat this clarification as frontend strict parser implementation or test authorization.

## Next gate

- Eligible for: PM intake followed, if PM elects, by focused Reliability, Data Quality and Verification contract review.
- PM must separately authorize any Level 1 frontend strict parser implementation gate after the required clarification/reviews are closed.
- Not authorized: `frontend/src/lib/acceptedStationEvents/schema.ts` modification, frontend/API tests, API response changes, status sync, stage, commit or push.

## Thread 输出 / 上下文评估

- 本次输出长度：中
- 当前 Thread 是否建议继续：no
- 下一轮是否建议新开 Thread：yes
- 理由：本 Level 2 contract clarification 已关闭前序 ambiguity；后续若需要 review 或 Level 1 frontend strict parser implementation，应与本次 docs-only gate 隔离，并由 PM 单独授权。
