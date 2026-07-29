# Edge MES Demo — ChatGPT PM Handoff — 2026-07-29 19:45 UTC+8

## 1. Handoff identity

- Project：Edge MES Demo
- PM handoff type：ChatGPT PM window transition
- Project absolute path：`/Users/chenjie/Documents/MES/edge-mes-demo`
- Handoff file：`docs/thread_handoff/chatgpt_pm_handoff_260729-1945.md`
- Authoring timezone：China Standard Time / UTC+8
- Delivery state：`WRITTEN / UNSTAGED / UNCOMMITTED / UNPUSHED`
- This handoff does not grant remote、Docker、Collector lifecycle、cleanup or Git authority.

## 2. Live repository baseline after Git closeout

Fresh recovery after the authorized exact seven-path commit/push established：

```text
branch: main
HEAD: 66563677d3d1129fbc79c2c284b5f6d8b62f1932
origin/main: 66563677d3d1129fbc79c2c284b5f6d8b62f1932
ahead / behind: 0 / 0
cached index: empty
git diff --check: PASS
git diff --cached --check: PASS
```

Latest commit：

```text
66563677d3d1129fbc79c2c284b5f6d8b62f1932
Accept exact loaded Collector image gate
```

Parent commit：

```text
ca68dd4a4913238fc62e9621f1ac632c709a3149
Add PM handoff before Collector activation
```

The exact seven-path stage/commit/push was explicitly authorized by the user and completed successfully. Push result：`main -> origin/main`，with `HEAD == origin/main` after push.

## 3. Exact files committed in 6656367

```text
docs/current_status.md
docs/roadmap.md
docs/reports/sprint4_d2_r7b_i1_pm_scope_reset_governance_decision_image_loaded_exact.md
docs/reports/sprint4_d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation.md
docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/local_prerequisite_terminal.json
docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/remote_reconciliation_terminal.json
docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/manifest.sha256
```

Commit summary：

```text
7 files changed
1426 insertions
32 deletions
```

No non-allowlist file was staged or committed.

## 4. Current closed gate

The package-closed image load gate is now closed and committed as：

```text
PASS
PM_SCOPE_RESET_ACCEPTS_R32_R5_R2_IMAGE_LOADED_EXACT
```

Accepted terminal facts：

```text
LOCAL_PACKAGE_CLOSED_IMAGE_VALIDATION_PASS
IMAGE_ARCHIVE_IDENTITY_VERIFIED
IMAGE_TRANSPORT_IDENTITY_VERIFIED
REMOTE_DOCKER_LOAD_COMMAND_PASS
DESCRIPTIVE_TAG_READY
REMOTE_LOADED_OBJECT_CONTENT_RECONCILED
IMAGE_LOADED_EXACT
```

Not established and not authorized：

```text
NOT ACTIVATION-ELIGIBLE
NOT ACTIVATED
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED
```

The normalization runner repair branch is closed：

```text
R32-R5 normalization runner repair chain: CLOSED / SUPERSEDED
new R32-R5-R6 runner repair: NOT AUTHORIZED
terminal JSON key-order/schema issue: NON-BLOCKING HISTORICAL DIAGNOSTIC
generic evidence-normalization framework: OUT OF CURRENT MVP SCOPE
```

## 5. Minimum accepted image identity facts

Frozen descriptive tag：

```text
edge-mes-demo-collector:r32-pkg-closed-ca68dd4
```

Retained local archive：

```text
/private/var/tmp/edge-mes-d2-r7b-i1-r32-ca68dd4/edge-mes-demo-collector-r32-ca68dd4-linux-arm64.tar
bytes: 54313984
SHA-256: b0fc3d6e4c511cfc1782d5ce15ef3d9cd053ce99a3571622daf165422d65ce2e
```

OCI manifest digest：

```text
sha256:899082388afebab65844cbc0e49fb69a0f19f8bf23c3c4c989f6533f2f2ce401
```

OCI config digest / remote Docker object ID：

```text
sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734
```

Accepted reconciliation facts：

```text
platform: linux / arm64
Created: 2026-07-29T15:43:02.675492291+08:00
Cmd: ["python", "-m", "app.main"]
WorkingDir: /app
ordered Env equality: PASS
canonical / remote RootFS count: 9 / 9
ordered RootFS equality: PASS
RootFS mismatch indices: []
all remote RootFS values: valid sha256 digests
```

Tag state from the accepted durable remote payload：

```text
descriptive tag
-> sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734

compatibility tag edge-mes-demo-collector:latest
-> sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a

known-bad image owns descriptive tag: false
```

The accepted R32-R5-R2 source SSH capture recorded：

```text
return code: 0
stdout: 11688 bytes
stderr: 0 bytes
structured SSH calls: 1
mutations during reconciliation: all zero
```

These are prior durable facts. This handoff does not represent them as a fresh remote observation.

## 6. Primary durable authority paths

Read these first for the current gate：

1. `docs/thread_handoff/pm_operating_rules.md`
2. `docs/current_status.md`
3. `docs/roadmap.md`
4. `docs/reports/sprint4_d2_r7b_i1_pm_scope_reset_governance_decision_image_loaded_exact.md`
5. `docs/reports/sprint4_d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation.md`
6. `docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/local_prerequisite_terminal.json`
7. `docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/remote_reconciliation_terminal.json`
8. `docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/manifest.sha256`
9. `docs/reports/sprint4_d2_r7b_i1_r31_package_closed_collector_image_materialization_deployment_plan.md`
10. this handoff file.

The R32-R5-R2 manifest verifies its report and two terminals as `3/3 OK` from the repository root.

## 7. Historical HOLD records and supersession boundary

Historical records remain unchanged：

```text
R32-R5-R2 original durable schema:
HOLD / TERMINAL_JSON_OBSERVED_ASSERTIONS_CONTRACT_HOLD

R32-R5-R3:
HOLD / no durable output

R32-R5-R4:
HOLD / RUNNER_SYNTAX_VALIDATION_FAILED

R32-R5-R5:
HOLD / PM_FROZEN_RUNNER_TARGET_SYNTAX_CONTRACT_DEFECT
```

These are process-history facts. Under the committed PM scope-reset decision, they no longer block `IMAGE_LOADED_EXACT` and must not be reopened through conversational momentum.

Do not issue another normalization-runner repair unless the user explicitly opens a separate Level 2 evidence-framework project.

## 8. Status-document authoring-time note

`docs/current_status.md` and `docs/roadmap.md` were authored before commit `6656367` and therefore contain next-sequence wording such as `Git closeout pending`.

Live Git now proves that the exact seven-path closeout is complete. For the current checkout：

```text
scope-reset docs/evidence Git closeout: COMMITTED / PUSHED
commit: 66563677d3d1129fbc79c2c284b5f6d8b62f1932
```

Treat the pre-commit wording as an authoring-time marker superseded by live Git and this later handoff. It does not reopen Git closeout and does not grant activation authority.

A future docs/status wording refresh is non-blocking unless another task needs those exact lines to serve as its authority source.

## 9. Known external dirty artifacts

Tracked dirty paths that existed before this handoff and remain excluded：

```text
.gitignore
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
docs/thread_handoff/pm_operating_rules.md
```

Do not modify、restore、stage、commit or clean these paths without a new exact-path authority.

The checkout also contains many pre-existing untracked historical reports/evidence directories, old PM handoffs and frontend build artifacts. Important excluded patterns include：

```text
docs/reports/evidence/d2_r7b_i1_*/
docs/reports/sprint3_*.md
docs/reports/sprint4_d2_r7b_i1_*.md not explicitly authorized
docs/thread_handoff/chatgpt_pm_handoff_*.md other than a newly authorized exact file
frontend/.next/
frontend/node_modules/
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
```

Do not use broad staging such as `git add .`、`git add -A` or `git add docs/`.

## 10. Current non-authorized surfaces

No authority currently exists for：

- network、SSH or remote read；
- reading SSH private-key contents；
- local or remote Docker commands；
- compatibility-tag mutation；
- Collector restart、recreate or activation；
- protected-service inspection or mutation；
- post-activation validation；
- rollback；
- runtime-loaded config observability；
- production accepted-fact generation or validation；
- cleanup of local archive、remote stage files、images、tags or historical artifacts；
- Git stage、commit、push or tag beyond a separately approved exact-path task.

A prior PASS never grants the next phase automatically.

## 11. Recommended next gate

The next product-facing gate, only after explicit user authorization, is：

```text
fresh read-only remote activation preflight
```

This must be a new Architecture / Integration Thread with a new authority and fresh remote-call budget.

Its narrow objective should be to determine whether activation is currently eligible by freshly reading：

- loaded target object and descriptive tag；
- active Collector identity、image、running/restarting/dead state、restart count and start time；
- compatibility alias current target；
- exact currently active protected-service set and frozen hard fields；
- current bind mount/source identity；
- rollback old-safe exact image identity；
- absence of ambiguous or foreign active target.

The preflight must be read-only. It must not tag、restart、recreate、activate、rollback or clean anything.

A preflight PASS may establish only：

```text
ACTIVATION_ELIGIBLE
```

It may not establish activation、runtime-loaded or production acceptance.

## 12. Carry-forward items

Current-gate blockers：none.

Non-blocking carry-forward items：

- status/roadmap contain pre-commit `Git closeout pending` wording; live Git and this handoff supersede it；
- generic evidence-normalization/audit framework is out of MVP and may be considered only as an independent future Level 2 project；
- all runtime、activation、rollback and production-validation phases remain separate.

Recommendations：none beyond preserving the authority separation above.

## 13. Recommended first read-only action for the next PM

Before issuing any task：

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
git status -sb
git log -8 --oneline --decorate
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git diff --name-only
git diff --cached --name-only
git diff --check
git diff --cached --check
```

Expected committed baseline at handoff：

```text
HEAD == origin/main == 66563677d3d1129fbc79c2c284b5f6d8b62f1932
ahead / behind: 0 / 0
cached index: empty
```

Live facts override this snapshot if the repository legitimately changes later.

## 14. Copyable prompt for the next ChatGPT PM window

```text
你是 Edge MES Demo 项目的新任 ChatGPT PM。

项目绝对路径：
/Users/chenjie/Documents/MES/edge-mes-demo

首先按顺序读取：

1. docs/thread_handoff/pm_operating_rules.md
2. docs/thread_handoff/chatgpt_pm_handoff_260729-1945.md
3. docs/current_status.md
4. docs/roadmap.md
5. docs/reports/sprint4_d2_r7b_i1_pm_scope_reset_governance_decision_image_loaded_exact.md
6. docs/reports/sprint4_d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation.md
7. docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/local_prerequisite_terminal.json
8. docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/remote_reconciliation_terminal.json
9. docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/manifest.sha256
10. docs/reports/sprint4_d2_r7b_i1_r31_package_closed_collector_image_materialization_deployment_plan.md

随后先执行只读 recovery：

cd /Users/chenjie/Documents/MES/edge-mes-demo
git status -sb
git log -8 --oneline --decorate
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git diff --name-only
git diff --cached --name-only
git diff --check
git diff --cached --check

Handoff 时的 committed baseline：

HEAD == origin/main == 66563677d3d1129fbc79c2c284b5f6d8b62f1932
ahead / behind: 0 / 0
cached index: empty

当前 closed gate：

PASS
PM_SCOPE_RESET_ACCEPTS_R32_R5_R2_IMAGE_LOADED_EXACT

已接受：

LOCAL_PACKAGE_CLOSED_IMAGE_VALIDATION_PASS
IMAGE_ARCHIVE_IDENTITY_VERIFIED
IMAGE_TRANSPORT_IDENTITY_VERIFIED
REMOTE_DOCKER_LOAD_COMMAND_PASS
DESCRIPTIVE_TAG_READY
REMOTE_LOADED_OBJECT_CONTENT_RECONCILED
IMAGE_LOADED_EXACT

仍未建立：

NOT ACTIVATION-ELIGIBLE
NOT ACTIVATED
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED

R32-R5 normalization runner repair chain 已 CLOSED / SUPERSEDED。不得继续生成 R32-R5-R6 runner repair。

当前不授权 network、SSH、Docker、tag mutation、Collector lifecycle、rollback、cleanup 或 Git mutation。

下一产品 gate 只能在用户明确授权后进入 fresh read-only remote activation preflight。该 preflight 必须新开 Architecture / Integration Thread，使用新 authority 与 fresh remote-call budget，只读观察 current loaded object、active Collector、compatibility alias、protected services、bind mount 和 rollback identity。不得在 preflight 中执行 tag、restart、recreate、activation、rollback 或 cleanup。

请先报告 read-only recovery 结果、当前 gate、外部 dirty artifacts、authority boundary 和建议的最小下一步；不要自动执行远端操作或 Git 操作。
```

## 15. Handoff completion state

This file completes the PM handoff writing step only：

```text
handoff: WRITTEN
staged: NO
committed: NO
pushed: NO
```

A separate explicit exact-path user authorization is required before staging、committing or pushing this handoff file.
