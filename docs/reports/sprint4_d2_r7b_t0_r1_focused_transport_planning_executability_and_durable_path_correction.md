# Sprint 4 D2-R7B T0-R1 Focused Transport Planning Executability and Durable-Path Correction

结论：PASS WITH RECOMMENDATIONS

## 1. 身份、范围与 precedence

- 报告名称：Sprint 4 D2-R7B T0-R1 Focused Transport Planning Executability and Durable-Path Correction
- 任务名称：D2-R7B-T0-R1 — Focused Transport Planning Executability and Durable-Path Correction
- Authority ID：PM-D2-R7B-T0-R1-FOCUSED-TRANSPORT-PLANNING-EXECUTABILITY-DURABLE-PATH-CORRECTION-260801-1551
- Executing Thread：Architecture / Integration
- delivery：REPOSITORY_DURABLE_REPORT
- exact report path：docs/reports/sprint4_d2_r7b_t0_r1_focused_transport_planning_executability_and_durable_path_correction.md
- 本轮仅原位修复本 report；不创建 helper、JSON、archive、checksum、workspace 或第二 report。

原 T0 report 不可修改。T0-R1 仅 supersedes its SSH argv、local stream、local/remote workspace、no-overwrite publication、future durable paths and exact allowlists；其余 identity、archive-validation、phase-separation、failure-protection and MVP clauses remain retained.

写入只建立：T0-R1-C1 REPORT REPAIRED = YES；不建立 PM acceptance、Reliability/Verification PASS、workspace、archive、remote target、transport、load、deployment、activation、runtime、production、rollback 或 Git 状态。

## 2. Authority identity 与 fresh baseline

已先完整读取并核验 authority task file：

~~~
path    = docs/thread_handoff/pm_task_20260801T0818Z_d2_r7b_t0_r1_c1_terminal_state_reconciliation_size_compression.md
regular = YES; symlink = NO; bytes = 21432
SHA-256 = a64c97de444801d00bb04aba1af77688e217b0f5bf76510656542f63b89e0777
Git     = ?? <exact path>, exactly one membership; indexed = NO; ignored = NO; unstaged = YES
~~~

其余 frozen identities：

~~~
T0-R1 task     = 31660 bytes / 1b24958de2dc82af80a00996b90b2f8cbbc20d8817d5a603baf1e0aba81982e5
pre-repair report = 26024 bytes / e36fc132ab2c4fb74ae8aaadc05302e1efa3f8d3ea5f17d87a9a401f59a70f11
original T0 task  = 27120 bytes / 07aae9bded474e3b6d5942e0e6516aa13d9e70e8d3ceab3014692b39b1e0c2c3
original T0 report = 24513 bytes / 9e462dc30b5c4f92645a7f06cd79bb48ffe838072277c04ab962acba3091a77c
PM Rules          = 56385 bytes / 4de2fcc7d20a08c3bc33e18a7f2e94861e006a80bce1a76be3781547e6477528
~~~

Fresh live baseline：

~~~
repository = /Users/chenjie/Documents/MES/edge-mes-demo
branch = main
HEAD = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
origin/main = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
ahead/behind = 0/0
tracked diff = docs/thread_handoff/pm_operating_rules.md only
cached diff = empty
git diff --check = PASS; git diff --cached --check = PASS
authority/report status = each exact path has one ?? membership; both untracked, unstaged, not indexed, not ignored
~~~

The pre-repair report was regular/non-symlink and 343 lines. Other untracked paths and the PM Rules modification are pre-existing external state; they were not read, modified or absorbed. Post-repair bytes/SHA-256 are supplied only by the final window manifest; this report does not embed its own final SHA-256.

## 3. Corrected phase sequence

~~~
T0     Accepted Local-Image Transport Planning — original written plan
T0-R1  Focused Executability and Durable-Path Correction
W0     Local Transport Workspace Materialization
A0     Local Archive Generation and Acceptance
R0     Remote Target Read-Only Preflight
S0     Remote Staging Workspace Materialization
T1     Archive Transport and Integrity Acceptance
L0     Remote Docker Load and Exact Object Identity Acceptance
C0     Deployment / Config Compatibility Read-Only Preflight
D0     Deployment Execution
B0     Pre-Activation Rollback Readiness
A1     Activation / Restart
R1     Runtime-Loaded Validation
P0     Production-Fact Validation
B1     Rollback Drill / Rollback Acceptance
C1     Final D2-R7B Closeout and Status Sync
~~~

每个 Gate 都需独立 PM/Owner authority；无 Gate 自动授予下一个 Gate。W0/S0 只 materialize exact directories，不生成 archive bytes/transport data，也不改变 Docker/service/config/lifecycle state。

## 4. B1–B6 blocker closure matrix

| blocker | complete T0-R1 closure |
|---|---|
| B1 SSH argv | -- before destination; R0/S0/L0 persisted /bin/sh -s --; T1 direct /bin/dd argv. |
| B2 local stream | One opened accepted-A0 FD is subprocess.run(..., stdin=fd, shell=False) producer; exactly two SSH calls; fail-closed; no cat/pipeline/SCP/rsync/SFTP. |
| B3 W0 | Exact local paths, ancestor lstat, one-component 0700 creates, owner/device/inode/link/empty checks; any pre-existing exact dir is HOLD. |
| B4 S0 | Zero-write R0 precedes S0; S0 creates only two exact remote dirs through one script-stdin SSH call; no archive/Docker/service action. |
| B5 local publication | A0 uses macOS os.link(..., follow_symlinks=False), fsync/stat/link/bytes/SHA proof, then exact-temp unlink. |
| B6 remote publication | T1 uses /usr/bin/ln --, same-device/inode/link/bytes/SHA proof, then /bin/rm -- exact temp; no mv -n or equivalent. |

## 5. Candidate/archive facts retained from T0

~~~
product source commit = 934ced7b9659cb566628b1709cf6d73463a534d8
accepted candidate    = sha256:8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013
platform              = linux/arm64
Docker context         = colima
WorkingDir             = /app
Cmd                    = ["python", "-m", "app.main"]
~~~

The full image ID, not a tag or filename, is the sole candidate authority. Original T0 retains the ordered nine-layer RootFS and archive validation; T0-R1 does not redesign them. A0 binds raw Config JSON SHA-256 to the candidate suffix, requires linux/arm64, WorkingDir/Cmd and ordered rootfs.diff_ids, reconciles manifest/layer order and layer TAR digests, and separates Git SHA, image/config and archive SHA-256. Archive bytes/SHA remain deferred to A0：

~~~
ARCHIVE BYTES    = TO BE MEASURED IN A0
ARCHIVE SHA256   = TO BE MEASURED IN A0
ARCHIVE ACCEPTED = NO
~~~

## 6. Correct SSH argv and stream contract

Every future SSH argv freezes the following order; the -- is before the destination：

~~~
/usr/bin/ssh
-F /Users/chenjie/.ssh/config
-o BatchMode=yes
-o ControlMaster=no
-o StrictHostKeyChecking=yes
-o UserKnownHostsFile=/Users/chenjie/.ssh/known_hosts
-o ConnectTimeout=10
-o ConnectionAttempts=1
--
<owner-bound-user>@<owner-bound-current-ssh-host>
<remote-command> <remote-args...>
~~~

Destination is mandatory Owner/PM-bound input; 10.0.0.217 is only a historical locator hint. R0/S0/L0 pass exact repository-persisted script bytes as SSH stdin and end remote argv with：

~~~
/bin/sh -s -- <exact-positional-arguments...>
~~~

No inline shell string, interpolation, local heredoc, command substitution or destination-after--- form is permitted. Script bytes/SHA-256, positional args and complete argv are locked before that Gate's one authorized SSH call.

T1 stream is a direct remote command, not a script：

~~~
/usr/bin/ssh <common-options> -- <verified-r0-target> \
  /bin/dd \
  of=/opt/edge-mes-demo/.transport/d2-r7b-t0/accepted-local-image-8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013.tar.uploading \
  bs=1048576 \
  conv=excl \
  status=none
~~~

Each remote token is one argv element; no shell pipeline/redirection.

Future T1 uses /opt/homebrew/opt/python@3.14/bin/python3.14 -B and persisted docs/reports/evidence/d2_r7b_t1_archive_transport_and_integrity_acceptance/transport_runner.py. Before the only stream call it verifies interpreter/primitives; opens only accepted A0 final with os.open(path, os.O_RDONLY | os.O_NOFOLLOW); fstats regular/non-symlink, one-link, expected device/inode, bytes/mode; hashes the FD, requires A0 SHA-256, then os.lseek(fd, 0, os.SEEK_SET). It passes that FD directly to subprocess.run(SSH_STREAM_ARGV, stdin=fd, shell=False, ...), records exit/bounded stdout-stderr hashes/expected bytes/call count, and makes any open/hash/seek/subprocess exception or nonzero SSH exit terminal HOLD. No second producer, /bin/cat, shell redirection, pipeline, SCP, rsync or SFTP. T1 has exactly two SSH calls: stream, then persisted remote_verify_publish.sh verify/publication/recheck.

## 7. Workspace materialization contracts

### W0 — local

Exact external paths：

~~~
base parent   = /Users/chenjie/Documents/MES/edge-mes-transport
task workspace = /Users/chenjie/Documents/MES/edge-mes-transport/d2-r7b-t0
~~~

W0 is future-only and uses frozen Python 3.14. It reads exact ancestors, runtime identity and declared repository paths. /Users/chenjie/Documents/MES must already be a regular non-symlink directory owned/searchable by the authorized user. It lstat-checks ancestors, rejects symlink/non-directory/foreign-owner/mode/collision, creates at most two missing components one at a time with 0700, fsyncs after creation, and re-lstats owner/device/inode/mode/link/empty state. Either exact directory already present is fail-closed; no reuse authority, archive/temp/final, Docker, network or remote action. W0 PASS establishes only LOCAL TRANSPORT WORKSPACE MATERIALIZED = YES; A0 requires PM/Owner authority.

### S0 — remote

R0 observes without mutation verified host/user/architecture/Docker identity, /opt/edge-mes-demo, .transport, child/temp/final absence, same-filesystem/owner/mode/space eligibility, privilege-free creation and exact tools /bin/sh, /bin/mkdir, /bin/chmod, /bin/dd, /usr/bin/ln, /usr/bin/stat, /usr/bin/sha256sum, /bin/rm, /usr/bin/docker. Ambiguity is HOLD. Pre-existing .transport is acceptable only if regular non-symlink, expected-owner, same-filesystem and non-unsafe-mode.

S0 may create only：

~~~
/opt/edge-mes-demo/.transport                 # only if R0 proved absent and eligible
/opt/edge-mes-demo/.transport/d2-r7b-t0        # absent before S0
~~~

S0 uses exactly one common-prefix SSH call with persisted remote_workspace_materializer.sh on stdin and positional args (/opt/edge-mes-demo, /opt/edge-mes-demo/.transport, /opt/edge-mes-demo/.transport/d2-r7b-t0). Its set -eu script does no mkdir -p, follows no symlink, uses /bin/mkdir then immediate /bin/chmod 0700, rechecks owner/mode/device/inode/empty state, and never overwrites, deletes, chowns, sudo-repairs or touches archive/Docker/Compose/config/service state. Maximum creates is two; all other writes are zero. S0 PASS establishes only REMOTE STAGING WORKSPACE MATERIALIZED = YES; T1 requires PM acceptance and Owner authorization.

## 8. A0 and T1 no-overwrite publication

### A0 local paths and transition

The original T0 archive paths remain the future A0 external paths, unchanged：

~~~
parent = /Users/chenjie/Documents/MES/edge-mes-transport/d2-r7b-t0
temp   = /Users/chenjie/Documents/MES/edge-mes-transport/d2-r7b-t0/.accepted-local-image-8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013.tar.tmp
final  = /Users/chenjie/Documents/MES/edge-mes-transport/d2-r7b-t0/accepted-local-image-8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013.tar
~~~

After one full-ID docker image save and A0 validation, require temp regular/non-symlink/one-link and final absent. Publish only with：

~~~python
os.link(temp_path, final_path, follow_symlinks=False)
~~~

EEXIST or any error is terminal HOLD. Then open/fsync final and parent; lstat temp/final for same device/inode, regular/non-symlink, link count 2 and exact bytes/SHA; unlink only exact temp; fsync parent again; require temp absent and final regular/non-symlink/one-link with unchanged device/inode/bytes/SHA/mode 0600. os.replace, rename-overwrite, mv, copy-to-final, truncation and unlinking an existing final are forbidden; this replaces T0 renameat2(RENAME_NOREPLACE)/unspecified-equivalent.

### T1 remote paths and transition

~~~
remote parent = /opt/edge-mes-demo/.transport/d2-r7b-t0
temp          = /opt/edge-mes-demo/.transport/d2-r7b-t0/accepted-local-image-8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013.tar.uploading
final         = /opt/edge-mes-demo/.transport/d2-r7b-t0/accepted-local-image-8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013.tar
script        = docs/reports/evidence/d2_r7b_t1_archive_transport_and_integrity_acceptance/remote_verify_publish.sh
~~~

The persisted script (exact executable paths proven by R0) requires temp regular/non-symlink/one-link and final absent; verifies temp bytes/SHA; runs /usr/bin/ln -- <temp> <final> on the verified filesystem; requires same device/inode/link count 2; re-verifies final bytes/SHA; then runs /bin/rm -- <temp> only after all checks. It finally requires temp absent and final regular/non-symlink/one-link with unchanged inode/bytes/SHA. It never uses mv, mv -n, ln -f, wildcard/glob, find -delete, broad cleanup or paths outside the two exact archive paths, and never removes final after later failure. This replaces T0 mv -n/unspecified-equivalent.

## 9. Repository durable paths (future proposals, not execution authority)

Archive bytes/workspaces remain outside the Git checkout. All cross-Thread report, JSON, runner and script paths are exact repository paths：

| Gate | report | exact artifacts |
|---|---|---|
| W0 | docs/reports/sprint4_d2_r7b_w0_local_transport_workspace_materialization.md | docs/reports/evidence/d2_r7b_w0_local_transport_workspace_materialization/01_workspace_materialization.json; docs/reports/evidence/d2_r7b_w0_local_transport_workspace_materialization/workspace_materializer.py |
| A0 | docs/reports/sprint4_d2_r7b_a0_local_archive_generation_and_acceptance.md | docs/reports/evidence/d2_r7b_a0_local_archive_generation_and_acceptance/01_archive_acceptance.json; docs/reports/evidence/d2_r7b_a0_local_archive_generation_and_acceptance/archive_validator.py |
| R0 | docs/reports/sprint4_d2_r7b_r0_remote_target_readonly_preflight.md | docs/reports/evidence/d2_r7b_r0_remote_target_readonly_preflight/01_remote_preflight.json; docs/reports/evidence/d2_r7b_r0_remote_target_readonly_preflight/remote_probe.sh; docs/reports/evidence/d2_r7b_r0_remote_target_readonly_preflight/remote_preflight_runner.py |
| S0 | docs/reports/sprint4_d2_r7b_s0_remote_staging_workspace_materialization.md | docs/reports/evidence/d2_r7b_s0_remote_staging_workspace_materialization/01_remote_workspace_materialization.json; docs/reports/evidence/d2_r7b_s0_remote_staging_workspace_materialization/remote_workspace_materializer.sh; docs/reports/evidence/d2_r7b_s0_remote_staging_workspace_materialization/remote_workspace_materialization_runner.py |
| T1 | docs/reports/sprint4_d2_r7b_t1_archive_transport_and_integrity_acceptance.md | docs/reports/evidence/d2_r7b_t1_archive_transport_and_integrity_acceptance/01_transport_acceptance.json; docs/reports/evidence/d2_r7b_t1_archive_transport_and_integrity_acceptance/transport_runner.py; docs/reports/evidence/d2_r7b_t1_archive_transport_and_integrity_acceptance/remote_verify_publish.sh |
| L0 | docs/reports/sprint4_d2_r7b_l0_remote_docker_load_and_exact_object_identity_acceptance.md | docs/reports/evidence/d2_r7b_l0_remote_docker_load_and_exact_object_identity_acceptance/01_remote_load_acceptance.json; docs/reports/evidence/d2_r7b_l0_remote_docker_load_and_exact_object_identity_acceptance/remote_load_probe.sh; docs/reports/evidence/d2_r7b_l0_remote_docker_load_and_exact_object_identity_acceptance/remote_load_runner.py |

No future report/artifact may live only under /Users/chenjie/Documents/MES/edge-mes-transport.

## 10. Corrected future Gate allowlists

Every future task must restate its own exact authority. These proposals are review-ready, not executable from T0-R1/C1.

### W0

- Paths: local reads exact /Users/chenjie/Documents/MES ancestors and frozen Python; repository reads/writes only W0 report/JSON/workspace_materializer.py; external archive and remote paths none.
- Budget: maximum two exact one-component directory creates; zero archive/file/Docker/SSH/network actions.
- Forbidden: reuse of either pre-existing exact directory, mkdir -p, symlink following, repair/delete/chown, temp/archive creation, Git mutation.
- PASS/HOLD: owner/device/inode/mode/link/empty invariants yield only local workspace materialized; collision/ambiguity is HOLD. Next A0 after PM/Owner authority; no inheritance.

### A0

- Paths: local reads W0 identity, candidate full ID and exact external parent/temp/final; repository report/JSON/archive_validator.py; remote/network none.
- Budget/command: one /opt/homebrew/bin/docker image save --output <exact-temp> <full-ID>; future Python 3.14 validator; no second save/fallback.
- Writes/forbidden: exact temp, hard-link final and declared repository files only; no directory/remote/Git action; no tag input, export, overwrite, os.replace, mv, broad cleanup or candidate/source/config change.
- PASS/HOLD: safe TAR, manifest/config/layer/RootFS, exact bytes/SHA and hard-link transition all pass; unknown archive bytes/SHA before A0. Next R0; no inheritance.

### R0

- Paths: local R0 report/JSON/script/runner and exact SSH config/known-hosts reads; remote read-only /opt/edge-mes-demo, .transport, task-child, archive paths, Docker/Collector identity and required tools; external archive none.
- Budget/command: exactly one SSH with common prefix and persisted remote_probe.sh via /bin/sh -s --; zero remote writes/Docker mutation.
- Forbidden: historical 10.0.0.217 as identity, mkdir/upload/dd/ln/rm/load/tag/Compose/config/restart/cleanup/privilege escalation.
- PASS/HOLD: target/user/arch/Docker, root/staging eligibility, absence/collision, free space, tools and permission checks all pass; else terminal HOLD. Next S0; no inheritance.

### S0

- Paths: local S0 report/JSON/script/runner; remote only exact .transport and d2-r7b-t0; external archive none.
- Budget/command: exactly one SSH with remote_workspace_materializer.sh stdin and /bin/sh -s -- positional args; maximum two mkdir/chmod directory creates; zero archive/Docker/service/config actions.
- Writes/forbidden: only R0-eligible missing exact dirs with immediate 0700; no extra file writes; no mkdir -p, overwrite/delete/chown/sudo/repair, archive, transport, Docker, Compose, config or lifecycle.
- PASS/HOLD: exact owner/mode/device/inode/empty post-state passes; else terminal HOLD. Next T1; only REMOTE STAGING WORKSPACE MATERIALIZED = YES, no inheritance.

### T1

- Paths: local read-only exact A0 final and T1 report/JSON/runner/script; external archive paths above; remote only exact temp/final staging paths; no active deployment paths.
- Budget/command: exactly two SSH calls—direct /bin/dd stream and persisted verify/publish script; opened-FD producer only; zero Docker/load/deployment/lifecycle calls.
- Writes/forbidden: one remote temp create, same-filesystem hard-link final, exact-temp unlink after proof; no directory/foreign cleanup; no pipeline/redirection, /bin/cat, SCP/rsync/SFTP, overwrite, mv -n, ln -f, retry, Docker/load/tag/restart.
- PASS/HOLD: A0/R0/S0 identities, FD checks, stream exit, remote bytes/SHA, inode/link and final recheck all pass; else HOLD. Next L0; only TRANSPORTED = YES and REMOTE STAGED ARCHIVE ACCEPTED = YES.

### L0

- Paths: local T1 identity and L0 report/JSON/script/runner; remote exact accepted final archive and Docker object; no local archive mutation or active deployment path.
- Budget/command: exactly one SSH with remote_load_probe.sh stdin and /bin/sh -s --; exactly one /usr/bin/docker image load --input <exact-final> only after exact full ID is absent, then exact-ID/config/RootFS recheck.
- Writes/forbidden: one load-created object when absent; zero tag/remove/archive cleanup/Compose/service writes; no tag-based or output-text-only acceptance, other input path, tag/remove/restart/activation/cleanup/foreign-object mutation.
- PASS/HOLD: full ID, linux/arm64, immutable Config, WorkingDir/Cmd and ordered RootFS match; pre-existing exact object needs explicit reuse authority; ambiguity is HOLD. Next C0; no deployment inheritance.

## 11. Failure, retry, cleanup and later separation

Future W0/A0/R0/S0/T1/L0 are fixed-budget and fail-closed: each has a new Owner-bound attempt ID, no default/reuse/fallback/retry after a consumed call; foreign/ambiguous objects are never removed; failure does not consume the next Gate; only exact T1 temp may be removed after all proof; all other cleanup needs exact authority. No global filesystem, Docker, image, container or service cleanup.

C0 is read-only; D0 does not activate; B0 precedes A1; A1 is separate from R1; P0 is separate from runtime-loaded validation; B1 is a real rollback drill/acceptance; C1 requires status sync and PM acceptance. PLC/HMI control and Edge read-only collection boundaries remain unchanged. Per-Gate evidence records authority/attempt/phase, expected-versus-actual identities, exact argv/script identity, RFC3339 UTC times, exits, bytes/SHA, archive/config/layer/image identity, mutation counters, terminal reason and next Gate. Static evidence is never remote/runtime/production truth.

## 12. Retained versus superseded T0 clauses

### Explicitly superseded by T0-R1

(1) SSH argv: -- precedes destination; R0/S0/L0 use persisted script stdin; T1 uses direct /bin/dd. (2) T1 producer: opened A0 FD plus shell-free subprocess; no implicit stdin/pipeline/cat. (3) W0/S0: separate exact-directory Gates with no-reuse/eligibility contracts. (4) A0: Python hard-link no-overwrite replaces renameat2/unspecified-equivalent. (5) T1: atomic /usr/bin/ln -- replaces mv -n/unspecified-equivalent. (6) Future durable paths/allowlists: repository W0/S0/T1 helper/script identities in Sections 9–10 replace external/ambiguous authority.

### Retained non-conflicting T0 clauses

Accepted full image ID/source commit/candidate identity separation; Docker image-save TAR and full-ID input; archive bytes/SHA deferred to A0; manifest, Config, ordered RootFS and layer validation; historical locator not current target authority; transport/load/deployment/activation/runtime/production separation; fail-closed failure, retry, foreign-object protection and no broad cleanup; rollback readiness before activation; proportional evidence and MVP alignment.

## 13. Review recommendation, validation record and terminal conclusion

Recommended smallest review sequence：

~~~
PM intake of T0-R1
→ focused Reliability planning review of original T0 + T0-R1
→ focused Verification exact-argv / durable-path / allowlist review
→ PM final transport-planning acceptance
→ Owner authorization of W0
~~~

Data Quality review is not automatic because this correction introduces no production-data semantics.

Actual C1 counters：

~~~
Python executed = 0
Docker action = 0
archive/workspace mutation = 0
SSH/network/remote call or mutation = 0
deployment/lifecycle action = 0
new files created = 0
Git stage/commit/push/tag = 0
authorized in-place report repair = 1
~~~

C1 validation: task/pre-repair/original T0/PM Rules identities; regular/non-symlink; changed set; size <=23500/24576; B1–B6; phase/path/allowlist; terminal count/equality; diff/cached-empty/status after final replacement. Manifest bytes/SHA; no self-hash.

MVP 路径一致性 = MVP-ALIGNED：supports safe accepted-local-image transport planning; closes false-PASS/unsafe-mutation boundaries; adds no product capability, topology, evidence framework, SBOM, signing, audit/forensics or retention; scope drift = NO.

结论：PASS WITH RECOMMENDATIONS

Single next Gate：PM Independent Intake — D2-R7B-T0-R1-C1 Focused Terminal-State Reconciliation and Size Compression。
