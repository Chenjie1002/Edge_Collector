# ChatGPT PM Handoff — 2026-07-08 22:37

Project: Edge MES Demo
Path: `/Users/chenjie/Documents/MES/edge-mes-demo`
Thread role: ChatGPT PM

## 1. First action for next PM: read-only recovery

The next PM must start with read-only recovery. Do not edit files, run tests, connect to DB, start Docker/browser/server/runtime, run typecheck/build, stage, commit or push before recovery.

Run:

```bash
git status -sb
printf '\n--- log -8 ---\n' && git log --oneline -8
printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
printf '\n--- origin/main ---\n' && git rev-parse origin/main
printf '\n--- diff name-only ---\n' && git diff --name-only
printf '\n--- cached name-only ---\n' && git diff --cached --name-only
printf '\n--- status all ---\n' && git status --short --untracked-files=all
```

If `git status` is blocked by tool safety, use equivalent read-only checks:

```bash
git rev-parse HEAD
git rev-parse origin/main
git log -1 --format='%H %s'
git log --oneline -8
git diff --name-only
git diff --cached --name-only
git ls-files --modified
git ls-files --deleted
git ls-files --others --exclude-standard | grep -v '^frontend/node_modules/'
```

Expected live baseline at handoff creation time:

```text
HEAD == origin/main == aa0e5b193a6296b81c2f2e610e9125d6858952c0
aa0e5b1 Sync apiClient focused no-DB test status
branch: main
```

Important: this file is created after `aa0e5b1`. If this handoff file is committed/pushed, live `HEAD` / `origin/main` will move to the handoff commit. Treat read-only recovery output as the source of truth.

## 2. PM rules and required context

Read and follow:

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`
- `docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`
- `docs/contracts/dashboard_api_contract.md`

PM rules still apply:

- Commit/push is PM-only and requires explicit user authorization.
- Use exact path allowlists only.
- Never use broad staging by default: do not use `git add .`, `git add -A` or `git add docs/`.
- Exclude pre-existing external dirty artifacts unless explicitly authorized.
- PASS WITH RECOMMENDATIONS closes a gate if there is no blocker; recommendations become carry-forward items.
- A review PASS does not authorize implementation, docs sync, stage, commit or push.

## 3. Current closed state

The following gates are closed:

```text
Sprint 3 Dashboard accepted-events no-DB vertical validation execution: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 Dashboard accepted-events no-DB vertical validation docs/status sync: PASS, commit b413876
PM handoff after Dashboard no-DB validation sync: PASS, commit c103e90
Sprint 3 Dashboard accepted-events apiClient focused no-DB test planning gate: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 Dashboard accepted-events apiClient focused no-DB tests implementation: CLOSED / PASS
Sprint 3 Dashboard accepted-events apiClient focused no-DB tests Reliability review: CLOSED / PASS
Sprint 3 Dashboard accepted-events apiClient focused no-DB tests Data Quality review: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 Dashboard accepted-events apiClient focused no-DB tests Verification review / exact evidence audit: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 Dashboard accepted-events apiClient focused no-DB tests exact-path commit/push: PASS, commit 96c0928
Sprint 3 Dashboard accepted-events apiClient focused no-DB tests docs/status sync: PASS, commit aa0e5b1
```

Current open gates at handoff creation time:

```text
None.
```

No review gate, execution gate, docs/status sync gate, commit gate or push gate is currently open at handoff creation time.

## 4. Recently completed work

Commit `96c0928` added focused accepted-events API client tests:

```text
96c0928970d9917e0a4142569ebbc8459d67cc3d Add focused accepted-events API client tests
```

Exact implementation commit allowlist:

```text
frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts
frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts
frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts
frontend/src/app/accepted-events/__tests__/page.test.tsx
```

Focused no-DB evidence reported by Architecture / Integration:

```text
apiClient.test.ts: 7 passed
query.test.ts: 12 passed
schema.test.ts: 26 passed
viewModel.test.ts: 3 passed
page.test.tsx: 8 passed
```

Review closeout:

```text
Reliability: CLOSED / PASS
Data Quality: CLOSED / PASS WITH RECOMMENDATIONS
Verification: CLOSED / PASS WITH RECOMMENDATIONS
```

Commit `aa0e5b1` synchronized status docs:

```text
aa0e5b193a6296b81c2f2e610e9125d6858952c0 Sync apiClient focused no-DB test status
```

Docs/status sync exact allowlist:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

## 5. Current dirty artifacts to preserve / exclude

Expected remaining dirty state after docs/status sync push:

```text
tracked diff:
.gitignore

untracked non-node_modules:
docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
docs/reports/phase1_to_sprint2_management_keynote_10p.html
docs/reports/sprint3_db_backed_api_validation_reliability_review.md
docs/thread_handoff/chatgpt_pm_handoff_20260624.md
docs/thread_handoff/chatgpt_pm_handoff_20260625.md
docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
frontend/node_modules/
```

Do not stage these by default:

```text
.gitignore
old handoff files
Keynote/report artifacts
sprint3_db_backed_api_validation_reliability_review.md
frontend/node_modules/
```

## 6. Still-valid implementation boundary

The Dashboard accepted-events consumer boundary remains:

- Dashboard/frontend only.
- Read-only consumer only.
- Only `GET /api/v2/production/accepted-station-events`.
- Query params only: `line_id`, `start_time`, `end_time`, `limit`, `cursor`.
- DTO allowlist only accepted fact fields from `production_accepted_station_event_fact`.
- No raw/debug/diagnostic/candidate/legacy fallback.
- No `work_order` / `product`.
- `accepted_at` means accepted fact timestamp only, not freshness / ACK / station freshness / `read_done`.
- Page summaries are current-page-only.
- Missing `line_id` / `start_time` / `end_time` fail closed before request.
- Invalid `limit` must fail closed.
- Cursor remains opaque and clears on line/time/limit scope changes.
- Invalid / expired / cross-scope cursor behavior must fail closed.
- Dashboard must not decode / mutate / construct cursor payload.
- No side effects beyond read-only frontend request construction/rendering.

Production fact source boundary remains:

- Only production fact source for DB/API/Dashboard consumers: `production_accepted_station_event_fact`.
- `raw_plc_sample`, `cycle_event`, `station_event`, `production_unit`, `quality_event`, `production_snapshot` and `production_events` must not be used as equivalent production fact sources, fallback sources, legacy compatibility sources or join-derived field fillers.
- Raw payload/raw hex/raw bytes/raw sample id, decoded/source normalized candidate payload, adapter disposition/reason/phase, candidate context, raw/normalized comparison context, decoder errors and diagnostic/review/audit payloads are diagnostic/review/debug only and must not enter production DTOs or Dashboard production facts.
- `ack_status`, `read_done`, `collector_state`, `quality_pareto_input`, `dashboard_state` and bare `result` / `defect` / `quality` / `pareto` keys remain forbidden in production consumer payloads and cursor payloads.
- NOK/detail fields may come only from accepted fact rows and must bind accepted upstream business evidence and shared station-event validation.

## 7. Carry-forward recommendations

Current carry-forward recommendation, non-blocking:

```text
Later separately authorize a defense-in-depth fixture for nested or renamed production-looking leakage variants.
```

Other future gates remain separate and require explicit PM/user authorization:

- Typecheck/build.
- Browser/manual smoke.
- API non-DB validation.
- DB-backed validation / `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`.
- Postgres/live DB work.
- Docker / docker compose / runtime/server startup.
- API/contract/DB/frontend production source edits.
- Optional debug/review diagnostics view.
- New migration.
- Deploy / tag / rollback / real PLC pilot.

## 8. What is not authorized now

At handoff creation time, the following are not authorized:

- Any implementation or repair.
- Test execution.
- API pytest.
- DB-backed validation.
- Postgres / live DB work.
- `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`.
- Browser/manual smoke.
- Docker / docker compose.
- Runtime/server startup.
- `npm run typecheck`.
- `npm run build`.
- Frontend/API/contract/package/DB edits.
- Docs/status edits.
- PM handoff edits after this file is committed, unless separately authorized.
- Deploy / tag / rollback.
- Real PLC pilot.
- Stage / commit / push.

## 9. Recommended next step

If the user wants to continue immediately, recommended next branch:

```text
No automatic next gate. Ask for explicit authorization.
```

Reason: implementation, reviews, exact-path commit/push and docs/status sync are closed. The next PM should either:

1. Start a new explicitly authorized planning gate for the non-blocking nested/renamed leakage defense-in-depth fixture; or
2. Start a separate PM-authorized validation branch such as typecheck/build, browser smoke, API non-DB or DB-backed validation; or
3. Keep the project idle and preserve the current clean baseline except external dirty artifacts.

## 10. Copyable restore prompt for next PM

```markdown
你是 Edge MES Demo 项目的 ChatGPT PM，请接手当前项目管理任务。

第一优先级：先恢复上下文，不要直接推进开发。

请先读取并遵守：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260708-2237.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
- docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md
- docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md
- docs/reports/sprint3_dashboard_api_implementation_plan.md
- docs/contracts/dashboard_api_contract.md

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

第一动作必须是 read-only recovery。不要编辑、不要运行 tests、不要连接 DB、不要启动 Docker/browser/runtime、不要 stage、不要 commit、不要 push。

执行：

    git status -sb
    printf '\n--- log -8 ---\n' && git log --oneline -8
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git rev-parse origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only
    printf '\n--- status all ---\n' && git status --short --untracked-files=all

Expected baseline at handoff creation time:

- HEAD / origin/main == aa0e5b193a6296b81c2f2e610e9125d6858952c0
- latest commit: aa0e5b1 Sync apiClient focused no-DB test status

注意：如果 handoff 文件已被 commit/push，live HEAD 会移动到 handoff commit。以 read-only recovery 的 live Git 结果为准。

当前关闭状态：

- Dashboard accepted-events apiClient focused no-DB tests implementation: CLOSED / PASS
- Reliability review: CLOSED / PASS
- Data Quality review: CLOSED / PASS WITH RECOMMENDATIONS
- Verification review: CLOSED / PASS WITH RECOMMENDATIONS
- exact-path implementation commit/push: PASS, commit 96c0928
- docs/status sync: PASS, commit aa0e5b1

当前没有挂起的 review gate、execution gate、docs/status sync gate、commit gate 或 push gate。

当前剩余 external dirty artifacts，应排除，不得 stage：

- .gitignore
- docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
- docs/reports/phase1_to_sprint2_management_keynote_10p.html
- docs/reports/sprint3_db_backed_api_validation_reliability_review.md
- docs/thread_handoff/chatgpt_pm_handoff_20260624.md
- docs/thread_handoff/chatgpt_pm_handoff_20260625.md
- docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
- docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
- frontend/node_modules/

不要 stage `.gitignore`、旧 handoff、Keynote/report artifacts、unrelated report 或 `frontend/node_modules/`。

当前 carry-forward recommendation：

- Later separately authorize a defense-in-depth fixture for nested or renamed production-looking leakage variants.

当前不授权：tests、DB、Docker、browser/runtime、typecheck/build、frontend/API/contract/package/DB edits、docs/status edits、stage/commit/push、deploy/tag/rollback/real PLC pilot。

完成 read-only recovery 和上下文恢复后报告：

1. live Git baseline 是否匹配；
2. dirty artifacts 是否只包含预期 external artifacts；
3. 当前 gate 状态；
4. 推荐下一步，但不要自动执行下一步。
```
