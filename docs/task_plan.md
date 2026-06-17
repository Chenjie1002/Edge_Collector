# 开发顺序与阶段目标

更新时间：2026-06-16

## 1. 总体目标

在树莓派 5B 上实现一套离线可运行的 Edge MES Demo：

1. 模拟 S7 PLC。
2. 采集 WS01/WS02/WS03 三工站数据。
3. 存入本地 PostgreSQL。
4. 提供追溯 API 和页面。
5. 使用 Grafana 做工程监控。
6. 预留将来主动同步到远端 Oracle。
7. 后续扩展自研 dashboard 和数字孪生首页。

## 2. 已完成阶段

### Phase 0 - 基础 Demo 与旧 Dashboard

已完成：

- Docker Compose 基础服务。
- PostgreSQL。
- 旧业务 simulator。
- 旧 DB100 快照映射。
- Collector 快照采集。
- Grafana 单线生产总览。
- 树莓派主机监控 dashboard。
- Grafana 字体自定义。

### Phase 1 - 事件模型与 Mapping

已完成：

- 新增 `config/mapping.yaml`。
- 固化 DB100/101/102/103 目标协议。
- 新增事件表：
  - `raw_plc_sample`
  - `cycle_event`
  - `quality_event`
  - `collector_runtime_status`
  - `collector_error_log`
  - `data_gap_event`
- Collector 增加 S7 address parser、mapping parser、read plan、decoder。

### Phase 2 - V-PLC 三工站模拟

已完成：

- Snap7 Server 注册 DB100、DB101、DB102、DB103。
- WS01/WS02/WS03 三工站并行 WIP 模型。
- WS01 Screw payload。
- WS02 EOL payload。
- WS03 Label/final payload。
- `payload_ready/read_done/cycle_valid` 握手。
- NOK 随机与强制 NOK。
- V-PLC 控制台 `http://10.0.0.217:8200/vplc`。
- 支持连续生产、按小时、按件数、按班次。
- 三工站已从旧 simulator 随机停机中解耦。
- 已加入 `unit_id` 工件实例 ID。
- 已实现上游 NOK 后下游 `SKIPPED` 流转。
- 已修复未 ACK payload 被下一件覆盖的风险。

### Phase 3 - Edge Collector 事件采集

已完成：

- Collector 后台事件采集线程。
- 按 `mapping.yaml` 读取 DB101/102/103。
- 写入 raw sample、cycle event、quality event、runtime status。
- 写回 `read_done`。
- 更新 `ack_status = ACK_OK`。
- 旧 production_snapshot 采集继续保留。
- 写入 `station_event` 工站履历。
- 写入 `production_unit` 工件当前状态。
- 写入 `unit_state_history` 状态变化记录。

### Phase 4 - 追溯 API、页面与 Grafana

已完成：

- 追溯 API：
  - `/trace/api?q=ASM-000052`
  - `/trace/api?q=SUB-000052`
  - `/trace/api?q=52`
  - `/trace/api/by-cycle?station_id=WS03&cycle_counter=50`
  - `/trace/api/recent`
- 追溯页面：
  - `/trace`
  - `/trace?q=ASM-000052`
- Grafana 新 dashboard：
  - `edge_mes_station_traceability.json`
  - URL: `http://10.0.0.217:3000/d/edge-mes-station-traceability`
- 已验证三站完整链路样例：
  - OK 件：`U-20260616-000001` / `ASM-000001`
  - NOK 件：`U-20260616-000014` / `ASM-000014` / `NG-000014`
  - `ASM-000014` 和 `NG-000014` 均可查到 WS01/WS02/WS03 完整履历

## 3. 当前未完成事项

### 高优先级

1. 修复/完善 `plc_boot_id`
   - 当前 Collector 尝试从 DB100 读取 boot id。
   - 由于 DB100 仍兼容旧 dashboard，新事件中可能出现 `UNKNOWN`。
   - 后续应将 boot id 固化到不冲突的 DB100 地址或每个 station DB。

2. 真实 ACK 模式
   - 当前 V-PLC 默认 `require_ack=false`，payload 保持约 10 秒。
   - 后续需要提供真实模式：未 ACK 不清除，超时置 `ack_timeout`。

3. 真实 UID 对齐
   - Demo 已实现 `unit_id`。
   - 真实 PLC 接入前要确认 PLC 侧提供 UID、载具 ID，或允许 Edge 按严格规则生成 UID。
   - 需要定义断电、counter reset、换班后的 UID 恢复规则。

4. Ignore Edge / Bypass 数据缺口
   - 表已预留：`data_gap_event`。
   - 逻辑未完整实现。
   - 要按 WS03 label_code 计数字段计算缺失件数。

### 中优先级

5. Oracle 主动同步
   - 当前 `sync-worker` 为 mock。
   - 需要定义 Oracle schema、同步批次、失败重试、幂等键。

6. Grafana dashboard 进一步打磨
   - 当前是工程监控 dashboard。
   - 可以继续优化变量、链接、阈值、表格字段、数据质量提示。

7. API 追溯规则增强
   - 增加按时间范围、结果、NOK code 查询。
   - 增加缺站提示。
   - 增加 raw sample drill-down。

8. 采集可靠性测试
   - 模拟断线、重连、ACK 失败、counter reset。
   - 验证 Collector 恢复策略。

### 低优先级 / 后续产品化

9. 自研 dashboard
   - 面向操作员/管理者，不受 Grafana panel 限制。
   - 可作为数字孪生首页入口。

10. 3D 设备与物料流动
   - 当前未实现。
   - 后续适合基于自研前端、Three.js 或轻量 Canvas 实现。

11. 权限与用户管理
   - 当前 demo 默认开放。
   - 生产环境需要登录、角色、审计。

## 4. 下一步执行顺序

建议顺序如下：

1. **可靠性补强**
   - 固化 `plc_boot_id`
   - 实现真实 ACK timeout
   - 实现 counter reset 检测
   - 实现 reconnect 后未 ACK payload 重试

2. **数据缺口与 Bypass**
   - 正式启用 `ignore_edge`
   - 完成 `data_gap_event`
   - 用 WS03 label_code 序号计算缺失件数

3. **Oracle 同步设计与实现**
   - 定义远端 Oracle 表
   - 定义本地 outbox 到 Oracle 的映射
   - 实现主动 push、重试、幂等

4. **Grafana 和追溯增强**
   - 增加数据质量/缺站指标
   - 增加 trace URL drill-down
   - 增加 station runtime 状态颜色阈值

5. **自研 dashboard 原型**
   - 独立于 Grafana
   - 首页显示整线状态、三工站状态、WIP、产量、节拍、NOK
   - 后续接 3D/数字孪生

6. **真实 PLC 接入准备**
   - 将 `config/mapping.yaml` 与真实 DB 协议对齐
   - 在测试环境切换 host/port/rack/slot
   - 用只读模式先验证 DB decode
   - 再启用 write `read_done`

## 5. 阶段验收建议

每个阶段至少验证：

- Docker 服务均为 running。
- API 对关键接口返回 200。
- Collector 无持续异常日志。
- Grafana dashboard 已 provision。
- PostgreSQL 有新数据写入。
- 关键链路可用：
  - V-PLC 生成 cycle
  - Collector 写入 `cycle_event`
  - API 查到 trace
  - Grafana 展示指标
