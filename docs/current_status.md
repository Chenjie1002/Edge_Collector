# 当前状态 / Codex 恢复上下文

更新时间：2026-06-16  
工作目录：`/Users/chenjie/Documents/MES/edge-mes-demo`  
树莓派部署目录：`/opt/edge-mes-demo`

## 1. 项目一句话状态

当前 Edge MES Demo 已经在树莓派上完成从 V-PLC 到 Collector、PostgreSQL、FastAPI 追溯页面和 Grafana dashboard 的闭环。系统可以离线运行，模拟单条产线、一个 PLC、三个工站，并按 S7 DB 协议采集生产事件。

## 2. 已完成内容

### 基础设施

- Docker Compose 多服务部署。
- PostgreSQL 本地数据库。
- Grafana dashboard provisioning。
- Prometheus + node-exporter 主机监控。
- Sync worker mock，预留 Oracle 主动同步。

### V-PLC

- `s7-plc-sim` 使用 Snap7 Server。
- 暴露：
  - S7 DB 通讯端口：`1102`
  - V-PLC 控制台：`8200`
- 注册 DB：
  - DB100 legacy
  - DB101 WS01
  - DB102 WS02
  - DB103 WS03
- 三工站并行 WIP。
- 全局 `unit_id` 从 WS01 创建并贯穿 WS02/WS03。
- 上游 NOK 后，下游工站仍接收该件，但写入 `process_status=SKIPPED`、`skip_reason=UPSTREAM_NOK`。
- WS03 对不合格件生成 `NG-xxxxxx`，并将工件状态置为不合格品处理。
- 未 ACK 的工站 payload 不允许被下一件覆盖。
- 支持：
  - 连续生产
  - 按小时
  - 按件数
  - 按班次
  - 暂停/恢复工站
  - 修改节拍、波动、NOK 率
  - 强制 NOK
  - 重置 WIP/counter

入口：

- `http://10.0.0.217:8200/vplc`

### Collector

- 旧快照链路仍采集 DB100 到 `production_snapshot`。
- 新事件链路读取 DB101/102/103。
- 写入：
  - `raw_plc_sample`
  - `cycle_event`
  - `station_event`
  - `production_unit`
  - `unit_state_history`
  - `quality_event`
  - `collector_runtime_status`
- 写回 `read_done`。
- 更新 `ack_status=ACK_OK`。

### API

- FastAPI 运行在 `8000`。
- 已有 KPI SVG 和 summary API。
- 新增三工站追溯：
  - `/trace`
  - `/trace/api`
  - `/trace/api/by-cycle`
  - `/trace/api/recent`

验证过：

- OK 件：`U-20260616-000001` -> WS01/WS02/WS03 三站完整，最终 `ASM-000001`。
- NOK 件：`U-20260616-000014` -> WS01=NOK，WS02/WS03=SKIPPED，最终 `ASM-000014` + `NG-000014`。
- `ASM-000014` 和 `NG-000014` 均可通过 `/trace/api` 查到完整三站。

### Grafana

已有 dashboard：

- `edge_mes_overview.json`
  - URL: `http://10.0.0.217:3000/d/edge-mes-overview`
  - 旧单线生产总览。
- `raspberry_pi_host_monitor.json`
  - URL: `http://10.0.0.217:3000/d/raspberry-pi-host-monitor`
  - 树莓派 CPU、内存、磁盘、温度等。
- `edge_mes_station_traceability.json`
  - URL: `http://10.0.0.217:3000/d/edge-mes-station-traceability`
  - 三工站 cycle time、产出、OK/NOK、NOK code、ACK、Collector 状态、最近追溯记录。

## 3. 当前文件结构

```text
edge-mes-demo/
  docker-compose.yml
  README.md
  .env.example

  api/
    Dockerfile
    requirements.txt
    app/
      main.py
      db.py
      routes/
        health.py
        machines.py
        kpi.py
        events.py
        sync.py
        trace.py

  collector/
    Dockerfile
    requirements.txt
    app/
      main.py
      config.py
      models.py
      plc/
        address.py
        decoder.py
        mapping.py
        read_plan.py
      services/
        storage.py
        event_detector.py
        event_collector.py
      sources/
        base.py
        simulator_source.py
        snap7_source.py

  s7_plc_sim/
    Dockerfile
    requirements.txt
    app/
      main.py
      plc_db.py
      pipeline.py
      control_api.py
    tests/
      test_pipeline_uid_flow.py

  simulator/
    Dockerfile
    requirements.txt
    app/
      main.py
      models.py
      simulator.py

  sync_worker/
    Dockerfile
    requirements.txt
    app/
      main.py

  config/
    app.yaml
    simulator.yaml
    plc_mapping.yaml
    mapping.yaml
    grafana/
      dashboards/
        dashboard.yaml
        edge_mes_overview.json
        edge_mes_station_traceability.json
        raspberry_pi_host_monitor.json
      datasources/
        postgres.yaml
        prometheus.yaml
      custom/
        grafana-custom-font.css
        grafana-custom.ttf
    prometheus/
      prometheus.yml

  db/
    init/
      001_schema.sql
      002_seed.sql
      003_event_schema.sql
      004_unit_trace_schema.sql

  scripts/
    generate_shift_demo_sql.py
    validate_edge_mapping.py
    read_s7_station_sample.py

  docs/
    architecture.md
    protocol.md
    task_plan.md
    decisions.md
    current_status.md
    edge_mes_demo_srs.md
    kpi_definitions.md
    custom_dashboard_plan.md
    plc_address_map.md
    scenario_control.md
```

说明：

- 目录中可能存在 `__pycache__`，它们不是源文件，不应作为文档依据。
- 部署时打包应排除 `__pycache__` 和 `*.pyc`。
- `edge_mes_demo_srs.md` 是当前正式技术方案与 SRS。
- `kpi_definitions.md` 是当前 KPI 口径与度量计划。
- `custom_dashboard_plan.md` 是后续自研 dashboard 与数字孪生首页规划。

## 4. 关键设计决策

- 本地数据库使用 PostgreSQL，远端 Oracle 仅作为未来同步目标。
- 保留旧 DB100 快照链路，避免旧 dashboard 失效。
- 新三工站协议使用 DB101/102/103。
- V-PLC 通过 Snap7 Server 模拟 S7。
- 三工站为并行 WIP，不是单线程顺序模拟。
- V-PLC 三工站从旧 simulator 的随机停机中解耦。
- Collector 旧快照采集和新事件采集并行运行。
- 当前追溯规则以 `unit_id` 为主关联键，`SUB/ASM/NG/序号` 只是查询入口。
- `cycle_event` 继续兼容旧查询；`station_event` 记录工站履历；`production_unit` 记录工件当前状态。
- Grafana 用于工程监控，自研数字孪生 dashboard 后续实现。
- 系统必须离线可运行。

## 5. 重要约束

- 单台设备、单条产线、单个 PLC。
- 当前树莓派是 8GB，SSD，性能足够当前 Demo。
- 不要破坏旧 `edge_mes_overview` dashboard。
- 不要删除旧 `production_snapshot` 链路。
- `config/plc_mapping.yaml` 是旧 DB100 映射。
- `config/mapping.yaml` 是新三工站协议映射。
- DB100 当前存在 legacy 兼容，不应直接假设已经完全符合新协议。
- V-PLC 当前端口 1102；真实 PLC 可能为 102。
- 默认不强制 ACK，payload_ready 保持约 10 秒；但未 ACK 的工站不会启动下一件，避免 payload 被覆盖。
- 当前 API/Grafana 无生产级认证设计。
- 当前 Oracle 同步未完成，只是 mock。

## 6. 未完成事项

高优先级：

- 将 `plc_boot_id` 从 collector 会话兜底升级为真实 PLC/V-PLC retained boot id。
- 实现真实 ACK timeout 和重试。
- 实现 counter reset 检测。
- 实现 Ignore Edge / Bypass 与 `data_gap_event`。
- 定义 Oracle 同步 schema 与幂等策略。

中优先级：

- 增强追溯 API，显示缺站原因和采集缺口边界。
- 对旧历史数据执行一次可选回填，将已有 `cycle_event` 尽量派生为 `station_event` / `production_unit`。
- Grafana 增加数据质量面板。
- V-PLC 增加断线、写失败、ACK 失败模拟。
- Collector 增加更完整错误日志。

后续产品化：

- 自研 dashboard。
- 3D 设备/物料流动数字孪生首页。
- 用户权限、审计日志、配置持久化。
- 真实 PLC 接入演练。

## 7. 下一步建议

建议下一步做 **可靠性补强**，顺序：

1. `plc_boot_id` 修正
   - 让 V-PLC 在稳定地址写 boot id。
   - Collector 正确读取并入库。

2. ACK 真实模式
   - 支持 `require_ack=true`。
   - 超时置 `ack_timeout`。
   - Collector 重启后补 ACK。

3. Ignore Edge / data gap
   - 正式启用整线 `ignore_edge` bit。
   - 数据缺口写入 `data_gap_event`。
   - 按 WS03 label_code 序号计算缺件。

4. Oracle sync worker
   - 设计远端表。
   - 实现主动 push。
   - 支持断网重试和幂等。

5. 自研 dashboard 初版
   - 不替代 Grafana 工程看板。
   - 面向操作员/管理层。
   - 为后续 3D 数字孪生做入口。

## 8. 常用命令

树莓派：

```bash
cd /opt/edge-mes-demo
docker compose ps
docker logs --tail 80 edge-mes-collector
docker logs --tail 80 edge-mes-s7-plc-sim
docker exec edge-mes-postgres psql -U edge_mes -d edge_mes
```

本地校验：

```bash
python3 -m compileall api/app collector/app s7_plc_sim/app
python3 scripts/validate_edge_mapping.py
python3 -m json.tool config/grafana/dashboards/edge_mes_station_traceability.json
```

追溯 API 示例：

```bash
curl 'http://10.0.0.217:8000/trace/api?q=ASM-000014'
curl 'http://10.0.0.217:8000/trace/api?q=NG-000014'
curl 'http://10.0.0.217:8000/trace/api/by-cycle?station_id=WS03&cycle_counter=14'
```
