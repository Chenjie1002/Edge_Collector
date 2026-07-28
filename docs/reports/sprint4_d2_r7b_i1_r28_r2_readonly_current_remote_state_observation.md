# Sprint 4 D2-R7B-I1 R28-R2 Read-Only Current Remote State Observation

## 1. 报告身份与结论

~~~text
报告名称：Sprint 4 D2-R7B-I1 R28-R2 Read-Only Current Remote State Observation
任务名称：D2-R7B-I1 R28-R2 — Read-Only Current Remote State Observation with Non-Blocking GitHub Reachability
执行 Thread：Architecture / Integration
Authority ID：PM-R28-R2-260728-REMOTE-READ-01
项目绝对路径：/Users/chenjie/Documents/MES/edge-mes-demo
Report delivery mode：REPOSITORY_DURABLE_REPORT
Exact report path：docs/reports/sprint4_d2_r7b_i1_r28_r2_readonly_current_remote_state_observation.md
Exact artifact paths：none
~~~

报告写前已确认：report path 为 ABSENT / NON-SYMLINK，docs/reports 为 regular non-symlink directory。

结论：PASS。该 PASS 仅表示本轮 local hard gate、一次只读 SSH observation、远端身份分类与 exact durable report 写入均完成；不表示 cleanup、eligibility、upload、deployment、restart、activation、runtime-load validation、production acceptance 或 Git closeout 已完成。

报告文件最终字节数：12618
报告 SHA-256（canonical projection；完整文件 SHA-256 见窗口 manifest）：7c847906a1b5267672ceba0a0a6f41d6daca3e3ccc64285cbfdec0be3ddbb725

## 2. Authority 与消费状态

~~~text
DOCS-REPORT-AUTHORITY:
CONSUMED BY THIS FIRST EXACT REPORT WRITE

REMOTE-OBSERVATION-AUTHORITY:
CONSUMED WHEN THE UNIQUE SSH PARENT STARTED

remote mutation budget: 0
SSH parent invocation budget: 1 maximum / 1 used / no retry
~~~

SSH 启动后未启动第二次 SSH、retry/resume 或 supplemental probe。报告写入不授权 remote mutation 或 Git write。

## 3. Required reading 与 non-inheritance

以下路径已按指定顺序完成只读读取；完成后重新读取 pm_operating_rules.md Section 10 与 Section 11：

1. docs/thread_handoff/pm_operating_rules.md
2. docs/current_status.md
3. docs/roadmap.md
4. docs/thread_handoff/chatgpt_pm_handoff_260728-1117.md
5. docs/reports/sprint4_d2_r7b_i1_r28_r1_readonly_current_remote_state_refresh.md
6. docs/reports/sprint4_d2_r7b_i1_r28_r1_r1_readonly_current_remote_state_refresh.md
7. docs/reports/sprint4_d2_r7b_i1_r27_r6_local_gate_closeout_and_status_sync.md
8. docs/reports/sprint4_d2_r7b_i1_r27_r6_r1_eof_identity_repair.md
9. docs/reports/sprint4_d2_r7b_i1_r26_exact_config_only_remote_execution.md
10. docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/final_terminal.json
11. docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/manifest.sha256
12. docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
13. docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
14. config/mapping.yaml

R28-R1/R28-R1-R1 仅为 prior HOLD evidence；R26 HOLD_UPLOAD_INTERRUPTED / UPLOAD_STAGED_NO_REPLACEMENT 仅为 retained historical terminal。live facts 以本报告的 fresh checks 为准。

## 4. Fresh local hard gate

~~~text
project: /Users/chenjie/Documents/MES/edge-mes-demo
pwd: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 5fe72282d1b1bcbf602712982e814ef488368122
origin/main: 5fe72282d1b1bcbf602712982e814ef488368122
ahead/behind: 0/0
cached index: empty
git diff --check: PASS
git diff --cached --check: PASS
config/mapping.yaml relative HEAD: clean
~~~

Recent commit：5fe7228 Close D2-R7B R27 local contract gate。写前 pre-existing tracked dirty files 为 .gitignore、docs/thread_handoff/pm_operating_rules.md；既有 untracked reports/evidence/handoffs/frontend artifacts 均保留，未清理、未 broad stage、未重新分类。

## 5. GitHub best-effort reachability

只执行一次 git ls-remote origin refs/heads/main：

~~~text
exit: 0
result: 5fe72282d1b1bcbf602712982e814ef488368122 refs/heads/main
GitHub remote main: VERIFIED / MATCH
blocking: no
retry: 0
~~~

该结果未授权 fetch、stage、commit、push、tag 或 remote mutation。

## 6. Local identities 与 preflight

### 6.1 Mapping and manifests

~~~text
config/mapping.yaml: regular non-symlink / 7112 bytes
SHA-256: d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
HEAD blob: b46a637f23c761d0a4c3fe048b3b7480a3dec2ce

P2-R2 manifest: 6 entries / 6 PASS
SHA-256: 2ae13bd6dc17167f98d2d59efd882e8a568d5c0ae6f36cbbb9ecb6f2d21086dd
P2-R3 manifest: 9 entries / 9 PASS
SHA-256: 8e5e99f5e52e87a6945b692ca8808b518e6cd360c84191f08aa9bf1d992f95c8
R26 manifest: 3 entries / 3 PASS
SHA-256: 257fb2945155d49e40638ea1dfedd4cc95aee127dca6a38fc7d72a8e8f362670
R26 terminal: HOLD_UPLOAD_INTERRUPTED / UPLOAD_STAGED_NO_REPLACEMENT / authority consumed / terminal
~~~

P2-R2、P2-R3、R26 manifest 均用 shasum -a 256 -c 逐项 fresh verified。

### 6.2 Retained local stage root

~~~text
root: /private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r2.0mW7V5
root: regular non-symlink directory / owner chenjie / uid 501 / mode 0700
entries exactly: config; config/mapping.yaml
config/mapping.yaml: regular non-symlink / owner chenjie / uid 501 / mode 0600
bytes: 7112
SHA-256: d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
~~~

该 root 只做 read-only identity check，未使用、修改、复制、删除或清理。

### 6.3 SSH key and local process preflight

~~~text
key: /Users/chenjie/.ssh/edge_pi_codex
type: regular non-symlink / owner chenjie / uid 501 / mode 0600
private-key contents: not read / not printed / not copied / not hashed

primitive: bounded pgrep -af per frozen token, excluding self/direct parent/pgrep child
task-owned active process count: 0
~~~

Frozen tokens：remote_i1_orchestrator.py、remote_preflight.py、remote_upload_exclusive.py、remote_deploy.py、remote_postflight.py、remote_rollback.py、D2-R7B-I1、mari@10.0.0.217、.mapping.yaml.d2-r7b-new。

## 7. Unique SSH observation

### 7.1 Invocation and stdout

~~~text
endpoint: mari@10.0.0.217:22
identity: /Users/chenjie/.ssh/edge_pi_codex
SSH parent invocation count: 1
SSH exit: 0
retry/resume/second SSH: 0
observer schema: d2-r7b-i1-r28-r2-readonly-observer/v1
stdout: one complete JSON object
observer errors: none
remote mutation reported by observer: 0
~~~

observer 通过 stdin 执行，未创建远端文件/temp，未使用 sudo、secret/environment dump、shell redirection 或 shell=True。唯一外部 command 为 docker inspect edge-mes-collector。

### 7.2 Observer identity

~~~text
observed_at UTC: 2026-07-28T05:47:45.548677+00:00
hostname: Pi-5b-Li
uid/user: 1000 / mari
observer self/direct parent: 1002619 / 1002618
~~~

### 7.3 Remote filesystem identities

Config parent：

~~~text
path: /opt/edge-mes-demo/config
state: REGULAR_DIRECTORY / realpath exact
owner/group: mari/mari / uid/gid 1000/1000
mode: 0775
device/inode: 2050/518154
mtime_ns/ctime_ns: 1785198414121139902 / 1785198414121139902
stable_during_observation: true
~~~

Target：

~~~text
path: /opt/edge-mes-demo/config/mapping.yaml
state: REGULAR_FILE / non-symlink / stable
realpath: /opt/edge-mes-demo/config/mapping.yaml
bytes: 5935
SHA-256: 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3
owner/group: mari/mari / uid/gid 1000/1000 / mode 0644
device/inode: 2050/550698
mtime_ns/ctime_ns: 1781794248000000000 / 1781834419097910641
fstat before/after: same dev, inode, size, mode, mtime_ns, ctime_ns
~~~

R26 upload candidate：

~~~text
path: /opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-new.8de5edb
state: REGULAR_FILE / non-symlink / stable
realpath: /opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-new.8de5edb
bytes: 7112
SHA-256: d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
owner/group: mari/mari / uid/gid 1000/1000 / mode 0644
device/inode: 2050/550822
mtime_ns/ctime_ns: 1785198414121139902 / 1785198414121139902
fstat before/after: same dev, inode, size, mode, mtime_ns, ctime_ns
~~~

Backup：

~~~text
/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml
state: ABSENT
~~~

Rollback temp：

~~~text
/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml
state: ABSENT
~~~

### 7.4 Sidecars and remote task processes

只列出 config parent 直接 children 中匹配 .mapping.yaml.d2-r7b-* 的名称：

~~~text
matching sidecars: 1
only: /opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-new.8de5edb
sidecar identity: same as exact R26 upload candidate above
~~~

remote observer 只读 /proc，排除 observer/direct parent，task token matches 为：

~~~text
remote task-owned process count: 0
matches: []
scan errors: []
~~~

### 7.5 Collector bounded identity

~~~text
exists: yes
id: 5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524
name: /edge-mes-collector
state/status: running / running
running: true
image ID: sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
configured image: edge-mes-demo-collector
restart count: 0
started_at: 2026-07-23T12:23:25.959624Z
mount: bind /opt/edge-mes-demo/config -> /app/config / RW=false
~~~

## 8. Classification 与 gate decision

Classification：RETAINED_R26_UPLOAD_IDENTITY_PROVEN。

A 类全部条件满足：target exact old identity stable；upload exact R26 identity stable；backup/rollback absent；matching sidecars only exact upload；local/remote task-owned process count 0；Collector running 且历史 image、mount、restart count、started_at unchanged。

因此本轮 gate 为 PASS。该分类只证明 retained upload 的 task-owned identity，可供 PM 另行评估 cleanup；不授权 cleanup。

~~~text
R26 retained upload identity proven: yes
Cleanup candidate: yes / exact upload sidecar only
Cleanup authorized: NO
Eligibility authorized: NO
Runtime-loaded config identity: NOT_OBSERVED
Production state: NOT_OBSERVED
~~~

## 9. Mutation audit 与禁止边界

~~~text
remote filesystem mutation: 0
Docker/Compose lifecycle: 0
Collector lifecycle: 0
cleanup: 0
upload/deploy/rollback: 0
restart/activation: 0
runtime-load validation: 0
production acceptance: 0
Git stage/commit/push/tag: 0 / 0 / 0 / 0
repository writes other than this exact report: 0
~~~

本任务不授权 cleanup、fresh eligibility、upload、deployment、rollback、restart/activation、runtime-load、production acceptance、status/roadmap/handoff/source/test/manifest 修改或任何 Git write。

## 10. Final local audit

报告写入后重新执行 live local audit：

~~~text
HEAD: 5fe72282d1b1bcbf602712982e814ef488368122
origin/main: 5fe72282d1b1bcbf602712982e814ef488368122
ahead/behind: 0/0
cached index: empty
git diff --check: PASS
git diff --cached --check: PASS
config/mapping.yaml relative HEAD: clean
local task-owned process count: 0
~~~

.gitignore、docs/thread_handoff/pm_operating_rules.md 及既有 untracked artifacts 保持 task 前状态；未发生 broad cleanup 或 Git mutation。task-owned changed path 仅为：

~~~text
docs/reports/sprint4_d2_r7b_i1_r28_r2_readonly_current_remote_state_observation.md
~~~

## 11. Blockers、recommendations 与 next gate

Blockers：none。

Recommendations：

1. 将本报告提交 ChatGPT PM durable remote-state intake；保持 WRITTEN / NOT YET PM-ACCEPTED / UNSTAGED / UNCOMMITTED / UNPUSHED。
2. 如 PM 需要处理 A 类 retained upload，只能另行授权 cleanup-only Level 2 mutation；本报告不授予删除权限。
3. Cleanup 后如需继续，必须另行执行 fresh read-only eligibility；本报告不授予 eligibility、upload 或 deployment。

唯一 next gate：

~~~text
R28-R2 report WRITTEN
→ ChatGPT PM durable remote-state intake
~~~

## 12. MVP 路径一致性

~~~text
当前任务是否仍直接服务于已批准 MVP: yes
对应 MVP 交付物或验收声明: D2-R7B exact config deployment 重新进入 remote gate 前的 retained-artifact identity 与 fail-closed boundary
是否引入超出 MVP 的产品能力、威胁模型、证据体系或基础设施: no
是否出现任务膨胀或验证框架替代产品交付: no
MVP classification: MVP-ALIGNED
~~~

## 13. Thread context assessment 与 delivery state

~~~text
本次输出长度: 长（durable report；Chat 返回 concise manifest）
当前 Thread 是否建议继续: no
下一轮是否建议新开 Thread: yes
理由: 本轮 SSH 与 report authority 均已消费；下一步是 PM durable intake，后续 cleanup/eligibility/deployment/Git 必须获得独立 authority。

R28-R2 artifacts:
WRITTEN
NOT YET PM-ACCEPTED
UNSTAGED
UNCOMMITTED
UNPUSHED

Current remote state:
OBSERVED READ-ONLY

Remote mutation:
NONE
~~~

本报告不代表 REVIEWED、ACCEPTED、VERIFIED、STAGED、COMMITTED、PUSHED、DEPLOYED 或 ACTIVATED。
