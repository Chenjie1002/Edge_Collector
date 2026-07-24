# Sprint 4 D2-R7A-R3B Collector Reliability Test-double Alignment

## 报告名称

Sprint 4 D2-R7A-R3B Collector Reliability Test-double Alignment

## 任务名称

D2-R7A-R3B — Align the Collector Reliability Test Doubles with the Current Accepted-fact Storage Contract

## 执行 Thread

Reliability

## 结论

PASS WITH RECOMMENDATIONS

三个 R2/R3A carry-forward failure 已消失。两个 Reliability test files 的 test doubles
现在执行当前 accepted-fact transaction contract；ACK failure/retry、existing read_done
repair、Snap7 persistence/ACK 顺序均有可检查 evidence。Expected COTP DT 仅作为 local
test-owned Snap7 server disconnect cleanup log 保留，未被屏蔽，也未转化为测试失败。

本结论只关闭 R3B test-double alignment。D2-R7A-R1 仍为 HOLD pending independent
Verification，不授权 D2-R7B、deployment、activation 或 D3。

## Authority

本次 authority 来自用户明确授权的 D2-R7A-R3B Reliability implementation scope，以及：

docs/thread_handoff/pm_operating_rules.md
docs/current_status.md
docs/reports/sprint4_d2_r7a_r1_collector_package_closure_verification.md
docs/reports/sprint4_d2_r7a_r2_regression_failure_diagnosis.md
docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md
scripts/run_non_db_pytest.py
collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py
collector/app/services/event_collector.py
collector/app/services/storage.py
collector/app/services/accepted_station_event_fact.py
collector/app/services/station_event_adapter.py

docs/current_status.md 未包含当前 Sprint-4 R3B truth；按用户要求，以 live Git 与 R1/R2/R3A
exact reports 为 gate authority。没有执行 SSH、remote Docker、Compose lifecycle、DB/API
mutation、V-PLC/PLC request、production data generation、Git stage/commit/push/tag/clean。

## PM workload/context assessment

任务规模：中
风险等级：Level 2
涉及范围：两个 Collector Reliability 测试文件及一个新报告
当前 Thread 是否建议继续：no
是否需要新开 Thread：yes
理由：R3A Architecture / Integration 已结束；本任务只处理 Reliability fixture contract，不能与 Architecture 或 Verification 混合

## Live Git recovery

开始前只读 recovery：

project root: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 58e6c7e042436f31e1512c64e3ab40a08d14bf27
origin/main: 58e6c7e042436f31e1512c64e3ab40a08d14bf27
ahead/behind: 0 / 0
cached: empty

开始前目标状态：

collector/tests/test_event_collector_reliability.py: clean / unstaged
collector/tests/test_snap7_reliability_integration.py: clean / unstaged
docs/reports/sprint4_d2_r7a_r3b_collector_reliability_test_double_alignment.md: ABSENT / NON-SYMLINK / UNSTAGED

最终 recovery/audit：

git diff --check: PASS
git diff --cached --name-only: empty
staged set: empty

两个目标测试文件现在为 unstaged modified；新报告为 unstaged untracked。未执行任何 Git
index 或 history mutation。

## Current gate status

D2-R7A package closure evidence: accepted
D2-R7A-R1 independent Verification: HOLD pending independent Verification
D2-R7A-R2 diagnosis: complete
D2-R7A-R3A: PASS WITH RECOMMENDATIONS
D2-R7A-R3B: PASS WITH RECOMMENDATIONS
D2-R7B / deployment / activation / D3: not eligible

R3A 的 aggregate runner 没有重新实现或修改；本任务只消费其四分区 execution contract。

## Failure root-cause confirmation

Fresh repair 前 target command 的结果为 3 failed, 4 passed。三个失败均在目标 ACK/read_done
assertion 之前发生：

- test_event_collector_reliability.py::test_ack_write_failure_is_marked_then_retried_on_same_payload
  stale accepted decision double lacked normalized_event / fact_key / content_fingerprint
- test_event_collector_reliability.py::test_existing_read_done_repairs_database_ack_status_without_second_write
  same stale accepted decision double then stopped before transaction/read_done branch
- test_snap7_reliability_integration.py::test_collector_reads_db104_persists_cycle_then_writes_ack
  stale IntegrationStorage lacked transaction and accepted-fact/cycle no-commit APIs

The production call order confirmed from EventCollectorWorker._process_station() is:

accepted adapter decision
-> build_accepted_station_event_fact()
-> storage.transaction()
-> insert_accepted_station_event_fact_no_commit()
-> persist_cycle_no_commit()
-> transaction commit
-> ACK/read_done handling

The failure was stale test-double contract drift, not production ACK/read_done or storage runtime
defect. The fix stayed test-only.

## Exact changed files

collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py
docs/reports/sprint4_d2_r7a_r3b_collector_reliability_test_double_alignment.md

没有修改 collector/app/**、common/**、scripts/run_non_db_pytest.py、pytest.ini、Docker/Compose、
config、DB/migrations、API、V-PLC/simulator 或 existing reports/handoffs。

## Test-double contract alignment

两个测试文件内的 test doubles 现在具备：

- accepted adapter decision 的 normalized_event、fact_key、content_fingerprint，并包含可供 build_accepted_station_event_fact() 使用的 canonical identity fields；
- transaction() context boundary，包含 begin、commit 和异常 rollback 语义；
- insert_accepted_station_event_fact_no_commit()，按 fact_key 与 source_identity 做 same-content idempotency / differing-content conflict guard；
- persist_cycle_no_commit()，按 (plc_id, station_id, plc_boot_id, cycle_counter) 模拟 current cycle upsert；
- 旧 persist_cycle() helper 保留为 guard，若 worker 错误调用 internal-commit API 则明确失败；
- test-only evidence fields 记录 accepted fact attempts、唯一 fact identity/content、cycle persistence、transaction events、ACK attempts/writes、DB104/station reads 和 ACK status calls。

没有通过降低断言、skip、xfail、排除测试、增加 retry/sleep 或改变 production runtime
取得 PASS。

## ACK failure/retry evidence

目标测试：
collector/tests/test_event_collector_reliability.py::EventCollectorReliabilityTest::test_ack_write_failure_is_marked_then_retried_on_same_payload

fresh result：PASS

关键 evidence：

- transaction/persistence attempts: 2
- accepted-fact insert attempts: 2
- unique accepted facts retained: 1
- unique source_identity values: 1
- unique fact_key values: 1
- unique persisted cycle identities: 1
- ACK write attempts: 2
- successful PLC ACK writes: 1
- mark_cycle_ack_failed(): 1
- mark_cycle_ack_ok(): 1
- error evidence: ACK_WRITE_FAILED

test-owned event order：

begin -> accepted_fact -> persist_cycle -> commit
-> ack_write_attempt -> ack_write_failed -> ack_failed
-> begin -> accepted_fact(existing) -> persist_cycle(upsert) -> commit
-> ack_write_attempt -> ack_write -> ack_ok

这证明第一次 accepted-fact/cycle persistence 完成后 ACK write 才失败；第二次相同 payload
可以 retry；第二次只有一次成功 PLC ACK write；同一 business identity 没有第二个不同
accepted fact。

## read_done recovery evidence

目标测试：
collector/tests/test_event_collector_reliability.py::EventCollectorReliabilityTest::test_existing_read_done_repairs_database_ack_status_without_second_write

fresh result：PASS

关键 evidence：

- payload read_done: True
- accepted-fact insert attempts: 1
- unique accepted facts retained: 1
- cycle persistence calls: 1
- transaction event order: begin -> accepted_fact -> persist_cycle -> commit -> ack_ok
- PLC ACK write attempts: 0
- mark_cycle_ack_ok(): 1

因此 current persistence transaction 正常完成后，数据库 ACK status 被修复为成功；没有
第二次 PLC ACK write，也没有绕过 accepted-fact persistence contract。

## Snap7 persistence/ACK evidence

目标测试：
collector/tests/test_snap7_reliability_integration.py::Snap7ReliabilityIntegrationTest::test_collector_reads_db104_persists_cycle_then_writes_ack

fresh result：PASS

test-owned local Snap7 server evidence：

- DB read sequence: DB104 -> DB101 -> DB102 -> DB103 -> DB101 handshake verification
- DB104 boot identity: 12345678-1234-1234-1234-123456789abc
- WS01 accepted fact: line_id=LINE_001, plc_id=PLC_001, station_id=WS01, cycle_counter=1, event_type=station_result, production_result=ok
- accepted-fact persistence calls: 1
- accepted facts retained: 1
- cycle persistence calls: 1
- transaction/ACK order: begin -> accepted_fact -> persist_cycle -> commit -> ack_write -> ack_ok
- successful PLC ACK writes: 1
- ACK handshake bit: set
- collector errors: []

断开连接时 Snap7 server 输出 Expected COTP DT, got 0x80。该日志发生在 test-owned
server/client cleanup；测试 assertions 已全部通过，DB104/station reads、persistence、
ACK evidence 均成立，因此分类为 secondary cleanup log。没有修改 production Snap7
behavior，也没有屏蔽该日志来制造 PASS。

## Aggregate runner evidence

Canonical command：
.venv/bin/python scripts/run_non_db_pytest.py

各分区均使用 runner 当前 .venv/bin/python 启动独立 subprocess，且保留其指定 marker
expression not db_backed and not postgres_local：

| 分区 | command / PYTHONPATH | exit | collected / executed | passed | failed | skipped | deselected | collection errors |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Root/common | env PYTHONPATH=collector:. ... -m pytest ... -q tests / collector:. | 0 | 316 | 316 | 0 | 0 | 0 | 0 |
| Collector | env PYTHONPATH=collector:. ... -m pytest ... -q collector/tests / collector:. | 0 | 88 total / 81 executed | 81 | 0 | 0 | 7 | 0 |
| API | env PYTHONPATH=api:. ... -m pytest ... -q api/tests / api:. | 0 | 93 total / 58 executed | 58 | 0 | 0 | 35 | 0 |
| S7 PLC simulator | env PYTHONPATH=s7_plc_sim:. ... -m pytest ... -q s7_plc_sim/tests / s7_plc_sim:. | 0 | 27 | 27 | 0 | 0 | 0 | 0 |

runner summary：

PARTITION_EXIT_CODES=[0, 0, 0, 0]
AGGREGATE_EXIT_CODE=0
runner process exit code: 0

四个分区 collection errors 均为 0；没有通过 runner 排除三个原 failure。

## Packaging evidence

Command：
env PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_container_packaging.py -q

exit code: 0
2 passed

本次没有修改 Dockerfile、Compose 或 packaging test。

## Focused suite evidence

Command：
env PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_station_event_model.py tests/test_collector_station_event_adapter.py tests/test_collector_station_event_runtime_source.py tests/test_line_config.py -q

exit code: 0
303 passed
collection errors: 0

## Target-file test evidence

Command：
env PYTHONPATH=collector:. .venv/bin/python -m pytest collector/tests/test_event_collector_reliability.py collector/tests/test_snap7_reliability_integration.py -q

exit code: 0
7 passed
collection errors: 0

三个 R2/R3A 原 failure 全部 PASS；两个文件无新增 failure。

## Scope / explicitly not touched

本次 implementation scope：

collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py

本次新增 durable report：

docs/reports/sprint4_d2_r7a_r3b_collector_reliability_test_double_alignment.md

明确未触碰：

collector/app/**
common/**
scripts/run_non_db_pytest.py
pytest.ini
tests/**
api/**
s7_plc_sim/app/**
simulator/**
config/**
collector/Dockerfile
docker-compose.yml
db/**
migrations/**
existing reports
existing handoffs
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md

禁止操作 audit：

SSH / remote Docker / remote mapping deployment: 0
Compose service lifecycle / Collector deployment / activation: 0
DB query/write / API request/mutation: 0
V-PLC / PLC external request or mutation: 0
production data generation: 0
Git stage / commit / push / tag / clean: 0
production runtime modification: 0

## Allowlist audit

允许 changed/new set 恰为：

collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py
docs/reports/sprint4_d2_r7a_r3b_collector_reliability_test_double_alignment.md

最终执行：

git diff --check: PASS
git diff --name-only: only the two modified target tests plus pre-existing dirty tracked paths; new report is untracked and separately checked by status
git diff --cached --name-only: empty
git status --short -- collector/tests/test_event_collector_reliability.py collector/tests/test_snap7_reliability_integration.py docs/reports/sprint4_d2_r7a_r3b_collector_reliability_test_double_alignment.md:
  M collector/tests/test_event_collector_reliability.py
  M collector/tests/test_snap7_reliability_integration.py
  ?? docs/reports/sprint4_d2_r7a_r3b_collector_reliability_test_double_alignment.md

既有 dirty context 保持原样并排除：

M .gitignore
M collector/Dockerfile
M docker-compose.yml
M docs/current_status.md
M docs/roadmap.md
M docs/thread_handoff/pm_operating_rules.md
?? scripts/run_non_db_pytest.py
?? tests/test_collector_container_packaging.py
?? existing Sprint-3/Sprint-4 reports, handoffs and frontend local artifacts

这些路径不是本任务 changed set，未被 stage、覆盖、清理或纳入报告 allowlist。

## Blockers

本 R3B implementation/validation gate 无 blocker。

仍存在的 process boundary 不是本 R3B blocker：

D2-R7A-R1: HOLD pending independent Verification
D2-R7B / deployment / activation / D3: not eligible

## Recommendations

1. 由 ChatGPT PM 对本 R3B report 执行 intake，并另行决定是否发布新的独立 Verification gate。
2. Verification 应在独立 authority 下重跑其完整 allowlist/回归矩阵；本 Reliability Thread 不顺手执行下一 gate。
3. 保留 Expected COTP DT 作为 secondary cleanup diagnostic；如需 cleanup 专项分析，应新开独立、最小范围任务，不修改 production Snap7 behavior。

## Next gate

Current next action: ChatGPT PM intake of the R3B report.
Eligible only after PM decision: independent Verification gate.
Not eligible: D2-R7B, deployment, Collector activation, config deployment, production accepted-fact generation, D3.

即使 R3B 取得 PASS WITH RECOMMENDATIONS，也必须保持：

D2-R7A-R1: HOLD pending independent Verification

## MVP 路径一致性

classification: MVP-ALIGNED WITH BACKLOG ITEMS
approved MVP claim: Collector accepted-event persistence and reliable ACK/read_done boundary
minimum invariant: accepted-fact identity and atomic persistence complete before ACK/read_done mutation; same payload retry remains idempotent
new product capability: none
new threat model / retention framework / infrastructure / runtime topology: none
validation scope growth faster than MVP claim: no
validation/governance replacing product delivery: no

本任务只修复阻塞真实 Reliability assertion 的 stale test doubles，直接服务于已批准的
Collector 数据链路 MVP；没有把 test evidence 扩展为 DB-backed、remote、deployment 或
production acceptance claim。

## Thread 输出 / 上下文评估

本次输出长度：长
当前 Thread 是否建议继续：no
下一轮是否建议新开 Thread：yes
理由：R3B implementation、fresh regression、allowlist audit 和 durable report 已完成；下一步是独立 Verification gate，继续本 Thread 会混合 Reliability 与 Verification 职责。
