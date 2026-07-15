# Sprint 3 Dashboard Raspberry Pi Docker Integration Verification Planning Review

报告名称：Sprint 3 Dashboard Raspberry Pi Docker Integration Verification Planning Review

任务名称：Gate B — Dashboard Raspberry Pi Docker Integration Verification Planning Review / Exact Future Implementation Allowlist Audit

执行 Thread：Verification

日期：2026-07-14

## Conclusion

**PASS WITH RECOMMENDATIONS**

本轮为 Gate B Verification planning review。六文件 future implementation allowlist 对冻结的 Dashboard Docker image、Compose service、Dashboard process health、Raspberry Pi deployment/resource/rollback guide 与后续 real Case A/B/C evidence planning 是 necessary、sufficient、exact、non-expanding。

未发现当前 blocker。该结论只表示 planning review closure，不表示 Gate B implementation、Docker/Compose、Raspberry Pi、real DB-backed Case A/B/C、DB/API/Dashboard 三层闭环或 Git write 已执行或通过。

当前 evidence classification 仍为：

~~~
synthetic / focused implementation evidence
~~~

## 1. Recovery baseline

第一动作完成 read-only recovery，live Git 结果为：

~~~
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 683a8a0eb9f901dbc5c53c9bef5c4e68acf95ffb
origin/main: 683a8a0eb9f901dbc5c53c9bef5c4e68acf95ffb
latest: 683a8a0 Add PM handoff after Gate A closeout
ahead/behind: 0 0
tracked diff: .gitignore only
cached diff: empty before this report creation
Gate B authority files: clean before this report creation
future targets: Dockerfile/.dockerignore/health route/test absent; compose/deployment present
generated artifacts: frontend/.next/, frontend/next-env.d.ts, frontend/node_modules/,
  frontend/tsconfig.tsbuildinfo present
~~~

Handoff 文件内部记录的 40c95bda... 是其 authoring-time baseline；live Git authority 已前进到 683a8a0...，且当前差异不影响 Gate B gate state、allowlist、authorization、excluded files 或 review authority，因此不构成 HOLD。

本轮未运行 tests、typecheck、build、Docker、Compose、PostgreSQL、SSH、Raspberry Pi、browser/server runtime、deployment、rollback、listener/port 操作，也未执行任何 Git write。

## 2. Current gate and review scope

Gate A 当前状态：

~~~
Accepted-events Consumer Truth Hardening: CLOSED / PASS WITH RECOMMENDATIONS
current evidence: synthetic / focused implementation evidence
real DB-backed Case A/B/C: NOT EXECUTED / NOT CLAIMED
Raspberry Pi runtime and Docker/Compose: NOT EXECUTED / NOT CLAIMED
~~~

本轮只审查 Gate B planning authority，不重开旧 Dashboard production URL Option C / 强审计 runtime-evidence 分支。

### Reviewed files

按 PM 指定顺序读取并静态审查：

~~~
docs/thread_handoff/pm_operating_rules.md
docs/thread_handoff/chatgpt_pm_handoff_260714-2155.md
docs/current_status.md
docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_plan.md
docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_reliability_review.md
docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_reliability_rereview.md
docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_review.md
docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_rereview.md
docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_rereview_round2.md
docs/reports/sprint3_accepted_events_consumer_truth_hardening_architecture_review.md
docs/reports/sprint3_accepted_events_consumer_truth_hardening_reliability_review.md
docs/reports/sprint3_accepted_events_consumer_truth_hardening_data_quality_review.md
docs/reports/sprint3_accepted_events_consumer_truth_hardening_verification_review.md
docker-compose.yml
docs/deployment/raspberry_pi.md
frontend/package.json
frontend/package-lock.json
frontend/next.config.ts
frontend/tsconfig.json
frontend/src/lib/acceptedStationEvents/apiOrigin.ts
frontend/src/lib/acceptedStationEvents/apiClient.ts
frontend/src/app/accepted-events/page.tsx
api/app/routes/health.py
api/app/routes/accepted_station_events.py
~~~

### Created file

~~~
CREATE docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_verification_review.md
~~~

### Explicitly not touched

~~~
frontend/Dockerfile
frontend/.dockerignore
frontend/src/app/health/route.ts
frontend/src/app/health/__tests__/route.test.ts
docker-compose.yml
docs/deployment/raspberry_pi.md
frontend/src/lib/acceptedStationEvents/schema.ts
frontend/src/lib/acceptedStationEvents/apiClient.ts
frontend/src/lib/acceptedStationEvents/viewModel.ts
frontend/src/components/accepted-events/**
frontend/src/app/accepted-events/page.tsx
frontend/package.json
frontend/package-lock.json
frontend/tsconfig.json
frontend/next.config.ts
API / DB / Collector / Grafana / V-PLC contracts or implementation
~~~

## 3. Exact six-file allowlist assessment

| Path | Decision | Gate B responsibility |
| --- | --- | --- |
| frontend/Dockerfile | Necessary | Multi-stage standalone build, npm ci, Node 22.23.0, ARM64-compatible image, non-root runtime, standalone/static/public copy |
| frontend/.dockerignore | Necessary | Exclude host/generated artifacts, .env*, .git, node_modules, coverage and logs without excluding build inputs |
| frontend/src/app/health/route.ts | Necessary | Fixed small Dashboard HTTP process readiness response only |
| frontend/src/app/health/__tests__/route.test.ts | Necessary | Fixed response shape/2xx and no-fetch/no-external-dependency proof |
| docker-compose.yml | Necessary | dashboard service, runtime env, port, local healthcheck, depends_on, bounded restart and no source/data mounts |
| docs/deployment/raspberry_pi.md | Necessary | Exact release/update boundary, resource gates, port preflight, rollback/cancellation and protected paths |

### Necessary

六个文件均有独立职责，删除任一文件都会使冻结 scope 缺少 image build boundary、health proof、Compose integration 或 deployment/resource/rollback authority。

### Sufficient

六个文件足以承载当前冻结 scope：

- Dockerfile 可从既有 tracked package.json、package-lock.json、next.config.ts、tsconfig.json 与 src/ 构建 standalone image；不需要 package、lockfile、TypeScript 或 Next config 变更。
- .dockerignore 可在 build context 边界阻断 host node_modules、host .next、generated files、.env* 与 .git；不需要清理现有 dirty/generated artifacts。
- 独立 /health route/test 可证明 Dashboard process readiness，不需要复用 API health、API route 或 DB contract。
- Compose 与 deployment guide 可共同承载 3001、http://api:8000、restart、资源、update、rollback/cancellation 与 protected-path rules。
- real Case A/B/C 是后续 evidence gate，不需要修改 accepted-events consumer business files、API、DB、Collector 或 Grafana。

### Missing paths

~~~
none
~~~

未发现必须修改六文件外路径的 mandatory requirement。package.json、tracked package-lock.json、next.config.ts 与 tsconfig.json 已提供 dependency、standalone 与 TypeScript authority；api/app/routes/health.py 的 DB-backed health 不能替代新 Dashboard /health，但也不需要修改。

### Unnecessary paths

~~~
none
~~~

不应因本 Gate 加入 accepted-events schema/apiClient/viewModel/renderers/tests、API、DB、Collector、Grafana、V-PLC、package/config 或额外 Compose service。

### Excluded paths

以下路径继续明确 excluded，不得借 Gate B repair 或 deployment evidence 扩大：

~~~
frontend/src/lib/acceptedStationEvents/schema.ts
frontend/src/lib/acceptedStationEvents/apiClient.ts
frontend/src/lib/acceptedStationEvents/viewModel.ts
frontend/src/components/accepted-events/**
frontend/src/app/accepted-events/page.tsx
frontend/package.json
frontend/package-lock.json
frontend/tsconfig.json
frontend/next.config.ts
api/**
db/**
collector/**
Grafana
V-PLC
other Compose services
~~~

## 4. Verification planning matrix

### Docker image and build context

- Plan freezes node:22.23.0-bookworm-slim, multi-stage build, tracked package-lock.json as dependency authority, npm ci, standalone output, native Linux ARM64 Pi build, non-root node runtime, no runtime npm install, and runtime copies limited to standalone, static and public.
- .dockerignore must exclude .next, node_modules, tsconfig.tsbuildinfo, next-env.d.ts, coverage, logs, .git and .env*, while retaining package.json, package-lock.json, next.config.ts, tsconfig.json, src/ and other build inputs.
- Host node_modules, host-built .next, macOS artifacts and .env must not enter context or image.
- Result: PASS WITH RECOMMENDATIONS. Future implementation/release evidence must record the resolved base manifest/image digest and final image ID/size; actual ARM64 build/run remains NOT EXECUTED.

### Origin, network and port

- Browser topology is http://<Raspberry-Pi-IP>:3001 → Dashboard container port 3000 → server-side http://api:8000 → API → PostgreSQL.
- Compose must inject server-only EDGE_MES_DASHBOARD_API_ORIGIN=http://api:8000 and EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=container.
- No build arg, NEXT_PUBLIC_*, localhost, 127.0.0.1 API origin, relative URL, host port 8000, browser-origin fallback, browser-side api DNS access or custom network is allowed.
- Dashboard host port is frozen at 3001; Grafana remains 3000. Repository static absence of conflict is not Pi proof; remote listener/firewall conflict is HOLD and port substitution is forbidden.
- Result: PASS WITH RECOMMENDATIONS. Future deployment evidence should record a bounded 3001 listener/firewall preflight result explicitly.

### Dashboard process health

- New /health is fixed small response and 2xx only; it reads no query, origin, API, DB, accepted facts or business filesystem state, and calls no fetch or other external dependency.
- Its test must freeze response shape/status and prove no fetch.
- Existing api/app/routes/health.py executes PostgreSQL SELECT 1 and is not reused. Dashboard healthy must never be called API healthy, DB healthy, accepted fact present or DB/API/Dashboard closed-loop PASS.
- Result: PASS.

### Compose and bounded process behavior

The planned dashboard service precisely covers:

~~~
image: edge-mes-dashboard:local
container_name: edge-mes-dashboard
ports: 3001:3000
restart: "on-failure:5"
depends_on:
  api:
    condition: service_started
local-only healthcheck at 127.0.0.1:3000/health
~~~

It has no source, node_modules, .next, data, .env or Docker socket mount, no privileged, host network or extra capabilities, and does not modify other services.

API failure must not fail local Dashboard process health or trigger Dashboard restart. One render makes at most one API request; there is no retry/fallback; API recovery happens only on a new page request; no stale production truth is retained.

The 120-second terminal authority is explicit: more than 5 restarts, persistent restarting/unhealthy or failure to become healthy is a failure; deployment must then execute docker compose stop dashboard. Logs use bounded tail/time windows. No crash-loop, request storm or log storm is authorized.

Result: PASS.

### Resource gates

Build preflight must record Docker root directory, docker system df, docker builder du, current Dashboard image ID/size, rollback image ID/size when present, /opt/edge-mes-demo filesystem free space, Docker root filesystem free space, memory used and Swap used, including two 30-second samples.

The preflight thresholds are explicit: relevant filesystem free space at least 6 GiB, or max(6 GiB, 2 × rollback image size + 3 GiB) when a rollback image exists; unreadable required metric, missing required rollback asset or continuously growing Swap is HOLD.

Build failure, timeout, OOM or incomplete image is terminal stop; no compose up, host artifacts, changed origin/profile/Node image, non-root removal, auto-prune or rollback-image deletion.

Postflight must recheck the metrics before deploy: free space at least 3 GiB, image plus BuildKit cache growth no more than 3 GiB, Dashboard image no more than 1 GiB, after 120 seconds Swap increase no more than 256 MiB, and two 30-second post samples show no continued Swap growth. Any failure retains old assets and is HOLD.

Result: PASS.

### Deployment and protected paths

- Remote path is /opt/edge-mes-demo.
- Release transport must protect data/ and remote .env and exclude .git/, frontend/node_modules/, frontend/.next/, frontend/tsconfig.tsbuildinfo, frontend/next-env.d.ts, __pycache__/ and *.pyc.
- Dashboard-only update is exactly docker compose up -d --build --no-deps dashboard. Full docker compose up -d --build and docker compose down are not Dashboard-only commands; API, PostgreSQL, Collector, Grafana, V-PLC and other core services must not be rebuilt or interrupted.
- Result: PASS WITH RECOMMENDATIONS. Future deployment-doc repair should enumerate the six approved release paths instead of relying only on “PM-approved release files” wording.

### Rollback and first-deployment cancellation

For a remote release with an existing previous Dashboard, the required assets are source release ID/commit, previous release files, old image tag and image ID, resolved Compose baseline, and service/container baseline. Recovery verifies Dashboard /health, one bounded accepted-events request, no API/PostgreSQL/Collector/V-PLC rebuild, and no data/ or remote .env overwrite. Missing asset or evidence is HOLD.

For first deployment with no previous Dashboard, the terminal name is first-deployment cancellation / existing-core-services non-impact validation. The failed Dashboard is stopped and removed; pre-deployment Compose/release files are restored; docker compose config --quiet passes; no edge-mes-dashboard container remains; host port 3001 is not listening; core service/container/image state and health match the deployment baseline; Collector/API/PostgreSQL/Grafana/V-PLC are not rebuilt; data/ and remote .env are not overwritten or reinitialized.

This path must not claim Dashboard rollback PASS, Dashboard /health PASS or accepted-events page PASS. Both paths prohibit docker compose down, volume delete, image prune, data restore, DB migration rollback and other-service rebuild.

Result: PASS.

### Real Case A/B/C and identity

- Case A is real accepted station_result / production_result=ok and is mandatory.
- Case B is real accepted station_result / production_result=nok with accepted non-null nok_code and nok_origin and null detail companion fields and is mandatory.
- Case C is real accepted station_nok detail companion only when a legal real Pi DB row exists; otherwise the result is NOT AVAILABLE / NOT VERIFIED. Case C cannot be replaced by synthetic fixture, mock response, API-only fixture, Case B or cycle event.
- Each case uses fact_key as primary identity and also checks source_event_id, content_fingerprint, event_ts and accepted_at. The target must be items[0] of the independent bounded API response.
- Each case records all 22 fields as DB raw value, API raw JSON value, display rule, Dashboard visible value and PASS/FAIL. Display placeholders do not populate the API raw column.
- Result: PASS.

### Empty, pagination, failure/recovery and evidence labels

- Known-empty bounded window must yield API items=[] and explicit Dashboard empty state with no old row/detail/summary/trace truth.
- Pagination uses next_cursor; the second independent request passes the opaque cursor unchanged and preserves line_id/start_time/end_time/limit scope; stable order, no duplicates, no omissions and one request per render are required.
- API stopped, 503, other 5xx, transport failure and malformed 2xx remain process-healthy/fail-closed or unavailable/error as specified; there is no stale truth, retry, fallback or partial salvage. Recovery only occurs on a new request; restart retains canonical env/origin.
- Focused/mocked evidence remains synthetic. Real closure requires PostgreSQL raw row, API raw JSON and Dashboard visible-value mapping. Health/build/screenshot/fixture/API-only evidence cannot be declared real closed-loop.
- Result: PASS.

## 5. Blockers

~~~
none
~~~

静态审查未发现六文件 allowlist 不充分、六文件外 mandatory path、health/API/DB/fact 语义混淆、unbounded restart/retry/request/log loop、资源门禁绕过、rollback/cancellation 伪 PASS、Case A/B/C identity 混淆、synthetic evidence 冒充 real closure 或 task-specific live Git/authority conflict。

## 6. Recommendations / carry-forward

以下均不阻断当前 planning closure：

1. Future Dockerfile implementation evidence 保存 node:22.23.0-bookworm-slim 的 resolved manifest/base digest 与最终 edge-mes-dashboard:local image ID/size，并保存实际 linux/arm64/v8 native build/run 证据。
2. Future docs/deployment repair 明确列出六个 approved release paths，并为 3001 listener/firewall preflight、rollback image absent 分支和 required metric unavailable 分支定义 bounded command/result record。
3. /health implementation/test 固定不可变 response shape 与明确 2xx status，并证明没有 fetch、API/DB/fact/file-system business dependency；不要把 healthcheck 结果升级为 closed-loop PASS。
4. Future runtime evidence 继续分别标记 real DB-backed、synthetic、NOT AVAILABLE / NOT VERIFIED，并把每个 case 的声明限制为独立 bounded request 的目标 items[0]。
5. Resource/rollback evidence 在 deploy 前保存 old release/image/baseline identity；缺失任一 required asset 或任一阈值失败立即 HOLD，不自动 prune、不删除 rollback image、不重建 core services。

## 7. Authorization boundary

~~~
Gate B implementation: not authorized
Dashboard tests/typecheck/build: not authorized by this review
Docker/Compose: not authorized
Raspberry Pi runtime/deployment/rollback: not authorized
PostgreSQL / real Case A/B/C: not authorized
Git stage/commit/push/tag: not authorized
~~~

本报告不授权从 planning review 直接跳入 implementation 或 runtime；PM 必须另行批准 implementation、tests、runtime/deploy/rollback 与 Git write lanes。

## 8. Git status

### Before report creation

~~~
cached diff: empty
tracked diff: .gitignore only
Gate B authority files: clean
~~~

### After report creation

~~~
report-only change:
  ?? docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_verification_review.md
cached diff: empty
~~~

Known external dirty artifacts remain excluded and untouched：

~~~
M .gitignore
docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
docs/reports/phase1_to_sprint2_management_keynote_10p.html
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_*.md
docs/reports/sprint3_db_backed_api_validation_reliability_review.md
docs/thread_handoff/chatgpt_pm_handoff_20260624.md
docs/thread_handoff/chatgpt_pm_handoff_20260625.md
docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
docs/thread_handoff/chatgpt_pm_handoff_260712-1349.md
docs/thread_handoff/chatgpt_pm_handoff_260713-1916.md
docs/thread_handoff/chatgpt_pm_handoff_260714-1450.md
frontend/.next/
frontend/next-env.d.ts
frontend/node_modules/
frontend/tsconfig.tsbuildinfo
~~~

本轮未删除、整理、清理、stage、commit、push 或改变上述 artifacts。

## 9. Next gate

~~~
Gate B Verification planning review: CLOSED / PASS WITH RECOMMENDATIONS
allowlist: necessary / sufficient / exact / non-expanding
next eligible action: PM review and separate Gate B implementation authorization
implementation: not authorized
runtime/deployment/rollback: not authorized
Git write: not authorized
~~~

PM approval required before implementation、tests、Docker/Compose、Raspberry Pi runtime、real evidence execution or Git write. No HOLD repair is required at this planning gate.

## 10. Thread output / context assessment

~~~
本次输出长度：中
当前 Thread 是否建议继续：yes
下一轮是否建议新开 Thread：no
理由：Gate B planning review scope 已闭合，下一步仍可在既有 Verification Thread 中承接独立 implementation authorization；不得与旧 Dashboard URL runtime-evidence 或其他 Gate 混合。
~~~
