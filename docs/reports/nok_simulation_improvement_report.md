# NOK Simulation Improvement Report

日期：2026-06-19  
状态：`PASS`

> 本报告是 Reliability Sprint 的 NOK 专项验收说明，记录工站逻辑、Payload、Trace、
> Dashboard 和 Verification 影响。`reliability_sprint_report.md` 只保留 P3 阶段摘要
> 与本报告链接，避免重复维护同一份细节。

## 1. 当前结论

NOK 模拟升级已经实现并完成本机回归与 Raspberry Pi 基础运行验证。

- 每个工站拥有独立 NOK Rate、独立随机数生成器和独立强制 NOK FIFO 队列。
- 强制 NOK 支持一次排队 `1..100` 个相同 code。
- NOK Code 按工站白名单校验，跨工站 code 会被拒绝并进入参数审计。
- 上游 NOK 导致的下游 `SKIPPED` 不消费下游强制 NOK 队列。
- 队列状态可查询、可清除，增加与清除操作均进入参数审计和参数快照。
- NOK 结果、code、缺陷来源和追溯标识沿现有 PLC Payload、Collector、数据库、
  Trace API 和 Grafana 链路传递。

## 2. 修改文件列表

### 直接实现

- `s7_plc_sim/app/pipeline.py`
  - 增加工站 NOK Code 白名单。
  - 将单次 `force_next_nok_code` 升级为 FIFO `forced_nok_queue`。
  - 增加 count、clear、pending 状态和独立 station RNG。
  - 保持上游 NOK、下游 SKIPPED 和缺陷来源传播逻辑。
- `s7_plc_sim/app/control_api.py`
  - `force-nok` 增加 `count` 和必填 `reason`。
  - 增加清除强制 NOK 队列接口。
  - 控制页显示 pending 数量并支持批量排队和清除。
- `s7_plc_sim/tests/test_nok_simulation.py`
  - 新增 NOK 队列、白名单、SKIPPED、清除和 API 审计测试。

### 配置与协议

- `config/vplc.yaml`
  - 定义 WS01、WS02、WS03 独立 NOK Rate 基线。
- `docs/contracts/vplc_runtime_parameters.md`
  - 冻结 NOK 队列、白名单、查询、清除和 SKIPPED 不消费规则。
- `docs/protocol.md`
  - 记录 NOK Code、Payload 字段和强制 NOK API。
- `docs/current_status.md`
  - 更新当前 NOK 模拟能力。
- `README.md`
  - 增加 V-PLC 控制入口和参数契约入口。
- `docs/reports/reliability_sprint_report.md`
  - 保留 P3 汇总和专项报告链接。

本次收尾未修改 API、Collector、Grafana Dashboard JSON 或其他业务逻辑。

## 3. NOK Code

本次升级未扩展新的协议编号；新增的是以下 code 的可执行工站白名单和批量强制注入
能力。

| Station | 可随机/强制产生的 NOK Code | 含义 |
| --- | --- | --- |
| WS01 | `10001` | `WS01_TQ_LOW` |
| WS01 | `10002` | `WS01_TQ_HIGH` |
| WS01 | `10003` | `WS01_ANG_LOW` |
| WS01 | `10004` | `WS01_ANG_HIGH` |
| WS02 | `20001` | `WS02_CUR_HIGH` |
| WS02 | `20002` | `WS02_VOLT_LOW` |
| WS02 | `20003` | `WS02_VOLT_HIGH` |
| WS02 | `20004` | `WS02_STALL_CUR_HIGH` |
| WS02 | `20005` | `WS02_STALL_TIME_HIGH` |
| WS03 | `30001` | `WS03_LABEL_PRINT_FAILED` |
| WS03 | `30002` | `WS03_LABEL_VERIFY_FAILED` |

`30003 WS03_UPSTREAM_NOK` 是下游跳站语义 code：当 WS01 或 WS02 已产生 NOK 时，
后续工站返回 `result=SKIPPED`、`process_status=SKIPPED` 和
`skip_reason=UPSTREAM_NOK`。它不属于 WS03 强制 NOK 白名单，控制页也不提供该选项。

## 4. WS01 NOK 逻辑

- 随机模式按 WS01 独立 `nok_rate` 判断，命中后从 `10001..10004` 中选择一个 code。
- 强制模式优先于随机模式，每个实际加工 cycle 从 WS01 FIFO 队列消费一个 code。
- WS01 NOK 后：
  - `result=NOK`。
  - `process_status=PROCESSED`。
  - `defect_origin_station=WS01`。
  - `defect_code` 为本次 WS01 NOK Code。
  - 工件进入 `ROUTE_BYPASSING`，继续流向 WS02、WS03。
- WS02、WS03 对该件写入 SKIPPED，不消费它们各自的强制 NOK 队列。

## 5. WS02 NOK 逻辑

- 仅当工件没有因 WS01 NOK 进入 bypass 状态时，WS02 才执行实际 NOK 判定。
- 随机模式按 WS02 独立 `nok_rate` 判断，命中后从 `20001..20005` 中选择一个 code。
- 强制模式从 WS02 FIFO 队列消费一个 code，并优先于随机模式。
- WS02 NOK 后：
  - `result=NOK`。
  - `process_status=PROCESSED`。
  - `defect_origin_station=WS02`。
  - `defect_code` 为本次 WS02 NOK Code。
  - 工件进入 `ROUTE_BYPASSING`。
- WS03 对该件写入 SKIPPED，并保留 WS02 缺陷来源。

## 6. WS03 NOK 逻辑

- 仅当工件没有上游 NOK 时，WS03 才执行实际 NOK 判定。
- 随机模式按 WS03 独立 `nok_rate` 判断，命中后从 `30001/30002` 中选择一个 code。
- 强制模式从 WS03 FIFO 队列消费一个 code，并优先于随机模式。
- WS03 NOK 后：
  - `result=NOK`。
  - `process_status=PROCESSED`。
  - `route_state=COMPLETED_NOK`。
  - `defect_origin_station=WS03`。
  - `defect_code` 为本次 WS03 NOK Code。
  - 生成 `NG-xxxxxx` reject ID。
- 上游已 NOK 的工件在 WS03 返回 SKIPPED，同样进入最终不合格品处理，但不消费 WS03
  强制 NOK 队列。

## 7. 工站独立 NOK Rate

当前受控基线：

| Station | NOK Rate |
| --- | ---: |
| WS01 | `0.020` |
| WS02 | `0.015` |
| WS03 | `0.010` |

- 三站各自保存 `nok_rate`，范围限制为 `0..1`。
- 三站使用独立 `random.Random` 实例，减少一个工站的随机调用对其他工站结果序列的
  耦合。
- `normal` Profile 允许修改 NOK Rate，但要求非空 `reason` 并写入参数审计。
- 强制 NOK 队列优先于随机 NOK；队列为空后才恢复按该站 NOK Rate 随机判定。

## 8. Payload 与 NOK Code 对应关系

工站 DB101/DB102/DB103 公共 Header：

| 字段 | 地址 | NOK 行为 |
| --- | --- | --- |
| `result` | `{db}.DBW16` | `2=NOK`，`3=SKIPPED` |
| `nok_code_count` | `{db}.DBW18` | 当前模拟写入 0 或 1，协议最多支持 3 |
| `nok_codes[0]` | `{db}.DBW20` | 当前 NOK 或 SKIPPED code |
| `nok_codes[1]` | `{db}.DBW22` | 当前实现通常为 0 |
| `nok_codes[2]` | `{db}.DBW24` | 当前实现通常为 0 |
| `route_state` | `{db}.DBW252` | bypass 或最终 OK/NOK 状态 |
| `process_status` | `{db}.DBW254` | `PROCESSED` 或 `SKIPPED` |
| `skip_reason` | `{db}.DBW256` | 上游 NOK 时为 `UPSTREAM_NOK` |
| `defect_origin_station` | `{db}.DBW258` | 首个实际 NOK 来源工站 |
| `defect_code` | `{db}.DBW260` | 首个实际 NOK Code |
| `reject_id` | `{db}.DBB304` | 最终不合格件为 `NG-xxxxxx` |

Collector 将 `result`、`nok_codes`、`defect_origin_station`、`defect_code` 和追溯字段
写入 `cycle_event`，并派生 `station_event`、`production_unit` 和 `quality_event`。

## 9. 测试结果

本次收尾于 2026-06-19 重新执行：

| 检查 | 结果 |
| --- | --- |
| NOK 专项测试 | `PASS`，5/5 |
| V-PLC 全量测试 | `PASS`，27/27 |
| Collector 单元/集成测试 | `PASS`，12/12 |
| 真实本地 Snap7 Server/Client ACK | `PASS` |
| mapping 校验 | `PASS` |

NOK 专项覆盖：

1. `count=3` 按 FIFO 连续产生三个 NOK，随后恢复 OK。
2. WS01 拒绝 WS02 code，队列不发生变化。
3. 上游 bypass 导致的下游 SKIPPED 不消费 WS02 pending 队列。
4. 清除 WS03 pending 队列后 count 和 code 列表归零。
5. API 支持 count、clear，并记录 `forced_nok_queue` 参数审计。

Collector 测试首次在受限沙箱中因无法绑定本地临时端口而有 1 项环境错误；在获准的
本机执行环境重跑后 12/12 通过。Snap7 连接关闭阶段仍出现一条
`Expected COTP DT, got 0x80` 日志，不影响断言和退出码。

远程 Raspberry Pi 已分别验证：

| Station | Code | 数据库结果 |
| --- | ---: | --- |
| WS01 | `10001` | `cycle_event.result=NOK` |
| WS02 | `20001` | `cycle_event.result=NOK` |
| WS03 | `30001` | `cycle_event.result=NOK` |

三个 pending 队列验证后均归零。

## 10. 对 Trace 的影响

- `unit_id` 不因随机或强制 NOK 改变，同一工件仍可串联 WS01、WS02、WS03。
- Trace API 已返回 `result`、`nok_codes`、`process_status`、`skip_reason`、
  `defect_origin_station`、`defect_code` 和 `reject_id`。
- WS01/WS02 NOK 后，下游事件显示 SKIPPED，同时保留最初缺陷来源和 code。
- WS03 NOK 或上游 NOK 最终都会生成不合格品状态和 reject ID。
- NOK 队列本身是模拟控制状态，不写入单件 Trace；实际消费后产生的 cycle 才进入
  Trace。队列增加、拒绝和清除由参数审计链路记录。

## 11. 对 Dashboard 的影响

- 本次未修改 Grafana Dashboard JSON。
- 现有三工站追溯 Dashboard 已直接查询 `cycle_event.result` 和 `nok_codes`，因此新
  产生的 NOK 会自动进入：
  - NOK 事件数。
  - OK/NOK by Station。
  - NOK Code 分布。
  - 最近 cycle 明细。
- WS03 合格率会因最终 NOK/SKIPPED 事件按现有查询口径变化。
- 批量强制 NOK 会明显改变选定时间窗口内的 NOK 数和良率，这是预期的模拟效果。
- Dashboard 不展示 pending 强制 NOK 队列；该状态当前只在 V-PLC 控制页和
  `/vplc/state` 中查看。

## 12. 对 Verification Team 的建议

1. 每个工站至少验证一个随机 NOK 和一个强制 NOK。
2. 对每个白名单 code 验证 `result`、`nok_codes[0]`、`defect_origin_station` 和
   `defect_code`。
3. 对跨工站 code 验证 HTTP 400、队列不变及 `accepted=false` 审计记录。
4. 排队多个 NOK 后验证 FIFO 消费、pending count 递减和清除接口。
5. 先在 WS01/WS02 制造 NOK，再确认下游 SKIPPED 不消费下游 pending 队列。
6. 以同一 `unit_id` 核对 PLC Payload、`cycle_event`、Trace API 和 Grafana 展示。
7. 验证 NOK 场景不破坏严格 ACK、幂等键、cycle counter 和 Collector 重启补 ACK。
8. 测试结束后清空 pending 队列并恢复三站 NOK Rate，避免污染后续 Cycle Time 或
   稳定性验收。

## 13. 遗留项

- 尚无覆盖所有 11 个可强制 NOK Code 的自动化参数化测试。
- 尚无专门展示 pending NOK 队列和参数审计的 Grafana 面板。
- 远程故障恢复矩阵和长时间稳定性验收属于 Reliability 收尾遗留，不影响 NOK 升级
  当前基础验收结果。
