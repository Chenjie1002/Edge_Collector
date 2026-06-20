# Phase-2 Sprint 1 Reliability Configuration Review

> **历史 Review 说明**
>
> 本报告记录 Sprint 1 Contract Hardening 之前的 Reliability review 状态。正文中的
> blocker、gap 和 `HOLD / CHANGES REQUIRED` 均为历史证据，已由
> `sprint1_contract_hardening_report.md` 完成返修，并由
> `sprint1_independent_gate_review.md` 独立关闭。Sprint 1 最终 Gate：**PASS**。
> 当前状态以上述两份最终报告为准。

日期：2026-06-20
Thread：Reliability
评审范围：Flexible Line Configuration 最小配置基础
实现代码修改：无
远程操作：无
最终 Gate 建议：`HOLD / CHANGES REQUIRED`

## 1. 评审摘要

Sprint 1 已形成一个隔离、可测试且不影响 Phase-1 运行链路的配置基础：

```text
config/lines/*.yaml
→ common.line_config.load_line_config()
→ semantic validation
→ frozen dataclass tree
```

当前实现能够稳定加载 WS01~WS03、WS01~WS10、WS01~WS20，能够表达
`station_type`、`station_order`、station-level cycle time、station-level NOK rate、
模板引用、DB number、PLC 上限和 Buffer 基础关系。现有负例对重复 ID/order、悬空引用、
DB 冲突和基础范围错误提供了有效保护。

但是，该配置尚不足以作为后续 V-PLC 参数化真源或性能压测真源。关键原因：

1. `cycle_profile.mode` 被 validator 校验，但在 `CycleProfile` dataclass 中被丢弃。
2. `random_seed`、global NOK rate、`config_version`、resolved config/hash 均未实现。
3. 未知字段会被静默接受并在解析时丢弃，配置拼写错误可能不报错。
4. `stress_20_station.yaml` 将 test Profile 的 `ideal_cycle_time_s` 和
   `cycle_time_s` 都改为 5 秒，未保持“仿真加速不改变工艺/OEE基线”的 Phase-1 规则。
5. payload template、DB mapping 缺少字段、read size、poll interval、方向和 payload
   大小，无法计算负载或生成可靠 read plan。
6. `30003 WS03_UPSTREAM_NOK` 与普通可随机/强制 NOK code 混在同一列表，未来 V-PLC
   可能误用。
7. 当前 Buffer 不是完整 route graph；20 站样例还将 Buffer 指向禁用的 WS20。

结论：

- 建议 Architecture Thread 继续修正 Sprint 1 配置基础。
- 不建议当前版本进入 Sprint 1 最终 gate。
- 不应在这些问题修正前接入 V-PLC、Collector 或性能压测运行链路。
- 当前无 Phase-1 回归，也未发现业务代码被误改。

## 2. 评审依据

### Phase-2 架构基线

- `docs/reports/phase2_architecture_freeze_report.md`
- `docs/reports/phase2_flexible_architecture_plan.md`
- `docs/contracts/line_configuration.md`
- `docs/reports/phase2_sprint_plan.md`
- `docs/reports/phase2_thread_task_plan.md`

### Sprint 1 交付

- `common/line_config/`
- `config/lines/demo_3_station.yaml`
- `config/lines/demo_10_station.yaml`
- `config/lines/stress_20_station.yaml`
- `tests/test_line_config.py`
- `docs/reports/sprint1_flexible_line_configuration_report.md`
- `docs/superpowers/plans/2026-06-20-flexible-line-configuration.md`

## 3. 配置优点

### 3.1 隔离性良好

- 当前运行链路没有导入 `common.line_config`。
- 未修改 V-PLC、Collector、API、DB、Dashboard、migration、Docker 或 `.env`。
- 三份 YAML 当前只是后续 Sprint 的输入资产，不会改变 Phase-1 运行行为。
- frozen dataclass 降低了加载后被无意原地修改的风险。

### 3.2 基础拓扑表达清晰

- 3/10/20 工站样例均可加载。
- `station_id` 和 `station_order` 唯一性已校验。
- station 到 PLC、payload template、NOK template、cycle profile 的引用已校验。
- PLC runtime DB、station DB 重复、mapping 数量和 station 数量上限已有保护。
- Buffer 上下游引用、位置和容量已有基础校验。

### 3.3 Phase-1 兼容意识正确

- 三站样例保留 `LINE_001`、`PLC_001`、DB101/102/103 和 DB104。
- 三站 cycle baseline 与 station NOK rate 保持当前 Phase-1 值。
- 当前实现没有提前替换 `config/mapping.yaml` 或 `config/vplc.yaml`。
- strict ACK、`plc_boot_id`、counter namespace 和参数审计没有被改动。

### 3.4 错误报告可用

- loader 区分文件不存在、YAML 语法错误、根节点类型错误和 semantic error。
- semantic error 使用字段路径聚合，适合作为未来 CLI 和 CI 检查基础。

## 4. V-PLC 参数化支撑评审

| 能力 | 当前状态 | Reliability 结论 |
| --- | --- | --- |
| WS01~WS03 | 支持 | 可表达并通过回归 |
| WS01~WS10 | 支持 | 可表达，不代表运行容量已验证 |
| WS01~WS20 | 支持 | 可表达，不代表 Raspberry Pi envelope 已验证 |
| `station_type` | 部分支持 | 任意字符串；缺少受控 registry/规范化 |
| `station_order` | 支持 | 适合排序，不足以表示分支、合流和旁路 |
| station-level cycle time | 部分支持 | `cycle_time_s` 与 profile ideal CT 语义和优先级不清 |
| Profile | 部分支持 | YAML 有 mode，但解析对象丢失 mode |
| global NOK rate | 不支持 | 顶层无字段、模型无字段、无 fallback 规则实现 |
| station-level NOK rate | 支持 | 已校验 0~1 |
| payload template | 严重不足 | 只有兼容类型，没有字段、地址、类型、长度或版本 |
| NOK template | 部分支持 | 只有 code 列表，缺少随机/强制权限和稳定名称 |
| Buffer | 部分支持 | 可表达局部关系，缺少 enabled、tracking mode 和完整路线 |

### 4.1 当前不能直接供 V-PLC 消费的原因

- `CycleProfile` 只保留 `profile_id` 和 `ideal_cycle_time_s`；`normal/fast/test` mode
  在 loader 输出中为不可用状态。
- 没有 `base_cycle_s`、`jitter_s`、`cycle_scale` 的分层结构。
- 没有 line-level `random_seed` 和 station seed offset。
- 没有 global NOK fallback。
- payload template 不能生成 DB byte layout 或 payload writer。
- NOK template 不能区分：
  - PLC 真实 NOK。
  - V-PLC 随机 NOK。
  - V-PLC 手动强制 NOK。
  - 下游 `SKIPPED` 语义 code。
- Buffer 不能可靠构建 RouteGraph。

## 5. 性能压测支撑评审

| 压测维度 | 当前状态 | 缺口 |
| --- | --- | --- |
| 产线长度 | 支持 | 仅能从 station order 推测线性长度 |
| station 数量 | 支持 | 有 PLC station limit |
| payload size | 不支持 | template 无字段和 size |
| cycle time | 部分支持 | 工艺基线与仿真时间混合 |
| NOK rate | 部分支持 | station-level 有，global fallback 无 |
| long-run duration | 不支持 | 无 smoke/8h/24h 场景字段 |
| stress profile | 部分支持 | YAML mode=test，但 loader 丢失 mode |
| fixed random seed | 不支持 | 无全局 seed 或 station offset |
| 参数快照 | 不支持 | 无 resolved config/version/hash |
| 参数变更审计 | 未接入 | 可后续接 Phase-1 audit writer，但必须先有稳定配置身份 |

### 5.1 缺少可计算的负载输入

合同要求估算：

```text
reads_per_second
estimated_payload_bytes_per_second
```

当前模型缺少：

- `poll_interval_ms`
- `read_start`
- `read_size_bytes`
- payload field count/size
- mapping direction
- PLC connection 数与连接参数
- batch/queue 目标
- test duration

因此 `stress_20_station.yaml` 当前只是“20 个 station object 的配置压力样例”，不能作为
Raspberry Pi、Snap7、Collector 或 PostgreSQL 的性能压力定义。

## 6. 可复现性评审

### 6.1 Profile 命名

优点：

- profile ID 使用 `normal_*`、`stress_*`，可读性较好。
- mode 限制为 `normal/fast/test`，延续 Phase-1 术语。

风险：

- profile ID 与 mode 是两个维度，但 loader 丢弃 mode。
- `stress_*` 的 ideal CT 设置为 5 秒，容易把“工艺基线”和“测试速度”混为一谈。
- station-level `cycle_time_s` 与 profile `ideal_cycle_time_s` 重复，缺少解析优先级。

### 6.2 Seed

当前无法固定 seed，也没有 station seed offset。相同 YAML 无法保证产生相同 NOK、
jitter 或异常序列。

### 6.3 配置版本与 Hash

当前只有 `schema_version`：

- 没有 `config_version`。
- 没有 canonical resolved JSON。
- 没有 source hash。
- 没有 resolved config hash。
- 没有 previous valid config reference。

`schema_version` 只能说明格式版本，不能标识一次具体配置发布。

### 6.4 未知字段处理

实际验证表明，在 YAML 中加入以下字段仍可成功加载：

```text
random_seed
global_nok_rate
config_version
unexpected_typo_field
cycle_scale
```

这些字段随后不会出现在 `LineConfig` 或 `CycleProfile` 对象中。该行为会造成“配置文件
看起来已设置，运行时实际未生效”的高风险静默失败，性质与 Phase-1 参数误用问题相似。

## 7. 配置风险

### R1 — Profile 语义在解析后丢失（阻塞）

位置：

- `common/line_config/models.py`
- `common/line_config/loader.py`
- `common/line_config/validator.py`

validator 校验 `cycle_profiles.*.mode`，但 `CycleProfile` 不保存 mode。未来 V-PLC 无法
可靠区分 normal/fast/test。

### R2 — Stress 配置重新混淆工艺基线与仿真速度（阻塞）

`stress_20_station.yaml` 将：

```text
ideal_cycle_time_s = 5.0
station cycle_time_s = 5.0
```

用于全部 test Profile。这违反 Phase-1 已冻结的原则：fast/test 只改变仿真速度，不改变
OEE ideal cycle time 或真实 process baseline。

### R3 — 缺少 seed、config version 与 hash（阻塞）

无法证明：

```text
same config + same seed + same profile = reproducible result
```

也无法将 cycle、参数快照、性能结果和具体配置发布可靠关联。

### R4 — 未知字段静默接受（阻塞）

拼写错误、尚未实现的字段或过期字段不会触发失败，而是被 loader 丢弃。配置系统必须
fail closed，不能静默降级。

### R5 — Payload/DB mapping 不足以生成 read plan 或计算负载（阻塞）

当前 template 仅有 compatible station type，mapping 仅有 DB number 和 purpose。无法：

- 生成 S7 字段布局。
- 校验字段 offset/length overlap。
- 区分 read-only/read-write。
- 确认 ACK 地址。
- 计算 payload bytes/sec。
- 验证 Snap7 PDU/read size。

### R6 — NOK code 语义不足（阻塞）

`demo_3_station.yaml` 的 WS03 NOK template 包含 `30003`。Phase-1 中该 code 表示上游
NOK 导致的下游 `SKIPPED`，不允许作为 WS03 随机或手动强制 NOK。

当前模板没有 `allow_random`、`allow_force`、稳定名称、类别、严重度或描述，未来消费者
无法安全过滤。

### R7 — Route/Buffer 与禁用工站风险（阻塞）

- 没有显式 entry、terminal、route edge、branch、merge 或 bypass。
- `station_order` 只能排序，不能代表完整路线。
- `stress_20_station.yaml` 中 WS20 被禁用，但 `BUF_WS19_WS20` 仍指向 WS20。
- validator 不检查禁用站是否成为唯一必经或 terminal 路径。

未来 V-PLC 若按 order 自动串联，可能在禁用站处停线或生成错误终点。

### R8 — 硬件容量上限缺少依据（高）

配置可声明任意 `max_stations` 和 mapping limit；validator 只检查自声明值，不检查已验收
hardware envelope。20 站当前是目标，不是容量证明。

### R9 — 字段枚举与规范化不足（高）

以下字段是任意字符串：

- `station_type`
- mapping `purpose`
- `buffer_type`

合同示例有大小写混用。loader 校验时会 trim 部分文本，但构建对象使用原始值，可能造成
大小写、空格或别名导致消费者分支不一致。

### R10 — Enabled 计数语义不一致（中）

合同描述 PLC 默认最多 20 个“启用工站”，当前 validator 对启用和禁用 station 全部计数。
需要明确上限约束的是配置对象数、启用运行数，还是两者分别限制。

## 8. 必须在 Sprint 1 修正

以下项目建议作为 Sprint 1 最终 gate 的硬条件。

### M1. 完成严格配置结构

- 增加 JSON Schema，或提供等价的严格 unknown-field rejection；按冻结合同应优先使用
  JSON Schema。
- 明确 required/optional/default 字段。
- 拒绝未知字段、错拼字段和不支持字段。
- 校验受控枚举与大小写规范。

### M2. 完成 canonical resolved config 与身份

- 增加 `config_version`。
- 生成 deterministic canonical resolved JSON。
- 分开记录 source file hash 与 resolved config hash。
- 明确 hash 算法和 canonicalization 规则。
- 增加稳定性测试：同一语义输入产生相同 hash；有效变更产生不同 hash。

### M3. 修正 Profile 与 Cycle Time 模型

Profile 至少保留：

```text
profile_id
mode = normal | fast | test
ideal_cycle_time_s
simulation.base_cycle_s
simulation.jitter_s
simulation.cycle_scale
```

- 明确 station override 的优先级。
- normal 禁止危险 scale/base。
- fast/test 只修改仿真速度。
- 修正 `stress_20_station.yaml`，不得用 5 秒覆盖工艺/OEE ideal CT。
- 删除或定义 `station.cycle_time_s` 与 profile ideal/base 的唯一语义，避免双真源。

### M4. 增加可复现仿真参数

- line/scenario-level `random_seed`。
- station-level deterministic seed offset，或从稳定 station ID 推导的明确算法。
- global NOK fallback。
- station-level NOK override。
- `test_run_id` 或 scenario ID。
- smoke/8h/24h duration 目标字段，或独立 versioned stress scenario。

### M5. 补齐 payload、mapping 与 sizing 最小字段

Sprint 1 不必实现 V-PLC/Collector，但配置必须足够让后续消费者无歧义生成：

- field layout/version。
- read/write direction。
- DB offset、length、type、STRING max length。
- read start/read size。
- poll interval。
- expected payload bytes。
- ACK/identity/required field 标记。

必须新增 overlap、range、direction、required field 和 payload size 负例。

### M6. 修正 NOK template

- 每个 code 至少有稳定名称、来源语义和 `allow_random/allow_force`。
- `30003` 只能作为 downstream SKIPPED/route semantic code，不能进入 WS03 随机或强制
  NOK 集合。
- template 需保留 version，避免同 code 意义漂移。

### M7. 增加 RouteGraph 与禁用站校验

- 明确 entry、terminal 和 route edge。
- station order 只用于默认排序。
- 检查连通性、循环、悬空、禁用站唯一必经路径。
- 修正 `BUF_WS19_WS20` 与 disabled WS20 的语义冲突。
- Buffer 增加 `enabled` 和 `tracking_mode`，明确它只用于观测/模拟，不授权 Edge 控制。

### M8. 定义硬件 envelope 引用

Sprint 1 无需完成真实 Raspberry Pi 性能验收，但必须：

- 在配置或 stress scenario 中声明目标 envelope ID/版本。
- 提供足够字段计算 reads/sec 和 bytes/sec。
- 生产模式配置超过已验收 envelope 时设计为 fail closed。
- 明确 3/10/20 只是配置目标，容量 PASS 由后续 Verification/Sprint 8 给出。

### M9. 补充测试

至少增加：

- unknown field rejection。
- mode/scale/ideal CT 保留。
- seed/global NOK/override resolution。
- canonical hash 稳定性。
- stress Profile 不改变 ideal CT。
- `30003` 不允许 random/force。
- disabled station route/terminal。
- mapping range/overlap/direction/payload size。
- hardware envelope 超限。
- enabled station count 语义。

## 9. 可后续优化项

以下内容可以在 Sprint 1 gate 之后或运行接入 Sprint 中实现：

- V-PLC/Collector 热 reload。
- reload 失败后保持上一有效配置的运行逻辑。
- 配置参数写入 Phase-1 审计表的 runtime adapter。
- 完整 8 小时/24 小时实际 soak。
- Raspberry Pi 实测 capacity envelope。
- Collector queue/batch/backpressure 实现。
- Prometheus `collector_config_hash_info` 等 runtime metrics。
- 配置快照数据库表和查询 API。
- 在线配置编辑器。
- 多分支、合流、循环工艺的完整 UI。
- Multi-Line。

注意：这些实现可以后续做，但 Sprint 1 必须先把它们需要的稳定配置身份、字段和边界
定义清楚。

## 10. 对 V-PLC 参数化的建议

建议后续使用独立 resolved runtime DTO，不直接把原始 YAML dict 传入 V-PLC：

```text
LineConfig source
→ strict validation
→ ResolvedLineConfig
  ├─ config_version/hash
  ├─ profile/mode
  ├─ global seed/NOK
  ├─ PlcRuntimeConfig[]
  ├─ StationRuntimeConfig[]
  ├─ RouteGraph
  ├─ Payload/NOK templates
  └─ HardwareEnvelopeRef
→ V-PLC
```

V-PLC 必须继续保护 Phase-1 规则：

- 未 ACK payload 不覆盖。
- `plc_boot_id` 和 counter namespace 不由 line config 随意覆盖。
- normal Profile 的 cycle guardrail 不可绕过。
- fast/test 数据必须带 profile/test run/config hash。
- 参数修改继续写 actor/reason/request ID/old/new/accepted。
- 配置错误时全量拒绝启动，不允许只启动部分 station。

## 11. 对性能压测的建议

建议将“产线配置”和“压力场景”分开版本化：

```text
line config
  = topology + PLC + station + mapping + templates + process baseline

stress scenario
  = profile + scale + seed + duration + fault schedule + target envelope
```

建议最小场景：

| Scenario | Station | Duration | 目的 |
| --- | ---: | ---: | --- |
| smoke_3 | 3 | 1h | Phase-1 兼容回归 |
| medium_10 | 10 | 1h/8h | 常规负载 |
| stress_20 | 20 | 1h | 峰值/容量探索 |
| soak_20 | 20 | 8h/24h | 长稳、温度、磁盘增长 |

每次压测记录：

- source/resolved config hash。
- scenario version、seed、profile、test run ID。
- 软件 commit/release ID。
- station/PLC/mapping/read size。
- CPU、内存、温度、磁盘。
- poll/decode/DB/ACK latency。
- queue depth、错误率、丢弃/重试。
- 事件数和数据库增长。

## 12. 对可复现性的建议

可复现实验身份建议固定为：

```text
software_version
+ schema_version
+ config_version
+ resolved_config_hash
+ scenario_version
+ random_seed
+ profile
+ test_run_id
```

snapshot 至少在以下时点生成：

- 启动。
- 配置 reload。
- Profile 切换。
- runtime 参数修改。
- 测试开始和结束。

事件至少能够无歧义关联 profile、config hash、PLC boot 和 test run。

## 13. 对 Config Hash 的建议

建议同时保留：

1. `source_sha256`
   - 对原始 YAML bytes 计算。
   - 用于发布包和文件完整性。
2. `resolved_config_sha256`
   - 对补齐 default、规范化枚举、排序后的 canonical JSON 计算。
   - 用于运行时身份、snapshot、事件关联和可复现性。

canonical 规则必须固定：

- UTF-8。
- key 排序。
- station/mapping/route 使用明确稳定排序。
- 浮点数规范化。
- 不包含加载时间、路径和其他易变字段。

只有 source 格式变化而语义不变时，source hash 可变化，resolved hash 应保持稳定。

## 14. 对 Hardware Envelope 的建议

建议配置引用版本化 envelope，而不是让每份 YAML 自行声称“支持 20 站”：

```yaml
hardware_envelope_ref: rpi5_8gb_ssd_v1
```

envelope 至少记录：

- Raspberry Pi 型号、内存、存储介质、散热条件。
- PLC 数、连接数、station 数、mapping 数。
- poll interval、read bytes/sec、event rate。
- queue/batch 参数。
- DB/API 并发和保留期。
- CPU、内存、温度、磁盘增长和 p95 门限。

Sprint 1 负责配置表达和静态估算；真实 PASS/FAIL 由后续 Verification 压测给出。

## 15. 对 Route Graph 的建议

不要用 `station_order` 或 Buffer 列表隐式生成控制流程。建议显式表达：

```yaml
route:
  entry_station_id: WS01
  terminal_station_ids: [WS19]
  edges:
    - {from: WS01, to: WS02, behavior: normal}
```

要求：

- route graph 用于 V-PLC 模拟和 Trace/OEE 拓扑，不授权 Edge 控制真实设备。
- branch/merge/bypass 必须显式声明。
- disabled station 不得成为唯一 entry、terminal 或必经路径。
- Buffer 关联 route edge，但 Buffer 不决定 release/transfer。
- 真实 PLC 的路线事实仍来自 PLC/HMI 事件。

## 16. 是否发现业务代码被误改

结论：`未发现`。

工作树检查未发现以下路径发生修改：

- `s7_plc_sim/`
- `collector/`
- `api/`
- `db/`
- `config/grafana/`
- `docker-compose.yml`
- `.env`
- `.env.example`

代码搜索也未发现现有运行模块导入 `common.line_config`。当前新增代码仅为隔离配置包和
配置层测试。

未跟踪旧文件 `docs/Edge MES Demo 当前进度报告.md` 未被本评审修改、暂存或纳入交付。

## 17. 测试与评审证据

本次 Reliability 评审重新执行：

| 检查 | 结果 |
| --- | --- |
| `tests/test_line_config.py` | PASS，21 |
| 根级 `tests/` | PASS，32 |
| API tests | PASS，5 |
| Collector tests | PASS，12；另含 3 个 subtests |
| V-PLC tests | PASS，27 |
| Python compileall | PASS |
| 三份 YAML 加载 | PASS |
| 配置解析字段检查 | PASS，确认 mode/seed/hash/sizing 字段当前缺失 |
| 运行链路导入扫描 | PASS，未发现接入 |
| `git diff --check` | PASS |

Collector Snap7 集成测试连接清理阶段输出一条
`Expected COTP DT, got 0x80`，不影响断言和退出码。

## 18. Gate 结论

### 是否建议 Sprint 1 继续推进

`建议继续`。当前隔离实现方向正确，适合小步补齐。

### 是否建议 Architecture Thread 修正配置

`建议修正`。优先顺序：

1. Profile/cycle/seed/global NOK。
2. config version/resolved hash/unknown-field rejection。
3. payload/mapping sizing。
4. NOK 语义与 `30003`。
5. route graph/disabled station。
6. hardware envelope 引用和负例。

### 是否建议进入 Sprint 1 最终 gate

`暂不建议`。

最终 gate 至少要求 M1~M9 完成、测试通过，并再次由 Reliability 与 Verification
复核。当前版本可以作为“最小配置基础 checkpoint”，不能作为“可供 V-PLC、Collector
或性能压测消费的冻结配置合同实现”。
