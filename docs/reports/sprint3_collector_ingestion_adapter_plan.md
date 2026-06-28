# Sprint 3 Collector Ingestion Adapter Plan

Date: 2026-06-28

Status: Sprint 3 Collector Ingestion Adapter planning/status reference. E1
runtime raw decoder repair is implemented, reviewed, committed and pushed at
`2c73410`.
DB/API/Dashboard/V-PLC/PLC pilot/deploy/tag/rollback remain not authorized.

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

### 4.4 Raw / normalized authority matrix

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

### 4.6 Offline fixture inventory

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

Conclusion: `PASS WITH RECOMMENDATIONS` for E1 docs/status sync preparation.
E1 review status has been synchronized after implementation, focused reviews
and exact allowlist commit/push at `2c73410`.

Reliability Review: `PASS WITH RECOMMENDATIONS`, no blocker.

Data Quality focused implementation review: `PASS WITH RECOMMENDATIONS`, no blocker.

Verification focused implementation review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

Eligible for docs-only closeout decision: yes.

D2-A decoder authority docs/contract-only repair: recorded. D2-A adds no code,
tests, config, schema, mapping, runtime Collector integration or raw runtime
wiring. D2-B fixture/test-only hardening is recorded at `dafbbf8`. D2-C minimal
registry/schema implementation is recorded at `5e5a617`. D3 runtime raw wiring
is recorded at `c9e7c22`. E1 runtime raw decoder repair is recorded at
`2c73410` / `2c73410281d1465db166b66ddc23e27d9337b90a`.

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
Future raw_policy change from raw_not_provided to raw_capable/raw_required requires a separate Level 2 mapping/config authority gate.
Current eligible next step is PM handoff readiness or next slice planning, not immediate DB/API/Dashboard/V-PLC/deploy.
```

Eligible for next PM planning gate: yes.

Eligible for implementation without PM approval: no. PM approval is required
before DB/API/Dashboard/V-PLC/PLC pilot/storage.py/ACK/deploy, commit/push,
tag, rollback or any change outside the approved docs allowlist.
