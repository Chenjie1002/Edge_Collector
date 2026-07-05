# DB/API/Dashboard consumer planning gate

Date: 2026-07-04
Thread: Architecture / Integration
Status: PASS WITH RECOMMENDATIONS

This planning gate freezes how downstream API and Dashboard consumers may read
accepted production facts. It does not authorize API implementation, Dashboard
or frontend implementation, new migration, Collector/runtime/storage change,
DB-backed test execution, Docker / docker compose action, deploy, tag, rollback,
staging, commit or push.

## 1. Source of truth boundary

The only production fact source for DB/API/Dashboard consumers is:

- `production_accepted_station_event_fact`

This source represents accepted station-event business facts after immutable
config authority, `raw_policy` / decoder authority, shared validation,
duplicate/conflict checks and adapter decision `accepted`.

The following tables or surfaces must not be described or used as equivalent
production fact sources, fallback sources, legacy compatibility sources or
join-derived field fillers:

- `raw_plc_sample`
- `cycle_event`
- `station_event`
- `production_unit`
- `quality_event`
- `production_snapshot`
- `production_events`

Consumer-facing production fields must come from
`production_accepted_station_event_fact` row fields only. Legacy/current tables
may remain useful for historical implementation internals or diagnostics, but
they are not consumer production fact authority.

## 2. Consumer data boundary

Dashboard/API consumers may consume only accepted station-event business facts
for OEE, traceability, station result, accepted result trend and production
status surfaces.

Allowed production fact semantics:

- line, PLC, station, station type, profile and config lineage;
- event type and accepted production result;
- unit / DMC identity where present on the accepted fact row;
- cycle counter, source event identity, source event time and accepted time;
- fact key and content fingerprint as immutable identity/reference fields;
- NOK/detail fields only when already present on accepted fact rows and bound
  to accepted upstream business evidence.

Diagnostic-only or review-only semantics:

- `raw_payload` and `raw_hex`;
- decoded payload and source normalized payload before accepted decision;
- adapter disposition, reason code and phase;
- candidate context;
- raw/normalized comparison context;
- decoder errors;
- diagnostic, review or audit payload references.

`raw_payload` / `raw_hex` is evidence, not a production fact. Diagnostic or raw
material must not enter OEE, traceability main views, Quality/Pareto production
metrics, Dashboard state or accepted production-result displays.

Non-accepted dispositions do not write defect detail. NOK/detail visibility must
bind to accepted upstream business evidence and shared station-event validation.
The side-effect boundary remains unchanged: no ACK/read_done mutation for the
current non-accepted payload.

## 3. API consumer contract planning

The consumer-facing API source boundary is the accepted fact read path:

- `GET /api/v2/production/accepted-station-events`

Allowed response fields for consumer planning:

| Field | Source | Consumer meaning | Fallback |
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
| `unit_id` | `production_accepted_station_event_fact.unit_id` | unit trace key when present | forbidden |
| `dmc` | `production_accepted_station_event_fact.dmc` | DMC trace key when present | forbidden |
| `cycle_counter` | `production_accepted_station_event_fact.cycle_counter` | source cycle counter | forbidden |
| `source_event_id` | `production_accepted_station_event_fact.source_event_id` | stable source event identity | forbidden |
| `event_ts` | `production_accepted_station_event_fact.event_ts` | source event time | forbidden |
| `accepted_at` | `production_accepted_station_event_fact.accepted_at` | accepted fact timestamp, not ACK time or freshness by itself | forbidden |
| `fact_key` | `production_accepted_station_event_fact.fact_key` | immutable production fact identity/reference | forbidden |
| `content_fingerprint` | `production_accepted_station_event_fact.content_fingerprint` | immutable content identity/reference | forbidden |
| `nok_code` | `production_accepted_station_event_fact.nok_code` | accepted NOK code only | forbidden |
| `nok_origin` | `production_accepted_station_event_fact.nok_origin` | accepted NOK origin only | forbidden |
| `nok_detail_code` | `production_accepted_station_event_fact.nok_detail_code` | accepted detail code only | forbidden |
| `nok_detail_source_event_id` | `production_accepted_station_event_fact.nok_detail_source_event_id` | detail source evidence identity | forbidden |
| `nok_detail_evidence_fact_key` | `production_accepted_station_event_fact.nok_detail_evidence_fact_key` | accepted upstream evidence fact reference | forbidden |

Query / read boundary:

- required scope: `line_id`, or an explicit server-injected single-line default;
- time range: bounded `start_time` / `end_time`, strict timezone-aware ISO-8601,
  max 31 days unless a later contract changes the limit;
- pagination: `limit` default 50, max 500, fail-closed for invalid values;
- cursor: tamper-resistant, schema/version checked, bound to line, time range,
  limit, direction and ordering tuple;
- sorting: stable order by `event_ts ASC`, `accepted_at ASC`, `fact_key ASC`;
- eligible future filters: `station_id`, `station_type`, `event_type`,
  `production_result`, `config_hash`, `unit_id`, `dmc`, `cycle_counter` and
  NOK/detail fields, only when sourced from the accepted fact table;
- excluded until later schema/contract gate: `work_order`, `product`, raw
  evidence filters, diagnostic reason filters, candidate-state filters and
  legacy table fields.

API consumers must not bypass the accepted fact source. They must not join
diagnostic/raw/candidate tables to fill production fields, and must not read
from diagnostic or raw surfaces to synthesize production result, NOK/detail,
Quality/Pareto or Dashboard facts.

This planning gate does not authorize API implementation or API contract edits.

## 4. Dashboard consumer planning

Dashboard pages and components must consume accepted fact API fields only unless
a future debug/review gate explicitly authorizes a separate diagnostic surface.

| Page / component | Allowed data | Explicit boundary |
| --- | --- | --- |
| Line overview | aggregated `event_type`, `production_result`, `event_ts`, `accepted_at`, station fields and counts from accepted facts | no raw/diagnostic/candidate fields; OEE must show incomplete/unknown rather than fabricate missing schedule/runtime denominators |
| Station status | `station_id`, `station_type`, latest accepted `event_ts`, latest accepted `production_result`, `config_hash`, `profile_id` | `accepted_at` is accepted fact timestamp, not collector freshness or ACK status |
| Accepted result trend | accepted `station_result` rows grouped by bounded time bucket, station/profile/config scope and `production_result` | no fallback to `quality_event`, `production_snapshot` or legacy summaries |
| NOK/detail visibility | accepted NOK/detail fields and `nok_detail_evidence_fact_key` only | no detail from adapter reason code, raw mismatch, decoder error or non-accepted disposition |
| Traceability drilldown | `unit_id`, `dmc`, `cycle_counter`, `source_event_id`, `fact_key`, `content_fingerprint`, event timeline fields from accepted facts | no raw bytes, candidate payload, diagnostic context or legacy event filler in main trace |

Debug/review-only or deferred surfaces:

- raw payload / raw hex viewer;
- decoder error view;
- raw/normalized diff view;
- candidate quarantine review;
- adapter disposition/reason explorer;
- audit evidence references;
- work order / product fields;
- Quality/Pareto completeness dashboards beyond accepted fact fields.

If a later debug/review page is authorized, it must be separate from production
Dashboard surfaces, use diagnostic/audit/review namespaces, and include
negative assertions that diagnostic material cannot become production facts,
OEE/traceability main facts, NOK/detail authority or ACK/read_done authority.

This planning gate does not authorize Dashboard/frontend implementation.

## 5. Forbidden data and fallbacks

Forbidden for API and Dashboard production consumers:

- raw payload, raw hex, raw sample id or raw bytes;
- decoded/source normalized candidate payloads before accepted decision;
- adapter disposition, reason code, phase or candidate context;
- raw/normalized comparison context;
- decoder errors;
- `quality_pareto_input`;
- `dashboard_state`;
- `ack_status`, `read_done` or Collector state;
- ambiguous production-looking keys such as bare `result`, `defect`, `quality`
  or `pareto`;
- any legacy/current table join that fills missing accepted fact fields;
- any synthetic field that makes non-accepted dispositions visible as
  production facts.

## 6. Proposed implementation slices

| Slice | Owner | Risk tier | Scope | Required review |
| --- | --- | --- | --- | --- |
| API consumer contract freeze | Architecture / Integration | Level 2 | docs/contracts planning for exact consumer fields, filter/sort contract, forbidden fallbacks and Dashboard component field map | Reliability, Data Quality, Verification |
| API read/query implementation | Architecture / Integration | Level 2 | API route/query changes only after exact allowlist; source remains `production_accepted_station_event_fact` | Reliability, Data Quality, Verification before commit |
| API tests | Verification with Architecture support | Level 2 | DTO allowlist, source isolation, forbidden surface, pagination/filter/sort, NOK/detail evidence and no side-effect tests; DB-backed opt-in only if separately approved | Reliability for read-only/timeout, Data Quality for field authority, Verification for matrix/allowlist |
| Dashboard read-only skeleton | Architecture / Integration | Level 2 | frontend shell that consumes only accepted fact API DTOs; no raw/debug data | Reliability, Data Quality, Verification |
| Dashboard visualization slice | Architecture / Integration | Level 2 | line overview, station status, accepted result trend, NOK/detail visibility and traceability drilldown from allowed fields | Reliability, Data Quality, Verification |
| Optional debug/review diagnostics view | Architecture / Integration with Data Quality lead | Level 2 | separate diagnostic/audit/review namespace surface, no OEE/traceability main facts | Reliability, Data Quality, Verification; especially leakage-negative review |

These slices remain Level 2 because they affect production fact visibility,
consumer semantics, API/Dashboard boundaries and diagnostic leakage risk. They
must not be downgraded because the expected code diff looks small.

## 7. Required review sequence

Recommended sequence before any implementation:

1. Architecture / Integration: API consumer contract freeze.
2. Reliability: read-only transaction, timeout, bounded query, no ACK/read_done,
   no Collector/PLC/runtime side-effect review.
3. Data Quality: accepted fact field authority, NOK/detail evidence binding,
   forbidden fallback and diagnostic/raw leakage review.
4. Verification: exact allowlist audit, DTO/filter/cursor/sort matrix,
   forbidden surface matrix and gate-to-implementation readiness review.
5. PM exact authorization before implementation.

After implementation, repeat Reliability, Data Quality and Verification focused
reviews before any exact-path staging/commit/push gate.

## 8. Carry-forward / excluded surfaces

Separate future PM-authorized work:

- actual timeout failure induction;
- worker/runtime DB-backed gates for unique-violation race;
- commit-before-ACK;
- non-accepted DB-backed zero-row / no ACK/read_done mutation;
- post-conflict re-read semantics;
- DB rollback proof;
- future DB-backed reruns with `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`;
- Docker / docker compose lifecycle action;
- V-PLC/PLC pilot;
- deploy, tag or rollback.

Explicitly not authorized by this gate:

- API implementation;
- Dashboard/frontend implementation;
- new migration;
- Collector/runtime/storage change;
- DB opt-in execution or DB connection;
- creating or dropping test DBs;
- broad tests;
- staging, commit or push.

## 9. Recommendations

- Before Dashboard implementation, create a separate contract freeze that maps
  each page/component to exact accepted fact fields and error/empty states.
- Keep `work_order` and `product` excluded until a later schema/contract gate
  creates accepted fact authority for those fields.
- Refresh any stale status wording in existing contract docs only in a future
  docs/status gate; this planning file does not edit those docs.
- Require leakage-negative tests for every future Dashboard/API consumer slice
  that touches result, NOK/detail, traceability or debug/review visibility.
