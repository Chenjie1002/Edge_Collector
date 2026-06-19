# Edge MES Final Remote Deploy Report

日期：2026-06-19  
目标主机：Raspberry Pi `Pi-5b-Li`（`10.0.0.217`）  
连接方式：SSH alias `edge-pi`  
部署结果：**PASS**

## 1. 部署范围

本次统一部署两个已在本地完成并通过回归的修复：

1. Recent API `cycle_counter` 字段语义修复。
2. Grafana 三工站 Dashboard Profile 隔离修复。

没有修改业务代码设计、数据库结构、PLC SIM、Collector、ACK 或 boot identity 逻辑。
远程目录不是 Git 仓库，本次没有执行 `git pull`。

## 2. 远程路径

实际部署路径：

```text
/opt/edge-mes-demo
```

部署前检查：

```bash
ssh edge-pi
cd /opt/edge-mes-demo
docker compose ps
```

结果：

- 9 个 Compose 服务均在运行。
- PostgreSQL 为 `healthy`。
- API、Grafana、Collector 和 V-PLC 正常运行。

## 3. 备份路径

最近既有恢复点：

```text
/home/mari/edge-mes-backups/rollback-drill-20260619-213700
```

本次部署前新建恢复点：

```text
/home/mari/edge-mes-backups/final-deploy-20260619-214651
```

备份内容：

```text
api/app/routes/trace.py
config/grafana/dashboards/edge_mes_station_traceability.json
docker-compose.yml
source.sha256
env.sha256
data-dir-stat-before.txt
container-baseline.txt
manifest.txt
```

安全说明：

- 只记录 `.env` SHA-256，没有读取、复制或保存 `.env` 内容。
- 没有读取或复制 SSH 私钥。
- 没有备份或覆盖 PostgreSQL、Grafana、Prometheus、V-PLC 数据 volume。

## 4. 同步文件

仅同步：

```text
api/app/routes/trace.py
config/grafana/dashboards/edge_mes_station_traceability.json
```

同步后本地和远程哈希一致：

```text
f2fced93a706a0642ea2c72fcf97d4ac1b9198fa05b7936f4107b4905265e7f4
api/app/routes/trace.py

b62e2a0186442a9f857c89892b749bb41827d1f67e106babaab26d68df1a1283
config/grafana/dashboards/edge_mes_station_traceability.json
```

同步后执行：

- Python compile：`PASS`
- Dashboard JSON parse：`PASS`

未同步：

- `.env`
- `docker-compose.yml`
- `db/` 或 migration
- Collector
- V-PLC / PLC SIM
- PostgreSQL、Grafana、Prometheus 数据目录
- 其他 Dashboard

## 5. 重建和刷新服务

### API

执行：

```bash
docker compose build api
docker compose up -d --no-deps api
```

新 API image：

```text
sha256:38f52bbd04d81ddea88fb5837cd4387113aa0591adf431aff3817aff98ac00f3
```

### Grafana

Dashboard provisioning 目录通过只读 volume 挂载。为确保新 JSON 立即进入运行态，仅执行：

```bash
docker compose restart grafana
```

没有重新构建或拉取 Grafana image。

### 未重启服务

以下容器 ID 和启动时间与部署前基线一致：

- `edge-mes-postgres`
- `edge-mes-collector`
- `edge-mes-s7-plc-sim`

Simulator、Prometheus、Node Exporter 和 Sync Worker 也未执行重建或重启。

## 6. 验证命令

### 本地发布前回归

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api \
  .venv/bin/python -m unittest discover -s api/tests -v

PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python -m unittest \
  tests/test_grafana_profile_filter.py \
  tests/test_acceptance_sprint.py -v
```

### 服务状态与健康检查

```bash
ssh edge-pi
cd /opt/edge-mes-demo
docker compose ps
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:3000/api/health
```

### Recent API

```text
GET /trace/api/recent?status=completed_ok&limit=3
```

### Grafana provisioning

```text
GET /api/dashboards/uid/edge-mes-station-traceability
```

### by-cycle 定向回归

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --by-cycle-only \
  --host 10.0.0.217 \
  --output /tmp/final_remote_deploy_by_cycle.json
```

### Acceptance 基础检查

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --snapshot-only \
  --host 10.0.0.217 \
  --output /tmp/final_remote_deploy_snapshot.json
```

## 7. 验证结果

### 7.1 本地回归

| Suite | Result |
| --- | --- |
| API tests | PASS，5/5 |
| Grafana + Acceptance tests | PASS，11/11 |
| Python compile | PASS |
| Grafana JSON parse | PASS |
| `git diff --check` | PASS |

### 7.2 Compose 与数据保护

| Check | Result |
| --- | --- |
| 9 个服务运行 | PASS |
| PostgreSQL healthy | PASS |
| `.env` SHA-256 不变 | PASS |
| `docker-compose.yml` SHA-256 不变 | PASS |
| 四个数据目录 inode 不变 | PASS |
| PostgreSQL 容器未重启 | PASS |
| Collector 容器未重启 | PASS |
| V-PLC 容器未重启 | PASS |

### 7.3 API Health

```json
{"status":"ok"}
```

结果：`PASS`

### 7.4 Recent API Counter 语义

Live 样本：

| Unit | Station | cycle_counter | station_cycle_counter | route_step |
| --- | --- | ---: | ---: | ---: |
| `U-20260619-001362` | WS03 | 1362 | 1362 | 3 |
| `U-20260619-001361` | WS03 | 1361 | 1361 | 3 |
| `U-20260619-001360` | WS03 | 1360 | 1360 | 3 |

验证结论：

- `cycle_counter` 等于真实 `station_cycle_counter`。
- `route_step=3` 使用独立字段表达。
- `plc_boot_id`、`plc_id`、`line_id` 正常返回。
- 原远程问题 `cycle_counter=3` 已消失。

结果：`PASS`

### 7.5 Grafana Profile Dashboard

Live Dashboard API 返回：

```text
Profile variable: profile
Default: normal
Include All: true
All value: all
Profile-filtered queries: 12
```

新增面板已生效：

```text
当前 V-PLC Profile
时间窗 Profile 构成
```

24 小时宽时间窗 SQL 结果：

```text
MIXED: fast, normal, test, unknown
```

Grafana health：

```json
{
  "database": "ok",
  "version": "13.0.2"
}
```

Grafana 日志确认 Dashboard provisioning 已完成。启动日志中仍有缺少可选
`plugins/alerting` provisioning 目录的既有提示，但不影响 Dashboard provisioning、
健康接口或本次 Profile Dashboard。

结果：`PASS`

### 7.6 by-cycle Boot Isolation

定向样本：

```text
Station: WS01
Counter: 1363
Current boot unit: U-20260619-001363
Historical boot unit: U-20260617-001363
```

验证：

- 默认查询返回当前 boot 工件。
- 显式当前 boot 返回当前工件。
- 显式历史 boot 返回历史工件。
- 所有 events 均严格匹配目标 boot。
- Live OpenAPI 仍包含：

  ```text
  station_id
  cycle_counter
  plc_boot_id
  plc_id
  line_id
  ```

结果：`PASS`

原始证据：

```text
/tmp/final_remote_deploy_by_cycle.json
SHA-256:
bcae27b5014be9a2a31a29f91f8efa1788732bea51d50761554cd044e3433200
```

### 7.7 Acceptance Sprint 基础检查

Snapshot assertions：

- V-PLC `normal`、scale `1.0`、strict ACK 正常。
- API health 正常。
- Grafana database 正常。
- Collector 三站 `RUNNING / CONNECTED`。
- 三站 rows、unique counters、max counter 一致。
- 当前 boot 非 `ACK_OK` 数量为 0。
- 重复事件键为 0。
- Collector error 窗口为空。
- Recent API counter 与 station counter 一致，且不等于 route step。

结果：`PASS`

原始证据：

```text
/tmp/final_remote_deploy_snapshot.json
SHA-256:
eb08595d67cf8e4d3724d3e49755c720d2cb2c2391195517ee61440505d2e869
```

## 8. 最终结论

本次部署的两个剩余项均已进入 Raspberry Pi live 运行环境：

- Recent API counter 语义：`PASS`
- Grafana Profile 隔离：`PASS`

by-cycle boot isolation、基础采集完整性、ACK、PostgreSQL 和其他非目标服务均保持正常。
没有数据库 schema 变更，没有覆盖配置或数据 volume。

## 9. Verification 建议

**建议 Verification 执行最终验收。**

建议最终验收重点复核：

1. Recent API 与 Trace 页面显示真实 station counter 和独立 route step。
2. Grafana 默认 Profile 为 `normal`。
3. 宽时间窗显示 `MIXED`，切换 Profile 后 KPI 口径正确。
4. by-cycle 跨 boot 定向回归继续通过。
5. 更新 `acceptance_report.md` 中 Recent API 与 Grafana 两项状态。

由于真实回滚演练此前已通过，本次 live 部署和专项回归也已通过，若 Verification 复核
一致，可以评估将总体结论由 `CONDITIONAL PASS` 升级为 `PASS`。
