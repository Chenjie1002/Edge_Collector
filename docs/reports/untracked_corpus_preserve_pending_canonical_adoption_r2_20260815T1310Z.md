# UNTRACKED_CORPUS_PRESERVE_PENDING_CANONICAL_ADOPTION_R2 — Continuation Reconciliation

## Terminal

`PASS / CANONICAL_ADOPTION_R2_CONTINUATION_READY_FOR_OWNER_TERMINAL`

This report certifies only the pre-commit continuation state. It does not claim that the R2 commit has already occurred.

## Historical predecessor terminal

Immutable predecessor terminal:

`HOLD / CANONICAL_ADOPTION_STAGED_ALLOWLIST_MISMATCH`

The predecessor successfully staged 16 paths, then stopped before B1/B2 because its staged-path hash used default Git `core.quotePath` display output.

The HOLD remains historical and is not rewritten.

## False-mismatch diagnosis

The predecessor expected staged pathset SHA-256:

`a4468cfe09b142d9fe83ce2b3b8c55e22ee672ce59abc63735a0696fa70ead15`

Default `git diff --cached --name-only` returned the Unicode path:

`docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`

as a C-style quoted display string. Hashing that display produced:

`1e6c280a8e5aa3e9cd8bc1d0db75f96411c823b6ee73daa17df346247e796fb2`

Using authority-safe unquoted path output:

`git -c core.quotePath=false diff --cached --name-only`

produced:

`a4468cfe09b142d9fe83ce2b3b8c55e22ee672ce59abc63735a0696fa70ead15`

which exactly matches the frozen 16-path allowlist.

Classification:

```text
FALSE_MISMATCH = YES
CAUSE = GIT_QUOTEPATH_DISPLAY_ENCODING
STAGED_ALLOWLIST_ACTUALLY_MATCHES = YES
UNAUTHORIZED_STAGE = NO
RESTAGE_REQUIRED = NO
RESET_REQUIRED = NO
```

## R2 entry state

Mechanically observed before R2 control-artifact creation:

```text
HEAD = 8bf994c60ffa6dd9bd082c5d9d40bbfbf8041239
origin/main = 6226bf3fb716880a176f9eb642b8139cef3255a6
staged count = 16
staged unquoted pathset SHA-256 = a4468cfe09b142d9fe83ce2b3b8c55e22ee672ce59abc63735a0696fa70ead15
unstaged tracked count = 0
untracked count = 665
```

The 16 staged paths are retained unchanged.

## Adopted authority set represented by existing stage

The existing stage contains exactly:

- 13 `KEEP_ON_MAIN_CANDIDATE` authority-continuity files from the semantic reconciliation;
- predecessor canonical-adoption task;
- predecessor 13-row adoption manifest;
- predecessor adoption report.

The 13 keep files remain frozen as:

```text
count = 13
bytes = 188368
pathset SHA-256 = 3d583f050d8f1e094980613c64bae4c5caaffaa2c793774bd20e0048e77d28e6
semantic recordset SHA-256 = e5c7cc1601924edc5b9e2da185ab5673bfd2d9bdc04c404e1929b26cc2940d4d
```

They include current G5 continuity evidence, the predecessor mainline handoff needed by the latest tracked handoff, and the still-active `FIELD-VALIDATION-COLLECTOR-DB` branch handoff/plan dependency chain.

## R2 continuation scope

R2 creates exactly two new governance artifacts:

- `docs/thread_handoff/pm_task_20260815T1310Z_untracked_corpus_preserve_pending_canonical_adoption_r2.md`
- `docs/reports/untracked_corpus_preserve_pending_canonical_adoption_r2_20260815T1310Z.md`

The Owner Terminal continuation may stage only these two paths in addition to the already-staged 16.

The final stage must therefore contain exactly 18 paths and must be identified using `core.quotePath=false`.

## Non-authority and exclusions

R2 does not touch:

- the 645 semantic tranche-2 archive candidates;
- existing local archive branch `archive/pm-evidence-20260815`;
- `.codex/**` or `AGENTS.md`;
- `frontend/next-env.d.ts`;
- the single exact duplicate `docs/reports/evidence/d2_r7b_i1_r67_r3_existing_candidate_validation_only_acceptance/input/config/mapping.yaml`;
- Docker/runtime/DB/API/PLC state;
- remote Git refs.

No push authority is granted.

## Historical formatting

The previously staged historical files may contain historical Markdown whitespace. Their bytes are immutable. Focused whitespace validation is limited to newly authored governance artifacts rather than rewriting historical evidence.

## Commit expectation

Single authorized commit message:

`docs: adopt remaining canonical PM authority evidence`

Expected successful terminal after independent post-commit verification:

`PASS / UNTRACKED_CORPUS_PRESERVE_PENDING_CANONICAL_ADOPTION_R2_COMMITTED`

`PUSHED=NO` remains mandatory.
