# UNTRACKED_CORPUS_GOVERNANCE_CONTROL_CLOSEOUT

## 1. report identity

Report name: `UNTRACKED_CORPUS_GOVERNANCE_CONTROL_CLOSEOUT`

Delivery: `REPOSITORY_DURABLE_REPORT`

Exact report path: `docs/reports/untracked_corpus_governance_control_closeout_20260815T1400Z.md`

The report path must be absent, non-symlink, untracked and not ignored before first write.

## 2. task identity

Task name: `UNTRACKED_CORPUS_GOVERNANCE_CONTROL_CLOSEOUT`

This file is the sole repository-backed authority for this task:

`docs/thread_handoff/pm_task_20260815T1400Z_untracked_corpus_governance_control_closeout.md`

Before any other repository read or command, verify the launcher-provided exact path, regular/non-symlink type, bytes and SHA-256. Mismatch => `HOLD / TASK_SELF_IDENTITY_MISMATCH`.

## 3. executing Thread

Assigned core Thread: `Integration / repository-governance closeout`.

Sub-agents: `NO`.

Do not split this work into successor tasks or additional approval gates. This task already authorizes the full local closeout transaction defined below.

## 4. project/root/workload

Project absolute path:
`/Users/chenjie/Documents/MES/edge-mes-demo`

All other repository paths in this task are relative to that root. Before resolving them, prove physical cwd and `git rev-parse --show-toplevel` equal the project root.

Workload: medium, mechanically bounded.

## 5. delivery mode / exact output authority

Authorized repository writes:

- create `docs/reports/untracked_corpus_governance_control_closeout_20260815T1400Z.md`
- minimally modify `docs/current_status.md`
- retain this task file and include it in the final main commit
- update local ref `refs/heads/archive/pm-evidence-20260815`
- create/remove exact temporary index `.git/pm-governance-closeout.index`
- delete only the frozen 15-file source set after archive verification

Final main commit exact path set:

```text
docs/current_status.md
docs/reports/untracked_corpus_governance_control_closeout_20260815T1400Z.md
docs/thread_handoff/pm_task_20260815T1400Z_untracked_corpus_governance_control_closeout.md
```

Expected 3-path SHA-256 over C-locale sorted paths, one path per line with final LF:

`f681fa5a59d0619f941e7af26a628d031d70cfcd0162f938e7bb3f0e56539911`

## 6. authority source

Owner instruction: create one task Prompt so the local client Thread completes the remaining corpus-governance work end-to-end without returning for repeated micro-gates.

Authority granted in this task:

- local read-only inspection;
- local archive successor creation and verification;
- atomic local archive ref update;
- exact 15-file working-copy deletion after verified archive preservation;
- exact report/status writes;
- exact 3-path `git add`;
- one local main commit;
- post-commit verification.

Not authorized: `push`, tag, network, SSH, Docker/runtime, DB/API mutation, PLC/V-PLC, product/source/test/frontend changes, FIELD workstream changes.

## 7. required reading order

Read exactly in this order:

1. this task file, after self-identity verification;
2. `AGENTS.md`;
3. `docs/thread_handoff/pm_operating_rules.md`;
4. `.agents/skills/edge-mes-pm-governance/SKILL.md` — explicitly invoked by this task;
5. `.agents/skills/edge-mes-pm-governance/references/task-materialization-contract.md`;
6. `docs/current_status.md`;
7. `docs/thread_handoff/chatgpt_pm_handoff_260815-1654.md`;
8. `docs/reports/untracked_corpus_historical_evidence_archive_tranche_2_closeout_20260815T1332Z.md`.

Order violation => `HOLD / REQUIRED_READING_ORDER_VIOLATION`.

## 8. fresh recovery / live facts

Expected entry baseline after this task file has been materialized:

```text
branch = main
HEAD = 3f6ba2c31e33f9fecd4d8fcb5d0a6353e5e4e16d
origin/main = 6226bf3fb716880a176f9eb642b8139cef3255a6
local ahead = 4
staged = 0
tracked dirty = 0
archive ref = 64d8610e8368c2175ddf2d25fd42929fae36b9ae
archive parent = f83a4be12d767b0649a6dc268b131766ab9b1f1f
remote archive tracking ref = absent
untracked = 16
```

The 16 untracked paths must consist only of this task plus the frozen source set from Section 10.

Exact report path must still be absent. Temporary index must be absent.

Any real drift in HEAD, origin, archive ref, staged/dirty state or frozen source identity => HOLD; do not normalize the baseline to the new state.

## 9. current gate / authority boundary

Already established and not reopened here:

- canonical continuity adoption completed;
- archive tranche 1 and tranche 2 completed locally;
- project-local Codex tooling adopted;
- `frontend/next-env.d.ts` hygiene committed;
- exact duplicate cleanup completed;
- remaining untracked debt before this task = 15 corpus-governance intermediate controls only.

Product/runtime truth is unchanged. In particular:

```text
P1_G6_PM_ACCEPTANCE = REMAINS CLOSED / PASS
REMOTE_G5_PRODUCTION_ACCEPTANCE = UNCHANGED
A1_S2 = NOT AUTHORIZED
FIELD-VALIDATION-COLLECTOR-DB = GOVERNANCE-ISOLATED
```

## 10. exact task scope / execution

### A. Freeze the 15-file source set

Define `SOURCE_SET` mechanically as:

`all current untracked paths minus this exact task path`.

Before any mutation, `SOURCE_SET` must satisfy all of:

```text
COUNT = 15
TOTAL_BYTES = 92059
PATHSET_SHA256 = 2c671eac5448ed36d2a03d08783f5aa0f09577144e0f530474708cb948a81aa1
RECORDSET_SHA256 = f39c9295126033114ff1f3ef7682f133917c4ae75206e58ae15130a2e869993e
```

Hash schemas:

- pathset: C-locale sorted UTF-8 paths, one per line, final LF;
- recordset: same path order, each line `path<TAB>bytes<TAB>sha256`, final LF.

Every source must be regular, non-symlink, untracked and not indexed.

### B. Create archive tranche 3 without touching main index

Use only Git plumbing and the exact temporary index `.git/pm-governance-closeout.index`.

1. Seed temporary index from archive commit `64d8610e8368c2175ddf2d25fd42929fae36b9ae`.
2. Add exactly `SOURCE_SET` into the temporary index with their live file mode/blob identities.
3. Write tree and create one successor commit with parent exactly `64d8610e8368c2175ddf2d25fd42929fae36b9ae` and subject:
   `archive: preserve corpus governance controls`
4. Before moving the ref, verify `old_archive..candidate` contains exactly 15 paths with the frozen pathset, and verify every candidate tree blob bytes/SHA against the frozen source recordset.
5. Atomically update only `refs/heads/archive/pm-evidence-20260815` using old-value compare-and-swap from `64d8610e...` to the candidate.
6. Re-read the ref and parent; both must match.

No checkout/switch/merge/rebase is authorized.

### C. Delete exact working copies

Only after Section B succeeds, reverify all 15 source files against the frozen recordset, then delete exactly those 15 working copies.

After deletion, untracked must equal exactly one path: this task file.

### D. Minimal current-status sync

Modify only `docs/current_status.md` by inserting one new highest-priority repository-governance block immediately before existing `## 0Q`.

Use heading `## 0R. 2026-08-15 Untracked Corpus Governance Closeout`.

The block must record, concisely:

- historical corpus reconciliation is closed locally;
- archive branch and new tranche-3 commit + parent;
- tranche 1 = 516, tranche 2 = 645, tranche 3 = 15;
- main pre-closeout HEAD = `3f6ba2c...`;
- no push performed;
- repository hygiene target after final commit = staged 0 / tracked dirty 0 / untracked 0;
- product/runtime/remote acceptance boundaries remain unchanged;
- FIELD branch remains isolated.

Do not rewrite older status blocks.

### E. Write durable closeout report

Create the exact report path from Section 1. It must include:

- terminal claim target;
- authority and entry baseline;
- frozen 15-file identities;
- archive old/new commit and verification;
- working-copy removal result;
- `current_status.md` change summary;
- final 3-path main allowlist and checks;
- no-push / no-runtime / no-product-mutation boundaries.

### F. Exact main commit

Before staging:

- main HEAD must still equal `3f6ba2c31e33f9fecd4d8fcb5d0a6353e5e4e16d`;
- origin/main unchanged;
- archive ref must equal the newly verified tranche-3 commit;
- tracked diff must contain only `docs/current_status.md`;
- untracked must contain exactly task + report;
- `git diff --check` must pass.

Then stage exactly the 3 paths from Section 5 and verify cached pathset equals `f681fa5a...` and `git diff --cached --check` passes.

Create exactly one main commit with subject:

`docs: close untracked corpus governance controls`

### G. Final verification

PASS requires all of:

```text
main parent = 3f6ba2c31e33f9fecd4d8fcb5d0a6353e5e4e16d
main commit changed paths = exact 3-path allowlist
origin/main = 6226bf3fb716880a176f9eb642b8139cef3255a6
staged = 0
tracked dirty = 0
untracked = 0
archive new parent = 64d8610e8368c2175ddf2d25fd42929fae36b9ae
archive old..new paths = exact frozen 15
archive blobs reconstruct frozen 15 recordset exactly
remote archive tracking = absent
PUSHED = NO
```

## 11. exact allowlist / budgets

Reads: task-required governance docs, Git metadata, exact source set, and files required to hash/verify the authorized transaction.

Writes: only surfaces in Section 5 plus exact deletion of `SOURCE_SET`.

Git mutation budgets:

- temporary-index archive build: 1;
- archive commit-tree: 1;
- archive ref update: 1;
- main exact stage: 1;
- main commit: 1;
- push/tag: 0.

Retry/repair budget after first mutation: `0` except cleanup of the exact temporary index file after a pre-ref-update failure. Do not invent successor attempts.

Host Python: `NOT AUTHORIZED / NOT REQUIRED`. Use Git/shell plumbing only; do not introduce a Python control-plane dependency.

Network/SSH/DB/API/runtime/PLC budgets: all `0`.

## 12. explicitly forbidden

Forbidden:

- `git add .`, `git add -A`, directory-wide stage;
- `git clean`, broad `rm`, reset, stash, restore of unrelated paths;
- checkout/switch/merge/rebase/cherry-pick;
- push/tag/fetch/pull;
- rewriting historical PASS/HOLD or archived blobs;
- product/source/test/frontend/runtime changes;
- creating extra task/report/helper/manifest/script files;
- changing the 15-file source set or final 3-path allowlist to make checks pass.

## 13. PASS / HOLD / stop criteria

PASS terminal:

`PASS / UNTRACKED_CORPUS_GOVERNANCE_CONTROL_CLOSEOUT_COMPLETE`

HOLD immediately on first real identity drift, allowlist violation, archive verification failure, delete failure, report/status write escape, staged-path mismatch, commit failure or final-state mismatch.

If archive ref has already advanced before a later HOLD, preserve that fact; do not roll it back unless separately authorized.

If main commit has already succeeded before a later verification HOLD, do not reset/amend/retry.

## 14. required validation / evidence

Required evidence:

- task self identity;
- root and Git baseline;
- frozen source count/bytes/pathset/recordset;
- archive candidate parent/pathset/blob verification;
- exact cleanup count;
- report identity;
- status diff containment;
- final cached allowlist/pathset;
- post-commit parent/changed-paths/staged/dirty/untracked;
- archive continuity and no remote tracking ref.

This is local repository evidence only; it must not be promoted to runtime/production evidence.

## 15. window manifest

Return a concise manifest only:

```text
TERMINAL = <PASS/HOLD>
MAIN_COMMIT = <sha or NO>
ARCHIVE_TRANCHE3_COMMIT = <sha or NO>
ARCHIVED_FILES = <n>
REMOVED_WORKING_COPIES = <n>
FINAL_STAGED = <n>
FINAL_TRACKED_DIRTY = <n>
FINAL_UNTRACKED = <n>
ORIGIN_MAIN = <sha>
PUSHED = NO
REPORT = <path / bytes / sha256>
```

Include blocker only on HOLD. Do not paste full report into chat.

## 16. next gate / non-inheritance

On PASS, this corpus-governance cleanup workstream is locally closed. There is **no additional corpus micro-gate**.

Return control to Mainline PM for normal product prioritization / handoff decisions.

This task grants no push, deploy, runtime, DB, PLC, A1-S2 or FIELD authority after terminalization.
