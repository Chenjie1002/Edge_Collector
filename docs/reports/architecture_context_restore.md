# Architecture / Integration Context Restore

更新时间：2026-06-20
用途：恢复 Phase-2 Sprint 2 planning freeze 阶段的 Architecture / Integration 上下文
当前 Gate：**PASS**

## 1. 一句话恢复

Phase-1 已最终验收 PASS；Phase-2 Architecture Planning 已冻结并 push；Sprint 1
Flexible Line Configuration 已通过 Independent Gate Review，并以 commit `b9f6a69`
完成 final commit / push；docs hygiene commit 为 `4215b7c`。当前正在进行 Sprint 2
Generic Station Event Model planning freeze；PM 决策已固化，三方 review 尚未执行，
implementation 尚未开始。

## 2. 当前 Git 与发布状态

```text
branch: main
HEAD: 4215b7c
origin/main: 4215b7c
latest commit: 4215b7c Finalize Sprint 1 architecture handoff and review history
Sprint 1 implementation: b9f6a69 Phase 2 Sprint 1 flexible line configuration
tags: phase1-pass-20260619
Phase-2 tag: not created
remote deploy: not performed
rollback drill: not performed
Sprint 2 planning: PM decisions frozen
required reviews: Reliability -> Data Quality -> Verification
Sprint 2 implementation: not started
```

## 3. Sprint 1 最终状态

```text
Sprint: Phase-2 Sprint 1 Flexible Line Configuration
Gate: PASS
runtime integration: none
```

权威文件：

- `docs/contracts/line_configuration.md`
- `docs/reports/sprint1_flexible_line_configuration_report.md`
- `docs/reports/sprint1_contract_hardening_report.md`
- `docs/reports/sprint1_independent_gate_review.md`
- `docs/thread_handoff/verification.md`
- `docs/reports/verification_context_restore.md`

## 4. 已交付能力

- strict YAML structure 与 unknown-field rejection。
- centralized allowed keys、enum 和 hard limits。
- 3/10/20 station configuration examples。
- immutable line/PLC/station/mapping/Buffer/template/Profile/scenario models。
- Profile mode 与 production/simulation timing 分离。
- deterministic resolved config、canonical JSON 与 stable SHA-256。
- seed、test run、global NOK fallback 与 station override。
- payload/mapping 的基础 read-size/poll/direction/layout 字段。
- NOK permission 与 `30003` reserved semantics。
- RouteGraph、entry/terminal、disabled station 与 Buffer validation。
- hardware/load class 与静态 load estimate。
- Buffer `enabled` / `tracking_mode`。

## 5. 最终验证证据

```text
focused: 20 passed, 57 deselected
configuration: 77 passed
root: 88 passed
API: 5 passed
Collector: 12 passed, 3 subtests passed
V-PLC: 27 passed
compileall: PASS
YAML load/hash/load summary: PASS
diff check: PASS
```

三份 resolved config hash：

```text
demo_3_station.yaml    50b92c3ac72a746060d3ff47d141bde1e24d53e9b4b35b0afa0d0fc8a23968e1
demo_10_station.yaml   08b9b4de701ef665597b0351240cc46d83ee649a5299f3db8551201d2a35dee5
stress_20_station.yaml e3afc329d76d559a3f211d088cfe2a749367a18774949db35d2af8a364a1fcfb
```

## 6. 运行链路边界

`common.line_config` 尚未被 V-PLC、Collector、API、DB 或 Dashboard 消费。Sprint 1
没有修改 migration、Docker、`.env`、volume 或远程 Raspberry Pi。

因此：

```text
remote verification: NOT REQUIRED
rollback drill: NOT REQUIRED
```

## 7. 历史 review

以下文件保存返修前的独立审计证据，正文中的 HOLD/FAIL 是历史状态：

- `docs/reports/sprint1_reliability_config_review.md`
- `docs/reports/sprint1_verification_matrix.md`

最终状态以以下文件为准：

- `docs/reports/sprint1_contract_hardening_report.md`
- `docs/reports/sprint1_independent_gate_review.md`

## 8. Sprint 2 planning

```text
Sprint 2: Generic Station Event Model
```

当前 planning 产出：

- `docs/contracts/station_event_model.md`
- `docs/reports/sprint2_generic_station_event_model_plan.md`

合同已冻结 event envelope、五类 MVP event type、result/NOK/nok_origin/source authority、
config lineage、payload/raw、timestamp/order/idempotency、validation 与 canonical
serialization。planning report 定义了后续 Reliability、Data Quality、Verification 和
Architecture 任务包。

本阶段只完成 planning + handoff，不授权 coding、migration、部署或跨模块修改。

PM 已冻结：

- `common/station_event/` 为后续 implementation 路径，但当前不存在实现包。
- MVP event：cycle start、cycle complete、result、NOK、heartbeat。
- frozen dataclass，不使用 Pydantic。
- UUIDv4 runtime 默认、UUIDv5 test-only、UUIDv7 future recommendation。
- 所有有效 event 强制 SHA-256 `config_hash`。
- normalized/raw payload 上限 16/64 KiB。
- `unknown` 仅限受控 heartbeat/diagnostic/future fault 语境。
- 独立 `nok_origin`；`30003` 只与 `system_reserved` 组合。

## 9. 下一 Architecture Thread 恢复顺序

1. `docs/thread_handoff/architecture.md`
2. `docs/reports/architecture_context_restore.md`
3. `docs/reports/sprint2_generic_station_event_model_plan.md`
4. `docs/contracts/station_event_model.md`
5. `docs/contracts/line_configuration.md`
6. `docs/contracts/dynamic_station_model.md`
7. `docs/reports/sprint1_independent_gate_review.md`

第一任务是按冻结顺序启动 Reliability review；完成后交 Data Quality，再由
Verification 建 Gate matrix。ChatGPT PM 汇总三方结论并授权前，不要准备或执行代码
implementation，不要创建 package，也不要把 planning freeze 误读为 implementation
已完成。

## 10. 禁止误读

- Sprint 1 当前不是 HOLD。
- Sprint 1 不需要继续 Contract Hardening。
- Sprint 1 可表达 20 stations，不代表 Raspberry Pi capacity certification。
- line config 尚未成为运行时真源。
- Edge 不是设备控制系统。
- Sprint 2 只有合同与计划草案，没有代码、tests、migration 或 runtime integration。
- PM 决策冻结不等于 implementation authorization。
- 当前没有 Phase-2 tag，也没有 Sprint 2 deploy / rollback drill。
