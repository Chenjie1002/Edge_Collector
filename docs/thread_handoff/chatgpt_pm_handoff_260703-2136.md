# Edge MES Demo — ChatGPT PM Handoff

交接时间：2026-07-03 21:36 UTC+8
当前角色：ChatGPT PM
项目路径：`/Users/chenjie/Documents/MES/edge-mes-demo`

## 1. 当前主线状态

当前项目主线已经完成 **DB/API/Dashboard guarded DB-backed accepted fact tests implementation + Reliability HOLD repair + review closeout + exact commit/push + docs/status sync** 的完整闭环。

当前 live baseline：

```text
HEAD == origin/main == 62231f1c6b4f898dc2a728ffdd97d76ba15595cd
latest commit:
62231f1 Sync guarded DB-backed test status
```

上一关键代码 / 测试 commit：

```text
636ba375248987b26d4ae68bdbf952d47f398bc8 Add guarded DB-backed accepted fact tests
```

上一 docs/status sync commit：

```text
62231f1c6b4f898dc2a728ffdd97d76ba15595cd Sync guarded DB-backed test status
```

当前没有挂起的 implementation gate、review gate、repair gate、commit gate、push gate。
当前没有 staged files。
当前不应直接进入 API/Dashboard implementation、DB opt-in test run 或 local Postgres harness implementation。

## 2. 新 PM 第一动作：read-only recovery

新 ChatGPT PM 接手后，第一动作必须是只读恢复。不要编辑、不要运行 tests、不要 stage、不要 commit、不要 push。

在项目路径执行：

```bash
git status -sb
printf '\n--- log -12 ---\n' && git log --oneline -12
printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
printf '\n--- origin/main ---\n' && git rev-parse origin/main
printf '\n--- diff name-only ---\n' && git diff --name-only
printf '\n--- cached name-only ---\n' && git diff --cached --name-only
```

预期：

```text
HEAD == origin/main == 62231f1c6b4f898dc2a728ffdd97d76ba15595cd
latest commit:
62231f1 Sync guarded DB-backed test status
cached name-only == empty
```

## 3. 当前 expected external dirty artifacts

以下 artifacts 是外部脏文件 / 旧交接或 Keynote 文件，不属于当前工程主线，除非 PM 明确 exact-path 授权，否则不要 stage、commit、clean、rewrite：

```text
M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

特别注意：`.gitignore` 是 external dirty artifact。不要误 stage。

严格禁止：

```bash
git add .
git add -A
git add docs/
git add db/
```

## 4. 本轮已完成 gates

### DB-backed/local Postgres hardening test planning

已完成：

- PM planning gate：PASS TO REVIEW WITH RECOMMENDATIONS
- Reliability planning review：PASS WITH RECOMMENDATIONS, no blocker
- Data Quality planning review：PASS WITH RECOMMENDATIONS, no blocker
- Verification planning review / exact allowlist audit：PASS WITH RECOMMENDATIONS, no blocker

核心 planning 决策：

```text
DB-backed tests are acceptable only if future implementation adds strict local/test DB safety controls.
Current repo did not yet contain DB-backed safety fixtures, so DB-backed tests must not be run before guards exist.
Tests must default-skip unless EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
DSN guard must reject unsafe targets before psycopg.connect().
Default test target DB name must match edge_mes_test_*.
Protected names such as edge_mes, postgres, prod and production must be rejected.
Temp DB create/drop must be guarded and local-only.
Docker compose must not be started by pytest.
```

### Guarded DB-backed accepted fact tests implementation

Implementation Thread：Architecture / Integration
结论：PASS WITH RECOMMENDATIONS

Initial implementation changed files：

```text
pytest.ini
collector/tests/conftest.py
collector/tests/test_db_backed_safety.py
collector/tests/test_event_collector_accepted_fact_db_backed.py
collector/tests/test_event_collector_accepted_fact_write_path.py
collector/app/services/accepted_station_event_fact.py
```

Implementation summary：

```text
Registered pytest markers: db_backed and postgres_local.
Added default skip unless EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
Added pure-unit DSN safety helpers.
Added separated maintenance/admin DSN guard.
Added temp DB lifecycle planning helpers and guarded DROP DATABASE statement generation.
Added deterministic migration file ordering and schema verification query helpers.
Added skipped-by-default DB-backed direct-storage test file.
Added DTO negative repair: station_result NOK missing accepted business NOK evidence fails closed before DB insert.
Preserved storage.py unchanged.
No DB opt-in tests run, no DB connection, no docker compose.
```

Focused default test command reported by implementation and reviews：

```bash
PYTHONPATH=collector:. .venv/bin/python -m pytest collector/tests/test_db_backed_safety.py collector/tests/test_event_collector_accepted_fact_write_path.py collector/tests/test_event_collector_accepted_fact_db_backed.py -q
```

Final safe/default result after repair：

```text
33 passed, 7 skipped
```

### Reliability HOLD and repair

First Reliability implementation review：HOLD.

HOLD blocker：

```text
DB-backed/local Postgres matrix was materially overstated.
collector/tests/conftest.py had placeholder skip fixtures for simulate_unique_violation_after_precheck and db_backed_worker.
Therefore race/unique-violation-after-precheck, worker rollback, commit failure, and DB-backed non-accepted ACK/read_done tests in collector/tests/test_event_collector_accepted_fact_db_backed.py were not executable coverage.
For that gate, the reported reliability matrix was stronger than actual coverage.
```

Architecture / Integration narrow repair：PASS WITH RECOMMENDATIONS.

Repair actions：

```text
Removed placeholder fixtures: simulate_unique_violation_after_precheck, db_backed_worker, fail_next_production_fact_write, fail_next_legacy_current_write, fail_next_commit.
Removed non-executable worker/race/commit/non-accepted scenarios from pytest-discovered DB-backed tests.
Limited DB-backed skipped-by-default pytest tests to seven direct-storage opt-in tests.
Added safety assertion that future DB-authorized scenarios are not exposed as placeholder pytest coverage.
Reclassified worker/race/commit/non-accepted DB-backed scenarios as future DB-authorized carry-forward work.
```

Reliability HOLD repair re-review：PASS WITH RECOMMENDATIONS, no blocker.

### Data Quality and Verification closeout

Data Quality implementation review：PASS WITH RECOMMENDATIONS, no blocker.

Data Quality confirmed：

```text
DTO station_result NOK evidence: PASS.
station_result OK behavior preserved.
station_nok detail evidence preserved.
production_accepted_station_event_fact remains the production accepted station-event fact surface.
fact_key/source identity/content_fingerprint authority preserved.
raw_payload/raw_hex excluded from production fact DTO/table assertions.
adapter disposition/reason/context remains diagnostic-only.
legacy/current tables are not equivalent production accepted fact surfaces.
future scenario reclassification is honest.
```

Verification implementation review / exact allowlist audit：PASS WITH RECOMMENDATIONS, no blocker.

Verification confirmed：

```text
Exact allowlist: PASS.
Cached state: empty.
git diff --check: PASS.
Default safe test command: 33 passed, 7 skipped.
DB connections: none.
Docker compose: not started.
storage.py unchanged.
migration 007 unchanged.
API/Dashboard/V-PLC/config/deploy surfaces unchanged.
```

### Exact commit/push gate

User explicitly authorized exact-path commit/push.

Commit：

```text
636ba375248987b26d4ae68bdbf952d47f398bc8 Add guarded DB-backed accepted fact tests
```

Committed files：

```text
pytest.ini
collector/tests/conftest.py
collector/tests/test_db_backed_safety.py
collector/tests/test_event_collector_accepted_fact_db_backed.py
collector/tests/test_event_collector_accepted_fact_write_path.py
collector/app/services/accepted_station_event_fact.py
```

Push result：

```text
024f4bd..636ba37 main -> main
```

### Post-push docs/status sync

Docs/status sync 已完成、commit、push。

Docs sync commit：

```text
62231f1c6b4f898dc2a728ffdd97d76ba15595cd Sync guarded DB-backed test status
```

Docs updated：

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

Post-push state：

```text
HEAD == origin/main == 62231f1c6b4f898dc2a728ffdd97d76ba15595cd
cached empty
external dirty artifacts still excluded
```

## 5. Current committed technical state

Guarded DB-backed accepted fact tests are now committed and pushed.

Current committed behavior / test infrastructure：

```text
pytest.ini registers db_backed and postgres_local markers.
DB-backed tests skip by default unless EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
Test-target DSN guard allows only local/test hosts and edge_mes_test_* database names.
Maintenance/admin DSN guard is separate and limited to local postgres/template1 maintenance targets.
DROP DATABASE statement generation is allowed only for proven edge_mes_test_* names.
Migration ordering helper loads db/init/*.sql as needed, then db/migrations/007_accepted_station_event_visibility.sql.
Schema verification queries check production_accepted_station_event_fact, uq_production_accepted_station_event_fact_key, uq_production_accepted_station_event_source and expected ck_* constraints.
DB-backed pytest-discovered tests are seven direct-storage opt-in tests and skip by default.
station_result NOK missing accepted business NOK evidence fails closed before DB insert.
```

Important limitation：

```text
This is NOT a full DB-backed local Postgres execution closeout.
No DB-backed opt-in tests were run.
No DB connection was made.
Docker compose was not started.
Worker-level DB-backed accepted rollback, commit failure before ACK, non-accepted DB-backed zero rows + no ACK/read_done mutation, race / unique-violation-after-precheck and post-unique-violation re-read semantics remain future PM-authorized local Postgres harness work.
```

## 6. Must preserve production-fact visibility boundary

后续所有 gate 必须继承并保护以下原文：

```text
Future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.

Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.

raw_payload/raw_hex is evidence, not a production fact.

Decoded/source normalized payloads remain candidates until accepted.

Non-accepted dispositions do not write defect detail.

NOK/detail visibility must bind to accepted upstream business evidence.

Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
```

## 7. 当前仍未授权的范围

当前没有授权：

- DB opt-in test run
- local Postgres connection
- docker compose start
- worker-level DB-backed harness
- race / unique-violation-after-precheck executable harness
- post-unique-violation re-read semantics implementation
- API implementation
- Dashboard/frontend/Trace UI/Grafana implementation
- new DB migration
- DB schema changes
- V-PLC behavior changes
- config/mapping.yaml changes
- raw_required
- line-wide `runtime_defaults.raw_policy` change
- deploy
- tag
- rollback drill
- real PLC pilot
- broad tests
- push/commit/stage unless PM opens exact gate

## 8. Carry-forward recommendations

Carry-forward items after this handoff：

```text
1. Future DB opt-in/local Postgres harness gate may implement real execution for:
   - worker-level DB-backed accepted rollback;
   - commit failure before ACK;
   - non-accepted DB-backed zero rows + no ACK/read_done mutation;
   - race / unique-violation-after-precheck;
   - post-unique-violation re-read semantics if PM decides idempotent race handling is required.

2. Future DB/API/Dashboard gates must use real production accepted fact table assertions, not synthetic visibility assumptions.

3. Do not treat legacy/current raw_plc_sample, cycle_event, station_event, production_unit or quality_event as equivalent to production accepted fact surface.

4. DB opt-in execution must require explicit PM authorization, reviewed local/test DSNs and no external/prod/default edge_mes targets.

5. API read path is a plausible next DB/API/Dashboard planning branch, but it must be opened as a separate Level 2 planning gate.
```

## 9. Recommended next PM decision

Recommended next step after read-only recovery：

```text
Do not start implementation immediately.
First decide between:

A. Future DB opt-in/local Postgres harness planning gate
   Purpose: actually execute the default-skipped DB-backed tests against a guarded local test database and add worker/race harness coverage if authorized.

B. API read path planning gate
   Purpose: plan bounded API access to production_accepted_station_event_fact without Dashboard/UI expansion.

C. Pause for process/governance cleanup
   Purpose: decide whether old external PM handoff/keynote artifacts or .gitignore should remain excluded or be handled by a separate exact-path governance task.
```

Default recommendation：choose **A only if PM wants to prove DB-backed runtime semantics next**; otherwise choose **B** to continue downstream DB/API/Dashboard product surface planning. In either case, open a new Level 2 planning gate first.

## 10. Copyable prompt for next ChatGPT PM window

```markdown
# Edge MES Demo — ChatGPT PM Handoff Restore

你现在接手 Edge MES Demo 项目的 ChatGPT PM 角色。

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

## 0. 当前接手背景

上一位 PM 已完成：

- DB/API/Dashboard guarded DB-backed accepted fact tests planning gate
- Reliability / Data Quality / Verification planning reviews
- guarded DB-backed accepted fact tests implementation
- Reliability implementation HOLD
- Architecture / Integration HOLD repair
- Reliability HOLD repair re-review
- Data Quality implementation review
- Verification implementation review / exact allowlist audit
- exact-path implementation commit/push
- post-push docs/status sync commit/push
- PM handoff 文件创建

当前最新主线 baseline 应为：

    HEAD == origin/main == 62231f1c6b4f898dc2a728ffdd97d76ba15595cd
    latest commit:
    62231f1 Sync guarded DB-backed test status

当前正确 PM handoff 文件应为：

    docs/thread_handoff/chatgpt_pm_handoff_260703-2136.md

## 1. 第一动作：read-only recovery

第一动作必须是 read-only recovery。不要编辑、不要运行 tests、不要 stage、不要 commit、不要 push。

执行：

    git status -sb
    printf '\n--- log -12 ---\n' && git log --oneline -12
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git rev-parse origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only

Expected live baseline:

    HEAD == origin/main == 62231f1c6b4f898dc2a728ffdd97d76ba15595cd
    latest commit:
    62231f1 Sync guarded DB-backed test status
    cached name-only == empty

Expected external dirty artifacts to exclude:

    M .gitignore
    ?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
    ?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

## 2. 必读文件

请先读取：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260703-2136.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md

## 3. 当前状态

DB/API/Dashboard guarded DB-backed accepted fact tests 已 CLOSED / PASS WITH RECOMMENDATIONS，并完成 commit/push：

    636ba375248987b26d4ae68bdbf952d47f398bc8 Add guarded DB-backed accepted fact tests

Docs/status sync 已 CLOSED / PASS，并完成 commit/push：

    62231f1c6b4f898dc2a728ffdd97d76ba15595cd Sync guarded DB-backed test status

当前没有挂起的 review、repair、commit、push gate。

## 4. 当前未授权

不要直接执行：

- implementation
- tests
- DB opt-in run
- local Postgres connection
- docker compose
- API/Dashboard implementation
- new migration
- storage.py changes
- config/mapping.yaml changes
- V-PLC changes
- deploy/tag/rollback
- stage/commit/push

## 5. 推荐下一步

先做 PM 判断，不要直接开工。

建议二选一：

1. Future DB opt-in/local Postgres harness planning gate
2. API read path planning gate

任一方向都应按 Level 2 planning gate 开始，先 planning，再 Reliability / Data Quality / Verification reviews。
```

## 11. Handoff file status

This file was generated locally by ChatGPT PM after the docs/status sync at `62231f1`.

Do not stage this handoff automatically. Exact-path stage/commit/push requires explicit PM authorization.
