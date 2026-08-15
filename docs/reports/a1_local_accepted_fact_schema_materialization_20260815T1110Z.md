# A1 Local Accepted Fact Schema Materialization

## Conclusion

```text
PASS / A1_LOCAL_ACCEPTED_FACT_SCHEMA_MATERIALIZATION_COMPLETE
EXACT_SCHEMA_RESULT = PUBLIC_ACCEPTED_FACT_RELATION_MATERIALIZED
POST_SCHEMA_SOURCE_STATE = AVAILABLE_BUT_EMPTY
LOCAL_ACCEPTED_FACT_ROW_COUNT = 0
```

This gate resolved the exact local schema blocker previously classified as `LOCAL_ACCEPTED_FACT_RELATION_MISSING`. It did not insert, import, synthesize or replay any accepted production facts.

## Authority

Owner authority: `OWNER-A1-LOCAL-ACCEPTED-FACT-SCHEMA-MATERIALIZATION-20260815T1909+0800`, based on Owner instruction `批准 A1_LOCAL_ACCEPTED_FACT_SCHEMA_MATERIALIZATION`.

Authoritative task:

```text
docs/thread_handoff/pm_task_20260815T1110Z_a1_local_accepted_fact_schema_materialization.md
TYPE = regular / non-symlink
BYTES = 9215
SHA256 = 1f4001aa11b484f93cd144c37b333ed8059780f1af06717861016bfadc685d25
```

Migration authority:

```text
db/migrations/007_accepted_station_event_visibility.sql
SHA256 = 5b60d7baf35dce20adc4d705533763dad394118e9b4e51295729d78c507ab0eb
DDL_INVOCATION_MAX = 1
RETRY = 0
CLEANUP = 0
DATA_DML = 0
```

## Entry baseline

```text
branch = main
HEAD = 6226bf3fb716880a176f9eb642b8139cef3255a6
origin/main = 6226bf3fb716880a176f9eb642b8139cef3255a6
ahead/behind = 0/0
staged = 0
tracked dirty = 0
git diff --check = PASS
git diff --cached --check = PASS
```

Runtime continuity before mutation:

```text
edge-mes-postgres = running / healthy
edge-mes-api = running
edge-mes-dashboard = running / healthy
```

## Migration ordering / compatibility preflight

Repository migration inventory:

```text
db/migrations/005_reliability_schema.sql
db/migrations/006_vplc_parameter_audit.sql
db/migrations/007_accepted_station_event_visibility.sql
```

`db/migrations/006_vplc_parameter_audit.sql` and `db/init/005_vplc_parameter_audit.sql` are not byte-identical, but the only semantic difference is that migration 006 wraps the same DDL in outer `BEGIN; ... COMMIT;`. Live DB verification established both VPLC audit tables and all three init-declared secondary indexes:

```text
vplc_parameter_change_log
vplc_parameter_snapshot
idx_vplc_parameter_change_time
idx_vplc_parameter_change_station
idx_vplc_parameter_snapshot_time
```

Migration 007 contains no foreign-table references, extensions, custom types, functions, views or explicit dependencies on migration 006 objects. It is therefore standalone-compatible with the current local schema.

A first read-only diagnostic query used incorrect expected names for two VPLC indexes and reported a diagnostic count of 1. No mutation occurred. A bounded corrective read-only enumeration immediately proved all three actual init-005 index names above exist. This was a diagnostic predicate correction, not repository or DB repair.

## Read-only DB preflight

```text
current_database = edge_mes
current_user = edge_mes
current_schema = public
search_path = "$user", public
CREATE privilege on public = true
public.production_accepted_station_event_fact = NULL / absent
vplc_parameter_change_log = present
vplc_parameter_snapshot = present
```

This preserved the prior exact boundary: the API was connected to the intended DB/schema, and the accepted-fact relation itself was missing.

## Controlled DDL transaction

Execution lock:

```text
MIGRATION_SHA = 5b60d7baf35dce20adc4d705533763dad394118e9b4e51295729d78c507ab0eb
DB = edge_mes
USER = edge_mes
TARGET = public.production_accepted_station_event_fact
DDL_INVOCATION_MAX = 1
RETRY = 0
CLEANUP = 0
DATA_DML = 0
```

Exactly one migration invocation was executed through the existing `edge-mes-postgres` container with `psql -X -v ON_ERROR_STOP=1 -U edge_mes -d edge_mes`, using the exact migration file on stdin.

Result:

```text
BEGIN
CREATE TABLE
CREATE INDEX x5
COMMENT statements completed
COMMIT
DDL_RC = 0
DDL_INVOCATIONS = 1/1
```

No migration 005/006 execution, no retry, no DROP, no cleanup and no row-level DML occurred.

## Post-DDL schema verification

Read-only verification established:

```text
TARGET_KIND = r  # ordinary table
COLUMN_COUNT = 23
ROW_COUNT = 0
CONSTRAINT_COUNT = 8
INDEX_COUNT = 8
```

Columns:

```text
id,line_id,plc_id,station_id,station_type,profile_id,config_hash,config_version,
event_type,production_result,unit_id,dmc,cycle_counter,source_event_id,event_ts,
accepted_at,fact_key,content_fingerprint,nok_code,nok_origin,nok_detail_code,
nok_detail_source_event_id,nok_detail_evidence_fact_key
```

Constraints present:

```text
production_accepted_station_event_fact_pkey
uq_production_accepted_station_event_fact_key
uq_production_accepted_station_event_source
ck_production_accepted_station_event_type
ck_production_accepted_station_event_result
ck_production_accepted_station_result_authority
ck_production_accepted_station_result_nok_authority
ck_production_accepted_station_nok_detail_authority
```

Expected migration indexes plus PK/unique backing indexes are present. VPLC audit table continuity remained intact.

## Post-DDL API verification

Fixed query:

```text
LINE_001 / WS02 / [2026-08-11T04:15:00Z, 2026-08-11T04:16:00Z)
```

Quality:

```text
HTTP 200
ok = 0
nok = 0
denominator = 0
quality_rate = null
data_sufficiency = UNAVAILABLE
```

This is an empty-data response, not a source-unavailable error.

Process Metrics:

```text
HTTP 200
status = PARTIAL
reason.code = EMPTY_ACCEPTED_WINDOW
reason.detail = query succeeded; no accepted facts
source.authority = production_accepted_station_event_fact
source.fallback = none
accepted_event_count = 0
```

Therefore the prior `503 / ACCEPTED_FACT_SOURCE_UNAVAILABLE` was resolved by materializing the missing relation. Current local data-path state is now `SOURCE_AVAILABLE_BUT_EMPTY`.

## Evidence boundary

This gate establishes only local schema availability. It does not establish that the local PostgreSQL contains the accepted production facts previously verified on the Raspberry Pi, and it does not import or recreate those remote facts.

The accepted remote G5 production evidence remains separate historical/runtime authority. The current local accepted-fact relation contains zero rows.

## Allowlist compliance

```text
DDL invocation = 1/1
DDL RC = 0
DDL retry = 0
INSERT = 0
UPDATE = 0
DELETE = 0
TRUNCATE = 0
COPY = 0
data seed/import = 0
Docker lifecycle = 0
Docker build/pull = 0
SSH/remote = 0
V-PLC/PLC action = 0
source/UI/compose write = 0
Git mutation = 0
```

Repository writes for this gate are limited to the authoritative task file and this exact durable report. PostgreSQL schema changes are the explicit Owner-authorized runtime mutation.

## MVP alignment

```text
MVP_ALIGNMENT = MVP-ALIGNED
```

The gate restored the minimum local accepted-fact schema required for A1 trusted real-data consumption without weakening source authority or fabricating data.

## Next gate

```text
NEXT_GATE = MAINLINE_PM_INTAKE_A1_LOCAL_ACCEPTED_FACT_SCHEMA_MATERIALIZATION
RECOMMENDED_SUCCESSOR = A1_LOCAL_ACCEPTED_FACT_DATA_SOURCE_RECONCILIATION
```

The successor should determine the correct provenance-preserving way for the local environment to obtain accepted facts. This PASS grants no data seeding, remote fact import, Collector activation, V-PLC stimulus, source/UI repair, Git publication or A1-S2 authority.
