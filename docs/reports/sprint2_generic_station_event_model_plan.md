# Phase-2 Sprint 2 Generic Station Event Model Plan

状态：Reliability N8 定向复验 `PASS WITH RECOMMENDATIONS`；N8 CLOSED；
implementation not started

更新时间：2026-06-21

Git 基线：`45fa2a8 Freeze Sprint 2 station event planning`

## 1. 背景

Sprint 1 已交付并冻结 flexible line configuration：严格 YAML、immutable model、
resolved config、stable config hash、3/10/20 station examples 与 77 项配置层测试。
Sprint 1 Gate 为 PASS，implementation commit 为 `b9f6a69`，docs hygiene commit 为
`4215b7c`。

当前运行链路仍使用 Phase-1 既有 V-PLC / Collector / DB / API / Dashboard。本 Sprint
规划不会接入或改变该链路。

## 2. 上下文对齐说明

本轮以 `45fa2a8` 和 Sprint 1 最终 Gate PASS 为当前状态。必读文件中仍保留部分历史
快照：

- `docs/thread_handoff/verification.md` 与
  `docs/reports/verification_context_restore.md` 仍含复验过程中的 `4ce7aa0`、HOLD
  片段。
- `docs/reports/sprint1_independent_gate_review.md` 同时保存初始 HOLD、blocker 发现与
  后续关闭证据，不能只读取中间段落判断当前 Gate。
- `docs/DOC_INDEX.md` 开头的“三工站当前协作范围”是 Phase-1 协作背景，不表示 Sprint 1
  flexible configuration 只能表达三站。

这些历史内容本轮不重写；Sprint 1 最终状态以 independent gate review 的最终 PASS、
implementation commit `b9f6a69` 和 docs hygiene commit `4215b7c` 为准。Sprint 2
planning freeze 已在 `45fa2a8` 提交。

## 2.1 Reliability N8 定向复验状态

`docs/reports/sprint2_station_event_reliability_review.md` 第 29~36 节记录第四轮
HOLD 历史，第 37~43 节记录当前 N8 定向复验，结论为
`PASS WITH RECOMMENDATIONS`。

第四轮已确认 CLOSED 且本轮不重新打开：

- UNKNOWN diagnostic context。
- Payload limits。
- Event required fields / presence-null / `profile_id`。
- N6 cycle-role uniqueness / content fingerprint。
- N7 stateful relation / detail-set constraints。

N8 已 CLOSED：`validated_nok_detail` evidence 已区分 detail 自身与 canonical parent
result comparison。

本轮只把 evidence comparison 按 type 拆分：

- `canonical_station_result` 比较 cited result 自身的 `result=nok`。
- `validated_nok_detail` 不比较 detail 自身 result；detail 必须 result absent，并解析
  accepted canonical parent `station_result(result=nok)`。
- 增加一组 official positive 与三组 negative examples。
- technical failure 继续禁止支持 `30003/UPSTREAM_NOK_SKIPPED`。

N6/N7 与既有 CLOSED items 无回归，未发现新 Reliability blocker。不扩大五类 MVP，
不创建 package、不修改 tests、不进入 implementation。

## 3. 从 Sprint 1 继承的能力

- `line_id`、`plc_id`、`station_id`、`station_type` 的配置身份。
- mapping、payload template、NOK template、cycle profile 与 route metadata。
- station-level NOK override、global fallback 与固定 simulation seed。
- reserved NOK code `30003` 的 `system_reserved` 约束。
- Buffer `enabled` / `tracking_mode`。
- resolved canonical JSON 与 SHA-256 `config_hash`。
- strict unknown-field rejection 与 fail-closed validator 风格。

## 4. 为什么需要 Generic Station Event Model

现有事件事实存在于多个协议和运行模块中。若直接接入更多工站，容易出现：

- 每站专用结构和查询分叉。
- result/NOK/Skip 语义漂移。
- boot/profile/config lineage 丢失。
- payload 无边界膨胀。
- Collector 被误用为生产控制决策者。
- 后续 DB/API/Dashboard 在合同未冻结时各自定义字段。

因此先冻结独立事件合同，再进入任何 runtime integration。

## 5. Sprint 2 MVP

PM 已批准后续实现使用独立 package：

```text
common/station_event/
  __init__.py
  models.py
  validator.py
  serializer.py
  errors.py
```

配套：

```text
tests/test_station_event.py
tests/fixtures/station_events/
docs/contracts/station_event_model.md
docs/reports/sprint2_generic_station_event_model_report.md
```

MVP 只包含：

- frozen dataclass model。
- 不引入 Pydantic 或重型 schema 依赖。
- event/result/source/actor enum。
- strict envelope validator。
- event-type/result/NOK/source-authority 组合校验。
- resolved line config correlation 校验。
- canonical dict / JSON serializer。
- positive/negative fixtures、snapshot 与 round-trip tests。

合同返修进一步冻结：

- `station_result` 是唯一 canonical production result carrier。
- `station_cycle_complete` 不携带 result。
- `station_nok` 是必须关联 canonical result 的 detail companion，不独立计数。
- physical cycle role 使用不含 config/cycle_id/source ID 的 `cycle_role_key`；
  NOK detail 使用 parent-scoped detail keys。
- `30003/system_reserved` 只在 strict accepted upstream business evidence 可解析时允许；
  technical failure 永远不能支持该 attribution。
- MVP 删除 system heartbeat；heartbeat boot identity 只能来自 PLC/V-PLC source。
- heartbeat 为 diagnostic-only，UNKNOWN 只允许 heartbeat 且必须有 strict
  `diagnostic_context`。
- source/actor/event/nok_origin 使用显式 allow matrix。
- `payload` 为 optional object；forbidden null 一律 reject；运行配置引用字段统一为
  `profile_id`。
- UUIDv4 只作为 event identity；`source_event_id` 只作来源追溯；`fact_key` 是
  config-aware identity，cycle/detail keys 承担 business uniqueness。
- content fingerprint 有官方 include/exclude、SHA-256 算法和 result/NOK vectors。
- MVP relation 缺失/state index 不可用一律 reject；defer/quarantine 仅 future。
- N8 evidence comparison 按 evidence type 执行；validated detail 的
  `upstream_result=nok` 与 canonical parent result 比较。
- payload/raw 增加深度、key、array、string、JSON type 和 raw encoding 限制。

## 6. 不纳入 Sprint 2 MVP

- Collector 或 V-PLC runtime adapter。
- PostgreSQL schema / migration / unique constraint。
- API endpoint、Dashboard、Trace Explorer。
- Buffer runtime event emission。
- fault/heartbeat 的 KPI 投影；`station_heartbeat` model 本身属于 MVP。
- Hold/Release/Rework 状态机和闭环。
- remote deployment、rollback drill、Phase-2 tag。

## 7. 建议实现路线

### Stage 0：合同 review

1. Architecture 已按 PM 决策冻结初版合同与 planning。
2. Reliability 已完成首轮审计，结论为 `HOLD / CHANGES REQUIRED`。
3. Architecture 按六个 blocker 返修合同与 planning。
4. Reliability 已完成 N8 定向复验并关闭全部 blocker。
5. 进入 Data Quality 审计完整性、血缘和重复/迟到语义。
6. Verification 基于通过 Reliability/Data Quality 审计的合同建立 Gate matrix。
7. ChatGPT PM 汇总并决定是否授权 implementation。

Reliability PASS 不等于 implementation 授权；仍须完成 Data Quality、Verification 与
ChatGPT PM authorization。

### Stage 1：测试骨架

1. 创建 `tests/test_station_event.py`。
2. 先写 model construction、enum、required field 和 strict unknown-field 失败测试。
3. 写 event/result/NOK 与 source/actor 组合负例。
4. 写 config correlation、round-trip、snapshot 和 size limit 测试。
5. 确认测试只依赖 `common.line_config`，不导入 runtime modules。

### Stage 2：最小独立实现

1. 定义 frozen models 和 enums。
2. 实现稳定 error code / field path。
3. 实现 validator 和 line config correlation。
4. 实现 canonical dict / JSON。
5. 增加 fixtures，并让 focused tests 通过。

### Stage 3：独立 Gate

1. 跑 station event focused tests。
2. 跑 Sprint 1 configuration tests 与 root regression。
3. 审计 import graph，确认没有 runtime integration。
4. 审计 diff scope、docs consistency 与 forbidden semantics。
5. Gate PASS 后只完成 Sprint 2 package closeout；runtime integration 进入后续独立
   Sprint。

## 8. 风险与边界

| 风险 | 影响 | 规划控制 |
| --- | --- | --- |
| Edge 根据测量值产生 NOK/Skip | 越过控制边界 | source/actor authority fail closed |
| event type 一次扩得过宽 | 合同失焦、测试爆炸 | MVP 只实现 cycle/result/NOK/heartbeat |
| `unknown` 吞掉 malformed result | 数据质量被掩盖 | 仅 heartbeat + strict diagnostic context；正常 result reject |
| `30003` 被用于随机 NOK | 路由语义污染 | 独立 reserved rule |
| technical failure 被归因为 upstream NOK | Edge 越过 PLC/HMI authority | 只接受 accepted upstream business evidence |
| config hash 未知/不匹配 | 错配工站与模板 | reject/quarantine policy |
| payload 成为垃圾桶 | 查询和审计失控 | JSON-only + depth/key/string/array + 16 KiB |
| raw payload 资源滥用 | 内存/存储风险 | json/utf8_text + 结构限制 + 64 KiB |
| 重复与 out-of-order | 重复计数、假顺序 | cycle-role/detail key + content fingerprint |
| result/NOK 多重投影 | OEE/Quality 重复计数 | physical production-result slot + detail-set rules |
| absent/null 漂移 | validator 对同一 envelope 得出不同结果 | strict presence matrix + canonical positive fixture |
| boot/profile 混用 | OEE/Trace 污染 | cycle event required fields |
| planning 被误认为 integration | 提前改 runtime | docs 明确 implementation not started |

## 9. Reliability 复验结论

Reliability 已定向复验 N8：

- `canonical_station_result` 是否比较 cited record 自身 `result=nok`。
- `validated_nok_detail` 是否保持自身 result absent，并比较 canonical parent
  `station_result.result=nok`。
- official positive example 是否可构造。
- detail 自带 result、parent result=ok、technical failure impersonation 是否全部 reject。
- N6、N7、UNKNOWN、payload limits、event required fields 是否未回归。

结论：`PASS WITH RECOMMENDATIONS`；N8 CLOSED，N6、N7 与既有 CLOSED items 无回归，
新 Reliability blocker 为无。

## 10. Data Quality 任务建议

可以开始正式 Data Quality review，审计 authority/outcome/idempotency 合同的完整性、
血缘和重复/迟到语义。该 review 不得修改 DB/migration，也不得被解释为 implementation
授权。

Data Quality review 应覆盖：

- 每类事件 completeness 和 conditional required fields。
- `event_id`、source event、cycle、unit、DMC 的 correlation。
- `plc_boot_id` + counter namespace 与 profile isolation。
- station sequence 只能基于明确 route/correlation，不能只靠时间邻近。
- `config_hash` lineage、station/type/template snapshot 可解释性。
- normalized/raw payload 的一致性、版本和重放证据。
- NOK reason、origin、reserved code 与多 code 扩展质量。
- duplicate、conflict、missing、late/out-of-order 的分类。
- invalid event quarantine 所需 reason/path/source evidence。
- Dashboard metric readiness 与“不完整数据不可冒充完整指标”。

输出建议：语义审计矩阵与最小追溯字段清单，不在本 Sprint 实现 Dashboard。

## 11. Verification 任务建议

Gate matrix 至少包含：

| 类别 | 必测项 |
| --- | --- |
| Construction | 每个 MVP event 的最小合法 model |
| Required fields | 全局与 conditional required、optional absent/null、forbidden null |
| Enum | event/result/source/actor 非法值 |
| Combination | per-event required/forbidden 与 event/result/NOK 合法、非法矩阵 |
| Reserved NOK | accepted upstream evidence；technical failure/missing/mismatch 全部 reject |
| Authority | source/actor/event/nok_origin allow matrix 全组合 |
| Config correlation | station/plc/type/profile_id/hash match/mismatch |
| Identity | cycle-role/detail keys、fact-key/content-fingerprint official vectors |
| Stateful | parent/evidence/config/state-index missing reject、result/detail duplicate/conflict |
| Time | UTC、malformed、out-of-order preservation |
| Payload | JSON type、depth、key、array、string、size、NaN、cycle reference、template |
| Raw | object/UTF-8 string、json/utf8_text encoding、结构、size、preservation |
| Serialization | canonical dict/JSON、round-trip、stable snapshot |
| Isolation | 不导入 Collector/V-PLC/API/DB/Dashboard |
| Regression | Sprint 1 config tests、root tests、compileall |
| Git/docs | allowed scope、diff check、contract/index consistency |

Sprint 2 Gate 不应以远程部署或 runtime API 验证为条件，因为这些明确不在 MVP。

## 12. 后续 Architecture Thread 任务建议

新 Architecture Thread 接手顺序：

1. 阅读 `docs/thread_handoff/architecture.md`。
2. 阅读 `docs/reports/architecture_context_restore.md`。
3. 阅读本 planning report。
4. 阅读 `docs/contracts/station_event_model.md`。
5. 重读 `docs/contracts/line_configuration.md` 与
   `docs/contracts/dynamic_station_model.md`。
6. 第 16 节 PM 决策及 Reliability 返修规则已经冻结，不再重新选型。
7. 第一任务是进入 Data Quality review。
8. Verification 可以开始建立合同 Gate matrix。
9. ChatGPT PM 未汇总审计结论并授权前，不得编写 implementation plan 或直接实施。

## 13. 建议 Gate 条件

Contract Gate：

- Reliability re-review 明确通过，六个 blocker 全部关闭。
- 随后 Data Quality 完成审阅。
- Verification 基于最终合同完成 Gate matrix。
- 第 16 节 PM 决策保持冻结，不被后续 Thread 静默改写。
- event/result/NOK/source/config/payload/idempotency 语义无 blocker。

Implementation Gate：

- 独立 package 与 tests 完成。
- focused、Sprint 1 regression、root tests、compileall 全部通过。
- canonical snapshots 稳定。
- negative matrix 覆盖所有 fail-closed rules。
- import/scope audit 证明未接 runtime。
- docs 与实现一致。

## 14. 建议测试矩阵规模

不以固定数字替代覆盖率，建议至少分组：

- 五类 MVP event（cycle start/complete、result、NOK、heartbeat）逐类最小正例。
- required/forbidden/unknown/type/enum 负例。
- authority matrix 与 event/result/NOK 组合表逐行正负例。
- `30003 + nok_origin=system_reserved` 至少覆盖合法 upstream business evidence，以及
  validation/rejected/malformed/missing/mismatch 等技术失败负例。
- `unknown` heartbeat + diagnostic context 正例，缺 context 与正常 result/cycle
  complete 负例。
- canonical result + primary/secondary/system-reserved details、duplicate/conflict、
  parent/evidence/state-index missing reject 和 detail-set fixture。
- config identity/hash/profile/disabled station mismatch。
- payload/raw size limit-1/limit/limit+1，以及 depth/key/array/string/type/encoding。
- event_id retry reuse、source identity trace-only、fact-key 与两个 official content
  fingerprint vectors。
- canonical ordering、round-trip、optional absent、optional null reject、forbidden null
  reject。
- Sprint 1 77 项配置测试保持通过。

## 15. 文档冻结顺序

1. `docs/contracts/station_event_model.md`
2. Reliability 首轮 review：HOLD
3. Architecture 第一轮 contract revision
4. Reliability 第二轮 re-review：HOLD
5. Architecture 第二轮最小 contract revision
6. Reliability 第三轮 re-review：HOLD
7. Architecture N5~N7 第三轮最小 contract revision
8. Reliability 第四轮 re-review：HOLD；N6/N7 CLOSED，N8 OPEN
9. Architecture N8 最小 contract revision（当前）
10. Reliability N8 定向复验：PASS WITH RECOMMENDATIONS；N8 CLOSED（当前）
11. Data Quality review
12. Verification Gate matrix
13. ChatGPT PM 汇总 review 并决定是否授权 implementation
14. Sprint 2 implementation plan（仅在获授权后）
15. model / validator / serializer / tests（仅在获授权后）
16. Sprint 2 implementation report
17. Independent Gate review

合同应先于代码；review 结论应先于 runtime 扩展。

## 16. PM 决策冻结

以下事项已裁定，不再作为开放问题：

1. 后续 implementation 路径为 `common/station_event/`；本轮不创建。
2. 保留独立 `station_nok`，但固定为 canonical `station_result` 的 detail companion；
   不独立产生 production outcome 或 Quality count。
3. MVP event type 为 `station_cycle_start`、`station_cycle_complete`、
   `station_result`、`station_nok`、`station_heartbeat`。
4. model 使用 frozen dataclass；不引入 Pydantic 或重型 schema 依赖。
5. accepted event identity 为 UUIDv4 且 retry 必须复用；`source_event_id` 只作 source
   trace；`fact_key` 是 config-aware identity，physical uniqueness 使用 cycle/detail
   keys。UUIDv7 为 future，UUIDv5 仅用于 validator 外部 helper/snapshot。
6. 所有有效 station event 强制携带 64 位 lowercase SHA-256 `config_hash`。
7. normalized/raw payload 上限为 16/64 KiB，并强制 JSON type、深度、key、array、
   string 与 raw encoding 限制，MVP 非法或超限 reject。
8. `unknown` 只允许 heartbeat，且必须有 strict `diagnostic_context`；正常 result/cycle
   complete 和 fixture 均不能绕过。
9. MVP `nok_origin` 为 `random/forced/plc/system_reserved/simulator`；manual/HMI/operator/
   unknown 延后。`system_reserved` 与 `30003` 双向绑定，并只接受 accepted upstream
   business evidence；technical failure 全部禁止。
10. 必须先完成 Reliability re-review 并通过；随后完成 Data Quality 与 Verification，
    ChatGPT PM 汇总结论并授权后，才能开始 implementation。
11. `payload` 是 optional object；MVP explicit null 均 reject；配置血缘字段统一为
    `profile_id=station.cycle_profile`。
12. stateless/stateful validation 必须保持可测试；MVP relation/config/state-index missing
    一律 reject，defer/future_quarantine 仅 future。
13. Pareto 固定为 distinct accepted defect-detail count，不是 NOK unit/cycle count。

### 强制审计顺序

```text
Architecture planning freeze
→ Reliability risk review: HOLD
→ Architecture first contract revision
→ Reliability second re-review: HOLD
→ Architecture second minimal contract revision
→ Reliability third re-review: HOLD
→ Architecture N5-N7 minimal contract revision
→ Reliability fourth re-review: HOLD, N8 only
→ Architecture N8 minimal contract revision
→ Reliability N8 focused re-review: PASS WITH RECOMMENDATIONS
→ Data Quality semantic/lineage review
→ Verification Gate matrix
→ ChatGPT PM authorization decision
→ implementation（仅在授权后）
```

## 17. 当前状态与结论

本文件只完成 Sprint 2 planning。当前：

- Sprint 1 Gate：PASS。
- HEAD / origin/main 基线：`45fa2a8`。
- Sprint 2 planning freeze commit：`45fa2a8`。
- Reliability N8 定向复验：`PASS WITH RECOMMENDATIONS`。
- CLOSED 且未退化：N6、N7、N8、UNKNOWN、payload limits、event required fields。
- 新 Reliability blocker：无。
- Sprint 2 implementation：未开始。
- runtime integration：未执行。
- commit / push / tag / deploy / rollback drill：本轮均不执行。

下一步进入 Data Quality review 与 Verification Gate matrix。两项 review 与 ChatGPT PM
authorization 完成前，仍禁止 implementation。当前文档可按精确 allowlist commit /
push。
