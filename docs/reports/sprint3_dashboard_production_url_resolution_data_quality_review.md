# Sprint 3 Dashboard production URL-resolution focused Data Quality re-review report

报告名称：Sprint 3 Dashboard production URL-resolution focused Data Quality re-review report

任务名称：Re-review the `d75c547` VER-URL-V1 resolver-contract repair after focused Reliability acceptance

执行 Thread：Data Quality

风险等级：Level 1 review-only；被审查的 future implementation remains Level 2。

结论：**PASS WITH RECOMMENDATIONS**

本次 focused re-review 独立审查 `d75c5477251de1b60f7a16e5d8803fd7c20f5b38`
对 resolver result、error-code、brand 和 typed environment seam 的 planning repair，确认其
是否保持 Dashboard accepted-facts 的 production-fact authority、严格 DTO/parser 语义、
transport/business profile 隔离以及 no-data-substitution 边界。Reliability 已在
`2483f2bec01a6ff19dab9432b28bfd0bd120814c` 接受该修复的 Reliability planning
authority；该结论只作为 review 输入，不替代本 Data Quality 独立裁决。

本 gate 不授权 implementation、tests、typecheck、build、runtime capture、browser/
server、API、DB/Postgres、Docker、status sync、stage、commit 或 push。

## A.1 Live baseline and read-only recovery

本次第一动作是 read-only recovery；在恢复前未修改文件或运行测试/runtime。

| Item | Live evidence |
| --- | --- |
| Branch | `main...origin/main` |
| HEAD | `2483f2bec01a6ff19dab9432b28bfd0bd120814c` |
| origin/main | `2483f2bec01a6ff19dab9432b28bfd0bd120814c` |
| Latest commit | `2483f2b Re-review Dashboard resolver contract reliability` |
| Parent | `6482e64344dd64c669a1602985081d24032f88df` |
| Ahead / behind | `0 / 0` |
| Cached diff | empty |
| Existing tracked diff | `.gitignore` only |
| Current review authority | committed historical report at `bb1935a` |

Expected external artifacts remained unchanged and excluded from this gate:

```text
M  .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
?? frontend/node_modules/
```

No unexpected staged file, source/config/package drift or authority collision was found.

## A.2 Reviewed authority and source boundaries

Focused review inputs:

```text
d75c547  Repair Dashboard URL resolution resolver contract
2483f2b  Re-review Dashboard resolver contract reliability
bb1935a  Record Dashboard URL resolution Data Quality review
```

`git show` confirms `d75c547` changed only
`docs/reports/sprint3_dashboard_production_url_resolution_plan.md`, and `2483f2b`
changed only the Reliability re-review report. Neither commit changed frontend source,
API contract, schema, query, view model, package/config or runtime topology.

The review re-read the Dashboard API contract, repaired URL-resolution plan, focused
Reliability conclusion, historical Data Quality authority, and current accepted-events
`page.tsx`, `apiClient.ts`, `schema.ts`, `viewModel.ts`, state component and focused
page/client tests. No resolver implementation exists yet; that is the expected
pre-implementation state, not a defect.

## A.3 Review question and bounded scope

The focused question is whether the new executable resolver contract can alter or
contaminate production fact meaning. The allowed future data flow remains:

```text
validated query
-> transport-only resolver result
-> fixed accepted-events endpoint
-> existing response classification
-> strict accepted-events parser
-> accepted-fact view model
-> ready or non-ready UI state
```

The resolver may decide only whether one trusted absolute root exists. It may not
select facts, add response metadata, reinterpret `profile_id`, synthesize an envelope,
modify query scope, preserve stale ready data or create a second source path.

## A.4 Resolver result union and UI-data isolation

**PASS.** The repaired authority freezes exactly:

```text
success own keys: ok, origin
failure own keys: ok, code, message
```

The failure message is the fixed safe literal:

```text
Accepted events service is not configured.
```

The plan explicitly forbids raw origin, raw profile, hostname, URL, query, headers,
credentials, parser error, stack, cause, diagnostic metadata or logging state from
entering either result branch. `page.tsx` must use only the `ok` discriminant and the
fixed failure `message`; it must not inspect or render `code`.

The existing page-state authority accepts only `kind` and `message` for `error`. It has
no transport profile, configuration code, origin or diagnostic slot. Therefore a
configuration failure cannot become an API DTO, ready view model, trace reference,
summary dimension or accepted-fact lineage value.

Future page tests must prove the generic error is visible while raw values, safe code,
transport profile and prior production surfaces remain absent. This is carry-forward
evidence, not an authority blocker.

## A.5 Transport profile versus accepted-fact `profile_id`

**PASS WITH RECOMMENDATION.** The two concepts remain separate:

```text
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE
  = local | container | production
  = outbound transport policy only

profile_id
  = production_accepted_station_event_fact.profile_id
  = response-owned accepted-fact lineage only
```

`AcceptedEventsApiOriginEnvironment` contains only two optional readonly transport
properties and is expressly forbidden from acquiring business `profile_id`, query,
headers, response data or fallback URL. The page must not pass the transport profile
to the client or view model. The resolver success path passes only the branded root
origin; the API response remains the sole source of item `profile_id`.

Current `schema.ts` contains `profile_id` only in the frozen 22-field DTO allowlist, and
`viewModel.ts` copies it only from the parsed item into `TraceReference.profileId`.
Current source has no environment-origin/profile imports or mapping. No
`schema.ts`, `query.ts` or `viewModel.ts` change is needed.

`DQ-URL-D1` remains carry-forward because implementation evidence must still prove
that `local`, `container` and `production` never overwrite/filter/render as business
`profile_id`, and that a ready trace reference preserves the response value exactly.

## A.6 Production fact authority and strict response semantics

**PASS.** The repaired resolver contract changes no data authority:

- only `production_accepted_station_event_fact` supplies consumer-facing facts;
- endpoint remains `GET /api/v2/production/accepted-station-events`;
- query authority remains the exact five keys and opaque API-owned cursor;
- response remains exact `{data,page}` / `{items}` / `{next_cursor,limit}`;
- all 22 item own keys remain required;
- explicit JSON `null` remains distinct from missing;
- unknown own keys remain forbidden;
- malformed 2xx remains `kind: "error"`;
- no raw/debug/diagnostic/candidate/review/audit source or fallback is introduced.

`schema.ts` still performs exact own-key validation at envelope, data, page and item
levels before copying values. A resolver result cannot bypass or populate that parser.
The API client must continue to send successful JSON through
`parseAcceptedStationEventsEnvelope()` before a ready result exists.

## A.7 Failure classification, stale truth and no substitution

**PASS.** The repaired sequence remains:

```text
invalid query
-> invalid-query before resolver/fetch

valid query + invalid/missing transport config
-> error with fixed message
-> zero client call
-> zero fetch
-> zero ready production surfaces

successful transport + malformed 2xx
-> error through strict parser

successful transport + valid exact response
-> ready from current response only
```

Configuration failure is not `empty`, `unavailable` or an accepted-fact absence claim.
It is a transport-configuration error. Existing page rendering returns early for every
non-ready state, so table, current-page summary, NOK evidence, trace reference and
cursor surfaces are absent. The repair adds no cache, old-result reuse, target/profile
merge, fixture fallback or missing-to-empty conversion.

This preserves the rule that empty means a valid exact response containing zero
accepted facts in the bounded query scope; configuration error never means empty.

## A.8 Safe logging versus production evidence

**PASS WITH CARRY-FORWARD.** The server log may contain only a fixed event marker, one
of eight safe configuration codes, fixed variable names and a safely known transport
profile category. It may not contain origin/hostname/raw profile, query scope,
credentials, response DTO values, DMC, unit ID, fact/source IDs, NOK evidence,
`profile_id`, accepted timestamps or parser payload.

Logging is outside resolver result, API response and view state. A logging failure must
not change the failure code/message or create a ready result. Future logging tests must
prove redaction and non-throwing containment; they are Reliability/Data Quality
carry-forward evidence inside `apiOrigin.test.ts`, not justification for a logger,
schema or DTO scope expansion.

## A.9 Runtime fixture and evidence classification

**PASS WITH RECOMMENDATION.** `VER-URL-V3` remains a dedicated future runtime-planning
gate. The repaired plan does not authorize a fixture or claim production-fact evidence.
It requires the future gate to distinguish:

```text
transport/request-count evidence
synthetic strict-parser fixture evidence
real production-fact evidence
```

A request-capture body that is malformed may prove method/path/query/count, but its
page outcome must remain `error`; it cannot be reported as ready or production-fact
evidence. A synthetic exact 22-key body can prove parser/view behavior only and still
is not DB-backed production evidence. `DQ-URL-D2` therefore remains carry-forward.

## A.10 Full regression evidence

**PASS WITH RECOMMENDATION.** The six-file focused implementation can add resolver and
page/client tests without modifying strict schema/view-model tests. However, focused URL
tests alone cannot certify the entire accepted-fact contract. A later authorized full
frontend regression must still execute existing schema/query/view-model/page/client
coverage for:

- exact 22 keys and explicit-null versus missing semantics;
- unknown-key and malformed-envelope rejection;
- malformed 2xx error classification;
- current-page-only summary;
- response-owned lineage and NOK evidence;
- stale-data removal across non-ready states.

`DQ-URL-D3` remains carry-forward. No additional test file or source-file expansion is
needed.

## A.11 Exact implementation allowlist assessment

**PASS.** The repaired authority remains implementable within exactly six files:

```text
Create frontend/src/lib/acceptedStationEvents/apiOrigin.ts
Modify frontend/src/lib/acceptedStationEvents/apiClient.ts
Modify frontend/src/app/accepted-events/page.tsx
Create frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
Modify frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
Modify frontend/src/app/accepted-events/__tests__/page.test.tsx
```

Data Quality requires no change to `schema.ts`, `query.ts`, `viewModel.ts`, components,
API, DB, package/lockfile, Next/TS config, Compose, README or dependency set. A claimed
need to place transport fields in DTO/view state, alter parser/query/view model, add a
fixture source or expand the six-file allowlist is `HOLD`, not permission to expand.

## A.12 Finding adjudication

### DQ-URL-D1

```text
Status: CARRY FORWARD
Severity: RECOMMENDATION
Area: transport profile / accepted-fact profile_id isolation
```

The planning authority now states the isolation directly and prohibits `code`/profile
from entering DTO or view state. Implementation tests still must prove it using the
public page/client/resolver boundaries. No planning blocker remains.

### DQ-URL-D2

```text
Status: CARRY FORWARD
Severity: RECOMMENDATION
Area: runtime fixture/evidence classification
```

The future runtime gate must separately label transport capture, synthetic strict-parser
fixture and real production-fact evidence. No runtime mechanism is authorized here.

### DQ-URL-D3

```text
Status: CARRY FORWARD
Severity: RECOMMENDATION
Area: full frontend contract regression
```

Future validation must run the existing full regression without expanding the focused
source/test allowlist.

### New findings

```text
none
```

### Blocking findings

```text
none
```

## A.13 VER-URL-V1 Data Quality decision

The `d75c547` planning repair is accepted from the Data Quality perspective:

```text
VER-URL-V1 Data Quality acceptance:
yes, planning authority only

Data Quality gate:
PASS WITH RECOMMENDATIONS

Data Quality blockers:
none

Carry-forward:
DQ-URL-D1
DQ-URL-D2
DQ-URL-D3

VER-URL-V1 cross-functional closure:
pending independent Verification re-review

Verification gate:
remains HOLD
```

This decision does not overwrite Verification authority and does not authorize
implementation, tests, build or runtime evidence.

## A.14 Authorization and next gate

```text
Focused Data Quality re-review: completed
Data Quality report commit/push: not authorized
Verification re-review: not authorized
Security/privacy planning review: not authorized
Implementation: not authorized
Tests/typecheck/build: not authorized
Runtime planning/validation: not authorized
Status sync: not authorized
```

After a separately authorized exact-path commit of this report, the recommended next
technical gate is:

```text
Verification re-review of the repaired VER-URL-V1 planning authority
```

Do not start Verification, Security/privacy or implementation from this report without
a new exact PM authorization.

---

## Historical Data Quality planning review — bb1935a

The sections below preserve the earlier Data Quality adjudication. Git history remains
the source of truth for the exact pre-`d75c547` report revision.

## 1. Baseline and recovery

创建报告前已执行指定的 read-only recovery。

| Item | Live evidence |
| --- | --- |
| Branch | main...origin/main |
| HEAD | 62e1424eff54fdbe4672f06ad2408dbf8b32430a |
| origin/main | 62e1424eff54fdbe4672f06ad2408dbf8b32430a |
| Latest commit | 62e1424 Close Dashboard URL resolution Reliability planning review |
| Cached diff | empty |
| Existing tracked diff | .gitignore only |
| Review target before this task | absent |

Expected external artifacts were present and excluded: .gitignore, the listed old PM handoffs, the Keynote HTML, the DB-backed Reliability report, and frontend/node_modules/. No target collision, unexpected HEAD advance, staged file, or authority conflict was found.

## 2. Reviewed authorities and source

已按顺序读取 PM operating rules、current status、Dashboard API contract、five named Dashboard validation/smoke/mock/URL-resolution plans、both Reliability authorities；并只读审计 PM 指定的 page/client/query/schema/view-model/components 和全部指定 tests。也执行了 call-site、parser、query-key、error-state、stale-data、summary、fact-authority、fallback 与 fixture/capture wording 搜索。

未运行 tests、typecheck/build、server、probe、mock、API 或 DB。

## 3. Review scope

被审查的 repair 只能改变 Server Component outbound transport target：query validation 之后，使用 trusted origin 组合既有 endpoint，然后保持既有 response classification、strict parser、view model 和 UI state。它不得选择 facts、变换 DTO、改变 parser、保留旧数据或创建第二条数据路径。

## 4. Production fact authority

**PASS.** 唯一 consumer-facing authority 是 production_accepted_station_event_fact。URL plan 明确 origin/profile 仅决定 API transport target，不参与 fact selection；没有 profile inference、local fixture、browser cache、static data、old result、alternate endpoint 或 source-table fallback。

Contract 明确禁止 raw_plc_sample、cycle_event、station_event、production_unit、quality_event、production_snapshot、production_events 作为 equivalent/fallback/filler。当前 frontend 无这些 source imports 或 joins。配置/上游失败进入 non-ready state，而不是数据替代。

## 5. Endpoint and query contract

**PASS.** Future repair preserves exactly:

~~~text
GET /api/v2/production/accepted-station-events
line_id
start_time
end_time
limit
cursor
~~~

buildAcceptedStationEventsQuery() and URLSearchParams remain query authority. Resolver only returns a branded root origin; new URL() composes the fixed path and cannot supply path prefix/query/fragment. The plan forbids profile-specific endpoint, extra query key and resolver-based query/origin selection.

query.ts preserves cursor opacity: it passes cursor unchanged and clears it only when line/time/limit scope changes; it does not decode, normalize or inspect cursor. Existing page validation remains before resolver, so invalid query is invalid-query before any request.

## 6. Response outer schema

**PASS.** Endpoint-specific exact schema stays:

~~~text
outer: { data, page }
data:  { items }
page:  { next_cursor, limit }
~~~

schema.ts uses assertExactOwnKeys() at outer/data/page/item levels. Missing and unknown own keys fail, including meta, status, message, debug, source, origin, profile, authority, trace, diagnostic and fallback. The plan does not alter parser allowlists or transmit origin/profile/config diagnostics into response, view model or UI.

## 7. 22-key DTO

**PASS.** acceptedStationEventFields holds the frozen 22 own keys and contract binds all of them directly to production_accepted_station_event_fact. parseItem() establishes exact own-key equality before copying validated values. URL origin, transport profile, api_origin and source_host are not DTO fields.

The plan distinguishes transport EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE from business item profile_id. There is no proposed mapping, overwrite, filter or UI substitute; future direct isolation proof remains DQ-URL-D1.

## 8. Null, missing and unknown semantics

**PASS.**

~~~text
explicit JSON null: legal where schema permits
missing required own key: illegal
unknown own key: illegal
~~~

The parser tests cover explicit null for every item key, true deletion of every required key, unsupported envelope/item keys and prototype-looking own keys. schema.ts copies validated values directly; it neither uses missing-to-null normalization nor default field filling. URL composition cannot delete, synthesize or repair fields.

## 9. Parser and malformed 2xx

**PASS.** apiClient.ts gives successful JSON to parseAcceptedStationEventsEnvelope(); JSON/parser failure is caught as kind: error. Existing tests prove malformed outer/data/page and missing-item-key 2xx responses cannot become ready, empty, invalid-query or unavailable.

The repair explicitly preserves strict parser traversal after absolute URL composition. Successful origin validation is transport-only, not payload validation. Fixture/capture must not inject view model or bypass parser.

## 10. Error classification

**PASS.**

~~~text
invalid query before request -> invalid-query
missing/invalid API origin -> error
API 4xx -> invalid-query
API 503 -> unavailable
other non-2xx -> error
network/DNS/TLS/redirect failure -> error
malformed 2xx -> error
~~~

Resolver runs after query validation. Configuration failure uses existing error with zero fetch, never empty or unavailable. redirect: error remains generic error. Safe bounded logging does not enter UI data.

## 11. Stale-data behavior

**PASS.** AcceptedEventsPageView returns early for non-ready state; only ready owns table, summary, NOK/detail evidence and trace reference. page.test.tsx already proves ready-to-loading/error/unavailable/invalid-query removal, and non-empty ready to current empty replacement removal including summary and both detail surfaces.

The plan preserves force-dynamic and cache: no-store, and forbids module-level response cache, fallback cache, profile-held data, previous-result reuse and cross-target merging. Configuration error therefore exposes no old items, summary, detail, fact reference or cursor.

## 12. Current-page summary

**PASS.** toAcceptedEventsViewModel() computes rows, byResult, byStation and totalAcceptedFacts only from the current envelope.items, labels it Current page only, and uses neither origin, transport profile, cursor inference nor cached pages. URL resolution cannot merge Phase A/Phase B, targets or profiles.

## 13. Timestamp and lineage

**PASS.** accepted_at remains Accepted fact timestamp only, not fetch/render/response/origin-resolution/restart/capture time, freshness, ACK or read_done. source_event_id, fact_key, content_fingerprint, nok_detail_source_event_id and nok_detail_evidence_fact_key remain parsed accepted-fact values. Resolver creates/recalculates none and cannot use origin/profile as business/config lineage.

## 14. Transport profile versus profile_id

**PASS WITH RECOMMENDATION.**

~~~text
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: local | container | production
profile_id: accepted-fact item field
~~~

Transport profile validates only the outbound root. It does not mean profile_id=production; local transport may return any legal item profile_id. Parser, view model, table and summary may not derive/filter business profile from transport config. No schema.ts/query.ts/viewModel.ts change is needed. DQ-URL-D1 requires explicit future regression assertions.

## 15. Runtime fixture/capture boundary

**PASS WITH RECOMMENDATION.** Loopback capture remains a separately authorized runtime gate and same-origin mock capability remains HOLD.

- Request-capture-only evidence may return malformed data to prove method/path/query/count, but the page result must be kind: error; it is not ready/data-correctness proof.
- Ready-state evidence must contain exact outer/data/page schema, complete 22 own keys, permitted explicit null, legal cursor/page limit and no unknown keys; it must traverse strict parser.
- Both are synthetic transport/contract evidence, not DB evidence or proof of production_accepted_station_event_fact availability. They can never be missing-config fallback/business authority.

The runtime report must separately label transport evidence, synthetic complete-contract fixture evidence and real production-fact evidence. DQ-URL-D2 records this obligation.

## 16. Reliability carry-forward interaction

REL-URL-R3 snapshot includes only transport config, never query response/business data, and cannot enable response reuse. REL-URL-R4 logging excludes response/DTO values, DMC, unit_id, fact/source IDs, NOK evidence, query scope and raw host/origin; failure cannot affect classification. REL-URL-R5 requires case-isolated environment/mocks/fixtures and separate malformed/null/missing assertions through parser. REL-URL-R6 correctly separates generic process ready from config/transport/payload data ready. None changes fact authority.

## 17. Exact implementation scope assessment

**PASS.** The six-file implementation allowlist is sufficient:

~~~text
Create: frontend/src/lib/acceptedStationEvents/apiOrigin.ts
Modify: frontend/src/lib/acceptedStationEvents/apiClient.ts
Modify: frontend/src/app/accepted-events/page.tsx
Create: frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
Modify: frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
Modify: frontend/src/app/accepted-events/__tests__/page.test.tsx
~~~

schema.ts, query.ts and viewModel.ts already own strict parsing/query/cursor/summary semantics; transport has no valid reason to modify them. No API, DB, component, package, lockfile, config or dependency change is required. A claimed need is HOLD, not scope expansion.

## 18. Test and evidence sufficiency

Future carry-forward evidence must cover:

- API client: exact absolute endpoint, exact five keys, opaque cursor encoding, GET/no-store/omit/redirect-error, unchanged classification and malformed-2xx parser error.
- Page: invalid query before resolver/fetch; invalid origin error/no fetch; full legal body ready; malformed body error; no stale truth surfaces; no transport profile in view state; response-owned profile_id.
- Existing schema.test.ts and viewModel.test.ts remain read-only but must execute in future full frontend regression to prove 22 fields, explicit null, missing/unknown keys, malformed envelope/page and NOK evidence.
- Runtime capture must distinguish request-only malformed evidence from complete ready-fixture evidence and clean up.

No schema.test.ts or viewModel.test.ts modification is required.

## 19. Findings

### DQ-URL-D1

ID: DQ-URL-D1

Severity: RECOMMENDATION

Status: CARRY FORWARD

Area: DTO / Tests

Finding: Authority distinguishes transport profile and item profile_id, but future test bullets do not yet name a direct isolation assertion.

Evidence: URL plan sections 7, 9, 10, 13 and 18 restrict transport profile to origin validation; schema.ts/viewModel.ts consume item values only. The authorized future tests include apiOrigin.test.ts, apiClient.test.ts and page.test.tsx.

Required resolution: implementation test carry-forward. Prove local/container/production never enter DTO/view state or filter items, and ready item profile_id equals the response value, not environment.

Gate impact: PASS WITH RECOMMENDATIONS.

### DQ-URL-D2

ID: DQ-URL-D2

Severity: RECOMMENDATION

Status: CARRY FORWARD

Area: Fixture / Runtime

Finding: Future loopback topology needs explicit evidence classification so request capture cannot be misreported as production fact or ready-data evidence.

Evidence: URL plan section 19 requires loopback synthetic capture/fixture and strict-parser traversal; mock capability remains HOLD; contract requires malformed 2xx -> kind: error.

Required resolution: runtime carry-forward. Separately label request-only transport evidence, synthetic complete-contract ready fixture evidence and real production-fact evidence; malformed capture outcome is error, ready only follows full strict parser.

Gate impact: PASS WITH RECOMMENDATIONS.

### DQ-URL-D3

ID: DQ-URL-D3

Severity: RECOMMENDATION

Status: CARRY FORWARD

Area: Tests

Finding: The six-file implementation scope correctly excludes schema/query/view-model edits, but strict contract tests require later full frontend regression evidence rather than inference from focused URL tests.

Evidence: schema.test.ts covers exact keys/null/missing/leakage; viewModel.test.ts covers current-page-only and lineage display; URL plan orders full frontend tests after focused tests.

Required resolution: test carry-forward. Future validation report records full schema/view-model regression without expanding source allowlist.

Gate impact: PASS WITH RECOMMENDATIONS.

## 20. Blocking findings

~~~text
none
~~~

## 21. Carry-forward recommendations

~~~text
DQ-URL-D1
DQ-URL-D2
DQ-URL-D3
REL-URL-R3
REL-URL-R4
REL-URL-R5
REL-URL-R6
~~~

## 22. Implementation readiness

**yes.** The repair can remain transport-only inside six files. It needs no schema/query/view-model change and no Data Quality architecture repair. The recommendations are bounded future evidence, not unresolved authority.

## 23. PASS conditions

A later gate passes only if it preserves endpoint/five keys/cursor opacity, exact parser, 22-key/null/missing/unknown semantics, error mapping, no-store/no-stale behavior, current-page-only summary, accepted-fact timestamp/lineage and fact authority; isolates transport profile from item profile_id; and closes DQ-URL-D1 through DQ-URL-D3 at their designated gates.

## 24. HOLD conditions

HOLD for source/profile fallback; endpoint/query change; cursor decoding/rewrite; transport-to-business profile mapping; parser bypass; malformed 2xx ready/empty/unavailable; missing-to-null repair; ignored unknown key; old data on configuration error; fixture presented as production fact; transport reinterpretation of accepted_at/lineage; needed schema/query/view-model edit; or non-six-file/package/config/dependency/mock expansion.

## 25. Required next action

Eligible next action: exact-path Data Quality review authority commit, subject to PM intake and explicit commit authorization.

PM authorization is required before commit, Verification/Security review, implementation, tests/typecheck/build or runtime recovery/capture work.

## 26. Thread output and context assessment

- 本次输出长度：长（durable review authority；window report 应保持简洁）。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：Data Quality 已完成独立裁决；commit、后续 review、implementation、test 与 runtime evidence 属于新的授权边界。

## Summary

~~~text
Blocking findings: none
Carry-forward recommendations: DQ-URL-D1, DQ-URL-D2, DQ-URL-D3
Closed-by-plan findings: none
New implementation files required: none
Schema/query/viewModel changes required: no
Implementation readiness: yes, subject to PM authorization and carry-forward evidence
~~~
