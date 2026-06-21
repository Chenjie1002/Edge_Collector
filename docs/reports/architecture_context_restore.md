# Architecture / Integration Context Restore

更新时间：2026-06-21
用途：恢复 Phase-2 Sprint 2 Verification HOLD 后 V6/V7/V10 docs-only 修订上下文
当前 Reliability Gate：**PASS WITH RECOMMENDATIONS**
当前 Data Quality Gate：**PASS WITH RECOMMENDATIONS**
当前 Verification Gate：**HOLD / CHANGES REQUIRED**

## 1. 一句话恢复

Phase-1 已最终验收 PASS；Phase-2 Architecture Planning 已冻结并 push；Sprint 1
Flexible Line Configuration 已通过 Independent Gate Review，并以 commit `b9f6a69`
完成 final commit / push；docs hygiene commit 为 `4215b7c`；Sprint 2 planning freeze
commit 为 `45fa2a8`。Reliability N8 定向复验结论为
`PASS WITH RECOMMENDATIONS`；N8 已 CLOSED，N6、N7 与既有 CLOSED items 均无回归，
且无新 Reliability blocker。Data Quality focused re-review 为
`PASS WITH RECOMMENDATIONS`；Verification 当前 `HOLD / CHANGES REQUIRED` 仅剩
V6/V7/V10。Architecture 已完成三个最小 docs-only 修订，等待 Verification focused
re-review；implementation 尚未开始。

## 2. 当前 Git 与发布状态

```text
branch: main
HEAD: 60adac2
origin/main: 60adac2
latest commit: 60adac2 Address Sprint 2 station event reliability review
Sprint 1 implementation: b9f6a69 Phase 2 Sprint 1 flexible line configuration
Sprint 1 docs hygiene: 4215b7c Finalize Sprint 1 architecture handoff and review history
tags: phase1-pass-20260619
Phase-2 tag: not created
remote deploy: not performed
rollback drill: not performed
Sprint 2 planning: Verification V6/V7/V10 docs-only revision in working tree
Reliability focused re-review: PASS WITH RECOMMENDATIONS
Data Quality focused re-review: PASS WITH RECOMMENDATIONS
Verification Gate: HOLD / CHANGES REQUIRED, V6/V7/V10
latest pushed commit: 60adac2
uncommitted docs changes: yes
required sequence: Verification focused re-review -> ChatGPT PM authorization
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

## 8. Sprint 2 planning 与 N8 定向复验

```text
Sprint 2: Generic Station Event Model
```

当前 planning 产出：

- `docs/contracts/station_event_model.md`
- `docs/reports/sprint2_generic_station_event_model_plan.md`
- `docs/reports/sprint2_station_event_reliability_review.md`

Reliability 当前控制结论：

```text
CLOSED: UNKNOWN diagnostic context
CLOSED: payload limits
CLOSED: event required fields
CLOSED: N6 cycle-role uniqueness / content fingerprint
CLOSED: N7 stateful relation / detail-set constraints
CLOSED: N8 validated_nok_detail evidence comparison
NEW BLOCKER: none
GATE: PASS WITH RECOMMENDATIONS
```

Architecture N8 最小合同返修已明确：

1. `canonical_station_result` evidence 比较 cited result 自身的 `result=nok`。
2. `validated_nok_detail` 自身继续禁止 `result`。
3. Detail evidence 的 `upstream_result=nok` 与 accepted canonical parent
   `station_result.result` 比较。
4. Detail 的 code/origin 只承担 NOK detail 语义，不替代 parent result。
5. 增加合法正例以及 detail 自带 result、parent result=ok、technical failure
   impersonation 三个 reject 负例。
6. Technical failure 继续禁止支持 `30003/UPSTREAM_NOK_SKIPPED`。

保持 CLOSED、未退化：

- UNKNOWN 仍只允许 heartbeat，并要求 strict `diagnostic_context`。
- payload/raw 继续保持 16/64 KiB、depth/key/array/string/JSON-type/raw-encoding 与
  超限 reject。
- event fields 继续保持 required/optional/forbidden、absent/null 与 `profile_id` 规则。

本阶段只完成 planning + handoff，不授权 coding、migration、部署或跨模块修改。

PM 已冻结：

- `common/station_event/` 为后续 implementation 路径，但当前不存在实现包。
- MVP event：cycle start、cycle complete、result、NOK、heartbeat。
- frozen dataclass，不使用 Pydantic。
- accepted envelope event identity 为 UUIDv4；UUIDv5 仅 validator 外部
  helper/snapshot；UUIDv7 future。physical cycle/detail keys 不依赖 source ID。
- 所有有效 event 强制 SHA-256 `config_hash`。
- normalized/raw payload 上限 16/64 KiB，并有结构资源限制。
- `unknown` 仅限有 strict diagnostic context 的 heartbeat。
- 独立 `nok_origin`；`30003` 与 `system_reserved` 双向绑定。
- `payload` optional、explicit null reject、`profile_id` 对齐 Sprint 1 cycle profile。
- fact key、cycle/detail uniqueness、content fingerprint 和 stateful disposition 按合同
  分工冻结。

## 9. Verification HOLD 与当前后续 Gate

Reliability 已验证且不重开：

1. `validated_nok_detail` positive evidence 可合法构造。
2. Evidence-type comparison 只有一个可执行解释。
3. 三个 N8 negative examples 均有唯一 reject 结果。
4. N6、N7、UNKNOWN、payload、event-fields 无回归。

Data Quality R1~R5 focused re-review 已 `PASS WITH RECOMMENDATIONS`。Verification
remaining blockers 为 V6 error mapping、V7 raw variant decision 与 V10 lifecycle
derived output。Architecture 已完成三个最小合同修订。

下一步必须由 Verification focused re-review；Data Quality 仅定向确认 V10/R5。
ChatGPT PM 授权前，implementation 仍禁止。

## 10. 下一 Architecture Thread 恢复顺序

1. `docs/thread_handoff/architecture.md`
2. `docs/reports/architecture_context_restore.md`
3. `docs/reports/sprint2_station_event_reliability_review.md`
4. `docs/reports/sprint2_generic_station_event_model_plan.md`
5. `docs/contracts/station_event_model.md`
6. `docs/contracts/line_configuration.md`
7. `docs/contracts/dynamic_station_model.md`
8. `docs/reports/sprint1_independent_gate_review.md`

第一任务是交 Verification focused re-review V6/V7/V10，并由 Data Quality 定向确认
V10/R5；之后交 ChatGPT PM 汇总授权，不能直接进入 implementation。

## 11. 工作树与提交边界

当前 HEAD/origin/main 和最新 pushed commit 均为 `60adac2`；工作树存在未提交文档
修改。当前 tag 仍只有 `phase1-pass-20260619`，未 deploy、未 rollback drill。

本轮 Architecture 允许修改：

- `docs/contracts/station_event_model.md`
- `docs/contracts/dynamic_station_model.md`
- `docs/reports/sprint2_generic_station_event_model_plan.md`
- `docs/thread_handoff/architecture.md`
- `docs/reports/architecture_context_restore.md`
- 必要时索引文件

未来 docs commit 必须精确 add，禁止 `git add .`，并排除：

- `docs/20260620_03_Edge MES Demo — ChatGPT PM Handoff.md`
- `docs/Edge MES Demo 当前进度报告.md`
- `docs/superpowers/`

Data Quality 与 Reliability 报告由各自 Thread 维护，本轮不得修改正文。

## 12. 禁止误读

- Sprint 1 当前不是 HOLD。
- Sprint 1 不需要继续 Contract Hardening。
- Sprint 1 可表达 20 stations，不代表 Raspberry Pi capacity certification。
- line config 尚未成为运行时真源。
- Edge 不是设备控制系统。
- Sprint 2 只有合同与计划草案，没有代码、tests、migration 或 runtime integration。
- PM 决策冻结不等于 implementation authorization。
- Reliability blocker 已关闭不等于 Sprint 2 implementation 已授权。
- 当前 Reliability Gate 为 `PASS WITH RECOMMENDATIONS`。
- 当前 Data Quality Gate 为 `PASS WITH RECOMMENDATIONS`。
- 当前 Verification Gate 仍为 `HOLD / CHANGES REQUIRED`；Architecture 自评修订完成
  不等于 focused re-review 已通过。
- 当前没有 Phase-2 tag，也没有 Sprint 2 deploy / rollback drill。
