# UNTRACKED_CORPUS_GOVERNANCE_CONTROL_CLOSEOUT — DURABLE REPORT

## 1. Terminal claim target

```text
PASS / UNTRACKED_CORPUS_GOVERNANCE_CONTROL_CLOSEOUT_COMPLETE
REPORT_DELIVERY = REPOSITORY_DURABLE_REPORT
EVIDENCE_CLASS  = LOCAL REPOSITORY / LOCAL ARCHIVE ONLY
```

本报告记录本轮 corpus-governance closeout 的 authority、冻结源集、archive tranche 3、exact working-copy removal、status sync，以及 Section F exact 3-path main stage/commit 的完整约束。最终 PASS 仅在 task Section 10.G 的 post-commit 条件全部 fresh verified 后成立；本报告不把本地证据升级为 remote/runtime/production acceptance。

## 2. Authority and entry baseline

唯一 authority：

```text
TASK = docs/thread_handoff/pm_task_20260815T1400Z_untracked_corpus_governance_control_closeout.md
TYPE = regular / non-symlink
BYTES = 11958
SHA-256 = 4083829754d691639d593336cb385a863e03fb1393f743019170a6de660cef77
```

Required reading order completed exactly：task、`AGENTS.md`、`docs/thread_handoff/pm_operating_rules.md`、`.agents/skills/edge-mes-pm-governance/SKILL.md`、`references/task-materialization-contract.md`、`docs/current_status.md`、`docs/thread_handoff/chatgpt_pm_handoff_260815-1654.md`、tranche-2 closeout report.

Root proof：

```text
PHYSICAL_CWD        = /Users/chenjie/Documents/MES/edge-mes-demo
GIT_ROOT            = /Users/chenjie/Documents/MES/edge-mes-demo
BRANCH              = main
MAIN_HEAD           = 3f6ba2c31e33f9fecd4d8fcb5d0a6353e5e4e16d
ORIGIN_MAIN         = 6226bf3fb716880a176f9eb642b8139cef3255a6
LOCAL_AHEAD         = 4
STAGED              = 0
TRACKED_DIRTY       = 0
UNTRACKED           = 16
ARCHIVE_OLD_REF     = 64d8610e8368c2175ddf2d25fd42929fae36b9ae
REMOTE_ARCHIVE_REF  = ABSENT
REPORT_PRESTATE     = ABSENT / non-symlink
TEMP_INDEX_PRESTATE = ABSENT / non-symlink
```

Entry untracked membership was exactly the task file plus the frozen 15-file source set. No unrelated path was adopted, cleaned, reset, stashed or staged.

## 3. Frozen 15-file source set

The source set was mechanically defined as all current untracked paths minus the exact task path. Every source was regular, non-symlink, untracked, not ignored and not indexed.

```text
COUNT            = 15
TOTAL_BYTES      = 92059
PATHSET_SHA256   = 2c671eac5448ed36d2a03d08783f5aa0f09577144e0f530474708cb948a81aa1
RECORDSET_SHA256 = f39c9295126033114ff1f3ef7682f133917c4ae75206e58ae15130a2e869993e
RECORDSET_SCHEMA = path<TAB>bytes<TAB>sha256
```

Frozen records (all live and archive modes verified as `100644`)：

```text
docs/reports/untracked_corpus_historical_evidence_archive_closeout_20260815T1244Z.md	7743	57036789f3011796e3aa2660b8d2c91a247f172bef0b4287dd597e937f8af8da
docs/reports/untracked_corpus_historical_evidence_archive_manifest_20260815T1231Z.tsv	2200	9dad4f87b1d8e0e6ac9ac466f49afc49c35890514f1816734d05908dbfcf895f
docs/reports/untracked_corpus_historical_evidence_archive_manifest_r2_20260815T1238Z.tsv	683	ee9aa69cc60f9c7ff30036d372e2e4a7477ccc4e325a39640bec1858b8e7c6d2
docs/reports/untracked_corpus_historical_evidence_archive_tranche_2_20260815T1320Z.md	6345	ad7668a67c0d1cbebd330358408cf5e2faed132ae0d82bed96cdc305cce4553e
docs/reports/untracked_corpus_historical_evidence_archive_tranche_2_closeout_20260815T1332Z.md	8455	6ed1e2fe454c6ab18d3495b8d9d6081cb899839b11655b14deab8a3665d20770
docs/reports/untracked_corpus_historical_evidence_archive_tranche_2_manifest_20260815T1320Z.tsv	1842	9de3581435a1db2b9683e8ecb6e32b42242b4d71818e33795be461b0fa1b5886
docs/reports/untracked_corpus_manifest_20260815T1137Z.tsv	5008	0d5537ee8e5298fbbfde7075e5447ae00e15d6e863f0e8f90aad66e2150fd9b0
docs/reports/untracked_corpus_preserve_pending_semantic_manifest_20260815T1251Z.tsv	4625	24b6e459fa09ba8308b53f2d5485cb1894c8f2dcfb40fa2c25e7b259d3663a58
docs/reports/untracked_corpus_preserve_pending_semantic_reconciliation_20260815T1251Z.md	12835	933bf5672d654417a98c6e6ff9ef2b211d48045aeeb2d9c156c3071a365579e0
docs/reports/untracked_corpus_reconciliation_and_retention_20260815T1137Z.md	10356	44e1f76862f5becd53a81972aabb1d0c85c2be5d593787b7c3882962d25a9bd9
docs/thread_handoff/pm_task_20260815T1137Z_untracked_corpus_reconciliation_and_retention.md	5698	66b7bb658e88cf0f20a85b52024a42c88c918ba1d4c20d5eae30d5bcf50cca70
docs/thread_handoff/pm_task_20260815T1231Z_untracked_corpus_historical_evidence_archive.md	8393	6b1b9f65120e19706837de16b0752eda563075f36514bd9cf2d12ce01a402359
docs/thread_handoff/pm_task_20260815T1238Z_untracked_corpus_historical_evidence_archive_r2.md	2022	1993d4e0015ac00c23b8101bc62520b6c160284d59acb1fd9e1d91eed4deb2c5
docs/thread_handoff/pm_task_20260815T1251Z_untracked_corpus_preserve_pending_semantic_reconciliation.md	7961	caf4822922a4a22f66c7505c529cf58df5d3f06ad02713930f70ad6e1ac36285
docs/thread_handoff/pm_task_20260815T1320Z_untracked_corpus_historical_evidence_archive_tranche_2.md	7893	983586a57d73f467179e957d23d27b7e6712a891a3e6741ac25b3c6d93f8e4cd
```

## 4. Archive tranche 3

The local archive was built through the exact temporary index `.git/pm-governance-closeout.index`; the main index was not touched. The temporary index was removed after verification.

```text
ARCHIVE_BRANCH        = archive/pm-evidence-20260815
OLD_COMMIT            = 64d8610e8368c2175ddf2d25fd42929fae36b9ae
OLD_COMMIT_PARENT     = f83a4be12d767b0649a6dc268b131766ab9b1f1f
NEW_COMMIT            = 419174f85d4ad1c8129c327a4525ef6b410e74f2
NEW_COMMIT_PARENT     = 64d8610e8368c2175ddf2d25fd42929fae36b9ae
NEW_COMMIT_SUBJECT    = archive: preserve corpus governance controls
NEW_TREE              = efeb48006bd73e1a69857bf74b386da73e325a7d
OLD..NEW_PATHS        = 15 exact additions
PATHSET_SHA256        = 2c671eac5448ed36d2a03d08783f5aa0f09577144e0f530474708cb948a81aa1
BLOB_BYTES            = 92059
BLOB_RECORDSET_SHA256= f39c9295126033114ff1f3ef7682f133917c4ae75206e58ae15130a2e869993e
REF_UPDATE            = old-value compare-and-swap PASS
REF_AFTER_UPDATE      = 419174f85d4ad1c8129c327a4525ef6b410e74f2
REF_PARENT_AFTER      = 64d8610e8368c2175ddf2d25fd42929fae36b9ae
REMOTE_TRACKING_REF   = ABSENT
PUSHED                = NO
```

Before the ref move, the candidate tree and candidate commit were independently checked for exact 15 additions, exact pathset, regular-file modes and every candidate blob byte count/SHA. The same parent/pathset/blob checks were repeated after CAS.

## 5. Working-copy removal

After archive CAS and a fresh re-read of all 15 live source identities against the frozen recordset, exactly those 15 paths were removed. No other working copy was targeted.

```text
REMOVED_WORKING_COPIES     = 15
REMOVAL_SCOPE              = frozen SOURCE_SET only
POST_REMOVAL_UNTRACKED     = 1
POST_REMOVAL_UNTRACKED_PATH= docs/thread_handoff/pm_task_20260815T1400Z_untracked_corpus_governance_control_closeout.md
TEMP_INDEX                 = ABSENT
MAIN_INDEX                 = unchanged / staged 0
```

## 6. Current status synchronization

Only `docs/current_status.md` was modified before report creation. A new highest-priority block `## 0R. 2026-08-15 Untracked Corpus Governance Closeout` was inserted immediately before the existing `## 0Q`; the older status blocks were not rewritten, deleted or reordered. `git diff --check` passed and the tracked diff contained only this path.

The block records local historical corpus reconciliation closure, archive tranche 1/2/3 counts (`516 / 645 / 15`), tranche-3 commit and parent, main pre-closeout HEAD, `PUSHED = NO`, the final hygiene target `staged 0 / tracked dirty 0 / untracked 0`, unchanged product/runtime/remote acceptance boundaries and continued `FIELD-VALIDATION-COLLECTOR-DB` isolation.

## 7. Exact main Git closeout authority

Section F is authorized once the following pre-stage facts remain true：

```text
MAIN_HEAD_BEFORE_COMMIT = 3f6ba2c31e33f9fecd4d8fcb5d0a6353e5e4e16d
ORIGIN_MAIN            = 6226bf3fb716880a176f9eb642b8139cef3255a6
ARCHIVE_REF            = 419174f85d4ad1c8129c327a4525ef6b410e74f2
TRACKED_DIFF           = docs/current_status.md only
UNTRACKED              = task + exact report only
WORKTREE_DIFF_CHECK    = PASS
```

The only paths authorized for one exact stage and one main commit are：

```text
docs/current_status.md
docs/reports/untracked_corpus_governance_control_closeout_20260815T1400Z.md
docs/thread_handoff/pm_task_20260815T1400Z_untracked_corpus_governance_control_closeout.md
```

The cached pathset must be C-locale sorted with final LF and SHA-256：

```text
f681fa5a59d0619f941e7af26a628d031d70cfcd0162f938e7bb3f0e56539911
```

Required checks are exact cached allowlist, `git diff --cached --check`, one commit with subject `docs: close untracked corpus governance controls`, then post-commit verification of parent, changed paths, staged/dirty/untracked counts, origin/main, archive continuity and absent remote archive tracking. `PUSHED = NO` is a hard terminal boundary.

## 8. Explicit non-claims and boundaries

This closeout performed no product/source/test/frontend mutation, runtime/Docker lifecycle, DB/API action, PLC/V-PLC action, SSH/network/fetch/pull/push/tag, deploy, reset, stash, clean or broad staging. The local archive is not remote publication. Local Git/archive/report evidence is not runtime-loaded, DB-backed, production or Owner acceptance evidence.

`P1_G6_PM_ACCEPTANCE` remains CLOSED / PASS; `REMOTE_G5_PRODUCTION_ACCEPTANCE` is unchanged; `A1_S2` remains not authorized; `FIELD-VALIDATION-COLLECTOR-DB` remains governance-isolated.

## 9. MVP alignment and next gate

```text
MVP_PATH_ALIGNMENT       = MVP-ALIGNED / repository-hygiene prerequisite
PRODUCT_CAPABILITY_ADDED = NO
CLAIM_EXPANSION          = NO
```

This task preserves accepted local governance evidence and removes only exact redundant working copies; it does not replace product delivery or create a new audit/forensics subsystem. The single remaining gate in this task is exact Section F main stage/commit and post-commit verification. On PASS, this corpus-governance cleanup workstream is locally closed with no additional corpus micro-gate; control returns to Mainline PM for normal product prioritization/handoff decisions.

## 10. State separation

At report creation, the report state is `WRITTEN`; it is not by itself `REVIEWED`, `ACCEPTED`, `VERIFIED`, `STAGED`, `COMMITTED`, `PUSHED`, `DEPLOYED`, `ACTIVATED`, `RUNTIME_LOADED` or `PRODUCTION_ACCEPTED`. The final window manifest must independently report the actual main commit and final Git/archive facts.
