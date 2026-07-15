# Sprint 3 Dashboard Raspberry Pi Docker Integration Verification Implementation Review

报告名称：

Sprint 3 Dashboard Raspberry Pi Docker Integration Verification Implementation Review

任务名称：

Gate B — Dashboard Raspberry Pi Docker Integration Verification Focused Implementation Review

执行 Thread：

Verification

## Conclusion

**PASS WITH RECOMMENDATIONS**

六文件 exact allowlist、Dockerfile/.dockerignore 静态边界、process-only /health、Compose
service 语义、本地 focused/typecheck/build 验证、部署 startup/resource/port/rollback/
cancellation 终局以及未来 real Case A/B/C evidence authority 均未发现 blocker。

本结论是 focused implementation review closure，不是以下任一项的 PASS：

~~~
Docker image build
Compose startup
Linux ARM64 build/run
Raspberry Pi deployment
Dashboard runtime health
API/DB readiness
rollback/cancellation drill
real Case A/B/C
DB/API/Dashboard 三层真实闭环
~~~

当前 evidence classification 保持：

~~~
synthetic / focused implementation evidence
local source/build evidence
Compose static parsing evidence（仅 PM 提供）
~~~

## Recovery baseline

本轮第一动作完成 read-only recovery，结果与任务预期一致：

~~~
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 683a8a0eb9f901dbc5c53c9bef5c4e68acf95ffb
origin/main: 683a8a0eb9f901dbc5c53c9bef5c4e68acf95ffb
ahead/behind: 0 0
latest: 683a8a0 Add PM handoff after Gate A closeout
cached diff: empty
tracked diff before report: .gitignore, docker-compose.yml, docs/deployment/raspberry_pi.md
target report before creation: absent
~~~

六文件在 recovery 时精确为：

~~~
M  docker-compose.yml
M  docs/deployment/raspberry_pi.md
?? frontend/Dockerfile
?? frontend/.dockerignore
?? frontend/src/app/health/route.ts
?? frontend/src/app/health/__tests__/route.test.ts
~~~

既有 .gitignore、旧 handoff/reports、Keynote artifact、既有 Gate B planning/review
reports、frontend/.next/、frontend/node_modules/、frontend/next-env.d.ts 与
frontend/tsconfig.tsbuildinfo 均视为 external/generated artifacts，未删除、清理、
恢复、stage、commit 或 push。

## Scope

### Reviewed files

~~~
frontend/Dockerfile
frontend/.dockerignore
frontend/src/app/health/route.ts
frontend/src/app/health/__tests__/route.test.ts
docker-compose.yml
docs/deployment/raspberry_pi.md
~~~

### Created report

~~~
docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_verification_implementation_review.md
~~~

目标报告在 recovery 时不存在，本轮只创建这一份报告；没有覆盖旧报告。

### Explicitly not touched

~~~
六个 implementation 文件
frontend/package.json
frontend/package-lock.json
frontend/next.config.ts
frontend/tsconfig.json
frontend/src/lib/acceptedStationEvents/**
frontend/src/app/accepted-events/**
frontend/src/components/accepted-events/**
api/**
collector/**
db/**
config/**
Grafana / V-PLC / other Compose services
docs/current_status.md
docs/thread_handoff/pm_operating_rules.md
.gitignore 与既有 external/generated artifacts
~~~

## Exact allowlist audit

判定：**PASS**。

- docker-compose.yml 与 docs/deployment/raspberry_pi.md 是本任务唯一 tracked
  implementation modifications。
- 四个 CREATE 路径是本任务唯一新增 implementation paths。
- protected paths tracked diff 为空；cached diff recovery 时为空，且本轮未执行任何
  Git write。
- docker-compose.yml diff 仅新增 dashboard service；没有修改 API、PostgreSQL、
  Collector、Grafana、V-PLC、Simulator、Prometheus 或其他 core service 语义。
- 外部 .gitignore 与 generated/untracked artifacts 不计入 Gate B implementation
  scope。

## Implementation verification matrix

| 审查项 | 结果 | 独立判定 |
| --- | --- | --- |
| Dockerfile static buildability | PASS | node:22.23.0-bookworm-slim、deps/builder/runner、tracked lockfile + npm ci、standalone/static/public copy、server.js、non-root node、runtime env 与 ownership 静态自洽；未发现必然 COPY/startup/permission failure。 |
| .dockerignore coverage | PASS | 排除 .next、node_modules、TypeScript generated files、coverage、logs、.git、.env*、editor/cache/temp；保留 package.json、package-lock.json、Next/TS config、src/、Dockerfile 与未来 public/，无 secret/artifact negation。 |
| /health route | PASS | 固定 200 与 exact {"status":"ok","service":"dashboard"}；不读取 API origin、DB、fact、filesystem 或 query，不调用 fetch。 |
| /health focused test | PASS | global fetch spy 有效挂载；断言 status、JSON content type、exact body、exact keys、fetch 未调用；异常 origin/profile env 不影响结果；async response 已 await，env/global cleanup 已执行。 |
| Compose dashboard service | PASS | context ./frontend、Dockerfile、edge-mes-dashboard:local、container_name、restart: "on-failure:5"、3001:3000、production env、HOSTNAME=0.0.0.0、PORT=3000、http://api:8000、container profile、api: service_started 均符合冻结语义。 |
| Compose healthcheck | PASS | runner 内置 node + Node 22 global fetch，只访问 http://127.0.0.1:3000/health；非 2xx/transport error 退出失败，不访问 API/DB/fact。 |
| Validation coverage | PASS | 本轮 fresh focused test/typecheck/build/diff-check 均通过；build 输出同时包含 /health 与 /accepted-events。PM 的 Compose parse 证据单独标为 static parsing。 |
| Process vs dependency health | PASS | /health 只证明 Next HTTP process；API /health/DB/accepted facts 继续是独立 runtime/data evidence。API unavailable 时 page 保持 fail closed、无 retry/fallback/stale truth，新 request 才恢复。 |
| Startup/restart terminal gate | PASS WITH RECOMMENDATIONS | 文档定义 bounded 120s、docker compose ps、RestartCount、health、bounded logs、failure 后 docker compose stop dashboard 与 stopped 终局；“超过 5 次 restart”建议统一为 RestartCount >= 5，但当前已无无界等待或超过 Compose 上限后继续 evidence 的可信路径。 |
| Port 3001 preflight | PASS WITH RECOMMENDATIONS | ss -ltnp 与实际可用的 nft/ufw/iptables 检查均有 bounded 入口；listener 或 firewall boundary 无法确认均为 HOLD，不换 port、不停止未知 listener。建议补 cancellation 后固定 command/result 模板。 |
| Resource preflight | PASS WITH RECOMMENDATIONS | DockerRootDir、docker system df、docker builder du、current/rollback image、/opt 与 Docker root filesystem、memory、Swap、双 30s sample、6 GiB/rollback-size/Swap/metric HOLD 条件均已冻结。建议统一 bytes 记录与增长算式。 |
| Build failure | PASS | failure、timeout、OOM、incomplete image 均为 terminal stop；failure 后禁止 compose up、host artifacts、换 Node/origin/profile、取消 non-root、auto-prune 或删除 rollback image。 |
| Postflight | PASS WITH RECOMMENDATIONS | startup 前重新检查 filesystem、image/cache growth、image size、120s Swap delta 与双 sample；3 GiB、3 GiB、1 GiB、256 MiB 门禁明确，失败则 HOLD。建议将 bytes 算式写成固定 record 模板。 |
| Dashboard-only update | PASS | 唯一路径为 docker compose up -d --build --no-deps dashboard；full up -d --build 与 down 明确不是 Dashboard-only，禁止主动重建/重启 core services。 |
| Release protection | PASS WITH RECOMMENDATIONS | Gate B Section 10 明确六文件 changed-file scope 不等于完整 release baseline，并保护 data/、remote .env、.git、host generated artifacts、node_modules、.next、__pycache__、*.pyc；旧通用 sections 仍保留 full-stack commands，建议继续强化 operator warning。 |
| Existing Dashboard rollback | PASS WITH RECOMMENDATIONS | 要求 source release ID、old files/image tag+ID、resolved Compose/service baseline；恢复旧 image 后只 force-recreate dashboard，验证 /health、一次 bounded accepted-events request、core non-rebuild、data/.env 不变；缺资产/证据为 HOLD。建议补固定 request/result 模板，不能用 screenshot/health 单独 PASS。 |
| First-deployment cancellation | PASS | 准确命名为 first-deployment cancellation / existing-core-services non-impact validation；stop/rm Dashboard、恢复文件、config --quiet、无 container、3001 释放、core baseline/health 不变、data/.env 不覆盖；不声明 rollback、Dashboard health、accepted-events 或 Case PASS。 |
| Case A/B/C | PASS | Case A real station_result OK mandatory；Case B real station_result NOK mandatory；Case C real station_nok detail conditional，不存在时 NOT AVAILABLE / NOT VERIFIED，禁止 synthetic/mock/API-only/Case B/cycle substitution。 |
| Exact 22 fields | PASS | 逐字段 DB raw、API raw JSON、display rule、Dashboard visible value、PASS/FAIL 表格已要求，且 placeholder 不得写入 API raw 列。 |
| Identity/lineage | PASS | 主 identity 为 fact_key，同时核对 source_event_id、content_fingerprint、event_ts、accepted_at；未将 source/fingerprint/time 字段互换或作为 fact identity 替代。 |
| items[0] claim scope | PASS | 每个 case 使用独立 bounded request 让目标成为 items[0]；声明范围限定为该 request 的目标第一项，不扩大为整页、时间窗或全库。 |
| Empty/pagination/failure/recovery | PASS WITH RECOMMENDATIONS | planning authority 与 deployment semantics 已把 items=[]、无 stale、opaque cursor、scope 保持、stable order、无重复/遗漏、one request/render、API stop/503/5xx/transport/malformed 2xx、new-request recovery 定义为后续 mandatory evidence；建议补固定 operator record 模板。缺任何必需 runtime evidence 时仍必须 HOLD，不能以截图/health/container running 替代。 |
| Evidence classification | PASS | focused test → synthetic/focused；typecheck/build → local source/build；Compose config → static parsing；Dashboard /health → process readiness；image inspect → image identity；DB raw + API raw + UI map → real three-layer case。未见低层证据升级为 real closure。 |

## Process health and dependency health adjudication

当前实现与文档保持以下不可合并的证据边界：

~~~
Dashboard /health 200
    -> Next HTTP process readiness only

API /health / PostgreSQL / accepted fact / Dashboard page
    -> independent runtime and data evidence
~~~

depends_on: service_started 只表示启动顺序。Dashboard process healthy 不会因 API
failure 自动变成 unhealthy，也不构成 DB/API/Dashboard closed loop。page 恢复只能由
新的 request 触发；一次 render 不 retry、不 fallback、不保留旧 production truth。

## Startup, port, resource and failure terminal adjudication

静态 authority 足以要求后续 operator 在 runtime gate 中记录：

~~~
最多 120s healthy window
docker compose ps dashboard
docker inspect ... RestartCount/health/image
bounded docker compose logs
failure 后 docker compose stop dashboard
stopped/non-restarting/non-sustained-unhealthy terminal state
~~~

Port、resource、build failure、postflight 任一 required boundary 无法确认时均保持
HOLD。文档没有提供通过替换 port、重建 core services、host artifact、auto-prune、
删除 rollback image 或降低 non-root boundary 来绕过的路径。

RestartCount 当前使用“超过 5 次 restart”文字而非统一的 RestartCount >= 5；这是
off-by-one 可复核性 recommendation。Compose on-failure:5 与 120s/stopped terminal
conditions 已防止无界等待，因此不升级为 blocker。

## Executed validation

以下均为本轮实际执行、且未触碰 Docker/Compose runtime、DB、API request、server/browser
runtime、SSH、Raspberry Pi 或真实 evidence：

| Command | Exit | Fresh result |
| --- | ---: | --- |
| cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && node -v | 0 | v22.23.0 |
| cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm test -- src/app/health/__tests__/route.test.ts | 0 | Test Files 1 passed (1)；Tests 1 passed (1) |
| cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && npm run typecheck -- --incremental false | 0 | tsc --noEmit --incremental false completed without error |
| cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend && NEXT_TELEMETRY_DISABLED=1 npm run build | 0 | Next 16.2.10 build completed；routes include ƒ /accepted-events and ƒ /health |
| cd /Users/chenjie/Documents/MES/edge-mes-demo && git diff --check -- frontend/Dockerfile frontend/.dockerignore frontend/src/app/health/route.ts frontend/src/app/health/__tests__/route.test.ts docker-compose.yml docs/deployment/raspberry_pi.md | 0 | no output |

git diff --check 是用户指定的本轮命令；untracked implementation files 同时已按源文件
静态读取，未被纳入 cached diff。build 产生/刷新 .next 与 TypeScript generated
artifacts，均保持 external/generated 状态，未手工删除或清理。

## PM-provided Compose evidence

PM 提供的前序证据为：

~~~
cd /Users/chenjie/Documents/MES/edge-mes-demo
docker compose config --quiet
echo $?
~~~

结果：

~~~
no error output
exit code: 0
~~~

本轮没有重新运行该命令，遵守“不运行 Docker/Compose config”的限制。该证据只证明
Compose v2 static parsing；不证明 Docker image build、Compose startup、health、ARM64、
Pi、API/DB readiness 或 real Case A/B/C。

## Reliability/Data Quality recommendations adjudication

前序 recommendations 均不构成本轮 blocker，裁决如下：

1. RestartCount >= 5：当前“超过 5 次 restart”存在 off-by-one 表述风险，但
   Compose on-failure:5、120s bounded window、health/restarting/stopped failure
   conditions 与显式 stop 已形成 fail-closed 终局；carry-forward recommendation。
2. Rollback bounded accepted-events request：文档已把该 request 设为 mandatory post-
   rollback evidence，并明确 screenshot/health 不能单独形成 PASS；缺失证据必须
   HOLD。固定 URL/result record 是可复核性增强 recommendation。
3. First-cancellation 后的 listener/core baseline record：mandatory outcome 已明确，
   固定 command/result 模板增强复核性，不改变现有 non-impact gate。
4. Image/cache bytes 与 growth 算式：阈值、baseline、required metric failure、
   no-auto-prune 与 pre/post 顺序均已明确；现场无法读取或无法计算时必须 HOLD。
   当前缺统一 bytes 模板，属于 recommendation。
5. Base digest、final image identity/size、native linux/arm64/v8：实现与文档未
   虚构 runtime evidence，后续 Pi gate 必须补齐；属于 carry-forward。
6. Empty/pagination/failure/recovery operator templates：planning authority 已将其
   作为后续 evidence invariant；当前缺固定记录模板不允许跳过验证后宣称 PASS，因此
   属于 recommendation，不是静态 implementation blocker。
7. 旧通用 full-stack up/down 命令：Gate B Section 10.7 明确其不是 Dashboard-only
   path；建议继续增加 operator warning，但不改变当前 scoped semantics。

## Blockers

~~~
none
~~~

未发现：

~~~
六文件外 implementation diff
Dockerfile 静态必然失败
health test 无法证明 no-fetch/exact response
health 依赖 API/DB/fact
Compose service 语义不符合冻结要求
validation 失败
startup/restart 等待无界
failure 后仍可无条件继续 runtime evidence
resource gate 无法判定或可通过 cleanup 绕过
port 冲突可绕过
Dashboard-only update 会重建 core services
release 会覆盖 data/.env
rollback 缺失资产仍可 PASS
first deployment 被称为 rollback
Case A/B/C 分类或 identity 混淆
items[0] 被扩大为整页 closure
synthetic/static evidence 被升级为 real evidence
live Git / allowlist / protected-path 冲突
~~~

## Recommendations

1. 将 startup failure predicate 统一写成 RestartCount >= 5，同时保留 120s、health、
   stopped 和 bounded logs 终局。
2. 为 startup failure、3001 cancellation listener、rollback bounded request、known-empty、
   pagination page 2、first-cancellation core baseline 增加固定 command/result record。
3. 将 image/cache/disk/Swap pre/post evidence 统一为 bytes，并给出 image growth、cache
   growth 与 combined growth 的算式；required metric 或计算无法完成时保持 HOLD。
4. 后续 runtime gate 记录 node:22.23.0-bookworm-slim resolved digest、final image
   ID/size、实际 linux/arm64/v8 build/run、120s healthy terminal、RestartCount 与
   bounded logs。
5. 保持 Case C 缺失时的 NOT AVAILABLE / NOT VERIFIED，并把每个 case 的声明严格限于
   独立 bounded request 的 items[0]。
6. Runtime evidence 继续逐项区分 real DB-backed、synthetic、static parsing、process
   readiness 与 image identity；任何缺失 mandatory row/API/UI/identity/22-field evidence
   均不得升级为 PASS。

## Authorization boundary

本轮没有获得、也没有行使以下授权：

~~~
implementation edits
Docker build / run
docker compose config / build / up / down / lifecycle
PostgreSQL / API request / DB query
server/browser runtime
SSH / Raspberry Pi command / port-firewall preflight
resource pre/postflight
rollback / first-deployment cancellation
real Case A/B/C
git add / commit / push / tag / restore / reset / clean
~~~

## Git status

报告创建前：

~~~
six-file implementation: 2 tracked modifications + 4 untracked implementation files
cached diff: empty
protected paths tracked diff: empty
~~~

报告创建后唯一新增 repository artifact 为本报告；外部 .gitignore 与既有/generated
artifacts 保持排除。最终只读复核确认：

~~~
git diff --name-only
git diff --cached --name-only
git status --short --untracked-files=all
~~~

其中 cached diff 保持为空；本报告是唯一新增 report-only change，六文件之外的其他
新增 artifacts 不计入本任务。

## Next gate

PASS WITH RECOMMENDATIONS 后可进入：

~~~
PM intake
Gate B Reliability implementation review: closed / PASS WITH RECOMMENDATIONS
Gate B Data Quality implementation review: closed / PASS WITH RECOMMENDATIONS
Gate B Verification implementation review: closed / PASS WITH RECOMMENDATIONS
PM exact-path implementation/review-report commit gate eligibility
~~~

仍需单独授权：

~~~
Docker build/start
Compose lifecycle
Linux ARM64 / Raspberry Pi deployment
port/firewall preflight
resource pre/postflight
rollback/cancellation drill
PostgreSQL/API runtime
real Case A/B/C
~~~

本 review 不允许从 static implementation review 直接跳到 Raspberry Pi runtime。

## Thread output / context assessment

~~~
本次输出长度：长
当前 Thread 是否建议继续：no
下一轮是否建议新开 Thread：yes
理由：Gate B Verification implementation review 已闭合；下一步是 PM intake 与
exact-path commit gate，runtime/deployment 仍需独立授权，且本轮上下文已覆盖完整
authority chain、六文件、前序 reviews 与 fresh local validation。
~~~
