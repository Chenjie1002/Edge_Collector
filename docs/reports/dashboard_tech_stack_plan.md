# Phase-2 Custom Dashboard Technology Plan

更新时间：2026-06-19
状态：正式技术路线，尚未实施
关联合同：[`../contracts/dashboard_api_contract.md`](../contracts/dashboard_api_contract.md)

## 1. 总体定位

自研 Dashboard 是 Phase-2 面向管理层、客户 Demo 和质量分析人员的主产品界面。
Grafana 继续承担工程可观测性，两者不互相替代。

| 用户 | 核心问题 | 主界面 |
| --- | --- | --- |
| 管理层 | 产线是否达标，损失在哪里 | Overview / OEE |
| 质量工程师 | 哪些工站和 NOK code 在恶化 | Quality / Trace |
| Demo 观众 | 系统能否一眼理解并下钻 | Overview / Genealogy |
| 工程师 | Collector、DB、API、PLC 是否健康 | Grafana |

设计原则：

- 低学习成本、少术语、先结论后证据。
- 第一屏可在 10 秒内读懂线状态、OEE、质量和异常。
- 管理层看摘要，质量工程师可逐层下钻到 payload。
- 支持 Demo mode，明确标注 profile、数据时间和是否为模拟数据。
- 暗色/浅色主题预留，品牌字体、配色和动效由 design token 管理。
- 不用炫技图表掩盖数据缺口或口径不完整。

## 2. 技术栈决策

### 2.1 Backend

- FastAPI。
- PostgreSQL。
- Pydantic response model。
- 后续可加入 Redis 作为短期缓存，但不作为 MVP 前置。
- 大报告导出使用异步 job；MVP 不引入复杂消息平台。

### 2.2 Frontend

- Next.js + React + TypeScript。
- App Router。
- TanStack Query 管理服务端数据。
- ECharts 提供业务图表。
- CSS variables/design tokens 管理主题。
- 静态或 standalone Node 部署方式在实施 Sprint 决定。

选择 Next.js 的原因：

- 路由、布局、错误边界和部署结构明确。
- 可同时支持静态壳与受控服务端能力。
- 便于后续报告页面、权限和品牌化。

MVP 不依赖公网、云服务或外部 CDN。

### 2.3 可选 Superset

Apache Superset 仅作为后续管理层自助分析选项，不进入 Phase-2 第一优先级。

优点：

- SQL Lab、切片、探索式分析成熟。
- 适合分析人员快速组合维度。

成本：

- 增加服务、元数据库、权限、升级和备份复杂度。
- 与产品化 Dashboard 重复部分能力。
- 在 Raspberry Pi 上增加资源占用。
- 仍需建立语义层，不能直接把原始表暴露给所有用户。

决策：Phase-2 MVP 不部署 Superset。完成数据模型、API 和预聚合后，再以独立 PoC
评估是否放到外部服务器。

## 3. Backend API 分层

| API Domain | 职责 |
| --- | --- |
| Line Configuration API | 已发布线/PLC/工站/Buffer 拓扑，只读预览 |
| Trace API | by-cycle/by-unit/by-DMC/by-station/by-NOK |
| Quality API | NOK、FPY、Pareto、工站质量 |
| OEE API | line/station A/P/Q/OEE 与数据充分性 |
| Dashboard Summary API | 首页 cards、状态、Top loss |
| Station Event API | 工站事件列表和趋势 |
| Raw Payload Drilldown API | 受限读取 decoded payload/raw evidence |

API 统一要求：

- `line_id` 必填或使用明确默认线。
- 有界时间窗。
- Profile 默认 normal。
- cursor pagination。
- 明确 `data_completeness`、`metric_version`、`config_version`。
- raw payload 权限与普通摘要分离。
- boot isolation 和 Profile isolation 不因前端简化而丢失。

## 4. 页面规划

### 4.1 Overview Page

- 当前线、时间窗、Profile、最后更新时间。
- Line status。
- OEE / A / P / Q cards。
- 实际产量、理论产量、差异。
- Top loss、瓶颈工站、当前异常。
- 动态工站与 Buffer 概览。
- 最近 NOK / Hold / data freshness 警示。

### 4.2 OEE Dashboard

- OEE trend。
- A/P/Q cards 与分解。
- station-level OEE bar。
- throughput trend。
- cycle time distribution。
- NOK loss。
- downtime / hold loss 预留。
- 点击指标进入来源事件和口径说明。

若数据不足，显示 Partial OEE，不把自然时间窗当计划生产时间。

### 4.3 Quality Dashboard

- NOK trend。
- NOK code Pareto。
- station quality ranking。
- FPY/pass rate。
- NOK category/severity。
- defect origin 与 skipped chain。
- payload evidence 下钻。

### 4.4 Trace Explorer

- 搜索 cycle、DMC、UID、NOK code。
- time window / line / station / station type filters。
- unit route timeline。
- 每站 PASS/NOK/SKIPPED。
- raw payload、quality event、ACK、boot 和 config hash。
- Genealogy graph 预留。

### 4.5 Station Detail Page

- 当前连接和采集 freshness。
- station type、order、PLC、Profile。
- throughput、CT distribution、NOK rate。
- 最近事件。
- payload schema 和 config version。
- “Open in Grafana” 工程入口。

### 4.6 Unit Genealogy Page

- unit summary。
- parent/child/replaced/rework relation。
- route timeline。
- quality evidence。
- 关系来源，不显示推测关系。

MVP 可先实现只读空态和 Trace link，Genealogy 图在关系模型稳定后启用。

### 4.7 Config Preview Page

- resolved line topology。
- PLC/station/Buffer/mapping 摘要。
- config version/hash。
- enabled/disabled station。
- payload/NOK template 版本。
- 只读，不提供在线修改真实 PLC 地址。

### 4.8 Engineering Link Page

- Grafana dashboard 链接。
- API health。
- Collector/DB/Prometheus 摘要。
- 当前 config hash。
- 明确提示工程面板和业务面板口径差异。

## 5. ECharts 图表规范

| 图表 | 推荐图形 | 交互 |
| --- | --- | --- |
| OEE trend | line | 时间缩放、Profile filter |
| A/P/Q cards | KPI cards + sparkline | 点击口径 |
| Station OEE | horizontal bar | 排序、下钻 |
| NOK trend | stacked line/bar | station/category filter |
| NOK Pareto | bar + cumulative line | Top N / Others |
| Station quality ranking | horizontal bar | FPY/NOK toggle |
| CT distribution | boxplot/histogram | station/profile filter |
| Throughput trend | line/step | bucket selector |
| Hold/downtime | timeline/stacked bar | Phase-2 reserved |

图表必须显示单位、时间窗、Profile、数据更新时间和 no-data/error 状态。禁止截断纵轴制造
夸张差异，除非显式标注。

## 6. Grafana 保留范围

Grafana 继续负责：

- Prometheus metrics。
- API latency/error。
- Collector health、queue、last collection。
- PostgreSQL health、connection、storage。
- V-PLC Profile、boot、ACK。
- 主机 CPU、内存、温度、磁盘。

Grafana 不承担：

- 管理层主首页。
- 最终 Quality Trace 产品界面。
- Genealogy。
- 复杂报告导出。
- 配置编辑。

## 7. UI / UX 原则

- 首屏最多 6 个主 KPI。
- 业务语言优先：产量、合格率、损失；工程字段放详情。
- 颜色不是唯一状态编码，同时使用图标和文字。
- 红色只用于需要行动的异常。
- 所有指标可查看公式、分母和数据充分性。
- 页面保留 loading、empty、partial、stale、error 五种状态。
- Demo mode 可锁定默认线、时间窗和演示导航，但不能使用假数据冒充实时数据。
- 桌面优先，平板可用，移动端保证查询和告警可读。
- 动效只用于状态变化和下钻，不做持续高负载装饰。

## 8. 刷新与缓存

| 数据 | 刷新 |
| --- | --- |
| Line/station status | 2~5 秒 |
| Dashboard summary | 10 秒 |
| OEE/Quality trend | 30~60 秒或手动 |
| Trace | 用户查询 |
| Config preview | config hash 变化后 |

API 返回 `generated_at` 和 `data_freshness_seconds`。前端发现 stale 时显示告警，不继续
把旧数据画成实时状态。

## 9. Dashboard MVP

第一批页面：

1. Overview。
2. OEE Dashboard。
3. Quality Dashboard。
4. Trace Explorer。
5. Station Detail。
6. Engineering Links。

第一批图表：

- OEE trend + A/P/Q。
- station OEE。
- throughput。
- NOK trend/Pareto。
- station quality ranking。
- CT distribution。

第一批 API：

- line configuration summary。
- dashboard summary。
- OEE summary/trend。
- quality summary/Pareto。
- station events。
- trace search/detail。
- raw payload drilldown。

暂缓：

- Superset。
- 3D digital twin。
- 在线配置编辑器。
- Genealogy 图的复杂编辑。
- PDF/Excel 高级模板。
- Hold/Rework 操作界面。

## 10. 验收标准

- 页面不假设 WS01~WS03 固定列。
- 相同 API 数据在 Overview/OEE/Quality 中口径一致。
- Profile、时间窗和 station filter 在 URL 中可复现。
- Partial OEE 和 stale data 明确可见。
- Trace 能从 unit 下钻到 station、quality 和 raw payload。
- 管理层页面不暴露任意 SQL。
- Grafana 工程入口仍可访问且职责清晰。
- 3/10/20 工站配置下布局不溢出、不丢站。
- 桌面与平板完成浏览器截图和交互 QA。
