# Edge MES Remote Rollback Drill Report

日期：2026-06-19  
目标主机：Raspberry Pi `Pi-5b-Li`（`10.0.0.217`）  
连接方式：SSH alias `edge-pi`  
远程路径：`/opt/edge-mes-demo`  
演练结论：**PASS**  
最终验收建议：**CONDITIONAL PASS**

## 1. 演练范围

本次执行真实远程代码回滚，范围严格限定为：

```text
api/app/routes/trace.py
API image / edge-mes-api container
```

未修改：

- 业务协议、ACK 定义、Data Gap 定义。
- 数据库 schema、migration 或数据库既有数据。
- `.env`、`docker-compose.yml`。
- Collector、V-PLC、PostgreSQL、Grafana、Prometheus 等其他服务。
- `data/postgres`、`data/grafana`、`data/prometheus`、`data/vplc`。

完整 Acceptance Sprint 会通过正常业务链路生成验收事件，但本次没有执行 SQL
`INSERT/UPDATE/DELETE`、数据清理或数据恢复。

## 2. 回滚对象与备份

既有旧版备份：

```text
/home/mari/edge-mes-backups/by-cycle-boot-isolation-20260619-151139
```

旧版 `trace.py`：

```text
b99781d166e3bba29d947343af973f059bfa3d7382b091595c8b24e7d0a897d4
```

演练前新建恢复点：

```text
/home/mari/edge-mes-backups/rollback-drill-20260619-213700
```

其中保存：

- 演练前 `api/app/routes/trace.py`。
- `docker-compose.yml`。
- source、Compose、`.env` 哈希。
- 数据目录 inode/权限基线。
- 9 个容器的 ID、启动时间和 image ID。
- 回滚对象与恢复对象 manifest。

演练前/恢复后 `trace.py`：

```text
33edbfae81d9bf717925f6a2a2de8dd6e1c3843b583ebdb98806d35de2a6ef65
```

## 3. 安全回滚步骤

1. 读取现有备份并确认旧、新文件哈希不同。
2. 创建独立演练前恢复点。
3. 记录 Compose、`.env`、数据目录和全部容器基线。
4. 将旧版 `trace.py` 复制到远程运行目录。
5. 执行 Python compile。
6. 仅执行：

   ```bash
   docker compose build api
   docker compose up -d --no-deps api
   ```

7. 等待 `/health` 恢复。
8. 验证旧版 OpenAPI 特征、Recent API、UID Trace 和 Compose 状态。

未执行 `docker compose down`，未重建依赖服务，未接触数据卷。

## 4. 真实回滚结果

回滚后 API image：

```text
sha256:1d15a0163edebe968e32d14e96bbcbdde5528a9084719b883e92e639f188091a
```

验证结果：

| Check | Result |
| --- | --- |
| 旧版 `trace.py` 哈希命中 | PASS |
| Python compile | PASS |
| API image build | PASS |
| API `/health` | PASS |
| UID Trace 三站查询 | PASS |
| OpenAPI 回退到旧版 2 参数 | PASS |
| 非 API 容器未重启 | PASS |

OpenAPI 由最新版本的 5 个参数真实回退为：

```text
station_id
cycle_counter
```

该差异证明旧代码已实际进入运行容器，不是仅复制文件的模拟回滚。

## 5. 恢复步骤

1. 从演练恢复点复制演练前 `trace.py`。
2. 校验 SHA-256 为
   `33edbfae81d9bf717925f6a2a2de8dd6e1c3843b583ebdb98806d35de2a6ef65`。
3. 执行 Python compile。
4. 仅重建并重启 API。
5. 等待 `/health`。
6. 验证 OpenAPI 恢复 5 个 boot identity 参数。
7. 执行 by-cycle 定向回归与完整 Acceptance Sprint。
8. 复核 Compose、`.env`、数据目录和非 API 容器基线。

恢复后 API image：

```text
sha256:edaac127c555cafdb7daae221d779b5d5d41db2962040fd9ee85f1f5c9278cc5
```

## 6. 恢复后验证结果

| Item | Result |
| --- | --- |
| `docker compose ps` | PASS，9 个服务运行，PostgreSQL healthy |
| API `/health` | PASS |
| Trace API | PASS |
| by-cycle 5 个 identity 参数 | PASS |
| by-cycle 跨 boot 定向回归 | PASS |
| Recent API 基本可访问 | PASS |
| Grafana `/api/health` | PASS，database `ok` |
| Grafana dashboard 可检索 | PASS |
| 完整 Acceptance Sprint | PASS |
| 非 API 容器 ID/启动时间 | PASS，演练前后不变 |
| Compose / `.env` 哈希 | PASS，演练前后不变 |
| 四个持久化目录 inode | PASS，演练前后不变 |
| API 最近日志 | PASS，无 error/traceback |

by-cycle 定向样本：

```text
Station: WS01
Counter: 1345
Current: U-20260619-001345
Historical: U-20260617-001345
```

默认、显式当前 boot、显式历史 boot 及 event boot scope 全部通过。

原始证据：

| File | SHA-256 |
| --- | --- |
| `/tmp/rollback_drill_by_cycle.json` | `6e2ed26993ac08803ca6ef480b3c425a3aab457aec2a17caa6eef0078ec823de` |
| `/tmp/rollback_drill_acceptance_sprint.json` | `8bc0ee822ec9f6fa9b362342ac4af646efb52fb11ca292ba9d948c29af3eab57` |

## 7. 验收工具补充

首次恢复后定向回归时，Grafana datasource 中用于寻找跨 boot 同 counter 样本的全表配对
查询达到 15 秒超时。Grafana 健康接口当时仅耗时 9ms，日志确认超时发生于该 SQL。

验收脚本改为先物化当前 boot 最近 200 条候选，再执行历史 boot 配对。同一查询在远程
PostgreSQL 上耗时约 51ms。该修改仅影响测试样本选择：

- `scripts/run_acceptance_sprint.py`
- `tests/test_acceptance_sprint.py`

修改后验收工具测试 `7/7` 通过，真实 by-cycle 回归通过。

## 8. 未关闭问题

回滚演练通过，但远程最新运行基线仍不满足无条件 PASS：

1. Recent API live 响应仍为：

   ```text
   cycle_counter=3
   station_cycle_counter=null
   route_step=null
   ```

   同一 UID 的三站真实 counter 为 `1346`。ACPT-M-01 的本地修复尚未部署。

2. Live Grafana dashboard 只有 `station` 变量，没有 `profile` 变量，也没有“当前
   V-PLC Profile”与“时间窗 Profile 构成”面板。Profile mixing 修复尚未部署。

## 9. 风险点

- 当前远程目录不是 Git working tree，回滚依赖文件级备份和哈希，仍缺少统一版本
  manifest 与自动 rollback 命令。
- API 回滚窗口内会短暂运行已知存在 by-cycle boot isolation 缺陷的旧版本；正式现场应
  选择维护窗口并限制调用。
- Acceptance Sprint 会生成正常/NOK/Skip 验收事件，应使用明确的验收时间窗或标识与
  生产统计区分。
- `external_running=false`，但 continuous plan 的 `line.running=true`，三站 counter
  持续增长；本次没有额外写入控制状态。

## 10. 最终验收建议

真实回滚、恢复、服务健康、Trace/by-cycle 回归和完整 Acceptance Sprint 均通过，
Deployment 回滚项可从 `BLOCKED` 更新为 `PASS`。

由于 ACPT-M-01 与 Grafana Profile 隔离修复尚未部署，整体结论保持：

```text
CONDITIONAL PASS / 有条件通过
```

待两项修复部署并完成 live 专项复验后，再评估升级为 `PASS`。
