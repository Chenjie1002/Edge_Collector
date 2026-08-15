# Edge MES Demo — Real Device Collector + Database Field Validation Branch Plan

更新时间：2026-08-08 08:32 UTC+8

## 0. Branch identity and purpose

Branch workstream ID:

`FIELD-VALIDATION-COLLECTOR-DB`

This is a parallel field-validation workstream for Edge MES Demo. Its purpose is to isolate the current data-acquisition and PostgreSQL path from the full Demo stack so it can be connected to real equipment for practical validation without dragging API, Dashboard, Grafana, V-PLC, simulator, sync-worker, transport/A0, or other mainline lifecycle work into the pilot.

The workstream must remain compatible with the accepted Edge MES architecture and event contracts, but it is not allowed to silently modify the mainline PM gate state. Mainline D2-R7B transport/A0 work and this field-validation branch have separate PM authority.

Primary product goal:

> Run a small, independently deployable Edge acquisition + PostgreSQL stack against a real PLC/device, prove that mapped device data can be read safely, decoded deterministically, persisted locally, recovered after normal faults, and inspected as real field evidence.

This branch is intended to answer a practical engineering question: **can the current collector/database core survive contact with a real device and real network behavior?**

## 1. Scope boundary

### 1.1 In scope

- Siemens S7 read path through `python-snap7` for real PLC/device validation.
- Existing mapping/read-plan/decoder logic under `collector/app/plc/`.
- Existing station-event adapter and accepted-fact logic when and only when the real source contract supports it.
- Existing PostgreSQL storage implementation under `collector/app/services/storage.py`.
- Existing DB schema/migrations required by collector persistence.
- A standalone field runtime containing only the minimum acquisition/database services.
- A real-device/site-specific mapping that does not overwrite `config/mapping.yaml`.
- Read-only shadow acquisition as the first real-device mode.
- Captured raw bytes + decoded field evidence sufficient to debug real addressing/type/endian/string/timestamp issues.
- Local DB-backed reliability tests and a bounded real-device pilot.
- Optional later ACK/writeback work only as a separate gate after a real PLC communication contract is frozen and explicitly authorized.

### 1.2 Explicitly out of scope for the initial branch

- API, Dashboard/frontend, Grafana, Prometheus UI work.
- V-PLC and simulator behavior changes except as local test fixtures.
- Oracle or `sync_worker` integration.
- OEE/management reporting expansion.
- Full MES workflow, operator workflows, recipe/parameter writeback, hold/release/rework control.
- Safety control, machine interlocks, motion control, emergency-stop logic.
- Production deployment acceptance.
- Mainline D2-R7B A05/R0/transport authority.
- Mainline Git merge/cherry-pick without separate Owner/mainline-PM authority.

## 2. Current reusable foundation

The repository already contains most of the reusable acquisition/database core. The branch should **reuse and isolate**, not fork and rewrite.

### 2.1 Collector assets already present

- `collector/app/plc/read_plan.py` builds bounded contiguous S7 DB read ranges from the mapping.
- `collector/app/plc/decoder.py` and related PLC mapping/address modules decode S7 values.
- `collector/app/services/event_collector.py` implements PLC connection, boot identity, station reads, adapter gating, transactional persistence, reliability handling, and Demo ACK behavior.
- `collector/app/services/storage.py` persists raw PLC samples, cycle events, quality data, accepted station-event facts, runtime status, and error records.
- `collector/tests/test_snap7_reliability_integration.py` already exercises Snap7 server/client behavior.
- DB-backed collector tests already exist under `collector/tests/`.

### 2.2 Database assets already present

The existing schema provides useful field-validation truth surfaces, including:

- `raw_plc_sample`
- `cycle_event`
- `quality_event`
- `collector_runtime_status`
- `collector_error_log`
- `data_gap_event`
- `production_accepted_station_event_fact`

The field branch should use a **separate PostgreSQL database/volume** while reusing compatible schema/migrations. Do not share the Demo `data/postgres` volume with real-device pilot data.

### 2.3 Existing orchestration coupling that must be removed for the branch

Current root `docker-compose.yml` couples the normal `collector` service to:

- `postgres`
- `s7-plc-sim`
- the full Demo config volume

`collector/app/main.py` can also start both the legacy snapshot loop and `EventCollectorWorker`, so it is not an ideal field-only entrypoint.

The branch therefore needs a **standalone field runtime/profile**, not a copy of the full Demo compose stack.

## 3. Important real-device safety finding

The current Demo event collector and the real PLC engineering guide do not have the same ACK byte ownership model.

Current Demo behavior in `collector/app/services/event_collector.py` writes the station handshake byte at offset 6 to set `read_done`:

`db_write(db_number, 6, bytearray([current_handshake_byte | 0b00000010]))`

The real-device engineering contract in `docs/plc_edge_integration_guide.md` explicitly requires:

- one variable has one writer;
- Edge must not modify PLC-owned process/control data;
- Edge write bits/words must use a dedicated Edge-owned write area;
- PLC-owned and Edge-owned BOOLs must not share a byte where a byte write could overwrite PLC bits;
- the recommended real protocol uses dedicated `ack_valid` + `ack_counter` semantics.

Therefore:

> **The first real-device pilot MUST be read-only. The existing Demo ACK implementation must not be enabled against a real PLC.**

Any real PLC writeback/ACK becomes a later, separately authorized gate after a site-specific PLC-Edge contract proves dedicated write ownership.

## 4. Architecture decision

Three approaches were considered.

### Approach A — copy `collector/` and DB schema into a new field application

Rejected as the default.

Advantages:
- fast isolation at first.

Problems:
- immediate source fork;
- fixes do not flow cleanly between Demo and field validation;
- mapping/decoder/storage semantics can diverge;
- doubles test and maintenance burden.

### Approach B — standalone field profile reusing existing collector/database core

**Recommended.**

Create a minimal field deployment surface and a small field-specific runtime entrypoint/mode while continuing to import the existing PLC mapping/read-plan/decoder/storage code.

Advantages:
- field findings directly validate the code intended for Edge MES;
- minimum duplication;
- mainline contracts remain visible;
- safe separation can be achieved at deployment/config/runtime-mode boundaries.

### Approach C — run an ad-hoc host Python script directly against the PLC and an external PostgreSQL

Allowed only as a diagnostic fallback, not the target branch architecture.

Advantages:
- easiest network debugging.

Problems:
- diverges from Docker/edge deployment behavior;
- encourages one-off scripts and undocumented state;
- weakens reproducibility.

## 5. Target field architecture

Initial read-only data flow:

```text
Real PLC / Device
    |
    | S7 TCP read only
    v
Standalone Field Collector
    |- site mapping
    |- bounded read plans
    |- S7 decoder
    |- raw/decoded validation
    |- runtime/error telemetry
    v
Isolated PostgreSQL
    |- raw_plc_sample
    |- collector_runtime_status
    |- collector_error_log
    |- cycle/accepted facts only when source contract is valid
```

Services intentionally absent from the first field runtime:

```text
simulator
s7-plc-sim
api
dashboard
grafana
prometheus
sync-worker
```

### 5.1 Recommended deployment isolation

Recommended future layout, subject to the branch PM's implementation task:

```text
deploy/field/
  docker-compose.field.yml
  .env.example

config/field/
  <site-or-device>/
    mapping.yaml
    app.yaml

collector/app/
  field_main.py
  services/field_sampler.py       # only if needed; reuse existing modules below it
```

The branch should not overwrite `config/mapping.yaml`. A field-specific mapping should be mounted read-only to the container path consumed by the field runtime.

Recommended isolated database defaults:

```text
POSTGRES_DB=edge_mes_field
separate Docker volume / host data directory
no reuse of ./data/postgres
```

The exact port, volume path and secret handling must be frozen by the branch PM for the target host before deployment.

## 6. Runtime modes

### 6.1 Mode 1 — `shadow_read_only`

This is the mandatory first real-device mode.

Required properties:

- S7 reads only.
- `snap7.client.Client.db_write` is unreachable from the field shadow path.
- no ACK/read_done/ack_valid/ack_counter write.
- no parameter write.
- no control DB mutation.
- reads only exact DB/range allowlisted by the site mapping.
- bounded polling interval and connection timeout.
- persistent error recording/backoff on connection/decode/DB failures.
- raw bytes and decoded values available for engineering comparison.

The shadow path may persist raw/decoded data even before the full station-event contract is proven. It must not manufacture production truth from ambiguous fields.

### 6.2 Mode 2 — `event_handshake`

Not authorized by this plan.

This future mode becomes eligible only after:

1. the real PLC communication DB is frozen;
2. Edge-owned ACK bytes/words are physically separate from PLC-owned bits;
3. `ack_valid`/`ack_counter` or an equivalent site contract is documented;
4. DB-commit-before-ACK behavior is tested;
5. PLC/device owner explicitly approves writeback;
6. Owner/branch PM issues a separate execution authority.

The existing Demo `read_done` byte-write implementation must not simply be pointed at the real PLC.

## 7. Site integration contract required before code/deployment execution

The branch PM's first real deliverable should freeze a **Real Device Integration Contract** containing at least:

### Device/network identity

- site/line/device identifier;
- PLC vendor/model/CPU;
- PLC IP/hostname;
- TCP port;
- rack/slot;
- network path from Edge host to PLC;
- target Edge host hardware/OS;
- whether Docker is allowed on that host.

### Read contract

For every scope/station:

- DB number;
- byte start/end;
- field name;
- Siemens type;
- byte/bit offset;
- string max length/charset;
- unit/scaling;
- invalid/sentinel value;
- sampling/event timing;
- owner/source of truth;
- whether the field is stable during the Edge read window.

### Identity/event semantics

- PLC restart/boot identity source;
- cycle/event counter source and reset/wrap rules;
- unit/DMC/carrier identity source;
- event-ready semantics if any;
- timestamp encoding and timezone;
- result/NOK code dictionary.

### Safety/write ownership

- exact areas Edge may read;
- exact areas Edge may write, default `NONE` for first pilot;
- explicit statement that machine safety/control does not depend on Edge;
- behavior when Edge is offline;
- PLC buffer/overwrite behavior.

### Data/operations

- expected cycle time/event rate;
- retention window for field DB;
- whether data contains serial numbers/operator identifiers or other sensitive plant data;
- backup/export requirement;
- rollback/stop procedure.

Unknown fields must remain unknown. The branch PM must not guess PLC addresses, counter semantics, timestamps or write ownership.

## 8. Phased branch gates

Each gate requires separate PM/Owner authority. Passing one gate does not authorize the next.

### FV0 — Branch takeover + site discovery / integration contract

Goal:
- establish exact real-device requirements without changing source or touching the device.

Deliverables:
- durable branch takeover report;
- Real Device Integration Contract;
- target host/network/deployment decision;
- exact first-pilot read allowlist.

No PLC/network mutation, DB deployment, Git branch creation, or source change is implied.

PASS when:
- device identity and read addresses are concrete enough to implement/test;
- first pilot write authority is explicitly `NONE`;
- no unresolved ambiguity could cause Edge to read a safety/control region by mistake.

### FV1 — Standalone field stack extraction

Goal:
- run only Collector + isolated PostgreSQL locally, without simulator/V-PLC/API/Dashboard dependencies.

Expected engineering deliverables:
- field compose/profile;
- isolated DB volume/database configuration;
- field runtime entrypoint/mode;
- site mapping mounting contract;
- config validation;
- tests proving no PLC write path is reachable in shadow mode.

Validation:
- local/synthetic Snap7 fixture first;
- DB-backed tests against isolated PostgreSQL;
- full existing relevant collector tests remain green.

### FV2 — Captured/synthetic mapping qualification

Goal:
- prove real-device address mapping and decoder semantics before live acquisition.

Inputs may include PLC watch-table exports, known-good values, or manually captured byte fixtures supplied by the device team.

Validation examples:
- S7 integer/REAL/string/endian correctness;
- timestamps;
- counter monotonicity/reset rules;
- valid/invalid ranges;
- payload lengths;
- raw bytes -> decoded JSON deterministic replay.

No live PLC writeback.

### FV3 — Real device read-only shadow pilot

Goal:
- connect the standalone field collector to the actual equipment and persist real data.

Hard boundary:
- read-only S7 traffic;
- `db_write=0`;
- no ACK or parameter/control writes.

Recommended pilot acceptance window:
- freeze a site-appropriate duration/event count in the FV3 task;
- default planning recommendation is at least 30 minutes and at least 20 valid target events/cycles where production rate allows;
- if equipment cadence is slower, use a duration/cycle threshold explicitly approved in the FV3 task rather than inventing PASS from a short sample.

Evidence should cover:
- successful connect/reconnect;
- exact DB/range reads;
- raw bytes;
- decoded values cross-checked with PLC/HMI/device truth;
- PostgreSQL rows;
- timestamps/counters;
- no write calls;
- CPU/network load observations where available;
- disconnect/restart behavior.

### FV4 — Reliability and data-quality acceptance

Goal:
- determine whether the field collector is credible enough for continued pilot use.

Required classes:
- DB unavailable/recovery;
- PLC disconnect/reconnect;
- collector restart;
- duplicate/repeated read behavior;
- counter reset/wrap classification;
- mapping mismatch/fail-closed behavior;
- invalid/partial payload behavior;
- storage growth/retention observation;
- data consistency versus PLC/HMI reference.

This gate may accept `PASS WITH RECOMMENDATIONS`; it must not demand a general audit/forensics system.

### FV5 — Optional real ACK/writeback protocol

Not part of the initial field-validation MVP.

Only open if the user wants true event handshaking after read-only validation succeeds.

This requires a new Architecture/Integration design and explicit device-team approval. Recommended contract follows `docs/plc_edge_integration_guide.md`: dedicated Edge-owned `ack_valid` and `ack_counter`, not the current Demo shared-byte `read_done` mutation.

### FV6 — Branch closure / mainline backport decision

Goal:
- classify field findings into:
  1. generic collector/database improvements worth integrating into mainline;
  2. site-specific mapping/config that stays outside generic core;
  3. field-only deployment assets;
  4. unresolved operational risks/backlog.

No automatic merge/cherry-pick. Mainline integration requires its own Owner/mainline PM authority and exact changed-file review.

## 9. Proposed code/test boundaries

The branch PM should prefer the following decomposition rather than broad refactoring.

### Reuse unchanged where possible

- `collector/app/plc/address.py`
- `collector/app/plc/mapping.py`
- `collector/app/plc/read_plan.py`
- `collector/app/plc/decoder.py`
- `collector/app/services/storage.py`
- `collector/app/services/station_event_adapter.py`
- shared station-event/config contracts under `common/`

### Likely branch additions/targeted changes

- standalone field entrypoint that does not start the legacy simulator snapshot loop;
- read-only sampler/service if the existing event worker cannot be safely reused without ACK;
- explicit field mode / writeback-off configuration;
- field compose/profile and isolated DB config;
- field/site mapping directory;
- tests proving shadow mode has zero PLC writes;
- captured-replay tests for real PLC byte samples.

Do not perform a large source-layer rewrite merely to make the field branch look cleaner.

## 10. Database strategy

### Initial strategy

Use PostgreSQL 16 as today, but create an isolated field database/volume.

Prefer reusing the current schema and migrations needed by Collector rather than inventing a second field schema. This allows field evidence to exercise the same persistence code.

For shadow-mode data that is not yet valid production event truth:

- raw sample/runtime/error tables are authoritative engineering evidence;
- accepted production fact tables must be written only when the event adapter/source contract is actually satisfied;
- ambiguous source data must not be coerced into accepted station events simply to populate the Dashboard schema.

### Retention

Field data retention must be explicitly frozen before long-running collection. Until then, the branch should use a bounded pilot database and avoid claiming production retention readiness.

## 11. Test strategy

The implementation branch should use TDD and retain the following test layers.

1. **Pure mapping/decoder tests**
   - captured bytes -> exact decoded values.
2. **Write-safety tests**
   - shadow runtime fails if a PLC write primitive is invoked;
   - no ACK path reachable from shadow CLI/config.
3. **Snap7 integration tests**
   - local server fixture; connection/reconnect/read-range behavior.
4. **DB-backed tests**
   - isolated PostgreSQL; raw/runtime/error persistence; transaction behavior.
5. **Fault tests**
   - PLC unavailable, DB unavailable, malformed bytes, mapping mismatch.
6. **Captured replay regression**
   - preserve sanitized real byte captures as explicit test fixtures only when plant-data handling permits.
7. **Field pilot evidence**
   - live reads and DB rows are real field evidence; synthetic tests must never be represented as real-device PASS.

## 12. Acceptance criteria for the branch MVP

The initial branch MVP is complete when all of the following are established:

- a standalone Collector + PostgreSQL field stack exists;
- it starts without simulator, V-PLC, API, Dashboard or sync-worker;
- a real site mapping is validated and source-controlled or otherwise durably managed under the site's confidentiality policy;
- collector connects to the target real PLC/device;
- all live pilot PLC operations are read-only;
- exact target DB/ranges are read and decoded correctly;
- real values are independently cross-checked against PLC/HMI/device truth;
- data persists into an isolated PostgreSQL database;
- connection and DB failures do not crash into uncontrolled write/retry behavior;
- collector restart/reconnect behavior is understood and documented;
- no field evidence is misrepresented as mainline production acceptance;
- the branch produces a clear decision on whether to proceed to a dedicated ACK/writeback gate.

## 13. Explicit non-goals / stop conditions

Stop and return to the branch PM before live connection when:

- PLC address ownership is ambiguous;
- the requested DB range overlaps a safety/control or unknown ownership area;
- the only way to proceed is to enable the existing Demo ACK byte write;
- real device access would require unauthorized network, credential, firewall or PLC-project mutation;
- mapping semantics are guessed rather than confirmed;
- the target DB environment would overwrite or contaminate existing Demo/production data;
- the user requests writeback before a dedicated write ownership contract exists.

## 14. Git/worktree strategy

This workstream should be isolated from the mainline PM's active workspace.

Recommended future Git branch name:

`field/real-device-collector-db`

Recommended execution model:

- use a separate Git worktree/checkout for the branch PM and its implementation Threads;
- do not create the branch/worktree until the Owner grants explicit Git/worktree authority;
- do not stage/commit/push/merge by inheritance from this planning document;
- branch PM owns only this field-validation workstream;
- mainline PM continues to own D2-R7B A0/A05/R0 progression;
- any backport/merge is a separate cross-workstream decision.

## 15. First information the branch PM must obtain from the Owner/device team

Before FV1/FV3 execution, obtain concrete answers for:

1. real PLC model/CPU and firmware family;
2. PLC IP, port, rack, slot and network path;
3. target Edge host and operating system;
4. exact stations/device types included in the pilot;
5. current PLC DB/address list or PLC project/watch-table export;
6. whether a dedicated Edge communication DB already exists;
7. expected cycle/event rate;
8. source of unit/DMC/counter/boot identity/timestamps;
9. whether the first pilot is strictly read-only — default answer must remain YES unless explicitly changed later;
10. desired pilot duration and acceptable plant-data retention/export policy.

## 16. PM recommendation

Start this branch with **FV0 read-only discovery + site integration contract**, not source implementation.

The current repository already has enough reusable collector/database capability that the highest-risk unknowns are not Python syntax or PostgreSQL CRUD. They are real PLC address semantics, network behavior, write ownership, event timing, and the mismatch between Demo ACK and the recommended real PLC ACK contract.

The independent branch PM should keep the first implementation small: isolate Collector + PostgreSQL, add a read-only field runtime, qualify the real mapping, and get real bytes into a clean field DB. Only after that evidence exists should the project decide whether an ACK protocol change is worth implementing.
