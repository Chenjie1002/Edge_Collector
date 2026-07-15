# Sprint 3 Dashboard Raspberry Pi Docker Integration Reliability Implementation Review

报告名称：`Sprint 3 Dashboard Raspberry Pi Docker Integration Reliability Implementation Review`

任务名称：`Gate B — Dashboard Raspberry Pi Docker Integration Reliability Focused Implementation Review`

执行 Thread：`Reliability`

## Conclusion

**PASS WITH RECOMMENDATIONS**

六文件实际实现未发现 Docker build/start 必然失败、Dashboard process health 依赖 API/DB、无界 restart/request/log loop、resource gate 绕过、Dashboard-only 更新重建 core services、release 覆盖 `data/`/远端 `.env`、rollback 伪 PASS 或 port `3001` 冲突绕过的 Reliability blocker。

本结论是静态 focused implementation review 结论，不是 Docker build、Compose startup、Linux ARM64、Raspberry Pi、API/DB readiness 或 real Case A/B/C PASS。

## Recovery baseline

第一动作已完成 read-only recovery：

```text
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 683a8a0eb9f901dbc5c53c9bef5c4e68acf95ffb
origin/main: 683a8a0eb9f901dbc5c53c9bef5c4e68acf95ffb
latest: 683a8a0 Add PM handoff after Gate A closeout
ahead/behind: 0 0
cached diff: empty
target report before creation: absent
```

六文件状态符合任务预期：

```text
M  docker-compose.yml
M  docs/deployment/raspberry_pi.md
?? frontend/Dockerfile
?? frontend/.dockerignore
?? frontend/src/app/health/route.ts
?? frontend/src/app/health/__tests__/route.test.ts
```

tracked implementation diff 为 `docker-compose.yml` 与 `docs/deployment/raspberry_pi.md`；外部 tracked dirty 为 `M .gitignore`；protected implementation paths diff 为空；cached diff 为空。

## Scope

### Reviewed files

```text
frontend/Dockerfile
frontend/.dockerignore
frontend/src/app/health/route.ts
frontend/src/app/health/__tests__/route.test.ts
docker-compose.yml
docs/deployment/raspberry_pi.md
```

### Created report

```text
docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_reliability_implementation_review.md
```

### Explicitly not touched

```text
六个 implementation 文件未修改
frontend/package.json
frontend/package-lock.json
frontend/next.config.ts
frontend/tsconfig.json
frontend/src/lib/acceptedStationEvents/**
frontend/src/app/accepted-events/**
frontend/src/components/accepted-events/**
API / DB / Collector / Grafana / V-PLC
.gitignore 与既有 external/generated artifacts
```

按任务指定顺序读取了 authority 与 implementation files；未执行 Git write、Docker/Compose lifecycle、PostgreSQL、SSH、Raspberry Pi、browser/server runtime，未运行 `npm run typecheck` 或 `npm run build`。
## Implementation reliability matrix

### Dockerfile dependency/build/runtime

**PASS。** `frontend/Dockerfile:3,10,19` 使用 `node:22.23.0-bookworm-slim` 的 `deps` / `builder` / `runner` 三阶段；依赖层只复制 `package.json` 与 tracked `package-lock.json`，执行 `npm ci --no-audit --no-fund`（lines 6-8），没有 `npm install` 或 host `node_modules` authority。BuildKit cache 只挂载 npm cache，不改变 lockfile authority。

builder 从 dependency stage 复制 `node_modules`，执行 `mkdir -p public && npm run build`（lines 15-17），兼容当前缺少 `public/` 与未来静态资产。runner 只复制 `.next/standalone`、`.next/static` 与 `public`，不重新安装 dependencies，不复制完整 source、`.next/cache` 或 secret。runtime copy 使用 `--chown=node:node`，创建 `.next` 后设置 `USER node`，以 `node server.js` 启动并监听 `3000`。静态检查未发现 ownership、目录、standalone server path 或 runtime write 权限的必然失败风险；实际 Docker build/ARM64 run 未执行。

### `.dockerignore` context boundary

**PASS。** `frontend/.dockerignore:1-10` 排除 `.next`、`node_modules`、`tsconfig.tsbuildinfo`、`next-env.d.ts`、coverage、logs、`*.log`、`.git`、`.env` 与 `.env.*`，没有 negation 重新包含 secret 或 host build output，也没有排除 package files、Next config、TypeScript config、`src/`、`Dockerfile` 或未来 `public/`。

### Process-only health

**PASS。** `frontend/src/app/health/route.ts:1-9` 返回固定 JSON `{"status":"ok","service":"dashboard"}` 与明确 `200`，不读取 query、env、API origin，不调用 fetch，不访问 DB、accepted facts 或业务 filesystem。

允许的 focused test 已通过：

```text
npm test -- src/app/health/__tests__/route.test.ts
Test Files  1 passed (1)
Tests      1 passed (1)
```

`route.test.ts:11-23` 对 global `fetch` 设置有效 spy，注入异常 API env，断言精确 status、content type、shape、无额外字段及 fetch 未调用。

### Compose health/restart/dependency

**PASS。** `docker-compose.yml:92-120` 实现冻结语义：`context ./frontend`、`Dockerfile`、`edge-mes-dashboard:local`、`edge-mes-dashboard`、`restart: "on-failure:5"`、`3001:3000`、production env、`HOSTNAME=0.0.0.0`、`PORT=3000`、`EDGE_MES_DASHBOARD_API_ORIGIN=http://api:8000`、`EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=container` 与 `depends_on api: service_started`。

healthcheck 是 runner 内可执行的 `CMD node -e`，使用 Node 22 global `fetch`，只请求 `http://127.0.0.1:3000/health`；不访问 API、DB 或 accepted facts。Dashboard 没有 source、`.next`、`node_modules`、`data`、`.env` 或 Docker socket mounts，也没有 custom/host network、privileged 或额外 capabilities；其他 services 未被本次实现修改。

### Bounded startup terminal gate

**PASS。** `docs/deployment/raspberry_pi.md:659-696` 定义最多 120 秒的 bounded healthy window，观察 `RestartCount`、状态、health 与 bounded `--tail` 日志；超过 5 次 restart、持续 `restarting`/`unhealthy`、120 秒未 healthy 或持续 crash/log/request-retry storm 时执行 `docker compose stop dashboard`，并要求证明 Dashboard 不再处于 `running`、`restarting` 或持续 `unhealthy`。

这与 `on-failure:5`、local-only healthcheck 和 API failure 不触发 process restart 一致。建议后续将“超过 5 次”进一步明确为与 `RestartCount`/最多 5 次 restart attempt 一致的 `>= 5` 终局措辞，避免 off-by-one 解释；当前仍有 fail-closed terminal path。

### API failure / no stale / no retry

**PASS。** Gate B 未修改 accepted-events consumer business files。既有 `apiClient.ts` 使用 `response.text()` 与 strict parser，单次 `GET`、`no-store`、不 retry、不 fallback；transport/503/其他 malformed 结果由 page fail closed，不保留旧 production truth。部署文档明确 API 未 ready/停止时 Dashboard process health 仍独立，恢复由新的 page request 触发；Compose healthcheck 不会把 API failure 变成 Dashboard restart。
### Port `3001` preflight

**PASS WITH RECOMMENDATIONS。** `docs/deployment/raspberry_pi.md:471-505` 使用 bounded `ss -ltnp` 记录 listener，并按实际可用性检查 `nft`、`ufw`、`iptables`，不假设工具全部存在。发现 `3001` listener 或无法确认 listener/firewall 边界均为 `HOLD`，不得停止未知 listener 或改用其他 port；Grafana `3000` 保持不变。

建议增加专门记录首次取消后 `3001` listener 的 command/result 模板；当前 HOLD 与不绕过边界已足够，不构成 blocker。

### Resource preflight

**PASS。** `docs/deployment/raspberry_pi.md:507-579` 要求 build 前记录 `DockerRootDir`、`docker system df`、`docker builder du`、current/rollback image ID/size、`/opt/edge-mes-demo` 与 Docker root filesystem free、memory 与 Swap，并进行间隔 30 秒的两个 Swap samples。

门禁为相关 filesystem 至少 `6 GiB` free；存在 rollback image 时为 `max(6 GiB, 2 × rollback image size + 3 GiB)`；required metric 不能读、Swap 两次 sample 持续增长或 rollback assets 缺失时 `HOLD`。没有“资源不足但先 build 看看”或 auto-prune bypass。

### Build failure

**PASS。** `docs/deployment/raspberry_pi.md:581-610` 覆盖 build failure、timeout、OOM kill 与 incomplete image。任一失败后不得 `docker compose up`，不得使用 host `node_modules`/`.next`/macOS artifacts，不得换 Node image、改变 origin/profile、取消 non-root 或自动 prune/删除 rollback image。

### Resource postflight

**PASS WITH RECOMMENDATIONS。** build 后、启动前重新记录同一资源组，并要求 free space 至少 `3 GiB`、new image + BuildKit cache growth `<= 3 GiB`、Dashboard image `<= 1 GiB`、120 秒后 Swap 增量 `<= 256 MiB`，以及两个间隔 30 秒的 post samples 不继续增长；任一失败即不启动、保留旧 assets、`HOLD`。

建议后续把 `docker system df`/`docker builder du` baseline 与单位统一为 bytes，并给出 image size 与 BuildKit cache 增量的逐项算式；当前已有 pre/post record、冻结阈值、required-metric HOLD 与禁止 cleanup bypass，未形成 blocker。

### Dashboard-only update

**PASS。** `docs/deployment/raspberry_pi.md:629-657` 将唯一更新命令冻结为：

```bash
docker compose up -d --build --no-deps dashboard
```

同时明确全量 `docker compose up -d --build` 与 `docker compose down` 不是 Dashboard-only update，并禁止主动重建或重启 API、PostgreSQL、Collector、Grafana、V-PLC、Simulator、Prometheus 或其他 core services；不删除 volume，不 reset data 或远端 `.env`。

### Release transport

**PASS。** `docs/deployment/raspberry_pi.md:420-453` 精确列出本 Gate 六个 changed paths，并明确它们只是 changed-file scope，不是完整可部署 release 文件全集；远端仍需已有 tracked frontend baseline，包括 `package.json`、`package-lock.json`、`next.config.ts`、`tsconfig.json` 与 `src/`。

发布保护明确排除 `data/`、远端 `.env`、`.git/`、`frontend/node_modules/`、`frontend/.next/`、generated TypeScript files、`__pycache__/` 与 `*.pyc`，禁止 destructive sync 覆盖 data 或 `.env`。没有提供会删除/覆盖这些路径的 release command。

### Previous Dashboard rollback

**PASS WITH RECOMMENDATIONS。** `docs/deployment/raspberry_pi.md:700-726` 要求在 build 前确认 source release ID/commit、旧 release files、old image tag/ID、resolved Compose baseline 与 service/container baseline；缺失 required asset 或 post-rollback evidence 即 `HOLD`。恢复旧 `edge-mes-dashboard:local` 后使用 `--no-deps --force-recreate` 启动，仅影响 Dashboard，验证 `/health`、一次 bounded accepted-events request、core service non-rebuild 与 `data/`/远端 `.env` 不变；禁止 `down`、volume delete、image prune 与其他 service rebuild。

建议把 bounded accepted-events request 的精确 URL/result record 模板补入文档，避免 rollback 只保留页面截图而没有 bounded request evidence；现有要求已经明确该 evidence 是 PASS 前提，未形成 blocker。

### First-deployment cancellation

**PASS。** 文档将无旧 Dashboard 路径命名为 `first-deployment cancellation / existing-core-services non-impact validation`，不称为 Dashboard rollback。失败后仅 stop/rm Dashboard，恢复 pre-deployment Compose/release files，执行 `docker compose config --quiet`，并要求无 `edge-mes-dashboard` container、`3001` listener 已释放、core service/container/image baseline 与 health 不变、API/PostgreSQL/Collector/Grafana/V-PLC 未重建、`data/` 与远端 `.env` 未覆盖。明确禁止声明 Dashboard rollback、`/health` 或 accepted-events page PASS。

### Real Case A/B/C bounded execution

**PASS。** 文档保持 Case A/B mandatory、Case C conditional；真实 Case C 不存在时只写 `NOT AVAILABLE / NOT VERIFIED`，不得用 mock/synthetic/API-only/Case B/cycle event 替代。每个 case 是独立 bounded request，目标必须为 API `items[0]`，并保存 `production_accepted_station_event_fact` raw row、API exact 22-field raw JSON、Dashboard display rule/value 与 `fact_key` 等 identity；不扫描无界历史，不形成 polling/retry storm。Case evidence 仍须在 resource/startup terminal gates 后、经独立 runtime authorization 执行；`/health` 不能替代 case evidence。
## Manual Compose validation evidence

以下为 PM 提供的人工前序证据，本 review 未重新运行：

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
docker compose config --quiet
echo $?
```

结果：

```text
no error output
exit code: 0
```

该证据仅证明当前 `docker-compose.yml` 可被 Docker Compose v2 静态解析；不证明 Docker build、Compose startup、Dashboard runtime、Linux ARM64、Raspberry Pi、API/DB readiness 或 real Case A/B/C。

## Blockers

```text
none
```

未发现：Dockerfile 必然 build/start failure、runner healthcheck 不可执行、health 依赖 API/DB/fact、restart/等待无界或失败后不 terminal stop、API failure 触发 Dashboard process restart、resource metric 不可读仍允许继续、build failure 后仍可 up、release 覆盖 data/.env、Dashboard-only 命令重建 core services、rollback assets 在 deploy 后才确认、first deployment 被错误声明为 rollback PASS、失败 container 或 3001 listener 必然残留、必须修改六文件外路径、live Git/allowlist/protected paths 冲突。

## Recommendations

1. 后续 deployment/operator 文档可将 restart 终局写成 `RestartCount >= 5`，明确 Docker `on-failure:5` 的 restart-attempt 语义，避免 off-by-one。
2. 为 rollback 的 bounded accepted-events request、first-deployment cancellation 后的 `3001` listener、core baseline compare 增加固定 command/result record 模板。
3. 将 image/cache pre/post 记录统一为 bytes，并列出 BuildKit cache 与 image growth 的可复核算式；保留当前 `HOLD` 与 no-auto-prune 边界。
4. 后续 runtime gate 记录 `node:22.23.0-bookworm-slim` resolved digest、最终 image ID/size、native `linux/arm64/v8` build/run、120 秒 healthy 终局与实际 `RestartCount`。
5. 既有通用运维 Sections 2/3/6 仍保留 full-stack `up`/`down` 命令；Gate B Section 10.7 已明确它们不是 Dashboard-only path。后续可继续强化 operator warning，但当前语义边界已足够防止将其解释为本 Gate 的启动命令。

## Authorization boundary

```text
no implementation edits
no Docker build/start
no Compose startup
no API/DB/PostgreSQL/SSH/Pi/browser/server runtime
no real Case A/B/C
no Git add/commit/push/tag/restore/reset/clean
```

实际执行的仅是用户允许的 health focused test 与六文件 `git diff --check`；未将其解释为 Docker、ARM64、Pi 或 production closure。

## Git status

### Six-file implementation diff

```text
M  docker-compose.yml
M  docs/deployment/raspberry_pi.md
?? frontend/Dockerfile
?? frontend/.dockerignore
?? frontend/src/app/health/route.ts
?? frontend/src/app/health/__tests__/route.test.ts
```

### Cached diff

```text
empty
```

### External/generated artifacts

保留且未触碰：

```text
M .gitignore
旧 PM handoff 文件与其余 handoff artifacts
docs/reports/phase1_to_sprint2_management_keynote_10p.html
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_*.md
docs/reports/sprint3_db_backed_api_validation_reliability_review.md
docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_verification_review.md
frontend/.next/
frontend/node_modules/
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
```

### Report-only change

```text
?? docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_reliability_implementation_review.md
```

除本报告外没有产生新文件；没有 stage、commit、push、restore、reset 或 clean。

## Next gate

```text
PM intake
Data Quality focused implementation review eligible
```

本报告不授权 Data Quality 之外的 runtime、Docker/Compose、Pi、real Case A/B/C、deploy、rollback 或 Git write。Data Quality review 仍应保持独立 scope，不修改本 Reliability review 的六文件结论或扩大到 consumer 业务文件。

## Thread output / context assessment

```text
本次输出长度：长
当前 Thread 是否建议继续：no
下一轮是否建议新开 Thread：yes
理由：Reliability focused implementation review 已闭合；下一步是独立 Data Quality focused implementation review，应保持 review lane 隔离并避免把 static PASS WITH RECOMMENDATIONS 误带入 Docker/Pi/runtime authorization。
```
