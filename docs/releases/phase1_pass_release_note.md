# Edge MES Demo Phase-1 PASS Release Note

发布日期：2026-06-19  
发布状态：**PASS / 版本冻结**  
发布标签：`phase1-pass-20260619`

## 1. Phase-1 目标

交付可在 Raspberry Pi 独立运行的单机、单产线、单 PLC、三工站 Edge MES Demo，
打通 V-PLC、Collector、PostgreSQL、FastAPI 与 Grafana，并以可重复的验收和回滚证据
确认核心生产闭环。

## 2. 最终验收结论

Phase-1 最终验收结论为：

```text
PASS / 通过
```

Phase-1 阻塞项已关闭。权威结论见：

- [`../reports/final_phase1_pass_report.md`](../reports/final_phase1_pass_report.md)
- [`../reports/acceptance_report.md`](../reports/acceptance_report.md)
- [`../reports/rollback_drill_report.md`](../reports/rollback_drill_report.md)

## 3. 核心能力

- 单机、单线、单 PLC、WS01/WS02/WS03 三工站 V-PLC 模拟。
- PLC identity、`plc_boot_id`、station counter、strict ACK 与重启恢复语义。
- Normal、三工站 NOK、上游 NOK 后下游 `SKIPPED` 的端到端追溯。
- Raw PLC Payload、`cycle_event`、`production_unit`、`quality_event` 与 Trace 交叉验证。
- `/trace/api/by-cycle` 按 boot、PLC、产线、工站和 counter 隔离。
- `/trace/api/recent` 返回真实 station counter，并独立表达 `route_step`。
- Grafana KPI、趋势与 Trace 查询支持 Profile 隔离，宽时间窗可识别 `MIXED`。
- V-PLC Profile、运行参数审计、确定性 NOK 注入和 Acceptance Sprint。
- 远程定向部署、备份、真实回滚与恢复验证。

## 4. 远程部署

远程部署路径：

```text
/opt/edge-mes-demo
```

连接方式：

```bash
ssh edge-pi
```

`edge-pi` 是本地 SSH alias。本仓库和本发布说明不包含 SSH 私钥、密码、token 或其他
登录凭据。远程目录不是 Git working tree，发布继续采用“备份 → 定向同步 → 只重建必要
服务 → live 验证 → 报告”的方式，不在远程执行 `git pull`。

## 5. 测试结果

| 验证项 | 结果 |
| --- | --- |
| Compose 服务 | PASS，9/9 running |
| PostgreSQL | PASS，healthy |
| Normal / NOK / Skip | PASS |
| Raw Payload / Quality Event / Trace | PASS |
| Strict ACK | PASS |
| counter 连续性与幂等 | PASS |
| UID 唯一性 | PASS |
| Recent API counter 语义 | PASS |
| by-cycle boot isolation | PASS |
| Grafana Profile 隔离 | PASS |
| Raspberry Pi 连续运行 | PASS，超过 1 小时 |
| 真实回滚与恢复 | PASS |
| 完整 Acceptance Sprint | PASS |
| 本地 API、Grafana 与 Acceptance 回归 | PASS |

## 6. 已知限制

- 仅覆盖单机、单产线、单 PLC、三工站离线 Demo。
- 不代表真实 PLC、安全、性能、容量或生产运维认证。
- Oracle Sync、真实 Oracle、企业集成和多产线不在 Phase-1 范围。
- `sync-worker` 仍为 mock-only。
- Rework 尚未定义。
- Data Gap / Ignore Edge / Missing Station 尚未形成完整 Collector 生命周期。
- 尚未完成 24 小时以上生产化长稳认证和正式资源 SLA。
- 发布与回滚尚未完全脚本化。
- Grafana anonymous 和 datasource 权限只适用于可信 Demo LAN。
- 历史数据包含 fast、test、normal 和 unknown Profile。

## 7. 下一阶段建议

1. 以 `docs/contracts/data_gap_event.md` 为起点完成 Data Gap 契约和生命周期。
2. 增加 additive migration、Ignore Edge、counter jump、missing unit/station 的实现与回归。
3. 自动化 deploy/rollback，并生成发布 manifest 与 checksum。
4. 执行 24 小时以上 soak、故障恢复矩阵、资源和磁盘容量验收。
5. 收紧 Grafana anonymous、datasource 和远程访问权限。
6. 真实 PLC 接入前重新确认 S7 identity、counter、ACK、gap 和地址映射。
7. Oracle、企业集成、多产线和 Rework 建立独立契约、计划与验收结论。

## 8. 回归保护

后续开发不得破坏以下 Phase-1 基线：

- ACK 协议与 `plc_boot_id` / counter reset 语义。
- `/trace/api/by-cycle` 的 boot isolation。
- Recent API 的真实 station counter 与独立 `route_step`。
- Grafana Profile scope 和宽窗 `MIXED` 提示。
- 不补造不存在的 `cycle_event`。
