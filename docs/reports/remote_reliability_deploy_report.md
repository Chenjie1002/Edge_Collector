# Remote Reliability Deployment Report

日期：2026-06-19  
目标主机：Raspberry Pi `Pi-5b-Li`  
结果：`PASS`，已恢复并保持 `normal` Profile。

## 1. 实际远程路径

部署目录：

```text
/opt/edge-mes-demo
```

Compose 文件：

```text
/opt/edge-mes-demo/docker-compose.yml
```

远程目录不是 Git 仓库，本次未使用 `git pull`、`git checkout` 或其他 Git 部署方式。

## 2. 部署方式

本次采用定向发布包部署：

1. 从本地工作树生成只包含 Reliability 相关文件的压缩包。
2. 排除 `.env`、`data/`、`.git`、`.venv`、`__pycache__` 和 `*.pyc`。
3. 上传到远程用户目录。
4. 解压覆盖 `/opt/edge-mes-demo` 中对应代码、配置、migration 和文档。
5. 执行 migration。
6. 仅重建 `s7-plc-sim` 与 `collector`。

发布包：

```text
edge-mes-reliability-release-20260619.tar.gz
```

SHA-256：

```text
0e3c3fa593b027ae31aad7c6356c020b346dbfe0fe15fbc7be083759b5e7343b
```

远程校验值与本地一致。

## 3. 备份内容

部署前备份：

```text
/home/mari/edge-mes-backups/edge-mes-demo-20260619-095457.tar.gz
```

大小约 3.6 MB。

备份包括：

- `docker-compose.yml`
- `s7_plc_sim/`
- `collector/`
- `config/`
- `db/`
- `docs/`
- `scripts/`
- `README.md`
- `.env.example`

备份不包含持久化 `data/`。

远程 `.env` 未被发布包包含。更新前后 SHA-256 相同：

```text
2f4a860abb23fe452bcb588788d852d0c6a3e7532df0b866f73a3b35d3f6f14c
```

`data/` 目录更新前后目录计数及可读容量标记相同。PostgreSQL、Grafana 和
Prometheus 持久化目录未被覆盖或删除。

## 4. 同步文件

### 服务代码

- `s7_plc_sim/`
- `collector/`

### 配置

- `docker-compose.yml`
- `config/app.yaml`
- `config/mapping.yaml`
- `config/vplc.yaml`

### Schema 与 migration

- `db/init/003_event_schema.sql`
- `db/init/005_vplc_parameter_audit.sql`
- `db/migrations/005_reliability_schema.sql`
- `db/migrations/006_vplc_parameter_audit.sql`

### 校验与文档

- `scripts/validate_edge_mapping.py`
- `docs/contracts/`
- `docs/deployment/`
- Reliability reports、handoff、protocol、status 和文档索引
- `README.md`
- `.env.example`

API 代码和 Grafana provisioning 本次没有修改，因此未同步对应服务代码或
Dashboard JSON。

## 5. Migration

已执行：

```bash
docker exec -i edge-mes-postgres \
  psql -v ON_ERROR_STOP=1 -U edge_mes -d edge_mes \
  < db/migrations/005_reliability_schema.sql

docker exec -i edge-mes-postgres \
  psql -v ON_ERROR_STOP=1 -U edge_mes -d edge_mes \
  < db/migrations/006_vplc_parameter_audit.sql
```

结果：

- `005_reliability_schema.sql`：`COMMIT`
- `006_vplc_parameter_audit.sql`：`COMMIT`
- `vplc_parameter_change_log`：存在
- `vplc_parameter_snapshot`：存在

## 6. 重建服务

已执行：

```bash
docker compose build s7-plc-sim collector
docker compose up -d s7-plc-sim collector
```

实际重建：

- `edge-mes-s7-plc-sim`
- `edge-mes-collector`

未重建：

- API：本次无 API 代码变更。
- Grafana：本次无 provisioning 或 Dashboard JSON 变更。
- PostgreSQL：保持运行和 healthy。
- Simulator、Prometheus、node-exporter、sync-worker：无相关变更。

## 7. 验证结果

### 7.1 Docker Compose

`docker compose ps` 显示 9 个服务全部运行，PostgreSQL 为 `healthy`。

状态：`PASS`

### 7.2 V-PLC Profile 与参数

最终启动日志：

```text
profile=normal
scale=1.0
ack_deadline_s=10.0
```

三站参数：

| Station | base_cycle_s | jitter_s | nok_rate |
| --- | ---: | ---: | ---: |
| WS01 | 30.4 | 1.2 | 0.020 |
| WS02 | 29.8 | 1.0 | 0.015 |
| WS03 | 29.2 | 0.9 | 0.010 |

`require_ack=true`，配置来源为 `/app/config/vplc.yaml`，config hash 非空。

状态：`PASS`

### 7.3 Normal Cycle Time

最终 normal PLC boot ID：

```text
6266e5ac-d8aa-4e8b-b82e-32c9b87fe499
```

按当前 boot ID 隔离后的数据库结果：

| Station | Rows | Avg | Min | Max |
| --- | ---: | ---: | ---: | ---: |
| WS01 | 4 | 29.50s | 29s | 31s |
| WS02 | 3 | 30.67s | 30s | 32s |
| WS03 | 2 | 29.50s | 29s | 30s |

三站 counter 不再约每 4 秒增长，已恢复到约 30 秒 normal 节拍。

状态：`PASS`

### 7.4 Collector 与 PostgreSQL

- Collector 持续记录 `cycle event stored`。
- 重建和 Profile 切换后 Collector 自动恢复连接。
- 最近 3 分钟写入 56 条 cycle，最新事件时间持续更新。
- 未发现持续 connection、identity、storage 或 ACK 错误。

状态：`PASS`

### 7.5 NOK 注入

在 fast Profile 下分别注入一次：

| Station | NOK code | 结果 |
| --- | ---: | --- |
| WS01 | 10001 | cycle_event `NOK` |
| WS02 | 20001 | cycle_event `NOK` |
| WS03 | 30001 | cycle_event `NOK` |

三个 pending 队列最终均归零。

状态：`PASS`

### 7.6 Normal Guardrail 与审计

在 normal Profile 请求：

```json
{"base_cycle_s": 1.0, "reason": "verify normal guardrail"}
```

结果：

- HTTP `400`
- 运行参数未改变
- `vplc_parameter_change_log.accepted=false`
- 拒绝原因：
  `normal profile does not allow runtime cycle edits`

状态：`PASS`

### 7.7 Dashboard

- Grafana `/api/health` 返回 database `ok`。
- Dashboard 的三工站 Cycle Time 数据源仍为 `cycle_event`。
- 当前 normal boot 的三站 Cycle Time 为约 29–32 秒，不再生成默认 4 秒事件。

状态：`PASS`

注意：历史时间范围仍包含部署前的 4 秒数据，以及本次验证主动生成的 fast/test
加速数据。Grafana 选择宽时间范围时可能显示混合平均值；选择最终 normal boot
之后的时间范围可看到约 30 秒。

### 7.8 Fast / Test Profile

数据库 startup snapshots：

| Profile | Scale | 结果 |
| --- | ---: | --- |
| normal | 1.0 | PASS |
| fast | 0.1 | PASS |
| test | 0.05 | PASS |

fast/test 均保持三站约 30 秒 process baseline，只修改 scale。

验证结束后已恢复：

```text
profile=normal
scale=1.0
require_ack=true
```

状态：`PASS`

### 7.9 API

API `/health`：

```json
{"status":"ok"}
```

状态：`PASS`

## 8. 最终运行状态

```text
profile=normal
scale=1.0
require_ack=true
WS01 base=30.4
WS02 base=29.8
WS03 base=29.2
PostgreSQL healthy
Collector running
Grafana healthy
API healthy
```

部署成功，无需回滚。

## 9. 遗留问题

1. 远程部署目录不是 Git 仓库，版本追踪依赖发布包、校验值和备份文件。
2. 历史数据库保留旧 4 秒事件；本次没有删除或改写历史数据。
3. 本次 fast/test 验证生成了少量 1–3 秒测试 cycle，应在 Dashboard 分析时按时间或
   `plc_boot_id` 排除。
4. 当前 Grafana 未新增参数审计专用面板；审计可通过 V-PLC API 或 PostgreSQL 查询。
5. Compose 构建过程中远程 tar 输出 macOS extended attribute 忽略提示，不影响文件
   内容、构建或运行。

