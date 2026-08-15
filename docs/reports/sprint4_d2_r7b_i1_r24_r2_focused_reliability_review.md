# Sprint 4 D2-R7B-I1 R24-R2 Focused Reliability Review

## 1. 报告名称、任务名称与执行 Thread

- 报告名称：Sprint 4 D2-R7B-I1 R24-R2 Focused Reliability Review
- 任务名称：D2-R7B-I1 R24-R2 — Review Parent-FD Inheritance Repair and Compatibility Fallback Safety
- 执行 Thread：Reliability
- 任务风险等级：Level 1 focused read-only Reliability review
- Report delivery mode：`REPOSITORY_DURABLE_REPORT`
- Exact report path：`docs/reports/sprint4_d2_r7b_i1_r24_r2_focused_reliability_review.md`

## 2. Conclusion

结论：`PASS WITH RECOMMENDATIONS`

R24-R1 已恢复本 review 目标的 production upload invariant：filesystem authority 来自同一个已打开、已加锁且仍存活的 parent directory FD；同一 numeric FD 被用于 `/proc/self/fd/<n>` 查询、`pass_fds=(n,)` 以及后续 basename existence checking 和 `dir_fd=parent_fd` exclusive creation。查询失败、invalid output、exception 或 FD failure 在 create 前 fail closed。

compatibility fallback 在 bounded substituted-callable probe 中确实会放弃 FD 参数；同消息的 callable-body `TypeError` 也会触发 path-only retry。但 persisted production `_filesystem_type` 会把 operational `TypeError` 先转换为 `ContractError`，persisted remote orchestrator 没有正常的 callable rebind 机制。该 fallback 当前可达面是 synthetic test seam，未建立 production false PASS、unauthorized mutation、foreign deletion 或 production-truth corruption，因此不构成 HOLD。

本结论不表示 focused Verification PASS、remote eligibility PASS、remote execution authorized、deployed、runtime loaded、Collector restarted/activated、staged、committed 或 pushed。

## 3. Authority handoff 与 current gate

最新 PM authority handoff：

| Path | Bytes | SHA-256 | Authority |
| --- | ---: | --- | --- |
| `docs/thread_handoff/chatgpt_pm_handoff_260727-2004.md` | 6204 | `c00dd804e11b3c464161dc4b58ac81f323390be6d26571cc3248f5683b4e3a7d` | `R24-R2 Focused Reliability Review: AUTHORIZED` |

live 文件 identity 与 handoff identity 匹配；handoff 明确授权本 exact task。审查期间恢复并保持：

- R23 execution：`HOLD / PM-ACCEPTED`；
- R23 remote state：`NO_MUTATION / PM-ACCEPTED`；
- R23 authority：`CONSUMED`；
- R24-R1 repair：`REPAIR PASS / PM-ACCEPTED FOR FOCUSED REVIEW`；
- R24-R2 focused Reliability：`AUTHORIZED`；
- Focused Verification：`NOT AUTHORIZED`；
- Remote、新 config-only execution、Collector restart、Collector activation、Git closeout：`NOT AUTHORIZED`。

本 task 未 retry、resume 或重新解释 R23 为 deployment PASS。

## 4. Frozen R24-R1 identities

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/reports/sprint4_d2_r7b_i1_r24_r1_parent_fd_findmnt_inheritance_repair.md` | 13473 | `93d6a9fec3118765872ea77fdfe89f9062d94594258888f95c157dbf8ba96110` |
| `docs/reports/evidence/d2_r7b_i1_r24_r1_parent_fd_findmnt_inheritance_repair/manifest.sha256` | 631 | `fe8f922f92d918877edccf37043bb99aeb548ff029db2541d7cfba905ef78de2` |
| `docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py` | 10203 | `b439a071ceb898f81689331fcba61a87e7825cbd418f899e34c072d599de3ee3` |
| `docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py` | 57998 | `71d31523518ef0686fc28cba82f7fe969d8cfc3ecaecb6578bb58e8152508969` |
| `docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256` | 528 | `62c4a1d939cc377ead65c9c76e83fea762a2b0fd8d7f2af9e0e1258f2c2cc8d8` |
| `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256` | 1122 | `42bf24b9ddd338624ca7e81bad9a924ca0a40c179071cbaa4c6fc1848f37dd90` |

R24-R1 report、package manifest、P2-R2/P2-R3 source 与 manifests 在 report 写入前均重新核验，identity 未漂移。

## 5. Git baseline

执行前及 report 写入前 live recovery：

- repository root：`/Users/chenjie/Documents/MES/edge-mes-demo`；
- branch：`main`；
- HEAD：`8de5edbb504538a233abbcc80102cb714c9cee65`；
- origin/main：`8de5edbb504538a233abbcc80102cb714c9cee65`；
- ahead/behind：`0/0`；
- cached set：empty；
- `git diff --check`：`PASS`。

已知 pre-existing tracked dirty / excluded 仍仅为：

- `.gitignore`；
- `docs/current_status.md`；
- `docs/thread_handoff/pm_operating_rules.md`。

其余 pre-existing untracked reports、handoffs、evidence、frontend 与 management artifacts 均保持原状，未纳入本 review write authority。

## 6. Files read

已读取并按 authority precedence 使用：

- `docs/thread_handoff/pm_operating_rules.md`；
- `docs/thread_handoff/chatgpt_pm_handoff_260727-2004.md`；
- `docs/thread_handoff/chatgpt_pm_handoff_260727-1931.md`；
- `docs/current_status.md`；
- `docs/roadmap.md`；
- `docs/reports/sprint4_d2_r7b_i1_r24_r1_parent_fd_findmnt_inheritance_repair.md`；
- `docs/reports/evidence/d2_r7b_i1_r24_r1_parent_fd_findmnt_inheritance_repair/manifest.sha256`；
- `docs/reports/sprint4_d2_r7b_i1_r23_remote_config_only_execution.md`；
- `docs/reports/evidence/d2_r7b_i1_r23_remote_config_only_execution/final_terminal.json`；
- `docs/reports/evidence/d2_r7b_i1_r23_remote_config_only_execution/manifest.sha256`；
- `docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py`；
- `docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py`；
- `docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256`；
- `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py`；
- `docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py`；
- `docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py`；
- `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256`。

R23 frozen facts retained as historical input：`REMOTE_UPLOAD=2`、`REMOTE_DEPLOY` 未启动、唯一 read-only postflight classification 为 `NO_MUTATION`、target 为 `OLD_EXACT`、upload temp / backup / rollback temp 为 `ABSENT`、Collector unchanged、retry/resume/cleanup/rollback/restart/activation counters 为 0。

## 7. Exact review scope

本 review 仅审查 R24-R1 parent-FD inheritance repair、compatibility fallback reachability、upload mutation ordering、identity/lock preservation、T33 adequacy 与既有 T29/T30/T34/T35/E contract safety。未重新设计 deployment package，未评价代码美观程度，未扩大到 generic FD abstraction、deployment framework、automated recovery、remote monitoring、Collector lifecycle、multi-node 或 production-readiness framework。

## 8. R1 — Exact FD inheritance

判定：`PASS`。

persisted production path 保持以下 exact contract：

```text
parent_fd = os.open(PARENT_PATH, O_RDONLY | O_DIRECTORY | O_NOFOLLOW)
parent_fd_path = /proc/self/fd/<parent_fd>
_filesystem_type(parent_fd_path, pass_fds=(parent_fd,))
```

具体判断：

- `_filesystem_type(path, *, pass_fds: tuple[int, ...] = ())` 将同一个传入 tuple 交给 `subprocess.run(..., pass_fds=pass_fds)`；
- `_parent_stat()` 在 `parent_fd` live 且已 `flock(LOCK_EX | LOCK_NB)` 后调用 filesystem query，`pass_fds` exact 为 `(parent_fd,)`；
- 未将 unrelated FD 放入 tuple；`shell=False` 保持；未显式设置 `close_fds=False`，因此 Python subprocess 默认 close-fds 语义保持安全，且显式 `pass_fds` 只放行该 parent FD；
- `_filesystem_type()` 是同步 subprocess call，parent FD 与 lock 在整个 query 期间仍存活；
- `_parent_stat()` 的 success 结果由 `upload()` 持有，stale check、basename create、write、verify 与 finally release 均在同一个 FD/lock boundary 内；
- `_parent_stat()` 每个 failure path 都通过 `except BaseException` unlock 并 close parent FD；`upload()` 的 success/failure finally 释放 parent FD 与 upload FD。

T33 实际观察到 `/proc/self/fd/4`、`pass_fds=(4,)`、`os.fstat(4)` success、unrelated FD absent、success 后 FD closed；path-based preflight/deploy/rollback calls 的 `pass_fds` 均为空。

## 9. R2 — `/proc/self` process semantics

判定：`PASS`。

没有 inheritance 时，child 中的 `/proc/self` 是 child PID 的 proc view；`/proc/self/fd/<n>` 不再因为 parent process 的同名 path 而自动指向 parent 已打开目录，且默认 close-fds 会关闭未显式传递的 FD。R24-R1 的 `pass_fds=(parent_fd,)` 使 child 保有同一个 opened directory FD，因此 child 自己解析 `/proc/self/fd/<same fd>` 时仍得到该 inherited opened directory，而不是 pathname-only substitution。

review 未发现 production path 用 pathname-only query 替代 upload parent FD authority。path-based callers 保持 empty FD set，且不继承 upload FD；这是 phase isolation，不是 upload authority 的替代。

## 10. R3 — TypeError compatibility fallback safety

判定：`PASS WITH RECOMMENDATIONS`；无 production blocker。

exact branch 为：

```python
try:
    filesystem = _filesystem_type(parent_fd_path, pass_fds=(parent_fd,))
except TypeError as exc:
    if "unexpected keyword argument 'pass_fds'" not in str(exc):
        raise
    filesystem = _filesystem_type(parent_fd_path)
```

逐项结论：

1. persisted production `_filesystem_type` 明确接受 `pass_fds`；
2. persisted `_filesystem_type` 内部的 `subprocess.run` operational `TypeError` 位于其内部 exception tuple 中，并先被包装为 `ContractError`；
3. 因而 outer fallback 仅在 module-level callable 被外部替换为旧的 path-only callable 时可达；
4. persisted `remote_i1_orchestrator.py` 通过 `build_remote_command()` 将 exact helper bytes `exec(compile(...))` 发送到 phase child，正常执行没有 rebind `_filesystem_type` 的机制；
5. P2-R3 fake remote test harness 的 `configure(ns)` 会把 callable 替换成 path-only lambda，这是 synthetic test seam，不是 persisted production execution；
6. 对真正 production `_filesystem_type` 的 operational `TypeError`，Probe A 观察到只抛 `ContractError`，不会进入 outer fallback；
7. fallback 本身若在 substituted callable 下可达，会导致 FD authority 被放弃，故属于 bounded test-seam maintainability debt；但当前没有 production-reachable false PASS 或 unsafe mutation path。

因此不能仅因 message matching 不优雅而 HOLD。该结论依赖 live source reachability：没有发现正常 persisted remote mechanism 会 rebind 该 callable。

## 11. Bounded probes

所有 probe 均使用 source bytes `compile(..., "exec")` 的 in-memory module loading；没有持久化 helper、fixture、JSON evidence、transcript、log 或 parser。

### Probe A — Persisted callable operational TypeError

mocked `subprocess.run` 抛出 `TypeError("unexpected keyword argument 'pass_fds'")`。

观察：`_filesystem_type` 返回 `ContractError`，错误为 `findmnt filesystem query failed: unexpected keyword argument 'pass_fds'`；mock call count `1`，收到 `pass_fds=(9,)`，未触发 outer fallback。

结果：`PASS`。production safety consequence：无 path-only false PASS。

### Probe B — Old callable substitution

module-level `_filesystem_type` 临时替换为只接受 positional path 的 callable。

观察：outer fallback 实际可达；path-only callable 被调用 `1` 次，返回 `ext4`，`_parent_stat()` success 返回 parent FD，probe 随后确认 FD closed。

结果：`PASS (bounded compatibility behavior)`。production reachability：仅外部 callable substitution；persisted normal production execution 未发现该替换。安全结论：test seam 可兼容旧 callable，但该 seam 不应被解释为 production FD authority。

### Probe C — Same-message internal TypeError from substituted callable

替换 callable 接受 keyword，并在收到 `pass_fds` 时于 callable body 抛出同样的 `TypeError`；path-only second call 返回 `ext4`。

观察：call shapes 为 `['pass_fds', 'path_only']`；outer fallback 确实再次调用 path-only 形式，随后 `_parent_stat()` 在该 substituted fixture 下返回 success。结果为 substituted-only false PASS / dropped FD authority。

结果：`PASS (reachability and consequence characterized)`。该 false PASS 需要 in-process callable substitution；它不是 persisted production normal path。推荐保留该边界说明并由后续 focused Verification 关注 source identity/rebind isolation，不在本 gate repair source。

## 12. R4 — Fail-closed mutation ordering

判定：`PASS`。

upload production 顺序为：完整 payload length/hash validation → pathname listed/opened/stable identity checks → bounded parent lock → FD-bound filesystem query → current pathname identity recheck → writable check → stale basename check → `os.open(basename, O_RDWR | O_CREAT | O_EXCL | O_NOFOLLOW, dir_fd=parent_fd)` → created-FD verification → write → chmod → fsync → read/hash/stat verification。

因此 stale basename check、upload-temp create、write、chmod、fsync 与 verify 全部晚于 filesystem authority PASS。findmnt unavailable、nonzero、invalid/multiline/non-ext4 output、exception 或 FD failure 在 named create 前终止；T21/T22/T33 均观察到 failure-before-create。

后续 deploy、rename/replace、backup、rollback 是独立后续 phase，当前 remote 未授权且未执行；它们各自的 persisted helper 在自身 filesystem gate 后才进入 bounded mutation contract。T33 同时确认这些 path-based filesystem calls 不继承 upload FD。R24-R2 未将其 phase authority 与 upload parent-FD authority 混合。

## 13. R5 — Race and identity preservation

判定：`PASS`。

- listed parent 必须是 non-symlink directory，device、owner/group、mode 先核验；
- `os.open(... O_DIRECTORY | O_NOFOLLOW)` 后以 `fstat` 对比 listed identity；
- lock 后再次 `fstat`，再核验 owner/group/mode；filesystem query 后再次 `lstat(PARENT_PATH)` 对比 opened stable identity；
- parent lock 覆盖 filesystem query、current identity recheck、stale basename check 与 basename create；query 不解除锁、不关闭 parent FD；
- create 使用 basename、`dir_fd=parent_fd`、`O_EXCL`、`O_NOFOLLOW`；没有绝对 pathname create 替代；
- upload failure path 不执行 unlink/rename/replace/rmdir；foreign basename/inode 不删除、不替换；
- T29 foreign inode safety、T30 post-verification replacement safety、T34 zero pathname cleanup 与 T35 retained-artifact fail-closed 均 fresh matrix PASS；
- retained artifact contract 保持：create 后 failure 返回 `RETAINED_RECOVERY_REQUIRED`，下一次 stale basename 直接 HOLD；无 automatic cleanup/retry。

## 14. R6 — Regression adequacy

判定：`PASS`，附 bounded test-depth recommendation。

T33 使用 persisted source bytes loader，并实际证明：

- `_parent_stat()` 打开 real parent FD；
- query path 是 `/proc/self/fd/<same fd>`；
- exact `pass_fds` 是 `(same fd,)`；
- fake subprocess boundary 的 `os.fstat(fd)` success；
- unrelated FD 不在 tuple；
- success payload/mode/identity/hash/inode 保持；
- non-ext4 failure 在 named create 前结束；
- preflight/deploy/rollback path calls 不继承 upload FD；
- success 后 upload parent FD closed。

T33 的 `fake_run` 不启动真实 child，因此它不是完整 OS-level `/proc/self` integration test；它验证的是 persisted source 的 subprocess call contract。该空洞不能在当前执行模型导致 production false PASS：production 使用标准 `subprocess.run`、`shell=False`、默认 close-fds 与 explicit pass_fds，且 source 已通过 A/静态调用链核验。真实 child probe 可作为后续 Verification 的 bounded recommendation，但不是本 Reliability gate blocker，也不授权本 task 修改 tests。

## 15. R7 — Existing safety invariants

判定：`PASS`。

- T29：foreign inode 被保留，pathname mutation counters 为 zero；
- T30：post-verification foreign replacement 被保留，helper 不做 pathname cleanup；
- T34：failure-path unlink/rename/replace/rmdir 均为 zero，owned artifact retained；
- T35：retained basename 阻止第二次 upload，未触发 cleanup/retry；
- R23 final terminal 仍为 `HOLD_UPLOAD_FAILED_NO_REPLACEMENT`、`classification=NO_MUTATION`、target `OLD_EXACT`，没有被本 review 改写为 deployment PASS；
- T/E contract counters 保持 retry `0`、resume `0`、cleanup `0`、rollback `0`、restart `0`、activation `0`；本 task 无 SSH、remote、upload、deploy、rollback、restart 或 activation。

## 16. Source-byte syntax validation

以下 exact persisted bytes 使用 `compile(path.read_bytes(), path, "exec")` fresh 验证并全部 `PASS`：

- `docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py`；
- `docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py`；
- `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py`；
- `docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py`。

未使用 `py_compile`、`compileall`、`-B`、`PYTHONDONTWRITEBYTECODE` 或 `PYTHONPYCACHEPREFIX`。

## 17. Matrix validation

- T matrix command：`python3 docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py`；
- T33：`PASS`；
- T1-T35：`MATRIX=PASS count=35/35`；
- E matrix command：`python3 docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py`；
- E1-E40：`PASS 40/40`。

## 18. Manifest checks

fresh check results：

- P2-R2 owning directory：`6/6 OK`；
- P2-R3 repository root：`9/9 OK`；
- R24-R1 package from repository root：`5/5 OK`；
- R23 historical evidence manifest：`3/3 OK`。

R24-R1 package manifest 的五个 entries sorted、self-excluded、无 duplicate；未修改任何 active 或 historical manifest。R23 report/final terminal/manifest identity 也保持：report `19121` bytes / `1fa6f78c5fdaa18d79926e484d97615a43915edac82845327c85a90527a86476`，final terminal `12280` bytes / `90cbb77b827f97580d4bbd58d5eafeb6758f950170f0ef5ff6810211498c9e86`。

## 19. Bytecode audit

测试前、T/E matrix 后、probes 后及 report write 前均审计以下 exact evidence trees：

- `docs/reports/evidence/d2_r7b_p2_r2`：`__pycache__=0`、`*.pyc=0`；
- `docs/reports/evidence/d2_r7b_p2_r3`：`__pycache__=0`、`*.pyc=0`；
- `docs/reports/evidence/d2_r7b_i1_r24_r1_parent_fd_findmnt_inheritance_repair`：`__pycache__=0`、`*.pyc=0`。

未执行 cleanup 制造该结果。

## 20. Allowlist audit

本 task 唯一 repository write path 为：

```text
docs/reports/sprint4_d2_r7b_i1_r24_r2_focused_reliability_review.md
```

report 写入前 exact path 为 `ABSENT / NON-SYMLINK`，report parent `docs/reports` 为 real non-symlink directory。未修改或创建 source、tests、manifests、R24-R1 report/package、R23 report/evidence、config、status、roadmap、PM rules、PM handoffs、`.gitignore`、review manifest、helper、fixture、JSON evidence、transcript、sidecar、second report 或 checkout-external report。

## 21. Production blockers

`none`。

没有发现：

- production-reachable `/proc/self/fd/<n>` query without same live inherited FD；
- normal persisted execution reachable compatibility fallback；
- real production TypeError converted into path-only false PASS；
- unrelated FD inheritance；
- parent identity/lock change before upload create；
- mutation before filesystem authority；
- foreign/retained artifact deletion or mutation；
- false PASS authorizing unsafe remote mutation；
- source/manifest/test internal inconsistency。

## 22. Recommendations

1. `R3`：保留当前 fallback 作为明确的 synthetic test compatibility seam；后续 source maintenance 可考虑更显式的 callable capability contract，但本建议不是当前 source repair authority，也不是 HOLD 条件。
2. `R6`：后续 focused Verification 如取得独立授权，可增加一个 real child `/proc/self` bounded check，以补充 T33 fake subprocess boundary；当前 T33 已充分建立 persisted source call contract，缺少该 OS-level child probe 不导致 production false PASS。

上述 recommendations 均满足：`no production false PASS`、`no unauthorized mutation`、`no foreign deletion`、`no production-truth corruption`。本 task 不执行 source/test repair。

## 23. MVP alignment

分类：`MVP-ALIGNED WITH BACKLOG ITEMS`。

本 review 直接服务已批准的 single-file config-only deployment MVP，确认 upload parent filesystem authority 不会被 pathname race 或 child FD inheritance gap 降级。未新增 deployment framework、automated recovery、remote monitoring、Collector lifecycle、multi-node 或 broader production-readiness claim。

## 24. Next gate 与 delivery state

唯一 next gate：

```text
R24-R2 report WRITTEN
→ PM durable report intake
```

若 PM 接受本 `PASS WITH RECOMMENDATIONS`：

```text
→ focused Verification review
→ fresh remote eligibility
→ only then possible new execution authority
```

不得自动进入后续 gate。

Delivery state：

```text
R24-R2 RELIABILITY REPORT WRITTEN
```

该状态仅表示 exact durable report 已写入；不表示 PM-ACCEPTED、VERIFICATION-PASS、REMOTE-AUTHORIZED、DEPLOYED、STAGED、COMMITTED 或 PUSHED。

## 25. Thread context assessment

- 本次输出长度：长；完整 Reliability evidence 保存在 exact repository report，Chat 仅返回 concise manifest；
- 当前 Thread 是否建议继续：`no`；
- 下一轮是否建议新开 Thread：`yes`；
- 理由：本次 focused Reliability review 已完成并交付；下一步是 PM durable report intake，若接受则由独立 focused Verification Thread 处理，不应在当前 Thread 中顺势修改 source/tests、执行 remote 或进入新 execution authority。

## 26. Final local facts

- HEAD unchanged：`8de5edbb504538a233abbcc80102cb714c9cee65`；
- origin/main unchanged：同上；
- ahead/behind：`0/0`；
- cached：empty；
- remote action：not performed；
- Git stage/commit/push：not performed。

