# Edge MES Final Phase 1 Acceptance Report

日期：2026-06-19  
目标主机：Raspberry Pi `Pi-5b-Li`（`10.0.0.217`）  
连接方式：SSH alias `edge-pi`  
远程路径：`/opt/edge-mes-demo`  
最终结论：**PASS**

## 1. 验证环境

本次只执行最终验收和报告更新：

- 未修改业务代码。
- 未重新部署或重启服务。
- 未修改协议、数据库 schema 或既有数据库数据。
- 完整 Acceptance Sprint 通过既有 V-PLC 控制接口生成验收事件，并在结束后恢复 NOK
  rate 和 pending queue。

读取：

- `docs/reports/final_remote_deploy_report.md`
- `docs/reports/rollback_drill_report.md`
- `docs/reports/acceptance_report.md`
- `docs/reports/final_acceptance_validation_report.md`
- `scripts/run_acceptance_sprint.py`

## 2. 服务状态

远程实际路径：

```text
/opt/edge-mes-demo
```

最终部署文件 SHA-256：

```text
api/app/routes/trace.py
f2fced93a706a0642ea2c72fcf97d4ac1b9198fa05b7936f4107b4905265e7f4

config/grafana/dashboards/edge_mes_station_traceability.json
b62e2a0186442a9f857c89892b749bb41827d1f67e106babaab26d68df1a1283
```

服务检查：

| Check | Result |
| --- | --- |
| Compose running services | PASS，9/9 |
| PostgreSQL | PASS，`healthy` |
| API `/health` | PASS，`{"status":"ok"}` |
| Grafana `/api/health` | PASS，database `ok`，version `13.0.2` |
| Collector | PASS，三站 `RUNNING / CONNECTED` |
| V-PLC | PASS，normal、scale 1.0、strict ACK |

API image：

```text
sha256:38f52bbd04d81ddea88fb5837cd4387113aa0591adf431aff3817aff98ac00f3
```

## 3. Recent API 验证结果

Live completed OK 样本：

| Unit | Station | cycle_counter | station_cycle_counter | route_step |
| --- | --- | ---: | ---: | ---: |
| `U-20260619-001377` | WS03 | 1377 | 1377 | 3 |
| `U-20260619-001376` | WS03 | 1376 | 1376 | 3 |
| `U-20260619-001375` | WS03 | 1375 | 1375 | 3 |

对首个样本继续查询 UID Trace：

```text
WS01 counter = 1377
WS02 counter = 1377
WS03 counter = 1377
```

验证：

- `cycle_counter == station_cycle_counter`。
- `cycle_counter` 与同 UID 最新三站真实事件 counter 一致。
- `route_step=3` 使用独立字段表达。
- `plc_boot_id`、`plc_id`、`line_id` 正常返回。
- 原远端错误 `cycle_counter=3` 已消失。

结果：`PASS`

ACPT-M-01：`CLOSED`

## 4. Grafana Profile 验证结果

Live Dashboard：

```text
UID: edge-mes-station-traceability
Profile default: normal
Include All: true
All value: all
Profile-filtered queries: 12
```

新增面板：

```text
当前 V-PLC Profile
时间窗 Profile 构成
```

24 小时宽时间窗只读 SQL：

```text
MIXED: fast, normal, test, unknown
```

验证：

- Profile 默认值为 `normal`。
- Profile 支持 `fast/test/unknown/All`。
- 基于 `cycle_event` 的 KPI、趋势和追溯查询应用 Profile scope。
- 宽时间窗明确提示混合 Profile。
- Grafana provisioning 后 dashboard API 已返回修复后的运行态配置。

结果：`PASS`

ACPT-M-05：`CLOSED`

Grafana 日志中仍存在缺少可选 `plugins/alerting` provisioning 目录的既有提示；它不影响
Dashboard provisioning、Profile 变量、查询或 Grafana health。

## 5. by-cycle 验证结果

Live OpenAPI 参数：

```text
station_id
cycle_counter
plc_boot_id
plc_id
line_id
```

最终定向样本：

| Field | Current | Historical |
| --- | --- | --- |
| Station | WS02 | WS02 |
| Counter | 1380 | 1380 |
| Boot | `6266e5ac-d8aa-4e8b-b82e-32c9b87fe499` | `COLLECTOR-6defad45-8244-4e60-9bd3-ab88b3ad045c` |
| Unit | `U-20260619-001380` | `U-20260617-001380` |

全部断言：

- 当前与历史 UID 不同：PASS。
- 默认查询返回当前 boot：PASS。
- 显式当前 boot 返回当前工件：PASS。
- 显式历史 boot 返回历史工件：PASS。
- 三类响应的 events 均严格匹配目标 boot：PASS。

原始证据：

```text
/tmp/final_phase1_by_cycle.json
SHA-256:
fe2279542d78279e6476b2c3e086d7e70f38bd9a54c32e8091bd7bb31ae144b3
```

结果：`PASS`

ACPT-H-01：`CLOSED`

## 6. 回滚演练确认

已读取并核对：

```text
docs/reports/rollback_drill_report.md
```

确认内容：

- 演练结论为 `PASS`。
- 旧版 `trace.py` 已真实进入 API image 并启动。
- 旧版 OpenAPI 的 2 参数特征得到验证。
- 随后恢复最新 by-cycle 版本。
- 恢复后 by-cycle 与完整 Acceptance Sprint 通过。
- 非 API 容器、Compose、`.env` 和持久化数据目录基线保持不变。

远程恢复点仍存在：

```text
/home/mari/edge-mes-backups/rollback-drill-20260619-213700
/home/mari/edge-mes-backups/final-deploy-20260619-214651
```

结果：`PASS`

## 7. Acceptance Sprint 结果

执行：

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --host 10.0.0.217 \
  --output /tmp/final_phase1_acceptance_sprint.json
```

结果：

| Flow | Result | Unit / Counter |
| --- | --- | --- |
| Normal | PASS | `U-20260619-001379` / 1379 |
| WS01 NOK | PASS | `U-20260619-001382` / 1382 / code 10001 |
| WS02 NOK | PASS | `U-20260619-001383` / 1383 / code 20001 |
| WS03 NOK | PASS | `U-20260619-001384` / 1384 / code 30001 |
| Skip | PASS | 上游 NOK 后下游 SKIPPED |
| Profile history | PASS | normal / fast / test |
| API/Grafana health | PASS | live |
| ACK | PASS | 场景事件 `ACK_OK` |

验收后恢复：

```text
restore_errors = []
profile = normal
scale = 1.0
require_ack = true
line.running = true
external_running = true
NOK rates = 0.02 / 0.015 / 0.01
pending forced NOK = 0 / 0 / 0
```

原始证据：

```text
/tmp/final_phase1_acceptance_sprint.json
SHA-256:
ce8b0bb6248a614642313fa6de84a0d1c9b418271883764ff02734891d329de4
```

Sprint 后只读快照：

```text
/tmp/final_phase1_post_sprint_snapshot.json
SHA-256:
5e766bcdc2a2c50162c226e50de556faf9a2d16e072ed75f0a3273510adf5cd8
```

快照确认：

- WS01/WS02/WS03 rows、unique counters、max counter 分别一致到
  `1390/1389/1388`。
- 当前 boot 非 `ACK_OK` 数量为 0。
- 重复事件键为 0。
- WS03 为 1388 行、1388 个不同 UID，serial `1..1388`。
- Collector 三站均为 `RUNNING / CONNECTED`，`ack_timeout=false`。
- Recent 列表的 `cycle_counter == station_cycle_counter`，且 `route_step=3`。

结果：`PASS`

## 8. 本地回归

| Suite | Result |
| --- | --- |
| API tests | PASS，5/5 |
| Grafana + Acceptance tests | PASS，11/11 |

未修改业务代码或测试逻辑。

## 9. acceptance_report.md 更新

已更新：

- 总结论从 `CONDITIONAL PASS` 更新为 `PASS`。
- Recent API 字段语义从 `FAIL` 更新为 `PASS`。
- ACPT-M-01 更新为 `CLOSED`。
- Grafana Profile 历史隔离从 `PARTIAL` 更新为 `PASS`。
- ACPT-M-05 更新为 `CLOSED`。
- 增加最终 by-cycle 与完整 Acceptance Sprint 原始证据。
- 保留部署自动化、Grafana 网络权限和生产化长稳测试等非 Phase 1 阻塞风险。

## 10. 最终结论

| Item | Result |
| --- | --- |
| 9 个 Compose 服务 | PASS |
| PostgreSQL healthy | PASS |
| Recent API counter 语义 | PASS |
| Grafana Profile 隔离 | PASS |
| by-cycle boot isolation | PASS |
| 真实回滚演练 | PASS |
| 完整 Acceptance Sprint | PASS |
| acceptance_report.md 更新 | YES |

最终结论：

```text
PASS / 通过
```

Edge MES Demo Phase 1 阻塞项已全部关闭，具备受控环境下客户演示条件。该结论不等同于
生产交付认证；网络权限、统一部署自动化、资源/磁盘专项验收和 24 小时以上长稳测试仍是
后续生产化工作。
