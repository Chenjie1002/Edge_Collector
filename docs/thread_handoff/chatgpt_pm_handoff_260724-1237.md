# Edge MES Demo — ChatGPT PM Handoff — 260724-1237

## 1. Handoff decision

This handoff is intentionally created at a clean project-management boundary:

- the current ChatGPT PM window is long;
- the Level 2 D2-R7A Collector package-closure slice is fully verified, committed and pushed;
- the next major branch, D2-R7B, has not started;
- deployment, Collector activation and D3 remain unauthorized.

The next ChatGPT PM must not infer authority from the previous conversation. It must perform fresh read-only recovery and issue a new, exact-scope task before any further work.

## 2. Project path and live repository baseline

Project root:

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

Handoff-time Git evidence:

```text
branch: main
HEAD: ddf55be6d1f33f37235789aa28dbdc441ec313a4
origin/main: ddf55be6d1f33f37235789aa28dbdc441ec313a4
ahead / behind: 0 / 0
cached set: empty
```

Latest commit:

```text
ddf55be6d1f33f37235789aa28dbdc441ec313a4
Close D2-R7A collector package closure gate
```

Previous baseline:

```text
58e6c7e042436f31e1512c64e3ab40a08d14bf27
Add PM handoff before D2-R7A verification
```

## 3. Current closed gate

Current authoritative conclusion:

```text
D2-R7A Collector package closure:
CLOSED / VERIFIED / COMMITTED / PUSHED
```

Supporting gate chain:

```text
D2-R7A implementation repair:
completed

D2-R7A-R1 initial Verification:
HOLD — broader regression blockers

D2-R7A-R2 diagnosis:
complete — no production runtime defect required

D2-R7A-R3A test execution boundary alignment:
PASS WITH RECOMMENDATIONS

D2-R7A-R3B Reliability test-double alignment:
PASS WITH RECOMMENDATIONS

D2-R7A-R4 independent Verification:
HOLD — explicit shell=False evidence mismatch

D2-R7A-R4A explicit shell contract repair:
PASS WITH RECOMMENDATIONS

D2-R7A-R4-R1 fresh independent Verification:
PASS

D2-R7A-C1 exact-path Git closeout:
PASS
```

Historical HOLD reports remain durable evidence of the diagnostic path. They are superseded as current blockers by the later repair and R4-R1 PASS.

## 4. D2-R7A committed paths

Commit `ddf55be6d1f33f37235789aa28dbdc441ec313a4` contains exactly these 14 paths:

```text
collector/Dockerfile
collector/tests/test_event_collector_reliability.py
collector/tests/test_snap7_reliability_integration.py
docker-compose.yml
docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
docs/reports/sprint4_d2_r7a_r1_collector_package_closure_verification.md
docs/reports/sprint4_d2_r7a_r2_regression_failure_diagnosis.md
docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md
docs/reports/sprint4_d2_r7a_r3b_collector_reliability_test_double_alignment.md
docs/reports/sprint4_d2_r7a_r4_collector_package_closure_reverification.md
docs/reports/sprint4_d2_r7a_r4_r1_collector_package_closure_reverification.md
docs/reports/sprint4_d2_r7a_r4a_explicit_shell_contract_repair.md
scripts/run_non_db_pytest.py
tests/test_collector_container_packaging.py
```

Commit stat:

```text
14 files changed
3777 insertions
14 deletions
```

Post-push evidence:

```text
HEAD == origin/main
ahead / behind == 0 / 0
cached set == empty
all 14 closeout paths clean
external dirty artifacts preserved
```

## 5. Reliable D2-R7A verification evidence

Fresh independent R4-R1 Verification established:

```text
Packaging regression:
2 passed

Focused station-event / adapter / line-config suite:
303 passed

Reliability target suite:
7 passed

Canonical non-DB aggregate:
PARTITION_EXIT_CODES=[0, 0, 0, 0]
AGGREGATE_EXIT_CODE=0
```

Aggregate partition evidence:

```text
Root/common:
316 passed

Collector:
81 passed, 7 deselected

API:
58 passed, 35 deselected

S7 PLC simulator:
27 passed

collection errors:
0 across all partitions
```

Runner contract evidence:

```text
one subprocess.run() call
explicit shell=False
command is a list
check=False
stdout/stderr passthrough
missing-root fail-closed
non-zero child exit propagates to aggregate exit
```

Container/package evidence:

```text
docker compose config: PASS
local validation image build: PASS
container app.main import: PASS
container app.services.event_collector import: PASS
container common.station_event import: PASS
container static mapping initialization: PASS
host static mapping initialization: PASS
host/container identity consistency: PASS
temporary validation image cleanup: PASS
```

Static mapping identity established by R4-R1:

```text
line_id: LINE_001
read-plan count: 4
runtime config hash:
0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
```

This evidence is local package/static-startup evidence only. It is not remote deployment, Collector activation, DB/API mutation, production data generation or D3 evidence.

## 6. Durable reports to read first

The next PM should treat these as the primary D2-R7A truth chain:

```text
docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
docs/reports/sprint4_d2_r7a_r1_collector_package_closure_verification.md
docs/reports/sprint4_d2_r7a_r2_regression_failure_diagnosis.md
docs/reports/sprint4_d2_r7a_r3a_test_execution_boundary_alignment.md
docs/reports/sprint4_d2_r7a_r3b_collector_reliability_test_double_alignment.md
docs/reports/sprint4_d2_r7a_r4_collector_package_closure_reverification.md
docs/reports/sprint4_d2_r7a_r4a_explicit_shell_contract_repair.md
docs/reports/sprint4_d2_r7a_r4_r1_collector_package_closure_reverification.md
```

Primary governance reference:

```text
docs/thread_handoff/pm_operating_rules.md
```

Important qualification: the working-tree copy of `pm_operating_rules.md` is externally dirty and was not included in D2-R7A closeout. The next PM must read it but must also inspect its Git diff and must not assume those unstaged changes are committed governance baseline.

## 7. Current working-tree state and external dirty artifacts

The D2-R7A committed paths are clean. The repository is not globally clean because substantial external/pre-existing artifacts remain.

Tracked modified paths visible at handoff time:

```text
.gitignore
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
```

These tracked modifications predate this handoff and were explicitly excluded from D2-R7A commit. Do not restore, clean, overwrite, stage or commit them without separate PM intake and exact-path authority.

Important untracked categories include:

```text
older ChatGPT PM handoff files
Sprint-3 and earlier Sprint-4 reports
frontend/.next/
frontend/node_modules/
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
other historical/local artifacts
```

The next PM must inspect live `git status`, not rely on this summary alone. No broad cleanup is authorized.

## 8. Governance/status synchronization debt

The current working-tree versions of:

```text
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
```

contain prior unstaged governance changes, including the data-first MVP direction and UI acceptance deferral. They do not yet provide a clean committed governance record of the newly closed D2-R7A baseline.

Current truth authority for D2-R7A is therefore:

```text
commit ddf55be6d1f33f37235789aa28dbdc441ec313a4
plus the committed R4-R1 Verification report
```

The next PM's first planning decision should be whether to open a separate, narrow governance/status reconciliation task before D2-R7B planning. That decision must be based on a read-only diff review and ownership analysis of the existing dirty files.

Do not casually append D2-R7A closure to those files inside another task. They may contain changes from previous windows that need their own exact-scope review and commit boundary.

## 9. Current next-gate status

```text
D2-R7A:
CLOSED

D2-R7B:
ELIGIBLE FOR PM PLANNING ONLY
NOT STARTED
NOT AUTHORIZED FOR IMPLEMENTATION

remote mapping deployment:
NOT AUTHORIZED until a new D2-R7B task is published

Collector deployment / activation:
NOT AUTHORIZED

production accepted-fact generation:
NOT AUTHORIZED

D3 controlled fresh-data reconciliation:
NOT AUTHORIZED

Git stage / commit / push:
NOT AUTHORIZED by this handoff
```

A PASS report or this handoff does not authorize any later phase automatically.

## 10. Recovered intended D2-R7B objective

The intended next gate recorded in the D2-R7A repair chain is:

```text
D2-R7B — deploy the exact HEAD config/mapping.yaml to the
remote read-only config mount source and verify its identity.

D2-R7B must not activate the Collector.
```

This is only a recovered intended objective, not a ready implementation prompt.

Before publishing D2-R7B, the next PM must recover and freeze at least:

- exact remote host and source path authority;
- exact target config mount source path;
- current remote file identity and backup/rollback boundary;
- exact HEAD mapping identity to deploy;
- whether remote mutation is currently safe and necessary;
- transport and privilege requirements;
- verification commands and identity fields;
- stop conditions;
- explicit prohibition on Collector activation or Compose lifecycle;
- whether Reliability, Data Quality and Verification reviews are required before mutation;
- exact report path and Git boundary.

Do not infer these details from old deployment attempts without fresh recovery.

## 11. Recommended sequence for the next PM

1. Perform fresh read-only Git recovery.
2. Verify this handoff against live `HEAD`, `origin/main`, recent log, cached set and working-tree artifacts.
3. Read the committed R4-R1 report and confirm D2-R7A is closed.
4. Inspect the diffs of `current_status.md`, `roadmap.md` and `pm_operating_rules.md` without modifying them.
5. Decide whether governance/status synchronization is a separate prerequisite gate or carry-forward debt.
6. Recover D2-R7B's exact objective, remote authority, prerequisites and rollback boundary.
7. Classify D2-R7B risk tier before publishing any task. Remote config mutation should be treated as Level 2 unless PM Rule and live evidence clearly justify otherwise.
8. Publish planning/diagnosis first if remote state or authority is uncertain.
9. Keep deployment separate from Collector activation.
10. Keep Collector activation separate from D3 controlled fresh-data reconciliation.
11. Do not enter Dashboard/browser evidence, OEE/Quality/Trace expansion or broad cleanup by momentum.

## 12. Non-authorized surfaces

The next PM and any new Thread must not assume authority for:

```text
source or test changes
Collector runtime wiring changes
DB schema or migration changes
DB writes or SQL mutation
API mutations
Dashboard/browser work
V-PLC or PLC control actions
remote SSH or Docker lifecycle
remote config copy/deployment
Collector start/restart/activation
rollback execution
fresh production data generation
production accepted-fact generation
D3 reconciliation
Git stage/commit/push/tag
status/roadmap/rules synchronization
broad cleanup
real PLC pilot work
```

Each surface requires a separately published task with exact allowlist, stop rules and review sequence.

## 13. Carry-forward invariants

The following project invariants remain active:

1. PLC/HMI remains the control authority; Edge remains non-invasive and observational.
2. Collector acceptance and persistence must complete before ACK/read_done mutation.
3. Same-payload retry must remain idempotent and must not create a second distinct accepted fact.
4. Diagnostic fields must not leak into production fact or bounded API truth.
5. Remote config deployment must use exact identity evidence and must not imply activation.
6. Collector deployment/activation requires separate authority and rollback planning.
7. D3 must use controlled fresh evidence and must not use SQL writes to manufacture production truth.
8. Dashboard/UI acceptance debt remains separate from the data-first mainline unless a later gate explicitly makes UI the deliverable.
9. Review-only Threads report HOLD on blockers and do not repair in the same Thread.
10. PASS does not imply commit, deploy, activation or next-gate authority.

## 14. Recommended first read-only action for the next PM

Run from the project root:

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git status -sb
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git log -8 --oneline --decorate
git diff --name-only
git diff --cached --name-only
git diff --check

git show --stat --oneline --decorate \
  ddf55be6d1f33f37235789aa28dbdc441ec313a4

git status --short -- \
  docs/current_status.md \
  docs/roadmap.md \
  docs/thread_handoff/pm_operating_rules.md \
  docs/thread_handoff/chatgpt_pm_handoff_260724-1237.md
```

Expected baseline at handoff creation:

```text
HEAD == origin/main == ddf55be6d1f33f37235789aa28dbdc441ec313a4
ahead / behind == 0 / 0
cached set == empty
handoff file == untracked / unstaged
```

If the live repository differs, the next PM must use live evidence and explain the drift before issuing any task.

## 15. Copyable prompt for the next ChatGPT PM window

```text
You are the new ChatGPT PM for the Edge MES Demo project.

Project path:
/Users/chenjie/Documents/MES/edge-mes-demo

First read:
1. docs/thread_handoff/pm_operating_rules.md
2. docs/thread_handoff/chatgpt_pm_handoff_260724-1237.md
3. docs/reports/sprint4_d2_r7a_r4_r1_collector_package_closure_reverification.md
4. docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
5. docs/current_status.md
6. docs/roadmap.md

Before making any decision, perform read-only recovery:
- git status -sb
- git rev-parse HEAD
- git rev-parse origin/main
- git rev-list --left-right --count HEAD...origin/main
- git log -8 --oneline --decorate
- git diff --name-only
- git diff --cached --name-only
- git diff --check

Expected committed baseline at handoff time:
HEAD == origin/main == ddf55be6d1f33f37235789aa28dbdc441ec313a4
ahead/behind == 0/0
cached set == empty
latest commit subject == Close D2-R7A collector package closure gate

Current project truth:
- D2-R7A Collector package closure is CLOSED / VERIFIED / COMMITTED / PUSHED.
- D2-R7A-R4-R1 is PASS.
- D2-R7B is eligible for PM planning only and is not authorized for implementation.
- Intended D2-R7B objective is exact-HEAD config/mapping.yaml deployment to the remote read-only config mount source, with identity verification and no Collector activation.
- Collector deployment/activation, production data generation and D3 remain unauthorized.

Important working-tree boundary:
- .gitignore, docs/current_status.md, docs/roadmap.md and docs/thread_handoff/pm_operating_rules.md are externally dirty and were not included in D2-R7A closeout.
- Many historical reports/handoffs and frontend generated artifacts remain untracked.
- Do not clean, restore, overwrite, stage or commit these without separate exact-path authority.

Your first PM decision after recovery:
1. determine whether a separate governance/status reconciliation task is needed before D2-R7B planning;
2. recover D2-R7B exact remote authority, target path, current remote state, identity, rollback boundary and review requirements;
3. publish planning/diagnosis first if any remote fact is uncertain.

Do not infer authority from the previous chat. Do not deploy config, activate Collector, access DB/API/V-PLC/PLC, generate production data, enter D3, modify governance files or perform Git mutation until a new exact-scope task and explicit authorization are issued.
```

## 16. Handoff file and commit boundary

Handoff file created by this workflow:

```text
docs/thread_handoff/chatgpt_pm_handoff_260724-1237.md
```

Creation timestamp convention:

```text
260724-1237
China Standard Time / UTC+8
```

This handoff must remain untracked and unstaged until the user explicitly authorizes exact-path stage/commit/push.

If later authorized, the commit must contain only this new handoff file unless the user separately authorizes another exact path. Existing dirty governance files must not be included by implication.

Suggested commit subject:

```text
Add PM handoff after D2-R7A closeout
```

This handoff itself does not authorize D2-R7B, deployment, activation, D3 or any other project mutation.
