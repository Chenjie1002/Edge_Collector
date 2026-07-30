# Sprint 4 D2-R7B-I1 R45 Runtime-Loaded Evidence Scope Reset Contract

## 1. 报告身份与 terminal decision

- 任务：D2-R7B-I1 R45 — Produce a Bounded Scope-Reset Addendum for Canonical Line Identity and Later Runtime-Validation Evidence Binding
- 执行 Thread：Architecture / Integration
- Authority：PM-D2-R7B-I1-R45-RUNTIME-LOADED-EVIDENCE-SCOPE-RESET-260730-1036
- Delivery：REPOSITORY_DURABLE_REPORT
- 唯一输出：docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md
- Authority：仅本文件的 docs write；无 source/test/runtime/Git/remote authority；不继承旧 Thread 权限。

结论：

~~~
PASS / RUNTIME_LOADED_EVIDENCE_SCOPE_RESET_READY_FOR_DATA_QUALITY_REREVIEW
~~~

本报告是 bounded scope-reset addendum，不是 R42/R44 的重写或复制。它冻结 DQ-B1、DQ-B2、DQ-B3 的后续 authority boundary；写入本身不表示 Data Quality accepted、Verification accepted、final PM accepted、implementation、test、Git closeout、fresh remote observation、RUNTIME-LOADED 或 PRODUCTION-ACCEPTED。

## 2. Fresh recovery、输入身份与 working-tree boundary

本轮在 task-owned write 前完成 live recovery：

| Field | Live fact |
| --- | --- |
| repository root | /Users/chenjie/Documents/MES/edge-mes-demo |
| branch | main |
| HEAD / origin/main | ce22ca71eff0548aa064129c160f7041603855e7 / same |
| HEAD^ | 35c50b1eb0f76d8b3361e8c122448ad03899559b |
| ahead / behind | 0 / 0 |
| tracked dirty / cached | empty / empty |
| diff checks | git diff --check PASS; cached PASS |
| initial untracked | 306 |
| composition | Batch D 300 + Batch E 1 + R40–R44 5 |
| R45 before write | ABSENT / NON-SYMLINK / UNTRACKED / UNSTAGED |

R36 authority closure 使用 exact Batch D/Batch E paths；与 R40–R44 按 repository-relative UTF-8 稳定排序比较：expected 306、live 306、unknown 0、missing 0。Batch D/E 未读取、评审、删除、移动或重新分类。

输入身份均匹配 PM Prompt：

| Input | Bytes | SHA-256 | State |
| --- | ---: | --- | --- |
| R42 docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md | 32319 | dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165 | PM-ACCEPTED CANDIDATE BASE / RELIABILITY-ACCEPTED / UNTRACKED / UNSTAGED / NOT FINAL |
| R43 docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md | 30244 | 95b2e63c4879fb5af6920b262300566c577612dd1753b13bf59928c1417338e8 | RELIABILITY PASS / PM-ACCEPTED / UNTRACKED / UNSTAGED |
| R44 docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md | 43036 | 3b4d1f3451d0b0036e5530bc83eb35b90ee2b6d140b0a2799b82df1ada035bfa | DATA QUALITY HOLD / PM-VERIFIED / HOLD ACCEPTED / UNTRACKED / UNSTAGED |

当前产品边界保持：

~~~
ACTIVATED                  = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED             = NO
PRODUCTION-ACCEPTED        = NO
~~~

## 3. R42/R45组合 authority 与 supersession

R42 仍是 candidate base application contract。R45 仅控制并 supersede 以下 R42 subjects：

| R45 subject | R45 control |
| --- | --- |
| DQ-B1 | canonical line_id authority and consistency |
| DQ-B2 | later source/image/config/process terminal binding |
| DQ-B3 | later raw-log/payload/parsed-evidence artifact identity |

所有其他 R42 clauses unchanged。R43 对未改变的 Reliability mechanisms 继续有效；R45 不改变 startup context、single-use、PID check、exactly-one scope、duplicate/cardinality/scope rules、deterministic application grammar、parser acceptance grammar、constructor emission order 或 logger/serialization failure behavior。若未来需要改变任一项，必须返回 PM 并 HOLD，不能在 R45 中写成 PASS。

R45 不 supersede R42 的 v1 shape、three-source/two-test implementation allowlist、PLC/DB/accepted-fact/ACK/read_done semantics、runtime/production truth boundary或其他未列明条款。

PM scope/assurance decision：DQ-B1 是 current application-contract blocker；DQ-B2 是 later deployment/runtime-validation terminal-binding blocker、不是 current application source-allowlist blocker；DQ-B3 是 later Verification evidence-artifact blocker、不是 current application logging-storage 或 telemetry blocker。R43 Reliability acceptance 对 unchanged R42 clauses 继续有效；本轮不要求 fresh Reliability re-review。

## 4. DQ-B1：canonical line_id 与 emission 前一致性

唯一 canonical authority：

~~~
canonical_line_id = EventCollectorWorker.resolved_config_snapshot.line_id
equivalent authoritative origin = EventCollectorWorker.mapping.runtime_snapshot.line_id
record line_id = canonical_line_id
~~~

EdgeMapping.line_id、RuntimeMappingSnapshot.line_id 与 ResolvedConfigSnapshot.line_id 必须表示同一 top-level、semantic-hash-bound line identity；resolved_config_hash 与该 snapshot 绑定。EventCollectorWorker.self.line_id 和 selected PLC entry 的 line_id 只能是 runtime routing projection，不是 independent semantic authority。

在 success serialization 和 emission 之前，future implementation 必须 fail closed 验证：

1. canonical line ID 是 non-empty string；
2. selected PLC entry 存在，继续使用当前 first-selected-PLC behavior；
3. selected PLC routing line_id 存在且是 non-empty string；
4. selected routing line_id == canonical_line_id；
5. emitted record 使用 canonical snapshot value，而不是 unchecked routing projection；
6. missing、mismatch、ambiguous selected routing identity 均无 success record。

不得改变 first-PLC selection、增加 multi-PLC routing、改变 production line model、把所有 PLC entries 放入 record 或改变 resolved-hash algorithm。

Future focused tests 必须在原 exact two-test allowlist 内覆盖：equal success；routing line missing、empty、mismatch 时 no success；record 输出 canonical snapshot line；resolved hash/schema/config/line 来自同一 snapshot；mismatch 在 serialization/emission 前失败；既有 PLC/DB/accepted-fact/ACK/read_done semantics 不变。

## 5. DQ-B2：later terminal source-to-record binding

后续 deployment/runtime-validation 才建立以下 terminal chain；每个箭头都必须 identity match 或有明确绑定：

~~~
accepted implementation source identity
→ accepted built/deployed full image ID
→ fresh active full image ID
→ fresh active full container ID + StartedAt
→ fresh active Collector main PID/process identity
→ fresh current container-visible mapping bytes
→ process-emitted mapping_content_sha256/resolved_config_hash
→ parsed v1 record
~~~

缺失、mismatch、stale、tag-only 或 ambiguous 任一环节均为 HOLD。accepted implementation source identity 只能来自未来经 review、Git closeout 后冻结的 commit 与 exact path manifest。descriptive tag、Config.Image、short ID、hostname 均不是 full image authority；accepted image 与 fresh active image 必须比较 full image ID。mapping bytes 必须对 current active container fresh read-only 获取并绑定到 accepted deployment/image；R35 historical image/config hash 不能自动成为 future fresh authority；record 自报 hash 不能成为自身 expected authority。local committed config 只有在 deployment evidence 绑定到 active container-visible bytes 后，才能作为 expected source。

该 chain 属于 later gate；不要求当前 application record 增加 Git commit、image ID、container ID、deployment manifest、remote filesystem query、Docker API、status endpoint 或 DB persistence。

Current future application implementation 仍只允许：

~~~
collector/app/main.py
collector/app/services/event_collector.py
collector/app/plc/mapping.py
~~~

Current future application tests 仍只允许：

~~~
collector/tests/test_event_collector_reliability.py
tests/test_collector_station_event_runtime_source.py
~~~

source/image/deployment binding 由 separate Git/build/deploy/runtime-validation authorities 建立；本 R45 不扩大 allowlist。

## 6. DQ-B3：bounded Verification evidence identity

一次 bounded runtime-validation execution 的 evidence classes 固定为以下 A–H。Future Prompt 必须为每类声明 exact repository path；R45 不选择具体路径。

| Class | Required bounded identity |
| --- | --- |
| A raw transport artifact | one current full-container-ID-scoped observation 的 exact bytes、full active container ID、observation start/end、byte length、SHA-256；不得先 normalize、reserialize 或只保存 parsed object |
| B observation metadata | command/authority ID、active container/image/process/start identities、bounded time、raw artifact path/hash；不得含 credential |
| C selected raw-line identity | raw artifact byte offset 或 stable line ordinal、exact selected raw-line bytes/hash；selection 必须来自 raw artifact，不得 substring 命中其他 line |
| D exact application-message bytes | 移除 formatter/transport prefix 后的 exact application component、exact literal start、byte length、SHA-256；可回溯到 selected raw line |
| E exact JSON payload bytes | one delimiter 之后的全部剩余 bytes、独立 length/SHA-256；不得 trim、normalize 或以 reserialized JSON 代替 |
| F parsed v1 object | 由 exact payload bytes 解析，exact key/type/schema validation；derived evidence，不替代 raw/payload authority |
| G comparison terminal | expected source、actual value、comparison result、lineage result、terminal/diagnostic classification、overall PASS/HOLD |
| H manifest | 绑定 A–G 全部 exact paths、bytes、SHA-256，防止 final validation 后 artifact 改变 |

Future parser minimum：拒绝 duplicate JSON member names；严格区分 boolean 与 integer；拒绝 numeric string 代替 integer；拒绝 missing/extra fields、unknown schema/event；不 trim/normalize 内部 string、不先丢弃 extra keys、不以 reserialized JSON 替代 exact payload。malformed、partial、duplicate、ambiguous、missing record 均 HOLD。

## 7. Unchanged v1、expected authority 与 truth boundary

R42 v1 仍只有以下 11 个 exact fields，除 DQ-B1 的 canonical source rule 外不增删：

~~~
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
~~~

不增加 image/container/Git/raw-artifact/scope/record-emitted-at/deployment fields。

Future Verification 的 non-self-referential expected authority：schema/event 使用 R42+R45 frozen literals；mapping path 使用 approved deployment contract + fresh container observation；raw mapping SHA 使用 fresh active-container-visible exact bytes 并绑定 approved deployed config；schema/config/canonical line 使用这些 exact bytes 的 independent parse；read-plan count 由 exact bytes 按 R42 scope rules independent derive；resolved hash 由 exact bytes independent semantic recompute；PID/time 使用 fresh active process/container observations；source/image 使用 accepted source manifest 与 accepted/full active image IDs。runtime record 只是 assertion，不能是自身 expected authority。

RUNTIME-LOADED record 仍只表示 runtime configuration/process evidence，不是 station event、accepted station-event fact、DB-backed production fact、PLC acknowledgement、read_done authority、machine-state truth、production acceptance 或 UI production truth。

## 8. Gate、audit 与 MVP assessment

后续 sequence 冻结为：

~~~
R45 scope-reset addendum
→ ChatGPT PM durable intake
→ focused independent Data Quality re-review of DQ-B1/B2/B3 only
→ ChatGPT PM durable intake
→ independent Verification planning review of R42 + R45
→ ChatGPT PM final planning-contract acceptance
→ separately authorized implementation
→ focused implementation reviews
→ separately authorized Git closeout
→ separately authorized build/deployment
→ separately authorized bounded runtime validation
→ PM acceptance of RUNTIME-LOADED
→ separate production accepted-fact planning
~~~

本轮唯一 changed path 是 R45 exact report；未修改 R42/R43/R44、source、tests、config、Dockerfile、Compose、status、roadmap、handoff、PM rules 或 Batch D/E。未执行 tests/application、remote/Docker/Compose、network/SSH、DB/API/PLC/V-PLC、lifecycle、Git add/stage/commit/push/tag、cleanup/restore/reset/stash/clean。

Terminal evidence boundary：

~~~
SCOPE-RESET CONTRACT WRITTEN
NOT DATA-QUALITY-ACCEPTED
NOT VERIFICATION-ACCEPTED
NOT FINAL PM-ACCEPTED
NOT IMPLEMENTED
NOT TESTED
NOT STAGED
NOT COMMITTED
NOT PUSHED
NO FRESH REMOTE OBSERVATION
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED
~~~

MVP classification：MVP-ALIGNED WITH BACKLOG ITEMS。本 addendum 只收敛三个 Data Quality authority boundaries；不建立 API、DB persistence、telemetry、generic registry、audit/forensics 或 retention subsystem。

Thread context：当前 Architecture / Integration Thread terminalized；continue current Thread: no；new Thread recommended: yes。下一步仅为 ChatGPT PM durable intake。

## 9. R45 final file identity

R45 是 regular UTF-8 file、NON-SYMLINK、UNSTAGED、UNTRACKED、NOT COMMITTED。由于报告不能在不改变自身 bytes 的情况下嵌入自己的 SHA-256，最终 bytes/SHA-256 由写入后的 detached read-only audit 测量，并在 Chat manifest 返回；该 detached identity 不是第二个 artifact。

~~~
path: docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md
file type: regular UTF-8
symlink: NO / NON-SYMLINK
index: UNSTAGED / UNTRACKED
final bytes/SHA-256: detached final audit in Chat manifest
~~~
