# Sprint 4 D2-R7B-I1 R29-R2-R1 Docs-Only Closeout Repair

## 1. 报告身份与结论

~~~text
报告名称：Sprint 4 D2-R7B-I1 R29-R2-R1 Docs-Only Closeout Repair
任务名称：D2-R7B-I1 R29-R2-R1 — Repair Docs-Only Closeout Artifacts and Restore Durable Consistency
执行 Thread：Architecture / Integration
Report delivery mode：REPOSITORY_DURABLE_REPORT
Exact report path：docs/reports/sprint4_d2_r7b_i1_r29_r2_remote_cleanup_closeout_and_status_sync.md
Exact artifact paths：none
项目绝对路径：/Users/chenjie/Documents/MES/edge-mes-demo
Original R29-R2 disposition：HOLD / PM-VERIFIED / PM-ACCEPTED AS FAIL-CLOSED DOCS WRITE
R29-R2-R1 repair disposition：PASS / WRITTEN
结论：PASS（仅表示 R29-R2-R1 docs-only repair validation 通过；原始 R29-R2 attempt 仍为 HOLD）
~~~

本报告保留原始 R29-R2 attempt 的 `HOLD / FAIL-CLOSED` 历史，并增加独立 R29-R2-R1 repair closeout。本报告、`docs/current_status.md` 与 `docs/roadmap.md` 只建立 `WRITTEN`；不建立 `PM-ACCEPTED`、`VERIFIED`、`STAGED`、`COMMITTED`、`PUSHED`、`DEPLOYED` 或 `ACTIVATED`。本报告自身最终 bytes/SHA-256 只在 concise window manifest 返回，正文不记录自引用 digest。

## 2. Authority 与消费状态

Original R29-R2 authority：来自前序用户授权与 `docs/thread_handoff/chatgpt_pm_handoff_260728-1425.md`，已被第一次 docs write 消费；其结果为 `HOLD / PM-VERIFIED / PM-ACCEPTED AS FAIL-CLOSED DOCS WRITE`，不被本轮重试或继承。

R29-R2-R1 repair authority：当前用户明确授权的独立 docs-only repair，仅允许修改上述 exact three paths。Authority state：`AUTHORIZED ONCE / DOCS-ONLY REPAIR / EXACT THREE PATHS / NO GIT MUTATION / NO NETWORK / NO SSH / NO REMOTE / NOT REUSABLE`。第一次修改任一 exact writable path 时消费；不授权 retry、第二次写入同一路径、Git stage/commit/push/tag、cleanup、eligibility、upload、deployment、rollback、restart、activation、runtime-loaded validation、production acceptance、source、test、helper 或 manifest 修改。

本轮只执行 local read-only recovery、source/evidence identity checks、进程审计、路径安全审计、三文件写入与最终本地 validation；network calls、SSH、remote calls 与 remote mutation 均为 `0`。

## 3. Required reading 与 evidence boundary

已按用户指定顺序读取并在完成 required reading 后再次读取 PM rules Section 10 与 Section 11：

~~~text
docs/thread_handoff/pm_operating_rules.md
docs/thread_handoff/chatgpt_pm_handoff_260728-1425.md
docs/current_status.md
docs/roadmap.md
docs/reports/sprint4_d2_r7b_i1_r28_r1_readonly_current_remote_state_refresh.md
docs/reports/sprint4_d2_r7b_i1_r28_r1_r1_readonly_current_remote_state_refresh.md
docs/reports/sprint4_d2_r7b_i1_r28_r2_readonly_current_remote_state_observation.md
docs/reports/sprint4_d2_r7b_i1_r29_r1_cleanup_exact_r26_upload_sidecar.md
docs/reports/sprint4_d2_r7b_i1_r27_r6_local_gate_closeout_and_status_sync.md
docs/reports/sprint4_d2_r7b_i1_r27_r6_r1_eof_identity_repair.md
docs/reports/sprint4_d2_r7b_i1_r26_exact_config_only_remote_execution.md
docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/final_terminal.json
docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
config/mapping.yaml
~~~

历史 report evidence、accepted read-only remote evidence、accepted cleanup transaction
evidence、current local Git facts 与 R29-R2 的 not-fresh-remote boundary 分开记录；历史
evidence 不被本轮改写为 fresh remote fact。

## 4. Fresh local recovery 与 live facts

从项目根目录完成了用户要求的 exact recovery。pre-repair live facts 为：

~~~text
pwd: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 5fe72282d1b1bcbf602712982e814ef488368122
origin/main: 5fe72282d1b1bcbf602712982e814ef488368122
ahead/behind: 0/0
git diff --name-only: .gitignore; docs/current_status.md; docs/roadmap.md; docs/thread_handoff/pm_operating_rules.md
git diff --cached --name-only: empty
git diff --check: PASS
git diff --cached --check: PASS
config/mapping.yaml relative HEAD: clean
cached index: empty
pre-existing tracked dirty: .gitignore; docs/current_status.md; docs/roadmap.md; docs/thread_handoff/pm_operating_rules.md
network calls: 0
SSH / remote calls: 0
~~~

本任务禁止 network probe、`git ls-remote`、fetch 与任何 remote refresh；local `origin/main` 仅作为用户指定的只读 baseline fact，不被升级为 fresh remote observation。

## 5. Process 与 output-path safety

完成 bounded self-excluding read-only process scan，仅统计实际 Python/helper 或指向
mari@10.0.0.217 的 SSH executable，排除扫描命令自身与 direct parent，并排除编辑器、
文档查看器和 token-only 参数进程：

~~~text
remote_i1_orchestrator.py: 0
remote_preflight.py: 0
remote_upload_exclusive.py: 0
remote_deploy.py: 0
remote_postflight.py: 0
remote_rollback.py: 0
D2-R7B SSH task: 0
task-owned process count: 0
~~~

写入前 output path safety：

~~~text
report path: regular non-symlink file / pre-repair R29-R2 report
docs/reports parent: regular non-symlink directory
~~~

未执行 kill、signal、attach、cleanup 或 retained local root repurpose。

## 6. Exact source identities

四份 R28/R29 source reports 在写入前精确匹配：

~~~text
R28-R1: 10755 bytes / 4e3dcae0fd282d8a9fe0afb94e9c5376ba933045d2825549c63cf55bebda4c12
R28-R1-R1: 7320 bytes / 3bd7f38eb2ce7251a38cbaa4b8ac3328aeb5d831a69cbbdc4413e06b01916bb0
R28-R2: 12618 bytes / 862db8035c1050c93809c616e6b98234835375622e2cd8d65ae0dcae9f7f8702
R29-R1: 7735 bytes / 0ca1795f43a8877484b164bc6fc87fffb8c754b9ce0e1780398a93fee8ad6d0b
~~~

Protected, source and pre-repair identities：

~~~text
R29-R2 report pre-repair: 12329 bytes / f362e789a99bbd72af53c2a5f1ef2a03628293f743ada6a64e8b2389ee666ac1
docs/current_status.md pre-repair: 145490 bytes / e4eefb86555bff74380f94a0492311b1bbe646ab3d43630e36f45d8cfcdf14e4
docs/roadmap.md pre-repair: 10108 bytes / ec2470eedc980c4568e1487c7ca35bc9d5970e9dbf53dda68c1eaeb298c7e66a
docs/current_status.md post-repair: 145805 bytes / 978a755a3d68bdd003832a84f9528f09326cc4543ed22df63b3182403b4ce115
docs/roadmap.md post-repair: 9595 bytes / 30d7e648436baef80ec866c9adbd600bc338677ede82142f14be4c7c3eb717b0
R29-R2 report post-repair: final bytes/SHA-256 returned only in concise window manifest
docs/thread_handoff/pm_operating_rules.md: 40858 bytes / 8e60c07d62e02cda93df5e0447127c226252f2f4a4525c4da996f6aef6fdd7db
.gitignore: 891 bytes / a302455543639fa197b725008240dc24c460505b9f09a0a4cd662bb6ba0bb442
config/mapping.yaml: 7112 bytes / d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
~~~

P2-R2、P2-R3、R26 manifests 分别 fresh verified 为 6/6 PASS、9/9 PASS、3/3 PASS。
Retained local materialization root 仍为 regular non-symlink directory，entries exactly
config 与 config/mapping.yaml；retained mapping 为 7112 bytes、SHA-256
d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d。root、mapping、
manifests、source reports、PM rules 与 .gitignore 均未修改。

## 7. R28/R29 accepted state reconciliation

R28-R1 与 R28-R1-R1：

~~~text
HOLD / SSH invocation 0 / remote NOT_OBSERVED
~~~

两次 HOLD 是历史 fail-closed gate/tooling outcomes，不是 Raspberry Pi、target、Collector
或 remote failure 证据。corrected GitHub rule 已按第 4 节记录：local frozen Git baseline
完整时 git ls-remote best-effort/non-blocking；成功 mismatch 才是 hard blocker。

R28-R2：

~~~text
PASS / PM-VERIFIED / PM-ACCEPTED
classification: RETAINED_R26_UPLOAD_IDENTITY_PROVEN
~~~

R29-R1：

~~~text
PASS / PM-VERIFIED / PM-ACCEPTED
classification: EXACT_R26_UPLOAD_SIDECAR_REMOVED
~~~

Accepted cleanup transaction boundary：

~~~text
remote host/user: Pi-5b-Li / mari / uid 1000
target: /opt/edge-mes-demo/config/mapping.yaml
target: OLD_EXACT / 5935 bytes / SHA-256 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3
R26 upload sidecar: removed / ENOENT
matching D2-R7B sidecars: 0
backup: ABSENT
rollback temp: ABSENT
Collector: edge-mes-collector / running
container ID: 5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524
image: sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
restart count: 0
started_at: 2026-07-23T12:23:25.959624Z
mount: bind /opt/edge-mes-demo/config -> /app/config / RW=false
Collector identity, run state, restart count, started_at and mount: unchanged
~~~

R29-R2 未执行 fresh eligibility，未执行 new config deployment、restart、activation 或
runtime-loaded identity validation；production acceptance 未观察、未建立。R29-R2 remote
call count 为 0，cleanup count 为 0，Collector lifecycle count 为 0。

## 8. Changed-file allowlist 与 diff boundaries

本轮 exact writable allowlist：

~~~text
docs/reports/sprint4_d2_r7b_i1_r29_r2_remote_cleanup_closeout_and_status_sync.md
docs/current_status.md
docs/roadmap.md
~~~

Original R29-R2 attempted to write only the exact three paths but failed closeout validation. R29-R2-R1 modified only the same exact three existing paths; no fourth file, temp, backup, patch artifact, sidecar report or manifest was created.

`docs/current_status.md` only replaces the existing 0H section. 0G and lower historical sections remain byte-for-byte unchanged; its historical projection removes full 0H and restores `141420 bytes / a09ce649519341415fd9cd856007fd94755e20a556248d4e1835ad7244648425`. Its repair reverse projection restores the pre-repair artifact exactly at `145490 bytes / e4eefb86555bff74380f94a0492311b1bbe646ab3d43630e36f45d8cfcdf14e4`.

`docs/roadmap.md` only changes the top `状态：`, the existing 1D section and Section 8 `当前下一步`. Its repair reverse projection restores `10108 bytes / ec2470eedc980c4568e1487c7ca35bc9d5970e9dbf53dda68c1eaeb298c7e66a`; its historical projection restores `8184 bytes / 61b5d706f6b50825bd0fdd63e1ac2b90aaae7869329789e5972b5d5590eb5345`. Data-first MVP and deferred UI acceptance policy remain present.

`.gitignore`、PM rules、四份 R28/R29 source reports、manifests、mapping 与 retained root identities 不变。

## 9. Git、remote、runtime 与 authority separation

~~~text
SSH invocations: 0
remote command / remote filesystem read: 0
remote mutation: 0
Docker/Compose lifecycle: 0
Collector lifecycle: 0
fresh remote eligibility: 0 / NOT RUN
new config deployment: 0 / NOT RUN
runtime-loaded config validation: 0 / NOT OBSERVED
production acceptance: 0 / NOT OBSERVED
Git stage: 0
Git commit: 0
Git push: 0
Git tag: 0
cached index: empty
~~~

network calls: 0
SSH invocations: 0
remote calls / remote filesystem read: 0
remote mutation: 0
Docker/Compose lifecycle: 0
Collector lifecycle: 0
fresh remote eligibility: 0 / NOT RUN
new config deployment: 0 / NOT RUN
runtime-loaded config validation: 0 / NOT OBSERVED
production acceptance: 0 / NOT OBSERVED
Git stage / commit / push / tag: 0 / 0 / 0 / 0
cached index: empty

R28-R2/R29-R1 accepted remote facts do not equal R29-R2-R1 fresh remote observation; historical report evidence, accepted cleanup evidence, local Git facts, deployment, runtime load and production acceptance remain separate.

## 10. Original HOLD 与 R29-R2-R1 repair validation

Original R29-R2 terminal：`HOLD / PM-VERIFIED / PM-ACCEPTED AS FAIL-CLOSED DOCS WRITE`。其 original blockers 是：两个 literal plus headings、report 错误记录 original `PASS`、`Blockers: none` 与 `本轮未触发 HOLD`、status/roadmap final hashes 错误、roadmap Section 8 仍为 R27-era sequence；closeout `NOT CLOSED`。

R29-R2-R1 repair PASS 依据（仅 docs-only self-check）：pre-repair identities exact；cached index empty；`git diff --check` 与 cached check PASS；mapping、protected/source identities exact；P2-R2/P2-R3/R26 manifests 为 `6/6`、`9/9`、`3/3 PASS`；task-owned process `0`；literal `^+## 0H` 与 `^+### 1D` 均 `0 matches`；current-status repair/historical projections exact；roadmap repair/historical projections exact；Section 8 sequence exact；report status/roadmap final hashes exact；final diff checks PASS。

R29-R2-R1 repair blockers：none after the above validations passed。原始 R29-R2 的 `HOLD`、failure history 与 blockers 未被覆盖。recommendations：ChatGPT PM 必须从 actual repository paths 执行 durable intake；之后才可审计 exact eight-path Git candidate set。fresh read-only remote eligibility 必须另行授权，新的 one-shot config-only execution 只在 eligibility PASS 后另行考虑。

唯一 next gate：

~~~text
R29-R2-R1 report/status/roadmap artifacts WRITTEN
→ ChatGPT PM durable intake
~~~

## 11. MVP 路径一致性

~~~text
current MVP support: D2-R7B exact config deployment 的最小安全 remote/Git re-entry boundary 与 durable status truth
minimum invariant: local exact-HEAD identity、accepted cleanup identity、Git/remote/runtime authority separation 不混淆
scope expansion: no
task inflation: no；deferred hardening 仍作为 backlog，不在本轮扩大
classification: MVP-ALIGNED WITH BACKLOG ITEMS
data-first policy: preserved
deferred UI acceptance policy: preserved / non-blocking for current data-first path
~~~

本轮没有新增产品能力、runtime topology、threat model、evidence infrastructure 或生产
acceptance claim；status/roadmap synchronization 只为下一独立 gate 提供 durable truth。

## 12. Thread context assessment 与 delivery state

~~~text
本次输出长度：长（durable report；Chat 仅返回 concise window manifest）
当前 Thread 是否建议继续：no
下一轮是否建议新开 Thread：yes
理由：R29-R2-R1 docs-only repair authority 已消费；下一步是 ChatGPT PM durable intake，之后 exact Git review、Git closeout 与 fresh remote eligibility 必须继续隔离。

Original R29-R2 report: WRITTEN / UNSTAGED / UNCOMMITTED / UNPUSHED / closeout NOT CLOSED
R29-R2-R1 report: WRITTEN / UNSTAGED / UNCOMMITTED / UNPUSHED
docs/current_status.md: WRITTEN / UNSTAGED / UNCOMMITTED / UNPUSHED
docs/roadmap.md: WRITTEN / UNSTAGED / UNCOMMITTED / UNPUSHED
~~~

本轮最多建立 `WRITTEN`。不得自行声明 `PM-ACCEPTED`、`VERIFIED`、`STAGED`、`COMMITTED`、`PUSHED`、`DEPLOYED` 或 `ACTIVATED`。

## 13. R29-R2-R1 repair closeout

```text
changed paths: exact three existing files only
original R29-R2: HOLD / FAIL-CLOSED DOCS WRITE / NOT CLOSED
R29-R2-R1: PASS / WRITTEN only
status post-repair: 145805 bytes / 978a755a3d68bdd003832a84f9528f09326cc4543ed22df63b3182403b4ce115
roadmap post-repair: 9595 bytes / 30d7e648436baef80ec866c9adbd600bc338677ede82142f14be4c7c3eb717b0
report post-repair: actual bytes/SHA-256 returned in the concise window manifest; not self-referenced here
network / SSH / remote / remote mutation: 0 / 0 / 0 / 0
Git staged / committed / pushed: no / no / no
```

The repair restores durable consistency only. It does not close Git, refresh remote eligibility, deploy config, restart or activate Collector, validate runtime-loaded identity, or establish production acceptance.
