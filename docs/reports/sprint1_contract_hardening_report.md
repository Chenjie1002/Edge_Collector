# Phase-2 Sprint 1 Contract Hardening Report

日期：2026-06-20
Thread：Architecture / Integration
状态：Verification 独立轻量复验 PASS；准备 final commit / push
运行链路：未接入

## 1. 执行摘要

Sprint 1 配置层已从“可加载 + 基础校验”升级为：

```text
YAML
→ strict allowed-key / enum validation
→ semantic validation
→ frozen dataclass tree
→ deterministic resolved config
→ canonical JSON
→ SHA-256 config hash
→ static load estimate
```

实现仍完全隔离，不被 V-PLC、Collector、API、DB、Dashboard 或 Docker 消费。

## 2. Verification HOLD 摘要与处理

| HOLD | 处理 |
| --- | --- |
| unknown field 静默丢弃 | 所有层级 fail closed，并返回字段路径 |
| station/buffer/profile 非法枚举 | 集中 enum registry |
| 20/4 上限可自行放大 | 固定 hard maximum；YAML 只能收紧 |
| Profile mode 丢失 | `CycleProfile.mode` 进入 frozen dataclass |
| stress 5 秒污染 ideal CT | 20 秒 production ideal 与 5 秒 simulation stress 分离 |
| payload template 过薄 | 增加 version/type/size/field layout |
| Buffer 指向 disabled WS20 | WS20 保持 disabled，但从 route/Buffer endpoint 移除 |

## 3. Reliability HOLD 摘要与处理

| HOLD | 处理 |
| --- | --- |
| 缺 config identity | config version + resolved canonical SHA-256 |
| 缺 seed/scenario/global NOK | `ScenarioConfig` 与 resolved fallback |
| mapping 不足以 sizing | read start/size/poll/direction/usage/type |
| 30003 可被随机/强制 | 固定 `system_reserved`，random/force 均禁止 |
| route graph 不完整 | Sprint 1 基础 entry/terminal/edge/reachability |
| 缺 hardware envelope | target hardware/load class + static summary |

## 4. 本次返修文件范围

- `common/line_config/schema.py`
- `common/line_config/models.py`
- `common/line_config/validator.py`
- `common/line_config/loader.py`
- `common/line_config/resolver.py`
- `common/line_config/__init__.py`
- `config/lines/demo_3_station.yaml`
- `config/lines/demo_10_station.yaml`
- `config/lines/stress_20_station.yaml`
- `tests/test_line_config.py`
- `docs/contracts/line_configuration.md`
- `docs/reports/sprint1_flexible_line_configuration_report.md`
- `docs/reports/sprint1_contract_hardening_report.md`
- 文档索引

没有修改任何现有运行链路。

## 5. Validator 规则

- unknown key：top-level、scenario、hardware、PLC、station、mapping、payload
  template/field、NOK template/code、profile/simulation、Buffer、route/edge。
- enum：station type、buffer type、profile mode、scenario type、mapping
  usage/direction/type、payload/NOK/field type、NOK category/severity/mode、hardware/load
  class。
- hard limits：整线/单 PLC 默认最多 20 stations，每 station 最多 4 mappings。
- reference：station/mapping PLC、mapping station、template、profile、Buffer、route。
- range：NOK rate、cycle、read size、poll interval、offset、capacity、field size。
- topology：entry/terminal enabled，edge/Buffer endpoint enabled，terminal 可达。
- timing：station production cycle 必须等于 profile ideal；stress timing 独立。
- NOK：reserved 30003 不得进入 random/forced；forced/random mode 必须显式授权。

## 6. 新增配置字段

- `config_version`
- `scenario.name/scenario_type/test_run_id/random_seed/global_nok_rate/production`
- `hardware_envelope.target_hardware_class/intended_load_class`
- `route_graph.entry_station_id/terminal_station_id/edges`
- Profile `mode` 与 `simulation.base_cycle_s/jitter_s/cycle_scale/stress_cycle_time_s`
- mapping `plc_id/station_id/usage/direction/mapping_type/read_start/read_size_bytes/poll_interval_ms`
- payload `version/template_type/approximate_size_bytes/fields`
- NOK code metadata 与 permission
- resolved station `effective_nok_rate`
- generated `config_hash`

## 7. Resolved config 与 hash

- `resolve_line_config(config)` 返回完整 dataclass tree 的 plain dictionary。
- `canonicalize_config(config)` 移除 `config_hash`，按 key 排序并输出紧凑 UTF-8 JSON。
- `compute_config_hash(config)` 对 canonical JSON 计算 SHA-256。
- loader 构造对象后计算 hash，并返回含 hash 的 frozen `LineConfig`。
- YAML key 顺序变化不影响 hash；seed 等有效语义变化会改变 hash。

## 8. Profile 与 stress cycle

`CycleProfile` 现在保留 mode 和独立 simulation timing。stress 样例：

- production/OEE ideal cycle：20 秒。
- simulation base：20 秒。
- simulation scale：4。
- stress scenario cycle：5 秒。
- scenario：`stress`、`production=false`。

因此 5 秒不会伪装成真实生产默认节拍。

## 9. Seed、NOK fallback 与 scenario

scenario 固定保存 random seed、test run identity 和 global NOK fallback。station 的
`nok_rate` 可为空；resolved object 同时保留 source `nok_rate=None` 与明确的
`effective_nok_rate`。

## 10. NOK 30003

`30003` 定义为 `UPSTREAM_NOK_SKIPPED`：

- category：route
- mode：system_reserved
- allow_random：false
- allow_force：false

validator 拒绝把 reserved code 改成普通 random/forced NOK。

## 11. RouteGraph、Buffer 与 disabled station

- entry/terminal 必须存在且 enabled。
- edge 和 Buffer endpoint 必须存在且 enabled。
- terminal 必须从 entry 可达。
- WS20 在 stress 样例中仍为 disabled，用于表达禁用配置，但不在有效 route 中，也不被
  Buffer 引用；terminal 调整为 WS19。

## 12. Hardware envelope 与 load estimate

`estimate_config_load()` 静态计算 station/mapping count、reads/s、read bytes/s、
event rate/s 和 payload bytes/s。该摘要供后续性能设计使用，不是实际硬件验收结果。

## 13. 测试清单

覆盖三份正例、Phase-1 baseline、immutability、unknown keys、enum、Profile 保真、
stress timing、version/hash、seed/NOK fallback、20/4 hard limits、PLC 引用、mapping
load fields、runtime DB、NOK permissions、route/Buffer/disabled station、hardware/load
summary 等。

测试先观察到 31 个目标失败，随后实施；最终 focused suite 为 62 项。

## 14. Deferred

- JSON Schema 文件自动生成。
- resolved snapshot 持久化、reload 和 previous-valid rollback。
- Collector read plan 与 S7 PDU/field overlap 完整算法。
- 复杂 route branch/merge/cycle 控制模型。
- V-PLC/Collector/API/DB/Dashboard 集成。
- 真实 Raspberry Pi 性能和长稳验收。
- Web Line Configuration Studio UI/API。

## 15. 最终本地复验

| Gate | 命令 | 结果 |
| --- | --- | --- |
| 配置层 | `.venv/bin/python -m pytest -q tests/test_line_config.py` | `77 passed` |
| 根级 tests | `.venv/bin/python -m pytest -q tests` | `88 passed` |
| API | 在 `api/` 执行 `../.venv/bin/python -m pytest -q tests` | `5 passed` |
| Collector | `PYTHONPATH=collector .venv/bin/python -m pytest -q collector/tests` | `12 passed, 3 subtests passed` |
| V-PLC | 在 `s7_plc_sim/` 执行 `../.venv/bin/python -m pytest -q tests` | `27 passed` |
| compileall | `.venv/bin/python -m compileall -q common/line_config tests/test_line_config.py api collector s7_plc_sim` | PASS |
| 三份 YAML | 独立调用 `load_line_config()` 与 `estimate_config_load()` | 3/10/20 stations PASS |
| 运行链路 import scan | 扫描 API/Collector/V-PLC/DB/Grafana/Compose | 无引用 |
| diff check | `git diff --check` | PASS |
| status | `git status --short --branch` | 未 commit；旧进度报告仍未跟踪 |

三份 resolved hash：

```text
demo_3_station.yaml    50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1
demo_10_station.yaml   08b9b4de701ef665597b0351240cc46d83ee649a5299f3db8551201d2a35dee5
stress_20_station.yaml e3afc329d76d559a3f211d088cfe2a749367a18774949db35d2af8a364a1fcfb
```

hash 变化原因是 resolved Buffer 新增 `enabled` 与 `tracking_mode` 两个合同字段；YAML
原始文本未修改。

## 16. Gate 结论

Verification 已完成独立轻量复验并将 Sprint 1 Gate 更新为 `PASS`。当前建议使用精确
allowlist 完成 final commit / push；仍不创建 tag、不部署、不执行 rollback drill。

## 17. Future Web Line Configuration Studio 预留

本 Sprint 已预留 pure Python loader/validator/resolver/hash/estimate 接口、集中 schema/
enum 和字段路径错误。后续仍需实现表单 UI、YAML round-trip、API、权限、版本历史和
发布工作流。本 Sprint 未实现网页、未新增前端项目、未接入 API/Dashboard。

## 18. Independent Gate 两项定向返修

Independent Gate Review 后仅修复两个剩余 blocker：

1. 显式 `station.nok_rate: null` 现在与字段缺失等价，source 值保留 `None`，
   `effective_nok_rate` 使用 global fallback。
2. Buffer 现在接受、校验并保留 `enabled` 与 `tracking_mode`；缺省分别为 `true` 和
   `counter_only`，tracking mode 枚举为 `unit_id/pallet_id/counter_only`。

resolver 无需专门分支：两字段进入 frozen dataclass 后，`asdict()`、canonical JSON 和
config hash 自动包含它们。strict unknown-field rejection 保持启用。

定向返修 focused suite：

```text
77 passed
```

最终完整复验结果见本报告第 15 节更新。
