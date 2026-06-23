# Sprint 2 Station Event Data Quality Review

日期：2026-06-21

审查角色：Data Quality Thread

审查对象：Phase-2 Sprint 2 Generic Station Event Model planning / contract

最终结论：**HOLD / CHANGES REQUIRED**

## 1. 本轮审查范围

本轮只审查 Sprint 2 station event planning / contract 是否足以支撑后续独立 package
实现，重点覆盖：

- canonical event model 与逐事件完整性。
- result / NOK outcome 与 detail 投影。
- normalized payload / raw payload 一致性与资源边界。
- event、fact、cycle-role、detail 与 content fingerprint identity。
- `config_hash`、mapping、template 与 resolved line configuration 血缘。
- 时间、父子关系、late/out-of-order 与 lifecycle coherence。
- future DB、API、Trace、Quality 和 Dashboard 的稳定语义。

本轮不是 implementation，没有修改合同、planning、handoff、代码、tests、runtime、
Collector、API、DB、Dashboard 或 V-PLC。

四个只读 subagent 分别审查：

1. Traceability Auditor：DQ1 / DQ6。
2. Result Projection Auditor：DQ2 / DQ4。
3. Payload Consistency Auditor：DQ3。
4. Identity / Fingerprint Auditor：DQ5。

subagent 只提供 findings；最终状态、blocker 合并和 Gate 建议由本 Data Quality Thread
逐项回到当前工作树合同后确定。

## 2. 读取文件列表

本轮完整读取：

1. `docs/contracts/station_event_model.md`
2. `docs/reports/sprint2_generic_station_event_model_plan.md`
3. `docs/reports/sprint2_station_event_reliability_review.md`
4. `docs/thread_handoff/architecture.md`
5. `docs/reports/architecture_context_restore.md`
6. `docs/contracts/line_configuration.md`
7. `docs/contracts/dynamic_station_model.md`
8. `docs/reports/phase2_sprint_plan.md`
9. `docs/reports/phase2_thread_task_plan.md`
10. `docs/DOC_INDEX.md`
11. `docs/reports/README.md`

## 3. 当前基线确认

执行：

```bash
git status --short
git log --oneline -3
git tag --list
git diff --check
test ! -d common/station_event && echo "common/station_event absent"
git diff -- common/ services/ apps/ tests/ || true
```

结果：

```text
HEAD        60adac2629d499ca5ee923786289c5ccd6d4b6aa
origin/main 60adac2629d499ca5ee923786289c5ccd6d4b6aa
latest      60adac2 Address Sprint 2 station event reliability review
tag         phase1-pass-20260619
common/station_event absent
git diff --check: PASS
code/tests/runtime diff: none
```

最近三个 commit：

```text
60adac2 Address Sprint 2 station event reliability review
45fa2a8 Freeze Sprint 2 station event planning
4215b7c Finalize Sprint 1 architecture handoff and review history
```

审查开始前只有以下用户明确禁止处理的未跟踪项：

```text
?? docs/20260620_03_Edge MES Demo — ChatGPT PM Handoff.md
?? docs/Edge MES Demo 当前进度报告.md
?? docs/superpowers/
```

`common/station_event/` 不存在；Sprint 2 implementation 尚未开始。

说明：部分 Architecture handoff/context 正文仍记录 `45fa2a8`，而当前真实 Git 基线已是
`60adac2`。这是 non-blocking 文档状态漂移，不影响本轮对当前 HEAD 合同内容的审查。

## 4. 分项结论

| 项目 | 结论 | 核心判断 |
| --- | --- | --- |
| DQ1 Traceability completeness | **HOLD / CHANGES REQUIRED** | config hash 基础完整，但 mapping/template version 血缘不够确定 |
| DQ2 Result projection consistency | **HOLD / CHANGES REQUIRED** | event contract 正确，dynamic DB model 仍可重复投影 result |
| DQ3 Payload/raw consistency | **HOLD / CHANGES REQUIRED** | 资源上限明确，但 raw→normalized 权威链和 mismatch 处置未冻结 |
| DQ4 NOK detail quality | **HOLD / CHANGES REQUIRED** | slot/30003 规则正确，但 detail 缺失时 Pareto completeness 未定义 |
| DQ5 Identity/idempotency | **HOLD / CHANGES REQUIRED** | identity 分层正确，但数值 canonicalization、raw evidence 与冲突优先级未冻结 |
| DQ6 Temporal/lifecycle coherence | **HOLD / CHANGES REQUIRED** | heartbeat/parent 规则完整，但 late 与 cycle lifecycle matrix 缺失 |
| DQ7 Future API/Dashboard implications | **HOLD / CHANGES REQUIRED** | 可支持基础查询，但结果权威、partial metrics、raw audit 和 lifecycle 状态尚不稳定 |

Reliability 当前 `PASS WITH RECOMMENDATIONS` 不被本报告重新打开。Reliability 已关闭的
N5/N6/N7/N8、UNKNOWN、payload resource limits 和 event presence 继续保持 CLOSED。
本报告发现的是独立的 Data Quality 与跨合同投影问题。

## 5. DQ1 — Traceability completeness

结论：**HOLD / CHANGES REQUIRED**

### 已通过

五类 MVP event 都要求：

- envelope/schema/event identity 与 source timestamp。
- `line_id / plc_id / station_id / station_type`。
- `config_version / config_hash`。
- `source / actor`。
- `correlation.source_event_id / fact_key / event_role`。

cycle/result/NOK 另外包含 boot、profile、cycle ID 和 counter；NOK detail 包含 parent
identity；heartbeat 明确是无 cycle/unit 的 diagnostic fact。

证据：

- `station_event_model.md` 第 4、4.2、12.1 节。
- `station_event_model.md:75-119`
- `station_event_model.md:469-486`

`config_hash` 与 Sprint 1 resolved config 的关联也足够严格：

- config/hash 缺失 reject。
- unknown hash 为 `CONFIG_NOT_FOUND`。
- station/PLC/type/profile mismatch 为 reject。
- 不允许套用当前配置或改写 source fact。

证据：

- `station_event_model.md:403-422`
- `line_configuration.md:356-378`

### HOLD DQ1-B1：event-level mapping lineage 不完整

问题描述：

- Sprint 1 允许一个 station 使用 1~4 个 mapping。
- station event 的 `correlation.mapping_id` 仍是 optional。
- 因此 `config_hash + station_id` 只能定位工站快照，不能总是确定本事件由哪个 DB
  mapping 产生。

风险：

- raw drill-down 无法稳定定位 source mapping。
- 同站多 mapping 合并时，无法证明字段来自主事件、扩展 payload 还是诊断 mapping。
- 后续 replay、schema mismatch 和 API event audit 可能给出不完整来源。

最小 Architecture 返修：

1. 对由 configured DB mapping 产生的 production event，将 `mapping_id` 设为 conditional
   required。
2. heartbeat 若不来自 station mapping，应明确其独立 source mapping/sequence 规则。
3. resolved config lookup 必须能按 event 保存并返回当时的 exact mapping snapshot。

是否阻塞 Verification / implementation：

- 阻塞完整 Verification Gate matrix。
- 阻塞 Sprint 2 implementation。

### HOLD DQ1-B2：payload template version 血缘不一致

问题描述：

- `correlation.payload_template` 只有一个 string。
- `line_configuration` 和 `dynamic_station_model` 要求 template ID 与 version 可追溯。
- 合同没有冻结该 string 是 versioned immutable ID，还是仅 template ID。

风险：

- 模板升级后历史 payload 无法唯一解释。
- API/raw replay 可能使用错误 schema 解释旧事件。
- 不同实现可能分别把 `screw_v1`、`screw:1` 或 ID/version 两字段作为 canonical 表达。

最小 Architecture 返修：

- 明确 `payload_template` 是不可变 versioned reference，或拆为
  `payload_template_id + payload_template_version`。
- 同时说明 NOK template/version 是否从 `config_hash` 唯一解析，避免 event/DB 合同漂移。

是否阻塞 Verification / implementation：

- 阻塞 lineage 与 raw replay 的正式 Gate。
- 阻塞 Sprint 2 implementation。

## 6. DQ2 — Result projection consistency

结论：**HOLD / CHANGES REQUIRED**

### 已通过

`station_event_model.md` 已明确：

- `station_result` 是唯一 canonical production result carrier。
- 每个 production result slot 最多一个 accepted canonical result。
- `station_cycle_complete` 不承载 result。
- `station_nok` 仅为 detail companion，不增加 outcome、NOK cycle、FPY 或 OEE Quality。
- duplicate 不重复投影；conflict reject，不进入指标。

证据：

- `station_event_model.md:204-240`
- `station_event_model.md:650-691`
- `station_event_model.md:795-809`

### HOLD DQ2-B1：dynamic DB model 与 canonical projection 未对齐

问题描述：

`dynamic_station_model.md` 仍同时建议：

- `cycle_event` 保存 `result`。
- `quality_event` 也保存 `result`。
- 一个 cycle 多个 NOK code 时可一 code 一行。

但该合同没有将其中一个声明为 authoritative outcome、另一个声明为 detail-only derived
projection。

风险：

- 一个 NOK cycle 可能按 defect code 数量重复产生 result/Quality outcome。
- API、OEE 和 Dashboard 可能分别从 `cycle_event` 或 `quality_event` 统计，产生不同
  NOK unit/cycle count。
- 后续 migration/adapter 在两个合同之间没有唯一实现方式。

最小 Architecture 返修：

1. 在 `dynamic_station_model.md` 明确 `station_event_model.md` 是 result authority。
2. production outcome 每个 `production_result_key` 只投影一次。
3. compatibility `cycle_event.result` 若保留，必须标记为 derived/non-authoritative。
4. 一 code 一行的质量明细只能按 `station_nok_detail_key` 投影，不能每行重复计算 outcome。
5. duplicate/conflict/system-reserved detail 不进入 outcome 或 ordinary defect projection。

是否阻塞 Verification / implementation：

- 阻塞 DB/API/Dashboard projection Gate。
- 阻塞 Sprint 2 implementation。

## 7. DQ3 — Payload/raw consistency

结论：**HOLD / CHANGES REQUIRED**

### 已通过

- normalized payload：JSON object，最大 16 KiB。
- raw payload：JSON object 或 UTF-8 string，最大 64 KiB。
- 已限制 depth、object/tree key、key bytes、array items、string bytes、JSON type、
  NaN/Infinity、循环引用。
- binary、image、base64、无界日志、凭据和未脱敏个人数据不属于 MVP。
- 超限 reject，不截断。
- raw 不参与 business result 决策，也不能替代 normalized payload。
- schema/parse/payload/ACK/config/clock/storage 技术失败不能产生 `30003`、business NOK、
  outcome 或 Skip attribution。

证据：

- `station_event_model.md:424-465`
- `station_event_model.md:299-306`
- `station_event_model.md:598-607`

### HOLD DQ3-B1：raw→normalized 权威链与 mismatch disposition 未冻结

问题描述：

合同只说明 raw 是 evidence、normalized 是受控 payload，但未明确：

- normalized 是否必须由 raw 通过指定 mapping/template/decoder 确定性生成。
- raw 与 normalized 同时存在时哪些字段必须一致。
- 顶层 result/NOK、normalized payload 和 raw decoded value 冲突时谁是 source authority。
- raw-only、normalized-only、两者皆有分别代表什么完整性等级。
- parse/schema/value mismatch 是 reject、conflict 还是其他唯一 disposition。

风险：

- 同一 raw 可能被不同 decoder 产生不同 normalized fact。
- normalized payload 可能绕过 raw 证据成为不可复核事实。
- API/Trace 无法说明“可重放”“仅 normalized”“raw mismatch”等数据质量状态。

最小 Architecture 返修：

1. 冻结权威链：

   ```text
   source raw evidence
   → exact mapping/template/decoder version
   → normalized payload
   → canonical business projection
   ```

2. 定义 raw/normalized comparison scope、数值规范化和 mismatch 唯一 disposition。
3. 增加稳定错误码，例如：
   `RAW_PARSE_ERROR / PAYLOAD_SCHEMA_MISMATCH / RAW_NORMALIZED_MISMATCH`。
4. 说明 raw-only / normalized-only 是否可 accepted，以及其 data completeness 状态。

是否阻塞 Verification / implementation：

- 阻塞 payload/raw consistency Gate。
- 阻塞 Sprint 2 implementation。

### HOLD DQ3-B2：raw UTF-8 text 与禁用内容规则不可执行

问题描述：

顶层 raw UTF-8 string 只受 64 KiB 限制，validator 无法仅凭字符串可靠区分普通文本、
base64 二进制、图片编码或截断日志。

风险：

- “禁止 base64/image/unbounded log”无法形成唯一测试结果。
- raw payload 可能退化为任意数据垃圾桶。

最小 Architecture 返修：

- MVP 最小方案：raw 只接受 JSON object；或
- 保留 UTF-8 text，但必须由 versioned template 声明明确的 content type/grammar，并
  对不透明编码 fail closed。
- 增加 whole-tree node/array-item 总量上限，补足结构遍历资源边界。

是否阻塞 Verification / implementation：

- 阻塞 raw content negative matrix。
- 阻塞 Sprint 2 implementation。

## 8. DQ4 — NOK detail quality

结论：**HOLD / CHANGES REQUIRED**

### 已通过

- parent `station_result(result=nok)` 自身是完整 canonical outcome。
- ordinary detail 使用 primary/secondary slot。
- primary 最多一个，且 code/origin 与 parent 一致。
- secondary 必须在 primary 后，code 不同、origin 一致。
- `30003` 使用独立 system-reserved slot。
- `30003` 只关联 canonical skip result 和 accepted upstream NOK evidence。
- `30003` 不进入 ordinary NOK outcome、Quality、FPY 或 Pareto。
- `validated_nok_detail` 的 `upstream_result` 与其 canonical parent result 比较，detail
  自身仍禁止 result。

证据：

- `station_event_model.md:214-240`
- `station_event_model.md:285-315`
- `station_event_model.md:488-607`
- `station_event_model.md:674-691`

### HOLD DQ4-B1：detail 可选但 Pareto completeness 未定义

问题描述：

- canonical `station_result(result=nok)` 不要求最终出现 `station_nok`。
- ordinary Pareto 又只统计 accepted distinct primary + secondary detail。
- 因此合法 NOK cycle 可以计入 NOK unit/cycle count，但 canonical primary code 完全不进入
  Pareto。

风险：

- Dashboard 可展示看似完整、实际缺失部分 NOK cycles 的 Pareto。
- NOK count 与 Pareto detail 总量的差异没有 coverage/partial 解释。
- API 无法区分“没有 secondary defect”和“整个 detail companion 缺失”。

最小 Architecture 返修：

保留 detail optional，不扩大 MVP，但冻结完整性指标：

```text
nok_cycle_count
nok_cycles_with_primary_detail
missing_primary_detail_cycle_count
detail_coverage
pareto_status = complete | partial
```

没有 accepted primary detail 时 Pareto 必须标记 `partial`；不得静默从 parent 合成
`station_nok` detail，也不得显示为完整 Pareto。

是否阻塞 Verification / implementation：

- 阻塞 Quality/Pareto completeness Gate。
- 阻塞 Sprint 2 implementation。

## 9. DQ5 — Identity and idempotency data quality

结论：**HOLD / CHANGES REQUIRED**

### 已通过

- `event_id`、`source_event_id`、`fact_key` 职责分离。
- UUIDv4 只表示 envelope identity，retry/replay 必须复用。
- `cycle_role_key` 独立于 source/config/unit identity，防止改变 config/source ID 绕过去重。
- NOK detail、primary 和 system-reserved 有独立 business key。
- absent optional field 与 explicit null 已严格分离。
- `profile_id` 和 `config_hash` 参与内容一致性；同 physical slot 改变它们会 conflict。
- fact-key 与 content-fingerprint 已有官方向量。

证据：

- `station_event_model.md:627-735`
- `station_event_model.md:737-809`

### HOLD DQ5-B1：JSON 数值 canonicalization 不足以跨实现稳定复现

问题描述：

payload 允许 finite JSON number，fingerprint 包含完整 normalized payload；但合同没有冻结：

- integer 与 float 的等价/不等价规则。
- `0 / 0.0 / -0.0`。
- exponent 与 decimal rendering。
- 跨 Python/JavaScript/PostgreSQL 的数值 canonical bytes。

风险：

- 同一测量事实可能因 serializer/runtime 不同被判 conflict。
- 不同语言实现可能对同 payload 产生不同 fingerprint。

最小 Architecture 返修：

- 采用 RFC 8785/JCS，或冻结等价的精确 JSON number canonicalization。
- 增加 `-0`、整数/小数、指数、边界数值 official vectors。

是否阻塞 Verification / implementation：

- 阻塞 fingerprint cross-runtime Gate。
- 阻塞 Sprint 2 implementation。

### HOLD DQ5-B2：raw evidence 变化不会进入 duplicate/conflict 审计

问题描述：

`raw_payload` 是审计/重放证据，却被明确从 `content_fingerprint` 排除。同一业务槽位若
normalized 内容相同但 raw 不同，会被判为普通 duplicate。

风险：

- decoder 漂移、source raw 变化或证据篡改不可见。
- 首次 accepted raw 与 retry raw 的差异没有可审计 disposition。

最小 Architecture 返修：

- 增加独立 `raw_evidence_fingerprint`。
- raw 不同不应创建第二个 production fact，但必须产生 audit-only
  `raw_variant/raw_evidence_conflict` 结果。

是否阻塞 Verification / implementation：

- 阻塞 raw evidence audit Gate。
- 阻塞 Sprint 2 implementation。

### HOLD DQ5-B3：多 key 同时碰撞时优先级未冻结

问题描述：

一个 incoming event 可能同时命中：

- event ID conflict。
- fact key conflict。
- cycle/detail slot conflict。

合同定义了各自错误，但未定义同时发生时的最终 disposition/error precedence 和 audit
返回内容。

风险：

- 不同 validator 对同一输入返回不同错误。
- Verification snapshot、API audit 和未来 quarantine reason 不稳定。

最小 Architecture 返修：

- 增加 precedence table，例如：
  `event_id → fact_key → cycle/detail slot`。
- decision 返回 matched key type、existing event ID、existing/incoming fingerprints 和
  final error code。

是否阻塞 Verification / implementation：

- 阻塞完整 duplicate/conflict matrix。
- 阻塞 Sprint 2 implementation。

## 10. DQ6 — Temporal and lifecycle coherence

结论：**HOLD / CHANGES REQUIRED**

### 已通过

- `event_ts / observed_at / created_at` 职责分离。
- source timestamp 不因迟到或异常而改写。
- future skew 有 5 分钟边界。
- out-of-order 允许保留并以 cycle counter 优先排序。
- NOK parent missing/not-found/unavailable/mismatch 都有唯一 reject。
- MVP 不接受 orphan detail，也没有含糊 pending/defer。
- heartbeat 是 diagnostic-only，UNKNOWN 不会污染 production trace。

证据：

- `station_event_model.md:609-625`
- `station_event_model.md:838-913`

### HOLD DQ6-B1：late event 没有可执行定义

问题描述：

planning 要求分类 `missing / late / out-of-order`，但合同只定义 future skew 和
out-of-order preservation，没有定义：

- late 的参考时钟或窗口。
- threshold。
- disposition。
- 是否仍可占据 production slot。
- API/Dashboard 的 late/complete 状态。

风险：

- 同一 delayed event 在不同实现中可能被 accepted、rejected 或仅标记。
- 数据完整性与实时 KPI 可能在晚到后无一致修订规则。

最小 Architecture 返修：

- 冻结 MVP late 定义。若 Sprint 2 不希望引入 runtime threshold，应明确：
  “offline model 不判 late；late 属 future runtime metadata，MVP 只保留 out-of-order”。
- 不得在 planning 中继续把 late 作为本 Sprint 可验证分类却不给规则。

是否阻塞 Verification / implementation：

- 阻塞 time classification Gate。
- 阻塞 Sprint 2 implementation。

### HOLD DQ6-B2：cycle lifecycle matrix 不完整

问题描述：

合同只写 role logical order：

```text
start → complete → production_result → nok_detail relation
```

但 stateful validation 未定义：

- result 是否可在 start/complete 不存在时 accepted。
- complete without start 是有效部分事实还是 orphan。
- result 先到后，start/complete 晚到时如何处理。
- 同 counter 内 timestamp reversal 是 reject、diagnostic 还是 accepted。
- missing role 是否影响 cycle completeness 或 production projection。

风险：

- “out-of-order 可接受”与“逻辑顺序检查”可产生多个实现解释。
- Trace timeline 和完整性指标无法区分 complete、partial、orphan、late-filled cycle。

最小 Architecture 返修：

- 增加 compact lifecycle/disposition matrix，冻结 predecessor 缺失、乱序到达、后补、
  timestamp reversal、projection eligibility 和 error/status。
- 不需要实现 storage 或 Collector，只需冻结合同语义。

是否阻塞 Verification / implementation：

- 阻塞 lifecycle Gate。
- 阻塞 Sprint 2 implementation。

## 11. DQ7 — Future API / Dashboard implications

结论：**HOLD / CHANGES REQUIRED**

### 已具备的稳定基础

基于当前合同，后续可以稳定实现：

- 按 line/PLC/station/boot/counter 查询 event audit。
- 按 accepted `station_result` 计算 OK/NOK/skip outcome。
- 按 accepted ordinary `station_nok` 计算 distinct defect detail。
- 排除 duplicate、conflict、heartbeat 和 `30003`。
- 按 config/profile 过滤。
- 对 raw/normalized payload 做有界展示。

### 仍阻塞兼容 API/Dashboard 的问题

1. dynamic DB contract 没有冻结 authoritative vs derived result projection。
2. Pareto 缺少 detail coverage/partial 状态。
3. mapping/template version 不足以支撑稳定 raw drill-down。
4. raw/normalized mismatch 与 raw variant 没有 audit status。
5. cycle partial/orphan/late 状态没有合同。
6. production event 可合法缺少 unit/DMC；未来 Trace 必须明确返回 cycle-only
   traceability，而不能把它展示成完整 unit genealogy。

最小 Architecture 返修：

- 只在现有合同中增加 projection authority、completeness metadata、lineage 和 lifecycle
  semantics；不新增 API endpoint、Dashboard、DB migration 或 runtime adapter。
- 对 unit/DMC 都 absent 的 accepted event，冻结 derived traceability level，例如
  `cycle_only`；不要为此新增业务控制流程。

是否阻塞 Verification / implementation：

- 可以让 Verification 先建立不受争议的基础 matrix。
- 不能冻结完整 Data Quality Gate matrix。
- 不建议进入 Sprint 2 implementation。

## 12. HOLD 项最小 Architecture 返修清单

建议合并为五个最小合同修订包，避免扩大 Sprint 2 MVP：

### R1. Lineage

- production event mapping ID conditional required。
- payload template ID/version 语义唯一。
- exact mapping/template/NOK-template snapshot 可按 `config_hash` 解析。

### R2. Projection 与 completeness

- dynamic DB model 对齐唯一 canonical `station_result`。
- defect row detail-only。
- Pareto detail coverage 与 `complete/partial` 状态。

### R3. Payload/raw consistency

- raw→mapping/template/decoder→normalized 权威链。
- raw/normalized mismatch 唯一 disposition/error。
- raw text content type/grammar 或 MVP 收窄为 JSON object。
- 独立 raw evidence fingerprint/audit variant。

### R4. Deterministic identity

- JSON number canonicalization。
- event/fact/cycle/detail 多 key collision precedence 与审计字段。

### R5. Temporal/lifecycle

- late 是 MVP rule 还是明确 future-only。
- start/complete/result/detail lifecycle/disposition matrix。
- cycle-only traceability 与 partial/orphan 状态。

上述修改都可以保持 docs-only，不需要创建 package、tests、DB/API/Collector/V-PLC/
Dashboard adapter，也不需要 deploy。

## 13. Non-blocking recommendations

1. 将 canonical positive fixtures 与真实 Sprint 1 resolved config 对齐。
2. 为 Unicode、数字边界、secondary/system-reserved detail 增加 official fingerprint
   vectors。
3. future stateful validator 使用同一 accepted-record snapshot，避免 lookup race。
4. 为 rejected decision 保留 stable error path、matched key 和 source evidence 摘要。
5. 将 `dynamic_station_model.md` 中旧式
   `(line, plc, station, boot, counter)` identity 明确升级为按 event role/detail slot 投影，
   但不要在本轮设计 DB unique constraint。
6. Architecture handoff/context 的 HEAD 文字在后续 docs hygiene 时更新为 `60adac2`。
7. heartbeat 频率、保留、降采样继续放在 future runtime/DB contract，不扩大 Sprint 2。

## 14. 总结论与 Gate 建议

最终结论：

```text
HOLD / CHANGES REQUIRED
```

理由：

- canonical result、NOK relation、authority、reserved code、presence/null、config mismatch
  和 basic business uniqueness 已具备良好基础。
- 但五组 Data Quality 语义尚未唯一冻结：lineage、projection completeness、
  raw/normalized consistency、cross-runtime fingerprint、temporal lifecycle。
- 若直接实现，不同实现者仍可能产生不同 accepted facts、不同 duplicate/conflict、
  不完整但未标记的 Pareto，以及不可复核的 raw drill-down。

明确建议：

| 决策 | 建议 |
| --- | --- |
| 是否可以进入 Verification Gate matrix | **可以准备基础 matrix；完整正式 Gate matrix 暂缓冻结** |
| 是否可以进入 Sprint 2 implementation | **否** |
| 是否需要回 Architecture | **是，仅执行第 12 节五个最小 docs-only 返修包** |
| 是否扩大 Sprint 2 MVP | **否** |
| 是否修改 Reliability 结论 | **否，保持 PASS WITH RECOMMENDATIONS** |

Architecture 完成最小返修后，应先做一次 Data Quality focused re-review，再由
Verification 冻结最终 Gate matrix，最后交 ChatGPT PM 决定是否授权 implementation。

## 15. 本轮文件与操作范围

本轮新增：

- `docs/reports/sprint2_station_event_data_quality_review.md`

本轮未修改：

- `docs/contracts/`
- `docs/reports/sprint2_generic_station_event_model_plan.md`
- `docs/reports/sprint2_station_event_reliability_review.md`
- `docs/thread_handoff/`
- code / tests / runtime

本轮未执行：

- 创建 `common/station_event/`
- implementation
- commit / push / tag
- deploy / rollback drill
- `git add .`

---

## 16. Data Quality focused re-review（2026-06-21）

> 本节追加记录 Architecture 完成 R1~R5 docs-only 返修后的 focused re-review。
> 第 1~15 节的 `HOLD / CHANGES REQUIRED` 保留为上一轮历史审计记录；当前 Data
> Quality 控制结论以本节至第 24 节为准。

### 16.1 本轮复验范围

本轮只复验上一轮第 12 节 R1~R5 是否关闭，以及返修是否引入新的 Data Quality
blocker。不重新扩大审查范围，不重开 Reliability N5~N8，不进入 implementation。

本轮未审查或实施：

- `common/station_event/` package、tests 或 fixtures。
- Collector、API、DB、Dashboard、V-PLC 或运行链路接入。
- migration、deploy、rollback drill、性能或现场容量验收。
- Architecture 合同、planning、handoff 的进一步修改。

### 16.2 读取文件列表

本轮读取当前 working tree 中的：

1. `docs/reports/sprint2_station_event_data_quality_review.md`
2. `docs/contracts/station_event_model.md`
3. `docs/contracts/dynamic_station_model.md`
4. `docs/reports/sprint2_generic_station_event_model_plan.md`
5. `docs/thread_handoff/architecture.md`
6. `docs/reports/architecture_context_restore.md`
7. `docs/contracts/line_configuration.md`
8. `docs/reports/sprint2_station_event_reliability_review.md`
9. `docs/DOC_INDEX.md`
10. `docs/reports/README.md`

重点复验了上一轮第 5~12 节、`station_event_model.md` 第 10、11、12、18 节、
`dynamic_station_model.md` 第 4 节，以及 planning、handoff/context 中最新 R1~R5
返修状态。

## 17. 当前基线与 working tree 确认

```text
HEAD        60adac2629d499ca5ee923786289c5ccd6d4b6aa
origin/main 60adac2629d499ca5ee923786289c5ccd6d4b6aa
latest      60adac2 Address Sprint 2 station event reliability review
tag         phase1-pass-20260619
common/station_event absent
code/tests/runtime diff: none
```

最近三个 commit：

```text
60adac2 Address Sprint 2 station event reliability review
45fa2a8 Freeze Sprint 2 station event planning
4215b7c Finalize Sprint 1 architecture handoff and review history
```

focused re-review 开始时，Architecture 的 7 个 docs-only 修改仍在 working tree；
Data Quality report 与用户明确禁止处理的三个路径为未跟踪项。本轮未处理这些禁止项。

`git diff --check`：**PASS**。

## 18. R1 — Lineage focused check

结论：**CLOSED**

关闭证据：

1. configured DB mapping 产生的 production event 已要求
   `correlation.mapping_id` conditional required；多 mapping station 不得只靠
   `station_id` 推断。
2. heartbeat 不来自 station mapping 时，必须引用 resolved config 中独立、不可变的
   diagnostic source mapping，并声明 boot-scoped sequence namespace 与 source
   authority；`source_event_id` 不得使用接收时间或随机数生成。
3. `correlation.payload_template` 已冻结为 immutable versioned reference，必须匹配同一
   `config_hash` snapshot 中唯一的 `template_id + version` reference。
4. NOK template 不在 event 中重复复制；exact `template_id + version` 必须由
   `config_hash + station_id` 唯一解析，存在多义或不匹配时 reject。
5. `lookup_resolved_config(config_hash)` 必须返回 immutable historical snapshot，并可按
   event 返回 exact mapping、payload template、decoder、NOK template、profile 与 route。
6. 合同明确禁止 fallback 到 current/latest config；历史 snapshot 不存在时
   `CONFIG_NOT_FOUND`，lineage 无法唯一解析时 `EVENT_LINEAGE_INVALID`。

R1 remaining OPEN item：**无**。

## 19. R2 — Projection / completeness focused check

结论：**CLOSED**

关闭证据：

1. `station_event_model.md` 已明确 `station_result` 是唯一 production result authority。
2. 每个 `production_result_key` 最多投影一次 accepted canonical outcome。
3. `dynamic_station_model.md` 已将 `cycle_event.result` 限定为 derived、
   non-authoritative compatibility projection，不得接收独立 result authority。
4. `quality_event` 已冻结为 detail-only projection；一 detail 一行时不得重复 `result`
   或增加 NOK cycle/outcome count。
5. duplicate、conflict 与 `system_reserved/30003` detail 均排除在 ordinary outcome、
   ordinary defect 与 Pareto 投影之外。
6. Pareto completeness 已冻结：

   ```text
   nok_cycle_count
   nok_cycles_with_primary_detail
   missing_primary_detail_cycle_count
   detail_coverage
   pareto_status = complete | partial
   ```

7. accepted NOK result 没有 accepted primary detail 时必须返回 `partial`；不得从 parent
   `nok_code` 静默合成 detail，也不得展示为完整 Pareto。

R2 remaining OPEN item：**无**。

## 20. R3 — Payload/raw consistency focused check

结论：**CLOSED**

关闭证据：

1. 唯一权威链已冻结：

   ```text
   source raw evidence
   → exact mapping/template/decoder version
   → normalized payload
   → canonical business projection
   ```

2. comparison scope 固定为 versioned template 声明的 decoded fields；字段名、类型、
   单位换算、missing/absent 与 JSON number bytes 使用同一模板/JCS 规则规范化。
3. raw 与 normalized 同时存在时，raw 经 exact decoder 得到的 declared fields 是
   comparison authority；normalized 必须逐字段匹配。raw 不替代顶层 canonical fields。
4. `raw_and_normalized`、`normalized_only`、`raw_only`、`evidence_mismatch` 四类
   `data_completeness` 状态及 accept/reject 规则已明确。
5. mismatch 唯一错误已冻结：
   `RAW_PARSE_ERROR / PAYLOAD_SCHEMA_MISMATCH / RAW_NORMALIZED_MISMATCH`。
6. raw 不参与 business result 决策，也不能替代 normalized payload/canonical fields。
7. parse/schema/value mismatch 不得产生 production outcome、ordinary NOK、`30003`、
   `UPSTREAM_NOK_SKIPPED` 或 Pareto entry。
8. MVP raw 已收敛为 JSON object only；顶层 UTF-8 text、bytes、binary、base64、image
   与 opaque/unbounded log 均不接受。
9. 已冻结 whole-tree key、array item 与总 node 上限，包括全树最多 256 array items、
   512 nodes。
10. 已新增独立 `raw_evidence_fingerprint = SHA-256(JCS(raw_payload))`。
11. 相同 production slot/content 但 raw fingerprint 不同时不创建第二个 production
    fact，只形成 audit-only `raw_variant`；raw/normalized 不一致为
    `raw_evidence_conflict / RAW_NORMALIZED_MISMATCH` 且不得 accepted。

R3 remaining OPEN item：**无**。

## 21. R4 — Deterministic identity focused check

结论：**CLOSED WITH RECOMMENDATIONS**

关闭证据：

1. `content_fingerprint`、`raw_evidence_fingerprint` 与 payload comparison 均冻结为
   RFC 8785 JSON Canonicalization Scheme（JCS）等价 UTF-8 bytes。
2. JSON number 限定为 finite IEEE 754 binary64；NaN/Infinity reject。
3. integer 安全范围、decimal/exponent shortest round-trip、`0/0.0/-0.0` 与
   `1/1.0` canonical equivalence 已明确。
4. Verification planned official vectors 已明确包含 `-0/-0.0`、`1/1.0`、`1e30`、
   `0.000001` 与 maximum finite binary64。
5. 多 key collision precedence 已冻结为：

   ```text
   event_id
   → fact_key
   → cycle_role_key / production_result_key
   → primary/system-reserved/station_nok_detail_key
   ```

6. audit decision 已包含 matched key type/value、existing event ID、existing/incoming
   content fingerprint、existing/incoming raw evidence fingerprint、final disposition
   与 final error code。

Non-blocking recommendation：

- Verification 将第 18.4 节 planned number vectors 落成跨 Python/JavaScript/PostgreSQL
  的 exact canonical bytes + SHA-256 fixtures，并补充 JCS 边界/rounding 负例。

该建议不要求 Architecture 再返修，不阻塞 R4 关闭。

## 22. R5 — Temporal/lifecycle focused check

结论：**CLOSED**

关闭证据：

1. Sprint 2 offline model 已明确不判定 `late`；threshold、watermark 与 arrived-late
   metadata 属 future runtime contract。
2. planning 与 Verification 已明确不得把 late 当作本 Sprint 可判定分类；MVP 只保留
   source timestamp、arrival-independent out-of-order preservation 与 timestamp
   reversal diagnostic。
3. lifecycle/disposition matrix 已覆盖：
   start missing、complete missing、result without start、result without complete、
   complete without start、result before start/complete arrival、start/complete late
   fill、timestamp reversal、NOK detail parent missing/OK、duplicate detail 与 conflict
   detail。
4. 每种情况均冻结 disposition、projection eligibility、`cycle_completeness` 与
   traceability。
5. missing start/complete 不阻止独立合法 canonical result 占据
   `production_result_key`；后到 role 只补 completeness，不改写 result。
6. unit/DMC 都 absent 的 accepted event 固定为
   `traceability_level=cycle_only`；Trace/API 只能展示 boot/counter/cycle lineage，
   不得宣称完整 unit genealogy。
7. NOK orphan relation 在 MVP fail closed：parent missing reject；parent OK reject。

R5 remaining OPEN item：**无**。

## 23. 新 Data Quality blocker 与总判断

本轮未发现新的 Data Quality blocker。

| 返修项 | focused re-review 结论 |
| --- | --- |
| R1 Lineage | **CLOSED** |
| R2 Projection / completeness | **CLOSED** |
| R3 Payload/raw consistency | **CLOSED** |
| R4 Deterministic identity | **CLOSED WITH RECOMMENDATIONS** |
| R5 Temporal/lifecycle | **CLOSED** |

remaining HOLD blocker：**无**。

本轮总控制结论：

```text
PASS WITH RECOMMENDATIONS
```

该结论不改变 Reliability 的 `PASS WITH RECOMMENDATIONS`，也不代表 Sprint 2
implementation 已获 ChatGPT PM 授权。

## 24. Gate 建议与本轮操作边界

| 决策 | focused re-review 建议 |
| --- | --- |
| 是否可以进入 Verification Gate matrix | **是，可以基于当前最终合同冻结完整 Gate matrix** |
| 是否可以进入 Sprint 2 implementation | **暂不可以；必须先完成 Verification Gate，并由 ChatGPT PM 明确授权** |
| 是否需要回 Architecture 做最小返修 | **否** |
| 是否扩大 Sprint 2 MVP | **否** |

本轮只更新：

- `docs/reports/sprint2_station_event_data_quality_review.md`

本轮未修改：

- Architecture contracts / planning / handoff。
- `docs/reports/sprint2_station_event_reliability_review.md`。
- code / tests / runtime。
- Collector / API / DB / Dashboard / V-PLC。

本轮未执行：

- 创建 `common/station_event/`。
- implementation。
- commit / push / tag / deploy。
- rollback drill。
- `git add .`。
*** End of File

---

## 38. Current implementation review status

本节位于文件末尾，是当前最终控制结论；详细 findings 与证据见第 32～36 节。

```text
HOLD
DQ-B1: STILL OPEN
DQ-B4: STILL OPEN
DQ-B5: STILL OPEN
R3: STILL OPEN
R5: CLOSED
```

在 DQ-F1～DQ-F3 完成最小 repair 与 targeted re-review 前，不具备 implementation
commit/push 条件。

---

## 37. 当前 Data Quality implementation 控制结论

本节是本报告当前最终控制结论，覆盖第 31 节 implementation 前
`PASS WITH RECOMMENDATIONS` 状态。详细 implementation findings 与证据见第 32～36 节。

```text
HOLD
DQ-B1 historical config snapshot lineage: STILL OPEN
DQ-B4 validated NOK detail traceability: STILL OPEN
DQ-B5 raw evidence authority: STILL OPEN
R3 raw evidence / fingerprint / projection authority: STILL OPEN
R5 temporal/lifecycle traceability consistency: CLOSED
```

Remaining blockers：

1. parent relation 未完整绑定 historical snapshot 的 `profile_id/station_type`。
2. accepted compatibility/non-`nok_detail` cited detail 可支持
   `validated_nok_detail` evidence。
3. historical snapshot 缺 exact decoder 时，raw-only 或 raw/normalized mismatch 可
   fail-open，并产生 authoritative production outcome。

上述三项完成最小 implementation repair、focused tests 与 targeted sanity re-review
前，不具备 implementation commit/push 条件。本 Thread 未授权或执行 implementation、
commit、push、tag、deploy、rollback drill 或 integration。

---

## 32. Sprint 2 Data Quality Focused Implementation Review（2026-06-23）

本节是 Generic Station Event Model implementation 的独立、read-only focused review。
只复验 DQ-B1、DQ-B4、DQ-B5、R3 与 R5；不重开完整 Data Quality review，不修改
implementation、tests 或合同。

### 32.1 当前基线与范围

```text
HEAD: e9abe45 Finalize Sprint 2 station event review gates
tag: phase1-pass-20260619
implementation: uncommitted working tree
common/station_event/: present
Collector/API/DB/Dashboard/V-PLC integration: none
migration: none
commit/push/tag/deploy/rollback drill: not performed by this review
```

本轮读取：

- `common/station_event/validation.py`
- `common/station_event/projection.py`
- `common/station_event/fingerprint.py`
- `common/station_event/lifecycle.py`
- `common/station_event/serialization.py`
- `common/station_event/models.py`
- `tests/test_station_event_model.py`
- 本 Data Quality report
- Sprint 2 Reliability review
- Sprint 2 Verification matrix
- Sprint 2 implementation report
- Architecture handoff/context restore

## 33. Focused status

### 33.1 DQ-B1 historical config snapshot lineage

结论：**STILL OPEN**

已通过：

- stateful validation 必须 lookup event 自身 `config_hash` 对应的 historical snapshot。
- event 自身会重新校验 line、station、PLC、station type、profile 与 config hash。
- cross-config、cross-station、cross-cycle parent 已有 fail-closed tests。

remaining blocker：

- `_parent_matches()` 的 relation fields 包含 line/PLC/station/boot/cycle/counter/
  unit/DMC/config，但未包含 `profile_id` 与 `station_type`。
- 独立探针将 accepted parent 的 `profile_id` 改为
  `wrong_historical_profile`，或将 `station_type` 改为 `vision`，stateful decision
  仍为 `accept`。
- 因此 parent relation 没有完整重放 historical snapshot lineage；parent 可在 event
  本身通过 snapshot validation 后，以错误 profile/station type 支持 relation。

最小 repair：

- shared canonical parent matcher 增加 parent/detail `profile_id` 与 `station_type`
  一致性。
- 或在使用 parent 前，对 parent 使用相同 historical snapshot 执行完整 config lineage
  validation；任一 mismatch fail closed。

### 33.2 DQ-B4 validated NOK detail traceability

结论：**STILL OPEN**

已通过：

- canonical parent 必须 lookup accepted。
- canonical parent 必须为 authoritative PLC/V-PLC
  `station_result(result=nok)`。
- canonical parent 必须 `correlation.event_role=production_result`。
- line/station/cycle/config、primary code/origin、secondary origin relation 已覆盖。
- duplicate/conflict/rejected canonical parent 与错误 parent role 已 fail closed。
- rejected decision 不进入 production outcome 或 defect projection。

remaining blocker：

- cited detail record 只检查 lookup accepted、`event_type=station_nok`、自身不携带
  `result`，随后直接进入 parent relation；没有重新要求
  `correlation.event_role=nok_detail`，也没有对 cited detail 重放完整 stateless/
  historical validation。
- 独立探针把 cited detail 的 `event_role` 改为 `compatibility`，同时由 state index
  返回 `disposition=accept`，最终 `validated_nok_detail` evidence 仍被 accepted。
- 因此 non-authoritative/compatibility cited detail 仍可形成 validated traceability。

最小 repair：

- evidence path 必须要求 cited detail `correlation.event_role=nok_detail`。
- cited detail 必须是通过同 historical snapshot 与 ordinary detail relation validation
  的 accepted canonical detail；不能只信任 lookup wrapper 的 accepted 标记。

### 33.3 DQ-B5 raw evidence authority

结论：**STILL OPEN**

已通过：

- binary/image/PDF/WebP/generic base64、binary MIME/key hint 与 repeated-log content
  已 fail closed。
- raw fingerprint 独立于 content fingerprint。
- raw variant 是 audit subtype，不改变 canonical identity。

remaining blocker：

- raw/normalized authority comparison 只在 historical snapshot 提供 callable
  `decode_raw_payload` 时执行。
- snapshot 没有 decoder 时，raw-only event 与 raw/normalized 明显不一致 event 均可
  accepted。
- 这违反 raw evidence 不得替代 normalized payload，以及 exact decoder 缺失时必须
  fail closed 的要求。

独立探针：

```text
RAW_ONLY accept None projection_eligible=true production_outcome=ok
RAW_NORMALIZED_NO_DECODER accept None projection_eligible=true production_outcome=ok
```

最小 repair：

- `raw_payload` 存在时 historical snapshot 必须提供 exact decoder；缺失时 reject
  `EVENT_LINEAGE_INVALID`、`RAW_PARSE_ERROR` 或合同选定的唯一稳定错误码。
- raw-only 永远不得形成 canonical business event。
- raw + normalized 必须经 exact decoder 比较；无法比较必须 fail closed。

### 33.4 R3 raw evidence / fingerprint / projection authority

结论：**STILL OPEN**

已通过：

```text
same canonical content + same raw fingerprint
→ duplicate

same canonical content + different raw fingerprint
→ duplicate + audit_subtype=raw_variant

different canonical content
→ conflict
```

- duplicate/raw_variant 不产生第二个 production result。
- conflict 不投影 production outcome。

remaining blocker：

- 在进入 duplicate/conflict/raw_variant 裁决前，raw-only 或无法使用 exact decoder
  对照的 raw/normalized event 可先被 accepted，并由 `projection_for()` 产生 authoritative
  production outcome。
- 因此 fingerprint decision 本身正确，但完整 R3 authority chain 仍可绕过。

### 33.5 R5 temporal/lifecycle traceability consistency

结论：**CLOSED**

- `LifecycleDerivedOutput` 八字段完整。
- `station_cycle_complete` stateless 禁止携带 result，projection 也不产生 outcome。
- `station_result` 是唯一 authoritative production result。
- heartbeat 固定 diagnostic-only。
- start/complete 双缺失唯一状态为
  `partial_cycle_missing_start_and_complete`。
- result-only + unit/DMC absent 固定 `cycle_only`。
- reject/duplicate/conflict 的 lifecycle output 与 projection eligibility 不矛盾。
- timestamp reversal 只形成 diagnostic timeline status，不改写 source timestamp 或
  canonical result。

## 34. Findings

### DQ-F1 — historical parent snapshot lineage 不完整

严重性：**blocker**

parent `profile_id` / `station_type` mismatch 可通过 shared parent matcher，未满足
historical snapshot full-lineage requirement。

### DQ-F2 — compatibility cited detail 可形成 validated NOK detail evidence

严重性：**blocker**

cited detail 的 `correlation.event_role` 未强制为 `nok_detail`，也未重放完整 accepted
detail validation。

### DQ-F3 — decoder 缺失时 raw authority fail-open

严重性：**blocker**

raw-only 与 raw/normalized mismatch 在 snapshot 无 decoder 时均 accepted，并可产生
authoritative production outcome。

## 35. Test evidence

执行：

```text
git status --short
git diff -- common/station_event tests/test_station_event_model.py
.venv/bin/python -m compileall common tests
.venv/bin/python -m pytest tests/test_station_event_model.py -q
.venv/bin/python -m pytest tests -q
git diff --check
```

结果：

```text
compileall: PASS
focused station_event: 119 passed
broader tests: 207 passed
git diff --check: PASS
unrelated failures: none
```

说明：`common/station_event/` 与 `tests/test_station_event_model.py` 当前为 untracked，
因此 `git diff -- common/station_event tests/test_station_event_model.py` 无输出；实际内容
已逐文件读取并通过上述测试执行。

## 36. Focused implementation review decision

结论：

```text
HOLD
```

| 项目 | 状态 |
| --- | --- |
| DQ-B1 historical config snapshot lineage | **STILL OPEN** |
| DQ-B4 validated NOK detail traceability | **STILL OPEN** |
| DQ-B5 raw evidence authority | **STILL OPEN** |
| R3 raw evidence / fingerprint / projection authority | **STILL OPEN** |
| R5 temporal/lifecycle traceability consistency | **CLOSED** |

决策：

- Remaining Data Quality blocker：**yes，DQ-F1/DQ-F2/DQ-F3**。
- Need Architecture repair：**yes，最小 implementation repair；不改合同语义**。
- Need Reliability re-review：**no**。本轮 findings 是 historical lineage、cited-detail
  authority 与 raw authority 的 Data Quality focused gap。
- Need Verification re-review：**yes，repair 后只做 DQ-F1～F3 targeted sanity check**。
- Eligible for implementation commit/push：**no**。

本 review 只修改本 Data Quality report；未修改 implementation、tests、contracts、
Collector/API/DB/Dashboard/V-PLC，未创建 migration，未 commit/push/tag/deploy 或执行
rollback drill。

---

## 25. Data Quality V10/R5 focused sanity check（2026-06-21）

> 本节只确认 Architecture 最新 V10 lifecycle 修订是否继续满足 Data Quality R5 /
> DQ6。第 1～15 节 HOLD 与第 16～24 节 focused re-review 记录均保留；本轮不重开
> R1～R4，也不重新执行完整 Data Quality review。

### 25.1 本轮确认范围

本轮只检查：

1. late 是否继续保持 future-only 且与 out-of-order preservation 不冲突。
2. lifecycle evaluation order 与 final classification 是否互斥、唯一。
3. accepted result 的 start/complete 双缺失状态是否唯一。
4. `LifecycleDerivedOutput` 八字段是否足以支撑 Data Quality、Trace 与 future API。
5. V10 修订是否引入新的 Data Quality blocker。

本轮不检查或实施 V6/V7、R1～R4、package、tests、runtime adapter、DB migration、
API、Dashboard、Collector 或 V-PLC。

### 25.2 读取文件

本轮读取当前 working tree：

1. `docs/reports/sprint2_station_event_data_quality_review.md`
2. `docs/reports/sprint2_station_event_verification_matrix.md`
3. `docs/contracts/station_event_model.md`
4. `docs/contracts/dynamic_station_model.md`
5. `docs/reports/sprint2_generic_station_event_model_plan.md`
6. `docs/thread_handoff/architecture.md`
7. `docs/reports/architecture_context_restore.md`
8. `docs/DOC_INDEX.md`
9. `docs/reports/README.md`

重点复验原 DQ6/R5 HOLD、第 16～24 节 Data Quality focused re-review、Verification
第 24～31 节，以及 `station_event_model.md` 第 18.5 节。

## 26. 当前基线与隔离确认

```text
HEAD        60adac2629d499ca5ee923786289c5ccd6d4b6aa
origin/main 60adac2629d499ca5ee923786289c5ccd6d4b6aa
latest      60adac2 Address Sprint 2 station event reliability review
tag         phase1-pass-20260619
common/station_event absent
code/tests/runtime diff: none
```

- Sprint 2 implementation 尚未开始。
- Architecture、Data Quality 与 Verification 当前变更均为 docs-only working tree。
- 本轮只更新本 Data Quality report。
- 未执行 commit、push、tag、deploy 或 rollback drill。
- `git diff --check`：**PASS**。

## 27. late 语义

结论：**CLOSED**

确认结果：

1. Sprint 2 offline model 明确不判定 late。
2. late threshold、watermark 与 arrived-late metadata 明确属于 future runtime
   contract。
3. `LifecycleDerivedOutput.late_status` 在 MVP 固定为
   `not_evaluated_future_runtime`。
4. planning/contract 不再把 late 当作本 Sprint 可判定分类。
5. out-of-order 与 late 已分离：arrival/source facts 保留，source timestamp 不改写；
   arrival order 与 logical role order 不同使用
   `timeline_status=out_of_order_preserved`。
6. timestamp reversal 只形成 derived diagnostic，不重排或改写 source fact。

late remaining OPEN item：**无**。

## 28. lifecycle matrix 互斥性

结论：**CLOSED**

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

确认结果：

1. 较早步骤产生的 reject、duplicate 或 conflict 不会被后续 lifecycle derivation
   改写。
2. incoming event final classification 已按 validation reject、duplicate、conflict、
   heartbeat、NOK relation、accepted production event 分支，单个 event 只有一个最终
   分类。
3. production role-presence 表对 start/complete 的四种组合互斥且穷尽。
4. result without start、without complete、without both 均由同一 role-presence 表生成
   唯一 completeness。
5. detail parent missing、parent OK、attached、duplicate 与 conflict 均有唯一
   disposition、lifecycle state 与 relation status。
6. MVP 没有引入 pending、defer 或 quarantine；这些仍为 future async runtime 范围。

lifecycle mutual-exclusivity remaining OPEN item：**无**。

## 29. start/complete 双缺失状态

结论：**CLOSED**

accepted `station_result` 且 accepted start/complete 都不存在时，唯一输出为：

```text
disposition=accept
lifecycle_state=partial_cycle_missing_start_and_complete
cycle_completeness=partial_cycle_missing_start_and_complete
timeline_status=result_only
projection_eligible=true
traceability_status=unit_traceable when unit_id or dmc exists, otherwise cycle_only
```

Data Quality 判断：

- 双缺失不会产生 `partial_missing_start` 与 `partial_missing_complete` 两个竞争状态。
- canonical result 仍可占据唯一 `production_result_key`，不会因 predecessor 缺失而丢失
  或重复投影。
- 后补 start/complete 只重算 derived completeness/timeline，不改写或重复 canonical
  result。
- unit/DMC 都 absent 时固定 `cycle_only`，只能展示 boot/counter/cycle lineage，不会
  污染或伪造 unit genealogy。

双缺失状态 remaining OPEN item：**无**。

## 30. `LifecycleDerivedOutput` 八字段

结论：**CLOSED WITH RECOMMENDATIONS**

八字段接口已冻结为：

1. `lifecycle_state`
2. `cycle_completeness`
3. `traceability_status`
4. `timeline_status`
5. `projection_eligible`
6. `parent_relation_status`
7. `detail_relation_status`
8. `late_status`

字段语义判断：

- `lifecycle_state` 提供总括性的 mutually exclusive final classification。
- `cycle_completeness` 表达 start/complete role completeness。
- `traceability_status` 区分 `unit_traceable`、`cycle_only`、`diagnostic_only` 与
  `not_applicable`。
- `timeline_status` 区分 in-order、out-of-order preserved、result-only、timestamp
  reversal 与 diagnostic。
- `projection_eligible` 已通过 classification table 形成唯一 boolean 语义。
- parent/detail relation fields 足以区分 attached、missing、parent OK invalid、
  duplicate 与 conflict。
- `late_status` 固定 future-only 状态，不伪装成已执行的 late classification。
- heartbeat 固定 `diagnostic_only` 且 `projection_eligible=false`。
- unit/DMC 都 absent 的 accepted production event 固定 `cycle_only`，不得展示为完整
  unit genealogy。

Non-blocking recommendations：

1. implementation fixtures 应对每一 lifecycle matrix row 断言全部八个字段，而不是只
   检查 `cycle_completeness`。
2. 后续 docs hygiene 可在字段枚举表中为 `projection_eligible` 显式补充
   `true | false` 类型。
3. future DB projection 若持久化完整 derived output，应同时保留总括字段
   `lifecycle_state`；当前 `dynamic_station_model.md` 的七字段查询清单不影响本合同八字段
   interface，也不构成 Sprint 2 blocker。

以上建议不要求 Architecture 再返修，不阻塞 R5 关闭。

## 31. R5 / DQ6 总判断与 Gate 建议

R5 / DQ6 结论：**CLOSED WITH RECOMMENDATIONS**

- 原 late 与 lifecycle matrix blocker 继续保持关闭。
- V10 修订增强了状态互斥性与 derived-output 可测试性，没有重新引入 temporal/
  lifecycle ambiguity。
- 新 Data Quality blocker：**无**。
- remaining Data Quality HOLD blocker：**无**。

本轮 Data Quality V10/R5 sanity check 总结论：

```text
PASS WITH RECOMMENDATIONS
```

| 决策 | Data Quality 建议 |
| --- | --- |
| 是否需要回 Architecture | **否** |
| 是否需要 Verification 再复验 | **否；V10 focused re-review 已关闭，建议项进入 implementation fixtures** |
| 是否可以 docs-only commit/push 当前 review stack | **可以由 ChatGPT PM 决定；必须使用精确 allowlist，且不代表 implementation authorization** |
| 是否可以进入 Sprint 2 implementation | **Data Quality 无 blocker；仅在 ChatGPT PM 明确授权后可以** |
| 是否扩大 Sprint 2 MVP | **否** |

本轮只更新：

- `docs/reports/sprint2_station_event_data_quality_review.md`

本轮未修改：

- Architecture contracts / planning / handoff。
- `docs/reports/sprint2_station_event_verification_matrix.md`。
- `docs/reports/sprint2_station_event_reliability_review.md`。
- code / tests / runtime。
- Collector / API / DB / Dashboard / V-PLC。

本轮未执行：

- 创建 `common/station_event/`。
- implementation。
- commit / push / tag / deploy。
- rollback drill。
- `git add .`。

---

## 39. Current implementation review final status

本节是文件末尾的当前最终控制结论。第 31 节是 implementation 前的历史状态；当前
implementation focused findings 与证据见第 32～36 节。

```text
HOLD
DQ-B1 historical config snapshot lineage: STILL OPEN
DQ-B4 validated NOK detail traceability: STILL OPEN
DQ-B5 raw evidence authority: STILL OPEN
R3 raw evidence / fingerprint / projection authority: STILL OPEN
R5 temporal/lifecycle traceability consistency: CLOSED
```

在 DQ-F1～DQ-F3 完成最小 implementation repair、focused tests 与 targeted sanity
re-review 前，不具备 implementation commit/push 条件。

---

## 40. Sprint 2 Data Quality Targeted Re-review Result（2026-06-23）

本节只复验上一轮 HOLD 的 DQ-F1～DQ-F3，并确认 R3 raw evidence / fingerprint /
projection authority chain；不重开完整 Data Quality review。

结论：**PASS WITH RECOMMENDATIONS**

### Focused status

- DQ-F1 parent profile/station_type lineage：**CLOSED**。
  `_parent_matches()` 的 shared parent relation 已在既有
  line/PLC/station/boot/cycle/counter/unit/DMC/config relation 上增加
  `profile_id` 与 `station_type` exact comparison。mismatch 稳定
  `reject / PARENT_EVENT_INVALID`，且不产生 projection。既有
  `event_role=production_result`、authoritative PLC/V-PLC source/actor、primary/
  secondary code-origin relation与 `30003` skip parent relation未被削弱。
- DQ-F2 cited detail role/canonical validation：**CLOSED**。
  `validated_nok_detail` cited record 必须先是 accepted lookup，再满足
  `event_type=station_nok`、自身不携带 authoritative `result`、
  `correlation.event_role=nok_detail`，并通过 historical config 下的 ordinary
  canonical `validate_event()`。随后继续 lookup accepted canonical NOK parent 并复用
  `_parent_matches()` 重放完整 parent relation。compatibility、diagnostic、wrong/
  missing role、non-accepted cited detail、non-accepted parent 与 wrong parent
  relation 均 fail closed；reject 不产生 production outcome、defect detail、
  compatibility projection、operator defect 或 Pareto input。
- DQ-F3 raw authority fail-closed：**CLOSED**。
  historical snapshot 下只要存在 `raw_payload`，就必须提供 callable
  `decode_raw_payload`；missing/exception 返回 `RAW_PARSE_ERROR`。decoder 存在时，
  raw-only 或 decoded/normalized canonical mismatch 返回
  `RAW_NORMALIZED_MISMATCH`；exact canonical match 可继续进入正常 stateful
  validation。raw rejection 发生在 duplicate/conflict/raw_variant lookup 前，因此
  raw-only、decoder-missing 与 mismatch event 不能先 accepted 或占据 authoritative
  slot。
- R3 raw evidence / fingerprint / projection authority chain：**CLOSED**。
  `validate_duplicate_or_conflict()` 的 content/raw fingerprint 规则未改变；
  same-content/same-raw 仍 duplicate，same-content/different-raw 仍
  `duplicate + RAW_VARIANT`，different-content 仍 conflict。raw_variant stateful
  fixture 同时提供 normalized payload 与 historical decoder，两个 raw variant 均
  解码到相同 canonical payload，不绕开 raw authority chain。reject、duplicate 与
  conflict 均不产生 authoritative production outcome；rejected detail 不产生 defect
  projection。

### Findings

- 未发现新的 Data Quality blocker。
- DQ-F1～DQ-F3 的修复均位于 shared validation/authority path，而不是仅靠 fixture
  特判。
- Non-blocking recommendation：当前 suite 已覆盖 DQ-F1 mismatch、cited-detail
  wrong/missing role、canonical parent replay、decoder missing/exception、
  raw-normalized mismatch、raw authority projection isolation 与合法 raw_variant。
  建议后续在允许修改 tests 的独立任务中，再增加两个具名 regression：
  `non-accepted cited detail record` 与 `raw-only + callable decoder`。本轮只读探针已
  分别确认其结果为 `UPSTREAM_EVIDENCE_INVALID` 与
  `RAW_NORMALIZED_MISMATCH`，故该覆盖粒度建议不阻塞 Gate。

### Tests

```text
git status:
HEAD/origin/main = e9abe45
working tree contains pre-existing uncommitted implementation/tests/reports/.gitignore

git diff -- common/station_event tests/test_station_event_model.py:
no tracked diff output; both requested paths are pre-existing untracked files

compileall:
PASS

focused station_event:
128 passed in 0.05s

broader tests:
216 passed in 0.92s

targeted DQ-F1/DQ-F2/DQ-F3/R3:
22 passed, 106 deselected in 0.02s

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

- `docs/reports/sprint2_station_event_data_quality_review.md`

### Scope audit

- implementation code modified：**no**
- tests modified：**no**
- contracts modified：**no**
- Collector/API/DB/Dashboard/V-PLC modified：**no**
- migration created：**no**
- tag created：**no**
- deploy：**no**
- rollback drill：**no**
- commit/push：**no**

### Decision

- Remaining Data Quality blocker：**no**
- Need Architecture repair：**no**
- Need Reliability re-review：**no**
- Need Verification targeted sanity check：**yes**。只做 DQ-F1～DQ-F3 targeted
  sanity check；不重开完整 Verification review。
- Eligible for implementation commit/push：**no**。Data Quality targeted Gate 已关闭，
  但仍须 Verification targeted sanity check 通过，并由 ChatGPT PM 给出精确 allowlist
  授权。

### Thread Health

- 本 Thread 已完成的主要任务：重读指定 implementation/tests/reports/handoff；复验
  DQ-F1～DQ-F3 与 R3 authority chain；运行 128/216 tests、22 个 targeted tests 与
  3 个独立边界探针；形成 targeted Gate 结论。
- 当前上下文是否仍适合继续：**适合完成本轮 Data Quality 收口；不应在本 Thread
  扩大到 Verification、implementation 或 commit/push。**
- 是否建议新开 Thread：**yes**。
- 如果建议新开，请给出 handoff 摘要：基线 `e9abe45`；Data Quality DQ-F1～DQ-F3
  与 R3 authority chain 已 CLOSED；128/216 tests PASS；22 个 targeted tests PASS；
  下一步仅做 Verification DQ-F1～DQ-F3 targeted sanity check；通过并获得 PM 精确
  授权前不得 commit/push/integration。
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：**低**。新
  Thread 应至少读取本节、implementation report 第 13 节、`_config()`、
  `_evidence_error()`、`_parent_matches()` 与对应 targeted tests。

## 41. Current Data Quality control conclusion

本节覆盖第 39 节 HOLD：

```text
PASS WITH RECOMMENDATIONS
DQ-F1 parent profile/station_type lineage: CLOSED
DQ-F2 cited detail role/canonical validation: CLOSED
DQ-F3 raw authority fail-closed: CLOSED
R3 raw evidence / fingerprint / projection authority chain: CLOSED
```

Data Quality remaining blocker 已清零。本结论不授权 commit/push；Verification
DQ-F1～DQ-F3 targeted sanity check 与 ChatGPT PM 精确授权完成前，不得进入
Collector/API/DB/Dashboard/V-PLC integration。
