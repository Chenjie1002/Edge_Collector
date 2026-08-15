# Sprint 3 DB-backed API validation planning Reliability review

报告名称：Sprint 3 DB-backed API validation planning Reliability review

任务名称：Sprint 3 DB-backed API validation planning gate - Reliability planning review

执行 Thread：Reliability

结论：PASS WITH RECOMMENDATIONS

本 review 只审查 planning report 的可靠性边界。没有连接 DB，没有运行 tests / DB-backed tests，没有设置 `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`，没有创建/删除 test DB，没有 apply migrations，没有 insert fixtures，没有启动 Docker / docker compose，没有 stage / commit / push。

## Scope

### reviewed files

- `docs/reports/sprint3_db_backed_api_validation_plan.md`
- `docs/thread_handoff/pm_operating_rules.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_api_consumer_implementation_plan.md`
- `api/app/routes/accepted_station_events.py` read-only reliability reference
- `api/tests/test_accepted_station_events_api.py` read-only reliability reference
- `api/tests/test_accepted_station_events_api_db_backed.py` read-only reliability reference
- `api/app/db.py` read-only reliability reference
- `api/app/main.py` read-only reliability reference

### changed files

- `docs/reports/sprint3_db_backed_api_validation_reliability_review.md`

### explicitly not touched

- `docs/reports/sprint3_db_backed_api_validation_plan.md`
- `.gitignore`
- known external dirty artifacts
- `api/app/routes/accepted_station_events.py`
- `api/tests/test_accepted_station_events_api.py`
- `api/tests/test_accepted_station_events_api_db_backed.py`
- `api/app/db.py`
- `api/app/main.py`
- migration/schema files
- Dashboard/frontend files
- Collector/runtime/storage.py
- `config/mapping.yaml`
- Docker / docker compose files
- V-PLC / PLC / deploy / tag / rollback surfaces

## Reliability review

### DB-backed validation target

PASS.

The plan correctly scopes future validation to:

```text
GET /api/v2/production/accepted-station-events
```

and to the API implementation after:

```text
97dc4d520ef8edc9b7620e5ce9e8a61d0e1aee7f
97dc4d5 Harden accepted station events API contract
```

Reliability impact is bounded: the plan validates the real PostgreSQL read behavior of the accepted station events API route and explicitly excludes Dashboard/frontend, Collector runtime, storage write path, PLC/V-PLC runtime behavior, Docker, deploy, tag, rollback and real PLC pilot.

### Future run/test allowlist

PASS.

The future execution command is limited to the exact focused API test paths:

- `api/tests/test_accepted_station_events_api.py`
- `api/tests/test_accepted_station_events_api_db_backed.py`

The plan explicitly forbids broad pytest commands and rejects scope expansion through `pytest`, `python -m pytest`, `pytest api`, `pytest api/tests`, `pytest collector`, `pytest .`, extra files, `-k` troubleshooting, narrower node reruns, Docker startup or DB work outside the future authorization gate.

Reliability assessment: this avoids accidental broad side effects and keeps the DB opt-in blast radius narrow enough for a later controlled execution gate.

### DB opt-in safety

PASS.

The plan correctly freezes that `EDGE_MES_ENABLE_DB_BACKED_TESTS=1` is forbidden in this planning gate and may be used only in a later separately PM-authorized execution gate.

It also requires:

- DB-backed tests remain default-safe unless explicitly opted in;
- target and maintenance DSNs are present only during the authorized execution;
- unsafe or malformed opt-in inputs skip or fail closed instead of connecting;
- credentials are not leaked in the execution report.

Reliability assessment: default-safe opt-in and masked DSN reporting are sufficient for planning closeout.

### DSN / isolated test DB safety

PASS.

The plan freezes the critical DSN controls:

- target DSN host must be loopback/test-local only: `localhost`, `127.0.0.1` or `::1`;
- target DB name must match `edge_mes_test_*`;
- protected DB names are forbidden;
- maintenance DSN must also be loopback/test-local only;
- maintenance DB must be `postgres` or `template1` only;
- target and maintenance DSNs must be distinct;
- Docker service hosts, remote LAN IPs, public hostnames and production-like DB names are forbidden;
- non-isolated DBs are forbidden.

The read-only reference in `api/tests/test_accepted_station_events_api_db_backed.py` already contains matching guard concepts: loopback host allowlist, `edge_mes_test_*` naming, protected DB name rejection, distinct target/maintenance DSNs and quoted create/drop statements.

Reliability assessment: this is adequate to prevent accidental production or compose-default DB targeting in the future execution gate.

### Cleanup and failure cleanup behavior

PASS WITH RECOMMENDATIONS.

The plan requires isolated DB cleanup in `finally` / equivalent cleanup and requires the execution report to include an explicit cleanup result such as:

```text
test_db_cleanup_ok edge_mes_test_api_read
```

Reliability assessment: cleanup is planned correctly. The later execution report must prove cleanup actually occurred and must not claim PASS if cleanup is unconfirmed.

Recommendation R1: Future execution report should distinguish these cleanup states explicitly:

- `test_db_cleanup_ok <db_name>`
- `test_db_cleanup_failed <db_name> <masked_reason>`
- `test_db_cleanup_not_attempted <masked_reason>`

Any state other than cleanup OK should be reported as `HOLD` for the DB-backed execution gate.

### Migration/schema verification before fixture insert

PASS.

The plan requires the migration to be applied only to the isolated test DB and requires schema verification after migration apply and before fixture insert.

Required checks include:

- table existence for `production_accepted_station_event_fact`;
- DTO / accepted fact authority columns;
- nullable / NOT NULL expectations;
- unique constraints;
- accepted-fact check constraints;
- metadata-only schema verification with no `INSERT`, `UPDATE` or `DELETE`.

Reliability assessment: the ordering is correct. Failing before fixture insert avoids using invalid schema as a partially reliable test substrate.

### Fixture and live API read behavior

PASS WITH RECOMMENDATIONS.

The plan requires fixtures to insert only accepted fact rows into isolated `production_accepted_station_event_fact`, including same timestamp tie-breakers, another-line rows and NOK/detail rows with accepted upstream evidence.

The plan also freezes valid bounded request behavior, exact DTO allowlist, source isolation, empty-result behavior, NOK/detail authority, pagination no duplicate/no omission, invalid cursor fail-closed and unsupported filter fail-closed.

Reliability assessment: these requirements are strong enough for a future DB-backed API validation execution gate.

Recommendation R2: Future execution report should explicitly identify whether empty-result behavior was proven by a named assertion. It should not infer empty-result correctness only from other-line filtering or from lack of returned rows in a different test.

### DB unavailable / missing table / missing schema / missing authority behavior

PASS WITH RECOMMENDATIONS.

The plan freezes fail-closed behavior:

- DB unavailable: explicit route error, currently `503 {"detail": "accepted fact source unavailable"}`;
- missing table: schema verification failure before fixture insert, or route-level accepted fact source unavailable error if encountered at API query time;
- missing schema / missing columns / nullability mismatch: schema verification failure before fixture insert;
- missing accepted-fact authority constraints: schema verification failure before fixture insert;
- forbidden source availability must never mask accepted fact table failure.

Reliability assessment: this is correct. The plan avoids fallback, avoids silent empty-result substitution for schema/source errors and avoids treating missing authority as normal absence of data.

Recommendation R3: Future execution report should separate these classes in evidence:

- schema verification failure before fixture insert;
- API route fail-closed error during read;
- valid empty result for a valid schema and valid bounded query.

These must not be collapsed into the same “empty/no data” bucket.

Recommendation R4: If the future execution observes route-level DB read failure as `500` instead of the planned `503`, report it explicitly as a reliability finding rather than normalizing it away. The planning expectation remains fail-closed with no fallback; exact error envelope should be confirmed by execution evidence.

### Source authority and fallback isolation

PASS.

The plan freezes the only production fact source as:

- `production_accepted_station_event_fact`

and forbids these fallback, join, field-filler or equivalent production fact sources:

- `raw_plc_sample`
- `cycle_event`
- `station_event`
- `production_unit`
- `quality_event`
- `production_snapshot`
- `production_events`

Reliability assessment: no fallback is the right reliability posture. In this slice, degraded source availability should produce explicit error/unknown/empty according to contract, not silently switch authority.

### Query/cursor/pagination reliability

PASS.

The plan limits the DB-backed validation query subset to:

- `line_id`
- `start_time`
- `end_time`
- `limit`
- `cursor`

Unsupported filters fail closed with 4xx. Cursor binding includes line, time window, limit, direction and ordering tuple. Stable order is frozen as:

```text
event_ts ASC
accepted_at ASC
fact_key ASC
```

Reliability assessment: the query and cursor plan protects against broad scans, cross-scope cursor replay, pagination instability, duplicate rows and omitted rows.

Recommendation R5: Keep duplicate query-key behavior as a carry-forward check for Verification. If duplicate `line_id`, `start_time`, `end_time`, `limit` or `cursor` keys are accepted by the framework in a surprising way, future execution should report it instead of assuming the first/last value is safe.

### No-side-effect behavior

PASS.

The plan freezes these requirements:

- `BEGIN READ ONLY` or equivalent read-only semantics;
- statement timeout;
- idle/read timeout expectation;
- no `INSERT`, `UPDATE` or `DELETE` by the API route;
- no write-side helper call;
- no ACK/read_done mutation;
- no Collector / PLC / V-PLC / runtime / storage / Dashboard side effect;
- success commits read-only transaction;
- controlled query failure rolls back and does not commit;
- actual timeout failure proof remains separate unless PM explicitly authorizes it.

Reliability assessment: this is sufficient for planning. It protects the route from becoming a production-state mutation surface during a DB-backed read validation.

Recommendation R6: Future execution evidence should show both success and failure transaction paths when available: success `COMMIT`, controlled failure `ROLLBACK`, no mutation SQL, no ACK/read_done tokens and no runtime side-effect tokens.

### Review sequence before execution

PASS.

The plan correctly freezes the required sequence:

1. Reliability planning review.
2. Data Quality planning review.
3. Verification planning review / exact future run allowlist audit.
4. PM explicit authorization for the execution gate.

Reliability assessment: no execution authority is inferred from planning PASS.

## Blockers

- none

## Recommendations

- R1: Future execution report must distinguish cleanup OK / cleanup failed / cleanup not attempted. Anything other than cleanup OK should be `HOLD`.
- R2: Future execution report should name the assertion that proves empty-result behavior.
- R3: Future execution report should separate schema verification failure, route fail-closed read error and valid empty result evidence.
- R4: If route-level DB read failure returns `500` instead of planned `503`, report it as a reliability finding; do not normalize it away.
- R5: Keep duplicate query-key behavior as a Verification carry-forward check.
- R6: Future execution evidence should show success `COMMIT`, controlled failure `ROLLBACK`, no mutation SQL, no ACK/read_done tokens and no runtime side-effect tokens where available.

## Evidence

### read-only recovery

Recovery before this review:

```text
HEAD == origin/main == 1012d71f739d6fd847fca1a95bbd14349ac99ebf
latest commit: 1012d71 Add PM handoff after API implementation closeout
cached name-only: empty
pre-existing diff name-only: .gitignore
status includes known external dirty artifacts and the untracked planning report
```

### docs/checks run

Read-only checks only:

```text
git status -sb
git log -1 --format='%H %s'
git rev-parse origin/main
git diff --name-only
git diff --cached --name-only
git status --short --untracked-files=all
grep/sed read-only review of planning report and reliability reference files
```

No tests were run. No DB-backed tests were run. No DB connection was made.

### git diff name-only

Expected after this review file is written:

```text
.gitignore
```

Note: `docs/reports/sprint3_db_backed_api_validation_plan.md` and this review report are untracked new docs files, so they do not appear in `git diff --name-only` until staged. They are not staged by this review.

### git cached name-only

Expected:

```text
empty
```

### status

Expected status includes:

```text
 M .gitignore
?? docs/reports/sprint3_db_backed_api_validation_plan.md
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? known external dirty artifacts
```

## Next gate

### eligible for

- Data Quality planning review of `docs/reports/sprint3_db_backed_api_validation_plan.md` with this Reliability review as carry-forward input.

### PM approval required before

- Verification planning review / exact future run allowlist audit after Data Quality review;
- any DB-backed execution;
- setting `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`;
- setting DB-backed DSN env vars;
- creating/dropping isolated test DB;
- applying migrations;
- inserting fixtures;
- running pytest;
- editing API route/tests/db/main/migration files;
- Docker / deploy / tag / rollback / real PLC pilot;
- stage / commit / push.

## Thread 输出 / 上下文评估

- 本次输出长度：中
- 当前 Thread 是否建议继续：yes
- 下一轮是否建议新开 Thread：no
- 理由：Reliability planning review 已关闭且无 blocker；Data Quality planning review 仍可在当前 PM Thread 中继续。进入 DB-backed execution、代码修复、测试执行或 commit/push 前必须重新授权并可考虑新 Thread。
