# Edge MES Demo — ChatGPT PM Handoff — 2026-07-29 14:17 CST

## 1. Handoff identity and purpose

```text
handoff path:
docs/thread_handoff/chatgpt_pm_handoff_260729-1417.md

created at:
2026-07-29 14:17 CST / UTC+8

project:
Edge MES Demo

project absolute path:
/Users/chenjie/Documents/MES/edge-mes-demo

handoff reason:
The current ChatGPT PM window has accumulated multiple remote task prompts,
durable intakes, superseded HOLD classifications, false-blocker invalidations
and a scope reset. The next MVP action is a remote image deployment/activation
mutation gate and must start from a fresh PM window with a shorter authority
boundary.
```

This handoff supersedes the previous ChatGPT PM window as conversational authority. It does not
supersede live repository or remote facts. A new PM must perform fresh read-only recovery before
issuing any implementation, image, remote, restart, activation, rollback or Git authority.

The handoff does not authorize the next mutation. It records the current authoritative state and
the smallest recommended next planning direction.

## 2. Fresh live recovery at handoff creation

The following local facts were observed immediately before creating this handoff:

```text
checkout:
/Users/chenjie/Documents/MES/edge-mes-demo

branch:
main

HEAD:
1fac3ee567f1108e5a18b155e4133e1fecd50246

origin/main:
1fac3ee567f1108e5a18b155e4133e1fecd50246

HEAD parent:
63d3cc70e787e0c837079aec0f5924dcbfa6a668

ahead / behind:
0 / 0

cached index:
empty

initial untracked count before this handoff:
13796

initial sorted NUL-delimited untracked-path SHA-256:
dc87f9e35398bb3f67d316c98f6807eff2ce79e814396ea73a166a0d7fcb3d92
```

Tracked dirty paths were exactly:

```text
.gitignore
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
docs/thread_handoff/pm_operating_rules.md
```

These six paths predate this handoff and are not modified by the handoff task. They remain
excluded from any future exact-path stage/commit authority unless the user separately names them.

After creating this one exact handoff file, the final untracked path state was:

```text
final untracked count:
13797

final sorted NUL-delimited untracked-path SHA-256:
2e6293eccf1e20005f6b8f87d3b716b71bfbbcddab6adc6b78d5923267984170

new path introduced by this handoff:
docs/thread_handoff/chatgpt_pm_handoff_260729-1417.md
```

The aggregate untracked digest is recorded as an observation only. It must not be precomputed as a
future PASS/HOLD blocker. Future tasks should prove allowlist compliance by subtracting their exact
authorized output paths and confirming that the remaining baseline set is unchanged.

## 3. Latest committed baseline and durable governance status

Latest commit:

```text
1fac3ee Add PM handoff after R30 reliability cleanup holds
```

It contains only:

```text
docs/thread_handoff/chatgpt_pm_handoff_260728-2152.md
```

The previous committed project/status closeout is:

```text
63d3cc7 Close D2-R7B R29 observation and cleanup documentation
```

`docs/current_status.md` and `docs/roadmap.md` are committed durable controls through the R29
closeout. They do not contain the later uncommitted R30-I1-R8/R9 config-deployment acceptance or
the R10 lifecycle-observer chain.

Current identities:

```text
docs/current_status.md:
145805 bytes
978a755a3d68bdd003832a84f9528f09326cc4543ed22df63b3182403b4ce115

docs/roadmap.md:
9595 bytes
30d7e648436baef80ec866c9adbd600bc338677ede82142f14be4c7c3eb717b0
```

No status/roadmap sync is authorized by this handoff. For the R30 state, live facts and the exact
accepted reports listed below are authoritative.

## 4. Current local source and config baseline

Current committed/runtime-relevant file identities:

```text
collector/Dockerfile:
218 bytes
e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839

docker-compose.yml:
5698 bytes
c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66

config/mapping.yaml:
7112 bytes
d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d

mapping Git blob:
b46a637f23c761d0a4c3fe048b3b7480a3dec2ce

mapping relative to HEAD:
clean
```

Mapping contract:

```text
schema_version:
runtime-mapping/v1

config_version:
2026.06.26-slice-a

line_id:
LINE_001

stations:
WS01, WS02, WS03

expected read-plan count:
4

expected resolved runtime config hash:
0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
```

The P2-R2/P2-R3 package evidence remains locally present with the accepted identities recorded in
the previous handoff and R8/R9 reports. Scoped cache under those two evidence trees was most
recently observed as zero `__pycache__` and zero `*.pyc`.

Do not use repository-wide or `collector/**` development cache as a lifecycle/deployment blocker.
Do not clean cache without separate exact ownership and cleanup authority.

## 5. Collector package-closure and image truth boundary

### 5.1 Package-closure implementation is committed

The package-closure implementation is included in committed history through:

```text
ddf55be Close D2-R7A collector package closure gate
```

The independent package-closure re-verification report is:

```text
path:
docs/reports/sprint4_d2_r7a_r4_r1_collector_package_closure_reverification.md

bytes:
16293

SHA-256:
aebf3c38a366e5ef4d1abcbccffba03b9245fc8da026b4bc45278cd5b50451d5

conclusion:
PASS
```

It established local package closure, non-DB regression, Compose render, temporary validation-image
build, container import closure and static mapping initialization.

The temporary validation image was:

```text
sha256:6e064bdc89b39afa1223aca9fbcd18add8c0cb9d0070bce6f227eb1581bba905
```

That validation image/tag was deliberately deleted by its owning Verification task. It is not a
current deployable image identity and must not be referenced as if it still exists.

### 5.2 Historical remote image `7b942...` is known bad and must not be activated

Historical remote image:

```text
sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
```

Relevant report:

```text
path:
docs/reports/sprint4_d2_r6_r1_new_collector_remote_config_static_compatibility_retry.md

bytes:
19443

SHA-256:
4b0942a624de4ec8bb9e2f360484e6c35165bf14136eb628c7927d66b9bcec86
```

That image matched the then-frozen new source hashes but failed static startup before mapping
validation:

```text
ModuleNotFoundError: No module named 'common'
```

It predates the committed package-closure fix. It is not the package-closed activation candidate.
A future PM must explicitly mark it:

```text
HISTORICAL KNOWN-BAD IMAGE
DO NOT ACTIVATE
DO NOT RETAG AS THE CURRENT COLLECTOR
```

Its continued remote existence was historical evidence only. A new PM must re-observe image
presence if that fact is relevant, but must not treat presence as eligibility.

### 5.3 A fresh deployable package-closed image identity does not yet exist

The next MVP gate must create or otherwise materialize a fresh package-closed image from the
current committed Dockerfile/source and establish a new exact image ID before activation.

The handoff does not decide whether the smallest safe mechanism is:

- local arm64 image build plus bounded transport/load;
- a bounded remote build from an exact materialized source package;
- another explicitly reviewed deployment mechanism.

That choice must be made in a new, shorter Architecture / Integration planning task. It must not
reuse the known-bad `7b942...` image.

## 6. Exact config-deployment state

### 6.1 R30-I1-R8 accepted config deployment

Report:

```text
path:
docs/reports/sprint4_d2_r7b_i1_r30_i1_r8_one_shot_exact_config_only_remote_execution.md

bytes:
8429

SHA-256:
0c1cc78b0a24c9e80ef3ac4538efa8391ff501154b9d18439fa01004679da0ff
```

Accepted PM state:

```text
CONFIG_DEPLOYMENT_PASS
CONFIG_DEPLOYED_IDENTITY_VERIFIED
EXECUTED
REMOTE_STATE_OBSERVED
WRITTEN
PM-VERIFIED
PM-ACCEPTED
```

R8 evidence:

```text
raw_terminal.ndjson:
13025 bytes
f2baa8ca164341286411efea601f94fa4c8d636f2a8ae9c10cbcf2701decf5b0

final_terminal.json:
13025 bytes
f2baa8ca164341286411efea601f94fa4c8d636f2a8ae9c10cbcf2701decf5b0

manifest.sha256:
498 bytes
d60c0bbe99821a629df2137c365b3f6c1d494fdcb58dfcba150020f7dee95658

manifest verification:
3/3 OK
```

R8 final remote relation:

```text
target mapping:
NEW_EXACT
7112 bytes
d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
mari/mari/0644
historical device/inode 2050/550822

backup:
OLD_EXACT
5935 bytes
86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3
mari/mari/0644
historical device/inode 2050/550916

upload sidecar:
ABSENT

rollback temp:
ABSENT

Collector mutation by R8:
none
```

### 6.2 R30-I1-R9 Reliability acceptance

Report:

```text
path:
docs/reports/sprint4_d2_r7b_i1_r30_i1_r9_focused_reliability_final_rereview.md

bytes:
17260

SHA-256:
a7542bd7ee7459f56c6671a03198a44245c22aa639a3207b3758cd8676f2ba91
```

Accepted PM state:

```text
RELIABILITY_PASS_WITH_RECOMMENDATIONS
REVIEWED
PM-VERIFIED
PM-ACCEPTED
```

R1-R8 review areas all passed. There were no production blockers. Synthetic `pass_fds` fallback
and a bounded real-child FD probe remain non-blocking backlog only.

No later R10 task modified the config target, backup, upload sidecar or rollback temp. Nevertheless,
a new mutation task must fresh-observe these identities before relying on them.

## 7. Current active Collector state

The latest authoritative focused observation is R30-I1-R10-R2-R1.

Report:

```text
path:
docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_r2_r1_focused_restartcount_schema_correction.md

bytes:
6199

SHA-256:
5538df46f3dfe55cff3981b1370496b3e3740a7362d0e4ed33815b4a36aa42d8
```

Artifacts:

```text
restartcount_observer.py:
12386 bytes
3450f2e7845a79f8077e4f9c24e6258a26d9f86f715a3a16ec675c5d0dd01aa8

raw_terminal.ndjson:
4245 bytes
a1364eb39e4cc508c04c93869c130005231b4a239ce49bff3b01d4310dd4be48

final_terminal.json:
4245 bytes
a1364eb39e4cc508c04c93869c130005231b4a239ce49bff3b01d4310dd4be48

manifest.sha256:
683 bytes
a61b945b39d22f044ee42a74427677e1b19c41341a160bb84df040c442ed091e

manifest verification:
4/4 OK
```

Accepted PM state:

```text
RESTARTCOUNT_CONFIRMATION_PASS
RESTARTCOUNT_SCHEMA_CORRECTED_AND_OBSERVED
RESTARTCOUNT_ZERO_STABLE
OBSERVED
WRITTEN
PM-VERIFIED
PM-ACCEPTED
```

Two read-only inspect samples, six seconds apart, observed:

```text
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

PID:
3365014

Status:
running

RestartCount:
0 -> 0
source: top-level Docker inspect $.RestartCount

Running / Restarting / Dead:
true / false / false

ExitCode / OOMKilled / Error:
0 / false / empty

restart policy:
unless-stopped

/app/config mount:
bind /opt/edge-mes-demo/config -> /app/config
read-only

bounded six-second lifecycle tuple:
stable
```

This is an existing safe old-image state, not package-closed new-Collector activation.

Current active-image limitation retained from earlier durable evidence:

```text
/app/app/main.py:
matched the newer main source

/app/app/services/event_collector.py:
old-image source, not current package-closed source

/app/app/services/accepted_station_event_fact.py:
ABSENT

/app/app/services/storage.py:
old-image source, not current package-closed source
```

Therefore:

```text
package-closed new Collector active:
NO

accepted-fact runtime active:
NOT ESTABLISHED

runtime-loaded new mapping in current old process:
NOT ESTABLISHED

production acceptance:
NOT ESTABLISHED
```

The new PM must fresh-observe the remote tuple immediately before any image/lifecycle mutation.

## 8. R10 chronology and authoritative PM reconciliation

This section is critical. Historical Thread conclusions must not be mistaken for current blockers.

### 8.1 R30-I1-R10 historical local HOLD

Report:

```text
path:
docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_controlled_collector_restart_runtime_validation.md

bytes:
9593

SHA-256:
92595578a084e07429c508b5a1d0cce8608e276a233a06752ad0cb26320d7713
```

Thread result:

```text
RUNTIME_RELOAD_HOLD
PROCESS_GATE_UNAVAILABLE / PRE_CONTROLLER_CACHE_DRIFT
```

PM reconciliation:

```text
PROCESS_GATE_UNAVAILABLE:
INVALIDATED

Reason:
/bin/ps was available and found zero task-owned processes.

PRE_CONTROLLER_CACHE_DRIFT:
INVALIDATED

Reason:
The authorized cache gate covered only P2-R2/P2-R3 evidence trees; both were zero.
Collector development cache was out of scope and non-blocking.
```

R10 performed no SSH, restart, rollback or recovery.

### 8.2 R30-I1-R10-R1 false remote-prestate mismatch

Report:

```text
path:
docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_r1_corrected_controlled_collector_restart_runtime_validation.md

bytes:
7743

SHA-256:
6e115591ff85eee492b43c3205cd95373f58cde8c6075271b630f7da69e3f980
```

Thread result:

```text
RUNTIME_RELOAD_HOLD
REMOTE_PRESTATE_MISMATCH
```

The controller read RestartCount from the wrong schema path:

```text
incorrect:
$.State.RestartCount

correct:
$.RestartCount
```

It compared `null` with expected integer zero and created a false mismatch. It did not observe a
nonzero RestartCount. It performed no restart, rollback, recovery or retry.

PM classification:

```text
FALSE MISMATCH
NOT A CURRENT REMOTE BLOCKER
```

### 8.3 R30-I1-R10-R2 incomplete observer

Report:

```text
path:
docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_r2_readonly_remote_lifecycle_observation.md

bytes:
16579

SHA-256:
9509336399b33fd65abf2abc267ce2ff8e4401dc147146207214e46d2d17af7f
```

Thread result:

```text
REMOTE_LIFECYCLE_OBSERVATION_HOLD
TERMINAL_INCOMPLETE
OBSERVER_SOURCE_CONTRACT_DEFECT
```

Its observer repeated the same incorrect `$.State.RestartCount` path. Partial lifecycle facts were
useful, but actual RestartCount remained unobserved in that task. No mutation occurred.

### 8.4 R30-I1-R10-R2-R1 corrected final observation

R10-R2-R1 corrected the schema and established the current stable zero count described in Section
7.

The Thread window later reported HOLD because a precomputed final untracked digest did not match.
PM independently proved:

```text
actual final count:
13796

actual final path digest:
dc87f9e35398bb3f67d316c98f6807eff2ce79e814396ea73a166a0d7fcb3d92

remove the five exact authorized R10-R2-R1 output paths:
13791 paths
942acd5e70d70c29358d44c24b46b7eb3773f1db987d0b36a7566dcdc39ab20e
```

The remaining set exactly restored the accepted baseline. The Prompt's frozen expected digest was
a PM precomputation error.

PM classification:

```text
DIGEST BLOCKER:
INVALIDATED

R10-R2-R1 DURABLE RESULT:
PASS
```

### 8.5 Withdrawn historical interpretation

The following earlier inference is explicitly withdrawn and must not be reopened:

```text
Collector RestartCount was nonzero.
Collector definitely restarted after R8.
There is an unexplained restart history requiring more forensics.
```

Authoritative replacement:

```text
RestartCount:
0 -> 0

StartedAt:
unchanged from R8 baseline

bounded lifecycle tuple:
stable

unexplained-restart investigation:
CLOSED / NOT ESTABLISHED
```

## 9. Scope reset and controls that must not return as blockers

PM scope classification at handoff:

```text
SCOPE RESET REQUIRED FOR THE R10 OBSERVER/OLD-IMAGE-RELOAD CHAIN
```

The repair/observer chain is closed. Do not authorize:

- another RestartCount observer;
- another lifecycle-logs/events investigation;
- a digest repair task;
- a repository-wide cache audit;
- another old-image runtime reload experiment as a prerequisite;
- another review of the same invalidated false blockers.

The following controls are not valid blockers for the next MVP deployment gate:

- a precomputed final aggregate untracked-path digest;
- nonzero cache under `collector/**`, `tests/**`, `.venv/**` or repository-wide locations;
- `pgrep` or local `/proc` availability;
- full lifecycle-event retention;
- theoretical state-combination completeness;
- logs/events forensic completeness;
- proof of every diagnostic field when it cannot change the authorized PASS/HOLD outcome.

Proportional controls that should remain:

- exact output/write allowlist;
- baseline-minus-authorized-output path equality;
- artifact manifest and exact source/evidence identity;
- `/bin/ps` task-owned process check only when a local owned process is actually relevant;
- one explicit remote-call/lifecycle budget;
- exact active/rollback image identities;
- target/backup config identities;
- protected-service pre/post hard-field equality;
- fail-closed stop on foreign mutation or ambiguous active target;
- observed values persisted before assertions;
- no hidden retry, second SSH or conversational continuation.

## 10. Current authoritative gate state

```text
Local package-closure implementation:
COMMITTED

Local package-closure independent Verification:
PASS

Fresh deployable package-closed image identity:
NOT YET MATERIALIZED

Historical remote image 7b942...:
KNOWN BAD / DO NOT ACTIVATE

Exact new mapping remote deployment:
PASS / PM-ACCEPTED

Config deployment Reliability:
PASS WITH RECOMMENDATIONS / PM-ACCEPTED

Current active Collector:
existing safe old image
running
RestartCount 0
bounded lifecycle stable

Current old process runtime-loaded new mapping:
NOT ESTABLISHED

Package-closed new Collector active:
NO

Accepted-fact runtime active:
NOT ESTABLISHED

Production accepted-fact persistence validation:
NOT ESTABLISHED

Production acceptance:
NOT ESTABLISHED

Git stage / commit / push for current R30 reports and this handoff:
NOT STARTED
```

The old-image runtime-reload experiment is no longer a mandatory prerequisite. Its value is lower
than moving to the package-closed Collector required for accepted-fact MVP behavior.

## 11. Next MVP direction

The next product action is:

```text
materialize a fresh package-closed Collector image from the current committed source
-> establish an exact image identity
-> transport or build it on the remote host through a bounded reviewed mechanism
-> perform one controlled Collector-only activation
-> prove active source/import closure and exact mapping load
-> roll back to the exact current old image if activation validation fails
```

The next task should not immediately execute this whole chain from conversational momentum.

Recommended sequence for the new PM:

1. Read this handoff and the exact reports listed in the copyable prompt.
2. Run fresh local recovery.
3. Perform one narrowly scoped read-only remote baseline only if necessary to freeze:
   - current Collector ID/image/status/RestartCount/mount;
   - current image tag;
   - presence and identities of old and historical known-bad images;
   - config target/backup/sidecars;
   - protected-service hard fields;
   - remote disk capacity and Docker architecture only if required by the chosen image transport.
4. Choose the smallest image materialization/transport mechanism.
5. Issue a short Architecture / Integration planning or execution Prompt with a new authority.
6. Keep production accepted-fact validation as a later independent gate after activation PASS.

The new PM should prefer a short task over a generated multi-purpose controller. A mutation helper
may still be used, but it should contain only the commands and rollback needed for the actual image
activation claim.

## 12. Exact non-authorized surfaces at handoff

This handoff grants no authority for:

- source or test changes;
- Dockerfile or Compose changes;
- config changes or redeployment;
- image build, save, transport, load, tag or removal;
- remote source archive creation;
- Collector restart, recreate or activation;
- rollback;
- DB/API/PLC/V-PLC operations;
- production-data generation;
- accepted-fact persistence validation;
- broader service lifecycle;
- cleanup of caches, stage roots, images, containers or sidecars;
- update of `docs/current_status.md` or `docs/roadmap.md`;
- Git stage, commit, push or tag;
- status claims derived only from this handoff without fresh recovery.

Prior PASS states do not automatically grant any of these actions.

## 13. Known external/untracked artifacts

The checkout contains a large pre-existing untracked set, including historical reports, handoffs,
frontend build/dependency outputs and evidence trees. The handoff task did not classify or clean
that broad set.

Future tasks must:

- use exact output paths;
- treat all unrelated untracked paths as external/excluded;
- not stage broad `docs/`, `frontend/`, report or evidence directories;
- not clean, prune or delete unrelated artifacts;
- not use the total untracked count as evidence that all paths belong to the current task;
- compare the baseline after subtracting exact authorized task outputs when needed.

Known broad examples include:

```text
frontend/.next/
frontend/node_modules/
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
historical docs/reports/**
historical docs/reports/evidence/**
historical docs/thread_handoff/**
```

These remain excluded unless a future user authority names exact paths.

## 14. Recommended first action for the next ChatGPT PM

The next PM's first response should not issue an activation Prompt.

It should:

1. Open the project at `/Users/chenjie/Documents/MES/edge-mes-demo`.
2. Read `docs/thread_handoff/pm_operating_rules.md`.
3. Read this exact handoff.
4. Read the minimum exact reports listed below.
5. Run fresh local read-only recovery.
6. State whether the handoff baseline is recovered or has drifted.
7. Confirm the scope reset and that `7b942...` is not an activation candidate.
8. Propose the smallest fresh read-only/planning gate required before package-closed image
   materialization and controlled activation.
9. Wait for explicit user authority before issuing or executing a remote mutation Prompt.

Minimum report reading order:

```text
docs/reports/sprint4_d2_r7a_r4_r1_collector_package_closure_reverification.md

docs/reports/sprint4_d2_r6_r1_new_collector_remote_config_static_compatibility_retry.md

docs/reports/sprint4_d2_r7b_i1_r30_i1_r8_one_shot_exact_config_only_remote_execution.md

docs/reports/sprint4_d2_r7b_i1_r30_i1_r9_focused_reliability_final_rereview.md

docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_r2_r1_focused_restartcount_schema_correction.md
```

Additional historical context only if needed:

```text
docs/reports/sprint4_d2_r4_post_mutation_collector_live_state_recovery.md

docs/reports/sprint4_d2_r5_existing_image_collector_activation.md

docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_controlled_collector_restart_runtime_validation.md

docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_r1_corrected_controlled_collector_restart_runtime_validation.md

docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_r2_readonly_remote_lifecycle_observation.md
```

## 15. Copyable prompt for the next ChatGPT PM window

```markdown
You are the new ChatGPT PM for the Edge MES Demo project.

Project absolute path:

`/Users/chenjie/Documents/MES/edge-mes-demo`

Your first task is context recovery only. Do not issue or execute an image build, transport,
remote mutation, Collector restart/activation, rollback, DB/API/PLC operation or Git action in
your first response.

Read in this order:

1. `docs/thread_handoff/pm_operating_rules.md`
2. `docs/thread_handoff/chatgpt_pm_handoff_260729-1417.md`
3. `docs/reports/sprint4_d2_r7a_r4_r1_collector_package_closure_reverification.md`
4. `docs/reports/sprint4_d2_r6_r1_new_collector_remote_config_static_compatibility_retry.md`
5. `docs/reports/sprint4_d2_r7b_i1_r30_i1_r8_one_shot_exact_config_only_remote_execution.md`
6. `docs/reports/sprint4_d2_r7b_i1_r30_i1_r9_focused_reliability_final_rereview.md`
7. `docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_r2_r1_focused_restartcount_schema_correction.md`

Then run fresh read-only local recovery:

- `pwd`
- `git status -sb`
- `git log -8 --oneline --decorate`
- `git rev-parse --show-toplevel`
- `git rev-parse --abbrev-ref HEAD`
- `git rev-parse HEAD`
- `git rev-parse origin/main`
- `git rev-parse HEAD^`
- `git rev-list --left-right --count HEAD...origin/main`
- `git diff --name-only`
- `git diff --cached --name-only`
- `git diff --check`
- `git diff --cached --check`
- verify `config/mapping.yaml` bytes/SHA and that it is clean relative to HEAD
- verify the exact identities of this handoff and the five minimum reports

Recover and report these authoritative boundaries:

- `HEAD == origin/main == 1fac3ee567f1108e5a18b155e4133e1fecd50246` unless fresh facts show drift;
- exact new mapping deployment is PM-accepted;
- current active Collector was most recently observed on the old safe image, running,
  `RestartCount=0`, with a stable six-second lifecycle tuple;
- the earlier nonzero-RestartCount interpretation is withdrawn;
- `sha256:7b94217f...` is a historical known-bad image with missing `common` import closure and must not
  be activated;
- the locally verified package-closed validation image was temporary and deleted;
- no current deployable package-closed image identity has yet been materialized;
- the R10 observer/old-image-reload chain is closed under a PM scope reset;
- precomputed final untracked aggregate digests, repository-wide cache and repeated lifecycle
  forensics must not become blockers;
- no mutation or Git authority is inherited from the handoff.

After recovery, provide:

1. whether the local handoff baseline is recovered or has drifted;
2. the current authoritative gate summary;
3. the smallest next read-only or planning action needed to materialize and deploy a fresh
   package-closed Collector image;
4. a recommendation on whether the next task should be Architecture / Integration planning or a
   bounded execution gate;
5. no mutation Prompt until the user explicitly authorizes it.
```

## 16. Handoff delivery, staging and next authorization

Delivery state:

```text
handoff:
WRITTEN

reviewed by a new PM:
NOT YET

accepted by user as new-window authority:
NOT YET

staged:
NO

committed:
NO

pushed:
NO
```

This handoff is the only repository path created by the current handoff task.

Do not stage automatically. Exact-path Git closeout requires a separate user authorization naming:

```text
docs/thread_handoff/chatgpt_pm_handoff_260729-1417.md
```

The current recommended action is to open a new ChatGPT PM window using the copyable prompt above.
No manual SSH, Docker, cleanup or rollback action is required before that handoff.
