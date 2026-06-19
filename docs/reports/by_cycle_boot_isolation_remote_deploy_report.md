# Trace by-cycle Boot Isolation Remote Deploy Report

日期：2026-06-19  
目标主机：Raspberry Pi `Pi-5b-Li`  
连接方式：已配置的 SSH 主机别名 `edge-pi`  
部署范围：仅 `/trace/api/by-cycle` boot isolation 修复  
结果：**PASS**

## 1. 远程路径

用户提供的路径：

```text
/home/pi/MES/edge-mes-demo
```

只读检查结果：

```text
NOT FOUND
```

SSH 登录后的 home 为 `/home/mari`。随后通过目录检查和运行中 API 容器的 Compose
labels 确认实际部署真源：

```text
Working directory: /opt/edge-mes-demo
Compose file:      /opt/edge-mes-demo/docker-compose.yml
```

本次部署全部在 `/opt/edge-mes-demo` 执行，没有创建或使用新的平行部署目录。

## 2. 部署前只读检查

执行：

```bash
ssh edge-pi
hostname
pwd
cd /opt/edge-mes-demo
docker compose ps
ls -la
docker compose config --quiet
```

结果：

- Hostname：`Pi-5b-Li`
- API、Collector、V-PLC、PostgreSQL、Grafana、Prometheus 等 9 个服务均在运行。
- PostgreSQL 状态为 `healthy`。
- API 部署前已运行约 2 天。
- API `/health` 返回：

  ```json
  {"status":"ok"}
  ```

- 部署前 live OpenAPI 的 by-cycle 参数只有：

  ```text
  station_id
  cycle_counter
  ```

- 远程旧版 `trace.py` SHA-256：

  ```text
  b99781d166e3bba29d947343af973f059bfa3d7382b091595c8b24e7d0a897d4
  ```

这与专项 Validation Report 的结论一致：远程 API 仍为修复前版本。

## 3. 备份位置

备份目录：

```text
/home/mari/edge-mes-backups/by-cycle-boot-isolation-20260619-151139
```

备份内容：

```text
api/
docker-compose.yml
source.sha256
env.sha256
data-dir-stat-before.txt
```

说明：

- 备份了完整远程 `api/` 目录和 `docker-compose.yml`。
- 只保存 `.env` 的 SHA-256，没有读取、复制或保存 `.env` 内容。
- 没有读取或接触 SSH 私钥。
- 没有将任何 SSH 凭据写入报告、日志或 Git 文件。

备份中的旧文件哈希：

```text
b99781d166e3bba29d947343af973f059bfa3d7382b091595c8b24e7d0a897d4  api/app/routes/trace.py
a71ab815a34f3c493f38ec572e0cf5892a9a7cdc081d8d3e2e312a380cad9ef0  docker-compose.yml
```

## 4. 同步文件

本次确认唯一需要部署的生产文件：

```text
api/app/routes/trace.py
```

同步命令：

```bash
scp api/app/routes/trace.py \
  edge-pi:/opt/edge-mes-demo/api/app/routes/trace.py
```

未同步：

- `docker-compose.yml`
- `.env`
- `data/`
- 数据库 migration
- Grafana 配置或 volume
- Prometheus 配置或数据
- Collector
- V-PLC / PLC SIM
- 测试文件和本地验收脚本

同步后本地与远程 `trace.py` SHA-256 一致：

```text
33edbfae81d9bf717925f6a2a2de8dd6e1c3843b583ebdb98806d35de2a6ef65
```

远程 Python compile 检查：

```text
REMOTE_TRACE_COMPILE_OK
```

## 5. 重建服务

只重建并重启 API：

```bash
cd /opt/edge-mes-demo
docker compose build api
docker compose up -d --no-deps api
```

结果：

```text
Image: edge-mes-demo-api
Image SHA-256:
edaac127c555cafdb7daae221d779b5d5d41db2962040fd9ee85f1f5c9278cc5
Container: edge-mes-api
Status: running
```

没有重建或重启：

- `edge-mes-collector`
- `edge-mes-s7-plc-sim`
- `edge-mes-postgres`
- `edge-mes-grafana`
- `edge-mes-prometheus`
- 其他 Compose 服务

部署后检查上述容器的启动时间保持不变。

## 6. 配置和数据保护检查

### `.env`

部署前后 SHA-256 一致：

```text
2f4a860abb23fe452bcb588788d852d0c6a3e7532df0b866f73a3b35d3f6f14c
```

### `docker-compose.yml`

本地、远程部署前后 SHA-256 一致：

```text
a71ab815a34f3c493f38ec572e0cf5892a9a7cdc081d8d3e2e312a380cad9ef0
```

### 持久化目录

以下目录没有被同步、删除或重新初始化：

```text
data/postgres
data/grafana
data/prometheus
data/vplc
```

目录 inode 在部署前后保持一致。Grafana 目录的 mtime 在运行期间自然更新，但本次没有
向任何 `data/` 路径写入部署文件。

## 7. 验证命令

### 服务和 API

```bash
cd /opt/edge-mes-demo
docker compose ps
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/openapi.json
docker compose logs --since 5m api
```

### 本地自动化

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api \
  .venv/bin/python -m unittest discover -s api/tests -v

PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python -m unittest tests/test_acceptance_sprint.py -v
```

### 真实跨 boot 定向回归

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --by-cycle-only \
  --host 10.0.0.217 \
  --output /tmp/by_cycle_boot_isolation_remote_deploy_validation.json
```

原始验证文件：

```text
/tmp/by_cycle_boot_isolation_remote_deploy_validation.json
SHA-256:
7c338533b127b569281f5cf1c44dada6bb242a3df561739fd8f95d7e85a450f6
```

## 8. 验证结果

### Compose 与健康检查

- 9 个服务均在运行。
- PostgreSQL `healthy`。
- API `/health`：`PASS`。
- API 启动日志无 error/traceback。
- 部署后 OpenAPI by-cycle 参数：

  ```text
  station_id
  cycle_counter
  plc_boot_id
  plc_id
  line_id
  ```

### 本地回归

| Suite | Result |
| --- | --- |
| Trace API boot isolation | PASS，3/3 |
| Acceptance 工具 | PASS，5/5 |

### 真实跨 boot 样本

自动选择：

| Field | Current | Historical |
| --- | --- | --- |
| PLC | `PLC_001` | `PLC_001` |
| Line | `LINE_001` | `LINE_001` |
| Station | `WS03` | `WS03` |
| Counter | `592` | `592` |
| Boot ID | `6266e5ac-d8aa-4e8b-b82e-32c9b87fe499` | `COLLECTOR-6defad45-8244-4e60-9bd3-ab88b3ad045c` |
| Unit ID | `U-20260619-000592` | `U-20260617-000592` |

断言结果：

| Check | Result |
| --- | --- |
| 当前/历史样本 UID 不同 | PASS |
| 默认查询返回当前 boot 工件 | PASS |
| 显式当前 boot 返回当前工件 | PASS |
| 显式历史 boot 返回历史工件 | PASS |
| 默认响应三站 events 全属于当前 boot | PASS |
| 显式当前响应三站 events 全属于当前 boot | PASS |
| 显式历史响应三站 events 全属于历史 boot | PASS |

定向回归最终状态：

```text
PASS
```

## 9. Acceptance 严重问题状态

`acceptance_report.md` 中的 ACPT-H-01：

```text
/trace/api/by-cycle 未按 plc_boot_id 隔离
```

已在 live Raspberry Pi API 上复现原问题的同类真实数据，并验证修复后：

- 默认查询不跨 boot。
- 显式当前 boot 查询正确。
- 显式历史 boot 查询正确。
- 三站 Trace event 不跨 boot 混合。

因此 ACPT-H-01 的技术问题可更新为：

```text
PASS — fixed, deployed, live targeted regression passed
```

## 10. 是否建议 Verification 重新执行最终验收

建议重新执行最终验收。

理由：

- 本报告已经关闭 ACPT-H-01 的定向技术验证。
- 最终 Acceptance Report 仍包含独立问题，例如 `/trace/api/recent` 字段语义、
  Dashboard 历史 Profile 隔离和部署/回滚验收。
- 应由 Verification Team 使用其最终验收流程更新整体结论，而不是仅依据部署线程将
  `CONDITIONAL PASS` 直接改为无条件 PASS。

建议至少重新执行：

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --by-cycle-only \
  --host 10.0.0.217 \
  --output /tmp/by_cycle_boot_isolation_final_verification.json
```

随后按 Verification Team 的范围决定是否重跑完整 acceptance sprint。
