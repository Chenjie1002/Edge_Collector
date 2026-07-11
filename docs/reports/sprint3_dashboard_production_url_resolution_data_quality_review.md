# Sprint 3 Dashboard production URL-resolution Data Quality planning review report

报告名称：Sprint 3 Dashboard production URL-resolution Data Quality planning review report

任务名称：Review the repaired Dashboard URL-resolution authority for production-fact lineage, strict response semantics and no-data-substitution guarantees

执行 Thread：Data Quality

风险等级：Level 1 review-only；被审查的 future implementation remains Level 2。

结论：**PASS WITH RECOMMENDATIONS**

本 review 只审查已提交的 URL-resolution planning authority 是否保持 Dashboard accepted-facts 的 production-fact、response-contract 与 stale-data 边界；不授权 implementation、tests、typecheck/build、runtime capture、browser/server、API、DB、Docker、stage、commit 或 push。

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
