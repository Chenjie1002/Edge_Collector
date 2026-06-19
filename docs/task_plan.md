# 开发顺序与阶段目标

更新时间：2026-06-17

## 1. 总体目标

在树莓派 5B 上实现一套离线可运行的 Edge MES Demo：

1. 模拟 S7 PLC。
2. 采集 WS01/WS02/WS03 三工站数据。
3. 存入本地 PostgreSQL。
4. 提供追溯 API 和页面。
5. 使用 Grafana 做工程监控。
6. 预留将来主动同步到远端 Oracle。
7. 后续扩展自研 dashboard 和数字孪生首页。
8. 后续最多扩展到 3 条流水线，并增加参数管理、MCU 文件接入、媒体归档、权限认证和 AI 结果接入。

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

### Phase 5 - 参数管理与 Changelog

计划目标：

- 对所有接入产线的可编辑参数集中管控。
- Edge 只读取和校验 PLC 参数，不主动回写 PLC。
- PLC 侧参数修改后通知 Edge 读取。
- 被授权账号登录后可修改参数，不需要审批流。
- 精确记录参数 changelog。

计划交付：

- `parameter_definition`
- `parameter_snapshot`
- `parameter_change_log`
- 参数读取/校验 API
- 参数变更查询页面或 Grafana 表格

### Phase 6 - MCU 高频文件接入与特征提取

计划目标：

- MCU 或专用采集器负责高频原始采集。
- 每个零件生成一个 CSV 或 JSON 文件。
- Edge 抓取、解析、处理、分析、存档文件。
- 文件与 `unit_id`、DMC、station_id 或时间戳关联。

计划交付：

- `part_data_file`
- `signal_feature`
- CSV/JSON parser
- 文件接入目录监听或上传 API
- 特征提取任务

### Phase 7 - 工业相机图片/视频接入

计划目标：

- 支持工业相机输出的图片或视频。
- 本地默认保留 7 天，可配置。
- 超期后归档或删除。
- 媒体与 `unit_id`、station_id、camera_id、capture_time 关联。

计划交付：

- `media_file`
- 媒体元数据 API
- retention job
- 追溯页面媒体链接

### Phase 8 - 归档与冷热备份

计划目标：

- 支持数据库历史、MCU 文件、图片/视频和日志归档。
- 支持按月或按季度强制归档。
- 支持移动硬盘冷备份和服务器热备份，二者均为可勾选项。

计划交付：

- `archive_job`
- `archive_job_item`
- 移动硬盘挂载检测
- 服务器上传接口
- 手动和定时归档任务

### Phase 9 - 权限、令牌与生物识别适配

计划目标：

- 建立用户、角色和权限体系。
- 支持令牌验证。
- 支持人脸识别模块或指纹模块等生物识别外设。
- 参数修改、归档任务、配置变更必须记录操作审计。

计划交付：

- `user_account`
- `role_permission`
- `auth_event`
- `operation_audit_log`
- 生物识别外设 adapter 接口

### Phase 10 - AI / Nvidia 边缘设备结果接入

计划目标：

- 树莓派不承担 AI 训练或重推理。
- Nvidia 边缘设备负责推理。
- Edge 接收 AI 结果并关联追溯。

计划交付：

- `ai_inference_result`
- AI 结果接收 API
- 模型版本、置信度、缺陷类型、推理耗时记录

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

5. Oracle 主动同步（Phase-2 Out of Scope）
   - 当前 `sync-worker` 只保留 mock。
   - 本阶段不定义 Oracle schema，不实现连接、push、失败重试或幂等。

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

9. 参数管理与 changelog
   - 参数定义、参数快照、变更日志。
   - PLC 参数修改通知后的读取和校验。

10. MCU CSV/JSON 文件接入
   - 每件一个高频采集文件。
   - 文件元数据、解析状态和特征提取。

11. 工业相机媒体接入
   - 图片/视频元数据。
   - 本地 7 天保留策略。

12. 归档任务管理
   - 移动硬盘冷备份。
   - 上传服务器热备份。
   - 按月/季度归档。

### 低优先级 / 后续产品化

13. 权限、令牌与生物识别适配
   - 用户、角色、令牌、人脸/指纹外设。
   - 参数修改和配置变更审计。

14. 自研 dashboard
   - 面向操作员/管理者，不受 Grafana panel 限制。
   - 可作为数字孪生首页入口。

15. 3D 设备与物料流动
   - 当前未实现。
   - 后续适合基于自研前端、Three.js 或轻量 Canvas 实现。

16. AI / Nvidia 边缘设备结果接入
   - Edge 只接收 AI 结果。
   - AI 推理和模型运行由外部 Nvidia 设备完成。

明确后置或排除：

- 电子 SOP 暂不需要。
- 维护保养模块暂不需要。
- 高频原始采样不由树莓派直接完成。
- 图片/视频长期存储不放在树莓派本地。
- 长期大数据分析和 AI 重计算放到其他设备或服务器。

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

3. **验证与回归**
   - 建立 ACK、PLC 重启、counter reset、Collector 重启和 data gap 测试矩阵
   - 验证 V-PLC -> Collector -> PostgreSQL -> API/Grafana 闭环
   - 将结果保存到 `docs/reports/`

4. **Grafana 和追溯增强**
   - 增加数据质量/缺站指标
   - 增加 trace URL drill-down
   - 增加 station runtime 状态颜色阈值

5. **参数管理与 changelog**
   - 参数定义
   - 参数快照
   - 参数变更日志
   - PLC 参数修改通知后的读取和校验

6. **MCU 文件接入**
   - CSV/JSON 文件格式
   - 每件一个文件
   - 文件元数据和特征提取

7. **媒体和归档**
   - 工业相机图片/视频元数据
   - 7 天保留策略
   - 移动硬盘和服务器归档任务

8. **权限认证**
   - 用户角色
   - 令牌
   - 人脸/指纹外设适配
   - 操作审计

9. **自研 dashboard 原型**
   - 独立于 Grafana
   - 首页显示整线状态、三工站状态、WIP、产量、节拍、NOK
   - 后续接 3D/数字孪生

10. **真实 PLC 接入准备**
   - 将 `config/mapping.yaml` 与真实 DB 协议对齐
   - 在测试环境切换 host/port/rack/slot
   - 用只读模式先验证 DB decode
   - 再启用 write `read_done`

Phase-2 Out of Scope：

- Oracle schema 和真实数据库连接。
- outbox 到 Oracle 的真实同步、重试和幂等。
- 修改 `sync-worker` 的 mock 定位。

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
