# Sprint 3 Dashboard production URL-resolution planning gate report

报告名称：Sprint 3 Dashboard production URL-resolution planning gate report

任务名称：Design a secure and deployment-safe absolute API URL resolution boundary for the Dashboard accepted-events Server Component

执行 Thread：Architecture / Integration

风险等级：Level 1 planning-only；future implementation is expected to be Level 2 because it changes the production Server Component outbound fetch target.

结论：**PASS WITH RECOMMENDATIONS**

本报告冻结一个 server-only、request-time、fail-closed 的 absolute API URL
resolution boundary。它不授权 implementation、tests、runtime probe、deployment、
configuration write、status sync、stage、commit 或 push。

## 1. Baseline and read-only recovery

本 gate 的第一动作是附件规定的 read-only recovery；没有在恢复前写入、启动
server、运行 probe/tests/typecheck/build、安装 dependency，或连接 API/DB/Docker。

| Item | Live evidence |
| --- | --- |
| Branch | `main...origin/main` |
| HEAD | `4715456dec23edacebe0cb3d59a23e3cb587a9fe` |
| origin/main | `4715456dec23edacebe0cb3d59a23e3cb587a9fe` |
| Latest commit | `4715456 Record Dashboard mock capability planning HOLD` |
| Cached diff | empty |
| Tracked diff before this report | `.gitignore` only |
| Target report before this gate | absent |

已确认的 external dirty artifacts 与任务预期一致：`.gitignore`、
`docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`、一份 Keynote HTML、
一份 DB-backed review、四份旧 PM handoff，以及 `frontend/node_modules/`。它们均不在
本 gate allowlist，未被读取为写入目标、清理、stage 或修改。

## 2. Context reviewed

已按任务指定顺序只读审计：

1. `docs/thread_handoff/pm_operating_rules.md`
2. `docs/thread_handoff/chatgpt_pm_handoff_260711-1802.md`
3. `docs/current_status.md`
4. `docs/contracts/dashboard_api_contract.md`
5. Dashboard vertical-validation、stale-data、typecheck/build、browser smoke 与
   same-origin no-DB mock-capability reports。
6. 任务指定的 `frontend/` package/config/page/loading/error/tests、accepted-events
   client/query/schema/view-model/tests、`docker-compose.yml`、`.env.example` 和
   `README.md`。

还进行了只读 search：`fetchAcceptedStationEvents` 全部 call sites、relative fetch、
`process.env`、`NEXT_PUBLIC_*`、request/forwarded headers、API origin/base、rewrite/
Route Handler/proxy/custom server、standalone/container/ports 和现有 configuration
validation patterns。结果是当前 `frontend/` 没有 API-origin env、header-derived origin、
rewrite、Route Handler、custom server、frontend Docker service 或 configured proxy。

## 3. Proven runtime defect

该 defect 已由独立 runtime feasibility probe 关闭，本 gate 不重新运行或质疑它：

| Evidence | Confirmed result |
| --- | --- |
| Valid accepted-events page query | HTTP 200 page response |
| Rendered UI state | `state-error` |
| Relative URL parse-error marker | present |
| `GET /api/v2/production/accepted-station-events` | not observed |
| API GET log count | `0` |
| Probe conclusion | `PASS` / `RELATIVE_URL_PRE_HTTP_FAILURE` |

当前 source 的实际调用是：

```ts
fetch("/api/v2/production/accepted-station-events?...", {
  method: "GET",
  cache: "no-store"
});
```

因此 failure 出现在 Server Component runtime 发出 HTTP 之前；它不是 API 4xx/5xx、
strict parser、view model、stale-data 或 API authority defect。修复目标必须是受控的
absolute URL resolution，而不是 same-origin transport 猜测或相对 URL fallback。

## 4. Current frontend/API deployment topology

| Surface | Current fact | Consequence |
| --- | --- | --- |
| Dashboard | Next.js `16.2.10`; dynamic Server Component; `output: "standalone"` | browser origin cannot be inferred as Node server's API target |
| Frontend package | only `test`, `typecheck`, `build` scripts | no current dev/proxy/origin configuration command abstraction |
| API | separate Compose `api` service; container and host port `8000` | it is not the Dashboard process or port |
| Compose | no frontend service or Dockerfile | `api` hostname is not currently a Dashboard runtime guarantee |
| `.env.example` | no Dashboard/API origin variable | no implicit default is available |
| Reverse proxy | none configured | forwarded headers have no established trust model |

Browser-visible and server-side API origins must remain independent. For example,
`https://dashboard.example` may render a Server Component which requests
`https://internal-api.example`; browser same-origin never authorizes deriving the
latter from the former. Equally, a container-local `http://api:8000` only has
meaning in a future frontend container attached to that Compose network; it is not a
host-runtime `localhost` replacement.

## 5. Scope and non-goals

In scope is only the planning of a secure production URL-resolution boundary for
`GET /api/v2/production/accepted-station-events`.

Out of scope: mock response/fixture, browser automation, API/contract changes,
endpoint changes, retry, timeout, auth/authz/token, gateway/load balancing, DB,
Docker implementation, real/local API validation, Collector/V-PLC/PLC, package
changes, Next config changes, status/handoff sync and every Git write after this
report. A need for any of those is a new exact-scope gate, not an implementation
detail of this report.

## 6. Contract and authority invariants

URL repair is transport configuration only. Future work must preserve all of the
following without reinterpretation:

- endpoint: only `GET /api/v2/production/accepted-station-events`;
- approved query keys only: `line_id`, `start_time`, `end_time`, `limit`, `cursor`;
- `buildAcceptedStationEventsQuery()` remains query authority; cursor remains opaque;
- `cache: "no-store"`, current-page-only summary and stale-data clearing remain;
- exact outer `{data,page}`, `data:{items}`, and `page:{next_cursor,limit}` schema;
- all 22 item own keys required; explicit JSON `null` legal; missing/unknown keys
  fail closed; malformed 2xx remains `kind: "error"`;
- existing 4xx → `invalid-query`, 503 → `unavailable`, other non-2xx/transport/
  parser errors → `error` classification;
- only `production_accepted_station_event_fact` is authority; no raw/debug/
  diagnostic/candidate/review/audit leakage and no `work_order` or `product`;
- `accepted_at` remains accepted-fact timestamp only, never freshness/ACK/read_done.

No URL resolver may synthesize data, alter query semantics, retry, select a fallback
endpoint, or make a malformed response look like empty/ready data.

## 7. API origin requirements

The production source is frozen as two **server-only runtime variables**:

```text
EDGE_MES_DASHBOARD_API_ORIGIN
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE
```

`EDGE_MES_DASHBOARD_API_ORIGIN` is the one canonical absolute API root. The profile
is required to make a deployment's hostname/port policy explicit rather than
implicitly trusting arbitrary configuration:

| Profile | Required origin form | Accepted use |
| --- | --- | --- |
| `local` | `http://127.0.0.1:8000`, `http://localhost:8000`, `http://[::1]:8000`, or an explicitly authorized loopback `:3100` smoke target | local frontend + local API or later loopback-only mock smoke |
| `container` | exactly `http://api:8000` | only a future frontend container on the same Compose network |
| `production` | `https://<non-loopback FQDN>` with default port 443 | standalone/reverse-proxy production deployment |

No profile may use an origin with a non-root pathname, query, fragment, or userinfo.
For `production`, IP literals (including private RFC1918 literals), `localhost`,
loopback, single-label hosts, `http:`, and non-443 ports are rejected. A production
FQDN may resolve to an internal address only through deployment-controlled DNS and
egress policy; DNS rebinding/egress firewall controls are operational follow-ups,
not a reason to accept an IP literal or request header in application code.

This is deliberately a closed profile allowlist. The exact configured origin is the
only permitted target for a resolved request; request data cannot add hosts, ports,
paths or schemes. If a future topology needs a different trusted host/port, it must
first extend this matrix through a new security planning gate, rather than silently
loosening the resolver.

`NEXT_PUBLIC_*` is forbidden. Neither variable may be read in browser code,
serialized into props, emitted in client bundles, or exposed in a response.

## 8. Approaches considered

| Approach | Assessment | Decision |
| --- | --- | --- |
| A. Explicit server-only API origin | Separates browser and server origins; compatible with standalone and containers; simple to validate and fail closed | **Selected**, with required profile policy |
| B. Derive from `Host`/`Forwarded`/`X-Forwarded-*` | Requires an absent proxy trust model; vulnerable to host/header injection, multi-value ambiguity and same-origin assumptions | Rejected |
| C. Explicit origin with trusted request-origin fallback | Reintroduces header trust, ambiguous precedence and deployment misuse for no required capability | Rejected; no fallback mode |
| D. Pass validated absolute origin into `apiClient` | Creates an explicit responsibility boundary; preserves fetch injection and prevents raw caller strings when branded type is used | Selected as the implementation shape beneath A |
| E. Next rewrite, Route Handler or proxy | risks permanent endpoint shadowing, routing/deployment coupling and does not by itself solve RSC absolute URL resolution | Rejected |
| F. Custom Next server supplies request origin | adds a startup/runtime dependency, risks standalone incompatibility and couples future mock work to production repair | Rejected |

Approach A plus D is intentionally not “use an environment variable” alone: it has
exact names, runtime timing, profile-specific host policy, syntax validation,
branded hand-off, fixed endpoint composition and no header/relative/default target.

## 9. Recommended architecture

Create a focused server-only resolver module:

```text
frontend/src/lib/acceptedStationEvents/apiOrigin.ts
```

Its public surface should expose a branded `TrustedAcceptedEventsApiOrigin` and a
request-time `resolveTrustedAcceptedEventsApiOrigin()` result. It reads both
variables when called, never at module import. It returns either a validated branded
root URL or a classified configuration failure; it must not throw raw environment
values into page/UI/log output.

`page.tsx` is the only production call site. After existing query validation succeeds,
it resolves the origin; failure renders the existing `kind: "error"` state and does
not call the client. On success it passes only the branded origin to the API client:

```ts
fetchAcceptedStationEvents(query, trustedApiOrigin, fetchImpl)
```

`apiClient.ts` must not accept an unvalidated `string` endpoint and must have no
environment/header knowledge. Tests may inject `fetchImpl` exactly as today. A TypeScript
brand is not an authorization mechanism by itself, so future code review and a
negative test must additionally enforce that no raw `process.env`/header/relative
URL is passed to `fetchAcceptedStationEvents`.

## 10. Environment/configuration contract

| Contract item | Frozen behavior |
| --- | --- |
| Read timing | request execution, inside resolver; not module import or build |
| Build requirement | no value required for `next build`; it must not be inlined |
| Runtime override | supported: restart standalone/server process with new server env; no rebuild |
| Missing/empty/profile missing | configuration error, `kind: "error"`, no fetch |
| Invalid/unsupported combination | configuration error, `kind: "error"`, no fetch |
| Precedence | only the two variables; no `.env` fallback, relative URL, localhost, `api`, browser host, request header or mock fallback |
| Public exposure | prohibited: no `NEXT_PUBLIC_*`, client prop or response echo |

Trailing slash is accepted and normalized to the root origin. Leading/trailing
whitespace and any ASCII control character are rejected before `URL` parsing;
normalization must not turn malformed configuration into a trusted value. A root
path is required: `https://internal-api.example/` is valid, while
`https://internal-api.example/base` and encoded/path-traversal variants are invalid.

This gate does **not** modify `.env.example`, `docker-compose.yml`, `README.md` or
`next.config.ts`. The repository currently has no frontend deployment topology, so
adding a root-level Compose value would falsely imply a host/container default. A
separate deployment/config documentation gate is required once a frontend service or
production process owner is authorized.

## 11. URL validation and composition

The resolver must reject, before any fetch:

- missing/empty values, unknown profile, whitespace/control characters or malformed URL;
- anything other than profile-allowed `http:`/`https:`;
- `username` or `password`;
- any query or fragment;
- non-root/encoded path prefix, ambiguous port or profile-host mismatch;
- local non-loopback address, container non-`api:8000`, or any forbidden production
  hostname/port/protocol.

The API client must compose a `URL` object, never string-concatenate:

```ts
const endpoint = new URL(
  "/api/v2/production/accepted-station-events",
  trustedApiOrigin
);
endpoint.search = buildAcceptedStationEventsQuery(query).toString();
```

Because the trusted base must have root pathname, the leading endpoint slash cannot
discard an approved prefix. `URLSearchParams` remains the only query construction
authority and encodes cursor values; the resolver never parses, decodes or edits a
cursor. The client then uses `endpoint.toString()` with `method: "GET"`,
`cache: "no-store"`, `credentials: "omit"`, and `redirect: "error"`. Rejecting
redirects prevents a validated first hop from becoming a second unvalidated outbound
target; a redirect produces the existing generic `kind: "error"` path.

## 12. SSRF and trust boundary

The resolver is a server-side outbound-request security boundary.

| Risk | Frozen control |
| --- | --- |
| Relative/default target | no fallback; invalid/missing config stops before fetch |
| Arbitrary scheme/file/data/ftp/unix | rejected by profile scheme policy |
| Userinfo credential leak | reject non-empty username/password |
| Query/fragment/base-path injection | reject on root origin; endpoint/query are constructed separately |
| Host/port escalation | closed profile matrix; exact target is config-derived only |
| Header injection / Host poisoning | resolver does not read `headers()`, `Host`, `Forwarded`, `X-Forwarded-Host` or `X-Forwarded-Proto` |
| Open redirect | `redirect: "error"` |
| Browser credential forwarding | `credentials: "omit"`; no production credential/header is authorized |
| DNS rebinding / egress | application rejects IP literals in production; deploy gate must constrain trusted DNS and network egress |

There is no trusted-proxy mode in this design. If one is ever needed, it requires a
new plan specifying proxy identity, direct-access rejection, canonical one-value
header extraction, CRLF/control rejection, repeated/multi-value rejection, host/port
validation and protocol validation. It is not an implementation shortcut.

## 13. Request/data flow

```text
AcceptedEventsPage
  -> validateAcceptedStationEventsQuery
  -> resolveTrustedAcceptedEventsApiOrigin (request-time server env only)
  -> fetchAcceptedStationEvents(query, TrustedAcceptedEventsApiOrigin, fetchImpl)
  -> buildAcceptedStationEventsQuery
  -> new URL(fixed endpoint, trusted root) + URLSearchParams
  -> fetch(absolute GET, no-store, omit credentials, redirect error)
  -> existing response classification
  -> existing strict parser
  -> existing view model
  -> existing UI state
```

An invalid query remains `invalid-query` before origin resolution/fetch. A valid query
with missing/invalid origin becomes `error`, renders no ready production data and
issues no accepted-events request. A valid resolved origin preserves every current
parser/classification/view-model branch.

## 14. Error and logging behavior

Configuration failure is a distinct cause within the existing `kind: "error"` UI
class, not `empty`, `invalid-query` or `unavailable`.

| Surface | Required behavior |
| --- | --- |
| User | fixed safe message: `Accepted events service is not configured.` |
| Server log | structured event code `DASHBOARD_API_ORIGIN_CONFIGURATION_ERROR`, profile/error category and variable names only |
| Never log | raw origin, parsed hostname, URL, query, credentials, token, browser `Host`/forwarded headers or request body |
| Upstream/API failures | retain current messages and classification; do not label them configuration failure |

The resolver's internal failure category may distinguish `missing`, `empty`,
`malformed`, `profile-mismatch`, `forbidden-scheme`, `forbidden-authority`,
`forbidden-path`, and `forbidden-url-component`; those labels are safe for server
diagnostics but are not returned to the browser.

## 15. Deployment matrix

| Scenario | Runtime configuration | Expected behavior |
| --- | --- | --- |
| Local frontend only, no API | unset | visible configuration `error`; zero outbound request; no fallback |
| Local frontend + local API | `PROFILE=local`, `ORIGIN=http://127.0.0.1:8000` | absolute server fetch to loopback API only |
| Local future mock smoke | `PROFILE=local`, `ORIGIN=http://127.0.0.1:3100` | only after separately authorized mock capability; URL repair supplies the required absolute target, not the mock itself |
| Standalone Next | inject `PROFILE=production`, `ORIGIN=https://internal-api.example` at process start | build artifact needs no env; runtime restart changes origin, rebuild is unnecessary |
| Future Docker frontend | inject `PROFILE=container`, `ORIGIN=http://api:8000` only in a separately authorized frontend service sharing Compose network | never valid on host runtime |
| Reverse proxy | server uses `PROFILE=production` internal API FQDN; browser may use a different dashboard FQDN | forwarded/browser headers remain irrelevant |

Illustrative future commands (not executed or authorized by this report):

```bash
# local development with an independently started local API
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=local \
EDGE_MES_DASHBOARD_API_ORIGIN=http://127.0.0.1:8000 \
frontend/node_modules/.bin/next dev --hostname 127.0.0.1 --port 3100

# after a separately authorized standalone build
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=production \
EDGE_MES_DASHBOARD_API_ORIGIN=https://internal-api.example \
HOSTNAME=127.0.0.1 PORT=3100 \
node frontend/.next/standalone/server.js
```

The second command is a production-profile topology example, not proof that
`internal-api.example` exists or is authorized today. Deployment-specific origin
ownership, DNS and service wiring stay with a separate deployment gate.

## 16. Mock-capability interaction

The previous same-origin no-DB mock-capability plan remains **HOLD**. Its relative
URL transport unknown is now closed by probe, but it cannot proceed until this URL
repair is implemented, reviewed and runtime-validated. This report neither designs
nor creates a mock, Route Handler, rewrite, custom server, fixture or intercept.

For a future loopback-only mock, an explicit `local` `http://127.0.0.1:3100` origin
can enable an absolute request to the approved single listener. It does not authorize
an API request, a second port, a browser session or a mock fallback when config is
missing. Browser/manual smoke remains separately CLOSED with recommendations and
cannot substitute for resolver/security tests.

## 17. Exact future implementation file allowlist

The following list is frozen for the future URL-resolution implementation gate only:

| Action | Exact file | Purpose |
| --- | --- | --- |
| Create | `frontend/src/lib/acceptedStationEvents/apiOrigin.ts` | server-only profile/env validation and branded trusted origin |
| Modify | `frontend/src/lib/acceptedStationEvents/apiClient.ts` | accept branded origin and compose absolute fixed endpoint |
| Modify | `frontend/src/app/accepted-events/page.tsx` | request-time resolution and safe configuration error rendering |
| Create | `frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts` | resolver/profile/negative/redaction tests |
| Modify | `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts` | absolute URL/composition/fetch option and no-relative regression tests |
| Modify | `frontend/src/app/accepted-events/__tests__/page.test.tsx` | resolver failure/no-fetch and ready-flow integration tests |

Not required in that implementation gate: `frontend/package.json`,
`frontend/package-lock.json`, `frontend/next.config.ts`, `frontend/tsconfig.json`,
`.env.example`, `docker-compose.yml`, `README.md`, API/DB/Collector/config/docs,
schema/query/viewModel, loading/error components, or any mock file. New dependency:
**none**; platform `URL`, `URLSearchParams`, TypeScript and existing Next/Node runtime
are sufficient.

`.env.example`, `docker-compose.yml` and `README.md` are deferred, not forgotten:
they require a follow-up deployment/config documentation gate that owns the actual
frontend service topology. Adding them in the URL implementation gate would expand
production deploy scope without an existing frontend container.

## 18. Exact future test file allowlist

Only the three paths named as test files in section 17 are allowed for the future
implementation test lane. Required cases are:

| Test area | Required assertions |
| --- | --- |
| Resolver | valid local HTTP, container `api:8000`, production HTTPS FQDN, trailing slash; request-time env reread |
| Resolver negatives | missing/empty/malformed; unknown profile; wrong profile pair; unsupported scheme; userinfo; query; fragment; pathname/encoded traversal; control/whitespace; prohibited host/port/IP; no secret/origin output |
| API client | fetch receives an absolute URL with exact endpoint and five approved query keys; cursor encoding; GET/no-store/omit/redirect error; `fetchImpl` remains injectable; no relative URL |
| Failure isolation | resolver failure means no `fetchImpl` call and visible `error` with no stale production surface |
| Contract regression | malformed 2xx still strict-parser `error`; 4xx/503/other classifications unchanged |
| Boundary regression | source search/test proves no `NEXT_PUBLIC_*`, raw `process.env`, request header, or unbranded string bypass at production call sites |

## 19. Future test and runtime validation strategy

The implementation gate must plan and run only its separately authorized command
sequence. Required evidence order is:

1. focused resolver unit tests;
2. focused API client tests;
3. focused page tests;
4. full frontend tests;
5. `npm run typecheck`;
6. `npm run build` plus generated-artifact audit/cleanup;
7. runtime missing-config probe;
8. runtime invalid-config probe;
9. separately authorized loopback local-API or no-DB mock probe;
10. browser/manual smoke only after mock-capability gate resumes.

Planned runtime acceptance probes, each needing separate authorization:

| Probe | Required proof |
| --- | --- |
| Missing configuration | Next starts; valid page query renders `error`; no accepted-events outbound request and no fallback |
| Invalid configuration | bad scheme/URL/profile fails before fetch; safe UI/log output |
| Explicit loopback origin | absolute method/path/query observed; strict parser remains in path; no contract change |
| Build/runtime | typecheck/build pass; standalone reads env at runtime; no origin/client-bundle leak |

Browser smoke is supplementary UI/network evidence. It cannot replace negative resolver,
SSRF, parser or source-boundary unit tests.

## 20. Package/config/dependency impact

| Surface | Future URL implementation decision |
| --- | --- |
| `frontend/package.json` | unchanged |
| `frontend/package-lock.json` | unchanged |
| new dependency | none |
| `frontend/next.config.ts` | unchanged |
| package scripts | unchanged |
| `.env.example` | unchanged in implementation; deployment-doc gate decides later |
| `docker-compose.yml` | unchanged; future frontend service is a separate gate |
| `README.md` | unchanged in implementation; deployment-doc gate decides later |

The existing `output: "standalone"` is compatible because Node server environment
variables are read at request time. The implementation must verify this instead of
assuming Next build-time substitution behavior.

## 21. Generated artifacts and cleanup

This planning gate creates no generated frontend artifacts. Future validation must
preflight and later remove only artifacts shown absent at preflight and created by its
own authorized commands, currently expected to include `frontend/.next/`,
`frontend/next-env.d.ts`, and `frontend/tsconfig.tsbuildinfo`. It must never use
`git clean`, reset/restore, broad deletion, or alter `frontend/node_modules/` and
external artifacts. Any unexpected tracked/config/package/generated drift is HOLD.

## 22. PASS conditions

This report is PASS-capable because it freezes all required design decisions:

- probe fact is accepted as `RELATIVE_URL_PRE_HTTP_FAILURE`;
- canonical source, exact names, strict precedence and request-time read are frozen;
- browser and server origin are explicitly distinct;
- missing/invalid configuration is `kind: "error"` with zero request and no fallback;
- no `NEXT_PUBLIC_*`, request header, relative URL, localhost default or Docker-name default;
- profile scheme/host/port/userinfo/query/fragment/path policies bound SSRF scope;
- URL composition, redirect and credential behavior are fixed;
- local/standalone/container/reverse-proxy/mock matrix is defined;
- exact code and test paths are frozen; package/config/dependency status is explicit;
- parser/contract/authority and stale-data behavior are preserved;
- runtime proof, cleanup and review sequence are explicit.

## 23. HOLD conditions

Future gates must stop with **HOLD** if any of the following appears:

- a different/no canonical source, `NEXT_PUBLIC_*`, relative/default/browser/header fallback;
- hardcoded `localhost`, `127.0.0.1`, `api:8000` or fixed port outside the frozen profile;
- request-header derivation without an independently approved trust model;
- origin userinfo/query/fragment/path, non-approved scheme/host/port, or redirect follow;
- an API contract/parser/authority/query/cursor/cache/stale-data change;
- inability to retain exact section-17 files, need for package/config/deploy/mock expansion;
- client-bundle configuration leak, sensitive log leak, unexpected outbound request, or
  build/runtime evidence contradicting request-time configuration;
- any stage/commit/push/deploy/runtime action without its own authority.

## 24. Required reviews

After a planning authority commit (not authorized here), the required sequence is:

```text
Architecture / Integration planning
-> planning authority commit
-> Reliability planning review
-> Data Quality planning review
-> Verification planning review
-> focused security/privacy review
-> PM implementation authorization
-> exact-scope implementation
-> implementation reviews
-> focused tests
-> full frontend tests
-> typecheck
-> build
-> runtime URL-resolution validation
-> resume mock-capability planning
-> browser/manual smoke
```

Review focus is fixed: Reliability reviews missing config, deployment profile and
fail-closed recovery; Data Quality guards endpoint contract/parser/authority/no-data
substitution; Verification checks exact URL/negative matrix/build/runtime evidence;
Security reviews SSRF, profile policy, scheme, host/header injection, credentials,
redirects and logging redaction.

## 25. Next gate sequence

Eligible next action is a **planning authority commit gate** for this single report,
but PM must explicitly authorize exact-path stage/commit/push first. No implementation
may start from this PASS WITH RECOMMENDATIONS result alone.

After the commit, the immediate work is the four planning reviews plus focused
security/privacy review. Only their accepted carry-forward conditions may be handed to
a Level-2 exact-file implementation authorization. The mock-capability plan remains
HOLD until that later implementation and runtime validation close.

## 26. Risks and recommendations

1. **Carry forward — deployment ownership:** no frontend Compose service or production
   reverse proxy exists. The profile matrix deliberately prevents this absence from
   becoming an unsafe default. Open a dedicated deployment/config-doc gate before
   documenting actual production values.
2. **Carry forward — egress/DNS:** application validation cannot prove DNS resolution
   or network egress safety. The future production deployment review must verify DNS
   ownership and egress restrictions for `production` profile FQDNs.
3. **Carry forward — mock capability:** absolute resolution is a prerequisite, not a
   mock design or proof. Keep the same-origin no-DB mock plan HOLD until its separate
   exact scope is re-reviewed.
4. **Closed by this plan:** relative URL feasibility is no longer an unknown; do not
   repeat the probe unless new evidence directly conflicts with its recorded result.
5. **Not a blocker:** no package, Next config, Docker or root env file change is
   required to implement the bounded resolver itself.

## 27. Thread output / context assessment

- 本次输出长度：长（durable planning report；window report 应保持简洁）。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：planning-only boundary 已冻结；authority commit、cross-functional reviews、
  security review、Level-2 implementation 和 runtime validation 均是不同授权，不能由
  本 gate 继承。
