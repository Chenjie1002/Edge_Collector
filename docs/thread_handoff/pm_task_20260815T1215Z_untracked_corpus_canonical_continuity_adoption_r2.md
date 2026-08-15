# UNTRACKED_CORPUS_CANONICAL_CONTINUITY_ADOPTION_R2

## 1. Authority

Owner explicitly approved `UNTRACKED_CORPUS_CANONICAL_CONTINUITY_ADOPTION_R2` after R1 stopped at the cached whitespace gate.

This successor does not rewrite, normalize, repair, delete, move, or restage the historical evidence already staged by R1. It exists only to close the exact Git commit transaction while preserving immutable historical bytes.

## 2. Historical predecessor terminal

R1 historical terminal is preserved as:

`HOLD / CACHED_DIFF_CHECK_FAILED`

Cause: `git diff --cached --check` returned non-zero because already-authored historical Markdown evidence contains Markdown hard-break trailing spaces and/or historical EOF blank-line variance. The output line `执行 Thread：Architecture / Integration` was historical document content printed by Git, not an active Thread or hung process.

R1 did successfully stage the exact allowlist before this HOLD.

## 3. R2 entry identity

Required entry facts:

- branch: `main`
- `HEAD=6226bf3fb716880a176f9eb642b8139cef3255a6`
- `origin/main=6226bf3fb716880a176f9eb642b8139cef3255a6`
- staged path count: `104`
- staged pathset SHA-256: `12a7b27c1c062593087eac008629a8d02bf582ba70098712d4faf67afc8a5f4e`
- staged binary diff SHA-256: `02fc8723a992dc2ff2c4b3a4d9d150c2041fd68b24dbf4eb282956ee6391a3ad`
- remaining untracked count before R2 task/report: `1186`
- focused newly-authored/canonical cached diff check: `0`
- global cached diff check: historical variance, RC `2`, warning lines `37`

If the 104-path staged pathset or staged binary diff identity differs, R2 must HOLD before any additional stage or commit.

## 4. Historical format variance policy

R2 explicitly accepts the existing global whitespace warnings as `HISTORICAL_FORMAT_VARIANCE` only when all of the following remain true:

1. the frozen R1 staged pathset and staged binary diff identities match exactly;
2. no high-confidence secret marker was found in the 100 candidate continuity files during R1 review;
3. the newly authored/canonical set passes focused `git diff --cached --check`;
4. no historical evidence file is edited merely to make `git diff --check` green.

This variance is not a product defect and not authority to weaken future source-code whitespace checks.

## 5. Exact mutation authority

R2 authorizes exactly:

1. stage this R2 task file;
2. stage the exact R2 report file:
   `docs/reports/untracked_corpus_canonical_continuity_adoption_r2_20260815T1215Z.md`;
3. verify the final staged path count and exact allowlist;
4. run focused cached diff check only on the newly-authored/canonical governance set;
5. execute exactly one Git commit with message:
   `docs: adopt canonical PM continuity evidence`.

No second commit, retry, reset, unstage, amend, rebase, checkout, restore, stash, clean, push, tag, branch creation, file rewrite, or broad `git add` is authorized.

## 6. Exact preserved R1 staged set

The existing 104 staged paths are immutable input to this successor. R2 does not re-run `git add` for them.

Their authority is represented by both frozen identities:

- pathset SHA-256 `12a7b27c1c062593087eac008629a8d02bf582ba70098712d4faf67afc8a5f4e`
- staged binary diff SHA-256 `02fc8723a992dc2ff2c4b3a4d9d150c2041fd68b24dbf4eb282956ee6391a3ad`

## 7. Focused check allowlist

After staging the two R2 governance artifacts, focused `git diff --cached --check` must pass for exactly these newly authored/canonical files:

- `docs/current_status.md`
- `docs/thread_handoff/pm_task_20260815T1203Z_untracked_corpus_canonical_continuity_adoption.md`
- `docs/reports/untracked_corpus_canonical_continuity_candidates_20260815T1203Z.tsv`
- `docs/reports/untracked_corpus_canonical_continuity_adoption_20260815T1203Z.md`
- `docs/thread_handoff/pm_task_20260815T1215Z_untracked_corpus_canonical_continuity_adoption_r2.md`
- `docs/reports/untracked_corpus_canonical_continuity_adoption_r2_20260815T1215Z.md`

The global historical cached check may remain RC 2 / 37 warning lines and is recorded, not repaired.

## 8. Commit success criteria

PASS requires:

- exact R1 staged identity preserved before R2 additions;
- R2 task/report exact identities verified;
- final staged count `106`;
- focused cached diff check `0`;
- exactly one commit RC `0`;
- commit parent exactly `6226bf3fb716880a176f9eb642b8139cef3255a6`;
- staged empty after commit;
- `origin/main` unchanged at predecessor because push is not authorized;
- remaining untracked count expected `1186` after the two R2 governance files are staged/committed; the pre-existing 104 staged paths are already excluded from `git ls-files --others`;
- no Docker, DB, HTTP, remote, source, config, runtime, cleanup, or product mutation.

## 9. Failure semantics

Any identity mismatch before commit => `HOLD / R2_STAGED_IDENTITY_DRIFT`.

Focused new/canonical whitespace failure => `HOLD / R2_FOCUSED_DIFF_CHECK_FAILED`.

Commit failure => `HOLD / R2_COMMIT_FAILED`, preserve staged state, no retry.

Post-commit count variance does not rewrite a successful commit; report exact observed state for Mainline PM intake.

## 10. Push boundary

`PUSHED=NO` is required. Publication to `origin/main` requires a later explicit Owner authority.
