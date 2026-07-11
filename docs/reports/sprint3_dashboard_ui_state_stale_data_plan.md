# Sprint 3 Dashboard accepted-events UI/state stale-data planning gate report

Date: 2026-07-11

报告名称：
Sprint 3 Dashboard accepted-events UI/state stale-data planning gate report

任务名称：
Freeze fail-closed UI/state behavior so prior accepted facts cannot remain visible as fresh production truth after loading, query rejection, parser/client error, source unavailability or an empty replacement result

执行 Thread：
Architecture / Integration

风险等级：
Level 1 — planning-only, frontend state/test boundary

结论：PASS WITH RECOMMENDATIONS

本 gate 只完成现状审计与未来 tests-only gate 规划。它不授权 frontend production implementation、tests、typecheck、build、browser/manual smoke、API/DB/Postgres、Docker、server/runtime、docs/status sync、stage、commit、push、deploy、tag、rollback、V-PLC 或 real PLC 操作。

## 1. Baseline and recovery

本 gate 第一动作执行了 read-only Git recovery。

```text
branch:
main

HEAD:
3c4bfd3e79f94d6d08917cb9c0b6be735303a403
3c4bfd3 Add PM handoff after explicit-null closeout

origin/main:
3c4bfd3e79f94d6d08917cb9c0b6be735303a403

cached diff:
empty

tracked working-tree diff:
M .gitignore
```

Live baseline 与 PM 授权时 expected baseline 完全一致。当前 dirty artifacts 仅为已声明 external artifacts：

```text
M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
?? frontend/node_modules/
```

本 planning report 创建后，它是本 gate 唯一新增的项目文件，仍保持 untracked，未 stage。

## 2. Required context reviewed

已读取并遵守：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260711-1305.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md`
- `docs/reports/sprint3_dashboard_accepted_events_envelope_contract_clarification_report.md`
- `docs/reports/sprint3_dashboard_accepted_events_item_required_key_contract_repair_report.md`

本 gate 还只读审计了：

- `frontend/package.json`
- `frontend/src/app/accepted-events/page.tsx`
- `frontend/src/app/accepted-events/loading.tsx`
- `frontend/src/app/accepted-events/error.tsx`
- `frontend/src/app/accepted-events/__tests__/page.test.tsx`
- `frontend/src/lib/acceptedStationEvents/apiClient.ts`
- `frontend/src/lib/acceptedStationEvents/viewModel.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts`
- `frontend/src/components/accepted-events/AcceptedEventsStates.tsx`
- `frontend/src/components/accepted-events/AcceptedEventsQueryControls.tsx`
- `frontend/src/components/accepted-events/__tests__/AcceptedEventsQueryControls.test.tsx`
- `frontend/src/components/accepted-events/PageSummaryStrip.tsx`
- `frontend/src/components/accepted-events/NokDetailEvidencePanel.tsx`
- `frontend/src/components/accepted-events/TraceReferencePanel.tsx`

## 3. Scope

### In scope

- 审计 accepted-events 页面从 request/query 到 page state 和 rendered production facts 的状态边界；
- 判断当前是否存在显式 cache、previous-data retention 或 fallback；
- 冻结 stale-data 的 fail-closed 定义；
- 比较可选实现路径并选择最小风险方案；
- 给出未来精确 tests-only allowlist、测试矩阵、验证命令和 stop conditions。

### Explicitly out of scope

- 不修改任何 `frontend/**` production 或 test 文件；
- 不运行 tests、typecheck、build 或 browser/manual smoke；
- 不修复或扩展 query controls navigation；
- 不引入 router、client fetch hook、state reducer、SWR、React Query、localStorage、sessionStorage、IndexedDB 或其他 cache；
- 不修改 API route、response envelope、DTO、cursor、query、DB、Collector/runtime、ACK/read_done、V-PLC、Docker/deploy；
- 不修改 `docs/current_status.md`、gate status、collector plan、contract、PM rules 或 handoff；
- 不 stage、commit 或 push。

## 4. Current architecture findings

### 4.1 Current data-fetch boundary is already non-caching by intent

`frontend/src/app/accepted-events/page.tsx` declares：

```text
export const dynamic = "force-dynamic"
```

`frontend/src/lib/acceptedStationEvents/apiClient.ts` performs one GET request with：

```text
cache: "no-store"
```

The existing `apiClient.test.ts` already asserts the single accepted-events request uses `method: "GET"` and `cache: "no-store"`. It also proves malformed 2xx responses map to client `kind: "error"` without retry, second request, fallback endpoint or empty-envelope normalization.

### 4.2 Current page state is structurally fail-closed

`PageViewState` is a discriminated union：

- non-ready state: `invalid-query | loading | empty | error | unavailable`；
- ready state: contains `query` and `viewModel`。

`AcceptedEventsPageView` returns early for every non-ready state and renders only the state message. The ready-only branch owns all production-truth surfaces：

- query controls；
- current-page summary；
- accepted-events table；
- NOK/detail evidence panel；
- trace reference panel。

Therefore current source structure does not pass `viewModel`, rows, summary, evidence or trace reference into `loading`, `error`, `unavailable` or `invalid-query` states.

### 4.3 Current route path does not construct a view model after a client failure

`AcceptedEventsPage` performs：

1. search-param query construction；
2. fail-closed query validation；
3. accepted-events client request；
4. immediate non-ready return when `result.ok === false`；
5. `toAcceptedEventsViewModel(result.envelope)` only on successful parsed envelope。

A parser/client error therefore does not call the ready-state construction path in the current implementation.

### 4.4 Current loading and error boundaries replace the page content with data-free states

- `loading.tsx` renders a `loading` state with the explicit notice that prior accepted facts are hidden；
- `error.tsx` renders an `error` state without any view model or production data props。

### 4.5 No active explicit client cache or prior-data retention mechanism was found

A source scan found no accepted-events use of：

- `useRouter` / router navigation state；
- `useTransition` / `startTransition`；
- SWR or React Query；
- `localStorage` / `sessionStorage` / IndexedDB；
- `keepPreviousData` or equivalent；
- custom accepted-events cache/store。

This means the carry-forward item is currently a **proof and regression-hardening gap**, not evidence of an already confirmed cache defect.

### 4.6 Existing tests partially cover the requirement but overstate one assertion

`page.test.tsx` includes a test named：

```text
does not render prior data as fresh production truth during loading or error
```

but the test body renders only the `loading` state. It proves the loading state has no table, but it does not execute：

- a previous ready render followed by a loading rerender；
- a previous ready render followed by error/unavailable/invalid-query；
- a non-empty ready result followed by an empty replacement result；
- removal of prior summary, NOK/detail evidence and trace references；
- the page-level handling of a client `error` result after a previous successful view。

The current wording therefore exceeds the executable evidence.

### 4.7 Query controls navigation is a separate concern

`AcceptedEventsQueryControls` supports an optional `onSubmit`, but the production page does not currently pass one. Making query controls navigate is outside this stale-data gate. This planning must not use the stale-data carry-forward item as authority to add router behavior or redesign the query workflow.

If a future navigation gate adds client transitions or previous-data retention, that gate must independently preserve the stale-data acceptance matrix below.

## 5. Stale-data contract to freeze

For this Dashboard production consumer, “fresh production truth” means data derived from the **current successfully validated, successfully fetched and strictly parsed accepted-events response for the current bounded query scope**.

The following are not fresh production truth：

- rows, summaries, NOK/detail evidence or trace references from a previous successful query after the current request enters loading；
- previous successful data after query validation fails；
- previous successful data after API 4xx, API 503, network/JSON failure, unexpected HTTP failure or strict parser failure；
- previous non-empty rows after the current successful query returns an empty item list；
- any client cache or future previous-data store not explicitly labelled historical/stale and isolated from production-truth surfaces。

Fail-closed UI rule：

```text
When the current accepted-events state is not ready, no prior ready-state production data may remain in the accepted-events table, current-page summary, NOK/detail evidence panel or trace reference panel.
```

Empty replacement rule：

```text
When a new successful current-scope response contains zero items, the previous rows and selected evidence/reference must be removed. The UI may display the current empty result and current-page count zero, but must not retain prior facts.
```

Error classification remains unchanged：

- pre-request validation / API 4xx → `invalid-query`；
- API 503 → `unavailable`；
- malformed successful response, strict parser throw, fetch/JSON failure and other request failure → `error`。

This gate does not change the accepted-events contract, source authority, DTO allowlist, explicit-null semantics, cursor ownership or request count.

## 6. Approaches considered

### Approach A — tests-only state-transition proof

Add deterministic component/page tests around the existing discriminated state model without changing production code.

Advantages：

- smallest possible scope；
- directly closes the current evidence gap；
- preserves the already fail-closed state structure；
- no new cache, router, store or state owner；
- no production semantic risk；
- easy exact-path audit。

Limitations：

- proves the current architecture only；
- does not implement future query navigation or client cache behavior；
- if a test exposes a real defect, production repair requires a separate gate。

### Approach B — add an explicit production state reducer / clear-data action

Introduce a new client state owner that clears rows, summary and detail on loading/error transitions.

Advantages：

- makes clearing behavior explicit if the page later becomes client-driven。

Disadvantages：

- creates state ownership that does not currently exist；
- duplicates the current discriminated-union/early-return protection；
- expands production surface without evidence of a production defect；
- could accidentally introduce previous-data retention or inconsistent server/client state。

### Approach C — introduce cache provenance and stale/fresh labels

Keep previous data but attach source scope, request generation and stale indicators.

Advantages：

- may support a future high-interactivity dashboard。

Disadvantages：

- unnecessary for the current page；
- materially increases state, cache and concurrency complexity；
- risks displaying historical data as current truth；
- requires broader design, browser behavior and race-condition validation；
- not appropriate for this Level 1 gate。

### Decision

**Approach A is selected and recommended.**

Current architecture already appears fail-closed. The correct next step is a separate Level 1 tests-only implementation gate that proves data removal across state transitions. Production code must remain unchanged unless those tests expose a concrete failure.

## 7. Future implementation gate classification

Recommended future gate：

```text
Level 1 — tests-only stale-data regression hardening
Owner: Verification
```

The implementation gate must begin with fresh read-only Git recovery. It must not infer authorization for production repair, broader test execution, typecheck/build, browser smoke, docs/status sync, stage, commit or push.

### Exact future implementation allowlist

```text
frontend/src/app/accepted-events/__tests__/page.test.tsx
```

No production file is included.

### Exact future read-only references

```text
frontend/src/app/accepted-events/page.tsx
frontend/src/app/accepted-events/loading.tsx
frontend/src/app/accepted-events/error.tsx
frontend/src/lib/acceptedStationEvents/apiClient.ts
frontend/src/lib/acceptedStationEvents/viewModel.ts
frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
frontend/src/components/accepted-events/AcceptedEventsStates.tsx
frontend/src/components/accepted-events/PageSummaryStrip.tsx
frontend/src/components/accepted-events/NokDetailEvidencePanel.tsx
frontend/src/components/accepted-events/TraceReferencePanel.tsx
```

## 8. Future test acceptance matrix

The future one-file tests-only gate must add or tighten executable coverage for all rows below.

| Case | Required setup | Required assertions |
| --- | --- | --- |
| ready → loading | render a ready state with identifiable row, summary, NOK/detail and trace values; rerender loading | loading message and prior-data-hidden notice visible; table, current-page summary, identifiable fact/DMC/NOK/trace values removed |
| ready → error | render ready then rerender `error` | error message visible; no table, summary, evidence or trace values from prior ready state |
| ready → unavailable | render ready then rerender `unavailable` | unavailable message visible; prior truth-bearing surfaces removed |
| ready → invalid-query | render ready then rerender `invalid-query` | invalid-query message visible; prior truth-bearing surfaces removed |
| ready non-empty → ready empty | render ready with one item, then rerender a ready state built from a zero-item envelope for the replacement scope | old row/evidence/reference removed; current empty message shown; current-page summary is zero and contains no old station/result counts |
| client error → page non-ready state | mock `fetchAcceptedStationEvents` to return `{ok:false, kind:"error"}` and render `AcceptedEventsPage` | error state rendered; no table, summary, NOK/detail or trace production data |
| source unavailable → page non-ready state | mock `{ok:false, kind:"unavailable"}` | unavailable state rendered; no ready production surfaces |
| existing loading/error test wording | update the existing overstated test or split it | test name and body must match exactly; no claim that error is covered unless error is executed |

The ready fixture must use distinctive identifiers so removal assertions cannot pass accidentally, for example：

```text
fact key: sha256:stale-fact
DMC: DMC-STALE-001
source event: PLC_001:WS01:stale
NOK detail code: STALE_DETAIL
config version: stale-config-version
```

Assertions must check more than `queryByRole("table") === null`. They must also verify removal of the prior summary and both detail surfaces, because stale production truth can leak outside the table.

## 9. Existing evidence that must remain green

The future tests-only gate must preserve, not rewrite, these already closed behaviors：

- invalid query fails before fetch；
- invalid URL limit fails closed without fetching or cursor decoding；
- malformed 2xx maps to client `kind: "error"`；
- no retry, second request or fallback endpoint；
- request uses `cache: "no-store"`；
- strict exact envelope and exact 22-key item parser remains unchanged；
- explicit JSON `null` remains legal and missing remains illegal；
- only `production_accepted_station_event_fact` is production fact authority；
- no raw/debug/diagnostic/candidate/legacy fields enter production UI。

The future gate must not reopen or reimplement strict parser or all-22-field explicit-null work.

## 10. Future validation commands

Only after PM explicitly authorizes the tests-only implementation gate：

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm test -- src/app/accepted-events/__tests__/page.test.tsx
cd /Users/chenjie/Documents/MES/edge-mes-demo && git diff --check -- frontend/src/app/accepted-events/__tests__/page.test.tsx
cd /Users/chenjie/Documents/MES/edge-mes-demo && git diff --name-only
cd /Users/chenjie/Documents/MES/edge-mes-demo && git diff --cached --name-only
cd /Users/chenjie/Documents/MES/edge-mes-demo && git status --short --untracked-files=all
```

Expected result：

- focused `page.test.tsx` command PASS；
- only the exact one-file allowlist is changed by the implementation gate；
- cached diff remains empty unless PM later separately authorizes staging；
- all external dirty artifacts remain untouched。

The future implementation gate does not include：

- full frontend suite；
- `apiClient.test.ts` rerun；
- `npm run typecheck`；
- `npm run build`；
- browser/manual smoke；
- API pytest or DB-backed validation。

Those validations remain separate gates.

## 11. Stop conditions and escalation

The future tests-only implementation Thread must stop and report `HOLD` without modifying production code if any of the following occurs：

- a ready → non-ready rerender leaves table, summary, evidence or trace content visible；
- zero-item replacement retains a prior selected row or detail；
- the test requires changing `page.tsx`, state types, loading/error boundaries, viewModel, API client or components；
- a router, cache/store, previous-data mechanism or request concurrency policy must be introduced；
- the current query controls navigation gap becomes necessary to test the stale-data requirement；
- package/config changes are required；
- focused tests cannot run reproducibly from the existing package environment；
- any non-allowlist file changes。

If a real production defect is exposed, PM must open a separate exact-scope repair planning gate. The tests-only gate must not silently expand into production implementation.

A future production repair limited to the accepted-events frontend may still be assessed as Level 1 if it is narrow and does not introduce a new cache/router/state architecture. Any new cache owner, previous-data retention, cross-request concurrency model, router transition architecture or API contract change requires fresh PM risk classification and may require Level 2 planning.

## 12. Explicit exclusions for every later gate

Unless separately authorized, exclude：

```text
.gitignore
frontend/node_modules/
docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
docs/reports/phase1_to_sprint2_management_keynote_10p.html
docs/reports/sprint3_db_backed_api_validation_reliability_review.md
docs/thread_handoff/chatgpt_pm_handoff_20260624.md
docs/thread_handoff/chatgpt_pm_handoff_20260625.md
docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

Forbidden staging remains：

```text
git add .
git add -A
git add docs/
```

Any later commit gate must use an exact path allowlist and run：

```bash
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

## 13. Blockers

None for this planning gate.

No current production stale-data defect was proven by read-only inspection. The gap is insufficient executable transition coverage.

## 14. Recommendations

1. Open the future Level 1 one-file tests-only gate described in sections 7–10.
2. Treat a failing transition test as a new repair-planning trigger, not permission to edit production code in the tests-only gate.
3. Keep query controls navigation, typecheck/build, browser smoke and API/DB validation as separate gates.
4. If future client-side navigation or caching is introduced, require request-scope/provenance and race-condition planning before allowing previous data to remain visible.

## 15. Next gate

Eligible for：

```text
Level 1 — Dashboard accepted-events stale-data regression tests-only implementation
Exact allowlist:
frontend/src/app/accepted-events/__tests__/page.test.tsx
```

Not automatically authorized：

- implementation or test execution；
- production frontend edits；
- typecheck/build/browser smoke；
- docs/status sync；
- stage/commit/push；
- API/DB/Collector/runtime/Docker/V-PLC/deploy/tag/rollback。

PM must separately authorize the tests-only implementation gate.

## 16. Thread output / context assessment

Thread 输出 / 上下文评估：

- 本次输出长度：中
- 当前 Thread 是否建议继续：yes，限下一轮单文件 tests-only gate
- 下一轮是否建议新开 Thread：yes
- 理由：planning 已完成并冻结 exact one-file allowlist；tests-only implementation 应由新的 Verification Thread 执行，避免把 Architecture planning 权限误扩展为测试或生产修复权限。
