# Sprint 3 Dashboard accepted-events strict parser fail-closed planning gate report

Date: 2026-07-10
Thread: Architecture / Integration
Status: HOLD

本 gate 仅做 planning。它不授权 parser implementation、tests、typecheck、
build、browser/server/runtime、API/DB/Postgres、Docker、contract/status sync、
stage、commit、push、tag、deploy、rollback 或 real PLC pilot。

## 1. Report identity

报告名称：
Sprint 3 Dashboard accepted-events strict parser fail-closed planning gate report

任务名称：
Dashboard accepted-events envelope/data/page strict parser fail-closed planning

执行 Thread：
Architecture / Integration

结论：HOLD

结论理由：当前 API route 与 accepted-station-events 专属示例均返回 exact
`data` + `page`，但 `docs/contracts/dashboard_api_contract.md` 的通用响应
Envelope 同时包含 `meta`，合同没有说明专属 endpoint 是否覆盖通用 Envelope、
也没有定义该 endpoint 的 exact `meta` schema。当前 gate 不允许修改 contract，
因此不能在不猜测的情况下冻结 envelope exact keys。继续 implementation 会造成
错误拒绝合法 `meta` 或继续静默接受未知 envelope 字段，均不满足 fail-closed
要求。

## 2. Read-only recovery

第一动作已执行指定 read-only recovery。

```text
branch: main tracking origin/main
HEAD: 885a09423997f9dfc3ad597607509fb37372717e
origin/main: 885a09423997f9dfc3ad597607509fb37372717e
latest commit: 885a094 Add PM handoff after leakage fixture closeout
git diff --name-only: .gitignore
git diff --cached --name-only: empty
```

`git status --short --untracked-files=all` 中的 dirty state 仅为本任务列明的
external artifacts；`frontend/node_modules/` 展开后的文件仍属于同一排除目录。
cached diff 为空，live baseline 与授权时 expected baseline 一致。

## 3. Scope

Scope:

- reviewed files:
  - `docs/thread_handoff/pm_operating_rules.md`
  - `docs/thread_handoff/chatgpt_pm_handoff_260710-1659.md`
  - `docs/current_status.md`
  - `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
  - `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
  - `docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`
  - `docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md`
  - `docs/reports/sprint3_dashboard_api_implementation_plan.md`
  - `docs/contracts/dashboard_api_contract.md`
  - `frontend/src/lib/acceptedStationEvents/schema.ts`
  - `frontend/src/lib/acceptedStationEvents/apiClient.ts`
  - `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`
  - `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts`
  - `api/app/routes/accepted_station_events.py`
- changed files:
  - `docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md`
- explicitly not touched:
  - `.gitignore`
  - `frontend/src/lib/acceptedStationEvents/schema.ts`
  - `frontend/src/lib/acceptedStationEvents/apiClient.ts`
  - all frontend tests and all other `frontend/**` files
  - `api/**`, including route and tests
  - `docs/contracts/dashboard_api_contract.md`
  - `docs/current_status.md`
  - adapter gate/status/plan, PM operating rules and PM handoff
  - package/config, DB/migration, Collector/runtime, ACK/read_done and Docker/deploy surfaces
  - all listed external dirty artifacts and `frontend/node_modules/`

## 4. Current parser finding

Current parser finding:

- item-level behavior:
  - `acceptedStationEventFields` is an exact allowlist.
  - `parseItem()` iterates `Object.keys(item)` and throws
    `forbidden accepted event DTO field: <key>` for every unknown item-level key.
  - Existing item fixtures already reject raw/debug/diagnostic/review/audit/candidate
    fields, camelCase/renamed aliases, production-looking aliases and accepted-looking
    values nested under unsupported item containers.
  - This slice must not expand or reinterpret the accepted fact DTO allowlist.
- envelope-level behavior:
  - The parser checks that the envelope is a non-null, non-array object and reads
    `data` and `page`.
  - It does not compare envelope keys with an exact allowlist. Extra keys, including
    `meta`, `review_payload`, `audit_payload`, aliases or unsupported containers,
    are silently omitted from the returned parsed object.
- data-level behavior:
  - The parser checks that `data` is an object and `data.items` is an array.
  - It does not reject keys other than `items`; extra keys are silently omitted.
- page-level behavior:
  - The parser validates `next_cursor` as string/null and `limit` as an integer in
    `1..500`.
  - It does not reject keys other than `next_cursor` and `limit`; extra keys are
    silently omitted.

Current `schema.test.ts` therefore proves non-return/leakage for outer unknown keys,
not fail-closed rejection. The existing test named
`does not return envelope, data, or page-level forbidden payloads` currently expects
successful parsing and stripping, so it must be replaced by rejection assertions only
after the contract blocker is closed.

## 5. Exact JSON shape audit

The unambiguous layers are frozen as follows:

```text
data allowed keys, exact:
- items

page allowed keys, exact:
- next_cursor
- limit

item allowed keys, unchanged and exact:
- line_id
- plc_id
- station_id
- station_type
- profile_id
- config_hash
- config_version
- event_type
- production_result
- unit_id
- dmc
- cycle_counter
- source_event_id
- event_ts
- accepted_at
- fact_key
- content_fingerprint
- nok_code
- nok_origin
- nok_detail_code
- nok_detail_source_event_id
- nok_detail_evidence_fact_key
```

Envelope exact keys are not frozen by this gate because the contract is ambiguous:

```text
candidate A, matching the live API route and endpoint-specific example:
- data
- page

candidate B, if the endpoint inherits the generic envelope:
- data
- meta
- page
```

No implementation may use either candidate as authority until the contract explicitly
chooses one. Arbitrary `meta`, optional unvalidated `meta`, and silent stripping of
`meta` or any other unknown envelope key are all forbidden outcomes.

## 6. Contract decision

Contract decision:

- exact envelope keys: unresolved; `data` and `page` are required, while `meta`
  remains a blocking contract ambiguity.
- exact data keys: `items` only.
- exact page keys: `next_cursor` and `limit` only.
- meta decision: option 3 — current contract contains a conflict that this gate
  cannot resolve; report `HOLD` and open a separate contract clarification gate.
- error classification:
  - client-side query construction/validation failure remains `invalid-query`;
  - API 4xx remains `invalid-query`;
  - API 503 remains `unavailable`;
  - malformed successful JSON, malformed DTO, or any future strict parser throw
    remains `error`;
  - other non-4xx/non-503 response or fetch/JSON failure remains `error`.

The current `apiClient.ts` already catches parser exceptions in the request/parse
`try` block and maps them to `kind: "error"`. No production client change is needed,
and this planning does not alter existing API 4xx/503 mapping.

Recommended contract clarification, not a decision made by this HOLD gate: explicitly
declare the accepted-station-events endpoint envelope to be exactly `{data, page}` and
forbid `meta`. This matches the live route and endpoint-specific example and avoids an
API compatibility change. If PM instead chooses legal `meta`, the contract must define
its exact required/optional keys and value schema; arbitrary `meta: object` is not
acceptable.

## 7. Fail-closed behavior to freeze after contract clarification

For every frozen layer, the parser must compare enumerable own JSON keys against that
layer's exact allowlist before constructing the returned value. Any set difference
must throw; it must not omit, normalize, rename, recurse into, or salvage accepted-looking
values from an unsupported key.

Required behavior:

- unknown envelope key: throw before returning an envelope;
- unknown data key: throw before parsing/returning items;
- unknown page key: throw before returning pagination state;
- nested unknown object: reject its unsupported container key; do not inspect nested
  values for salvage or production meaning;
- camelCase/renamed alias: reject, including `nextCursor`, `pageLimit`, `rawPayload`,
  `dashboardState`, `productionQuality` and equivalent aliases;
- production-looking alias: reject, including bare or prefixed result/defect/quality/
  pareto fields not in the existing item allowlist;
- accepted-looking values nested under unsupported containers: reject the container,
  even if nested values resemble `fact_key`, `source_event_id`, `production_result`,
  `nok_code` or other accepted fields;
- empty key and prototype-looking keys: cover `""`, `"__proto__"`, `"prototype"`
  and `"constructor"` as own JSON keys at envelope/data/page and item levels; each is
  an unknown key and must be rejected;
- object edge cases in scope: `null`, arrays and wrong primitive shapes remain rejected;
  JSON fixtures for prototype-looking keys must be created with `JSON.parse` or another
  own-property-safe construction so object-literal `__proto__` semantics cannot make
  the test vacuous;
- object edge cases out of this HTTP JSON slice: symbol keys, non-enumerable properties,
  inherited properties, getters, Proxy behavior and non-JSON class instances. They are
  not representable in `Response.json()` output and do not justify prototype-normalizing
  or cloning behavior in this slice.

The parser remains a validator of the API's JSON response, not a compatibility adapter.

## 8. Compatibility boundary

The intended strict parser hardening, after the contract blocker closes, must satisfy
all of the following:

- no API endpoint change;
- no query parameter change;
- no accepted fact DTO field allowlist change;
- no cursor decode, mutate, construct, schema or lifecycle change;
- no production fact authority change;
- no `work_order`, `product`, raw/debug/diagnostic/review/audit/candidate or legacy
  fields;
- no DB, API route, contract, Collector, runtime, ACK/read_done or deployment semantic
  change;
- no legacy/current/raw/diagnostic fallback;
- no stale prior data or non-accepted evidence becoming production truth.

These conditions cannot yet all be confirmed because envelope compatibility is not
frozen. If contract clarification selects legal `meta` or requires API/contract changes,
the strict parser slice crosses the frontend/API/contract boundary and must be replanned
as Level 2.

## 9. Risk classification

Risk classification:

- Level 2
- rationale:
  - The current blocker is a contract ambiguity, not a line-local parser detail.
  - Closing it requires an explicit `dashboard_api_contract.md` clarification; contract
    modification is a Level 2 trigger under this gate's rules.
  - Supporting `meta` would additionally require an exact meta schema and potentially
    an API response change, also Level 2.
  - Only if a separate contract clarification gate explicitly forbids `meta`, confirms
    exact `{data,page}`, and requires no API/client/error/authority change may the later
    parser implementation be reclassified as Level 1 with the small frontend-only
    allowlist below.

## 10. Future exact implementation and test allowlists

The following lists are conditional planning output only. They are not eligible for
authorization while this report is `HOLD`.

Future exact implementation allowlist:

Only after contract clarification selects exact `{data,page}` and confirms no
API/contract/client change:

```text
frontend/src/lib/acceptedStationEvents/schema.ts
```

Future exact test allowlist:

```text
frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts
frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
```

`apiClient.test.ts` is required because the acceptance matrix explicitly requires proof
that a strict parser exception from a successful HTTP response becomes the existing
client `error` state. `frontend/src/lib/acceptedStationEvents/apiClient.ts` is excluded
because its current mapping already satisfies that contract.

If clarification selects legal `meta`, these allowlists are invalid and must be replaced
by a new exact Level 2 allowlist after the exact meta schema and API compatibility plan
are approved. Directory-level allowlists remain forbidden.

## 11. Planning acceptance matrix

The later implementation/test gate, if eligible, must freeze and prove:

- valid exact envelope passes;
- valid empty `items` envelope passes;
- valid opaque cursor passes unchanged;
- unknown envelope key rejects;
- unknown data key rejects;
- unknown page key rejects;
- nested diagnostic/review/audit/raw/candidate container rejects at each outer layer;
- camelCase/renamed alias rejects;
- production-looking alias rejects;
- accepted-looking values nested under an unsupported container reject;
- empty and prototype-looking own JSON keys reject;
- existing item-level forbidden field matrix continues to pass without expanding the
  DTO allowlist;
- the parser no longer silently strips unsupported envelope/data/page keys;
- a strict parser throw from a 2xx response maps through `apiClient` to `error`;
- existing pre-request/API 4xx maps remain `invalid-query`;
- existing API 503 mapping remains `unavailable`;
- valid current API `{data:{items:[]},page:{next_cursor,limit}}` responses remain
  compatible;
- no cursor decode/mutate/construct;
- no raw/debug/diagnostic/review/audit/candidate/legacy fallback;
- no stale data or production evidence leakage.

The contract clarification gate must first add one acceptance assertion that states
whether `meta` rejects or validates against an exact endpoint-specific schema. No test
may encode that choice before the contract gate closes.

## 12. Future validation commands

Future validation commands:

These commands are proposals for a later explicitly authorized frontend validation
gate. They were not run in this planning gate.

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm test -- src/lib/acceptedStationEvents/__tests__/schema.test.ts
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm test -- src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
cd /Users/chenjie/Documents/MES/edge-mes-demo && git diff --check -- frontend/src/lib/acceptedStationEvents/schema.ts frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
cd /Users/chenjie/Documents/MES/edge-mes-demo && git diff --name-only
cd /Users/chenjie/Documents/MES/edge-mes-demo && git diff --cached --name-only
cd /Users/chenjie/Documents/MES/edge-mes-demo && git status --short --untracked-files=all
```

Future execution must stop on the first failure and must compare the final changed set
against the exact three-file implementation/test allowlist plus the pre-existing external
exclusions. Typecheck/build are not part of this proposed focused gate unless separately
authorized.

## 13. Explicit exclusions

Explicit exclusions:

- `frontend/src/lib/acceptedStationEvents/apiClient.ts` production edits;
- API endpoint, route, query params, response, tests or error envelope edits;
- `docs/contracts/dashboard_api_contract.md` inside the parser implementation slice;
- accepted fact DTO additions/removals or semantic changes;
- `meta` support without an exact schema and separate Level 2 authorization;
- cursor decode/mutate/construct or cursor compatibility changes;
- `work_order`, `product`, raw/debug/diagnostic/review/audit/candidate fields;
- DB/Postgres/migration, Collector/runtime/storage, PLC/V-PLC, ACK/read_done;
- browser/server/runtime, Docker, deploy, tag, rollback, real PLC pilot;
- broad frontend/API tests, typecheck/build unless separately authorized;
- docs/status sync, stage, commit and push;
- `.gitignore`, PM handoffs, unrelated reports and `frontend/node_modules/`.

## 14. Blockers

Blockers:

- B1: `docs/contracts/dashboard_api_contract.md` does not state whether
  accepted-station-events inherits the generic `meta` field or whether its endpoint-
  specific envelope is exactly `{data,page}`.
- B2: If `meta` is legal, no endpoint-specific exact `meta` schema is defined and the
  live API route does not emit it.
- B3: Because B1/B2 are unresolved, the final envelope allowlist and Level 1
  frontend-only compatibility claim cannot be frozen safely.

## 15. Recommendations

Recommendations:

- Open a separate Architecture / Integration contract clarification gate with an exact
  docs-only allowlist for `docs/contracts/dashboard_api_contract.md`.
- Prefer explicitly making this endpoint's exact envelope `{data,page}` and prohibiting
  `meta`, because that matches the live route and endpoint-specific example and keeps the
  later implementation frontend-only. This is a recommendation requiring contract
  approval, not authority granted by this report.
- If PM chooses legal `meta`, define its exact keys, types, required/optional status and
  compatibility behavior, then replan API + frontend as Level 2; never accept arbitrary
  `meta: object`.
- After contract clarification, issue a new exact implementation authorization rather
  than treating this HOLD report or the earlier leakage recommendation as implementation
  authority.

## 16. Next gate

Next gate:

- eligible for: separate Level 2 contract clarification planning/edit gate for the
  accepted-station-events exact envelope and `meta` inheritance decision.
- not eligible for: strict parser implementation, tests, API/contract production changes,
  status sync, stage, commit or push.
- after clarification chooses exact `{data,page}` without API/error/authority changes:
  PM may open a new Level 1 frontend strict parser implementation gate using the exact
  implementation/test allowlists in section 10.
- after clarification chooses legal `meta`: PM must open a new Level 2 cross-boundary
  planning sequence; section 10's conditional allowlists must not be reused.

PM approval remains required before every later gate.

## 17. Thread output / context assessment

Thread 输出 / 上下文评估：

- 本次输出长度：长
- 当前 Thread 是否建议继续：no
- 下一轮是否建议新开 Thread：yes
- 理由：本 gate 已完成 parser/contract 审计并停在明确的 contract blocker；下一轮
  是独立 Level 2 contract clarification gate，必须与本 planning gate 及此前
  tests-only leakage fixture closeout 隔离，不能把 recommendation/HOLD 自动解释为
  implementation authorization。
