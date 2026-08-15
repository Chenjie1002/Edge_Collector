# Sprint 4 D2-R7B-I1 R30-I1-R4-R1 Focused Reliability Cleanup-Boundary Re-review

## 1. Executive conclusion

```text
conclusion: HOLD
classification: RELIABILITY_HOLD
review scope: REL-R30-B5 only
P2-R2 rerun: no
P2-R3: exactly once; E1-E50 PASS 50/50
package modification: 0
Git / network / SSH / remote: 0 / 0 / 0 / 0
```

`REL-R30-B5` and `REL-R30-CLEANUP-001` remain OPEN. The persisted P2-R3
matrix passed, but the required pre-delete cleanup validation failed before any
deletion because the bounded validator used `/tmp` as its temporary-tree base;
the current macOS test roots are under `/private/var/folders/.../T`. Per the
authority, the validator was not repaired or rerun, P2-R3 was not rerun, and no
cleanup mutation occurred. This report is the single durable output.

No source, test, manifest, helper, postflight, mapping, status, roadmap,
handoff, Git or remote surface was modified.

## 2. Scope and accepted prior evidence

This was a new Reliability Thread and a focused rereview of the single open
finding from R30-I1-R4. The following prior evidence was accepted and not
replayed:

- P2-R2 `37/37 PASS`, T18 PASS and T19 PASS with `ordinary_env=True` and
  `cache_equal=True`;
- R30-I1-R4 findings B1-B4 and B6-B10 closed;
- R30-I1-R4 `REL-R30-B5 / REL-R30-CLEANUP-001` open;
- R30-R2 superseded, void and not used.

The P2-R2 matrix was not invoked by this task. The only test command run was:

```text
python3 docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py
```

## 3. Fresh baseline

```text
project root: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 63d3cc70e787e0c837079aec0f5924dcbfa6a668
origin/main: 63d3cc70e787e0c837079aec0f5924dcbfa6a668
ahead/behind: 0/0
cached: empty
git diff --check: PASS
git diff --cached --check: PASS
mapping relative to HEAD: clean
mapping HEAD blob: b46a637f23c761d0a4c3fe048b3b7480a3dec2ce
mapping bytes / SHA-256: 7112 / d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
initial untracked count: 13765
initial untracked SHA-256: 71a323d2b2317d93a193f71bd088cd0e7bb35543b4402c78523eb6f746fb806f
ordinary environment: PYTHONDONTWRITEBYTECODE absent; PYTHONPYCACHEPREFIX absent
ordinary Python: dont_write_bytecode=False; pycache_prefix=None
scoped cache: P2-R2 0 __pycache__ / 0 *.pyc; P2-R3 0 __pycache__ / 0 *.pyc
task-owned process count: 0
report path before write: ABSENT / NON-SYMLINK
```

Pre-existing tracked dirty paths were preserved and were not created by this
task:

```text
.gitignore
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
docs/thread_handoff/pm_operating_rules.md
```

## 4. Frozen identity set

All identities matched the task authority before P2-R3 and in the post-test
read-only audit:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh` | 2653 | `943d44916af0b556bed0ca4c44cf309cba9fe10e62ff50f531e21bd68a486a7b` |
| `docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256` | 528 | `f9dd9d8a3e49624dbdb1f8473e295371aeb90b51c2874adfac4aea757cd74749` |
| `docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py` | 67695 | `aa40fa64d8d9cc8508a6e0c480714778381bb2e13c21ffa14bd553205f3e9183` |
| `docs/reports/evidence/d2_r7b_p2_r2/remote_preflight.py` | 11129 | `6ddae658ed30ba38c20dcd3fa29fa9719cb940f3c8da4b904c6dfae810061f9c` |
| `docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py` | 10563 | `30a02e5bc63545b08b1536e59abc418685cf846fbe2c930847d1f1b983f5ae7b` |
| `docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py` | 15483 | `657498d42906c260ad12d53c16044a6a272cd1bea1a60ebfd2538b178baf02ff` |
| `docs/reports/evidence/d2_r7b_p2_r2/remote_rollback.py` | 13248 | `e2690ef991827ad8107430ee0449be913afa65dbf166fe2c1cf19fec0b7736ff` |
| `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py` | 63505 | `28d4b910df01d73c8d4d05264a9d63df1efc7751f1afb85f5f663491a396f0a4` |
| `docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py` | 15456 | `b26051aa1fcbb71b84a16173f3c393542bd6c94bc24e619e4ebfb12c4d60d5ee` |
| `docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py` | 102372 | `f19f4d0f19e6e21bfeb51931fa903cbf84eee107922be817ace9090050a5414c` |
| `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256` | 1122 | `ae35c26d0709bf8b6c1ac500528e67b15f45393d8a782db0e2e3d6994a12a733` |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` |

Manifest validation remained `P2-R2 6/6 OK` and `P2-R3 9/9 OK`. The old
full commit pin occurred zero times and the current full pin occurred twice in
the two evidence trees.

## 5. P2-R3 evidence

Execution window:

```text
start: 2026-07-28T12:38:17Z / 1785242297
end: 2026-07-28T12:38:53Z / 1785242333
execution count: 1
exit: 0
matrix: E1-E50 PASS 50/50
E39: PASS — persisted loader fixture success/failure sys.modules transaction
E40: PASS — ordinary environment and repository cache unchanged
```

The test persisted loader contract used source bytes plus `compile(...,
"exec")` and a `sys.modules` transaction. It emitted only these candidate
paths:

```text
SYNTHETIC_ROOT=/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r3-y4tz28jg
LOCAL_STAGE_PARENT=/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r3-y4tz28jg/local-stage-parent
RETAINED_ROOT=/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r3-y4tz28jg
RETAINED_ROOT=/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2_r7b_p2_r3_e39kq3_dmrm
```

## 6. Candidate relation and cleanup boundary

Canonicalization and path-component relation analysis identified three unique
realpaths. `SYNTHETIC_ROOT` and its duplicate `RETAINED_ROOT` share one
realpath. `LOCAL_STAGE_PARENT` is a strict descendant of that path. The E39
retained root is independent.

| Label | Original path | Realpath | Relation | Intended outer root | Actual deletion target |
| --- | --- | --- | --- | --- | --- |
| `SYNTHETIC_ROOT` | `.../d2-r7b-p2-r3-y4tz28jg` | same | root candidate | yes | none; cleanup stopped |
| `LOCAL_STAGE_PARENT` | `.../d2-r7b-p2-r3-y4tz28jg/local-stage-parent` | same | strict descendant of synthetic root | no | no |
| `RETAINED_ROOT` duplicate | `.../d2-r7b-p2-r3-y4tz28jg` | same as synthetic root | realpath duplicate | deduplicated | no additional call |
| `RETAINED_ROOT` E39 | `.../d2_r7b_p2_r3_e39kq3_dmrm` | same | independent root candidate | yes | none; cleanup stopped |

Read-only post-failure lstat confirmed all four stdout lines still resolve to
present non-symlink directories. The observed identities were:

```text
synthetic outer: dev=16777234 inode=11887612 uid=501 gid=20 mode=0700
local stage parent: dev=16777234 inode=11887613 uid=501 gid=20 mode=0755
E39 outer: dev=16777234 inode=11887935 uid=501 gid=20 mode=0700
```

The intended outer-root cardinality was two: one `d2-r7b-p2-r3` root and one
`d2_r7b_p2_r3` root. However, the deletion set was not frozen for mutation.
The pre-delete validation stopped on the temporary-tree check before recursive
entry validation. No `shutil.rmtree` call, descendant deletion, symlink follow,
or other cleanup mutation occurred.

The exact blocker was:

```text
pre-delete validator result: FAIL
failed gate: system temporary tree containment
validator assumption: fixed /tmp root
live candidate tree: /private/var/folders/.../T
mutation count: 0
validator repair/retry: prohibited and not performed
```

Because the gate stopped before recursive traversal, the descendant inventory
was not completed. Symlink follow count is `0` because no traversal or
symlink-follow operation occurred; the current test's symlink-child allowance
was not converted into a cleanup PASS.

## 7. Cleanup evidence and stop state

```text
deletion set frozen before mutation: no; pre-delete gate failed
actual outer-root deletion calls: 0
per-root mutation count: 0
descendant deletion calls: 0
symlink follow count: 0
actual deletion failures: 0
cleanup validation failures: 1
remaining stdout lines: 4 PRESENT
remaining unique canonical paths: 3 PRESENT
```

This is a fail-closed stop, not a successful cleanup. No retry, alternate
environment, validator repair, second P2-R3 run, prefix scan, temporary-parent
cleanup or historical-root cleanup was performed.

## 8. Reliability finding closure

```text
REL-R30-B5: OPEN
REL-R30-CLEANUP-001: OPEN
Critical findings: 0
Important findings: 1
Minor findings: 0
```

The existing Important finding remains open because the focused task did not
establish a compliant deletion procedure. The failed pre-delete validator is
the exact blocker for this attempt; it did not mutate a repository, foreign
object or retained historical root.

## 9. Post-test audit

```text
scoped cache before/after: 0 __pycache__ / 0 *.pyc; unchanged
package/test/helper/postflight/mapping identities: unchanged / PASS
P2-R2 manifest after test: 6/6 OK
P2-R3 manifest after test: 9/9 OK
HEAD/origin/ahead-behind: unchanged / 63d3cc70... / 63d3cc70... / 0/0
cached index: empty
tracked dirty set: unchanged six pre-existing paths
task-owned process after stop: 0
network / SSH / remote: 0 / 0 / 0
```

The post-test untracked set before this report write remained exactly the
initial set: 13765 paths with SHA-256
`71a323d2b2317d93a193f71bd088cd0e7bb35543b4402c78523eb6f746fb806f`.

## 10. Evidence classification

Accepted for this focused Reliability gate:

- live local Git and filesystem facts;
- frozen persisted package, test, helper and manifest identities;
- ordinary-environment P2-R3 local/synthetic matrix evidence;
- stdout-only candidate relation evidence up to the failed pre-delete gate;
- no-mutation and unchanged repository audit.

Not established:

- compliant outer-root cleanup;
- remote deployment or fresh remote eligibility;
- runtime config load;
- Collector activation or restart;
- production acceptance;
- any remote mutation or remote state after this review.

## 11. MVP alignment and Thread context

```text
current MVP support: exact local D2-R7B config-deployment safety boundary
minimum invariant: exact package identity and fail-closed external cleanup
scope expansion: none
task inflation: none
classification: MVP-ALIGNED / LOCAL-ONLY RELIABILITY HOLD
本次输出长度: 长 durable HOLD report；Chat 返回 concise manifest
当前 Thread 是否建议继续: no
下一轮是否建议新开 Thread: yes
理由: cleanup-boundary validation failed before mutation; any validator repair or cleanup decision requires fresh PM authority and a new Reliability boundary
```

## 12. Delivery and next gate

```text
delivery state: WRITTEN only
immediate next gate: RELIABILITY-HOLD / WRITTEN -> ChatGPT PM durable intake
```

PM intake 后，如需继续，必须由新的明确 authority 处置 cleanup-boundary
validator/contract问题并重新建立独立 Reliability review。不得在本报告基础上
恢复 R30-R2，也不得自动进入 Verification、Git、fresh remote eligibility、SSH、
upload、deployment、rollback、restart、activation、runtime-loaded validation 或
production acceptance。

