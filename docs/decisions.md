# 关键设计决策记录

更新时间：2026-06-16

## ADR-001: 本地数据库使用 PostgreSQL

决策：

- 本地 Edge 数据库使用 PostgreSQL。
- 远端服务器数据库是 Oracle，但本地不直接使用 Oracle。

原因：

- PostgreSQL 在树莓派上部署简单。
- Grafana 对 PostgreSQL 支持成熟。
- 本地离线运行更轻量。
- Oracle 作为未来同步目标，由 sync worker 主动推送。

影响：

- 当前 schema 以 PostgreSQL 为准。
- 将来 Oracle 同步需要做字段映射和幂等策略。

## ADR-002: 保留旧 DB100 快照链路

决策：

- 旧 `config/plc_mapping.yaml` 和 DB100 快照链路保留。
- 新三工站协议放在 `config/mapping.yaml`。

原因：

- 旧 Grafana 单线生产总览依赖 `production_snapshot`。
- 直接切 DB100 会造成已有 dashboard 掉线。
- 新协议还在演进，不宜破坏旧 demo。

影响：

- DB100 当前存在语义兼容负担。
- `ignore_edge` 在 mapping 中定义，但运行链路尚未完全切换。
- 后续需要一次正式 DB100 语义迁移。

## ADR-003: 三工站使用 DB101/DB102/DB103

决策：

- WS01 使用 DB101。
- WS02 使用 DB102。
- WS03 使用 DB103。
- 三个工站共用公共 header，payload 从 DBB100 开始。

原因：

- 更接近真实多工站 PLC DB 结构。
- Collector 可按 station read plan 独立读取。
- 便于 Grafana、API 按 station 维度统计。

影响：

- Collector 必须支持 mapping parser 和 read plan。
- V-PLC 必须注册多个 DB。

## ADR-004: V-PLC 先模拟 S7 DB 通讯，不直接接硬件

决策：

- Demo 阶段使用 Snap7 Server 模拟 S7 PLC。
- 真实 PLC 接入后，再切换 Snap7 Client host/port。

原因：

- 无需硬件即可展示完整采集链路。
- 可在虚拟环境调试 DB 协议、Collector、dashboard。
- 可以主动制造故障、NOK、停机和 WIP。

影响：

- 当前 Snap7 端口为 1102。
- 真实 PLC 常用 102，需要部署时调整。

## ADR-005: 三工站为并行流水线 WIP

决策：

- 三个工站不是单线程顺序执行。
- V-PLC 内部维护 WIP 队列：
  - WS01 -> WS02
  - WS02 -> WS03

原因：

- 更接近真实流水线。
- 可以展示 WIP、工站等待、并行 cycle。
- 时间戳追溯边界风险更低。

影响：

- 数据库展示层仍可按 DMC/label_code/序号追溯。
- 后续真实系统建议增加明确 trace_id。

## ADR-006: 追溯优先使用 UID，DMC/Label/Reject 作为入口

决策：

- WS01 创建全局 `unit_id`，格式示例 `U-20260616-000052`。
- WS02/WS03 必须继承同一个 `unit_id`。
- WS01/WS02 使用 `SUB-000052`。
- WS03 使用 `ASM-000052`。
- 不合格最终由 WS03 生成 `NG-000052`。
- API 查询时先定位 seed event，再优先按 `unit_id` 拉取 WS01/WS02/WS03。
- `SUB`、`ASM`、`NG`、尾部序号只是用户查询入口，不再作为主关联键。

原因：

- 并行 WIP 场景下，单靠时间戳、序号或 DMC 尾号推断会有错配风险。
- UID 更接近真实 MES 中的 unit/workpiece instance。
- DMC/Label/Reject 的业务语义不同，不应承担唯一主键职责。

风险：

- 真实 PLC 接入时，需要在 DB 中提供等价 UID、载具 ID 或可稳定生成的工件实例 ID。
- 如果真实 PLC 无法提供 UID，Edge 需要定义严格的生成与断点恢复策略。

后续：

- 与真实 PLC DB 协议对齐 UID 字段。
- 定义 UID 在断电、换班、counter reset 后的恢复规则。

## ADR-007: Collector 事件采集不替代旧快照采集

决策：

- Collector 主循环继续采集旧 `production_snapshot`。
- 新事件采集作为后台 worker 并行运行。

原因：

- 兼容旧 dashboard。
- 降低切换风险。
- 便于对比新旧数据链路。

影响：

- Collector 内有两条链路：
  - old snapshot source
  - new event collector worker

## ADR-008: V-PLC 三工站与旧 simulator 停机解耦

决策：

- 旧 simulator 仍驱动 DB100 legacy running。
- DB101/102/103 三工站由 V-PLC 控制台的 production plan 控制。

原因：

- 旧 simulator 有随机报警/停机，曾导致三个 WS 同时 IDLE/STOP。
- 用户需要独立定义连续生产多少小时、班次或件数。

影响：

- `/vplc` 页面中的整线 RUN/STOP 以 V-PLC production plan 为准。
- `external_running` 仍保留在状态 JSON 中用于调试旧 DB100 来源。

## ADR-009: V-PLC 默认不强制 ACK

决策：

- 当前 `require_ack=false`。
- payload_ready 默认保持约 10 秒。
- 工站在 `payload_ready=true` 且未被 ACK/自动清除前，不会启动下一件。
- Collector 正常会写回 `read_done` 并将 `ack_status=ACK_OK`。

原因：

- Demo 阶段避免 Collector 短暂重启导致 V-PLC 停死。
- 未 ACK 禁止启动下一件，避免高节拍 demo 下 payload 被覆盖。

风险：

- 这不是最严格的真实 PLC 握手。

后续：

- 增加真实模式：
  - 未 ACK 不清除
  - 超时置 `ack_timeout`
  - Collector 重启后补 ACK

## ADR-013: 增加 station_event 与 production_unit

决策：

- 保留 `cycle_event` 作为兼容表。
- 新增 `station_event` 作为工站履历追加表。
- 新增 `production_unit` 作为工件当前状态表。
- 新增 `unit_state_history` 记录状态变化。

原因：

- Grafana 和旧 API 已经依赖 `cycle_event`，不宜破坏。
- 追溯页面需要按工件展示完整履历，而不是只看散落的工站 cycle。
- “进行中 / 已完成合格 / 不合格”属于工件状态，不是单条 cycle 状态。

影响：

- Collector 写入 `cycle_event` 后，会派生写入 `station_event` 和 `production_unit`。
- Trace API 优先按 `unit_id` 查询 `cycle_event`，最近记录按 `production_unit` 分组。

## ADR-010: Grafana 用作工程监控，自研 dashboard 留到后续

决策：

- 当前继续使用 Grafana 展示工程监控和数据验证。
- 数字孪生、3D、动画首页暂不放在 Grafana 内实现。

原因：

- Grafana 快速、稳定，适合时序和 SQL dashboard。
- Grafana 对复杂自定义 UI、3D、物料动画不适合。

影响：

- 已有 dashboard：
  - 单线生产总览
  - 树莓派主机监控
  - 三工站追溯与采集监控
- 后续自研前端可以复用 API 和 PostgreSQL 数据模型。

## ADR-011: 系统必须离线可运行

决策：

- 本地所有核心功能运行在树莓派 Docker Compose 中。
- 不依赖外部云服务。

原因：

- 工业现场可能无稳定公网。
- Edge 采集与展示必须本地可用。

影响：

- 外部 Oracle 只是未来同步目标。
- sync worker 应采用主动推送、断点续传、重试。

## ADR-012: 文档作为 Codex 恢复上下文入口

决策：

- 新增 5 份核心文档：
  - `docs/architecture.md`
  - `docs/protocol.md`
  - `docs/task_plan.md`
  - `docs/decisions.md`
  - `docs/current_status.md`

原因：

- 当前项目已包含 V-PLC、Collector、API、Grafana、数据库多模块。
- 后续 Codex 恢复上下文需要稳定入口，避免依赖聊天历史。
