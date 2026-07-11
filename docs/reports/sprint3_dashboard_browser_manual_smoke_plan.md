# Sprint 3 Dashboard browser/manual smoke planning gate report

报告名称：Sprint 3 Dashboard browser/manual smoke planning gate report

任务名称：Freeze the exact browser/manual smoke execution boundary for the Dashboard accepted-events page without starting any server, browser, API, DB or runtime

执行 Thread：Architecture / Integration

风险等级：Level 1

结论：PASS WITH RECOMMENDATIONS

本报告只冻结未来 browser/manual smoke execution boundary。本 gate 未启动 server、browser、API、DB、Docker、Collector、V-PLC 或 PLC；未运行 tests/typecheck/build；未安装 dependency；未创建 mock、截图或临时输出；未 stage、commit 或 push。

## 1. Baseline and read-only recovery

在 /Users/chenjie/Documents/MES/edge-mes-demo 的 live recovery 为：

~~~text
branch: main
HEAD == origin/main:
c085226f0d911e12041e89d6e0587e660847e389
latest commit:
c085226 Add PM handoff before browser smoke planning
cached diff:
empty
~~~

外部 dirty set 与预期一致：M .gitignore、七个声明的未跟踪 docs/report/handoff 文件及 frontend/node_modules/（12,252 entries）。均未被修改、删除、cleanup、stage 或 commit。

## 2. Required context reviewed

已按顺序只读审计：
- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260711-1802.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
- docs/contracts/dashboard_api_contract.md
- docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md
- docs/reports/sprint3_dashboard_ui_state_stale_data_plan.md
- docs/reports/sprint3_dashboard_frontend_typecheck_build_validation_plan.md
- 授权列出的 package/config、accepted-events page/loading/error/test、API client/query/schema/view model 和 UI components。

strict parser、22-field explicit-null、UI/state stale-data 和 typecheck/build 均为 CLOSED。manual smoke 仅做 runtime-visible 抽样，不能替代或重新开启它们。

## 3. Scope

本 gate 的唯一写入文件为本报告。未来 browser/manual execution 默认：

~~~text
expected tracked source/config/package/test changes: none
~~~

需要改动 production source、test、package、lockfile、Next/TS config 或 mock 文件时，execution 必须 HOLD，并由 PM 新开 exact-scope implementation gate。

## 4. Current runtime/tooling findings

| Finding | Static evidence | Planning result |
| --- | --- | --- |
| Scripts | frontend/package.json only has test, typecheck, build; no dev/start/preview | execution 不得添加 script；仅可在另行授权下直接调用现有 local Next binary。 |
| Runtime | Next 16.2.10; next.config.ts has output: standalone | dev 不需 prior build；production mode 必须重新 build，因为原 .next 已清理。 |
| Fetch | dynamic server page → apiClient relative GET /api/v2/production/accepted-station-events, cache: no-store | browser interception 不能被假定可拦截 server-side fetch。 |
| Mock/fixture | no frontend/src/app/api route、mock API、static fixture、API base URL/rewrite 或 configured intercept | 完整 data/state matrix 今日不能 commands-only 执行。 |
| Browser tooling | no direct Playwright/Cypress/Selenium/Puppeteer dependency, script, config or output dir | 第一个 lane 为 manual；automation 另开 planning/implementation。 |
| Artifacts | closed build gate gives frontend/.next/, frontend/next-env.d.ts, frontend/tsconfig.tsbuildinfo | preflight 后仅精确清理这些新生成路径。 |

package-lock 的 transitive optional mentions 不等于已配置的 MSW 或 Playwright。

## 5. Browser/manual smoke goals

未来 smoke 只验证 read-only consumer 可见行为和 network boundary：

~~~text
GET /api/v2/production/accepted-station-events only
query keys: line_id, start_time, end_time, limit, cursor only
authority: production_accepted_station_event_fact only
outer keys: data,page; data: items; page: next_cursor,limit
meta unsupported; cursor opaque/API-owned
~~~

不得暴露 raw/debug/diagnostic/candidate/review/audit 或 legacy/raw fallback、work_order、product；accepted_at 只能是 accepted fact timestamp，不能是 freshness/ACK/read_done。manual 不能完整证明 DB authority、22-field/null matrix、strict parser negative matrix 或全量 API 语义。

## 6. Approaches considered

| Approach | Current readiness | Runtime/artifacts | Risk and coverage | Decision |
| --- | --- | --- | --- | --- |
| A. Next dev + deterministic mock/intercept + manual browser | Next binary exists，same-origin mock 不存在 | no prior build; dev may generate .next, next-env, tsbuildinfo | mock closure 后可 no-DB 覆盖 UI/network state | 推荐第一条 browser lane，但以前置 mock-capability closure 为条件。 |
| B. production build/server + mock | no start script, no mock | new authorized build required | repeats build/config-drift/cleanup risk | 不作为 first lane。 |
| C. Playwright/Cypress | not configured | depends on runtime | repeatable but needs dependency/config/browser/output policy | 单独 gate；本 lane 不安装。 |
| D. frontend + local accepted-events API | API outside scope; no no-DB fixture service found | mode-dependent | API/DB/runtime risk | 非默认；单独 authorization lane。 |

## 7. Recommended first execution lane

选择 Approach A，但必须先关闭独立的 Level 1 same-origin no-DB mock-capability planning/implementation/review sequence。mock 必须使实际 page.tsx → apiClient.ts → query builder → strict parser 路径运行，不得直接注入 page/view model 或替换 RSC/document response。

缺少该能力是 execution prerequisite，不是本 planning report 的 blocker。Browser DevTools override 只有在另行证明可到达 server-side fetch/parser 时才可考虑，否则不可作为 data source/evidence。

## 8. Runtime/server/API/mock boundary

候选 frontend runtime command，proposal only — not executed in this planning gate：

~~~bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
frontend/node_modules/.bin/next dev --hostname 127.0.0.1 --port 3100
~~~

dev 优于 production preview：无 build prerequisite。next start 不作为首选，因为它需要新授权 next build、生成 artifacts，且不解决 mock gap。

先决 mock capability 必须是 same-origin、no-DB，并提供 deterministic valid empty/OK/NOK、malformed 2xx、4xx、503、network/JSON failure、next cursor、invalid/expired/cross-scope cursor。它必须：
- 不连接 DB、Docker、remote API、production credential、Collector、V-PLC 或 PLC；
- 处理 frontend origin 上的 relative accepted-events path；
- 维持 exact envelope、22-key DTO 和 explicit JSON null；
- 将 malformed fixture 经过真实 strict parser；
- 在 commands-only smoke 内 immutable；需要编辑则 HOLD。

## 9. Port and network boundary

| Surface | Frozen boundary |
| --- | --- |
| Frontend | 127.0.0.1:3100 only；禁止 0.0.0.0、::、LAN、VPN、public bind。 |
| Mock/API | same-origin 127.0.0.1:3100/api/v2/production/accepted-station-events only；本 plan 不批准 second API port。 |
| Browser | http://127.0.0.1:3100/accepted-events 和批准 query variants only。 |
| API request | GET exact path；仅 line_id,start_time,end_time,limit,cursor。 |
| Ancillary requests | same-origin Next/RSC/static/dev assets only，单独记录。 |
| Forbidden | internet/external endpoint、remote DB/Postgres、Docker、SSH tunnel、Raspberry Pi、Collector、V-PLC、real PLC、production credential。 |

unexpected host/endpoint/method/query key、non-loopback listener、credential request 或 DB/runtime connection 是 immediate HOLD。

## 10. Browser/manual scenario matrix

Manual evidence = DOM/URL/Network/Console observation；automated evidence is sampled only，不能声称覆盖所有 code path。

| # | Scenario | Expected manual evidence | Automated evidence / manual limit |
| ---: | --- | --- | --- |
| 1 | no query/missing required | invalid-query; no API request | page/query; sample |
| 2 | invalid limit | invalid-query; no request | query/page; sample |
| 3 | invalid time | invalid-query; no request | query; sample |
| 4 | inverted window | invalid-query; no request | query; sample |
| 5 | over-31-day | invalid-query; no request | query; sample |
| 6 | loading | loading; no old table/summary/NOK/trace | stale-data; timing sample |
| 7 | empty | bounded-scope empty + zero current-page summary | stale-data/page |
| 8 | ready accepted OK | table + current-page summary | component/view model; fixture not production proof |
| 9 | ready accepted NOK/detail | accepted NOK/detail only | component/view model |
| 10 | malformed success | error, never empty/ready | strict parser/API client; one fixture only |
| 11 | API 4xx | invalid-query, no ready data | API client/page |
| 12 | API 503 | unavailable, no ready data | API client/page |
| 13 | network/JSON/parser failure | error, no ready data | API client |
| 14 | next cursor | opaque; visible only if approved navigation exists | query/view model; current page no next-page action |
| 15 | same-scope cursor forward | unchanged opaque cursor in request | query; needs navigation/control |
| 16 | line scope change | new scope request, no old truth | query/stale-data |
| 17 | time scope change | new scope request, no old truth | query/stale-data |
| 18 | limit scope change | new scope request, no old truth | query/stale-data |
| 19 | scope change clears cursor | resulting request has no cursor | query |
| 20 | invalid/expired/cross-scope cursor | 4xx → invalid-query | API contract/client; full binding is API validation |
| 21 | ready → loading | all prior truth hidden | stale-data |
| 22 | ready → error | all prior truth hidden | stale-data |
| 23 | ready → unavailable | all prior truth hidden | stale-data |
| 24 | ready → invalid-query | all prior truth hidden | stale-data |
| 25 | non-empty ready → empty | old values absent; current zero counts | stale-data |
| 26 | page summary | literal Current page only; no total-across-pages | view model/component |
| 27 | accepted_at | Accepted fact timestamp only; no freshness/ACK/read_done | view model/page |
| 28 | forbidden surfaces | raw/debug/diagnostic/candidate/legacy absent from UI/DOM/Console/request/fixture | schema/page; scan non-exhaustive |
| 29 | no work_order/product | absent from UI/DOM/Console/request/fixture | schema/view model |
| 30 | endpoint-only call | Network API entry is accepted-events GET with approved query names | API client; framework assets excluded but same-origin |

AcceptedEventsQueryControls has optional onSubmit and no router navigation. Direct URL variants may be used in a future lane; adding navigation code during execution is forbidden.

## 11. Evidence and screenshot/log policy

Future evidence:
- one screenshot per approved visible state, URL/query only when scope proof requires it;
- Network method/host/path/query key names/response classification;
- page-session Console and DOM-visible state;
- server stdout/stderr, PID, readiness, stop and port release;
- generated-artifact inventory; preflight/final Git audit.

Do not capture credentials, tokens, secret headers, sensitive fixture values, unrelated tabs or unrelated local paths. Default evidence location is a separately authorized external temporary location; no screenshot/log/HAR enters Git automatically. Repository evidence requires another exact-path authorization. This gate creates none.

## 12. Exact future command allowlist

All commands are proposal only — not executed in this planning gate. Future PM prompt must authorize the lane, the approved mock-capability commit and any external temporary evidence directory. No command creates the missing mock.

### 12.1 Read-only preflight

~~~bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
git status -sb
git log -1 --format='%H %s'
git rev-parse origin/main
git diff --name-only
git diff --cached --name-only
git status --short --untracked-files=all | grep -v '^?? frontend/node_modules/' || true
git status --short --untracked-files=all -- frontend | grep -v '^?? frontend/node_modules/' || true
find frontend -maxdepth 2 \( -name '.next' -o -name 'out' -o -name 'dist' -o -name 'coverage' -o -name '*.tsbuildinfo' -o -name 'next-env.d.ts' \) -print | sort
~~~

### 12.2 Server start, readiness, PID

~~~bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
mkdir -p "${TMPDIR:-/tmp}/edge-mes-dashboard-smoke"
frontend/node_modules/.bin/next dev --hostname 127.0.0.1 --port 3100 >"${TMPDIR:-/tmp}/edge-mes-dashboard-smoke/next-dev.stdout.log" 2>"${TMPDIR:-/tmp}/edge-mes-dashboard-smoke/next-dev.stderr.log" &
echo $! >"${TMPDIR:-/tmp}/edge-mes-dashboard-smoke/next-dev.pid"
for attempt in 1 2 3 4 5 6 7 8 9 10 11 12; do
  curl --fail --silent --show-error --max-time 5 http://127.0.0.1:3100/ >/dev/null && break
  sleep 1
done
curl --fail --silent --show-error --max-time 5 http://127.0.0.1:3100/ >/dev/null
cat "${TMPDIR:-/tmp}/edge-mes-dashboard-smoke/next-dev.pid"
lsof -nP -iTCP:3100 -sTCP:LISTEN
~~~

curl is loopback readiness only, not scenario evidence.

### 12.3 Browser/manual work

Open only http://127.0.0.1:3100/accepted-events and approved query variants. Per scenario record URL, visible result, Network and Console. Do not sign in, use production profile, accept certificate exception or navigate outside loopback. First lane has no automation command.

### 12.4 Stop, cleanup, final Git audit

~~~bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
kill -TERM "$(cat "${TMPDIR:-/tmp}/edge-mes-dashboard-smoke/next-dev.pid")"
for attempt in 1 2 3 4 5; do
  lsof -nP -iTCP:3100 -sTCP:LISTEN >/dev/null || break
  sleep 1
done
! lsof -nP -iTCP:3100 -sTCP:LISTEN
ps -p "$(cat "${TMPDIR:-/tmp}/edge-mes-dashboard-smoke/next-dev.pid")" -o pid=,command= || true
rm -rf /Users/chenjie/Documents/MES/edge-mes-demo/frontend/.next
rm -f /Users/chenjie/Documents/MES/edge-mes-demo/frontend/next-env.d.ts
rm -f /Users/chenjie/Documents/MES/edge-mes-demo/frontend/tsconfig.tsbuildinfo
git status -sb
git diff --name-only
git diff --cached --name-only
git status --short --untracked-files=all -- frontend | grep -v '^?? frontend/node_modules/' || true
find frontend -maxdepth 2 \( -name '.next' -o -name 'out' -o -name 'dist' -o -name 'coverage' -o -name '*.tsbuildinfo' -o -name 'next-env.d.ts' \) -print | sort
~~~

rm -rf only applies to exact preflight-absent frontend/.next created by authorized server. Never use git clean, broad rm -rf, find -delete, git restore/reset or clean frontend/node_modules/external artifacts.

## 13. Exact future file/generated-artifact allowlist

| Category | Frozen rule |
| --- | --- |
| Read-only | frontend/package.json, frontend/package-lock.json, frontend/next.config.ts, frontend/tsconfig.json, listed accepted-events files, approved mock record, this report. |
| Tracked changes | none; source/config/package/test/mock change is HOLD. |
| Generated | only preflight-absent frontend/.next/, frontend/next-env.d.ts, frontend/tsconfig.tsbuildinfo, then exact cleanup. |
| Evidence | external temporary files only if separately authorized; never auto-save/stage in repo. |
| Repair | none; obtain new exact allowlist. |
| Excluded | .gitignore, frontend/node_modules/, all external artifacts, api/**, collector/**, db/**, config/**, Docker, README, status docs, all Git writes. |

## 14. Process and artifact cleanup

Future owner records PID and port ownership before browser use, applies readiness timeout, closes manual/automation browser session, sends TERM, proves port release, and removes only allowed newly generated artifacts. Failure path: capture allowed evidence, stop server/browser, exact-clean transient artifacts, then HOLD. No server may remain for a later task.

## 15. PASS conditions

PASS requires matching PM baseline/external artifacts and empty cached diff; approved no-DB same-origin mock; 127.0.0.1:3100 only; endpoint/method/query boundary correct; authorized matrix results correct; no stale truth; current-page-only and accepted timestamp semantics correct; forbidden fields absent; server/browser/PID/port and generated artifacts cleaned; final frontend no tracked drift; external artifacts unchanged; no Git write and no API/DB/Docker/Collector/V-PLC/PLC side effect.

## 16. HOLD conditions

HOLD for absent/bypassing/unapproved mock; required package/config/source/test/tooling install; listener/network/request boundary violation; cursor parsing/construction/mutation; malformed 2xx rendered as empty/ready; stale truth or forbidden field visible; process/port/artifact cleanup failure or broad cleanup need; cached/tracked/external drift; or stage/commit/push/deploy/tag/rollback.

## 17. Explicit exclusions

No mock implementation, browser automation install, local/real API, API tests, DB/Postgres, Docker, SSH tunnel, Collector/V-PLC/PLC runtime, frontend repair/router work, package/config change, typecheck/build rerun, docs/status sync, stage, commit, push, deploy, tag or rollback.

## 18. Blockers

None for this planning gate.

Execution prerequisite: deterministic same-origin no-DB mock/intercept does not currently exist. PM must authorize its exact planning/implementation/review before full manual smoke. Missing browser automation is a repeatability tradeoff, not a blocker.

## 19. Recommendations

1. Carry forward a Level 1 same-origin no-DB mock-capability planning gate with exact files and proof of real server fetch/API client/parser use.
2. After closure, open a new commands-only Approach A manual smoke Thread using this report's preflight, network, evidence and cleanup rules.
3. Use direct URL variants until router/navigation is separately authorized.
4. Evaluate Playwright/Cypress only in a separate planning/implementation gate with package/lock/config/browser/evidence allowlists.
5. Keep strict parser, all-22 null, stale-data and typecheck/build CLOSED; smoke is supplemental only.

## 20. Next gate

Eligible for:

~~~text
Level 1 — Dashboard same-origin no-DB mock-capability planning gate
Owner: Architecture / Integration
Mode: planning-only
~~~

PM approval remains required before mock implementation, server/browser execution, automation, API/local API, typecheck/build/tests, DB/Docker/runtime, docs/status sync or Git writes.

## 21. Thread output / context assessment

- 本次输出长度：长
- 当前 Thread 是否建议继续：no
- 下一轮是否建议新开 Thread：yes
- 理由：planning-only boundary 已冻结；mock capability design/implementation 与 runtime execution 需要独立 authorization，不能继承本次权限。
