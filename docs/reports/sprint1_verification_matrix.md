# Phase-2 Sprint 1 Verification Matrix

> **历史 Review 说明**
>
> 本报告记录 Sprint 1 Contract Hardening 之前的 Verification matrix 与初始 Gate。
> 正文中的 blocker、gap 和 `HOLD / CHANGES REQUIRED` 均为历史证据，已由
> `sprint1_contract_hardening_report.md` 完成返修，并由
> `sprint1_independent_gate_review.md` 独立关闭。Sprint 1 最终 Gate：**PASS**。
> 当前状态以上述两份最终报告为准。

日期：2026-06-20
Thread：Verification
Sprint：Flexible Line Configuration
评审类型：配置层验收矩阵与实现审查
业务代码修改：无
远程操作：无
最终 Gate 建议：**HOLD / CHANGES REQUIRED**

## 1. 执行摘要

Sprint 1 已建立隔离的 YAML 配置加载基础：

```text
config/lines/*.yaml
→ common.line_config.load_line_config()
→ semantic validation
→ frozen dataclass tree
```

三个 3/10/20 工站示例均能加载，Phase-1 三站标识、DB101/102/103、DB104、cycle
baseline 和 NOK rate 得到基础回归。当前 Git 范围没有触碰 V-PLC、Collector、API、
数据库、migration、Dashboard、Docker、`.env`、volume 或远程环境，因此本 Sprint
不需要远程部署验证，也不需要 rollback drill。

但当前版本尚未满足 Sprint 1 最终配置 gate。Verification 临时负例证明以下错误配置会
被接受：

- 未受控的 `station_type`。
- 每 PLC 超过默认 20 站，只需把配置中的 `max_stations` 自行调大。
- 每站超过默认 4 个 DB mapping，只需把配置中的上限自行调大。
- 非法 `buffer_type`。
- 未知/拼写错误字段，加载后被静默丢弃。

此外：

- `cycle_profile.mode` 被 validator 校验，但未进入 `CycleProfile` dataclass。
- 20 站 stress 配置把 test 仿真时间和 OEE ideal cycle baseline 同时改为 5 秒。
- 当前 payload template 只有兼容类型，不能表达或验证合同要求的复杂 payload 字段。
- `BUF_WS19_WS20` 指向禁用的 WS20，尚无禁用站路线约束。

因此建议 Architecture / Integration 修正配置 fail-closed、默认上限和 Profile/模板
语义，补充负例后再进入 Sprint 1 最终 gate。不要因这些缺口提前接入运行链路。

## 2. 验收范围

本次验收：

- `common/line_config/` 的 YAML loader、dataclass 和 semantic validator。
- `demo_3_station.yaml`、`demo_10_station.yaml`、`stress_20_station.yaml`。
- 配置正例、负例、容量保护、引用完整性和 Buffer 基础语义。
- Phase-1 三站配置结构兼容。
- Git 变更范围与运行链路隔离性。
- Sprint 1 需要执行的本地回归等级。
- 是否需要远程部署和 rollback。

## 3. 不验收范围

本次不验收：

- V-PLC 或 Collector 实际消费 line config。
- 动态 read plan、payload 编解码、ACK 写回和多 PLC runtime。
- 数据库模型、migration、API、Dashboard 或 Grafana 运行行为。
- 10/20 工站真实运行性能、Raspberry Pi capacity envelope 或长稳。
- JSON Schema、resolved config、canonical JSON、config hash 的最终实现。
- field-level S7 offset/length/address overlap。
- route graph、分支、合流、Rework 或 Hold。
- 远程部署和 rollback。

这些能力进入后续 Sprint 或 Sprint 1 后续配置治理小步，不得从当前“YAML 可加载”推导
为已完成。

## 4. 状态定义

| 状态 | 含义 |
| --- | --- |
| PASS | 已执行并有直接证据 |
| PARTIAL | 有实现或间接覆盖，但缺少完整断言 |
| MISSING | 当前没有对应测试或实现 |
| FAIL | 实际探针证明不符合合同 |
| N/A | 当前隔离配置 Sprint 不需要执行 |

## 5. 配置加载验收矩阵

| ID | 验收项 | 当前证据 | 状态 | Gate |
| --- | --- | --- | --- | --- |
| CFG-LOAD-01 | `demo_3_station.yaml` 加载成功 | pytest 参数化加载，3 stations | PASS | 必须 |
| CFG-LOAD-02 | `demo_10_station.yaml` 加载成功 | pytest 参数化加载，10 stations | PASS | 必须 |
| CFG-LOAD-03 | `stress_20_station.yaml` 加载成功 | pytest 参数化加载，20 stations | PASS | 必须 |
| CFG-LOAD-04 | 返回 immutable dataclass tree | `FrozenInstanceError` 回归 | PASS | 必须 |
| CFG-LOAD-05 | station 按 `station_order` 稳定排序 | 三份配置排序断言 | PASS | 必须 |
| CFG-LOAD-06 | 文件不存在、YAML 语法错误、根节点非 mapping | validator 支持，当前目标测试未直接覆盖 | PARTIAL | 必须补测 |
| CFG-LOAD-07 | unknown field fail-closed | 临时探针加入 `unexpected_typo_field` 后仍成功加载 | FAIL | 阻塞 |

## 6. 配置校验验收矩阵

| ID | 负例 | 实现状态 | 测试状态 | 结论 |
| --- | --- | --- | --- | --- |
| CFG-VAL-01 | 缺少 `line_id` | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-02 | 缺少 PLC `plc_id` | 会拒绝 | 未直接覆盖 | 必须补测 |
| CFG-VAL-03 | 缺少 station `plc_id` | 临时探针会拒绝 | 未纳入 pytest | 必须补测 |
| CFG-VAL-04 | 重复 `plc_id` | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-05 | 重复 `station_id` | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-06 | 重复 `station_order` | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-07 | 非法/未受控 `station_type` | 匹配自定义模板后会被接受 | 无测试 | FAIL / 阻塞 |
| CFG-VAL-08 | 非法 NOK rate `<0` / `>1` / 非数字 | `>1` 已拒绝 | 只覆盖 `1.1` | PARTIAL，补边界 |
| CFG-VAL-09 | cycle time `<=0` / 非数字 | `0` 已拒绝 | 已覆盖零值 | PARTIAL，补负数/类型 |
| CFG-VAL-10 | payload template 引用不存在 | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-11 | payload template 类型不兼容 | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-12 | payload template catalog 非 mapping/兼容类型为空 | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-13 | NOK template 引用不存在 | 临时探针会拒绝 | 未纳入 pytest | 必须补测 |
| CFG-VAL-14 | NOK template 类型不兼容 | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-15 | NOK codes 为空/重复/非整数 | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-16 | cycle profile 引用不存在 | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-17 | cycle profile mode 非法 | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-18 | ideal cycle time 非法 | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-19 | Buffer 引用不存在 | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-20 | Buffer 自连接 | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-21 | Buffer position 不在上下游之间 | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-22 | Buffer capacity 非法 | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-23 | Buffer ID 重复 | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-24 | 非法 `buffer_type` | 临时探针 `teleporter` 被接受 | 无实现/测试 | FAIL / 阻塞 |
| CFG-VAL-25 | PLC 引用不存在 | 临时探针会拒绝 | 未纳入 pytest | 必须补测 |
| CFG-VAL-26 | 配置声明的 `max_stations` 被超过 | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-27 | 默认 20 站保护上限不可由配置自行放大 | 21 站 + `max_stations=21` 被接受 | 无实现/测试 | FAIL / 阻塞 |
| CFG-VAL-28 | 每站 mapping 数超过配置声明值 | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-29 | 默认每站 4 mapping 上限不可自行放大 | 5 mappings + limit=5 被接受 | 无实现/测试 | FAIL / 阻塞 |
| CFG-VAL-30 | mapping ID 重复 | 会拒绝 | 未覆盖 | 必须补测 |
| CFG-VAL-31 | 同 PLC DB number 冲突 | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-32 | station DB 与 runtime DB 冲突 | 会拒绝 | 已覆盖 | PASS |
| CFG-VAL-33 | runtime DB 在同一配置内重复/冲突 | station 冲突已覆盖；PLC 间 runtime 规则未明确测试 | PARTIAL |
| CFG-VAL-34 | DB number / runtime DB 非法值 | positive int validator 支持 | 未覆盖 | 必须补测 |

## 7. 向后兼容验收矩阵

| ID | 验收项 | 证据 | 状态 |
| --- | --- | --- | --- |
| COMP-01 | Phase-1 默认 Demo 行为不被破坏 | 三站 YAML 保留 LINE_001、PLC_001、DB101/102/103、DB104、cycle/NOK | PASS |
| COMP-02 | 当前运行流程未消费 line config | 运行模块扫描未发现 `common.line_config` / `config/lines` 引用 | PASS |
| COMP-03 | 未修改 V-PLC | Git scope 无 `s7_plc_sim/` 变更 | PASS |
| COMP-04 | 未修改 Collector | Git scope 无 `collector/` 变更 | PASS |
| COMP-05 | 未修改 API | Git scope 无 `api/` 变更 | PASS |
| COMP-06 | 未修改 DB / migration | Git scope 无 `db/` 变更 | PASS |
| COMP-07 | 未修改 Dashboard | Git scope 无 `config/grafana/` 变更 | PASS |
| COMP-08 | 未修改 Docker / `.env` / volume | Git scope无 Compose、env 或 volume 变更 | PASS |
| COMP-09 | 未修改远程部署 | 本 Thread 未执行 SSH、部署或服务重启 | PASS |
| COMP-10 | 不提交旧未跟踪进度报告 | `docs/Edge MES Demo 当前进度报告.md` 仍为未跟踪；必须继续排除 | PASS / 提交门禁 |
| COMP-11 | Phase-1 根级回归 | 本次独立重跑 `tests/`：32 passed | PASS |
| COMP-12 | API / Collector / V-PLC 回归 | Architecture 报告记录 5 / 12(+3) / 27 passed | PASS（引用交付证据） |

说明：COMP-01 当前证明的是“配置结构等价且运行链路未接入”，不是新 YAML 已与
Phase-1 `config/mapping.yaml` 形成完整 resolved read-plan 等价。

## 8. 边界验证矩阵

| ID | 边界 | 当前证据 | 状态 | Gate |
| --- | --- | --- | --- | --- |
| BND-01 | WS01~WS03 baseline | 三站身份、DB、cycle、NOK 精确断言 | PASS | 必须 |
| BND-02 | WS01~WS10 medium | 10 站、10 类型、2 Buffer 可加载 | PASS | 必须 |
| BND-03 | WS01~WS20 stress | 20 站、2 PLC、4 Buffer、多 DB mapping 可加载 | PASS | 必须 |
| BND-04 | disabled station | WS20 `station_enabled=false`；默认 true 有测试 | PARTIAL | 必须补语义 |
| BND-05 | station without optional payload | `payload_template=None` 已覆盖 | PASS | 必须 |
| BND-06 | station with complex payload template | 当前模板只有 compatible types，没有字段/schema/size | MISSING | 阻塞合同完整 gate |
| BND-07 | station with NOK template | 三份 YAML 有引用和兼容性基础验证 | PARTIAL | 补 codes/权限语义 |
| BND-08 | buffer before / after station | 位置约束已覆盖合法/非法 | PASS | 必须 |
| BND-09 | Buffer 指向 disabled station | stress Buffer 指向禁用 WS20，validator 不拒绝 | FAIL / 未决 | 阻塞 |
| BND-10 | PLC station limit | 仅验证自声明 limit，不保护默认 20 | FAIL | 阻塞 |
| BND-11 | station DB limit | 仅验证自声明 limit，不保护默认 4 | FAIL | 阻塞 |
| BND-12 | Profile mode 保留 | validator 校验 mode，dataclass 丢失 mode | FAIL | 阻塞 |
| BND-13 | stress baseline 与 simulation speed 分离 | stress ideal CT 和 station CT 都设为 5 秒 | FAIL | 阻塞 |

## 9. 必须通过项

Sprint 1 最终 gate 前必须满足：

1. 三份 3/10/20 工站 YAML 正例持续通过。
2. 所有必填标识、重复 ID/order、悬空引用和 DB 冲突负例进入 pytest。
3. 配置必须 fail-closed：
   - 拒绝 unknown field。
   - 拒绝非法枚举或完成受控 registry 验证。
4. `max_stations` 不得自行突破默认 20；提高上限必须有显式、可审计的 sizing override
   机制和 Verification 批准。
5. `max_db_mappings_per_station` 不得自行突破默认 4。
6. `CycleProfile` 必须保留 `mode`；工艺 ideal CT 与 simulation scale/base time 分离。
7. 明确 disabled station 与 Buffer/terminal route 的合法规则，并补测试。
8. payload/NOK template 至少达到 Sprint 1 已声明的结构边界，或合同和报告明确把复杂
   template 标为后续且不得声称当前已支持。
9. `stress_20_station.yaml` 不得用 test 加速值覆盖 OEE ideal cycle baseline。
10. `docs/Edge MES Demo 当前进度报告.md` 不得被纳入提交。

## 10. 可选项

以下可以不阻塞“最小配置基础”修正后的 gate，但应进入后续配置治理：

- JSON Schema 文件。
- canonical resolved JSON 与 config hash。
- 配置 diff 和 reload 生命周期。
- field-level S7 offset/length/address overlap。
- 负载估算与 Raspberry Pi capacity envelope。
- 完整 route graph、分支、合流和循环检测。
- 只读配置验证 CLI。

注意：这些项目如果继续在 Sprint 1 报告中作为已交付能力描述，就会从“可选/延期”变为
必须项。

## 11. 当前测试覆盖评价

当前结果：

```text
tests/test_line_config.py: 21 passed
root tests/: 32 passed
API: 5 passed（Architecture 交付证据）
Collector: 12 passed + 3 subtests（Architecture 交付证据）
V-PLC: 27 passed（Architecture 交付证据）
compileall: PASS
三份 YAML 加载: PASS
git diff --check: PASS
```

评价：

- 正例和基础引用/冲突校验覆盖良好。
- 21 个测试中，三份 YAML 和 Phase-1 baseline 证据可用。
- 负例数量和合同维度不足，当前不能支撑“严格配置基础”最终 gate。
- 现有测试主要证明“能加载”和“部分错误会拒绝”，尚未证明 fail-closed、默认硬上限、
  受控枚举、Profile 保真和复杂模板边界。

## 12. 必须补充的负例测试

最低补充集合：

1. 缺少 PLC `plc_id`。
2. 缺少 station `plc_id`。
3. 重复 PLC ID。
4. station 引用不存在的 PLC。
5. 未受控/非法 `station_type`。
6. unknown top-level、PLC、station、mapping、template、buffer 字段。
7. NOK rate：负数、1、0、非数字边界。
8. cycle time：负数、零、非数字。
9. payload template：不存在、类型不兼容、catalog 非 mapping、兼容类型为空。
10. NOK template：不存在、类型不兼容、codes 空/重复/非整数。
11. cycle profile：不存在、非法 mode、ideal CT 非法、mode 在 resolved object 中保留。
12. Buffer：悬空引用、自连接、重复 ID、非法 type、非法 capacity、指向 disabled
    terminal 的规则。
13. 21 站在没有批准 sizing override 时失败。
14. 每站 5 个 DB mapping 在没有批准 override 时失败。
15. mapping ID 重复、DB number 非法、runtime DB 冲突。
16. 未知字段不能静默加载。
17. stress Profile 不改变 OEE ideal cycle baseline。

## 13. 回归测试等级建议

| Suite | 本 Sprint 是否需要 | 理由 |
| --- | --- | --- |
| 本地 pytest：`tests/test_line_config.py` | 必须 | 配置层主 gate |
| 根级 `tests/` | 必须 | 防止共享包/import 和既有验收工具回归 |
| API tests | 建议必须 | 成本低，证明公共 Python 变更未污染 API |
| Collector tests | 建议必须 | 成本可控，保护 Phase-1 配置/依赖隔离 |
| V-PLC tests | 建议必须 | 成本可控，保护 Phase-1 baseline |
| compileall | 必须 | 新公共 Python 包基本门禁 |
| YAML 三文件独立加载 | 必须 | 正例资产门禁 |
| Acceptance Sprint | 不需要 | 配置未进入运行链路；完整 Sprint 会写入验收事件 |
| 远程部署验证 | 不需要 | 没有远程运行文件需要部署 |
| rollback drill | 不需要 | 没有部署、migration、Compose 或 volume 变更 |

若后续 diff 出现以下任一项，验证等级必须提高：

- V-PLC / Collector 导入 `common.line_config`。
- API、DB、Dashboard 消费新配置。
- migration、Docker、`.env`、volume 或远程文件变化。
- Phase-1 `config/mapping.yaml` / `config/vplc.yaml` 被替换。

## 14. 风险项

| 风险 | 等级 | 说明 |
| --- | --- | --- |
| 未知字段静默丢弃 | 高 | 拼写错误看似生效，运行对象实际没有该配置 |
| 默认 station / mapping 上限可自行放大 | 高 | 绕过合同保护与 Verification sizing gate |
| Profile mode 丢失 | 高 | 后续无法可靠隔离 normal/fast/test |
| stress ideal CT 被改成 5 秒 | 高 | test 数据可能污染 OEE Performance 口径 |
| station/buffer/purpose 任意字符串 | 高 | 消费者出现大小写、别名和未知分支 |
| payload template 过于骨架化 | 高 | 无法生成 read plan、校验地址或计算负载 |
| NOK template 语义不足 | 高 | SKIPPED code 可能被误用于随机/强制 NOK |
| Buffer 指向 disabled WS20 | 高 | 后续按 order 构建 runtime 时可能产生错误终点 |
| 双真源过渡 | 中 | 新 YAML 尚未与旧 mapping 形成 resolved equivalence |
| 20 站“可表达”被误解为容量证明 | 中 | 当前没有 Raspberry Pi 性能证据 |

## 15. 对 Architecture Thread 的修正建议

1. 优先实现严格 unknown-field rejection；如果 JSON Schema 延期，Python validator 也
   必须提供等价 fail-closed 行为。
2. 增加受控枚举/registry：
   - `station_type`
   - mapping `purpose`
   - `buffer_type`
   - cycle profile `mode`
3. 把默认保护上限与配置声明值分开：
   - `HARD_DEFAULT_MAX_STATIONS_PER_PLC = 20`
   - `HARD_DEFAULT_MAX_DB_MAPPINGS_PER_STATION = 4`
   - 高于默认值必须走显式 sizing override，不允许普通 YAML 自行放大。
4. `CycleProfile` 保存 `mode`，并明确：
   - `ideal_cycle_time_s` 是 OEE 工艺基线。
   - simulation base/jitter/scale 是 V-PLC 参数。
5. 修正 `stress_20_station.yaml`，保留工艺 ideal CT，用独立 test scale 表达加速。
6. 明确 disabled station 的路线语义；至少禁止 Buffer 把禁用站作为唯一终点。
7. 扩展 payload/NOK template 的最小结构，或收窄 Sprint 1 声明，避免把兼容类型目录
   误称为完整复杂模板。
8. 为 `30003 WS03_UPSTREAM_NOK` 等语义 code 增加随机/强制权限，避免误注入。
9. 补足本报告第 12 节负例后，再请求 Verification 复验。
10. 提交时显式排除旧未跟踪文件：

    ```text
    docs/Edge MES Demo 当前进度报告.md
    ```

## 16. 是否建议进入 Sprint 1 最终 Gate

当前建议：

```text
HOLD / CHANGES REQUIRED
```

理由：

- 配置层隔离性和正例基础合格。
- Phase-1 回归没有被破坏。
- 但 fail-closed、默认硬上限、受控枚举、Profile 保真、复杂模板和禁用站路线仍有
  合同级缺口。
- 这些问题在配置被 V-PLC/Collector 消费前修复成本最低；若带入 Sprint 3，会转化为
  运行可靠性与数据口径问题。

复验条件：

1. 阻塞项修正。
2. 必须负例进入 `tests/test_line_config.py` 或等价配置测试文件。
3. 配置层、根级、API、Collector、V-PLC、compileall、YAML load 和 diff check 全部
   通过。
4. 运行链路仍未接入时，继续不要求远程部署或 rollback。
