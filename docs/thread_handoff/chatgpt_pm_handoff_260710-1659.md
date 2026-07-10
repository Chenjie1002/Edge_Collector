# ChatGPT PM Handoff — 2026-07-10 16:59 UTC+8

Project: Edge MES Demo
Path: `/Users/chenjie/Documents/MES/edge-mes-demo`
Thread role: ChatGPT PM

## 1. First action for next PM: read-only recovery

下一位 PM 必须先执行 read-only recovery。恢复完成前，不要编辑文件、运行 tests、连接 DB、启动 Docker/browser/server/runtime、运行 typecheck/build、stage、commit 或 push。

执行：

```bash
git status -sb
printf '\n--- log -8 ---\n' && git log --oneline -8
printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
printf '\n--- origin/main ---\n' && git rev-parse origin/main
printf '\n--- diff name-only ---\n' && git diff --name-only
printf '\n--- cached name-only ---\n' && git diff --cached --name-only
printf '\n--- status all ---\n' && git status --short --untracked-files=all
```

Expected live baseline at handoff creation time:

```text
HEAD == origin/main == d231a6af0c59555f449d882a45a81b0dcc284914
d231a6a Sync nested leakage fixture status
branch: main
```

Important: this file is created after `d231a6a`. If this handoff file is later committed/pushed, live `HEAD` / `origin/main` will move to the handoff commit. Treat read-only recovery output as the source of truth.

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
- `PASS WITH RECOMMENDATIONS` closes a gate when there is no blocker; recommendations become carry-forward items.
- A review PASS does not authorize implementation, tests, docs sync, stage, commit or push.

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
Sprint 3 Dashboard accepted-events nested/renamed leakage defense-in-depth fixture implementation: CLOSED / PASS
Sprint 3 Dashboard accepted-events nested/renamed leakage defense-in-depth fixture Reliability review: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 Dashboard accepted-events nested/renamed leakage defense-in-depth fixture Data Quality review: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 Dashboard accepted-events nested/renamed leakage defense-in-depth fixture Verification review / exact evidence audit: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 Dashboard accepted-events nested/renamed leakage defense-in-depth fixture exact-path commit/push: PASS, commit 244a6dd
Sprint 3 Dashboard accepted-events nested/renamed leakage defense-in-depth fixture docs/status sync: PASS, commit d231a6a
```

Current open gates at handoff creation time:

```text
None.
```

No review gate, execution gate, docs/status sync gate, commit gate or push gate is currently open at handoff creation time.

## 4. Recently completed work

### 4.1 Defense-in-depth fixture implementation

Commit `244a6dd` added nested/renamed production-looking leakage fixtures:

```text
244a6dd82b294f695aaf2bf6a6a849d7ad94dcb6 Harden Dashboard leakage fixtures
```

Exact implementation commit allowlist:

```text
frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts
frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts
```

Focused no-DB evidence reported by Architecture / Integration:

```text
schema.test.ts: 49 passed
viewModel.test.ts: 4 passed
git diff --check -- frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts: PASS
```

Review closeout:

```text
Reliability: CLOSED / PASS WITH RECOMMENDATIONS
Data Quality: CLOSED / PASS WITH RECOMMENDATIONS
Verification: CLOSED / PASS WITH RECOMMENDATIONS
Blockers: none
```

The implementation remained tests-only. It did not modify production source, API, contract, DB, package/config, docs/status, Docker/runtime/browser surfaces or deployment behavior.

### 4.2 Docs/status sync

Commit `d231a6a` synchronized durable status docs:

```text
d231a6af0c59555f449d882a45a81b0dcc284914 Sync nested leakage fixture status
```

Docs/status sync exact allowlist:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

The docs/status sync records:

- fixture implementation/review/commit/push closed state;
- implementation evidence of 49 + 4 focused tests;
- exact two-test-file scope;
- future strict parser fail-closed recommendation;
- no current blocker.

## 5. Current dirty artifacts to preserve / exclude

Expected remaining dirty state before this handoff file is staged:

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
docs/thread_handoff/chatgpt_pm_handoff_260710-1659.md
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

For a later handoff commit gate, the only eligible exact path is:

```text
docs/thread_handoff/chatgpt_pm_handoff_260710-1659.md
```

## 6. Still-valid Dashboard accepted-events boundary

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
- Renamed/camelCase and production-looking aliases must remain excluded from accepted fact DTO/viewModel/render evidence.
- NOK/detail fields may come only from accepted fact rows and must bind accepted upstream business evidence and shared station-event validation.

## 7. Carry-forward recommendation

Current non-blocking recommendation:

```text
Later separately authorize a strict parser contract hardening slice so
parseAcceptedStationEventsEnvelope() fails closed on unsupported
envelope/data/page-level keys instead of only stripping/not returning them.
```

This recommendation is not an open gate and is not current implementation authorization.

A future strict parser slice should be treated as a new exact-scope gate. It may require production parser changes, so the next PM must first classify whether the scope is Level 1 or Level 2 based on the proposed authority/contract impact. Do not infer repair authorization from the current recommendation.

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
- Deploy / tag / rollback.
- Real PLC pilot.
- Stage / commit / push of this handoff until the user explicitly authorizes the exact path.

## 9. Recommended next step

No automatic next gate.

The next PM should first complete read-only recovery and then ask for explicit user authorization before starting one of these branches:

1. exact-path stage/commit/push for this handoff file, if not already committed;
2. a separately planned strict envelope/data/page fail-closed parser hardening gate;
3. a separately authorized validation branch such as typecheck/build, browser smoke, API non-DB or DB-backed validation;
4. keep the project idle and preserve the current baseline except external dirty artifacts.

## 10. Copyable restore prompt for next PM

```markdown
你是 Edge MES Demo 项目的 ChatGPT PM，请接手当前项目管理任务。

第一优先级：先恢复上下文，不要直接推进开发。

请先读取并遵守：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260710-1659.md
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

- HEAD / origin/main == d231a6af0c59555f449d882a45a81b0dcc284914
- latest commit: d231a6a Sync nested leakage fixture status

注意：如果 handoff 文件已被 commit/push，live HEAD 会移动到 handoff commit。以 read-only recovery 的 live Git 结果为准。

当前关闭状态：

- Dashboard accepted-events nested/renamed leakage defense-in-depth fixture implementation: CLOSED / PASS
- Reliability review: CLOSED / PASS WITH RECOMMENDATIONS
- Data Quality review: CLOSED / PASS WITH RECOMMENDATIONS
- Verification review / exact evidence audit: CLOSED / PASS WITH RECOMMENDATIONS
- exact-path implementation commit/push: PASS, commit 244a6dd
- docs/status sync commit/push: PASS, commit d231a6a

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

- Later separately authorize strict parser contract hardening so `parseAcceptedStationEventsEnvelope()` fails closed on unsupported envelope/data/page-level keys instead of only stripping/not returning them.

当前不授权：tests、DB、Docker、browser/runtime、typecheck/build、frontend/API/contract/package/DB edits、docs/status edits、stage/commit/push、deploy/tag/rollback/real PLC pilot。

完成 read-only recovery 和上下文恢复后报告：

1. live Git baseline 是否匹配；
2. dirty artifacts 是否只包含预期 external artifacts；
3. 当前 gate 状态；
4. 推荐下一步，但不要自动执行下一步。
```
