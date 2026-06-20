# Line Configuration Contract

更新时间：2026-06-20
状态：Sprint 1 Gate PASS；配置合同已冻结并准备 final commit / push；运行链路尚未接入
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

### 2.1 Sprint 1 已实施子集

Sprint 1 采用以下最小基础：

```text
config/lines/*.yaml
→ common.line_config.load_line_config()
→ strict Python structure + semantic validator
→ immutable dataclass object tree
→ resolved config / canonical JSON / SHA-256 config hash
→ static load estimate
```

当前没有引入 JSON Schema 运行依赖，也没有把 line config 接入 V-PLC、Collector、API
或数据库。Python allowed-key/schema tables 是 Sprint 1 的结构单一真源；JSON Schema
文件生成、配置快照持久化和 reload 生命周期仍是后续配置治理工作。

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
    station_enabled: true
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
| `station_enabled` | 缺省为 `true`；禁用工站未来不启动采集，但不得删除历史数据 |

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

Sprint 1 YAML 使用小写枚举：

```text
unit_id | pallet_id | counter_only
```

两个字段均允许省略；resolved config 的明确缺省值为：

```yaml
enabled: true
tracking_mode: counter_only
```

显式值必须被 loader 保留并参与 canonical resolved config 与 config hash。
`enabled` 必须是 boolean；非法 `tracking_mode` 必须 fail closed。

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
     station_enabled: true, mapping_refs: [WS01_MAIN], payload_template: assembly_v1,
     nok_template: assembly_nok_v1, cycle_profile: normal_assembly}
  - {station_id: WS02, station_order: 20, station_type: SCREW, plc_id: PLC_001,
     station_enabled: true, mapping_refs: [WS02_MAIN], payload_template: screw_v1,
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
- Sprint 1 YAML 的规范字段为 `station_enabled`，缺省为 `true`。后续数据库内部可存储
  `enabled`，但配置/API 边界不得出现两个可同时设置且可能冲突的字段。
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

## 16. Sprint 1 Contract Hardening 冻结字段

### 16.1 配置身份与场景

顶层必须包含：

```yaml
schema_version: 1
config_version: "2026.06.20-demo3-v1"
scenario:
  name: phase1-compatible-demo
  scenario_type: demo       # demo | test | stress | synthetic
  test_run_id: demo3-default
  random_seed: 20260620
  global_nok_rate: 0.01
  production: true
hardware_envelope:
  target_hardware_class: raspberry_pi_5  # local_dev | raspberry_pi_5 | generic_edge
  intended_load_class: demo              # demo | medium | stress
```

- `config_version` 标识人工配置发布版本。
- `config_hash` 不写回 YAML，由 loader 对 resolved config 的 canonical JSON 计算 SHA-256。
- canonical JSON 使用 UTF-8、key 排序、无多余空白；hash 不包含自身 `config_hash` 字段。
- 同一语义配置仅调整 YAML key 顺序时 hash 不变；有效字段变化时 hash 改变。
- station 未声明 `nok_rate` 时，resolved station 保留 `nok_rate=null`，并通过
  `effective_nok_rate` 明确解析后的 global fallback。
- station 显式声明 `nok_rate: null` 与未声明语义相同；非 null 值仍必须通过 0~1
  范围校验。

### 16.2 Profile 与 timing

```yaml
cycle_profiles:
  synthetic_stress:
    mode: stress
    ideal_cycle_time_s: 20.0
    simulation:
      base_cycle_s: 20.0
      jitter_s: 0.5
      cycle_scale: 4.0
      stress_cycle_time_s: 5.0
```

- `ideal_cycle_time_s` 和 station `cycle_time_s` 是生产/OEE 工艺基线，二者必须一致。
- `base_cycle_s`、`jitter_s`、`cycle_scale`、`stress_cycle_time_s` 只描述仿真。
- stress/synthetic 必须显式提供 `stress_cycle_time_s`，且 scenario 必须
  `production: false`。
- stress 示例的 5 秒只用于未来仿真/压测，不得覆盖 20 秒工艺基线。

### 16.3 DB mapping 最小负载字段

每个 mapping 必须包含：

```yaml
mapping_id: WS01_MAIN
plc_id: PLC_001
station_id: WS01
db_number: 101
usage: event
direction: read_write
mapping_type: event
read_start: 0
read_size_bytes: 64
poll_interval_ms: 500
```

受控枚举：

- `usage`: `status/event/payload/payload_ext/parameter/diagnostic`
- `direction`: `read/read_write`
- `mapping_type`: `status/event/payload/runtime`

`read_size_bytes`、`poll_interval_ms` 必须为正数，`read_start` 必须为非负整数。station
mapping 的 `plc_id/station_id` 必须与父 station 一致。runtime DB 保留地址不得作为
station mapping。

### 16.4 Payload 与 NOK 最小字段

Payload template 必须包含 version、template type、compatible station types、
approximate size 和至少一个 field。field 必须包含 name、type、offset、length、
required 和 direction。

NOK code 必须包含 code、稳定 name、category、severity、mode、`allow_random` 和
`allow_force`。mode 分为：

- `random_simulated_nok`
- `forced_test_nok`
- `system_reserved`

`30003` 固定为 `UPSTREAM_NOK_SKIPPED` route semantic code，只允许
`system_reserved`，禁止 random 和 force。

### 16.5 Route、Buffer 与硬上限

- 默认合同硬上限为整线 20 stations、每 station 4 mappings；普通 YAML 只能收紧，
  不能自行提高。
- entry/terminal 必须存在且 enabled。
- route edge 和 Buffer endpoint 必须存在且 enabled。
- terminal 必须从 entry 可达。
- Buffer type 仅允许 `fifo/pallet/conveyor/virtual`，position 必须位于上下游 order
  之间。
- disabled station 可以保留在配置中供历史/未来用途，但不能成为当前 route 或 Buffer
  endpoint。`stress_20_station.yaml` 的 WS20 因此不进入当前有效 route。

### 16.6 静态负载摘要

`estimate_config_load(config)` 返回：

- station / mapping count
- reads per second
- estimated read bytes per second
- estimated event rate per second
- estimated payload bytes per second

这些值只由配置静态估算，用于后续 sizing 输入，不代表 Raspberry Pi 性能验收结果。

## 17. Strict validation 与错误定位

`common/line_config/schema.py` 集中管理 allowed keys、enum 和 hard limit。validator 对
top-level、scenario、hardware、PLC、station、mapping、payload template/field、NOK
template/code、profile/simulation、Buffer、route/edge 全部 fail closed。

错误保留字段路径，例如：

```text
stations[0].foo is not allowed
plcs[0].unknown_key is not allowed
cycle_profiles.synthetic_stress.simulation.jitter_s must be non-negative
route_graph.edges[2].to_station_id 'WS99' does not exist
```

validator 是纯 Python 调用接口，不依赖 CLI，可直接被未来 API/Web backend 复用。

## 18. Future Web Line Configuration Studio

未来 Web-based Line Configuration Studio 可以直接复用：

- `load_line_config()`：YAML 文件导入。
- `validate_line_config()`：结构化路径错误。
- centralized schema/enums：表单选项和前后端规则单一真源。
- frozen dataclass model：YAML 反向解析后的稳定对象。
- `resolve_line_config()`：resolved config 预览。
- `canonicalize_config()` / `compute_config_hash()`：hash 预览。
- `estimate_config_load()`：静态负载摘要。

后续实现内容包括表单 UI、YAML 编辑/导出、实时字段高亮、API 封装、权限、版本历史与
配置发布流程。本 Sprint 不新增 React/Next.js，不新增前端项目，不接入 API/Dashboard，
也不修改任何运行链路。
