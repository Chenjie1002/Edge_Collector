# Sprint 4 D2-R7B-I1 R27-R4 Orchestrator Phase Evidence Focused Reliability Re-review

## 1. 报告、任务、Thread 与 Authority

- 报告名称：Sprint 4 D2-R7B-I1 R27-R4 Orchestrator Phase Evidence Focused Reliability Re-review
- 任务名称：D2-R7B-I1 R27-R4 — Re-review Strict Phase Evidence Gating Under PM Scope Reset
- 执行 Thread：Reliability
- Authority ID：PM-R27-R4-260728-REL-02
- Report delivery mode：REPOSITORY_DURABLE_REPORT
- 唯一写入授权：本报告 exact path；source/test/manifest repair、remote、Git 均未授权且未执行。

## 2. 结论

PASS。

独立复核的 exact persisted orchestrator、helpers、tests 与 manifests 均匹配授权身份。严格 phase-evidence validators 在批准的 scope-reset threat model 内阻止不完整、伪造或跨阶段不一致 evidence 授权后续 mutation 或 final PASS。没有发现 production-reachable false transition、false final PASS、call-budget、child ownership/reaping、diagnostic separation 或 terminal-delivery blocker。

本结论仅为本地 static/synthetic Reliability evidence；不建立 current remote state、remote mutation、deployed current identity、runtime config load、Collector restart/activation 或 production acceptance。

## 3. PM scope reset 与当前边界

批准 threat model：一个 authorized orchestrator、每 phase 一个 owned SSH child、persisted manifest-bound helpers、无 concurrent untrusted same-directory writer、postflight 为 final deployed-identity authority。

- retained blocker：REL-R27-R2-ORCH-001 在 R27-R3 implementation boundary 声称 CLOSED；本独立 re-review 确认其 phase-evidence gating 关闭条件成立。
- deferred：REL-R27-R2-UPLOAD-001、REL-R27-R2-DEPLOY-001 均为 REPRODUCED / HARDENING BACKLOG / NON-BLOCKING；本轮未重新打开，也未声称 concurrent-writer hardening 已完成。
- R26 保持 historical HOLD_UPLOAD_INTERRUPTED / UPLOAD_STAGED_NO_REPLACEMENT evidence；没有 retry、resume 或 remote observation。

## 4. Fresh recovery、输出 preflight 与初始身份

在 /Users/chenjie/Documents/MES/edge-mes-demo 复核：

    branch: main
    HEAD: 8de5edbb504538a233abbcc80102cb714c9cee65
    origin/main: 8de5edbb504538a233abbcc80102cb714c9cee65
    ahead/behind: 0/0
    cached: empty
    git diff --check: PASS
    config/mapping.yaml relative to HEAD: clean

输出 docs/reports/sprint4_d2_r7b_i1_r27_r4_orchestrator_phase_evidence_focused_reliability_rereview.md 在写前为 ABSENT；parent 是 regular non-symlink directory，mode 0755、owner chenjie，无 unsafe collision。pre-existing tracked dirty 仍为 .gitignore、docs/current_status.md、docs/thread_handoff/pm_operating_rules.md；既有 untracked reports/evidence/frontend artifacts 均排除。

| 已读 report / artifact | bytes | SHA-256 | 结果 |
| --- | ---: | --- | --- |
| R27-R1 report | 10155 | 8a5a92f09e5c405331a68c4bb2d97f9999a175a0b6bf1a17b9590fe5dcd8968f | MATCH |
| R27-R2 Reliability HOLD report | 25557 | 565cd2b26728b17e731d1cefd744a970f4b7e2606af0b704932a17cdceec1d13 | MATCH |
| R27-R3 accepted implementation report | 15809 | 808effe132648e641dd3264c82c7bad7a987352ab0936a8a2a94e14abf23b0aa | MATCH |
| P2-R3 orchestrator | 63505 | daa4b5056aeacdaf3781c3ccd6c7306dd728876d334ab59af244ebd35f08ee64 | MATCH |
| P2-R3 execution test | 102372 | f19f4d0f19e6e21bfeb51931fa903cbf84eee107922be817ace9090050a5414c | MATCH |
| P2-R3 manifest | 1122 | 8e5e99f5e52e87a6945b692ca8808b518e6cd360c84191f08aa9bf1d992f95c8 | MATCH |
| postflight | 15456 | b26051aa1fcbb71b84a16173f3c393542bd6c94bc24e619e4ebfb12c4d60d5ee | MATCH |
| preflight | 11129 | 6ddae658ed30ba38c20dcd3fa29fa9719cb940f3c8da4b904c6dfae810061f9c | MATCH |
| upload | 10563 | 30a02e5bc63545b08b1536e59abc418685cf846fbe2c930847d1f1b983f5ae7b | MATCH |
| deploy | 15483 | 657498d42906c260ad12d53c16044a6a272cd1bea1a60ebfd2538b178baf02ff | MATCH |
| P2-R2 test | 67695 | aa40fa64d8d9cc8508a6e0c480714778381bb2e13c21ffa14bd553205f3e9183 | MATCH |
| P2-R2 manifest | 528 | 2ae13bd6dc17167f98d2d59efd882e8a568d5c0ae6f36cbbb9ecb6f2d21086dd | MATCH |

remote_rollback.py 亦未漂移：13248 bytes，e2690ef991827ad8107430ee0449be913afa65dbf166fe2c1cf19fec0b7736ff。

## 5. RR1 — preflight evidence gate

PASS。_validate_preflight() 只接受 exact eight-key object，严格要求 status=PASS、endpoint、hostname、principal、target/parent device、positive integer inode 与 filesystem；type(x) is int 排除 bool。{}、wrong status、missing 或 additional fields 都不通过。

E46 对 complete-but-invalid preflight variants 逐项证明：child return code 保持 0、interruption_kind=null、auth_state=NOT_STARTED、phase_evidence_error=INVALID_PREFLIGHT_SCHEMA、REMOTE_CALL_COUNT=1，且 upload/mutation-capable phase 没有启动。

## 6. RR2 — upload evidence gate

PASS。_validate_upload() 强制 exact eleven-key schema、status=PASS、phase=REMOTE_UPLOAD，并对 path/realpath、bytes、SHA-256、device、positive inode、owner/group/mode 全部精确比对。E47 覆盖 empty、wrong phase/status、missing identity、additional field 与错误 path/hash/bytes/mode；deploy 不启动，仅有一次 postflight，3 calls，terminal 为 HOLD_UPLOAD_EVIDENCE_INVALID。schema invalid 不被改判为 authentication failure。

本判断只审查 transition authorization；不把任意 concurrent pathname replacement 重新引入当前 blocker。

## 7. RR3 — deploy 与 cross-phase gate

PASS。_validate_deploy() 要求 exact top-level、source/target/backup nested keys、常量、完整 path/content/ownership/device/mode 与 positive inodes，并验证：

    accepted upload.inode == deploy.source_upload_temp.inode == deploy.target.inode_after
    deploy.target.inode_before == accepted preflight target inode
    deploy.target.inode_before != deploy.target.inode_after

E48 覆盖 schema mismatch 与两类 inode relation mismatch；每例均为 4 calls、恰一 postflight、HOLD_DEPLOY_EVIDENCE_INVALID，即使 postflight classification 为 DEPLOYED_IDENTITY_VERIFIED 也绝不 final PASS。此为 phase-evidence consistency，不声称 hostile filesystem actor resistance。

## 8. RR4 — postflight final-PASS gate

PASS。_validate_postflight() 强制 complete exact schema、child return code 0、exact status/phase/classification、NEW_EXACT target、ABSENT upload/rollback temps、OLD_EXACT backup、UNCHANGED Collector、exact paths 与四个 lifecycle counters 全为 zero。E49 拒绝 {}、minimal classification spoof、wrong status、missing state object、additional field 与 nonzero lifecycle counter；结果为 HOLD_POSTFLIGHT_EVIDENCE_INVALID / UNKNOWN_OR_UNSAFE，无 second postflight。

## 9. RR5 — diagnostic separation

PASS。normally exited schema-invalid children 保留实际 child_returncode=0，稳定产生 phase_evidence_valid=false 及 phase-specific error；不被归类为 authentication/interruption。E46/E47 明确断言 interruption_kind is null、auth_state=NOT_STARTED。既有 lifecycle matrix 保持 authentication、EOF、operator cancellation、password prompt、owned-child reaping 与 terminal fallback 的独立处理。

## 10. RR6 — call、process 与 terminal invariants

PASS。源码及 E1–E50 矩阵确认：invalid preflight 1 call；invalid upload 3；invalid deploy 4；invalid postflight 4；success 4；无 fifth call、retry/resume、cleanup/rollback/restart/activation。_postflight_once() 仅在所需 terminal branch 调用一次；owned runner 的 child lifecycle、NDJSON authoritative terminal selection 和 delivery fallback 均未被 validator 改写。

## 11. RR7 — regression adequacy

PASS。E1–E45 全部仍在且通过。E46 覆盖 complete invalid preflight，E47 upload，E48 deploy schema/cross-phase，E49 spoofed/incomplete postflight；E50 读取 manifest-bound 的实际 preflight、upload、deploy 与 postflight helper bytes，核验 source SHA-256、完整 four-phase sequence 与 local synthetic final PASS。它不是 test-generated success wrapper，也不构成 remote evidence。T1–T37 也完整通过。

## 12. RR8 — manifests、R26 与 scope-reset compliance

PASS。P2-R2 manifest 为 6 sorted、duplicate-free、self-excluded entries；P2-R3 为 9，且绑定本次 review 的 exact orchestrator/test bytes 与 unchanged helpers/postflight。两套 manifest 分别 6/6、9/9。

R26 report、final terminal 与 manifest 分别仍为 10314 / 12872 / 453 bytes 和指定 SHA-256；R26 manifest 3/3。retained stage root 是 regular non-symlink directory，owner chenjie、mode 0700；其 config/mapping.yaml 是 regular non-symlink，owner chenjie、mode 0600、7112 bytes、SHA-256 d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d。未使用、未写入、未删除该 root。

## 13. Fresh local validation

    source-byte compile (in-memory compile, no py_compile/compileall): PASS 8/8
    T1–T37: PASS 37/37
    E1–E50: PASS 50/50
    P2-R2 manifest: PASS 6/6
    P2-R3 manifest: PASS 9/9
    R26 historical manifest: PASS 3/3
    __pycache__: 0
    *.pyc: 0
    remote calls: 0

一次在 P2-R2 subdirectory 下对 repo-relative commands 的错误调用在打开 source 前报告 ENOENT；没有启动 test matrix、没有文件写入，也不计作 validation evidence。随后所有 compile/test/manifest checks 都从正确 checkout root（P2-R2 manifest 按其 own cwd contract）成功运行。

## 14. Allowlist、process 与 Git boundary

- changed files：仅本报告。
- explicitly not touched：orchestrator、tests、manifests、helpers、postflight、config/mapping.yaml、R26/R27-R1/R27-R2/R27-R3 reports/evidence、retained stage root、remote、Git。
- process boundary：task-owned orchestrator/helper/SSH process none before and after local tests；no active child remains。
- Git staged/committed/pushed/tagged：no / no / no / no。
- Git reset/stash/clean：no。
- final git diff --check：PASS；cached empty；config/mapping.yaml clean。

Allowlist compliance：PASS。Process boundary：PASS。

## 15. Production blockers、recommendations 与 deferred hardening

Production blockers：none inside the approved threat model。

Recommendations：none。没有发现同时满足“非 blocker”且具有必要 current-gate value 的维护或 test-depth 项目。

- REL-R27-R2-UPLOAD-001：deferred hardening backlog；本 PASS 不声称修复。
- REL-R27-R2-DEPLOY-001：deferred hardening backlog；本 PASS 不声称修复。

## 16. Evidence interpretation、next gate 与 MVP alignment

valid helper phase evidence 仅授权下一 orchestrator phase；该 authorization 不证明 mutation occurrence。postflight deployment identity 不证明 runtime config loading；runtime loading 不证明 Collector restart/activation；activation 也不证明 production acceptance。current remote state：NOT OBSERVED。

MVP-ALIGNED UNDER SCOPE RESET：本轮只复核 one-shot config-deployment chain 的 phase-evidence and final PASS safeguards，未新增 remote/runtime/production claim 或扩展 threat model。

唯一 next gate：

    R27-R4 Reliability re-review report WRITTEN
    → ChatGPT PM durable Reliability re-review intake

Reliability PASS 不自动授权 Verification、source/test repair、helper hardening、remote cleanup/eligibility/deployment、rollback、retry/resume、restart/activation、runtime-load validation 或任何 Git action。

## 17. Thread context assessment

- 本次输出长度：长（durable report；window manifest 应保持短）。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：本轮 Reliability authority 已 terminal；PM exact-path intake 必须先于 independent Verification。
