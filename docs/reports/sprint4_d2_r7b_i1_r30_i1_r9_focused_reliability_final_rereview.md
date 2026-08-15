# Sprint 4 D2-R7B-I1 R30-I1-R9 Focused Reliability Final Re-Review

## 1. 报告身份、authority 与结论

- 报告名称：Sprint 4 D2-R7B-I1 R30-I1-R9 Focused Reliability Final Re-Review
- 任务名称：D2-R7B-I1 R30-I1-R9 — Focused Reliability Final Re-Review of the Exact Successful Config-Only Deployment
- 执行 Thread：Reliability
- Authority source / ID：PM-R30-I1-R9-260729-FOCUSED-RELIABILITY-01
- Report delivery mode：REPOSITORY_DURABLE_REPORT
- Exact report path：docs/reports/sprint4_d2_r7b_i1_r30_i1_r9_focused_reliability_final_rereview.md
- Exact artifact paths：none
- Docs write authority：本 exact report path 一次性授权；source、test、manifest、mapping、external filesystem、remote 与 Git write 均未授权。

结论：RELIABILITY_PASS_WITH_RECOMMENDATIONS

Delivery state：REVIEWED / WRITTEN

本报告只审查 R30-I1-R8 已持久化的 exact config-only deployment evidence、当前持久化 package/source 与其 fail-closed 控制流。它不建立或继承 VERIFIED、RE-EXECUTED、REMOTE-OBSERVED、RUNTIME-LOADED、RESTARTED、ACTIVATED、PRODUCTION-ACCEPTED、STAGED、COMMITTED 或 PUSHED。

## 2. Scope、required reading 与 evidence boundary

按授权顺序读取了：

- docs/thread_handoff/pm_operating_rules.md，包括 Sections 9–13；
- docs/thread_handoff/chatgpt_pm_handoff_260728-2152.md；
- docs/current_status.md；
- docs/roadmap.md；
- R24-R2、R26、R29-R1、R30-P1、R30-I1-R5、R30-I1-R6、R30-I1-R7 与 R30-I1-R8 durable reports；
- R30-I1-R8 raw_terminal.ndjson、final_terminal.json 与 manifest.sha256；
- P2-R2/P2-R3 current package manifests、local materializer、四个 phase helpers、rollback helper、orchestrator、postflight 与 config/mapping.yaml。

在所有指定资料读取完成后，重新读取了 PM Rules Section 10、11、12、13，然后才开始正式 review 与 report write。

本轮仅执行 read-only Git/status/hash/manifest/JSON/static AST/shell-syntax/process/stage-root checks。没有执行 package、helper、orchestrator、test、pytest、SSH、network、remote observation、remote mutation、cleanup、rollback、restart、activation、DB/API/Dashboard/V-PLC 或 Git mutation。

## 3. Fresh repository baseline

Fresh recovery cwd：/Users/chenjie/Documents/MES/edge-mes-demo

- root: /Users/chenjie/Documents/MES/edge-mes-demo
- branch: main
- HEAD: 1fac3ee567f1108e5a18b155e4133e1fecd50246
- origin/main: 1fac3ee567f1108e5a18b155e4133e1fecd50246
- HEAD parent: 63d3cc70e787e0c837079aec0f5924dcbfa6a668
- ahead/behind: 0/0
- cached: empty
- git diff --check: PASS
- git diff --cached --check: PASS

Current tracked dirty set 精确为以下六项，均为本轮排除的 pre-existing dirty artifact：

- .gitignore
- docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
- docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
- docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
- docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
- docs/thread_handoff/pm_operating_rules.md

config/mapping.yaml relative to HEAD 为 clean：

- HEAD blob: b46a637f23c761d0a4c3fe048b3b7480a3dec2ce
- bytes: 7112
- SHA-256: d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d

R9 report path 在任何 review/write 前为 ABSENT / NON-SYMLINK。初始 untracked set：

- count: 13779
- sorted NUL-delimited path-set SHA-256: b164e7ef38abfb09be41e079cf6f8139f2f3aa2ef698a92b95ab3157d1af6aa8

本轮没有 stage、commit、push、tag、reset、restore、checkout、stash 或 clean。

## 4. Durable R8 evidence identity

R30-I1-R8 current identities 与授权冻结值一致：

- report：8429 bytes；SHA-256 0c1cc78b0a24c9e80ef3ac4538efa8391ff501154b9d18439fa01004679da0ff
- raw_terminal.ndjson：13025 bytes；SHA-256 f2baa8ca164341286411efea601f94fa4c8d636f2a8ae9c10cbcf2701decf5b0
- final_terminal.json：13025 bytes；SHA-256 f2baa8ca164341286411efea601f94fa4c8d636f2a8ae9c10cbcf2701decf5b0
- manifest.sha256：498 bytes；SHA-256 d60c0bbe99821a629df2137c365b3f6c1d494fdcb58dfcba150020f7dee95658

R8 artifact parent only contains final_terminal.json、manifest.sha256、raw_terminal.ndjson。

R8 manifest is sorted、unique、self-excluded，exactly 3 entries，3/3 OK。R8 raw and final are byte-for-byte equal and semantically equal。

## 5. R1 — Durable evidence identity and authority

判定：PASS。

Fresh identity audit established：

- R8 report/raw/final/manifest all exist as regular non-symlink files with the frozen identities；
- artifact parent has no second terminal、copy、log、transcript、sidecar 或 extra manifest；
- R8 manifest binds exactly the final terminal、raw terminal 与 report and excludes itself；
- raw/final relation is exact byte equality, not summary reconstruction；
- R8 report 的 CONFIG_DEPLOYMENT_PASS / CONFIG_DEPLOYED_IDENTITY_VERIFIED / EXECUTED / REMOTE_STATE_OBSERVED wording matches the authoritative terminal and explicitly excludes runtime load、restart、activation and production acceptance；
- current Git/package/cache/process final boundary is unchanged before this R9 report write；
- the only newly authorized repository path in this task is the exact R9 report path。

No evidence identity drift、second authoritative source or summary-over-terminal substitution was found。

## 6. R2 — Terminal delivery authority

判定：PASS。

Raw terminal facts：

- non-empty records: 1
- valid JSON records: 1
- invalid/partial records: 0
- authoritative candidates: 1
- raw/final exact bytes: equal
- terminal_delivery_attempt: 1
- terminal_delivery_status: PRIMARY
- terminal_delivery_authoritative: true
- terminal_delivery_framing: NDJSON
- terminal_delivery_fallback: false
- terminal_primary_delivery_interrupted: false
- terminal_stream_prefix_may_be_partial: false

The selected terminal is unambiguous。Semantic authority fields are internally consistent：

- status: CONFIG_DEPLOYED_IDENTITY_VERIFIED
- classification: DEPLOYED_IDENTITY_VERIFIED
- phase: FINAL_TERMINAL
- message: RUNTIME CONFIG LOAD NOT CLAIMED

No partial、fallback、interrupted 或 ambiguous terminal was promoted to success。

## 7. R3 — Source/evidence binding

判定：PASS。

R8 local_source binds the displayed execution source to the persisted current bytes：

- baseline branch: main
- baseline HEAD/origin: 1fac3ee567f1108e5a18b155e4133e1fecd50246 / 1fac3ee567f1108e5a18b155e4133e1fecd50246
- ahead/behind: 0/0
- mapping blob: b46a637f23c761d0a4c3fe048b3b7480a3dec2ce
- mapping bytes/SHA-256: 7112 / d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
- composite manifest: 9 entries / 9/9 OK

Current persisted package identities matched the terminal/manifest binding：

- local_materialization.sh：2653 bytes；SHA-256 5e7b4991d29921472c16dec2cf655cb744a204bd16723c236df50c15e5de65ef
- remote_preflight.py：11129 bytes；SHA-256 6ddae658ed30ba38c20dcd3fa29fa9719cb940f3c8da4b904c6dfae810061f9c
- remote_upload_exclusive.py：10563 bytes；SHA-256 30a02e5bc63545b08b1536e59abc418685cf846fbe2c930847d1f1b983f5ae7b
- remote_deploy.py：15483 bytes；SHA-256 657498d42906c260ad12d53c16044a6a272cd1bea1a60ebfd2538b178baf02ff
- remote_rollback.py：13248 bytes；SHA-256 e2690ef991827ad8107430ee0449be913afa65dbf166fe2c1cf19fec0b7736ff
- remote_i1_orchestrator.py：63505 bytes；SHA-256 47c85c2fa311af222cf185c290722ae5c551e5d481d7e43ce2b336e237f6c536
- remote_postflight.py：15456 bytes；SHA-256 b26051aa1fcbb71b84a16173f3c393542bd6c94bc24e619e4ebfb12c4d60d5ee

Static source review confirms local materializer reads exact HEAD:config/mapping.yaml and validates blob/bytes/SHA；orchestrator verifies the composite manifest and transports the materialized payload。No temporary/embedded alternate implementation masquerading as the persisted package was found。

## 8. R4 — State-machine and remote-call authority

判定：PASS。

Persisted orchestrator state machine and R8 terminal agree：

LOCAL_SOURCE_GATE → REMOTE_PREFLIGHT → REMOTE_UPLOAD → REMOTE_DEPLOY → REMOTE_POSTFLIGHT → FINAL_TERMINAL

- REMOTE_CALL_COUNT: 4
- all five executed phase exits: 0
- last started phase: REMOTE_POSTFLIGHT
- postflight attempted/completed/call count: true / true / 1
- retry/resume: 0 / 0
- owned child: started, reaped, return code 0, no signal
- phase_evidence_valid: true

Source control flow only starts upload after validated preflight, only starts deploy after validated upload, and invokes postflight once。Invalid child JSON、interrupted children、invalid phase schema and incomplete postflight are promoted to HOLD states rather than success。There is no second orchestrator、manual SSH、direct helper call、supplemental postflight、retry or resume evidence in R8。

## 9. R5 — Upload and deploy mutation safety

判定：PASS。

remote_upload_exclusive.py static control flow satisfies：

- payload length/SHA validation occurs before any create/open-for-create；
- parent is opened with O_DIRECTORY | O_NOFOLLOW, identity/owner/group/mode and lock are checked；
- the same parent FD is used for /proc/self/fd/<fd>, pass_fds=(fd,), basename existence and dir_fd=parent_fd creation；
- upload uses exact basename plus O_EXCL | O_NOFOLLOW, exact mode/owner/group, fsync and read-back identity verification；
- failure after create retains the upload sidecar as RETAINED_RECOVERY_REQUIRED；no automatic unlink、retry or cleanup is present。

remote_deploy.py static control flow satisfies：

- old target is verified by exact device/inode/bytes/SHA/owner/group/mode before backup and replace；
- upload is reopened and reverified by exact content identity；
- backup uses exclusive create, copies exact old bytes, fsyncs and is reopened/reverified；
- parent fsync occurs before final rechecks；
- target and upload are rechecked by exact identity immediately before replace；
- exactly one os.replace(UPLOAD_TEMP_PATH, TARGET_PATH) is used；EXDEV has no fallback；
- final target is verified as exact new bytes and a changed inode；backup is verified as exact old bytes and its original inode；
- no restart、activation、rollback or cleanup is present in the deploy helper。

The R8 terminal successful postflight relation cannot be produced by upload-only、backup-only or partial states under the orchestrator promotion branches。

## 10. R6 — Final remote-state relation

判定：PASS。

R8 authoritative final relation：

- target: NEW_EXACT；7112 bytes；SHA-256 d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d；device/inode 2050/550822；owner/group/mode mari/mari/0644；exact realpath true；
- pre-execution target: OLD_EXACT；5935 bytes；SHA-256 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3；inode 550698；
- upload temp: ABSENT；
- backup: OLD_EXACT；5935 bytes；SHA-256 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3；device/inode 2050/550916；owner/group/mode mari/mari/0644；
- rollback temp: ABSENT；
- Collector: UNCHANGED；running true；restart count 0；same ID/image/started_at/mount true。

This relation excludes NO_MUTATION、UPLOAD_STAGED_NO_REPLACEMENT、BACKUP_CREATED_NO_REPLACEMENT、PARTIAL_DEPLOYMENT and UNKNOWN_OR_UNSAFE from the promoted R8 success。The unchanged Collector relation is an observation only；it does not claim runtime config loading。

## 11. R7 — Fail-closed behavior and unauthorized-action audit

判定：PASS。

Source and terminal evidence establish：

- terminal promotion requires valid deploy helper evidence plus a single valid postflight with DEPLOYED_IDENTITY_VERIFIED；
- invalid child JSON is fail-closed and does not become a successful phase result；
- fallback terminal is itself a HOLD with UNKNOWN_OR_UNSAFE and NOT_OBSERVED remote objects；
- phase interruptions do not trigger retry/resume or a second postflight；
- counters are all zero：retry、resume、cleanup、rollback、restart-by-task and activation；
- owned child was reaped and bounded task-process scan is zero；
- no upload-sidecar manual cleanup、backup cleanup、stage-root cleanup、rollback、restart、activation or unauthorized Git action occurred；
- no local/synthetic evidence is labelled as runtime-loaded or production-accepted evidence。

Bounded process audit after the read-only checks found no process matching the task-owned orchestrator/helper/postflight/R8/R9 tokens。Scoped caches remain 0 __pycache__ / 0 *.pyc for both P2-R2 and P2-R3。

## 12. R8 — Evidence classification and MVP alignment

判定：PASS。

R8 establishes only：

- exact config file deployment identity；
- exact old backup identity；
- Collector unchanged observation；
- four-call execution identity。

R8 does not establish：

- runtime-loaded config；
- Collector reload/restart；
- activation；
- production runtime behavior；
- accepted station-event facts；
- production acceptance；
- Git closeout。

Classification：MVP-ALIGNED WITH BACKLOG ITEMS。

Approved MVP deliverable remains exact config-only deployment of config/mapping.yaml。The minimum Reliability invariant is that the terminal cannot report successful deployment when the persisted target/backup/upload/rollback relation is partial、unknown or unsafe, and cannot cross into an unauthorized lifecycle action。No new product capability、threat model、retention/archive framework、deployment framework、runtime topology or generic audit framework was added。

## 13. Findings classification

### Production blockers

none。

No credible false PASS、partial deployment promoted as success、terminal ambiguity、source/manifest mismatch、unauthorized mutation、foreign-object consequence、owned-process leak or local/synthetic-to-production evidence misclassification was found。

### Non-blocking recommendations

1. 保留并明确标注 remote_upload_exclusive.py 的 pass_fds compatibility fallback 为 synthetic callable-substitution seam。当前 persisted helper 的 _filesystem_type 明确接受 pass_fds，其内部 operational TypeError 会先转换为 ContractError；正常 orchestrator execution 没有 callable rebind 机制，因此该 fallback 未形成 production false PASS。后续 source maintenance 可考虑更显式的 capability contract，但本轮不 repair、不测试、不升级为 blocker。
2. 后续独立 Verification 若取得新 authority，可增加一个 bounded real-child /proc/self/fd/<fd> check 以补充现有 source/static contract；当前缺少该 probe 不改变 R8 的真实执行关系，也不阻止本轮 Reliability conclusion。

### Backlog

- 上述 compatibility seam 的长期收紧；
- bounded real-child FD inheritance probe，仅在独立 authority 下。

### Out of scope

- Collector restart/reload、activation、runtime-loaded validation；
- production behavior、accepted station-event facts、production acceptance；
- backup/stage-root cleanup policy；
- second postflight、额外 telemetry、tree digest/serializer、generic audit/forensics framework；
- DB/API/Dashboard/V-PLC/D3、source/test repair、Git closeout。

## 14. Stopping-rule application

Section 12/13 stopping rule 已满足：defined terminal invariants 覆盖完整；没有可信 false PASS、partial deployment success、unauthorized mutation、foreign-object consequence、owned-process leak 或 evidence-classification expansion。额外 diagnostic completeness、理论状态组合、第二次 postflight、runtime validation 与 cleanup 不会改变本轮 PASS/HOLD claim，因此不升级为 blocker，也不继续打开新的 review framework。

## 15. Final report write boundary

本轮唯一创建路径为本报告自身。Report write 前该路径为 ABSENT / NON-SYMLINK；其他 source、test、package、manifest、mapping、R8 report/artifact、status、roadmap、handoff、PM rules、.gitignore 与 external artifact 均未修改。

预期 final untracked set 为 initial set 加本 exact report path：

- count: 13780
- sorted NUL-delimited path-set SHA-256: b369a85075747fdc964753be4edfb6ac3b4c076e30b126ebcf837276153f117c

## 16. Next gate、Thread context 与 non-inheritance

唯一 next gate：

R30-I1-R9 RELIABILITY_PASS_WITH_RECOMMENDATIONS / REVIEWED / WRITTEN
→ ChatGPT PM durable intake only

即使 PM 接受本报告，也不得自动进入 Collector restart、activation、runtime-loaded validation、production acceptance、cleanup、rollback 或 Git closeout。任何后续 lifecycle gate 必须使用新 authority、新 Thread、新 remote-call budget、新 runtime evidence 与独立 PASS/HOLD criteria。

Thread context assessment：

- 本次输出长度：长；完整证据已写入 exact durable report，Chat 仅返回 concise manifest；
- 当前 Thread 是否建议继续：no；
- 下一轮是否建议新开 Thread：yes；
- 理由：R9 focused Reliability review 已完成，下一步是 PM durable intake；任何 Collector restart/activation/runtime-load gate 都需要新的 Architecture / Integration Thread 与新 authority。

## 17. Delivery state

RELIABILITY_PASS_WITH_RECOMMENDATIONS
REVIEWED
WRITTEN

本报告没有建立 PM-ACCEPTED、VERIFIED、STAGED、COMMITTED、PUSHED、DEPLOYED、ACTIVATED、RUNTIME-LOADED 或 PRODUCTION-ACCEPTED。

