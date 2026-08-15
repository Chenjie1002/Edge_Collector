# A1 VP2-G5 Local Candidate Reliability Focused Review — Shadow PM Recovery R1

## 1. 结论与 authority

```text
结论 = PASS / A1_VP2_G5_LOCAL_CANDIDATE_RELIABILITY_FOCUSED_REVIEW
执行 Thread = Reliability / shadow_reliability
Evidence class = LOCAL STATIC + LOCAL TEST EVIDENCE ONLY
REPORT_DELIVERY_MODE = REPOSITORY_DURABLE_REPORT
REPORT_PATH = docs/reports/mainline_pm_a1_vp2_g5_local_candidate_reliability_focused_review_20260815T0128Z.md
REPORT_WRITE = exactly once, after all review checks
```

Task self-identity 机械核验通过：

```text
TASK_PATH = docs/thread_handoff/pm_task_20260815T0128Z_shadow_pm_a1_vp2_g5_local_candidate_reliability_focused_review.md
TASK_TYPE = regular / non-symlink
TASK_BYTES = 16443
TASK_SHA256 = e2bbae2dc6268c538d7fe0341cd0ee6cdea87d946c61ce5920c6dbdeaaf8f4c1
TASK_SELF_IDENTITY = PASS
```

本报告只使用 task Section 7 的 required-reading 顺序和 Section 8 fresh facts；未继承其他
Thread、predecessor HOLD、repair、Verification、Git、runtime 或 Goal acceptance authority。
Required-reading 文件均成功读取，并在读后确认 regular/non-symlink；未发现影响本 claim 的
缺失、symlink、scope 或 authority 冲突。未执行 Data Quality routine re-review，未进入
Verification。

## 2. Fresh root / Git / candidate facts

```text
PWD_P = /Users/chenjie/Documents/MES/edge-mes-demo
GIT_ROOT = /Users/chenjie/Documents/MES/edge-mes-demo
BRANCH = main
HEAD = 1d63d2febdb05a8177e2b64acd9850a88d87c255
ORIGIN_MAIN = 1d63d2febdb05a8177e2b64acd9850a88d87c255
AHEAD_BEHIND = 0/0
STAGED = EMPTY
TRACKED_DIRTY = collector/app/services/station_event_runtime_source.py; tests/test_collector_station_event_runtime_source.py
REPORT_PRESTATE = ABSENT / NOT_IGNORED / NOT_INDEXED
```

Protected candidate entry/final expected identity：

```text
SOURCE = collector/app/services/station_event_runtime_source.py
SOURCE_TYPE = regular / non-symlink
SOURCE_BYTES = 7790
SOURCE_SHA256 = ee48d2cedf837d65970a76c618b7dd08748c422c9557b5d60c7ed06336910d2c
SOURCE_NUMSTAT = 2 insertions / 1 deletion

TEST = tests/test_collector_station_event_runtime_source.py
TEST_TYPE = regular / non-symlink
TEST_BYTES = 37617
TEST_SHA256 = afdadc6f7c1fd6e5f3971a108d5a5d2667763bcef653d4a54bed892691cd059f
TEST_NUMSTAT = 37 insertions / 0 deletions

git diff --check = PASS
git diff --cached --check = PASS
```

## 3. Static diff containment

Source diff is exactly the accepted `_decode_result` boundary：

```diff
-    return str(decoded).lower()
+    normalized = str(decoded).lower()
+    return "skip" if normalized == "skipped" else normalized
```

The inherited test diff contains only the `_decode_result` import and 37 added lines for the
result-code table plus WS02/WS03 source-payload regression. No mapping, validator, adapter,
storage, transaction, ACK/read_done, retry, reserved NOK `30003`, config, PLC/V-PLC, DB/API,
Docker, UI or other runtime-safety surface changed. No out-of-scope product path changed.

The source call boundary remains: `build_runtime_source_payload()` calls `_decode_result()`,
then emits the source payload consumed by the unchanged `adapt_source_payload()` validation
boundary. The adapter remains the decision boundary; this change does not synthesize acceptance,
projection, persistence, ACK or read_done behavior.

## 4. Result normalization behavior matrix

| Input / mapping result | Expected canonical output | Evidence |
|---|---|---|
| `None` | `None` | unchanged early return in `_decode_result` |
| `OK` | `ok` | exact result-code table regression, code `1` |
| `NOK` | `nok` | exact result-code table regression, code `2` |
| `SKIPPED` | `skip` | exact result-code table regression, code `3`; only new alias |
| `UNKNOWN` | `unknown` | exact result-code table regression, code `0` |
| other fallback value | existing lowercase behavior | unchanged `str(decoded).lower()` fallback; only exact `skipped` is remapped |

因此 `NON_SKIPPED_BEHAVIOR = PRESERVED`，result code `3` 的 business/mapping token 仍为
`SKIPPED`，但 adapter validation 前的 runtime-source canonical token 为 `skip`。没有
fail-open 变化：validator/adapter policy、invalid-result handling、storage and ACK/read_done
ownership remain outside the diff and unchanged.

## 5. WS02/WS03 与 adapter guard evidence

`tests/test_collector_station_event_runtime_source.py` 的新增回归使用 real
`config/mapping.yaml`，对 WS02 和 WS03 构造 `result = 3`、raw bytes source payload，并分别
断言 `payload["result"] == "skip"` 且不等于 `"skipped"`。两条路径都通过。

指定 adapter guard 使用 unchanged `station_event_adapter.py` 与
`test_route_predecessor_mismatch_rejects_system_reserved_detail_without_adapter_synthesis`：

```text
route predecessor mismatch + system_reserved NOK 30003
decision = rejected / UPSTREAM_EVIDENCE_INVALID
projection_metadata = None
adapter synthesis = none
```

该 guard 通过，证明本候选没有放宽 route-predecessor、system-reserved detail、NOK `30003`
或 adapter rejection boundary。静态 source/adapter review 亦确认未触及 storage transaction、
ACK/read_done ordering、retry/idempotency 或 process ownership。

## 6. Exact local pytest evidence

Test budget and actual counters：

```text
PYTEST_COMMANDS = 2 / max 2
RETRY = 0
FALLBACK = 0
SECOND_INTERPRETER = 0
DEPENDENCY_INSTALL = 0
```

1. Invocation：

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=collector:. .venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_collector_station_event_runtime_source.py
```

```text
EXIT = 0
SUMMARY = 65 passed in 0.19s
```

2. Invocation：

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=collector:. .venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_collector_station_event_adapter.py::test_route_predecessor_mismatch_rejects_system_reserved_detail_without_adapter_synthesis
```

```text
EXIT = 0
SUMMARY = 1 passed in 0.04s
```

Task-local delegated runtime remained the exact `.venv/bin/python` override from the task:
resolved Python 3.13.3, arm64, resolved bytes `119328`, SHA-256
`f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5`, pytest `9.1.1`.
No bytecode/cacheprovider or dependency mutation was authorized or observed.

## 7. Write, state separation and counters

The report was created exactly once at the exact allowlisted path after all static checks and
both pytest commands passed. Immediately after the write, final report identity, source/test
identity, exact changed paths, staged state and Git checks were mechanically audited; the final
report bytes and SHA-256 are published in the Section 15 window manifest. The report does not
claim a self-referential hash inside its own bytes.

```text
CHANGED_FILES = exact report path only
SOURCE_TEST_MUTATION = 0 during this review
REPORT_WRITE = 1
GIT_MUTATIONS = 0
REMOTE_ACTIONS = 0
RUNTIME_ACTIONS = 0
DB_ACTIONS = 0
DOCKER_ACTIONS = 0
PLC_VPLC_ACTIONS = 0
UI_ACTIONS = 0
SUB_AGENT = 0
```

State separation：

```text
WRITTEN = YES / this report only
REVIEWED = YES / this child review
ACCEPTED = NOT ESTABLISHED / parent independent intake required
VERIFIED = NOT ESTABLISHED
STAGED = NO
COMMITTED = NO
PUSHED = NO
RUNTIME_LOADED = NOT CLAIMED
REMOTE_VERIFIED = NOT CLAIMED
PRODUCTION_ACCEPTED = NOT CLAIMED
A1_VP2_G5_ACCEPTED = NO
OWNER_VISUAL_ACCEPTED = NO
```

## 8. Blockers / recommendations / MVP

```text
Blockers = none
Recommendations = none
```

MVP 路径一致性：`MVP-ALIGNED`。本 review 直接支持 accepted station-result data path 的最小
invariant：result code `3` 在 adapter validation 前输出 canonical `skip`，而既有结果语义、
ACK/read_done、storage and adapter safety boundary 不变。新增 product capability、architecture、
runtime topology、evidence platform、retention or threat-model scope = none；没有把 review
framework 当作产品交付物。

Thread 输出 / 上下文评估：

```text
TASK_SIZE = small / sufficient
SUB_AGENT_PLAN = no / none
SUB_AGENT_ACTUAL = no / none
CURRENT_THREAD_CAN_CONTINUE = yes
OWNER_NEXT_ROUND_MANUAL_NEW_TOP_LEVEL_THREAD = no
REASON = single focused Reliability review; parent retains independent intake and this child stops after report
```

唯一 next gate：

`SHADOW_MAINLINE_PM_PARENT_INDEPENDENT_INTAKE_OF_RELIABILITY_REPORT`

Parent must independently read this actual report, verify its final identity, source/test identity,
changed paths, test evidence, Git state, scope, MVP alignment and state separation. This PASS does
not authorize Verification, repair, Git publication, remote/runtime, DB/API, Docker, PLC/V-PLC,
UI, production acceptance or A1-S2.

