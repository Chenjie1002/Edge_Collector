# Sprint 4 D2-R7B-I1 R51 Independent Data Quality Implementation Review

## 1. 报告身份、authority 与结论

报告名称：Sprint 4 D2-R7B-I1 R51 Independent Data Quality Implementation Review

任务名称：D2-R7B-I1 R51 — Independently Review Runtime-Loaded Observability Data Quality Implementation

执行 Thread：Data Quality

Authority source / ID：PM-D2-R7B-I1-R51-INDEPENDENT-DATA-QUALITY-IMPLEMENTATION-REVIEW-260730-1446

Report delivery mode：REPOSITORY_DURABLE_REPORT

Exact report path：

    docs/reports/sprint4_d2_r7b_i1_r51_independent_data_quality_implementation_review.md

Exact artifact paths：none

Docs / artifact write authority：仅 exact R51 report path；本报告第一次写入时消费。

本 authority 是 one-shot、Data Quality review-only，不继承 R48、R49 或 R50 authority；不授权 source、test、config、contract、status、roadmap、handoff、repair、Reliability、Verification、Git、build、Docker、remote、runtime validation 或 production acceptance。

最终结论：

    PASS WITH RECOMMENDATIONS

该结论仅表示当前 persisted R48 + R49 source/test implementation package 通过本轮独立 Data Quality implementation review，且无 current-gate blocker。它不表示：

    DATA-QUALITY-ACCEPTED
    VERIFICATION-REVIEWED
    STAGED
    COMMITTED
    PUSHED
    BUILT
    DEPLOYED
    RUNTIME-LOADED
    PRODUCTION-ACCEPTED

本报告是唯一本轮 task-owned write。报告 bytes/SHA-256 不在报告内自引用，由 post-write detached audit 返回。

## 2. Review scope、precedence 与 non-inheritance

本轮只审查：

- R48 + R49 persisted implementation package；
- R42 + R45 + R46 当前有效 Data Quality contract；
- R43 accepted Reliability implementation review 的未改变边界；
- R47 Verification planning contract 中的 future oracle；
- current persisted source、storage boundary 与两个 focused tests；
- local source/test evidence 与 later runtime/production evidence 的 truth boundary。

合同解释顺序严格采用：

    PM operating rules
    → current PM handoff
    → R42 base implementation contract
    → R45 bounded Data Quality scope-reset addendum
    → R43 Reliability acceptance
    → R46 accepted focused Data Quality contract
    → R47 Verification planning contract
    → R48 implementation
    → R49 repair
    → R50 accepted Reliability implementation review
    → current persisted source and tests

R44 只作为历史 DQ-B1、DQ-B2、DQ-B3 blocker origin。R45 + R46 已 supersede R44 对 current source 的 blocker interpretation；R44 的历史 HOLD 不在本轮重新升级。

当前产品边界：

    ACTIVATED = YES
    STATIC_MAPPING_INITIALIZED = YES
    RUNTIME-LOADED = NO
    PRODUCTION-ACCEPTED = NO

## 3. Initial live Git recovery

在任何 R51 report write 前，从真实 checkout 执行了 Prompt 要求的 read-only recovery：

    cd /Users/chenjie/Documents/MES/edge-mes-demo

    git status -sb
    git log -8 --oneline --decorate
    git rev-parse --show-toplevel
    git rev-parse --abbrev-ref HEAD
    git rev-parse HEAD
    git rev-parse origin/main
    git rev-list --left-right --count HEAD...origin/main
    git diff --name-only
    git diff --cached --name-only
    git diff --check
    git diff --cached --check
    git -c core.quotePath=false ls-files --others --exclude-standard

Recovery result：

| Field | Live result |
| --- | --- |
| repository root | /Users/chenjie/Documents/MES/edge-mes-demo |
| branch | main |
| HEAD | 4a733d7995a94398ade693822662ebd2b22f9d3d |
| origin/main | 4a733d7995a94398ade693822662ebd2b22f9d3d |
| ahead / behind | 0 / 0 |
| tracked dirty | exactly the five expected R48/R49 source/test paths |
| cached | empty |
| git diff --check | PASS |
| git diff --cached --check | PASS |
| R51 report before write | ABSENT / NON-SYMLINK |
| R51 authority pre-write | usable |

Five tracked dirty paths：

    collector/app/main.py
    collector/app/plc/mapping.py
    collector/app/services/event_collector.py
    collector/tests/test_event_collector_reliability.py
    tests/test_collector_station_event_runtime_source.py

Recent log：

    4a733d7 (HEAD -> main, origin/main, origin/HEAD) Add PM handoff before runtime-loaded implementation
    ce22ca7 Add ChatGPT PM handoff after authority-chain closeout
    35c50b1 Materialize current Collector activation authority chain
    2d7ff45 Materialize repository governance and hygiene inventory
    ac33e6b Add PM handoff after image load gate closeout
    6656367 Accept exact loaded Collector image gate
    ca68dd4 Add PM handoff before Collector activation
    1fac3ee Add PM handoff after R30 reliability cleanup holds

没有执行 reset、restore、checkout、stash、clean、delete、move 或任何 mutation 修复 recovery。

## 4. Raw / normalized untracked-set evidence

在 R51 写入前保留了 git -c core.quotePath=false ls-files --others --exclude-standard -z 的 raw observation；没有打开 Batch D/E 内容。

采用 repository-relative full path、deterministic UTF-8 stable sort，并按 exact R40–R50 report paths 与 Batch E 的 frontend/next-env.d.ts 进行分类：

| Observation | Result |
| --- | ---: |
| raw untracked count | 312 |
| normalized unique count | 312 |
| duplicate count | 0 |
| Batch D | 300 |
| Batch E | 1 |
| R40–R50 reports | 11 |
| unknown | 0 |
| missing expected R40–R50 | 0 |
| missing expected Batch E | 0 |

R51 写入后 expected composition 为：

    Batch D 300 + Batch E 1 + R40–R51 12 = 313
    unknown 0
    missing 0

Batch D/E 在本轮未打开、删除、移动、stage 或 reclassification。

## 5. Exact reviewed input identities

所有 required input 均为 readable、regular、NON-SYMLINK；以下 bytes/SHA-256 是 live checkout identity。R42–R50 与 Prompt expected identities 全部匹配。

### 5.1 Governance / PM inputs

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| docs/thread_handoff/pm_operating_rules.md | 49170 | a692fdafbdea8c63d184cb11548e73731aefccd3110818004b028ba7ee9fe7f5 |
| docs/current_status.md | 150180 | ee7126fd20f1774f54cee9b238cab4e3e0943bce854402b1594060212f88cc23 |
| docs/thread_handoff/chatgpt_pm_handoff_260730-1203.md | 26183 | c9a7ed7283d4574578e1608fc6891bdb91373d97bac3191740863917af3ad8e1 |

### 5.2 R42–R50 report inputs

| Report | Bytes | SHA-256 |
| --- | ---: | --- |
| R42 docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md | 32319 | dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165 |
| R45 docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md | 13786 | 8fd646f24565bbcb27aa9063038774fee3b5398d66566f961bee296ffff02ef2 |
| R43 docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md | 30244 | 95b2e63c4879fb5af6920b262300566c577612dd1753b13bf59928c1417338e8 |
| R44 docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md | 43036 | 3b4d1f3451d0b0036e5530bc83eb35b90ee2b6d140b0a2799b82df1ada035bfa |
| R46 docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md | 23703 | f460fef43d975de41ed624fa49d8a1a8dcd5246b4ae55b222189f40703914b81 |
| R47 docs/reports/sprint4_d2_r7b_i1_r47_runtime_loaded_observability_verification_planning_review.md | 34592 | 4de247e350eb595077219856cf63b0319ee83d14026b6beaaf7c5d83211a0ae4 |
| R48 docs/reports/sprint4_d2_r7b_i1_r48_runtime_loaded_observability_implementation.md | 15692 | caa3203630c5b321c950d078fda7424f4f1ca8edcd7f4a45b88525adfdda0d10 |
| R49 docs/reports/sprint4_d2_r7b_i1_r49_pre_record_db_connection_ordering_repair.md | 11749 | 5d09732094f3266eccc34a002b0203a3889f33be1c6b56568c43b42c50618dde |
| R50 docs/reports/sprint4_d2_r7b_i1_r50_independent_reliability_implementation_review.md | 34024 | 40cfc45b6fcc756a15f2e550b8d7b051a4d797a6bd8c72da1d6b2fb0aa9941d9

### 5.3 Current implementation / review inputs

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| collector/app/main.py | 2525 | d1a461294c91f9f86cde4af87b21bb1147bed5561d64028e8462a8f57d46de80 |
| collector/app/services/event_collector.py | 24313 | 02cab6ea15572ae0b2f6059462f9cd6856cd483ab0dcc37c87d39267aad1e8e2 |
| collector/app/plc/mapping.py | 18876 | ba39583a699f8347c0ff5eaec2e7c807dad909c815269de607a36e8b93c023a7 |
| collector/app/services/storage.py | 38319 | f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b |
| collector/tests/test_event_collector_reliability.py | 32253 | fa8a677f5a249b849438b7ec43e2bbd14ff14e8c590e54d02274daa640b06835 |
| tests/test_collector_station_event_runtime_source.py | 33212 | 7b5b77f40c5bc3eff1a364064876ed79d0d28ffa5bf5f25ee9ba279498d409cd |

## 6. Effective contract interpretation

R42 controls base application implementation. R45 supersedes R42 only for：

| Subject | Effective authority |
| --- | --- |
| canonical line_id and selected routing-line equality | R45 |
| later source/image/config/process terminal binding | R45 |
| later raw-log/payload/parsed-evidence identity | R45 |
| all other runtime-loaded application fields and lifecycle | unchanged R42 |

R43 accepted the unchanged Reliability mechanisms; R46 accepted the focused Data Quality closure of DQ-B1/B2/B3; R47 accepted deterministic Verification planning. R45 does not authorize current source expansion or A–H artifact creation.

R44 historical blocker supersession：

- DQ-B1 historical ambiguity is closed by canonical ResolvedConfigSnapshot line authority plus emission-before-success routing equality.
- DQ-B2 historical source/image/config/process gap is deferred to later independently authorized runtime validation.
- DQ-B3 historical parsed-only/raw-normalized evidence gap is deferred to later independently authorized Verification/runtime evidence.
- Absence of A–H artifacts, active image identity, process identity or current container mapping is therefore not a current application implementation HOLD.

## 7. R48 + R49 + R50 package state distinction

| State | R48 | R49 | R50 / current PM boundary |
| --- | --- | --- | --- |
| source/test files | WRITTEN | WRITTEN with bounded pre-record ordering repair | current persisted package |
| local validation | TESTED | TESTED | re-run in this R51 and PASS |
| PM state | PM-ACCEPTED for independent review | PM-ACCEPTED | R50 result PM-ACCEPTED; R50 report itself remains WRITTEN |
| Reliability review | not established before R50 | not established before R50 | RELIABILITY-REVIEWED / PASS WITH RECOMMENDATIONS |
| Data Quality review | not established | not established | this R51 is the current DQ review |
| Git | not staged / committed / pushed | not staged / committed / pushed | remains not staged / committed / pushed |
| build/deploy/runtime | not established | not established | not established |

状态边界：

    WRITTEN ≠ TESTED ≠ PM-ACCEPTED ≠ RELIABILITY-REVIEWED
    RELIABILITY-REVIEWED ≠ DATA-QUALITY-REVIEWED
    DATA-QUALITY-REVIEWED ≠ VERIFICATION-REVIEWED
    REVIEWED ≠ STAGED ≠ COMMITTED ≠ PUSHED
    PUSHED ≠ BUILT ≠ DEPLOYED ≠ ACTIVATED
    ACTIVATED ≠ RUNTIME-LOADED ≠ PRODUCTION-ACCEPTED

## 8. Same-byte mapping read chain

Current load_edge_mapping implementation is at collector/app/plc/mapping.py:143-160.

链路为：

    exact input path
    → reject final symlink
    → resolve strict canonical path
    → regular-file check
    → one canonical_path.read_bytes()
    → SHA-256(raw_bytes)
    → raw_bytes.decode("utf-8")
    → yaml.load(decoded_text, UniqueKeySafeLoader)
    → parse_edge_mapping(raw)
    → bind mapping_path and mapping_content_sha256 to returned EdgeMapping

独立 AST audit 结果：

| Check in load_edge_mapping | Result |
| --- | ---: |
| read_bytes calls | 1 |
| read_text calls | 0 |
| SHA-256 calls | 1 |
| decode calls | 1 |
| YAML load calls | 1 |

同一 raw byte sequence 被 hash、decode 和 parse。parse_edge_mapping() 接收已经加载到内存的 raw mapping，不再读取 path；没有 second mapping read、text re-encode hash、newline-normalized hash 或 substituted parsed path。

invalid UTF-8 在 decode 阶段失败；malformed YAML、duplicate YAML key、root type或 semantic contract failure均在 success record 前失败。

## 9. Raw identity 与 semantic identity separation

### 9.1 mapping_content_sha256

mapping_content_sha256 在 mapping.py:150-151 直接由 exact raw bytes 计算：

    hashlib.sha256(raw_bytes).hexdigest()

因此它代表 exact file-byte identity，包括换行、编码和原始 byte layout。它不是 path string、decoded text 的重编码 hash，也不是 semantic snapshot hash。hexdigest 本身为 lowercase 64-hex；EventCollectorWorker 在 event_collector.py:136-137 再执行 canonical regex 检查。

### 9.2 resolved_config_hash

resolved_config_hash 的 authority 是 RuntimeMappingSnapshot.config_hash。mapping.py:242-260 构造 hash-bound snapshot；mapping.py:282-290 使用 deterministic JSON semantic content、sort_keys=True、compact separators、allow_nan=False，再对 UTF-8 encoded semantic snapshot 做 SHA-256。该 content 包含 schema/config/source/line/timezone/hash namespace、decoder registry identity、route graph、interpretation code tables 和 station projections，并对 route/stations采用稳定排序。

EventCollectorWorker 在 event_collector.py:138-148 验证 runtime snapshot 与 ResolvedConfigSnapshot 的 content hash consistency，并要求 resolved hash 为 lowercase 64-hex。

### 9.3 Separation ruling

| Identity | Actual authority | Meaning | Can replace the other? |
| --- | --- | --- | --- |
| mapping_content_sha256 | one exact raw byte read | raw file identity | no |
| resolved_config_hash | deterministic semantic/resolved snapshot | interpreted configuration identity | no |
| record field | application assertion of both | value to compare later | neither is expected authority |

Focused test test_semantically_same_mapping_bytes_have_distinct_raw_sha_but_same_resolved_hash proves a newline-only raw change changes raw SHA while preserving semantic hash. No copying or substitution between the two hashes exists in the persisted implementation.

## 10. Internally consistent initialization chain

Current worker constructor order at event_collector.py:77-130 is：

    mandatory startup context consume
    → load_edge_mapping
    → raw/runtime/resolved identity validation
    → exact PLC selection and routing-line check
    → timezone and resolved registry construction/lookup
    → Snap7 client object construction only
    → complete read-plan list construction
    → list-first duplicate/cardinality/scope validation
    → dict conversion
    → line and configured station runtime materialization
    → exact record serialization
    → one logger emission
    → constructor return

R49 ordering preserves the record boundary：

    main startup context and non-DB setup
    → EventCollectorWorker constructor and record
    → Thread construction/start
    → legacy main-loop Storage(database_url())
    → worker run_forever Storage(self.dsn)
    → first poll_once / PLC and DB operations

main.py:25-47 and event_collector.py:220-235 show no DB Storage construction before the record on the enabled path. R50 verified Storage constructor-call/order with explicit spies; storage.py:18-20 remains the real psycopg.connect boundary, but it is reached only after Thread.start or at worker run_forever entry.

No local review, fake test or AST result is being represented as deployed process, active image, current container mapping, raw container log, real DB/PLC evidence, RUNTIME-LOADED or PRODUCTION-ACCEPTED.

## 11. Canonical line_id and routing projection

R45 + R46 current rule：

    canonical_line_id = resolved_config_snapshot.line_id
    equivalent origin = mapping.runtime_snapshot.line_id
    record line_id = canonical snapshot line
    selected PLC line_id = routing projection only

Current implementation:

- event_collector.py:100-107 requires exactly one selected PLC entry, a non-empty string routing line_id and exact equality with the resolved snapshot line;
- event_collector.py:105 and 203 use resolved snapshot line for worker/application record;
- self.line_id remains the runtime projection used by later existing collector paths;
- mismatch, missing, empty or ambiguous selected routing identity fails before serialization.

This prevents unchecked PLC routing projection from becoming semantic line authority. It preserves existing first-selected routing/product boundary and does not add multi-PLC behavior.

## 12. List-first read-plan and count authority

Current implementation retains all values before dict conversion：

    configured_station_ids = [station.station_id for station in self.mapping.stations]
    expected_scopes = ["line", *configured_station_ids]
    generated_scopes = [plan.scope for plan in plans_list]

Validation before dict conversion rejects：

- reserved configured station ID line；
- duplicate configured station IDs；
- duplicate generated scopes；
- cardinality mismatch；
- expected/generated scope multiset mismatch；
- missing or extra scopes；
- anything other than exactly one line plan；
- non-positive complete plan list。

Only after these checks does code build plans = {plan.scope: plan for plan in plans_list}. station_runtimes is then materialized once per configured station and its length is checked. Disabled configured stations are not filtered; they remain in mapping.stations, expected_scopes, generated plans and read_plan_count.

The emitted read_plan_count is len(plans_list) after this validation. It is not derived from the post-conversion dictionary and cannot hide duplicate/missing/extra scopes through dict overwrite.

## 13. Exact v1 record object

Current emitted object literal is in event_collector.py:196-208. AST literal-key audit found exactly these 11 keys：

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

Field and serialization checks：

- no missing or extra key in the emitted object;
- evidence_schema_version is exactly edge-mes/collector-runtime-loaded/v1;
- event_type is exactly collector_runtime_loaded;
- mapping_content_sha256 and resolved_config_hash are lowercase 64-hex;
- process_pid and read_plan_count are positive integer and explicitly reject boolean;
- collector_main_started_at_utc is emitted by the main context generator as UTC with literal Z;
- JSON is deterministic, compact, UTF-8-capable, allow_nan=False and one-line;
- logger is invoked once with collector_runtime_loaded_json=<JSON_OBJECT>;
- no optional scope list、record_emitted_at、image/container/Git/raw artifact fields.

Focused reliability test test_worker_emits_one_exact_record_before_constructor_returns asserts exact key-set, literals, line, timestamp, compact serialization, hash regex, integer/non-boolean types and prohibited substrings.

## 14. Per-field authority matrix

| Field | Current actual source | Expected future authority | Truth role |
| --- | --- | --- | --- |
| evidence_schema_version | frozen constant RUNTIME_LOADED_EVIDENCE_SCHEMA_VERSION | R42/R45 frozen literal | application assertion; not production schema |
| event_type | frozen constant RUNTIME_LOADED_EVENT_TYPE | R42/R45 frozen literal | application assertion; not production event |
| mapping_path | EdgeMapping.mapping_path bound by load_edge_mapping to canonical exact path; main default is /app/config/mapping.yaml | approved deployment path plus fresh active-container mount observation | path assertion/projection; not content authority |
| mapping_content_sha256 | SHA-256 of the single raw byte sequence read by load_edge_mapping | fresh SHA-256 of current active-container-visible exact mapping bytes, bound to accepted deployment | raw-byte identity assertion; not expected authority |
| mapping_schema_version | EdgeMapping.schema_version from parsed YAML and same snapshot projection | independent parse of exact authoritative active mapping bytes | hash-bound mapping projection; not production schema |
| config_version | EdgeMapping.config_version from parsed YAML and same snapshot projection | independent parse of exact authoritative active mapping bytes | hash-bound configuration projection |
| line_id | ResolvedConfigSnapshot.line_id, with selected PLC routing line equality checked before emission | independent parse of active mapping bytes using canonical snapshot line rule | canonical line assertion/correlation; not production line fact |
| read_plan_count | len(plans_list) after complete list-first validation and before dict conversion | independently derive one line plus every configured station, including disabled | validated plan-count assertion; not station-event count |
| resolved_config_hash | RuntimeMappingSnapshot / ResolvedConfigSnapshot deterministic semantic hash | independently recompute semantic hash from exact active mapping bytes using accepted algorithm/source | semantic identity assertion; not self-expected authority |
| collector_main_started_at_utc | capture_startup_context() at main.py:18-22 | fresh container StartedAt and bounded observation time | application time assertion/correlation; not event time |
| process_pid | os.getpid() captured at main.py:18-22 and consumed once | fresh active Collector main PID in the same process/container namespace | process correlation assertion; not production actor identity |

All record values are assertions to compare. No self-reported record field is used as expected-value authority.

## 15. Self-referential expected-value rejection

The current implementation creates the record from loaded application objects, but no local test or source code treats the serialized record as its own expected source. The later non-self-referential expected matrix is：

- schema/event: frozen contract literals；
- mapping path: approved deployment contract plus fresh active mount；
- raw mapping SHA: fresh exact active-container bytes；
- mapping schema/config/line: independent parse of those bytes；
- read-plan count: independent list-first derivation including disabled stations；
- resolved hash: independent semantic recomputation or separately pre-frozen accepted algorithm/value bound to the exact bytes；
- PID/time: fresh process/container observations；
- source/image: accepted source manifest and full image IDs；
- raw log lineage: exact raw artifact → selected line → application message → payload → parsed object。

Historical mapping hashes, tags, Config.Image, short IDs, manual/static observations and record self-report are rejected as expected authority. This later chain is a future gate; it is not claimed as currently observed.

## 16. Prohibited, secret and production-field audit

The exact v1 JSON has no：

- DSN、credential、host、port or database connection detail；
- PLC raw bytes、station payload、unit/DMC、production event or machine state；
- DB result、accepted station-event fact、NOK/detail production fact；
- ACK、read_done、retry、collector health or worker health；
- image ID、container ID、Git identity、deployment or runtime acceptance claim。

The DSN remains an internal worker attribute for later run_forever Storage construction; it is not placed in the record or success application message. PLC/DB/accepted-fact/ACK/read_done calls remain in poll/runtime paths after record and are not part of v1 record authority.

R50 explicit Storage ordering review confirms that pre-record source setup only constructs non-DB source objects; real Storage connection is later. The local FakeStorage/FakeClient tests are synthetic local oracles only.

## 17. Runtime metadata versus production truth

The v1 record means only：

    current application startup asserted that required mapping,
    resolved semantic snapshot and complete read-plan initialization
    succeeded before Thread.start and worker PLC/DB/ACK activity.

It does not mean：

    worker thread healthy
    PLC connected or read
    DB reachable or written
    accepted fact generated or persisted
    ACK/read_done completed
    machine state or production event observed
    image/container/deployment accepted
    RUNTIME-LOADED accepted
    PRODUCTION-ACCEPTED

The current product state remains ACTIVATED = YES and STATIC_MAPPING_INITIALIZED = YES, while RUNTIME-LOADED and PRODUCTION-ACCEPTED remain NO. No local/static/manual/fake result is represented as deployed/runtime/production truth.

## 18. DQ-B1 current implementation closure

DQ-B1 is closed at current implementation level：

- canonical line is the hash-bound resolved snapshot line；
- selected PLC line is only a routing projection；
- exact equality is required before serialization/emission；
- the record writes canonical snapshot line；
- missing, empty, ambiguous or mismatched routing identity fails closed；
- the check does not change PLC, DB, accepted-fact or ACK/read_done semantics。

Focused oracle coverage includes equal, mismatch, missing, empty and ambiguous routing cases. No current cross-line false PASS blocker remains.

## 19. DQ-B2 later source/image/config/process boundary

DQ-B2 remains a later runtime evidence responsibility, not a current application artifact requirement. The required later chain is：

    accepted implementation source/path manifest
    → accepted built/deployed full image ID
    → fresh active full image ID
    → fresh active full container ID + StartedAt
    → fresh active Collector main PID/process identity
    → fresh active-container mapping bytes
    → emitted raw/semantic hashes
    → parsed v1 record

Tags, Config.Image, short IDs, hostname, historical mapping hash and record self-report are not expected authority. Current application package must not add image/container/Git fields, source manifest fields, Docker API, remote filesystem access or deployment artifacts. The absence of this later chain in current checkout is not a current-gate HOLD.

Classification：future runtime evidence task。

## 20. DQ-B3 later A–H raw/payload/parsed lineage boundary

DQ-B3 also remains later Verification/runtime evidence responsibility. A future bounded validator must retain, under a separately authorized exact artifact allowlist：

- A raw transport artifact with current full-container-ID scope, interval, length and SHA-256；
- B observation metadata with authority, image/container/process/start identity and raw binding；
- C selected raw-line bytes/offset or stable ordinal；
- D exact application-message bytes；
- E exact JSON payload bytes after the single delimiter；
- F parsed exact v1 object；
- G per-field expected/actual/lineage terminal comparison；
- H final manifest binding A–G after validation。

Raw bytes must be preserved before parse/selection normalization; exact payload bytes must not be trimmed, normalized or replaced by reserialized JSON. Duplicate JSON members, bool-as-integer, numeric strings, missing/extra keys and malformed/partial/ambiguous records must fail closed in the future parser.

Current application package does not need to create A–H artifacts, choose future filenames or add a parser/telemetry/retention subsystem. No future filename was selected in this R51 review.

Classification：future runtime evidence task。

## 21. Focused test-oracle assessment

### 21.1 Current source/mapping oracles

The current focused tests provide credible current implementation oracles：

| Required case | Current evidence | Ruling |
| --- | --- | --- |
| second mapping read | Path.read_bytes count is asserted as one; AST sees one read_bytes in loader | covered for current implementation |
| hash and parse use same bytes | YAML loader input is asserted equal to raw_bytes.decode("utf-8"); raw SHA is asserted over raw_bytes | covered |
| invalid UTF-8 / malformed YAML | explicit fail-closed fixture | covered |
| raw bytes change but semantic hash stable | newline-only raw change gives different raw SHA and same resolved hash | covered |
| duplicate/missing/extra scope | duplicate plan, missing plan, extra/multiset mismatch and duplicate configured station tests | covered |
| canonical/routing mismatch | mismatch, missing, empty and ambiguous routing tests | covered |
| missing/extra record key | exact emitted key-set assertion detects both | covered |
| wrong hash/type/literal | hash regex, integer/non-boolean checks and exact schema/event literals | covered |
| disabled configured station authority | disabled station remains in read_plan_count | covered |
| local/static/manual/production truth confusion | tests use fake/local paths and assert no production/ACK/read_done message leakage; reports retain local/runtime boundary | current package does not claim runtime/production truth; later external oracle remains separate |

Key focused tests：

    tests/test_collector_station_event_runtime_source.py:159
    tests/test_collector_station_event_runtime_source.py:187
    tests/test_collector_station_event_runtime_source.py:201
    tests/test_collector_station_event_runtime_source.py:213
    collector/tests/test_event_collector_reliability.py:391
    collector/tests/test_event_collector_reliability.py:441
    collector/tests/test_event_collector_reliability.py:451-489
    collector/tests/test_event_collector_reliability.py:545-563
    collector/tests/test_event_collector_reliability.py:582-608
    collector/tests/test_event_collector_reliability.py:610-744

### 21.2 R49/R50 ordering oracle

R49/R50 added and independently reviewed explicit Storage constructor-call/order oracle：

    record
    → thread_construct
    → thread_start
    → legacy_storage_construct

and：

    worker storage_construct
    → poll_once

Storage initialization failure is observed once, propagated, with no retry/poll/re-emission. This closes the previous R48 pre-record DB connection concern without changing current Data Quality record contents.

### 21.3 Blind spots and boundary

The focused tests do not and should not establish：

- active image/container/process identity；
- current container-visible mapping bytes；
- raw container log transport or A–H artifact lineage；
- real DB/PLC evidence；
- RUNTIME-LOADED or PRODUCTION-ACCEPTED.

Those are later independent runtime/Verification responsibilities. The strict RFC3339 negative fixture is not present as a current negative test, but the only main-generated timestamp path is canonical UTC Z; this is classified as Verification carry-forward, not a current false-PASS blocker. No source/test repair is authorized.

## 22. R50 strict RFC3339 negative-fixture recommendation

R50 recommended a negative fixture for an explicitly hand-built CollectorStartupContext that is parseable by fromisoformat but not the frozen strict RFC3339 grammar.

Assessment：

- classification: Verification carry-forward；
- necessity for current gate: not necessary；
- current source behavior: main.py:20 uses datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), producing UTC Z with T;
- current consume path checks string、Z suffix、UTC parse and PID;
- no current main-generated false PASS was found；
- no source/test modification is made in R51；
- later parser/validator must remain strict at the runtime evidence gate。

升级为 current-gate blocker 的条件未满足：没有证据表明 current main-generated timestamp can produce a credible Data Quality false PASS under the current claim.

## 23. Validation commands and fresh results

### 23.1 Exact py_compile

执行的 exact command：

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile \
      collector/app/main.py \
      collector/app/services/event_collector.py \
      collector/app/plc/mapping.py \
      collector/tests/test_event_collector_reliability.py \
      tests/test_collector_station_event_runtime_source.py

结果：PASS，exit code 0。

### 23.2 Exact focused pytest A

执行的 exact command：

    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=collector:. \
    .venv/bin/python -m pytest \
      collector/tests/test_event_collector_reliability.py \
      -q

结果：PASS，24 passed，8 subtests passed，0 failures，exit code 0。

### 23.3 Exact focused pytest B

执行的 exact command：

    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=collector:. \
    .venv/bin/python -m pytest \
      tests/test_collector_station_event_runtime_source.py \
      -q

结果：PASS，56 passed，0 failures，exit code 0。

两个 pytest command 均分别完整运行；未使用 -k、skip、xfail、reduced selection、broad suite、coverage；未启动应用，未连接真实 DB/PLC/network/remote。

## 24. Source/test mutation、cached 与 diff-check audit

验证后、R51 write 前：

    git diff --name-only
    collector/app/main.py
    collector/app/plc/mapping.py
    collector/app/services/event_collector.py
    collector/tests/test_event_collector_reliability.py
    tests/test_collector_station_event_runtime_source.py

    git diff --cached --name-only
    empty

    git diff --check
    PASS

    git diff --cached --check
    PASS

六个 reviewed implementation inputs 与 expected bytes/SHA-256 unchanged。五条 source/test dirty set 与 recovery baseline一致。R51 在 write 前 ABSENT；此前没有 report mutation。

## 25. Forbidden-action counters

| Action | Count |
| --- | ---: |
| source/test/config/contract/status/roadmap/handoff modification | 0 |
| R48/R49/R50 modification | 0 |
| unauthorized helper/fixture/manifest/raw-log/sidecar/A–H artifact | 0 |
| Git add/stage/commit/push/tag | 0 |
| reset/restore/checkout/stash/clean/delete/move/merge/rebase/cherry-pick | 0 |
| build/package/dependency installation | 0 |
| Docker/Compose/lifecycle | 0 |
| network/SSH/curl/remote | 0 |
| real DB connection/query/write/migration | 0 |
| PLC/V-PLC connection/read/write | 0 |
| application startup/runtime validation | 0 |
| A–H evidence generation | 0 |
| accepted-fact/production event/ACK/read_done activity | 0 |
| Batch D/E open/delete/move/stage/reclassification | 0 |

授权的 py_compile 与 focused pytest 是 local validation only；它们不改变以上 truth boundary。

## 26. Finding matrix and necessity classification

| Finding / candidate | Classification | R51 disposition |
| --- | --- | --- |
| recovery/input identity drift | current-gate blocker | none; all recovery gates matched |
| same-byte mapping read/hash/decode/parse failure | current-gate blocker | none; implementation and oracle PASS |
| raw SHA / semantic hash conflation | current-gate blocker | none; distinct code paths and focused test PASS |
| canonical line replaced by unchecked routing line | current-gate blocker | none; equality is required before emission |
| duplicate/cardinality/scope hidden by dict conversion | current-gate blocker | none; list-first validation is before dict conversion |
| missing/extra/wrong-type/literal v1 record | current-gate blocker | none; exact record and focused oracle PASS |
| secret/production/ACK/read_done leakage into v1 | current-gate blocker | none; prohibited-field audit PASS |
| local/static/fake evidence represented as runtime/production truth | current-gate blocker | none; package/reports keep boundary explicit |
| R50 strict RFC3339 negative fixture | Verification carry-forward | no current repair; later negative fixture/validator review |
| later source/image/config/process identity chain | future runtime evidence task | later independent gate; not current source expansion |
| later A–H raw/payload/parsed lineage | future runtime evidence task | later independent Verification/runtime gate; no current artifact |
| current application should choose future A–H filenames | unnecessary / duplicate / scope expansion | rejected |
| record_emitted_at、sorted scope list、generic telemetry、retention、audit/forensics、hostile same-process anti-forgery | unnecessary / duplicate / scope expansion | rejected |
| current source/test repair | current-gate necessary repair | none |
| new Reliability re-review | unnecessary for this gate | R50 already accepted; no Reliability mechanism changed |

## 27. Blockers

Current Data Quality blockers：none。

Current-gate necessary repair：none。

本轮没有触发 HOLD。尤其没有发现：

- second mapping read or different bytes for hash versus parse；
- raw SHA derived from normalized/re-encoded text；
- raw and semantic hash conflation；
- unchecked routing line replacing canonical line；
- duplicate/missing/extra plan scope hidden by dict conversion；
- missing/extra/wrong-type v1 key set under the reviewed current record;
- boolean accepted as PID/count；
- record self-report used as expected authority；
- DSN/credential/PLC/DB/ACK/read_done/production field leakage；
- local/static/fake evidence represented as deployed/runtime/production truth；
- R45 later evidence absence incorrectly repaired through current source expansion；
- validation failure or source/test mutation；
- cached non-empty or unknown untracked path.

## 28. Recommendations and necessity

1. Strict RFC3339 negative fixture：Verification carry-forward，bounded and non-blocking。仅在 later Verification/runtime validator scope中执行；不修改 current source/test。
2. Source/image/config/process binding：future runtime evidence task。保持在 separately authorized build/deploy/runtime gate；不向 v1 record添加 image/container/Git fields。
3. A–H raw/payload/parsed evidence：future runtime evidence task。future Prompt 必须选择 exact artifact paths；R51 不选择文件名、不创建 artifact。
4. record_emitted_at、sorted scope list、generic telemetry、retention、audit/forensics、hostile same-process anti-forgery：unnecessary / duplicate / scope expansion；不创建新任务。
5. R50 first-context-consumer-after-failure recommendation：已被 R50 current focused test test_constructor_failure_consumes_context_and_prevents_retry 覆盖；本轮分类为 unnecessary / duplicate，不重复开 repair。

Recommendations 不改变 R51 conclusion，不授权 Verification execution、Git、build、Docker、remote、runtime validation 或 production acceptance。

## 29. Product / evidence boundary

R51 只能得出：

    current local persisted implementation package
    = source WRITTEN
    + focused tests TESTED
    + Reliability-REVIEWED by R50
    + Data-Quality-REVIEWED by this R51 report when PM accepts it

R51 不能得出：

    accepted implementation commit
    accepted image
    deployed process
    current container-visible mapping
    raw container log
    real DB or PLC evidence
    RUNTIME-LOADED
    PRODUCTION-ACCEPTED

Current product state remains：

    ACTIVATED = YES
    STATIC_MAPPING_INITIALIZED = YES
    RUNTIME-LOADED = NO
    PRODUCTION-ACCEPTED = NO

## 30. MVP 路径一致性

分类：MVP-ALIGNED WITH BACKLOG ITEMS。

approved MVP deliverable：在不改变 PLC、DB、accepted-fact、ACK/read_done 或 production semantics 的前提下，为 Collector runtime-loaded mapping/config initialization claim 建立最小可审查的 application record 与 local implementation oracle。

本轮最小 terminal invariant：

    exact raw mapping bytes are loaded once and bound to raw SHA/decode/parse;
    semantic resolved hash is distinct and deterministic;
    complete validated read-plan scope is bound to the count;
    canonical line equals selected routing projection before emission;
    exact 11-key record does not leak production or runtime-acceptance claims.

本轮没有新增 API、DB schema/migration、telemetry、generic audit/forensics、retention、cryptographic provenance、hostile same-process subsystem、runtime topology、image/container fields或production capability。后续最小动作仍是 PM durable intake，再由 PM 单独发布 independent Verification implementation review authority；不是继续扩大本 Thread。

## 31. Thread 输出 / 上下文评估

本次输出长度：长 durable report。

当前 Thread 是否建议继续：no。

下一轮是否建议新开 Thread：yes。

理由：R51 Data Quality implementation review authority 在本报告写入后 terminalized；下一阶段若 PM 接受且无 blocker，应使用独立 Verification implementation review authority，不能继承本 Thread authority或R50 Reliability authority。

## 32. Exact next gate and stop point

    R51 independent Data Quality implementation review WRITTEN
    → ChatGPT PM durable intake
    → if and only if PM accepts R51 and no blocker:
      independent Verification implementation review
    → stop before any Git/build/Docker/remote/runtime/production action

R51 不自动授权：

    repair
    Git candidate/stage/commit/push/tag
    build
    Docker/Compose
    deploy/lifecycle
    remote/SSH
    runtime validation
    A–H evidence
    RUNTIME-LOADED
    PRODUCTION-ACCEPTED

## 33. Final state vocabulary

    source: WRITTEN in current dirty checkout
    tests: TESTED by exact focused commands
    R48: WRITTEN / TESTED / PM-ACCEPTED FOR INDEPENDENT REVIEW
    R49: WRITTEN / TESTED / PM-ACCEPTED
    R50: RELIABILITY-REVIEWED / PASS WITH RECOMMENDATIONS / WRITTEN report
    R51: DATA-QUALITY-REVIEWED / PASS WITH RECOMMENDATIONS / WRITTEN report
    STAGED: NO
    COMMITTED: NO
    PUSHED: NO
    BUILT: NO
    DEPLOYED: NO
    ACTIVATED: YES as prior product boundary
    RUNTIME-LOADED: NO
    PRODUCTION-ACCEPTED: NO

## 34. Final report identity and stop

R51 report path must remain regular UTF-8, NON-SYMLINK, UNSTAGED and UNTRACKED. Its final bytes and SHA-256 are intentionally omitted from this file to avoid self-reference and will be returned only by the post-write detached audit.

End state：PASS WITH RECOMMENDATIONS / DATA-QUALITY-REVIEWED / WRITTEN ONLY.

完成 exact R51 report write后，执行唯一 post-write detached read-only audit并立即停止。
