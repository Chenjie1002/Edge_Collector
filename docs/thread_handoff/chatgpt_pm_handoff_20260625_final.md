# Edge MES Demo — ChatGPT PM Handoff Final

Date: 2026-06-25
Handoff owner: outgoing ChatGPT PM
Next owner: new ChatGPT PM
Project path: `/Users/chenjie/Documents/MES/edge-mes-demo`

## 1. Purpose

This handoff is the latest PM continuity note after Sprint 3 offline adapter implementation, R-N1/R-N2 hardening, docs/status consolidation, and baseline repair.

Use this file only as a PM continuity artifact. The durable repository truth sources are:

```text
docs/thread_handoff/pm_operating_rules.md
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/contracts/collector_ingestion_adapter.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
docs/DOC_INDEX.md
```

## 2. Current repository baseline

Current verified baseline at handoff:

```text
HEAD / origin/main:
4f424c6ada57e936c8e6d92c49f66414a55ea9c1

latest commit:
4f424c6 Repair Sprint 3 current baseline status

branch:
main

Phase-1 tag:
phase1-pass-20260619
```

Recent commits:

```text
4f424c6 Repair Sprint 3 current baseline status
fd79e21 Sync Sprint 3 hardening gate status
577c1a1 Harden Sprint 3 collector adapter recommendations
b930c0e Consolidate PM operating rules and Sprint 3 gate status
b43a12f Implement Sprint 3 collector ingestion adapter offline slice
4e0e1f1 Plan Sprint 3 collector ingestion adapter boundary
1a22cdc Clarify Sprint 2 closeout repository baseline
82b2127 Close out Sprint 2 documentation state
```

## 3. Current working tree

Final verified dirty tree before handoff:

```text
 M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
```

This new handoff file may also appear as untracked after creation:

```text
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
```

Meaning:

- `.gitignore` is a pre-existing dirty artifact and must remain excluded unless PM explicitly authorizes it.
- PM handoff files and Keynote/reporting artifacts are external local continuity/reporting artifacts and must remain excluded unless PM explicitly authorizes them.
- Do not use `git add .`, `git add -A`, or `git add docs/`.

## 4. Sprint 3 status at handoff

Sprint 3 Collector Ingestion Adapter status:

```text
Offline adapter implementation: completed, reviewed, committed, pushed
R-N1/R-N2 recommendation hardening: completed, reviewed, committed, pushed
Docs/status sync and baseline repair: completed, committed, pushed
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Verification focused review: PASS WITH RECOMMENDATIONS, no blocker
Runtime Collector integration: not authorized
DB/API/Dashboard/V-PLC/deploy/tag/rollback/real PLC pilot: not authorized
```

Implemented offline adapter files:

```text
collector/app/services/resolved_config_registry.py
collector/app/services/station_event_adapter.py
tests/test_collector_station_event_adapter.py
```

R-N1/R-N2 hardening closeout:

```text
R-N1 / DQ-N1 / V-N1:
CLOSED. Resolved snapshot content hash self-check implemented. Tampered snapshot content with unchanged config_hash field is rejected as CONFIG_HASH_MISMATCH before normalized event, lifecycle, or projection output.

R-N2 / DQ-N2 / V-N2:
CLOSED. Route predecessor mismatch and non-system-reserved direct parent mismatch negative fixtures are separated and assertion paths are clearer.
```

## 5. Important preserved recommendations

These are not blockers for the committed hardening slice:

```text
Reliability recommendation:
If future registries allow non-ResolvedConfigSnapshot duck-typed snapshots, require an equivalent content_hash_matches() protocol or fail closed.

Reliability recommendation:
Future runtime/fixture decoders should use a stable explicit decoder id. Current module.qualname identity is acceptable for this offline fixture slice.

Data Quality recommendation:
Any newly modeled resolved snapshot field that can affect adapter interpretation must be added to compute_resolved_config_hash() in the same change.

Data Quality recommendation:
If future registries can return non-ResolvedConfigSnapshot objects, require equivalent content-hash verification.

Verification recommendation:
Any future commit must keep exact allowlist staging and continue excluding .gitignore, PM handoff artifacts, and Keynote/reporting artifacts.
```

## 6. Next recommended PM action

The next stage should be a fresh runtime integration planning gate.

Do not authorize runtime implementation directly.

Recommended next PM task:

```text
Architecture / Integration — Sprint 3 runtime integration planning gate
```

New PM should open a fresh PM window and ask Codex to run a new Architecture / Integration planning Thread.

The next gate should be planning-only:

- no file modification;
- no stage;
- no commit;
- no push;
- no runtime implementation;
- no DB/API/Dashboard/V-PLC/deploy/tag/rollback/real PLC pilot.

## 7. Runtime integration planning direction from previous HOLD gate

A prior planning attempt returned HOLD because docs/current baseline still referenced `577c1a1` as current status while actual HEAD was `fd79e21`. That blocker has since been repaired and committed at `4f424c6`.

The useful planning findings from that HOLD report were:

```text
Proposed runtime integration boundary:
- Collector entry likely belongs in EventCollectorWorker._process_station().
- Adapter should run after decode_read_plan() and payload/cycle/counter readiness checks, before storage.persist_cycle().
- Runtime source payload should be built from decoded payload + raw_hex + runtime station/mapping/plc_boot_id/observed_at.
- source_event_id must be deterministic from plc_id/station_id/plc_boot_id/cycle_counter/event_type, not random or retry-time dependent.
- Runtime registry construction must generate ResolvedConfigSnapshot from an immutable reviewed mapping snapshot.
- Accepted adapter decisions may proceed to existing storage.persist_cycle() and existing persist-then-ACK/read_done behavior.
- Rejected/deferred/quarantined/duplicate/conflict/raw_variant decisions must not write new production outcome/projection/defect detail.
- Adapter must not become ACK owner. ACK/read_done remains owned by existing EventCollectorWorker after storage success.
```

Suggested split:

```text
Slice A:
runtime source payload builder + runtime resolved config registry + focused tests; still no ACK/DB integration.

Slice B:
integrate adapter gate in EventCollectorWorker._process_station(); accepted path goes to existing persist_cycle(); non-accepted path writes diagnostic/error only and does not ACK unless separately approved.

Slice C:
future projection/DB schema/API/Dashboard work, not part of the next immediate slice.
```

Key open risk:

```text
config/mapping.yaml currently has no explicit runtime config_hash, mapping_id, payload_template, station_type, cycle_profile, or raw policy fields. Runtime registry construction needs a reviewed deterministic mapping contract before implementation.
```

## 8. Suggested first message for new ChatGPT PM

Use this in a fresh ChatGPT PM window:

```text
你现在作为新的 ChatGPT PM，接手 Edge MES Demo 项目。

请先读取：
- docs/thread_handoff/pm_operating_rules.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/contracts/collector_ingestion_adapter.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
- docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md

当前 baseline：
- 4f424c6ada57e936c8e6d92c49f66414a55ea9c1
- 4f424c6 Repair Sprint 3 current baseline status

当前状态：
- Sprint 3 offline adapter implementation 已完成并提交。
- R-N1/R-N2 hardening 已完成并提交。
- docs/status baseline repair 已完成并提交。
- Reliability / Data Quality / Verification focused review 均为 PASS WITH RECOMMENDATIONS，无 blocker。
- runtime Collector integration 尚未授权。
- DB/API/Dashboard/V-PLC/deploy/tag/rollback/real PLC pilot 均未授权。

当前目标：
重新开启 Architecture / Integration — Sprint 3 runtime integration planning gate。

要求：
- 只做 planning，不做 implementation。
- 先核对 HEAD / origin/main 与 docs/current_status.md 是否一致。
- 评估是否需要新 Codex Thread。
- 返回 runtime integration boundary、minimal slice、allowlist proposal、test plan、required focused reviews。
```

## 9. Suggested Codex prompt for the next gate

```text
报告名称：
Architecture / Integration — Sprint 3 runtime integration planning gate report

任务名称：
Plan runtime Collector integration boundary after Sprint 3 offline adapter hardening closeout

执行 Thread：
Architecture / Integration

PM 任务前工作量评估：
- 任务规模：中
- 涉及范围：Collector runtime integration planning、boundary design、allowlist proposal、test strategy
- 是否需要新开 Thread：建议新开 Architecture / Integration Thread
- 理由：Sprint 3 offline adapter implementation、R-N1/R-N2 hardening、docs/status sync/baseline repair 已完成并提交；下一步是新的 runtime integration planning gate，可能涉及 Collector runtime、storage、ACK/read_done、DB write path 与 regression scope，需要独立上下文，避免和前序 implementation/review/commit 线程混在一起。

请先读取：
- docs/thread_handoff/pm_operating_rules.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/contracts/collector_ingestion_adapter.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
- collector/app/services/resolved_config_registry.py
- collector/app/services/station_event_adapter.py
- collector/app/main.py
- collector/app/services/event_collector.py
- collector/app/services/storage.py
- collector/app/plc/decoder.py
- collector/app/plc/mapping.py
- tests/test_collector_station_event_adapter.py

背景：
当前 baseline：
- 4f424c6ada57e936c8e6d92c49f66414a55ea9c1
- 4f424c6 Repair Sprint 3 current baseline status

当前状态：
- Sprint 3 offline adapter implementation 已完成。
- R-N1/R-N2 hardening 已完成。
- Docs/status baseline repair 已完成。
- Reliability / Data Quality / Verification focused review 均为 PASS WITH RECOMMENDATIONS，无 blocker。
- 当前尚未授权 runtime Collector integration。
- DB/API/Dashboard/V-PLC/deploy/tag/rollback/real PLC pilot 均未授权。

本轮任务：
1. 只做 runtime integration planning gate，不修改文件。
2. 梳理当前 offline adapter 如何接入 Collector runtime，但不要实现。
3. 明确 runtime integration 的最小边界。
4. 判断 runtime integration 是否应拆成多个 slice。
5. 返回 proposed exact implementation allowlist。
6. 返回 proposed test plan。
7. 明确需要 Reliability / Data Quality / Verification 哪些 review gate。
8. 不要 stage，不要 commit，不要 push。

必须排除：
- .gitignore
- PM handoff artifacts
- Keynote/reporting artifacts
- DB migration files
- API files
- Dashboard/frontend files
- V-PLC files
- deploy/tag/rollback files
- real PLC pilot work

不要修改文件。
不要 stage。
不要 commit。
不要 push。
不要进入 implementation。

返回窗口短报告，格式遵守 docs/thread_handoff/pm_operating_rules.md。
```
