# Sprint 4 D2-R7B-I1 R30-I1-R10-R2 Independent Read-Only Remote Collector Lifecycle Observation

## 1. 结论

~~~
REMOTE_LIFECYCLE_OBSERVATION_HOLD
classification: TERMINAL_INCOMPLETE / OBSERVER_SOURCE_CONTRACT_DEFECT
~~~

唯一 SSH 返回 0，observer 也只执行了 1 次；但 observer 没有从 Docker inspect 结果持久化实际 RestartCount。第一、第二 inspect record 的 state.restart_count 均为 null，而本任务明确要求 actual RestartCount 无条件进入 terminal。因此 raw terminal 中表面上的 status=PASS 不能被提升为权威观察 PASS，任务按 terminal-incomplete 规则 HOLD。

本轮没有重试、第二次 SSH、人工 SSH、restart、rollback、recovery、cleanup 或其他远端 mutation。已保留 raw terminal，并将其逐字节复制到 final terminal；两者仍是语义上不完整的同一候选，不构成完整 lifecycle facts authority。

## 2. 报告、任务、Thread 与 authority

~~~
报告名称：Sprint 4 D2-R7B-I1 R30-I1-R10-R2 Independent Read-Only Remote Collector Lifecycle Observation
任务名称：D2-R7B-I1 R30-I1-R10-R2 — Observe and Classify the Unexplained Collector Restart History without Mutation
执行 Thread：Architecture / Integration（独立 Thread）
Authority source / ID：PM-R30-I1-R10-R2-260729-READONLY-LIFECYCLE-OBSERVATION-01
Report delivery mode：REPOSITORY_REPORT_WITH_ARTIFACTS
~~~

唯一报告路径：

~~~
docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_r2_readonly_remote_lifecycle_observation.md
~~~

唯一 artifact 路径：

~~~
docs/reports/evidence/d2_r7b_i1_r30_i1_r10_r2_readonly_remote_lifecycle_observation/lifecycle_observer.py
docs/reports/evidence/d2_r7b_i1_r30_i1_r10_r2_readonly_remote_lifecycle_observation/raw_terminal.ndjson
docs/reports/evidence/d2_r7b_i1_r30_i1_r10_r2_readonly_remote_lifecycle_observation/final_terminal.json
docs/reports/evidence/d2_r7b_i1_r30_i1_r10_r2_readonly_remote_lifecycle_observation/manifest.sha256
~~~

Docs/artifact write authority 仅覆盖以上 exact paths；source、test、product code、config、Git、remote mutation 与 lifecycle authority 均未授予。

## 3. Scope 与 evidence boundary

本轮按任务指定顺序读取 PM Rules、handoff、status、roadmap、R4/R5/R8/R9/R10/R10-R1 reports 与 artifacts、config/mapping.yaml、docker-compose.yml；随后重读 PM Rules Sections 10–13，才创建 observer 并执行 SSH。

本轮目标是 bounded read-only lifecycle observation，不建立以下事实：

- CONFIG_RUNTIME_LOADED、RESTARTED、ROLLED_BACK、RECOVERED、NEW_IMAGE_ACTIVATED；
- Collector 健康 PASS、production accepted fact、production acceptance；
- 绝对 root cause；
- Git STAGED、COMMITTED 或 PUSHED。

由于 actual RestartCount 未被 observer 写入 terminal，本轮连完整 lifecycle facts authority 也未建立。下文的 remote fields 是 raw candidate 中可见的 partial observation，必须与最终 HOLD 区分。

## 4. Fresh local baseline

SSH 前 live recovery：

~~~
checkout: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 1fac3ee567f1108e5a18b155e4133e1fecd50246
origin/main: 1fac3ee567f1108e5a18b155e4133e1fecd50246
HEAD^: 63d3cc70e787e0c837079aec0f5924dcbfa6a668
ahead/behind: 0/0
cached: empty
tracked dirty: exactly six pre-existing paths
~~~

六项 pre-existing tracked dirty paths：

~~~
.gitignore
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
docs/thread_handoff/pm_operating_rules.md
~~~

config/mapping.yaml relative to HEAD clean；blob 为 b46a637f23c761d0a4c3fe048b3b7480a3dec2ce，7112 bytes，SHA-256 为 d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d。

output collision gate 在 observer 创建前通过：本轮 exact report、artifact parent、observer、raw、final、manifest 均为 ABSENT / NON-SYMLINK。冻结的 initial untracked set 也匹配：13786，sorted NUL-delimited SHA-256 5fbc13305d87999661080925d8d8d1de707d129b1c3f38d507e5bb2d3be33fef。

P2/cache/process/credential gates：

- P2-R2 manifest：528 bytes，SHA-256 30aabc24d931813069756c61d58d5ea3f8e6207ea1927f03f88c95f51e384a85，6/6 OK；P2-R3 manifest：1122 bytes，SHA-256 45d8205aa37f8f5b9e1ec43bdcf7b68e752ff9ea169ef69b2594508d907f94ce，9/9 OK；
- P2-R2/P2-R3 scoped cache：0 __pycache__ / 0 *.pyc；
- /bin/ps -axo pid=,ppid=,command= self/ancestor/ps-child excluding scan：task matches 0；
- SSH key /Users/chenjie/.ssh/edge_pi_codex：regular non-symlink，uid 501，mode 0600；内容未读、未 hash、未复制、未打印；
- resolved endpoint：mari@10.0.0.217，port 22，identity file exact，无 ProxyCommand/ProxyJump。

## 5. Prior evidence identity

本轮只读确认了 prior artifacts 未漂移：

| Evidence | Bytes | SHA-256 |
| --- | ---: | --- |
| R8 report | 8429 | 0c1cc78b0a24c9e80ef3ac4538efa8391ff501154b9d18439fa01004679da0ff |
| R8 raw/final | 13025 each | f2baa8ca164341286411efea601f94fa4c8d636f2a8ae9c10cbcf2701decf5b0 |
| R8 manifest | 498 | d60c0bbe99821a629df2137c365b3f6c1d494fdcb58dfcba150020f7dee95658 |
| R9 report | 17260 | a7542bd7ee7459f56c6671a03198a44245c22aa639a3207b3758cd8676f2ba91 |
| R10 report | 9593 | 92595578a084e07429c508b5a1d0cce8608e276a233a06752ad0cb26320d7713 |
| R10-R1 report | 7743 | 6e115591ff85eee492b43c3205cd95373f58cde8c6075271b630f7da69e3f980 |
| R10-R1 controller | 50012 | 4d21b637a0b30a335bb0ef904847743706e7344b39e305f141a060da4fbdb668 |
| R10-R1 raw/final | 572 each | 6fa6f8541b9a260446aa596e8260b03a419552e2f38e56ff0369ee2ffbf6a83a |
| R10-R1 manifest | 744 | 496d11a614308aee3d9a5aa7dd6014422848e50680763a7896ff7e5fb6d06e45 |

R10-R1 的历史边界是 REMOTE_PRESTATE_MISMATCH，只观察到 RestartCount 非零但没有持久化数值；该 authority 未被继承，也没有从它推断本轮 actual count。

## 6. Observer identity 与 static audit

Observer：docs/reports/evidence/d2_r7b_i1_r30_i1_r10_r2_readonly_remote_lifecycle_observation/lifecycle_observer.py。

~~~
bytes: 31433
SHA-256: 6e3b69d37f5b63b3dad2bfa6d3c0597080dd7ed7ca611a0873baa60760dea9a2
AST parse: PASS
compile: PASS
subprocess.run calls: 1
shell=True: 0
filesystem write-capable calls: 0
Docker command guard: inspect/logs/events allowlist enforced
retry/resume loops: 0
terminal emission calls: exactly 1
fixed endpoint/host/container/historical ID: PASS
observer import/execute/dry-run before SSH: NOT RUN
~~~

Observer 使用 Python standard library、list-based subprocess 与 shell=False；没有 remote temp/helper、secret/environment dump、DB/API/PLC/Simulator access、Docker lifecycle command、write/open-for-write/remove/rename/chmod/chown。Static audit 完成后 source identity 未变化。

## 7. SSH 与 mutation accounting

~~~
SSH parent count: 1
observer execution count: 1
SSH exit: 0
retry: 0
resume: 0
second SSH: 0
manual SSH: 0
restart by task: 0
rollback: 0
recovery: 0
remote file writes: 0
cleanup: 0
~~~

Remote command surface 仅为 observer 内的 read-only docker inspect、docker logs、docker events、systemctl show docker 与 /proc/exact config reads。没有 Compose、restart、stop/start、exec、cp、image/tag、DB/API/PLC、sudo/elevation 或 background process。

## 8. Partial remote facts observed by the invalid terminal

### 8.1 Host and Docker

~~~
hostname: Pi-5b-Li
principal: mari
/usr/bin/docker: regular non-symlink, uid 0, mode 0755, executable, group/other writable false
docker device/inode: 2050/59474
host boot ID: 1bf8008b-cb38-4353-8ab4-061282ab2473
host boot UTC: 2026-06-14T05:35:34.000Z
uptime seconds: 3888093.68
boot/uptime internal consistency: PASS, delta 0.67s
observation UTC: 2026-07-29T05:37:08.350Z
Docker daemon: AVAILABLE
ActiveEnterTimestamp: Sun 2026-06-14 13:54:10 CST
ExecMainStartTimestamp: Sun 2026-06-14 13:54:09 CST
~~~

Collector StartedAt 在 2026-07-23，明显不在 host boot 或 Docker daemon start 的 120 秒窗口内；observer flags 为 HOST_BOOT_CORRELATION_PRESENT=false 与 DOCKER_DAEMON_START_CORRELATION_PRESENT=false。这只是时间关系，不能用于因果结论。

### 8.2 Config / backup / sidecar relation

| Object | State | Bytes | SHA-256 | Device/inode | Owner/group/mode |
| --- | --- | ---: | --- | --- | --- |
| target mapping.yaml | NEW_EXACT | 7112 | d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d | 2050/550822 | mari/mari/0644 |
| exact backup | OLD_EXACT | 5935 | 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3 | 2050/550916 | mari/mari/0644 |
| upload sidecar | ABSENT | — | — | — | — |
| rollback temp | ABSENT | — | — | — | — |

Target、backup 均 regular non-symlink，realpath exact；config parent 是 regular directory，device/inode 2050/518154，mari/mari/0775。Config drift 未被用作本轮 pre-terminal HOLD，也没有修复。

### 8.3 Collector first complete-shaped record

Name discovery 成功：docker inspect edge-mes-collector exit 0；observed ID 为 historical exact ID，因此没有执行 historical-ID fallback。

第一、第二样本中除 reference 字段外的 lifecycle tuple 相同：

~~~
Id: 5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524
historical ID match: true
Name: edge-mes-collector
Image: sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
historical image match: true
Config.Image: edge-mes-demo-collector
Compose project/service: edge-mes-demo / collector
Created: 2026-07-23T12:23:25.124184859Z
StartedAt: 2026-07-23T12:23:25.959624Z
FinishedAt: 0001-01-01T00:00:00Z
Status/running/paused/restarting/dead: running / true / false / false / false
PID: 3365014
ExitCode: 0
OOMKilled: false
Error: empty
Restart policy: unless-stopped / MaximumRetryCount=0
Health: absent
Mount: bind /opt/edge-mes-demo/config -> /app/config, rw=false
~~~

关键缺失：

~~~
first State.RestartCount: null
second State.RestartCount: null
actual RestartCount: NOT_OBSERVED
~~~

这不是“RestartCount 为 null”的产品事实；这是 observer 从 Docker inspect schema 读取错误位置、没有持久化 actual field 的 source defect。由于任务要求实际数值无条件进入 terminal，第一完整 lifecycle record 和第二样本均不能成为 authoritative record。

### 8.4 Stability, logs and events

Observer candidate 给出的 comparison 为 STABLE，changed fields 为空，且 exact 6-second wait 只执行一次；但该 stability result 仍受 RestartCount 缺失影响，不能替代完整 lifecycle fact。

Bounded logs：

~~~
command: docker logs --timestamps --tail 1000 <observed ID>
exit: 0
stdout bytes/SHA: 0 / e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
stderr bytes/SHA: 136456 / 3c23769bf7585612962142035a6d27d5ec57dedeac2b8266209862fb9483146f
line count: 1000
timestamp range: 2026-07-29T05:21:54.646322403Z .. 2026-07-29T05:37:13.723242765Z
startup markers: 0
fatal/error matches: 0
PLC/DB diagnostics: 0
~~~

Bounded Docker events：

~~~
command exit: 0
window: 7 days, exact current-container filter
state: NO_RETAINED_EVENTS
event count: 0
invalid lines: 0
stdout bytes/SHA: 0 / e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
restart/die/start/oom evidence: none observed
~~~

NO_RETAINED_EVENTS 不证明没有发生过 restart。日志没有 startup/fatal evidence 也不证明绝对 root cause 不存在。

## 9. Cause assessment boundary

Raw candidate 的 provisional lifecycle finding 为 ROOT_CAUSE_NOT_DETERMINED，所有 direct/correlation evidence flags 为 false：

~~~
EXPLICIT_DOCKER_RESTART_EVENT_PRESENT: false
DIE_START_SEQUENCE_PRESENT: false
OOM_EVIDENCE_PRESENT: false
NONZERO_EXIT_EVIDENCE_PRESENT: false
HOST_BOOT_CORRELATION_PRESENT: false
DOCKER_DAEMON_START_CORRELATION_PRESENT: false
ACTIVE_RESTART_LOOP_PRESENT: false
STARTUP_FAILURE_LOG_EVIDENCE_PRESENT: false
STABLE_NONZERO_RESTART_COUNT: false (actual count missing)
~~~

本轮不能建立 ROOT_CAUSE_ESTABLISHED，也不能把 mapping、PLC/DB diagnostics、空 events 或 stable partial tuple 解释成 restart cause。因为 actual RestartCount 缺失，连“稳定非零计数”的分类也不能成立；candidate 的 ROOT_CAUSE_NOT_DETERMINED 仅为不越界的 provisional label。

## 10. Raw/final terminal contract

~~~
raw_terminal.ndjson: 1 line, 1 non-empty record, valid JSON, trailing LF
raw bytes: 16896
raw SHA-256: bf3e535b75e06c8fbcf7f36fa4b1afaa078fddec40d362e375fb07eb2827e41f
final_terminal.json: exact byte copy of raw
final bytes: 16896
final SHA-256: bf3e535b75e06c8fbcf7f36fa4b1afaa078fddec40d362e375fb07eb2827e41f
raw/final cmp: PASS
terminal candidate status: PASS (observer emitted)
authoritative terminal: false (required RestartCount field absent)
~~~

Raw terminal 的 PASS / REMOTE_LIFECYCLE_FACTS_OBSERVED / FINAL_TERMINAL / manual_action_required=false 不足以覆盖本任务 terminal contract；semantic completeness gate 优先于 observer 自报状态。

## 11. Final local audit and delivery state

At the point before report creation，untracked set was 13789，sorted NUL SHA-256 a6fd3798d413dfd1cab335b308d394d2a3f232ccc928c15e76c30f5a3980aec5（initial set + observer + raw + final）。此报告和 manifest 也只创建于 exact allowlist；没有 placeholder、alternative output、source/test/config modification 或 Git mutation。

本轮最终 audit 已确认：

- final untracked set 为 13791，sorted NUL SHA-256 942acd5e70d70c29358d44c24b46b7eb3773f1db987d0b36a7566dcdc39ab20e；剔除本轮五个 exact authorized paths 后，剩余集合为 initial 13786 / 5fbc13305d87999661080925d8d8d1de707d129b1c3f38d507e5bb2d3be33fef；
- HEAD/origin/main 仍为 1fac3ee567f1108e5a18b155e4133e1fecd50246；ahead/behind 0/0；cached empty；tracked dirty 仍 exact six；mapping clean；
- observer 31433 bytes / 6e3b69d37f5b63b3dad2bfa6d3c0597080dd7ed7ca611a0873baa60760dea9a2、raw/final 各 16896 bytes / bf3e535b75e06c8fbcf7f36fa4b1afaa078fddec40d362e375fb07eb2827e41f 未漂移；
- manifest 为 path-sorted、unique、self-excluded，4/4 OK；P2 manifests/cache、mapping、stage roots、/bin/ps process gate 均未漂移；
- no second network call、no remote mutation、no task-owned process remains。

## 12. Blockers and next gate

Blocker：lifecycle_observer.py projects Docker RestartCount from the wrong inspect location, so actual RestartCount is not persisted. This is a terminal/source contract blocker, not a Collector root-cause claim.

Recommendations：none within this consumed authority. Observer repair、static re-audit、second SSH、manual observation、restart or any diagnostic expansion requires a fresh PM task and new authority。

唯一 next gate：

~~~
ChatGPT PM durable intake only
~~~

本任务的 HOLD 不授权 observer repair、new SSH、restart、rollback、recovery、cleanup、config mutation、runtime validation、production acceptance 或 Git closeout。R10 restart gate 不能由本轮重新发放。

## 13. Prohibited-action audit

~~~
restart/stop/start/rollback/recovery/recreate/image-tag mutation: 0
remote file writes: 0
DB/API/PLC/Simulator: 0
logs follow / events follow: 0
second SSH / retry / resume / manual SSH: 0
sudo/elevation: 0
Git stage/commit/push/tag/reset/restore/checkout/stash/clean: 0
private-key contents access: 0
~~~

## 14. MVP 路径一致性

~~~
classification: MVP-ALIGNED WITH BACKLOG ITEMS
approved deliverable: explain unexplained Collector restart history using bounded read-only evidence
minimum truth invariant: actual lifecycle facts must be persisted before classification
new product capability: none
new generic monitoring/forensics framework: none
task inflation: no
stopping rule: applied at first terminal-contract blocker; no retry or expansion
~~~

本任务直接服务于已批准的数据-first Collector/runtime safety path；本轮发现的 observer defect 不能通过扩大监控或诊断框架解决。

## 15. Thread 输出 / 上下文评估

~~~
本次输出长度: 长（完整 durable HOLD report + exact artifacts）
当前 Thread 是否建议继续: no
下一轮是否建议新开 Thread: yes
理由: 唯一 SSH 已消费，且 terminal incomplete；任何 repair、second SSH 或 lifecycle action 需要新的 PM authority
~~~

## 16. Delivery state

~~~
WRITTEN: report/artifacts only
REVIEWED: local final audit after artifact closure
ACCEPTED: not established
VERIFIED: not established
STAGED/COMMITTED/PUSHED: no/no/no
DEPLOYED/ACTIVATED/RUNTIME-LOADED/PRODUCTION-ACCEPTED: no/no/no/no
~~~
