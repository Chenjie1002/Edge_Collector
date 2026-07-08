# 当前状态 / Codex 恢复上下文

更新时间：2026-07-08
工作目录：`/Users/chenjie/Documents/MES/edge-mes-demo`
树莓派部署目录：`/opt/edge-mes-demo`

## 0. 当前 PM / Codex 协作状态

当前主线：Phase-2 Sprint 3 Dashboard accepted-events apiClient focused no-DB tests post-push docs/status sync。

Last verified baseline before this docs/status sync:

```text
live HEAD / origin/main at authoring time:
96c0928970d9917e0a4142569ebbc8459d67cc3d
96c0928 Add focused accepted-events API client tests

branch:
main

tag:
phase1-pass-20260619
```

Note: live `HEAD` / `origin/main` must be checked with `git rev-parse` in each
Thread. This durable baseline is an audit marker from the status sync time, not
a requirement that the document hash exactly match `HEAD` after later docs-only
commits.

当前 Sprint 3 gate：

```text
Slice D2-B fixture/test-only decoder authority hardening: PASS WITH RECOMMENDATIONS
Slice D2-B implementation: PASS WITH RECOMMENDATIONS
Slice D2-B Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice D2-B Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice D2-B Verification focused review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice D2-B exact two-file tests-only commit/push: PASS, commit dafbbf8
Slice D3 runtime raw wiring implementation: PASS WITH RECOMMENDATIONS
Slice D3 Reliability focused implementation review: PASS WITH RECOMMENDATIONS, no blocker
Slice D3 Data Quality focused implementation review: PASS WITH RECOMMENDATIONS, no blocker
Slice D3 Verification focused implementation review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice D3 exact allowlist commit/push: PASS, commit c9e7c22
Slice E1 runtime raw decoder repair implementation: PASS WITH RECOMMENDATIONS
Slice E1 Reliability focused review: PASS, no blocker
Slice E1 Data Quality focused review: PASS, no blocker
Slice E1 Verification focused review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice E1 exact allowlist commit/push: PASS, commit 2c73410
Slice F1 raw_policy authority docs/contracts edit: PASS
Slice F1 Reliability focused review: PASS, no blocker
Slice F1 Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice F1 Verification exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice F1 exact docs/contracts commit/push: PASS, commit ac1838c
Slice F2 raw_policy raw_capable implementation: PASS
Slice F2 Reliability focused implementation review: PASS, no blocker
Slice F2 Data Quality focused implementation review: PASS, no blocker
Slice F2 Verification exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice F2 exact config/test commit/push: PASS, commit 829d5c7
Slice G WS01 raw_capable post-commit sanity tests-only hardening: PASS
Slice G Reliability focused review: PASS, no blocker
Slice G Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice G Verification exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice G exact tests-only commit/push: PASS, commit 398f11c
Slice H WS02 raw_policy raw_capable rollout planning: PASS WITH RECOMMENDATIONS
Slice H WS02 raw_policy raw_capable implementation: PASS
Slice H Reliability focused implementation review: PASS WITH RECOMMENDATIONS, no blocker
Slice H Data Quality focused implementation review: PASS WITH RECOMMENDATIONS, no blocker
Slice H Verification exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice H exact config/test commit/push: PASS, commit c7e80e8
Slice I WS03 raw_policy raw_capable rollout planning: PASS WITH RECOMMENDATIONS
Slice I WS03 raw_policy raw_capable implementation: PASS
Slice I Reliability focused implementation review: PASS, no blocker
Slice I Data Quality focused implementation review: PASS, no blocker
Slice I Verification exact allowlist audit: PASS, no blocker
Slice I exact config/test commit/push: PASS, commit 045d21c
Slice J downstream adapter decision / diagnostic / projection boundary planning: CLOSED / PASS WITH RECOMMENDATIONS
Slice J tests-only hardening implementation: CLOSED / PASS WITH RECOMMENDATIONS
Slice J Reliability focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Slice J Data Quality focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Slice J Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Slice J exact tests-only commit/push: PASS, commit ed9a61e
Sprint 3 accepted production-fact visibility boundary docs/contracts freeze: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 accepted production-fact visibility boundary Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Sprint 3 accepted production-fact visibility boundary Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Sprint 3 accepted production-fact visibility boundary Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Sprint 3 production-fact visibility boundary exact docs/status/PM-rule commit/push: PASS, commit 11cf077
PM handoff after production-fact visibility boundary: PASS, commit ffa9348
DB/API/Dashboard production visibility planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Production-fact leakage negative tests planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Tests-only adapter production-fact leakage negative implementation: CLOSED / PASS WITH RECOMMENDATIONS
Tests-only adapter production-fact leakage Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Tests-only adapter production-fact leakage Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Tests-only adapter production-fact leakage Verification exact allowlist audit / review-sequence closeout: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Tests-only adapter visibility exact-path commit/push: PASS, commit fd3a799
DB/API/Dashboard production visibility contract gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard implementation planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard implementation planning Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard implementation planning Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard implementation planning Verification focused review / exact planning allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB schema field-name contract freeze planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB schema field-name contract freeze docs/contracts edit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB schema field-name contract freeze Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB schema field-name contract freeze Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB schema field-name contract freeze Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB schema field-name contract freeze exact docs/contracts commit/push: PASS, commit af60328
DB/API/Dashboard Slice 1 schema-only planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 1 schema-only implementation gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 1 schema-only Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 1 schema-only Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 1 schema-only Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 1 schema-only exact migration commit/push: PASS, commit e75f652
DB/API/Dashboard Slice 2 DB write path Architecture initial planning: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 2 DB write path Reliability first planning review: CLOSED / HOLD
DB/API/Dashboard Slice 2 DB write path Architecture planning repair: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 2 DB write path Reliability planning re-review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 2 DB write path Data Quality planning review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 2 DB write path Verification planning review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 2 DB write path Architecture implementation + focused tests: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 2 DB write path Reliability focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 2 DB write path Data Quality focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 2 DB write path Verification focused implementation review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard Slice 2 DB write path exact commit gate: PASS, commit 299d28a
DB/API/Dashboard Slice 2 DB write path exact push gate: PASS, commit 299d28a
DB/API/Dashboard DB-backed/local Postgres hardening test planning gate: CLOSED / PASS TO REVIEW WITH RECOMMENDATIONS
DB/API/Dashboard DB-backed/local Postgres hardening test planning Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/local Postgres hardening test planning Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/local Postgres hardening test planning Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard guarded DB-backed accepted fact tests implementation: CLOSED / PASS WITH RECOMMENDATIONS
DB/API/Dashboard guarded DB-backed accepted fact tests Reliability focused implementation review: CLOSED / HOLD; blocker repaired and closed by re-review
DB/API/Dashboard guarded DB-backed accepted fact tests HOLD repair: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard guarded DB-backed accepted fact tests Reliability HOLD repair re-review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard guarded DB-backed accepted fact tests Data Quality focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard guarded DB-backed accepted fact tests Verification focused implementation review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard guarded DB-backed accepted fact tests exact commit/push: PASS, commit 636ba37
DB/API/Dashboard API read path planning gate: CLOSED / PASS TO REVIEW WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path planning Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path planning Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path planning Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path contract freeze docs-only edit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path contract freeze Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path contract freeze Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path contract freeze Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path contract freeze exact docs commit/push: PASS, commit 2d0918a
DB/API/Dashboard API read path contract freeze post-push docs/status sync: PASS, commit 2da0a75
PM handoff after API read path contract status sync: PASS, commit 4648734
DB/API/Dashboard API read path implementation planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation planning Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation planning Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation planning Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API read path implementation exact commit/push: PASS, commit 763b248
DB/API/Dashboard DB-backed/live Postgres API Read Validation planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Reliability planning review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Data Quality planning review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Verification planning review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only implementation: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Reliability implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Data Quality implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation Verification implementation review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard DB-backed/live Postgres API Read Validation exact-path implementation commit/push: PASS, commit b30db5c
PM handoff after DB-backed API read validation tests: PASS, commit b817a9d
DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync: PASS, commit 64d0e12
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Reliability Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Data Quality Review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Verification Review / Exact Future Run Allowlist Audit: CLOSED / HOLD, blocker B1
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair: CLOSED / PASS, no blocker
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair Verification Re-review: CLOSED / PASS WITH RECOMMENDATIONS, blocker B1 CLOSED
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair exact-path commit/push: PASS, commit 2cfad5d
PM handoff after API DB-backed schema verification: PASS, commit 99dfc26
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD Repair post-push docs/status sync: PASS, local docs/status-only sync; not committed/pushed by this gate
DB-backed API validation harness tests/harness-only repair: CLOSED / PASS, commit 8a8004c
Remote existing PostgreSQL DB-backed API validation rerun with repaired RecordingConnection proxy: CLOSED / PASS, focused pytest 62 passed in 8.68s, test_db_cleanup_ok edge_mes_test_api_read
PM handoff after DB-backed validation harness repair: PASS, commit 5543c87
DB/API/Dashboard consumer planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard consumer planning Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard consumer planning Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard consumer planning Verification focused review / exact planning allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard consumer planning exact planning doc commit/push: PASS, commit f4de1c3
PM handoff after consumer planning: PASS, commit cd6dff8
DB/API/Dashboard API consumer contract freeze gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API consumer contract freeze Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API consumer contract freeze Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API consumer contract freeze Verification focused review / exact contract allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API consumer contract freeze exact contract commit/push: PASS, commit f65a120
DB/API/Dashboard API implementation planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API implementation planning Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API implementation planning Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API implementation planning Verification focused review / exact future implementation allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard API implementation planning exact-path commit/push: PASS, commit 2dc4b4d
DB/API/Dashboard accepted station events API implementation gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard accepted station events API implementation Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard accepted station events API implementation Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard accepted station events API implementation Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
DB/API/Dashboard accepted station events API implementation exact-path commit/push: PASS, commit 97dc4d5
DB-backed API validation planning exact-path commit/push: PASS, commit 78ce29b
DB-backed API validation first SSH-tunnel execution: CLOSED / HOLD, focused pytest 1 failed and 87 passed; controlled failure assertion expected 500 but route returned 503
DB-backed API validation focused repair exact-path commit/push: PASS, commit 1d040a6
PM handoff after DB-backed repair: PASS, commit a0042fb
DB-backed API validation execution rerun with SSH tunnel DSNs: CLOSED / PASS WITH RECOMMENDATIONS, focused pytest 88 passed in 12.94s
DB-backed API validation post-execution docs/status sync: PASS, commit ba02249
Dashboard/API implementation planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard/API implementation planning Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard/API implementation planning Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard/API implementation planning Verification focused review / exact future implementation allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard/API implementation planning exact-path commit/push: PASS, commit 4fcdd66
Dashboard/API implementation planning post-push docs/status sync: PASS, local docs/status-only sync; not committed/pushed by this gate
Dashboard implementation preparation / allowlist gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard implementation preparation / allowlist exact-path commit/push: PASS, commit 4ad0e91
Dashboard accepted-events frontend implementation: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events frontend implementation Reliability focused review: initial HOLD for B1 missing query fallback and B2 package-local validation reproducibility; HOLD repair CLOSED / PASS WITH RECOMMENDATIONS; re-review CLOSED / PASS WITH RECOMMENDATIONS, B1/B2 CLOSED
Dashboard accepted-events frontend implementation Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events frontend implementation Verification focused review: initial HOLD for V-B1 npm run build mutating frontend/tsconfig.json by adding "incremental": true; HOLD repair CLOSED / PASS WITH RECOMMENDATIONS; re-review CLOSED / PASS WITH RECOMMENDATIONS, V-B1 CLOSED
Dashboard accepted-events frontend exact-path commit/push: PASS, commit 896c2d1
Dashboard accepted-events frontend post-push docs/status sync: PASS, commit 42ccd32
PM handoff after Dashboard frontend closeout: PASS, commit f433c92
Dashboard accepted-events vertical validation planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events vertical validation Reliability planning review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events vertical validation Data Quality planning review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events vertical validation Verification planning review / exact future run allowlist audit: CLOSED / HOLD, blockers B1/B2/B3
Dashboard accepted-events vertical validation planning HOLD repair: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events vertical validation Verification planning HOLD repair re-review: CLOSED / PASS WITH RECOMMENDATIONS, blockers B1/B2/B3 CLOSED
Dashboard accepted-events vertical validation planning exact-path commit/push: PASS, commit dd6dc53
Dashboard accepted-events vertical validation post-push docs/status sync: PASS, commit b7ce52b
PM handoff after Dashboard vertical validation sync: PASS, commit 8b2e7a0
Dashboard frontend no-DB validation environment prep gate: CLOSED / PASS; `npm ci` completed; `frontend/node_modules/` is local dependency artifact only, not staged and not a tracked diff
Dashboard accepted-events no-DB vertical validation execution: CLOSED / PASS WITH RECOMMENDATIONS
Dashboard accepted-events no-DB vertical validation Architecture execution: PASS; 4 focused frontend files / 19 tests passed
Dashboard accepted-events no-DB vertical validation Verification review / exact evidence audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events no-DB vertical validation Data Quality review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events no-DB vertical validation Reliability review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events apiClient focused no-DB test planning gate: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events apiClient focused no-DB tests implementation: CLOSED / PASS
Dashboard accepted-events apiClient focused no-DB tests Reliability review: CLOSED / PASS, no blocker
Dashboard accepted-events apiClient focused no-DB tests Data Quality review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events apiClient focused no-DB tests Verification review / exact evidence audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Dashboard accepted-events apiClient focused no-DB tests exact-path commit/push: PASS, commit 96c0928
Slice D2-C decoder registry authority implementation: PASS WITH RECOMMENDATIONS
Slice D2-C Reliability implementation review: PASS WITH RECOMMENDATIONS, no blocker
Slice D2-C Data Quality implementation review: PASS WITH RECOMMENDATIONS, no blocker
Slice D2-C Verification implementation review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice D2-C exact allowlist commit/push: PASS, commit 5e5a617
Slice D2-A decoder authority docs/contract-only repair: PASS WITH RECOMMENDATIONS, closed after recommendation repair
Slice D2-A Reliability focused review: PASS, no blocker
Slice D2-A Data Quality focused review: PASS WITH RECOMMENDATIONS, recommendation repaired, no blocker
Slice D2-A Verification focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice D2-A exact allowlist commit/push: PASS, commit 2f6294c
Slice D1 raw boundary test-only hardening implementation: PASS WITH RECOMMENDATIONS
Slice D1 Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice D1 Data Quality focused review: PASS, no blocker
Slice D1 Verification focused review / allowlist audit: PASS, no blocker
Slice D1 exact allowlist commit/push: PASS, commit 0358b60
Slice C runtime adapter diagnostic observability implementation: PASS
Slice C Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice C Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice C Verification focused review / allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice C exact allowlist commit/push: PASS, commit e02e39d
Slice B runtime adapter gate implementation: PASS
Slice B Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice B Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Slice B Verification focused review / allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice B exact allowlist commit/push: PASS, commit c677515
Slice A mapping contract hardening: PASS, commit 706f5da
Offline adapter implementation: PASS
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Verification focused review: PASS WITH RECOMMENDATIONS, no blocker
Exact allowlist commit/push: PASS, commit b43a12f
R-N1/R-N2 hardening commit/push: PASS, commit 577c1a1
Docs/status sync: PASS, commit fd79e21
Docs/status baseline repair: PASS, commit 4f424c6
PM rules / baseline semantics repair: PASS, commit e284a06
Eligible for downstream DB/API/Dashboard planning gate, likely API read path or DB-backed hardening tests, after Slice 2 DB write path push: yes
D3 docs/status sync exact allowlist: completed after implementation commit c9e7c22
D3 actual raw-capable/raw-required runtime wiring: CLOSED at c9e7c22
E1 runtime raw decoder repair: CLOSED at 2c73410 / 2c73410281d1465db166b66ddc23e27d9337b90a
F1 raw_policy authority docs/contracts freeze: CLOSED at ac1838c / ac1838cbc9378d72da66ace35a200a909f4d5b89
F2 raw_policy raw_capable authority implementation: CLOSED at 829d5c7 / 829d5c71982b8d22556102b6e67ed9c1e981131d
Slice G WS01 raw_capable post-commit sanity tests-only hardening: CLOSED at 398f11c / 398f11cfb20717d628d03c0a486a31745fe3030d
Slice H WS02 raw_policy raw_capable authority implementation: CLOSED at c7e80e8 / c7e80e8e931b5f23d6ea42fee7b10b27191b5e20
Slice I WS03 raw_policy raw_capable authority implementation: CLOSED at 045d21c / 045d21c14436e8fe13a26bc32b7c2956df0cd99f
Slice J downstream adapter boundary tests-only hardening: CLOSED at ed9a61e / ed9a61ef2bd8e6be12ad786fd7846f2efcfb0cad
Sprint 3 accepted production-fact visibility boundary docs/contracts freeze: CLOSED / PASS WITH RECOMMENDATIONS; Reliability, Data Quality and Verification focused reviews CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Tests-only adapter production-fact leakage negative implementation: CLOSED at fd3a799 / fd3a79901619c9afe664c709834b7e396187f8b2
DB schema field-name contract freeze docs/contracts edit: CLOSED at af60328 / af60328815821898165ffd5a45aafc9e9c1da705 after Reliability, Data Quality and Verification focused reviews passed with recommendations and no blockers.
DB/API/Dashboard Slice 1 schema-only accepted station-event visibility migration: CLOSED at e75f652 / e75f6525f662702e4a6ccc8f8c43d48d001f33ff after Reliability, Data Quality and Verification focused reviews passed with recommendations and no blockers.
DB/API/Dashboard Slice 2 DB write path: CLOSED at 299d28a / 299d28aa5c91b8c3cf7115b6582ce26d45b64706 after Architecture, Reliability, Data Quality, Verification, exact commit and exact push gates closed.
DB/API/Dashboard guarded DB-backed accepted fact tests: CLOSED at 636ba37 / 636ba375248987b26d4ae68bdbf952d47f398bc8 after planning, Reliability, Data Quality, Verification, HOLD repair, exact commit and exact push gates closed.
DB/API/Dashboard API read path contract freeze: CLOSED at 2d0918a / 2d0918adebe5cd29e59177bc2159c7f447cb5c38 after Architecture planning, Reliability, Data Quality, Verification planning reviews, docs-only contract freeze, Reliability/Data Quality/Verification contract reviews, exact docs commit and exact push gates closed.
DB/API/Dashboard API read path implementation: CLOSED at 763b248 / 763b248ca835f59096e73aa5e199a4bf903ac946 after Architecture implementation, Reliability, Data Quality, Verification exact allowlist audit, focused tests, exact commit and exact push gates closed.
DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only implementation: CLOSED at b30db5c / b30db5cd2bd1d109d83c8da1a222d5ad37517448 after Architecture implementation, Reliability, Data Quality, Verification exact allowlist audit, focused default-skipped harness tests, exact commit and exact push gates closed.
DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync: CLOSED at 64d0e12 / 64d0e12dc76898a2da3ce09c2c0e94dbbf33ac80.
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Gate and Reliability/Data Quality planning reviews: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Verification Review / Exact Future Run Allowlist Audit found blocker B1; B1 is now CLOSED after HOLD repair and Verification re-review.
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning HOLD repair is committed/pushed at 2cfad5d / 2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e.
The HOLD repair updated api/tests/test_accepted_station_events_api_db_backed.py with API-side pre-insert schema/constraint/column/nullability verification.
The schema verification runs after migration apply and before fixture insert in the DB-backed API run path.
PM handoff after API DB-backed schema verification is committed/pushed at 99dfc26 / 99dfc265983d757de7c23f6a677cabbc05bc4f5a.
DB-backed API validation harness repair is committed/pushed at 8a8004c / 8a8004c53f5bca871610807ae1ec99650e759127.
Remote live DB-backed API validation rerun against the repaired harness is CLOSED / PASS: focused pytest 62 passed in 8.68s, migration apply/schema verification/fixture insert/API live DB read assertions completed, and isolated test DB cleanup returned test_db_cleanup_ok edge_mes_test_api_read.
PM handoff after DB-backed validation harness repair is committed/pushed at 5543c87 / 5543c877e85c2d77c0a7f67bec1d36d2a206ca76.
DB/API/Dashboard consumer planning gate is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at f4de1c3 / f4de1c345f503c9556bceece99ef22be091c025e.
DB/API/Dashboard consumer planning Reliability, Data Quality and Verification focused reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers; recommendations are carry-forward items and do not block the current docs/status sync.
PM handoff after consumer planning is committed/pushed at cd6dff8 / cd6dff82c752c3c43e5a62223a5b03d28987c146.
DB/API/Dashboard API consumer contract freeze gate is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at f65a120 / f65a120545efcdb7ca39f20dbf703a804f82763f.
API consumer contract freeze changed file: docs/contracts/dashboard_api_contract.md.
API consumer contract freeze Reliability, Data Quality and Verification focused reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers; recommendations are carry-forward items.
DB/API/Dashboard API implementation planning gate is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at 2dc4b4d / 2dc4b4d7eb3a3e16a24acdfeeec2d980d7b58084.
API implementation planning changed file: docs/reports/sprint3_api_consumer_implementation_plan.md.
API implementation planning Reliability, Data Quality and Verification focused reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers; recommendations are carry-forward items.
DB/API/Dashboard accepted station events API implementation is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at 97dc4d5 / 97dc4d520ef8edc9b7620e5ce9e8a61d0e1aee7f.
API implementation changed files: api/app/routes/accepted_station_events.py and api/tests/test_accepted_station_events_api.py.
API implementation Reliability, Data Quality and Verification focused reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers; recommendations are carry-forward items.
Focused non-DB validation for the implementation: `PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py -q` -> 53 passed; `PYTHONPATH=api .venv/bin/python -m compileall api/app` -> PASS; `git diff --check -- api/app/routes/accepted_station_events.py api/tests/test_accepted_station_events_api.py` -> PASS.
DB-backed API validation planning is committed/pushed at 78ce29b / 78ce29bd4229912a9164f9e35c911f0037e14a83. The first SSH-tunnel DB-backed execution returned HOLD with focused pytest 1 failed / 87 passed due to the controlled failure assertion expecting 500 while the route correctly returned 503. The focused repair is committed/pushed at 1d040a6 / 1d040a6d90085adee7e95914d9696c0ed6834c44 and aligned the expected failure status/detail to 503 `{"detail": "accepted fact source unavailable"}` while preserving rollback/no-side-effect assertions. PM handoff after DB-backed repair is committed/pushed at a0042fb / a0042fb8f21b38aa4a74e35b2c0cddbce80a7994.
DB-backed API validation execution rerun with SSH tunnel DSNs is CLOSED / PASS WITH RECOMMENDATIONS: exact focused command used only `api/tests/test_accepted_station_events_api.py` and `api/tests/test_accepted_station_events_api_db_backed.py`; result `88 passed in 12.94s`. The run used DB-backed opt-in and loopback SSH tunnel DSNs in masked form: target database `edge_mes_test_api_read`, maintenance database `postgres`, Mac `localhost:5433` -> Pi `localhost:5432`. No code edits, no staged files, no commit/push and no Docker/deploy/tag/rollback were performed during rerun intake. Terse `-q` output did not print an explicit cleanup line, but pytest reported no teardown/cleanup error. The post-execution docs/status sync is committed/pushed at ba02249 / ba0224972f18e097307310039c27f29259b3a0cc.
Dashboard/API implementation planning gate is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at 4fcdd66 / 4fcdd6623247aaf9d3d3df23fd7cadf49f5d662a. Changed file: docs/reports/sprint3_dashboard_api_implementation_plan.md. Architecture / Integration planning, Reliability focused planning review, Data Quality focused planning review and Verification focused planning review / exact future implementation allowlist audit are all CLOSED / PASS WITH RECOMMENDATIONS with no blockers.
Dashboard implementation preparation / allowlist gate is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at 4ad0e91 / 4ad0e91b41c4595295140d32b6bc96aa41f81b35.
Dashboard accepted-events frontend implementation is CLOSED / PASS WITH RECOMMENDATIONS with no blockers after Reliability HOLD repair/re-review, Data Quality review and Verification HOLD repair/re-review. The implementation is committed/pushed at 896c2d1 / 896c2d159ce9c934c53f62607d93475d5fffd681.
Current live baseline for this docs/status sync: 896c2d1 / 896c2d159ce9c934c53f62607d93475d5fffd681. The API implementation commit synchronized by earlier docs/status update was 97dc4d5; the DB-backed API validation planning commit was 78ce29b; the focused repair commit was 1d040a6; the DB-backed rerun docs/status commit was ba02249; the Dashboard/API implementation planning commit is 4fcdd66; the Dashboard implementation preparation / allowlist commit is 4ad0e91; the Dashboard accepted-events frontend implementation commit is 896c2d1. The Dashboard accepted-events frontend implementation gate is now a separate closed PASS gate.
The committed Dashboard accepted-events frontend changed exactly 28 `frontend/` allowlist files: `frontend/package.json`, `frontend/package-lock.json`, `frontend/next.config.ts`, `frontend/tsconfig.json`, `frontend/src/app/layout.tsx`, `frontend/src/app/accepted-events/page.tsx`, `frontend/src/app/accepted-events/loading.tsx`, `frontend/src/app/accepted-events/error.tsx`, `frontend/src/app/accepted-events/__tests__/page.test.tsx`, `frontend/src/lib/acceptedStationEvents/apiClient.ts`, `frontend/src/lib/acceptedStationEvents/query.ts`, `frontend/src/lib/acceptedStationEvents/schema.ts`, `frontend/src/lib/acceptedStationEvents/viewModel.ts`, `frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts`, `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`, `frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts`, `frontend/src/components/accepted-events/AcceptedEventsTable.tsx`, `frontend/src/components/accepted-events/AcceptedEventsQueryControls.tsx`, `frontend/src/components/accepted-events/PageSummaryStrip.tsx`, `frontend/src/components/accepted-events/NokDetailEvidencePanel.tsx`, `frontend/src/components/accepted-events/TraceReferencePanel.tsx`, `frontend/src/components/accepted-events/AcceptedEventsStates.tsx`, `frontend/src/components/accepted-events/__tests__/AcceptedEventsTable.test.tsx`, `frontend/src/components/accepted-events/__tests__/AcceptedEventsQueryControls.test.tsx`, `frontend/src/components/accepted-events/__tests__/PageSummaryStrip.test.tsx`, `frontend/src/components/accepted-events/__tests__/NokDetailEvidencePanel.test.tsx`, `frontend/src/components/accepted-events/__tests__/TraceReferencePanel.test.tsx`, `frontend/src/styles/globals.css`.
Dashboard accepted-events frontend implementation boundary: Dashboard/frontend only; read-only consumer only; only `GET /api/v2/production/accepted-station-events`; query params only `line_id`, `start_time`, `end_time`, `limit`, `cursor`; DTO allowlist only accepted fact fields from `production_accepted_station_event_fact`; no raw/debug/diagnostic/candidate/legacy fallback; no `work_order` / `product`; `accepted_at` means accepted fact timestamp only; page summaries are current-page-only.
Dashboard accepted-events frontend validation evidence from the closed review chain: `npm ci` PASS; `npm test` PASS, 9 files / 24 tests; `npm run typecheck` PASS; `npm run build` PASS after V-B1 repair; generated artifacts cleaned; `git diff --check -- frontend` PASS. npm `allow-scripts` warning for `fsevents` / `sharp` is carried as a CI/reproducibility note, not a blocker.
Dashboard accepted-events vertical validation planning is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at dd6dc53 / dd6dc53627c6e27b5ff206096a91d77dd76d4d23. The planning report is `docs/reports/sprint3_dashboard_accepted_events_vertical_validation_plan.md`. Reliability and Data Quality planning reviews are CLOSED / PASS WITH RECOMMENDATIONS with no blockers. Verification planning review initially returned HOLD for B1 forbidden surface matrix precision, B2 future allowlist exactness and B3 expired cursor fail-closed coverage; Architecture / Integration repaired the planning report and Verification re-review CLOSED B1/B2/B3 with PASS WITH RECOMMENDATIONS. No validation execution, tests, DB-backed run, browser/manual smoke, Docker/runtime/server, frontend/API/contract/package/DB edits or docs/status sync execution occurred in the planning gate.
Dashboard accepted-events vertical validation post-push docs/status sync is committed/pushed at b7ce52b / b7ce52bde04686ff55974c8c7dac1e5605150ad5. PM handoff after Dashboard vertical validation sync is committed/pushed at 8b2e7a0 / 8b2e7a01045978f8f4248038fbc1b589f16e66c2.
Dashboard frontend no-DB validation environment prep gate is CLOSED / PASS: exact command `cd frontend && npm ci` completed with no tracked file diff; `frontend/node_modules/` exists as a local dependency artifact and must remain excluded from staging.
Dashboard accepted-events no-DB vertical validation execution is CLOSED / PASS WITH RECOMMENDATIONS. Architecture / Integration executed only the four authorized frontend focused commands and reported 4 files / 19 tests passed: `query.test.ts` 8 tests, `schema.test.ts` 2 tests, `viewModel.test.ts` 2 tests and `page.test.tsx` 7 tests. Verification focused review / exact evidence audit, Data Quality focused review and Reliability focused review are all CLOSED / PASS WITH RECOMMENDATIONS with no blockers.
The no-DB execution carry-forward recommendations were later handled by a separately authorized `apiClient` focused no-DB tests branch: only-GET endpoint behavior, 4xx invalid / expired / cross-scope cursor mapping, 503 unavailable mapping, explicit invalid `limit` executable coverage and a forbidden leakage parameterized matrix.
Dashboard accepted-events apiClient focused no-DB test planning gate is CLOSED / PASS WITH RECOMMENDATIONS. The implementation gate is CLOSED / PASS and committed/pushed at 96c0928 / 96c0928970d9917e0a4142569ebbc8459d67cc3d with exact test-only files: `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts`, `frontend/src/lib/acceptedStationEvents/__tests__/query.test.ts`, `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`, `frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts` and `frontend/src/app/accepted-events/__tests__/page.test.tsx`.
Focused no-DB evidence for the apiClient branch: `apiClient.test.ts` 7 passed, `query.test.ts` 12 passed, `schema.test.ts` 26 passed, `viewModel.test.ts` 3 passed and `page.test.tsx` 8 passed. Reliability focused review is CLOSED / PASS; Data Quality focused review is CLOSED / PASS WITH RECOMMENDATIONS; Verification focused review / exact evidence audit is CLOSED / PASS WITH RECOMMENDATIONS. No production source, package/config, API, contract, DB, docs/status, Docker/runtime/browser, typecheck/build, stage/commit/push expansion occurred during the implementation or review gates.
Carry-forward recommendation after the apiClient focused no-DB tests branch: later separately authorize a defense-in-depth fixture for nested or renamed production-looking leakage variants. This is not a current blocker.
Current live baseline for this docs/status sync: 96c0928 / 96c0928970d9917e0a4142569ebbc8459d67cc3d. The next eligible branch is exact-path docs/status sync commit/push for this sync after PM authorization, PM handoff if thread/context is long, or a separately authorized future gate such as typecheck/build, browser smoke, API non-DB, DB-backed validation, or the nested/renamed leakage defense-in-depth fixture.
Only production fact source for DB/API/Dashboard consumers: production_accepted_station_event_fact. raw_plc_sample, cycle_event, station_event, production_unit, quality_event, production_snapshot and production_events must not be used as equivalent production fact sources, fallback sources, legacy compatibility sources or join-derived field fillers.
Response DTO fields must come field-by-field from production_accepted_station_event_fact row fields; fallback is forbidden.
The accepted station events API route now allows only line_id, start_time, end_time, limit and cursor query parameters for this slice; all other accepted-fact filters, work_order/product, raw/diagnostic/candidate filters and unknown query parameters fail closed with 422.
raw payload/raw_hex/raw bytes/raw_sample_id, decoded/source normalized candidate payload, adapter disposition/reason/phase, candidate context, raw/normalized comparison context, decoder errors and diagnostic/review/audit payloads are diagnostic/review/debug only and must not enter production DTOs, production Dashboard, OEE or traceability main production facts.
ack_status, read_done, collector_state, quality_pareto_input, dashboard_state and bare result/defect/quality/pareto production-looking keys are forbidden in production consumer payloads and cursor payloads.
NOK/detail fields may come only from accepted fact rows and must bind accepted upstream business evidence and shared station-event validation.
work_order and product remain excluded until a later schema/contract authority gate. accepted_at is an accepted fact timestamp, not collector freshness, ACK time, station freshness or read_done time.
An optional debug/review diagnostics view remains deferred and must be a separate Level 2 gate with separate diagnostic/audit/review namespaces and leakage-negative review before implementation.
Carry-forward recommendations after implementation: configure non-default ACCEPTED_STATION_EVENTS_CURSOR_SECRET before production deploy; consider fail-closed behavior/tests for duplicate allowed query keys; optionally add explicit invalid timezone and cursor no-DB-query assertions; optionally add COMMIT/ROLLBACK sequencing spy assertions; future DB unavailable / missing schema / missing table / missing authority error envelope may be refined if Dashboard consumers need differentiated states.
DB/API/Dashboard consumer planning, API consumer contract freeze, API implementation planning, accepted station events API implementation, DB-backed API validation planning/repair, DB-backed API validation execution rerun, Dashboard/API implementation planning, Dashboard implementation preparation / allowlist, Dashboard accepted-events frontend implementation, Dashboard accepted-events vertical validation planning, Dashboard accepted-events no-DB vertical validation execution and Dashboard accepted-events apiClient focused no-DB tests are closed. The next eligible branch is exact-path docs/status sync commit/push for this sync after PM authorization, PM handoff if thread/context is long, or a separately authorized future gate such as typecheck/build, browser smoke, API non-DB, DB-backed validation, or the nested/renamed leakage defense-in-depth fixture.
DB/API/Dashboard expansion beyond the accepted station-event fact DB write path, guarded DB-backed accepted fact tests, accepted fact API read contract/docs freeze, accepted fact API read path implementation, API consumer planning/contract/planning/implementation, DB-backed API validation harness repair, completed remote live validation, the completed 88-pass SSH-tunnel DB-backed API rerun, Dashboard/API implementation planning and the committed accepted-events frontend remains not authorized except future separately authorized exact-scope gates.
Optional debug/review diagnostics view, new migration, future DB-backed reruns, worker/runtime DB-backed gates, EDGE_MES_ENABLE_DB_BACKED_TESTS=1 outside an approved gate, local/remote Postgres connection outside an approved gate, Docker / docker compose lifecycle actions, deploy, tag, rollback, broad tests, actual timeout failure proof, real PLC pilot, API/contract/DB/runtime expansion and stage/commit/push: not authorized without separate PM approval.
```

当前 Sprint 3 Slice J downstream adapter boundary tests-only hardening files 已提交：

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
```

Slice J downstream adapter boundary tests-only hardening summary:

```text
Slice J hardened the frozen downstream adapter decision / diagnostic / projection boundary in tests only.
Commit message: Harden Sprint 3 Slice J adapter boundary tests.
Commit: ed9a61e / ed9a61ef2bd8e6be12ad786fd7846f2efcfb0cad.
Accepted decisions remain the only path to existing persist/ACK behavior.
Non-accepted dispositions rejected / deferred / quarantined / duplicate / conflict / raw_variant are covered under read_done=False and read_done=True and must not persist, mutate ACK/read_done status for the current non-accepted payload, project, write defect detail or become production-visible facts.
duplicate/raw_variant wording is tightened to "no ACK/read_done mutation for the current non-accepted payload".
raw_variant remains represented as disposition == "duplicate" plus AuditSubtype.RAW_VARIANT.
Focused tests: 80 passed.
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker.
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker.
Verification focused review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker.
No production code changed.
No storage.py / DB / API / Dashboard / V-PLC / config / Docker / deploy changed.
ACK/read_done ownership unchanged.
```

Sprint 3 accepted production-fact visibility boundary summary:

```text
The accepted production-fact visibility boundary docs/contracts freeze is CLOSED / PASS WITH RECOMMENDATIONS.
Changed docs/contracts files: docs/contracts/collector_ingestion_adapter.md and docs/reports/sprint3_collector_ingestion_adapter_plan.md.
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker.
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker.
Verification focused review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker.
Future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.
Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
raw_payload/raw_hex is evidence, not a production fact; it is only a future review-only/audit-only candidate.
Decoded/source normalized payloads remain candidates until accepted; non-accepted candidates stay diagnostic-only.
Non-accepted dispositions do not write defect detail; NOK/detail visibility must bind to accepted upstream business evidence.
DB/API/Dashboard schema/API/UI/DB work remains deferred; future gates must restate exact allowlist, review gates and production-fact leakage negative tests.
ACK/read_done ownership remains unchanged, and visibility/diagnostic/review-only logic cannot become the owner.
Future hardening backlog: duplicate/conflict precedence, historical config replay, exact-byte canonical fixture vectors, raw error taxonomy and production-fact leakage negative tests.
Carry-forward: before actual DB/API/Dashboard implementation, consider tightening any remaining "candidate visible facts" wording to "candidate future production-visible facts".
No tests, implementation, storage.py, DB/API/Dashboard, V-PLC, Docker/deploy, ACK/read_done ownership, tag, rollback or real PLC pilot is authorized by this boundary freeze.
```

当前 Sprint 3 adapter production-fact leakage negative tests files 已提交：

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
```

Sprint 3 adapter production-fact leakage negative tests summary:

```text
Tests-only adapter production-fact leakage negative implementation is CLOSED / PASS WITH RECOMMENDATIONS.
Commit message: Harden adapter visibility tests.
Commit: fd3a799 / fd3a79901619c9afe664c709834b7e396187f8b2.
Changed files: collector/tests/test_event_collector_adapter_gate.py and tests/test_collector_station_event_adapter.py.
The implementation strengthened runtime non-accepted adapter decision coverage so diagnostic context does not expose production projection, production outcome, defect detail, Quality/Pareto or Dashboard keys.
The implementation added offline production-fact leakage summary assertions and a negative matrix for rejected, deferred, quarantined, duplicate, raw_variant and conflict.
The implementation added diagnostic reason-code coverage proving RAW_NORMALIZED_MISMATCH cannot become NOK/detail or Quality authority.
Accepted positive control is preserved only to seed legal accepted state for duplicate/conflict/raw_variant checks.
Focused tests: collector/tests/test_event_collector_adapter_gate.py -> 36 passed; tests/test_collector_station_event_adapter.py -> 46 passed.
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker.
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker.
Verification exact allowlist audit / review-sequence closeout: PASS WITH RECOMMENDATIONS, no blocker.
No production code changed.
No config/mapping.yaml / raw_required / line-wide runtime_defaults.raw_policy changed.
No storage.py / DB / API / Dashboard / V-PLC / Docker / deploy changed.
ACK/read_done ownership unchanged; preserve exact boundary: no ACK/read_done mutation for the current non-accepted payload.
Future production visibility remains limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.
Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
raw_payload/raw_hex is evidence, not a production fact.
Decoded/source normalized payloads remain candidates until accepted; non-accepted dispositions do not write defect detail.
NOK/detail visibility must bind to accepted upstream business evidence.
DB/API/Dashboard remains not authorized by this tests-only gate.
Carry-forward: future DB/API/Dashboard implementation gates should replace current synthetic visibility-summary keys with real schema/API/UI field assertions once those surfaces are explicitly authorized.
Carry-forward: future DB/API/Dashboard gates must restate exact allowlist, review gates and production-fact leakage negative tests.
Next eligible gate: DB/API/Dashboard production visibility contract gate, or a separately authorized hardening planning gate for duplicate/conflict precedence, historical config replay, raw error taxonomy or exact-byte canonical fixture vectors.
```

DB/API/Dashboard Slice 2 DB write path summary:

```text
DB/API/Dashboard Slice 2 DB write path implementation is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at 299d28a / 299d28aa5c91b8c3cf7115b6582ce26d45b64706.
Commit message: Implement accepted station event fact write path.
Added accepted station-event fact write path for production_accepted_station_event_fact.
Added accepted_station_event_fact.py DTO/helper.
Added Storage.transaction() and no-internal-commit write variants.
Accepted path writes production fact + legacy/current persistence in one transaction.
ACK/read_done mutation happens only after successful transaction commit.
Non-accepted dispositions create zero production rows and no ACK/read_done mutation for the current payload.
Preserve exact boundary wording: no ACK/read_done mutation for the current non-accepted payload.
Duplicate/conflict/raw_variant/idempotency behavior implemented and tested with focused fake/spy coverage.
No DB migration/API/Dashboard/V-PLC/config/deploy/tag/rollback changes in this slice.
Architecture implementation evidence: collector/tests/test_event_collector_adapter_gate.py -> 36 passed; tests/test_collector_station_event_adapter.py -> 46 passed; collector/tests/test_event_collector_accepted_fact_write_path.py -> 12 passed; compileall collector/app/services -> PASS; git diff --check -> PASS.
Reliability reran focused commands: 36 passed; 46 passed; 12 passed; compileall PASS; git diff --check PASS.
Data Quality ran combined focused tests: 94 passed.
Verification final audit: 94 passed; compileall PASS; git diff --check PASS; cached empty; exact allowlist PASS.
Future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.
Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
raw_payload/raw_hex is evidence, not a production fact.
Decoded/source normalized payloads remain candidates until accepted.
Non-accepted dispositions do not write defect detail.
NOK/detail visibility must bind to accepted upstream business evidence.
Carry-forward before 636ba37: add DB-backed/live Postgres tests for production_accepted_station_event_fact unique constraints, rollback behavior, commit failure, connection failure and race/unique-violation-after-precheck.
Carry-forward before 636ba37: add direct storage-level coverage for insert_accepted_station_event_fact_no_commit() against real DB constraints.
Carry-forward before 636ba37: add DTO builder negative coverage for station_result nok missing accepted NOK evidence.
Carry-forward after 636ba37: default-skipped DB-backed direct-storage tests and pure DSN/fixture safety tests now exist; actual DB opt-in/local Postgres execution remains unauthorized.
Carry-forward after 636ba37: worker-level DB-backed accepted rollback, commit failure before ACK, non-accepted DB-backed zero rows + no ACK/read_done mutation, race / unique-violation-after-precheck and post-unique-violation re-read semantics require a future PM-authorized local Postgres harness gate.
Carry-forward: future DB/API/Dashboard gates must use real production accepted fact table assertions, not synthetic visibility assumptions.
Carry-forward: do not treat legacy/current raw_plc_sample, cycle_event, station_event, production_unit or quality_event as equivalent to production accepted fact surface.
Next eligible gate: DB/API/Dashboard consumer planning is now closed; the next consumer branch is API consumer contract freeze, a Level 2 planning/contract branch requiring separate PM authorization. Future DB opt-in/local Postgres API read validation harness work remains separately authorized.
Not authorized yet: DB opt-in test run, local Postgres connection, docker compose, Dashboard implementation, new migration, deploy, tag, rollback, broad tests or real PLC pilot.
```

DB/API/Dashboard guarded DB-backed accepted fact tests summary:

```text
DB/API/Dashboard guarded DB-backed accepted fact tests are CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at 636ba37 / 636ba375248987b26d4ae68bdbf952d47f398bc8.
Commit message: Add guarded DB-backed accepted fact tests.
Changed files: pytest.ini, collector/tests/conftest.py, collector/tests/test_db_backed_safety.py, collector/tests/test_event_collector_accepted_fact_db_backed.py, collector/tests/test_event_collector_accepted_fact_write_path.py, collector/app/services/accepted_station_event_fact.py.
The implementation registers db_backed and postgres_local pytest markers.
DB-backed tests are skipped by default unless EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
DSN safety helpers validate test-target and maintenance/admin DSNs before any psycopg.connect path.
Test-target DB names must match edge_mes_test_* and protected names such as edge_mes, postgres, prod and production are rejected.
Maintenance/admin DSNs are separated from test-target DSNs and limited to local postgres/template1 maintenance targets.
Temp DB helpers generate guarded create/drop plans and DROP DATABASE statements only for proven edge_mes_test_* names.
Migration helper ordering is deterministic: db/init/*.sql as needed, then db/migrations/007_accepted_station_event_visibility.sql.
Schema verification checks production_accepted_station_event_fact and expected unique/check constraints before db_backed_storage yields.
DB-backed pytest-discovered tests are limited to seven direct-storage opt-in tests skipped by default.
Non-executable worker/race/commit/non-accepted DB-backed scenarios were reclassified as future DB-authorized carry-forward items, not current coverage.
station_result NOK missing accepted business NOK evidence now fails closed in the DTO builder before DB insert.
Focused default tests: PYTHONPATH=collector:. .venv/bin/python -m pytest collector/tests/test_db_backed_safety.py collector/tests/test_event_collector_accepted_fact_write_path.py collector/tests/test_event_collector_accepted_fact_db_backed.py -q -> 33 passed, 7 skipped.
Reliability first implementation review found HOLD for overstated placeholder matrix; Architecture repair removed placeholder pytest coverage; Reliability re-review closed the blocker with PASS WITH RECOMMENDATIONS.
Data Quality focused implementation review: PASS WITH RECOMMENDATIONS, no blocker.
Verification focused implementation review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker; git diff --check PASS; exact allowlist PASS.
No DB opt-in tests were run, no DB connection was made, and docker compose was not started.
No storage.py, migration 007, API, Dashboard/frontend, V-PLC, config/mapping.yaml, docker-compose.yml, deploy/tag/rollback or docs/status/handoff files changed in the implementation commit.
Carry-forward: worker-level DB-backed accepted rollback, commit failure before ACK, non-accepted DB-backed zero rows + no ACK/read_done mutation, race / unique-violation-after-precheck and post-unique-violation re-read semantics require a future PM-authorized local Postgres harness gate.
```

DB/API/Dashboard API read path contract freeze summary:

```text
DB/API/Dashboard API read path contract freeze is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at 2d0918a / 2d0918adebe5cd29e59177bc2159c7f447cb5c38.
Commit message: Freeze accepted fact API read contract.
Changed file: docs/contracts/dashboard_api_contract.md.
The contract freezes future GET /api/v2/production/accepted-station-events as a future API contract only, not a current implementation claim.
The future endpoint may read only production_accepted_station_event_fact and must not treat raw_plc_sample, cycle_event, station_event, production_unit, quality_event, production_snapshot or production_events as equivalent production fact sources.
Response DTO allowlist is limited to accepted station-event business fact fields from production_accepted_station_event_fact, including NOK/detail accepted evidence reference fields.
Forbidden fields include raw_payload/raw_hex, adapter diagnostics, candidate/normalized/raw comparison context, decoder errors, diagnostic/review/audit payloads, legacy payload/raw_sample_id, ack_status, read_done, collector_state, dashboard_state, quality_pareto_input and ambiguous result/defect/quality/pareto keys.
Query contract requires bounded start_time/end_time, line_id or explicit server default scope, limit max 500, strict cursor parsing and stable pagination order.
Reliability/Data Quality/Verification contract freeze reviews: PASS WITH RECOMMENDATIONS, no blocker.
Carry-forward: statement_timeout / idle timeout should become future implementation MUST; cursor tuple/sorting/tie-breaker and cursor scope/filter/time-window binding should be frozen before implementation; api/app/db.py remains conditional future allowlist only if centralized read-only DB helper support is needed.
Future implementation allowlist planning should start from api/app/routes/accepted_station_events.py, api/app/main.py and api/tests/test_accepted_station_events_api.py; no API implementation, tests, DB opt-in run, migration, storage.py, collector, config, Dashboard/frontend/Grafana, V-PLC, Docker/deploy/tag/rollback is authorized by this docs/status sync.
```

DB/API/Dashboard API read path implementation summary:

```text
DB/API/Dashboard API read path implementation is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at 763b248 / 763b248ca835f59096e73aa5e199a4bf903ac946.
Commit message: Implement accepted station events read API.
Changed files: api/app/main.py, api/app/routes/accepted_station_events.py, api/tests/test_accepted_station_events_api.py.
Endpoint implemented: GET /api/v2/production/accepted-station-events.
The endpoint reads only production_accepted_station_event_fact and does not read, join or fallback to raw_plc_sample, cycle_event, station_event, production_unit, quality_event, production_snapshot or production_events.
DTO response fields are limited to the frozen accepted fact allowlist; raw/diagnostic/candidate/review/audit/ACK/read_done/collector/Dashboard/Quality/Pareto leakage is forbidden and covered by focused tests.
Query validation requires line_id and bounded start_time/end_time, uses strict timezone-aware ISO parsing, default limit 50, max limit 500, and fail-closed invalid limit/time/window behavior.
Cursor is HMAC signed, schema/version checked and binds line_id, start_time, end_time, limit, direction and ordering tuple; stable order is event_ts ASC, accepted_at ASC, fact_key ASC.
Read safety uses BEGIN READ ONLY, SET LOCAL statement_timeout = '3s', SET LOCAL idle_in_transaction_session_timeout = '3s', SELECT-only query, COMMIT/ROLLBACK, no write-path helper reuse and no Collector/PLC/V-PLC/runtime side effect.
NOK/detail fields are returned only from accepted fact row fields and must bind accepted upstream business evidence.
Focused validation: PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py -> 27 passed; git diff --check PASS.
Reliability implementation review: PASS WITH RECOMMENDATIONS, no blocker.
Data Quality implementation review: PASS WITH RECOMMENDATIONS, no blocker.
Verification implementation review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker.
api/app/db.py was not changed; DB opt-in/local Postgres execution was not run and remains unauthorized.
Carry-forward: before production deploy, ACCEPTED_STATION_EVENTS_CURSOR_SECRET must be managed as a real deployment secret rather than relying on the development fallback.
Next eligible gate: DB/API/Dashboard consumer planning is now closed; the next consumer branch is API consumer contract freeze, a Level 2 planning/contract branch requiring separate PM authorization. Separately authorized DB opt-in / live local Postgres API read validation planning remains independent.
```

DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only implementation and explicit DB opt-in/live local Postgres run planning HOLD repair summary:

```text
DB/API/Dashboard DB-backed/live Postgres API Read Validation tests-only implementation is CLOSED / PASS WITH RECOMMENDATIONS and committed/pushed at b30db5c / b30db5cd2bd1d109d83c8da1a222d5ad37517448.
DB/API/Dashboard DB-backed/live Postgres API Read Validation post-push docs/status sync is CLOSED / PASS and committed/pushed at 64d0e12 / 64d0e12dc76898a2da3ce09c2c0e94dbbf33ac80.
DB/API/Dashboard explicit DB opt-in/live local Postgres API Read Validation Run Planning Gate is CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Reliability planning review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Data Quality planning review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Verification planning review / exact future run allowlist audit: CLOSED / HOLD, blocker B1.
HOLD repair: CLOSED / PASS, no blocker.
Verification re-review: CLOSED / PASS WITH RECOMMENDATIONS, blocker B1 CLOSED.
HOLD repair exact-path commit/push: PASS, commit 2cfad5d / 2cfad5d9d8d91ed824a59b1b6eb713e3e50b0a1e.
PM handoff after API DB-backed schema verification: PASS, commit 99dfc26 / 99dfc265983d757de7c23f6a677cabbc05bc4f5a.
DB-backed API validation harness repair: PASS, commit 8a8004c / 8a8004c53f5bca871610807ae1ec99650e759127.
Remote existing PostgreSQL DB-backed API validation rerun with repaired RecordingConnection proxy: PASS, focused pytest 62 passed in 8.68s; test DB cleanup: test_db_cleanup_ok edge_mes_test_api_read.
PM handoff after DB-backed validation harness repair: PASS, commit 5543c87 / 5543c877e85c2d77c0a7f67bec1d36d2a206ca76.
DB-backed API validation planning exact-path commit/push: PASS, commit 78ce29b / 78ce29bd4229912a9164f9e35c911f0037e14a83.
DB-backed API validation first SSH-tunnel execution: HOLD, focused pytest 1 failed / 87 passed; failure was controlled failure assertion `assert 503 == 500`.
DB-backed API validation focused repair: PASS, commit 1d040a6 / 1d040a6d90085adee7e95914d9696c0ed6834c44; expected status aligned to 503 with exact detail `{"detail": "accepted fact source unavailable"}` and failure-path no-side-effect assertion preserved.
PM handoff after DB-backed repair: PASS, commit a0042fb / a0042fb8f21b38aa4a74e35b2c0cddbce80a7994.
DB-backed API validation execution rerun with SSH tunnel DSNs: CLOSED / PASS WITH RECOMMENDATIONS, focused pytest `88 passed in 12.94s` using exact files `api/tests/test_accepted_station_events_api.py` and `api/tests/test_accepted_station_events_api_db_backed.py`.
DB-backed API validation rerun masked DSN facts: target host `localhost`, target port `5433`, target database `edge_mes_test_api_read`, maintenance database `postgres`, SSH tunnel Mac `localhost:5433` -> Pi `localhost:5432`.
DB-backed API validation rerun cleanup evidence: terse `-q` output did not print an explicit cleanup line; pytest reported no teardown/cleanup error.
DB-backed API validation post-execution docs/status sync: PASS, commit ba02249 / ba0224972f18e097307310039c27f29259b3a0cc.
Dashboard/API implementation planning gate: CLOSED / PASS WITH RECOMMENDATIONS, commit 4fcdd66 / 4fcdd6623247aaf9d3d3df23fd7cadf49f5d662a.
Dashboard/API implementation planning report: docs/reports/sprint3_dashboard_api_implementation_plan.md.
Dashboard/API implementation planning Architecture / Integration, Reliability, Data Quality and Verification focused planning reviews: CLOSED / PASS WITH RECOMMENDATIONS with no blockers.
Dashboard/API implementation planning carry-forward recommendations: convert category-level Dashboard implementation allowlist into exact file paths before implementation authorization; add explicit invalid / expired / cross-scope cursor UI negative tests; keep page-level summary labelled as current page only; ensure stale prior data cannot render as fresh production truth; keep future implementation Dashboard-only/read-only unless PM opens a separate API/contract gate.
Commit message for implementation: Add DB-backed API read validation tests.
Commit message for HOLD repair: Add API DB-backed schema verification.
Commit message for harness repair: Fix DB-backed API validation harness.
Changed file for implementation and repair: api/tests/test_accepted_station_events_api_db_backed.py.
The implementation added only api/tests/test_accepted_station_events_api_db_backed.py.
The HOLD repair added API-side pre-insert schema/constraint/column/nullability verification for production_accepted_station_event_fact.
The schema verification checks table existence, DTO/accepted fact columns, nullability expectations, unique constraints and accepted-fact check constraints.
The schema verification is called after migration apply and before fixture insert in the live DB-backed execution path.
The harness repair fixed duplicate cursor limit handling, QueryRecorder false positives and RecordingConnection proxy completeness including execute delegation.
DB-backed API tests remain default skipped unless a PM-authorized DB opt-in run sets EDGE_MES_ENABLE_DB_BACKED_TESTS=1.
Default non-DB focused run before HOLD repair: PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_accepted_station_events_api.py api/tests/test_accepted_station_events_api_db_backed.py -q -> 27 passed, 32 skipped.
HOLD repair focused GREEN run: 41 passed, 19 skipped.
Collector DB safety run after HOLD repair: 20 passed.
Harness repair default-safe focused tests: local 43 passed, 19 skipped; remote 43 passed, 19 skipped.
Remote live DB-backed API validation rerun after harness repair: 62 passed in 8.68s.
Remote live DB-backed API validation cleanup: test_db_cleanup_ok edge_mes_test_api_read.
DB-backed API validation execution rerun after focused repair: 88 passed in 12.94s.
DB-backed API validation rerun cleanup: no explicit cleanup line printed in terse `-q` output; no pytest teardown/cleanup error reported.
git diff --check -> PASS in implementation and HOLD repair gates.
Reliability implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Data Quality implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
Verification implementation review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker.
EDGE_MES_ENABLE_DB_BACKED_TESTS=1 was set only in separately authorized DB-backed execution gates.
The authorized remote validation used loopback DSNs only, created/dropped isolated edge_mes_test_api_read, applied existing migrations, verified schema, inserted fixtures and completed API live DB read assertions. The later SSH-tunnel rerun used masked loopback DSNs with Mac `localhost:5433` tunneling to Pi `localhost:5432` and target database `edge_mes_test_api_read`.
Docker / docker compose lifecycle actions were not performed.
Live DB validation has completed for this focused DB-backed API validation harness lane and the later focused DB-backed API rerun lane.
Actual timeout failure proof has not completed.
Do not claim actual timeout failure proof completed.
Current tests prove timeout statements / read behavior and schema verification in the focused DB-backed API validation lane; they do not prove actual timeout failure induction.
API read path source boundary remains only production_accepted_station_event_fact.
Do not treat raw_plc_sample, cycle_event, station_event, production_unit, quality_event, production_snapshot or production_events as equivalent production fact sources, fallback sources or join-derived field fillers.
Future production visibility remains limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted.
Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
raw_payload/raw_hex is evidence, not a production fact.
Decoded/source normalized payloads remain candidates until accepted.
Non-accepted dispositions do not write defect detail.
NOK/detail visibility must bind to accepted upstream business evidence.
Preserve exact wording: no ACK/read_done mutation for the current non-accepted payload.
Future gates remain separate: exact-path docs/status commit/push for this sync; API consumer contract freeze as a Level 2 planning/contract branch; actual timeout failure induction; worker/runtime DB-backed gates for unique-violation race, commit-before-ACK, non-accepted DB-backed zero-row/no ACK/read_done mutation, post-conflict re-read semantics and DB rollback; future DB-backed reruns; deploy/tag/rollback/real PLC pilot only after separate PM authorization.
```

当前 Sprint 3 Slice I WS03 raw_policy raw_capable authority files 已提交：

```text
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

Slice I WS03 raw_policy raw_capable authority summary:

```text
Slice I implemented a narrow Level 2 mapping/config authority rollout for WS03 only.
Commit message: Roll out Slice I WS03 raw policy authority.
Commit: 045d21c / 045d21c14436e8fe13a26bc32b7c2956df0cd99f.
WS01 remains raw_capable.
WS02 remains raw_capable.
WS03 / ws03_runtime_v1 / station_runtime_payload_v1 station-level raw_policy is now raw_capable.
Line-wide runtime_defaults.raw_policy remains raw_not_provided.
raw_required was not introduced.
Runtime/source code was not changed.
The focused tests cover real mapping three-station station-level raw_capable authority, WS03 nominal raw source-builder path, WS03 missing raw RAW_EVIDENCE_MISSING fail-closed, WS01/WS02 raw_capable regression, line-wide default, and config_hash lineage.
Reliability focused review: PASS, no blocker.
Data Quality focused review: PASS, no blocker.
Verification exact allowlist audit: PASS, no blocker.
storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy and ACK/read_done ownership unchanged.
No raw_required introduction and no line-wide raw_policy change.
```

当前 Sprint 3 Slice H WS02 raw_policy raw_capable authority files 已提交：

```text
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

Slice H WS02 raw_policy raw_capable authority summary:

```text
Slice H implemented a narrow Level 2 mapping/config authority rollout for WS02 only.
Commit message: Roll out Slice H WS02 raw policy authority.
Commit: c7e80e8 / c7e80e8e931b5f23d6ea42fee7b10b27191b5e20.
WS01 remains raw_capable.
WS02 / ws02_runtime_v1 / station_runtime_payload_v1 station-level raw_policy is now raw_capable.
WS03 remains raw_not_provided.
Line-wide runtime_defaults.raw_policy remains raw_not_provided.
raw_required was not introduced.
Runtime/source code was not changed.
The focused tests cover real mapping WS02 nominal raw source-builder path, WS02 missing raw RAW_EVIDENCE_MISSING fail-closed, WS01 raw_capable regression, WS03 raw_not_provided normalized-only regression, line-wide default, and config_hash lineage.
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker.
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker.
Verification exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker.
storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy and ACK/read_done ownership unchanged.
No WS03 raw_capable rollout and no raw_required introduction.
```

当前 Sprint 3 Slice G WS01 raw_capable post-commit sanity tests-only hardening files 已提交：

```text
tests/test_collector_station_event_runtime_source.py
```

Slice G WS01 raw_capable post-commit sanity tests-only hardening summary:

```text
Slice G added focused tests-only hardening after Slice F2 WS01 raw_capable authority.
Commit message: Harden Slice G raw policy sanity tests.
Commit: 398f11c / 398f11cfb20717d628d03c0a486a31745fe3030d.
The new tests use real config/mapping.yaml authority, not synthetic replacement, for WS01/WS02/WS03 sanity coverage.
WS01 raw_capable nominal source-builder path now asserts provided raw bytes produce raw_payload.raw_hex while normalized payload remains present.
WS01 raw_capable missing raw now asserts RAW_EVIDENCE_MISSING fail-closed and no silent downgrade to raw_not_provided.
WS02 and WS03 remain raw_not_provided and normalized-only under real mapping authority.
Reliability focused review: PASS.
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker; optional future clarity assertion: snapshot.config_hash == mapping.runtime_snapshot.config_hash.
Verification exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker.
No config/mapping.yaml, runtime/source code, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy or ACK/read_done ownership change.
No WS02/WS03 raw_capable rollout and no raw_required introduction.
```

当前 Sprint 3 Slice F2 raw_policy raw_capable authority files 已提交：

```text
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

Slice F2 raw_policy raw_capable authority summary:

```text
Slice F2 implemented a narrow Level 2 mapping/config authority change for WS01 only.
Commit message: Implement Sprint 3 Slice F2 raw policy authority.
Commit: 829d5c7 / 829d5c71982b8d22556102b6e67ed9c1e981131d.
WS01 / ws01_runtime_v1 / station_runtime_payload_v1 station-level raw_policy is now raw_capable.
No line-wide default change was made; WS02 and WS03 remain raw_not_provided.
raw_required was not introduced.
Runtime/source code was not changed.
Existing runtime path still carries raw_bytes and raw_payload/raw_hex under mapping/config authority.
raw_capable missing raw remains RAW_EVIDENCE_MISSING fail-closed.
RAW_PARSE_ERROR and RAW_NORMALIZED_MISMATCH remain fail-closed.
Non-accepted decisions still do not persist, ACK, project or become DB/API/Dashboard-visible production facts.
Reliability focused review: PASS.
Data Quality focused review: PASS.
Verification exact allowlist audit: PASS WITH RECOMMENDATIONS.
storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy and ACK/read_done ownership unchanged.
```

当前 Sprint 3 Slice F1 raw_policy authority docs/contracts files 已提交：

```text
docs/contracts/collector_ingestion_adapter.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

Slice F1 raw_policy authority docs/contracts summary:

```text
Slice F1 froze raw_policy authority semantics after D3 runtime raw wiring and E1 runtime raw decoder repair.
Commit message: Freeze Sprint 3 Slice F1 raw_policy authority.
Commit: ac1838c / ac1838cbc9378d72da66ace35a200a909f4d5b89.
Runtime code-path capability is not a mapping/config authority upgrade.
event_collector.py can pass raw_bytes=data and station_event_runtime_source.py can materialize raw_payload/raw_hex, but current mapping/config authority remains the immutable raw_policy declaration.
Current config/mapping.yaml default raw_policy remains raw_not_provided.
raw_not_provided is an authority declaration that a source does not produce raw evidence; it is not a synonym for missing runtime raw path.
raw_capable/raw_required missing raw must fail closed as RAW_EVIDENCE_MISSING or future PM-approved equivalent and must not silently downgrade to raw_not_provided.
RAW_PARSE_ERROR and RAW_NORMALIZED_MISMATCH remain fail-closed.
Rejected/diagnostic decisions still do not project, persist, ACK or become DB/API/Dashboard-visible production facts.
Future raw_policy move to raw_capable/raw_required remains a separate Level 2 mapping/config authority gate.
Reliability focused review: PASS.
Data Quality focused review: PASS WITH RECOMMENDATIONS.
Verification exact allowlist audit: PASS WITH RECOMMENDATIONS.
config/mapping.yaml, raw_policy actual value, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy and ACK/read_done ownership unchanged.
```

当前 Sprint 3 Slice E1 runtime raw decoder repair files 已提交：

```text
collector/app/services/resolved_config_registry.py
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_runtime_source.py
```

Slice E1 runtime raw decoder repair summary:

```text
Slice E1 repaired a narrow runtime raw decoder payload materialization issue after Slice E HOLD.
Commit message: Repair Sprint 3 Slice E1 runtime raw decoder.
Commit: 2c73410 / 2c73410281d1465db166b66ddc23e27d9337b90a.
Root cause: runtime raw decoder converted raw_hex with immutable bytes.fromhex(...).
Snap7 util decode path can require a mutable buffer and raised TypeError: 'bytes' object does not support item assignment.
Repair: decode_read_plan(bytearray.fromhex(raw_hex), plan, mapping_snapshot.timezone).
The bytearray is local decode input only.
Canonical raw_hex evidence remains unchanged and still comes from bytes(raw_bytes).hex().
Nominal Snap7 raw path persists exactly once and ACK/read_done side effect occurs exactly once.
Malformed raw remains RAW_PARSE_ERROR fail-closed.
Raw/normalized mismatch remains RAW_NORMALIZED_MISMATCH fail-closed.
Non-accepted decisions still do not persist/ACK.
Diagnostics remain diagnostics.
Raw evidence remains evidence, not production fact.
Reliability focused review: PASS.
Data Quality focused review: PASS.
Verification focused review / exact allowlist audit: PASS WITH RECOMMENDATIONS.
config/mapping.yaml, raw_policy, storage.py, DB/API/Dashboard/frontend, V-PLC behavior, Docker/deploy and ACK/read_done ownership unchanged.
```

当前 Sprint 3 Slice D3 runtime raw wiring files 已提交：

```text
collector/app/plc/mapping.py
collector/app/services/event_collector.py
collector/app/services/resolved_config_registry.py
collector/tests/test_event_collector_adapter_gate.py
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

Slice D3 runtime raw wiring summary:

```text
Slice D3 runtime raw wiring implemented, reviewed, committed and pushed at c9e7c22.
Commit message: Implement Sprint 3 Slice D3 runtime raw wiring.
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
Reliability / Data Quality / Verification focused implementation reviews: PASS WITH RECOMMENDATIONS, no blocker.
DB/API/Dashboard-visible behavior unchanged.
storage.py not touched.
V-PLC behavior unchanged.
Docker/deploy/tag/rollback not authorized.
ACK/read_done ownership unchanged.
```

当前 Sprint 3 Slice D2-C decoder registry authority files 已提交：

```text
collector/app/services/decoder_registry.py
collector/app/services/resolved_config_registry.py
tests/test_collector_station_event_adapter.py
```

Slice D2-C decoder registry authority summary:

```text
Slice D2-C decoder registry authority implemented, reviewed, committed and pushed at 5e5a617.
Commit message: Implement Sprint 3 Slice D2-C decoder registry authority.
D2-C adds offline decoder registry/schema authority and immutable decoder binding to resolved config snapshots.
D2-C requires decoder id/version/callable binding from immutable DecoderRegistrySnapshot and binds decoder registry snapshot identity/content hash to the resolved config snapshot.
Missing registry, registry hash mismatch, unknown decoder id, decoder version mismatch, callable missing, callable exception and decoded output mismatch fail closed.
D2-C has no fallback to latest/current registry, latest/current config, current mapping file, environment defaults or ad hoc fixture callable.
D2-C introduced no D3 runtime raw wiring.
D2-C introduced no event_collector.py, station_event_runtime_source.py, storage.py, DB/API/Dashboard/V-PLC/Docker/deploy change.
ACK/read_done ownership unchanged.
D2-C focused adapter tests: 43 passed.
Collector adapter gate regression: 22 passed.
Runtime source regression: 35 passed.
compileall collector/app/services: PASS.
git diff --check: PASS.
git diff --cached --check before commit: PASS.
```

当前 Sprint 3 Slice D2-B tests-only hardening files 已提交：

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
```

Slice D2-B decoder authority tests-only hardening summary:

```text
Slice D2-B fixture/test-only decoder authority hardening implemented, reviewed, committed and pushed at dafbbf8.
Commit message: Harden Sprint 3 Slice D2-B decoder authority tests.
D2-B is tests-only hardening; no production code changed.
No docs/contracts/plan changed in the implementation commit.
No schema/config/mapping change.
No decoder registry/schema implementation.
No runtime raw wiring.
No DB/API/Dashboard/V-PLC/Docker/deploy change.
No ACK/read_done ownership change.
D2-B coverage includes unknown decoder id current test-only expression, missing callable, callable exception via existing D1 coverage, decoded output mismatch, forbidden raw content, RAW_EVIDENCE_MISSING, raw-only / RAW_ONLY_UNSUPPORTED, raw_capable/raw_required missing raw, normalized-only under immutable raw_not_provided authority, no fallback to latest/current config snapshot, no fallback to latest callable / decoder binding, and non-accepted decisions no projection / no persist / no ACK.
D2-B focused tests: 57 passed.
Runtime source regression: 35 passed.
Collector reliability + Snap7 regression: 7 passed.
git diff --check: PASS.
git diff --cached --check: PASS before commit.
Reliability / Data Quality / Verification focused reviews: PASS WITH RECOMMENDATIONS, no blocker.
```

当前 Sprint 3 Slice D2-A docs/contract-only authority repair files 已提交：

```text
docs/contracts/collector_ingestion_adapter.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

Slice D2-A decoder authority docs/contract-only repair summary:

```text
Slice D2-A decoder registry / decoder callable authority contract repair implemented, reviewed, committed and pushed at 2f6294c.
D2-A is docs/contract-only; no code or tests changed.
D2-A does not implement decoder registry, decoder callable, schema/config/mapping change, or runtime raw wiring.
D2-A binds decoder registry identity, decoder id, decoder version, callable decoder, raw_policy and payload template authority to immutable resolved config snapshot / registry snapshot.
D2-A forbids fallback to latest/current runtime config, latest registry, current mapping file, environment defaults or ad hoc fixture fields.
D2-A fail-closed taxonomy includes RAW_PARSE_ERROR, RAW_NORMALIZED_MISMATCH, RAW_CONTENT_FORBIDDEN and RAW_EVIDENCE_MISSING.
unknown decoder id, missing callable, decoder exception, decoder output mismatch, forbidden raw content and raw-only inputs fail closed without production fact, projection, defect/Pareto/API-visible state or ACK.
raw_not_provided remains the only normalized-only authority.
raw_capable/raw_required missing raw remain fail-closed unless PM later approves a contract change.
Reliability review PASS; Data Quality review PASS WITH RECOMMENDATIONS and recommendation repaired; Verification review PASS WITH RECOMMENDATIONS.
D2-B fixture/test-only, D2-C registry/schema implementation and D3 runtime raw
wiring later closed as separate PM-authorized gates.
```

当前 Sprint 3 Slice D1 test-only hardening files 已提交：

```text
collector/tests/test_event_collector_adapter_gate.py
tests/test_collector_station_event_adapter.py
tests/test_collector_station_event_runtime_source.py
```

Slice D1 raw boundary test-only hardening summary:

```text
Slice D1 raw_not_provided regression and raw boundary fixture hardening implemented, reviewed, committed and pushed at 0358b60.
D1 is test-only hardening; no production code changed.
D1 is not raw runtime support.
No schema/config/mapping change.
No decoder registry.
No raw runtime wiring.
No event_collector.py implementation change.
No storage.py / DB / API / Dashboard / V-PLC / Docker / deploy change.
ACK/read_done ownership unchanged.
raw_not_provided normalized-only path remains accepted only under immutable mapping/resolved snapshot authority.
raw_capable/raw_required missing raw fail closed as RAW_EVIDENCE_MISSING.
raw-only rejects as RAW_ONLY_UNSUPPORTED before identity/projection/fingerprint production.
RAW_EVIDENCE_MISSING / RAW_ONLY_UNSUPPORTED / RAW_PARSE_ERROR / RAW_NORMALIZED_MISMATCH / RAW_CONTENT_FORBIDDEN non-accepted decisions assert no persist / no ACK.
```

当前 Sprint 3 Slice B implementation files 已提交：

```text
collector/app/services/event_collector.py
collector/app/services/station_event_runtime_source.py
collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py
tests/test_collector_station_event_runtime_source.py
collector/tests/test_event_collector_adapter_gate.py
```

Slice B runtime adapter gate summary:

```text
runtime adapter gate implemented and committed at c677515.
adapter gate inserted after payload/cycle/counter guards and counter reset fail-safe, before existing storage.persist_cycle().
accepted-only path continues to existing storage.persist_cycle() plus existing read_done/ACK behavior.
non-accepted decisions do not persist, do not project, do not write defect detail, and do not ACK.
adapter remains non-owner of ACK/read_done.
```

当前 Sprint 3 Slice C diagnostic observability files 已提交：

```text
collector/app/services/event_collector.py
collector/tests/test_event_collector_adapter_gate.py
```

Slice C runtime adapter diagnostic observability summary:

```text
runtime adapter diagnostic observability hardening implemented and committed at e02e39d.
adapter exception path records ADAPTER_GATE_FAILED.
non-accepted decision path records ADAPTER_DECISION_NOT_ACCEPTED.
diagnostic raw_context includes adapter_phase, adapter_disposition, adapter_error_code and adapter_reason where available.
collector state remains non-production diagnostic state, for example ADAPTER_REJECTED.
accepted-only persist path remains unchanged.
non-accepted decisions still do not persist, do not project, do not write defect detail, and do not ACK.
adapter remains non-owner of ACK/read_done.
no raw evidence runtime wiring was introduced.
no storage.py, DB/API/Dashboard/V-PLC/deploy changes were made.
```

当前 Sprint 3 offline adapter implementation files 已提交：

```text
collector/app/services/resolved_config_registry.py
collector/app/services/station_event_adapter.py
tests/test_collector_station_event_adapter.py
```

当前 Sprint 3 recommendation hardening 已完成：

```text
R-N1 / DQ-N1 / V-N1: CLOSED, resolved snapshot content hash self-check implemented.
R-N2 / DQ-N2 / V-N2: CLOSED, route predecessor and direct parent negative fixtures clarified.
Reliability / Data Quality / Verification focused review: PASS WITH RECOMMENDATIONS, no blocker.
Exact allowlist commit/push: PASS, commit 577c1a1.
Docs/status sync completed at fd79e21.
Docs/status baseline repair completed at 4f424c6.
PM rules / baseline semantics repair completed at e284a06.
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

Slice D2-C carry-forward recommendations:

```text
D3 runtime raw wiring remained a separate PM-authorized gate after D2-C and is now closed at c9e7c22.
D2-C PASS alone did not prove runtime raw support; D3 c9e7c22 is the runtime raw wiring closure.
Keep rejected-decision normalized_event/canonical_bytes/fact_key diagnostic-only, not production fact or Quality/Pareto/API-visible state.
Registry failures currently surface as RAW_PARSE_ERROR rather than dedicated decoder-authority public codes; this is non-blocking unless PM opens a future taxonomy gate.
Adapter remains non-owner of ACK/read_done.
No DB/API/Dashboard/V-PLC/deploy/tag/rollback/real PLC pilot is authorized.
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

Slice D2-A carry-forward recommendations:

```text
D2-B fixture/test-only decoder authority hardening is implemented, reviewed, committed and pushed at dafbbf8.
D2-C full decoder registry/schema lookup for unknown decoder id / version mismatch / callable binding is implemented, reviewed, committed and pushed at 5e5a617.
D3 runtime raw wiring is implemented, reviewed, committed and pushed at c9e7c22.
If diagnostic evidence later enters metrics/alerting, avoid production fact, NOK code, Quality/Pareto outcome naming.
Adapter remains non-owner of ACK/read_done.
No DB/API/Dashboard/V-PLC/deploy/tag/rollback/real PLC pilot is authorized.
```

当前外部既有 dirty artifacts，应排除，除非 PM 明确授权：

```text
M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

Codex Thread 应先读取：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- 对应 task-specific contract/report files

下方内容保留 Phase-1 / 早期 Demo 状态快照，供上下文恢复使用；当前开发 gate 以上方 Sprint 3 状态为准。

## 1. 项目一句话状态

Edge MES Demo 已经在树莓派上完成从 V-PLC 到 Collector、PostgreSQL、FastAPI 追溯页面和 Grafana dashboard 的 Phase-1 闭环。Phase-2 Sprint 1 flexible line configuration 与 Sprint 2 generic station event model 已完成；Sprint 3 当前聚焦 Collector ingestion adapter offline implementation，不等于 runtime Collector integration。

## 2. 已完成内容

### 基础设施

- Docker Compose 多服务部署。
- PostgreSQL 本地数据库。
- Grafana dashboard provisioning。
- Prometheus + node-exporter 主机监控。
- Sync worker mock，预留 Oracle 主动同步。

### V-PLC

- `s7-plc-sim` 使用 Snap7 Server。
- 暴露：
  - S7 DB 通讯端口：`1102`
  - V-PLC 控制台：`8200`
- 注册 DB：
  - DB100 legacy
  - DB101 WS01
  - DB102 WS02
  - DB103 WS03
  - DB104 runtime / PLC identity
- 三工站并行 WIP。
- 全局 `unit_id` 从 WS01 创建并贯穿 WS02/WS03。
- 上游 NOK 后，下游工站仍接收该件，但写入 `process_status=SKIPPED`、`skip_reason=UPSTREAM_NOK`。
- WS03 对不合格件生成 `NG-xxxxxx`，并将工件状态置为不合格品处理。
- 未 ACK 的工站 payload 不允许被下一件覆盖。
- 默认严格 ACK；超过 10 秒 deadline 只置 `ack_timeout`，不释放 payload。
- DB104 提供运行期间稳定的 `plc_boot_id`、heartbeat 和持久化 restart counter。
- 手动 WIP/counter reset 会轮换 boot identity 并清除旧 station DB payload。
- station 参数由 `config/vplc.yaml` 统一提供。
- 支持 `normal / fast / test` Profile：
  - `normal` 固定 `scale=1.0`，并锁定 runtime base/jitter 编辑。
  - `fast/test` 只通过 scale 加速，不改变约 30 秒的 process baseline。
- `/vplc/state` 返回当前 profile、scale、配置来源和 config hash。
- 参数修改必须提供 reason，并记录 actor、client IP、request ID、old/new 和接受/拒绝状态。
- startup、runtime update、reset 和周期性参数快照写入审计链路。
- 强制 NOK 支持按工站 code 白名单排队 1–100 件，并可查询或清除 pending 队列。
- 支持：
  - 连续生产
  - 按小时
  - 按件数
  - 按班次
  - 暂停/恢复工站
  - `fast/test` 模式修改节拍、波动
  - 修改 NOK 率
  - 批量强制 NOK 和清除 pending NOK
  - 重置 WIP/counter

入口：

- `http://10.0.0.217:8200/vplc`

### Collector

- 旧快照链路仍采集 DB100 到 `production_snapshot`。
- 新事件链路读取 DB101/102/103。
- 写入：
  - `raw_plc_sample`
  - `cycle_event`
  - `station_event`
  - `production_unit`
  - `unit_state_history`
  - `quality_event`
  - `collector_runtime_status`
- 写回 `read_done`。
- 数据提交成功后才写回 `read_done`。
- ACK 写回失败标记 `ACK_WRITE_FAILED` 并在后续轮询重试。
- Collector 重启后通过 PLC 当前 payload 和数据库幂等键补 ACK。
- 同 boot counter 下降会记录 `PLC_COUNTER_RESET` 并停止 ACK。
- 连接、identity、读取/解码、存储和 ACK 错误写入 `collector_error_log`。

### API

- FastAPI 运行在 `8000`。
- 已有 KPI SVG 和 summary API。
- 新增三工站追溯：
  - `/trace`
  - `/trace/api`
  - `/trace/api/by-cycle`
  - `/trace/api/recent`

验证过：

- OK 件：`U-20260616-000001` -> WS01/WS02/WS03 三站完整，最终 `ASM-000001`。
- NOK 件：`U-20260616-000014` -> WS01=NOK，WS02/WS03=SKIPPED，最终 `ASM-000014` + `NG-000014`。
- `ASM-000014` 和 `NG-000014` 均可通过 `/trace/api` 查到完整三站。

### Grafana

已有 dashboard：

- `edge_mes_overview.json`
  - URL: `http://10.0.0.217:3000/d/edge-mes-overview`
  - 旧单线生产总览。
- `raspberry_pi_host_monitor.json`
  - URL: `http://10.0.0.217:3000/d/raspberry-pi-host-monitor`
  - 树莓派 CPU、内存、磁盘、温度等。
- `edge_mes_station_traceability.json`
  - URL: `http://10.0.0.217:3000/d/edge-mes-station-traceability`
  - 三工站 cycle time、产出、OK/NOK、NOK code、ACK、Collector 状态、最近追溯记录。

## 3. 当前文件结构

```text
edge-mes-demo/
  docker-compose.yml
  README.md
  .env.example

  api/
    Dockerfile
    requirements.txt
    app/
      main.py
      db.py
      routes/
        health.py
        machines.py
        kpi.py
        events.py
        sync.py
        trace.py

  collector/
    Dockerfile
    requirements.txt
    app/
      main.py
      config.py
      models.py
      plc/
        address.py
        decoder.py
        mapping.py
        read_plan.py
      services/
        storage.py
        event_detector.py
        event_collector.py
      sources/
        base.py
        simulator_source.py
        snap7_source.py

  s7_plc_sim/
    Dockerfile
    requirements.txt
    app/
      main.py
      plc_db.py
      pipeline.py
      control_api.py
      runtime_config.py
      parameter_audit.py
    tests/
      test_pipeline_uid_flow.py
      test_reliability.py
      test_runtime_config.py
      test_parameter_audit.py
      test_nok_simulation.py

  simulator/
    Dockerfile
    requirements.txt
    app/
      main.py
      models.py
      simulator.py

  sync_worker/
    Dockerfile
    requirements.txt
    app/
      main.py

  config/
    app.yaml
    vplc.yaml
    simulator.yaml
    plc_mapping.yaml
    mapping.yaml
    grafana/
      dashboards/
        dashboard.yaml
        edge_mes_overview.json
        edge_mes_station_traceability.json
        raspberry_pi_host_monitor.json
      datasources/
        postgres.yaml
        prometheus.yaml
      custom/
        grafana-custom-font.css
        grafana-custom.ttf
    prometheus/
      prometheus.yml

  db/
    init/
      001_schema.sql
      002_seed.sql
      003_event_schema.sql
      004_unit_trace_schema.sql

  scripts/
    generate_shift_demo_sql.py
    validate_edge_mapping.py
    read_s7_station_sample.py

  docs/
    architecture.md
    protocol.md
    task_plan.md
    decisions.md
    current_status.md
    edge_expansion_plan.md
    plc_edge_integration_guide.md
    edge_mes_demo_srs.md
    kpi_definitions.md
    custom_dashboard_plan.md
    plc_address_map.md
    scenario_control.md
```

说明：

- 目录中可能存在 `__pycache__`，它们不是源文件，不应作为文档依据。
- 部署时打包应排除 `__pycache__` 和 `*.pyc`。
- `edge_mes_demo_srs.md` 是当前正式技术方案与 SRS。
- `plc_edge_integration_guide.md` 是面向现场 PLC 工程师和技师的通用接入规范，覆盖 S7-300/S7-1200/S7-1500。
- `kpi_definitions.md` 是当前 KPI 口径与度量计划。
- `custom_dashboard_plan.md` 是后续自研 dashboard 与数字孪生首页规划。

## 4. 关键设计决策

- 本地数据库使用 PostgreSQL，远端 Oracle 仅作为未来同步目标。
- 保留旧 DB100 快照链路，避免旧 dashboard 失效。
- 新三工站协议使用 DB101/102/103。
- V-PLC 通过 Snap7 Server 模拟 S7。
- 三工站为并行 WIP，不是单线程顺序模拟。
- V-PLC 三工站从旧 simulator 的随机停机中解耦。
- Collector 旧快照采集和新事件采集并行运行。
- 当前追溯规则以 `unit_id` 为主关联键，`SUB/ASM/NG/序号` 只是查询入口。
- `cycle_event` 继续兼容旧查询；`station_event` 记录工站履历；`production_unit` 记录工件当前状态。
- Grafana 用于工程监控，自研数字孪生 dashboard 后续实现。
- 系统必须离线可运行。
- 高频信号由 MCU 或专用采集器采集，每个零件输出 CSV/JSON 文件，Edge 负责解析、特征提取、关联和归档。
- 参数管理只读校验，不主动回写 PLC；PLC 侧修改后通知 Edge 读取并记录 changelog。
- 工业相机图片/视频只做短期本地缓存，默认 7 天。
- 归档支持移动硬盘冷备份和服务器热备份，均作为可勾选任务。
- 权限管理需要支持账号、令牌和人脸/指纹等生物识别外设。
- AI 推理和长期数据处理放到 Nvidia 边缘设备或服务器，Edge 只接收结果。

## 5. 重要约束

- 当前 Demo 是单台设备、单条产线、单个 PLC；长期目标最多 3 条流水线。
- 当前树莓派是 8GB，SSD，性能足够当前 Demo。
- 不要破坏旧 `edge_mes_overview` dashboard。
- 不要删除旧 `production_snapshot` 链路。
- `config/plc_mapping.yaml` 是旧 DB100 映射。
- `config/mapping.yaml` 是新三工站协议映射。
- DB100 当前存在 legacy 兼容，不应直接假设已经完全符合新协议。
- V-PLC 当前端口 1102；真实 PLC 可能为 102。
- 默认严格 ACK；deadline 默认 10 秒，未 ACK payload 不会自动清除或被覆盖。
- 当前 API/Grafana 无生产级认证设计。
- Oracle / `sync-worker` 属于 Phase-2 Out of Scope；当前只保留 mock，不实施真实 Oracle 集成。
- 电子 SOP 暂不需要。
- 维护保养模块暂不需要。
- 图片/视频长期存储不放在树莓派本地。
- 高频原始信号不由树莓派直接采集。

## 6. 未完成事项

高优先级：

- 实现 Ignore Edge / Bypass 与 `data_gap_event`。
- 在树莓派 PostgreSQL 执行 `db/migrations/005_reliability_schema.sql` 并完成容器级故障恢复验收。

中优先级：

- 增强追溯 API，显示缺站原因和采集缺口边界。
- 对旧历史数据执行一次可选回填，将已有 `cycle_event` 尽量派生为 `station_event` / `production_unit`。
- Grafana 增加数据质量面板。
- V-PLC 增加断线、写失败、ACK 失败模拟。
- 增加故障注入控制项，便于手工触发 ACK 写失败和断线。
- 参数管理与 changelog。
- MCU CSV/JSON 文件接入与特征提取。
- 工业相机图片/视频元数据与 7 天保留。
- 归档任务管理。
- 权限、令牌和生物识别适配。

后续产品化：

- 自研 dashboard。
- 3D 设备/物料流动数字孪生首页。
- 用户权限、审计日志、配置持久化。
- 真实 PLC 接入演练。
- AI / Nvidia 边缘设备结果接入。

## 7. 下一步建议

可靠性代码闭环已完成；建议下一步按以下顺序推进：

1. 部署迁移与容器验收
   - 在树莓派执行 `db/migrations/005_reliability_schema.sql`。
   - 重建 V-PLC / Collector，执行断线、重启、ACK timeout 和 reset 验收。

2. Ignore Edge / data gap
   - 正式启用整线 `ignore_edge` bit。
   - 数据缺口写入 `data_gap_event`。
   - 按 WS03 label_code 序号计算缺件。

3. 验证与回归
   - 建立可靠性、数据缺口和端到端验证矩阵。
   - 保存每个 Thread 的验证报告。

4. 自研 dashboard 初版
   - 不替代 Grafana 工程看板。
   - 面向操作员/管理层。
   - 为后续 3D 数字孪生做入口。

Phase-2 Out of Scope：

- Oracle schema、真实连接、主动 push、重试和幂等。
- `sync-worker` 只保留现有 mock 行为，不作为本阶段验收项。

## 8. 常用命令

树莓派：

```bash
cd /opt/edge-mes-demo
docker compose ps
docker logs --tail 80 edge-mes-collector
docker logs --tail 80 edge-mes-s7-plc-sim
docker exec edge-mes-postgres psql -U edge_mes -d edge_mes
```

本地校验：

```bash
python3 -m compileall api/app collector/app s7_plc_sim/app
python3 scripts/validate_edge_mapping.py
python3 -m json.tool config/grafana/dashboards/edge_mes_station_traceability.json
```

追溯 API 示例：

```bash
curl 'http://10.0.0.217:8000/trace/api?q=ASM-000014'
curl 'http://10.0.0.217:8000/trace/api?q=NG-000014'
curl 'http://10.0.0.217:8000/trace/api/by-cycle?station_id=WS03&cycle_counter=14'
```
