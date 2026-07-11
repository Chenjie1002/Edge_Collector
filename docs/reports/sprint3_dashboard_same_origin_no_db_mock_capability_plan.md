# Sprint 3 Dashboard same-origin no-DB mock-capability planning gate report

报告名称：Sprint 3 Dashboard same-origin no-DB mock-capability planning gate report

任务名称：Design a deterministic, production-safe, same-origin no-DB mock capability for Dashboard accepted-events browser/manual smoke

执行 Thread：Architecture / Integration

风险等级：Level 1

结论：**HOLD**

本 gate 仅规划：未启动 server/browser/API/DB/Docker/runtime，未运行 tests/typecheck/build/probe，未安装 dependency，未改动 frontend/API/config/package/lockfile/test，未 stage、commit 或 push。

HOLD 精确原因：动态 Server Component 的 `fetch("/api/v2/production/accepted-station-events?..." )` 是相对 URL。静态审计无法可靠证明 Next 16.2.10 Server runtime 是否提供 origin、是否发出 HTTP、最终 host/port，或是否回环到 Next listener。因此不能冻结真实 mock transport 或 exact implementation file allowlist，也不能称 implementation-ready。

## 1. Baseline and read-only recovery

`main`; `HEAD == origin/main == 23fc439a05aa52e1b09d0d45e5ea0a21d25d9ed5`; latest `23fc439 Freeze Dashboard browser smoke planning`; cached diff empty; diff name-only only `.gitignore`。外部 dirty set 与预期一致：`.gitignore`、七个声明的 docs/report/handoff artifacts、`frontend/node_modules/`（12,252 entries）；均未触碰。目标报告开始时不存在。

## 2. Context reviewed

已按要求顺序只读审计 PM rules、handoff、status、Dashboard contract、vertical validation、stale-data、typecheck/build、browser smoke reports；并审计授权的 package/config、page/loading/error/tests、apiClient/query/schema/viewModel、component/tests。Next node_modules 仅检索 custom server/Route Handler/rewrite/instrumentation 文档与入口。

## 3. Current repository findings

- Next 16.2.10 / React 19.2.7 / TypeScript 6.0.3；scripts 只有 `test`、`typecheck`、`build`。
- `next.config.ts` 只有 `output: "standalone"`；无 rewrite/proxy/API base URL/mock mode。
- page 是 dynamic Server Component；apiClient default global fetch 发 relative URL，`GET` / `cache: "no-store"`。
- 无 custom server、Route Handler、middleware/proxy、rewrite、fixture、MSW、browser runner 配置。lockfile transitive MSW metadata 和 Next experimental files 不等于已配置 tooling。

## 4. Current Server Component request flow

`browser -> page.tsx -> query validation -> fetchAcceptedStationEvents -> buildAcceptedStationEventsQuery -> global fetch(relative URL) -> transport (unproven) -> response.json -> parseAcceptedStationEventsEnvelope -> toAcceptedEventsViewModel -> AcceptedEventsPageView`。invalid query 在 fetch 前失败；non-2xx/JSON/parser/transport failure 均映射 non-ready state。

## 5. Relative URL fetch feasibility

无 browser document origin 的 Server runtime 不可从现有 source 推知 relative URL 可解析；也不可证明 custom server/Route Handler/rewrite 可捕获。若 parse-before-HTTP 失败，apiClient catch 产生 `kind:"error"`。必须先开独立 commands-only probe（本 gate 未执行）：preflight 记录 `.next`/`next-env.d.ts`/`tsconfig.tsbuildinfo`、port 3100、temp dir；启动现有 Next binary 仅绑定 `127.0.0.1:3100` 并记录 PID/log；curl 一个仅含批准 query 的 page URL；依据响应/日志判别 parse error、same-origin HTTP 或其他失败；TERM 已记录 PID、证明 port release、只清理由本次生成的 exact paths。parse error 必须另开 URL-resolution production-runtime planning gate；HTTP evidence 仍须定位 capture boundary。

## 6. Mock capability goals

未来能力必须 default-off、deterministic、no-DB、loopback-only、全合成，并完整经过 page/query/apiClient/HTTP/strict parser/view model/UI。禁止 fixture import page、view-model injection、static HTML、预先合法化 malformed body、或 browser interception 冒充 server-side request。禁止 DB/Docker/remote/internet/Collector/V-PLC/PLC/credential/real cookie/header。

## 7. Contract and authority invariants

仅 `GET /api/v2/production/accepted-station-events` 与 `line_id,start_time,end_time,limit,cursor`；唯一 authority `production_accepted_station_event_fact`；exact outer/data/page/item own keys、完整 22-key DTO、null legal/missing illegal、unknown fail closed、malformed 2xx -> error、cursor opaque、accepted_at only fact timestamp、current-page-only、无 raw/debug/diagnostic/candidate/review/audit/work_order/product。

## 8. Approaches considered

| Approach | Decision |
| --- | --- |
| A dev-only custom Next server | Conditional preferred after probe：one loopback port、no dependency；必须证明 RSC HTTP 可捕获且与 standalone 兼容。 |
| B env-gated Route Handler | Reject：即使 disabled 仍占/shadow production path，default safety不明。 |
| C rewrite + second process | Reject；two ports/processes，**requires browser/manual smoke plan amendment and separate PM approval**。 |
| D fetch injection/instrumentation/resolver | 非 mock-only；可能只测 fake transport 或成为 production runtime repair。 |
| E local no-DB API | 排除为 Level-1 first option：扩大 API/port/proxy risk。 |

## 9. Scenario selector alternatives

Option 1 reserved `line_id` 可重复但污染业务语义且有 production misuse 风险；Option 2 env per server start default-off/immutable、不加第六 query key、但每场景重启；Option 3 loopback control channel 增 endpoint/port/state/cleanup 风险。条件推荐 Option 2：显式 opt-in + 每进程 immutable whitelist scenario；delay 用单独启动，不设 control endpoint。

## 10. Recommended architecture

**Conditional recommendation, not implementation-ready.** one Node custom dev server process / one `127.0.0.1:3100` listener. Only `EDGE_MES_DASHBOARD_MOCK=enabled` + whitelisted scenario launches it and logs synthetic-only. exact GET/path/query guard emits raw status/body; every other request forwards to Next; apiClient retains JSON/parser handling. Production `next start`/deployment never launches it. Single listener cannot truthfully simulate TCP refusal；network failure remains automated transport-test authority。

## 11. Production-default safety

Unset opt-in has no mock path/fallback/Route Handler shadow. Reject unknown scenario; bind only 127.0.0.1; no credential; synthetic stable `SYNTHETIC_`/`TEST_` IDs/cursors/fact keys/timestamps and visible startup marker。

## 12. Request and data flow

Positive flow is section 4 exactly. Negative fixtures remain raw malformed HTTP bodies until response.json/strict parser. DevTools is not primary internal-fetch evidence; server logs qualify only after probe proves listener reachability。

## 13. Deterministic scenario matrix

- 200: empty, accepted OK, accepted NOK, NOK detail, complete all-null, next cursor.
- 4xx and invalid/expired/cross-scope cursor; 503; malformed 200 envelope/missing key/unknown outer/data/page/item key; invalid JSON; delayed response.
- True transport refusal remains existing/new automated injected-fetch test primary. Browser smoke samples UI/loading/error only; existing parser/stale-data tests remain primary closed evidence.

## 14. Security and synthetic-data policy

Fixtures are authored synthetic only: no DB export, production log, real DMC/unit/supplier/operator/host/token/credential/cookie/header. No internet. Evidence only in separately authorized external temporary location; not Git by default.

## 15. Exact future implementation file allowlist

**Not frozen: HOLD.** Non-authorizing candidates only: `frontend/scripts/dashboard-accepted-events-mock-server.mjs`; `frontend/src/lib/acceptedStationEvents/mockFixtures.ts`; `frontend/src/lib/acceptedStationEvents/mockScenario.ts`. `frontend/src/lib/acceptedStationEvents/apiClient.ts` only if probe proves relative failure—then separate production URL-resolution repair, not mock-only. Excluded absent new authority: page, next config, package, lockfile. Generated-only if preflight absent: `.next/`, `next-env.d.ts`, `tsconfig.tsbuildinfo`, then exact cleanup. Future test paths cannot freeze before runtime boundary is known.

## 16. Exact future test strategy

Proposal only: exact-path tests for default-disabled/scenario whitelist; GET/path/query and unsupported key rejection; 22-key/null/forbidden fields; malformed pass-through; 4xx/503/JSON/network mapping; cursor opacity; loopback bind; PID/port cleanup; no production shadow. Runtime probe, implementation tests, browser smoke and existing closed regression evidence remain distinct. typecheck/build are separate gates.

## 17. Exact future command allowlist

All proposal only—not executed. Preflight: `git status -sb`; HEAD/origin/diff/cached/status excluding node_modules; exact generated-path existence; `lsof -nP -iTCP:3100 -sTCP:LISTEN`. Probe start: `frontend/node_modules/.bin/next dev --hostname 127.0.0.1 --port 3100` to a unique external temp dir, record `$!`; curl valid page URL; capture headers/body/log/listener; `kill -TERM` only recorded PID and prove port release. Conditional mock start is `EDGE_MES_DASHBOARD_MOCK=enabled EDGE_MES_DASHBOARD_MOCK_SCENARIO=<whitelist> node frontend/scripts/dashboard-accepted-events-mock-server.mjs --hostname 127.0.0.1 --port 3100`. Future focused test/typecheck/build are separately authorized. Never npm install/ci, npx download, git clean/reset/restore, broad delete, killall/pkill, or `rm -rf frontend`。

## 18. Ports, processes and network boundary

Conditional design is one process/one port `127.0.0.1:3100`; browser and accepted-events API same origin only. Any second address/port/outbound connection/credential/DB/runtime connection/unexpected method-path-query is immediate HOLD。

## 19. Generated artifacts and cleanup

Record preflight state of generated artifacts, PID/log/temp/evidence/browser/listener. Close browser, TERM recorded PID, prove release, then only remove exact preflight-absent artifacts created by run. Never clean node_modules/external artifacts/unknown paths or mask drift with Git.

## 20. PASS conditions

PASS requires probe-resolved Server Component URL/capture; exact implementation/test files frozen; default-off/no-shadow proof; no-DB single-port loopback; no dependency; exact command/cleanup; no browser-plan conflict。

## 21. HOLD conditions

Relative fetch uncertainty; URL repair without new planning; endpoint shadow; extra query key; DB/Docker/remote; dependency; second port without amendment; apiClient/parser bypass; default-off uncertainty; or broad cleanup.

## 22. Risks and recommendations

Carry forward feasibility probe as blocker. Parse failure requires production URL-resolution planning; HTTP result requires custom-server compatibility/default-off proof. Do not overclaim network refusal manual evidence. Approach C needs explicit browser plan amendment.

## 23. Required reviews

After probe/exact scope: Architecture / Integration, Reliability, Data Quality, Verification, focused security/privacy. Browser plan amendment not needed for one process/one port; mandatory for Approach C. Sequence: planning commit -> probe -> if needed URL planning -> reviews -> implementation -> reviews -> tests/typecheck/build -> manual smoke. None is authorized here.

## 24. Next gate sequence

Eligible next gate: new commands-only runtime feasibility probe Thread with its own exact temp/PID/evidence/artifact allowlist. PM approval required before probe, commit, implementation, tests, server/browser or Git write.

## 25. Thread output / context assessment

- 本次输出长度：large planning report; window concise.
- 当前 Thread 是否建议继续：no.
- 下一轮是否建议新开 Thread：yes.
- 理由：relative URL feasibility is a separate commands-only runtime boundary and must not inherit report-write authority.
