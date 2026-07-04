# Sprint 3 Collector Ingestion Adapter Gate Status

Updated: 2026-07-04

Purpose: compact current gate/status source for Codex Threads working on Sprint 3 Collector Ingestion Adapter.

Read this file together with:

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- `docs/contracts/collector_ingestion_adapter.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`

## 1. Last verified baseline

```text
live HEAD / origin/main at authoring time:
99dfc265983d757de7c23f6a677cabbc05bc4f5a
99dfc26 Add PM handoff after API DB-backed schema verification

Branch:
main

Phase-1 tag:
phase1-pass-20260619

Phase-2 tag:
not created

Runtime integration:
Slice B runtime adapter gate implemented and committed
Slice C runtime adapter diagnostic observability hardening implemented and committed
Slice D1 raw boundary test-only hardening implemented and committed
Slice D2-A decoder authority docs/contract-only repair implemented and committed
Slice D2-B decoder authority tests-only hardening implemented and committed
Slice D2-C decoder registry authority implemented and committed
Slice D3 runtime raw wiring implemented and committed
Slice E1 runtime raw decoder repair implemented and committed
Slice F1 raw_policy authority docs/contracts freeze implemented and committed
Slice F2 raw_policy raw_capable authority implemented and committed
Slice G WS01 raw_capable post-commit sanity tests-only hardening implemented and committed
Slice H WS02 raw_policy raw_capable authority implemented and committed
Slice I WS03 raw_policy raw_capable authority implemented and committed
Slice J downstream adapter boundary tests-only hardening implemented and committed
Sprint 3 production-fact visibility boundary docs/status/PM-rule commit/push completed at 11cf077
PM handoff after production-fact visibility boundary committed at ffa9348
Adapter production-fact leakage negative tests implemented, reviewed and committed at fd3a799
DB schema field-name contract freeze docs/contracts edit reviewed, committed and pushed at af60328
DB/API/Dashboard Slice 1 schema-only accepted station-event visibility migration committed and pushed at e75f652
DB/API/Dashboard Slice 2 DB write path implemented, reviewed, committed and pushed at 299d28a
DB/API/Dashboard guarded DB-backed accepted fact tests implemented, reviewed, committed and pushed at 636ba37
DB/API/Dashboard API read path contract freeze reviewed, committed and pushed at 2d0918a
DB/API/Dashboard API read path implementation reviewed, committed and pushed at 763b248
DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only implementation reviewed, committed and pushed at b30db5c
PM handoff after DB-backed API read validation tests committed and pushed at b817a9d
DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync committed and pushed at 64d0e12
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD repair committed and pushed at 2cfad5d
PM handoff after API DB-backed schema verification committed and pushed at 99dfc26

Deploy / rollback drill:
not performed
```

Live `HEAD` / `origin/main` are dynamic repository facts and must be checked by
each Thread with `git rev-parse`. The baseline above records the last verified
status sync point at authoring time; later docs-only commits may move `HEAD`
without invalidating this status document.

## 2. Current working tree notes

Current local working tree contains external dirty artifacts. The Sprint 3 implementation files are now tracked in commit `b43a12f`.
R-N1/R-N2 hardening is tracked in commit `577c1a1`.
The docs/status sync is tracked in commit `fd79e21`; the baseline status repair is tracked in commit `4f424c6`; the PM rules / baseline semantics repair pre-baseline is tracked in commit `e284a06`.
Slice A mapping contract hardening is tracked in commit `706f5da`.
Slice B runtime adapter gate is tracked in commit `c677515`.
Slice C runtime adapter diagnostic observability hardening is tracked in commit `e02e39d`.
Slice D1 raw boundary test-only hardening is tracked in commit `0358b60`.
Slice D2-A decoder authority docs/contract-only repair is tracked in commit `2f6294c`.
Slice D2-B decoder authority tests-only hardening is tracked in commit `dafbbf8`.
Slice D2-C decoder registry authority is tracked in commit `5e5a617`.
Slice D3 runtime raw wiring is tracked in commit `c9e7c22`.
Slice E1 runtime raw decoder repair is tracked in commit `2c73410`.
Slice F1 raw_policy authority docs/contracts freeze is tracked in commit `ac1838c`.
Slice F2 raw_policy raw_capable authority is tracked in commit `829d5c7`.
Slice G WS01 raw_capable post-commit sanity tests-only hardening is tracked in commit `398f11c`.
Slice H WS02 raw_policy raw_capable authority is tracked in commit `c7e80e8`.
Slice I WS03 raw_policy raw_capable authority is tracked in commit `045d21c`.
Slice J downstream adapter boundary tests-only hardening is tracked in commit `ed9a61e`.
Sprint 3 production-fact visibility boundary docs/status/PM-rule commit/push is tracked in commit `11cf077`.
PM handoff after production-fact visibility boundary is tracked in commit `ffa9348`.
Tests-only adapter production-fact leakage negative implementation is tracked in commit `fd3a799` after Reliability, Data Quality and Verification reviews passed with recommendations and no blockers.
DB schema field-name contract freeze docs/contracts edit is tracked in commit `af60328` after Reliability, Data Quality and Verification reviews passed with recommendations and no blockers.
DB/API/Dashboard Slice 1 schema-only accepted station-event visibility migration is tracked in commit `e75f652` after Reliability, Data Quality and Verification reviews passed with recommendations and no blockers.
DB/API/Dashboard Slice 2 DB write path is tracked in commit `299d28a` after Architecture, Reliability, Data Quality, Verification, exact commit and exact push gates closed.
DB/API/Dashboard guarded DB-backed accepted fact tests are tracked in commit `636ba37` after planning, Reliability, Data Quality, Verification, HOLD repair, exact commit and exact push gates closed.
DB/API/Dashboard API read path contract freeze is tracked in commit `2d0918a` after Architecture planning, Reliability, Data Quality, Verification planning reviews, docs-only contract freeze, Reliability/Data Quality/Verification contract reviews, exact docs commit and exact push gates closed.
DB/API/Dashboard API read path implementation is tracked in commit `763b248` after Architecture implementation, Reliability, Data Quality, Verification exact allowlist audit, focused tests, exact commit and exact push gates closed.
DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only implementation is tracked in commit `b30db5c` after planning, Reliability, Data Quality, Verification, focused default-skipped harness tests, exact commit and exact push gates closed.
PM handoff after DB-backed API read validation tests is tracked in commit `b817a9d`.
DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync is tracked in commit `64d0e12`.
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD repair is tracked in commit `2cfad5d` after Verification B1 was closed by re-review.
PM handoff after API DB-backed schema verification is tracked in commit `99dfc26`.

Sprint 3 implementation files committed:

```text
collector/app/services/resolved_config_registry.py
collector/app/services/station_event_adapter.py
tests/test_collector_station_event_adapter.py
```

Sprint 3 Slice B runtime adapter gate files committed:

```text
collector/app/services/event_collector.py
collector/app/services/station_event_runtime_source.py
collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py
tests/test_collector_station_event_runtime_source.py
collector/tests/test_event_collector_adapter_gate.py
```

Sprint 3 Slice C runtime adapter diagnostic observability files committed:

```text
collector/app/services/event_collector.py
collector/tests/test_event_collector_adapter_gate.py
```

Sprint 3 Slice D1 raw boundary test-only hardening files committed:

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
tests/test_collector_station_event_runtime_source.py
```

Sprint 3 Slice D2-A decoder authority docs/contract-only repair files committed:

```text
docs/contracts/collector_ingestion_adapter.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

Sprint 3 Slice D2-B decoder authority tests-only hardening files committed:

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
```

Sprint 3 Slice D2-C decoder registry authority files committed:

```text
collector/app/services/decoder_registry.py
collector/app/services/resolved_config_registry.py
tests/test_collector_station_event_adapter.py
```

Sprint 3 Slice D3 runtime raw wiring files committed:

```text
collector/app/plc/mapping.py
collector/app/services/event_collector.py
collector/app/services/resolved_config_registry.py
collector/tests/test_event_collector_adapter_gate.py
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

Sprint 3 Slice E1 runtime raw decoder repair files committed:

```text
collector/app/services/resolved_config_registry.py
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_runtime_source.py
```

Sprint 3 Slice F1 raw_policy authority docs/contracts files committed:

```text
docs/contracts/collector_ingestion_adapter.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

Sprint 3 Slice F2 raw_policy raw_capable authority files committed:

```text
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

Sprint 3 Slice G WS01 raw_capable post-commit sanity tests-only hardening files committed:

```text
tests/test_collector_station_event_runtime_source.py
```

Sprint 3 Slice H WS02 raw_policy raw_capable authority files committed:

```text
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

Sprint 3 Slice I WS03 raw_policy raw_capable authority files committed:

```text
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

Sprint 3 Slice J downstream adapter boundary tests-only hardening files committed:

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
```

Sprint 3 adapter production-fact leakage negative tests files committed:

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
```

DB schema field-name contract freeze docs/contracts files committed:

```text
docs/contracts/collector_ingestion_adapter.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

DB/API/Dashboard Slice 1 schema-only files committed:

```text
db/migrations/007_accepted_station_event_visibility.sql
```

DB/API/Dashboard Slice 2 DB write path files committed:

```text
collector/app/services/accepted_station_event_fact.py
collector/app/services/event_collector.py
collector/app/services/storage.py
collector/tests/test_event_collector_accepted_fact_write_path.py
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
```

DB/API/Dashboard guarded DB-backed accepted fact test files committed:

```text
pytest.ini
collector/tests/conftest.py
collector/tests/test_db_backed_safety.py
collector/tests/test_event_collector_accepted_fact_db_backed.py
collector/tests/test_event_collector_accepted_fact_write_path.py
collector/app/services/accepted_station_event_fact.py
```

DB/API/Dashboard API read path contract freeze files committed:

```text
docs/contracts/dashboard_api_contract.md
```

DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only file committed:

```text
api/tests/test_accepted_station_events_api_db_backed.py
```

External dirty artifacts currently expected and excluded unless PM explicitly says otherwise:

```text
M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

The external artifacts are PM handoff / Keynote / reporting artifacts and are not part of the Sprint 3 technical implementation.

## 3. Sprint 3 slice boundary

Historical first slice name:

```text
Collector ingestion adapter offline fixtures
```

Historical first-slice input/output boundary:

```text
source payload fixture
-> normalized station_event envelope
-> shared validation helpers
-> lifecycle output
-> offline projection metadata
-> adapter diagnostic decision wrapper
```

Explicit non-goals for the historical first slice:

- runtime Collector integration;
- DB write path;
- DB migration;
- FastAPI endpoint;
- Dashboard / Trace UI;
- V-PLC behavior change;
- real PLC pilot;
- Docker/deploy;
- tag;
- rollback.

Current D3 runtime raw wiring boundary:

```text
runtime station db_read(...) bytes
-> raw_bytes on runtime source
-> build_runtime_source_payload() raw_payload={"raw_hex": ...}
-> adapt_source_payload()
-> normalized candidate + adapter decision gate
-> accepted-only existing persist/ACK path
```

D3 does not change DB/API/Dashboard-visible behavior, storage.py, V-PLC
behavior, Docker/deploy/tag/rollback or ACK/read_done ownership.

## 4. Completed gates

| Gate | Result | Blocker |
| --- | --- | --- |
| Docs-only contract planning | PASS | none |
| Reliability review on contract | PASS WITH RECOMMENDATIONS | none |
| Data Quality targeted re-review on contract | PASS WITH RECOMMENDATIONS | none; DQ-B1 CLOSED |
| Verification review on contract | PASS WITH RECOMMENDATIONS | none |
| Docs-only closeout / status sync | PASS | none |
| Final allowlist audit for docs-only commit | PASS | none |
| Docs-only commit/push | PASS | none |
| First implementation slice authorization planning | PASS | none |
| Offline adapter implementation | PASS | none |
| Reliability focused implementation review | PASS WITH RECOMMENDATIONS | none |
| Data Quality focused implementation review | PASS WITH RECOMMENDATIONS | none |
| Verification focused implementation review | PASS WITH RECOMMENDATIONS | none |
| Exact allowlist commit/push | PASS | none |
| R-N1/R-N2 hardening focused reviews | PASS WITH RECOMMENDATIONS | none |
| R-N1/R-N2 exact allowlist commit/push | PASS | none |
| Docs/status sync for R-N1/R-N2 hardening baseline | PASS | none |
| Docs/status baseline repair | PASS | none |
| Slice A mapping contract hardening | PASS | none |
| Slice B runtime adapter gate implementation | PASS | none |
| Slice B Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| Slice B Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| Slice B Verification focused review / allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice B exact allowlist commit/push | PASS | none |
| Slice C diagnostic observability implementation | PASS | none |
| Slice C Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| Slice C Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| Slice C Verification focused review / allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice C exact allowlist commit/push | PASS | none |
| Slice D1 raw boundary test-only hardening implementation | PASS WITH RECOMMENDATIONS | none |
| Slice D1 Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| Slice D1 Data Quality focused review | PASS | none |
| Slice D1 Verification focused review / allowlist audit | PASS | none |
| Slice D1 exact allowlist commit/push | PASS | none |
| Slice D2-A decoder authority docs/contract-only repair | PASS WITH RECOMMENDATIONS | none |
| Slice D2-A Reliability focused review | PASS | none |
| Slice D2-A Data Quality focused review | PASS WITH RECOMMENDATIONS | none; recommendation repaired |
| Slice D2-A Verification focused review | PASS WITH RECOMMENDATIONS | none |
| Slice D2-A exact allowlist commit/push | PASS | none |
| Slice D2-B fixture/test-only decoder authority hardening | PASS WITH RECOMMENDATIONS | none |
| Slice D2-B Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| Slice D2-B Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| Slice D2-B Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice D2-B exact two-file tests-only commit/push | PASS | none |
| Slice D2-C decoder registry authority implementation | PASS WITH RECOMMENDATIONS | none |
| Slice D2-C Reliability implementation review | PASS WITH RECOMMENDATIONS | none |
| Slice D2-C Data Quality implementation review | PASS WITH RECOMMENDATIONS | none |
| Slice D2-C Verification implementation review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice D2-C exact allowlist commit/push | PASS | none |
| Slice D3 runtime raw wiring implementation | PASS WITH RECOMMENDATIONS | none |
| Slice D3 Reliability focused implementation review | PASS WITH RECOMMENDATIONS | none |
| Slice D3 Data Quality focused implementation review | PASS WITH RECOMMENDATIONS | none |
| Slice D3 Verification focused implementation review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice D3 exact allowlist commit/push | PASS | none |
| Slice E1 runtime raw decoder repair implementation | PASS WITH RECOMMENDATIONS | none |
| Slice E1 Reliability focused review | PASS | none |
| Slice E1 Data Quality focused review | PASS | none |
| Slice E1 Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice E1 exact allowlist commit/push | PASS | none |
| Slice F1 raw_policy authority docs/contracts edit | PASS | none |
| Slice F1 Reliability focused review | PASS | none |
| Slice F1 Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| Slice F1 Verification exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice F1 exact docs/contracts commit/push | PASS | none |
| Slice F2 raw_policy raw_capable implementation | PASS | none |
| Slice F2 Reliability focused implementation review | PASS | none |
| Slice F2 Data Quality focused implementation review | PASS | none |
| Slice F2 Verification exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice F2 exact config/test commit/push | PASS | none |
| Slice G WS01 raw_capable post-commit sanity tests-only hardening | PASS | none |
| Slice G Reliability focused review | PASS | none |
| Slice G Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| Slice G Verification exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice G exact tests-only commit/push | PASS | none |
| Slice H WS02 raw_policy raw_capable rollout planning | PASS WITH RECOMMENDATIONS | none |
| Slice H WS02 raw_policy raw_capable implementation | PASS | none |
| Slice H Reliability focused implementation review | PASS WITH RECOMMENDATIONS | none |
| Slice H Data Quality focused implementation review | PASS WITH RECOMMENDATIONS | none |
| Slice H Verification exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice H exact config/test commit/push | PASS | none |
| Slice I WS03 raw_policy raw_capable rollout planning | PASS WITH RECOMMENDATIONS | none |
| Slice I WS03 raw_policy raw_capable implementation | PASS | none |
| Slice I Reliability focused implementation review | PASS | none |
| Slice I Data Quality focused implementation review | PASS | none |
| Slice I Verification exact allowlist audit | PASS | none |
| Slice I exact config/test commit/push | PASS | none |
| Slice J downstream adapter boundary planning | PASS WITH RECOMMENDATIONS | none |
| Slice J tests-only hardening implementation | PASS WITH RECOMMENDATIONS | none |
| Slice J Reliability focused implementation review | PASS WITH RECOMMENDATIONS | none |
| Slice J Data Quality focused implementation review | PASS WITH RECOMMENDATIONS | none |
| Slice J Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Slice J exact tests-only commit/push | PASS | none |
| Accepted production-fact visibility boundary docs/contracts freeze | PASS WITH RECOMMENDATIONS | none |
| Accepted production-fact visibility boundary Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| Accepted production-fact visibility boundary Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| Accepted production-fact visibility boundary Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| Production-fact visibility boundary exact docs/status/PM-rule commit/push | PASS | none |
| PM handoff after production-fact visibility boundary | PASS | none |
| DB/API/Dashboard production visibility planning gate | PASS WITH RECOMMENDATIONS | none |
| Production-fact leakage negative tests planning gate | PASS WITH RECOMMENDATIONS | none |
| Tests-only adapter production-fact leakage negative implementation | PASS WITH RECOMMENDATIONS | none |
| Tests-only adapter production-fact leakage Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| Tests-only adapter production-fact leakage Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| Tests-only adapter production-fact leakage Verification exact allowlist audit / review-sequence closeout | PASS WITH RECOMMENDATIONS | none |
| Tests-only adapter visibility exact-path commit/push | PASS | none |
| DB/API/Dashboard production visibility contract gate | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard implementation planning gate | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard implementation planning Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard implementation planning Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard implementation planning Verification focused review / exact planning allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB schema field-name contract freeze planning gate | PASS WITH RECOMMENDATIONS | none |
| DB schema field-name contract freeze docs/contracts edit | PASS WITH RECOMMENDATIONS | none |
| DB schema field-name contract freeze Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| DB schema field-name contract freeze Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| DB schema field-name contract freeze Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB schema field-name contract freeze exact docs/contracts commit/push | PASS | none |
| DB/API/Dashboard Slice 1 schema-only planning gate | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 1 schema-only implementation gate | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 1 schema-only Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 1 schema-only Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 1 schema-only Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 1 schema-only exact migration commit/push | PASS | none |
| DB/API/Dashboard Slice 2 DB write path Architecture initial planning | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 2 DB write path Reliability first planning review | HOLD | planning repair required and later closed |
| DB/API/Dashboard Slice 2 DB write path Architecture planning repair | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 2 DB write path Reliability planning re-review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 2 DB write path Data Quality planning review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 2 DB write path Verification planning review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 2 DB write path Architecture implementation + focused tests | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 2 DB write path Reliability focused implementation review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 2 DB write path Data Quality focused implementation review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 2 DB write path Verification focused implementation review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard Slice 2 DB write path exact commit gate | PASS | none |
| DB/API/Dashboard Slice 2 DB write path exact push gate | PASS | none |
| DB/API/Dashboard DB-backed/local Postgres hardening test planning gate | PASS TO REVIEW WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/local Postgres hardening test planning Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/local Postgres hardening test planning Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/local Postgres hardening test planning Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard guarded DB-backed accepted fact tests implementation | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard guarded DB-backed accepted fact tests Reliability focused implementation review | HOLD | placeholder coverage overstated; later repaired and closed |
| DB/API/Dashboard guarded DB-backed accepted fact tests HOLD repair | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard guarded DB-backed accepted fact tests Reliability HOLD repair re-review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard guarded DB-backed accepted fact tests Data Quality focused implementation review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard guarded DB-backed accepted fact tests Verification focused implementation review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard guarded DB-backed accepted fact tests exact commit/push | PASS | none |
| DB/API/Dashboard API read path planning gate | PASS TO REVIEW WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path planning Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path planning Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path planning Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path contract freeze docs-only edit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path contract freeze Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path contract freeze Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path contract freeze Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path contract freeze exact docs commit/push | PASS | none |
| DB/API/Dashboard API read path contract freeze post-push docs/status sync | PASS | none |
| PM handoff after API read path contract status sync | PASS | none |
| DB/API/Dashboard API read path implementation planning gate | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path implementation planning Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path implementation planning Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path implementation planning Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path implementation | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path implementation Reliability focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path implementation Data Quality focused review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path implementation Verification focused review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard API read path implementation exact commit/push | PASS | none |
| DB/API/Dashboard DB-backed/live Postgres API Read Validation planning gate | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/live Postgres API Read Validation Reliability planning review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/live Postgres API Read Validation Data Quality planning review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/live Postgres API Read Validation Verification planning review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only implementation | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/live Postgres API Read Validation Reliability implementation review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/live Postgres API Read Validation Data Quality implementation review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/live Postgres API Read Validation Verification implementation review / exact allowlist audit | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard DB-backed/live Postgres API Read Validation exact-path implementation commit/push | PASS | none |
| PM handoff after DB-backed API read validation tests | PASS | none |
| DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync | PASS | none |
| DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Gate | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Reliability Review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Data Quality Review | PASS WITH RECOMMENDATIONS | none |
| DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Verification Review / Exact Future Run Allowlist Audit | HOLD | B1; later repaired and closed |
| DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair | PASS | none |
| DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair Verification Re-review | PASS WITH RECOMMENDATIONS | B1 CLOSED |
| DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair exact-path commit/push | PASS | commit 2cfad5d |
| PM handoff after API DB-backed schema verification | PASS | commit 99dfc26 |
| DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair post-push docs/status sync | PASS | local docs/status-only sync; not committed/pushed by this gate |

Current overall status:

```text
Sprint 3 Collector Ingestion Adapter offline implementation and R-N1/R-N2 hardening: implemented, reviewed, committed and pushed.
Sprint 3 Slice A mapping contract hardening: implemented, reviewed, committed and pushed at 706f5da.
Sprint 3 Slice B runtime adapter gate: implemented, reviewed, committed and pushed at c677515.
Sprint 3 Slice C runtime adapter diagnostic observability hardening: implemented, reviewed, committed and pushed at e02e39d.
Sprint 3 Slice D1 raw boundary test-only hardening: implemented, reviewed, committed and pushed at 0358b60.
Sprint 3 Slice D2-A decoder authority docs/contract-only repair: reviewed, recommendation-repaired, committed and pushed at 2f6294c.
Sprint 3 Slice D2-B fixture/test-only decoder authority hardening: implemented, reviewed, committed and pushed at dafbbf8.
Sprint 3 Slice D2-C decoder registry authority: implemented, reviewed, committed and pushed at 5e5a617.
Sprint 3 Slice D3 runtime raw wiring: implemented, reviewed, committed and pushed at c9e7c22.
Sprint 3 Slice E1 runtime raw decoder repair: implemented, reviewed, committed and pushed at 2c73410.
Sprint 3 Slice F1 raw_policy authority docs/contracts freeze: reviewed, committed and pushed at ac1838c.
Sprint 3 Slice F2 raw_policy raw_capable authority: implemented, reviewed, committed and pushed at 829d5c7.
Sprint 3 Slice G WS01 raw_capable post-commit sanity tests-only hardening: implemented, reviewed, committed and pushed at 398f11c.
Sprint 3 Slice H WS02 raw_policy raw_capable authority: implemented, reviewed, committed and pushed at c7e80e8.
Sprint 3 Slice I WS03 raw_policy raw_capable authority: implemented, reviewed, committed and pushed at 045d21c.
Sprint 3 Slice J downstream adapter boundary tests-only hardening: implemented, reviewed, committed and pushed at ed9a61e.
Sprint 3 accepted production-fact visibility boundary docs/contracts freeze: reviewed with Reliability, Data Quality and Verification PASS WITH RECOMMENDATIONS and no blockers; exact docs/status/PM-rule commit/push completed at 11cf077.
PM handoff after production-fact visibility boundary: committed and pushed at ffa9348.
DB/API/Dashboard production visibility planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Production-fact leakage negative tests planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Tests-only adapter production-fact leakage negative implementation: CLOSED / PASS WITH RECOMMENDATIONS; committed and pushed at fd3a799 / fd3a79901619c9afe664c709834b7e396187f8b2.
Tests-only leakage changed files: collector/tests/test_event_collector_adapter_gate.py and tests/test_collector_station_event_adapter.py.
Tests-only leakage validation: collector/tests/test_event_collector_adapter_gate.py -> 36 passed; tests/test_collector_station_event_adapter.py -> 46 passed; git diff --check PASS.
Tests-only leakage review closeout: Reliability, Data Quality and Verification exact allowlist audit all PASS WITH RECOMMENDATIONS and no blockers.
DB schema field-name contract freeze docs/contracts edit: CLOSED / PASS WITH RECOMMENDATIONS; committed and pushed at af60328 / af60328815821898165ffd5a45aafc9e9c1da705.
DB schema field-name contract freeze review closeout: Reliability, Data Quality and Verification exact allowlist audit all PASS WITH RECOMMENDATIONS and no blockers.
DB schema field-name contract freeze reserves production, diagnostics, audit and review namespaces; diagnostic fields must not use result, defect, quality, pareto or dashboard_state production-like names.
DB/API/Dashboard Slice 1 schema-only migration: CLOSED / PASS WITH RECOMMENDATIONS; committed and pushed at e75f652 / e75f6525f662702e4a6ccc8f8c43d48d001f33ff.
DB/API/Dashboard Slice 1 created `production_accepted_station_event_fact` as a production-only landing surface for accepted station-event business facts.
Slice 1 migration contains no raw payload/raw hex/raw JSON, adapter disposition/reason/candidate context, Quality/Pareto/Grafana/Dashboard state, DML/write path or ACK/read_done ownership.
DB/API/Dashboard Slice 2 DB write path implementation: CLOSED / PASS WITH RECOMMENDATIONS; committed and pushed at 299d28a / 299d28aa5c91b8c3cf7115b6582ce26d45b64706.
Slice 2 added accepted station-event fact write path for `production_accepted_station_event_fact`.
Slice 2 added `accepted_station_event_fact.py` DTO/helper.
Slice 2 added `Storage.transaction()` and no-internal-commit write variants.
Slice 2 accepted path writes production fact + legacy/current persistence in one transaction.
Slice 2 ACK/read_done mutation happens only after successful transaction commit.
Slice 2 non-accepted dispositions create zero production rows and no ACK/read_done mutation for the current payload.
Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
Slice 2 duplicate/conflict/raw_variant/idempotency behavior is implemented and tested with focused fake/spy coverage.
Slice 2 introduced no DB migration, API, Dashboard, V-PLC, config, deploy, tag or rollback changes.
Slice 2 Architecture implementation evidence: collector/tests/test_event_collector_adapter_gate.py -> 36 passed; tests/test_collector_station_event_adapter.py -> 46 passed; collector/tests/test_event_collector_accepted_fact_write_path.py -> 12 passed; compileall collector/app/services -> PASS; git diff --check -> PASS.
Slice 2 Reliability reran focused commands: 36 passed; 46 passed; 12 passed; compileall PASS; git diff --check PASS.
Slice 2 Data Quality ran combined focused tests: 94 passed.
Slice 2 Verification final audit: 94 passed; compileall PASS; git diff --check PASS; cached empty; exact allowlist PASS.
Future DB/API/Dashboard gates must use real production accepted fact table assertions, not synthetic visibility assumptions.
Accepted production-fact visibility boundary limits future visibility to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.
Diagnostic artifacts, raw evidence and non-accepted normalized candidates remain diagnostic/review/debug only, not production facts, Quality/Pareto input, defect detail authority or ACK/read_done authority.
Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
raw_payload/raw_hex is evidence, not a production fact.
Decoded/source normalized payloads remain candidates until accepted.
Non-accepted dispositions do not write defect detail; NOK/detail visibility must bind to accepted upstream business evidence.
API/Dashboard implementation, new migration, deploy, tag, rollback, broad tests and real PLC pilot remain deferred; future gate must restate exact allowlist, review gates and production-fact leakage negative tests.
ACK/read_done ownership remains unchanged, including no ACK/read_done mutation for the current non-accepted payload.
DB/API/Dashboard guarded DB-backed accepted fact tests: CLOSED / PASS WITH RECOMMENDATIONS; committed and pushed at 636ba37 / 636ba375248987b26d4ae68bdbf952d47f398bc8.
Guarded DB-backed tests changed files: pytest.ini, collector/tests/conftest.py, collector/tests/test_db_backed_safety.py, collector/tests/test_event_collector_accepted_fact_db_backed.py, collector/tests/test_event_collector_accepted_fact_write_path.py and collector/app/services/accepted_station_event_fact.py.
Guarded DB-backed tests register db_backed/postgres_local markers, default-skip DB-backed tests unless EDGE_MES_ENABLE_DB_BACKED_TESTS=1, validate test-target and maintenance DSNs before psycopg.connect, and add deterministic migration/schema verification helpers.
Guarded DB-backed direct-storage opt-in tests are pytest-discovered but skipped by default; default focused command produced 33 passed, 7 skipped.
station_result NOK missing accepted business NOK evidence now fails closed in the accepted fact DTO builder before DB insert.
Reliability first implementation review found HOLD because placeholder worker/race/commit/non-accepted coverage overstated the DB-backed matrix; the repair removed placeholder pytest coverage and reclassified those scenarios as future DB-authorized carry-forward work; Reliability re-review, Data Quality review and Verification audit then passed with recommendations and no blockers.
No DB opt-in tests were run, no DB connection was made, and docker compose was not started.
No storage.py, migration 007, API, Dashboard/frontend, V-PLC, config/mapping.yaml, docker-compose.yml, deploy/tag/rollback or docs/status/handoff files changed in the implementation commit.
Carry-forward: worker-level DB-backed accepted rollback, commit failure before ACK, non-accepted DB-backed zero rows + no ACK/read_done mutation, race / unique-violation-after-precheck and post-unique-violation re-read semantics require a future PM-authorized local Postgres harness gate.
Carry-forward: do not treat legacy/current `raw_plc_sample`, `cycle_event`, `station_event`, `production_unit` or `quality_event` as equivalent to production accepted fact surface.
DB/API/Dashboard API read path contract freeze: CLOSED / PASS WITH RECOMMENDATIONS; committed and pushed at 2d0918a / 2d0918adebe5cd29e59177bc2159c7f447cb5c38.
API read path contract changed file: docs/contracts/dashboard_api_contract.md.
API read path contract freezes future GET /api/v2/production/accepted-station-events as a future API contract only, not a current implementation claim.
API read path future endpoint may read only production_accepted_station_event_fact and must not treat raw_plc_sample, cycle_event, station_event, production_unit, quality_event, production_snapshot or production_events as equivalent production fact sources.
API read path response DTO allowlist is limited to accepted station-event business fact fields from production_accepted_station_event_fact; forbidden fields include raw_payload/raw_hex, adapter diagnostics, candidate/normalized/raw comparison context, legacy payload/raw_sample_id, ack_status, read_done, collector_state, dashboard_state, quality_pareto_input and ambiguous result/defect/quality/pareto keys.
API read path query contract requires bounded time window, line_id or explicit server default scope, limit max 500, strict cursor parsing and stable pagination order.
API read path Reliability/Data Quality/Verification contract reviews passed with recommendations and no blockers.
Carry-forward from contract freeze: statement_timeout / idle timeout became implementation MUST; cursor tuple/sorting/tie-breaker and cursor scope/filter/time-window binding were frozen before implementation; api/app/db.py remained conditional and was not changed.
DB/API/Dashboard API read path implementation: CLOSED / PASS WITH RECOMMENDATIONS; committed and pushed at 763b248 / 763b248ca835f59096e73aa5e199a4bf903ac946.
API read path implementation changed files: api/app/main.py, api/app/routes/accepted_station_events.py and api/tests/test_accepted_station_events_api.py.
API read path implementation endpoint: GET /api/v2/production/accepted-station-events.
API read path implementation reads only production_accepted_station_event_fact, exposes only frozen DTO fields, enforces bounded line/time/limit validation, HMAC signed cursor binding, BEGIN READ ONLY, statement_timeout and idle_in_transaction_session_timeout, and keeps no ACK/read_done mutation for the current non-accepted payload.
API read path implementation validation: PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py -> 27 passed; git diff --check PASS.
API read path Reliability/Data Quality/Verification implementation reviews passed with recommendations and no blockers.
Carry-forward: before production deploy, ACCEPTED_STATION_EVENTS_CURSOR_SECRET must be managed as a real deployment secret rather than relying on the development fallback.
DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only implementation: CLOSED / PASS WITH RECOMMENDATIONS; committed and pushed at b30db5c / b30db5cd2bd1d109d83c8da1a222d5ad37517448.
DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync: CLOSED / PASS; committed and pushed at 64d0e12 / 64d0e12dc76898a2da3ce09c2c0e94dbbf33ac80.
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Gate and Reliability/Data Quality planning reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers.
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Verification Review / Exact Future Run Allowlist Audit found HOLD blocker B1.
B1 is CLOSED after HOLD repair and Verification re-review.
HOLD repair exact-path commit/push: PASS at 2cfad5d / 2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e.
PM handoff after API DB-backed schema verification: PASS at 99dfc26 / 99dfc265983d757de7c23f6a677cabbc05bc4f5a.
Current live handoff baseline after the latest PM handoff commit: 99dfc26 / 99dfc265983d757de7c23f6a677cabbc05bc4f5a. The implementation commit synchronized by the earlier docs/status update is b30db5c; the HOLD repair commit synchronized by this docs/status update is 2cfad5d.
DB-backed API read validation changed only api/tests/test_accepted_station_events_api_db_backed.py.
The HOLD repair added API-side pre-insert schema/constraint/column/nullability verification for production_accepted_station_event_fact in api/tests/test_accepted_station_events_api_db_backed.py.
The schema verification checks table existence, DTO/accepted fact columns, nullable / NOT NULL expectations, unique constraints and accepted-fact check constraints.
The schema verification runs after migration apply and before fixture insert in the future live DB-backed execution path.
DB-backed API tests are default skipped unless a future PM-authorized DB opt-in run sets EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
DB-backed API read validation default non-DB focused run before HOLD repair: PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py api/tests/test_accepted_station_events_api_db_backed.py -q -> 27 passed, 32 skipped.
HOLD repair focused GREEN run: 41 passed, 19 skipped.
Collector DB safety focused run after HOLD repair: 20 passed.
DB-backed API read validation and HOLD repair git diff --check -> PASS.
DB-backed API read validation Reliability, Data Quality and Verification implementation reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers.
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
API read path source boundary remains only production_accepted_station_event_fact; raw_plc_sample, cycle_event, station_event, production_unit, quality_event, production_snapshot and production_events must not be described as equivalent production fact sources, fallback sources or join-derived field fillers.
Future production visibility remains limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.
Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
raw_payload/raw_hex is evidence, not a production fact.
Decoded/source normalized payloads remain candidates until accepted.
Non-accepted dispositions do not write defect detail; NOK/detail visibility must bind to accepted upstream business evidence.
Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
Next eligible gate: separately authorized actual DB opt-in / live local Postgres API read validation run, or Dashboard/API consumer planning gate. Actual timeout failure induction remains a separate future gate. Worker/runtime DB-backed gates for unique-violation race, commit-before-ACK, non-accepted DB-backed zero-row/no ACK/read_done mutation, post-conflict re-read semantics and DB rollback remain future authorized work. Deploy/tag/rollback/real PLC pilot require separate PM authorization.
Slice B inserted the adapter gate after payload/cycle/counter guards and counter reset fail-safe, before existing storage.persist_cycle().
Slice B accepted-only path continues to existing storage.persist_cycle() plus existing read_done/ACK behavior.
Slice B non-accepted decisions do not persist, do not project, do not write defect detail, and do not ACK.
Adapter remains non-owner of ACK/read_done.
Slice C adapter exception path records ADAPTER_GATE_FAILED.
Slice C non-accepted decision path records ADAPTER_DECISION_NOT_ACCEPTED.
Slice C diagnostic raw_context includes adapter_phase, adapter_disposition, adapter_error_code and adapter_reason where available.
Slice C collector state remains non-production diagnostic state, for example ADAPTER_REJECTED.
Slice C accepted-only persist path remains unchanged.
Slice C non-accepted decisions still do not persist, do not project, do not write defect detail, and do not ACK.
Slice C introduced no raw evidence runtime wiring and no storage.py, DB/API/Dashboard/V-PLC/deploy changes.
Slice D1 is test-only hardening; no production code changed.
Slice D1 is not raw runtime support.
Slice D1 introduced no schema/config/mapping change, no decoder registry, no raw runtime wiring, no event_collector.py implementation change, and no storage.py / DB / API / Dashboard / V-PLC / Docker / deploy change.
Slice D1 leaves ACK/read_done ownership unchanged.
Slice D1 confirms raw_not_provided normalized-only path remains accepted only under immutable mapping/resolved snapshot authority.
Slice D1 confirms raw_capable/raw_required missing raw fail closed as RAW_EVIDENCE_MISSING.
Slice D1 confirms raw-only rejects as RAW_ONLY_UNSUPPORTED before identity/projection/fingerprint production.
Slice D1 confirms RAW_EVIDENCE_MISSING / RAW_ONLY_UNSUPPORTED / RAW_PARSE_ERROR / RAW_NORMALIZED_MISMATCH / RAW_CONTENT_FORBIDDEN non-accepted decisions assert no persist / no ACK.
Slice D2-A is docs/contract-only and introduced no code, tests, schema/config/mapping change, decoder implementation or runtime raw wiring.
Slice D2-A binds decoder registry identity, decoder id, decoder version, callable decoder, raw_policy and payload template authority to immutable resolved config snapshot / registry snapshot.
Slice D2-A forbids fallback to latest/current runtime config, latest registry, current mapping file, environment defaults or ad hoc fixture fields.
Slice D2-A fail-closed taxonomy includes RAW_PARSE_ERROR, RAW_NORMALIZED_MISMATCH, RAW_CONTENT_FORBIDDEN and RAW_EVIDENCE_MISSING.
Slice D2-A keeps raw_not_provided as the only normalized-only authority and keeps raw_capable/raw_required missing raw fail-closed unless PM later approves a contract change.
Slice D2-A keeps adapter non-owner of ACK/read_done and kept D2-B/D2-C/D3 as separate later gates; D2-B, D2-C and D3 are now closed.
Slice D2-B is tests-only hardening; no production code changed.
Slice D2-B introduced no docs/contracts/plan change in the implementation commit.
Slice D2-B introduced no schema/config/mapping change, no decoder registry/schema implementation, no runtime raw wiring, no DB/API/Dashboard/V-PLC/Docker/deploy change, and no ACK/read_done ownership change.
Slice D2-B coverage includes unknown decoder id current test-only expression, missing callable, callable exception via existing D1 coverage, decoded output mismatch, forbidden raw content, RAW_EVIDENCE_MISSING, raw-only / RAW_ONLY_UNSUPPORTED, raw_capable/raw_required missing raw, normalized-only under immutable raw_not_provided authority, no fallback to latest/current config snapshot, no fallback to latest callable / decoder binding, and non-accepted decisions no projection / no persist / no ACK.
Slice D2-C adds narrow decoder registry authority in collector/app/services/decoder_registry.py.
Slice D2-C adds immutable DecoderRegistrySnapshot / DecoderBinding authority.
Slice D2-C binds decoder registry snapshot identity/content hash to the resolved config snapshot.
Slice D2-C requires decoder id/version/callable binding from immutable registry snapshot.
Slice D2-C fail-closes missing registry, hash mismatch, unknown decoder id, version mismatch, callable missing, callable exception and decoded output mismatch.
Slice D2-C has no fallback to latest/current registry, latest/current config, current mapping file, env defaults or ad hoc fixture callable.
Slice D2-C introduced no D3 runtime raw wiring and no mapping/config/runtime/deploy changes.
Slice D2-C introduced no event_collector.py, station_event_runtime_source.py, storage.py, DB/API/Dashboard/V-PLC/Docker/deploy changes.
Slice D2-C leaves ACK/read_done ownership unchanged.
Slice D3 passes runtime station db_read(...) bytes as raw_bytes into runtime source.
Slice D3 build_runtime_source_payload() generates raw_payload={"raw_hex": ...}.
Slice D3 raw_payload enters adapt_source_payload().
Slice D3 keeps raw evidence as evidence, not production fact.
Slice D3 keeps decoder output as normalized candidate only.
Slice D3 still requires an accepted adapter decision before persist/ACK.
Slice D3 config/mapping.yaml carries decoder_version and decoder_registry snapshot id/content hash.
Slice D3 mapping.py parses, validates and hash-covers authority fields.
Slice D3 resolved_config_registry.py builds immutable decoder registry snapshot binding from runtime mapping.
Slice D3 intends no env/default/latest/ad hoc fallback.
Slice D3 introduced no DB/API/Dashboard-visible behavior change, no storage.py change, no V-PLC behavior change, no Docker/deploy/tag/rollback change and no ACK/read_done ownership change.
Slice E1 repaired the runtime raw decoder by using bytearray.fromhex(raw_hex) as local decode input for decode_read_plan(...).
Slice E1 keeps canonical raw_hex evidence unchanged; bytearray is not persisted evidence or production fact.
Slice E1 keeps nominal Snap7 raw path persist/ACK exactly once and malformed raw / raw-normalized mismatch fail-closed.
Slice E1 introduced no config/mapping.yaml, raw_policy, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy or ACK/read_done ownership change.
Slice F1 freezes raw_policy authority semantics in docs/contracts only.
Slice F1 states runtime code-path capability is not a mapping/config authority upgrade.
Slice F1 keeps current config/mapping.yaml default raw_policy as raw_not_provided and makes future raw_capable/raw_required a separate Level 2 mapping/config authority gate.
Slice F1 keeps RAW_EVIDENCE_MISSING, RAW_PARSE_ERROR and RAW_NORMALIZED_MISMATCH fail-closed.
Slice F1 keeps rejected/diagnostic decisions non-production and not DB/API/Dashboard-visible facts.
Slice F1 introduced no config/mapping.yaml raw_policy actual value change, runtime implementation, tests, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy or ACK/read_done ownership change.
Slice F2 changes only WS01 station-level raw_policy to raw_capable in config/mapping.yaml.
Slice F2 leaves line-wide runtime_defaults unchanged and keeps WS02/WS03 raw_not_provided.
Slice F2 adds real mapping authority test coverage in tests/test_collector_station_event_runtime_source.py.
Slice F2 does not introduce raw_required.
Slice F2 keeps raw_capable missing raw as RAW_EVIDENCE_MISSING fail-closed and keeps RAW_PARSE_ERROR / RAW_NORMALIZED_MISMATCH fail-closed.
Slice F2 introduced no runtime/source code, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy or ACK/read_done ownership change.
Slice G adds tests-only post-commit sanity coverage after Slice F2.
Slice G uses real config/mapping.yaml authority to cover WS01 raw_capable nominal source-builder raw_hex behavior, WS01 missing raw RAW_EVIDENCE_MISSING fail-closed, and WS02/WS03 raw_not_provided normalized-only regression.
Slice G does not modify config/mapping.yaml, runtime/source code, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy or ACK/read_done ownership.
Slice G does not roll out WS02/WS03 raw_capable and does not introduce raw_required.
Slice G Reliability review: PASS.
Slice G Data Quality review: PASS WITH RECOMMENDATIONS, no blocker.
Slice G Verification exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker.
Slice H changes only WS02 station-level raw_policy to raw_capable in config/mapping.yaml.
Slice H leaves line-wide runtime_defaults unchanged and keeps WS01 raw_capable and WS03 raw_not_provided.
Slice H adds real mapping authority test coverage in tests/test_collector_station_event_runtime_source.py for WS02 nominal raw path, WS02 RAW_EVIDENCE_MISSING fail-closed, WS01 regression, WS03 normalized-only regression, line-wide default and config_hash lineage.
Slice H does not introduce raw_required.
Slice H introduced no runtime/source code, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy or ACK/read_done ownership change.
Slice H Reliability review: PASS WITH RECOMMENDATIONS, no blocker.
Slice H Data Quality review: PASS WITH RECOMMENDATIONS, no blocker.
Slice H Verification exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker.
Slice I changes only WS03 station-level raw_policy to raw_capable in config/mapping.yaml.
Slice I leaves line-wide runtime_defaults unchanged and keeps WS01/WS02/WS03 station-level raw_capable.
Slice I adds real mapping authority test coverage in tests/test_collector_station_event_runtime_source.py for three-station station-level raw_capable authority, WS03 nominal raw path, WS03 RAW_EVIDENCE_MISSING fail-closed, WS01/WS02 regression, line-wide default and config_hash lineage.
Slice I does not introduce raw_required.
Slice I introduced no runtime/source code, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy or ACK/read_done ownership change.
Slice I Reliability review: PASS, no blocker.
Slice I Data Quality review: PASS, no blocker.
Slice I Verification exact allowlist audit: PASS, no blocker.
Slice J is tests-only hardening for the frozen downstream adapter decision / diagnostic / projection boundary.
Slice J confirms accepted decisions remain the only path to existing persist/ACK behavior.
Slice J covers rejected / deferred / quarantined / duplicate / conflict / raw_variant under read_done=False and read_done=True.
Slice J requires no persist, no ACK/read_done mutation for the current non-accepted payload, no projection, no defect detail and no production-visible fact for non-accepted payloads.
Slice J keeps raw_variant represented as disposition == "duplicate" plus AuditSubtype.RAW_VARIANT.
Slice J introduced no production code, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, config/mapping.yaml, Docker/deploy or ACK/read_done ownership change.
Slice J Reliability review: PASS WITH RECOMMENDATIONS, no blocker.
Slice J Data Quality review: PASS WITH RECOMMENDATIONS, no blocker.
Slice J Verification exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker.
Docs/status sync completed at fd79e21.
Docs/status baseline repair completed at 4f424c6.
PM rules / baseline semantics repair pre-baseline: e284a06 Repair PM rules and Sprint 3 baseline status.
Eligible for PM handoff readiness or downstream next-slice planning after Slice J docs/status sync: yes.
D3 actual raw-capable/raw-required runtime wiring: CLOSED at c9e7c22.
E1 runtime raw decoder repair: CLOSED at 2c73410 / 2c73410281d1465db166b66ddc23e27d9337b90a.
F1 raw_policy authority docs/contracts freeze: CLOSED at ac1838c / ac1838cbc9378d72da66ace35a200a909f4d5b89.
F2 raw_policy raw_capable authority implementation: CLOSED at 829d5c7 / 829d5c71982b8d22556102b6e67ed9c1e981131d.
Slice G WS01 raw_capable post-commit sanity tests-only hardening: CLOSED at 398f11c / 398f11cfb20717d628d03c0a486a31745fe3030d.
Slice H WS02 raw_policy raw_capable authority implementation: CLOSED at c7e80e8 / c7e80e8e931b5f23d6ea42fee7b10b27191b5e20.
Slice I WS03 raw_policy raw_capable authority implementation: CLOSED at 045d21c / 045d21c14436e8fe13a26bc32b7c2956df0cd99f.
Slice J downstream adapter boundary tests-only hardening: CLOSED at ed9a61e / ed9a61ef2bd8e6be12ad786fd7846f2efcfb0cad.
DB/API/Dashboard/V-PLC/deploy/tag/rollback/real PLC pilot: not authorized.
```

## 5. Implementation summary

Implemented files:

```text
collector/app/services/resolved_config_registry.py
collector/app/services/station_event_adapter.py
tests/test_collector_station_event_adapter.py
```

Implementation characteristics:

- pure offline adapter;
- no runtime Collector import;
- no `Storage` import;
- no DB write;
- no ACK / `read_done` / write-back behavior;
- no Snap7 polling;
- no API/Dashboard/V-PLC/deploy changes;
- uses shared `common.station_event` helpers for parsing, validation, lifecycle, projection and fingerprints.

Slice B runtime adapter gate characteristics:

- runtime adapter gate inserted in `EventCollectorWorker._process_station()`;
- insertion point is after `payload_ready` / `cycle_valid` / `cycle_counter`
  guard and `CounterDecision.RESET` fail-safe, before existing
  `storage.persist_cycle()`;
- accepted adapter/shared validation decision is required before the existing
  `storage.persist_cycle()` path;
- rejected, deferred, quarantined, duplicate, conflict and raw_variant decisions
  do not call `storage.persist_cycle()`, do not project, do not write defect
  detail, and do not ACK;
- ACK/read_done ownership remains with the existing EventCollectorWorker
  handshake path after accepted-only persist success;
- no `storage.py`, DB migration, API, Dashboard, V-PLC, deploy, tag, rollback
  or real PLC pilot changes.

Slice C runtime adapter diagnostic observability characteristics:

- adapter exception diagnostics remain on the existing collector error path and
  record `ADAPTER_GATE_FAILED`;
- non-accepted adapter decision diagnostics remain on the existing collector
  error path and record `ADAPTER_DECISION_NOT_ACCEPTED`;
- diagnostic `raw_context` includes `adapter_phase`, `adapter_disposition`,
  `adapter_error_code` and `adapter_reason` where available;
- collector state remains a non-production diagnostic state such as
  `ADAPTER_REJECTED`;
- accepted-only persist path remains unchanged;
- rejected, deferred, quarantined, duplicate, conflict and raw_variant decisions
  still do not call `storage.persist_cycle()`, do not project, do not write
  defect detail, and do not ACK;
- adapter remains non-owner of ACK/read_done;
- no raw evidence runtime wiring was introduced;
- no `storage.py`, DB migration, API, Dashboard, V-PLC, deploy, tag, rollback
  or real PLC pilot changes.

## 6. Required validation commands

Last observed validation results before exact allowlist commit:

```text
focused adapter tests: 26 passed
station_event + line_config regression: 205 passed
collector runtime reliability regression: 6 passed
compileall collector/app/services: PASS
git diff --check: PASS
trailing whitespace scan on implementation files: PASS
```

Last observed Slice B validation results before exact allowlist commit:

```text
collector runtime adapter/reliability regression: 18 passed
runtime source + adapter regression: 59 passed
compileall collector/app/plc collector/app/services: PASS
git diff --check: PASS
git diff --cached --check: PASS
```

Last observed Slice C validation results before exact allowlist commit:

```text
collector runtime adapter/reliability regression: 19 passed
runtime source + adapter regression: 59 passed
compileall collector/app/plc collector/app/services: PASS
git diff --check: PASS
git diff --cached --check: PASS
```

Last observed Slice D1 validation results before exact allowlist commit:

```text
D1 focused tests: 84 passed
collector reliability + Snap7 regression: 7 passed
git diff --check: PASS
git diff --cached --check: PASS
```

Last observed Slice D2-B validation results before exact allowlist commit:

```text
D2-B focused tests: 57 passed
runtime source regression: 35 passed
collector reliability + Snap7 regression: 7 passed
git diff --check: PASS
git diff --cached --check: PASS
```

Last observed Slice D2-C validation results before exact allowlist commit:

```text
focused adapter tests: 43 passed
collector adapter gate regression: 22 passed
runtime source regression: 35 passed
compileall collector/app/services: PASS
git diff --check: PASS
git diff --cached --check: PASS
```

Last observed Slice D3 validation/review results before exact allowlist commit:

```text
Architecture / Integration implementation: PASS WITH RECOMMENDATIONS
Reliability focused implementation review: PASS WITH RECOMMENDATIONS
Data Quality focused implementation review: PASS WITH RECOMMENDATIONS
Verification focused implementation review / exact allowlist audit: PASS WITH RECOMMENDATIONS
git diff --check: PASS
git diff --cached --check: PASS
```

Last observed Slice E1 validation/review results before exact allowlist commit:

```text
Architecture / Integration implementation: PASS WITH RECOMMENDATIONS
Reliability focused review: PASS
Data Quality focused review: PASS
Verification focused review / exact allowlist audit: PASS WITH RECOMMENDATIONS
collector/tests/test_snap7_reliability_integration.py -> 1 passed
collector/tests/test_event_collector_adapter_gate.py -> 30 passed
collector/tests/test_event_collector_reliability.py -> 6 passed
tests/test_collector_station_event_runtime_source.py -> 45 passed
tests/test_collector_station_event_adapter.py -> 43 passed
compileall collector/app/plc collector/app/services -> PASS
git diff --check: PASS
```

Last observed Slice I validation/review results before exact allowlist commit:

```text
Architecture / Integration implementation: PASS
Reliability focused review: PASS
Data Quality focused review: PASS
Verification focused review / exact allowlist audit: PASS
TDD red check before config change: 3 failed, 49 passed; failures showed WS03 still raw_not_provided
focused runtime source tests: 52 passed
adjacent adapter gate regression: 30 passed
git diff --check: PASS
git diff --cached --check before commit: PASS
```

For future hardening or next-slice work, rerun the relevant focused and regression tests before staging.

## 7. Exact commit allowlist history

The exact allowlist commit has already been completed. The only files committed in `b43a12f` were:

```text
collector/app/services/resolved_config_registry.py
collector/app/services/station_event_adapter.py
tests/test_collector_station_event_adapter.py
```

Commit message used:

```text
Implement Sprint 3 collector ingestion adapter offline slice
```

The R-N1/R-N2 hardening exact allowlist commit has also been completed. The only files committed in `577c1a1` were:

```text
collector/app/services/resolved_config_registry.py
collector/app/services/station_event_adapter.py
tests/test_collector_station_event_adapter.py
```

Commit message used:

```text
Harden Sprint 3 collector adapter recommendations
```

The Slice B runtime adapter gate exact allowlist commit has also been completed. The only files committed in `c677515` were:

```text
collector/app/services/event_collector.py
collector/app/services/station_event_runtime_source.py
collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py
tests/test_collector_station_event_runtime_source.py
collector/tests/test_event_collector_adapter_gate.py
```

Commit message used:

```text
Implement Sprint 3 Slice B runtime adapter gate
```

The Slice C runtime adapter diagnostic observability exact allowlist commit has
also been completed. The only files committed in `e02e39d` were:

```text
collector/app/services/event_collector.py
collector/tests/test_event_collector_adapter_gate.py
```

Commit message used:

```text
Harden Sprint 3 adapter diagnostics
```

The Slice D1 raw boundary test-only hardening exact allowlist commit has also
been completed. The only files committed in `0358b60` were:

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
tests/test_collector_station_event_runtime_source.py
```

Commit message used:

```text
Harden Sprint 3 Slice D1 raw boundary tests
```

The Slice D2-B decoder authority tests-only hardening exact allowlist commit has
also been completed. The only files committed in `dafbbf8` were:

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
```

Commit message used:

```text
Harden Sprint 3 Slice D2-B decoder authority tests
```

The Slice D2-C decoder registry authority exact allowlist commit has also been
completed. The only files committed in `5e5a617` were:

```text
collector/app/services/decoder_registry.py
collector/app/services/resolved_config_registry.py
tests/test_collector_station_event_adapter.py
```

Commit message used:

```text
Implement Sprint 3 Slice D2-C decoder registry authority
```

The Slice D3 runtime raw wiring exact allowlist commit has also been completed.
The only files committed in `c9e7c22` were:

```text
collector/app/plc/mapping.py
collector/app/services/event_collector.py
collector/app/services/resolved_config_registry.py
collector/tests/test_event_collector_adapter_gate.py
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

Commit message used:

```text
Implement Sprint 3 Slice D3 runtime raw wiring
```

The Slice E1 runtime raw decoder repair exact allowlist commit has also been
completed. The only files committed in `2c73410` were:

```text
collector/app/services/resolved_config_registry.py
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_runtime_source.py
```

Commit message used:

```text
Repair Sprint 3 Slice E1 runtime raw decoder
```

Slice C carry-forward recommendations:

```text
R-N1: future raw-capable/raw-required runtime source still needs separate raw evidence focused review.
R-N2: diagnostic enrichment must remain non-owner of ACK/read_done.
R-N3: adapter_reason must remain read-only diagnostic if later used for metrics/alerting/retry policy; it must not become a production success, PLC release, or ACK retry criterion.
DQ-N1: metrics/alerting should use adapter_phase / adapter_error_code as observability dimensions and must not reuse NOK code, quality result, or production outcome naming.
Next gate: eligible for downstream PM planning; raw evidence runtime wiring, DB/API/Dashboard/V-PLC/deploy/tag/rollback/real PLC pilot and further runtime implementation require separate PM approval.
```

Slice D1 carry-forward recommendations:

```text
D2 decoder registry / decoder callable authority remains separate.
D3 actual raw-capable/raw-required runtime wiring later closed at c9e7c22.
raw_capable/raw_required missing raw remains fail-closed unless PM approves contract change.
Adapter diagnostics remain read-only observability, not ACK policy or production policy.
No schema/config/mapping/storage/API/Dashboard/V-PLC/deploy work without separate PM approval.
```

Slice D2-A carry-forward recommendations:

```text
D2-B fixture/test-only decoder authority hardening is implemented, reviewed, committed and pushed at dafbbf8.
D2-C full decoder registry/schema lookup for unknown decoder id / version mismatch / callable binding is implemented, reviewed, committed and pushed at 5e5a617.
D3 runtime raw wiring is implemented, reviewed, committed and pushed at c9e7c22.
If diagnostic evidence later enters metrics/alerting, avoid production fact, NOK code, Quality/Pareto outcome naming.
Adapter remains non-owner of ACK/read_done.
No DB/API/Dashboard/V-PLC/deploy/tag/rollback/real PLC pilot is authorized.
```

Slice D2-C carry-forward recommendations:

```text
D3 runtime raw wiring remained a separate PM-authorized gate after D2-C and is now closed at c9e7c22.
D2-C PASS alone did not prove runtime raw support; D3 c9e7c22 is the runtime raw wiring closure.
Keep rejected-decision normalized_event/canonical_bytes/fact_key diagnostic-only, not production fact or Quality/Pareto/API-visible state.
Registry failures currently surface as RAW_PARSE_ERROR rather than dedicated decoder-authority public codes; this is non-blocking unless PM opens a future taxonomy gate.
No runtime raw wiring, mapping/config/runtime/deploy, DB/API/Dashboard/V-PLC/deploy/tag/rollback or ACK/read_done ownership change was authorized by D2-C alone.
```

Slice D3 carry-forward recommendations:

```text
current config/mapping.yaml runtime default still uses raw_policy: raw_not_provided; D3 runtime code path always passes raw_bytes=data, so this is not a blocker.
If PM later wants runtime source policy explicitly changed to raw_capable/raw_required, it needs a separate mapping/config authority change and review.
Next technical gate should not expand DB/API/Dashboard/V-PLC/storage.py/ACK/deploy without separate PM authorization.
```

Slice E1 carry-forward recommendations:

```text
E1 is closed at 2c73410 as a narrow runtime raw decoder repair after Slice E HOLD.
E1 does not authorize config/mapping.yaml, raw_policy, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy or ACK/read_done ownership changes.
Future raw_policy change from raw_not_provided to raw_capable/raw_required requires a separate Level 2 mapping/config authority gate.
Current eligible next step is PM handoff readiness or next slice planning, not immediate DB/API/Dashboard/V-PLC/deploy.
```

Required exclusions for future tasks remain:

```text
.gitignore
docs/thread_handoff/pm_operating_rules.md
docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
docs/reports/phase1_to_sprint2_management_keynote_10p.html
docs/thread_handoff/chatgpt_pm_handoff_20260624.md
docs/thread_handoff/chatgpt_pm_handoff_20260625.md
docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

Do not stage or commit any docs/runtime/deploy artifacts unless PM explicitly changes a future task allowlist.

## 8. Recommendation hardening status

The previous R-N1/R-N2 recommendations are closed by the `577c1a1` hardening commit. They were not blockers for the original offline adapter commit and remain non-blocker hardening history.

| ID | Status |
| --- | --- |
| R-N1 / DQ-N1 / V-N1 | CLOSED. Resolved snapshot content hash self-check implemented; tampered snapshot content with unchanged `config_hash` field rejects as `CONFIG_HASH_MISMATCH`. |
| R-N2 / DQ-N2 / V-N2 | CLOSED. Route predecessor mismatch and non-`30003/system_reserved` direct parent mismatch fixtures are split and named clearly. |

Suggested handling:

- preserve the closed recommendation history for later review context;
- do not treat these closed recommendations as blockers;
- runtime Collector integration beyond the Slice B adapter gate remains
  unauthorized unless PM explicitly approves the next runtime slice.

## 9. Slice B carry-forward recommendations

These recommendations are not blockers for the `c677515` Slice B commit:

| ID | Status |
| --- | --- |
| R-N1 | Carry forward. Future raw-capable/raw-required runtime source needs renewed raw evidence focused review. |
| R-N2 | Carry forward. Future diagnostic enrichment may split `ADAPTER_GATE_FAILED` vs non-accepted decisions, without changing ACK or production fact semantics. |

## 10. Future prompt minimization

Future Codex prompts for Sprint 3 can be short. They should tell the Thread to read:

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- this gate status file
- the task-specific contract/report files

Then provide only the immediate task, exact allowlist if any, and expected report format.
