# Line Configuration Contract

更新时间：2026-06-19  
状态：下一阶段架构合同，尚未实施  
适用范围：非侵入式 Edge MES Demo 的 1~N 工站、Buffer、多 PLC 与未来多产线配置

## 1. 目的与控制边界

本合同定义产线拓扑、PLC 连接、工站、Buffer、DB mapping、payload template、NOK
template 和节拍配置的统一表达方式。

本合同不授权 Edge 改变 PLC 控制逻辑：

- PLC 仍负责设备动作、互锁、安全、放行、Hold、Rework、Skip/Bypass 决策。
- Edge 只读取 PLC/HMI 已定义的状态与事件，完成采集、存储、追溯、OEE 和展示。
- V-PLC 可按本合同模拟流转，但模拟行为不得被解释为真实项目中的 Edge 控制能力。

## 2. 配置格式决策

采用组合方案，但只有一个运行时真源：

| 格式 | 用途 | 是否为运行时真源 |
| --- | --- | --- |
| YAML | 人工维护的产线、PLC、工站、Buffer、模板引用和 feature flag | 是 |
| JSON Schema | 校验 YAML 解析后的对象结构、类型、枚举、唯一性和容量限制 | 否 |
| JSON | API 返回、resolved config、配置快照、hash 计算和审计 | 否 |
| CSV | 工站清单、DB 字段清单的批量导入/导出和现场评审 | 否 |

禁止同时维护语义等价的 YAML 和 JSON 配置。CSV 必须先转换为 YAML 草稿并通过
Schema 校验后才能进入运行配置。

推荐文件布局：

```text
config/
  lines/
    LINE_001.yaml
    LINE_002.yaml
  templates/
    station/
      screw_station.yaml
      eol_test_station.yaml
      label_station.yaml
    payload/
      common_header_v1.yaml
      screw_payload_v1.yaml
      eol_payload_v1.yaml
      label_payload_v1.yaml
    nok/
      screw_nok_v1.yaml
      eol_nok_v1.yaml
      label_nok_v1.yaml
    buffer/
      fifo_buffer_v1.yaml
  schema/
    line_config.schema.json
```

## 3. 顶层配置模型

每个产线文件至少包含：

```yaml
schema_version: 1
line_id: LINE_001
name: Demo Assembly Line
enabled: true
timezone: Asia/Shanghai

plcs:
  - plc_id: PLC_001
    protocol: s7
    host: s7-plc-sim
    port: 1102
    rack: 0
    slot: 1
    runtime_db: 104
    max_stations: 20
    max_db_mappings_per_station: 4

stations:
  - station_id: WS01
    station_order: 10
    station_type: SCREW
    plc_id: PLC_001
    enabled: true
    mapping_refs: [WS01_MAIN]
    payload_template: screw_payload_v1
    nok_template: screw_nok_v1
    cycle_profile: normal_screw

buffers:
  - buffer_id: BUF_WS01_WS02
    from_station_id: WS01
    to_station_id: WS02
    buffer_position: 15
    buffer_type: FIFO
    capacity: 1

features:
  manual_nok_simulation: true
  hold_simulation: false
  rework_simulation: false
```

## 4. 标识与排序规则

- `line_id`：Edge 节点内稳定唯一，例如 `LINE_001`。
- `plc_id`：Edge 节点内稳定唯一，一个 PLC 可服务多个工站。
- `station_id`：在 `line_id` 内唯一，默认示例使用 `WS01`~`WS20`，但不限制显示名。
- `station_order`：正整数，决定默认路线和 UI 排序；推荐使用 10、20、30，便于插站。
- `buffer_id`：在 `line_id` 内唯一。
- 数据库和 API 中引用工站时必须同时带 `line_id`；跨 PLC 事件还必须带 `plc_id`。
- 禁止仅依赖 `WS01` 作为全局唯一键。

## 5. 工站模型

每个工站至少包含：

| 字段 | 规则 |
| --- | --- |
| `station_id` | 产线内唯一 |
| `station_order` | 产线内唯一且大于 0 |
| `station_type` | 稳定枚举或受控字符串 |
| `plc_id` | 必须引用本产线已声明 PLC |
| `mapping_refs` | 1~4 个 mapping；当前 Demo 默认 1 个 |
| `payload_template` | 引用版本化 payload 模板 |
| `nok_template` | 引用版本化 NOK code 模板 |
| `cycle_profile` | 引用节拍基线 |
| `enabled` | 禁用工站不启动采集，但不得删除历史数据 |

`station_type` 表达行为类别，不承担实例身份。两个同类型工站仍使用不同
`station_id`。

推荐第一批类型：

```text
GENERIC, ASSEMBLY, SCREW, PRESS, TEST, VISION, LABEL, PACK, MANUAL
```

## 6. PLC、DB 与硬件容量限制

Phase-2 不把“20 个工站”写成所有现场的硬件承诺。配置必须同时表达软件保护上限和
本次部署验证上限：

| 层级 | 工站规模 | 用途 |
| --- | ---: | --- |
| 默认 Demo | 3 | WS01~WS03，保持 Phase-1 行为 |
| 中等线验证 | 10 | WS01~WS10，验证动态配置与常规负载 |
| 较高负载验证 | 20 | WS01~WS20，验证边缘硬件容量与降级 |
| 超过 20 | 按 sizing 结果 | 合同允许，但必须显式提高软件上限并重新验收 |

默认软件保护规则：

- 每个 PLC 默认最多配置 20 个启用工站。
- 每个工站默认 1 个主事件 DB。
- 每个工站最多 4 个 DB mapping，用于主事件、扩展 payload、参数或诊断数据。
- 每个 PLC 必须有且只有一个 runtime/identity mapping。
- 同一 PLC 内，DB number 与地址范围不得发生未声明重叠。
- 超过声明上限时配置校验失败，V-PLC 和 Collector 均不得部分启动。
- `max_stations`、`max_db_mappings_per_station` 只能收紧默认上限；提高上限需要新的
  性能报告和 Verification 签字。

容量评估不能只看工站数量，还必须计算：

```text
reads_per_second
= Σ(1000 / poll_interval_ms × mappings_per_station)

estimated_payload_bytes_per_second
= Σ(read_size_bytes × reads_per_second)
```

Raspberry Pi 验收必须同时观察 CPU、内存、温度、PLC read latency、Collector loop
latency、queue depth、DB write latency、API p95、磁盘增长和错误率。真实 PLC 项目还要
结合 PLC 型号、DB 大小、PDU、网络抖动、连接数和 Snap7 性能重新 sizing。

## 7. DB Mapping

每个 mapping 独立声明：

```yaml
db_mappings:
  - mapping_id: WS01_MAIN
    plc_id: PLC_001
    station_id: WS01
    db_number: 101
    purpose: EVENT
    poll_interval_ms: 500
    templates:
      - common_header_v1
      - screw_payload_v1
```

规则：

- `mapping_id` 在 Edge 节点内唯一。
- `purpose` 推荐枚举：`RUNTIME`、`EVENT`、`PAYLOAD_EXT`、`PARAMETER`、`DIAGNOSTIC`。
- ACK 写回字段只能出现在明确声明 `direction: read_write` 的 mapping。
- Collector 按 mapping 生成一个或多个 read plan，不允许一个 read plan 跨 DB。
- 配置校验必须检查字段越界、地址重叠、缺少 required 字段和重复写地址。

## 8. Payload 与 NOK 模板

Payload 模板只定义字段解码，不定义 PLC 控制行为。模板至少包含：

- `template_id`、`version`、`compatible_station_types`。
- 字段名、S7 地址模板、类型、长度、required、单位、语义说明。
- 哪些字段进入共享列，哪些字段进入 `payload JSONB`。

NOK 模板至少包含：

- `template_id`、`version`。
- code、稳定名称、工站类型、分类、严重度和描述。
- 是否允许 V-PLC 随机模拟、是否允许手动强制模拟。

真实 PLC 的 NOK 判定始终来自 PLC/HMI。Edge 不根据 payload 阈值自行把 OK 改为
NOK。

## 9. Buffer 模型

Buffer 表达站间拓扑与观测语义，不表示 Edge 控制队列。

| 字段 | 说明 |
| --- | --- |
| `buffer_id` | 产线内唯一 |
| `from_station_id` | 上游工站 |
| `to_station_id` | 下游工站 |
| `buffer_position` | UI/拓扑排序位置；推荐位于上下游 `station_order` 之间 |
| `buffer_type` | `FIFO`、`PALLET`、`CONVEYOR`、`VIRTUAL` |
| `capacity` | 可观测容量；未知时可为空 |
| `tracking_mode` | `UNIT_ID`、`PALLET_ID`、`COUNTER_ONLY` |
| `enabled` | 是否参与拓扑和展示 |

V-PLC 可以按 Buffer 配置模拟 WIP。真实项目中 Buffer 进入、离开、阻塞和释放由
PLC 控制，Edge 只记录事件或由相邻工站事件推导观测状态。

## 10. 节拍配置

Cycle profile 必须区分工艺基线与仿真速度：

```yaml
cycle_profiles:
  normal_screw:
    ideal_cycle_time_s: 30.0
    simulation:
      base_cycle_s: 30.4
      jitter_s: 1.2
      cycle_scale: 1.0
```

- `ideal_cycle_time_s` 用于 OEE Performance 口径。
- `simulation.base_cycle_s/jitter_s` 仅用于 V-PLC。
- `cycle_scale` 仅用于 Demo 加速，不得改变 OEE 工艺基线。
- 真实 PLC 接入时，Edge 不向 PLC 下发这些值。

每个工站还可声明 station-level cycle time 与 station-level NOK 参数：

```yaml
stations:
  - station_id: WS04
    cycle_profile: normal_test
    simulation:
      nok_rate: 0.015
      random_seed_offset: 4
```

- `station.simulation.nok_rate` 优先于全局默认值。
- 全局 NOK rate 只作为未配置工站的 fallback，不覆盖显式工站值。
- 固定 random seed 加 `station_id` 或 `random_seed_offset` 生成独立、可复现随机流。
- 这些参数只控制 V-PLC，不得成为真实 PLC 的质量判定规则。

## 11. 兼容当前 WS01/WS02/WS03

首个配置化版本必须做到：

- `LINE_001`、`PLC_001`、DB104 保持不变。
- WS01/DB101、WS02/DB102、WS03/DB103 地址和模板语义保持不变。
- 当前 `config/mapping.yaml` 可被转换为 `LINE_001.yaml + templates`，解析后生成等价
  read plan。
- DB100 legacy 使用独立 compatibility adapter，不混入新 station template。
- 兼容期间旧链路与新配置链路的 KPI、Trace 和 ACK 不得相互替代。

## 12. WS01~WS10 与 WS01~WS20 扩展示例

扩展配置不复制 10 或 20 份完整字段定义，而是复用版本化模板：

```yaml
line_id: LINE_001
plcs:
  - plc_id: PLC_001
    max_stations: 20

stations:
  - {station_id: WS01, station_order: 10, station_type: ASSEMBLY, plc_id: PLC_001,
     enabled: true, mapping_refs: [WS01_MAIN], payload_template: assembly_v1,
     nok_template: assembly_nok_v1, cycle_profile: normal_assembly}
  - {station_id: WS02, station_order: 20, station_type: SCREW, plc_id: PLC_001,
     enabled: true, mapping_refs: [WS02_MAIN], payload_template: screw_v1,
     nok_template: screw_nok_v1, cycle_profile: normal_screw}
  # WS03~WS10 使用相同字段结构，可混合 TEST/VISION/LABEL/MANUAL 等类型。
```

WS01~WS10 验证配置要求：

- 至少 5 种 `station_type`。
- 至少 2 个 Buffer。
- 至少 1 个仅基础状态工站，其 payload 使用 `generic_status_v1`。
- 至少 2 个复杂 payload 工站。
- 一个 PLC 可下挂全部 10 站，也可按 PLC_001/PLC_002 拆分。

WS01~WS20 验证配置要求：

- 至少 2 个 PLC，每个 PLC 的工站数和 mapping 数均不超过声明上限。
- 至少 4 个 Buffer，包含 FIFO 和 PALLET 两类。
- 至少 1 个禁用工站，用于验证 `station_enabled=false` 不启动采集但历史仍可查询。
- 至少 1 个工站使用 2~4 个 DB mapping。
- 使用 fast/test profile 生成压力负载时，OEE 查询必须排除非 normal Profile 或明确标记。

扩展示例中的 DB number 仅为 Demo 分配结果，不是通用 Siemens 标准地址。实际项目必须
通过配置评审和地址冲突校验后使用。

## 13. 配置生命周期

配置发布流程：

```text
编辑 YAML
→ JSON Schema 校验
→ 语义校验
→ 生成 resolved JSON
→ 计算 config hash
→ 保存配置快照
→ V-PLC/Collector 启动或显式 reload
```

运行中禁止静默接受半份配置。reload 必须全量校验，失败时继续使用上一份有效配置并
记录错误。

配置快照至少包含：

- `schema_version`、`config_version`、`config_hash`。
- resolved line/PLC/station/buffer/mapping/template。
- 加载时间、加载来源、软件版本、校验结果。
- 生效范围和上一有效版本。

## 14. 语义校验规则

Schema 之外必须执行：

- `line_id/plc_id/station_id/buffer_id/mapping_id` 唯一性。
- `station_order` 在同一路线内唯一且大于 0。
- `station_enabled` 与 `enabled` 只允许一个规范字段；Phase-2 统一存储为 `enabled`，
  API 可提供 `station_enabled` 兼容别名。
- station、buffer、mapping、template 引用不得悬空。
- entry/terminal station 和 route graph 必须连通；禁用站不得成为唯一必经路径。
- Buffer 的上下游站不得相同，不得形成未声明循环。
- `buffer_position` 必须大于上游、且小于下游默认 route position；分支路线需显式声明
  route edge，不能仅靠 position 推导控制逻辑。
- DB number、offset、length、数据类型和 STRING 最大长度不得越界。
- read/write 地址冲突必须显式声明；ACK 字段不得出现在只读 mapping。
- payload required 字段、identity、counter、ready/valid/ACK 字段必须齐全。
- NOK code 在模板内唯一，且 station type 必须兼容。
- cycle time、poll interval、NOK rate、Buffer capacity 必须在配置范围内。
- `normal/fast/test` profile 名称受控；normal 的 OEE ideal CT 不受仿真 scale 改写。
- 配置估算负载超过当前硬件验收 envelope 时拒绝生产模式启动。

## 15. 验收条件

- 一份 YAML 可描述 1、3、10、20 个工站；20 以上可表达但必须重新 sizing。
- 工站顺序、类型、PLC、Buffer、mapping、payload、NOK 和 cycle profile 可校验。
- 重复 ID、悬空引用、DB 地址冲突和容量超限会阻止启动。
- WS01/WS02/WS03 解析结果与当前 mapping 等价。
- WS01~WS10、WS01~WS20 示例可生成稳定 resolved JSON 和 config hash。
- 工站级 cycle time、工站级 NOK rate、全局 NOK fallback 和固定 seed 可复现。
- CSV 不能绕过 YAML 和 Schema 成为运行时真源。
- Edge 配置中不存在控制 Hold、Rework、Skip/Bypass 的业务决策规则。
