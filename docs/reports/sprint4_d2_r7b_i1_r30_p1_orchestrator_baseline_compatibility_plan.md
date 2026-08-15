# Sprint 4 D2-R7B-I1 R30-P1 Orchestrator Baseline Compatibility Plan

## 1. Executive conclusion

```text
planning result: PASS
root cause: STALE_LOCAL_BASELINE_PIN
implementation performed: no
tests executed: no
remote execution performed: no
network / SSH / remote: 0 / 0 / 0
Git mutation: 0
delivery state established by this report: WRITTEN only
```

The accepted local execution package is payload-compatible with the current
checkout. The compatibility gap is the exact Git commit pin in two persisted
local execution sources: both still require `8de5edbb504538a233abbcc80102cb714c9cee65`,
while the current accepted checkout is `63d3cc70e787e0c837079aec0f5924dcbfa6a668`.

The mapping blob, bytes and SHA-256 are unchanged. The minimum future repair is
two literal `EXPECTED_COMMIT` updates plus the two required manifest cascades.
Remote helpers, tests, remote artifact basenames, rollback namespace and
historical evidence remain frozen. This report plans the repair; it does not
implement or accept it.

## 2. Task, authority and scope

```text
task: D2-R7B-I1 R30-P1 — Plan Local-Only Orchestrator Baseline Compatibility Repair
executing Thread: Architecture / Integration
report delivery mode: REPOSITORY_DURABLE_REPORT / PLANNING ONLY
exact writable path: docs/reports/sprint4_d2_r7b_i1_r30_p1_orchestrator_baseline_compatibility_plan.md
artifact paths: none
authority: AUTHORIZED ONCE / LOCAL-ONLY PLANNING / READ-ONLY SOURCE ANALYSIS
source/test/manifest writes during this task: 0
Git / network / SSH / remote authority: not authorized
```

The first write of this report consumes the one-shot planning authority. No
retry or second report write is permitted. The report does not establish
`IMPLEMENTED`, `TESTED`, `RELIABILITY-ACCEPTED`, `VERIFICATION-ACCEPTED`,
`STAGED`, `COMMITTED`, `PUSHED`, `REMOTE-ELIGIBLE`, `DEPLOYED`,
`ACTIVATED` or `PRODUCTION-ACCEPTED`.

## 3. Required reading and evidence boundary

The specified PM Rules Sections 9, 10 and 11 were read before and Sections 10
and 11 were read again after the required repository reading. The specified
handoff, status, roadmap, R26–R29 reports, P2-R2/P2-R3 source, test and
manifest files, and `config/mapping.yaml` were read from the checkout.

Historical reports are context, not a substitute for current source bytes.
Where a historical report describes a prior source identity, the current
persisted source and its current manifest entry are authoritative for this
planning decision.

## 4. Fresh local baseline

Fresh read-only recovery from `/Users/chenjie/Documents/MES/edge-mes-demo`
returned:

| Check | Observed result |
| --- | --- |
| checkout root | `/Users/chenjie/Documents/MES/edge-mes-demo` |
| branch | `main` |
| `HEAD` | `63d3cc70e787e0c837079aec0f5924dcbfa6a668` |
| `origin/main` | `63d3cc70e787e0c837079aec0f5924dcbfa6a668` |
| ahead / behind | `0 / 0` |
| `HEAD` parent | `5fe72282d1b1bcbf602712982e814ef488368122` |
| `HEAD` subject | `Close D2-R7B R29 observation and cleanup documentation` |
| `HEAD` path count | `8` |
| cached index | empty |
| `git diff --check` | PASS |
| `git diff --cached --check` | PASS |
| tracked dirty | `.gitignore`; `docs/thread_handoff/pm_operating_rules.md` |
| mapping worktree | clean relative to `HEAD` |
| report path before write | ABSENT / NON-SYMLINK |
| `docs/reports` | regular directory, non-symlink, realpath exact |
| task-owned process count | `0` |

The checkout also contains a broad pre-existing untracked set of historical
reports/evidence/handoffs and frontend artifacts. It was preserved and is not
part of this report's write set. No untracked path was staged, cleaned,
reclassified or modified.

The exact mapping identity is:

```text
path: config/mapping.yaml
bytes: 7112
SHA-256: d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
HEAD blob: b46a637f23c761d0a4c3fe048b3b7480a3dec2ce
```

This is the expected current mapping identity. It is equal to the accepted
old package payload identity; the payload did not drift.

## 5. Current persisted package identities

The six required identities were measured from the current checkout before
the report write:

| Path | Bytes | SHA-256 | Full old commit pin | Planned disposition |
| --- | ---: | --- | --- | --- |
| `docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh` | 2653 | `e5daa5483ef012c4528875878c1f41ba894409694b38d683a742306bbf76ba31` | yes, line 8 | MODIFY one literal pin |
| `docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py` | 67695 | `aa40fa64d8d9cc8508a6e0c480714778381bb2e13c21ffa14bd553205f3e9183` | no | KEEP |
| `docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256` | 528 | `2ae13bd6dc17167f98d2d59efd882e8a568d5c0ae6f36cbbb9ecb6f2d21086dd` | no | MODIFY identity entry after source finalization |
| `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py` | 63505 | `daa4b5056aeacdaf3781c3ccd6c7306dd728876d334ab59af244ebd35f08ee64` | yes, line 28 | MODIFY one literal pin |
| `docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py` | 102372 | `f19f4d0f19e6e21bfeb51931fa903cbf84eee107922be817ace9090050a5414c` | no | KEEP |
| `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256` | 1122 | `8e5e99f5e52e87a6945b692ca8808b518e6cd360c84191f08aa9bf1d992f95c8` | no | MODIFY identity entries after source finalization |

The current P2-R2 manifest binds the current helper identities, including
`remote_preflight.py` `11129` bytes / `6ddae658...`,
`remote_upload_exclusive.py` `10563` bytes / `30a02e5b...`,
`remote_deploy.py` `15483` bytes / `657498d4...`, and
`remote_rollback.py` `13248` bytes / `e2690ef9...`. The current P2-R3
manifest additionally binds `remote_postflight.py` `15456` bytes /
`b26051aa...`. These current entries are consistent with the current manifest
files; historical report snapshots with other source hashes are not a reason
to broaden this plan.

## 6. Root-cause classification

The source contracts separate five identities:

| Contract | Current evidence | Classification |
| --- | --- | --- |
| A. Local checkout baseline pin | `local_materialization.sh:8` and `remote_i1_orchestrator.py:28` require `8de5edb...`; live `HEAD` is `63d3cc70...` | `STALE_LOCAL_BASELINE_PIN` |
| B. Mapping payload identity | current blob `b46a...`, 7112 bytes and SHA `d9bb...` match all accepted payload constants | unchanged payload |
| C. Remote transaction artifact namespace | sidecar, backup and rollback names use short `8de5edb` label | frozen remote namespace |
| D. Historical evidence identity | R26/R28/R29 evidence preserves prior baseline and cleanup facts | historical identity; do not rewrite |
| E. Manifest-bound package identity | P2-R2 has 6 entries; P2-R3 has 9 entries, each hash-binding persisted source bytes | cascaded package identity |

The root cause is therefore not mapping content drift, remote target drift,
Collector drift, helper semantic failure, deployment failure or runtime
failure. The orchestrator's local source gate rejects the checkout before any
SSH child can start because the exact commit pin is stale.

## 7. Exact old-commit and short-label occurrence map

An exact search of the two evidence directories found exactly two full old
commit occurrences:

```text
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh:8
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py:28
```

No full `8de5edbb504538a233abbcc80102cb714c9cee65` occurrence exists in the
two tests, either manifest, the five remote helpers or `remote_postflight.py`
within the scanned package evidence tree.

The short `8de5edb` label has a different meaning and occurs as follows:

| Occurrence group | Paths | Meaning |
| --- | --- | --- |
| Remote upload/backup/rollback namespace | `remote_preflight.py`, `remote_upload_exclusive.py`, `remote_deploy.py`, `remote_rollback.py`, `remote_postflight.py`, `remote_i1_orchestrator.py` | exact remote artifact basenames; not a checkout baseline pin |
| P2-R2 synthetic fixtures and cleanup assertions | `test_d2_r7b_contract.py` | historical/frozen sidecar fixture names used to test stale, retained and rollback states |
| P2-R3 synthetic remote fixture | `test_d2_r7b_execution_contract.py` | path-contract fixture names used for phase and postflight tests |
| Accepted historical reports | R26–R29 reports and related evidence | historical execution/cleanup identity; not a source repair target |

The three frozen remote names are:

```text
/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-new.8de5edb
/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml
/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml
```

## 8. Minimum implementation candidate set

The future R30-I1 writable set should be exactly four paths:

| Path | Decision | Minimum intended change | Manifest consequence | Test consequence | Review owner |
| --- | --- | --- | --- | --- | --- |
| `docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh` | MODIFY | `EXPECTED_COMMIT=8de5edbb...` → `EXPECTED_COMMIT=63d3cc70e787e0c837079aec0f5924dcbfa6a668` | update P2-R2 entry and then P2-R3 entry | existing materializer/local-gate tests run; no source change | Architecture / Integration |
| `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py` | MODIFY | `EXPECTED_COMMIT = "8de5edbb..."` → `EXPECTED_COMMIT = "63d3cc70..."` | update P2-R3 entry | existing baseline/local-source and synthetic phase tests run; no source change | Architecture / Integration |
| `docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256` | MODIFY | regenerate one changed source digest; preserve six paths | exact 6 paths, sorted, unique, self-excluded | no test edit | Architecture / Integration + Verification |
| `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256` | MODIFY | regenerate changed local materializer and orchestrator digests | exact 9 paths, sorted, unique, self-excluded | no test edit | Architecture / Integration + Verification |

The following files are explicitly kept unchanged:

```text
docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py
docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py
docs/reports/evidence/d2_r7b_p2_r2/remote_preflight.py
docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py
docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py
docs/reports/evidence/d2_r7b_p2_r2/remote_rollback.py
docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py
config/mapping.yaml
```

The remote helpers have no full commit pin. Their direct contracts remain
payload, target, filesystem, ownership, artifact-path, postflight and
rollback contracts. No source evidence requires changing them for this
baseline-only repair.

## 9. Baseline update design

The intended source diff is limited to these two assignments:

```text
local_materialization.sh:
EXPECTED_COMMIT=8de5edbb504538a233abbcc80102cb714c9cee65
→ EXPECTED_COMMIT=63d3cc70e787e0c837079aec0f5924dcbfa6a668

remote_i1_orchestrator.py:
EXPECTED_COMMIT = "8de5edbb504538a233abbcc80102cb714c9cee65"
→ EXPECTED_COMMIT = "63d3cc70e787e0c837079aec0f5924dcbfa6a668"
```

All of the following remain unchanged:

```text
EXPECTED_BRANCH = main
EXPECTED_BLOB = b46a637f23c761d0a4c3fe048b3b7480a3dec2ce
EXPECTED_NEW_BYTES = 7112
EXPECTED_NEW_SHA256 = d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
EXPECTED_OLD_BYTES = 5935
EXPECTED_OLD_SHA256 = 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3
CONFIRMATION_TOKEN = D2-R7B-I1-CONFIG-ONLY
TRANSPORT_ENDPOINT = mari@10.0.0.217
Collector hostname/principal/image/container/mount/restart identity
```

Do not replace the exact pin with an environment override, old worktree,
detached HEAD, reset/checkout, dynamic “accept any HEAD”, mapping-only hash
acceptance or direct helper calls. Those alternatives either bypass the
baseline contract or create a different execution surface.

## 10. Manifest update plan

The manifest cascade is mandatory because source identity is part of the
accepted package identity:

1. Establish final source/test bytes. Only the two source files above change;
   both tests and all remote helpers remain byte-identical.
2. Regenerate and verify the P2-R2 manifest. Its path set remains six
   directory-relative entries; only the `local_materialization.sh` digest
   changes.
3. Regenerate and verify the P2-R3 composite manifest from those final bytes.
   Its path set remains nine repository-root-relative entries; the
   `local_materialization.sh` and `remote_i1_orchestrator.py` digests change.
4. Check both manifests for exact count, exact path set, sorted order, no
   duplicates, self-exclusion and exact hash equality. Do not edit any source
   after these final manifest checks.

The current manifest byte counts are 528 and 1122. Replacing fixed-width
SHA-256 values while preserving formatting and path sets should preserve those
counts, but the future implementation must measure final bytes rather than
asserting a predicted value. The future report must record final identities.

## 11. Test-source decision and coverage

```text
test-source modification decision: NOT REQUIRED
```

The existing persisted tests already provide the required red/green behavior:

- `test_d2_r7b_contract.py` invokes the persisted local materializer in its
  `main()` before T1; with the current HEAD and the stale pin it fails before
  materialization, and with the two-line repair it can pass. T2 checks shell
  syntax, parsed `0<TAB>0` and the bounded cleanup contract; T13 checks the
  same ahead/behind parsing.
- `test_d2_r7b_execution_contract.py` drives the persisted orchestrator through
  the real local source gate in E3, E5/E6 and later success/failure cases. E3
  proves manifest drift gives `HOLD_LOCAL_SOURCE` and zero remote calls; the
  successful synthetic cases prove the current-baseline path after the source
  pin is repaired.
- The current tests cover default-safe no-execute behavior, exact manifest
  path/count/order validation, source transport, synthetic successful phase
  state, remote call counts, path contracts, rollback/cleanup separation and
  zero restart/activation counters.

There is no need to add a test that merely duplicates the two exact source
constants. The exact pin already fails closed on future baseline drift, and
the persisted local materializer plus orchestrator tests exercise that gate.
A future implementation must run the existing tests; this planning Thread did
not run them.

## 12. Exact future implementation validation plan

The following commands are for a separately authorized R30-I1 implementation
Thread. None was executed here.

### 12.1 Pre-repair red evidence

From the repository root, run the persisted local materializer once before the
source edit:

```text
sh docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
```

Expected result: exit `2`, `HOLD / NO MATERIALIZATION: HEAD drift`. The stale
pin fails before the bounded temporary root is created. This is local failure
evidence only.

### 12.2 Source and manifest repair checks

After the two literal source updates and final manifest regeneration, run:

```text
sh -n docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
shasum -a 256 -c docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
shasum -a 256 -c docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
```

Expected results: shell syntax PASS; P2-R2 `6/6 OK`; P2-R3 `9/9 OK`.

Compile persisted Python bytes without import-loader bytecode creation:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -c 'from pathlib import Path; files=[Path("docs/reports/evidence/d2_r7b_p2_r2/remote_preflight.py"),Path("docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py"),Path("docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py"),Path("docs/reports/evidence/d2_r7b_p2_r2/remote_rollback.py"),Path("docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py"),Path("docs/reports/evidence/d2_r7b_p2_r3/remote_postflight.py"),Path("docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py"),Path("docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py")]; [compile(p.read_bytes(), str(p), "exec") for p in files]'
```

Expected result: exit `0`, no `__pycache__` or `.pyc` created in either
evidence directory.

### 12.3 Persisted tests

```text
python3 docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py
```

Expected result from the current persisted file: `MATRIX=PASS count=37/37`.

```text
python3 docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py
```

Expected result from the current persisted file: `E1-E50: PASS 50/50`.

These are local synthetic/persisted-source checks, not remote, deployment,
runtime-load or production evidence. Their private synthetic roots must be
removed only by the separately authorized implementation/review workflow and
only by exact recorded paths.

### 12.4 Final local audit

```text
git status -sb
git diff --name-only
git diff --cached --name-only
git diff --check
git diff --cached --check
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
pgrep -af 'remote_i1_orchestrator\\.py|remote_preflight\\.py|remote_upload_exclusive\\.py|remote_deploy\\.py|remote_postflight\\.py|remote_rollback\\.py|mari@10\\.0\\.0\\.217'
```

Expected implementation-local result: only the four exact candidate paths are
changed, index state is explicitly governed, diff checks pass, no unauthorized
Git mutation occurred and task-owned process count is `0`.

## 13. Remote namespace decision

```text
decision: PRESERVE EXISTING REMOTE ARTIFACT PATHS
```

The decision is based on the current source contract and accepted evidence:

- mapping payload identity is unchanged;
- R29-R1/R29-R2 accepted cleanup evidence records the exact old upload path
  as absent after cleanup, with backup and rollback temp absent;
- helpers, tests and historical reports bind the three basenames broadly;
- the short label is a transaction namespace, not the local Git baseline;
- migrating it would require coordinated source, test, evidence, manifest and
  review changes without improving this local compatibility repair.

No source or test may rename the sidecar, backup or rollback basename as part
of R30-P1. A later namespace migration would require a separate security and
ownership decision with separate authority.

## 14. R30-R2 authority disposition

```text
current R30-R2 authority: ISSUED / NOT CONSUMED / BLOCKED BEFORE START
recommendation: SUPERSEDE / VOID BEFORE FUTURE EXECUTION
```

R30-R2 was limited to the previously accepted exact package. The package will
change when the two source files and manifests are repaired, and it has not
passed the subsequent Architecture, Reliability, Verification and Git gates
for the repaired identity. It must not be reused, resumed or silently rebound
to the repaired package. ChatGPT PM should formally supersede/void it after
durable intake and issue a new task ID plus explicit authority for any future
execution.

## 15. Gate plan and non-inheritance

The only next gate from this Thread is:

```text
R30-P1 plan WRITTEN
→ ChatGPT PM durable intake
```

The planned subsequent gates are:

```text
new explicit R30-I1 authority
→ local-only two-source / two-manifest repair
→ Architecture self-validation
→ independent Reliability review
→ focused repair only if independently required
→ independent Verification
→ separately authorized docs/status closeout, if needed
→ exact-path Git review
→ separately authorized stage / commit / push
→ fresh read-only remote eligibility
→ new separately authorized one-shot config-only execution
```

Every arrow is a separate gate. Planning does not authorize implementation;
local PASS does not authorize Reliability or Verification acceptance; reviewed
package identity does not authorize Git mutation; Git closeout does not
authorize remote eligibility; eligibility does not authorize execution; and
execution does not authorize restart, activation or production acceptance.

### Commit self-pin consequence

The exact `EXPECTED_COMMIT` contract has an important sequencing consequence:
committing the four-path repair changes `HEAD` again. A package repaired to
`63d3cc70...` will therefore become stale after a later Git commit unless the
new commit is not used as the execution baseline.

Before fresh eligibility, PM must choose one explicit safe path:

1. Execute against the reviewed uncommitted package while `HEAD` remains
   `63d3cc70...`, then perform later Git closeout separately; or
2. If Git closeout must precede eligibility, issue a new baseline-refreeze
   task after the commit, update the two pins to the new exact `HEAD`,
   regenerate both manifests, and repeat focused Reliability/Verification
   checks before eligibility.

There is no safe “commit and keep accepting `63d3cc70...`” shortcut. The
baseline-refreeze consequence is governance work caused by the exact-commit
contract, not permission to accept arbitrary HEAD or to skip review gates.

## 16. Risk register

| Risk | Required control | Residual status |
| --- | --- | --- |
| accepting arbitrary HEAD | keep exact branch, exact `HEAD`, exact `origin/main`, `0/0`, cached-empty checks | controlled |
| stale manifest | regenerate P2-R2 before P2-R3; verify exact counts, paths, sort, self-exclusion and hashes | controlled by repair plan |
| remote namespace migration | preserve existing short-label basenames; no helper/test path edits | out of scope |
| reusing R30-R2 | supersede/void before future execution; issue new task ID and authority | blocked by governance |
| direct helper bypass | future execution only through manifest-bound orchestrator sequence | prohibited |
| old worktree / detached HEAD | run from current checkout; no reset, checkout, old worktree or dynamic baseline | prohibited |
| source/test mismatch | run tests against persisted exact paths and verify both manifests after final bytes | controlled by review |
| synthetic PASS while local gate fails | run direct materializer red/green and orchestrator local-source gate before considering remote eligibility | must be demonstrated later |
| commit changes the pinned baseline | choose execution-before-Git or post-commit baseline-refreeze; do not silently proceed | explicit sequencing gate |
| historical report identity drift | treat current persisted bytes and manifests as current authority; do not rewrite historical reports | bounded historical debt |

## 17. MVP alignment

```text
current MVP support: exact single-file D2-R7B config deployment compatibility
minimum invariant: current checkout identity, mapping blob/bytes/SHA and exact source/manifest binding remain fail-closed
scope expansion: none
task inflation: none; the four-path cascade is the minimum identity repair; commit self-pin handling is a governance consequence
classification: MVP-ALIGNED / LOCAL-ONLY COMPATIBILITY PLANNING
```

No product capability, runtime topology, Collector behavior, remote target,
deployment semantics, cleanup capability, rollback capability, restart or
activation behavior is added or changed.

## 18. Thread context assessment

```text
本次输出长度: 长（durable planning report；Chat 仅返回 concise manifest）
当前 Thread 是否建议继续: no
下一轮是否建议新开 Thread: yes
理由: 本 Thread 只建立 Architecture / Integration planning boundary；R30-I1 implementation、Reliability、Verification、Git 与 remote gates 必须使用新的 authority 和独立 Thread。
```

The report is a planning output only. It must stop at PM durable intake.
