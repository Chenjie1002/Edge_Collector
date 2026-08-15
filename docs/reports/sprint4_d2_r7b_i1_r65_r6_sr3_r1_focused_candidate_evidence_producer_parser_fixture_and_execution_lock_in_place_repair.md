# Sprint 4 D2-R7B-I1 R65-R6-SR3-R1 Focused Candidate Evidence Producer / Parser, Fixture Coverage, and Execution-Lock In-Place Repair Report

## 1. 任务身份与结论

- 任务：`D2-R7B-I1 R65-R6-SR3-R1 — Focused Producer/Parser Contract Repair, Static Fixture Expansion, and Execution-Lock In-Place Replacement`
- 执行 Thread：`Architecture / Integration`
- authority：`PM-D2-R7B-I1-R65-R6-SR3-R1-FOCUSED-IN-PLACE-REPAIR-260731-1300`
- Delivery：`REPOSITORY_REPORT_WITH_ARTIFACTS`
- 结论：`PASS`

本报告仅记录一次 local/static/synthetic focused repair 已写入。原 SR3 PM intake 的 `HOLD / PM ACCEPTED NO` 保持其历史意义；本报告不构成 PM intake、PM acceptance、BUILD READY、R66 authority、Docker build、candidate image、remote、runtime 或 production 事实。

## 2. 预修复门禁、身份与 allowlist

fresh recovery 的 repository 为 `/Users/chenjie/Documents/MES/edge-mes-demo`，branch 为 `main`；`HEAD = origin/main = 0e7544a12b00799780d76723ca0de781bc2e8ad7`，ahead/behind 为 `0 / 0`，tracked/cached diff 均为空，两个 whitespace check 均 PASS，且 product commit `934ced7b9659cb566628b1709cf6d73463a534d8` 是 `HEAD` ancestor。

预写入 identity 全部匹配，且均为 regular、non-symlink、strict UTF-8、untracked、unstaged、not indexed：

| Artifact | Previous bytes | Previous SHA-256 |
| --- | ---: | --- |
| original SR3 report | 10743 | `5ddcfbcfe75d9bb4daff2c9912776ad7280b13bcaf84603689fd79c238e98128` |
| producer/parser | 21139 | `91250d8d65abaa1bdf6ef843cf394cc7ef0614c7df2013b4737e035137be3708` |
| focused test | 10560 | `88bdcdb7d9382993978bfe629c2da9182950a9fca44a633b77a85ca752f5d606` |
| invalid lock | 8092 | `db8692c39bc4425465c4f8d83ad755a6dd8c93dc65c5e7cb059da707a32b7d71` |

本报告 initial path 为 `ABSENT / NON-SYMLINK / NOT INDEXED`。受限 Batch D/E extraction 仅使用两条 fixed `.exact_paths[]` expressions；与其余 Prompt-named external paths 的 repository-relative UTF-8 bytewise comparison（dedup 前检查）确认 pre-repair membership 为 `328 raw / 328 unique / 0 duplicate / 0 unknown / 0 missing`。

仅修改以下三项 artifact 并创建本报告；原 SR3 report、product source、status、roadmap、handoff 和所有其它 existing artifact 均未修改。

## 3. 五个 PM intake blocker closure

| Blocker | Status | In-place closure / focused evidence |
| --- | --- | --- |
| `PM-SR3-INTAKE-001` | `CLOSED` | lock schema-v2 用实测 UTC 取代 future local chronology；见 §6。 |
| `PM-SR3-INTAKE-002` | `CLOSED` | 06 接收 independently supplied expected source inventory，并逐 path/type/mode/bytes/SHA 比较 candidate-read actual；缺失、extra、reorder、duplicate、alias、copy-back 与字段 mismatch 均 HOLD。 |
| `PM-SR3-INTAKE-003` | `CLOSED` | source walker 逐目录项 `lstat`；regular-only、link count 1，symlink/hardlink/FIFO/socket/device/unknown/stat/read failure 均 fail closed。 |
| `PM-SR3-INTAKE-004` | `CLOSED` | parser framing 只接受 U+0020/U+0009/U+000A/U+000D；不以 no-argument `strip/lstrip/rstrip` 作为 JSON framing。 |
| `PM-SR3-INTAKE-005` | `CLOSED` | R66 canonical records 逐 argv/number/classification 验证并机械计算预算；pure Gate A/B/C/Final validator 保留 terminal-10 self-exclusion。 |

terminal 07 现在要求独立传入、closed-validated 的四个 top-level pins（`httpx==0.28.1`、`psycopg[binary]==3.2.3`、`PyYAML==6.0.2`、`python-snap7==3.0.0`）；candidate distribution inventory 只作为 actual。common root/schema/binding failure 同时抑制 06/07/09；source comparison failure 只抑制 06，pins failure 只抑制 07，command-9 facts failure 只抑制 09。

## 4. Focused fixture evidence and repair cycle

唯一执行的 test command 为：

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m pytest -p no:cacheprovider docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/test_candidate_evidence_producer.py -q
```

覆盖包括 allowed/disallowed JSON whitespace、recursive duplicate keys、source directory/symlink/hardlink/FIFO/socket/missing/read failure、UTF-8 order、06 expected/actual comparison、07 expected pins 以及 accepted transitive distribution、09 inspect separation、每条 R66 command 的 token mutation、missing/duplicate/reorder/tenth/build/container/probe/tag/retry/cleanup/classification drift，以及 Gate A/B/C/Final/terminal-10 self-exclusion。

初始 complete suite 为 `80 passed / 2 failed`；失败仅为 temp socket fixture 路径超过 macOS AF_UNIX limit，以及 alias fixture 未将同一 parsed inventory 传入 evaluator。`repair cycle 1 / 2` 只修复这两个 fixture mechanics；随后 suite `82 passed`。没有改变 probe schema-v1、CLI、product source、Docker topology、`9 / 5 / 5` contract、terminals 01–10、no-retry/no-cleanup 或任何 non-claim。

最终身份冻结：

| Event | UTC |
| --- | --- |
| final test start | `2026-07-31T05:18:13.612006000Z` |
| final test end | `2026-07-31T05:18:28.288767000Z` |

最终执行为 `82 passed in 0.06s`，exit `0`，skipped `0`，xfailed `0`；test 从 exact persisted implementation path 导入。final test 前/后 identities 完全一致：

| Artifact | Final bytes | Final SHA-256 |
| --- | ---: | --- |
| `candidate_evidence_producer.py` | 31188 | `fa51372fc850ea49517226194103f05992a6bc5b654a74e85c04d46e4d91ee42` |
| `test_candidate_evidence_producer.py` | 15464 | `166b4d42c4c3fc82b594498240f371af188421e5bba7c284265cc568bd0ee2cc` |

## 5. R66 static command and gate result

The validator accepts only the frozen commands 1–9, rejects `docker run`/`exec`/`cp` and tag/reference/retry/cleanup tokens, and mechanically calculates: Docker calls `9`; network-capable `5`; daemon-mutating `5`; builds `1`; validation containers `1`; producer invocations/probes `1`; stdout JSON documents `1`; tag/reference `0`; retries `0`; cleanup `0`.

Gate A requires 01/02 before commands 1–4. Gate B requires commands 1–4, 03 and a matching materialization lock before 5. Gate C requires 5–6 and 04/05 before 7. Final requires 7–9 and 06–09 before terminal 10. This is pure/static validation only; no Docker command was executed.

## 6. One-shot execution-lock replacement and audit

Old lock chronology was invalid: `created_at_utc = 2026-07-31T12:05:00Z` was later than the observed actual UTC `2026-07-31T04:57:37Z`. After final test, identity freeze and Git checks PASS, the old lock was rechecked as exact `8092` bytes / `db8692…7d71`, then replaced exactly once in place.

New lock identity:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `execution_lock.json` | 10511 | `22533d1eade03bd9098a04dc0e5d9ac8443871b55d0775ba172efb7f9319e551` |

New lock is regular/non-symlink, strict UTF-8 JSON, schema version `2`, `LOCKED`, closed 18-key top-level object, and has a unique lock ID. Its actual chronology is:

```text
2026-07-31T05:18:13.612006000Z
<= 2026-07-31T05:18:28.288767000Z
<= 2026-07-31T05:18:50.439377Z
<= 2026-07-31T05:20:12.235915Z
```

The sequence is final-test start, final-test end, lock creation and post-lock audit UTC; lock time is not future. Lock records the superseded identity, explicit replacement authority, final artifact identities, exact command records/mechanical budget, test result, repair window `closed: true`, all five closed blockers, and phase non-claims. Producer, test and lock were not modified after the final test/lock audit.

## 7. Final boundary, Git state and MVP alignment

No Docker, network, remote, package install/resolution, application/Collector/API/DB/frontend test, Git stage, commit, push or tag occurred; counters are all `0`. Pre-existing ignored cache directories outside the task artifact path were observed-only and untouched; the exact focused test command used `PYTHONDONTWRITEBYTECODE=1` and disabled pytest cache, and created no task-owned cache/bytecode artifact.

Evidence remains local/static/synthetic only. No synthetic source inventory, distribution record, static command record or unit-test inspect fact is represented as an actual candidate, Docker, runtime or production observation.

MVP 路径一致性：`MVP-ALIGNED`。本修复直接服务于 approved MVP 的一个具体 local `linux/arm64` Collector candidate build/image acceptance 前置：防止 terminal 06/07/09 因 parser boundary、source discovery、expected/actual alias 或 static R66 contract 而产生 false PASS。未引入额外产品能力、threat model、evidence/retention framework 或 runtime topology。

```text
Next gate:
R65-R6-SR3-R1 focused in-place repair package WRITTEN
-> ChatGPT PM durable intake only
```

## 8. Required state

```text
SR3-R1 WRITTEN                   = YES
PRODUCER REPAIRED                = YES
PARSER REPAIRED                  = YES
FIXTURES EXPANDED                = YES
TESTED                           = YES
EXECUTION LOCK REPLACED          = YES
PM ACCEPTED                      = NO
BUILD READY                      = NO
R66 AUTHORIZED                   = NO
BUILT                            = NO
LOCAL IMAGE ACCEPTED             = NO
DEPLOYED                         = NO
RUNTIME-LOADED                   = NO
PRODUCTION-ACCEPTED              = NO
```
