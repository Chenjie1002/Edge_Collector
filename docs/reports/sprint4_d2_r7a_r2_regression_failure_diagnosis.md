# D2-R7A-R2 broader regression failure diagnosis

## Task

~~~text
D2-R7A-R2 — Diagnose Broader Regression Failures after Package Closure Verification
~~~

本任务只做 root cause analysis、minimal repair plan design 与 impact assessment。不实施修复、
不修改测试、不修改 runtime source、不运行 Docker/Compose lifecycle、不访问 remote、不部署、
不激活 Collector，也不执行 DB/API/V-PLC/PLC 生产操作。

## Thread

~~~text
Architecture / Integration
~~~

任务类型：Level 2 Diagnosis Gate。Import execution boundary、Collector Reliability fixture
contract 与后续 Verification re-verification 保持独立职责，不创建混合职责 Thread。

## Authority

项目根目录：

~~~text
/Users/chenjie/Documents/MES/edge-mes-demo
~~~

开始前读取：

~~~text
docs/thread_handoff/pm_operating_rules.md
docs/reports/sprint4_d2_r7a_r1_collector_package_closure_verification.md
docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
collector/Dockerfile
docker-compose.yml
tests/test_collector_container_packaging.py
~~~

live Git recovery：

~~~text
HEAD:        58e6c7e042436f31e1512c64e3ab40a08d14bf27
origin/main: 58e6c7e042436f31e1512c64e3ab40a08d14bf27
ahead/behind: 0/0
cached:      empty
~~~

既有 D2-R7A / 外部 dirty paths 保持原样，未修改、未清理、未 stage：

~~~text
.gitignore
collector/Dockerfile
docker-compose.yml
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
tests/test_collector_container_packaging.py
既有 untracked handoff/report/frontend artifacts
~~~

本任务唯一新增文件是本报告；没有修改 collector/app、common、pytest.ini、配置、
Dockerfile、Compose 或任何测试文件。

## Current Gate Status

当前 gate 必须保持：

~~~text
D2-R7A package closure repair: accepted evidence
D2-R7A-R1 independent verification: HOLD
~~~

R1 已取得并保持：

~~~text
Packaging regression: PASS
Focused Collector/station-event: PASS
Compose render: PASS
Container import closure: PASS
Mapping static initialization: PASS
~~~

R1 未关闭：

~~~text
Repository broader non-DB pytest: 9 collection errors
Collector-only broader non-DB: 3 failed tests
~~~

本诊断不否定 package/container PASS，不重新打开 ModuleNotFoundError: common 的 package
closure 问题，也不改变 D2-R7A implementation。

## Environment Assumptions

~~~text
Python:        .venv/bin/python 3.13.3
pytest:        9.1.1
python-snap7:  3.0.0
pytest.ini:    仅声明 db_backed / postgres_local marker，没有 pythonpath 配置
~~~

Collector runtime image 使用 python:3.12-slim、WORKDIR /app、python -m app.main。当前
D2-R7A Dockerfile materialize：

~~~text
/app/app       <- collector/app
/app/common    <- repository common
~~~

本次只执行本地 pytest collection/test diagnostics 与本地 test fixture diagnostics。
Snap7 server 是 test-owned local fixture；没有真实/远端 V-PLC 或 PLC mutation，没有
DB/API/remote mutation。诊断结果不代表新的 container、DB 或 runtime acceptance 证据。

## Failure Classification

| blocker | first failing boundary | classification | production/runtime defect proven |
| --- | --- | --- | --- |
| broader 9 collection errors | Python module collection | test execution boundary / namespace collision | no |
| reliability failure 1 | accepted adapter double before storage/ACK | stale adapter fixture, then stale storage fixture | no |
| reliability failure 2 | accepted adapter double before storage/read_done | stale adapter fixture, then stale storage fixture | no |
| reliability failure 3 | storage double after DB104/DB101-103 reads | stale integration storage fixture | no |

三项 reliability failure 都在目标 assertion 前进入 STORAGE_WRITE_FAILED，不能直接证明
ACK/retry/read_done runtime behavior defect。

## Import Boundary Analysis

### Repository source roots

当前 repository 至少包含：

~~~text
api/app
collector/app
simulator/app
s7_plc_sim/app
sync_worker/app
~~~

各 service runtime 都可以使用 top-level app，但它们不是 repository-wide 同一 interpreter
中的可安全合并 namespace。s7_plc_sim/app 有 __init__.py；其他 service app roots 主要
通过 directory-on-sys.path 作为 namespace source 使用。

### PYTHONPATH=collector:. 的实际冲突

当前 invocation 的 module resolution：

~~~text
app       -> namespace search path: collector/app
app.main  -> collector/app/main.py
common    -> repository-root common/__init__.py
~~~

因此：

- API tests 的 from app.main import app 实际拿到 collector/app/main.py。Collector 的
  app.main 只有 main()，没有 FastAPI module-level app，产生 cannot import name app。
- s7 tests 的 app.control_api、app.pipeline、app.runtime_config 都错误查找 collector/app，
  产生 ModuleNotFoundError。
- collector/tests/test_reliability.py 与 s7_plc_sim/tests/test_reliability.py 有相同裸
  basename。pytest 默认 path-prepend collection 导致 imported-module file mismatch。
- DB-backed API test 即使 marker deselect，也必须先 import/collect；7 deselected 不能
  消除 collection error。

R1 reproduction：

~~~text
397/404 tests collected
9 errors during collection
7 deselected
~~~

分布为 4 个 API import errors、4 个 s7 import errors、1 个同名 test_reliability mismatch。

### Runtime Docker 与 pytest 的边界差异

~~~text
Docker runtime:
  每个 service 是独立 image/process。
  WORKDIR /app 下只有当前 service 的 /app/app；Collector 另有 /app/common。
  top-level import app 在单个 container 内无竞争。

Repository pytest:
  多个 service source roots 被放入一个 interpreter。
  PYTHONPATH=collector:. 只选择 collector/app 作为 app namespace。
  pytest 还会把多个 tests directories 参与 collection，放大裸 basename 冲突。
~~~

因此 container import closure PASS 与 repository-wide pytest collection HOLD 可以同时成立；
后者不构成 package closure 回归，不授权修改 Dockerfile/Compose。

### Minimal import direction

推荐每个 service source root 使用独立 subprocess/interpreter invocation，再由
aggregate gate 汇总 exit status：

~~~text
collector tests:    PYTHONPATH=collector:.
api tests:          PYTHONPATH=api:.
s7 tests:           PYTHONPATH=s7_plc_sim:.
root/common tests:  按测试实际 import contract 选择单一 source root
~~~

本诊断只做 collection 对照，结果如下，不能当作完整 regression PASS：

~~~text
PYTHONPATH=api:.          api/tests        58/93 collected, 35 deselected, no error
PYTHONPATH=s7_plc_sim:.  s7_plc_sim/tests 27 collected, no error
PYTHONPATH=collector:.   collector/tests  81/88 collected, 7 deselected, no error
~~~

--import-mode=importlib 可以缓解裸 test basename 导入方式，但不能单独解决 app source-root
collision，不是充分修复。

## Collector Reliability Failure Analysis

### Failure 1 — ACK write failure marked, then retried on same payload

目标测试：

~~~text
collector/tests/test_event_collector_reliability.py::EventCollectorReliabilityTest::test_ack_write_failure_is_marked_then_retried_on_same_payload
~~~

测试的 public assertion 是 storage.persist_calls == 2，但第一次 _process_station 就没有
进入 persist/ACK 分支。其 make_worker 在 test_event_collector_reliability.py:90-102
返回只有 disposition/final_error_code 的 SimpleNamespace。

当前 worker 在 event_collector.py:200-204 先执行：

~~~text
build_accepted_station_event_fact(adapter_decision)
storage.transaction()
storage.insert_accepted_station_event_fact_no_commit(...)
storage.persist_cycle_no_commit(...)
~~~

诊断 probe 取得的第一实际错误：

~~~text
STORAGE_WRITE_FAILED
AttributeError: 'types.SimpleNamespace' object has no attribute 'normalized_event'
~~~

所以当前 failure 首先是 accepted adapter decision fixture 没有实现
build_accepted_station_event_fact 所需的 canonical decision contract，不是
FakeClient.fail_writes=1 消费后的 ACK retry 失败。

即使补齐 adapter decision，旧 FakeStorage 在 test_event_collector_reliability.py:39-73
仍只提供 persist_cycle，缺少 transaction、accepted-fact no-commit 与 cycle no-commit
接口，下一步仍会在 storage boundary 失败。

当前实现预期状态转移：

~~~text
第一次同一 payload:
  last_counter=None -> ACCEPT
  transaction 成功 -> accepted fact/cycle 写入
  db_write 失败 -> ACK_WRITE_FAILED + mark_cycle_ack_failed

第二次同一 payload:
  same (plc_id, station_id, plc_boot_id, cycle_counter) -> DUPLICATE
  不因 DUPLICATE 直接 return，继续幂等 persistence/ACK recovery
  相同 fact identity/content -> fact insert existing
  cycle_event 使用同一业务唯一键 ON CONFLICT
  db_write 成功 -> mark_cycle_ack_ok
~~~

Storage 的 fact identity/no-op 在 storage.py:324-401；cycle_event 以
(plc_id, station_id, plc_boot_id, cycle_counter) upsert 在 storage.py:540-568。
当前证据支持 retry/idempotency 设计路径，但旧 fixture 未走到它。

### Failure 2 — Existing read_done repairs DB ACK status without second write

目标测试：

~~~text
collector/tests/test_event_collector_reliability.py::EventCollectorReliabilityTest::test_existing_read_done_repairs_database_ack_status_without_second_write
~~~

该测试同样先被缺失 normalized_event 拦截；补齐 adapter decision 后仍会被旧
FakeStorage.transaction 缺失拦截。因此 ack_ok_calls == 0 不是 read_done 分支证据。

当前 worker 在 event_collector.py:236-243 的顺序：

~~~text
成功完成 fact/cycle transaction
-> read_done=True 时直接 mark_cycle_ack_ok
-> 不调用 client.db_write
~~~

这与已通过的 adapter gate positive control test_event_collector_adapter_gate.py:279-287
一致：read_done=True 先 persistence，再 DB ACK-status repair，PLC 不发生第二次 write。
最小解释是 stale fixture contract，不是 read_done authority 或 duplicate write regression。

### Failure 3 — Snap7 reads DB104, persists cycle, then writes ACK

目标测试：

~~~text
collector/tests/test_snap7_reliability_integration.py::Snap7ReliabilityIntegrationTest::test_collector_reads_db104_persists_cycle_then_writes_ack
~~~

IntegrationStorage 在 test_snap7_reliability_integration.py:23-48 只提供旧
persist_cycle，没有 transaction/no-commit/fact API。

DEBUG reproduction 显示：

~~~text
DB104 read: success, 53 bytes
DB101 read: success, 346 bytes
DB102 read: success, 346 bytes
DB103 read: success, 346 bytes
WS01 payload decode: payload_ready=True, cycle_valid=True, cycle_counter=1
~~~

随后：

~~~text
STORAGE_WRITE_FAILED
AttributeError: 'IntegrationStorage' object has no attribute 'transaction'

persisted: 0
ack_ok: 0
client.db_write: not reached
~~~

这证明 DB104/DB101-103 read contract 已运行到 storage boundary；首个错误不是
DB104 mapping、Snap7 read timing 或 ACK bit encoding。Expected COTP DT, got 0x80 出现在
client disconnect 后的 server handler cleanup，是次级 cleanup diagnostic，不应先用
sleep/retry 修复。另一个 in-memory diagnostic storage 仅补齐 transaction、accepted-fact
no-commit 与 cycle no-commit API 后，该测试 assertion 通过；这不是生产 DB 证据。

## Root Cause Hypothesis

### Recommended

1. 将 repository-wide pytest 改为按 service source root 隔离的 test execution boundary，
   用独立 subprocess 汇总 broader non-DB gate。
2. 将两个 reliability test doubles 同步到 299d28a 后的 accepted-fact transaction
   contract，保留 ACK/read_done 状态顺序的精确断言。
3. 在新 authority 下重新执行完整 regression；不改变 Collector runtime code。

这是最小路径：修复 collection/test-fixture 与当前 implementation contract 的边界，
不把已通过的 container closure 改成新的 namespace architecture。

### Alternative

全 repository 显式 package namespace refactor，例如把 collector.app、api.app、
s7_plc_sim.app 等改成唯一顶层名称，并同步 production imports、Docker CMD、tests 与
启动入口。该方向会扩大 runtime/source 变更面并重新触及 container import contract，
不作为当前最小方案。

### Rejected

- 在 collector/app 中兼容旧 persist_cycle 或给 storage API 加 fallback：会掩盖 stale
  test double，可能绕过 accepted-fact atomic transaction。
- 增加 Snap7 sleep/retry 或改变 DB104/ACK 地址：当前首个错误在 storage fixture，关键
  reads 已成功。
- 修改 collector/Dockerfile、docker-compose.yml、common、pytest.ini 或 remote deployment：
  超出当前诊断和明示禁止范围。

## Minimal Repair Recommendation

### 1. 是否需要修改代码

~~~text
No code change required
~~~

这里的 code 指 production/runtime code。当前证据没有证明需要修改 collector/app、common、
Docker package closure 或 ACK/read_done runtime logic。

后续需要两个独立的 test-only / execution-boundary actions：

~~~text
import boundary: test execution contract update
reliability boundary: test-double contract update
~~~

这两个 action 不能在本诊断 Thread 中实施。

### 2. 修改范围预测

Expected files：

~~~text
collector/tests/test_event_collector_reliability.py
  - accepted adapter decision fixture 补齐 normalized_event/fact_key/content_fingerprint
  - FakeStorage 补齐 transaction、accepted-fact no-commit、persist-cycle no-commit
  - 保留旧 persist_cycle guard 或明确 worker 不应调用它

collector/tests/test_snap7_reliability_integration.py
  - IntegrationStorage 补齐同一 transaction/accepted-fact no-commit/cycle no-commit contract
  - 保留 DB104 read、WS01 payload、handshake/ACK assertions
~~~

Expected modules：仅上述测试文件中的 test double / fixture helpers。不修改
collector/app/services/event_collector.py 或 collector/app/services/storage.py。

Import execution boundary 推荐不新增 production module；如 PM 要求一个单一 canonical
命令，再由独立 Architecture / Integration authority 评估只负责分包 subprocess aggregate
的 test runner，且不把多个 app roots 合并进一个 Python process。

Out-of-scope：

~~~text
collector/Dockerfile
docker-compose.yml
collector/app/**
common/**
pytest.ini
config/**
api/app/**
s7_plc_sim/app/**
simulator/app/**
db/** / migrations
remote SSH / remote Docker / mapping deployment
Collector activation / Compose lifecycle
DB write / API mutation / V-PLC/PLC mutation / production data generation
Git stage / commit / push / tag
~~~

### 3. Regression Strategy

修复 authority 完成后必须由独立 Verification gate 重新验证：

| gate | required re-validation | pass condition |
| --- | --- | --- |
| packaging regression | tests/test_collector_container_packaging.py | 2 tests pass，且不改 Docker/Compose |
| focused collector tests | R1 station-event/collector focused suite | 303 passed，0 collection error |
| broader pytest | collector、api、s7_plc_sim source root 分包并 aggregate | 0 collection error，完整记录 deselect |
| collector reliability suite | 两个 reliability test files | 三个目标 failure 全部通过，状态顺序/identity 断言成立 |
| container import closure | fresh image import app.main、event_collector、common.station_event | IMPORT_CLOSURE=PASS，不解释为 activation |

关键 acceptance assertions：

~~~text
Failure 1:
  first ACK failure -> mark_cycle_ack_failed + ACK_WRITE_FAILED
  same payload second poll -> exactly one successful ACK write + mark_cycle_ack_ok
  same business identity does not create a second accepted fact

Failure 2:
  read_done=True -> no client.db_write
  DB ACK status repair exactly once
  persistence precedes ACK-status repair

Failure 3:
  DB104 identity read succeeds
  WS01 payload decoded and persisted in test-owned storage
  ACK bit written and handshake assertion passes
~~~

本矩阵不能在本 Thread 执行；当前只提出最小验证路线。

## Risk Assessment

### Product/runtime impact

~~~text
当前诊断没有发现必须修改 production Collector/Storage/ACK/read_done 的 blocker。
D2-R7A package closure、container import closure、mapping static initialization 不受影响。
~~~

### Repair risk

- Test-only contract sync 风险低，但必须同步 accepted decision identity 与 transaction
  ordering；只补方法名而不补 identity/rollback 语义会产生 false PASS。
- 分包 pytest 风险中等；aggregate 漏掉一个 service root 会把 collection error 变成假 PASS。
  必须记录每个 subprocess 的 command、exit code、collected、deselected 与 aggregate result。
- --import-mode=importlib 不能改变 app first-present resolution，不是完整修复。
- Expected COTP DT 若在 fixture contract 修复后仍造成 failure，再独立开 Reliability fixture
  investigation；当前没有证据支持改变 Snap7 timing 或 runtime protocol。

### Evidence limitation

本次 diagnosis 依赖 local test doubles 与 local Snap7 server。它确定失败边界和最小方向，
但不能替代未来授权的 real DB-backed transaction/race/unique-violation 验证，也不能授权
deployment、activation 或 D2-R7B。

## Required Follow-up Thread

必须拆成以下独立职责，不创建混合 Thread：

1. Architecture / Integration：只处理 repository test execution boundary / aggregate command
   contract；不修改 Collector Reliability fixture，不修改 production namespace。
2. Reliability：只处理两个 reliability test files 的 current storage/accepted-decision
   fixture contract，并验证 ACK failure/retry、read_done repair、Snap7 persistence/ACK
   状态顺序；不处理 repository-wide import boundary。
3. Verification：前两个独立任务完成后，重新执行 packaging、focused、分包 broader、
   reliability suite 与 container import closure；这是 re-verification gate，不顺手修复
   blocker。

上述独立 PASS 之前，D2-R7B、remote mapping deployment、Collector activation 与 D3 均不
eligible。

## Scope / Evidence / Blockers / Recommendations / Next Gate

### Scope

~~~text
Reviewed:
  PM rules, D2-R7A repair/R1 reports, collector/Dockerfile, docker-compose.yml,
  packaging test, pytest.ini, app roots, event_collector.py, storage.py,
  reliability tests and working adapter-gate fixtures.

Changed:
  docs/reports/sprint4_d2_r7a_r2_regression_failure_diagnosis.md only.

Explicitly not touched:
  implementation, tests, Docker/Compose, config, common, DB/API/V-PLC/PLC,
  remote state and Git index/history.
~~~

### Evidence

~~~text
Repository broader: 9 collection errors, 397/404 collected, 7 deselected
Collector broader: 78 passed, 3 failed, 7 deselected
API isolated collection: 58/93 collected, 35 deselected, no error
s7 isolated collection: 27 collected, no error
Collector isolated collection: 81/88 collected, 7 deselected, no error
Reliability diagnosis: missing accepted-decision/storage APIs are first errors
Snap7 diagnosis: DB104 and station reads succeed; storage transaction is first blocker
~~~

### Blockers

~~~text
1. Repository-wide pytest invocation has an invalid shared app import boundary.
2. Reliability test doubles predate the accepted-fact transaction API and stop before target
   ACK/read_done assertions.
3. No post-repair regression evidence exists; this diagnosis does not close R1 HOLD.
~~~

### Recommendations

~~~text
1. Keep production source and D2-R7A package closure unchanged.
2. Authorize only the two independent narrow follow-up actions listed above.
3. Require aggregate per-source-root regression before any next deployment gate.
4. Treat any new production/runtime blocker after fixture synchronization as a new Reliability
   finding, not permission to broaden this diagnosis.
~~~

### Next Gate

~~~text
Current next eligible action: PM authorization for separate boundary/fixture tasks.
D2-R7B: NOT ELIGIBLE from current HOLD.
Deployment / activation / D3: NOT AUTHORIZED.
~~~

## MVP 路径一致性

~~~text
classification: MVP-ALIGNED WITH BACKLOG ITEMS
approved MVP claim:
  Collector package closure and reliable accepted-event persistence/ACK boundary
minimum invariant:
  no false container import PASS, no stale test boundary masking a reliability regression,
  no ACK/read_done claim before storage/identity contract is exercised
new product capability: none
new threat model / retention / infrastructure / runtime topology: none
scope drift: no product scope drift
~~~

本轮存在重复 repair/review 的流程膨胀风险，但两个 blocker 都直接影响已批准 MVP 行为的
可信验证，推荐方案仅为 execution boundary 与 stale fixture contract 的最小收敛。若后续
出现与这两个根因无关的新 blocker，PM 应先做 scope reset/比例性复核，不得顺延本 authority。

## Thread Output / Context Assessment

~~~text
本次输出长度: 长
当前 Thread 是否建议继续: no
下一轮是否建议新开 Thread: yes
理由: 本诊断已完成并保持 HOLD；后续需分别处理 execution boundary、Reliability fixture
contract 与 Verification re-run，继续本 Thread 会违反职责隔离并扩大 authority。
~~~

## Conclusion

~~~text
HOLD
~~~

Diagnosis complete + minimal repair plan proposed。

HOLD 的根因不是 D2-R7A container package closure 回归，而是：

~~~text
repository-wide pytest 的多 app namespace / test collection 边界冲突
+
三个 reliability tests 使用了 299d28a 之前的 adapter/storage test-double contract
~~~

在新的职责隔离 follow-up authority 完成分包 collection contract 与 test-double 同步，
并取得完整回归矩阵之前，不能将 D2-R7A-R1 改判为 PASS，也不能进入 D2-R7B、deployment
或 activation。
