# Collector Ingestion Adapter Contract

Status: Sprint 3 Collector ingestion adapter contract. Offline adapter,
runtime adapter gate, diagnostics, raw boundary tests and D2-C offline decoder
registry authority are implemented/reviewed/committed. Runtime raw wiring, DB
writes, API endpoints, Dashboard, V-PLC behavior changes, PLC pilot, deploy,
tag and rollback are not authorized.

Updated: 2026-06-27

Applies to: Phase-2 Sprint 3 Collector ingestion adapter offline fixtures.

## 1. Scope and non-goals

This contract defines the offline ingestion adapter boundary between a
PLC/V-PLC source payload fixture and the already implemented
`common.station_event` package.

In scope for this draft:

- Offline source payload fixture interpretation.
- Immutable resolved config snapshot lookup by `config_hash`.
- Normalized `station_event` envelope construction.
- Adapter-owned diagnostic decision wrapper for accepted, rejected, deferred,
  quarantined, duplicate, conflict and raw_variant outcomes.
- Canonical bytes and fingerprints produced by `common.station_event` helpers.
- Lifecycle and projection metadata produced only as offline metadata.
- Fixture inventory and future ownership proposal.

Out of scope for this stage:

- Runtime Collector connection.
- DB write, schema change or migration.
- FastAPI endpoint.
- Dashboard, Trace UI or frontend.
- V-PLC behavior change.
- Real PLC pilot.
- Docker, deploy, tag or rollback.
- Any API-visible production outcome.

## 2. First implementation slice

Slice name: `Collector ingestion adapter offline fixtures`.

The first implementation slice, when PM later authorizes implementation, should
be a pure offline adapter around fixtures. It must not connect to PLC/V-PLC
runtime, storage, API or Dashboard code.

Inputs:

| Input | Required | Authority |
| --- | --- | --- |
| Frozen resolved config snapshot | yes | immutable config registry fixture selected by `config_hash` |
| PLC/V-PLC source payload fixture | yes | simulated or captured source boundary input |
| Mapping/template/profile/station snapshot | yes | resolved config snapshot contents |
| Optional raw payload | no | raw evidence only; never production fact by itself |
| State index fixture | yes for stateful decisions | accepted prior-event index fixture |

Outputs:

| Output | Meaning |
| --- | --- |
| Normalized `station_event` envelope | candidate envelope for `common.station_event` validation |
| Canonical bytes / fingerprints | canonical JSON bytes and fact/content/raw fingerprints from shared helpers |
| Validation decision | accepted/rejected decision from shared validation helpers |
| Lifecycle output | derived lifecycle metadata from shared helper |
| Projection metadata | offline metadata only; not persisted and not API-visible |
| Reject/defer/quarantine-style decision wrapper | adapter diagnostic wrapper for fixture assertions |

This slice produces no DB row and no API-visible production outcome. Accepted in
this context means "accepted by offline contract validation", not "stored",
"visible" or "deployed".

## 3. Adapter boundary

### 3.1 Source payload boundary

The source payload boundary is the exact data received from the source fixture
plus its fixture context:

- source kind: `plc` or `vplc`;
- mapping identity and source namespace;
- source timestamp and source event sequence when present;
- raw payload when the fixture includes it;
- the `config_hash` used to select a resolved config snapshot;
- state index fixture for duplicate/conflict/parent relation checks.

The adapter may decode, normalize and reject this input. It must not persist it,
mutate runtime config, or synthesize PLC/HMI decisions.

### 3.2 Normalized envelope boundary

The normalized envelope is the candidate `station_event` source envelope passed
to `common.station_event.parse_event()`, `validate_event()` and, where a state
fixture is required, `validate_event_stateful()` or
`validate_duplicate_or_conflict()`.

The adapter owns mapping source fields into the envelope. The shared package
owns station-event rules after the envelope exists.

### 3.3 Field authority

| Field group | Authority |
| --- | --- |
| `line_id`, `plc_id`, `station_id`, `station_type`, `profile_id`, `config_version`, `config_hash` | immutable resolved config snapshot selected by event/source `config_hash` |
| `event_type`, `result`, `nok_code`, `nok_origin`, `cycle_counter`, `unit_id`, `dmc`, payload values | PLC/V-PLC source payload after mapping/template decode |
| `plc_boot_id` | PLC/V-PLC runtime identity fact, carried in source/context |
| `mapping_id`, `payload_template` | resolved mapping/template snapshot |
| `source`, `actor` | source authority context, not transport channel |
| `event_id` | adapter/normalizer identity for the candidate envelope; must satisfy station-event contract |
| `source_event_id` | PLC/V-PLC/source fixture stable sequence or source-provided stable identity; not a transport retry ID |
| `observed_at` | Collector first-observed UTC time in future runtime; fixture value in offline tests |
| `created_at` | future DB time only; forbidden in current source envelope |

`source_event_id` must come from the PLC/V-PLC/source fixture stable sequence
or a source-provided stable identity. The normalizer or adapter must not create
or replace `source_event_id` with a random value, receive time, retry time or
Collector wrapper ID. `source_event_id` is not a transport retry ID.

### 3.4 Timestamp semantics

| Timestamp | Meaning | Present in this slice |
| --- | --- | --- |
| `event_ts` | source event time from PLC/V-PLC fact | yes |
| `observed_at` | Collector first-observed UTC time | optional fixture value; future runtime field |
| `created_at` | future DB insertion time | no; forbidden in current envelope |

The adapter must not replace `event_ts` with `observed_at`, and future storage
must not let `created_at` overwrite source event time.

Future runtime clock policy is not implemented in this slice. Clock skew,
missing source timestamp handling, monotonicity and watermark policy remain
future runtime work. The current offline slice must not infer `late` event
status from these missing policies. `observed_at` must not override `event_ts`,
and `created_at` is future DB time outside the current source envelope.

### 3.5 Boot/profile/station type/config hash semantics

- `plc_boot_id` isolates counter namespaces and parent relations.
- `profile_id` must come from the resolved station `cycle_profile` snapshot, not
  from profile mode labels.
- `station_type` is a historical event snapshot and must match the immutable
  snapshot selected by `config_hash`.
- `config_hash` selects the only valid resolved config snapshot for
  interpretation. It is not a hint to fall back to current runtime config.

### 3.6 Validator boundary

The adapter must call `common.station_event` validation helpers. It must not
duplicate, fork or reinterpret station-event rules.

Required helper boundary:

- parse/shape: `parse_event()`;
- stateless validation: `validate_event()`;
- stateful lineage/parent validation: `validate_event_stateful()`;
- duplicate/conflict/raw_variant: `validate_duplicate_or_conflict()`;
- lifecycle: `derive_lifecycle()`;
- projection metadata: `projection_for()`.

If a rule is missing or unclear, the next step is a station-event contract review
or shared helper change after PM authorization, not local adapter logic.

### 3.7 Serializer and fingerprint boundary

The adapter must use `common.station_event` canonical serializer and fingerprint
helpers:

- `canonical_json_bytes()`;
- `compute_fact_key()`;
- `compute_content_fingerprint()`;
- `compute_raw_evidence_fingerprint()`;
- `cycle_role_key()`;
- `production_result_key()`;
- `station_nok_detail_key()`.

Language-default JSON must never be used for identity, canonical bytes,
fingerprint comparison or duplicate/conflict decisions.

### 3.8 Projection metadata boundary

Projection output in this slice is metadata only:

- no persistence;
- no API-visible outcome;
- no production result row;
- no Quality/Pareto row;
- no Dashboard or Trace UI claim.

Rejected, deferred or quarantined inputs never project. Duplicate, conflict and
raw_variant decisions also produce no new production projection in this slice.

## 4. Resolved config snapshot contract

### 4.1 Lookup rule

The lookup input is `config_hash` from the incoming envelope/source context. The
adapter must retrieve exactly one immutable resolved config snapshot for that
hash before decoding or validating production semantics.

Events must be interpreted only by their own immutable `config_hash` snapshot.
The adapter must never fallback to latest/current runtime config when the
historical snapshot is missing or mismatched.

### 4.2 Required snapshot contents

The resolved snapshot fixture must contain:

| Snapshot content | Required use |
| --- | --- |
| line | `line_id`, timezone and line-scoped namespace |
| PLC | `plc_id`, runtime/identity mapping and source identity context |
| station | `station_id`, station order and station-specific source mapping |
| station_type | historical station type used by the event |
| station_enabled | disabled-station heartbeat-only rule |
| mapping | exact `mapping_id`, purpose, DB/source layout and source namespace |
| payload template reference/version | normalized payload field decode and template lineage |
| raw_policy | one of `raw_not_provided`, `raw_capable` or `raw_required`, selected from the immutable snapshot |
| decoder registry reference | immutable decoder registry snapshot identity for this `config_hash` |
| decoder id / decoder version / callable decoder | raw payload decode authority into normalized candidate payload |
| NOK template | allowed NOK code/origin interpretation |
| profile/cycle_profile | exact `profile_id` expected by the station-event contract |
| route/direct predecessor | upstream business evidence and direct predecessor validation |
| config_version/hash | readable version and immutable SHA-256 snapshot identity |

### 4.3 Decoder registry authority

D2-C decoder registry authority is implemented, reviewed, committed and pushed
at `5e5a617` for the offline adapter authority path. It implements immutable
decoder registry/schema authority and decoder callable binding for resolved
config snapshots. It does not implement D3 runtime raw wiring, runtime Collector
raw evidence connection, DB/API/Dashboard/V-PLC/deploy changes or ACK/read_done
ownership changes.

For any source that carries raw evidence or is declared `raw_capable` /
`raw_required`, the resolved config snapshot must bind interpretation to an
immutable decoder registry snapshot. The binding must include:

- decoder registry identity and registry content hash or equivalent immutable
  snapshot identity;
- decoder id selected by the mapping/payload template;
- decoder version expected by the event's immutable `config_hash` snapshot;
- callable decoder reference authorized for that decoder id/version;
- raw_policy selected by the immutable snapshot;
- payload template identity/version that the decoder output must satisfy.

Decoder id, decoder version and callable decoder authority must come from the
immutable resolved config snapshot and its referenced decoder registry snapshot.
They must not come from the latest registry, latest runtime config, current
mapping file, environment defaults or ad hoc fixture fields. The adapter must
never fallback to a latest/current decoder or runtime config when the historical
decoder id/version/callable binding is missing, unknown or mismatched.

The decoder callable is authority only for translating raw evidence into a
normalized candidate payload. It is not a production fact authority by itself.
The decoded candidate must still pass payload template checks,
raw/normalized comparison where normalized input is present, shared
station-event validation, fingerprinting and wrapper decision rules before any
offline projection metadata may be derived.

Fail-closed decoder authority rules:

- unknown decoder id: reject before decode as `RAW_PARSE_ERROR` or a more
  specific future decoder-authority code after PM approval;
- decoder id known but callable missing: reject before decode as
  `RAW_PARSE_ERROR`;
- decoder version mismatch: reject before decode as `RAW_PARSE_ERROR` or
  `RAW_NORMALIZED_MISMATCH` if a decoded/normalized comparison is possible;
- decoder callable exception: reject as `RAW_PARSE_ERROR`;
- decoder output does not match payload template, lineage, field authority or
  supplied normalized values: reject as `RAW_NORMALIZED_MISMATCH` or
  `EVENT_LINEAGE_INVALID` as applicable;
- forbidden raw content detected before or during decode: reject as
  `RAW_CONTENT_FORBIDDEN`;
- raw-only input before identity/projection/fingerprint production: remain
  unsupported and fail closed; it must not produce production facts, projection
  metadata, defect detail, Quality/Pareto output, API-visible state or ACK.

D2 owns decoder registry / decoder callable authority and immutable snapshot
binding. D2-C closes the offline registry/schema implementation gate with these
committed files:

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

D3 owns actual raw-capable/raw-required runtime wiring. D3 remains HOLD until
separately authorized. D2-C must not be read as runtime raw support or runtime
current mapping-file no-fallback closure. D2-C does not authorize D3 raw
runtime wiring, DB/API/Dashboard/V-PLC/deploy changes or ACK/read_done
ownership changes.

### 4.4 Fail-closed cases

| Case | Decision | Meaning |
| --- | --- | --- |
| `CONFIG_NOT_FOUND` | rejected | no immutable snapshot exists for the event/source `config_hash` |
| `CONFIG_HASH_MISMATCH` | rejected | snapshot content/hash does not match the supplied hash |
| `EVENT_LINEAGE_INVALID` | rejected | line/PLC/station/station_type/profile/mapping/predecessor lineage fails |
| `RAW_PARSE_ERROR` | rejected in MVP | raw payload exists but required decoder is missing or cannot parse |
| `RAW_NORMALIZED_MISMATCH` | rejected | decoded raw output does not match supplied normalized payload or template authority |
| `RAW_CONTENT_FORBIDDEN` | rejected | raw content is forbidden by contract before becoming evidence |
| `RAW_EVIDENCE_MISSING` | rejected | `raw_capable` or `raw_required` source is missing required raw evidence under immutable snapshot authority |

In this MVP, decoder missing with raw may be fail-closed rejected as
`RAW_PARSE_ERROR`. Future runtime may evolve some raw parsing failures into
deferred/quarantine semantics, but this offline contract does not persist
quarantine.

## 5. Raw / normalized authority matrix

| Input shape | MVP decision | Production fact authority | Projection |
| --- | --- | --- | --- |
| raw-only | unsupported and fail-closed before identity/projection/fingerprint production | none | never |
| normalized-only | may proceed to shared validation only when immutable source protocol, mapping or payload template declares raw is not provided, for example `raw_not_provided` or an equivalent no-raw capability, and config lineage is valid | normalized envelope from source mapping with explicit no-raw authority | only offline metadata if accepted |
| raw + normalized match | may proceed to shared validation | normalized envelope; raw is evidence | only offline metadata if accepted |
| raw + normalized conflict | rejected as raw/normalized mismatch | none | never |
| unknown decoder id | rejected as `RAW_PARSE_ERROR` before decode | none | never |
| decoder missing | rejected as `RAW_PARSE_ERROR` when raw is present or raw is required | none | never |
| decoder mismatch/exception | rejected as `RAW_PARSE_ERROR` or `RAW_NORMALIZED_MISMATCH` | none | never |
| forbidden raw content | rejected as `RAW_CONTENT_FORBIDDEN` | none | never |
| same content, different raw / raw_variant | duplicate + `raw_variant` diagnostic if canonical content is identical and only raw fingerprint differs | existing accepted canonical content | no new projection |
| future exact-byte fixture | must compare exact canonical bytes/fingerprints, not language-default JSON | shared canonical helpers | only after future gate |

Raw payload is evidence, not an independent production fact. Rejected, deferred
or quarantined inputs never project.

The raw_policy relationship is fail-closed:

- `raw_not_provided`: normalized-only may enter shared validation only when the
  immutable resolved snapshot, mapping or payload template explicitly declares
  no raw is produced or available.
- `raw_capable`: missing raw remains fail-closed unless PM later approves a
  contract change; it must not silently downgrade to `raw_not_provided`.
- `raw_required`: missing raw is fail-closed as `RAW_EVIDENCE_MISSING` or an
  equivalent future PM-approved code, with no projection or ACK.

`normalized-only` is not a bypass around raw evidence checks. It is allowed only
when the immutable source protocol, mapping or payload template explicitly says
raw is not produced or not available, such as `raw_not_provided` or an equivalent
capability. That no-raw declaration must come from the immutable resolved
snapshot, mapping or payload template, not from a temporary fixture field. If
the source, mapping or payload template requires raw and raw is missing, the
current offline slice must fail closed as rejected. Such an input must not
produce offline projection metadata, production outcome, defect detail,
DB-visible state or API-visible state. The adapter must not route a raw-capable
or raw-required source through `normalized-only` to avoid the raw evidence
check.

`30003/system_reserved` upstream evidence must not be synthesized by the
adapter. A `30003` skip relation must depend on legal accepted upstream business
evidence validated by shared stateful validation. Rejected, non-authoritative or
cross-config upstream evidence must not produce detail projection.

Sprint 3 adapter work does not modify Phase-1 ACK, `read_done` or write-back
semantics. Adapter retry and diagnostic wrappers must not become ACK owners.
This slice does not connect to runtime Collector and therefore does not change
boot, profile, counter or ACK behavior.

## 6. Reject / defer / quarantine contract

The adapter wrapper records a diagnostic decision for fixture assertions. It does
not write DB rows in this stage.

| Decision | Meaning in this slice | DB write allowed in this stage | API-visible production outcome |
| --- | --- | --- | --- |
| accepted | shared validators accepted the envelope and offline metadata was derived | no | no |
| rejected | fail-closed validation or contract violation | no | no |
| deferred | future retry/dependency semantics reserved; no current persistence | no | no |
| quarantined | diagnostic decision semantics only; no quarantine persistence implemented | no | no |
| duplicate | same business key and same canonical content as an accepted fixture | no | no |
| conflict | same business key but different canonical content | no | no |
| raw_variant | same canonical content but different raw evidence fingerprint | no | no |

Quarantined in this slice means only that the adapter can label a fixture as a
diagnostic decision category. No quarantine table, queue, retry worker or API is
implemented or authorized.

## 7. Offline fixture inventory

The first implementation test plan should include, but is not authorized in this
docs-only draft:

| Fixture | Acceptance intent |
| --- | --- |
| 3-station `cycle_start` / `cycle_complete` / `station_result OK` | nominal station flow across WS01-WS03 |
| `station_result NOK` + `station_nok` detail companion | canonical result plus detail-only companion |
| heartbeat | diagnostic-only liveness, no production projection |
| disabled_station heartbeat-only | post-MVP/future fixture; must not imply current runtime disabled-station behavior |
| unknown config hash | `CONFIG_NOT_FOUND` fail-closed |
| mapping mismatch | `EVENT_LINEAGE_INVALID` or mapping-specific rejection |
| payload_template_mismatch | fail closed when payload template identity/version does not match immutable snapshot |
| route_predecessor_mismatch | fail closed when route predecessor evidence does not match immutable snapshot |
| direct_predecessor_mismatch | fail closed when direct predecessor relation does not match immutable snapshot |
| profile mismatch | profile lineage fail-closed |
| station_type mismatch | station type historical snapshot fail-closed |
| raw decoder missing | `RAW_PARSE_ERROR` in MVP |
| unknown decoder id | `RAW_PARSE_ERROR` in MVP; no fallback to latest/current registry |
| raw decoder mismatch | `RAW_PARSE_ERROR` or raw/normalized mismatch |
| decoder output payload template mismatch | `RAW_NORMALIZED_MISMATCH` or lineage/template rejection; no projection |
| forbidden raw content | `RAW_CONTENT_FORBIDDEN` |
| normalized-only with source protocol/mapping declared no-raw | may enter shared validation |
| raw-required source with missing raw | fail-closed rejected; no projection |
| raw-capable source missing raw | fail-closed unless PM later approves a contract change; must not become accepted production fact |
| duplicate | same key and same canonical content |
| conflict | same key and different canonical content |
| raw_variant | same canonical content, different raw evidence fingerprint |
| historical resolved config snapshot | old event interpreted by old immutable snapshot |
| current config changed but historical event still uses old snapshot | no fallback to current config |
| multi-mapping station requiring exact `mapping_id` | rejects ambiguous or wrong mapping |
| future JCS exact-byte canonical JSON/fingerprint vectors | cross-runtime canonical identity guard |

## 8. Future file ownership proposal

This section is a proposal only. It does not authorize file creation or edits.

Possible future code:

- `collector/app/services/station_event_adapter.py`
- `collector/app/services/resolved_config_registry.py`

Possible future tests:

- `tests/test_collector_station_event_adapter.py`
- dedicated adapter fixture JSON path;
- future cross-runtime canonical fixture tests.

Existing files read-only for the first implementation:

- `common/station_event/*`
- `common/line_config/*`

Explicitly excluded:

- untracked PM handoff artifacts;
- DB migrations;
- FastAPI routes;
- Dashboard/frontend;
- V-PLC runtime;
- Docker/deploy files.

## 9. Required future tests

The following test groups are required before implementation can be accepted in a
future authorized implementation thread.

| Test group | Acceptance criteria |
| --- | --- |
| adapter nominal tests | 3-station cycle/result/NOK/heartbeat fixtures normalize and validate through shared helpers |
| lineage tests | config hash, line, PLC, station, station_type, profile, route/predecessor and mapping mismatches fail closed |
| raw authority tests | raw-only, normalized-only declared no-raw from immutable snapshot/mapping/template, raw-required missing raw, raw-capable missing raw, decoder missing, decoder exception, raw/normalized mismatch and forbidden raw content never produce facts |
| decoder authority tests | decoder registry snapshot, decoder id, decoder version and callable decoder are selected only from the immutable resolved snapshot; unknown decoder id, missing callable, callable exception, output mismatch and forbidden raw content fail closed with no fallback |
| decision tests | accepted/rejected/deferred/quarantined/duplicate/conflict/raw_variant wrappers are deterministic and non-persistent |
| projection tests | wrapper decision and `projection_for()` metadata are asserted together; only accepted envelopes produce offline projection metadata; rejected/deferred/quarantined/duplicate/conflict/raw_variant never project or leak rejected detail into Pareto/defect rows |
| Phase-1 regression tests | existing 3-station behavior and default runtime remain unchanged |
| future JCS exact-byte boundary tests | canonical bytes and fingerprints match approved vectors before JavaScript/PostgreSQL/API/DB integration |
| future duplicate/conflict precedence tests | multi-key duplicate/conflict precedence covers `event_id`, `fact_key`, cycle role / production result key and detail key, not only a single `fact_key` |
| future historical config replay tests | historical config replay and current-config-changed/old-snapshot behavior are covered |
| future raw error taxonomy tests | `RAW_PARSE_ERROR`, `RAW_NORMALIZED_MISMATCH`, `RAW_CONTENT_FORBIDDEN` and `RAW_EVIDENCE_MISSING` remain distinct |

## 10. Review gates

| Gate | Required conclusion before next step |
| --- | --- |
| Architecture gate | contract boundaries, ownership and non-goals are clear |
| Reliability gate | runtime safety, config snapshot behavior, decoder failure handling and queue/quarantine future semantics are acceptable |
| Data Quality gate | field authority, raw/normalized authority and projection boundaries preserve fact integrity |
| Verification gate | fixture matrix and acceptance criteria are testable without runtime side effects |
| PM authorization gate | explicit PM approval is required before implementation, tests, DB/API/Dashboard/V-PLC work, commit, push, tag, deploy or rollback |

## 11. Current control conclusion

Architecture contract/status sync: `PASS`.

Reliability Review: `PASS WITH RECOMMENDATIONS`, no blocker.

Data Quality targeted re-review: `PASS WITH RECOMMENDATIONS`, DQ-B1 CLOSED.

Verification Review: `PASS WITH RECOMMENDATIONS`, no blocker.

Eligible for docs-only closeout decision: yes.

D2-A decoder authority docs/contract-only repair: recorded. D2-C decoder
registry authority is implemented, reviewed, committed and pushed at
`5e5a617`. D2-C implements offline immutable decoder registry/schema authority
and decoder callable binding, but does not implement runtime raw support or D3
runtime raw wiring.

Eligible for D3 planning gate: yes, after PM approval.

Eligible for implementation without PM approval: no. PM approval is required
before runtime Collector raw wiring, DB/API/Dashboard/V-PLC/PLC pilot,
commit/push, tag, deploy, rollback or any change outside the approved docs
allowlist.
