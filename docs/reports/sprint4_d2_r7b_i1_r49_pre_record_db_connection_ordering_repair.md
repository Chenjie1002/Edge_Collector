# Sprint 4 D2-R7B-I1 R49 Pre-Record DB Connection Ordering Repair Report

## 1. 报告身份与结论

- 报告名称：Sprint 4 D2-R7B-I1 R49 Pre-Record DB Connection Ordering Repair Report
- 任务名称：D2-R7B-I1 R49 — Repair Pre-Record DB Connection Ordering
- 执行 Thread：Architecture / Integration
- Authority source / ID：`PM-D2-R7B-I1-R49-PRE-RECORD-DB-CONNECTION-ORDERING-REPAIR-260730-1321`
- Report delivery mode：`REPOSITORY_DURABLE_REPORT`
- 结论：`PASS / LOCAL REPAIR WRITTEN AND TESTED`

本 authority 为一次性、仅限本地 Architecture / Integration 修复；首次授权写入时消费，不继承 R48，且不授予 Reliability、Data Quality、Verification、Git、build、Docker、remote、runtime validation 或 production acceptance 权限。

状态必须区分：R49 已 `WRITTEN`、三条授权本地验证已 `TESTED`；未 `PM-ACCEPTED`、未独立 `REVIEWED`、未 `STAGED`、未 `COMMITTED`、未 `PUSHED`、未 `DEPLOYED`、未新增 `ACTIVATED`。产品状态仍为 `ACTIVATED = YES`、`STATIC_MAPPING_INITIALIZED = YES`、`RUNTIME-LOADED = NO`、`PRODUCTION-ACCEPTED = NO`。

## 2. 初始恢复与 R48 输入身份

任何 task-owned 写入前，执行了 Prompt 指定的 read-only Git recovery。

| 项目 | 结果 |
| --- | --- |
| repository root | `/Users/chenjie/Documents/MES/edge-mes-demo` |
| branch | `main` |
| HEAD / origin/main | `4a733d7995a94398ade693822662ebd2b22f9d3d` / same |
| ahead / behind | `0 / 0` |
| cached | empty |
| tracked dirty | 仅五条预期 R48 paths |
| `git diff --check` / cached check | PASS / PASS |
| R49 report initial state | `ABSENT / NON-SYMLINK / UNTRACKED / UNSTAGED` |

初始 R48 identity 与 Prompt 完全匹配：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `collector/app/main.py` | 2524 | `e04c1e20ccb7eba71e97656c526fb951de25bd8b4f15aab4f6d3edf5d7ae97e6` |
| `collector/app/services/event_collector.py` | 24285 | `90a5d87b27544c1505280d729e8b3a99c8b5e52f207625686533d92bea8672bd` |
| `collector/app/plc/mapping.py` | 18876 | `ba39583a699f8347c0ff5eaec2e7c807dad909c815269de607a36e8b93c023a7` |
| `collector/tests/test_event_collector_reliability.py` | 27836 | `c80cf24086325171e4807751fd3a010a23da2c433c6a4e8dbcf65f0301bccd7e` |
| `tests/test_collector_station_event_runtime_source.py` | 33212 | `7b5b77f40c5bc3eff1a364064876ed79d0d28ffa5bf5f25ee9ba279498d409cd` |
| R48 report | 15692 | `caa3203630c5b321c950d078fda7424f4f1ca8edcd7f4a45b88525adfdda0d10` |

## 3. PM intake blocker、根因与边界

R48 的 source、tests 和 report 是 `WRITTEN`，但未 PM 接受、未进入独立 Reliability implementation review。本轮唯一 blocker 是成功 runtime-loaded record 之前存在 DB connection，以及原测试没有显式观察 `Storage` 构造调用与排序。

`collector/app/services/storage.py` 未修改。其 `Storage.__init__(dsn)` 的真实边界为：

```python
self.conn = psycopg.connect(dsn, autocommit=False)
```

因此每次 `Storage(...)` 都是潜在真实 DB connection，不能由 Fake 的 `.events`、写入次数或无 DB write 结论替代。

修复前 enabled path：

```text
main context → source setup → legacy Storage(database_url()) [DB connection]
→ worker constructor → worker Storage(dsn) [DB connection]
→ runtime-loaded record → Thread.start()
```

修复后 enabled path：

```text
main context → non-DB source/config setup → EventCollectorWorker constructor
→ validation + one runtime-loaded record → Thread construction/start
→ legacy main-loop Storage(database_url()) [DB connection]

worker Thread entry run_forever()
→ worker Storage(dsn) [exactly once, after Thread.start]
→ first poll_once()
```

disabled event-collector path 不构造 worker、不会产生 runtime-loaded record，仍在原 main-loop 进入前构造 legacy Storage 并维持既有产品行为。

## 4. 实现与写入 allowlist

本轮 task-owned 修改仅为：

```text
collector/app/main.py
collector/app/services/event_collector.py
collector/tests/test_event_collector_reliability.py
docs/reports/sprint4_d2_r7b_i1_r49_pre_record_db_connection_ordering_repair.md
```

实现要点：

1. `main.py` 在 enabled worker 成功构造、唯一 record 同步发出、Thread 已 construction/start 后，才构造 legacy main-loop `Storage` 与 `EventDetector`。
2. `EventCollectorWorker.__init__()` 保存私有进程内 `dsn`，不构造 `Storage`；原 mapping、resolved snapshot、canonical line、read-plan、single-use startup context、record validation 和 serialization 保持不变，record 仍是构造器最后 required action。
3. `run_forever()` 的入口首先执行 `self.storage = Storage(self.dsn)`，随后才记录 worker-start 信息和进入首次 `poll_once()`；构造失败不被 catch、不会 retry、不会补发 record。

未修改：`collector/app/services/storage.py`、`collector/app/plc/mapping.py`、`tests/test_collector_station_event_runtime_source.py`、R48 report、DB/API/schema/config/Docker/Compose/PLC/ACK/read_done 行为，以及 Batch D/E。

## 5. 测试 oracle 与结果矩阵

Reliability 测试用显式 `storage_factory` 记录每次 `Storage` constructor invocation，而不是只检查 FakeStorage 的 events/writes。关键观察值是 `storage_constructor_calls` 与跨 main path 的 ordered `events`。

| 情形 | Explicit Storage oracle | 结果 |
| --- | --- | --- |
| 成功 worker constructor | `[]` | PASS |
| read-plan / canonical-line validation failure | `[]` | PASS |
| serialization failure | `[]` | PASS |
| logger emission failure | `[]` | PASS |
| missing / foreign-PID / reused startup context | `[]` | PASS |
| enabled main success | `record → thread_construct → thread_start → legacy_storage_construct` | PASS |
| enabled main constructor failure | Thread.start false；legacy storage calls `[]` | PASS |
| `run_forever()` entry | `storage_construct → poll_once` | PASS |
| worker Storage initialization failure | one constructor call, propagated, no retry, no second runtime-loaded message | PASS |
| existing persistence / ACK/read_done / no-PLC-I/O constructor regressions | focused suite retained | PASS |

这些是 local fake-based implementation tests。它们不建立真实 DB connection、PLC I/O、runtime-loaded acceptance、deployed-process evidence 或 production truth。

## 6. TDD、修复窗口与验证

根因假设：两个 eager `Storage(...)` 调用越过了 R42/R45 的 success-record side-effect boundary；把 legacy construction 移至 `Thread.start()` 后、把 worker construction 移至 `run_forever()` entry 可以关闭该边界而不改变 polling/persistence/ACK/read_done。

先写入显式 constructor/order oracle 并运行完整 focused pytest A，观察到红灯；初始失败证明旧 eager construction/ordering 不符合新增断言。随后完成最小产品改动。验证期间发生两项仅限测试夹具的机械修复，均未改变 ordering、record、single-use 或 PASS/HOLD 语义：异常路径先保存 call list，以及在 mock global `json.dumps` 前加载 mapping。预授权窗口使用 `2 / 2` cycles，之后没有进一步改写三条 R49 source/test paths。

执行锁后的三条可写 source/test identity：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `collector/app/main.py` | 2525 | `d1a461294c91f9f86cde4af87b21bb1147bed5561d64028e8462a8f57d46de80` |
| `collector/app/services/event_collector.py` | 24313 | `02cab6ea15572ae0b2f6059462f9cd6856cd483ab0dcc37c87d39267aad1e8e2` |
| `collector/tests/test_event_collector_reliability.py` | 32253 | `fa8a677f5a249b849438b7ec43e2bbd14ff14e8c590e54d02274daa640b06835` |

精确验证命令与结果：

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile \
  collector/app/main.py \
  collector/app/services/event_collector.py \
  collector/app/plc/mapping.py \
  collector/tests/test_event_collector_reliability.py \
  tests/test_collector_station_event_runtime_source.py
```

结果：PASS，exit code 0。

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -m pytest \
  collector/tests/test_event_collector_reliability.py \
  -q
```

结果：PASS，`24 passed, 8 subtests passed in 0.22s`。

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -m pytest \
  tests/test_collector_station_event_runtime_source.py \
  -q
```

结果：PASS，`56 passed in 0.14s`。

## 7. 保护路径、Git 与 untracked 审计

保护 path 的终态 identity 与 R49 intake 完全一致：

| Protected path | Bytes | SHA-256 | Comparison |
| --- | ---: | --- | --- |
| `collector/app/plc/mapping.py` | 18876 | `ba39583a699f8347c0ff5eaec2e7c807dad909c815269de607a36e8b93c023a7` | IDENTICAL |
| `tests/test_collector_station_event_runtime_source.py` | 33212 | `7b5b77f40c5bc3eff1a364064876ed79d0d28ffa5bf5f25ee9ba279498d409cd` | IDENTICAL |
| R48 report | 15692 | `caa3203630c5b321c950d078fda7424f4f1ca8edcd7f4a45b88525adfdda0d10` | IDENTICAL |

写入 R49 report 前：raw `git ls-files --others --exclude-standard` count 为 310；按 repository-relative full path 的 UTF-8 stable sort 后 count 也为 310。分类是 Batch D 300 + Batch E 1 + R40–R48 9，unknown 0，missing 0。report 写入后终态应为且 post-write audit 确认：Batch D 300 + Batch E 1 + R40–R49 10 = 311，raw 与 normalized count 都必须为 311，unknown 0。

终态 Git 要求和审计：cached 仍 empty；`git diff --check` 与 `git diff --cached --check` PASS；未 stage、commit、push 或 tag。`git diff --name-only` 可见五条 R48 tracked dirty paths，其中 mapping/runtime-source 两条已按保护 identity 保持 byte-identical；R49 新增变化只在允许的 `main.py`、`event_collector.py` 与 Reliability test。

## 8. Forbidden-action counters、边界与建议

| Action category | Count |
| --- | ---: |
| Git stage / commit / push / tag / reset / restore / stash / clean | 0 |
| build / package | 0 |
| Docker / Compose | 0 |
| remote / SSH / network / curl | 0 |
| real DB connection/query/write/migration | 0 |
| PLC / V-PLC connection/read/write | 0 |
| application startup / runtime validation / A–H evidence | 0 |
| Batch D/E open, modify, delete, move, stage or reclassify | 0 |

Blockers：none for this bounded local implementation gate.

Recommendations：PM durable intake must independently verify this exact report and final identities. Only after PM accepts R49 may a new independent Reliability implementation review assess the record-before-DB ordering, constructor no-Storage boundary, one-shot context, scope validation and no-side-effect behavior. Do not infer Data Quality、Verification、Git、build、Docker、remote、runtime validation、`RUNTIME-LOADED` or `PRODUCTION-ACCEPTED` authority.

MVP 路径一致性：`MVP-ALIGNED`。本轮仅关闭一个会使 runtime-loaded record 错误越过 DB connection boundary 的具体 false-PASS 风险；没有引入 API、DB persistence、telemetry、retry、DI framework、audit/forensics、retention、运行时拓扑或产品能力。

Thread 输出 / 上下文评估：长 durable report；当前 Thread 不建议继续，下一轮必须新开独立 Thread，因为 R49 authority 已消费且后续 Reliability review 不能继承实现权限。

## 9. 下一 gate 与 report identity

唯一 next gate：

```text
R49 local repair WRITTEN
→ ChatGPT PM durable intake
→ independent Reliability implementation review only after PM accepts R49
```

本报告自身的终态 bytes/SHA-256 不能嵌入自身而不改变 bytes；它由 post-write detached read-only audit 记录在本任务 Chat manifest。该 identity 仅证明本报告 bytes，不能形成 PM acceptance、review、Git、deploy、runtime 或 production authority。
