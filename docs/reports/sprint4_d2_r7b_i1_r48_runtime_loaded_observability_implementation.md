# Sprint 4 D2-R7B-I1 R48 Minimal Process-Bound Runtime-Loaded Observability Implementation

## 1. Task identity and terminal decision

Task: D2-R7B-I1 R48 — Implement Minimal Process-Bound Runtime-Loaded Observability
Executing Thread: Architecture / Integration
New Authority ID: PM-D2-R7B-I1-R48-RUNTIME-LOADED-OBSERVABILITY-IMPLEMENTATION-260730-1256
Report delivery: REPOSITORY_DURABLE_REPORT
Report path: docs/reports/sprint4_d2_r7b_i1_r48_runtime_loaded_observability_implementation.md
Terminal decision: PASS / IMPLEMENTED LOCALLY

This result means only that the exact local source/test/report implementation was written and the permitted local checks passed. It does not mean independent review, PM acceptance, Git closeout, build, deploy, runtime validation, RUNTIME-LOADED acceptance, or PRODUCTION-ACCEPTED.

## 2. Authority boundary and non-inheritance

This was a one-shot authority. The expired authority PM-D2-R7B-I1-R48-RUNTIME-LOADED-OBSERVABILITY-IMPLEMENTATION-260730-1149 was not reused. No old Thread, PM window, Prompt, or authority was inherited.

Authority properties were AUTHORIZED ONCE; ARCHITECTURE / INTEGRATION IMPLEMENTATION; LOCAL SOURCE / TEST / REPORT WRITE ONLY; EXACT ALLOWLIST; NO GIT, BUILD, DOCKER, COMPOSE, REMOTE, SSH, RUNTIME VALIDATION, A–H EVIDENCE, or PRODUCTION ACCEPTANCE AUTHORITY; NOT REUSABLE. The authority was consumed at the first allowlist write.

## 3. Required reading order

The following were read completely and in order:

1. docs/thread_handoff/pm_operating_rules.md
2. docs/thread_handoff/chatgpt_pm_handoff_260730-1203.md
3. docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md
4. docs/reports/sprint4_d2_r7b_i1_r45_runtime_loaded_evidence_scope_reset_contract.md
5. docs/reports/sprint4_d2_r7b_i1_r43_process_bound_runtime_loaded_observability_reliability_rereview.md
6. docs/reports/sprint4_d2_r7b_i1_r46_runtime_loaded_evidence_data_quality_rereview.md
7. docs/reports/sprint4_d2_r7b_i1_r47_runtime_loaded_observability_verification_planning_review.md
8. docs/reports/sprint4_d2_r7b_i1_r44_process_bound_runtime_loaded_observability_data_quality_review.md
9. collector/app/main.py
10. collector/app/services/event_collector.py
11. collector/app/plc/mapping.py
12. collector/tests/test_event_collector_reliability.py
13. tests/test_collector_station_event_runtime_source.py

R42 remains the base contract. R45 supersedes R42 only for canonical line identity and selected routing equality, later source/image/config/process binding, and later raw-log/application-message/payload/parsed evidence identity. R44 remains historical blocker origin only.

## 4. Initial live Git recovery

Before any task-owned write:

    root /Users/chenjie/Documents/MES/edge-mes-demo
    branch main
    HEAD 4a733d7995a94398ade693822662ebd2b22f9d3d
    origin/main 4a733d7995a94398ade693822662ebd2b22f9d3d
    HEAD^ ce22ca71eff0548aa064129c160f7041603855e7
    ahead / behind 0 / 0
    tracked dirty empty
    cached empty
    git diff --check PASS
    git diff --cached --check PASS
    untracked 309

Initial composition was Batch D 300, Batch E frontend/next-env.d.ts 1, and R40–R47 reports 8; unknown 0. Batch D/E were not read, changed, deleted, moved, or reclassified. .venv/bin/python existed and was executable; no dependency installation or environment creation occurred.

## 5. Initial exact identities

Current handoff: docs/thread_handoff/chatgpt_pm_handoff_260730-1203.md, 26183 bytes, SHA-256 c9a7ed7283d4574578e1608fc6891bdb91373d97bac3191740863917af3ad8e1, regular NON-SYMLINK tracked clean file. Live Git identity overrides the handoff's older authoring-time untracked wording.

Initial source/test identities:

    collector/app/main.py: 2073 / a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090
    collector/app/services/event_collector.py: 16342 / eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f
    collector/app/plc/mapping.py: 17433 / c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098
    collector/tests/test_event_collector_reliability.py: 12774 / 462656c9d9146e492b52296ca2b40a1f37fe40cba95a2068e4c6317fd33c2472
    tests/test_collector_station_event_runtime_source.py: 30571 / 7d9d894eaa784e36c729e824ee87de73a863765089fd12e388bc926164229fd7

Contract/review identities:

    R42 32319 / dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165
    R45 13786 / 8fd646f24565bbcb27aa9063038774fee3b5398d66566f961bee296ffff02ef2
    R43 30244 / 95b2e63c4879fb5af6920b262300566c577612dd1753b13bf59928c1417338e8
    R46 23703 / f460fef43d975de41ed624fa49d8a1a8dcd5246b4ae55b222189f40703914b81
    R47 34592 / 4de247e350eb595077219856cf63b0319ee83d14026b6beaaf7c5d83211a0ae4
    R44 43036 / 3b4d1f3451d0b0036e5530bc83eb35b90ee2b6d140b0a2799b82df1ada035bfa

## 6. R42 + R45 final contract interpretation

Candidate A remains a one-shot, process-bound, main-process startup application assertion. It proves that the main-entry process consumed startup context, one raw mapping load completed hash/decode/parse, runtime and resolved snapshots agree, the full read-plan list passed validation, canonical line equals the selected routing projection, worker construction completed, and the record was emitted synchronously before Thread.start.

It does not prove thread start or health, PLC connection/read, DB health/write, production event or fact, ACK, read_done, image/container/process deployment, RUNTIME-LOADED acceptance, or PRODUCTION-ACCEPTED.

## 7. Implementation summary: main.py

main.py now captures one RFC3339 UTC timestamp with literal Z and os.getpid() at the first executable main boundary. The same mandatory context is passed to EventCollectorWorker only when event_collector_enabled() is true. Thread creation and start remain after worker construction.

## 8. Implementation summary: mapping.py

load_edge_mapping() resolves the exact regular non-symlink path, performs one raw-byte read, hashes those exact bytes, explicitly UTF-8 decodes them, parses that same decoded text, and binds canonical path plus lowercase 64-hex raw SHA to EdgeMapping. Duplicate YAML keys fail closed. parse_edge_mapping() direct callers and existing semantic hash behavior remain available.

## 9. Implementation summary: event_collector.py

CollectorStartupContext has single-use consume semantics. Missing, reused, invalid timestamp, bool/non-positive PID, and PID mismatch fail closed; constructor failure after consumption leaves the context consumed. Worker validates mapping/runtime/resolved hashes and schema/config/line projections, exact PLC selection, canonical line equality, and list-first plan scope/cardinality invariants. It constructs exactly one v1 object and emits it with one synchronous logger call as the constructor's final required action.

## 10. Same-byte raw identity

mapping_content_sha256 is calculated directly from raw bytes and cannot use read_text(), newline normalization, or re-encoding. The YAML parser receives raw_bytes.decode("utf-8") from that same read. Invalid UTF-8, malformed YAML, duplicate key, non-mapping root, semantic failure, or hash failure produces no success record. Raw SHA and resolved_config_hash remain distinct authorities.

## 11. Startup context single-use semantics

The context is marked consumed before later validation and construction. main does not recover it from environment; worker does not generate it; poll_once(), run_forever(), exception handlers, fallback, retry, and replay do not emit it. A second consumer or reuse fails closed.

## 12. Canonical line authority

Canonical line_id is RuntimeMappingSnapshot.line_id / ResolvedConfigSnapshot.line_id and is bound to the same resolved hash. The selected PLC entry's line_id is routing projection only. Missing, empty, ambiguous, or mismatched routing identity fails before serialization; the record uses the canonical snapshot value and self.line_id remains consistent with it.

## 13. List-first read-plan validation

configured_station_ids, expected_scopes = ["line"] + configured_station_ids, and generated_scopes are retained before dict conversion. Checks cover reserved line collision, duplicate configured IDs, duplicate generated scopes, exact positive cardinality, exact scope multiset, exactly one line plan, missing/extra scope, and one-to-one station materialization. Disabled configured stations remain counted. read_plan_count is the validated original list length.

## 14. Exact v1 schema and serialization

Exact keys are evidence_schema_version, event_type, mapping_path, mapping_content_sha256, mapping_schema_version, config_version, line_id, read_plan_count, resolved_config_hash, collector_main_started_at_utc, and process_pid.

Literals are edge-mes/collector-runtime-loaded/v1 and collector_runtime_loaded. Serialization uses ensure_ascii=False, sort_keys=True, separators=(",", ":"), and allow_nan=False. Hashes are lowercase 64-hex; count and PID are JSON integers but not bool; timestamp is RFC3339 UTC with Z. The application message is exactly collector_runtime_loaded_json=<COMPACT_JSON>. No DSN, credential, PLC payload, station payload, DB result, accepted fact, ACK/read_done, production, image, or container claim is included.

## 15. Emission ordering and failure boundary

The order is capture context, normal main setup, enabled worker construction including all validation and the unique record emission, Thread construction, then Thread.start. Serialization or logger failure propagates before thread creation/start. Failure paths emit no success record and do not PLC connect/read/write, DB connect/write, accepted-fact, ACK, or read_done mutate. Existing poll/persistence/ACK/read_done code was not changed.

## 16. Focused test matrix: reliability file

collector/tests/test_event_collector_reliability.py covers main context handoff, emission-before-thread, exactly-one record, exact key/literals/compact JSON, disabled station count, duplicate/missing/extra/cardinality/scope failures, duplicate station ID, canonical/routing equal/mismatch/missing/empty/ambiguous cases, mandatory/PID/single-use context, constructor-failure consumption, serialization/logger propagation, and no PLC/DB/ACK/read_done side effects. Existing persistence and ACK/read_done regression tests remain.

## 17. Focused test matrix: runtime-source file

tests/test_collector_station_event_runtime_source.py covers one-read raw bytes, exact-byte hash, same decoded/parsed text, canonical path, lowercase 64-hex SHA, raw-byte newline change versus semantic hash stability, invalid UTF-8, malformed/duplicate YAML, and existing raw payload lineage. Local/static/manual/synthetic objects are not described as runtime-loaded accepted facts.

## 18. Allowed validation commands and exact results

py_compile command:

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile collector/app/main.py collector/app/services/event_collector.py collector/app/plc/mapping.py collector/tests/test_event_collector_reliability.py tests/test_collector_station_event_runtime_source.py

Result: PASS, exit code 0. It was executed with the permitted environment and no dependency/environment mutation.

Focused pytest A command:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=collector:. .venv/bin/python -m pytest collector/tests/test_event_collector_reliability.py -q

Result: PASS, 21 passed, 6 subtests passed in 0.20s, exit code 0.

Focused pytest B command:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_station_event_runtime_source.py -q

Result: PASS, 56 passed in 0.14s, exit code 0.

## 19. Exact changed-path audit

Before report creation, git diff --name-only contained exactly:

    collector/app/main.py
    collector/app/plc/mapping.py
    collector/app/services/event_collector.py
    collector/tests/test_event_collector_reliability.py
    tests/test_collector_station_event_runtime_source.py

Cached path set was empty. No excluded path changed. This report is the only sixth task-owned path.

## 20. Forbidden-action counters

    Git mutation: 0
    build/package/npm: 0
    Docker/Compose: 0
    remote/SSH/network/curl: 0
    DB connection/query/write/migration: 0
    PLC/V-PLC connection/read/write
: 0
    runtime validation/application startup/A–H evidence: 0
    Batch D/E handling or mutation: 0

The focused tests used local fake/isolated objects only and do not constitute runtime or production evidence.

## 21. Final Git/index/untracked audit

Immediately after this report write, the required final read-only audit will verify:

    HEAD == origin/main == 4a733d7995a94398ade693822662ebd2b22f9d3d
    branch == main
    ahead / behind == 0 / 0
    tracked dirty == the five implementation source/test paths only
    cached == empty
    git diff --check == PASS
    git diff --cached --check == PASS
    untracked == 310
    composition == Batch D 300 + Batch E 1 + R40–R47 8 + R48 1
    unknown untracked == 0

The report must remain regular UTF-8, NON-SYMLINK, UNSTAGED, and UNTRACKED. Its final bytes/SHA-256 are returned from the detached post-write audit rather than embedded self-referentially.

## 22. Product/evidence boundary

Current product state remains ACTIVATED = YES, STATIC_MAPPING_INITIALIZED = YES, RUNTIME-LOADED = NO, PRODUCTION-ACCEPTED = NO. Local implementation and focused tests do not establish independent review, image/build/deploy/active process, fresh container log/mapping evidence, RUNTIME-LOADED = YES, PLC, DB, persistence, ACK, read_done, or production acceptance.

## 23. Blockers and bounded recommendations

Implementation blockers are none if the final audit preserves the exact allowlist and expected untracked composition. Recommendations are bounded to a fresh independent Reliability implementation review of single-use, constructor ordering, scope validation, canonical line equality, serialization, and no-side-effect behavior; later separately authorized Data Quality/Verification gates may handle source/image/config/process and A–H evidence. record_emitted_at, sorted scope list, generic telemetry, retention, audit/forensics, and production accepted-fact work remain out of scope.

## 24. MVP alignment

Classification: MVP-ALIGNED WITH BACKLOG ITEMS. This work directly supports the approved minimal process-bound runtime-loaded mapping/config identity claim and prevents concrete cross-line, stale/foreign, raw/normalized, duplicate-scope, and constructor-side-effect false PASS. It adds no API, DB persistence, telemetry, generic registry, audit/forensics, retention, runtime topology, PLC/ACK/read_done, or production-fact capability.

## 25. Next gate and stop point

After this durable report and final read-only audit, stop immediately. The only next gate is R48 local implementation WRITTEN → ChatGPT PM durable intake → independent Reliability implementation review. Do not enter Data Quality review, Verification review, Git acceptance, stage/commit/push, build, Docker/Compose, remote, runtime validation, A–H evidence, RUNTIME-LOADED acceptance, or PRODUCTION-ACCEPTED acceptance.

## 26. Thread context assessment and terminal vocabulary

This is a long durable implementation report. The current Thread is terminalized; continue current Thread: no; new Thread recommended: yes, because the next review requires fresh Reliability authority and must not inherit this authority.

    LOCAL IMPLEMENTATION WRITTEN
    FOCUSED TESTS PASSED
    NOT REVIEWED BY INDEPENDENT THREADS
    NOT STAGED
    NOT COMMITTED
    NOT PUSHED
    NOT BUILT
    NOT DEPLOYED
    NOT RUNTIME-VALIDATED
    RUNTIME-LOADED = NO
    PRODUCTION-ACCEPTED = NO
