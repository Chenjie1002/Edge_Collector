# ChatGPT PM Operating Rules

Updated: 2026-06-27

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

### Baseline and status semantics

`git rev-parse HEAD` and `git rev-parse origin/main` are dynamic repository
facts. Each Thread that depends on repository state should check them directly
with read-only commands instead of treating a durable document hash as live
truth.

Durable status documents may record a `last verified baseline`, `last status
sync baseline` or `latest known baseline at authoring time`. Those values are
historical audit markers, not a requirement that the document hash must always
equal the current `HEAD` after later docs-only commits.

A docs-only repair/status commit naturally creates a new `HEAD`. If durable
docs still name the pre-repair baseline that the Thread verified before the
commit, that difference alone is not a `HOLD`; report the live `HEAD` /
`origin/main` difference and continue within the PM-authorized task.

Stop and report `HOLD` only when task-specific docs conflict with the live
repository or PM instruction on gate state, allowlist, scope, authorization
boundary, excluded files, out-of-scope surfaces, or runtime behavior.

## 5. Dirty working tree and external artifacts

Some local artifacts may exist for PM handoff, Keynote/reporting, or other ChatGPT windows. Unless PM explicitly includes them in a task allowlist, they must be treated as external and excluded.

Current known external artifact patterns include:

```text
docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
docs/thread_handoff/chatgpt_pm_handoff_20260624.md
docs/thread_handoff/chatgpt_pm_handoff_20260625.md
docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
docs/reports/phase1_to_sprint2_management_keynote_10p.html
```

A modified `.gitignore` may also be a pre-existing external dirty artifact. A task must not stage or commit it unless PM explicitly authorizes that exact file.

Every implementation/commit report should separately list:

- implementation files;
- pre-existing dirty artifacts;
- staged files;
- files explicitly excluded.

## 6. Project boundary rules

The Edge MES Demo project absolute path is:

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

All Codex Thread prompts, workspace references and local command planning for this project should use this path unless PM explicitly declares a different checkout/worktree.

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

### PM report intake rule

When the user sends an `Architecture / Integration`, `Reliability`, `Data Quality`, `Verification` or other Thread report, ChatGPT PM should treat it as a report intake event by default.

PM should not ask why the report was sent, and should not spend effort inferring the user's intent when the report format already indicates a completed Thread task.

PM default action is:

1. read and summarize the report conclusion;
2. classify the result as `PASS`, `PASS WITH RECOMMENDATIONS` or `HOLD`;
3. check blockers, scope expansion, allowlist violations, failed tests, staged files, unauthorized modifications and gate/status conflicts;
4. classify recommendations as current-gate blockers, carry-forward items, docs/status sync items or `HOLD` items;
5. make a PM decision: accept, `HOLD`, request more evidence, authorize repair, authorize next review, authorize exact commit/push or open the next planning gate;
6. issue the next minimal authorized task prompt when the report is sufficient;
7. never infer authorization for implementation, staging, commit, push, deploy, rollback, D2-C/D3 or any later phase from a `PASS` report alone.

## 8. Subagent rules

Subagents may be requested when a task benefits from focused read-only review.

Subagent constraints:

- prompts must be self-contained;
- reports must be in Chinese;
- subagents are read-only unless PM explicitly authorizes repair;
- subagents must not expand scope to code/tests/migration/runtime/deploy;
- subagents must not stage/commit/push/tag;
- subagent conclusions are review input only; final gate decision remains with PM.

## 9. Thread handoff and governance docs

When a Thread becomes long or carries too much prior context, PM should start a new Thread instead of continuing by momentum. The new prompt must restate the live repository baseline, current gate state, expected dirty artifacts, exact allowlist, explicit non-goals and next authorized action. A new Thread must not infer authority from the previous chat window.

For handoff between Threads, PM should include:

- project absolute path;
- live `HEAD` and `origin/main` from the latest PM or Thread check;
- latest relevant commit and gate conclusion;
- files already changed, staged, committed or pushed;
- known external dirty artifacts to exclude;
- exact allowlist for the new task;
- explicit surfaces not authorized, especially runtime wiring, schema/config changes, DB/API/Dashboard/V-PLC/deploy/tag/rollback and real PLC pilot work.

Governance documents such as this file, `README.md`, `docs/current_status.md` and gate status reports are durable project controls. They should be updated when PM rules, phase roadmap, Thread roles, baseline semantics or gate state materially change. Those updates require an explicit PM task and exact allowlist. They must not be bundled into code, runtime, schema, deployment or handoff artifact commits unless PM explicitly authorizes that bundle.

`README.md` is a public orientation document. It may summarize the project phases, Thread model and development workflow, but it must not replace the live gate/status documents. When README, PM rules and status files disagree on current authorization, Threads must stop and ask PM for a status repair instead of guessing.

## 10. Minimal prompt pattern

Before assigning a task, PM must record:

- task size;
- expected file scope;
- whether the current Thread has enough context capacity;
- whether a new Thread is needed;
- the reason for continuing the current Thread or opening a new one.

Future Codex prompts should prefer this short pattern:

```text
报告名称：
<Report name>

任务名称：
<Task name>

执行 Thread：
<Architecture / Integration | Reliability | Data Quality | Verification>

PM 任务前工作量评估：
- 任务规模：小 / 中 / 大
- 涉及范围：<expected file/domain scope>
- 当前 Thread 是否建议继续：yes / no
- 是否需要新开 Thread：yes / no
- 理由：<context capacity / scope isolation reason>

请先读取：
- docs/thread_handoff/pm_operating_rules.md
- docs/current_status.md
- <task-specific gate/status doc>
- <task-specific contract/report files>

按照上述文件中的 current gate、allowlist、excluded files 和报告格式执行。
不要扩大范围。
```

If task-specific docs are incomplete or inconsistent with the working tree on
gate state, allowlist, scope, authorization boundary, excluded files or
out-of-scope surfaces, stop and report `HOLD`. A durable baseline hash that
names the last verified docs/status sync baseline is not by itself a blocker
when live `git rev-parse` output shows only later authorized docs-only commits.

## 11. Window report vs repository report

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

When returning a report, the Thread must reassess context capacity after completing the task. This reassessment must state:

- the current output length;
- whether the current Thread can continue to carry the next task;
- whether the next round should start a new Thread;
- the reason for that recommendation.

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
