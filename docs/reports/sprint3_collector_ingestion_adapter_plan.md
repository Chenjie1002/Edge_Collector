# Sprint 3 Collector Ingestion Adapter Plan

Date: 2026-06-28

Status: Sprint 3 Collector Ingestion Adapter planning/status reference. Sprint
3 Slice J downstream Collector adapter decision / diagnostic / projection
boundary tests-only hardening is CLOSED / PASS WITH RECOMMENDATIONS at
`ed9a61e`. Sprint 3 accepted production-fact visibility boundary
docs/contracts freeze is recorded as a planning boundary only. Sprint 3
raw_policy station-level rollout checkpoint remains CLOSED / PASS WITH
RECOMMENDATIONS after Slice I. E1 runtime raw decoder repair remains historical
implementation history at `2c73410`.
DB/API/Dashboard/V-PLC/PLC pilot/deploy/tag/rollback remain not authorized.

Current PM intake live baseline for accepted production-fact visibility
boundary docs/contracts freeze:

- Branch: `main`.
- HEAD / `origin/main`: `9135011f0695893ca801e7e962c65c6da3b77e84`.
- Latest commit: `9135011 Add PM handoff after Slice J tests-only sync`.
- Sprint 3 Slice J downstream planning-only gate: CLOSED / PASS WITH
  RECOMMENDATIONS.
- Sprint 3 Slice J tests-only hardening: CLOSED / PASS WITH RECOMMENDATIONS.
- Sprint 3 raw_policy station-level rollout checkpoint: CLOSED / PASS WITH
  RECOMMENDATIONS.
- WS01 / WS02 / WS03 station-level `raw_policy`: `raw_capable`.
- Line-wide `runtime_defaults.raw_policy`: `raw_not_provided`.
- `raw_required`: not introduced.
- Runtime/source code, `storage.py`, DB/API/Dashboard/V-PLC/Docker/deploy and
  ACK/read_done ownership: unchanged.

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

### 4.8 Offline fixture inventory

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

Conclusion: `PASS WITH RECOMMENDATIONS` for Sprint 3 Slice J downstream adapter
boundary tests-only hardening docs/status reference sync.

Current control status: Sprint 3 Slice J downstream adapter decision /
diagnostic / projection boundary tests-only hardening is CLOSED / PASS WITH
RECOMMENDATIONS at `ed9a61e`. Accepted decisions remain the only path to
existing persist/ACK behavior. Non-accepted dispositions rejected / deferred /
quarantined / duplicate / conflict / raw_variant are covered under
`read_done=False` and `read_done=True` and must not persist, mutate
ACK/read_done status for the current non-accepted payload, project, write defect
detail or become production-visible facts.

Current PM intake live baseline:

```text
HEAD / origin/main:
ed9a61ef2bd8e6be12ad786fd7846f2efcfb0cad
Latest commit:
ed9a61e Harden Sprint 3 Slice J adapter boundary tests
```

Historical authoring baselines in this document, including the E1
`2c73410281d1465db166b66ddc23e27d9337b90a` marker, remain audit markers only.
They must not be read as the current live baseline after later Slice F1/F2/G/H/I
and Slice J commits.

Reliability Review: `PASS WITH RECOMMENDATIONS`, no blocker.

Data Quality focused implementation review: `PASS WITH RECOMMENDATIONS`, no blocker.

Verification focused implementation review / exact allowlist audit: `PASS WITH RECOMMENDATIONS`, no blocker.

Eligible for docs-only closeout decision: closed by this status sync.

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

Eligible for next PM planning gate: yes, after this docs/status sync. Next
eligible action is PM handoff readiness or a separately authorized downstream
planning gate, not immediate DB/API/Dashboard/V-PLC/deploy/runtime expansion.

Eligible for implementation without PM approval: no. PM approval is required
before DB/API/Dashboard/V-PLC/PLC pilot/storage.py/ACK/deploy, commit/push,
tag, rollback or any change outside the approved docs allowlist.
