# Sprint 3 Dashboard Raspberry Pi Docker Integration Reliability Review

报告名称：`Sprint 3 Dashboard Raspberry Pi Docker Integration Reliability Review`

任务名称：`Accepted-events Dashboard 树莓派 Docker 集成 Reliability Planning Review`

执行 Thread：`Reliability`

日期：`2026-07-14`

## 1. 结论

**HOLD**

本轮为 docs-only Reliability planning review。Architecture plan 的 Option A、
Next standalone 方向、`container` origin、Dashboard process health 与现有
accepted-events fail-closed client 边界基本一致，但当前计划仍缺少三个会影响
部署安全闭环的 Reliability invariant。不得进入 implementation、Data Quality、
Verification 或 Raspberry Pi runtime gate，直到 Architecture 完成下列最小修复
并重新提交 Reliability planning re-review。

本报告没有修改 Architecture plan、Compose、实现代码、部署文档或既有 dirty
artifacts。

## 2. Recovery baseline

read-only recovery 结果：

```text
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: bdda24fd930339b565d0c1894daece42c6039ac7
origin/main: bdda24fd930339b565d0c1894daece42c6039ac7
ahead/behind: 0 0
latest: bdda24f Reset Dashboard URL validation scope
cached diff: empty
tracked diff: .gitignore only
target report before this write: absent
```

已存在的 untracked/dirty artifacts 被视为外部 artifacts 并保持不动，包括旧
Dashboard runtime-evidence reports、PM handoff files、Keynote/reporting artifact、
`frontend/node_modules/` 与 `frontend/tsconfig.tsbuildinfo`。本轮没有整理、删除、
覆盖、stage、commit 或 push。

## 3. Review scope and evidence

已读取用户指定的 PM rules、current status、Architecture plan、scope-reset design
与 execution report、Dashboard API contract、Raspberry Pi deployment guide、现有
Compose、frontend package/lock/config/origin/client/page 以及 API health route。

本轮未运行 tests、typecheck、build、Docker/Docker Compose、PostgreSQL、SSH、
Raspberry Pi、browser/server runtime 或任何 deployment/rollback action。

静态确认的安全边界：

- `frontend/next.config.ts` 已固定 `output: "standalone"`；
  `frontend/package-lock.json` 为 tracked `lockfileVersion: 3`，Next `16.2.10`
  要求 Node `>=20.9.0`，lockfile 包含 Linux ARM64 SWC optional packages。
- Plan 的 `node:22.23.0-bookworm-slim`、native ARM64 build、`npm ci`、runtime-only
  server env 与 `.dockerignore` 方向合理；没有把 `localhost` 或临时 origin 作为
  build 默认值的授权。
- 现有 `api/app/routes/health.py` 执行 PostgreSQL `SELECT 1`，不能复用为
  Dashboard process health。Plan 新增独立 `/health` 且禁止 API/DB/fact access 的
  方向正确。
- 现有 client 使用 absolute accepted-events GET、`cache: "no-store"`、不 retry、
  不 fallback；page 的 query validation 在 origin resolver/request 前执行，失败
  不构造 production view model。
- 现有 Compose 的 Grafana host port `3000` 与计划的 Dashboard `3001:3000`
  不冲突；`api` service DNS 与 `http://api:8000` 的 container profile 一致。
- Plan 的 `depends_on: api: condition: service_started` 被正确限定为启动顺序，
  没有把 container running/healthy 或 Compose startup 当作 API/DB closed-loop
  PASS。

## 4. Reliability blockers

### `REL-DASH-R1`：restart policy 未定义 crash-loop / log-loop 的 fail-closed 约束

证据：Architecture plan Section 8 的 proposed `dashboard` service 使用
`restart: unless-stopped`；Section 18 只把 container/Compose restart 列为后续
review 项，没有冻结启动失败后的最大重启次数、backoff、人工停机条件或日志风暴
停止条件。`unless-stopped` 对进程级启动失败可能持续重启，形成持续 crash loop 和
日志消耗；这与本 Gate 要求的“不得形成持续 crash loop、请求风暴或日志风暴”不相容。

最小 Architecture repair：只修复 plan 的 Sections 8、13、18/19，冻结一个可
验证的 bounded restart/backoff/stop policy，并明确：

- startup failure 在达到边界后保持 stopped/明确失败，不继续无限重启；
- healthcheck 只访问本地 Dashboard `/health`，不得因 API failure 触发请求重试；
- page render 仍保持同一次 render 一次 request、恢复只由新的 page request 触发；
- implementation 与 deployment evidence 必须能观察到 bounded restart outcome。

不得借此扩展 API、Compose 其他 service、通用故障注入或监控平台。

### `REL-DASH-R2`：首次部署失败的 rollback 闭环缺少 Dashboard health/request 验证

证据：Plan Section 15.2 对 subsequent Dashboard update rollback 要求恢复 image、
`docker compose up -d --no-deps --force-recreate dashboard`、验证 Dashboard
`/health`，再执行一次 bounded accepted-events query；但 Section 15.3 的 first
deployment rollback 只执行 `docker compose rm -sf dashboard`、恢复 Compose/release
files 与 `docker compose config --quiet`，没有 rollback 后的 Dashboard health 和
bounded accepted-events request 验证。`docker compose config --quiet` 不能替代这
两项验证。

最小 Architecture repair：只修复 Section 15.3，明确 first-deployment failure 的
可恢复资产、rollback 类型与终局证据：

- 若存在可恢复的上一版 Dashboard release/image，必须复用 Section 15.2 的
  health + 一次 bounded accepted-events request 证据；
- 若确实没有上一版 Dashboard，必须把该路径明确标记为“取消本次新增 service、
  不产生 Dashboard rollback PASS”，并定义所需的 existing-core-services
  non-impact proof；不能用删除 service 后的 `config --quiet` 宣称 rollback
  closure；
- 任一 required rollback asset 或 required post-rollback evidence 缺失时保持
  `HOLD`，不得部署。

该修复不得引入 `docker compose down`，不得覆盖/删除 `data/`、远端 `.env` 或
其他服务。

### `REL-DASH-R3`：资源/磁盘/Swap/BuildKit cache 只有记录项，没有停止条件

证据：Plan Sections 11.5、14、19 要求记录 `docker system df`、image size、
filesystem free space、Swap 与 cache growth，但没有冻结“磁盘不足、Swap 异常增长、
BuildKit cache 失控或 image build failure 时立即停止”的可执行 gate。将这些事实
仅作为 baseline/recommendation，无法保证 build/deploy 在资源风险下 fail closed。

最小 Architecture repair：只修复 Plan Sections 11.5、14、19，并同步到未来允许
修改的 `docs/deployment/raspberry_pi.md`，明确 preflight/build/postflight 顺序：

- build 前记录并检查 free space、Swap、Docker disk usage、现有/rollback image
  与 BuildKit cache；任一不可用或超过 PM 冻结的 measurable bound，立即 `HOLD`，
  不 build、不 deploy；
- image build 失败是 terminal stop，不得自动换用 host `node_modules`、host
  `.next`、localhost origin、临时 origin 或错误 profile；
- build 后再次记录同一组指标；cache/image/disk 变化超过冻结边界时停止并保留
  rollback asset；
- 不自动运行 `docker system prune`、`docker builder prune` 或删除 rollback image。

该修复只涉及 Dashboard build/deployment safety，不打开容量测试或通用资源平台。

## 5. Non-blocking carry-forward recommendations

以下项目不阻断本轮之外的 Architecture repair，但必须传递给后续 gate：

- **Verification：** 对 `node:22.23.0-bookworm-slim` 记录 resolved manifest/image
  digest；在真实 Pi 上分别证明 native ARM64 build、startup、Dashboard `/health`、
  API 未 ready 窗口、API stop/recovery、single-request 与 no-stale transitions。
- **Verification：** 固定 healthcheck `interval: 10s`、`timeout: 3s`、`retries: 10`、
  `start_period: 20s` 的启动证据，并确认 health route 只产生固定响应、不触发
  API/DB/fact access。
- **Data Quality：** 继续核对唯一事实源
  `production_accepted_station_event_fact`、exact 22-key envelope、explicit
  `null`、NOK/detail accepted evidence binding，以及 malformed 2xx 不显示任何
  production surface；不得把本 Reliability PASS/HOLD 与 DB-backed fact closure
  混用。
- **Implementation：** `Dockerfile` 必须在未注入 production API origin 时完成
  build；runtime env 只由 Compose 注入
  `EDGE_MES_DASHBOARD_API_ORIGIN=http://api:8000` 与
  `EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=container`；不得使用 `ARG`、
  `NEXT_PUBLIC_*`、host `node_modules`、host `.next`、host network、Docker socket、
  privileged 或业务数据 volume。
- **Implementation：** 更新 `docs/deployment/raspberry_pi.md` 时，必须把
  `docker compose up -d --build --no-deps dashboard` 作为 Dashboard-only update
  的唯一路径，并把现有通用 `docker compose up -d --build` / `docker compose down`
  明确隔离为非 Dashboard-only 操作，避免误触 API、PostgreSQL、Collector、Grafana、
  V-PLC 或数据目录。
- **Implementation/Verification：** rollback release ID、旧 release files、旧
  image tag/ID、resolved Compose config 与 container baseline 必须在新 build 前
  记录；缺一项即 `HOLD`。

## 6. Allowlist assessment

Architecture plan Section 17 的 proposed exact implementation allowlist **范围足够，
无当前缺漏**：

```text
CREATE frontend/Dockerfile
CREATE frontend/.dockerignore
CREATE frontend/src/app/health/route.ts
CREATE frontend/src/app/health/__tests__/route.test.ts
MODIFY docker-compose.yml
MODIFY docs/deployment/raspberry_pi.md
```

这六个路径足以承载 multi-stage standalone image、build-context 排除、独立
Dashboard `/health`、Compose runtime env/port/depends_on/healthcheck 与 Raspberry
Pi update/rollback/resource instructions。既有 `package.json`、tracked
`package-lock.json`、`next.config.ts`、`apiOrigin.ts`、`apiClient.ts`、`page.tsx`、
API、Collector、DB、Grafana、Node-RED、reverse proxy、TLS 均不应加入 allowlist。

但在 `REL-DASH-R1` 至 `REL-DASH-R3` 修复并经 Reliability re-review 前，该
allowlist 不能被 implementation 使用。

## 7. Next gate

```text
Current gate: Reliability planning review = HOLD
Required next action: Architecture repair of only REL-DASH-R1/R2/R3
Then: Reliability planning re-review
After Reliability closes: Data Quality planning review -> Verification planning review
Implementation: not authorized
Raspberry Pi / Docker / DB / browser runtime: not authorized
stage/commit/push/tag/deploy/rollback: not authorized
```

Architecture repair 不得修改本报告以外的本轮文件，且不得扩大到旧 Dashboard URL
runtime-evidence 强审计分支。

## 8. Thread output / context assessment

- 本次输出长度：中。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：本报告已完成一个独立 Level 2 deployment integration Reliability gate；
  下一轮应携带 `REL-DASH-R1`、`REL-DASH-R2`、`REL-DASH-R3` 的最小修复证据，继续
  与旧 Dashboard URL runtime-evidence review 历史隔离。
