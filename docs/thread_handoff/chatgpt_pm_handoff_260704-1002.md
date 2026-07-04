# Edge MES Demo — ChatGPT PM Handoff 260704-1002

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
```

Expected live baseline after this handoff is created:

```text
HEAD == origin/main == 737473fc4d5d7f232d700f1f973621e9f5851e0f
latest commit:
737473f Sync API read path implementation status
cached name-only == empty
```

Important baseline rule: live `HEAD` / `origin/main` must still be verified. Historical baselines in durable docs are audit markers and are not HOLD by themselves after later docs-only / handoff commits.

## 1. Current repository state at handoff creation

Last verified immediately before this handoff file was created:

```text
branch: main
HEAD / origin/main: 737473fc4d5d7f232d700f1f973621e9f5851e0f
latest commit: 737473f Sync API read path implementation status
cached: empty by status inspection
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

This handoff file itself is newly created in the current task:

```text
docs/thread_handoff/chatgpt_pm_handoff_260704-1002.md
```

Until it is explicitly committed, expect it to appear as an additional untracked file. If PM authorizes a handoff commit gate, stage only this exact file and continue excluding `.gitignore` and old PM/Keynote artifacts.

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
DB/API/Dashboard API read path planning gate: CLOSED / PASS TO REVIEW WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path planning Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path planning Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path planning Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path contract freeze docs-only edit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path contract freeze Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path contract freeze Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path contract freeze Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path contract freeze exact docs commit/push: PASS, commit 2d0918a
DB/API/Dashboard API read path contract freeze post-push docs/status sync: PASS, commit 2da0a75
PM handoff after API read path contract status sync: PASS, commit 4648734
DB/API/Dashboard API read path implementation planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation planning Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation planning Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation planning Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation exact commit/push: PASS, commit 763b248
DB/API/Dashboard API read path implementation post-push docs/status sync: PASS, commit 737473f
```

Current durable status files are synced to `737473f`:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

## 3. API read path implementation summary

Implementation commit:

```text
763b248ca835f59096e73aa5e199a4bf903ac946 Implement accepted station events read API
```

Docs/status sync commit:

```text
737473fc4d5d7f232d700f1f973621e9f5851e0f Sync API read path implementation status
```

Changed implementation files:

```text
api/app/main.py
api/app/routes/accepted_station_events.py
api/tests/test_accepted_station_events_api.py
```

Conditional allowlist not used:

```text
api/app/db.py
```

Implemented endpoint:

```text
GET /api/v2/production/accepted-station-events
```

Implementation behavior:

```text
source: only production_accepted_station_event_fact
query validation: required line_id, required bounded start_time/end_time, strict timezone-aware ISO parsing, default limit 50, max limit 500, invalid limit/time/window fail closed
cursor: HMAC signed, schema/version checked, binds line_id, start_time, end_time, limit, direction and ordering tuple
stable order: event_ts ASC, accepted_at ASC, fact_key ASC
read safety: BEGIN READ ONLY, SET LOCAL statement_timeout = '3s', SET LOCAL idle_in_transaction_session_timeout = '3s', SELECT-only query, COMMIT/ROLLBACK, no write-path helper reuse
DTO allowlist: frozen accepted fact fields only
NOK/detail: returned only from accepted fact row fields and must bind accepted upstream business evidence
```

Validation evidence:

```text
PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py -> 27 passed
git diff --check -> PASS
git diff --cached --check before commit -> PASS
```

Review evidence:

```text
Reliability implementation review: PASS WITH RECOMMENDATIONS, no blocker
Data Quality implementation review: PASS WITH RECOMMENDATIONS, no blocker
Verification implementation review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
```

## 4. Contract / visibility boundary to preserve exactly

```text
Future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.

Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.

raw_payload/raw_hex is evidence, not a production fact.

Decoded/source normalized payloads remain candidates until accepted.

Non-accepted dispositions do not write defect detail.

NOK/detail visibility must bind to accepted upstream business evidence.

Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
```

## 5. API read path source and field boundary

The implemented endpoint may read only:

```text
production_accepted_station_event_fact
```

The following must not become equivalent production fact sources, fallback sources or join-derived field fillers for this endpoint:

```text
raw_plc_sample
cycle_event
station_event
production_unit
quality_event
production_snapshot
production_events
```

DTO allowlist:

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

Forbidden fields / surfaces:

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
local Postgres connection
docker compose
new migration
storage.py changes
collector changes
config/mapping.yaml changes
Dashboard/frontend/Grafana implementation
V-PLC changes
deploy/tag/rollback
broad tests
real PLC pilot
stage/commit/push except exact future PM-authorized gates
```

The API endpoint implementation is closed, but live DB-backed/runtime validation is not claimed. Future DB-backed/live Postgres API read validation remains a separate PM-authorized gate.

## 7. Carry-forward recommendations

```text
Before production deploy, ACCEPTED_STATION_EVENTS_CURSOR_SECRET must be managed as a real deployment secret rather than relying on the development fallback.
Future DB-backed/live Postgres API read validation remains separate PM-authorized work; current coverage is focused API tests using mocked/stubbed DB access, not live schema/runtime coverage.
work_order/product remain excluded until a later schema/contract gate.
Dashboard/API consumer planning may proceed only as a separate PM-authorized planning gate.
```

## 8. Recommended next gates

Recommended immediate next gate:

```text
Exact-path PM handoff commit gate
```

If authorized, stage only:

```text
docs/thread_handoff/chatgpt_pm_handoff_260704-1002.md
```

Suggested commit message:

```text
Add PM handoff after API read path implementation closeout
```

After handoff commit/push, next technical gate options:

```text
DB/API/Dashboard DB-backed/live Postgres API Read Validation Planning Gate
DB/API/Dashboard Dashboard/API Consumer Planning Gate
```

Do not start implementation, DB opt-in run, Dashboard work, deploy/tag/rollback or broad tests directly.

## 9. Suggested prompt for next PM / next Thread

```markdown
# Edge MES Demo — ChatGPT PM Handoff Restore

你现在接手 Edge MES Demo 项目的 ChatGPT PM 角色。

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

第一动作必须是 read-only recovery。不要编辑、不要运行 tests、不要连接 DB、不要 stage、不要 commit、不要 push。

执行：

    git status -sb
    printf '\n--- log -12 ---\n' && git log --oneline -12
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git rev-parse origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only

Expected live baseline:

    HEAD == origin/main == 737473fc4d5d7f232d700f1f973621e9f5851e0f
    latest commit:
    737473f Sync API read path implementation status
    cached name-only == empty

当前正确 PM handoff 文件：

    docs/thread_handoff/chatgpt_pm_handoff_260704-1002.md

当前已完成：

- DB/API/Dashboard API read path planning gate
- Reliability / Data Quality / Verification planning reviews
- API read path contract freeze docs-only edit
- Reliability / Data Quality / Verification contract reviews
- exact docs commit/push at 2d0918a
- post-push docs/status sync at 2da0a75
- PM handoff at 4648734
- API read path implementation planning gate
- Reliability / Data Quality / Verification implementation planning reviews
- API read path implementation and focused tests
- Reliability / Data Quality / Verification implementation reviews
- exact implementation commit/push at 763b248
- post-push docs/status sync at 737473f

当前没有挂起的 review gate、repair gate、implementation gate、status sync gate。

剩余 dirty/untracked external artifacts 不属于当前任务，不要 stage：

    M .gitignore
    ?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
    ?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

下一步建议：先提交并 push 本 PM handoff 文件，之后再开 DB/API/Dashboard DB-backed/live Postgres API Read Validation Planning Gate 或 Dashboard/API Consumer Planning Gate。不要直接 implementation、DB opt-in、Dashboard、deploy/tag/rollback 或 broad tests。
```
