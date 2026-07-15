# Raspberry Pi 部署与运维

更新时间：2026-06-19  
部署目标：Raspberry Pi 5B，Docker Compose，单机离线 Edge MES Demo。

> **安全要求：SSH 密码、私钥、Token、数据库生产密码及其他敏感凭据不得写入本仓库。**
>
> SSH 主机、用户和认证方式由运维人员在执行部署时单独提供。本文只记录非敏感的部署
> 路径、命令和验收方法。

## 1. 部署路径

树莓派项目目录已通过容器的
`com.docker.compose.project.working_dir` 标签和远程 compose 文件位置确认：

```text
/opt/edge-mes-demo
```

Compose 文件：

```text
/opt/edge-mes-demo/docker-compose.yml
```

后续所有远程检查、部署、migration、日志和回滚操作均以
`/opt/edge-mes-demo` 为工作目录，不使用 `/home/pi/edge-mes-demo`。

持久化数据位于项目目录下：

```text
/opt/edge-mes-demo/data/postgres
/opt/edge-mes-demo/data/grafana
/opt/edge-mes-demo/data/prometheus
/opt/edge-mes-demo/data/vplc
```

更新或回滚时不得删除、覆盖或重新初始化 `data/`。

## 2. 服务启动方式

进入部署目录：

```bash
cd /opt/edge-mes-demo
```

首次启动或需要重建镜像：

```bash
docker compose up -d --build
```

普通启动：

```bash
docker compose up -d
```

停止服务但保留容器和数据：

```bash
docker compose stop
```

停止并删除容器、保留持久化目录：

```bash
docker compose down
```

默认 V-PLC 使用 `normal` Profile。快速演示必须显式指定：

```bash
VPLC_PROFILE=fast docker compose up -d --build s7-plc-sim
```

## 3. Docker Compose 常用命令

查看服务状态：

```bash
docker compose ps
```

查看解析后的 Compose 配置：

```bash
docker compose config
```

重建全部服务：

```bash
docker compose up -d --build
```

仅重建 Reliability 相关服务：

```bash
docker compose up -d --build s7-plc-sim collector
```

重启指定服务：

```bash
docker compose restart s7-plc-sim collector api
```

查看容器资源占用：

```bash
docker stats --no-stream
```

## 4. 常用健康检查

### 容器状态

```bash
cd /opt/edge-mes-demo
docker compose ps
docker inspect --format '{{.Name}} {{.State.Status}} {{if .State.Health}}{{.State.Health.Status}}{{end}}' \
  $(docker compose ps -q)
```

### API

```bash
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/trace/api/recent
```

### V-PLC

```bash
curl -fsS http://127.0.0.1:8200/health
curl -fsS http://127.0.0.1:8200/vplc/state
```

重点确认：

- `profile` 为预期值。
- 正常部署时 `scale=1.0`。
- WS01/WS02/WS03 的 `base_cycle_s` 约为 30 秒。
- `config_hash` 非空。
- `require_ack=true`。

### Simulator、Grafana、Prometheus

```bash
curl -fsS http://127.0.0.1:8100/health
curl -fsS http://127.0.0.1:3000/api/health
curl -fsS http://127.0.0.1:9090/-/healthy
```

### PostgreSQL

```bash
docker exec edge-mes-postgres \
  pg_isready -U edge_mes -d edge_mes

docker exec edge-mes-postgres \
  psql -U edge_mes -d edge_mes -c 'SELECT now();'
```

检查核心表：

```bash
docker exec edge-mes-postgres \
  psql -U edge_mes -d edge_mes -c \
  "SELECT to_regclass('public.cycle_event'),
          to_regclass('public.collector_error_log'),
          to_regclass('public.vplc_parameter_change_log'),
          to_regclass('public.vplc_parameter_snapshot');"
```

## 5. 日志查看

查看全部服务最近日志：

```bash
docker compose logs --tail 100
```

持续跟踪 Reliability 相关日志：

```bash
docker compose logs -f --tail 100 s7-plc-sim collector
```

分别查看：

```bash
docker logs --tail 200 edge-mes-s7-plc-sim
docker logs --tail 200 edge-mes-collector
docker logs --tail 200 edge-mes-api
docker logs --tail 200 edge-mes-postgres
docker logs --tail 200 edge-mes-grafana
```

按时间范围查看：

```bash
docker logs --since 30m edge-mes-s7-plc-sim
docker logs --since 30m edge-mes-collector
```

## 6. 更新部署流程

### 6.1 更新前

```bash
cd /opt/edge-mes-demo
docker compose ps
docker compose config --quiet
docker compose logs --tail 50 s7-plc-sim collector
```

记录当前版本或发布包标识，并备份非敏感配置。不要把服务器上的 `.env`、SSH 文件或
其他凭据复制回仓库。

建议先备份数据库：

```bash
mkdir -p /opt/edge-mes-backups
docker exec edge-mes-postgres \
  pg_dump -U edge_mes -d edge_mes -Fc \
  > /opt/edge-mes-backups/edge_mes-before-update.dump
```

### 6.2 更新文件

将经过本机测试的项目文件同步到：

```text
/opt/edge-mes-demo
```

同步时必须排除：

```text
data/
.env
__pycache__/
*.pyc
.git/
```

SSH 连接方式由用户单独提供后，再确定具体使用 `rsync`、`scp` 或其他发布方式。

### 6.3 执行数据库 migration

现有部署升级 Reliability 功能时执行：

```bash
cd /opt/edge-mes-demo

docker exec -i edge-mes-postgres \
  psql -U edge_mes -d edge_mes \
  < db/migrations/005_reliability_schema.sql

docker exec -i edge-mes-postgres \
  psql -U edge_mes -d edge_mes \
  < db/migrations/006_vplc_parameter_audit.sql
```

Migration 失败时停止更新，不要继续重建业务服务。

### 6.4 重建服务

```bash
docker compose up -d --build s7-plc-sim collector api
docker compose ps
```

如果公共配置、Dashboard 或其他服务也有变化：

```bash
docker compose up -d --build
```

### 6.5 更新后检查

```bash
curl -fsS http://127.0.0.1:8200/vplc/state
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:3000/api/health
docker compose logs --tail 100 s7-plc-sim collector api
```

## 7. 回滚建议

### 代码与镜像回滚

- 每次部署前保留上一份可运行发布目录或明确的 Git commit/tag。
- 不要在原目录内进行不可逆覆盖；推荐以发布包或版本目录保存上一版本。
- 回滚代码后重新构建对应服务：

  ```bash
  cd /opt/edge-mes-demo
  docker compose up -d --build s7-plc-sim collector api
  ```

### 数据库回滚

- Schema migration 应优先保持向后兼容。
- 不建议直接删除新列或新表。
- 如 migration 导致服务不可用，先回滚应用版本；数据库保留新增结构通常比逆向删除更安全。
- 只有在确认必须恢复数据库时，才从更新前的 `pg_dump` 备份恢复。
- 数据库恢复会覆盖更新后的业务数据，执行前必须再次确认影响范围。

### 配置回滚

- 保留上一版非敏感配置文件。
- 服务器 `.env` 单独备份和管理，不进入仓库。
- 回滚后运行 `docker compose config --quiet`，再启动服务。

## 8. 验证 Checklist

### 部署基础

- [ ] 当前目录为 `/opt/edge-mes-demo`。
- [ ] `docker compose config --quiet` 通过。
- [ ] 所有目标容器为 `running`，PostgreSQL 为 `healthy`。
- [ ] `data/` 持久化目录未被覆盖或删除。

### 数据库

- [ ] PostgreSQL `pg_isready` 通过。
- [ ] `005_reliability_schema.sql` 已成功执行。
- [ ] `006_vplc_parameter_audit.sql` 已成功执行。
- [ ] `cycle_event`、`collector_error_log`、`vplc_parameter_change_log` 和
      `vplc_parameter_snapshot` 均存在。

### V-PLC 与 Cycle Time

- [ ] `/vplc/state` 返回成功。
- [ ] 默认 `profile=normal`、`scale=1.0`。
- [ ] 三站基准节拍约为 30 秒。
- [ ] normal Profile 修改 `base_cycle_s=1` 被拒绝并写入参数审计。
- [ ] V-PLC 重启后产生新的 `plc_boot_id`。
- [ ] startup snapshot 包含 profile、config hash 和 boot ID。

### Reliability

- [ ] DB104 boot ID 在同一进程运行期间稳定。
- [ ] 停止 Collector 超过 ACK deadline 后 payload 仍保留，`ack_timeout=true`。
- [ ] Collector 恢复后同一 cycle 不重复，并最终变为 `ACK_OK`。
- [ ] ACK 写回失败时记录 `ACK_WRITE_FAILED` 并能够自动重试。
- [ ] 同 boot counter 下降时记录 `PLC_COUNTER_RESET`，且不 ACK。

### API 与可视化

- [ ] API `/health` 正常。
- [ ] Trace API 可返回最近三工站事件。
- [ ] Grafana `/api/health` 正常。
- [ ] Prometheus `/-/healthy` 正常。
- [ ] Dashboard 的三工站 Cycle Time 恢复到预期范围。

### 日志

- [ ] V-PLC 日志无持续启动失败或配置解析错误。
- [ ] Collector 日志无持续连接、identity、存储或 ACK 错误。
- [ ] PostgreSQL 日志无 migration 或磁盘错误。

## 9. SSH 凭据管理

以下内容不得写入本仓库、Markdown 文档、Git commit、Issue 或日志：

- SSH 密码。
- SSH 私钥及其内容。
- 私钥口令。
- Token、API Key。
- 含真实敏感密码的 `.env`。
- 可直接登录服务器的完整凭据组合。

仓库中只允许记录非敏感信息，例如部署路径、服务名、端口和通用运维命令。SSH
连接方式应通过仓库外的安全渠道单独提供，并只用于当前授权的远程操作。

## 10. Gate B：Dashboard Raspberry Pi Docker 集成

本节只定义未来获得 PM 明确授权后的 Dashboard Docker build、部署、回滚和真实
accepted-fact 证据流程。它不表示本地实现阶段已经执行 Docker build、Linux ARM64、
Raspberry Pi、Compose startup、rollback 或 Case A/B/C。

### 10.1 部署拓扑与 process health 边界

冻结拓扑：

```text
browser
  -> http://<Raspberry-Pi-IP>:3001
  -> edge-mes-dashboard (container port 3000)
  -> Dashboard server-side http://api:8000
  -> API
  -> PostgreSQL

Grafana
  -> host port 3000 unchanged
```

浏览器只访问 Raspberry Pi 的 host port `3001`，不得解析或直接访问 Compose service
DNS `api`。`http://api:8000` 只由 Dashboard server-side 使用。

Dashboard 容器的 `/health` 只证明 Next HTTP process readiness。它不证明：

```text
API readiness
PostgreSQL readiness
accepted fact 存在
Case A/B/C 闭环
DB/API/Dashboard 三层闭环
```

API 停止、未 ready 或故障时，Dashboard process 仍应保持 `healthy`。accepted-events
页面必须 fail closed；同一次 render 不 retry、不 fallback、不保留 stale production
truth。API 恢复后，只能由新的 page request 重新请求。

### 10.2 Gate B release changed-path scope 与发布保护

本 Gate 的 changed-file scope 精确为：

```text
frontend/Dockerfile
frontend/.dockerignore
frontend/src/app/health/route.ts
frontend/src/app/health/__tests__/route.test.ts
docker-compose.yml
docs/deployment/raspberry_pi.md
```

这六个路径只描述本 Gate 的变更集合，不表示远端构建可以删除、遗漏或忽略既有 tracked
frontend baseline。发布包或版本目录必须仍包含 Docker build 所需的完整、经批准的
tracked source baseline，例如 `frontend/package.json`、`frontend/package-lock.json`、
`frontend/next.config.ts`、`frontend/tsconfig.json` 和 `frontend/src/`。

发布 transport 必须保护并排除：

```text
data/
remote .env
.git/
frontend/node_modules/
frontend/.next/
frontend/tsconfig.tsbuildinfo
frontend/next-env.d.ts
__pycache__/
*.pyc
```

不得使用可能覆盖 `data/` 或远端 `.env` 的 destructive sync。不得把 host
`node_modules`、host `.next`、macOS build artifacts 或本地 `.env` 复制到远端或镜像。

### 10.3 Base image、架构与 image identity evidence

未来 Docker/runtime gate 必须保存以下实际证据，不得用 tag 名称或静态计划替代：

```text
node:22.23.0-bookworm-slim resolved RepoDigest / base image ID
actual linux/arm64/v8 architecture
edge-mes-dashboard:local final image ID
final image size
source release ID / commit
resolved Compose baseline
```

本地六文件实现阶段不得填写虚构 digest、image ID、size 或 ARM64 PASS。只有真实 Pi
build/run 后才能声明相关结果。

### 10.4 Host port 3001 listener 与 firewall preflight

在复制 release 或 build 前，记录 bounded listener/firewall preflight：

```bash
cd /opt/edge-mes-demo

date -Is
ss -ltnp

if command -v nft >/dev/null 2>&1; then
  sudo nft list ruleset
fi

if command -v ufw >/dev/null 2>&1; then
  sudo ufw status
fi

if command -v iptables >/dev/null 2>&1; then
  sudo iptables -S
fi
```

不假设 `nft`、`ufw`、`iptables` 全部存在；必须记录实际可用工具和命令结果。

冻结终局：

```text
发现 host port 3001 已有 listener -> HOLD，回 PM
无法确认 3001 listener/firewall 边界 -> HOLD
不得现场改成其他 port
不得停止、kill 或重配置未知 listener
```

Repository 中没有静态端口冲突不等于 Pi host preflight PASS。

### 10.5 Build 前 resource preflight

在任何 Dashboard build 前，记录 release 和 rollback identity，并运行：

```bash
cd /opt/edge-mes-demo

release_id=<PM-approved-release-id>
docker_root=$(docker info --format '{{.DockerRootDir}}')
printf 'DockerRootDir=%s\n' "$docker_root"

docker system df
docker builder du

if docker image inspect edge-mes-dashboard:local \
  --format 'CURRENT {{.Id}} {{.Size}}'; then
  :
else
  printf 'CURRENT_DASHBOARD_IMAGE ABSENT\n'
fi

if docker image inspect "edge-mes-dashboard:rollback-${release_id}" \
  --format 'ROLLBACK {{.Id}} {{.Size}}'; then
  :
else
  printf 'ROLLBACK_DASHBOARD_IMAGE ABSENT\n'
fi

df -h /opt/edge-mes-demo
df -h "$docker_root"
free -h
swapon --show

printf '%s\n' '--- memory/swap sample 1 ---'
date -Is
free -h
swapon --show
sleep 30
printf '%s\n' '--- memory/swap sample 2 ---'
date -Is
free -h
swapon --show
```

`swapon --show` 明确返回无已配置 Swap 时，应记录为 `none`；命令或 required metric
无法读取时为 `HOLD`，不得把“未知”当作零。

Build 前门禁：

```text
/opt/edge-mes-demo 所在 filesystem至少6 GiB free
DockerRootDir所在filesystem至少6 GiB free

存在rollback image时，DockerRootDir required free：
max(6 GiB, 2 × rollback image size + 3 GiB)

两个间隔30秒的preflight sample中Swap持续增长 -> HOLD
required metric无法读取 -> HOLD
需要旧Dashboard rollback但required rollback assets缺失 -> HOLD
```

若 Docker root 与 `/opt/edge-mes-demo` 位于同一 filesystem，只计算一次，但记录中必须
明确二者相同。

已有上一版 Dashboard 时，build 前还必须保存：

```text
source release ID / commit
old release files
old Dashboard image tag / ID
resolved Compose baseline
service / container baseline
```

### 10.6 Build fail-closed 与 deploy 前 postflight

未来 build 使用 PM 授权的 Dashboard build 命令。发生任一情况：

```text
docker compose build dashboard失败
timeout
OOM kill
incomplete image
```

必须立即停止，并遵守：

```text
不得docker compose up
不得使用host node_modules
不得使用host .next
不得使用macOS artifact
不得改变origin/profile
不得更换Node image绕过
不得取消non-root运行边界
不得自动docker system prune或docker builder prune
不得删除rollback image
```

Build 成功后、启动新 Dashboard 前，重新运行 Section 10.5 的资源命令，记录新
Dashboard image ID/size 与 BuildKit cache 增量；再等待 120 秒并执行两个间隔 30 秒的
memory/Swap samples。

Postflight 必须同时满足：

```text
相关filesystem至少3 GiB free
new Dashboard image + BuildKit cache增长不超过3 GiB
Dashboard final image不超过1 GiB
等待120秒后Swap相对build前baseline增长不超过256 MiB
两个间隔30秒的postflight samples中Swap不继续增长
```

任一条件失败：

```text
不得启动新Dashboard
保留旧release/image与rollback assets
HOLD并回PM
不得用自动cleanup绕过阈值
```

### 10.7 Dashboard-only update 与 startup/restart terminal gate

唯一 Dashboard-only update 路径：

```bash
cd /opt/edge-mes-demo
docker compose up -d --build --no-deps dashboard
```

以下命令不是 Dashboard-only update：

```bash
docker compose up -d --build
docker compose down
```

Section 2、3、6 中保留的全量 Compose 命令属于既有通用运维流程，不得在 Gate B
Dashboard-only release 中使用。Dashboard-only update 不得主动重建或重启：

```text
API
PostgreSQL
Collector
Grafana
V-PLC
Simulator
Prometheus
其他core services
```

启动后最多等待 120 秒进入 `healthy`。在 bounded 观察窗口内记录：

```bash
docker compose ps dashboard
docker inspect edge-mes-dashboard \
  --format 'status={{.State.Status}} restart_count={{.RestartCount}} health={{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}} image={{.Image}}'
docker compose logs --tail 200 dashboard
```

日志必须使用 bounded `--tail` 或 bounded `--since`，不得无界跟踪。

任一条件为失败：

```text
超过5次restart
持续restarting
持续unhealthy
120秒未healthy
持续crash-loop、log-loop或request/retry storm
```

失败后执行：

```bash
docker compose stop dashboard
```

然后必须证明 Dashboard 不再处于：

```text
running
restarting
持续unhealthy
```

`depends_on: service_started` 只表示启动顺序，不是 API readiness 证明。Dashboard
healthcheck 只能访问容器本地 `http://127.0.0.1:3000/health`，不得访问 API、DB 或
accepted facts。

### 10.8 Rollback 与首次部署取消

#### 10.8.1 已有上一版 Dashboard

部署前必须具有 Section 10.5 列出的完整 rollback assets。失败时先恢复上一版
`docker-compose.yml` 与 frontend release files，再恢复旧 image identity：

```bash
cd /opt/edge-mes-demo
docker image tag "edge-mes-dashboard:rollback-${release_id}" edge-mes-dashboard:local
docker compose config --quiet
docker compose up -d --no-deps --force-recreate dashboard
docker compose ps dashboard
curl -fsS http://127.0.0.1:3001/health
```

Rollback 后还必须执行一次 bounded accepted-events page request，并验证：

```text
Dashboard /health通过
一次bounded accepted-events request符合fail-closed或ready合同
API/PostgreSQL/Collector/V-PLC未被重建
其他core services未被重建
remote data/未被覆盖
remote .env未被覆盖
```

缺少旧 release files、old image tag/ID、resolved Compose baseline、service/container
baseline 或 post-rollback evidence 时为 `HOLD`，不得声明 rollback PASS。

#### 10.8.2 首次部署且无上一版 Dashboard

终局名称只能是：

```text
first-deployment cancellation / existing-core-services non-impact validation
```

失败后：

```bash
cd /opt/edge-mes-demo
docker compose stop dashboard
docker compose rm -sf dashboard
```

随后恢复部署前 Compose/release files，并验证：

```bash
docker compose config --quiet
```

必须证明：

```text
无edge-mes-dashboard container
host port 3001不再监听
core service/container/image状态与部署前baseline一致
核心service health符合部署前基线
API/PostgreSQL/Collector/Grafana/V-PLC未被重建
其他core services未被重建
remote data/未覆盖或重新初始化
remote .env未覆盖或重新初始化
```

该路径不存在可恢复的旧 Dashboard，因此不得声称：

```text
Dashboard rollback PASS
Dashboard /health PASS
accepted-events page PASS
```

两条路径都禁止：

```text
docker compose down
volume delete
image prune
data restore
DB migration rollback
其他service rebuild
```

### 10.9 Real Case A/B/C 三层 evidence boundary

只有 PM 单独授权真实 Raspberry Pi runtime evidence 后，才能执行以下 case：

```text
Case A — mandatory:
real accepted station_result / production_result=ok

Case B — mandatory:
real accepted station_result / production_result=nok

Case C — conditional:
real accepted station_nok detail companion
```

真实 Case C 不存在时，必须记录：

```text
NOT AVAILABLE / NOT VERIFIED
```

不得用 synthetic fixture、mock、API-only fixture、Case B 或 cycle event 替代 Case C。
不得用 cycle event 替代 Case A，也不得用 `station_nok` 替代 Case B。

每个 case 必须完成：

```text
PostgreSQL production_accepted_station_event_fact raw row
-> API raw JSON exact 22 fields
-> Dashboard visible/display rule
```

使用以下字段完成身份核对：

```text
fact_key
source_event_id
content_fingerprint
event_ts
accepted_at
```

每个 case 使用独立 bounded query，使目标 fact 成为 API response 的 `items[0]`。只可声明
该目标第一项闭环，不得把第一项 evidence 扩大为整页全部 rows 的三层闭环。

Exact 22 fields：

```text
line_id
plc_id
station_id
station_type
profile_id
config_hash
config_version
event_type
production_result
unit_id
dmc
cycle_counter
source_event_id
event_ts
accepted_at
fact_key
content_fingerprint
nok_code
nok_origin
nok_detail_code
nok_detail_source_event_id
nok_detail_evidence_fact_key
```

每个 case 的逐字段表必须包含全部 22 行，并使用以下列：

| field | DB raw value | API raw JSON value | display rule | Dashboard visible value | PASS/FAIL |
| --- | --- | --- | --- | --- | --- |
| `<one of the exact 22 fields>` | `<raw DB value>` | `<raw API value>` | `<frozen display rule>` | `<visible value>` | `<PASS or FAIL>` |

Display placeholder 不得写入 API raw JSON value 列。Dashboard process `/health`、API
`/health`、Docker image、截图、synthetic fixture、mock response 或 API-only evidence
均不能替代真实三层 evidence。
