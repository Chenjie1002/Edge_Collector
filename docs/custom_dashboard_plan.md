# 自研 Dashboard 与数字孪生首页规划

更新时间：2026-06-16  
阶段定位：后续产品化模块，不替代当前 Grafana 工程监控  
建议技术栈：React + Vite + FastAPI API + PostgreSQL

## 1. 定位

当前 Grafana 适合工程监控、采集调试、SQL 看板和主机资源观察，但不适合承担最终操作员界面、管理层首页和数字孪生体验。

自研 dashboard 的定位是：

- 面向操作员和生产管理者。
- 第一屏展示整线状态、产量、合格率、cycle time、异常和 WIP。
- 后续接入 3D 设备、物料流动和工站状态动画。
- 保留 Grafana 作为工程诊断入口。

## 2. 边界

| 模块 | 继续用 Grafana | 自研 Dashboard |
| --- | --- | --- |
| Collector 状态 | 是 | 摘要显示 |
| ACK / raw sample 调试 | 是 | 只显示异常提醒 |
| 主机 CPU/内存/磁盘 | 是 | 可在系统状态页摘要 |
| 操作员首页 | 否 | 是 |
| 数字孪生 3D | 否 | 是 |
| 工站状态动画 | 否 | 是 |
| 追溯查询 | 可链接 | 是 |
| KPI 说明文档 | 否 | 独立说明页 |

## 3. 首版页面

### 3.1 首页 / Line Overview

目标：打开后立即知道产线是否在运行、当前产出是否达标、哪个工站异常。

首屏模块：

- 整线运行状态。
- 当前班次实际产量、理论产量、差异。
- WS03 合格率。
- 平均 cycle time。
- 当前 WIP。
- 三工站状态条。
- 实时产出曲线：实际累计 vs 理论累计。
- 最近异常 / NOK / 停机提示。

### 3.2 工站详情 / Station Detail

每个工站显示：

- 当前状态：IDLE/RUNNING/WAITING/BLOCKED/ALARM。
- 当前 DMC。
- 最近 cycle。
- CT 趋势。
- NOK code。
- 工站参数：基准节拍、波动、NOK 率。
- 最近 20 条工站事件。

### 3.3 追溯 / Traceability

保留当前追溯能力，但产品化：

- 搜索 ASM/SUB/序号。
- 三工站时间线。
- 已完成合格 / 进行中 / 不合格三栏。
- 缺站原因提示。
- raw sample drill-down 链接。

### 3.4 数据质量 / Data Quality

面向工程师：

- Collector 在线状态。
- ACK 未确认。
- 数据缺口。
- counter reset。
- raw sample 最新时间。
- PLC 连接状态。

## 4. 后续数字孪生首页

数字孪生首页建议分两阶段做。

### Phase DT-1 轻量 2.5D

使用 SVG/Canvas/CSS 实现：

- 三工站布局。
- 物料小块从 WS01 流向 WS03。
- 工站状态颜色。
- WIP 数量。
- NOK 件用红色路径或标记显示。

优点：

- 对树莓派资源友好。
- 更快可实现。
- 更容易与真实数据绑定。

### Phase DT-2 3D 设备展示

使用 Three.js 实现：

- 设备 3D 模型。
- 物料流动动画。
- 工站状态灯。
- 点击工站进入详情。

注意：

- 3D 模型、贴图和动画需要控制资源占用。
- 首版不建议把 3D 做成所有数据交互的唯一入口。
- 3D 应服务于理解产线，而不是遮挡 KPI。

## 5. API 需求

建议新增或稳定以下 API：

| API | 用途 |
| --- | --- |
| `GET /api/line/summary` | 整线首页摘要 |
| `GET /api/line/output-trend` | 实际/理论产出曲线 |
| `GET /api/stations/status` | 三工站实时状态 |
| `GET /api/stations/{station_id}/events` | 工站最近事件 |
| `GET /api/trace?q=` | 追溯查询，复用当前能力 |
| `GET /api/data-quality/summary` | 采集健康摘要 |
| `GET /api/kpi/shift` | 当前班次 KPI |

## 6. 前端技术建议

建议使用：

- React + Vite
- CSS variables 作为轻量 design tokens
- ECharts 或 uPlot 做趋势图
- Three.js 后续接 3D
- lucide-react 做图标
- fetch/SWR 或 TanStack Query 做数据刷新

刷新策略：

- 首页 KPI：5-10 秒刷新。
- 工站状态：1-2 秒刷新。
- 追溯结果：手动刷新。
- 主机资源：10 秒刷新即可，仍可留在 Grafana。

## 7. 首版验收

首版自研 dashboard 完成时应满足：

- 首页不依赖 Grafana。
- 页面能在树莓派本机部署。
- 不影响现有 API、Collector、V-PLC、Grafana。
- 实际产量、理论产量、差异值显示符合已定义 KPI 口径。
- 实时产出曲线只缩放时间轴，不混淆纵轴口径。
- 三工站状态可读，移动端不溢出。
- 所有关键数据来自 API，不使用硬编码静态假数据。

## 8. 开发前置条件

开始编码前需要完成：

1. 确认首版是否只做 2D dashboard，不做 3D。
2. 确认是否直接嵌入现有 FastAPI，还是新建前端服务。
3. 固化 KPI API 响应格式。
4. 出一版视觉概念图。
5. 通过浏览器截图检查桌面和移动端布局。

建议下一轮先做：

- `GET /api/line/summary`
- `GET /api/line/output-trend`
- 自研 dashboard 首页静态布局
- 绑定真实 API

