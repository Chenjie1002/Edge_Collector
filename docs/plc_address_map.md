# Demo PLC S7 Address Map

> 本文件只记录当前 Demo 的旧 DB100 地址，不是通用 PLC 接入标准，也不应直接复制到实际设备。
>
> 实际生产环境请使用：
>
> - `docs/plc_edge_integration_guide.md`：通用 PLC/Edge 接入规范，覆盖 S7-300、S7-1200、S7-1500。
> - `docs/protocol.md`：当前项目已实现的 V-PLC 协议。
> - `config/mapping.yaml`：当前三工站 Demo 的实际 Edge mapping。

This demo exposes the simulated machine state through `DB100`.

| Field | S7 address | Type | Description |
| --- | --- | --- | --- |
| `running` | `DB100.DBX0.0` | Bool | Machine producing |
| `auto_mode` | `DB100.DBX0.1` | Bool | Auto mode enabled |
| `alarm_active` | `DB100.DBX0.2` | Bool | Alarm active |
| `cycle_counter` | `DB100.DBD4` | DInt | Completed cycles |
| `good_count` | `DB100.DBD8` | DInt | Good parts |
| `ng_count` | `DB100.DBD12` | DInt | NG parts |
| `total_count` | `DB100.DBD16` | DInt | Total parts |
| `cycle_time_ms` | `DB100.DBD20` | DInt | Last cycle time in ms |
| `alarm_code` | `DB100.DBW24` | Int | Alarm code |
| `stop_reason_code` | `DB100.DBW26` | Int | Stop reason code |
| `product_type_code` | `DB100.DBB28` | Byte | `1=TYPE_A`, `2=TYPE_B`, `3=TYPE_C` |
| `shift_code` | `DB100.DBB29` | Byte | `1=DAY`, `2=NIGHT` |
| `scenario_code` | `DB100.DBB30` | Byte | `0=normal`, `1=material_shortage`, `2=sensor_fault`, `3=changeover`, `4=maintenance`, `5=slow_cycle`, `6=fast_run` |
| `unix_time_seconds` | `DB100.DBD32` | DInt | PLC state timestamp |

The S7 simulator listens on TCP port `1102` so it can run without privileged
host access. Real Siemens PLCs usually use port `102`.
