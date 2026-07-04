# Sprint 3 Collector Ingestion Adapter Plan

Date: 2026-06-28

Status: Sprint 3 Collector Ingestion Adapter planning/status reference. DB/API/
Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning
HOLD Repair post-push docs/status sync is CLOSED / PASS as a local docs/status-only
sync and is not committed/pushed by this gate. The HOLD repair is committed and
pushed at `2cfad5d` after Verification B1 was closed by re-review. The latest
PM handoff after API DB-backed schema verification is committed/pushed at
`99dfc26`. DB/API/Dashboard DB-backed/live Postgres API Read Validation
tests-only implementation remains CLOSED / PASS WITH RECOMMENDATIONS and
committed/pushed at `b30db5c`; the prior DB-backed API read validation
post-push docs/status sync is committed/pushed at `64d0e12`. DB/API/Dashboard
API read path implementation remains CLOSED / PASS WITH RECOMMENDATIONS and
committed/pushed at `763b248`. DB/API/Dashboard API read path contract freeze is
CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at `2d0918a`.
DB/API/Dashboard guarded DB-backed accepted fact tests are CLOSED / PASS WITH
RECOMMENDATIONS and committed/pushed at `636ba37` after Reliability, Data Quality
and Verification reviews, including a Reliability HOLD repair and re-review.
DB/API/Dashboard Slice 2 DB write path implementation is CLOSED / PASS WITH
RECOMMENDATIONS and committed/pushed at `299d28a`. Sprint 3 Slice J downstream
Collector adapter decision / diagnostic / projection boundary tests-only
hardening is CLOSED / PASS WITH RECOMMENDATIONS at `ed9a61e`. Sprint 3 accepted
production-fact visibility boundary docs/contracts freeze is CLOSED / PASS WITH
RECOMMENDATIONS and committed in the production-fact visibility boundary
closeout at `11cf077`. Tests-only adapter production-fact leakage negative
implementation is CLOSED / PASS WITH RECOMMENDATIONS and committed at `fd3a799`.
Sprint 3 raw_policy station-level rollout checkpoint remains CLOSED / PASS WITH
RECOMMENDATIONS after Slice I. E1 runtime raw decoder repair remains historical
implementation history at `2c73410`. Dashboard implementation, new migration,
V-PLC/PLC pilot/deploy/tag/rollback, DB opt-in local Postgres execution, Docker /
docker compose, live DB validation, actual timeout failure proof and broad tests
remain not authorized.

Current PM intake live baseline for DB-backed API read validation HOLD repair post-push docs/status sync:

- Branch: `main`.
- HEAD / `origin/main`: `99dfc265983d757de7c23f6a677cabbc05bc4f5a`.
- Latest commit: `99dfc26 Add PM handoff after API DB-backed schema verification`.
- Sprint 3 Slice J downstream planning-only gate: CLOSED / PASS WITH
  RECOMMENDATIONS.
- Sprint 3 Slice J tests-only hardening: CLOSED / PASS WITH RECOMMENDATIONS.
- Sprint 3 accepted production-fact visibility boundary: CLOSED / PASS WITH
  RECOMMENDATIONS; exact docs/status/PM-rule commit/push completed at `11cf077`.
- DB/API/Dashboard production visibility planning gate: CLOSED / PASS WITH
  RECOMMENDATIONS.
- Production-fact leakage negative tests planning gate: CLOSED / PASS WITH
  RECOMMENDATIONS.
- Tests-only adapter production-fact leakage negative implementation: CLOSED /
  PASS WITH RECOMMENDATIONS; committed at `fd3a799`.
- DB/API/Dashboard Slice 1 schema-only migration: CLOSED / PASS WITH
  RECOMMENDATIONS; committed at `e75f652`.
- DB/API/Dashboard Slice 2 DB write path: CLOSED / PASS WITH RECOMMENDATIONS;
  committed/pushed at `299d28a`.
- DB/API/Dashboard guarded DB-backed accepted fact tests: CLOSED / PASS WITH
  RECOMMENDATIONS; committed/pushed at `636ba37`.
- DB/API/Dashboard API read path planning gate: CLOSED / PASS TO REVIEW WITH
  RECOMMENDATIONS.
- DB/API/Dashboard API read path contract freeze: CLOSED / PASS WITH
  RECOMMENDATIONS; committed/pushed at `2d0918a`.
- DB/API/Dashboard API read path implementation: CLOSED / PASS WITH
  RECOMMENDATIONS; committed/pushed at `763b248`.
- DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only
  implementation: CLOSED / PASS WITH RECOMMENDATIONS; committed/pushed at
  `b30db5c`.
- DB/API/Dashboard DB-backed/live Postgres API Read Validation Reliability /
  Data Quality / Verification implementation reviews: CLOSED / PASS WITH
  RECOMMENDATIONS, no blocker.
- PM handoff after DB-backed API read validation tests: PASS; committed/pushed
  at `b817a9d`.
- DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push
  docs/status sync: PASS; committed/pushed at `64d0e12`.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning Gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning Reliability Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning Data Quality Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning Verification Review / Exact Future Run Allowlist Audit: CLOSED /
  HOLD, blocker B1.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning HOLD Repair: CLOSED / PASS, no blocker.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning HOLD Repair Verification Re-review: CLOSED / PASS WITH
  RECOMMENDATIONS, blocker B1 CLOSED.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning HOLD Repair exact-path commit/push: PASS; committed/pushed at
  `2cfad5d`.
- PM handoff after API DB-backed schema verification: PASS; committed/pushed at
  `99dfc26`.
- DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation
  Run Planning HOLD Repair post-push docs/status sync: PASS as local
  docs/status-only sync; not committed/pushed by this gate.
- DB/API/Dashboard Slice 2 exact commit gate: PASS.
- DB/API/Dashboard Slice 2 exact push gate: PASS.
- Guarded DB-backed accepted fact tests exact commit/push gate: PASS.
- WS01 / WS02 / WS03 station-level `raw_policy`: `raw_capable`.
- Line-wide `runtime_defaults.raw_policy`: `raw_not_provided`.
- `raw_required`: not introduced.
- `api/tests/test_accepted_station_events_api_db_backed.py` now includes
  API-side pre-insert schema/constraint/column/nullability verification for the
  future DB-backed API run path.
- Schema verification runs after migration apply and before fixture insert.
- DB opt-in local Postgres execution, `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`, live
  DB validation, actual timeout failure proof, new DB migration, Dashboard,
  V-PLC, config, Docker / docker compose, deploy, tag, rollback and real PLC
  pilot: not authorized by this docs/status sync closeout.

The E1 authoring baseline below is retained as a historical audit marker. It is
not the live repository baseline for this post-Slice I status sync.

Live baseline at E1 docs/status sync authoring time:

- Branch: `main`.
- HEAD / `origin/main`: `2c73410281d1465db166b66ddc23e27d9337b90a`.
- Latest commit: `2c73410 Repair Sprint 3 Slice E1 runtime raw decoder`.
- Sprint 2 implementation commit: `17cf5d2 Implement Sprint 2 generic station event model`.
- Sprint 2 docs-only closeout commit: `82b2127 Close out Sprint 2 documentation state`.
- Phase-1 tag: `phase1-pass-20260619`.
- Phase-2 tag: not created.
- Runtime integration: not started.
- Deploy / rollback drill: not performed.

## 1. Purpose

This plan freezes the first Sprint 3 Collector ingestion adapter slice as an
offline fixture contract. It prepares Reliability, Data Quality and Verification
review without authorizing code or tests.

The companion contract is:

- `docs/contracts/collector_ingestion_adapter.md`

## 2. Scope and non-goals

In scope:

- define the offline ingestion adapter boundary;
- define resolved config snapshot lookup by immutable `config_hash`;
- define source payload, normalized envelope, raw evidence, validation,
  fingerprint, lifecycle and projection-metadata boundaries;
- define reject/defer/quarantine-style diagnostic wrapper semantics;
- propose future file ownership and required future test groups.

Non-goals:

- no runtime Collector connection;
- no DB write;
- no migration;
- no FastAPI endpoint;
- no Dashboard or Trace UI;
- no V-PLC behavior changes;
- no real PLC pilot;
- no deploy, tag or rollback;
- no commit/push in this drafting thread.

## 3. First implementation slice definition

Slice name: `Collector ingestion adapter offline fixtures`.

Inputs:

- frozen resolved config snapshot;
- PLC/V-PLC source payload fixture;
- mapping/template/profile/station snapshot;
- optional raw payload;
- state index fixture.

Outputs:

- normalized `station_event` envelope;
- canonical bytes / fingerprints;
- validation decision;
- lifecycle output;
- projection metadata;
- reject/defer/quarantine-style decision wrapper.

This slice produces no DB row and no API-visible production outcome.

## 4. Contract decisions

### 4.1 Collector ingestion adapter contract

The adapter maps source fixture data into a candidate `station_event` envelope,
then delegates station-event semantics to `common.station_event`.

Key decisions:

- source payload boundary is fixture input plus source context;
- normalized envelope boundary is the candidate passed to shared validators;
- field authority is split between source facts, resolved config snapshots and
  adapter metadata;
- `event_ts` is source event time;
- `observed_at` is Collector first-observed UTC time;
- `created_at` is future DB time and is not present in current envelope;
- future runtime clock skew, missing source timestamp, monotonicity and
  watermark policy are not implemented; current offline fixtures must not infer
  `late`, `observed_at` must not override `event_ts`, and `created_at` remains
  future DB time outside the envelope;
- `plc_boot_id`, `profile_id`, `station_type` and `config_hash` must preserve
  historical lineage;
- `source_event_id` must come from PLC/V-PLC/source fixture stable sequence or
  source-provided stable identity, not random values, receive time, retry time,
  Collector wrapper IDs or transport retry IDs;
- adapter must call shared validation helpers and must not duplicate
  station-event rules;
- adapter must use shared canonical serializer/fingerprint helpers and never use
  language-default JSON for identity;
- projection output is metadata only in this slice, with no persistence and no
  API-visible production outcome.
- Sprint 3 adapter does not modify Phase-1 ACK, `read_done` or write-back
  semantics; adapter retry/wrapper logic is not an ACK owner, and this offline
  slice does not change boot/profile/counter/ACK behavior.

### 4.2 Resolved config snapshot contract

Lookup input: `config_hash` from incoming envelope/source context.

Required snapshot contents:

- line;
- PLC;
- station;
- station_type;
- station_enabled;
- mapping;
- payload template reference/version;
- raw_policy;
- decoder registry reference;
- decoder id / decoder version / callable decoder;
- NOK template;
- profile/cycle_profile;
- route/direct predecessor;
- config_version/hash.

Historical snapshot rule:

- events must be interpreted only by their own immutable `config_hash` snapshot;
- adapter must never fallback to latest/current runtime config.

Fail-closed cases:

- `CONFIG_NOT_FOUND`;
- `CONFIG_HASH_MISMATCH`;
- `EVENT_LINEAGE_INVALID`;
- `RAW_PARSE_ERROR`;
- `RAW_NORMALIZED_MISMATCH`;
- `RAW_CONTENT_FORBIDDEN`;
- `RAW_EVIDENCE_MISSING`.

### 4.3 D2-A decoder authority planning outcome

D2-A is a docs/contract-only authority repair. It freezes contract language for
decoder registry authority, decoder id / decoder version / callable decoder
authority, immutable resolved config snapshot binding, fail-closed decoder
taxonomy and the no-fallback rule. D2-A does not implement code, tests, schema,
config, mapping, runtime Collector integration or raw runtime wiring.

D2 authority decisions now carried by the companion contract:

- decoder registry identity and registry snapshot/hash are selected only through
  the immutable resolved config snapshot for the event `config_hash`;
- decoder id, decoder version and callable decoder authority are selected only
  from that immutable snapshot and its referenced decoder registry snapshot;
- no fallback to latest/current runtime config, latest registry, current mapping
  file or environment defaults is allowed;
- unknown decoder id, missing decoder callable, decoder callable exception,
  decoder output mismatch and forbidden raw content fail closed;
- raw-only remains unsupported and fail-closed before identity, projection or
  fingerprint production;
- `raw_not_provided` is the only normalized-only authority; `raw_capable` and
  `raw_required` missing raw remain fail-closed unless PM later approves a
  contract change;
- raw evidence is evidence, not an independent production fact.

D2-B fixture/test-only hardening is implemented, reviewed, committed and pushed
at `dafbbf8`. It covers decoder authority negative cases and raw_policy
fixtures without production code changes.

D2-C minimal registry/schema implementation is implemented, reviewed, committed
and pushed at `5e5a617`.

D2-C committed files:

```text
collector/app/services/decoder_registry.py
collector/app/services/resolved_config_registry.py
tests/test_collector_station_event_adapter.py
```

D2-C validation evidence:

```text
PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_station_event_adapter.py -> 43 passed
PYTHONPATH=collector:. .venv/bin/python -m pytest collector/tests/test_event_collector_adapter_gate.py -> 22 passed
PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_station_event_runtime_source.py -> 35 passed
.venv/bin/python -m compileall collector/app/services -> PASS
git diff --check -> PASS
git diff --cached --check before commit -> PASS
```

D3 actual raw-capable/raw-required runtime wiring is implemented, reviewed,
committed and pushed at `c9e7c22`. D3 owns runtime raw evidence wiring, not the
D2-A contract repair, D2-B tests-only hardening or D2-C offline registry/schema
implementation.

D3 committed files:

```text
collector/app/plc/mapping.py
collector/app/services/event_collector.py
collector/app/services/resolved_config_registry.py
collector/tests/test_event_collector_adapter_gate.py
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

D3 implementation summary:

```text
runtime station db_read(...) bytes are passed as raw_bytes into runtime source.
build_runtime_source_payload() generates raw_payload={"raw_hex": ...}.
raw_payload enters adapt_source_payload().
raw evidence remains evidence, not production fact.
decoder output remains normalized candidate only.
accepted adapter decision remains required before persist/ACK.
config/mapping.yaml now carries decoder_version and decoder_registry snapshot id/content hash.
mapping.py parses, validates and hash-covers authority fields.
resolved_config_registry.py builds immutable decoder registry snapshot binding from runtime mapping.
No env/default/latest/ad hoc fallback is intended.
DB/API/Dashboard-visible behavior unchanged.
storage.py not touched.
V-PLC behavior unchanged.
Docker/deploy/tag/rollback not authorized.
ACK/read_done ownership unchanged.
```

E1 runtime raw decoder repair is implemented, reviewed, committed and pushed at
`2c73410`. E1 is a narrow repair after Slice E HOLD. It changes the runtime raw
decoder payload materialization so `decode_read_plan(...)` receives
`bytearray.fromhex(raw_hex)` as local mutable decode input, while canonical
`raw_hex` evidence remains unchanged. Nominal Snap7 raw path persists exactly
once and ACK/read_done side effect occurs exactly once. Malformed raw remains
`RAW_PARSE_ERROR` fail-closed, raw/normalized mismatch remains
`RAW_NORMALIZED_MISMATCH` fail-closed, non-accepted decisions still do not
persist/ACK, diagnostics remain diagnostics and raw evidence remains evidence,
not production fact.

E1 committed files:

```text
collector/app/services/resolved_config_registry.py
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_runtime_source.py
```

E1 preserves exclusions: `config/mapping.yaml`, `raw_policy`, `storage.py`,
DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy and ACK/read_done
ownership remain unchanged.

### 4.4 Slice F1 raw_policy authority docs/contracts edit

Slice F1 is a Level 2 authority planning/edit for docs/contracts only. It
freezes raw_policy authority semantics after D3 runtime raw wiring and E1
runtime raw decoder repair. F1 does not authorize runtime implementation, tests,
config/schema/mapping changes, `raw_policy` value changes, DB/API/Dashboard,
V-PLC, Docker/deploy, `storage.py`, ACK/read_done ownership, tag, rollback or
real PLC pilot work.

The key F1 planning decision is that runtime code-path capability is not the
same thing as a mapping/config authority upgrade. Current runtime code can carry
raw bytes because `event_collector.py` passes `raw_bytes=data` and
`station_event_runtime_source.py` can generate `raw_payload` / `raw_hex`.
However, the current mapping/config authority declaration remains the immutable
snapshot value from `config/mapping.yaml`, whose default is still
`raw_policy: raw_not_provided`. Runtime raw capability must not automatically
upgrade that declaration to `raw_capable` or `raw_required`.

F1 freezes these raw_policy definitions:

- `raw_not_provided`: normalized-only may enter shared validation only when the
  immutable resolved snapshot, mapping or payload template explicitly declares
  that the source does not produce raw. It is not a synonym for a missing
  runtime raw path.
- `raw_capable`: source/mapping authority declares that raw can be provided.
  Missing raw must fail closed as `RAW_EVIDENCE_MISSING` or a future
  PM-approved equivalent. It must not silently downgrade to `raw_not_provided`.
  Raw parse errors and raw/normalized mismatches remain fail-closed.
- `raw_required`: raw is required evidence. Missing raw must fail closed, with
  no projection, persist or ACK. It must not enter implementation until PM has
  explicitly accepted the production data-flow impact of missing raw at runtime.

raw_policy remains tied to mapping/config authority, decoder registry authority,
the immutable resolved snapshot, raw/normalized evidence comparison,
`RAW_PARSE_ERROR`, `RAW_NORMALIZED_MISMATCH`, `RAW_EVIDENCE_MISSING`,
accepted/rejected/diagnostic decisions, accepted-only persist/ACK side effects
and future DB/API/Dashboard visibility. Rejected or diagnostic decisions must
not project, persist, ACK or become visible production facts.

Minimum future gate for `raw_capable`:

- mapping/config immutable snapshot explicitly declares raw capability;
- decoder registry authority is complete;
- raw/normalized evidence gate is defined;
- negative cases cover missing raw, parse error, mismatch and no fallback;
- Reliability, Data Quality and Verification gates are explicit.

Minimum future gate for `raw_required`:

- PM separately authorizes the change;
- runtime missing-raw fail-closed impact on production data flow is explicit;
- Reliability, Data Quality and Verification gates are completed;
- exact implementation allowlist is frozen;
- the task does not default-touch `storage.py`, DB/API/Dashboard/V-PLC,
  Docker/deploy, ACK/read_done or unrelated runtime surfaces.

Future implementation candidate files remain candidates only. They do not
authorize edits without a later PM-approved implementation prompt with an exact
allowlist.

### 4.5 Raw / normalized authority matrix

The contract defines the matrix for:

- raw-only;
- normalized-only;
- raw + normalized match;
- raw + normalized conflict;
- unknown decoder id;
- decoder missing;
- decoder mismatch/exception;
- forbidden raw content;
- same content, different raw / raw_variant;
- future exact-byte fixture.

MVP decision: decoder missing with raw may be fail-closed rejected as
`RAW_PARSE_ERROR`. Future runtime may evolve this into deferred/quarantine
semantics, but current offline contract does not persist quarantine. Raw-only
cannot become production facts. Rejected, deferred or quarantined inputs never
project.

Raw-only must not produce a production fact, projection metadata, defect detail,
Quality/Pareto row, API-visible state or ACK. Normalized-only remains valid only
under immutable `raw_not_provided` authority. A source declared `raw_capable` or
`raw_required` with missing raw remains fail-closed unless PM later approves a
contract change.

Data Quality targeted repair for DQ-B1:

- `normalized-only` may enter shared validation only when immutable source
  protocol, mapping or payload template declares raw is not provided, for example
  `raw_not_provided` or an equivalent no-raw capability.
- The no-raw declaration must come from the immutable resolved snapshot, mapping
  or payload template, not from a temporary fixture field.
- If the source/mapping/template requires raw and raw is missing, the offline
  slice must fail closed as rejected. It must not be marked as a future deferred
  diagnostic in the current D2-A/D2-B/D2-C authority path unless PM later
  approves a contract change.
- Raw-required or raw-capable missing raw must not produce offline projection
  metadata, production outcome, defect detail, DB-visible state or API-visible
  state.
- Adapter logic must not use `normalized-only` to bypass raw evidence checks.
- Adapter logic must not synthesize `30003/system_reserved` upstream evidence;
  `30003` skip relation depends on accepted upstream business evidence validated
  by shared stateful validation. Rejected, non-authoritative or cross-config
  upstream evidence must not produce detail projection.

### 4.5 Reject / defer / quarantine contract

The contract defines accepted, rejected, deferred, quarantined, duplicate,
conflict and raw_variant diagnostic decisions.

Important constraints:

- quarantined in this slice means diagnostic decision semantics only;
- no quarantine persistence is implemented;
- DB write allowed in this stage: no for all decisions;
- API-visible production outcome: no for all decisions in this stage.

### 4.6 Slice J downstream adapter decision / diagnostic / projection boundary

Slice J name: `Sprint 3 Slice J -- Downstream Collector Adapter Decision /
Diagnostic / Projection Boundary`.

Objective: freeze the downstream boundary after station-level `raw_policy`
rollout so future implementation work cannot confuse adapter diagnostics,
candidate payloads or raw evidence with production facts. Slice J makes the
accepted adapter decision the only route into the existing persist/ACK path and
keeps all non-accepted dispositions out of persistence, ACK, projection, defect
detail and production visibility.

Proposed tier: Level 2 for any later implementation because the boundary
touches runtime safety, fact authority, ACK/read_done side-effect routing and
future DB/API/Dashboard visibility. This docs/contracts freeze itself is a
Level 1 docs/contracts planning edit with no runtime semantics change.

Future candidate implementation allowlist category: Collector adapter decision
gate, runtime source/adapter tests and diagnostic-only assertions. Candidate
runtime files and tests must remain a future PM-approved exact allowlist; this
section does not authorize edits. Future implementation must not default-include
`storage.py`, DB/API/Dashboard/frontend, V-PLC, Docker/deploy,
`config/mapping.yaml`, `raw_required` introduction, ACK/read_done ownership or
line-wide `raw_policy` changes.

Slice J boundary decisions:

- only `accepted` adapter decisions may reach the existing persist/ACK path;
- `rejected`, `deferred`, `quarantined`, `duplicate`, `conflict` and
  `raw_variant` decisions must not persist, ACK, project, write defect detail or
  become DB/API/Dashboard-visible production facts;
- diagnostic observability may record reason codes and candidate context for
  review, but remains non-owner of ACK/read_done and must not drive
  persistence;
- `raw_payload` / `raw_hex` is evidence only, not a production fact or defect
  detail authority;
- decoded or normalized payload remains a candidate until an accepted adapter
  decision exists;
- DB/API/Dashboard production visibility is deferred to a separate
  production-fact boundary planning gate.

Required review gates before later implementation:

- Architecture / Integration: confirm ownership, side-effect path and exact
  implementation allowlist.
- Reliability: confirm non-accepted decisions are fail-closed and cannot ACK or
  mutate read_done.
- Data Quality: confirm candidate/raw/diagnostic data cannot leak into
  production facts, defect detail, Quality/Pareto or Dashboard state.
- Verification: confirm accepted-only and non-accepted no-side-effect cases are
  testable with deterministic fixtures and runtime regression checks.
- PM authorization: explicitly authorize implementation, tests, exact staging,
  commit/push or any DB/API/Dashboard/V-PLC/deploy/tag/rollback expansion.

Explicit non-goals for Slice J docs freeze:

- no runtime/source code changes;
- no tests run and no test files changed;
- no `config/mapping.yaml` change;
- no `raw_required` introduction;
- no `storage.py` change;
- no DB/API/Dashboard/frontend/V-PLC/Docker/deploy change;
- no ACK/read_done ownership change;
- no real PLC pilot, tag, rollback, stage, commit or push.

Next eligible gate after docs freeze: Reliability focused review of the Slice J
docs/contracts boundary. Implementation remains ineligible until Architecture,
Reliability, Data Quality and Verification gates close and PM separately
authorizes an exact implementation allowlist.

Post-hardening note: the later Slice J tests-only hardening gate has since
closed at `ed9a61e` with Reliability, Data Quality and Verification focused
reviews all PASS WITH RECOMMENDATIONS and no blocker. This does not authorize
DB/API/Dashboard/V-PLC/deploy/runtime expansion.

### 4.7 Accepted production-fact visibility boundary freeze

Purpose: freeze future production-fact visibility rules before any
DB/API/Dashboard implementation. This is a docs/contracts planning boundary
only. It does not authorize schema, storage, API, Dashboard, Trace UI, V-PLC,
Collector runtime, `storage.py`, `config/mapping.yaml`, Docker/deploy,
ACK/read_done ownership, tests, staging, commit, push, tag, rollback or real PLC
pilot work.

Accepted production facts:

- future DB/API/Dashboard gates may consider only accepted station-event facts
  as production-visible facts;
- accepted requires immutable config authority, `raw_policy` / decoder
  authority, shared station-event validation, duplicate/conflict checks and an
  adapter decision of `accepted`;
- candidate future production-visible facts are limited to accepted
  station-event business facts under this contract's field authority, including
  line/PLC/station identity, station type, profile/config lineage, event
  type/result, legal NOK detail when bound to accepted upstream business
  evidence, unit/DMC, cycle counter, source event identity and source event
  time;
- raw evidence, diagnostic wrapper fields, rejected candidates and
  non-accepted dispositions are not production facts.

Diagnostic-only artifacts:

- adapter disposition, reason code, candidate context and raw/normalized
  comparison context remain diagnostic, review and debug material only;
- diagnostic artifacts must not become production facts, Quality/Pareto input,
  defect detail authority or ACK/read_done authority;
- diagnostic visibility must not drive persistence, projection, retry commit,
  Dashboard state or production side effects.

Raw evidence visibility:

- `raw_payload` / `raw_hex` is evidence, not a production fact;
- raw evidence may be proposed later as review-only or audit-only material, but
  it must not default into DB/API/Dashboard production visibility;
- raw evidence is not defect detail authority, Quality/Pareto input, Dashboard
  state or ACK/read_done authority.

Normalized candidate visibility:

- decoded raw output and source normalized payload are candidates until the
  adapter decision is accepted;
- non-accepted candidates are diagnostic-only and must not enter production
  facts, projection metadata, defect detail, Quality/Pareto input or Dashboard
  state;
- rejected, deferred, quarantined, duplicate, conflict and raw_variant payloads
  must not become production-visible facts.

Defect detail guard:

- non-accepted dispositions do not write defect detail;
- NOK/detail visibility must be bound to accepted upstream business evidence
  and shared station-event validation;
- rejected, deferred, quarantined, duplicate, conflict and raw_variant payloads
  must not generate defect detail, Quality/Pareto input or Dashboard defect
  state.

DB/API/Dashboard visibility deferral:

- this gate continues to defer DB/API/Dashboard implementation;
- the current freeze defines future visibility rules only and does not perform
  schema, DB write path, API, UI or runtime work;
- any future DB/API/Dashboard gate must restate exact allowlist, review gates
  and production-fact leakage negative tests before implementation.

ACK/read_done ownership:

- production-fact visibility planning does not change ACK/read_done ownership;
- visibility, diagnostic and review-only logic must not become ACK/read_done
  owner;
- the existing boundary remains: no ACK/read_done mutation for the current
  non-accepted payload.

Future hardening backlog:

- duplicate/conflict precedence;
- historical config replay;
- exact-byte canonical fixture vectors;
- raw error taxonomy;
- production-fact leakage negative tests.

### 4.8 DB schema field-name namespace contract freeze

Purpose: freeze field-name and namespace wording for future DB/API/Dashboard
schema/API/UI gates. This is a docs/contracts planning boundary only. It does
not authorize SQL, migration, storage, API, Dashboard, Trace UI, runtime
Collector, `storage.py`, tests, staging, commit, push, deploy, rollback, tag or
real PLC pilot work.

Production namespace:

- future production fact fields must use `production.*`;
- the frozen accepted station-event production names are
  `production.line_id`, `production.plc_id`, `production.station_id`,
  `production.station_type`, `production.profile_id`,
  `production.config_hash`, `production.config_version`,
  `production.event_type`, `production.production_result`,
  `production.unit_id`, `production.dmc`, `production.cycle_counter`,
  `production.source_event_id`, `production.event_ts`,
  `production.accepted_at`, `production.fact_key` and
  `production.content_fingerprint`;
- frozen NOK/detail production authority names are `production.nok_code`,
  `production.nok_origin`, `production.nok_detail_code`,
  `production.nok_detail_source_event_id` and
  `production.nok_detail_evidence_fact_key`;
- NOK/detail production visibility requires accepted upstream business evidence
  and shared station-event validation.

Diagnostics namespace:

- diagnostic, review and debug material must use isolated `diagnostics.*`
  names;
- frozen diagnostic names are `diagnostics.adapter_disposition`,
  `diagnostics.adapter_reason_code`, `diagnostics.adapter_phase`,
  `diagnostics.candidate_event_id`,
  `diagnostics.candidate_context_ref`,
  `diagnostics.raw_normalized_compare_status` and
  `diagnostics.decoder_error_code`;
- diagnostic payloads must not contain ambiguous production-looking keys:
  `result`, `defect`, `quality`, `pareto` or `dashboard_state`;
- `RAW_NORMALIZED_MISMATCH` may appear only as
  `diagnostics.adapter_reason_code = RAW_NORMALIZED_MISMATCH` or
  `diagnostics.raw_normalized_compare_status = mismatch`; it is forbidden from
  NOK/detail, defect origin, Quality/Pareto input and Dashboard defect state.

Audit and review namespaces:

- frozen audit names are `audit.raw_evidence_ref`,
  `audit.raw_evidence_fingerprint`, `audit.raw_hex_ref`,
  `audit.decoder_registry_snapshot_id` and
  `audit.decoder_registry_content_hash`;
- frozen review names are `review.candidate_payload_ref`,
  `review.raw_normalized_diff_ref` and `review.quarantine_ref`;
- `raw_payload` / `raw_hex` is only review-only or audit-only evidence
  reference/fingerprint material. It is not a production fact, not production
  fact table input and not KPI/OEE/Quality/Pareto/Grafana production query
  input.

Non-accepted disposition boundary:

- `rejected`, `deferred`, `quarantined`, `duplicate`, `conflict` and
  `raw_variant` may appear only as diagnostic/audit/review isolated material;
- non-accepted dispositions must not write production facts, NOK/detail rows,
  Quality/Pareto input, Dashboard state, Grafana production fields or
  ACK/read_done authority;
- preserve exact wording: no ACK/read_done mutation for the current
  non-accepted payload.

Future leakage assertions:

- future DB/API/Dashboard implementation gates must replace synthetic adapter
  leakage keys with real schema/API/UI assertions;
- future gates must assert diagnostic payloads do not contain `result`,
  `defect`, `quality`, `pareto` or `dashboard_state`;
- future gates must assert non-accepted dispositions have no production row, no
  NOK/detail row, no Quality/Pareto/Grafana production fields and no raw
  evidence in a production table;
- future gates must preserve exact wording: no ACK/read_done mutation for the
  current non-accepted payload.

### 4.9 Tests-only adapter production-fact leakage negative closeout

Tests-only adapter production-fact leakage negative implementation is
implemented, reviewed, committed and pushed at `fd3a799` /
`fd3a79901619c9afe664c709834b7e396187f8b2`.

Changed test files:

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
```

Implementation summary:

- strengthened runtime non-accepted adapter decision coverage so diagnostic
  context does not expose production projection, production outcome, defect
  detail, Quality/Pareto or Dashboard keys;
- added offline production-fact leakage summary assertions;
- added a negative matrix for `rejected`, `deferred`, `quarantined`,
  `duplicate`, `raw_variant` and `conflict`;
- added diagnostic reason-code coverage proving `RAW_NORMALIZED_MISMATCH` cannot
  become NOK/detail or Quality authority;
- preserved accepted positive control only to seed legal accepted state for
  duplicate/conflict/raw_variant checks.

Validation evidence:

```text
PYTHONPATH=collector:. .venv/bin/python -m pytest collector/tests/test_event_collector_adapter_gate.py -> 36 passed
PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_station_event_adapter.py -> 46 passed
Verification closeout: collector/tests/test_event_collector_adapter_gate.py -> 36 passed in 0.12s
Verification closeout: tests/test_collector_station_event_adapter.py -> 46 passed in 0.06s
git diff --check -> PASS
```

Review sequence closeout:

```text
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Verification exact allowlist audit / review-sequence closeout: PASS WITH RECOMMENDATIONS, no blocker
```

Boundary preserved:

- future production visibility is limited to accepted station-event business
  facts after immutable config authority, `raw_policy` / decoder authority,
  shared validation, duplicate/conflict checks and adapter decision `accepted`;
- adapter disposition, reason code, candidate context and raw/normalized
  comparison context remain diagnostic/review/debug only;
- `raw_payload` / `raw_hex` is evidence, not a production fact;
- decoded/source normalized payloads remain candidates until accepted;
- non-accepted dispositions do not write defect detail;
- NOK/detail visibility must bind to accepted upstream business evidence;
- ACK/read_done ownership is unchanged; preserve exact wording: no ACK/read_done
  mutation for the current non-accepted payload;
- DB/API/Dashboard remains not authorized by this tests-only gate.

Carry-forward recommendations:

- future DB/API/Dashboard implementation gates should replace current synthetic
  visibility-summary keys with real schema/API/UI field assertions once those
  surfaces are explicitly authorized;
- future DB/API/Dashboard gates must restate exact allowlist, review gates and
  production-fact leakage negative tests;
- this tests-only adapter coverage must not be treated as DB/API/Dashboard
  implementation authorization.

Next eligible gate: DB/API/Dashboard production visibility contract gate, or a
separately authorized hardening planning gate for duplicate/conflict precedence,
historical config replay, raw error taxonomy or exact-byte canonical fixture
vectors. No implementation is authorized automatically.

### 4.10 Offline fixture inventory

Required future fixture inventory:

- 3-station `cycle_start` / `cycle_complete` / `station_result OK`;
- `station_result NOK` + `station_nok` detail companion;
- heartbeat;
- disabled_station heartbeat-only as post-MVP/future fixture, without implying
  current runtime disabled-station behavior;
- unknown config hash;
- mapping mismatch;
- payload_template_mismatch;
- route_predecessor_mismatch;
- direct_predecessor_mismatch;
- profile mismatch;
- station_type mismatch;
- unknown decoder id;
- raw decoder missing;
- raw decoder mismatch;
- decoder output payload_template mismatch;
- forbidden raw content;
- normalized-only with source protocol/mapping declared no-raw;
- raw-required source with missing raw;
- raw-capable source missing raw;
- duplicate;
- conflict;
- raw_variant;
- historical resolved config snapshot;
- current config changed but historical event still uses old snapshot;
- multi-mapping station requiring exact `mapping_id`;
- future JCS exact-byte canonical JSON/fingerprint vectors.

## 5. Future ownership proposal

Proposal only, not authorized implementation.

Possible future code:

- `collector/app/services/station_event_adapter.py`
- `collector/app/services/resolved_config_registry.py`

Possible future tests:

- `tests/test_collector_station_event_adapter.py`
- dedicated adapter fixture JSON path;
- future cross-runtime canonical fixture tests.

Existing files read-only for first implementation:

- `common/station_event/*`
- `common/line_config/*`

Explicitly excluded:

- untracked PM handoff artifacts;
- DB migrations;
- FastAPI routes;
- Dashboard/frontend;
- V-PLC runtime;
- Docker/deploy files.

## 6. Required future tests

| Test group | Acceptance criteria |
| --- | --- |
| Adapter nominal tests | nominal 3-station/result/NOK/heartbeat fixtures normalize and validate through shared helpers |
| Lineage tests | config hash, mapping, profile, station type and route/predecessor mismatches fail closed |
| Raw authority tests | raw-only, normalized-only declared no-raw from immutable snapshot/mapping/template, raw-required missing raw, raw-capable missing raw, decoder missing, decoder exception, `RAW_PARSE_ERROR`, `RAW_NORMALIZED_MISMATCH`, `RAW_CONTENT_FORBIDDEN` and `RAW_EVIDENCE_MISSING` never produce facts and remain distinguishable |
| Decoder authority tests | decoder registry snapshot, decoder id, decoder version and callable decoder are immutable-snapshot-bound; unknown decoder id, missing callable, callable exception, decoded output mismatch, forbidden raw content and no-fallback-to-latest/current cases fail closed |
| Decision tests | accepted/rejected/deferred/quarantined/duplicate/conflict/raw_variant wrappers are deterministic and non-persistent |
| Projection tests | wrapper decision and `projection_for()` metadata are asserted together; only accepted envelopes produce offline projection metadata; non-accepted decisions never project or leak rejected detail into Pareto/defect rows |
| Phase-1 regression tests | current 3-station runtime behavior remains unchanged |
| Future JCS exact-byte boundary tests | canonical bytes and fingerprints match approved vectors before JavaScript/PostgreSQL/API/DB integration |
| Future duplicate/conflict precedence tests | multi-key duplicate/conflict precedence covers `event_id`, `fact_key`, cycle role / production result key and detail key, not only a single `fact_key` |
| Future historical config replay tests | historical config replay is covered, including current config changed but historical event still uses old snapshot |

## 7. Review gates

| Gate | Required review question |
| --- | --- |
| Architecture gate | Are boundaries, field authority, ownership and non-goals clear enough for review? |
| Reliability gate | Are runtime safety, config snapshot, decoder failure and future quarantine semantics acceptable? |
| Data Quality gate | Do raw/normalized authority and projection rules preserve production fact integrity? |
| Verification gate | Is the fixture matrix testable without runtime side effects? |
| PM authorization gate | Has PM explicitly authorized implementation, tests, commit/push or any runtime surface? |

## 8. Current control conclusion

Conclusion: `PASS` for DB/API/Dashboard explicit DB opt-in/live local
Postgres API Read Validation Run Planning HOLD Repair post-push docs/status
reference sync.

Current control status: DB/API/Dashboard explicit DB opt-in/live local Postgres
API Read Validation Run Planning HOLD Repair is CLOSED / PASS and
committed/pushed at `2cfad5d` after Verification B1 was closed by re-review.
The latest PM handoff after API DB-backed schema verification is committed/pushed
at `99dfc26`. DB/API/Dashboard DB-backed/live Postgres API Read Validation
tests-only implementation remains CLOSED / PASS WITH RECOMMENDATIONS and
committed/pushed at `b30db5c`; the prior post-push docs/status sync is committed
at `64d0e12`. The HOLD repair updated
`api/tests/test_accepted_station_events_api_db_backed.py` with API-side
pre-insert schema/constraint/column/nullability verification. The schema
verification runs after migration apply and before fixture insert in the future
DB-backed API run path. DB-backed API tests are still default skipped unless a
future PM-authorized DB opt-in run sets `EDGE_MES_ENABLE_DB_BACKED_TESTS=1`.
This docs/status sync does not claim DB opt-in execution, local Postgres
connection, live DB validation, actual timeout failure proof, Dashboard/UI,
migration, Collector runtime changes, Docker / docker compose execution,
deploy/tag/rollback or real PLC pilot work. The API read path source boundary
remains only `production_accepted_station_event_fact` while preserving the
production-fact visibility boundary. The prior API read path implementation
remains CLOSED / PASS WITH RECOMMENDATIONS at `763b248`; the prior guarded
DB-backed accepted fact tests remain CLOSED / PASS WITH RECOMMENDATIONS at
`636ba37`; and the prior Slice 2 DB write path remains CLOSED / PASS WITH
RECOMMENDATIONS at `299d28a`: accepted decisions may write the production fact
plus legacy/current persistence in one transaction, ACK/read_done mutation
happens only after successful transaction commit, and non-accepted dispositions
create zero production rows and no ACK/read_done mutation for the current
payload. Preserve exact wording: no ACK/read_done mutation for the current
non-accepted payload.

Current PM intake live baseline:

```text
HEAD / origin/main:
99dfc265983d757de7c23f6a677cabbc05bc4f5a
Latest commit:
99dfc26 Add PM handoff after API DB-backed schema verification
```

Historical authoring baselines in this document, including the E1
`2c73410281d1465db166b66ddc23e27d9337b90a` marker, remain audit markers only.
They must not be read as the current live baseline after later Slice F1/F2/G/H/I,
Slice J, production-fact visibility boundary, PM handoff, adapter leakage tests,
DB schema field-name contract, Slice 1 schema-only migration, Slice 2 DB write
path, guarded DB-backed accepted fact test commits, API read path contract freeze
commit `2d0918a`, API read path implementation commit `763b248`, DB-backed API
read validation tests commit `b30db5c`, handoff commit `b817a9d`, post-push
status sync commit `64d0e12`, API DB-backed schema verification HOLD repair
commit `2cfad5d`, or PM handoff commit `99dfc26`.

Architecture initial planning: `PASS WITH RECOMMENDATIONS`, no blocker.

Reliability first planning review: `HOLD`, later closed by Architecture planning repair.

Architecture planning repair: `PASS WITH RECOMMENDATIONS`, no blocker.

Reliability planning re-review: `PASS WITH RECOMMENDATIONS`, no blocker.

Data Quality planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

Verification planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

Architecture implementation + focused tests: `PASS WITH RECOMMENDATIONS`, no blocker.

Reliability focused implementation review: `PASS WITH RECOMMENDATIONS`, no blocker.

Data Quality focused implementation review: `PASS WITH RECOMMENDATIONS`, no blocker.

Verification focused implementation review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test planning gate: `PASS TO REVIEW WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Reliability planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Data Quality planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Verification planning review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test implementation: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Reliability implementation review: `HOLD`, later closed by Architecture HOLD repair and Reliability re-review.

Guarded DB-backed accepted fact test HOLD repair: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Reliability HOLD repair re-review: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Data Quality implementation review: `PASS WITH RECOMMENDATIONS`, no blocker.

Guarded DB-backed accepted fact test Verification implementation review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

Exact commit gate for guarded DB-backed accepted fact tests: `PASS`.

Exact push gate for guarded DB-backed accepted fact tests: `PASS`.

API read path planning gate: `PASS TO REVIEW WITH RECOMMENDATIONS`, no blocker.

API read path Reliability planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path Data Quality planning review: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path Verification planning review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path contract freeze docs-only edit: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path contract freeze Reliability review: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path contract freeze Data Quality review: `PASS WITH RECOMMENDATIONS`, no blocker.

API read path contract freeze Verification review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

Exact commit/push gate for API read path contract freeze: `PASS`, commit `2d0918a`.

Eligible for docs/status sync closeout decision: closed by this status sync.

D2-A decoder authority docs/contract-only repair: recorded. D2-A adds no code,
tests, config, schema, mapping, runtime Collector integration or raw runtime
wiring. D2-B fixture/test-only hardening is recorded at `dafbbf8`. D2-C minimal
registry/schema implementation is recorded at `5e5a617`. D3 runtime raw wiring
is recorded at `c9e7c22`. E1 runtime raw decoder repair is recorded at
`2c73410` / `2c73410281d1465db166b66ddc23e27d9337b90a`. F1 raw_policy
authority docs/contracts freeze is recorded at `ac1838c`. F2 WS01
station-level raw_policy raw_capable authority is recorded at `829d5c7`. Slice
G WS01 post-commit sanity tests-only hardening is recorded at `398f11c`. Slice H
WS02 station-level raw_policy raw_capable authority is recorded at `c7e80e8`.
Slice I WS03 station-level raw_policy raw_capable authority is recorded at
`045d21c`. Slice J downstream adapter boundary tests-only hardening is recorded
at `ed9a61e` / `ed9a61ef2bd8e6be12ad786fd7846f2efcfb0cad`.

D2-C carry-forward recommendations:

```text
D3 runtime raw wiring remained a separate PM-authorized gate after D2-C and is now closed at c9e7c22.
D2-C PASS alone did not prove runtime raw support; D3 c9e7c22 is the runtime raw wiring closure.
Keep rejected-decision normalized_event/canonical_bytes/fact_key diagnostic-only, not production fact or Quality/Pareto/API-visible state.
Registry failures currently surface as RAW_PARSE_ERROR rather than dedicated decoder-authority public codes; this is non-blocking unless PM opens a future taxonomy gate.
```

D3 carry-forward recommendations:

```text
current config/mapping.yaml runtime default still uses raw_policy: raw_not_provided; D3 runtime code path always passes raw_bytes=data, so this is not a blocker.
If PM later wants runtime source policy explicitly changed to raw_capable/raw_required, it needs a separate mapping/config authority change and review.
Next technical gate should not expand DB/API/Dashboard/V-PLC/storage.py/ACK/deploy without separate PM authorization.
```

E1 carry-forward recommendations:

```text
E1 is closed at 2c73410 as a narrow runtime raw decoder repair after Slice E HOLD.
E1 does not authorize config/mapping.yaml, raw_policy, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy or ACK/read_done ownership changes.
Historical F1/F2/G/H/I gates have since moved WS01, WS02 and WS03 station-level raw_policy to raw_capable while keeping line-wide runtime_defaults.raw_policy as raw_not_provided.
Future raw_required introduction or any line-wide raw_policy default change still requires a separate Level 2 mapping/config authority gate.
Current eligible next step is downstream PM planning, not immediate DB/API/Dashboard/V-PLC/deploy.
```

Slice J downstream planning-only gate: CLOSED / PASS WITH RECOMMENDATIONS.
Slice J tests-only hardening implementation: CLOSED / PASS WITH
RECOMMENDATIONS. Reliability, Data Quality and Verification focused reviews:
PASS WITH RECOMMENDATIONS, no blocker. Focused tests: 80 passed. No production
code changed.

Adapter production-fact leakage negative tests implementation: CLOSED / PASS
WITH RECOMMENDATIONS at `fd3a799`. Reliability, Data Quality and Verification
focused reviews: PASS WITH RECOMMENDATIONS, no blocker. Focused tests: 36 passed
for `collector/tests/test_event_collector_adapter_gate.py` and 46 passed for
`tests/test_collector_station_event_adapter.py`. No production code changed.

DB/API/Dashboard Slice 2 DB write path implementation summary:

```text
Added accepted station-event fact write path for production_accepted_station_event_fact.
Added accepted_station_event_fact.py DTO/helper.
Added Storage.transaction() and no-internal-commit write variants.
Accepted path writes production fact + legacy/current persistence in one transaction.
ACK/read_done mutation happens only after successful transaction commit.
Non-accepted dispositions create zero production rows and no ACK/read_done mutation for the current payload.
Duplicate/conflict/raw_variant/idempotency behavior implemented and tested with focused fake/spy coverage.
No DB migration/API/Dashboard/V-PLC/config/deploy/tag/rollback changes in this slice.
```

Slice 2 validation evidence:

```text
Architecture implementation: collector/tests/test_event_collector_adapter_gate.py -> 36 passed; tests/test_collector_station_event_adapter.py -> 46 passed; collector/tests/test_event_collector_accepted_fact_write_path.py -> 12 passed; compileall collector/app/services -> PASS; git diff --check -> PASS.
Reliability reran focused commands: 36 passed; 46 passed; 12 passed; compileall PASS; git diff --check PASS.
Data Quality combined focused tests: 94 passed.
Verification final audit: 94 passed; compileall PASS; git diff --check PASS; cached empty; exact allowlist PASS.
```

Production-fact visibility boundary preserved:

```text
Future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.
Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
raw_payload/raw_hex is evidence, not a production fact.
Decoded/source normalized payloads remain candidates until accepted.
Non-accepted dispositions do not write defect detail.
NOK/detail visibility must bind to accepted upstream business evidence.
Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
```

Guarded DB-backed accepted fact tests summary:

```text
Commit: 636ba37 / 636ba375248987b26d4ae68bdbf952d47f398bc8.
Changed files: pytest.ini, collector/tests/conftest.py, collector/tests/test_db_backed_safety.py, collector/tests/test_event_collector_accepted_fact_db_backed.py, collector/tests/test_event_collector_accepted_fact_write_path.py, collector/app/services/accepted_station_event_fact.py.
Registered db_backed and postgres_local markers.
DB-backed tests are skipped by default unless EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
Pure-unit safety coverage validates test-target DSN, maintenance/admin DSN, protected DB name rejection, safe DROP DATABASE statement generation, deterministic migration ordering and schema verification query presence without connecting to DB.
DB-backed direct-storage opt-in tests are pytest-discovered but skipped by default; default focused run produced 33 passed, 7 skipped.
station_result NOK missing accepted business NOK evidence now fails closed in build_accepted_station_event_fact() before DB insert.
No DB opt-in tests were run, no DB connection was made and docker compose was not started.
No storage.py, migration 007, API, Dashboard/frontend, V-PLC, config/mapping.yaml, docker-compose.yml, deploy/tag/rollback or docs/status/handoff files changed in the implementation commit.
```

Guarded DB-backed accepted fact carry-forward recommendations:

```text
Future PM-authorized local Postgres harness remains required before claiming worker-level DB-backed accepted rollback, commit failure before ACK, non-accepted DB-backed zero rows + no ACK/read_done mutation, race / unique-violation-after-precheck, or post-unique-violation re-read semantics coverage.
Future DB/API/Dashboard gates must use real production accepted fact table assertions, not synthetic visibility assumptions.
Do not treat legacy/current raw_plc_sample, cycle_event, station_event, production_unit or quality_event as equivalent to production accepted fact surface.
DB opt-in local Postgres execution, API/Dashboard implementation, new migration, V-PLC/PLC pilot, deploy, tag, rollback and broad tests remain not authorized until separate PM gate.
```

API read path contract freeze summary:

```text
Commit: 2d0918a / 2d0918adebe5cd29e59177bc2159c7f447cb5c38.
Changed file: docs/contracts/dashboard_api_contract.md.
Future endpoint contract: GET /api/v2/production/accepted-station-events.
This is a future API contract only and does not claim current implementation.
Source table is limited to production_accepted_station_event_fact; no legacy/current fallback or equivalent production fact source is allowed.
Response fields must come only from production_accepted_station_event_fact; raw/diagnostic/candidate/review/audit/ACK/read_done/collector/Dashboard/Quality/Pareto leakage is forbidden.
Query contract requires bounded start_time/end_time, line_id or explicit server default scope, limit max 500, strict cursor parsing and stable pagination order.
NOK/detail fields must bind accepted upstream business evidence.
Future implementation must preserve no ACK/read_done mutation and no Collector/PLC/runtime side effect.
```

API read path implementation summary:

```text
Commit: 763b248 / 763b248ca835f59096e73aa5e199a4bf903ac946.
Commit message: Implement accepted station events read API.
Changed files: api/app/main.py, api/app/routes/accepted_station_events.py, api/tests/test_accepted_station_events_api.py.
Endpoint implemented: GET /api/v2/production/accepted-station-events.
Source table remains limited to production_accepted_station_event_fact; no legacy/current fallback or equivalent production fact source is allowed.
Response fields come only from production_accepted_station_event_fact and remain limited to the frozen DTO allowlist.
Query validation requires line_id, bounded start_time/end_time, strict timezone-aware ISO parsing, default limit 50, max limit 500 and fail-closed invalid limit/time/window behavior.
Cursor is HMAC signed, schema/version checked and binds line_id, start_time, end_time, limit, direction and ordering tuple; stable order is event_ts ASC, accepted_at ASC, fact_key ASC.
Read safety uses BEGIN READ ONLY, statement_timeout, idle_in_transaction_session_timeout, SELECT-only query and no write-path helper reuse.
NOK/detail fields are returned only from accepted fact row fields and must bind accepted upstream business evidence.
Focused validation: PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py -> 27 passed; git diff --check PASS.
Reliability implementation review: PASS WITH RECOMMENDATIONS, no blocker.
Data Quality implementation review: PASS WITH RECOMMENDATIONS, no blocker.
Verification implementation review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker.
api/app/db.py was not changed.
DB opt-in/local Postgres execution, new migration, storage.py, collector changes, Dashboard/frontend/Grafana, V-PLC, Docker/deploy/tag/rollback and broad tests remain unauthorized.
```

API read path implementation carry-forward recommendations:

```text
Before production deploy, ACCEPTED_STATION_EVENTS_CURSOR_SECRET must be managed as a real deployment secret rather than relying on the development fallback.
Future DB-backed/live Postgres API read validation remains separate PM-authorized work; this implementation was validated with focused mocked/stubbed API tests only and does not claim live schema/runtime coverage.
work_order/product remain excluded until a later schema/contract gate.
```

DB-backed/live Postgres API Read Validation tests-only implementation and explicit DB opt-in/live local Postgres run planning HOLD repair summary:

```text
Implementation commit: b30db5c / b30db5cd2bd1d109d83c8da1a222d5ad37517448.
Implementation post-push docs/status sync commit: 64d0e12 / 64d0e12dc76898a2da3ce09c2c0e94dbbf33ac80.
HOLD repair commit: 2cfad5d / 2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e.
Latest PM handoff commit: 99dfc26 / 99dfc265983d757de7c23f6a677cabbc05bc4f5a.
Commit message for implementation: Add DB-backed API read validation tests.
Commit message for HOLD repair: Add API DB-backed schema verification.
Changed file: api/tests/test_accepted_station_events_api_db_backed.py.
The implementation added only api/tests/test_accepted_station_events_api_db_backed.py.
The HOLD repair added API-side pre-insert schema/constraint/column/nullability verification for production_accepted_station_event_fact.
The schema verification checks table existence, DTO/accepted fact columns, nullable / NOT NULL expectations, unique constraints and accepted-fact check constraints.
The schema verification runs after migration apply and before fixture insert in the future live DB-backed execution path.
DB-backed API tests are default skipped unless a future PM-authorized DB opt-in run sets EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
Default non-DB focused run before HOLD repair: PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py api/tests/test_accepted_station_events_api_db_backed.py -q -> 27 passed, 32 skipped.
HOLD repair focused GREEN run: 41 passed, 19 skipped.
Collector DB safety focused run after HOLD repair: 20 passed.
git diff --check -> PASS in implementation and HOLD repair gates.
Reliability implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Data Quality implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Verification implementation review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Explicit DB opt-in/live local Postgres API Read Validation Run Planning Gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Planning Reliability Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Planning Data Quality Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Planning Verification Review / Exact Future Run Allowlist Audit: CLOSED / HOLD, blocker B1.
HOLD repair: CLOSED / PASS, no blocker.
HOLD repair Verification re-review: CLOSED / PASS WITH RECOMMENDATIONS, B1 CLOSED.
EDGE_MES_ENABLE_DB_BACKED_TESTS=1 was not set.
No DB opt-in run was executed.
No local Postgres connection was made.
No temp DB create/drop was executed.
No migration was applied against live DB.
No fixture insert into live DB was executed.
Docker / docker compose was not started.
Live DB validation has not completed.
Actual timeout failure proof has not completed.
Do not claim live DB validation completed.
Do not claim actual timeout failure proof completed.
Current tests prove timeout statements / read behavior and future-run schema verification are covered by planned/default-skipped harness, not that a real timeout failure path was induced or that live DB validation has completed.
```

DB-backed/live Postgres API Read Validation carry-forward recommendations:

```text
Future actual DB opt-in / live local Postgres API read validation run remains separately PM-authorized work before executing EDGE_MES_ENABLE_DB_BACKED_TESTS=1, connecting to local Postgres, creating/dropping a temp DB, applying migrations against live DB, inserting fixtures into live DB or claiming live DB validation.
Future actual timeout failure induction remains a separate PM-authorized gate; timeout setting verification alone is not actual timeout failure proof.
Future Dashboard/API consumer planning gate remains separate and must not be folded into this docs/status sync.
Worker/runtime DB-backed gates for unique-violation race, commit-before-ACK, non-accepted DB-backed zero-row/no ACK/read_done mutation, post-conflict re-read semantics and DB rollback remain future authorized work.
API read path source boundary remains only production_accepted_station_event_fact; raw_plc_sample, cycle_event, station_event, production_unit, quality_event, production_snapshot and production_events must not be described as equivalent production fact sources, fallback sources or join-derived field fillers.
Future production visibility remains limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.
Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
raw_payload/raw_hex is evidence, not a production fact.
Decoded/source normalized payloads remain candidates until accepted.
Non-accepted dispositions do not write defect detail.
NOK/detail visibility must bind to accepted upstream business evidence.
Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
Deploy/tag/rollback/real PLC pilot require separate PM authorization.
```

Eligible for next PM planning gate: yes, after this docs/status sync. Recommended
next eligible action is a separately authorized actual DB opt-in / live local
Postgres API read validation run gate, or Dashboard/API consumer planning.
Actual timeout failure induction remains a separate future PM-authorized gate.

Eligible for implementation without PM approval: no. PM approval is required
before Dashboard implementation, DB opt-in/local Postgres execution,
EDGE_MES_ENABLE_DB_BACKED_TESTS=1, Docker / docker compose, tests beyond focused
default-skipped harness checks, new migration, V-PLC/PLC pilot, storage/API
expansion, deploy, tag, rollback, broad tests, real PLC pilot, commit/push or any
change outside the approved docs allowlist.
