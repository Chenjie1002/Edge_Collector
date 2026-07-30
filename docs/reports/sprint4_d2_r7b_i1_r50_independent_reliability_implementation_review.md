# Sprint 4 D2-R7B-I1 R50 Independent Reliability Implementation Review

## 1. 报告身份、任务与 authority

- 报告名称：Sprint 4 D2-R7B-I1 R50 Independent Reliability Implementation Review
- 任务名称：D2-R7B-I1 R50 — Independently Review Runtime-Loaded Observability Implementation After R49
- 执行 Thread：Reliability
- Authority source / ID：PM-D2-R7B-I1-R50-INDEPENDENT-RELIABILITY-IMPLEMENTATION-REVIEW-260730-1423
- Report delivery mode：REPOSITORY_DURABLE_REPORT
- Exact report path：docs/reports/sprint4_d2_r7b_i1_r50_independent_reliability_implementation_review.md
- Exact artifact paths：none
- Docs / artifact write authority：仅 exact R50 report path；第一次写入本报告时消费；不继承 R48/R49 implementation authority。

## 2. 结论

~~~text
PASS WITH RECOMMENDATIONS
~~~

当前 R48 + R49 persisted source/test package 满足 R42 + R45 Reliability implementation contract。没有发现当前 gate 的 Reliability blocker。R49 已关闭 R48 暴露的 pre-record Storage connection/order 风险，并且当前 focused tests 使用显式 Storage constructor-call/order oracle；本轮独立审查确认该修复未引入新的 DB、PLC、accepted-fact、ACK/read_done、retry/replay 或 constructor-order false PASS。

本结论只表示本地 source/test package 的独立 Reliability review result。它不表示：

~~~text
RUNTIME-LOADED = YES
PRODUCTION-ACCEPTED = YES
deployed process evidence
real DB evidence
real PLC evidence
active image/container evidence
Git stage/commit/push
build/deploy/remote/runtime validation
Data Quality review
Verification review
~~~

## 3. Authority、scope 与禁止边界

本轮只执行 Reliability review-only 工作：读取指定 contracts/reports/source/tests，执行只读 Git/path/hash/AST 检查，以及 Prompt 授权的一个 py_compile 和两个完整 focused pytest commands。未修改 source、tests、config、contracts、status、roadmap、handoff、R48/R49 report；未创建 helper、fixture、manifest、log、sidecar、evidence directory 或其他 artifact。R50 本报告是唯一 task-owned write。

R42 是 base implementation contract；R45 只 supersede canonical line_id/routing equality、later source/image/config/process binding、later raw-log/payload/parsed evidence identity。R43 是 accepted Reliability planning/re-review；R46 是 accepted focused Data Quality re-review；R47 是 accepted Verification planning review；R44 仅作为历史 Data Quality blocker origin，不覆盖 R45/R46。

## 4. 按要求读取的输入与身份

以下 expected identities 在 recovery 后对 live regular, readable, non-symlink files 重新计算；所有给定 bytes/SHA-256 均匹配。PM Rules/current status/R44 的 identity 也记录为 live observation；它们不改变 Prompt 给出的 expected identity gate。

| Input | Bytes | SHA-256 | File identity |
| --- | ---: | --- | --- |
| docs/thread_handoff/pm_operating_rules.md | 49170 | a692fdafbdea8c63d184cb11548e73731aefccd3110818004b028ba7ee9fe7f5 | regular / non-symlink / readable |
| docs/current_status.md | 150180 | ee7126fd20f1774f54cee9b238cab4e3e0943bce854402b1594060212f88cc23 | regular / non-symlink / readable |
| docs/thread_handoff/chatgpt_pm_handoff_260730-1203.md | 26183 | c9a7ed7283d4574578e1608fc6891bdb91373d97bac3191740863917af3ad8e1 | regular / non-symlink / readable |
| R42 docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md | 32319 | dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165 | regular / non-symlink / readable |
| R45 docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md | 13786 | 8fd646f24565bbcb27aa9063038774fee3b5398d66566f961bee296ffff02ef2 | regular / non-symlink / readable |
| R43 docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md | 30244 | 95b2e63c4879fb5af6920b262300566c577612dd1753b13bf59928c1417338e8 | regular / non-symlink / readable |
| R44 docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md | 43036 | 3b4d1f3451d0b0036e5530bc83eb35b90ee2b6d140b0a2799b82df1ada035bfa | regular / non-symlink / readable |
| R46 docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md | 23703 | f460fef43d975de41ed624fa49d8a1a8dcd5246b4ae55b222189f40703914b81 | regular / non-symlink / readable |
| R47 docs/reports/sprint4_d2_r7b_i1_r47_runtime_loaded_observability_verification_planning_review.md | 34592 | 4de247e350eb595077219856cf63b0319ee83d14026b6beaaf7c5d83211a0ae4 | regular / non-symlink / readable |
| R48 docs/reports/sprint4_d2_r7b_i1_r48_runtime_loaded_observability_implementation.md | 15692 | caa3203630c5b321c950d078fda7424f4f1ca8edcd7f4a45b88525adfdda0d10 | regular / non-symlink / readable |
| R49 docs/reports/sprint4_d2_r7b_i1_r49_pre_record_db_connection_ordering_repair.md | 11749 | 5d09732094f3266eccc34a002b0203a3889f33be1c6b56568c43b42c50618dde | regular / non-symlink / readable |
| collector/app/main.py | 2525 | d1a461294c91f9f86cde4af87b21bb1147bed5561d64028e8462a8f57d46de80 | regular / non-symlink / readable |
| collector/app/services/event_collector.py | 24313 | 02cab6ea15572ae0b2f6059462f9cd6856cd483ab0dcc37c87d39267aad1e8e2 | regular / non-symlink / readable |
| collector/app/plc/mapping.py | 18876 | ba39583a699f8347c0ff5eaec2e7c807dad909c815269de607a36e8b93c023a7 | regular / non-symlink / readable |
| collector/app/services/storage.py | 38319 | f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b | regular / non-symlink / readable |
| collector/tests/test_event_collector_reliability.py | 32253 | fa8a677f5a249b849438b7ec43e2bbd14ff14e8c590e54d02274daa640b06835 | regular / non-symlink / readable |
| tests/test_collector_station_event_runtime_source.py | 33212 | 7b5b77f40c5bc3eff1a364064876ed79d0d28ffa5bf5f25ee9ba279498d409cd | regular / non-symlink / readable |

## 5. Initial live Git recovery

Recovery 在任何 report write 前完成，使用 Prompt 要求的 read-only command set：

~~~text
repository root: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 4a733d7995a94398ade693822662ebd2b22f9d3d
origin/main: 4a733d7995a94398ade693822662ebd2b22f9d3d
ahead / behind: 0 / 0
cached: empty
tracked dirty:
  collector/app/main.py
  collector/app/plc/mapping.py
  collector/app/services/event_collector.py
  collector/tests/test_event_collector_reliability.py
  tests/test_collector_station_event_runtime_source.py
git diff --check: PASS
git diff --cached --check: PASS
R50 report before write: ABSENT
~~~

最近八条提交的首条为 4a733d7 (HEAD -> main, origin/main, origin/HEAD) Add PM handoff before runtime-loaded implementation；本轮没有使用 commit history 替代 live facts。

## 6. R42 + R45 final Reliability contract interpretation

本轮以以下 minimum terminal invariants 作为实现审查 oracle：

1. app.main.main() 在第一 executable boundary 创建一个 mandatory startup context，包含 main-entry RFC3339 UTC Z time 与 current os.getpid()。
2. Context 无默认值、只消费一次；missing/reused/foreign-PID/invalid context fail closed；constructor 后续 failure 不能使 context 可 retry/replay。
3. load_edge_mapping() 对 exact regular non-symlink path 只读 raw bytes 一次，hash 同一 bytes，显式 UTF-8 decode 同一 bytes，并把 raw identity 绑定到 parsed mapping。
4. Worker 在 dict conversion 前保留 configured_station_ids、expected_scopes、generated_scopes，拒绝 reserved line collision、duplicate、missing、extra、count/multiset/one-to-one mismatch。
5. Canonical record line_id 来自 hash-bound resolved snapshot；selected PLC line 是 routing projection，必须等于 canonical line 后才能 success。
6. Record 只有 exact 11-key v1 object，application grammar 为 collector_runtime_loaded_json=<JSON_OBJECT>，serialization deterministic、compact、single-line、fail-propagating。
7. Success emission 是 EventCollectorWorker.__init__() 最后一个 required action，早于 constructor return、Thread.start()、worker run_forever、PLC/DB/accepted-fact/ACK/read_done activity。
8. Worker constructor 不构造 Storage、 不连接 DB、PLC；run_forever() entry 才 exactly once 构造 Storage，然后 worker-start logging，再 first poll_once()。
9. Storage initialization failure propagates，不 retry、不 poll、不 re-emit runtime-loaded record。
10. Local source/tests/fakes 只建立 local implementation evidence，不建立 deployed process、real DB/PLC、active image/container、RUNTIME-LOADED 或 production truth。

R45 的 source/image/config/process binding 与 A–H raw evidence 是后续独立 runtime/Verification gate，不要求当前 application record 扩大字段或 allowlist。

## 7. R48 + R49 implementation package state distinction

| State | R48 | R49 | R50 result |
| --- | --- | --- | --- |
| source/test package | WRITTEN | WRITTEN、包含 pre-record DB ordering repair | independently reviewed; no blocker |
| local focused validation | R48 historical PASS | R49 historical py_compile + A/B PASS | freshly rerun and PASS |
| PM state | PM-ACCEPTED FOR INDEPENDENT REVIEW | PM-ACCEPTED repair input | R50 only reports review; no later authority |
| Reliability review | not established | not established before R50 | RELIABILITY-REVIEWED / WRITTEN after this report |
| Git | not staged/committed/pushed | not staged/committed/pushed | remains not staged/committed/pushed |
| build/deploy/runtime | not established | not established | remains not established |

R49 的 exact repair is visible in live diff: main.py moved legacy Storage(database_url()) after worker construction and Thread.start()；event_collector.py stores dsn and moves worker Storage(self.dsn) to run_forever() entry；Reliability test adds explicit constructor-call and ordered-event assertions。storage.py itself remains unchanged，其真实 connection boundary remains Storage.__init__() line 20 psycopg.connect(dsn, autocommit=False)。

## 8. Startup-context ownership、PID、single-use、failure consumption

### 8.1 Creation and handoff

collector/app/main.py:18-22 的 capture_startup_context() 生成 UTC Z timestamp 与 os.getpid()；main():25-26 在 load_config():27 前调用。main.py:35-40 只在 enabled event collector path 把这一 context 显式传给一个 EventCollectorWorker。

CollectorStartupContext 在 collector/app/services/event_collector.py:44-74 是 mandatory dataclass：worker signature :78-86 无默认 context；:87-89 拒绝错误类型并立即调用 consume()。

### 8.2 PID and single-use

consume():50-74 先检查 _consumed，然后在 :53 将其置为 True，再验证 string/Z/UTC、positive non-boolean integer 与 process_pid == os.getpid()。因此 invalid input、foreign PID、later mapping/PLC/plan/serialization failure 均消耗 context；重复 consumer 不会重新获得 capability。实现没有通过 environment/default 生成 context，也没有把 context 传给第二个 worker。

Context object 不是 cryptographic token，也不声称抵抗任意同进程手工伪造；这与 R42/R45 的 explicit non-claim 一致。当前 gate 要求的是 main-created mandatory handoff、PID binding、single-use 和 fail-closed consumption，而不是 generic anti-forgery subsystem。

### 8.3 Failure consumption / non-replay

collector/tests/test_event_collector_reliability.py:582-594 明确验证：第一次 consumer 在 canonical-line constructor failure 后，第二次使用同一 context 仍失败；:565-580 覆盖 missing/foreign-PID/reused。该测试关闭了 R43/R46/R47 carry-forward 的“first consumer remains consumed after later constructor failure”风险。

结论：startup context contract PASS；无当前 Reliability blocker。

## 9. Exact-one record、serialization、logger failure 与 replay

event_collector.py:193-218 构造一个 v1 record，含 exact 11 keys；:209-215 使用 ensure_ascii=False、sort_keys=True、compact separators 与 allow_nan=False；:216-217 拒绝 CR/LF；:218 只调用一次 logger.info，application message 以 exact collector_runtime_loaded_json= 开头。

event_collector.py:196-207 的字段来源分离为 raw byte SHA、mapping/resolved projection、validated plan count、main-entry timestamp/PID；没有 DSN、credential、PLC payload、accepted fact、ACK/read_done 或 production fields。json.dumps failure 与 logger failure 没有被 catch；不会 fallback、retry、delayed replay 或 substitute success。

test_event_collector_reliability.py:391-440 观察一次 logger call、exact key set、literal、compact deterministic reserialization、integer/non-boolean PID/count、lowercase 64-hex hashes与禁用字段；:596-608 观察 serialization/logger exception propagation 与 zero Storage constructor calls。

结论：exact-one/deterministic/fail-propagating/no-retry contract PASS。 本地 logger spy 不等同于 container log evidence；后续 A–H gate 仍需独立 raw transport/payload lineage。

## 10. Constructor-last-action analysis

EventCollectorWorker.__init__() 的 required action sequence 为：

~~~text
event_collector.py:89  consume mandatory context
event_collector.py:93  load exact mapping
event_collector.py:94  validate raw/resolved/hash/projection identity
event_collector.py:95-110 validate one PLC, canonical/routing line, rack/slot/timezone
event_collector.py:111-118 build and verify resolved registry lookup
event_collector.py:119 construct Snap7 client object only
event_collector.py:120-129 build/validate plans and materialize runtimes
event_collector.py:130 emit unique record
event_collector.py:131 constructor return
~~~

event_collector.py:130 是最后一个 required constructor action；其后只有 Python function return，没有可能失败的 product-required action。snap7.client.Client() 是 object construction，不是 connect/read/write；Storage 不在 constructor call graph。

## 11. Main ordering：context → non-DB setup → record → Thread → legacy Storage

main.py:25-47 的 enabled path 为：

~~~text
main.py:26       capture context
main.py:27-33    load config and construct non-DB source setup
main.py:35-40    EventCollectorWorker constructor; unique record is emitted inside it
main.py:41-45    construct/start event-collector Thread
main.py:47-48    construct legacy main-loop Storage and EventDetector
~~~

Snap7Source.__init__() 只在 collector/app/sources/snap7_source.py:45 构造 client object，connect/read 只在 read():52-56；SimulatorSource.__init__():8-10 只保存 URL，network read 在 read():11-14。因此 main 的 pre-record non-DB setup 没有 DB connection 或 PLC I/O。

Storage.__init__() 的真实 connection boundary 是 storage.py:18-20。main 的 legacy call 在 record/Thread.start 之后，满足 R49/R50 ordering；constructor failure 在 worker creation 阶段抛出时不会到达 legacy Storage（测试 :662-697）。

## 12. Worker constructor / run_forever / Storage / poll ordering

event_collector.py:77-130 中没有 Storage(...) call。AST read-only audit 对 __init__ 的 Storage call count 为 0；唯一 PLC-related constructor action 是 snap7.client.Client() object construction at :119。

run_forever():220-235 的顺序是：

~~~text
event_collector.py:221  self.storage = Storage(self.dsn) exactly once at entry
event_collector.py:222-227 worker-start logging
event_collector.py:228-235 loop; first poll_once at :230
~~~

Storage construction 在 loop/try block 外；因此 initialization exception 在 :221 直接 propagate，不会被 loop exception handler 捕获，也不会 retry、poll 或 re-emit record。正常运行时 first poll_once() 才在 :230 进入 PLC connect/read and DB/accepted-fact/ACK paths。

## 13. Storage initialization failure propagation

storage.py:18-20 证明 Storage(...) 本身可能进行真实 DB connection。R49 将 worker call 移到 run_forever():221，并保留 self.dsn at constructor :90。没有 try/except、retry、fallback 或 second record path 包围这次 initialization。

test_event_collector_reliability.py:724-744 使用 failing Storage factory：观察恰好一次 storage_construct、异常原样传播、runtime-loaded message list 为 empty；同时 constructor exact-one test :391-440 已证明 record 只在 constructor success path 发出一次。该组合能检测 premature constructor Storage、re-emission 与 failure swallowing，且不会把 FakeStorage 的 events/writes 当作 constructor-call evidence。

结论：Storage failure contract PASS；不进入 poll loop、不 retry、不重新发出 record。

## 14. PLC、DB、accepted-fact、ACK/read_done side-effect matrix

| Path | DB connection/query/write | PLC connect/read/write | accepted fact | ACK/read_done | R50 ruling |
| --- | --- | --- | --- | --- | --- |
| successful worker constructor before record | none; no Storage object | only snap7.client.Client() object construction; no connect/read/write | none | none | PASS |
| mapping/context/plan/canonical/logger/serialization failure before record | none | no I/O before failure point | none | none | PASS |
| enabled main before record | no legacy Storage until main.py:47, after Thread.start/record | source constructors are object/file setup only | none | none | PASS |
| worker Storage initialization failure after record | one attempted Storage constructor at run entry; real DB call may fail there | no poll/PLC activity | none | none | PASS |
| first poll_once() and later station processing | existing Storage/PLC/accepted-fact/ACK behavior begins here | existing behavior begins here | existing build_accepted_station_event_fact/transaction path at event_collector.py:356-372 | existing mark_cycle_ack_* and PLC db_write at :392-426 | outside pre-record claim; unchanged |

Existing side-effect ownership remains after runtime-loaded record: _process_station() writes runtime status at event_collector.py:272-287, accepted fact/transaction at :356-372, and ACK/read_done branches at :392-426; these are not reachable from constructor before record. No source change touched storage.py.

## 15. Canonical line、routing equality 与 list-first read-plan

event_collector.py:100-107 selects exactly one PLC entry, requires non-empty routing line_id and compares it to self.resolved_config_snapshot.line_id before any record. _emit_runtime_loaded_record():203 writes the resolved snapshot line, not an unchecked PLC projection. This is the R45 canonical line rule；first-PLC behavior remains unchanged and no multi-PLC feature was added.

event_collector.py:174-191 preserves list-first values before dict conversion：

~~~text
configured_station_ids = [station.station_id ...]
expected_scopes = ["line", *configured_station_ids]
generated_scopes = [plan.scope ...]
~~~

It rejects reserved line collision, duplicate station IDs, duplicate generated scopes, count mismatch, exact scope multiset mismatch, missing/extra scopes, non-one-line scope and non-positive plan list. Only after this validation does :122 create plans dict and :123-129 materialize line/station runtimes. Disabled configured stations remain included because all mapping stations are used in expected scopes and runtime materialization.

Focused cases are at test_event_collector_reliability.py:441-495 and :545-563；all passed。

结论：canonical-line、routing equality、scope/cardinality/list-first invariants PASS。

## 16. Mapping raw-byte identity 与 resolved semantic identity

mapping.py:143-160 resolves the exact path, rejects exact-path symlink/non-regular file, performs one read_bytes() at :150，hashes those exact bytes at :151，decodes those same bytes at :152，parses the decoded text at :153，and binds path/raw SHA to the parsed EdgeMapping at :156-160。没有 second read、text re-encode hash 或 newline normalization hash。

mapping.py:242-260 creates the runtime snapshot and computes semantic config_hash；:282-290 uses deterministic semantic content serialization. mapping_content_sha256 remains raw-byte identity；resolved_config_hash remains semantic/resolved identity。tests/test_collector_station_event_runtime_source.py:159-185 observes one raw read、one YAML load、same decoded text、raw SHA；:187-199 verifies raw-byte change gives different raw SHA while semantic hash remains stable；:201-218 and :255-315 cover decode/YAML/registry failure paths.

结论：same-byte/raw-vs-semantic separation PASS。These local tests do not establish active container-visible mapping evidence；该 evidence 仍属于 later R45/R47 runtime gate。

## 17. Focused test oracle assessment

### 17.1 Reliability focused file

test_event_collector_reliability.py:358-389 的 construct_worker() 显式 patch event_collector_module.Storage，由 storage_factory 记录每一次 constructor invocation；成功 constructor 断言 storage_constructor_calls == [] at :391-396。这不是只看 FakeStorage 的 events/writes，因此能检测 constructor-time Storage(...)/DB connection false PASS。

test_event_collector_reliability.py:610-660 用 ordered events 观察 record → thread_construct → thread_start → legacy_storage_construct；:662-697 覆盖 worker constructor failure 时无 Thread.start、无 legacy Storage；:699-722 覆盖 storage_construct → poll_once；:724-744 覆盖 Storage init failure propagation/no retry/no re-emission。

该文件还覆盖 exact record、serialization/logger failure、context PID/single-use/consumption、scope/line failure、no constructor PLC/DB/ACK/read_done side effects与 existing persistence/ACK/read_done regressions。Fake-based tests 的盲点是它们不建立 real DB/PLC/process evidence；这属于明确的 later gate boundary，不是当前实现 review 的 false PASS blocker。

### 17.2 Runtime-source focused file

tests/test_collector_station_event_runtime_source.py:159-185 显式观察 raw byte read count、YAML loader input 和 hash identity；:187-218、:246-315 覆盖 raw/semantic and parse/registry failure boundaries。其余 56-test file 保持 raw payload/normalized lineage and no production-evidence misclassification assertions。它不执行 product startup、real DB、PLC、network 或 remote operation。

### 17.3 False-PASS assessment

没有发现会让 fake-only test 在当前 source 已经 premature Storage construction 时仍然 PASS 的路径：worker constructor 的 exact Storage call spy 会失败；main ordering test 的 ordered legacy Storage event 会失败；run entry/failure tests 分别观察 storage-before-poll 与 no-retry/no-reemit。FakeClient 也没有提供 constructor connect 方法，若 constructor 越界调用 connect 会使 positive construction test 失败；当前 source AST 更直接确认 constructor 没有 PLC I/O call。

## 18. Exact validation commands and fresh results

### 18.1 py_compile

Exact command：

~~~bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile \
  collector/app/main.py \
  collector/app/services/event_collector.py \
  collector/app/plc/mapping.py \
  collector/tests/test_event_collector_reliability.py \
  tests/test_collector_station_event_runtime_source.py
~~~

Result：PASS，exit code 0。

### 18.2 Focused pytest A

Exact command：

~~~bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -m pytest \
  collector/tests/test_event_collector_reliability.py \
  -q
~~~

Result：PASS，24 passed, 8 subtests passed in 0.22s，exit code 0。

### 18.3 Focused pytest B

Exact command：

~~~bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -m pytest \
  tests/test_collector_station_event_runtime_source.py \
  -q
~~~

Result：PASS，56 passed in 0.15s，exit code 0。

两个 pytest commands 分别完整运行；没有 -k、skip、xfail、reduced selection、broad suite、coverage、application startup 或 real DB/PLC/network operation。

## 19. Changed-path、cached 与 diff-check audit

测试后、R50 write 前：

~~~text
git diff --name-only:
  collector/app/main.py
  collector/app/plc/mapping.py
  collector/app/services/event_collector.py
  collector/tests/test_event_collector_reliability.py
  tests/test_collector_station_event_runtime_source.py

git diff --cached --name-only: empty
git diff --check: PASS
git diff --cached --check: PASS
R50 report: absent before write
~~~

测试后五条 source/test identities 与 R49 execution-lock identities 保持一致；无 source/test mutation 由本轮 validation 造成。R50 write 后预期唯一新增 path 是本 report；不得 stage/commit/push。

## 20. Raw and normalized untracked-set evidence

本轮保留了 git -c core.quotePath=false ls-files --others --exclude-standard 的 raw observation，并以 repository-relative full path 进行 deterministic UTF-8 stable sort；没有打开 Batch D/E 内容、没有输出其 raw path dump、没有删除/移动/reclassify。

~~~text
before R50 write
raw enumeration count: 311
raw duplicate count: 0
normalized stable-sort unique count: 311
R40–R49 expected report paths present: 10 / 10
Batch D residual count: 300
Batch E (frontend/next-env.d.ts): 1
unknown: 0
missing expected R40–R49: 0
~~~

该 raw/normalized evidence 与 PM expected composition 一致：Batch D 300 + Batch E 1 + R40–R49 10 = 311。Post-write expected composition 为 Batch D 300 + Batch E 1 + R40–R50 11 = 312；final detached audit 负责确认。

## 21. Forbidden-action counters

| Action category | Count | Result |
| --- | ---: | --- |
| source/test/config/contract/status/roadmap/handoff modification | 0 | compliant |
| R48/R49 report modification | 0 | compliant |
| unauthorized report/helper/fixture/manifest/log/sidecar/evidence artifact | 0 before exact R50 write | compliant |
| Git add/stage/commit/push/tag/reset/restore/checkout/stash/clean/delete/move | 0 | compliant |
| build/package/dependency installation | 0 | compliant |
| Docker/Compose/lifecycle | 0 | compliant |
| network/SSH/curl/remote | 0 | compliant |
| real DB connection/query/write/migration | 0 | compliant |
| PLC/V-PLC connect/read/write | 0 | compliant |
| application startup/runtime validation/A–H evidence | 0 | compliant |
| accepted-fact/production event/ACK/read_done activity | 0 | compliant |
| Batch D/E open/delete/move/stage/reclassification | 0 | compliant |

py_compile/pytest 可能产生被 ignore 的 transient cache；本轮没有执行 cleanup，符合禁止清理约束；Git-authoritative untracked composition 仍按上节保持 311。

## 22. Finding matrix and necessity classification

| Finding | Evidence | Classification | R50 disposition |
| --- | --- | --- | --- |
| R48 eager pre-record DB connection | storage.py:18-20；R49 diff；main.py:47；worker run_forever():221 | current-gate necessary repair | CLOSED by PM-accepted R49; independently PASS in R50 |
| Worker constructor could call Storage prematurely | event_collector.py:77-130；AST Storage call count 0；explicit spy test_event_collector_reliability.py:358-396 | current-gate necessary repair | CLOSED; no blocker |
| Main legacy Storage could precede record/Thread | main.py:25-48；ordered oracle :610-660 | current-gate necessary repair | CLOSED; no blocker |
| Storage initialization swallowed/retried/re-emitted | event_collector.py:220-235；test :724-744 | current-gate necessary repair | CLOSED; no blocker |
| Context first consumer not consumed after later constructor failure | event_collector.py:50-74；test :582-594 | current-gate necessary repair | CLOSED; no blocker |
| Canonical line/routing mismatch or list-to-dict false PASS | event_collector.py:100-129,174-191；tests :451-563 | current-gate necessary repair | CLOSED; no blocker |
| Manual same-process context forgery resistance | R42/R45 explicit non-claim; later external PID/container/log provenance | unnecessary / scope expansion | not a current finding; no repair |
| Strict RFC3339 negative assertion for an explicitly hand-built context | main.py:18-22 emits canonical form；consume():54-65 validates Z/UTC via fromisoformat；later parser contract remains strict | next-review carry-forward | bounded recommendation only; does not create current false PASS from main path |
| Generic telemetry, retry, DI, heartbeat, retention or forensic subsystem | R42/R45/R47 stopping rules | unnecessary / duplicate / scope expansion | rejected for current MVP |

## 23. Blockers

~~~text
Current Reliability blockers: none.
Recovery/input identity blockers: none.
Allowlist/forbidden-action blockers: none.
Validation blockers: none.
~~~

No HOLD condition was observed。In particular：DB connection cannot occur before the unique record on the enabled main path；worker constructor cannot construct Storage；required failure paths do not emit a valid success record；Storage failure propagates without retry/poll/re-emission；canonical line/scope checks fail closed；focused oracle detects premature Storage construction；all required validation commands pass。

## 24. Recommendations and necessity classification

1. REL-R50-REC-001：在 future independent implementation/Verification review 中，为 hand-built CollectorStartupContext 增加 one bounded negative fixture，拒绝可被 fromisoformat 接受但不是 canonical RFC3339 T/precision grammar 的 timestamp。分类：next-review carry-forward；不是 current-gate necessary repair，因为 main capture_startup_context() 只生成 canonical UTC Z，后续 runtime parser 仍必须按 R47 strict oracle 验证，当前没有由 main path 造成的 false PASS。
2. REL-R50-REC-002：保持当前 explicit Storage constructor-call/order oracle，不退回只观察 FakeStorage events/writes 的测试方式。分类：unnecessary / duplicate / scope expansion 作为新 task；这是已闭合的 current-gate invariant，不应再开 repair。
3. REL-R50-REC-003：raw transport adapter、application-message extraction、strict JSON parser 与 A–H source/image/process evidence继续留在 later separately authorized runtime/Verification gate。分类：future independent task；不修改当前 three-source/two-test package，也不改变 R50 conclusion。

没有 current-gate necessary repair recommendation。没有把 R42/R45/R47 已冻结的 mandatory later-gate work重复升级为本轮 source/test repair。

## 25. Product/evidence boundary

当前产品状态必须继续保持：

~~~text
ACTIVATED = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED = NO
PRODUCTION-ACCEPTED = NO
~~~

本轮 local source inspection、AST checks、fake-based pytest 和 py_compile 只证明：当前 checkout 的 implementation package 可编译、focused local oracle 通过、R48/R49 source/test bytes 与 reviewed package 一致。它们不证明 deployed process、real DB、PLC runtime、active image/container、fresh container-visible mapping bytes、current container log、accepted station-event fact、ACK/read_done 或 production truth。

## 26. MVP 路径一致性

~~~text
MVP-ALIGNED WITH BACKLOG ITEMS
~~~

approved MVP deliverable：在不改变 PLC、DB、accepted-fact、ACK/read_done 或 production semantics 的前提下，为 Collector runtime-loaded mapping/config claim 建立最小 process-bound success record 与 safe ordering boundary。

minimum invariant：只有完成 same-byte mapping/resolved/read-plan/canonical-line initialization，且 record 已在 worker constructor 最后 required action 发出后，才允许进入 Thread/Storage/poll lifecycle；任何 pre-record DB/PLC/accepted-fact/ACK side effect、retry/replay、premature Storage、scope overwrite 或 failure swallow 都必须 fail closed。

本轮未新增 product capability、runtime topology、threat model、retention、telemetry、audit/forensics、API、DB schema、migration、Docker、remote 或 production acceptance burden。新增的 strict-timestamp assertion 仅是 bounded carry-forward，不阻塞当前 MVP gate。

## 27. Thread 输出 / 上下文评估

~~~text
本次输出长度：长 durable review
当前 Thread 是否建议继续：no
下一轮是否建议新开 Thread：yes
理由：R50 independent Reliability authority 在 exact report write 后 terminalized；后续必须由 ChatGPT PM durable intake 再决定是否发布新的 repair、Data Quality、Verification、Git 或 runtime authority，不能继承 R50。
~~~

## 28. Exact next gate and stop point

~~~text
R50 independent Reliability review WRITTEN
→ ChatGPT PM durable intake
~~~

不得从本报告自动推断 repair、Data Quality、Verification、Git candidate/stage/commit/push、build、Docker、remote、deployment、lifecycle、runtime validation、RUNTIME-LOADED 或 PRODUCTION-ACCEPTED authority。

完成本报告和 post-write detached audit 后立即停止。Report bytes/SHA-256 由 post-write detached audit 返回，不在本报告内自引用。

## 29. State vocabulary and final boundary

~~~text
R48: WRITTEN / TESTED / PM-ACCEPTED FOR INDEPENDENT REVIEW
R49: WRITTEN / TESTED / PM-ACCEPTED
R50: RELIABILITY-REVIEWED / WRITTEN only
source: WRITTEN in current dirty checkout; not committed
tests: TESTED by this report's exact focused commands; not committed
Git: STAGED = NO / COMMITTED = NO / PUSHED = NO
build: NOT BUILT
deploy: NOT DEPLOYED
activation: ACTIVATED = YES is prior product boundary; R50 adds no activation
runtime-loaded: NO
production-accepted: NO
~~~

## 30. R50 final identity rule

本报告为 regular UTF-8 non-symlink durable report。由于把自身最终 SHA-256 写入自身会改变 bytes，bytes 与 SHA-256 不在本报告内自引用；post-write detached read-only audit 将对 exact path 重新测量，并只在 Chat concise manifest 返回该 detached identity。该 detached identity 不构成第二个 artifact，不改变 allowlist，也不建立 PM acceptance、Git 或任何后续 phase authority。

End state：PASS WITH RECOMMENDATIONS / RELIABILITY-REVIEWED / WRITTEN ONLY。
