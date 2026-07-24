# Sprint 4 D2-R7A-R4 Collector Package-closure Re-verification

## 报告名称

Sprint 4 D2-R7A-R4 Collector Package-closure Re-verification

## 任务名称

D2-R7A-R4 — Independently Re-verify the Collector Package Closure and Regression Repairs

## 执行 Thread

Verification

## 结论

HOLD

Packaging、focused Collector/station-event、Reliability target 和四分区 aggregate
positive checks 均通过；但 required negative-case contract 检查发现
scripts/run_non_db_pytest.py 的 live working tree 没有显式 shell=False。R3A 报告称
runner 使用 subprocess.run(..., shell=False)，与当前文件不一致。按本 Verification
authority，不能把 Python 默认值推断为已满足的 explicit evidence contract，因此在
negative-case gate 处 fail-closed 停止。

Compose render、validation image build、container import closure、container mapping
initialization 和 image cleanup 均未执行；本报告不将其推断为 PASS。

## Authority

本次 authority 来自用户指定的 D2-R7A-R4 independent Verification scope，以及：

- docs/thread_handoff/pm_operating_rules.md
- docs/current_status.md
- docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
- docs/reports/sprint4_d2_r7a_r1_collector_package_closure_verification.md
- docs/reports/sprint4_d2_r7a_r2_regression_failure_diagnosis.md
- docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md
- docs/reports/sprint4_d2_r7a_r3b_collector_reliability_test_double_alignment.md

本任务为 review/validation-only。除本报告外没有修改项目文件；发现 blocker 后没有
进入 repair，也没有扩大到 deployment、activation、DB/API/V-PLC/PLC 或 D2-R7B/D3。

## PM workload/context assessment

- 任务规模：中
- 风险等级：Level 2 Verification gate
- 涉及范围：D2-R7A package closure、R3A aggregate runner、R3B Reliability test doubles、本地 validation image 和本报告
- 当前 Thread 是否建议继续：no
- 是否需要新开 Thread：yes
- 理由：本轮在 negative-case contract blocker 处 fail-closed；后续 repair 或 re-verification 必须由 PM 另行 intake。

## Live Git and Docker recovery

开始前只读 recovery：

- branch: main
- HEAD: 58e6c7e042436f31e1512c64e3ab40a08d14bf27
- origin/main: 58e6c7e042436f31e1512c64e3ab40a08d14bf27
- ahead / behind: 0 / 0
- cached: empty

Expected gate artifacts 与用户给定集合一致：

- modified: collector/Dockerfile, docker-compose.yml,
  collector/tests/test_event_collector_reliability.py,
  collector/tests/test_snap7_reliability_integration.py
- untracked: tests/test_collector_container_packaging.py,
  scripts/run_non_db_pytest.py，以及 D2-R7A repair/R1/R2/R3A/R3B reports

.gitignore、governance docs、既有 handoff/report/frontend artifacts 等 external dirty
artifacts 保持原样，未修改、恢复、清理、stage 或纳入本任务。

Docker recovery：

- active context: colima
- SERVER: 29.5.2
- OS: Ubuntu 24.04.4 LTS
- ARCH: aarch64
- CPUS: 4
- MEM: 8307113984

R4 report preflight：ABSENT / NON-SYMLINK / UNSTAGED。
validation tag edge-mes-demo-collector:d2-r7a-r4-validation-20260724 preflight：ABSENT。

## Current gate status

- D2-R7A package closure implementation: present, uncommitted
- D2-R7A-R1: HOLD pending this independent re-verification
- D2-R7A-R2: diagnosis complete
- D2-R7A-R3A: PASS WITH RECOMMENDATIONS
- D2-R7A-R3B: PASS WITH RECOMMENDATIONS
- D2-R7B / deployment / activation / D3: not eligible

R4 不修改上述 gate status，也不将 positive checks 推导为 R1 closure。

## Reviewed implementation/test set

按用户指定顺序读取并核对：

- collector/Dockerfile
- docker-compose.yml
- tests/test_collector_container_packaging.py
- scripts/run_non_db_pytest.py
- collector/tests/test_event_collector_reliability.py
- collector/tests/test_snap7_reliability_integration.py
- config/mapping.yaml

同时读取 PM rules、current status、D2-R7A repair、R1、R2、R3A、R3B reports。

当前 Dockerfile 包含 collector/requirements.txt、collector/app 与 repository-root
common 的 COPY closure；Compose Collector build 为 context . 和
dockerfile collector/Dockerfile。

## Packaging result

执行：
env PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_container_packaging.py -q

结果：exit 0，2 passed，0 failed，0 collection errors。

## Focused result

执行用户指定的 station-event focused suite：

env PYTHONPATH=collector:. .venv/bin/python -m pytest
tests/test_station_event_model.py
tests/test_collector_station_event_adapter.py
tests/test_collector_station_event_runtime_source.py
tests/test_line_config.py -q

结果：exit 0，303 passed in 1.10s，0 failed，0 skipped，0 deselected，
0 collection errors。

## Reliability target result

执行：
env PYTHONPATH=collector:. .venv/bin/python -m pytest
collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py -q

结果：exit 0，7 passed in 0.24s，0 failed，0 skipped，0 deselected，
0 collection errors。

三个 R2 原 failure 均真实执行并通过。live tests 仍包含：

- ACK failure -> mark_cycle_ack_failed -> same-payload retry -> mark_cycle_ack_ok
- read_done=True -> no second PLC ACK write -> database ACK status repair
- Snap7 DB104 -> DB101/DB102/DB103 reads -> accepted persistence -> ACK write/handshake

required -q output 未显示 Expected COTP DT。R3B 的 secondary cleanup classification 未被
本 Thread 屏蔽或修改。

## Aggregate result

执行：
.venv/bin/python scripts/run_non_db_pytest.py

runner process exit code: 0。

| partition | test root | PYTHONPATH | exit | collected / executed | passed | failed | skipped | deselected | collection errors |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Root/common | tests | collector:. | 0 | 316 / 316 | 316 | 0 | 0 | 0 | 0 |
| Collector | collector/tests | collector:. | 0 | 88 / 81 | 81 | 0 | 0 | 7 | 0 |
| API | api/tests | api:. | 0 | 93 / 58 | 58 | 0 | 0 | 35 | 0 |
| S7 PLC simulator | s7_plc_sim/tests | s7_plc_sim:. | 0 | 27 / 27 | 27 | 0 | 0 | 0 | 0 |

四个 command 均使用 runner 当前 .venv interpreter、独立 subprocess 和
not db_backed and not postgres_local marker。runner summary 为：

- PARTITION_EXIT_CODES=[0, 0, 0, 0]
- AGGREGATE_EXIT_CODE=0

Collector partition 另报告 3 subtests passed；四分区 collection errors 均为 0。

## Negative-case result

所有 in-memory negative validation 均使用项目 .venv/bin/python，未写入 repository。

已通过：

- 缺少任一 required test root 时，_validate_partition_contract() 抛出 RuntimeError：
  NEGATIVE_MISSING_ROOT=PASS。
- monkeypatch 子进程 exit codes 为 [0, 1, 0, 0] 时，main() 返回 1，并输出
  PARTITION_EXIT_CODES=[0, 1, 0, 0]、AGGREGATE_EXIT_CODE=1：
  NEGATIVE_NONZERO_AGGREGATE=PASS。

Blocker：

- NEGATIVE_SHELL_FALSE=HOLD。

scripts/run_non_db_pytest.py:114-119 的 live source 为：

    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        env=environment,
        check=False,
    )

当前调用没有显式 shell=False。虽然 Python subprocess 默认值为 false，但本 gate 要求并
检查的是 runner 的 shell=False contract；不能用默认行为替代当前 working tree 的
explicit evidence，也不能根据 R3A 报告旧表述推断 live source 已满足。

因为该 required negative case fail-closed，本 Thread 没有继续执行同一 negative harness
中的 stdout/stderr passthrough 与 Reliability exclusion assertions，也没有修改 runner。
两次 loader/order setup error 发生在 runner contract assertion 之前，均未触及
repository；最终 source-based check 确认了上述真实 mismatch。

## Compose render result

NOT REACHED / stopped at required negative-case blocker。

未执行 docker compose config，未执行任何 Compose service lifecycle command。

## Image build identity

NOT REACHED / no docker build executed。

tag preflight 已确认 edge-mes-demo-collector:d2-r7a-r4-validation-20260724 ABSENT。
没有 image ID、architecture、OS 或 size evidence；没有启动 Compose service、Collector
或 validation container。

## Container import closure result

NOT REACHED。未执行 docker run --rm --network none --read-only。
IMPORT_CLOSURE 未声明。

## Mapping static initialization result

NOT REACHED。未执行 container-side load_edge_mapping()、build_read_plans()、resolved
snapshot 或 hash comparison。MAPPING_STATIC_INITIALIZATION 未声明。

## Host/container consistency

NOT REACHED。没有执行本次 authority 要求的 host/container 同一 mapping static
initialization 对照，不能声明 LINE_001、read-plan count 或 resolved config hash 一致。

## Cleanup result

NOT REQUIRED / NOT REACHED。没有执行 build，也没有创建由本 Thread 所有的 image/tag；
validation tag 从 preflight 起保持 ABSENT。没有执行 broad cleanup、prune 或删除其他 image。

## Exact allowlist audit

本 Thread 唯一允许新增路径：

docs/reports/sprint4_d2_r7a_r4_collector_package_closure_reverification.md

本 Thread 未修改任何 implementation/test/config/source 文件；R4 report 是唯一新增
文件。最终 audit 结果：

- git diff --check: PASS
- git diff --cached --name-only: empty
- R4 report: untracked / unstaged
- git diff --no-index --check /dev/null R4 report: no whitespace diagnostics；exit 1 为
  untracked file 与 /dev/null 的预期差异码

## Scope / explicitly not touched

明确未触碰：

- collector/Dockerfile
- docker-compose.yml
- tests/test_collector_container_packaging.py
- scripts/run_non_db_pytest.py
- collector/tests/**
- collector/app/**
- common/**
- api/**
- s7_plc_sim/**
- simulator/**
- config/**
- pytest.ini
- db/**
- migrations/**
- existing reports
- existing handoffs
- governance docs

Forbidden-action audit：

- SSH / remote Docker / remote mapping deployment: 0
- Compose service lifecycle: 0
- Collector deployment / activation: 0
- DB query/write: 0
- API request/mutation: 0
- V-PLC / PLC external request or mutation: 0
- production data generation: 0
- implementation/source/test/config modification: 0
- Git stage / commit / push / tag / clean: 0

## Blockers

1. scripts/run_non_db_pytest.py:114-119 does not explicitly pass shell=False, while the R4
   required negative-case contract requires that runner property to be proven against the live
   working tree. R3A report wording and live source are inconsistent.
2. Because the negative-case gate fail-closed, required Compose render, one-shot validation
   image build, container import closure, mapping initialization and host/container consistency
   evidence were not reached.

## Recommendations

1. PM intake the runner contract mismatch as a new minimal repair/re-review decision. This
   Verification Thread did not repair it.
2. After PM-authorized repair, run a fresh independent Verification authority from recovery and
   re-run the complete matrix, including remaining negative assertions, Compose render, one-shot
   image build, isolated container initialization and cleanup.
3. Do not change R1 to committed/closed; do not enter D2-R7B, deployment, activation or D3.

## Next gate

Current: HOLD。
Next eligible action: PM intake for minimal runner contract repair or explicitly re-scoped
independent re-verification。
Not eligible: D2-R7B / deployment / Collector activation / config deployment / production
accepted-fact generation / D3。

## MVP 路径一致性

- classification: MVP-ALIGNED WITH BACKLOG ITEMS
- approved MVP claim: Collector image package closure and credible non-DB regression boundary
- minimum invariant: no false PASS from a shared test process or swallowed subprocess failure;
  container/package evidence must remain separate from activation evidence
- new product capability: none
- new threat model / retention framework / runtime topology: none
- scope drift: none

The negative-case blocker directly affects whether the aggregate runner can be trusted as the
approved MVP regression boundary. The R4 stop rule prevented validation framework repair from
becoming an implicit implementation task.

## Thread 输出 / 上下文评估

- 本次输出长度：长
- 当前 Thread 是否建议继续：no
- 下一轮是否建议新开 Thread：yes
- 理由：本轮已完成独立 positive regression evidence，并在 live runner contract
  mismatch 处 HOLD；任何 repair 或重新验证都需要 PM 新 authority、独立 allowlist 和
  fresh recovery，不能在当前 Thread 顺势扩大。
