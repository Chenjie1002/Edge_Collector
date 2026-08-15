# Sprint 4 D2-R7B-I1 R66 One-Shot Minimal Exact-Commit Local Collector Build/Image Acceptance Execution Report

## Conclusion

`HOLD / LOCAL_MATERIALIZATION_INVENTORY_FAILURE`

R66 authority was consumed at exclusive creation of the declared attempt and evidence roots. No Docker command was executed. The attempt must not be repaired, retried, reused, or cleaned up.

## Failure record

The exact materialization phase created the task-owned roots and generated the declared source and mapping archives from product commit `934ced7b9659cb566628b1709cf6d73463a534d8`. During construction of the required exact Git-tree ordinary-file inventory, the executor encountered:

```text
RuntimeError: nonordinary git tree item collector/app
```

This occurred at `git_tree_ordinary_file_inventory`: the directory path was observed as a Git tree entry, rather than an ordinary file. Consequently the required Git-tree/archive/extracted three-way ordinary-file comparison and materialization lock were not established.

The failure arose after the first task-owned write. Per the frozen one-shot boundary, no correction of the inventory procedure, second archive, re-extraction, retry, cleanup, reuse, Docker call, or dependent terminal was performed.

## Durable evidence

- Attempt ID: `d2-r7b-i1-r66-934ced7-a1`
- Attempt root: `/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1` — task-owned partial attempt; retained without cleanup.
- Evidence root: `docs/reports/evidence/d2_r7b_i1_r66_exact_commit_collector_local_build_image_acceptance`
- Published terminal: `01_source_materialization_terminal.json` — `HOLD`
- Terminals 02–10: not executed and not published.

The expected exact source commit was `934ced7b9659cb566628b1709cf6d73463a534d8`; the mapping authority was `config/mapping.yaml`, `7112` bytes, SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`. These facts do not cure the missing materialization lock.

## Docker and phase audit

```text
Docker calls / network-capable / daemon-mutating = 0 / 0 / 0
Builds / validation containers / probes          = 0 / 0 / 0
Candidate full ID                                = NOT OBSERVED
Selected immutable base                          = NOT OBSERVED
Source closure / dependency pins / Config        = NOT EXECUTED
RootFS / isolated validation                     = NOT EXECUTED
Remote / Git mutation                            = 0 / 0
```

The pre-write recovery had passed: `HEAD = origin/main = 0e7544a12b00799780d76723ca0de781bc2e8ad7`, tracked and cached diffs were empty, and untracked membership was `335 / 335 / 0 / 0 / 0`. The post-failure report is untracked and no Git staging, commit, push, or tag occurred.

## Status and next gate

```text
R66 EXECUTED             = NO
LOCAL CANDIDATE BUILT    = NO
LOCAL IMAGE ACCEPTED     = NO
PM ACCEPTED              = NO
ARCHIVED                 = NO
TRANSPORTED              = NO
REMOTE LOADED            = NO
DEPLOYED                 = NO
ACTIVATED BY 934ced7     = NO
RUNTIME-LOADED           = NO
PRODUCTION-ACCEPTED      = NO
```

MVP alignment is `MVP-ALIGNED`: the stopped work was limited to the approved local candidate materialization gate and introduced no product, remote, runtime, or production claim.

The only next gate is `R66 execution package WRITTEN -> ChatGPT PM durable intake only`. A future attempt requires a new authority, new attempt ID, new roots, and fresh recovery; it must not reuse this partial attempt.
