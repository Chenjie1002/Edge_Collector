# Edge MES Demo — ChatGPT PM Handoff

交接时间：2026-07-03  
当前角色：ChatGPT PM  
项目路径：`/Users/chenjie/Documents/MES/edge-mes-demo`

## 1. 当前主线状态

当前项目主线已经完成 **DB/API/Dashboard Slice 2 DB write path implementation + docs/status sync** 的完整闭环。

当前 live baseline：

```text
HEAD == origin/main == 1ba6970444d9b1478fe7e8e5c3406e5a9b043c01
latest commit:
1ba6970 Sync Slice 2 write path status
```

上一关键代码 commit：

```text
299d28aa5c91b8c3cf7115b6582ce26d45b64706 Implement accepted station event fact write path
```

当前没有挂起的 implementation gate、review gate、commit gate、push gate。  
当前没有 staged files。  
当前不应直接进入 API/Dashboard implementation。

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
HEAD == origin/main == 1ba6970444d9b1478fe7e8e5c3406e5a9b043c01
latest commit:
1ba6970 Sync Slice 2 write path status
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

## 4. 已完成的重要 gates

### Slice 1 schema-only closeout

已完成：

- DB/API/Dashboard Slice 1 schema-only planning gate：CLOSED / PASS WITH RECOMMENDATIONS
- DB/API/Dashboard Slice 1 schema-only implementation gate：CLOSED / PASS WITH RECOMMENDATIONS
- DB/API/Dashboard Slice 1 schema-only Reliability focused review：CLOSED / PASS WITH RECOMMENDATIONS
- DB/API/Dashboard Slice 1 schema-only Data Quality focused review：CLOSED / PASS WITH RECOMMENDATIONS
- DB/API/Dashboard Slice 1 schema-only Verification focused review / exact allowlist audit：CLOSED / PASS WITH RECOMMENDATIONS
- DB/API/Dashboard Slice 1 schema-only exact migration commit/push：PASS，commit `e75f652`
- DB/API/Dashboard Slice 1 schema-only docs/status sync：PASS，commit `496adf1`
- PM handoff after Slice 1 schema closeout：PASS，commit `5b3c061`

Slice 1 migration 创建：

```text
db/migrations/007_accepted_station_event_visibility.sql
```

核心表：

```text
production_accepted_station_event_fact
```

用途：production-only landing surface for accepted station-event business facts。

### Slice 2 DB write path planning / review closeout

已完成：

- Architecture initial planning：PASS WITH RECOMMENDATIONS
- Reliability first planning review：HOLD
- Architecture planning repair：PASS WITH RECOMMENDATIONS
- Reliability planning re-review：PASS WITH RECOMMENDATIONS
- Data Quality planning review：PASS WITH RECOMMENDATIONS
- Verification planning review：PASS WITH RECOMMENDATIONS

Reliability 第一轮 HOLD 的核心原因：

- 原 planning 未冻结足够明确的 transaction boundary。
- `storage.persist_cycle()` 与 helpers 存在 internal commit 风险。
- production fact insert 与 legacy/current persistence 之间可能发生 partial write divergence。
- ACK/read_done post-commit safety 未充分冻结。

Architecture repair 后选择并冻结：

```text
Option B:
Storage transaction API/context manager + no-internal-commit write variants
```

强制 transaction sequence：

```text
adapter accepted decision
-> build accepted fact DTO from accepted AdapterDecision / validated event
-> open one explicit DB transaction
-> insert/upsert production_accepted_station_event_fact
-> perform legacy/current persistence in the same transaction
-> commit
-> only after commit may existing ACK/read_done mutation happen
```

### Slice 2 implementation + review closeout

代码 implementation 已完成、review、commit、push。

Implementation commit：

```text
299d28aa5c91b8c3cf7115b6582ce26d45b64706 Implement accepted station event fact write path
```

Changed files in implementation commit：

```text
collector/app/services/storage.py
collector/app/services/event_collector.py
collector/app/services/accepted_station_event_fact.py
collector/tests/test_event_collector_adapter_gate.py
collector/tests/test_event_collector_accepted_fact_write_path.py
```

实现摘要：

- Added accepted station-event fact write path for `production_accepted_station_event_fact`.
- Added `accepted_station_event_fact.py` DTO/helper.
- Added `Storage.transaction()` and no-internal-commit write variants.
- Accepted path writes production fact + legacy/current persistence in one transaction.
- ACK/read_done mutation happens only after successful transaction commit.
- Non-accepted dispositions create zero production rows and no ACK/read_done mutation for current payload.
- Duplicate/conflict/raw_variant/idempotency behavior implemented and tested with focused fake/spy coverage.
- No DB migration/API/Dashboard/V-PLC/config/deploy/tag/rollback changes in this slice.

已完成 implementation reviews：

- Architecture implementation + focused tests：PASS WITH RECOMMENDATIONS
- Reliability focused implementation review：PASS WITH RECOMMENDATIONS
- Data Quality focused implementation review：PASS WITH RECOMMENDATIONS
- Verification focused implementation review / exact allowlist audit：PASS WITH RECOMMENDATIONS
- Exact commit gate：PASS
- Exact push gate：PASS

Validation evidence：

```text
collector/tests/test_event_collector_adapter_gate.py -> 36 passed
tests/test_collector_station_event_adapter.py -> 46 passed
collector/tests/test_event_collector_accepted_fact_write_path.py -> 12 passed
combined focused tests -> 94 passed
compileall collector/app/services -> PASS
git diff --check -> PASS
exact allowlist audit -> PASS
cached empty
```

### Post-push docs/status sync

Docs/status sync 已完成、commit、push。

Docs sync commit：

```text
1ba6970444d9b1478fe7e8e5c3406e5a9b043c01 Sync Slice 2 write path status
```

Docs updated：

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

Post-push state：

```text
HEAD == origin/main == 1ba6970444d9b1478fe7e8e5c3406e5a9b043c01
cached empty
external dirty artifacts still excluded
```

## 5. Must preserve production-fact visibility boundary

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

## 6. 当前仍未授权的范围

当前没有授权：

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

## 7. Carry-forward recommendations

以下 recommendations 不阻塞当前主线，但应作为下一阶段重点：

1. Add DB-backed/live Postgres tests for:
   - `production_accepted_station_event_fact` unique constraints
   - rollback behavior
   - commit failure
   - connection failure
   - same key/source same content no-op
   - different content conflict
   - race / unique-violation-after-precheck

2. Add direct storage-level coverage for:
   - `insert_accepted_station_event_fact_no_commit()`
   - fact_key behavior
   - source identity behavior
   - same content idempotency
   - different content conflict
   - real DB constraints

3. Add DTO builder negative coverage:
   - `station_result nok` missing accepted NOK evidence should fail closed earlier, not rely mainly on DB constraints.

4. Future DB/API/Dashboard gates must use real `production_accepted_station_event_fact` assertions, not synthetic visibility assumptions.

5. Do not treat legacy/current tables as equivalent to production accepted fact surface:
   - `raw_plc_sample`
   - `cycle_event`
   - `station_event`
   - `production_unit`
   - `quality_event`

## 8. Recommended next task

推荐下一步不是 API/Dashboard implementation，而是：

```text
DB/API/Dashboard Slice 2 DB-backed/local Postgres hardening test planning gate
```

理由：

- Slice 2 DB write path 已实现并 push。
- 目前关键 DB 行为主要靠 fake/spy tests 覆盖。
- Reliability、Data Quality、Verification 都把 DB-backed coverage 作为 carry-forward。
- API/Dashboard 后续会依赖 `production_accepted_station_event_fact` 的可信度。
- 在进入 API read path 之前，最好先规划并补强 real DB constraint / rollback / concurrency tests。

推荐顺序：

```text
1. DB-backed/local Postgres hardening test planning gate
2. DB-backed hardening tests implementation + focused reviews
3. API read path planning gate
4. API implementation
5. Dashboard/Trace read-only visibility planning
```

## 9. Suggested next prompt summary

新 PM 可以基于下面任务开启下一个 Architecture / Integration Thread：

```text
DB/API/Dashboard Slice 2 DB-backed/local Postgres hardening test planning gate
```

任务性质：

```text
Level 2 planning-only
Do not implement.
Do not run tests.
Do not stage/commit/push.
Do not connect to production/external DB.
```

规划重点：

- 是否使用 existing local test DB / docker compose / pytest fixture / transaction rollback fixture。
- 是否允许连接本地 Postgres；必须禁止 production/external DB。
- 需要新增或修改哪些 test files。
- 是否需要修改 `storage.py` 或仅新增 tests。
- 如何加载 migration `007_accepted_station_event_visibility.sql`。
- 如何保证测试数据隔离、可重复、不会污染真实环境。
- 如何覆盖 unique constraints、rollback、commit failure、connection failure、race、unique-violation-after-precheck、DTO negative coverage。

如果无法保证只使用安全 local/test DB，或 hardening tests 会污染真实环境，应报告 HOLD。

## 10. PM 操作原则

新 PM 继续遵循：

- 所有 implementation / tests / stage / commit / push / deploy / tag / rollback 必须单独授权。
- Level 2 任务必须先 planning，再 Reliability / Data Quality / Verification review，再 implementation。
- 不要把 PASS WITH RECOMMENDATIONS 当作自动授权下一步 implementation。
- 不要自动 push。
- 不要 broad staging。
- 所有 commit 必须 exact-path allowlist。
- 对 external dirty artifacts 保持隔离。
