# ChatGPT PM Handoff — 2026-07-11 13:05 UTC+8

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
HEAD == origin/main == 19d2a2523ea0da3d124ad73d9ff999c84d45c2ab
19d2a25 Sync explicit-null regression status
branch: main
```

Important: this file is created after `19d2a25`. If this handoff file is later committed/pushed, live `HEAD` / `origin/main` will move to the handoff commit. Treat read-only recovery output as the source of truth.

## 2. PM rules and required context

Read and follow:

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260711-1305.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md`
- `docs/reports/sprint3_dashboard_accepted_events_envelope_contract_clarification_report.md`
- `docs/reports/sprint3_dashboard_accepted_events_item_required_key_contract_repair_report.md`
- `docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`
- `docs/reports/sprint3_dashboard_implementation_preparation_allowlist.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`

PM rules still apply:

- Commit/push is PM-only and requires explicit user authorization.
- Use exact path allowlists only.
- Never use broad staging by default: do not use `git add .`, `git add -A` or `git add docs/`.
- Exclude pre-existing external dirty artifacts unless explicitly authorized.
- `PASS WITH RECOMMENDATIONS` closes a gate when no blocker exists; recommendations become carry-forward items.
- A review PASS does not authorize implementation, tests, docs sync, stage, commit or push.
- Durable status baselines are audit markers; live Git recovery remains authoritative.

## 3. Current closed state

Dashboard accepted-events strict parser fail-closed hardening and the follow-on all-22-field explicit-null regression are fully closed.

```text
Strict parser planning gate:
CLOSED / initial HOLD because generic Envelope meta conflicted with endpoint response shape; repaired and closed

Exact-envelope contract clarification:
CLOSED / PASS

Exact-envelope Reliability contract review:
CLOSED / PASS WITH RECOMMENDATIONS, no blocker

Exact-envelope Data Quality contract review:
CLOSED / PASS WITH RECOMMENDATIONS, no blocker

Exact-envelope Verification contract review:
CLOSED / initial HOLD for item required/optional and missing/null ambiguity; repaired and closed

Item required-key/null contract repair:
CLOSED / PASS

Item required-key/null Data Quality targeted re-review:
CLOSED / PASS WITH RECOMMENDATIONS, no blocker

Item required-key/null Verification targeted re-review:
CLOSED / PASS WITH RECOMMENDATIONS, original blocker CLOSED

Strict parser implementation:
CLOSED / PASS

Reliability implementation review:
CLOSED / PASS, no blocker

Data Quality implementation review:
CLOSED / PASS WITH RECOMMENDATIONS, no blocker

Verification implementation review:
CLOSED / PASS WITH RECOMMENDATIONS, no blocker

Docs authority exact-path commit/push:
PASS, commit 7824063

Strict parser implementation exact-path commit/push:
PASS, commit 2cf616d

Strict parser post-push docs/status sync exact-path commit/push:
PASS, commit f784c91

PM handoff after strict parser closeout:
PASS, commit 9b47163

All-22-field explicit-null regression tests-only gate:
CLOSED / PASS

Explicit-null regression exact-path commit/push:
PASS, commit bdbcea0

Explicit-null regression post-push docs/status sync exact-path commit/push:
PASS, commit 19d2a25
```

Current open gates at handoff creation time:

```text
None.
```

No review, implementation, repair, test, docs/status sync, commit or push gate is open.

## 4. Recently completed work

### 4.1 Contract authority and strict parser implementation

Contract authority:

```text
7824063305cfaf4d44db6c8a01d095dd59586f10
7824063 Clarify Dashboard strict parser contract
```

Exact four-file scope:

```text
docs/contracts/dashboard_api_contract.md
docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md
docs/reports/sprint3_dashboard_accepted_events_envelope_contract_clarification_report.md
docs/reports/sprint3_dashboard_accepted_events_item_required_key_contract_repair_report.md
```

Strict parser implementation:

```text
2cf616d4dafbd497ec3db29ade826b1159e9025a
2cf616d Harden Dashboard accepted-events parser
```

Exact three-file scope:

```text
frontend/src/lib/acceptedStationEvents/schema.ts
frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts
frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
```

Frozen behavior:

- Endpoint-specific exact envelope only: outer `data` / `page`, data `items`, page `next_cursor` / `limit`.
- `meta` and all other unknown outer/data/page/item keys are unsupported.
- All 22 accepted-event DTO keys are required own keys.
- Required means key presence, not non-null value.
- Nullable values are represented by explicit JSON `null`; missing is not equivalent to explicit `null`.
- Missing or unknown keys in a 2xx response make the response malformed and fail closed.
- Malformed 2xx remains client `kind: "error"`.
- Silent stripping, normalization, defaulting, fallback, partial parsing and nested-field salvage are forbidden.
- `apiClient.ts` was not modified; no retry, second request or fallback endpoint was introduced.
- No API, DB, Collector, runtime, viewModel, page, store, cache, package or config changes occurred.

Strict-parser implementation focused evidence:

```text
schema.test.ts: 143 passed
apiClient.test.ts: 12 passed
git diff --cached --check: PASS
```

These were focused no-DB frontend tests only. Full frontend suite, typecheck, build, browser smoke, API tests and DB-backed tests were not run for that branch.

### 4.2 Follow-on all-22-field explicit-null regression

Tests-only commit:

```text
bdbcea0707941b4ca98f3fe4393bbbfae98a3764
bdbcea0 Add explicit-null accepted event coverage
```

Exact one-file scope:

```text
frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts
```

The parameterized regression covers all 22 required DTO fields one at a time with explicit JSON `null` and proves:

- the required own key remains present;
- the item retains exactly 22 keys;
- the field remains `null` without defaulting or normalization;
- the parsed item exactly matches the input item.

Focused evidence:

```text
schema.test.ts: 165 passed
git diff --check -- frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts: PASS
```

No production code, API, DB, Collector, runtime, viewModel, page, store, cache, contract or package/config changed. The full frontend suite, `apiClient.test.ts`, typecheck, build, browser smoke, API tests and DB tests were not run by this follow-on gate.

### 4.3 Post-push docs/status sync

```text
19d2a2523ea0da3d124ad73d9ff999c84d45c2ab
19d2a25 Sync explicit-null regression status
```

Exact three-file scope:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

The sync records:

- live authoring-time baseline `bdbcea0`;
- tests-only gate `CLOSED / PASS`;
- `schema.test.ts: 165 passed` focused evidence;
- exact one-file test scope and no production-code change;
- separate preservation of the strict-parser implementation evidence `143 + 12`;
- closure of the former optional all-22-field explicit-null recommendation;
- remaining carry-forward limited to UI/state stale-data protection and separately planned validation branches.

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
?? docs/thread_handoff/chatgpt_pm_handoff_260711-1305.md
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
docs/thread_handoff/chatgpt_pm_handoff_260711-1305.md
```

## 6. Still-valid Dashboard accepted-events boundary

The Dashboard accepted-events consumer boundary remains:

- Dashboard/frontend read-only consumer only.
- Only `GET /api/v2/production/accepted-station-events`.
- Query parameters only: `line_id`, `start_time`, `end_time`, `limit`, `cursor`.
- DTO allowlist only accepted fact fields from `production_accepted_station_event_fact`.
- Response envelope must be exact and fail closed on unsupported keys.
- Each item must contain the exact 22-key DTO set.
- Missing required keys are malformed; explicit `null` remains valid and is now field-by-field regression tested.
- No raw/debug/diagnostic/candidate/review/audit/legacy fallback.
- No `work_order` / `product`.
- `accepted_at` means accepted fact timestamp only, not freshness, ACK, station freshness or `read_done` time.
- Page summaries remain current-page-only.
- Missing required query scope and invalid `limit` fail closed before request.
- Cursor remains opaque and clears on line/time/limit scope changes.
- Invalid / expired / cross-scope cursor behavior remains fail closed.
- Dashboard must not decode, mutate or construct cursor payload.
- No side effects beyond the read-only frontend request and rendering path.

Production fact source boundary remains:

- Only `production_accepted_station_event_fact` is the consumer-facing production fact authority.
- `raw_plc_sample`, `cycle_event`, `station_event`, `production_unit`, `quality_event`, `production_snapshot` and `production_events` are not equivalent production fact sources, fallbacks or join-derived field fillers.
- Raw payload/raw hex/raw bytes/raw sample id, normalized candidate payload, adapter disposition/reason/phase, candidate context, raw-normalized comparison context, decoder errors and diagnostic/review/audit payloads must not enter production DTOs.
- `ack_status`, `read_done`, `collector_state`, `quality_pareto_input`, `dashboard_state` and bare result/defect/quality/pareto fields remain forbidden.
- Renamed, camelCase and production-looking aliases remain excluded.
- NOK/detail fields may come only from accepted fact rows and valid upstream business evidence.

## 7. Carry-forward recommendations

The former recommendations for strict envelope fail-closed hardening and all-22-field explicit-null parameterization are CLOSED.

Remaining non-blocking recommendations:

1. Separate future UI/state gate: ensure a parser/client error cannot present old successful data or cache as fresh production truth.
2. Separately planned validation branches may cover typecheck/build, browser smoke, API non-DB validation or DB-backed validation.

These are not open gates and do not constitute authorization.

## 8. What is not authorized now

At handoff creation time, the following are not authorized:

- Any implementation or repair.
- Test execution.
- Full frontend suite.
- `npm run typecheck` or `npm run build`.
- Browser/manual smoke.
- API pytest or API changes.
- DB-backed validation or `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`.
- Postgres/live DB work.
- Docker / docker compose / runtime/server startup.
- Frontend, API, contract, package, DB, Collector or runtime edits.
- Docs/status edits.
- UI/state stale-data implementation.
- Deploy, tag, rollback or real PLC pilot.
- Any stage/commit/push outside the exact handoff path authorized for this gate.

## 9. Recommended next step

No automatic next gate.

The next PM should first complete read-only recovery and then report the live state before recommending one of these options:

1. keep the project idle at the fully closed explicit-null baseline;
2. open a separate Level 1 UI/state stale-data planning gate;
3. plan a separate validation branch such as typecheck/build, browser smoke, API non-DB or DB-backed validation.

Do not automatically execute any option.

## 10. Copyable restore prompt for next PM

```markdown
你是 Edge MES Demo 项目的 ChatGPT PM，请接手当前项目管理任务。

第一优先级：先恢复上下文，不要直接推进开发。

请先读取并遵守：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260711-1305.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
- docs/contracts/dashboard_api_contract.md
- docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md
- docs/reports/sprint3_dashboard_accepted_events_envelope_contract_clarification_report.md
- docs/reports/sprint3_dashboard_accepted_events_item_required_key_contract_repair_report.md

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

- HEAD / origin/main == 19d2a2523ea0da3d124ad73d9ff999c84d45c2ab
- latest commit: 19d2a25 Sync explicit-null regression status

注意：如果handoff文件已被commit/push，live HEAD会移动到handoff commit。以read-only recovery的live Git结果为准。

当前关闭状态：

- Dashboard accepted-events strict parser planning/contract/implementation链路：CLOSED
- docs authority exact-path commit/push：PASS，commit 7824063
- strict parser implementation exact-path commit/push：PASS，commit 2cf616d
- strict parser post-push docs/status sync：PASS，commit f784c91
- strict parser PM handoff：PASS，commit 9b47163
- all-22-field explicit-null regression tests-only gate：CLOSED / PASS
- focused evidence：schema.test.ts 165 passed
- explicit-null regression exact-path commit/push：PASS，commit bdbcea0
- explicit-null regression post-push docs/status sync：PASS，commit 19d2a25

当前没有挂起的review、implementation、repair、test、docs/status sync、commit或push gate。

当前剩余external dirty artifacts，应排除，不得stage：

- .gitignore
- docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
- docs/reports/phase1_to_sprint2_management_keynote_10p.html
- docs/reports/sprint3_db_backed_api_validation_reliability_review.md
- docs/thread_handoff/chatgpt_pm_handoff_20260624.md
- docs/thread_handoff/chatgpt_pm_handoff_20260625.md
- docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
- docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
- frontend/node_modules/

新handoff文件如果尚未提交：

- docs/thread_handoff/chatgpt_pm_handoff_260711-1305.md

不要stage `.gitignore`、旧handoff、Keynote/report artifacts、unrelated report或`frontend/node_modules/`。

当前非阻塞carry-forward：

- separate UI/state stale-data gate；
- separately planned typecheck/build/browser/API/DB-backed validation。

当前不授权：implementation、tests、DB、Docker、browser/runtime、typecheck/build、frontend/API/contract/package/DB/docs edits、deploy/tag/rollback/real PLC pilot，以及任何未经单独批准的stage/commit/push。

完成read-only recovery和上下文恢复后报告：

1. live Git baseline；
2. baseline是否匹配handoff创建时的审计标记，或是否因handoff commit而前移；
3. dirty artifacts是否只包含预期external artifacts及可能未提交的新handoff；
4. 当前gate状态；
5. 推荐下一步，但不要自动执行下一步。
```
