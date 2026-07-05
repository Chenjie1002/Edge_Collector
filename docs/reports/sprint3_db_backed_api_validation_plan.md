# Sprint 3 DB-backed API validation planning gate report

报告名称：Sprint 3 DB-backed API validation planning gate report

任务名称：Sprint 3 DB-backed API validation planning gate

执行 Thread：Architecture / Integration

结论：PASS WITH RECOMMENDATIONS

本 gate 只做 docs-only planning。没有连接 DB，没有运行 DB-backed tests，没有设置 `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`，没有创建/删除 test DB，没有 apply migrations，没有 insert fixtures，没有启动 Docker / docker compose，没有 broad pytest，没有 stage / commit / push。

## Scope

### reviewed files

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260705-1623.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_api_consumer_implementation_plan.md`
- `api/app/routes/accepted_station_events.py` read-only reference
- `api/tests/test_accepted_station_events_api.py` read-only reference
- `api/tests/test_accepted_station_events_api_db_backed.py` read-only reference
- `api/app/db.py` read-only reference
- `api/app/main.py` read-only reference
- `db/migrations/007_accepted_station_event_visibility.sql` read-only schema reference

### changed files

- `docs/reports/sprint3_db_backed_api_validation_plan.md`

### explicitly not touched

- `.gitignore`
- known external dirty artifacts:
  - `docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`
  - `docs/reports/phase1_to_sprint2_management_keynote_10p.html`
  - `docs/reports/sprint3_db_backed_api_validation_reliability_review.md`
  - `docs/thread_handoff/chatgpt_pm_handoff_20260624.md`
  - `docs/thread_handoff/chatgpt_pm_handoff_20260625.md`
  - `docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md`
  - `docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md`
- API route / API tests / DB-backed test / DB connection code:
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
- V-PLC / PLC pilot / deploy / tag / rollback surfaces

## Planning

### DB-backed validation target

Future DB-backed validation target is the accepted station events API route after implementation commit:

```text
97dc4d520ef8edc9b7620e5ce9e8a61d0e1aee7f
97dc4d5 Harden accepted station events API contract
```

Endpoint under validation:

```text
GET /api/v2/production/accepted-station-events
```

Validation purpose:

- prove the route still obeys `docs/contracts/dashboard_api_contract.md` when reading a real PostgreSQL database created from the project migration schema;
- prove the route reads only `production_accepted_station_event_fact`;
- prove DB-backed behavior matches the already hardened non-DB API contract for query bounds, cursor, DTO allowlist, forbidden leakage, source isolation, no side effects and failure behavior;
- do not validate Dashboard/frontend, Collector runtime, storage write path, PLC/V-PLC runtime behavior, deploy, tag, rollback or real PLC pilot.

### future run/test allowlist

Future execution is not authorized by this planning gate. If PM later opens a separate execution gate, the future test command allowlist is limited to the exact focused API test paths below.

Allowed future DB-backed execution command shape:

```bash
EDGE_MES_ENABLE_DB_BACKED_TESTS=1 \
EDGE_MES_DB_BACKED_TEST_DSN='postgresql://<test_user>:<password>@localhost:<port>/edge_mes_test_api_read' \
EDGE_MES_DB_BACKED_MAINTENANCE_DSN='postgresql://<test_user>:<password>@localhost:<port>/postgres' \
PYTHONPATH=api .venv/bin/python -m pytest \
  api/tests/test_accepted_station_events_api.py \
  api/tests/test_accepted_station_events_api_db_backed.py \
  -q
```

Allowed future default-safe preflight command, only if a later PM-authorized execution gate explicitly wants to confirm default skip behavior before DB opt-in:

```bash
PYTHONPATH=api .venv/bin/python -m pytest \
  api/tests/test_accepted_station_events_api.py \
  api/tests/test_accepted_station_events_api_db_backed.py \
  -q
```

File inclusion is frozen as:

- `api/tests/test_accepted_station_events_api.py`: included. Purpose: non-DB API contract regression for the hardened route.
- `api/tests/test_accepted_station_events_api_db_backed.py`: included. Purpose: guarded live PostgreSQL validation and schema/fixture/API-read assertions.

Forbidden future test execution unless PM opens a separate gate:

- `pytest`
- `python -m pytest`
- `pytest api`
- `pytest api/tests`
- `pytest collector`
- `pytest .`
- any broad pytest command without the exact two test file paths above
- any DB-backed command using a production DSN, non-loopback DSN, non-isolated DB or unapproved environment variable setup
- any command that starts Docker / docker compose, applies migrations outside the isolated test DB, or touches Collector/Dashboard/V-PLC/runtime surfaces

Troubleshooting with a narrower single test node, changing test paths, changing `-k`, changing DB names, or adding files requires separate PM authorization. This planning report does not authorize it.

### DB opt-in safety

`EDGE_MES_ENABLE_DB_BACKED_TESTS=1` is forbidden in this planning gate and may be used only in a later separately PM-authorized execution gate.

Future execution must preserve default-safe behavior:

- DB-backed tests must remain skipped unless `EDGE_MES_ENABLE_DB_BACKED_TESTS=1` is explicitly set in the execution gate.
- `EDGE_MES_DB_BACKED_TEST_DSN` must be present only during the authorized execution gate.
- `EDGE_MES_DB_BACKED_MAINTENANCE_DSN` must be present only during the authorized execution gate.
- The execution report must print or describe DSN safety in masked form; it must not leak credentials.
- If opt-in env vars are absent, malformed or unsafe, the run must skip or fail closed rather than connecting.

### DSN/test DB safety

Future execution DSN restrictions are frozen as:

- target DSN scheme must be `postgresql` or `postgres`;
- target host must be loopback/test-local only: `localhost`, `127.0.0.1` or `::1`;
- target DB name must match `edge_mes_test_*`;
- target DB name must not be `edge_mes`, `postgres`, `prod` or `production`;
- maintenance DSN host must also be loopback/test-local only;
- maintenance DB must be `postgres` or `template1` only;
- target DSN and maintenance DSN must be distinct;
- Docker service host names such as `postgres`, remote LAN IPs, public hostnames and production-like DB names are forbidden;
- non-isolated DBs are forbidden;
- the execution gate must create/use one isolated test DB and must drop it during cleanup.

Required cleanup behavior:

- future execution must drop the isolated test DB in `finally` / equivalent cleanup even on test failure;
- execution report must include cleanup result, for example:

```text
test_db_cleanup_ok edge_mes_test_api_read
```

- if cleanup is not confirmed, report `HOLD` and do not claim DB-backed validation PASS.

### migration/schema verification

Future execution must apply only the accepted fact visibility migration into the isolated test DB before fixture insert:

```text
db/migrations/007_accepted_station_event_visibility.sql
```

Migration expectations:

- apply migration against the isolated test DB only;
- do not apply migrations against production, compose default DB or any non-isolated DB;
- after migration apply and before any fixture insert, run schema verification;
- if schema verification fails, stop before fixture insert and report `HOLD` or test failure; do not query API as if schema were valid.

Schema verification must check:

- table existence:
  - `production_accepted_station_event_fact`
- accepted fact table columns / DTO authority columns:
  - `line_id`
  - `plc_id`
  - `station_id`
  - `station_type`
  - `profile_id`
  - `config_hash`
  - `config_version`
  - `event_type`
  - `production_result`
  - `unit_id`
  - `dmc`
  - `cycle_counter`
  - `source_event_id`
  - `event_ts`
  - `accepted_at`
  - `fact_key`
  - `content_fingerprint`
  - `nok_code`
  - `nok_origin`
  - `nok_detail_code`
  - `nok_detail_source_event_id`
  - `nok_detail_evidence_fact_key`
- table may also have internal `id BIGSERIAL PRIMARY KEY`; `id` is not part of the DTO and must not be returned by the API.

Nullable / NOT NULL expectations:

- NOT NULL:
  - `line_id`
  - `plc_id`
  - `station_id`
  - `station_type`
  - `profile_id`
  - `config_hash`
  - `config_version`
  - `event_type`
  - `cycle_counter`
  - `source_event_id`
  - `event_ts`
  - `accepted_at`
  - `fact_key`
  - `content_fingerprint`
- nullable:
  - `production_result`
  - `unit_id`
  - `dmc`
  - `nok_code`
  - `nok_origin`
  - `nok_detail_code`
  - `nok_detail_source_event_id`
  - `nok_detail_evidence_fact_key`

Unique constraints to verify:

- `uq_production_accepted_station_event_fact_key`
- `uq_production_accepted_station_event_source`

Accepted-fact check constraints to verify:

- `ck_production_accepted_station_event_type`
- `ck_production_accepted_station_event_result`
- `ck_production_accepted_station_result_authority`
- `ck_production_accepted_station_result_nok_authority`
- `ck_production_accepted_station_nok_detail_authority`

Verification query safety:

- schema verification queries must be metadata-only before fixture insert;
- schema verification must not contain `INSERT`, `UPDATE` or `DELETE`;
- fixture insert may occur only after migration apply and schema verification pass.

### fixture/API read validation

Future DB-backed validation fixture requirements:

- insert accepted fact rows only into isolated `production_accepted_station_event_fact`;
- include multiple `station_result` accepted facts for `LINE_001`;
- include same timestamp tie-breaker rows so order by `event_ts`, `accepted_at`, `fact_key` is proven;
- include at least one other-line accepted fact, for example `LINE_999`, to prove `line_id` isolation;
- include one accepted `station_nok` detail row with accepted upstream evidence fields:
  - `nok_code`
  - `nok_origin`
  - `nok_detail_code`
  - `nok_detail_source_event_id`
  - `nok_detail_evidence_fact_key`
- do not insert raw/candidate/diagnostic fallback rows to make the API pass;
- do not use legacy/current tables as fixture authorities.

Future API live DB read assertions must cover:

- `200` response for valid bounded request;
- exact DTO allowlist for every returned item;
- no forbidden source/surface leakage in response or cursor payload;
- API query reads only `production_accepted_station_event_fact`;
- valid line/window/limit filtering;
- empty-result behavior: valid bounded request with no matching accepted facts must return `200` with `data.items == []`, `page.next_cursor == null`, and echoed `page.limit`, with no legacy/current/raw fallback;
- NOK/detail fields come only from the accepted fact row fields and accepted upstream evidence;
- pagination returns no duplicates and no omissions;
- invalid cursor, tampered cursor or cross-scope cursor fails closed before DB query where applicable;
- unsupported filters and unknown query parameters fail closed.

Failure behavior to freeze for future execution:

- DB unavailable: route returns explicit fail-closed error, currently `503 {"detail": "accepted fact source unavailable"}`, with no fallback;
- missing table: schema verification fails before fixture insert, or route fails closed with the accepted fact source unavailable error if encountered at API query time; no fallback;
- missing schema / missing columns / nullability mismatch: schema verification fails before fixture insert; no fallback;
- missing accepted-fact authority constraints: schema verification fails before fixture insert; no fallback;
- forbidden source availability must never mask accepted fact table failure.

### source authority

Only production fact source for this validation:

- `production_accepted_station_event_fact`

Forbidden as fallback, join source, field filler, equivalent production fact source or legacy compatibility source:

- `raw_plc_sample`
- `cycle_event`
- `station_event`
- `production_unit`
- `quality_event`
- `production_snapshot`
- `production_events`

The route SQL must not join these tables. Missing accepted fact fields must remain null/empty/error according to contract; they must not be filled from any forbidden source.

### DTO/leakage assertions

Exact DTO allowlist has 22 fields:

- `line_id`
- `plc_id`
- `station_id`
- `station_type`
- `profile_id`
- `config_hash`
- `config_version`
- `event_type`
- `production_result`
- `unit_id`
- `dmc`
- `cycle_counter`
- `source_event_id`
- `event_ts`
- `accepted_at`
- `fact_key`
- `content_fingerprint`
- `nok_code`
- `nok_origin`
- `nok_detail_code`
- `nok_detail_source_event_id`
- `nok_detail_evidence_fact_key`

Forbidden in response DTO, cursor payload, meta/debug payload, helper output and Dashboard production consumer payload:

- raw payload / `raw_payload` / `raw_hex` / `raw_sample_id` / raw bytes
- decoded/source normalized candidate payload before accepted decision
- adapter disposition / reason / phase / candidate context
- raw/normalized comparison context
- decoder errors
- diagnostic/review/audit payloads
- `ack_status` / `read_done` / `collector_state`
- `quality_pareto_input` / `dashboard_state`
- bare `result` / `defect` / `quality` / `pareto`
- any legacy/current table join filler
- any synthetic field that makes non-accepted dispositions visible as production facts
- `work_order` / `product` until a later schema/contract authority gate creates accepted-fact authority for them

`accepted_at` must be treated only as accepted fact timestamp. It must not be interpreted as collector freshness, ACK time, station freshness or read_done time.

### query/cursor/pagination assertions

Allowed query subset for this DB-backed validation:

- `line_id`
- `start_time`
- `end_time`
- `limit`
- `cursor`

Unsupported filters must fail closed with 4xx, including but not limited to:

- `station_id`
- `station_type`
- `event_type`
- `production_result`
- `config_hash`
- `unit_id`
- `dmc`
- `cycle_counter`
- `source_event_id`
- `fact_key`
- `content_fingerprint`
- `nok_code`
- `nok_origin`
- `nok_detail_code`
- `nok_detail_source_event_id`
- `nok_detail_evidence_fact_key`
- `work_order`
- `product`
- raw/candidate/diagnostic/review/audit filters
- any unknown query parameter

Required query behavior:

- `line_id`, `start_time` and `end_time` are required;
- `start_time` and `end_time` must be strict timezone-aware ISO-8601 values;
- missing, malformed, unbounded, reversed or over-large time window fails closed;
- maximum time window remains 31 days unless a later contract changes it;
- `limit` defaults to 50 and maxes at 500;
- invalid `limit` fails closed;
- invalid, malformed, stale-version, unsigned/tampered or cross-scope cursor fails closed.

Cursor must bind:

- line scope;
- time window;
- limit;
- direction;
- ordering tuple;
- any future implemented accepted-fact filters, if a later separate gate expands the allowed filter set.

Stable ordering is frozen as:

```text
event_ts ASC
accepted_at ASC
fact_key ASC
```

Pagination assertions:

- page 1 and replayed page 2 must not duplicate rows;
- page 1 and replayed page 2 must not omit rows inside the bounded line/time scope;
- cursor payload must contain no forbidden DTO/source leakage fields;
- cursor replay with changed line/window/limit/direction/order must fail closed.

### no-side-effect assertions

Future DB-backed validation must prove or report:

- API route uses `BEGIN READ ONLY` or equivalent read-only semantics;
- route sets statement timeout;
- route sets idle/read timeout expectation;
- route performs no `INSERT`, `UPDATE` or `DELETE`;
- route performs no write-side helper call;
- route performs no ACK/read_done mutation;
- route performs no Collector / PLC / V-PLC / runtime / storage / Dashboard side effect;
- route does not mutate `ack_status`, `read_done`, `collector_state`, runtime status or PLC state;
- successful read commits read-only transaction;
- controlled query failure rolls back and does not commit;
- timeout failure proof remains a future separate gate unless the execution gate explicitly authorizes it.

### review sequence before execution

Before any future DB-backed execution, the planning report must pass:

1. Reliability planning review.
2. Data Quality planning review.
3. Verification planning review / exact future run allowlist audit.
4. PM explicit authorization for the execution gate.

A PASS from this planning gate does not authorize DB connection, `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`, test DB creation/deletion, migration apply, fixture insert, Docker, broad pytest, stage, commit, push, deploy, tag, rollback or real PLC pilot.

## Evidence

### read-only recovery

Initial recovery was run before edits. Result summary:

```text
branch: main...origin/main
HEAD: 1012d71f739d6fd847fca1a95bbd14349ac99ebf Add PM handoff after API implementation closeout
origin/main: 1012d71f739d6fd847fca1a95bbd14349ac99ebf
cached name-only: empty
pre-existing diff name-only: .gitignore
status all: known external dirty artifacts only
```

Recovery confirmed expected baseline:

```text
HEAD == origin/main == 1012d71f739d6fd847fca1a95bbd14349ac99ebf
```

### docs/checks run

Read-only/document checks used in this planning gate:

```text
wc -l required docs and references
sed read-only reads from required docs and optional API references
rg read-only key-term scans for source/DTO/cursor/DB-backed boundaries
sed read-only migration 007 schema reference
```

No tests were run. No DB-backed tests were run. No DB connection was made.

### git diff name-only

After this docs-only planning edit, task-relevant state:

```text
tracked diff name-only remains limited to pre-existing .gitignore
new untracked task file: docs/reports/sprint3_db_backed_api_validation_plan.md
```

### git cached name-only

Post-edit requirement:

```text
empty
```

### status

Post-edit allowed state:

```text
 M .gitignore
?? docs/reports/sprint3_db_backed_api_validation_plan.md
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

## Blockers

- none

## Recommendations

- Before the future execution gate, restate the exact masked DSN values and confirm the target database name matches `edge_mes_test_*`.
- Future execution report should explicitly include whether empty-result behavior was asserted by test output or by a named focused assertion; do not silently infer it from other-line fixtures.
- Future execution report should separately classify schema verification failures vs runtime API `503` failures so missing schema/table/authority does not get misreported as a normal empty result.
- Keep actual timeout failure proof as a separate future gate unless PM explicitly authorizes it.
- Keep optional debug/review diagnostics view deferred to a separate Level 2 gate.

## Next gate

### eligible for

- Reliability planning review for this DB-backed API validation planning report.
- Then Data Quality planning review.
- Then Verification planning review / exact future run allowlist audit.

### PM approval required before

- any DB-backed execution;
- setting `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`;
- setting DB-backed DSN env vars;
- creating/dropping isolated test DB;
- applying migrations;
- inserting fixtures;
- running the allowed future pytest command;
- editing API route/tests/db/main/migration files;
- Docker / deploy / tag / rollback / real PLC pilot;
- stage / commit / push.

## Thread 输出 / 上下文评估

- 本次输出长度：中
- 当前 Thread 是否建议继续：yes
- 下一轮是否建议新开 Thread：no
- 理由：本次是 docs-only planning gate，范围单一且上下文仍可控；下一步可在当前 PM Thread intake Reliability planning review report。如果进入 DB-backed execution 或需要测试/DB/Docker/代码修复，应按 gate 边界重新授权，必要时新开 Thread。
