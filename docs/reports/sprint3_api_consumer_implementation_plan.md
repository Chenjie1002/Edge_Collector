# Sprint 3 API implementation planning gate report

Date: 2026-07-05
Thread: Architecture / Integration
Status: PASS WITH RECOMMENDATIONS

This gate is planning only. It does not claim API implementation is complete and
does not authorize FastAPI/API implementation, tests, DB execution, Docker,
Dashboard/frontend work, migration/schema changes, Collector/runtime/storage.py
changes, staging, commit, push, deploy, tag, rollback or real PLC pilot.

## 1. API implementation objective

Future implementation target:

- endpoint: `GET /api/v2/production/accepted-station-events`
- route family: production accepted fact read path under `/api/v2/production`
- behavior: return paged accepted station-event business facts from
  `production_accepted_station_event_fact` only, with bounded query parameters,
  stable ordering, tamper-resistant cursor, DTO allowlist enforcement, forbidden
  source leakage negatives and no side effects.

This is a delta hardening / contract-alignment plan for the existing endpoint,
not a new consumer-facing route. The existing route and tests already reference
the endpoint, accepted fact source, DTO allowlist, HMAC cursor, read-only
transaction, timeout settings and focused leakage negatives. Future
implementation must still be treated as a new Level 2 implementation gate
because this planning gate does not edit or validate the route.

Future implementation deltas to evaluate before coding:

- align the route and tests with every frozen contract expectation in
  `docs/contracts/dashboard_api_contract.md`;
- decide whether the next implementation slice implements accepted-fact filters
  beyond `line_id`, `start_time`, `end_time`, `limit` and `cursor`, or explicitly
  fails closed for unsupported filter parameters until a later filter slice;
- bind cursor payload to every implemented accepted-fact filter, limit,
  direction and ordering tuple;
- freeze HTTP error envelope details and concrete DB unavailable / missing table
  / missing schema / missing authority behavior before implementation review;
- keep Dashboard component field matrix as read-only consumer reference only,
  with no Dashboard implementation in the API implementation gate.

## 2. Source authority

The only consumer-facing production fact source is:

- `production_accepted_station_event_fact`

Forbidden as production source, fallback, legacy compatibility source or
join-derived field filler:

- `raw_plc_sample`
- `cycle_event`
- `station_event`
- `production_unit`
- `quality_event`
- `production_snapshot`
- `production_events`

DTO fields must be mapped field-by-field from
`production_accepted_station_event_fact` row fields only. Fallback is forbidden
for every field. Missing accepted fact fields must remain null, absent,
unknown/error per contract, or fail closed according to the future error
contract; they must not be filled from legacy/current/raw/diagnostic sources.

## 3. DTO implementation acceptance matrix

| DTO field | Source row field | Meaning | Fallback |
| --- | --- | --- | --- |
| `line_id` | `production_accepted_station_event_fact.line_id` | line scope | forbidden |
| `plc_id` | `production_accepted_station_event_fact.plc_id` | PLC scope | forbidden |
| `station_id` | `production_accepted_station_event_fact.station_id` | station scope | forbidden |
| `station_type` | `production_accepted_station_event_fact.station_type` | station class | forbidden |
| `profile_id` | `production_accepted_station_event_fact.profile_id` | profile scope | forbidden |
| `config_hash` | `production_accepted_station_event_fact.config_hash` | historical config authority | forbidden |
| `config_version` | `production_accepted_station_event_fact.config_version` | config lineage label | forbidden |
| `event_type` | `production_accepted_station_event_fact.event_type` | accepted station-event kind | forbidden |
| `production_result` | `production_accepted_station_event_fact.production_result` | accepted result for `station_result` only | forbidden |
| `unit_id` | `production_accepted_station_event_fact.unit_id` | unit trace key when present on accepted fact row | forbidden |
| `dmc` | `production_accepted_station_event_fact.dmc` | DMC trace key when present on accepted fact row | forbidden |
| `cycle_counter` | `production_accepted_station_event_fact.cycle_counter` | source cycle counter | forbidden |
| `source_event_id` | `production_accepted_station_event_fact.source_event_id` | stable source event identity | forbidden |
| `event_ts` | `production_accepted_station_event_fact.event_ts` | source event time | forbidden |
| `accepted_at` | `production_accepted_station_event_fact.accepted_at` | accepted fact timestamp only; not collector freshness, ACK time, station freshness or read_done time | forbidden |
| `fact_key` | `production_accepted_station_event_fact.fact_key` | immutable production fact identity/reference | forbidden |
| `content_fingerprint` | `production_accepted_station_event_fact.content_fingerprint` | immutable content identity/reference | forbidden |
| `nok_code` | `production_accepted_station_event_fact.nok_code` | accepted NOK code only | forbidden |
| `nok_origin` | `production_accepted_station_event_fact.nok_origin` | accepted NOK origin only | forbidden |
| `nok_detail_code` | `production_accepted_station_event_fact.nok_detail_code` | accepted detail code only | forbidden |
| `nok_detail_source_event_id` | `production_accepted_station_event_fact.nok_detail_source_event_id` | detail source evidence identity | forbidden |
| `nok_detail_evidence_fact_key` | `production_accepted_station_event_fact.nok_detail_evidence_fact_key` | accepted upstream evidence fact reference | forbidden |

NOK/detail fields are visible only when present on accepted fact rows and bound
to accepted upstream business evidence plus shared station-event validation.
They must not be synthesized from adapter reason code, raw mismatch, decoder
error, candidate context or non-accepted disposition.

## 4. Forbidden DTO / source leakage matrix

Future implementation and tests must prove the response DTO, cursor payload,
meta/debug payloads, helper output and Dashboard production consumer payloads do
not expose, derive or use:

| Forbidden surface | Acceptance expectation |
| --- | --- |
| raw payload / `raw_payload` / `raw_hex` / `raw_sample_id` / raw bytes | never returned, used as filter authority or embedded in cursor/meta |
| decoded/source normalized candidate payload before accepted decision | never returned or used to fill DTO fields |
| adapter disposition / reason / phase / candidate context | never production-visible and never NOK/detail authority |
| raw/normalized comparison context | diagnostic/review only; no production DTO leakage |
| decoder errors | diagnostic/review only; no production DTO leakage |
| diagnostic/review/audit payloads | no production API or Dashboard production payload exposure |
| `ack_status` / `read_done` / `collector_state` | no read-path DTO, meta, filter or mutation authority |
| `quality_pareto_input` / `dashboard_state` | forbidden production sources and DTO keys |
| bare `result` / `defect` / `quality` / `pareto` | forbidden ambiguous production-looking keys |
| legacy/current table join filler | no joins to fill missing accepted fact fields |
| synthetic non-accepted production-visible fields | forbidden; non-accepted dispositions remain non-production-visible |

`work_order` and `product` remain excluded until a later schema/contract
authority gate creates accepted fact authority for them.

## 5. Query / filter / sort / page plan

Future implementation acceptance expectations:

- `line_id` is required, unless the service injects an explicit audited
  single-line default. Implicit cross-line reads are forbidden.
- `start_time` and `end_time` are required, bounded and parsed as strict
  timezone-aware ISO-8601.
- Maximum query window is 31 days unless a later contract changes the limit.
- `limit` defaults to 50 and has max 500.
- Stable order is `event_ts ASC`, `accepted_at ASC`, `fact_key ASC`.
- Cursor is tamper-resistant, schema/version checked and fail-closed.
- Cursor binds line, time range, every implemented accepted-fact filter, limit,
  direction and ordering tuple.
- Invalid filter, invalid cursor, invalid limit, invalid time, missing window,
  unbounded window and over-large window fail closed with 4xx.
- Eligible accepted-fact filters for this contract family are `station_id`,
  `station_type`, `event_type`, `production_result`, `config_hash`, `unit_id`,
  `dmc`, `cycle_counter`, `source_event_id`, `fact_key`, `content_fingerprint`,
  `nok_code`, `nok_origin`, `nok_detail_code`,
  `nok_detail_source_event_id` and `nok_detail_evidence_fact_key`.
- Any unimplemented eligible filter must either be left out of the authorized
  implementation slice or explicitly rejected with 4xx; it must not be ignored
  silently or implemented through legacy/raw/current sources.

## 6. Reliability plan

Future implementation must satisfy:

- read-only DB transaction or equivalent read-only query semantics;
- documented statement timeout and idle/read timeout expectations;
- bounded query protection through required scope, bounded time range, max
  window, limit and cursor binding;
- DB unavailable, missing table, missing schema, missing authority and
  unknown-state behavior defined as explicit error, empty or unknown response;
- no fallback to legacy/raw/current/diagnostic sources under DB unavailable,
  missing table, missing schema, missing authority or unknown-state conditions;
- no `INSERT`, `UPDATE` or `DELETE`;
- no write-side helper reuse;
- no ACK/read_done mutation;
- no Collector, PLC, V-PLC, runtime, storage or Dashboard side effect;
- `fact_key`, `content_fingerprint` and `source_event_id` remain identity /
  reference fields only, not mutation authority.

## 7. Data Quality plan

Future Data Quality review must verify:

- every DTO field is sourced from the accepted fact row field named in the
  acceptance matrix;
- NOK/detail fields bind only to accepted upstream business evidence and shared
  station-event validation;
- raw, diagnostic, candidate, comparison and decoder-error payloads cannot
  leak into production facts, OEE, traceability, Quality/Pareto or Dashboard
  production surfaces;
- `accepted_at` is the accepted fact timestamp only, not collector freshness,
  ACK time, station freshness or read_done time;
- `work_order` and `product` remain excluded until a future schema/contract
  authority gate.

## 8. Verification plan

Future implementation test/review matrix:

| Matrix area | Required coverage |
| --- | --- |
| DTO positive allowlist | response items contain exactly allowed DTO fields, including all NOK/detail evidence fields |
| Forbidden field/source negatives | every forbidden surface in section 4 absent from response, cursor/meta/helper output and SQL source usage |
| Source isolation | query reads `production_accepted_station_event_fact` only and never joins forbidden source tables |
| Query/filter/cursor/limit/time/window | invalid filter, unsupported filter, invalid cursor, invalid limit, invalid time, missing/unbounded window and over-large window fail closed with 4xx |
| Cursor binding and stable ordering | cursor binds line, time range, implemented filters, limit, direction and ordering tuple; ordering uses `event_ts`, `accepted_at`, `fact_key` |
| NOK/detail evidence | NOK/detail DTO fields come only from accepted fact row fields and do not use diagnostic reason/raw mismatch/decoder error |
| No side effect | no write SQL, no write-side helper, no ACK/read_done mutation, no Collector/PLC/V-PLC/runtime/storage/Dashboard side effect |
| Dashboard contract reference | Dashboard component field matrix is read-only reference only; no Dashboard implementation in this gate |
| DB-backed opt-in | live DB rerun remains a separate future gate with explicit PM authorization; this planning gate does not authorize `EDGE_MES_ENABLE_DB_BACKED_TESTS=1` |

## 9. Future implementation allowlist proposal

Candidate exact allowlist for a later PM-authorized implementation gate:

- `api/app/routes/accepted_station_events.py` - route/query/cursor/DTO/error
  hardening for the existing accepted fact endpoint.
- `api/tests/test_accepted_station_events_api.py` - focused non-DB tests for DTO
  allowlist, forbidden leakage, filter/cursor/time/limit/window behavior,
  stable ordering and no-side-effect assertions.
- `api/tests/test_accepted_station_events_api_db_backed.py` - only if PM
  explicitly authorizes DB-backed harness/test updates; default execution must
  remain skipped unless a separate DB run gate authorizes opt-in.

Read-only or conditional candidates:

- `api/app/main.py` - read-only by default because the route is already
  registered; include only if route registration changes are proven necessary.
- `api/app/db.py` - not included by default. It requires separate PM
  authorization if future implementation proves connection-level timeout,
  read-only session defaults or DB error mapping cannot be implemented inside
  the route without duplicating unsafe connection behavior.

Explicitly excluded from the future API implementation allowlist unless PM opens
a separate gate:

- Dashboard/frontend files;
- Collector/runtime/storage.py;
- migration/schema files;
- config/mapping.yaml;
- Docker / docker compose files;
- optional debug/review diagnostics view;
- deploy/tag/rollback or PLC/V-PLC pilot files.

## 10. Review sequence

Required sequence before any implementation:

1. Reliability focused planning review.
2. Data Quality focused planning review.
3. Verification focused planning review / exact future implementation allowlist
   audit.
4. PM explicit authorization before implementation.

Required sequence after implementation:

1. Reliability focused implementation review.
2. Data Quality focused implementation review.
3. Verification focused implementation review / exact allowlist audit.
4. PM explicit authorization for exact-path stage/commit/push.

## 11. Recommendations

- Keep the next implementation slice narrow: route hardening plus focused API
  tests only, with DB-backed harness edits separated unless PM explicitly
  authorizes them.
- Freeze HTTP error envelope and DB unavailable / missing table / missing schema
  / missing authority behavior before implementation coding.
- Treat accepted-fact filter expansion as an explicit implementation decision:
  either implement a named subset and bind it into cursor scope, or reject
  unsupported filters with 4xx.
- Keep optional debug/review diagnostics view deferred to a separate Level 2
  gate with diagnostic/audit/review namespaces and leakage-negative review.
