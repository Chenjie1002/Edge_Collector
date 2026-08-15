# UNTRACKED_CORPUS_PRESERVE_PENDING_CANONICAL_ADOPTION

## 1. Owner authority

Owner explicitly approved `UNTRACKED_CORPUS_PRESERVE_PENDING_CANONICAL_ADOPTION` on 2026-08-15.

This authority is bounded to adopting the exact 13 `KEEP_ON_MAIN_CANDIDATE` files identified by the accepted semantic reconciliation, plus this gate's exact task/manifest/report. It authorizes one exact Git stage and one local commit only. Push is not authorized.

## 2. Repository baseline

Expected entry baseline:

- branch: `main`
- `HEAD=8bf994c60ffa6dd9bd082c5d9d40bbfbf8041239`
- `origin/main=6226bf3fb716880a176f9eb642b8139cef3255a6`
- local main ahead/behind: `1/0`
- staged: `0`
- tracked dirty: `0`
- pre-task untracked count: `678`

The existing local commit `8bf994c...` is accepted continuity and must not be rewritten, amended, rebased, reset, or pushed by this gate.

## 3. Source semantic authority

Accepted source manifest:

`docs/reports/untracked_corpus_preserve_pending_semantic_manifest_20260815T1251Z.tsv`

Identity:

- bytes: `4625`
- SHA-256: `24b6e459fa09ba8308b53f2d5485cb1894c8f2dcfb40fa2c25e7b259d3663a58`

Frozen keep set:

- count: `13`
- bytes: `188368`
- pathset SHA-256: `3d583f050d8f1e094980613c64bae4c5caaffaa2c793774bd20e0048e77d28e6`
- recordset SHA-256: `e5c7cc1601924edc5b9e2da185ab5673bfd2d9bdc04c404e1929b26cc2940d4d`
- high-confidence secret marker matches: `0`

## 4. Exact 13-file adoption allowlist

1. `docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`
2. `docs/reports/branch_real_device_collector_db_field_validation_plan.md`
3. `docs/reports/mainline_pm_a1_vp2_g5_adapter_result_combination_invalid_cause_isolation_r2_order_unambiguous_dependency_free_parent_independent_intake_20260814T1438Z.md`
4. `docs/reports/mainline_pm_a1_vp2_g5_cross_station_focus_only_db_rca_r3_parent_independent_intake_20260814T1327Z.md`
5. `docs/reports/mainline_pm_a1_vp2_g5_local_candidate_independent_closeout_goal_closeout.md`
6. `docs/reports/mainline_pm_a1_vp2_g5_local_candidate_reliability_focused_review_20260815T0128Z.md`
7. `docs/reports/mainline_pm_a1_vp2_g5_local_candidate_verification_focused_review_20260815T0142Z.md`
8. `docs/reports/mainline_pm_a1_vp2_g5_runtime_deployment_evidence_split_final_verification.md`
9. `docs/reports/mainline_pm_a1_vp2_g5_runtime_deployment_evidence_split_goal_closeout.md`
10. `docs/reports/mainline_pm_a1_vp2_g5_runtime_deployment_evidence_split_shadow_pm_ledger.md`
11. `docs/thread_handoff/chatgpt_pm_handoff_260808-0807.md`
12. `docs/thread_handoff/chatgpt_pm_handoff_260814-2303.md`
13. `docs/thread_handoff/chatgpt_pm_handoff_real_device_collector_db_branch_260808-0832.md`

These files are adopted because they are direct dependencies of current mainline authority/current status/PM rules or of the still-open `FIELD-VALIDATION-COLLECTOR-DB` branch authority chain.

## 5. Gate control artifacts

This gate may additionally stage exactly:

- `docs/thread_handoff/pm_task_20260815T1301Z_untracked_corpus_preserve_pending_canonical_adoption.md`
- `docs/reports/untracked_corpus_preserve_pending_canonical_adoption_manifest_20260815T1301Z.tsv`
- `docs/reports/untracked_corpus_preserve_pending_canonical_adoption_20260815T1301Z.md`

Final staged allowlist count must therefore be exactly `16`.

## 6. Explicitly excluded corpus

This gate must not stage, edit, delete, archive, ignore, move, rename, or otherwise mutate:

- the `645` tranche-2 historical archive candidates;
- `.codex/**` or `AGENTS.md`;
- `frontend/next-env.d.ts`;
- the exact duplicate `docs/reports/evidence/d2_r7b_i1_r67_r3_existing_candidate_validation_only_acceptance/input/config/mapping.yaml`;
- prior archive control/governance artifacts not in this gate's exact allowlist;
- product source, tests, runtime configuration, database, Docker state, PLC/V-PLC state, remote state, or archive branch refs.

No broad `git add .`, `git add docs/`, `git clean`, reset, stash, rebase, amend, checkout, branch mutation, merge, cherry-pick, or push is allowed.

## 7. Execution hard gates

Before staging:

1. exact baseline identities must match Section 2;
2. staged must be empty and tracked dirty must be zero;
3. all 13 files must be regular/non-symlink and untracked;
4. exact count/bytes/pathset/recordset identities must match Section 3;
5. gate task/manifest/report must match their mechanically published identities;
6. no candidate may have a high-confidence secret marker hit.

Any mismatch terminates `HOLD` before staging.

## 8. Exact stage semantics

Stage only the 16 exact allowlist paths.

After staging:

- staged path count must equal `16`;
- staged pathset must equal the frozen final allowlist pathset published by this gate;
- no non-allowlisted path may be staged.

Focused `git diff --cached --check` must be applied to the three newly authored gate artifacts. Historical adopted evidence bytes must not be rewritten merely to satisfy current whitespace conventions.

## 9. Commit semantics

Exactly one local commit is authorized with message:

`docs: adopt remaining canonical PM authority evidence`

Requirements:

- commit parent must be `8bf994c60ffa6dd9bd082c5d9d40bbfbf8041239`;
- commit changed-path count must equal `16`;
- commit pathset must match the frozen 16-path allowlist;
- after commit staged and tracked dirty must both be `0`;
- `origin/main` must remain `6226bf3fb716880a176f9eb642b8139cef3255a6`;
- no push.

Commit failure preserves staged state and stops. No retry, reset, amend, or cleanup is authorized.

## 10. Expected result

Success terminal:

`PASS / UNTRACKED_CORPUS_PRESERVE_PENDING_CANONICAL_ADOPTION_COMMITTED`

This establishes durable Git retention for the 13 current/branch authority dependencies and this gate's governance artifacts only. It does not close the historical tranche-2 archive work, the local tooling review, generated-file decision, or exact-duplicate cleanup.
