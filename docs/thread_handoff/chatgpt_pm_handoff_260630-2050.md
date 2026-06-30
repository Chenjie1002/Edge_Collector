# Edge MES Demo — ChatGPT PM Handoff 260630-2050

你现在接手 Edge MES Demo 项目的 ChatGPT PM 工作。

用户偏好：中文为主。
PM 角色：负责规划、授权边界、Thread 调度、报告 intake、exact-path stage/commit/push gate。
不要未经授权直接 implementation、tests、deploy、tag、rollback、stage、commit、push。

本 handoff 使用中国标准时间 / UTC+8 文件名后缀：`260630-2050`。

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

不要在 read-only recovery 前发 implementation prompt、不要 stage、不要 commit、不要 push。

---

## 3. 当前 Git baseline

当前主线已同步：

```text
HEAD == origin/main == c899e6eb6ce91442f091df1362b92f5330c7d8ca
```

最新 commit：

```text
c899e6e Freeze Sprint 3 Slice J adapter boundary docs
```

最近关键 commits：

```text
c899e6e Freeze Sprint 3 Slice J adapter boundary docs
414c9a8 Sync Sprint 3 post-raw-policy status docs
1ed1e44 Add PM handoff after Slice I status sync
ae8787e Sync Sprint 3 Slice I gate status
045d21c Roll out Slice I WS03 raw policy authority
7f576be Repair PM handoff baseline semantics
44f2446 Add PM handoff and UTC+8 handoff workflow
50c37c7 Sync Sprint 3 Slice H gate status
c7e80e8 Roll out Slice H WS02 raw policy authority
44ed02d Sync Sprint 3 Slice G gate status
398f11c Harden Slice G raw policy sanity tests
e8650f1 Add PM handoff timestamp naming rule
```

Durable docs may still mention older hashes such as `045d21c`, `1ed1e44` or `414c9a8` as historical audit markers. Live Git facts are authoritative and must be checked directly with read-only commands.

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

本 handoff 文件为新文件：

```text
docs/thread_handoff/chatgpt_pm_handoff_260630-2050.md
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

## 5. 当前 closed 状态

当前主线：Phase-2 Sprint 3 Collector Ingestion Adapter。

已闭环到：

```text
Sprint 3 raw_policy station-level rollout checkpoint: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 post-raw_policy docs/status sync: CLOSED, commit 414c9a8
Sprint 3 Slice J downstream planning-only gate: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 Slice J docs/contracts boundary freeze: CLOSED, commit c899e6e
Sprint 3 Slice J Reliability docs boundary review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Sprint 3 Slice J Data Quality docs boundary review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Sprint 3 Slice J Verification docs boundary review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
```

当前没有挂起的 review gate、commit gate、status sync gate。

Durable status references：

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
docs/contracts/collector_ingestion_adapter.md
```

---

## 6. Sprint 3 raw_policy closure summary

当前 raw_policy station-level rollout 已关闭：

```text
WS01 station-level raw_policy: raw_capable
WS02 station-level raw_policy: raw_capable
WS03 station-level raw_policy: raw_capable
line-wide runtime_defaults.raw_policy: raw_not_provided
raw_required: not introduced
runtime/source code: unchanged
storage.py / DB / API / Dashboard / V-PLC / Docker / deploy: unchanged
ACK/read_done ownership: unchanged
```

关键 commits：

```text
829d5c7 Implement Sprint 3 Slice F2 raw policy authority    # WS01
398f11c Harden Slice G raw policy sanity tests
c7e80e8 Roll out Slice H WS02 raw policy authority          # WS02
045d21c Roll out Slice I WS03 raw policy authority          # WS03
414c9a8 Sync Sprint 3 post-raw-policy status docs
```

Do not treat all-station `raw_capable` as authorization for `raw_required`, line-wide raw_policy default changes, DB/API/Dashboard visibility, ACK/read_done ownership changes, deployment, rollback or real PLC pilot.

---

## 7. Sprint 3 Slice J boundary freeze summary

Slice J name：

```text
Sprint 3 Slice J — Downstream Collector Adapter Decision / Diagnostic / Projection Boundary
```

Docs/contracts freeze committed at：

```text
c899e6e Freeze Sprint 3 Slice J adapter boundary docs
c899e6eb6ce91442f091df1362b92f5330c7d8ca
```

Committed files：

```text
docs/contracts/collector_ingestion_adapter.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
```

Slice J frozen boundary：

```text
- only accepted adapter decisions may reach existing persist/ACK path;
- rejected / deferred / quarantined / duplicate / conflict / raw_variant must not persist, ACK, project, write defect detail or become DB/API/Dashboard-visible production facts;
- diagnostic observability remains non-owner of ACK/read_done, persist, retry commit, projection and defect-detail creation;
- raw_payload/raw_hex remains evidence only, not production fact;
- decoded/normalized payload remains candidate until accepted adapter decision;
- DB/API/Dashboard production visibility is deferred to a separate production-fact boundary gate.
```

Slice J docs/contracts reviews：

```text
Architecture / Integration docs/contracts freeze: PASS
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Verification focused review / exact allowlist audit: PASS WITH RECOMMENDATIONS, no blocker
PM exact-path commit/push: PASS, commit c899e6e
```

Reliability / Data Quality / Verification carry-forward recommendations：

```text
- In later implementation wording/tests, tighten duplicate/raw_variant phrasing from “no new ACK” to “no ACK/read_done mutation for the current non-accepted payload”.
- Future implementation tests should assert rejected / deferred / quarantined / duplicate / conflict / raw_variant cause:
  - no persist;
  - no ACK/read_done mutation;
  - no projection;
  - no defect detail write;
  - no production visibility.
- Preserve accepted-only production fact creation.
- Non-accepted dispositions must not create production facts, projection metadata, defect detail or production visibility.
- Raw evidence remains evidence only.
- Decoded/normalized payloads remain candidates until accepted adapter decision.
- DB/API/Dashboard visibility requires a separate production-fact boundary gate.
```

---

## 8. 当前推荐下一步

建议先做 handoff，然后在新 PM 窗口开启：

```text
Sprint 3 Slice J implementation planning
```

重要：下一步仍然不是 implementation，也不是 tests。它应该先冻结 exact implementation allowlist、minimal implementation objective、review gates 和 non-goals。

Reasoning：

```text
当前 ChatGPT PM 窗口已经历多个 read-only planning gates、docs/status sync、Slice J docs/contracts freeze、Reliability/Data Quality/Verification reviews 和两次 exact-path commit/push。
Slice J docs/contracts freeze 刚好是天然切点。
下一步是新的 Level 2 implementation-planning branch，应重新声明 baseline、dirty artifacts、scope、candidate allowlist、review gates 和授权边界。
```

---

## 9. 下一步任务边界建议

建议的新 Thread 任务：

```text
Sprint 3 Slice J implementation planning
```

Owner：

```text
Architecture / Integration
```

Proposed tier：

```text
Level 2 planning gate
```

Suggested objective：

```text
Freeze the smallest Slice J implementation plan that hardens adapter decision / diagnostic / projection boundaries without starting DB/API/Dashboard visibility, ACK/read_done ownership changes, raw_required, storage.py, deploy or runtime expansion.
```

Candidate implementation allowlist category only, not authorization：

```text
collector/app/services/station_event_adapter.py
collector/app/services/event_collector.py only if runtime diagnostic/gate behavior needs narrow hardening
tests/test_collector_station_event_adapter.py
collector/tests/test_event_collector_adapter_gate.py
common/station_event/projection.py only if projection helper semantics are explicitly in scope
```

PM should not authorize all of these by default. Slice J implementation planning should select the smallest exact allowlist needed.

Required gate sequence if implementation is later authorized：

```text
1. Architecture / Integration implementation planning
2. Architecture / Integration implementation, only after explicit PM approval
3. Reliability focused implementation review
4. Data Quality focused implementation review
5. Verification focused implementation review / exact allowlist audit
6. PM direct exact-path stage/commit/push, only after explicit user authorization
```

---

## 10. Non-authorized surfaces

Do not touch without separate explicit PM authorization：

```text
implementation
tests
config/mapping.yaml
raw_required
line-wide runtime_defaults.raw_policy
runtime/source expansion outside exact allowlist
storage.py
DB schema / migration / write path
FastAPI / API
Dashboard / Trace UI / frontend
V-PLC behavior
Docker / deploy
tag / rollback / real PLC pilot
ACK/read_done ownership
external dirty artifacts
```

---

## 11. PM / Thread governance observations

用户问：当前 PM 规则以及各 Thread 规则是否需要在这次交接时完善？

PM 判断：

```text
No mandatory governance rule update is required before the next task.
Do not block handoff or Slice J implementation planning on PM rules edits.
```

值得考虑但不建议和本 handoff 混 commit 的规则完善：

```text
1. Review-only Thread report wording can be tightened:
   - distinguish “changed files under review / dirty files being reviewed” from “files changed by this Thread”.
   - Several review reports listed target docs under changed files while also saying no file edits; humans understood it, but future agents could misread it.

2. ACK wording can be made more precise in future implementation/test prompts:
   - prefer “no ACK/read_done mutation for the current non-accepted payload” over “no new ACK”, especially for duplicate/raw_variant.
   - This is currently carried forward as a Slice J recommendation rather than a global PM rule.

3. Keep the existing practice that after Level 2 docs/contracts freeze closes and before implementation planning starts, PM should hand off when the ChatGPT window is long.
   - This is already mostly covered by pm_operating_rules.md handoff workflow.
```

Recommendation：

```text
Do not edit docs/thread_handoff/pm_operating_rules.md in this handoff unless the user explicitly authorizes a separate exact-path governance update.
Carry the three observations above into the next PM window.
If the next PM sees the same “changed files under review vs changed by Thread” ambiguity recur, open a small Level 0 PM rules update with exact path docs/thread_handoff/pm_operating_rules.md.
```

---

## 12. Suggested prompt for the next ChatGPT PM

Use this prompt when opening a new ChatGPT PM window. Keep it as one copyable Markdown block.

```markdown
# Edge MES Demo — ChatGPT PM 接手 Prompt

你的角色是一位 ChatGPT PM，负责接手 Edge MES Demo 项目的开发管理、Thread 调度、gate 判断、报告 intake、授权边界控制，以及 exact-path stage/commit/push gate。

请先阅读交接文件：

/Users/chenjie/Documents/MES/edge-mes-demo/docs/thread_handoff/chatgpt_pm_handoff_260630-2050.md

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

HEAD == origin/main == c899e6eb6ce91442f091df1362b92f5330c7d8ca

latest commit:
c899e6e Freeze Sprint 3 Slice J adapter boundary docs

如果 live Git 与上述 baseline 不一致，先报告差异，不要猜测继续。

## 3. 当前 closed 状态

Sprint 3 raw_policy station-level rollout checkpoint: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 post-raw_policy docs/status sync: CLOSED, commit 414c9a8
Sprint 3 Slice J downstream planning-only gate: CLOSED / PASS WITH RECOMMENDATIONS
Sprint 3 Slice J docs/contracts boundary freeze: CLOSED, commit c899e6e
Sprint 3 Slice J Reliability docs boundary review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Sprint 3 Slice J Data Quality docs boundary review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
Sprint 3 Slice J Verification docs boundary review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker

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

Slice J docs/contracts freeze committed files:

docs/contracts/collector_ingestion_adapter.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md

Slice J frozen boundary:

- only accepted adapter decisions may reach existing persist/ACK path;
- rejected / deferred / quarantined / duplicate / conflict / raw_variant must not persist, ACK, project, write defect detail or become DB/API/Dashboard-visible production facts;
- diagnostic observability remains non-owner of ACK/read_done, persist, retry commit, projection and defect-detail creation;
- raw_payload/raw_hex remains evidence only, not production fact;
- decoded/normalized payload remains candidate until accepted adapter decision;
- DB/API/Dashboard production visibility is deferred to a separate production-fact boundary gate.

Carry-forward recommendations:

- In later implementation wording/tests, tighten duplicate/raw_variant phrasing from “no new ACK” to “no ACK/read_done mutation for the current non-accepted payload”.
- Future implementation tests should assert rejected / deferred / quarantined / duplicate / conflict / raw_variant cause no persist, no ACK/read_done mutation, no projection, no defect detail write and no production visibility.

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

建议先做：

Sprint 3 Slice J implementation planning

执行 Thread：Architecture / Integration
任务性质：Level 2 planning gate only

目标：冻结最小 Slice J implementation objective、exact implementation allowlist、required review gates 和 non-goals。

边界：
不运行 tests。
不改文件，除非后续 PM 明确授权 planning docs edit。
不改 config/mapping.yaml。
不引入 raw_required。
不改 storage.py。
不改 DB/API/Dashboard/V-PLC/Docker/deploy。
不改 ACK/read_done ownership。
不 stage / commit / push，除非用户后续明确 exact-path 授权。
```

---

## 13. Handoff commit note

This handoff file was generated after Slice J docs/contracts boundary freeze was committed and pushed.
If committing this file, use exact path only:

```text
docs/thread_handoff/chatgpt_pm_handoff_260630-2050.md
```

Suggested commit message:

```text
Add PM handoff after Slice J boundary freeze
```

Do not stage `.gitignore`, old PM handoff files, Keynote/reporting artifacts or pm_operating_rules.md unless the user explicitly authorizes those exact paths.
