# Reliability Thread Handoff

更新时间：2026-06-19  
Thread：Thread01-Reliability  
Phase-1 最终状态：`PASS`

> 2026-06-19 已完成 Phase-1 最终验收。本文件是后续 Thread 恢复 Reliability
> 上下文的首要入口。若早期 RCA、计划或 Sprint 报告仍包含 `PENDING`、`BLOCKED`
> 或“尚未实施”表述，以本文件和最新验收结论为准。

## 1. Phase-1 已完成内容

### Reliability 基础

- DB104 PLC runtime identity 已投入使用：
  - `protocol_version = DB104.DBW0`
  - `heartbeat_counter = DB104.DBD4`
  - `plc_restart_counter = DB104.DBD8`
  - `plc_boot_id = DB104.DBB12 STRING[36]`
  - `ignore_edge = DB104.DBX52.3`
- V-PLC 默认启用严格 ACK：
  - `payload_ready=TRUE` 后冻结当前 payload。
  - ACK 超时只设置 `ack_timeout=TRUE`，不清除或覆盖 payload。
  - 收到 `read_done=TRUE` 后才清除握手位并允许下一件。
- Collector 使用以下幂等键持久化事件：

  ```text
  plc_id + station_id + plc_boot_id + cycle_counter
  ```

- Collector 完成 raw sample、cycle、station/unit/quality 数据提交后才写 ACK。
- ACK 写回失败、Collector 重启补 ACK、counter reset 阻断和错误状态落库已实现。

### Profile 与 Cycle Time

- 已实现 `normal / fast / test` Profile。
- `config/vplc.yaml` 是 V-PLC station 参数真源。
- `normal` Profile 固定 `scale=1.0`，锁定 runtime base/jitter 修改。
- `fast/test` 只通过 scale 加速，保留约 30 秒 process baseline。
- 旧版本约 4–5 秒异常节拍已修复。
- 当前 Raspberry Pi `normal` Profile 三站实测约 29–32 秒。

### 参数治理

- 参数修改要求非空 `reason`。
- accepted/rejected 修改均记录 actor、client IP、request ID、old/new、profile 和拒绝原因。
- startup、runtime update、reset 和周期性参数快照已实现。
- 已提供只读审计接口：
  - `GET /vplc/audit/changes`
  - `GET /vplc/audit/snapshots`
- migration 005、006 已在 Raspberry Pi PostgreSQL 成功执行。

### NOK 模拟

- WS01、WS02、WS03 拥有独立 NOK Rate、独立 RNG 和独立强制 NOK FIFO 队列。
- 强制 NOK 支持 `count=1..100`、工站 code 白名单、pending 查询和队列清除。
- 上游 NOK 产生的下游 `SKIPPED` 不消费下游强制 NOK 队列。
- NOK 结果已贯通 PLC Payload、Collector、数据库、Trace 和现有 Grafana 查询。
- Raspberry Pi 已验证 WS01、WS02、WS03 均可产生 NOK。

### 测试、部署与文档

- V-PLC 全量测试：27/27 PASS。
- Collector 单元/集成测试：12/12 PASS。
- 真实本地 Snap7 Server/Client ACK：PASS。
- mapping、compileall、Compose 静态解析和 `git diff --check`：PASS。
- Raspberry Pi 9 个 Compose 服务运行，PostgreSQL 为 `healthy`。
- 实际远程部署路径为 `/opt/edge-mes-demo`，该目录不是 Git 仓库。
- 部署使用定向发布包和 Compose 重建，不使用 `git pull`。
- 部署未覆盖 `.env`、PostgreSQL/Grafana/Prometheus 持久化数据。

## 2. 本 Thread 负责的关键变更

### 契约

- `docs/contracts/plc_identity_and_counter.md`
- `docs/contracts/ack_protocol.md`
- `docs/contracts/vplc_runtime_parameters.md`

### V-PLC

- `s7_plc_sim/app/plc_db.py`
- `s7_plc_sim/app/pipeline.py`
- `s7_plc_sim/app/runtime_config.py`
- `s7_plc_sim/app/parameter_audit.py`
- `s7_plc_sim/app/control_api.py`
- `s7_plc_sim/app/main.py`

### Collector 与数据库

- `collector/app/services/reliability.py`
- `collector/app/services/event_collector.py`
- `collector/app/services/storage.py`
- `config/mapping.yaml`
- `db/init/003_event_schema.sql`
- `db/init/005_vplc_parameter_audit.sql`
- `db/migrations/005_reliability_schema.sql`
- `db/migrations/006_vplc_parameter_audit.sql`

### 配置与测试

- `config/vplc.yaml`
- `config/app.yaml`
- `docker-compose.yml`
- `s7_plc_sim/tests/test_reliability.py`
- `s7_plc_sim/tests/test_runtime_config.py`
- `s7_plc_sim/tests/test_parameter_audit.py`
- `s7_plc_sim/tests/test_nok_simulation.py`
- `s7_plc_sim/tests/test_pipeline_uid_flow.py`
- `collector/tests/`

## 3. 当前稳定状态

```text
Phase-1 acceptance = PASS
remote path = /opt/edge-mes-demo
profile = normal
cycle_scale = 1.0
require_ack = true
ack_deadline_s = 10.0
WS01 base_cycle_s = 30.4
WS02 base_cycle_s = 29.8
WS03 base_cycle_s = 29.2
PostgreSQL = healthy
Collector = continuously storing cycle_event
```

- 当前三站 cycle 约 29–32 秒。
- normal Profile 拒绝危险的 runtime cycle edit，并记录拒绝审计。
- `fast/test` Profile 已验证可用，验收结束后已恢复 `normal`。
- WS01、WS02、WS03 NOK 注入均已验证，pending 队列已清空。
- Grafana 和 API 健康检查通过。

## 4. 已知限制

- 远程 `/opt/edge-mes-demo` 不是 Git 仓库；版本追踪依赖发布包 checksum、部署报告和备份。
- 数据库保留部署前约 4 秒历史事件及验收期间的 `fast/test` 快速事件；宽时间范围查询
  可能混合不同 Profile 数据，应按时间或 `plc_boot_id` 隔离。
- Grafana 尚无参数审计与 pending NOK 队列专用面板；当前通过 V-PLC API、控制页和
  PostgreSQL 查询。
- Snap7 集成测试关闭连接时可能输出
  `Expected COTP DT, got 0x80`，当前不影响断言、退出码或运行结果。
- 真实 PLC、多产线、认证体系、Oracle 真实同步、媒体归档和 AI 不属于 Phase-1。
- `data_gap_event`、Ignore Edge 闭环及数据质量展示属于 Data Quality Thread。
- SSH 密码、私钥、Token 和其他凭据不得写入仓库。

## 5. 下一阶段建议

1. 由 Data Quality Thread 基于 DB104 `ignore_edge`、稳定 `plc_boot_id` 和 counter
   语义实现 `data_gap_event`。
2. 由 Verification Thread 将 Phase-1 验收矩阵沉淀为可重复执行的端到端回归脚本。
3. Dashboard 查询增加 Profile/boot/time 范围隔离，避免历史快速节拍影响当前指标。
4. 如运维需要，再增加参数审计和 pending NOK 队列 Grafana 面板。
5. 为非 Git 远程部署建立发布编号、checksum、备份和回滚登记。
6. Phase-2 若启动真实 PLC、Oracle 或多产线工作，必须先新增契约，不得直接改变
   Phase-1 已冻结语义。

## 6. 新 Thread 如何恢复上下文

### 必读顺序

1. [`../reports/reliability_context_restore.md`](../reports/reliability_context_restore.md)
2. [`../reports/reliability_sprint_report.md`](../reports/reliability_sprint_report.md)
3. [`../reports/remote_reliability_deploy_report.md`](../reports/remote_reliability_deploy_report.md)
4. [`../reports/nok_simulation_improvement_report.md`](../reports/nok_simulation_improvement_report.md)
5. [`../contracts/plc_identity_and_counter.md`](../contracts/plc_identity_and_counter.md)
6. [`../contracts/ack_protocol.md`](../contracts/ack_protocol.md)
7. [`../contracts/vplc_runtime_parameters.md`](../contracts/vplc_runtime_parameters.md)
8. [`../protocol.md`](../protocol.md)
9. [`../current_status.md`](../current_status.md)

### 恢复后先检查

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
git status --short
```

如需核对远程运行状态，使用 `/opt/edge-mes-demo`，不要假设远程目录是 Git 仓库：

```bash
cd /opt/edge-mes-demo
docker compose ps
docker compose logs --tail=80 s7-plc-sim
docker compose logs --tail=80 collector
```

同时核对：

- `/vplc/state` 为 `profile=normal`、`scale=1.0`。
- 三站 base 参数为 `30.4 / 29.8 / 29.2`。
- PostgreSQL 持续产生 `cycle_event`。
- 后续修改继续遵守：

  ```text
  docs/contracts/ → code/config/migration → tests → docs/reports/
  ```

不要重新分析已经关闭的 4 秒 Cycle Time 根因，也不要重做 Reliability 架构。新 Thread
应直接消费 Phase-1 稳定接口，并只处理其明确的新范围。

## 7. 证据入口

- [`../reports/cycle_time_rca.md`](../reports/cycle_time_rca.md)
- [`../reports/cycle_time_fix_plan.md`](../reports/cycle_time_fix_plan.md)
- [`../reports/reliability_report.md`](../reports/reliability_report.md)
- [`../reports/reliability_sprint_report.md`](../reports/reliability_sprint_report.md)
- [`../reports/nok_simulation_improvement_report.md`](../reports/nok_simulation_improvement_report.md)
- [`../reports/remote_reliability_deploy_report.md`](../reports/remote_reliability_deploy_report.md)
- [`../deployment/raspberry_pi.md`](../deployment/raspberry_pi.md)
