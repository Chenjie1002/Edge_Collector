# ChatGPT PM Operating Rules

Updated: 2026-08-03

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

### Pre-authority local repair window

PM may explicitly delegate a bounded `PRE_AUTHORITY_LOCAL_REPAIR_WINDOW` to the executing Thread.
This delegation exists to close mechanical local defects without returning every syntax or artifact-
format mistake to PM. It never delegates remote, mutation, lifecycle, rollback, Git or phase-change
authority.

The repair window is valid only before any external or irreversible authority is consumed, including
SSH/network access, remote read or mutation, Docker/Compose lifecycle, deployment, activation,
rollback, DB/API/PLC/V-PLC interaction, production-data generation, Git stage/commit/push/tag or
cleanup outside the task-owned output paths.

The Prompt must state whether the window is authorized and must freeze a maximum repair-cycle
budget. The default is `not authorized`; when authorized, the normal maximum is two cycles. A cycle
means one bounded local edit set followed by the complete required local validation set. Exhausting
the budget without a clean local gate is `HOLD`; the Thread must not invent another cycle.

Eligible automatic repairs are limited to task-owned exact output paths and mechanical defects that
do not change product, runtime or authority semantics, such as:

- syntax, indentation, quoting, bracket or missing-import errors;
- local JSON/schema shape or required-field mistakes;
- incorrect references between the task's own exact artifacts;
- manifest sorting, duplication, self-exclusion or path-format defects;
- report/window formatting defects;
- local harness defects whose repair does not change the behavior or claim under test.

The Thread must stop and return PM instead of auto-repairing any change to:

- authority IDs, endpoint/user/credential identity or remote-call budget;
- image IDs, tags, service names, command categories or mutation counts;
- target, backup, sidecar, config or rollback paths and frozen hashes;
- write/read allowlists, PASS/HOLD semantics, stop conditions or next-gate meaning;
- rollback, cleanup, lifecycle or protected-object boundaries;
- source/product/runtime behavior, production-truth semantics or evidence authority fields.

Before the first task-owned write, the Thread must capture the fresh pre-task live facts. Those facts
may be held in memory initially, but they must be persisted in the declared local prerequisite
artifact before any external or remote authority is consumed. A separate pre-snapshot artifact is
required only when the Prompt explicitly declares one.

During the repair window, newly created exact helper/artifact paths are `TASK-OWNED MUTABLE DRAFTS`.
Their existence does not trigger `OUTPUT_PATH_PREEXISTS` within the same non-terminal task.
`OUTPUT_PATH_PREEXISTS` applies at initial task entry, or when a later authority attempts to reuse a
path terminalized by an earlier PASS/HOLD report, unless PM explicitly grants exact-path in-place
repair.

After all local checks pass, the Thread must create an `EXECUTION_LOCK` in its declared local
evidence. The lock must record at minimum:

- captured pre-task live facts and authority-input identities;
- final helper/artifact byte lengths and SHA-256 identities;
- local validation results and repair-cycle count with a concise repair summary;
- exact external/remote command, call budget and mutation authority to be consumed.

After `EXECUTION_LOCK`, execution helpers and authority-bearing fields are immutable. Any later local
failure is `HOLD`; no further repair, retry or authority-budget increase is allowed. A remote or
post-mutation failure can never reopen the local repair window.

### Canonical comparison for unordered discovery

Remote and runtime discovery commands often return sets in a non-authoritative order. A Thread must
not classify drift by directly comparing raw list order when the product claim concerns membership or
per-object identity rather than ordering.

Before comparing set-valued observations, the Thread must normalize them with a stable identity key
and deterministic field representation. Examples include:

- Compose containers and services: key by Compose service, then full container ID;
- container-ID discovery: compare as a sorted unique set when order has no authority;
- mounts: sort by type, source and destination, while retaining the read/write flag;
- image tags, sidecars and path sets: compare as sorted unique strings;
- dictionaries or JSON objects: compare after deterministic key ordering without dropping fields.

The raw observation and the normalized comparison input must both remain in durable evidence. A raw
ordering difference alone is diagnostic-only and must not become a `HOLD` blocker. Duplicate stable
keys, missing objects, additional objects or field differences after normalization remain real drift
and must fail closed when they affect the authorized invariant.

Within an authorized pre-authority local repair window, a Thread may mechanically correct missing or
incorrect canonicalization and rerun the full local validation set when the stable key and comparison
semantics are already frozen by the Prompt or accepted durable authority. It must return PM when
choosing a new authority key, dropping compared fields or otherwise weakening PASS/HOLD semantics
would be required.

### Local and remote identity authority separation

A local repository path and a remote deployed path with the same filename are separate objects. Their
byte length, hash, ownership, mode, topology role and update history must not be assumed equal.

Every Prompt that compares or mutates a remote file must name separately:

- the local source identity, when relevant;
- the remote deployed identity and the durable or fresh-remote authority that established it;
- whether local-to-remote byte equality has actually been established by an accepted deployment gate;
- which identity is terminal for the current remote prerequisite.

A committed or current local file hash is not a valid expected remote hash merely because the paths
share a basename. Remote expected identity must come from accepted remote evidence or from a fresh
read-only observation in the current authority. When accepted remote evidence and the local checkout
differ, that difference is not drift unless the current gate explicitly requires and has already
established local-to-remote equality.

Within an authorized pre-authority local repair window, a Thread may correct a local/remote authority
reference mechanically only when the intended remote identity is explicit in PM-named, accepted
durable evidence and the correction does not broaden the remote object, command or PASS claim. If
multiple plausible remote identities exist, the evidence conflicts, or a new identity must be
selected, the Thread must return `HOLD` to PM rather than choosing one.

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

Before assigning a task, PM must make two separate assessments:

Owner-facing main-Thread routing assessment:

- task size;
- expected file scope;
- whether the current Owner/PM conversation has enough context capacity;
- whether the Owner should manually dispatch the task into a new top-level Thread;
- the reason for continuing the current top-level Thread or opening a new one.

This routing recommendation is for the Owner only. It belongs in the Owner summary and must not be written as an instruction for the executing Thread to open、switch or create a new top-level conversation/window/Thread. Repository-backed tasks are manually dispatched by the Owner.

Executing-Thread sub-agent assessment:

- whether sub-agents are recommended to improve execution efficiency or review quality;
- the exact independently delegable subtask(s), or `none`;
- the reason sub-agents are or are not appropriate;
- the authority boundary: sub-agents inherit no authority beyond the task file, and the assigned core Thread remains responsible for integration、validation and the final report.

The sub-agent assessment must appear inside the authoritative task file. Future Thread prompts must use the fixed outer template in this section. This is a mandatory governance format, not a preferred example.

Before issuing any Architecture / Integration、Reliability、Data Quality or Verification Prompt, PM must re-read this section and audit the completed Prompt against the mandatory field checklist below. Correct task content does not excuse a non-conforming Prompt structure.

### Repository-backed Prompt dispatch

Repository-backed Prompt mode is the mandatory default for every new Architecture / Integration、Reliability、Data Quality or Verification task unless the Owner explicitly overrides it for that one task. The complete authoritative Prompt must be materialized as one uniquely named repository file:

```text
docs/thread_handoff/pm_task_<YYYYMMDDTHHMMZ>_<task-id>_<slug>.md
```

Naming rules:

- the timestamp is UTC and uses the exact minute-resolution form `YYYYMMDDTHHMMZ`;
- `<task-id>` and `<slug>` use lowercase ASCII letters, digits and underscores only;
- task-ID separators such as `-` or `/` are normalized to underscores;
- the slug is concise, stable and describes the authorized task rather than its result;
- every task file path is unique and an existing task file must never be overwritten.

The task file itself must contain the complete fixed 16-section Prompt defined below. The first required-reading item inside the Prompt must be the task file itself, and the executing Thread must verify its exact path, regular/non-symlink type, byte length and SHA-256 against the Owner launcher before reading other authority files or performing any task action.

The Chat window must not repeat the full Prompt. It must show only:

1. a concise Owner summary covering the Gate, assigned core Thread, Owner-facing recommendation on whether to dispatch into a new top-level Thread, task-file sub-agent recommendation, principal authority boundary, major mutations or command budgets, decisive PASS/HOLD stop condition and single next gate;
2. the task-file identity: exact repository path, bytes, SHA-256 and current Git state;
3. a short launcher instructing the already selected executing Thread to read that exact task file first, verify the identity and execute only the authority contained there.

The launcher must not instruct the executing Thread to open、switch or create a new top-level conversation/window/Thread. That dispatch decision belongs to the Owner. The launcher is not independent authority and must not broaden, summarize away or contradict the task file. When the launcher and task file differ, the executing Thread must stop with `HOLD / TASK_FILE_LAUNCHER_IDENTITY_OR_AUTHORITY_MISMATCH`.

The launcher must use this fixed structure and order:

```text
你是 Edge MES Demo 项目的独立 <Architecture / Integration | Reliability | Data Quality | Verification> Thread。

项目绝对路径：

`/Users/chenjie/Documents/MES/edge-mes-demo`

首先读取并核验以下 authoritative task file：

`<repository-relative task path>`

Expected identity：

- regular / non-symlink
- bytes：`<exact bytes>`
- SHA-256：`<exact lowercase SHA-256>`

必须在读取任何其他 repository content、运行 Python、执行 Git 命令、测试、probe、调用 sub-agent 或写入文件前完成 task self-identity gate。

该 task file 是本轮完整且唯一的 authority。Launcher 不构成独立 authority，也不得扩张、缩减或替代 task file 内容。

若 path、type、bytes、SHA-256 或 authority 与 launcher 不一致，立即停止并返回：

`HOLD / TASK_FILE_LAUNCHER_IDENTITY_OR_AUTHORITY_MISMATCH`

核验通过后，严格按照 task file 执行。不得继承其他 core Thread 或 predecessor task 的隐含 authority。

本任务只授权 <one concise sentence naming the exact principal scope and exact durable output authority>。

不授权 <one concise sentence naming the principal excluded mutations/phases>。
```

Launcher-specific path rule：the project absolute path appears exactly once in the launcher；the task path and every repository-internal path in the launcher are relative to that project root；external retained/runtime/remote paths are omitted from the launcher unless they are the principal target and are necessary to prevent ambiguity。

Task files are authority and audit records:

- they must not be added to `.gitignore` or any exclude mechanism;
- immediately after materialization they must be regular, non-symlink, not ignored, visible in `git status`, untracked, unstaged and not indexed unless a separate prior Git authority explicitly establishes another state;
- their path must be included in exact untracked-membership accounting;
- writing or dispatching a task file does not authorize staging, commit, push or tag;
- stage、commit、push and tag require later independent exact-path Git authority;
- after the Owner launcher publishes the file identity, the file is immutable for that dispatched task. A correction requires a new unique task file and a new launcher that explicitly supersede the prior file, unless the Owner grants an exact pre-execution in-place correction before the executing Thread consumes authority.

A Prompt already dispatched before this rule was materialized is not retroactively invalidated. This mode applies beginning with the next newly issued Thread Prompt.

### Identity verification tiers and SHA mismatch triage

Exact SHA-256 remains a hard authority gate only where the current task depends on exact bytes to determine authority or executable behavior. Do not turn every required-reading file into a transcription-sensitive hard gate.

Use these three identity classes:

1. `AUTHORITY_HARD_GATE`
   - includes the current repository-backed task file, any execution/commit/deploy authority artifact, and any helper/test/spec/evidence object whose exact bytes are directly consumed to perform the authorized action;
   - require exact path, regular/non-symlink type, byte length and mechanically compared SHA-256;
   - a confirmed byte mismatch is HOLD.
2. `PROTECTED_CONTINUITY`
   - includes legacy helpers/tests, adapters and other files that must remain unchanged during the task but whose historical expected bytes are not themselves the current authority source;
   - compute and record an entry identity from the live file, then recompute at the final audit and require `final == entry`;
   - do not require a task-embedded historical expected SHA unless the task has a specific reason that exact historical bytes are authority-bearing.
3. `HISTORICAL_OR_SEMANTIC_READ`
   - includes prior reports, prior planning tasks, status/history documents and other context used only for bounded semantic facts;
   - require exact path plus regular/non-symlink existence and validate the task-relevant semantic facts;
   - SHA may be recorded diagnostically but mismatch alone is not HOLD unless the current task explicitly upgrades that file to `AUTHORITY_HARD_GATE`.

Expected SHA values must never be manually retyped for comparison when a machine-readable source line or live file can be compared mechanically. A Thread must not classify `REQUIRED_READING_IDENTITY_MISMATCH` from a copied or summarized SHA string without first performing the triage below.

SHA mismatch triage is mandatory and does not consume a pre-authority repair cycle because it is read-only classification, not repository repair:

1. re-read the exact authoritative task/launcher line once from the source file rather than from prior chat text or a copied value;
2. verify that any expected SHA is exactly 64 lowercase hexadecimal characters; a malformed/truncated copied value is a validator/transcription defect, not repository drift;
3. recompute the live file SHA once with an approved read-only hashing command;
4. compare expected and actual mechanically without retyping either value;
5. if the authoritative source line and live file agree, continue and record `SHA_TRIAGE_FALSE_MISMATCH`; do not consume repair budget and do not terminalize the task;
6. only when the mechanically re-read authoritative expected identity genuinely differs from the live object may the Thread return an identity-drift HOLD.

A failed diagnostic command used only for this triage is not itself a repair cycle when it reads no unauthorized repository content and performs no mutation; rerun the same bounded check with a corrected invocation and record the diagnostic defect. Broad reads, unauthorized paths or any mutation remain governed by the normal allowlist and can still be terminal HOLD.

New task prompts should minimize embedded SHA ledgers. Prefer:

- exact SHA hard gates for the task itself and action-bearing executable/authority artifacts;
- entry/final continuity for protected non-authority files;
- semantic validation for historical/background reads.

The launcher task self-identity gate remains unchanged and strict.

### Governed local repository write target and path-base rule

Repository mutation safety is determined by the effective resolved target inside the declared local repository/worktree, not by any product-specific tool name or remote workspace abstraction. A Codex local Thread operates directly on its local checkout/worktree and must not be required to obtain Devspace、MCP workspaceId or another external workspace binding unless that external environment is itself the explicit task target.

For governed repository writes:

- before the first repository mutation, verify the local execution root with read-only facts: physical `cwd` and `git rev-parse --show-toplevel` must both resolve to the declared project root for the active checkout/worktree;
- every task-owned mutation target must be one exact allowlisted repository-relative path. `..`、path traversal、globs、directory-level targets and inferred output paths are forbidden. If a local editing primitive requires an absolute path, the Thread must mechanically prove that the resolved target is exactly `project_root / allowlisted_relative_path` before mutation;
- write primitives are environment-specific implementation details, not governance authorities. Codex Local may use the local editor/patch/write primitive actually available in that Thread only when its path base or explicit target can be verified for that invocation. Do not require Devspace、workspaceId、MCP binding or another tool that is unavailable in the local Codex execution environment;
- generic patch/edit primitives, including `apply_patch`, are not globally forbidden by name. They are permitted only when the current environment exposes or otherwise allows the Thread to prove the effective target/base before the first authority-bearing write. If the primitive's path base is ambiguous or cannot be proven, do not use that primitive; choose another local editing method whose exact target is verifiable;
- shell redirection、heredoc、`tee`、`sed -i`、`perl -i`、generated patcher scripts or other mutation mechanisms remain forbidden when the task or harness cannot prove exact target confinement and changed-path accounting. A task may explicitly authorize a different mechanism only with an exact root/target contract;
- immediately after the first write performed with a mutation primitive in a task, verify that the expected allowlisted repository path exists or changed as intended and inspect changed-path accounting. When the primitive previously exhibited an uncertain base, also verify that the known repository parent/sibling location does not contain a same-suffix stray object before continuing;
- a write that actually lands outside the exact allowlist is a real unauthorized mutation and is terminal HOLD unless the Owner grants separate exact cleanup/recovery authority. Do not silently delete、move、adopt or retry the stray object;
- an external cleanup action is never inherited from repository write authority. It requires an explicit exact absolute-path cleanup authorization and must not broaden into parent-directory cleanup or recursive deletion;
- task prompts that authorize local repository writes must state the root/target proof required before mutation, but should avoid hard-coding product-specific tool brands unless that specific tool is itself part of the task contract;
- an environment-specific binding failure such as missing Devspace/workspaceId is not repository drift when the task is intended for Codex Local and the declared local checkout/worktree is valid. If no mutation or authority-consuming action occurred, PM may reject that HOLD as `CROSS_ENVIRONMENT_TOOL_BINDING_ASSUMPTION` and relaunch under the environment-neutral rule.

This rule applies to all newly launched or relaunched mutation tasks. Existing terminal HOLDs caused by an actual out-of-allowlist write remain real historical HOLDs; a later cross-environment binding HOLD does not erase that history, but it also does not create a new repository defect when no mutation occurred.

### Host control-plane Python 3.14 runtime freeze

Any PM task that uses host-side Python for authority-bearing discovery, parsing, hashing, archive inspection, validation, evidence generation, test execution or direct-final record creation must use the frozen project control-plane runtime below. This rule applies to host-side PM/Thread tooling only; it does not change the Collector product runtime, Dockerfile base image, container runtime or any separately frozen candidate runtime.

Frozen runtime identity until an explicit Owner-approved governance or environment update supersedes it:

```text
formula line       = homebrew/core/python@3.14
formula version    = 3.14.6
entrypoint         = /opt/homebrew/opt/python@3.14/bin/python3.14
resolved target    = /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14
version            = Python 3.14.6
architecture       = arm64
resolved bytes     = 52448
resolved SHA-256   = b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf
```

Mandatory invocation and acceptance rules:

- use the exact absolute entrypoint `/opt/homebrew/opt/python@3.14/bin/python3.14`; use `-B` or `PYTHONDONTWRITEBYTECODE=1` whenever repository or attempt-root bytecode creation is not explicitly authorized;
- `/usr/bin/python3`, Command Line Tools Python, `xcrun python3`, unqualified `python`/`python3`, `/usr/bin/env python*`, generic `/opt/homebrew/bin/python3` and implicit PATH resolution are forbidden for authority-bearing host-side Python work unless one task receives an explicit exact-runtime override from the Owner;
- before the first task-owned write, package mutation, Docker/daemon call, network call or remote call, the executing Thread must verify the entrypoint, link resolution, exact patch version, `sys.executable`, `platform.machine()`, resolved regular/non-symlink executable type, bytes and SHA-256;
- the same exact interpreter that will execute the real parser or producer must execute a pre-write compatibility smoke for every nontrivial language or standard-library primitive on which the task depends, including examples such as `zip(..., strict=True)`, `tarfile`, `pathlib`, JSON encoding, UTF-8 handling and required hashing APIs;
- a smoke performed with another interpreter, another path or another Python minor version is not transferable evidence;
- the task Prompt must record the frozen runtime identity and exact required primitive smoke. Runtime or primitive drift is `HOLD / HOST_CONTROL_PLANE_PYTHON_RUNTIME_DRIFT_OR_INCOMPATIBILITY` before authority-consuming work;
- there is no fallback interpreter after authority consumption. Repair, package install, upgrade, downgrade, relink or runtime substitution requires a new explicit environment authority;
- this governance rule does not itself authorize Homebrew install/update/upgrade, shell-profile changes, PATH changes, symlink mutation or Python package installation;
- a future Python 3.14 patch change or migration to another minor version requires an explicit Owner-approved governance/environment update that freezes the replacement identities before a dependent task is dispatched.

A Prompt already terminalized before this runtime freeze remains historical and must not be edited, retried or reclassified. This runtime rule applies beginning with the next newly issued Thread Prompt.

The required outer order is:

1. report identity;
2. task identity;
3. executing Thread;
4. project absolute path、repository path convention and PM workload / sub-agent assessment;
5. report delivery mode and exact output authority;
6. authority source;
7. required reading order;
8. fresh recovery / live-fact checks;
9. current gate and authority boundary;
10. exact task scope and execution steps;
11. exact write / command / remote / Git allowlist;
12. explicitly excluded and forbidden operations;
13. PASS / HOLD criteria and stop conditions;
14. required validation and evidence;
15. required window-report format;
16. next gate and non-inheritance statement.

A section may be short when it does not apply, but it must remain visible and state `none`、`not applicable` or `not authorized`; PM must not silently omit authority-bearing sections.

The authoritative repository-backed task file must use this template:

```text
报告名称：
<Report name>

任务名称：
<Task name>

执行 Thread：
<Architecture / Integration | Reliability | Data Quality | Verification>

项目绝对路径：
/Users/chenjie/Documents/MES/edge-mes-demo

Repository path convention：
- the project absolute path is declared exactly once in this dedicated field;
- every other repository-internal task、report、artifact、source、test and required-reading path in this Prompt must be relative to that project root;
- paths outside the repository, including retained、runtime、remote、mount or deployment paths, remain exact absolute paths;
- before using any relative repository path, the executing Thread must verify that its working directory is the exact project root;
- do not repeat the project absolute path elsewhere in the authoritative task file or its machine blocks unless a frozen external tool contract makes an absolute value technically unavoidable; any such exception must be named and justified explicitly;
- the separately published launcher declares the same project absolute path exactly once under its own fixed launcher template and otherwise uses repository-relative paths.

PM 任务前工作量 / sub-agent 评估：
- 任务规模：小 / 中 / 大
- 涉及范围：<expected file/domain scope>
- 是否建议使用 sub-agent：yes / no
- sub-agent exact scope：<independently delegable subtasks, or none>
- 理由：<efficiency、quality、independence and integration-boundary reason>
- authority boundary：sub-agents inherit no authority beyond this task file；the assigned core Thread owns integration、validation and the final report

Report delivery mode：
<CHAT_ONLY | CONVERSATION_ATTACHMENT | REPOSITORY_DURABLE_REPORT | REPOSITORY_REPORT_WITH_ARTIFACTS>

Exact report path：
<none or one exact path>

Exact artifact paths：
<none or one exact path per artifact>

Docs / artifact write authority：
<not authorized | granted for the exact paths above only>

Authority source / ID：
<exact PM handoff, report, authority ID or current user instruction>

请先按顺序读取：
1. <this exact repository-backed task file; verify path, regular/non-symlink type, bytes and SHA-256 against the Owner launcher>
2. docs/thread_handoff/pm_operating_rules.md
3. docs/current_status.md
4. <current PM handoff or authority file>
5. <task-specific gate/status docs>
6. <task-specific source/contract/report/evidence files>

Fresh recovery / live facts：
- <exact read-only commands or checks required before work>
- <expected baseline, dirty/cached state and process/output absence checks>
- live facts override historical document snapshots

Current gate / authority boundary：
- <accepted prior gates>
- <current task authority>
- <authorities explicitly not granted>
- prior PASS does not authorize the next phase

本轮任务：
1. <exact required action>
2. <exact required action>
3. <stop point and delivery requirement>

Exact allowlist：
- files that may be read:
- files that may be created or modified:
- commands/tests that may be run:
- host control-plane Python runtime: exact entrypoint, resolved identity, version/architecture/bytes/SHA-256 and pre-write primitive compatibility smoke, or `not applicable`
- pre-authority local repair window: not authorized | authorized, with exact cycle budget and eligible repair classes
- execution lock: required fields and the point after which helpers become immutable
- unordered discovery: stable canonicalization keys and raw-versus-normalized evidence requirements
- local/remote identities: separate expected identities and the authority source for each
- remote calls, if any:
- Git actions, if any:

明确排除 / 禁止：
- <pre-existing dirty and external artifacts>
- <out-of-scope source, runtime, DB, API, frontend, V-PLC, deploy or lifecycle surfaces>
- <stage/commit/push/tag/cleanup/reset/stash rules>

PASS / HOLD criteria and stop conditions：
- PASS only when: <exact terminal conditions>
- HOLD when: <drift, ambiguity, failed checks, allowlist violation or unauthorized action>
- on HOLD: <stop immediately; no repair/retry/cleanup unless separately authorized>

Required validation / evidence：
- <tests, manifests, hashes, process audit, Git audit and evidence boundaries>
- distinguish local/synthetic/static evidence from remote/runtime/production evidence

窗口返回格式：
- use the report format required by Section 11
- keep the Chat report concise when durable output is required
- include conclusion, changed files, checks, allowlist, Git state, blockers, recommendations, next gate, MVP alignment and Thread context assessment

Next gate：
- <single next PM intake or review gate>
- do not infer implementation, remote, Git, deploy, restart, activation or later-phase authority from this task result
```

Mandatory pre-dispatch audit：

- the complete Prompt is stored in one unique `docs/thread_handoff/pm_task_<YYYYMMDDTHHMMZ>_<task-id>_<slug>.md` file;
- the task filename uses UTC, normalized lowercase task ID and slug, and does not overwrite an existing path;
- the task file is regular, non-symlink, not ignored, visible in `git status`, untracked, unstaged and not indexed at initial dispatch unless separately authorized otherwise;
- the task file is the first required-reading item and requires exact path/bytes/SHA-256 verification before any other task action;
- the Chat response contains only the Owner summary, exact task-file identity and short launcher, not the full Prompt body;
- the Owner summary contains the Owner-facing top-level Thread routing recommendation; the task file and launcher do not instruct the executing Thread to open、switch or create a new top-level conversation/window/Thread;
- the task file explicitly states whether sub-agents are recommended, their exact independently delegable scope or `none`, the reason, and the non-inheritance/integration boundary;
- the launcher follows the fixed role-first template：assigned core Thread；project absolute path exactly once；repository-relative task path；expected regular/non-symlink、bytes and SHA-256；pre-action self-identity gate；complete-authority statement；mismatch HOLD；concise principal authorization and exclusion boundaries；
- the launcher states that the task file is complete authority and does not broaden or contradict it;
- the project absolute path appears exactly once in the authoritative task file's dedicated project-path field and exactly once in the separately published launcher；all other repository-internal paths are relative to that root, while external/runtime/retained/remote paths remain exact absolute paths inside the task file;
- the executing Thread is required to verify the exact project root as its working directory before resolving repository-relative paths;
- exact task-file membership is included in the expected working-tree accounting;
- Git stage、commit、push and tag for the task file remain separately authorized;
- every heading above is present in the required order;
- task-specific authority, allowlist and prohibited operations are explicit;
- when host-side Python is used, the Prompt freezes the Section 10 Python 3.14 entrypoint and identity, forbids implicit/PATH/Apple CLT fallback, and defines exact pre-write primitive compatibility smoke;
- report delivery mode and exact output paths are declared before execution;
- remote-call budget and consumption rules are explicit when remote access is involved;
- the Prompt explicitly states whether a pre-authority local repair window is authorized, its cycle budget, eligible repair classes and forbidden authority-bearing changes;
- when repair is authorized, the Prompt defines the execution-lock evidence and helper immutability point;
- Git stage、commit、push and tag authority are independently stated;
- PASS、HOLD、stop behavior and next gate are explicit;
- no wording implies that an earlier PASS automatically grants a later phase;
- the Prompt does not depend on another Thread's implicit memory or a conversation-only attachment;
- the Prompt does not repeat or reissue a task when PM has explicitly accepted the current task and only requested future template correction.

If task-specific docs are incomplete or inconsistent with the working tree on
gate state, allowlist, scope, authorization boundary, excluded files or
out-of-scope surfaces, stop and report `HOLD`. A durable baseline hash that
names the last verified docs/status sync baseline is not by itself a blocker
when live `git rev-parse` output shows only later authorized docs-only commits.

## 11. Window report, durable report and cross-Thread handoff

This section is effective immediately for every new PM task, repair, review and Verification gate.

Future Codex Threads must keep the chat-window report short and put durable detail in repository documents when the result must be preserved, independently reviewed or reused by another Thread.

### 11.1 Report delivery classification

Every task Prompt must classify its intended report delivery as one of:

```text
CHAT_ONLY
CONVERSATION_ATTACHMENT
REPOSITORY_DURABLE_REPORT
REPOSITORY_REPORT_WITH_ARTIFACTS
```

The meanings are:

- `CHAT_ONLY`: a short conclusion, blocker list or temporary read-only summary. It is not durable cross-Thread authority.
- `CONVERSATION_ATTACHMENT`: a file supplied through the current chat. It is external conversation evidence, not a repository file, and must not be assumed accessible from another Thread, Codex session or workspace.
- `REPOSITORY_DURABLE_REPORT`: a report written to one exact repository path under explicit docs-write authority.
- `REPOSITORY_REPORT_WITH_ARTIFACTS`: a durable report plus exact source, helper, fixture, test, manifest or log artifact paths required for later independent review.

A chat attachment, `/mnt/data/...` path, downloaded file or prior window transcript must never be represented as an existing path under the project checkout.

Conversation attachments must be classified as:

```text
EXTERNAL CONVERSATION EVIDENCE
NOT A REPOSITORY FILE
NOT DURABLE CROSS-THREAD AUTHORITY
```

If attachment content is needed by another Thread, PM must either:

1. authorize materialization to exact repository paths; or
2. restate every required fact and requirement completely in the next Prompt.

The next Thread must not depend on implicit attachment access.

### 11.2 Mandatory durable-delivery triggers

A task must use `REPOSITORY_DURABLE_REPORT` or `REPOSITORY_REPORT_WITH_ARTIFACTS` when any of the following is true:

- the report is expected to exceed approximately 200 lines;
- it includes more than approximately 50 lines of code;
- it includes an executable helper, deployment command, rollback command or test harness;
- it contains extensive logs, matrices, test results or evidence terminals;
- a later Architecture / Integration, Reliability, Data Quality or Verification Thread must reuse or independently inspect it;
- source-evidence identity must prove that displayed source, tested source and future execution source are the same bytes;
- the result changes or supports a durable gate, deployment, activation, rollback or production-truth claim.

A task matching these conditions must not return its complete report only in Chat and must not delete the only tested source after reporting its hash.

Small, temporary and read-only tasks may remain `CHAT_ONLY` when no later Thread needs the full detail.

### 11.3 Prompt-time output authority

For durable delivery, PM must declare all output paths before execution. The Prompt must include:

```text
report delivery mode:
REPOSITORY_DURABLE_REPORT | REPOSITORY_REPORT_WITH_ARTIFACTS

exact report path:
docs/reports/<exact-name>.md

exact artifact paths:
<none or one explicit path per artifact>

docs/artifact write authority:
granted for exact paths only

Git stage / commit / push:
not authorized unless separately granted
```

The Thread may create or modify only those exact output paths. It must not choose additional report, helper, fixture, log or manifest paths by convenience.

Docs/artifact write authority does not authorize source changes, staging, commit, push, tag, cleanup outside authorized paths or remote mutation.

### 11.4 Durable artifact layout and source-evidence binding

Code-heavy evidence should use a bounded layout such as:

```text
docs/reports/<task-report>.md
docs/reports/evidence/<task-id>/<helper-or-fixture-1>
docs/reports/evidence/<task-id>/<helper-or-fixture-2>
docs/reports/evidence/<task-id>/manifest.sha256
```

Every persisted artifact must have a declared responsibility and exact path.

When executable source or a test harness is part of the evidence, the required order is:

```text
capture fresh pre-task live facts before the first task-owned write
→ generate exact artifact files
→ when explicitly authorized, repair only eligible mechanical defects within the frozen cycle budget
→ after every repair cycle, rerun the complete required local validation set
→ compute preliminary identities
→ run syntax/compile checks on those exact files
→ run all tests by importing or executing those exact files
→ compute final byte lengths and SHA-256 values
→ verify no artifact changed after the final test
→ persist the local prerequisite evidence and EXECUTION_LOCK before external/remote authority consumption
→ consume the separately authorized execution authority, if any
→ write the final report and manifest
→ remove only separately authorized synthetic temporary files
```

The pre-task facts may be captured in memory before helper creation and persisted later in the
exact declared local prerequisite artifact. Do not require a separate pre-snapshot file unless the
Prompt grants that exact output path. Once the task emits a terminal PASS/HOLD report and manifest,
its output paths are terminalized and cannot be reused by a later authority without explicit PM
in-place-repair authorization.

The following are prohibited:

- testing an embedded or temporary copy while reporting a different repository artifact;
- modifying a helper after its final test without rerunning the full suite;
- deleting the only exact source and retaining only its hash;
- placing a second helper implementation inside the test harness;
- representing synthetic PASS as remote, deployed, activated or production evidence;
- using a temporary path as future cross-Thread authority.

A hash proves identity only when the corresponding bytes remain available to the reviewer.

### 11.5 Chat-window manifest

For durable tasks, the Thread must return a concise manifest rather than pasting the full report or helper source into Chat.

Default durable window manifest:

```text
报告名称：
任务名称：
执行 Thread：
结论：PASS / PASS WITH RECOMMENDATIONS / HOLD

Report delivery mode:
Report path:
Report bytes:
Report SHA-256:

Artifacts:
- path:
  bytes:
  SHA-256:
  role:

Changed files:
Tests/checks:
Allowlist compliance:
Git staged:
Git committed:
Git pushed:
Blockers:
Recommendations:
Next gate:
MVP 路径一致性:
Thread 输出 / 上下文评估:
```

The manifest must distinguish:

```text
WRITTEN
REVIEWED
ACCEPTED
VERIFIED
STAGED
COMMITTED
PUSHED
DEPLOYED
ACTIVATED
```

None of these states implies another.

Do not paste full command output into the chat window unless a command fails, a gate is `HOLD`, PM explicitly asks for raw output, or the raw fragment is necessary to explain a blocker. Even on `HOLD`, prefer the minimum failing excerpt and keep the complete evidence in the durable report when a report path is authorized.

### 11.6 PM intake requirements

PM intake for a durable task must read the actual repository files from their exact paths and must verify:

- changed-file allowlist;
- report existence, byte length and SHA-256;
- artifact existence, byte lengths and SHA-256 values;
- manifest consistency with repository content;
- tests executed against the persisted exact artifacts;
- final Git state and authority boundaries;
- whether the report is merely written or has also been reviewed, accepted, verified, committed or pushed.

A Chat summary, attachment title, reported path or reported hash must not substitute for reading the actual durable files.

If PM cannot access the declared durable report or artifact, intake must report `HOLD / DURABLE EVIDENCE NOT ACCESSIBLE`. PM must not infer PASS from the Chat manifest alone.

### 11.7 Cross-Thread authority

A later Thread may rely only on:

- committed repository authority files;
- exact-path durable reports and artifacts that PM has explicitly accepted in the current checkout;
- facts and authority fully restated in its own Prompt.

A later Thread must not rely on:

- content that was only pasted into a previous chat window;
- a conversation attachment that was not materialized;
- `/mnt/data/...` or other temporary conversation paths;
- deleted synthetic files;
- another Thread's implicit memory;
- an unverified path mentioned in a prior report.

Uncommitted durable reports may be used only when PM explicitly names the exact paths and confirms they exist in the current checkout. Their uncommitted status must remain visible and they must not be mistaken for committed authority.

### 11.8 Default report content

Every Thread report, whether Chat-only or durable, must include the report name, task name, executing Thread, conclusion, Scope, Evidence, Blockers, Recommendations, Next gate, MVP-path alignment and Thread output/context assessment.

Default short window report requirements:

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
- 当前 Thread 是否建议继续承载后续任务：yes / no
- Owner 是否应在下一轮手工分发到新的top-level Thread：yes / no
- 本任务sub-agent计划：yes / no；exact scope / none
- 本任务sub-agent实际使用：yes / no；实际scope / none
- 理由：
```

When returning a report, the Thread must reassess context capacity after completing the task. This reassessment is advisory metadata for the Owner only; the executing Thread must not open、switch or create a new top-level conversation/window/Thread. It must state:

- the current output length;
- whether the current Thread can continue to carry the next task;
- whether the Owner should manually dispatch the next round into a new top-level Thread;
- the task-file sub-agent recommendation and the actual sub-agent usage/scope;
- the reason for those recommendations and any variance from the task-file sub-agent plan.

Do not repeat long-term background already stored in project docs. Reference the relevant durable paths instead.

When a repository report/status file is updated, the window manifest must include:

- the exact path updated;
- the report and artifact identities;
- the final conclusion;
- changed files;
- tests or checks run;
- blockers/recommendations;
- next gate;
- Git staged/committed/pushed state.

If a task changes current gate status, update the relevant gate/status document under explicit authority or explicitly state why it was not updated.

### 11.9 Git authority separation

Writing a durable report or artifact establishes only:

```text
WRITTEN
```

It does not establish:

```text
ACCEPTED
VERIFIED
STAGED
COMMITTED
PUSHED
DEPLOYED
ACTIVATED
```

Stage, commit, push and tag remain separate PM authorities with exact changed-file allowlists. A report-writing Thread must stop after its manifest unless further Git authority was explicitly included in the same Prompt.

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
