# Sprint 4 D2-R7B-I1 R52 Independent Verification Implementation Review

## 1. 报告身份、权限与终端结论

- 报告名称：Sprint 4 D2-R7B-I1 R52 Independent Verification Implementation Review
- 任务名称：D2-R7B-I1 R52 — Independently Verify Runtime-Loaded Observability Implementation Package
- 执行 Thread：Verification
- Authority source / ID：PM-D2-R7B-I1-R52-INDEPENDENT-VERIFICATION-IMPLEMENTATION-REVIEW-260730-1507
- Report delivery mode：REPOSITORY_DURABLE_REPORT
- Exact report path：docs/reports/sprint4_d2_r7b_i1_r52_independent_verification_implementation_review.md
- Exact artifact paths：none
- Docs / artifact write authority：仅 exact R52 report path；本次写入消费 authority

## 结论：HOLD

当前 R48 + R49 persisted source/test package 的 source implementation 静态检查、AST 检查、局部 fake-based focused tests、py_compile 与两个完整 pytest command 均通过；但两个 focused test files 尚未形成 R47 terminal implementation matrix 所要求的独立、可回归的全部 negative / expected-value / forbidden-side-effect oracle。存在能够在当前 focused tests 仍 PASS 的 credible false-PASS paths，因此本轮不能进入 PM final implementation-package acceptance 或 separate Git-candidate review。

本结论仅表示 R52 independent Verification implementation review 的 package-readiness gate 为 HOLD。不表示：

~~~
R52 PM-ACCEPTED
GIT-CANDIDATE-ACCEPTED
STAGED
COMMITTED
PUSHED
BUILT
DEPLOYED
RUNTIME-LOADED
PRODUCTION-ACCEPTED
~~~

本轮没有修复任何 source、test、config、contract、status、roadmap 或 handoff；没有执行 Git mutation、build、Docker、remote、runtime 或 production action。

## 2. Scope、合同解释顺序与 non-inheritance

本轮只审查：

- R48 + R49 persisted implementation package；
- collector/app/main.py、collector/app/services/event_collector.py、collector/app/plc/mapping.py、collector/app/services/storage.py；
- collector/tests/test_event_collector_reliability.py；
- tests/test_collector_station_event_runtime_source.py；
- R42 + R45 + R47 implementation-level Verification contract；
- R43 accepted Reliability review、R46 accepted focused Data Quality review、R50 accepted Reliability implementation review、R51 accepted Data Quality implementation review；
- local source/test evidence 与 later runtime/production evidence boundary。

合同解释顺序严格为：

~~~
PM operating rules
→ current PM handoff
→ R42 base implementation contract
→ R45 bounded scope-reset addendum
→ R43 accepted Reliability contract review
→ R46 accepted focused Data Quality contract review
→ R47 accepted Verification planning contract
→ R48 implementation
→ R49 PM-accepted repair
→ R50 independent Reliability implementation review
→ R51 independent Data Quality implementation review
→ current persisted source and tests
~~~

R44 仅作为历史 DQ-B1、DQ-B2、DQ-B3 blocker origin。R45 + R46 已 supersede R44 对 current source 的 blocker interpretation；本轮没有恢复 R44 的 current-source blocker。

R52 不继承 R48、R49、R50 或 R51 authority，不继承其 PASS / PASS WITH RECOMMENDATIONS 作为本轮 Verification result，不授权 repair、Git、build、Docker、remote、runtime validation 或 production acceptance。

## 3. Initial live Git recovery

Recovery 在真实 checkout /Users/chenjie/Documents/MES/edge-mes-demo 完成，且在 R52 report 写入前再次冻结：

| Field | Live result |
| --- | --- |
| repository root | /Users/chenjie/Documents/MES/edge-mes-demo |
| branch | main |
| HEAD | 4a733d7995a94398ade693822662ebd2b22f9d3d |
| origin/main | 4a733d7995a94398ade693822662ebd2b22f9d3d |
| ahead / behind | 0 / 0 |
| cached | empty |
| tracked dirty | exactly five expected source/test paths |
| git diff --check | PASS |
| git diff --cached --check | PASS |
| R52 path before write | ABSENT / NON-SYMLINK |

Initial and pre-write changed tracked set 均为：

~~~
collector/app/main.py
collector/app/plc/mapping.py
collector/app/services/event_collector.py
collector/tests/test_event_collector_reliability.py
tests/test_collector_station_event_runtime_source.py
~~~

git status -sb 为 ## main...origin/main 加上述五条 dirty paths。没有执行 reset、restore、checkout、stash、clean、delete、move 或其他 recovery mutation。

## 4. Exact reviewed input identity table

所有 required input 在写入前均为 readable、regular、NON-SYMLINK；live bytes/SHA-256 与 authority expected identities 一致。

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| docs/thread_handoff/pm_operating_rules.md | 49170 | a692fdafbdea8c63d184cb11548e73731aefccd3110818004b028ba7ee9fe7f5 |
| docs/current_status.md | 150180 | ee7126fd20f1774f54cee9b238cab4e3e0943bce854402b1594060212f88cc23 |
| docs/thread_handoff/chatgpt_pm_handoff_260730-1203.md | 26183 | c9a7ed7283d4574578e1608fc6891bdb91373d97bac3191740863917af3ad8e1 |
| R42 report | 32319 | dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165 |
| R45 report | 13786 | 8fd646f24565bbcb27aa9063038774fee3b5398d66566f961bee296ffff02ef2 |
| R43 report | 30244 | 95b2e63c4879fb5af6920b262300566c577612dd1753b13bf59928c1417338e8 |
| R44 report | 43036 | 3b4d1f3451d0b0036e5530bc83eb35b90ee2b6d140b0a2799b82df1ada035bfa |
| R46 report | 23703 | f460fef43d975de41ed624fa49d8a1a8dcd5246b4ae55b222189f40703914b81 |
| R47 report | 34592 | 4de247e350eb595077219856cf63b0319ee83d14026b6beaaf7c5d83211a0ae4 |
| R48 report | 15692 | caa3203630c5b321c950d078fda7424f4f1ca8edcd7f4a45b88525adfdda0d10 |
| R49 report | 11749 | 5d09732094f3266eccc34a002b0203a3889f33be1c6b56568c43b42c50618dde |
| R50 report | 34024 | 40cfc45b6fcc756a15f2e550b8d7b051a4d797a6bd8c72da1d6b2fb0aa9941d9 |
| R51 report | 42262 | f006a01917b0cdb6deb568e1403cc5bf54d304ee84efc136ec84b2fd4023c7d7 |
| collector/app/main.py | 2525 | d1a461294c91f9f86cde4af87b21bb1147bed5561d64028e8462a8f57d46de80 |
| collector/app/services/event_collector.py | 24313 | 02cab6ea15572ae0b2f6059462f9cd6856cd483ab0dcc37c87d39267aad1e8e2 |
| collector/app/plc/mapping.py | 18876 | ba39583a699f8347c0ff5eaec2e7c807dad909c815269de607a36e8b93c023a7 |
| collector/app/services/storage.py | 38319 | f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b |
| collector/tests/test_event_collector_reliability.py | 32253 | fa8a677f5a249b849438b7ec43e2bbd14ff14e8c590e54d02274daa640b06835 |
| tests/test_collector_station_event_runtime_source.py | 33212 | 7b5b77f40c5bc3eff1a364064876ed79d0d28ffa5bf5f25ee9ba279498d409cd |

上述 source/test identities 在 py_compile、两个 pytest 及 pre-write detached audit 后保持不变。

## 5. Current state distinction

| State | R52 result |
| --- | --- |
| R48 implementation | WRITTEN / TESTED / PM-ACCEPTED FOR INDEPENDENT REVIEW |
| R49 repair | WRITTEN / TESTED / PM-ACCEPTED |
| R50 Reliability review | RELIABILITY-REVIEWED / PASS WITH RECOMMENDATIONS / WRITTEN report |
| R51 Data Quality review | DATA-QUALITY-REVIEWED / PASS WITH RECOMMENDATIONS / WRITTEN report |
| R52 Verification review | WRITTEN / HOLD |
| source/test package | persisted in current dirty checkout, not committed |
| Git | STAGED = NO / COMMITTED = NO / PUSHED = NO |
| build/image | NOT BUILT / no accepted image |
| deployment/process | NOT DEPLOYED / no active-process evidence |
| product boundary | ACTIVATED = YES, STATIC_MAPPING_INITIALIZED = YES |
| runtime/product claims | RUNTIME-LOADED = NO, PRODUCTION-ACCEPTED = NO |

R50 与 R51 的 source-level conclusions 未因当前 source/test bytes 变化而失效：R49 的 pre-record Storage ordering、R50 的 Reliability mechanisms、R51 的 current Data Quality source semantics 均在本轮复核中仍成立。R52 新发现的是 Verification focused oracle sufficiency blocker，而不是把 R44 historical DQ blocker 重新打开。

## 6. Effective R42 + R45 + R47 implementation contract

- main.main() 在第一个 executable boundary 创建 mandatory startup context；不使用默认值、环境 fallback、retry 或 replay。
- Context 至少携带 collector_main_started_at_utc 与 current os.getpid()；consume single-use；missing、reused、foreign-PID、invalid PID/timestamp fail closed；first consumer 在 later constructor failure 后仍 consumed。
- load_edge_mapping() 对 exact path 拒绝 final symlink，要求 regular file；只读一次 raw bytes；同一 bytes 用于 SHA-256、explicit UTF-8 decode 与 YAML parse；duplicate key、invalid UTF-8、malformed YAML、semantic/resolved failure fail closed。
- mapping_content_sha256 是 raw-byte identity；resolved_config_hash 是 semantic/resolved snapshot identity；二者 lower-case 64-hex、来源不可互换，record self-report 不是 expected authority。
- Canonical line_id 来自 hash-bound runtime/resolved snapshot；selected PLC line 仅为 routing projection；missing、empty、ambiguous、mismatch 在 serialization/emission 前 fail closed。
- Read plan 必须 list-first；在 dict conversion 前检查 duplicate station、reserved line、duplicate generated scope、missing/extra/multiset/cardinality、exactly one line plan、disabled station inclusion；read_plan_count 来自完整验证后的 original list。
- v1 record 必须 exact 11-key set、exact schema/event literals、positive non-boolean integer PID/count、lower-case 64-hex hashes、RFC3339 UTC Z timestamp；compact deterministic UTF-8 one-line JSON；allow_nan=False；application grammar 为一条 collector_runtime_loaded_json=<JSON_OBJECT>。
- Logger/serializer failure propagate；record 是 worker constructor 最后 required action，早于 Thread construction/start；enabled main path 的 legacy Storage 在 Thread.start() 之后；worker run_forever() 只在 thread entry 构造一次 Storage，然后 start log，再 first poll。
- Constructor/failure paths 不得 DB、PLC I/O、accepted-fact、ACK/read_done；record 不得泄漏 DSN、credential、PLC raw bytes、station payload、DB result、production fact 或 image/container/Git/runtime-acceptance claim。
- Local source/test evidence 不能升级为 accepted commit、accepted image、deployed process、active container mapping、raw container log、real DB/PLC evidence、RUNTIME-LOADED 或 PRODUCTION-ACCEPTED。

## 7. Requirement → source → test traceability matrix

| Terminal invariant | Source implementation evidence | Positive oracle | Required negative oracle / current focused coverage | Exact failure point | Forbidden-side-effect oracle | R52 ruling |
| --- | --- | --- | --- | --- | --- | --- |
| Main-entry context creation/no default | main.py:18-26; event_collector.py:78-89 | test_main_passes_one_context_and_emits_before_thread_start; test_worker_emits_one_exact_record | missing context and foreign PID at reliability_test.py:565-580; invalid timestamp/zero/bool PID absent | consume before mapping at event_collector.py:87-89 | constructor failure tests observe no Storage calls | source PASS; negative oracle incomplete |
| PID ownership/single-use/failure consumption | event_collector.py:50-74; reliability_test.py:582-594 | current-PID context emits; reused context fails | foreign PID/reuse and later-constructor failure covered; manual-origin and strict timestamp negatives absent | before mapping/serialization | no Storage/client writes in context failure tests | source PASS; strict timestamp carry-forward |
| Main timestamp grammar | main.py:20 | main fake test checks only endswith Z | no strict regex/hand-built noncanonical negative fixture | context consume at event_collector.py:56-65 | no product side effect | current main path canonical; carry-forward |
| Same-byte mapping read | mapping.py:143-160, one read at :150 | runtime_source_test.py:159-184 | no Path.read_text spy; invalid/malformed test :201-210 does not count reads; final symlink/non-regular negatives absent | path :145-149, read/decode/parse :150-155 | no worker/logger/Storage side-effect assertion | BLOCKER V-B1/V-B4 |
| Raw SHA / semantic hash separation | mapping.py:151, :242-260, :282-290; event_collector.py:136-148 | independent raw hashlib check at runtime_source_test.py:182; newline change :187-199 | worker record only regex at reliability_test.py:435-436; no independent expected raw/resolved values | before plans/record | no integrated no-record check for loader/semantic failure | BLOCKER V-B2 |
| Canonical line/routing equality | event_collector.py:95-107; record snapshot at :203 | current mapping emits and line checked at reliability_test.py:417-420 | mismatch/missing/empty/ambiguous at :545-563 | before serialization | failure path zero Storage calls | sufficient for current line false-PASS |
| List-first scope validation | event_collector.py:120-129, :174-191 | valid constructor; disabled count at reliability_test.py:441-449 | duplicate/missing/extra/multiset/duplicate station at :451-495; direct missing-line/one-to-one absent | validation :121 before dict :122; materialization :124-129 | :497-523 checks no storage/client writes | core PASS; bounded oracle gap |
| Exact 11-key record/literals | event_collector.py:196-208; constants :33-35 | exact set/literals :401-418 | set catches missing/extra; positive count/PID >0 and exact hash values absent | record before dumps :196-209 | no Storage in constructor spy | BLOCKER V-B2/V-B3 |
| Serialization/determinism | event_collector.py:209-218 | compact expected dump :421-430 | failure propagation :596-608; delimiter count/nonfinite negative absent | serializer/logger call | no thread/Storage on failure | source PASS; grammar oracle incomplete |
| Constructor-last-action/order | event_collector.py:119-130; main.py:35-47 | ordered events :610-660 | failure prevents thread/start/storage :662-697; no Thread.start failure fixture | record before Thread; legacy Storage :47 | real Storage constructor spy | R50/R51 remains valid |
| Worker Storage/run/poll ordering | event_collector.py:220-235; storage.py:18-20 | storage→poll :699-722 | init failure one call/no retry/no poll/re-emission :724-744 | Storage :221 | no poll/second record | PASS |
| Failure path no DB/PLC/accepted-fact/ACK/read_done | event_collector.py:237-426 | no-I/O fake constructor | mapping parse/semantic failure lacks worker-integrated side-effect oracle | before record for covered constructor cases | missing for loader failure integration | BLOCKER V-B4 |

## 8. Positive-oracle matrix

| Subject | Positive oracle | Independence assessment |
| --- | --- | --- |
| context handoff | main fake receives one context; worker consumes current PID | credible for handoff/order; timestamp only suffix-level |
| single-use | one worker emits; same context second construction raises | credible; failure-consumption covered |
| mapping one-read | Path.read_bytes count 1 and YAML input equals decoded test bytes | credible for current read_bytes path, not alternate read |
| raw hash | independent hashlib.sha256(raw_bytes) equality | credible for loader raw field |
| semantic stability | newline variation distinct raw SHA/equal computed semantic hash | relation demonstrated; expected semantic hash uses same implementation |
| canonical line | current LINE_001 record and routing mismatch negatives | adequate for mismatch; success source-role distinction AST-backed |
| plan count | disabled station uses len(build_read_plans(mapping)) | not fully independent of plan generator |
| exact keys/literals | set equality and frozen literals | credible |
| type | int plus not bool | catches bool, not non-positive |
| ordering | ordered event list and real Storage constructor spy | credible/non-tautological |
| Storage failure | one constructor, propagated error, no poll/re-emission | credible |

## 9. Negative-oracle matrix

| Required negative | Current test | Result |
| --- | --- | --- |
| missing context | reliability_test.py:568-570 | covered |
| foreign PID / reused context | reliability_test.py:571-580 | covered |
| first consumer remains consumed after later failure | reliability_test.py:582-594 | covered |
| noncanonical fromisoformat timestamp | none | bounded carry-forward: main canonical, later parser strict |
| bool/zero/negative context PID | none | source check exists; focused negative incomplete |
| final symlink | none | current blocker V-B1 |
| non-regular mapping path | none | current blocker V-B1 |
| second read_text/different-byte parse | no text-read spy; only read_bytes count | current blocker V-B1 |
| invalid UTF-8 / malformed YAML | runtime_source_test.py:201-210 | direct loader negative; worker side-effect absent |
| duplicate YAML key | runtime_source_test.py:213-218 | loader negative covered; worker integration absent |
| semantic/resolved hash failure | runtime_source_test.py:500-512 | registry negative; worker integration absent |
| line missing/empty/ambiguous/mismatch | reliability_test.py:545-563 | covered |
| duplicate/missing/extra/multiset plan | reliability_test.py:451-495 | core cases covered |
| exact positive integer | only type/non-bool | >0 absent; V-B3 |
| exact raw/resolved record hashes | regex only | independent expected absent; V-B2 |
| serializer/logger failure | reliability_test.py:596-608 | covered |
| one delimiter/application grammar | startswith + split('=', 1) | exact oracle incomplete; V-B3 |
| Storage premature/failure retry | reliability_test.py:391-396, :699-744 | covered |

## 10. Exact failure-point matrix

| Failure | Current source point | Must happen before | R52 assessment |
| --- | --- | --- | --- |
| context missing/reused/PID invalid | event_collector.py:50-74, :87-89 | mapping, serialization, record | source correct; invalid-value tests incomplete |
| final path symlink/non-regular | mapping.py:145-149 | read/hash/decode/parse and worker actions | source correct; negative oracle missing |
| read/decode/YAML/semantic failure | mapping.py:150-160; worker :93-94 | record :130 | source ordering correct; integrated oracle missing |
| hash/resolved projection mismatch | event_collector.py:132-162 | plan materialization and record | source correct; expected-value oracle incomplete |
| routing line mismatch | event_collector.py:100-107 | serialization | covered |
| plan scope/cardinality failure | event_collector.py:174-191 | dict :122, record :130 | core covered |
| serialization failure | event_collector.py:209-217 | logger and thread | covered |
| logger failure | event_collector.py:218 | constructor return/thread | covered |
| Storage initialization failure | event_collector.py:221 outside try loop | first poll/retry loop | covered |

## 11. Forbidden-side-effect matrix

| Path | Required forbidden effects | Current evidence | Ruling |
| --- | --- | --- | --- |
| successful worker constructor | no Storage, DB, PLC connect/read/write, accepted fact/ACK/read_done | Storage spy :364-396; AST __init__ Storage count 0 | PASS |
| mapping/context/line/plan failure | no record, Storage, PLC I/O, accepted fact, ACK/read_done | context/line/scope tests observe no Storage; scope observes no client writes | PASS for covered paths |
| loader invalid UTF-8/YAML/semantic | same no-side-effect boundary | direct loader tests do not construct worker/logger/client | HOLD gap V-B4 |
| serializer/logger failure | no fallback/retry/substitute/replay | :596-608; source no catch | PASS |
| main enabled ordering | record → Thread construction → Thread.start → legacy Storage | :610-660 | PASS |
| worker run | one Storage → start log → first poll | :699-744 | PASS |
| later polling | DB/PLC/accepted-fact/ACK/read_done later runtime behavior | event_collector.py:237-426 | out of current claim |

## 12. Startup-context ownership、PID、single-use 与 failure consumption

Source review：

- main.py:25-26 creates context before load_config and before source setup.
- main.py:35-40 passes the same context only to enabled worker path.
- CollectorStartupContext has no default for required fields; EventCollectorWorker.startup_context is required keyword-only with no default.
- consume() marks _consumed at event_collector.py:53 before timestamp/PID validation and mapping construction.
- PID rejects bool, non-int and non-positive at :66-71, then compares to current os.getpid() at :72-73.
- No os.getenv/os.environ context fallback, worker context generation, retry, replay or exception-based re-emission exists in reviewed implementation paths.
- test_constructor_failure_consumes_context_and_prevents_retry proves monotonic consumption after later routing failure.

Independent timestamp acceptance probe showed that consume() accepts noncanonical-but-fromisoformat-accepted forms including space separator, missing seconds, basic date/time, comma fractional separator and ISO week date. capture_startup_context() itself emits datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z') with T, seconds and UTC Z.

Classification: BOUNDED VERIFICATION CARRY-FORWARD for strict RFC3339 negative fixture, not a new current false-PASS blocker. Current main-created authority is canonical; context is not a hostile same-process anti-forgery token; later R47 runtime parser must apply strict timestamp grammar and external process/time authority. This does not cure V-B1–V-B4.

## 13. Strict RFC3339 recommendation independent terminal classification

| Check | Result |
| --- | --- |
| capture_startup_context grammar | canonical UTC Z, ISO T, seconds, optional microseconds |
| CollectorStartupContext.consume range | broader than strict RFC3339 through datetime.fromisoformat |
| focused positive oracle | fixed timestamp plus endswith Z only |
| focused negative oracle | absent |
| credible current false PASS | not established under current claim because main-created authority is canonical and later external parser is strict |
| classification | BOUNDED VERIFICATION CARRY-FORWARD |
| current repair | none authorized |

## 14. Same-byte mapping loader analysis

Current source chain：

~~~
source_path.is_symlink()
→ source_path.resolve(strict=True)
→ canonical_path.is_file()
→ canonical_path.read_bytes() once
→ sha256(raw_bytes)
→ raw_bytes.decode('utf-8')
→ yaml.load(decoded_text, UniqueKeySafeLoader)
→ parse_edge_mapping(raw)
→ bind canonical path/raw SHA
~~~

AST confirms one canonical_path.read_bytes() call, zero read_text() calls in the persisted loader, one SHA-256 call, one decode and one YAML load. Duplicate YAML keys fail through UniqueKeySafeLoader; root/semantic/decoder-registry failures occur before EdgeMapping return. Current source implementation passes same-byte semantic review.

Verification oracle does not pass: test_mapping_loader_reads_exact_raw_bytes_once_and_binds_raw_identity patches/counts only Path.read_bytes; it does not spy Path.read_text or another alternate read. A hypothetical implementation that hashes read_bytes then parses a second read_text can pass that test for ordinary LF input. The test named invalid_utf8_and_malformed_yaml_fail_closed_without_second_read asserts only exceptions and does not count reads. No focused test creates a final symlink or directory path. This is a current Verification blocker, not a claim that current loader presently has the defect.

## 15. Raw mapping_content_sha256 versus semantic resolved_config_hash

Current source roles remain distinct：

- mapping_content_sha256 is hashlib.sha256(raw_bytes).hexdigest() at mapping.py:150-151.
- resolved_config_hash is RuntimeMappingSnapshot.config_hash at mapping.py:242-260 and :282-290, checked against resolved snapshot at event_collector.py:138-148.
- Both current values are lower-case 64-hex before record emission; worker regex enforcement is at event_collector.py:136-141.
- Raw newline change proves raw SHA changes while semantic snapshot hash remains stable, but that semantic expected value is obtained from the same implementation path.
- Record self-report is not expected authority; later R45/R47 expected values must come from fresh exact bytes and independent/frozen accepted semantic algorithm.

Current implementation source passes. The focused worker record test only checks r"^[0-9a-f]{64}$" for both fields and does not assert emitted raw hash equals actual test bytes or emitted resolved hash equals independent expected snapshot value. Swapped raw/semantic fields or constant lower-case 64-hex values could pass focused tests. This is V-B2, a current Verification blocker.

## 16. Canonical line / routing equality analysis

Current implementation satisfies R45/R46：

~~~
canonical_line_id = resolved_config_snapshot.line_id
equivalent origin = mapping.runtime_snapshot.line_id
selected PLC line = routing projection only
record line = resolved_config_snapshot.line_id
~~~

event_collector.py:95-107 requires exactly one PLC entry, non-empty selected routing line and exact equality with canonical snapshot line. event_collector.py:203 emits snapshot line, not unchecked routing projection. Focused tests cover mismatch, missing, empty and ambiguous selected routing identities at reliability_test.py:545-563; no success is emitted on those paths.

The success fixture has equal canonical/routing values, so source-role authority is primarily source/AST-backed rather than independent success-fixture-backed. This does not create a current line false-PASS because mismatch negative and pre-serialization equality guard exist. Bounded recommendation only.

## 17. List-first read-plan / scope / count analysis

event_collector.py:174-191 preserves configured_station_ids, expected_scopes and generated_scopes before plans = {plan.scope: plan ...} at :122. It rejects reserved line, duplicate configured stations, duplicate generated scopes, cardinality mismatch, multiset mismatch, non-one-line and non-positive plan list. :124-129 materializes one station runtime per configured station and checks cardinality. Disabled stations are not filtered and remain in expected scope/count. read_plan_count is len(plans_list) at :130.

Focused tests cover duplicate station, duplicate plan, missing station scope, extra/multiset mismatch and disabled station count. Storage/client side-effect assertions cover the main scope failure path.

There is no direct fixture that removes the line plan or independently asserts the post-validation one-to-one runtime list, and the disabled count expected value is computed with the same build_read_plans(mapping) function rather than a frozen independent count. Source order and negative scope checks nevertheless prevent the specific dict-overwrite false-PASS in current code. These are bounded pre-acceptance oracle improvements and must be addressed together with V-B blockers before future final package acceptance.

## 18. Exact v1 record analysis

Current record literal at event_collector.py:196-208 contains exactly：

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

Exact schema/event literals are frozen constants. json.dumps uses ensure_ascii=False, sort_keys=True, compact separators and allow_nan=False; CR/LF is rejected. Logger call is one synchronous logger.info(f"collector_runtime_loaded_json={serialized}").

The exact-record test detects missing/extra keys, schema/event literal changes, bool-vs-int, compact serialization mismatch and prohibited production/ack/read_done substrings. It does not independently verify:

- record raw SHA against exact test bytes;
- record resolved hash against independent semantic expected value;
- process_pid == os.getpid() at record assertion;
- read_plan_count > 0 and process_pid > 0;
- exact one-delimiter count rather than only startswith plus split('=', 1).

Those omissions can allow wrong positive values or swapped hash authority to pass focused tests. They are current Verification blockers V-B2/V-B3 although persisted source expressions are correct.

## 19. Deterministic serialization、delimiter 与 logger analysis

Source inspection confirms no catch around json.dumps or logger.info; serializer/logger exceptions propagate. No fallback, retry, substitute success, delayed replay, poll-loop emission or persistent replay exists in reviewed paths. Record is emitted once from constructor and no second record path exists in run_forever().

The focused serializer test recomputes compact JSON from the already parsed record and compares the application message. This is valid serialization-shape coverage, but not independent value coverage. The test checks literal prefix but not exact delimiter count; current source has one literal delimiter and compact one-line JSON. Delimiter/strict-message negative remains bounded V-B3 gap.

## 20. Constructor-last-action、main/Thread/Storage ordering

AST and source review：

- EventCollectorWorker.__init__() has zero Storage(...) calls and final statement _emit_runtime_loaded_record(...) at event_collector.py:130.
- snap7.client.Client() at :119 constructs a client object only; connect/read/write are later poll_once paths.
- main.py:35-45 constructs and starts event Thread only after worker constructor/record; main.py:47 constructs legacy Storage after Thread.start().
- run_forever() constructs worker Storage exactly once at event_collector.py:221, logs worker start, then enters first poll_once() at :230.
- storage.py:18-20 is the real psycopg.connect boundary; not reached on enabled main path before record and thread start.

R50 ordered-event test is credible: it uses a real Storage constructor-call spy and observes record → thread_construct → thread_start → legacy_storage_construct. R50 storage-failure test observes one construction, propagated error, no poll and no runtime-record re-emission. R50/R51 ordering conclusions remain valid.

## 21. Test-oracle anti-tautology assessment

### Credible oracles

- Storage constructor-call spy records constructor invocation rather than inspecting FakeStorage state at reliability_test.py:364-396.
- Ordered-event oracle detects record/Thread/legacy Storage reordering at :610-660.
- Path.read_bytes count plus YAML loader input can detect the current one-read path and different decoded content for the tested read path at runtime_source_test.py:159-184.
- Exact key-set assertion detects missing/extra v1 keys at reliability_test.py:401-416.
- not isinstance(value, bool) distinguishes bool from int at :431-434.

### Tautological or incomplete oracles

- Record serialization expected string is constructed from parsed record itself at :421-430. Acceptable for formatting only; cannot validate independent hash/line/count/PID authority.
- Disabled-station count expected value uses len(build_read_plans(mapping)) at :441-449, reusing the same plan generator rather than fixed independently derived count.
- Runtime semantic hash tests compare values produced by the same semantic hash implementation; raw SHA has independent hashlib assertion, but worker record binding does not.
- Worker record test checks hash shape, not expected hash identity; wrong lower-case 64-hex values can pass.
- Mapping test observes only read_bytes, so a second read_text can evade it.

Current focused tests are not fake-only premature-I/O false PASS for Storage/order; R49/R50 closed that issue. But they are not a complete independent Verification oracle for same-byte path identity and record field authority. This is the basis of HOLD.

## 22. Expected-value independence assessment

| Record field/group | Required independent expected source | Current focused oracle |
| --- | --- | --- |
| schema/event | frozen R42/R45 literals | exact literals; PASS |
| mapping path | exact loader-bound path fixture | indirectly current path; no symlink negative |
| raw mapping SHA | hashlib.sha256 of exact fixture bytes | loader test only; worker record not compared |
| mapping schema/config/canonical line | parsed exact fixture/snapshot | line hardcoded current value; no same-snapshot expected matrix |
| read-plan count | independently derived full scope count, disabled included | same build_read_plans generator; not fully independent |
| resolved hash | independently recomputed accepted semantic algorithm or frozen expected | source function consistency only; no worker record expected comparison |
| PID | current os.getpid() | context source/test; record field only type/non-bool |
| timestamp | main-created canonical timestamp plus later strict parser | fixed hand-built timestamp/suffix check; strict negative carry-forward |

Record self-report is not used as expected authority by this report or source review. Current focused tests do not fully materialize independent expected values needed to detect wrong record projection. V-B2 remains a current Verification blocker.

## 23. Prohibited-field、secret与truth-boundary audit

Source record key set has no DSN, credential, host/port, PLC raw bytes, station payload, unit/DMC, DB result, accepted fact, ACK/read_done, machine state, production event, image ID, container ID, Git ID, deployment field or runtime-acceptance field. Storage retains DSN internally for later run_forever construction but it is not placed in the application record.

Focused test checks absence of production, ack and read_done; exact key-set/source inspection covers remaining prohibited classes. No source/test/report text represented local/static/fake evidence as current active container, raw log, real DB/PLC, RUNTIME-LOADED or PRODUCTION-ACCEPTED. No A–H artifact, future parser, image identity or deployment claim was created.

## 24. DQ-B2 / DQ-B3 later-gate boundary

R46/R51 closures remain valid and are not current source blockers：

~~~
accepted implementation source/path manifest
→ accepted built/deployed full image ID
→ fresh active full image ID
→ fresh active full container ID + StartedAt
→ active Collector main PID/process identity
→ fresh active-container mapping bytes
→ emitted raw/semantic hashes
→ parsed v1 record
~~~

R52 HOLD does not authorize or require DQ-B2 deployment binding, DQ-B3 A–H raw/payload/parsed artifact creation, strict runtime parser execution, source/image acceptance, Docker, remote observation or runtime validation. Future A–H filenames remain unselected. Current absence of image/container/process/raw-log evidence is NOT_EXECUTED, not current implementation failure.

## 25. Exact validation commands and fresh results

### 25.1 py_compile

Exact authorized command：

~~~bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile \
  collector/app/main.py \
  collector/app/services/event_collector.py \
  collector/app/plc/mapping.py \
  collector/tests/test_event_collector_reliability.py \
  tests/test_collector_station_event_runtime_source.py
~~~

Result：PASS, exit code 0。

### 25.2 Focused pytest A

Exact authorized command：

~~~bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -m pytest \
  collector/tests/test_event_collector_reliability.py \
  -q
~~~

Result：PASS, 24 passed, 8 subtests passed in 0.22s, exit code 0。

### 25.3 Focused pytest B

Exact authorized command：

~~~bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -m pytest \
  tests/test_collector_station_event_runtime_source.py \
  -q
~~~

Result：PASS, 56 passed in 0.14s, exit code 0。

两个 pytest command 均分别完整运行；未使用 -k、skip、xfail、reduced selection、broad suite、coverage；未启动应用，未连接真实 DB/PLC/network/remote。

## 26. Source/test identity、post-test mutation与 Git/package audit

测试后至 execution lock 的 source/test identity 仍为：

~~~
collector/app/main.py                                      2525  d1a461294c91f9f86cde4af87b21bb1147bed5561d64028e8462a8f57d46de80
collector/app/services/event_collector.py                  24313 02cab6ea15572ae0b2f6059462f9cd6856cd483ab0dcc37c87d39267aad1e8e2
collector/app/plc/mapping.py                               18876 ba39583a699f8347c0ff5eaec2e7c807dad909c815269de607a36e8b93c023a7
collector/tests/test_event_collector_reliability.py        32253 fa8a677f5a249b849438b7ec43e2bbd14ff14e8c590e54d02274daa640b06835
tests/test_collector_station_event_runtime_source.py       33212 7b5b77f40c5bc3eff1a364064876ed79d0d28ffa5bf5f25ee9ba279498d409cd
~~~

storage.py 保持 38319 / f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b。git diff --name-only 与 expected tracked dirty set 完全一致；git diff --cached --name-only empty；两项 diff check PASS。没有 source/test post-test mutation。

## 27. Raw and normalized untracked-set evidence

使用 R36 authority materialization JSON 仅作 membership comparison；Batch D/E 内容没有打开、删除、移动、stage 或 reclassify。Raw enumeration 使用 NUL records；normalized comparison 使用 repository-relative full path 的 deterministic UTF-8 stable sort。

### R52 写入前冻结值

| Observation | Result |
| --- | ---: |
| raw untracked count | 313 |
| normalized unique count | 313 |
| duplicate count | 0 |
| Batch D | 300 |
| Batch E | 1 |
| R40–R51 reports | 12 |
| unknown | 0 |
| missing expected membership | 0 |
| R52 before write | ABSENT |

R52 exact report write 是唯一授权新增 path，因此写入后 expected composition 为 Batch D 300 + Batch E 1 + R40–R52 13 = 314，unknown 0。最终 detached audit 在 Chat manifest 返回实际 bytes/SHA 与 final composition；不在本报告内自引用。

## 28. Forbidden-action counters

| Action category | Count | Result |
| --- | ---: | --- |
| authorized R52 report write | 1 | exact path only |
| source/test/config/contract/status/roadmap/handoff modification | 0 | compliant |
| R48/R49/R50/R51 report modification | 0 | compliant |
| unauthorized helper/fixture/manifest/raw-log/sidecar/A–H artifact | 0 | compliant |
| Git add/stage/commit/push/tag | 0 | compliant |
| reset/restore/checkout/stash/clean/delete/move/merge/rebase/cherry-pick | 0 | compliant |
| build/package/dependency installation | 0 | compliant |
| Docker/Compose/lifecycle | 0 | compliant |
| network/SSH/curl/remote | 0 | compliant |
| real DB connection/query/write/migration | 0 | compliant |
| PLC/V-PLC connection/read/write | 0 | compliant |
| application startup/runtime validation | 0 | compliant |
| A–H evidence generation | 0 | compliant |
| accepted-fact/production event/ACK/read_done activity | 0 | compliant |
| Batch D/E content open/delete/move/stage/reclassification | 0 | compliant |
| R36 JSON membership read | 1 | explicitly authorized |

授权的 AST/hash/timestamp/set probes、py_compile 与 focused pytest 仅属于 local/static/fake validation；没有产生 runtime 或 production evidence。

## 29. Finding matrix与necessity classification

| Finding | Minimum evidence | Classification | Terminal disposition |
| --- | --- | --- | --- |
| read_bytes test does not detect second read_text/alternate read; invalid-read test does not count reads | runtime_source_test.py:159-180, :201-210 | current Verification blocker | HOLD; no repair authorized |
| final symlink and non-regular mapping negative oracle absent | no symlink/directory fixture; source checks mapping.py:145-149 | current Verification blocker | HOLD; no repair authorized |
| worker record raw/resolved hash fields only regex-checked; no independent expected values | reliability_test.py:435-436; serializer expected derives from record | current Verification blocker | HOLD; no repair authorized |
| record PID/count positive-value and exact application-grammar oracle incomplete | reliability_test.py:431-434, :399-400 | current Verification blocker | HOLD; no repair authorized |
| invalid mapping/decode/semantic failure not integrated with no-record/no-DB/no-PLC side-effect oracle | direct loader/registry tests do not construct worker/logger/client | current Verification blocker | HOLD; no repair authorized |
| strict RFC3339 hand-built negative fixture absent | consume accepts broader fromisoformat range; main generator canonical; later parser strict | bounded Verification carry-forward | later parser/evidence gate |
| missing direct line-plan and station-runtime one-to-one negative fixture | core scope tests/source order exist | bounded pre-acceptance oracle recommendation | future same-path oracle repair |
| DQ-B2 source/image/config/process chain absent locally | R45/R46/R47 later evidence boundary | later runtime evidence task | not current blocker |
| DQ-B3 A–H raw/payload/parsed artifacts absent | R45/R46/R47 later evidence boundary | later independent task | not current blocker |
| record_emitted_at, scope list, telemetry, retention, forensic or hostile anti-forgery additions | no concrete current false-PASS need | unnecessary / scope expansion | rejected |

## 30. Current blockers

### V-B1 — Same-byte loader negative oracle is incomplete

Current load_edge_mapping() source is correct, but focused tests can pass if a future source regression uses a second Path.read_text() after hashing. Current test counts only Path.read_bytes and does not instrument alternate reads. It also has no final symlink or non-regular path negative. This violates R52 requirement that mapping-loader oracle detect second read/different-byte parse and all required negative paths be covered.

### V-B2 — Record raw/semantic expected-value oracle is not independent

Worker positive test checks both hashes only against lower-case 64-hex regex. It does not compare mapping_content_sha256 to exact test bytes or resolved_config_hash to an independent/frozen semantic expected value. A wrong hash assignment or constant digest can pass focused tests. Serializer expected string is built from parsed record itself and cannot serve as value-authority oracle.

### V-B3 — Exact positive numeric and application-grammar oracle is incomplete

Focused test distinguishes bool from int but does not assert positive PID/count values. It checks startswith and split('=', 1) rather than exact one-delimiter application grammar. Current source has required checks, but focused package can pass after a record-value or grammar regression that remains within tested shape. This is a frozen v1 Verification requirement.

### V-B4 — Mapping/semantic failure side-effect oracle is not integrated

Invalid UTF-8, malformed YAML, duplicate key and semantic/resolved failures are tested directly at loader/registry layer. Focused files do not construct worker with these failures while asserting zero logger success emission, zero Storage construction, zero PLC I/O and zero accepted-fact/ACK/read_done activity. Source ordering currently places failures before emission, but required forbidden-side-effect regression oracle is incomplete.

These are package Verification blockers. They do not imply current persisted source presently executes a second read, emits wrong hash, performs premature Storage construction or leaks production data. No current source/test repair is authorized; stop condition is reached.

## 31. Recommendations

1. Under a fresh PM-authorized implementation/package-repair authority, add only minimum focused oracle changes needed to close V-B1–V-B4: alternate-read counting, final symlink/non-regular fixtures, independent raw/semantic expected values, positive PID/count and exact delimiter assertions, and integrated loader/semantic failure side-effect assertions.
2. Keep explicit Storage constructor spy and ordered-event oracle from R49/R50; do not replace them with FakeStorage state assertions.
3. Keep strict RFC3339 negative fixture as bounded Verification/runtime parser carry-forward. It should reject space/basic/week-date/missing-seconds/comma forms while preserving canonical main-created form; it is not authorization to add hostile same-process subsystem.
4. Add direct missing-line and station-runtime one-to-one fixtures only within same exact two focused test paths if PM opens repair authority; do not create a third test path.
5. Preserve DQ-B2/DQ-B3 as later source/image/config/process and A–H runtime evidence gates; do not add image/container/Git/raw-artifact fields to v1 or current source.

## 32. PM final implementation-package / Git-candidate eligibility

eligible to enter separate PM final implementation-package acceptance / Git-candidate review: NO。

Reason：R52 has current Verification blockers V-B1–V-B4. Package is locally WRITTEN + TESTED + RELIABILITY-REVIEWED + DATA-QUALITY-REVIEWED, but not VERIFICATION-REVIEWED because focused oracle set does not credibly prevent listed false-PASS paths.

This does not authorize repair. PM must issue a new exact authority if it chooses to repair focused oracle package. After that authority produces a new persisted package, PM may decide whether to issue a fresh independent review; no authority is inherited from R52.

## 33. Product/evidence boundary

Only local conclusion supported by this report is：

~~~
current source/test bytes are identified;
current source static/AST review is complete;
focused tests execute and pass locally;
R50/R51 implementation-review conclusions remain valid within their scopes;
R52 Verification package gate is HOLD because focused oracle sufficiency is incomplete.
~~~

The following remain unobserved/not established：

~~~
accepted implementation commit
accepted image
deployed active process
current container-visible mapping
raw container log
real DB evidence
real PLC evidence
runtime A–H evidence
RUNTIME-LOADED
PRODUCTION-ACCEPTED
~~~

ACTIVATED = YES and STATIC_MAPPING_INITIALIZED = YES are prior product boundary facts; they do not imply R52 runtime or production claim.

## 34. MVP 路径一致性

分类：MVP-ALIGNED WITH BOUNDED VERIFICATION HOLD。

批准的 MVP deliverable 是：在不改变 PLC、DB、accepted-fact、ACK/read_done 或 production semantics 的前提下，为 Collector runtime-loaded mapping/config initialization claim 建立最小 process-bound application record 与可信 local implementation oracle。

本轮 blockers 直接对应 false PASS 风险：second mapping read/different-byte parse、raw/semantic identity substitution、wrong positive record values、以及 failure-path side-effect leakage。它们没有新增 API、DB schema、migration、telemetry、generic audit/forensics、retention、cryptographic provenance、runtime topology 或 production capability。

R52 没有发生任务膨胀到 Docker、remote、A–H runtime generation 或 production acceptance；strict timestamp 与 DQ-B2/B3 仍被限制在 later gate。当前最小 next action 是 PM 处理 R52 HOLD，而不是继续扩大本 Thread 或自行修复。

## 35. Thread 输出 / 上下文评估

- 本次输出长度：长 durable report
- 当前 Thread 是否建议继续：no
- 下一轮是否建议新开 Thread：yes
- 理由：R52 one-shot Verification review authority 在 exact report write 后 terminalized；当前已有明确 package oracle blockers，任何 repair 必须由 PM 发布 fresh exact authority，不能继承 R52 或 R50/R51 authority。

## 36. Exact next gate and stop point

~~~
R52 independent Verification implementation review WRITTEN / HOLD
→ ChatGPT PM durable intake
→ PM decides whether to issue a fresh exact-path oracle repair authority
→ only after a repaired persisted package and fresh independent review may PM reconsider final implementation-package acceptance
→ Git-candidate review remains separate and requires fresh PM authorization
~~~

完成本报告后不得执行：source/test repair、stage、commit、push、tag、build、Docker/Compose、network/SSH、remote observation、runtime validation、A–H evidence generation、RUNTIME-LOADED acceptance 或 PRODUCTION-ACCEPTED acceptance。

Final report bytes/SHA-256 由 post-write detached audit 返回；不在本报告内自引用。
