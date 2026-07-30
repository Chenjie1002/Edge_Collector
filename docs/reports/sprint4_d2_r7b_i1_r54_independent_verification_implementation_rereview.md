# Sprint 4 D2-R7B-I1 R54 Independent Verification Implementation Re-review

## 1. 报告身份、authority 与结论

- 报告名称：Sprint 4 D2-R7B-I1 R54 Independent Verification Implementation Re-review
- 任务名称：D2-R7B-I1 R54 — Independently Re-review Runtime-Loaded Observability After R53
- 执行 Thread：Verification
- Authority source / ID：`PM-D2-R7B-I1-R54-INDEPENDENT-VERIFICATION-IMPLEMENTATION-REREVIEW-260730-1607`
- Report delivery mode：`REPOSITORY_DURABLE_REPORT`
- 本 task-owned write：仅本报告；首次写入时 authority 已消费。

结论：

```text
PASS WITH RECOMMENDATIONS
```

R52 的四项历史 Verification blocker 已由当前持久化 source 与 R53 的两个 focused test 文件独立复核为 closed：`V-B1`、`V-B2`、`V-B3`、`V-B4` 均没有可信 current false-PASS gap。R47 terminal matrix、R49 Storage constructor/order oracle 和 anti-tautology 审查均为 PASS。不存在当前 Verification blocker。

本裁定只表示本地 checkout 中的 source/test package 已 `VERIFICATION-REVIEWED = YES`，并且可进入**单独的 PM final implementation-package acceptance / Git-candidate review 决策**；它不是该 PM acceptance，也不表示 Git candidate 已被接受、stage、commit、push、build、deploy、runtime validation、`RUNTIME-LOADED` 或 `PRODUCTION-ACCEPTED`。

## 2. Scope、non-inheritance 与状态边界

本轮为 one-shot、review-only Verification authority。读取规定合同链、当前 source/config/tests 和 R36 materialization JSON；运行仅 Prompt 列出的 py_compile 与两条分别完整的 pytest command；唯一写入本报告。未修改 source、tests、config、contract、status、roadmap、handoff 或 R48–R53 reports；未创建 artifact、helper、fixture、manifest、raw log、sidecar 或 evidence directory。

合同解释遵循：PM Rules → current handoff → R42 → R45 → R43 → R46 → R47 → R48 → R49 → R50 → R51 → R52 historical HOLD → R53 repair candidate → persisted source/tests。R52 是 blocker 起点；R53 的 `WRITTEN / TESTED` 不替代本独立验收。

```text
SOURCE / TEST WRITTEN       = YES (R48/R49 implementation; R53 test-only repair)
TESTED                      = YES (fresh local commands below)
PM-ACCEPTED                 = R48/R49/R50/R51/R52/R53 as historically stated; R54 itself NOT YET
RELIABILITY-REVIEWED        = YES (R50 historical accepted result)
DATA-QUALITY-REVIEWED       = YES (R51 historical accepted result)
VERIFICATION-REVIEWED       = YES (this R54 result only)
GIT-CANDIDATE-ACCEPTED      = NO / PM decision required
STAGED / COMMITTED / PUSHED = NO / NO / NO
BUILT / DEPLOYED            = NO / NO
ACTIVATED                   = YES
STATIC_MAPPING_INITIALIZED  = YES
RUNTIME-LOADED              = NO
PRODUCTION-ACCEPTED         = NO
```

## 3. Initial live Git recovery and input identities

Before the first R54 write, every required input was regular, non-symlink and readable; the R54 path was absent and non-symlink. Fresh Git facts were:

| Field | Observed value |
| --- | --- |
| repository root | `/Users/chenjie/Documents/MES/edge-mes-demo` |
| branch | `main` |
| HEAD / origin/main | `4a733d7995a94398ade693822662ebd2b22f9d3d` / same |
| ahead / behind | `0 / 0` |
| cached | empty |
| tracked dirty | exactly `collector/app/main.py`, `collector/app/plc/mapping.py`, `collector/app/services/event_collector.py`, and the two authorized test files |
| `git diff --check` / cached check | PASS / PASS |

The prescribed documents were read in the required order. Current identities at recovery (all regular/non-symlink/readable) were:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| PM Rules | 49170 | `a692fdafbdea8c63d184cb11548e73731aefccd3110818004b028ba7ee9fe7f5` |
| current status | 150180 | `ee7126fd20f1774f54cee9b238cab4e3e0943bce854402b1594060212f88cc23` |
| PM handoff 260730-1203 | 26183 | `c9a7ed7283d4574578e1608fc6891bdb91373d97bac3191740863917af3ad8e1` |
| R42 / R45 / R43 / R46 / R47 | 32319 / 13786 / 30244 / 23703 / 34592 | `dba08acb675c08561e24c97fb543507d02c387eb82efc7ee253a833528b59165` / `8fd646f24565bbcb27aa9063038774fee3b5398d66566f961bee296ffff02ef2` / `95b2e63c4879fb5af6920b262300566c577612dd1753b13bf59928c1417338e8` / `f460fef43d975de41ed624fa49d8a1a8dcd5246b4ae55b222189f40703914b81` / `4de247e350eb595077219856cf63b0319ee83d14026b6beaaf7c5d83211a0ae4` |
| R48 / R49 | 15692 / 11749 | `caa3203630c5b321c950d078fda7424f4f1ca8edcd7f4a45b88525adfdda0d10` / `5d09732094f3266eccc34a002b0203a3889f33be1c6b56568c43b42c50618dde` |
| R50 / R51 / R52 / R53 | 34024 / 42262 / 47886 / 13871 | `40cfc45b6fcc756a15f2e550b8d7b051a4d797a6bd8c72da1d6b2fb0aa9941d9` / `f006a01917b0cdb6deb568e1403cc5bf54d304ee84efc136ec84b2fd4023c7d7` / `633bf9e619e080d4be0bd99390486243dda8cc8f385f77bf7589dd63623f45f8` / `10f6a8b5d95c52e493835dcd2e250ec14fc5b22b58791576cd94f4f62730b03e` |

| Persisted product/test input | Bytes | SHA-256 | Frozen match |
| --- | ---: | --- | --- |
| `collector/app/main.py` | 2525 | `d1a461294c91f9f86cde4af87b21bb1147bed5561d64028e8462a8f57d46de80` | YES |
| `collector/app/services/event_collector.py` | 24313 | `02cab6ea15572ae0b2f6059462f9cd6856cd483ab0dcc37c87d39267aad1e8e2` | YES |
| `collector/app/plc/mapping.py` | 18876 | `ba39583a699f8347c0ff5eaec2e7c807dad909c815269de607a36e8b93c023a7` | YES |
| `collector/app/services/storage.py` | 38319 | `f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b` | YES |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` | YES |
| `collector/tests/test_event_collector_reliability.py` | 38392 | `9af7658577ea16344a000e00eb3e346464944eeb15d223f74b7cc690d2f46af3` | YES |
| `tests/test_collector_station_event_runtime_source.py` | 36408 | `5419dcb1e2fb5819e63c9891937cfe96a29becc21bf9be89f7602d0c3aa650d2` | YES |

Frozen independent values were independently reconfirmed: mapping raw SHA `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`; resolved semantic hash `0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38`; canonical line `LINE_001`; read-plan count `4`.

## 4. R53 exact changed-path review

R53 declares the exact task-owned changed set as the two focused test files and its own report. Current Git diff contains the five expected dirty implementation/test paths; the three product files are the protected pre-existing R48/R49 implementation surface, while R53’s candidate test changes are confined to the two authorized tests. R53’s report is untracked and its frozen bytes match. All protected product/config and R50–R53 identities above match frozen values; no third test, helper, fixture or product path is present. Conclusion: the R53 repair candidate respected its stated test-only scope.

## 5. V-B1 — same-byte loader and negative-path oracle

`load_edge_mapping()` rejects a final symlink before resolution, resolves the supplied path, rejects a non-regular target, then performs exactly one `Path.read_bytes()`, hashes those bytes, UTF-8 decodes those same bytes, and passes that decoded string to `yaml.load()`.

The valid-loader test patches both `Path.read_bytes` and `Path.read_text`, asserts raw read `== 1`, alternate text read `== 0`, asserts the YAML call received `raw_bytes.decode("utf-8")`, and independently hashes fixture bytes. Any future `read_text()` on the product path, including a second/alternate read, increments the patched target and fails the test. The failure parameterization repeats the exact `1 / 0` observation for invalid UTF-8, malformed YAML, and duplicate-key YAML.

The symlink and directory fixtures invoke the product loader, require its explicit contract exception, and observe `0` raw reads and `0` text reads. This is content-read-before-rejection protection, not a fixture-only predicate. `V-B1 = CLOSED`.

## 6. V-B2 — independent raw and semantic authority

Before parsing the emitted message, `independent_expected_runtime_record()` reads protected `config/mapping.yaml` bytes and computes `hashlib.sha256(raw_bytes)` itself; it separately requires that value to equal the frozen raw constant. The semantic expected value is the distinct frozen external constant, not copied from the record or a parsed record-derived snapshot. The full expected record is built before the logger message is decoded.

The test then requires parsed record equality to that full independent record and equality of the payload to deterministic compact serialization of it. Swapped raw/semantic candidates and zero-digest candidates are specifically unequal to both independent expected and emitted record. Thus raw/semantic exchange, a constant digest, or wrong field projection fails; serializer equality is a serialization/grammar check, not the authority source for values. `V-B2 = CLOSED`.

## 7. V-B3 — PID, count and complete application grammar

The record test independently requires `process_pid` to be `int`, not `bool`, positive and exactly `os.getpid()`. It independently requires `read_plan_count` to be `int`, not `bool`, positive, `1 + len(mapping.stations)`, and exactly `4`; neither expected is derived from the record or a post-conversion plans dictionary.

Its parser boundary is fixed-prefix plus full payload: it slices only after `collector_runtime_loaded_json=`, invokes `JSONDecoder.raw_decode(payload)`, requires `end == len(payload)`, and compares the full payload to deterministic compact serialization of the independently built expected record. This rejects trailing data. It does not impose `count("=") == 1`; JSON strings containing a legal `=` therefore remain valid. `V-B3 = CLOSED`.

## 8. V-B4 — worker-integrated failure and no-side-effect matrix

The R53 helper constructs the real `EventCollectorWorker`, rather than testing a copied loader or only a fake state. It patches the product lookup points for `Storage`, `snap7.client.Client`, accepted-fact builder, logger, `EventCollectorWorker.run_forever`, and `threading.Thread`; it records constructor calls before the exception is asserted and reads every counter afterward.

| Failure injected through real worker constructor | Required observed result | Verdict |
| --- | --- | --- |
| invalid UTF-8 file | `UnicodeDecodeError`; no success record; Storage/Snap7/accepted fact/Thread/run_forever all zero | PASS |
| malformed YAML file | `yaml.YAMLError`; same zero counters | PASS |
| duplicate YAML key file | `RuntimeMappingContractError`; same zero counters | PASS |
| valid mapping with tampered runtime snapshot semantic hash | `ValueError`; same zero counters | PASS |

The helper is not an early-return false PASS: `construct_worker()` initializes the spies first, uses actual loader only when `mapping=None`, then invokes `EventCollectorWorker`; the assertions inspect logger calls, constructor-call lists and mock call counts after the expected exception. `Storage` is not constructed, so its events—and therefore DB mutation/ACK/read_done effects—are empty; the direct client constructor spy is also zero, excluding PLC I/O. The test does not rely solely on FakeStorage state. `V-B4 = CLOSED`.

## 9. R49 preservation and complete R47 terminal matrix

R49’s existing assertions remain present and strong: successful main ordering is `record → thread_construct → thread_start → legacy_storage_construct`; worker-constructor failure prevents both Thread start and legacy Storage construction; `run_forever()` has exactly one Storage construction before first poll; Storage initialization failure propagates without retry or re-emission. Source confirms `Storage(self.dsn)` is at `run_forever()` entry and the actual `psycopg.connect` boundary remains in `Storage.__init__()`.

| R47 current terminal invariant | Independent current result |
| --- | --- |
| mandatory main context, current PID, single-use, failure-consumed | PASS: main captures it before config; `consume()` marks consumed before validation; tests cover missing/foreign/reuse/later failure |
| same-byte loader | PASS: one raw read/hash/decode/parse path plus V-B1 spies/negatives |
| raw/semantic identity separation | PASS: raw bytes SHA versus resolved hash, independent V-B2 authorities |
| canonical line and list-first plan | PASS: routing/canonical equality before record; list scopes validated before dict conversion/materialization |
| exact 11-key deterministic record | PASS: exact key set, compact sorted JSON, no CR/LF, full-payload test |
| constructor-last-action | PASS: record follows loaded identity, PLC object construction, plan validation and station runtime materialization; no subsequent required constructor action |
| Thread/Storage order | PASS: record precedes Thread; legacy Storage follows Thread; worker Storage begins only at run entry |
| no pre-record DB/PLC/accepted-fact/ACK/read_done side effect | PASS: V-B4 counters plus retained R49 order and constructor tests |

No credible positive, negative, failure or side-effect oracle gap remains in that matrix.

## 10. Anti-tautology, regression detection and over-constraint assessment

| Check | Result |
| --- | --- |
| raw expected hash comes from protected bytes, not record | PASS |
| semantic expected is a frozen distinct value, not runtime self-output | PASS |
| expected PID/count come from `os.getpid()` and mapping cardinality | PASS |
| expected message is built before parsing record and serialized independently | PASS |
| frozen constants bind protected mapping identity | PASS |
| trivial swap/constant assertions supplement, not replace, full record equality | PASS |

R53 regression mapping is reliable: an alternate/second text read fails V-B1; raw/semantic swap, constant digest or wrong field projection fails V-B2; bool/wrong PID/count, prefix deviation or trailing payload fails V-B3; loader/identity failure that reaches logger, Storage, Snap7, accepted-fact, thread or polling surface fails V-B4. The tests do not over-constrain a lawful implementation: they require contract-visible byte, record and order semantics, not a particular YAML parser internals, JSON-internal `=` count, real database/PLC, image or process identity.

Strict hand-built RFC3339 negative fixture remains a bounded non-blocking carry-forward: current context parsing and suffix/UTC checks exist, and no specific current false PASS was found. The direct missing-line-plan/station-runtime one-to-one fixture remains a bounded recommendation: existing missing/extra/duplicate/multiset/cardinality checks plus materialized-count guard prevent the credible scope false PASS. DQ-B2 source/image/config/process binding and DQ-B3 A–H evidence remain later independently authorized runtime evidence work, not missing artifacts here.

## 11. Validation, post-validation integrity and Git audit

Executed exactly as authorized, with no `-k`, skip, xfail, reduced selection, broad suite, coverage or application startup:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile \
  collector/app/main.py \
  collector/app/services/event_collector.py \
  collector/app/plc/mapping.py \
  collector/tests/test_event_collector_reliability.py \
  tests/test_collector_station_event_runtime_source.py
```

Result: PASS, exit 0.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=collector:. \
.venv/bin/python -m pytest collector/tests/test_event_collector_reliability.py -q
```

Result: PASS, `25 passed, 11 subtests passed in 0.24s`.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=collector:. \
.venv/bin/python -m pytest tests/test_collector_station_event_runtime_source.py -q
```

Result: PASS, `59 passed in 0.14s`.

After validation and before this write, all seven product/test identities and R50–R53 protected identities in Section 3 matched again; cached remained empty; both diff checks remained PASS; the five-path tracked dirty set was unchanged. This confirms no post-validation source/test mutation.

Raw NUL untracked inspection and deterministic repository-relative UTF-8 stable sort before R54 write found raw `315`, normalized unique `315`, duplicates `0`, raw and normalized SHA-256 `f70585c5ef516987d005db3548129bbfa5ede7e0eadad112610497a8b9c62a02`. Membership using only R36 materialization JSON: Batch D `300`, Batch E `1`, R40–R53 `14`, unknown `0`, missing `0`. After this report, expected is Batch D `300` + Batch E `1` + R40–R54 `15` = `316` with unknown/missing `0`.

## 12. Findings, forbidden-action audit, next gate and context

| Finding | Classification |
| --- | --- |
| V-B1 through V-B4 | closed |
| R49 constructor/order and R47 matrix | closed / PASS |
| strict RFC3339 fixture; direct line-plan/station-runtime fixture | bounded carry-forward, non-blocking |
| DQ-B2/DQ-B3 source/image/config/process and A–H evidence | future runtime evidence task |
| new image/container/Git/telemetry/record fields or future artifact naming | unnecessary / scope expansion |

Forbidden-action counters: source/test/config/contract/status/roadmap/handoff modification `0`; Git stage/commit/push/tag/reset/restore/checkout/stash/clean `0`; build/package/dependency install `0`; Docker/Compose/lifecycle `0`; network/SSH/curl/remote `0`; real DB/PLC/API/accepted-fact/ACK/read_done `0`; application startup/runtime validation `0`; Batch D/E content operation `0`.

Blockers: none.

Recommendations: retain only the two bounded carry-forwards stated above; they do not require repair before PM intake.

MVP 路径一致性：`MVP-ALIGNED WITH BOUNDED BACKLOG ITEMS`。本轮验证现有 minimal runtime-loaded observability implementation 的 local false-PASS resistance；未增加产品能力、证据系统、威胁模型、DB/PLC/API 或 runtime topology。

Thread 输出 / 上下文评估：长；当前 Verification Thread 不建议继续；下一轮需要新的 PM-owned intake/authority，因为本 authority 已在写入本报告时消费，且后续 PM acceptance/Git-candidate decision 不可继承。

Exact next gate and stop point:

```text
R54 independent Verification implementation re-review WRITTEN
→ ChatGPT PM durable intake
→ only if PM accepts R54 with no blocker: PM final implementation-package acceptance
→ PM may separately decide whether to open exact-path Git-candidate review
```

No stage, commit, push, build, Docker, remote, runtime validation, `RUNTIME-LOADED` or `PRODUCTION-ACCEPTED` authority follows from this report. Stop after the required detached post-write audit.

The final bytes/SHA-256 of this report are intentionally returned only by the post-write detached audit and are not self-referenced here.
