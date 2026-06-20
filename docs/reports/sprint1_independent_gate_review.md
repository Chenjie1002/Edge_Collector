# Phase-2 Sprint 1 Independent Gate Review

日期：2026-06-20
Thread：Verification
Sprint：Flexible Line Configuration
评审对象：Architecture Contract Hardening
运行链路修改：无
远程操作：无
Gate 结论：**PASS**

> 2026-06-20 最终轻量复验已完成，权威结论见第 16 节。第 1~14 节保留首次独立
> 复验时的 HOLD 证据与返修条件，作为问题发现和关闭记录。

## 1. Gate 结论（首次独立复验历史）

Architecture Contract Hardening 已关闭初始 Verification HOLD 的七个核心问题，并通过
绝大多数 Reliability 配置身份、Profile、mapping、NOK、route 和静态负载要求。

独立复验仍发现两个阻塞问题：

1. 合同允许 station 显式配置 `nok_rate: null` 使用
   `scenario.global_nok_rate`，validator 也接受；但 loader 在构建
   `effective_nok_rate` 时执行 `float(None)`，抛出 `TypeError`。
2. `line_configuration.md` 和 Architecture handoff 要求 Buffer 保存
   `enabled`、`tracking_mode`，但 `BufferConfig`、allowed keys、loader、YAML 和测试
   均未实现；带这两个合同字段的配置被当作 unknown field 拒绝。

Verification 为这两个问题加入了轻量合同测试，没有修改实现。最终 focused suite：

```text
74 passed, 2 failed
```

因此当前不建议 commit / push Sprint 1。修正两个阻塞并完成本报告复验条件后，可重新
评估 PASS。

## 2. 复验范围

已复验：

- Architecture handoff 与 context restore。
- 初始 Verification / Reliability HOLD 报告。
- Contract Hardening 实施报告。
- `common/line_config/` loader、models、schema、validator、resolver 和公共导出。
- 三份 3/10/20 工站 YAML。
- `tests/test_line_config.py`。
- Line Configuration Contract、Sprint 计划、Roadmap 和文档索引。
- 配置、根级、API、Collector、V-PLC 和 compileall 回归。
- 15 项独立负例/hash 抽查。
- 当前 Git 基线、运行链路隔离和未跟踪文件。

未执行：

- 远程部署。
- 服务重启。
- Acceptance Sprint。
- rollback drill。
- migration、Docker、`.env` 或 volume 操作。

## 3. Verification HOLD 项逐项复验

| 初始 HOLD | 独立证据 | 结果 |
| --- | --- | --- |
| 非法 `station_type` 应失败 | 临时变体 `teleporter` 返回字段路径错误 | CLOSED / PASS |
| 超过默认 20 站应失败 | 21 stations + `max_stations=21` 仍被 hard maximum 20 拒绝 | CLOSED / PASS |
| 每站超过 4 DB mapping 应失败 | 5 mappings + declared limit 5 仍被 hard maximum 4 拒绝 | CLOSED / PASS |
| 非法 `buffer_type` 应失败 | `teleporter` 被 enum validator 拒绝 | CLOSED / PASS |
| unknown field 应失败 | top-level、station 及深层结构均 fail closed | CLOSED / PASS |
| Profile mode 不得丢失 | `CycleProfile.mode`、simulation timing 进入 frozen dataclass | CLOSED / PASS |
| stress cycle 语义修正 | ideal/base 20s、scale 4、stress 5s、`production=false` | CLOSED / PASS |

结论：**原 Verification HOLD 项全部关闭。**

## 4. Reliability HOLD 项逐项复验

| Reliability HOLD | 独立复验 | 结果 |
| --- | --- | --- |
| strict unknown-field rejection | 覆盖 top/scenario/hardware/PLC/station/mapping/template field/NOK code/profile simulation/Buffer/route | PASS |
| config version | 三份 YAML 与 `LineConfig.config_version` 存在 | PASS |
| canonical resolved config | `resolve_line_config()` + sorted compact JSON | PASS |
| stable config hash | YAML key 顺序不变 hash；seed 变化改变 hash | PASS |
| seed | `ScenarioConfig.random_seed` 保留 | PASS |
| global NOK fallback | 缺省 key 时有效；显式 null 时 loader 崩溃 | **FAIL / BLOCKER** |
| scenario / test run metadata | name/type/test_run_id/production 均保留 | PASS |
| Profile / ideal / base / jitter / scale 分离 | dataclass 与 stress YAML 均分离 | PASS |
| payload / mapping 支撑基础 sizing/read plan | field layout、size、read range、poll、direction、usage/type 存在 | PASS（基础层） |
| NOK 30003 reserved | `system_reserved`，random/force false；篡改会失败 | PASS |
| RouteGraph 基础校验 | enabled entry/terminal、edge 引用、可达性 | PASS |
| Buffer 不指向 disabled station | validator 拒绝；stress Buffer 终点修正为 WS19 | PASS |
| Buffer `enabled/tracking_mode` | 合同与 handoff 要求存在，实现拒绝字段 | **FAIL / BLOCKER** |
| hardware envelope / static load estimate | hardware/load class 与 reads/s、bytes/s、event/payload rate 输出存在 | PASS（非性能认证） |
| 对应负例测试 | 原 62 项 + Verification 补充深层 unknown/enum；两条新合同测试暴露阻塞 | PARTIAL / HOLD |

结论：**Reliability HOLD 尚未全部关闭。**

## 5. 代码与配置审计结果

### 5.1 Strict unknown-field rejection

`schema.py` 集中 allowed keys，validator 已覆盖：

- top-level。
- scenario / hardware。
- PLC / station / mapping。
- payload template / payload field。
- NOK template / NOK code。
- cycle profile / simulation。
- Buffer。
- route graph / route edge。

错误包含字段路径。Verification 新增三条深层 unknown 测试后均通过。

状态：`PASS`

### 5.2 Enum validation

已验证：

- station type。
- buffer type。
- profile mode。
- mapping usage / direction / type。
- payload template / field type。
- NOK template / category / severity / mode。
- scenario type、hardware/load class。

Verification 新增 mapping/template/NOK enum 负例后全部通过。

状态：`PASS`

### 5.3 Profile mode preservation

- `CycleProfile.mode` 存在。
- loader 保存 mode。
- tests 断言 normal 与 stress Profile。

状态：`PASS`

### 5.4 Stress timing semantics

`stress_20_station.yaml`：

```text
scenario_type=stress
production=false
ideal_cycle_time_s=20
base_cycle_s=20
jitter_s=0.5
cycle_scale=4
stress_cycle_time_s=5
```

5 秒只用于 synthetic stress，不覆盖 OEE production ideal。

状态：`PASS`

### 5.5 Config identity / hash

- `config_version` 存在。
- resolved config 包含完整 frozen dataclass tree。
- canonical JSON 去除 `config_hash`，按 key 排序，UTF-8 紧凑输出。
- SHA-256 对 canonical JSON 计算。
- YAML key 顺序变化 hash 不变。
- random seed 变化 hash 改变。

状态：`PASS`

### 5.6 Seed / global NOK / station override

- seed、scenario、test run ID 已保留。
- station override 与 `effective_nok_rate` 已存在。
- station 不声明 `nok_rate` 时 fallback 正常。
- station 显式声明 `nok_rate: null` 时 validator 接受，但 loader 抛出 `TypeError`。

状态：`FAIL`

### 5.7 PLC / station / DB mapping limits

- station / mapping PLC 引用严格。
- 21 stations 被硬上限拒绝。
- 5 mappings 被硬上限拒绝。
- runtime DB reservation 冲突被拒绝。
- mapping read size/poll/range 和 enum 已校验。

状态：`PASS`

### 5.8 Payload / mapping fields

已具备：

- mapping DB number、read start、read size、poll interval、direction、usage/type。
- payload template version/type/approximate size。
- payload field type/offset/length/required/direction。

当前仍未实现完整 S7 PDU、字段 overlap 和 read-plan 生成，Hardening 报告已明确 deferred。
这些不阻塞当前配置合同基础 Gate，但在 Sprint 3 接入前必须完成。

状态：`PASS（Sprint 1 基础范围）`

### 5.9 NOK 30003

`30003 UPSTREAM_NOK_SKIPPED`：

```text
category=route
mode=system_reserved
allow_random=false
allow_force=false
```

篡改为 random pool 会被拒绝。

状态：`PASS`

### 5.10 RouteGraph / Buffer / disabled station

- entry / terminal 必须存在且 enabled。
- edge / Buffer endpoint 必须存在且 enabled。
- terminal 必须从 entry 可达。
- stress WS20 disabled，不在 route/Buffer 中，terminal 为 WS19。

但 Buffer 合同字段 `enabled` 与 `tracking_mode` 未进入 model/schema/loader/YAML。

状态：`PARTIAL / HOLD`

### 5.11 Hardware envelope / static estimate

三份配置均输出：

| Config | Stations | Reads/s | Read bytes/s |
| --- | ---: | ---: | ---: |
| demo 3 | 3 | 6 | 384 |
| demo 10 | 10 | 19 | 1184 |
| stress 20 | 20 | 205 | 13440 |

同时输出 event rate 与 payload bytes/s。该结果是静态估算，不是 Raspberry Pi capacity
PASS。

状态：`PASS（静态输入）`

## 6. 测试命令与结果

### Contract Hardening 原始 focused suite

```bash
.venv/bin/python -m pytest -q tests/test_line_config.py
```

在 Verification 增补测试前：

```text
62 passed
```

### Verification 增补合同测试后

```bash
.venv/bin/python -m pytest -q tests/test_line_config.py
```

结果：

```text
74 passed, 2 failed
```

失败：

1. `test_explicit_null_station_nok_rate_uses_global_fallback`
2. `test_buffer_enabled_and_tracking_mode_are_preserved`

### 根级 tests

返修原始状态：

```text
73 passed
```

增补测试后：

```text
85 passed, 2 failed
```

失败均为上述 Sprint 1 合同问题，与 Phase-1 既有测试无关。

### API

```bash
cd api
../.venv/bin/python -m pytest -q tests
```

```text
5 passed
```

### Collector

第一次受限环境执行：

```text
11 passed, 1 failed, 3 subtests passed
```

唯一失败是 Snap7 集成测试无法绑定 `127.0.0.1` 临时端口：

```text
PermissionError: [Errno 1] Operation not permitted
```

获准环境重跑同一命令：

```text
12 passed, 3 subtests passed
```

### V-PLC

```text
27 passed
```

### Compileall

```text
PASS
```

### 三份 YAML

```text
demo_3_station.yaml    3 stations  PASS
demo_10_station.yaml  10 stations PASS
stress_20_station.yaml 20 stations PASS
```

Hash 与 Architecture 报告一致：

```text
f094e10efdb756b449e2654b9901282069ddde8a750d6ebc14d3722bae721678
12ede112b0bbfcec371fe3732e387875b301e27e7412310252c54cbfd61778ef
9d35425a7f50207ddeda9698d18d526a625f734c7fca9bf0e498e467176ad7e2
```

### Skip / xfail

pytest 输出未显示 skipped 或 xfail；测试源扫描未发现 skip/xfail marker。

## 7. 独立负例抽查结果

| 抽查 | 结果 |
| --- | --- |
| unknown top-level field | PASS，拒绝 |
| unknown nested station field | PASS，拒绝 |
| invalid station type | PASS，拒绝 |
| invalid profile mode | PASS，拒绝 |
| 21 stations | PASS，拒绝 |
| 5 DB mappings | PASS，拒绝 |
| unknown PLC reference | PASS，拒绝 |
| unknown payload template | PASS，拒绝 |
| unknown NOK template | PASS，拒绝 |
| reserved 30003 in random pool | PASS，拒绝 |
| Buffer references disabled station | PASS，拒绝 |
| route terminal disabled | PASS，拒绝 |
| invalid global NOK rate | PASS，拒绝 |
| invalid polling interval | PASS，拒绝 |
| YAML field order changed | PASS，hash 不变 |
| meaningful seed change | PASS，hash 改变 |

额外抽查：

| 抽查 | 结果 |
| --- | --- |
| explicit station `nok_rate: null` | FAIL，`TypeError: float(None)` |
| Buffer `enabled/tracking_mode` | FAIL，被 unknown-field validator 拒绝 |

## 8. 运行链路隔离审计

| 检查 | 结果 |
| --- | --- |
| V-PLC 导入/消费 `common.line_config` | 未发现 |
| Collector 导入/消费 | 未发现 |
| API 导入/消费 | 未发现 |
| DB / migration 修改 | 未发现 |
| Dashboard 修改 | 未发现 |
| Docker / `.env` / volume 修改 | 未发现 |
| 远程环境操作 | 未执行 |

Sprint 1 仍是纯本地配置基础，不影响 Phase-1 运行环境。

## 9. 文档一致性审计

通过：

- 规范路径均使用 `config/lines/`，未发现旧 `configs/lines/`。
- 未发现 TODO/TBD/FIXME 占位。
- 未把 Edge 描述为主动控制 Hold/Rework/Skip。
- stress 配置明确 `production=false`，未描述为真实生产默认。
- Dashboard/Grafana 只出现在“不修改/后续范围”，未混入 Sprint 1 实现。
- Hardening 报告的 62 passed 与 Architecture 原始结果一致。

不一致：

1. `docs/reports/sprint1_flexible_line_configuration_report.md` 仍写“57 项配置层测试”，
   Hardening 报告写 62 项；当前 Verification 增补后为 76 collected、2 failed。
2. `docs/contracts/line_configuration.md` 定义 Buffer `tracking_mode` / `enabled`，
   `docs/thread_handoff/architecture.md` 也把它列为 Hardening 范围，但实现未包含。

## 10. 是否需要远程部署

```text
NO
```

运行链路仍完全隔离。当前没有远程文件需要部署，且 Gate 为 HOLD。

## 11. 是否需要 rollback drill

```text
NO
```

没有 migration、Compose、`.env`、volume 或远程运行变更。

## 12. 是否建议 commit / push

```text
NO — HOLD
```

Architecture / Integration 应先修正：

1. 显式 null station NOK fallback。
2. Buffer `enabled/tracking_mode` 的合同、model、schema、loader、YAML 与测试一致性。
3. 更新 Sprint 1 报告测试数量。

修正后由 Verification 重跑 focused/root/API/Collector/V-PLC/compile/YAML/diff/status gate。

## 13. 未跟踪文件说明

当前：

```text
HEAD        4ce7aa00ff805925103ae9f1bfbe63142a074bbf
origin/main 4ce7aa00ff805925103ae9f1bfbe63142a074bbf
tag         phase1-pass-20260619
```

Sprint 1 仍未 commit / push。

旧文件：

```text
docs/Edge MES Demo 当前进度报告.md
```

仍为未跟踪文件，本 Thread 未修改、未暂存、未提交。后续提交必须继续显式排除。

## 14. 复验条件

1. 两个阻塞测试转绿。
2. `tests/test_line_config.py` 全部通过。
3. 根级 tests 无失败。
4. API / Collector / V-PLC 回归通过。
5. compileall、三份 YAML、hash/load summary、`git diff --check` 通过。
6. 运行链路继续保持隔离。
7. 文档测试数量和 Buffer 字段描述与实现一致。

满足后可再次评估 Sprint 1 PASS，并由 Architecture / Integration 执行精确范围的
docs + config + tests commit / push。

## 15. Architecture 定向返修记录

日期：2026-06-20
状态：两个 blocker 已完成最小修复，等待 Verification 轻量复验
Gate：仍由 Verification 保持 `HOLD`，本段不替代独立 Gate 更新

### Blocker 1：显式 null NOK fallback

- 根因：`dict.get("nok_rate", fallback)` 对显式 null 返回 `None`，随后
  `float(None)`。
- 修复：loader 对缺失或 null 统一使用 `scenario.global_nok_rate`；source
  `nok_rate` 仍保留为 `None`。
- focused evidence：
  `test_explicit_null_station_nok_rate_uses_global_fallback` 已通过。
- 非 null 非法 NOK rate 负例继续通过。

### Blocker 2：Buffer enabled / tracking_mode

- `schema.BUFFER_KEYS` 接受 `enabled`、`tracking_mode`。
- `BufferConfig`、loader、resolved config 和 hash 保留两个字段。
- `enabled` 缺省为 `true` 且必须是 boolean。
- `tracking_mode` 缺省为 `counter_only`，枚举为
  `unit_id/pallet_id/counter_only`。
- 显式 `enabled=false` 与 `tracking_mode=unit_id` preservation 测试已通过。
- 非法 tracking mode 与 unknown Buffer field 继续 fail closed。

### 当前 focused 结果

```text
77 passed
```

Architecture 完整回归：

```text
配置层：77 passed
根级：88 passed
API：5 passed
Collector：12 passed, 3 subtests passed
V-PLC：27 passed
compileall：PASS
三份 YAML / hash / load summary：PASS
git diff --check：PASS
运行链路 import scan：PASS，无接入
```

三份 YAML 的 resolved hash 因新增 Buffer resolved fields 按预期变化：

```text
demo_3_station.yaml    50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1
demo_10_station.yaml   08b9b4de701ef665597b0351240cc46d83ee649a5299f3db8551201d2a35dee5
stress_20_station.yaml e3afc329d76d559a3f211d088cfe2a749367a18774949db35d2af8a364a1fcfb
```

Architecture 建议 Verification 只对两项 blocker、上述回归证据和运行链路隔离做轻量复验。

## 16. Verification 最终轻量复验

日期：2026-06-20
角色：Verification，只读验证；未修改业务实现
最终结论：**PASS**

### 16.1 Blocker 关闭结果

| Blocker | 独立复验证据 | 结果 |
| --- | --- | --- |
| 显式 `station.nok_rate: null` fallback | null 与缺失字段均保留 source `None`，`effective_nok_rate` 均回退至 global；二者 resolved hash 相同；非法非 null 值仍失败 | CLOSED / PASS |
| Buffer `enabled/tracking_mode` | 默认值、显式 `enabled=false`、三种合法 tracking mode、非法 mode、非法 boolean 和 unknown field 均独立验证 | CLOSED / PASS |

focused 命令：

```bash
.venv/bin/python -m pytest -q tests/test_line_config.py \
  -k 'explicit_null_station_nok_rate or buffer_enabled_and_tracking_mode or \
  invalid_buffer_tracking_mode or invalid_nok_rates or unknown_fields'
```

结果：

```text
20 passed, 57 deselected
```

### 16.2 完整回归

| Gate | 结果 |
| --- | --- |
| 配置层 | `77 passed` |
| 根级 tests | `88 passed` |
| API | `5 passed` |
| Collector | `12 passed, 3 subtests passed` |
| V-PLC | `27 passed` |
| compileall | PASS |
| 三份 YAML load / resolved / estimate | PASS |
| `git diff --check` | PASS |

三份 YAML 新 hash：

```text
demo_3_station.yaml    50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1
demo_10_station.yaml   08b9b4de701ef665597b0351240cc46d83ee649a5299f3db8551201d2a35dee5
stress_20_station.yaml e3afc329d76d559a3f211d088cfe2a749367a18774949db35d2af8a364a1fcfb
```

独立反算时，仅从 resolved Buffer 删除 `enabled` 与 `tracking_mode`，即可逐一精确恢复
首次复验记录的三个旧 hash。因此 hash 变化只来自新增 resolved Buffer 合同字段。

### 16.3 Scope / isolation

- V-PLC、Collector、API 未导入或消费 `common.line_config`。
- DB schema / migration、Dashboard、Docker、`.env`、volume 无修改。
- `HEAD` 与 `origin/main` 仍为
  `4ce7aa00ff805925103ae9f1bfbe63142a074bbf`。
- tag 仍只有 `phase1-pass-20260619`。
- 未 commit、push、tag、deploy、远程重启或执行 rollback drill。
- `docs/Edge MES Demo 当前进度报告.md` 仍未跟踪，必须继续排除。
- 另有既存未跟踪 PM handoff 文档，不属于 Sprint 1 Gate 内容，提交时同样应使用精确
  allowlist 排除。

### 16.4 非阻塞文档观察

`sprint1_flexible_line_configuration_report.md` 仍保留“57 项配置层测试”的历史描述，
但已在同句明确以 hardening report 的 fresh verification 为准。当前权威计数为
`77 passed`。建议 Architecture 在 final commit 前把该句更新为当前计数，避免读者误解；
此项不影响配置行为、回归结果或 Gate PASS。

### 16.5 Final Gate

```text
Sprint 1 Gate: PASS
remote verification: NOT REQUIRED
rollback drill: NOT REQUIRED
```

建议 Architecture / Integration Thread 进入精确范围的 Sprint 1 final commit / push。
建议 commit message：

```text
Phase 2 Sprint 1 flexible line configuration
```
