# Sprint 4 D2-R7B-I1 R65-R6-SR3-R2 Focused Expected-Authority Binding, Expected-Pin Duplicate Preservation, Command-9 Topology Validation, and Chronological Predecessor-Gate Repair Report

## 1. 任务身份与结论

- 任务：`D2-R7B-I1 R65-R6-SR3-R2 — Focused Terminal-06 Expected Authority Binding, Terminal-07 Requirements Authority Parsing, Command-9 Topology Validation, and Strict R66 Progression Repair`
- 执行 Thread：`Architecture / Integration`
- authority：`PM-D2-R7B-I1-R65-R6-SR3-R2-FOCUSED-IN-PLACE-REPAIR-260731-1329`
- Delivery：`REPOSITORY_REPORT_WITH_ARTIFACTS`
- 结论：`HOLD / REPAIR_CYCLE_BUDGET_EXHAUSTED`
- 报告写入 UTC：`2026-07-31T05:49:15Z`

本轮没有通过 local gate，且本 authority 已 terminalized。不得继续修改 producer、test 或 execution lock；不得重跑或重试测试；不得进入 R66、review、Docker、Git 或远端阶段。

## 2. Pre-repair live baseline 与范围

首次写入前，repository 是 `/Users/chenjie/Documents/MES/edge-mes-demo`，branch `main`，且 `HEAD = origin/main = 0e7544a12b00799780d76723ca0de781bc2e8ad7`，ahead/behind `0 / 0`。tracked/cached diff 均为空，两个 whitespace check 均 PASS，且 `934ced7b9659cb566628b1709cf6d73463a534d8` 是 `HEAD` ancestor。

受限 Batch D/E 只通过两条授权 `.exact_paths[]` expression 提取路径；未读取其内容。pre-repair membership 为 `329 raw / 329 unique / 0 duplicate / 0 unknown / 0 missing`。原 SR3、SR3-R1、producer、test 与 schema-v2 lock 均为 regular、non-symlink、strict UTF-8、untracked、unstaged、not indexed；新 SR3-R2 report 初始为 `ABSENT / NON-SYMLINK / NOT INDEXED`。

原始身份均精确匹配：

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| original SR3 report | 10743 | `5ddcfbcfe75d9bb4daff2c9912776ad7280b13bcaf84603689fd79c238e98128` |
| SR3-R1 report | 9265 | `7e7099332db2bbec9d611827073b2bfc55680b15e7df00850e69ad28653c5a61` |
| producer/parser | 31188 | `fa51372fc850ea49517226194103f05992a6bc5b654a74e85c04d46e4d91ee42` |
| focused test | 15464 | `166b4d42c4c3fc82b594498240f371af188421e5bba7c284265cc568bd0ee2cc` |
| schema-v2 execution lock | 10511 | `22533d1eade03bd9098a04dc0e5d9ac8443871b55d0775ba172efb7f9319e551` |

## 3. 已尝试的 scoped repair 与 RED evidence

只在允许的 producer/test exact paths 内进行了 initial pass 和两次 bounded repair cycles。新增的测试意图覆盖：terminal-01 raw publication/lineage/canonical inventory digest 的 typed immutable authority；raw locked requirements 的 duplicate-before-dedup parser；raw command-9 inspect network/read-only/tmpfs/two-mount topology；以及 `authorize_next_r66_action(...)` 的 chronological pre-action prefixes。

首次完整 focused suite 是预期 RED：新测试调用尚不存在的 typed-authority APIs，结果 `99 failed, 69 passed`。这证明新增测试在 producer 尚未实现新合同前会失败。

cycle 1 后的完整 suite 在 collection 阶段 HOLD：Python 3.13 在该 test 的 dynamic import loading style 下处理 `@dataclass` authority container 时报 `AttributeError: 'NoneType' object has no attribute '__dict__'`。cycle 2 将该容器换为显式 immutable `__slots__` classes 后重新运行完整同一命令。

## 4. Terminal test failure

唯一允许的命令为：

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m pytest -p no:cacheprovider docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/test_candidate_evidence_producer.py -q
```

最后一次运行结果：exit `1`，`167 passed, 1 failed`，skipped `0`，xfailed `0`，duration `0.11s`。

失败测试为 `test_terminal06_requires_typed_terminal01_authority_not_list_or_actual_copies`。它试图对 parser-returned immutable `mappingproxy` actual inventory 直接调用 `json.dumps(actual)`，在到达 terminal-06 fail-closed assertion 前产生：

```text
TypeError: Object of type mappingproxy is not JSON serializable
```

此错误位于 task-owned focused test fixture 的 JSON round-trip construction，而不是 Docker、candidate、runtime 或 product source。依 Prompt，任何 complete suite failure 与 repair-cycle budget exhausted 都使 authority terminalized；本 Thread 不得进行第三次修复，不能把该失败改写为 PASS。

## 5. Post-failure immutable audit

未替换 execution lock。它仍是 schema `2`、lock ID `D2-R7B-I1-R65-R6-SR3-R1-EXECUTION-LOCK-260731-051850`、SR3-R1 authority，身份仍为 `10511 / 22533d1eade03bd9098a04dc0e5d9ac8443871b55d0775ba172efb7f9319e551`。

原 SR3 与 SR3-R1 reports 身份未变。失败后草稿身份为：

| Artifact | Final bytes | Final SHA-256 | Role |
| --- | ---: | --- | --- |
| `docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/candidate_evidence_producer.py` | 42337 | `e9295405d44e1b1645f3804ce65309cd512e10e135e65da57c4f04539bf0d0d8` | unaccepted repair draft |
| `docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/test_candidate_evidence_producer.py` | 29023 | `244fe093114d94506891d1523d312bddb60fbdbc843d8b80f5406496e0a41875` | failing focused-test draft |

Post-failure Git checks仍为 tracked diff empty、cached diff empty、staged false。报告写入前的 membership 仍为 `329`；本 report 作为唯一新 output 使 expected final membership 为 `330`，但它不是 PASS release evidence。exact evidence directory 未发现 `.pytest_cache`、`__pycache__` 或 `.pyc`。Docker、network、remote、package install、application test、Git stage/commit/push/tag 均为 `0`；task-owned final process count `0`。

## 6. Blockers、边界与下一 Gate

### Blockers

1. `SR3-R2-TEST-001`: JSON round-trip negative fixture does not materialize frozen mapping entries before serialization; final suite fails.
2. `SR3-R2-REPAIR-BUDGET-001`: initial local pass plus two post-failure repair cycles have been consumed; third repair is prohibited.

四个 SR3-R1 PM intake blockers不得标记 `CLOSED`：没有 final passing suite、没有 final-test identity freeze、没有 schema-v3 lock replacement 或 post-lock audit。

### Non-claims

所有本轮证据仍是 local/static/synthetic only。`PM ACCEPTED = NO`，`BUILD READY = NO`，`R66 AUTHORIZED = NO`，`BUILT = NO`，`LOCAL IMAGE ACCEPTED = NO`，`DEPLOYED = NO`，`RUNTIME-LOADED = NO`，`PRODUCTION-ACCEPTED = NO`。

### MVP 路径一致性

- 当前任务直接服务于批准 MVP：yes；目标是 future local linux/arm64 Collector candidate build/image acceptance 的 minimum expected/actual authority invariant。
- 引入额外产品能力、threat model、evidence framework 或 runtime topology：no。
- classification：`MVP-ALIGNED WITH BLOCKING LOCAL TEST FIXTURE DEFECT`。

### Next gate

```text
HOLD SR3-R2 repair package WRITTEN
-> ChatGPT PM durable intake only
```

仅 PM 可决定是否用一个新的 explicit authority 对 failing test fixture 进行最小修复；本 Thread 不自行发布任何 Reliability、Data Quality、Verification、R66、Docker、Git、remote 或 runtime Prompt。
