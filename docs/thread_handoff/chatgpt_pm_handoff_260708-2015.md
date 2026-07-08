# ChatGPT PM Handoff — 260708-2015

Created: 2026-07-08 20:15 China Standard Time / UTC+8
Project: Edge MES Demo
Project path: `/Users/chenjie/Documents/MES/edge-mes-demo`

## 1. Next PM first action

The next ChatGPT PM must start with read-only recovery. Do not edit, run tests, connect DB, start Docker/browser/runtime, stage, commit or push before recovery.

```bash
git status -sb
printf '\n--- log -8 ---\n' && git log --oneline -8
printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
printf '\n--- origin/main ---\n' && git rev-parse origin/main
printf '\n--- diff name-only ---\n' && git diff --name-only
printf '\n--- cached name-only ---\n' && git diff --cached --name-only
printf '\n--- status all ---\n' && git status --short --untracked-files=all
```

Expected baseline at handoff creation time:

```text
HEAD == origin/main == b41387661d62f33971d39e83ec89152c0500e859
latest commit: b413876 Sync Dashboard no-DB validation status
```

Important: this handoff file is created after commit `b413876`. If this handoff file is later committed/pushed, live `HEAD` / `origin/main` will move to the handoff commit. Treat the recovery output as source of truth and compare it against the user-provided latest baseline in the new PM window.

## 2. Required reading

Read and obey:

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`
- `docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`
- `docs/contracts/dashboard_api_contract.md`

## 3. Current closed gate state

Current closed gate:

```text
Sprint 3 Dashboard accepted-events no-DB vertical validation execution:
CLOSED / PASS WITH RECOMMENDATIONS
```

Status sync for that gate:

```text
Docs/status sync: PASS
Commit/push: b41387661d62f33971d39e83ec89152c0500e859 Sync Dashboard no-DB validation status
Committed files:
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

No pending review, execution, docs/status sync, commit or push gate is open at handoff creation time.

## 4. Recently completed work

### 4.1 Dashboard accepted-events vertical validation planning

- Planning gate: CLOSED / PASS WITH RECOMMENDATIONS.
- Planning commit: `dd6dc53 Plan Dashboard accepted-events vertical validation`.
- Planning post-push docs/status sync: `b7ce52b Sync Dashboard vertical validation status`.
- PM handoff after planning sync: `8b2e7a0 Add PM handoff after Dashboard vertical validation sync`.

### 4.2 Frontend dependency environment prep

- Gate: CLOSED / PASS.
- Exact command authorized and executed: `cd frontend && npm ci`.
- Result: dependencies installed; `frontend/node_modules/` exists as a local dependency artifact only.
- No tracked package/source/docs diff introduced by this gate.
- `frontend/node_modules/` must remain excluded from staging.

### 4.3 no-DB focused frontend validation execution

Architecture / Integration execution gate:

```text
PASS
4 focused frontend files / 19 tests passed
```

Focused evidence:

```text
frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts: 8 tests passed
frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts: 2 tests passed
frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts: 2 tests passed
frontend/src/app/accepted-events/__tests__/page.test.tsx: 7 tests passed
```

Only the four authorized `npm test -- <file>` commands were reported as executed. No DB/API pytest, DB-backed run, browser/manual smoke, Docker/runtime/server, typecheck/build, docs/status sync, stage, commit or push was executed during this validation execution gate.

### 4.4 Focused reviews

Review chain result:

```text
Verification focused review / exact evidence audit: PASS WITH RECOMMENDATIONS, no blocker
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
```

PM closeout:

```text
Sprint 3 Dashboard accepted-events no-DB vertical validation execution gate:
CLOSED / PASS WITH RECOMMENDATIONS
```

## 5. Current implementation boundary

These boundaries remain active unless a future PM explicitly opens a separate gate:

- Dashboard/frontend only.
- Read-only consumer only.
- Only `GET /api/v2/production/accepted-station-events`.
- Query params only: `line_id`, `start_time`, `end_time`, `limit`, `cursor`.
- DTO allowlist only accepted fact fields from `production_accepted_station_event_fact`.
- No raw/debug/diagnostic/candidate/legacy fallback.
- No `work_order` / `product`.
- `accepted_at` means accepted fact timestamp only, not freshness / ACK / station freshness / read_done.
- Page summaries are labelled current page only.
- Missing `line_id` / `start_time` / `end_time` fail closed before request.
- Cursor remains opaque and clears on line/time/limit scope changes.
- Invalid / expired / cross-scope cursor behavior must fail closed.
- Dashboard must not decode / mutate / construct cursor payload.
- No side effects beyond read-only frontend request construction/rendering.

## 6. Carry-forward recommendations

These are not blockers for the closed no-DB validation execution gate, but should be carried to future focused evidence work:

1. Add a separately authorized `apiClient` focused test for only-GET endpoint behavior, 4xx invalid/expired/cross-scope cursor mapping and 503 unavailable mapping.
2. Add an explicit executable invalid `limit` case.
3. Expand forbidden leakage fixtures into a parameterized full matrix.

Potential next branches, all requiring explicit PM authorization:

- `apiClient` focused no-DB tests.
- API non-DB focused evidence.
- `npm run typecheck` / `npm run build` gate.
- Browser/manual smoke gate.
- DB-backed validation gate.
- A fresh planning branch for the next Dashboard/API/DB slice.

## 7. Known external dirty artifacts to exclude

At handoff creation time, known external dirty artifacts are:

```text
.gitignore
docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
docs/reports/phase1_to_sprint2_management_keynote_10p.html
docs/reports/sprint3_db_backed_api_validation_reliability_review.md
docs/thread_handoff/chatgpt_pm_handoff_20260624.md
docs/thread_handoff/chatgpt_pm_handoff_20260625.md
docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
frontend/node_modules/
```

Do not stage or commit any of these unless the user explicitly authorizes the exact path. In particular, do not use `git add .`, `git add -A` or broad `git add docs/`.

## 8. Non-authorized surfaces

Not authorized by this handoff:

- tests execution;
- API pytest;
- DB-backed validation;
- Postgres / live DB work;
- `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`;
- browser/manual smoke;
- Docker / docker compose;
- runtime/server startup;
- `npm run typecheck`;
- `npm run build`;
- frontend/API/contract/package/DB edits;
- DB migration;
- Collector runtime integration;
- V-PLC/PLC behavior changes;
- deploy / tag / rollback;
- real PLC pilot;
- stage / commit / push without explicit PM/user authorization.

## 9. Current handoff file status

This handoff file path:

```text
docs/thread_handoff/chatgpt_pm_handoff_260708-2015.md
```

At creation, this file is not yet committed. Per PM rules, do not stage it automatically. The user must explicitly authorize exact-path stage/commit/push.

If authorized, stage exactly this file only:

```bash
git add docs/thread_handoff/chatgpt_pm_handoff_260708-2015.md
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
git commit -m "Add PM handoff after Dashboard no-DB validation sync"
git push
```

Do not stage `.gitignore`, old handoff files, Keynote/reporting artifacts, unrelated reports or `frontend/node_modules/`.

## 10. Copyable prompt for next ChatGPT PM window

```markdown
你是 Edge MES Demo 项目的 ChatGPT PM，请接手当前项目管理任务。

第一优先级：先恢复上下文，不要直接推进开发。

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

请先读取并遵守：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260708-2015.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
- docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md
- docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md
- docs/reports/sprint3_dashboard_api_implementation_plan.md
- docs/contracts/dashboard_api_contract.md

第一动作必须是 read-only recovery。不要编辑、不要运行 tests、不要连接 DB、不要启动 Docker/browser/runtime、不要 stage、不要 commit、不要 push。

执行：

    git status -sb
    printf '\n--- log -8 ---\n' && git log --oneline -8
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git rev-parse origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only
    printf '\n--- status all ---\n' && git status --short --untracked-files=all

Expected live baseline if this handoff has not yet been committed:

    HEAD == origin/main == b41387661d62f33971d39e83ec89152c0500e859
    latest commit: b413876 Sync Dashboard no-DB validation status

If the user reports a later PM handoff commit, treat that reported commit as the expected live baseline and verify it with read-only recovery.

当前关闭状态：

- Sprint 3 Dashboard accepted-events no-DB vertical validation execution: CLOSED / PASS WITH RECOMMENDATIONS
- Docs/status sync for that gate: PASS, committed/pushed at b413876
- No pending review, execution, docs/status sync, commit or push gate is open unless the user gives a new explicit authorization.

当前 carry-forward recommendations：

1. Separately authorize `apiClient` focused test for only-GET endpoint behavior, 4xx invalid/expired/cross-scope cursor mapping and 503 unavailable mapping.
2. Add explicit invalid `limit` executable coverage.
3. Expand forbidden leakage fixtures into a parameterized full matrix.

当前必须排除的 external dirty artifacts：

- .gitignore
- docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
- docs/reports/phase1_to_sprint2_management_keynote_10p.html
- docs/reports/sprint3_db_backed_api_validation_reliability_review.md
- docs/thread_handoff/chatgpt_pm_handoff_20260624.md
- docs/thread_handoff/chatgpt_pm_handoff_20260625.md
- docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
- docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
- frontend/node_modules/

不要使用 broad staging。不要 stage `.gitignore`、旧 handoff、Keynote/reporting artifacts、unrelated reports 或 `frontend/node_modules/`。

请先完成 read-only recovery 和上下文恢复，然后向用户报告当前 gate 状态与推荐下一步。不要自动进入 tests/API/DB/browser/typecheck/build/docs sync/stage/commit/push。
```
