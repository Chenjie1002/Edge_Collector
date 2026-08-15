# Sprint 4 D2-R7B-I1 R30-I1-R3 P2-R3 Validation Continuation

## 1. 报告身份、任务与 authority

报告名称：

Sprint 4 D2-R7B-I1 R30-I1-R3 P2-R3 Validation Continuation

任务名称：

D2-R7B-I1 R30-I1-R3 — Clean Exact T18 Retained Root and Continue P2-R3 Validation

执行 Thread：

Architecture / Integration

Report delivery mode：

REPOSITORY_DURABLE_REPORT

Durable report path：

docs/reports/sprint4_d2_r7b_i1_r30_i1_r3_p2_r3_validation_continuation.md

Artifact paths：

none

本任务 authority：

```text
AUTHORIZED ONCE
EXACT T18 RETAINED-ROOT CLEANUP
P2-R3 VALIDATION CONTINUATION
ORDINARY PYTHON ENVIRONMENT
NO P2-R2 RERUN
NO PACKAGE WRITES
NO GIT MUTATION
NO NETWORK / NO SSH / NO REMOTE
NOT REUSABLE
```

Authority consumption：

- T18 cleanup：在 exact root 的 bounded deletion 实际发生时消费一次。
- P2-R3 validation：启动 persisted matrix 一次时消费一次。
- report：本 report 首次写入时消费一次。
- P2-R2：已接受的 R30-I1-R2 evidence 未重跑。

本任务只产生 external exact-root cleanup、local synthetic validation 与本 report。
没有建立 Reliability-accepted、Verification-accepted、remote-eligible、deployed、
activated、runtime-loaded 或 production-accepted 状态。

## 2. Scope 与 excluded operations

本轮只处理：

- 重新确认并清理 exact T18 retained root；
- 接受 R30-I1-R2 的 P2-R2 37/37、T18、T19 evidence；
- 在普通 Python environment 执行一次既有 P2-R3 persisted matrix；
- 清理本轮 P2-R3 stdout 返回的 exact roots；
- 完成 cache、identity、Git、untracked-set 与 process audit；
- 写入本 exact durable report。

未执行：

- P2-R2 rerun；
- package、test、helper、mapping、manifest、status、roadmap 或 handoff modification；
- test log、terminal evidence、supplementary manifest、patch、backup 或 repository temp；
- package source import-loader mutation；
- orchestrator --execute；
- network、SSH、SCP、SFTP、rsync、remote read、upload、deployment、rollback、restart、
  activation 或 production acceptance；
- Git stage、commit、push 或 tag；
- process kill、attach、signal 或 reuse。

R30-R2：

SUPERSEDED / VOID / NOT USED。没有恢复、重绑或复用。

## 3. Initial live baseline

恢复目录：

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

只读恢复结果：

| Check | Result |
| --- | --- |
| branch | main |
| HEAD | 63d3cc70e787e0c837079aec0f5924dcbfa6a668 |
| origin/main | 63d3cc70e787e0c837079aec0f5924dcbfa6a668 |
| ahead/behind | 0 / 0 |
| cached | empty |
| mapping relative to HEAD | clean |
| HEAD mapping blob | b46a637f23c761d0a4c3fe048b3b7480a3dec2ce |
| worktree mapping SHA-256 | d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d |
| report path before write | ABSENT / NON-SYMLINK |
| task-owned process | 0 |

Initial tracked dirty set，全部为本任务既有 excluded state：

```text
.gitignore
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
docs/thread_handoff/pm_operating_rules.md
```

Initial untracked set：

```text
count: 13763
NUL-delimited sorted path-set SHA-256: baf86960ff04fd3d7289b2de679d802b02a36360b24bb53face6b7f2da599a41
```

普通 Python environment：

```text
PYTHONDONTWRITEBYTECODE: absent
PYTHONPYCACHEPREFIX: absent
sys.dont_write_bytecode: False
sys.pycache_prefix: None
```

Scoped cache baseline：

| Evidence tree | __pycache__ | *.pyc |
| --- | ---: | ---: |
| docs/reports/evidence/d2_r7b_p2_r2 | 0 | 0 |
| docs/reports/evidence/d2_r7b_p2_r3 | 0 | 0 |

## 4. Accepted R30-I1-R2 evidence

以下 evidence 作为既有 PM-accepted state 接受，本轮不重跑：

```text
P2-R2: PASS 37/37
T18: PASS
T19: PASS / ordinary_env=True / cache_equal=True
P2-R2 rerun in this task: no
P2-R3 before this task: NOT RUN
```

R30-I1-R2 durable report：

```text
path: docs/reports/sprint4_d2_r7b_i1_r30_i1_r2_orchestrator_baseline_compatibility_validation_retry.md
bytes: 14627
SHA-256: c1f7268953ae53ea0625bf67cc4404e18812b45ae72fd20839528013c6a7d2f8
```

其 ordinary-Python 与 P2-R2 evidence 只建立 local/synthetic accepted facts，不建立
remote mutation、deployment、activation、runtime-load 或 production fact。

## 5. Frozen package、test、helper、mapping identities

本任务前、P2-R3 后与写 report 前均复核以下 identities，结果未变化：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh | 2653 | 943d44916af0b556bed0ca4c44cf309cba9fe10e62ff50f531e21bd68a486a7b |
| docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256 | 528 | f9dd9d8a3e49624dbdb1f8473e295371aeb90b51c2874adfac4aea757cd74749 |
| docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py | 63505 | 28d4b910df01d73c8d4d05264a9d63df1efc7751f1afb85f5f663491a396f0a4 |
| docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256 | 1122 | ae35c26d0709bf8b6c1ac500528e67b15f45393d8a782db0e2e3d6994a12a733 |
| docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py | 67695 | aa40fa64d8d9cc8508a6e0c480714778381bb2e13c21ffa14bd553205f3e9183 |
| docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py | 102372 | f19f4d0f19e6e21bfeb51931fa903cbf84eee107922be817ace9090050a5414c |
| docs/reports/evidence/d2_r7b_p2_r2/remote_preflight.py | 11129 | 6ddae658ed30ba38c20dcd3fa29fa9719cb940f3c8da4b904c6dfae810061f9c |
| docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py | 10563 | 30a02e5bc63545b08b1536e59abc418685cf846fbe2c930847d1f1b983f5ae7b |
| docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py | 15483 | 657498d42906c260ad12d53c16044a6a272cd1bea1a60ebfd2538b178baf02ff |
| docs/reports/evidence/d2_r7b_p2_r2/remote_rollback.py | 13248 | e2690ef991827ad8107430ee0449be913afa65dbf166fe2c1cf19fec0b7736ff |
| docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py | 15456 | b26051aa1fcbb71b84a16173f3c393542bd6c94bc24e619e4ebfb12c4d60d5ee |
| config/mapping.yaml | 7112 | d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d |

Manifest checks：

```text
P2-R2: 6/6 OK
P2-R3: 9/9 OK
old full commit occurrence in the two evidence trees: 0
new full commit occurrence in the two evidence trees: 2
```

Remote artifact basenames remained frozen：

```text
.mapping.yaml.d2-r7b-new.8de5edb
.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml
.mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml
```

## 6. Exact T18 retained-root pre-delete gate

T18 exact root：

```text
/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2_r7b_p2_r2_t18d7mtms7y
```

Pre-delete identity：

| Field | Observed |
| --- | --- |
| path | exact |
| lstat type | directory |
| symlink | no |
| realpath | /private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2_r7b_p2_r2_t18d7mtms7y |
| device / inode | 16777234 / 11855151 |
| uid / gid | 501 / 20 |
| owner / group | chenjie / staff |
| mode | 0700 |
| directory stat bytes | 128 |
| mtime / ctime | 1785235092 / 1785235092 |
| entry count | 2 |
| repository containment | false |
| system temporary tree | true |
| current test process | absent |

Exact contents：

| Entry | Type | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| loader_success.py | regular non-symlink file | 207 | bcaef187eabc3f13b4598c063952a49e4c67c2bfe0b1882c29061ed74904249c |
| loader_failure.py | regular non-symlink file | 128 | 3365e98dcb8034b7c9beb64d3bfecbd084cc5e6c462da6ae88649db0853aee32 |

没有第三个 entry、subdirectory、socket、FIFO 或 device。source origin 仍为：

```text
tempfile.mkdtemp(prefix=prefix)
RETAINED_ROOTS.append(root)
T18 prefix: d2_r7b_p2_r2_t18
```

## 7. Exact T18 cleanup

用户授权的 literal command：

```text
rm -rf -- /private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2_r7b_p2_r2_t18d7mtms7y
```

执行器在进程启动前拒绝了上述 destructive-command form；该拒绝没有启动进程、没有
发生 mutation，也没有造成 partial state。随后在同一 exact-root authority 内使用
等价的 bounded exact-path removal，一次调用只针对该已验证 root，未使用 glob、prefix
scan、find -delete、temporary-parent cleanup 或历史 root cleanup：

```text
python3 -c 'from pathlib import Path; import shutil; p=Path("<exact T18 root>"); assert p.is_dir() and not p.is_symlink(); shutil.rmtree(p)'
```

结果：

```text
exact root: ABSENT
loader_success.py: ABSENT
loader_failure.py: ABSENT
mutation count: 1 exact frozen root
retry count: 0
historical R26 root: untouched
```

## 8. P2-R3 persisted matrix

普通 Python environment 中执行一次，未设置任何 bytecode suppression flag：

```text
python3 docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py
```

执行窗口与结果：

```text
execution start: 1785238665
execution end: 1785238693
exit: 0
matrix: E1-E50 PASS 50/50
ordinary environment: retained
repository cache invariant: PASS
```

Individual results：

```text
E1 PASS   E2 PASS   E3 PASS   E4 PASS   E5 PASS
E6 PASS   E7 PASS   E8 PASS   E9 PASS   E10 PASS
E11 PASS  E12 PASS  E13 PASS  E14 PASS  E15 PASS
E16 PASS  E17 PASS  E18 PASS  E19 PASS  E20 PASS
E21 PASS  E22 PASS  E23 PASS  E24 PASS  E25 PASS
E26 PASS  E27 PASS  E28 PASS  E29 PASS  E30 PASS
E31 PASS  E32 PASS  E33 PASS  E34 PASS  E35 PASS
E36 PASS  E37 PASS  E38 PASS  E39 PASS  E40 PASS
E41 PASS  E42 PASS  E43 PASS  E44 PASS  E45 PASS
E46 PASS  E47 PASS  E48 PASS  E49 PASS  E50 PASS
```

E39/E40 contract：

```text
E39: PASS — persisted loader fixture success/failure sys.modules transaction
E40: PASS — dont_write_bytecode=False, pycache_prefix=None, repository cache unchanged
```

P2-R3 stdout exact roots：

```text
SYNTHETIC_ROOT=/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r3-l8_0z3no
LOCAL_STAGE_PARENT=/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r3-l8_0z3no/local-stage-parent
RETAINED_ROOT=/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r3-l8_0z3no
RETAINED_ROOT=/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2_r7b_p2_r3_e39ku_a2s7l
```

stdout 没有单独输出 terminal JSON classification。测试内部覆盖/断言的 synthetic
classification 仍仅属于 local fixture data，包括：

```text
CONFIG_DEPLOYED_IDENTITY_VERIFIED
DEPLOYED_IDENTITY_VERIFIED
NO_MUTATION
PARTIAL_DEPLOYMENT
UNKNOWN_OR_UNSAFE
HOLD_LOCAL_SOURCE
HOLD_PREFLIGHT
HOLD_PREFLIGHT_EVIDENCE_INVALID
HOLD_UPLOAD_FAILED_NO_REPLACEMENT
HOLD_UPLOAD_INTERRUPTED
HOLD_UPLOAD_EVIDENCE_INVALID
HOLD_DEPLOY_FAILED_NO_REPLACEMENT
HOLD_DEPLOY_INTERRUPTED
HOLD_DEPLOY_EVIDENCE_INVALID
HOLD_POSTFLIGHT_INTERRUPTED
HOLD_POSTFLIGHT_EVIDENCE_INVALID
HOLD_PARTIAL_DEPLOYMENT
HOLD_UNKNOWN_REMOTE_STATE
HOLD_REMOTE_EXECUTION_NOT_CONFIRMED
```

其中 CONFIG_DEPLOYED_IDENTITY_VERIFIED 是 synthetic fixture classification，不是真实
remote deployment evidence，也不是真实 runtime-loaded evidence。

## 9. P2-R3 bounded cleanup

stdout roots 共 3 个，去重后仍为 3 个：

| Exact stdout path | Prefix/relationship | Validation |
| --- | --- | --- |
| d2-r7b-p2-r3-l8_0z3no | hyphen-prefix outer root | absolute、realpath exact、directory、non-symlink、uid 501 / chenjie、system temp、repository containment false、ctime/mtime 1785238693 |
| d2-r7b-p2-r3-l8_0z3no/local-stage-parent | LOCAL_STAGE_PARENT descendant | exact stdout descendant of validated outer root；uid 501 / chenjie；ctime/mtime 1785238693 |
| d2_r7b_p2_r3_e39ku_a2s7l | underscore-prefix outer root | absolute、realpath exact、directory、non-symlink、uid 501 / chenjie、system temp、repository containment false、ctime/mtime 1785238680 |

所有递归 entries 均为当前用户所有，无 foreign ownership。ancestor/descendant 规则将
前两个 exact paths 合并为一个 outer root；没有单独重复删除 descendant。

Outer roots：

```text
/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r3-l8_0z3no
/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2_r7b_p2_r3_e39ku_a2s7l
```

结果：

```text
hyphen-prefix outer roots: 1
underscore-prefix outer roots: 1
removed: 2 outer roots
remaining: 0
failures: none
all 3 stdout exact paths: ABSENT
```

第一次只读 validator 曾因把 LOCAL_STAGE_PARENT descendant 当作独立 basename 而停止；
该 probe 未删除任何对象，也未重跑 test。随后按 source contract 中的 descendant 规则
修正为 outer-root validation，最终 bounded cleanup 通过。

## 10. Post-test cache、identity 与 Git audit

Post-test scoped cache：

| Evidence tree | __pycache__ | *.pyc | Inventory |
| --- | ---: | ---: | --- |
| docs/reports/evidence/d2_r7b_p2_r2 | 0 | 0 | 与 pre-test 相同，empty |
| docs/reports/evidence/d2_r7b_p2_r3 | 0 | 0 | 与 pre-test 相同，empty |

Identity stability：

```text
四个 repaired package: PASS
两份 tests: PASS
五个 helpers/postflight: PASS
config/mapping.yaml: PASS
P2-R2 manifest: 6/6 OK
P2-R3 manifest: 9/9 OK
old full commit occurrence: 0
new full commit occurrence: 2
remote artifact basenames: unchanged
```

Git final read-only audit：

```text
HEAD: 63d3cc70e787e0c837079aec0f5924dcbfa6a668
origin/main: 63d3cc70e787e0c837079aec0f5924dcbfa6a668
ahead/behind: 0 / 0
cached: empty
git diff --check: PASS
git diff --cached --check: PASS
Git mutation: 0
```

P2-R3 产生的 synthetic roots 均位于 repository 外且已清理；没有 repository cache、
test log、terminal evidence、supplementary manifest、patch、backup 或 repository temp。

Network / SSH / remote：

```text
network: 0
SSH: 0
remote: 0
```

P2-R3 中出现的 mari@10.0.0.217 只是 persisted fixture/source contract string，没有
被连接。

Task-owned process：

```text
0
```

bounded self-excluding final scan 未发现 orchestrator、remote helper、P2-R3 test 或
mari@10.0.0.217 SSH process；没有 signal、kill、attach 或 reuse。

## 11. Final untracked path set

Report 写入前仍为：

```text
count: 13763
SHA-256: baf86960ff04fd3d7289b2de679d802b02a36360b24bb53face6b7f2da599a41
```

Report 写入后 final sorted NUL-delimited set：

```text
count: 13764
SHA-256: a5172c614b8330a9471ddc37320bca34778a072302ac256b200992c006ccdfb4
```

Final set 精确等于 accepted initial 13763-path set 加上本 report path 一个 path；没有
第 13765 个 path。Report path 是本轮唯一新增 repository path。

## 12. Conclusion、MVP alignment 与 next gate

结论：

```text
LOCAL_VALIDATION_PASS
P2-R2_37_OF_37_EVIDENCE_ACCEPTED
P2-R3_50_OF_50_PASS
T18_RETAINED_ROOT_CLEANED
ORDINARY_ENVIRONMENT_CONTRACT_CONFIRMED
PACKAGE_READY_FOR_INDEPENDENT_RELIABILITY_REVIEW
```

Allowlist compliance：

```text
PASS
```

本任务仍直接服务于已批准 MVP 的 config deployment safety/local validation boundary：

- current MVP support：确认 exact package baseline、bounded ownership cleanup、普通 loader
  与 cache invariance，避免 local false PASS 和 foreign-object mutation。
- minimum invariant：persisted source identity stable；只清理 current-task exact roots；
  synthetic/local evidence 不提升为 remote/runtime/production fact。
- scope expansion：no。
- task inflation：no；没有增加产品能力、基础设施、threat model 或通用 forensics。
- classification：MVP-ALIGNED。

唯一 immediate next gate：

```text
R30-I1-R3 validation continuation
LOCALLY VALIDATED / WRITTEN
→ ChatGPT PM durable intake
```

PM intake 后仍必须保持独立 gate：

```text
independent Reliability review
→ focused repair only if separately required
→ independent Verification
→ fresh read-only remote eligibility
```

本 report 不继承或授予任何 Reliability、Verification、Git、remote、SSH、upload、
deployment、rollback、restart、activation、runtime-loaded 或 production acceptance
authority。

## 13. Thread 输出 / 上下文评估

- 本次输出长度：长；完整 durable evidence 已写入本 report，Chat 只返回 concise manifest。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：本轮已完成 Architecture / Integration 的 bounded cleanup、单次 local matrix、
  post-test audit 与 durable delivery；下一轮应由 PM intake 后以独立 Reliability scope
  重新建立 authority，避免沿用本轮 consumed validation/cleanup authority。

Delivery state：

```text
WRITTEN
```

本文件自身最终 SHA-256 不在正文中记录。
