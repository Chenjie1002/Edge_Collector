# Recent API Cycle Counter Fix Report

日期：2026-06-19  
问题编号：ACPT-M-01  
范围：`GET /trace/api/recent`  
状态：本地修复与回归测试完成，待部署后由 Verification 复验

## 1. 问题根因

修复前，Recent API 直接从 `production_unit` 查询：

```sql
SELECT
  current_station_id AS station_id,
  current_route_step AS cycle_counter
FROM production_unit;
```

`production_unit.current_route_step` 表示工件当前工艺路线步骤：

```text
WS01 = 1
WS02 = 2
WS03 = 3
```

它不是 PLC 工站的 `cycle_counter`。

因此完成件通常返回：

```json
{
  "station_id": "WS03",
  "cycle_counter": 3
}
```

但同一工件真实 `cycle_event.cycle_counter` 可能是 `1287`。

2026-06-19 live 复现：

```text
Unit: U-20260619-001287
Recent cycle_counter: 3
Trace WS01/WS02/WS03 cycle_counter: 1287
```

问题只在 API 字段映射层：

- Collector 已正确持久化 `cycle_event.cycle_counter`。
- `production_unit.current_route_step` 本身数据正确。
- 不需要修改 PLC SIM、Collector 或数据库 schema。

## 2. 原字段语义

| 原字段 | 实际数据来源 | 实际语义 | 问题 |
| --- | --- | --- | --- |
| `cycle_counter` | `production_unit.current_route_step` | 工艺路线步骤 | 字段名声称是 PLC counter，实际是 1/2/3 |
| `station_id` | `production_unit.current_station_id` | 工件当前工站 | 与错误的 `cycle_counter` 同时展示，容易误认为工站 counter |

原实现会让 Trace 页面显示：

```text
WS03 · #3
```

而不是：

```text
WS03 · #1287 · Step 3
```

## 3. 修复后字段语义

已先更新：

- `docs/contracts/plc_identity_and_counter.md`

Recent API 字段定义：

| 字段 | 修复后语义 |
| --- | --- |
| `station_cycle_counter` | 该 UID 最新真实工站事件的 `cycle_event.cycle_counter` |
| `route_step` | `production_unit.current_route_step`，即当前工艺路线步骤 |
| `cycle_counter` | 兼容字段，值与 `station_cycle_counter` 相同 |
| `station_id` | `station_cycle_counter` 所属最新工站 |
| `plc_boot_id` | 最新工站事件所属 PLC boot |
| `plc_id` / `line_id` | 工件和最新事件所属 PLC/产线范围 |

Recent API 通过 `unit_id + plc_id + line_id` 关联该工件最新真实 `cycle_event`：

```sql
LEFT JOIN LATERAL (
    SELECT
           ce.station_id,
           ce.plc_boot_id,
           ce.cycle_counter
    FROM cycle_event ce
    WHERE ce.unit_id = pu.unit_id
      AND ce.plc_id = pu.plc_id
      AND ce.line_id = pu.line_id
    ORDER BY
           ce.route_step DESC NULLS LAST,
           ce.plc_end_time DESC NULLS LAST,
           ce.id DESC
    LIMIT 1
) latest_event ON TRUE
```

如果 legacy/incomplete 工件没有可关联的 `cycle_event`：

```text
station_cycle_counter = null
cycle_counter = null
route_step = production_unit.current_route_step
```

API 不再使用 route step 伪装成 cycle counter。

## 4. 修改文件

| 文件 | 修改内容 |
| --- | --- |
| `docs/contracts/plc_identity_and_counter.md` | 冻结 Recent API counter、route step 和兼容字段语义 |
| `api/app/routes/trace.py` | Recent 查询关联最新 cycle event，并更新 Trace 页面显示 |
| `api/tests/test_trace_recent.py` | 新增 Recent 字段语义回归测试 |
| `docs/reports/recent_api_cycle_counter_fix_report.md` | 本报告 |

未修改：

- `s7_plc_sim/`
- `collector/`
- `db/`
- `/trace/api`
- `/trace/api/by-cycle`
- Grafana dashboard

## 5. API 响应变化

### 修复前

```json
{
  "unit_id": "U-20260619-001287",
  "station_id": "WS03",
  "cycle_counter": 3
}
```

### 修复后

```json
{
  "unit_id": "U-20260619-001287",
  "plc_id": "PLC_001",
  "line_id": "LINE_001",
  "plc_boot_id": "6266e5ac-d8aa-4e8b-b82e-32c9b87fe499",
  "station_id": "WS03",
  "cycle_counter": 1287,
  "station_cycle_counter": 1287,
  "route_step": 3
}
```

### 兼容策略

- 保留已有 `cycle_counter` 字段，避免现有调用方因字段删除而失败。
- 修正 `cycle_counter` 的值，使其符合字段原本声称的 PLC counter 语义。
- 新增 `station_cycle_counter`，供新调用方使用明确名称。
- 新增 `route_step`，承载原来被错误塞入 `cycle_counter` 的值。
- 新增 identity 字段属于 additive change。

依赖旧错误行为、把 `cycle_counter=1/2/3` 当 route step 的外部调用方需要改用
`route_step`。这是必要的语义修正，不能继续保留错误值。

## 6. 前端与 Dashboard 影响

### Trace 页面

Trace 页面调用 `/trace/api/recent`。

修复前显示：

```text
WS03 · #3
```

修复后显示：

```text
WS03 · #1287 · Step 3
```

页面优先使用 `station_cycle_counter`，并保留 `cycle_counter` fallback，因此对新旧响应均
可渲染。

点击最近工件时仍优先使用 label、reject ID 或 unit ID 查询，不依赖 counter，现有追溯
功能不受影响。

### Grafana

现有 Grafana dashboard 直接查询 PostgreSQL，不调用 `/trace/api/recent`。

本次无需修改 Dashboard JSON。

### Acceptance 工具

`scripts/run_acceptance_sprint.py` 从 Recent API 选择 `unit_id`，没有依赖 Recent 返回的
错误 counter 值，因此现有完整验收流程不被破坏。

## 7. 数据库与性能

本次不修改数据库。

现有索引：

```text
idx_cycle_event_unit_id
```

可支持按 `unit_id` 查找工件事件。当前单机 Demo 不需要新增索引。

在 Raspberry Pi PostgreSQL 上只读执行同一查询形状，结果：

| Unit | State | Station | station_cycle_counter | route_step |
| --- | --- | --- | ---: | ---: |
| `U-20260619-001292` | WAITING_NEXT_STATION | WS02 | 1292 | 2 |
| `U-20260619-001293` | WAITING_NEXT_STATION | WS01 | 1293 | 1 |
| `U-20260619-001291` | COMPLETED_OK | WS03 | 1291 | 3 |

真实数据证明 counter 和 route step 已能明确分离。

## 8. 测试结果

### TDD RED

旧代码运行新增测试：

```text
Ran 2 tests
FAILED (errors=2)
```

失败原因：

- 响应没有 `station_cycle_counter`。
- 响应没有独立 `route_step`。
- legacy/incomplete 工件仍会把 route step 放入 `cycle_counter`。

### TDD GREEN

Recent API 专项测试：

```text
Ran 2 tests in 0.011s
OK
```

覆盖：

1. 最新真实 station counter 与 route step 分离。
2. `cycle_counter` 兼容字段等于真实 station counter。
3. `plc_boot_id` 与 counter 来自同一最新事件。
4. 无 cycle event 时 counter 返回 null，不使用 route step 填充。

### 全量本地回归

| Suite | Result |
| --- | --- |
| API tests | PASS，5/5 |
| Acceptance 工具 tests | PASS，6/6 |
| Python syntax | PASS，10 个 API 相关文件 |
| `git diff --check` | PASS |

by-cycle 的三项 boot isolation 测试全部通过，证明本次修改没有破坏
`/trace/api/by-cycle`。

## 9. 对 Verification 的复验建议

建议部署 API 后执行针对性复验：

1. 确认 `/trace/api/recent?status=completed_ok&limit=1` 返回：
   - `cycle_counter == station_cycle_counter`
   - `cycle_counter` 等于该 UID 最新 Trace event 的真实 counter
   - `route_step=3`
2. 确认 in-progress WS01/WS02 工件分别返回：
   - 正确 station counter
   - `route_step=1/2`
3. 确认 Trace 页面最近记录显示：

   ```text
   Station · #真实 counter · Step route_step
   ```

4. 重跑 API 测试和 Acceptance 工具测试。
5. 重新执行完整 Acceptance Sprint，确认：
   - Normal/NOK/Skip 流程不变。
   - by-cycle boot isolation 继续通过。

ACPT-M-01 只有在 Raspberry Pi live API 部署并完成上述验证后，才建议从 FAIL 更新为
PASS。
