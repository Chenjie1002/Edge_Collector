# Sprint 4 D2-R7B-I1 R27-R2 Mutation Helper JSON Contract Focused Reliability Review

## 1. 报告、任务、Thread 与 Authority 身份

- 报告名称：Sprint 4 D2-R7B-I1 R27-R2 Mutation Helper JSON Contract Focused Reliability Review
- 任务名称：D2-R7B-I1 R27-R2 — Independent Reliability Review of Canonical Mutation Helper JSON Contract
- 执行 Thread：Reliability
- Authority ID：`PM-R27-R2-260728-REL-01`
- 任务规模：中 / Level 2 focused review
- Report delivery mode：`REPOSITORY_DURABLE_REPORT`
- Exact report path：`docs/reports/sprint4_d2_r7b_i1_r27_r2_mutation_helper_json_contract_reliability_review.md`
- 写 authority：仅本 exact report path
- Source/test/manifest repair：未授权、未执行
- Remote / SSH：未授权、`0` calls
- Git stage / commit / push / tag：未授权、未执行

## 2. 结论

结论：`HOLD`。

发现三个 production-reachable blocker：

1. upload helper 可以在已验证 FD 对应的 basename 被外来 inode 替换后仍以 exit `0` 输出 `status=PASS`；JSON 的 inode、bytes、SHA-256 描述已脱离命名路径的原 task-owned FD 对象，而 `path` / `realpath` 指向外来对象。
2. deploy helper 没有强制 `source_upload_temp.inode == target.inode_after`，最终 target/backup 检查也不是 opened-FD-bound identity transaction；同目录外部替换可以使 success JSON 把 `CONSUMED_BY_ATOMIC_REPLACE` source 与另一 final target inode 混为一次完整、无歧义的 success evidence。
3. persisted orchestrator 仅要求 return-code-0 stdout 可解码为任意 JSON object；`{}` 不会被 `_normalize_invalid_child_json()` fail closed，且实际 `execute()` 会继续启动 `REMOTE_DEPLOY`。因此 phase acceptance 仍可仅依赖 child return code 加“任意 object”，没有验证 canonical helper success schema、`status` 或 `phase`。

上述分别满足本 Prompt 的 upload identity false-PASS、deploy identity ambiguity 和 invalid upload evidence authorizing a later mutation 的 HOLD 条件。按 stop condition，本 review 在两只必要的本地 blocker-confirmation probes 后停止，没有运行 T1–T37、E1–E45 或 source-byte compile，也没有修复 source、tests 或 manifests。

## 3. Scope 与明确排除

已审查：

- 两个 persisted mutation helper 的 success/failure control flow 与 exact final bytes；
- preflight、rollback、orchestrator、postflight 的相邻 boundary；
- T1–T37 与 E1–E45 persisted test source，重点为 T29/T30/T36/T37、fake SSH 与 E41–E45；
- P2-R2 / P2-R3 manifests；
- corrected R27-R1 durable report；
- R26 report、terminal、manifest 与 retained stage-root identity；
- `config/mapping.yaml` identity；
- live Git、output path、cache 与 process boundaries。

明确未执行或未触碰：

- 未修改 helper、tests、manifests、orchestrator、preflight、postflight、rollback、materializer、mapping、R26/R27-R1 evidence 或治理文件；
- 未执行 SSH、SCP、SFTP、rsync、remote inspection、cleanup、deploy、rollback、retry、resume、Collector、Docker 或 Compose lifecycle；
- 未使用 R26 retained stage root 作为 fixture 或执行输入；
- 未执行 Git stage、commit、push、tag、reset、stash 或 clean；
- 未建立 Data Quality、runtime-load、activation、production-data 或 production acceptance claim。

## 4. Fresh Git baseline

在 exact checkout root 执行 live recovery，结果：

```text
repository: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 8de5edbb504538a233abbcc80102cb714c9cee65
origin/main: 8de5edbb504538a233abbcc80102cb714c9cee65
ahead/behind: 0/0
cached: empty
git diff --check: PASS
config/mapping.yaml relative to HEAD: clean
```

pre-existing tracked dirty / excluded 与 Prompt 一致：

```text
.gitignore
docs/current_status.md
docs/thread_handoff/pm_operating_rules.md
```

其余既有 untracked reports/evidence/frontend artifacts 保持 excluded。`docs/current_status.md` 的最高 durable section 仍是旧 R17-R4 snapshot；本 review 以用户本轮明确的 `PM-R27-R2-260728-REL-01` 与 accepted corrected R27-R1 exact path 为当前 authority，未修改该预存 dirty status 文件，也未由其继承任何 later-phase authority。

## 5. Output preflight

写报告前 exact output path：

```text
docs/reports/sprint4_d2_r7b_i1_r27_r2_mutation_helper_json_contract_reliability_review.md
ABSENT
NON-SYMLINK by lstat ENOENT
parent docs/reports: real directory, non-symlink
parent realpath: /Users/chenjie/Documents/MES/edge-mes-demo/docs/reports
```

没有 pre-existing path/parent collision；未覆盖、删除、改名或复用任何文件。

## 6. Initial accepted identities

全部为 regular non-symlink：

| Path | Bytes | SHA-256 | Result |
| --- | ---: | --- | --- |
| `docs/reports/sprint4_d2_r7b_i1_r27_r1_mutation_helper_json_contract_repair.md` | 10155 | `8a5a92f09e5c405331a68c4bb2d97f9999a175a0b6bf1a17b9590fe5dcd8968f` | MATCH |
| `docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py` | 10563 | `30a02e5bc63545b08b1536e59abc418685cf846fbe2c930847d1f1b983f5ae7b` | MATCH |
| `docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py` | 15483 | `657498d42906c260ad12d53c16044a6a272cd1bea1a60ebfd2538b178baf02ff` | MATCH |
| `docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py` | 67695 | `aa40fa64d8d9cc8508a6e0c480714778381bb2e13c21ffa14bd553205f3e9183` | MATCH |
| `docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256` | 528 | `2ae13bd6dc17167f98d2d59efd882e8a568d5c0ae6f36cbbb9ecb6f2d21086dd` | MATCH |
| `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py` | 45783 | `eea3e8778cc94c78a0931b2404f888a78176996cd1a4421a7442667c8b859085` | MATCH |
| `docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py` | 15456 | `b26051aa1fcbb71b84a16173f3c393542bd6c94bc24e619e4ebfb12c4d60d5ee` | MATCH |
| `docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py` | 89604 | `d1dc0962995686b171cef0b134036ee5fbe24f3b8055b02b68d1fa5e68a871f5` | MATCH |
| `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256` | 1122 | `18edbdc940d1eaef4edbc9dc831dee38716704194b05b564dfc8fb1a6da24714` | MATCH |

相邻 frozen source identities：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `remote_preflight.py` | 11129 | `6ddae658ed30ba38c20dcd3fa29fa9719cb940f3c8da4b904c6dfae810061f9c` |
| `remote_rollback.py` | 13248 | `e2690ef991827ad8107430ee0449be913afa65dbf166fe2c1cf19fec0b7736ff` |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` |

## 7. Exact repair delta 与 persisted final-byte review

本 evidence tree 为 pre-existing untracked authority，Git 没有可用的 tracked before/after textual diff。Reliability 没有把这一点替换成 implementation report 的结论；审查对象是上表 exact persisted final bytes，并用 R27-R1 report 中冻结的 pre-repair identities/RED 描述限定 delta：

- upload：新增 canonical JSON serialization；`upload()` 返回身份字段；`main()` 写 compact sorted JSON；
- deploy：新增 canonical nested JSON；捕获 pre-rename upload identity、final target/backup fields；`main()` 写 compact sorted JSON；
- P2-R2 tests：新增 T36/T37；
- P2-R3 fake SSH：success 路径改为执行 persisted helper `main()`；新增 E41–E45；
- 两份 manifests 更新为当前 exact hashes；
- orchestrator 与 postflight bytes 保持不变。

结论来自 current final control flow，而不是继承 R27-R1 implementation PASS。

## 8. R1 — Canonical success-output framing

判定：`PASS`（framing only）。

两个 persisted `main()` 均直接使用：

```text
json.dumps(..., sort_keys=True, separators=(",", ":")) + "\n"
sys.stdout.write(...)
return 0
```

因此 canonical formatting 由 helper `main()` 自身实现，不依赖 fake SSH wrapper。upload blocker probe 也观察到 exit `0`、stderr empty、exact one physical JSON line、one trailing newline 与 `status=PASS`。两个 helpers 的 success top-level/nested key sets 在 persisted tests 中为 exact set assertions。

本项只确认 byte framing/determinism；它不证明 JSON 内字段和命名 filesystem object 真实绑定。该 truthfulness failure 由 R2/R3 单独 HOLD。

## 9. R2 — Upload success identity truthfulness

判定：`HOLD`。

已确认的正面控制：

- stdin bytes/SHA 在 create 前完整验证；
- parent 使用 opened FD、no-follow、bounded lock 与 device/owner/group/mode/filesystem checks；
- named create 为 basename + `dir_fd` + `O_CREAT|O_EXCL|O_NOFOLLOW`；
- file write 后执行 chmod、file fsync 与 FD-bound size/hash/stat verification；
- create 后 failure 保留 artifact 并返回 `RETAINED_RECOVERY_REQUIRED`；没有自动 cleanup。

Blocker `REL-R27-R2-UPLOAD-001`：

- `_verify_upload_fd()` 只验证 opened FD；
- verification 后没有用 `os.stat(..., dir_fd=parent_fd, follow_symlinks=False)` 把 basename 当前 identity 与 FD identity 重新绑定；
- `path` / `realpath` 来自 pathname，而 bytes/SHA/device/inode/owner/group/mode 来自已打开 FD；
- `upload()` return 后 finally 关闭 FD 并释放 parent lock，`main()` 随后才输出 JSON。

bounded probe 在 `_verify_upload_fd()` 完成后，用另一 inode 替换 exact basename，但不注入 error。persisted `main()` 结果：

首次 probe harness 使用 `SimpleNamespace` copy，配置赋值未回写函数 globals，导致 helper 在未配置状态下返回空 stdout，随后 JSON parse 失败。该结果不属于 helper contract evidence，也没有 repository/remote mutation；确认 loader defect 后仅更正为 `ModuleType.__dict__` source-byte loader一次。以下为更正后实际 persisted-source 结果：

```text
returncode=0
stderr_empty=true
one_line=true
emitted_status=PASS
emitted_inode=11762724
named_inode=11762725
inode_match=false
emitted_bytes=7112
named_bytes=32
emitted_sha_match_named=false
```

这直接证明 success JSON 可为一个已经不再由 `path` 命名的 task-owned FD object 声明 PASS，而 named path 实际是外来对象。属于 production-reachable false PASS / foreign-object identity ambiguity，必须 HOLD。

## 10. R3 — Deploy identity truthfulness and atomic replacement

判定：`HOLD`。

已确认的正面控制：

- old target 与 upload 在 rename 前分别 opened、FD-verified 并 rechecked；
- backup exclusive/no-follow create、fsync、reopen/verify 与 parent fsync 在 replace 前完成；
- `os.replace(upload, target)` 是唯一 replacement primitive；`EXDEV` fail closed、无 fallback；
- replace 后 parent fsync，再检查 final target 与 final backup；
- target old/new inode 不同；failure 不执行 rollback、cleanup 或 retry；
- success JSON 在 deploy() 完成 final checks 后才由 `main()` 输出。

Blocker `REL-R27-R2-DEPLOY-001`：

- final target check 接受 `expected_inode=None`，没有要求 `final_target.st_ino == upload_identity.st_ino`；
- final target/backup 的 digest 由 pathname read 取得，未通过 opened no-follow FD 与 initial `lstat` 做同一 identity transaction；
- JSON 对 target SHA 使用 expected constant，而不是一个与 final target stat 同时绑定的 FD verification result；
- final checks 后 deploy() finally 释放 lock，`main()` 才输出 JSON。

因此同目录 actor 可在 atomic replace 后、final verification/serialization boundary 替换成另一 exact-content inode。helper 仍可输出：

```text
source_upload_temp.state=CONSUMED_BY_ATOMIC_REPLACE
source_upload_temp.inode=<original upload inode>
target.inode_after=<different final inode>
status=PASS
```

这违反本 gate 明确要求的 same-filesystem rename inode relation，并使 source、target 与 final pathname object 的关系不完整/歧义。T37 只断言 `target.inode_after != target.inode_before`，未断言 `source_upload_temp.inode == target.inode_after`。

## 11. R4 — Failure and retained-artifact invariants

判定：`PASS`（static control-flow review）。

- upload caught failure：exit `2`，stderr prefix `HOLD / `，stdout 无 success JSON；
- deploy caught failure：exit `2`，stderr prefix `HOLD / NO WRITE: `，stdout 无 success JSON；
- stale upload remains blocker；
- upload create 后 failure 保持 `RETAINED_RECOVERY_REQUIRED`，没有 automatic cleanup；
- deploy 没有 cleanup、retry、resume 或 rollback path；
- `EXDEV` 仍 fail closed；
- retry/resume/cleanup/rollback/activation semantics 未在两个 helper repair 中增加。

T29/T30/T34/T35 与 E45 source 仍覆盖 failure/foreign retention，但本 review 因 blocker stop 未 fresh 执行这些 cases。R4 PASS 不升级 R2/R3 identity truthfulness，也不继承 R27-R1 matrix PASS。

## 12. R5 — Strict orchestrator compatibility

判定：`HOLD`。

正面边界：

- `_decode_json()` 使用 UTF-8 decode 后一次 `json.loads()`，拒绝 empty、malformed、multiple JSON values、list、scalar 与 trailing text；
- `_normalize_invalid_child_json()` 将 return-code-0 且不可解码 object 的 stdout 标记为 `INVALID_CHILD_JSON`；
- legacy text 不被接受；
- relevant mutation failure branches最多执行一次 postflight；
- final deployment success 仍要求 postflight `DEPLOYED_IDENTITY_VERIFIED`，helper JSON 不是 final deployed-identity authority。

Blocker `REL-R27-R2-ORCH-001`：

- `_decode_json()` 对任意 dict 返回成功，包括 `{}`；
- `_normalize_invalid_child_json()` 对 `{}` 不加 interruption；
- `execute()` 在 upload 后只检查 `child_returncode != 0` 或 interruption，不验证 decoded object 的 exact key set、`status=PASS`、`phase=REMOTE_UPLOAD` 或 identity fields；
- 因而 complete but contract-invalid object 会触发下一 mutation phase。

bounded persisted-source probe 结果：

```text
_decode_json(b"{}\n") -> {}
normalizer_added_interruption=false
phases=REMOTE_PREFLIGHT->REMOTE_UPLOAD->REMOTE_DEPLOY->REMOTE_POSTFLIGHT
deploy_started=true
```

这是“仅 return code + 任意 object”推断 helper success，并直接启动 deploy；符合本 Prompt 的 later-mutation false-PASS HOLD condition。

## 13. R6 — Race, ownership, path and process safety

判定：`HOLD`。

owner/group lookup、parent FD/lock、exclusive create、no-follow、same-device gate、FD close 与 process ownership 的既有正面控制仍在。未发现本 review 自身留下 FD、subprocess、orchestrator、helper 或 SSH process。

但是 R2 probe 已证明一个真实的 post-verification basename TOCTOU window；R3 也未关闭 atomic replace 后 source-to-final-target inode binding。advisory `flock` 不能阻止不协作的同目录 actor。该风险能造成 success evidence 指向外来或未验证 pathname object，不属于纯 style/diagnostic recommendation，必须 HOLD。

## 14. R7 — Regression adequacy and cross-artifact realism

判定：`HOLD`。

正面覆盖：

- T36/T37 调用 persisted helper `main()`，不是 source string scan；
- exact stdout framing/schema 由 `parse_compact_json_line()` 与 exact key sets 检查；
- emitted identity 与正常 synthetic filesystem objects 比较；
- stdout 通过 persisted orchestrator `_decode_json()` / normalization；
- fake SSH 从 orchestrator bootstrap 恢复 exact helper source bytes并执行 persisted `main()`；
- actual upload payload 进入 helper stdin，process-global stdin 在 finally 恢复；
- actual helper stdout 到达 orchestrator；正常 success path 到达 postflight；
- E44 覆盖 empty、legacy、malformed、multiple、list、scalar、trailing text；E45 覆盖 helper exit-2；
- E1–E40 source 保持在同一 matrix，success path 没有 test-generated helper success wrapper。

Blocking coverage gaps：

1. T30 在 foreign replacement 后主动抛 `ContractError`，因此只证明 failure-path 不清理外来 inode；它没有让 `_verify_upload_fd()` 返回并断言 helper 必须拒绝 success。
2. T36 只覆盖无 race 的 normal path，不能捕获 `REL-R27-R2-UPLOAD-001`。
3. T37 未断言 `source_upload_temp.inode == target.inode_after`，不能捕获 `REL-R27-R2-DEPLOY-001`。
4. E44 只覆盖 syntactically invalid/non-object stdout，未覆盖 `{}`、wrong status、wrong phase、missing/extra fields 或 partial identity 的 return-code-0 JSON object；不能捕获 `REL-R27-R2-ORCH-001`。

因此当前 regression suite 可在上述 production-reachable false-PASS paths 存在时仍全绿，R7 必须 HOLD。

## 15. R8 — Manifest closure and historical-evidence isolation

判定：`PASS`。

- P2-R2 manifest：6/6 OK，exact 6 stable entries；
- P2-R3 manifest：9/9 OK，exact 9 stable entries；
- 两份 manifests 均 sorted、duplicate-free、self-excluded；
- manifests 绑定本 review 静态审查与 probes 所加载的 exact persisted bytes；
- orchestrator/postflight identities unchanged；
- R26 report/evidence/manifest identities unchanged；
- R26 retained stage root 未作为 fixture/input；
- probes 只建立 local synthetic blocker evidence，不是 remote evidence；
- 未引入 runtime-load、Collector activation 或 production acceptance claim。

一次 manifest invocation 从 P2-R2 子目录错误调用 root-relative P2-R3/R26 manifests，产生 file-not-found verifier error；该命令未修改任何文件。随后从 repository root 按 manifest contract 更正，P2-R3 9/9 与 R26 3/3 均 OK。该调用错误不是 artifact drift，也未被隐藏。

## 16. Source-byte compile result

`NOT RUN / STOPPED ON RELIABILITY BLOCKER`。

没有使用 `py_compile` 或 `compileall`。两只必要 probes 使用 source bytes `compile(..., "exec")` / in-memory `ModuleType` loader，成功加载实际 upload helper 与 orchestrator bytes，但这不是要求的 8/8 compile matrix，故不记为 8/8 PASS。

## 17. T1–T37 result

`NOT RUN / STOPPED ON RELIABILITY BLOCKER`。

未继承 R27-R1 报告中的 37/37 PASS 为本 review fresh result。原因是 R2/R3/R5/R6/R7 blockers 已由 persisted control flow 与 bounded probes 建立；Prompt 的 HOLD stop condition 要求停止且不得修复。

## 18. E1–E45 result

`NOT RUN / STOPPED ON RELIABILITY BLOCKER`。

未继承 R27-R1 报告中的 45/45 PASS 为本 review fresh result。orchestrator `{}` probe 已直接证明 E44 未覆盖的 contract-invalid-object phase transition。

## 19. Manifest checks

```text
P2-R2: 6/6 OK
P2-R3: 9/9 OK
R26 historical evidence: 3/3 OK
```

结构检查：三份 manifest 均 count exact、sorted、duplicate-free、self-excluded。

## 20. Cache audit

报告写入前及首次完整写后 readback：

```text
docs/reports/evidence/d2_r7b_p2_r2: __pycache__=0, *.pyc=0
docs/reports/evidence/d2_r7b_p2_r3: __pycache__=0, *.pyc=0
```

没有执行 cache cleanup 来制造该结果。

## 21. R26 evidence identity recheck

| Path | Bytes | SHA-256 | Result |
| --- | ---: | --- | --- |
| `docs/reports/sprint4_d2_r7b_i1_r26_exact_config_only_remote_execution.md` | 10314 | `dd25adf90cd4c11f3e2611321b3ed4642785021c81e859f31b229f082936f3b2` | UNCHANGED |
| `docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/final_terminal.json` | 12872 | `4799fc7e9cf27212cd9f696afa40f24c48cf69320bf0700b3ee39b5e7c5be600` | UNCHANGED |
| `docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/manifest.sha256` | 453 | `257fb2945155d49e40638ea1dfedd4cc95aee127dca6a38fc7d72a8e8f362670` | UNCHANGED |

R26 manifest 3/3 OK，同时覆盖 `raw_terminal.ndjson`。R26 仍是 historical `HOLD_UPLOAD_INTERRUPTED / UPLOAD_STAGED_NO_REPLACEMENT` evidence；本 review 没有刷新或观察 current remote state。

## 22. Retained R26 stage-root recheck

```text
path: /private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r2.0mW7V5
type: regular directory / non-symlink
owner: chenjie (uid 501)
mode: 0700
mapping type: regular non-symlink
mapping mode: 0600
mapping bytes: 7112
mapping SHA-256: d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
```

stage root untouched；未删除、重命名、写入、执行或作为 fixture/input。

## 23. Changed-file allowlist audit

本 task 唯一 authorized write：

```text
docs/reports/sprint4_d2_r7b_i1_r27_r2_mutation_helper_json_contract_reliability_review.md
```

报告写入前该 path ABSENT。两只 probes 只使用自动回收的 task-owned synthetic temporary root / in-memory module；未创建额外 repository report、note、schema、log、sidecar、fixture 或 evidence artifact。最终 exact changed-file 与 Git audit 在报告写后 readback 中复核。

写后 readback 结果：本报告为 exact path 下的 regular non-symlink；`git status --short --untracked-files=all -- <exact report>` 只有本报告一项 `??`。全部 frozen R27-R1/source/test/manifest/R26/mapping identities 与初始值重新比较均为 `MATCH`；tracked dirty 仍恰为 `.gitignore`、`docs/current_status.md`、`docs/thread_handoff/pm_operating_rules.md`。因此 task changed-file allowlist：`PASS`。

## 24. Process audit

报告写入前及写后 fresh process audit：

```text
task-owned orchestrator/helper process count: 0
SSH process count: 0
remote calls: 0
```

probe 没有启动 SSH、orchestrator subprocess 或 helper subprocess；无 FD/process leak 被观察到。

## 25. Final Git boundary

报告写入后 final readback：

```text
branch: main
HEAD: 8de5edbb504538a233abbcc80102cb714c9cee65
origin/main: 8de5edbb504538a233abbcc80102cb714c9cee65
ahead/behind: 0/0
cached: empty
git diff --check: PASS
config/mapping.yaml: clean relative to HEAD
```

Git stage/commit/push/tag/reset/stash/clean 均未执行。写后 readback 同时确认：本报告 regular non-symlink、trailing-whitespace lines `0`；protected identities 全部 `MATCH`；两棵 active evidence trees 的 `__pycache__=0`、`*.pyc=0`；R26 stage root unchanged；task-owned/SSH process count 均为 `0`。report 自身最终 bytes/SHA 由 Chat window manifest 提供，避免报告自引用。

## 26. Production blockers

### REL-R27-R2-UPLOAD-001 — success JSON 可描述已脱离 pathname 的 verified FD object

- consequence：direct false PASS；命名路径可为 foreign/unverified object；可能使 orchestrator 启动 deploy。
- required disposition：source/test repair 需要新的 PM authority；本 review 不修复。

### REL-R27-R2-DEPLOY-001 — source upload 与 final target inode relation 未被强制

- consequence：deploy JSON 可把 consumed upload 与另一 final target object 表示为完整、无歧义的 success；direct identity false PASS / safety ambiguity。
- required disposition：source/test repair 需要新的 PM authority；本 review 不修复。

### REL-R27-R2-ORCH-001 — 任意 return-code-0 JSON object 可授权 deploy phase

- consequence：`{}`、wrong-status、wrong-phase 或 partial-identity object 不会 fail closed；direct unauthorized later mutation transition。
- required disposition：orchestrator/test repair 需要新的 PM authority；本 review 不修复。

## 27. Bounded recommendations

`none`。

当前需要处理的三项均具有直接 false-PASS 或 safety consequence，已归类为 blockers，不降级为 recommendation。未发现需要在本 HOLD 结论之外增加无直接后果的维护或诊断建议。

## 28. Evidence and authority distinctions

- helper-emitted execution evidence：本地 synthetic probe 证明当前 helper 可输出 canonical bytes，但 upload identity 可与 named object 不一致；
- orchestrator phase acceptance：当前会接受任意 return-code-0 JSON object 并进入下一 phase；
- postflight deployed-identity classification：仍是 final remote identity authority，但本 task 未调用；它不能消除“invalid upload evidence 已授权 deploy”的 phase-safety defect；
- remote deployment：未执行、未观察；
- runtime loading：未执行、未证明；
- Collector activation/restart：未执行、未证明；
- production acceptance：未执行、未证明。

Local synthetic probes 不证明 current remote state。

## 29. Next gate

唯一 next gate：

```text
R27-R2 Reliability HOLD report WRITTEN
→ ChatGPT PM durable Reliability intake
```

只有 PM 完成 exact-path intake 后，才可决定是否另行授权最小 source/test/orchestrator repair。不得由本 HOLD 自动进入 Verification、remote cleanup、remote eligibility refresh、remote deployment、rollback、retry/resume、Collector restart/activation、runtime-load validation 或 Git closeout。

## 30. MVP alignment

分类：`MVP-ALIGNED`。

本 review 直接保护 single-file exact config-only deployment MVP 的三个最小安全 invariant：mutation helper evidence 必须描述 exact verified object、atomic replace source/target identity 不得歧义、无 canonical success evidence 不得启动下一 mutation phase。三项均可造成具体 false PASS 或 unsafe later mutation，不是扩展 threat model 或构造通用审计系统。

本 task 未引入新产品能力、remote/runtime topology、retention framework、Data Quality schema 或 production claim。没有把 local probes 升级为 remote、runtime 或 production evidence。

## 31. Thread context assessment

- 本次输出长度：长（完整证据保存在本 durable report；Chat 返回短 manifest）；
- 当前 Thread 是否建议继续：no；
- 下一轮是否建议新开 Thread：yes；
- 理由：Reliability authority 已以 HOLD terminal；PM intake 必须先决定 blocker disposition，且任何 repair/Verification 都需要新的独立 authority。
