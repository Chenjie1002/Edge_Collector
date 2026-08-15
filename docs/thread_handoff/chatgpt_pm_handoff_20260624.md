# Edge MES Demo — ChatGPT PM Handoff

日期：2026-06-24  
交接对象：新的 ChatGPT PM 窗口  
当前阶段：Phase-2 Sprint 2 已完成 implementation、closeout、baseline correction，并已 push；下一步是 Sprint 3 Integration Boundary Planning  
当前最高优先级：不要直接进入 Sprint 3 implementation，先完成 Sprint 3 integration boundary planning

---

## 1. 新 ChatGPT PM 的角色

你现在接手 Edge MES Demo 项目的 ChatGPT PM / 技术项目经理角色。

ChatGPT PM 职责：

- 不直接修改代码，除非用户明确要求你通过 Devspace 做有限编辑。
- 不直接 commit / push / tag / deploy，除非用户明确授权。
- 负责任务拆分、Codex Prompt 编写、优先级判断、结果审核。
- 负责决定任务交给哪个 Codex Thread。
- 负责控制阶段边界，防止 Codex 顺手扩大范围。
- 负责设置 gate：planning / review / repair / commit / integration / deploy。
- 负责在 Thread 过长时要求 handoff，并安排新 Thread 接手。

默认工作规则：

- review、focused re-review、final audit、HOLD 后 repair、跨角色 gate 判断：优先新开 Thread。
- 小范围文档修正、whitespace-only repair、单点 follow-up：可以留在当前 Thread。
- Codex 任务必须自包含，不要依赖上一个 Thread 的隐含上下文。
- 凡涉及 commit/push，必须使用精确 allowlist，禁止 `git add .` / `git add -A` / `git add docs/`。

---

## 2. 项目总体边界

项目：Edge MES Demo

定位：

- 非侵入式 Edge MES / Traceability / OEE Demo。
- PLC 是控制大脑。
- Edge Collector 只负责采集、解析、落库。
- PostgreSQL 负责结构化存储与追溯。
- FastAPI 负责查询与服务接口。
- Grafana / Trace / Dashboard 负责展示与分析。
- Edge 不替代 PLC 控制逻辑。
- Edge 不主动决定生产流程。

必须长期守住：

- 不让 Edge 主动控制生产。
- 不让 Collector / API / DB / Dashboard 改动绕过 planning gate。
- 不把 offline station event package 误解为已经 runtime integrated。
- 不在未授权情况下新增 migration、tag、deploy、rollback drill。
- 不修改 Phase-1 默认行为。

---

## 3. 当前 Git 状态，已核验

本地仓库路径：

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

当前机器：

```text
ChenjiedeMacBook-Pro.local
```

当前 branch：

```text
main
```

当前状态：

```text
HEAD:
1a22cdc70e7daaaca3befc6c94fc1610ea2205fb

origin/main:
1a22cdc70e7daaaca3befc6c94fc1610ea2205fb

remote main:
1a22cdc70e7daaaca3befc6c94fc1610ea2205fb

branch status:
main...origin/main
```

最新 log：

```text
1a22cdc Clarify Sprint 2 closeout repository baseline
82b2127 Close out Sprint 2 documentation state
17cf5d2 Implement Sprint 2 generic station event model
e9abe45 Finalize Sprint 2 station event review gates
60adac2 Address Sprint 2 station event reliability review
45fa2a8 Freeze Sprint 2 station event planning
4215b7c Finalize Sprint 1 architecture handoff and review history
b9f6a69 Phase 2 Sprint 1 flexible line configuration
```

当前 tag：

```text
phase1-pass-20260619
```

当前工作树：

```text
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
```

说明：

- tracked working tree clean。
- 唯一既有未跟踪文件是本地 PM handoff artifact。
- 该文件没有被提交，不属于当前 Sprint 2 closeout。
- 不要随手删除，也不要提交，除非用户明确授权。
- 本 handoff 文件本身也是本地交接 artifact；是否纳入 git 需 PM/用户后续明确授权。

---

## 4. 当前 source of truth

当前 repository baseline：

```text
1a22cdc Clarify Sprint 2 closeout repository baseline
```

Sprint 2 implementation commit：

```text
17cf5d2 Implement Sprint 2 generic station event model
```

Sprint 2 docs-only closeout commit：

```text
82b2127 Close out Sprint 2 documentation state
```

Sprint 2 closeout baseline correction commit：

```text
1a22cdc Clarify Sprint 2 closeout repository baseline
```

当前结论：

```text
Sprint 2 Generic Station Event Model implementation: completed
Sprint 2 closeout: completed
Sprint 2 baseline correction: completed
HEAD/origin/main/remote main: synced at 1a22cdc
Remaining blocker: none
Runtime integration: not started
Phase-2 tag: not created
Deploy: not performed
Rollback drill: not performed
```

---

## 5. 已完成阶段总览

### Phase-1

状态：PASS。

已完成：

- 单机 Demo 最终验收 PASS。
- GitHub freeze / tag / release note / push report 已完成。
- tag：`phase1-pass-20260619`
- Raspberry Pi 远程部署曾通过验证，但当前 Sprint 2 / Sprint 3 planning 不涉及远程部署。

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

状态：PASS。

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

### Sprint 2：Generic Station Event Model

状态：完成并 closeout。

关键 commits：

```text
45fa2a8 Freeze Sprint 2 station event planning
60adac2 Address Sprint 2 station event reliability review
e9abe45 Finalize Sprint 2 station event review gates
17cf5d2 Implement Sprint 2 generic station event model
82b2127 Close out Sprint 2 documentation state
1a22cdc Clarify Sprint 2 closeout repository baseline
```

当前最终状态：

```text
Implementation: completed
Commit/push: completed
Closeout: completed
Baseline correction: completed
Reliability: PASS
Data Quality: PASS WITH RECOMMENDATIONS
Verification: PASS WITH RECOMMENDATIONS
Remaining blocker: none
Runtime integration: not started
```

---

## 6. Sprint 2 已交付内容

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
docs/contracts/station_event_model.md
.gitignore
```

Sprint 2 能力范围：

- 五类 MVP event：
  - `station_cycle_start`
  - `station_cycle_complete`
  - `station_result`
  - `station_nok`
  - `station_heartbeat`
- frozen dataclass model。
- validator / serializer separation。
- normalized payload / raw payload limits。
- raw content authority validation。
- fact/content/raw evidence fingerprint。
- duplicate / conflict / raw_variant 裁决。
- NOK policy：
  - `station_result(result=NOK)` 是唯一 canonical production result。
  - `station_nok` 是 detail companion。
  - `30003` system-reserved skip relation 已隔离。
- lifecycle derived output 八字段。
- projection eligibility。
- config / lineage fields。
- historical resolved config snapshot validation。
- parent relation authority。
- raw evidence fail-closed。

重要限制：

- 这是 offline contract package。
- 尚未接入 Collector runtime。
- 尚未接入 PostgreSQL persistence。
- 尚未接入 FastAPI。
- 尚未接入 Dashboard / Trace。
- 尚未接入 V-PLC。
- 尚未实现 retry / quarantine / registry / runtime adapter。
- 接入 JavaScript/PostgreSQL 前建议补充跨运行时 JCS exact-byte fixtures。

---

## 7. Sprint 2 Review / Repair 摘要

### Reliability

最终状态：PASS。

关键关闭项：

- R-B2：跨 config accepted skip parent 支持 `30003`。
- R-B4：canonical parent authority/config/code/origin/role 校验不完整。
- 后续 canonical parent `event_role=production_result` 已强制。

最终修复：

- `30003` parent 增加 same-config 校验。
- canonical parent matcher 校验：
  - authoritative PLC/V-PLC
  - config
  - profile / station_type
  - primary code/origin
  - secondary origin
  - `event_role=production_result`
- rejected event 不产生 production outcome、defect detail 或 projection。

### Data Quality

最终状态：PASS WITH RECOMMENDATIONS。

关键关闭项：

- DQ-F1 parent snapshot lineage。
- DQ-F2 compatibility cited detail canonical validation。
- DQ-F3 raw authority fail-closed。

非阻塞建议：

- 后续补充具名 regression：
  - non-accepted cited detail
  - raw-only + callable decoder

### Verification

最终状态：PASS WITH RECOMMENDATIONS。

确认：

- V-DQ1 parent profile/station_type lineage：PASS
- V-DQ2 validated cited detail canonical authority：PASS
- V-DQ3 raw authority fail-closed：PASS
- V-DQ4 targeted regression / isolation：PASS

---

## 8. 当前禁止事项

虽然 Sprint 2 已完成并 closeout，但仍禁止未经 PM 单独授权直接做：

- Phase-2 tag。
- deploy。
- rollback drill。
- Collector runtime integration。
- API endpoint implementation。
- DB schema / migration implementation。
- Dashboard / Trace implementation。
- V-PLC behavior changes。
- real PLC pilot implementation。
- future event types。
- 修改 Phase-1 默认行为。
- 宽泛 staging：
  - `git add .`
  - `git add -A`
  - `git add docs/`

尤其注意：

```text
docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
```

这是既有未跟踪 PM handoff 文件。不要提交，不要清理，除非用户明确授权。

---

## 9. 当前正确下一步

现在可以进入：

```text
Sprint 3 Integration Boundary Planning
```

但仍然不能直接进入：

```text
Sprint 3 implementation
```

建议开新的 **Architecture / Integration Sprint 3 boundary planning Thread**。

原因：

- 这是阶段边界规划。
- 会涉及 Collector、DB、API、Dashboard、PLC pilot 的边界排序。
- 需要防止 Codex 顺手开始写 runtime integration。
- 适合新 Thread，避免 commit/push Thread 上下文继续膨胀。

推荐 Sprint 3 最小切入点：

```text
Contract-first Collector adapter / event ingestion boundary
```

推荐第一切片：

```text
resolved config snapshot + PLC/V-PLC source payload
-> station_event envelope
-> validation decision / projection metadata output
```

第一切片明确不做：

- DB write path。
- DB migration。
- FastAPI endpoint implementation。
- Dashboard / Trace UI。
- V-PLC behavior changes。
- real PLC pilot implementation。
- deploy。
- rollback drill。
- Phase-2 tag。

---

## 10. Sprint 3 Planning 推荐方向

Sprint 3 应分层规划，不要一次性打穿全链路。

建议顺序：

1. Collector adapter / event ingestion contract。
2. Offline adapter fixtures。
3. Raw / normalized decoder contract。
4. Error / reject / quarantine boundary。
5. Idempotency / duplicate / conflict handling boundary。
6. DB schema / migration design gate。
7. FastAPI query contract。
8. Trace / Dashboard data contract。
9. Pilot PLC path planning。

不要把 DB migration 和 Collector adapter 实现混在同一个第一 implementation slice 中。

---

## 11. 下一条给 Codex 的建议 Prompt

可以直接发给新的 Codex Thread：

```text
你现在作为 Edge MES Demo 项目的 Architecture / Integration Sprint 3 boundary planning Thread。

当前阶段：Phase-2 Sprint 2 已完成 implementation、docs-only closeout 与 closeout baseline correction；准备 Sprint 3 integration boundary planning。

当前状态：
- 当前仓库路径：/Users/chenjie/Documents/MES/edge-mes-demo
- 当前 branch：main
- 当前 HEAD/origin/main/remote main：
  1a22cdc Clarify Sprint 2 closeout repository baseline
- Sprint 2 implementation commit：
  17cf5d2 Implement Sprint 2 generic station event model
- Sprint 2 docs-only closeout commit：
  82b2127 Close out Sprint 2 documentation state
- Sprint 2 closeout baseline correction commit：
  1a22cdc Clarify Sprint 2 closeout repository baseline
- Phase-1 tag：phase1-pass-20260619
- Phase-2 tag：未创建
- deploy：未执行
- rollback drill：未执行
- runtime integration：未开始
- 当前仍存在一个未跟踪 PM handoff 文件，必须排除：
  docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md

当前 PM 结论：
- Sprint 2 Generic Station Event Model implementation：完成
- Sprint 2 closeout：完成
- Remaining blocker：none
- 现在允许进入 Sprint 3 integration boundary planning
- 仍不允许直接进入 Sprint 3 implementation

你的任务是只做 Sprint 3 integration boundary planning，不写 implementation code。

规划目标：

1. 定义 Sprint 3 的最小 integration slice。
2. 推荐 integration 顺序：
   - Collector adapter / event ingestion
   - DB schema / migration
   - FastAPI query contract
   - Dashboard / Trace view
   - Pilot PLC path
3. 明确第一阶段应该做什么、不做什么。
4. 明确各阶段需要哪些合同、测试、review gates。
5. 明确哪些事项必须继续等待 PM 单独授权。
6. 给出 Sprint 3 thread plan：
   - Architecture / Integration
   - Reliability
   - Data Quality
   - Verification
   - optional Dashboard / Frontend
   - optional PLC pilot

必须读取：

docs/thread_handoff/architecture.md
docs/reports/architecture_context_restore.md
docs/reports/sprint2_generic_station_event_model_implementation_report.md
docs/reports/sprint2_station_event_reliability_review.md
docs/reports/sprint2_station_event_data_quality_review.md
docs/reports/sprint2_station_event_verification_matrix.md
docs/reports/phase2_sprint_plan.md
docs/reports/phase2_thread_task_plan.md
docs/roadmap.md
docs/contracts/station_event_model.md
docs/contracts/line_configuration.md
docs/contracts/dynamic_station_model.md
common/station_event/

必须执行只读命令：

cd /Users/chenjie/Documents/MES/edge-mes-demo

git status --short
git status -sb
git log --oneline -8
git tag --list
find common/station_event -maxdepth 1 -type f | sort

重点判断：

Sprint 3 first slice 是否应优先选择：
- Collector adapter / event ingestion boundary
- offline adapter fixtures
- resolved config snapshot + source payload -> station_event envelope
- validation decision / projection metadata output
- no DB write path yet

必须明确排除：
- DB migration implementation
- FastAPI endpoint implementation
- Dashboard / Trace implementation
- V-PLC behavior changes
- real PLC pilot implementation
- deploy
- rollback drill
- Phase-2 tag

禁止事项：

- 不修改 code。
- 不修改 tests。
- 不新增 migration。
- 不接入 Collector/API/DB/Dashboard/V-PLC。
- 不实现 runtime integration。
- 不创建 tag。
- 不 deploy。
- 不 rollback drill。
- 不 commit/push。
- 不使用 git add .
- 不使用 git add -A
- 不使用 git add docs/
- 不处理或提交未跟踪 PM handoff 文件：
  docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md

如果需要记录 planning 结果，只允许提出建议，不要直接修改文件。是否写入 planning docs 需要 PM 后续单独授权。

返回格式：

## Sprint 3 Integration Boundary Planning Result

结论：PASS / HOLD

Current baseline:
- HEAD:
- origin/main:
- remote main:
- working tree:
- tag list:

Sprint 2 closeout status:
- implementation committed/pushed:
- docs-only closeout committed/pushed:
- baseline correction committed/pushed:
- remaining blocker:
- runtime integration started:
- tag/deploy/rollback performed:

Recommended Sprint 3 first slice:
- recommended first integration slice:
- why this slice first:
- inputs:
- outputs:
- explicitly excluded:
- success criteria:

Sprint 3 boundary:
- Collector adapter / event ingestion:
- DB schema / migration:
- FastAPI query contract:
- Dashboard / Trace view:
- Pilot PLC path:

Required contracts:
- ...

Required tests:
- ...

Required review gates:
- Architecture:
- Reliability:
- Data Quality:
- Verification:
- PM authorization:

Risks:
- ...

Recommended thread plan:
- Architecture / Integration:
- Reliability:
- Data Quality:
- Verification:
- optional Dashboard / Frontend:
- optional PLC pilot:

Decision:
- eligible to start Sprint 3 implementation:
- PM approval required before:
- recommended next Codex thread:
- remaining blocker:

Thread Health:
- 本 Thread 已完成的主要任务：
- 当前上下文是否仍适合继续：
- 是否建议新开 Thread：
- 如果建议新开，请给出 handoff 摘要：
- 是否存在上下文不足、历史信息可能遗失、或需要重新读取文件的风险：
```

---

## 12. PM 判断摘要

当前不是“implementation 未完成”的状态，也不是“closeout 未完成”的状态。

当前是：

```text
Sprint 2 independent station event model: completed
Sprint 2 closeout: completed
Baseline correction: completed
HEAD/origin/main/remote main: 1a22cdc
Working tree tracked diff: clean
Only existing untracked file: local PM handoff artifact
Remaining blocker: none
Integration: not started
```

下一步：

```text
Sprint 3 Integration Boundary Planning
```

不是：

```text
Sprint 3 implementation
```

下一任 ChatGPT PM 应先审核 Codex 返回的 Sprint 3 boundary plan，再决定是否需要：

- docs-only planning commit；
- Reliability review；
- Data Quality review；
- Verification matrix；
- PM 精确授权 Sprint 3 first implementation slice。
