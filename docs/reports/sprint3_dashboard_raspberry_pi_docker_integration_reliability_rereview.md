# Sprint 3 Dashboard Raspberry Pi Docker Integration Reliability Re-review

报告名称：`Sprint 3 Dashboard Raspberry Pi Docker Integration Reliability Re-review`

任务名称：`复验 REL-DASH-R1/R2/R3 Architecture HOLD Repair`

执行 Thread：`Reliability`

日期：`2026-07-14`

## 1. Conclusion

**PASS WITH RECOMMENDATIONS**

本轮只复验上一轮 Reliability HOLD 的 `REL-DASH-R1`、`REL-DASH-R2`、
`REL-DASH-R3`。Architecture plan 已补齐三项 blocker 所要求的可执行终局条件，
没有发现新的 Reliability blocker。该结论是 planning closure，不是 Raspberry Pi、
Docker、真实 accepted-fact 或 DB-backed runtime PASS。

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
target rereview report before this write: absent
```

既有 untracked/dirty artifacts（包括上一轮 Reliability report、Architecture plan、
PM handoff、旧 runtime-evidence reports、`frontend/node_modules/` 与
`frontend/tsconfig.tsbuildinfo`）均保持不动。本轮未 stage、commit、push 或整理
任何 dirty artifact。

## 3. Scope and execution boundary

已读取：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_plan.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_reliability_review.md`
- `docs/deployment/raspberry_pi.md`
- `docker-compose.yml`

本轮未运行 tests、typecheck、build、Docker/Docker Compose、PostgreSQL、SSH、
Raspberry Pi、browser/server runtime、deployment 或 rollback。

未重新审查已通过且未被本次修复触碰的完整 Architecture 设计；未打开旧
Dashboard URL runtime-evidence 强审计分支。

## 4. REL-DASH-R1 status

**`REL-DASH-R1 CLOSED`**

Architecture plan Sections 8、13、18 已冻结：

- Dashboard 独立使用 `restart: "on-failure:5"`，不修改其他 Compose services；
- build/up 后最多等待 120 秒进入 `healthy`；超过 5 次 process restart、持续
  `restarting`、持续 `unhealthy` 或 120 秒未 healthy 时终止部署；
- 失败后显式执行 `docker compose stop dashboard`，不允许无限重启；
- `unhealthy` 不会自动触发 rollback，部署侧显式观察并停止；
- healthcheck 只访问 `http://127.0.0.1:3000/health`，API failure 不导致
  Dashboard process restart；
- 同一次 page render 最多一次 API request，API 恢复只由新的 page request 触发；
- 日志只能使用 bounded `--tail` 或 bounded time window；
- Verification 后续可观察 `RestartCount`、120 秒终局、stopped 状态及无
  request/retry/log storm。

因此，上一轮关于无限 crash-loop、healthcheck 误触发 restart 和 request/log storm
的 blocker 已关闭。实际 restart evidence 仍属于后续 runtime/Verification gate。

## 5. REL-DASH-R2 status

**`REL-DASH-R2 CLOSED`**

Architecture plan Section 15.3 已精确区分两条路径：

### 远端已有上一版 Dashboard

必须先具备 source release ID、旧 release files、旧 image identity/tag、resolved
Compose baseline 与 service/container baseline；恢复旧 Dashboard 后必须验证：

- Dashboard `/health`；
- 一次 bounded accepted-events request；
- API、PostgreSQL、Collector、V-PLC 与 `data/` 未被重建或覆盖。

缺少 required asset 或 required evidence 时保持 `HOLD`。

### 首次新增且无上一版 Dashboard

路径被定义为：

```text
first-deployment cancellation / existing-core-services non-impact validation
```

该路径只停止并移除 Dashboard，恢复部署前 Compose/release files，验证 Compose
config、Dashboard container 不存在、host port `3001` 不监听、现有 core services
health 与 service/container/image non-impact，并确认 `data/` 与远端 `.env` 未被
删除或覆盖。

该路径明确不产生 Dashboard rollback PASS，不伪造 Dashboard `/health` 或
accepted-events page PASS。两条路径均禁止 `docker compose down`、volume delete、
image prune、data restore、DB rollback 与其他 service rebuild。

因此，上一轮关于首次部署 rollback 语义与验证缺口的 blocker 已关闭。

## 6. REL-DASH-R3 status

**`REL-DASH-R3 CLOSED`**

Architecture plan Sections 14.1、14.2、14.3 已冻结可执行、fail-closed 的首版
资源门禁：

- build 前记录 Docker root、项目 filesystem、Docker disk usage、BuildKit cache、
  image identity/size、memory 与 Swap；required metric 无法读取即 `HOLD`；
- preflight filesystem free space 至少 `6 GiB`；已有 rollback image 时使用
  `max(6 GiB, 2 × rollback image size + 3 GiB)`；两次间隔 30 秒的 Swap sample
  持续增长即 `HOLD`；
- build failure、timeout、OOM 或 incomplete image 立即停止，不继续 `up`；不得
  使用 host `node_modules`、host `.next`、macOS artifact、localhost/temporary
  origin、错误 profile、不同 Node image 或取消 non-root boundary；
- 不自动执行 `docker system prune`、`docker builder prune`，不删除 rollback image；
- deploy 前 postflight 要求 filesystem free space 至少 `3 GiB`、image + BuildKit
  cache 增长不超过 `3 GiB`、Dashboard image 不超过 `1 GiB`、Swap 相对 baseline
  不增加超过 `256 MiB`，且两次间隔 30 秒的 Swap sample 不增长；
- 任一 postflight 失败均不得启动 Dashboard，必须保留 rollback assets 并报告
  `HOLD`。

因此，上一轮关于资源记录没有 stop gate 的 blocker 已关闭。实际 Pi 指标采集仍未
执行，必须由后续 runtime gate 完成。

## 7. Allowlist assessment

Proposed implementation allowlist 仍然足够且无新增缺漏：

```text
CREATE frontend/Dockerfile
CREATE frontend/.dockerignore
CREATE frontend/src/app/health/route.ts
CREATE frontend/src/app/health/__tests__/route.test.ts
MODIFY docker-compose.yml
MODIFY docs/deployment/raspberry_pi.md
```

R1/R2/R3 的实现承载均可在这六个路径内完成。不得加入 API、Collector、DB、
Grafana、Node-RED、reverse proxy、TLS 或其他 frontend 业务文件。

当前 `docs/deployment/raspberry_pi.md` 仍保留通用 `docker compose up -d --build`、
`docker compose down` 等旧运维命令；这是 implementation 阶段在既有 allowlist 内
同步 Dashboard-only、rollback/cancellation、资源 stop gate 的 carry-forward，
不是本轮 planning blocker。当前未修改该文件。

## 8. Carry-forward recommendations

- **Verification：** 在 PM 单独授权后验证 native ARM64 build/run、120 秒 healthy
  终局、`RestartCount`、显式 stopped 状态、bounded logs、no request/retry storm、
  6/3 GiB、1 GiB、256 MiB 与双样本 Swap 门禁。
- **Implementation：** 将本报告已关闭的 R1/R2/R3 条件同步进
  `docs/deployment/raspberry_pi.md`；Dashboard-only update 必须使用
  `docker compose up -d --build --no-deps dashboard`，不得误用全量 `up` 或
  `down` 影响核心服务。
- **Data Quality：** 下一 gate 独立核对
  `production_accepted_station_event_fact`、exact 22-key envelope、NOK/detail
  accepted evidence binding 与 real/synthetic evidence claim；不得把本 planning
  closure 当作 DB-backed fact closure。
- **Runtime：** 仍未授权连接 PostgreSQL、树莓派或执行 Docker/Compose；所有
  rollback asset/evidence 缺失路径继续保持 `HOLD`。

## 9. Next gate

```text
Current gate: Reliability planning re-review = PASS WITH RECOMMENDATIONS
REL-DASH-R1: CLOSED
REL-DASH-R2: CLOSED
REL-DASH-R3: CLOSED
Next eligible gate: PM-arranged Data Quality planning review
Implementation / Verification / Raspberry Pi runtime: not authorized by this report
stage/commit/push/tag/deploy/rollback: not authorized
```

本轮结束，不进入 Data Quality、Verification、implementation 或 runtime。

## 10. Thread output / context assessment

- 本次输出长度：中。
- 当前 Thread 是否建议继续：yes，可承接 PM 安排的下一独立 planning review。
- 下一轮是否建议新开 Thread：no。
- 理由：本轮只复验上一轮三个 blocker，范围已闭合，继续当前 Thread 不会扩大到
  旧 URL runtime-evidence 分支。
