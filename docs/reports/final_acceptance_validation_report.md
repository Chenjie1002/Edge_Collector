# Edge MES Final Acceptance Validation Report

日期：2026-06-19  
目标主机：Raspberry Pi `Pi-5b-Li`  
连接方式：SSH alias `edge-pi`  
远程路径：`/opt/edge-mes-demo`  
验证范围：ACPT-H-01 关闭验证与最终 Acceptance Sprint 复验  
最终结论：**CONDITIONAL PASS**

## 1. 验证环境

本次只执行验证和报告更新：

- 未修改业务逻辑。
- 未修改 API 代码。
- 未同步文件。
- 未重建或重启服务。
- 验收脚本的 Profile 历史查询窗口问题得到修正；该修改只影响测试工具。

读取：

- `docs/reports/by_cycle_boot_isolation_remote_deploy_report.md`
- `docs/reports/by_cycle_boot_isolation_validation_report.md`
- `docs/reports/acceptance_report.md`
- `scripts/run_acceptance_sprint.py`

## 2. 远程路径与 Compose

SSH 实际登录：

```text
Host: Pi-5b-Li
Path: /opt/edge-mes-demo
Compose: /opt/edge-mes-demo/docker-compose.yml
```

`docker compose ps` 结果：

- 9 个服务全部运行。
- PostgreSQL 为 `healthy`。
- API 容器为 `running`。
- Collector、V-PLC、PostgreSQL、Grafana 等服务没有因本次复验重启。

状态：`PASS`

## 3. API 容器状态

API 容器：

```text
Container: edge-mes-api
Status: running
Image:
sha256:edaac127c555cafdb7daae221d779b5d5d41db2962040fd9ee85f1f5c9278cc5
Started:
2026-06-19T07:12:02.387089991Z
```

运行标签确认：

```text
working_dir=/opt/edge-mes-demo
compose_file=/opt/edge-mes-demo/docker-compose.yml
```

远程 `trace.py`：

```text
SHA-256:
33edbfae81d9bf717925f6a2a2de8dd6e1c3843b583ebdb98806d35de2a6ef65
```

与远程部署报告中的修复文件一致。

API `/health`：

```json
{"status":"ok"}
```

API 启动日志：

- Uvicorn 正常启动。
- 没有 error 或 traceback。
- by-cycle 默认、显式当前 boot、显式历史 boot 请求均返回 HTTP 200。

状态：`PASS`

## 4. OpenAPI 隔离参数

Live OpenAPI 已显示：

```text
station_id
cycle_counter
plc_boot_id
plc_id
line_id
```

这与本地修复后的 API 定义一致，证明 API 容器确实运行修复版本，不再是上次验证时只有
两个参数的旧 handler。

状态：`PASS`

## 5. 配置、备份与数据保护

备份目录存在：

```text
/home/mari/edge-mes-backups/by-cycle-boot-isolation-20260619-151139
```

备份中包含：

- 旧 `api/`。
- `docker-compose.yml`。
- source hash。
- `.env` hash。
- 部署前数据目录 stat。

当前与备份记录：

```text
docker-compose.yml:
a71ab815a34f3c493f38ec572e0cf5892a9a7cdc081d8d3e2e312a380cad9ef0

.env:
2f4a860abb23fe452bcb588788d852d0c6a3e7532df0b866f73a3b35d3f6f14c
```

二者与部署前记录一致。以下持久化目录仍存在：

```text
data/postgres
data/grafana
data/prometheus
data/vplc
```

状态：`PASS`

## 6. 本地回归测试

### Trace API

```text
Ran 3 tests
OK
```

覆盖：

- 默认查询选择当前 boot。
- 显式当前 boot 选择当前工件。
- 显式历史 boot 选择历史工件。

### Acceptance 工具

```text
Ran 6 tests
OK
```

除 by-cycle 参数与跨 boot 隔离外，新增验证：

- 系统长期运行后，即使最近 100 条快照全为 normal，Profile 验收仍从 PostgreSQL 历史
  正确确认 normal/fast/test。

状态：`PASS`

## 7. by-cycle Boot Isolation 验证

执行：

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --by-cycle-only \
  --host 10.0.0.217 \
  --output /tmp/by_cycle_boot_isolation_final_acceptance.json
```

真实样本：

| Field | Current | Historical |
| --- | --- | --- |
| PLC | PLC_001 | PLC_001 |
| Line | LINE_001 | LINE_001 |
| Station | WS02 | WS02 |
| Counter | 617 | 617 |
| Boot ID | `6266e5ac-d8aa-4e8b-b82e-32c9b87fe499` | `COLLECTOR-6defad45-8244-4e60-9bd3-ab88b3ad045c` |
| Unit ID | `U-20260619-000617` | `U-20260617-000617` |

断言：

| Check | Result |
| --- | --- |
| 当前/历史 UID 不同 | PASS |
| 默认查询返回当前工件 | PASS |
| 显式当前 boot 返回当前工件 | PASS |
| 显式历史 boot 返回历史工件 | PASS |
| 默认响应三站 events 全属于当前 boot | PASS |
| 显式当前响应三站 events 全属于当前 boot | PASS |
| 显式历史响应三站 events 全属于历史 boot | PASS |

原始证据：

```text
/tmp/by_cycle_boot_isolation_final_acceptance.json
SHA-256:
4054c522ca2eb182a40197bf4b15d12cdc157658b3d390f39200fdc5446f0a9d
```

状态：`PASS`

## 8. ACPT-H-01

原问题：

```text
/trace/api/by-cycle 可能跨 plc_boot_id 返回旧 boot 工件
```

本次证据确认：

- 修复文件已部署。
- API 容器运行修复镜像。
- OpenAPI 包含 5 个 identity 参数。
- 默认查询使用当前 boot。
- 显式当前和历史 boot 均严格隔离。
- 三站 Trace 不跨 boot 混合。

ACPT-H-01 状态：

```text
CLOSED / PASS
```

## 9. Acceptance Sprint 重跑

首次重跑时，业务流程已执行，但测试工具只取最近 100 条参数快照；长期运行后该窗口只
包含 normal，导致 Profile 历史断言失败。数据库中的 fast/test 历史没有丢失。

验收工具改为：

- 从 PostgreSQL 对 normal/fast/test 各取最新一条历史记录。
- 当前 normal boot 仍从最新运行快照确认。

修改仅位于：

- `scripts/run_acceptance_sprint.py`
- `tests/test_acceptance_sprint.py`

修正后完整执行：

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --host 10.0.0.217 \
  --output /tmp/final_acceptance_sprint.json
```

结果：

```text
PASS
```

覆盖结果：

- Normal Flow：PASS，`U-20260619-000625`，三站 counter 625。
- WS01 NOK：PASS，code `10001`。
- WS02 NOK：PASS，code `20001`。
- WS03 NOK：PASS，code `30001`。
- Skip Flow：PASS。
- 每个 NOK 场景的默认及显式当前 boot by-cycle 查询：PASS。
- normal/fast/test Profile 历史：PASS。
- 当前 Profile：normal，scale 1.0。
- Collector 三站：RUNNING / CONNECTED。
- API/Grafana health：PASS。
- 测试结束后三站 NOK rate 恢复。
- 测试结束后三站 forced NOK pending 为 0。

原始证据：

```text
/tmp/final_acceptance_sprint.json
SHA-256:
2287f6fc9f227be60df5c0a20788b6fee2b2e5a4488244dbb1e91c623bc1e698
```

最终恢复快照：

```text
/tmp/final_acceptance_post_run_snapshot.json
SHA-256:
01f995efe7b2ed436e2ee96c5ab5b87fd9424d1b056310fdc22d64d4d33f8f03
```

快照确认：

- Profile `normal`，scale `1.0`。
- 三站 NOK rate 已恢复为 `0.02 / 0.015 / 0.01`。
- 三站 pending queue 均为 0。
- 三站 Collector 均为 `RUNNING / CONNECTED`。
- 当前 boot 每站 rows、unique counter、max counter 一致。
- 非 `ACK_OK` 为 0，重复事件键为 0。

## 10. acceptance_report.md 更新

已更新：

- ACPT-H-01 从 `FAIL` 改为 `PASS / CLOSED`。
- API by-cycle Acceptance Matrix 改为 `PASS`。
- Raspberry Pi Compose 独立复核改为 `PASS`。
- 本次 API 定向部署的备份、同步、重建、验证改为 `PASS`。
- 增加本次定向和完整 Acceptance Sprint 证据。

未将总报告升级为无条件 `PASS`，原因是仍有独立未关闭项：

1. `/trace/api/recent` 仍将 `current_route_step=3` 返回为 `cycle_counter`；同一 UID
   `U-20260619-000629` 的真实三站 counter 为 `629`。
2. 部署回滚仍没有实际执行。
3. Grafana 宽时间窗仍混合旧 4 秒、fast/test 和 normal 数据。

因此 `acceptance_report.md` 继续保持：

```text
CONDITIONAL PASS / 有条件通过
```

## 11. 最终结论

| Item | Result |
| --- | --- |
| API 容器运行修复版本 | PASS |
| by-cycle boot isolation | PASS |
| ACPT-H-01 | CLOSED |
| 完整 Acceptance Sprint | PASS |
| acceptance_report.md 更新 | YES |
| 总验收结论 | CONDITIONAL PASS |

本次最终复验完成了 ACPT-H-01 的关闭。系统的严重追溯错配问题已消除，但依据现有完整
Acceptance Matrix，尚不能忽略仍为 FAIL/BLOCKED/PARTIAL 的独立项目而升级为无条件
`PASS`。
