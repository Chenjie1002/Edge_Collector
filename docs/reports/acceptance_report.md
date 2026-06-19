# Edge MES Acceptance Report

日期：2026-06-19  
验收范围：单机、单产线、单 PLC、三工站 Edge MES Demo  
目标主机：Raspberry Pi `Pi-5b-Li`（`10.0.0.217`）  
最终结论：**PASS / 通过**

最终复验：2026-06-19  
[`final_acceptance_validation_report.md`](final_acceptance_validation_report.md) 已确认
ACPT-H-01 关闭，完整 Acceptance Sprint 通过。
[`rollback_drill_report.md`](rollback_drill_report.md) 已确认真实回滚与恢复通过。
[`final_phase1_pass_report.md`](final_phase1_pass_report.md) 已独立确认 Recent API 与
Grafana Profile 隔离修复进入 live 运行环境，并再次完成 by-cycle 与完整 Acceptance
Sprint。Phase 1 总验收升级为 `PASS`。

## 1. Executive Summary

本次验收没有新增业务功能、没有修改架构、没有修改协议、数据库结构或公共接口。
验收通过已有 V-PLC、FastAPI、Grafana 和 PostgreSQL 数据源执行，发现问题后只调整
验收脚本，不修改业务逻辑。

核心生产闭环具备客户演示基础：

- V-PLC 当前为 `normal` Profile、`scale=1.0`、`require_ack=true`。
- 同一个 PLC boot 连续运行 6,206 秒，约 103 分钟。
- WS01/WS02/WS03 counter 分别连续到 `200/199/198`。
- 当前 boot 每站数据库行数等于 counter 最大值，且唯一 counter 数相同。
- 当前 boot 非 `ACK_OK` 事件为 0。
- 未发现重复幂等键。
- WS03 共 198 条记录，198 个不同 UID，序号从 1 连续到 198。
- 正常三站流程、WS01/WS02/WS03 NOK、上游 NOK 后下游 SKIPPED 均通过。
- NOK Code、Raw PLC Payload、Trace、`quality_event`、Grafana PostgreSQL 数据源一致。
- API 和 Grafana 健康检查正常，Collector 三站均为 `RUNNING / CONNECTED`。

ACPT-H-01、Recent API counter 语义和 Grafana Profile 历史隔离均已在 Raspberry Pi
live 环境关闭：

真实远程回滚演练已经完成：旧版 API 可启动，随后恢复最新 by-cycle 版本，非 API
容器未重启，Compose、`.env` 和数据目录基线保持不变。

最终完整 Acceptance Sprint 再次确认 Normal、三站 NOK、Skip、Trace、ACK、Profile 和
验收后状态恢复全部通过。Phase 1 阻塞项已全部关闭。

## 2. Scope and Evidence

### 2.1 读取的契约与报告

- `docs/contracts/ack_protocol.md`
- `docs/contracts/plc_identity_and_counter.md`
- `docs/contracts/data_gap_event.md`
- `docs/contracts/vplc_runtime_parameters.md`
- `docs/thread_handoff/verification.md`
- `docs/reports/reliability_sprint_report.md`
- `docs/reports/remote_reliability_deploy_report.md`
- `docs/reports/nok_simulation_improvement_report.md`
- `docs/reports/reliability_report.md`

### 2.2 本次新增验收资产

- `scripts/run_acceptance_sprint.py`
  - 正常三站 Trace 验证。
  - WS01、WS02、WS03 确定性 NOK 注入。
  - Raw PLC Payload、`quality_event`、`cycle_event` 和 Trace 交叉检查。
  - Profile、Collector、Grafana 和 PostgreSQL 只读证据采集。
  - NOK rate 和 pending queue 自动恢复。
- `tests/test_acceptance_sprint.py`
  - PostgreSQL array 结果归一化。
  - Raw mapping NOK 字段解析。
  - 按 `plc_boot_id + station_id + counter` 查找当前事件。
  - 跨 boot 样本查询先限制当前 boot 候选集，避免历史数据增长后全表配对超时。

### 2.3 原始执行证据

| 文件 | SHA-256 | 说明 |
| --- | --- | --- |
| `/tmp/edge_mes_acceptance_sprint.json` | `cc869e5ecc72856974fe4c1304037f9b82ffa6caae1a4d70cdd4a7586fad0b68` | 正常/NOK/Skip/Profile 验收 |
| `/tmp/edge_mes_acceptance_1h_final.json` | `3c6602b135793da7118904c9297127fd778be702383bcf714d1cb0b6718f8cac` | 103 分钟运行终点证据 |
| `/tmp/by_cycle_boot_isolation_final_acceptance.json` | `4054c522ca2eb182a40197bf4b15d12cdc157658b3d390f39200fdc5446f0a9d` | 最终跨 boot 同 counter 定向复验 |
| `/tmp/final_acceptance_sprint.json` | `2287f6fc9f227be60df5c0a20788b6fee2b2e5a4488244dbb1e91c623bc1e698` | 修复部署后的完整 Acceptance Sprint |
| `/tmp/rollback_drill_by_cycle.json` | `6e2ed26993ac08803ca6ef480b3c425a3aab457aec2a17caa6eef0078ec823de` | 回滚恢复后的跨 boot 定向复验 |
| `/tmp/rollback_drill_acceptance_sprint.json` | `8bc0ee822ec9f6fa9b362342ac4af646efb52fb11ca292ba9d948c29af3eab57` | 回滚恢复后的完整 Acceptance Sprint |
| `/tmp/final_phase1_by_cycle.json` | `fe2279542d78279e6476b2c3e086d7e70f38bd9a54c32e8091bd7bb31ae144b3` | 最终 Phase 1 跨 boot 定向复验 |
| `/tmp/final_phase1_acceptance_sprint.json` | `ce8b0bb6248a614642313fa6de84a0d1c9b418271883764ff02734891d329de4` | 最终 Phase 1 完整 Acceptance Sprint |
| `/tmp/final_phase1_post_sprint_snapshot.json` | `5e766bcdc2a2c50162c226e50de556faf9a2d16e072ed75f0a3273510adf5cd8` | 最终 Sprint 后完整性与恢复快照 |

`/tmp` 文件是本次执行环境中的原始证据；本报告保存可长期审计的关键结果。

## 3. Acceptance Matrix

状态定义：

- `PASS`：本次已执行并取得符合预期的直接证据。
- `PARTIAL`：核心项通过，但仍有未独立执行或证据不足的子项。
- `FAIL`：本次执行得到不符合要求的结果。
- `BLOCKED`：当前环境缺少执行条件。

| Layer | Test Item | Status | Evidence / Result |
| --- | --- | --- | --- |
| PLC | 当前 Profile、scale、ACK 模式 | PASS | `normal`、`1.0`、`require_ack=true` |
| PLC | 三站 counter 连续 | PASS | WS01 `1..200`、WS02 `1..199`、WS03 `1..198`，无缺号 |
| PLC | 三站约 30 秒 normal cycle | PASS | 平均约 `30.44/29.97/29.27s` |
| PLC | WS01/WS02/WS03 强制 NOK | PASS | `10001/20001/30001` 均在对应工站执行 |
| PLC | NOK Raw Payload | PASS | `result=2`、`nok_code_count=1`、`nok_codes_1` 正确 |
| Collector | 三站运行与 PLC 连接 | PASS | 三站均 `RUNNING / CONNECTED` |
| Collector | ACK 状态 | PASS | 当前 boot 非 `ACK_OK` 数量为 0 |
| Collector | NOK/Skip 持久化 | PASS | 三个 NOK 工件均产生正确 `cycle_event` |
| Collector | 长稳期间错误 | PASS | 当前 boot 启动后无持续错误；3 条连接错误发生于启动前窗口 |
| Database | counter 唯一与连续 | PASS | rows = unique counters = max counter |
| Database | 幂等键重复 | PASS | 重复键查询结果为空 |
| Database | UID 唯一与连续 | PASS | WS03 198 行、198 UID、serial `1..198` |
| Database | Quality Event | PASS | 三个 NOK 工站均有正确 code 和 `nok_source=PLC` |
| API | `/health` | PASS | `{"status":"ok"}` |
| API | UID Trace | PASS | 正常、NOK、Skip 三站 Trace 完整 |
| API | `/trace/api/by-cycle` | PASS | live 默认/显式当前/显式历史 boot 查询与三站 event scope 全部正确 |
| API | `/trace/api/recent` 字段语义 | PASS | live `cycle_counter = station_cycle_counter`，`route_step` 独立返回 |
| Grafana | `/api/health` | PASS | database `ok`，Grafana `13.0.2` |
| Grafana | Dashboard provisioning | PASS | Overview 与 Station Traceability 均可检索 |
| Grafana | Cycle/NOK/ACK 数据源一致 | PASS | Dashboard SQL 来源与本次 `cycle_event` 查询一致 |
| Grafana | Profile 历史数据隔离 | PASS | 默认 normal，12 条查询应用 Profile scope，宽窗明确显示 `MIXED` |
| Raspberry Pi | 连续运行至少 1 小时 | PASS | 同一 boot 连续 6,206 秒 |
| Raspberry Pi | PostgreSQL 可查询 | PASS | Grafana datasource 实际执行 PostgreSQL 查询成功 |
| Raspberry Pi | Collector / V-PLC / API / Grafana | PASS | 运行接口和数据库状态均持续更新 |
| Raspberry Pi | `docker compose ps` 本次独立复核 | PASS | SSH alias `edge-pi`：9 个服务运行，PostgreSQL healthy |
| Deployment | 备份、同步、API 重建、验证 | PASS | 备份存在、哈希一致、仅 API 重建、live OpenAPI/回归通过 |
| Deployment | 回滚 | PASS | 真实旧版回滚、API 恢复、哈希/容器/数据目录复核和完整回归均通过 |

## 4. Local Regression Baseline

### 4.1 V-PLC

```text
Ran 27 tests in 12.717s
OK
```

覆盖 Profile、参数审计、NOK FIFO、Skip、ACK、identity 和 UID 流程。

### 4.2 Collector

受限环境第一次执行时，真实 Snap7 测试因无法绑定本地端口而失败。切换到获准的本机
执行环境后：

```text
Ran 12 tests in 0.178s
OK
```

连接关闭阶段仍有一条 `Expected COTP DT, got 0x80` 日志，但断言和退出码正常。

### 4.3 Static

- Python compile：`PASS`
- Mapping validation：`PASS`
- Grafana JSON parse：`PASS`
- `git diff --check`：`PASS`

## 5. Normal Production Flow

测试工件：

```text
U-20260619-000092
```

| Station | Counter | Result | ACK | Trace |
| --- | ---: | --- | --- | --- |
| WS01 | 92 | OK | ACK_OK | 完整 |
| WS02 | 92 | OK | ACK_OK | 完整 |
| WS03 | 92 | OK | ACK_OK | 完整 |

验证结果：

- 三站使用同一 `unit_id`。
- 三站 counter 一致。
- 三站顺序为 WS01 → WS02 → WS03。
- 三站结果为 OK。
- 三站 ACK 为 `ACK_OK`。
- Trace 事件数量为 3。

状态：`PASS`

## 6. NOK Flow

### 6.1 WS01 NOK

工件：`U-20260619-000095`  
Counter：`95`  
NOK Code：`10001`

| Layer | Result |
| --- | --- |
| Raw Payload | `result=2`、`nok_code_count=1`、`nok_codes_1=10001` |
| Collector/DB | WS01 `NOK`，`defect_origin_station=WS01` |
| Quality Event | `result=NOK`、`nok_codes={10001}`、`nok_source=PLC` |
| Trace | WS01 NOK；WS02/WS03 SKIPPED；同一 UID |
| ACK | 三站 `ACK_OK` |

状态：`PASS`

### 6.2 WS02 NOK

工件：`U-20260619-000097`  
Counter：`97`  
NOK Code：`20001`

| Layer | Result |
| --- | --- |
| Raw Payload | `result=2`、`nok_code_count=1`、`nok_codes_1=20001` |
| Collector/DB | WS01 OK、WS02 NOK、WS03 SKIPPED |
| Quality Event | `result=NOK`、`nok_codes={20001}`、`nok_source=PLC` |
| Trace | 缺陷来源为 WS02，WS03 保留 `defect_code=20001` |
| ACK | 三站 `ACK_OK` |

状态：`PASS`

### 6.3 WS03 NOK

工件：`U-20260619-000098`  
Counter：`98`  
NOK Code：`30001`

| Layer | Result |
| --- | --- |
| Raw Payload | `result=2`、`nok_code_count=1`、`nok_codes_1=30001` |
| Collector/DB | WS01/WS02 OK、WS03 NOK |
| Quality Event | `result=NOK`、`nok_codes={30001}`、`nok_source=PLC` |
| Trace | 缺陷来源为 WS03，最终状态为 NOK |
| ACK | 三站 `ACK_OK` |

状态：`PASS`

## 7. Skip Flow

WS01 NOK 工件 `U-20260619-000095`：

| Station | Result | Process Status | Skip Reason | Defect Origin | Defect Code |
| --- | --- | --- | --- | --- | ---: |
| WS01 | NOK | PROCESSED | NONE | WS01 | 10001 |
| WS02 | SKIPPED | SKIPPED | UPSTREAM_NOK | WS01 | 10001 |
| WS03 | SKIPPED | SKIPPED | UPSTREAM_NOK | WS01 | 10001 |

附加断言：

- WS02/WS03 的 `nok_codes={30003}`，符合 `WS03_UPSTREAM_NOK` 跳站语义。
- 三站 UID 和 counter 一致。
- 三站均为 `ACK_OK`。
- Grafana Dashboard 使用的 `cycle_event` 数据源返回相同结果。
- 测试结束后三站 pending forced NOK queue 均为 0。

状态：`PASS`

## 8. Profile Validation

| Profile | Scale | Evidence | Status |
| --- | ---: | --- | --- |
| normal | 1.0 | 当前 V-PLC state、数据库 snapshot、Cycle Time | PASS |
| fast | 0.1 | 同日 `vplc_parameter_snapshot` 和 Reliability 部署记录 | PASS |
| test | 0.05 | 同日 `vplc_parameter_snapshot` 和 Reliability 部署记录 | PASS |

当前最终状态：

```text
profile=normal
scale=1.0
require_ack=true
WS01 base=30.4
WS02 base=29.8
WS03 base=29.2
```

当前 normal boot 的 Dashboard 数据源结果：

| Station | Rows | Average Cycle | Counter Range |
| --- | ---: | ---: | --- |
| WS01 | 99（场景验收采样时） | 30.44s | 1–99 |
| WS02 | 98 | 29.97s | 1–98 |
| WS03 | 98 | 29.27s | 1–98 |

Profile 显示、当前 cycle 和数据库/Grafana 查询结果一致。

状态：`PASS`

## 9. Raspberry Pi Continuous Run

观察窗口：

```text
Start: 2026-06-19 10:05:28 +08:00
End:   2026-06-19 11:48:55 +08:00
Duration: 6,206 seconds
```

终点状态：

| Item | Result |
| --- | --- |
| V-PLC | normal，运行中 |
| WS01 | counter 200 |
| WS02 | counter 199 |
| WS03 | counter 198 |
| Collector | 三站 RUNNING / CONNECTED |
| ACK timeout | 三站 FALSE |
| API | healthy |
| Grafana | database ok |
| Duplicate event key | 0 |
| Non-ACK_OK in current boot | 0 |
| WS03 UID | 198/198 唯一，serial 1–198 |

`collector_error_log` 最近两小时有 3 条 `PLC_CONNECTION_FAILED`：

```text
First: 2026-06-19 10:04:07 +08:00
Last:  2026-06-19 10:05:26 +08:00
Message: TCP connection failed: [Errno 111] Connection refused
```

它们发生在当前 normal boot 启动时间 `10:05:28` 之前，符合 Profile 切换/容器启动窗口；
当前 boot 运行期间未形成持续连接故障。

状态：`PASS`

## 10. Deployment Validation

### 10.1 已有一次成功部署证据

`remote_reliability_deploy_report.md` 记录：

- 部署前生成代码/配置备份：
  `/home/mari/edge-mes-backups/edge-mes-demo-20260619-095457.tar.gz`
- 发布包 SHA-256 本地与远程一致。
- `.env` 更新前后 SHA-256 一致。
- `data/`、PostgreSQL、Grafana 和 Prometheus 数据未被覆盖。
- 两个 migration 均 `COMMIT`。
- `s7-plc-sim` 与 `collector` 镜像重建成功。
- 更新后 9 个服务运行，PostgreSQL healthy。
- 最终恢复 normal Profile。

### 10.2 本次独立验证结果

| Step | Status | Notes |
| --- | --- | --- |
| 备份 | PASS | SSH 独立确认 by-cycle 部署备份目录及文件存在 |
| 同步 | PASS | 远程 `trace.py` 哈希与修复文件一致 |
| 重建 | PASS | API 镜像、容器启动时间和 Compose label 与部署报告一致 |
| 验证 | PASS | OpenAPI、真实跨 boot 回归和完整 Acceptance Sprint 通过 |
| 回滚 | PASS | 真实回退旧版 API 后恢复最新 by-cycle 版本，非 API 容器与数据目录基线不变 |

### 10.3 可重复性判断

当前已取得两次定向部署证据：Reliability 部署，以及本次仅 API 的 by-cycle 修复部署。
二者均包含备份、同步、定向重建和 post-deploy 验证；本次又完成了真实 rollback
drill。远程目录仍不是 Git 仓库，也没有仓库内统一 deploy/rollback 脚本。

状态：`PARTIAL`

## 11. Issues Found

### 11.1 严重问题

#### ACPT-H-01：按 Cycle 查询可能返回错误历史工件 — CLOSED

历史失败证据：

- 修复部署前，Raspberry Pi live OpenAPI 只有 `station_id`、`cycle_counter` 两个参数。
- 真实样本 `WS03 counter=541` 同时存在当前与历史 boot：
  - 当前：`U-20260619-000541`
  - 历史：`U-20260617-000541`
- 显式指定历史 boot 后，live API 仍返回当前工件。

最终复验：

- live OpenAPI 已包含 `plc_boot_id`、`plc_id`、`line_id`。
- 当前/历史 boot 共用 WS02 counter 617：
  - 默认查询返回当前 `U-20260619-000617`。
  - 显式当前 boot 返回当前工件。
  - 显式历史 boot 返回 `U-20260617-000617`。
  - 三站 events 均保持目标 boot scope。
- 完整 Acceptance Sprint 的三类 NOK by-cycle 断言通过。

当前状态：`PASS — fixed, deployed, live regression passed`

专项证据：

- [`by_cycle_boot_isolation_validation_report.md`](by_cycle_boot_isolation_validation_report.md)
- [`by_cycle_boot_isolation_remote_deploy_report.md`](by_cycle_boot_isolation_remote_deploy_report.md)
- [`final_acceptance_validation_report.md`](final_acceptance_validation_report.md)

### 11.2 中等问题

#### ACPT-M-01：Recent Trace 的 `cycle_counter` 字段语义错误 — CLOSED

最终 live 样本中：

- `cycle_counter` 与 `station_cycle_counter` 一致。
- `route_step=3` 使用独立字段返回。
- 同一 UID 的 Recent counter 与 WS01/WS02/WS03 Trace counter 一致。
- `plc_boot_id`、`plc_id`、`line_id` 均正常返回。

当前状态：`PASS — fixed, deployed, live regression passed`

#### ACPT-M-02：真实回滚已通过，统一可执行入口仍缺失

2026-06-19 已真实执行旧版 API 回滚、健康验证、最新版本恢复和完整回归，回滚能力状态
为 `PASS`。当前仍依赖人工文件复制与定向重建，自动化方面缺少：

- 可重复执行的 deploy 脚本。
- 发布 manifest。
- 自动备份校验。
- 自动 post-deploy 验证。

#### ACPT-M-03：Verification SSH 访问 — CLOSED

最终复验已通过 SSH alias `edge-pi` 独立获取：

- `docker compose ps`
- API 容器状态、镜像和 Compose labels
- API 日志
- 备份文件存在性
- `.env` / Compose 哈希
- 持久化数据目录状态

#### ACPT-M-04：Grafana 匿名访问可执行任意只读 SQL 查询

匿名 Viewer 可调用 `/api/ds/query`，PostgreSQL datasource 显示 `readOnly=false`。
本次验收使用该入口完成了数据库查询，因此已经证明局域网匿名访问者可以构造任意查询
读取业务表。未执行任何写入测试。

该配置适合封闭 Demo 调试，不适合直接暴露给客户网络或生产环境。

#### ACPT-M-05：Dashboard 宽时间窗口混合不同 Profile 数据 — CLOSED

最终 live Dashboard 已确认：

- Profile 默认值为 `normal`。
- 支持 `fast/test/unknown/All`。
- 12 条 `cycle_event` 查询应用 Profile scope。
- “当前 V-PLC Profile”与“时间窗 Profile 构成”面板已生效。
- 24 小时宽时间窗返回 `MIXED: fast, normal, test, unknown`，不再把混合数据伪装为
  单一工况。

当前状态：`PASS — fixed, deployed, live regression passed`

### 11.3 低优先级问题

#### ACPT-L-01：Snap7 测试关闭连接时有 COTP 清理日志

本地测试退出时出现：

```text
Expected COTP DT, got 0x80
```

测试断言和退出码正常，当前不影响功能。

#### ACPT-L-02：启动窗口产生 3 条短暂连接失败

当前 normal boot 启动前约 79 秒内有 3 条 `PLC_CONNECTION_FAILED`，随后自动恢复。
建议 Dashboard 区分启动期短暂错误与持续连接错误。

## 12. Recommended Fix Order

1. **补充统一 deploy/rollback 入口**
   - 固化发布 manifest、备份校验、定向重建和 post-deploy 验证。
2. **收紧 Demo 网络访问**
   - 评估关闭 Grafana anonymous、限制 datasource 权限或仅允许可信 LAN。
3. **优化低优先级日志**
   - 降低 Snap7 关闭连接日志噪音。
   - 对启动期 Collector 重连增加状态窗口解释。

## 13. Distance to “Customer Demonstrable”

### 当前已经具备

- 可演示三工站连续生产。
- 可演示约 30 秒真实口径 cycle。
- 可演示正常件 UID 三站贯通。
- 可演示 WS01、WS02、WS03 独立 NOK。
- 可演示上游 NOK 后下游 SKIPPED。
- 可演示 Raw Payload、数据库、Trace 和 Dashboard 一致。
- 可连续运行超过 1 小时，counter、UID 和 ACK 保持完整。

### 客户演示前 Phase 1 门禁

- Recent API counter 语义：已完成。
- Dashboard Profile 隔离与 `MIXED` 提示：已完成。
- by-cycle boot isolation：已完成。
- 真实 rollback 记录：已完成。
- 最终完整 Acceptance Sprint：已完成。

### 客户网络或生产试用前必须完成

1. 收紧 Grafana 匿名访问和 PostgreSQL datasource 权限。
2. 完成独立的 Compose、日志、资源和磁盘验收。
3. 完成部署自动化、版本标识、数据库备份和真实回滚演练。
4. 执行 24 小时或更长时间稳定性测试。

综合判断：

> Edge MES Demo Phase 1 验收结论为 `PASS`，具备受控环境下客户演示条件。该结论不等同
> 于生产交付认证；Grafana 网络权限、统一部署自动化、资源/磁盘专项验收和 24 小时以上
> 长稳测试仍属于后续生产化工作。
