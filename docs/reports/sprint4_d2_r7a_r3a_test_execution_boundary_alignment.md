# Sprint 4 D2-R7A-R3A Test Execution Boundary Alignment

## 报告名称

~~~text
Sprint 4 D2-R7A-R3A Test Execution Boundary Alignment
~~~

## 任务名称

~~~text
D2-R7A-R3A — Implement the Per-service-root Non-DB Pytest Aggregate Runner
~~~

## 执行 Thread

~~~text
Architecture / Integration
~~~

## 结论

~~~text
PASS WITH RECOMMENDATIONS
~~~

本报告只关闭 R3A 的 test execution boundary alignment 目标。D2-R7A-R1
整体 gate 仍保持 \`HOLD\`，原因是 Collector Reliability 的三个既有测试失败尚未处理；
这些失败已由新的 aggregate runner 真实显示并保留为 R3B carry-forward blocker。

## Authority

本次 authority 来自用户明确授权的 D2-R7A-R3A 实施范围，以及：

~~~text
docs/thread_handoff/pm_operating_rules.md
docs/reports/sprint4_d2_r7a_r1_collector_package_closure_verification.md
docs/reports/sprint4_d2_r7a_r2_regression_failure_diagnosis.md
pytest.ini
~~~

本任务只允许新增以下两个路径：

~~~text
scripts/run_non_db_pytest.py
docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md
~~~

未执行 SSH、remote Docker、remote mapping deployment、Compose service lifecycle、
Collector activation、DB query/write、API request/mutation、V-PLC/PLC request or
mutation、production data generation、rollback 或任何 Git stage/commit/push/tag/clean。

## PM workload/context assessment

~~~text
任务规模: 小
风险等级: Level 1 focused implementation，服务于当前 Level 2 D2-R7A gate
涉及范围: 一个测试 aggregate runner、一个 durable report
当前 Thread 是否建议继续: yes（实施授权已在本轮明确确认）
是否需要新开 Thread: no
理由: 只读诊断已在当前 Thread 完成；本轮未改变问题边界或职责边界
~~~

## Current Gate Status

~~~text
D2-R7A package closure evidence: accepted
D2-R7A-R1: HOLD
D2-R7A-R2 diagnosis: complete
D2-R7A-R3A boundary alignment: PASS WITH RECOMMENDATIONS
D2-R7B / activation / D3: not eligible
~~~

## Live Git recovery

实施前和最终审计均确认：

~~~text
project root: /Users/chenjie/Documents/MES/edge-mes-demo
branch:       main
HEAD:         58e6c7e042436f31e1512c64e3ab40a08d14bf27
origin/main:  58e6c7e042436f31e1512c64e3ab40a08d14bf27
ahead/behind: 0/0
cached:       empty
~~~

实施前目标路径状态均为：

~~~text
scripts/run_non_db_pytest.py: ABSENT / NON-SYMLINK / UNSTAGED
docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md:
  ABSENT / NON-SYMLINK / UNSTAGED
~~~

## Root cause confirmation

当前 repository 至少包含以下 service \`app\` roots：

~~~text
api/app
collector/app
simulator/app
s7_plc_sim/app
sync_worker/app
~~~

API、Collector、S7 simulator 的测试/runtime import contract 都使用裸 \`app.*\`，但
这些 service 在 Docker 中是独立 image/process；每个 container 的 \`/app/app\` 只有当前
service 的 app source root，因此 Docker runtime 不存在 repository-wide 的同解释器
namespace 竞争。

原始命令在单一 Python interpreter 中设置 \`PYTHONPATH=collector:.\`，使：

~~~text
app -> collector/app
app.main -> collector/app/main.py
~~~

API tests 的 \`from app.main import app\` 因此错误解析到 Collector \`app.main\`；S7 tests
的 \`app.control_api\`、\`app.pipeline\` 等也错误解析到 Collector namespace。多个裸
\`test_reliability.py\` 还会在同一 collection process 中产生 imported-module file
mismatch。

实施前 fresh reproduction：

~~~text
397/404 tests collected (7 deselected), 9 errors during collection
~~~

这确认 blocker 是 test execution boundary / namespace collision，不是 D2-R7A container
package closure，也没有证明 production runtime defect。

## Exact changed files

~~~text
scripts/run_non_db_pytest.py
docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md
~~~

\`pytest.ini\`、现有测试、production source、Docker/Compose、common、config 和既有报告
均未修改。

## Runner partition contract

\`scripts/run_non_db_pytest.py\` 使用当前 runner 的 \`sys.executable\` 启动四个独立
\`subprocess.run(..., shell=False)\`；每个子进程只接收一个 service source root 的
\`PYTHONPATH\`。Root/common 与 Collector 即使使用相同 \`PYTHONPATH\`，也保持两个独立
subprocess，避免把两个 test root 合并到一个 interpreter collection。

| 分区 | test root | subprocess \`PYTHONPATH\` | marker expression |
| --- | --- | --- | --- |
| Root/common tests | \`tests/\` | \`collector:.\` | \`not db_backed and not postgres_local\` |
| Collector tests | \`collector/tests/\` | \`collector:.\` | \`not db_backed and not postgres_local\` |
| API tests | \`api/tests/\` | \`api:.\` | \`not db_backed and not postgres_local\` |
| S7 PLC simulator tests | \`s7_plc_sim/tests/\` | \`s7_plc_sim:.\` | \`not db_backed and not postgres_local\` |

Runner additionally：

- fail-closed 检查四个 test roots 必须恰好覆盖指定集合；缺失、重复或额外遗漏会返回
  non-zero；
- fail-closed 检查当前 \`sys.executable\` 必须解析到项目 \`.venv/bin/python\`；
- 逐分区输出名称、test root、\`PYTHONPATH\`、完整命令和 exit code；
- 不捕获或重写 pytest stdout/stderr，collection errors、failed、skipped、deselected
  和 pytest traceback 保持原样输出；
- 任一子进程非零时输出 \`AGGREGATE_EXIT_CODE=1\` 并返回 non-zero；
- 不修改 pytest marker 定义，也不排除或静默跳过已知 Reliability failures。

## Subprocess validation evidence

### 1. Root/common tests

完整命令：

~~~bash
env PYTHONPATH=collector:. /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python \
  -m pytest -m 'not db_backed and not postgres_local' -q tests
~~~

结果：

~~~text
exit code: 0
collection errors: 0
collected: 316
passed: 316
failed: 0
skipped: 0
deselected: 0
~~~

### 2. Collector tests

完整命令：

~~~bash
env PYTHONPATH=collector:. /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python \
  -m pytest -m 'not db_backed and not postgres_local' -q collector/tests
~~~

结果：

~~~text
exit code: 1
collection errors: 0
collected: 81 executed + 7 deselected
passed: 78
failed: 3
skipped: 0
subtests passed: 3
~~~

三个失败均为 R2 已确认的既有 Reliability fixture contract failures：

~~~text
collector/tests/test_event_collector_reliability.py::EventCollectorReliabilityTest::test_ack_write_failure_is_marked_then_retried_on_same_payload
collector/tests/test_event_collector_reliability.py::EventCollectorReliabilityTest::test_existing_read_done_repairs_database_ack_status_without_second_write
collector/tests/test_snap7_reliability_integration.py::Snap7ReliabilityIntegrationTest::test_collector_reads_db104_persists_cycle_then_writes_ack
~~~

Failure boundary 仍是 R2 记录的 stale adapter/storage test doubles；本任务没有修改这些
测试文件、\`collector/app/**\`、ACK/read_done 或 storage contract。Runner 保留了三个
failure 的完整 pytest assertion/traceback，未将其转换成成功。

### 3. API tests

完整命令：

~~~bash
env PYTHONPATH=api:. /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python \
  -m pytest -m 'not db_backed and not postgres_local' -q api/tests
~~~

结果：

~~~text
exit code: 0
collection errors: 0
collected: 93 total / 35 deselected
passed: 58
failed: 0
skipped: 0
~~~

### 4. S7 PLC simulator tests

完整命令：

~~~bash
env PYTHONPATH=s7_plc_sim:. /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python \
  -m pytest -m 'not db_backed and not postgres_local' -q s7_plc_sim/tests
~~~

结果：

~~~text
exit code: 0
collection errors: 0
collected: 27
passed: 27
failed: 0
skipped: 0
deselected: 0
~~~

## Aggregate exit-code evidence

runner 原始汇总输出：

~~~text
PARTITION_EXIT_CODES=[0, 1, 0, 0]
AGGREGATE_EXIT_CODE=1
~~~

runner process exit code：

~~~text
1
~~~

该 non-zero 结果由 Collector 分区的三个已知 Reliability failures 真实产生；没有
collection error，也没有新增失败。原始单 interpreter 的 9 个 namespace-related
collection errors 已消失。

## Runner static check

命令：

~~~bash
.venv/bin/python -m py_compile scripts/run_non_db_pytest.py
~~~

结果：

~~~text
exit code: 0
~~~

## Packaging regression evidence

命令：

~~~bash
env PYTHONPATH=collector:. /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python \
  -m pytest tests/test_collector_container_packaging.py -q
~~~

结果：

~~~text
exit code: 0
2 passed in 0.01s
~~~

本任务没有修改 \`collector/Dockerfile\`、\`docker-compose.yml\` 或 packaging test。

## Focused Collector/station-event suite evidence

命令：

~~~bash
env PYTHONPATH=collector:. /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python \
  -m pytest \
  tests/test_station_event_model.py \
  tests/test_collector_station_event_adapter.py \
  tests/test_collector_station_event_runtime_source.py \
  tests/test_line_config.py -q
~~~

结果：

~~~text
exit code: 0
303 passed in 1.12s
collection errors: 0
failed: 0
skipped: 0
~~~

## Scope / explicitly not touched

本次实际新增：

~~~text
scripts/run_non_db_pytest.py
docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md
~~~

明确未触碰：

~~~text
pytest.ini
tests/**
collector/tests/**
api/tests/**
s7_plc_sim/tests/**
collector/app/**
api/app/**
s7_plc_sim/app/**
simulator/app/**
common/**
config/**
collector/Dockerfile
docker-compose.yml
existing reports
existing handoffs
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
~~~

未处理两个 Reliability test files 的 stale test doubles；该工作属于独立后续任务。

## Allowlist audit

实施前目标路径均为 \`ABSENT / NON-SYMLINK / UNSTAGED\`。最终审计确认：

~~~text
allowed new paths:
  scripts/run_non_db_pytest.py
  docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md

cached set: empty
git stage/commit/push/tag/clean: 0
~~~

最终 tracked dirty paths 仍为实施前已存在的：

~~~text
.gitignore
collector/Dockerfile
docker-compose.yml
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
~~~

既有 untracked handoff/report/frontend artifacts 也保持原样，未由本任务修改、覆盖、
清理或纳入 allowlist。两个新增路径以外没有本任务新增或修改的 repository 文件。

## Blockers

~~~text
R3B carry-forward blocker:
Collector 分区仍有三个既有 Reliability test failures；它们来自 R2 已确认的 stale
adapter/storage test doubles，在目标 ACK/read_done assertion 前阻塞。R3A 没有授权修复，
也没有 production runtime defect 证据。
~~~

该 blocker 使 D2-R7A-R1 overall regression gate 继续保持 \`HOLD\`，但不阻塞本 R3A
execution-boundary alignment 的 \`PASS WITH RECOMMENDATIONS\` 结论。

## Recommendations

1. 由 PM 单独 intake 本报告；不得从 R3A 结论自动进入 R3B、Reliability fixture repair
   或 Verification re-run。
2. 若 PM 后续授权 R3B，应只处理上述三个 stale test-double failures，并保留当前四分区
   runner 作为唯一 repository non-DB aggregate execution contract。
3. Reliability fixture 修复完成后，再由独立 Verification authority 重跑 packaging、
   focused、四分区 aggregate、container import closure 等其授权矩阵。

## Next gate

~~~text
当前动作: 停止，等待 ChatGPT PM 对 R3A 报告 intake。
下一阶段: 仅在 PM 新授权后，独立决定是否开启 D2-R7A-R3B / Reliability fixture repair。
D2-R7B / deployment / Collector activation / D3: not eligible / not authorized。
~~~

本 Thread 不自行执行下一 gate、Reliability repair、independent Verification、Git
commit/push 或任何 runtime/deployment 操作。

## MVP 路径一致性

~~~text
classification: MVP-ALIGNED WITH BACKLOG ITEMS
approved MVP claim:
  Collector package closure 与其可重复的 non-DB regression execution boundary
minimum invariant:
  不让多个 service app namespace 在同一 pytest interpreter 中产生 false collection
  result；任何真实子进程 failure 必须传递到 aggregate exit code
new product capability: none
new runtime topology: none
new threat model / evidence retention framework: none
scope drift: none
~~~

本任务只把已有 test execution contract 固化为四个 service-root subprocess；没有将
测试边界修复扩展为 production namespace refactor、Docker package repair、ACK/read_done
行为变化或 Reliability fixture implementation。验证复杂度与当前 MVP 的可信 regression
claim 相称，R3B failures 保持可见而不被 R3A 吞并。

## Thread 输出 / 上下文评估

~~~text
本次输出长度: 中
当前 Thread 是否建议继续: no（R3A 实施、验证和报告已完成）
下一轮是否建议新开 Thread: yes（若 PM 授权 R3B/Reliability repair，应使用新的明确 authority）
理由: 当前任务已达到最终边界；继续执行会把 test execution boundary 与 Reliability
fixture repair 或 Verification 混成一个 gate。
~~~
