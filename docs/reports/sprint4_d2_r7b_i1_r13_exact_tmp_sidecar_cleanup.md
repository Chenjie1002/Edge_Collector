# Sprint 4 D2-R7B-I1 R13 Exact Temporary Sidecar Cleanup Report

## 1. 报告名称

`Sprint 4 D2-R7B-I1 R13 Exact Temporary Sidecar Cleanup Report`

## 2. 任务名称

`D2-R7B-I1 R13 — Exact /tmp Sidecar Cleanup`

## 3. 执行 Thread

`Architecture / Integration`

## 4. 结论

`R13 exact /tmp sidecar cleanup: PASS`

两个 frozen exact sidecars 均完成 exact single-file deletion，两个路径最终均为 absent；未删除任何父目录、其他 `/tmp` entry 或 repository bytecode。R12 V12 blocker prerequisite：`CLEANUP COMPLETED`。

本结论不改变 R12 Verification 当前状态：`V1–V11 PASS`、`N1–N5 PASS`、`V12 HOLD`、overall `HOLD / PM ACCEPTED`。

## 5. Scope

本任务仅覆盖：

- `/Users/chenjie/Documents/MES/edge-mes-demo` exact checkout 的 read-only recovery；
- 指定 repository artifacts、manifests、source/config identities、Git baseline 和 zero-bytecode 的删除前/删除后审计；
- 两个 exact `/tmp` sidecar 的 frozen identity 核验；
- 对两个 exact files 各执行一次 `os.unlink()`；
- 写入本 exact R13 durable report。

未执行 tests、probes、full pytest、syntax/compile checks、SSH、remote read/mutation、Docker、Compose、Collector runtime、config deployment、Second I1、retry、resume、rollback、restart、activation、Git stage、commit 或 push。

## 6. Authority

本任务仅使用用户对以下两个 exact external files 的一次性删除授权：

1. `/tmp/d2_r7b_r12_post_manifest_p2r3.out`
2. `/tmp/d2_r7b_r12_post_manifest_i1.out`

该 authority 未扩展到 `/tmp`、其他 sidecar、父目录、repository cleanup、R12 修改、Verification closeout、remote/runtime 或 Git mutation。

当前 gate 保持：

- First D2-R7B-I1：`EXECUTED ONCE / INTERRUPTED / AUTHORITY CONSUMED`；
- remote mutation：`NOT PROVEN`；
- deployment identity：`NOT ESTABLISHED`；
- runtime config load：`NOT ESTABLISHED`；
- Collector activation：`NOT ESTABLISHED`；
- Second I1：`NOT AUTHORIZED / NOT EXECUTED`；
- Git closeout：`NOT AUTHORIZED / NOT EXECUTED`。

## 7. Workspace

- workspace mode：`checkout`；未创建 worktree；
- `pwd`：`/Users/chenjie/Documents/MES/edge-mes-demo`；
- report parent：`/Users/chenjie/Documents/MES/edge-mes-demo/docs/reports`；
- report parent：real directory、非 symlink、realpath exact match；
- R13 report target 删除前：`ABSENT / NON-SYMLINK`。

`/tmp` 在本机的 `lstat()` 类型为系统 symlink；R13 未删除或修改该 parent path，只对两个已通过 `lstat()` frozen identity 的 regular files 执行 exact unlink。

## 8. Files read

以下文件按任务要求顺序读取，均为 read-only：

1. `docs/thread_handoff/pm_operating_rules.md`
2. `docs/current_status.md`
3. `docs/thread_handoff/chatgpt_pm_handoff_260725-1434.md`
4. `docs/reports/sprint4_d2_r7b_i1_r12_focused_verification_review.md`
5. `docs/reports/sprint4_d2_r7b_i1_r11_focused_reliability_rereview.md`
6. `docs/reports/sprint4_d2_r7b_i1_r10_r1_required_path_correction_exact_bytecode_cleanup.md`
7. `docs/reports/sprint4_d2_r7b_i1_remote_config_mutation_execution.md`
8. `docs/reports/evidence/d2_r7b_i1/final_terminal.json`
9. `docs/reports/evidence/d2_r7b_i1/manifest.sha256`
10. `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py`
11. `docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py`
12. `docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py`
13. `docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py`
14. `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256`
15. `config/mapping.yaml`
16. `/tmp/d2_r7b_r12_post_manifest_p2r3.out`
17. `/tmp/d2_r7b_r12_post_manifest_i1.out`

## 9. Current gate

R10-R1 cleanup：`PASS / PM ACCEPTED`。

R11 Reliability：`PASS / PM ACCEPTED`。

R12 Verification：`V1–V11 PASS`、`N1–N5 PASS`、`V12 HOLD`、overall `HOLD / PM ACCEPTED`。

R12 的 HOLD 原因是最终 manifest audit 误写两个 checkout 外 `/tmp` sidecars。本 R13 只完成该 cleanup prerequisite，不改写 R12，不将 R12 改为 Verification PASS。

## 10. R12 report identity

| Path | Bytes | SHA-256 | Result |
| --- | ---: | --- | --- |
| `docs/reports/sprint4_d2_r7b_i1_r12_focused_verification_review.md` | 20608 | `f68a2a247cef21f622a1ca4572a0615cf70edf9588fd11add65c8b3c3755ffab` | matched |

## 11. Initial Git baseline

删除前 live preflight：

- branch：`main`；
- HEAD：`8de5edbb504538a233abbcc80102cb714c9cee65`；
- origin/main：`8de5edbb504538a233abbcc80102cb714c9cee65`；
- ahead / behind：`0 / 0`；
- cached diff：empty；
- `git diff --check`：`PASS`；
- `git diff --name-only`：`.gitignore`、`docs/thread_handoff/pm_operating_rules.md`。

已知 tracked dirty artifacts 为 `.gitignore` 与 `docs/thread_handoff/pm_operating_rules.md`。既有 untracked reports、evidence、handoffs、frontend generated artifacts 与 `frontend/node_modules/` 均保留并排除；R13 未对其执行 cleanup 或 staging。

## 12. Initial manifests

删除前直接执行 manifest checks，未使用 `>`、`>>`、`tee`、output capture sidecar 或 temporary log：

- P2-R3：`9/9 OK`；manifest identity `e7cfd92930e6a697e50b850ad06fad912455a6b564b9b747d71a6544b16d7bd3`；
- I1：`2/2 OK`；manifest identity `8b2f3718316b0879033de29256826f3d589556afd70d5e7433c55de79ab50e16`。

## 13. Initial source identities

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py` | 45783 | `eea3e8778cc94c78a0931b2404f888a78176996cd1a4421a7442667c8b859085` |
| `docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py` | 15456 | `b26051aa1fcbb71b84a16173f3c393542bd6c94bc24e619e4ebfb12c4d60d5ee` |
| `docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py` | 81566 | `465c83b02110e39c9fe4d7e5626a083256d3ed8bc86d9d44cf4f942d844b2b09` |
| `docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py` | 26635 | `aabed2243fc86ab43697752e9996ff07a1c7c967d845f10a6ba0dc9f4d00303a` |
| `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256` | 1122 | `e7cfd92930e6a697e50b850ad06fad912455a6b564b9b747d71a6544b16d7bd3` |
| `docs/reports/evidence/d2_r7b_i1/manifest.sha256` | 251 | `8b2f3718316b0879033de29256826f3d589556afd70d5e7433c55de79ab50e16` |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` |

## 14. Initial zero-bytecode state

删除前 scoped scan：

- `docs/reports/evidence/d2_r7b_p2_r2`：`0 __pycache__`、`0 *.pyc`；
- `docs/reports/evidence/d2_r7b_p2_r3`：`0 __pycache__`、`0 *.pyc`。

## 15. Sidecar 1 frozen identity

Path：`/tmp/d2_r7b_r12_post_manifest_p2r3.out`

- file type：regular file；
- symlink：`false`；
- bytes：`564`；
- SHA-256：`fa78e4762d462b1b9e21499929258f52ec0f6c6ab256ea41a815a26baa5ad29b`；
- `mtime_ns`：`1784994051810972971`；
- content exact：`true`；
- frozen identity result：`matched`。

## 16. Sidecar 2 frozen identity

Path：`/tmp/d2_r7b_r12_post_manifest_i1.out`

- file type：regular file；
- symlink：`false`；
- bytes：`127`；
- SHA-256：`de733b0afe488af7cba84b4c261b0ffc7df9a0042c8a4e1887b8c869c7e708b8`；
- `mtime_ns`：`1784994051824315772`；
- content exact：`true`；
- frozen identity result：`matched`。

## 17. Sidecar contents

Sidecar 1 仅包含 P2-R3 composite manifest 的九条 `OK` 输出：

```text
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh: OK
docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py: OK
docs/reports/evidence/d2_r7b_p2_r2/remote_preflight.py: OK
docs/reports/evidence/d2_r7b_p2_r2/remote_rollback.py: OK
docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py: OK
docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py: OK
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py: OK
docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py: OK
docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py: OK
```

Sidecar 2 仅包含 I1 manifest 的两条 `OK` 输出：

```text
docs/reports/sprint4_d2_r7b_i1_remote_config_mutation_execution.md: OK
docs/reports/evidence/d2_r7b_i1/final_terminal.json: OK
```

## 18. Exact cleanup execution

所有 preflight 通过后按 exact 顺序执行：

1. 对 Sidecar 1 exact path 执行一次 `os.unlink('/tmp/d2_r7b_r12_post_manifest_p2r3.out')`；
2. 立即确认 Sidecar 1 `absent=True`、`symlink_absent=True`；
3. 再次核对 Sidecar 2 frozen identity；
4. 对 Sidecar 2 exact path 执行一次 `os.unlink('/tmp/d2_r7b_r12_post_manifest_i1.out')`；
5. 立即确认 Sidecar 2 `absent=True`、`symlink_absent=True`。

`os.unlink()` 调用数：`2`，每个 exact path 一次。没有 retry、第二轮 cleanup、wildcard、glob、`find -delete`、`rm -r`、`rm -rf`、parent deletion 或其他 `/tmp` scan/cleanup。

## 19. Post-delete absence checks

- `/tmp/d2_r7b_r12_post_manifest_p2r3.out`：`ABSENT`；symlink：`ABSENT`；
- `/tmp/d2_r7b_r12_post_manifest_i1.out`：`ABSENT`；symlink：`ABSENT`；
- `/tmp` parent：retained，未执行 deletion；
- `/Users/chenjie/Documents/MES/edge-mes-demo/docs/reports` parent：retained，real directory、非 symlink；
- parent directories deleted：`none`。

## 20. Post-cleanup manifests

删除后再次直接执行两份 manifest checks，未写入任何 output file：

- P2-R3：`9/9 OK`；
- I1：`2/2 OK`。

## 21. Post-cleanup zero-bytecode

- `docs/reports/evidence/d2_r7b_p2_r2`：`0 __pycache__`、`0 *.pyc`；
- `docs/reports/evidence/d2_r7b_p2_r3`：`0 __pycache__`、`0 *.pyc`。

R13 未执行 repository bytecode cleanup，也未重跑任何 tests/probes。

## 22. Final source/report identities

删除后重新核对，以下 identities 全部稳定：

- R12 report：20608 bytes，SHA-256 `f68a2a247cef21f622a1ca4572a0615cf70edf9588fd11add65c8b3c3755ffab`；
- R11 report：17401 bytes，SHA-256 `e524ba29987862ef7277b26fabbd22e61a00c4e510a449d2aacfb6079e07e522`；
- R10-R1 report：17289 bytes，SHA-256 `431e73247ab7c3cfc3954768d626c4fcb3f54b56cf9cd38595eba7590d2ef42d`；
- historical execution report：5631 bytes，SHA-256 `2c88906dd61df1cf3dd298135a1d7f82585f3a6787379ce27c1dbbd11d53ad1b`；
- `remote_i1_orchestrator.py`：`eea3e8778cc94c78a0931b2404f888a78176996cd1a4421a7442667c8b859085`；
- `remote_postflight.py`：`b26051aa1fcbb71b84a16173f3c393542bd6c94bc24e619e4ebfb12c4d60d5ee`；
- P2-R3 test：`465c83b02110e39c9fe4d7e5626a083256d3ed8bc86d9d44cf4f942d844b2b09`；
- P2-R2 test：`aabed2243fc86ab43697752e9996ff07a1c7c967d845f10a6ba0dc9f4d00303a`；
- P2-R3 manifest：`e7cfd92930e6a697e50b850ad06fad912455a6b564b9b747d71a6544b16d7bd3`；
- I1 manifest：`8b2f3718316b0879033de29256826f3d589556afd70d5e7433c55de79ab50e16`；
- `config/mapping.yaml`：`d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`。

R13 report 的自身 bytes/SHA-256 在写入后由 Chat-window manifest 计算，避免在 durable report 内形成自引用 hash。

## 23. Final Git state

R13 report 写入前的 post-cleanup repository status baseline 为 `13695` status entries，status SHA-256 `b3e29a30f80b73c7e2240f4e9ac27fdb6840b9710665f71c07c3d7d1402a5dab`；该 baseline 包含既有 dirty artifacts，不包含 R13 report。

写入 R13 report 后必须只新增本 exact report；最终审计确认：

- branch：`main`；
- HEAD：`8de5edbb504538a233abbcc80102cb714c9cee65`，unchanged；
- origin/main：`8de5edbb504538a233abbcc80102cb714c9cee65`，unchanged；
- ahead / behind：`0 / 0`；
- cached：empty；
- `git diff --check`：`PASS`；
- staged：`no`；
- committed：`no`；
- pushed：`no`；
- pre-existing tracked dirty artifacts：preserved；
- pre-existing untracked reports/evidence/handoffs/frontend artifacts：preserved；
- newly written repository file：only `docs/reports/sprint4_d2_r7b_i1_r13_exact_tmp_sidecar_cleanup.md`。

## 24. Changed/deleted object allowlist

| Object | Classification | Result |
| --- | --- | --- |
| `/tmp/d2_r7b_r12_post_manifest_p2r3.out` | deleted external file | exact frozen identity matched; deleted once |
| `/tmp/d2_r7b_r12_post_manifest_i1.out` | deleted external file | exact frozen identity matched; deleted once |
| `docs/reports/sprint4_d2_r7b_i1_r13_exact_tmp_sidecar_cleanup.md` | written repository report | only repository write; not staged |
| Existing evidence/synthetic roots | retained synthetic root | retained; no R13 cleanup |
| `.gitignore` | pre-existing tracked dirty artifact | retained; not modified by R13 |
| `docs/thread_handoff/pm_operating_rules.md` | pre-existing tracked dirty artifact | retained; not modified by R13 |
| Existing untracked reports/evidence/handoffs/frontend artifacts | pre-existing dirty artifacts | retained and excluded |
| `/tmp` and all parent directories | retained parent objects | no deletion |

## 25. Blockers

R13 cleanup blockers：`none`。

未关闭的上层 boundary 保持原样：R12 `V12 HOLD`、overall D2-R7B-I1 `HOLD / PM ACCEPTED`。这不是 R13 cleanup failure，也未在本任务中修复或重判。

## 26. Recommendations

`Recommendations: none`

## 27. Next gate

唯一 next gate：`PM durable report intake`。

本 Thread 不进入 Verification closeout，不修改 R12，不执行 Second I1，不进入 remote/runtime，不进行 Git closeout，也不更新 status 或 handoff。

## 28. MVP 路径一致性

- 是否服务 approved MVP：`yes`；
- 目的：删除 R12 最终审计误写的两个 exact sidecars，恢复 Verification closeout 的最小前置条件；
- 防止 allowlist false PASS：`yes`；
- 防止 unrelated `/tmp` object deletion：`yes`；
- 新产品能力：`no`；
- 新 generic cleanup/forensics framework：`no`；
- task inflation：`no`；
- classification：`MVP-ALIGNED`。

## 29. Thread 输出 / 上下文评估

本 Thread 是独立的一次性 Level 1 exact external artifact cleanup。R12 Verification Thread 的 authority 未被继承；cleanup authority 仅来自本任务明确授权。完整命令输出和完整 durable report 不复制到 Chat；Chat 仅交付 concise manifest。写入本报告并交付 manifest 后立即停止，等待 PM durable intake。

## 30. Delivery state

`WRITTEN`

本报告不得解读为 PM accepted、Verification passed、V12 closed、overall D2-R7B-I1 passed、staged、committed、pushed、deployed 或 activated。
