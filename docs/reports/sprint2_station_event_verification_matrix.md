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

---

## 32. Sprint 2 Implementation Verification Review（2026-06-21）

本节记录对基线
`e9abe45 Finalize Sprint 2 station event review gates`
之后未提交 Generic Station Event Model MVP implementation 的独立复验。第 30 节是
implementation 前合同 Gate；当前 implementation Gate 结论以本节为准。

总结论：**HOLD**

Gate results:

- V1 Scope/isolation：**PASS**。工作树实现范围为独立
  `common/station_event/`、`tests/test_station_event_model.py`、implementation report
  与 Architecture handoff/context 更新；Collector、API、DB、Dashboard、Grafana、
  V-PLC、migration 与 Phase-1 runtime 无 diff。未 commit/push/tag/deploy/rollback
  drill。
- V2 MVP event schema：**PASS**。validator accepted enum 只有五类 MVP event；
  `station_skip/station_hold/station_release/station_rework/station_fault/buffer_enter/
  buffer_exit` 只存在于 `FUTURE_RESERVED_EVENT_TYPES`。
- V3 Dataclass/serializer/validator：**PASS WITH RECOMMENDATIONS**。model 使用 frozen
  dataclass，nested payload/correlation 被递归冻结；无 Pydantic、ORM 或 DB binding；
  serializer、fingerprint、validator 分离，canonical dict/JSON 与 mutation isolation
  有测试。
- V4 Payload/raw validation：**HOLD**。16/64 KiB、JSON type、depth/key/array/node/
  string/number、错误码 precedence 与 reject boundary 已实现并通过现有测试；但
  `RAW_CONTENT_FORBIDDEN` 只按四个 key 名
  `base64/binary/image/opaque_log` 拒绝。独立探针
  `raw_payload={"blob":"data:image/png;base64,..."}` 被接受，未满足合同对 binary/
  base64/image/opaque encoded content fail-closed 的要求。现有 64 tests 没有该负例，
  也没有系统覆盖各资源限制的 limit-1/limit/limit+1。
- V5 Fingerprint/idempotency：**PASS**。same content/same raw 为 duplicate；same
  content/different raw 为 `duplicate + audit_subtype=raw_variant`；different content
  为 conflict。raw variant 不创建第二个 fact、不改变 result、不投影指标。canonical
  key ordering、array order、numeric vectors、raw fingerprint 与 absent/null policy
  有覆盖。
- V6 NOK policy：**HOLD**。canonical result/detail authority 与 projection separation
  已实现，但 stateful relation 有三项阻塞缺口：
  1. `30003/system_reserved` parent 检查在确认 `result=skip` 后提前返回，未校验
     line/plc/station/boot/counter/cycle/unit/DMC 一致；跨 station/cycle skip parent
     被接受。
  2. secondary detail 未校验 `nok_code` 必须不同于 parent primary code；相同 code
     的 secondary 被接受。
  3. `validated_nok_detail` evidence 只确认 cited detail 自身无 `result`，没有解析并
     验证其 accepted canonical parent `station_result(result=nok)`；也未执行 current
     station direct-enabled-predecessor 与 subject lineage 校验。无 canonical parent
     lookup 的 detail evidence 被接受。
- V7 Lifecycle/temporal：**PASS WITH RECOMMENDATIONS**。`LifecycleDerivedOutput`
  八字段完整；四种 completeness 逐字段断言，late 固定
  `not_evaluated_future_runtime`，heartbeat diagnostic-only，cycle-only、
  out-of-order 与 timestamp reversal 均有测试。建议补齐 reject/detail/heartbeat 每个
  branch 的八字段 table-driven assertions。
- V8 Projection：**PASS**。`station_result` 是唯一 authoritative production outcome；
  compatibility projection 标记 non-authoritative；ordinary `station_nok` 只产生
  detail row；reserved 30003、reject、duplicate、conflict 均不投影。
- V9 Test quality：**HOLD**。`64 passed`、`152 passed`、`141 passed` 与 compileall
  均可独立复现，但 64 focused cases 未覆盖上述五个独立对抗性负例。根目录无参数
  pytest 的 10 个 collection errors 可确认为既有多服务顶层 `app` import layout：
  当前 implementation 未修改 `api/collector/s7_plc_sim`，且按既有独立运行方式可复现
  API `5 passed`、Collector `12 passed, 3 subtests passed`、V-PLC `27 passed`。这些
  collection errors 与本次 diff 无关，但 focused suite 的缺口会掩盖本次实现问题。

Blockers:

- B1：stateful validation 取得 resolved config snapshot 后只比较 `config_hash`，没有
  用该 snapshot 重新执行 station/PLC/type/profile/mapping/template lineage 校验；
  独立探针中的 `WS99` event 被接受。
- B2：`30003/system_reserved` detail 可关联跨 station/cycle 的 skip parent。
- B3：secondary NOK detail 可复用 canonical primary `nok_code`。
- B4：`validated_nok_detail` evidence 未验证 accepted canonical NOK parent、direct
  predecessor 与 current-event subject lineage。
- B5：opaque base64/image raw content 可通过非 denylist key 绕过
  `RAW_CONTENT_FORBIDDEN`。
- B6：现有 focused tests 未覆盖 B1～B5。

Required Architecture repairs:

- **不需要修改合同语义**。当前 `station_event_model.md` 已明确 B1～B5 的 expected
  behavior；需要 Implementation Thread 按现有合同做最小代码与 focused test 修复。

Recommendations:

- 将 B1～B5 各增加至少一个 reject regression test，并用 table-driven tests 覆盖
  parent/evidence/config mismatch。
- payload/raw 边界补齐 limit-1、limit、limit+1，尤其 total bytes、string、array、
  node/depth。
- 对 `validated_nok_detail` 增加完整 fixture：cited detail、canonical NOK parent、
  current skip parent、route/config snapshot 与 state-index records。
- 保持无参数全仓 pytest import layout 本 Sprint 不修；继续记录各服务独立测试命令。

Need Reliability focused review:

- **yes**。B2～B4 直接触及 Reliability 已关闭的 N5/N7/N8 stateful parent/evidence/
  detail-set 语义；Implementation 修复后应做一次仅针对这些项的 focused re-review。

Need Data Quality focused review:

- **yes**。B1、B4、B5 影响 R1 lineage、R3 raw evidence authority 与 R5 lifecycle/
  traceability 输入可信度；只需 focused review，不重开已通过的其他范围。

Eligible for implementation commit/push:

- **no**
- 条件：B1～B5 修复；新增回归测试；station-event focused、root `tests/`、Sprint 1 +
  Sprint 2 focused、compileall、各服务独立 regressions 与 `git diff --check` 重新通过；
  Reliability/Data Quality focused re-review 无 blocker；再由 PM 明确授权 commit/push。

Scope checks:

- Collector/API/DB/Dashboard/V-PLC modified：**no**
- migration created：**no**
- tag created：**no**；当前只有 `phase1-pass-20260619`
- deploy：**no**
- rollback drill：**no**
- PM handoff / progress report / docs/superpowers staged or modified：**未 staged，仍为
  untracked 并排除在本次 review/commit scope 外**

Test evidence:

- compileall：**PASS**
- focused pytest：**64 passed in 0.05s**
- broader pytest：root `tests/` **152 passed in 1.30s**；Sprint 1 + Sprint 2 focused
  **141 passed in 1.29s**；API **5 passed**；Collector **12 passed, 3 subtests passed**；
  V-PLC **27 passed**
- git diff --check：**PASS**
- known unrelated failures：repo root 无参数 pytest 在 collection 阶段出现 **10 个
  `ModuleNotFoundError: app`**；原因是 API、Collector、V-PLC 各自使用顶层 `app`
  package，需要独立 cwd/PYTHONPATH。相关模块相对 `e9abe45` 无 diff。

Independent adversarial evidence:

```text
PROBE1_CONFIG_STATION_MISMATCH accept None
PROBE2_RESERVED_CROSS_CYCLE_PARENT accept None
PROBE3_SECONDARY_SAME_PRIMARY_CODE accept None
PROBE4_DETAIL_EVIDENCE_WITHOUT_CANONICAL_PARENT_LOOKUP accept None
PROBE5_OPAQUE_BASE64_IMAGE True []
```

上述五项按当前合同均应 reject，因此 implementation Gate 必须 HOLD。

Thread Health:

- 本 Thread 已完成的主要任务：必读材料恢复、scope/isolation 审计、V1～V9
  implementation review、官方测试复验、多服务 collection-error 归因、五项对抗性负例
  复现与 Gate 判断。
- 当前上下文是否仍适合继续：**适合完成本次 review 收口；不适合在同一任务中直接修改
  implementation，因为本 Thread 角色被限定为只读 Verification。**
- 是否建议新开 Thread：**yes，交回 Implementation Thread 做 B1～B5 最小修复。**
- 如果建议新开，请给出 handoff 摘要：基线 `e9abe45`；当前 Gate HOLD；只修 B1～B5
  并新增对应 tests；不改合同、不接 runtime、不改 migration；修复后回 Reliability/
  Data Quality focused review，再回 Verification re-gate。
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：**低**。关键合同、
  Reliability/Data Quality/Verification 历史、implementation report、实现与 tests 已
  在本 Thread 读取；新 Thread 仍应按 handoff 重新读取本节和
  `station_event_model.md` 的 parent/evidence/config/raw 相关段落。

本轮 Verification 只修改本报告；未修改 implementation、tests、合同、handoff、
Collector、API、DB、Dashboard 或 V-PLC，未 commit/push/tag/deploy/rollback drill。

---

## 33. Sprint 2 Implementation Verification Focused Re-review（2026-06-22）

本节只复验第 32 节 B1～B5 repair，不重开完整 Sprint 2 planning / implementation
review。当前 focused re-review 结论以本节为准。

总结论：**HOLD**

Focused blocker status:

- B1 historical config snapshot lineage：**CLOSED**。stateful validation 在
  `lookup_resolved_config(config_hash)` 后重新执行 `validate_event(raw, config)`；
  missing station、station mismatch、missing profile 与 profile mismatch 均 fail
  closed，matching historical station/profile snapshot accepted。独立重放原
  `WS99` 绕过得到 `reject / CONFIG_NOT_FOUND`。
- B2 30003 parent isolation：**CLOSED**。`30003/system_reserved` parent 必须是
  accepted canonical `station_result(result=skip)`，并逐字段匹配
  line/PLC/station/boot/cycle/counter/unit/DMC。cross-station、cross-cycle 与 future
  parent 均 reject；合法 same-cycle skip parent accepted，但 projection 保持
  non-production isolated，不进入 ordinary defect/Pareto。technical failure evidence
  仍 reject。
- B3 secondary NOK duplicate code：**CLOSED**。secondary 仍要求 accepted primary；
  与 primary code 重复或与已有 secondary code 重复均
  `reject / DETAIL_CODE_DUPLICATE`，distinct secondary accepted。没有 secondary 时
  primary-only 状态稳定 accepted；缺 primary 的 secondary 继续
  `PRIMARY_DETAIL_REQUIRED`。
- B4 validated_nok_detail canonical parent：**CLOSED**。cited detail 必须无
  authoritative result，并解析到 accepted canonical
  `station_result(result=nok)` parent；missing parent 返回
  `UPSTREAM_EVIDENCE_NOT_FOUND`，OK/duplicate/conflict/rejected parent 与 route/subject
  mismatch 返回 `UPSTREAM_EVIDENCE_INVALID`。direct predecessor、unit/DMC、config 与
  parent identity 均有 focused tests。
- B5 base64/image raw bypass：**STILL OPEN**。已关闭上一轮
  `data:image/...;base64,...`、PNG/JPEG/GIF/BMP magic、`image/image_base64/blob/binary/
  file` key hint 与多行重复日志样例；normal short raw strings accepted。但独立同类探针
  仍确认：
  - WebP base64 magic `UklGR...` 放在普通 `payload` key 下被 accepted。
  - PDF/binary base64 `JVBERi0...` 放在普通 `payload` key 下被 accepted。
  - 约 7 KiB 的单行重复 log-like string 被 accepted。

  这些输入直接落在本轮要求的“JSON string 中夹带图片/二进制、obvious base64
  image-like、repeated/unbounded log-like string”范围，因此 B5 尚未 fail closed。

Blockers:

- B5：raw content detection 仍依赖有限 key/magic denylist 与“多行重复”启发式，
  WebP/通用 binary base64 和单行重复日志仍可绕过 `RAW_CONTENT_FORBIDDEN`。
- B5 focused tests 未包含上述三类直接同类负例。

Required Architecture repairs:

- **不需要修改合同语义**。合同已经明确禁止 binary/base64/image 与
  opaque/unbounded log；Implementation Thread 需继续做 B5 最小修复并新增回归测试。

Recommendations:

- raw string fail-closed 规则不要只枚举 PNG/JPEG/GIF/BMP magic；至少覆盖 WebP 与常见
  binary/file magic，或使用受控 raw text allowlist/grammar，避免继续扩充脆弱 denylist。
- repeated/unbounded log detection 同时覆盖多行与单行重复模式，并保持 normal short
  diagnostic text accepted。
- B5 新增 table-driven tests：WebP、PDF/通用 binary base64、单行重复日志、正常短文本。

Need Reliability focused review:

- **yes**。B2～B4 已通过本轮 Verification focused re-review，可进入 Reliability
  parent/evidence/detail-set focused review；无需等待 B5。

Need Data Quality focused review:

- **yes，但尚不能完成最终 focused sign-off**。B1/B4 已关闭，可先复验 lineage 与
  canonical parent；B5 属 R3 raw evidence authority，需等 B5 再修后一起关闭。

Eligible for implementation commit/push:

- **no**
- Conditions：B5 完整关闭；新增 WebP/binary-base64/single-line-log regression tests；
  station-event focused、root `tests/`、Sprint 1 + Sprint 2 focused、compileall 与
  `git diff --check` 重新通过；Reliability/Data Quality focused review 无 blocker；
  ChatGPT PM 明确授权 commit/push。

Scope checks:

- Collector/API/DB/Dashboard/V-PLC modified：**no**
- migration created：**no**
- tag created：**no**；当前仍只有 `phase1-pass-20260619`
- deploy：**no**
- rollback drill：**no**
- commit/push：**no**
- PM handoff / progress report / docs/superpowers staged or modified：**未 staged，仍为
  untracked，未纳入 implementation/repair scope**

Test evidence:

- compileall：**PASS**
- focused station_event：**89 passed in 0.10s**
- broader tests：root `tests/` **177 passed in 1.28s**；Sprint 1 + Sprint 2 focused
  **166 passed in 1.28s**
- git diff --check：**PASS**
- known unrelated failures：repo-root 无参数 pytest 仍在 collection 阶段出现 **10 个
  `ModuleNotFoundError: app`**；API、Collector、V-PLC 使用各自顶层 `app` package，
  与本次 repair diff 无关。

Independent focused evidence:

```text
B1_WRONG_STATION reject CONFIG_NOT_FOUND
B1_MATCHING_SNAPSHOT accept None
B2_CROSS_PARENT reject PARENT_EVENT_INVALID
B2_LEGAL_SKIP_PARENT accept None
B3_PRIMARY_CODE_DUP reject DETAIL_CODE_DUPLICATE
B3_SECONDARY_CODE_DUP reject DETAIL_CODE_DUPLICATE
B3_DISTINCT_SECONDARY accept None
B4_MISSING_CANONICAL_PARENT reject UPSTREAM_EVIDENCE_NOT_FOUND
B4_REJECTED_CANONICAL_PARENT reject UPSTREAM_EVIDENCE_INVALID
B4_ACCEPTED_CANONICAL_PARENT accept None
B5_DATA_URI False [('RAW_CONTENT_FORBIDDEN', 'raw_payload.blob')]
B5_PNG_MAGIC False [('RAW_CONTENT_FORBIDDEN', 'raw_payload.payload')]
B5_WEBP_MAGIC True []
B5_PDF_BASE64 True []
B5_SINGLE_LINE_REPEATED_LOG True []
B5_NORMAL_SHORT True []
```

Files changed by this review:

- `docs/reports/sprint2_station_event_verification_matrix.md`

Thread Health:

- 本 Thread 已完成的主要任务：重读上轮 HOLD 与 repair 状态；逐项审计 B1～B5
  实现/测试；复现 89/177/166 tests；重放上一轮攻击样例；对 B5 同类边界做独立探针；
  完成 focused Gate 判断。
- 当前上下文是否仍适合继续：**适合完成本轮 Verification 收口；不适合直接修改
  implementation，因为本 Thread 角色限定为 focused re-review。**
- 是否建议新开 Thread：**yes，交回 Implementation/Architecture repair Thread，仅继续
  修 B5。**
- 如果建议新开，请给出 handoff 摘要：基线 `e9abe45`；B1～B4 CLOSED；B5 STILL
  OPEN；只修 WebP/通用 binary base64 与单行重复 log bypass，并增加对应 tests；不改
  合同、不接 runtime、不改 migration；修复后回 Verification B5-only re-review，并由
  Data Quality 完成 R3 focused sign-off。
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：**低**。新 Thread
  仍应读取本节、第 32 节、implementation report、`validation.py` raw content helper
  与 B5 tests。

本轮 Verification 未修改 implementation、tests、合同、handoff、Collector、API、DB、
Dashboard 或 V-PLC，未 commit/push/tag/deploy/rollback drill。

---

## 35. Sprint 2 Verification B5-final Re-review（2026-06-22）

本节只复验第 34 节 B5-R1/R2，不重开 B1～B4 或完整 implementation review。当前
B5-final 结论以本节为准。

总结论：**PASS**

B5 final status:

- periodic repeated substring/log detection：**CLOSED**。约 7 KiB 的
  `ERR42|WARN99|OK;`、`abc123XYZ-`、
  `station=WS1;cycle=C001;result=NOK;` 与上一轮
  `fault-code-17|station-WS02|` 周期模式均稳定
  `reject / RAW_CONTENT_FORBIDDEN`。实现使用 4 KiB 后启用的 bounded zlib
  compression signal，不依赖固定 32-byte chunk 边界；token、character、multiline
  与 chunk rules 仍作为附加 fail-closed 检查。正常短 note/message 与合理非重复长文本
  accepted。
- binary/base64-overlimit precedence：**CLOSED**。超过 raw string limit 的 PDF、
  WebP、generic binary base64、image/webp data URI、application/pdf data URI、
  application/octet-stream data URI，以及 oversized PDF/octet-stream MIME 均以
  `RAW_CONTENT_FORBIDDEN` 作为第一错误；普通 oversized non-binary text 仍为
  `RAW_STRING_BYTES_LIMIT`。实现只扫描最多 4096 encoded characters 的 prefix，并仅
  解码该有界 sample，没有完整 decode 巨大字符串。

Blockers:

- 无

Required Architecture repairs:

- 不需要

Recommendations:

- 保留 periodic fragments、oversized forbidden precedence、normal short text 和
  non-repeated long text fixtures，后续修改 raw validator 时作为固定 regression
  matrix。
- future 若调整 compression ratio / sample size，应由 Data Quality 与 Verification
  重新评估 false-positive / false-negative 边界。

Need Reliability focused review:

- **yes**。Verification 已关闭 B1～B5；按既定流程，Reliability 仍需对已关闭的
  B2～B4 parent/evidence/detail-set repair 做 focused sign-off。

Need Data Quality focused review:

- **yes**。B1/B4 lineage 与 B5 raw evidence authority 现已通过 Verification，可进入
  Data Quality focused sign-off。

Eligible for implementation commit/push:

- **no，尚需后续 Gate**
- Conditions：Reliability B2～B4 focused review PASS；Data Quality B1/B4/B5 focused
  review PASS；ChatGPT PM 汇总并明确授权；提交时使用精确 allowlist，继续排除 PM
  handoff、当前进度报告与 `docs/superpowers/`。

Scope checks:

- B1-B4 logic changed：**no**
- Collector/API/DB/Dashboard/V-PLC modified：**no**
- migration created：**no**
- tag created：**no**；当前仍只有 `phase1-pass-20260619`
- deploy：**no**
- rollback drill：**no**
- commit/push：**no**
- PM handoff / progress report / docs/superpowers staged or modified：**未 staged，仍为
  untracked，未纳入 implementation repair**

Test evidence:

- compileall：**PASS**
- focused station_event：**107 passed in 0.08s**
- broader tests：root `tests/` **195 passed in 1.29s**
- git diff --check：**PASS**
- known unrelated failures：repo-root 无参数 pytest 仍在 collection 阶段出现 **10 个
  `ModuleNotFoundError: app`**；属于既有 API/Collector/V-PLC 顶层 `app` import
  layout，与 B5 final repair 无关。

Independent B5-final evidence:

```text
ERR_WARN_OK reject RAW_CONTENT_FORBIDDEN
ABC_PATTERN reject RAW_CONTENT_FORBIDDEN
STRUCTURED_LOG reject RAW_CONTENT_FORBIDDEN
PRIOR_FRAGMENT reject RAW_CONTENT_FORBIDDEN
NORMAL_SHORT_NOTE accept
NORMAL_SHORT_MESSAGE accept
NORMAL_NONREPEATED_LONG accept
OVERSIZED_PDF_BASE64 first error RAW_CONTENT_FORBIDDEN
OVERSIZED_WEBP_BASE64 first error RAW_CONTENT_FORBIDDEN
OVERSIZED_GENERIC_BASE64 first error RAW_CONTENT_FORBIDDEN
OVERSIZED_WEBP_DATA_URI first error RAW_CONTENT_FORBIDDEN
OVERSIZED_PDF_DATA_URI first error RAW_CONTENT_FORBIDDEN
OVERSIZED_OCTET_DATA_URI first error RAW_CONTENT_FORBIDDEN
OVERSIZED_PDF_MIME first error RAW_CONTENT_FORBIDDEN
OVERSIZED_OCTET_MIME first error RAW_CONTENT_FORBIDDEN
OVERSIZED_NONBINARY_TEXT first error RAW_STRING_BYTES_LIMIT
```

Files changed by this review:

- `docs/reports/sprint2_station_event_verification_matrix.md`

Thread Health:

- 本 Thread 已完成的主要任务：读取 B5-final repair 与最新 Gate；审计 bounded
  compression/prefix implementation 和新增 tests；复现 107/195 tests；独立验证任务
  指定 periodic patterns、oversized binary categories、precedence 与 positive
  guardrails；完成 B5-final Gate 判断。
- 当前上下文是否仍适合继续：**适合完成 Verification 收口；后续角色应切换到独立
  Reliability / Data Quality focused review。**
- 是否建议新开 Thread：**yes**。
- 如果建议新开，请给出 handoff 摘要：基线 `e9abe45`；Verification implementation
  B1～B5 全部 CLOSED；B5-final PASS；implementation 未提交；下一步 Reliability
  focused review B2～B4 与 Data Quality focused review B1/B4/B5，均通过后交 PM
  授权 commit/push；不得进入 integration。
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：**低**。新 Thread
  应读取第 32～35 节、implementation report 与相应合同段落。

本轮 Verification 未修改 implementation、tests、合同、handoff、Collector、API、DB、
Dashboard 或 V-PLC，未 commit/push/tag/deploy/rollback drill。

---

## 34. Sprint 2 Verification B5-only Re-review（2026-06-22）

本节只复验第 33 节唯一 remaining blocker B5，不重开 B1～B4 或完整 implementation
review。当前 B5-only 结论以本节为准。

总结论：**HOLD**

B5 status:

- WebP base64：**CLOSED**。`data:image/webp;base64,...` 与普通
  `raw/payload/note/content` key 下的 WebP base64 均
  `reject / RAW_CONTENT_FORBIDDEN`。实现通过 base64 decode 后检查
  `RIFF....WEBP`，不依赖 PNG/JPEG denylist；focused tests 与独立生成 bytes probe
  均通过。
- PDF/generic binary base64：**CLOSED**。PDF data URI、`application/pdf`、
  `application/octet-stream`、普通 key 下 `%PDF` base64 与高比例不可打印 generic
  binary base64 均 `RAW_CONTENT_FORBIDDEN`。正常短 note、DMC、station note、ordinary
  message 与合理非重复长文本 accepted。
- ordinary-key binary base64：**CLOSED**。即使 key 是 `raw/payload/note/content`，
  validator 仍解码 base64，并根据 PDF/WebP header 或不可打印字节比例 reject；key
  hint 是额外防线而非唯一防线。printable text 的 base64 表示未被误判为 binary。
- repeated single-line log：**STILL OPEN**。约 7 KiB 的重复 token 与重复字符已
  `RAW_CONTENT_FORBIDDEN`，但约 7 KiB 的重复片段
  `fault-code-17|station-WS02|` 循环字符串仍被 accepted。该输入长度低于 16 KiB /
  64 KiB 资源上限，直接属于本轮要求的“重复片段构成的 log-like raw string”，因此
  B5 未完全关闭。
- raw-text grammar / allowlist strategy：**STILL OPEN**。实现已有明确的 4 KiB 启用
  阈值、MIME/data URI 类别拒绝、base64 decode + binary ratio、token/字符/chunk
  重复率与 false-positive guardrails；但当前固定 32-character chunk 切分不能识别与
  chunk 边界不对齐的周期片段。另外，明显 PDF/binary base64 超过 raw string 16 KiB
  时，helper 在内容检查前直接返回，最终错误为 `RAW_STRING_BYTES_LIMIT`，未保持合同
  `RAW_CONTENT_FORBIDDEN` 高于 string limit 的 precedence。

Blockers:

- B5-R1：长单行周期片段重复字符串仍可绕过 repeated/unbounded log detection。
- B5-R2：超过 raw string limit 的明显 binary/base64 内容未先形成
  `RAW_CONTENT_FORBIDDEN`，错误 precedence 不符合合同。
- focused tests 未覆盖非 32-byte 对齐的重复片段与 binary/base64 + string-limit
  multi-error precedence。

Required Architecture repairs:

- **不需要修改合同语义**。Implementation Thread 需继续做 B5 最小修复：
  1. 使用与固定 chunk 边界无关的周期/片段重复率检测。
  2. 对超长 raw string 仍先执行有界 prefix/category binary detection，保证
     `RAW_CONTENT_FORBIDDEN` precedence；不得完整解码无界内容。
  3. 增加两组 regression tests。

Recommendations:

- 周期检测使用有界 rolling window、prefix sampling 或最小周期检测，避免只按固定
  32-byte chunk 分桶。
- binary precedence 检查只需对有界 prefix 做 data URI/MIME/base64/header/category
  判断，避免增加资源风险。
- 保留当前正常短文本、printable base64 text 和合理非重复长文本 positive fixtures。

Need Reliability focused review:

- **yes**。与 B5 无关的 B2～B4 已 CLOSED，可进入 Reliability focused review。

Need Data Quality focused review:

- **yes，但 R3 raw evidence 最终 sign-off 仍需等待 B5-R1/R2 关闭**。当前 WebP/PDF/
  generic binary 分类已可复验，repeated-fragment 与 precedence 仍未关闭。

Eligible for implementation commit/push:

- **no**
- Conditions：关闭 B5-R1/R2；新增 periodic-fragment 与 binary+overlimit precedence
  tests；focused、broader、compileall、`git diff --check` 重新通过；Reliability/Data
  Quality focused review 无 blocker；ChatGPT PM 明确授权。

Scope checks:

- B1-B4 logic changed：**no（本轮只读审计未发现 B5 repair 以外的新增改动）**
- Collector/API/DB/Dashboard/V-PLC modified：**no**
- migration created：**no**
- tag created：**no**；当前仍只有 `phase1-pass-20260619`
- deploy：**no**
- rollback drill：**no**
- commit/push：**no**
- PM handoff / progress report / docs/superpowers staged or modified：**未 staged，仍为
  untracked，未纳入 implementation repair**

Test evidence:

- compileall：**PASS**
- focused station_event：**101 passed in 0.10s**
- broader tests：root `tests/` **189 passed in 1.34s**
- git diff --check：**PASS**
- known unrelated failures：repo-root 无参数 pytest 仍在 collection 阶段出现 **10 个
  `ModuleNotFoundError: app`**；属于既有多服务顶层 `app` import layout，与 B5 repair
  无关。

Independent B5 evidence:

```text
WEBP_DATA_URI reject RAW_CONTENT_FORBIDDEN
WEBP ordinary raw/payload/note/content reject RAW_CONTENT_FORBIDDEN
PDF_DATA_URI reject RAW_CONTENT_FORBIDDEN
OCTET_DATA_URI reject RAW_CONTENT_FORBIDDEN
PDF/OCTET MIME reject RAW_CONTENT_FORBIDDEN
PDF ordinary raw/payload/note/content reject RAW_CONTENT_FORBIDDEN
GENERIC binary ordinary raw/payload/note/content reject RAW_CONTENT_FORBIDDEN
TOKEN_REPEAT_7K reject RAW_CONTENT_FORBIDDEN
CHAR_REPEAT_7K reject RAW_CONTENT_FORBIDDEN
FRAGMENT_REPEAT_7K accept
NON_REPEATED_LONG accept
SHORT_NOTE / DMC / STATION_NOTE / ORDINARY_MESSAGE accept
PRINTABLE_BASE64_TEXT accept
PRECEDENCE_BINARY_AND_LONG reject RAW_STRING_BYTES_LIMIT
```

Files changed by this review:

- `docs/reports/sprint2_station_event_verification_matrix.md`

Thread Health:

- 本 Thread 已完成的主要任务：读取 B5 finding/repair/contract/helper/tests；复现
  101/189 tests；审计 scope；独立验证 WebP、PDF/generic binary、ordinary key、
  repeated log、positive guardrail 与错误 precedence；完成 B5-only Gate 判断。
- 当前上下文是否仍适合继续：**适合完成本轮 Verification 收口；不适合直接修代码。**
- 是否建议新开 Thread：**yes，交回 Implementation/Architecture，仅修 B5-R1/R2。**
- 如果建议新开，请给出 handoff 摘要：基线 `e9abe45`；WebP、PDF/generic binary、
  ordinary-key base64 已 CLOSED；只修周期片段重复绕过和 binary+overlimit precedence；
  增加对应 tests；不动 B1～B4、不接 runtime；修复后回 Verification B5 final
  re-review，再交 Data Quality R3 focused sign-off。
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：**低**。新 Thread
  应读取本节、第 33 节、implementation report、`_raw_content_forbidden()`、
  `_is_repeated_unbounded_text()` 与 B5 tests。

本轮 Verification 未修改 implementation、tests、合同、handoff、Collector、API、DB、
Dashboard 或 V-PLC，未 commit/push/tag/deploy/rollback drill。

## 37. B5-final 最终控制结论

第 34 节 `HOLD` 是 B5 final repair 前的历史审计；第 35 节为完整 B5-final re-review。
当前最终控制结论：

```text
PASS
periodic repeated substring/log detection: CLOSED
binary/base64-overlimit precedence: CLOSED
Verification implementation blockers B1-B5: all CLOSED
```

下一步进入 Reliability B2～B4 focused review 与 Data Quality B1/B4/B5 focused review；
两者通过并经 ChatGPT PM 明确授权前，仍不得 commit/push 或进入 integration。

---

## 38. Sprint 2 Verification Targeted Relation Sanity Check（2026-06-23）

本节只复验 Reliability R-B2/R-B4 repair 对 Verification relation Gate 的影响，并对
B1/B5 做轻量 sanity check；不重开完整 Verification B1～B5 或 Data Quality review。

结论：**PASS**

Focused status:

- V-R1 30003 / skip parent relation：**PASS**。`30003/system_reserved` 的 accepted
  skip parent 必须通过共享 `_parent_matches()`，其中包含 accepted lookup、
  authoritative production-result authority、same line/PLC/station/boot/cycle/
  counter/unit/DMC/config 与 `event_role=production_result`。cross-config skip parent
  稳定 `reject / PARENT_EVENT_INVALID`；technical-failure/cross-config evidence 稳定
  reject。所有 reject decision 均
  `projection_eligible=false`、`production_outcome=null`、`defect_detail=null`，不进入
  production NOK、ordinary/operator defect 或 Pareto。
- V-R2 validated_nok_detail canonical parent relation：**PASS**。canonical parent
  现在必须同时满足 `event_type=station_result`、`result=nok`、accepted/canonical、
  PLC/PLC 或 V-PLC/simulator authority、same line/PLC/station/boot/cycle/unit-DMC/
  config、primary code/origin 或 secondary origin relation，以及
  `correlation.event_role=production_result`。role 为
  `cycle_complete/diagnostic/compatibility/None` 或缺失、non-authoritative、
  duplicate/conflict/rejected、cross-config/line/station/cycle、primary code mismatch、
  origin mismatch 均稳定 `reject / UPSTREAM_EVIDENCE_INVALID`。detail 自身携带 result
  仍 stateless `FIELD_FORBIDDEN`。合法 PLC primary、V-PLC primary 与 distinct
  secondary path accepted。
- V-R3 historical config snapshot lineage sanity：**PASS**。stateful validation 仍先
  lookup historical config 并重放 line/station/profile/config validation；matching
  snapshot accepted，missing station 为 `CONFIG_NOT_FOUND`，profile mismatch 为
  `EVENT_LINEAGE_INVALID`。parent relation 的 same-config 检查未绕过 snapshot
  lineage。
- V-R4 B5 raw validation sanity：**PASS**。periodic structured repeated substring 与
  forbidden WebP/data-URI fixture 仍 `RAW_CONTENT_FORBIDDEN`；正常短 message/DMC
  accepted。本轮 relation repair 未改 raw validation path，无需重开 B5 full audit。

Findings:

- 无 blocker。
- `production_result` role enforcement 位于共享 `_parent_matches()`，current
  `station_nok` parent 与 `validated_nok_detail` evidence canonical-parent path 使用同一
  relation，避免两条验证路径漂移。
- 正例与 reject projection boundary 均经独立探针确认。

Tests:

- git status：HEAD/origin/main 均为 `e9abe45`；working tree 有既有未提交
  implementation/tests/reports 与 `.gitignore` 修改。本 review 开始前已存在。
- compileall：**PASS**
- focused station_event：**119 passed in 0.06s**
- broader tests：root `tests/` **207 passed in 0.93s**
- targeted relation/B1/B5 tests：**44 passed, 75 deselected in 0.03s**
- git diff --check：**PASS**
- unrelated failures：本轮未运行 repo-root 无参数 pytest；此前既有多服务顶层 `app`
  layout collection errors 不纳入本轮结论。

Independent targeted evidence:

```text
VR1_CROSS_CONFIG_SKIP_PARENT reject PARENT_EVENT_INVALID no projection
VR1_TECH_FAILURE_CROSS_CONFIG reject UPSTREAM_EVIDENCE_INVALID no projection
VR2_VALID_PLC_PRIMARY accept
VR2_VALID_VPLC_PRIMARY accept
VR2_VALID_SECONDARY accept
VR2_ROLE cycle_complete/diagnostic/compatibility/None/missing
  -> reject UPSTREAM_EVIDENCE_INVALID no projection
VR2_STATUS duplicate/conflict/reject
  -> reject UPSTREAM_EVIDENCE_INVALID no projection
VR2_CROSS_CONFIG/LINE/STATION/CYCLE
  -> reject UPSTREAM_EVIDENCE_INVALID no projection
VR2_PRIMARY_CODE/ORIGIN/NON_AUTHORITY
  -> reject UPSTREAM_EVIDENCE_INVALID no projection
VR2_SECONDARY_ORIGIN_MISMATCH
  -> reject UPSTREAM_EVIDENCE_INVALID no projection
VR2_DETAIL_SELF_RESULT -> FIELD_FORBIDDEN
VR3_VALID_SNAPSHOT accept
VR3_MISSING_STATION reject CONFIG_NOT_FOUND
VR3_PROFILE_MISMATCH reject EVENT_LINEAGE_INVALID
VR4_PERIODIC reject RAW_CONTENT_FORBIDDEN
VR4_FORBIDDEN reject RAW_CONTENT_FORBIDDEN
VR4_NORMAL accept
```

Files changed by this review:

- `docs/reports/sprint2_station_event_verification_matrix.md`

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

- Remaining Verification blocker：**no**
- Need Architecture repair：**no**
- Need Reliability re-review：**no**；最新 Reliability focused re-review 已 PASS。
- Need Data Quality focused review：**yes**；由 ChatGPT PM 安排 B1/B4/B5 focused
  implementation review，本 Thread 不扩大执行。
- Eligible for implementation commit/push：**no**；即使本轮 PASS，仍须 Data Quality
  focused review 关闭并由 ChatGPT PM 给出精确 allowlist 授权。

Thread Health:

- 本 Thread 已完成的主要任务：重读 matcher/evidence implementation、targeted tests、
  Verification/Reliability 报告与 handoff；复现 119/207 tests；运行 44 个 targeted
  tests；独立重放 R-B2 cross-config、R-B4 role/authority/config/code-origin/status、
  B1 snapshot 与 B5 smoke probes；形成 targeted PASS。
- 当前上下文是否仍适合继续：**适合完成 Verification targeted 收口；不应在本 Thread
  扩大到 Data Quality 或 commit/push。**
- 是否建议新开 Thread：**yes**。
- 如果建议新开，请给出 handoff 摘要：基线 `e9abe45`；Reliability R-B2/R-B3/R-B4
  CLOSED；Verification targeted relation sanity PASS；B1/B5 sanity 无回归；
  119/207 tests PASS；下一步由 PM 安排 Data Quality B1/B4/B5 focused implementation
  review；其通过前不得 commit/push/integration。
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：**低**。Data
  Quality Thread 应读取本节、Reliability 第 48～49 节、implementation report 第
  11～12 节及对应合同。

本轮只修改 Verification report；未修改 implementation、tests、合同、Collector、API、
DB、Dashboard、V-PLC、migration 或发布状态，未 commit/push/tag/deploy/rollback
drill。

---

## 39. Sprint 2 Verification DQ-F1～DQ-F3 Targeted Sanity Check Result（2026-06-23）

本节只验证 Data Quality DQ-F1～DQ-F3 minimal repair 是否真实落地，以及 repair 是否
造成 Verification regression；不重开完整 Sprint 2 Verification matrix，不进入
integration。

结论：**PASS WITH RECOMMENDATIONS**

### Focused status

- V-DQ1 parent profile/station_type lineage：**PASS**。
  shared `_parent_matches()` 已在既有 line/PLC/station/boot/cycle/counter/unit/DMC/
  config relation 上强制比较 `profile_id` 与 `station_type`。任一 mismatch 均
  `reject / PARENT_EVENT_INVALID`。matcher 继续要求
  `event_type=station_result`、`correlation.event_role=production_result`、
  PLC/PLC 或 V-PLC/simulator authoritative source/actor，以及 primary/secondary
  NOK code-origin relation；`30003` 仍只接受 same-relation `result=skip` parent。
  reject decision 不产生 authoritative production outcome、defect detail、
  compatibility projection 或 projection eligibility，因此不会形成 operator defect、
  Pareto 或其他 production projection input。
- V-DQ2 validated cited detail canonical authority：**PASS**。
  cited detail lookup 必须 accepted，record 必须是无 authoritative `result` 的
  `station_nok`，且
  `correlation.event_role=nok_detail`。随后在 historical config 下重放 ordinary
  `validate_event()`，再 lookup accepted canonical NOK parent 并复用
  `_parent_matches()` 重放完整 relation。compatibility、diagnostic、wrong/missing
  role、non-accepted cited detail、non-accepted parent 与 wrong parent relation 均
  fail closed 为既有 upstream evidence error；reject 不产生 projection。
- V-DQ3 raw authority fail-closed：**PASS**。
  historical snapshot 下只要 `raw_payload` present，就必须提供 callable
  `decode_raw_payload`。missing decoder 或 decoder exception 返回
  `RAW_PARSE_ERROR`；raw-only 或 decoded/normalized canonical mismatch 返回
  `RAW_NORMALIZED_MISMATCH`；raw + normalized exact decoder match 可继续正常验证。
  config/raw validation 位于 duplicate/conflict/detail-slot lookup 前，因此 rejected raw
  evidence 不能先 accepted、不能占据 authoritative slot，也不产生 authoritative
  production outcome。duplicate/conflict/raw_variant function 未被修改：
  same-content/same-raw 仍 duplicate，same-content/different-raw 仍
  `duplicate + RAW_VARIANT`，different-content 仍 conflict。stateful raw_variant
  fixture 同时提供 normalized payload 与 decoder，不绕开 raw authority chain。
- V-DQ4 targeted regression / isolation：**PASS**。
  repair 新增 9 个 focused cases，因此 station-event 从 119 增至 128、root
  `tests/` 从 207 增至 216，增量一致且完整 suite 全部通过。Data Quality targeted
  22 tests 的 DQ-F1～DQ-F3/R3 结论与本轮源码映射、128/216 suite 及独立探针一致，
  不与既有 Verification matrix 冲突。本轮未发现 contracts、Collector、API、DB、
  Dashboard、V-PLC 或 migration 变更。

### Findings

- 未发现新的 Verification blocker。
- DQ-F1～DQ-F3 repair 均位于 shared validation/authority path，不是 fixture-only
  bypass。
- Non-blocking recommendation：在后续允许修改 tests 的独立任务中，可将
  `non-accepted cited detail record` 与 `raw-only + callable decoder` 两个本轮只读
  探针固化为具名 regression。当前探针已分别证明
  `reject / UPSTREAM_EVIDENCE_INVALID` 与 `RAW_NORMALIZED_MISMATCH`，因此不要求
  Architecture 当前扩展，也不阻塞本 Gate。

### Tests

```text
git status:
branch = main
HEAD = e9abe45
working tree contains pre-existing uncommitted implementation/tests/reports/.gitignore

git diff -- common/station_event tests/test_station_event_model.py:
no tracked diff output; both requested paths are pre-existing untracked files

compileall:
PASS

focused station_event:
128 passed in 0.06s

broader tests:
216 passed in 0.95s

Data Quality targeted reference:
22 passed, 106 deselected; conclusions consistent with this review

independent probes:
RAW_ONLY_WITH_DECODER -> RAW_NORMALIZED_MISMATCH, no authoritative outcome
RAW_EXACT_MATCH -> valid
NON_ACCEPTED_CITED_DETAIL -> reject / UPSTREAM_EVIDENCE_INVALID, no projection

git diff --check:
PASS

unrelated failures:
none in the required commands
```

### Files changed by this review

- `docs/reports/sprint2_station_event_verification_matrix.md`

### Scope audit

- implementation code modified：**no**
- tests modified：**no**
- contracts modified：**no**
- Collector/API/DB/Dashboard/V-PLC modified：**no**
- migration created：**no**
- tag created：**no**；仍只有 `phase1-pass-20260619`
- deploy：**no**
- rollback drill：**no**
- commit/push：**no**

### Decision

- Remaining Verification blocker：**no**
- Need Architecture repair：**no**
- Need Data Quality re-review：**no**；最新 targeted re-review 已
  `PASS WITH RECOMMENDATIONS`。
- Need Reliability re-review：**no**；本轮未削弱 Reliability 已关闭 relation/raw
  constraints。
- Eligible for implementation commit/push：**no**。本轮 targeted sanity check 已关闭，
  但仍须由 ChatGPT PM 执行 final pre-commit audit 并给出精确 allowlist；本结论本身不
  授权 commit/push。
- Next recommended step：交 ChatGPT PM 做 final pre-commit audit、working-tree
  allowlist 与精确 staging/commit/push 决策；继续禁止 integration、migration、tag、
  deploy 与 rollback drill。

### Thread Health

- 本 Thread 已完成的主要任务：恢复当前 working-tree gate 上下文；重读指定
  implementation/tests/reports/handoff；逐项验证 V-DQ1～V-DQ4；运行 compileall、
  128/216 tests、diff checks 与 3 个独立探针；形成 targeted Gate 结论。
- 当前上下文是否仍适合继续：**适合完成本轮 Verification 收口；不应在本 Thread
  扩大到 PM pre-commit、staging、commit/push 或 integration。**
- 是否建议新开 Thread：**yes，交 ChatGPT PM final pre-commit audit Thread。**
- 如果建议新开，请给出 handoff 摘要：基线 `e9abe45`；Reliability focused PASS；
  Data Quality DQ-F1～DQ-F3 targeted re-review
  `PASS WITH RECOMMENDATIONS`；Verification V-DQ1～V-DQ4
  `PASS WITH RECOMMENDATIONS`；128/216 tests、compileall、`git diff --check`
  全部 PASS；无 remaining Verification blocker；下一步只做 PM final pre-commit
  audit 与精确 allowlist，未授权前不得 commit/push/integration。
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：**低**。新
  Thread 应读取本节、Data Quality 第 40～41 节、implementation report 第 13 节及
  fresh `git status --short`；不得依赖旧 working-tree inventory。

## 40. Current Verification control conclusion

本节追加于第 38 节 relation sanity PASS 之后，记录 DQ-F1～DQ-F3 repair 的最终
Verification targeted 状态：

```text
PASS WITH RECOMMENDATIONS
V-DQ1 parent profile/station_type lineage: PASS
V-DQ2 validated cited detail canonical authority: PASS
V-DQ3 raw authority fail-closed: PASS
V-DQ4 targeted regression / isolation: PASS
Remaining Verification blocker: no
```

本结论不授权 commit/push。下一步必须由 ChatGPT PM 做 final pre-commit audit 并给出
精确 allowlist；在此之前不得进入 Collector/API/DB/Dashboard/V-PLC integration。

---

## 41. Post-commit closeout current-control note（2026-06-24）

本文件前文保留 Verification matrix、implementation review 与 targeted sanity check
各轮审计当时的 Git 基线、working tree 状态与 handoff 建议；其中 `60adac2`、
`e9abe45`、implementation 未提交、final pre-commit audit 等描述均为历史证据，不再
代表当前 repo 状态。

当前 Sprint 2 source of truth：

```text
HEAD/origin/main: 17cf5d2 Implement Sprint 2 generic station event model
Sprint 2 implementation: committed/pushed
Verification targeted Gate: PASS WITH RECOMMENDATIONS
Remaining Verification blocker: none
runtime integration: not started
migration/tag/deploy/rollback drill: not performed
```

本 closeout note 只同步文档控制状态，不修改 implementation、tests、Collector、API、
DB、Dashboard、V-PLC、migration 或发布状态。
