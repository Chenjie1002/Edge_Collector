# Sprint 4 D2-R7B-I1 R43 Process-Bound Runtime-Loaded Observability Reliability Re-review

## 1. 报告身份、结论与交付分类

报告名称：Sprint 4 D2-R7B-I1 R43 Process-Bound Runtime-Loaded Observability Reliability Re-review

任务名称：D2-R7B-I1 R43 — Independently Re-review the Consolidated R42 Contract for Closure of Reliability Blockers B1–B3

执行 Thread：Reliability

Authority source / ID：PM-D2-R7B-I1-R43-PROCESS-BOUND-RUNTIME-LOADED-RELIABILITY-REREVIEW-260730-0940

Report delivery mode：REPOSITORY_DURABLE_REPORT

唯一允许写入路径：

~~~
docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md
~~~

Authority properties：

~~~
AUTHORIZED ONCE
INDEPENDENT RELIABILITY RE-REVIEW
LOCAL DOCS WRITE ONLY
NO REPAIR
NO SOURCE OR TEST WRITE
NO RUNTIME AUTHORITY
NOT REUSABLE
~~~

Terminal decision：

~~~
PASS / RELIABILITY_REREVIEW_ACCEPTS_R42_CONSOLIDATED_CONTRACT
~~~

R42 的 B1–B3 repair contract 已通过独立 Reliability re-review。没有发现新的 credible false-PASS、stale/foreign-process acceptance、required-initialization failure 后仍产生 success record、unauthorized PLC/DB/ACK/production side effect、allowlist 不可实现或 local/static evidence 被误分类为 runtime evidence 的 blocker。

本结论只接受 R42 作为后续 PM durable intake 的 candidate contract；不表示 R42 已由 PM final-accepted，不表示 source/test 已实现或通过测试，也不授予任何 implementation、Data Quality、Verification、Git、remote、Docker、lifecycle、runtime-loaded 或 production authority。

证据边界：

~~~
RE-REVIEWED
WRITTEN
NOT REPAIRED
NOT IMPLEMENTED
NOT TESTED
NOT STAGED
NOT COMMITTED
NOT PUSHED
NO FRESH REMOTE OBSERVATION
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED
~~~

## 2. Scope、读取边界与执行限制

本轮只复核：R42 consolidated Architecture contract、R41 B1–B3 blockers、current source identity、future exact implementation/test allowlist、focused test matrix、gate separation 与 MVP alignment。

按 Prompt 指定顺序读取了：

~~~
docs/thread_handoff/pm_operating_rules.md
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/chatgpt_pm_handoff_260730-0834.md
docs/reports/sprint4_d2_r7b_i1_r31_package_closed_collector_image_materialization_deployment_plan.md
docs/reports/sprint4_d2_r7b_i1_r35_phase5_post_activation_validation.md
docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/local_prerequisite_terminal.json
docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/post_activation_terminal.json
docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/manifest.sha256
docs/reports/sprint4_d2_r7b_i1_r36_working_tree_hygiene_authority_materialization_plan.md
docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/authority_materialization_plan.json
docs/reports/sprint4_d2_r7b_i1_r40_process_bound_runtime_loaded_observability_plan.md
docs/reports/sprint4_d2_r7b_i1_r41_process_bound_runtime_loaded_observability_reliability_review.md
docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md
collector/app/main.py
collector/app/config.py
collector/app/services/event_collector.py
collector/app/services/resolved_config_registry.py
collector/app/plc/mapping.py
collector/app/plc/read_plan.py
collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py
tests/test_collector_station_event_runtime_source.py
tests/test_collector_container_packaging.py
collector/Dockerfile
docker-compose.yml
config/mapping.yaml
~~~

本轮仅执行 read-only Git/path/hash/content inspection。没有执行 pytest、compileall、application process、Collector construction/start、Docker/Compose、network/SSH、remote filesystem、DB/API/PLC/V-PLC，也没有生成 production event、synthetic accepted fact 或 ACK/read_done activity。

没有处理、遍历评审、删除、移动或重新分类 Batch D/E；没有修改 R40、R41、R42、source、test、config、Dockerfile、Compose、status、roadmap、handoff 或 PM rules。

## 3. Fresh Git recovery 与 authority baseline

在本报告首次写入前执行了 live recovery。结果：

| Field | Live fact |
| --- | --- |
| repository root | /Users/chenjie/Documents/MES/edge-mes-demo |
| branch | main |
| HEAD | ce22ca71eff0548aa064129c160f7041603855e7 |
| origin/main | ce22ca71eff0548aa064129c160f7041603855e7 |
| HEAD^ | 35c50b1eb0f76d8b3361e8c122448ad03899559b |
| ahead / behind | 0 / 0 |
| tracked dirty | empty |
| cached | empty |
| git diff --check | PASS |
| git diff --cached --check | PASS |
| initial untracked count | 304 |

Prompt expected baseline 与 live baseline 完全一致。没有 baseline drift，因此没有触发 HOLD，也没有使用 mutation 恢复 baseline。

R36 authority materialization JSON 的 batch facts 为：Batch D historical manual review 300，Batch E frontend/next-env.d.ts 1。当前 untracked set 与 Batch D + Batch E + R40 + R41 + R42 exact expected set 比较：

~~~
unknown paths: 0
missing expected paths: 0
initial composition: 300 + 1 + 1 + 1 + 1 = 304
~~~

## 4. R40 / R41 / R42 输入身份复核

### 4.1 R40

| Field | Value |
| --- | --- |
| path | docs/reports/sprint4_d2_r7b_i1_r40_process_bound_runtime_loaded_observability_plan.md |
| bytes | 23337 |
| SHA-256 | 280cb553f5fc8bf81c92e689493782749534293de4876a05d88063080caabb91 |
| file identity | UTF-8 regular file / NON-SYMLINK |
| index state | UNSTAGED / UNTRACKED / NOT COMMITTED |
| authority state | WRITTEN / PM-REVIEWED / PM-VERIFIED / historical planning input / not final contract |

### 4.2 R41

| Field | Value |
| --- | --- |
| path | docs/reports/sprint4_d2_r7b_i1_r41_process_bound_runtime_loaded_observability_reliability_review.md |
| bytes | 25111 |
| SHA-256 | 6dc2c7a11ea2e6c4723bda69ed270b2e9a6cb7e3f4f75d13673599640adb5bb1 |
| file identity | UTF-8 regular file / NON-SYMLINK |
| index state | UNSTAGED / UNTRACKED / NOT COMMITTED |
| authority state | REVIEWED / WRITTEN / PM-REVIEWED / PM-VERIFIED / HOLD ACCEPTED |

### 4.3 R42

| Field | Value |
| --- | --- |
| path | docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md |
| bytes | 32319 |
| SHA-256 | dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165 |
| file identity | UTF-8 regular file / NON-SYMLINK |
| index state | UNSTAGED / UNTRACKED / NOT COMMITTED |
| authority state | REPAIRED CONTRACT WRITTEN / PM-REVIEWED / PM-VERIFIED / accepted as R43 input / not Reliability-accepted before this review |

R40、R41、R42 均是 PM-verified uncommitted inputs；本报告不将其表示为 committed authority、Git authority、implementation authority 或 runtime evidence。

## 5. Prior accepted boundary 与 historical evidence

R35 report 及其 exact evidence 只作为历史 accepted evidence 读取：

~~~
R35 report bytes/SHA:
3002 / 133c303e6a556b4be9e2c9535a10ff3b5a9dd06bf5b6f3fca1f272d707b75ee0

local_prerequisite_terminal.json:
52496 / 41c28d5c22e9c934c4edfeea0b07a1a84ec893b2ce9918d2bb17f2808afc7ce7

post_activation_terminal.json:
72307 / 135e66854fc032ceddc81ce6fa0cf28b51c90efd081f7f6c15e9e9299295e618

R35 evidence boundary:
ACTIVATED = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED = NO
PRODUCTION-ACCEPTED = NO
~~~

R35 static/container probe、isolated process、manual worker construction 和 static mapping check 均不能代表 active Collector main process 的 process-bound runtime-loaded evidence。本轮没有刷新或声称任何 remote/container/process/log fact。

旧 current_status.md / roadmap.md 中的 activation-pending 或 historical next-gate 文本不重开已关闭 gate；当前解释以 live Git、current Prompt、PM handoff、R35/R36 durable evidence、R40/R41/R42 exact inputs 为准。

## 6. Current source identity table

以下 identity 来自本轮 live worktree bytes，并用 git hash-object 与 HEAD:<path> 对比；所有列出的 path 均 CLEAN、regular、NON-SYMLINK。Git blob hash 与 SHA-256 不混用。

| Path | Bytes | SHA-256 | HEAD relation |
| --- | ---: | --- | --- |
| collector/app/main.py | 2073 | a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090 | CLEAN |
| collector/app/config.py | 764 | 4f01689a34fb494f7ea84cf74b303ce8aed0957d1dd9c05fc7773563cd577afc | CLEAN |
| collector/app/services/event_collector.py | 16342 | eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f | CLEAN |
| collector/app/services/resolved_config_registry.py | 17337 | 1844449a3f99e9ca53bddc8063c151fb0f889920597bccb170f5e62f3715db2c | CLEAN |
| collector/app/plc/mapping.py | 17433 | c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098 | CLEAN |
| collector/app/plc/read_plan.py | 1482 | fd5f675501444ed8378d6a296c3ed3d8769af97a1f19d1e95f3c00d76d4b02d6 | CLEAN |
| collector/tests/test_event_collector_reliability.py | 12774 | 462656c9d9146e492b52296ca2b40a1f37fe40cba95a2068e4c6317fd33c2472 | CLEAN |
| collector/tests/test_snap7_reliability_integration.py | 8025 | 5cc75a9cd37eeee6f3a80e29d186b55b3aab3a335898d77e204a9d653f686b54 | CLEAN |
| tests/test_collector_station_event_runtime_source.py | 30571 | 7d9d894eaa784e36c729e824ee87de73a863765089fd12e388bc926164229fd7 | CLEAN |
| tests/test_collector_container_packaging.py | 941 | 351e80a76a53f742258e91196b109172de7b43dc3fa359e63ef44c9e7ad9c26e | CLEAN |
| collector/Dockerfile | 218 | e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839 | CLEAN |
| docker-compose.yml | 5698 | c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66 | CLEAN |
| config/mapping.yaml | 7112 | d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d | CLEAN |

关键 current-source facts：

1. app.main.main() 当前先完成 config/source/storage/detector construction，再构造 EventCollectorWorker、创建并启动 daemon thread；worker loop 的 PLC/DB/ACK 行为在 constructor 之后。
2. EventCollectorWorker.__init__() 当前在 build_read_plans() 后直接做 dict-by-scope conversion，且当前没有 success record；这正是 future R42 implementation 的修复边界。
3. load_edge_mapping() 当前通过 text read 进入 YAML parse，尚未把 raw byte SHA 与同一次 decode/parse 绑定；R42 已将该改变严格限定到 mapping.py。
4. build_read_plans() 与现有 mapping source 足以被 worker 在 dict conversion 前审查；不需要修改 read_plan.py、mapping content、PLC、DB 或 ACK/read_done surface。

## 7. R42 self-contained consolidated contract assessment

结论：YES / SELF-CONTAINED。

R42 独立重述了后续 implementer/reviewer 所需的合同，而非要求隐式拼接 R40/R41。覆盖内容如下：

| Required contract element | R42 location | Assessment |
| --- | --- | --- |
| process-bound claim | §§6–7 | complete |
| exact emission point | §7.2 | complete |
| B1 duplicate/cardinality/scope | §8 | complete |
| B2 startup context/provenance/uniqueness/timestamp | §7.1, §7.3, §9 | complete |
| B3 log grammar/parser boundary | §10 | complete |
| exact record fields/key set | §§9.3, 11 | complete |
| same-byte mapping identity | §12 | complete |
| source/test allowlists | §§13–14 | complete |
| focused test matrix | §15 | complete |
| later validation contract | §16 | complete |
| non-claims/gate separation | §§16–18 | complete |

R40/R41 只用于历史来源核验。R42 本身已冻结 Candidate A、record authority、failure absence、external provenance split、future paths 与 next-gate sequence；未来实现无需依赖 R40/R41 的未重述细节。

## 8. R41 B1–B3 closure matrix

| Blocker | R42 repair closure | Reliability result |
| --- | --- | --- |
| B1 duplicate/cardinality/scope false PASS | list-first capture、reserved-scope rejection、duplicate-before-dict、count/set/multiset/one-to-one checks、disabled station required-scope preservation | CLOSED |
| B2 process provenance/uniqueness/field conflict | mandatory single-use startup context、PID/time application assertions、fresh external container/process/log authority、exactly-one scope、timestamp rename/relations、exact field classification | CLOSED |
| B3 parser-boundary false PASS | exact application literal、single JSON payload、deterministic serialization、strict rejection matrix、logger/serialization propagation、no fallback/retry | CLOSED |

## 9. B1 duplicate/cardinality/scope assessment

R42 §8 明确要求在 dict conversion 前保留并验证：

~~~
configured_station_ids
expected_scopes = ["line"] + configured_station_ids
generated_scopes = [plan.scope for plan in build_read_plans(mapping)]
~~~

在 success emission 前 fail closed 的条件全部列明：

~~~
missing line plan
configured station ID == reserved scope "line"
duplicate configured station IDs
duplicate generated plan scopes
generated count != expected count
missing expected scope
unexpected generated scope
expected/generated set or multiset mismatch
station runtime not one-to-one with configured stations
materialized station runtime count mismatch
post-conversion dict length != expected scope count
~~~

该顺序保证 duplicate station ID 与 duplicate generated scope 在 dict overwrite 之前可见；只有检查全部通过后才允许建立 dict、line plan 与 station runtimes。disabled configured stations 继续属于 required scope set，R42 没有改变现有 runtime product semantics。

独立可实现性判断：YES。event_collector.py 可在现有 build_read_plans() 返回 list 后完成全部检查；不需修改 read_plan.py、config/mapping.yaml、PLC、DB、ACK/read_done 或 production behavior。两条 allowed test paths 可覆盖每个 failure case。

结论：B1 CLOSED / NO CREDIBLE FALSE-PASS BLOCKER。

## 10. B2 startup-context、PID、provenance 与 uniqueness assessment

R42 冻结的 startup context contract：

~~~
created at first executable boundary of app.main.main()
mandatory and no default
at least collector_main_started_at_utc and process_pid
process_pid == os.getpid() at constructor/emission
single-use consumption
missing/repeated/reused/foreign-PID context fails closed
passed only to exactly one worker on this main startup path
not cryptographic and not external/container identity authority
~~~

该语义足以约束 future implementation/test 的 authority-bearing outcome：任何 context 缺失、重复消费、reused 或 PID mismatch 都不能产生 valid record；普通实现选择（例如 context object 的不可变字段、内部 consumed flag 或专用 consume method）不改变 PASS/HOLD 结果，不构成 blocker。R42 test matrix 明确覆盖 absent/reused/foreign-PID、duplicate worker、manual/probe caller、os.getpid() mismatch 与 Thread.start() failure。

Exactly-one scope 已明确为：

~~~
exactly one valid success record
per invocation of app.main.main()
for the current active Collector Python process
~~~

它不是 per-worker、per-poll/retry、per-log-stream；container restart 是新的 boundary；同一 active container/start boundary 中 zero、two or more matching records 均为 HOLD；repeated main() 是新的 main-entry boundary，但同一 active boundary 不接受第二条。startup failure 或未形成有效 worker path 不被当作 PASS 的 zero-record success。

Application assertion 与 external terminal provenance 严格拆开：

~~~
application: collector_main_started_at_utc, process_pid, mapping/plan fields
external: full active container ID, full active image ID, fresh StartedAt,
          active Collector main PID/process identity, current container-scoped log envelope,
          bounded observation timestamp
~~~

后续 validator 必须拒绝 stale prior-start、other-container、manual/probe、foreign PID、active process absent/ambiguous、Thread.start() failure 后遗留 record，以及 duplicate/ambiguous/malformed/missing records；不能把 worker health、PLC、DB、persistence、ACK/read_done 或 production fact 添加进本 record claim。

结论：B2 CLOSED / SUFFICIENTLY SPECIFIC / NO CREDIBLE FALSE-PASS BLOCKER。

## 11. Timestamp semantics assessment

R42 已将 R40 的 process_started_at_utc 改为：

~~~
collector_main_started_at_utc
~~~

其含义明确为 Python app.main.main() entry timestamp，而非 OS process birth。输出必须为 RFC3339 UTC、Z 形式；malformed、non-UTC、impossible ordering 或无法建立时钟关系时不得 PASS。

后续 validation 的最小关系已冻结：

~~~
fresh container StartedAt
<= collector_main_started_at_utc
<= bounded observation time
~~~

没有发明毫秒 tolerance，也没有扩展成 clock synchronization subsystem。结论：CLOSED。

## 12. Application fields、external authority 与 exact v1 key set

R42 v1 application record 的 terminal fields：

~~~
evidence_schema_version
event_type
mapping_path
mapping_content_sha256
mapping_schema_version
config_version
line_id
read_plan_count
resolved_config_hash
~~~

Correlation application fields：

~~~
collector_main_started_at_utc
process_pid
~~~

R42 消除了 R40 对 process_pid 的 required/diagnostic classification 冲突；v1 exact key set 禁止 missing 与 extra fields。record_emitted_at、sorted scope list 以及其他 diagnostic fields 不进入 v1，也不能成为 PASS authority。

mapping_content_sha256 是 exact raw mapping-file byte identity；resolved_config_hash 是 validated semantic/resolved identity。R42 没有新增第二个 semantic hash，也没有把 external container/image/process facts 混入 application JSON。record 不含 secret、DSN、credentials、host/port、raw PLC bytes、production payload、event/DB result、ACK/read_done 或 production fact。

结论：FIELD AUTHORITY CLOSED。

## 13. B3 deterministic logging grammar 与 strict parser assessment

唯一 application-message grammar：

~~~
collector_runtime_loaded_json=<JSON_OBJECT>
~~~

serialization contract 已固定：

~~~
exact v1 key set
sort_keys=True
compact separators
allow_nan=False
UTF-8
one line
no CR/LF
no sensitive/raw/production fields
~~~

R42 清楚区分 logging formatter 的 timestamp/level prefix 与 application message。Parser 的输入边界是 application-message component，而不是任意 raw log substring；该 component 必须以 exact literal 开头，literal 后的全部剩余内容是唯一 JSON payload。

Parser 必须拒绝：

~~~
arbitrary substring match
extra suffix
multiple delimiter
partial/truncated JSON
non-object JSON
missing key
extra key
wrong schema
wrong event type
malformed/ambiguous/missing/duplicate matching records
zero or two-or-more matching records
~~~

因此 logging-prefix 之外的 application-message extraction 已足够确定：未来 parser 只能在已经确定的 application-message boundary 上做 exact-start/full-payload parse，不得通过 find/substring 命中任意日志文本。formatter prefix 的具体时间格式不成为 application authority，也无需新增 logging framework、storage、telemetry、heartbeat 或 retention system。

serialization failure 与 logger invocation failure 必须传播；无 fallback、retry、substitute success、poll-loop 或 delayed replay。handler buffering、log loss、rotation、missing collection 只产生 evidence unavailable/HOLD。

结论：B3 CLOSED / NO PARSER FALSE-PASS BLOCKER。

## 14. Exact emission point 与 side-effect boundary

R42 要求 success emission 是 worker constructor 的最后一个 required action，并且位于以下全部成功之后：

~~~
same-byte mapping read/hash/decode/parse
mapping contract validation
PLC/line/rack/slot/timezone derivation
resolved snapshot construction and hash consistency
registry construction
Snap7 client object construction
complete read-plan list construction
B1 duplicate/cardinality/scope validation
line plan materialization
one-to-one station runtime materialization
startup-context PID/single-use validation
deterministic serialization
~~~

它发生在 constructor return、Thread.start()、run_forever、PLC connect/read/write、DB query/write/transaction、accepted-fact generation 和 ACK/read_done 之前；emission 后不允许还有会使 constructor 失败的 required action。

R42 对现有 Storage(dsn) wrapper construction 保持窄声明：不把 wrapper construction 宣称为已发生 DB query/write。该处理没有扩大 claim，也没有改变 PLC、DB、accepted-fact、ACK/read_done 或 disabled-station semantics。

结论：EMISSION ORDER CLOSED。

## 15. Same-byte raw mapping identity

R42 §12 冻结 exact path 的单次 raw-byte lineage：

~~~
read exact raw bytes once
hash those exact bytes
explicit UTF-8 decode those exact bytes
parse the decoded content
bind raw identity to the parsed EdgeMapping
~~~

明确禁止 second read、text re-encoding hash、newline normalization hash、substituted path authority；read/decode/parse/semantic/resolved-hash failure 不产生 success record。

该 contract 可由 collector/app/plc/mapping.py 单独承载，同时保留 direct parse_edge_mapping() caller compatibility，不改变 mapping semantics、配置内容、disabled-station behavior 或 existing caller behavior。mapping_content_sha256 与 resolved_config_hash 互补而非两个 semantic authorities。

结论：RAW IDENTITY CLOSED。

## 16. Future exact implementation allowlist review

### 16.1 Source allowlist

| Path | Necessary | Sufficient | Exact responsibility | Missing path | Expansion risk |
| --- | --- | --- | --- | --- | --- |
| collector/app/main.py | yes | yes with the other two | first-boundary context creation and exactly-one worker handoff | none | lifecycle/config/endpoint expansion |
| collector/app/services/event_collector.py | yes | yes with the other two | context consume/PID check, B1 validation, v1 serialization/emission, no post-emission required action | none | PLC/DB/polling/ACK changes |
| collector/app/plc/mapping.py | yes | yes for raw-byte binding | one-read hash/decode/parse identity and compatible mapping exposure | none | mapping semantic/caller change |

Independent result：three-source allowlist NECESSARY / SUFFICIENT。config.py、resolved_config_registry.py、read_plan.py、storage.py、Dockerfile、Compose、mapping content、Snap7 integration、API、DB schema、Dashboard、V-PLC、production、ACK/read_done surface 均无需加入。没有 credible missing source path。

### 16.2 Test allowlist

| Path | Necessary | Sufficient | Exact responsibility | Missing path | Expansion risk |
| --- | --- | --- | --- | --- | --- |
| collector/tests/test_event_collector_reliability.py | yes | yes with the other test | constructor context/one-shot/no-I-O/logging/emission-order/side-effect tests and existing persistence/ACK semantics regression | none | integration/runtime execution expansion |
| tests/test_collector_station_event_runtime_source.py | yes | yes with the other test | same-byte mapping identity, decode/parse/hash failures, duplicate/scope fixtures and static/manual evidence boundary | none | new generic runtime harness |

Independent result：two-test allowlist NECESSARY / SUFFICIENT。collector/tests/test_snap7_reliability_integration.py 与 tests/test_collector_container_packaging.py 本轮仅作为指定输入审查，不需要被 future R42 implementation 修改或纳入 allowlist。若未来发现额外 source/test path 不可避免，必须另行 PM decision；本 review 不授权扩展。

## 17. Future focused test matrix sufficiency review

R42 §15 覆盖了本轮要求的全部 credible false-PASS 面：

| Required case | Covered by R42 |
| --- | --- |
| absent/reused/foreign-PID context | yes |
| duplicate worker / duplicate record | yes |
| duplicate station ID / duplicate scope | yes |
| reserved line collision | yes |
| missing/extra/count mismatch | yes |
| same-byte one-read identity | yes |
| invalid UTF-8 | yes |
| parse/semantic/resolved-hash failure | yes |
| exact one-line JSON | yes |
| strict parser malformed/substring/extra rejection | yes |
| logger/serialization exception | yes |
| final-action ordering | yes |
| no PLC/DB/accepted-fact/ACK side effects | yes |
| existing persistence and ACK/read_done semantics | yes |
| static/manual evidence cannot become runtime evidence | yes |

两条 test path 的职责边界可以承载该 matrix，不需要执行 application loop、PLC、DB、accepted-fact、ACK/read_done 或 production flow。本轮没有执行 tests；上述结论是 test-contract sufficiency review，不是 test PASS。

结论：TEST MATRIX SUFFICIENT / NOT EXECUTED。

## 18. New credible blocker assessment

本轮未发现符合 blocker 门槛的新问题。

| Candidate finding | Decision | Reason |
| --- | --- | --- |
| generic telemetry/log retention | not blocker | 不影响当前 exact record 的 false-PASS/HOLD claim；缺失只 HOLD |
| cryptographic startup token / hostile same-process forgery | out of scope | R42 明确不作此 claim；external fresh facts 负责 terminal provenance |
| clock synchronization subsystem | out of scope | R42 只要求无法建立时间关系时 HOLD |
| API/status endpoint/DB persistence/generic registry | out of scope | Candidate A 的最小 logging channel 已足够 |
| optional diagnostic fields | backlog only | 不进入 v1 authority，不能改变 PASS/HOLD |
| current disabled event-collector configuration or startup failure | not a false PASS | no valid record is accepted as success; zero matching record is HOLD |

Blockers：none。

## 19. Bounded non-blocking recommendations

NON_BLOCKING_RECOMMENDATIONS_PRESENT。

1. Future implementation test 可额外把“首次 context consumer 在任意 constructor failure 后仍不可被 retry/reuse”作为单独 assertion，以便把 single-use 的失败路径也固定成 monotonic fail-closed；该建议不改变 R42 的 current PASS 结论、不扩展 source/test allowlist，也不引入新 authority。
2. Future runtime validator 应保持 raw container-log transport adapter 与 application-message parser 的接口分离，并记录 parser 接收到的是完整 application-message component；这只是实现可审查性要求，不改变 R42 v1 fields 或增加 logging infrastructure。

上述建议不是 current-gate blocker，不得由 PM 自动升级为额外 repair 或 allowlist expansion。

## 20. MVP alignment assessment

~~~
MVP-ALIGNED WITH BACKLOG ITEMS
~~~

approved MVP deliverable：为已批准的 Collector runtime-loaded mapping/config identity claim 建立最小、可独立验证的 process-bound success-record contract。

minimum invariant：required mapping/resolved/read-plan initialization 成功后才可能产生一条 deterministic record；record 必须能与 fresh active process/container/start/log boundary 相关联；失败、缺失、重复、stale、foreign 或 malformed evidence 均不得 PASS。

本轮没有新增产品能力、threat model、API、DB persistence、telemetry、heartbeat、audit/forensics、retention model、runtime topology、PLC/DB/ACK/read_done semantics 或 disabled-station semantics。审查复杂度仍服务于具体 false-PASS 与 evidence-boundary 风险，没有替代产品交付。

## 21. Changed-path / forbidden-action audit

本轮唯一 task-owned changed path：

~~~
docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md
~~~

明确未修改：

~~~
R40 report
R41 report
R42 report
任何 source/test/config/Dockerfile/Compose
current_status.md
roadmap.md
chatgpt_pm_handoff_260730-0834.md
pm_operating_rules.md
Batch D/E
~~~

明确未执行：

~~~
pytest / compileall / application process
Collector construction/start
Docker/Compose/network/SSH/remote filesystem
DB/API/PLC/V-PLC
production event / synthetic accepted fact
ACK/read_done
git add / stage / commit / push / tag
restore/reset/stash/clean/delete/move/archive
~~~

## 22. Final Git/index/untracked audit

本报告写入后必须保持并由 final read-only audit 验证：

~~~
HEAD == origin/main == ce22ca71eff0548aa064129c160f7041603855e7
HEAD^ == 35c50b1eb0f76d8b3361e8c122448ad03899559b
ahead / behind == 0 / 0
tracked dirty == empty
cached == empty
initial untracked == 304
final untracked == 305
final composition == Batch D 300 + Batch E 1 + R40 1 + R41 1 + R42 1 + R43 1
unknown paths == 0
~~~

R43 输出在首次写入前已确认 ABSENT / NON-SYMLINK / UNSTAGED / UNTRACKED。此报告写入是唯一 mutation；没有 stage、commit、push 或其他 mutation。

## 23. R43 report identity

R43 是 regular UTF-8 non-symlink file，final bytes 与 SHA-256 由写入完成后的同一 final read-only audit 测量，并在本任务 Chat concise manifest 中返回。由于一个文件不能在不改变自身 bytes 的情况下嵌入自身最终 SHA-256，本节采用 PM durable-report 的 detached final identity 规则；Chat manifest 的 bytes/SHA 是本报告的 final identity，而非第二个 artifact。

~~~
path: docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md
encoding: UTF-8
file type: regular
symlink: NO / NON-SYMLINK
index: UNSTAGED / UNTRACKED
final bytes: detached final audit in Chat manifest
final SHA-256: detached final audit in Chat manifest
~~~

## 24. Terminal next gate

~~~
R43 Reliability re-review WRITTEN
→ ChatGPT PM durable intake only
→ PM may accept R42 as candidate contract superseding R40
→ PM may separately issue Data Quality planning review
~~~

本轮不自动触发 Data Quality、Verification、implementation、Git closeout、deployment、lifecycle、runtime-loaded validation、RUNTIME-LOADED acceptance 或 production accepted-fact work。R43 PASS、R42 repair 与本报告 recommendations 均不推断后续 authority。

## 25. Thread context assessment

~~~
output length: long durable review
continue current Thread: no
new Thread recommended: yes
reason: independent Reliability authority is terminalized; PM durable intake must occur before any separately authorized Data Quality/Verification/implementation gate
~~~

完成本报告与 final audit 后立即停止。
