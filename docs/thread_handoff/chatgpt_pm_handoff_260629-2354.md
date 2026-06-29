# Edge MES Demo — ChatGPT PM Handoff 260629-2354

你现在接手 Edge MES Demo 项目的 ChatGPT PM 工作。

用户偏好：中文为主。
PM 角色：负责规划、授权边界、Thread 调度、报告 intake、exact-path stage/commit/push gate。
不要未经授权直接 implementation、deploy、tag、rollback、stage、commit、push。

---

## 1. 项目路径

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

---

## 2. 新 PM 接手第一步

第一步必须执行 read-only recovery，不要直接继续任务。

建议命令：

```bash
git status -sb
printf '\n--- log -12 ---\n' && git log --oneline -12
printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
printf '\n--- origin/main ---\n' && git show-ref --hash refs/remotes/origin/main
printf '\n--- diff name-only ---\n' && git diff --name-only
printf '\n--- cached name-only ---\n' && git diff --cached --name-only
```

然后读取：

```text
docs/thread_handoff/pm_operating_rules.md
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
docs/contracts/collector_ingestion_adapter.md
```

---

## 3. 当前 Git baseline

当前主线已同步：

```text
HEAD == origin/main == 50c37c75cef4eba99e65238da64a6ecc4ae9d006
```

最新 commit：

```text
50c37c7 Sync Sprint 3 Slice H gate status
```

最近关键 commits：

```text
50c37c7 Sync Sprint 3 Slice H gate status
c7e80e8 Roll out Slice H WS02 raw policy authority
44ed02d Sync Sprint 3 Slice G gate status
398f11c Harden Slice G raw policy sanity tests
e8650f1 Add PM handoff timestamp naming rule
0443b80 Sync Sprint 3 Slice F2 gate status
829d5c7 Implement Sprint 3 Slice F2 raw policy authority
734ba52 Sync Sprint 3 Slice F1 gate status
ac1838c Freeze Sprint 3 Slice F1 raw_policy authority
d02b98d Sync Sprint 3 Slice E1 gate status
2c73410 Repair Sprint 3 Slice E1 runtime raw decoder
dac87c1 Add PM task risk tier rules
```

Durable status sync is complete for Slice H at `50c37c7`.

---

## 4. 当前 working tree

当前剩余 dirty 是已知 external artifacts，不属于当前开发闭环：

```text
M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
```

本 handoff 文件本身为新文件：

```text
docs/thread_handoff/chatgpt_pm_handoff_260629-2354.md
```

重要规则：

```text
Do not stage .gitignore unless explicitly authorized by exact path.
Do not stage old PM handoff / Keynote artifacts unless explicitly authorized by exact path.
Do not use git add .
Do not use git add -A.
Do not use git add docs/.
```

任何 stage/commit/push 必须 exact-path allowlist，并由用户明确授权。

---

## 5. 当前 Sprint 3 状态

当前主线：Phase 2 Sprint 3 Collector Ingestion Adapter。

已闭环到：

```text
Sprint 3 Slice H WS02 raw_policy raw_capable authority implementation: CLOSED
```

Slice H implementation commit：

```text
c7e80e8 Roll out Slice H WS02 raw policy authority
c7e80e8e931b5f23d6ea42fee7b10b27191b5e20
```

Slice H docs/status sync commit：

```text
50c37c7 Sync Sprint 3 Slice H gate status
50c37c75cef4eba99e65238da64a6ecc4ae9d006
```

Slice H gate 状态：

```text
Slice H WS02 raw_policy raw_capable rollout planning: PASS WITH RECOMMENDATIONS
Slice H Architecture / Integration implementation: PASS
Slice H Reliability focused implementation review: PASS WITH RECOMMENDATIONS, no blocker
Slice H Data Quality focused implementation review: PASS WITH RECOMMENDATIONS, no blocker
Slice H Verification exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
Slice H exact config/test commit/push: PASS, commit c7e80e8
Slice H docs/status sync: PASS, commit 50c37c7
```

当前没有挂起的 review gate、commit gate、status sync gate。

Durable status references：

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
docs/contracts/collector_ingestion_adapter.md
```

`docs/current_status.md` 和 `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md` 已同步 Slice H。

---

## 6. Slice H 技术摘要

Slice H 是 F2/F1 后的 narrow Level 2 mapping/config authority rollout。

目标：

```text
仅将 WS02 / ws02_runtime_v1 / station_runtime_payload_v1 的 station-level raw_policy 推进为 raw_capable。
```

Committed files：

```text
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

行为结果：

```text
- WS01 remains raw_capable
- WS02 station-level raw_policy: raw_capable
- WS03 remains raw_not_provided
- line-wide runtime_defaults.raw_policy remains raw_not_provided
- raw_required not introduced
- runtime/source code unchanged
- storage.py unchanged
- DB/API/Dashboard/frontend unchanged
- V-PLC behavior unchanged
- Docker/deploy unchanged
- ACK/read_done ownership unchanged
```

Evidence / authority semantics：

```text
- WS02 raw_capable is explicit mapping/config authority from config/mapping.yaml.
- WS02 raw evidence is WS02 source-builder raw bytes; it is not inherited from WS01 upstream evidence.
- raw_payload.raw_hex remains evidence only, not production fact.
- normalized payload remains present and is not replaced by raw evidence.
- source-builder payload is not a DB/API/Dashboard-visible production fact by itself.
- accepted adapter decision remains the side-effect gate before persist/ACK.
- rejected/diagnostic decisions do not project, persist, ACK or become DB/API/Dashboard-visible production facts.
```

Tests added/updated:

```text
- WS01/WS02 declare raw_capable while line-wide default remains raw_not_provided.
- WS02 nominal raw source-builder path emits raw_payload.raw_hex and preserves normalized payload.
- WS02 missing raw raises RAW_EVIDENCE_MISSING fail-closed.
- WS03 remains raw_not_provided normalized-only.
- snapshot.config_hash == mapping.runtime_snapshot.config_hash lineage assertion.
- direct YAML assertion keeps runtime_defaults.raw_policy at raw_not_provided.
```

Validation evidence reported by Threads:

```text
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=collector:. .venv/bin/python -m pytest -p no:cacheprovider tests/test_collector_station_event_runtime_source.py
51 passed

PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=collector:. .venv/bin/python -m pytest -p no:cacheprovider collector/tests/test_event_collector_adapter_gate.py
30 passed

git diff --check
PASS
```

Carry-forward recommendation, not blocker:

```text
Future tests may extract a cwd-agnostic helper for direct YAML/config assertions.
Current repo-root pytest gate accepts Path("config/mapping.yaml") + yaml.safe_load.
```

---

## 7. Slice G 摘要

Slice G 是 WS01 raw_capable 后的 tests-only hardening。

Commits：

```text
398f11c Harden Slice G raw policy sanity tests
44ed02d Sync Sprint 3 Slice G gate status
```

Scope：

```text
- Changed only tests/test_collector_station_event_runtime_source.py in implementation commit.
- Added real config/mapping.yaml source-builder sanity for WS01 raw_capable nominal raw evidence.
- Added WS01 missing raw RAW_EVIDENCE_MISSING fail-closed sanity.
- Added WS02/WS03 raw_not_provided normalized-only regression before Slice H.
- No config change.
- No runtime/source code change.
- No storage.py / DB / API / Dashboard / V-PLC / deploy / ACK/read_done change.
```

---

## 8. Slice F2 摘要

Slice F2 是 WS01 raw_policy raw_capable authority rollout。

Commits：

```text
829d5c7 Implement Sprint 3 Slice F2 raw policy authority
0443b80 Sync Sprint 3 Slice F2 gate status
```

Scope：

```text
- Changed config/mapping.yaml and tests/test_collector_station_event_runtime_source.py.
- WS01 station-level raw_policy became raw_capable.
- WS02 / WS03 remained raw_not_provided at that time.
- line-wide default remained raw_not_provided.
- raw_required not introduced.
- runtime/source code unchanged.
```

---

## 9. Sprint 3 completed chain since F1

```text
F1 raw_policy authority docs/contracts freeze: CLOSED at ac1838c / 734ba52
F2 WS01 raw_capable authority: CLOSED at 829d5c7 / 0443b80
PM handoff timestamp naming rule: CLOSED at e8650f1
Slice G WS01 raw_capable post-commit sanity tests-only hardening: CLOSED at 398f11c / 44ed02d
Slice H WS02 raw_capable authority: CLOSED at c7e80e8 / 50c37c7
```

Older Sprint 3 slices already closed and documented in durable status:

```text
Offline adapter implementation
R-N1/R-N2 hardening
Slice A mapping contract hardening
Slice B runtime adapter gate
Slice C runtime adapter diagnostic observability hardening
Slice D1 raw boundary test-only hardening
Slice D2-A decoder authority docs/contract-only repair
Slice D2-B decoder authority tests-only hardening
Slice D2-C decoder registry authority
Slice D3 runtime raw wiring
Slice E1 runtime raw decoder repair
```

---

## 10. Process and authorization rules to preserve

Thread roles:

```text
Architecture / Integration: planning, contracts, implementation under PM allowlist, status sync
Reliability: runtime safety, ACK/read_done, fail-closed, side effects
Data Quality: fact authority, lineage, projection, raw/normalized evidence
Verification: test matrix, regressions, exact allowlist audit
PM: report intake, gate sequencing, exact-path stage/commit/push after explicit authorization
```

Risk tiers:

```text
Level 0: PM direct exact-path commit/push, small mechanical status sync
Level 1: focused docs/tests/contracts changes with no runtime or authority semantics
Level 2: runtime behavior, PLC/V-PLC, ACK/read_done, DB write path, storage.py, decoder/registry authority, raw/normalized evidence, schema/config semantics
```

Important: mapping/config `raw_policy` authority change is Level 2 even if it is a one-line diff.

Never infer authorization from a PASS report. The user must explicitly authorize implementation, tests, staging, commit, push, deploy, tag or rollback.

---

## 11. Current recommended next step

Do not start a new implementation immediately.

Recommended first action for the next PM window:

```text
1. Perform read-only recovery.
2. Confirm HEAD == origin/main == 50c37c75cef4eba99e65238da64a6ecc4ae9d006.
3. Confirm working tree only has expected external artifacts plus this handoff file state, depending on whether the current PM commits it.
4. Confirm there are no pending review/commit/status gates.
5. Decide the next planning target.
```

Reasonable next planning options:

```text
Option A: Sprint 3 Slice I planning — WS03 raw_capable rollout feasibility.
Option B: Pause Sprint 3 raw_policy rollout and plan a broader status/quality checkpoint.
Option C: Plan cleanup of cwd-agnostic config assertion helper as a low-risk test hygiene task, only if PM decides it is worth doing.
```

Recommendation:

```text
If continuing raw_policy rollout, choose Option A as planning-only first:
Sprint 3 Slice I planning — WS03 single-station raw_capable rollout feasibility / boundary / gate design.
Do not directly implement WS03.
Do not introduce raw_required.
Do not touch runtime/source code, storage.py, DB/API/Dashboard/V-PLC/deploy, or ACK/read_done.
```

---

## 12. Suggested prompt for the next ChatGPT PM

Use this prompt when opening a new ChatGPT PM window:

```text
@Devspace
# Edge MES Demo 项目交接

你的角色设定是一位项目经理，需要阅读下面的交接文件和补充说明，接手该项目的开发。

交接文件绝对路径：
/Users/chenjie/Documents/MES/edge-mes-demo/docs/thread_handoff/chatgpt_pm_handoff_260629-2354.md

## 1. 当前真正 baseline

HEAD == origin/main == 50c37c75cef4eba99e65238da64a6ecc4ae9d006

latest commit:
50c37c7 Sync Sprint 3 Slice H gate status

下一位 PM 接手第一步必须执行 read-only recovery，不要直接继续任务。

## 2. 当前 closed 状态

Sprint 3 Slice H WS02 raw_policy raw_capable authority: CLOSED
Slice H docs/status sync: CLOSED
当前没有挂起的 review gate、commit gate、status sync gate。

## 3. 剩余 dirty 不属于当前任务

以下 dirty / untracked artifacts 是 external artifacts，不是待处理技术变更，不要顺手 stage：

M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

## 4. 第一轮任务

先做 read-only recovery，并给出下一步建议。
优先考虑 Sprint 3 Slice I planning — WS03 single-station raw_capable rollout feasibility。
不要直接 implementation。
```

---

## 13. Handoff commit note

This handoff file was generated after Slice H docs/status sync.
If committing this file, use exact path only:

```text
docs/thread_handoff/chatgpt_pm_handoff_260629-2354.md
```

Suggested commit message:

```text
Add PM handoff after Slice H status sync
```

Do not stage `.gitignore` or old PM handoff / Keynote artifacts.
