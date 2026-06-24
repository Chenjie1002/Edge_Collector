# Phase-2 Sprint 2 Station Event Reliability Review

日期：2026-06-21
Thread：Reliability
审计对象：Generic Station Event Model planning / contract
当前复验结论：`PASS WITH RECOMMENDATIONS`
implementation：未开始
业务代码、tests、runtime 修改：无

> 第 1~12 节保留 2026-06-20 首轮 Reliability HOLD 的历史证据。Architecture
> 返修后的独立复验结论见第 13 节起；首轮 finding 不应被误读为当前合同逐字状态。
> 第 13~19 节保留第二轮 Reliability HOLD 历史；第三轮详细复验见第 20~27 节，
> 第 29~36 节保留第四轮 N8 HOLD 历史；文件末尾 N8 定向复验为当前控制结论。

## 1. 审计范围

本次仅审计以下 planning / contract 是否足够安全、稳定、可实施：

- `docs/contracts/station_event_model.md`
- `docs/reports/sprint2_generic_station_event_model_plan.md`

上下文依据：

- `docs/thread_handoff/architecture.md`
- `docs/reports/architecture_context_restore.md`
- `docs/contracts/line_configuration.md`
- `docs/reports/sprint1_contract_hardening_report.md`
- `docs/reports/sprint1_independent_gate_review.md`
- `docs/reports/sprint1_reliability_config_review.md`
- `docs/DOC_INDEX.md`
- `docs/reports/README.md`

本次未修改合同、计划、代码、tests、migration、API、Collector、V-PLC、Dashboard、
Docker、`.env` 或远程环境。

## 2. 上下文确认

当前 Git 证据：

```text
HEAD        45fa2a89be9396f61cf9c3abfba132279021f7de
origin/main 45fa2a89be9396f61cf9c3abfba132279021f7de
latest      45fa2a8 Freeze Sprint 2 station event planning
tag         phase1-pass-20260619
```

- Sprint 1 Gate：`PASS`。
- Sprint 1 implementation commit：`b9f6a69`。
- Docs hygiene commit：`4215b7c`。
- Sprint 2 planning freeze commit：`45fa2a8`。
- Sprint 2 implementation：尚未开始。
- `common/station_event/`：不存在。
- Phase-2 tag：未创建。
- deploy / rollback drill：未执行。
- 本次活动：仅 Reliability review。

说明：Architecture handoff/context 和 Sprint 2 plan 正文中仍有 `4215b7c` 作为 planning
输入基线或旧 HEAD 的文字记录；实际 Git 状态已前进到 planning freeze commit
`45fa2a8`。这是文档收尾一致性问题，不改变本次合同风险判断。

## 3. 当前结论

合同具备以下优点：

- Edge 与 PLC/HMI 控制边界总体明确。
- MVP 和 future event_type 已分层。
- 缺失或 malformed result 禁止静默降级为 `unknown`。
- `config_hash`、boot/profile/counter 血缘意识完整。
- payload/raw payload 有明确总大小上限。
- `30003` 已禁止 random、forced、manual，并要求
  `nok_origin=system_reserved`。
- Sprint 2 package 与现有运行链路隔离。

但当前合同仍存在多处无法由 validator 确定性执行的 blocker。若直接进入
implementation，不同实现者可能分别定义 source authority、结果去重、diagnostic
context、heartbeat 字段、event identity 和 payload 安全规则，随后在 Collector、DB、
API 和 Dashboard 接入时形成不兼容语义。

因此：

- Contract Gate：`HOLD / CHANGES REQUIRED`。
- 可以继续 Data Quality review，帮助补齐血缘、重复、迟到和投影语义。
- Architecture 必须在 implementation 授权前修订合同。
- 当前仍禁止 Sprint 2 implementation。

## 4. Blocker Findings

### B1. `source` / `actor` authority 没有可执行许可矩阵

风险：

- 合同列出 source、actor 和原则，但没有定义每种 `event_type × source × actor` 的合法
  组合。
- `source=collector` 被纳入 MVP enum，但 Collector 只能产生 ingestion、validation、
  quarantine 技术元数据；这些又不是五类 MVP station event。
- `source=system` 可以产生 reserved semantic，但哪些 event_type、actor、NOK origin
  合法并不明确。
- `actor=hmi/operator` 与 source 的证据要求只有文字说明，validator 无法确定性执行。

证据位置：

- `station_event_model.md` 第 9 节，第 220–247 行。
- 第 13 节要求 validator 校验 authority 组合，但合同没有给出组合表。

影响范围：

- station_nok 的事实权威。
- reserved `30003` 的合法生产者。
- Collector 后续 normalizer。
- manual import、HMI、operator 审计。
- Verification negative matrix。

建议 Architecture 最小修复：

1. 增加规范的 source-event_type-actor allow matrix。
2. 明确 Collector 不得作为五类业务事实的 authority；若仅负责 envelope normalizer，
   保留原始 authority 字段，不能把 source 改写为 collector。
3. 明确 `system_reserved` 可由哪些 source/actor 组合产生。
4. MVP 不准备接入的 `manual_import/hmi/operator` 组合要么明确禁止，要么定义必要
   evidence 字段。
5. 非法组合必须 strict reject。

是否需要重新 review：`是`。

### B2. `station_cycle_complete`、`station_result`、`station_nok` 存在重复事实与重复计数

风险：

- `station_cycle_complete` 可以携带 `result` 和 `nok_code`。
- `station_result(result=nok)` 是规范结果事实。
- `station_nok` 又可与同周期的 NOK result 共存。
- 合同只写“通过 correlation 关联且不得重复计数”，但没有定义必须关联的字段、投影
  优先级、冲突处理或唯一性。
- 推荐幂等事实键包含 `event_type`，因此三种 event_type 会天然成为三个不同事实键，
  无法防止结果/NOK 被统计两次或三次。

证据位置：

- `station_event_model.md` 第 7.1 节，第 147–151 行。
- 第 8 节组合矩阵，第 186–205 行。
- 第 12 节推荐幂等键，第 298–301 行。

影响范围：

- Quality、FPY、NOK count、OEE Quality。
- cycle terminal state。
- DB projection 与 unique constraint。
- API、Dashboard、Trace timeline。

建议 Architecture 最小修复：

保留 PM 已冻结的独立 `station_nok`，但必须新增规范：

1. 指定唯一的 outcome authority，例如 `station_result`。
2. 明确 `station_cycle_complete.result` 与独立 `station_result` 的互斥或一致性规则。
3. `station_nok` 作为 detail/evidence event 时，必须引用规范 outcome event，例如
   `correlation.parent_event_id`。
4. 同周期多事件的 `result/nok_code/nok_origin` 必须一致；冲突时 reject 或标记 conflict，
   不得选择最后写入者。
5. 明确 quality projection 只计一次，`station_nok` 不额外增加 station outcome count。
6. 定义同一 cycle/result role 的事实唯一键和冲突规则。

是否需要重新 review：`是`。

### B3. `unknown` 的 diagnostic validation context 无法在合同字段中表达

风险：

- 正常 `station_result` 默认禁止 `unknown`，但“明确 diagnostic validation context”
  可以接受。
- 当前 envelope 没有 `event_class`、`diagnostic_context` 或等价字段。
- 如果 implementation 使用 validator 的外部布尔参数允许 `unknown`，同一事件在不同
  调用路径可能得到不同校验结果，容易被误用为绕过严格 result 校验。

证据位置：

- `station_event_model.md` 第 8 节，第 192、213–218 行。
- planning 第 16 节 PM 决策第 8 项。

影响范围：

- malformed/missing result 的 fail-closed 行为。
- fixtures 与 runtime 数据隔离。
- future fault/diagnostic 扩展。
- API 与 DB 对 UNKNOWN 的解释。

建议 Architecture 最小修复：

- Sprint 2 MVP 中将 `unknown` 限定为 `station_heartbeat`。
- 正常 `station_result` 和 `station_cycle_complete` 一律禁止 `unknown`。
- diagnostic/fault 场景待 future event contract 定义可验证字段后再开放。
- UUIDv5 fixture 或测试模式不能自动赋予业务字段放宽权限。

是否需要重新 review：`是`。

### B4. 每类 event 的必需字段不完整，`station_heartbeat` 的 diagnostic-only 边界不够硬

风险：

- 合同只说“周期相关事件”必须带 boot/profile/cycle 字段，但没有列出哪些 event_type
  属于周期相关。
- `station_heartbeat` 是否需要 `plc_boot_id`、profile、cycle_id、cycle_counter 不明确。
- heartbeat 被列为 MVP station event，但没有明确禁止参与 cycle count、OEE、Quality、
  terminal result 或生产控制判断。
- heartbeat 的 source/actor、payload template 和幂等身份也不明确。

证据位置：

- `station_event_model.md` 第 4 节，第 96–103 行。
- 第 8 节 heartbeat result 规则，第 194 行。
- 第 18 节又将 heartbeat KPI 和设备状态模型延后。

影响范围：

- model constructor 与 validator required matrix。
- heartbeat 高频数据量与去重。
- Dashboard/OEE 误计。
- Collector/DB 后续投影。

建议 Architecture 最小修复：

1. 增加 per-event required/forbidden field matrix。
2. 明确 heartbeat 为 `diagnostic-only`。
3. 明确 heartbeat 不产生 cycle、result、NOK、unit state 或 OEE/Quality 投影。
4. 明确 heartbeat 是否必须带 `plc_boot_id`，以及其独立序号/时间幂等规则。
5. 如果 Sprint 2 package 无法定义稳定 heartbeat identity，建议 model 词汇保留但将其
   implementation 降为 future。

是否需要重新 review：`是`。

### B5. UUIDv4 runtime 默认与重试幂等策略冲突

风险：

- runtime 默认允许 UUIDv4。
- `event_id` 可以由 source 或 normalizer 产生。
- 如果 normalizer 在每次重试时生成新的 UUIDv4，同一 source fact 会变成多个事件。
- 推荐事实键依赖 `source_event_id`，但 correlation schema 没有规定该字段对哪些 source
  必填，也没有规定稳定生成算法。
- UUIDv5 标记 test-only，无法用于 runtime deterministic identity；UUIDv7 future 也不
  解决 source fact 去重。

证据位置：

- `station_event_model.md` 第 6 节，第 124–129 行。
- 第 12 节，第 296–301 行。
- canonical example 的 `correlation.source_event_id` 不是规范 required 字段。

影响范围：

- Collector retry/restart。
- outbox replay。
- DB unique constraint。
- duplicate/conflict 分类。
- station_result/station_nok 关联。

建议 Architecture 最小修复：

1. 明确 `event_id` 在首次 normalizing 后必须持久复用，retry 不得重新生成。
2. 定义 `source_event_id` 对各 source 的 required/optional 规则和稳定算法。
3. 将 source fact identity 与 envelope instance identity 分开：
   - `event_id`：不可变 envelope identity。
   - `source_event_id` / `fact_key`：稳定 source fact identity。
4. 定义无法提供 source event ID 时，基于 boot/counter/event role 的确定性 fact key。
5. UUID version 只约束格式，不应承担业务幂等。
6. 明确相同 fact key、不同 event_id 的 duplicate/conflict 处理。

是否需要重新 review：`是`。

### B6. Payload 资源边界仍不足以安全实现

风险：

- 16 KiB / 64 KiB 总大小合理，但只限制最终 canonical 表示。
- 未限制 payload/raw object 的嵌套深度、key 数量、单 key/value 长度和允许的 JSON
  value 类型。
- 没有明确禁止 Python bytes、循环引用或自定义对象进入 model。
- `raw_payload` 可为 UTF-8 string 或 base64 string，但 `correlation.raw_encoding`
  本身没有 schema、枚举和必需规则。
- 深度异常对象可能在 size 计算前触发递归或高 CPU/内存消耗。

证据位置：

- `station_event_model.md` 第 11 节，第 265–286 行。
- 第 13 节只要求类型、编码和总大小。

影响范围：

- offline validator/serializer 的资源安全。
- future Collector memory。
- DB JSONB、API response 和日志。
- raw payload 被当作任意数据垃圾桶。

建议 Architecture 最小修复：

1. 定义 JSON-only 值类型，禁止 binary blob、自定义对象、循环引用。
2. 定义最大嵌套深度、最大 key 数、key 长度、string 长度和 array 长度。
3. 明确大小按 canonical UTF-8 encoded bytes 计算。
4. `raw_encoding` 使用受控枚举并对 raw type 条件必需。
5. base64 必须严格解码校验；同时考虑编码后和解码后上限。
6. 保留禁止 credential、secret、token、未脱敏 PII 的规则。
7. 所有超限/非法类型在 MVP strict reject，不截断。

是否需要重新 review：`是`。

## 5. 重点审计结论

### A. 控制边界

结论：`原则 PASS，执行规则 HOLD`。

- 合同明确 Edge 只记录、解析、校验、存储和展示，不决定 Hold/Release/Rework/Skip。
- `station_nok` 被描述为外部事实，不代表 Edge 判定 NOK。
- future Hold/Release/Rework 明确需要独立合同。
- 但 source/actor 没有 allow matrix，authority 无法由 validator 确定性执行。
- `station_heartbeat` 必须补充 diagnostic-only 与禁止业务投影规则。

### B. MVP event_type

结论：`五类可以保留，但必须收紧组合`。

- 不建议因本次审计直接删除 `station_nok`，因为 PM 已冻结其独立 detail/evidence 用途。
- 必须修复 `cycle_complete/result/nok` 三重结果事实的 authority、关联和去重。
- `station_heartbeat` 应明确 diagnostic-only；如不能定义稳定 identity，可降为
  future implementation。
- future event_type 当前已有“不实现 adapter/DB/Dashboard”的文字保护，建议再增加
  validator enum 不接受 future type 的明确条款。

### C. NOK 与 `30003`

结论：`reserved code 基础保护较好，但整体仍 HOLD`。

- `30003` 已要求 `nok_origin=system_reserved`。
- 已禁止 random、forced、manual。
- 因“只能与 system_reserved 组合”，plc/hmi/simulator/unknown origin 也应被拒绝。
- 仍需明确允许产生该 reserved event 的 source/actor 组合。
- `station_nok(result=skip)` 必须明确不计为质量 NOK outcome，避免 system reserved
  route semantic 污染 NOK Pareto/FPY。
- validator 必须直接禁止普通 NOK template/code 使用 `30003`。

### D. `UNKNOWN`

结论：`HOLD`。

- missing/malformed result strict reject 的方向正确。
- heartbeat 可允许 `unknown`。
- 正常 station_result/cycle_complete 应一律拒绝 `unknown`。
- 当前“diagnostic context”没有 envelope 字段，不能安全实现，应延后开放。

### E. source / actor / authority

结论：`HOLD`。

- source 表示 ingress authority，actor 表示触发主体，这一概念区分可保留。
- 必须增加 source-event_type-actor-nok_origin 许可矩阵。
- Collector 只能规范化/观察，不得成为 OK/NOK/Skip 的业务 authority。
- system 只能产生明确 reserved/diagnostic event。
- manual_import 不等于 manual NOK。
- HMI/operator 接入可延后，但不能留下宽松默认。

### F. config_hash / line config

结论：`PASS WITH REQUIRED CLARIFICATIONS`，不是单独 blocker。

- 所有有效 event 强制携带 config_version/config_hash 是合理且必要的。
- 64 位 lowercase SHA-256 hex 与 Sprint 1 resolved hash 一致。
- 缺失、格式错误：必须 model validation reject。
- 格式合法但未知、identity mismatch：
  - Sprint 2 离线 validator 在传入 resolved config 时应返回 correlation failure。
  - future Collector 才执行 quarantine，不得套用当前配置。
- 建议明确结构校验与 `validate_against_config()` 两阶段结果。
- event 必须同时保留 config_version，且 version/hash 必须来自同一 resolved snapshot。
- profile、station/plc/type、mapping/template 都应按同一 hash 校验。
- quarantine 是 future runtime 概念，本 Sprint 只定义错误分类，不实现队列或存储。

### G. payload / raw_payload

结论：`总大小合理，结构资源限制 HOLD`。

- 16 KiB normalized、64 KiB raw 对当前 Edge Demo 是保守且合理的初始上限。
- 大小应按 canonical UTF-8 encoded bytes 计算。
- 必须补齐嵌套、key/value、JSON type、base64 和循环引用规则。
- raw payload 不得包含 binary blob、凭据、密钥、Token 或未脱敏 PII。
- MVP 超限 strict reject；quarantine 延后。

### H. timestamp / ordering / idempotency

结论：`时间语义基本可用，幂等 HOLD`。

- event_ts / observed_at / created_at 分层清晰。
- out-of-order 允许且不得改写 event_ts，方向正确。
- 需要定义 future isolation 与 accepted event 的状态分类；Sprint 2 不实现存储。
- `cycle_counter` 应优先于 event_ts 排序，但 start/complete/result 在同 counter 内仍需
  event role/order 规则。
- UUIDv4 可作为 event ID，但不能作为唯一幂等策略。
- 必须补齐稳定 source fact identity 与 retry reuse 规则。

### I. implementation risk

结论：`规划结构正确，但当前禁止进入实现`。

后续获授权时建议：

- 使用 `common/station_event/`。
- 使用 frozen dataclass、enum、独立 validator、serializer、errors。
- fixtures 与 canonical snapshots 独立保存。
- model construction 不得绕过 validator。
- 不接入 Collector、API、DB、V-PLC 或 Dashboard。
- 运行 focused tests、Sprint 1 config regression、root regression 和 compileall。
- import graph 必须证明 package 只依赖标准库和 `common.line_config`。

## 6. 必须由 Architecture 修复的合同问题

按最小修复顺序：

1. 增加 per-event required/forbidden field matrix。
2. 增加 source × actor × event_type × nok_origin allow matrix。
3. 定义 cycle_complete/result/nok 的 outcome authority、关联、一致性和只计一次规则。
4. 将 MVP `unknown` 限定为 heartbeat；diagnostic/fault 延后。
5. 明确 heartbeat diagnostic-only、identity、required fields 和禁止业务投影。
6. 定义 event ID、source fact key、retry reuse、duplicate/conflict 的确定性规则。
7. 增加 payload/raw 的结构资源限制和 raw encoding schema。
8. 明确 future event_type 不进入 Sprint 2 validator accepted enum。
9. 明确 offline config correlation error 与 future runtime quarantine 的边界。
10. 明确 `30003` source/actor、projection exclusion 与普通 NOK template 禁用规则。

修订后需要 Reliability re-review。

## 7. Non-blocking Recommendations

按优先级：

### P1

- 将 `correlation` 本身定义为 strict object，至少规范：
  `source_event_id`、`mapping_id`、`payload_template`、`raw_encoding`、
  `parent_event_id`。
- 为 validation error 固定 error code，例如：
  `AUTHORITY_FORBIDDEN`、`RESULT_CONFLICT`、`CONFIG_HASH_MISMATCH`、
  `RESERVED_NOK_FORBIDDEN`、`PAYLOAD_TOO_DEEP`、`EVENT_ID_CONFLICT`。
- 明确 canonical content fingerprint 是否排除 `event_id`，避免用途混淆。

### P2

- 定义 timestamp 合理范围和未来时间容差；异常时分类，不改写 source timestamp。
- 明确 cycle start/complete/result 的事件角色顺序，不用时间邻近推断。
- 明确 disabled station 只允许哪些 diagnostic event。
- 对 `config_version`、profile、template version 使用同一 snapshot lineage。

### P3

- UUIDv7 保持 future recommendation，不进入 MVP 正例必要条件。
- manual import、HMI/operator 业务事件可以继续延后，避免一次扩张 authority。
- heartbeat 的频率、降采样和保留策略放到后续 runtime/DB 合同。

## 8. 对后续 Thread 的建议

### Data Quality

建议继续 review，并重点审计：

- canonical outcome 与 detail event 的投影规则。
- station_result/station_nok/cycle_complete 的去重与冲突。
- `30003` 是否排除 Quality NOK、FPY 和 Pareto。
- source fact key、event_id、cycle_id、unit_id、DMC 的血缘。
- duplicate/conflict/late/out-of-order 的分类。
- config snapshot lineage 与 unknown hash 语义。
- raw/normalized 一致性和重放证据。
- future DB unique key 能否支持事实去重而不丢失 evidence event。

Data Quality review 可以基于当前合同和本报告继续进行，但不得把当前合同视为已通过。

### Verification

建议在 Architecture 修订后建立 Gate：

- 每类 event 的 required/forbidden 字段矩阵。
- source/actor/event/nok_origin 全组合正负例。
- Collector/system 越权生成业务事实负例。
- cycle_complete/result/nok 一致、冲突和重复计数 fixtures。
- `30003` 合法 system_reserved 场景及所有其他 origin/source/result 非法场景。
- UNKNOWN heartbeat 正例；正常 result/cycle complete 全部负例。
- missing/malformed/unknown/mismatch config hash。
- UUIDv4 retry reuse、同 fact 不同 event_id、同 event_id 不同 content。
- payload/raw limit-1、limit、limit+1、深度、key 数、string、base64、NaN、binary、
  cycle reference。
- out-of-order preservation 与 event role ordering。
- Sprint 1 77 项配置测试、root regression、compileall 和 import isolation。

### Architecture

- 必须先修合同 blocker。
- 可以等 Data Quality review 完成后一次性合并语义修订，减少反复改合同。
- Verification Gate matrix 应基于修订后的合同，而不是当前 planning freeze 文本。

## 9. 是否建议进入 Data Quality review

`建议继续`。

原因：

- 当前是审计序列，不是 implementation 序列。
- Data Quality 对 outcome projection、血缘、duplicate/late/conflict 和 DB future key
  有独立价值。
- PM 可汇总 Reliability 与 Data Quality 意见后派回 Architecture 一次性修订。

限制：

- Data Quality review 不得把当前合同标记为 PASS。
- 不得开始 migration、DB model 或 Collector storage implementation。

## 10. 是否建议进入 implementation

`不建议，仍禁止`。

开始 implementation 前至少需要：

1. Architecture 完成第 6 节合同修订。
2. Reliability re-review 关闭 blocker。
3. Data Quality 完成语义/血缘 review。
4. Verification 建立修订后 Gate matrix。
5. ChatGPT PM 明确授权。

## 11. 文件与操作范围

本次新增：

- `docs/reports/sprint2_station_event_reliability_review.md`

本次未更新：

- `docs/DOC_INDEX.md`
- `docs/reports/README.md`

索引可在 PM 接收审计报告或 Architecture 合并修订时统一更新。

本次未执行：

- 代码或 tests 修改。
- `common/station_event/` 创建。
- migration / API / Collector / V-PLC / Dashboard 修改。
- commit / push / tag。
- deploy / rollback drill。
- Sprint 2 implementation。

## 12. 最终建议

- PM 是否应派回 Architecture 修订合同：`是`。
- 是否继续 Data Quality review：`是，仅继续审计`。
- 是否允许 Sprint 2 implementation：`否`。
- 当前 Contract Gate：`HOLD / CHANGES REQUIRED`。

## 20. 第三轮 Reliability Re-review（Architecture 第二轮返修后）

### 20.1 上下文与范围确认

本轮由新的独立 Reliability Thread 基于**当前本地工作树**复验，不以
`origin/main` 中尚未包含返修的文档作为审计对象。

已阅读：

- `docs/reports/sprint2_station_event_reliability_review.md`
- `docs/contracts/station_event_model.md`
- `docs/reports/sprint2_generic_station_event_model_plan.md`
- `docs/thread_handoff/architecture.md`
- `docs/reports/architecture_context_restore.md`
- `docs/contracts/line_configuration.md`
- `docs/reports/sprint1_contract_hardening_report.md`
- `docs/reports/sprint1_independent_gate_review.md`
- `docs/DOC_INDEX.md`
- `docs/reports/README.md`

Git 基线：

```text
HEAD        45fa2a89be9396f61cf9c3abfba132279021f7de
origin/main 45fa2a89be9396f61cf9c3abfba132279021f7de
tag         phase1-pass-20260619
```

Sprint 2 implementation 仍未开始；`common/station_event/` 不存在。本轮仅做合同
Reliability re-review，未修改合同、planning、handoff、代码、tests 或 runtime。

本轮使用三个只读 subagent：

1. Authority Evidence Auditor（Noether）：审计 `system_reserved/30003`、upstream
   evidence、system heartbeat 与 Edge authority 边界。
2. Production Result Key Auditor（Kepler）：审计 production result key、NOK detail
   key、duplicate/conflict 与统计去重。
3. Presence and Stateful Validation Auditor（Copernicus）：审计 presence/null/profile、
   fact-key algorithm、stateful interface 与 UNKNOWN/payload 回归。

subagent 只输出 findings，未修改文件，也未作最终 Gate 判断。以下结论由主
Reliability Thread 交叉核对后给出。

### 20.2 第三轮结论

```text
HOLD / CHANGES REQUIRED
```

一句话理由：presence/null 与已关闭的 UNKNOWN/payload 规则已经稳定，但
`30003` 的 authority evidence 仍可把技术失败解释成 upstream NOK，production-result
uniqueness/content comparison 仍未形成不可绕过的单一算法，且部分 stateful relation
规则存在互相冲突或无法在当前接口执行的约束。

## 21. 四个 OPEN blocker 第三轮复验

### 21.1 Authority matrix：OPEN

已关闭的部分：

- 五类 MVP event 已逐行列出 `source × actor × event_type × nok_origin` allow
  matrix；未列组合 fail closed。
- Collector 不在 accepted source/actor enum 中，不能直接成为五类业务 event
  authority。
- HMI、operator、manual import、API 与 manual NOK 明确为 future/non-MVP。
- `30003` 与 `system_reserved` 双向绑定；普通 NOK 不能使用 `30003`。
- system heartbeat 已限定为 observer diagnostic，`event_ts` 是 observation
  timestamp，并排除 cycle/result/OEE/FPY/Quality/NOK projection。

仍 OPEN 的证据与风险：

1. `upstream_event/source_event_reference` 明确要求解析为 accepted upstream
   `station_result(result=nok)`，但 `rejected_payload/validation_failure` 只需证明
   upstream station、subject 或 source-cycle relation；它们不证明 upstream NOK。
   合同仍允许 Edge 的 Collector/validator 证据支持
   `30003 UPSTREAM_NOK_SKIPPED`。这会把采集/校验技术异常升级为业务原因归因，即使
   `30003` 被排除生产指标，也仍越过了 PLC/HMI 对 Skip 原因的 authority 边界。
2. evidence station 必须位于 enabled upstream route，但合同未冻结 “upstream”
   是直接前驱还是任意有向祖先，也未定义分支路径 identity。不同 validator 可对同一
   route graph 得出不同 evidence 结论。
3. 所有 heartbeat 都 required `plc_boot_id`；system
   `collector_health/config_observation` 未定义该值是被观察 PLC、simulator 还是
   observer boot identity。PLC 不可达时存在猜测或冒用 production identity 的风险。

Architecture 最小修复：

- `30003` 只接受解析到 accepted upstream `station_result(result=nok)` 的证据；将
  rejected payload / validation failure 放入 heartbeat 或 future technical diagnostic，
  不得命名为 `UPSTREAM_NOK_SKIPPED`。
- 冻结 upstream route 的图语义；MVP 可收敛为“当前 resolved config 的直接 enabled
  前驱”，分支/祖先归因延后。
- 按 heartbeat category 明确 `plc_boot_id` target；无法确认 PLC identity 的 observer
  diagnostic 不得伪造 PLC boot。

残留风险：高。需要 Architecture 再修。

### 21.2 Result 去重：OPEN

已关闭的部分：

- `station_result` 明确为唯一 production result carrier。
- `station_cycle_complete` 禁止携带 result。
- `station_nok` 是 parent-bound detail companion，不额外增加 OEE、FPY、Quality 或
  NOK outcome。
- Result/NOK detail business key 已排除 `source_event_id`。
- NOK detail key 已固定为 parent/code/origin；相同 detail duplicate，不同 defect code
  可保留但不改变 parent result。
- `30003/system_reserved` 明确排除 Quality、NOK outcome 和 defect Pareto。
- 两个 SHA-256 official fact-key vectors 独立重算均匹配合同。

仍 OPEN 的证据与风险：

1. 合同要求“每 cycle 最多一个 accepted canonical result”，但 production-result
   business key 包含 `config_hash` 与 `cycle_id`，state index 只有
   `get_by_fact_key()`，没有独立的 cycle-role lookup。改变 key 中的 config identity
   即可绕过原 key；合同未定义同一 boot/counter 在 config transition/replay 时应
   conflict、reject 还是成为第二个 result。
2. 相同 fact key 的 duplicate/conflict 使用“canonical content 排除
   `event_id/source_event_id/observed_at`”，但未冻结被比较 object 的完整字段路径、
   nested `correlation.source_event_id` 删除规则或 official duplicate/conflict vectors。
   两个实现可能分别比较 envelope object、serialized bytes 或业务字段子集，得出不同
   disposition。
3. 合同允许同 parent 的不同 defect code，却要求“至少一个 detail 与 parent primary
   code 一致”。当前逐 event stateful 接口没有 cycle/detail-set finalization，也没有
   查询 parent 全部 details 的 lookup；因此无法在流式 accept 时确定未来是否会出现
   primary detail。

Architecture 最小修复：

- 冻结独立 cycle-role uniqueness tuple，例如
  `(line_id, plc_id, station_id, plc_boot_id, cycle_counter, event_role)`，并将
  `cycle_id/config_hash/result/NOK metadata` 纳入 conflict content；或在 state index
  增加等价 lookup 并冻结 config-transition disposition。
- 冻结 semantic fingerprint object、精确排除路径、canonical bytes/compare 算法及
  duplicate/conflict test vectors。
- 要求 primary NOK detail 先于其他 details accepted，或删除当前接口无法执行的
  “最终至少一个”集合约束并交给后续完整性审计。

残留风险：高。仍存在重复 result、实现间 disposition 漂移与 Pareto completeness
不一致风险。需要 Architecture 再修。

### 21.3 Event required fields：CLOSED

证据：

- 五类 event 均有 required/optional/forbidden matrix。
- `payload` 统一为 optional object；required null、optional null、forbidden null 均
  reject，absent 与 explicit null 不再混用。
- `created_at` 对 source envelope forbidden；`observed_at` optional。
- `profile_id` 明确对应 resolved station `cycle_profile`，不再与 profile mode 混用。
- `station_result` required result；cycle start/complete 禁止 result；
  `station_nok` required result/nok_code/nok_origin/correlation parent；heartbeat
  diagnostic-only。

残留风险：

- 文档中的 canonical example 是抽象示例，其 line/station/type/template/hash 不对应仓库
  当前三站 config。实现前应提供一个与 resolved config 逐字段匹配的 official positive
  fixture，避免把抽象示例直接当成可运行正例。

该残留属于 fixture hygiene，不重新打开本项。无需为 required-fields 规则再次返修；
可在 Architecture 本轮其他最小修复中顺手补齐。

### 21.4 Idempotency：OPEN

已关闭的部分：

- `event_id`、`source_event_id`、`fact_key` 三类 identity 职责已分离。
- runtime event identity 为 UUIDv4；retry/replay 必须复用；UUIDv5
  validator-external-only；UUIDv7 future。
- fact-key canonical JSON UTF-8 SHA-256 算法、字段排序、编码和两个 digest vectors 已
  冻结。
- stateless/stateful validator、state index 基本 lookup 与六种 disposition 已定义。

仍 OPEN 的证据与风险：

1. business dedupe key 本身可确定计算，但 duplicate/conflict 的 content fingerprint
   尚未同等冻结，故 stateful validator 仍不能保证跨实现给出同一 disposition。
2. 第 7.1 节写明 parent 缺失必须 reject/conflict；第 13.2 节又规定合法 reference
   尚未进入 state index 时 `defer + PARENT_NOT_AVAILABLE`。若前者意指字段 absent、后者
   意指 record not available，合同必须明说；当前文本对 “parent 缺失” 有两个可执行
   结果。
3. upstream evidence resolution 同样同时存在 unresolved => reject 与 record not yet
   available => defer 的表述，未冻结 lookup 的 not-found/not-yet-indexed 状态如何区分。
4. 当前 `state_index` 不足以执行 cycle-role uniqueness 和 primary-detail 集合约束。

Architecture 最小修复：

- 补齐 content fingerprint 的 deterministic algorithm/vectors。
- 将 parent/evidence 状态明确拆为：
  field absent、reference malformed、record not yet indexed、record definitively
  absent、record mismatch，并逐项冻结 disposition/error code。
- 增加 cycle-role/detail-set lookup，或删除当前接口不能执行的跨事件约束。

残留风险：高。需要 Architecture 再修。

## 22. 已 CLOSED 项回归确认

### 22.1 UNKNOWN diagnostic context：仍 CLOSED

- UNKNOWN 仍仅允许 `station_heartbeat`。
- strict `diagnostic_context` 的字段、category、reason、source 与格式限制仍在。
- production result、cycle complete 及 malformed/missing result 均不能降级为
  UNKNOWN。

未发现退化。

### 22.2 Payload limits：仍 CLOSED

- normalized payload 16 KiB、raw payload 64 KiB 上限保持。
- UTF-8 serialized bytes、最大深度、object/tree key、array item、key/string length、
  JSON-only type 与 raw encoding 规则保持。
- binary、image、base64、unbounded log 不在 MVP；超限统一 reject。

未发现退化。

## 23. 第三轮新发现 blocker

### N5. 技术失败仍可被 system 归因为 `UPSTREAM_NOK_SKIPPED`

风险：

Collector/validator 的 rejected payload 或 validation failure 不等于 PLC/V-PLC 已确认
upstream NOK。当前规则仍允许 Edge 生成带业务原因名称的 detail。

证据：

- `30003` 名称固定为 `UPSTREAM_NOK_SKIPPED`。
- evidence type 允许 `rejected_payload/validation_failure`，source 允许
  `collector/validator`。
- 只有 upstream event/reference 两类强制解析为 accepted
  `station_result(result=nok)`。

建议 Architecture 最小修复：

只让 accepted upstream NOK fact 支持 `30003`；技术异常使用 heartbeat/future
technical diagnostic。

### N6. Cycle-role uniqueness 与 content fingerprint 未完全冻结

风险：

仅依赖包含 config identity 的 fact key 不能明确处理同一 physical cycle 的 config
transition/replay；content comparison 也可能因实现选择不同而产生 duplicate/conflict
漂移。

证据：

- production-result key 包含 `config_hash/cycle_id`。
- state index 只有 fact-key lookup，没有 cycle-role lookup。
- content fingerprint 只描述排除字段，没有完整 canonical object/bytes vectors。

建议 Architecture 最小修复：

增加独立 cycle-role uniqueness lookup/tuple，并冻结 semantic fingerprint 算法与向量。

### N7. Stateful relation 的缺失状态与集合约束不可唯一执行

风险：

parent/evidence not found 可被实现为 reject 或 defer；“至少一个 primary NOK detail”
无法由当前逐 event 接口最终判定。

证据：

- 第 7.1 节 parent 缺失要求 reject/conflict，第 13.2 节 record not in index 要求 defer。
- evidence unresolved reject 与 evidence not available defer 未定义可区分的 lookup 状态。
- state index 没有 detail-set/finalization lookup。

建议 Architecture 最小修复：

冻结 relation lookup 的状态机和 disposition；增加必要 lookup/finalization，或删除无法
流式执行的集合约束。

## 24. Non-blocking Recommendations

1. 提供与真实 resolved config 对齐的 official positive fixtures；抽象 envelope 只用于
   schema 说明。
2. 为 ID、reason code、snake_case 与字段路径冻结精确正则。
3. 为 Unicode、边界长度、nested optional fields 增加 fact-key/fingerprint vectors。
4. 明确不同 defect code 的 Pareto 指标名称是“defect detail count”，不得被 Dashboard
   命名为 NOK unit/cycle count。
5. heartbeat frequency、downsampling、retention 继续留给 runtime/DB 合同。
6. 后续 DB/API/Dashboard projection contract 逐表标记 authoritative、derived、
   detail-only，并验证 `30003` 的排除。
7. UUIDv7、HMI/operator/manual import、DB unique constraint 与 quarantine storage
   继续保持 future，不进入 Sprint 2 合同实现范围。

## 25. 对后续 Thread 的建议

### Data Quality

```text
暂缓正式 review；仅可由 PM 明确授权只读预审
```

Authority、Result uniqueness 与 stateful relation 仍有 blocker，尚不能把当前合同交给
Data Quality 作为稳定统计语义基线。

### Verification

```text
暂缓正式 Gate matrix
```

可保留候选 negative cases，但 duplicate/conflict、parent/evidence disposition 与
`30003` authority 的 expected result 尚未唯一冻结，不能形成正式 Gate。

### Architecture

```text
需要再次最小合同返修
```

只需修复 N5~N7；不要重新打开已 CLOSED 的 UNKNOWN、payload limits 和 event presence
决策。

### Implementation

```text
仍禁止
```

不得创建 `common/station_event/`、tests、DB/API/Collector/V-PLC/Dashboard adapter，
不得进入 Sprint 2 implementation。

## 26. 第三轮文件与操作范围

本轮只修改：

- `docs/reports/sprint2_station_event_reliability_review.md`

未更新：

- `docs/DOC_INDEX.md`：已存在本报告入口。
- `docs/reports/README.md`：已存在本报告入口。

未修改合同、planning、handoff、业务代码、tests、runtime、DB schema、API、Collector、
V-PLC、Dashboard、Docker、`.env` 或 volume。

未执行 commit、push、tag、deploy、rollback drill，也未进入 Sprint 2 implementation。

## 27. 第三轮最终建议

- 是否建议 PM 派回 Architecture：`是，仅做 N5~N7 最小合同返修`。
- 是否建议继续 Data Quality：`否，暂缓正式 review；仅可只读预审`。
- 是否建议暂缓 Verification：`是`。
- 是否仍禁止 implementation：`是`。
- 四个上一轮 OPEN blocker：
  - Authority matrix：`OPEN`
  - Result 去重：`OPEN`
  - Event required fields：`CLOSED`
  - Idempotency：`OPEN`
- 回归项：
  - UNKNOWN diagnostic context：`CLOSED，无退化`
  - Payload limits：`CLOSED，无退化`
- 当前 Contract Gate：`HOLD / CHANGES REQUIRED`。

## 13. Architecture 返修后 Reliability Re-review

日期：2026-06-20

审计角色：Reliability

审计方式：主 Reliability Thread 汇总三个只读 subagent 的独立 findings，并回到当前
工作树合同逐项核验。subagent 未修改文件，也未作最终 Gate 判断。

使用的 subagent：

1. Authority Boundary Auditor：检查 source / actor / event / NOK authority 与 Edge 控制
   边界。
2. Result Dedup Auditor：检查 canonical result、NOK companion、fact key 与统计入口。
3. Validation Executability Auditor：检查字段矩阵、UNKNOWN、幂等、payload、时间和
   correlation 是否可确定性转化为 validator tests。

本轮审计基于 Architecture 当前未提交工作树，而不是只读取 `origin/main`。

### 13.1 上下文确认

```text
HEAD:        45fa2a8
origin/main: 45fa2a8
tag:         phase1-pass-20260619
Sprint 1:    PASS
Sprint 2 implementation: not started
Phase-2 tag: not created
deploy / rollback drill: not performed
```

本轮只做 Reliability re-review。未修改合同、planning、handoff、代码、tests、
runtime、DB、API、Collector、V-PLC、Dashboard、Docker 或远程环境。

### 13.2 Re-review 结论

```text
HOLD / CHANGES REQUIRED
```

一句话理由：Architecture 已关闭 UNKNOWN 与 payload 资源阈值等关键缺口，但 authority、
cycle-role 唯一性、字段 presence/null 语义和 stateful idempotency 仍存在无法由
validator 确定性执行的 blocker，直接实现仍可能产生 Edge 越权归因和结果重复计数。

## 14. 六个原始 Blocker 复验

### B1. Authority matrix：OPEN

已关闭部分：

- 五类 MVP event 均进入逐行 allow matrix。
- Collector 不再是 accepted source/actor，也不得改写原始 authority。
- HMI、operator、manual import、API 和 manual NOK 明确为 future/non-MVP。
- 普通 NOK 无法合法使用 `30003`；`30003` 与 `system_reserved` 双向绑定。

仍阻塞的证据：

- 第 2 节规定 Skip 与现场放行由 PLC/HMI 决定。
- 第 9 节却允许 `station_nok + source=system + actor=system + code=30003`。
- 该 system event 只需引用 `station_result(result=skip)`，没有上游 NOK event/evidence
  字段证明“本次 Skip 由上游 NOK 导致”。
- `station_heartbeat + system/system` 被允许用于 internal/config diagnostic，但
  `event_ts` 又被定义为 PLC/V-PLC 事实时间，`diagnostic_context.category` 也没有
  `internal/config`。

风险：

- Edge system 可把普通 PLC Skip 归因为 `UPSTREAM_NOK_SKIPPED`，越过“只记录事实”的
  控制边界。
- system heartbeat 的时间权威、boot 关联和 diagnostic category 无法确定性验证，
  可能伪装 PLC liveness。

Architecture 最小修复：

1. MVP 删除 `system/system station_nok(30003)`，只接受 PLC/V-PLC 明确提供的 reserved
   fact；或增加必须引用的 upstream NOK evidence，并明确其为 derived projection，
   不能冒充 source business fact。
2. 删除 system heartbeat，或拆为独立 technical diagnostic event，明确 system
   timestamp、target boot 关联和不可表示现场 liveness。
3. 将 `source` 从含糊的 “ingress context” 改为 originating fact authority；传输通道
   以后使用独立 metadata。

### B2. Result 去重：OPEN

已关闭部分：

- `station_result` 已明确为唯一 production result carrier。
- `station_cycle_complete` 已禁止携带 result/NOK。
- `station_nok` 必须引用 canonical result，且不进入 OEE、FPY、Quality、NOK outcome。
- future DB/API/Dashboard 的 production 统计入口已指向 accepted `station_result`。

仍阻塞的证据：

- 合同要求每 cycle 最多一个 accepted canonical result。
- result `fact_key` 却包含 `source_event_id`。
- duplicate/conflict 只对相同 `fact_key` 定义。
- 同 cycle、同 `production_result` role 只要使用两个不同的稳定
  `source_event_id`，就会生成两个不同 fact key，并可能同时 accepted。
- NOK detail fact key 同样包含 `source_event_id`；相同 parent/code 可被不同 source ID
  表达为多条 detail，重复进入 Pareto evidence。
- 第 7.1 节要求普通 detail 的单数 `nok_code` 与 parent 一致，第 12.3 节又允许同一
  result 有多个不同 detail code，二者不能同时满足。

风险：

- 同一 cycle 仍可能产生两个 accepted production result，重复计入 Quality、FPY、
  NOK outcome 和 OEE Quality。
- NOK detail/Pareto 仍可能重复，且多 code 的合法性无法确定。

Architecture 最小修复：

1. 冻结独立于 `source_event_id` 的 cycle-role uniqueness key，例如
   `(line_id, plc_id, station_id, plc_boot_id, cycle_counter, production_result)`。
2. 为 NOK detail 冻结 parent 下的逻辑唯一键，例如
   `(parent_event_id, nok_code, detail_role)`。
3. 明确 MVP 是单 NOK code，还是支持 code 集合；删除互相冲突的“一致”与“多 code”
   规则。

### B3. UNKNOWN diagnostic context：CLOSED

证据：

- `unknown` 只允许 `station_heartbeat`。
- heartbeat 强制 `diagnostic_context`。
- category、reason code、message 和 incomplete reason 已形成 strict object。
- `station_result`、`station_cycle_complete` 和 fixture/test mode 均不得放宽 UNKNOWN。
- missing/malformed production result 必须 reject，不能转换为 UNKNOWN。

残留风险：

- `reason_code` 建议冻结精确正则；`incomplete_reason` 建议明确 string/非空规则。
- credential/PII 禁止属于治理政策，不能仅靠通用 validator 完全自动证明。

上述残留项不重新打开 UNKNOWN blocker，但应进入 Verification negative matrix。

### B4. Event required fields：OPEN

已关闭部分：

- 五类 MVP event 已有 required / optional / forbidden 主矩阵。
- heartbeat 已明确 diagnostic-only，并排除 cycle、unit、result、OEE、Quality、FPY、
  NOK count 与控制投影。
- result/cycle/NOK 的基本组合已 fail closed。

仍阻塞的证据：

- 第 4 节把 `payload` 放入所有 event 的 common required fields。
- 第 4.2 节又把 `payload/raw_payload` 列入五类 event 的 optional 列。
- canonical 示例的 `station_result(result=ok)` 携带 `nok_code: null`、
  `nok_origin: null` 和 `raw_payload: null`；组合矩阵对非 NOK result 将 NOK 字段标为
  forbidden，raw 类型又只允许 object/string。
- serializer 规定保留有语义的显式 `null`，合同没有说明这些 null 是合法 presence、
  非法 presence，还是等价于 absent。
- `observed_at` 在可选字段和时间章节中出现，但未进入逐事件 optional matrix；
  `created_at` 也未被逐事件明确列为 source envelope forbidden。
- `profile` 未明确承载 Sprint 1 的 cycle profile ID，还是 profile mode；示例使用
  `normal`，而 resolved config 的 profile 引用可能是 `normal_screwdriving`。

风险：

- 同一个 envelope 可被不同 validator 分别接受或拒绝。
- canonical 示例本身可能无法通过合同。
- config correlation 无法确定 profile 应与哪个 resolved 字段比较。

Architecture 最小修复：

1. 明确 `payload` 是 required object（允许 `{}`）还是 optional；只保留一个定义。
2. 为所有 optional/forbidden 字段冻结 absent 与 explicit null 规则，并修正 canonical
   示例。
3. 将 `observed_at`、`created_at` 放入明确的 per-event/top-level allowlist。
4. 明确 `profile` 为 cycle profile ID 或 mode，并与 Sprint 1 resolved config 对齐。

### B5. Idempotency：OPEN

已关闭部分：

- `event_id`、`source_event_id` 与 `fact_key` 的职责已分离。
- retry/replay 必须复用 event ID。
- 相同 fact key / event ID 的 duplicate 与 conflict 已禁止 last-write-wins。
- UUIDv4 是 envelope identity；UUIDv5 仅 fixture/snapshot；UUIDv7 future。
- Sprint 2 明确不实施 DB unique constraint 或 Collector retry。

仍阻塞的证据：

- fact key 因包含 `source_event_id`，不能保证“每 cycle 一个 production result”和
  “相同 parent/code 一个 detail”的业务唯一性。
- “tuple 的 canonical JSON SHA-256”未冻结 JSON array/object 表示、Unicode 处理或
  official digest test vector。
- parent accepted、同 cycle 已有 result、同 fact key 历史 content、同 event ID 历史
  content 都是 stateful validation，但合同未定义 validator 接收 parent/index/batch
  context 的接口，也未定义 parent 尚未到达时 reject、defer 或 unresolved。
- 无原生 source ID 时的 boot-scoped role/sequence 没有冻结 sequence 来源、重启恢复和
  exact encoding；heartbeat 尤其没有 cycle counter。
- validator 被要求区分 UUIDv4 runtime 与 UUIDv5 test-only，但 envelope 中没有可信的
  runtime/test context。

风险：

- 不同实现者会产生不同 fact key。
- 单事件 validator 与带历史状态 validator 会给出不同结果。
- retry、out-of-order parent 和冲突分类仍可能漂移。

Architecture 最小修复：

1. 将 source fact identity 与业务 role uniqueness 分为两个明确 key。
2. 给 fact key 增加逐字节 canonical 算法和至少一个完整 digest test vector。
3. 定义 stateless envelope validation 与 stateful relation/idempotency validation 的
   接口、输入和 disposition。
4. 明确无原生 source ID 时每类 event 的稳定 ID 生成规则。
5. 将 UUID version 规则改成 envelope 可判定规则；不要依赖隐式 test mode。

### B6. Payload limits：CLOSED

证据：

- normalized payload：canonical compact JSON UTF-8 最大 16384 bytes。
- raw payload：JSON object 或 UTF-8 text，最大 65536 bytes。
- 最大深度 6，root object 计第 1 层。
- 单 object 最多 64 keys；全树最多 128 keys。
- key 最大 64 UTF-8 bytes；array 最多 128 items。
- normalized string 最大 4096 bytes；raw nested string 最大 16384 bytes。
- 只允许 JSON 类型，禁止 bytes、binary、base64、image、自定义对象、tuple/set、
  循环引用、NaN 和 Infinity。
- raw type 与 `raw_encoding=json/utf8_text` 条件绑定。
- validator 必须先做有界、循环安全遍历，再序列化并检查总大小。
- MVP 超限/非法类型直接 reject，不截断。

残留风险：

- payload template 到 normalized JSON type 的精确映射、`extensions` 声明方式和
  template 为空时的规则仍需 Data Quality / Verification 细化。

这些残留不影响资源上限本身的可测试性，因此 payload resource blocker 关闭。

## 15. 新发现的 Blocker

### N1. System reserved event 缺少可验证的上游业务证据

风险：

Edge system 可把 PLC 的普通 `result=skip` 解释成 `30003 UPSTREAM_NOK_SKIPPED`，形成
未经 PLC/HMI 证明的 route/business attribution。

证据：

- 控制边界规定 Skip 决策属于 PLC/HMI。
- authority matrix 允许 `system/system station_nok(30003)`。
- parent 只要求当前工站 `result=skip`，没有 upstream NOK parent/evidence。

建议 Architecture 最小修复：

- 删除该 system authority；或增加独立 derived-event contract 和强制 upstream NOK
  evidence，不把派生归因表示为 source station fact。

### N2. Cycle-role 与 NOK-detail 业务唯一键缺失

风险：

不同 `source_event_id` 可绕过当前 fact-key duplicate/conflict，导致同 cycle 多 result
和同 parent/code 多 detail。

证据：

- fact key 包含 `source_event_id`。
- duplicate/conflict 只比较相同 fact key。
- 合同同时声明每 cycle 最多一个 result、相同 detail role 不重复。

建议 Architecture 最小修复：

- 增加不含 source ID 的业务 role uniqueness key；source ID 只作为来源证据和 source
  retry identity。

### N3. Canonical envelope 与字段 presence/null 规则互相冲突

风险：

canonical 示例可能被严格 validator 拒绝，且 payload、NOK、raw、observed/created
字段的 required/optional/forbidden 结果不唯一。

证据：

- payload 同时出现在 common required 和 per-event optional。
- OK 示例保留 forbidden NOK null 字段和 raw null。
- serializer 要保留有语义 null，但未定义这些 null 的业务语义。

建议 Architecture 最小修复：

- 冻结 absent/null 规则、统一字段矩阵，并使 canonical 示例成为必须通过的官方 positive
  fixture。

### N4. Stateful validation 边界未形成可实现接口

风险：

parent、duplicate、conflict、cycle uniqueness 不能由单 envelope validator 判断；若
接口不冻结，实现会在 validator、repository、Collector 或 DB 之间任意分散。

证据：

- 合同要求 parent accepted 与历史 content 比较。
- planning 只列 `validator.py`，没有 relation context / index 输入或 disposition。

建议 Architecture 最小修复：

- 明确两阶段 validation：stateless envelope validation 与 stateful relation/
  idempotency validation；冻结输入、输出、错误码和 parent 未到达处理。

## 16. Non-blocking Recommendations

1. 为 `reason_code`、ID、snake_case 和字段路径冻结精确正则/格式。
2. 固定错误码优先级、多错误聚合顺序和 duplicate disposition；补充 enum/type/timestamp/
   unknown-config/cycle-role 错误码。
3. 为 fact key 提供 ASCII、中文 ID 和边界长度官方 test vectors。
4. 明确 V-PLC `forced` 只表示测试执行模式，不等于 operator authority；未来请求者审计
   使用独立 metadata。
5. heartbeat 频率、降采样、retention 继续留给 runtime/DB 合同。
6. UUIDv7 继续保持 future，不进入 MVP 正例必要条件。
7. 后续 DB projection contract 必须逐表标明 authoritative、derived、detail-only，并
   明确 legacy `production_snapshot`、`cycle_event`、`quality_event` 与新
   `station_result` 的迁移/兼容关系。
8. 接入前必须验证 Dashboard Pareto 排除 `30003/system_reserved`，不得直接复用当前
   所有 NOK code 的无差别计数。
9. payload template 到 JSON type、required field、extensions 和空模板行为交由 Data
   Quality 形成语义清单，再进入 Verification tests。

## 17. 对后续 Thread 的建议

### Data Quality

```text
暂缓正式 review
```

原因：当前 planning 已冻结为 Reliability re-review 通过后再进入 Data Quality；本轮仍有
authority、outcome uniqueness、presence/null 和 stateful validation blocker。若 PM 要求
并行，只能做只读预审，不能把结果作为 Contract Gate 或 implementation 授权。

### Verification

```text
暂缓正式 Gate matrix
```

原因：当前合同尚不能为 cycle-role uniqueness、null/presence、system reserved evidence
和 stateful validation 提供单一预期结果。可以保留负例清单，但不应冻结正式 Gate。

### Architecture

```text
需要再次最小合同返修
```

仅修订本报告 B1、B2、B4、B5/N1~N4 所列规则即可；无需重新打开已关闭的 UNKNOWN 和
payload resource limit 决策，也不应进入 implementation。

## 18. Re-review 文件与操作范围

本轮只更新：

- `docs/reports/sprint2_station_event_reliability_review.md`

本轮不需要更新：

- `docs/DOC_INDEX.md`：已包含本报告入口。
- `docs/reports/README.md`：已包含本报告入口。

未执行：

- 业务代码、tests、runtime、合同、planning、handoff 修改。
- `common/station_event/` 创建。
- DB schema / migration、API、Collector、V-PLC、Dashboard 修改。
- Docker、`.env`、volume 修改。
- commit、push、tag、deploy、rollback drill。
- Sprint 2 implementation。

## 19. Re-review 最终建议

- 是否建议 PM 派回 Architecture：`是`。
- 是否建议继续 Data Quality：`否，暂缓正式 review；仅可只读预审`。
- 是否建议暂缓 Verification：`是`。
- 是否仍禁止 implementation：`是`。
- 六个 blocker：
  - Authority matrix：`OPEN`
  - Result 去重：`OPEN`
  - UNKNOWN diagnostic context：`CLOSED`
  - Event required fields：`OPEN`
  - Idempotency：`OPEN`
  - Payload limits：`CLOSED`
- 当前 Contract Gate：`HOLD / CHANGES REQUIRED`。

## 28. 第三轮当前控制结论

本节覆盖第 1~19 节的历史状态；第三轮完整证据与最小修复见第 20~27 节。

```text
HOLD / CHANGES REQUIRED
```

- Authority matrix：`OPEN`
- Result 去重：`OPEN`
- Event required fields：`CLOSED`
- Idempotency：`OPEN`
- UNKNOWN diagnostic context：`CLOSED，无退化`
- Payload limits：`CLOSED，无退化`
- 新 blocker：N5~N7，见第 23 节。
- PM：建议派回 Architecture 做最小合同返修。
- Data Quality：暂缓正式 review，仅可只读预审。
- Verification：暂缓正式 Gate matrix。
- Sprint 2 implementation：仍禁止。
- 本轮仅修改本 Reliability 报告；未修改合同、planning、handoff、代码、tests 或
  runtime，未 commit、push、tag、deploy 或 rollback drill。

## 29. 第四轮 Reliability Re-review（Architecture 第三轮返修后）

日期：2026-06-21

### 29.1 上下文与审计范围

本轮由 Reliability Thread 基于当前本地未提交工作树复验 Architecture 对第三轮
N5~N7 finding 的合同返修；不以 `origin/main` 中的旧 planning freeze 文本替代当前
工作树。

已阅读：

- `docs/reports/sprint2_station_event_reliability_review.md`
- `docs/contracts/station_event_model.md`
- `docs/reports/sprint2_generic_station_event_model_plan.md`
- `docs/thread_handoff/architecture.md`
- `docs/reports/architecture_context_restore.md`
- `docs/contracts/line_configuration.md`
- `docs/reports/sprint1_contract_hardening_report.md`
- `docs/reports/sprint1_independent_gate_review.md`
- `docs/DOC_INDEX.md`
- `docs/reports/README.md`

Git 与实施边界：

```text
HEAD        45fa2a89be9396f61cf9c3abfba132279021f7de
origin/main 45fa2a89be9396f61cf9c3abfba132279021f7de
tag         phase1-pass-20260619
common/station_event/ absent
Sprint 2 implementation not started
```

本轮使用只读 subagent：

1. System Reserved Evidence Auditor（Dalton）：审计 N5 的 technical failure、
   `30003/system_reserved`、upstream business evidence、route/unit/boot/config 与
   heartbeat authority。
2. Cycle Role and Fingerprint Auditor（Hegel）：审计 N6 的 cycle/detail keys、
   fact key、content fingerprint、duplicate/conflict、official vectors 与 Pareto。
3. Stateful Relation Auditor（Wegener）：审计 N7 的 lookup/disposition、state index、
   primary/secondary/system-reserved detail set。
4. N5 Schema Consistency Auditor（Parfit）：在主 Thread 发现 schema 交叉矛盾后，定向
   复核 `validated_nok_detail` evidence 正例是否可构造。

subagent 仅输出 findings，未修改文件，也未作最终 Gate 判断。本节结论由主
Reliability Thread 汇总并对合同逐项交叉核验。

### 29.2 第四轮结论

```text
HOLD / CHANGES REQUIRED
```

一句话理由：N6 cycle-role/fingerprint 与 N7 stateful relation 已形成确定性合同，N5
的大部分 authority 风险也已关闭；但 `validated_nok_detail` evidence 同时要求 cited
`station_nok` 的 `result` absent 和等于 `nok`，导致该 accepted evidence type 没有合法
正例，validator 无法按单一规则实现。

## 30. N5~N7 第四轮复验

### 30.1 N5：OPEN

已关闭的部分：

- validation、schema、parse、payload-limit、ACK、config、clock、counter、storage 等
  technical failure 明确只能 reject 或进入 future technical diagnostic，不能支持
  `30003`、business NOK、production outcome 或 Skip attribution。
- upstream evidence type 已收敛为
  `canonical_station_result/validated_nok_detail`；Collector、validator、system
  technical record 不再是 business evidence。
- evidence 必须解析到 accepted、`source=plc/vplc` 的 upstream NOK fact，并逐项校验
  station、PLC、boot、direct enabled predecessor、unit/DMC 和 config hash。
- 只有 counter、无显式 unit/DMC 关联时禁止生成 `30003`。
- system heartbeat authority 已退出 MVP；MVP heartbeat 只接受 `plc/plc` 或
  `vplc/simulator`，boot identity 必须来自同一 source，且 heartbeat 不进入生产指标或
  控制投影。
- missing、not-found、unavailable、mismatch 均 reject，不再先接受或投影 `30003`。

仍 OPEN 的证据：

1. 第 4.2、8 节规定 `station_nok.result` forbidden/absent。
2. 第 12.1.1 节允许 `evidence_type=validated_nok_detail`，同时要求 evidence object 的
   `upstream_result` 固定为 `nok`。
3. 同节又要求 cited `station_nok` record 的 `result` 与 evidence object 逐字段相等。

因此：

- cited detail 不含 `result` 时，无法满足 `upstream_result=nok` 的逐字段相等；
- cited detail 携带 `result=nok` 时，又会被 per-event matrix 以
  `FIELD_FORBIDDEN` 拒绝；
- `validated_nok_detail` 被声明为 accepted evidence type，却不存在可通过全部规则的
  合法正例。

残留风险：高。不同 validator 只能选择忽略 comparison、违反 event matrix，或永久拒绝
该 evidence type，合同不可确定执行。

Architecture 最小修复：

- 按 `evidence_type` 冻结 comparison matrix：
  - `canonical_station_result`：直接比较 cited result 的 `result=nok`；
  - `validated_nok_detail`：cited detail 不比较 `result`，将
    `upstream_result=nok` 与该 detail 的 accepted canonical parent result 比较。
- 增加一个 `validated_nok_detail` official positive fixture 和 result/parent mismatch
  negative fixtures。

是否需要 Architecture 再修：`是，仅修上述 evidence type comparison`。

### 30.2 N6：CLOSED

证据：

- `cycle_role_key` 固定为
  `(line_id, plc_id, station_id, plc_boot_id, cycle_counter, event_role)`。
- `production_result_key = cycle_role_key`，并明确排除
  `config_hash/config_version/cycle_id/unit_id/dmc/source_event_id`；这些字段变化进入
  fingerprint conflict，不能创建第二个 accepted result。
- `station_nok_detail_key`、`primary_nok_detail_key` 和
  `system_reserved_detail_key` 已形成独立业务槽位。
- `fact_key`、physical business slot 和 `content_fingerprint` 的职责已分离。
- fingerprint 精确 exclude paths、included content、absent/null、timestamp、UTF-8
  canonical JSON 与 SHA-256 lowercase hex 已冻结。
- 相同槽位相同 fingerprint 为 duplicate；不同 fingerprint 为 conflict，MVP reject，
  不进入 projection 或 Pareto。
- 主 Reliability Thread 独立复算：

```text
station_result fact key:          PASS
station_nok fact key:             PASS
station_result content fingerprint: PASS
station_nok content fingerprint:    PASS
```

- Pareto 已固定为 accepted distinct non-system-reserved
  `defect_detail_count`；NOK unit/cycle count 只来自 canonical
  `station_result(result=nok)`。

残留风险：仅 non-blocking。后续 Verification 仍需验证实现同时执行 fact-key 与
cycle/detail-slot lookup，并补充 secondary/system-reserved/Unicode 边界向量。

是否需要 Architecture 再修：`否`。

### 30.3 N7：CLOSED

证据：

- required parent/evidence/config field missing、state index unavailable、lookup
  not-found、record mismatch 均有唯一 reject/error 规则。
- `defer/future_quarantine` 明确为 future-only，不属于 MVP accepted validator。
- state index 已覆盖 event、fact、cycle role、parent result、upstream evidence、
  detail set/detail key 与 resolved config lookup。
- lookup 状态固定为 `found/not_found/unavailable`，不再使用含糊 pending/unresolved。
- primary 必须匹配 parent canonical code/origin，且每个 parent 最多一个。
- secondary code 必须不同于 primary、origin 一致，并要求 accepted primary 已存在；
  否则 `PRIMARY_DETAIL_REQUIRED`。
- canonical NOK result 本身完整，不要求最终一定存在 detail，因此无需 batch
  finalization。
- `30003` 使用独立 system-reserved slot，每个 skip parent 最多一个，不属于
  primary/secondary production defect set，也不进入 defect Pareto。

残留风险：仅 non-blocking。实现时应使用 accepted-record snapshot，避免多个 lookup
在并发变化中读取不同状态；`lookup_detail_set()` 返回结构可在 implementation contract
中进一步命名化。

是否需要 Architecture 再修：`否`。

## 31. 已 CLOSED 项回归确认

### UNKNOWN diagnostic context：仍 CLOSED

- UNKNOWN 仍只允许 `station_heartbeat`。
- heartbeat 仍 required strict `diagnostic_context`。
- station result、cycle complete、missing/malformed result 不能降级为 UNKNOWN。
- system heartbeat authority 删除没有放宽 UNKNOWN；PLC/V-PLC heartbeat 组合仍
  fail closed。

未发现退化。

### Payload limits：仍 CLOSED

- normalized payload 16 KiB、raw payload 64 KiB 保持。
- UTF-8 byte 计算、depth/key/array/string、JSON-only、encoding、NaN/Infinity 和超限
  reject 规则保持。
- binary/base64/image/unbounded log 仍不属于 MVP。

未发现退化。

### Event required fields：仍 CLOSED

- 五类 event required/optional/forbidden matrix 保持。
- required/optional/forbidden 的 missing/null 规则保持 fail closed。
- `profile_id=resolved station.cycle_profile` 保持。
- cycle start/complete 禁止 result；station result required result；station NOK required
  parent/fact/detail role；heartbeat diagnostic-only。

未发现该 blocker 的规则退化。第 30.1 节的问题是 upstream evidence comparison 的新增
交叉矛盾，不重新打开通用 event required-fields finding。

## 32. 第四轮新发现 blocker

### N8. `validated_nok_detail` evidence 的 result comparison 不可满足

风险：

合同公开允许一种永远无法通过全部 validator 规则的 evidence type。实现可能静默忽略
`result` comparison、错误允许 `station_nok.result`，或永久拒绝该分支，造成不同实现
对同一 `30003` 证据给出不同结果。

证据：

- `station_nok.result` forbidden/absent。
- `validated_nok_detail` 是 accepted evidence type。
- evidence `upstream_result` required 且固定为 `nok`。
- cited record comparison 列表包含 `result`。

建议 Architecture 最小修复：

按 evidence type 拆分 comparison；detail evidence 的 `upstream_result` 应验证其
canonical parent result，而不是验证 forbidden 的 detail `result`。增加一组官方正负
例即可，不需要重新设计 authority、key 或 state index。

## 33. Non-blocking Recommendations

1. 为 `canonical_station_result` 与 `validated_nok_detail` 建立逐类型 evidence
   comparison table 与 fixtures。
2. Verification 增加跨 PLC、direct-predecessor、多直接前驱、unit/DMC mismatch、
   boot/config mismatch 和 technical-failure impersonation 负例。
3. 增加 secondary、system-reserved、Unicode 与边界长度 fingerprint vectors。
4. `fact_key` identity 表可将“参与 production uniqueness”改写为“不单独承担
   physical uniqueness”，避免脱离第 12.4 节误读。
5. 实现 stateful validator 时使用一致的 accepted-record snapshot，并对所有
   `not_found/unavailable` 分支做 table-driven tests。
6. 继续保持 `30003` 为 derived route diagnostic，不得被 Dashboard 命名为 production
   NOK outcome；Pareto 使用 `defect_detail_count`。
7. canonical example 与真实 resolved config 对齐仍建议在 implementation fixtures 前
   完成，但不阻塞 N5~N7 的本轮结论。

## 34. 对后续 Thread 的建议

### Data Quality

```text
暂缓正式 review；仅可只读预审
```

N8 修复后，Reliability 只需对 evidence comparison 做定向复验；通过后即可进入正式
Data Quality review。

### Verification

```text
暂缓正式 Gate matrix
```

可以准备候选 matrix，但 `validated_nok_detail` positive/negative expected result 尚未
唯一，不能冻结正式 Gate。

### Architecture

```text
需要一次极小范围合同修复
```

仅修 N8，不重新打开 N6、N7、UNKNOWN、payload 或 event required-fields。

### Implementation

```text
仍禁止
```

不得创建 `common/station_event/`、修改 tests 或接入 DB/API/Collector/V-PLC/Dashboard。

## 35. 第四轮文件与操作范围

本轮只修改：

- `docs/reports/sprint2_station_event_reliability_review.md`

未更新：

- `docs/DOC_INDEX.md`：已经存在本报告入口。
- `docs/reports/README.md`：已经存在本报告入口。

未修改合同、planning、handoff、业务代码、tests、runtime、DB schema、API、Collector、
V-PLC、Dashboard、Docker、`.env` 或 volume。

未执行 commit、push、tag、deploy、rollback drill，也未进入 Sprint 2 implementation。

## 36. 第四轮历史控制结论

本节保留第四轮 N8 HOLD 的历史控制结论；当前控制结论以第 43 节为准。

```text
HOLD / CHANGES REQUIRED
```

- N5：`OPEN`，仅剩 N8 evidence comparison blocker。
- N6：`CLOSED`。
- N7：`CLOSED`。
- UNKNOWN diagnostic context：`CLOSED，无退化`。
- Payload limits：`CLOSED，无退化`。
- Event required fields：`CLOSED，无退化`。
- 新 blocker：N8，见第 32 节。
- PM：建议派回 Architecture，仅修 N8。
- Data Quality：暂缓正式 review，仅可只读预审。
- Verification：暂缓正式 Gate matrix。
- Sprint 2 implementation：仍禁止。

## 37. N8 定向 Reliability Re-review

日期：2026-06-21

### 37.1 本轮范围

本轮只复验第四轮唯一剩余 blocker N8：

- `validated_nok_detail` evidence 是否保持 detail `result` forbidden/absent。
- `upstream_result=nok` 是否改为验证 accepted canonical parent
  `station_result.result`。
- `canonical_station_result` evidence 是否仍验证 cited result 自身。
- official positive 与三个 reject negative examples 是否有单一可执行结果。
- technical failure boundary 是否保持。

除检查 N8 修复是否直接造成回归外，本轮不重新打开 N6、N7、UNKNOWN diagnostic
context、payload limits 或 event required fields。

读取当前工作树：

- `docs/reports/sprint2_station_event_reliability_review.md`
- `docs/contracts/station_event_model.md`
- `docs/reports/sprint2_generic_station_event_model_plan.md`
- `docs/thread_handoff/architecture.md`
- `docs/reports/architecture_context_restore.md`

### 37.2 N8 定向结论

```text
PASS WITH RECOMMENDATIONS
```

N8 已关闭。evidence comparison 已按 evidence type 分开，`validated_nok_detail` 合法
路径与三个 reject 路径均有唯一结果；未发现 N6、N7 或既有 CLOSED items 回归。

## 38. N8 逐项复验

### 38.1 Detail 自身 result：PASS

- `station_nok.result` 在 per-event matrix 中仍为 forbidden。
- result combination table 仍要求 `station_nok.result=absent`。
- `validated_nok_detail` comparison 明确要求 cited detail 不存在 `result`，包括
  explicit null；出现时返回 `FIELD_FORBIDDEN`。

结论：detail 不再被要求携带或比较自身 result，原 N8 矛盾已消除。

### 38.2 Canonical parent result：PASS

- state index 必须通过 cited detail 的 `parent_event_id/parent_fact_key` 唯一解析 accepted
  canonical `station_result`。
- canonical parent 的 `result` 必须为 `nok`。
- evidence `upstream_result=nok` 明确与 canonical parent result 比较，而不是与 detail
  自身比较。
- detail 的 `nok_code/nok_origin/detail_role` 只表达 NOK detail 语义，不替代、不生成、
  不改写 parent production result。

结论：parent result authority 与 detail semantics 已分离且可确定执行。

### 38.3 Evidence lineage：PASS

`validated_nok_detail` 与 canonical parent 必须满足：

- accepted PLC/V-PLC authority。
- 同一 upstream station、PLC/V-PLC authority、boot、config 与 cycle role。
- upstream station 是 current station 的 direct enabled predecessor。
- upstream/current 存在逐字节相同 `unit_id` 或 `dmc`。
- 同 PLC 时 boot ID 相同；跨 PLC 时各自 boot ID 来自 cited source。
- 只有 counter、没有显式 subject identity 时禁止生成 `30003`。

结论：station、PLC/V-PLC、route、unit/DMC、boot、config 与 cycle-role 关联仍完整。

### 38.4 Canonical station-result evidence：PASS

`canonical_station_result` 分支仍直接验证 cited
`station_result.result=nok`；event、source、fact、station、PLC、boot、NOK code 与
config 必须与 evidence object 一致。

结论：N8 修复没有削弱 canonical result evidence。

### 38.5 Technical failure boundary：PASS

以下记录仍明确不是 upstream business evidence：

- malformed/rejected payload。
- schema/parse/validation failure。
- missing required field。
- payload-limit failure。
- Collector/validator/system technical record。

它们不能支持或生成：

- `30003`。
- `UPSTREAM_NOK_SKIPPED`。
- ordinary production NOK。
- operator/process defect。
- production outcome。
- defect Pareto entry。

结论：技术失败没有被升级为业务 NOK、Skip attribution 或 defect evidence。

### 38.6 Official examples：PASS

Positive：

- cited accepted primary NOK detail 自身 result absent。
- detail 解析到 accepted canonical parent `station_result(result=nok)`。
- evidence `upstream_result=nok` 与 parent result 比较。
- lineage 与共同关联规则一致时 accepted path 可构造。

Negative：

1. detail 自身携带 `result`：
   `reject / FIELD_FORBIDDEN`。
2. canonical parent 为 `station_result(result=ok)`：
   `reject / UPSTREAM_EVIDENCE_INVALID`。
3. technical failure 冒充 `30003/UPSTREAM_NOK_SKIPPED` evidence：
   `reject / UPSTREAM_EVIDENCE_INVALID`。

三个负例均有唯一、可测试的 reject 结果。

## 39. 回归确认

- N6 cycle-role uniqueness / content fingerprint：`CLOSED，无回归`。
- N7 stateful relation / detail-set：`CLOSED，无回归`。
- UNKNOWN diagnostic context：`CLOSED，无回归`。
- Payload limits：`CLOSED，无回归`。
- Event required fields：`CLOSED，无回归`。

本轮未发现新的 Reliability blocker。

## 40. Non-blocking Recommendations

1. 将第 12.1.2 节 pseudo example 在后续 Verification fixture 中展开为完整 envelope、
   cited detail、canonical parent、current skip event 和 state-index records。
2. 为 evidence object 中名为 `parent_event_id/parent_fact_key` 的 cited-record identity
   明确逐字段映射，避免实现者与 cited detail 自身的 parent fields 混淆。
3. Verification 使用 table-driven tests 覆盖 PLC/V-PLC、跨 PLC、boot/config、
   direct-predecessor 与 unit/DMC mismatch。
4. 继续保持 `30003` 为 system-reserved route diagnostic，不进入 production NOK、
   operator defect 或 `defect_detail_count`。

以上建议不阻塞 N8 关闭。

## 41. 后续 Gate 与操作边界

- Reliability 当前结论：`PASS WITH RECOMMENDATIONS`。
- N8：`CLOSED`。
- Architecture 无需再次返修 blocker；可由 PM 决定是否进行 docs-only 精确 allowlist
  commit / push。
- 可以进入 Data Quality review。
- 可以由 Verification 开始建立合同 Gate matrix。
- Data Quality / Verification review 与 ChatGPT PM 授权完成前，仍禁止 Sprint 2
  implementation。
- 仍禁止创建 `common/station_event/`、修改代码/tests/runtime、tag、deploy 或 rollback
  drill。

## 42. N8 定向复验文件与操作范围

本轮只修改：

- `docs/reports/sprint2_station_event_reliability_review.md`

未更新：

- `docs/DOC_INDEX.md`：已有本报告入口。
- `docs/reports/README.md`：已有本报告入口。

未修改 Architecture contract、planning、handoff、代码、tests、runtime、DB、API、
Collector、V-PLC、Dashboard、Docker、`.env` 或 volume。

未执行 commit、push、tag、deploy 或 rollback drill。

## 43. 当前控制结论

本节覆盖此前各轮 HOLD 历史，是当前 Reliability 控制结论。

```text
PASS WITH RECOMMENDATIONS
```

- N8：`CLOSED`。
- N6：`CLOSED`。
- N7：`CLOSED`。
- UNKNOWN diagnostic context：`CLOSED`。
- Payload limits：`CLOSED`。
- Event required fields：`CLOSED`。
- 新 Reliability blocker：无。
- PM 可以进入 docs-only 精确 allowlist commit / push 决策。
- 可以继续 Data Quality review 与 Verification Gate matrix。
- Sprint 2 implementation、tag、deploy、rollback drill：仍禁止。

---

## 44. Sprint 2 Reliability Focused Implementation Review

日期：2026-06-22
基线：`e9abe45 Finalize Sprint 2 station event review gates`
范围：只复验 implementation repair 后 B2～B4 的 parent / evidence / detail-set
可靠性语义；不重开完整 Sprint 2 review。

总结论：**HOLD**

Focused status:

- R-B2 30003 parent/evidence isolation：**OPEN**。cross-station、cross-cycle、future /
  non-result parent、缺失 evidence、technical-failure evidence 均已 fail closed；合法
  same-cycle skip parent 保持 non-production isolated，`30003` 不进入 ordinary
  defect、production NOK 或 Pareto。但独立变异探针确认，当前
  `station_nok(30003)` 可引用与 detail/current evidence 不同 `config_hash` 的 accepted
  `station_result(result=skip)` parent，仍返回 `accept`。parent relation 尚未完整绑定
  canonical config lineage，`parent/evidence mismatch fail-closed` 未完全关闭。
- R-B3 detail-set uniqueness：**CLOSED**。secondary 与 primary code 重复、secondary
  与已有 secondary code 重复均稳定
  `reject / DETAIL_CODE_DUPLICATE`；distinct secondary accepted；缺 primary 的
  secondary 保持 `PRIMARY_DETAIL_REQUIRED`。重复 detail 的 decision 不进入 projection，
  不产生 production NOK、ordinary defect 或 Pareto detail。
- R-B4 validated NOK detail parent semantics：**OPEN**。missing、OK、duplicate、
  conflict、rejected canonical parent 均已 reject；detail 自身 authoritative result
  仍 forbidden；direct predecessor 与 unit/DMC subject match 已执行。但 canonical
  parent 与 cited detail 之间只比较
  line/PLC/station/boot/cycle/counter/unit/DMC，未校验合同要求的
  `config_hash`、PLC/V-PLC source authority，以及 primary detail 的 canonical
  `nok_code/nok_origin` parent relation。独立探针分别将 parent 改为不同 config、
  不同合法 authority、不同 primary code，三种输入均错误返回 `accept`。

Blockers:

- R-B2：`_parent_matches()` 的 `30003` 分支未比较 parent/detail `config_hash`，导致跨
  config accepted skip parent 可支持 system-reserved detail。
- R-B4：`_evidence_error()` 解析 canonical parent 后未完整重放 ordinary
  `station_nok` parent relation；缺少 parent/detail config、source authority 与
  primary/secondary code-origin 语义校验。
- 当前 focused tests 未覆盖上述四个 fail-closed 负例。

Required Architecture repairs:

- 不需要修改已冻结合同语义。
- Implementation Thread 需做最小修复：
  1. `30003` current skip parent relation 增加 parent/detail `config_hash` 一致性。
  2. `validated_nok_detail` canonical parent 增加 parent/detail `config_hash` 与
     PLC/V-PLC source/actor authority 一致性。
  3. 对 cited primary detail，canonical parent 的 `nok_code/nok_origin` 必须完全一致；
     对 secondary detail，code 可不同但 `nok_origin` 必须一致。
  4. 增加对应 regression tests，并确认错误稳定为 `PARENT_EVENT_INVALID` 或
     `UPSTREAM_EVIDENCE_INVALID`。

Recommendations:

- 将 ordinary detail 的 parent matcher 抽成单一 relation helper，并由 current detail
  validation 与 `validated_nok_detail` evidence validation 共用，避免两条路径再次漂移。
- focused tests 增加 same-PLC boot mismatch、跨 PLC source authority、config mismatch、
  primary code/origin mismatch 与 secondary origin mismatch 的 table-driven matrix。
- 保留现有 B2 cross-station/cycle、B3 duplicate code、B4 missing/non-accepted parent
  与 technical failure fixtures。

Need Verification re-review:

- **yes**。最小 repair 后只需定向复验 R-B2 config-bound skip parent 与 R-B4 canonical
  parent full relation；无需重开 B1/B5 或完整 Sprint 2 review。

Need Data Quality review:

- **yes**。R-B4 直接影响 canonical parent lineage 与 evidence authority；本
  Reliability HOLD 关闭后，再完成既定 B1/B4/B5 focused Data Quality sign-off。

Eligible for implementation commit/push:

- **no**
- Conditions：关闭 R-B2/R-B4；新增 regression tests；focused/root tests、
  compileall、`git diff --check` 通过；Verification 与 Data Quality focused review 无
  blocker；ChatGPT PM 明确授权。

Scope checks:

- Collector/API/DB/Dashboard/V-PLC modified：**no**
- migration created：**no**
- tag created：**no**；当前仍只有 `phase1-pass-20260619`
- deploy：**no**
- rollback drill：**no**
- commit/push：**no**
- PM handoff / progress report / docs/superpowers staged or modified：**未 staged；仍为
  既有 untracked 内容，本 review 未修改**

Test evidence:

- compileall：**PASS**
- focused station_event：**107 passed in 0.06s**
- broader tests：root `tests/` **195 passed in 1.23s**
- git diff --check：**PASS**
- known unrelated failures：repo-root 无参数 pytest 在 collection 阶段仍有 **10 个
  `ModuleNotFoundError: app`**；属于既有 API/Collector/V-PLC 顶层 package layout，
  不计为本次 failure。

Independent focused evidence:

```text
B4_PARENT_CONFIG_MISMATCH accept None
B4_PARENT_AUTHORITY_MISMATCH accept None
B4_PRIMARY_PARENT_CODE_MISMATCH accept None
B2_SKIP_PARENT_CONFIG_MISMATCH accept None
B3_DUP_PROJECTION reject DETAIL_CODE_DUPLICATE False None
```

Files changed by this review:

- `docs/reports/sprint2_station_event_reliability_review.md`

Thread Health:

- 本 Thread 已完成的主要任务：读取指定报告、合同、implementation、tests 与 handoff；
  复验 B2～B4 contract-to-code-to-test 语义；运行 compileall、focused/root tests、scope
  checks；补做 parent/evidence/detail-set 独立变异探针；形成 focused Gate 判断。
- 当前上下文是否仍适合继续：**适合完成本轮 Reliability 收口；不适合直接修改
  implementation，因为本 Thread 被限定为只读 review。**
- 是否建议新开 Thread：**yes，交回 Implementation repair Thread，仅修上述
  R-B2/R-B4。**
- 如果建议新开，请给出 handoff 摘要：基线 `e9abe45`；Verification B1～B5 CLOSED，
  但 Reliability focused review 发现 B2 skip parent config lineage 与 B4 canonical
  parent config/authority/code-origin relation 仍可绕过；B3 CLOSED；只做最小
  validator + tests repair，不改合同、不接 integration；修复后回 Reliability /
  Verification 定向复验。
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：**低**。新 Thread
  应读取本节、Verification 第 33～37 节、implementation report 第 7～10 节，以及
  `validation.py` 的 `_parent_matches()`、`_evidence_error()`。

本轮未修改 implementation、tests、合同、handoff、Collector、API、DB、Dashboard 或
V-PLC，未 commit/push/tag/deploy/rollback drill。

## 45. 当前 Reliability 控制结论

本节覆盖第 43 节 planning-stage 控制结论，并作为 implementation focused review 后的
当前控制结论：

```text
HOLD
R-B2: OPEN
R-B3: CLOSED
R-B4: OPEN
```

在 R-B2/R-B4 最小 implementation repair、focused re-review、Data Quality review 与
ChatGPT PM 明确授权完成前，不具备 implementation commit/push 条件。

---

## 46. Sprint 2 Reliability Focused Re-review Result

日期：2026-06-22
基线：`e9abe45 Finalize Sprint 2 station event review gates`
范围：只复验 R-B2/R-B4 repair，并轻量确认 R-B3/B5 未回归。

结论：**HOLD**

Focused status:

- R-B2 30003 parent config_hash isolation：**CLOSED**。统一 parent matcher 已比较
  line/PLC/station/boot/cycle/counter/unit/DMC/config；parent 必须为 accepted、
  authoritative PLC/V-PLC `station_result(result=skip)`。同 station/cycle 但跨 config
  parent 稳定 `reject / PARENT_EVENT_INVALID`；合法 same-config skip parent accepted，
  但 `30003` projection 保持 non-production isolated。
- R-B4 canonical parent authority/config/code-origin relation：**仍 OPEN，仅剩 canonical
  role blocker**。config mismatch、PLC/V-PLC authority mismatch、primary code mismatch、
  primary/secondary origin mismatch、missing/non-accepted/OK parent 均稳定
  `reject / UPSTREAM_EVIDENCE_INVALID`；detail 自身 result 仍 forbidden，route 与
  subject lineage 保持。但 `_parent_matches()` 只检查
  `event_type=station_result`、result 与 source/actor，没有检查
  `correlation.event_role=production_result`。独立探针把 accepted parent 的
  `event_role` 改为 `cycle_complete` 后，`validated_nok_detail` 仍返回 `accept`。
  因此 compatibility/non-production role parent 仍可支持 validated NOK detail，不满足
  “accepted canonical production result parent” 的 fail-closed 要求。
- R-B3 duplicate detail-set regression：**CLOSED，无回归**。primary-secondary 与
  secondary-secondary duplicate code 仍返回 `DETAIL_CODE_DUPLICATE`；reject decision
  不产生 defect detail 或 production projection。
- B5 raw validation regression：**CLOSED，无回归**。PDF/base64 forbidden precedence
  与 periodic repeated substring smoke probes 均返回 `RAW_CONTENT_FORBIDDEN`；本轮未
  扩大 raw validation 审计。

Findings:

- 唯一 blocker：canonical parent relation 缺
  `correlation.event_role == production_result` 检查。
- 新增 `test_validated_nok_detail_rejects_non_authoritative_parent_roles()` 只改变
  `event_type` 为 cycle-complete/heartbeat，没有覆盖
  `event_type=station_result` 但 role 为 compatibility/non-production 的旁路。
- 已关闭 repair 未发现退化：R-B2 same-config isolation、R-B4 config/authority/
  code-origin、R-B3 duplicate detail-set、B5 raw validation 均符合预期。

Tests:

- git status：基线仍为 `e9abe45`；working tree 有既有未提交 implementation/tests/
  reports 与 `.gitignore` 修改；本 review 开始前即存在。
- compileall：**PASS**
- focused station_event：**114 passed in 0.09s**
- broader tests：root `tests/` **202 passed in 2.79s**
- git diff --check：**PASS**
- unrelated failures：repo-root 无参数 pytest 在 collection 阶段仍有 **10 个
  `ModuleNotFoundError: app`**，属于既有 API/Collector/V-PLC 顶层 package layout，
  不计为本轮 failure。

Independent focused evidence:

```text
RB2_CROSS_CONFIG_SKIP_PARENT reject PARENT_EVENT_INVALID False None
RB2_VALID_SAME_CONFIG accept None False None
RB4_PARENT_CONFIG reject UPSTREAM_EVIDENCE_INVALID False None
RB4_PARENT_AUTHORITY reject UPSTREAM_EVIDENCE_INVALID False None
RB4_PRIMARY_CODE reject UPSTREAM_EVIDENCE_INVALID False None
RB4_PRIMARY_ORIGIN reject UPSTREAM_EVIDENCE_INVALID False None
RB4_SECONDARY_VALID accept None False None
RB4_SECONDARY_ORIGIN_MISMATCH reject UPSTREAM_EVIDENCE_INVALID False None
RB4_COMPATIBILITY_ROLE_PARENT accept None False None
RB3_DUPLICATE_CODE reject DETAIL_CODE_DUPLICATE False None
B5_PDF False [('RAW_CONTENT_FORBIDDEN', 'raw_payload.payload')]
B5_PERIODIC False [('RAW_CONTENT_FORBIDDEN', 'raw_payload.message')]
```

Files changed by this review:

- `docs/reports/sprint2_station_event_reliability_review.md`

Scope audit:

- implementation code modified：**no**
- tests modified：**no**
- contracts modified：**no**
- Collector/API/DB/Dashboard/V-PLC modified：**no**
- migration created：**no**
- tag created：**no**；仍只有 `phase1-pass-20260619`
- deploy：**no**
- rollback drill：**no**
- commit/push：**no**

Decision:

- Remaining Reliability blocker：**yes，仅 R-B4 canonical parent role**。
- Need Architecture repair：**yes，最小 implementation repair**。在统一 parent matcher
  中要求 canonical parent `correlation.event_role=production_result`，并增加
  compatibility/non-production role negative test；预期错误
  `UPSTREAM_EVIDENCE_INVALID`。
- Need Verification targeted re-review：**yes**。修复后只做 parent-role 定向 sanity
  re-review，不重开 B1/B5 或完整 Verification。
- Need Data Quality focused review：**yes，但不得在本 Thread 扩大执行**。Reliability
  blocker 关闭后按既定流程完成 B1/B4/B5 focused sign-off。
- Eligible for implementation commit/push：**no**。即使下一轮 Reliability PASS，也
  必须等待 Data Quality focused sign-off，并由 ChatGPT PM 对 Architecture /
  Integration Thread 单独给出精确 allowlist 授权。

Thread Health:

- 本 Thread 已完成的主要任务：读取指定 implementation/tests/report/handoff；审计统一
  parent matcher 与 evidence path；复现 114/202 tests；重放 R-B2/R-B4 旧绕过；
  独立检查 secondary origin、compatibility role、R-B3 projection 与 B5 smoke tests；
  形成 focused Gate 判断。
- 当前上下文是否仍适合继续：**适合完成本轮 Reliability 收口；不适合直接修改
  implementation。**
- 是否建议新开 Thread：**yes，交回 Architecture/Implementation repair Thread。**
- 如果建议新开，请给出 handoff 摘要：基线 `e9abe45`；R-B2 CLOSED，R-B3/B5 无回归；
  R-B4 config/authority/code-origin 已关闭，但
  `event_type=station_result(result=nok)` + 合法 authority +
  `correlation.event_role=cycle_complete` 仍被 accepted。只需在 parent matcher 增加
  `production_result` role 检查和一个负例；不改合同、不接 integration。修后回
  Reliability 与 Verification targeted re-review。
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：**低**。新 Thread
  只需读取本节、`validation.py::_parent_matches()` 与 R-B4 tests。

本轮未修改 implementation、tests、合同、PM handoff、当前进度报告或
`docs/superpowers/`，未 commit/push/tag/deploy/rollback drill。

## 47. 当前 Reliability 控制结论

本节覆盖第 45 节 repair 前控制结论：

```text
HOLD
R-B2: CLOSED
R-B4: OPEN - canonical production_result role not enforced
R-B3: CLOSED, no regression
B5: CLOSED, no regression
```

在 R-B4 parent-role blocker、targeted re-review、Data Quality focused sign-off 与
ChatGPT PM 精确授权完成前，不具备 implementation commit/push 条件。

---

## 48. Sprint 2 Reliability R-B4 Minimal Repair Re-review Result

日期：2026-06-23
基线：`e9abe45 Finalize Sprint 2 station event review gates`
范围：只复验 R-B4 canonical parent `event_role=production_result` enforcement，并
轻量确认 R-B2/R-B3/B5 无回归。

结论：**PASS**

Focused status:

- R-B4 canonical parent `event_role=production_result` enforcement：**CLOSED**。
  `_evidence_error()` 对 accepted `validated_nok_detail` evidence 解析 canonical parent
  后复用 `_parent_matches()`；该 matcher 现在同时要求：
  `event_type=station_result`、`result=nok`、accepted lookup、
  PLC/PLC 或 V-PLC/simulator authority、same line/PLC/station/boot/cycle/unit-DMC/
  config、primary code/origin 或 secondary origin relation，以及
  `correlation.event_role=production_result`。
- parent role 为 `cycle_complete/diagnostic/compatibility/None` 或 key 缺失时，均稳定
  `reject / UPSTREAM_EVIDENCE_INVALID`。reject decision 的 projection
  `projection_eligible=false`，`production_outcome=null`，`defect_detail=null`；不成为
  validated detail，不进入 production NOK、ordinary/operator defect 或 Pareto。
- 合法 accepted authoritative `station_result(result=nok)`、same-config、
  matching code/origin 且 `event_role=production_result` 的 canonical parent 保持
  accepted。
- R-B2 30003 parent config isolation regression：**CLOSED，无回归**。跨 config skip
  parent 稳定 `PARENT_EVENT_INVALID`，且不产生 defect projection。
- R-B3 duplicate detail-set regression：**CLOSED，无回归**。duplicate code 稳定
  `DETAIL_CODE_DUPLICATE`，且不产生 production outcome 或 defect projection。
- B5 raw validation regression：**CLOSED，无回归**。periodic repeated fragment 与
  forbidden image/base64 fixture 均稳定 `RAW_CONTENT_FORBIDDEN`。

Findings:

- 未发现新的 Reliability blocker。
- `production_result` role 检查位于共享 canonical parent matcher，current detail 与
  `validated_nok_detail` evidence path 使用同一 fail-closed relation，未出现两条路径
  再次漂移。
- 本轮没有扩大到 Data Quality full review 或 Verification full re-review。

Tests:

- git status：HEAD 仍为 `e9abe45`；working tree 有既有未提交 implementation/tests/
  reports 与 `.gitignore` 修改。本 review 未修改这些路径。
- `git diff -- common/station_event/validation.py tests/test_station_event_model.py`：
  tracked diff 为空；两路径仍为既有 untracked implementation/tests，本 review 只读。
- compileall：**PASS**
- focused station_event：**119 passed in 0.06s**
- broader tests：root `tests/` **207 passed in 0.99s**
- targeted R-B4/R-B2/R-B3/B5 tests：**15 passed**
- `git diff --check`：**PASS**
- unrelated failures：未运行 repo-root 无参数 pytest；无新增 unrelated failure。

Independent focused evidence:

```text
R-B4_ROLE production_result accept None False None None
R-B4_ROLE cycle_complete reject UPSTREAM_EVIDENCE_INVALID False None None
R-B4_ROLE diagnostic reject UPSTREAM_EVIDENCE_INVALID False None None
R-B4_ROLE compatibility reject UPSTREAM_EVIDENCE_INVALID False None None
R-B4_ROLE None reject UPSTREAM_EVIDENCE_INVALID False None None
R-B4_ROLE <missing> reject UPSTREAM_EVIDENCE_INVALID False None None
R-B2_CROSS_CONFIG reject PARENT_EVENT_INVALID None
R-B3_DUPLICATE reject DETAIL_CODE_DUPLICATE False None None
B5_PERIODIC False [('RAW_CONTENT_FORBIDDEN', 'raw_payload.message')]
B5_FORBIDDEN False [('RAW_CONTENT_FORBIDDEN', 'raw_payload.payload')]
```

Files changed by this review:

- `docs/reports/sprint2_station_event_reliability_review.md`

Scope audit:

- implementation code modified：**no**
- tests modified：**no**
- contracts modified：**no**
- Collector/API/DB/Dashboard/V-PLC modified：**no**
- migration created：**no**
- tag created：**no**
- deploy：**no**
- rollback drill：**no**
- commit/push：**no**

Decision:

- Remaining Reliability blocker：**no**
- Need Architecture repair：**no**
- Need Verification targeted re-review：**yes**。只做 canonical parent role/relation
  sanity check；不重开 B1/B5 或完整 Verification。
- Need Data Quality focused review：**yes**。由 ChatGPT PM 安排既定 focused
  implementation review；本 Thread 不扩大执行。
- Eligible for implementation commit/push：**no**。Reliability PASS 不构成授权；仍需
  Verification targeted relation sanity check、Data Quality focused review 和 ChatGPT
  PM 精确 allowlist 授权。

Thread Health:

- 本 Thread 已完成的主要任务：重读 matcher/evidence path、new role tests 与最新
  reports/handoff；复现 119/207 tests；运行 15 个定向回归；独立重放合法/非法/missing
  parent role、R-B2 cross-config、R-B3 duplicate projection 与 B5 smoke probes；形成
  focused PASS。
- 当前上下文是否仍适合继续：**适合完成本轮 Reliability 收口；不应在本 Thread 继续
  Verification 或 Data Quality review。**
- 是否建议新开 Thread：**yes**。
- 如果建议新开，请给出 handoff 摘要：基线 `e9abe45`；Reliability R-B2/R-B3/R-B4
  全部 CLOSED，B5 regression CLOSED；canonical parent 强制
  `event_role=production_result`，错误/None/missing role 均
  `UPSTREAM_EVIDENCE_INVALID` 且不投影；119/207 tests PASS；下一步由 PM 安排
  Verification targeted relation sanity check 和 Data Quality focused review；不得
  commit/push。
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：**低**。后续
  Thread 应读取本节、`_parent_matches()`、`_evidence_error()` 与 role-focused tests。

本轮只修改 Reliability report；未修改 implementation、tests、合同、PM handoff、
当前进度报告或 `docs/superpowers/`，未 commit/push/tag/deploy/rollback drill。

## 49. 当前 Reliability 控制结论

本节覆盖第 47 节 HOLD：

```text
PASS
R-B2: CLOSED
R-B3: CLOSED
R-B4: CLOSED
B5 regression: CLOSED
```

Reliability focused blocker 已全部关闭，但不授权 commit/push。下一步由 ChatGPT PM
安排 Verification targeted relation sanity check 与 Data Quality focused implementation
review；两者通过并获得 PM 精确授权前，不得 commit/push 或进入 integration。

---

## 50. Post-commit closeout current-control note（2026-06-24）

本文件前文保留 Reliability review 各轮审计当时的 Git 基线、working tree 状态与
handoff 建议；其中 `45fa2a8`、`e9abe45`、未提交 implementation 等描述均为历史证据，
不再代表当前 repo 状态。

当前 Sprint 2 source of truth：

```text
HEAD/origin/main: 17cf5d2 Implement Sprint 2 generic station event model
Sprint 2 implementation: committed/pushed
Reliability focused Gate: PASS
Remaining Reliability blocker: none
runtime integration: not started
migration/tag/deploy/rollback drill: not performed
```

本 closeout note 只同步文档控制状态，不修改 implementation、tests、Collector、API、
DB、Dashboard、V-PLC、migration 或发布状态。
