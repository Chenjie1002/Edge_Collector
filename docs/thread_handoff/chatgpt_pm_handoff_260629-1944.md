# Edge MES Demo — ChatGPT PM Handoff 260629-1944

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

## 2. 当前 Git baseline

当前主线已同步：

```text
HEAD == origin/main == 0443b8041b20f3598e830c7340e3cdce6de89219
```

最新 commit：

```text
0443b80 Sync Sprint 3 Slice F2 gate status
```

最近关键 commits：

```text
0443b80 Sync Sprint 3 Slice F2 gate status
829d5c7 Implement Sprint 3 Slice F2 raw policy authority
734ba52 Sync Sprint 3 Slice F1 gate status
ac1838c Freeze Sprint 3 Slice F1 raw_policy authority
d02b98d Sync Sprint 3 Slice E1 gate status
2c73410 Repair Sprint 3 Slice E1 runtime raw decoder
dac87c1 Add PM task risk tier rules
cd0c01a Sync Sprint 3 Slice D3 gate status
```

---

## 3. 当前 working tree

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
docs/thread_handoff/chatgpt_pm_handoff_260629-1944.md
```

重要规则：

```text
Do not stage .gitignore unless explicitly authorized by exact path.
Do not stage old PM handoff / keynote artifacts unless explicitly authorized by exact path.
Do not use git add .
Do not use git add -A.
Do not use git add docs/.
```

任何 stage/commit/push 必须 exact-path allowlist，并由用户明确授权。

---

## 4. PM handoff file naming rule update

本次交接新增稳定规则：

```text
PM handoff file names must be unique.
New ChatGPT PM handoff files should use timestamp suffix format YYMMDD-hhmm.
Example: docs/thread_handoff/chatgpt_pm_handoff_260629-1944.md
Use the user's/project local time when available.
Never overwrite an existing PM handoff file.
```

已更新文件：

```text
docs/thread_handoff/pm_operating_rules.md
```

注意：PM rules 是 durable governance doc。若要提交本次交接文件和命名规则更新，必须 exact-path stage：

```text
docs/thread_handoff/pm_operating_rules.md
docs/thread_handoff/chatgpt_pm_handoff_260629-1944.md
```

---

## 5. 当前 Sprint 3 状态

当前主线：Phase 2 Sprint 3 Collector Ingestion Adapter。

已闭环到：

```text
Sprint 3 Slice F2 raw_policy raw_capable authority implementation: CLOSED
```

F2 implementation commit：

```text
829d5c7 Implement Sprint 3 Slice F2 raw policy authority
829d5c71982b8d22556102b6e67ed9c1e981131d
```

F2 docs/status sync commit：

```text
0443b80 Sync Sprint 3 Slice F2 gate status
0443b8041b20f3598e830c7340e3cdce6de89219
```

F2 gate 状态：

```text
Architecture / Integration implementation: PASS
Reliability focused implementation review: PASS
Data Quality focused implementation review: PASS
Verification exact allowlist audit: PASS WITH RECOMMENDATIONS
Exact allowlist commit/push: PASS
Docs/status sync: PASS
```

Durable status references：

```text
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/reports/sprint3_collector_ingestion_adapter_plan.md
docs/contracts/collector_ingestion_adapter.md
```

这些文档应作为 durable status authority，除非 live Git 直接矛盾。

---

## 6. F2 技术摘要

F2 是 F1 raw_policy authority freeze 后的 narrow Level 2 mapping/config authority implementation。

F2 目标：

```text
仅将 WS01 / ws01_runtime_v1 / station_runtime_payload_v1 的 station-level raw_policy 从 raw_not_provided 推进为 raw_capable。
```

F2 committed files：

```text
config/mapping.yaml
tests/test_collector_station_event_runtime_source.py
```

F2 行为：

```text
- WS01 station-level raw_policy: raw_capable
- WS02 / WS03 remain raw_not_provided
- line-wide runtime_defaults unchanged
- raw_required not introduced
- runtime/source code unchanged
- storage.py unchanged
- DB/API/Dashboard/frontend unchanged
- V-PLC behavior unchanged
- Docker/deploy unchanged
- ACK/read_done ownership unchanged
```

F2 authority / evidence semantics：

```text
- runtime code-path capability does not equal mapping/config authority upgrade
- WS01 raw_capable is now explicit mapping/config authority from config/mapping.yaml
- raw_capable missing raw remains RAW_EVIDENCE_MISSING fail-closed
- RAW_PARSE_ERROR remains fail-closed
- RAW_NORMALIZED_MISMATCH remains fail-closed
- raw evidence remains evidence, not production fact
- decoded raw payload / normalized candidate still requires accepted adapter decision before production path
- rejected/diagnostic decisions do not project, persist, ACK or become DB/API/Dashboard-visible production facts
```

F2 test evidence：

```text
PYTHONPATH=collector:. .venv/bin/python -m pytest tests/test_collector_station_event_runtime_source.py collector/tests/test_event_collector_adapter_gate.py
76 passed
```

---

## 7. F1 技术摘要

F1 是 F2 的前置 docs/contracts authority freeze。

F1 commits：

```text
ac1838c Freeze Sprint 3 Slice F1 raw_policy authority
734ba52 Sync Sprint 3 Slice F1 gate status
```

F1 关键结论：

```text
- runtime raw path capability is not a mapping/config authority upgrade
- raw_not_provided is an authority declaration, not a synonym for missing runtime raw path
- raw_capable/raw_required missing raw must fail closed
- future raw_policy move to raw_capable/raw_required is a separate Level 2 mapping/config authority gate
- rejected/diagnostic decisions remain non-production and not DB/API/Dashboard-visible facts
```

---

## 8. 当前 no-go surfaces

除非用户后续明确授权新的 Level 2 task，不要触碰：

```text
raw_required
line-wide raw_policy default change
collector/app/services/storage.py
DB/API/Dashboard/frontend
V-PLC behavior
Docker/deploy
ACK/read_done ownership
tag
rollback
real PLC pilot
```

任何后续 raw_policy 扩展到 WS02/WS03、或推进 raw_required，都必须重新走：

```text
Architecture / Integration planning
Architecture / Integration implementation, if authorized
Reliability focused review
Data Quality focused review
Verification exact allowlist audit
PM exact-path stage/commit/push gate
Docs/status sync, if committed
```

---

## 9. PM operating rules

Read first：

```text
docs/thread_handoff/pm_operating_rules.md
```

Core rules：

```text
- PM owns authorization and exact-path stage/commit/push gates.
- Long-lived Threads: Architecture / Integration, Reliability, Data Quality, Verification.
- Never use git add .
- Never use git add -A.
- Never use git add docs/.
- Deploy/tag/rollback require separate explicit authorization.
- ACK/read_done ownership changes require separate authorization.
- DB/API/Dashboard/V-PLC/storage.py/config/raw_policy changes require separate PM authorization.
- Do not stage/commit old PM handoff artifacts or .gitignore unless explicitly authorized by exact path.
- New PM handoff files should use YYMMDD-hhmm suffix and must not overwrite existing files.
```

Risk tier reminders：

```text
Level 0:
- PM direct exact-path commit/push
- small PM docs/rule/status edits
- mechanical status/hash sync

Level 1:
- one focused Thread
- low-risk docs/tests/contracts changes
- no runtime behavior/authority semantics

Level 2:
- runtime behavior
- PLC/V-PLC
- ACK/read_done
- DB write path
- storage.py
- decoder/registry authority
- raw/normalized evidence semantics
- schema/config semantics
- raw_policy mapping/config authority changes
```

Do not downgrade Level 2 just because the diff is small.

---

## 10. Required first action for new PM

Start with read-only recovery：

```text
git status -sb
git log --oneline -8
git log -1 --format=%H
git show-ref --hash refs/remotes/origin/main
git diff --name-only
git diff --cached --name-only
```

Expected after this handoff, before committing the handoff artifact itself：

```text
HEAD == origin/main == 0443b8041b20f3598e830c7340e3cdce6de89219
staged files empty
tracked dirty includes .gitignore plus PM rules / new handoff file if this handoff task has not been committed
old external dirty artifacts remain excluded
```

If source/test/config/runtime/docs-status files are unexpectedly dirty, stop and report before continuing.

---

## 11. Current handoff readiness assessment

Current PM handoff readiness：

```text
Suitable for PM handoff: yes
```

Reasons：

```text
- F2 implementation closed
- F2 Reliability / Data Quality / Verification gates closed
- F2 exact commit/push closed
- F2 docs/status sync closed
- HEAD == origin/main
- staged set empty before this handoff task
- no uncommitted source/test/config/docs-status task changes
- only known external artifacts remain
```

The only active handoff-specific changes are expected to be：

```text
docs/thread_handoff/pm_operating_rules.md
docs/thread_handoff/chatgpt_pm_handoff_260629-1944.md
```

---

## 12. Suggested next decision

Recommended next PM action after handoff commit, if user wants to continue development：

```text
Architecture / Integration — Sprint 3 Slice G planning
```

Candidate planning directions：

```text
A. WS01 raw_capable post-commit sanity / broader regression planning
B. raw_capable rollout planning: whether to extend to WS02/WS03 or pause
C. raw_required impact planning, only if user explicitly wants it; not recommended as immediate implementation
```

Recommended default：

```text
Start with Slice G planning, not implementation.
```

Do not immediately edit source/test/config/runtime files without a new PM-authorized task.

---

## 13. Handoff commit guidance

If the current user wants this handoff artifact and naming rule committed, use exact-path stage only：

```text
git add docs/thread_handoff/pm_operating_rules.md docs/thread_handoff/chatgpt_pm_handoff_260629-1944.md
```

Recommended commit message：

```text
Add PM handoff timestamp naming rule
```

Before commit：

```text
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

Expected staged files only：

```text
docs/thread_handoff/pm_operating_rules.md
docs/thread_handoff/chatgpt_pm_handoff_260629-1944.md
```

Do not stage：

```text
.gitignore
old PM handoff / Keynote artifacts
any source/test/config/runtime/status files
```
