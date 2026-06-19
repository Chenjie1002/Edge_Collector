# Trace by-cycle Boot Isolation Validation Report

日期：2026-06-19  
问题编号：ACPT-H-01  
范围：`GET /trace/api/by-cycle` 针对性回归  
目标主机：Raspberry Pi `10.0.0.217`  
结论：**FAIL — 本地修复通过，但 live API 尚未部署修复版本**

## 1. 验证目标

本次只验证 Data Quality Thread 对 `/trace/api/by-cycle` 的 boot isolation 修复，不修改
API、Collector、PLC、数据库 schema 或业务逻辑。

验收条件：

1. 相同 `station_id + cycle_counter` 在当前和历史 boot 中同时存在时，默认查询只能返回
   当前 boot 工件。
2. 显式指定当前 `plc_boot_id` 时只能返回当前工件。
3. 显式指定历史 `plc_boot_id` 时只能返回该历史工件。
4. 返回的 Trace events 必须携带实际 `plc_boot_id`，且三站不得跨 boot 混合。
5. 更新后的完整验收脚本可以通过新增的 by-cycle identity 断言。

## 2. 阅读与检查范围

- `docs/reports/acceptance_report.md`
- `docs/reports/by_cycle_boot_isolation_fix_report.md`
- `scripts/run_acceptance_sprint.py`
- `api/app/routes/trace.py`
- `api/tests/test_trace_by_cycle.py`
- `tests/test_acceptance_sprint.py`

本地实现与修复报告一致：

- 未指定 boot 时从 `collector_runtime_status` 推导当前 identity。
- 查询使用 `station_id + cycle_counter + plc_boot_id`，并可附加 `plc_id + line_id`。
- by-cycle seed event 后的 UID/serial Trace 继续使用相同 boot scope。
- Trace event 响应包含 `plc_id`、`line_id`、`plc_boot_id`。

## 3. 回归测试补充

在现有 `scripts/run_acceptance_sprint.py` 增加：

```text
--by-cycle-only
```

该模式自动从真实 PostgreSQL 数据中选择：

- 当前 `collector_runtime_status` 所属 boot 的事件。
- 相同 station/counter 的历史 boot 事件。
- 当前与历史工件的 `unit_id` 不同。

随后执行：

1. 默认 by-cycle 查询。
2. 显式当前 boot 查询。
3. 显式历史 boot 查询。
4. 三组响应 event boot identity 检查。

`tests/test_acceptance_sprint.py` 新增回归，验证上述三种查询的预期隔离结果。

本次只修改验收脚本和验收脚本测试。

## 4. 本地自动化结果

### 4.1 Trace API 回归

命令：

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api \
  .venv/bin/python -m unittest discover -s api/tests -v
```

结果：

```text
Ran 3 tests in 0.007s
OK
```

覆盖：

- 默认查询选择当前 boot。
- 显式当前 boot 不返回旧工件。
- 显式旧 boot 返回旧工件。

### 4.2 Acceptance 工具回归

命令：

```bash
PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python -m unittest tests/test_acceptance_sprint.py -v
```

结果：

```text
Ran 5 tests
OK
```

新增测试确认默认、显式当前、显式旧 boot 三种调用保持隔离。

### 4.3 Static

- Python compile：`PASS`
- 相关文件 `git diff --check`：`PASS`

## 5. Live OpenAPI 部署核对

本地 OpenAPI 中 `/trace/api/by-cycle` 有 5 个参数：

```text
station_id
cycle_counter
plc_boot_id
plc_id
line_id
```

树莓派 live OpenAPI 实际只有：

```text
station_id
cycle_counter
```

这证明 Raspberry Pi 上正在运行的 API 容器仍是修复前版本。即使请求 URL 携带
`plc_boot_id`、`plc_id` 和 `line_id`，旧 FastAPI handler 也会忽略这些未知参数。

状态：`FAIL`

## 6. 真实跨 Boot 同 Counter 验证

命令：

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --by-cycle-only \
  --host 10.0.0.217 \
  --output /tmp/by_cycle_boot_isolation_validation.json
```

自动选中的真实样本：

| Field | Current | Historical |
| --- | --- | --- |
| PLC | PLC_001 | PLC_001 |
| Line | LINE_001 | LINE_001 |
| Station | WS03 | WS03 |
| Counter | 541 | 541 |
| Boot ID | `6266e5ac-d8aa-4e8b-b82e-32c9b87fe499` | `COLLECTOR-6defad45-8244-4e60-9bd3-ab88b3ad045c` |
| Unit ID | `U-20260619-000541` | `U-20260617-000541` |

最终验证门再次执行时，脚本独立选择了另一组样本：

| Field | Current | Historical |
| --- | --- | --- |
| Station | WS01 | WS01 |
| Counter | 550 | 550 |
| Boot ID | `6266e5ac-d8aa-4e8b-b82e-32c9b87fe499` | `COLLECTOR-6defad45-8244-4e60-9bd3-ab88b3ad045c` |
| Unit ID | `U-20260619-000550` | `U-20260617-000550` |

第二组样本得到相同结果：显式旧 boot 仍返回
`U-20260619-000550`，而不是 `U-20260617-000550`。因此失败可重复，不依赖 counter 541
这一条数据。

执行结果：

| Check | Result |
| --- | --- |
| 样本当前/历史 UID 不同 | PASS |
| 默认查询返回当前 UID | PASS |
| 显式当前 boot 返回当前 UID | PASS，但参数实际被旧 API 忽略 |
| 显式旧 boot 返回历史 UID | **FAIL**，仍返回当前 UID |
| 默认响应 events 带当前 boot ID | **FAIL**，字段缺失 |
| 显式当前响应 events 带当前 boot ID | **FAIL**，字段缺失 |
| 显式旧响应 events 带历史 boot ID | **FAIL**，字段缺失 |

关键事实：

```text
Expected historical unit: U-20260617-000541
Actual explicit-old result: U-20260619-000541
```

原始证据：

```text
/tmp/by_cycle_boot_isolation_validation.json
SHA-256:
7a923902dab5cd17452d78825ae4a499341e579ab7e5dcae2de00b8386e74e06

/tmp/by_cycle_boot_isolation_validation_final.json
SHA-256:
470977e8f0399053127b2c7a87d3f586c58636029af577cbc1b8858a5b2a5598
```

状态：`FAIL`

## 7. 原始 Acceptance 案例复查

请求：

```text
GET /trace/api/by-cycle
  ?station_id=WS01
  &cycle_counter=89
  &plc_boot_id=6266e5ac-d8aa-4e8b-b82e-32c9b87fe499
  &plc_id=PLC_001
  &line_id=LINE_001
```

Live API 返回当前 `U-20260619-000089`，但所有 event 的 `plc_boot_id` 均缺失。
这不是修复成功的证据：当前工件恰好是数据库中较新的记录，而 live handler 没有识别
新增参数。

## 8. 完整验收脚本重跑

命令：

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --host 10.0.0.217 \
  --output /tmp/acceptance_sprint_by_cycle_regression.json
```

结果：

```text
FAIL
KeyError: 'plc_id'
```

失败位置：

```text
validate_nok_scenario()
  → identity_event["plc_id"]
```

更新后的验收脚本要求 live Trace event 返回 identity 字段。旧 API 响应没有
`plc_id`、`line_id` 和 `plc_boot_id`，因此正式验收被正确阻断。

脚本在 `finally` 中恢复测试参数。失败后重新采集状态：

- Profile：`normal`
- Scale：`1.0`
- WS01 NOK rate：`0.02`
- WS02 NOK rate：`0.015`
- WS03 NOK rate：`0.01`
- 三站 forced NOK pending：`0`
- API：healthy
- Grafana：database `ok`
- Collector：三站 `RUNNING / CONNECTED`

恢复证据：

```text
/tmp/by_cycle_post_regression_snapshot.json
SHA-256:
f301212507b34cb138c3d01ce9b0bca2e0c856c92ddb52764f430eb3902ba4c0
```

## 9. Root Cause

本次回归失败不是本地修复代码错误，也不是数据库缺少测试数据。

证据链：

1. 本地 API 3/3 回归通过。
2. 本地 OpenAPI 含 5 个参数。
3. live OpenAPI 仅含旧版 2 个参数。
4. live 显式旧 boot 请求仍返回当前工件。
5. live event 响应没有新增 identity 字段。

根因：

> Data Quality Thread 的修复已存在于本地工作树，但 Raspberry Pi API 镜像/容器尚未
> 使用该修复代码重建和部署。

## 10. Acceptance Conclusion

`acceptance_report.md` 不可从 `CONDITIONAL PASS` 更新为 `PASS`。

ACPT-H-01 状态仍为：

```text
FAIL — local fixed, live not deployed
```

即使 ACPT-H-01 部署后通过，总报告中仍有以下独立事项：

- `/trace/api/recent` 的 `cycle_counter` 字段语义问题。
- 部署/回滚独立复验仍未完成。
- Grafana Profile 历史数据隔离仍为 PARTIAL。

因此当前继续保持：

```text
CONDITIONAL PASS / 有条件通过
```

## 11. Required Next Step

由有 Raspberry Pi 部署权限的 Thread/人员执行：

```bash
cd /opt/edge-mes-demo

# 同步修复后的 api/app/routes/trace.py
docker compose build api
docker compose up -d api
```

部署后必须再次执行：

```bash
PYTHONPATH=api .venv/bin/python -m unittest discover -s api/tests -v

.venv/bin/python scripts/run_acceptance_sprint.py \
  --by-cycle-only \
  --host 10.0.0.217 \
  --output /tmp/by_cycle_boot_isolation_validation.json

.venv/bin/python scripts/run_acceptance_sprint.py \
  --host 10.0.0.217 \
  --output /tmp/acceptance_sprint_by_cycle_regression.json
```

只有定向回归为 `PASS`，且 live OpenAPI 包含三个新增 identity 参数后，才能关闭
ACPT-H-01。
