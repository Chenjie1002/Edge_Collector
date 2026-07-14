# Sprint 3 Accepted-events Dashboard Raspberry Pi Docker Integration Plan

## 1. Report name / task / executing Thread

- Report name: `Sprint 3 Accepted-events Dashboard Raspberry Pi Docker Integration Plan`
- Task: 为 accepted-events Next Dashboard 制定 Raspberry Pi Docker / Compose 集成与真实 accepted-fact 闭环验收方案；Gate A Consumer Truth Hardening 已关闭，当前恢复 Gate B 部署规划 authority
- Executing Thread: `Architecture / Integration`
- Date: `2026-07-14`
- Planning conclusion: **PASS WITH RECOMMENDATIONS — Gate A CLOSED; Gate B planning authority retained**
- Data Quality state: **`DQ-DASH-D1/D2/D3` CLOSED**；Gate A Architecture、Reliability、Data Quality、Verification focused implementation reviews 均无 blocker
- Authorization state: Gate A implementation 已提交并 push 于 `a3cf64de31bf5eb12a1aa3eeed52aa3a451b8e79`；Gate B implementation、Docker、Raspberry Pi runtime、deploy/rollback 尚未授权

## 2. Recovery evidence

第一动作按 PM 指令完成 read-only recovery，实际结果：

```text
branch: main
HEAD:        bdda24fd930339b565d0c1894daece42c6039ac7
origin/main: bdda24fd930339b565d0c1894daece42c6039ac7
latest:      bdda24f Reset Dashboard URL validation scope
ahead/behind: 0 0
cached diff: empty
tracked diff: .gitignore only
```

外部既有 dirty artifacts 包括 `.gitignore`、旧 Dashboard runtime-evidence review/report、旧 PM handoff、`docs/reports/phase1_to_sprint2_management_keynote_10p.html`、`frontend/node_modules/` 和 `frontend/tsconfig.tsbuildinfo`。本任务未删除、修改、stage 或纳入这些文件。

本次只读取 authority 与实现事实；未运行 tests、typecheck、build、Docker、DB、SSH、Raspberry Pi、stage、commit 或 push。

## 3. Current implementation facts

### 3.1 Frontend / Next

- `frontend/package.json` 固定 `next: 16.2.10`、`react: 19.2.7`、`react-dom: 19.2.7`。
- `frontend/package-lock.json` 存在、已 tracked、`lockfileVersion: 3`，是 dependency install authority；Docker build 必须使用 `npm ci`，不得改用无 lockfile install。
- lockfile 中 Next `16.2.10` 要求 Node `>=20.9.0`，并包含 Linux ARM64 glibc 与 musl SWC optional packages。
- `frontend/next.config.ts` 已冻结 `output: "standalone"`。
- 当前不存在 `frontend/Dockerfile`、`frontend/.dockerignore`、`frontend/public/` 或可供复制的 `.next/`；planning 不生成 `.next`。
- Next 官方 standalone 产物为 `.next/standalone` 加最小 `server.js`；`public` 与 `.next/static` 不会自动进入 standalone，必须显式复制。参考：[Next.js output documentation](https://nextjs.org/docs/app/api-reference/config/next-config-js/output) 与 [official with-docker example](https://github.com/vercel/next.js/tree/canary/examples/with-docker)。

### 3.2 Trusted origin / client / page

- `container` profile 只接受 canonical `http://api:8000` 或尾随 `/` 版本，并规范化为 `http://api:8000`。
- query 在 resolver 与 request 之前验证；invalid query 不调用 resolver、不发请求。
- accepted-events client 只构造 absolute `GET /api/v2/production/accepted-station-events`，使用 `cache: "no-store"`、`credentials: "omit"`、`redirect: "error"`。
- client 不 retry、不 fallback；2xx response 必须通过 exact-envelope / exact-22-key strict parser。
- Gate A 已将成功2xx runtime路径修复为 `response.text()` -> source-preserving `JSON.parse` reviver `context.source` -> exact typed/cross-field parser；`response.json()` source-loss seam 已关闭并提交于 `a3cf64d`。
- 4xx 映射为 `invalid-query`，503 映射为 `unavailable`，其他 5xx、transport error 与 malformed 2xx 映射为 `error`；均不得显示 production surfaces。
- 页面是 dynamic Server Component。浏览器只访问 Dashboard；server-side request 才访问内部 service DNS `api`。
- 现有 UI 可显示目标 fact 的 table row、Trace references 与 NOK/detail evidence。由于 detail panel 固定选择当前 page 第一项，三层对账时必须用 bounded query / cursor 让目标 fact 成为 API response 第一项。

### 3.3 API / Compose / deployment

- accepted-events API 已注册于 FastAPI，唯一事实表为 `production_accepted_station_event_fact`，返回 exact `data/items` 与 `page` envelope。
- API `/health` 会执行 PostgreSQL `SELECT 1`，所以它证明 API + DB，而不是 Dashboard process readiness。
- Compose 当前服务均使用隐式 default project network，未定义自定义 `networks`；service name `api` 可在该网络内解析。
- 当前固定 `container_name` 模式为 `edge-mes-*`；`api` 为 `edge-mes-api`，host/container port 为 `8000:8000`。
- Grafana 已占用 `3000:3000`；仓库中没有 host port `3001` 冲突。
- 当前仅 PostgreSQL 有 Compose healthcheck；API 没有 healthcheck。
- 所有现有服务使用 `restart: unless-stopped`。
- Raspberry Pi 部署目录 authority 为 `/opt/edge-mes-demo`；`data/`、远端 `.env`、`.git`、本地 `node_modules` 与生成物不得被发布覆盖。

## 4. Scope and non-goals

### In scope

- 一个独立 `dashboard` Docker image 与 Compose service 的未来实现设计。
- 浏览器 `http://<Raspberry-Pi-IP>:3001` 到 Dashboard，再由 Dashboard server-side 请求 `http://api:8000` 的固定拓扑。
- Dashboard process health、Pi 更新/回滚、真实 accepted-fact 三层对账、failure/recovery 与资源基线。

### Non-goals

- Lucky、反向代理、域名、TLS、公网访问、用户认证、权限系统、Kubernetes。
- 新 DB schema、accepted fact contract、API endpoint、Dashboard 业务功能。
- Collector、V-PLC、Grafana、Node-RED、多产线容量测试。
- 通用强审计取证框架；本计划只保留会影响 false PASS、stale truth、容器可启动性、ARM64、网络/端口、数据安全、rollback 或真实/合成证据边界的 gate。

## 5. Three architecture options

| Option | Design | Advantages | Costs / risks | Decision |
| --- | --- | --- | --- | --- |
| A | 在现有 `docker-compose.yml` 新增 `dashboard`，使用 `frontend/Dockerfile` | 单一运维入口；自动加入现有 default network；可直接使用 `api:8000`；符合当前 Pi 运维方式 | Compose 文件增加一个服务；更新时必须确保只重建 dashboard | **Recommended** |
| B | 新增 `docker-compose.dashboard.yml` overlay | frontend 变更可单独开关；文件级隔离较强 | 每条 config/up/rollback 命令都要同时带两个 compose 文件；project/network/container naming 更易漂移；远端操作复杂 | Not recommended for v1 |
| C | Dashboard 不容器化，由 host systemd 运行 | 少一层 container；可直接使用 host Node | 破坏单一 Compose 运维模型；需要 host Node/npm、独立日志/用户/升级/rollback；`api` service DNS 在 host 不可用；更易误用 localhost | Rejected |

Option A 最符合现有单机 Compose authority，并保持 Dashboard 与 API 在同一项目网络内。Option B 只在未来出现独立发布节奏或独立 Compose ownership 时重新评估；Option C 仅作对比。

## 6. Recommended topology

冻结首版拓扑：

```text
browser
  -> http://<Raspberry-Pi-IP>:3001
  -> edge-mes-dashboard (container port 3000)
  -> trusted resolver: container / http://api:8000
  -> edge-mes-api (service api, container port 8000)
  -> PostgreSQL
```

冻结端口：

```text
Dashboard: host 3001 -> container 3000
Grafana:   host 3000 -> container 3000 (unchanged)
API:       host 8000 -> container 8000 (unchanged)
```

不新增 custom network。`dashboard`、`api` 与 `postgres` 继续加入 Compose 自动创建的 default project network；browser 不解析或访问 `api` service name。

## 7. Frontend Docker image design

### 7.1 Image strategy decision

| Image option | Assessment | Decision |
| --- | --- | --- |
| A. Single-stage Node image | 会把完整 dev dependencies、source 与 build cache 留在 runtime image，攻击面与磁盘占用较大 | Reject |
| B. Multi-stage build + standalone runtime | `npm ci` 与 build 可复现；runtime 只含 traced dependencies、static/public 与 server | **Select** |
| C. Host build then copy `.next` | 本地 macOS/CPU 与 Pi Linux ARM64 不同；会绕开 containerized dependency authority，并容易复制 dirty/generated artifacts | Reject |

### 7.2 Frozen build/runtime design

- Base image: `node:22.23.0-bookworm-slim` for `deps`、`builder`、`runner`。
- Rationale: 满足 Next `>=20.9.0`，使用 Debian glibc，与 lockfile 的 `@next/swc-linux-arm64-gnu` 对齐；Docker Official Image 已提供 `linux/arm64/v8`。参考：[Node official image tags](https://hub.docker.com/_/node/tags?name=22.23.0-bookworm-slim)。
- Architecture: Pi 上 native `linux/arm64/v8` build 是首版 authority；本轮不引入 buildx/QEMU cross-build。
- Dependency stage: 先复制 `package.json` 与 tracked `package-lock.json`，执行 `npm ci --no-audit --no-fund`。
- Cache: 使用 BuildKit npm cache mount；源码变化不使 dependency layer 无条件失效。`.next/cache` 不进入 runtime image。
- Builder: 从 dependency stage 复制 `node_modules`，再复制被 `.dockerignore` 约束的 frontend source，执行 `mkdir -p public` 后 `npm run build`。
- `mkdir -p public` 是必要设计：当前仓库没有 `frontend/public/`，但 runtime copy 必须同时兼容“当前为空”和“未来有静态资产”。
- Runner copy:
  - `/app/.next/standalone` -> `/app`
  - `/app/.next/static` -> `/app/.next/static`
  - `/app/public` -> `/app/public`
- Runtime user: 使用 image 内置 non-root `node`，所有 runtime files 使用 `--chown=node:node`；为 `.next` 创建 node-owned 目录以容纳 Next runtime cache。
- Runtime env: `NODE_ENV=production`、`NEXT_TELEMETRY_DISABLED=1`、`HOSTNAME=0.0.0.0`、`PORT=3000`。
- Startup: `CMD ["node", "server.js"]`；不得使用 `next dev` 或重新安装 dependencies。
- Expose: `3000`。
- `.dockerignore` 至少排除 `.next`、`node_modules`、`tsconfig.tsbuildinfo`、`next-env.d.ts`、coverage、logs、`.git` 与 `.env*`；不得排除 package lock、source、Next config 或 tests needed by build context checks。
- Image identity: Compose 显式设置 `image: edge-mes-dashboard:local`，避免 rollback 依赖可变的 Compose project name。

`node:22.23.0-bookworm-slim` tag 已冻结到 patch line；implementation review 仍须记录实际 manifest/image digest。ARM64 build/run 只有在 Pi gate 执行后才能宣称 PASS。

## 8. Compose service design

未来 `docker-compose.yml` 中的冻结设计：

```yaml
dashboard:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  image: edge-mes-dashboard:local
  container_name: edge-mes-dashboard
  restart: "on-failure:5"
  environment:
    TZ: Asia/Shanghai
    NODE_ENV: production
    HOSTNAME: 0.0.0.0
    PORT: "3000"
    EDGE_MES_DASHBOARD_API_ORIGIN: http://api:8000
    EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: container
  ports:
    - "3001:3000"
  depends_on:
    api:
      condition: service_started
  healthcheck:
    test: ["CMD", "node", "-e", "fetch('http://127.0.0.1:3000/health').then(r=>{if(!r.ok)process.exit(1)}).catch(()=>process.exit(1))"]
    interval: 10s
    timeout: 3s
    retries: 10
    start_period: 20s
```

Design decisions:

- 继续固定 `container_name: edge-mes-dashboard`，与现有项目一致。
- 不挂载 source、`.next`、`node_modules`、Docker socket、`data/` 或 `.env`。
- 不新增 `privileged`、host network 或额外 capabilities。
- `depends_on` 只控制 Compose 启动顺序，**不能证明 API ready**。API 当前没有 Compose healthcheck，本计划不借 Dashboard 集成扩大修改 API service health semantics。
- API 未 ready、停止或故障时，Dashboard process 仍保持 healthy；accepted-events 页面本次 server render 显示 non-ready error/unavailable state，不保留旧 production truth。
- API 恢复后由下一次用户 page request 重新尝试一次；同一次 render 不 retry、不 fallback、不发第二个 request。
- 首版只重建 Dashboard image；不重建、不重启 API，除非 API 本身另有独立授权变更。
- `restart: "on-failure:5"` 只适用于 Dashboard；不得借本次修复修改其他 Compose service 的 restart policy。
- Dashboard build/up 后，部署 gate 最多等待 120 秒进入 `healthy`。在这 120 秒内累计出现超过 5 次 process restart、持续 `restarting`、持续 `unhealthy` 或最终未进入 `healthy`，立即停止本次部署。
- 失败终局必须显式执行 `docker compose stop dashboard`，随后进入 rollback/cancellation；不得让 Dashboard 继续无限重启。Docker healthcheck 的 `unhealthy` 本身不会自动触发可靠 rollback，停止动作由部署 gate 显式观察并执行。
- healthcheck 只能请求容器本地 `http://127.0.0.1:3000/health`，不得请求 API、DB 或 accepted facts；API failure 不得导致 Dashboard process restart。
- page render 仍保持同一次 render 最多一次 API request；恢复只由新的 browser/page request 触发。日志检查只能使用 bounded `--tail` 或 bounded time window，不得无界采集。
- 不引入 watchdog、监控平台、通用故障注入框架，也不修改其他 Compose service。

## 9. Environment and trusted-origin contract

Compose runtime 必须精确注入：

```text
EDGE_MES_DASHBOARD_API_ORIGIN=http://api:8000
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=container
```

Contract invariants:

1. 两个变量是 server-only runtime env，不是 build args，也不得改为 `NEXT_PUBLIC_*`。
2. resolver 必须继续返回 branded `TrustedAcceptedEventsApiOrigin`；页面不得直接读取字符串并发 fetch。
3. 只能使用 absolute `http://api:8000/api/v2/production/accepted-station-events?...`。
4. 不得 fallback 到 `localhost`、`127.0.0.1`、relative URL、host port `8000` 或 browser-origin。
5. browser 只访问 `<Raspberry-Pi-IP>:3001`，不得直接访问内部 Docker service name。
6. client 必须继续走 strict parser；不得从 legacy/raw/diagnostic endpoint 或 table 补值。
7. invalid config 必须在 request 前 fail closed，安全 UI message 不回显错误 origin 原值。
8. Dashboard container logs 只能记录安全 error code；环境值中不放 credentials 或 secret。

## 10. Healthcheck/readiness decision

| Choice | Assessment | Decision |
| --- | --- | --- |
| A. accepted-events page without query | 稳定返回 `invalid-query`，但把 query validation 页面误当 process health，且不能清晰区分 route contract | Reject |
| B. root or 404 | root/404 与 accepted-events runtime 无直接 readiness contract；404 成功判定语义错误 | Reject |
| C. minimal Dashboard `/health` route | 可证明 Next HTTP process 可接受请求；不触碰 API/DB/production data | **Select** |
| D. TCP/process only | 能证明端口/process 存在，但不能证明 Next HTTP route 可服务 | Reject as primary check |

新增 route 的严格边界：

- Exact path: `frontend/src/app/health/route.ts`。
- 只返回固定小响应，例如 `{"status":"ok","service":"dashboard"}` 与 2xx。
- 不读取 query、Dashboard API origin、API、DB、accepted-events page、production facts 或 filesystem state。
- 它只证明 Dashboard process/runtime HTTP ready；**不证明 API、DB、Collector、V-PLC 或 production facts ready**。
- 必须有独立 exact test `frontend/src/app/health/__tests__/route.test.ts`，证明 handler 不调用 fetch 且响应 shape 固定。
- route 与 test 都需要进入下一阶段独立 implementation allowlist；本 planning gate 不创建它们。

## 11. Raspberry Pi deployment flow

### 11.1 Deployment preflight and baseline record

部署路径保持：

```text
/opt/edge-mes-demo
```

在未来 PM 明确 remote runtime authorization 后，先记录本地 release commit 与远端基线。远端不依赖 `.git`，因为 `.git` 明确不复制。

```bash
cd /opt/edge-mes-demo
date -Is
docker compose config --quiet
docker compose ps
docker compose images
docker system df
df -h /opt/edge-mes-demo
docker stats --no-stream
```

若已存在 Dashboard，更新前保留 image：

```bash
release_id=<PM-approved-release-id>
old_dashboard_image=$(docker image inspect edge-mes-dashboard:local --format '{{.Id}}')
docker image tag "$old_dashboard_image" "edge-mes-dashboard:rollback-${release_id}"
```

同时在仓库外 deployment record 记录 source commit、resolved Compose config hash、旧 Dashboard image ID、container ID 与时间；不得把 SSH credential 或远端 `.env` 写入仓库。

### 11.2 File update boundary

发布只把 PM 审核后的 release files 同步到 `/opt/edge-mes-demo`，必须排除：

```text
data/
.env
.git/
frontend/node_modules/
frontend/.next/
frontend/tsconfig.tsbuildinfo
frontend/next-env.d.ts
__pycache__/
*.pyc
```

不得使用未保护 `data/` 与 `.env` 的 destructive sync。实际 `rsync` / `scp` transport 在 PM 提供连接方式并授权后单独冻结；本计划不记录 credential。

### 11.3 Compose validation and first deployment

文件落位后先验证，不 build 其他 service：

```bash
cd /opt/edge-mes-demo
docker compose config --quiet
docker compose config
docker compose build dashboard
docker compose up -d dashboard
docker compose ps dashboard api postgres
```

`docker compose up -d dashboard` 可以启动已存在但停止的 dependencies；它不构成 API readiness proof，也不要求 rebuild API。

### 11.4 Dashboard-only update

普通 Dashboard 更新：

```bash
cd /opt/edge-mes-demo
docker compose config --quiet
docker compose up -d --build --no-deps dashboard
docker compose ps dashboard
curl -fsS http://127.0.0.1:3001/health
```

`--no-deps` 保证更新不主动重建或重启 API/PostgreSQL。若 API、contract 或 DB 需要变化，必须开独立 gate。

### 11.5 Cache and disk behavior

- 第一次 Pi build 必须能访问 lockfile 中的 npm package source，或已有可用 Docker/BuildKit cache；不得把 host `node_modules` 作为替代。
- dependency layer 由 package files 决定；source-only update 应复用 `npm ci` layer/cache。
- 每次 build 可能留下旧 image 与 BuildKit cache。`docker system df`、BuildKit cache、image size、Docker root/project filesystem free space、memory 与 Swap 必须按 Section 14 在 build 前后重新记录；required metric 无法读取即 `HOLD`。
- Section 14 的 preflight -> build -> postflight 是 fail-closed 顺序：build 失败、超时、OOM kill 或不完整 image 时立即停止，不得继续 `docker compose up`；不得改用 host artifacts、不同 origin/profile/Node image、取消 non-root boundary、自动 prune 或删除 rollback image。
- postflight 任一资源门禁失败时不得启动新 Dashboard，必须保留旧 release/image 与 rollback assets 并报告 `HOLD`；不得通过自动清理绕过阈值。
- 本 gate 不自动执行 `docker system prune`、`docker builder prune` 或删除 rollback image；清理需要独立确认，且必须保留当前与 rollback image。
- 上述初始资源与 fail-closed 规则未来必须同步到 `docs/deployment/raspberry_pi.md`；该文件不在本轮 allowlist 内。

## 12. Consumer truth contract and real accepted-fact validation matrix

本节是 `DQ-DASH-D1/D2/D3` 的 current Architecture planning authority。它先冻结
accepted-events consumer truth，再定义真实 Pi DB-backed evidence。Docker health、API
health、synthetic fixture、mock response 或页面截图均不能替代本节合同。

真实闭环只可在 PM 明确 Raspberry Pi runtime authorization 后执行：

```text
V-PLC
-> Collector
-> Validator / accepted fact write
-> PostgreSQL
-> Accepted-events API
-> Accepted-events Dashboard
```

### 12.1 Exact 22-field type/nullability contract — DQ-DASH-D1

Consumer parser 必须在进入 view model 前验证 exact envelope、exact 22 keys、逐字段
JSON type/nullability、enum、UTC time、safe-integer、原始 numeric token 和下节 cross-field
contract。任何一个 item 不合法，整个 2xx response fail closed；不得返回 partial items、
跳过坏 row、补默认值或继续渲染其余合法 row。

Gate A 的成功响应 runtime authority 冻结为：

```text
HTTP Response
-> response.text()
-> source-preserving JSON parse
-> exact envelope / exact 22-field typed parser
-> cross-field validation
-> view model
```

Gate A implementation 已将 `apiClient.ts` 的 `await response.json()` 替换为
`response.text()` 与 raw-text parser。不得重新引入普通 `JSON.parse(rawText)` 后仅依靠
parsed number 的兼容路径，因为该顺序会在 schema boundary 前丢失原始数字词法。

`schema.ts` 必须规划 raw-text runtime 入口，例如：

```text
parseAcceptedStationEventsEnvelopeJson(rawText: string)
```

该入口是 runtime authority。既有 parsed-object 入口
`parseAcceptedStationEventsEnvelope(value: unknown)` 可保留用于 focused synthetic tests
或内部 typed-object validation，但它不能单独证明 no-rounding closure，也不得继续被
`apiClient.ts` 用作 HTTP response authority。

| # | Field | Frozen JSON contract | Consumer rule |
| ---: | --- | --- | --- |
| 1 | `line_id` | non-null string | 保留原始 string；空字符串不改成 null/`unknown`，display 明确为 `Empty string` |
| 2 | `plc_id` | non-null string | 同上 |
| 3 | `station_id` | non-null string | 同上 |
| 4 | `station_type` | non-null string | 同上 |
| 5 | `profile_id` | non-null string | 同上 |
| 6 | `config_hash` | non-null string | 同上；不得从 current config 补值 |
| 7 | `config_version` | non-null string | 同上；保持 historical row value |
| 8 | `event_type` | non-null string enum | 只允许 `station_cycle_start`、`station_cycle_complete`、`station_result`、`station_nok`；heartbeat/未知值 fail closed |
| 9 | `production_result` | string or explicit null | 非 null 时只允许 `ok`、`nok`、`skip`、`not_applicable`；numeric/unknown result fail closed |
| 10 | `unit_id` | string or explicit null | null 与空字符串保持不同 raw value；display 分离 |
| 11 | `dmc` | string or explicit null | null 与空字符串保持不同 raw value；display 分离 |
| 12 | `cycle_counter` | JSON number, non-null safe integer | raw-text parser必须先验证原始token为canonical decimal integer且位于safe range；typed parser再验证 `typeof number` 与 `Number.isSafeInteger`；numeric-looking string、NaN/Infinity、fraction、exponent、`-0`、unsafe integer fail closed；不得舍入、截断或模糊化 |
| 13 | `source_event_id` | non-null string | 保留 raw string；不得使用 `fact_key` 或 display placeholder 替代 |
| 14 | `event_ts` | non-null valid UTC ISO string | 必须是可解析且带 `Z` UTC 的 API string；number timestamp、无时区/无效string fail closed；不得与 `accepted_at` 交换 |
| 15 | `accepted_at` | non-null valid UTC ISO string | 同上；语义只为 accepted fact timestamp，不是 freshness/ACK/read_done time |
| 16 | `fact_key` | non-null string | canonical row/renderer join key；空字符串保留但不得补造 identity |
| 17 | `content_fingerprint` | non-null string | 保留 raw accepted fact identity/reference |
| 18 | `nok_code` | safe integer number or explicit null | number时必须保留并验证原始numeric token；null保持显式null；不接受numeric-looking string、fraction、exponent、`-0`或unsafe integer |
| 19 | `nok_origin` | string or explicit null | 不接受 number/object/array；空字符串保留其 raw 语义 |
| 20 | `nok_detail_code` | safe integer number or explicit null | number时必须保留并验证原始numeric token；null保持显式null；不接受numeric-looking string、fraction、exponent、`-0`或unsafe integer |
| 21 | `nok_detail_source_event_id` | string or explicit null | 不接受 number；不得从 diagnostic/source candidate 补值 |
| 22 | `nok_detail_evidence_fact_key` | string or explicit null | accepted upstream evidence reference；不得从 legacy/raw/diagnostic source 补值 |

统一规则：non-null string 不接受 number、boolean、object、array或null。Nullable string
只接受 string 或显式 JSON null。当前任务不把 DB `BIGINT` API 改为 string；未来若必须
支持超出 JavaScript safe integer 的 `cycle_counter`，需另开 API contract planning，
不得在 Consumer Truth Hardening 中自行扩大 producer contract。

#### Source-preserving numeric lexeme contract

`parseAcceptedStationEventsEnvelopeJson(rawText)` 使用 Node `22.23.0` runtime 已支持的
`JSON.parse(rawText, reviver)` `context.source`，在信任 JavaScript number 前读取原始
numeric token。需要执行该检查的字段只有：

```text
cycle_counter
nok_code
nok_detail_code
page.limit
```

冻结规则：

1. 上述字段的值为 number 时，reviver 必须取得对应 `context.source`；缺失 source
   context 时整个 response fail closed，不得退回普通 `JSON.parse` 或 parsed-object
   validation。
2. 原始 token 必须匹配 canonical decimal integer：

   ```text
   ^(?:0|-?[1-9][0-9]*)$
   ```

   因此必须拒绝 decimal fraction、exponent、leading-zero变体和 `-0`。
3. 对通过词法检查的 token 使用 `BigInt(context.source)`，并验证范围为：

   ```text
   Number.MIN_SAFE_INTEGER
   ...
   Number.MAX_SAFE_INTEGER
   ```

   超出范围时整个 response fail closed，不得先舍入、截断或转成display text。
4. raw-token gate通过后，exact typed parser仍必须验证 `typeof value === "number"`、
   `Number.isSafeInteger(value)`、field-level nullability和cross-field contract。
5. `nok_code`与`nok_detail_code`为显式null时不要求numeric source；为number时必须执行
   完整source-preserving gate。`cycle_counter`与`page.limit`必须为number。
6. `page.limit`通过词法和safe-range检查后仍必须满足 `1..500`。
7. numeric-looking string由typed parser拒绝；NaN/Infinity不是合法JSON，parse failure
   仍整体映射为fail-closed error。
8. 任一item或`page.limit`失败时整个2xx response失败，不得跳过bad row、返回partial
   items或继续渲染其他row。

TypeScript边界：当前`tsconfig.json`只声明`ES2022` lib。Gate A不得修改tsconfig、package
files或dependencies；`schema.ts`应使用最小module-local type wrapper/type narrowing表达
Node `22.23.0`的reviver context `{ source?: string }`，不得加入第三方lossless JSON库。
运行时若实际没有提供source context，按上述规则fail closed，而不是启用兼容fallback。

错误与数据泄漏边界：source-preserving parse、JSON syntax、numeric token、exact parser或
cross-field validation失败均保持client `kind: "error"`，并使用稳定、通用的安全消息。
不得向页面、日志或报告回显完整raw response、原始numeric lexeme、内部origin、DB error、
raw payload或parser内部细节。request URL、fetch options、status mapping、single-request、
no-retry和no-fallback行为不变。

Gate A focused tests至少冻结：

```text
Schema raw-text rejects:
- "cycle_counter": 1.0
- "cycle_counter": 1e0
- "cycle_counter": 9007199254740991.1
- "cycle_counter": 9007199254740992
- "cycle_counter": "12"
- "nok_code": 10.0
- "nok_detail_code": 2e0
- "limit": 50.0
- any numeric token spelled as -0

Schema raw-text accepts:
- "cycle_counter": 0
- "cycle_counter": 9007199254740991
- "cycle_counter": -9007199254740991
- "nok_code": null
- "nok_detail_code": null
- "limit": 50
```

Schema tests还必须证明：一个非法item导致整个response失败；source context不可用时fail
closed；raw body和numeric lexeme不进入错误消息；parsed-object parser仅为synthetic/
internal validation，不能替代raw-text runtime test。

API client tests必须证明：成功2xx只调用`response.text()`和raw-text parser；不调用
`response.json()`；rounding/fraction payload返回`kind: "error"`；一次render仍只有一次
HTTP request；不retry、不fallback；parser错误消息不泄漏raw body或trusted origin。

### 12.2 Cross-field semantic validation — DQ-DASH-D2

| Event type | Required production/NOK shape | Forbidden combination |
| --- | --- | --- |
| `station_result` + `production_result=nok` | `production_result` non-null；`nok_code` non-null safe integer；`nok_origin` non-null string；三个 `nok_detail_*` 全部 null | 缺失 NOK authority、任何 detail companion 字段非null |
| `station_result` + `ok/skip/not_applicable` | `production_result` non-null；`nok_code`/`nok_origin` null；三个 `nok_detail_*` null | 非NOK result携带NOK或detail authority |
| `station_nok` | `production_result=null`；`nok_code`、`nok_origin`、`nok_detail_code`、`nok_detail_source_event_id`、`nok_detail_evidence_fact_key` 全部非null | 把detail companion投影为第二个production outcome，或缺失accepted upstream detail evidence |
| `station_cycle_start` / `station_cycle_complete` | `production_result=null`；`nok_code`/`nok_origin` null；三个 `nok_detail_*` null | cycle row携带outcome、NOK或detail authority |

Parser 必须在构造 `AcceptedStationEventItem` 前完成上述关系验证。违反关系的 malformed
2xx response 整体映射为 client `kind: "error"`，不得进入 view model、不得部分渲染、
不得转成 empty/invalid-query/unavailable，也不得从 DB migration 已有 producer constraint
推断 consumer 无需防御。

### 12.3 Raw API value and display value separation — DQ-DASH-D2

冻结 consumer 分层：

```text
HTTP JSON
-> exact parser: typed raw AcceptedStationEventItem
-> view model: raw value retained + separately derived display value/display kind
-> renderer: consumes display value, never rewrites or claims it is the API value
```

- Parser 必须原样保留 API string/number/null；不得使用 `?? null`、`String(...)`、
  `Number(...)` 或 `"unknown"` normalization。
- View model 必须保留 raw value，并单独派生 display text / display kind；三层逐字段对账
  使用 raw API value，不使用 display placeholder。
- API explicit null 可显示 `—` 或 `Not applicable`，但 retained raw value仍为null。
- 空字符串显示为明确 `Empty string`，不得显示成null、missing或unknown。
- Missing key、invalid type和invalid cross-field combination不是display state，而是整个
  response fail-closed error。
- 不得用含糊的 `unknown` 同时表示 null、empty、invalid、missing或not applicable。
- `station_nok` production outcome显示为 `Not applicable — NOK detail companion`；cycle
  event显示为 `Not applicable — cycle event`；这两个display不得进入production-result统计。
- production result summary只统计 `event_type=station_result`；`station_nok`和cycle events
  不计入 `byResult`。总 accepted fact row count仍可统计所有当前页accepted facts，并继续
  标记 `Current page only`。
- NOK/detail panel必须显示row type/role，明确区分 `station_result outcome` 与
  `station_nok detail companion`。
- table row、NOK/detail panel与trace reference必须从同一个 selected raw item派生，并以
  同一个 `fact_key` 绑定。当前target-first-item策略保持；它只证明该bounded request的
  `items[0]`，不得扩大成整页全部records闭环。

Current renderer static impact：

- `schema.ts` 承载逐字段类型、enum、UTC、safe-integer和cross-field fail-closed boundary；
- `viewModel.ts` 承载raw/display分离、row role、production-result-only summary和同一item派生；
- `AcceptedEventsTable.tsx` 承载outcome/null/empty display；
- `NokDetailEvidencePanel.tsx` 承载row role与detail companion语义；
- `PageSummaryStrip.tsx` 必须明确result mix仅为 `station_result`；
- `TraceReferencePanel.tsx` 当前也使用 `unknown` placeholder，直接承载null/empty display，
  因此属于Gate A最小范围；
- `page.tsx` 当前已把第一row fact key、selected evidence和selected reference绑定到同一
  first item，不需要production source修改；只需page focused regression覆盖新语义。

不得新增 debug view、raw-data page、selection功能、API fallback或新业务字段。

### 12.4 Frozen real DB-backed cases — DQ-DASH-D3

| Case | Mandatory row shape | Execution / claim rule |
| --- | --- | --- |
| **Case A — accepted `station_result` OK** | `event_type=station_result`；`production_result=ok`；`nok_code=null`；`nok_origin=null`；全部 `nok_detail_*=null` | Mandatory；同一 `fact_key` 完成 DB raw row、API raw item、Dashboard display mapping逐字段对账 |
| **Case B — accepted `station_result` NOK** | `event_type=station_result`；`production_result=nok`；`nok_code`非null integer；`nok_origin`非null string；全部 `nok_detail_*=null` | Mandatory；不得用 `station_nok` detail row替代outcome evidence |
| **Case C — accepted `station_nok` detail companion** | `event_type=station_nok`；`production_result=null`；`nok_code`、`nok_origin`和三个 `nok_detail_*` 全部非null；`nok_detail_evidence_fact_key`引用accepted upstream evidence | 仅在真实Pi数据库存在该row时执行；不存在时必须写 `NOT AVAILABLE / NOT VERIFIED` |

Case C 不得由 synthetic fixture、mock response、API-only response或 Case B 的
`station_result` NOK代替。Cycle event不得作为Case A；`station_nok`不得作为Case B。
每个case只可声明一个独立bounded request目标第一项闭环。

### 12.5 Evidence identity and three-layer comparison

- 使用 `fact_key` 作为三层主 identity，同时核对 `source_event_id`、
  `content_fingerprint`、`event_ts` 与 `accepted_at`。
- synthetic fixture不得作为DB-backed evidence；每份记录必须标明 `real DB-backed` 或
  `synthetic`。
- bounded query / opaque cursor必须让目标 `fact_key` 成为API `items[0]`；否则该case不得
  宣称Dashboard visible-value closure。

| Layer | Required evidence | Pass condition |
| --- | --- | --- |
| PostgreSQL | 从 `production_accepted_station_event_fact` 按目标 `fact_key` 读一行 | 恰好一行；保存直接22字段raw row，不join legacy/raw/diagnostic table |
| API | 对同一 `line_id` 与bounded time window请求accepted-events endpoint | exact envelope/22 keys；目标item为第一项；raw values与DB row一致；UTC serialization差异按合同显式对账 |
| Dashboard | 请求 `http://<Pi-IP>:3001/accepted-events?...` | table、Trace reference、NOK/detail panel绑定同一 `fact_key`；display值由对应raw值和冻结display rule推导；无raw/legacy/diagnostic字段 |

对账表必须包含全部22字段的：DB raw value、API raw JSON value、display rule、Dashboard
visible value、PASS/FAIL。Display placeholder不能填入API raw value列。

### 12.6 Query, empty and pagination evidence

- Empty：已知无row的bounded window，API `items=[]`，Dashboard显示empty且无旧值。
- Pagination：使用 `limit` 产生 `next_cursor`，第二次独立page request原样传入opaque
  cursor；验证stable order、无重复/遗漏，并说明每个render仍只发一个API request。
- 不以“页面看起来正常”作为PASS；必须保留DB row、API item与Dashboard visible-value
  三方对账表。第一项证据不得宣称当前页所有row均已逐字段闭环。

## 13. Failure/recovery matrix

| Case | Evidence tier | Expected Dashboard behavior | Required invariants |
| --- | --- | --- | --- |
| Dashboard config missing | focused test + future container config-negative run | safe `error`；0 API request | no fallback, no origin value leak, no production surfaces |
| Dashboard config wrong | focused test + future container config-negative run | safe `error`；0 API request | no localhost/relative fallback |
| API container stopped | Pi runtime | transport `error`；Dashboard health remains healthy；Dashboard process 不 restart | one failed attempt for render, no stale truth, no second request |
| API returns 4xx | focused/client/page test；real API invalid query where applicable | `invalid-query` | no fallback, no production surfaces |
| API returns 503 | focused/client/page test + Pi recovery observation | `unavailable` | no stale truth, no retry |
| API returns other 5xx | focused/client/page test | `error` | no stale truth, no retry |
| API returns malformed 2xx | strict-parser/client/page test | `error` | no partial salvage, no raw/legacy leakage |
| API recovers | Pi runtime | 下一次新的 browser/page request 进入 ready | recovery 不在旧 render 中 retry；新 render exactly one request |
| Dashboard container restart | Pi runtime | `/health` 从 unavailable 到 healthy，随后 page 可重新加载 | env 保持 canonical；无 client-stored stale truth |
| Dashboard process exit / bounded restart | Pi runtime + bounded logs | 记录 process restart 次数；最多允许 5 次自动 restart | 120 秒内超过 5 次、持续 `restarting`、持续 `unhealthy` 或未进入 `healthy` 即 terminal stop；执行 `docker compose stop dashboard` |
| Dashboard healthcheck `unhealthy` | Pi runtime | 不把 healthcheck 状态自动当作 rollback；部署 gate 显式观察并停止 | healthcheck 只请求本地 `/health`；不得请求 API/DB/facts；失败后 Dashboard 为 stopped |
| Dashboard log-loop / request-loop | bounded logs + request observation | 失败后停止采集与部署 | bounded `--tail`/time window；无持续 crash-loop、log-loop、API request/retry storm |
| Compose overall restart | PM-authorized Pi runtime | order 可观察；API 未 ready 时 fail closed，下一次 request 恢复 | `depends_on` 不被误称 readiness proof |
| Empty query result | real API + Dashboard | explicit empty | no old row/detail/summary truth |
| NOK accepted fact | real DB/API/Dashboard | NOK 与 detail visible | same `fact_key`; accepted evidence only |
| Paginated result | real API + Dashboard | page 1/page 2 各自 bounded | opaque cursor；stable order；one request per render |

所有 case 继续保持：

```text
no fallback
no stale production truth
no second request within one render
no raw/legacy/diagnostic data leakage
```

R1 deployment gate 的终局证据必须同时记录：

1. Dashboard process exit 与 `RestartCount` 的实际次数；
2. 从 `docker compose up` 开始到 120 秒的终局状态，明确 `healthy` 或失败；
3. 失败后 `docker compose stop dashboard` 已完成，且 Dashboard 不再处于 `running`、`restarting` 或持续 `unhealthy`；
4. 同一次 page render 的 API request 次数为 0 或 1，恢复只由新的 browser/page request 产生，不存在 request/retry storm；
5. bounded 日志窗口中不存在持续 crash-loop 或 log-loop。

不要为 malformed 2xx 或其他 negative cases在 Pi 上构建通用故障注入/取证平台；现有 focused tests 可提供该层证据，Pi runtime 聚焦 container/network/restart 与真实 DB-backed closed loop。

## 14. Resource baseline

Dashboard build/deploy 必须按“build 前 preflight -> build -> build 后、deploy 前 postflight”顺序执行。以下是首版保守资源门禁；它只适用于 Dashboard build/deploy，不是 Node-RED 容量指标，也不扩展为通用资源监控平台。

### 14.1 Build 前 preflight

在任何 `docker compose build dashboard` 前，必须记录同一份 baseline record：

```bash
cd /opt/edge-mes-demo
docker info --format '{{.DockerRootDir}}'
docker system df
docker builder du
docker image inspect edge-mes-dashboard:local --format '{{.Id}} {{.Size}}'
docker image inspect edge-mes-dashboard:rollback-<release-id> --format '{{.Id}} {{.Size}}'
df -h /opt/edge-mes-demo
df -h "$(docker info --format '{{.DockerRootDir}}')"
free -h
swapon --show
```

记录字段必须包括：

- Docker root directory；
- Docker disk usage；
- BuildKit cache usage；
- 当前 Dashboard image 与 rollback image（若不存在，记录为 absent）；
- `/opt/edge-mes-demo` 所在 filesystem free space；
- Docker root 所在 filesystem free space；
- memory used、Swap used；
- 当前与 rollback image 的 baseline image IDs。

Docker root 与 `/opt/edge-mes-demo` 所在 filesystem 均至少保留 `6 GiB` free。若二者是同一 filesystem，只计算一次，但必须在 record 中明确记录二者相同。若已存在 rollback Dashboard image，Docker root filesystem 的 required free space 取以下较大值：

```text
max(6 GiB, 2 × rollback image size + 3 GiB)
```

如果任一 required metric 无法读取，立即 `HOLD`，不得 build 或 deploy。连续两个、间隔 30 秒的 preflight samples 中若 Swap used 持续增长，立即 `HOLD`。若现有远端 Dashboard 需要 rollback 但 required rollback asset（旧 release files、旧 image identity/tag、resolved Compose baseline）缺失，不得 build。

### 14.2 Build fail-closed

- `docker compose build dashboard` 失败、超时、被 OOM kill 或产生不完整 image，立即停止；不得继续 `docker compose up`。
- build 失败时不得自动改用 host `node_modules`、host `.next`、macOS build artifact、localhost origin、临时 origin、错误 profile、不同 Node image，或取消 non-root boundary。
- 不自动执行 `docker system prune`、`docker builder prune`，也不删除 rollback image；旧 release/image 与 rollback assets 必须保留。

### 14.3 Build 后、deploy 前 postflight

build 完成后、启动新 Dashboard 前，重新记录与 14.1 相同的一组指标，并加入新 Dashboard image ID/size 与 BuildKit cache 增量。必须满足：

- 两个相关 filesystem 的 free space 仍至少为 `3 GiB`；同一 filesystem 仍只计算一次并明确记录；
- 新增 Dashboard image 加 BuildKit cache 的总增长不超过 `3 GiB`；
- 最终 Dashboard image size 不超过 `1 GiB`；
- 等待 120 秒后，Swap used 不得高于 build 前 baseline 超过 `256 MiB`；
- Swap 必须在两个、间隔 30 秒的 post-build samples 中保持不增长。

任一条件不满足：不启动新 Dashboard，保留旧 release/image 与 rollback assets，报告 `HOLD`，不得自动清理以绕过阈值。只有全部 postflight 条件满足后，才可进入 Section 11.3 的 Dashboard `up` 与 R1 120 秒 healthy gate。

### 14.4 Pi runtime observation record

在资源门禁通过并获得独立 runtime authorization 后，至少在 deployment 前、Dashboard idle、一次真实 page request 后记录：

```bash
docker stats --no-stream edge-mes-dashboard
docker inspect edge-mes-dashboard --format '{{.State.StartedAt}} {{.State.Health.Status}} {{.Image}}'
docker image inspect edge-mes-dashboard:local --format '{{.Id}} {{.Size}}'
uptime
free -h
swapon --show
df -h / /opt/edge-mes-demo
docker system df
```

还必须记录：

- Dashboard container CPU / memory。
- 整机 CPU / memory / Swap / disk free。
- image size 与 Docker build cache growth。
- `docker compose up` 到 Dashboard health `healthy` 的 startup time。
- 对同一 bounded real-fact query 的 API response time。
- 对应 Dashboard page response time。

建议用 `curl -o /dev/null -sS -w '%{http_code} %{time_total}\n'` 记录 API 与 page timing，并保存 exact URL scope。这里不定义多产线 capacity threshold；Node-RED / multi-line load 属于后续分支。

## 15. Rollback plan

### 15.1 Required rollback assets

- 部署前 source release ID / commit。
- 上一版 release files 或完整版本目录；绝不包含或覆盖 `data/` 与远端 `.env`。
- `edge-mes-dashboard:rollback-<release-id>` image tag 与 image ID。
- 部署前 resolved Compose config 与 service/container baseline。

### 15.2 Subsequent Dashboard update rollback

先恢复上一版 `docker-compose.yml` 与 frontend release files，然后：

```bash
cd /opt/edge-mes-demo
docker image tag "edge-mes-dashboard:rollback-<release-id>" edge-mes-dashboard:local
docker compose config --quiet
docker compose up -d --no-deps --force-recreate dashboard
docker compose ps dashboard
curl -fsS http://127.0.0.1:3001/health
```

随后重新执行一条 bounded accepted-events query，确认 rollback 后仍为 fail-closed / valid ready state。不得运行 `docker compose down`，避免无关服务中断。

### 15.3 First deployment rollback

首次部署失败必须先区分远端是否已有上一版 Dashboard；不得把两个场景都写成“Dashboard rollback PASS”。

#### A. 远端已经存在上一版 Dashboard

该场景按普通版本 rollback 处理，必须复用 Section 15.2 的闭环：

1. 恢复上一版 `docker-compose.yml` 与 frontend release files；
2. 恢复旧 Dashboard image identity；
3. 重新创建上一版 Dashboard；
4. 验证 Dashboard `/health`；
5. 执行一次 bounded accepted-events request；
6. 验证 API、PostgreSQL、Collector、V-PLC 与 `data/` 未被重建或覆盖。

缺少旧 release files、旧 image identity、resolved Compose baseline 或上述验证证据时结论为 `HOLD`，不得部署。

#### B. 首次增加 Dashboard，远端没有上一版 Dashboard

该场景定义为：

```text
first-deployment cancellation / existing-core-services non-impact validation
```

该路径的最小恢复步骤为：

1. 停止并移除失败的 Dashboard container/service instance；在仍包含 `dashboard` service 的新 Compose config 下仅允许使用：

   ```bash
   docker compose stop dashboard
   docker compose rm -sf dashboard
   ```

2. 恢复部署前 `docker-compose.yml` 与 release files；
3. 执行：

   ```bash
   docker compose config --quiet
   ```

4. 确认不存在 `edge-mes-dashboard` container，并确认 host port `3001` 不再监听；
5. 对照部署前 baseline 检查现有 core services 的 service/container/image 状态；
6. 验证 PostgreSQL `healthy`；验证 API `/health`；验证 V-PLC `/health` 或既有 runtime health endpoint；验证 Simulator、Grafana、Prometheus 的既有 health endpoint；
7. 确认 Collector、API、PostgreSQL、Grafana、V-PLC 未因取消操作被重建；
8. 确认 `data/` 与远端 `.env` 未被删除、覆盖或重新初始化。

该路径恢复后不存在 Dashboard，因此不要求也不允许伪造 Dashboard `/health` 或 accepted-events page PASS。终局只能是 `cancellation/non-impact PASS` 或 `HOLD`。

两条路径均禁止：

- `docker compose down`；
- volume delete、image prune、data restore、DB migration rollback；
- 其他 service rebuild。

## 16. Security and secret boundary

- `EDGE_MES_DASHBOARD_API_ORIGIN` 与 profile 是非敏感 internal topology；不得携带 credential。
- `.env` 不复制进 build context/image，不覆盖远端 `.env`，也不写入报告或 Git。
- Dashboard 使用 non-root `node`，不挂 Docker socket、不使用 privileged/host network、不挂持久化业务数据。
- `http://api:8000` 只在 Compose bridge network 内使用；browser 只访问 Pi `3001`。
- 首版无 TLS/auth，故只能用于受控内网 Demo；不得表述为公网或生产安全边界。
- host port `3001` 按现有 Compose 风格监听 host interfaces。remote preflight 必须检查实际 listener/firewall；发现冲突即 **HOLD**，不得改用其他端口绕过冻结值。
- Server-only env 不得改为 `NEXT_PUBLIC_*`；内部 service DNS 与 origin 不应进入 browser-side fetch contract。
- runtime error 页面不得泄漏原始 origin、secret、DB error、raw payload 或 stack trace。

## 17. Sequential implementation Gates and exact proposed allowlists

本次 repair 冻结两个严格顺序 Gate。两者均只是未来建议allowlist；当前不授权任何
implementation、tests或runtime。

### 17.1 Gate A — Accepted-events Consumer Truth Hardening

Gate A必须先关闭 `DQ-DASH-D1` residual numeric source-preservation风险，并实现已冻结
的 `DQ-DASH-D2/D3` consumer contract：response text/source-preserving numeric lexeme、
逐字段类型/nullability、safe integer、enum/UTC、event/result/NOK cross-field fail closed、
raw/display分离、outcome/detail UI语义和focused tests。

精确建议allowlist：

```text
MODIFY frontend/src/lib/acceptedStationEvents/schema.ts
MODIFY frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts
MODIFY frontend/src/lib/acceptedStationEvents/apiClient.ts
MODIFY frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
MODIFY frontend/src/lib/acceptedStationEvents/viewModel.ts
MODIFY frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts
MODIFY frontend/src/components/accepted-events/AcceptedEventsTable.tsx
MODIFY frontend/src/components/accepted-events/__tests__/AcceptedEventsTable.test.tsx
MODIFY frontend/src/components/accepted-events/NokDetailEvidencePanel.tsx
MODIFY frontend/src/components/accepted-events/__tests__/NokDetailEvidencePanel.test.tsx
MODIFY frontend/src/components/accepted-events/PageSummaryStrip.tsx
MODIFY frontend/src/components/accepted-events/__tests__/PageSummaryStrip.test.tsx
MODIFY frontend/src/components/accepted-events/TraceReferencePanel.tsx
MODIFY frontend/src/components/accepted-events/__tests__/TraceReferencePanel.test.tsx
MODIFY frontend/src/app/accepted-events/__tests__/page.test.tsx
```

路径纳入理由：

- `schema.ts`/test：raw-text runtime parser、source-preserving numeric lexeme gate、parsed-object
  synthetic/internal boundary和22-field fail-closed matrix；
- `apiClient.ts`/test：唯一HTTP response text seam；必须把`response.json()`替换为
  `response.text()` + raw-text parser，并证明single-request/no-retry/no-fallback与安全通用
  parse error message；schema-only修改无法恢复已经丢失的number lexeme；
- `viewModel.ts`/test：raw/display分离、row role、result-only summary、same-item derivation；
- table/detail/summary/trace组件及tests：这些组件当前直接渲染`unknown`或result mix，确实
  承载新display/outcome规则；
- `page.test.tsx`：验证完整ready render的同一`fact_key`绑定、station_result/station_nok/
  cycle display、empty/error no-stale regression；不修改page生产逻辑。

原则上明确排除：

```text
frontend/src/app/accepted-events/page.tsx
frontend/src/lib/acceptedStationEvents/apiOrigin.ts
frontend/src/lib/acceptedStationEvents/query.ts
frontend/package.json
frontend/package-lock.json
frontend/tsconfig.json
frontend/next.config.ts
DB migration / Collector / API route / API tests / Docker / Compose / deployment / Grafana
```

`page.tsx`现有first-item binding无需修改。`apiClient.ts`仅允许修改成功2xx body读取、
raw-text parser调用与安全通用parse error mapping；request URL、fetch options、4xx/503/
other-5xx mapping、single-request、no-retry和no-fallback行为必须保持不变。若Gate A实现
发现必须修改上述排除路径，立即`HOLD`并回PM；不得自行扩大。

Gate A必须完成独立的Architecture、Reliability、Data Quality、Verification focused
implementation reviews且全部无blocker，PM才能宣布Gate A关闭。Gate A PASS不授权Git
write或Gate B。

### 17.2 Gate B — Dashboard Raspberry Pi Docker Integration

Gate B只能在Gate A独立关闭后恢复原部署六文件范围：

```text
CREATE frontend/Dockerfile
CREATE frontend/.dockerignore
CREATE frontend/src/app/health/route.ts
CREATE frontend/src/app/health/__tests__/route.test.ts
MODIFY docker-compose.yml
MODIFY docs/deployment/raspberry_pi.md
```

Gate B只实现standalone image、Dashboard process health、Compose service、Pi deployment/
rollback/resource guide。Gate B不得再次修改accepted-events schema、view model、renderer、
consumer tests或业务语义；若部署实现需要consumer改动，结论必须为`HOLD`并回到新的
Consumer Truth planning gate。

## 18. Frozen review and authorization sequence

当前冻结顺序：

1. Architecture `DQ-DASH-D1` numeric source-preservation docs-only repair：CLOSED。
2. Data Quality planning re-review round 2：CLOSED；`DQ-DASH-D1/D2/D3` 全部 CLOSED。
3. Gate A 15-file Consumer Truth Hardening implementation：CLOSED；implementation commit
   `a3cf64de31bf5eb12a1aa3eeed52aa3a451b8e79` 已 push。
4. Gate A Architecture、Reliability、Data Quality、Verification focused implementation
   reviews：全部 CLOSED / PASS WITH RECOMMENDATIONS，无 blocker。
5. PM Gate A overall closeout：CLOSED / PASS WITH RECOMMENDATIONS。
6. 下一 eligible gate 为 Gate B Verification planning review；复核 Section 17.2 六文件
   allowlist、process health/API readiness分离、startup/recovery、no retry/no stale、
   bounded restart、rollback/cancellation、ARM64、Compose/network/port、resource gate与
   real DB-backed Case A/B/C evidence plan。
7. 只有 Gate B Verification planning review 无 blocker，且 PM 单独授权后，才能执行
   六文件 Gate B implementation及后续独立focused reviews；不得借部署任务重开consumer
   业务语义。
8. PM Raspberry Pi runtime authorization必须再次单独批准transport、remote commands、
   release files、rollback ID和真实DB-backed evidence scope。
9. Remote deployment/evidence/status sync与stage/commit/push仍分别需要PM明确授权。

Gate A closure不自动授权Gate B implementation或runtime。Reviewer不得重新引入已废弃的
通用强审计取证框架，也不得重开已关闭的`DQ-DASH-D1/D2/D3`，除非新的实现事实改变其
authority。

## 19. Risks and recommendations

### Architecture repair disposition

```text
DQ-DASH-D1: CLOSED; source-preserving response.text/context.source implementation and reviews passed
DQ-DASH-D2: CLOSED; cross-field/raw-display/outcome-detail implementation and reviews passed
DQ-DASH-D3: CLOSED; real Case A/B/C planning matrix preserved; runtime evidence still pending
Gate A Architecture review: CLOSED / PASS WITH RECOMMENDATIONS
Gate A Reliability review: CLOSED / PASS WITH RECOMMENDATIONS
Gate A Data Quality review: CLOSED / PASS WITH RECOMMENDATIONS
Gate A Verification review: CLOSED / PASS WITH RECOMMENDATIONS
Gate A overall: CLOSED / PASS WITH RECOMMENDATIONS
Gate A implementation commit: a3cf64de31bf5eb12a1aa3eeed52aa3a451b8e79
```

Gate A closure只证明consumer implementation及本地focused/full validation完成。当前证据仍
为`synthetic / focused implementation evidence`，不得解释为Gate B、Raspberry Pi、真实
DB-backed Case A/B/C或三层runtime闭环PASS。

### Recommendations / carry-forward

1. **ARM64 proof pending:** lockfile 与 official image 均有 ARM64 path，但实际 Pi native build、startup 与 page request 未执行；必须在 remote runtime gate 证明。
2. **Dependency source/cache:** tracked lockfile 的 resolved package source 与 Pi network/cache 可用性需要 preflight；失败时 HOLD，不得复制 host `node_modules` 或 host-built `.next`。
3. **Image identity:** implementation/release evidence记录 `node:22.23.0-bookworm-slim` resolved digest 与最终 Dashboard image ID，便于供应链追踪与 rollback。
4. **Port reality:** repo 无 3001 冲突，但 Pi host listener 只有 remote preflight 能证明；冲突时回 PM，不自行换端口。
5. **Detail selection:** 当前 UI detail panel 固定第一项。真实三层对账必须让目标 fact 成为 response 第一项；这不是本轮新增 Dashboard 交互功能的授权。
6. **Health semantics:** `/health` 只能用于 Dashboard process readiness；不得把 healthy container 宣称为 API/DB/accepted-fact closed-loop PASS。
7. **Disk growth:** 保留一个明确 rollback image，同时观察 BuildKit cache；清理动作不得与部署隐式捆绑。
8. **Consumer empty-string semantics:** producer contract当前未统一禁止所有identity/config string为空；Gate A必须保留raw empty string并显式显示，不得擅自补造业务值。若后续producer决定禁止empty string，应另开contract gate。
9. **BIGINT beyond safe integer:** 当前Gate A只允许safe integer number并fail closed；超出范围的真实数据需要新的API serialization contract，不得在Dashboard静默舍入或改用模糊文本。
10. **Case C availability:** 真实Pi若无accepted `station_nok` row，必须记录 `NOT AVAILABLE / NOT VERIFIED`；这不阻塞Case A/B，但不得伪造detail closure。

### Repair closeout / next-gate constraints

- `REL-DASH-R1` 已冻结 Dashboard 专用 `restart: "on-failure:5"`、120 秒 healthy 终局、显式 stop、local-only healthcheck、single-request/no-storm 与 bounded log evidence；这些是后续 Reliability/Verification 的设计 gate，不是本轮 runtime PASS。
- `REL-DASH-R2` 已冻结“远端已有上一版”普通版本 rollback 与“首次新增且无上一版”`first-deployment cancellation / existing-core-services non-impact validation` 的分支终局；缺少 required asset/evidence 只能 `HOLD`。
- `REL-DASH-R3` 已冻结 14.1/14.2/14.3 的 6 GiB、rollback image size、3 GiB、1 GiB、Swap `256 MiB` 与双样本增长门禁；任何阈值失败都不得启动新 Dashboard，不得通过自动清理绕过。
- 这些规则未来必须同步到 `docs/deployment/raspberry_pi.md`；该文件是本轮 excluded file，当前不得修改。
- 资源阈值仅适用于首版 Dashboard build/deploy，不是 Node-RED 容量指标或通用资源监控平台。只有真实 Pi evidence 证明阈值不适用时，才可由 PM 另开 planning repair 调整；现场不得绕过。

## 20. Final conclusion

**PASS WITH RECOMMENDATIONS — Gate A CLOSED; Gate B NOT AUTHORIZED**

`DQ-DASH-D1` runtime authority已实现为`response.text()` -> source-preserving `JSON.parse`
reviver `context.source` -> exact typed parser，并覆盖canonical integer lexeme、BigInt
safe-range、source-context缺失fail closed与稳定安全error。`DQ-DASH-D2` 的cross-field/
raw-display/outcome-detail implementation与`DQ-DASH-D3`的real Case A/B/C planning matrix均
通过独立review。Gate A 15-file implementation已提交并push于：

```text
a3cf64de31bf5eb12a1aa3eeed52aa3a451b8e79
Harden accepted-events consumer truth
```

Gate A Architecture、Reliability、Data Quality与Verification focused implementation reviews
全部CLOSED / PASS WITH RECOMMENDATIONS且无blocker；PM终局复验为full frontend suite
`11 files / 237 tests` PASS、typecheck PASS、Next production build PASS。因此Gate A overall
为CLOSED / PASS WITH RECOMMENDATIONS。

当前证据仍只属于`synthetic / focused implementation evidence`。Docker/Compose、ARM64
Pi build/run、port/network、restart/rollback、真实DB-backed Case A/B/C三层对账与资源基线
均未执行或声明PASS。

下一eligible gate为PM授权的Gate B Verification planning review。Gate B implementation、
Raspberry Pi runtime、deploy/rollback及任何后续Git write仍需分别明确授权。
