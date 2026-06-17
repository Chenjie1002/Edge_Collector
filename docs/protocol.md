# 通讯协议、寄存器与数据格式

更新时间：2026-06-16

## 1. 通讯协议

当前 V-PLC 使用 `python-snap7` 的 Snap7 Server 模拟 Siemens S7 通讯。

| 项 | 当前值 |
| --- | --- |
| Host | `s7-plc-sim`，外部访问 `10.0.0.217` |
| Port | `1102` |
| Rack | `0` |
| Slot | `1` |
| Poll interval | Collector 默认 `500ms` 事件采集 |
| Mapping | `config/mapping.yaml` |

说明：

- 真实 S7 PLC 常用 102 端口；当前 Demo 使用 1102，避免权限和端口冲突。
- Collector 使用 Snap7 Client 读取 DB 块。
- V-PLC 使用 Snap7 Server 注册 DB100、DB101、DB102、DB103。
- `payload_ready` 和 `read_done` 用于基本握手。

## 2. DB 块职责

| DB | 作用 | 当前状态 |
| --- | --- | --- |
| DB100 | 线级状态 / legacy dashboard 兼容 | 旧快照链路仍使用，部分字段与新协议语义存在兼容冲突 |
| DB101 | WS01 Screw Station | 新三工站事件采集已使用 |
| DB102 | WS02 EOL Test Station | 新三工站事件采集已使用 |
| DB103 | WS03 Label / Final Station | 新三工站事件采集已使用 |

重要约束：

- `config/mapping.yaml` 定义了目标协议。
- `config/plc_mapping.yaml` 是旧 DB100 快照采集映射，暂时保留。
- 当前 DB100 兼容旧 dashboard，因此 `ignore_edge` 的新语义尚未完全切换到运行链路。

## 3. 工站公共 Header

DB101、DB102、DB103 共用同一套 header。

| 字段 | 地址模板 | 类型 | 说明 |
| --- | --- | --- | --- |
| `station_status` | `{db}.DBW0` | word | 工站状态 |
| `cycle_counter` | `{db}.DBD2` | dint | 工站 cycle 计数 |
| `payload_ready` | `{db}.DBX6.0` | bool | PLC 数据已准备好 |
| `read_done` | `{db}.DBX6.1` | bool | Edge 已读取并确认 |
| `ack_timeout` | `{db}.DBX6.2` | bool | ACK 超时标志 |
| `cycle_valid` | `{db}.DBX6.3` | bool | 当前 payload 是否有效 cycle |
| `plc_start_time` | `{db}.DBD8` | unix_time_seconds | PLC cycle 开始时间 |
| `plc_end_time` | `{db}.DBD12` | unix_time_seconds | PLC cycle 结束时间 |
| `result` | `{db}.DBW16` | word | 0 UNKNOWN, 1 OK, 2 NOK, 3 SKIPPED |
| `nok_code_count` | `{db}.DBW18` | word | NOK code 数量，最多 3 |
| `nok_codes[0]` | `{db}.DBW20` | word | NOK code 1 |
| `nok_codes[1]` | `{db}.DBW22` | word | NOK code 2 |
| `nok_codes[2]` | `{db}.DBW24` | word | NOK code 3 |
| `alarm_code` | `{db}.DBW26` | word | 工站报警码 |
| `downtime_type` | `{db}.DBW28` | word | 停机类型 |
| `pallet_id_numeric` | `{db}.DBD30` | dint | 当前用作 serial/pallet numeric |
| `station_dmc` | `{db}.DBB40` | string(40) | 工站 DMC / label |
| `unit_id` | `{db}.DBB200` | string(48) | 工件全局 UID，三站保持一致 |
| `route_step` | `{db}.DBW250` | word | 工艺路线步骤，WS01=1, WS02=2, WS03=3 |
| `route_state` | `{db}.DBW252` | word | 0 UNKNOWN, 1 NORMAL, 2 BYPASSING, 3 COMPLETED_OK, 4 COMPLETED_NOK |
| `process_status` | `{db}.DBW254` | word | 0 UNKNOWN, 1 PROCESSED, 2 SKIPPED |
| `skip_reason` | `{db}.DBW256` | word | 0 NONE, 1 UPSTREAM_NOK |
| `defect_origin_station` | `{db}.DBW258` | word | 0 UNKNOWN, 1 WS01, 2 WS02, 3 WS03 |
| `defect_code` | `{db}.DBW260` | word | 缺陷源站的数字 NOK code |
| `final_label_code` | `{db}.DBB262` | string(40) | 最终下线 ID，通常由 WS03 写入 |
| `reject_id` | `{db}.DBB304` | string(40) | 不合格品 ID，通常为 `NG-xxxxxx` |

## 4. 工站 Payload

### WS01 / DB101 / Screw Station

| 字段 | 地址 | 类型 |
| --- | --- | --- |
| `screw_1_torque_nm` | DB101.DBD100 | real |
| `screw_1_angle_deg` | DB101.DBD104 | real |
| `screw_2_torque_nm` | DB101.DBD108 | real |
| `screw_2_angle_deg` | DB101.DBD112 | real |
| `screw_3_torque_nm` | DB101.DBD116 | real |
| `screw_3_angle_deg` | DB101.DBD120 | real |

### WS02 / DB102 / EOL Test Station

| 字段 | 地址 | 类型 |
| --- | --- | --- |
| `avg_current_a` | DB102.DBD100 | real |
| `avg_voltage_v` | DB102.DBD104 | real |
| `clockwise_time_ms` | DB102.DBD108 | dint |
| `counterclockwise_time_ms` | DB102.DBD112 | dint |
| `stall_peak_current_a` | DB102.DBD116 | real |
| `stall_time_ms` | DB102.DBD120 | dint |
| `upstream_ws01_end_time` | DB102.DBD124 | unix_time_seconds |
| `upstream_ws01_result` | DB102.DBW128 | word |
| `upstream_child_dmc` | DB102.DBB130 | string[40] |

### WS03 / DB103 / Label Station

| 字段 | 地址 | 类型 |
| --- | --- | --- |
| `serial_no` | DB103.DBD100 | dint |
| `product_model_code` | DB103.DBW104 | word |
| `upstream_ws02_end_time` | DB103.DBD106 | unix_time_seconds |
| `upstream_ws02_result` | DB103.DBW110 | word |
| `upstream_child_dmc` | DB103.DBB112 | string[40] |
| `upstream_ws02_dmc` | DB103.DBB154 | string[40] |

## 5. Code Tables

### station_status

| Code | Text |
| --- | --- |
| 0 | UNKNOWN |
| 1 | IDLE |
| 2 | RUNNING |
| 3 | WAITING |
| 4 | BLOCKED |
| 5 | ALARM |
| 6 | OFFLINE |
| 7 | MANUAL_CONFIRM_REQUIRED |

### result

| Code | Text |
| --- | --- |
| 0 | UNKNOWN |
| 1 | OK |
| 2 | NOK |
| 3 | SKIPPED |

### NOK codes

| Range | 用途 |
| --- | --- |
| 10000-19999 | WS01 |
| 20000-29999 | WS02 |
| 30000-39999 | WS03 |
| 90000-99999 | Edge/System/Comm |

当前已定义：

| Code | Meaning |
| --- | --- |
| 10001 | WS01_TQ_LOW |
| 10002 | WS01_TQ_HIGH |
| 10003 | WS01_ANG_LOW |
| 10004 | WS01_ANG_HIGH |
| 20001 | WS02_CUR_HIGH |
| 20002 | WS02_VOLT_LOW |
| 20003 | WS02_VOLT_HIGH |
| 20004 | WS02_STALL_CUR_HIGH |
| 20005 | WS02_STALL_TIME_HIGH |
| 30001 | WS03_LABEL_PRINT_FAILED |
| 30002 | WS03_LABEL_VERIFY_FAILED |
| 30003 | WS03_UPSTREAM_NOK |
| 90001 | EDGE_READ_TIMEOUT |
| 90002 | EDGE_ACK_WRITE_FAILED |
| 90003 | PLC_COUNTER_RESET |

## 6. Handshake

当前事件采集逻辑：

1. V-PLC 完成一个工站 cycle。
2. 写入 header 与 payload。
3. 设置 `payload_ready = TRUE`、`cycle_valid = TRUE`。
4. Collector 轮询 DB。
5. Collector 解码并写入：
   - `raw_plc_sample`
   - `cycle_event`
   - `quality_event`
   - `collector_runtime_status`
6. Collector 写回 `{db}.DBX6.1 read_done = TRUE`。
7. Collector 将 `cycle_event.ack_status` 更新为 `ACK_OK`。
8. V-PLC 检测 `read_done` 后清除握手位。

当前 V-PLC 默认 `require_ack = false`，但是工站只要 `payload_ready = TRUE` 就不会启动下一件，避免未采集 payload 被覆盖。如果 Edge 未 ACK，V-PLC 约 10 秒后自动清除，以避免 demo 停死。后续真实 PLC 模式可以切换为强制 ACK。

## 7. 时间格式

- PLC DB 内时间当前使用 Unix seconds。
- Python API 和数据库使用 `Asia/Shanghai` 本地事件语义。
- PostgreSQL 字段类型使用 `TIMESTAMPTZ`。
- API 输出 ISO string。

## 8. 追溯规则

当前 Demo 追溯规则：

- 全局工件 UID：`U-20260616-000052`，从 WS01 创建并贯穿 WS02/WS03。
- WS01 子件 ID：`SUB-000052`
- WS02 继承并写入子件 ID：`SUB-000052`
- WS03 最终 ID：`ASM-000052`
- WS03 同时写入最终 ID 和上游子件 ID。
- 如果 WS01 NOK，WS02/WS03 仍接收该件，但 `process_status=SKIPPED`、`skip_reason=UPSTREAM_NOK`，WS03 生成 `NG-xxxxxx` 并进入不合格品流程。
- API 优先通过 `unit_id` 串联三站；`child_dmc`、`label_code`、`reject_id`、尾部序号仅作为输入解析入口。

约束：

- 当前 V-PLC 内部使用 WIP 队列保证工站流转关系。
- `cycle_event` 保留旧 dashboard/API 兼容字段，同时新增 `unit_id`、`route_state`、`process_status` 等字段。
- `station_event` 是按工站追加的履历表。
- `production_unit` 是工件当前状态表。
- 旧数据缺 `unit_id` 时，API 才允许使用 DMC/时间兜底。
