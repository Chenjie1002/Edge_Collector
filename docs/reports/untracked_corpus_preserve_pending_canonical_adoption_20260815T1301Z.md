# UNTRACKED_CORPUS_PRESERVE_PENDING_CANONICAL_ADOPTION — PM Review Report

## Terminal before Git mutation

`PASS / CANONICAL_ADOPTION_PACKAGE_READY_FOR_EXACT_LOCAL_COMMIT`

Owner authorized `UNTRACKED_CORPUS_PRESERVE_PENDING_CANONICAL_ADOPTION`. This review prepares a bounded 16-path local Git adoption transaction. No stage, commit, push, archive, delete, ignore, Docker, database, PLC/V-PLC, remote, or product mutation has occurred while preparing this report.

## Repository entry baseline

- branch: `main`
- `HEAD=8bf994c60ffa6dd9bd082c5d9d40bbfbf8041239`
- `origin/main=6226bf3fb716880a176f9eb642b8139cef3255a6`
- main is locally ahead of origin by one accepted canonical-continuity commit
- staged: `0`
- tracked dirty: `0`
- pre-gate untracked count: `678`

The prior local commit is immutable continuity for this gate and is not amended/rebased/reset/pushed.

## Semantic source authority

Accepted semantic reconciliation:

`docs/reports/untracked_corpus_preserve_pending_semantic_manifest_20260815T1251Z.tsv`

- bytes: `4625`
- SHA-256: `24b6e459fa09ba8308b53f2d5485cb1894c8f2dcfb40fa2c25e7b259d3663a58`

The semantic classifier resolved all former `PRESERVE_PENDING` files and identified exactly 13 `KEEP_ON_MAIN_CANDIDATE` paths because they are direct dependencies of current mainline authority/current-status governance or the still-open `FIELD-VALIDATION-COLLECTOR-DB` branch authority chain.

Frozen semantic keep identity:

- count: `13`
- bytes: `188368`
- pathset SHA-256: `3d583f050d8f1e094980613c64bae4c5caaffaa2c793774bd20e0048e77d28e6`
- semantic-classifier recordset SHA-256: `e5c7cc1601924edc5b9e2da185ab5673bfd2d9bdc04c404e1929b26cc2940d4d`
- high-confidence secret-marker files: `0`

The adoption manifest uses a narrower four-column row schema (`path,bytes,sha256,family`), so its own row-stream hash is intentionally not compared to the semantic-classifier recordset hash. Mechanical adoption authority is instead bound to all 13 individual file bytes/SHA values plus the semantic manifest identity and keep pathset.

## Exact keep set rationale

The 13 paths consist of:

- nine current G5/accepted-runtime durable reports still directly referenced by current mainline authority;
- `chatgpt_pm_handoff_260814-2303.md`, the immediate predecessor of the currently tracked mainline handoff;
- `chatgpt_pm_handoff_real_device_collector_db_branch_260808-0832.md`, the still-open `FIELD-VALIDATION-COLLECTOR-DB` branch handoff;
- `branch_real_device_collector_db_field_validation_plan.md`, the branch handoff's primary durable plan;
- `chatgpt_pm_handoff_260808-0807.md` plus the legacy `docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md` authority dependencies retained by current governance/branch references.

These are not selected merely because they are recent. Their retention is based on live authority-reference dependency.

## Exact adoption manifest

`docs/reports/untracked_corpus_preserve_pending_canonical_adoption_manifest_20260815T1301Z.tsv`

The manifest lists every one of the 13 exact paths with bytes, SHA-256 and family. Corrected verification after manifest creation returned:

- rows: `13`
- bytes sum: `188368`
- no individual `DRIFT=` result

## Gate control artifacts

The local commit may additionally adopt only:

1. `docs/thread_handoff/pm_task_20260815T1301Z_untracked_corpus_preserve_pending_canonical_adoption.md`
2. `docs/reports/untracked_corpus_preserve_pending_canonical_adoption_manifest_20260815T1301Z.tsv`
3. this report

Therefore final commit allowlist = `13 + 3 = 16` paths.

## Explicit exclusions

This gate does not touch:

- the `51 SUPERSEDED_BUT_AUDITABLE + 594 ARCHIVE_TRANCHE_2_CANDIDATE = 645` files reserved for a later archive tranche;
- existing local archive branch `archive/pm-evidence-20260815`;
- `.codex/**`, `AGENTS.md`;
- `frontend/next-env.d.ts`;
- the known exact duplicate mapping evidence copy;
- earlier corpus/archive governance control artifacts not in this exact allowlist;
- product source/runtime/database/PLC/V-PLC/remote state.

## Git transaction recommendation

Owner Terminal may perform exactly:

1. revalidate baseline and all 13 individual identities;
2. revalidate the three gate artifacts against mechanically published bytes/SHA;
3. stage exactly the 16 allowlisted paths;
4. assert staged count and frozen 16-path pathset;
5. run focused `git diff --cached --check` on the three newly authored gate artifacts only;
6. create one local commit with message `docs: adopt remaining canonical PM authority evidence`;
7. verify commit parent, 16 changed paths, clean staged/tracked state, unchanged `origin/main`, and no push.

Historical evidence bytes must not be rewritten to satisfy modern formatting rules.

## Expected post-commit meaning

A PASS means the remaining current mainline/branch authority dependencies are durably stored in main Git history. It does not mean the historical corpus is fully cleaned. Tranche-2 archive, local tooling review, generated-file decision, exact-duplicate cleanup, archive privacy review and publication remain separate future authorities.
