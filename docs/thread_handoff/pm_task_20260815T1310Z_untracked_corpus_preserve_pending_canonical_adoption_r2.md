# UNTRACKED_CORPUS_PRESERVE_PENDING_CANONICAL_ADOPTION_R2

## 1. Owner authority

Owner explicitly approved:

`UNTRACKED_CORPUS_PRESERVE_PENDING_CANONICAL_ADOPTION_R2`

This is a focused successor to the historical terminal:

`HOLD / CANONICAL_ADOPTION_STAGED_ALLOWLIST_MISMATCH`

The predecessor HOLD is immutable. R2 does not rewrite it.

## 2. Exact defect corrected

The predecessor transaction staged the exact intended 16 paths, but computed the staged pathset hash from default `git diff --cached --name-only` output. Git default `core.quotePath` C-style-quoted the Unicode em dash in:

`docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`

This changed only the display string used for hashing and produced a false mismatch.

Independent read-only reconciliation proved:

```text
STAGED_COUNT = 16
DEFAULT_DISPLAY_HASH = 1e6c280a8e5aa3e9cd8bc1d0db75f96411c823b6ee73daa17df346247e796fb2
UNQUOTED_PATHSET_HASH = a4468cfe09b142d9fe83ce2b3b8c55e22ee672ce59abc63735a0696fa70ead15
EXPECTED_PATHSET_HASH = a4468cfe09b142d9fe83ce2b3b8c55e22ee672ce59abc63735a0696fa70ead15
STAGED_ALLOWLIST_ACTUALLY_MATCHES = YES
```

R2 therefore uses `git -c core.quotePath=false diff --cached --name-only` for authority-bearing path identity.

## 3. Entry baseline

R2 entry was mechanically observed as:

```text
main HEAD = 8bf994c60ffa6dd9bd082c5d9d40bbfbf8041239
origin/main = 6226bf3fb716880a176f9eb642b8139cef3255a6
staged = 16
staged unquoted pathset SHA-256 = a4468cfe09b142d9fe83ce2b3b8c55e22ee672ce59abc63735a0696fa70ead15
unstaged tracked = 0
untracked = 665
```

The existing 16 staged paths are retained exactly. R2 must not reset, unstage, restage, rewrite, normalize, or otherwise mutate those staged file bytes before the R2 continuation transaction.

## 4. Existing staged authority

The existing staged set consists only of the 13 semantic `KEEP_ON_MAIN_CANDIDATE` files plus the predecessor adoption task, manifest, and report.

The 13 keep files are frozen by:

```text
KEEP_COUNT = 13
KEEP_BYTES = 188368
KEEP_PATHSET_SHA256 = 3d583f050d8f1e094980613c64bae4c5caaffaa2c793774bd20e0048e77d28e6
semantic recordset SHA-256 = e5c7cc1601924edc5b9e2da185ab5673bfd2d9bdc04c404e1929b26cc2940d4d
```

Predecessor 16-path staged pathset:

`a4468cfe09b142d9fe83ce2b3b8c55e22ee672ce59abc63735a0696fa70ead15`

## 5. R2 write allowlist

R2 may create and later stage exactly these two new governance artifacts:

1. `docs/thread_handoff/pm_task_20260815T1310Z_untracked_corpus_preserve_pending_canonical_adoption_r2.md`
2. `docs/reports/untracked_corpus_preserve_pending_canonical_adoption_r2_20260815T1310Z.md`

No other file write is authorized by R2.

## 6. Git mutation authority

After both R2 artifacts are frozen by regular/non-symlink, bytes, and SHA-256, Owner Terminal may:

1. verify the existing 16 staged paths using `core.quotePath=false`;
2. stage exactly the two R2 artifacts;
3. verify the final staged set is exactly 18 paths;
4. run focused `git diff --cached --check` only on newly authored governance artifacts;
5. execute exactly one commit;
6. perform read-only post-commit verification.

No `git add .`, `git add docs/`, reset, stash, clean, broad restore, amend, retry commit, push, tag, merge, rebase, or branch mutation is authorized.

## 7. Commit message

Exact intended commit message:

`docs: adopt remaining canonical PM authority evidence`

## 8. Push boundary

`PUSHED = NO`

No remote publication authority exists in this gate.

## 9. Historical-format boundary

Historical authority/evidence files are not reformatted merely to satisfy modern whitespace style. Focused diff checking applies only to newly authored governance artifacts. Existing historical bytes remain immutable.

## 10. Product/runtime boundary

This gate performs no Docker, Compose, DB, API, HTTP, PLC, V-PLC, runtime, deployment, or product-source mutation.

`FIELD-VALIDATION-COLLECTOR-DB` remains governance-isolated; its durable handoff and plan are included only because current branch authority still depends on them.

## 11. Failure semantics

If any hard gate fails before commit:

- preserve the existing staged state;
- do not reset or retry;
- terminalize HOLD with the exact reason.

If commit succeeds but a post-commit observation differs, the commit remains immutable and the variance must be reconciled in a successor gate.

## 12. Expected terminal

Successful continuation terminal:

`PASS / UNTRACKED_CORPUS_PRESERVE_PENDING_CANONICAL_ADOPTION_R2_COMMITTED`

with a new local main commit, `PUSHED=NO`, and no tracked/staged residue.
