# Sprint 3 Collector Ingestion Adapter Gate Status

Updated: 2026-06-27

Purpose: compact current gate/status source for Codex Threads working on Sprint 3 Collector Ingestion Adapter.

Read this file together with:

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- `docs/contracts/collector_ingestion_adapter.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`

## 1. Last verified baseline

```text
last verified HEAD / origin/main at authoring time:
0358b6047fd657e272e636d2c8754a26bf793c03
0358b60 Harden Sprint 3 Slice D1 raw boundary tests

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

Slice name:

```text
Collector ingestion adapter offline fixtures
```

Input/output boundary:

```text
source payload fixture
-> normalized station_event envelope
-> shared validation helpers
-> lifecycle output
-> offline projection metadata
-> adapter diagnostic decision wrapper
```

Explicit non-goals for the current slice:

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

Current overall status:

```text
Sprint 3 Collector Ingestion Adapter offline implementation and R-N1/R-N2 hardening: implemented, reviewed, committed and pushed.
Sprint 3 Slice A mapping contract hardening: implemented, reviewed, committed and pushed at 706f5da.
Sprint 3 Slice B runtime adapter gate: implemented, reviewed, committed and pushed at c677515.
Sprint 3 Slice C runtime adapter diagnostic observability hardening: implemented, reviewed, committed and pushed at e02e39d.
Sprint 3 Slice D1 raw boundary test-only hardening: implemented, reviewed, committed and pushed at 0358b60.
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
Docs/status sync completed at fd79e21.
Docs/status baseline repair completed at 4f424c6.
PM rules / baseline semantics repair pre-baseline: e284a06 Repair PM rules and Sprint 3 baseline status.
Eligible for downstream PM planning for D2 decoder registry / decoder callable authority: yes.
D2 decoder registry / decoder callable authority remains separate and requires PM approval.
D3 actual raw-capable/raw-required runtime wiring remains HOLD until D2 authority is resolved.
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
D3 actual raw-capable/raw-required runtime wiring remains HOLD until D2 authority is resolved.
raw_capable/raw_required missing raw remains fail-closed unless PM approves contract change.
Adapter diagnostics remain read-only observability, not ACK policy or production policy.
No schema/config/mapping/storage/API/Dashboard/V-PLC/deploy work without separate PM approval.
```

Required exclusions for future tasks remain:

```text
.gitignore
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
