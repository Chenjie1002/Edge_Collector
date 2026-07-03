# Edge MES Demo — ChatGPT PM Handoff 260704-0005

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
HEAD == origin/main == 2da0a75127095e57c14109b739034b4b1a85f54f
latest commit:
2da0a75 Sync API read path contract status
cached name-only == empty
```

Important baseline rule: live `HEAD` / `origin/main` must still be verified. Historical baselines in durable docs are audit markers and are not HOLD by themselves after later docs-only / handoff commits.

## 1. Current repository state at handoff creation

Last verified immediately before this handoff file was created:

```text
branch: main
HEAD / origin/main: 2da0a75127095e57c14109b739034b4b1a85f54f
latest commit: 2da0a75 Sync API read path contract status
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
docs/thread_handoff/chatgpt_pm_handoff_260704-0005.md
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
DB/API/Dashboard API read path contract freeze post-push docs/status sync: PASS
DB/API/Dashboard API read path contract status exact docs/status commit/push: PASS, commit 2da0a75
```

Current durable status files are synced to `2da0a75`:

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

## 3. Current contract freeze summary

Contract freeze commit:

```text
2d0918adebe5cd29e59177bc2159c7f447cb5c38 Freeze accepted fact API read contract
```

Status sync commit:

```text
2da0a75127095e57c14109b739034b4b1a85f54f Sync API read path contract status
```

Changed contract file:

```text
docs/contracts/dashboard_api_contract.md
```

Frozen future endpoint contract:

```text
GET /api/v2/production/accepted-station-events
```

This is only a future API contract. It does not claim current implementation.

Contract source boundary:

```text
Only production_accepted_station_event_fact may be the production fact source.
raw_plc_sample, cycle_event, station_event, production_unit, quality_event, production_snapshot and production_events must not be treated as equivalent production fact sources.
No legacy/current fallback or join is allowed to fill fields for this endpoint.
```

Response DTO allowlist:

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

Query contract carry-forward:

```text
bounded start_time/end_time required
line_id required or explicit server default scope
limit max 500
strict cursor parsing
invalid cursor/limit/bounds fail closed
stable pagination order based on event_ts/accepted_at plus stable identity such as fact_key
work_order/product excluded until later schema/contract gate
```

## 4. Production-fact visibility boundary to preserve exactly

```text
Future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.

Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.

raw_payload/raw_hex is evidence, not a production fact.

Decoded/source normalized payloads remain candidates until accepted.

Non-accepted dispositions do not write defect detail.

NOK/detail visibility must bind to accepted upstream business evidence.

Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
```

## 5. Reliability / Data Quality / Verification carry-forward

Reliability carry-forward:

```text
future endpoint must be read-only
read-only transaction required
statement_timeout / idle timeout should become future implementation MUST
no INSERT/UPDATE/DELETE
no ACK/read_done mutation
no Collector/PLC/runtime side effect
cursor tuple / sorting direction / tie-breaker must be frozen before implementation
scope/filter/time window should be included in cursor validation
api/app/db.py is only conditional future allowlist if centralized read-only DB helper is needed
```

Data Quality carry-forward:

```text
all response fields must come only from production_accepted_station_event_fact
accepted_at is accepted fact timestamp only, not dashboard freshness / ACK time / collector state
source_event_id / fact_key / content_fingerprint are immutable identity/reference only, not retry/write/ACK authority
NOK/detail must bind accepted upstream business evidence
adapter reason code, raw mismatch, decoder error and quality_event must not derive NOK/detail
work_order/product remain excluded until later schema/contract gate
avoid Dashboard/Quality/Pareto/Summary wording drift
```

Verification future test matrix:

```text
positive DTO allowlist assertions
negative forbidden-field assertions
source non-equivalence / no legacy fallback assertions
bounded query and cursor validation
cursor tamper / invalid cursor fail-closed cases
cursor binds scope/filter/time window
NOK/detail evidence response assertions
read-only / no ACK/read_done side-effect assertions
forbidden surface guard for migration/storage/collector/config/dashboard/V-PLC/docker/deploy
```

## 6. Current non-authorized scope

The following remain not authorized:

```text
implementation
tests
DB opt-in run
local Postgres connection
docker compose
API/Dashboard implementation
API read path implementation
new migration
storage.py changes
collector changes
config/mapping.yaml changes
Dashboard/frontend/Grafana
V-PLC changes
deploy/tag/rollback
broad tests
real PLC pilot
stage/commit/push except exact future PM-authorized gates
```

## 7. Recommended next gates

Recommended immediate next gate:

```text
Exact-path PM handoff commit gate
```

If authorized, stage only:

```text
docs/thread_handoff/chatgpt_pm_handoff_260704-0005.md
```

Suggested commit message:

```text
Add PM handoff after API read path contract status sync
```

After handoff commit/push, next technical gate recommendation:

```text
DB/API/Dashboard API Read Path Implementation Planning Gate
```

Do not start implementation directly. Treat it as Level 2 planning first.

Recommended initial future implementation allowlist to review, not to implement yet:

```text
api/app/routes/accepted_station_events.py
api/app/main.py
api/tests/test_accepted_station_events_api.py
```

Conditional future allowlist only if planning proves it is necessary:

```text
api/app/db.py
```

Explicit exclusions for implementation planning unless PM expands scope:

```text
db/migrations/*
collector/app/services/storage.py
collector/app/services/event_collector.py
collector/app/services/accepted_station_event_fact.py
api/app/routes/trace.py
collector/tests/*
config/mapping.yaml
Dashboard/frontend/Grafana
Docker
V-PLC
deploy/tag/rollback
.gitignore
old PM handoff/keynote artifacts
```

## 8. Suggested prompt for next PM / next Thread

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

    HEAD == origin/main == 2da0a75127095e57c14109b739034b4b1a85f54f
    latest commit:
    2da0a75 Sync API read path contract status
    cached name-only == empty

当前正确 PM handoff 文件：

    docs/thread_handoff/chatgpt_pm_handoff_260704-0005.md

当前已完成：

- DB/API/Dashboard API read path planning gate
- Reliability / Data Quality / Verification planning reviews
- API read path contract freeze docs-only edit
- Reliability / Data Quality / Verification contract reviews
- exact docs commit/push at 2d0918a
- post-push docs/status sync commit/push at 2da0a75

当前没有挂起的 review gate、repair gate、status sync gate。

剩余 dirty/untracked external artifacts 不属于当前任务，不要 stage：

    M .gitignore
    ?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
    ?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

下一步建议：先提交并 push 本 PM handoff 文件，之后再开 DB/API/Dashboard API Read Path Implementation Planning Gate。不要直接 implementation。
```
