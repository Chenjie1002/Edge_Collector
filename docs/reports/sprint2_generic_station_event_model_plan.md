# Phase-2 Sprint 2 Generic Station Event Model Plan

状态：planning freeze；PM 决策已固化，implementation not started

更新时间：2026-06-20

基线：`4215b7c Finalize Sprint 1 architecture handoff and review history`

## 1. 背景

Sprint 1 已交付并冻结 flexible line configuration：严格 YAML、immutable model、
resolved config、stable config hash、3/10/20 station examples 与 77 项配置层测试。
Sprint 1 Gate 为 PASS，implementation commit 为 `b9f6a69`，docs hygiene commit 为
`4215b7c`。

当前运行链路仍使用 Phase-1 既有 V-PLC / Collector / DB / API / Dashboard。本 Sprint
规划不会接入或改变该链路。

## 2. 上下文对齐说明

本轮以 `4215b7c` 和 Sprint 1 最终 Gate PASS 为当前状态。必读文件中仍保留部分历史
快照：

- `docs/thread_handoff/verification.md` 与
  `docs/reports/verification_context_restore.md` 仍含复验过程中的 `4ce7aa0`、HOLD
  片段。
- `docs/reports/sprint1_independent_gate_review.md` 同时保存初始 HOLD、blocker 发现与
  后续关闭证据，不能只读取中间段落判断当前 Gate。
- `docs/DOC_INDEX.md` 开头的“三工站当前协作范围”是 Phase-1 协作背景，不表示 Sprint 1
  flexible configuration 只能表达三站。

这些历史内容本轮不重写；Sprint 1 最终状态以 independent gate review 的最终 PASS
更新、Architecture handoff/context 和 commit `b9f6a69` / `4215b7c` 为准。

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

1. Architecture 按 PM 决策冻结 `station_event_model.md` 与本 planning report。
2. Reliability 审计控制边界、失败模式和幂等风险。
3. Data Quality 审计完整性、血缘和重复/迟到语义。
4. Verification 把冻结合同与前两份审计结论转成可执行 Gate matrix。
5. ChatGPT PM 汇总三方结论并决定是否授权 implementation。

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
| `unknown` 吞掉 malformed result | 数据质量被掩盖 | heartbeat/diagnostic 受控；正常 result reject |
| `30003` 被用于随机 NOK | 路由语义污染 | 独立 reserved rule |
| config hash 未知/不匹配 | 错配工站与模板 | reject/quarantine policy |
| payload 成为垃圾桶 | 查询和审计失控 | template strict + 16 KiB |
| raw payload 无上限 | 内存/存储风险 | type/encoding + 64 KiB |
| 重复与 out-of-order | 重复计数、假顺序 | deterministic identity + preserve timestamps |
| boot/profile 混用 | OEE/Trace 污染 | cycle event required fields |
| planning 被误认为 integration | 提前改 runtime | docs 明确 implementation not started |

## 9. Reliability 任务建议

Reliability review 应逐项判断：

- PLC/HMI/Edge authority 是否清晰，Collector 能否误造业务事实。
- MVP event type 是否足够小；defined-only 类型是否会被误当作 implemented。
- result/NOK/Skip 组合是否有歧义或 silent fallback。
- 独立 `nok_origin` 是否可被伪造，是否与 source/actor 发生矛盾。
- `30003` 是否只保护 upstream-NOK skip 语义。
- source/actor 是否能被伪造或滥用。
- config hash missing/unknown/mismatch 策略是否 fail safe。
- payload/raw payload 的类型、大小和深度是否有资源风险。
- timestamp、counter reset、out-of-order、duplicate/conflict 策略是否确定。
- 未来 retry、quarantine、DB unique key 是否会造成事实丢失。
- Sprint 1、Phase-1 import/runtime 是否完全隔离。

输出建议：独立 reliability review 报告，结论使用
`PASS / HOLD / CHANGES REQUIRED`，列出 blocker 与非阻塞建议。

## 10. Data Quality 任务建议

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
| Required fields | 全局与 conditional required 缺失 |
| Enum | event/result/source/actor 非法值 |
| Combination | event_type/result/nok_code/nok_origin 合法与非法矩阵 |
| Reserved NOK | `30003` allowed/forbidden 场景 |
| Authority | source/actor 可接受与越权组合 |
| Config correlation | station/plc/type/profile/hash match/mismatch |
| Identity | UUIDv4、UUIDv5 test-only、UUIDv7 compatibility、boot/counter/cycle_id |
| Time | UTC、malformed、out-of-order preservation |
| Payload | type、unknown、size、NaN、template |
| Raw | object/string/base64、encoding、size、preservation |
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
6. 第 16 节 PM 决策已经冻结，不再重新选型。
7. 先准备 Reliability review 输入；完成后依次交 Data Quality 与 Verification。
8. ChatGPT PM 未汇总三方结论并授权前，不得编写 implementation plan 或直接实施。

## 13. 建议 Gate 条件

Contract Gate：

- Reliability、Data Quality、Verification 均完成审阅。
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

- 五类 MVP event（cycle start/complete、result、NOK、heartbeat）各 2 个正例。
- required/unknown/type/enum 负例。
- event/result/NOK 组合表逐行正负例。
- `30003 + nok_origin=system_reserved` 至少 1 个合法、4 个非法来源/结果模式。
- `unknown` heartbeat/diagnostic 正例与正常 result/cycle complete 负例。
- source/actor authority 逐类覆盖。
- config identity/hash/profile/disabled station mismatch。
- payload/raw boundary 的 limit-1、limit、limit+1。
- duplicate/conflict/out-of-order fixtures。
- canonical ordering、round-trip、explicit null 与 absent。
- Sprint 1 77 项配置测试保持通过。

## 15. 文档冻结顺序

1. `docs/contracts/station_event_model.md`
2. Reliability review
3. Data Quality review
4. Verification Gate matrix
5. ChatGPT PM 汇总三方 review 并决定是否授权 implementation
6. Sprint 2 implementation plan（仅在获授权后）
7. model / validator / serializer / tests（仅在获授权后）
8. Sprint 2 implementation report
9. Independent Gate review

合同应先于代码；review 结论应先于 runtime 扩展。

## 16. PM 决策冻结

以下事项已裁定，不再作为开放问题：

1. 后续 implementation 路径为 `common/station_event/`；本轮不创建。
2. 保留独立 `station_nok`，并测试其与 `station_result(result=nok)` 的组合边界。
3. MVP event type 为 `station_cycle_start`、`station_cycle_complete`、
   `station_result`、`station_nok`、`station_heartbeat`。
4. model 使用 frozen dataclass；不引入 Pydantic 或重型 schema 依赖。
5. runtime 默认允许 UUIDv4；UUIDv7 为未来推荐；UUIDv5 仅用于 deterministic tests。
6. 所有有效 station event 强制携带 64 位 lowercase SHA-256 `config_hash`。
7. normalized payload / raw payload 上限分别为 16 KiB / 64 KiB，MVP 超限 reject。
8. `unknown` 只用于 heartbeat、未来 fault、明确 diagnostic/incomplete/unknown context
   和专用 fixture；禁止掩盖正常结果缺失或 malformed。
9. `nok_origin` 是独立字段，枚举为
   `random/forced/manual/plc/hmi/system_reserved/simulator/unknown`；不放入 correlation。
10. 必须依次完成 Reliability、Data Quality、Verification review，ChatGPT PM 汇总结论
    并授权后，才能开始 implementation。

### 强制审计顺序

```text
Architecture planning freeze
→ Reliability risk review
→ Data Quality semantic/lineage review
→ Verification Gate matrix
→ ChatGPT PM authorization decision
→ implementation（仅在授权后）
```

## 17. 当前状态与结论

本文件只完成 Sprint 2 planning。当前：

- Sprint 1 Gate：PASS。
- HEAD / origin/main 基线：`4215b7c`。
- Sprint 2 implementation：未开始。
- runtime integration：未执行。
- commit / push / tag / deploy / rollback drill：本轮均不执行。

下一步先交给 Reliability；随后 Data Quality，再由 Verification 建立 Gate matrix。
ChatGPT PM 未授权前不得生成或执行代码实施任务。
