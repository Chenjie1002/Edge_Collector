# Verification Thread Handoff

更新时间：2026-06-19  
状态：**Phase-1 FINAL ACCEPTANCE PASS**  
目标环境：Raspberry Pi `Pi-5b-Li`（`10.0.0.217`）  
SSH alias：`edge-pi`  
远程路径：`/opt/edge-mes-demo`

## 1. 当前结论

单机、单产线、单 PLC、三工站 Edge MES Demo 的 Phase-1 验收已完成，最终结论：

```text
PASS / 通过
```

最终证据：

- [`../reports/final_phase1_pass_report.md`](../reports/final_phase1_pass_report.md)
- [`../reports/acceptance_report.md`](../reports/acceptance_report.md)
- [`../reports/final_remote_deploy_report.md`](../reports/final_remote_deploy_report.md)
- [`../reports/rollback_drill_report.md`](../reports/rollback_drill_report.md)

本结论表示系统具备受控环境下客户演示条件，不等同于生产交付认证。

## 2. Phase-1 已完成内容

### 2.1 完整闭环

已验证：

```text
V-PLC
  ↓
Collector
  ↓
PostgreSQL
  ↓
FastAPI
  ↓
Grafana
```

- 远程 9 个 Compose 服务运行正常。
- PostgreSQL 为 `healthy`。
- Collector 三站均为 `RUNNING / CONNECTED`。
- V-PLC 最终为 `normal`、`scale=1.0`、`require_ack=true`。
- API 与 Grafana health 正常。

### 2.2 业务与可靠性

- Normal / OK Flow：PASS。
- WS01、WS02、WS03 确定性 NOK：PASS。
- 上游 NOK 后下游 SKIPPED：PASS。
- Trace 三站 UID、counter、顺序、结果与 ACK 一致：PASS。
- ACK、payload 保留、幂等、boot identity、counter reset 等组件回归通过。
- 当前 boot counter 连续，未发现重复事件键。
- WS03 UID 唯一且 serial 连续。
- 当前 boot 非 `ACK_OK` 数量为 0。
- Rework：`N/A`，Phase-1 未定义该业务，不得自行新增。

### 2.3 已关闭问题

| Issue | 最终状态 | 关闭证据 |
| --- | --- | --- |
| ACPT-H-01：`/trace/api/by-cycle` 跨 boot 返回旧工件 | CLOSED / PASS | 默认、显式当前 boot、显式历史 boot 和 event scope 均通过 |
| ACPT-M-01：Recent API 把 route step 当 cycle counter | CLOSED / PASS | live `cycle_counter = station_cycle_counter`，`route_step` 独立返回 |
| ACPT-M-05：Grafana 宽时间窗混合 Profile | CLOSED / PASS | 默认 normal、12 条查询应用 Profile scope、宽窗显示 `MIXED` |
| Deployment rollback | PASS | 已执行真实旧版 API 回滚、恢复和完整回归 |

### 2.4 最终 Acceptance Sprint

最终执行：

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --host 10.0.0.217 \
  --output /tmp/final_phase1_acceptance_sprint.json
```

结果：

- Normal：`U-20260619-001379` / counter 1379。
- WS01 NOK：code 10001。
- WS02 NOK：code 20001。
- WS03 NOK：code 30001。
- Skip、Profile history、Trace、ACK、API/Grafana health：PASS。
- `restore_errors=[]`。
- NOK rate 恢复为 `0.02 / 0.015 / 0.01`。
- pending forced NOK 恢复为 `0 / 0 / 0`。

最终 Sprint 后快照：

```text
WS01 rows = unique counters = max counter = 1390
WS02 rows = unique counters = max counter = 1389
WS03 rows = unique counters = max counter = 1388
WS03 UID = 1388 / 1388 unique
non-ACK_OK = 0
duplicate event keys = 0
```

## 3. 本 Thread 负责的关键变更

本 Thread 的职责是验证和报告，不主动修改业务逻辑。

### 3.1 验收自动化

- 建立并维护 `scripts/run_acceptance_sprint.py`：
  - Normal Flow。
  - 三站确定性 NOK 与 Skip。
  - Raw Payload、`quality_event`、`cycle_event`、Trace 交叉验证。
  - by-cycle 默认/显式 boot 隔离回归。
  - Profile 历史、Collector、API、Grafana 和数据完整性快照。
  - 测试结束后自动恢复 NOK rate。
- 增加 `tests/test_acceptance_sprint.py`。
- 增加 `tests/test_grafana_profile_filter.py`。
- 增加 API by-cycle 与 Recent 语义回归测试。

验收工具曾因历史数据增长导致跨 boot 样本 SQL 达到 Grafana 15 秒 timeout。测试查询已
改为先限制当前 boot 最近 200 条候选，再配对历史 boot；该修改只影响测试样本选择，不
改变业务代码或数据库。

### 3.2 远程验证

- 独立验证 Raspberry Pi 实际运行目录和 Compose 状态。
- 验证 API/Grafana live 部署文件哈希。
- 验证 Recent API、Grafana Profile Dashboard 和 by-cycle live 行为。
- 执行真实 API rollback drill。
- 确认回滚与恢复期间非目标容器、Compose、`.env` 和持久化目录基线不变。

### 3.3 报告资产

本 Thread 产出的核心报告包括：

- `verification_report.md`
- `reliability_report.md`
- `acceptance_report.md`
- `by_cycle_boot_isolation_validation_report.md`
- `final_acceptance_validation_report.md`
- `rollback_drill_report.md`
- `final_phase1_pass_report.md`
- `verification_context_restore.md`

不要重复创建新的“最终验收报告”；后续状态更新优先修改现有报告或建立明确的下一阶段
报告。

## 4. 当前稳定状态

最终远程运行基线：

```text
Remote path: /opt/edge-mes-demo
Compose services: 9/9 running
PostgreSQL: healthy
API health: ok
Grafana database: ok
Grafana version: 13.0.2
Profile: normal
Scale: 1.0
Strict ACK: enabled
```

最终部署哈希：

```text
api/app/routes/trace.py
f2fced93a706a0642ea2c72fcf97d4ac1b9198fa05b7936f4107b4905265e7f4

config/grafana/dashboards/edge_mes_station_traceability.json
b62e2a0186442a9f857c89892b749bb41827d1f67e106babaab26d68df1a1283
```

远程恢复点：

```text
/home/mari/edge-mes-backups/rollback-drill-20260619-213700
/home/mari/edge-mes-backups/final-deploy-20260619-214651
```

## 5. 已知限制

以下项目不阻塞 Phase-1 PASS，但仍需保留：

- Oracle Sync 仍不在本阶段验收范围；`sync-worker` 只保留 mock。
- Phase-1 没有定义 Rework Flow。
- 尚未完成 24 小时以上生产化长稳认证；现有证据包括超过 1 小时连续运行。
- 尚未完成 CPU、内存、磁盘、温度和容量的正式阈值/SLA 认证。
- 远程目录不是 Git working tree，发布与回滚仍依赖文件备份、哈希和人工定向重建。
- 尚无统一、可重复执行的 deploy/rollback 脚本和发布 manifest。
- Grafana 匿名 Viewer 可调用 datasource 查询；适合可信 Demo LAN，不适合直接暴露给
  客户网络或生产网络。
- Grafana 启动日志存在缺少可选 `plugins/alerting` provisioning 目录的提示，不影响
  当前 Dashboard provisioning 和 health。
- legacy DB100 dashboard 与三工站 DB101-104 Profile KPI 是两个口径，不应混合解释。
- Phase-1 PASS 是受控 Demo 验收，不代表真实 PLC、多产线、安全、性能和生产运维认证。

## 6. 下一阶段建议

建议按以下顺序推进：

1. 建立统一 deploy/rollback 脚本、发布 manifest、备份校验和 post-deploy gate。
2. 执行 Raspberry Pi 24 小时以上 soak：
   - Collector、V-PLC、PostgreSQL 故障恢复。
   - counter、UID、ACK、gap 和资源趋势。
   - CPU、内存、磁盘、温度和数据增长。
3. 收紧 Grafana anonymous 与 PostgreSQL datasource 权限。
4. 补充 Compose、日志、磁盘和重启自恢复的生产化验收。
5. 若进入真实 PLC 阶段，按契约优先方式扩展 S7-300/1200/1500 接入，不复用 Demo
   假设作为生产协议。
6. Oracle Sync、多产线、Rework 等新业务必须建立新的范围和契约，不能直接纳入
   Phase-1 PASS。

## 7. 新 Thread 如何恢复上下文

新 Thread 开始时按以下顺序读取：

1. [`../DOC_INDEX.md`](../DOC_INDEX.md)
2. [`../current_status.md`](../current_status.md)
3. [`../reports/verification_context_restore.md`](../reports/verification_context_restore.md)
4. [`../reports/final_phase1_pass_report.md`](../reports/final_phase1_pass_report.md)
5. [`../reports/acceptance_report.md`](../reports/acceptance_report.md)
6. [`../reports/final_remote_deploy_report.md`](../reports/final_remote_deploy_report.md)
7. [`../reports/rollback_drill_report.md`](../reports/rollback_drill_report.md)
8. 根据任务读取 `contracts/` 中对应契约。

恢复后先执行只读基线：

```bash
ssh edge-pi
cd /opt/edge-mes-demo
docker compose ps
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:3000/api/health
curl -fsS http://127.0.0.1:8200/vplc/state
```

必要时执行：

```bash
.venv/bin/python scripts/run_acceptance_sprint.py \
  --snapshot-only \
  --host 10.0.0.217 \
  --output /tmp/context_restore_snapshot.json

.venv/bin/python scripts/run_acceptance_sprint.py \
  --by-cycle-only \
  --host 10.0.0.217 \
  --output /tmp/context_restore_by_cycle.json
```

不要一开始就运行完整 Sprint；完整 Sprint 会生成 Normal/NOK/Skip 验收事件。只有任务
明确要求重新验收时再执行。

## 8. 不可违反的边界

- 不修改 ACK、PLC identity、counter 或 Data Gap 定义。
- 任何协议、数据库结构或公共接口变化：先更新 `docs/contracts/`，再修改代码，最后
  在 `docs/reports/` 记录影响。
- 不为让测试通过而修改业务逻辑。
- 不覆盖远程 `.env`、Compose 或 `data/`。
- 不重复创建已有测试或验收文档。
- Oracle Sync 在单机 Demo 验收中保持 Out of Scope。
