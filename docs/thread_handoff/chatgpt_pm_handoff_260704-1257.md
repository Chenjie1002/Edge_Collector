# Edge MES Demo — ChatGPT PM Handoff 260704-1257

## 0. Role / first instruction for next PM

You are taking over the Edge MES Demo project PM role.

Project path:

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

First action must be read-only recovery. Do not edit, do not run tests, do not connect to DB, do not start Docker, do not stage, do not commit, and do not push before recovery.

Run:

```bash
git status -sb
printf '\n--- log -12 ---\n' && git log --oneline -12
printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
printf '\n--- origin/main ---\n' && git rev-parse origin/main
printf '\n--- diff name-only ---\n' && git diff --name-only
printf '\n--- cached name-only ---\n' && git diff --cached --name-only
printf '\n--- status all ---\n' && git status --short --untracked-files=all
```

Expected live baseline at handoff creation:

```text
HEAD == origin/main == 2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e
latest commit:
2cfad5d Add API DB-backed schema verification
cached name-only == empty
```

Important baseline rule: live `HEAD` / `origin/main` must still be verified. Historical baselines in durable docs are audit markers and are not HOLD by themselves after later authorized commits.

## 1. Current repository state at handoff creation

Last verified immediately before this handoff file was created:

```text
branch: main
HEAD / origin/main: 2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e
latest commit: 2cfad5d Add API DB-backed schema verification
cached: empty
```

Expected external dirty artifacts to continue excluding:

```text
M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

This handoff file is newly created in the current task:

```text
docs/thread_handoff/chatgpt_pm_handoff_260704-1257.md
```

Until it is explicitly committed, expect it to appear as an additional untracked file. If PM authorizes a handoff commit gate, stage only this exact file and continue excluding `.gitignore`, old PM handoff files and Keynote/reporting artifacts.

Strictly forbidden unless separately authorized:

```text
git add .
git add -A
git add docs/
git add db/
```

## 2. What just closed

The following sequence is CLOSED / PASS unless noted otherwise:

```text
DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync: CLOSED / PASS, commit 64d0e12
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Reliability Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Data Quality Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Verification Review / Exact Future Run Allowlist Audit: CLOSED / HOLD, blocker B1
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair: CLOSED / PASS, no blocker
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair Verification Re-review: CLOSED / PASS WITH RECOMMENDATIONS, blocker B1 CLOSED
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair exact-path commit/push: CLOSED / PASS, commit 2cfad5d
```

Latest pushed commit:

```text
2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e Add API DB-backed schema verification
```

Committed file in latest repair:

```text
api/tests/test_accepted_station_events_api_db_backed.py
```

The repair added API-side pre-insert schema/constraint/column/nullability verification to the DB-backed API read validation harness. The verification is called in `db_backed_api_database()` after migration apply and before `yield plan`, which means it occurs before `seeded_rows()` inserts fixtures.

Repair evidence reported by the Architecture / Integration repair Thread:

```text
RED check first failed as expected: 1 failed, 40 passed, 19 skipped
GREEN API focused run: 41 passed, 19 skipped
Collector DB safety run: 20 passed
git diff --check: PASS
```

PM intake / Verification re-review evidence:

```text
changed technical file only: api/tests/test_accepted_station_events_api_db_backed.py
cached name-only: empty before commit and after commit
git diff --check: PASS
staged exact path only for commit: api/tests/test_accepted_station_events_api_db_backed.py
push complete: main -> origin/main, 2cfad5d
```

## 3. Current pending gate

The next PM should treat the following as pending:

```text
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair post-push docs/status sync
```

This status sync has not been assigned, implemented, committed or pushed yet.

Recommended next action is a docs/status-only Architecture / Integration task. It should update durable project status to record commit `2cfad5d` and Verification B1 closeout, while explicitly stating that live DB validation itself has still not been executed.

Recommended docs/status sync allowlist:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

The docs/status sync should not run tests, connect to DB, start Docker, edit API/runtime code, stage, commit or push unless separately authorized.

## 4. DB-backed API read validation status summary

Existing endpoint:

```text
GET /api/v2/production/accepted-station-events
```

API read path implementation commit:

```text
763b248ca835f59096e73aa5e199a4bf903ac946 Implement accepted station events read API
```

DB-backed API read validation tests-only implementation commit:

```text
b30db5cd2bd1d109d83c8da1a222d5ad37517448 Add DB-backed API read validation tests
```

DB-backed API read validation post-push docs/status sync commit:

```text
64d0e12dc76898a2da3ce09c2c0e94dbbf33ac80 Sync DB-backed API read validation status
```

DB-backed API schema verification HOLD repair commit:

```text
2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e Add API DB-backed schema verification
```

Current DB-backed API test file:

```text
api/tests/test_accepted_station_events_api_db_backed.py
```

Current harness status:

```text
DB-backed API tests are default skipped unless EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
EDGE_MES_ENABLE_DB_BACKED_TESTS=1 was not set during planning/review/repair/commit gates.
No DB opt-in run has executed.
No local Postgres connection has been made.
No temp DB create/drop has executed outside the default-skipped harness.
No migration has been applied against live DB.
No fixture insert into live DB has executed.
Docker / docker compose was not started.
Live DB validation has not completed.
Actual timeout failure proof has not completed.
```

Current repaired future-run evidence capability:

```text
The API DB-backed target now contains API-side schema verification helper coverage for:
- table exists: production_accepted_station_event_fact
- DTO / accepted fact columns
- nullable / NOT NULL expectations
- unique constraints: uq_production_accepted_station_event_fact_key, uq_production_accepted_station_event_source
- check constraints: ck_production_accepted_station_event_type, ck_production_accepted_station_event_result, ck_production_accepted_station_result_authority, ck_production_accepted_station_result_nok_authority, ck_production_accepted_station_nok_detail_authority

The helper is called after migration apply and before fixture insert in future live DB-backed execution.
```

Important overclaim boundary:

```text
The presence of the helper and committed tests is not live DB evidence by itself. A future report may claim live local Postgres API read validation only after PM explicitly authorizes and the opt-in run actually executes.
```

## 5. Boundaries to preserve exactly

Production visibility boundary:

```text
Future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.

Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.

raw_payload/raw_hex is evidence, not a production fact.

Decoded/source normalized payloads remain candidates until accepted.

Non-accepted dispositions do not write defect detail.

NOK/detail visibility must bind to accepted upstream business evidence.

Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
```

API read path source boundary:

```text
only production_accepted_station_event_fact
```

The following must not become equivalent production fact sources, fallback sources or join-derived field fillers for the API read endpoint:

```text
raw_plc_sample
cycle_event
station_event
production_unit
quality_event
production_snapshot
production_events
```

DTO allowlist remains:

```text
line_id
plc_id
station_id
station_type
profile_id
config_hash
config_version
event_type
production_result
unit_id
dmc
cycle_counter
source_event_id
event_ts
accepted_at
fact_key
content_fingerprint
nok_code
nok_origin
nok_detail_code
nok_detail_source_event_id
nok_detail_evidence_fact_key
```

Forbidden fields / surfaces remain:

```text
raw_payload
raw_hex
adapter disposition/reason/phase
candidate context
normalized candidate payload
raw/normalized comparison context
decoder errors
diagnostic/review/audit payloads
quality_pareto_input
dashboard_state
legacy payload
raw_sample_id
ack_status
read_done
collector_state
ambiguous result / defect / quality / pareto keys
```

## 6. Still not authorized

Do not do any of the following unless PM explicitly authorizes a separate gate:

```text
EDGE_MES_ENABLE_DB_BACKED_TESTS=1
local Postgres connection
EDGE_MES_DB_BACKED_TEST_DSN use
EDGE_MES_DB_BACKED_MAINTENANCE_DSN use
temp DB create/drop
migration application against live DB
fixture insert into live DB
actual DB opt-in / live local Postgres pytest run
Docker / docker compose
API server start
Dashboard/frontend/Grafana implementation
API route / production code expansion
worker/runtime DB-backed tests
collector runtime changes
storage.py changes
config/mapping.yaml changes
new migration
V-PLC changes
broad tests
deploy/tag/rollback
real PLC pilot
stage/commit/push except exact future PM-authorized gates
```

Candidate future command remains not authorized until a separate PM decision:

```bash
EDGE_MES_ENABLE_DB_BACKED_TESTS=1 \
EDGE_MES_DB_BACKED_TEST_DSN="$EDGE_MES_DB_BACKED_TEST_DSN" \
EDGE_MES_DB_BACKED_MAINTENANCE_DSN="$EDGE_MES_DB_BACKED_MAINTENANCE_DSN" \
PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api_db_backed.py -q -m "db_backed and postgres_local"
```

## 7. Carry-forward recommendations

For the next docs/status sync:

```text
Record 2cfad5d as the exact pushed HOLD repair commit.
Record Verification B1 as CLOSED after re-review.
Record that api/tests/test_accepted_station_events_api_db_backed.py now includes API-side pre-insert schema/constraint/column/nullability verification.
Record that no live DB validation has executed.
Record that actual timeout failure proof remains future scope.
Keep future DB opt-in/live local Postgres execution as a separate PM-authorized gate.
```

For a future actual DB opt-in/live local Postgres run:

```text
Require explicit PM approval before setting EDGE_MES_ENABLE_DB_BACKED_TESTS=1 or using DSNs.
Classify failures as read-only recovery mismatch, DSN validation failure, connection failure, temp DB drop/create failure, migration failure, schema/constraint verification failure, fixture insert failure, API read assertion failure, timeout setting verification failure, teardown failure, unexpected file modification, or unauthorized command/scope expansion.
Report pre-insert schema verification evidence separately from live API read assertion evidence.
Do not claim actual timeout failure proof from timeout setting verification alone.
If teardown fails, report HOLD with exact temp DB name and bounded manual cleanup instructions.
```

Future separate gates remain:

```text
actual timeout failure induction
Dashboard/API consumer planning and validation
worker/runtime DB-backed race / unique-violation semantics
commit-before-ACK behavior
non-accepted zero-row / no ACK/read_done mutation behavior
post-conflict re-read semantics and DB rollback
deploy/tag/rollback/real PLC pilot
```

## 8. Recommended next task prompt

Copy this into the next ChatGPT PM window or Architecture / Integration Thread when ready:

```markdown
# Edge MES Demo — ChatGPT PM Handoff Restore

你现在接手 Edge MES Demo 项目的 ChatGPT PM 角色。

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

## 0. 当前接手背景

上一位 PM 已完成：

- DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync，commit `64d0e12`
- explicit DB opt-in/live local Postgres API Read Validation Run Planning Gate
- Reliability planning review
- Data Quality planning review
- Verification planning review / exact future run allowlist audit：HOLD，B1
- HOLD repair：在 `api/tests/test_accepted_station_events_api_db_backed.py` 中补齐 API-side pre-insert schema/constraint/column/nullability verification
- Verification re-review：B1 CLOSED / PASS WITH RECOMMENDATIONS
- exact-path HOLD repair commit/push：commit `2cfad5d`
- PM handoff 文件创建：`docs/thread_handoff/chatgpt_pm_handoff_260704-1257.md`（当前文件；若尚未 commit，必须只按 exact path 处理）

当前最新主线 baseline 应为：

    HEAD == origin/main == 2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e
    latest commit:
    2cfad5d Add API DB-backed schema verification

## 1. 第一动作：read-only recovery

第一动作必须是 read-only recovery。不要编辑、不要运行 tests、不要连接 DB、不要启动 Docker、不要 stage、不要 commit、不要 push。

执行：

    git status -sb
    printf '\n--- log -12 ---\n' && git log --oneline -12
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git rev-parse origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only
    printf '\n--- status all ---\n' && git status --short --untracked-files=all

Expected live baseline：

    HEAD == origin/main == 2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e
    latest commit:
    2cfad5d Add API DB-backed schema verification
    cached name-only == empty

## 2. 请先读取

    docs/thread_handoff/pm_operating_rules.md
    docs/current_status.md
    docs/thread_handoff/chatgpt_pm_handoff_260704-1257.md
    docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
    docs/reports/sprint3_collector_ingestion_adapter_plan.md
    docs/contracts/dashboard_api_contract.md

## 3. 当前 pending gate

推荐下一步：

    DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair post-push docs/status sync

执行 Thread：

    Architecture / Integration

推荐 allowlist：

    docs/current_status.md
    docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
    docs/reports/sprint3_collector_ingestion_adapter_plan.md

必须记录：

- `2cfad5d` 已 push；
- Verification B1 已关闭；
- `api/tests/test_accepted_station_events_api_db_backed.py` 已补齐 API-side pre-insert schema/constraint/column/nullability verification；
- schema verification 在 migration apply 后、fixture insert 前；
- 未执行 DB opt-in；
- 未设置 `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`；
- 未连接 local Postgres；
- 未启动 Docker；
- 未执行 live DB validation；
- 未完成 actual timeout failure proof；
- future actual DB opt-in/live local Postgres run 仍需单独 PM 授权。

不要执行：

    EDGE_MES_ENABLE_DB_BACKED_TESTS=1
    local Postgres connection
    temp DB create/drop
    migration apply
    fixture insert
    Docker / docker compose
    API server start
    Dashboard/frontend/Grafana
    worker/runtime DB-backed gates
    deploy/tag/rollback
    broad tests
    stage/commit/push unless separately authorized

## 4. External dirty artifacts

继续排除：

    M .gitignore
    ?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
    ?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

如果当前 handoff 文件尚未 commit，也会看到：

    ?? docs/thread_handoff/chatgpt_pm_handoff_260704-1257.md

不要使用：

    git add .
    git add -A
    git add docs/
    git add db/
```

## 9. Handoff commit note

This handoff file itself is not committed by creation. If PM authorizes commit/push, use exact path only:

```bash
git add docs/thread_handoff/chatgpt_pm_handoff_260704-1257.md
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
git commit -m "Add PM handoff after API DB-backed schema verification"
git push
```

Do not stage `.gitignore`, old PM handoff files, Keynote/reporting artifacts, broad `docs/`, or unrelated files.
