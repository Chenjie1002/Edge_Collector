# ChatGPT PM Handoff — 2026-07-11 18:02 UTC+8

Project: Edge MES Demo
Path: `/Users/chenjie/Documents/MES/edge-mes-demo`
Thread role: ChatGPT PM

## 1. First action for next PM: read-only recovery

下一位 PM 必须先执行 read-only recovery。恢复完成前，不要编辑文件、运行 tests、连接 DB、启动 Docker/browser/server/runtime、运行 typecheck/build、stage、commit 或 push。

执行：

```bash
git status -sb
printf '\n--- log -12 ---\n' && git log --oneline -12
printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
printf '\n--- origin/main ---\n' && git rev-parse origin/main
printf '\n--- diff name-only ---\n' && git diff --name-only
printf '\n--- cached name-only ---\n' && git diff --cached --name-only
printf '\n--- status all ---\n' && git status --short --untracked-files=all
```

Expected live baseline at handoff creation time:

```text
HEAD == origin/main == ee45f4b5314be80f643fa00ca12ea91e4ada94cb
ee45f4b Sync Dashboard frontend build validation status
branch: main
cached diff: empty
```

Important: this file is created after `ee45f4b`. If this handoff file is later committed/pushed, live `HEAD` / `origin/main` will move to the handoff commit. Treat the new Thread's read-only recovery output as the source of truth.

## 2. PM rules and required context

Read and follow:

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260711-1802.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`
- `docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md`
- `docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`
- `docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md`
- `docs/reports/sprint3_dashboard_accepted_events_envelope_contract_clarification_report.md`
- `docs/reports/sprint3_dashboard_accepted_events_item_required_key_contract_repair_report.md`
- `docs/reports/sprint3_dashboard_ui_state_stale_data_plan.md`
- `docs/reports/sprint3_dashboard_frontend_typecheck_build_validation_plan.md`

PM rules still apply:

- Commit/push is PM-only and requires explicit user authorization.
- Use exact path allowlists only.
- Never use broad staging by default: do not use `git add .`, `git add -A` or `git add docs/`.
- Exclude pre-existing external dirty artifacts unless explicitly authorized.
- `PASS WITH RECOMMENDATIONS` closes a gate when no blocker exists; recommendations become carry-forward items.
- A review or execution PASS does not authorize implementation, tests, docs sync, stage, commit, push, browser/server/runtime, DB or deployment work.
- Durable status baselines are audit markers; live Git recovery remains authoritative.
- Browser/manual smoke is a new independent gate. Do not infer its authorization from the closed typecheck/build gate.

## 3. Current closed state

The current Dashboard accepted-events safety, parser, stale-data and frontend compile/build validation chain is closed.

```text
Dashboard accepted-events frontend implementation:
CLOSED / PASS WITH RECOMMENDATIONS
implementation commit: 896c2d1

Dashboard accepted-events vertical validation planning:
CLOSED / PASS WITH RECOMMENDATIONS
planning commit: dd6dc53

Dashboard accepted-events no-DB vertical validation execution:
CLOSED / PASS WITH RECOMMENDATIONS

Dashboard accepted-events apiClient focused no-DB tests:
CLOSED / PASS
commit: 96c0928

Dashboard accepted-events nested/renamed leakage defense-in-depth fixture:
CLOSED / PASS
commit: 244a6dd

Dashboard accepted-events strict parser planning/contract/implementation chain:
CLOSED

Strict parser docs authority exact-path commit/push:
PASS, commit 7824063

Strict parser implementation exact-path commit/push:
PASS, commit 2cf616d

Strict parser post-push docs/status sync:
PASS, commit f784c91

PM handoff after strict parser closeout:
PASS, commit 9b47163

All-22-field explicit-null regression tests-only gate:
CLOSED / PASS
focused evidence: schema.test.ts 165 passed
commit: bdbcea0

Explicit-null regression docs/status sync:
PASS, commit 19d2a25

Dashboard UI/state stale-data planning gate:
CLOSED / PASS WITH RECOMMENDATIONS
planning authority commit: 156a812

Dashboard UI/state stale-data tests-only Verification gate:
CLOSED / PASS
focused evidence: page.test.tsx 14 passed
commit: 963218a

Dashboard UI/state stale-data docs/status sync:
PASS, commit 51c9e9e

Dashboard frontend typecheck/build planning gate:
CLOSED / PASS WITH RECOMMENDATIONS
planning authority commit: 2a88ffe

Dashboard frontend typecheck/build Verification execution:
CLOSED / PASS

Dashboard frontend typecheck/build docs/status sync:
PASS, commit ee45f4b
```

Current open gates at handoff creation time:

```text
None.
```

No review, implementation, repair, test, browser/manual smoke, docs/status sync, commit or push gate is open.

## 4. Recently completed work

### 4.1 UI/state stale-data regression closeout

Planning authority:

```text
156a812bf4529e198ca32373d7d109370a6e3e0d
156a812 Plan Dashboard stale-data regression coverage
```

Planning report:

```text
docs/reports/sprint3_dashboard_ui_state_stale_data_plan.md
```

Tests-only implementation:

```text
963218a098e97b5d3c4993f2913e5f7f7355f98e
963218a Add Dashboard stale-data regression coverage
```

Exact implementation file:

```text
frontend/src/app/accepted-events/__tests__/page.test.tsx
```

Focused evidence:

```text
page.test.tsx: 14 passed
```

Covered transitions include:

- ready to loading;
- ready to error;
- ready to unavailable;
- ready to invalid query;
- non-empty ready to empty ready;
- client error/unavailable results rendering no stale production surfaces.

The tests prove prior table, current-page summary, NOK/detail evidence, trace references, selected truth and distinctive old values do not remain visible as fresh production truth after non-ready or empty transitions.

No production source, API, DB, Collector, runtime, contract, package or config changed.

Post-push durable docs/status sync:

```text
51c9e9eb0743d0451fb578d56ff8b4016d9e6565
51c9e9e Sync Dashboard stale-data regression status
```

Exact files:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

### 4.2 Frontend typecheck/build planning authority

Planning authority:

```text
2a88ffec6dd528b52e104f75f0395f7ecf0bfe2e
2a88ffe Plan Dashboard frontend typecheck build validation
```

Exact file:

```text
docs/reports/sprint3_dashboard_frontend_typecheck_build_validation_plan.md
```

Planning conclusion:

```text
Level 1 — commands-only frontend validation
Owner: Verification
Planning: CLOSED / PASS WITH RECOMMENDATIONS
Expected implementation files: none
```

Frozen execution order:

1. read-only preflight;
2. `npm run typecheck`;
3. immediate tracked/generated-artifact audit;
4. exact typecheck artifact cleanup;
5. `npm run build` only if typecheck lane passes;
6. immediate tracked/generated-artifact audit;
7. exact build artifact cleanup;
8. final restoration audit.

Historical risk preserved in the plan:

- `next build` had previously mutated `frontend/tsconfig.json` by adding `"incremental": true`;
- command exit 0 is insufficient if any tracked config/source/test/package drift occurs;
- broad cleanup such as `git clean -fd`, `git clean -fdx` or broad `rm` is forbidden.

### 4.3 Frontend typecheck/build Verification execution

Verification report conclusion:

```text
PASS
```

The previous Verification Thread and ChatGPT PM both executed and verified the commands on the then-current source baseline.

Environment:

```text
node: v22.23.0
npm: 11.17.0
```

Typecheck:

```text
npm run typecheck
tsc --noEmit
exit code 0
```

Typecheck generated only:

```text
frontend/tsconfig.tsbuildinfo
```

It was precisely removed after evidence capture.

Build:

```text
npm run build
next build
exit code 0
```

Build routes:

```text
/_not-found
/accepted-events
```

Build generated only the allowed paths:

```text
frontend/.next/
frontend/next-env.d.ts
```

`frontend/tsconfig.tsbuildinfo` was also an allowed transient in the overall gate when produced. All allowed transient artifacts were precisely cleaned.

Tracked-drift result:

```text
frontend/package.json: unchanged
frontend/package-lock.json: unchanged
frontend/tsconfig.json: unchanged
frontend/next.config.ts: unchanged
frontend/src/**: unchanged
cached diff: empty
final frontend status excluding node_modules: empty
```

No tests, dependency install, frontend server, browser, API/DB, Docker, source/config repair, stage, commit or push occurred in the Verification execution gate.

Because the gate was commands-only and no tracked file changed, there is no implementation commit.

### 4.4 Frontend typecheck/build durable docs/status sync

```text
ee45f4b5314be80f643fa00ca12ea91e4ada94cb
ee45f4b Sync Dashboard frontend build validation status
```

Exact three-file scope:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

The sync records:

- planning authority `2a88ffe`;
- typecheck/build Verification `CLOSED / PASS`;
- `tsc --noEmit` and `next build` exit 0;
- routes `/_not-found` and `/accepted-events`;
- zero tracked frontend drift;
- generated-artifact allowlist and exact cleanup;
- final frontend status restored;
- no implementation commit;
- remaining validation branches limited to browser/manual smoke, API no-DB and API DB-backed validation.

## 5. Current dirty artifacts to preserve / exclude

Expected remaining dirty state after this handoff file is created and before it is staged:

```text
tracked diff:
M .gitignore

untracked non-node_modules:
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
?? docs/thread_handoff/chatgpt_pm_handoff_260711-1802.md
?? frontend/node_modules/
```

Do not stage these by default:

```text
.gitignore
old untracked handoff files
Keynote/report artifacts
sprint3_db_backed_api_validation_reliability_review.md
frontend/node_modules/
```

For this handoff commit gate, the only eligible exact path is:

```text
docs/thread_handoff/chatgpt_pm_handoff_260711-1802.md
```

## 6. Still-valid Dashboard accepted-events boundary

The Dashboard accepted-events consumer boundary remains:

- Dashboard/frontend read-only consumer only.
- Only `GET /api/v2/production/accepted-station-events`.
- Query parameters only: `line_id`, `start_time`, `end_time`, `limit`, `cursor`.
- DTO allowlist only accepted fact fields from `production_accepted_station_event_fact`.
- Response envelope must be exact and fail closed on unsupported keys.
- Outer keys are only `data` and `page`; `data` requires only `items`; `page` requires only `next_cursor` and `limit`.
- `meta` is unsupported.
- Each item must contain the exact 22-key DTO set.
- Missing required keys are malformed; explicit JSON `null` remains valid and is field-by-field regression tested.
- No silent strip, normalization, defaulting, fallback, partial parsing or nested-field salvage.
- No raw/debug/diagnostic/candidate/review/audit/legacy fallback.
- No `work_order` / `product`.
- `accepted_at` means accepted fact timestamp only, not freshness, ACK, station freshness or `read_done` time.
- Page summaries remain current-page-only.
- Missing required query scope and invalid `limit` fail closed before request.
- Cursor remains opaque and clears on line/time/limit scope changes.
- Invalid / expired / cross-scope cursor behavior remains fail closed.
- Dashboard must not decode, mutate or construct cursor payload.
- No side effects beyond the read-only frontend request and rendering path.
- UI/state transitions must not present old success data as fresh production truth.

Production fact source boundary remains:

- Only `production_accepted_station_event_fact` is the consumer-facing production fact authority.
- `raw_plc_sample`, `cycle_event`, `station_event`, `production_unit`, `quality_event`, `production_snapshot` and `production_events` are not equivalent production fact sources, fallbacks or join-derived field fillers.
- Raw payload/raw hex/raw bytes/raw sample id, normalized candidate payload, adapter disposition/reason/phase, candidate context, raw-normalized comparison context, decoder errors and diagnostic/review/audit payloads must not enter production DTOs.
- `ack_status`, `read_done`, `collector_state`, `quality_pareto_input`, `dashboard_state` and bare result/defect/quality/pareto fields remain forbidden.
- Renamed, camelCase and production-looking aliases remain excluded.
- NOK/detail fields may come only from accepted fact rows and valid upstream business evidence.

## 7. Carry-forward and recommended next branch

The following recommendations are closed and must not be re-described as future work:

- strict parser exact-envelope hardening;
- all-22-field explicit-null parameterization;
- UI/state stale-data regression coverage;
- current-baseline frontend typecheck/build validation.

Remaining separately planned validation branches:

1. browser/manual smoke;
2. API no-DB consolidated validation;
3. API DB-backed consolidated validation.

The user and current PM selected the next recommended substantive branch as:

```text
Level 1 — Dashboard browser/manual smoke planning gate
Owner: Architecture / Integration
Mode: planning-only
```

This is a recommendation and handoff target, not active authorization. The next PM must first perform read-only recovery, confirm the handoff, report current state, and wait for explicit user authorization before editing a planning report or starting any server/browser process.

Expected planning topics for that future gate include:

- mock API versus separately authorized local API target;
- exact frontend server command and port;
- browser automation versus manual evidence;
- invalid query, loading, empty, unavailable, successful page, cursor and scope-change scenarios;
- stale-data visible evidence;
- screenshots/log evidence and privacy boundaries;
- server/build/generated-artifact cleanup;
- no DB, Docker, deploy or production credential use by default;
- exact stop/HOLD rules;
- separation between planning and execution authorization.

## 8. What is not authorized now

At handoff creation time, the following are not authorized:

- Browser/manual smoke planning edits.
- Browser/manual smoke execution.
- Frontend server or preview startup.
- Browser automation or screenshot capture.
- Any source, test, config, package or lockfile change.
- Any implementation or repair.
- Any test execution.
- `npm run typecheck` or `npm run build` rerun.
- `npm ci`, install, update or dependency repair.
- API pytest or API changes.
- DB-backed validation or `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`.
- Postgres/live DB/SSH tunnel work.
- Docker / docker compose / Collector / V-PLC / real PLC work.
- Docs/status edits.
- Deploy, tag or rollback.
- Any stage/commit/push outside the exact handoff path if separately authorized.

## 9. Handoff file commit gate

This handoff file is not staged automatically.

If the user authorizes exact-path commit/push, PM may stage only:

```text
docs/thread_handoff/chatgpt_pm_handoff_260711-1802.md
```

Required staged-set audit:

```bash
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

Suggested commit message:

```text
Add PM handoff before browser smoke planning
```

Do not stage `.gitignore`, old handoff files, reporting artifacts, unrelated docs or `frontend/node_modules/`.

## 10. Copyable restore prompt for next PM

```markdown
你是 Edge MES Demo 项目的 ChatGPT PM，请接手当前项目管理任务。

第一优先级：先恢复上下文，不要直接推进开发。

请先读取并遵守：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260711-1802.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
- docs/contracts/dashboard_api_contract.md
- docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md
- docs/reports/sprint3_dashboard_ui_state_stale_data_plan.md
- docs/reports/sprint3_dashboard_frontend_typecheck_build_validation_plan.md

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

第一动作必须是 read-only recovery。不要编辑、不要运行 tests、不要连接 DB、不要启动 Docker/browser/server/runtime、不要运行 typecheck/build、不要 stage、不要 commit、不要 push。

执行：

    git status -sb
    printf '\n--- log -12 ---\n' && git log --oneline -12
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git rev-parse origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only
    printf '\n--- status all ---\n' && git status --short --untracked-files=all

Expected baseline at handoff creation time:

- HEAD / origin/main == ee45f4b5314be80f643fa00ca12ea91e4ada94cb
- latest commit: ee45f4b Sync Dashboard frontend build validation status
- branch: main
- cached diff: empty

注意：如果 handoff 文件已被 commit/push，live HEAD 会移动到 handoff commit。以 read-only recovery 的 live Git 结果为准。

当前关闭状态：

- Dashboard accepted-events frontend implementation：CLOSED / PASS WITH RECOMMENDATIONS，commit 896c2d1
- no-DB vertical validation：CLOSED / PASS WITH RECOMMENDATIONS
- apiClient focused no-DB tests：CLOSED / PASS，commit 96c0928
- nested/renamed leakage fixture：CLOSED / PASS，commit 244a6dd
- strict parser planning/contract/implementation chain：CLOSED
- strict parser docs authority：PASS，commit 7824063
- strict parser implementation：PASS，commit 2cf616d
- all-22-field explicit-null regression：CLOSED / PASS，commit bdbcea0，schema.test.ts 165 passed
- UI/state stale-data planning：CLOSED / PASS WITH RECOMMENDATIONS，commit 156a812
- UI/state stale-data tests-only Verification：CLOSED / PASS，commit 963218a，page.test.tsx 14 passed
- frontend typecheck/build planning：CLOSED / PASS WITH RECOMMENDATIONS，commit 2a88ffe
- frontend typecheck/build Verification：CLOSED / PASS
- typecheck/build evidence：tsc --noEmit exit 0；next build exit 0；zero tracked drift；generated artifacts cleaned
- frontend typecheck/build docs/status sync：PASS，commit ee45f4b

当前没有挂起的 review、implementation、repair、test、browser/manual smoke、docs/status sync、commit 或 push gate。

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

新 handoff 文件如果尚未提交：

- docs/thread_handoff/chatgpt_pm_handoff_260711-1802.md

不要 stage `.gitignore`、旧 handoff、Keynote/report artifacts、unrelated report 或 `frontend/node_modules/`。

推荐的下一实质候选任务：

    Level 1 — Dashboard browser/manual smoke planning gate
    Owner: Architecture / Integration
    planning-only

这只是推荐，不构成授权。不要自动编辑 planning report，也不要启动 server/browser。

当前不授权：implementation、tests、typecheck/build rerun、browser/manual smoke、server、API/DB、Docker、frontend/API/contract/package/DB/docs edits、deploy/tag/rollback/real PLC pilot，以及任何未经单独批准的 stage/commit/push。

完成 read-only recovery 和上下文恢复后报告：

1. live Git baseline；
2. baseline 是否匹配 handoff 创建时的审计标记，或是否因 handoff commit 而前移；
3. dirty artifacts 是否只包含预期 external artifacts及可能未提交的新 handoff；
4. 当前 gate 状态；
5. browser/manual smoke planning 的推荐 scope、风险等级和需用户授权的第一动作，但不要自动执行。
```
