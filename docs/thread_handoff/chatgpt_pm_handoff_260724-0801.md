# Edge MES Demo — ChatGPT PM Handoff — 260724-0801

## 1. Handoff decision

```text
PM handoff: REQUIRED NOW
Current PM window continue: NO
Reason: long Level-2 deployment/diagnostic chain, role-boundary correction, and a clean pre-Verification handoff point
```

This handoff is created before publishing the next Codex task. The current PM window must not publish or execute D2-R7A-R1 after this file is created.

The next ChatGPT PM must perform read-only recovery first and must not infer any implementation, review, deployment, rollback, Git, DB/API/V-PLC or later-gate authority from this handoff.

## 2. Project and live repository baseline

```text
Project path:
/Users/chenjie/Documents/MES/edge-mes-demo

Branch:
main

Live HEAD:
9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148

Live origin/main:
9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148

Ahead / behind:
0 / 0

Cached/staged:
empty

Latest commit:
9e0aba2 Add PM handoff after runtime planning closeout
```

Recent commits:

```text
9e0aba2 Add PM handoff after runtime planning closeout
c4b9bcd Sync Gate B runtime deployment planning status
b41e1ab Close Gate B runtime deployment planning gates
a21b90a Update PM recommendation scope and handoff
29f0259 Add PM handoff after Gate B closeout
7857be1 Sync Gate B Dashboard Docker integration status
8ddba3b Add Dashboard Raspberry Pi Docker integration
683a8a0 Add PM handoff after Gate A closeout
```

No Sprint-4 D1/D2 implementation, report or deployment work in the current chain has been staged, committed or pushed.

## 3. Current MVP objective

The approved MVP path remains data-first:

```text
PLC / V-PLC event truth
-> Collector acceptance and persistence
-> production_accepted_station_event_fact
-> bounded APIs
-> OEE / Quality / Trace data semantics
-> final UI integration later
```

Dashboard/browser acceptance remains deferred, visible debt. It is not a blocker for the current Collector/DB/API data path, and the old Attempt-3 browser-evidence chain must not be reopened.

## 4. Current working-tree state

### D2-R7A exact implementation/report paths

```text
M  collector/Dockerfile
M  docker-compose.yml
?? tests/test_collector_container_packaging.py
?? docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
```

These four paths are the only D2-R7A implementation/report artifacts. They are unstaged and uncommitted.

### Pre-existing tracked dirty governance artifacts

```text
M .gitignore
M docs/current_status.md
M docs/roadmap.md
M docs/thread_handoff/pm_operating_rules.md
```

These are pre-existing external dirty artifacts. They are not part of D2-R7A or its next Verification gate. Do not restore, edit, stage or bundle them without a separate exact PM authority.

### Other external untracked artifacts

The tree contains many pre-existing untracked Sprint-3/Sprint-4 reports, old handoffs, Keynote/report files and frontend generated artifacts, including:

```text
docs/reports/** unrelated to the exact current gate
docs/thread_handoff/chatgpt_pm_handoff_*.md existing historical files
frontend/.next/
frontend/node_modules/
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
```

Do not use broad `git add`, `git clean`, restore or repository cleanup.

## 5. Durable status caveat

`docs/current_status.md`, `docs/roadmap.md` and the latest committed handoff predate most of the Sprint-4 D1/D2 chain. Current Sprint-4 gate truth must be recovered from live Git plus the exact reports listed below.

The existing dirty governance files must not be silently treated as an authorized status-sync task. Status/governance sync remains pending unless a later PM explicitly authorizes an exact-path Level-0 task.

## 6. Sprint-4 D1/D2 gate lineage

### D1-R2 — existing accepted fact reconciliation

Report:

`docs/reports/sprint4_d1_r2_existing_accepted_production_fact_db_api_reconciliation.md`

Terminal:

```text
HOLD / NO_PREEXISTING_ELIGIBLE_ACCEPTED_RESULT
```

No eligible accepted production result existed in the inspected DB scope. Controlled fresh-data evidence remains a later objective, not yet authorized.

### D2 initial through D2-R2

The first deployment attempts were blocked by command/transport/integrity issues. No valid deployment PASS was established.

### D2-R3 — new image build with incomplete outer terminal

Report:

`docs/reports/sprint4_d2_r3_direct_dd_collector_accepted_fact_deployment.md`

New image successfully built:

```text
sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
linux / arm64 / v8
size: 174329249
```

Terminal:

```text
HOLD / EXECUTION_CONTRACT_VIOLATION / SSH2_TERMINAL_INCOMPLETE
```

### D2-R4 — post-mutation state recovery

Report:

`docs/reports/sprint4_d2_r4_post_mutation_collector_live_state_recovery.md`

Thread-local terminal:

```text
HOLD / COLLECTOR_RECREATE_PARTIAL_STATE
```

PM operational classification:

```text
SAFE_OLD_COLLECTOR_ACTIVE / NEW_IMAGE_READY
```

### D2-R5 — existing-image activation and rollback

Report:

`docs/reports/sprint4_d2_r5_existing_image_collector_activation.md`

Terminal:

```text
HOLD / ACTIVATION_VALIDATION_FAILED / ROLLED_BACK
```

The new image was activated once. The new Collector was observed as:

```text
Container ID:
92521519e2ef2d9123834a19d4677888c2b37b9b0d017629aad1d21ea1d36af9

Image:
sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c

Status / RestartCount:
running / 3
```

The gate correctly failed and performed the one authorized rollback.

### Current safe remote Collector after D2-R5 rollback

```text
Container:
edge-mes-collector

Container ID:
5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524

Image:
sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a

Config.Image:
edge-mes-demo-collector

Compose project/service:
edge-mes-demo / collector

Created:
2026-07-23T12:23:25.124184859Z

StartedAt:
2026-07-23T12:23:25.959624Z

Status / RestartCount:
running / 0

Active tag:
edge-mes-demo-collector -> sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
```

No later task has authority to assume this state is still live without a new read-only check.

### Frozen protected service identities from the last remote evidence

```text
PostgreSQL:
ID bb3ba0738e692c68b14a62ca64296e484990d3b86b1f6d395c27b200af5cb890
Image sha256:f961d097a9cedd37779baef1aab3fe87ef1c63b3b34d361f90a98ea5c9b77e56
Project/service edge-mes-demo / postgres
Status/restart running / 0

API:
ID 12e841b4ac33a75c835cee81f0df46e4dbcdb9382b50ca50523f5fad02c57058
Image sha256:9f03f370b37fd5fd2ddfd4e4e9e64d4c6b60312910e731157888544371683c11
Project/service edge-mes-demo / api
Status/restart running / 0

S7 PLC simulator:
ID d21e950b98ae87bbd3ee321074100d0b54b174235ce46df34c5100e1130b785f
Image sha256:3a28ae38c623d8cb80f775f954315e633b1108112082c37ece698c7562522238
Project/service edge-mes-demo / s7-plc-sim
Status/restart running / 0

Simulator:
ID 3ebe1e4725af577ac477594afe3046f7e5a197b8162f503ebac036d09b4fcfd5
Image sha256:08448d2876c30e9cbbecda4f0ca9a27a5e085a33f14dab2a6d2be3dd06430430
Project/service edge-mes-demo / simulator
Status/restart running / 0
```

Protected-service `Config.Image` is diagnostic-only unless a task explicitly freezes it. Do not repeat the D2-R6 assertion defect by treating it as a hard equality field.

### D2-R6 — first static diagnostic attempt

Report:

`docs/reports/sprint4_d2_r6_new_collector_remote_config_compatibility_diagnostic.md`

Terminal:

```text
HOLD / EXECUTION_CONTRACT_VIOLATION / LOCAL_PRESTATE_ASSERTION_DEFECT
```

The script incorrectly compared PostgreSQL `Config.Image=postgres:16` against an unfrozen value. No mapping or disposable-container diagnostic ran.

### D2-R6-R1 — corrected static diagnostic

Report:

`docs/reports/sprint4_d2_r6_r1_new_collector_remote_config_static_compatibility_retry.md`

Terminal:

```text
HOLD / NEW_IMAGE_STATIC_STARTUP_FAILED / IMPORT_PREREQUISITE_FAILED
```

Evidence:

```text
Remote mapping:
/opt/edge-mes-demo/config/mapping.yaml
5935 bytes
SHA-256 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3
classification: PHASE1_CONFIG_MATCH

New image source hashes:
MATCHED

First import failure:
ModuleNotFoundError: No module named 'common'
```

The import failed before mapping load or resolved-config construction. Therefore D2-R6-R1 did not prove that the remote mapping caused the D2-R5 restart loop.

## 7. Confirmed independent defects

### Defect A — Collector image package closure

`collector/app/services/station_event_adapter.py` imports:

```python
from common.station_event import ...
```

Before D2-R7A:

```text
Compose build context: ./collector
Dockerfile copied only collector/app as /app/app
Repository-root common/ was outside the build context
```

The built image therefore could not import `common.station_event`.

### Defect B — remote Phase-1 mapping contract drift

The remote mapping exactly matches the known Phase-1 mapping identity and lacks current runtime-mapping required fields such as:

```text
schema_version
config_version
authoritative_source
hash_algorithm
plc_identity_namespace
decoder_registry
runtime_defaults
```

Classification:

```text
PHASE1_CONFIG_MATCH
INCOMPATIBLE_WITH_CURRENT_RUNTIME_MAPPING_CONTRACT
```

Do not claim that this mapping caused the D2-R5 restart loop until the image package-closure repair is independently validated and the configuration path is tested in a later authorized gate.

## 8. D2-R7A Architecture / Integration implementation

Task:

```text
Data-first Gate D2-R7A — Repair the Collector Image Package Closure and Add a Container Regression Gate
```

Executing Thread:

```text
Architecture / Integration
```

Report:

`docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md`

Current terminal:

```text
HOLD / IMPLEMENTATION_TEST_FAILED
and
HOLD / LOCAL_CONTAINER_PACKAGE_VALIDATION_FAILED
```

### Exact implementation

`docker-compose.yml` now uses repository-root build context:

```yaml
collector:
  build:
    context: .
    dockerfile: collector/Dockerfile
```

`collector/Dockerfile` now materializes the runtime package closure:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY collector/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY collector/app ./app
COPY common ./common

CMD ["python", "-m", "app.main"]
```

New regression test:

`tests/test_collector_container_packaging.py`

The test structurally verifies the Compose build object and the required Dockerfile COPY lines.

### Evidence already obtained

```text
Packaging regression red gate:
2 failed as expected before implementation

Packaging regression green gate:
2 passed

Docker Compose render:
PASS
```

### Why D2-R7A remained HOLD

Focused and broader pytest were run without the project's required import environment and failed collection with:

```text
ModuleNotFoundError: No module named 'app'
```

The correct project test environment is:

```text
PYTHONPATH=collector:.
Python executable: .venv/bin/python
```

The local Docker daemon was unavailable at D2-R7A execution time, so image build and isolated container validation did not run.

The source diff has since been PM-reviewed as scope-correct. Do not rerun D2-R7A or modify these files merely because its environment-dependent verification was incomplete.

## 9. Local Docker prerequisite is now available

Colima was installed and verified after D2-R7A:

```text
Colima version:
0.10.3

Runtime:
docker

VM:
macOS Virtualization.Framework

Current Docker context:
colima

Docker endpoint:
unix:///Users/chenjie/.colima/default/docker.sock

Docker client:
29.6.1

Docker server:
29.5.2

Server OS:
Ubuntu 24.04.4 LTS

Architecture:
aarch64

CPU / memory:
4 CPU / approximately 8 GB

Storage driver:
overlayfs
```

Fresh handoff-time `docker info` returned successfully.

The next task must still perform its own Docker preflight; this handoff is not substitute runtime evidence.

## 10. Thread-role correction

PM Rule defines four independent core Threads:

```text
Architecture / Integration
Reliability
Data Quality
Verification
```

Do not use a mixed label such as `Architecture / Verification`.

D2-R7A implementation was completed by Architecture / Integration. The next gate must be assigned to a new independent Verification Thread and must be review/validation-only.

If Verification finds a valid blocker, it reports HOLD. PM then decides whether a separately authorized Architecture / Integration repair is necessary. Verification must not repair the implementation in the same Thread.

## 11. Current gate and authorization boundary

```text
Current gate:
D2-R7A HOLD pending independent local validation

D2-R7A-R1:
NOT YET PUBLISHED at handoff time

D2-R7B remote mapping deployment:
NOT ELIGIBLE

Collector reactivation:
NOT AUTHORIZED

D3 controlled fresh-data and DB/API reconciliation:
NOT ELIGIBLE

Git stage/commit/push:
NOT AUTHORIZED
```

No later phase becomes authorized from a PASS report alone.

## 12. Recommended sequence for the next PM

1. Perform read-only recovery from live Git and verify this handoff against the working tree.
2. Confirm the four D2-R7A paths remain the only current implementation/report artifacts.
3. Confirm staged set remains empty and external dirty artifacts remain excluded.
4. Re-run a read-only Colima/Docker preflight.
5. Classify D2-R7A-R1 as an independent Verification-only task and publish it to a new Verification Thread.
6. The Verification task must not modify source, tests, Dockerfile, Compose, config or reports other than its own new report.
7. Intake the Verification result before deciding any next action.
8. If Verification passes, do not automatically deploy or commit. Reassess Level-2 review obligations and explicitly decide whether focused Reliability/Data Quality review is necessary before exact Git closeout.
9. Only after all required review gates close may PM request explicit exact-path stage/commit/push authorization.
10. D2-R7B remains a separate remote config-deployment gate and must not activate Collector.
11. Collector activation remains a later independent authority with explicit rollback.
12. D3 remains later and must use controlled fresh production evidence without SQL writes.

## 13. D2-R7A-R1 intended Verification scope

The next PM should publish a compact, complete prompt with this identity:

```text
Report:
Sprint 4 D2-R7A-R1 Collector Package-closure Verification

Task:
Data-first Gate D2-R7A-R1 — Independently Verify the Existing Collector Package-closure Repair

Executing Thread:
new independent Verification Thread
```

Required PM workload assessment in the task prompt:

```text
Task size: medium
Scope: local tests, Compose render, one temporary local image, isolated import and HEAD-mapping static validation
Current Thread continue: no
New Thread required: yes
Reason: Architecture / Integration completed implementation; independent Verification must validate without inherited edit authority
```

Verification must use:

```text
PYTHONPATH=collector:.
.venv/bin/python -m pytest ...
```

It should validate, without edits:

```text
packaging regression
focused station-event/adapter/line-config tests
broader non-DB tests
Docker Compose render
one local validation image build
common.station_event import closure
current HEAD mapping static initialization
temporary image tag cleanup
exact allowlist and Git audit
```

Expected current HEAD mapping identity:

```text
config/mapping.yaml bytes:
7112

SHA-256:
d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d

schema_version:
runtime-mapping/v1

config_version:
2026.06.26-slice-a

runtime config hash:
0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38

station count:
3
```

Verification prohibitions:

```text
no source/test/Dockerfile/Compose/config edits
no dependency installation
no SSH or remote Docker
no DB/API/V-PLC
no remote config deployment
no Collector activation
no stage/commit/push/tag
no Dashboard or D3
```

## 14. Carry-forward recommendations

Current-gate necessary:

```text
Independent D2-R7A-R1 Verification using correct PYTHONPATH and working Colima daemon
```

Carry-forward after Verification PASS:

```text
PM reassessment of Level-2 focused review obligations before Git closeout
Separate D2-R7B exact HEAD mapping deployment, with no Collector activation
Separate later Collector activation/rollback gate
Separate later D3 controlled fresh-data reconciliation
```

Not current-gate work:

```text
Dashboard/browser evidence
OEE/Quality/Trace expansion
pagination or Case A/B/C expansion
status/governance sync
broad cleanup
```

## 15. Non-authorized surfaces

The next PM and next Verification Thread must not assume authority for:

```text
source or config repair
runtime Collector wiring changes
DB schema or DB writes
API changes
V-PLC/PLC actions
remote SSH or Docker lifecycle
remote config copy/deployment
Collector activation or rollback
fresh production data generation
Dashboard/browser work
OEE/Quality/Trace expansion
Git stage/commit/push/tag
status/rules/roadmap synchronization
real PLC pilot work
```

## 16. Recommended first read-only action for the next PM

Run from:

`/Users/chenjie/Documents/MES/edge-mes-demo`

```bash
git status -sb
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git log -8 --oneline --decorate
git diff --name-only
git diff --cached --name-only
git diff --check

git status --short -- \
  collector/Dockerfile \
  docker-compose.yml \
  tests/test_collector_container_packaging.py \
  docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md

docker context ls
docker info --format 'SERVER={{.ServerVersion}} OS={{.OperatingSystem}} ARCH={{.Architecture}} CPUS={{.NCPU}} MEM={{.MemTotal}}'
```

Then read, in order:

```text
docs/thread_handoff/pm_operating_rules.md
docs/thread_handoff/chatgpt_pm_handoff_260724-0801.md
docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
docs/reports/sprint4_d2_r6_r1_new_collector_remote_config_static_compatibility_retry.md
docs/reports/sprint4_d2_r5_existing_image_collector_activation.md
docs/reports/sprint4_d2_r4_post_mutation_collector_live_state_recovery.md
collector/Dockerfile
docker-compose.yml
tests/test_collector_container_packaging.py
config/mapping.yaml
```

If live Git or task paths differ from this handoff, stop and classify the discrepancy before publishing the next task.

## 17. Copyable prompt for the next ChatGPT PM window

```text
You are the next ChatGPT PM for Edge MES Demo.

Project path:
/Users/chenjie/Documents/MES/edge-mes-demo

First read:
- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260724-0801.md

Before issuing any Codex task, perform read-only recovery:
- git status -sb
- git rev-parse HEAD
- git rev-parse origin/main
- git rev-list --left-right --count HEAD...origin/main
- git log -8 --oneline --decorate
- git diff --name-only
- git diff --cached --name-only
- git diff --check
- inspect exact D2-R7A paths
- docker context ls
- docker info

Expected baseline at handoff:
HEAD == origin/main == 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead/behind 0/0
staged empty

Expected D2-R7A artifacts:
M collector/Dockerfile
M docker-compose.yml
?? tests/test_collector_container_packaging.py
?? docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md

Colima Docker daemon was verified available at handoff. Recheck it; do not assume.

Current gate:
D2-R7A Architecture / Integration implementation is HOLD only because independent environment-correct validation is incomplete. Do not rerun D2-R7A and do not modify its four paths.

Next recommended task, not yet published:
D2-R7A-R1 — Independently Verify the Existing Collector Package-closure Repair
Executing Thread: a new independent Verification Thread only.

The Verification task must be read-only except for its own new report. It must use PYTHONPATH=collector:. and .venv/bin/python, validate packaging regression, focused/broader non-DB tests, Compose render, one local image build, common.station_event import closure and HEAD mapping static initialization. It must not modify source/tests/Dockerfile/Compose/config, use SSH, deploy remote config, activate Collector, access DB/API/V-PLC, stage/commit/push, or enter D2-R7B/D3.

Do not mix Architecture and Verification in one Thread. If Verification reports a blocker, intake it and separately decide whether Architecture repair is necessary.

After any Verification PASS, do not automatically commit or deploy. Reassess Level-2 review obligations and request explicit exact-path Git authorization only after required reviews close.
```

## 18. Handoff file and Git boundary

```text
Handoff file:
docs/thread_handoff/chatgpt_pm_handoff_260724-0801.md

Created using UTC+8 timestamp:
2026-07-24 08:01 +0800

Staging:
NOT AUTHORIZED / NOT PERFORMED

Commit:
NOT AUTHORIZED / NOT PERFORMED

Push:
NOT AUTHORIZED / NOT PERFORMED
```

Do not stage this handoff automatically. If the user later authorizes Git closeout, PM must use an exact path allowlist and exclude all D2-R7A implementation paths and external dirty artifacts unless those paths are separately and explicitly authorized.
