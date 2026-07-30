# Sprint 4 D2-R7B-I1 R44 Process-Bound Runtime-Loaded Observability Data Quality Review

## 1. 报告身份、authority 与 terminal decision

- 报告名称：Sprint 4 D2-R7B-I1 R44 Process-Bound Runtime-Loaded Observability Data Quality Review
- 任务名称：D2-R7B-I1 R44 — Independently Review R42 Runtime-Loaded Evidence Truth, Lineage and Field Authority
- 执行 Thread：Data Quality
- Authority source / ID：PM-D2-R7B-I1-R44-PROCESS-BOUND-RUNTIME-LOADED-DATA-QUALITY-REVIEW-260730-0958
- Delivery：REPOSITORY_DURABLE_REPORT
- 唯一输出路径：docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md
- Authority properties：AUTHORIZED ONCE / INDEPENDENT DATA QUALITY REVIEW / LOCAL DOCS WRITE ONLY / NO REPAIR / NO SOURCE OR TEST WRITE / NO RUNTIME AUTHORITY / NOT REUSABLE

Terminal decision：

    HOLD / DATA_QUALITY_BLOCKER_REQUIRES_PM_SCOPE_REASSESSMENT
    NEW BLOCKER CLASS — PM SCOPE/ASSURANCE REASSESSMENT REQUIRED

本报告只审查 R42 candidate contract 的 fact authority、raw-to-semantic-to-record lineage、expected-value authority、evidence classification 与 future Verification planning sufficiency。没有修改 R42/R43、source、test、config、Dockerfile、Compose、status、roadmap、handoff 或 PM rules。

Evidence boundary：

    DATA-QUALITY-REVIEWED
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

## 2. Scope、precedence 与读取边界

本轮按 authority precedence 解释事实：live Git recovery；current PM Prompt；docs/thread_handoff/chatgpt_pm_handoff_260730-0834.md；R35/R36 committed durable evidence；PM-verified R42/R43 exact inputs；recent Git history；旧 current_status.md / roadmap.md sections。

按 Prompt 顺序读取了：

1. docs/thread_handoff/pm_operating_rules.md
2. docs/current_status.md
3. docs/roadmap.md
4. docs/thread_handoff/chatgpt_pm_handoff_260730-0834.md
5. docs/reports/sprint4_d2_r7b_i1_r31_package_closed_collector_image_materialization_deployment_plan.md
6. docs/reports/sprint4_d2_r7b_i1_r35_phase5_post_activation_validation.md
7. docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/local_prerequisite_terminal.json
8. docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/post_activation_terminal.json
9. docs/reports/evidence/d2_r7b_i1_r35_phase5_post_activation_validation/manifest.sha256
10. docs/reports/sprint4_d2_r7b_i1_r36_working_tree_hygiene_authority_materialization_plan.md
11. docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/authority_materialization_plan.json
12. docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md
13. docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md
14. collector/app/main.py
15. collector/app/services/event_collector.py
16. collector/app/plc/mapping.py
17. collector/app/plc/read_plan.py
18. collector/app/services/resolved_config_registry.py
19. config/mapping.yaml
20. collector/Dockerfile
21. docker-compose.yml
22. collector/tests/test_event_collector_reliability.py
23. tests/test_collector_station_event_runtime_source.py

R40/R41 仅作为 R36 expected untracked paths；本轮没有读取、评审、重新分类或处理 Batch D/E。

## 3. Fresh Git recovery 与 R44 output boundary

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
| initial untracked count | 305 |
| R44 before write | ABSENT / NON-SYMLINK / UNTRACKED / UNSTAGED |

使用 R36 authority_materialization_plan.json 的 exact Batch D/E paths 与 R40/R41/R42/R43 四个 exact paths 组成 UTF-8 稳定排序 expected set，和 live git ls-files --others --exclude-standard 精确比较：

    expected count: 305
    live count: 305
    unknown paths: 0
    missing expected paths: 0
    composition: Batch D 300 + Batch E 1 + R40 1 + R41 1 + R42 1 + R43 1

本轮没有 git add、stage、commit、push、tag、restore、reset、stash、clean、delete、move、archive 或 cleanup。

## 4. Active input identities 与 accepted boundary

### 4.1 R42

| Field | Value |
| --- | --- |
| path | docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md |
| bytes | 32319 |
| SHA-256 | dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165 |
| file | UTF-8 regular file / NON-SYMLINK |
| index | UNSTAGED / UNTRACKED / NOT COMMITTED |
| state | REPAIRED CONTRACT WRITTEN / PM-REVIEWED / PM-VERIFIED / PM-ACCEPTED AS CANDIDATE CONTRACT |

### 4.2 R43

| Field | Value |
| --- | --- |
| path | docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md |
| bytes | 30244 |
| SHA-256 | 95b2e63c4879fb5af6920b262300566c577612dd1753b13bf59928c1417338e8 |
| file | UTF-8 regular file / NON-SYMLINK |
| index | UNSTAGED / UNTRACKED / NOT COMMITTED |
| state | RE-REVIEWED / WRITTEN / PM-REVIEWED / PM-VERIFIED / PASS ACCEPTED |

### 4.3 R35/R36 boundary

R35：3002 bytes，SHA-256 133c303e6a556b4be9e2c9535a10ff3b5a9dd06bf5b6f3fca1f272d707b75ee0；其 local/post terminal 与 manifest 均为已接受历史 evidence。R35 只证明 ACTIVATED 与 STATIC_MAPPING_INITIALIZED，仍明确 RUNTIME-LOADED = NO、PRODUCTION-ACCEPTED = NO。

R36 authority facts：Batch D historical review 300、Batch E frontend/next-env.d.ts 1；R36 不授权本轮处理它们。

当前 PM-accepted product boundary：

    ACTIVATED                  = YES
    STATIC_MAPPING_INITIALIZED = YES
    RUNTIME-LOADED             = NO
    PRODUCTION-ACCEPTED        = NO

## 5. Current source identity table

以下是 live worktree bytes 的 SHA-256；全部为 regular NON-SYMLINK，相对 HEAD 的 tracked diff 与 cached diff 均为空。

| Path | Bytes | SHA-256 | HEAD relation |
| --- | ---: | --- | --- |
| collector/app/main.py | 2073 | a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090 | CLEAN |
| collector/app/services/event_collector.py | 16342 | eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f | CLEAN |
| collector/app/plc/mapping.py | 17433 | c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098 | CLEAN |
| collector/app/plc/read_plan.py | 1482 | fd5f675501444ed8378d6a296c3ed3d8769af97a1f19d1e95f3c00d76d4b02d6 | CLEAN |
| collector/app/services/resolved_config_registry.py | 17337 | 1844449a3f99e9ca53bddc8063c151fb0f889920597bccb170f5e62f3715db2c | CLEAN |
| config/mapping.yaml | 7112 | d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d | CLEAN |
| collector/Dockerfile | 218 | e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839 | CLEAN |
| docker-compose.yml | 5698 | c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66 | CLEAN |
| collector/tests/test_event_collector_reliability.py | 12774 | 462656c9d9146e492b52296ca2b40a1f37fe40cba95a2068e4c6317fd33c2472 | CLEAN |
| tests/test_collector_station_event_runtime_source.py | 30571 | 7d9d894eaa784e36c729e824ee87de73a863765089fd12e388bc926164229fd7 | CLEAN |

当前实现事实：main.py 先构造 config/source/storage/detector，再构造 worker 并启动 thread；event_collector.py 当前在 build_read_plans() 后直接做 dict-by-scope conversion，当前没有 R42 success record；mapping.py 当前使用 Path(path).read_text()，还没有 raw-byte hash 与同一次 decode/parse 的绑定。这些只是 live source facts，不被表示为实现 PASS。

## 6. R42 candidate contract 的 Data Quality 结论摘要

R42/R43 已明确以下正确边界：Candidate A 是 main-process startup 的 one-shot deterministic application record；记录只声明 mapping/resolved/read-plan initialization 与 main-entry PID/time assertions，不声明 Thread.start、worker health、PLC、DB、accepted fact、ACK/read_done 或 production。

R42 也已冻结 exact v1 key set、strict application-message literal、same-byte read/hash/decode/parse 目标、B1 duplicate/cardinality/scope 顺序、fresh container/process/log external provenance 目标以及 three-source/two-test implementation allowlist。这些部分可以作为后续修复的基础。

但下列三个 Data Quality 缺口仍可导致 cross-scope、stale/foreign-runtime 或 raw/normalized false PASS，因此不能接受 R42 进入 Verification planning：

1. line_id 没有唯一 canonical source 与冲突 fail-closed 规则。
2. accepted implementation source 到 fresh active image、container/process、config bytes 的 bounded binding 没有冻结为 terminal expected authority。
3. raw container-log transport、exact application-message/payload bytes 与 parsed record 之间没有冻结可供独立复核的 bounded durable identity；R43 仅给出接口分离建议。

上述问题不是当前 runtime 已发生的事实，而是 R42 candidate contract 允许 future validator 接受错误事实的设计缺口。

## 7. Implementation-time authoritative lineage

目标链：

    exact mapping path
    → one raw-byte read
    → mapping_content_sha256
    → explicit UTF-8 decode of the same bytes
    → YAML parse
    → EdgeMapping
    → RuntimeMappingSnapshot
    → semantic config hash
    → ResolvedConfigSnapshot hash-consistency check
    → validated read-plan list
    → duplicate/cardinality/scope validation
    → runtime-loaded record fields

| Stage | Input authority | Output authority / class | Required transformation | Failure behavior |
| --- | --- | --- | --- | --- |
| exact path selection | approved application path /app/config/mapping.yaml | path selection, not content identity | open only the exact regular/non-symlink path | wrong path, missing mount, symlink or scope drift → HOLD |
| raw read | exact path bytes visible to process | one immutable raw byte sequence / raw evidence | one read only; no newline normalization | read/error/second-read/substituted path → no success record |
| raw identity | same raw bytes | lowercase 64-hex mapping_content_sha256 / raw-derived evidence | SHA-256 directly over bytes | mismatch or noncanonical digest → HOLD |
| decode | same raw bytes | explicit UTF-8 text / derived evidence | decode exactly those bytes | invalid UTF-8 or re-encoding hash → no success record |
| YAML parse | decoded text | parsed mapping object / parsed evidence | strict parse; ambiguous duplicate keys must not be silently collapsed | malformed/ambiguous mapping → no success record |
| EdgeMapping | parsed object | typed mapping model / parsed authority | preserve top-level mapping identity, line fields, stations and PLC routing data | required field or semantic validation failure → no success record |
| RuntimeMappingSnapshot | EdgeMapping semantic fields | hash-bound semantic snapshot / derived authority | construct same snapshot and compute config_hash deterministically | snapshot hash mismatch → no success record |
| ResolvedConfigSnapshot | RuntimeMappingSnapshot | resolved snapshot with same config_hash / derived authority | build registry/snapshot and verify content_hash_matches | hash inconsistency or registry mismatch → no success record |
| read plans | same typed mapping | full list of line + all configured station plans / derived plan authority | build list before dict conversion | missing/extra/duplicate/cardinality/scope mismatch → no success record |
| runtime projections | validated list + same hash-bound snapshots | line plan and one station runtime per configured station / projected evidence | materialize only after B1 checks; disabled configured stations remain in expected count | one-to-one/count mismatch → no success record |
| record construction | same context, snapshots and validated plans | v1 JSON object / application assertion | exact keys, exact types, compact deterministic UTF-8 one-line serialization | missing/extra key, wrong type or serialization failure → no success record |

The current source has not implemented this chain. R42 is a future contract only; this review does not execute EventCollectorWorker, tests, application, Docker or remote runtime.

## 8. Later runtime-validation authoritative lineage

Required future chain：

    accepted implementation source identity
    → built/deployed image identity
    → fresh active image identity
    → fresh active container/process identity
    → current container-ID-scoped raw log evidence
    → exact application-message extraction
    → exact JSON payload bytes
    → parsed v1 object
    → expected-value comparisons
    → terminal PASS/HOLD decision

| Stage | Input authority | Output | Class | Failure behavior |
| --- | --- | --- | --- | --- |
| source identity | approved frozen commit and exact implementation manifest | accepted source identity | external authority | absent or wrong source binding → HOLD |
| image identity | fresh build/deploy evidence from accepted source | full top-level image ID sha256:<64> | external authority | tag/Config.Image only, mismatch or unavailable ID → HOLD |
| active container/process | fresh full container ID, image ID, StartedAt and active main PID | current process boundary | external authority | stale/foreign/ambiguous process or image → HOLD |
| raw log envelope | current full-container-ID-scoped bounded transport output and interval | exact raw bytes/line identity | raw external evidence | missing, truncated, rotated, unbound or rewritten transport → HOLD |
| application extraction | selected raw line/application-message component | exact bytes beginning collector_runtime_loaded_json= | derived but byte-preserving evidence | substring search, multiple delimiter, wrong line or suffix → HOLD |
| JSON payload | exact bytes after delimiter | exact payload bytes, separately retained | derived raw-payload evidence | duplicate names, malformed/truncated/non-object/normalization ambiguity → HOLD |
| parsed record | exact payload bytes | v1 object with exact key set/types | parsed evidence | missing/extra key, bool-as-integer, string-as-integer or unknown schema → HOLD |
| expected comparison | non-self-referential expected matrix | per-field expected/actual and lineage result | comparison evidence | any mismatch or unproven relation → HOLD |
| terminal result | all external and application evidence | PASS or HOLD | terminal decision | never upgrade to production truth |

The raw transport artifact, selected line, extracted message, exact payload, parsed object and field comparison must remain distinguishable. A parsed object alone is not raw authority.

## 9. R42 v1 field-authority matrix

| Field | JSON type / canonical format | Immediate source | Derivation | Authority class | Expected-value authority | Cross-field rule | Mismatch outcome | Use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| evidence_schema_version | string; exact edge-mes/collector-runtime-loaded/v1 | frozen record contract | constant | application assertion | frozen R42 contract | paired with exact event_type | HOLD | terminal |
| event_type | string; exact collector_runtime_loaded | frozen record contract | constant | application assertion | frozen R42 contract | paired with schema version | HOLD | terminal |
| mapping_path | string; exact /app/config/mapping.yaml | required constructor path | canonical path projection | application assertion / deployment projection | approved deployment contract plus fresh active mount observation | path must be the path whose bytes were read and hashed | HOLD | terminal |
| mapping_content_sha256 | string; lowercase 64-character SHA-256 hex | same raw bytes used for decode/parse | SHA-256(raw bytes) | raw-derived application assertion | fresh active-container-visible mapping bytes bound to approved deployed config; never historical R35 hash or record self-value | path, raw bytes, parsed mapping and record share one lineage | HOLD | terminal |
| mapping_schema_version | string; exact non-empty parsed value, current expected runtime-mapping/v1 | top-level parsed mapping | projection from same EdgeMapping/snapshot | hash-bound projection | independently parsed exact authoritative mapping bytes | equals resolved snapshot schema and independent expected value | HOLD | terminal |
| config_version | string; exact non-empty parsed value, current expected 2026.06.26-slice-a | top-level parsed mapping | projection from same snapshot | hash-bound projection | independently parsed exact authoritative mapping bytes | equals resolved snapshot config version | HOLD | terminal |
| line_id | string; exact canonical source required | R42 is ambiguous: top-level RuntimeMappingSnapshot.line_id/ResolvedConfigSnapshot.line_id versus first PLC entry used by EventCollectorWorker.self.line_id | projection must be from one frozen canonical source and cross-checked against routing projection | currently unresolved, potentially cross-scope | independently parsed exact mapping bytes and fresh approved config | top-level hash-bound identity must equal any selected PLC routing line identity before emission | HOLD; blocker DQ-B1 | terminal and external correlation |
| read_plan_count | JSON integer, not boolean; positive | validated complete plan list | len(validated_plans) after B1, before dict conversion | derived plan assertion | independent count from exact authoritative mapping: 1 line scope + all configured station scopes, disabled included | exact scope/cardinality/multiset and resolved hash must agree | HOLD | terminal |
| resolved_config_hash | string; lowercase 64-character SHA-256 hex | ResolvedConfigSnapshot.config_hash bound to RuntimeMappingSnapshot.config_hash | semantic hash of same parsed snapshot | hash-bound semantic assertion | independent recomputation from exact authoritative mapping bytes or pre-approved non-self-referential value | projections and registry lookup use this same hash-bound snapshot | HOLD | terminal |
| collector_main_started_at_utc | string; RFC3339 UTC with literal Z | mandatory main-entry startup context | capture at app.main.main entry | application correlation assertion | fresh container StartedAt and bounded observation time | StartedAt <= value <= observation time | HOLD | process correlation |
| process_pid | JSON integer, not boolean; positive | same mandatory startup context and os.getpid | capture current Python process PID | application correlation assertion | fresh active Collector main PID/process observation | PID equals current active process and belongs to current container/log boundary | HOLD | process correlation |

No v1 field is an independent production fact. No field may establish PLC connection, DB health, event persistence, ACK/read_done, machine state, accepted fact or production acceptance.

## 10. Canonical type/format review

| Field/group | Data Quality ruling |
| --- | --- |
| schema/event | exact literals; unknown/new schema or event type fails closed; no best-effort compatibility |
| path | exact application path; path string is not content identity |
| raw and semantic hashes | lowercase 64-hex SHA-256; raw hash is byte identity, resolved hash is semantic/resolved identity; no conflation |
| schema/config projections | exact parsed strings and independent expected values; format-only validation is insufficient |
| line_id | exact canonical source must be frozen; current equal values LINE_001 do not resolve future source semantics |
| read_plan_count | JSON integer, non-boolean, positive, independently derived and exact against full validated scope set; disabled stations count |
| collector_main_started_at_utc | RFC3339 UTC with Z; offset forms, malformed values and impossible ordering fail closed |
| process_pid | JSON integer, non-boolean and positive; compare to fresh process observation |
| JSON object | exact key set; no extra/missing keys; duplicate member names, truncation, non-object payload and parser normalization ambiguity fail closed |

## 11. line_id authority assessment — blocker DQ-B1

Live source has two observable identities：

1. collector/app/plc/mapping.py:133 reads top-level raw.line_id; it populates EdgeMapping.line_id and RuntimeMappingSnapshot.line_id at :205-209. This value is included in _runtime_hash_content at :260-266 and copied into ResolvedConfigSnapshot.line_id at resolved_config_registry.py:176-178. It is therefore the semantic/resolved-hash-bound candidate canonical source.
2. collector/app/services/event_collector.py:46-48 selects the first mapping.plcs entry and sets self.line_id from self.plc.get("line_id", self.mapping.line_id). The value is used by existing runtime status, error, accepted-fact and persistence calls. PLC entries are not included in RuntimeMappingSnapshot semantic hash content.

Current config/mapping.yaml has LINE_001 at top-level line_id, plcs[0].line_id and line.line_id at :4, :39 and :42. Current equality is not a contract decision.

R42 §9.3 and §11 only call the record value loaded line_id; they do not state which of the two sources is canonical, whether PLC line identity is only a routing projection, or that mismatch must fail closed. R43 §12 repeats the field list but does not close this ambiguity. Therefore a future record could emit PLC LINE_B while resolved_config_hash binds top-level LINE_A, or vice versa. A later validator comparing only the record self-report and hash can accept a cross-line/cross-scope false PASS.

Minimal contract requirement returned to PM：

- freeze RuntimeMappingSnapshot.line_id / ResolvedConfigSnapshot.line_id from the top-level mapping as the record's canonical line authority;
- classify EventCollectorWorker.self.line_id / PLC entry line_id as routing projection only;
- before emission, validate the selected PLC routing line identity is present, unique and equal to the canonical hash-bound line identity;
- emit the canonical snapshot line value, not an unchecked PLC projection;
- any mismatch, missing value or ambiguous PLC selection fails closed before the record.

This is a credible cross-line false-PASS blocker and requires PM scope/assurance reassessment. No source or test repair is authorized in this Thread.

## 12. Raw mapping identity assessment

The live committed/local mapping file is config/mapping.yaml, 7112 bytes, SHA-256 d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d. R35 recorded the same host/container mapping SHA as historical accepted static evidence. That historical value is not fresh active-runtime authority.

Required authority separation：

- mapping_content_sha256 is calculated over the exact bytes used for the one decode and YAML parse;
- no second read, newline normalization, text re-encoding hash or substituted path;
- explicit UTF-8 decode consumes those same bytes;
- raw SHA is not the path string and is not the semantic/resolved hash;
- process-emitted SHA is an application assertion and cannot self-prove correctness;
- R35 historical hash cannot be reused as future active-runtime expected authority;
- a future validator must fresh-read/hash the active container-visible mapping file and bind those bytes to the approved deployed config/image;
- committed/local bytes may be an expected source only when the deployment gate proves the exact bytes were visible to the active container;
- static recomputation supports expected values but never independently proves process-bound loading.

Raw-byte mismatch, unavailable fresh mapping bytes, symlink/path drift or broken binding is HOLD.

## 13. Semantic/resolved identity assessment

RuntimeMappingSnapshot.config_hash is computed from parsed semantic content including top-level line identity, schema/config projections, route graph, code tables and station projections. ResolvedConfigSnapshot receives the same hash, verifies mapping snapshot content, builds the decoder registry and checks content consistency. The in-memory registry also rejects a lookup whose object/hash content does not match.

The two hashes have distinct duties：

- mapping_content_sha256: exact raw file-byte identity;
- resolved_config_hash: semantic/resolved identity of the same parsed, hash-bound snapshot.

No second independent semantic mapping hash is justified. A future validator's expected resolved hash must be independently recomputed from the exact authoritative mapping bytes or taken from an explicitly pre-approved, non-self-referential expected value. The runtime record itself is never its own expected-value authority.

## 14. Projection-field assessment

mapping_schema_version, config_version, line_id and read_plan_count are denormalized assertions, not independent truth authorities. They must be projected from the same hash-bound mapping/snapshot/validated-plan objects and compared to independently derived expected values.

- A projection/source mismatch is terminal HOLD.
- Parser format checks alone are insufficient for terminal PASS; expected-value comparison is required.
- The future validator should parse exact authoritative mapping bytes independently for schema, config, line and count.
- No requirement exists to copy every mapping field into v1; only fields needed to prevent schema-invalid, cross-scope or false runtime truth belong in the contract.

The unresolved line_id source is the exception: it is not a harmless denormalization difference because it can bind a record to a different line than the resolved hash.

## 15. read_plan_count truth semantics

R42 §8 correctly requires list-first capture：

    configured_station_ids = [station.station_id for station in mapping.stations]
    expected_scopes = ["line"] + configured_station_ids
    generated_scopes = [plan.scope for plan in build_read_plans(mapping)]

The count must be taken only after complete duplicate/cardinality/scope/multiset and one-to-one station-runtime validation, before dict overwrite. Expected count is independently derived from exact mapping bytes as 1 line scope + all current configured station scopes; disabled configured stations remain included. Count mismatch is HOLD.

The v1 record need not add a sorted scope list: validated implementation contract, resolved hash and independent expected count are sufficient for this claim, provided B1 checks and expected comparison are actually enforced.

## 16. Application assertion versus external authority

Application record may assert only：

- loaded mapping raw and semantic identities;
- loaded schema/config/line projections;
- loaded validated complete plan count;
- main-entry timestamp and PID correlation assertions.

Only later external observation may establish：

- full active container ID;
- full active image ID;
- fresh container StartedAt;
- active Collector main PID/process identity;
- current full-container-ID-scoped log envelope;
- bounded observation timestamp;
- fresh active-container mapping bytes;
- accepted implementation/image identity.

Config.Image, descriptive tags, compatibility tags, hostname, ordinary startup logs, PID/timestamp alone, path/hash alone, R35 static probe, local/static/manual records and synthetic records are not standalone runtime authority.

## 17. Source/image/config/process binding — blocker DQ-B2

R31 distinguishes exact top-level image ID from tags and Config.Image; its Dockerfile copies committed collector/app and common source closure, while Compose mounts ./config read-only at /app/config. Therefore source/image identity and mapping/config identity are separate dimensions that must be joined by evidence.

R42 §16 requires fresh active image/container/process facts but does not freeze an expected-value comparison from accepted implementation source identity to the fresh active image. It also does not require the fresh active image, container and process to be bound to exact container-visible mapping bytes before comparing process-emitted hashes. R35 historical image and mapping facts cannot supply future freshness.

Without this bounded join, a stale or foreign implementation/image can emit a correctly formatted v1 record and be found in a current PID/container log envelope; a validator that checks only the record and current process relation could accept it as the intended runtime-loaded implementation.

Minimal bounded requirement：

    approved implementation commit/path manifest
    → accepted built/deployed full image ID
    → fresh active full image ID
    → fresh active full container ID + StartedAt
    → active Collector main PID
    → current container-visible mapping bytes
    → process-emitted raw/semantic identities
    → parsed v1 record

This is limited to the current runtime-loaded claim. It does not require general supply-chain security, hostile same-process protection, tamper-resistant audit, generic forensics or long-term retention.

## 18. Raw versus normalized log evidence — blocker DQ-B3

R42 §10 defines the application-message grammar and a strict parser boundary; R43 §13 confirms the distinction between logging prefix and application message. R43's recommendation to separate the transport adapter and parser is useful but non-blocking wording only. Neither contract freezes the durable identity needed to independently prove that a terminal parsed object came from exact raw transport rather than a substituted normalized line.

Future bounded evidence must retain, separately and without canonicalizing raw identity：

1. current full-container-ID-scoped raw log bytes or exact bounded artifact, observation interval and raw artifact SHA-256;
2. selected raw line identity/order within that bounded envelope;
3. exact extracted application-message bytes;
4. exact JSON payload bytes after the one delimiter, with its own byte identity;
5. parsed v1 object and exact key/type validation result;
6. per-field expected/actual comparisons, lineage checks and terminal PASS/HOLD.

This is not a general log retention or telemetry subsystem. It is the minimum bounded evidence needed to prevent raw/normalized replacement, substring selection, synthetic/manual evidence misclassification or post-hoc parsed-object substitution. If only a normalized object is retained, a false runtime PASS remains credible.

## 19. Parser transformation assessment

The future parser must preserve string values and exact payload bytes; it must not trim or normalize internal JSON strings, convert numeric strings to integers, accept booleans as integers, discard extra keys before validation, or replace raw evidence with a reserialized object. It must reject malformed/truncated/non-object JSON, duplicate JSON member names, missing/extra keys, unknown schema/event type, duplicate matching records and ambiguous application messages. Serialization and logger errors must propagate; no fallback, retry, substitute success, delayed replay or poll-loop emission is permitted.

R42 covers much of this boundary but does not explicitly freeze duplicate JSON member rejection or non-boolean integer checks in its focused matrix. Those checks are included here as mandatory Data Quality acceptance conditions within the existing two-test allowlist, not as a request for a new parser subsystem.

## 20. Record schema/version and runtime/production boundary

evidence_schema_version is exactly edge-mes/collector-runtime-loaded/v1; it is the evidence-record schema and is not mapping_schema_version. Unknown/new schema or event type fails closed. The v1 record excludes DSN, credentials, host/port, raw PLC bytes, unit ID, DMC, station event payload, NOK detail, DB result, accepted fact, ACK/read_done state and production counters.

The correct classification is：

    RUNTIME-LOADED record = runtime configuration/process evidence
    not = station event
    not = accepted station-event fact
    not = DB-backed production fact
    not = PLC acknowledgement
    not = read_done authority
    not = machine-state truth
    not = production acceptance
    not = UI production truth

RUNTIME-LOADED can never be upgraded by this record to PRODUCTION-ACCEPTED, PLC-CONNECTED, DB-HEALTHY, EVENT-PERSISTED, ACK-VALIDATED or any accepted-fact claim. The record must not enter production DB or accepted-fact projection.

## 21. Future exact implementation/test allowlist review

| Surface | Necessary | Sufficient | Data Quality responsibility | Additional path |
| --- | --- | --- | --- | --- |
| collector/app/main.py | yes | yes with the other two | main-entry context/time/PID and exactly-one worker handoff | none |
| collector/app/services/event_collector.py | yes | yes with the other two | context single-use/PID, canonical line check, B1 validation, exact record and one-shot emission | none |
| collector/app/plc/mapping.py | yes | yes for same-byte raw binding | one-read bytes/hash/decode/parse binding and raw identity exposure | none |
| collector/tests/test_event_collector_reliability.py | yes | yes with the other test | constructor, context, line conflict, B1, field types, no-side-effect and emission-order cases | none |
| tests/test_collector_station_event_runtime_source.py | yes | yes with the other test | same-byte raw identity, parse failures, hash consistency, strict payload/manual evidence cases | none |

The existing exclusions resolved_config_registry.py, read_plan.py, config/mapping.yaml, Dockerfile, Compose, Storage, PLC/DB/ACK/read_done and production surfaces do not need to be added for the minimum contract repair. No additional source/test path is required. If a future runtime-validation gate needs durable raw evidence files, those must receive a separate exact artifact allowlist; that is not permission to expand this R44 report or the R42 implementation allowlist.

The allowlist is necessary/sufficient in shape, but it is not safe for implementation until PM resolves DQ-B1–DQ-B3 and accepts the repaired assurance boundary.

## 22. Future test-matrix Data Quality sufficiency

| Required case | R42/R43 status | R44 ruling |
| --- | --- | --- |
| one raw read, hash same bytes, explicit decode/parse | contract present; current implementation not changed | must be tested, not executed here |
| raw SHA lowercase 64-hex and raw/semantic distinction | partially explicit | add exact canonical-format assertion |
| resolved hash bound to same parsed snapshot | present in contract and current registry design | sufficient in contract, test required later |
| schema/config/line projections from same authority | schema/config present; line source unresolved | line conflict is blocker |
| top-level/PLC line conflict fail closed | absent from R42 §15 | blocker DQ-B1 |
| validated complete plan count, disabled included | present | sufficient in contract, test required later |
| projection mismatch produces no success record | implied but not enumerated for every projection | add focused assertions within existing paths |
| exact integer/non-boolean PID and count | not explicit enough in R42 matrix | mandatory parser/type assertion |
| exact timestamp Z and fresh PID relation | present | sufficient in contract, test required later |
| missing/extra keys, unknown schema/event | present | sufficient in contract, test required later |
| duplicate JSON member names and duplicate records | duplicate records present; member-name case not frozen | mandatory strict-parser assertion |
| raw/normalized/manual/static evidence separation | boundary present; durable raw identity absent | blocker DQ-B3 |
| secrets/production fields absent | present | sufficient in contract |
| no production accepted-fact/ACK/read_done path | present | sufficient in contract |

The two exact test paths can cover the needed cases. This is a test-contract review only; no pytest, compileall, application construction or runtime test was executed.

## 23. Later Verification expected-value matrix

| Terminal field/group | Non-self-referential expected source |
| --- | --- |
| schema/event | frozen R42 v1 contract; exact literals |
| mapping path | approved deployment contract plus fresh active-container mount/path observation |
| raw mapping SHA | fresh hash of active container-visible mapping bytes, bound to approved deployed config/image; not R35 historical hash and not record self-value |
| mapping schema/config/line | independent parse of exact authoritative mapping bytes; line uses PM-frozen canonical source and conflict rule |
| read-plan count | independent derivation from exact mapping and R42 scope rules: one line plus all configured stations, including disabled |
| resolved config hash | independent semantic recomputation from exact authoritative mapping bytes, or explicitly pre-approved equivalent value |
| collector main PID | fresh process observation for current active container |
| collector main start time | fresh container StartedAt plus bounded observation time relation |
| source/image/process binding | accepted implementation manifest → accepted full image ID → fresh active full image/container/process facts |
| raw log lineage | exact bounded raw artifact/hash → selected line → exact application message → exact payload bytes → parsed object |

The runtime record is an assertion to compare, never the sole expected-value authority.

## 24. New credible blocker assessment

### DQ-B1 — canonical line_id ambiguity with cross-line false PASS

R42 §§9.3/11 and R43 §12 list line_id but do not select top-level hash-bound mapping identity versus PLC routing projection. Live source confirms these are distinct observable values, and PLC entry identity is excluded from semantic hash. A future record/hash pair can therefore cross lines while passing self-consistency. Minimal requirement: freeze top-level snapshot line identity as canonical, classify PLC line as routing projection, compare before emission, fail closed on mismatch.

### DQ-B2 — source/image/config/process binding absent from terminal authority

R42 §16 asks for fresh image/container/process facts but does not require fresh active image identity to equal the accepted implementation's deployed image identity or bind that image/process to fresh container-visible mapping bytes. A stale/foreign implementation can emit a valid-looking record in a current process/log boundary. Minimal requirement is the bounded source → image → container/process → config bytes → record chain in §17.

### DQ-B3 — raw/normalized durable evidence identity not frozen

R42/R43 define a strict parser boundary but do not require preservation of exact bounded raw transport bytes, selected line identity, exact application message and exact JSON payload bytes alongside parsed object/comparison. A later terminal report retaining only a normalized object can silently replace raw evidence and still PASS. Minimal requirement is the bounded evidence set in §18, without a general retention subsystem.

All three are credible false-PASS/evidence-authority blockers, not presentation preferences. They are new Data Quality blocker findings after Architecture repair and Reliability re-review; PM must reassess scope and assurance proportionality before any Architecture repair, Verification planning or implementation is authorized.

## 25. Bounded non-blocking recommendations

After PM resolves the blockers, retain these as bounded implementation-review checks rather than new scope：

1. Explicitly test that a first startup-context consumer remains consumed after constructor failure; no retry/reuse can emit a success record.
2. Keep raw transport adapter, application-message extractor and JSON parser as separate reviewable stages while retaining exact bounded evidence.
3. Keep record_emitted_at and sorted scope list out of v1 unless a later PM decision shows a concrete false-PASS need.
4. Preserve the existing no-API/no-DB/no-telemetry/no-generic-registry/no-production semantics.

These recommendations do not authorize source/test edits, runtime validation or allowlist expansion.

## 26. Changed-path / allowlist audit

Task-owned changed set：

    docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md

No other path was created or modified by this review. R42, R43, all source/test/config/Docker/Compose files, status/roadmap/handoff/PM rules and Batch D/E remain untouched. No Git index or remote state was changed.

## 27. Final Git/index/untracked audit

After writing this report, the required final read-only audit is：

    HEAD == origin/main == ce22ca71eff0548aa064129c160f7041603855e7
    HEAD^ == 35c50b1eb0f76d8b3361e8c122448ad03899559b
    ahead / behind == 0 / 0
    tracked dirty == empty
    cached == empty
    initial untracked == 305
    final untracked == 306
    final composition == Batch D 300 + Batch E 1 + R40 1 + R41 1 + R42 1 + R43 1 + R44 1
    unknown paths == 0

R44 must remain UNSTAGED / UNTRACKED / NON-SYMLINK / regular UTF-8. Its final bytes and SHA-256 are measured by the detached post-write audit and returned in the Chat manifest; embedding its own SHA-256 into the same bytes would be self-referential. This detached identity is not a second artifact.

## 28. Evidence boundary and next gate

    DATA-QUALITY-REVIEWED / WRITTEN only
    NOT REPAIRED
    NOT IMPLEMENTED
    NOT TESTED
    NOT RUNTIME-LOADED
    NOT PRODUCTION-ACCEPTED

Next gate：

    R44 Data Quality HOLD WRITTEN
    → ChatGPT PM durable intake only
    → PM scope/assurance proportionality reassessment
    → no automatic Architecture repair, Verification review or implementation

R42 candidate acceptance, R43 PASS, this R44 review and any bounded recommendation do not grant future source/test, Git, remote, Docker, lifecycle, runtime-loaded or production authority.

## 29. MVP alignment

MVP-ALIGNED WITH BACKLOG ITEMS。

The review remains bounded to the minimum runtime-loaded configuration/process claim and identifies only the evidence bindings needed to prevent cross-line, stale/foreign-image and raw/normalized false PASS. It does not add API, DB persistence, production fact validation, PLC/ACK/read_done semantics, telemetry, generic registry, audit/forensics, cryptographic provenance or long-term log retention. The HOLD is an assurance-contract HOLD, not a request for a new Level 2 product project.

## 30. Thread context assessment

    output length: long durable review
    continue current Thread: no
    new Thread recommended: yes
    reason: independent Data Quality review is terminalized; PM durable intake and scope/assurance reassessment must occur before any new Architecture repair, Verification planning or implementation authority

End state：DATA-QUALITY HOLD WRITTEN ONLY。
