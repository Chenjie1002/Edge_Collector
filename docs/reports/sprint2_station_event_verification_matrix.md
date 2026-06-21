# Sprint 2 Station Event Verification Gate Matrix

日期：2026-06-21
Thread：Verification
对象：Phase-2 Sprint 2 Generic Station Event Model planning / contract / review state
审查类型：Gate matrix / verification planning；不是 implementation

## 1. 总控制结论

```text
HOLD / CHANGES REQUIRED
```

当前合同的大部分语义已经具备可验证性，但仍有三组 Verification blocker：

1. payload/raw 的 array-item 与 string-value limit 没有唯一稳定错误码映射。
2. 相同 business content、不同合法 raw evidence 时，`duplicate` 与 audit-only
   `raw_variant` 的最终裁决关系未冻结。
3. lifecycle matrix 在 start 与 complete 同时缺失等组合状态下不互斥，且没有冻结
   `projection_eligibility / cycle_completeness / traceability` 的派生输出接口。

- Reliability 当前控制结论为 `PASS WITH RECOMMENDATIONS`；N5、N6、N7、N8、
  UNKNOWN diagnostic context、payload limits、event required fields 均 CLOSED。
- Data Quality focused re-review 当前控制结论为 `PASS WITH RECOMMENDATIONS`；
  R1、R2、R3、R5 CLOSED，R4 CLOSED WITH RECOMMENDATIONS。
- 本轮 finding 不重新打开 Reliability 已关闭项；它们是 Verification
  executability / acceptance ambiguity。
- Architecture 需要做一次最小 docs-only 返修。
- 返修后需要 Verification focused re-review；V10 涉及 R5，建议 Data Quality 只做
  R5 定向复验。Reliability 无需复验。

本结论表示 planning / contract / review state 已完成审查，但 Verification planning
Gate 当前为 HOLD。当前不建议 ChatGPT PM 授权 implementation。

## 2. 本轮审查范围

本轮只完成：

1. 核验当前 working tree，而不是只读取 `origin/main`。
2. 将 Reliability CLOSED items 与 Data Quality R1～R5 转为正式 V1～V12 Gate matrix。
3. 冻结 implementation 前必须满足的测试类别、负面测试、隔离边界和验收条件。
4. 判断是否仍有阻塞 implementation authorization 的 Verification blocker。

本轮不执行：

- implementation 或 implementation plan。
- 创建 `common/station_event/`。
- 修改 code、tests、runtime、Collector、API、DB、Dashboard 或 V-PLC。
- 修改 Architecture contract/planning/handoff。
- 修改 Reliability 或 Data Quality report。
- migration、commit、push、tag、deploy 或 rollback drill。

## 3. 读取文件

完整审查当前 working tree 中以下文件：

1. `docs/contracts/station_event_model.md`
2. `docs/contracts/dynamic_station_model.md`
3. `docs/contracts/line_configuration.md`
4. `docs/reports/sprint2_generic_station_event_model_plan.md`
5. `docs/reports/sprint2_station_event_reliability_review.md`
6. `docs/reports/sprint2_station_event_data_quality_review.md`
7. `docs/thread_handoff/architecture.md`
8. `docs/reports/architecture_context_restore.md`
9. `docs/reports/phase2_sprint_plan.md`
10. `docs/reports/phase2_thread_task_plan.md`
11. `docs/DOC_INDEX.md`
12. `docs/reports/README.md`

控制结论读取规则：

- Reliability 以其第 37～43 节为当前状态；早期 HOLD 为历史审计记录。
- Data Quality 以其第 16～24 节为当前状态；第 1～15 节 HOLD 为历史审计记录。
- `station_event_model.md` 第 18 节是 R1～R5 最新冻结语义；与早期概括冲突时以该节为准。

## 4. 当前基线与隔离确认

| 项目 | 当前证据 | 结论 |
| --- | --- | --- |
| HEAD | `60adac2 Address Sprint 2 station event reliability review` | PASS |
| origin/main | `60adac2` | PASS |
| 最近三个 commit | `60adac2`、`45fa2a8`、`4215b7c` | PASS |
| tag | 仅 `phase1-pass-20260619` | PASS |
| `common/station_event/` | absent | PASS |
| Sprint 2 implementation | 未开始 | PASS |
| code/tests/runtime diff | 无 | PASS |
| Collector/API/DB/Dashboard/V-PLC diff | 无 | PASS |
| 当前业务工作范围 | Architecture 与 review docs-only working tree | PASS |
| Phase-2 tag | 未创建 | PASS |
| deploy / rollback drill | 未执行 | PASS |

审查开始前 working tree 为：

```text
 M docs/DOC_INDEX.md
 M docs/contracts/dynamic_station_model.md
 M docs/contracts/station_event_model.md
 M docs/reports/README.md
 M docs/reports/architecture_context_restore.md
 M docs/reports/sprint2_generic_station_event_model_plan.md
 M docs/thread_handoff/architecture.md
?? docs/20260620_03_Edge MES Demo — ChatGPT PM Handoff.md
?? docs/Edge MES Demo 当前进度报告.md
?? docs/reports/sprint2_station_event_data_quality_review.md
?? docs/superpowers/
```

本轮只新增本 Verification report；用户明确禁止处理的三个未跟踪路径保持不动。

## 5. Gate 总表

| Gate | 结论 | Verification 判断 |
| --- | --- | --- |
| V1 Scope / isolation | PASS | implementation 未开始，当前变更保持 docs-only |
| V2 Event schema | PASS WITH RECOMMENDATIONS | 五类事件的 required/optional/forbidden、authority 与 absence 语义已冻结 |
| V3 Config / lineage | PASS WITH RECOMMENDATIONS | historical exact snapshot 与 mismatch disposition 可验证 |
| V4 Result projection | PASS | canonical result authority 与 detail-only projection 唯一 |
| V5 NOK detail / reserved code | PASS WITH RECOMMENDATIONS | ordinary detail、30003 与 evidence boundary 可执行 |
| V6 Payload / raw | HOLD / CHANGES REQUIRED | array/string resource limit 缺唯一错误码 |
| V7 Identity / idempotency | HOLD / CHANGES REQUIRED | duplicate 与 raw_variant 的最终裁决未冻结 |
| V8 Fingerprint determinism | PASS WITH RECOMMENDATIONS | JCS 与官方向量已定义；跨 runtime fixture 为实施期必测 |
| V9 Stateful relation | PASS | lookup interface 与 fail-closed disposition 已冻结 |
| V10 Temporal / lifecycle | HOLD / CHANGES REQUIRED | lifecycle 组合状态与派生输出 schema 不唯一 |
| V11 Metrics / Dashboard / API readiness | PASS WITH RECOMMENDATIONS | 指标口径已可验证，但本 Sprint 不实现 endpoint/UI/DB migration |
| V12 Implementation readiness | HOLD / CHANGES REQUIRED | V6、V7、V10 blocker 关闭前不得授权 implementation |

## 6. V1 — Scope / isolation Gate

**结论：PASS**

### Verification objective

证明当前是 planning/contract/review stack，未混入 Sprint 2 implementation 或运行链路变更。

### Source contract/docs

- `station_event_model.md` 第 2、15、17、19 节。
- `sprint2_generic_station_event_model_plan.md` 第 1、6、17 节。
- Architecture handoff/context 的基线与禁止事项。
- 当前 Git working tree。

### Expected test categories

- Git scope audit。
- path existence audit。
- code/tests/runtime diff audit。
- package/import isolation audit。
- tag/deploy/rollback state audit。

### Negative tests

- `common/station_event/` 意外存在。
- `common/`、`services/`、`apps/`、`tests/` 出现 station-event implementation diff。
- Collector/API/DB/Dashboard/V-PLC 被提前修改。
- planning review 中出现 migration、deploy、tag 或 rollback artifact。

### Acceptance criteria

- `common/station_event absent`。
- code/tests/runtime diff 为空。
- 当前新增内容只有 Verification report。
- 未 commit、push、tag、deploy、rollback drill。

### Implementation boundary

本 Gate 只验证隔离，不授权创建 package、tests 或 adapter。

## 7. V2 — Event schema Gate

**结论：PASS WITH RECOMMENDATIONS**

### Verification objective

保证五类 MVP event 对同一输入给出唯一、fail-closed 的 schema 与 authority 结果。

### Source contract/docs

- `station_event_model.md` 第 4～9 节，尤其第 4.2、4.3、8.1、9、9.1 节。
- Reliability 当前控制结论及 CLOSED event required/UNKNOWN findings。

### Expected test categories

- 五类 event 最小合法正例。
- common required fields table tests。
- per-event required/optional/forbidden table tests。
- absent/null/unknown field tests。
- result/event/NOK combination tests。
- source/actor/nok_origin authority table tests。
- profile/config/station-enabled tests。
- heartbeat diagnostic-only projection exclusion tests。

### Negative tests

- required field missing 或 explicit null。
- optional field explicit null。
- forbidden field present，包括 null。
- `station_cycle_complete` 携带 `result`。
- `station_result` 缺 result、使用 unknown 或 NOK 字段组合错误。
- `station_nok` 携带 result/diagnostic context 或缺 parent/detail role。
- heartbeat 携带 cycle/unit/DMC/NOK/upstream evidence。
- heartbeat `unknown` 缺 strict diagnostic context。
- disabled station 产生 production event。
- source/actor/nok_origin 不在 allow matrix。
- Collector/system 冒充 PLC/V-PLC production authority。

### Acceptance criteria

- `station_cycle_start`、`station_cycle_complete`、`station_result`、`station_nok`、
  `station_heartbeat` 均有最小正例和逐字段负例。
- `profile_id` 对 cycle/result/NOK 必需，对 heartbeat optional 且存在时必须匹配 config。
- unit/DMC 可 absent，但不得猜测或互相替代。
- heartbeat 永远不进入 cycle、result、NOK、OEE、Quality、FPY 或控制投影。
- UNKNOWN 只允许 heartbeat 且有可验证 diagnostic context。

### Implementation boundary

只实现独立 model/validator/serializer；不接 Collector、DB、API 或 Dashboard。

### Non-blocking recommendation

将五类 event × authority × result 组合实现为 table-driven fixtures，避免逐测试手写漂移。

## 8. V3 — Config / lineage Gate

**结论：PASS WITH RECOMMENDATIONS**

### Verification objective

保证事件只能由其自身 `config_hash` 对应的 immutable historical snapshot 解释。

### Source contract/docs

- `station_event_model.md` 第 10、12.1、13、16、18.1 节。
- `line_configuration.md` 第 5、7、8、13、16 节。
- Data Quality focused R1 CLOSED。

### Expected test categories

- `config_hash` format、lookup、identity match/mismatch。
- exact station/PLC/type/profile lookup。
- configured mapping conditional-required tests。
- heartbeat diagnostic mapping lineage tests。
- immutable payload template reference tests。
- decoder version/NOK template/version resolution tests。
- historical snapshot replay tests。

### Negative tests

- missing/invalid/unknown `config_hash`。
- 用 current/latest config 解释历史 event。
- mapping absent、wrong mapping 或同站多 mapping 时猜测 mapping。
- mutable/unversioned payload template reference。
- decoder/NOK template 无法解析、存在多义或与 event code/origin 不一致。
- station/PLC/type/profile/route identity mismatch。

### Acceptance criteria

- lookup 至少返回 exact line/PLC/station、mapping、payload template、decoder、NOK
  template、profile 与 route snapshot。
- `CONFIG_NOT_FOUND`、`CONFIG_HASH_MISMATCH`、`EVENT_LINEAGE_INVALID` 各有唯一负例。
- historical event 永不 fallback 到 current config。
- configured production mapping 的 `mapping_id` 必须存在并逐字匹配。

### Implementation boundary

Sprint 2 只实现离线 resolved-config correlation；不实现 runtime registry、reload、
snapshot persistence 或 DB migration。

### Non-blocking recommendation

增加“同 station 多 mapping、同 template ID 多 version、历史 snapshot 缺失”三组专门 fixture。

## 9. V4 — Result projection Gate

**结论：PASS**

### Verification objective

证明每个 physical production result slot 只产生一个 canonical outcome。

### Source contract/docs

- `station_event_model.md` 第 7.1、12.4、12.7、18.2 节。
- `dynamic_station_model.md` 第 4.1、4.3、4.4 节。
- Data Quality focused R2 CLOSED。

### Expected test categories

- `production_result_key` uniqueness。
- outcome/detail projection separation。
- compatibility projection tests。
- duplicate/conflict no-projection tests。
- reserved detail exclusion tests。

### Negative tests

- `station_cycle_complete` 创建或携带 result。
- `station_nok` 创建第二个 outcome。
- `cycle_event.result` 被当作独立 authority。
- `quality_event` 重复 result 或增加 NOK cycle count。
- duplicate/conflict 再次投影。
- `30003` 进入 ordinary defect、Pareto、production NOK、FPY 或 Quality。

### Acceptance criteria

- `station_result` 是唯一 canonical production result authority。
- 每个 `production_result_key` 最多一次 accepted outcome projection。
- `cycle_event.result` 只能 derived/non-authoritative。
- quality/defect row detail-only。
- `station_nok` 只投影 accepted distinct detail。

### Implementation boundary

本 Sprint 验证 projection contract 与纯函数行为，不实现真实 DB row、API 聚合或 Dashboard。

## 10. V5 — NOK detail / reserved code Gate

**结论：PASS WITH RECOMMENDATIONS**

### Verification objective

保证 ordinary primary/secondary detail 与 `30003/system_reserved` 使用不同、可审计的槽位和证据规则。

### Source contract/docs

- `station_event_model.md` 第 7.1、8、9、12.1.1、12.1.2、12.4、13.2、18.2 节。
- Reliability N8 current re-review。

### Expected test categories

- primary/secondary/system-reserved slot tests。
- canonical parent relation tests。
- upstream evidence type tests。
- code/origin/route/subject/boot/config consistency tests。
- Pareto completeness tests。

### Negative tests

- 第二个 primary。
- secondary 在 primary 之前。
- primary code/origin 与 parent 不一致。
- secondary code 等于 parent primary code 或 origin 不一致。
- ordinary detail parent 不是 canonical NOK result。
- `30003` parent 不是 canonical skip result。
- `30003` 缺 evidence、evidence not found/mismatch/state unavailable。
- `validated_nok_detail` 自身携带 result。
- cited detail parent 为 OK。
- technical failure 支持 `30003/UPSTREAM_NOK_SKIPPED`。
- counter-only、无相同 unit/DMC 时生成 30003。

### Acceptance criteria

- 每 parent 最多一个 primary；secondary 必须在 accepted primary 后，且 code 不同、
  origin 一致。
- 每 skip parent 最多一个 system-reserved detail。
- `validated_nok_detail` 比较 canonical parent `station_result(result=nok)`，detail
  自身 result 必须 absent。
- ordinary NOK parent 是 canonical `station_result(result=nok)`。
- technical failure 永不生成 business NOK、30003、Skip attribution 或 Pareto entry。
- detail 可选；缺 primary 时 outcome 仍 valid，但 Pareto 必须 `partial`。

### Implementation boundary

不实现 route execution、Collector quarantine 或 batch finalization。

### Non-blocking recommendation

把 Reliability pseudo example 扩成完整 current skip event、cited detail、canonical
parent 与 state-index records fixture。

## 11. V6 — Payload / raw Gate

**结论：HOLD / CHANGES REQUIRED**

### Verification objective

证明 normalized/raw 输入有确定资源边界、唯一 authority chain 和 mismatch disposition。

### Source contract/docs

- `station_event_model.md` 第 11、12.1、13.1、18.3、18.4 节。
- Data Quality focused R3 CLOSED。

### Expected test categories

- 16 KiB normalized 与 64 KiB raw boundary tests。
- depth/key/array/string/node limit tests。
- JSON type与 number tests。
- raw encoding/template/decoder lineage tests。
- raw-only/normalized-only/both-present completeness tests。
- mismatch error classification tests。
- raw evidence fingerprint/audit variant tests。

### Negative tests

- limit+1 byte、depth+1、key/array/node/string 超限。
- NaN、Infinity、超 binary64/safe integer range。
- bytes、binary、base64、image、opaque/unbounded log、自定义对象、循环引用。
- raw top-level 非 object 或 `raw_encoding != json`。
- raw-only 被 accepted 为 canonical business event。
- raw 替代 canonical top-level/result fields。
- parse/schema/value mismatch。

### Acceptance criteria

- normalized payload 最大 16384 bytes；raw 最大 65536 bytes。
- raw MVP 仅 JSON object。
- authority chain 为
  `raw → exact mapping/template/decoder → normalized → canonical projection`。
- `RAW_PARSE_ERROR`、`PAYLOAD_SCHEMA_MISMATCH`、`RAW_NORMALIZED_MISMATCH` 唯一可测。
- completeness 明确为 `raw_and_normalized`、`normalized_only`、`raw_only`、
  `evidence_mismatch`。
- raw fingerprint 只用于 audit；`raw_variant` 不创建第二个 business fact；
  `raw_evidence_conflict` 不 accepted。
- 单 array 129 items、全树 257 array items、normalized string 4097 bytes、raw nested
  string 16385 bytes 必须各自返回唯一稳定 error code/path。

### Remaining blocker

合同冻结了 array/string 阈值，但 error code 清单没有为这些 limit 指定唯一映射。
这些输入可能未触发 total-size 或 total-node limit，因此 Verification 无法为
limit+1 fixture 断言唯一 expected code。

最小 Architecture 返修：

- 新增 `PAYLOAD_ARRAY_LIMIT`、`PAYLOAD_STRING_LIMIT`；或
- 明确将单 array、全树 array items、normalized/raw string limit 分别映射到哪个现有
  stable error code。

### Implementation boundary

不实现 raw storage retention、binary content type、runtime quarantine 或 drill-down UI。

### Non-blocking recommendation

边界测试同时检查 canonical UTF-8 byte size，而不是 Python 字符数。

## 12. V7 — Identity / idempotency Gate

**结论：HOLD / CHANGES REQUIRED**

### Verification objective

保证 envelope identity、source trace、deterministic fact identity、business slot 与内容比较各司其职。

### Source contract/docs

- `station_event_model.md` 第 6、12.3～12.7、13.2、18.4 节。
- Reliability N6/N7 CLOSED。
- Data Quality focused R4 CLOSED WITH RECOMMENDATIONS。

### Expected test categories

- UUIDv4 accepted identity/retry reuse。
- UUIDv5 fixture-helper exclusion。
- source event retry stability。
- fact/cycle-role/detail key official tests。
- same-slot duplicate/conflict。
- multi-key collision precedence。
- audit decision field completeness。

### Negative tests

- retry/replay 重新生成 UUIDv4。
- validator accepted event 使用 UUIDv5。
- source_event_id 使用随机数或接收时间。
- 通过改变 source_event_id 绕过 production slot。
- same slot + different fingerprint 被 merge 或 last-write-wins。
- lower-priority collision 覆盖 higher-priority final error。
- decision 缺 matched/existing/incoming/final audit fields。

### Acceptance criteria

- `event_id`、`source_event_id`、`fact_key` 职责明确且不可互换。
- `cycle_role_key`、`production_result_key`、`station_nok_detail_key`、
  `primary_nok_detail_key`、`system_reserved_detail_key` 全部有 fixture。
- same slot + same fingerprint 为 duplicate；different 为 conflict。
- precedence 固定：
  `event_id → fact_key → cycle-role/result → detail slots`。
- audit 至少包含 matched key type/value、existing event ID、existing/incoming content
  fingerprint、existing/incoming raw fingerprint、final disposition/error。

### Remaining blocker

以下场景同时命中 event/fact duplicate 与 raw evidence variant：

```text
same event_id
same fact_key
same content_fingerprint
different valid raw_evidence_fingerprint
```

第 12.7 节要求 final disposition 为 `duplicate`，第 18.3 节又定义 audit-only
`raw_variant`；但 `ValidationDecision` 没有 `raw_variant`，合同也未说明它是 final
disposition、audit subtype 还是 additional finding。

最小 Architecture 返修必须冻结：

- final disposition 是否仍为 `duplicate`。
- `raw_variant` 的正式 audit 字段/枚举位置。
- `final_error_code` 是 null、固定 warning code 或其他值。
- 与 multi-key precedence、`additional_matched_keys` 的关系。

### Implementation boundary

不实现 DB unique constraint、Collector retry 或 quarantine persistence。

### Non-blocking recommendation

将 UUIDv7 保持 future recommendation，不作为 MVP 正例必要条件。

## 13. V8 — Fingerprint determinism Gate

**结论：PASS WITH RECOMMENDATIONS**

### Verification objective

保证跨 Python、JavaScript 与 PostgreSQL 边界得到相同 canonical bytes 与 SHA-256。

### Source contract/docs

- `station_event_model.md` 第 12.5、12.6、14、18.4 节。
- Data Quality focused R4 CLOSED WITH RECOMMENDATIONS。

### Expected test categories

- canonical key ordering、UTF-8、lowercase SHA-256。
- absent vs null。
- enum/timestamp normalization。
- profile/config inclusion。
- official fact/content fingerprint vectors。
- RFC 8785/JCS number vectors。
- field-order independence 与 mutation sensitivity。

### Negative tests

- 使用语言默认 serializer。
- `ensure_ascii`、空格、换行、key order 导致 bytes 漂移。
- absent 与 null 混同。
- NaN/Infinity。
- `-0`、integer/decimal、exponent form 在不同 runtime 输出不同。
- 删除 include 字段或错误递归删除同名字段。
- raw fingerprint 替代 content fingerprint。

### Acceptance criteria

- canonical JSON 使用 RFC 8785/JCS 等价 UTF-8 bytes。
- SHA-256 输出 lowercase hex，前缀按合同。
- official station result/NOK fact 与 content vectors 精确匹配。
- 数字向量至少包含：
  `-0/-0.0 → 0`、`1/1.0 → 1`、`1e30 → 1e+30`、
  `0.000001 → 0.000001`、maximum finite binary64。
- 修改 event_id/observed_at/source_event_id 不改变 content fingerprint；修改 result、
  config、cycle、payload、detail/parent/evidence 必须改变。

### Implementation boundary

本 Gate 要求 fixture 级跨 runtime 证明；不要求本 planning review 现在运行 JS/PG 实现。

### Non-blocking recommendations

- implementation Gate 必须补跨 Python/JavaScript/PostgreSQL exact bytes + hash fixtures。
- 增加 Unicode、rounding、中文 ID 与边界长度向量；这些不阻塞当前合同 Gate。

## 14. V9 — Stateful relation Gate

**结论：PASS**

### Verification objective

保证所有 parent/evidence/config/uniqueness relation 在 state index 缺失时 fail closed。

### Source contract/docs

- `station_event_model.md` 第 12.1.1、12.4、12.7、13.2 节。
- Reliability N7 CLOSED。

### Expected test categories

- lookup interface contract tests。
- missing/unavailable/not-found/mismatch tests。
- duplicate/conflict precedence tests。
- parent/evidence/config/detail-set tests。

### Negative tests

- state index 未提供或 unavailable。
- required parent/evidence/config field missing。
- parent/evidence/config lookup not found。
- found record type/result/cycle/route/subject/config 不匹配。
- secondary 无 accepted primary。
- missing relation 被 defer/quarantine/accept。

### Acceptance criteria

state index 必须覆盖：

- event ID / fact key lookup。
- cycle-role lookup。
- parent result lookup。
- upstream evidence lookup。
- detail-set / detail-key lookup。
- resolved config lookup。

并满足：

- unavailable → `STATE_INDEX_UNAVAILABLE`。
- not found → `PARENT_NOT_FOUND`、`UPSTREAM_EVIDENCE_NOT_FOUND` 或
  `CONFIG_NOT_FOUND`。
- same slot/same fingerprint → duplicate。
- same slot/different fingerprint → conflict。
- defer/quarantine 仅 future，不属于 MVP accepted validator。

### Implementation boundary

state index 是只读抽象接口；本 Sprint 不实施 repository、DB constraint 或 async ingestion。

## 15. V10 — Temporal / lifecycle Gate

**结论：HOLD / CHANGES REQUIRED**

### Verification objective

保证 source、observer、storage 时间不互相覆盖，out-of-order 与 lifecycle completeness 可确定处理。

### Source contract/docs

- `station_event_model.md` 第 3、5、12.2、18.5 节。
- Data Quality focused R5 CLOSED。

### Expected test categories

- RFC 3339 UTC/下限/future skew tests。
- `event_ts/observed_at/created_at` ownership tests。
- arrival-order independence。
- lifecycle table-driven tests。
- projection/completeness/traceability derived metadata tests。

### Negative tests

- source envelope 携带 `created_at`。
- 非 UTC、早于 2000、超 observed_at 5 分钟。
- 修改 event_ts 以制造顺序。
- 用时间邻近补 parent、unit 或 genealogy。
- MVP 将 event 判为 late。
- timestamp reversal 改写/重排 source fact。

### Acceptance criteria

必须覆盖：

- start missing。
- complete missing。
- result without start。
- result without complete。
- complete without start。
- result before start/complete arrival。
- start/complete 后补。
- timestamp reversal。
- nok detail parent missing/OK。
- duplicate/conflict detail。

每项都有 disposition、projection eligibility、`cycle_completeness` 与 traceability；
unit/DMC 都 absent 时固定 `cycle_only`，不得宣称完整 genealogy。

### Remaining blocker

当前 lifecycle matrix 的条件存在重叠：

- `result without start`
- `result without complete`
- `result before start/complete arrival`

当 start 与 complete 同时缺失时，可同时得到 `partial_missing_start`、
`partial_missing_complete` 或笼统的 `partial`；“至少”和“剩余 partial”不能作为
唯一验收值。`ValidationDecision` 也只冻结 disposition/accepted，未定义承载
projection eligibility、cycle completeness、traceability 与 lifecycle diagnostic 的
派生输出 schema。

最小 Architecture 返修：

1. 将 lifecycle condition 改为互斥且穷尽的 role-presence 状态表。
2. 明确 start+complete 双缺失、补到一个 role、全部补齐的唯一状态与迁移。
3. 冻结独立 lifecycle derivation function/interface 及输出 schema，或扩展
   `ValidationDecision` 使上述字段可直接断言。
4. 保持 late future-only，不扩大 MVP。

### Implementation boundary

late threshold、watermark、arrived-late metadata 属 future runtime；MVP 不判 late。

### Non-blocking recommendation

fixture 应显式区分 source event order、arrival order 与 timestamp order。

## 16. V11 — Metrics / Dashboard / API readiness Gate

**结论：PASS WITH RECOMMENDATIONS**

### Verification objective

保证未来 consumer 可以从同一 canonical authority 计算 NOK outcome、detail Pareto 与 completeness。

### Source contract/docs

- `station_event_model.md` 第 7.1、18.2、18.3、18.5 节。
- `dynamic_station_model.md` 第 4.1～4.4、9 节。
- Data Quality focused R2/R3/R5。

### Expected test categories

- outcome vs detail metric separation。
- Pareto completeness formula tests。
- duplicate/conflict/reserved exclusion。
- raw audit drill-down metadata tests。
- cycle-only traceability presentation contract tests。

### Negative tests

- `NOK unit/cycle count` 与 `defect_detail_count` 混用。
- 一个 cycle 多 detail 增加多个 NOK outcomes。
- 缺 primary 仍显示完整 Pareto。
- `30003` 进入 ordinary Pareto/NOK。
- API/Dashboard 使用 cycle complete、quality row 或 raw 作为 result authority。
- compatibility projection 与 canonical result 分别计数。

### Acceptance criteria

至少冻结并验证：

```text
nok_cycle_count
nok_cycles_with_primary_detail
missing_primary_detail_cycle_count
detail_coverage
pareto_status = complete | partial
```

- `nok_cycle_count=0` 时 coverage 为 1.0、status complete。
- 缺 primary 时 status partial，并对 consumer 可见。
- raw drill-down 显示 completeness、variant/conflict 与 lineage，不改变 canonical result。
- API/Dashboard result authority 只来自 accepted `station_result`。

### Implementation boundary

本 planning Gate 不新增 API endpoint、DB migration、Dashboard 或 raw drill-down UI。

### Non-blocking recommendation

后续 consumer contract 应明确 compatibility projection 的局限与 `partial` UI 文案。

## 17. V12 — Implementation readiness Gate

**结论：HOLD / CHANGES REQUIRED**

### Verification objective

判断当前最终合同是否已足够明确，使 implementation Thread 可以在 PM 授权后按测试先行方式实施。

### Source contract/docs

- Reliability 当前第 43 节。
- Data Quality focused re-review 第 23～24 节。
- `sprint2_generic_station_event_model_plan.md` 第 7、11、13、14、16、17 节。
- V1～V11 本矩阵。

### Expected test categories

implementation 前测试计划必须至少包含：

1. 五类 event construction。
2. required/optional/forbidden、absent/null。
3. enum/combination/authority。
4. config lineage。
5. payload/raw boundaries 与 mismatch。
6. UUID/fact/slot/fingerprint。
7. stateful parent/evidence/config。
8. projection/Pareto completeness。
9. temporal/lifecycle/traceability。
10. canonical serialization/round-trip/snapshot。
11. import/scope isolation。
12. Sprint 1 config regression、root regression、compileall。

### Negative tests

- 任一 CLOSED finding 没有可执行 fixture。
- implementation 偷接 runtime 模块。
- 依赖 DB/API/Dashboard 才能验证纯 model。
- 使用未冻结的 defer/quarantine/late 语义。
- 通过改合同语义来让测试通过。

### Acceptance criteria

解除 V12 HOLD 必须满足：

- V1～V11 无 HOLD。
- Reliability 与 Data Quality 均无 remaining blocker，且 Verification 新 finding 已关闭。
- implementation prompt 明确 exact file scope、tests-first、no runtime integration。
- focused tests、Sprint 1 regression、root tests、compileall、diff/import audit 均列为
  implementation closeout Gate。
- PM 明确授权后方可实施。

### Implementation boundary

Verification 只能建议 PM 授权；本 Thread 不创建 package、tests 或代码。

## 18. Implementation 前冻结的最小测试矩阵

| Test family | 必须覆盖 |
| --- | --- |
| Construction | 五类 MVP event 最小正例 |
| Presence | required missing/null、optional absent/null、forbidden present/null |
| Combination | event/result/NOK/diagnostic/authority 全表 |
| Config | hash、station/PLC/type/profile、mapping/template/decoder/NOK/route snapshot |
| NOK | parent、primary/secondary、30003、两类 evidence、technical failure |
| Payload | 16 KiB、depth/key/array/string/node/type/number |
| Raw | 64 KiB、JSON-only、decoder comparison、completeness、mismatch、audit fingerprint |
| Identity | UUIDv4 retry、UUIDv5 fixture policy、fact/role/detail keys |
| Fingerprint | official vectors、JCS numbers、field order、mutation |
| Stateful | unavailable/not-found/mismatch、duplicate/conflict、precedence/audit |
| Lifecycle | missing roles、out-of-order fill、timestamp reversal、cycle-only |
| Projection | one outcome、detail-only、Pareto complete/partial、reserved exclusion |
| Serialization | canonical dict/JSON、round-trip、snapshot、mutation isolation |
| Isolation | no Collector/V-PLC/API/DB/Dashboard imports |
| Regression | Sprint 1 config、root suite、compileall、git diff check |

## 19. Remaining blocker

```text
remaining HOLD blocker: V6-B1, V7-B1, V10-B1/B2
```

最小返修项：

1. 冻结 array/string resource limit 的唯一错误码。
2. 冻结 `duplicate` 与 audit-only `raw_variant` 的 final-decision/audit schema。
3. 将 lifecycle matrix 改为互斥、穷尽的状态表，并冻结 lifecycle derived output
   interface/schema。

这些返修只需修改 Architecture contract/planning 的最小相关段落，不需要扩大 event
type、修改 Reliability 结论或进入 implementation。

## 20. Non-blocking recommendations

1. 将 R4 JCS 数字向量实现为 Python/JavaScript/PostgreSQL exact bytes + SHA-256 fixtures。
2. 增加 Unicode、中文 ID、rounding、边界长度和 secondary/system-reserved official vectors。
3. 将 N8 pseudo example 扩成完整 envelope + state-index fixture。
4. 使用 table-driven matrix 覆盖 authority、lifecycle、collision precedence 与错误码。
5. 后续 docs hygiene 将 Architecture plan/handoff/context、`DOC_INDEX.md` 和
   `reports/README.md` 中仍写 Data Quality HOLD/待复验的历史状态，更新为 focused
   re-review `PASS WITH RECOMMENDATIONS`。该状态漂移不影响当前合同 Gate。
6. docs-only commit/push 应使用精确 allowlist，继续排除用户指定的三个未跟踪路径，并
   禁止 `git add .`。

## 21. Gate 决策建议

| 决策 | Verification 建议 |
| --- | --- |
| 是否可以进入 Sprint 2 implementation | **否** |
| 是否需要回 Architecture | **是，只做 V6/V7/V10 最小 docs-only 返修** |
| 是否需要 Reliability re-review | **否** |
| 是否需要 Data Quality re-review | **是，仅对 V10/R5 做 focused re-review** |
| 是否扩大 Sprint 2 MVP | **否** |
| 是否可以 docs-only commit/push 当前 review stack | **不建议作为 implementation-ready stack 提交；可由 PM 决定是否先保存 HOLD 审计证据** |

建议 docs-only allowlist 至少覆盖当前 Architecture R1～R5 stack、Data Quality focused
review 与本 Verification report；实际提交清单由 ChatGPT PM 在 commit 前根据
`git status --short` 精确确认。

明确不得纳入：

- `docs/20260620_03_Edge MES Demo — ChatGPT PM Handoff.md`
- `docs/Edge MES Demo 当前进度报告.md`
- `docs/superpowers/`

## 22. 文件与操作范围

本轮新增：

- `docs/reports/sprint2_station_event_verification_matrix.md`

本轮未修改：

- Architecture contracts / planning / handoff。
- `docs/reports/sprint2_station_event_reliability_review.md`。
- `docs/reports/sprint2_station_event_data_quality_review.md`。
- code / tests / runtime。
- Collector / API / DB / Dashboard / V-PLC。

本轮未执行：

- 创建 `common/station_event/`。
- implementation。
- commit / push / tag / deploy。
- rollback drill。
- `git add .`。

## 23. 最终结论

```text
HOLD / CHANGES REQUIRED
```

Sprint 2 Generic Station Event Model 的大部分合同语义和测试矩阵已经冻结，但 V6
resource-limit error mapping、V7 raw-variant decision、V10 lifecycle state/output 仍存在
唯一性缺口。建议 ChatGPT PM 派回 Architecture 做最小 docs-only 返修；完成后由
Verification focused re-review，并由 Data Quality 仅复验 V10/R5。关闭前不得授权
Sprint 2 implementation。

---

## 24. Verification focused re-review（2026-06-21）

> 本节追加记录 Architecture 完成 V6/V7/V10 最小 docs-only 修订后的 focused
> re-review。第 1～23 节的 `HOLD / CHANGES REQUIRED` 与 remaining blocker 保留为
> 上一轮历史审计记录；当前 Verification 控制结论以本节至第 31 节为准。

### 24.1 本轮复验范围

本轮只复验：

1. V6 payload/raw final error mapping、multi-error precedence 与 fail-closed boundary。
2. V7 same canonical content + different raw evidence fingerprint 的 final decision。
3. V10 lifecycle evaluation order、mutual exclusivity、双缺失 completeness 与 derived
   output interface。

除非上述修订直接造成回归，本轮不重开 V1～V5、V8～V9、V11；不扩大 Sprint 2 MVP，
不进入 implementation。

### 24.2 读取文件

本轮读取当前 working tree：

1. `docs/reports/sprint2_station_event_verification_matrix.md`
2. `docs/contracts/station_event_model.md`
3. `docs/contracts/dynamic_station_model.md`
4. `docs/reports/sprint2_generic_station_event_model_plan.md`
5. `docs/thread_handoff/architecture.md`
6. `docs/reports/architecture_context_restore.md`
7. `docs/reports/sprint2_station_event_data_quality_review.md`
8. `docs/reports/sprint2_station_event_reliability_review.md`
9. `docs/DOC_INDEX.md`
10. `docs/reports/README.md`

重点复验 `station_event_model.md` 的 Payload/raw final error mapping、12.7、13.2、
18.3～18.5，以及 Architecture handoff/context 对 V6/V7/V10 的修订摘要。

## 25. 当前基线与隔离确认

```text
HEAD        60adac2
origin/main 60adac2
latest      60adac2 Address Sprint 2 station event reliability review
tag         phase1-pass-20260619
common/station_event absent
code/tests/runtime diff: none
```

- Sprint 2 implementation 尚未开始。
- Collector、API、DB、Dashboard、V-PLC、tests 与 runtime 无 diff。
- 当前 Architecture 修订保持 docs-only。
- 本 Verification Thread 只更新本报告。
- 未执行 commit、push、tag、deploy 或 rollback drill。

## 26. V6 focused re-review

结论：**CLOSED**

### 26.1 15 类限制与唯一 final error code

| 限制 | final error code | 结论 |
| --- | --- | --- |
| normalized total bytes > 16 KiB | `PAYLOAD_TOTAL_BYTES_LIMIT` | CLOSED |
| raw total bytes > 64 KiB | `RAW_TOTAL_BYTES_LIMIT` | CLOSED |
| max JSON depth exceeded | `PAYLOAD_DEPTH_LIMIT` | CLOSED |
| object/whole-tree key count exceeded | `PAYLOAD_OBJECT_KEY_COUNT_LIMIT` | CLOSED |
| key UTF-8 bytes exceeded | `PAYLOAD_KEY_BYTES_LIMIT` | CLOSED |
| array/whole-tree array items exceeded | `PAYLOAD_ARRAY_ITEMS_LIMIT` | CLOSED |
| whole-tree node count exceeded | `PAYLOAD_TREE_NODE_LIMIT` | CLOSED |
| normalized string bytes exceeded | `PAYLOAD_STRING_BYTES_LIMIT` | CLOSED |
| raw string bytes exceeded | `RAW_STRING_BYTES_LIMIT` | CLOSED |
| unsupported JSON type | `PAYLOAD_TYPE_FORBIDDEN` | CLOSED |
| NaN / Infinity | `JSON_NUMBER_NON_FINITE` | CLOSED |
| binary/base64/image/opaque encoded log attempt | `RAW_CONTENT_FORBIDDEN` | CLOSED |
| raw parse failure | `RAW_PARSE_ERROR` | CLOSED |
| normalized schema mismatch | `PAYLOAD_SCHEMA_MISMATCH` | CLOSED |
| raw-normalized mismatch | `RAW_NORMALIZED_MISMATCH` | CLOSED |

15 类条件均有唯一 final code；validator 稳定错误码清单也已同步使用新名称，没有保留
与本 mapping 竞争的旧 payload-limit code。

### 26.2 Precedence 与稳定复现

合同冻结了 1～15 的唯一 precedence：

```text
RAW_PARSE_ERROR
→ RAW_CONTENT_FORBIDDEN
→ PAYLOAD_TYPE_FORBIDDEN
→ JSON_NUMBER_NON_FINITE
→ depth
→ object/key
→ array
→ tree node
→ normalized/raw total bytes
→ normalized/raw string bytes
→ schema mismatch
→ raw-normalized mismatch
```

同一 precedence 项存在多个字段错误时，final path 固定为 JSON-style path
lexicographic 最小值，其余只进入 `additional_errors`，不改变 final code。因此
multi-limit fixture 可以稳定断言 code 与 path。

### 26.3 Fail-closed 与业务投影边界

合同明确所有 V6 error：

- reject/fail closed，不截断、不自动修复、不降级 accepted。
- 不产生 production outcome 或 production NOK。
- 不产生 `30003` 或 `UPSTREAM_NOK_SKIPPED`。
- 不产生 ordinary defect 或 Pareto defect。

V6 remaining OPEN item：**无**。

## 27. V7 focused re-review

结论：**CLOSED**

### 27.1 Final decision

最终裁决已唯一冻结：

| business/content/raw comparison | final disposition | audit subtype | final error |
| --- | --- | --- | --- |
| same slot + same content + same raw | `duplicate` | `none` | `null` |
| same slot + same content + different raw | `duplicate` | `raw_variant` | `null` |
| same slot + different content | `conflict` | `none` | multi-key precedence conflict code |

`raw_variant` 明确是 audit subtype，不是新的 disposition。只有 multi-key precedence
已经选定 final duplicate 且 canonical content 相同时，才比较 raw fingerprint 并附加
`raw_variant`。

### 27.2 Canonical fact 与指标边界

`duplicate + raw_variant`：

- 不创建第二个 production fact。
- 不改变首次 accepted canonical result。
- 不进入 OK/NOK/Skip/OEE/Pareto。
- raw fingerprint 不替代 content fingerprint 或 business-slot uniqueness。

content fingerprint 不同时，raw fingerprint 相同或不同都不能改变 `conflict` final
decision，也不能附加 `raw_variant`。

### 27.3 Audit output

合同已冻结：

- `matched_key_type` / `matched_key_value`，用于表达 matched business slot。
- existing event ID。
- existing/incoming content fingerprint。
- existing/incoming raw evidence fingerprint。
- final disposition / final error code。
- `audit_subtype`。
- lower-priority collision 可进入 `additional_matched_keys`，但不能改变 final decision。

这与既有
`event_id → fact_key → cycle-role/result → detail-slot`
multi-key precedence 一致。

V7 remaining OPEN item：**无**。

## 28. V10 focused re-review

结论：**CLOSED WITH RECOMMENDATIONS**

### 28.1 Evaluation order 与 mutual exclusivity

合同冻结八步 evaluation order：

```text
schema
→ config/authority
→ parent/business slot
→ duplicate/conflict
→ predecessor role presence
→ timestamp order
→ projection eligibility
→ completeness/traceability derivation
```

早期 reject/duplicate/conflict 不得被后续派生改写。incoming event final classification
按 reject、duplicate、conflict、heartbeat、NOK relation、accepted production event
分支执行；每个 MVP event 只有一个最终分类。

production role-presence 状态已互斥且穷尽：

| start | complete | 唯一 completeness |
| --- | --- | --- |
| yes | yes | `complete_cycle` |
| no | yes | `partial_cycle_missing_start` |
| yes | no | `partial_cycle_missing_complete` |
| no | no | `partial_cycle_missing_start_and_complete` |

### 28.2 Start/complete 双缺失

accepted `station_result` 且 start/complete 都不存在时唯一输出为：

```text
disposition=accept
lifecycle_state=partial_cycle_missing_start_and_complete
cycle_completeness=partial_cycle_missing_start_and_complete
timeline_status=result_only
projection_eligible=true
traceability_status=unit_traceable when unit_id or dmc exists, otherwise cycle_only
```

后补 start 或 complete 的状态迁移也已逐路径冻结；后补只重算 derived metadata，不重复
或改写 canonical result。

### 28.3 Derived output interface

独立接口已冻结：

```text
derive_lifecycle(
  event,
  validation_decision,
  accepted_cycle_roles,
  accepted_parent
) -> LifecycleDerivedOutput
```

八个字段为：

1. `lifecycle_state`
2. `cycle_completeness`
3. `traceability_status`
4. `timeline_status`
5. `projection_eligible`
6. `parent_relation_status`
7. `detail_relation_status`
8. `late_status`

第八个字段 `late_status` 在 MVP 固定为
`not_evaluated_future_runtime`，明确表示 late threshold、watermark 与 arrived-late
metadata 尚未由本 Sprint 评估。

### 28.4 保留边界

- heartbeat 固定 `diagnostic_only`，不具备 projection eligibility。
- unit/DMC 都 absent 的 accepted production event 固定为 `cycle_only`，不得展示为完整
  unit genealogy。
- out-of-order 保留 arrival/source facts，不改写 source timestamp。
- timestamp reversal 只形成 diagnostic/derived timeline status，不重排 source fact。
- late 继续 future-only。

### 28.5 Non-blocking recommendations

1. implementation fixture 应逐行断言全部八个 derived fields，不只断言
   `cycle_completeness`。
2. `projection_eligible` 已通过 classification table 冻结为 boolean 语义；后续 docs
   hygiene 可在字段枚举表中补一行 `true | false`，避免读者只从 projection column
   推导类型。
3. `dynamic_station_model.md` 的 future projection field list 当前列出七个查询字段，
   未重复列出总括性的 `lifecycle_state`；这不影响 station-event contract 的八字段
   interface，但未来若持久化完整 output，应明确是否同步保存该总括字段。

以上建议不影响 mutual exclusivity、双缺失结果或 interface 可执行性。

V10 remaining OPEN item：**无**。

## 29. 回归与新 blocker 检查

- V6 修订未改变 normalized/raw 16/64 KiB、JSON-only、authority chain 或 mismatch
  business boundary。
- V7 修订未改变 event/fact/cycle/detail identity、content fingerprint 或 multi-key
  conflict precedence。
- V10 修订未改变 canonical result authority、NOK parent relation、out-of-order source
  preservation、heartbeat diagnostic-only 或 late future-only。
- 未发现 V1～V5、V8～V9、V11 的直接回归。
- 新 Verification blocker：**无**。

## 30. Focused re-review Gate 建议

本轮 Verification focused re-review 总结论：

```text
PASS WITH RECOMMENDATIONS
```

| 决策 | Verification 建议 |
| --- | --- |
| V6 | **CLOSED** |
| V7 | **CLOSED** |
| V10 | **CLOSED WITH RECOMMENDATIONS** |
| remaining HOLD blocker | **无** |
| 是否回 Architecture 做 blocker 返修 | **否** |
| Reliability re-review | **不需要** |
| Data Quality re-review | **建议仅对 V10/R5 做定向确认，不重开 R1～R4** |
| 是否可以进入 implementation | **Verification 无 blocker；完成 Data Quality V10/R5 定向确认并由 ChatGPT PM 明确授权后可以** |
| docs-only commit/push | **可以由 PM 决定；必须使用精确 allowlist，不得解释为 implementation authorization** |

## 31. 本轮文件与操作范围

本轮只更新：

- `docs/reports/sprint2_station_event_verification_matrix.md`

本轮未修改：

- Architecture contracts / planning / handoff。
- `docs/reports/sprint2_station_event_reliability_review.md`。
- `docs/reports/sprint2_station_event_data_quality_review.md`。
- code / tests / runtime。
- Collector / API / DB / Dashboard / V-PLC。

本轮未执行：

- 创建 `common/station_event/`。
- implementation。
- commit / push / tag / deploy。
- rollback drill。
- `git add .`。

当前 Verification 控制结论以第 30 节为准；第 1～23 节 HOLD 保留为历史审计证据。
