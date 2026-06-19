# Verification Context Restore

更新时间：2026-06-19  
用途：新 Verification / Reliability / Data Quality Thread 的快速上下文恢复  
当前里程碑：**Edge MES Demo Phase-1 FINAL PASS**

## 1. 一句话状态

Raspberry Pi 上的单机、单产线、单 PLC、三工站 Edge MES Demo 已完成 Phase-1 最终
验收：9 个服务正常，PostgreSQL healthy，Normal/NOK/Skip、Trace、ACK、Recent API、
by-cycle boot isolation、Grafana Profile 隔离和真实 rollback drill 均为 `PASS`。

## 2. 恢复上下文的最短路径

按顺序读取：

1. [`final_phase1_pass_report.md`](final_phase1_pass_report.md)
2. [`acceptance_report.md`](acceptance_report.md)
3. [`final_remote_deploy_report.md`](final_remote_deploy_report.md)
4. [`rollback_drill_report.md`](rollback_drill_report.md)
5. [`../thread_handoff/verification.md`](../thread_handoff/verification.md)
6. [`../DOC_INDEX.md`](../DOC_INDEX.md)
7. [`../current_status.md`](../current_status.md)

若任务涉及语义或接口，再读取：

- [`../contracts/ack_protocol.md`](../contracts/ack_protocol.md)
- [`../contracts/plc_identity_and_counter.md`](../contracts/plc_identity_and_counter.md)
- [`../contracts/data_gap_event.md`](../contracts/data_gap_event.md)
- [`../contracts/vplc_runtime_parameters.md`](../contracts/vplc_runtime_parameters.md)

## 3. Phase-1 已完成

- V-PLC → Collector → PostgreSQL → FastAPI → Grafana 完整链路验证。
- 9 个远程 Compose 服务与 PostgreSQL health 验证。
- Normal、三站 NOK、Skip、Raw Payload、Quality Event、Trace 和 ACK 交叉验证。
- counter 连续性、UID 唯一性、事件幂等与 ACK 完整性验证。
- `/trace/api/by-cycle` 按 `plc_boot_id` 隔离并完成真实跨 boot 回归。
- `/trace/api/recent` 返回真实 station counter 和独立 `route_step`。
- Grafana Profile 默认 normal，支持 fast/test/unknown/All，宽时间窗显示 `MIXED`。
- 真实远程旧版 API 回滚、启动验证、最新版本恢复和完整回归。
- 最终 Acceptance Sprint 与 post-sprint 完整性快照。

最终状态：

```text
ACPT-H-01 CLOSED / PASS
ACPT-M-01 CLOSED / PASS
ACPT-M-05 CLOSED / PASS
Deployment rollback PASS
Phase-1 acceptance PASS
```

## 4. 本 Thread 的关键资产

### 自动化

```text
scripts/run_acceptance_sprint.py
tests/test_acceptance_sprint.py
tests/test_grafana_profile_filter.py
api/tests/test_trace_by_cycle.py
api/tests/test_trace_recent.py
```

常用命令：

```bash
# 只读快照
.venv/bin/python scripts/run_acceptance_sprint.py \
  --snapshot-only \
  --host 10.0.0.217 \
  --output /tmp/context_restore_snapshot.json

# by-cycle 定向回归
.venv/bin/python scripts/run_acceptance_sprint.py \
  --by-cycle-only \
  --host 10.0.0.217 \
  --output /tmp/context_restore_by_cycle.json

# 完整业务验收；会生成验收事件
.venv/bin/python scripts/run_acceptance_sprint.py \
  --host 10.0.0.217 \
  --output /tmp/context_restore_acceptance.json
```

### 最终原始证据

```text
/tmp/final_phase1_by_cycle.json
fe2279542d78279e6476b2c3e086d7e70f38bd9a54c32e8091bd7bb31ae144b3

/tmp/final_phase1_acceptance_sprint.json
ce8b0bb6248a614642313fa6de84a0d1c9b418271883764ff02734891d329de4

/tmp/final_phase1_post_sprint_snapshot.json
5e766bcdc2a2c50162c226e50de556faf9a2d16e072ed75f0a3273510adf5cd8
```

`/tmp` 文件可能随机器清理而消失；长期结论以 `docs/reports/` 中的报告为准。

## 5. 当前远程稳定基线

```text
SSH alias: edge-pi
Host: Pi-5b-Li / 10.0.0.217
Path: /opt/edge-mes-demo
Services: 9/9 running
PostgreSQL: healthy
API: http://10.0.0.217:8000
Grafana: http://10.0.0.217:3000
V-PLC: http://10.0.0.217:8200
Profile: normal
Scale: 1.0
ACK: strict / require_ack=true
```

最终部署文件：

```text
api/app/routes/trace.py
f2fced93a706a0642ea2c72fcf97d4ac1b9198fa05b7936f4107b4905265e7f4

config/grafana/dashboards/edge_mes_station_traceability.json
b62e2a0186442a9f857c89892b749bb41827d1f67e106babaab26d68df1a1283
```

恢复点：

```text
/home/mari/edge-mes-backups/rollback-drill-20260619-213700
/home/mari/edge-mes-backups/final-deploy-20260619-214651
```

## 6. 快速只读健康检查

```bash
ssh edge-pi
cd /opt/edge-mes-demo

docker compose ps
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:3000/api/health
curl -fsS http://127.0.0.1:8200/vplc/state
curl -fsS "http://127.0.0.1:8000/trace/api/recent?status=completed_ok&limit=3"
```

预期：

- 9 个服务 running。
- PostgreSQL healthy。
- Recent `cycle_counter == station_cycle_counter`。
- `route_step` 独立返回。
- V-PLC 为 normal / scale 1.0 / require_ack true。

## 7. 已知限制

- Phase-1 只覆盖单机、单线、单 PLC、三工站离线 Demo。
- Oracle Sync、真实 Oracle、企业集成、多产线均未验收。
- Rework 未定义，当前为 `N/A`。
- 尚无 24 小时以上生产化长稳认证和正式资源 SLA。
- 发布/回滚尚未脚本化；远程目录不是 Git working tree。
- Grafana anonymous/datasource 权限只适合可信 Demo LAN。
- legacy DB100 dashboard 不具备 DB101-104 Profile 归属。
- Phase-1 PASS 不代表真实 PLC、安全、性能或生产运维认证。

## 8. 下一阶段建议

1. deploy/rollback 自动化与发布 manifest。
2. Raspberry Pi 24 小时以上 soak 和故障恢复矩阵。
3. Grafana anonymous 与 datasource 权限收紧。
4. Compose 自动恢复、日志、资源、磁盘和容量验收。
5. 真实 PLC 接入前重新确认 S7 identity、counter、ACK 与 gap 契约。
6. Oracle Sync、多产线、Rework 等新范围建立独立合同、测试计划和验收结论。

## 9. 新 Thread 开始时的规则

- 先执行只读检查，再判断是否需要完整 Sprint。
- 完整 Sprint 会产生 Normal/NOK/Skip 验收事件，不应作为普通健康探针。
- 不修改业务逻辑来迁就测试。
- 不覆盖 `.env`、Compose 或 `data/`。
- 协议、数据库结构、公共接口变化必须先更新 `docs/contracts/`。
- 不把 Phase-1 PASS 外推为生产交付 PASS。
- 不重复创建现有 handoff、验收和测试文档。
