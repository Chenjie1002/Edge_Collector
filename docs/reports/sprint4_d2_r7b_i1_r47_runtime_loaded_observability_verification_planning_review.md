# Sprint 4 D2-R7B-I1 R47 Runtime-Loaded Observability Verification Planning Review

## 1. Report identity, authority and terminal decision

- 任务：D2-R7B-I1 R47 — Independently Review Whether the R42 + R45 Combined Contract Is Deterministically Implementable and Verifiable
- 执行 Thread：Verification
- Authority source / ID：`PM-D2-R7B-I1-R47-RUNTIME-LOADED-OBSERVABILITY-VERIFICATION-PLANNING-REVIEW-260730-1120`
- Delivery：`REPOSITORY_DURABLE_REPORT`
- 唯一允许写入路径：本文件
- Authority：`AUTHORIZED ONCE / INDEPENDENT VERIFICATION PLANNING REVIEW / LOCAL DOCS WRITE ONLY / NO IMPLEMENTATION / NO TEST EXECUTION / NO REMOTE OR RUNTIME AUTHORITY / NO REPAIR / NOT REUSABLE`

### Terminal decision

```text
PASS / VERIFICATION_PLANNING_ACCEPTS_R42_R45_COMBINED_CONTRACT
NON_BLOCKING_RECOMMENDATIONS_PRESENT
```

R42 继续控制 base application contract；R45 只对 canonical `line_id`、后续 source/image/config/process terminal binding 及 raw-log/payload/parsed-evidence identity supersede。R43 对未改变的 Reliability clauses 继续有效，R46 已 focused-accept DQ-B1/DQ-B2/DQ-B3。未发现会造成 false PASS、self-referential expected authority、无法建立 terminal oracle 或必须扩大 current application allowlist 的新 blocker。

本报告只表示 `VERIFICATION-PLANNING-REVIEWED / WRITTEN`。不表示 implementation、test、Git、build、deploy、active process、fresh remote observation、`RUNTIME-LOADED` 或 `PRODUCTION-ACCEPTED`。

## 2. Scope, evidence boundary and prohibited actions

本轮只审查：R42 + R45 effective precedence、claim ladder、current three-source/two-test allowlist、future implementation test oracle、source-to-image-to-process binding、PID namespace semantics、container-visible mapping/resolved-hash oracle、raw-log adapter、A–H bounded evidence、strict parser、ordered terminal algorithm、failure matrix、MVP proportionality与停止规则。

本轮未执行 pytest、compileall、application/Collector、Docker/Compose、network/SSH、remote/DB/API/PLC/V-PLC、Git mutation、source/test/config repair 或生产 fact/ACK/read_done activity。Batch D/E 未处理。

证据边界：

```text
VERIFICATION-PLANNING-REVIEWED
WRITTEN
NOT REPAIRED
NOT IMPLEMENTED
NOT TESTED
NOT STAGED
NOT COMMITTED
NOT PUSHED
NOT BUILT
NOT DEPLOYED
NO FRESH REMOTE OBSERVATION
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED
```

## 3. Fresh Git recovery and current product boundary

| Field | Live result |
| --- | --- |
| repository root | `/Users/chenjie/Documents/MES/edge-mes-demo` |
| branch | `main` |
| HEAD | `ce22ca71eff0548aa064129c160f7041603855e7` |
| origin/main | `ce22ca71eff0548aa064129c160f7041603855e7` |
| HEAD^ | `35c50b1eb0f76d8b3361e8c122448ad03899559b` |
| ahead / behind | `0 / 0` |
| tracked dirty | empty |
| cached | empty |
| `git diff --check` / cached | PASS / PASS |
| initial untracked | 308 |
| R47 before write | ABSENT / NON-SYMLINK / UNSTAGED / UNTRACKED |

当前产品状态保持：

```text
ACTIVATED                  = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED             = NO
PRODUCTION-ACCEPTED        = NO
```

R35 的 active image/static mapping evidence 只能证明 `ACTIVATED` 与 `STATIC_MAPPING_INITIALIZED`，不能代替 process-bound runtime-loaded evidence。旧 status/roadmap 的 historical next-gate 文本不重开已关闭 gate。

## 4. Exact input identities

以下输入均为 regular UTF-8、NON-SYMLINK、UNTRACKED、UNSTAGED，live bytes/hash 与 Prompt 一致，且本轮未修改：

| Input | Bytes | SHA-256 | State |
| --- | ---: | --- | --- |
| R42 `docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md` | 32319 | `dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165` | PM-ACCEPTED CANDIDATE BASE / RELIABILITY-ACCEPTED / NOT FINAL |
| R43 `docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md` | 30244 | `95b2e63c4879fb5af6920b262300566c577612dd1753b13bf59928c1417338e8` | RELIABILITY RE-REVIEW PASS / PM-ACCEPTED |
| R44 `docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md` | 43036 | `3b4d1f3451d0b0036e5530bc83eb35b90ee2b6d140b0a2799b82df1ada035bfa` | HISTORICAL DATA QUALITY HOLD / BLOCKER ORIGIN |
| R45 `docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md` | 13786 | `8fd646f24565bbcb27aa9063038774fee3b5398d66566f961bee296ffff02ef2` | BOUNDED SCOPE-RESET ADDENDUM / PM-VERIFIED |
| R46 `docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md` | 23703 | `f460fef43d975de41ed624fa49d8a1a8dcd5246b4ae55b222189f40703914b81` | DATA QUALITY RE-REVIEW PASS / ACCEPTED AS R47 INPUT |

R44 remains historical blocker evidence only. R46 is the accepted focused closure input; it does not grant implementation or runtime authority.

## 4A. Current source, test, image and mapping identities

All listed current paths are clean relative to HEAD, regular, NON-SYMLINK, and unchanged in this review.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `collector/app/main.py` | 2073 | `a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090` |
| `collector/app/config.py` | 764 | `4f01689a34fb494f7ea84cf74b303ce8aed0957d1dd9c05fc7773563cd577afc` |
| `collector/app/services/event_collector.py` | 16342 | `eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f` |
| `collector/app/services/resolved_config_registry.py` | 17337 | `1844449a3f99e9ca53bddc8063c151fb0f889920597bccb170f5e62f3715db2c` |
| `collector/app/plc/mapping.py` | 17433 | `c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098` |
| `collector/app/plc/read_plan.py` | 1482 | `fd5f675501444ed8378d6a296c3ed3d8769af97a1f19d1e95f3c00d76d4b02d6` |
| `collector/tests/test_event_collector_reliability.py` | 12774 | `462656c9d9146e492b52296ca2b40a1f37fe40cba95a2068e4c6317fd33c2472` |
| `collector/tests/test_snap7_reliability_integration.py` | 8025 | `5cc75a9cd37eeee6f3a80e29d186b55b3aab3a335898d77e204a9d653f686b54` |
| `tests/test_collector_station_event_runtime_source.py` | 30571 | `7d9d894eaa784e36c729e824ee87de73a863765089fd12e388bc926164229fd7` |
| `tests/test_collector_container_packaging.py` | 941 | `351e80a76a53f742258e91196b109172de7b43dc3fa359e63ef44c9e7ad9c26e` |
| `collector/Dockerfile` | 218 | `e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839` |
| `docker-compose.yml` | 5698 | `c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66` |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` |

## 5. Effective R42 + R45 precedence

| Subject | Effective authority | Verification result |
| --- | --- | --- |
| base application contract | R42 | unambiguous |
| canonical `line_id` and emission-time equality | R45 supersedes R42 only here | unambiguous |
| later source → image → config → process binding | R45 supersedes R42 only here | unambiguous |
| later raw transport → selected line → application message → payload → parsed evidence identity | R45 supersedes R42 only here | unambiguous |
| startup context, single-use, PID check, exactly-one, scope/cardinality, deterministic grammar, parser rejection, emission order and logger/serialization failure | unchanged R42, Reliability accepted by R43 | unambiguous |
| DQ-B1/B2/B3 closure | R46 accepts the R42 + R45 combination | unambiguous |
| R44 | historical blocker origin only | does not control current combined contract |

No R42/R45 subject has conflicting terminal rules. R45 does not change v1 shape, three-source/two-test allowlist, PLC/DB/accepted-fact/ACK/read_done semantics or runtime/production truth boundary.

## 6. Claim ladder and stage authority

| Stage | Can establish | Cannot establish; next authority is separate |
| --- | --- | --- |
| local contract review | wording/precedence and planned oracle are deterministic | source implementation or any runtime fact |
| local implementation tests | future exact source/test behavior under local fixtures | build, image, deployment or active process |
| implementation source acceptance | exact three changed source paths, bytes, hashes and focused test result | Git closeout or image freshness |
| Git closeout | reviewed commit and exact path manifest | build/deploy/active container |
| built image acceptance | accepted commit/closure produced a full immutable image ID | deployed or active image |
| deployed image/config acceptance | accepted image/config was placed in the intended deployment scope | current active process or runtime record |
| active container/process observation | fresh full image/container/StartedAt/main-process binding | application initialized record or production fact |
| bounded runtime-loaded validation | one current process-bound v1 record plus independent mapping/log evidence | worker health, PLC, DB, accepted fact or production truth |
| PM `RUNTIME-LOADED` acceptance | PM accepts the bounded runtime-loaded claim | `PRODUCTION-ACCEPTED` |
| production accepted-fact validation | separate accepted-fact evidence if separately authorized | this R47 or runtime record itself |
| `PRODUCTION-ACCEPTED` | only the independent production gate's claim | no broader claim than that gate |

Local/static/synthetic/no-DB/manual evidence never upgrades to runtime or production evidence. A partial result at any stage is not a partial PASS; the relevant stage remains `HOLD`.

## 7. Non-inheritance matrix

| From | Does not authorize |
| --- | --- |
| R47 PASS | implementation, source/test edits, Git, build, deploy or runtime validation |
| implementation PASS | Git closeout, image build or deployment |
| Git closeout | build/deploy, lifecycle or runtime observation |
| image/deployment PASS | active process or runtime-loaded validation |
| active process + record | production event, DB persistence, ACK/read_done or production acceptance |
| R43/R46 PASS | any later phase without fresh PM authority |

Every later phase needs fresh exact PM authority, paths and identity audit.

## 8. Current implementation source allowlist review

The exact three-source allowlist is necessary and sufficient together. No additional current application source path is required.

| Source path | Necessary / sufficient | Missing path | Responsibility and expected mutation | Forbidden mutation / regression risk | Verification method |
| --- | --- | --- | --- | --- | --- |
| `collector/app/main.py` | yes / yes with other two | none | At the first executable startup boundary create one mandatory, no-default context carrying entry UTC time and `os.getpid()`; pass it to exactly one worker. | No endpoint, registry, heartbeat, lifecycle, config semantic, PLC/DB/ACK/read_done or production change. Main loop must not create another capability. | constructor handoff; context missing/reuse/foreign-PID negatives; alternate caller no-record |
| `collector/app/services/event_collector.py` | yes / yes with other two | none | Consume context once; preserve list-first plans; reject duplicates/reserved `line`, count/scope/one-to-one errors; enforce canonical snapshot line vs routing line; exact v1 emission last. | No polling/PLC connection, DB query/write, accepted fact, ACK/read_done, persistence or disabled-station change. Existing `self.line_id` stays routing only. | constructor, serialization, side-effect, scope, line and failure-propagation tests |
| `collector/app/plc/mapping.py` | yes / yes for raw binding with other two | none | Read exact raw bytes once, hash/decode/parse those bytes and bind raw identity while preserving `parse_edge_mapping()` callers. | No second read, re-encode/newline-normalized hash, mapping redesign or caller break. | read-count/same-byte, invalid UTF-8/YAML/semantic/hash failure tests |

Excluded: `config.py`, `resolved_config_registry.py`, `read_plan.py`, `storage.py`, `collector/Dockerfile`, `docker-compose.yml`, `config/mapping.yaml`, PLC/DB/ACK/read_done/production, API/Dashboard/V-PLC. Later image/config/process and A–H paths are separate authorities.

## 9. Current test allowlist and focused commands

| Test path | Responsibility | Sufficiency ruling |
| --- | --- | --- |
| `collector/tests/test_event_collector_reliability.py` | context/one-shot/PID, constructor order, canonical line, scope/cardinality, exact record, no-I/O/no-side-effect and existing persistence/ACK/read_done regressions | necessary and sufficient with the other test |
| `tests/test_collector_station_event_runtime_source.py` | one-read raw mapping identity, decode/YAML/semantic/resolved-hash failures, mapping/scope fixtures, strict payload and manual/static evidence boundary | necessary and sufficient with the other test |

Future focused commands are exactly:

```bash
PYTHONPATH=collector:. pytest -q collector/tests/test_event_collector_reliability.py
PYTHONPATH=collector:. pytest -q tests/test_collector_station_event_runtime_source.py
```

The commands have explicit import context and target exactly the allowed test files. Fixtures can remain in those test paths. Existing `test_snap7_reliability_integration.py` and `test_collector_container_packaging.py` were read as protected regression/package evidence, but are not modified or added to the R47 implementation allowlist. This is a test-plan sufficiency result; no command was executed in R47.

## 10. Application implementation verification matrix

| Terminal invariant group | Positive oracle | Negative oracle and required failure point | Forbidden side effects | Classification |
| --- | --- | --- | --- | --- |
| main-entry context, mandatory/no-default, `process_pid == os.getpid()` | main creates one context and one worker receives it | absent, reused, foreign-PID or `process_pid != os.getpid()` fails before success serialization/emission | no alternate/manual caller success capability | terminal PASS/HOLD |
| single-use and exactly-one | one valid record per `main()` invocation/current start boundary | second consumer, duplicate worker, 0 or ≥2 matching records for one boundary are HOLD; `Thread.start()` failure record alone is not PASS | no retry, replay or per-poll emission | terminal PASS/HOLD |
| same-byte mapping identity | one raw read; raw SHA equals bytes decoded and parsed | invalid UTF-8, YAML, semantic or resolved-hash mismatch yields no record before emission | no second read/substituted path | terminal PASS/HOLD |
| mapping/plc/scope structure | line plan plus each configured station maps one-to-one; disabled configured stations count | duplicate station IDs, reserved `line`, duplicate/missing/extra scopes, count or one-to-one mismatch before dict conversion | no dict-overwrite hiding, no station omission | terminal PASS/HOLD |
| canonical line | snapshot `line_id` is non-empty and selected routing line exists/non-empty/equal; record uses snapshot value | missing/empty/mismatch/ambiguous routing line before serialization | no first-PLC or production line-model change | terminal PASS/HOLD |
| exact v1 object and field types | exact 11-key object, literals, lower 64-hex hashes, integer count/PID, RFC3339 UTC `Z` | missing/extra/unknown/wrong type/numeric string/bool-as-int/bad timestamp rejects | no secret/raw/production fields | terminal PASS/HOLD |
| deterministic serialization | sorted compact UTF-8 one-line JSON, no CR/LF, `allow_nan=False` | serialization or logger failure propagates; no suffix/fallback/retry/replay | no substitute record | terminal PASS/HOLD |
| emission order | success emission is last required constructor action after all checks | any required action after emission that can fail is a contract failure/HOLD | no `Thread.start`, PLC connect, DB query/write, accepted fact or ACK/read_done in constructor | terminal PASS/HOLD |
| compatibility/non-regression | existing persistence and ACK/read_done tests retain current semantics | any changed side effect is implementation HOLD, not a runtime-loaded PASS | no production event generation | terminal PASS/HOLD |

The application record remains an assertion of required initialization and main-entry correlation; later external expected values are mandatory for runtime PASS.

## 11. Startup-context failure-path assessment

The R43/R46 carry-forward is testable within the existing two-test allowlist: make a first context consumer enter the consumed state, force a later constructor failure, then assert a second worker/consumer cannot obtain success capability. It is defense-in-depth for the already-frozen single-use rule and does not change that rule or require another source/test path. It is an implementation-acceptance assertion, not a current blocker: only a demonstrated path that permits duplicate valid success capability could become a false-PASS blocker. Recommendation remains bounded and non-blocking until then.

## 12. Field-level oracle requirements

Future implementation and future runtime parser must enforce:

- `mapping_content_sha256` and `resolved_config_hash`: lowercase exactly 64 hexadecimal characters;
- `read_plan_count` and `process_pid`: JSON integer, not boolean, not numeric string;
- `collector_main_started_at_utc`: RFC3339 UTC with literal `Z`;
- exact `schema_version` and `event_type` literals;
- exact 11-key set, rejecting missing and extra keys;
- schema/config/canonical line/count/hash projections derive from one hash-bound snapshot and are compared to independently derived expected values;
- the emitted record is never its own expected oracle; no copying a self-reported hash/line/count into expected values.

## 13. Implementation acceptance and Git closeout identity

Future implementation acceptance must freeze, before any later phase:

```text
exact changed source/test path set
final bytes and SHA-256 for every changed file
focused command and output
no post-test mutation
tracked/cached/untracked audit
reviewed commit ID
exact path manifest
```

The implementation report/helper paths, Git manifest and commit are future authorities. R47 did not stage, commit or push.

## 14. Accepted source to accepted image

The future chain is:

```text
accepted implementation commit + exact source/path manifest
→ deterministic build-input closure
→ build result
→ accepted full top-level image ID
```

The full top-level immutable `Image` ID is the identity. Descriptive tag, compatibility tag, `Config.Image` and short ID are not sufficient. Build/deployment evidence must bind the accepted commit and exact source closure to the image. R31/R35 historical image evidence is history/baseline only; if the existing image cannot prove inclusion of the new implementation, a separately authorized fresh build/redeploy is required. R47 did not build or deploy.

## 15. Accepted image to active container/process

Future runtime validation must fresh-observe:

```text
accepted full image ID == fresh active full image ID
fresh full active container ID
→ that active image
→ current StartedAt
→ active Collector main process/executable/cmdline
```

Tag-only, short container ID, hostname-only, stale prior container, foreign container, ambiguous/absent process or image mismatch is HOLD. A process-bound record is accepted only inside the current full-container-ID and current `StartedAt` boundary.

## 16. PID namespace verification semantics

`process_pid` is the Python PID from `os.getpid()` in the Collector container namespace. The future validator must independently obtain the Collector main PID in that same namespace and verify executable/cmdline ownership. Host PID or `docker inspect State.Pid` may only assist through explicit namespace mapping/`NSpid` relationship; numerical equality across namespaces is invalid. A read-only `docker exec` probe must not be mistaken for the Collector main, and no worker may be imported/constructed as the probe. Missing, mismatched or ambiguous namespace mapping is HOLD. This rule is executable later without adding fields to v1.

## 17. Container-visible mapping and resolved-hash oracle

From the fresh full active container ID, later validation must independently read `/app/config/mapping.yaml` bytes and record path identity, regular/non-symlink status when observable, byte length and SHA-256. It must not use host-file similarity, historical R35 hash or the record's own hash as authority. Schema/config/canonical line/count are independently parsed/derived from those exact bytes.

The accepted `resolved_config_hash` oracle is either:

1. a pure mapping snapshot/hash function in an independent validator, whose source/algorithm is accepted and hash-verified, run over the exact current container-visible bytes; or
2. a pre-frozen expected value bound to the accepted source/algorithm and exact mapping bytes during implementation acceptance.

The validator must choose one in its future Prompt and record its source identity. Any inability to bind expected hash to exact bytes plus accepted algorithm/source is HOLD. Static recomputation alone is diagnostic; record self-report alone is never PASS.

## 18. Raw-log collection and deterministic transport adapter

Future validation is bounded to one fresh full-container-ID-scoped observation interval. It must retain command/authority, start/end, exit status, raw transport bytes, byte length and raw SHA-256 before parse/selection/normalization; stdout/stderr or Docker log-stream boundaries must be explicit. Missing, truncated, unbound or failed collection is HOLD. Arbitrary terminal display text is not raw authority.

The application message is exactly:

```text
collector_runtime_loaded_json=<JSON_OBJECT>
```

The adapter must derive transport-prefix rules from the accepted deployed source and actual logging configuration; identify the application component only on a complete raw-line boundary; HOLD on multiple marker candidates or unremovable prefix. It must preserve selected raw line, exact application component and exact payload bytes/hashes separately. Adapter extraction and JSON parsing are separate stages. Marker substring search inside arbitrary raw bytes is not PASS.

## 19. A–H bounded evidence plan

Future runtime Prompt must choose one exact repository path for each class; R47 does not create or choose those paths.

| Class | Producer / input authority | Required content and byte identity | Validation / failure / role | Secret boundary |
| --- | --- | --- | --- | --- |
| A raw transport | bounded collector/log capture from current full container ID | exact raw bytes, interval, length, SHA-256 | collection boundary and hash before parse; unavailable/truncated → HOLD; raw authority | no credentials |
| B metadata | validator/orchestrator | authority/command, image/container/StartedAt/process, interval, A binding | schema and identity checks; missing/mismatch → HOLD; correlation | redact credentials |
| C selected raw line | adapter from A | byte offset or stable ordinal, exact line bytes/hash | selection only from A; ambiguous/missing → HOLD; lineage | no arbitrary terminal text |
| D application message | transport adapter from C | exact prefix-stripped bytes beginning with literal, length/hash | complete-line/prefix rule; multiple/unstrippable → HOLD; extraction evidence | no raw PLC/secret fields |
| E JSON payload | parser input after exactly one delimiter in D | all remaining exact bytes, length/hash; no trim/reserialize | strict JSON boundary; malformed/partial/duplicate → HOLD; payload authority | no sensitive payload |
| F parsed v1 object | strict parser from E | exact object, 11 keys, exact types/literals | duplicate members/wrong types/missing/extra/unknown → HOLD; derived evidence | reject prohibited fields |
| G comparison terminal | independent expected-value calculator + F | expected source, actual, comparison, lineage, PASS/HOLD | every mismatch/unproven relation → HOLD; terminal comparison | do not store secrets |
| H manifest | final locked validator | A–G exact paths, bytes, SHA-256 and final validation binding | post-validation change or missing member → HOLD; terminal manifest | no credentials |

A–H are bounded validation evidence, not retention, telemetry, audit or forensics infrastructure.

## 20. Future helper authority and execution lock

If the later bounded runtime gate uses a helper, its Prompt must declare exact helper source/test paths and forbid a second test-harness implementation. Sequence: create → syntax/compile → focused tests → final helper/test bytes and SHA-256 → execution lock → immutable helper → A–H from that version → manifest proves no post-validation change. Post-lock mutation is HOLD. R47 creates no helper/artifact/lock and adds no helper to the three-source allowlist.

## 21. Strict JSON parser oracle

The future parser must require exactly one complete application payload and reject duplicate JSON member names, non-object JSON, missing/extra keys, unknown schema/event, boolean-as-integer, numeric strings, malformed/partial payloads, and two-or-more matching records. It must validate exact lowercase hashes and RFC3339 UTC `Z`, preserve internal strings without trim/normalization, validate extra keys before any discard, and never replace exact payload bytes with reserialized JSON. Zero matching records, ambiguous lines or unavailable log collection are HOLD, not diagnostic PASS.

## 22. Ordered fail-closed terminal runtime-validation algorithm

```text
1. verify accepted implementation commit and exact source/path manifest;
2. verify accepted full top-level image ID and build/deployment binding;
3. fresh observe full active image, full container ID, StartedAt and Collector main process;
4. verify accepted image == active image and process belongs to that container/start boundary;
5. fresh read current container-visible mapping bytes and derive independent raw/schema/config/line/count values;
6. derive the resolved-config expected hash using the selected non-self-referential oracle;
7. capture one bounded raw log artifact with interval, exit status and raw identity;
8. select exactly one raw line, application message and payload with reversible A–E lineage;
9. parse one exact v1 object and reject duplicate/malformed/ambiguous records;
10. compare every terminal/correlation field and timestamp/PID namespace relation;
11. verify A–H bytes/hashes/manifest and no post-final-validation mutation;
12. issue PASS only if every step is proven; any failure, missing fact, mismatch or ambiguity issues HOLD.
```

No step may be skipped while retaining a partial PASS. A PASS from this algorithm still requires separate PM acceptance before the `RUNTIME-LOADED` label is used.

## 23. Terminal PASS field matrix

| Field/fact | Actual source | Expected source | Comparison / terminal authority | Mismatch outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| schema/event | parsed v1 object | frozen R42/R45 literals | exact strings | HOLD | F/G |
| mapping path | record + active mount | approved path + fresh active observation | exact path and bytes-read lineage | HOLD | B/F/G |
| raw mapping SHA | record | hash of current container-visible bytes | lowercase 64-hex and exact equality | HOLD | B/G |
| mapping schema/config/line | record | independent parse of same bytes; canonical snapshot line | exact values and same-snapshot lineage | HOLD | B/G |
| read-plan count | record | `1 + all configured stations`, disabled included | integer and exact count/scope set | HOLD | B/G |
| resolved hash | record | independent accepted algorithm over same bytes, or bound frozen value | exact lowercase hash, non-self-referential | HOLD | B/G |
| collector main time | record | fresh StartedAt and observation time | `StartedAt <= time <= observation` and UTC `Z` | HOLD | B/G |
| container PID | record | same-namespace fresh Collector main PID | exact integer and executable ownership | HOLD | B/G |
| accepted/active image | build/deploy + active inspect | accepted full image ID | full immutable ID equality | HOLD | B |
| active container/start/process | fresh observation | current full container and StartedAt boundary | ownership/non-stale/unique | HOLD | B |
| raw line/message/payload | A–E | reversible raw-to-parsed lineage | exactly one, exact bytes/hashes | HOLD | A–E/H |
| record cardinality | bounded current log envelope | exactly one matching v1 record | 1 and no duplicate/ambiguous match | HOLD | A/C/F/G |

## 24. Failure matrix

| Failure ID / condition | Classification | Terminal behavior |
| --- | --- | --- |
| source commit/path manifest mismatch | current claim blocker | HOLD before image/runtime claim |
| accepted vs active full image mismatch; tag/Config.Image/short ID only | current claim blocker | HOLD |
| stale log after restart, foreign container, absent/ambiguous process | current claim blocker | HOLD |
| host PID compared directly to container PID; missing namespace mapping | current claim blocker | HOLD |
| mapping unavailable/changed/symlink/path drift; raw hash mismatch | current claim blocker | HOLD |
| resolved hash cannot be independently bound to exact bytes/accepted algorithm | current claim blocker | HOLD |
| canonical line/routing line mismatch; count/scope mismatch | application/runtime claim blocker | HOLD; no success record for implementation negative |
| record absent, duplicate, malformed, partial or wrong schema/event | current claim blocker | HOLD |
| duplicate JSON members, wrong types, bool/int confusion, numeric string | current claim blocker | HOLD |
| timestamp ordering or UTC format failure | current claim blocker | HOLD |
| raw artifact, selected line, message, payload or manifest identity mismatch | current claim blocker | HOLD |
| `Thread.start()` failure after record | runtime correlation failure | HOLD; record is not standalone PASS |
| log collection unavailable/truncated/unbound | evidence unavailable | HOLD |
| helper/artifact changed after execution lock/final validation | evidence integrity failure | HOLD |
| worker health, PLC connectivity, DB health, persistence, ACK/read_done, machine state | out of current RUNTIME-LOADED claim | diagnostic/out of claim; never PASS through v1 record |
| long-term retention, generic audit/forensics, telemetry taxonomy | out of current scope | diagnostic/recommendation only; not blocker |

## 25. Runtime record non-claims

The v1 record does not prove worker thread health, PLC connectivity, DB health, event persistence, accepted station-event facts, ACK/read_done, machine-state truth, UI production truth or `PRODUCTION-ACCEPTED`. It must not be inserted into production DB or accepted-fact projections. `RUNTIME-LOADED` remains runtime configuration/process evidence only.

## 26. MVP proportionality and stopping rule

Classification：`MVP-ALIGNED WITH BACKLOG ITEMS`。

The combined contract supports the minimum process-bound runtime-loaded mapping/config claim and blocks only concrete cross-line, stale/foreign image/process, self-reported-hash or normalized-log false PASS. A–H is one bounded set; the helper is a validation tool. No API, DB persistence, telemetry, generic registry, audit/forensics, retention, v1 field or production-fact requirement was added.

After terminal invariants and independent oracles are covered, diagnostic completeness/theoretical combinations move to backlog. No new blocker without a direct false-PASS, stale-truth, unsafe-process or evidence-confusion consequence.

## 27. New credible blocker assessment and recommendations

### Blockers

`none`.

The current three-source/two-test allowlist is necessary/sufficient; R42/R45 precedence is unambiguous; field, source/image/process, PID namespace, mapping/hash, raw-log, A–H, parser and terminal algorithm oracles are independently expressible and fail-closed. R47 does not require an additional current source/test path.

### Bounded non-blocking recommendations

1. Future implementation acceptance should explicitly assert that the first context consumer remains consumed after later constructor failure.
2. Future runtime helper should keep transport adapter, application-message extractor and JSON parser as separately reviewable stages while preserving A–H byte lineage.
3. Keep `record_emitted_at` and sorted scope list out of v1 unless PM later identifies a concrete false-PASS risk.
4. Keep source/image/config/process binding and A–H paths in later independent authority prompts; do not add them to current application files.

These recommendations do not authorize repair, implementation, test execution or allowlist expansion.

## 28. Changed-path and final Git/index/untracked audit

唯一 task-owned changed path is:

```text
docs/reports/sprint4_d2_r7b_i1_r47_runtime_loaded_observability_verification_planning_review.md
```

R42–R46、source/test/config/Dockerfile/Compose、status、roadmap、handoff、PM rules、Batch D/E and all other paths remain untouched. No Git index or remote state was changed.

The post-write audit must and did preserve:

```text
HEAD == origin/main == ce22ca71eff0548aa064129c160f7041603855e7
HEAD^ == 35c50b1eb0f76d8b3361e8c122448ad03899559b
ahead / behind == 0 / 0
tracked dirty == empty
cached == empty
initial untracked == 308
final untracked == 309
unknown/missing expected paths == 0 / 0
R47 == regular UTF-8 NON-SYMLINK UNSTAGED UNTRACKED
```

Because embedding a file's own final SHA-256 changes that file's bytes, the canonical R47 bytes/SHA-256 are the detached post-write read-only identity returned in the Chat manifest. This is not a second artifact and does not change the exact allowlist.

## 29. Next gate and Thread context

```text
R47 independent Verification planning review WRITTEN
→ ChatGPT PM durable intake only
→ PM may issue final planning-contract acceptance
→ implementation still requires a separate exact authority
```

continue current Thread: `no`

new Thread recommended: `yes` for the next independently authorized phase; this Verification planning review is terminalized. R47 PASS, R46 PASS, R43 PASS and all recommendations do not authorize implementation, Git, build, deploy, runtime validation, `RUNTIME-LOADED` acceptance or production accepted-fact work.

## 30. R47 final identity

```text
path: docs/reports/sprint4_d2_r7b_i1_r47_runtime_loaded_observability_verification_planning_review.md
encoding: UTF-8
file type: regular
symlink: NO / NON-SYMLINK
index: UNSTAGED / UNTRACKED
bytes/SHA-256: detached post-write read-only audit in Chat manifest
```

End state：`VERIFICATION-PLANNING-REVIEWED / WRITTEN ONLY`。
