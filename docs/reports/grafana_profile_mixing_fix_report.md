# Grafana Profile Mixing Fix Report

日期：2026-06-19  
范围：单机、单产线、三工站 Edge MES Demo  
状态：**LOCAL FIX COMPLETE / 待部署后 Verification 复验**

## 1. 问题根因

`Edge MES 三工站追溯与采集监控` Dashboard 的产量、合格率、Cycle Time、NOK 和 ACK
查询只使用 Grafana 时间窗与工站条件，没有区分产生事件时的 V-PLC Profile。

`normal`、`fast`、`test` 的 cycle scale 不同，历史上还存在没有参数快照的旧 boot。
因此宽时间窗会把不同工况直接聚合，导致平均 Cycle Time、产量趋势和质量统计的解释口径
不清晰。

Raspberry Pi 现有数据库只读验证结果：

| Profile | Cycle 数 | Boot 数 | 平均 Cycle Time |
| --- | ---: | ---: | ---: |
| `normal` | 3945 | 2 | 29.905s |
| `fast` | 45 | 1 | 3.133s |
| `test` | 20 | 1 | 1.650s |
| `unknown` | 144671 | 3 | 5.011s |

这些数据若直接混合，平均值不再代表任何单一运行 Profile。

## 2. Profile 当前入库情况

Profile 已经入库，无需修改 Collector：

- `cycle_event.plc_boot_id` 保存每条 cycle 所属 PLC 启动周期。
- `vplc_parameter_snapshot.plc_boot_id` 与 `profile` 保存 V-PLC 参数快照。
- V-PLC Profile 在同一 boot 内保持确定，可通过 `plc_boot_id` 建立归属。

没有对应参数快照的历史 boot 归类为 `unknown`，不会推断为 `normal`。

## 3. 受影响 Dashboard

### 已修复

`config/grafana/dashboards/edge_mes_station_traceability.json`

受影响查询：

- WS03 OK 下线数。
- WS03 合格率。
- 三站平均 Cycle Time。
- ACK 未确认数。
- NOK 事件数。
- 三站 Cycle Time 趋势。
- 三站产出趋势。
- OK/NOK by Station。
- NOK Code 分布。
- 最近产品追溯记录。
- WS03 下线追溯入口。
- ACK 状态趋势。

### 不应用 Profile 过滤

- Collector 在线工站。
- Collector 运行状态。
- Raw PLC Sample 最新解码。

上述面板属于实时采集诊断，不是生产 KPI。

### Legacy Dashboard

`edge_mes_overview.json` 使用 `production_snapshot`，属于 legacy DB100 兼容演示口径。
该数据没有 DB101-104 V-PLC boot/Profile 归属，本次没有把它与三工站 Profile 强行
关联，也不应与三工站 KPI 合并解释。

## 4. 修复方案

### 4.1 Profile Filter

新增 Dashboard 变量：

```text
Profile = normal | fast | test | unknown | All
默认值 = normal
```

所有基于 `cycle_event` 的 KPI、趋势和追溯查询均通过：

```text
cycle_event.plc_boot_id
  -> vplc_parameter_snapshot.plc_boot_id
  -> vplc_parameter_snapshot.profile
```

应用 Profile 过滤。

选择 `All` 时允许跨 Profile 分析，但不再把结果伪装为单一工况。

### 4.2 当前 Profile

新增“当前 V-PLC Profile”面板：

- 从 `collector_runtime_status` 取得当前 `plc_boot_id`。
- 从该 boot 的最新 `vplc_parameter_snapshot` 取得 Profile。
- 无快照时显示 `unknown`。

该面板表示当前运行状态，不等同于用户选择的历史 Profile 筛选值。

### 4.3 宽时间窗提示

新增“时间窗 Profile 构成”面板。该查询故意不跟随 Profile filter，而是检查完整时间窗：

- 无数据：`NO DATA`
- 单一 Profile：显示 Profile 名称
- 多个 Profile：显示 `MIXED: ...`

现场 24 小时窗口验证结果：

```text
MIXED: fast, normal, test, unknown
```

默认 `normal` 过滤后的现场结果：

```text
cycles = 3945
avg_cycle_time = 29.905s
```

### 4.4 Recent Trace 时间窗

发现“最近产品追溯记录”原查询没有 `$__timeFilter`，会绕过 Dashboard 时间窗读取历史
事件。本次同时补上时间过滤和 Profile 过滤。

## 5. 修改文件

- `docs/contracts/vplc_runtime_parameters.md`
  - 增加 Dashboard Profile 归属契约。
- `docs/kpi_definitions.md`
  - 明确 Grafana KPI 的 Profile 过滤、`unknown` 和 `All/MIXED` 口径。
- `config/grafana/dashboards/edge_mes_station_traceability.json`
  - 新增 Profile 变量、当前 Profile、时间窗 Profile 构成，并修复相关查询。
- `tests/test_grafana_profile_filter.py`
  - 新增 Dashboard 配置回归测试。
- `docs/reports/grafana_profile_mixing_fix_report.md`
  - 记录本次修复范围与验证结果。

## 6. Schema 变更

**无 schema 变更。**

本次复用已有 `cycle_event.plc_boot_id` 和 `vplc_parameter_snapshot`。没有新增表、字段、
索引或 migration，也没有修改 Collector、PLC SIM、ACK 和 boot identity 逻辑。

当前 Demo 数据规模下无需为了该问题增加索引。若参数快照长期增长并出现 Dashboard 查询
延迟，可后续单独评估：

```sql
CREATE INDEX ... ON vplc_parameter_snapshot (plc_boot_id, captured_at DESC);
```

该建议不属于本次变更。

## 7. 测试与验证结果

### 自动化测试

```text
python -m unittest tests/test_grafana_profile_filter.py -v

Ran 4 tests
OK
```

覆盖：

- Profile 默认值为 `normal`。
- 支持 `fast/test/unknown/All`。
- 所有 `cycle_event` KPI/趋势/追溯查询应用 Profile scope。
- 当前 Profile 面板使用 Collector boot 与参数快照。
- 宽时间窗面板能返回 `MIXED`，且不被当前 Profile filter 遮蔽。
- 最近追溯表遵守 Grafana 时间窗。

### 静态检查

- Dashboard JSON parse：`PASS`
- `git diff --check`：`PASS`
- Dashboard panel layout：无重叠，Profile 状态面板位于顶部。

### 现场只读数据验证

- 宽窗 Profile 分类：`PASS`
- `MIXED` 提示查询：`PASS`
- `normal` 单 Profile KPI 查询：`PASS`
- 未写入数据库，未重启或部署服务。

## 8. 风险与限制

- 本次 Dashboard 文件尚未部署到 Raspberry Pi；远程 Grafana 当前仍运行部署前版本。
- `unknown` 历史量较大，这是旧 boot 缺少参数快照的真实结果，不应自动归入
  `normal`。
- 用户主动选择 `All` 后仍会得到混合 KPI，但顶部会明确显示 `MIXED`。
- Legacy Overview 不具备 Profile 归属，继续作为独立兼容演示 Dashboard 使用。

## 9. 对 Verification 的复验建议

建议在 Dashboard 文件安全部署并让 Grafana provisioning 重新加载后执行专项复验：

1. 默认打开 Dashboard，确认 Profile 为 `normal`。
2. 使用覆盖 normal/fast/test/旧数据的宽时间窗，确认顶部显示 `MIXED`。
3. 分别切换 `normal`、`fast`、`test`、`unknown`，核对 Cycle Time 与数据库结果。
4. 选择 `All`，确认混合结果存在但口径警示清晰。
5. 确认最近追溯记录受时间窗和 Profile 双重约束。
6. 确认 Collector 状态和 Raw Sample 实时诊断不受 Profile 过滤影响。

通过后可将 Acceptance Report 中“Grafana Profile 历史数据隔离”从 `PARTIAL` 更新为
`PASS`。无需重新执行完整长稳 Sprint，专项 Grafana/SQL 复验即可。
