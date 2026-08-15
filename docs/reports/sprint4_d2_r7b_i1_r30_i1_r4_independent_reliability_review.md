# Sprint 4 D2-R7B-I1 R30-I1-R4 Independent Reliability Review

## 1. Executive conclusion

报告名称：Sprint 4 D2-R7B-I1 R30-I1-R4 Independent Reliability Review

任务名称：D2-R7B-I1 R30-I1-R4 — Independently Review Repaired Orchestrator Baseline Compatibility Package

执行 Thread：Reliability

结论：HOLD

classification：RELIABILITY_HOLD

本轮只进行了 independent local Reliability review。四路径 repaired package、source、test、manifest、helper、postflight、mapping 和 runtime/config context 均未被本 Thread 修改；唯一 repository write 是本报告本身。

package modification：0

Git / network / SSH / remote：0 / 0 / 0 / 0

本报告不把 Architecture / Integration 的 local validation、synthetic matrix PASS 或 historical report 结论提升为 Reliability acceptance、remote eligibility、deployment、runtime-loaded 或 production fact。

HOLD 的唯一 gating finding 是 REL-R30-B5 / REL-R30-CLEANUP-001：P2-R3 cleanup validator 首次选择了 LOCAL_STAGE_PARENT descendant 作为待删 outer root，违反了本任务要求的 ancestor/descendant deduplication 和“每个 validated outer root 一次 exact-path cleanup”边界。该错误没有触碰仓库、foreign object 或历史 retained root；所有当前测试 roots 最终已清理，但 cleanup execution contract 已发生实际偏离，因此本轮不能给出 RELIABILITY-PASS。

## 2. Scope、authority 与 non-inheritance

本轮按授权只读并复审：

- PM Rules Section 9、10、11，当前 handoff、current_status、roadmap；
- R30-P1、R30-I1、R30-I1-R1、R30-I1-R2、R30-I1-R3 durable reports；
- 既有 P2-R2/P2-R3 source、tests、manifests、五个 helpers/postflight；
- config/mapping.yaml、docker-compose.yml、Collector source/runtime context；
- 既有 P2-R3、P2-R5、P2-R6、R7、R8、R9、R12 Reliability/Verification references。

本轮 authority：

AUTHORIZED ONCE / INDEPENDENT RELIABILITY REVIEW / LOCAL-ONLY / ORDINARY PYTHON ENVIRONMENT / EXISTING TESTS ONLY / BOUNDED CURRENT-TEST ROOT CLEANUP / ONE EXACT REPORT / NO PACKAGE WRITES / NO GIT MUTATION / NO NETWORK / NO SSH / NO REMOTE。

R30-R2：SUPERSEDED / VOID / NOT USED。没有恢复、重绑或复用。

本轮没有执行 Verification、fresh remote eligibility、SSH、upload、deployment、rollback、restart、activation、runtime-loaded validation、production acceptance、Git stage/commit/push/tag 或任何 repair。

## 3. Fresh baseline

| Check | Fresh result |
| --- | --- |
| project root | /Users/chenjie/Documents/MES/edge-mes-demo |
| branch | main |
| HEAD | 63d3cc70e787e0c837079aec0f5924dcbfa6a668 |
| origin/main | 63d3cc70e787e0c837079aec0f5924dcbfa6a668 |
| ahead/behind | 0 / 0 |
| cached index | empty |
| mapping worktree | clean |
| HEAD mapping blob | b46a637f23c761d0a4c3fe048b3b7480a3dec2ce |
| mapping bytes / SHA-256 | 7112 / d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d |
| git diff --check | PASS |
| git diff --cached --check | PASS |
| initial untracked count | 13764 |
| initial untracked NUL-delimited path-set SHA-256 | a5172c614b8330a9471ddc37320bca34778a072302ac256b200992c006ccdfb4 |
| ordinary environment variables | PYTHONDONTWRITEBYTECODE absent; PYTHONPYCACHEPREFIX absent |
| ordinary Python flags | sys.dont_write_bytecode=False; sys.pycache_prefix=None |
| scoped cache baseline | P2-R2: 0 __pycache__, 0 *.pyc; P2-R3: 0 __pycache__, 0 *.pyc |
| task-owned process scan | 0 |
| report path before write | ABSENT / NON-SYMLINK |

Pre-existing tracked dirty paths, not created by this Reliability task：

- .gitignore
- docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
- docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
- docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
- docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
- docs/thread_handoff/pm_operating_rules.md

The older handoff/status snapshots record 5fe72282... or earlier baselines. Live checkout and current persisted bytes were authoritative for this review, as required by the task. The R30 task authority explicitly supplied the current 63d3cc70... baseline; no baseline guess or path substitution was used.

## 4. Frozen identities

### 4.1 Repaired package and manifests

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh | 2653 | 943d44916af0b556bed0ca4c44cf309cba9fe10e62ff50f531e21bd68a486a7b |
| docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256 | 528 | f9dd9d8a3e49624dbdb1f8473e295371aeb90b51c2874adfac4aea757cd74749 |
| docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py | 63505 | 28d4b910df01d73c8d4d05264a9d63df1efc7751f1afb85f5f663491a396f0a4 |
| docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256 | 1122 | ae35c26d0709bf8b6c1ac500528e67b15f45393d8a782db0e2e3d6994a12a733 |

### 4.2 Tests、helpers、postflight and mapping

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py | 67695 | aa40fa64d8d9cc8508a6e0c480714778381bb2e13c21ffa14bd553205f3e9183 |
| docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py | 102372 | f19f4d0f19e6e21bfeb51931fa903cbf84eee107922be817ace9090050a5414c |
| docs/reports/evidence/d2_r7b_p2_r2/remote_preflight.py | 11129 | 6ddae658ed30ba38c20dcd3fa29fa9719cb940f3c8da4b904c6dfae810061f9c |
| docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py | 10563 | 30a02e5bc63545b08b1536e59abc418685cf846fbe2c930847d1f1b983f5ae7b |
| docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py | 15483 | 657498d42906c260ad12d53c16044a6a272cd1bea1a60ebfd2538b178baf02ff |
| docs/reports/evidence/d2_r7b_p2_r2/remote_rollback.py | 13248 | e2690ef991827ad8107430ee0449be913afa65dbf166fe2c1cf19fec0b7736ff |
| docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py | 15456 | b26051aa1fcbb71b84a16173f3c393542bd6c94bc24e619e4ebfb12c4d60d5ee |
| config/mapping.yaml | 7112 | d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d |

### 4.3 R30 durable reports

| Report | Bytes | SHA-256 |
| --- | ---: | --- |
| R30-P1 plan | 23698 | 7626686017485f190f8033232c71e550e20f980319509f773d5f5acbcc60e208 |
| R30-I1 implementation HOLD | 11145 | f313f1a8c0bcee0ea8687e2e2c5420f483e5b021e4a898dc9cefda34da98fa44 |
| R30-I1-R1 | 10503 | 1d2b258bbbce188749abdbdb03d8d064be28047e2edd21c84a64ce458afcda72 |
| R30-I1-R2 | 14627 | c1f7268953ae53ea0625bf67cc4404e18812b45ae72fd20839528013c6a7d2f8 |
| R30-I1-R3 | 16700 | 5d27c2c678d877928326b6d35f14a061a2526133b13c8c1cb141d906c50dc390 |

All frozen identities remained stable before tests, after cleanup, and before this report write. Report self-SHA is intentionally not recorded in this durable body to avoid self-reference; it is supplied in the Chat manifest after writing.

## 5. Exact diff and manifest closure

The live four-path diff is exactly:

1. local_materialization.sh: EXPECTED_COMMIT 8de5edbb504538a233abbcc80102cb714c9cee65 → 63d3cc70e787e0c837079aec0f5924dcbfa6a668；
2. remote_i1_orchestrator.py: EXPECTED_COMMIT 8de5edbb504538a233abbcc80102cb714c9cee65 → 63d3cc70e787e0c837079aec0f5924dcbfa6a668；
3. P2-R2 manifest: local_materialization digest only；
4. P2-R3 manifest: local_materialization digest and remote_i1_orchestrator digest only。

Diff assessment：

- old full commit occurrences in the current evidence tree: 0；
- new full commit occurrences: 2；
- semantic source assignment changes: 2 exact lines；
- remote helper/postflight source changes: 0；
- test source changes: 0；
- mapping changes: 0；
- remote artifact basename changes: 0。

Manifest closure：

- P2-R2：6 entries，directory-relative，sorted，duplicates 0，self-entry 0，hash verification 6/6 OK；
- P2-R3：9 entries，repository-root-relative，sorted，duplicates 0，self-entry 0，hash verification 9/9 OK；
- P2-R3 composite entry for local_materialization binds the current repaired P2-R2 materializer bytes, not the old manifest snapshot。

## 6. Local source gate and remote-contract non-regression

Static source and fresh matrix evidence show the local gate checks exact repository root, branch main, HEAD, origin/main, ahead/behind 0/0, cached-empty state, clean mapping, exact mapping blob/bytes/SHA and manifest-bound persisted source identities before any remote-capable phase. The stale/wrong HEAD, origin drift, ahead/behind drift, cached drift, mapping drift and manifest drift cases remain fail-closed with zero remote calls in the persisted matrices.

The repaired package preserves：

- endpoint mari@10.0.0.217；
- confirmation token D2-R7B-I1-CONFIG-ONLY；
- mapping payload identity；
- old remote target identity and exact preflight/postflight constants；
- phase order REMOTE_PREFLIGHT → REMOTE_UPLOAD → REMOTE_DEPLOY → one read-only REMOTE_POSTFLIGHT；
- source/payload transport separation；
- exact upload, backup and rollback paths；
- postflight classification and cross-phase identity binding；
- integer lifecycle counters cleanup_count=0, rollback_count=0, restart_count_by_task=0, activation_count=0；
- no automatic cleanup, automatic rollback, restart or activation。

The frozen transaction namespace is preserved, not migrated：

- .mapping.yaml.d2-r7b-new.8de5edb
- .mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml
- .mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml

No direct helper execution or orchestrator --execute was performed.

## 7. Fresh persisted test evidence

### 7.1 P2-R2

Command：python3 docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py

This command was run exactly once in the ordinary environment.

- exit: 0；
- matrix: PASS count=37/37；
- T18: PASS；
- T19: PASS, ordinary_env=True, cache_equal=True；
- stdout root lines: 20；
- realpath-deduplicated intended outer roots: 19；
- final validated cleanup: 19/19 removed, all absent；
- P2-R2 cleanup failures: 0；
- historical R26 retained root: not touched。

### 7.2 P2-R3

Command：python3 docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py

This command was run exactly once after P2-R2 PASS and successful final P2-R2 cleanup.

- exit: 0；
- matrix: E1-E50 PASS 50/50；
- E39: PASS；
- E40: PASS；
- stdout root lines: 4；
- observed unique paths: 3；
- intended outer roots: 2 (synthetic root plus underscore-prefixed retained root)；
- LOCAL_STAGE_PARENT: one descendant of the synthetic outer root；
- final root state: all exact stdout paths ABSENT；
- final post-cleanup remaining roots: 0。

Cleanup incident and finding：

The first P2-R3 cleanup validator inverted the ancestor test and selected LOCAL_STAGE_PARENT plus the independent retained root as deletion targets. It executed one exact bounded deletion on the descendant and one on the independent root, leaving the synthetic outer root. A corrected read-only validation then recognized the user-owned fixture symlink config-alias as a permitted child entry, and one exact outer-root deletion removed the synthetic root. No repository, foreign-owned object, historical R26 root or non-stdout path was touched. The final filesystem state is clean, but the intermediate descendant deletion is an actual deviation from the required cleanup ownership/deduplication contract.

## 8. Reliability closure matrix

| Finding / invariant | Status | Fresh evidence |
| --- | --- | --- |
| REL-R30-B1 exact local baseline pin | CLOSED | live HEAD/origin 63d3cc70...; exact source constants; P2-R2 T1/T13 and P2-R3 E3/E5/E6-style local gate cases |
| REL-R30-B2 mapping payload invariance | CLOSED | mapping clean; HEAD blob b46a637f...; 7112 bytes; SHA d9bb5...; T1/T3 and E local identity checks |
| REL-R30-B3 manifest cascade | CLOSED | exact four-path diff; P2-R2 6/6 and P2-R3 9/9 |
| REL-R30-B4 ordinary-environment test validity | CLOSED | environment flags absent; sys flags false/None; P2-R2 37/37 and P2-R3 50/50; T18/T19/E39/E40 PASS |
| REL-R30-B5 cleanup ownership | OPEN / IMPORTANT | P2-R3 first cleanup selected LOCAL_STAGE_PARENT descendant; final roots absent but ancestor/descendant dedup contract was violated |
| REL-R30-B6 remote contract non-regression | CLOSED | frozen constants, helpers/postflight/tests unchanged; phase and namespace static review; no remote call |
| REL-R30-B7 failure-state determinism | CLOSED | persisted T/E matrices cover local source, manifest, preflight, upload, deploy and postflight fail-closed branches |
| REL-R30-B8 lifecycle zero-action boundary | CLOSED | source and matrix assertions preserve scalar zero cleanup/rollback/restart/activation counters |
| REL-R30-B9 self-pin/Git sequencing | CLOSED | EXPECTED_COMMIT equals current HEAD; exact commit-before-execution consequence recorded; no Git mutation |
| REL-R30-B10 authority and evidence classification | CLOSED | local/static/synthetic evidence kept separate from remote/runtime/production claims; R30-R2 void |

No Critical finding was observed. The Important cleanup finding is sufficient for HOLD.

## 9. Temporary-root ownership and post-test audit

All P2-R2 stdout roots passed exact-path, absolute path, realpath, current-user ownership, system temporary-tree containment, repository exclusion, current-test time-window and recursive ownership checks before deletion. P2-R2 used the two authorized prefixes d2-r7b-p2-r2 and d2_r7b_p2_r2.

P2-R3 exact stdout paths were all current-test, user-owned, repository-external and within the two authorized prefixes or the synthetic outer root. The synthetic fixture contained a user-owned symlink child; the outer root itself was a regular non-symlink directory. Final exact stdout paths are absent. The intermediate descendant deletion is recorded above as a gating deviation rather than hidden as a successful cleanup.

Post-test audit：

- scoped P2-R2 cache: 0 __pycache__, 0 *.pyc；
- scoped P2-R3 cache: 0 __pycache__, 0 *.pyc；
- package/test/helper/postflight/mapping identities: unchanged；
- manifests after tests: 6/6 and 9/9；
- HEAD/origin/ahead-behind: unchanged at 63d3cc70... / 63d3cc70... / 0/0；
- cached index: empty；
- tracked dirty set: unchanged six pre-existing paths；
- task-owned process after cleanup: 0；
- network / SSH / remote counters: 0 / 0 / 0。

## 10. Evidence classification

Accepted for this Reliability gate：

- live local Git and filesystem facts；
- persisted source/manifest identities；
- static contract review；
- ordinary-environment persisted local/synthetic matrices；
- bounded cleanup final absence evidence。

Not established：

- remote deployment；
- fresh remote eligibility；
- runtime config load；
- Collector activation/restart；
- production acceptance；
- any remote mutation or remote state after this review。

The strings mari@10.0.0.217 and the remote artifact paths were source/fixture contract data only; no connection was made.

## 11. Final Git and untracked boundary

Before writing this report, the NUL-delimited untracked set remained exactly the initial set：

- count: 13764；
- SHA-256: a5172c614b8330a9471ddc37320bca34778a072302ac256b200992c006ccdfb4。

The expected final set after this report write is the accepted initial 13764-path set plus this exact report path only. The report path is not included in this body’s self-hash calculation.

Git：

- HEAD: 63d3cc70e787e0c837079aec0f5924dcbfa6a668；
- origin/main: 63d3cc70e787e0c837079aec0f5924dcbfa6a668；
- ahead/behind: 0/0；
- cached: empty；
- Git mutation: 0。

## 12. MVP path and Thread context

- current MVP support: yes — this review protects the exact local config-deployment compatibility and fail-closed evidence boundary；
- minimum invariant: exact current baseline, mapping payload, manifest closure, ordinary loader behavior and bounded test cleanup must remain fail-closed；
- scope expansion: no；
- task inflation: no；
- classification: MVP-ALIGNED / RELIABILITY_HOLD。

本次输出长度：长，完整 evidence 位于本 durable report，Chat 只返回 concise manifest。

当前 Thread 是否建议继续：no。

下一轮是否建议新开 Thread：yes。

理由：本轮已完成 independent Reliability review 和一次性 fresh matrices；存在需要 PM intake 后单独处置的 Important cleanup-boundary finding，不能在本 Thread 继续 repair、Verification、Git 或 remote gate。

## 13. Delivery state and next gate

本报告写入后只建立 WRITTEN。它不建立 ACCEPTED、VERIFIED、STAGED、COMMITTED、PUSHED、REMOTE-ELIGIBLE、DEPLOYED、ACTIVATED、RUNTIME-LOADED 或 PRODUCTION-ACCEPTED。

Immediate next gate：

RELIABILITY-HOLD / WRITTEN → ChatGPT PM durable intake

PM intake 后，如需继续，应以新的明确 authority 单独安排 cleanup-boundary repair 或 focused Architecture / Integration repair，再重新建立独立 Reliability review。不得在本报告基础上恢复 R30-R2，也不得自动进入 Verification、Git、fresh remote eligibility、SSH、upload、deployment、rollback、restart、activation 或 production acceptance。
