# Sprint 3 Dashboard production URL-resolution Verification planning review report

报告名称：Sprint 3 Dashboard production URL-resolution Verification planning review report

任务名称：Review URL-resolution implementation and validation executability

执行 Thread：Verification

风险等级：Level 1 review-only；future implementation and runtime validation remain Level 2。

结论：**HOLD**

本 review 未运行 tests、typecheck、build、server、browser、probe、mock、API、DB、Docker 或 dependency install；未修改 authority、frontend、package/config、generated artifacts 或 external artifacts。本次唯一写入为本 report。

## 1. Baseline and recovery

| Item | Live evidence |
| --- | --- |
| Branch | `main...origin/main` |
| HEAD | `bb1935a6e872bb957fc5da61c0c9acaae98c5956` |
| Latest commit | `bb1935 Record Dashboard URL resolution Data Quality review` |
| origin/main | `bb1935a6e872bb957fc5da61c0c9acaae98c5956` |
| ahead/behind | `0 0` |
| Cached diff | empty |
| Tracked diff | `.gitignore` only |
| Review target before this task | absent |

Expected external dirty artifacts were present and excluded: `.gitignore`, the named historical PM handoffs, `docs/reports/phase1_to_sprint2_management_keynote_10p.html`, `docs/reports/sprint3_db_backed_api_validation_reliability_review.md`, and `frontend/node_modules/`. No target collision, unknown HEAD advance, staged change, or frontend dirty change (excluding `node_modules`) was found.

## 2. Reviewed authorities and source

完整读取 PM operating rules、current status、Dashboard API contract、vertical validation、stale-data、typecheck/build、browser/manual smoke、same-origin mock-capability、URL-resolution plan、both Reliability reviews，以及 Data Quality review。只读审计了授权的 package/config、page/error/loading、client/query/schema/viewModel、全部指定 tests、component tests、Compose、`.env.example` 和 README。

Static searches confirm one accepted-events client call site, one current relative URL client call, no current frontend `process.env` or `NEXT_PUBLIC_*` use, no Vitest/Vite config, and no existing capture/fixture runtime implementation. `next.config.ts` has only `output: "standalone"`; Compose has no frontend service.

## 3. Current tooling

`frontend/package.json` freezes:

```text
npm test          -> vitest run --environment jsdom
npm run typecheck -> tsc --noEmit
npm run build     -> next build
```

The script forwards arguments after `npm test --` to `vitest run`; therefore each proposed exact test path is a valid focused file filter. Use three ordered commands—resolver, client, then page—rather than one combined command: this localizes failure and gives each env-mutating resolver run an independent Vitest invocation. No package script, Vitest config, dependency, or test-helper file is required for that ordering.

Vitest `describe.sequential`, `afterEach`, `vi.resetModules`, and the existing `vi.mock`/`mockReset` pattern are sufficient for serial test-local cleanup and module-isolated logging tests. They do not by themselves make a direct `process.env` property-read count observable.

## 4. Review scope and exact implementation allowlist

The planned six paths remain the only source/test scope:

```text
Create: frontend/src/lib/acceptedStationEvents/apiOrigin.ts
Modify: frontend/src/lib/acceptedStationEvents/apiClient.ts
Modify: frontend/src/app/accepted-events/page.tsx
Create: frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
Modify: frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
Modify: frontend/src/app/accepted-events/__tests__/page.test.tsx
```

`schema.ts`, `query.ts`, `viewModel.ts`, components, package/lock/config, `.env.example`, Compose, README, logger/config utilities, fixtures and runtime helpers remain excluded. Apart from finding `VER-URL-V1`, the six paths are sufficient for resolver, brand, typed failure handling, absolute composition, fetch options, page no-fetch handling, focused tests and DQ transport-profile isolation. No additional source file, schema/query/view-model edit, or dependency is justified.

## 5. Resolver testability

The authority correctly freezes server-only paired variables, request-time reading, fail-closed raw validation, `URL.origin` canonicalization, a fixed safe UI message, finite safe-code logging, and no production reset export. Positive/negative origin forms can be table-parameterized by profile and boundary class; split parameter tables by local/container/production/negative to preserve failure localization.

However, it does not freeze the exported result union/discriminant, exact safe-code members, or the permitted seam for proving each environment *property* is read exactly once. A behavioral re-read test can prove that separate invocations observe changed values and module isolation can prove per-module dedupe; neither proves one versus two reads of one property during one invocation. A global `process.env` proxy is expressly disallowed, and no non-proxy observation mechanism or production-facing injection contract is specified.

This prevents implementation/test authors from deciding, without new design judgment, whether the resolver throws or returns, how page detects failure, how the brand is obtained in client tests, how logging codes are triggered, and how the exact-read invariant is measured. This is the blocking finding below.

## 6. API client and page testability

After `VER-URL-V1` is repaired, the planned files are sufficient.

- `apiClient.ts` can accept only `TrustedAcceptedEventsApiOrigin`, compose `new URL(fixedPath, origin)`, retain `URLSearchParams`, injected `fetchImpl`, one fetch, `GET`, `cache: "no-store"`, `credentials: "omit"`, and `redirect: "error"`.
- A client test can obtain a legitimate brand through the frozen resolver success path; any compile-time ordinary-string rejection belongs in a `// @ts-expect-error` assertion, not a production cast. The production page must contain no cast.
- The existing page test already mocks the client and resets it in `afterEach`. It can additionally mock the resolver in the same file: invalid query must precede resolver/client/fetch; configuration failure must render the fixed error with zero client/fetch and no ready/table/summary/NOK/trace/cursor surfaces; valid resolution must pass the brand once.
- Existing parser/client state coverage supports unchanged malformed-2xx, 4xx, 503, other non-2xx, network, and redirect classifications. The future page test must add direct assertions that transport profile never enters rows/summary/UI while response `profile_id` stays response-owned (`DQ-URL-D1`).

## 7. Focused tests, full regression, and contract coverage

Recommended future order:

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend
npm test -- src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
npm test -- src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
npm test -- src/app/accepted-events/__tests__/page.test.tsx
npm test
```

The full command, not focused URL tests, is the closure point for `DQ-URL-D3`. It must record test-file/test/pass/fail/skip counts, exit code, and unhandled-rejection evidence. It executes the unchanged schema/query/viewModel/component suites that protect: endpoint/five keys, opaque cursor, exact outer/data/page structure, 22 required keys, explicit null versus missing/unknown, malformed 2xx, classifications, stale-data removal, current-page-only summary, `accepted_at`, lineage, and forbidden fallback leakage.

## 8. Typecheck, build, bundle, and cleanup

The existing validation authority makes the order executable: focused/full tests, `npm run typecheck`, exact artifact audit/cleanup, then `npm run build`. `tsconfig.json` is `incremental`, so `frontend/tsconfig.tsbuildinfo` may be generated; build may generate `frontend/.next`, `frontend/next-env.d.ts`, and `frontend/tsconfig.tsbuildinfo`. All three were absent and untracked at this review preflight.

Future build must run with both URL variables unset, make no API request, and must not be treated as runtime readiness. The current standalone setting is sufficient to require a `frontend/.next/standalone` artifact after a successful build. Cleanup is already exact: only preflight-absent, task-created named paths may be removed; never `node_modules`, `git clean`, reset/restore, or broad deletion.

## 9. Client/server bundle leakage

The authority requires no client leakage but does not yet freeze an executable client-chunk inspection. This is non-blocking, because it needs no source/package/config change. The runtime/build gate should inspect `frontend/.next/static/**` separately from `.next/server/**`: the two variable names and resolver module marker must be absent from static browser chunks; server occurrence of variable names is not itself a leak. The gate must also record that no configured raw origin was supplied at build time and must not claim a whole-`.next` grep proves browser safety.

## 10. Runtime recovery and capture/fixture evidence

The plan correctly keeps runtime execution separate from source implementation and requires one build, two different Next PIDs, no rebuild, the same standalone artifact, Phase-A zero accepted-events outbound request, and Phase-B exactly one capture request.

It does not freeze the capture implementation, temporary location/allowlist, fixture body source, request-counter persistence/output, or the concrete evidence mechanism for zero versus exactly-one request. An absent listener plus connection refusal is not zero-request evidence. This does not block the six-file implementation: it requires a dedicated runtime planning gate before any runtime authorization. That gate must choose an existing available capture method or else return HOLD; it may not silently add package/config/source scope. It must define `/usr/sbin/lsof` availability/path, preflight listeners, record only owned PIDs, TERM only recorded PIDs, prove both ports released, hash/manifest the standalone artifact before Phase A and recheck it before Phase B, and separately label transport, synthetic strict-contract fixture, and real production-fact evidence (`DQ-URL-D2`).

## 11. Finding closure

| Finding | Required closure point |
| --- | --- |
| `REL-URL-R3` | repaired resolver contract plus focused snapshot/read-count and request-time re-read tests; page/client env-read source search |
| `REL-URL-R4` | focused finite-code, per-code dedupe, redaction, logging-throw containment, and module-reset tests; runtime only needs repeated-request safe-log/no-raw-output observation |
| `REL-URL-R5` | serial resolver suite, exact presence/value restoration, failure-safe `afterEach`, module isolation, and no host-env default |
| `REL-URL-R6` | later deployment/config gate for accepted-events readiness, alerting, diagnostics, DNS and egress |
| `DQ-URL-D1` | client/page isolation assertions: transport profile absent from DTO/view state and response `profile_id` preserved |
| `DQ-URL-D2` | dedicated runtime report’s three-way evidence classification |
| `DQ-URL-D3` | recorded successful full `npm test`, including unchanged schema/query/viewModel/component suites |

## 12. Contract and source-search evidence

Future validation must supplement, not replace, tests with source search proving no relative accepted-events fetch, `NEXT_PUBLIC_*`, `Host`/`Forwarded` origin, page/client raw env access, unvalidated string endpoint, fallback endpoint, new query key, production mock/fixture path, or schema/query/viewModel/package/config change. Static source currently has no `process.env`/`NEXT_PUBLIC_*` use and has exactly one relative accepted-events fetch call; that is the targeted repair point.

## 13. Findings

### VER-URL-V1

ID: `VER-URL-V1`

Severity: `BLOCKER`

Status: `OPEN`

Area: `Testability / Scope / Tests`

Finding: The URL plan names the resolver and conceptual typed failure but does not freeze an executable public result contract or a permitted non-global-proxy method to observe the required exactly-once reads of both env properties. Behavioral tests alone cannot prove that count.

Evidence: plan sections 9, 14 and 18 require one immutable two-variable snapshot, typed failure, finite logging, and exact read evidence; current frontend has no resolver/test seam and no environment-read helper. The six-file test allowlist forbids an extra helper, and the task forbids a global `process.env` proxy and production-only reset export.

Required resolution: **planning repair** to the existing URL-resolution authority before implementation. It must freeze one typed non-throwing result union (success brand and failure safe code/message), brand creation/consumption rules, finite safe-code set, and an explicit testable environment-input seam. The seam may be an optional, typed environment object used only by the resolver’s test invocation (with production defaulting internally to `process.env`); it must preserve validation and not expose raw origin or require page/client env reads. The repair must state exact `afterEach` restoration, serial/module-isolated test use, and that no global `process.env` proxy or test-only production reset export is permitted.

Gate impact: `HOLD`.

### VER-URL-V2

ID: `VER-URL-V2`

Severity: `RECOMMENDATION`

Status: `CARRY FORWARD`

Area: `Bundle / Build`

Finding: Client-leakage intent is frozen but the exact static-chunk inspection command and positive/negative interpretation are not.

Evidence: plan sections 7 and 19 forbid public exposure; current `next.config.ts` only sets standalone output.

Required resolution: **build gate**; add a read-only `.next/static/**` versus `.next/server/**` inspection to the authorized evidence log. No source/package/config change.

Gate impact: `PASS WITH RECOMMENDATIONS` after `VER-URL-V1` closes.

### VER-URL-V3

ID: `VER-URL-V3`

Severity: `RECOMMENDATION`

Status: `CARRY FORWARD`

Area: `Runtime / Evidence / Cleanup`

Finding: same-artifact intent is strong, but no existing capture/fixture method or exact temporary artifact boundary proves zero/exactly-one outbound requests.

Evidence: no capture implementation exists; the URL plan assigns a separate loopback capture/fixture endpoint but does not name its implementation or evidence persistence.

Required resolution: **dedicated runtime planning gate** with exact capture method, fixture matrix, temp/PID/log/port/artifact allowlist, request counter evidence, `/usr/sbin/lsof` preflight, same-artifact hash/manifest, and three-way DQ evidence labels.

Gate impact: implementation may proceed only after `VER-URL-V1` closes; runtime remains not ready.

## 14. Blocking findings and carry-forward recommendations

```text
Blocking findings: VER-URL-V1
Carry-forward recommendations: VER-URL-V2, VER-URL-V3
Closed-by-plan findings: none
New findings: VER-URL-V1, VER-URL-V2, VER-URL-V3
```

## 15. Readiness and conditions

```text
Implementation allowlist sufficient: no, until VER-URL-V1 freezes the resolver/test contract
Package/config/script changes required: no
Additional source files required: no
Schema/query/viewModel changes required: no
New dependency: no
Implementation readiness: no
Runtime validation readiness: requires separate planning gate
```

PASS is not available because `VER-URL-V1` is open. After the planning repair closes it, the applicable planning conclusion is `PASS WITH RECOMMENDATIONS`, not bare PASS, because bundle inspection and runtime capture planning remain explicit later gates. HOLD persists for any package/config/script/helper expansion, inability to preserve the brand boundary, unsafe env isolation, parser/query/view-model drift, build/API dependency, unsafe cleanup, unknown capture tool, or conflated source/runtime authorization.

## 16. Required next action

PM must authorize an exact-path Architecture planning repair of `docs/reports/sprint3_dashboard_production_url_resolution_plan.md` for `VER-URL-V1`, followed by a fresh Reliability/Data Quality/Verification re-review as PM directs. Do not commit this review, start Security/privacy review, implement, modify tests, run tests/typecheck/build, or start runtime validation from this HOLD.

## 17. Thread output / context assessment

- 本次输出长度：长（durable Verification authority；window report 应保持简洁）。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：planning repair、cross-functional re-review、implementation, build, and runtime capture are distinct PM authorization boundaries.
