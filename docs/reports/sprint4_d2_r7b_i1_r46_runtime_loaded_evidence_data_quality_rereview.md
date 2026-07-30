# Sprint 4 D2-R7B-I1 R46 Runtime-Loaded Evidence Data Quality Re-review

## 1. 报告身份、authority 与 terminal decision

- 任务：D2-R7B-I1 R46 — Focusedly Re-review DQ-B1, DQ-B2 and DQ-B3 Against the R42 + R45 Combined Contract
- 执行 Thread：Data Quality
- Authority source / ID：PM-D2-R7B-I1-R46-RUNTIME-LOADED-EVIDENCE-DATA-QUALITY-REREVIEW-260730-1053
- Delivery：REPOSITORY_DURABLE_REPORT
- 唯一 task-owned output：docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md
- Review scope：仅 DQ-B1、DQ-B2、DQ-B3；不重开开放式 Reliability review，不扩大 assurance scope。

### Terminal decision

```
PASS / DATA_QUALITY_REREVIEW_ACCEPTS_R42_R45_COMBINED_CONTRACT
NON_BLOCKING_RECOMMENDATIONS_PRESENT
```

本结论只表示 R42 + R45 combined candidate contract 通过本轮 focused Data Quality re-review，允许进入 ChatGPT PM durable intake，再由 PM 单独决定是否发布 independent Verification planning review authority。它不表示 implementation、tests、fresh remote observation、RUNTIME-LOADED 或 PRODUCTION-ACCEPTED。

## 2. Fresh Git recovery 与 baseline

本轮在 task-owned write 前执行了 Prompt 要求的只读 recovery；live facts 如下：

| Field | Live fact | Result |
| --- | --- | --- |
| repository root | /Users/chenjie/Documents/MES/edge-mes-demo | PASS |
| branch | main | PASS |
| HEAD | ce22ca71eff0548aa064129c160f7041603855e7 | PASS |
| origin/main | ce22ca71eff0548aa064129c160f7041603855e7 | PASS |
| HEAD^ | 35c50b1eb0f76d8b3361e8c122448ad03899559b | PASS |
| ahead / behind | 0 / 0 | PASS |
| tracked dirty | empty | PASS |
| cached | empty | PASS |
| git diff --check | PASS | PASS |
| git diff --cached --check | PASS | PASS |
| initial untracked | 307 | PASS |
| R46 output before write | ABSENT / NON-SYMLINK / UNTRACKED / UNSTAGED | PASS |

R36 authority materialization plan 的 exact Batch D/E closure 为 301 paths（Batch D 300、Batch E 1）。加上 R40–R45 六个 exact report paths 后 expected untracked set 为 307。按 repository-relative UTF-8 path 稳定排序，和 live untracked set 的 comm -3 比较为空：

```
unknown paths = 0
missing paths = 0
set equality = PASS
```

Batch D/E 未被读取、评审、删除、移动或重新分类；本轮只读取 R36 JSON authority 所需的 exact path list。

## 3. R42 / R43 / R44 / R45 exact input identity

四个 input 均为 regular UTF-8、NON-SYMLINK、UNTRACKED、UNSTAGED；均未被本轮修改。

| Input | Bytes | SHA-256 | State |
| --- | ---: | --- | --- |
| docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md | 32319 | dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165 | PM-ACCEPTED CANDIDATE BASE / RELIABILITY-ACCEPTED / UNTRACKED / UNSTAGED / NOT COMMITTED / NOT FINAL |
| docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md | 30244 | 95b2e63c4879fb5af6920b262300566c577612dd1753b13bf59928c1417338e8 | RELIABILITY RE-REVIEW PASS / PM DURABLE INTAKE ACCEPTED / UNTRACKED / UNSTAGED / NOT COMMITTED |
| docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md | 43036 | 3b4d1f3451d0b0036e5530bc83eb35b90ee2b6d140b0a2799b82df1ada035bfa | DATA QUALITY HOLD / PM-REVIEWED / PM-VERIFIED / HOLD ACCEPTED / UNTRACKED / UNSTAGED / NOT COMMITTED |
| docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md | 13786 | 8fd646f24565bbcb27aa9063038774fee3b5398d66566f961bee296ffff02ef2 | SCOPE-RESET CONTRACT WRITTEN / PM-REVIEWED / PM-VERIFIED / ACCEPTED AS R46 INPUT / UNTRACKED / UNSTAGED / NOT COMMITTED / NOT DATA-QUALITY-ACCEPTED / NOT FINAL |

R35 durable evidence was read only for the accepted phase boundary. Its relevant classification remains ACTIVATED = YES, STATIC_MAPPING_INITIALIZED = YES, RUNTIME-LOADED = NO, PRODUCTION-ACCEPTED = NO；its historical image/config identity is not reused as future freshness authority.

## 4. R42 + R45 combined-contract assessment

### 4.1 Bounded-addendum assessment

R42 continues to control the candidate base application contract. R45 is a bounded addendum, not a hidden R42 rewrite or an R44 rewrite. R45 controls only these three subjects：

1. canonical line_id authority and emission-time consistency（DQ-B1）；
2. later source/image/config/process terminal binding（DQ-B2）；
3. later raw-log/payload/parsed-evidence identity（DQ-B3）。

R45 explicitly leaves all other R42 clauses unchanged, including：

- startup context and mandatory context creation；
- single-use consumption；
- PID check；
- exactly-one and duplicate/cardinality/scope checks；
- deterministic application-message grammar and strict parser boundary；
- constructor emission order；
- logger/serialization failure propagation；
- v1 shape；
- PLC/DB/accepted-fact/ACK/read_done semantics；
- runtime/production truth boundary；
- exact three-source/two-test implementation allowlist。

因此 R45 没有改变 R43 已审查的 Reliability mechanism。R43 对 unchanged R42 clauses 继续有效；本轮不需要重新打开 Reliability。

### 4.2 Current product boundary

```
ACTIVATED                  = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED             = NO
PRODUCTION-ACCEPTED        = NO
```

当前源码仍没有实现 runtime-loaded success record，load_edge_mapping() 仍是现状的 text-read 路径；这属于 future implementation contract 尚未执行的状态，不是本轮 Data Quality contract re-review 的 blocker。R46 未执行 source/test repair、tests、application construction 或 runtime validation。

## 5. DQ-B1 closure：canonical line identity

### 5.1 Canonical / routing line authority matrix

| Value | Authority role | R46 decision |
| --- | --- | --- |
| EventCollectorWorker.resolved_config_snapshot.line_id | canonical line authority used by record | ACCEPTED |
| EventCollectorWorker.mapping.runtime_snapshot.line_id | equivalent authoritative origin | ACCEPTED |
| top-level EdgeMapping.line_id | same parsed top-level line identity feeding the runtime snapshot | ACCEPTED as same semantic identity |
| selected PLC entry line_id | selected runtime routing projection | NOT independent semantic authority |
| EventCollectorWorker.self.line_id | current first-selected-PLC routing projection used by existing runtime/DB paths | NOT independent semantic authority |
| emitted record line_id | canonical snapshot line value | MUST use canonical value |

The current source parses top-level line_id into EdgeMapping, creates RuntimeMappingSnapshot with that same value, includes the line identity in the runtime semantic hash, and builds ResolvedConfigSnapshot from that hash-bound snapshot. The selected PLC entry and self.line_id remain routing projections. R45 therefore closes the previous ambiguity without introducing a multi-PLC product feature or changing first-selected-PLC behavior.

### 5.2 Emission-before-fail-closed contract

R45 requires all of the following before success serialization and emission：

- canonical line is a non-empty string；
- selected PLC entry exists；
- selected routing line exists and is a non-empty string；
- selected routing line equals canonical line；
- record uses canonical snapshot line；
- missing, empty, mismatch or ambiguous routing identity produces no success record。

This is sufficient to prevent a PLC projection from being paired with a different hash-bound top-level line. The check is an application-record gate only；it does not change PLC connection, DB, accepted-fact, ACK/read_done or production semantics.

### 5.3 DQ-B1 test-contract sufficiency

The existing two-test allowlist contains the necessary responsibility split. The future matrix is complete for this blocker：

- equal canonical/routing line produces success；
- missing routing line produces no record；
- empty routing line produces no record；
- routing/canonical mismatch produces no record；
- record emits the canonical snapshot line；
- schema, config, line and resolved hash are from the same snapshot；
- mismatch fails before serialization/emission；
- existing PLC/DB/accepted-fact/ACK/read_done behavior remains unchanged。

No test was executed in R46。

**DQ-B1：CLOSED。** No residual cross-line false-PASS blocker remains in the combined contract。

## 6. DQ-B2 closure：terminal source-to-record binding

### 6.1 Terminal chain

R45 freezes the following later-gate chain；each arrow requires an identity match or explicit binding：

```
accepted implementation source identity
→ accepted built/deployed full image ID
→ fresh active full image ID
→ fresh active full container ID + StartedAt
→ fresh active Collector main PID/process identity
→ fresh current container-visible mapping bytes
→ process-emitted mapping_content_sha256/resolved_config_hash
→ parsed v1 record
```

Missing, mismatch, stale, tag-only or ambiguous evidence is HOLD。R46 accepts this as a complete terminal contract, not as a claim that the chain has been freshly observed.

### 6.2 Non-self-referential expected-authority matrix

| Subject | Required independent expected authority | R46 decision |
| --- | --- | --- |
| accepted source | future reviewed Git closeout commit plus exact path manifest | complete |
| accepted image vs active image | full image ID comparison | complete |
| image identity | full top-level Image；not tag, Config.Image, short ID or hostname | complete |
| active container/process | fresh container belongs to fresh active image；PID/process belongs to that container | complete |
| mapping bytes | fresh read-only read from current active container | complete |
| deployed config binding | container-visible bytes bound to approved deployed config/image | complete |
| historical R35 image/config hash | diagnostic/history only；not future freshness authority | complete |
| record self-reported hashes | assertion only；never own expected authority | complete |
| local committed config | expected source only after deployment binding proves active visibility | complete |

The chain does not require the application to access Docker API, remote filesystem, Git metadata, status endpoint or DB. It does not add Git/image/container/deployment/raw-artifact fields to the current application record.

### 6.3 Current application scope non-expansion

The current three-source implementation allowlist remains unchanged：

| Source path | Necessary | Sufficient with the other two | Responsibility | Additional path |
| --- | --- | --- | --- | --- |
| collector/app/main.py | yes | yes | main-entry context/time/PID and exactly-one worker handoff | none |
| collector/app/services/event_collector.py | yes | yes | context single-use/PID, canonical line check, B1 validation, exact record and one-shot emission | none |
| collector/app/plc/mapping.py | yes | yes for raw-byte binding | one-read bytes/hash/decode/parse binding and raw identity exposure | none |

resolved_config_registry.py、read_plan.py、config/mapping.yaml、collector/Dockerfile、docker-compose.yml、Storage、PLC/DB/ACK/read_done and production surfaces are not missing current implementation paths for this focused contract. DQ-B2 remains a later deployment/runtime-validation gate, not current application-record expansion。

**DQ-B2：CLOSED。** No stale/foreign/tag-only/self-referential authority PASS remains allowed by R45。

## 7. DQ-B3 closure：bounded evidence classes and raw-byte lineage

### 7.1 A–H evidence-class assessment

| Class | Required bounded evidence | R46 decision |
| --- | --- | --- |
| A | raw transport artifact：current full-container-ID-scoped exact bytes, interval, length, SHA-256 | complete |
| B | observation metadata：authority/command, active container/image/process/start identity, bounded time, raw binding；no credential | complete |
| C | selected raw-line identity：byte offset or stable line ordinal, exact bytes/hash；selection from raw artifact | complete |
| D | exact application-message bytes：formatter/transport prefix removed, exact literal start, length/hash, reversible to selected line | complete |
| E | exact JSON payload bytes：one delimiter after all remaining bytes, independent length/hash, no trim/normalize/reserialize | complete |
| F | parsed v1 object：derived from exact payload with exact key/type/schema validation | complete |
| G | comparison terminal：expected source, actual, result, lineage and PASS/HOLD classification | complete |
| H | manifest：A–G exact paths, bytes and hashes bound after final validation | complete |

R45 does not choose future artifact filenames. That is intentional and correct：future Verification/runtime-validation Prompt must freeze exact paths for A–H before creating them.

### 7.2 Raw-to-parsed byte lineage

The combined contract requires：

```
bounded raw transport bytes
→ selected raw line by byte offset/stable ordinal
→ exact application-message bytes
→ exact JSON payload bytes after one delimiter
→ parsed v1 object
→ per-field expected/actual comparison
→ A–H manifest binding
```

The parsed object is derived evidence and cannot replace raw bytes or payload bytes. Payload bytes cannot be trimmed, normalized or reserialized for authority. A missing raw artifact, unavailable current observation or broken identity binding is HOLD, not an invitation to build long-term retention, telemetry, DB persistence, generic audit or forensics infrastructure。

### 7.3 Parser Data Quality minimum

The future parser contract is complete and must：

- reject duplicate JSON member names；
- distinguish JSON boolean from integer；
- reject numeric strings in place of integers；
- reject missing or extra keys；
- reject unknown schema/event；
- preserve internal strings without trim/normalization；
- validate extra keys rather than discard them first；
- never substitute reserialized JSON for exact payload；
- classify malformed, partial, duplicate, ambiguous or missing records as HOLD。

These are future helper/test responsibilities within the existing two-test allowlist；no parser source path is added to the current application allowlist。

**DQ-B3：CLOSED。** No parsed-only or normalized-only evidence PASS remains allowed。

## 8. v1 shape、expected values 与 truth boundary

### 8.1 Exact v1 field set

R42 + R45 retain exactly these 11 fields；除 canonical line_id source rule 外不增删：

```
collector_main_started_at_utc
config_version
evidence_schema_version
event_type
line_id
mapping_content_sha256
mapping_path
mapping_schema_version
process_pid
read_plan_count
resolved_config_hash
```

No image ID, container ID, Git commit, deployment manifest, raw artifact hash, scope list or record_emitted_at field is added。

### 8.2 Future non-self-referential expected-value matrix

| Field/group | Expected source |
| --- | --- |
| schema/event | frozen R42 + R45 literals |
| mapping path | approved deployment contract plus fresh container observation |
| raw mapping SHA | fresh exact bytes visible in active container, bound to approved deployed config/image |
| mapping schema/config/canonical line | independent parse of those exact bytes |
| read-plan count | independent derivation from exact bytes under R42 scope rules：one line plus all configured stations, including disabled |
| resolved hash | independent semantic recomputation from those exact bytes |
| PID/time | fresh active process/container observations |
| source/image | accepted source manifest plus accepted/full active image identities |
| raw log lineage | exact raw artifact/hash → selected line → application message → payload → parsed object |

The runtime record is an assertion to compare, never its own expected-value authority。

### 8.3 Runtime / production truth boundary

```
runtime-loaded record = runtime configuration/process evidence
not = station event
not = accepted station-event fact
not = DB-backed production fact
not = PLC acknowledgement
not = read_done authority
not = machine-state truth
not = production acceptance
not = UI production truth
```

R46 does not authorize DB/API/PLC/V-PLC access, accepted-fact generation, ACK/read_done handling, production event generation or any upgrade from runtime evidence to production truth。

## 9. Reliability non-regression assessment

R45 expressly preserves R43-reviewed mechanisms. The DQ additions are bounded to record authority and later evidence binding；they do not alter：

- startup-context lifecycle, single-use or PID validation；
- exactly-one/current-start boundary；
- duplicate/cardinality/scope validation and disabled-station required scope；
- deterministic application grammar and strict parser boundary；
- serialization/logger error propagation；
- constructor emission order；
- PLC selection, polling, DB, accepted-fact, ACK/read_done or production semantics。

The DQ-B1 routing/canonical equality check is an emission-before-success guard and preserves first-selected-PLC behavior. It is not a Reliability mechanism rewrite。

Reliability clauses unchanged：yes。

## 10. Three-source / two-test allowlist review

### Source paths

The three source paths are necessary and sufficient together for the current contract. No additional current implementation path is required. In particular, later source/image/config/process binding and A–H artifacts are not reasons to add current application files。

### Test paths

| Test path | Necessary | Sufficient with the other test | Responsibility | Additional path |
| --- | --- | --- | --- | --- |
| collector/tests/test_event_collector_reliability.py | yes | yes | constructor context/one-shot/PID, emission order, line consistency and no-side-effect/regression semantics | none |
| tests/test_collector_station_event_runtime_source.py | yes | yes | same-byte raw identity, parse/hash failures, mapping/scope fixtures, strict payload and manual/static evidence boundary | none |

No pytest、compileall、application process or test helper was run. Existing source/test paths are unchanged relative to HEAD；no credible missing current path was found。

## 11. New credible blocker assessment

R46 used only the permitted blocker classes：

| Candidate | R46 result |
| --- | --- |
| DQ-B1 cross-line false PASS | closed by canonical snapshot authority plus emission-before-fail-closed routing equality |
| DQ-B2 stale/foreign/tag-only/self-referential PASS | closed by terminal source→image→container/process→mapping bytes→record chain |
| DQ-B3 parsed/normalized evidence replacing raw evidence | closed by A–H classes and exact raw/payload lineage |
| runtime metadata represented as production truth | closed by explicit truth boundary and v1 exclusions |
| current three-source/two-test allowlist unable to implement DQ-B1 | no；allowlist is necessary/sufficient |
| R45 changes a Reliability-reviewed mechanism | no；R45 preserves R43 clauses |

No new credible Data Quality blocker exists。以下均未被提升为 blocker：generic telemetry taxonomy、long-term retention、complete supply-chain security、cryptographic provenance、hostile same-process forgery、extra diagnostic fields、scope list、production accepted-fact validation、future artifact filenames。

## 12. Bounded non-blocking recommendations

以下建议不改变本轮 PASS，不增加 current source/test allowlist，不授权 runtime execution：

1. Future implementation test 应明确验证 startup-context consumer 在 constructor failure 后仍保持 consumed，防止 retry/reuse 形成 success capability。
2. Future Verification helper 保持 raw transport adapter、application-message extractor 与 JSON parser 为可分别审查的阶段，同时保留 exact bounded evidence。
3. 继续把 record_emitted_at 与 sorted scope list 留在 backlog，除非 PM 以后以具体 false-PASS 风险另行冻结。
4. 保持 no-API/no-DB/no-telemetry/no-generic-registry/no-production semantics。

NON_BLOCKING_RECOMMENDATIONS_PRESENT 只表示后续 focused implementation/Verification review 的 bounded carry-forward，不表示当前 gate 缺陷。

## 13. Changed-path / authority audit

本轮 task-owned changed set 只有：

```
docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md
```

本轮未修改：

- R42、R43、R44、R45；
- collector/app/main.py、collector/app/services/event_collector.py、collector/app/plc/mapping.py、collector/app/plc/read_plan.py、collector/app/services/resolved_config_registry.py；
- config/mapping.yaml、collector/Dockerfile、docker-compose.yml；
- 两个 exact test paths；
- status、roadmap、handoff、PM rules；
- Batch D/E；
- 任何 helper、fixture、manifest、terminal JSON 或第二份 report。

Git index、commit、push、remote state 均未改变。

## 14. Final Git/index/untracked audit

写入 R46 后，expected untracked set 变为 R36 Batch D/E 301 + R40–R46 7 = 308。最终 detached read-only audit 必须并已用于验证：

```
HEAD == origin/main == ce22ca71eff0548aa064129c160f7041603855e7
HEAD^ == 35c50b1eb0f76d8b3361e8c122448ad03899559b
ahead / behind == 0 / 0
tracked dirty == empty
cached == empty
initial untracked == 307
final untracked == 308
Batch D == 300
Batch E == 1
R40 == 1
R41 == 1
R42 == 1
R43 == 1
R44 == 1
R45 == 1
R46 == 1
unknown paths == 0
missing paths == 0
set equality == PASS
```

R46 final path identity：

```
path: docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md
regular UTF-8: yes
symlink: no / NON-SYMLINK
index: UNSTAGED / UNTRACKED
bytes/SHA-256: detached final post-write audit, returned in the concise Chat manifest
```

报告不能把自身最终 SHA-256 嵌入自身而保持该 SHA 不变；因此 R46 的最终 bytes/SHA-256 采用写入后的 detached read-only audit 记录，并在 Chat manifest 返回。该 detached identity 不是第二个 artifact，也不改变 exact report allowlist。

## 15. Evidence boundary

```
DATA-QUALITY-RE-REVIEWED
WRITTEN
NOT REPAIRED
NOT IMPLEMENTED
NOT TESTED
NOT STAGED
NOT COMMITTED
NOT PUSHED
NO FRESH REMOTE OBSERVATION
NOT VERIFICATION-ACCEPTED
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED
```

## 16. MVP alignment

```
MVP-ALIGNED WITH BACKLOG ITEMS
```

本轮只收敛阻止 runtime-loaded evidence false PASS 的最小 Data Quality authority：canonical line、later source/image/config/process binding、bounded raw/payload/parsed lineage。没有引入 API、DB persistence、telemetry、generic registry、audit/forensics、cryptographic provenance 或 long-term retention subsystem。当前 assurance claim 未膨胀。

## 17. Next gate 与 Thread context

如果 R46 PASS，唯一 next gate：

```
R46 focused Data Quality re-review WRITTEN
→ ChatGPT PM durable intake only
→ PM may separately issue an independent Verification planning review
  of the R42 + R45 combined contract
```

本 Thread 立即 terminalized：

```
continue current Thread: no
new Thread recommended: yes
reason: R44 Data Quality HOLD 已由新的独立 R46 Thread 仅针对 DQ-B1/DQ-B2/DQ-B3 完成复核；后续 Verification planning 必须由 PM 另行发布新 authority，不得继承本轮 PASS 自动执行。
```

R46 PASS、R45 scope reset、R43 Reliability PASS 与本报告 recommendations 均不得推断 implementation、Verification execution、Git closeout、build/deploy、Docker/Collector lifecycle、fresh remote observation、RUNTIME-LOADED acceptance 或 production accepted-fact authority。

End state：DATA-QUALITY-RE-REVIEWED / WRITTEN ONLY。
