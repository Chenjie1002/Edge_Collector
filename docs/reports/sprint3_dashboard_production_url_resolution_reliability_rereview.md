# Sprint 3 Dashboard production URL-resolution Reliability planning re-review report

报告名称：Sprint 3 Dashboard production URL-resolution Reliability planning re-review report

任务名称：Re-review the repaired Dashboard production URL-resolution planning authority and adjudicate REL-URL-R1 through REL-URL-R7

执行 Thread：Reliability

风险等级：Level 1 review-only；被审查的 future implementation remains Level 2。

结论：**PASS WITH RECOMMENDATIONS**

本报告独立复审已提交的 repair authority `f4c24ea8d829325788ce36d8029f71d516eef7f0`。不采纳 Architecture 的 “addressed” 声明作为证据；以下结论仅来自 committed repair、原 Reliability HOLD authority、Dashboard contract 和授权的当前 frontend surfaces。未运行 tests、typecheck、build、server、probe、browser、API、DB/Postgres 或 Docker；未 stage、commit 或 push。

## 1. Baseline and recovery

按要求，创建本报告前先执行 read-only recovery。

| Item | Live evidence |
| --- | --- |
| Branch | `main...origin/main` |
| HEAD | `f4c24ea8d829325788ce36d8029f71d516eef7f0` |
| origin/main | `f4c24ea8d829325788ce36d8029f71d516eef7f0` |
| Latest commit | `f4c24e Repair Dashboard production URL resolution planning` |
| Working tracked diff | `.gitignore` only |
| Cached diff | empty |
| Re-review target before this task | absent |

The live baseline exactly matches the PM-provided durable baseline. The external dirty artifacts were unchanged and excluded: `.gitignore`; `docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`; `docs/reports/phase1_to_sprint2_management_keynote_10p.html`; `docs/reports/sprint3_db_backed_api_validation_reliability_review.md`; the four listed old PM handoff files; and `frontend/node_modules/`.

## 2. Reviewed commits and authorities

Reviewed commits:

```text
53ade97ed310078d9d52b4e812c72a18392e1e61  Freeze Dashboard production URL resolution planning
5922b4bb1a8ca7b5c95ab2834fff0bcd1a3aefed  Record Dashboard URL resolution Reliability HOLD
f4c24ea8d829325788ce36d8029f71d516eef7f0  Repair Dashboard production URL resolution planning
```

Read in the required order: PM operating rules, current status, Dashboard API contract, browser smoke plan, same-origin no-DB mock-capability plan, original Reliability review, repaired production URL-resolution plan; then the authorized package/config/page/client/query/test surfaces. The repair diff was directly inspected. `git show --stat f4c24ea` proves the repair commit changed only `docs/reports/sprint3_dashboard_production_url_resolution_plan.md`.

`docs/current_status.md` is a historical status control and does not contradict the live Git baseline or the committed repaired authority. Per PM rules, its older authoring baseline is not itself a HOLD condition.

## 3. Original HOLD summary

The original Reliability review recorded `HOLD` because:

- `REL-URL-R1` was a blocker: no unique, complete, testable canonicalization/profile-matching contract.
- `REL-URL-R2` was a blocker: no complete invalid/missing configuration to corrected-restart same-artifact recovery evidence.
- `REL-URL-R3` through `REL-URL-R6` were carry-forward recommendations for snapshot timing, bounded logging, test isolation and deployment readiness.
- `REL-URL-R7` was closed by bounded plan scope.

## 4. Repair diff summary

The repair adds rather than merely labels the missing authority:

- exact closed raw profile forms and production FQDN grammar in plan section 7;
- exact eleven-step raw-precheck → `new URL()` → parsed re-verification algorithm and ambiguity matrix in section 11;
- one immutable per-invocation two-variable snapshot in section 9;
- finite, redacted, non-throwing logging in section 14;
- exact environment restore/isolation rules in section 18;
- same-artifact, two-phase restart recovery acceptance in section 19;
- explicit deployment ownership and unchanged six-file implementation allowlist in sections 15, 17 and 20.

No repair changed the API contract, current frontend source, package/config, tests, mock capability state or deployment topology.

## 5. Canonicalization re-review

Plan section 11.1 freezes one deterministic resolver sequence: both property-existence checks, non-empty checks, leading/trailing whitespace rejection, ASCII-control rejection, non-ASCII rejection, percent rejection, backslash rejection, profile-specific raw closed-form matching, only then `new URL()`, parsed component/profile re-verification, and branded canonical result or typed failure.

This leaves no implementation choice to trim, lowercase, decode, strip, repair or otherwise normalize malformed input. Section 11.1 further requires rejection when parser normalization conflicts with raw policy or changes profile identity. Therefore parser behavior cannot bypass raw policy.

The section 11.2 decision matrix explicitly resolves all original ambiguity classes: optional root slash; uppercase scheme/host; trailing dot; explicit production `:443`; zero-padded port; `[::1]`; expanded IPv6; Unicode/IDN; lower-case ASCII punycode; percent encoding; backslash; duplicate/non-root path; query/fragment/userinfo; empty and single-label production hosts; and port overflow.

## 6. Profile matching re-review

Plan section 7 freezes exact lower-case ASCII raw syntax:

```text
local:
http://127.0.0.1:8000[/]
http://127.0.0.1:3100[/]
http://localhost:8000[/]
http://localhost:3100[/]
http://[::1]:8000[/]
http://[::1]:3100[/]

container:
http://api:8000[/]

production:
https://<lower-case ASCII FQDN>[/]
```

The same section rejects local aliases/implicit ports/alternate IPv6 and container aliases. Production requires lower-case `https`, no explicit port including `:443`, a dotted lower-case ASCII FQDN with bounded labels, root path only and no IP literal, `localhost`, single-label host, trailing dot, userinfo, query or fragment. It permits `xn--...` only as already lower-case ASCII labels passing those grammar rules; it prohibits Unicode-to-punycode conversion, hostname fallback, DNS-derived matching and profile failover.

Section 11.3 defines `TrustedAcceptedEventsApiOrigin` as only `URL.origin`, with no trailing slash, path, query, fragment or userinfo. Sections 9 and 11 require `apiClient.ts` to accept only that brand, prohibit page/client self-construction, and require endpoint composition by `new URL()` plus `URLSearchParams`, not string concatenation.

## 7. Restart recovery re-review

Plan section 19 freezes a future independent runtime gate with the exact evidence topology:

```text
build once
-> run same artifact with missing/invalid pair
-> valid accepted-events page request shows safe kind:"error"
-> zero outbound accepted-events request
-> stop process
-> correct environment
-> restart the same artifact without rebuild
-> valid request yields exactly one corrected absolute accepted-events request
```

It expressly requires one `next build`, no origin value at build, the same `frontend/.next/standalone` artifact in both phases, a new process rather than hot reload, and a first request after restart that reads a new snapshot. Phase A requires zero capture requests and port release. Phase B fixes the exact `local` / `http://127.0.0.1:8000` pair, a separately authorized loopback capture/fixture, exactly one `GET` to the fixed endpoint, only approved query keys, strict parser traversal, no stale environment/no extra request, and process/port/artifact/Git cleanup.

This is a future runtime acceptance requirement only. It neither claims that the probe ran nor reopens the mock-capability HOLD.

## 8. Snapshot/read timing

Plan section 9 requires each resolver invocation to read both environment properties exactly once at its beginning into one immutable local snapshot. All validation, canonicalization, logging category, typed failure and brand must derive from that snapshot; there is no resolver reread, module-import read or build-time snapshot. `page.tsx` and `apiClient.ts` are forbidden from environment reads. Section 18 requires tests for request-time reread and single-snapshot behavior.

## 9. Logging reliability

Plan section 14 freezes a closed `OriginConfigurationErrorCode` enum and module-local `Set<OriginConfigurationErrorCode>`. The finite enum bounds memory and permits at most one safe-code record per process; a restart resets it. It allows only a fixed event marker, safe category, variable names and safely known profile category, excluding raw origin, hostname, URL, query, credentials, headers and user input. Logging is contained as non-throwing, cannot change the typed failure, needs no dependency/logger file, is testable with module isolation/reset, and has no production reset export.

## 10. Test isolation

Plan section 18 requires each environment-mutating test to preserve prior property presence and value, restore the original value in `afterEach` when present and otherwise `delete` it, never write string `"undefined"`, run shared-env cases serially, set a complete pair per case, avoid host-environment defaults, execute restoration after failures, prevent module-cache snapshots, and keep page mocks independent of environment restore. These rules make invalid-config cases unable to contaminate corrected ready-flow cases and make logging dedupe isolation reproducible.

## 11. Deployment readiness carry-forward

Plan section 15 expressly distinguishes generic Next process readiness from accepted-events service readiness. The six-file implementation adds no health endpoint, startup validation, Compose/Next config or deployment docs. A later deployment/config gate owns accepted-events-specific readiness, alerting and operator diagnostics. This is correctly a deployment follow-up, not a claim that current source implementation solves deployment readiness.

## 12. Contract and scope consistency

### 12.1 Profile syntax versus parser

The raw forms and parsed checks agree: optional root slash becomes `URL.origin`; production raw policy excludes `:443` before parsing and parsed port verification preserves that policy; `%` and backslash are rejected before parsing; `localhost` and exact `[::1]` are local-only; expanded IPv6 and trailing dots are rejected; lower-case ASCII punycode is governed by the same FQDN label rule. No raw/parsed contradiction was found.

### 12.2 Logging versus implementation scope

The prescribed enum, process-local set and contained `console.error` can live in `apiOrigin.ts`; no logger utility, dependency, package/config change, page/client responsibility expansion or production reset export is required.

### 12.3 Restart recovery versus mock HOLD

The plan keeps `docs/reports/sprint3_dashboard_same_origin_no_db_mock_capability_plan.md` at `HOLD`. The future loopback capture is runtime recovery evidence under separate authorization, not a mock-capability repair. The repair creates no Route Handler, rewrite, custom server, fixture or mock.

### 12.4 Runtime evidence versus source scope

The two-phase capture/fixture is a future runtime-gate artifact. It does not expand the six-file production source allowlist; `.env.example`, Compose, README and Next config remain outside it, and real deployment values remain a later deployment gate.

### 12.5 Contract preservation

Plan section 6 and the current `apiClient.ts`/`query.ts` preserve the fixed `GET` endpoint, five approved query keys, opaque cursor, `cache: "no-store"`, strict response parser, 22 required DTO keys, explicit-null distinction, error classification, stale-data clearing and `production_accepted_station_event_fact` authority. The repair contains no conflicting contract change.

### 12.6 Exact implementation scope re-check

The repaired plan section 17 keeps exactly this future allowlist:

```text
Create: frontend/src/lib/acceptedStationEvents/apiOrigin.ts
Modify: frontend/src/lib/acceptedStationEvents/apiClient.ts
Modify: frontend/src/app/accepted-events/page.tsx
Create: frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
Modify: frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
Modify: frontend/src/app/accepted-events/__tests__/page.test.tsx
```

It expressly excludes package/lock files, Next/TS config, `.env.example`, Compose, README, logger/config utility, `schema.ts`, `query.ts`, `viewModel.ts`, `loading.tsx` and `error.tsx`. A claimed need to expand it is `HOLD`; no present source requirement makes expansion necessary.

## 13. Finding adjudication R1-R7

### REL-URL-R1

ID: `REL-URL-R1`

Original severity: `BLOCKER`

Re-review status: `CLOSED`

Evidence in repaired authority: plan sections 7, 9, 10, 11.1, 11.2, 11.3, 18, 22 and 23.

Assessment: The repaired authority fixes raw precheck order, all profile-specific exact forms, parser timing and post-parse component checks, ambiguity accept/reject results, no-repair semantics, `URL.origin` canonical brand and `new URL()` endpoint composition. An implementer need not decide a canonicalization, profile-match or parser-normalization rule at implementation time.

Required carry-forward: none.

Gate impact: none.

### REL-URL-R2

ID: `REL-URL-R2`

Original severity: `BLOCKER`

Re-review status: `CLOSED`

Evidence in repaired authority: plan sections 10, 15, 19, 21, 22 and 23.

Assessment: The future runtime gate is fully frozen as one-build/two-process/same-standalone-artifact proof with Phase-A zero request, Phase-B corrected-pair exactly-one request, no rebuild, no hot reload, no stale module/environment snapshot, exact loopback capture boundary and cleanup. This closes the planning blocker; it does not certify a runtime probe.

Required carry-forward: exact future runtime acceptance in plan section 19.

Gate impact: none for planning; runtime execution remains separately authorized.

### REL-URL-R3

ID: `REL-URL-R3`

Original severity: `RECOMMENDATION`

Re-review status: `CLOSED WITH CARRY-FORWARD`

Evidence in repaired authority: plan sections 9, 10, 13, 18 and 23.

Assessment: One invocation must read each variable once into one immutable snapshot, with every downstream decision derived from it and no page/client/import/build reread. This is no longer advisory wording.

Required carry-forward: six-file implementation must implement that snapshot; focused tests must prove per-request reread, exactly-once property access and no module/build freeze.

Gate impact: recommendation.

### REL-URL-R4

ID: `REL-URL-R4`

Original severity: `RECOMMENDATION`

Re-review status: `CLOSED WITH CARRY-FORWARD`

Evidence in repaired authority: plan sections 14, 17, 18, 22 and 23.

Assessment: The closed enum plus finite process-local set, once-per-code behavior, safe payload limitation, restart reset and non-throwing containment resolve repeated logging, leakage and error-path reliability without scope expansion.

Required carry-forward: implementation/tests must demonstrate finite once-per-code dedupe, redaction, contained logging failure and module-isolated reset behavior.

Gate impact: recommendation.

### REL-URL-R5

ID: `REL-URL-R5`

Original severity: `RECOMMENDATION`

Re-review status: `CLOSED WITH CARRY-FORWARD`

Evidence in repaired authority: plan section 18 and HOLD conditions in section 23.

Assessment: Exact property-presence restoration, serial pair setup, failure-safe `afterEach`, no host defaults, cache isolation and mock/env separation remove the original environment-sharing ambiguity.

Required carry-forward: the three authorized test files must apply and prove these rules, including invalid-to-valid isolation.

Gate impact: recommendation.

### REL-URL-R6

ID: `REL-URL-R6`

Original severity: `RECOMMENDATION`

Re-review status: `CLOSED WITH CARRY-FORWARD`

Evidence in repaired authority: plan sections 15, 17, 20 and 26.

Assessment: The repair explicitly says generic Next readiness is not accepted-events readiness, preserves the no-health/no-startup-validation/no-deployment-doc scope, and assigns readiness, alerting and diagnostics to a later deployment/config gate.

Required carry-forward: future deployment/config gate must define accepted-events-specific readiness, alerting and operator diagnostics, including deployment DNS/egress ownership.

Gate impact: recommendation; not a current six-file source blocker.

### REL-URL-R7

ID: `REL-URL-R7`

Original severity: `NOTE`

Re-review status: `CLOSED`

Evidence in repaired authority: plan sections 5, 6, 19, 23 and 26.

Assessment: The bounded repair explicitly excludes retry, timeout, circuit breaker, fallback and secondary origin. The recovery proof also requires no fallback and no extra request. No scope expansion supersedes this decision.

Required carry-forward: none.

Gate impact: none.

## 14. New findings

```text
none
```

No `REL-URL-R8` finding is required. The repaired authority has no identified internal contradiction, contract change or allowlist insufficiency.

## 15. Blocking findings

```text
none
```

## 16. Carry-forward requirements

- `REL-URL-R3`: implementation/test proof of a single immutable request-time pair snapshot and no extra environment reads.
- `REL-URL-R4`: implementation/test proof of finite safe-code dedupe, redaction and non-throwing logging containment.
- `REL-URL-R5`: authorized test implementation must use exact environment restore, serial shared-env execution and cache/mock isolation.
- `REL-URL-R6`: a separate deployment/config gate must decide accepted-events readiness, alerting, operator diagnostics, DNS and egress.
- `REL-URL-R2`: separately authorized runtime recovery gate must execute, not merely restate, plan section 19 same-artifact evidence.

These are carry-forward acceptance obligations, not blockers for the repaired planning authority and not authorization to implement, test, build, run or deploy.

## 17. Implementation readiness

The repaired plan is implementation-ready for the next PM-authorized review sequence: `REL-URL-R1` and `REL-URL-R2` are closed; the remaining obligations are explicit, bounded and assigned to implementation/test/runtime/deployment gates; no package/config/deployment source expansion is necessary; and no current contract or mock-capability HOLD is reopened.

## 18. PASS conditions

A bare `PASS` would require no carry-forward recommendation. This re-review intentionally retains explicit implementation/test/deployment follow-up, so the applicable conclusion is `PASS WITH RECOMMENDATIONS` rather than `PASS`.

## 19. HOLD conditions

The next gate must return `HOLD` if any of the following appears: raw input repair or implicit normalization; case-insensitive/DNS-equivalent matching; unlisted default-port or IPv6 acceptance; Unicode conversion; reread/mixed environment pair; import/build snapshot; hot-reload claim; missing Phase A/B runtime evidence; unbounded/throwing/leaking logging; shared-env test leakage; fallback/client leak/unexpected request; contract/parser/authority/query/cursor/cache/stale-data drift; or a need to expand the six-file/package/config/deployment/mock scope.

## 20. Required next action

Eligible next action: exact-path Reliability re-review authority commit for this report, subject to PM intake and explicit commit authorization.

PM authorization is still required before committing this report; starting Data Quality, Verification or Security review; implementation; tests/typecheck/build; runtime recovery validation; mock-capability planning; or any Git/deployment operation.

## 21. Thread output/context assessment

- 本次输出长度：长（durable re-review authority；window report 应保持简洁）。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：本 re-review 已完成独立裁决；exact-path commit、后续 cross-functional review、implementation、runtime recovery 和 deployment gate 都需要独立 PM authorization，不能继承本次 review-only 权限。

## Summary

```text
Blocking findings: none
Closed findings: REL-URL-R1, REL-URL-R2, REL-URL-R7
Closed with carry-forward: REL-URL-R3, REL-URL-R4, REL-URL-R5, REL-URL-R6
Open findings: none
New findings: none
Implementation readiness: yes, subject to future PM authorization and carry-forward acceptance
```
