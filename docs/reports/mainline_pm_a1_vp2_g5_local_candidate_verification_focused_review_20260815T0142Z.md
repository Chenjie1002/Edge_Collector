# A1 VP2-G5 Local Candidate Verification Focused Review — Shadow PM Recovery R1

## 1. 结论与任务身份

```text
结论 = PASS / A1_VP2_G5_LOCAL_CANDIDATE_VERIFICATION_FOCUSED_REVIEW
任务名称 = SHADOW-PM-A1-VP2-G5-LOCAL-CANDIDATE-VERIFICATION-FOCUSED-REVIEW-20260815T0142Z
执行 Thread = Verification / shadow_verification
Evidence class = LOCAL STATIC + LOCAL TEST EVIDENCE ONLY
REPORT_DELIVERY_MODE = REPOSITORY_DURABLE_REPORT
REPORT_PATH = docs/reports/mainline_pm_a1_vp2_g5_local_candidate_verification_focused_review_20260815T0142Z.md
REPORT_WRITE = exactly once, after all verification checks
```

本 exact task file 已先完成 launcher identity gate：

```text
TASK_PATH = docs/thread_handoff/pm_task_20260815T0142Z_shadow_pm_a1_vp2_g5_local_candidate_verification_focused_review.md
TASK_TYPE = regular / non-symlink
TASK_BYTES = 17188
TASK_SHA256 = 2c2b5eeb1813d50c7162f2dbd5d468a8c6bd0b6804ee2805c9b64dccdf4a3de9
TASK_SELF_IDENTITY = PASS
AUTHORITY_MODEL = task file is complete and unique authority
```

未继承其他 Thread 的隐含 authority；本报告只建立 `WRITTEN`，不建立
`ACCEPTED`、`VERIFIED`、`STAGED`、`COMMITTED`、`PUSHED`、`RUNTIME_LOADED`、
`REMOTE_VERIFIED` 或 `PRODUCTION_ACCEPTED`。

## 2. Required reading、root 与 parent evidence

Section 7 reading order 已完成：

1. 本 exact task file；
2. `docs/thread_handoff/pm_operating_rules.md`；
3. `docs/current_status.md`；
4. Shadow PM Charter；
5. Charter Amendment 001；
6. Shadow PM Ledger；
7. Mainline-accepted local repair report；
8. Parent-accepted Reliability report；
9. `collector/app/services/station_event_runtime_source.py`；
10. `tests/test_collector_station_event_runtime_source.py`；
11. `collector/app/services/station_event_adapter.py`；
12. `tests/test_collector_station_event_adapter.py` 中仅与指定 adapter guard 相关的 helper、fixture 与 test。

Required-reading inputs 均可读取且未发现影响本 claim 的 authority 冲突。现场 root：

```text
PWD_P = /Users/chenjie/Documents/MES/edge-mes-demo
GIT_ROOT = /Users/chenjie/Documents/MES/edge-mes-demo
```

Parent-accepted Reliability evidence identity/content：

```text
RELIABILITY_REPORT = docs/reports/mainline_pm_a1_vp2_g5_local_candidate_reliability_focused_review_20260815T0128Z.md
RELIABILITY_REPORT_TYPE = regular / non-symlink
RELIABILITY_REPORT_BYTES = 8643
RELIABILITY_REPORT_SHA256 = f8fd9b9eb248c7852d3906dfbd4351f20a1a5e12b5f7896a6cb7afe61f6c88ff
RELIABILITY_TERMINAL = PASS / A1_VP2_G5_LOCAL_CANDIDATE_RELIABILITY_FOCUSED_REVIEW
RELIABILITY_PARENT_INTAKE = ACCEPT PASS
RELIABILITY_RECOMMENDATIONS = none
```

该 parent report 明确其证据类别为 local static + local test only，并绑定下述 source/test
identity；它是 predecessor evidence，不是本 Verification self-acceptance。

## 3. Fresh live facts 与 same-candidate binding

Report 写入前 fresh facts：

```text
BRANCH = main
HEAD = 1d63d2febdb05a8177e2b64acd9850a88d87c255
ORIGIN_MAIN = 1d63d2febdb05a8177e2b64acd9850a88d87c255
AHEAD_BEHIND = 0/0
STAGED = EMPTY
TRACKED_DIRTY = collector/app/services/station_event_runtime_source.py; tests/test_collector_station_event_runtime_source.py
GIT_DIFF_CHECK = PASS
GIT_DIFF_CACHED_CHECK = PASS
```

Final candidate identity：

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
```

Reliability report reviewed exactly the same source/test bytes and hashes. Therefore：

```text
FINAL_REVIEWS_BIND_SAME_CANDIDATE = YES
```

Candidate diff containment is exact：

```diff
-    return str(decoded).lower()
+    normalized = str(decoded).lower()
+    return "skip" if normalized == "skipped" else normalized
```

Source change is only the `_decode_result` exact `skipped` -> `skip` canonicalization. Test
change is only the imported `_decode_result` plus 37 inserted lines covering the result-code
table and WS02/WS03 source-payload regression. No mapping, validator, adapter, storage,
transaction, ACK/read_done, retry, reserved NOK `30003`, config, PLC/V-PLC, DB/API, Docker or
UI path changed.

Report path prestate before this write was `ABSENT / NOT_IGNORED / NOT_INDEXED`.

## 4. Independent result-normalization matrix

本 review independently read `_decode_result` and the persisted focused test WIP，且执行了完整
runtime-source test file：

| Input / mapping result | Canonical output | Independent evidence |
|---|---|---|
| `None` | `None` | `_decode_result` unchanged early return |
| `OK` | `ok` | result-code table control, code `1` |
| `NOK` | `nok` | result-code table control, code `2` |
| `SKIPPED` | `skip` | code `3` test and exact source alias |
| `UNKNOWN` | `unknown` | result-code table control, code `0` |
| other fallback value | existing lowercase behavior | unchanged `str(decoded).lower()` fallback; only exact lowercase `skipped` aliases to `skip` |

`config/mapping.yaml` 的 business token `SKIPPED`、canonical validator vocabulary、V-PLC
result code `3` 与 adapter decision boundary 均未改动。没有把 alias 修复扩大为新的
fallback、fail-open、storage、ACK/read_done 或 acceptance policy。

## 5. WS02/WS03 regression 与 adapter rejection guard

`test_downstream_skipped_result_builds_canonical_skip_source_payload` 使用 real
`config/mapping.yaml`、resolved runtime snapshot、result code `3` 和 raw source bytes，
分别覆盖 WS02 与 WS03，并断言 `payload["result"] == "skip"` 且不等于 `"skipped"`。
这是对 accepted defect 的 source-payload path regression，不是 synthetic replacement。

指定 adapter guard 为：

```text
test_route_predecessor_mismatch_rejects_system_reserved_detail_without_adapter_synthesis
route_from = WS99
upstream evidence station = WS01
detail role = system_reserved
NOK code = 30003
expected decision = rejected / UPSTREAM_EVIDENCE_INVALID
projection_metadata = None
adapter synthesis = none
```

`station_event_adapter.py` 的 route/predecessor、reserved detail 与 projection boundary 保持
unchanged；该 guard 独立通过。它不建立任何 remote/runtime/production evidence。

## 6. Exact pytest evidence

Task Section 11 的两条命令按规定顺序各执行一次：

1. `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=collector:. .venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_collector_station_event_runtime_source.py`

   ```text
   EXIT = 0
   SUMMARY = 65 passed in 0.16s
   INVOCATIONS = 1
   ```

2. `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=collector:. .venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_collector_station_event_adapter.py::test_route_predecessor_mismatch_rejects_system_reserved_detail_without_adapter_synthesis`

   ```text
   EXIT = 0
   SUMMARY = 1 passed in 0.03s
   INVOCATIONS = 1
   ```

Test runtime identity remained task-frozen：

```text
ENTRYPOINT = .venv/bin/python
RESOLVED = /Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13
VERSION = Python 3.13.3
ARCHITECTURE = arm64
RESOLVED_BYTES = 119328
RESOLVED_SHA256 = f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5
PYTEST = 9.1.1
PYTHON_BINDING = PYTHONPATH=collector:.
```

Counters：

```text
PYTEST = 2 / max 2
RETRY = 0
FALLBACK = 0
SECOND_INTERPRETER = 0
DEPENDENCY_INSTALL = 0
```

## 7. Scope、state separation 与 writes

本 child 未修改 source/test；唯一 repository write 是本 exact report path。未执行或触及
Git mutation、remote、runtime、DB/API、Docker、PLC/V-PLC、UI、production stimulus 或
sub-agent。

```text
CHILD_REPOSITORY_WRITES_OUTSIDE_REPORT = 0
SOURCE_TEST_MUTATION = 0
REPORT_WRITE = 1
SUB_AGENT = 0
GIT_MUTATIONS = 0
REMOTE_ACTIONS = 0
RUNTIME_ACTIONS = 0
DB_ACTIONS = 0
DOCKER_ACTIONS = 0
PLC_VPLC_ACTIONS = 0
UI_ACTIONS = 0
```

状态严格分离：

```text
WRITTEN = YES / this report only
REVIEWED = YES / this independent Verification review
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

Report 写入后的 final identity、exact changed-path audit 与 Git audit 必须以本 report 写入后
机械输出和 Section 15 child manifest 为终端值；报告不嵌入自身 SHA，以避免自引用哈希造成
第二次写入。写后审计确认只新增本 exact report，保留既有 source/test dirty candidate，
staged 仍为空。

## 8. Blockers、Recommendations、MVP 与 Thread context

```text
Blockers = none
Recommendations = none
```

MVP 路径一致性：`MVP-ALIGNED`。本 review 直接服务 accepted station-result data path 的最小
invariant：result code `3` 在 adapter validation 前输出 canonical `skip`，同时保留所有其他
result semantics 与 safety boundary。新增 product capability、architecture、runtime topology、
evidence platform、retention 或 threat-model scope = none；验证框架没有替代产品交付。

Thread 输出 / 上下文评估：

```text
TASK_SIZE = small / sufficient
SUB_AGENT_PLAN = no / none
SUB_AGENT_ACTUAL = no / none
CURRENT_THREAD_CAN_CONTINUE = yes
OWNER_NEXT_ROUND_MANUAL_NEW_TOP_LEVEL_THREAD = no
REASON = single independent Verification review; parent retains final intake and this child stops after report
```

## 9. Next gate

唯一 next gate：

`SHADOW_MAINLINE_PM_PARENT_INDEPENDENT_INTAKE_OF_VERIFICATION_REPORT`

Parent 必须读取实际 report，重新核验 report bytes/SHA、Reliability report identity/content、
source/test identity、changed paths、tests、Git state、scope、MVP alignment 与 state separation。
本 PASS 不自动授权 Goal closeout、Git publication、remote/runtime、DB/API、Docker、PLC/V-PLC、
UI、production acceptance、Owner visual acceptance 或 A1-S2。

