# Sprint 4 D1-R2 Existing Accepted Production Fact DB/API Reconciliation

## 报告名称

Sprint 4 D1-R2 Existing Accepted Production Fact DB/API Reconciliation

## 任务名称

Data-first Gate D1-R2 — Locate One Pre-existing Accepted Result and Reconcile PostgreSQL/API

## 执行 Thread

新的独立 Architecture / Integration Thread

## Authority

~~~text
Authority ID: SPRINT4-D1-R2-EXISTING-ACCEPTED-FACT-DB-API-9e0aba2
Authority type: READ-ONLY PRODUCT/DATA RECONCILIATION
Implementation / data-generation / remote-mutation authority: NONE / NONE / NONE
~~~

## 结论

~~~text
HOLD / NO_PREEXISTING_ELIGIBLE_ACCEPTED_RESULT
~~~

冻结 discovery scope 内没有 normal-profile、station_result、production_result 为 ok/nok 且能形成唯一一微秒 API scope 的既有 accepted production fact。本结论不是 Collector、PostgreSQL 或 API 产品缺陷；本任务没有生成或修改数据。

## D1-R1 proportional evidence intake

按 PM 正式 intake 读取并保留 D1-R1 的 thread-local terminal HOLD / IDENTITY_INSPECT_COMMAND_OR_CAPTURE_DEFECT，未修改其报告、未建立第三个 identity-only diagnostic。

~~~text
SSH target exit: 0; stderr: empty
API tuple field count: 7; observed fields match frozen API expected fields
PostgreSQL tuple field count: 6; observed fields match frozen PostgreSQL expected fields
runtime identity drift in captured tuples: not present
marker naming/punctuation difference: diagnostic-only / non-blocking
~~~

本任务不以 marker literal、marker punctuation、marker naming 或 stdout label spelling 阻塞字段比较。

## Required reads and truth boundary

已按授权顺序读取 handoff、current_status Section 0D、roadmap 1A/3/5/6/8、PM rules 12/13/14、API4/L2D、D1、D1-R1、migration 007、accepted fact builder、Collector accepted transaction path、Storage accepted fact insert path、accepted-events route。

production_accepted_station_event_fact 是 accepted-only production landing surface。非 accepted disposition、raw/normalized candidate、adapter/decoder diagnostics 和 review/audit data 不能成为 production truth。API 只从该表按同一 line_id 与 [start_time,end_time) scope、read-only transaction、3s timeout、event_ts ASC / accepted_at ASC / fact_key ASC 顺序读取 DTO allowlist。D1/D1-R1 均未执行 DB query 或 accepted-events GET；没有恢复 Dashboard browser、pagination、Case A/B/C 或 22-field plan。

## Live Git recovery and report precondition

~~~text
Git root: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
origin/main: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind: 0 / 0
cached: empty
protected source (frontend, api, docker-compose.yml): PASS (exit 0)
~~~

Tracked dirty set was preserved exactly:

~~~text
.gitignore
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
~~~

Task-external untracked reports remained untouched:

~~~text
docs/reports/sprint4_existing_real_accepted_production_fact_readonly_reconciliation.md
docs/reports/sprint4_d1_r1_minimal_runtime_identity_field_diagnostic.md
~~~

Other pre-existing untracked reports, handoffs and frontend generated artifacts remained external. Before SSH this target was ABSENT / NON-SYMLINK / UNTRACKED / UNSTAGED.

## Frozen discovery scope

~~~text
line_id: LINE_001
profile_id: normal
event_type: station_result
production_result: ok or nok
discovery_start_time: 2026-07-16T09:23:34.000000Z
discovery_end_time: 2026-07-23T09:23:34.000000Z
interval: [start, end), exactly 7 days
~~~

The current UTC instant was obtained once before SSH. No second window, line, scope, now() value, or retry was used.

## Runtime eligibility

Each direct docker inspect exited 0 and emitted exactly one complete tuple.

| Runtime | Hard-gate fields | Observed | Result |
| --- | --- | --- | --- |
| API | Image; Config.Image; project/service; status | sha256:9f03f370b37fd5fd2ddfd4e4e9e64d4c6b60312910e731157888544371683c11; edge-mes-demo-api; edge-mes-demo/api; running | PASS |
| PostgreSQL | Image; project/service; status | sha256:f961d097a9cedd37779baef1aab3fe87ef1c63b3b34d361f90a98ea5c9b77e56; edge-mes-demo/postgres; running | PASS |

~~~text
API tuple count: 7
API diagnostic-only Id / RestartCount:
12e841b4ac33a75c835cee81f0df46e4dbcdb9382b50ca50523f5fad02c57058 / 0

PostgreSQL tuple count: 6
PostgreSQL diagnostic-only Id / RestartCount:
bb3ba0738e692c68b14a62ca64296e484990d3b86b1f6d395c27b200af5cb890 / 0

API hard-gate fields: PASS
PostgreSQL hard-gate fields: PASS
diagnostic-only changes: none observed
~~~

## Exactly-once accounting

~~~text
SSH invocation / remote shell sequence: 1 / 1
API inspect / PostgreSQL inspect: 1 / 1
DB query: 1
accepted-events HTTP GET / short JSON parser: 0 / 0
retry / second scope / second SSH: 0 / 0 / 0
remote mutation: 0
~~~

Remote environment was PATH=/usr/bin:/bin and DOCKER_HOST=unix:///var/run/docker.sock; HOME, DOCKER_CONFIG, BUILDX_CONFIG, DOCKER_CONTEXT, DOCKER_TLS_VERIFY and DOCKER_CERT_PATH were unset.

## DB query and candidate terminal

One CTE statement against public.production_accepted_station_event_fact used default_transaction_read_only=on and statement_timeout=3s. Within the frozen scope it filtered LINE_001, normal, station_result, and ok/nok; ordered candidates by event_ts ASC, accepted_at ASC, fact_key ASC; and selected at most one candidate only if the same-line [event_ts,event_ts + 1 microsecond) API scope had exact_scope_count = 1.

~~~text
DB query exit: 0
candidate row: absent
eligible pre-existing accepted result: NOT FOUND
exact scope count: N/A (no candidate)
terminal: HOLD / NO_PREEXISTING_ELIGIBLE_ACCEPTED_RESULT
~~~

## Exact API scope and HTTP/JSON terminal

No candidate exists, so no exact API scope can be formed and the contractual HTTP branch was not entered.

~~~text
API scope: N/A
accepted-events HTTP GET: 0
HTTP status / data.items / page.limit / page.next_cursor: N/A / N/A / N/A / N/A
JSON parser: 0
~~~

## 10-field reconciliation matrix

No DB/API identity value is inferred or marked PASS.

| Field | DB value | API value | Result |
| --- | --- | --- | --- |
| line_id | N/A | N/A | N/A — no eligible candidate |
| plc_id | N/A | N/A | N/A — no eligible candidate |
| station_id | N/A | N/A | N/A — no eligible candidate |
| profile_id | N/A | N/A | N/A — no eligible candidate |
| config_hash | N/A | N/A | N/A — no eligible candidate |
| event_type | N/A | N/A | N/A — no eligible candidate |
| production_result | N/A | N/A | N/A — no eligible candidate |
| source_event_id | N/A | N/A | N/A — no eligible candidate |
| event_ts | N/A | N/A | N/A — no eligible candidate |
| fact_key | N/A | N/A | N/A — no eligible candidate |

## Forbidden-surface audit

N/A — no API response. The task did not observe or infer behavior for raw, raw_payload, raw_evidence, normalized, normalized_candidate, decoder, decoder_diagnostics, adapter, adapter_disposition, review, audit, quality_pareto_input, dashboard_state, bare result, defect, quality or pareto. production_result remains the allowed authoritative field.

## Prohibited-action audit

~~~text
data generation, V-PLC, PLC, Collector runtime: 0
SQL INSERT / UPDATE / DELETE / DDL, migration, schema change: 0
Docker build/tag, Compose lifecycle, restart/recreate, logs, network/volume mutation, cleanup/prune: 0
browser, pagination, cursor, Case A/B/C, 22-field reconciliation: 0
fixture/mock/synthetic data: 0
source/config/test/current-status/roadmap/rules/D1/D1-R1 report edits: 0
generic controller, reusable validator, evidence platform, remote script file: 0
stage/commit/push/tag/git clean: 0
remote mutation: 0
~~~

## Blockers

~~~text
Exact blocker: no pre-existing eligible accepted result in the frozen discovery scope.
Product defect claim: none.
~~~

## Recommendations and next gate

~~~text
Recommendations: PM intake only.
Eligible for: PM decision only.
PM approval required before: controlled fresh accepted-result generation, any new discovery scope, DB/API retry, or a new product/data gate.
~~~

This authority does not authorize data generation, pagination, OEE, Quality, Trace, Dashboard, Git operation, or Full Runtime work.

## MVP 路径一致性

~~~text
approved product claim:
accepted production fact -> PostgreSQL production landing surface -> bounded accepted-events API

minimum truth invariant:
one DB production fact and one API DTO item must match in the same exact scope

new capability/infrastructure: none
scope drift: none
classification: MVP-ALIGNED
~~~

The task proportionally tested the pre-existing-data prerequisite and stopped on its defined empty terminal. Marker or evidence-format repair did not become the primary deliverable.

## Thread 输出 / 上下文评估

~~~text
output length: medium
current Thread continue: no
new Thread required: yes
reason: the independent authority's sole SSH and DB query are consumed; any generation or new scope requires fresh PM authority and invocation counts.
~~~

## Final Git audit

The final read-only Git audit confirmed:

~~~text
HEAD == origin/main: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind: 0 / 0
cached: empty
tracked dirty: unchanged (.gitignore, current_status.md, roadmap.md, pm_operating_rules.md)
protected source (frontend, api, docker-compose.yml): PASS
target: regular / non-symlink / untracked / unstaged / uncommitted
target whitespace diagnostics: NONE (git diff --no-index --check exit 1 is expected for an untracked file)
target conflict markers: NONE
only task-created path: this report
~~~

## PM intake

~~~text
报告名称：Sprint 4 D1-R2 Existing Accepted Production Fact DB/API Reconciliation
任务名称：Data-first Gate D1-R2 — Locate One Pre-existing Accepted Result and Reconcile PostgreSQL/API
执行 Thread：新的独立 Architecture / Integration Thread

结论：HOLD / NO_PREEXISTING_ELIGIBLE_ACCEPTED_RESULT

Live baseline:
- HEAD: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
- origin/main: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
- ahead/behind: 0 / 0
- cached: empty
- protected source: PASS

Runtime eligibility:
- API hard-gate fields: PASS
- PostgreSQL hard-gate fields: PASS
- diagnostic-only changes: none observed

Invocation counts:
- SSH: 1
- API inspect: 1
- PostgreSQL inspect: 1
- DB query: 1
- HTTP GET: 0
- JSON parser: 0
- remote mutation: 0

Frozen scope:
- line: LINE_001
- start: 2026-07-16T09:23:34.000000Z
- end: 2026-07-23T09:23:34.000000Z

DB evidence:
- eligible candidate: NOT FOUND
- exact scope count: N/A

API evidence:
- HTTP / items / limit / next_cursor: N/A / N/A / N/A / N/A

Reconciliation:
- 10-field result: N/A — no eligible candidate
- forbidden-surface result: N/A — no API item

Blockers:
- no pre-existing eligible accepted result in the frozen scope

Recommendations:
- PM intake only

Next gate:
- eligible for: PM decision only
- PM approval required before: controlled fresh accepted-result generation or any new scope/retry

MVP 路径一致性：
- approved product claim: accepted production fact -> PostgreSQL production landing surface -> bounded accepted-events API
- minimum truth invariant: one DB fact and one API DTO item must match in the same exact scope
- new capability/infrastructure: none
- scope drift: none
- classification: MVP-ALIGNED

Thread 输出 / 上下文评估：
- output length: medium
- current Thread continue: no
- new Thread required: yes
- reason: exactly-once SSH and DB-query authority consumed
~~~
