# Edge MES Demo — Independent Branch PM Handoff — Real Device Collector + DB Field Validation — 2026-08-08 08:32 UTC+8

## 0. Handoff purpose

Owner requested a separate branch workstream that isolates the current data-acquisition and database path so it can be connected to real equipment for practical field validation, and requested that this branch be handed to a different independent ChatGPT PM.

Branch workstream ID:

`FIELD-VALIDATION-COLLECTOR-DB`

This handoff transfers branch planning context and branch-PM decision responsibility only. It does **not** transfer mainline PM ownership and does not authorize source mutation, Git branch/worktree creation, network access to a real PLC, Docker deployment, database deployment, PLC writeback, stage/commit/push/merge, or any production action.

The new branch PM is expected to lead the field-validation workstream independently while respecting the mainline PM's separate authority over D2-R7B A0/A05/R0 and later gates.

## 1. Authoritative branch plan

Primary durable branch plan:

```text
path  = docs/reports/branch_real_device_collector_db_field_validation_plan.md
bytes = 22245
SHA   = d885ff5b2e41f938b95dec3a8238bdd0148a11116028527d71726562bdac3d02
state = WRITTEN / branch PM takeover input / untracked / unstaged
```

The branch PM must read this plan completely before proposing implementation.

The plan defines the branch architecture, scope, phased gates FV0–FV6, field safety boundary, database isolation strategy, recommended worktree strategy, and the unresolved site information required from the Owner/device team.

## 2. Relationship to the mainline project

Current mainline PM handoff:

```text
path  = docs/thread_handoff/chatgpt_pm_handoff_260808-0807.md
bytes = 23845
SHA   = 0d4fc92c6c4b02bfe6b5b713317707f97c163ca673b61014393b87c1fb656197
state = current mainline PM handoff
```

Mainline state transferred by that handoff includes:

```text
LOCAL TRANSPORT WORKSPACE MATERIALIZED = YES
W0 ACCEPTED                            = YES
A0-C1                                  = PM ACCEPTED / PASS
A0 ARCHIVE ACCEPTOR QUALIFIED          = YES
A05                                    = UNUSED / NOT AUTHORIZED
A0 EXECUTION AUTHORIZED                = NO
ARCHIVE ACCEPTED                       = NO
R0 AUTHORIZED                          = NO
```

The branch PM must not change, reinterpret, advance, block, or inherit those mainline gates. Mainline A05/transport/archive work is separate from the real-device collector/database branch.

The branch may later propose generic collector/database fixes for backport, but no merge/cherry-pick/mainline mutation is authorized by this handoff.

## 3. Branch current state

At handoff:

```text
BRANCH PM HANDOFF                         = WRITTEN
BRANCH WORKSTREAM                         = FIELD-VALIDATION-COLLECTOR-DB
BRANCH PLAN                               = WRITTEN
FV0 SITE INTEGRATION CONTRACT             = NOT STARTED
FV1 STANDALONE FIELD STACK                = NOT STARTED
FV2 MAPPING/CAPTURE QUALIFICATION          = NOT STARTED
FV3 REAL DEVICE READ-ONLY PILOT           = NOT STARTED
FV4 RELIABILITY/DATA QUALITY ACCEPTANCE    = NOT STARTED
FV5 REAL ACK/WRITEBACK                     = NOT AUTHORIZED / OPTIONAL LATER
FV6 BACKPORT/CLOSURE                       = NOT STARTED
REAL PLC NETWORK ACCESS                    = NOT AUTHORIZED BY THIS HANDOFF
REAL PLC WRITEBACK                         = FORBIDDEN UNTIL SEPARATE CONTRACT/AUTHORITY
FIELD POSTGRES DEPLOYMENT                  = NOT AUTHORIZED
GIT BRANCH/WORKTREE                        = RECOMMENDED / NOT CREATED / NOT AUTHORIZED
GIT STAGE/COMMIT/PUSH/MERGE                = NOT AUTHORIZED
```

No collector source, DB schema, compose file, mapping, runtime, PLC, Docker service, or Git ref was changed as part of branch planning/handoff.

## 4. Current repository baseline

Fresh planning-time baseline:

```text
branch            = main
HEAD              = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
origin/main       = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
ahead / behind    = 0 / 0
tracked unstaged  = docs/current_status.md
                     docs/thread_handoff/pm_operating_rules.md
cached diff       = empty
```

The checkout contains extensive pre-existing untracked project artifacts. Do not perform broad cleanup, reset, stash, global untracked equality checks, or broad staging as part of branch takeover.

The two branch planning/handoff files are expected to be new untracked/unstaged docs until separate Git authority is granted.

## 5. Required takeover reading order for the branch PM

The new branch PM should perform a read-only takeover in this order:

1. this exact branch handoff;
2. `docs/reports/branch_real_device_collector_db_field_validation_plan.md`;
3. current `docs/thread_handoff/pm_operating_rules.md`, especially Sections 10–13;
4. current mainline `docs/thread_handoff/chatgpt_pm_handoff_260808-0807.md` for authority separation only;
5. `docs/architecture.md`;
6. `docs/plc_edge_integration_guide.md`;
7. `docs/contracts/ack_protocol.md`;
8. `docs/contracts/collector_ingestion_adapter.md` for accepted-only persist/ACK and source-authority boundaries;
9. `collector/app/main.py`;
10. `collector/app/services/event_collector.py`;
11. `collector/app/services/storage.py`;
12. `collector/app/plc/read_plan.py` plus mapping/decoder modules as needed;
13. `config/mapping.yaml` as the current Demo mapping, not a real-site mapping;
14. `db/init/003_event_schema.sql` and `db/migrations/007_accepted_station_event_visibility.sql`;
15. existing Snap7/reliability/DB-backed collector tests relevant to the field path.

After reading, the branch PM should fresh-check the repository state rather than treating this handoff's Git snapshot as permanent authority.

## 6. Key architectural conclusion already established

Do **not** fork/copy the collector and database implementation into a second application.

Recommended architecture:

- reuse existing PLC mapping/read-plan/decoder modules;
- reuse existing storage and DB schema where compatible;
- create an independent field deployment/profile;
- use a separate field PostgreSQL database/volume;
- use a dedicated field runtime entrypoint/mode that does not require simulator/V-PLC/API/Dashboard;
- first live mode is strictly read-only shadow acquisition;
- later ACK/writeback is a separate optional gate.

The branch is intended to validate the real collector/database core, not create a disposable diagnostic script that cannot be integrated back.

## 7. Critical safety finding — real PLC writeback is not yet compatible with the Demo ACK path

Current Demo event collector writes `read_done` by modifying the station handshake byte at DB offset 6.

The project's real PLC engineering guide requires a dedicated Edge-owned write area and specifically warns against PLC-owned and Edge-owned BOOLs sharing a byte because normal byte writes can overwrite the other writer's bits.

The real guide recommends dedicated `ack_valid` + `ack_counter` semantics.

Therefore the branch PM must preserve this rule:

```text
FIRST REAL DEVICE PILOT = READ ONLY
PLC db_write calls       = 0
ACK/read_done writes     = 0
parameter/control writes = 0
```

The branch PM must not authorize the existing Demo `read_done` byte-write against real equipment merely because it works with V-PLC.

If the Owner later wants true handshake testing, open FV5 only after the PLC/device team freezes exact Edge-owned write addresses and explicitly approves writeback.

## 8. Reusable current code boundaries

Useful existing components:

```text
collector/app/plc/address.py
collector/app/plc/mapping.py
collector/app/plc/read_plan.py
collector/app/plc/decoder.py
collector/app/services/storage.py
collector/app/services/station_event_adapter.py
collector/app/services/event_collector.py
collector/tests/test_snap7_reliability_integration.py
collector/tests/*db_backed*
db/init/003_event_schema.sql
db/migrations/007_accepted_station_event_visibility.sql
```

Important current coupling:

- root `docker-compose.yml` collector depends on `postgres` and `s7-plc-sim`;
- `collector/app/main.py` starts the normal source snapshot loop and can separately start `EventCollectorWorker`;
- this is why the field branch should introduce a small standalone runtime/profile rather than run the full Demo stack against a real device.

## 9. Branch gate model

### FV0 — Branch takeover + real-device site integration contract

This should be the first branch gate.

Purpose:
- obtain exact real PLC/device facts and freeze a read-only pilot contract before implementation.

Required inputs from Owner/device team:

1. PLC model/CPU and firmware family;
2. PLC IP/host, TCP port, rack, slot;
3. target Edge host/OS and network path;
4. target stations/device types;
5. exact DB/address list or PLC project/watch-table export;
6. whether a dedicated Edge communication DB already exists;
7. expected cycle/event rate;
8. unit/DMC/counter/boot/timestamp sources;
9. confirmation that first pilot is read-only;
10. desired pilot duration and plant-data retention/export rules.

The branch PM must not guess any of these facts.

### FV1 — Standalone Collector + PostgreSQL field stack

Expected outcome:
- only acquisition + isolated Postgres required;
- no simulator/V-PLC/API/Dashboard/sync-worker dependency;
- field-specific mapping remains separate from Demo mapping;
- shadow mode statically and dynamically proves zero PLC writes.

### FV2 — Mapping / captured-byte qualification

Qualify real addresses, types, endianness, strings, timestamp/counter semantics using known values/captured fixtures before live pilot acceptance.

### FV3 — Real-device read-only shadow pilot

This is the first live PLC gate and requires separate explicit network/device authority.

Hard rule:

`db_write = 0`

### FV4 — Reliability / data-quality acceptance

Validate reconnect, DB outage/recovery, restart, repeated reads, counter behavior, mapping failures, and cross-check against PLC/HMI/device truth.

### FV5 — Optional ACK/writeback redesign

Not part of initial branch MVP. Requires a separate design based on dedicated Edge-owned ACK addresses.

### FV6 — Mainline backport/closure decision

Classify generic reusable changes, site-specific config, field-only deployment assets and remaining risks. No automatic merge.

## 10. Branch MVP definition

The first branch MVP is not "production MES" and not "full event handshake".

It is:

> A standalone Collector + PostgreSQL runtime connects to one real PLC/device, performs only approved S7 reads, correctly decodes the approved site mapping, persists real field data in an isolated local database, survives ordinary disconnect/restart/DB failure scenarios without uncontrolled behavior, and produces enough evidence to decide whether a later ACK/writeback pilot is justified.

A successful branch MVP must not be represented as mainline production acceptance.

## 11. Recommended future file topology

The branch plan recommends, but does not authorize, a focused layout such as:

```text
deploy/field/docker-compose.field.yml
deploy/field/.env.example
config/field/<site-or-device>/mapping.yaml
config/field/<site-or-device>/app.yaml
collector/app/field_main.py
collector/app/services/field_sampler.py   # only if existing workers cannot safely provide read-only behavior
```

The implementation PM should reuse existing modules and avoid broad refactoring.

Use an isolated PostgreSQL database/volume such as `edge_mes_field`; do not point real pilot collection at the Demo `./data/postgres` volume.

Exact paths may be refined by the branch PM's FV1 task, but they must remain explicit and isolated.

## 12. Git/worktree recommendation and authority separation

Recommended branch name:

`field/real-device-collector-db`

Recommended execution isolation:

- separate Git worktree/checkout for the branch PM and implementation Threads;
- do not create it from conversational momentum;
- Owner must explicitly authorize Git branch/worktree creation;
- branch PM may not stage/commit/push merely because it owns the branch workstream;
- stage/commit/push/merge remain separate authority under PM Rules;
- no merge/cherry-pick into mainline until Owner/mainline PM accepts the exact backport scope.

This is important because the main checkout currently contains active mainline PM authority documents and uncommitted artifacts.

## 13. Branch PM operating principles

The independent branch PM should follow these priorities:

1. field safety before convenience;
2. exact real-device facts before implementation assumptions;
3. read-only acquisition before writeback;
4. reuse collector/database core instead of source fork;
5. separate field data from Demo data;
6. captured real bytes become replayable tests where plant-data policy allows;
7. synthetic evidence and live device evidence remain explicitly separated;
8. no Dashboard/API work until acquisition/database truth is credible;
9. no overgrown audit framework; validation should answer concrete field risks;
10. each FV gate has separate authority and stop conditions.

## 14. What this handoff authorizes the new branch PM to do

The new branch PM is authorized to:

- perform read-only branch takeover;
- inspect repository documents/source/tests relevant to this branch;
- lead branch planning and decompose FV0–FV6;
- ask the Owner for missing real-device/site facts;
- propose repository-backed tasks and authority boundaries;
- recommend whether a separate worktree/branch is required.

This handoff does **not** authorize the branch PM to directly execute or delegate:

- source/config/schema changes;
- Docker/container mutations;
- network calls to a real PLC;
- firewall/VPN changes;
- PLC project download/upload;
- S7 write operations;
- Postgres deployment/mutation outside explicitly approved local test fixtures;
- Git branch/worktree/stage/commit/push/merge;
- mainline A05/R0 work.

Those require fresh Owner authority and repository-backed tasks as required by PM Rules.

## 15. First branch-PM decision after takeover

The branch PM should **not** start with code.

First action after takeover:

`FV0 — Real Device Integration Contract / Read-Only Pilot Boundary`

The PM should return an Owner-facing intake checklist for the missing device facts. Once the Owner/device team supplies those facts, the PM should freeze the FV0 contract and then propose the smallest FV1 implementation task.

If the real device already has a dedicated communication DB and a documented address table, the branch PM may accelerate FV0 but must still mechanically separate read ownership from write ownership.

## 16. Handoff terminal state

```text
FIELD-VALIDATION-COLLECTOR-DB PLAN      = WRITTEN
BRANCH PM HANDOFF                       = WRITTEN
SUCCESSOR BRANCH PM TAKEOVER            = PENDING
FV0                                     = ELIGIBLE FOR PLANNING / NOT EXECUTION-AUTHORIZED
FV1                                     = NOT AUTHORIZED
FV2                                     = NOT AUTHORIZED
FV3 REAL DEVICE ACCESS                  = NOT AUTHORIZED
FV5 PLC WRITEBACK                       = NOT AUTHORIZED
GIT BRANCH/WORKTREE                     = NOT AUTHORIZED
MAINLINE PM AUTHORITY                   = SEPARATE / UNCHANGED
```

The outgoing planning PM should stop leading this branch after publishing the handoff identity and successor-PM launcher.
