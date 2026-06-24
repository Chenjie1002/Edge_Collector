# Architecture / Integration Context Restore

更新时间：2026-06-23
用途：恢复 Phase-2 Sprint 2 Generic Station Event Model implementation 上下文
当前 Reliability Gate：**PASS WITH RECOMMENDATIONS**
当前 Reliability focused Gate：**PASS**
当前 Data Quality targeted Gate：**PASS WITH RECOMMENDATIONS；DQ-F1～DQ-F3 CLOSED**
当前 Verification targeted Gate：**PASS WITH RECOMMENDATIONS；V-DQ1～V-DQ4 PASS**
Remaining Reliability / Data Quality / Verification blocker：**none**

## 1. 一句话恢复

Phase-1 已最终验收 PASS；Phase-2 Architecture Planning 已冻结并 push；Sprint 1
Flexible Line Configuration 已通过 Independent Gate Review，并以 commit `b9f6a69`
完成 final commit / push；docs hygiene commit 为 `4215b7c`；Sprint 2 planning freeze
commit 为 `45fa2a8`。Reliability N8 定向复验结论为
`PASS WITH RECOMMENDATIONS`；N8 已 CLOSED，N6、N7 与既有 CLOSED items 均无回归，
且无新 Reliability blocker。Data Quality focused re-review 与 V10/R5 sanity check
均为 `PASS WITH RECOMMENDATIONS`；Verification focused re-review 也为
`PASS WITH RECOMMENDATIONS`。ChatGPT PM 已基于 `e9abe45` 授权 implementation；
Generic Station Event Model MVP package 与 tests 已完成。Verification implementation
review 发现 B1~B5；Verification 已通过 B5-final re-review 并关闭 B1~B5。Reliability
focused review 已关闭 R-B2/R-B3/R-B4 与 B5 regression。DQ-F1～DQ-F3 repair、
Data Quality targeted re-review 与 Verification targeted sanity check 均已完成，
remaining blocker 为 none。Sprint 2 implementation 已通过 commit
`17cf5d2 Implement Sprint 2 generic station event model` push 到 `origin/main`；尚未
进入任何 runtime integration。

## 2. 当前 Git 与发布状态

```text
branch: main
HEAD: 17cf5d2
origin/main: 17cf5d2
latest commit: 17cf5d2 Implement Sprint 2 generic station event model
Sprint 1 implementation: b9f6a69 Phase 2 Sprint 1 flexible line configuration
Sprint 1 docs hygiene: 4215b7c Finalize Sprint 1 architecture handoff and review history
tags: phase1-pass-20260619
Phase-2 tag: not created
remote deploy: not performed
rollback drill: not performed
Sprint 2 implementation: committed/pushed
common/station_event: present
tests/test_station_event_model.py: present
Reliability focused review: PASS
Data Quality targeted re-review: PASS WITH RECOMMENDATIONS
Verification DQ-F1-DQ-F3 targeted sanity check: PASS WITH RECOMMENDATIONS
Verification contract Gate: PASS WITH RECOMMENDATIONS
Verification implementation review: PASS; B1-B5 CLOSED
remaining Reliability blocker: none
remaining Data Quality blocker: none
remaining Verification blocker: none
latest pushed commit: 17cf5d2
uncommitted implementation/tests/report changes: no tracked diff
required sequence: docs-only closeout hygiene -> PM authorization before Sprint 3 runtime work
focused station_event tests: 128 passed
broader tests: 216 passed
git diff --check: PASS
Collector/API/DB/Dashboard/V-PLC integration: none
migration: none
commit/push: complete at 17cf5d2
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

PM 在 planning freeze 时冻结、现已由 implementation 实现：

- `common/station_event/` 为 implementation 路径，当前 working tree 已存在。
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

## 9. 历史 Verification HOLD 与后续关闭

> 本节记录 implementation 前的历史 Gate。当前控制状态见文件顶部与第 15 节。

Reliability 已验证且不重开：

1. `validated_nok_detail` positive evidence 可合法构造。
2. Evidence-type comparison 只有一个可执行解释。
3. 三个 N8 negative examples 均有唯一 reject 结果。
4. N6、N7、UNKNOWN、payload、event-fields 无回归。

Data Quality R1~R5 focused re-review 当时已 `PASS WITH RECOMMENDATIONS`。Verification
曾留下 V6 error mapping、V7 raw variant decision 与 V10 lifecycle derived output；
Architecture 后续完成三个最小合同修订并关闭这些项。

该历史 sequence 已完成，不再是当前待办。

## 10. 下一 Architecture Thread 恢复顺序

1. `docs/thread_handoff/architecture.md`
2. `docs/reports/architecture_context_restore.md`
3. `docs/reports/sprint2_station_event_reliability_review.md`
4. `docs/reports/sprint2_generic_station_event_model_plan.md`
5. `docs/contracts/station_event_model.md`
6. `docs/contracts/line_configuration.md`
7. `docs/contracts/dynamic_station_model.md`
8. `docs/reports/sprint1_independent_gate_review.md`

第一任务是以 `17cf5d2` 为当前 source of truth 做 docs-only closeout hygiene；任何
Sprint 3 runtime work、migration、tag、deploy 或 rollback drill 都需要 PM 单独授权。

## 11. 工作树与提交边界

当前 HEAD/origin/main 和最新 pushed commit 均为 `17cf5d2`；tracked working tree 无
implementation/tests/report diff。当前 tag 仍只有 `phase1-pass-20260619`，未 deploy、
未 rollback drill。

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
- Sprint 2 已有独立 `common/station_event/` 与直接相关 tests，但没有 migration 或
  runtime integration。
- implementation 已完成 commit/push，但不等于 runtime integration 已开始。
- review blocker 已关闭不等于已获得 commit/push 授权。
- 当前 Reliability Gate 为 `PASS WITH RECOMMENDATIONS`。
- 当前 Data Quality Gate 为 `PASS WITH RECOMMENDATIONS`。
- 当前 Verification contract Gate 为 `PASS WITH RECOMMENDATIONS`；V6/V7/V10 已关闭。
- 当前 Verification implementation review 为 `PASS`；B1~B5 CLOSED。
- 当前 Reliability focused review 为 `PASS`。
- 当前 Data Quality targeted re-review 为 `PASS WITH RECOMMENDATIONS`。
- 当前 Verification DQ-F1～DQ-F3 targeted sanity check 为
  `PASS WITH RECOMMENDATIONS`。
- 当前三个 review domain 均无 remaining blocker。
- 当前没有 Phase-2 tag，也没有 Sprint 2 deploy / rollback drill。

## 13. Sprint 2 implementation evidence（更新至 2026-06-23 final targeted reviews）

```text
implementation baseline: e9abe45 Finalize Sprint 2 station event review gates
implementation commit: 17cf5d2 Implement Sprint 2 generic station event model
package: common/station_event/
focused tests: 128 passed
root tests regression: 216 passed
compileall: PASS
git diff --check: PASS
commit/push: complete at 17cf5d2
```

Implementation report：
`docs/reports/sprint2_generic_station_event_model_implementation_report.md`。

仍未修改或接入 Collector、API、DB、Dashboard、Grafana、V-PLC；未创建 migration、
tag，未 deploy，未执行 rollback drill。

## 14. Implementation repair handoff

本轮只修复 Verification implementation review B1~B5：

- historical config snapshot station/profile lineage fail-closed。
- `30003` parent station/cycle identity isolation。
- secondary NOK code 去重。
- `validated_nok_detail` canonical NOK parent。
- raw WebP/PDF/generic binary base64、binary MIME/key hint、约 7 KiB 周期性单行
  fragment rejection，以及 binary/base64-overlimit forbidden precedence。
- `30003` same-config skip parent isolation。
- `validated_nok_detail` authoritative canonical parent、same-config 与
  primary code/origin relation。
- canonical parent `correlation.event_role=production_result` enforcement。

新增回归测试后 focused 为 `128 passed`，root `tests/` 为 `216 passed`。Verification
B1~B5、Reliability R-B2/R-B3/R-B4/B5 regression、Data Quality DQ-F1～DQ-F3 与
Verification V-DQ1～V-DQ4 均已关闭。Sprint 2 implementation 已完成 commit/push；
未获 PM 明确授权前不得进入 integration。

## 15. Data Quality repair 与最终 targeted Gate context（2026-06-23）

Data Quality focused implementation review 曾返回 HOLD，findings 为 DQ-F1～DQ-F3；
Architecture 随后完成最小 implementation repair：

```text
DQ-F1 parent lineage:
profile_id + station_type exact comparison

DQ-F2 cited detail authority:
accepted station_nok
+ correlation.event_role=nok_detail
+ ordinary stateless canonical validation
+ accepted canonical NOK parent replay

DQ-F3 raw authority:
raw_payload -> callable historical decoder required
missing/exception -> RAW_PARSE_ERROR
raw-only/mismatch -> RAW_NORMALIZED_MISMATCH
```

projection isolation：

- rejected production event 不产生 authoritative production outcome。
- rejected detail 不产生 defect/operator/Pareto projection。
- `projection_eligible=false`。

duplicate/conflict/raw_variant 规则未修改。raw_variant fixture 已改为 normalized payload
与 historical decoder 均存在，两个 raw variant 解码为相同 canonical payload。

当前最终状态：

```text
Reliability focused review: PASS
Data Quality targeted re-review: PASS WITH RECOMMENDATIONS
Verification DQ-F1-DQ-F3 targeted sanity check: PASS WITH RECOMMENDATIONS
Remaining Reliability blocker: no
Remaining Data Quality blocker: no
Remaining Verification blocker: no
focused station_event tests: 128 passed
broader tests: 216 passed
git diff --check: PASS
```

Sprint 2 implementation 已完成 commit/push。Collector/API/DB/Dashboard/V-PLC
integration、migration、tag、deploy、rollback drill 均未进入；后续必须由 PM 单独
授权。
