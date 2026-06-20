# Phase-2 Architecture Freeze Report

日期：2026-06-20
Thread：Architecture / Integration
冻结类型：docs-only architecture planning baseline
状态：已冻结并推送

## 1. 本次冻结目标

将 Phase-2 正式架构规划冻结为后续 Reliability、Data Quality、Verification 和
Frontend / Dashboard Thread 的共同文档基线。

本次冻结不进入 coding，不修改业务实现、数据库 migration、Docker、远程部署脚本、
`.env`、持久化 volume 或运行环境。

## 2. 新增文档

- `docs/reports/phase2_flexible_architecture_plan.md`
- `docs/reports/dashboard_tech_stack_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/phase2_sprint_plan.md`
- `docs/reports/phase2_thread_task_plan.md`
- `docs/reports/phase2_architecture_freeze_report.md`

## 3. 修改文档

- `docs/contracts/line_configuration.md`
- `docs/contracts/dynamic_station_model.md`
- `docs/roadmap.md`
- `docs/DOC_INDEX.md`
- `docs/reports/README.md`
- `docs/reports/next_architecture_plan.md`

`next_architecture_plan.md` 已明确标记为历史架构底稿。若其 WS01~WS15、五 Sprint 或
React+Vite 等旧结论与正式 Phase-2 文件冲突，以本次冻结文件为准。

## 4. Phase-2 架构结论摘要

目标链路：

```text
YAML Line Configuration
→ Schema + semantic validation + config hash
→ Configurable V-PLC / Real PLC
→ Config-driven Collector
→ Shared PostgreSQL Event Model + JSONB
→ Bounded FastAPI OEE / Quality / Trace APIs
→ Next.js + ECharts Management Dashboard
```

Grafana 保留工程可观测性。PLC/HMI 始终是设备控制和现场流程真源；Edge 只采集、
存储、关联、计算、查询和展示。

## 5. 柔性产线架构结论

- Phase-1 WS01~WS03 保留为默认兼容配置。
- Phase-2 验证 WS01~WS10 和 WS01~WS20。
- 20 站以上可由合同表达，但必须重新进行硬件 sizing 和 Verification。
- 支持多 PLC、混合 `station_type`、基础/复杂 payload、多个 DB mapping 和 Buffer。
- 每个 PLC 默认保护上限为 20 个启用工站，每站最多 4 个 DB mapping。
- Buffer 只表达拓扑和观测，不让 Edge 控制流转。
- 配置真源为 YAML，JSON Schema 和 semantic validator 负责校验，resolved JSON/hash
  负责发布和审计。

## 6. 动态工站模型结论

- 禁止为 WS01、WS02 或未来工站创建独立业务表。
- 使用 line/PLC/station/type/schema/template 配置实体和通用事件表。
- `line_id/plc_id/station_id/station_order/plc_boot_id/profile/counter` 为结构化维度。
- 工站专有测量值使用版本化 JSONB payload。
- cycle、station、quality、hold、rework 通过不可变 event/correlation/source key
  关联。
- 延续 Phase-1 boot isolation、Profile isolation 和 counter namespace。
- 时间窗、分页、索引、聚合和数据保留策略已进入合同。
- 整线聚合读取 terminal station/route 配置，不再固定 WS03。

## 7. Dashboard 技术路线结论

- Backend：FastAPI + PostgreSQL。
- Frontend：Next.js + React + TypeScript。
- Charts：ECharts。
- Grafana：主机、Collector、PLC、DB、API latency、Prometheus 工程监控。
- 自研 Dashboard：管理层 Overview/OEE、Quality、Trace Explorer、Station Detail。
- Apache Superset 为后续 optional，不进入 Phase-2 MVP。
- 3D digital twin、在线配置编辑器和高级报告模板暂缓。
- API 必须有界、分页、Profile/boot 隔离，并返回数据充分性和口径版本。

## 8. Sprint 规划结论

Phase-2 拆分为九个 Sprint：

1. Flexible Line Configuration
2. Generic Station Event Model
3. Configurable V-PLC and Collector
4. OEE API and Dashboard MVP
5. Quality Dashboard and Trace Explorer
6. Hold Event Model
7. Rework Optional
8. Performance and Long-run Validation
9. Multi-Line Planning

每个 Sprint 均已定义目标、输入、输出、涉及模块、负责 Thread、验收标准、风险、
不做什么、远程部署要求和 rollback 演练要求。

## 9. Thread 分工结论

- Architecture / Integration：合同、边界、Sprint、Roadmap、跨 Thread 冲突。
- Reliability：V-PLC、Profile/参数治理、Collector runtime、长稳和性能。
- Data Quality：DB model、JSONB 边界、API 语义、聚合和数据可信度。
- Verification：验收矩阵、回归、远程部署验证、rollback 和 10/20 站容量。
- Frontend / Dashboard：Next.js、ECharts、OEE、Quality、Trace 和 UI/UX。

建议新增独立 Frontend / Dashboard Thread，避免 Data Quality 同时承担查询语义与产品
界面实现。

## 10. 架构红线检查结果

| 红线 | 结果 |
| --- | --- |
| Edge 被描述为控制系统 | 未发现 |
| Edge 主动决定 Hold/Rework/Skip | 未发现 |
| Multi-Line 被设为第一优先级 | 未发现；仅 Sprint 9 规划 |
| 每工站独立建表 | 明确禁止 |
| Data Gap/Missing Unit 成为核心 | 未发生；均非 MVP 核心 |
| Grafana 成为管理层主 Dashboard | 未发生；保留工程视角 |
| 自研 Dashboard/Grafana 分工缺失 | 已明确 |
| 忽略 WS01~WS20 | 未发生 |
| 忽略 Raspberry Pi 性能边界 | 未发生 |
| 忽略 boot/profile/counter 经验 | 未发生 |

## 11. Docs-only 检查结果

- Git 工作树变更全部位于 `docs/`。
- 未修改业务代码。
- 未修改数据库 migration。
- 未修改 Docker/Compose。
- 未修改远程部署脚本。
- 未修改 `.env` 或 `.env.example`。
- 未修改 volume、日志、缓存或远程环境。
- 八个核心交付物存在且非空。
- DOC_INDEX 和 reports index 已更新。
- 本地 Markdown 链接检查无失效。
- 未完成标记扫描无命中。
- 九个 Sprint 的要求字段完整。
- 常见私钥和 token pattern 扫描无命中。
- `git diff --check` 通过。

## 12. 未跟踪文件处理说明

以下既有文件保持未跟踪、未修改、未暂存：

```text
docs/Edge MES Demo 当前进度报告.md
```

该文件是 Phase-1 冻结期间发现的旧进度报告，包含过时状态并与
`docs/current_status.md`、最终 PASS 报告的职责重叠。本次不删除、不修订、不提交。

## 13. 当前未进入 Coding

本次只冻结文档。以下均未实施：

- line config schema/validator。
- 新 migration。
- 动态 V-PLC / Collector。
- Dashboard API。
- Next.js frontend。
- Hold/Rework 模型。
- 远程部署和服务重启。

规划文档中的 checkbox 表示后续 Sprint 工作，不代表已交付功能。

## 14. 下一步推荐 Sprint

只启动 Sprint 1：Flexible Line Configuration。

推荐顺序：

1. Architecture / Integration 继续维护合同和配置术语。
2. Reliability 评审 PLC DB、ACK、Profile 和 sizing 边界。
3. Verification 编写 3/10/20 站配置正负例矩阵。
4. 通过配置 gate 后，再启动 Sprint 2 数据模型实施。

## 15. 推荐 Codex Thread

- 继续使用 Architecture / Integration Thread 作为 Sprint 1 owner。
- 继续使用 Reliability Thread 做 PLC/ACK/性能评审。
- 继续使用 Data Quality Thread 为 Sprint 2 提前准备 migration tests，不提前实施。
- 继续使用 Verification Thread 编写验收矩阵。
- Sprint 4 前新建 Frontend / Dashboard Thread。

## 16. 风险项

- Phase-1 mapping 和新 line config 过渡期可能形成双真源。
- 20 站是验证目标，不是无条件硬件承诺。
- 多 DB payload 合并必须有确定性 cycle/correlation key。
- 完整 OEE 依赖 production calendar 和 equipment state。
- Raspberry Pi 的 CPU、内存、温度、SSD 增长和查询性能尚未实测。
- Next.js 新服务会增加后续部署、权限和 rollback 复杂度。
- Hold/Rework 如果来源事件定义不清，容易越过非侵入边界。

## 17. 用户需要确认的问题

在启动 Sprint 1 前建议确认：

1. 是否接受 WS01~WS20 为 Phase-2 验证目标，而不是产品硬上限。
2. 是否接受 Next.js + ECharts 作为自研 Dashboard MVP 技术栈。
3. 是否同意新增 Frontend / Dashboard Thread。
4. 是否确认 Phase-2 MVP 不把 Data Gap、Missing Unit、Superset 和 3D 纳入核心。
5. 是否在未来 Sprint 1 完成后再评估创建 Phase-2 planning tag；本次不创建 tag。

## 18. Git 冻结结果

Phase-2 Architecture Planning 主提交：

```text
commit: ec0f4f3
message: Phase 2 architecture planning docs
branch: main
remote: origin
push: PASS
```

本次未创建 release tag。该结果段在主提交推送成功后补充，因此通过独立的报告收尾提交
进入 `main`，不改变主架构提交的内容或创建额外 tag。
