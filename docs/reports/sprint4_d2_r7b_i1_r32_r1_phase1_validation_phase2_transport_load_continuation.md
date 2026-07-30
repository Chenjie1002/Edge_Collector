# Sprint 4 D2-R7B-I1 R32-R1 Phase 1 Validation and Phase 2 Transport/Load Continuation

## 报告身份

报告名称：
Sprint 4 D2-R7B-I1 R32-R1 Phase 1 Validation and Phase 2 Transport/Load Continuation

任务名称：
D2-R7B-I1 R32-R1 — Correct the Host Validation Interpreter Contract, Validate the Existing Exact Fresh Image, Then Perform the Bounded Archive, Transport and Remote Load Continuation

执行 Thread：
Architecture / Integration

Authority source / ID：
PM-D2-R7B-I1-R32-R1-HOST-INTERPRETER-CORRECTION-CONTINUATION-01

Report delivery mode：
REPOSITORY_REPORT_WITH_ARTIFACTS

## 结论

HOLD

Terminal classification：
REMOTE_PREFLIGHT_PROBE_CONTRACT_HOLD

The first and only SSH call observed all task-contract remote prerequisite facts as passing, but
the bounded shell probe added an unauthorized condition requiring the remote `mari` UID to equal
the local UID `501`. The remote authorized user was `mari`, `/home/mari` was owned by `mari:mari`,
and the observed remote UID was `1000`. The extra UID comparison caused the preflight command to
return exit `2` / `HOLD`. Under the one-shot stop rule, this task did not repair the probe, retry
SSH, transport, load, or make any additional network call.

The observed remote contract facts themselves were:

```text
authorized user: mari
/home/mari: mari:mari:1000:700:directory
stage root: ABSENT
remote archive: ABSENT
Docker: linux / aarch64, normalized arm64
free disk: 461896556544 bytes
required free bytes: 377049027
retained safety margin: 268435456 bytes
descriptive tag: ABSENT
fresh exact image ID: ABSENT
```

## Fresh local baseline and retained identity

```text
project root: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: ca68dd4a4913238fc62e9621f1ac632c709a3149
origin/main: ca68dd4a4913238fc62e9621f1ac632c709a3149
HEAD^: 1fac3ee567f1108e5a18b155e4133e1fecd50246
ahead / behind: 0 / 0
cached index: empty
git diff --check: PASS
git diff --cached --check: PASS
```

The six prompt-listed tracked dirty paths were preserved as pre-existing external artifacts and
were not read as execution source, modified, cleaned, staged or committed:

```text
.gitignore
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
docs/thread_handoff/pm_operating_rules.md
```

R32 durable identity verification:

```text
R32 report: 5405 bytes / SHA-256 cc287fa63c0901bd1e8663621bcd3757fe2b85da0d883f105862aa803af73430
R32 manifest: 6/6 OK
R32 build-input manifest: 3797 bytes / SHA-256 ad339c6adaa3556df513b9dca30af6fe129b2d583b3f7720adab0b9e692044da
retained build-context verification: 38/38 OK
mapping: 7112 bytes / SHA-256 d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
mapping HEAD blob: b46a637f23c761d0a4c3fe048b3b7480a3dec2ce
build-relevant source relative to frozen baseline: clean
```

Retained exact image:

```text
tag: edge-mes-demo-collector:r32-pkg-closed-ca68dd4
image ID: sha256:899082388afebab65844cbc0e49fb69a0f19f8bf23c3c4c989f6533f2f2ce401
OS / Architecture: linux / arm64
size: 54299587
created: 2026-07-29T15:43:02.675492291+08:00
```

## Phase 1 validation

### Host interpreter prerequisite

```text
exact interpreter: /Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python
snap7: 3.0.0
PyYAML: 6.0.2
prerequisite invocation count: 1
system python3 used: no
dependency installation: no
bytecode write: no
Storage construction: 0
Snap7 client construction: 0
network connections: 0
```

Classification:

```text
HOST_VALIDATION_INTERPRETER_PREREQUISITE_PASS
```

### Host static mapping

```text
host static invocation count: 1
schema_version: runtime-mapping/v1
config_version: 2026.06.26-slice-a
line_id: LINE_001
read-plan count: 4
resolved config hash: 0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
Storage construction: 0
Snap7 client construction: 0
network connections: 0
```

### Isolated exact-image validation

The sole container invocation used the exact full image ID with `--rm`, `--pull never`,
`--network none`, `--read-only`, the bounded `/tmp` tmpfs, `PYTHONDONTWRITEBYTECODE=1`, and the
read-only config bind mount. It imported `app.main`, `app.services.event_collector`,
`common.station_event`, and the actual `common.station_event` module closure:

```text
constants, errors, fingerprint, lifecycle, models, projection, serialization, validation
```

Container static fields exactly matched host static fields:

```text
schema_version: runtime-mapping/v1
config_version: 2026.06.26-slice-a
line_id: LINE_001
read-plan count: 4
resolved config hash: 0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
container validation invocation count: 1
Storage construction: 0
Snap7 client construction: 0
network connections: 0
long-running process: 0
production data: 0
```

Phase 1 classification:

```text
LOCAL_PACKAGE_CLOSED_IMAGE_VALIDATION_PASS
```

Durable evidence: `docs/reports/evidence/d2_r7b_i1_r32_r1_phase1_validation_phase2_transport_load_continuation/phase1_validation_terminal.json`.

## Archive

The archive was created only after Phase 1 PASS, with one `docker save` invocation whose source
was the exact full image ID. It was not overwritten or cleaned:

```text
local archive: /private/var/tmp/edge-mes-d2-r7b-i1-r32-ca68dd4/edge-mes-demo-collector-r32-ca68dd4-linux-arm64.tar
archive state: PRESENT / REGULAR / NON-SYMLINK
bytes: 54313984
SHA-256: b0fc3d6e4c511cfc1782d5ce15ef3d9cd053ce99a3571622daf165422d65ce2e
docker save invocation count: 1
post-save exact image/tag identity: unchanged
post-save R32 manifest: 6/6 OK
```

Classification:

```text
IMAGE_ARCHIVE_IDENTITY_VERIFIED
```

## Remote call budget and terminal

```text
Call 1 / load-only preflight SSH: 1, consumed, terminal command exit 2 / HOLD
Call 2 / transport: 0, not executed
Call 3 / remote load/verify: 0, not executed
total network calls: 1
retry / resume / supplemental SSH: 0
```

Remote stage root and archive remained absent. No remote Docker load, tag/retag, container
lifecycle, Compose command, cleanup, compatibility alias mutation, active Collector inspection,
protected-service inspection, logs/events, DB/API/PLC/V-PLC/simulator operation or production data
operation occurred.

Durable remote evidence:

```text
docs/reports/evidence/d2_r7b_i1_r32_r1_phase1_validation_phase2_transport_load_continuation/phase2_remote_preflight_terminal.json
```

Transport and load terminal artifacts are explicit `NOT_EXECUTED` records caused by the preflight
terminal and contain no inferred remote success:

```text
phase2_transport_terminal.json: NOT_EXECUTED
phase2_remote_load_terminal.json: NOT_EXECUTED
```

## Mutation and Git audit

```text
Docker build: 0
Docker pull: 0
Docker isolated validation container: 1
Docker save: 1
Docker load: 0
Docker tag/retag: 0
Docker image removal: 0
Docker/Compose lifecycle: 0
Compatibility alias mutation: NO
cleanup: 0
Git staged: NO
Git committed: NO
Git pushed: NO
Git reset/restore/checkout/stash/clean: 0
```

Repository paths created by this task are limited to the exact report and five JSON terminal
artifacts plus the final self-excluded manifest. No source, test, Dockerfile, Compose, config,
status, roadmap, handoff, R32 report or R32 artifact was modified.

## Retained residue

Local retained residue:

```text
/private/var/tmp/edge-mes-d2-r7b-i1-r32-ca68dd4
/private/var/tmp/edge-mes-d2-r7b-i1-r32-ca68dd4/build-context
/private/var/tmp/edge-mes-d2-r7b-i1-r32-ca68dd4/edge-mes-demo-collector-r32-ca68dd4-linux-arm64.tar
edge-mes-demo-collector:r32-pkg-closed-ca68dd4 -> sha256:899082388afebab65844cbc0e49fb69a0f19f8bf23c3c4c989f6533f2f2ce401
```

Remote retained residue:

```text
/home/mari/.edge-mes-demo-stage/d2-r7b-i1-r32-ca68dd4: ABSENT
/home/mari/.edge-mes-demo-stage/d2-r7b-i1-r32-ca68dd4/edge-mes-demo-collector-r32-ca68dd4-linux-arm64.tar: ABSENT
```

No cleanup was authorized or executed.

## Blockers and recommendations

Blocker:

```text
REMOTE_PREFLIGHT_PROBE_CONTRACT_HOLD
```

The one-shot preflight probe incorrectly compared the remote authorized user's UID with the local
UID. This is an execution-contract defect in the bounded probe, not evidence of a remote user or
filesystem ownership failure. Nevertheless, the command returned HOLD and the authority requires
immediate stop without repair or retry; therefore transport and load remain unexecuted.

Recommendations:

```text
none within this consumed authority
```

No activation Prompt is generated. Any future continuation requires a new PM authority and fresh
execution budget.

## Evidence classification

Established:

```text
HOST_VALIDATION_INTERPRETER_PREREQUISITE_PASS
LOCAL_PACKAGE_CLOSED_IMAGE_VALIDATION_PASS
IMAGE_ARCHIVE_IDENTITY_VERIFIED
NOT ACTIVATED
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED
```

Not established:

```text
IMAGE_TRANSPORT_IDENTITY_VERIFIED
IMAGE_LOADED_EXACT
ACTIVATION_ELIGIBLE
ACTIVATED
RUNTIME-LOADED
PRODUCTION-ACCEPTED
```

## MVP 路径一致性

```text
当前任务是否直接服务批准 MVP: yes
minimum invariant: only the retained exact package-closed image may produce archive evidence, and remote load evidence must be exact-ID bound before any activation gate
是否扩大产品能力、威胁模型、证据平台或基础设施: no
是否 task inflation: no
classification: MVP-ALIGNED
```

The local image, static package closure and exact archive directly support the approved Collector
package-closure/deployment boundary. The failed continuation does not authorize broad diagnostics,
runtime lifecycle, production truth or infrastructure work.

## Next gate and Thread context assessment

唯一 next gate：

```text
R32-R1 continuation -> ChatGPT PM durable intake only
```

不得自动进入 active Collector preflight、compatibility alias mutation、restart/recreate,
activation、post-activation validation、rollback、runtime config observability、production
accepted-fact persistence、cleanup 或 Git closeout。

```text
本次输出长度: 长（完整事实已持久化，Chat 返回 concise manifest）
当前 Thread 是否建议继续: no
下一轮是否建议新开 Thread: yes
理由: one-shot remote preflight authority has terminated at HOLD; a new authority and fresh context are required, and the local bounded probe contract must be corrected before any future remote call
```

## Artifact manifest

The final self-excluded `manifest.sha256` binds this report and the five JSON terminal artifacts;
all six referenced files are regular, non-symlink files and the final verification is `6/6 OK`.
