# Sprint 4 D2-R7B-I1 R42 Process-Bound Runtime-Loaded Observability Architecture Contract Repair

## 1. 报告身份、结论与交付分类

报告名称：`Sprint 4 D2-R7B-I1 R42 Process-Bound Runtime-Loaded Observability Architecture Contract Repair`

任务名称：`D2-R7B-I1 R42 — Produce a Consolidated Architecture Contract that Repairs R41 Reliability Blockers B1–B3`

执行 Thread：`Architecture / Integration`

Authority source / ID：`PM-D2-R7B-I1-R42-PROCESS-BOUND-RUNTIME-LOADED-ARCHITECTURE-REPAIR-260730-0923`

Delivery：`REPOSITORY_DURABLE_REPORT`

唯一报告路径：

```text
docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md
```

Authority properties：

```text
AUTHORIZED ONCE
CONSOLIDATED ARCHITECTURE CONTRACT REPAIR
LOCAL DOCS WRITE ONLY
NO SOURCE OR TEST WRITE
NO PRE-AUTHORITY REPAIR
NO REMOTE OR RUNTIME AUTHORITY
NOT REUSABLE
```

结论：

```text
PASS / CONSOLIDATED_ARCHITECTURE_REPAIR_READY_FOR_RELIABILITY_REREVIEW
```

本结论只表示 R42 consolidated Architecture contract 已按 B1–B3 完成文档级修复，准备交给新的独立 Reliability re-review。它不表示 R42 已被 PM 接受为 final contract，也不授予 implementation、test、Git、remote、Docker、lifecycle、runtime-loaded 或 production authority。

证据边界：

```text
REPAIRED CONTRACT WRITTEN
NOT YET RELIABILITY-ACCEPTED
NOT FINAL PM-ACCEPTED
NOT IMPLEMENTED
NOT TESTED
NOT STAGED
NOT COMMITTED
NOT PUSHED
NO FRESH REMOTE OBSERVATION
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED
```

## 2. Authority precedence、输入与 supersession

本报告按以下优先级解释事实：

1. live Git recovery；
2. current PM Prompt / 本 authority；
3. `docs/thread_handoff/chatgpt_pm_handoff_260730-0834.md`；
4. R35/R36 committed durable evidence；
5. PM-verified R40/R41 exact inputs；
6. recent committed Git history；
7. `docs/current_status.md` / `docs/roadmap.md` 的旧 sections。

旧 status/roadmap 中的 activation-pending 或历史 next-gate 文字不重开已经关闭的 activation gate。R35 的 `ACTIVATED` 与 `STATIC_MAPPING_INITIALIZED` 仍不等于 process-bound `RUNTIME-LOADED`。

R40 与 R41 的关系保持如下：

```text
R40 remains preserved historical planning evidence.
R41 remains preserved Reliability review evidence.
R42 supersedes R40 as the candidate implementation contract only if:
- R42 is accepted by PM; and
- a fresh independent Reliability re-review passes.
```

本报告写入本身不得宣称 R42 已 supersede、accepted 或 authorized for implementation。R40/R41 原文件均保留，未被覆盖或修改。

保留 Candidate A：

```text
one-shot deterministic startup record
emitted by the active Collector main-process startup path
after complete mapping/resolved/read-plan initialization
before Thread.start and worker PLC/DB/ACK activity
existing logging channel only
```

不得改用 API、DB persistence、status endpoint、heartbeat、generic registry、telemetry、audit 或 forensics 方案。`InMemoryResolvedConfigRegistry` 仍只是既有 resolved-config lookup infrastructure，不被提升为 runtime-status authority。

## 3. Fresh live recovery 与输入身份

项目绝对路径：`/Users/chenjie/Documents/MES/edge-mes-demo`

本轮 task-owned write 前完成的 live recovery：

| Field | Live fact |
| --- | --- |
| repository root | `/Users/chenjie/Documents/MES/edge-mes-demo` |
| branch | `main` |
| HEAD | `ce22ca71eff0548aa064129c160f7041603855e7` |
| origin/main | `ce22ca71eff0548aa064129c160f7041603855e7` |
| HEAD^ | `35c50b1eb0f76d8b3361e8c122448ad03899559b` |
| ahead / behind | `0 / 0` |
| tracked dirty | empty |
| cached | empty |
| `git diff --check` | PASS |
| `git diff --cached --check` | PASS |
| initial untracked files | `303` |
| initial untracked composition | Batch D 300 + Batch E 1 + R40 1 + R41 1 |
| R42 output before write | ABSENT / NON-SYMLINK / UNSTAGED / UNTRACKED |

本轮没有修复或重分类 Batch D/E，没有使用 `git add`、`git commit`、`git push`、`git clean`、`restore`、`reset`、`stash` 或 broad staging。R42 是初始 303 项之外唯一新增路径，预期最终 untracked count 为 304。

R40 输入重新核验：

| Path | Bytes | SHA-256 | State |
| --- | ---: | --- | --- |
| `docs/reports/sprint4_d2_r7b_i1_r40_process_bound_runtime_loaded_observability_plan.md` | 23337 | `280cb553f5fc8bf81c92e689493782749534293de4876a05d88063080caabb91` | WRITTEN / PM-REVIEWED / PM-VERIFIED / UNTRACKED / UNSTAGED / NOT COMMITTED / NOT ACCEPTED AS FINAL IMPLEMENTATION CONTRACT |

R41 输入重新核验：

| Path | Bytes | SHA-256 | State |
| --- | ---: | --- | --- |
| `docs/reports/sprint4_d2_r7b_i1_r41_process_bound_runtime_loaded_observability_reliability_review.md` | 25111 | `6dc2c7a11ea2e6c4723bda69ed270b2e9a6cb7e3f4f75d13673599640adb5bb1` | REVIEWED / WRITTEN / PM-REVIEWED / PM-VERIFIED / HOLD ACCEPTED / UNTRACKED / UNSTAGED / NOT COMMITTED |

R40/R41 均为 PM-verified uncommitted inputs，不被表示为 committed authority、implementation authority 或 Git authority。两者均为 regular UTF-8 non-symlink 文件，cached path set 为空。

## 4. Current accepted product boundary 与历史证据

当前 PM-accepted 产品状态：

```text
ACTIVATED                  = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED             = NO
PRODUCTION-ACCEPTED        = NO
```

R35 是历史的 bounded read-only post-activation evidence。它证明 active image/source/import/static mapping/lifecycle relation，但明确保留：

```text
RUNTIME-LOADED        = NO
PRODUCTION-ACCEPTED   = NO
```

R35 的 isolated container/static probe、独立 Python process、manual worker construction 或 static mapping check，均不能代表 current active Collector main process 已经完成本合同所需的 process-bound initialization。

R36 只提供历史 working-tree hygiene 与 authority materialization evidence：Batch D historical manual review 300 项、Batch E `frontend/next-env.d.ts` 1 项；本轮不读取、评审、删除、移动或重新分类 Batch D/E。

## 5. Current source identity table

以下是本轮按 Prompt exact read order 读取并以 live bytes/hash 核验的 source/config/runtime surface。所有列出的现有 source/test/config/Docker/Compose 路径相对 HEAD clean；本轮不修改它们。

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

当前 source review 的关键事实：`app.main.main()` 先执行 config/source/storage/detector construction，再构造 `EventCollectorWorker`、创建 daemon `Thread` 并启动；worker constructor 当前在 `build_read_plans()` 后直接执行 dict-by-scope conversion，且当前没有 success record。`mapping.py` 当前 `load_edge_mapping()` 使用 `Path(path).read_text()`，尚未把 raw file bytes/hash 与同一次 parse 绑定。

## 6. Consolidated process-bound claim

R42 v1 的唯一 runtime-loaded claim 是：当前 active Collector Python process 的 main startup path 已经成功完成 required mapping/resolved/read-plan initialization，并在 worker thread 启动前发出一条可由后续独立 runtime validation 交叉验证的 deterministic application record。

该 record 只声称：

```text
proves required mapping/resolved/read-plan initialization
does not prove Thread.start success
does not prove worker health
does not prove PLC connection
does not prove DB health
does not prove event persistence
does not prove ACK/read_done
does not prove production acceptance
```

它不是 process heartbeat、worker-health、PLC health、DB health、accepted-fact、ACK/read_done 或 production-truth record。

## 7. Candidate A 的 startup lifecycle 与 exact emission point

### 7.1 Mandatory startup context

Future implementation 必须在 `app.main.main()` 的第一个可执行 startup boundary 创建一个 mandatory startup context。该 context：

- 无默认值；
- 不允许 optional/default 参数让 manual/probe caller 静默获得 success-record capability；
- 至少携带 `collector_main_started_at_utc` 与 `process_pid`；
- `process_pid` 必须在 constructor/emission 时等于当前 `os.getpid()`；
- context 必须具有 single-use consumption 语义；
- 缺失、重复消费、reused 或 PID 不一致时 fail closed；
- 只由本次 `main()` startup path 传给 exactly one `EventCollectorWorker`；
- 不声称能够抵抗任意同进程代码伪造；最终 provenance 仍由后续 fresh external facts 建立。

Context 本身不是跨进程 registry、不是 cryptographic token、不是 container identity。它的最小职责是阻止 alternate caller/default path 意外获得合法 success-record capability，并让后续 validator 能够比对 main-process PID/time assertion。

### 7.2 Exact emission order

`EventCollectorWorker.__init__()` 的 success emission 必须是最后一个 required constructor action，并且只在以下全部成功后发生：

1. same-byte mapping read/hash/decode/parse；
2. mapping contract validation；
3. PLC/line/rack/slot/timezone derivation；
4. resolved snapshot construction；
5. resolved hash consistency validation；
6. in-memory registry construction；
7. Snap7 client object construction；
8. complete read-plan list construction；
9. B1 规定的 duplicate/cardinality/scope validation；
10. line plan materialization；
11. every configured station runtime 的一一 materialization；
12. startup-context PID 与 single-use validation；
13. deterministic JSON serialization。

已有 `Storage(dsn)` wrapper construction 可保留其既有位置，但本合同不把它扩大解释为已完成 DB query/write。success record 必须在以下事件之前发出：

```text
EventCollectorWorker.__init__ return
Thread.start
run_forever
PLC connect/read/write
DB query/write/transaction
accepted-fact generation
ACK/read_done activity
```

emission 之后不得存在任何会使 worker constructor 失败的 required action。任何 mapping/read/decode/parse/resolved-hash/plan/context/serialization/logger failure 都必须在 success record 之前失败，或在 serialization/logger invocation 处传播异常；不得 catch-and-success、fallback、retry、poll-loop emission、delayed replay 或 persistent replay。

### 7.3 Exactly-one scope

R42 冻结的 exactly-one scope 是：

```text
exactly one valid success record
per invocation of app.main.main()
for the current active Collector Python process
```

因此：

- 不是每个 worker object；
- 不是每次 poll/retry；
- 不是每个 log stream；
- container restart 是新的 start boundary；
- 同一 active container/start boundary 中 0 条、2 条或更多 matching records 都是 HOLD；
- duplicate worker construction 或 reused context 不得产生第二条 valid record；
- repeated `main()` invocation 必须形成不同 main-entry boundary；later validator 不得为同一 active boundary 接受多条 matching records。

## 8. B1 repair：duplicate/cardinality/scope contract

在任何 dict-by-scope conversion 和 success emission 之前，必须保留 list 形态并建立以下 exact values，顺序与现有配置一致：

```python
configured_station_ids = [
    station.station_id for station in mapping.stations
]
expected_scopes = ["line"] + configured_station_ids
generated_scopes = [
    plan.scope for plan in build_read_plans(mapping)
]
```

`generated_scopes` 必须在转换为 dict 之前取得。未来 constructor pre-emission check 必须 fail closed 拒绝全部以下条件：

- line fields 未产生 `line` plan；
- 任一 configured station ID 等于保留 scope `line`；
- duplicate configured station IDs；
- duplicate generated plan scopes；
- `len(generated_scopes) != len(expected_scopes)`；
- 任一 expected scope 缺失；
- 任一 generated scope 不在 expected scopes 中；
- generated scope set/multiset 与 expected scope set/multiset 不完全一致；
- station runtime 不能与每个 configured station 一一对应；
- materialized station runtime 数量不是 configured station 数量；
- conversion 后 dict 长度不是 expected scope count。

检查顺序必须保证 duplicate station IDs 与 duplicate generated scopes 在 dict overwrite 前仍可见。只有全部检查通过后，才允许建立 `plans = {plan.scope: plan ...}`、建立 line plan 和按现有 configured order materialize station runtimes；station runtime 必须每项恰好对应一个 configured station，不得静默省略。

当前 disabled-station behavior 不变：`build_read_plans()` 当前为 mapping 中所有 stations 建 plan，R42 继续把所有 current configured stations 视为 required。改变 disabled-station runtime semantics 是独立 product decision，不属于 R42。

所有上述失败都必须发生在 success record emission 之前，不能产生 valid success record。

## 9. B2 repair：provenance、uniqueness、timestamp 与字段分类

### 9.1 Active-main provenance split

startup context、PID 与 timestamp 是 application assertions，不是独立 external authority。后续 validator 必须从 fresh external facts 建立 terminal provenance：

```text
full active container ID
full active image ID
fresh container StartedAt
active Collector main PID/process identity
current container-ID-scoped log envelope
bounded observation timestamp
```

validator 必须要求 record PID 等于 fresh active Collector main PID，且 record 属于 current full-container-ID log envelope 与 current `StartedAt` boundary。以下均不得 PASS：

- stale prior-start record；
- other-container record；
- manual process record；
- `docker exec` probe record；
- foreign PID record；
- active process 不存在或身份不明确；
- `Thread.start()` 失败后遗留的 record 单独作为 PASS；
- worker thread health、PLC connection 或 DB health被误读为 record claim。

后续 validator 只能在 current active container-ID-scoped logs 中寻找唯一 matching record；缺失、重复、ambiguous、malformed 或无法建立 process identity 时为 HOLD。不得通过增加 storage、telemetry、endpoint 或 heartbeat 来弥补。

### 9.2 Timestamp semantics

字段从 `process_started_at_utc` 改为：

```text
collector_main_started_at_utc
```

精确定义：它是 Python `app.main.main()` entry timestamp，不是 OS process birth time；使用 RFC3339 UTC，并且输出必须使用 `Z`。malformed、non-UTC、impossible ordering 或无法建立时钟关系时不能建立 PASS。

后续 validator 的最小时间关系：

```text
fresh container StartedAt
<= collector_main_started_at_utc
<= bounded observation time
```

不得发明毫秒级 tolerance，也不得扩展为 clock synchronization project。若 clock 状态不能建立上述关系，结果为 HOLD。

### 9.3 Application record field authority matrix

Terminal application-claim fields：

```text
evidence_schema_version
event_type
mapping_path
mapping_content_sha256
mapping_schema_version
config_version
line_id
read_plan_count
resolved_config_hash
```

Correlation application-claim fields：

```text
collector_main_started_at_utc
process_pid
```

External correlation authority 仅由后续 independent runtime-validation authority 提供：

```text
full active container ID
full active image ID
fresh container StartedAt
active Collector main PID/process identity
current container-ID-scoped log envelope
bounded observation timestamp
```

R42 v1 success record 不加入 optional diagnostic fields。`record_emitted_at` 和 sorted scope list 是 backlog-only diagnostics，不属于 v1 fields，不得用于 PASS/HOLD。上述 application v1 JSON object 必须具有 exact key set，不允许额外字段。

## 10. B3 repair：deterministic logging grammar 与 strict parser boundary

唯一 application-message grammar：

```text
collector_runtime_loaded_json=<JSON_OBJECT>
```

JSON serialization 必须：

- 使用 R42 exact key set；
- `sort_keys=True`；
- compact separators；
- `allow_nan=False`；
- UTF-8；
- 单行；
- 不包含 CR 或 LF；
- 不包含 DSN、credential、host/port、raw PLC bytes、production payload、unit/DMC、event data、DB result、ACK/read_done data 或 production fact。

Python logging formatter 的时间和 level prefix 属于 transport/logging prefix，不属于 JSON payload。后续 parser 只接受 application-message 部分以 exact literal `collector_runtime_loaded_json=` 开头的完整一行；不得在任意日志文本中 substring-match。literal 之后的全部剩余内容是唯一 JSON payload。

Parser 必须拒绝：

- extra suffix；
- multiple delimiter；
- partial/truncated JSON；
- non-object JSON；
- missing key；
- extra key；
- wrong schema；
- wrong event type；
- malformed、ambiguous、missing 或 duplicate matching records；
- 0 条或 2 条以上 matching records。

serialization 或 logger invocation 异常必须传播；不得 fallback、retry 或 emit substitute success record。handler buffering、log loss、rotation 或 collection failure 不触发新的 storage/telemetry 工作，只表示 evidence unavailable 并 HOLD。

## 11. Exact v1 record shape

固定 exact key set：

```text
{
  "collector_main_started_at_utc": "<RFC3339 UTC with Z>",
  "config_version": "<mapping config_version>",
  "evidence_schema_version": "edge-mes/collector-runtime-loaded/v1",
  "event_type": "collector_runtime_loaded",
  "line_id": "<loaded line_id>",
  "mapping_content_sha256": "<sha256 of exact mapping bytes>",
  "mapping_path": "/app/config/mapping.yaml",
  "mapping_schema_version": "<loaded schema_version>",
  "process_pid": <os.getpid integer>,
  "read_plan_count": <validated complete count>,
  "resolved_config_hash": "<validated semantic/resolved hash>"
}
```

上面的 object 仅为字段/值合同示意；最终 serialized object 采用 `sort_keys=True`，所以 parser 只接受 exact keys，不依赖示意顺序。v1 不加入 `record_emitted_at`、scope list 或任何 optional key。`mapping_content_sha256` 是 raw file-byte identity；`resolved_config_hash` 是 validated semantic/resolved identity。不得新增虚假的第二个 semantic mapping hash。

## 12. Same-byte raw mapping identity

Future `load_edge_mapping` contract 必须对 exact path：

1. 只读取一次 raw bytes；
2. 对同一 raw bytes 计算 SHA-256；
3. 对同一 raw bytes 执行显式 UTF-8 decode；
4. 将该 decoded content 交给 YAML parse；
5. 将 raw identity 与 parsed `EdgeMapping` 绑定并供 record 使用。

不得 second read、先 text read 再 re-encode 计算 hash、newline normalization 后计算 hash、或把另一路 substituted path 当作 parsed authority。read/decode/parse/semantic/resolved-hash failure 时不得产生 success record。

`mapping_content_sha256` 是 exact file-byte identity；`resolved_config_hash` 是 validated semantic/resolved identity。两者互补，但不是两个独立 semantic authorities；不得新增第二个 mapping semantic hash。

`collector/app/plc/mapping.py` 的 future change 必须保持现有 direct `parse_edge_mapping()` callers 可用，不借机改变 mapping semantic contract、配置内容、disabled-station behavior 或 existing caller compatibility。

## 13. Future exact implementation allowlist

Future implementation 只允许以下 exact three source paths：

| Path | Frozen responsibility |
| --- | --- |
| `collector/app/main.py` | capture main-entry boundary；create one mandatory startup context；pass it to exactly one event worker；不增加 runtime endpoint 或 lifecycle feature |
| `collector/app/services/event_collector.py` | define/consume minimal startup context；enforce PID/single-use；validate duplicate/cardinality/scopes；build exact record；emit exactly once as final required constructor action；不改变 polling、PLC、DB、accepted-fact 或 ACK/read_done |
| `collector/app/plc/mapping.py` | same-byte read/hash/decode/parse binding；expose raw identity；preserve semantic behavior 与 existing caller compatibility |

如果 Architecture analysis 认为额外 source path 不可避免，必须 HOLD 并返回 PM；不得自动扩展 allowlist。明确排除：`config.py`、`resolved_config_registry.py`、`read_plan.py`、`collector/Dockerfile`、`docker-compose.yml`、`config/mapping.yaml`、`storage.py`、API、DB schema、Dashboard、V-PLC、Snap7 runtime integration、production、ACK/read_done surface。

## 14. Future exact test allowlist 与 focused commands

Future test 只允许以下 exact two paths：

| Path | Frozen responsibility |
| --- | --- |
| `collector/tests/test_event_collector_reliability.py` | constructor-level context/one-shot/no-I-O/logging/emission-order tests，以及现有 persistence/ACK/read_done semantics 不回归的 focused coverage |
| `tests/test_collector_station_event_runtime_source.py` | same-byte raw mapping identity、decode/parse/hash failure、duplicate mapping/scope fixture 与 isolated/manual evidence boundary coverage |

未来 implementation authority 才可使用以下 commands；本轮未执行：

```bash
PYTHONPATH=collector:. pytest -q collector/tests/test_event_collector_reliability.py
PYTHONPATH=collector:. pytest -q tests/test_collector_station_event_runtime_source.py
```

`collector/tests/test_snap7_reliability_integration.py`、`tests/test_collector_container_packaging.py` 和其他现有测试本轮仅作指定输入审查，未来 R42 implementation diff 不得修改它们；现有 persistence、PLC、ACK/read_done 与 packaging semantics 必须保持，不由本合同扩大 test allowlist。

## 15. Future focused test matrix

两条 allowed test paths 至少必须覆盖：

### Startup context、provenance 与 uniqueness

- valid main context emits exactly one record；
- absent context emits no valid record；
- reused context fails closed；
- foreign PID context fails closed；
- duplicate worker with same context 不能产生第二条 record；
- manual/probe/isolated worker path 不能单独满足 active-main contract；
- `process_pid != os.getpid()` fails closed；
- exactly-one scope 按 `main()` invocation/current active process boundary 验证；
- repeated `main()` 形成不同 boundary，same boundary 不接受第二条；
- `Thread.start()` failure 后的 record 不能单独成为 later runtime PASS。

### B1 duplicate/cardinality/scope

- duplicate station ID 在 dict conversion/emission 前失败；
- station ID `line` collision 失败；
- duplicate generated scope 失败；
- missing line scope 失败；
- missing station scope 失败；
- unexpected extra scope 失败；
- count mismatch 失败；
- station runtime 一一对应失败时无 record；
- disabled configured station 仍属于 required scope set。

### Raw mapping、record grammar 与 failure propagation

- same-byte SHA 使用一次 read 且 hash bytes 等于被 decode/parse 的 bytes；
- invalid UTF-8 fails closed；
- YAML parse/semantic/resolved-hash failure emits no record；
- canonical exact-key one-line JSON；
- `sort_keys=True`、compact separators、`allow_nan=False`、UTF-8；
- no CR/LF；
- strict parser 只接受 one full application-message payload；
- substring/prefix/suffix/multiple-delimiter/partial/non-object/extra-key 均拒绝；
- logger/serialization exception propagates；
- no fallback、retry、delayed replay 或 substitute success；
- no secret/raw/production payload。

### Constructor side-effect boundary 与 compatibility

- success emission is final required constructor action；
- valid/failed constructor path 不连接 PLC；
- 不 query/write DB、transaction、accepted fact、ACK/read_done；
- constructor path 不生成 production event；
- existing persistence 和 ACK/read_done tests 保持原语义；
- `parse_edge_mapping()` existing callers 保持可用；
- isolated/static/manual record 不能单独满足 later runtime validation。

不得新增 test path。不得以 test fixture、manual probe 或 synthetic log 把 local/static evidence 提升为 runtime-loaded 或 production evidence。

## 16. Later independent runtime-loaded validation contract

实现与 fresh independent Reliability/Data Quality/Verification planning gates通过并经 PM final planning-contract acceptance 后，才可另行授权 bounded runtime-loaded validation。该 validation 至少必须：

1. fresh observe full active container ID，而非 hostname、short ID 或 tag；
2. fresh observe full active image ID、fresh `StartedAt` 与 active Collector main PID/process identity；
3. 从 current full-container-ID-scoped log envelope 读取 application message；
4. 用 strict parser 找到 exactly one matching v1 record；
5. 校验 application terminal fields exact key/value/schema/event type；
6. 校验 record PID 等于 fresh active Collector main PID；
7. 校验 `StartedAt <= collector_main_started_at_utc <= bounded observation time`；
8. 拒绝 stale prior-start、other-container、foreign-PID、manual、probe、duplicate、ambiguous、partial 或 malformed record；
9. active process 不存在、identity 不明确、log envelope 不可建立或 timestamp relation 不可建立时 HOLD；
10. 不把 worker thread health、PLC connection、DB health、persistence、ACK/read_done 或 accepted fact 填入本 record claim。

`Config.Image`、descriptive tag、compatibility tag、hostname 或普通 startup log 不是 full image/process identity authority。R35 的 static probe 不可复用为本 gate 的 process-bound evidence。任何 stale log、log rotation、handler loss 或 current envelope unavailable 只表示 evidence unavailable 并 HOLD，不触发新增 persistence/telemetry。

## 17. Gate sequence 与 authority separation

后续 gate sequence 冻结为：

```text
R42 Architecture consolidated repair
→ ChatGPT PM durable intake
→ fresh independent Reliability re-review
→ ChatGPT PM durable intake
→ independent Data Quality planning review
→ ChatGPT PM durable intake
→ independent Verification planning review
→ ChatGPT PM final planning-contract acceptance
→ separately authorized implementation
→ focused implementation reviews
→ separately authorized Git closeout
→ separately planned deployment/lifecycle work if needed
→ separately authorized bounded runtime-loaded validation
→ PM acceptance of RUNTIME-LOADED
→ separate production accepted-fact planning
```

Reliability re-review 必须先 PASS，之后才能进入 Data Quality review。任何前序 PASS、R42 `WRITTEN` 或历史 R35/R36 evidence 都不自动授予下一阶段。

## 18. Required non-claims 与 MVP assessment

本合同不新增 API、DB persistence、generic registry、telemetry、heartbeat、audit、forensics、status endpoint、storage surface、runtime topology、PLC/DB/ACK/read_done semantics 或 disabled-station semantics。

明确 non-claims：

```text
R42 does not prove source implementation exists.
R42 does not prove tests pass.
R42 does not prove a record was emitted.
R42 does not prove Thread.start succeeded.
R42 does not prove worker health or PLC/DB health.
R42 does not prove event persistence, ACK/read_done or production acceptance.
R42 does not provide fresh remote/container/process/log observation.
```

MVP alignment：`MVP-ALIGNED WITH BACKLOG ITEMS`。本轮只修复 Candidate A 的 false-PASS contract gaps；`record_emitted_at`、sorted scope list、API/status/telemetry 等均为 backlog 或 out-of-scope，不进入 v1。

## 19. Changed-path、allowlist 与 forbidden-action audit

任务-owned changed set 只允许：

```text
docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md
```

本轮未修改：

```text
R40 report
R41 report
任何 source/test/config/Dockerfile/Compose
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/chatgpt_pm_handoff_260730-0834.md
pm_operating_rules.md
Batch D/E
```

本轮禁止且未执行：

```text
pytest
compileall
application process
Collector construction/start
Docker/Compose
network/SSH/remote filesystem
DB/API/PLC/V-PLC
production event/synthetic accepted fact
ACK/read_done activity
git add / stage / commit / push / tag
restore/reset/stash/clean/delete/move/archive
```

## 20. Final Git/index/untracked audit与 R42 identity

R42 写入后应保持：

```text
HEAD == origin/main == ce22ca71eff0548aa064129c160f7041603855e7
HEAD^ == 35c50b1eb0f76d8b3361e8c122448ad03899559b
ahead / behind == 0 / 0
tracked dirty == empty
cached == empty
initial untracked == 303
final untracked == 304
new tracked/cached path == none
new untracked path == R42 exact report only
```

由于报告不能在不改变自身 bytes 的情况下嵌入自身最终 SHA-256，本报告的最终 regular/non-symlink、UTF-8、bytes 与 SHA-256 由写入完成后的同一 terminal read-only audit 重新测量，并在本任务 concise Chat manifest 中作为 detached final identity 返回；该 detached identity 不构成第二个 repository artifact，也不改变 changed-path allowlist。报告写入前的 R42 输出条件已确认 `ABSENT / NON-SYMLINK / UNSTAGED / UNTRACKED`。

R42 final identity 的 canonical terminal fields：

```text
path: docs/reports/sprint4_d2_r7b_i1_r42_process_bound_runtime_loaded_observability_architecture_repair.md
bytes: terminal post-write measurement in Chat manifest
SHA-256: terminal post-write measurement in Chat manifest
encoding: UTF-8
file type: regular file
symlink: NO / NON-SYMLINK
index: UNSTAGED / UNTRACKED
```

## 21. Blockers、bounded recommendations、next gate 与 Thread context

当前 R42 Architecture repair blockers：`none`。B1、B2、B3 已全部吸收；若后续 Reliability re-review 发现新的实现级问题，应以 fresh independent review 的新 blocker 返回 PM，不在本 Thread 自动修复。

bounded recommendations：

1. PM durable intake 后，开启新的独立 Reliability re-review；不得继续继承 R40/R41 Thread authority。
2. Reliability PASS 后，再分别进入 Data Quality 与 Verification planning review；不得把本报告直接当作 implementation authorization。
3. 后续 implementation 只使用 exact three-source/two-test allowlist；任何额外路径需求先 HOLD 返回 PM。
4. 保持 R35/R36/R40/R41 历史 evidence 原样，不用新记录重写过去的 activation 或 runtime classification。

Next gate：`ChatGPT PM durable intake → fresh independent Reliability re-review`

Thread context assessment：本 Architecture task 已 terminalized；不得继续执行下一 gate，不得构造 `EventCollectorWorker`，不得执行 test/application/remote/Git action。下一步必须使用新的 independent Reliability authority。

---

End state：`REPAIRED CONTRACT WRITTEN ONLY`。
