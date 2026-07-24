# ChatGPT PM Operating Rules

Updated: 2026-07-24

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
| simple exact-path stage/commit/push after review gates pass | PM directly |
| commit authorization, push authorization, tag/deploy/rollback authorization | PM only |

Simple commit gates are PM execution work, not a separate long-lived Thread. After Architecture / Reliability / Data Quality / Verification review gates pass with no blockers, PM may directly run the exact-path stage/commit/push sequence when explicitly authorized by the user. PM must still preserve the exact allowlist, verify the staged set before commit, exclude external dirty artifacts, and report commit/push evidence.

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

### Task risk tiers

Before executing or issuing the next task, PM must classify it as one of these tiers:

| Tier | Default owner | Typical scope | Required workflow |
| --- | --- | --- | --- |
| Level 0 | PM directly | exact-path commit/push, small PM rule edits, simple status/hash sync, mechanical docs updates | exact allowlist, staged-set audit when applicable, concise PM report |
| Level 1 | one focused Thread | low-risk docs/tests/contracts changes that do not alter runtime behavior or authority semantics | compact prompt, exact allowlist, focused validation |
| Level 2 | full gate sequence | runtime behavior, PLC/V-PLC, ACK/read_done, DB write path, `storage.py`, decoder/registry authority, raw/normalized evidence, schema/config semantics | planning before implementation, exact implementation allowlist, Reliability/Data Quality/Verification focused reviews before commit |

Do not use the Level 2 workflow for Level 0 work. Do not downgrade Level 2 work because it looks small in line count.

Uncertainty handling follows the same tiering:

- If uncertainty affects safety, authority, PLC/V-PLC/runtime behavior, DB write path, ACK/read_done, deployment, or irreversible Git actions, stop and ask PM.
- If uncertainty only affects low-risk wording or mechanical docs, make a conservative best effort and report assumptions.

### Remote config deployment and runtime activation separation

Remote config deployment is a Level 2 mutation even when the file content is already committed and
its change is small. It must not be combined with Collector restart, Collector activation, Compose
lifecycle, production data generation or D3 by convenience.

Before authorizing any remote config mutation, PM must freeze and record:

- the exact remote host and authority source;
- the exact read-only config mount source path and the container-visible target path;
- the current remote file identity, ownership and permissions;
- the exact local source identity, including Git baseline and file hash;
- the backup or rollback source and the conditions under which rollback may be executed;
- transport and privilege requirements;
- verification commands and stop conditions;
- explicit confirmation that config deployment does not authorize restart or activation.

Remote read authority, remote mutation authority, Docker/Compose authority, restart authority,
activation authority and rollback authority are separate grants. A planning report may recommend
one of them but cannot grant it. A successful config copy proves only deployment and identity; it
does not prove runtime load, Collector health, accepted-fact generation or production readiness.

## 4. Git safety rules

Never use broad staging unless PM explicitly authorizes it for a specific exceptional case.

Forbidden by default:

```bash
git add .
git add -A
git add docs/
```

Commit/push tasks must use exact path allowlists and verify staged files before committing. For simple commit gates, PM should perform this directly after explicit user authorization instead of creating another Thread prompt.

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
5. classify the next action as Level 0, Level 1 or Level 2;
6. decide whether to pause for process review, perform a PM-direct action, authorize repair, authorize next review, authorize exact commit/push or open the next planning gate;
7. issue the next minimal authorized task prompt only when continuing is clearly the right PM decision;
8. never infer authorization for implementation, staging, commit, push, deploy, rollback, D2-C/D3 or any later phase from a `PASS` report alone.

### Recommendation necessity and scope rule

PM must not forward reviewer recommendations automatically. For every recommendation received during report intake, PM must evaluate whether it is necessary for the current authorized product claim and gate, and classify it as one of:

- current-gate necessary repair;
- next-review or Verification carry-forward;
- runtime execution record requirement;
- future independent task;
- unnecessary, duplicate or scope expansion.

A recommendation that merely repeats an already-mandatory planning or contract requirement is not a new task. A recommendation must not enlarge the product claim, threat model, authority fields, retention model, runtime topology, implementation allowlist or evidence burden without explicit user approval. Only an item that is necessary to prevent a credible false PASS, stale or invalid production truth, unsafe process ownership, protected-object mutation or synthetic/local evidence misclassification may be promoted into a blocker or current repair.

PM should issue only the minimum accepted repair or next-gate scope. Rejected, duplicate or future-only recommendations must not become implicit requirements in later prompts. If no recommendation is necessary, PM should state `Recommendations: none` instead of inventing carry-forward work.

After every Level 2 task closes, PM should pause before chaining the next task and check whether any process rule, allowlist habit, validation gap or recurring mistake should be added to this file. Complex-task lessons should be recorded here only when they are stable project rules, not one-off observations.

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

### ChatGPT PM handoff workflow

A ChatGPT PM handoff should be created when the current ChatGPT PM window becomes long, after a Level 2 slice closes, before a new major planning branch, or whenever the user asks to start a new PM window.

PM handoff file names must be unique. New ChatGPT PM handoff files must use the timestamp suffix format `YYMMDD-hhmm` in China Standard Time / UTC+8, for example `docs/thread_handoff/chatgpt_pm_handoff_260629-2354.md`. Do not use browser-local, server-local, Japan, Pacific or inferred project machine time for this filename. Use UTC+8 even if the user or runtime environment is elsewhere. Never overwrite an existing PM handoff file.

Handoff flow:

1. Run read-only recovery first: `git status -sb`, recent log, live `HEAD`, live `origin/main`, working-tree diff name-only and cached diff name-only.
2. Confirm current gate state from durable status docs and live Git. If a review, commit or docs/status sync gate is still pending, finish or explicitly record it before handoff.
3. Generate one new handoff file under `docs/thread_handoff/` with the UTC+8 timestamp suffix.
4. The handoff must include project path, live baseline, latest commit, current closed gate, known external dirty artifacts, committed files, durable status references, non-authorized surfaces, carry-forward recommendations, and the recommended first read-only action for the next PM.
5. Include a copyable prompt for the next ChatGPT PM window. That prompt must instruct the new PM to perform read-only recovery before continuing.
6. Audit the generated handoff file path and internal references so the filename, title, suggested prompt path and commit note all match.
7. Do not stage the handoff file automatically. Ask the user for explicit exact-path stage/commit/push authorization.
8. If authorized, stage only the new handoff file and any explicitly authorized governance rule file. Verify `git diff --cached --name-only`, `git diff --cached --check` and `git diff --cached --stat` before commit.
9. Do not stage `.gitignore`, old PM handoff files, Keynote/reporting artifacts, broad `docs/`, or unrelated files.
10. After commit/push, report final `HEAD`, `origin/main`, staged files and remaining external dirty artifacts.

Governance documents such as this file, `README.md`, `docs/current_status.md` and gate status reports are durable project controls. They should be updated when PM rules, phase roadmap, Thread roles, baseline semantics or gate state materially change. Those updates require an explicit PM task and exact allowlist. They must not be bundled into code, runtime, schema, deployment or handoff artifact commits unless PM explicitly authorizes that bundle.

`README.md` is a public orientation document. It may summarize the project phases, Thread model and development workflow, but it must not replace the live gate/status documents. When README, PM rules and status files disagree on current authorization, Threads must stop and ask PM for a status repair instead of guessing.

## 10. Minimal prompt pattern

Before assigning a task, PM must record:

- task size;
- expected file scope;
- whether the current Thread has enough context capacity;
- whether a new Thread is needed;
- the reason for continuing the current Thread or opening a new one.

Future Codex prompts should prefer this short pattern.

When PM issues a task prompt for another Thread, the Thread prompt body must be returned as one complete copyable Markdown block. Do not split the Thread prompt body across multiple separate code fences. PM may write intake, judgment or explanation before or after the prompt, but the Thread prompt itself must remain a single copyable Markdown block so the user can copy it directly into the target Thread. Inside the copyable prompt, nested command, file and path examples may still use indented blocks or fenced examples when useful, provided the prompt body remains one copyable block.

Future Codex prompts should use this pattern:

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

MVP 路径一致性：
- 当前任务是否仍直接服务于已批准 MVP：yes / no
- 对应的 MVP 交付物或验收声明：
- 是否引入超出 MVP 的产品能力、威胁模型、证据体系或基础设施：no / yes（列出）
- 是否出现任务膨胀或验证框架替代产品交付：no / yes
- 若为 no/yes 异常，PM 处理建议：scope reset / backlog / 独立 Level 2 项目 / 其他

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

## 12. Evidence-gate scope control

Verification strength must be proportional to the product claim being made. A local synthetic
validation must not silently become a general-purpose tamper-resistant audit, archive or
forensics subsystem unless PM opens that work as a separate Level 2 project.

A review finding may block an evidence gate only when it can materially cause one of the
following outcomes:

- a false PASS for the product behavior under test;
- stale, incomplete or schema-invalid data being presented as valid production truth;
- an owned process or listener remaining active and contaminating a later run;
- an unknown process being selected for termination;
- deletion, overwrite or mutation of an object not proven to belong to the authorized task;
- synthetic, local or no-DB evidence being represented as production, deployed or DB-backed evidence.

Diagnostic precision, telemetry taxonomy, retained archive uniqueness, full failure-record
self-containment and cross-field completeness are recommendations unless they directly create
one of the blocker outcomes above. Every evidence plan must distinguish terminal authority
fields from diagnostic-only fields. Diagnostic-only fields must not acquire blocker authority
through review wording alone.

Reviewers must not expand the product claim, threat model, field authority, retention model or
runtime topology without explicit PM approval. After one focused repair and one independent
re-review of the same gate, a new blocker class requires PM to reassess scope and assurance
proportionality before authorizing another repair. PM may supersede an overgrown validation
branch with a narrower authority document; superseded executable literals must be clearly
marked and must not be run by conversational momentum.

Static review has a stopping rule: once all defined terminal invariants are covered and no
credible false-PASS or safety-boundary violation remains, new diagnostic completeness findings
move to backlog or recommendations. A reviewer may not require proof of every theoretically
possible state combination when those combinations cannot change the authorized PASS/HOLD
claim.

## 13. Mandatory MVP-path alignment check

At the end of every Architecture / Integration, Reliability, Data Quality or Verification task,
the executing Thread must explicitly reassess whether the completed work and the proposed next
gate still directly serve the currently approved MVP. This is a mandatory completion gate, not
an optional recommendation.

The reassessment must identify:

- the approved MVP deliverable or product claim that the task directly supports;
- the minimum terminal, safety or truth invariant that justified the work;
- any newly introduced product capability, threat model, evidence/retention framework,
  infrastructure, operational topology or review requirement;
- whether task or candidate size, number of repair rounds, number of blocker classes, report
  volume or validation complexity is growing faster than the MVP product claim;
- whether the work is still advancing the product, or whether the validation/governance
  mechanism has become the primary deliverable.

A task remains on the MVP path only when all of the following are true:

- it is necessary to implement or credibly validate an already approved MVP behavior;
- it prevents a concrete false PASS, stale production truth, unsafe mutation, foreign-object
  termination, unowned process contamination or synthetic/production evidence confusion;
- it does not silently add a broader product claim, threat model, audit/forensics subsystem,
  retention model, infrastructure layer or runtime topology;
- the assurance effort is proportional to the user-visible or operational MVP claim;
- the next proposed task is the smallest action that materially advances the MVP.

The following are warning signs of scope drift and task inflation:

- repeated repair/re-review cycles introduce new blocker classes instead of closing the original
  product risk;
- executable candidates, reports, matrices or evidence schemas grow substantially while the MVP
  behavior being proved remains unchanged;
- diagnostic completeness, archive uniqueness, full failure self-containment or theoretical state
  coverage becomes blocker authority without a direct false-PASS or safety consequence;
- a validation framework, governance process or evidence protocol becomes more complex than the
  product change it exists to validate;
- the next task mainly improves the review system rather than the MVP product or its minimum safe
  execution boundary.

If any warning sign is present, the Thread must report it and may not silently recommend another
repair. PM intake must independently classify the result as one of:

```text
MVP-ALIGNED
MVP-ALIGNED WITH BACKLOG ITEMS
SCOPE RESET REQUIRED
SEPARATE LEVEL 2 PROJECT REQUIRED
```

When the classification is `SCOPE RESET REQUIRED`, the current repair chain is paused. PM must
restate the MVP claim, retain only requirements that directly prevent the blocker outcomes in
Section 12, downgrade other findings to recommendations/backlog, and issue a narrower task.
When the classification is `SEPARATE LEVEL 2 PROJECT REQUIRED`, that work must receive an
independent objective, scope, allowlist, risk assessment and authorization; it must not block the
existing MVP by conversational momentum.

Every task window report and every PM intake must include an `MVP 路径一致性` section. A task
may not conclude `PASS` or `PASS WITH RECOMMENDATIONS` without this section. If the Thread omits
it, PM must treat the completion report as incomplete and request only the missing alignment
assessment before authorizing the next gate.

## 14. Data-first MVP and deferred UI acceptance policy

The approved Phase-2 execution order is data-first. Collector acceptance, production-fact
persistence, bounded API contracts and OEE / Quality / Trace data semantics may continue while a
Dashboard-only browser-rendering or visual acceptance gap remains open.

A UI-only gap is `DEFERRED / NON-BLOCKING` when all of the following are true:

- the authoritative DB and API data path has independent, production-relevant evidence;
- no evidence shows that the UI is displaying stale, false or cross-scope production truth;
- the UI cannot mutate production data, equipment control state or authority boundaries;
- the gap is limited to rendering proof, layout, empty-state presentation, interaction polish,
  screenshots or browser automation;
- the current gate does not explicitly define a demonstrable UI as its primary deliverable.

A UI issue becomes a current blocker only when it can:

- display stale, incorrect or synthetic data as fresh production truth;
- write or mutate production data, equipment state or security authority;
- conceal a DB/API contract, data-quality or failure-state defect;
- make the product unavailable for an explicitly authorized demonstration or UI delivery gate;
- prevent final integration, release acceptance or a committed operational workflow.

A deferred UI acceptance debt must remain visible in `docs/current_status.md` and the active PM
handoff. It must not be reported as `PASS`, silently dropped or used to claim a complete
DB/API/Dashboard runtime gate. It may coexist with continued MVP development and with an archived
Full Runtime `HOLD`.

Repeated browser-evidence or harness failures that do not establish a product defect must not
create an unlimited repair chain. After the PM stopping rule is reached, the branch is archived
and additional retries require a new product-level objective, not merely another evidence-tool
repair. Final UI acceptance should prefer the minimum proportional evidence: real runtime, fixed
test data, human browser inspection, key screenshots and a small focused smoke test. Building a
generic browser evidence or forensics platform is outside the MVP unless separately authorized.
