# Edge MES Demo 文档索引

更新时间：2026-06-20

## 1. 当前协作范围

本阶段只整理和推进单机、单产线、单 PLC、三工站的离线可运行 Demo。

本阶段目标：

- 补强 ACK、PLC identity、counter reset 和 Collector 恢复可靠性。
- 实现 Ignore Edge / Bypass 数据缺口记录。
- 建立可重复执行的验证与报告机制。
- 为三个 Codex Thread 提供共享契约和交接入口。

Phase-2 Out of Scope：

- Oracle schema、真实 Oracle 连接和凭据。
- outbox 到 Oracle 的真实 push、重试、幂等和运维。
- `sync-worker` 业务扩展；当前只保留 mock。
- 多产线、真实 PLC 上线、参数管理、媒体、归档、权限和 AI。

这里的 “Phase-2” 指本次三 Thread 协作之后的产品阶段，不等同于
[`task_plan.md`](task_plan.md) 中已经完成的 “Phase 2 - V-PLC 三工站模拟”。

## 2. 核心文档

| 文档 | 类型 | 用途 | 当前定位 |
| --- | --- | --- | --- |
| [`architecture.md`](architecture.md) | Architecture | 服务拓扑、数据流、数据库分层和架构约束 | 现有架构真源，不重复创建 architecture 文档 |
| [`current_status.md`](current_status.md) | Project Status | 当前完成能力、限制、未完成事项和常用命令 | 仓库内项目状态真源；不另建 `PROJECT_STATUS.md` |
| [`task_plan.md`](task_plan.md) | Roadmap | 阶段、优先级、执行顺序和验收建议 | 现有 roadmap 真源 |
| [`edge_mes_demo_srs.md`](edge_mes_demo_srs.md) | SRS | 当前 Demo 的范围、功能和非功能需求 | 需求基线 |
| [`decisions.md`](decisions.md) | ADR | 已确认的关键设计决策及原因 | 决策历史，不在 handoff 中重复解释 |
| [`protocol.md`](protocol.md) | Implemented Protocol | 当前 DB100/101/102/103 地址、字段和握手实现 | 描述当前实现，不代表生产级通用协议 |
| [`plc_edge_integration_guide.md`](plc_edge_integration_guide.md) | Engineering Guide | 面向真实 PLC 的通用接入规范 | Phase-2/现场接入参考，本阶段不完整实现 |
| [`roadmap.md`](roadmap.md) | Phase-2 Roadmap | Phase-1 freeze 后的九 Sprint 优先级与 gate | Phase-2 路线图真源 |

说明：仓库外存在 `../docs/PROJECT_STATUS.md` 审计快照，但它不属于
`edge-mes-demo` Git 仓库，也不是协作真源。项目状态以
[`current_status.md`](current_status.md) 为准。

## 3. 专题文档

| 文档 | 用途 | 当前阶段 |
| --- | --- | --- |
| [`plc_address_map.md`](plc_address_map.md) | 旧 DB100 Demo 地址说明 | 保留兼容 |
| [`scenario_control.md`](scenario_control.md) | Simulator 场景控制页面和 API | 当前可用 |
| [`kpi_definitions.md`](kpi_definitions.md) | KPI、ACK 和数据缺口指标口径 | 数据质量 Thread 输入 |
| [`custom_dashboard_plan.md`](custom_dashboard_plan.md) | 自研 dashboard 与数字孪生规划 | 后续产品化 |
| [`edge_expansion_plan.md`](edge_expansion_plan.md) | 多产线、参数、媒体、归档、权限、AI 扩展 | Phase-2 及以后 |

## 4. 协作契约

契约文件定义三个 Thread 必须共同遵守的边界。修改契约时，应先更新契约，
再由受影响 Thread 修改代码。

| 文档 | 主要使用者 | 内容 |
| --- | --- | --- |
| [`contracts/ack_protocol.md`](contracts/ack_protocol.md) | Reliability、Verification | 当前 ACK 行为、目标状态机、幂等和失败处理 |
| [`contracts/plc_identity_and_counter.md`](contracts/plc_identity_and_counter.md) | Reliability、Data Quality、Verification | PLC 启动身份、counter、重启和回绕规则 |
| [`contracts/data_gap_event.md`](contracts/data_gap_event.md) | Data Quality、Verification | Ignore Edge / Bypass 缺口边界和计数规则 |
| [`contracts/vplc_runtime_parameters.md`](contracts/vplc_runtime_parameters.md) | Reliability、Verification | Profile、Cycle Time guardrail、参数审计/快照和 NOK 模拟 |
| [`contracts/line_configuration.md`](contracts/line_configuration.md) | Architecture、Reliability | 柔性单线、PLC、工站、Buffer、mapping 与容量合同 |
| [`contracts/station_event_model.md`](contracts/station_event_model.md) | Architecture、Reliability、Data Quality、Verification | Sprint 2 PM 决策已冻结的通用工站事件 envelope、语义、校验与序列化合同 |
| [`contracts/dynamic_station_model.md`](contracts/dynamic_station_model.md) | Architecture、Data Quality | 动态工站、共享事件、JSONB、索引与保留策略 |
| [`contracts/dashboard_api_contract.md`](contracts/dashboard_api_contract.md) | Data Quality、Frontend、Verification | OEE、Quality、Trace 与 Dashboard 公共 API 合同 |

## 5. Thread 交接入口

| 启动顺序 | Thread | 交接文件 | 主要职责 |
| --- | --- | --- | --- |
| 1 | Reliability | [`thread_handoff/reliability.md`](thread_handoff/reliability.md) | 固化 PLC identity/counter，完成严格 ACK 和恢复语义 |
| 2 | Data Quality | [`thread_handoff/data_quality.md`](thread_handoff/data_quality.md) | 基于稳定 counter 实现 data gap，并增强查询和可观测性 |
| 3 | Verification | [`thread_handoff/verification.md`](thread_handoff/verification.md) | 执行集成、故障恢复和回归验收，形成最终报告 |

Verification Thread 可以在前两个 Thread 开发期间准备测试环境和基线，但最终
验收应在 Reliability 和 Data Quality 交付后执行。

## 6. 报告

[`reports/README.md`](reports/README.md) 定义验证报告命名、内容和提交规则。
Thread 不应把临时聊天结论当作交付；关键验证结果必须写入 `docs/reports/`。

Phase-1 统一上下文恢复入口：

| Thread | Handoff | Context Restore |
| --- | --- | --- |
| Reliability | [`thread_handoff/reliability.md`](thread_handoff/reliability.md) | [`reports/reliability_context_restore.md`](reports/reliability_context_restore.md) |
| Data Quality | [`thread_handoff/data_quality.md`](thread_handoff/data_quality.md) | [`reports/data_quality_context_restore.md`](reports/data_quality_context_restore.md) |
| Verification | [`thread_handoff/verification.md`](thread_handoff/verification.md) | [`reports/verification_context_restore.md`](reports/verification_context_restore.md) |

Phase-1 冻结发布说明：

- [`releases/phase1_pass_release_note.md`](releases/phase1_pass_release_note.md)

Phase-2 正式规划：

- [`reports/phase2_flexible_architecture_plan.md`](reports/phase2_flexible_architecture_plan.md)
- [`reports/dashboard_tech_stack_plan.md`](reports/dashboard_tech_stack_plan.md)
- [`reports/phase2_sprint_plan.md`](reports/phase2_sprint_plan.md)
- [`reports/phase2_thread_task_plan.md`](reports/phase2_thread_task_plan.md)
- [`roadmap.md`](roadmap.md)

Phase-2 Sprint 1：

- [`reports/sprint1_flexible_line_configuration_report.md`](reports/sprint1_flexible_line_configuration_report.md)
- [`reports/sprint1_contract_hardening_report.md`](reports/sprint1_contract_hardening_report.md)
- [`reports/sprint1_independent_gate_review.md`](reports/sprint1_independent_gate_review.md)
- [`reports/sprint1_verification_matrix.md`](reports/sprint1_verification_matrix.md)
- [`reports/sprint1_reliability_config_review.md`](reports/sprint1_reliability_config_review.md)
- `config/lines/demo_3_station.yaml`
- `config/lines/demo_10_station.yaml`
- `config/lines/stress_20_station.yaml`
- `common/line_config/`

Phase-2 Sprint 2 planning freeze：

- [`contracts/station_event_model.md`](contracts/station_event_model.md)
- [`reports/sprint2_generic_station_event_model_plan.md`](reports/sprint2_generic_station_event_model_plan.md)
- [`reports/sprint2_station_event_reliability_review.md`](reports/sprint2_station_event_reliability_review.md)

Reliability N8 定向复验结论为 `PASS WITH RECOMMENDATIONS`；N6、N7、N8、UNKNOWN、
payload limits、event required fields 均 CLOSED 且无回归，新 Reliability blocker 为无。
下一步可进入 Data Quality review 与 Verification Gate matrix；两项 review 与 ChatGPT PM
授权完成前，Sprint 2 implementation 仍禁止。

## 7. 代码与配置入口

| 路径 | 作用 |
| --- | --- |
| `config/mapping.yaml` | 新三工站协议 mapping |
| `config/lines/` | Phase-2 柔性产线 YAML 示例；当前不参与运行 |
| `common/line_config/` | strict loader/validator、resolved config、hash 与静态 load estimate |
| `config/plc_mapping.yaml` | 旧 DB100 快照 mapping |
| `config/vplc.yaml` | V-PLC station baseline 与 Profile 配置 |
| `s7_plc_sim/` | Snap7 V-PLC、三工站 pipeline 和控制页 |
| `collector/` | DB100 快照采集与 DB101/102/103 事件采集 |
| `api/` | KPI、事件、同步状态和追溯 API |
| `db/init/` | PostgreSQL schema 和 seed |
| `scripts/` | mapping 校验、S7 sample 读取和 Demo SQL 工具 |
| `docker-compose.yml` | 单机 Demo 服务编排 |

## 8. 文档维护规则

- 不重复创建 architecture、roadmap、project status 或 SRS。
- 当前行为变化时，优先更新 `protocol.md` 和 `current_status.md`。
- 设计决策变化时，更新 `decisions.md`。
- Thread 共享语义变化时，先更新 `contracts/`。
- 任何协议、数据库结构或公共接口修改，必须遵守以下顺序：
  1. 先更新 `docs/contracts/` 中受影响的契约。
  2. 再修改代码、配置或数据库 migration。
  3. 最后在 `docs/reports/` 对应报告中记录影响范围、兼容性和验证结果。
- Thread 交付状态更新到对应 `thread_handoff/` 和 `reports/`。
- Oracle / `sync-worker` 在本阶段始终标记为 Phase-2 Out of Scope。
