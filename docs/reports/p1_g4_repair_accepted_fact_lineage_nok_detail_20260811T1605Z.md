# P1-G4 bounded product repair report — accepted-fact lineage and NOK detail

## 1. 终端结论

`HOLD / API_BYTECODE_CACHE_AUDIT_FAILED`

F1 historical config lineage 与 F2 NOK detail 的 TDD repair 已完成，focused/regression tests、in-memory compile、route registration、source/fallback/lineage 静态检查与 diff check 均通过。最终一次性 audit 在 API bytecode/cache absence 断言处失败，未继续执行其后的 status recheck；按 task terminal policy 未重试、未清理、未继续其他 gate。

最早终端边界：本地 final validation 的 `API_BYTECODE_CACHE=ABSENT` 检查，而非 F1/F2 产品行为。

## 2. Task self-identity 与 authority

```text
TASK_PATH = docs/thread_handoff/pm_task_20260811T1605Z_p1_g4_repair_accepted_fact_lineage_nok_detail.md
TASK_NAME = P1_G4_REPAIR_ACCEPTED_FACT_LINEAGE_NOK_DETAIL_20260811T1605Z
TASK_ROLE = Shadow bounded product repair worker
TASK_CLASS = PRODUCT_REPAIR_GATE_1_OF_3
FAILURE_FAMILY = G4_ACCEPTED_FACT_LINEAGE_AND_NOK_DETAIL_SUFFICIENCY
GOAL_ID = P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1
CURRENT_GATE = P1-G4-R_FOCUSED_RELIABILITY
PRODUCT_REPAIR_GATES_USED = 1/3
```

Task 文件先于其他仓库读取核验：regular non-symlink，`bytes=11473`，`SHA-256=160754b047259ad0e37086ac20b0fc46f6e5a3f17c7c7fbebb4a569f2edcfc11`；文件内 self-identity 五项匹配，`TASK_SELF_IDENTITY=PASS`。

本 task 允许 authority identities：

| artifact | bytes | SHA-256 |
| --- | ---: | --- |
| `docs/thread_handoff/pm_operating_rules.md` | 69697 | `45d4be226d2c4754fb2b21b55fce6f4086cb24e643b170f1ad1ab475a596bf9f` |
| `docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_charter.md` | 20025 | `cfc05c53ef03f890cf5be2228f47369c2042457294384b82db9bd85b8c348dd3` |
| `docs/contracts/production_process_kpi_contract.md` | 28427 | `776e744314f9ec33884765c20f8d88dab45afeda74354cf7e10e7fc226809252` |
| `docs/reports/p1_g4_i_bounded_production_metrics_api_20260811T1525Z.md` | 14056 | `32d041fc243041be87ee7d43339237e7fa7a5aa53c0be904ed35a0afedab0482` |
| `docs/reports/p1_g4_r_focused_reliability_review_20260811T1555Z.md` | 12543 | `11c85624f2ef2d4943434b19bbbeaa5cdbc333fdc7f9eb73a796c0f0936a5c6e` |

## 3. Candidate identity binding

Entry identities matched task Section 4 before any candidate write：

| path | entry bytes | entry SHA-256 |
| --- | ---: | --- |
| `api/app/routes/process_metrics.py` | 19270 | `94fae79a51646d5e360d3654db31190fdfd0abb7a76f2de5d02b4446a817e7f9` |
| `api/tests/test_process_metrics_api.py` | 21011 | `60f0c6b0c40d5d39f7020a94bd4ec00a5f28015d70e0069fdd0c3bb9e3bda083` |
| `api/app/main.py` | 524 | `038f7ea2c900f8288742586fe38430f6f5e0ce352fd1e4d7117d0e467f811dad` |

Final candidate identities before report write：

| path | final bytes | final SHA-256 |
| --- | ---: | --- |
| `api/app/routes/process_metrics.py` | 19771 | `a7313117776e6ba8255bf2f60755bfad5a6bcf510767f0129720f8425984f1cb` |
| `api/tests/test_process_metrics_api.py` | 23821 | `6eb1e0ced1cb745755f94b3719c1a91923ca7f6ffe4d538b21004b2a9432566a` |
| `api/app/main.py` | 524 | `038f7ea2c900f8288742586fe38430f6f5e0ce352fd1e4d7117d0e467f811dad` |

`api/app/main.py` 未写入且 byte-identical。其他 protected identities 也通过 final identity check：`docs/contracts/production_metrics_contract.md` = `8229 / 2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e`；`api/app/routes/quality_trace.py` = `9538 / 6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a`；`api/tests/test_quality_trace_api.py` = `13296 / bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c`。G3 与上述五项 authority identities 均保持不变。

## 4. Repair 内容与 exact write scope

Child-owned write paths 仅为：

- `api/app/routes/process_metrics.py`
- `api/tests/test_process_metrics_api.py`
- `docs/reports/p1_g4_repair_accepted_fact_lineage_nok_detail_20260811T1605Z.md`

未修改 `api/app/main.py`、G3/predecessor contract、predecessor route/test、Ledger、DB schema、configuration、frontend 或其他路径。report path 在写入前不存在。

F1：保留 accepted-fact-only SELECT；对 NULL/blank config hash/version 返回 `UNRESOLVED`，多个 tuple 返回 `MIXED`，单一 tuple 在当前无 historical resolver 时也返回 `UNRESOLVED`；route 不再包含 `SINGLE_RESOLVED`，ideal CT 保持无 numeric value 与 `HISTORICAL_CONFIG_AUTHORITY_MISSING`。

F2：accepted-fact SELECT 与 fake row fixture 覆盖 `nok_code`、`nok_origin`、`nok_detail_code`、`nok_detail_source_event_id`、`nok_detail_evidence_fact_key` 五项；任一 NOK detail NULL/blank 时 `quality_rate=PARTIAL`、reason `QUALITY_NOK_DETAIL_INCOMPLETE` 且 denominator>0 保留 numeric value；五项完整绑定的 accepted NOK 保持 predecessor `SUPPORTED`。未添加 join、fallback、synthetic evidence、schema migration、diagnostic/raw source 或 historical registry。

## 5. TDD 与 validation evidence

唯一 bounded TDD repair cycle：

1. RED：先写 F1/F2 regression tests 与 fixture，再运行：

   ```text
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -m pytest -p no:cacheprovider -q api/tests/test_process_metrics_api.py
   ```

   Result：`2 failed, 32 passed`。失败分别为 code-present/incomplete NOK detail 误报 `SUPPORTED`，以及 single config tuple 误报 `SINGLE_RESOLVED`；无语法/环境错误。

2. GREEN focused：同一命令在最小 route edit 后 `34 passed in 0.17s`。

3. predecessor regression：

   ```text
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -m pytest -p no:cacheprovider -q api/tests/test_process_metrics_api.py api/tests/test_quality_trace_api.py
   ```

   Result：`50 passed in 0.20s`。两套测试均 patch `app.db.get_conn` 使用 fake database；real DB connection count = 0。

4. in-memory compile：

   ```text
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api .venv/bin/python -B -c 'from pathlib import Path; files=(Path("api/app/routes/process_metrics.py"),Path("api/tests/test_process_metrics_api.py"),Path("api/app/main.py")); [compile(p.read_text(encoding="utf-8"),str(p),"exec") for p in files]; print("IN_MEMORY_COMPILE=PASS")'
   ```

   Result：`IN_MEMORY_COMPILE=PASS`。

5. 独立 import/route check：`GET /api/v2/process-metrics` exact registration = `PASS`，无其他 method；source/fallback/lineage static check = `PASS`，确认 accepted-fact source、half-open predicates、五项 detail fields、no `SINGLE_RESOLVED`、no forbidden legacy/current-YAML/WS03/DB-write/ACK/read_done source；`git diff --check` 与 untracked candidate `git diff --no-index --check` 均无 whitespace output。

## 6. Status、staged 与 containment evidence

首次写入前 live baseline：

```text
pwd -P = /Users/chenjie/Documents/MES/edge-mes-demo
git rev-parse --show-toplevel = /Users/chenjie/Documents/MES/edge-mes-demo
branch = main
HEAD = cf4eac54d3f365b0addfaae13f5e7292e3233641
origin/main = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
git status --short --untracked-files=all = 880 lines / 39c7c5190527f08d8dd0b7464157b414c20e7eaebac12dd4be365165a8efb5f5
git diff --cached --name-only = 0 lines / e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

首次 test write 与 route write 后均复核 full status count/SHA 未变，task-owned status 仍仅显示 pre-existing `M api/app/main.py` 与 untracked route/test，staged names 为空，report path 未创建。未清理或接管外部 dirty/untracked corpus。最终 audit 在 API bytecode/cache absence 断言失败后停止，故未对该失败作清理或二次验证。

Project runtime fresh identity：`.venv/bin/python` = CPython 3.13.3 arm64，pytest 9.1.1，FastAPI 0.115.6，psycopg 3.2.3；base = `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13`，`bytes=119328`，SHA-256 `f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5`。

## 7. State and counters

```text
WRITTEN = yes (local candidate/test and this report)
REVIEWED = yes (local TDD/test/hash/static audit)
ACCEPTED = no
VERIFIED = no
STAGED = no
COMMITTED = no
PUSHED = no
DEPLOYED = no
ACTIVATED = no
PRODUCTION_ACCEPTED = no

DB_RUNTIME_ACTION = 0
REMOTE_ACTION = 0
DOCKER_COMPOSE_ACTION = 0
PLC_VPLC_ACTION = 0
PRODUCTION_STIMULUS = 0
GIT_MUTATION = 0
PRODUCT_REPAIR = 1
```

本 child 未执行 DB/runtime、remote/SSH/network、Docker/Compose、PLC/V-PLC、production stimulus、Git stage/commit/push/tag/reset/stash/restore/checkout/rebase/merge/clean、Ledger edit、nested child、sub-agent、self-intake 或后续 gate。Parent 必须独立 intake 本 report 与 changed artifacts；本 report 不授权 Reliability re-review、Data Quality、Verification 或 Goal acceptance。

## 8. Next gate

`NEXT_GATE = PARENT_INDEPENDENT_REPAIR_REPORT_INTAKE`

Parent 应先处理 `API_BYTECODE_CACHE_AUDIT_FAILED`，重新核验 candidate/report identities 与 exact allowlist；不得把本 child 的 HOLD 解释为 parent acceptance，也不得继承 prior G4-R report 作为 changed candidate 的 fresh reliability acceptance。
