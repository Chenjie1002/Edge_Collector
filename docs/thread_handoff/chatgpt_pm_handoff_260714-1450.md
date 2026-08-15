# ChatGPT PM Handoff — 2026-07-14 14:50 UTC+8

报告名称：Edge MES Demo ChatGPT PM handoff after Option C retained-record Data Quality value-validation HOLD

任务名称：Transfer PM ownership before any D7/D8 planning repair or later Verification gate

执行角色：ChatGPT PM

```text
Project: Edge MES Demo
Project path: /Users/chenjie/Documents/MES/edge-mes-demo
Risk: Level 2
Mode: PM-handoff-only / docs-only

Committed baseline:
HEAD == origin/main == e04ee45f87e1b4b57237a285f337ac8be4686df9
latest commit: e04ee45 Add PM handoff after Dashboard URL validation closeout
ahead/behind: 0 0
cached diff: empty

Option C private-parent / run-root planning: accepted under T1–T3 boundary
Reliability Option C manifest review: PASS WITH RECOMMENDATIONS
Current Reliability blockers: none

Data Quality current gate: HOLD
DQ-RUNTIME-OPTIONC-D1: ACCEPTED / CLOSED
DQ-RUNTIME-OPTIONC-D2: HOLD / NOT ACCEPTED
DQ-RUNTIME-OPTIONC-D3: ACCEPTED / CLOSED
DQ-RUNTIME-OPTIONC-D4: RECOMMENDATION
DQ-RUNTIME-OPTIONC-D5: ACCEPTED / CLOSED
DQ-RUNTIME-OPTIONC-D6: HOLD / NOT ACCEPTED
DQ-RUNTIME-OPTIONC-D7: BLOCKER / OPEN
DQ-RUNTIME-OPTIONC-D8: BLOCKER / OPEN
DQ-RUNTIME-OPTIONC-D9: OBSERVATION
DQ-RUNTIME-D2-3: CARRY FORWARD
DQ-URL-D3: CARRY FORWARD

Verification: NOT AUTHORIZED
Private-parent preparation: NOT AUTHORIZED
Legacy-root cleanup/migration: NOT AUTHORIZED
Section 14 execution/runtime rerun: NOT AUTHORIZED
Tests/typecheck/build: NOT AUTHORIZED
Git stage/commit/push: NOT AUTHORIZED
Global Gate: HOLD

Current planning/review files staged/committed/pushed: no / no / no
Current six-file frontend implementation staged/committed/pushed: no / no / no
This handoff staged/committed/pushed: no / no / no
```

This handoff is created because the current PM window has reached the governance boundary explicitly
frozen before the latest Data Quality re-review. The next PM must not continue by conversational
momentum. The only currently eligible technical lane is a separately authorized Architecture /
Integration docs-only planning repair for `DQ-RUNTIME-OPTIONC-D7` and
`DQ-RUNTIME-OPTIONC-D8`, followed by an independent Data Quality re-review.

The previous PM handoff,
`docs/thread_handoff/chatgpt_pm_handoff_260713-1916.md`, predates Option C, the private-parent /
run-specific-root architecture, the manifest terminal-commit repairs, and the latest retained-record
Data Quality reviews. This file supersedes it for the current branch.

## 1. First action for the next PM: read-only recovery

The next PM must begin with read-only recovery. Do not edit files, run Section 14, run tests,
typecheck or build, create the private parent, touch the retained legacy root, start Next/capture,
bind ports, run curl/browser/lsof, connect to API/DB/Postgres/Docker, stage, commit or push before
this recovery.

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git status -sb

printf '\n--- log -12 ---\n'
git log --oneline -12

printf '\n--- HEAD ---\n'
git log -1 --format='%H %s'

printf '\n--- origin/main ---\n'
git rev-parse origin/main

printf '\n--- ahead/behind ---\n'
git rev-list --left-right --count HEAD...origin/main

printf '\n--- diff name-only ---\n'
git diff --name-only

printf '\n--- cached name-only ---\n'
git diff --cached --name-only

printf '\n--- current handoff ---\n'
git status --short -- \
  docs/thread_handoff/chatgpt_pm_handoff_260714-1450.md

printf '\n--- current Option C authority and latest gates ---\n'
git status --short -- \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_plan.md \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_private_root_update.md \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_manifest_repair.md \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_manifest_reliability_rereview.md \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_manifest_data_quality_review.md \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_data_quality_repair.md \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_data_quality_rereview.md \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_value_validation_repair.md \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_value_validation_data_quality_rereview.md

printf '\n--- proposed next repair and review targets ---\n'
for target in \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_failure_relation_repair.md \
  docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_failure_relation_data_quality_rereview.md
do
  if [ -e "$target" ] || [ -L "$target" ]; then
    printf 'PRESENT_OR_LINK %s\n' "$target"
  else
    printf 'ABSENT %s\n' "$target"
  fi
done

printf '\n--- private parent ---\n'
parent=/tmp/edge-mes-dashboard-url-runtime-evidence-runs
if [ -e "$parent" ] || [ -L "$parent" ]; then
  /bin/ls -ld "$parent"
  /usr/bin/stat -f '%N %HT dev=%d inode=%i uid=%u mode=%p' "$parent"
else
  printf 'ABSENT %s\n' "$parent"
fi

printf '\n--- legacy retained root aliases ---\n'
for root in \
  /tmp/edge-mes-dashboard-url-runtime-evidence \
  /private/tmp/edge-mes-dashboard-url-runtime-evidence
do
  if [ -e "$root" ] || [ -L "$root" ]; then
    /usr/bin/stat -f '%N %HT dev=%d inode=%i mode=%p' "$root"
  else
    printf 'ABSENT %s\n' "$root"
  fi
done

printf '\n--- generated and quarantine paths ---\n'
for path in \
  frontend/.next \
  frontend/next-env.d.ts \
  frontend/tsconfig.tsbuildinfo \
  frontend/.edge-mes-runtime-evidence-next.quarantine \
  frontend/.edge-mes-runtime-evidence-next-env.quarantine \
  frontend/.edge-mes-runtime-evidence-tsbuildinfo.quarantine
do
  if [ -e "$path" ] || [ -L "$path" ]; then
    printf 'PRESENT_OR_LINK %s\n' "$path"
  else
    printf 'ABSENT %s\n' "$path"
  fi
done
```

Expected committed baseline at handoff creation:

```text
branch:
main

HEAD == origin/main ==
e04ee45f87e1b4b57237a285f337ac8be4686df9

latest commit:
e04ee45 Add PM handoff after Dashboard URL validation closeout

ahead/behind:
0 0

cached diff:
empty
```

Expected handoff state before any future Git authorization:

```text
?? docs/thread_handoff/chatgpt_pm_handoff_260714-1450.md
```

Expected runtime filesystem state:

```text
ABSENT /tmp/edge-mes-dashboard-url-runtime-evidence-runs

PRESENT and unchanged:
/tmp/edge-mes-dashboard-url-runtime-evidence
/private/tmp/edge-mes-dashboard-url-runtime-evidence
same Directory object:
dev=16777234 inode=7372301 mode=40755

ABSENT frontend/.next
ABSENT frontend/next-env.d.ts
ABSENT frontend/tsconfig.tsbuildinfo
ABSENT frontend/.edge-mes-runtime-evidence-next.quarantine
ABSENT frontend/.edge-mes-runtime-evidence-next-env.quarantine
ABSENT frontend/.edge-mes-runtime-evidence-tsbuildinfo.quarantine
```

Known external dirty state does not itself create a recovery HOLD. Stop only if the committed
baseline, cached state, target prestate, private-parent state, legacy-root identity,
generated/quarantine state or task-specific authority differs materially.

Do not run pull, fetch, merge, rebase, reset, restore or clean during recovery.

## 2. Required authority reading order

The next PM must read in this order:

```text
docs/thread_handoff/pm_operating_rules.md
docs/thread_handoff/chatgpt_pm_handoff_260714-1450.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_plan.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_private_root_update.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_reliability_review.md
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_manifest_repair.md
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_manifest_reliability_rereview.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_manifest_data_quality_review.md
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_data_quality_repair.md
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_data_quality_rereview.md
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_value_validation_repair.md
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_value_validation_data_quality_rereview.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_root_identity_primitive_feasibility.md

docs/current_status.md
```

Use this authority order when documents conflict:

```text
live Git
→ this PM handoff
→ latest value-validation Data Quality re-review HOLD
→ current Section 14 executable literal
→ latest Architecture value-validation repair report
→ earlier Data Quality Option C reports
→ Reliability Option C PASS report
→ Architecture Option C/private-root reports
→ primitive feasibility report
→ earlier runtime-evidence reports
→ docs/current_status.md
```

`docs/current_status.md` does not contain the latest Option C review branch. Do not silently update
it. Durable status sync remains a separately authorized future task.

## 3. Live repository state at handoff creation

Read-only recovery at handoff creation confirmed:

```text
branch: main
HEAD: e04ee45f87e1b4b57237a285f337ac8be4686df9
origin/main: e04ee45f87e1b4b57237a285f337ac8be4686df9
ahead/behind: 0 0
cached diff: empty
```

Latest committed history remains headed by:

```text
e04ee45 Add PM handoff after Dashboard URL validation closeout
20b9446 Add PM handoff at Dashboard URL test HOLD
1ea41b7 Repair Dashboard ORIGIN_MALFORMED authority
bba8648 Re-review Dashboard resolver contract data quality
2483f2b Re-review Dashboard resolver contract reliability
6482e64 Add PM handoff after Dashboard resolver planning repair
d75c547 Repair Dashboard URL resolution resolver contract
7784e54 Record Dashboard URL resolution Verification HOLD
bb1935a Record Dashboard URL resolution Data Quality review
62e1424 Close Dashboard URL resolution Reliability planning review
f4c24ea Repair Dashboard production URL resolution planning
5922b4b Record Dashboard URL resolution Reliability HOLD
```

No current Option C planning/review document is staged, committed or pushed. No current six-file
frontend implementation change is staged, committed or pushed.

## 4. Known external dirty artifacts to preserve and exclude

Known external dirty state includes at least:

```text
M .gitignore

M frontend/src/app/accepted-events/__tests__/page.test.tsx
M frontend/src/app/accepted-events/page.tsx
M frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
M frontend/src/lib/acceptedStationEvents/apiClient.ts

?? frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
?? frontend/src/lib/acceptedStationEvents/apiOrigin.ts
?? frontend/node_modules/

?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
?? docs/thread_handoff/chatgpt_pm_handoff_260712-1349.md
?? docs/thread_handoff/chatgpt_pm_handoff_260713-1916.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? existing runtime-evidence reports listed in this handoff
```

These paths are not automatically authorized for edit, cleanup, staging or commit. A future task
must use an exact allowlist. The presence of these known dirty paths is not, by itself, a recovery
blocker.

## 5. Current six-file frontend implementation

Exact implementation set remains:

```text
M  frontend/src/app/accepted-events/__tests__/page.test.tsx
M  frontend/src/app/accepted-events/page.tsx
M  frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
M  frontend/src/lib/acceptedStationEvents/apiClient.ts
?? frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
?? frontend/src/lib/acceptedStationEvents/apiOrigin.ts
```

Current state:

```text
implementation completed: yes
implementation staged: no
implementation committed: no
implementation pushed: no
```

This implementation is outside the next eligible D7/D8 repair lane. Do not modify, run, stage or
commit it without a new exact authorization.

## 6. Frozen Option C architecture and threat boundary

The following decisions are frozen and must not be reopened during D7/D8 repair unless an explicit
new blocker proves a regression:

```text
Architecture direction:
private verified parent
+ unpredictable run-specific root
+ per-run manifest mapping
+ retained success/failure evidence

private parent:
/tmp/edge-mes-dashboard-url-runtime-evidence-runs
must be pre-created by a separate workspace-preparation gate
runtime does not create or adopt an unknown parent

run nonce:
randomBytes(32)
64 lowercase hex
one generation per run

run root:
<private-parent>/run-<nonce>
exclusive creation
root CWD object binding
evidence_root=.

manifest:
<private-parent>/run-<nonce>.manifest.json
all final/tmp I/O relative to verified private-parent CWD
31-key exact manifest mapping
ACTIVE / SUCCESS / FAILURE state model
publication uncertainty uses read-only reconciliation

filesystem threat boundary:
DEFENDS T1, T2 under owner/0700/non-privileged assumptions, and T3
DOES NOT CLAIM T4 deliberate same-UID malicious race
DOES NOT CLAIM T5 privileged/root manipulation
atomic mkdir/open proof: NOT_CLAIMED

legacy retained root:
outside Option C namespace
historical retained failure artifact
not adopted, migrated or cleaned
cleanup NOT AUTHORIZED
```

## 7. Reliability gate state

Current Reliability state:

```text
Architecture private-root update: PASS WITH RECOMMENDATIONS
Reliability Option C manifest re-review: PASS WITH RECOMMENDATIONS
Current Reliability blockers: none
```

Accepted findings:

```text
ARCH-RUNTIME-ROOT-1: ACCEPTED / CLOSED
REL-RUNTIME-ROOT-R1: ACCEPTED / CLOSED
REL-RUNTIME-ROOT-R2: ACCEPTED / CLOSED
REL-RUNTIME-ROOT-R3:
  RECLASSIFIED AS DOCUMENTED T4 NON-CLAIM
  ACCEPTED UNDER T1–T3 THREAT BOUNDARY
REL-RUNTIME-ROOT-R4: ACCEPTED / CLOSED
REL-RUNTIME-OPTIONC-R1: ACCEPTED / CLOSED
REL-RUNTIME-OPTIONC-R2: ACCEPTED / CLOSED
```

Preserved Reliability controls include:

```text
verified parent-CWD manifest I/O
disk manifest as source of truth
publication uncertainty reconciliation
confirmed SUCCESS → SUCCESS_COMMITTED → exit 0
signals cannot create SUCCESS + nonzero
UNKNOWN → no overwrite, no cleanup, no PASS, nonzero
FAILURE cannot overwrite SUCCESS
no fallible filesystem/process action after confirmed SUCCESS
TERM-only child cleanup
KILL == 0
wait rc 127 is never success
requestServerClose / server.close / joined waiter preserved
root/private-parent/manifest delete authority == 0
```

A future D7/D8 repair must preserve all of these controls.

## 8. Current Data Quality gate state

Latest independent Data Quality review:

```text
report:
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_value_validation_data_quality_rereview.md

conclusion:
HOLD
```

Finding state:

```text
DQ-RUNTIME-OPTIONC-D1:
ACCEPTED / CLOSED
pre-terminal summary remains READY_TO_COMMIT_SUCCESS and does not project terminal SUCCESS

DQ-RUNTIME-OPTIONC-D2:
HOLD / NOT ACCEPTED
retained failure/UNKNOWN join remains incomplete because D7/D8 are open

DQ-RUNTIME-OPTIONC-D3:
ACCEPTED / CLOSED
all HOLD branches use explicit root/manifest/parent/marker state and sentinels

DQ-RUNTIME-OPTIONC-D4:
RECOMMENDATION
retained-set global uniqueness and archive inventory remain separate

DQ-RUNTIME-OPTIONC-D5:
ACCEPTED / CLOSED
summary 57-field frozen-source lineage, freeze timing, raw equality and semantic relations accepted

DQ-RUNTIME-OPTIONC-D6:
HOLD / NOT ACCEPTED
failure-state frozen-source record still lacks complete source normalization and cross-field relations

DQ-RUNTIME-OPTIONC-D7:
BLOCKER / OPEN
illegal manifest_parent_fsync_result may be silently normalized to UNKNOWN

DQ-RUNTIME-OPTIONC-D8:
BLOCKER / OPEN
failure-state cross-field semantic relation matrix is incomplete

DQ-RUNTIME-OPTIONC-D9:
OBSERVATION
expected payload environment-variable size boundary is not explicitly proven

DQ-RUNTIME-D2-3:
CARRY FORWARD
pagination/aggregation semantics remain unproven

DQ-URL-D3:
CARRY FORWARD
real production-fact producer/DB/adapter/collector lineage remains unproven
```

## 9. D7 exact blocker

Current root cause:

```text
freeze_failure_state_values initializes:
failure_expected_manifest_parent_fsync_result=UNKNOWN

approved source values are copied through a case branch

unapproved/illegal source value uses a no-op default

therefore the preinitialized UNKNOWN survives

validator accepts UNKNOWN
```

This means an illegal source token can become a legal retained `UNKNOWN`, after which the writer
and validator can raw-equal the same sanitized payload. The record no longer distinguishes:

```text
approved unsupported/unknown telemetry
versus
illegal or corrupted source value
```

Required repair direction, subject to a new PM prompt:

```text
define the approved manifest_parent_fsync_result taxonomy
copy only approved values
fail closed on every unapproved value
if UNKNOWN is retained, define its exact approved origin and keep it distinguishable from illegal input
preserve NOT_CHECKED versus unsupported versus operational error semantics
```

Do not silently sanitize illegal input.

## 10. D8 exact blocker

The 76-field failure payload is now frozen, serialized once, raw-equal and read back. The remaining
problem is semantic rather than structural: mutually contradictory values can still be frozen into
one internally byte-stable record.

The missing or incomplete relation families include:

```text
manifest confirmed state
↔ confirmed digest
↔ publication result
↔ reconciliation state
↔ terminal commit state
↔ terminal disposition

cleanup result per role
↔ wait status per role
↔ role start/reaped state

port release result
↔ listener/lsof result
↔ process cleanup result

partial_build_retained
↔ six source/quarantine filesystem states

ownership handoff stage
↔ handoff results
↔ ownership verification
↔ delete stage
↔ postcondition result

fixture lineage result
↔ expected/post-request digest and byte availability

capture response evidence state
↔ response_error_seen
↔ response_completion_committed
↔ response_write_started
↔ capture_terminal_flag
↔ capture_last_state
```

Examples that must be rejected by a future repair include:

```text
illegal parent-fsync token normalized to UNKNOWN
cleanup success with wait rc 127 or nonzero
port recorded released while listener state remains unresolved
postcondition PASS while ownership handoff failed
fixture_lineage_result PASS with missing/mismatched digest or byte evidence
response complete while response_error_seen=true
capture ERROR state with success response flags
terminal disposition inconsistent with manifest state/reconciliation
```

The future Architecture repair must build a complete relation matrix and fail closed before
freezing/writing a contradictory payload.

## 11. D9 observation

The summary and failure expected payloads are transported through environment variables to Node
readback validators. Existing protections include:

```text
CR/LF rejection
fixed field count
single payload construction
raw byte equality
exec/env failure is fail closed
```

There is no explicit payload-size upper bound. Data Quality classified this as an observation, not
a current blocker. A future D7/D8 repair may carry it as a recommendation, but must not expand into
a broad transport redesign unless separately authorized.

## 12. Current report lineage

Current Option C authority/review lineage is untracked and unstaged:

```text
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_plan.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_private_root_update.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_reliability_review.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_manifest_repair.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_manifest_reliability_rereview.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_manifest_data_quality_review.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_data_quality_repair.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_data_quality_rereview.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_value_validation_repair.md

docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_option_c_value_validation_data_quality_rereview.md
```

Earlier root-identity, execution, Reliability and Data Quality reports also remain untracked. Do not
stage them by broad path or assume they are included in a future repair allowlist.

## 13. Current static facts

Latest Data Quality review and Architecture repair reported and PM intake confirmed:

```text
canonical Section 14 fence: 1
runtime_evidence_main definition/call: 1 / 1
planned build call: 1
manifest fields: 31
summary fields: 57
failure-state fields: 76
summary frozen assignments/serializer/validator: 57 / 57 / 57
failure frozen assignments/serializer/validator: 76 / 76 / 76
summary raw equality: present
failure raw equality: present
summary live-state recomputation after freeze: 0
failure writer/validator live-state recomputation: 0
failure freeze-time filesystem observations: 6
post-freeze mutation of those observed paths: 0
premature terminal SUCCESS wording: 0
root/private-parent/manifest delete authority: 0
KILL: 0
Section 14 zsh -n: PASS
runtime/tests/typecheck/build/process/port execution: none
```

These facts do not close D7/D8. Raw equality can faithfully retain a semantically invalid frozen
payload.

## 14. Next eligible lane

After the next PM performs recovery and intake, the only currently eligible technical lane is:

```text
Architecture / Integration
docs-only planning repair
exactly DQ-RUNTIME-OPTIONC-D7 and DQ-RUNTIME-OPTIONC-D8
```

Recommended sequence:

```text
1. Architecture / Integration D7/D8 planning repair
2. independent Data Quality focused re-review of D2/D6/D7/D8
3. only if Data Quality has no blocker:
   independent Verification focused review
4. private-parent workspace preparation remains a separate later gate
5. Section 14 execution/runtime rerun remains a separate later gate
6. Git stage/commit/push remains PM-only and separately authorized
```

The next PM may issue a new Architecture prompt only after confirming live recovery and the exact
repair target prestate. Do not authorize Verification in parallel with an open Data Quality HOLD.

## 15. Explicit non-authorized surfaces

Until a new PM authorization says otherwise, do not:

```text
modify frontend implementation or tests
run frontend tests/typecheck/build
run Section 14
create or prepare /tmp/edge-mes-dashboard-url-runtime-evidence-runs
create a new run-specific evidence root
write a manifest, summary or failure-state
modify, move, rename or delete the legacy retained root
run Next/capture/curl/browser/lsof or bind ports
connect to API/DB/Postgres or start Docker
change DB/API/Dashboard/V-PLC/Collector behavior
run deployment, rollback or real PLC work
stage, commit, push or tag
update docs/current_status.md or other governance docs
close DQ-RUNTIME-OPTIONC-D4, DQ-RUNTIME-D2-3 or DQ-URL-D3
```

## 16. Handoff file state and future Git rule

This handoff was created as the only file authorized by the PM handoff action:

```text
docs/thread_handoff/chatgpt_pm_handoff_260714-1450.md
```

It must remain unstaged until the user explicitly authorizes exact-path stage/commit/push.

A future handoff commit, if explicitly authorized, must stage only:

```text
docs/thread_handoff/chatgpt_pm_handoff_260714-1450.md
```

unless the user separately names another governance file. Do not stage `.gitignore`, old handoffs,
Option C reports, frontend implementation, `frontend/node_modules/`, broad `docs/` or any other
untracked/modified file.

Before committing, verify:

```bash
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

## 17. Copyable prompt for the next ChatGPT PM window

```markdown
# Edge MES Demo — ChatGPT PM Handoff Restore

你现在接手 Edge MES Demo 项目的 ChatGPT PM 角色。

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

第一优先级：恢复上下文和live repository state，不要直接授权repair、Verification、runtime或Git write。

请先读取并遵守：

    docs/thread_handoff/pm_operating_rules.md
    docs/thread_handoff/chatgpt_pm_handoff_260714-1450.md

## 1. 第一动作：read-only recovery

执行handoff第1节中的完整read-only recovery。

Expected baseline：

    HEAD == origin/main ==
    e04ee45f87e1b4b57237a285f337ac8be4686df9

    latest commit:
    e04ee45 Add PM handoff after Dashboard URL validation closeout

    ahead/behind:
    0 0

    cached:
    empty

Expected handoff：

    ?? docs/thread_handoff/chatgpt_pm_handoff_260714-1450.md

Expected runtime filesystem：

    private parent:
    ABSENT /tmp/edge-mes-dashboard-url-runtime-evidence-runs

    legacy root aliases:
    present, unchanged, same Directory object
    dev=16777234 inode=7372301 mode=40755

    generated/quarantine six paths:
    all ABSENT

Known external dirty state is allowed and must be preserved/excluded. Do not return HOLD merely
because `.gitignore`, the six-file frontend implementation, `frontend/node_modules/`, previous
handoffs or existing reports are dirty/untracked.

## 2. Current gate state

    Reliability:
    PASS WITH RECOMMENDATIONS
    no current blocker

    Data Quality:
    HOLD

    DQ-RUNTIME-OPTIONC-D1:
    ACCEPTED / CLOSED

    DQ-RUNTIME-OPTIONC-D2:
    HOLD / NOT ACCEPTED

    DQ-RUNTIME-OPTIONC-D3:
    ACCEPTED / CLOSED

    DQ-RUNTIME-OPTIONC-D4:
    RECOMMENDATION

    DQ-RUNTIME-OPTIONC-D5:
    ACCEPTED / CLOSED

    DQ-RUNTIME-OPTIONC-D6:
    HOLD / NOT ACCEPTED

    DQ-RUNTIME-OPTIONC-D7:
    BLOCKER / OPEN

    DQ-RUNTIME-OPTIONC-D8:
    BLOCKER / OPEN

    DQ-RUNTIME-OPTIONC-D9:
    OBSERVATION

    DQ-RUNTIME-D2-3:
    CARRY FORWARD

    DQ-URL-D3:
    CARRY FORWARD

    Verification:
    NOT AUTHORIZED

    private-parent preparation:
    NOT AUTHORIZED

    runtime rerun:
    NOT AUTHORIZED

    Git write:
    NOT AUTHORIZED

    Global Gate:
    HOLD

## 3. Required PM intake

恢复后完整读取handoff第2节列出的authority chain，重点核对：

    latest Data Quality re-review HOLD
    DQ-RUNTIME-OPTIONC-D7
    DQ-RUNTIME-OPTIONC-D8
    DQ-RUNTIME-OPTIONC-D9
    current Section 14 literal

D7：非法或未知的manifest_parent_fsync_result不能静默归一化成合法UNKNOWN。

D8：failure-state必须闭合manifest、terminal、cleanup/wait、port/listener、artifact和fixture/response跨字段关系。

D9仅为payload environment size observation，不得自动升级成广泛transport redesign。

## 4. Next decision

完成PM intake后，判断并在需要时签发一个新的Architecture / Integration docs-only repair Prompt，范围严格限制为：

    DQ-RUNTIME-OPTIONC-D7
    DQ-RUNTIME-OPTIONC-D8

不得同时授权：

    Verification
    private-parent preparation
    Section 14 execution/runtime
    tests/typecheck/build
    cleanup
    stage/commit/push

Architecture repair之后必须重新进行独立Data Quality focused re-review；只有Data Quality无blocker后才可考虑Verification。

开始时只做read-only recovery和PM intake，不要编辑或执行runtime。
```

## 18. Final handoff gate

```text
Handoff file created: yes
Handoff file staged: no
Handoff file committed: no
Handoff file pushed: no
Current Data Quality gate: HOLD
Current Global Gate: HOLD
Next PM first action: read-only recovery
Next eligible technical lane: Architecture D7/D8 docs-only planning repair, only after new PM authorization
```
