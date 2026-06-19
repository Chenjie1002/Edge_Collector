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
