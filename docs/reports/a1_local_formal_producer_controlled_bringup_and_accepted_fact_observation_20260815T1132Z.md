# A1 Local Formal Producer Controlled Bring-up and Accepted Fact Observation — Result

## Conclusion

`PASS / A1_LOCAL_FORMAL_PRODUCER_ACCEPTED_FACT_OBSERVED`

The local formal producer path generated the first production accepted fact naturally through the implemented V-PLC -> Collector -> PostgreSQL path. No fixture, manual SQL insert, forced NOK, remote copy/import or sync-worker path was used.

## Authority

Owner authorized `A1_LOCAL_FORMAL_PRODUCER_CONTROLLED_BRINGUP_AND_ACCEPTED_FACT_OBSERVATION` on 2026-08-15.

Task:
`docs/thread_handoff/pm_task_20260815T1132Z_a1_local_formal_producer_controlled_bringup_and_accepted_fact_observation.md`

Mechanical identity before execution:
- regular / non-symlink
- bytes: `6177`
- SHA-256: `cb0aa692b46d5514ada65b5973ed7a83d9671fd52016847ab76b9d1aeb7921a0`

## Frozen baseline

- branch: `main`
- HEAD: `6226bf3fb716880a176f9eb642b8139cef3255a6`
- origin/main: `6226bf3fb716880a176f9eb642b8139cef3255a6`
- ahead/behind: `0/0`
- staged: `0`
- tracked dirty: `0`
- diff checks: PASS
- protected runtime prestate: postgres running, API running, dashboard running
- accepted fact pre-count: `0`

Frozen producer images:
- simulator: `sha256:e27022b07ae46639ca19b090613a90f839aa112de2dc514ef0a5705ca8c189a0`
- s7-plc-sim: `sha256:551cfe8f71d150949a212af7c6e4723c82c24fc73017e5b08f1dbe4f8a64a815`
- collector: `sha256:3a7ec1f2bcc6811508e43b0765f177d89aa6f5011bba86f1152ff458a50e8df9`

## Lifecycle

Execution lock start UTC: `2026-08-15T11:33:47Z`.

Single authorized producer bring-up:
`docker compose up -d --no-build --pull never simulator s7-plc-sim collector`

- invocation count: `1/1`
- RC: `0`
- build: `0`
- pull: `0`
- retry: `0`

All three producer containers reached `running` during observation.

## Accepted-fact transition

Bounded polling observed:
- rounds 1-6: fact count `0`
- round 7: fact count `1`

Observation end UTC: `2026-08-15T11:34:19Z`.

Transition: `0 -> 1`.

The first accepted fact was:
- line_id: `LINE_001`
- station_id: `WS01`
- event_type: `station_result`
- production_result: `ok`
- unit_id: `U-20260815-000001`
- dmc: `SUB-000001`
- cycle_counter: `1`
- source_event_id: `sha256:aef4f112b0d23444c7e36dab0f6e0f4e24558a6dfc1722ea6997c52b3eeb425c`
- event_ts: `2026-08-15T19:34:19+08:00`
- accepted_at: `2026-08-15T19:34:19.341916+08:00`
- fact_key: `sha256:36c739dea4671abefdf7a366809d790393311e7843a854a789b323ecdcc4fabf`

This evidence came from the production accepted-fact table and not from a fallback source.

## Producer containment

Because the default V-PLC plan is continuous, the gate used its one bounded containment stop after decisive evidence:
`docker compose stop collector s7-plc-sim simulator`

- stop invocation: `1/1`
- stop RC: `0`
- no `down`, `rm`, volume deletion, image deletion or network cleanup
- postgres/API/dashboard remained running
- generated accepted fact remained in PostgreSQL

Final producer container states were stopped/exited. Collector and s7-plc-sim reported exit code 137 after Compose stop containment; simulator exited 0. The stop command itself returned RC 0 and the bounded-write objective was achieved. This gate does not classify the 137 containment exit code as a product runtime failure because no unexpected exit occurred during the production observation window.

## Consumer verification

Read-only verification window used `2026-08-15T11:33:47Z` to `2026-08-15T11:34:30Z`.

### Quality

`GET /api/v2/production/quality` for `LINE_001 / WS01`:
- HTTP 200
- ok: `1`
- nok: `0`
- denominator: `1`
- quality_rate: `1.0`
- data_sufficiency: `SUPPORTED`

### Process Metrics

`GET /api/v2/process-metrics` for the same scope/window:
- HTTP 200
- status: `PARTIAL`
- reason: `ACCEPTED_FACT_QUERY_OK`
- accepted_event_count: `1` / SUPPORTED
- quality_good_event_count: `1` / SUPPORTED
- quality_rate: `1.0` / SUPPORTED
- unsupported/partial metrics retained their previously accepted authority limits; no false full-OEE authority was introduced.

### Accepted Events API

`GET /api/v2/production/accepted-station-events`:
- HTTP 200
- one returned item
- returned item matches the live WS01 accepted fact above
- next_cursor: null

### Station Summary

Fixed-query Station Summary:
- HTTP 200
- decisive response text included `Station Summary`, `LINE_001`, `WS01`, `SUPPORTED`, `PARTIAL`
- no `Quality source unavailable` or `Process Metrics source unavailable` was observed in the bounded extraction

This establishes the local A1 data chain through the consumer surface. Raw HTML is supporting evidence only; full Owner visual acceptance remains a separate state.

## Mutations and exclusions

Authorized intrinsic runtime writes occurred through existing product code only. No manual SQL DML, seed, fixture, force-NOK, V-PLC parameter mutation, remote copy, sync-worker, source/config edit, build/pull, SSH or Git mutation occurred.

## Protected runtime and Git continuity

After producer containment:
- `edge-mes-postgres`: running / healthy
- `edge-mes-api`: running
- `edge-mes-dashboard`: running / healthy
- accepted fact final count: `1`

Git remained:
- HEAD = origin/main = `6226bf3fb716880a176f9eb642b8139cef3255a6`
- staged `0`
- tracked dirty `0`

## Product conclusion

The local production path is now mechanically demonstrated:

`V-PLC -> Collector accepted decision -> production_accepted_station_event_fact -> API -> Station Summary`

The prior local blockers progressed from missing runtime, to missing image, to missing schema, to empty accepted-fact source, and are now closed for a naturally produced WS01 accepted fact.

This PASS does not claim universal station/history correctness, full OEE authority, remote/local equivalence, or Owner visual acceptance.

## Next gate

Do not immediately reopen the producer. The next product step should choose between:
1. a bounded multi-station production observation sufficient to produce WS02/WS03 facts and exercise skip/NOK semantics naturally, or
2. returning to A1 Owner visual/product review now that real local data exists.

The long-lived untracked corpus remains outside this gate and must be handled by a separate exact-scope reconciliation/retention task; no broad `git add`, `git clean`, delete or adoption is authorized here.
