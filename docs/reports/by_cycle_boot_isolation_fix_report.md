# Trace by-cycle Boot Isolation Fix Report

日期：2026-06-19  
问题编号：ACPT-H-01  
范围：`GET /trace/api/by-cycle`  
状态：本地修复与回归测试完成，待部署后由 Verification 复验

## 1. 问题根因

修复前，`/trace/api/by-cycle` 使用：

```sql
SELECT *
FROM cycle_event
WHERE station_id = %s
  AND cycle_counter = %s
ORDER BY id DESC
LIMIT 1;
```

该查询缺少 `plc_boot_id`。根据
[`../contracts/plc_identity_and_counter.md`](../contracts/plc_identity_and_counter.md)，
新的 PLC boot 允许 counter 从 0 或 1 重新开始，因此
`station_id + cycle_counter` 在历史数据中不是唯一事件身份。

冻结的核心身份为：

```text
plc_id + station_id + plc_boot_id + cycle_counter
```

验收 Sprint 中，当前 normal boot 的 WS01 counter 89 被错误解析为
`U-20260616-000089`，证明 `ORDER BY id DESC` 不能替代 boot identity。

根因仅位于 Trace API 查询层：

- `cycle_event` 已保存 `plc_id`、`line_id`、`plc_boot_id` 和 `cycle_counter`。
- Collector 已按完整 identity 持久化。
- `collector_runtime_status` 已保存各工站当前 boot identity。
- 不需要修改 PLC SIM 或 Collector。

## 2. 契约更新

修改：

- `docs/contracts/plc_identity_and_counter.md`

新增 Trace by-cycle 查询规则：

- 显式提供 `plc_boot_id` 时只查指定 boot。
- 未提供时从 `collector_runtime_status` 推导指定工站当前
  `plc_id + line_id + plc_boot_id`。
- 当前 boot 或目标 cycle 不存在时返回 404，不回退历史 boot。
- 找到 seed cycle 后，按 UID 或 legacy serial 补齐三站 Trace 时继续保持相同 boot
  范围。

## 3. 修改文件

| 文件 | 修改内容 |
| --- | --- |
| `docs/contracts/plc_identity_and_counter.md` | 增加 by-cycle 完整 identity 查询契约 |
| `api/app/routes/trace.py` | 实现当前 boot 推导、指定 boot 查询和 Trace 补齐范围隔离 |
| `api/tests/test_trace_by_cycle.py` | 新增三项 API 回归测试 |
| `scripts/run_acceptance_sprint.py` | 验收客户端支持 boot/plc/line 参数，NOK 场景增加 by-cycle 断言 |
| `tests/test_acceptance_sprint.py` | 增加验收客户端 URL 参数回归测试 |
| `docs/reports/by_cycle_boot_isolation_fix_report.md` | 本报告 |

未修改：

- `s7_plc_sim/`
- `collector/`
- ACK 协议和实现
- 数据库 schema
- Grafana dashboard

## 4. 查询逻辑变化

### 4.1 未指定 boot

请求保持兼容：

```text
GET /trace/api/by-cycle?station_id=WS01&cycle_counter=89
```

API 先从 `collector_runtime_status` 获取指定工站当前：

```text
plc_id
line_id
plc_boot_id
```

再查询：

```sql
WHERE station_id = :station_id
  AND cycle_counter = :cycle_counter
  AND plc_boot_id = :current_plc_boot_id
  AND plc_id = :current_plc_id
  AND line_id = :current_line_id
```

当前 runtime identity 或当前 boot 的目标 cycle 不存在时返回 404。

### 4.2 显式指定 boot

新增可选参数：

```text
plc_boot_id
plc_id
line_id
```

示例：

```text
GET /trace/api/by-cycle
  ?station_id=WS01
  &cycle_counter=89
  &plc_boot_id=6266e5ac-d8aa-4e8b-b82e-32c9b87fe499
  &plc_id=PLC_001
  &line_id=LINE_001
```

`plc_boot_id` 是指定历史 boot 查询的必要隔离字段；`plc_id` 和 `line_id` 用于进一步
收窄当前单机/单线范围。

### 4.3 三站 Trace 补齐

修复前，seed cycle 找到后，UID/serial 查询没有 boot 条件，理论上仍可能在补齐阶段
混入其他 boot 的事件。

修复后，by-cycle 路径会把 seed event 的：

```text
plc_id + line_id + plc_boot_id
```

继续传给：

- UID Trace 查询。
- serial Trace 查询。
- legacy 上游事件补齐查询。

响应中的每个 event 也新增：

- `plc_id`
- `line_id`
- `plc_boot_id`

方便调用方核对事件身份。

## 5. 数据库与索引评估

本次没有数据库变更。

现有约束：

```sql
UNIQUE (plc_id, station_id, plc_boot_id, cycle_counter)
```

已覆盖默认当前 boot 的核心精确查询。`line_id` 是附加范围字段，不改变冻结的事件唯一
身份。

显式指定旧 boot 但不提供 `plc_id` 时，查询仍可正确隔离；当前单机 Demo 数据规模不需要
额外索引。若未来扩展多 PLC 或历史数据量显著增长，再评估：

```text
(plc_boot_id, station_id, cycle_counter)
```

本次不为未来多产线场景提前修改 schema。

## 6. 新增测试

### API 回归

`api/tests/test_trace_by_cycle.py` 覆盖：

1. 相同 `station_id + cycle_counter` 在不同 `plc_boot_id` 中各有一条事件。
2. 不指定 boot 时，从 `collector_runtime_status` 推导当前 boot，不能返回旧工件。
3. 显式指定当前 boot 时，不能返回旧 boot 工件。
4. 显式指定旧 boot 时，正确返回旧 boot 对应工件。
5. Trace event 响应包含实际 `plc_boot_id`。

TDD RED 证据：

```text
旧代码运行 3 项测试：
FAILED (failures=2, errors=1)
```

失败内容包括：

- 默认查询返回 `U-20260616-000089`，预期 `U-20260619-000089`。
- 显式传入当前 boot 仍返回旧工件。
- 响应没有 `plc_boot_id`。

修复后：

```text
Ran 3 tests in 0.007s
OK
```

### Acceptance 工具回归

`tests/test_acceptance_sprint.py` 新增：

- 验收客户端正确发送 `plc_boot_id`、`plc_id`、`line_id`。

`validate_nok_scenario()` 在后续验收中会同时检查：

- 不指定 boot 的 by-cycle 查询返回当前工件。
- 显式指定 boot 的 by-cycle 查询返回同一工件。

## 7. 测试结果

| 检查 | 结果 |
| --- | --- |
| Trace API boot isolation | PASS，3/3 |
| Acceptance 工具单元测试 | PASS，4/4 |
| V-PLC 回归 | PASS，27/27 |
| Collector 回归 | PASS，12/12 |
| Python syntax compile | PASS，11 个相关文件 |
| Edge mapping validation | PASS |
| `git diff --check`（本次文件） | PASS |

Collector Snap7 集成测试结束时仍出现既有日志：

```text
Expected COTP DT, got 0x80
```

断言和退出码正常，与本次 Trace API 修复无关。

本次没有在树莓派上部署 API，因此 live endpoint 复验状态为 `NOT RUN`。

## 8. 对 Trace 页面影响

当前 Trace HTML 页面只调用：

- `/trace/api`
- `/trace/api/recent`

页面没有调用 `/trace/api/by-cycle`，因此本次参数扩展不会破坏页面现有功能。

现有 by-cycle 调用方式仍兼容：

```text
station_id + cycle_counter
```

行为变化仅为：默认查询当前 boot，不再从全部历史 boot 中猜测一条事件。

Trace event 响应增加 identity 字段属于 additive change，现有前端忽略未知字段，不受影响。

## 9. 是否建议 Verification 重新跑 Acceptance Sprint

建议重新执行。

部署 API 修复后，Verification 至少应执行：

1. 本地 API 回归：

   ```bash
   PYTHONPATH=api .venv/bin/python -m unittest discover -s api/tests -v
   ```

2. 在树莓派上构造或选择两个不同 boot、相同 station/counter 的事件。
3. 验证默认查询返回当前 boot 工件。
4. 验证显式当前 boot 返回当前工件。
5. 验证显式旧 boot 返回旧工件。
6. 重新执行 `scripts/run_acceptance_sprint.py`。更新后的 NOK 场景会自动验证默认和显式
   boot 的 by-cycle 查询。

ACPT-H-01 只有在部署后的 live API 完成上述验证后，才建议从 FAIL 改为 PASS。
