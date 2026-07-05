# ChatGPT PM Handoff — Edge MES Demo

Created: 2026-07-05 09:29 UTC+8

## 1. Project / PM context

Project path:

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

Remote validation host used in the previous DB-backed validation chain:

```text
SSH alias: edge-pi
remote verified checkout: /home/mari/edge-mes-demo-work
remote Phase 1 deploy path: /opt/edge-mes-demo
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

This handoff is for a new ChatGPT PM window. The new PM must perform read-only recovery before continuing.

## 2. Live repository baseline at handoff creation

Local recovery result at handoff creation:

```text
HEAD == origin/main == f4de1c345f503c9556bceece99ef22be091c025e
latest commit:
f4de1c3 Add DB API Dashboard consumer planning
cached name-only: empty
```

Recent commits:

```text
f4de1c3 Add DB API Dashboard consumer planning
961217e Sync DB-backed validation harness status
5543c87 Add PM handoff after DB-backed validation harness repair
8a8004c Fix DB-backed API validation harness
a4d1644 Sync API DB-backed schema verification status
99dfc26 Add PM handoff after API DB-backed schema verification
2cfad5d Add API DB-backed schema verification
64d0e12 Sync DB-backed API read validation status
```

## 3. Current working tree / external artifacts

At handoff creation, the working tree still contains known external dirty artifacts that must not be staged unless explicitly authorized:

```text
 M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

No staged files at handoff creation.

The newly created file is this handoff:

```text
docs/thread_handoff/chatgpt_pm_handoff_260705-0929.md
```

Do not stage this handoff unless the user explicitly authorizes an exact-path handoff commit gate.

## 4. Closed gate immediately before handoff

Gate:

```text
DB/API/Dashboard consumer planning gate + review sequence + exact-path planning doc commit/push
```

Conclusion:

```text
CLOSED / PASS WITH RECOMMENDATIONS
```

Committed and pushed file:

```text
docs/reports/sprint3_db_api_dashboard_consumer_plan.md
```

Commit:

```text
f4de1c345f503c9556bceece99ef22be091c025e Add DB API Dashboard consumer planning
```

Push result:

```text
961217e..f4de1c3  main -> main
```

Staged-set audit before commit included only:

```text
docs/reports/sprint3_db_api_dashboard_consumer_plan.md
```

Excluded from commit:

```text
.gitignore
old PM handoff files
Keynote/reporting artifacts
current_status.md and existing gate/status docs
API / Collector / storage / migration / Dashboard / frontend / V-PLC / config files
```

## 5. DB/API/Dashboard consumer planning chain summary

The prior DB-backed validation harness chain was already closed before this planning branch:

```text
8a8004c Fix DB-backed API validation harness
remote live DB-backed API validation: PASS, focused pytest 62 passed in 8.68s
test DB cleanup: test_db_cleanup_ok edge_mes_test_api_read
5543c87 Add PM handoff after DB-backed validation harness repair
961217e Sync DB-backed validation harness status
```

Then the Dashboard/API consumer planning branch was opened.

Architecture / Integration created the planning doc:

```text
docs/reports/sprint3_db_api_dashboard_consumer_plan.md
```

Architecture / Integration planning conclusion:

```text
PASS WITH RECOMMENDATIONS
```

Reliability focused review conclusion:

```text
PASS WITH RECOMMENDATIONS, no blocker
```

Data Quality focused review conclusion:

```text
PASS WITH RECOMMENDATIONS, no blocker
```

Verification focused review / exact planning allowlist audit conclusion:

```text
PASS WITH RECOMMENDATIONS, no blocker
```

PM then performed exact-path stage/commit/push for only the new planning doc:

```text
f4de1c3 Add DB API Dashboard consumer planning
```

## 6. Planning boundary frozen by f4de1c3

The planning doc freezes these boundaries for downstream API/Dashboard consumers:

```text
Only production fact source: production_accepted_station_event_fact
```

The following surfaces must not be treated as equivalent production fact sources, fallback sources, legacy compatibility sources or join-derived field fillers:

```text
raw_plc_sample
cycle_event
station_event
production_unit
quality_event
production_snapshot
production_events
```

Consumer-facing production fields must come only from accepted fact rows. raw payload, raw_hex, decoded/source normalized payloads, adapter disposition, reason code, candidate context and raw/normalized comparison context are diagnostic/review/debug only and must not enter OEE or traceability main production facts.

`quality_pareto_input`, `dashboard_state` and ambiguous production-looking keys such as bare `result`, `defect`, `quality` or `pareto` are forbidden as production consumer sources.

`work_order` and `product` remain excluded until a later schema/contract authority gate exists.

`accepted_at` is an accepted fact timestamp. It must not be presented as collector freshness, ACK time or station freshness.

Optional debug/review diagnostics view must be a separate Level 2 gate and must pass leakage-negative review before implementation.

## 7. Carry-forward recommendations

Reliability / Data Quality / Verification recommendations are carry-forward items, not blockers for the committed planning doc:

```text
API consumer contract freeze / implementation prompts must explicitly include read-only transaction, statement/read timeout, invalid filter/cursor/limit fail-closed or 4xx behavior and large-query protection.

Future API tests must include explicit DTO allowlist and forbidden-source negative tests proving legacy/current/raw/diagnostic/candidate sources cannot fill production fields.

Future acceptance must define DB unavailable / missing table / missing schema / missing authority behavior as error, empty or unknown, and must prohibit fallback.

Dashboard contract freeze must add a page/component-to-field matrix and empty/error/unknown state, especially preventing accepted_at from being displayed as collector freshness or ACK time.

Optional debug/review diagnostics view must be a separate Level 2 gate with leakage-negative review.
```

## 8. Current open / pending work

Current open work:

```text
1. DB/API/Dashboard consumer planning post-push docs/status sync gate
2. exact-path docs/status commit/push after that sync
3. optional handoff commit for this file, only if user authorizes
```

Recommended next gate:

```text
DB/API/Dashboard consumer planning post-push docs/status sync gate
```

Recommended owner:

```text
Architecture / Integration
```

Recommended task tier:

```text
Level 1 docs/status sync
```

Expected docs/status allowlist, to be confirmed by the next PM before issuing the task:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

The docs/status sync should record:

```text
DB/API/Dashboard consumer planning gate: CLOSED / PASS WITH RECOMMENDATIONS
Reliability review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Data Quality review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Verification review / exact planning allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Exact-path planning doc commit/push: CLOSED / PASS, commit f4de1c3
```

After docs/status sync and exact-path docs/status commit/push are closed, the next eligible planning branch is:

```text
API consumer contract freeze
```

That branch is Level 2 and must not be treated as a simple docs edit just because it may initially modify contract documents.

## 9. Non-authorized surfaces

The next PM must not infer authorization for:

```text
API implementation
Dashboard/frontend implementation
new migration
DB write path changes
Collector/runtime/storage changes
DB opt-in execution
EDGE_MES_ENABLE_DB_BACKED_TESTS=1
DB connection
temp DB create/drop
Docker / docker compose lifecycle
tests
broad tests
deploy/tag/rollback
real PLC pilot
stage/commit/push
```

## 10. Suggested prompt for the next ChatGPT PM window

Copy this into the next ChatGPT PM window:

```markdown
你是 Edge MES Demo 的 ChatGPT PM，请接手当前项目管理任务。

第一优先级：先恢复上下文，不要直接推进开发。

请先读取并遵守：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260705-0929.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
- docs/reports/sprint3_db_api_dashboard_consumer_plan.md

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

Expected live baseline：

    HEAD == origin/main == f4de1c345f503c9556bceece99ef22be091c025e
    latest commit:
    f4de1c3 Add DB API Dashboard consumer planning
    cached name-only == empty

最近已完成的关键链路：

    1. DB-backed API validation harness repair + remote live validation docs/status sync 已关闭：commit 961217e。
    2. DB/API/Dashboard consumer planning gate 已关闭：PASS WITH RECOMMENDATIONS。
    3. Reliability / Data Quality / Verification focused reviews 均 PASS WITH RECOMMENDATIONS，无 blocker。
    4. Exact-path planning doc commit/push 已完成：f4de1c3 Add DB API Dashboard consumer planning。

当前 known external dirty artifacts，不要 stage / clean / edit，除非我明确授权：

    .gitignore
    docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
    docs/reports/phase1_to_sprint2_management_keynote_10p.html
    docs/thread_handoff/chatgpt_pm_handoff_20260624.md
    docs/thread_handoff/chatgpt_pm_handoff_20260625.md
    docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
    docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

当前待办不是新功能开发，而是先做 docs/status 同步。

推荐下一步 gate：

    DB/API/Dashboard consumer planning post-push docs/status sync gate

推荐执行 Thread：

    Architecture / Integration

建议 docs/status sync allowlist 先由你读取确认，但预计是：

    docs/current_status.md
    docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
    docs/reports/sprint3_collector_ingestion_adapter_plan.md

注意：

- 不要自动授权 API consumer contract freeze。
- 不要自动授权 API implementation / Dashboard implementation。
- 不要 stage/commit/push，除非我明确授权 exact-path gate。
- 不要动 `.gitignore` 和旧 artifacts。
- 不要连接 DB、运行 DB-backed pytest、启动/停止 Docker，除非单独授权。
- 后续给 Codex / Thread 的 prompt 必须符合 pm_operating_rules.md：中文、单块可复制 Markdown、包含报告名称/任务名称/执行 Thread/PM 任务前工作量评估/读取列表/allowlist/exclusions/报告格式。
```

## 11. Summary for user-facing PM continuity

Current project is in a good state. The Dashboard/API consumer planning branch is closed, reviewed by Reliability/Data Quality/Verification, and committed/pushed at `f4de1c3`.

The immediate next work is documentation/status synchronization for that planning branch, not API or Dashboard implementation.

After the docs/status sync and exact-path commit/push are closed, the next eligible branch is `API consumer contract freeze`, which is a Level 2 planning/contract branch requiring the full review sequence before any implementation.
