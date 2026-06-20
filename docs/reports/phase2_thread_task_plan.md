# Phase-2 Thread Task Plan

更新时间：2026-06-19
状态：正式分工规划

## 1. 协作原则

```text
Architecture contract
→ Reliability runtime
→ Data Quality model/query
→ Frontend product experience
→ Verification gate
```

- 一个公共文件同一时间只允许一个主责 Thread 修改。
- schema/API/协议先更新合同。
- Verification 可提前写测试，但不为通过测试改业务语义。
- 每个 Sprint 使用报告和 handoff 传递状态，不依赖聊天历史。
- PLC/HMI 控制边界由 Architecture / Integration 负责仲裁。

## 2. Architecture / Integration Thread

职责：

- 系统边界、合同和术语。
- Sprint 拆分和依赖顺序。
- line/station/PLC/Buffer/config 模型。
- 跨 Thread 文件所有权与冲突处理。
- Roadmap、版本门禁和兼容策略。
- Multi-Line 规划。

主要文件：

- `docs/contracts/line_configuration.md`
- `docs/contracts/dynamic_station_model.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/phase2_*`
- `docs/roadmap.md`

不得：

- 越过实施 Thread 直接改业务代码。
- 将 Edge 规划成 PLC 控制器。
- 在性能证据前承诺任意工站规模。

完成定义：

- 合同字段一致、无冲突。
- Sprint 输入输出和 owner 明确。
- 变更顺序、compatibility 和 rollback gate 明确。

## 3. Reliability Thread

职责：

- V-PLC 模块化。
- Profile、参数治理、seed 和 snapshot。
- 多 PLC Collector 连接、重连、ACK、queue、backpressure。
- simulator 可复现性。
- 长时间运行、资源、故障注入和性能压测支持。
- Prometheus runtime metrics。

主责模块：

- `s7_plc_sim/`
- Collector connection/runtime 部分
- `config/vplc*`
- Reliability tests/reports

必须保护：

- payload 未 ACK 不覆盖。
- `plc_boot_id` 和 counter namespace。
- normal/fast/test 语义。
- 参数变更审计。

与 Data Quality 的边界：

- Reliability 负责“可靠地得到并传递事件”。
- Data Quality 负责“事件如何结构化、关联、查询和聚合”。

## 4. Data Quality Thread

职责：

- dynamic station DB model。
- migration/rollback 设计。
- JSONB 与结构化列边界。
- event correlation、unit identity、quality facts。
- boot/profile isolation 延续。
- OEE/Quality/Trace 查询语义和 aggregation correctness。
- 保留策略、索引和查询计划。

主责模块：

- `db/`
- Collector normalizer/storage
- FastAPI query/service
- Data Quality tests/reports

必须保护：

- 不按时间猜 Genealogy。
- 不补造 cycle。
- by-cycle 不跨 boot。
- route_step 不充当 counter。
- fast/test 不污染 normal KPI。

## 5. Verification Thread

职责：

- 逐 Sprint 验收矩阵。
- contract tests、回归、migration dry-run。
- 远程部署验证和 rollback drill。
- WS01~WS10 / WS01~WS20 性能、长稳和故障恢复。
- Dashboard API/UI 数据一致性。
- 输出明确 PASS/FAIL/BLOCKED 和 capacity envelope。

主责资产：

- `tests/`
- `scripts/` 中验收工具
- `docs/reports/*validation*`
- deployment evidence

验收分层：

| 层 | 重点 |
| --- | --- |
| Config | 正例、负例、hash、兼容 |
| V-PLC | seed、Profile、ACK、20 站 |
| Collector | reconnect、queue、batch、latency |
| DB | uniqueness、migration、index、retention |
| API | pagination、window、boot/profile |
| UI | 口径、空态、下钻、3/10/20 站 |
| Remote | backup、deploy、health、rollback |

## 6. Frontend / Dashboard Thread

建议新增独立 Thread。原因：

- Next.js/ECharts/UI 状态和浏览器 QA 是独立专业域。
- 避免 Data Quality 同时承担 SQL/API 与产品界面。
- Grafana 与产品 Dashboard 需要持续边界管理。

职责：

- Next.js frontend。
- ECharts 图表。
- Overview、OEE、Quality、Trace Explorer、Station Detail。
- UI/UX、design tokens、主题和 Demo mode。
- Dashboard API 消费、缓存、错误/空/partial/stale 状态。
- 与 Grafana 的导航和职责分工。
- 浏览器截图、响应式和可访问性 QA。

主责模块：

- Phase-2 frontend workspace。
- frontend tests。
- `docs/reports/dashboard_tech_stack_plan.md` 的实施状态。

不得：

- 在前端重新计算另一套 OEE。
- 直接连接 PostgreSQL。
- 使用静态假数据冒充实时结果。
- 通过 UI 暗示 Edge 可控制 PLC。

## 7. Sprint RACI

| Sprint | A | R | C | V |
| --- | --- | --- | --- | --- |
| 1 Flexible Config | Architecture | Architecture | Reliability, Data Quality | Verification |
| 2 Generic Model | Architecture | Data Quality | Reliability | Verification |
| 3 Configurable Runtime | Architecture | Reliability + Data Quality | Frontend | Verification |
| 4 OEE MVP | Architecture | Frontend + Data Quality | Reliability | Verification |
| 5 Quality/Trace | Architecture | Data Quality + Frontend | Reliability | Verification |
| 6 Hold Model | Architecture | Data Quality + Reliability | Frontend | Verification |
| 7 Rework Optional | Architecture | Data Quality + Reliability | Frontend | Verification |
| 8 Performance | Architecture | Verification + Reliability | Data Quality, Frontend | Verification |
| 9 Multi-Line Plan | Architecture | Architecture | All Threads | All Threads review |

A = accountable，R = responsible，C = consulted，V = acceptance owner。

## 8. 共享文件冲突规则

高冲突文件：

```text
collector/app/services/event_collector.py
collector/app/services/storage.py
api/app/routes/trace.py
db/init/*
db/migrations/*
docs/contracts/*
```

规则：

1. Sprint 开始时登记 owner。
2. Reliability 和 Data Quality 不同时修改同一高冲突文件。
3. 公共字段改名先改 contract，并列消费者。
4. Frontend 不反向驱动临时 API 字段；先更新 API contract。
5. Verification 的修复建议由 owner 实施，Verification 保持独立验收。

## 9. Thread Handoff 模板

每次交接至少包含：

- Sprint、commit、config/schema/API version。
- 改动文件和未改文件。
- 已通过/失败/未运行的测试。
- migration 和 rollback 状态。
- 远程部署状态。
- 已知限制。
- 下一 Thread 的输入、禁止事项和精确命令。

## 10. 决策升级机制

以下情况返回 Architecture / Integration：

- PLC/HMI 与 Edge 职责不清。
- 新字段影响两个以上模块。
- 需要破坏性 migration。
- unit/cycle/boot/profile 语义冲突。
- 20 站性能不达标，需要缩小 envelope 或拆 PLC/Edge。
- Frontend 需要合同之外的聚合。
- Multi-Line 影响单线 namespace 或部署结构。
