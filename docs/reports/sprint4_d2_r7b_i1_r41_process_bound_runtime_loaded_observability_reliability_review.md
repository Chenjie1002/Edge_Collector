# Sprint 4 D2-R7B-I1 R41 Process-Bound Runtime-Loaded Observability Reliability Planning Review

## 1. Report identity and bounded authority

- Task: `D2-R7B-I1 R41 — Independently Review R40 for False-PASS, Failure-Closure and Process-Provenance Risks`
- Thread: `Reliability`
- Authority ID: `PM-D2-R7B-I1-R41-PROCESS-BOUND-RUNTIME-LOADED-RELIABILITY-REVIEW-260730-0904`
- Delivery: `REPOSITORY_DURABLE_REPORT`
- Exact output: `docs/reports/sprint4_d2_r7b_i1_r41_process_bound_runtime_loaded_observability_reliability_review.md`
- Authority: `AUTHORIZED ONCE / INDEPENDENT RELIABILITY REVIEW / LOCAL DOCS WRITE ONLY / NO REPAIR / NO SOURCE OR TEST WRITE / NO RUNTIME AUTHORITY / NOT REUSABLE`

**Conclusion: `HOLD / RELIABILITY_BLOCKERS_REQUIRE_ARCHITECTURE_REPAIR`.**

R40 is a PM-verified **uncommitted** planning input only. It is `WRITTEN / PM-REVIEWED / PM-VERIFIED / UNTRACKED / UNSTAGED / NOT COMMITTED`, and is not implementation authority. This review neither repairs R40 nor authorizes implementation, tests, lifecycle activity, or a later review.

Evidence boundary:

```text
REVIEWED
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
```

## 2. Fresh recovery and input identities

Read-only recovery at the real checkout established:

| Field | Result |
| --- | --- |
| root / branch | `/Users/chenjie/Documents/MES/edge-mes-demo` / `main` |
| `HEAD` | `ce22ca71eff0548aa064129c160f7041603855e7` |
| `origin/main` | `ce22ca71eff0548aa064129c160f7041603855e7` |
| `HEAD^` | `35c50b1eb0f76d8b3361e8c122448ad03899559b` |
| ahead / behind | `0 / 0` |
| tracked dirty / cached | empty / empty |
| worktree and cached diff checks | clean / clean |
| initial untracked | `302` |
| initial visible composition | Batch D aggregate `300`, Batch E `frontend/next-env.d.ts` `1`, R40 `1` |

The live baseline matches the Prompt. The move from older R35/R36 authoring baselines to `ce22ca7` is explained by the committed PM handoff; it is not source or authority drift. Older `current_status.md` and `roadmap.md` were treated as historical snapshots only. Current accepted state remains `ACTIVATED=YES`, `STATIC_MAPPING_INITIALIZED=YES`, `RUNTIME-LOADED=NO`, `PRODUCTION-ACCEPTED=NO`.

R40 was reverified before this output write:

| Input | Bytes | SHA-256 | File state |
| --- | ---: | --- | --- |
| `docs/reports/sprint4_d2_r7b_i1_r40_process_bound_runtime_loaded_observability_plan.md` | 23337 | `280cb553f5fc8bf81c92e689493782749534293de4876a05d88063080caabb91` | UTF-8 regular non-symlink; untracked and unstaged |

The R41 output was initially absent, non-symlink, untracked, and unstaged. No pre-authority repair window exists.

## 3. Source identity and reviewed boundary

All listed source, test, image-context, and mapping inputs were byte-compared with current `HEAD`; all matched. Relevant current identities are:

| Path | Bytes | SHA-256 | HEAD blob |
| --- | ---: | --- | --- |
| `collector/app/main.py` | 2073 | `a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090` | `96c43fda428b943efc62bcb5b8c09b4ff8b25332` |
| `collector/app/config.py` | 764 | `4f01689a34fb494f7ea84cf74b303ce8aed0957d1dd9c05fc7773563cd577afc` | `d140d24829137c01dce2d39c3ba848ff586d1d73` |
| `collector/app/services/event_collector.py` | 16342 | `eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f` | `e2ce5fead0de7a04eb60795eb95316b3b9b873a8` |
| `collector/app/services/resolved_config_registry.py` | 17337 | `1844449a3f99e9ca53bddc8063c151fb0f889920597bccb170f5e62f3715db2c` | `77d32a3153bba991dc1880da8262d770df2b0480` |
| `collector/app/plc/mapping.py` | 17433 | `c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098` | `6b35adb5203de0434ad5e069d8634f7a14b1b9f1` |
| `collector/app/plc/read_plan.py` | 1482 | `fd5f675501444ed8378d6a296c3ed3d8769af97a1f19d1e95f3c00d76d4b02d6` | `10c6d1f51bfa379b652760a5cba37b5f8723435c` |
| `collector/tests/test_event_collector_reliability.py` | 12774 | `462656c9d9146e492b52296ca2b40a1f37fe40cba95a2068e4c6317fd33c2472` | `27d64d29fd6cae7db3ef51cf385fd5916a6eb140` |
| `collector/tests/test_snap7_reliability_integration.py` | 8025 | `5cc75a9cd37eeee6f3a80e29d186b55b3aab3a335898d77e204a9d653f686b54` | `51348ddf5195e428b61fcbac2b1fe40c4ea58d97` |
| `tests/test_collector_station_event_runtime_source.py` | 30571 | `7d9d894eaa784e36c729e824ee87de73a863765089fd12e388bc926164229fd7` | `f14a4de64a6a17d427af6be08594640249e521f2` |
| `tests/test_collector_container_packaging.py` | 941 | `351e80a76a53f742258e91196b109172de7b43dc3fa359e63ef44c9e7ad9c26e` | `d13770db1bd7f9edac95aa6e33edab48636ab077` |
| `collector/Dockerfile` | 218 | `e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839` | `7d89c84349a5e86f673767e25ac52da7013cc456` |
| `docker-compose.yml` | 5698 | `c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66` | `7c71c8cb64f3790e02914ff22f8ab4f76dfb6084` |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` | `b46a637f23c761d0a4c3fe048b3b7480a3dec2ce` |

### 3.1 Startup and failure boundary map

`main()` currently performs `load_config`, source construction, `Storage`, and `EventDetector` construction before it constructs `EventCollectorWorker`; it then creates and starts the daemon thread. Only afterwards does the main snapshot loop call `source.read`, `ensure_machine`, `insert_snapshot`, and `detector.process`. The reviewed exact paths establish call ordering, not a fresh runtime fact.

The worker constructor performs, in order: `Storage(dsn)` construction; mapping read/parse; PLC/line/rack/slot derivation; `ZoneInfo`; resolved snapshot construction and hash validation; in-memory registry construction; `snap7.client.Client()` construction; `build_read_plans`; dict-by-scope conversion; and line/station runtime materialization. `Thread.start`, `run_forever`, `_ensure_connected`, `connect`, line/station `db_read`, status/transaction persistence, `db_write`, and ACK/read_done handling occur later. A constructor-time record after a complete pre-emission check is therefore before those explicit worker I/O calls.

`Storage`, source, and detector constructors have already been invoked before the planned record. Their internals were deliberately not inspected because they are outside the exact source-read allowlist. R40 must not overstate Candidate A as proof that *no constructor anywhere in main* could have performed I/O; its intended and supportable claim is narrower: complete mapping/worker initialization before worker loop PLC/DB/ACK activity.

## 4. Failure-mode matrix

`success record` means a record satisfying the planned success grammar. `false PASS` means a later validator could credibly accept it as active-main `RUNTIME-LOADED`, not merely that startup is unavailable.

| Failure mode | Can emit success record? | Can create false PASS? | Required prevention | Authority |
| --- | --- | --- | --- | --- |
| mapping file read/decode/parse failure | no | no | code/test: propagate before emission | none |
| mapping semantic or decoder/hash failure | no | no | code/test: existing construction remains pre-emission | none |
| resolved snapshot mismatch | no | no | code/test: propagate `CONFIG_HASH_MISMATCH` before emission | none |
| timezone construction failure | no | no | code/test: `ZoneInfo` remains pre-emission | none |
| Snap7 client construction failure | no | no | code/test: constructor failure before emission | none |
| missing line read plan | no, after repair | yes in current source if merely recorded | code/test: require line scope before emission | diagnostic in R40, covered by scope blocker |
| configured station plan missing | no, after repair | yes in current source because comprehension drops it | code/test: exact coverage check before emission | diagnostic in R40, covered by scope blocker |
| duplicate station IDs or duplicate plan scopes | yes under R40's underspecified dict conversion | **yes** | code/test: detect duplicate expected IDs and duplicate generated scopes before dict conversion | **blocker B1** |
| constructor exception before record | no | no | code/test: no catch-and-success fallback | none |
| record serialization or logger call raises | no, if propagation is preserved | no | code/test: propagate; no fallback/retry | none |
| handler buffers, loses, truncates, or collector misses record | record may have been attempted | no if absence/malformed is HOLD | later validation: exact log-scope, absence/malformed HOLD | none |
| required constructor step after record | must be no | yes if present | code: record must be final constructor action before return | none if frozen in repair |
| worker constructor succeeds but `Thread.start()` fails | yes | yes without active-process correlation | later validation: exact active-main PID/container/start boundary; stale record rejected | **blocker B2** |
| worker thread immediately fails | yes | no if record claim is initialization-only and active process remains proven | later validation; do not reinterpret record as health/PLC/DB evidence | none |
| main and worker lifecycles are separate | yes | yes if record is treated as loop-health | terminal definition limits claim to loaded initialization; later validation proves active main | none |
| container restarts while old logs remain | old record remains | yes without start-boundary correlation | later validation: full container ID, current `StartedAt`, active PID, scoped logs | **blocker B2** |
| duplicate worker construction | yes | **yes** | single-use startup context plus duplicate-is-HOLD validation | **blocker B2** |
| repeated `main()` in one Python process | yes | **yes** unless scope is fixed | exactly-one is per `main()` invocation; same active container/start may accept one only | **blocker B2** |
| manual/test/probe worker construction | yes if it can obtain a usable context | **yes** without active-main PID correlation | required context and external active-main PID equality | **blocker B2** |
| stale, duplicate, or ambiguous record | possible | **yes** | strict parser; exactly one matching record for current boundary; otherwise HOLD | **blocker B2/B3** |
| malformed/partial record | possible log fragment | no if rejected | strict whole-message parser; malformed/partial HOLD | **blocker B3** |
| log rotation/collection makes record unavailable | no observable record | no if absence is HOLD | later validation only; no new retention system | none |

## 5. Exactly-one, provenance, and timestamp decisions

### 5.1 Exactly-one scope

The minimum valid scope is **one success record per invocation of `app.main.main()` for the active Collector Python process**. A normal container start can have one such invocation; a later container restart is a new boundary. It is not per log stream, polling iteration, retry, worker object, or arbitrary Python process.

For the later runtime-validation envelope, exactly one *matching* record must exist in the full active-container-ID log stream for the current `StartedAt` to observation interval. Zero, two or more, parser ambiguity, or a record associated with a different PID/start boundary is `HOLD / NOT RUNTIME-LOADED`. A legitimate restart is distinguishable only by a newly observed container start boundary and active process; it does not make two matching records for one boundary acceptable.

R40 does not yet freeze the required single-use context/duplicate rule, so duplicate workers or repeated `main()` can create several valid-looking lines. This is B2, not a diagnostic.

### 5.2 Active-main-process provenance

Timestamp and PID values alone are application claims, not sufficient provenance. A manual worker, isolated process, test, or future caller can produce syntactically identical values. The smallest fail-closed repair is a mandatory, non-default startup-context object created once at the first executable boundary of `main()`, supplied only to the one worker constructed on that path, carrying the main PID and main-entry timestamp, and consumed once by the emission path. The worker must reject a context whose PID is not `os.getpid()` and must have no record-emitting default context.

This object is not cryptographic and is not a cross-process registry; it prevents accidental alternate caller paths from silently inheriting a record capability. It cannot by itself prove container ownership against arbitrary in-container code. Therefore later bounded validation remains terminal for provenance: it must fresh-observe full active container ID, image ID, `StartedAt`, and active Collector-main PID/process identity; collect only that container's logs; and require equality with the record PID. A missing, changed, or unprovable process identity is HOLD. `Thread.start()` failure, an immediately failed thread, old logs, and `docker exec`/probe records then cannot establish PASS.

### 5.3 Timestamp semantics

R40's value is captured at Python `main()` entry, not at OS process birth. Rename it to `collector_main_started_at_utc`; do not retain `process_started_at_utc`, whose ordinary reading is OS process creation. It is a RFC3339 UTC application claim with `Z` output and a parseable calendar timestamp. The later validator must require the record time to be no earlier than the fresh container `StartedAt` and no later than its own bounded observation. No invented millisecond tolerance is authorized. A malformed value, non-UTC form, impossible ordering, or clock change that prevents those relations is fail-closed HOLD; this is not a clock-synchronization project.

## 6. Field-authority matrix

R40's table calls `process_pid` required yet its diagnostic paragraph calls it diagnostic-only. That conflict is a B2 blocker. The required repaired classification is:

| Category | Fields / facts | PASS/HOLD meaning |
| --- | --- | --- |
| terminal authority (application claim) | `evidence_schema_version`, `event_type`, `mapping_path`, `mapping_content_sha256`, `mapping_schema_version`, `config_version`, `line_id`, `read_plan_count`, `resolved_config_hash` | Missing, wrong, unexpected, or ambiguous value is HOLD. These establish the loaded mapping/read-plan claim only. |
| correlation authority | `collector_main_started_at_utc`, `process_pid`; externally observed full container ID, image ID, `StartedAt`, active main PID/process identity, and container-ID-scoped log envelope | Application correlation-field absence/mismatch is HOLD. External facts are supplied only by later authorized validation; they are not application assertions. |
| diagnostic-only | optional record-emission timestamp and sorted scope list | Never silently promote to terminal blocker. If present they must be non-sensitive and parseable; they cannot cure a missing terminal/correlation field. |

No DSN, credentials, host/port, raw bytes, raw/accepted payload, unit/DMC, event/DB data, ACK/read_done data, or production fact belongs in the record. `resolved_config_hash` is the semantic identity; do not emit an invented second semantic mapping hash.

## 7. Raw mapping identity and read-plan completeness

Current `load_edge_mapping` uses `Path(path).read_text()` before YAML parsing, so current code cannot prove that a proposed raw SHA came from the exact byte sequence parsed. R40 correctly includes `collector/app/plc/mapping.py`; its repair contract must say that one read obtains bytes, hashes those bytes, decodes those same bytes as UTF-8, and parses that decoded content. It must not perform a second read, normalize newlines, hash text re-encoding, or trust a substituted path. Decode/parse failure emits no record. Raw SHA is file-byte identity; `resolved_config_hash` is the validated semantic/resolved identity. They are complementary, not independent semantic authorities.

`mapping.py` is necessary and sufficient for that narrow raw-byte binding. An `EdgeMapping` extension must remain backward-compatible for existing callers/tests or be rejected under a separately authorized scope decision; R40 must not change mapping semantics merely to surface the byte identity.

Current `build_read_plans` produces a list, but the worker immediately turns it into `{plan.scope: plan}`. Duplicate scope keys overwrite before the current station comprehension, while a missing station is silently omitted. Before that conversion, repair must define:

```text
expected scopes = ["line"] + [station.station_id for station in mapping.stations]
```

Under current behavior, disabled stations remain in the required set because `build_read_plans` currently builds every listed station; changing disabled-station runtime behavior would be a separate scope decision. The constructor must reject: absent line plan; any station ID equal to `line`; duplicate station IDs; duplicate generated plan scopes; a plan count different from expected count; any missing expected scope; and any unexpected scope. It must only construct the dict and emit success after those checks. This neither connects PLC nor changes DB/ACK/read_done behavior.

R40 says “exact one-to-one coverage” but does not make cardinality/duplicate-before-dict rejection explicit and its acceptance list omits duplicate ID/scope cases. B1 is therefore a credible false-PASS blocker.

## 8. Logging and parser boundary

The current `basicConfig` prefixes ordinary logger messages with timestamp and level. “Structured JSON log event” is not enough to tell a later validator where payload begins or how partial/multiple JSON fragments are rejected. R40 must freeze a minimal one-line envelope: one deterministic message literal (for example `collector_runtime_loaded_json=`) followed by one `json.dumps` object with sorted keys, compact separators, `allow_nan=False`, UTF-8, and no embedded CR/LF. The later parser must accept exactly one full message payload after that literal in the container-scoped stream, not a substring of arbitrary output; handler prefix is outside the payload. Serialization/logger exceptions must propagate and cannot trigger retry/success fallback.

Logging-handler buffering, lost collection, rotation, a missing line, or a truncated/malformed line do not justify persistent storage, telemetry, API, heartbeat, or retention work. They mean only that the later validator has insufficient evidence and returns HOLD. R40 lacks this parser contract and tests for it, so B3 is a blocker.

## 9. Future exact allowlist review

| Path | Necessary | Sufficient | Responsibility | Credible missing path | Scope-expansion risk |
| --- | --- | --- | --- | --- | --- |
| `collector/app/main.py` | yes | no alone | create/pass one startup context; one worker/start boundary | none; existing permitted reliability test can import/patch it | adding lifecycle/Compose work is out of scope |
| `collector/app/services/event_collector.py` | yes | no alone | post-construction emission, scope cardinality checks, no pre-I/O side effects | none | changing polling, DB, PLC, ACK/read_done is forbidden |
| `collector/app/plc/mapping.py` | yes | yes for raw-byte binding | same-byte read/hash/decode/parse exposure | none | semantic schema/caller contract expansion needs PM |
| `collector/tests/test_event_collector_reliability.py` | yes | no alone | constructor/startup-context/one-shot/no-I/O/logging and `Thread.start()`-failure simulations | none | do not convert to integration/runtime test |
| `tests/test_collector_station_event_runtime_source.py` | yes | no alone | raw-byte identity, parse/hash, duplicate mapping/scope fixture coverage | none | retain station-event authority boundaries |

The frozen three-source/two-test set is sufficient **only after** B1–B3 are repaired in R40. No additional path is currently required for a PM decision. `config.py`, registry, read-plan, Snap7 integration, packaging test, Dockerfile, Compose, mapping content, storage, production/ACK surfaces remain excluded.

## 10. Acceptance-test sufficiency review

R40's planned tests are useful but insufficient as written. The repaired two-file plan must additionally prove:

1. exact one main-context / one worker record, and no record with absent, reused, foreign-PID, manual, or probe context;
2. duplicate station ID, duplicate generated plan scope, reserved `line` collision, missing line, missing station, and unexpected scope all fail before emission;
3. raw SHA is calculated from the same bytes supplied to UTF-8 decode/YAML parse, with no second read or newline-normalized hash;
4. canonical one-line serialization, parser acceptance of one full payload only, and logger/serialization failure with no fallback;
5. record is final constructor action; then simulate `Thread.start()` failure and show later validation must reject its stale/non-active PID boundary;
6. no Snap7 connect/read/write, Storage query/write/transaction, accepted-fact generation, ACK, or read_done activity during valid or failed constructor paths;
7. existing ACK/read_done and persistence assertions remain unchanged; and
8. static/isolated evidence remains classified as static, not process-bound runtime evidence.

The two allowed tests can contain these focused tests without new test paths. No test was executed in R41.

## 11. Blockers, bounded repair, and recommendations

### Blockers requiring Architecture repair

1. **B1 — duplicate scope/cardinality false PASS.** Source: `event_collector.py` constructor dict conversion and station comprehension; `mapping.py`/`read_plan.py` allow duplicate station-derived scopes. Consequence: malformed duplicate IDs/scopes can be overwritten and still look complete. Minimum repair: amend R40 to freeze duplicate-before-dict and exact cardinality/scope rules plus tests; no source patch under this authority.
2. **B2 — process provenance, uniqueness, and field-authority conflict.** Source: R40 §8.1 classifies `process_pid` both required and diagnostic-only; §8.2/§11 do not freeze active-main PID equality or a single-use context. Consequence: manual/probe/repeated worker records, stale records after restart, and `Thread.start()` failure can be mistaken for the active main process. Minimum repair: amend R40 with the mandatory single-use context, `collector_main_started_at_utc`, correlation matrix, and exact later external PID/container/start-boundary HOLD rule.
3. **B3 — parser-boundary false PASS.** Source: R40 §8/§10; current logger formatting in `main.py`. Consequence: malformed, prefixed, partial, or substring-matched output can be accepted ambiguously. Minimum repair: amend R40 with deterministic one-line message grammar, strict parser acceptance/rejection semantics, and focused tests; no logging service or persistence subsystem.

### Non-blocking recommendations

- State explicitly that Candidate A proves successful required initialization only; it does not prove worker health, PLC connectivity, DB health, event persistence, ACK/read_done, or production acceptance.
- Keep disabled stations in the present required-plan set unless a separately authorized product behavior change decides otherwise.
- Keep optional scope-list and record-emission time diagnostic-only.

The necessary repair is a narrow Architecture documentation/contract correction to R40 followed by fresh independent review. It must not modify source, tests, Docker/Compose, config, status, roadmap, or handoff under this R41 authority.

## 12. Audit, next gate, MVP, and thread context

Final local audit records the exact changed-path allowlist as this R41 report only. No source/test/config/Docker/Compose/status/roadmap/handoff/R40 file was modified; no tests, application, Docker, network, SSH, DB/API/PLC/V-PLC, or Git mutation was performed. `git diff`, cached diff, and both whitespace checks are empty; R41 remains untracked and unstaged. Final untracked composition is `303`: Batch D aggregate `300`, Batch E `1`, R40 `1`, R41 `1`.

R41 file identity at its final write boundary:

```text
path: docs/reports/sprint4_d2_r7b_i1_r41_process_bound_runtime_loaded_observability_reliability_review.md
state: UTF-8 regular file / NON-SYMLINK / UNTRACKED / UNSTAGED
pre-final-audit written snapshot: 24389 bytes / SHA-256 4c451c6828d8e0a870a8035e049237a3aca850cad7b475fd6a2986f3f24da82b
final exact file identity: re-established after terminal report text is complete and returned in the mandatory concise Chat manifest; no second report/artifact is authorized.
```

Final disposition:

```text
R41 Reliability review WRITTEN
→ ChatGPT PM durable intake only
→ PM decides whether to issue narrowly scoped Architecture repair
```

MVP alignment: `MVP-ALIGNED WITH BACKLOG ITEMS`. The blockers retain Candidate A and only close false-PASS gaps; they do not introduce telemetry, API, persistence, a generic registry, cross-process coordination, or a Level 2 topology project.

Thread context assessment:

```text
output length: long durable review
continue current Thread: no
new Thread recommended: yes
reason: this independent review authority is terminal; any R40 repair or further review requires fresh PM authority and may not inherit it.
```
