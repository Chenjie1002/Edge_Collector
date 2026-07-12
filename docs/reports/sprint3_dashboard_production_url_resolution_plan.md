# Sprint 3 Dashboard production URL-resolution VER-URL-V1-B1 planning authority repair report

报告名称：Sprint 3 Dashboard production URL-resolution VER-URL-V1-B1 planning authority repair report

任务名称：Resolve the executable reachability of `ORIGIN_MALFORMED` and repair the closed resolver error contract

执行 Thread：Architecture / Integration

风险等级：Level 1 planning-only；future implementation remains Level 2 because it changes the production Server Component outbound fetch target.

结论：**PASS WITH RECOMMENDATIONS**

本报告冻结 server-only、request-time、fail-closed 的 absolute API URL-resolution
boundary，并以本次 Architecture planning repair 补足 `VER-URL-V1` / `VER-URL-V1-B1`
所需的可执行 resolver result、brand、environment-read test contract 与
`ORIGIN_MALFORMED` input-native reachability。它不授权 implementation、
tests、runtime probe、deployment、configuration write、status sync、stage、commit 或
push。

Architecture planning repair has addressed the documented
Reliability HOLD findings in the planning authority.

Architecture planning repair addresses `VER-URL-V1-B1` in authority only.

Verification remains **HOLD** until independent cross-functional re-review accepts
the repaired authority.

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

### VER-URL-V1-B1 live repair baseline and external artifacts

This B1 authority repair was made only after read-only recovery confirmed:

```text
HEAD == origin/main == bba8648e4862cfa31bc0bd02d620750288305056
latest commit: bba8648 Re-review Dashboard resolver contract data quality
ahead/behind: 0 0
cached diff: empty
tracked diff: .gitignore only
```

The unchanged external artifacts are `M .gitignore`, the listed historical PM handoff
and reporting files, and `frontend/node_modules/`. They are not plan inputs to edit,
cleanup, stage, commit, or otherwise mutate. The sole writable path for this B1 repair
is this report.

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

Its public contract is frozen exactly as follows; future implementation must not
rename, widen, replace, or redesign it:

```ts
export type AcceptedEventsApiOriginEnvironment = Readonly<{
  EDGE_MES_DASHBOARD_API_ORIGIN?: string;
  EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE?: string;
}>;

declare const trustedAcceptedEventsApiOriginBrand: unique symbol;

export type TrustedAcceptedEventsApiOrigin = string & {
  readonly [trustedAcceptedEventsApiOriginBrand]:
    "TrustedAcceptedEventsApiOrigin";
};

export type OriginConfigurationErrorCode =
  | "ORIGIN_MISSING"
  | "PROFILE_MISSING"
  | "ORIGIN_EMPTY"
  | "PROFILE_EMPTY"
  | "PROFILE_UNSUPPORTED"
  | "ORIGIN_NON_CANONICAL"
  | "ORIGIN_PROFILE_MISMATCH"
  | "ORIGIN_MALFORMED";

export type AcceptedEventsApiOriginResolution =
  | { readonly ok: true; readonly origin: TrustedAcceptedEventsApiOrigin }
  | {
      readonly ok: false;
      readonly code: OriginConfigurationErrorCode;
      readonly message: "Accepted events service is not configured.";
    };

export function resolveTrustedAcceptedEventsApiOrigin(
  environment?: AcceptedEventsApiOriginEnvironment
): AcceptedEventsApiOriginResolution;
```

`OriginConfigurationErrorCode` is a closed union of exactly **eight** codes. No
catch-all code, parser-error payload, raw value, profile, URL, or diagnostic key may
be added to the public failure result. `ORIGIN_MALFORMED` remains in that eight-code
union because section 11.1 now freezes an input-native, native-parser reachability
vector; it is not a monkey-patch-only contingency.

`environment === undefined` means that the resolver itself uses `process.env`.
The no-argument call is the production call: `page.tsx` calls
`resolveTrustedAcceptedEventsApiOrigin()`. Supplying a typed environment is a formal,
production-compatible dependency seam for focused resolver tests, not a test-only
export. No caller may use a global mutable override, `setEnvironmentForTests()`, or a
production reset export.

At the beginning of **each invocation** the resolver chooses the supplied environment
or `process.env`, reads each named property exactly once, and creates an immutable
local snapshot. Every validation, classification, logging category, typed result, and
brand derives only from that snapshot. The implementation need not literally use
`Object.freeze`, but it must not reread either source property during an invocation.

There is no module-import environment read and no build-time snapshot. `page.tsx`
does not read either variable itself. `apiClient.ts` has no environment or header
knowledge and accepts only the brand, never an unvalidated string endpoint. This is
also the implementation acceptance for `REL-URL-R3`.

`page.tsx` remains the only production call site. After existing query validation
succeeds, it resolves the origin with no argument. It must use the discriminant:

```ts
const resolution = resolveTrustedAcceptedEventsApiOrigin();

if (!resolution.ok) {
  return { kind: "error", message: resolution.message };
}
```

The actual page return structure follows its existing view contract. Failure performs
zero client calls, zero fetch calls, and exposes no ready data. On success it passes
only `resolution.origin` to `fetchAcceptedStationEvents(query, resolution.origin,
fetchImpl)`. The page must not inspect `code`, read env, create/cast a brand, select an
endpoint, or catch a configuration exception as ordinary control flow.

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

`AcceptedEventsApiOriginEnvironment` contains only the two readonly optional transport
properties in section 9. It must not acquire query values, headers, `Host`,
`Forwarded`, browser origin, fetch, logger, fallback URL, business `profile_id`, or
response data. The production-default sequence is conceptually:

```ts
const source = process.env;
const rawOrigin = source.EDGE_MES_DASHBOARD_API_ORIGIN;
const rawProfile = source.EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE;
const snapshot = { rawOrigin, rawProfile };
```

Each property access is exactly once, and after `snapshot` is made the resolver must
not access `source` again. It must not store source or snapshot in module scope, read
it in helpers/logging/page/client, or read it at import/build time. The optional
argument permits tests to use a local typed getter object; it neither modifies nor
proxies global `process.env`.

## 11. URL validation and composition

### 11.1 Deterministic resolver algorithm

For one snapshot, classification returns the first matching failure and is fixed in
this exact precedence: `ORIGIN_MISSING`, `PROFILE_MISSING`, `ORIGIN_EMPTY`,
`PROFILE_EMPTY`, `PROFILE_UNSUPPORTED`, raw safety/canonicality validation, profile
matching, `new URL()` parsing, parsed-component re-verification. The deterministic
mapping is:

| Condition | Result code |
| --- | --- |
| origin property absent | `ORIGIN_MISSING` |
| profile property absent | `PROFILE_MISSING` |
| origin is exactly `""` | `ORIGIN_EMPTY` |
| profile is exactly `""` | `PROFILE_EMPTY` |
| profile is not exactly `local`, `container`, or `production` | `PROFILE_UNSUPPORTED` |
| whitespace/control/non-ASCII/`%`/backslash, or no allowed canonical raw representation | `ORIGIN_NON_CANONICAL` |
| origin has another known profile's exact canonical syntax but not the selected profile | `ORIGIN_PROFILE_MISMATCH` |
| `new URL()` throws after raw checks | `ORIGIN_MALFORMED` |
| parsed protocol/host/port/path/userinfo/query/fragment disagrees with selected profile or raw identity | `ORIGIN_PROFILE_MISMATCH` |

First test the selected profile's closed raw syntax. If that fails but another known
profile's exact syntax succeeds, return `ORIGIN_PROFILE_MISMATCH`; if no known syntax
succeeds, return `ORIGIN_NON_CANONICAL`. Production FQDN grammar is a known production
syntax. DNS, parser lowercase/default-port normalization, and Unicode conversion never
establish a match.

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
return `ORIGIN_PROFILE_MISMATCH` rather than canonicalize through the conflict. Every
expected configuration invalidity is non-throwing and returns the failure union; only a
genuine programming defect may naturally throw.

### 11.1A `ORIGIN_MALFORMED` executable reachability freeze (`VER-URL-V1-B1`)

Architecture independently selects **Path A: an executable input-native vector
exists**. The exact public-resolver input is:

```ts
{
  EDGE_MES_DASHBOARD_API_ORIGIN: "https://xn--a.example",
  EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production",
}
```

It passes the selected `production` raw grammar before parsing: `https` is exact
lower-case; `xn--a.example` is lower-case ASCII; it has a dot; both labels are 1--63
characters and begin/end with an ASCII letter or digit; the hostname is below 253
characters; and it has neither an explicit port nor a non-root path, userinfo, query,
fragment, percent sign, backslash, control, or non-ASCII character. It therefore is
neither `ORIGIN_NON_CANONICAL` nor `ORIGIN_PROFILE_MISMATCH` at the raw stage.

The `xn--a` label is syntactically within the closed raw FQDN policy but is not a valid
IDNA A-label for the target WHATWG parser. The local deterministic probe on the target
implementation runtime, `node v22.23.0`, produced `TypeError` from both
`new URL("https://xn--a.example")` and the optional-root-slash variant. The resolver
must catch that native parser exception and return exactly:

```ts
{
  ok: false,
  code: "ORIGIN_MALFORMED",
  message: "Accepted events service is not configured.",
}
```

The future public resolver test calls the resolver with the typed environment object
above and asserts that exact own-key result. It must not monkey-patch global `URL`,
inject a parser, replace a production boundary, add a constructor/reset seam, or use a
synthetic thrown exception as acceptance evidence.

Runtime assumption and drift rule: the currently frozen executable evidence is Node
`v22.23.0` WHATWG `URL`. The implementation/test gate must record its actual Node
version and must prove this same input still throws natively before accepting
`ORIGIN_MALFORMED`. If a supported target runtime instead accepts it, the gate is
**HOLD**: it must not simulate rejection, silently reclassify the vector, remove the
code, or widen the raw grammar. Architecture must first issue a new authority repair
that preserves fail-closed canonicality and the public exact-result contract.

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

### 11.2A Closed public-resolver input-native negative matrix

Every closed code has one direct public-resolver vector. These are typed local
environment-object inputs to `resolveTrustedAcceptedEventsApiOrigin(environment)`;
they do not mutate `process.env`, use a global proxy, or inject a production seam.
The table fixes the expected first result under section-11 precedence.

| Code | Exact environment input | Why this code wins |
| --- | --- | --- |
| `ORIGIN_MISSING` | `{ EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" }` | origin property is absent; first precedence check |
| `PROFILE_MISSING` | `{ EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:8000" }` | origin exists; profile property is absent |
| `ORIGIN_EMPTY` | `{ EDGE_MES_DASHBOARD_API_ORIGIN: "", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" }` | both properties exist; origin is exactly empty |
| `PROFILE_EMPTY` | `{ EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:8000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "" }` | origin is valid and profile is exactly empty |
| `PROFILE_UNSUPPORTED` | `{ EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:8000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "staging" }` | profile is non-empty but outside the closed set |
| `ORIGIN_NON_CANONICAL` | `{ EDGE_MES_DASHBOARD_API_ORIGIN: "http://127.0.0.1:08000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" }` | zero-padded port is no exact known-profile form and raw policy rejects it before parsing |
| `ORIGIN_PROFILE_MISMATCH` | `{ EDGE_MES_DASHBOARD_API_ORIGIN: "http://api:8000", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "local" }` | raw input is the exact `container` form, not the selected `local` form |
| `ORIGIN_MALFORMED` | `{ EDGE_MES_DASHBOARD_API_ORIGIN: "https://xn--a.example", EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production" }` | selected production raw grammar passes; target native `new URL()` throws as section 11.1A freezes |

For every row, the failure result owns exactly `ok`, `code`, and `message`, and the
message is the fixed safe literal. The test must assert the direct own-key set, not
only the code. A future test may include additional reject rows from section 11.2, but
may not replace any table row with a global parser mock or an implementation-only
helper.

### 11.3 Branded base and endpoint composition

`TrustedAcceptedEventsApiOrigin` stores only `URL.origin`: no trailing slash,
pathname, query, fragment, or userinfo. Examples:

```text
http://127.0.0.1:8000/ -> http://127.0.0.1:8000
http://[::1]:3100/ -> http://[::1]:3100
https://internal-api.example/ -> https://internal-api.example
```

The branded string is exactly `parsedUrl.origin`. The brand can be created only on the
successful path of `resolveTrustedAcceptedEventsApiOrigin`; its constructor/branding
helper is not exported. Production call sites must not use `as
TrustedAcceptedEventsApiOrigin`. `apiClient.ts` accepts the brand, never a raw string
or string union; its tests obtain a valid brand through this resolver and typed test
environment. A compile-time negative test may use `// @ts-expect-error ordinary string
must not satisfy the brand`, but production code gains no unsafe test constructor.

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
  -> resolveTrustedAcceptedEventsApiOrigin() (one server-env snapshot)
  -> `{ ok: false, code, message }` / no outbound request
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
behavior. The success result owns exactly `ok` and `origin`; the failure result owns
exactly `ok`, `code`, and `message`. Neither raw input, profile, hostname, URL,
diagnostic metadata, query, headers, parser error, stack, cause, credentials, nor
logging state may be added to either resolver result.

The transport profile and safe configuration code never enter the API DTO, response,
or view model. `profile_id` remains response-owned accepted-fact data only; the
environment seam neither changes production-fact authority nor schema/query/view-model
semantics.

## 14. Error and logging behavior

Configuration failure is a distinct cause within existing `kind: "error"`, never
`empty`, `invalid-query`, or `unavailable`. The browser receives only the fixed safe
message `Accepted events service is not configured.`

Logging is bounded and non-throwing without a new dependency or logger file:

- failure uses exactly the closed `OriginConfigurationErrorCode` union in section 9;
- module scope holds only `Set<OriginConfigurationErrorCode>`; each safe code logs at
  most once per process, and the eight-code closed union bounds set size at **8**;
- restart naturally resets deduplication;
- each log contains `DASHBOARD_API_ORIGIN_CONFIGURATION_ERROR`, safe category,
  variable names, and profile category only when safely known;
- it never includes raw origin, URL, hostname, query, headers, credentials, or user
  input;
- `console.error`/logging is wrapped in non-throwing containment. Logging failure
  must not alter the typed resolver result or enter a Next error boundary; logging
  occurs before failure return but does not appear in that result.

Logging derives only from the captured snapshot and determined safe code; it must not
reread the environment. Safe variable-name mapping is fixed constants, never raw
input. Tests isolate dedupe using `vi.resetModules()` and dynamic import, not an
exported dedupe set or production reset function. This is the implementation acceptance
for `REL-URL-R4`.

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
| Resolver positives | every exact local/container form, compliant production FQDN/punycode, optional root slash, `URL.origin` brand; direct exact own keys `ok`, `origin` |
| Resolver negatives | every section-11 matrix reject; every row in section 11.2A (all eight safe codes); direct exact own keys `ok`, `code`, `message`; exact fixed safe message and no raw-value output; `ORIGIN_MALFORMED` uses only the native `https://xn--a.example` vector and records the actual Node version |
| Snapshot timing | success and failure getter-object tests prove each input property is read once; no module-import/build snapshot; `page.tsx`/client never read env |
| API client | exact absolute endpoint; only five query keys; cursor encoding; GET/no-store/omit/redirect-error; injected fetch; no relative URL |
| Failure isolation | resolver failure yields no fetch, visible error, and no stale production surface |
| Regression | strict malformed-2xx error and existing 4xx/503/other classifications |
| Logging | finite once-per-code dedupe, redaction, non-throwing containment through module isolation/reset |

The required exact-read seam is a typed local getter object, not a global proxy. A
focused success test and focused failure test each use the formal `environment`
argument, increment `originReads` and `profileReads` from its two getters, invoke the
resolver, and assert both counts are exactly `1`. The failure case proves there is no
extra read after classification failure. It must not use `Proxy(process.env)`, replace
global `process.env`, call `Object.defineProperty(process.env, ...)`, monkey-patch
`ProcessEnv`, install a global getter hook, or add a production counter/reset export.

A separate request-time re-read test proves invocation A observes environment A and
invocation B observes environment B. It does not replace the getter-based
single-invocation proof. Direct-argument parameterized tests require no mutation of
`process.env`. Only production-default or re-read tests may mutate it; those tests save
each property's prior presence and value and, in `afterEach`, restore the old value or
`delete` it. They never write string `"undefined"`, run serially, set a complete pair,
and never use developer-machine env as a default. Restoration must run after test
failure. Page mocks and `process.env` restoration remain independent. This is the test
acceptance for `REL-URL-R5`.

Brand-boundary tests prove resolver success creates the brand, the API client accepts
that resolver brand, an ordinary string fails compile time, the page contains no cast,
and its underlying value is canonical `URL.origin`. Logging tests prove same-code
dedupe, distinct-code logging, redaction of both raw values, containment when
`console.error` throws, and reset only through `vi.resetModules()` plus dynamic import.

## 19. Future test and runtime validation strategy

The future implementation gate requires separate authorization for commands. Its
evidence order is resolver tests, client tests, page tests, full frontend tests,
typecheck, build/artifact audit, then separately authorized runtime probes. No test,
build, server, capture endpoint, or recovery probe is run by this repair.

### Bundle carry-forward

`VER-URL-V2` remains **CARRY FORWARD**. A future build-evidence gate must inspect
`.next/static/**` separately from `.next/server/**`, prove raw configured origin values
do not enter client artifacts, and not treat server occurrence of variable names as a
leak. A whole-`.next` grep alone is not browser-safety evidence. This repair performs
neither build nor bundle inspection.

### Runtime carry-forward

`VER-URL-V3` remains **CARRY FORWARD** and is an independent runtime-planning gate,
not hot reload or an authorization to run a server. It must later choose and authorize
the exact capture/fixture method, temporary/log/request-counter artifact allowlist,
zero/exactly-one evidence, same-artifact hash, `/usr/sbin/lsof` preflight, PID/port
cleanup, and Data Quality evidence classification. This repair neither chooses that
mechanism nor adds a helper, fixture, package/config, or runtime procedure.

The retained outcome requirement is request-time behavior: a fresh invocation must
observe its current configured pair, and a corrected process restart against the same
artifact must not be claimed without later evidence. That future evidence must
distinguish synthetic transport/strict-parser fixture evidence from real
production-fact evidence.

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
  parser order, eight-code precedence, profile forms, parser re-verification, exact
  discriminated result own keys, and `URL.origin` brand;
- every one of the eight closed public codes has the section-11.2A input-native vector;
  specifically, `https://xn--a.example` passes raw production grammar and throws from
  the actual target Node `new URL()` without a monkey-patch or injected parser;
- no browser/header/relative/default/profile fallback or client leak;
- valid query plus invalid configuration is safe `error` with zero request;
- formal typed environment seam, success/failure getter exact-read evidence, separate
  request-time re-read evidence, and no global `process.env` proxy/test-only export;
- finite, redacted, non-throwing configuration logging and serial exact env-test
  isolation;
- `VER-URL-V2` and `VER-URL-V3` remain carry-forward future gates;
- the six-file allowlist is unchanged with no package/config/deployment expansion;
- parser/contract/fact authority/stale-data behavior is preserved;
- `VER-URL-V1-B1` is addressed in authority only; cross-functional closure remains
  pending.

## 23. HOLD conditions

Future gates must stop with **HOLD** for any raw input repair/implicit normalization,
case-insensitive or DNS-equivalent matching, default-port acceptance outside the exact
forms, Unicode conversion, expanded IPv6 acceptance, reread/mixed environment pair,
module-import/build snapshot, raw-string/cast brand creation, non-discriminated or
throwing configuration handling, extra result keys, a missing safe code/mapping,
global env proxy, production test-only reset/export, unbounded/throwing logging,
env-test leakage, fallback, client leak, unexpected request, contract/parser/
authority/query/cursor/cache/stale-data change, or any need for a non-six-file/
package/config/deployment/mock expansion. Unauthorized stage/commit/push/deploy/runtime
actions are also HOLD. It is additionally **HOLD** if the target Node runtime does not
natively throw for `https://xn--a.example`, if `ORIGIN_MALFORMED` lacks an
input-native public vector, or if a test attempts to manufacture that failure by a
global `URL` monkey-patch, injected parser, production-only constructor/reset, or
production-boundary override.

## 24. Required reviews

After an explicitly authorized planning-authority commit, the required sequence is an
independent focused Reliability re-review, focused Data Quality re-review, then
Verification re-review. They decide whether the authority repair closes `VER-URL-V1-B1`;
this report does not alter any review authority or claim a gate passed. Focused
Security/privacy planning review follows before any PM implementation decision.
Implementation, tests, build, and runtime work each require new authorization.

Reliability must recheck raw canonicalization/profile matching, one-snapshot timing,
the non-throwing union, finite failure logging, and test isolation. Data Quality must
confirm error code/failure union do not enter DTO or view state and transport profile
stays isolated from `profile_id`. Verification must audit the exact allowlist, result
contract, getter seam, and carry-forward evidence topology.

## 25. Next gate sequence

```text
PM exact-path commit authorization (not granted here)
-> planning authority commit
-> focused Reliability re-review
-> focused Data Quality re-review
-> Verification re-review
-> focused Security/privacy planning review
-> PM implementation authorization decision
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

### Reliability/Verification repair matrix

| Finding | Repair status in plan | Remaining authority |
| --- | --- | --- |
| VER-URL-V1 | prior resolver/test seam repair retained | superseded for Verification closure by `VER-URL-V1-B1` |
| VER-URL-V1-B1 | `ORIGIN_MALFORMED` is reachable through the exact native-parser vector; eight-code union, precedence, public vectors, logging bound and runtime-drift HOLD are frozen | pending independent Reliability/Data Quality/Verification re-review |
| VER-URL-V2 | retained | future build evidence gate |
| VER-URL-V3 | retained | dedicated runtime planning gate |
| REL-URL-R3 | preserved and made directly testable | pending implementation evidence |
| REL-URL-R4 | preserved with exact safe codes | pending implementation evidence |
| REL-URL-R5 | preserved | pending test evidence |
| DQ-URL-D1 | preserved | pending page/client test evidence |
| DQ-URL-D2 | retained | pending runtime evidence |
| DQ-URL-D3 | retained | pending full regression |

### Repair conclusion

The planning conclusion remains **PASS WITH RECOMMENDATIONS**. Architecture has
repaired the executable `ORIGIN_MALFORMED` reachability and closed resolver error
contract required by `VER-URL-V1-B1`.
Verification remains **HOLD** until independent cross-functional re-review accepts the
repaired authority. This is not implementation authorization.

### Historical Reliability repair matrix

| Finding | Repair status in plan | Remaining authority |
| --- | --- | --- |
| REL-URL-R1 | historical planning repair retained | independent Reliability re-review |
| REL-URL-R2 | historical planning repair retained | dedicated future runtime evidence |
| REL-URL-R3 | incorporated and directly testable | pending implementation evidence |
| REL-URL-R4 | incorporated with exact safe codes | pending implementation evidence |
| REL-URL-R5 | incorporated as test acceptance | pending test evidence |
| REL-URL-R6 | retained as deployment follow-up | future deployment gate |
| REL-URL-R7 | closed by existing bounded scope | no new authority in this repair |

## 27. Thread output / context assessment

- 本次输出长度：长（durable planning authority；window report 应保持简洁）。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：repair 已完成；commit gate、Reliability re-review、implementation 与 runtime
  validation 均需独立 PM authorization，不能继承本次 docs-only 权限。
