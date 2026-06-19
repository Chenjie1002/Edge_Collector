# Data Quality Thread Handoff

更新时间：2026-06-19  
Thread：Data Quality / Traceability  
Phase-1 最终状态：`PASS`  
业务代码修改：本次最终 handoff 无

> Phase-1 已完成最终验收。本文件取代 2026-06-18 的实施前计划，作为后续 Thread
> 恢复 Data Quality、Trace API 和 Grafana 数据口径的首要入口。旧文档中的
> “计划待确认”“尚未实施”等状态不再代表 Phase-1 整体状态。

## 1. Phase-1 已完成内容

Phase-1 已在单机、单产线、单 PLC、WS01/WS02/WS03 三工站范围内完成：

- V-PLC、Collector、PostgreSQL、FastAPI、Grafana 的完整闭环。
- 稳定的 `plc_boot_id`、工站 `cycle_counter` 和严格 ACK 语义。
- `unit_id` 贯穿三工站，OK、三工站 NOK、上游 NOK 后下游 `SKIPPED` 可追溯。
- Raw PLC Payload、`cycle_event`、`quality_event`、Trace 和 Dashboard 交叉验证。
- `/trace/api/by-cycle` 按 boot、PLC、产线、工站和 counter 隔离。
- `/trace/api/recent` 返回真实工站 counter，并将工艺步骤拆为 `route_step`。
- Grafana 对 `normal / fast / test / unknown` Profile 进行明确隔离。
- 真实远程部署、备份、恢复、回滚演练和最终 Acceptance Sprint。

最终验收结论：

```text
Phase-1 = PASS
```

权威结果见：

- [`../reports/final_phase1_pass_report.md`](../reports/final_phase1_pass_report.md)
- [`../reports/acceptance_report.md`](../reports/acceptance_report.md)

## 2. 本 Thread 负责的关键变更

### 2.1 by-cycle Boot Isolation

修复 `/trace/api/by-cycle` 跨 PLC 启动周期返回旧工件的问题。

查询 identity 固定为：

```text
plc_boot_id
+ plc_id
+ line_id
+ station_id
+ cycle_counter
```

行为：

- 未指定 boot 时选择当前运行 boot。
- 指定当前 boot 时只返回当前工件。
- 指定历史 boot 时只返回该历史工件。
- 返回的全部 events 必须属于目标 boot。

相关文件：

- `api/app/routes/trace.py`
- `api/tests/test_trace_by_cycle.py`
- `scripts/run_acceptance_sprint.py`
- `tests/test_acceptance_sprint.py`
- `docs/contracts/plc_identity_and_counter.md`

### 2.2 Recent API Counter 语义

修复 `/trace/api/recent` 将 `production_unit.current_route_step` 错误作为
`cycle_counter` 返回的问题。

当前字段口径：

| 字段 | 语义 |
| --- | --- |
| `station_cycle_counter` | 最新真实 `cycle_event.cycle_counter` |
| `cycle_counter` | 兼容字段，等于 `station_cycle_counter` |
| `route_step` | `production_unit.current_route_step` |
| `station_id` | 最新真实工站事件所属工站 |
| `plc_boot_id` | 最新事件所属启动周期 |
| `plc_id` / `line_id` | 工件所属 PLC 与产线范围 |

没有真实 cycle event 时，counter 返回 `null`，不得用 route step 填充。

相关文件：

- `api/app/routes/trace.py`
- `api/tests/test_trace_recent.py`
- `docs/contracts/plc_identity_and_counter.md`
- `docs/reports/recent_api_cycle_counter_fix_report.md`

### 2.3 Grafana Profile 隔离

`Edge MES 三工站追溯与采集监控` 已新增：

- `profile` 变量，默认 `normal`。
- `fast / test / unknown / All` 选项。
- “当前 V-PLC Profile”面板。
- “时间窗 Profile 构成”面板。
- 宽时间窗多 Profile 时显示 `MIXED: ...`。

12 条基于 `cycle_event` 的 KPI、趋势和追溯查询使用：

```text
cycle_event.plc_boot_id
  -> vplc_parameter_snapshot.plc_boot_id
  -> profile
```

进行过滤。Collector 状态和 Raw Sample 仍作为实时诊断数据，不参与生产 KPI Profile
过滤。

相关文件：

- `config/grafana/dashboards/edge_mes_station_traceability.json`
- `tests/test_grafana_profile_filter.py`
- `docs/contracts/vplc_runtime_parameters.md`
- `docs/kpi_definitions.md`
- `docs/reports/grafana_profile_mixing_fix_report.md`

### 2.4 部署与验收

- 远程路径：`/opt/edge-mes-demo`
- 远程目录不是 Git 仓库，不使用 `git pull`。
- Recent API 与 Grafana 修复已定向部署。
- 真实 API 回滚和恢复演练：`PASS`。
- by-cycle 跨 boot 定向回归：`PASS`。
- 完整 Acceptance Sprint：`PASS`。

最终部署恢复点：

```text
/home/mari/edge-mes-backups/final-deploy-20260619-214651
```

## 3. 当前稳定状态

```text
Phase-1 acceptance = PASS
remote path = /opt/edge-mes-demo
Compose services = 9/9 running
PostgreSQL = healthy
V-PLC profile = normal
cycle scale = 1.0
strict ACK = enabled
Collector = WS01/WS02/WS03 RUNNING / CONNECTED
non-ACK_OK in accepted current-boot events = 0
duplicate event identity = 0
```

当前已验证：

- normal、WS01 NOK、WS02 NOK、WS03 NOK、Skip、Trace 和 Quality Event。
- Recent API 的 `cycle_counter == station_cycle_counter`，`route_step` 独立。
- by-cycle 默认、显式当前 boot 和显式历史 boot 均严格隔离。
- Grafana Profile 默认 `normal`，宽窗混合状态可见。
- `.env`、Compose 文件和数据 volume 未被最终部署覆盖。

最终发布文件 SHA-256：

```text
api/app/routes/trace.py
f2fced93a706a0642ea2c72fcf97d4ac1b9198fa05b7936f4107b4905265e7f4

config/grafana/dashboards/edge_mes_station_traceability.json
b62e2a0186442a9f857c89892b749bb41827d1f67e106babaab26d68df1a1283
```

## 4. 已知限制

### 4.1 Data Gap 专项尚未进入 Phase-1 实现

以下能力已有契约或占位 schema，但未作为 Phase-1 验收功能交付：

- `ignore_edge` 上升沿创建 gap。
- bypass 结束后由首个有效 WS03 event 关闭 gap。
- `data_gap_event` 完整生命周期与幂等恢复。
- WS03 Label 序号缺件计算。
- counter jump 自动形成 gap。
- Missing Unit / Missing Station 专项统计。
- Gap、Missing Station、Data Quality 独立 Dashboard。
- Trace 中的 Gap 边界和 Raw Sample Drill Down 专项模型。

`db/init/003_event_schema.sql` 中存在 `data_gap_event` 基础表，
`docs/contracts/data_gap_event.md` 存在基础契约，但 Collector 尚无完整 gap 写入状态机。
后续 Thread 不得把“有表/有契约”误判为“功能已实现”。

### 4.2 历史数据

- PostgreSQL 中存在旧约 4–5 秒数据、`fast/test` 验收数据和没有 Profile 快照的旧
  boot。
- 无参数快照的 boot 归类为 `unknown`，不得推断为 `normal`。
- Legacy `edge_mes_overview.json` 使用 `production_snapshot`，不具备新三工站
  V-PLC Profile 归属，不能与 Profile KPI 混合解释。

### 4.3 产品化边界

Phase-1 `PASS` 表示受控 Demo 验收通过，不等同于生产认证。尚未覆盖：

- 真实 PLC 和现场网络。
- 多产线。
- Oracle 真实同步和企业集成。
- 完整认证授权。
- 统一自动部署系统。
- 24 小时以上生产级长稳、资源和磁盘容量专项验收。
- 媒体、归档和 AI。

## 5. 下一阶段建议

### P1：Data Gap 生命周期

1. 先复核并补充 `docs/contracts/data_gap_event.md`。
2. 基于现有 DB104 `ignore_edge`、稳定 `plc_boot_id` 和 counter 实现 Collector gap
   状态机。
3. 使用数据库中的 open gap 作为恢复真源，确保 Collector 重启不重复创建。
4. bypass 期间不补造 cycle event，不修改 ACK 行为。

### P2：缺件和缺站解释

1. WS03 有有效 Label 序号时，以 Label 差值为缺件主口径。
2. counter 作为 fallback 和一致性校验。
3. 明确区分 `PROCESSED_NOK`、`SKIPPED`、`MISSING_GAP` 和
   `MISSING_UNEXPLAINED`。
4. 不使用时间邻近关系伪造缺失工站事件。

### P3：Trace 与 Dashboard

1. Trace 返回 gap 起止边界、持续时间、缺件数、计数依据和可信状态。
2. 提供 `raw_sample_id` Drill Down。
3. 增加 Data Quality、Gap、Missing Station Dashboard。
4. Dashboard 继续保持 Profile/boot/time scope，不回退为宽窗混合查询。

### P4：验证

至少覆盖：

- Ignore Edge 上升沿幂等创建。
- 下降沿后首个 WS03 event 关闭。
- Collector 在 open gap 中重启。
- Label/counter 一致、fallback、冲突和未知边界。
- Missing Station 与 `SKIPPED/NOK` 不混淆。
- 新能力不破坏 strict ACK、boot isolation、Recent 语义和 Profile Dashboard。

## 6. 新 Thread 如何恢复上下文

### 最小阅读顺序

1. [`../reports/data_quality_context_restore.md`](../reports/data_quality_context_restore.md)
2. [`../reports/final_phase1_pass_report.md`](../reports/final_phase1_pass_report.md)
3. [`../reports/acceptance_report.md`](../reports/acceptance_report.md)
4. [`../reports/final_remote_deploy_report.md`](../reports/final_remote_deploy_report.md)
5. [`../reports/recent_api_cycle_counter_fix_report.md`](../reports/recent_api_cycle_counter_fix_report.md)
6. [`../reports/grafana_profile_mixing_fix_report.md`](../reports/grafana_profile_mixing_fix_report.md)
7. [`../contracts/plc_identity_and_counter.md`](../contracts/plc_identity_and_counter.md)
8. [`../contracts/vplc_runtime_parameters.md`](../contracts/vplc_runtime_parameters.md)
9. [`../contracts/data_gap_event.md`](../contracts/data_gap_event.md)
10. [`../current_status.md`](../current_status.md)

### 本地恢复

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
git status --short
```

当前工作树可能包含 Phase-1 的未提交文件。不要只凭 Git 状态判断功能是否部署，应以
最终报告、文件哈希和 live 运行证据为准。

### 远程只读恢复

```bash
ssh edge-pi
cd /opt/edge-mes-demo
docker compose ps
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:3000/api/health
```

远程不是 Git 仓库，不执行 `git pull`。如需部署：

```text
本地确认精确文件
→ 创建远程新备份
→ 定向同步
→ 只重建必要服务
→ 验证 Compose/API/Grafana/回归
→ 更新 docs/reports/
```

### 新 Thread 工作原则

- Phase-1 已验收 `PASS`，不要重复实施已关闭的 by-cycle、Recent 或 Profile 修复。
- Data Gap 仍是下一阶段新功能，开始编码前必须先确认 contract 与 schema 方案。
- 修改协议、schema 或公共 API 时，严格遵守：

  ```text
  docs/contracts/ → code/config/migration → tests → docs/reports/
  ```

- 不修改冻结的 ACK、`plc_boot_id` 和 counter 语义。
- Oracle、多产线和企业集成继续保持 Out of Scope，除非新的项目范围明确启动。

## 7. 权威证据入口

- [`../reports/final_phase1_pass_report.md`](../reports/final_phase1_pass_report.md)
- [`../reports/acceptance_report.md`](../reports/acceptance_report.md)
- [`../reports/final_remote_deploy_report.md`](../reports/final_remote_deploy_report.md)
- [`../reports/rollback_drill_report.md`](../reports/rollback_drill_report.md)
- [`../reports/by_cycle_boot_isolation_fix_report.md`](../reports/by_cycle_boot_isolation_fix_report.md)
- [`../reports/recent_api_cycle_counter_fix_report.md`](../reports/recent_api_cycle_counter_fix_report.md)
- [`../reports/grafana_profile_mixing_fix_report.md`](../reports/grafana_profile_mixing_fix_report.md)
