# Sprint 4 D2-R7B-I1 R65-R6-SR3 Candidate Evidence Producer / Parser Implementation, Static Fixture Testing, and Execution-Lock Materialization Report

## 1. 结论与状态

- 任务：`D2-R7B-I1 R65-R6-SR3 — Independent Candidate Evidence Producer and Strict Parser Implementation, Unit/Static Fixture Testing, and Execution-Lock Materialization`
- 执行 Thread：`Architecture / Integration`
- 一次性 authority：`PM-D2-R7B-I1-R65-R6-SR3-PRODUCER-PARSER-IMPLEMENTATION-STATIC-FIXTURE-EXECUTION-LOCK-260731-1205`
- Delivery：`REPOSITORY_REPORT_WITH_ARTIFACTS`
- 结论：`PASS`

本结论仅建立以下本地状态：

```text
WRITTEN                         = YES
IMPLEMENTED                     = YES
TESTED                          = YES
EXECUTION LOCKED                = YES
PM ACCEPTED                     = NO
BUILD READY                     = NO
R66 AUTHORIZED                  = NO
BUILT                           = NO
LOCAL IMAGE ACCEPTED            = NO
DEPLOYED                        = NO
RUNTIME-LOADED                  = NO
PRODUCTION-ACCEPTED             = NO
```

所有证据是 local/static/synthetic fixture evidence。没有 candidate filesystem、candidate distribution、container inspect、Docker、network、remote、runtime 或 production observation。

## 2. Fresh baseline、membership 与输入身份

首次 task-owned write 前，fresh recovery 确认 repository 为
`/Users/chenjie/Documents/MES/edge-mes-demo`，branch 为 `main`，且：

```text
HEAD = origin/main = 0e7544a12b00799780d76723ca0de781bc2e8ad7
ahead / behind = 0 / 0
tracked diff = empty
cached diff = empty
git diff --check = PASS
git diff --cached --check = PASS
934ced7b9659cb566628b1709cf6d73463a534d8 is an ancestor of HEAD = PASS
```

受限 Batch membership extraction 仅使用授权的 `.batches[] | select(.batch_id == "D"|"E") | .exact_paths[]` expressions；Batch D/E 内容未读取。其计数为 `300 / 1`。以 repository-relative path、UTF-8 bytewise sort 且 dedup 前 duplicate check 比对，写入前 membership 为：

```text
raw / unique / duplicate / unknown / missing = 324 / 324 / 0 / 0 / 0
```

当前 handoff、SR1、SR2-R1、Reliability、initial Data Quality HOLD、SR2-R4、SR2-R5、SR2-R6 均为 regular、non-symlink、strict UTF-8、untracked、unstaged、uncommitted，且身份完全匹配：

| Input | bytes | SHA-256 |
| --- | ---: | --- |
| handoff | 22534 | `b90b0bc14e14e33df869a46b9d7b99cbcd4878da2281a751409389545d7e0383` |
| SR1 | 23402 | `e2108e4e870e6681d2594e5832113b7032355e2274effc82d7acea2c3172872d` |
| SR2-R1 | 15975 | `aec7cefe779e39abeeac7db747b91f8a236ce6ea544f875164520398cebb66cf` |
| Reliability | 13032 | `87cb8d69a429278f1b1c9ec81243a7e7c61dccafdecc00e63fc74f416d740601` |
| initial Data Quality HOLD | 26581 | `b7a991c45c369827669967542f9e1a70d6f09f7d92413702b3bfc04ad28e7449` |
| SR2-R4 | 17288 | `c0ee5bb04c989954e80e089816b72287f60c5b18671077bc4e883eb933b8d31a` |
| SR2-R5 | 17002 | `b715c8678a8af1eacc0b6281ab78df231f604a63cd6b25fbeb5d2f1a7b54b3d4` |
| SR2-R6 | 27983 | `9c4b74a49e86d6f989e845f5afd6255b250f77b7313bc33f4a3ac3d255192426` |

四个 output paths 在首次写入前均为 `ABSENT / NON-SYMLINK / NOT INDEXED`。

## 3. 实现边界

唯一 implementation file 同时承载唯一 producer、strict parser、schema-v1 validator、source/distribution/mapping/import/action validators、06/07/09 eligibility、terminal-10 pure closure validator、static R66 token contract，以及 exclusive/no-follow JSON publication helper。没有第二 producer、parser、helper source、schema registry、terminal 11、raw/normalized sidecar 或第二 manifest。

冻结 CLI 只接受：`--attempt-id`、`--candidate-full-id`、`--producer-sha256`、`--mapping-sha256`。future container path 为 `/opt/edge-mes-probe/candidate_evidence_producer.py`；token representation 使用 candidate `python -B`，仅一个 invocation、一个 stdout JSON document，diagnostics 仅 stderr，且 `import app.main` 不调用 guarded production `main()`。

Parser 严格拒绝 BOM、invalid UTF-8、non-object root、NDJSON/second document、prefix/suffix、truncated bytes 和递归 duplicate keys。它在 materialization/defaulting 前只 parse 一次，并将同一 immutable logical object 交给 06/07/09。schema-v1 强制 exact 14-key closed root、closed nested records、ordinary/OCI digest grammar、RFC3339 UTC `Z` timestamps、integer-not-boolean、`PASS == probe_exit 0` truth relation、exact ten zero-only action keys，以及独立 attempt/candidate/producer/mapping binding。

source policy仅允许 `/app/requirements.txt`、`/app/app/**`、`/app/common/**` 的 regular non-link/non-hardlink files；package path 是 `/app/common/station_event/__init__.py`。distribution policy 使用 PEP-compatible canonical name（`psycopg[binary] -> psycopg`）、duplicate-before-dedup、canonical/raw/version ordering，并将四个 pins 与 complete candidate inventory 比较；unexpected complete transitive distributions 不自动失败。

`R66_COMMANDS` 只冻结而未执行 commands 1–9 token arrays。static validator 强制 `9 / 5 / 5` budget、一 build、一 validation container、一 producer invocation/probe、一个 stdout JSON document、zero tag/reference/retry/cleanup，且拒绝 `docker run`、`docker exec`、`docker cp`、second container/producer/probe 和第十次 Docker call。

## 4. Focused static fixtures 与测试

唯一允许的完整测试命令实际执行为：

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m pytest -p no:cacheprovider docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/test_candidate_evidence_producer.py -q
```

最后完整运行结果为 `49 passed in 0.04s`，exit status `0`。测试通过 exact repository implementation path import，没有测试内替代 producer/parser。

覆盖家族包括：strict UTF-8/BOM/one-root/framing；root 与 nested duplicate keys；schema/root cardinality、null/missing/unknown/type/digest/timestamp/default rejection；source scope/order/duplicate/type-mode-bytes-hash fixtures；PEP canonicalization、ordering、conflict、pins 与 accepted unexpected transitive distribution；mapping/import/exact ten action keys；PASS/HOLD status and binding suppression；parse-once/same-object 06/07/09 consumption；R66 commands 1–9 shape/budget；01–09 terminal-10 self-excluding closure；synthetic temporary-directory exclusive no-overwrite/no-follow publication。

初始 TDD red run 因 exact implementation path 尚不存在而按预期 collection failure；首次 complete suite 为 `46 passed / 3 failed`，错误仅为 synthetic distribution fixture ordering（`python-snap7` 在 `PyYAML` 前）。授权 repair window 使用 `1 / 2` cycle 修正该 test fixture；未改变 authority、schema、topology、budget、PASS/HOLD standard 或 non-claims。随后全量运行和最终全量运行均 PASS。

最终测试前/后 implementation 与 test identity 完全相同：

| Artifact | bytes | SHA-256 |
| --- | ---: | --- |
| `candidate_evidence_producer.py` | 21139 | `91250d8d65abaa1bdf6ef843cf394cc7ef0614c7df2013b4737e035137be3708` |
| `test_candidate_evidence_producer.py` | 10560 | `88bdcdb7d9382993978bfe629c2da9182950a9fca44a633b77a85ca752f5d606` |

`PYTHONDONTWRITEBYTECODE=1` 与 `-p no:cacheprovider` 生效；没有 `.pytest_cache`、`__pycache__` 或 `.pyc` repository artifact。

## 5. Execution lock 与锁后审计

所有 required tests、post-test identity 与 pre-lock Git checks PASS 后，execution lock 以新的 exact absent path materialized。它为 regular、non-symlink、strict UTF-8、no BOM、closed 16-key JSON object，并记录 authority inputs、source/test host and repository paths、pre/post equality、parser policy、frozen CLI、future R66 tokens/budget、actual test result、repair window、forbidden-action counters、Git audit 与 non-claims。

| Artifact | bytes | SHA-256 | role |
| --- | ---: | --- | --- |
| `docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/execution_lock.json` | 8092 | `db8692c39bc4425465c4f8d83ad755a6dd8c93dc65c5e7cb059da707a32b7d71` | immutable local execution lock |

lock JSON parse, closed-key audit, UTF-8 audit, lock identity audit and post-lock source/test identity audit PASS。execution lock 创建后未修改 producer、test 或 lock，也未重新开启 repair window。

## 6. 最终 allowlist、Git 与非授权行动

本任务仅创建下列四个 exact paths：

```text
docs/reports/sprint4_d2_r7b_i1_r65_r6_sr3_candidate_evidence_producer_parser_implementation_static_fixture_testing_execution_lock.md
docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/candidate_evidence_producer.py
docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/test_candidate_evidence_producer.py
docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/execution_lock.json
```

最终 expected untracked membership 为 `328 raw / 328 unique / 0 duplicate / 0 unknown / 0 missing`（324 baseline + four exact outputs）。tracked diff、cached diff、staged set 均为空；所有新增文件仍为 `untracked / unstaged / uncommitted / unpushed`。

forbidden-action counters：Docker `0`；network `0`；remote `0`；package install/resolution `0`；application/Collector/API/DB/frontend test `0`；Git stage/commit/push/tag `0/0/0/0`。task-owned final process count `0`。没有读写 Batch D/E content，没有修改 product source、Dockerfile、requirements、mapping、status、roadmap、PM Rules、handoff或任何 existing report。

## 7. MVP 路径一致性与下一 Gate

`MVP-ALIGNED`。本任务直接服务于已批准 MVP deliverable：一个具体 local `linux/arm64` Collector candidate build/image acceptance 的候选证据前置。minimum invariant 是 terminals 06/07/09 只能消费 mechanically candidate-bound、strictly parsed、fail-closed candidate evidence，并且不能把 synthetic/local evidence 升格为 runtime 或 production truth。

没有引入额外产品能力、threat model、evidence framework、retention platform、runtime topology、SBOM、mirror、hash lock、reproducibility、remote/deployment/activation能力。实现与 fixtures 的规模仍是冻结单一 producer/parser 与有限 static contract 所必需，classification 为 `MVP-ALIGNED`。

唯一 next gate：

```text
R65-R6-SR3 implementation/test/execution-lock package WRITTEN
-> ChatGPT PM durable intake only
```

本报告不发布 Reliability、Data Quality、Verification、R66、Docker、Git、remote、deployment、activation、runtime 或 production Prompt，也不授予其中任一 authority。
