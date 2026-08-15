# P1-G2-I Candidate Import Syntax Repair Report

## 1. 任务结论

- 任务名称：P1-G2-I Candidate Import Syntax Repair
- 执行 Thread：Architecture / Integration
- 项目绝对路径：`/Users/chenjie/Documents/MES/edge-mes-demo`
- `PRIMARY_CLASS = PRODUCT_DEFECT`
- `CURRENT_FAILURE_FAMILY = G2_I_CANDIDATE_IMPORT_SYNTAX_ERROR`
- `PRODUCT_REPAIR_GATE = +1`
- `CONTROL_PLANE_RECOVERY_GATE = +0`
- 终端：`HOLD / FRESH_PRODUCT_OR_TEST_FAILURE`
- 原因：授权 route 语法修复后 import/compile smoke 通过；唯一 focused pytest 在 collection 阶段于 immutable `api/tests/test_quality_trace_api.py:297` 发现重复 keyword argument `fact_key`，exit `2`。按 authority 未修改测试、未重试。

## 2. Task self-identity 与 ordered reading

- task 文件：`docs/thread_handoff/pm_task_20260811T1153Z_p1_g2_i_candidate_import_syntax_repair.md`
- regular/non-symlink：`True` / `False`
- bytes：`19130`
- SHA-256：`5f5e1687f349df30c22922e750cf374035a2678d950b649682037d093abc976f`
- parent launcher 期望完全匹配；task 文件未修改。
- physical cwd 与 Git root 在解析相对路径前均为：`/Users/chenjie/Documents/MES/edge-mes-demo`

按 Section 5 的 2–16 顺序完成读取：

1. `docs/thread_handoff/pm_operating_rules.md`
2. `docs/current_status.md`
3. `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter.md`
4. `docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_bootstrap_dry_run.md`
5. `docs/reports/shadow_pm_p1_quality_trace_local_mvp_ledger.md`
6. `docs/reports/p1_g0_production_source_adequacy_semantic_boundary_freeze.md`
7. `docs/reports/p1_production_truth_semantics_trusted_consumption_plan.md`
8. `docs/contracts/production_metrics_contract.md`
9. `docs/thread_handoff/pm_task_20260811T1100Z_p1_g2_i_quality_trace_implementation.md`
10. `docs/reports/p1_g2_i_quality_trace_implementation.md`
11. `docs/thread_handoff/pm_task_20260811T1136Z_p1_g2_i_test_runtime_override_recovery.md`
12. `docs/reports/p1_g2_i_test_runtime_override_recovery.md`
13. `api/app/routes/quality_trace.py`
14. `api/app/main.py`
15. `api/tests/test_quality_trace_api.py`

## 3. Live repository / Git evidence

- branch：`main`
- HEAD：`dbe5706e4b01387101f2a4666e73f3c13ffeb0e`
- `origin/main`：`2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35`
- `origin/main...HEAD` left/right：`0<TAB>1`
- cached/staged names：空
- `git diff --cached --check`：exit `0`
- `git diff --check`：exit `0`
- entry tracked dirty set：`api/app/main.py`、`docs/current_status.md`、`docs/thread_handoff/pm_operating_rules.md`
- entry pre-existing untracked artifacts：存在；未 stage、adopt、clean 或修改。候选 route、测试、G1 contract、task 文件在 entry 均为 pre-existing untracked paths。
- child report entry：absent、non-symlink
- final staged/committed/pushed：`STAGED = NO`、`COMMITTED = NO`、`PUSHED = NO`
- Git mutation：`0`

## 4. Entry / final identities

| path | entry bytes | entry SHA-256 | final bytes | final SHA-256 | preserved |
| --- | ---: | --- | ---: | --- | --- |
| `api/app/routes/quality_trace.py` | 9529 | `b3d0464d4725271d8f444078971bb8e565e868810f089bc8f5df58c52875704a` | 9538 | `6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a` | authorized mutation |
| `api/app/main.py` | 464 | `2bdc34c1950654ca81d0041171a3c17d646c87e9655e79c3bac120baf47438ed` | 464 | `2bdc34c1950654ca81d0041171a3c17d646c87e9655e79c3bac120baf47438ed` | YES |
| `api/tests/test_quality_trace_api.py` | 13265 | `2c406e8e96a403d4b4a0eeb321d0ee5dcf37c01dd90b53e536f92fb270de4bd3` | 13265 | `2c406e8e96a403d4b4a0eeb321d0ee5dcf37c01dd90b53e536f92fb270de4bd3` | YES |
| `docs/contracts/production_metrics_contract.md` | 8229 | `2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e` | 8229 | `2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e` | YES |

Route exact-scope audit：entry route 经唯一授权逆变换可还原为 entry bytes/SHA；最终 helper 为 `return HTTPException(...)`，且恰有两个 `raise _source_unavailable(exc) from exc` call sites，plain raise 为 `0`。未发生其他 route 内容变化。

## 5. Control-plane 与 authorized venv identity

- control-plane：`/opt/homebrew/opt/python@3.14/bin/python3.14`
- 所有 identity、hash、parsing、audit 与本报告证据均由冻结 Python 3.14 完成。
- authorized runtime：`./.venv/bin/python`
- `.venv/pyvenv.cfg version`：`3.13.3`
- Python：`3.13.3`
- architecture：`arm64`
- resolved base interpreter：`/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13`
- base interpreter regular/non-symlink：`True` / `False`
- base interpreter bytes：`119328`
- base interpreter SHA-256：`f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5`
- pytest：`9.1.1`
- fastapi：`0.115.6`
- psycopg：`3.2.3`
- runtime/package/venv identity：PASS

## 6. Repair 与验证证据

唯一 product source mutation：`api/app/routes/quality_trace.py`。

精确变更：

```diff
-    ) from exc
+    )
 
     except Exception as exc:
-        raise _source_unavailable(exc)
+        raise _source_unavailable(exc) from exc
 
     except Exception as exc:
-        raise _source_unavailable(exc)
+        raise _source_unavailable(exc) from exc
```

上方三个语义边界分别为 helper return、quality endpoint call site、trace endpoint call site；未修改 endpoint、SQL、DTO、fallback 或 contract 语义。

Import/compile smoke（授权 venv，单次）：

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api ./.venv/bin/python -B -c 'from pathlib import Path; compile(Path("api/app/routes/quality_trace.py").read_text(), "api/app/routes/quality_trace.py", "exec"); import app.main; print("IMPORT_COMPILE_SMOKE=PASS")'
```

- result：`PASS`
- 未启动 server，未发起 API 请求，未连接 DB。

Focused pytest（严格单次）：

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=api ./.venv/bin/python -m pytest -q api/tests/test_quality_trace_api.py
```

- starts：`1`
- exit：`2`
- collection：started；execution：未开始
- earliest fresh failure：`api/tests/test_quality_trace_api.py:297`，`SyntaxError: keyword argument repeated: fact_key`
- output summary：pytest collection 在 `_pytest/assertion/rewrite.py` 编译 immutable test 时失败；未执行测试用例。
- 未重试 pytest，未运行其他测试或 suite。

## 7. Scope、状态与 counters

- `WRITTEN = YES`（本报告为唯一 child-created output）
- `PARENT_PM_INTAKE_REQUIRED = YES`
- `ACCEPTED = NO`
- `VERIFIED = NO`
- `STAGED = NO`
- `COMMITTED = NO`
- `PUSHED = NO`
- `RUNTIME_LOADED = NO`
- `PRODUCTION_ACCEPTED = NO`

```text
PRODUCT_SOURCE_MUTATIONS = 1 file: api/app/routes/quality_trace.py
TEST_SOURCE_MUTATIONS = 0
CONTRACT_MUTATIONS = 0
MAIN_PY_MUTATIONS = 0
VENV_MUTATIONS = 0
PACKAGE_OR_PIP_MUTATIONS = 0
NETWORK = 0
DB_API_RUNTIME = 0
DOCKER_COMPOSE = 0
REMOTE_SSH = 0
PLC_VPLC = 0
PRODUCTION_STIMULUS = 0
GIT_STAGE_COMMIT_PUSH_TAG = 0
P1_G3_EXECUTION = 0
NESTED_SUB_AGENTS = 0
```

## 8. Truth / fallback boundary

```text
LEGACY_KPI_FALLBACK = NO_CHANGE
LEGACY_TRACE_FALLBACK = NO_CHANGE
TIME_PROXIMITY_TRACE_FILL = NO_CHANGE
FIXED_WS03_PRODUCTION_AUTHORITY = NO_CHANGE
FULL_GENEALOGY_CLAIM = NO_CHANGE
FULL_OEE_NUMERIC_CLAIM = NO_CHANGE
DB_MIGRATION = 0
```

本 child 只报告 `WRITTEN` 证据与当前 HOLD；不更新 Ledger，不接受 candidate，不宣称 `VERIFIED`、`RUNTIME_LOADED` 或 `PRODUCTION_ACCEPTED`，不创建 successor/review/repair work。focused pytest 的 immutable test 语法错误由 parent PM intake 处理；本 child 不扩大 repair scope。

## 9. Terminal block

```text
G2_REPAIR_TASK_SELF_IDENTITY_PASS = YES
G2_FAILURE_FAMILY = G2_I_CANDIDATE_IMPORT_SYNTAX_ERROR
G2_PRIMARY_CLASS = PRODUCT_DEFECT
G2_REPAIR_ATTEMPT = NEXT_ATTEMPT
G2_ROUTE_ENTRY_BYTES = 9529
G2_ROUTE_ENTRY_SHA256 = b3d0464d4725271d8f444078971bb8e565e868810f089bc8f5df58c52875704a
G2_ROUTE_FINAL_BYTES = 9538
G2_ROUTE_FINAL_SHA256 = 6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a
G2_MAIN_IDENTITY_PRESERVED = YES
G2_TEST_IDENTITY_PRESERVED = YES
G2_G1_CONTRACT_IDENTITY_PRESERVED = YES
G2_RUNTIME_AUTHORITY = PASS
G2_IMPORT_COMPILE_SMOKE = PASS
G2_FOCUSED_PYTEST_STARTS = 1
G2_FOCUSED_TEST = FAIL
G2_PRODUCT_SOURCE_MUTATIONS = 1
G2_TEST_SOURCE_MUTATIONS = 0
G2_CONTRACT_MUTATIONS = 0
G2_MAIN_PY_MUTATIONS = 0
G2_VENV_MUTATIONS = 0
G2_PACKAGE_OR_PIP_MUTATIONS = 0
G2_NETWORK_DB_DOCKER_REMOTE_PLC_ACTIONS = 0
G2_GIT_MUTATIONS = 0
G2_P1_G3_EXECUTION = 0
G2_CHILD_TERMINAL = HOLD / FRESH_PRODUCT_OR_TEST_FAILURE
PARENT_PM_INTAKE_REQUIRED = YES
```
