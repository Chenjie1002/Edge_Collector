# P1-G2-I Trace Test Helper Identity Repair Report

## 1. 任务结论

```text
PASS / P1_G2_I_TRACE_TEST_HELPER_IDENTITY_REPAIR_COMPLETE
PARENT_PM_INTAKE_REQUIRED = YES
```

本 child 严格执行唯一 authoritative task file。两处且仅两处测试夹具编辑完成，import/compile smoke 通过，唯一授权 focused pytest 启动 1 次并通过 `16 passed`。未修改 product source、main.py、contract、Amendment、Ledger 或其他路径；未执行任何外部、运行时、Git mutation 或 nested agent action。

## 2. Task / authority identity

```text
TASK_PATH = docs/thread_handoff/pm_task_20260811T1234Z_p1_g2_i_trace_test_helper_identity_repair.md
TASK_TYPE = regular / non-symlink
TASK_BYTES = 19861
TASK_SHA256 = 5d717743591f58e544db97cb67727332ae7cae3265b404535962a2c4398adcd2
TASK_FILE_LAUNCHER_IDENTITY = PASS
```

Amendment：

```text
PATH = docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter_amendment_001_project_test_runtime.md
BYTES = 5197
SHA256 = c8b558c75a926415041a90de5e8221e514e58cec80e48361c23480d83242c633
PRESERVED = YES
```

```text
CURRENT_GATE = P1-G2-I_QUALITY_TRACE_IMPLEMENTATION
G2_FAILURE_FAMILY = G2_I_FOCUSED_TEST_EXECUTION_TRACE_HELPER_IDENTITY_SETUP
G2_PRIMARY_CLASS = TEST_DEFECT
G2_REPAIR_ATTEMPT = 1
TASK_PRODUCT_REPAIR_GATE_DELTA = +1
PRODUCT_REPAIR_GATES_USED_AFTER_TASK = 3
CONTROL_PLANE_RECOVERY_GATE_DELTA = +0
CONTROL_PLANE_RECOVERY_GATES_USED = 1
TOTAL_DISPATCHED_GATE_DELTA = +1
TOTAL_DISPATCHED_GATES_AFTER_TASK = 6
MVP_ALIGNMENT = YES
ARCHITECTURE_REDESIGN = NO
```

## 3. Ordered-read manifest

以下路径按 task Section 5 的 1→17 顺序读取；第 1 项在任何其他 repository read、Git、Python、test、probe、sub-agent 或 write 前完成 self-identity gate：

1. `docs/thread_handoff/pm_task_20260811T1234Z_p1_g2_i_trace_test_helper_identity_repair.md`
2. `docs/thread_handoff/pm_operating_rules.md`
3. `docs/current_status.md`
4. `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter.md`
5. `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_bootstrap_dry_run.md`
6. `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter_amendment_001_project_test_runtime.md`
7. `docs/reports/shadow_pm_p1_quality_trace_local_mvp_ledger.md`
8. `docs/reports/p1_g0_production_source_adequacy_semantic_boundary_freeze.md`
9. `docs/reports/p1_production_truth_semantics_trusted_consumption_plan.md`
10. `docs/contracts/production_metrics_contract.md`
11. `docs/reports/p1_g2_i_candidate_import_syntax_repair.md`
12. `docs/reports/p1_g2_i_duplicate_fact_key_test_repair.md`
13. `api/app/routes/quality_trace.py`
14. `api/app/main.py`
15. `api/tests/test_quality_trace_api.py`
16. `.venv/pyvenv.cfg`
17. `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13`

未读取清单外的 repository 内容；未使用 sub-agent；未更新 Ledger。

## 4. Live Git / protected continuity

```text
PHYSICAL_CWD = /Users/chenjie/Documents/MES/edge-mes-demo
GIT_TOP_LEVEL = /Users/chenjie/Documents/MES/edge-mes-demo
BRANCH = main
HEAD = dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
ORIGIN_MAIN = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
ORIGIN_MAIN...HEAD = 0<TAB>1
CACHED_STAGED_NAMES = empty
GIT_DIFF_CHECK = PASS
GIT_CACHED_DIFF_CHECK = PASS
```

entry 与 final 的 pre-existing protected tracked dirty set 均为：

```text
api/app/main.py
docs/current_status.md
docs/thread_handoff/pm_operating_rules.md
```

上述三条 tracked dirty path 未被修改。本 task 的测试文件在 entry 即为 pre-existing untracked artifact；本 task 仅在该 exact allowlist path 上完成授权编辑。报告写入前 report path 不存在且为 non-symlink；所有其他既有 untracked artifacts 均保留。

## 5. Entry / final identities

| path | entry | final | result |
| --- | --- | --- | --- |
| `api/app/routes/quality_trace.py` | 9538 / `6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a` | same | preserved |
| `api/app/main.py` | 464 / `2bdc34c1950654ca81d0041171a3c17d646c87e9655e79c3bac120baf47438ed` | same | preserved |
| `api/tests/test_quality_trace_api.py` | 13230 / `ae29eb7bbfcdf7b8a28d8c8fc9186857d29b890f7294e50e776b5d51a51c26d3` | 13296 / `bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c` | exact two-edit repair |
| `docs/contracts/production_metrics_contract.md` | 8229 / `2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e` | same | preserved |
| Amendment | 5197 / `c8b558c75a926415041a90de5e8221e514e58cec80e48361c23480d83242c633` | same | preserved |
| previous report | 6569 / `74e7e01237c58c2ca1e73587ba1ec97a5eac48d93bdafa8237210cc8f0dead05` | same | preserved |

两处精确语义编辑：

1. `request_trace()` 在 `query.update(params)` 前加入 `if "dmc" in params: query.pop("unit_id")`；DMC-only 请求移除 helper 默认 unit identity，显式同时提供两者时仍由 `query.update(params)` 保留 XOR rejection。
2. `test_trace_identity_is_xor_and_rejects_before_db_query` 的第一项参数从 `{}` 改为 `{"unit_id": ""}`，保留 422 与 no-DB-query 断言。

control-plane Python 对 final source 做反向重建：撤销上述新增 block 与空 mapping replacement 后得到 `13230` bytes、SHA-256 `ae29eb7bbfcdf7b8a28d8c8fc9186857d29b890f7294e50e776b5d51a51c26d3`，机械证明没有第三处测试源变更。

## 6. Runtime identities

CONTROL_PLANE_PYTHON：

```text
ENTRYPOINT = /opt/homebrew/opt/python@3.14/bin/python3.14
RESOLVED = /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14
VERSION = 3.14.6
ARCHITECTURE = arm64
BYTES = 52448
SHA256 = b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf
```

PROJECT_TEST_RUNTIME：

```text
RUNTIME = ./.venv/bin/python
PYVENV_VERSION = 3.13.3
PYTHON = 3.13.3
ARCHITECTURE = arm64
RESOLVED_BASE = /Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13
BASE_REGULAR_NON_SYMLINK = YES
BASE_BYTES = 119328
BASE_SHA256 = f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5
PYTEST = 9.1.1
FASTAPI = 0.115.6
PSYCOPG = 3.2.3
G2_PROJECT_TEST_RUNTIME = PASS
```

## 7. Validation evidence

Import/compile collection-precondition smoke（single run，未启动 server、未连接 DB/API）：

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api ./.venv/bin/python -B -c 'from pathlib import Path; compile(Path("api/tests/test_quality_trace_api.py").read_text(), "api/tests/test_quality_trace_api.py", "exec"); import app.main; print("IMPORT_COLLECTION_SMOKE=PASS")'
result = IMPORT_COLLECTION_SMOKE=PASS
G2_IMPORT_COLLECTION_SMOKE = PASS
```

Exact focused pytest（single authorized start）：

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api ./.venv/bin/python -m pytest -q api/tests/test_quality_trace_api.py
starts = 1
result = 16 passed in 0.17s
G2_FOCUSED_PYTEST_STARTS = 1
G2_FOCUSED_TEST = PASS
```

未运行 broad suite、第二次 pytest、server、DB/API live runtime、Docker、network 或 remote probe。

## 8. Changed-path / action audit

```text
TASK_SOURCE_CHANGED_PATH = api/tests/test_quality_trace_api.py
REPORT_CREATED_PATH = docs/reports/p1_g2_i_trace_test_helper_identity_repair.md
OTHER_SOURCE_CHANGED_PATHS = none
CACHED_STAGED_NAMES = empty
GIT_DIFF_CHECK = PASS
LEDGER_MUTATIONS_BY_CHILD = 0
```

本 child 只写入 Section 9 授权的测试路径与本 exact report path；没有创建 artifact。`WRITTEN` 仅表示 report 已写入，不表示 PM intake、acceptance、verification 或 Git publication。

## 9. Action counters and state distinctions

```text
G2_TEST_SOURCE_MUTATIONS = 1
G2_PRODUCT_SOURCE_MUTATIONS = 0
G2_MAIN_PY_MUTATIONS = 0
G2_CONTRACT_MUTATIONS = 0
G2_AMENDMENT_MUTATIONS = 0
G2_VENV_MUTATIONS = 0
G2_PACKAGE_OR_PIP_MUTATIONS = 0
G2_NETWORK_DB_DOCKER_REMOTE_PLC_ACTIONS = 0
G2_GIT_MUTATIONS = 0
G2_P1_G3_EXECUTION = 0
G2_NESTED_SUB_AGENTS = 0
G2_LEDGER_MUTATIONS_BY_CHILD = 0
WRITTEN = YES
ACCEPTED = NO
VERIFIED = NO
STAGED = NO
COMMITTED = NO
PUSHED = NO
RUNTIME_LOADED = NO
PRODUCTION_ACCEPTED = NO
```

## 10. Explicit boundary block

```text
LEGACY_KPI_FALLBACK = NO_CHANGE
LEGACY_TRACE_FALLBACK = NO_CHANGE
TIME_PROXIMITY_TRACE_FILL = NO_CHANGE
FIXED_WS03_PRODUCTION_AUTHORITY = NO_CHANGE
FULL_GENEALOGY_CLAIM = NO_CHANGE
FULL_OEE_NUMERIC_CLAIM = NO_CHANGE
DB_MIGRATION = 0
```

## 11. Required terminal block

```text
G2_TEST_REPAIR_TASK_SELF_IDENTITY_PASS = YES
G2_FAILURE_FAMILY = G2_I_FOCUSED_TEST_EXECUTION_TRACE_HELPER_IDENTITY_SETUP
G2_PRIMARY_CLASS = TEST_DEFECT
G2_REPAIR_ATTEMPT = 1
G2_TEST_ENTRY_BYTES = 13230
G2_TEST_ENTRY_SHA256 = ae29eb7bbfcdf7b8a28d8c8fc9186857d29b890f7294e50e776b5d51a51c26d3
G2_TEST_FINAL_BYTES = 13296
G2_TEST_FINAL_SHA256 = bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c
G2_ROUTE_IDENTITY_PRESERVED = YES
G2_MAIN_IDENTITY_PRESERVED = YES
G2_G1_CONTRACT_IDENTITY_PRESERVED = YES
G2_AMENDMENT_IDENTITY_PRESERVED = YES
G2_PROJECT_TEST_RUNTIME = PASS
G2_IMPORT_COLLECTION_SMOKE = PASS
G2_FOCUSED_PYTEST_STARTS = 1
G2_FOCUSED_TEST = PASS
G2_TEST_SOURCE_MUTATIONS = 1
G2_PRODUCT_SOURCE_MUTATIONS = 0
G2_MAIN_PY_MUTATIONS = 0
G2_CONTRACT_MUTATIONS = 0
G2_AMENDMENT_MUTATIONS = 0
G2_VENV_MUTATIONS = 0
G2_PACKAGE_OR_PIP_MUTATIONS = 0
G2_NETWORK_DB_DOCKER_REMOTE_PLC_ACTIONS = 0
G2_GIT_MUTATIONS = 0
G2_P1_G3_EXECUTION = 0
G2_CHILD_TERMINAL = PASS / P1_G2_I_TRACE_TEST_HELPER_IDENTITY_REPAIR_COMPLETE
PARENT_PM_INTAKE_REQUIRED = YES
```

## 12. MVP alignment / next gate / Thread assessment

`MVP 路径一致性 = MVP-ALIGNED`：本 task 只修复已批准 Quality + accepted-fact Trace MVP 的测试请求构造，使 DMC-only 与 explicit blank identity 的已冻结 XOR contract 得到正确回归覆盖；未新增产品能力、威胁模型、证据平台、基础设施或 runtime topology，也未把验证机制扩展为产品交付物。

唯一 next gate：Parent Shadow Mainline PM independent intake。Parent 必须重新读取本 report 与实际 repository files，独立核验 report/test identities、两处 diff scope、route/main/G1/Amendment continuity、Git state、pytest evidence 与 `WRITTEN`/`ACCEPTED`/`VERIFIED` distinctions；本 child 不接受 G2、不更新 Ledger、不创建后续 Reliability task。

Thread output/context assessment：本次输出为短 durable report；当前 child 已完成 exact scope，不创建或切换 top-level Thread；task-file sub-agent plan 为 `no / none`，实际使用 `no / none`，无偏差。

