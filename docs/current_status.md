# 当前状态 / Codex 恢复上下文

更新时间：2026-06-27
工作目录：`/Users/chenjie/Documents/MES/edge-mes-demo`
树莓派部署目录：`/opt/edge-mes-demo`

## 0. 当前 PM / Codex 协作状态

当前主线：Phase-2 Sprint 3 Slice B runtime adapter gate closeout。

Last verified baseline before this docs sync:

```text
last verified HEAD / origin/main at authoring time:
c677515eab36ec0e39bb587a1f3c7bc3edbf2f41
c677515 Implement Sprint 3 Slice B runtime adapter gate

branch:
main

tag:
phase1-pass-20260619
```

Note: live `HEAD` / `origin/main` must be checked with `git rev-parse` in each
Thread. This durable baseline is an audit marker from the status sync time, not
a requirement that the document hash exactly match `HEAD` after later docs-only
commits.

当前 Sprint 3 gate：

```text
Slice B runtime adapter gate implementation: PASS
Slice B Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice B Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice B Verification focused review / allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice B exact allowlist commit/push: PASS, commit c677515
Slice A mapping contract hardening: PASS, commit 706f5da
Offline adapter implementation: PASS
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Verification focused review: PASS WITH RECOMMENDATIONS, no blocker
Exact allowlist commit/push: PASS, commit b43a12f
R-N1/R-N2 hardening commit/push: PASS, commit 577c1a1
Docs/status sync: PASS, commit fd79e21
Docs/status baseline repair: PASS, commit 4f424c6
PM rules / baseline semantics repair: PASS, commit e284a06
Eligible for downstream PM planning for next runtime slice: yes
DB/API/Dashboard/V-PLC/deploy/tag/rollback/real PLC pilot: not authorized
```

当前 Sprint 3 Slice B implementation files 已提交：

```text
collector/app/services/event_collector.py
collector/app/services/station_event_runtime_source.py
collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py
tests/test_collector_station_event_runtime_source.py
collector/tests/test_event_collector_adapter_gate.py
```

Slice B runtime adapter gate summary:

```text
runtime adapter gate implemented and committed at c677515.
adapter gate inserted after payload/cycle/counter guards and counter reset fail-safe, before existing storage.persist_cycle().
accepted-only path continues to existing storage.persist_cycle() plus existing read_done/ACK behavior.
non-accepted decisions do not persist, do not project, do not write defect detail, and do not ACK.
adapter remains non-owner of ACK/read_done.
```

当前 Sprint 3 offline adapter implementation files 已提交：

```text
collector/app/services/resolved_config_registry.py
collector/app/services/station_event_adapter.py
tests/test_collector_station_event_adapter.py
```

当前 Sprint 3 recommendation hardening 已完成：

```text
R-N1 / DQ-N1 / V-N1: CLOSED, resolved snapshot content hash self-check implemented.
R-N2 / DQ-N2 / V-N2: CLOSED, route predecessor and direct parent negative fixtures clarified.
Reliability / Data Quality / Verification focused review: PASS WITH RECOMMENDATIONS, no blocker.
Exact allowlist commit/push: PASS, commit 577c1a1.
Docs/status sync completed at fd79e21.
Docs/status baseline repair completed at 4f424c6.
PM rules / baseline semantics repair completed at e284a06.
```

Slice B carry-forward recommendations:

```text
R-N1: future raw-capable/raw-required runtime source needs renewed raw evidence focused review.
R-N2: future diagnostic enrichment may split ADAPTER_GATE_FAILED vs non-accepted decisions, without changing ACK or production fact semantics.
```

当前外部既有 dirty artifacts，应排除，除非 PM 明确授权：

```text
M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

Codex Thread 应先读取：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- 对应 task-specific contract/report files

下方内容保留 Phase-1 / 早期 Demo 状态快照，供上下文恢复使用；当前开发 gate 以上方 Sprint 3 状态为准。

## 1. 项目一句话状态

Edge MES Demo 已经在树莓派上完成从 V-PLC 到 Collector、PostgreSQL、FastAPI 追溯页面和 Grafana dashboard 的 Phase-1 闭环。Phase-2 Sprint 1 flexible line configuration 与 Sprint 2 generic station event model 已完成；Sprint 3 当前聚焦 Collector ingestion adapter offline implementation，不等于 runtime Collector integration。

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
  - DB104 runtime / PLC identity
- 三工站并行 WIP。
- 全局 `unit_id` 从 WS01 创建并贯穿 WS02/WS03。
- 上游 NOK 后，下游工站仍接收该件，但写入 `process_status=SKIPPED`、`skip_reason=UPSTREAM_NOK`。
- WS03 对不合格件生成 `NG-xxxxxx`，并将工件状态置为不合格品处理。
- 未 ACK 的工站 payload 不允许被下一件覆盖。
- 默认严格 ACK；超过 10 秒 deadline 只置 `ack_timeout`，不释放 payload。
- DB104 提供运行期间稳定的 `plc_boot_id`、heartbeat 和持久化 restart counter。
- 手动 WIP/counter reset 会轮换 boot identity 并清除旧 station DB payload。
- station 参数由 `config/vplc.yaml` 统一提供。
- 支持 `normal / fast / test` Profile：
  - `normal` 固定 `scale=1.0`，并锁定 runtime base/jitter 编辑。
  - `fast/test` 只通过 scale 加速，不改变约 30 秒的 process baseline。
- `/vplc/state` 返回当前 profile、scale、配置来源和 config hash。
- 参数修改必须提供 reason，并记录 actor、client IP、request ID、old/new 和接受/拒绝状态。
- startup、runtime update、reset 和周期性参数快照写入审计链路。
- 强制 NOK 支持按工站 code 白名单排队 1–100 件，并可查询或清除 pending 队列。
- 支持：
  - 连续生产
  - 按小时
  - 按件数
  - 按班次
  - 暂停/恢复工站
  - `fast/test` 模式修改节拍、波动
  - 修改 NOK 率
  - 批量强制 NOK 和清除 pending NOK
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
- 数据提交成功后才写回 `read_done`。
- ACK 写回失败标记 `ACK_WRITE_FAILED` 并在后续轮询重试。
- Collector 重启后通过 PLC 当前 payload 和数据库幂等键补 ACK。
- 同 boot counter 下降会记录 `PLC_COUNTER_RESET` 并停止 ACK。
- 连接、identity、读取/解码、存储和 ACK 错误写入 `collector_error_log`。

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
      runtime_config.py
      parameter_audit.py
    tests/
      test_pipeline_uid_flow.py
      test_reliability.py
      test_runtime_config.py
      test_parameter_audit.py
      test_nok_simulation.py

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
    vplc.yaml
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
    edge_expansion_plan.md
    plc_edge_integration_guide.md
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
- `plc_edge_integration_guide.md` 是面向现场 PLC 工程师和技师的通用接入规范，覆盖 S7-300/S7-1200/S7-1500。
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
- 高频信号由 MCU 或专用采集器采集，每个零件输出 CSV/JSON 文件，Edge 负责解析、特征提取、关联和归档。
- 参数管理只读校验，不主动回写 PLC；PLC 侧修改后通知 Edge 读取并记录 changelog。
- 工业相机图片/视频只做短期本地缓存，默认 7 天。
- 归档支持移动硬盘冷备份和服务器热备份，均作为可勾选任务。
- 权限管理需要支持账号、令牌和人脸/指纹等生物识别外设。
- AI 推理和长期数据处理放到 Nvidia 边缘设备或服务器，Edge 只接收结果。

## 5. 重要约束

- 当前 Demo 是单台设备、单条产线、单个 PLC；长期目标最多 3 条流水线。
- 当前树莓派是 8GB，SSD，性能足够当前 Demo。
- 不要破坏旧 `edge_mes_overview` dashboard。
- 不要删除旧 `production_snapshot` 链路。
- `config/plc_mapping.yaml` 是旧 DB100 映射。
- `config/mapping.yaml` 是新三工站协议映射。
- DB100 当前存在 legacy 兼容，不应直接假设已经完全符合新协议。
- V-PLC 当前端口 1102；真实 PLC 可能为 102。
- 默认严格 ACK；deadline 默认 10 秒，未 ACK payload 不会自动清除或被覆盖。
- 当前 API/Grafana 无生产级认证设计。
- Oracle / `sync-worker` 属于 Phase-2 Out of Scope；当前只保留 mock，不实施真实 Oracle 集成。
- 电子 SOP 暂不需要。
- 维护保养模块暂不需要。
- 图片/视频长期存储不放在树莓派本地。
- 高频原始信号不由树莓派直接采集。

## 6. 未完成事项

高优先级：

- 实现 Ignore Edge / Bypass 与 `data_gap_event`。
- 在树莓派 PostgreSQL 执行 `db/migrations/005_reliability_schema.sql` 并完成容器级故障恢复验收。

中优先级：

- 增强追溯 API，显示缺站原因和采集缺口边界。
- 对旧历史数据执行一次可选回填，将已有 `cycle_event` 尽量派生为 `station_event` / `production_unit`。
- Grafana 增加数据质量面板。
- V-PLC 增加断线、写失败、ACK 失败模拟。
- 增加故障注入控制项，便于手工触发 ACK 写失败和断线。
- 参数管理与 changelog。
- MCU CSV/JSON 文件接入与特征提取。
- 工业相机图片/视频元数据与 7 天保留。
- 归档任务管理。
- 权限、令牌和生物识别适配。

后续产品化：

- 自研 dashboard。
- 3D 设备/物料流动数字孪生首页。
- 用户权限、审计日志、配置持久化。
- 真实 PLC 接入演练。
- AI / Nvidia 边缘设备结果接入。

## 7. 下一步建议

可靠性代码闭环已完成；建议下一步按以下顺序推进：

1. 部署迁移与容器验收
   - 在树莓派执行 `db/migrations/005_reliability_schema.sql`。
   - 重建 V-PLC / Collector，执行断线、重启、ACK timeout 和 reset 验收。

2. Ignore Edge / data gap
   - 正式启用整线 `ignore_edge` bit。
   - 数据缺口写入 `data_gap_event`。
   - 按 WS03 label_code 序号计算缺件。

3. 验证与回归
   - 建立可靠性、数据缺口和端到端验证矩阵。
   - 保存每个 Thread 的验证报告。

4. 自研 dashboard 初版
   - 不替代 Grafana 工程看板。
   - 面向操作员/管理层。
   - 为后续 3D 数字孪生做入口。

Phase-2 Out of Scope：

- Oracle schema、真实连接、主动 push、重试和幂等。
- `sync-worker` 只保留现有 mock 行为，不作为本阶段验收项。

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
