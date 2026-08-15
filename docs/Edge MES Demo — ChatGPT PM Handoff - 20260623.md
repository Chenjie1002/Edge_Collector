# Edge MES Demo — ChatGPT PM Handoff

日期：2026-06-23
交接对象：新的 ChatGPT PM 窗口
当前阶段：Phase-2 Sprint 2 已完成 implementation commit/push；准备 Sprint 2 closeout 与 Sprint 3 integration boundary planning
当前最高优先级：不要直接进入 runtime integration，先做 Sprint 2 收口确认与 Sprint 3 集成边界规划

---

## 1. 新 ChatGPT PM 的角色

你现在接手的是 Edge MES Demo 项目的 ChatGPT PM / 技术项目经理角色。

ChatGPT PM 职责：

* 不直接修改代码。
* 不直接操作仓库，除非用户明确要求并通过 Devspace 只读/有限操作核验。
* 不直接 commit / push / tag / deploy。
* 负责拆任务、写 Codex Prompt、判断优先级、审核 Codex 返回结果。
* 负责决定任务交给哪个 Codex Thread。
* 负责控制边界，避免 Codex 跨阶段扩大范围。
* 负责在 review / repair / commit / implementation / integration 各阶段之间设置 gate。
* 负责在 Thread 过长时要求 handoff，并安排新 Thread 接手。

新增 PM 工作规则：

```text
PM 发布每个 Codex 任务前，必须评估工作量与上下文风险：

- 工作量大 / gate 性质强 / 需要跨多个文件读取 / 需要运行完整测试 /
  需要独立审查 / 上一 Thread 上下文已长：
  → 建议新开 Thread，并提供自包含 prompt。

- 工作量小 / 单文件小修 / 纯文档状态同步 / 同一 repair 内的立即 follow-up /
  当前 Thread 上下文仍清晰：
  → 可以留在当前 Thread。

默认：
review、focused re-review、final pre-commit audit、HOLD 后 repair、跨角色 gate 判断，优先新开 Thread。
小范围补充说明、whitespace-only repair、单点文档修正，可以留在当前 Thread。
```

Codex Thread 分工：

* Architecture / Integration：规划、合同、实现、修复、handoff、最终 docs/code allowlist commit-push。
* Reliability：可靠性、控制边界、资源、幂等、错误语义审计。
* Data Quality：追溯完整性、数据质量、结果投影、payload/raw 一致性审计。
* Verification：Gate matrix、独立复验、测试覆盖、scope/isolation 审计。
* 后续可能新增 Dashboard / Frontend Thread，但当前还没进入 Dashboard implementation。

---

## 2. 项目总体边界

项目：Edge MES Demo

定位：

* 非侵入式 Edge MES / Traceability / OEE Demo。
* PLC 仍然是设备控制大脑。
* HMI / PLC 定义 Hold、Rework、Skip、Manual NOK 等现场流程。
* Edge Collector 只负责采集、解析、落库。
* PostgreSQL 负责结构化存储与追溯。
* FastAPI 负责查询与服务接口。
* Grafana / Trace / Dashboard 负责展示与分析。
* Edge 不替代 PLC 控制逻辑。
* Edge 不主动决定生产控制流程。

当前必须守住：

* Sprint 2 独立 station event model 已完成并 push。
* 这不等于已经接入 Collector / API / DB / Dashboard / V-PLC。
* 当前不得直接开始 runtime integration，除非先完成 Sprint 3 integration boundary plan。
* 当前不得创建 Phase-2 tag。
* 当前不得 deploy。
* 当前不得 rollback drill。
* 当前不得新增 DB migration，除非进入明确授权的 DB integration Sprint。
* 当前不得让 Codex 顺手修改 Phase-1 默认行为。

---

## 3. 当前 Git 状态，已核验

本地仓库路径：

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

当前状态，Devspace 只读核验：

```text
git status: clean

HEAD:
17cf5d22ae2875f1048acf683cb43309f724cbb9

origin/main:
17cf5d22ae2875f1048acf683cb43309f724cbb9

latest log:
17cf5d2 Implement Sprint 2 generic station event model
e9abe45 Finalize Sprint 2 station event review gates
60adac2 Address Sprint 2 station event reliability review
45fa2a8 Freeze Sprint 2 station event planning
4215b7c Finalize Sprint 1 architecture handoff and review history

tag:
phase1-pass-20260619
```

当前结论：

```text
Sprint 2 Generic Station Event Model implementation：COMMITTED / PUSHED
Commit：17cf5d2 Implement Sprint 2 generic station event model
Remaining blocker：none
Working tree：clean
Phase-2 tag：未创建
deploy / rollback drill：未执行
runtime integration：未开始
```

重要提醒：

部分已提交文档是在 final pre-commit audit 阶段写成的，可能仍有“implementation complete in working tree; not committed/pushed”这类提交前表述。当前真实 source of truth 是 Git 状态：`HEAD == origin/main == 17cf5d2`，工作树 clean。后续如果做 Sprint 2 closeout，可用 docs-only 方式更新这些 post-commit 状态描述，但不要把这误判成 Sprint 2 未提交。

---

## 4. 已完成阶段总览

### Phase-1

状态：PASS。

已完成：

* 单机 Demo 最终验收 PASS。
* GitHub freeze / tag / release note / push report 已完成。
* tag：`phase1-pass-20260619`
* Raspberry Pi 远程部署曾通过验证，但当前 Sprint 2 不涉及远程部署。

### Phase-2 Architecture Planning

状态：完成。

主要文档：

```text
docs/reports/phase2_flexible_architecture_plan.md
docs/contracts/line_configuration.md
docs/contracts/dynamic_station_model.md
docs/reports/dashboard_tech_stack_plan.md
docs/contracts/dashboard_api_contract.md
docs/reports/phase2_sprint_plan.md
docs/reports/phase2_thread_task_plan.md
docs/roadmap.md
docs/reports/phase2_architecture_freeze_report.md
```

### Sprint 1：Flexible Line Configuration

最终状态：PASS。

关键 commits：

```text
b9f6a69 Phase 2 Sprint 1 flexible line configuration
4215b7c Finalize Sprint 1 architecture handoff and review history
```

主要交付：

```text
common/line_config/
config/lines/demo_3_station.yaml
config/lines/demo_10_station.yaml
config/lines/stress_20_station.yaml
tests/test_line_config.py
```

Sprint 1 关键结论：

* Gate 已 PASS。
* 所有 Sprint 1 blocker 已关闭。
* Phase-1 默认行为未受影响。
* 未创建 Phase-2 tag。
* 未 deploy。
* 未 rollback drill。

---

## 5. Sprint 2 当前最终状态

Sprint 2 名称：Phase-2 Sprint 2：Generic Station Event Model

当前最终 commit：

```text
17cf5d2 Implement Sprint 2 generic station event model
```

当前真实状态：

```text
Implementation：completed
Commit/push：completed
HEAD/origin/main：17cf5d22ae2875f1048acf683cb43309f724cbb9
Working tree：clean
Reliability：PASS
Data Quality：PASS WITH RECOMMENDATIONS
Verification：PASS WITH RECOMMENDATIONS
Remaining blocker：none
Runtime integration：not started
Tag/deploy/rollback drill：not performed
```

Sprint 2 已交付文件：

```text
common/station_event/
  __init__.py
  constants.py
  errors.py
  fingerprint.py
  lifecycle.py
  models.py
  projection.py
  serialization.py
  validation.py

tests/test_station_event_model.py

docs/reports/sprint2_generic_station_event_model_implementation_report.md
docs/thread_handoff/architecture.md
docs/reports/architecture_context_restore.md
docs/reports/sprint2_station_event_reliability_review.md
docs/reports/sprint2_station_event_data_quality_review.md
docs/reports/sprint2_station_event_verification_matrix.md
.gitignore
```

`.gitignore` 本轮新增了本地 PM/Codex artifact ignore 规则，防止误提交：

```text
docs/20260620_03_Edge MES Demo — ChatGPT PM Handoff.md
docs/Edge MES Demo 当前进度报告.md
docs/superpowers/
```

---

## 6. Sprint 2 已实现能力

Sprint 2 implementation 已覆盖：

* MVP event types 五类：

  * `station_cycle_start`
  * `station_cycle_complete`
  * `station_result`
  * `station_nok`
  * `station_heartbeat`
* future types 仅 reserved，不实现。
* frozen dataclass model。
* nested mutation isolation。
* validator / serializer separation。
* normalized payload / raw payload limits。
* raw content authority validation。
* fingerprint / idempotency：

  * fact fingerprint
  * content fingerprint
  * raw evidence fingerprint
  * duplicate / conflict / raw_variant
* NOK policy：

  * `station_result(result=NOK)` 是唯一 canonical production result。
  * `station_nok` 是 detail companion。
  * `30003` system-reserved skip relation 隔离。
  * primary / secondary detail relation。
* lifecycle derived output 八字段。
* projection eligibility。
* config / lineage fields。
* historical resolved config snapshot lookup / validation。
* parent relation authority。
* raw evidence fail-closed。

已知限制：

* 这是离线 contract package。
* 尚未接入 Collector runtime。
* 尚未接入 PostgreSQL persistence。
* 尚未接入 FastAPI。
* 尚未接入 Dashboard / Trace。
* 尚未实现 retry、quarantine、registry 或 runtime adapter。
* 接入 JavaScript/PostgreSQL 前建议补充跨运行时 JCS exact-byte fixtures。

---

## 7. Sprint 2 review / repair 历史摘要

### 7.1 Reliability

最终状态：PASS。

过程中曾有 blocker：

* R-B2：跨 config accepted skip parent 支持 `30003`。
* R-B4：canonical parent authority/config/code/origin/role 不完整。
* 后续又发现 canonical parent `event_role=production_result` 未强制。

最终修复：

* 30003 parent 增加 same-config 校验。
* canonical parent matcher 校验：

  * authoritative PLC/V-PLC
  * config
  * primary code/origin
  * secondary origin
  * `event_role=production_result`
* 非 production_result parent 返回 fail-closed。
* rejected event 不产生 production outcome、defect detail 或 projection。

最终测试曾达到：

```text
focused station_event: 119 passed
broader tests: 207 passed
```

后续 Data Quality repair 增加测试后，最终 suite 变为：

```text
focused station_event: 128 passed
broader tests: 216 passed
```

### 7.2 Data Quality

Data Quality focused implementation review 曾 HOLD。

HOLD blocker：

```text
DQ-F1 parent snapshot lineage 不完整：
_parent_matches() 未比较 profile_id / station_type。

DQ-F2 compatibility cited detail 可成为 validated evidence：
cited detail 未强制 event_role=nok_detail，也未重放 canonical detail validation。

DQ-F3 raw authority fail-open：
raw_payload 存在但 snapshot 无 decoder 时，raw-only / mismatch event 可 accepted 并产生 outcome。
```

Architecture minimal repair 后：

* DQ-F1：

  * parent/detail `profile_id` exact match。
  * parent/detail `station_type` exact match。
* DQ-F2：

  * cited detail 必须 `correlation.event_role == "nok_detail"`。
  * cited detail 必须通过 historical canonical validation。
  * cited detail replay accepted parent relation。
* DQ-F3：

  * `raw_payload` present 时 snapshot 必须有 callable `decode_raw_payload`。
  * 缺 decoder / decoder 异常：`RAW_PARSE_ERROR`。
  * raw-only / raw-normalized mismatch：`RAW_NORMALIZED_MISMATCH`。
  * rejected raw evidence 不产生 authoritative projection。

Data Quality targeted re-review 结论：

```text
PASS WITH RECOMMENDATIONS

DQ-F1 parent profile/station_type lineage: CLOSED
DQ-F2 cited detail role/canonical validation: CLOSED
DQ-F3 raw authority fail-closed: CLOSED
R3 raw evidence / fingerprint / projection authority chain: CLOSED
Remaining Data Quality blocker: no
```

非阻塞建议：

* 后续可补充具名 regression：

  * non-accepted cited detail
  * raw-only + callable decoder

### 7.3 Verification

Verification targeted relation sanity check 曾 PASS。

后续 Data Quality repair 后，Verification DQ-F1～DQ-F3 targeted sanity check 结论：

```text
PASS WITH RECOMMENDATIONS

V-DQ1 parent profile/station_type lineage: PASS
V-DQ2 validated cited detail canonical authority: PASS
V-DQ3 raw authority fail-closed: PASS
V-DQ4 targeted regression / isolation: PASS
Remaining Verification blocker: no
```

确认：

* repair 未修改 contracts。
* repair 未触碰 Collector/API/DB/Dashboard/V-PLC。
* repair 未新增 migration。
* repair 未 tag/deploy/rollback drill。
* repair 未 commit/push，直到 PM final allowlist 授权后才 commit/push。

---

## 8. 最终 commit/push 过程摘要

Final pre-commit audit 曾 HOLD 一次：

* 原因不是代码问题，而是两份 Architecture 权威文档状态漂移：

  * `docs/thread_handoff/architecture.md`
  * `docs/reports/architecture_context_restore.md`
* 修复后 re-audit PASS。

Commit/push 前又 HOLD 一次：

* 原因是 staged whitespace check 失败：

  * 多个 Python 文件 EOF extra blank line。
  * implementation report trailing whitespace。
* PM 授权 whitespace-only repair。
* 修复后：

  * `git diff --cached --check`: PASS
  * staged files 精确匹配 17 个 allowlist 文件
  * tests PASS

最终 commit/push：

```text
commit: 17cf5d2
message: Implement Sprint 2 generic station event model
push: PASS, main -> main
final status: clean
```

最终测试：

```text
compileall: PASS
focused station_event: 128 passed
broader tests: 216 passed
unrelated failures: none
```

---

## 9. 当前禁止事项

当前虽然 Sprint 2 已 push，但仍禁止未经规划直接做：

* Phase-2 tag。
* deploy。
* rollback drill。
* Collector runtime integration。
* API endpoint integration。
* DB schema / migration。
* Dashboard / Trace implementation。
* V-PLC changes。
* future event types。
* 修改 Phase-1 默认行为。
* 宽泛 staging：

  * `git add .`
  * `git add -A`
  * `git add docs/`

如果后续要提交任何 closeout docs，也必须使用精确 allowlist。

---

## 10. 当前正确下一步

不要立刻让 Codex 接 runtime。

建议下一步做：

```text
Sprint 2 Closeout + Sprint 3 Integration Boundary Plan
```

目标不是写 integration code，而是定义 Sprint 3 的边界、顺序、风险和 review gates。

建议开新的 Architecture / Integration Planning Thread。
按 PM 新规则，这属于工作量中等、跨多个组件、有阶段边界风险，建议新 Thread。

Sprint 3 可选方向：

```text
A. Collector adapter / event ingestion
B. DB schema / migration
C. FastAPI query contract
D. Dashboard / Trace view
E. Pilot PLC path
```

推荐优先顺序：

```text
1. Sprint 2 closeout：确认 17cf5d2 为 implementation baseline，整理 post-commit state。
2. Sprint 3 integration boundary plan：定义最小 runtime integration path。
3. 优先规划 Collector → station_event adapter，而不是直接 DB/Dashboard。
4. 单独设计 DB migration gate，不要和 Collector adapter 混在一个 Sprint。
5. Pilot PLC path 作为并行 planning，不要阻塞 station event runtime integration。
```

---

## 11. 下一条给 Architecture / Integration Planning Thread 的建议 Prompt

可以把下面 prompt 发给新的 Architecture / Integration Planning Thread：

```text
你现在作为 Edge MES Demo 项目的 Architecture / Integration Planning Thread。

当前阶段：Phase-2 Sprint 2 已完成 implementation commit/push；准备 Sprint 2 closeout 与 Sprint 3 integration boundary planning。

这是新 Thread，请根据本 prompt 恢复上下文。

当前 Git 状态：

- HEAD/origin/main：17cf5d22ae2875f1048acf683cb43309f724cbb9
- latest commit：17cf5d2 Implement Sprint 2 generic station event model
- working tree：clean
- tag：phase1-pass-20260619
- Phase-2 tag：未创建
- deploy / rollback drill：未执行
- runtime integration：未开始

已完成：

- Phase-1 PASS。
- Sprint 1 Flexible Line Configuration PASS。
- Sprint 2 Generic Station Event Model implementation 已 commit/push。
- Sprint 2 Reliability：PASS。
- Sprint 2 Data Quality targeted re-review：PASS WITH RECOMMENDATIONS。
- Sprint 2 Verification targeted sanity：PASS WITH RECOMMENDATIONS。
- focused station_event：128 passed。
- broader tests：216 passed。
- Remaining blocker：none。

Sprint 2 已交付：

common/station_event/
tests/test_station_event_model.py
docs/reports/sprint2_generic_station_event_model_implementation_report.md
docs/thread_handoff/architecture.md
docs/reports/architecture_context_restore.md
docs/reports/sprint2_station_event_reliability_review.md
docs/reports/sprint2_station_event_data_quality_review.md
docs/reports/sprint2_station_event_verification_matrix.md

当前任务：

只做 planning，不写 implementation code，不新增 migration，不接入 runtime。

目标：

1. 做 Sprint 2 closeout 状态确认。
2. 识别已提交文档中是否还有 post-commit 状态漂移，例如“not committed/pushed”之类提交前描述。
3. 提出是否需要一个 docs-only closeout commit；如果需要，给出精确 allowlist 和范围。
4. 规划 Sprint 3 integration boundary：
   - Collector adapter / event ingestion
   - DB schema / migration
   - FastAPI query contract
   - Dashboard / Trace view
   - Pilot PLC path
5. 推荐 Sprint 3 最小切入点与 review gates。
6. 明确哪些事情必须继续禁止：
   - tag
   - deploy
   - rollback drill
   - runtime integration
   - DB migration
   - Dashboard implementation
   - V-PLC changes
   除非后续 PM 单独授权。

必须读取：

- docs/thread_handoff/architecture.md
- docs/reports/architecture_context_restore.md
- docs/reports/sprint2_generic_station_event_model_implementation_report.md
- docs/reports/sprint2_station_event_reliability_review.md
- docs/reports/sprint2_station_event_data_quality_review.md
- docs/reports/sprint2_station_event_verification_matrix.md
- docs/reports/phase2_sprint_plan.md
- docs/reports/phase2_thread_task_plan.md
- docs/roadmap.md
- docs/contracts/station_event_model.md
- docs/contracts/line_configuration.md
- docs/contracts/dynamic_station_model.md
- common/station_event/

必须执行只读命令：

git status --short
git log --oneline -8
git tag --list
find common/station_event -maxdepth 1 -type f | sort

禁止事项：

- 不修改 code。
- 不修改 tests。
- 不新增 migration。
- 不接入 Collector/API/DB/Dashboard/V-PLC。
- 不 tag。
- 不 deploy。
- 不 rollback drill。
- 不 commit/push。
- 不使用 git add . / git add -A / git add docs/。

返回格式：

## Sprint 2 Closeout + Sprint 3 Integration Boundary Plan

结论：PASS / HOLD

Current baseline:
- HEAD:
- origin/main:
- working tree:
- tag list:

Sprint 2 closeout:
- implementation committed/pushed:
- remaining blocker:
- docs post-commit drift:
- need docs-only closeout commit: yes/no
- if yes, proposed allowlist:

Sprint 3 recommended boundary:
- recommended first integration slice:
- excluded from Sprint 3 first slice:
- required contracts:
- required tests:
- required review gates:

Risks:
- ...

Recommended thread plan:
- Architecture:
- Reliability:
- Data Quality:
- Verification:
- optional Dashboard/Frontend:
- optional PLC pilot:

Decision:
- eligible to start Sprint 3 implementation:
- PM approval required before:
```

---

## 12. PM 判断摘要

当前不是“review 未完成”的状态。
当前是：

```text
Sprint 2 independent station event model：完成
Commit/push：完成
HEAD/origin/main：17cf5d2
Working tree：clean
Remaining blocker：none
Integration：未开始
```

正确下一步：

```text
Sprint 2 Closeout + Sprint 3 Integration Boundary Plan
→ 决定是否需要 docs-only post-commit closeout
→ 决定 Sprint 3 最小集成切片
→ 再分配 Architecture / Reliability / Data Quality / Verification tasks
```

严禁跳过 planning 直接接 Collector/API/DB/Dashboard/V-PLC。
