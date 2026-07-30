# Sprint 4 D2-R7B-I1 R53 Focused Verification Oracle Closure Repair Report

## 1. 报告身份、authority 与结论

- 报告名称：Sprint 4 D2-R7B-I1 R53 Focused Verification Oracle Closure Repair Report
- 任务名称：D2-R7B-I1 R53 — Close V-B1–V-B4 Focused Verification Oracle Gaps
- 执行 Thread：Architecture / Integration
- Authority source / ID：`PM-D2-R7B-I1-R53-VERIFICATION-ORACLE-CLOSURE-REPAIR-260730-1534`
- Delivery：`REPOSITORY_DURABLE_REPORT`
- 本 authority：one-shot；首次 task-owned 写入已消费；仅本报告及两个既有 focused test files；不继承 R48–R52 authority。

结论：

```text
PASS / TEST ORACLE REPAIR WRITTEN AND TESTED
```

R52 的 `HOLD` 是 focused package oracle 不足，而非已持久化 product source 被判错。R53 仅补强该 oracle；未修改 product source、config、contract、Storage、PLC、ACK/read_done 或 production behavior。

状态边界：

```text
TEST ORACLE REPAIR WRITTEN = YES
TESTED                     = YES
PM-ACCEPTED                = NOT_ESTABLISHED
VERIFICATION-REVIEWED      = NOT_ESTABLISHED
GIT-CANDIDATE-ACCEPTED     = NOT_ESTABLISHED
STAGED / COMMITTED / PUSHED = NO / NO / NO
BUILT / DEPLOYED           = NO / NO
RUNTIME-LOADED             = NO
PRODUCTION-ACCEPTED        = NO
```

## 2. Initial live recovery 与输入身份

在任何 task-owned 写入前，已依 Prompt 顺序执行完整 Git recovery。结果：

| Field | Live result |
| --- | --- |
| repository root | `/Users/chenjie/Documents/MES/edge-mes-demo` |
| branch | `main` |
| HEAD / origin/main | `4a733d7995a94398ade693822662ebd2b22f9d3d` / same |
| ahead / behind | `0 / 0` |
| cached | empty |
| tracked dirty | `main.py`、`mapping.py`、`event_collector.py`、两个 authorized test files，恰为预期五条 |
| `git diff --check` / cached check | PASS / PASS |
| R53 before write | `ABSENT / NON-SYMLINK / UNTRACKED / UNSTAGED` |

所需输入均为 readable regular non-symlink files，并与冻结值一致。关键受保护/输入身份如下：

| Path | Bytes | SHA-256 | Result |
| --- | ---: | --- | --- |
| `collector/app/main.py` | 2525 | `d1a461294c91f9f86cde4af87b21bb1147bed5561d64028e8462a8f57d46de80` | IDENTICAL |
| `collector/app/services/event_collector.py` | 24313 | `02cab6ea15572ae0b2f6059462f9cd6856cd483ab0dcc37c87d39267aad1e8e2` | IDENTICAL |
| `collector/app/plc/mapping.py` | 18876 | `ba39583a699f8347c0ff5eaec2e7c807dad909c815269de607a36e8b93c023a7` | IDENTICAL |
| `collector/app/services/storage.py` | 38319 | `f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b` | IDENTICAL |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` | IDENTICAL |
| R50 | 34024 | `40cfc45b6fcc756a15f2e550b8d7b051a4d797a6bd8c72da1d6b2fb0aa9941d9` | IDENTICAL |
| R51 | 42262 | `f006a01917b0cdb6deb568e1403cc5bf54d304ee84efc136ec84b2fd4023c7d7` | IDENTICAL |
| R52 | 47886 | `633bf9e619e080d4be0bd99390486243dda8cc8f385f77bf7589dd63623f45f8` | IDENTICAL |

R42、R45、R47、R48、R49、PM Rules、current status 与 PM handoff 亦均按指定顺序读取，保持 regular/non-symlink/readable；未把历史文档快照替代 live facts。

## 3. R52 HOLD 裁定与 test-only boundary

R52 已被 PM 接受为 `HOLD`，当前 blocker 仅为 V-B1–V-B4 的 false-PASS 防护不足：alternate read、raw/semantic identity、正整数/grammar、以及 worker-integrated failure side effect。R50/R51 在各自范围内继续有效。

本轮精确 task-owned changed set：

```text
collector/tests/test_event_collector_reliability.py
tests/test_collector_station_event_runtime_source.py
docs/reports/sprint4_d2_r7b_i1_r53_focused_verification_oracle_closure_repair.md
```

未修改的 pre-existing tracked dirty source paths 是 `collector/app/main.py`、`collector/app/plc/mapping.py`、`collector/app/services/event_collector.py`；它们不属于本轮 changed set。未创建第三个 test/helper/fixture path、manifest、raw log、sidecar、evidence directory 或 A–H artifact。

## 4. V-B1 closure：same-byte loader 与 path negatives

valid loader path 的 oracle 同时 spy `Path.read_bytes()` 与 `Path.read_text()`：

1. 产品 loader 必须 `read_bytes()` 恰好一次；
2. 产品 loader 必须 `read_text()` 零次；
3. YAML loader 的输入必须等于同一 raw bytes 的 UTF-8 decoded text；
4. `mapping_content_sha256` 必须等于 `hashlib.sha256(raw_bytes)`，且 canonical path 仍为该 loader-bound file；
5. expected raw bytes 来自 test fixture，不从 record 或 mapping self-report 复制。

invalid UTF-8、malformed YAML、duplicate YAML key 统一使用 read-byte/read-text spy。三条失败路径均证实 `read_bytes == 1`、`read_text == 0`，因此第二次或 alternate text read 会被发现。新增 final-symlink fixture 和 directory non-regular fixture；两者均在 content read 前 fail closed，并各自断言 `read_bytes == 0`、`read_text == 0`。

## 5. V-B2 closure：独立 raw/semantic expected values

Reliability oracle 直接读取受保护 `config/mapping.yaml` bytes，并独立执行 `hashlib.sha256()`；结果必须同时等于 emitted `mapping_content_sha256` 与冻结 raw value：

```text
d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
```

`resolved_config_hash` 的 expected authority 是独立冻结 semantic value，而非 emitted record 或其 parsed copy：

```text
0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
```

raw/semantic expected values分别建立并显式 `!=`。完整 expected record 由 frozen literals、independent raw SHA、frozen semantic SHA、固定 main context、`os.getpid()` 与 `1 + len(mapping.stations)` 建立，之后才与 parsed record 比较。oracle 另构造 raw/semantic swap 与 zero-digest constant candidates，并断言二者都不能等于 independent expected record 或 emitted record；因此字段互换、常量替代或错误投影不能通过。

## 6. V-B3 closure：PID、count 与 application grammar

`process_pid` 的 oracle 要求 type 为 `int`、not `bool`、`> 0`，并精确等于当前 `os.getpid()`。`read_plan_count` 要求 type 为 `int`、not `bool`、`> 0`，独立等于 `1 + len(mapping.stations)`，且对受保护 mapping 精确等于 `4`；expected 没有从 emitted record 或 post-conversion dict 导出。

application grammar 以固定边界验证：

```text
prefix = "collector_runtime_loaded_json="
application_message starts exactly with prefix
payload = application_message[len(prefix):]
application_message == prefix + payload
JSONDecoder.raw_decode(payload) consumes exactly len(payload)
json.loads(payload) == parsed complete object
payload == deterministic compact serialization of independently expected record
```

没有使用 `application_message.count("=") == 1`；该规则会错误拒绝 JSON string 内合法 `=`，而 fixed-prefix/full-payload comparison 已提供精确且不过宽的 boundary oracle。

## 7. V-B4 closure：worker-integrated failure matrix

新增 test-local helper 在实际 `EventCollectorWorker` constructor path 上执行失败 fixture，显式 spy/observe success logger、`Storage` constructor、Snap7 `Client` constructor、accepted-fact builder、`run_forever` poll surface 与 `threading.Thread` construction。每个失败 path 均要求：constructor raises；zero runtime-loaded success logger emission；zero Storage constructor/mutation；zero Snap7 client construction/PLC I/O；zero accepted-fact builder；zero ACK/read_done；zero Thread 或 poll behavior。

| Failure path | Constructor result | Required counters |
| --- | --- | --- |
| invalid UTF-8 mapping file | `UnicodeDecodeError` | all zero |
| malformed YAML mapping file | `yaml.YAMLError` | all zero |
| duplicate YAML key mapping file | `RuntimeMappingContractError` | all zero |
| valid mapping + tampered runtime snapshot semantic/resolved identity | `ValueError` | all zero |

R49/R50 existing explicit Storage constructor spy and ordered-event oracle remain present and unweakened：success main path 仍为 `record → thread_construct → thread_start → legacy_storage_construct`；该 repair 没有用 FakeStorage state 替代 constructor/order oracle。

## 8. Repair window、validation 与 execution lock

预授权 local repair window 使用 `2 / 2` cycles，均仅修改 authorized test-local imports/helpers/fixtures/spies/assertions：

1. cycle 1：完成 V-B1–V-B4 oracle additions，三条完整 validation PASS；
2. cycle 2：将 malformed YAML 失败 type 收紧为 `yaml.YAMLError`，并加入 explicit Thread constructor zero-call assertion；三条完整 validation PASS。

cycle 2 后 execution lock 已冻结两个 test files；后续只允许写本 R53 report。锁定身份：

| Test file | Bytes | SHA-256 |
| --- | ---: | --- |
| `collector/tests/test_event_collector_reliability.py` | 38392 | `9af7658577ea16344a000e00eb3e346464944eeb15d223f74b7cc690d2f46af3` |
| `tests/test_collector_station_event_runtime_source.py` | 36408 | `5419dcb1e2fb5819e63c9891937cfe96a29becc21bf9be89f7602d0c3aa650d2` |

Exact authorized validation commands and results：

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile \
  collector/app/main.py \
  collector/app/services/event_collector.py \
  collector/app/plc/mapping.py \
  collector/tests/test_event_collector_reliability.py \
  tests/test_collector_station_event_runtime_source.py
```

Result：PASS, exit code 0。

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -m pytest \
  collector/tests/test_event_collector_reliability.py \
  -q
```

Result：PASS, `25 passed, 11 subtests passed in 0.23s`。

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=collector:. \
.venv/bin/python -m pytest \
  tests/test_collector_station_event_runtime_source.py \
  -q
```

Result：PASS, `59 passed in 0.14s`。两个 pytest command 均分别完整运行；未使用 `-k`、skip、xfail、reduced selection、broad suite、coverage 或 application startup。

## 9. Protected-path、Git 与 untracked audit

execution lock 后再次核验所有 protected source/config/R48–R52 identities，结果均为 `IDENTICAL`；cached 仍 empty，`git diff --check` 与 `git diff --cached --check` 均 PASS。没有 post-lock test-file mutation。

R53 写入前，raw NUL untracked observation 与 repository-relative UTF-8 stable-sort normalized observation 的结果为：

| Metric | Value |
| --- | ---: |
| raw count / normalized unique count | 314 / 314 |
| duplicates | 0 |
| Batch D / Batch E / R40–R52 | 300 / 1 / 13 |
| unknown / missing | 0 / 0 |
| raw NUL digest | `11c773aee4a5c357ec5b8c014d042dbea5ec69d809309557c613f8cc9d2f447a` |
| normalized path-list digest | `3e052e589ef295a3cb77dbe1ea93003194207c1c36fbf72a289c1047e7fb9447` |

R36 `authority_materialization_plan.json` 仅用于 membership classification；Batch D/E content 未打开、删除、移动、stage 或 reclassify。写入本 R53 后的 expected composition 是 Batch D 300 + Batch E 1 + R40–R53 14 = 315，且 unknown/missing 必须为 0；post-write detached audit 负责确认。

## 10. Forbidden actions、blockers、recommendations 与产品边界

| Forbidden-action category | Count |
| --- | ---: |
| product source/config/contract/status/roadmap/handoff modification | 0 |
| Git add/stage/commit/push/tag/reset/restore/checkout/stash/clean | 0 |
| build/package/dependency installation | 0 |
| Docker/Compose/lifecycle | 0 |
| network/SSH/curl/remote | 0 |
| real DB/PLC/API/accepted-fact/ACK/read_done action | 0 |
| application startup/runtime validation/A–H evidence | 0 |
| Batch D/E content operation | 0 |

Blockers：none for this exact test-only repair, contingent on the final detached audit preserving the stated allowlist and untracked composition。

Recommendations：

1. strict RFC3339 hand-built negative fixture：non-blocking Verification carry-forward；not required for R53。
2. direct missing-line-plan 与 station-runtime one-to-one fixture：non-blocking future same-path recommendation；not required for R53。
3. DQ-B2 source/image/config/process binding 与 DQ-B3 A–H evidence：later independent runtime gate，not current implementation repair。

产品/evidence boundary 保持：

```text
ACTIVATED                  = YES
STATIC_MAPPING_INITIALIZED = YES
RUNTIME-LOADED             = NO
PRODUCTION-ACCEPTED        = NO
```

Local mocks、spies 和 focused tests 仅证明 local test oracle；不证明 source defect 曾存在或已修复、accepted implementation commit/image、deployed active process、real DB/PLC、runtime A–H evidence、`RUNTIME-LOADED` 或 production truth。

## 11. MVP、Thread context、next gate 与 stop point

MVP 路径一致性：`MVP-ALIGNED`。R53 仅关闭 R52 所列四类可验证 false-PASS 风险；没有新增 API、DB schema/migration、telemetry、audit/forensics、retention、runtime topology 或 production capability。

Thread 输出 / 上下文评估：本 durable report 完成后当前 Architecture / Integration authority terminalized；当前 Thread 是否建议继续：`no`；是否需要新开 Thread：`yes`。理由：R53 不能继承为 independent Verification review、Git 或任何后续 phase authority。

唯一 next gate：

```text
R53 focused Verification-oracle repair WRITTEN
→ ChatGPT PM durable intake
→ only if PM accepts R53 with no blocker: fresh independent Verification implementation re-review
```

不得由 R53 自动推断 `VERIFICATION-REVIEWED`、Git candidate、stage、commit、push、build、Docker、remote、runtime validation、`RUNTIME-LOADED` 或 `PRODUCTION-ACCEPTED` authority。完成本报告和 final detached read-only audit 后立即停止。

本报告自身 final bytes/SHA-256 由 post-write detached audit 返回 Chat manifest，不在本文件内自引用。
