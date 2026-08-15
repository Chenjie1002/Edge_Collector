# A1 Local Accepted Fact Source Read-only Reconciliation

## Conclusion

```text
PASS / A1_LOCAL_ACCEPTED_FACT_SOURCE_RECONCILIATION_COMPLETE
EXACT_BOUNDARY = LOCAL_ACCEPTED_FACT_RELATION_MISSING
SPECIFIC_CAUSE = CURRENT_LOCAL_EDGE_MES_DATABASE_HAS_NO public.production_accepted_station_event_fact RELATION
```

The local API/database binding and PostgreSQL search path are valid. The current local `edge_mes` database does not contain `public.production_accepted_station_event_fact`, so the API's direct SELECT from that relation necessarily fails and is surfaced as `accepted fact source unavailable` / `ACCEPTED_FACT_SOURCE_UNAVAILABLE`.

This is a local schema/materialization gap. It is not a frontend defect, not an API route-registration defect, not a query-scope mismatch, and not a database host/search-path mismatch.

## Authority / task identity

```text
TASK = docs/thread_handoff/pm_task_20260815T1106Z_a1_local_accepted_fact_source_readonly_reconciliation.md
TASK_TYPE = regular / non-symlink
TASK_BYTES = 10677
TASK_SHA256 = 7ebbe1df1c6c810d0e1cd4074dae8b9438c450c30f4e59971f4c4950b2261952
AUTHORITY = OWNER-A1-LOCAL-ACCEPTED-FACT-SOURCE-READONLY-RECONCILIATION-20260815T1906+0800
REPORT_PRESTATE = ABSENT
```

## Accepted predecessor runtime state

The predecessor local minimal-stack gate established and this gate re-confirmed without lifecycle mutation:

```text
edge-mes-postgres = running / healthy
edge-mes-api = running
edge-mes-dashboard = running / healthy
```

Predecessor HTTP evidence remains accepted input:

- API `/health` = HTTP 200;
- relevant OpenAPI routes present;
- `/api/v2/production/scope-options` = HTTP 200 and contains `LINE_001 / WS02`;
- Quality fixed WS02 window = HTTP 503 `accepted fact source unavailable`;
- Process Metrics fixed WS02 window = HTTP 503, `reason.code=ACCEPTED_FACT_SOURCE_UNAVAILABLE`, source authority `production_accepted_station_event_fact`;
- Station Summary = HTTP 200 and safely reports the upstream source as unavailable.

No HTTP request was required or made in this reconciliation gate.

## Static DB/init/migration contract

`docker-compose.yml` binds PostgreSQL and API as follows:

```text
POSTGRES_DB=edge_mes
POSTGRES_USER=edge_mes
API DATABASE_URL=postgresql://edge_mes:***@postgres:5432/edge_mes
postgres initialization mount=./db/init:/docker-entrypoint-initdb.d:ro
```

The current declared fresh-init directory contains:

```text
db/init/001_schema.sql
db/init/002_seed.sql
db/init/003_event_schema.sql
db/init/004_unit_trace_schema.sql
db/init/005_vplc_parameter_audit.sql
```

There is no `production_accepted_station_event_fact` reference in `db/init/**`.

The accepted-fact relation DDL instead exists in:

```text
db/migrations/007_accepted_station_event_visibility.sql
```

That migration defines `production_accepted_station_event_fact` in the normal/public schema resolution path together with its constraints and indexes.

Current migration inventory observed:

```text
db/migrations/005_reliability_schema.sql
db/migrations/006_vplc_parameter_audit.sql
db/migrations/007_accepted_station_event_visibility.sql
```

Therefore the committed Compose bootstrap does not itself mount migration 007 into PostgreSQL's `/docker-entrypoint-initdb.d` bootstrap directory. This static fact explains why migration 007 is not guaranteed to be applied by the current declared local bootstrap path. The exact historical reason the existing `data/postgres` state lacks migration 007 is not promoted beyond the live fact that it is currently unapplied/missing.

## Live API DB binding

One bounded read-only `docker inspect edge-mes-api` environment read established, with password omitted from evidence:

```text
scheme = postgresql
user = edge_mes
host = postgres
port = 5432
database = edge_mes
```

This exactly matches the Compose-local PostgreSQL service/database target. Therefore:

```text
API_DB_BINDING_MISMATCH = NO
```

## Single read-only PostgreSQL reconciliation

Exactly one `docker exec edge-mes-postgres psql` invocation was used. It ran a single batch under:

```text
BEGIN TRANSACTION READ ONLY
...
ROLLBACK
```

No DDL, DML, COPY, schema mutation, seed, migration, or file-writing meta-command was used.

Live DB identity:

```text
current_database = edge_mes
current_user = edge_mes
current_schema = public
search_path = "$user", public
```

Accepted-fact relation lookup:

```text
to_regclass('public.production_accepted_station_event_fact') = NULL
```

No `pg_class / pg_namespace` row for that relation was returned.

The public schema itself is populated and queryable. The bounded catalog query observed 17 public relations, including existing project relations such as:

```text
cycle_event
station_event
production_unit
production_snapshot
quality_event
vplc_parameter_change_log
vplc_parameter_snapshot
```

This rules out a generally empty/uninitialized PostgreSQL catalog. The exact accepted-fact relation alone is absent from the current schema surface relevant to the API query.

Because the relation is absent, no row-count or fixed WS02-window content query was attempted; doing so would have required referencing a nonexistent relation and was unnecessary to establish the exact boundary.

## Exact boundary decision

```text
EXACT_BOUNDARY = LOCAL_ACCEPTED_FACT_RELATION_MISSING
```

Adjacent classes rejected:

- `API_DB_BINDING_MISMATCH`: rejected; API points to `postgres:5432/edge_mes`, matching the inspected local DB.
- `DB_SEARCH_PATH_OR_SCHEMA_MISMATCH`: rejected; current schema is `public`, search path includes `public`, and the specifically qualified `public.production_accepted_station_event_fact` is itself absent.
- `LOCAL_ACCEPTED_FACT_RELATION_PRESENT_EMPTY`: rejected; the relation does not exist.
- `LOCAL_ACCEPTED_FACT_FIXED_SCOPE_EMPTY`: rejected; relation absence occurs before row/window semantics.
- `LOCAL_ACCEPTED_FACT_PRESENT_AND_QUERYABLE`: rejected by `to_regclass = NULL`.
- frontend/query-scope defect: already excluded by predecessor runtime evidence and is upstream of the current source failure.

## Local versus remote truth

This result is local-only.

It does **not** invalidate the accepted Raspberry Pi G5 production evidence, where WS02/WS03 accepted production facts were previously verified after activation. The local database and the remote accepted production database are separate evidence surfaces.

Accordingly:

```text
REMOTE_G5_PRODUCTION_FACTS = PRESERVED / UNAFFECTED
LOCAL_ACCEPTED_FACT_SOURCE = UNAVAILABLE BECAUSE RELATION IS MISSING
```

## Budgets / mutations

```text
PSQL_PROCESS_INVOCATIONS = 1 / 1
DB_TRANSACTION_MODE = READ ONLY
DB_QUERY = bounded catalog/identity SELECT only
DB_WRITE = 0
DDL = 0
DML = 0
MIGRATION_APPLY = 0
DATA_SEED = 0
HTTP = 0
DOCKER_LIFECYCLE = 0
BUILD/PULL = 0
SSH/REMOTE = 0
VPLC/PLC = 0
GIT_MUTATION = 0
SUB_AGENT = 0
```

Repository changes for this gate are limited to this exact durable report plus the already-materialized task file; both remain untracked/unstaged unless separately authorized later.

## Final continuity

At final audit:

```text
HEAD = 6226bf3fb716880a176f9eb642b8139cef3255a6
origin/main = 6226bf3fb716880a176f9eb642b8139cef3255a6
staged = 0
tracked dirty = 0
git diff --check = PASS
git diff --cached --check = PASS
```

Runtime remained continuously present:

```text
edge-mes-postgres = running / healthy
edge-mes-api = running
edge-mes-dashboard = running / healthy
```

No cleanup or restart was performed.

## MVP alignment

```text
MVP_ALIGNMENT = MVP-ALIGNED
```

This diagnosis directly isolates why the already-approved Station Summary cannot consume accepted production facts in the local runtime. It does not expand UI or product scope.

## Recommendation / next gate

```text
NEXT_GATE = MAINLINE_PM_INTAKE_A1_LOCAL_ACCEPTED_FACT_SOURCE_RECONCILIATION
```

The most likely minimal successor is a separately authorized local schema-materialization gate whose first question is whether applying the accepted migration chain through `007_accepted_station_event_visibility.sql` to the current local database is safe and sufficient. That successor must independently account for migration ordering/dependencies and current schema state before any DDL is executed.

This report grants no migration execution, schema repair, data seed/replay, Collector/V-PLC activity, remote sync, Docker lifecycle, Git publication, or UI authority.