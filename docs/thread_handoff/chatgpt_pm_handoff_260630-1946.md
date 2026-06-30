# Edge MES Demo — ChatGPT PM Handoff 260630-1946

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
HEAD == origin/main == ae8787eed9dde7ba56eaac7a66b7eb4990cf57bf
```

最新 commit：

```text
ae8787e Sync Sprint 3 Slice I gate status
```

最近关键 commits：

```text
ae8787e Sync Sprint 3 Slice I gate status
045d21c Roll out Slice I WS03 raw policy authority
7f576be Repair PM handoff baseline semantics
44f2446 Add PM handoff and UTC+8 handoff workflow
50c37c7 Sync Sprint 3 Slice H gate status
c7e80e8 Roll out Slice H WS02 raw policy authority
44ed02d Sync Sprint 3 Slice G gate status
398f11c Harden Slice G raw policy sanity tests
e8650f1 Add PM handoff timestamp naming rule
0443b80 Sync Sprint 3 Slice F2 gate status
829d5c7 Implement Sprint 3 Slice F2 raw policy authority
734ba52 Sync Sprint 3 Slice F1 gate status
```

Durable status sync is complete for Slice I at `ae8787e`.

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
docs/thread_handoff/chatgpt_pm_handoff_260630-1946.md
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

当前主线：Phase-2 Sprint 3 Collector Ingestion Adapter。

已闭环到：

```text
Sprint 3 Slice I WS03 raw_policy raw_capable authority implementation: CLOSED
Slice I docs/status sync: CLOSED
```

Slice I implementation commit：

```text
045d21c Roll out Slice I WS03 raw policy authority
045d21c14436e8fe13a26bc32b7c2956df0cd99f
```

Slice I docs/status sync commit：

```text
ae8787e Sync Sprint 3 Slice I gate status
ae8787eed9dde7ba56eaac7a66b7eb4990cf57bf
```

Slice I gate 状态：

```text
Slice I WS03 raw_policy raw_capable rollout planning: PASS WITH RECOMMENDATIONS
Slice I Architecture / Integration implementation: PASS
Slice I Reliability focused implementation review: PASS, no blocker
Slice I Data Quality focused implementation review: PASS, no blocker
Slice I Verification exact allowlist audit: PASS, no blocker
Slice I exact config/test commit/push: PASS, commit 045d21c
Slice I docs/status sync: PASS, commit ae8787e
```

当前没有挂起的 review gate、commit gate、status sync gate。

Durable status references：

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
docs/contracts/collector_ingestion_adapter.md
```

`docs/current_status.md` 和 `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md` 已同步 Slice I。

---

## 6. Slice I 技术摘要

Slice I 是 Slice H 后的 narrow Level 2 mapping/config authority rollout。

目标：

```text
仅将 WS03 / ws03_runtime_v1 / station_runtime_payload_v1 的 station-level raw_policy 推进为 raw_capable。
```

Committed files：

```text
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

行为结果：

```text
- WS01 remains raw_capable
- WS02 remains raw_capable
- WS03 station-level raw_policy: raw_capable
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
- WS03 raw_capable is explicit mapping/config authority from config/mapping.yaml.
- WS03 raw evidence is WS03 source-builder raw bytes; it is not inherited from WS01/WS02 upstream evidence.
- raw_payload.raw_hex remains evidence only, not production fact.
- normalized payload remains present and is not replaced by raw evidence.
- source-builder payload is not a DB/API/Dashboard-visible production fact by itself.
- accepted adapter decision remains the side-effect gate before persist/ACK.
- rejected/diagnostic decisions do not project, persist, ACK or become DB/API/Dashboard-visible production facts.
```

Tests added/updated:

```text
- WS01/WS02/WS03 declare station-level raw_capable while line-wide default remains raw_not_provided.
- WS03 nominal raw source-builder path emits raw_payload.raw_hex and preserves normalized payload.
- WS03 missing raw raises RAW_EVIDENCE_MISSING fail-closed.
- WS01/WS02 raw_capable regressions remain covered.
- snapshot.config_hash == mapping.runtime_snapshot.config_hash lineage assertion remains covered.
- direct YAML assertion keeps runtime_defaults.raw_policy at raw_not_provided.
```

Validation evidence reported by Threads:

```text
TDD red check before config change: 3 failed, 49 passed; failures showed WS03 still raw_not_provided

PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=collector:. .venv/bin/python -m pytest -p no:cacheprovider tests/test_collector_station_event_runtime_source.py
52 passed

PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=collector:. .venv/bin/python -m pytest -p no:cacheprovider collector/tests/test_event_collector_adapter_gate.py
30 passed

git diff --check
PASS

git diff --cached --check before commit
PASS
```

Slice I review result:

```text
Reliability focused review: PASS, no blocker.
Data Quality focused review: PASS, no blocker.
Verification exact allowlist audit: PASS, no blocker.
```

---

## 7. Slice H 摘要

Slice H 是 WS02 raw_capable authority rollout。

Commits：

```text
c7e80e8 Roll out Slice H WS02 raw policy authority
50c37c7 Sync Sprint 3 Slice H gate status
```

Scope：

```text
- Changed config/mapping.yaml and tests/test_collector_station_event_runtime_source.py.
- WS02 station-level raw_policy became raw_capable.
- WS01 remained raw_capable.
- WS03 remained raw_not_provided at that time.
- line-wide runtime_defaults.raw_policy remained raw_not_provided.
- raw_required not introduced.
- runtime/source code unchanged.
```

---

## 8. Slice G / F2 摘要

Slice G 是 WS01 raw_capable 后的 tests-only hardening。

Commits：

```text
398f11c Harden Slice G raw policy sanity tests
44ed02d Sync Sprint 3 Slice G gate status
```

Slice F2 是 WS01 raw_policy raw_capable authority rollout。

Commits：

```text
829d5c7 Implement Sprint 3 Slice F2 raw policy authority
0443b80 Sync Sprint 3 Slice F2 gate status
```

F2/Slice G 后 WS01 raw_capable authority 与 real mapping tests 已闭环。Slice H/Slice I 后 WS02、WS03 也已完成 station-level raw_capable rollout。

---

## 9. Sprint 3 completed chain since F1

```text
F1 raw_policy authority docs/contracts freeze: CLOSED at ac1838c / 734ba52
F2 WS01 raw_capable authority: CLOSED at 829d5c7 / 0443b80
PM handoff timestamp naming rule: CLOSED at e8650f1
Slice G WS01 raw_capable post-commit sanity tests-only hardening: CLOSED at 398f11c / 44ed02d
Slice H WS02 raw_capable authority: CLOSED at c7e80e8 / 50c37c7
PM handoff + UTC+8 workflow / baseline semantics: CLOSED at 44f2446 / 7f576be
Slice I WS03 raw_capable authority: CLOSED at 045d21c / ae8787e
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
Level 0: PM direct exact-path commit/push, small PM rule edits, simple status/hash sync, mechanical docs updates
Level 1: focused docs/tests/contracts changes with no runtime or authority semantics
Level 2: runtime behavior, PLC/V-PLC, ACK/read_done, DB write path, storage.py, decoder/registry authority, raw/normalized evidence, schema/config semantics
```

Important: mapping/config `raw_policy` authority change is Level 2 even if it is a one-line diff.

Never infer authorization from a PASS report. The user must explicitly authorize implementation, tests, staging, commit, push, deploy, tag or rollback.

PM direct tasks such as exact-path commit/push or docs/status sync should be executed by PM after explicit authorization; do not generate a separate Thread prompt for PM-only execution.

Future task prompts for Threads should be returned as one complete copyable Markdown block and should not include `@Devspace`.

---

## 11. Current recommended next step

Do not start a new implementation immediately.

Recommended first action for the next PM window:

```text
1. Perform read-only recovery.
2. Confirm HEAD == origin/main == ae8787eed9dde7ba56eaac7a66b7eb4990cf57bf.
3. Confirm working tree only has expected external artifacts plus this handoff file state, depending on whether the current PM commits it.
4. Confirm there are no pending review/commit/status gates.
5. Decide the next planning target.
```

Reasonable next planning options:

```text
Option A: Sprint 3 raw_policy rollout checkpoint — confirm all three stations are now raw_capable and decide whether raw_policy rollout is complete for Sprint 3.
Option B: Pause Sprint 3 raw_policy rollout and plan a broader status/quality checkpoint.
Option C: Plan a low-risk test hygiene task, for example cwd-agnostic config assertion helper, only if PM decides it is worth doing.
Option D: Start planning the next downstream Sprint 3 area, while keeping DB/API/Dashboard/V-PLC/deploy/ACK/storage.py changes under separate explicit authorization.
```

Recommendation:

```text
Pause after Slice I closure and start with a read-only checkpoint / next-slice planning decision.
Do not introduce raw_required by default.
Do not touch runtime/source code, storage.py, DB/API/Dashboard/V-PLC/deploy, or ACK/read_done without a new Level 2 plan and explicit PM authorization.
```

---

## 12. Suggested prompt for the next ChatGPT PM

Use this prompt when opening a new ChatGPT PM window. Keep it as one copyable Markdown block.

```markdown
# Edge MES Demo — ChatGPT PM 接手 Prompt

你的角色是一位 ChatGPT PM，负责接手 Edge MES Demo 项目的开发管理、Thread 调度、gate 判断、报告 intake、授权边界控制，以及 exact-path stage/commit/push gate。

请先阅读交接文件：

/Users/chenjie/Documents/MES/edge-mes-demo/docs/thread_handoff/chatgpt_pm_handoff_260630-1946.md

然后读取并遵守 PM 规则文件：

/Users/chenjie/Documents/MES/edge-mes-demo/docs/thread_handoff/pm_operating_rules.md

还需要读取当前 durable status：

/Users/chenjie/Documents/MES/edge-mes-demo/docs/current_status.md
/Users/chenjie/Documents/MES/edge-mes-demo/docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
/Users/chenjie/Documents/MES/edge-mes-demo/docs/reports/sprint3_collector_ingestion_adapter_plan.md
/Users/chenjie/Documents/MES/edge-mes-demo/docs/contracts/collector_ingestion_adapter.md

## 1. 第一动作：只读恢复，不要直接继续开发

进入项目路径：

/Users/chenjie/Documents/MES/edge-mes-demo

先执行 read-only recovery：

    git status -sb
    printf '\n--- log -12 ---\n' && git log --oneline -12
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git show-ref --hash refs/remotes/origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only

不要在 read-only recovery 前发 implementation prompt、不要 stage、不要 commit、不要 push。

## 2. 当前真正 baseline

HEAD == origin/main == ae8787eed9dde7ba56eaac7a66b7eb4990cf57bf

latest commit:
ae8787e Sync Sprint 3 Slice I gate status

如果 live Git 与上述 baseline 不一致，先报告差异，不要猜测继续。

## 3. 当前 closed 状态

Sprint 3 Slice I WS03 raw_policy raw_capable authority implementation: CLOSED
Slice I docs/status sync: CLOSED
当前没有挂起的 review gate、commit gate、status sync gate。

## 4. 当前剩余 dirty 是 external artifacts，不要顺手处理

以下 dirty / untracked artifacts 是外部历史产物，不属于当前任务，不要 stage、不要 commit、不要 cleanup，除非用户明确 exact-path 授权：

M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

## 5. 当前 Sprint 3 状态摘要

WS01: raw_capable
WS02: raw_capable
WS03: raw_capable
line-wide runtime_defaults.raw_policy: raw_not_provided
raw_required: not introduced
runtime/source code: unchanged
storage.py / DB / API / Dashboard / V-PLC / Docker / deploy: unchanged
ACK/read_done ownership: unchanged

Slice I committed files:

config/mapping.yaml
tests/test_collector_station_event_runtime_source.py

Slice I docs/status sync committed files:

docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md

## 6. PM 规则提醒

不得未经用户授权直接 implementation。
不得未经用户授权运行 tests，除非任务 prompt 明确允许。
不得未经用户授权 stage / commit / push。
不得 deploy / tag / rollback / real PLC pilot，除非用户明确授权。
不得使用 git add . / git add -A / git add docs/。
所有 stage/commit/push 必须 exact-path allowlist。
收到 Thread 报告后，PM 需要先 intake 判断 PASS / PASS WITH RECOMMENDATIONS / HOLD，再决定并发送下一个最小任务 prompt。
PM direct tasks 不需要生成任务 prompt；用户授权后直接执行并报告。
Thread 任务 prompt 必须作为一个完整可复制 Markdown 块输出，且不要包含 @Devspace。

## 7. 推荐下一步

不要直接 implementation。

建议先做 read-only checkpoint / next-slice planning decision：

Sprint 3 raw_policy rollout checkpoint — confirm all three stations are now raw_capable and decide whether raw_policy rollout is complete for Sprint 3.

边界：
不引入 raw_required。
不改 runtime/source code。
不改 storage.py。
不改 DB/API/Dashboard/V-PLC/Docker/deploy。
不改 ACK/read_done ownership。
不 stage / commit / push，除非用户后续明确 exact-path 授权。
```

---

## 13. Handoff commit note

This handoff file was generated after Slice I docs/status sync.
If committing this file, use exact path only:

```text
docs/thread_handoff/chatgpt_pm_handoff_260630-1946.md
```

Suggested commit message:

```text
Add PM handoff after Slice I status sync
```

Do not stage `.gitignore` or old PM handoff / Keynote artifacts.
