# Sprint 3 Dashboard Raspberry Pi Runtime Deployment Evidence Plan

报告名称：

`Sprint 3 Dashboard Raspberry Pi Runtime Deployment Evidence Plan`

任务名称：

`Gate B — Raspberry Pi Runtime / Deployment Evidence Planning`

执行 Thread：

`Architecture / Integration`

结论：PASS WITH RECOMMENDATIONS

本报告是未来 runtime/deployment execution 的 planning authority，不是 Docker、Compose、Raspberry Pi、API、DB、rollback 或真实 Case A/B/C 的执行报告。下一次 runtime execution 必须先取得 PM 对本报告 exact allowlist 的独立批准，并按本报告 fail-closed 顺序执行。

## Scope

- reviewed files:
  - live Git baseline、当前 PM handoff、`docs/current_status.md`、Gate B compact status、Gate B Architecture plan、Reliability/Data Quality/Verification planning review stack、三份 implementation review；
  - `frontend/Dockerfile`、`frontend/.dockerignore`、Dashboard `/health` route/test、`docker-compose.yml`、`docs/deployment/raspberry_pi.md`；
  - `docs/contracts/dashboard_api_contract.md`、accepted-events schema/client/viewModel/page、accepted-events API/health、`007_accepted_station_event_visibility.sql`、accepted fact builder。
- created file:
  - `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`
- changed existing files:
  - none。
- explicitly not touched:
  - `docs/current_status.md`、PM handoff、PM operating rules、Gate B status/plan/review reports；
  - `frontend/Dockerfile`、`frontend/.dockerignore`、health route/test、`docker-compose.yml`、`docs/deployment/raspberry_pi.md`；
  - accepted-events consumer、API、DB migration/schema、Collector、Grafana、V-PLC、config、package/dependency files；
  - `.gitignore`、旧 reports/handoffs、Keynote artifacts、`frontend/.next/`、`frontend/node_modules/`、`frontend/next-env.d.ts`、`frontend/tsconfig.tsbuildinfo`。

本轮只进行了 read-only recovery、authority/code reading 和本报告创建；没有运行 tests、typecheck、Next build、Docker/Compose、SSH、Raspberry Pi、port/firewall、resource、DB/API/browser、rollback/cancellation 或 Git write。

## Recovery

- HEAD: `29f02599447e4510209cd0ad419f70539f034507` (`Add PM handoff after Gate B closeout`)
- origin/main: `29f02599447e4510209cd0ad419f70539f034507`
- ahead/behind: `0 0`
- cached diff: empty
- working-tree diff: `.gitignore` only；`git status --short --untracked-files=all` 另有已知 external/generated artifacts。
- external/generated artifacts:
  - `M .gitignore`；
  - `frontend/.next/`、`frontend/node_modules/`、`frontend/next-env.d.ts`、`frontend/tsconfig.tsbuildinfo`；
  - 历史 Dashboard runtime-evidence reports、旧 reports/handoffs、Keynote artifact。

这些 artifacts 不属于本任务，未删除、clean、restore、整理、broad-stage 或纳入本报告之外的任何文件。Gate B implementation/review commits 与当前 `HEAD`、授权边界和 excluded paths 无实质冲突。

当前已关闭但仅限 static/local evidence 的状态：

```text
Gate B static implementation: CLOSED / PASS WITH RECOMMENDATIONS
Reliability implementation review: CLOSED / PASS WITH RECOMMENDATIONS / no blocker
Data Quality implementation review: CLOSED / PASS WITH RECOMMENDATIONS / no blocker
Verification implementation review: CLOSED / PASS WITH RECOMMENDATIONS / no blocker
Docker image / Compose startup / ARM64 / Pi runtime / rollback / real Case A/B/C:
NOT EXECUTED / NOT CLAIMED
```

六个 Gate B implementation 文件是 changed-file scope，不是完整可构建 release。未来 release 必须从 live committed HEAD 提取完整 approved tracked frontend baseline；不得从 dirty working tree、未提交文件、generated artifacts 或 host `node_modules` / `.next` 构建。

## Approach comparison

| option | data/`.env` protection | rollback asset / release identity | Compose project/network/container identity | 操作复杂度 | first deployment / update / cancellation | 证据可复核性 | decision |
|---|---|---|---|---|---|---|---|
| A. 现有 `/opt/edge-mes-demo` 原地受保护更新 | 依靠 staging、显式 approved paths、永不 delete/覆盖 `data/`、remote `.env` | 需要 build 前冻结 old release、old image、resolved Compose 与 core baseline；可保留 `.rollback/<release_id>` | 最稳定：固定 working directory、现有 default network、`edge-mes-dashboard` container identity 与 Grafana `3000` 不变 | 最低；符合当前单机 Compose authority | Branch A 用旧资产 rollback；Branch B 只做 Dashboard cancellation；失败路径短 | manifest、checksums、container/image baseline 与 bounded logs 可直接对照 | **推荐 v1** |
| B. 版本化 release 目录 + `current` 指针/受控切换 | 版本目录天然保留旧文件；仍必须把 `data/`、`.env` 放在固定受保护位置 | 最强的文件级 rollback 与 identity；但须额外证明 project directory、相对 volume、network 与 container identity 未漂移 | 风险较高：切换工作目录/指针可能改变 Compose project、相对路径或 volume 解析；必须另做 identity proof | 中高；需要维护 pointer、路径绑定和双目录状态 | 更新 rollback 清晰；first deployment 仍需 cancellation；切换错误时更难判断 active release | 文件证据强，但 runtime identity 证据量更大 | 未来可评估，不作为 v1 默认 |
| C. 临时 remote build workspace + approved release 同步 | active `/opt/edge-mes-demo` 在 build 前保持不变；同步仍必须保护 `data/`、`.env` | build workspace 可保存 release/archive/image evidence；activation 前仍需冻结旧资产 | 临时 workspace 可能产生不同 Compose project/network/relative path；必须显式 identity proof，不能靠名称推断 | 中；transport 与 activation 分离，但命令更易越界 | 对已有 Dashboard 有安全 dry boundary；first deployment 取消路径仍需 active cleanup proof | build evidence 好，active runtime lineage 较复杂 | 作为未来 repair/large release option，不作为当前 v1 |

推荐 Option A，但采用“固定 active path + protected staging/archive + immutable release manifest”的受保护变体：active path 始终是 `/opt/edge-mes-demo`；旧 release files、rollback image tag/ID 和 evidence record 保存在不触碰 `data/`、remote `.env` 的受保护目录；不引入 registry、Kubernetes、CI/CD、签名系统或新基础设施。任何无法证明 active path、project/network/container identity 的切换都只能 `HOLD`。

## Planned execution sequence

执行主机固定为真正的 Raspberry Pi 5B Linux host；remote working directory 固定为 `/opt/edge-mes-demo`。本地 Mac 只负责从 committed `HEAD` 生成 release identity 和 transport artifact；不得用本地 build 结果替代 Pi native build。

### Phase A — release identity 与本地 release baseline

前置条件：PM 已批准 runtime execution；live `HEAD` 与 `origin/main` 已重新 read-only 核对；目标 release commit 是 committed `HEAD`；没有把 dirty `.gitignore` 或任何 untracked/generated artifact 纳入 release。

冻结的 release authority：

```text
source_commit = live `git rev-parse HEAD`
release_id = PM-approved ID bound to source_commit
tracked file list = committed approved frontend baseline only
per-file checksum = checksum of the file at source_commit
release archive checksum = checksum of archive produced from source_commit
transport timestamp = UTC/ISO-8601 timestamp at transport completion
remote landing path = /opt/edge-mes-demo
resolved Compose config checksum = remote resolved config evidence, stored outside repository
```

approved tracked baseline 至少包含：

```text
frontend/package.json
frontend/package-lock.json
frontend/next.config.ts
frontend/tsconfig.json
frontend/src/**
frontend/Dockerfile
frontend/.dockerignore
docker-compose.yml
docs/deployment/raspberry_pi.md
```

实际 release manifest 必须由 committed tree 生成，例如以 `git ls-tree -r --name-only <source_commit> -- <approved paths>` 取得路径、以 `git show <source_commit>:<path> | shasum -a 256` 取得 per-file checksum，并以 `git archive <source_commit> -- <approved paths> | shasum -a 256` 取得 archive checksum。这里只定义未来 command category；未取得 PM runtime authorization 前不得执行这些生成/transport commands。

PASS 条件：source commit、release ID、完整 tracked list、checksums、archive checksum 与 destination 绑定且无 dirty/generated file。

HOLD 条件：`HEAD` 不是 committed source authority、manifest 与 source commit 不一致、任何 required tracked file 缺失、checksum 无法重算、release ID 未绑定，或出现 `.env`、`.git`、host `node_modules`、host `.next`、macOS artifact、untracked report/handoff。

### Phase B — remote read-only 现状与 Branch A / Branch B 判定

前置条件：Phase A PASS；transport 尚未改变 active path；只允许 remote read-only inspection。

先保存 remote release/service baseline：当前 active release files、当前 `docker-compose.yml`、resolved Compose config、all service/container/image identity、`StartedAt`、`RestartCount`、health/running state、Docker project/network labels、port state，以及 `data/` 与 remote `.env` 的 protected-path identity/metadata。不得把 `.env` 内容写入 evidence 或 repository。

分支判定：

- Branch A（已有可运行上一版 Dashboard）：`edge-mes-dashboard` container/service、old image tag/ID、old release files、old compose config 和可复核 service/container baseline 全部存在且相互一致。缺一项不是 Branch B，而是 `HOLD`。
- Branch B（首次增加 Dashboard）：远端不存在上一版 Dashboard container、image/release asset；先冻结 core-service baseline、pre-deployment Compose/release backup、core container/image identity、health、3001 baseline、`data/` 与 remote `.env` protection proof。
- Ambiguous state：只有 image、只有停掉的 container、旧 files 与 image 不匹配、或无法判断是否可运行上一版时，停止并 `HOLD`，不得擅自按 first deployment 处理。

Branch A build 前必须保存：

```text
old source release ID
old frontend/release files
old docker-compose.yml
old resolved Compose config/checksum
old Dashboard image tag and image ID
old Dashboard container ID
old service/container/image baseline
old port 3001 state
```

Branch B 只允许建立 cancellation baseline；不得在终局把它称作 Dashboard rollback。

### Phase C — release transport 与 protected paths

前置条件：Phase B 判定完成且 required Branch A rollback assets 或 Branch B cancellation baseline 已通过；transport destination 仍为 `/opt/edge-mes-demo`。

transport 只把 approved release archive/manifest 先落到受保护的 remote staging path，再由受控的 approved-path activation 进入 active path。future transport command category 允许 `rsync` 或 `scp` 到 release staging，但禁止 destructive `--delete` 和 broad sync；SSH host/user/identity 由 PM 在仓库外提供，credential、token、password、remote `.env` 内容绝不写入 report/repository。

必须保护、不得覆盖或删除：

```text
/opt/edge-mes-demo/data/
/opt/edge-mes-demo/.env
既有数据库 volume / bind data
既有 rollback release/image
```

transport exclude 至少包含：

```text
data/
.env
.env.*
.git/
frontend/node_modules/
frontend/.next/
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
macOS build artifacts
__pycache__/
*.pyc
```

PASS 条件：remote landing path、transport timestamp、archive/checksum、approved file list 和 protected-path proof 一致；active `data/`、remote `.env`、DB volume、old rollback assets 的 identity/mtime/size/ownership 未发生非授权变化。

HOLD 条件：无法把 transport 限制到 approved paths、无法核对 landing checksum、需要覆盖 `.env`/`data/`、发现 archive 中有 host generated artifacts，或 transport 会删除/重建未知内容。

### Phase D — port `3001` listener / firewall preflight

前置条件：Phase C PASS；任何 build、Compose startup 或 release activation 前完成。Grafana `3000` 必须保持现有 identity。

bounded command/result record 必须至少覆盖：

```text
host port 3001 listener result
listener owner PID/process/container
Docker published-port state
actual available firewall tool and result: nft / ufw / iptables
Grafana port 3000 unchanged
pre-deployment 3001 baseline
```

建议 future record 使用固定的 read-only command categories：`ss -ltnp` 精确观察 `3001`、`docker ps`/`docker inspect` 解析 published port 与 owner、`command -v nft/ufw/iptables` 后只读取实际可用的 firewall rules/status；若 read privilege 不足，也按无法确认处理。

终端 gate：

```text
3001 已被未知 listener 占用 -> HOLD
listener owner PID/process/container 无法确认 -> HOLD
firewall boundary 无法确认 -> HOLD
不得停止、kill 或重配置未知 process/listener
不得改用其他 port
不得修改 Grafana 3000
```

first-deployment cancellation 后必须用同一 bounded template 固定记录 `3001 released / no listener`；无法得到固定 release evidence 时 cancellation 只能 `HOLD`。

### Phase E — DockerRootDir、filesystem、image/cache、memory/Swap preflight

前置条件：port/firewall PASS；Branch A rollback assets 或 Branch B cancellation backup 已冻结；build 尚未开始。

所有数值以 bytes 为 authority，human-readable 输出只能作为附录。记录：

```text
DockerRootDir
/opt/edge-mes-demo filesystem identity
DockerRootDir filesystem identity
same-filesystem boolean
filesystem total/free bytes for both paths
pre_image_usage_bytes
pre_buildkit_cache_bytes
current Dashboard image ID/size bytes
rollback Dashboard image ID/size bytes, or ABSENT
memory total/available/used bytes
Swap total/used bytes
two preflight Swap samples 30 seconds apart
```

bounded command/result template 必须使用 remote Linux 可取得的 raw bytes：DockerRootDir 由 `docker info --format '{{.DockerRootDir}}'`；filesystem total/free 由 `df -B1` 或等价 raw-byte output；filesystem identity 由 device/filesystem identity output；memory/Swap 由 `/proc/meminfo` 的 kB 数值乘 `1024` 后保存为 bytes；current/rollback image size 由 `docker image inspect --format '{{.Id}} {{.Size}}'`；image usage 与 BuildKit cache 必须使用可可靠解析为 bytes 的 Docker/BuildKit output。无法将 human-readable usage 可靠转换为 bytes 时，不得继续。

`pre_image_usage_bytes`、`post_image_usage_bytes`、`pre_buildkit_cache_bytes`、`post_buildkit_cache_bytes` 的 measurement 必须使用相同的 command/source、metric scope、unit、parser/accounting method、Docker daemon/context，并记录 relevant timestamps。Phase H 必须以相同 identity 重新取得 post values；任何 raw counter、unit、scope、parser/accounting identity、Docker context 或 relevant timestamp 无法可靠核对时，在 startup 前 `HOLD`。

先保存 raw counters 并计算 raw delta，写入 evidence record：

```text
raw_image_delta_bytes = post_image_usage_bytes - pre_image_usage_bytes
raw_cache_delta_bytes = post_buildkit_cache_bytes - pre_buildkit_cache_bytes
```

若任一 raw delta 小于 `0`，必须保留原始 pre/post bytes，记录可复核原因，并确认前后 command/source、scope、unit、parser/accounting method、Docker daemon/context 与 relevant timestamps 一致；无法解释或无法完成前后状态对账时，在 startup 前 `HOLD`。负值不得作为 capacity credit，不得用负 image delta 抵消 cache growth，也不得用负 cache delta 抵消 image growth。即使负 delta 有合理原因，terminal calculation 仍将对应 negative growth 视为 `0`。

用于 terminal gate 的保守 growth：

```text
effective_image_growth_bytes = max(0, raw_image_delta_bytes)
effective_cache_growth_bytes = max(0, raw_cache_delta_bytes)
combined_growth_bytes = effective_image_growth_bytes + effective_cache_growth_bytes
```

preflight gate：

```text
project filesystem free >= 6 GiB
DockerRootDir filesystem free >= 6 GiB
若存在 rollback image：DockerRootDir free >= max(6 GiB, 2 * rollback_image_size_bytes + 3 GiB)
required metric 无法读取或算式无法可靠完成 -> HOLD
两次相隔 30 秒的 preflight Swap used 持续增长 -> HOLD
```

同一 filesystem 只计算一次，但 record 必须明确写出 two paths same filesystem。不得运行 `docker system prune`、`docker builder prune`、image prune，不得删除 rollback image，不得用清理绕过门禁。

### Phase F — rollback assets 或 first-deployment cancellation baseline 冻结

Branch A 必须在 build 前拥有 source release ID、old release files、old Compose、resolved Compose checksum、old Dashboard image tag/ID、old container/service/image baseline、old `3001` state 和 protected-path proof。缺一项即 `HOLD`。

Branch B 必须在 build 前拥有 pre-deployment Compose/release backup、core service/container/image identity、core health/running state、`3001` baseline、`data/` 与 remote `.env` protection proof。终局只能是 `first-deployment cancellation / existing-core-services non-impact PASS` 或 `HOLD`，不得声明 Dashboard rollback PASS。

### Phase G — base image resolution 与 native ARM64 build

前置条件：A-F 全部 PASS；所有资源门禁通过；release manifest 与 remote active/staging checksum 已核对；Branch A rollback asset 已保留，或 Branch B cancellation baseline 已冻结。

只允许在 Raspberry Pi 原生 host 执行 Dashboard image build。必须记录：

```text
actual host architecture
actual Docker architecture
actual final image OS/architecture/variant == linux/arm64/v8
node:22.23.0-bookworm-slim resolved RepoDigest
resolved base image ID
source release ID
build start timestamp
build end timestamp
build exit code
bounded build log result
```

未来 build command category 是独立的 Dashboard-only image build（例如已冻结 release context 下的 `docker compose build`/等价 Dashboard-only build）；不得用 `docker compose up -d --build` 代替；不得 build other service。Build log 只能保留 bounded tail/time-window evidence，build exit code 必须从 build command 本身记录，不能从 log 文本推断。

ARM64 PASS 必须由 host、Docker、image 三层实际值共同证明。以下均不能推导 ARM64 PASS：lockfile 存在 ARM64 package、Docker Hub tag 声称支持 ARM64、本地 macOS build、Compose config PASS、Dockerfile static review PASS。

Build failure、timeout、OOM kill、non-zero exit 或 incomplete image 是 terminal stop：不得 startup，不得 fallback 到 host `node_modules`、host `.next`、macOS artifact、不同 Node image、localhost API origin、错误 origin profile、relative/browser origin、root runtime、temporary Dockerfile 或 temporary Compose override。

### Phase H — build postflight 与 image identity

前置条件：Phase G build exit `0` 且 final image inspect 完整；否则停止。

重新记录 Phase E 的所有 raw-byte metrics，以及：

```text
final edge-mes-dashboard:local image ID
final RepoTags
final image size bytes
post_image_usage_bytes
post_buildkit_cache_bytes
post filesystem free bytes
post memory/Swap bytes
```

必须使用 Phase E 冻结的同一 command/source、metric scope、unit、parser/accounting method、Docker daemon/context 和 relevant timestamp 规则取得 post counters，并保留原始 pre/post bytes、raw deltas 及前后状态对账记录。若任一 raw delta 小于 `0`，其原因无法复核、measurement identity 不一致或前后状态无法对账，则在 startup 前 `HOLD`；不得把负值计为 capacity credit 或抵消另一 counter 的正增长。

postflight gate：

```text
相关 filesystem free >= 3 GiB
final Dashboard image size <= 1 GiB
combined_growth_bytes <= 3 GiB
build 后等待 120 秒，Swap used 相对 build 前 baseline 增量 <= 256 MiB
两个相隔 30 秒的 post-build Swap sample 不得持续增长
任一 required metric 缺失或算式不可复核 -> HOLD
```

任何 postflight failure 都不得 startup；必须保留 old release/image/rollback assets，不得 prune/删除以绕过阈值。

### Phase I — Dashboard-only startup

前置条件：Phase H PASS；core service baseline 已保存；image ID、tag、architecture、origin/profile 的 identity 已记录。

启动只能使用独立 build 完成后的 Dashboard-only 命令：

```text
docker compose up -d --no-deps dashboard
```

不得使用 `docker compose down`、`docker compose up -d --build`、全量 service rebuild、volume recreate/delete、API/PostgreSQL/Collector/Grafana/V-PLC rebuild。启动前后必须对已冻结范围内的 existing core services 比较：container ID、image ID、`StartedAt`、`RestartCount`、health/running state、Compose project identity、network identity、container identity。core comparison 仅针对 existing core services；Dashboard 自身 container ID 变化不作为 core drift。

Dashboard-only startup 后，以下任一情况均为统一 fail-closed terminal：core service rebuilt、core service restarted、container ID changed、image ID changed、`StartedAt` changed、`RestartCount` increased、health/running state unexpectedly changed、Compose project identity changed、network identity changed、container identity changed、required comparison unavailable、comparison result incomplete、pre/post state cannot be reconciled，或其他 core status drift。此时：

```text
core-service non-impact = HOLD
current Dashboard startup evidence = HOLD
stop further runtime/data/case evidence
不得继续 Phase J-L/M/N；overall runtime/deployment evidence cannot PASS
不得尝试 restart、rebuild、recreate 或 repair core services
```

启动后同时记录容器实际 runtime values，但只保留所需字段：

```text
EDGE_MES_DASHBOARD_API_ORIGIN=http://api:8000
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=container
NODE_ENV=production
HOSTNAME=0.0.0.0
PORT=3000
```

不要 dump 全量 environment；不得泄漏其他 env、credential 或 secret。禁止 `NEXT_PUBLIC_*`、`localhost`、`127.0.0.1` API origin、host port `8000`、relative URL 或 browser-origin fallback。

### Phase J — 120-second process-health / restart terminal gate

前置条件：Dashboard-only startup command exit `0`；API failure drill 尚未开始；core baseline retained。

bounded observation 必须保存 Dashboard `Status`、`Health.Status`、`RestartCount`、`StartedAt`、image ID、bounded logs、120 秒 deadline 和 observation timestamps。统一 failure predicate：

```text
RestartCount >= 5 -> FAIL
持续 restarting -> FAIL
持续 unhealthy -> FAIL
120 秒未进入 healthy -> FAIL
crash-loop / log-loop / request-retry storm -> FAIL
```

这里以 `RestartCount >= 5` 为唯一 terminal wording，不使用模糊的“超过 5 次”。失败后必须显式执行：

```text
docker compose stop dashboard
```

并用固定 result record 证明：Dashboard 不再 `running`、不再 `restarting`、不再持续 `unhealthy`；bounded logs 停止增长；没有持续 API request/retry storm。stop command 或终局 evidence 失败时为 `HOLD`，不得继续 data/case evidence。

### Phase K — process health 与 API/data health 分离

独立保存以下 evidence，不互相替代：

```text
Dashboard /health -> Next HTTP process readiness only
API /health -> API + PostgreSQL readiness under current API health semantics
PostgreSQL readiness -> database readiness only
accepted-events API response -> accepted-fact API/data evidence
Dashboard /accepted-events page -> consumer render evidence
```

`Dashboard /health = 200` 不得声明 API ready、DB ready、accepted fact 存在、Case A/B/C 通过或 DB/API/Dashboard closed-loop PASS。`depends_on: service_started` 只能证明 Compose startup ordering。

API unavailable scenario 必须以独立、bounded、PM separately authorized 的 failure drill 规划；不创建通用 fault-injection platform，不修改 API。drill 期间必须证明：

```text
API stopped/unreachable
Dashboard /health remains healthy
accepted-events page fail closed
no stale production truth
same render does not retry
new browser/page request can recover after API restoration
API failure does not restart Dashboard process
```

若没有独立授权的受控 API-unavailable drill，API failure/no-retry/recovery 只能标记 `NOT VERIFIED`，不能纳入 runtime PASS。request count 必须来自 bounded request/log evidence；不能靠截图或“页面看起来正常”。

### Phase L — known-empty 与 pagination evidence

Known-empty 必须固定一个具名 bounded production accepted-fact scope，并在 PostgreSQL、API 与 Dashboard 使用完全相同的 `line_id/start_time/end_time/limit`。先保存仅针对 `production_accepted_station_event_fact` 的 bounded read-only PostgreSQL zero-row result；不得查询或 join legacy/raw/diagnostic source、使用 API mock/synthetic，或通过清空 DB、fixture、write、schema/migration/API/frontend/Collector change 制造 empty。随后独立保存同一 scope 的 request URL/parameters、API raw response 和 page result：

```text
PostgreSQL production_accepted_station_event_fact bounded read-only result == zero rows
API data.items == []
Dashboard 显示 explicit empty
无旧 table row
无旧 summary
无旧 NOK/detail evidence
无旧 trace reference
```

该 evidence 只声明这个具名 bounded production accepted-fact scope contains zero rows；不得扩大为 database、line、history 或 global empty claim。PostgreSQL query unavailable、wrong source、scope mismatch、nonzero row、API `data.items != []`、Dashboard 不为 explicit empty、保留 stale prior truth 或任一 scope record 不完整，均为 known-empty `HOLD`；overall runtime evidence 不得 `PASS`。

Pagination：page 1 使用 bounded `line_id/start_time/end_time/limit`，保存原始 `next_cursor` 与 page 1 `fact_key` set；page 2 原样传入 opaque cursor，并保持相同 `line_id/start_time/end_time/limit`，保存 page 2 `fact_key` set。必须验证 stable order（`event_ts`, `accepted_at`, `fact_key`）、无重复、无遗漏、每个 render 只发一次 request。应以同一 bounded DB read-only key set 作为遗漏/重复核对 authority；截图不充分。

任何 cursor 被修改、scope 参数变化、fact_key set 无法对齐、request count 无法证明或 UI 保留旧 truth，均为 `HOLD`。

### Phase M — real Case A/B/C

只有 Phase A-L 全部通过且 PM 另行批准 real evidence scope 后执行。每个 case 使用独立 bounded request，让目标 fact 成为 `items[0]`；声明范围仅限该 request 的目标第一项，不扩大到整页、整个 window 或整个 database。不得用 synthetic fixture、mock response、API-only fixture、Case B、cycle event 或 `station_nok` 替代另一个 case。

| case | required real fact | field predicate | availability / terminal |
|---|---|---|---|
| Case A | accepted `station_result` | `production_result=ok`；`nok_code=null`；`nok_origin=null`；三个 `nok_detail_* = null` | mandatory；无法取得真实且可隔离的 target-first-item -> HOLD |
| Case B | accepted `station_result` | `production_result=nok`；`nok_code` non-null；`nok_origin` non-null；`nok_detail_code`、`nok_detail_source_event_id`、`nok_detail_evidence_fact_key` 全为 null | mandatory；无法取得真实且可隔离的 target-first-item -> HOLD |
| Case C | accepted `station_nok` detail companion | `production_result=null`；`nok_code`、`nok_origin`、三个 `nok_detail_*` 全 non-null；`nok_detail_evidence_fact_key` 绑定 accepted upstream evidence fact | conditional；真实 row 不存在 -> `NOT AVAILABLE / NOT VERIFIED`；真实 row 存在但无法 target-first-item 或 relation proof 不通过 -> HOLD |

目标 discovery 只能使用 PostgreSQL read-only query 从 `production_accepted_station_event_fact` 找到真实 candidate，再用 API 支持的 bounded `line_id/start_time/end_time/limit/cursor` 复核；不得插入 fixture、修改 DB、join legacy/raw/diagnostic table 或用 current config 覆盖 historical fields。若 API 支持的 query 无法把 mandatory target 排到 `items[0]`，不得扩大 claim 或改用 unsupported filter。

Case C 仅在真实 `station_nok` row 不存在时为 `NOT AVAILABLE / NOT VERIFIED`。若真实 Case C row 存在，必须另外保存 named、bounded、read-only relation proof：令 `parent_fact_key = Case C.nok_detail_evidence_fact_key`，只在同一 `production_accepted_station_event_fact` 表以 `fact_key = parent_fact_key` 查询 parent。parent 必须恰好一行、`event_type=station_result` 且 `production_result=nok`。parent 与 Case C 必须相同的 `line_id`、`plc_id`、`station_id`、`cycle_counter`、`config_hash`；`unit_id` 与 `dmc` 按 null-safe same-subject 规则处理：仅当双方均 non-null 才比较且必须相等，绝不转换 null；`unit_id` 或 `dmc` 至少一项必须可比较且相等。两项均不可比较或任一可比较项不相等，均为 Case C `HOLD`。

真实 Case C 已存在时，relation query unavailable、`nok_detail_evidence_fact_key` 为 null、parent 缺失或多行、parent type/result 错误、identity mismatch 或 same-subject 无法证明，均为 Case C `HOLD`，不得写成 `NOT AVAILABLE / NOT VERIFIED`。此 proof 不引入 parent_event_id、plc_boot_id、cycle_id、detail_role、`nok_code`/`nok_origin` equality、relation graph、D7/D8 matrix、archive/forensics、global completeness、historical replay 或新 authority fields。

### Phase N — exact 22-field DB/API/Dashboard reconciliation

每一个可执行真实 case 都必须固定如下三层链路：

```text
PostgreSQL production_accepted_station_event_fact raw row
  -> API raw JSON exact 22-field item
  -> Dashboard visible mapping
```

主 identity 为 `fact_key`，并同时核对 `source_event_id`、`content_fingerprint`、`event_ts`、`accepted_at`。逐字段表必须包含：

| field | DB raw value | API raw JSON value | display rule | Dashboard visible value | PASS / FAIL |
|---|---|---|---|---|---|
| `line_id` |  |  |  |  |  |
| `plc_id` |  |  |  |  |  |
| `station_id` |  |  |  |  |  |
| `station_type` |  |  |  |  |  |
| `profile_id` |  |  |  |  |  |
| `config_hash` |  |  |  |  |  |
| `config_version` |  |  |  |  |  |
| `event_type` |  |  |  |  |  |
| `production_result` |  |  |  |  |  |
| `unit_id` |  |  |  |  |  |
| `dmc` |  |  |  |  |  |
| `cycle_counter` |  |  |  |  |  |
| `source_event_id` |  |  |  |  |  |
| `event_ts` |  |  |  |  |  |
| `accepted_at` |  |  |  |  |  |
| `fact_key` |  |  |  |  |  |
| `content_fingerprint` |  |  |  |  |  |
| `nok_code` |  |  |  |  |  |
| `nok_origin` |  |  |  |  |  |
| `nok_detail_code` |  |  |  |  |  |
| `nok_detail_source_event_id` |  |  |  |  |  |
| `nok_detail_evidence_fact_key` |  |  |  |  |  |

Rules：placeholder 不能写进 API raw JSON value；不得从 legacy/raw/diagnostic table 补值；不得用 current config 覆盖 historical `config_hash`/`config_version`；不得互换 `event_ts` 与 `accepted_at`；不得把 `station_nok` 当第二个 production result；不得从 Case B 推导 Case C；所有 cross-field closure 必须来自同一 target item。

Case C 的 parent relation proof 是与该 exact 22-field table 分离的 named bounded read-only record；不得向本表增加 parent 或 relation fields，也不得用 22-field item 对账替代 parent relation terminal。

### Phase O — rollback 或 first-deployment cancellation

#### Branch A：existing Dashboard rollback

前置条件：Phase B 已证明 required assets 完整；失败 terminal 已先 stop Dashboard；old release/image/baseline 仍在 protected storage。

冻结顺序：恢复上一版 frontend/release files 和 `docker-compose.yml`；恢复 old `edge-mes-dashboard` image identity/tag；执行 `docker compose config --quiet`；只使用 `docker compose up -d --no-deps --force-recreate dashboard`；验证 Dashboard `/health`；执行一次固定 bounded accepted-events request；比较冻结的 core service baseline：container ID、image ID、`StartedAt`、`RestartCount`、health/running state、Compose project identity、network identity、container identity 未变化；验证 `data/`、remote `.env` 未覆盖。

任何 required rollback asset、config result、health、bounded request、core comparison 或 protected-path proof 缺失 -> `HOLD`，不得声明 rollback PASS。

Rollback 后，若任一 core service rebuilt、restarted、发生 container ID/image ID/`StartedAt`/`RestartCount`/health/running state/Compose project identity/network identity/container identity drift，或 required comparison unavailable、comparison result incomplete、pre/post state cannot be reconciled，均为：

```text
Branch A rollback = HOLD
core-service non-impact not proven
overall runtime/deployment evidence cannot PASS
```

不得因为旧 Dashboard 恢复 healthy、容器名称相同或服务看起来可用而忽略 core drift；不得尝试 restart、rebuild、recreate 或 repair core services。

#### Branch B：first-deployment cancellation

冻结顺序：`docker compose stop dashboard`；`docker compose rm -sf dashboard`；恢复 pre-deployment Compose/release files；执行 `docker compose config --quiet`；确认不存在 `edge-mes-dashboard` container；确认 `3001` 不再监听；比较冻结的 core service baseline：container ID、image ID、`StartedAt`、`RestartCount`、health/running state、Compose project identity、network identity、container identity；验证 core health；确认 core services 未重建；确认 `data/` 与 remote `.env` 未覆盖、删除或重新初始化。

终局只能是：

```text
first-deployment cancellation / existing-core-services non-impact PASS
或 HOLD
```

Cancellation 后，若任一 core service rebuilt、restarted、发生 container ID/image ID/`StartedAt`/`RestartCount`/health/running state/Compose project identity/network identity/container identity drift，或 required comparison unavailable、comparison result incomplete、pre/post state cannot be reconciled，均为：

```text
first-deployment cancellation / existing-core-services non-impact = HOLD
core-service non-impact not proven
overall runtime/deployment evidence cannot PASS
```

不得声明 `existing-core-services non-impact PASS`；不得因为 core service 名称相同、容器重新恢复 healthy 或服务看起来可用而忽略 drift；不得尝试 restart、rebuild、recreate 或 repair core services。

不得声明 Dashboard rollback PASS、Dashboard `/health` PASS、accepted-events PASS 或 Case A/B/C PASS。两条路径都禁止 `docker compose down`、volume delete、image/cache prune、data restore、DB migration/rollback、停止未知 listener、修改 port/firewall 或其他 service rebuild。

### Phase P — final evidence classification 与 PASS/HOLD adjudication

低层 evidence 不得升级为高层结论：

| evidence | permitted claim | not permitted |
|---|---|---|
| focused unit test | synthetic / focused implementation evidence | runtime/process/data/real closure |
| TypeScript / Next build | local source/build evidence | Pi image/ARM64/runtime |
| `docker compose config` | static parsing evidence | image build/startup/health |
| resolved base digest / image inspect | image identity evidence | native build/run unless actual host/image arch also recorded |
| Dashboard `/health` | Dashboard Next HTTP process readiness | API/DB/fact/Case/three-layer PASS |
| API `/health` | API + DB readiness under current API health semantics | accepted fact exists or Dashboard page PASS |
| PostgreSQL raw row + API raw item + Dashboard mapping | real DB-backed three-layer evidence for the named target item/case | whole page/window/database closure without per-item evidence |
| missing real Case C row | `NOT AVAILABLE / NOT VERIFIED` | synthetic/mock/Case B substitution |
| extant Case C with unavailable/invalid parent relation proof | Case C `HOLD` | `NOT AVAILABLE / NOT VERIFIED` or Case C PASS |

`raw_image_delta_bytes` 或 `raw_cache_delta_bytes` 的负值、无法解释或无法完成前后状态对账，均为 startup 前 `HOLD`；任何 terminal calculation 只能使用两个非负 `effective_*_growth_bytes`，负值不得提供容量抵扣。

Overall mandatory core-service terminal：以下任一情况出现，overall runtime/deployment evidence 必须为 `HOLD`，不得 `PASS`：

```text
core-service rebuild
core-service restart
core-service identity drift
core status drift
core comparison unavailable or unreconciled
```

其中 core identity/status comparison 继续只针对已冻结的 existing core services；Dashboard 自身 container ID 变化不作为 core-service drift。名称相同、容器重新恢复 healthy 或服务看起来可用均不能替代 container/image/`StartedAt`/`RestartCount`/health/running、Compose project、network、container identity 的 pre/post proof。

未来一次完整 runtime/deployment PASS 只能在以下全部满足后按 scope 声明：release identity/transport protection、Branch A/B gate、3001/firewall、resource pre/postflight、native `linux/arm64/v8` image identity、Dashboard-only startup、120-second process terminal、runtime origin/profile、core non-impact、known-empty、pagination、mandatory Case A/B、Case C conditional classification（存在时含 parent relation proof）、exact 22-field reconciliation，以及适用的 rollback/cancellation terminal evidence。known-empty 或任一 mandatory phase 为 `HOLD`，overall 不得 `PASS`；Case C 缺失仅可为 `NOT AVAILABLE / NOT VERIFIED`，不能由此伪造 Case C PASS。

## Evidence authority

- static:
  - committed source tree、focused health test、TypeScript/Next local build、`docker compose config`；当前均只能保留既有 Gate B static/local classification。
- process:
  - Dashboard `/health`、container `Status`/`Health.Status`、`StartedAt`、`RestartCount`、bounded logs；只证明 process/runtime readiness。
- image identity:
  - actual Pi host/Docker/image architecture、`node:22.23.0-bookworm-slim` resolved RepoDigest/base image ID、final `edge-mes-dashboard:local` ID/RepoTags/size、build timestamps/exit code。
- API/DB:
  - API `/health`、PostgreSQL readiness、accepted-events API raw JSON、opaque cursor/page evidence；各自保持独立 semantics。
- real three-layer:
  - exact `production_accepted_station_event_fact` raw row、same `fact_key` API raw 22-field item、Dashboard visible mapping/display rule；每个 case 单独保存、逐字段 PASS/FAIL。
- NOT AVAILABLE:
  - real Case C `station_nok` row 不存在时写 `NOT AVAILABLE / NOT VERIFIED`；不得伪造 Case C closure。

## Future exact execution allowlist

下一次 runtime execution 只允许以下 categories；每条实际命令必须先被 PM 批准并落入对应 category。任何未被覆盖的 future command 在执行前回 PM。以下只列非敏感 command shape，不写 SSH identity、password、token、remote `.env` 或真实 credential。

### Allowed categories

1. local read-only release identity commands
   - `git status -sb`、`git rev-parse HEAD`、`git rev-parse origin/main`、ahead/behind、`git ls-tree`/`git ls-files`、committed-tree `git show`/`git archive` manifest/checksum commands。
   - 只读核对 `HEAD` source authority；不得使用 dirty file content。
2. remote read-only preflight commands
   - `date -Is`、`pwd`、`docker info`/`docker compose version`、`docker compose ps`/`docker compose config --quiet`、`docker compose images`、`docker inspect`、`docker image inspect`、`docker ps`、`ss -ltnp`、实际可用的 `nft`/`ufw`/`iptables` read-only output、raw-byte `df`/filesystem identity、`/proc/meminfo`、Docker disk/cache usage、protected-path metadata。
   - 只读查询；无法读取 required metric 或 firewall boundary 即 HOLD。
3. release transport commands
   - 仅 approved archive/manifest 到 remote staging/approved paths 的 `rsync` 或 `scp`；必须排除 `data/`、`.env*`、`.git/`、host generated artifacts，禁止 `--delete`、broad sync 和 credential 写入。
4. Dashboard-only image build commands
   - 已核对 release context 后的 Dashboard-only `docker compose build`/等价 single-service build；记录 base digest、architecture、exit code、timestamps、bounded logs。
   - 禁止 build other service、`docker compose up -d --build` 或 fallback artifacts。
5. image inspect commands
   - `docker image inspect`、`docker inspect`、`docker info` 的 bounded identity/architecture/size/RepoDigest/ID output。
6. Dashboard-only startup/stop/rm commands
   - `docker compose up -d --no-deps dashboard`；失败 terminal 的 `docker compose stop dashboard`；Branch B cancellation 的 `docker compose rm -sf dashboard`。
   - `docker compose rm -sf dashboard` 只能用于 Branch B first-deployment cancellation。Dashboard startup failure、health failure、restart failure、API failure 或普通 cleanup 的 terminal 只能使用 `docker compose stop dashboard`；不得自动升级为 container removal。其他 Dashboard container removal 需求必须 return to PM，并要求 separately authorized future command category；本次不创建该新 category。
7. bounded health/API/page requests
   - Dashboard `curl -fsS http://127.0.0.1:3001/health`、API `/health`、PostgreSQL readiness、bounded accepted-events API/page request、known-empty、pagination page 1/page 2；保存 URL scope、status、raw response 与 request count，不保存 secret。
   - API-unavailable drill 只有在 PM 另行批准 controlled failure scenario 后可执行；没有该授权时只能 NOT VERIFIED。
8. bounded PostgreSQL read-only queries
   - 仅 `production_accepted_station_event_fact` 的 schema/readiness/target-row/fact_key-set、known-empty zero-row 与 Case C parent relation 查询；使用 read-only transaction。Case C parent relation 查询只可用 `fact_key = Case C.nok_detail_evidence_fact_key` 在同表查询；不得 `INSERT`、`UPDATE`、`DELETE`、fixture、migration、restore、ACK/read_done mutation 或 legacy/raw/diagnostic join。
9. bounded logs
   - Dashboard `docker compose logs --tail <bounded>` / bounded `--since`、bounded API access/request evidence；不使用无界 follow，不把 log absence 当作 health/data PASS。
10. rollback commands
    - Branch A only：恢复 approved old files、恢复 old image tag/ID、`docker compose config --quiet`、`docker compose up -d --no-deps --force-recreate dashboard`、Dashboard health、one bounded accepted-events request、core/protected-path comparison。
    - core drift/restart/rebuild/unreconciled comparison 或 required comparison unavailable/incomplete -> `Branch A rollback = HOLD`；core-service non-impact not proven；overall runtime/deployment evidence cannot PASS；旧 Dashboard healthy 不得覆盖该 terminal。
11. first-deployment cancellation commands
    - Branch B only：`docker compose stop dashboard`、`docker compose rm -sf dashboard`、恢复 approved pre-deployment files、`docker compose config --quiet`、container/3001/core/data/`.env` non-impact evidence。
    - core drift/restart/rebuild/unreconciled comparison 或 required comparison unavailable/incomplete -> `first-deployment cancellation / existing-core-services non-impact = HOLD`；不得声明 existing-core-services non-impact PASS；overall runtime/deployment evidence cannot PASS。
12. final evidence collection commands
    - approved manifest/checksum、resolved Compose checksum、image/base identity、runtime env allowlisted fields、health/restart/log/port/resource bytes、case raw DB/API/UI records、rollback/cancellation terminal record、final PASS/HOLD classification。

### Forbidden list

```text
docker compose down
docker compose up -d --build（全量）
volume delete / recreate
DB migration / DB write / fixture insert / synthetic fact insert
data restore
image prune / cache prune / docker system prune / docker builder prune
停止未知 listener/process
修改 port
修改 firewall
修改 remote .env
覆盖、删除或重新初始化 data/
API / DB / Collector / Grafana / V-PLC rebuild
把 host node_modules、host .next、macOS artifact 复制到 release/image
localhost / 127.0.0.1 / relative / browser-origin API fallback
NEXT_PUBLIC_* origin
root runtime、temporary Dockerfile、temporary Compose override
package install 或 upgrade
implementation edit
stage / commit / push / tag
docker compose rm -sf dashboard outside Branch B first-deployment cancellation
任何未被 exact allowlist 覆盖的 future command
```

## Blockers

- none for this planning gate。
- 当前实现和现有 Gate B review stack 没有发现必须在本轮修复的 false-PASS、data overwrite、core-service impact、rollback/cancellation impossibility、ARM64 evidence impossibility 或 three-layer authority blocker。
- Docker image、Compose startup、Pi resource/port、runtime/API/DB、real Case A/B/C 和 rollback/cancellation 仍是未来 execution gates，不能写成当前 PASS。

## Recommendations

1. `docs/deployment/raspberry_pi.md` 仍保留历史通用 `docker compose up -d --build`、`docker compose down`、migration 和全栈运维命令；当前 Section 10 的 Dashboard-only boundary 足以让本 planning report fail closed，但建议 PM 在 future docs-repair lane 中把 Section 10.7 拆成 separate build 与 `docker compose up -d --no-deps dashboard` startup，并把 bytes/result templates、`RestartCount >= 5`、post-cancellation port record 和 rollback request record 写入该指南。此项是 future repair candidate，不是本轮直接修改授权。
2. 在 runtime execution 前由 PM 冻结 remote shell、SSH transport、release ID、bounded timeout/log limits、raw-byte Docker/BuildKit metric parser 和 API-unavailable drill authorization；本报告不保存 credential。
3. Reliability focused planning review 应独立复核 Phase D/E/G/J/O 的 terminal predicates、protected-path proof、bytes calculations 和 `RestartCount >= 5` wording。
4. Data Quality focused planning review 应独立复核 Phase L-N 的 known-empty/pagination、Case A/B/C availability、fact-key identity、exact 22-field table、raw/display separation 与 no-fallback rules。
5. Verification focused planning review 应独立复核 exact future command allowlist、Branch A/B terminal classification、request count/no-retry evidence、core non-impact comparison、evidence hierarchy 和 forbidden list。

## Next gate

- eligible for:
  - Reliability focused planning review。
- PM approval required before:
  - Data Quality/Verification planning reviews（按 PM sequence）；
  - any implementation edit or docs/deployment repair；
  - Docker/Compose command、image build/start/stop/rm、SSH、Raspberry Pi、port/firewall/resource inspection；
  - API-unavailable drill、PostgreSQL query、real Case A/B/C、rollback/cancellation；
  - stage、commit、push、tag、deploy 或 rollback execution。

## Thread 输出 / 上下文评估

- 本次输出长度：长；详细 planning 已写入 `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`，窗口只保留结论、关键设计、blockers、recommendations 和 next gate。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：本任务是新的 Level 2 runtime/deployment planning branch；下一步是独立 Reliability focused planning review，必须与当前 Architecture planning、已关闭 static implementation、完整 Dashboard UI/UX 和旧 Dashboard URL Option C/strong-audit branch 保持隔离。
