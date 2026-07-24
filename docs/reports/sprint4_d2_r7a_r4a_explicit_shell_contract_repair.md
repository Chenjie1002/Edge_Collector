# Sprint 4 D2-R7A-R4A Explicit Shell Contract Repair

## 报告名称

Sprint 4 D2-R7A-R4A Explicit Shell Contract Repair

## 任务名称

D2-R7A-R4A — Make the Aggregate Runner’s Non-shell Execution Contract Explicit

## 执行 Thread

Architecture / Integration

## 结论

PASS WITH RECOMMENDATIONS

本报告只关闭 D2-R7A-R4A 的 focused repair 目标：将 aggregate runner 的既有
non-shell execution contract 在 live source 中显式 materialize。它不关闭 D2-R7A-R4，
不改变 D2-R7A-R1 的状态，也不替代新的独立 Verification authority。

## Authority

本次 authority 来自用户明确授权的 D2-R7A-R4A Level 1 focused repair，以及：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md`
- `docs/reports/sprint4_d2_r7a_r4_collector_package_closure_reverification.md`
- `scripts/run_non_db_pytest.py`

Exact implementation allowlist 只有：

```text
scripts/run_non_db_pytest.py
docs/reports/sprint4_d2_r7a_r4a_explicit_shell_contract_repair.md
```

未执行 SSH、remote Docker、remote mapping deployment、Compose service lifecycle、
Collector deployment/activation、DB query/write、API request/mutation、V-PLC/PLC request
or mutation、production data generation、rollback、Git stage/commit/push/tag/clean，亦未进入
D2-R7B 或 D3。

## PM workload/context assessment

```text
任务规模: 小
风险等级: Level 1 focused repair，服务于当前 Level 2 D2-R7A gate
涉及范围: 一个 runner 文件和一个新 repair report
当前 Thread 是否建议继续: no
是否需要新开 Thread: yes
理由: R4 Verification Thread 已在 explicit shell contract blocker 处结束；本修复由
Architecture / Integration 独立执行，不能让 Verification 在原 Thread 中修改实现
```

## Live Git recovery

开始前按 authority 执行只读 recovery，结果为：

```text
project root: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 58e6c7e042436f31e1512c64e3ab40a08d14bf27
origin/main: 58e6c7e042436f31e1512c64e3ab40a08d14bf27
ahead / behind: 0 / 0
cached: empty
```

开始前目标文件身份确认：

```text
scripts/run_non_db_pytest.py:
  existing untracked R3A implementation, NON-SYMLINK, UNSTAGED
docs/reports/sprint4_d2_r7a_r4_collector_package_closure_reverification.md:
  existing untracked R4 Verification report, NON-SYMLINK, UNSTAGED
docs/reports/sprint4_d2_r7a_r4a_explicit_shell_contract_repair.md:
  ABSENT, NON-SYMLINK, UNSTAGED
```

工作树中另有实施前已存在的 dirty artifacts，包括 `.gitignore`、Collector
Docker/Compose、Reliability test files、governance/status/roadmap 文件、既有 reports、
handoffs 和 frontend 生成物；这些文件不属于本任务，未修改、覆盖、清理或纳入 allowlist。

## Current gate status

修复前后保持以下 gate 状态：

```text
D2-R7A package closure implementation: present, uncommitted
D2-R7A-R1: HOLD pending fresh independent Verification
D2-R7A-R3A: PASS WITH RECOMMENDATIONS
D2-R7A-R3B: PASS WITH RECOMMENDATIONS
D2-R7A-R4: HOLD / EXPLICIT_SHELL_CONTRACT_MISMATCH until fresh independent Verification
D2-R7B / deployment / activation / D3: not eligible
```

R4 的既有 positive execution record 被作为 intake context；本次 fresh local validation
证明 R4A repair contract，但没有把 positive result 推导为 R4 或 R1 closure。

## Blocker intake

R4 report 确认 live runner 原调用为：

```python
completed = subprocess.run(
    command,
    cwd=REPO_ROOT,
    env=environment,
    check=False,
)
```

Python 默认行为等价于 `shell=False`，但 R3A durable report 使用了显式
`subprocess.run(..., shell=False)` 的表述。该 mismatch 被分类为：

```text
LIVE SOURCE / DURABLE EVIDENCE MISMATCH
EXPLICIT AUDIT CONTRACT NOT MATERIALIZED
```

R4A 只处理这个 evidence contract，不处理其他 runner、测试、runtime 或 deployment
行为。

## Exact code change

在 `scripts/run_non_db_pytest.py:114-120` 的既有唯一 `subprocess.run()` 调用中增加一个
keyword argument：

```python
completed = subprocess.run(
    command,
    cwd=REPO_ROOT,
    env=environment,
    check=False,
    shell=False,
)
```

没有修改 `command` 内容、partition、environment、`check=False`、exit-code aggregation、
异常处理、stdout/stderr 处理、test selection、marker 或其他 runner 行为；没有增加 shell
wrapper，也没有使用位置参数表达 contract。

## Explicit shell-contract evidence

TDD read-only RED check 在修复前按预期失败：

```text
RED: subprocess.run is missing explicit shell keyword
process exit code: 1
```

修复后的 checks 使用项目 `.venv/bin/python`，未写入 repository：

```text
Python AST parse: PASS
subprocess.run call count: 1
explicit shell keyword count: 1
shell value: AST constant False
AST_EXPLICIT_SHELL_FALSE=PASS
AST_SUBPROCESS_RUN_CALL_COUNT=1
```

静态编译：

```text
.venv/bin/python -m py_compile scripts/run_non_db_pytest.py
exit code: 0
```

## Negative-case evidence

in-memory monkeypatch validation 使用 `.venv/bin/python`，没有写入 repository：

```text
NEGATIVE_SUBPROCESS_CALL=PASS
NEGATIVE_COMMAND_IS_LIST=PASS
NEGATIVE_CWD=/Users/chenjie/Documents/MES/edge-mes-demo
NEGATIVE_PYTHONPATH=collector:.
NEGATIVE_CHECK_FALSE=PASS
NEGATIVE_STDOUT_STDERR_PASSTHROUGH=PASS
```

该 monkeypatch 确认 `_run_partition()` 实际传递 `shell=False`，command 仍为 list，
`cwd` 仍为 repository root，`env["PYTHONPATH"]` 仍为当前分区值，`check=False` 保持不变，
且 kwargs 没有 `stdout`、`stderr` 或 `capture_output`。

缺少 required test root 的负例仍 fail-closed：

```text
NEGATIVE_MISSING_ROOT=PASS
error: test root is not a directory
```

模拟子进程 exit codes `[0, 1, 0, 0]` 的 aggregate 负例：

```text
NEGATIVE_NONZERO_AGGREGATE=PASS
PARTITION_EXIT_CODES=[0, 1, 0, 0]
AGGREGATE_EXIT_CODE=1
NEGATIVE_MAIN_NONZERO=PASS
```

## Aggregate evidence

canonical command：

```bash
.venv/bin/python scripts/run_non_db_pytest.py
```

四分区均由 runner 以独立 subprocess 执行，四分区 marker 均为
`not db_backed and not postgres_local`：

```text
Root/common: env PYTHONPATH=collector:. /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python -m pytest -m 'not db_backed and not postgres_local' -q tests
Collector: env PYTHONPATH=collector:. /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python -m pytest -m 'not db_backed and not postgres_local' -q collector/tests
API: env PYTHONPATH=api:. /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python -m pytest -m 'not db_backed and not postgres_local' -q api/tests
S7 PLC simulator: env PYTHONPATH=s7_plc_sim:. /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python -m pytest -m 'not db_backed and not postgres_local' -q s7_plc_sim/tests
```

| 分区 | test root / `PYTHONPATH` | exit | passed | failed | skipped | deselected | collection errors |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Root/common | `-m pytest -m 'not db_backed and not postgres_local' -q tests` / `collector:.` | 0 | 316 | 0 | 0 | 0 | 0 |
| Collector | `-m pytest -m 'not db_backed and not postgres_local' -q collector/tests` / `collector:.` | 0 | 81 | 0 | 0 | 7 | 0 |
| API | `-m pytest -m 'not db_backed and not postgres_local' -q api/tests` / `api:.` | 0 | 58 | 0 | 0 | 35 | 0 |
| S7 PLC simulator | `-m pytest -m 'not db_backed and not postgres_local' -q s7_plc_sim/tests` / `s7_plc_sim:.` | 0 | 27 | 0 | 0 | 0 | 0 | 0 |

canonical runner summary：

```text
Root/common: 316 passed in 1.13s
Collector: 81 passed, 7 deselected, 3 subtests passed in 0.30s
API: 58 passed, 35 deselected in 0.22s
S7 PLC simulator: 27 passed in 12.63s
PARTITION_EXIT_CODES=[0, 0, 0, 0]
AGGREGATE_EXIT_CODE=0
runner process exit code: 0
```

计数与 R4 预期一致；无新 failure、collection error 或漏跑。

## Packaging evidence

command：

```bash
env PYTHONPATH=collector:. .venv/bin/python -m pytest \
  tests/test_collector_container_packaging.py -q
```

result：`exit 0`，`2 passed`，`0 failed`，`0 collection errors`。

## Focused evidence

command：

```bash
env PYTHONPATH=collector:. .venv/bin/python -m pytest \
  tests/test_station_event_model.py \
  tests/test_collector_station_event_adapter.py \
  tests/test_collector_station_event_runtime_source.py \
  tests/test_line_config.py -q
```

result：`exit 0`，`303 passed in 1.10s`，`0 failed`，`0 skipped`，`0 collection errors`。

## Reliability evidence

command：

```bash
env PYTHONPATH=collector:. .venv/bin/python -m pytest \
  collector/tests/test_event_collector_reliability.py \
  collector/tests/test_snap7_reliability_integration.py -q
```

result：`exit 0`，`7 passed in 0.24s`，`0 failed`，`0 skipped`，`0 collection errors`。

## Exact changed files

本任务 changed/new set 恰为：

```text
scripts/run_non_db_pytest.py
docs/reports/sprint4_d2_r7a_r4a_explicit_shell_contract_repair.md
```

其中 runner 是开始前已存在的 untracked R3A implementation，本任务只修改其一个
`subprocess.run()` keyword；R4A report 是本任务唯一新增 report。

## Scope / explicitly not touched

未修改：

```text
docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md
docs/reports/sprint4_d2_r7a_r4_collector_package_closure_reverification.md
tests/**
collector/tests/**
collector/app/**
common/**
api/**
s7_plc_sim/**
simulator/**
pytest.ini
config/**
collector/Dockerfile
docker-compose.yml
db/**
migrations/**
existing reports
existing handoffs
governance docs
```

本次没有执行任何 remote/runtime/deployment/activation/DB/API/PLC/production-data 操作，
没有修改测试选择或 marker，也没有重新执行或宣称完成 R4 Verification。

## Allowlist audit

最终只读审计要求和结果：

```text
git diff --check: PASS
git diff --cached --name-only: empty
target status: scripts/run_non_db_pytest.py untracked; R4A report untracked
cached set: empty
```

由于两个允许路径均为 untracked，使用 `git diff --no-index --check /dev/null <path>`
补充检查时只出现 untracked-vs-/dev/null 的预期 exit 1，没有 whitespace diagnostics。
没有执行 Git stage、commit、push、tag 或 clean。

## Blockers

本 R4A focused repair 的实现与本地验证没有新 blocker。

Gate-level carry-forward blocker 保持不变：R4A 还没有被新的独立 Verification authority
重新 intake/re-verify，因此 `D2-R7A-R4` 与 `D2-R7A-R1` 仍为 `HOLD`。该边界不是本次
一行 contract repair 的失败，而是禁止 Architecture / Integration 自行关闭 Verification
gate 的流程约束。

## Recommendations

1. 由 ChatGPT PM intake 本 R4A report，并将 `shell=False` 作为 live source 的显式
   contract evidence。
2. PM 另行发布新的独立 Verification authority，fresh recovery 后重跑其完整授权矩阵；
   R4A 不修改 R4 report，也不在本 Thread 继续 Verification。
3. 在 fresh independent Verification 完成前，保持 D2-R7A-R1 `HOLD`，不进入 D2-R7B、
   deployment、Collector activation、production accepted-fact generation 或 D3。

## Next gate

```text
当前动作: 停止，等待 ChatGPT PM 对 R4A report intake
下一可授权动作: 新的独立 Verification authority / fresh R4 verification
D2-R7A-R1: HOLD pending fresh independent Verification
D2-R7B / deployment / activation / D3: not eligible
```

## MVP 路径一致性

```text
classification: MVP-ALIGNED WITH BACKLOG ITEMS
approved MVP claim: Collector package closure 的可信 non-DB regression execution boundary
minimum invariant: runner 的 non-shell contract 必须显式、子进程 failure 必须聚合传递，
  且 pytest stdout/stderr 不能被吞掉
new product capability: none
new runtime topology: none
new threat model / evidence-retention framework: none
scope drift: none
```

本任务直接消除 live source 与 durable evidence 的 false-PASS 风险，只增加一个显式
keyword，验证复杂度与当前 MVP claim 成比例；没有把 validation framework 扩展为新的
产品能力、运行拓扑、审计/留存系统或部署流程。

## Thread 输出 / 上下文评估

```text
本次输出长度: 中
当前 Thread 是否建议继续: no
下一轮是否建议新开 Thread: yes
理由: R4A repair、fresh local verification 和 durable report 已完成；下一步是独立
Verification authority，继续留在本 Thread 会混合 Architecture / Integration repair 与
Verification gate closure。
```
