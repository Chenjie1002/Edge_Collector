# ChatGPT PM Operating Rules

Updated: 2026-06-25

Applies to: Edge MES Demo ChatGPT PM / Codex Thread workflow.

This file stores stable PM rules so future Codex prompts can stay short. A task prompt may reference this file instead of repeating every operating rule inline.

## 1. Language and reporting

- Codex prompts and reports must be written in Chinese.
- Technical terms, file names, function names, error codes, contract names and commit messages may keep their English form.
- Reports must clearly state `PASS`, `PASS WITH RECOMMENDATIONS` or `HOLD` when the task is a gate/review.
- If a result is partial or a command cannot be run, report it explicitly instead of implying success.

## 2. PM and Thread roles

The long-lived core Threads are:

1. `Architecture / Integration`
2. `Reliability`
3. `Data Quality`
4. `Verification`

Do not create long-lived roles named Repair, Closeout, Final Audit, Targeted Re-review, or Implementation by default. Those are task types under one of the core Threads unless PM explicitly says otherwise.

Default ownership:

| Task type | Owner |
| --- | --- |
| contract design, boundary design, ownership, docs repair, status sync | Architecture / Integration |
| runtime safety, ACK, retry, authority, fail-closed behavior | Reliability |
| fact authority, lineage, projection, raw/normalized evidence, NOK outcome/detail | Data Quality |
| fixture matrix, negative cases, regression gate, final allowlist audit | Verification |
| commit authorization, push authorization, tag/deploy/rollback authorization | PM only |

## 3. Authority gates

A Codex Thread must not assume permission to do a later phase simply because a previous phase passed.

PM must explicitly authorize each of the following:

- implementation;
- tests;
- staging;
- commit;
- push;
- tag;
- deploy;
- rollback drill;
- runtime Collector integration;
- DB migration or DB write path changes;
- FastAPI/API changes;
- Dashboard/frontend changes;
- V-PLC/runtime simulator behavior changes;
- real PLC pilot work.

If a task is review-only or planning-only, the Thread must not modify files.

## 4. Git safety rules

Never use broad staging unless PM explicitly authorizes it for a specific exceptional case.

Forbidden by default:

```bash
git add .
git add -A
git add docs/
```

Commit/push tasks must use exact path allowlists and verify staged files before committing:

```bash
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

If any non-allowlist file is staged, unstage and report `HOLD`.

## 5. Dirty working tree and external artifacts

Some local artifacts may exist for PM handoff, Keynote/reporting, or other ChatGPT windows. Unless PM explicitly includes them in a task allowlist, they must be treated as external and excluded.

Current known external artifact patterns include:

```text
docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
docs/thread_handoff/chatgpt_pm_handoff_20260624.md
docs/thread_handoff/chatgpt_pm_handoff_20260625.md
docs/reports/phase1_to_sprint2_management_keynote_10p.html
```

A modified `.gitignore` may also be a pre-existing external dirty artifact. A task must not stage or commit it unless PM explicitly authorizes that exact file.

Every implementation/commit report should separately list:

- implementation files;
- pre-existing dirty artifacts;
- staged files;
- files explicitly excluded.

## 6. Project boundary rules

The project is a non-invasive Edge MES / Traceability / OEE Demo.

- PLC remains the control brain.
- Edge Collector collects, decodes, validates and records data.
- Edge must not replace PLC control logic.
- Edge must not actively decide production flow.
- Offline contracts or fixtures do not mean runtime integration is complete.

Phase-1 default behavior must not be changed unless PM explicitly authorizes a change.

## 7. Review gate conventions

Reviews should classify findings as:

- `Blockers`: must be fixed before the next gate.
- `Recommendations`: useful improvements that do not block the current gate.

A `PASS WITH RECOMMENDATIONS` means no blocker exists, but the recommendations should be passed to later Threads.

## 8. Subagent rules

Subagents may be requested when a task benefits from focused read-only review.

Subagent constraints:

- prompts must be self-contained;
- reports must be in Chinese;
- subagents are read-only unless PM explicitly authorizes repair;
- subagents must not expand scope to code/tests/migration/runtime/deploy;
- subagents must not stage/commit/push/tag;
- subagent conclusions are review input only; final gate decision remains with PM.

## 9. Minimal prompt pattern

Before assigning a task, PM should estimate:

- task size;
- expected file scope;
- whether the current Thread has enough context capacity;
- whether a new Thread is needed.

Future Codex prompts should prefer this short pattern:

```text
你现在作为 <Thread> — <Task>。

请先读取：
- docs/thread_handoff/pm_operating_rules.md
- docs/current_status.md
- <task-specific gate/status doc>
- <task-specific contract/report files>

按照上述文件中的 current gate、allowlist、excluded files 和报告格式执行。
不要扩大范围。
```

If task-specific docs are incomplete or inconsistent with the working tree, stop and report `HOLD`.

## 10. Window report vs repository report

Future Codex Threads should keep the chat-window report short and put durable detail in repository documents when the task is important enough to preserve.

Default window report requirements:

```text
报告名称：

任务名称：

执行 Thread：

结论：PASS / PASS WITH RECOMMENDATIONS / HOLD

Scope:
- reviewed files:
- changed files:
- explicitly not touched:

Evidence:
- tests:
- git status:
- allowlist compliance:

Blockers:
- none / list blockers

Recommendations:
- none / list recommendations

Next gate:
- eligible for:
- PM approval required before:

Thread 输出 / 上下文评估:
- 本次输出长度：短 / 中 / 长
- 当前 Thread 是否建议继续：yes / no
- 下一轮是否建议新开 Thread：yes / no
- 理由：
```

Every Thread report must include the report name, task name, executing Thread, conclusion, Scope, Evidence, Blockers, Recommendations, Next gate, and Thread output/context assessment.

When returning a report, the Thread must assess:

- the current output length;
- whether the current Thread can continue to carry the next task;
- whether the next round should start a new Thread.

Do not paste full command output into the chat window unless a command fails, a gate is `HOLD`, or PM explicitly asks for raw output.

Do not repeat long-term background already stored in project docs. Reference the relevant paths instead.

For important phase results, long review details should be written to or summarized in an appropriate repository file, for example:

```text
docs/reports/<sprint_or_task>_<thread>_review.md
docs/reports/<sprint_or_task>_implementation_report.md
docs/reports/<sprint_or_task>_gate_status.md
docs/current_status.md
docs/thread_handoff/<thread>.md
```

When a repository report/status file is updated, the chat-window report should include:

- the path updated;
- the final conclusion;
- changed files;
- tests or checks run;
- blockers/recommendations;
- next gate.

If the task is small, read-only, or temporary, a repository report file is optional. The Thread should still return a short window report.

If the task changes current gate status, update the relevant gate/status document or explicitly state why it was not updated.
