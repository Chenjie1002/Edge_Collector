# Thread Reports

本目录保存三个 Codex Thread 的可审计交付报告，不保存临时草稿或聊天记录。

## Naming

```text
YYYY-MM-DD-reliability.md
YYYY-MM-DD-data-quality.md
YYYY-MM-DD-verification.md
```

同一天重复执行时追加短序号：

```text
YYYY-MM-DD-verification-02.md
```

## Required Sections

每份报告至少包含：

1. Scope
2. Commit / working tree state
3. Files changed
4. Commands executed
5. Evidence and results
6. Contract checks
7. Known issues
8. Handoff

## Status Vocabulary

- `PASS`：已执行并取得符合预期的证据。
- `FAIL`：已执行但结果不符合契约。
- `BLOCKED`：因环境或外部依赖未执行，必须写明阻塞条件。
- `NOT RUN`：不在本次范围，不能写成 PASS。

## Rules

- 不用“应该正常”代替执行证据。
- 失败项不得从报告中删除。
- 报告必须区分当前实现与目标契约。
- 只记录单机 Demo 当前阶段结果。
- Oracle / `sync-worker` 真实集成统一标记为 Phase-2 Out of Scope。
- 协议、数据库结构或公共接口变更必须先更新 `docs/contracts/`，再修改实现。
- 上述变更完成后，报告必须明确记录：
  - 受影响的 contract、代码、配置、migration 和调用方。
  - 是否存在破坏性变更或兼容性要求。
  - 已执行的验证及未执行的阻塞项。

## Current Reliability Reports

- `reliability_sprint_report.md`：Reliability Sprint 总体阶段、部署与遗留项。
- `nok_simulation_improvement_report.md`：NOK 模拟升级专项验收。
- `remote_reliability_deploy_report.md`：Raspberry Pi 部署与远程基础运行验证。

## Phase-1 Freeze Reports

- `acceptance_report.md`：Phase-1 综合验收矩阵与长期证据。
- `final_phase1_pass_report.md`：Phase-1 最终 PASS 结论。
- `reliability_context_restore.md`：Reliability Thread 上下文恢复入口。
- `data_quality_context_restore.md`：Data Quality Thread 上下文恢复入口。
- `verification_context_restore.md`：Verification Thread 上下文恢复入口。
- `github_push_phase1_report.md`：版本冻结、commit、tag 与 GitHub push 结果。

## Phase-2 Architecture Planning

- `phase2_flexible_architecture_plan.md`：柔性产线、V-PLC、Collector、API、OEE/Quality/Trace 总体规划。
- `dashboard_tech_stack_plan.md`：Next.js、FastAPI、ECharts、Grafana 和可选 Superset 分工。
- `phase2_sprint_plan.md`：九个 Sprint 的输入、输出、owner、gate、部署与 rollback 计划。
- `phase2_thread_task_plan.md`：Architecture、Reliability、Data Quality、Verification、Frontend 分工。
- `../roadmap.md`：Phase-1 freeze 后的 Phase-2 优先级、MVP 和九 Sprint 路线图。
- `next_architecture_plan.md`：历史架构底稿；若与上述文件冲突，以上述 Phase-2 正式规划为准。

对应合同：

- `../contracts/line_configuration.md`：柔性产线配置、WS01~WS20+、Buffer、mapping 与容量边界。
- `../contracts/dynamic_station_model.md`：通用工站事件、JSONB、查询隔离、索引与保留策略。
- `../contracts/dashboard_api_contract.md`：OEE、Quality、Trace 和 Dashboard API 公共合同。

## Phase-2 Sprint Reports

- `sprint1_flexible_line_configuration_report.md`：3/10/20 工站 YAML、独立 loader、
  strict validator、测试和运行链路隔离结果。
- `sprint1_contract_hardening_report.md`：Verification / Reliability HOLD 返修、配置身份、
  Profile/stress、NOK、route、sizing 与最终 Gate PASS 证据。
- `sprint1_independent_gate_review.md`：Contract Hardening 独立复验、运行链路隔离审计、
  blocker 关闭记录与最终 PASS 结论。
- `sprint1_verification_matrix.md`：返修前 Verification `HOLD / CHANGES REQUIRED` 输入。
- `sprint1_reliability_config_review.md`：返修前 Reliability `HOLD / CHANGES REQUIRED` 输入。
