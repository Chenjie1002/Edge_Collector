# Edge MES Demo — ChatGPT PM Handoff

Date: 2026-06-25
Handoff owner: outgoing ChatGPT PM
Next owner: new ChatGPT PM
Project path: `/Users/chenjie/Documents/MES/edge-mes-demo`

## 1. New PM role

You are taking over as ChatGPT PM for the Edge MES Demo project.

Your job is not to implement code directly by default. Your responsibilities are:

- read project docs and current gate/status files;
- decide next Thread and task;
- produce short, precise Codex prompts;
- audit Codex Thread reports;
- enforce allowlists, phase boundaries, and git safety;
- decide PASS / PASS WITH RECOMMENDATIONS / HOLD;
- authorize implementation, staging, commit, push, tag, deploy, rollback only when appropriate.

Use Chinese for prompts and reports. Technical terms, file paths, function names, error codes and commit messages may remain in English.

## 2. Important new workflow rule

The project has moved to a docs-first PM workflow.

Future prompts should be short. Long-lived rules and current gate state should live in repo docs, not in the chat window.

Codex Threads should normally be told to read:

```text
docs/thread_handoff/pm_operating_rules.md
docs/current_status.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
<task-specific contract/report files>
```

Then the prompt should only include:

- immediate task;
- exact allowlist if any;
- files to exclude;
- report format if the default is not enough.

Window reports should be short. Durable details should go into `docs/reports/`, `docs/current_status.md`, or `docs/thread_handoff/`.

This rule has been written into:

```text
docs/thread_handoff/pm_operating_rules.md
```

but that file is currently uncommitted.

## 3. Current git baseline

Local Devspace check showed:

```text
HEAD:
b43a12f7d85d6acb3278a6208cac1c9b1d4d175a

origin/main:
b43a12f7d85d6acb3278a6208cac1c9b1d4d175a

latest commit:
b43a12f Implement Sprint 3 collector ingestion adapter offline slice

branch:
main

tag list:
phase1-pass-20260619
```

Recent commits:

```text
b43a12f Implement Sprint 3 collector ingestion adapter offline slice
4e0e1f1 Plan Sprint 3 collector ingestion adapter boundary
1a22cdc Clarify Sprint 2 closeout repository baseline
82b2127 Close out Sprint 2 documentation state
17cf5d2 Implement Sprint 2 generic station event model
e9abe45 Finalize Sprint 2 station event review gates
60adac2 Address Sprint 2 station event reliability review
45fa2a8 Freeze Sprint 2 station event planning
```

## 4. Current working tree

Current working tree at handoff time:

```text
 M .gitignore
 M docs/DOC_INDEX.md
 M docs/current_status.md
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/pm_operating_rules.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
```

Meaning:

- `.gitignore` is a pre-existing dirty artifact and should remain excluded unless PM explicitly decides otherwise.
- Keynote / PM handoff artifacts are external/untracked and should remain excluded unless PM explicitly decides otherwise.
- `docs/DOC_INDEX.md`, `docs/current_status.md`, `docs/thread_handoff/pm_operating_rules.md`, and `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md` are part of the docs-first PM consolidation performed in the outgoing PM window.
- This handoff file itself, `docs/thread_handoff/chatgpt_pm_handoff_20260625.md`, is for PM continuity and should not be committed unless the new PM explicitly decides it belongs in repo history.

No staging, commit, push, tag, deploy, rollback was performed by the outgoing PM during docs consolidation.

## 5. Sprint 3 status

Sprint 3 current slice:

```text
Collector Ingestion Adapter offline implementation
```

Current state:

```text
Docs-only contract: committed and pushed at 4e0e1f1
Offline adapter implementation: committed and pushed at b43a12f
Reliability focused review: PASS WITH RECOMMENDATIONS, no blocker
Data Quality focused review: PASS WITH RECOMMENDATIONS, no blocker
Verification focused review: PASS WITH RECOMMENDATIONS, no blocker
Runtime integration: not authorized
DB/API/Dashboard/V-PLC/PLC pilot/deploy/tag/rollback: not authorized
```

Implementation files committed in `b43a12f`:

```text
collector/app/services/resolved_config_registry.py
collector/app/services/station_event_adapter.py
tests/test_collector_station_event_adapter.py
```

The implementation is an offline adapter only:

```text
source payload fixture
-> normalized station_event envelope
-> shared validation helpers
-> lifecycle output
-> offline projection metadata
-> adapter diagnostic decision wrapper
```

It is not runtime Collector integration.

## 6. Current docs-first consolidation work

The outgoing PM created/updated the following docs to reduce future prompt size:

New files:

```text
docs/thread_handoff/pm_operating_rules.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
```

Modified files:

```text
docs/current_status.md
docs/DOC_INDEX.md
```

Purpose:

- centralize stable PM rules;
- record Sprint 3 gate state;
- document short prompt pattern;
- document window-short-report / repo-long-report policy;
- make future Codex prompts much shorter.

Validation performed:

```text
git diff --check: PASS
pm_operating_rules.md trailing whitespace scan: PASS
```

A trailing whitespace scan over all four docs reports one existing Markdown hard line break in `docs/current_status.md:4`. `git diff --check` passes.

## 7. Recommended immediate next PM action

Do not start runtime integration yet.

Recommended next action:

```text
Architecture / Integration — PM operating docs consolidation review and exact docs-only commit planning
```

The new PM should first audit the docs consolidation and decide whether to commit it.

Suggested docs-only commit allowlist, if approved after review:

```text
docs/thread_handoff/pm_operating_rules.md
docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
docs/current_status.md
docs/DOC_INDEX.md
```

Files that should remain excluded unless PM explicitly changes scope:

```text
.gitignore
docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
docs/thread_handoff/chatgpt_pm_handoff_20260624.md
docs/thread_handoff/chatgpt_pm_handoff_20260625.md
docs/reports/phase1_to_sprint2_management_keynote_10p.html
```

Suggested commit message if the docs consolidation passes review:

```text
Consolidate PM operating rules and Sprint 3 gate status
```

Before committing, require:

```bash
git status --short --untracked-files=all
git diff --name-only
git diff --check
grep -nE '[[:blank:]]$' docs/thread_handoff/pm_operating_rules.md docs/reports/sprint3_collector_ingestion_adapter_gate_status.md docs/current_status.md docs/DOC_INDEX.md || true
git add docs/thread_handoff/pm_operating_rules.md docs/reports/sprint3_collector_ingestion_adapter_gate_status.md docs/current_status.md docs/DOC_INDEX.md
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

Stage only the four allowlist docs. Do not stage `.gitignore`, Keynote artifacts, or PM handoff artifacts.

## 8. Open recommendations from Sprint 3 reviews

These are not blockers for the already committed offline adapter implementation.

```text
R-N1 / DQ-N1 / V-N1:
Add a resolved snapshot content hash self-check fixture that recomputes snapshot content hash and compares it with config_hash, not only returned object field mismatch.

R-N2 / DQ-N2 / V-N2:
Add a clearer non-30003/system_reserved route/direct predecessor negative fixture and clean up misleading route test naming/assertion path.
```

Recommended handling:

- keep them as next hardening slice candidates;
- do not treat them as blockers for the current committed offline adapter;
- do not use them to justify runtime integration without a new planning gate.

## 9. Rules the new PM must preserve

- Do not authorize runtime Collector integration just because offline adapter implementation passed.
- Do not authorize DB/API/Dashboard/V-PLC/deploy/tag/rollback without explicit separate gate.
- Do not let Codex use `git add .`, `git add -A`, or `git add docs/`.
- Exact allowlists must be used for staging/commit tasks.
- Exclude `.gitignore` unless it is explicitly in allowlist.
- Exclude Keynote/reporting artifacts unless PM explicitly decides to commit them.
- Keep prompts short by referencing project docs.
- Keep window reports short; long durable details belong in repo docs.

## 10. Minimal prompt template for the new PM

Use this pattern for future Codex tasks:

```text
你现在作为 <Thread> — <Task>。

请先读取：
- docs/thread_handoff/pm_operating_rules.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- <task-specific contract/report files>

本轮任务：<one paragraph>

允许修改 / stage / commit 的 exact allowlist：
- <paths, or none>

必须排除：
- .gitignore
- PM handoff artifacts
- Keynote/reporting artifacts
- any runtime/deploy files outside scope

按 pm_operating_rules.md 的窗口短报告规则返回结果。
```

## 11. Suggested next Codex prompt

If the new PM wants to commit the docs consolidation, use a short prompt like this:

```text
你现在作为 Architecture / Integration — PM operating docs consolidation review and exact docs-only commit planning。

请先读取：
- docs/thread_handoff/pm_operating_rules.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/DOC_INDEX.md

本轮只做 docs consolidation review。核对这四个文件是否准确反映当前 PM workflow、Sprint 3 gate、b43a12f baseline 和 prompt minimization 规则。

如 PASS，返回 exact docs-only commit allowlist。
不要 stage，不要 commit，不要 push。
按 pm_operating_rules.md 的窗口短报告规则返回。
```

After that review returns PASS, the PM may authorize an exact docs-only commit using the four-file allowlist listed in Section 7.
