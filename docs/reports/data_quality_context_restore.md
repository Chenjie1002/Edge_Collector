# Data Quality Context Restore

更新时间：2026-06-19  
恢复范围：Phase-1 Data Quality / Traceability 最终状态  
业务代码修改：无  
Phase-1 最终验收：`PASS`

> 本报告用于新 Thread 快速恢复上下文。它区分“Phase-1 已交付能力”和“已有规划但
> 尚未实现的 Data Gap 能力”。不要从早期 handoff 中的计划状态重新推断当前系统状态。

## 1. Phase-1 已完成内容

Phase-1 已完成：

1. 三工站工件 identity、counter、ACK 和 Trace 闭环。
2. OK、三工站 NOK、上游 NOK 后下游 `SKIPPED` 的端到端追溯。
3. Raw PLC Payload、cycle、unit、quality 与 Trace 结果交叉验证。
4. `/trace/api/by-cycle` 的 `plc_boot_id` 隔离。
5. `/trace/api/recent` 的真实 station counter 与 route step 语义拆分。
6. Grafana KPI 和趋势的 Profile 隔离及宽窗 `MIXED` 提示。
7. Raspberry Pi 定向部署、真实回滚恢复和完整 Acceptance Sprint。
8. Phase-1 最终验收结论：`PASS`。

## 2. 本 Thread 关键变更

### by-cycle

- 当前查询 identity 包含 boot、PLC、产线、工站和 counter。
- 相同 `cycle_counter`、不同 `plc_boot_id` 的工件不会串线。
- 默认查询当前 boot；显式历史 boot 可正确返回历史工件。

### Recent API

```text
cycle_counter = station_cycle_counter = 最新真实 cycle_event counter
route_step = production_unit.current_route_step
```

不再返回完成件恒为 `cycle_counter=3` 的错误语义。

### Grafana

- `profile` 默认 `normal`。
- 支持 `fast / test / unknown / All`。
- 12 条 `cycle_event` 查询应用 Profile scope。
- 宽时间窗多 Profile 显示 `MIXED`。
- 当前 Profile 与历史筛选 Profile 分开表达。

### 部署

```text
remote path = /opt/edge-mes-demo
backup = /home/mari/edge-mes-backups/final-deploy-20260619-214651
```

最终只部署：

```text
api/app/routes/trace.py
config/grafana/dashboards/edge_mes_station_traceability.json
```

## 3. 当前稳定状态

| 项目 | 状态 |
| --- | --- |
| Phase-1 Acceptance | PASS |
| Compose | 9/9 running |
| PostgreSQL | healthy |
| V-PLC | normal / scale 1.0 / strict ACK |
| Collector | 三站 RUNNING / CONNECTED |
| Recent API | counter 语义正确 |
| by-cycle | 跨 boot 隔离 PASS |
| Grafana | Profile 隔离 PASS |
| 真实回滚演练 | PASS |
| 完整 Acceptance Sprint | PASS |

最终验收样本确认：

- Recent `cycle_counter == station_cycle_counter`。
- Recent `cycle_counter != route_step`。
- by-cycle 当前和历史 boot 返回不同 UID，event scope 正确。
- 当前 boot counter 连续、无重复 identity、非 `ACK_OK` 为 0。
- Grafana 默认 `normal`，宽窗可见 `MIXED: fast, normal, test, unknown`。

## 4. 已知限制

### 未交付的 Data Gap 能力

以下能力不属于已完成的 Phase-1 功能：

- Ignore Edge 运行状态机。
- `data_gap_event` 自动创建、关闭、恢复和统计。
- WS03 Label 序号缺件计算。
- bypass 遗漏工件识别。
- counter jump gap 自动持久化。
- Missing Unit / Missing Station 专项查询。
- Gap 边界、持续时间和 Raw Sample Drill Down。
- Data Quality、Gap、Missing Station 独立 Dashboard。

当前只有：

- `docs/contracts/data_gap_event.md` 基础契约。
- `db/init/003_event_schema.sql` 中的基础表。
- DB104 的 `ignore_edge` 字段。

没有完整 Collector gap lifecycle。新 Thread 必须将其作为新功能实施，不得声称已经
存在。

### 其他限制

- 远程目录不是 Git 仓库。
- 历史数据包含旧快速周期、fast/test 和 unknown Profile。
- Legacy DB100 `production_snapshot` 与新三工站 V-PLC 数据路径分离。
- Phase-1 PASS 不代表真实 PLC、多产线、Oracle、认证和生产级长稳已完成。

## 5. 下一阶段建议

优先顺序：

1. 完善 `data_gap_event` contract，明确 Label 主口径、counter fallback、冲突和 unknown。
2. 添加最小 additive migration，不大改现有 schema。
3. 实现 Collector Ignore Edge / counter jump gap 生命周期和重启恢复。
4. Trace 增加 missing reason、gap boundary、duration 和 raw sample drill-down。
5. 增加 Data Quality / Gap / Missing Station Dashboard。
6. 增加 gap、ignore edge、missing unit、Trace API 回归测试。

回归保护：

- 不修改 ACK 协议。
- 不修改 `plc_boot_id` 和 counter reset 语义。
- 不破坏 `/trace/api/by-cycle` boot isolation。
- 不把 route step 再次作为 cycle counter。
- 不取消 Grafana Profile scope。
- 不补造不存在的 cycle event。

## 6. 新 Thread 如何恢复上下文

### 必读顺序

1. `docs/thread_handoff/data_quality.md`
2. `docs/reports/data_quality_context_restore.md`
3. `docs/reports/final_phase1_pass_report.md`
4. `docs/reports/acceptance_report.md`
5. `docs/reports/final_remote_deploy_report.md`
6. `docs/reports/recent_api_cycle_counter_fix_report.md`
7. `docs/reports/grafana_profile_mixing_fix_report.md`
8. `docs/contracts/plc_identity_and_counter.md`
9. `docs/contracts/vplc_runtime_parameters.md`
10. `docs/contracts/data_gap_event.md`

### 本地检查

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
git status --short
```

不要因工作树未提交而判定远程未部署。应核对最终报告和文件哈希。

### 远程检查

```bash
ssh edge-pi
cd /opt/edge-mes-demo
docker compose ps
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:3000/api/health
```

远程不执行 `git pull`。所有发布继续采用：

```text
备份 → 定向同步 → 只重建必要服务 → live 验证 → 报告
```

### 开始新开发前

1. 先确认任务是否属于已关闭 Phase-1 回归，还是新的 Data Gap 能力。
2. 若修改协议、schema 或公共 API，先更新 `docs/contracts/`。
3. 使用现有测试保护 by-cycle、Recent 和 Grafana Profile。
4. 明确单机 Demo 边界，Oracle、企业集成和多产线继续 Out of Scope。

## 7. 权威证据

- `docs/reports/final_phase1_pass_report.md`
- `docs/reports/acceptance_report.md`
- `docs/reports/final_remote_deploy_report.md`
- `docs/reports/rollback_drill_report.md`
- `docs/reports/by_cycle_boot_isolation_fix_report.md`
- `docs/reports/recent_api_cycle_counter_fix_report.md`
- `docs/reports/grafana_profile_mixing_fix_report.md`
