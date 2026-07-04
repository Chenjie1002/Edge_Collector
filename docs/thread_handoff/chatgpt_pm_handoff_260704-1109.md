# Edge MES Demo — ChatGPT PM Handoff 260704-1109

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
HEAD == origin/main == b30db5cd2bd1d109d83c8da1a222d5ad37517448
latest commit:
b30db5c Add DB-backed API read validation tests
cached name-only == empty
```

Important baseline rule: live `HEAD` / `origin/main` must still be verified. Historical baselines in durable docs are audit markers and are not HOLD by themselves after later authorized commits.

## 1. Current repository state at handoff creation

Last verified immediately before this handoff file was created:

```text
branch: main
HEAD / origin/main: b30db5cd2bd1d109d83c8da1a222d5ad37517448
latest commit: b30db5c Add DB-backed API read validation tests
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
docs/thread_handoff/chatgpt_pm_handoff_260704-1109.md
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
DB/API/Dashboard DB-backed/live Postgres API Read Validation planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Reliability planning review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Data Quality planning review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Verification planning review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only implementation: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Reliability implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Data Quality implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Verification implementation review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation exact-path commit/push: PASS, commit b30db5c
```

Commit pushed:

```text
b30db5cd2bd1d109d83c8da1a222d5ad37517448 Add DB-backed API read validation tests
```

Committed file:

```text
api/tests/test_accepted_station_events_api_db_backed.py
```

Validation evidence from implementation/reviews:

```text
PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py api/tests/test_accepted_station_events_api_db_backed.py -q
-> 27 passed, 32 skipped

PYTHONPATH=collector:. .venv/bin/python -m pytest collector/tests/test_db_backed_safety.py -q
-> 20 passed

git diff --check
-> PASS
```

No DB opt-in / local Postgres / Docker was run. `EDGE_MES_ENABLE_DB_BACKED_TESTS=1` was not set.

## 3. Current pending gate

The next PM should treat the following as pending:

```text
DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync
```

This status sync has not been assigned, implemented, committed or pushed yet.

Recommended next technical action is a docs/status-only Architecture / Integration task. It should update durable project status to record commit `b30db5c`, while explicitly stating that live DB validation itself has not been executed.

Recommended docs/status sync allowlist:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

The docs/status sync should not run tests, connect to DB, start Docker, edit API/runtime code, stage, commit or push unless separately authorized.

## 4. API read path and DB-backed test summary

Existing implemented endpoint:

```text
GET /api/v2/production/accepted-station-events
```

API read path implementation commit:

```text
763b248ca835f59096e73aa5e199a4bf903ac946 Implement accepted station events read API
```

API read path implementation files:

```text
api/app/main.py
api/app/routes/accepted_station_events.py
api/tests/test_accepted_station_events_api.py
```

DB-backed API read validation test commit:

```text
b30db5cd2bd1d109d83c8da1a222d5ad37517448 Add DB-backed API read validation tests
```

DB-backed API read validation test file:

```text
api/tests/test_accepted_station_events_api_db_backed.py
```

The new test file prepares a default-skipped, opt-in guarded DB-backed/live Postgres API read validation harness for the accepted station event read endpoint. It records and checks the planned live SQL/read behavior when a future PM separately authorizes local Postgres DB-backed execution.

Current coverage status:

```text
Default non-DB focused run: 27 passed, 32 skipped.
Collector DB safety focused run: 20 passed.
DB-backed API tests are default skipped.
No local Postgres validation has been executed.
No live DB evidence has been claimed.
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

## 6. Current non-authorized scope

The following remain not authorized:

```text
DB opt-in run
EDGE_MES_ENABLE_DB_BACKED_TESTS=1
local Postgres connection
temp DB create/drop
migration application against live DB
fixture insert into live DB
docker compose
compose host postgres
new migration
storage.py changes
collector runtime changes
config/mapping.yaml changes
API route / production code expansion
Dashboard/frontend/Grafana implementation
V-PLC changes
deploy/tag/rollback
broad tests
real PLC pilot
stage/commit/push except exact future PM-authorized gates
```

Do not claim any of the following as completed:

```text
live DB validation completed
actual timeout failure proof completed
local Postgres execution completed
DB opt-in execution completed
Docker execution completed
production runtime validation completed
```

## 7. Carry-forward recommendations

```text
Before production deploy, ACCEPTED_STATION_EVENTS_CURSOR_SECRET must be managed as a real deployment secret rather than relying on the development fallback.
Future authorized live DB validation should explicitly set EDGE_MES_ENABLE_DB_BACKED_TESTS=1 and guarded local/test DSNs only after PM approval.
Actual timeout failure proof remains future authorized work; current tests prove timeout statements are set, not that a real timeout failure path was induced.
Worker/runtime DB-backed unique-violation race, commit-before-ACK, non-accepted DB-backed zero-row/no ACK/read_done mutation, post-conflict re-read semantics and worker-level DB rollback remain separate future gates.
Dashboard/Grafana consumer planning remains separate future work.
work_order/product remain excluded until a later schema/contract gate.
```

## 8. Recommended next gate

Recommended immediate next gate:

```text
DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync
```

After that docs/status sync is reviewed and committed/pushed, next options are:

```text
PM handoff after docs/status sync
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Gate
DB/API/Dashboard Dashboard/API Consumer Planning Gate
```

Do not directly run DB opt-in, connect to local Postgres, start Docker, begin Dashboard implementation, deploy, tag, rollback or run broad tests.

## 9. Suggested prompt for next PM / next Thread

```markdown
# Edge MES Demo — ChatGPT PM Handoff Restore

你现在接手 Edge MES Demo 项目的 ChatGPT PM 角色。

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

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

Expected live baseline:

    HEAD == origin/main == b30db5cd2bd1d109d83c8da1a222d5ad37517448
    latest commit:
    b30db5c Add DB-backed API read validation tests
    cached name-only == empty

当前正确 PM handoff 文件：

    docs/thread_handoff/chatgpt_pm_handoff_260704-1109.md

请先读取：

    docs/thread_handoff/pm_operating_rules.md
    docs/current_status.md
    docs/thread_handoff/chatgpt_pm_handoff_260704-1109.md
    docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
    docs/reports/sprint3_collector_ingestion_adapter_plan.md

## 2. 当前已完成事项

上一位 PM 已完成并 push：

- DB/API/Dashboard DB-backed/live Postgres API Read Validation planning gate
- Reliability / Data Quality / Verification planning reviews
- tests-only implementation in `api/tests/test_accepted_station_events_api_db_backed.py`
- Reliability / Data Quality / Verification implementation reviews
- exact-path commit/push at `b30db5c`

Current latest commit:

    b30db5cd2bd1d109d83c8da1a222d5ad37517448 Add DB-backed API read validation tests

Committed file:

    api/tests/test_accepted_station_events_api_db_backed.py

Evidence:

    PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py api/tests/test_accepted_station_events_api_db_backed.py -q
    -> 27 passed, 32 skipped

    PYTHONPATH=collector:. .venv/bin/python -m pytest collector/tests/test_db_backed_safety.py -q
    -> 20 passed

    git diff --check
    -> PASS

No DB opt-in / local Postgres / Docker was run.

## 3. Current pending task

Recommended first task:

    DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync

Recommended docs allowlist:

    docs/current_status.md
    docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
    docs/reports/sprint3_collector_ingestion_adapter_plan.md

Do not run tests, DB opt-in, local Postgres, Docker, Dashboard, deploy/tag/rollback, broad tests or real PLC pilot.

## 4. Remaining dirty / untracked external artifacts

Do not stage, clean or rewrite:

    M .gitignore
    ?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
    ?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

Strictly forbidden:

    git add .
    git add -A
    git add docs/
    git add db/
```
