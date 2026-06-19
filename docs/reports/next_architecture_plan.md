# Next Architecture Plan

更新时间：2026-06-19  
工作模式：Architecture / Integration Thread  
状态：架构规划完成，等待后续 Thread 分 Sprint 实施  
范围：非侵入式 Edge MES / Traceability / OEE Demo

## 1. Executive Summary

下一阶段应把当前“单线、单 PLC、固定 WS01/WS02/WS03”的可运行 Demo，演进为
“配置驱动的 1~N 工站、多 Buffer、可扩展多产线 Edge 数据平台”，同时保持控制边界：

> PLC/HMI 决定设备动作和制造处置；Edge 只采集、记录、关联、计算、查询和展示。

推荐架构主线：

```text
YAML line config
→ JSON Schema + semantic validation
→ resolved configuration + hash
→ V-PLC/Collector dynamic runtime
→ shared PostgreSQL event model + JSONB payload
→ Trace/Quality/OEE query layer
→ Grafana engineering view + custom management UI
```

关键决策：

- YAML 是人工维护和部署配置真源；JSON Schema 校验；JSON 用于 API/快照；CSV
  仅用于批量导入导出。
- 数据库使用 `production_line`、`plc_config`、`station_config`、
  `buffer_config`、`plc_db_mapping` 等配置注册实体。
- 生产事件继续使用共享表，避免每个工站创建独立表。
- `line_id/plc_id/station_id/station_order` 成为标准维度。
- 工站特有工艺字段进入 `payload JSONB`，稳定查询字段保留关系列。
- 当前 DB100 legacy 与 DB101/102/103 + DB104 新链路继续隔离兼容。
- Grafana 保留工程诊断；管理层、操作员和复杂 Trace 后续使用自研前端。
- Hold/Rework/Skip 只消费 PLC/HMI 定义事件；Edge 不做业务决策。

本计划只修改文档，不修改业务代码、数据库、Docker 或远程部署。

## 2. 审阅基线与当前事实

### 2.1 文档真源

- 仓库内没有根级 `PROJECT_STATUS.md`；仓库外 `../docs/PROJECT_STATUS.md` 是旧审计
  快照。
- 当前仓库状态真源是 `docs/current_status.md`。
- `docs/DOC_INDEX.md` 把 `docs/task_plan.md` 定义为既有 roadmap 真源。
- 用户本次明确要求 `docs/roadmap.md`，因此新增该文件作为“下一阶段架构路线图”，
  不删除 `task_plan.md`。

### 2.2 当前实现

- V-PLC 固定创建 WS01/WS02/WS03、DB101/102/103，并使用两个内存队列表达站间 WIP。
- `config/mapping.yaml` 已有 station template 和 station list，Collector 可按配置生成
  read plan；但只选择第一个 PLC，且数据库投影和 Trace 仍有 WS03/三站硬编码。
- `config/vplc.yaml` 只支持固定三站。
- DB104 已承担 PLC runtime identity、heartbeat 和 `ignore_edge`。
- PostgreSQL 已有共享 `cycle_event/station_event/quality_event/production_unit`，
  并已使用 JSONB payload；方向正确。
- DB100 legacy snapshot 和 DB101~104 event path 是两条不同链路。
- OEE 尚未完整实现；当前主要是产量、合格率、CT 和采集健康指标。
- Trace 当前属于单件过程追溯，尚不是完整装配/部件 Genealogy。
- Rework 当前没有协议和实现；Verification 已明确标记为 N/A。

### 2.3 必须先处理的遗留风险

- 当前验收报告仍有 Trace by-cycle 错配和 recent 字段语义问题。
- Reliability 的长时间故障恢复矩阵尚未完全闭环。
- Data Gap 合同已存在，但实现仍待后续 Thread。
- 工作树包含多个 Thread 的在途修改，后续实施必须按合同和 Sprint 边界隔离。

## 3. 功能边界

### A. Edge 必须做，且不侵入 PLC

| 能力 | Edge 职责 |
| --- | --- |
| OEE | 保存状态/产量/质量事实，按明确口径计算和展示 |
| Quality Dashboard | 展示 OK/NOK、code、趋势、缺站和数据质量 |
| Trace | 按 `unit_id`、标签、工站事件查询过程履历 |
| Genealogy | 保存明确的父子件/替换/Rework 关系并查询 |
| 模块化产线配置 | 管理 line/PLC/station/buffer/mapping/template |
| 多工站与 Buffer 模型 | 表达拓扑、WIP 观测和查询，不控制流转 |
| 多产线能力 | 数据隔离、配置隔离、查询隔离和容量验证 |
| 参数化 PLC SIM | 用配置生成 Demo 工站、DB、节拍和事件 |
| Collector 配置化 | 从 mapping 动态生成采集计划和解码模型 |
| 数据质量 | ACK、counter、gap、raw sample、采集健康 |
| 配置审计 | resolved config、版本、hash、加载结果 |

### B. Edge 可以配合做，但依赖 PLC/HMI 定义事件

| 事件 | PLC/HMI | Edge |
| --- | --- | --- |
| Hold | 决定 Hold/Release 和原因 | 记录、投影当前状态、展示历史 |
| Rework | 决定对象、路线、开始/完成/失败 | 记录轮次和路线履历 |
| Manual NOK | 操作员/HMI 确认 NOK | 保存来源、操作者和原因 |
| Skip/Bypass | PLC/HMI 决定是否跳过 | 保存 `SKIPPED` 和原因 |
| Data Gap | PLC 提供 bypass/identity/counter 事实 | 建立缺口边界和可信度 |
| Missing Unit | PLC/扫码/人工提供证据 | 展示异常和调查状态 |

Edge 不允许把“没有采到事件”直接等同于 PLC 执行了 Skip、Hold 或 Rework。

### C. Demo 中可由 V-PLC 模拟，真实项目由 PLC 控制

- 随机 NOK。
- Manual NOK 场景。
- Hold/Release 场景。
- Rework 路线与轮次。
- Buffer 进入、等待、阻塞、离开。
- 1~N 工站产品流转。
- Skip/Bypass 和上游 NOK 后的下游跳站。

所有模拟功能必须带 `simulation_only` 语义和 feature flag，不能复用为真实 PLC 控制
API。

### D. 当前阶段不优先

- Oracle/ERP/MES 真实同步。
- Data Gap 自动补数或伪造 cycle。
- Missing Unit 自动修正。
- 完整质量审批、电子签核和工作流引擎。
- 复杂 RBAC、组织、多租户。
- Edge 主动写工艺参数或控制 PLC。
- 3D 数字孪生、AI 推理、长期媒体库。

## 4. 模块化产线配置

详细合同见：

- [`../contracts/line_configuration.md`](../contracts/line_configuration.md)
- [`../contracts/dynamic_station_model.md`](../contracts/dynamic_station_model.md)

### 4.1 格式结论

推荐：

```text
YAML runtime source
+ JSON Schema validation
+ resolved JSON snapshot/API
+ CSV import/export only
```

不用纯 JSON 的原因：现场工程配置可读性和注释能力较差。  
不用纯 CSV 的原因：无法自然表达模板、嵌套 payload、Buffer 拓扑和 feature flags。  
不用 YAML+JSON 双真源的原因：容易漂移。

### 4.2 容量目标

- 每条线支持 1~N 工站。
- 下一阶段验证 WS01~WS15。
- 每个 PLC 软件上限 15 个启用工站。
- 每站默认 1 个事件 DB，最多 4 个 DB mapping。
- 每个 PLC 一个 runtime/identity DB。
- 上限必须配置校验；真实 PLC 项目再做性能 sizing。

### 4.3 模板

- `station template`：station type、默认状态、必需字段。
- `payload template`：解码字段和单位。
- `NOK template`：code、名称、分类、模拟权限。
- `buffer template`：FIFO/PALLET/CONVEYOR/VIRTUAL。
- `cycle profile`：OEE ideal CT 与 V-PLC simulation CT 分离。

## 5. 数据库动态适配

### 5.1 推荐表

| 表 | 决策 | 用途 |
| --- | --- | --- |
| `production_line` | 使用 | 产线实例、版本、hash |
| `plc_config` | 使用 | PLC 连接和 runtime mapping |
| `station_config` | 使用 | 工站类型、顺序、模板、启用状态 |
| `buffer_config` | 使用 | 站间拓扑和容量 |
| `plc_db_mapping` | 使用 | DB purpose、模板引用、轮询策略 |
| 每站独立事件表 | 禁止 | 会导致 schema 和查询随工站数膨胀 |

### 5.2 关系列与 JSONB

关系列保存：

```text
line_id, plc_id, station_id, station_order/route_step,
unit_id, boot_id, counter, timestamps, result, process_status, ack_status
```

JSONB 保存：

- 工站专有工艺测量值。
- 模板版本和低频扩展字段。
- decoded raw context。

当前 `cycle_event` 与 `station_event` 已符合大方向。后续主要补配置实体、动态终站判断、
模板版本和多线唯一性，不需要为 WS04~WS15 建表。

### 5.3 当前兼容

- WS01/DB101、WS02/DB102、WS03/DB103、runtime DB104 保持。
- 当前数据按 `LINE_001/PLC_001` 回填或映射。
- `WS03` 终站逻辑先通过配置声明替代，再考虑多终站。
- DB100 legacy 保留 compatibility adapter，不纳入新事件模型的 station list。

## 6. PLC SIM 模块化方案

### 6.1 配置输入

建议 `config/lines/LINE_001.yaml` 引用 station/buffer/payload/NOK/cycle templates。
`config/vplc.yaml` 在过渡期保留，最终成为 profile/仿真覆盖文件，而不是工站清单真源。

### 6.2 运行结构

将固定 `ThreeStationPipeline` 演进为：

```text
LineSimulator
  ├─ StationRuntime[1..N]
  ├─ BufferRuntime[0..N]
  ├─ RouteGraph
  ├─ CycleProfileResolver
  └─ SimulationEventController
```

每站 runtime 根据配置创建 DB bytearray、状态、计数器、payload writer 和 NOK generator。
每条 Buffer 只在 V-PLC 内模拟队列。

### 6.3 Feature flags

建议：

```yaml
features:
  random_nok_simulation: true
  manual_nok_simulation: true
  hold_simulation: false
  rework_simulation: false
  buffer_simulation: true
```

- `hold_simulation=false` 时不生成 Hold/Release。
- `rework_simulation=false` 时不进入 Rework 路线。
- flag 只影响 V-PLC 模拟，不影响 Collector 记录真实 PLC 已发出的标准事件。
- 所有人工模拟调用必须审计 reason、actor、request_id。

## 7. Collector 配置化采集

### 7.1 当前基础

当前 Collector 已能：

- 解析 YAML station template。
- 为每个 station 生成 read plan。
- 动态遍历 `mapping.stations`。

当前限制：

- 只选择 `mapping.plcs[0]`。
- 一个 station read plan 只能覆盖一个 DB。
- Trace/Storage 的终站和状态投影含 WS03 硬编码。
- 部分验证脚本固定 WS01/WS02/WS03。
- legacy DB100 使用另一套 source/mapping。

### 7.2 目标结构

```text
ConfigLoader
→ PlcRuntime[]
  → MappingRuntime[]
    → ReadPlan[]
      → Decoder
      → EventNormalizer
      → Shared Storage
```

每个 `PlcRuntime` 独立连接、identity、poll policy、错误状态和 station list。一个工站有
多个 mapping 时，先按 `mapping_id/purpose` 采集，再在事件归一化层合并已证明属于同一
cycle 的 payload。

### 7.3 legacy 兼容

- DB100 保留 `LegacySnapshotAdapter`。
- DB101/102/103 保留当前 `EventMappingAdapter`。
- 新配置解析器生成与当前 mapping 等价的 resolved read plan。
- legacy 和 event path 共享数据库连接可以，不能共享 identity/ACK 语义。
- 当新 Dashboard 不再依赖 DB100 后，再单独立项退役；本计划不删除。

## 8. OEE / Quality Dashboard

### 8.1 OEE 层级

推荐层级：

```text
Edge Node
→ Production Line
→ Station
→ Shift / Hour
→ Product / Order（后续）
```

指标：

- Availability：计划生产时间与设备状态事件。
- Performance：理想节拍、运行时间、总产量。
- Quality：Good Count / Total Count。
- OEE = A × P × Q。

当前数据不足以无条件计算完整 Availability。未配置班次、计划停机或可靠状态事件时，
页面必须显示“Partial OEE / 数据不足”，不能用自然时间窗冒充计划生产时间。

### 8.2 管理层展示

低学习成本页面只显示：

- 线状态。
- 当前班次 OEE/产量/达成率/合格率。
- Top loss。
- 瓶颈工站。
- 当前 Hold、NOK、Data Gap 摘要。
- 红黄绿状态和清晰的口径说明入口。

### 8.3 工程师展示

保留：

- 每站 CT 分布和趋势。
- ACK、payload_ready、counter、boot identity。
- Collector 错误、raw sample、mapping/config hash。
- Data Gap 边界。
- NOK code、payload drill-down。
- PLC/Edge 时间偏差。

### 8.4 Grafana 与自研前端

Grafana 保留：

- 主机与容器健康。
- Collector/PLC/ACK 工程监控。
- CT、NOK、Gap 的诊断 dashboard。
- 临时 SQL 验证。

自研前端负责：

- 管理层 OEE 首页。
- 操作员线览。
- 动态工站拓扑与 Buffer。
- 产品化 Trace/Genealogy。
- 报告导出和口径说明。

技术栈建议：

```text
React + TypeScript + Vite
TanStack Query
ECharts
FastAPI read-only APIs
```

首版不引入 Next.js、微前端或 3D。离线部署优先，静态资源可由 FastAPI 或独立轻量
Web 容器托管；Docker 变更属于后续实施，不在本次执行。

## 9. Trace / Genealogy

### 9.1 区别

Traceability 回答：

- 这一个 `unit_id` 经过哪些站？
- 每站什么时候加工、结果如何、测量值是什么？
- 哪个 NOK/Skip/Hold 事件影响了它？

Genealogy 回答：

- 这个总成由哪些子件、批次、载具、替换件组成？
- 某个缺陷子件影响了哪些上层产品？
- Rework 前后、替换前后是什么关系？

### 9.2 当前定位

当前系统更接近单件过程 Traceability：

- 已有 `unit_id`。
- 已有 WS01~WS03 station event。
- 已有 child/final/reject 查询入口。

它还不是完整 Genealogy，因为没有通用 `unit_relation`，也没有多子件装配、拆解、
替换、批次关系和 Rework 轮次。

### 9.3 演进为 Quality Genealogy

顺序：

1. 稳定动态 station route 和 terminal station。
2. 引入 `unit_relation`。
3. 记录 `ASSEMBLED_FROM/REPLACED_BY/REWORK_OF`。
4. 将 quality event 关联到 unit、relation、station event。
5. 支持正向影响分析和反向来源追溯。

所有关系必须来自 PLC/HMI/扫码/外部系统明确事件，不按时间接近猜测。

### 9.4 查询页面

- 顶部统一搜索：unit、DMC、label、reject、pallet。
- Summary：当前状态、最终结果、Hold、Rework、Gap。
- Route Timeline：按动态 station_order 展示。
- Genealogy Graph：父子件与替换/Rework 关系。
- Quality Panel：NOK、Manual NOK、缺陷来源、测量值。
- Evidence：raw sample、config/template version、ACK。

### 9.5 报告导出

首版建议服务端生成：

- JSON：机器交换与审计。
- CSV：事件和测量明细。
- PDF：面向客户/质量工程师的固定版式报告。

报告必须包含查询条件、生成时间、line/station、配置版本、数据缺口声明和口径版本。
不建议首版直接导出 Excel 多 Sheet，除非业务方明确要求。

## 10. Hold / Rework 边界

### 10.1 PLC/HMI 决定

- Hold/Release 时机。
- Hold reason。
- Rework 对象、路线、次数上限和完成判定。
- Manual NOK。
- Skip/Bypass。
- 工件能否继续流转。

### 10.2 Edge 记录

- 原始来源事件。
- unit、line、station、actor、reason、timestamp。
- Hold placed/released。
- Rework requested/started/completed/failed。
- 路线和关系事件。
- 配置 feature flag 和模板版本。

### 10.3 Edge 展示

- 当前 Held 工件。
- Hold 持续时间和原因。
- Rework 次数、路线、结果。
- 对 OEE/Quality 的影响。
- 事件证据和来源。

### 10.4 暂不做

- Edge 自动 Hold。
- Edge 自动 Release。
- Edge 决定 Rework 路线。
- 审批流、电子签名、MRB 完整流程。
- 自动修复 Missing Unit 或 Data Gap。

### 10.5 建模

Hold 使用追加事件 `HOLD_PLACED/HOLD_RELEASED`。  
Rework 通过 `features.rework_enabled` 开关投影；关闭时不生成 Rework 业务投影，但保留
原始证据和诊断。详细见 dynamic station contract。

## 11. 五个 Sprint

### Sprint 1：合同、配置规范与验证器

**目标**

冻结动态产线配置和动态数据模型；建立 YAML/Schema/语义校验方案；把当前三站配置
转换为兼容样例。

**输入文件**

- `config/mapping.yaml`
- `config/vplc.yaml`
- `docs/contracts/*.md`
- `docs/architecture.md`
- 本计划和两个新合同

**输出文件**

- `config/schema/line_config.schema.json`
- `config/lines/LINE_001.yaml`
- `config/templates/**`
- 配置校验器与测试
- 更新 `docs/protocol.md`、`docs/current_status.md`

**涉及模块**

- `config/`
- `scripts/`
- 文档与测试

**推荐 Thread**

- Architecture / Integration 主导
- Reliability 评审 ACK/identity/mapping 边界
- Verification 编写配置负例矩阵

**风险点**

- 当前 mapping 和 V-PLC config 双真源。
- 模板拆分后地址语义漂移。
- 过早构建 UI 配置编辑器。

**验收标准**

- 1/3/15 工站样例通过 Schema 和语义校验。
- 当前 WS01~WS03 生成等价 read plan。
- 冲突地址、重复 ID、悬空引用、容量超限明确失败。
- 不修改业务运行行为。

### Sprint 2：V-PLC 动态工站与 Buffer

**目标**

把固定三站 pipeline 改为配置驱动的 1~N 工站与 Buffer 模拟，保留当前三站行为。

**输入文件**

- Sprint 1 配置和模板
- `s7_plc_sim/app/pipeline.py`
- `s7_plc_sim/app/plc_db.py`
- `s7_plc_sim/app/runtime_config.py`
- `docs/contracts/vplc_runtime_parameters.md`

**输出文件**

- 动态 Line/Station/Buffer runtime
- 动态 DB 注册和 payload writer
- Hold/Rework/Manual NOK feature flag 框架
- 单元测试和 V-PLC 专项报告

**涉及模块**

- `s7_plc_sim/`
- `config/`
- `docs/reports/`

**推荐 Thread**

- Reliability Thread
- Architecture / Integration 做合同一致性评审

**风险点**

- ACK payload 不可覆盖约束被破坏。
- 动态模板造成 DB 越界。
- Buffer 模拟被误解为 Edge 控制逻辑。
- 当前参数审计和 profile 行为回归。

**验收标准**

- 1、3、15 工站启动测试通过。
- 当前 WS01~WS03 UID/NOK/Skip/ACK 流程回归通过。
- Hold/Rework 默认关闭。
- 未 ACK 工站仍阻止下一 payload。
- DB100 legacy 行为不变。

### Sprint 3：Collector 多 PLC/多 Mapping 与动态数据模型

**目标**

Collector 从 line config 创建多个 PlcRuntime 和 read plan；Storage/API 不再依赖固定
WS01/WS02/WS03；先合同后 migration。

**输入文件**

- Sprint 1/2 输出
- `collector/app/plc/`
- `collector/app/services/event_collector.py`
- `collector/app/services/storage.py`
- `db/init/003_event_schema.sql`
- `db/init/004_unit_trace_schema.sql`
- dynamic station contract

**输出文件**

- 多 PLC/mapping Collector runtime
- proposed migration 与回滚说明
- 配置注册表和模板版本字段
- 动态 terminal station 投影
- API compatibility adapter
- 数据模型与 Collector 测试

**涉及模块**

- `collector/`
- `db/`
- `api/`
- `scripts/`

**推荐 Thread**

- Data Quality Thread 主导数据模型和 gap 兼容
- Reliability 负责连接、ACK、identity
- Architecture / Integration 评审跨模块合同

**风险点**

- 多线下 `unit_id` 唯一性。
- 一个工站多个 DB 的 cycle 合并。
- DB migration 与现有 volume。
- WS03 硬编码遗漏。
- Reliability/Data Quality 共享文件冲突。

**验收标准**

- 同一 Collector 可加载至少两 PLC 配置样例。
- 共享事件表支持动态 station_id。
- 当前 LINE_001 数据和 Trace 保持兼容。
- 不创建每站独立表。
- ACK、counter、gap 唯一性包含正确 line/plc/station 维度。

### Sprint 4：OEE、Quality、Trace/Genealogy 查询层

**目标**

形成统一指标口径、动态路线 Trace、Quality Genealogy 最小模型和分层 Dashboard。

**输入文件**

- `docs/kpi_definitions.md`
- `docs/custom_dashboard_plan.md`
- `api/app/routes/kpi.py`
- `api/app/routes/trace.py`
- Grafana dashboards
- Sprint 3 数据模型

**输出文件**

- OEE contract 和数据充分性规则
- line/station/shift KPI API
- 动态 Trace API
- `unit_relation` 最小实现计划或 migration
- Grafana 工程 dashboard 更新
- 自研前端 API contract

**涉及模块**

- `api/`
- `db/`
- `config/grafana/`
- 文档

**推荐 Thread**

- Data Quality Thread：质量与缺口
- Verification Thread：指标复算与 Trace 完整性
- 单独 Dashboard/UI Thread：自研前端

**风险点**

- 在缺少计划时间时伪造 OEE。
- Profile/fast 数据污染生产口径。
- Genealogy 通过时间猜测关系。
- 管理层与工程层使用不同 KPI 定义。

**验收标准**

- A/P/Q 可回溯到事实事件；数据不足明确显示。
- 动态工站路线不固定三列。
- Trace by-cycle 已修复且不串历史工件。
- Quality/Genealogy 关系有来源证据。
- Grafana 与 API 对同一窗口复算一致。

### Sprint 5：Hold/Rework、报告导出与多线验收

**目标**

在不让 Edge 控制 PLC 的前提下，增加 Hold/Rework 事件记录与展示，完成报告导出和
1~3 条线容量/隔离验收。

**输入文件**

- Hold/Rework event contract
- Sprint 2 feature flags
- Sprint 3/4 API 和数据模型
- `docs/thread_handoff/verification.md`
- 部署与验收脚本

**输出文件**

- Hold/Rework 追加事件模型
- feature flag 行为
- Trace/Quality 展示
- JSON/CSV/PDF 报告
- 多线隔离、容量、恢复验收报告
- 更新 `docs/current_status.md` 和路线图

**涉及模块**

- `s7_plc_sim/`
- `collector/`
- `db/`
- `api/`
- 自研前端或 Trace 页面
- `tests/`、`scripts/`

**推荐 Thread**

- Architecture / Integration 冻结边界
- Reliability 实现模拟与采集可靠性
- Data Quality 实现事件投影
- Verification 最终验收

**风险点**

- Rework 被实现为 Edge 决策。
- Hold 状态覆盖原始事件。
- 多线资源超出树莓派能力。
- PDF 报告遗漏数据缺口或配置版本。

**验收标准**

- Edge 不能发起 Hold/Release/Rework 控制动作。
- feature flag 关闭时不生成 Rework 业务投影。
- Hold/Rework 历史为追加式且可追溯。
- LINE_001~LINE_003 查询和数据隔离通过。
- 报告包含配置版本、口径、Gap 声明和来源证据。
- Verification 输出明确 PASS/FAIL/BLOCKED，不以“能展示”替代可靠性验收。

## 12. Thread 协作与变更门禁

执行顺序：

```text
Architecture contract
→ Reliability runtime
→ Data Quality model/query
→ Verification
→ UI/productization
```

门禁：

1. 修改协议、数据库结构或公共 API 前先更新 `docs/contracts/`。
2. Reliability 与 Data Quality 同时涉及 `event_collector.py`、`storage.py`、schema、
   mapping 时，不并行修改同一文件。
3. Verification 可以提前写测试矩阵，但最终验收必须使用稳定合同和已部署版本。
4. 每个 Sprint 必须更新 `docs/current_status.md` 和对应报告。
5. Oracle/ERP、自动补数、复杂权限不进入上述五个 Sprint。

## 13. Architecture Acceptance Checklist

- [x] 明确 Edge/PLC/HMI 控制边界。
- [x] 选择 YAML + JSON Schema + JSON snapshot + CSV import/export。
- [x] 定义 1~N 工站、WS01~WS15、Buffer、station_type 和 mapping 上限。
- [x] 推荐配置注册表和共享事件表。
- [x] 明确 JSONB 使用边界。
- [x] 兼容 DB100 legacy 与 DB101~104。
- [x] 规划模块化 V-PLC 和配置化 Collector。
- [x] 区分 OEE 管理层和工程师视图。
- [x] 区分 Traceability 与 Genealogy。
- [x] 冻结 Hold/Rework 非侵入边界。
- [x] 形成五个可交接 Sprint。
- [x] 未修改业务代码、数据库 migration、Docker 或树莓派部署。
