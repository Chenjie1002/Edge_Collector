# ChatGPT PM Handoff — Edge MES Demo

Created: 2026-07-05 12:01 UTC+8

## 1. Project / PM context

Project path:

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

Operating rules:

```text
docs/thread_handoff/pm_operating_rules.md
```

Thread model:

```text
Architecture / Integration
Reliability
Data Quality
Verification
```

This handoff is for a new ChatGPT PM window. The new PM must perform read-only recovery before continuing and must treat live Git output as the source of truth.

## 2. Live repository baseline at handoff creation

Read-only recovery result at handoff creation:

```text
HEAD == origin/main == d99a8f12342a2d2fba6880f641e7dd63a4015fab
latest commit:
d99a8f1 Sync API consumer contract status
cached name-only: empty
```

Recent commits:

```text
d99a8f1 Sync API consumer contract status
f65a120 Freeze API consumer contract
5e7c1c8 Sync consumer planning status
cd6dff8 Add PM handoff after consumer planning
f4de1c3 Add DB API Dashboard consumer planning
961217e Sync DB-backed validation harness status
5543c87 Add PM handoff after DB-backed validation harness repair
8a8004c Fix DB-backed API validation harness
```

## 3. Current working tree / external artifacts

At handoff creation, the working tree contains only known external dirty artifacts plus this newly created handoff file.

Known external dirty artifacts that must not be staged unless explicitly authorized:

```text
 M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

Newly created PM handoff file, not yet staged at creation:

```text
docs/thread_handoff/chatgpt_pm_handoff_260705-1201.md
```

Do not stage this handoff unless the user explicitly authorizes an exact-path handoff commit gate. If this handoff is later committed, live `HEAD` / `origin/main` from read-only recovery supersedes the baseline shown above.

## 4. Closed gates immediately before handoff

### 4.1 DB/API/Dashboard consumer planning closeout

Gate:

```text
DB/API/Dashboard consumer planning gate + review sequence + exact-path planning doc commit/push + post-push docs/status sync
```

Conclusion:

```text
CLOSED / PASS WITH RECOMMENDATIONS
```

Committed planning document:

```text
docs/reports/sprint3_db_api_dashboard_consumer_plan.md
```

Planning commit:

```text
f4de1c345f503c9556bceece99ef22be091c025e Add DB API Dashboard consumer planning
```

PM handoff after consumer planning:

```text
cd6dff82c752c3c43e5a62223a5b03d28987c146 Add PM handoff after consumer planning
```

Post-push docs/status sync commit:

```text
5e7c1c8e74005dccf1074a6a793e1b038c9dd43a Sync consumer planning status
```

Review sequence:

```text
Architecture / Integration planning: PASS WITH RECOMMENDATIONS
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Verification focused review / exact planning allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
```

### 4.2 API consumer contract freeze closeout

Gate:

```text
DB/API/Dashboard API consumer contract freeze planning/contract gate + Reliability/Data Quality/Verification focused reviews + exact-path contract commit/push + post-push docs/status sync
```

Conclusion:

```text
CLOSED / PASS WITH RECOMMENDATIONS
```

Committed contract file:

```text
docs/contracts/dashboard_api_contract.md
```

Contract commit:

```text
f65a120545efcdb7ca39f20dbf703a804f82763f Freeze API consumer contract
```

Post-push docs/status sync commit:

```text
d99a8f12342a2d2fba6880f641e7dd63a4015fab Sync API consumer contract status
```

Review sequence:

```text
Architecture / Integration contract freeze: PASS WITH RECOMMENDATIONS
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Verification focused review / exact contract allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
```

Exact contract commit staged only:

```text
docs/contracts/dashboard_api_contract.md
```

Exact docs/status sync commit staged only:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

## 5. Frozen consumer / contract boundaries

Only consumer-facing production fact source:

```text
production_accepted_station_event_fact
```

The following must not be used as equivalent production fact sources, fallback sources, legacy compatibility sources or join-derived field fillers:

```text
raw_plc_sample
cycle_event
station_event
production_unit
quality_event
production_snapshot
production_events
```

Consumer-facing production DTO fields must come from `production_accepted_station_event_fact` row fields only. All fallbacks are forbidden.

Forbidden from production DTOs, production Dashboard payloads, OEE, traceability main facts, accepted result displays and Quality/Pareto production metrics:

```text
raw payload / raw_hex / raw bytes / raw_sample_id
decoded or source normalized candidate payload before accepted decision
adapter disposition / reason / phase / candidate context
raw-normalized comparison context
decoder errors
diagnostic / review / audit payloads
ack_status / read_done / collector_state
quality_pareto_input / dashboard_state
bare result / defect / quality / pareto keys
legacy/current table joins that fill missing accepted fact fields
```

NOK/detail fields may be visible only when present on accepted fact rows and bound to accepted upstream business evidence and shared station-event validation.

`accepted_at` is an accepted fact timestamp. It is not collector freshness, ACK time, station freshness, read_done time or station liveness.

`work_order` and `product` remain excluded until a later schema/contract authority gate creates accepted fact authority for them.

Optional debug/review diagnostics view remains deferred. It requires a separate Level 2 gate, separate diagnostic/audit/review namespaces and leakage-negative review before implementation.

## 6. Carry-forward recommendations

Carry-forward recommendations are not blockers for the closed contract/status gates:

```text
Future API implementation planning must translate the contract into an executable acceptance matrix.
Future implementation planning must freeze concrete timeout values, HTTP/error envelope behavior and cursor signature/secret/version tuple details.
Future implementation planning must define DB unavailable / missing table / missing schema / missing authority / unknown state behavior, and must explicitly prohibit fallback to legacy/raw/current/diagnostic sources.
Future tests/reviews must cover DTO positive allowlist, forbidden DTO/source leakage, invalid query/filter/cursor/time/window, Dashboard empty/error/unknown states and no-side-effect assertions.
Future Dashboard/API implementation gates must preserve the Dashboard page/component field matrix and must not fabricate OEE schedule/runtime denominators or station freshness.
`work_order` / `product` remain excluded until a later schema/contract authority gate.
```

## 7. Current open / pending work

Current pending work after this handoff file is created:

```text
1. Optional exact-path commit/push of this handoff file only, if the user explicitly authorizes it.
2. After handoff closeout, the next eligible product branch is an API implementation planning gate or Dashboard/API implementation planning gate.
```

Recommended immediate next gate if continuing handoff closeout:

```text
PM-direct exact-path handoff commit/push
```

Expected exact allowlist for handoff commit:

```text
docs/thread_handoff/chatgpt_pm_handoff_260705-1201.md
```

Suggested commit message:

```text
Add PM handoff after API consumer contract closeout
```

Recommended next product gate after handoff/status closeout:

```text
API implementation planning gate
```

Alternative eligible branch:

```text
Dashboard/API implementation planning gate
```

Both are Level 2 planning/implementation branches. Do not treat either as a simple docs edit. Do not start either without explicit PM authorization.

## 8. Non-authorized surfaces

Do not infer authorization for:

```text
API implementation
Dashboard/frontend implementation
tests
DB opt-in execution or DB connection
EDGE_MES_ENABLE_DB_BACKED_TESTS=1
temp DB create/drop
Docker / docker compose lifecycle
new migration / schema changes
Collector/runtime/storage.py changes
config/mapping.yaml changes
V-PLC / PLC pilot work
optional debug/review diagnostics implementation
stage/commit/push except exact-path handoff commit if explicitly authorized
deploy/tag/rollback
real PLC pilot
```

## 9. Suggested prompt for the next ChatGPT PM window

Copy this into the next ChatGPT PM window:

```markdown
你是 Edge MES Demo 的 ChatGPT PM，请接手当前项目管理任务。

第一优先级：先恢复上下文，不要直接推进开发。

请先读取并遵守：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260705-1201.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
- docs/reports/sprint3_db_api_dashboard_consumer_plan.md
- docs/contracts/dashboard_api_contract.md

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

第一动作必须是 read-only recovery：

    git status -sb
    printf '\n--- log -8 ---\n' && git log --oneline -8
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git rev-parse origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only
    printf '\n--- status all ---\n' && git status --short --untracked-files=all

Expected live baseline at handoff creation:

    HEAD == origin/main == d99a8f12342a2d2fba6880f641e7dd63a4015fab
    latest commit:
    d99a8f1 Sync API consumer contract status
    cached name-only == empty

If this handoff file was committed after creation, the live recovery result supersedes the expected baseline above.

最近已完成的关键链路：

    1. DB/API/Dashboard consumer planning gate 已关闭并完成 docs/status sync：
       5e7c1c8 Sync consumer planning status

    2. API consumer contract freeze 已关闭：
       Architecture / Reliability / Data Quality / Verification 均 PASS WITH RECOMMENDATIONS，无 blocker

    3. Exact-path contract commit/push 已完成：
       f65a120 Freeze API consumer contract

    4. API consumer contract freeze post-push docs/status sync 已完成：
       d99a8f1 Sync API consumer contract status

当前 known external dirty artifacts，不要 stage / clean / edit，除非我明确授权：

    .gitignore
    docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
    docs/reports/phase1_to_sprint2_management_keynote_10p.html
    docs/thread_handoff/chatgpt_pm_handoff_20260624.md
    docs/thread_handoff/chatgpt_pm_handoff_20260625.md
    docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
    docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

如果当前 handoff 文件尚未提交，`docs/thread_handoff/chatgpt_pm_handoff_260705-1201.md` 也会显示为 untracked；不要 stage，除非我明确授权 exact-path handoff commit/push。

当前待办不是新功能开发。若 handoff 文件尚未提交，推荐下一步是 exact-path handoff commit/push。

若 handoff 已提交，下一条 eligible product branch 是：

    API implementation planning gate

可选 eligible branch：

    Dashboard/API implementation planning gate

注意：

- API implementation planning / Dashboard/API implementation planning 都是 Level 2，需要单独授权。
- 不要自动授权 API implementation / Dashboard implementation。
- 不要自动授权 tests、DB execution、Docker、migration、Collector/runtime/storage/config 修改。
- 不要自动授权 optional debug/review diagnostics view。
- 不要 stage/commit/push，除非我明确授权 exact-path gate。
- 不要动 `.gitignore` 和旧 artifacts。
- 后续给 Codex / Thread 的 prompt 必须符合 pm_operating_rules.md：中文、单块可复制 Markdown、包含报告名称/任务名称/执行 Thread/PM 任务前工作量评估/读取列表/allowlist/exclusions/报告格式。
```

## 10. Summary for user-facing PM continuity

Current project is in a good state. DB/API/Dashboard consumer planning and API consumer contract freeze are closed, reviewed by Reliability/Data Quality/Verification, committed and synchronized into durable status documents.

The immediate handoff closeout action is optional exact-path commit/push of this handoff file. After that, the next product branch should be a separately authorized Level 2 planning gate, most likely API implementation planning. No API implementation, Dashboard implementation, tests, DB, Docker, deployment or PLC pilot work is authorized by this handoff.
