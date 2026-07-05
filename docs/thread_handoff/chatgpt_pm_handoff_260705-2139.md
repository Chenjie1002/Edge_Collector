# Edge MES Demo — ChatGPT PM Handoff 260705-2139

## 0. 接手角色

你现在接手 Edge MES Demo 项目的 ChatGPT PM 角色。

项目路径：

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

当前任务状态：Sprint 3 DB-backed API validation execution rerun 前的 PM handoff。

下一位 PM 第一优先级：先恢复上下文，不要直接推进执行。

---

## 1. 第一动作：read-only recovery

第一动作必须是 read-only recovery。不要编辑、不要运行 tests、不要连接 DB、不要启动 Docker、不要 stage、不要 commit、不要 push。

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

Expected live baseline at handoff time：

```text
HEAD == origin/main == 1d040a6d90085adee7e95914d9696c0ed6834c44
latest commit:
1d040a6 Align DB-backed API failure assertion
cached name-only == empty
```

Expected dirty / untracked artifacts at handoff time：

```text
 M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

这些 dirty / untracked artifacts 不属于当前任务，不要顺手 stage / commit / clean / modify。

特别注意：

```text
docs/reports/sprint3_db_backed_api_validation_reliability_review.md
```

这是 earlier PM 误生成的 unauthorized local artifact，不是正式 Reliability Thread 输出。不要读取、不要引用、不要 stage、不要 commit。

---

## 2. 必读文件

先读：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260705-2139.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/reports/sprint3_db_backed_api_validation_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_api_consumer_implementation_plan.md`

可只读参考：

- `api/app/routes/accepted_station_events.py`
- `api/tests/test_accepted_station_events_api.py`
- `api/tests/test_accepted_station_events_api_db_backed.py`
- `api/app/db.py`
- `api/app/main.py`
- `db/migrations/007_accepted_station_event_visibility.sql`

不要读取 / 引用：

- `docs/reports/sprint3_db_backed_api_validation_reliability_review.md`

---

## 3. 本轮已完成事项

### 3.1 DB-backed API validation planning gate

正式 planning report：

```text
docs/reports/sprint3_db_backed_api_validation_plan.md
```

Architecture / Integration planning gate：PASS WITH RECOMMENDATIONS。

Reliability planning review：PASS WITH RECOMMENDATIONS。

Data Quality planning review：PASS WITH RECOMMENDATIONS。

Verification planning review / exact future run allowlist audit：PASS WITH RECOMMENDATIONS。

Planning exact-path commit/push：PASS。

Planning commit：

```text
78ce29bd4229912a9164f9e35c911f0037e14a83 Plan DB-backed API validation
```

### 3.2 First DB-backed execution attempts

DB-backed execution gate was attempted through user local command / SSH tunnel setup.

First execution HOLD：missing DSNs.

Second execution HOLD：DSNs still not injected into execution Thread environment; default-safe preflight ran and passed/skipped without DB opt-in:

```text
69 passed, 19 skipped
```

PM then advised user to run exact command locally to avoid exposing password in ChatGPT.

User ran exact focused DB-backed command locally through SSH tunnel.

Result:

```text
1 failed, 87 passed in 12.69s
```

Failure:

```text
api/tests/test_accepted_station_events_api_db_backed.py::test_live_api_rolls_back_on_controlled_query_failure_only
assert 503 == 500
```

### 3.3 Execution HOLD repair planning

Repair planning gate：PASS WITH RECOMMENDATIONS。

Root cause: DB-backed controlled failure test expected `500`, while contract / route / non-DB test expect fail-closed `503 {"detail": "accepted fact source unavailable"}`.

Planning conclusion：test expectation bug / contract alignment mismatch, not API route bug.

Allowed repair file：

```text
api/tests/test_accepted_station_events_api_db_backed.py
```

### 3.4 Focused repair implementation

Focused test-only repair implementation：PASS。

Changed file：

```text
api/tests/test_accepted_station_events_api_db_backed.py
```

Reported changes:

- changed expected status from `500` to `503`;
- added exact response detail assertion:
  - `assert response.json() == {"detail": "accepted fact source unavailable"}`
- added failure-path runtime side-effect guard:
  - `assert not failing_recorder.runtime_side_effect_seen`
- preserved:
  - `BEGIN READ ONLY`
  - `ROLLBACK`
  - no `COMMIT`
  - no mutation/write SQL
  - no ACK/read_done

Implementation validation reported:

```text
compileall PASS
default-safe pytest: 69 passed, 19 skipped
git diff --check PASS
```

No DB-backed execution was run during repair implementation.

### 3.5 Focused repair review / exact-path audit

Verification focused repair review：PASS WITH RECOMMENDATIONS。

Review confirmed:

- one-file test-only diff;
- route / contract alignment to `503 {"detail": "accepted fact source unavailable"}`;
- rollback/no-side-effect coverage preserved;
- exact-path commit readiness.

### 3.6 Focused repair exact-path commit/push

PM-authorized exact-path commit/push gate：PASS。

Only staged/committed/pushed:

```text
api/tests/test_accepted_station_events_api_db_backed.py
```

Commit:

```text
1d040a6d90085adee7e95914d9696c0ed6834c44 Align DB-backed API failure assertion
```

Push result:

```text
HEAD == origin/main == 1d040a6d90085adee7e95914d9696c0ed6834c44
```

---

## 4. 当前未完成事项 / 下一步

下一步是：

```text
DB-backed execution rerun with SSH tunnel DSNs
```

这是 PM-authorized execution gate，需要新 Thread 执行，保持证据隔离。

不应先做 docs/status sync，也不应先做 tag/deploy/rollback。DB-backed execution rerun 结果出来后，再决定是否做 docs/status sync。

---

## 5. SSH tunnel / DSN 状态

Postgres 在树莓派 Docker 上：

```text
container: edge-mes-postgres
image: postgres:16
host port: 5432
container port: 5432
status: healthy
```

User chose SSH tunnel mode because project checkout is on Mac and gate allowlist requires loopback host.

Tunnel shape:

```text
Mac localhost:5433 -> Pi localhost:5432 -> edge-mes-postgres Docker container
```

User verified tunnel / test user successfully:

```text
current_user      | edge_mes_test
current_database  | postgres
inet_server_port  | 5432
```

This means:

- Mac `localhost:5433` tunnel is connected;
- remote Postgres server port is `5432`;
- test user `edge_mes_test` can connect to maintenance DB `postgres`.

Do not write real password into reports or handoff. Use masked facts only.

Masked DSN facts:

```text
target_scheme=postgresql
target_host=localhost
target_port=5433
target_database=edge_mes_test_api_read
target_db_name_matches_edge_mes_test_prefix=yes
maintenance_scheme=postgresql
maintenance_host=localhost
maintenance_port=5433
maintenance_database=postgres
maintenance_database_allowed=yes
target_and_maintenance_distinct=yes
ssh_tunnel_mode=Mac localhost:5433 -> Pi localhost:5432
```

Real DSN shape for user local execution:

```bash
EDGE_MES_DB_BACKED_TEST_DSN='postgresql://edge_mes_test:<password>@localhost:5433/edge_mes_test_api_read'
EDGE_MES_DB_BACKED_MAINTENANCE_DSN='postgresql://edge_mes_test:<password>@localhost:5433/postgres'
```

Password is the password user set for PostgreSQL role `edge_mes_test`. Do not ask user to paste it unless they explicitly choose to do so. Preferred path is user runs exact command locally and posts output.

---

## 6. Exact focused command for next execution rerun

Recommended user-local command, with password substituted locally and not pasted back:

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

EDGE_MES_ENABLE_DB_BACKED_TESTS=1 \
EDGE_MES_DB_BACKED_TEST_DSN='postgresql://edge_mes_test:<password>@localhost:5433/edge_mes_test_api_read' \
EDGE_MES_DB_BACKED_MAINTENANCE_DSN='postgresql://edge_mes_test:<password>@localhost:5433/postgres' \
PYTHONPATH=api .venv/bin/python -m pytest \
  api/tests/test_accepted_station_events_api.py \
  api/tests/test_accepted_station_events_api_db_backed.py \
  -q
```

Allowed exact test paths only:

- `api/tests/test_accepted_station_events_api.py`
- `api/tests/test_accepted_station_events_api_db_backed.py`

Forbidden without new PM authorization:

- broad `pytest`
- `pytest api`
- `pytest .`
- unapproved `-k`
- single-node troubleshooting
- Docker / docker compose
- code edits
- stage / commit / push
- deploy / tag / rollback
- real PLC pilot

If user posts rerun output, PM intake should classify:

- PASS if all tests pass and no cleanup issue is reported;
- HOLD if any failure remains, cleanup not confirmed, or command deviated from allowlist.

---

## 7. Execution evidence requirements to carry forward

When intake-ing the rerun, require evidence / summary for:

- exact two test files;
- DB-backed opt-in used;
- masked DSN facts;
- isolated target DB name `edge_mes_test_api_read`;
- schema verification happened before fixture insert;
- table existence / columns / nullability / unique constraints / check constraints verified;
- exact DTO allowlist assertion;
- forbidden leakage absence;
- source-only read;
- cursor payload cleanliness;
- empty-result semantics;
- line/window/limit filtering;
- NOK/detail evidence;
- pagination no duplicate/no omission;
- invalid/tampered/cross-scope cursor fail-closed;
- unsupported query parameter fail-closed;
- success COMMIT / controlled failure ROLLBACK where covered;
- no mutation SQL;
- no ACK/read_done;
- no Collector / PLC / V-PLC / runtime / storage / Dashboard side effect;
- cleanup evidence.

Carry-forward recommendations:

- duplicate query-key behavior remains not covered unless explicitly added in a later gate;
- actual timeout failure proof remains separate unless separately authorized;
- do not confuse valid empty result with schema/source/authority failure.

---

## 8. PM intake expectations for next result

If next DB-backed rerun returns all pass, PM should respond with:

- execution gate PASS / PASS WITH RECOMMENDATIONS;
- note that prior controlled failure `503` mismatch was repaired and committed in `1d040a6`;
- confirm no code changes in rerun;
- decide next gate.

Likely next gate after successful rerun:

```text
post-execution docs/status sync planning or exact docs/status sync gate
```

Expected docs/status sync files may include, pending PM rules and current status structure:

- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`

Do not start docs/status sync until execution PASS is received and PM authorizes.

If rerun fails, do not broaden troubleshooting. Open a focused HOLD triage/planning gate based on the exact failure.

---

## 9. Current committed history

At handoff time:

```text
1d040a6 Align DB-backed API failure assertion
78ce29b Plan DB-backed API validation
1012d71 Add PM handoff after API implementation closeout
029a735 Sync accepted station events API status
97dc4d5 Harden accepted station events API contract
2dc4b4d Add API consumer implementation planning
472161c Add PM handoff after API consumer contract closeout
d99a8f1 Sync API consumer contract status
```

Important commits:

```text
97dc4d520ef8edc9b7620e5ce9e8a61d0e1aee7f Harden accepted station events API contract
78ce29bd4229912a9164f9e35c911f0037e14a83 Plan DB-backed API validation
1d040a6d90085adee7e95914d9696c0ed6834c44 Align DB-backed API failure assertion
```

---

## 10. Thread / context recommendation

当前 Thread 已经很长，混合了：

- planning gate；
- review sequence；
- execution attempts；
- DSN / SSH tunnel setup；
- focused repair planning；
- repair implementation；
- review / exact-path commit/push；
- PM handoff。

建议下一位 PM 在新 Thread 接手。

下一位 PM 接手后不要直接跑命令。先执行 read-only recovery，确认：

```text
HEAD == origin/main == 1d040a6d90085adee7e95914d9696c0ed6834c44
cached name-only == empty
```

然后询问/确认用户是否仍保持 SSH tunnel 窗口打开，并让用户本地执行 exact command，或在明确授权并安全处理密码后进入 DB-backed execution rerun gate。

Preferred安全路径：用户本地执行 exact command，把 pytest 输出贴回；PM 做 intake。

---

## 11. 禁止项提醒

除非用户明确授权新的 gate，否则禁止：

- 修改代码；
- 修改 docs/status；
- 运行 DB-backed tests；
- 设置 `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`；
- 连接 DB；
- 创建/删除 test DB；
- apply migrations；
- insert fixtures；
- 启动 Docker；
- broad pytest；
- stage / commit / push；
- deploy / tag / rollback；
- real PLC pilot。

任何 commit/push 必须 exact-path allowlist，禁止 `git add .`。
