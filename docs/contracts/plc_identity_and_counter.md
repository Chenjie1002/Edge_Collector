# PLC Identity and Counter Contract

更新时间：2026-06-19  
适用范围：当前单机、单 PLC、三工站 V-PLC Demo。

## 1. 目的

稳定定义 PLC 运行实例和工站事件 counter，使重启、清零、回绕和重复采集不会
覆盖历史事件。

## 2. 当前问题

- V-PLC 已生成启动 UUID，但当前主循环没有把它写入可读取 DB。
- `config/mapping.yaml` 把 `plc_boot_id` 放在 DB100，而 DB100 同时承担 legacy
  dashboard 数据，现有地址存在兼容冲突风险。
- Collector 读取失败时使用 Collector 会话 UUID 兜底。Collector 每次重启会产生
  新值，因此它不能代表 PLC identity。
- `cycle_counter` 由各工站独立维护，当前没有 reset/回绕检测。

## 3. Phase-1 Demo 决策

为避免破坏 DB100 legacy 链路，单机 Demo 新增专用线级运行身份 DB：

```text
DB104 = Edge line runtime / identity
```

DB104 最小字段：

| 字段 | 推荐地址 | 类型 | 规则 |
| --- | --- | --- | --- |
| `protocol_version` | `DB104.DBW0` | WORD | 当前固定为 1 |
| `heartbeat_counter` | `DB104.DBD4` | DINT | V-PLC 运行时递增 |
| `plc_restart_counter` | `DB104.DBD8` | DINT | 每次 V-PLC 冷启动递增；Demo 可持久化到本地 volume |
| `plc_boot_id` | `DB104.DBB12` | STRING[36] | 每次启动生成，运行期间不变 |
| `ignore_edge` | `DB104.DBX52.3` | BOOL | Data Quality Thread 使用 |

DB100 保持旧快照用途，不在本阶段塞入新的 identity 字段。

## 4. Identity 规则

- `plc_id`：配置身份，当前为 `PLC_001`，跨重启不变。
- `plc_boot_id`：运行实例身份，每次 V-PLC 进程启动变化，运行期间不变。
- `plc_restart_counter`：辅助诊断字段，不替代 `plc_boot_id`。
- Collector 不得使用自身会话 ID 作为正常幂等身份。
- Collector 读取不到有效 `plc_boot_id` 时：
  - 不 ACK 新 payload。
  - 更新 runtime status 为 identity invalid。
  - 写入 `collector_error_log`。

## 5. Counter 规则

- WS01、WS02、WS03 各自维护独立 `cycle_counter`。
- 每发布一个有效 OK、NOK 或 SKIPPED 事件，counter 增加 1。
- IDLE、RUNNING 或状态刷新不增加 counter。
- 同一个 `plc_boot_id` 内，counter 必须单调递增。
- 新 `plc_boot_id` 允许 counter 从 0 或 1 重新开始。
- 手动 reset 必须形成新的 `plc_boot_id`，不能在同一 boot identity 下静默清零。

## 6. Reset、回绕和异常

| 情况 | 判定 | 处理 |
| --- | --- | --- |
| 正常下一件 | 同 boot，counter 增加 | 正常采集 |
| 重复 payload | 同 boot，counter 相同 | 幂等更新并补 ACK |
| counter 跳跃 | 同 boot，counter 增加超过 1 | 交给 data gap 规则记录 |
| counter reset | 同 boot，counter 变小 | 记录 `PLC_COUNTER_RESET`，停止 ACK，等待新 boot identity |
| PLC 重启 | boot ID 变化 | 建立新事件分区，counter 可重新开始 |
| counter 回绕 | 同 boot，到达定义上限后回到 0 | 本 Demo 不主动制造；若发生按 reset 异常处理 |

## 7. 持久化与幂等

事件唯一键保持：

```text
plc_id + station_id + plc_boot_id + cycle_counter
```

`unit_id` 是工件追溯身份，不代替 PLC event identity。`unit_id` 重复属于业务数据
错误，应由 Verification 单独报告。

## 8. Thread 边界

- Reliability Thread：注册 DB104、写入 identity、修改 mapping 和 Collector 校验。
- Data Quality Thread：使用稳定 boot/counter 判断缺口，不自行定义 reset 语义。
- Verification Thread：验证 PLC 重启、Collector 重启、手动 reset、counter 跳跃和重复 payload。
- Oracle / `sync-worker` 不参与 identity 或幂等验收，属于 Phase-2 Out of Scope。

## 9. 验收条件

- V-PLC 启动后 DB104 可读到非空、稳定的 `plc_boot_id`。
- V-PLC 重启后 boot ID 变化。
- Collector 重启不改变事件的 PLC boot identity。
- 同一事件重复采集不增加 cycle_event 行数。
- 同 boot counter 下降会被阻止并记录。

## 10. Trace by-cycle 查询规则

`GET /trace/api/by-cycle` 不得只使用 `station_id + cycle_counter` 查询。counter 在新的
PLC boot 中允许从 0 或 1 重新开始，因此不包含 boot identity 的查询会跨启动周期返回
旧工件。

查询规则：

1. 完整事件隔离键保持：

   ```text
   plc_id + station_id + plc_boot_id + cycle_counter
   ```

2. `line_id` 已存在于当前事件模型中，API 查询时同时用于收窄当前单线范围，但不替代
   `plc_id` 或 `plc_boot_id`。
3. 调用方显式提供 `plc_boot_id` 时，必须只返回该 boot 下的事件；可选
   `plc_id` / `line_id` 用于进一步限定。
4. 调用方未提供 `plc_boot_id` 时，API 必须从 `collector_runtime_status` 推导指定工站
   当前的 `plc_id + line_id + plc_boot_id`，再按完整 identity 查询。
5. 当前 boot identity 不存在或目标 cycle 不存在时返回 404，不得回退到历史 boot。
6. 找到 seed cycle 后，按 `unit_id` 或 legacy serial 补齐三站 Trace 时仍必须保持相同
   `plc_id + line_id + plc_boot_id` 范围，不能在补齐阶段重新混入旧 boot。

现有唯一约束：

```text
UNIQUE (plc_id, station_id, plc_boot_id, cycle_counter)
```

已覆盖核心精确查询，不要求为本次修复修改 schema。

## 11. Trace recent 字段语义

`GET /trace/api/recent` 返回工件摘要时，必须区分工艺路线步骤和 PLC 工站 cycle counter。

字段定义：

| 字段 | 语义 |
| --- | --- |
| `station_cycle_counter` | 该工件最新工站事件的真实 `cycle_event.cycle_counter` |
| `route_step` | 该工件当前/最新工艺路线步骤，当前 Demo 为 WS01=1、WS02=2、WS03=3 |
| `cycle_counter` | 兼容字段，值必须等于 `station_cycle_counter`；不得再表示 route step |
| `station_id` | `station_cycle_counter` 所属的工站 |
| `plc_boot_id` | `station_cycle_counter` 所属事件的 PLC boot identity |

规则：

1. `production_unit.current_route_step` 只能映射为 `route_step`，不得别名为
   `cycle_counter`。
2. Recent API 应从该 `unit_id` 最新的真实 `cycle_event` 获取
   `station_cycle_counter`、`station_id` 和 `plc_boot_id`。
3. 为兼容现有调用方，保留 `cycle_counter` 字段，但其值修正为真实
   `station_cycle_counter`。
4. 没有可关联 cycle event 的 legacy/incomplete 工件返回
   `station_cycle_counter=null`、`cycle_counter=null`，不得用 route step 填充。
