# Sprint 4 D2-R7B-I1 R40 Process-Bound Runtime-Loaded Observability Planning

## 1. 报告身份与结论

- 任务：D2-R7B-I1 R40 — Plan the Smallest Process-Bound Runtime-Loaded Mapping Identity Evidence Gate
- 执行 Thread：Architecture / Integration
- Authority：`PM-D2-R7B-I1-R40-PROCESS-BOUND-RUNTIME-LOADED-OBSERVABILITY-PLAN-260730-0849`
- Delivery：`REPOSITORY_DURABLE_REPORT`
- Authority properties：`AUTHORIZED ONCE / LOCAL PLANNING DOCS WRITE ONLY / NO SOURCE OR TEST WRITE / NO PRE-AUTHORITY REPAIR / NO REMOTE OR RUNTIME AUTHORITY / NOT REUSABLE`

**结论：`PASS / PROCESS_BOUND_RUNTIME_LOADED_OBSERVABILITY_PLAN_READY_FOR_REVIEW`**

```text
PLANNING_PASS / SOURCE_CHANGE_REQUIRED
WRITTEN
NOT IMPLEMENTED
NOT TESTED
NOT STAGED
NOT COMMITTED
NOT PUSHED
NO FRESH REMOTE OBSERVATION
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED
```

选择的未来机制是 **Candidate A：active Collector main process 的 one-shot structured startup record**。它仅需将已成功构造的 mapping identity、resolved snapshot 与完整 read-plan set 输出到现有标准日志通道；不建立 API、DB persistence、管理 endpoint、generic registry、telemetry 或 heartbeat 子系统。

当前源码没有该 exact process-bound record，故不能以 R35 static probe 或当前日志升级 `RUNTIME-LOADED`。本报告不授权实现、测试、Docker/Compose、Collector lifecycle、remote observation、Git 或生产事实活动。

## 2. Fresh recovery、authority precedence 与输出路径前置条件

本轮只读 recovery 位于 `/Users/chenjie/Documents/MES/edge-mes-demo`：

| Field | Live result |
| --- | --- |
| root / branch | `/Users/chenjie/Documents/MES/edge-mes-demo` / `main` |
| HEAD / origin/main | `ce22ca71eff0548aa064129c160f7041603855e7` / same |
| HEAD^ | `35c50b1eb0f76d8b3361e8c122448ad03899559b` |
| ahead / behind | `0 / 0` |
| tracked dirty / cached | empty / empty |
| `git diff --check` / cached check | PASS / PASS |
| initial untracked | `301` |
| initial docs untracked | `300` |
| Batch E visible path | `frontend/next-env.d.ts` |

该 baseline 与 Prompt expected baseline 完全一致。最近一次前移是已明确授权的单文件 PM handoff commit `ce22ca7`，其 parent 为 `35c50b1`；无 source、tracked/cached state 或 authority-chain drift，故继续。`current_status.md` 和 `roadmap.md` 仅作历史快照；当前解释优先级为 live Git、`chatgpt_pm_handoff_260730-0834.md`、R35/R36 durable evidence、recent committed history、再到 status/roadmap。旧文本中的 activation pending 不会重开已关闭 gate。

初始 exact report path 检查：`ABSENT / NON-SYMLINK / UNTRACKED / UNSTAGED`（absence test=0、non-symlink test=0、`git ls-files --error-unmatch`=1、cached path set empty）。本报告是本轮唯一授权写入路径。R36 只用于确认 Batch D=300 historical manual-review 与 Batch E=1；未对 Batch D 作任何审阅、删除、移动或分类改写。

## 3. 当前 accepted gate 与 evidence boundary

```text
ACTIVATED                  = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED             = NO
PRODUCTION-ACCEPTED        = NO
```

R35 是历史 accepted、bounded read-only evidence：active Collector ID、image ID、read-only mount、source hashes、lifecycle stability，以及 isolated `docker exec` static import/mapping construction 已成功。它的 `container_static_exec` 明确记录 `runtime_worker_constructions=0`、PLC/DB/API connections=0，因此证明静态兼容性而非运行中主进程已经加载 mapping。没有 fresh remote observation 本轮发生。

静态 probe、isolated `docker exec` import、独立 Python process、或重新构造的 `EventCollectorWorker`，均可证明 source/import/config compatibility；它们不是 active Collector main process 的 evidence，不能单独作 `RUNTIME-LOADED` PASS authority。`RUNTIME-LOADED` 也不表示 PLC connected、DB healthy、event accepted、ACK/read_done、DB/API truth 或 `PRODUCTION-ACCEPTED`。

## 4. Key source identity audit

下列均为 current HEAD worktree bytes；没有 source/test/config 修改。

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `collector/app/main.py` | 2073 | `a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090` |
| `collector/app/config.py` | 764 | `4f01689a34fb494f7ea84cf74b303ce8aed0957d1dd9c05fc7773563cd577afc` |
| `collector/app/services/event_collector.py` | 16342 | `eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f` |
| `collector/app/services/resolved_config_registry.py` | 17337 | `1844449a3f99e9ca53bddc8063c151fb0f889920597bccb170f5e62f3715db2c` |
| `collector/app/plc/mapping.py` | 17433 | `c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098` |
| `collector/app/plc/read_plan.py` | 1482 | `fd5f675501444ed8378d6a296c3ed3d8769af97a1f19d1e95f3c00d76d4b02d6` |
| `collector/Dockerfile` | 218 | `e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839` |
| `docker-compose.yml` | 5698 | `c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66` |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` |
| `collector/tests/test_event_collector_reliability.py` | 12774 | `462656c9d9146e492b52296ca2b40a1f37fe40cba95a2068e4c6317fd33c2472` |
| `collector/tests/test_snap7_reliability_integration.py` | 8025 | `5cc75a9cd37eeee6f3a80e29d186b55b3aab3a335898d77e204a9d653f686b54` |
| `tests/test_collector_station_event_runtime_source.py` | 30571 | `7d9d894eaa784e36c729e824ee87de73a863765089fd12e388bc926164229fd7` |
| `tests/test_collector_container_packaging.py` | 941 | `351e80a76a53f742258e91196b109172de7b43dc3fa359e63ef44c9e7ad9c26e` |

## 5. Current Collector startup lifecycle call map

### 5.1 `app.main.main()`

`collector/app/main.py` executes in this order:

1. `load_config()` reads optional `/app/config/app.yaml`; `interval_ms` and `source_type` are selected.
2. `Snap7Source(...)` is constructed for `source_type == "snap7"`; otherwise `SimulatorSource(...)` is constructed.
3. `Storage(database_url())` is constructed for the snapshot loop.
4. `EventDetector(storage)` is constructed.
5. If `event_collector_enabled()` (default true), `EventCollectorWorker(dsn, host, port)` is fully constructed, then a daemon thread named `event-collector` is created and started with target `event_worker.run_forever`.
6. Only after that does `main` log `collector started source_type=... interval_ms=...` and enter its infinite snapshot loop.
7. The snapshot loop performs `source.read()`, `storage.ensure_machine`, `storage.insert_snapshot`, and `detector.process`; these are distinct from the event-worker loop.

Thus the event worker runs in a thread of the active Collector Python main process. A future record emitted synchronously during the successful constructor is before `Thread.start()`, `run_forever()`, the first event-worker PLC connect/read, and all event-worker DB writes.

### 5.2 `EventCollectorWorker.__init__()`

Current constructor order in `collector/app/services/event_collector.py` is:

1. `self.storage = Storage(dsn)` (a wrapper construction; it is not an observed DB query/write here).
2. retain host/port; `load_edge_mapping(mapping_path)` reads/parses the mapping.
3. select PLC entry/fallback and materialize `plc_id`, `line_id`, rack and slot.
4. construct `ZoneInfo(self.mapping.timezone)`.
5. `build_resolved_config_snapshot_from_mapping(self.mapping.runtime_snapshot)` validates the runtime mapping hash and constructs the resolved snapshot; build failure raises.
6. construct `InMemoryResolvedConfigRegistry` with that one validated snapshot.
7. construct `snap7.client.Client()`; this does not call `connect`.
8. construct `plans = {plan.scope: plan for plan in build_read_plans(self.mapping)}`; set `line_plan`; build station runtimes only for stations whose ID is present in `plans`.

Important current gap: `build_read_plans` rejects an empty/multi-DB scope, but the constructor's station comprehension silently omits a station absent from `plans`. Therefore current code does not prove a complete required station-read-plan set and has no startup success emission. Future implementation must fail closed before emission when the line plan is absent or the exact station-ID set of plans differs from `self.mapping.stations`.

### 5.3 First runtime interaction and current logs

`run_forever()` first logs `event collector started host=... port=... stations=...`, then calls `poll_once()`. `poll_once()` first invokes `_ensure_connected()`; that calls `client.connect(...)` only when disconnected. Next it reads the line plan (`_read_plc_boot_id`), then station reads/decodes. DB runtime-status writes and any accepted-fact/cycle persistence occur later in `_process_station`; ACK writes occur only after accepted persistence and only when `read_done` is false.

Current startup logs can prove that the worker thread entered `run_forever` and disclose host/port/station IDs. They cannot prove mapping file identity, mapping hash, resolved snapshot hash, read-plan completeness, process start boundary, or association with a later fresh container observation. The main `collector started` log is likewise not mapping evidence.

## 6. Strict minimum definition of `RUNTIME-LOADED`

`RUNTIME-LOADED` is a later, bounded, **process-bound** claim only if one observed success record satisfies all of the following:

1. It was emitted once by the active Collector main process during its own `main()` startup path, not by a probe, exec process, test, or separately constructed worker.
2. The same worker has successfully loaded the exact mapping bytes/path, validated its mapping content identity, built a hash-consistent resolved snapshot, and materialized a complete line-plus-station read-plan set.
3. Emission is before `Thread.start`, `run_forever`, `_ensure_connected`, PLC read/write, DB query/write, accepted-fact activity, ACK/read_done activity, or production data generation.
4. The record can be correlated later to one freshly observed active container/image and fresh process-start boundary using the record's PID/time fields plus the exact container log stream. Hostname is never assumed to be a container ID.
5. Any mapping parse/hash failure, resolved-snapshot mismatch, missing/invalid read plan, constructor exception, or failed complete-set check produces **no success record**.

This definition expressly excludes claims about connection health or production truth. A container running without this record remains `ACTIVATED` at most; it is not `RUNTIME-LOADED`.

## 7. Candidate comparison and decision

| Candidate | Scope / confidence | Decision |
| --- | --- | --- |
| A. one-shot structured process-startup record | One log line from the active main-process constructor after all required construction, before worker loop/I-O. Existing logging channel; no persistent surface. Exact later correlation is supplied by fresh container-ID-scoped log collection plus PID/time checks. | **Selected** |
| B. read-only in-process status surface | Needs an API/endpoint or exposed registry, lifecycle ownership, readiness semantics, concurrency/thread-safety, operational discovery and possibly persistence/retention. `InMemoryResolvedConfigRegistry` is config lookup infrastructure, not a process-status contract. | Rejected; backlog/separate Level 2 project only if a future product requirement demands it. |
| C. external static/exec probe | Can prove source/image/mount/import/config compatibility, as R35 did. It is a second process and cannot prove the running worker's constructor succeeded. | Rejected as standalone PASS authority; retain only as complementary static evidence where separately authorized. |

Candidate A is the smallest credible solution. No current source provides an equally trustworthy record. If implementation review finds that A requires an API, DB persistence, generic registry, cross-process coordination, or complex topology, stop with `HOLD / SCOPE_RESET_REQUIRED`; do not substitute Candidate B by convenience.

## 8. Frozen minimum evidence-record contract

### 8.1 One success record

Emit exactly one structured log event with a stable JSON object and event type `collector_runtime_loaded` only at the emission point in §8.3. Required authority fields:

| Field | Authority purpose |
| --- | --- |
| `evidence_schema_version` = `edge-mes/collector-runtime-loaded/v1` | Parser/contract identity, distinct from mapping schema. |
| `event_type` = `collector_runtime_loaded` | Stable, unique success-event discriminator. |
| `process_started_at_utc` | RFC3339 UTC timestamp captured at the entry boundary of active `app.main.main()` and passed to its worker. |
| `process_pid` | `os.getpid()` from that same process; diagnostic correlation, not a container ID. |
| `mapping_path` | Exact loaded path, expected `/app/config/mapping.yaml` under current image/mount contract. |
| `mapping_content_sha256` | SHA-256 of the exact bytes parsed by `load_edge_mapping`, not a second path reread. |
| `mapping_schema_version` | Loaded mapping `schema_version`. |
| `config_version` | Loaded mapping `config_version`. |
| `line_id` | Loaded mapping/PLC line identity. |
| `read_plan_count` | Count after complete-set validation; current expected count is four (line plus WS01/WS02/WS03). |
| `resolved_config_hash` | Hash-consistent resolved snapshot identity. |

Diagnostic-only fields, if they remain one-line/non-sensitive and do not alter PASS authority: `process_pid`, a record emission timestamp, and a sorted read-plan-scope list. The scope list is useful to diagnose mismatches, but `read_plan_count` plus exact expected fields is the authority minimum. No DSN, credentials, raw PLC bytes, raw/accepted payload, unit/DMC, event data, DB result, endpoint, host/port, ACK/read_done data, or production fact may be logged.

The mapping runtime semantic hash and current resolved config hash are intentionally the same value: `build_resolved_config_snapshot_from_mapping` requires `candidate.compute_content_hash() == mapping_snapshot.config_hash`, and sets `snapshot.config_hash` from `mapping_snapshot.config_hash`. The record therefore emits only `resolved_config_hash`; it must not fabricate a second independent `mapping_runtime_config_hash`. By contrast `mapping_content_sha256` is the exact YAML-byte identity and is a distinct raw-file authority.

The mapping's decoder-registry snapshot ID/content hash was evaluated. It is directly validated while parsing and is included in the semantic resolved/config hash; it is **not** emitted as an independent authority field because that would duplicate the same current config authority. It may only become a diagnostic field under a future explicit review if the review shows a direct false-PASS prevention need.

### 8.2 Correlation without hostname assumption

The record must not contain or trust hostname as a container ID. It also must not guess Docker metadata from application code. Future bounded validation correlates the record externally: fresh full active container ID, image ID and `State.StartedAt`; exact `docker logs` (or equally bounded container-ID-scoped log observation) for that full container; record emitted after the observed container start boundary; PID/time consistency with fresh process observation if separately authorized. The container ID is the validation envelope, while PID/time identify the application process inside it. A log from a different container, an earlier start boundary, a missing/ambiguous record, duplicate matching records, or unverifiable PID/start correlation is a fail-closed HOLD.

### 8.3 Exact emission point and failure absence

Future code must capture the main-process start timestamp at the first executable boundary of `app.main.main()` and pass it only to the worker created by that startup path. In `EventCollectorWorker.__init__`, emission occurs only after all of these succeed: exact-byte mapping load/hash capture; PLC/line/timezone derivation; resolved snapshot construction and hash-consistency check; in-memory registry construction; Snap7 client construction; `build_read_plans`; non-null line plan; and exact one-to-one coverage of every configured station by its plan. It must occur before return from the constructor, hence before `Thread.start()` and every loop/I-O interaction.

There is no success fallback, retry, poll-loop emission, delayed replay, persistent record, or catch-and-log-success path. Exceptions propagate under existing startup behavior; the absence of a matching success record is failure/non-establishment, never success.

## 9. Frozen future implementation and test allowlists

### 9.1 Source allowlist (exactly 3 paths)

| Path | Why necessary |
| --- | --- |
| `collector/app/main.py` | Capture the active main-process startup boundary once and pass only that bounded context to its worker. |
| `collector/app/services/event_collector.py` | Complete read-plan coverage validation and exact one-shot structured success emission after all construction succeeds. |
| `collector/app/plc/mapping.py` | Bind raw mapping SHA-256 to the same bytes that are parsed, exposing that identity without a second/racy file read. |

### 9.2 Test allowlist (exactly 2 paths)

| Path | Why necessary |
| --- | --- |
| `collector/tests/test_event_collector_reliability.py` | Constructor-level success-once/no-I-O/no-record-on-failure tests with fake storage/client and captured logger. |
| `tests/test_collector_station_event_runtime_source.py` | Mapping raw-byte identity and existing mapping/resolved-hash fail-closed contract coverage. |

`storage.py`, DB schema, API, Dashboard, V-PLC, mapping content, Dockerfile, Compose, `config.py`, `resolved_config_registry.py`, Snap7 integration test, packaging test, production contracts and ACK/read_done code are explicitly excluded. If review proves any additional path unavoidable, it is a separate PM decision and not an implied allowlist expansion.

Planned focused commands for a future authorized implementation gate only; **not executed in R40**:

```bash
PYTHONPATH=collector:. pytest -q collector/tests/test_event_collector_reliability.py
PYTHONPATH=collector:. pytest -q tests/test_collector_station_event_runtime_source.py
```

## 10. Future implementation acceptance tests

The future two-path test plan must establish all of the following without starting the application loop, connecting PLC, querying/writing DB, generating production data, or altering existing ACK/read_done ownership:

1. Valid initialization emits exactly one `collector_runtime_loaded` record with exactly the allowlisted authority fields, no secret/raw/production payload and no duplicate emission from poll/retry paths.
2. The captured record is after mapping raw-byte hash, mapping parse/validation, resolved snapshot construction/content match, and full line/station read-plan materialization.
3. Mapping load failure emits no success record.
4. Tampered/resolved-config hash mismatch emits no success record.
5. Missing/invalid line or station read plan emits no success record; specifically cover the current silent station-plan omission risk.
6. Worker/process construction used for the evidence path does not call Snap7 `connect`, `db_read`, `db_write`, Storage query/write/transaction, accepted-fact build, or production event generation.
7. The record has the exact mapping path/raw SHA, mapping schema/config/line, plan count, resolved hash and process fields; the mapping runtime hash/resolved hash equality is asserted rather than represented as two independent identities.
8. Existing event collector persistence, transaction, accepted-fact and ACK/read_done tests retain their current behavior.
9. A record from a manually constructed worker or isolated static-probe-like path cannot satisfy the active-main-process startup-context contract; later container-ID-scoped runtime validation remains required.

## 11. Later bounded runtime-loaded validation contract (not executed)

A separate read-only runtime-validation Prompt must require fresh evidence for: full active container ID; full image ID; container `StartedAt`; fresh active process boundary; the exact one-shot record; record-to-container-ID-scoped log correlation; PID/time consistency; expected raw mapping SHA and semantic/resolved fields; exact success-record uniqueness; and protected-service stability.

It must classify mapping/load failure, absent record, duplicate record, mismatched mapping/image/start time, unproven container/process association, or unproven read-plan completeness as `HOLD / NOT RUNTIME-LOADED`. It must make no DB/API/PLC mutation, no production-data generation, no lifecycle mutation, no rollback, and no automatic rollback. Rollback needs a later explicit lifecycle authority. `PRODUCTION-ACCEPTED` remains a separate planning/execution/acceptance path.

## 12. Gate separation, scope assessment and next gate

Required sequence remains:

```text
R40 Architecture / Integration planning
→ PM durable intake
→ independent Reliability planning review
→ independent Data Quality planning review
→ independent Verification planning review
→ PM implementation authorization
→ Architecture / Integration implementation
→ focused Reliability / Data Quality / Verification implementation reviews
→ exact Git closeout under separate authority
→ separate deployment/lifecycle planning if deployment is required
→ separate bounded read-only runtime-loaded validation
→ PM acceptance of RUNTIME-LOADED
→ separate production accepted-fact planning
```

No arrow inherits implementation, test, Git, deploy/restart, runtime-observation, rollback, or production authority. The design is `MVP-ALIGNED WITH BACKLOG ITEMS`: Candidate B/status endpoint is a backlog-only separate Level 2 project, not current work. There is no task inflation into telemetry, audit, forensics, generic registry, API, persistence or product monitoring.

### Final audit at report write boundary

- authorized changed path: this report only;
- prohibited source/test/config/Docker/Compose/status/roadmap/handoff paths: unchanged by R40;
- network / SSH / remote filesystem / Docker / Compose / DB / API / PLC / V-PLC: `0`;
- application/runtime execution and test execution: `0`;
- Git add/stage/commit/push/tag/reset/restore/clean/stash: `0`.

Before terminal return, report regular-file/non-symlink/UTF-8/trailing-whitespace identity, final Git/index checks and final untracked delta must be rechecked. Expected final untracked is initial `301` plus this one report = `302`; no Batch D/E handling is implied.

**Blockers：none。**

**Recommendation：** ChatGPT PM durable intake only; it may decide whether to issue the next independent planning review. No implementation recommendation is an authorization.

**Only next gate：**

```text
R40 Architecture / Integration planning report WRITTEN
→ ChatGPT PM durable intake only
```

### Thread context assessment

- output length：long durable planning contract; Chat must remain concise.
- continue current Thread：no.
- new Thread recommended：yes.
- reason：R40 is terminalized local Level 2 planning. Reliability/Data Quality/Verification review, implementation and runtime validation require independently scoped authority and must not inherit this Thread context.
