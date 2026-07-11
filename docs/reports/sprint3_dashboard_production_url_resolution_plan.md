# Sprint 3 Dashboard production URL-resolution planning gate report

报告名称：Sprint 3 Dashboard production URL-resolution planning gate report

任务名称：Design a secure and deployment-safe absolute API URL resolution boundary for the Dashboard accepted-events Server Component

执行 Thread：Architecture / Integration

风险等级：Level 1 planning-only；future implementation remains Level 2 because it changes the production Server Component outbound fetch target.

结论：**PASS WITH RECOMMENDATIONS**

本报告冻结 server-only、request-time、fail-closed 的 absolute API URL-resolution
boundary，并已按 Reliability HOLD repair 补足 deterministic canonicalization、restart
recovery 和 carry-forward acceptance。它不授权 implementation、tests、runtime probe、
deployment、configuration write、status sync、stage、commit 或 push。

Architecture planning repair has addressed the documented
Reliability HOLD findings in the planning authority.

The Reliability gate remains HOLD until an independent
Reliability re-review accepts the repaired authority.

## 1. Baseline and read-only recovery

本 report 的原始 planning gate 在写入前执行 read-only recovery；没有在恢复前写入、
启动 server、运行 probe/tests/typecheck/build、安装 dependency，或连接 API/DB/Docker。
本次 repair 也只修改本 report，且不得把下列历史 authoring baseline 当作 live Git truth。

| Item | Original planning-gate evidence |
| --- | --- |
| Branch | `main...origin/main` |
| HEAD | `4715456dec23edacebe0cb3d59a23e3cb587a9fe` |
| origin/main | `4715456dec23edacebe0cb3d59a23e3cb587a9fe` |
| Latest commit | `4715456 Record Dashboard mock capability planning HOLD` |
| Cached diff | empty |
| Tracked diff before original report | `.gitignore` only |
| Target report before original gate | absent |

External dirty artifacts are excluded from this planning authority. They must never
be cleaned, staged, or modified without separate exact-path PM authorization.

## 2. Context reviewed

The authority is bounded by `docs/contracts/dashboard_api_contract.md`, the browser
smoke and same-origin mock-capability plans, the current accepted-events page/client/
query tests, and the Reliability review
`docs/reports/sprint3_dashboard_production_url_resolution_reliability_review.md`.

The current `frontend/` has no API-origin environment variable, header-derived
origin, rewrite, Route Handler, custom server, frontend Docker service, or configured
proxy. `next.config.ts` has `output: "standalone"`. Those facts do not authorize a
runtime or deployment change in this report.

## 3. Proven runtime defect

The independent runtime feasibility probe already closed the transport fact below;
this report does not rerun it:

| Evidence | Confirmed result |
| --- | --- |
| Valid accepted-events page query | HTTP 200 page response |
| Rendered UI state | `state-error` |
| Relative URL parse-error marker | present |
| `GET /api/v2/production/accepted-station-events` | not observed |
| API GET log count | `0` |
| Probe conclusion | `PASS` / `RELATIVE_URL_PRE_HTTP_FAILURE` |

The current source calls a relative accepted-events URL, so the repair target is a
controlled absolute URL resolver rather than same-origin transport guessing or a
relative URL fallback.

## 4. Current frontend/API deployment topology

| Surface | Current fact | Consequence |
| --- | --- | --- |
| Dashboard | Next.js `16.2.10`; dynamic Server Component; `output: "standalone"` | browser origin cannot establish the Node server API target |
| API | separate Compose `api` service; container and host port `8000` | it is not the Dashboard process or port |
| Compose | no frontend service or Dockerfile | `api` hostname is not a current host-runtime guarantee |
| `.env.example` | no Dashboard/API origin variable | no implicit default is available |
| Reverse proxy | none configured | forwarded headers have no established trust model |

Browser-visible and server-side API origins remain independent. `http://api:8000`
has meaning only in a future frontend container attached to the appropriate Compose
network; it is not a host-runtime `localhost` replacement.

## 5. Scope and non-goals

This report plans only the secure URL-resolution boundary for
`GET /api/v2/production/accepted-station-events`.

Out of scope: mock response/fixture, browser automation, API/contract changes,
endpoint changes, retry, timeout, circuit breaker, fallback, secondary origin,
auth/authz/token, gateway/load balancing, DB, Docker implementation, real/local API
validation, Collector/V-PLC/PLC, package changes, Next config changes, status/handoff
sync and every Git write after this report. A need for any such work is a new exact-
scope gate, not an implementation detail.

## 6. Contract and authority invariants

Future work must preserve all of the following without reinterpretation:

- only `GET /api/v2/production/accepted-station-events`;
- only `line_id`, `start_time`, `end_time`, `limit`, `cursor`; query construction
  remains `buildAcceptedStationEventsQuery()` / `URLSearchParams` authority;
- `cache: "no-store"`, `credentials: "omit"`, `redirect: "error"`, current-page-only
  summary and stale-data clearing;
- exact `{data,page}` / `{items}` / `{next_cursor,limit}`, all 22 DTO own keys,
  explicit JSON `null`, and malformed 2xx as `kind: "error"`;
- 4xx → `invalid-query`, 503 → `unavailable`, other non-2xx/transport/parser →
  `error`;
- only `production_accepted_station_event_fact` is fact authority; no raw/debug/
  diagnostic/candidate/review/audit leakage, `work_order`, or `product`;
- `accepted_at` remains an accepted-fact timestamp, never freshness/ACK/read_done.

No resolver may synthesize data, alter query semantics, retry, select a fallback
endpoint, or make malformed response data look empty or ready.

## 7. API origin requirements

The source is exactly two server-only runtime variables:

```text
EDGE_MES_DASHBOARD_API_ORIGIN
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE
```

They are a paired closed configuration contract. There is no `.env`, relative URL,
localhost, `api`, browser-origin, request-header, mock, profile-failover, or default
fallback. `NEXT_PUBLIC_*` is forbidden: neither value may enter browser code, props,
responses, or a client bundle.

The only accepted raw forms are these exact lower-case ASCII forms. A trailing root
slash is optional where shown; no other spelling is equivalent.

| Profile | Accepted raw syntax | Allowed use |
| --- | --- | --- |
| `local` | `http://127.0.0.1:8000[/]`, `http://127.0.0.1:3100[/]`, `http://localhost:8000[/]`, `http://localhost:3100[/]`, `http://[::1]:8000[/]`, `http://[::1]:3100[/]` | local API or separately authorized loopback-only capture/mock validation |
| `container` | `http://api:8000[/]` | future frontend container on the matching Compose network only |
| `production` | `https://<lower-case ASCII FQDN>[/]` | separately authorized standalone/reverse-proxy deployment |

`local` rejects all other loopback aliases, `0.0.0.0`, `::`, LAN/private addresses,
DNS-derived loopback names, other ports, implicit ports, `localhost.`, and expanded
or alternate IPv6 notation. `container` rejects `API`, `api.`, localhost,
`127.0.0.1`, `host.docker.internal`, other service names, other ports, and HTTPS.

`production` requires an exact lower-case `https` scheme, no explicit port (including
`:443`), a hostname containing at least one dot, total hostname length at most 253,
and labels of 1–63 lower-case ASCII letters/digits/hyphens that begin and end with a
letter or digit. It rejects empty labels, trailing dots, IP literals, `localhost`,
single-label hosts, pathname other than `/`, query, fragment, and userinfo. No TLD
allowlist is added without Reliability/Security review. Lower-case ASCII `xn--...`
labels are allowed only when these FQDN label rules pass; Unicode is never converted
to punycode by the resolver.

## 8. Approaches considered

| Approach | Assessment | Decision |
| --- | --- | --- |
| Explicit server-only paired origin/profile | separates browser/server origins and supports deterministic validation | **Selected** |
| Derive from `Host`/`Forwarded`/`X-Forwarded-*` | no proxy trust model; host/header injection and ambiguity | Rejected |
| Request-origin/default/profile fallback | reintroduces precedence and deployment misuse | Rejected |
| Pass a validated branded origin into `apiClient` | keeps one explicit trust boundary and fetch injection | **Selected** |
| Next rewrite, Route Handler, proxy, custom server | routing/deployment coupling; does not solve trust/canonicalization | Rejected |

## 9. Recommended architecture

Create the future focused resolver module:

```text
frontend/src/lib/acceptedStationEvents/apiOrigin.ts
```

It exposes a branded `TrustedAcceptedEventsApiOrigin` and
`resolveTrustedAcceptedEventsApiOrigin()`. At the beginning of **each invocation** it
reads `EDGE_MES_DASHBOARD_API_ORIGIN` and
`EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE` exactly once into an immutable local snapshot.
Every validation, canonicalization, logging category, typed failure, and brand derives
only from that same snapshot. The implementation need not literally use
`Object.freeze`, but it must not reread either environment property during an
invocation.

There is no module-import environment read and no build-time snapshot. `page.tsx`
does not read either variable itself. `apiClient.ts` has no environment or header
knowledge and accepts only the brand, never an unvalidated string endpoint. This is
also the implementation acceptance for `REL-URL-R3`.

`page.tsx` remains the only production call site. After existing query validation
succeeds, it resolves the origin. A typed resolver failure renders the existing
`kind: "error"` branch and performs zero client/fetch calls. On success it passes the
brand to `fetchAcceptedStationEvents(query, trustedApiOrigin, fetchImpl)`.

## 10. Environment/configuration contract

| Contract item | Frozen behavior |
| --- | --- |
| Read timing | request execution inside resolver; one immutable two-variable snapshot per invocation |
| Build | no value required for `next build`; neither value may be inlined or fixed at build time |
| Runtime correction | operator changes process environment, stops Next, then restarts the same artifact; not hot reload |
| Missing/empty/invalid pair | safe configuration `kind: "error"`; no fetch |
| Precedence | only the pair; no fallback or profile inference |
| Public exposure | no `NEXT_PUBLIC_*`, client prop, response echo, or client-bundle value |

Raw values are never repaired. The resolver must not `trim`, lowercase, decode,
replace, remove dots, remove ports, or otherwise repair malformed input into a
trusted origin. Profile matching is raw-syntax policy plus parser verification, not
case-insensitive or DNS-equivalent matching.

## 11. URL validation and composition

### 11.1 Deterministic resolver algorithm

For one snapshot, the algorithm is fixed in this exact order:

1. Check that both profile and origin properties exist.
2. Check that neither value is an empty string.
3. Reject leading or trailing whitespace.
4. Reject any ASCII control character.
5. Reject any non-ASCII character.
6. Reject any percent sign (`%`).
7. Reject any backslash (`\\`).
8. Reject raw syntax not in the profile-specific closed forms in section 7.
9. Only then call platform `new URL()`.
10. Verify parsed components and the same profile policy again.
11. Return one canonical branded origin or a typed configuration failure.

The raw-syntax step rejects uppercase scheme or hostname, trailing-dot hostnames,
explicit production `:443`, noncanonical or zero-padded ports, Unicode/raw IDN,
percent-encoded authority/path or encoded slash, duplicate path slashes, non-root
path, userinfo, query, fragment, empty hostname, port overflow, production IP literals
and production single-label names. It also rejects every form outside the exact local
and container lists. Platform URL parsing is never a policy substitute.

After parsing, verify `protocol`, `hostname`, `port`, `pathname`, `username`,
`password`, `search`, `hash`, and `origin`. The pathname must be exactly `/`; username,
password, search, and hash must be empty; scheme/host/port must still match the same
profile. If parser normalization conflicts with raw policy or changes profile identity,
reject rather than canonicalize through the conflict.

### 11.2 Canonicalization decision matrix

| Input class | Decision | Reason/canonical result |
| --- | --- | --- |
| trailing slash | accept | brand uses `URL.origin` |
| uppercase scheme | reject | strict raw canonical syntax |
| uppercase hostname | reject | strict raw canonical syntax |
| trailing dot | reject | no DNS-equivalent ambiguity |
| explicit production `:443` | reject | one production representation |
| zero-padded port | reject | no parser-normalized ambiguity |
| IPv6 `[::1]` | accept for local only | canonical exact form |
| expanded IPv6 loopback | reject | one textual representation |
| Unicode hostname | reject | no implicit IDN conversion |
| lower-case ASCII punycode FQDN | accept when label rules pass | already canonical ASCII |
| percent encoding | reject | no encoded authority/path ambiguity |
| backslash | reject | no URL separator normalization |
| duplicate slash/path | reject | root pathname only |
| query/fragment/userinfo | reject | base origin only |
| empty/single-label production host | reject | profile mismatch |
| port overflow | reject | malformed configuration |

### 11.3 Branded base and endpoint composition

`TrustedAcceptedEventsApiOrigin` stores only `URL.origin`: no trailing slash,
pathname, query, fragment, or userinfo. Examples:

```text
http://127.0.0.1:8000/ -> http://127.0.0.1:8000
http://[::1]:3100/ -> http://[::1]:3100
https://internal-api.example/ -> https://internal-api.example
```

The client must compose, never concatenate:

```ts
const endpoint = new URL(
  "/api/v2/production/accepted-station-events",
  trustedApiOrigin
);
endpoint.search = buildAcceptedStationEventsQuery(query).toString();
```

`URLSearchParams` remains the query authority. `fetch` uses the absolute endpoint
with `method: "GET"`, `cache: "no-store"`, `credentials: "omit"`, and
`redirect: "error"`; redirect rejection remains generic `kind: "error"`.

## 12. SSRF and trust boundary

The resolver is a server-side outbound-request boundary.

| Risk | Frozen control |
| --- | --- |
| Relative/default target | missing or invalid pair stops before fetch; no fallback |
| Arbitrary scheme or host/port | exact raw profile forms plus parser re-verification |
| Parser/DNS-equivalent ambiguity | strict raw spelling and the section-11 matrix |
| Userinfo/query/fragment/base-path injection | raw and parsed component rejection |
| Header injection / Host poisoning | do not read `headers()`, `Host`, `Forwarded`, `X-Forwarded-Host`, or `X-Forwarded-Proto` |
| Open redirect | `redirect: "error"` |
| Browser credential forwarding | `credentials: "omit"`; no credential/header forwarding |
| DNS rebinding / egress | production rejects IP literals; later deployment gate owns DNS/egress constraints |

There is no trusted-proxy mode. Any future mode requires its own security plan and
must specify proxy identity, direct-access rejection, one-value extraction,
CRLF/control/repeated-value rejection, host/port validation, and protocol validation.

## 13. Request/data flow

```text
AcceptedEventsPage
  -> validateAcceptedStationEventsQuery
  -> resolveTrustedAcceptedEventsApiOrigin (one server-env snapshot)
  -> typed configuration error / no outbound request
     OR TrustedAcceptedEventsApiOrigin
  -> fetchAcceptedStationEvents(query, brand, fetchImpl)
  -> buildAcceptedStationEventsQuery
  -> new URL(fixed endpoint, trusted root) + URLSearchParams
  -> fetch(absolute GET, no-store, omit credentials, redirect error)
  -> existing response classification -> strict parser -> view model -> UI state
```

Invalid query remains `invalid-query` before resolution. Valid query with missing or
invalid configuration becomes `error`, hides ready production data, and sends no
accepted-events request. Valid origin preserves parser/classification/view-model
behavior.

## 14. Error and logging behavior

Configuration failure is a distinct cause within existing `kind: "error"`, never
`empty`, `invalid-query`, or `unavailable`. The browser receives only the fixed safe
message `Accepted events service is not configured.`

Logging is bounded and non-throwing without a new dependency or logger file:

- failure uses a closed `OriginConfigurationErrorCode` enum;
- module scope holds only `Set<OriginConfigurationErrorCode>`; each safe code logs at
  most once per process, and the finite enum bounds set size;
- restart naturally resets deduplication;
- each log contains `DASHBOARD_API_ORIGIN_CONFIGURATION_ERROR`, safe category,
  variable names, and profile category only when safely known;
- it never includes raw origin, URL, hostname, query, headers, credentials, or user
  input;
- `console.error`/logging is wrapped in non-throwing containment. Logging failure
  must not alter the typed resolver result or enter a Next error boundary.

Tests may isolate dedupe by module reset/isolation. No production-only reset export is
allowed. This is the implementation acceptance for `REL-URL-R4`.

## 15. Deployment matrix

| Scenario | Runtime configuration | Expected behavior |
| --- | --- | --- |
| Local frontend only | unset | visible configuration `error`; zero outbound request; no fallback |
| Local frontend + local API | `local` / `http://127.0.0.1:8000` | exact absolute loopback request only |
| Local recovery capture | `local` / `http://127.0.0.1:8000` | only in separately authorized runtime recovery gate |
| Standalone Next | `production` / valid production FQDN at process start | build artifact needs no env; a restart can read corrected env |
| Future Docker frontend | `container` / `http://api:8000` | only in separately authorized frontend-container deployment |
| Reverse proxy | `production` / internal API FQDN | browser/forwarded headers stay irrelevant |

Generic Next process readiness can succeed while an accepted-events valid query fails
closed because this configuration is absent. This six-file implementation adds no
health endpoint, startup validation, Compose/Next configuration, or deployment docs.
A future deployment/config gate owns accepted-events-specific readiness, alerting, and
operator diagnostics; generic server ready must not be documented as accepted-events
service ready. This is `REL-URL-R6`, a non-blocking future recommendation.

## 16. Mock-capability interaction

The same-origin no-DB mock-capability plan remains **HOLD**. This report designs no
mock, Route Handler, rewrite, custom server, fixture, or intercept. A future local
`http://127.0.0.1:3100` form can only be used after its own authorization and cannot
be a missing-config fallback. Browser/manual smoke cannot replace resolver/security
tests or restart-recovery evidence.

## 17. Exact future implementation file allowlist

The future URL-resolution implementation gate may change exactly these six files:

| Action | Exact file | Purpose |
| --- | --- | --- |
| Create | `frontend/src/lib/acceptedStationEvents/apiOrigin.ts` | resolver, brand, typed configuration failure, finite safe logging |
| Modify | `frontend/src/lib/acceptedStationEvents/apiClient.ts` | branded origin and absolute fixed endpoint composition |
| Modify | `frontend/src/app/accepted-events/page.tsx` | request-time resolution and safe configuration error rendering |
| Create | `frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts` | resolver/profile/canonicalization/redaction/isolation tests |
| Modify | `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts` | absolute URL/composition/fetch-option regression tests |
| Modify | `frontend/src/app/accepted-events/__tests__/page.test.tsx` | resolver failure/no-fetch and ready-flow integration tests |

The allowlist is unchanged. It excludes logger/config utilities, `package.json`, lock
files, `next.config.ts`, `tsconfig.json`, `.env.example`, `docker-compose.yml`,
`README.md`, `schema.ts`, `query.ts`, `viewModel.ts`, `loading.tsx`, and `error.tsx`.
New dependency: **none**. A claimed need to expand it is `HOLD`, not permission to
expand it.

## 18. Exact future test file allowlist

Only the three test paths in section 17 may change. They must cover:

| Test area | Required assertions |
| --- | --- |
| Resolver positives | every exact local/container form, compliant production FQDN/punycode, optional root slash, `URL.origin` brand |
| Resolver negatives | every section-11 matrix reject; missing/empty/unknown pair; wrong profile pair; controls/whitespace/non-ASCII/percent/backslash; parser conflict; no raw-value output |
| Snapshot timing | one invocation reads each env property once; no module-import/build snapshot; `page.tsx`/client never read env |
| API client | exact absolute endpoint; only five query keys; cursor encoding; GET/no-store/omit/redirect-error; injected fetch; no relative URL |
| Failure isolation | resolver failure yields no fetch, visible error, and no stale production surface |
| Regression | strict malformed-2xx error and existing 4xx/503/other classifications |
| Logging | finite once-per-code dedupe, redaction, non-throwing containment through module isolation/reset |

Environment-mutating tests must save each property’s prior presence and value. In
`afterEach`, restore the old value when it existed; otherwise `delete` the property.
They must never write string `"undefined"`, must run serially (for example a Vitest
sequential suite), set a complete origin/profile pair per case, and never use the
developer machine environment as a default. `afterEach` restoration must run after
test failure. Module cache isolation cannot freeze a test’s environment snapshot.
Page mocks and `process.env` restoration remain independent. This is the test
acceptance for `REL-URL-R5`.

## 19. Future test and runtime validation strategy

The future implementation gate requires separate authorization for commands. Its
evidence order is resolver tests, client tests, page tests, full frontend tests,
typecheck, build/artifact audit, then separately authorized runtime probes. No test,
build, server, capture endpoint, or recovery probe is run by this repair.

### Restart recovery acceptance

This is an independent future runtime gate, not hot reload. It must prove:

```text
missing/invalid config
-> valid accepted-events page request fails closed
-> visible kind:"error"
-> zero accepted-events outbound request
-> stop Next process
-> correct runtime environment
-> restart the same build artifact
-> subsequent valid request resolves corrected origin
-> exactly one accepted-events request
-> no rebuild between the two runs
```

`next build` executes once only and requires neither origin value. Both phases use the
same `frontend/.next/standalone` artifact. The corrected run is a fresh process, not
a changed environment within the first process; module cache/import state cannot
retain the old pair, and the first valid request after restart reads the new snapshot.

Future topology is Next standalone on `127.0.0.1:3100` and an authorized loopback
capture/fixture endpoint on `127.0.0.1:8000`.

**Phase A — invalid or missing configuration.** Do not start the capture endpoint, or
prove its request count is zero. Start the same artifact with an absent pair or an
explicit invalid pair; send one valid accepted-events page query; observe safe
configuration `error`, zero accepted-events outbound request, and no relative,
localhost, container, or mock fallback. Stop Next and prove the port is released.

**Phase B — corrected configuration after restart.** Start the separately authorized
loopback-only synthetic capture/fixture endpoint. Without rebuild, restart that same
standalone artifact with:

```text
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=local
EDGE_MES_DASHBOARD_API_ORIGIN=http://127.0.0.1:8000
```

Send the same valid page query. The capture endpoint observes exactly one
`GET /api/v2/production/accepted-station-events`; the query contains only `line_id`,
`start_time`, `end_time`, `limit`, and `cursor` only when explicitly requested.
Method, path, query, and fetch options remain contractual; a synthetic response still
passes the strict parser; record final page state. Stop every recorded process, free
both ports, clean only recorded generated artifacts, and restore Git status.

This future probe passes only with same artifact, no rebuild, Phase-A zero request,
corrected-restart exactly one request to corrected absolute origin, no stale
env/module snapshot, no fallback, no extra request, no client-bundle origin leak, and
complete cleanup. This addresses `REL-URL-R2` in planning authority only.

## 20. Package/config/dependency impact

| Surface | Future URL implementation decision |
| --- | --- |
| `frontend/package.json` / lockfile | unchanged |
| new dependency | none |
| `frontend/next.config.ts` / `tsconfig.json` | unchanged |
| `.env.example`, `docker-compose.yml`, `README.md` | unchanged; a deployment/config-doc gate decides later |
| package scripts | unchanged |

The resolver must prove request-time behavior rather than assume standalone build-time
substitution behavior. This is not authorization to add package/config/deployment
scope.

## 21. Generated artifacts and cleanup

This repair creates no generated artifacts. Future authorized validation must preflight
and remove only its own preflight-absent `frontend/.next/`, `frontend/next-env.d.ts`,
and `frontend/tsconfig.tsbuildinfo` when generated. Never use `git clean`, reset,
restore, broad deletion, or alter `frontend/node_modules/`/external artifacts.
Unexpected tracked/config/package/generated drift is `HOLD`.

## 22. PASS conditions

This planning authority is PASS-capable only when all of these remain true:

- exact paired runtime variables, single immutable invocation snapshot, strict raw
  parser order, profile forms, parser re-verification, and `URL.origin` brand;
- no browser/header/relative/default/profile fallback or client leak;
- valid query plus invalid configuration is safe `error` with zero request;
- finite, redacted, non-throwing configuration logging and serial exact env-test
  isolation;
- same-artifact restart recovery acceptance with Phase-A zero and Phase-B exactly-one
  request is frozen for a future runtime gate;
- the six-file allowlist is unchanged with no package/config/deployment expansion;
- parser/contract/fact authority/stale-data behavior is preserved;
- Reliability blockers addressed by planning repair; closure remains pending
  Reliability re-review.

## 23. HOLD conditions

Future gates must stop with **HOLD** for any raw input repair/implicit normalization,
case-insensitive or DNS-equivalent matching, default-port acceptance outside the exact
forms, Unicode conversion, expanded IPv6 acceptance, reread/mixed environment pair,
module-import/build snapshot, hot-reload claim, missing Phase-A/Phase-B recovery
evidence, unbounded/throwing logging, env-test leakage, fallback, client leak,
unexpected request, contract/parser/authority/query/cursor/cache/stale-data change,
or any need for a non-six-file/package/config/deployment/mock expansion. Unauthorized
stage/commit/push/deploy/runtime actions are also HOLD.

## 24. Required reviews

After an explicitly authorized planning-authority commit, the immediate next gate is
an independent Reliability re-review of this repaired authority. It alone may accept
or retain `REL-URL-R1`/`REL-URL-R2`; this report does not alter the Reliability review
or claim its gate passed. Later Data Quality, Verification, Security/privacy,
implementation, tests, build, and runtime work each require new authorization.

Reliability must recheck raw canonicalization/profile matching, one-snapshot timing,
finite failure logging, test isolation, and same-artifact restart recovery acceptance.
Data Quality must preserve endpoint/parser/fact authority; Verification must audit the
exact allowlist, static matrix, and future evidence topology.

## 25. Next gate sequence

```text
PM exact-path commit authorization (not granted here)
-> planning authority commit
-> independent Reliability re-review of repaired authority
-> any later reviews/implementation only after explicit PM authorization
```

No implementation may start from this report. The mock-capability plan remains HOLD
until later implementation and runtime validation, and this report does not resume it.

## 26. Risks and recommendations

1. **REL-URL-R6 retained:** deployment ownership still lacks a frontend service and
   accepted-events-specific readiness/alerting decision. It is a later deployment gate,
   not a six-file source blocker.
2. **Egress/DNS:** application validation cannot prove DNS ownership or egress safety;
   a future production deployment review must cover them.
3. **REL-URL-R7 — CLOSED BY PLAN:** no retry, timeout, circuit breaker, fallback, or
   secondary origin enters this bounded URL-resolution scope.
4. **Mock capability:** absolute resolution is a prerequisite, not mock design or
   proof. Keep its separate plan HOLD until its own authority is re-reviewed.

### Reliability HOLD repair matrix

| Finding | Repair status in plan | Remaining authority |
| --- | --- | --- |
| REL-URL-R1 | addressed | pending Reliability re-review |
| REL-URL-R2 | addressed | pending Reliability re-review |
| REL-URL-R3 | incorporated as implementation acceptance | pending Reliability re-review |
| REL-URL-R4 | incorporated as implementation acceptance | pending Reliability re-review |
| REL-URL-R5 | incorporated as test acceptance | pending Reliability re-review |
| REL-URL-R6 | retained as deployment follow-up | pending Reliability re-review |
| REL-URL-R7 | closed by existing bounded scope | pending Reliability acknowledgement |

## 27. Thread output / context assessment

- 本次输出长度：长（durable planning authority；window report 应保持简洁）。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：repair 已完成；commit gate、Reliability re-review、implementation 与 runtime
  validation 均需独立 PM authorization，不能继承本次 docs-only 权限。
