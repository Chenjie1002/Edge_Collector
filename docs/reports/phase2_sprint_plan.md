# Phase-2 Sprint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox syntax for tracking.

**Goal:** 将 Phase-1 三工站 Demo 演进为配置驱动的单线柔性 Edge MES，并交付 OEE、
Quality、Trace Dashboard 与可审计性能边界。

**Architecture:** 先冻结 line/data/API contracts，再按配置、事件模型、V-PLC/Collector、
Dashboard、业务预留和性能验收顺序实施。PLC/HMI 始终控制现场流程，Edge 只采集、存储、
计算、查询和展示。

**Tech Stack:** YAML、JSON Schema、Python/FastAPI、PostgreSQL/JSONB、Snap7 V-PLC、
Next.js/React/TypeScript、ECharts、Grafana/Prometheus。

---

## 1. 全局门禁

- [ ] 任何协议、schema、公共 API 变化先更新 `docs/contracts/`。
- [ ] 每个 Sprint 先写失败测试或验收样例，再实现。
- [ ] Phase-1 的 ACK、boot isolation、Profile isolation、counter/route_step 语义必须回归。
- [ ] 远程部署前必须有精确文件清单、备份、checksum、post-deploy gate。
- [ ] migration、容器、数据卷变化必须有 rollback 演练方案。
- [ ] 每个 Sprint 更新报告、handoff、`docs/current_status.md` 和 Roadmap 状态。

## Sprint 1: Flexible Line Configuration

### 目标

从固定 WS01~WS03 配置升级为可描述 WS01~WS20+、多 PLC、Buffer、模板和负载上限的
配置化单线模型。

### 输入

- `docs/contracts/line_configuration.md`
- `config/mapping.yaml`
- `config/vplc.yaml`
- `docs/protocol.md`

### 输出

- `config/schema/line_config.schema.json`
- `config/lines/LINE_001.yaml`
- `config/lines/examples/LINE_001_10_STATIONS.yaml`
- `config/lines/examples/LINE_001_20_STATIONS.yaml`
- `config/templates/**`
- `scripts/validate_line_config.py`
- 配置负例测试与 Sprint 报告

### 涉及模块

`config/`、`scripts/`、`tests/`、`docs/contracts/`

### 负责 Thread

Architecture / Integration 主责；Reliability 评审 DB/ACK；Verification 负责负例矩阵。

### 执行清单

- [ ] 将 Phase-1 mapping 转为 resolved-equivalent LINE_001 配置。
- [ ] 为 line/PLC/station/buffer/mapping/template 建 JSON Schema。
- [ ] 实现重复 ID、悬空引用、DB 越界/重叠、容量和负载语义校验。
- [ ] 增加 3/10/20 工站正例和至少 20 个负例。
- [ ] 生成稳定 canonical JSON、config hash 和 diff。
- [ ] 验证旧 mapping 与新 resolved read plan 等价。

### 验收标准

- 3/10/20 工站配置通过；20+ 需显式 sizing override。
- WS01~WS03 地址、ACK、payload 语义等价。
- 错误配置拒绝全量加载，不部分启动。
- resolved output 在相同输入下稳定。

### 风险

双真源、模板地址漂移、Demo 地址被误当通用标准。

### 不做

不改 V-PLC/Collector 运行逻辑，不建配置 UI。

### 远程部署 / Rollback

不需要远程部署；不需要 rollback drill。

## Sprint 2: Generic Station Event Model

### 目标

让数据库和公共查询不再假设固定三站，冻结通用事件、配置镜像、索引与保留策略。

### 输入

- `docs/contracts/dynamic_station_model.md`
- `docs/contracts/dashboard_api_contract.md`
- Phase-1 schema 与 Trace tests
- Sprint 1 resolved config

### 输出

- additive migration 设计与 rollback SQL
- 通用配置表和事件字段
- compatibility view/adapter 设计
- Data Quality 单元/集成测试
- migration dry-run 报告

### 涉及模块

`db/`、`collector/app/services/storage.py`、`api/`、`tests/`

### 负责 Thread

Data Quality 主责；Architecture 审核合同；Verification 审核迁移和数据一致性。

### 执行清单

- [ ] 为 3/10/20 工站准备 migration fixture。
- [ ] 先写 boot/profile/identity 唯一性失败测试。
- [ ] 实施 production_line/plc/station/type/schema/NOK template 发布镜像。
- [ ] 扩展共享 cycle/station/quality 表，不创建每站表。
- [ ] 增加事件 correlation key、template version、config hash。
- [ ] 建立索引、statement timeout 和保留策略验证。
- [ ] 验证 Phase-1 数据和 endpoint compatibility。

### 验收标准

- 同一 counter 不同 boot 不冲突。
- 3/10/20 station_id 查询无需 schema 变化。
- Profile 默认隔离。
- migration 前后 Phase-1 样本可复算。
- rollback 在副本数据库通过。

### 风险

现有数据约束、unit_id 全局唯一性、索引写放大。

### 不做

不实现 Hold/Rework 业务；不做破坏性重命名。

### 远程部署 / Rollback

需要受控远程部署；必须真实 rollback drill。

## Sprint 3: Configurable V-PLC and Collector

### 目标

V-PLC 与 Collector 基于同一 resolved line configuration 支持 3/10/20 工站。

### 输入

- Sprint 1 配置
- Sprint 2 event model
- ACK、identity、runtime parameter contracts

### 输出

- Configurable LineSimulator / PlcRuntime / StationRuntime / BufferRuntime
- Collector multi-PLC/multi-mapping runtime
- 有界队列、batch writer、backpressure
- Prometheus metrics
- 可靠性与集成报告

### 涉及模块

`s7_plc_sim/`、`collector/`、`config/`、`tests/`

### 负责 Thread

Reliability 主责；Data Quality 负责 normalizer/storage；Architecture 处理共享合同。

### 执行清单

- [ ] 写 3/10/20 工站 V-PLC 启动与 payload tests。
- [ ] 将固定 pipeline 拆成配置驱动 runtime。
- [ ] 保留 strict ACK、boot、counter、Profile、audit。
- [ ] 增加固定 seed、station NOK rate、global fallback。
- [ ] Collector 为每 PLC 建独立连接和 poll task。
- [ ] 实现 payload schema validation 和通用 event normalization。
- [ ] 实现有界 queue、batch write、backpressure 和 metrics。
- [ ] 注入 disconnect/reconnect、DB delay、ACK failure。

### 验收标准

- Phase-1 3 站全量回归。
- 10/20 站无事件丢失、重复 identity。
- 未 ACK payload 不覆盖。
- queue 能在 burst 后回落。
- fast/test 数据不会进入 normal KPI。

### 风险

线程/协程竞争、Snap7 连接限制、DB burst、共享文件冲突。

### 不做

不实现 Edge 控制 Hold/Rework；不删除 DB100 compatibility。

### 远程部署 / Rollback

需要；V-PLC/Collector 定向重建。必须 rollback drill。

## Sprint 4: OEE API and Dashboard MVP

### 目标

建立管理层可理解的 OEE Dashboard，并明确数据不足状态。

### 输入

- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/dashboard_tech_stack_plan.md`
- `docs/kpi_definitions.md`
- Sprint 2/3 数据

### 输出

- OEE summary/trend APIs
- Next.js Overview/OEE 页面
- A/P/Q、station OEE、throughput、CT 图表
- metric fixtures 和口径复算报告

### 涉及模块

`api/`、新 frontend workspace、`tests/`、Dashboard docs

### 负责 Thread

Frontend / Dashboard 主责 UI；Data Quality 主责指标；Verification 复算。

### 执行清单

- [ ] 为完整/缺 schedule/缺 state/MIXED Profile 写 API contract tests。
- [ ] 实现 OEE query service 和有界聚合。
- [ ] Scaffold Next.js 离线前端和 design tokens。
- [ ] 实现 Overview、OEE filters 和 ECharts。
- [ ] 增加 loading/empty/partial/stale/error。
- [ ] 对 3/10/20 工站做布局和 API 性能测试。

### 验收标准

- A/P/Q 可追溯到事实和口径版本。
- 数据不足不显示伪 OEE。
- summary p95 < 1 秒。
- 管理层第一屏一眼可读。
- Grafana 仍独立承担工程监控。

### 风险

错误 Availability、前端刷新风暴、管理/工程口径漂移。

### 不做

不做 Superset、3D、在线配置编辑和复杂权限。

### 远程部署 / Rollback

需要新增/更新 API 与前端服务；需要应用级 rollback，若 Compose 变化则做完整演练。

## Sprint 5: Quality Dashboard and Trace Explorer

### 目标

交付 NOK、FPY、Pareto、质量排名和动态工站 Trace/Genealogy 查询体验。

### 输入

- Sprint 2 event model
- Dashboard API contract
- Phase-1 Trace baseline

### 输出

- Quality APIs
- Trace search/detail/by-station/by-NOK
- Quality Dashboard、Trace Explorer、Station Detail
- raw payload drilldown
- 报告导出接口预留

### 涉及模块

`api/`、frontend、`tests/`

### 负责 Thread

Data Quality + Frontend / Dashboard；Verification 验证语义和性能。

### 执行清单

- [ ] 写 boot/profile isolation 与动态路线 contract tests。
- [ ] 实现 quality summary/trend/Pareto/station ranking。
- [ ] 实现 cursor Trace search 和 unit timeline。
- [ ] 加入 payload schema/version 和 raw evidence 下钻。
- [ ] 展示 PASS/NOK/SKIPPED、defect origin、skipped chain。
- [ ] 验证相同数据在 API、前端和 Grafana 中可复算。

### 验收标准

- Trace 不固定三列。
- by-cycle 不跨 boot。
- Pareto 含分母与 Others。
- raw payload 有权限、大小和掩码限制。
- 3/10/20 工站时间线可读。

### 风险

大查询、payload 泄露、Genealogy 猜测。

### 不做

不实现推测 Genealogy，不做高级 PDF/Excel 模板。

### 远程部署 / Rollback

需要；API/frontend 可独立 rollback，数据库若不变可不做 migration rollback。

## Sprint 6: Hold Event Model

### 目标

采集和展示 PLC/HMI 定义的 Hold/Remove/Scrap/Release 事件。

### 输入

- Hold contract section
- PLC/HMI event mapping
- Sprint 2/5 event/Trace

### 输出

- additive hold event model
- Collector normalizer
- Trace/Quality/OEE projection
- Hold timeline UI

### 涉及模块

contracts、DB、Collector、API、frontend、tests

### 负责 Thread

Architecture 定义边界；Data Quality 建模；Reliability 采集；Frontend 展示。

### 执行清单

- [ ] 用 fixture 定义 placed/released/removed/scrapped 顺序和异常序列。
- [ ] 实施追加式事件，不覆盖原 cycle。
- [ ] 计算持续时间和未关闭 Hold。
- [ ] 在 OEE 中仅按已批准口径计入 loss。
- [ ] 验证 Edge 无控制 endpoint。

### 验收标准

- 事件来源和 reason 可审计。
- 异常顺序明确告警。
- Edge 不能发起 Hold/Release。

### 风险

把业务状态投影误当控制、事件乱序。

### 不做

不做审批流、电子签名、MRB。

### 远程部署 / Rollback

需要；有 migration，必须 rollback drill。

## Sprint 7: Rework Optional

### 目标

通过 feature flag 可选启用 Rework，默认关闭。

### 输入

- Rework contract
- route graph / unit relation
- Sprint 6 event pattern

### 输出

- rework event/relation model
- V-PLC simulation-only scenario
- Collector/API/Trace projection
- UI read-only展示

### 涉及模块

contracts、V-PLC、Collector、DB、API、frontend、tests

### 负责 Thread

Architecture + Data Quality 主责；Reliability 模拟；Verification 场景验收。

### 执行清单

- [ ] 写 flag off/on、round、route、failed/completed tests。
- [ ] 默认关闭，不生成 Rework 业务投影。
- [ ] 开启时只消费明确 PLC/HMI event。
- [ ] 使用追加事件和 `REWORK_OF`，不改写历史。
- [ ] UI 展示轮次、路线、结果和来源。

### 验收标准

- flag off 无 Rework 投影。
- flag on 关系可追溯。
- Edge 不决定路线。

### 风险

状态爆炸、历史被覆盖、误实现控制 API。

### 不做

不做自动路线优化和人工审批系统。

### 远程部署 / Rollback

需要；默认关闭部署，migration 必须 rollback drill。

## Sprint 8: Performance and Long-run Validation

### 目标

证明 WS01~WS10 / WS01~WS20 在 Raspberry Pi 上的真实可用 envelope。

### 输入

- 3/10/20 配置
- V-PLC pressure profiles
- Prometheus metrics
- API/UI

### 输出

- 性能测试脚本
- 1h/8h/24h 报告
- capacity envelope
- bottleneck/RCA
- deployment/rollback runbook 更新

### 涉及模块

Verification scripts、Prometheus/Grafana、reports

### 负责 Thread

Verification 主责；Reliability 处理运行稳定性；Data Quality 校验数据。

### 执行清单

- [ ] 运行工站/PLC/payload/mapping/DB delay 测试矩阵。
- [ ] 记录 CPU、内存、温度、磁盘、queue、poll、DB、API p95。
- [ ] 校验事件数、唯一键、ACK、boot/profile/config hash。
- [ ] 运行故障恢复和 restart matrix。
- [ ] 输出明确通过 envelope 和超限行为。

### 验收标准

- 24 小时无事实丢失、重复、跨 boot/profile 污染。
- queue 不持续增长。
- API/UI 在定义 SLA 内。
- 超限时系统 fail closed 或明确降级。

### 风险

磁盘增长、温度降频、测试数据污染 normal KPI。

### 不做

不把 20 站结果外推为任意规模。

### 远程部署 / Rollback

需要专用验收部署；每轮前有恢复点，完成 rollback/recovery drill。

## Sprint 9: Multi-Line Planning

### 目标

在模块化单线稳定后，规划 LINE_A / LINE_B / LINE_C，不在本 Sprint 实施多线。

### 输入

- Sprint 8 envelope
- 单线 contracts
- 现场 PLC/网络拓扑需求

### 输出

- Multi-Line architecture decision
- isolation/capacity/security/deployment plan
- line-level config namespace
- 下一阶段 Sprint backlog

### 涉及模块

Architecture docs、contracts、deployment planning

### 负责 Thread

Architecture / Integration 主责；四个实施 Thread 评审。

### 执行清单

- [ ] 评估单 Edge 多线与每线独立 Edge。
- [ ] 规划 line namespace、资源 quota、故障隔离。
- [ ] 规划 API/Auth/backup/upgrade。
- [ ] 用 Sprint 8 数据计算 1/2/3 线容量。
- [ ] 输出 go/no-go 和下一阶段合同。

### 验收标准

- 不共享模糊 station/unit namespace。
- 单线故障不静默污染其他线。
- 容量结论有实测依据。
- 未实施的多线能力不标记为已交付。

### 风险

共享资源争抢、跨线 UID 冲突、部署复杂度。

### 不做

不改业务代码、不部署 LINE_B/C、不接 Oracle。

### 远程部署 / Rollback

不需要；纯规划 Sprint。

## 2. 推荐提交节奏

每个 Sprint 至少拆为：

```text
contract/test fixtures
→ implementation slice
→ regression/performance
→ docs/report/handoff
```

不要把 schema、Collector、API、Frontend 和部署压成一个不可回滚提交。
