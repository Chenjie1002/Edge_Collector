# Sprint 4 D2-R7A-R4-R1 Collector Package-closure Re-verification

## 报告名称

Sprint 4 D2-R7A-R4-R1 Collector Package-closure Re-verification

## 任务名称

D2-R7A-R4-R1 — Freshly Re-verify the Collector Package Closure after the Explicit Shell-contract Repair

## 执行 Thread

Verification

## 结论

PASS

本报告只关闭本次 fresh independent Verification matrix 的本地 package-closure、non-DB regression、Compose render、validation image、container import/static mapping 与 cleanup 证据边界。未关闭 Git closeout，也未授权 D2-R7B、deployment、activation 或 D3。

## Authority

本次 authority 来自用户指定的 D2-R7A-R4-R1 Level 2 Verification scope，以及以下 exact authority/report/source：

- docs/thread_handoff/pm_operating_rules.md
- docs/current_status.md
- docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
- docs/reports/sprint4_d2_r7a_r1_collector_package_closure_verification.md
- docs/reports/sprint4_d2_r7a_r2_regression_failure_diagnosis.md
- docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md
- docs/reports/sprint4_d2_r7a_r3b_collector_reliability_test_double_alignment.md
- docs/reports/sprint4_d2_r7a_r4_collector_package_closure_reverification.md
- docs/reports/sprint4_d2_r7a_r4a_explicit_shell_contract_repair.md
- collector/Dockerfile
- docker-compose.yml
- tests/test_collector_container_packaging.py
- scripts/run_non_db_pytest.py
- collector/tests/test_event_collector_reliability.py
- collector/tests/test_snap7_reliability_integration.py
- config/mapping.yaml

本任务为 review/validation-only。除本报告外没有修改项目文件；没有进入 repair、remote/runtime deployment、DB/API/V-PLC/PLC 或 production data scope。

## PM workload/context assessment

- 任务规模：中
- 风险等级：Level 2 Verification gate
- 涉及范围：package closure、test execution boundary、Reliability test doubles、Compose render、本地 validation image、container static initialization 与本报告
- 当前 Thread 是否建议继续：no
- 是否需要新开 Thread：yes
- 理由：本 fresh independent Verification 已完成完整矩阵；后续只等待 PM intake 与 exact-path Git closeout 决策，不能在本 Thread 顺势进入下一个 gate。

## Live Git and Docker recovery

项目路径：/Users/chenjie/Documents/MES/edge-mes-demo

开始前只读 recovery：

    branch: main
    HEAD: 58e6c7e042436f31e1512c64e3ab40a08d14bf27
    origin/main: 58e6c7e042436f31e1512c64e3ab40a08d14bf27
    ahead / behind: 0 / 0
    cached: empty

开始前 scoped expected gate artifacts 与用户给定集合一致：

    modified:
      collector/Dockerfile
      docker-compose.yml
      collector/tests/test_event_collector_reliability.py
      collector/tests/test_snap7_reliability_integration.py
    untracked:
      tests/test_collector_container_packaging.py
      scripts/run_non_db_pytest.py
      D2-R7A repair/R1/R2/R3A/R3B/R4/R4A reports

.gitignore、governance/status/roadmap、历史 reports、handoffs 与 frontend generated/local artifacts 是既有 external dirty artifacts，未修改、恢复、清理、stage 或纳入本任务。

Docker recovery：

    active context: colima
    SERVER: 29.5.2
    OS: Ubuntu 24.04.4 LTS
    ARCH: aarch64
    CPUS: 4
    MEM: 8307113984

新报告 preflight：ABSENT / NON-SYMLINK / UNSTAGED。

R4A live-source repair preflight：scripts/run_non_db_pytest.py 中唯一的 subprocess.run() 调用包含显式 shell=False；AST value 为常量 False。

validation tag edge-mes-demo-collector:d2-r7a-r4-r1-validation-20260724 开始前为 ABSENT。

## Current gate status

验证前保持：

    D2-R7A package closure implementation: present, uncommitted
    D2-R7A-R1: HOLD pending this independent Verification
    D2-R7A-R2: diagnosis complete
    D2-R7A-R3A: PASS WITH RECOMMENDATIONS
    D2-R7A-R3B: PASS WITH RECOMMENDATIONS
    D2-R7A-R4: HOLD
    D2-R7A-R4A: PASS WITH RECOMMENDATIONS
    D2-R7B / deployment / activation / D3: not eligible

本报告不修改上述历史 gate status，也不将本地 positive evidence 推导为 deployment、activation、production fact 或 D3 evidence。

## Reviewed implementation/test set

本次核对的 current implementation/test set：

- collector/Dockerfile
- docker-compose.yml
- tests/test_collector_container_packaging.py
- scripts/run_non_db_pytest.py
- collector/tests/test_event_collector_reliability.py
- collector/tests/test_snap7_reliability_integration.py
- config/mapping.yaml

并按用户指定顺序读取 PM rules、current status、D2-R7A repair、R1、R2、R3A、R3B、R4 与 R4A reports。

## Packaging result

命令：

    env PYTHONPATH=collector:. .venv/bin/python -m pytest \
      tests/test_collector_container_packaging.py -q

结果：

    exit code: 0
    2 passed
    0 failed
    0 collection errors

测试真实确认 Compose Collector build 为 repository-root context，并确认 Dockerfile 的 collector/requirements.txt、collector/app 与 repository-root common COPY closure。

## Focused result

命令：

    env PYTHONPATH=collector:. .venv/bin/python -m pytest \
      tests/test_station_event_model.py \
      tests/test_collector_station_event_adapter.py \
      tests/test_collector_station_event_runtime_source.py \
      tests/test_line_config.py -q

结果：exit code 0，303 passed，0 failed，0 skipped，0 collection errors。

## Reliability result

命令：

    env PYTHONPATH=collector:. .venv/bin/python -m pytest \
      collector/tests/test_event_collector_reliability.py \
      collector/tests/test_snap7_reliability_integration.py -q

结果：exit code 0，7 passed，0 failed，0 skipped，0 xfailed，0 collection errors。

三个 R2 failure 均在本轮实际执行并通过：

- ACK failure 后写入失败状态，并允许相同 payload retry；第二次只产生一次成功 ACK write；相同 business identity 只保留一个 accepted fact。
- read_done=True 完成 persistence 后修复数据库 ACK status，PLC ACK write 次数为 0。
- Snap7 实际读取 DB104、DB101、DB102、DB103，并完成 accepted-fact/cycle persistence、transaction completion before ACK、ACK handshake 与 ACK success marking。

本轮 -q target output 没有出现 Expected COTP DT；没有屏蔽或修改 production Snap7 behavior。R3B 的既有 secondary cleanup classification 保持不变。

## Aggregate result

canonical command：

    .venv/bin/python scripts/run_non_db_pytest.py

完整 fresh evidence：

| 分区 | test root | PYTHONPATH | exit | collected | executed | passed | failed | skipped | deselected | collection errors |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Root/common | tests/ | collector:. | 0 | 316 | 316 | 316 | 0 | 0 | 0 | 0 |
| Collector | collector/tests/ | collector:. | 0 | 88 | 81 | 81 | 0 | 0 | 7 | 0 |
| API | api/tests/ | api:. | 0 | 93 | 58 | 58 | 0 | 0 | 35 | 0 |
| S7 PLC simulator | s7_plc_sim/tests/ | s7_plc_sim:. | 0 | 27 | 27 | 27 | 0 | 0 | 0 | 0 |

runner summary：

    PARTITION_EXIT_CODES=[0, 0, 0, 0]
    AGGREGATE_EXIT_CODE=0
    runner process exit code: 0

四个分区均由独立 subprocess 执行，marker 为 not db_backed and not postgres_local，没有 collection error、漏跑或新 failure。Collector 分区另报告 3 subtests passed。

本命令为现场完整记录执行 2 次：第一次执行已完成但初始工具轮询未呈现 S7 最终摘要；第二次 fresh invocation 取得上述完整、exit-0 evidence。两次均未因测试 failure retry，也没有修改 runner 或 repository。

## Explicit shell-contract result

使用项目 .venv/bin/python 对 live scripts/run_non_db_pytest.py 做只读 AST/monkeypatch validation：

- subprocess.run() 调用数：1。
- 每个调用均显式传入 shell=False，且 AST value 是常量 False。
- _pytest_command() 返回参数 list；实际 monkeypatch 观察到 command 为 list。
- check=False 显式传入。
- 未传入 stdout、stderr、capture_output。
- 没有 shell wrapper、shell=True、/bin/sh、bash -c 或 sh -c。
- runner source 未排除 test_event_collector_reliability.py 或 test_snap7_reliability_integration.py；Collector partition 实际执行 81 tests。

静态和运行时结果：

    AST_EXPLICIT_SHELL_FALSE=PASS
    AST_SUBPROCESS_RUN_CALL_COUNT=1
    AST_COMMAND_LIST_CONTRACT=PASS
    AST_NO_SHELL_WRAPPER=PASS
    AST_RELIABILITY_TESTS_NOT_EXCLUDED=PASS
    NEGATIVE_EXPLICIT_SUBPROCESS_KWARGS=PASS
    NEGATIVE_OUTPUT_PASSTHROUGH=PASS

## Negative-case result

所有 negative validation 均使用项目 .venv/bin/python，只做 in-memory monkeypatch/AST inspection，不写入 repository：

    NEGATIVE_MISSING_ROOT=PASS
    NEGATIVE_NONZERO_AGGREGATE=PASS
      simulated [0, 1, 0, 0]
      PARTITION_EXIT_CODES=[0, 1, 0, 0]
      AGGREGATE_EXIT_CODE=1
      main() returns 1
    NEGATIVE_EXPLICIT_SUBPROCESS_KWARGS=PASS
      shell=False
      check=False
      cwd=/Users/chenjie/Documents/MES/edge-mes-demo
      env[PYTHONPATH]=collector:.
      no stdout/stderr/capture_output kwargs
    NEGATIVE_OUTPUT_PASSTHROUGH=PASS

第一次 harness loader 因动态测试模块未注册到 sys.modules 而退出；这是 harness 自身 setup error，不是项目 source/test evidence。修正 loader setup 后同一检查完整 exit 0；没有写入 repository，也没有改变 runner。

## Compose render result

命令：docker compose config

结果：exit code 0，无 config error。Collector rendered build：

    context: /Users/chenjie/Documents/MES/edge-mes-demo
    dockerfile: collector/Dockerfile

未执行任何 Compose service lifecycle：up、down、create、start、stop、restart、rm 均为 0。

## Image build identity

validation tag preflight 为 ABSENT。唯一一次 image build：

    docker build --pull=false \
      --file collector/Dockerfile \
      --tag edge-mes-demo-collector:d2-r7a-r4-r1-validation-20260724 \
      .

结果：exit code 0。

    IMAGE_ID: sha256:6e064bdc89b39afa1223aca9fbcd18add8c0cb9d0070bce6f227eb1581bba905
    OS: linux
    Architecture: arm64
    Size: 54425315 bytes

Build 使用当前 Colima local daemon，没有启动 Compose service 或 Collector main loop。一次带不存在 .Variant 字段的只读 inspect 模板曾返回 template error；随后使用有效字段重新取得上述 identity，不影响 build、image identity 或后续 container validation。

## Container import closure result

使用 validation image 执行：docker run --rm --network none --read-only，并只读挂载 config/ 到 /app/config:ro。结果：

    exit code: 0
    IMPORT_CLOSURE=PASS
    APP_MAIN_PATH=/app/app/main.py
    EVENT_COLLECTOR_PATH=/app/app/services/event_collector.py
    COMMON_STATION_EVENT_PATH=/app/common/station_event/__init__.py

import app.main、import app.services.event_collector、import common.station_event 均成功。命令没有调用 app.main.main()，没有启动 Collector loop，没有连接 DB/PLC，也没有访问网络。

## Container mapping result

同一隔离 command 完成：

    MAPPING_STATIC_INITIALIZATION=PASS
    line_id=LINE_001
    read-plan count=4
    resolved config hash=0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38

已执行 load_edge_mapping()、build_read_plans()、resolved config snapshot construction、runtime snapshot hash consistency assertion 与 non-empty plan assertion。

## Host mapping result

使用 env PYTHONPATH=collector:. .venv/bin/python 对同一 config/mapping.yaml 执行相同 static initialization：

    exit code: 0
    HOST_MAPPING_STATIC_INITIALIZATION=PASS
    line_id=LINE_001
    read-plan count=4
    resolved config hash=0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38

## Host/container consistency

host 与 container 完全一致：

    line_id: LINE_001 == LINE_001
    read-plan count: 4 == 4
    resolved config hash: 0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38 == 0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
    HOST_CONTAINER_CONSISTENCY=PASS

## Cleanup result

按允许范围删除仅由本 Thread 创建并核对过 image ID 的临时 tag/image：

    docker image rm edge-mes-demo-collector:d2-r7a-r4-r1-validation-20260724: exit 0
    validation tag: ABSENT
    VALIDATION_TAG_CLEANUP=PASS

没有执行 broad cleanup、prune 或删除其他 image。

## Exact allowlist audit

本 gate implementation/test set 准确为：

    collector/Dockerfile
    docker-compose.yml
    tests/test_collector_container_packaging.py
    scripts/run_non_db_pytest.py
    collector/tests/test_event_collector_reliability.py
    collector/tests/test_snap7_reliability_integration.py

本 Verification Thread 唯一新增路径：

    docs/reports/sprint4_d2_r7a_r4_r1_collector_package_closure_reverification.md

最终 audit：

    git diff --check: PASS
    git diff --cached --name-only: empty
    new report: untracked / unstaged / non-symlink
    implementation/test/config paths: not modified by Verification
    R4 and R4A existing reports: not modified by Verification
    external dirty artifacts: preserved, not cleaned, not staged

没有执行 git add、git commit、git push、git tag 或 git clean。

## Scope / explicitly not touched

未触碰或未授权：

- collector/app/**、common/**、api/**、s7_plc_sim/**、simulator/**
- config/mapping.yaml 及其他 config
- collector/Dockerfile、docker-compose.yml、全部 implementation/test source
- pytest.ini、DB/migrations、API、Dashboard、V-PLC/PLC
- existing reports、handoffs、governance/status/roadmap files
- SSH、remote Docker、remote mapping deployment
- Compose service lifecycle、Collector deployment/activation、rollback drill
- DB query/write、API request/mutation、production accepted-fact generation
- Git index/history mutation

Forbidden-action audit invocation counts：

    SSH / remote Docker / remote mapping deployment: 0
    Compose service lifecycle: 0
    Collector deployment / activation: 0
    DB query/write / API request/mutation: 0
    V-PLC / PLC external request or mutation: 0
    production data generation: 0
    Git stage / commit / push / tag / clean: 0
    packaging regression: 1
    focused suite: 1
    reliability target: 1
    canonical aggregate runner: 2 (second invocation was the complete recorded evidence)
    negative AST/monkeypatch validation: 2 attempts, one harness setup failure then one complete pass
    docker compose config: 1
    validation image build: 1
    container import/static mapping command: 1
    host static mapping command: 1
    validation image cleanup: 1

## Blockers

无 blocker。所有 Conclusion Rules 所列 required PASS 条件均已取得本轮 evidence；没有 test failure、collection error、漏跑、runner contract failure、Compose/image/container/mapping failure、cleanup failure、staged set 或 unauthorized modification。

## Recommendations

1. 由 ChatGPT PM 对本报告执行 intake，并在保持当前 exact allowlist 与 external dirty boundary 的前提下，另行决定是否授权 exact-path Git closeout。
2. 即使本 gate PASS，也不得从本报告推导 D2-R7B、config deployment、Collector activation、production accepted-fact generation 或 D3 authorization。

## Next gate

    Current gate: D2-R7A-R4-R1 PASS
    Next action: PM intake and separate exact-path Git closeout decision
    D2-R7B / deployment / activation / D3: not authorized by this report

## MVP 路径一致性

    当前任务是否仍直接服务于已批准 MVP：yes
    对应 MVP 交付物或验收声明：Collector image package closure、可信 non-DB regression boundary 与静态 mapping startup compatibility
    是否引入超出 MVP 的产品能力、威胁模型、证据体系或基础设施：no
    是否出现任务膨胀或验证框架替代产品交付：no

## Thread 输出 / 上下文评估

    本次输出长度：长
    当前 Thread 是否建议继续：no
    下一轮是否建议新开 Thread：yes
    理由：完整 fresh Verification matrix、image/container closure、cleanup、exact audit 与 durable report 已完成；后续由 PM intake 决定 Git closeout，不应在本 Thread 继续执行。
