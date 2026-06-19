# 通讯协议、寄存器与数据格式

更新时间：2026-06-19

> 本文件描述当前 Edge MES Demo 已实现的协议和地址。
>
> 面向实际设备、不同工艺和 S7-300/S7-1200/S7-1500 的通用接入要求，请阅读 `docs/plc_edge_integration_guide.md`。实际设备不得把本文件中的 DB101/DB102/DB103 Payload 当成固定行业标准。

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
- V-PLC 使用 Snap7 Server 注册 DB100、DB101、DB102、DB103、DB104。
- `payload_ready`、`read_done` 和 `ack_timeout` 使用严格 ACK 状态机。

## 2. DB 块职责

| DB | 作用 | 当前状态 |
| --- | --- | --- |
| DB100 | 线级状态 / legacy dashboard 兼容 | 旧快照链路仍使用，部分字段与新协议语义存在兼容冲突 |
| DB101 | WS01 Screw Station | 新三工站事件采集已使用 |
| DB102 | WS02 EOL Test Station | 新三工站事件采集已使用 |
| DB103 | WS03 Label / Final Station | 新三工站事件采集已使用 |
| DB104 | 线级 runtime / PLC identity | Collector 读取 boot identity、heartbeat 和 restart counter |

重要约束：

- `config/mapping.yaml` 定义了目标协议。
- `config/plc_mapping.yaml` 是旧 DB100 快照采集映射，暂时保留。
- DB100 继续兼容旧 dashboard，不承载新 identity。
- `config/mapping.yaml` 的 line read plan 固定读取 DB104。

### 2.1 DB104 线级 Runtime

| 字段 | 地址 | 类型 | 说明 |
| --- | --- | --- | --- |
| `protocol_version` | `DB104.DBW0` | word | 当前固定为 1 |
| `heartbeat_counter` | `DB104.DBD4` | dint | V-PLC 主循环递增 |
| `plc_restart_counter` | `DB104.DBD8` | dint | 冷启动或手动 counter reset 时递增并持久化 |
| `plc_boot_id` | `DB104.DBB12` | string[36] | 当前运行实例 UUID；运行期间稳定 |
| `ignore_edge` | `DB104.DBX52.3` | bool | Data Quality Thread 使用 |

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
8. V-PLC 检测 `read_done` 后清除 `payload_ready`、`read_done`、`ack_timeout` 和
   `cycle_valid`，随后才允许下一件。

当前 V-PLC 默认严格 ACK。ACK deadline 默认为 10 秒，通过
`VPLC_ACK_DEADLINE_SECONDS` 调整。超时后只设置 `ack_timeout=TRUE`，不会自动清除
或覆盖 payload。Collector 每轮都按
`plc_id + station_id + plc_boot_id + cycle_counter` 幂等落库，因此 ACK 写回失败或
Collector 重启后可继续补 ACK。

`cycle_event.ack_status` 只允许：

- `PENDING`
- `ACK_OK`
- `ACK_WRITE_FAILED`

ACK 写回失败会增加 `retry_count`；连接、identity、读取/解码、存储、ACK 写回和
counter reset 错误写入 `collector_error_log`。

## 7. 时间格式

- PLC DB 内时间当前使用 Unix seconds。
- Python API 和数据库使用 `Asia/Shanghai` 本地事件语义。
- PostgreSQL 字段类型使用 `TIMESTAMPTZ`。
- API 输出 ISO string。

## 8. V-PLC Runtime Parameters

参数与 Profile 契约见
[`contracts/vplc_runtime_parameters.md`](contracts/vplc_runtime_parameters.md)。

当前参数解析顺序：

```text
built-in safe defaults
  → config/vplc.yaml
  → VPLC_PROFILE / VPLC_CYCLE_SCALE
  → profile 允许的 runtime update
```

`normal` profile 固定 `scale=1.0`，三站 base 必须在 20–60 秒，runtime API
不可修改 base/jitter。`fast/test` 保留 process baseline，只通过 scale 加速。

参数修改接口：

```text
POST /vplc/stations/{station_id}
```

请求必须包含 `reason`。服务端记录 actor、client IP、request ID、old/new、
profile、accepted 和 rejection reason。

审计查询：

```text
GET /vplc/audit/changes
GET /vplc/audit/snapshots
```

查询优先读取 PostgreSQL 持久历史，数据库不可用时回退到当前进程内最近记录。

数据库表：

- `vplc_parameter_change_log`
- `vplc_parameter_snapshot`

强制 NOK：

```text
POST   /vplc/stations/{station_id}/force-nok
DELETE /vplc/stations/{station_id}/force-nok?reason=...
```

POST 支持 `nok_code`、`count=1..100` 和 `reason`。NOK code 必须属于目标工站。
队列只在目标工站实际加工 cycle 时消费；上游 NOK 形成的下游 SKIPPED 不消费队列。

## 9. 追溯规则

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

## 10. 未来文件接口约定

### 10.1 MCU 高频采集文件

高频采集由 MCU 或专用采集器完成，Edge 不直接采样高频信号。

约定：

- 文件格式：CSV 或 JSON。
- 文件粒度：每个零件一个文件。
- 推荐关联字段：
  - `unit_id`
  - `station_id`
  - `dmc`
  - `sample_start_time`
  - `sample_end_time`
  - `mcu_id`
  - `sampling_rate_hz`
- Edge 保存原始文件路径、校验值、解析状态和特征提取结果。
- 原始文件不直接写入 PostgreSQL 二进制字段。

### 10.2 工业相机媒体文件

图片/视频来源为工业相机。

约定：

- 推荐关联字段：
  - `unit_id`
  - `station_id`
  - `camera_id`
  - `capture_time`
  - `inspection_result`
  - `file_type`
  - `file_checksum`
- 本地默认保留 7 天，可配置。
- 超期后根据归档策略上传服务器、复制到移动硬盘或删除。
- PostgreSQL 只保存元数据和索引，不保存大型媒体二进制。

### 10.3 参数变更通知

参数由 PLC/HMI 或受控工程工具修改，Edge 不主动回写 PLC。

约定：

- PLC 侧参数修改后通知 Edge。
- Edge 收到通知后读取最新参数。
- Edge 对参数值进行范围、类型、枚举和版本校验。
- 参数 changelog 必须记录旧值、新值、账号、认证方式、修改来源、读取时间、校验结果。
