# Sprint 4 D2-R7B-I1 R24-R3 Focused Verification Review

## 1. 报告身份与结论

- 报告名称：Sprint 4 D2-R7B-I1 R24-R3 Focused Verification Review
- 任务名称：D2-R7B-I1 R24-R3 — Verify Active Helper Selection and Real-Child FD Inheritance
- 执行 Thread：Verification
- 任务风险等级：Level 1 focused read-only Verification
- 报告交付模式：REPOSITORY_DURABLE_REPORT
- 唯一写入路径：docs/reports/sprint4_d2_r7b_i1_r24_r3_focused_verification_review.md
- 结论：PASS WITH RECOMMENDATIONS

本结论证明 active deployment package 选择了修复后的 helper，真实本地 child 的
directory FD inheritance identity 通过，negative child 没有获得等价 authority，且没有
发现 production blocker。它不表示 current remote eligibility PASS、remote execution
authorized、uploaded、deployed、runtime loaded、Collector restarted/activated、staged、
committed 或 pushed。

## 2. Authority handoff 与当前 gate

当前最新 PM authority：

    path: docs/thread_handoff/chatgpt_pm_handoff_260727-2034.md
    bytes: 5587
    SHA-256: 1e4bf0d8e9f70b4bd427c305acea967b1a92134efca80077e293af1d9738d6a7
    R24-R3 Focused Verification Review: AUTHORIZED

本 review fresh 恢复并保持：

    R23 execution: HOLD / PM-ACCEPTED
    R23 remote state: NO_MUTATION / PM-ACCEPTED
    R23 authority: CONSUMED
    R24-R1 repair: REPAIR PASS / PM-ACCEPTED FOR FOCUSED REVIEW
    R24-R2 Reliability: PASS WITH RECOMMENDATIONS / PM-ACCEPTED
    R24-R3 focused Verification: AUTHORIZED
    Remote: NOT AUTHORIZED
    Remote eligibility refresh: NOT AUTHORIZED
    New config-only execution: NOT AUTHORIZED
    Source/test/manifest modification: NOT AUTHORIZED
    Collector restart: NOT AUTHORIZED
    Collector activation: NOT AUTHORIZED
    Git closeout: NOT AUTHORIZED

本 task 未 retry、resume 或重新解释 R23 为 deployment PASS；未执行 SSH、remote refresh、
upload、deploy、rollback、Docker/Compose、Collector restart 或 activation。

## 3. R24-R2 PM intake

R24-R2 report 的 frozen identity 为 21795 bytes、
0b3a7b34ae546b8dad0554d3fe77a3465720346673286bb85a44b27f1540face。PM intake 已接受：

- source-byte syntax：PASS；
- T33：PASS；
- T1-T35：PASS 35/35；
- E1-E40：PASS 40/40；
- P2-R2 manifest：6/6 PASS；
- P2-R3 manifest：9/9 PASS；
- R24-R1 package manifest：5/5 PASS；
- R23 historical manifest：3/3 PASS；
- bytecode：0；
- HEAD/origin：一致，ahead/behind 0/0，cached empty。

R24-R2 接受的 Reliability 判断为 R1 exact FD inheritance PASS、R2 /proc/self
semantics PASS、R3 compatibility fallback PASS WITH RECOMMENDATIONS，无 production
blocker。本 review 独立补充 active selection、bootstrap round-trip 与真实 child probe。

## 4. Frozen identities

report 写入前及写入前最后一次 recovery 均 fresh 核验以下 identity：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| docs/thread_handoff/chatgpt_pm_handoff_260727-2034.md | 5587 | 1e4bf0d8e9f70b4bd427c305acea967b1a92134efca80077e293af1d9738d6a7 |
| docs/reports/sprint4_d2_r7b_i1_r24_r2_focused_reliability_review.md | 21795 | 0b3a7b34ae546b8dad0554d3fe77a3465720346673286bb85a44b27f1540face |
| docs/reports/sprint4_d2_r7b_i1_r24_r1_parent_fd_findmnt_inheritance_repair.md | 13473 | 93d6a9fec3118765872ea77fdfe89f9062d94594258888f95c157dbf8ba96110 |
| docs/reports/evidence/d2_r7b_i1_r24_r1_parent_fd_findmnt_inheritance_repair/manifest.sha256 | 631 | fe8f922f92d918877edccf37043bb99aeb548ff029db2541d7cfba905ef78de2 |
| docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py | 10203 | b439a071ceb898f81689331fcba61a87e7825cbd418f899e34c072d599de3ee3 |
| docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py | 57998 | 71d31523518ef0686fc28cba82f7fe969d8cfc3ecaecb6578bb58e8152508969 |
| docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256 | 528 | 62c4a1d939cc377ead65c9c76e83fea762a2b0fd8d7f2af9e0e1258f2c2cc8d8 |
| docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py | 45783 | eea3e8778cc94c78a0931b2404f888a78176996cd1a4421a7442667c8b859085 |
| docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256 | 1122 | 42bf24b9ddd338624ca7e81bad9a924ca0a40c179071cbaa4c6fc1848f37dd90 |
| docs/reports/evidence/d2_r7b_i1_r23_remote_config_only_execution/final_terminal.json | 12280 | 90cbb77b827f97580d4bbd58d5eafeb6758f950170f0ef5ff6810211498c9e86 |

任何 frozen identity 未发生 drift。

## 5. Git baseline

项目绝对路径：/Users/chenjie/Documents/MES/edge-mes-demo。

report 写入前 live recovery：

    root: /Users/chenjie/Documents/MES/edge-mes-demo
    branch: main
    HEAD: 8de5edbb504538a233abbcc80102cb714c9cee65
    origin/main: 8de5edbb504538a233abbcc80102cb714c9cee65
    ahead/behind: 0/0
    cached: empty
    git diff --check: PASS

已知 pre-existing tracked dirty / excluded：.gitignore、docs/current_status.md、
docs/thread_handoff/pm_operating_rules.md。既有 untracked reports、evidence、handoffs、
frontend 与 management artifacts 均保持只读，不纳入本 task write authority。

report 写入前 exact report path 为 ABSENT / NON-SYMLINK，parent docs/reports 为 real
non-symlink directory。

## 6. Exact review scope

本 review 仅覆盖：

1. active helper identity 与 P2-R2/P2-R3/package manifest binding；
2. orchestrator HELPERS、read_bytes()、base64 bootstrap、local composite manifest gate；
3. real-child FD inheritance 与 no-pass_fds isolation；
4. host /proc/self/fd evidence boundary；
5. compatibility fallback 的 persisted production reachability；
6. filesystem authority 之后的 mutation ordering、retained artifact 与 cleanup boundary；
7. R23 historical truth、T/E/matrix/package/bytecode/Git allowlist integrity。

不重新设计 helper，不修改 compatibility fallback，不扩展到 Linux CI、generic subprocess
framework、deployment framework、automated recovery、remote monitoring、Collector lifecycle、
multi-node deployment 或 production-readiness framework。

## 7. V1 — Active helper identity

判定：PASS。

live active upload helper：

    path: docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py
    bytes: 10203
    SHA-256: b439a071ceb898f81689331fcba61a87e7825cbd418f899e34c072d599de3ee3

旧 R23 historical helper identity 为：

    1d69bb970f7c37968ac33d37373e261431c1f7ed98f041f95e59de4351381a88

旧 SHA 不出现在当前 P2-R2 manifest、P2-R3 composite manifest 或 R24-R1 package manifest；
当前 active manifest-bound upload helper 是新 SHA。R23 historical terminal 中的旧 helper
identity 未被解释为当前 active bytes。

## 8. V2 — Active manifest binding

判定：PASS。

fresh manifest checks：

| Manifest | Entries | Result |
| --- | ---: | --- |
| docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256（owning directory） | 6 | 6/6 OK |
| docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256（repository root） | 9 | 9/9 OK |
| docs/reports/evidence/d2_r7b_i1_r24_r1_parent_fd_findmnt_inheritance_repair/manifest.sha256 | 5 | 5/5 OK |
| docs/reports/evidence/d2_r7b_i1_r23_remote_config_only_execution/manifest.sha256 | 3 | 3/3 OK |

P2-R2 manifest exact upload-helper entry绑定新 SHA，exact test entry绑定
71d31523518ef0686fc28cba82f7fe969d8cfc3ecaecb6578bb58e8152508969；P2-R3 composite manifest
对应两项均绑定新 SHA/当前 test SHA。三份 active/package manifest 的 path set 均按稳定
排序、无 duplicate、self-excluded；R24-R1 package manifest 绑定当前两份 active manifests、
active source/test 与 R24-R1 report。

R17/R18/R23 historical artifacts 未被本 task 写入，且未被 active package manifest 重新
绑定。R23 historical report、terminal 与 manifest identity 在本 review 中保持不变。

## 9. V3 — Orchestrator/helper/bootstrap selection

判定：PASS。

live source/AST 与 in-memory compile/exec evidence：

- remote_i1_orchestrator.py:34-38 的 HELPERS["remote_upload"] exact 指向
  docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py；
- remote_i1_orchestrator.py:545-547 对传入 Path 执行 helper.read_bytes()，再交给
  build_remote_command()；
- remote_i1_orchestrator.py:73-77 使用 base64 encode，并生成
  base64.b64decode(...) → compile(..., "exec") → exec(...) bootstrap；
- remote_i1_orchestrator.py:111-138 的 local composite manifest gate 读取并验证 stable
  nine-file path set、regular non-symlink source 与实际 SHA；
- orchestrator source 不包含旧 helper SHA、不读取 R23 evidence path，也没有 embedded stale
  upload-helper copy；orchestrator source 中没有 _filesystem_type callable rebind。

没有发现正常 persisted execution 会从 R23 evidence 读取旧 helper bytes 或 normal production
callable rebind。P2-R3 synthetic harness 的 callable substitution 仍只作为 test seam。

## 10. Bootstrap round-trip

判定：PASS。

使用 live active helper bytes 调用 persisted build_remote_command()，从生成 command 的
base64 literal 恢复 bytes，并以 in-memory compile(..., "exec") / exec(...) 执行 bootstrap
定义；无 remote invocation。

    active helper SHA-256:   b439a071ceb898f81689331fcba61a87e7825cbd418f899e34c072d599de3ee3
    round-trip SHA-256:      b439a071ceb898f81689331fcba61a87e7825cbd418f899e34c072d599de3ee3
    SHA match:               yes
    bootstrap compile/exec:  PASS

## 11. V4 — Positive real-child FD inheritance probe

判定：PASS。

probe 为 inline、本地、非持久化 Python；使用 bounded system temporary directory，并执行
实际 subprocess.run(..., pass_fds=(fd,))，child 执行 os.fstat(fd)。observed：

    host: Darwin / sys.platform=darwin
    parent fd: 3
    parent st_dev: 16777234
    parent st_ino: 11601208
    child returncode: 0
    child fstat: OK
    child st_dev/st_ino: 16777234 / 11601208
    positive identity match: yes
    parent fd live after child: yes
    final close: yes

child 返回的 device/inode 与 parent 完全一致，证明实际 child 保留的是同一个 opened
directory FD authority，而不是只传递 pathname。

## 12. V5 — Negative no-pass_fds isolation probe

判定：PASS。

使用同一 parent FD number 启动第二个真实 child，但不提供 pass_fds。child numeric FD 为
3，os.fstat(3) 返回 OSError / errno=9 (EBADF)；child returncode 为 0，但没有获得
与 parent 相同的 directory identity：

    negative same identity: false
    negative isolation: true

本 probe 没有把 numeric FD 不存在作为必需条件；若 child runtime 复用该 number，也只会在
device/inode 不同的情况下通过 negative isolation。

## 13. V6 — Host /proc/self/fd evidence

结果：HOST_PROC_SELF_UNAVAILABLE。

host facts：

    uname -s: Darwin
    sys.platform: darwin
    /proc/self/fd exists: false

本 host 不提供 Linux /proc/self/fd，因此没有伪造 Linux proc evidence，也没有使用
/dev/fd 声称等价证明。positive probe 已通过真实 child FD identity；缺少 Linux proc view
只影响 evidence depth，属于 recommendation-only，不是 HOLD。

## 14. V7 — Compatibility fallback production reachability

结果：PASS WITH RECOMMENDATIONS，无 production blocker。

独立 in-memory evidence：

1. persisted _filesystem_type(path, *, pass_fds=()) 接受 pass_fds；fake subprocess
   对 operational TypeError("unexpected keyword argument 'pass_fds'") 的一次调用被
   persisted source 转换为 ContractError，没有返回 path-only PASS；
2. 替换 module-level callable 为旧的 path-only callable 后，outer fallback 在 bounded
   synthetic seam 中实际可达；
3. remote_i1_orchestrator.py 通过 source bytes + compile/exec bootstrap，不导入并重新
   bind upload helper 的 _filesystem_type，正常 persisted execution 没有发现该 substitution
   mechanism；
4. P2-R3 synthetic harness substitution 不能作为 production reachability 证据，也没有
   改变 active helper bytes 的 production selection path。

Recommendation 是保留该 synthetic compatibility seam 的边界说明，并在未来需要 Linux
proc evidence depth 时增加 bounded Linux-host probe。两项均已证明：no production false
PASS、no unsafe mutation、no stale helper selection、no production-truth corruption。

## 15. V8 — Mutation ordering and fail-closed boundary

判定：PASS。

active helper line evidence：

- remote_upload_exclusive.py:95-103：listed parent 为 non-symlink directory，并核验
  device、owner/group、mode；
- :107-110：os.open(... O_DIRECTORY | O_NOFOLLOW) 后 os.fstat() 与 listed identity
  比较；
- :112-124：parent lock 覆盖 stable FD identity、owner/group/mode checks；
- :125-136：filesystem query 使用同一个 parent FD 的 /proc/self/fd/<fd> 与
  pass_fds=(parent_fd,)，并在 query 后重做 current parent identity check；
- :230-235：payload length/hash validation 在 parent open 与任何 create 前；
- :239-242：stale basename check 后才用 basename、dir_fd=parent_fd、O_EXCL、
  O_NOFOLLOW 创建；
- :244-249：created FD verification、write、chmod、fsync、read/hash/stat verification
  在 create 后执行；
- :250-263：create 后 failure 返回 RETAINED_RECOVERY_REQUIRED 并保留 exact artifact；
  helper source AST 中没有 unlink、rename、replace 或 rmdir mutation call。

filesystem failure 在 named create 前结束；create 后 failure 无 automatic cleanup、retry
或 foreign deletion。parent lock、filesystem query、current identity check 与 create 均在
同一 opened parent FD boundary 中。

## 16. V9 — Historical execution truth preservation

判定：PASS。

R23 final terminal fresh parse：

    status: HOLD_UPLOAD_FAILED_NO_REPLACEMENT
    phase: REMOTE_UPLOAD
    REMOTE_CALL_COUNT: 3
    classification: NO_MUTATION
    target state: OLD_EXACT
    target sha256: 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3
    upload temp: ABSENT
    backup: ABSENT
    rollback temp: ABSENT
    Collector: UNCHANGED
    retry_count: 0
    resume_count: 0
    cleanup_count: 0
    rollback_count: 0
    restart_count: 0
    activation_count: 0
    terminal bytes/SHA: 12280 / 90cbb77b827f97580d4bbd58d5eafeb6758f950170f0ef5ff6810211498c9e86

R23 仍是 HOLD，target 仍为 historical OLD_EXACT，postflight 仍为 historical
NO_MUTATION，authority 仍 consumed。R24-R1/R24-R2 与本地 Verification 没有把 R23 改写
为 deployment PASS；current remote eligibility 未刷新，新 execution 仍未授权。

## 17. Source-byte syntax

以下 exact persisted bytes 使用 compile(path.read_bytes(), path, "exec") fresh 验证，
全部 PASS：

- docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py；
- docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py；
- docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py；
- docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py。

未使用 py_compile、compileall、-B、PYTHONDONTWRITEBYTECODE 或 PYTHONPYCACHEPREFIX。

## 18. T/E matrix

- T command：python3 docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py；
  T33 PASS，MATRIX=PASS count=35/35；
- E command：python3 docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py；
  E1-E40: PASS 40/40。

两次 matrix 均针对当前 persisted source/test bytes 执行，没有 source/test/manifest 修改。

## 19. Manifest、bytecode 与 allowlist audit

Manifest 结果为 6/6、9/9、5/5、3/3；active/package manifests 的 sorted、self-excluded、
duplicate contract 通过。

测试前、T/E matrix 后、real-child probe 后及 report 写入前 bytecode audit：

    docs/reports/evidence/d2_r7b_p2_r2: __pycache__=0, *.pyc=0
    docs/reports/evidence/d2_r7b_p2_r3: __pycache__=0, *.pyc=0
    docs/reports/evidence/d2_r7b_i1_r24_r1_parent_fd_findmnt_inheritance_repair: __pycache__=0, *.pyc=0

没有通过 cleanup 制造 bytecode 结果。

本 task write allowlist 只有本 report；未创建 review manifest、JSON evidence、helper、
fixture、child script、parser、transcript、stdout/stderr sidecar、test-output log、second
report 或 checkout 外 report。既有 dirty/untracked artifacts 未被纳入 task change。

## 20. Blockers

none。

没有发现：

- active manifest 绑定旧 upload helper；
- orchestrator 不读取当前 active helper bytes；
- bootstrap round-trip SHA mismatch；
- positive real child 无法继承相同 directory FD identity；
- negative child 获得相同 directory authority；
- normal persisted execution 可触发 path-only fallback；
- filesystem authority 前发生 mutation；
- source/test/manifests 内部不一致；
- historical R23 truth 被提升为 deployment PASS；
- probe 或测试产生未授权 repository mutation。

## 21. Recommendations

1. 当前 host 为 Darwin，/proc/self/fd 不可用；若未来需要 Linux proc-level evidence depth，
   可在独立、明确授权的 Linux CI/job 中增加 bounded real-child probe。该建议不改变本次
   active selection、FD identity、mutation safety 或 production truth 结论。
2. 保留 R24-R2 已接受的 compatibility fallback seam 说明；后续 source maintenance 可
   重新评估 callable capability contract，但本 task 不修改 source/test，也不将 synthetic
   substitution 解释为 production path。

上述 recommendations 均为 evidence-depth / maintenance backlog，不构成当前 Verification
blocker；均满足 no production false PASS、no unsafe mutation、no stale helper selection
与 no production-truth corruption。

## 22. MVP alignment

分类：MVP-ALIGNED WITH BACKLOG ITEMS。

本 review 直接服务已批准的 single-file config-only deployment MVP：确认 active package
不会选择 stale helper，且 filesystem authority 在真实 child subprocess boundary 中不被
降级。最小 terminal/safety invariant 是 active bytes selection、same-directory FD identity、
filesystem-before-mutation 与 R23 truth preservation。

本 task 未新增 deployment framework、automated recovery、remote monitoring、Collector
lifecycle、multi-node、Linux infrastructure 或更宽 production-readiness claim。Linux proc
evidence depth 与 fallback seam maintenance 保持 backlog/recommendation，不阻塞当前 MVP
Verification claim。

## 23. Next gate 与 delivery state

唯一 next gate：

    R24-R3 report WRITTEN
    → PM durable report intake only

若 PM 接受本 PASS WITH RECOMMENDATIONS，后续才可在新的 exact read-only authority 下
fresh remote eligibility；只有再次获得明确 execution authority 后，才可能讨论新的
config-only execution。不得自动进入后续 gate。

Delivery state：

    R24-R3 VERIFICATION REPORT WRITTEN

WRITTEN 不表示 PM-ACCEPTED、REMOTE-ELIGIBLE、REMOTE-AUTHORIZED、DEPLOYED、
STAGED、COMMITTED 或 PUSHED。

## 24. Thread context assessment

- 本次输出长度：长；完整证据保存在本 exact durable report，Chat 只返回 concise manifest；
- 当前 Thread 是否建议继续：no；
- 下一轮是否建议新开 Thread：yes；
- 理由：R24-R3 focused Verification 已完成并写入 durable report；下一步是 PM durable
  intake，后续 remote eligibility 必须在新 authority 下独立开启，不应在本 Thread 中顺势
  执行 remote、修改 source/test 或进入 execution gate。

## 25. Final local boundary statement

本报告只记录 local/static/synthetic/package-closure/real-child Verification evidence。没有
remote action、remote refresh、upload、deploy、rollback、restart、activation、Docker/Compose、
Git stage、Git commit 或 Git push。R24-R3 report 的最终 bytes/SHA 与最终 Git status 以
PM durable intake 时重新读取本 exact path 的 live facts 为准。
