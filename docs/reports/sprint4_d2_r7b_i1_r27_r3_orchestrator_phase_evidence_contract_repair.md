# Sprint 4 D2-R7B-I1 R27-R3 Orchestrator Phase Evidence Contract Repair

## 1. 报告 / 任务 / Thread / Authority

- 报告名称：Sprint 4 D2-R7B-I1 R27-R3 Orchestrator Phase Evidence Contract Repair
- 任务名称：D2-R7B-I1 R27-R3 — Enforce Strict Remote Phase Evidence Before Mutation and Final PASS
- 执行 Thread：Architecture / Integration
- Authority ID：`PM-R27-R3-260728-SCOPE-01`
- Authority state：`AUTHORIZED ONCE / CONSUMED BY THIS EXACT IMPLEMENTATION`
- Report delivery mode：`REPOSITORY_REPORT_WITH_ARTIFACTS`
- Remote authority：not authorized / not used
- Git stage / commit / push / tag：not authorized / not performed

## 2. 结论

`PASS`。

在 exact four-file write allowlist 内完成 orchestrator phase-evidence contract 修复。持久化
orchestrator 现在仅在前一 phase 的 JSON record 具有 exact key set、严格类型、冻结常量、
phase-specific 语义及必要 cross-phase identity relation 时，才授权下一 mutation phase 或最终
`CONFIG_DEPLOYED_IDENTITY_VERIFIED`。

本 PASS 是本地 implementation evidence；不建立 current remote state、remote mutation、runtime
load、Collector restart/activation、production acceptance 或 Git closeout。

## 3. PM scope reset

Approved MVP claim：

> The one-shot orchestrator may start a remote mutation phase only after receiving complete,
> phase-correct, machine-readable evidence from the preceding persisted helper.
>
> Final CONFIG_DEPLOYED_IDENTITY_VERIFIED may be emitted only after a complete, semantically
> valid postflight record proves the exact deployed target, backup, temporary-file and Collector
> state.

Retained current blocker：`REL-R27-R2-ORCH-001`，由本任务关闭于 implementation boundary。

Deferred hardening findings：

- `REL-R27-R2-UPLOAD-001`：REPRODUCED / BACKLOG / NON-BLOCKING UNDER RESET THREAT MODEL；未声称修复。
- `REL-R27-R2-DEPLOY-001`：REPRODUCED / BACKLOG / NON-BLOCKING UNDER RESET THREAT MODEL；未声称修复。

## 4. Approved execution / threat model

```text
one authorized orchestrator
one owned SSH child per phase
persisted manifest-bound helpers
no concurrent untrusted writer is part of the approved execution model
postflight remains final deployed-identity authority
```

未加入 arbitrary concurrent same-directory untrusted replacement resistance；未修改任何 helper。

## 5. Fresh baseline

- root：`/Users/chenjie/Documents/MES/edge-mes-demo`
- branch：`main`
- HEAD：`8de5edbb504538a233abbcc80102cb714c9cee65`
- origin/main：`8de5edbb504538a233abbcc80102cb714c9cee65`
- ahead / behind：`0 / 0`
- cached paths：empty
- `git diff --check`：PASS
- `config/mapping.yaml` relative to HEAD：clean
- pre-existing tracked dirty preserved：`.gitignore`、`docs/current_status.md`、`docs/thread_handoff/pm_operating_rules.md`
- pre-existing untracked reports/evidence/frontend artifacts：excluded and untouched

## 6. Output preflight

`docs/reports/sprint4_d2_r7b_i1_r27_r3_orchestrator_phase_evidence_contract_repair.md`
在任何 write 前为 `ABSENT`；`docs`、`docs/reports`、`docs/reports/evidence` 与 P2-R3 parent
均为 regular non-symlink directories，无 unsafe parent/path collision。未覆盖、删除、重命名或复用旧输出。

## 7. Accepted authority / initial identities

R27-R2 Reliability report：

- bytes：`25557`
- SHA-256：`565cd2b26728b17e731d1cefd744a970f4b7e2606af0b704932a17cdceec1d13`
- conclusion：`HOLD / PM-REVIEWED`

Initial implementation identities：

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `remote_i1_orchestrator.py` | 45783 | `eea3e8778cc94c78a0931b2404f888a78176996cd1a4421a7442667c8b859085` |
| `test_d2_r7b_execution_contract.py` | 89604 | `d1dc0962995686b171cef0b134036ee5fbe24f3b8055b02b68d1fa5e68a871f5` |
| P2-R3 `manifest.sha256` | 1122 | `18edbdc940d1eaef4edbc9dc831dee38716704194b05b564dfc8fb1a6da24714` |
| P2-R2 `manifest.sha256` | 528 | `2ae13bd6dc17167f98d2d59efd882e8a568d5c0ae6f36cbbb9ecb6f2d21086dd` |

Frozen helper identities matched the Prompt before implementation；其中 preflight/upload/deploy/test/P2-R2
manifest 与 postflight 的 final audit 仍与 initial SHA-256 一致。

## 8. Initial gates

- P2-R2 manifest：PASS `6/6`
- P2-R3 manifest：PASS `9/9`
- R26 manifest：PASS `3/3`
- T1–T37：PASS `37/37`
- E1–E45：PASS `45/45`
- source-byte compile：PASS `8/8`
- repository evidence `__pycache__`：`0`
- repository evidence `*.pyc`：`0`

两次 read-only manifest checker 曾使用错误 cwd：P2-R3 的 repo-relative entries 不能从 P2-R3
directory 校验；P2-R2 的 basename-relative entries 不能从 repository root 校验。两次均只产生
`No such file` checker output，无文件 mutation；按各自 manifest path contract 从正确 cwd 重跑后分别
`9/9` 与 `6/6` PASS。该诊断错误不作为 artifact drift 或 mutation evidence。

## 9. Root cause / accepted ORCH blocker

`REL-R27-R2-ORCH-001` 的 current persisted root cause：

- `_decode_json()` 只拒绝 empty、malformed、multi-value、non-object JSON；
- return-code-0 的任意 object（包括 `{}`）未经过 phase-specific schema/semantic validation；
- preflight `{}` 可授权 upload，upload `{}` 可授权 deploy；
- deploy record 未与 accepted upload inode 交叉绑定；
- final PASS 只依赖 postflight return code 与稀疏 `classification` 字段。

## 10. TDD RED evidence

先修改 test，未修改 orchestrator；E1–E45 仍 `45/45`，新增 E46–E50 初次运行 `0/5`，总计
`45/50`。

精确 bounded RED probe：

```json
{"classification":"DEPLOYED_IDENTITY_VERIFIED","phases":["remote_preflight.py","remote_upload_exclusive.py","remote_deploy.py","remote_postflight.py"],"probe":"PRE_IMPLEMENTATION_RED_PREFLIGHT_EMPTY_OBJECT","process_returncode":0,"remote_call_count":4,"terminal_status":"CONFIG_DEPLOYED_IDENTITY_VERIFIED"}
```

即 return-code-0 的 preflight `{}` 错误授权了 upload、deploy 与 final PASS。

## 11. Phase validator design

未添加 JSON Schema runtime dependency。实现使用显式 Python validators：

- exact top-level / nested key-set checks；
- exact constant 与 phase checks；
- `type(value) is int` 的 strict integer checks，排除 bool-as-int；
- positive-integer inode checks；
- frozen production path / principal / owner / group / device / filesystem / bytes / SHA / mode checks；
- 仅在已有 bounded synthetic test boundary 中派生 fixture path / owner / group / device / inode；
- stable diagnostic fields：`phase_evidence_valid`、`phase_evidence_error`；
- stable errors：`INVALID_CHILD_JSON`、`INVALID_PREFLIGHT_SCHEMA`、`INVALID_UPLOAD_SCHEMA`、
  `INVALID_DEPLOY_SCHEMA`、`INVALID_POSTFLIGHT_SCHEMA`、`CROSS_PHASE_IDENTITY_MISMATCH`。

`_decode_json()` 未改成 permissive parser；aliases、legacy text、missing fields 与 additional fields 均不接受。

## 12. REMOTE_PREFLIGHT behavior

只有 exact eight-key record 且 status/endpoint/hostname/principal/device/inode/filesystem 均符合 phase
expectation 才可进入 `REMOTE_UPLOAD`。

E46 覆盖 `{}`、wrong status、missing field、additional field。全部：

- stop before upload；
- `REMOTE_CALL_COUNT == 1`；
- mutation-capable phase 未启动；
- observed child return code 保留为 `0`；
- terminal `HOLD_PREFLIGHT_EVIDENCE_INVALID`；
- diagnostic `INVALID_PREFLIGHT_SCHEMA`。

## 13. REMOTE_UPLOAD behavior

只有 exact eleven-key record 以及 exact phase/path/realpath/bytes/SHA/device/inode/owner/group/mode
才可进入 `REMOTE_DEPLOY`。accepted upload record retained in-memory for deploy cross-phase comparison。

E47 覆盖 `{}`、wrong phase/status、missing inode、additional field、wrong path/hash/bytes/mode。全部：

- deploy 不启动；
- exactly one read-only postflight maximum；
- `REMOTE_CALL_COUNT == 3`；
- terminal `HOLD_UPLOAD_EVIDENCE_INVALID`；
- diagnostic `INVALID_UPLOAD_SCHEMA`。

## 14. REMOTE_DEPLOY / cross-phase behavior

严格验证 exact top-level keys 与 `source_upload_temp`、`target`、`backup` exact nested keys，且验证：

- status / phase / operation constants；
- new/old bytes、SHA、mode、path、realpath、device、owner、group；
- positive inodes；
- target inode-before 与 preflight target inode；
- target inode-before != inode-after；
- deploy source inode == accepted upload inode；
- deploy source inode == target inode-after。

E48 覆盖 wrong phase/status/operation、missing/extra nested field、upload→source mismatch、source→target
mismatch。每个 case 都运行 exactly one postflight，`REMOTE_CALL_COUNT == 4`；即使 postflight 观察
`DEPLOYED_IDENTITY_VERIFIED`，仍返回 `HOLD_DEPLOY_EVIDENCE_INVALID`，不产生 final PASS。

这避免 misleading final PASS；不声称阻止 hostile concurrent writer。

## 15. REMOTE_POSTFLIGHT spoof resistance

final PASS 要求 persisted postflight exact eleven-key record、child return code `0`、status/phase/classification
constants、完整 NEW_EXACT target、ABSENT upload/rollback、OLD_EXACT backup、UNCHANGED Collector、exact
artifact paths 及全部 zero lifecycle counters。

E49 覆盖 `{}`、minimal classification spoof、wrong status、missing state object、additional top-level field、
nonzero lifecycle counter。全部返回 `HOLD_POSTFLIGHT_EVIDENCE_INVALID`，无 second postflight、无 final PASS。

非 deployed safe classifications 也要求 complete record、exact state-object shapes 与 classification/state
relation；invalid postflight 被降为 `UNKNOWN_OR_UNSAFE`，不能授权成功。

## 16. Authentication / evidence diagnostic separation

normally exited schema-invalid child：

- 保留 actual child return code；
- `interruption_kind == null`；
- `auth_state == NOT_STARTED`；
- 通过 `phase_evidence_valid=false` 与 stable phase-evidence error 诊断。

不再复用 `AUTHENTICATION_OR_INTERRUPTION_UNKNOWN`。原 authentication、EOF、operator cancellation、prompt
interruption 与 child-reaping semantics 继续由既有 E cases 覆盖。

## 17. Call-budget / postflight-once / terminal audit

- preflight invalid：1 call，0 mutation-capable call；
- upload invalid：preflight + upload + one postflight，3 calls；
- deploy invalid：4 calls，one postflight；
- postflight invalid：4 calls，no second postflight；
- valid persisted success：exact phase sequence，4 calls；
- retry/resume/cleanup/rollback/restart/activation counters：all zero；
- no fifth call；
- PhaseOwnedRunner、child ownership/reaping、NDJSON authoritative selection 与 delivery fallback tests preserved。

## 18. GREEN / final tests

- focused GREEN after strict validation and complete test-double repair：E1–E50 `50/50`
- final persisted-manifest run：E1–E50 `50/50`
- T1–T37：`37/37`
- source-byte compile：`8/8`
- P2-R2 manifest：`6/6`
- P2-R3 manifest：`9/9`
- cache audit：`__pycache__=0`、`*.pyc=0`

E50 使用 actual persisted preflight/upload/deploy/postflight helper bytes，通过完整 state machine，exact sequence
与 `REMOTE_CALL_COUNT == 4`，final local synthetic status 保持
`CONFIG_DEPLOYED_IDENTITY_VERIFIED`。该 synthetic PASS 明确为 local-only。

## 19. Final artifact identities

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py` | 63505 | `daa4b5056aeacdaf3781c3ccd6c7306dd728876d334ab59af244ebd35f08ee64` |
| `docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py` | 102372 | `f19f4d0f19e6e21bfeb51931fa903cbf84eee107922be817ace9090050a5414c` |
| `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256` | 1122 | `8e5e99f5e52e87a6945b692ca8808b518e6cd360c84191f08aa9bf1d992f95c8` |
| P2-R2 `manifest.sha256` unchanged | 528 | `2ae13bd6dc17167f98d2d59efd882e8a568d5c0ae6f36cbbb9ecb6f2d21086dd` |

P2-R3 manifest：exactly 9 entries、sorted、duplicate-free、self-excluded；只有 orchestrator 与 execution-test
entries 更新。

## 20. Exact changed-file allowlist

本任务仅创建/修改：

1. `docs/reports/sprint4_d2_r7b_i1_r27_r3_orchestrator_phase_evidence_contract_repair.md`
2. `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py`
3. `docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py`
4. `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256`

P2-R2 helpers/tests/manifest、postflight、materializer、rollback、mapping、R26/R27-R1/R27-R2 evidence、
governance docs 与其他 repository paths 均未修改。Allowlist compliance：`PASS`。

## 21. R26 boundary recheck

Frozen R26 evidence：

- report SHA-256：`dd25adf90cd4c11f3e2611321b3ed4642785021c81e859f31b229f082936f3b2`
- final terminal SHA-256：`4799fc7e9cf27212cd9f696afa40f24c48cf69320bf0700b3ee39b5e7c5be600`
- manifest SHA-256：`257fb2945155d49e40638ea1dfedd4cc95aee127dca6a38fc7d72a8e8f362670`
- R26 manifest：`3/3`

Retained stage root：

- path：`/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r2.0mW7V5`
- root：regular non-symlink directory，owner `chenjie`，mode `0700`
- retained mapping：7112 bytes，SHA-256
  `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`

R26 evidence/stage root untouched；未作为 fixture 使用。

## 22. Process / remote / Git boundary

- task-owned orchestrator/helper/SSH process before implementation：none
- task-owned orchestrator/helper/SSH process final：none
- SSH / remote calls：`0`
- remote inspection / cleanup / deploy / rollback：none
- Collector / Docker / Compose lifecycle：none
- Git staged：no
- Git committed：no
- Git pushed：no
- Git tagged/reset/stashed/cleaned：no
- final branch/HEAD/origin/ahead-behind：`main` /
  `8de5edbb504538a233abbcc80102cb714c9cee65` /
  `8de5edbb504538a233abbcc80102cb714c9cee65` / `0/0`
- final cached paths：empty
- `config/mapping.yaml`：clean relative to HEAD，7112 bytes，expected SHA-256

Process boundary：`PASS`。

## 23. Blockers / recommendations

Current R27-R3 implementation blocker：none。

Recommendations / backlog：

- `REL-R27-R2-UPLOAD-001` remains deferred Level 2 hardening backlog；
- `REL-R27-R2-DEPLOY-001` remains deferred Level 2 hardening backlog；
- no claim that concurrent-writer resistance is fixed；
- fresh focused Reliability re-review requires separate PM authority after durable intake。

## 24. Evidence interpretation boundaries

- helper phase evidence authorizes only the next orchestrator phase；
- authorization to start a phase is not proof that mutation occurred；
- deploy helper evidence is not final deployed-identity authority；
- postflight deployed-identity evidence is not runtime-load evidence；
- runtime load is not Collector restart/activation evidence；
- activation is not production acceptance；
- local synthetic PASS is not current remote state。

Current remote claim：`NOT OBSERVED BY R27-R3`。

## 25. MVP alignment

`MVP-ALIGNED UNDER SCOPE RESET`：strict preceding-phase evidence now gates each mutation transition；strict,
complete postflight evidence gates final deployment PASS；call budget、child ownership 与 terminal delivery are
preserved。未扩大为 helper hardening、remote execution、runtime/activation 或 production claim。

## 26. Next gate / Thread assessment

唯一 next gate：

```text
R27-R3 implementation report/artifacts WRITTEN
→ ChatGPT PM durable implementation intake
```

不得自动进入 Reliability re-review、Verification、helper hardening、remote cleanup/eligibility/deployment、
rollback、retry/resume、Collector restart/activation、runtime-load validation 或 Git closeout。

- 本次输出长度：长
- 当前 Thread 是否建议继续：no
- 下一轮是否建议新开 Thread：yes
- 理由：implementation authority 已 terminal；PM exact-path intake 必须先于任何 focused Reliability re-review。
