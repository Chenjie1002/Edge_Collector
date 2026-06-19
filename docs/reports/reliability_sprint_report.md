# Reliability Sprint Report

日期：2026-06-19  
范围：V-PLC Profile、Cycle Time 参数治理、参数审计/快照、NOK 模拟升级、测试与文档。

> NOK 模拟的工站规则、Payload、Trace、Dashboard 和 Verification 细节统一记录在
> [`nok_simulation_improvement_report.md`](nok_simulation_improvement_report.md)。
> 本报告只保留 P3 阶段摘要，避免两份报告重复维护。

## 当前进度

Reliability Sprint 的 P1–P4 代码实施、本机自动化验证和 Raspberry Pi 定向部署均已
完成。远程当前运行 `normal` Profile，三站 cycle 已从旧版本约 4–5 秒恢复到约
29–32 秒。剩余工作集中在故障恢复矩阵和长时间稳定性验收。

## 已完成

- P1：Profile 体系与 Cycle Time 修复完成。
- P2：参数审计与参数快照完成。
- P3：NOK FIFO 队列、白名单与批量模拟完成。
- P4：本机测试、文档、远程 migration、定向镜像重建和运行验证完成。
- 远程 9 个 Compose 服务运行正常，PostgreSQL 为 `healthy`。
- WS01、WS02、WS03 均已产生 NOK；`fast/test` Profile 验证后已恢复 `normal`。
- Collector 持续落库，PostgreSQL 持续产生 `cycle_event`。
- normal 模式非法 cycle 参数修改已验证被拒绝并进入审计记录。
- 部署未覆盖远程 `.env`、数据库 volume、Grafana volume 和 Prometheus 数据。

## 未完成

- ACK timeout、Collector 重启、数据库断开、ACK 写失败和 counter reset 的远程故障
  注入矩阵。
- 24 小时或更长时间的稳定性运行观察。
- Grafana 参数审计专用面板。
- Dashboard 宽时间范围对历史 4 秒数据及本次 `fast/test` 测试数据的隔离展示。

## 下一步

1. 执行远程 Reliability 故障恢复矩阵并记录逐项证据。
2. 完成长时间 normal Profile 稳定性观察。
3. 明确 Dashboard 查询窗口或按 `plc_boot_id` 过滤，避免混入历史快速 cycle。
4. 继续使用发布包 checksum、远程备份和部署报告管理非 Git 部署目录。

## P1：Profile 体系与 Cycle Time 修复

状态：`PASS`

### 完成内容

- 新增 `normal / fast / test` Profile。
- 新增受控参数真源 `config/vplc.yaml`。
- station 设计基线从 `pipeline.py` 硬编码迁移到 resolved runtime configuration。
- `normal` 强制 `cycle_scale=1.0`、base 20–60 秒、jitter 0–10 秒。
- `normal` runtime API 禁止修改 base/jitter。
- `fast/test` 保留快速仿真和 runtime cycle edit。
- `/vplc/state` 返回 profile、配置来源和配置 hash。
- V-PLC 启动日志输出完整 resolved configuration。
- 控制页显示 profile，并在 normal 模式禁用 base/jitter 输入。
- `ideal_cycle_time_ms` 从旧的 1200 修正为 30000。

### 修改文件

- `docs/contracts/vplc_runtime_parameters.md`
- `config/vplc.yaml`
- `config/app.yaml`
- `docker-compose.yml`
- `s7_plc_sim/app/runtime_config.py`
- `s7_plc_sim/app/pipeline.py`
- `s7_plc_sim/app/main.py`
- `s7_plc_sim/app/control_api.py`
- `s7_plc_sim/tests/test_runtime_config.py`

### 测试结果

- P1 红灯：`ModuleNotFoundError: app.runtime_config`。
- P1 定向测试：6/6 PASS。
- V-PLC 全量测试：14/14 PASS。
- Python compileall：PASS。
- `git diff --check`：PASS。

### 下一步任务

- P2：参数变更审计。
- P2：startup/runtime/periodic 参数快照。
- P2：审计数据库 migration 和只读查询接口。

## P2：参数审计与参数快照

状态：`PASS`

### 完成内容

- 参数修改要求非空 `reason`。
- API 捕获 actor、client IP 和 request ID。
- accepted/rejected 修改均记录 old/new、profile 和拒绝原因。
- rejected normal cycle edit 不改变运行参数。
- startup、runtime update、reset、5 分钟 periodic snapshot 已接入。
- 审计数据库不可用时保留进程内最近记录，不中断 V-PLC。
- 新增变更与快照只读查询接口：
  - `GET /vplc/audit/changes`
  - `GET /vplc/audit/snapshots`
- 查询优先返回 PostgreSQL 持久历史；数据库不可用时回退到进程内最近记录。
- 新增 PostgreSQL init schema 与可重复执行 migration。
- V-PLC Compose 增加 PostgreSQL 依赖与 `DATABASE_URL`。

### 修改文件

- `s7_plc_sim/app/parameter_audit.py`
- `s7_plc_sim/app/pipeline.py`
- `s7_plc_sim/app/control_api.py`
- `s7_plc_sim/app/main.py`
- `s7_plc_sim/requirements.txt`
- `s7_plc_sim/tests/test_parameter_audit.py`
- `db/init/005_vplc_parameter_audit.sql`
- `db/migrations/006_vplc_parameter_audit.sql`
- `docker-compose.yml`

### 测试结果

- P2 红灯：`ModuleNotFoundError: app.parameter_audit`。
- P2 定向测试：5/5 PASS。
- V-PLC 全量测试：19/19 PASS。
- Python compileall：PASS。
- `git diff --check`：PASS。

### 下一步任务

- P3：强制 NOK 从单次值升级为确定性队列。
- P3：station NOK code 白名单校验。
- P3：支持 count、查询待执行数量和清除队列。

## P3：NOK 模拟升级

状态：`PASS`

### 完成内容

- 每站确定性 FIFO 强制 NOK 队列、`count=1..100` 和工站 code 白名单已实现。
- pending 查询、清除、参数审计、独立 NOK Rate/RNG 和 SKIPPED 不消费规则已实现。
- Payload、Trace 与 Dashboard 影响及完整验证建议见
  [`nok_simulation_improvement_report.md`](nok_simulation_improvement_report.md)。

### 修改文件

- `s7_plc_sim/app/pipeline.py`
- `s7_plc_sim/app/control_api.py`
- `s7_plc_sim/tests/test_nok_simulation.py`
- `docs/contracts/vplc_runtime_parameters.md`

### 测试结果

- P3 红灯：5 项测试因旧 `force_nok()` 不支持 count/queue 而失败。
- P3 定向测试：5/5 PASS。
- 本次收尾重新执行 V-PLC 全量测试：27/27 PASS。
- Python compileall：PASS。
- `git diff --check`：PASS。

### 下一步任务

- P4：更新 protocol、status、README 和部署说明。
- P4：执行 V-PLC、Collector、mapping、compileall 与静态校验全量验收。
- P4：核对 migration 和 Compose 配置，并在 Raspberry Pi 完成部署验证。

## P4：测试、文档与远程部署

状态：本机实施与验证 `PASS`；Raspberry Pi 定向部署与基础运行验证 `PASS`；
远程故障恢复矩阵 `PENDING`

### 完成内容

- 更新 README、`.env.example`、文档索引、当前状态、协议和 Reliability handoff。
- 补充 Profile、参数 API、审计表、快照和 NOK 队列的当前实现说明。
- runtime update、reset 与 periodic snapshot 自动继承当前 PLC boot ID。
- 修复 normal 控制页保存 NOK rate 时仍提交锁定 base/jitter 的问题。
- WS03 控制页不再提供仅用于下游 skip 语义的 `30003` 强制 NOK code。
- 核对实际 `config/vplc.yaml`：
  - normal：scale 1.0。
  - fast：scale 0.1。
  - 三站 process baseline 保持约 30 秒。
- 核对 Compose profile 环境和 `006_vplc_parameter_audit.sql` 必要表定义。
- 备份远程关键部署文件并同步本地 Reliability Sprint 更新。
- 在远程成功执行 migration 005 和 006。
- 仅重建 `s7-plc-sim` 和 `collector`，未覆盖 `.env` 或持久化 volume。
- 验证 normal Profile 三站 cycle、Collector 落库、NOK、参数审计以及 fast/test
  Profile。

### 修改文件

- `README.md`
- `.env.example`
- `docs/DOC_INDEX.md`
- `docs/current_status.md`
- `docs/protocol.md`
- `docs/thread_handoff/reliability.md`
- `docs/reports/reliability_sprint_report.md`
- `s7_plc_sim/app/pipeline.py`
- `s7_plc_sim/app/control_api.py`
- `s7_plc_sim/app/main.py`
- `s7_plc_sim/tests/test_parameter_audit.py`
- `s7_plc_sim/tests/test_runtime_config.py`

### 测试结果

| 检查 | 结果 |
| --- | --- |
| V-PLC 全量测试 | PASS，27/27 |
| Collector 单元/集成测试 | PASS，12/12 |
| 真实本地 Snap7 Server/Client ACK | PASS |
| mapping 校验 | PASS |
| actual `vplc.yaml` normal/fast 解析 | PASS |
| Docker Compose YAML 静态解析 | PASS |
| audit migration 静态检查 | PASS |
| Python compileall | PASS |
| `git diff --check` | PASS |
| Raspberry Pi PostgreSQL migration 005/006 | PASS，均为 `COMMIT` |
| Raspberry Pi 定向镜像重建 | PASS，仅 `s7-plc-sim`、`collector` |
| Raspberry Pi Compose 服务状态 | PASS，9 个服务运行，PostgreSQL healthy |
| normal Profile cycle | PASS，三站约 29–32 秒 |
| WS01/WS02/WS03 NOK | PASS |
| normal 非法 base cycle 修改审计 | PASS，HTTP 400、`accepted=false` |
| fast/test Profile 可用性 | PASS，验证后已恢复 normal |
| Collector 与 `cycle_event` 持续性 | PASS |
| 远程故障恢复矩阵 | PENDING |
| 长时间稳定性观察 | PENDING |

Collector 集成测试首次在受限沙箱内因禁止绑定本地临时端口失败；在获准的本地执行环境
重跑后 12/12 PASS。Snap7 连接清理仍输出一条
`Expected COTP DT, got 0x80`，不影响测试断言和退出码。

### 下一步任务

本 Sprint 的实现、部署和基础运行验证已完成。下一阶段：

1. 执行 ACK timeout payload 保持验证。
2. 执行 Collector 重启补 ACK 验证。
3. 执行 PostgreSQL 中断与恢复验证。
4. 执行 ACK 写失败和重试状态验证。
5. 注入同 boot counter reset，验证阻断落库与 ACK。
6. 完成长时间 normal Profile 稳定性观察。

## Sprint Final Status

- P1 Profile 体系与 Cycle Time 修复：`PASS`
- P2 参数审计与参数快照：`PASS`
- P3 NOK 模拟升级：`PASS`
- P4 本机测试与文档：`PASS`
- Raspberry Pi migration 与定向 Compose 部署：`PASS`
- Raspberry Pi 基础运行验收：`PASS`
- Raspberry Pi 故障恢复矩阵：`PENDING`

远程部署完整证据见
[`remote_reliability_deploy_report.md`](remote_reliability_deploy_report.md)。

## Reliability Sprint 最终交付物

### 契约与配置

- `docs/contracts/plc_identity_and_counter.md`
- `docs/contracts/ack_protocol.md`
- `docs/contracts/vplc_runtime_parameters.md`
- `config/vplc.yaml`
- `config/mapping.yaml`
- `config/app.yaml`
- `docker-compose.yml`

### V-PLC 与 Collector 实现

- `s7_plc_sim/app/runtime_config.py`
- `s7_plc_sim/app/parameter_audit.py`
- `s7_plc_sim/app/pipeline.py`
- `s7_plc_sim/app/control_api.py`
- `s7_plc_sim/app/main.py`
- `s7_plc_sim/app/plc_db.py`
- `collector/app/services/reliability.py`
- `collector/app/services/event_collector.py`
- `collector/app/services/storage.py`

### Schema 与 Migration

- `db/init/003_event_schema.sql`
- `db/init/005_vplc_parameter_audit.sql`
- `db/migrations/005_reliability_schema.sql`
- `db/migrations/006_vplc_parameter_audit.sql`

### 自动化测试

- `s7_plc_sim/tests/test_reliability.py`
- `s7_plc_sim/tests/test_runtime_config.py`
- `s7_plc_sim/tests/test_parameter_audit.py`
- `s7_plc_sim/tests/test_nok_simulation.py`
- `s7_plc_sim/tests/test_pipeline_uid_flow.py`
- `collector/tests/test_reliability.py`
- `collector/tests/test_event_collector_reliability.py`
- `collector/tests/test_snap7_reliability_integration.py`

### 文档与报告

- `docs/current_status.md`
- `docs/protocol.md`
- `docs/DOC_INDEX.md`
- `docs/deployment/raspberry_pi.md`
- `docs/thread_handoff/reliability.md`
- `docs/reports/reliability_context_restore.md`
- `docs/reports/cycle_time_rca.md`
- `docs/reports/cycle_time_fix_plan.md`
- `docs/reports/reliability_report.md`
- `docs/reports/reliability_sprint_report.md`
- `docs/reports/nok_simulation_improvement_report.md`
- `docs/reports/remote_reliability_deploy_report.md`
