# Sprint 4 D2-R7B-I1 PM Scope-Reset Governance Decision — IMAGE_LOADED_EXACT

## 报告身份

- 决策：D2-R7B-I1 package-closed Collector image load gate scope reset
- 执行角色：ChatGPT PM
- Authority：`PM-D2-R7B-I1-SCOPE-RESET-IMAGE-LOADED-EXACT-260729-1932`
- Delivery mode：`REPOSITORY_DURABLE_REPORT`
- 结论：`PASS`
- Terminal classification：`PM_SCOPE_RESET_ACCEPTS_R32_R5_R2_IMAGE_LOADED_EXACT`

## Scope

本决策只执行本地 PM governance intake、既有 durable evidence 的只读交叉复核，以及 gate/status 同步。没有执行新的 network、SSH、Docker、remote filesystem、Collector lifecycle、cleanup 或 Git mutation。

本决策不改写 R32-R5、R32-R5-R1、R32-R5-R2、R32-R5-R4 或 R32-R5-R5 的历史报告与 artifacts。它保留这些任务各自的原始 PASS/HOLD 过程结论，同时按 `docs/thread_handoff/pm_operating_rules.md` Sections 12–13 对证据 burden 进行比例性 scope reset。

## Live repository baseline

```text
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: ca68dd4a4913238fc62e9621f1ac632c709a3149
origin/main: ca68dd4a4913238fc62e9621f1ac632c709a3149
HEAD^: 1fac3ee567f1108e5a18b155e4133e1fecd50246
ahead / behind: 0 / 0
cached index: empty
git diff --check: PASS
git diff --cached --check: PASS
```

六个 pre-existing tracked dirty paths 保持外部排除状态：

```text
.gitignore
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
docs/thread_handoff/pm_operating_rules.md
```

## Restated MVP claim

本 gate 的最小产品声明是：

> 一个由冻结源码生成并完成本地 package-closure 验证的 Linux/arm64 Collector image，已经通过完整 archive transport/load 流程，以内容与 archive config 完全一致的 Docker image object 存在于远端；该 image 尚未激活。

`IMAGE_LOADED_EXACT` 只要求证明：

1. archive OCI config digest 与远端 Docker object ID 相等；
2. OS、architecture、Created、Cmd、WorkingDir 与 ordered Env 相等；
3. archive 的九项 ordered RootFS diff IDs 与远端九项 ordered RootFS Layers 相等；
4. descriptive tag 指向该 object；
5. compatibility tag 仍指向旧安全 image；
6. known-bad image 不持有 descriptive tag；
7. reconciliation 没有执行 load、tag、container lifecycle、filesystem mutation 或 cleanup。

本 gate 不要求建立 generic evidence-normalization、audit、retention 或 forensics framework。

## Accepted durable source evidence

主要 factual source：

```text
docs/reports/sprint4_d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation.md
docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/local_prerequisite_terminal.json
docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/remote_reconciliation_terminal.json
docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/manifest.sha256
```

R32-R5-R2 durable identities：

```text
report: 5047 bytes / f90b41a047c7380b85d630f79e4624f59265184cf0455b433f87846fed61ac7e
local terminal: 8415 bytes / 98e1dce7ba947e99b7c9e81ce3ac3431cc951abe4f8c0b3d104adf48e25cbd5d
remote terminal: 32190 bytes / 629dfda5d8c1b8e1096ccbc64625154c3778d80d239522bdb0652295c3586997
manifest: 560 bytes / 58185a699aa93f2379b411be33063bdaacd40020303d935b135ae69f9c923f49
manifest result: 3/3 OK
```

PM 对 retained archive 与 R32-R5-R2 parsed payload 的只读交叉复核得到：

```text
archive config digest:
sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734

remote object ID:
sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734

identity equality: PASS
ordered Env equality: PASS
canonical / remote RootFS count: 9 / 9
ordered RootFS equality: PASS
RootFS mismatch indices: []
all remote RootFS digests valid: PASS

descriptive tag:
edge-mes-demo-collector:r32-pkg-closed-ca68dd4
-> sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734

compatibility tag:
edge-mes-demo-collector:latest
-> sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a

known-bad descriptive-tag relation: ABSENT
source SSH return code: 0
source SSH stdout / stderr: 11688 / 0 bytes
source network calls: 1
source mutations: all zero
```

这次 PM 复核不是新的 remote observation，而是对 retained local archive 与既有 durable remote payload 的本地重新计算。

## Scope-reset judgment

R32-R5-R2 的原始 terminal schema 没有顶层 `observed` / `assertions`，因此其 schema delivery 缺陷仍作为历史事实保留：

```text
R32-R5-R2 durable schema:
HOLD / TERMINAL_JSON_OBSERVED_ASSERTIONS_CONTRACT_HOLD
```

R32-R5-R3、R4、R5 的 normalization attempts 也保留原始过程结论：

```text
R32-R5-R3: HOLD / no durable output
R32-R5-R4: HOLD / RUNNER_SYNTAX_VALIDATION_FAILED
R32-R5-R5: HOLD / PM_FROZEN_RUNNER_TARGET_SYNTAX_CONTRACT_DEFECT
```

这些缺陷没有造成以下任一 Section 12 blocker outcome：

- 没有缺失或错误的 remote RootFS/Env factual payload；
- 没有把 local/synthetic evidence 表示为新的 remote observation；
- 没有错误 image identity 或 tag relation；
- 没有 remote mutation、protected-object mutation 或 lifecycle contamination；
- 没有将 activated/runtime/production 状态误写为 PASS。

连续 normalization runner repair 已使 evidence mechanism 比 MVP load claim 更复杂，符合 `SCOPE RESET REQUIRED` warning signs。继续要求新的 runner repair 将成为 task inflation，而不是防止可信 false PASS 所必需的最小动作。

## Accepted gate state

PM 现接受：

```text
LOCAL_PACKAGE_CLOSED_IMAGE_VALIDATION_PASS
IMAGE_ARCHIVE_IDENTITY_VERIFIED
IMAGE_TRANSPORT_IDENTITY_VERIFIED
REMOTE_DOCKER_LOAD_COMMAND_PASS
DESCRIPTIVE_TAG_READY
REMOTE_LOADED_OBJECT_CONTENT_RECONCILED
IMAGE_LOADED_EXACT
```

继续保持：

```text
NOT ACTIVATION-ELIGIBLE
NOT ACTIVATED
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED
```

`IMAGE_LOADED_EXACT` 的 accepted authority 来自 R32-R5-R2 durable factual payload、retained archive identity 和本 PM scope-reset decision的组合，不改变历史 R32-R5-R2 report 自身的 schema HOLD 记录。

## Supersession and backlog

```text
R32-R5 normalization runner repair chain: CLOSED / SUPERSEDED
new R32-R5-R6 runner repair: NOT AUTHORIZED
terminal JSON key-order/schema defect: NON-BLOCKING HISTORICAL DIAGNOSTIC
generic evidence-normalization framework: OUT OF CURRENT MVP SCOPE
```

如未来确实需要通用 evidence schema 或 audit framework，必须作为独立 Level 2 项目定义目标、风险、allowlist 和验收标准，不得继续阻塞本 MVP。

## Authority boundary

本决策与 docs/status sync 不授权：

- network、SSH 或 remote read；
- compatibility tag mutation；
- Collector restart、recreate 或 activation；
- post-activation validation；
- rollback；
- runtime-loaded config observability；
- production accepted-fact validation；
- cleanup；
- Git stage、commit、push 或 tag。

R31 中的 activation phase separation 仍有效。任何 activation preflight 必须使用新的独立 authority，并 fresh 读取当时的 remote object、active Collector、compatibility alias、protected services 和 rollback identity。

## Next gate

当前 docs/status sync 完成后，唯一 next gate 是：

```text
ChatGPT PM exact-path Git candidate review
```

该 review 必须决定本 scope-reset report、`docs/current_status.md`、`docs/roadmap.md` 以及其引用的未提交 source evidence应采用的精确 Git closeout allowlist。没有用户明确授权时，不得 stage、commit 或 push。

Git closeout完成后，用户才可单独授权：

```text
fresh read-only remote activation preflight
```

## MVP 路径一致性

- 当前决策直接服务批准 MVP：yes。
- MVP deliverable：远端已加载且内容精确匹配的 package-closed Collector image，保持未激活状态。
- minimum invariant：archive config/Env/RootFS、remote object、descriptive tag、safe-old compatibility tag必须一致，且 reconciliation mutation为零。
- 新增产品能力、威胁模型、evidence framework或基础设施：no。
- task inflation：normalization repair chain已停止并降级为历史诊断。
- classification：`MVP-ALIGNED`。
