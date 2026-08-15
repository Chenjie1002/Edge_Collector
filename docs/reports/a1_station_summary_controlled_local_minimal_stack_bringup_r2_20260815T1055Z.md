# A1 Station Summary Controlled Local Minimal Stack Bring-up R2

## Conclusion

```text
PASS / A1_LOCAL_MINIMAL_STACK_RUNTIME_READY
DATA_PATH_ROUTE_OR_SCOPE_FAILURE=ACCEPTED_FACT_SOURCE_UNAVAILABLE
```

The Owner-assisted local runtime transaction successfully established the exact minimal local stack `postgres -> api -> dashboard` from the previously materialized frozen images. The trusted Dashboard origin binding is correct and both API and Dashboard health endpoints returned HTTP 200. The remaining failure is not local runtime bring-up or frontend origin wiring: both trusted production data routes returned the accepted-fact-source unavailable boundary, and Station Summary surfaced that unavailability without fabricating data.

## Authority / task identity

```text
TASK=docs/thread_handoff/pm_task_20260815T1055Z_a1_station_summary_controlled_local_minimal_stack_bringup_r2.md
TASK_TYPE=regular/non-symlink
TASK_BYTES=15188
TASK_SHA256=7d87a6822fb17993b10eaaecc0b965d76414b729fbace9248f0e5205dfd07057
OWNER_AUTHORITY=approved A1_STATION_SUMMARY_CONTROLLED_LOCAL_MINIMAL_STACK_BRINGUP_R2
REPORT_PRESTATE=ABSENT
```

## Entry repository state

```text
BRANCH=main
HEAD=6226bf3fb716880a176f9eb642b8139cef3255a6
ORIGIN_MAIN=6226bf3fb716880a176f9eb642b8139cef3255a6
AHEAD_BEHIND=0/0
STAGED=0
TRACKED_DIRTY=0
DIFF_CHECK=PASS
CACHED_DIFF_CHECK=PASS
```

## Frozen image identities

The R2 lifecycle used the exact image identities established by the prior image-materialization PASS:

```text
postgres:16
  sha256:11a9d238fbb48bab14599c57e41123254452b1a2d93c6c8595bce96f346bd082

edge-mes-demo-api
  sha256:3e8dd63059df782930016211b39c584a5c6c3a751bbbe385cd2eb85f4dede6e2

edge-mes-dashboard:local
  sha256:445f2c100471ec207c020973681f9c02765d05476a1dd9e70999e767822edb5a
```

No build or pull was authorized or executed in this R2 gate.

## Lifecycle result

Exactly one authorized lifecycle invocation was performed:

```text
docker compose up -d --no-build --pull never postgres api dashboard
LIFECYCLE_COUNT=1
LIFECYCLE_RC=0
RETRY=0
CLEANUP=0
```

Compose created the project network and the three authorized containers only.

Bounded readiness completed on round 2:

```text
ROUND=1 PG=running/healthy API=running DASH=running/starting
ROUND=2 PG=running/healthy API=running DASH=running/healthy
RUNTIME_READY=1
```

Observed runtime objects:

```text
edge-mes-postgres
  container_id=37028d1bcf406e6c5597802ad383ec1a5ec291bbe22306ed71767f7295509451
  image=sha256:11a9d238fbb48bab14599c57e41123254452b1a2d93c6c8595bce96f346bd082
  status=running
  health=healthy
  started_at=2026-08-15T11:03:46.727486163Z

edge-mes-api
  container_id=56063ec1d3c047d69e8d9d09eb7b931d94a769823ee8a6f14c82668e997f92e3
  image=sha256:3e8dd63059df782930016211b39c584a5c6c3a751bbbe385cd2eb85f4dede6e2
  status=running
  published_port=8000

edge-mes-dashboard
  container_id=fad83ccca54258a50a004a4878ac78cc30cd1ffea13b5d33e20545be40d63e28
  image=sha256:445f2c100471ec207c020973681f9c02765d05476a1dd9e70999e767822edb5a
  status=running
  health=healthy
  started_at=2026-08-15T11:03:57.398487419Z
  published_port=3001
```

One read-only `docker inspect` formatting command emitted a template parsing error for the API because `.State.Health` is absent on a container without a healthcheck. This was a diagnostic formatting defect only. It did not consume lifecycle authority, mutate state, or undermine API runtime proof: readiness had already observed `API=running`, the final filtered Docker snapshot showed the API running, and the API health endpoint subsequently returned HTTP 200.

## Trusted origin result

Live Dashboard environment:

```text
EDGE_MES_DASHBOARD_API_ORIGIN=http://api:8000
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=container
TRUSTED_ORIGIN_ENV_OK=1
```

Therefore the previously observed localhost-preview message `Accepted events service is not configured.` is not reproduced by the controlled Compose Dashboard runtime. The current controlled Dashboard has the expected trusted origin binding.

## HTTP / data-path evidence

### API health

```text
GET /health -> HTTP 200
{"status":"ok"}
```

### OpenAPI route presence

```text
GET /openapi.json -> HTTP 200
ROUTE_PRESENT=/api/v2/production/scope-options
ROUTE_PRESENT=/api/v2/production/quality
ROUTE_PRESENT=/api/v2/process-metrics
```

### Scope catalog

```text
GET /api/v2/production/scope-options -> HTTP 200
contract=production-scope-options/v1
LINE_001 present
WS02 present
```

This proves the fixed query scope is recognized by the current local scope catalog.

### Quality

Fixed query:

```text
LINE_001 / WS02 / [2026-08-11T04:15:00Z, 2026-08-11T04:16:00Z)
```

Result:

```text
HTTP 503
{"detail":"accepted fact source unavailable"}
```

### Process Metrics

Same fixed scope/window returned:

```text
HTTP 503
status=UNAVAILABLE
reason.code=ACCEPTED_FACT_SOURCE_UNAVAILABLE
reason.detail=accepted fact source unavailable
source.authority=production_accepted_station_event_fact
source.config_window_state=UNRESOLVED
source.fallback=none
metrics=[]
```

### Dashboard

```text
GET /health -> HTTP 200
GET /station-summary -> HTTP 200
  Station Summary
  Select scope and apply

GET fixed-query /station-summary -> HTTP 200
  LINE_001
  WS02
  Quality source unavailable
  Process Metrics source unavailable
  UNAVAILABLE
```

The Dashboard therefore fails closed and reports upstream source unavailability. No evidence supports a frontend product defect in this gate.

## Exact classification

```text
RUNTIME_CLASSIFICATION=PASS / A1_LOCAL_MINIMAL_STACK_RUNTIME_READY
DATA_PATH_CLASSIFICATION=DATA_PATH_ROUTE_OR_SCOPE_FAILURE=ACCEPTED_FACT_SOURCE_UNAVAILABLE
```

Rejected adjacent classifications:

- `API_RUNTIME_UNREACHABLE`: rejected; API health and OpenAPI are HTTP 200.
- `DASHBOARD_CONTAINER_ENVIRONMENT_DRIFT`: rejected; live trusted-origin env exactly matches the committed container contract.
- `SCOPE_CATALOG_UNAVAILABLE`: rejected; scope-options is HTTP 200 and contains `LINE_001 / WS02`.
- `QUERY_SCOPE_MISMATCH`: rejected; the fixed scope is present in the catalog.
- `FRONTEND_PRODUCT_DEFECT`: rejected; Station Summary correctly surfaces both unavailable upstream sources.
- `DATA_PATH_REAL_DATA_VISIBLE`: not established; trusted production data source is unavailable locally.

The remaining unresolved boundary is below the API route/scope layer: the local API cannot read its required `production_accepted_station_event_fact` authority from the local PostgreSQL venue. This report does not infer whether the cause is a missing relation/view, schema/init mismatch, empty/incomplete local database materialization, or another DB-side availability condition because direct DB inspection was not authorized in this gate.

## Evidence boundary

This is local-only runtime truth. It does not invalidate the accepted Raspberry Pi G5 production evidence for WS02/WS03. The fixed local PostgreSQL venue may not contain the same production facts or schema state as the accepted remote venue.

## Allowlist / mutation accounting

```text
AUTHORIZED_SERVICES=postgres,api,dashboard
OTHER_COMPOSE_SERVICES_STARTED=0
BUILD=0
PULL=0
LIFECYCLE_INVOCATIONS=1
LIFECYCLE_RETRY=0
CLEANUP=0
DIRECT_DB_QUERY=0
DIRECT_DB_WRITE=0
PSQL=0
SSH=0
REMOTE_FS=0
VPLC_ACTION=0
PLC_ACTION=0
SOURCE_WRITE=0
UI_WRITE=0
COMPOSE_WRITE=0
GIT_STAGE/COMMIT/PUSH/TAG=0
```

PostgreSQL storage changes caused by normal startup are intrinsic authorized lifecycle side effects only; no application-level SQL mutation was performed by this gate.

## Final repository audit

Owner evidence and Mainline PM intake both establish:

```text
HEAD=6226bf3fb716880a176f9eb642b8139cef3255a6
ORIGIN_MAIN=6226bf3fb716880a176f9eb642b8139cef3255a6
AHEAD_BEHIND=0/0
STAGED=0
TRACKED_DIRTY=0
DIFF_CHECK=PASS
CACHED_DIFF_CHECK=PASS
```

The task and this report remain untracked/unstaged unless separately authorized later.

## MVP alignment

```text
MVP_ALIGNMENT=MVP-ALIGNED
```

The controlled local venue now proves that the A1 Station Summary frontend-to-API wiring is operational. The remaining MVP blocker is the local accepted production fact source availability, not UI cosmetics.

## Next gate

```text
NEXT_GATE=A1_LOCAL_ACCEPTED_FACT_SOURCE_READONLY_RECONCILIATION
```

The next gate should be a bounded local-only read-only DB/source reconciliation that determines why `production_accepted_station_event_fact` is unavailable in the current local PostgreSQL venue. It should distinguish at minimum: missing relation/view, schema/init materialization mismatch, DB/schema selection mismatch, relation present but query dependency failure, or another exact read-side cause.

This PASS grants no direct DB query, DB repair/write, schema creation, data seeding, container cleanup/restart, build/pull, source/UI/config changes, remote execution, Git publication, or A1-S2 authority.
