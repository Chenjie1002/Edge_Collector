# Sprint 4 D2-R7B T0-R3-C1-R1 Corrected Read-Boundary Fresh Retry

报告名称：Sprint 4 D2-R7B T0-R3-C1-R1 Corrected Read-Boundary Fresh Retry
任务名称：D2-R7B-T0-R3-C1-R1 — Corrected Read-Boundary Fresh Retry of SSH Serialization, Non-Recursive Evidence Identity and Attempt-Scoped Durable Paths
执行 Thread：Architecture / Integration
结论：PASS WITH RECOMMENDATIONS

Report delivery mode：REPOSITORY_DURABLE_REPORT
Report path：`docs/reports/sprint4_d2_r7b_t0_r3_c1_r1_corrected_read_boundary_fresh_retry.md`
Authority ID：`PM-D2-R7B-T0-R3-C1-R1-CORRECTED-READ-BOUNDARY-FRESH-RETRY-260801-1816`

## 1. Authority identity and fresh baseline

Input identity checks：PASS。

| exact input | bytes | SHA-256 | filesystem / Git membership |
|---|---:|---|---|
| `docs/thread_handoff/pm_task_20260801T1016Z_d2_r7b_t0_r3_c1_r1_corrected_read_boundary_fresh_retry.md` | 32727 | `b4196fc6704ff75b2b77bee1bd5d902ae3c9c9c6d955812945bfdeffb539f557` | regular, non-symlink, link=1, one `??`, untracked, unstaged, not indexed, not ignored |
| `docs/thread_handoff/pm_operating_rules.md` | 56385 | `4de2fcc7d20a08c3bc33e18a7f2e94861e006a80bce1a76be3781547e6477528` | regular, non-symlink, link=1, tracked `M`, not ignored |
| `docs/reports/sprint4_d2_r7b_t0_accepted_local_image_transport_plan.md` | 24513 | `9e462dc30b5c4f92645a7f06cd79bb48ffe838072277c04ab962acba3091a77c` | regular, non-symlink, link=1, one `??`, untracked, not indexed, not ignored |
| `docs/reports/sprint4_d2_r7b_t0_r1_focused_transport_planning_executability_and_durable_path_correction.md` | 23486 | `2ac3e90d50c6252a35cd2445a29615b0ca7c31cc7643cfdace657aa035d2a937` | regular, non-symlink, link=1, one `??`, untracked, not indexed, not ignored |
| `docs/reports/sprint4_d2_r7b_t0_r2_focused_reliability_transport_planning_review.md` | 20240 | `089b28fb82100ecadbf05f3fbf08a0ec5c4836e5cc2eb4fcbedd0faace2d5ec0` | regular, non-symlink, link=1, one `??`, untracked, not indexed, not ignored |
| `docs/thread_handoff/pm_task_20260801T0926Z_d2_r7b_t0_r3_reliability_blocking_terminalization_freshness_recovery_contract_repair.md` | 29504 | `7ac5f7cae387692d8776f185f0bcc746d5c29fe851de562b32181e0c766fa2c6` | regular, non-symlink, link=1, one `??`, untracked, not indexed, not ignored |
| `docs/reports/sprint4_d2_r7b_t0_r3_reliability_blocking_terminalization_freshness_and_recovery_contract_repair.md` | 24535 | `0866247f79f2f0f125c211bc00324a9d97115e236c58f929304fda187f19b08b` | regular, non-symlink, link=1, one `??`, untracked, not indexed, not ignored |
| `docs/reports/sprint4_d2_r7b_t0_r3_c1_ssh_serialization_nonrecursive_identity_and_attempt_scoped_paths_correction.md` | 2423 | `d1957b79ab582e9644d5ca4c63fc17e525b762c38a97231bf4119abbf8863d4e` | regular, non-symlink, link=1, one `??`, untracked, not indexed, not ignored |

Fresh live baseline：

```text
repository   = /Users/chenjie/Documents/MES/edge-mes-demo
branch       = main
HEAD         = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
origin/main  = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
ahead/behind = 0/0
tracked diff = docs/thread_handoff/pm_operating_rules.md only
cached diff  = empty
git diff --check = PASS
git diff --cached --check = PASS
current task exact membership = one ??; untracked/unstaged/not indexed/not ignored
report path before write = ABSENT, non-symlink
```

The repository contains pre-existing external dirty/untracked paths. They were kept excluded and unmodified; the task-owned changed/created set is the exact report path only. Candidate image, Docker daemon, external transport path and remote target were not inspected.

## 2. Required read ledger and boundary

The following is the complete project content-read ledger, in the required order：

1. `docs/thread_handoff/pm_task_20260801T1016Z_d2_r7b_t0_r3_c1_r1_corrected_read_boundary_fresh_retry.md` — read to EOF, 674 lines.
2. `docs/thread_handoff/pm_operating_rules.md` — read only the named sections/topics concerning pre-authority execution lock, output-path collision/`OUTPUT_PATH_PREEXISTS`, durable evidence, authority consumption, retry/recovery, terminalization, report delivery, `WRITTEN` separation and no inheritance; unrelated PM Rules sections were not read.
3. `docs/reports/sprint4_d2_r7b_t0_accepted_local_image_transport_plan.md` — read to EOF, 481 lines.
4. `docs/reports/sprint4_d2_r7b_t0_r1_focused_transport_planning_executability_and_durable_path_correction.md` — read to EOF, 318 lines.
5. `docs/reports/sprint4_d2_r7b_t0_r2_focused_reliability_transport_planning_review.md` — read to EOF, 203 lines.
6. `docs/thread_handoff/pm_task_20260801T0926Z_d2_r7b_t0_r3_reliability_blocking_terminalization_freshness_recovery_contract_repair.md` — read to EOF, 631 lines.
7. `docs/reports/sprint4_d2_r7b_t0_r3_reliability_blocking_terminalization_freshness_and_recovery_contract_repair.md` — read to EOF, 334 lines.
8. `docs/reports/sprint4_d2_r7b_t0_r3_c1_ssh_serialization_nonrecursive_identity_and_attempt_scoped_paths_correction.md` — read to EOF, 34 lines, only for predecessor terminal identity, actual fail-closed result and lack of substantive closure.

Unauthorized content reads：NO。No other project content path was read. The predecessor diagnosis is corrected precisely: the prior procedural HOLD was caused by unauthorized extra content reads of the original T0, T0-R1 and T0-R2 task files; it was not a report-before-task ordering issue. The predecessor HOLD remains terminal evidence and is not reclassified.

## 3. Precedence, retained identity and scope

This report supersedes only the conflicting T0-R3 clauses on SSH serialization, digest projection and durable path identity. It retains T0-R3 execution-lock, terminalization, freshness, ownership and recovery contracts, the eight T0-R2 Reliability protection goals, B1–B6, accepted candidate identity, Config/ordered RootFS/archive validation and every phase boundary.

Retained planning inputs：

- accepted candidate full-ID: `sha256:8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013`;
- product source commit: `934ced7b9659cb566628b1709cf6d73463a534d8`;
- platform: `linux/arm64`; Docker context: `colima`; `WorkingDir=/app`; `Cmd=["python","-m","app.main"]`;
- ordered RootFS has 9 layers and remains ordered; A0 must validate manifest, raw Config JSON identity, OS/architecture, WorkingDir/Cmd, rootfs and every layer digest;
- W0 → A0 → R0 → S0 → T1 → L0 remain independent Gates. Archive bytes/SHA are measured only by A0; R0 remains zero-mutation eligibility; T1 remains transport/staging only; L0 remains exact remote image acceptance;
- A0 uses hard-link no-overwrite publication; T1 uses exclusive temporary creation, same-filesystem no-overwrite hard-link publication and exact temporary removal only after proof;
- deployment, activation, runtime-loaded, production-fact and rollback claims remain separate; PLC/HMI retain control authority and Edge remains read-only for collection;
- `classification=MVP-ALIGNED`, product claim unchanged, `scope drift=NO`, `scope inflation=NO`, new product feature=NO. No registry, SBOM, signing, generic evidence service/library/database, telemetry, HA, orchestration, audit/forensics or retention scope is added.

## 4. PM blocker closure: 3/3

| blocker | conflicting predecessor ambiguity | corrected controlling contract and removed false-PASS/unsafe ambiguity | focused Reliability rereview from durable text |
|---|---|---|---|
| `PM-R3-001` | OpenSSH destination-following values were described as if independently preserved remote argv; archive stdin and script transport were not separated. | OpenSSH is modeled as one server-side remote-command string. Future T1 freezes one complete serialized string, exactly one local argv element after destination, `posix-sh-single-quote-v1`, explicit `$0`/`$1…$N` semantics, byte bounds, offline vectors and same-call host/root/staging guards. The accepted A0 archive FD remains direct SSH stdin and the sole archive-byte producer; guard source bytes never use stdin. | YES |
| `PM-R3-002` | A final evidence/JSON/raw-output hash could be interpreted as a hash of the document containing that hash, creating recursive or self-contradictory identity. | `execution_lock_payload_canonical_sha256` and `terminal_payload_canonical_sha256` hash only their respective RFC 8785/JCS canonical payload bytes. Payloads contain no self-dependent digest. Predecessor lock raw SHA and final terminal-document raw SHA are external whole-file identities; the complete final JSON raw SHA is never embedded in that same JSON. R0 stdout/stderr raw hashes are computed by the local runner after SSH completion, never by remote self-report. | YES |
| `PM-R3-003` | Fixed per-Gate report/evidence/helper paths could be overwritten or reused after terminalization, recovery or a fresh normal attempt. | Every normal/recovery authority consumes a PM/Owner-prebound literal attempt ID and resolves report/evidence/temp/helper paths before publication. Each attempt root is immutable after PASS/HOLD; recovery and a later fresh normal attempt have different IDs and roots, with no `latest`, alias, symlink, truncate, rename-overwrite, delete or reopen. | YES |

The three blockers are contractually closed, not merely acknowledged. No PM acceptance, Reliability rereview, Verification or execution authority is implied.

## 5. Correct OpenSSH serialization and archive stream contract

OpenSSH does not preserve independent remote argv after the destination. The future T1 local argv is frozen as：

```text
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
<one-complete-serialized-remote-command-string>
```

There is exactly one local argv element after destination. The logical remote string is：

```text
/bin/sh -c <Q(remote_stream_guard_source)> <Q(arg0)> <Q(arg1)> ... <Q(argN)>
```

For `/bin/sh -c`, the first value after the command string is the explicit `$0` (`arg0`); the next value is `$1` (`arg1`), continuing through `$N`. Values following the destination are therefore not treated as independently transmitted remote argv. The second verify/publish call uses the same one-string rule or a separately frozen contract that proves the exact server-side command bytes; it cannot revert to implied remote argv preservation.

`Q` is frozen as `posix-sh-single-quote-v1`：

1. input is a bounded 7-bit ASCII byte sequence;
2. NUL or any byte above `0x7f` is HOLD before execution lock;
3. output begins and ends with ASCII byte `0x27`;
4. each input single quote is encoded as exact bytes `0x27 0x5c 0x27 0x27`, displayed as `'\''`;
5. every other byte, including LF in guard source, is preserved byte-for-byte inside the quoted token;
6. locale-dependent escaping, Unicode normalization, ANSI-C quoting, `printf %q`, double-quote encoding, command substitution and shell expansion are forbidden.

Future T1 positional values are PM-bound 7-bit ASCII with no NUL/LF and explicit byte ceilings. The guard source is regular/non-symlink, LF-normalized, 7-bit ASCII, NUL-free and `<=8192` bytes. The final serialized remote command is 7-bit ASCII and `<=16384` bytes. The execution lock records guard path/bytes/SHA, encoder version, each unquoted positional value and byte length, serialized-command bytes/SHA, complete local SSH argv/call budget, and offline fixture identity/result.

Before the lock, a zero-network Gate-local validator runs fixed ASCII fixtures covering empty input, spaces, LF in script source, single quote, backslash, semicolon, dollar sign and mixed tokens. It proves that frozen local `/bin/sh -c` interpretation reconstructs exact script bytes and positional values; failure is local HOLD before SSH authority.

The accepted-A0 archive FD remains direct SSH stdin and the only archive-byte producer. The runner opens/checks/hashes/seeks that FD and passes it directly to shell-free `subprocess.run(..., stdin=fd)`. No `/bin/cat`, pipeline, shell redirection, SCP, rsync, SFTP or second archive producer is permitted. Guard source bytes are transported as the single remote-command argv element, not through archive stdin.

## 6. Non-recursive evidence identity and R0 hashing

Every future Gate envelope has the conceptual fields：

```text
schema_version
attempt_id
execution_lock_payload
execution_lock_payload_canonical_sha256
predecessor_document_raw_sha256
terminal_payload
terminal_payload_canonical_sha256
```

In the pre-mutation lock document, `terminal_payload` and its digest are absent. `execution_lock_payload_canonical_sha256` is SHA-256 over only RFC 8785/JCS canonical bytes of `execution_lock_payload`; that payload contains no field equal to or dependent on its own digest. Before terminal replacement, the complete lock-document raw SHA-256 is measured externally and becomes `predecessor_document_raw_sha256` in the terminal document. `terminal_payload_canonical_sha256` similarly hashes only JCS bytes of `terminal_payload`, which has no self-dependent field.

The complete final terminal JSON raw SHA-256 is external metadata supplied by the attempt report/window manifest or a later exact identity inventory. It is not embedded in the same final JSON. The ambiguous T0-R3 phrases “canonical/raw JSON SHA-256”, “terminal JSON SHA-256” and remote raw-output self-hash are superseded wherever they could imply recursion. Canonical payload hashes and external raw whole-file hashes are separate authorities.

R0 emits exactly one bounded UTF-8 JSON object plus one newline. It does not claim its complete stdout/stderr hash. After SSH completion, the local runner computes raw stdout bytes/count/SHA-256 and raw stderr bytes/count/SHA-256, parses the remote object under the strict one-record/EOF/schema contract, and computes the payload canonical SHA-256. Those identities enter the local attempt-scoped envelope. Missing/unknown/duplicate fields, malformed data, truncation, extra bytes, nonzero exit, timeout or parser failure is `R0 HOLD / NOT_OBSERVED`; no stale merge or remote self-hash is allowed.

## 7. PM-bound attempt IDs and immutable paths

Every future authority publishes one literal attempt ID before execution. The runner consumes it and never generates, increments, infers or defaults it.

```text
normal   = d2-r7b-<gate>-a<NN>
recovery = d2-r7b-<gate>-rc-a<NN>
gate     = w0 | a0 | r0 | s0 | t1 | l0
NN       = 01 through 99
regex    = \Ad2-r7b-(w0|a0|r0|s0|t1|l0)(-rc)?-a(0[1-9]|[1-9][0-9])\z
```

No slash, dot, whitespace, uppercase, Unicode, environment expansion, path separator or previously published ID is allowed. Recovery never resets numbering and cannot authorize a later normal attempt. After recovery, PM/Owner must publish a different normal ID.

Attempt root grammar：`docs/reports/evidence/d2_r7b_<gate>/<attempt_id>/`
Attempt report grammar：`docs/reports/sprint4_d2_r7b_<gate>_<attempt_id>_<gate-specific-slug>.md`

The angle-bracket forms above are planning grammar only; each future Prompt must resolve them to literal exact paths before publication. Under each root, the future task declares only its exact files, such as `01_<gate>_evidence.json`, same-directory `01_<gate>_evidence.json.tmp`, and the named helper/runner/script. All exact paths must be absent and non-symlink at entry. After terminalization they are immutable predecessor evidence. No `latest`, fixed mutable index, alias, symlink, convenience copy, overwrite, truncate, relink, delete or reopen is permitted.

### Future Gate path/budget/terminal table

| Gate | normal / recovery ID | report; evidence final / same-dir temp; helper/runner/script | frozen budget, terminal/reuse boundary and recovery |
|---|---|---|---|
| W0 | `d2-r7b-w0-aNN` / `d2-r7b-w0-rc-aNN` | `..._<attempt_id>_<slug>.md`; `01_w0_evidence.json` / `.tmp`; `workspace_materializer.py` | max two one-component directory creates; lock before create; precondition `NO_MUTATION`, partial create `RETAINED_RECOVERY_REQUIRED`; no normal reuse/removal of retained/foreign dirs; W0-RC only; next A0 only under fresh authority |
| A0 | `d2-r7b-a0-aNN` / `d2-r7b-a0-rc-aNN` | `..._<attempt_id>_<slug>.md`; `01_a0_evidence.json` / `.tmp`; `archive_validator.py` | exactly one full-ID image save and hard-link no-overwrite publication; any post-save/link/unlink/proof uncertainty keeps `ARCHIVE ACCEPTED=NO`; A0-RC only; next R0 only under fresh authority |
| R0 | `d2-r7b-r0-aNN` / no external recovery category | `..._<attempt_id>_<slug>.md`; `01_r0_evidence.json` / `.tmp`; `remote_probe.sh`, `remote_preflight_runner.py` | exactly one zero-mutation SSH, one record/EOF/bounds/schema; partial/uncertain=`NOT_OBSERVED`, no stale merge; no recovery category in current plan, fresh R0 uses a new normal ID/root after new authority; next S0 only after fresh acceptance |
| S0 | `d2-r7b-s0-aNN` / `d2-r7b-s0-rc-aNN` | `..._<attempt_id>_<slug>.md`; `01_s0_evidence.json` / `.tmp`; `remote_workspace_materializer.sh`, `remote_workspace_materialization_runner.py` | one SSH, max two exact directory creates; same-call host/root/parent rebind before mutation; safe parent reuse only with exact bound identity and absent child; partial state `RETAINED_RECOVERY_REQUIRED`; S0-RC only; next T1 fresh |
| T1 | `d2-r7b-t1-aNN` / `d2-r7b-t1-rc-aNN` | `..._<attempt_id>_<slug>.md`; `01_t1_evidence.json` / `.tmp`; `transport_runner.py`, `remote_stream_guard.sh`, `remote_verify_publish.sh` | exactly two SSH calls: guarded stream then verify/publish/recheck; FD sole producer; timeout/partial/publication-unobserved blocks L0 and retry; T1-RC only; next L0 fresh |
| L0 | `d2-r7b-l0-aNN` / `d2-r7b-l0-rc-aNN` | `..._<attempt_id>_<slug>.md`; `01_l0_evidence.json` / `.tmp`; `remote_load_probe.sh`, `remote_load_runner.py` | one SSH and one image load only after exact full-ID absence; post-load uncertainty=`LOAD_STATE_UNCERTAIN`; no second load/tag/remove/C0; L0-RC only; next C0 only under fresh authority |

All rows retain T0-R3 lock-before-authority, same-call freshness, exact pre-state, terminal JSON durability, no-retry/no-reuse and foreign-object protection. R0 is zero mutation and has no external recovery category; all other recovery categories are failure-only, unpublished in the happy path and require new PM/Owner authority.

## 8. Retained Reliability and transport protection goals

The eight accepted T0-R2 findings remain accounted for and are not reopened：

- `REL-R2-W0-001`: W0 ownership branches, exact post-create identity and retained recovery are durable; no normal adoption of a partial workspace.
- `REL-R2-S0-001`: safe pre-existing `.transport` reuse, absent-child creation, child collision and failed-parent retention are explicit.
- `REL-R2-R0-001`: S0/T1/L0 bind current stable host, deployment root and staging-parent identity in the consuming call before mutation/publication.
- `REL-R2-R0-002`: R0 has one complete bounded record, clean EOF, strict schema and `NOT_OBSERVED` on any incomplete result.
- `REL-R2-A0-001`: every post-link/post-unlink boundary is terminalized; archive acceptance remains NO until final-only proof and durable terminal JSON.
- `REL-R2-T1-001`: remote temp/final/publication states and unobserved outcomes remain HOLD, retained and blocked from L0/retry.
- `REL-R2-L0-001`: load-state uncertainty, full-ID/config/RootFS mismatch and explicit reuse are terminal; retention is not PASS.
- `REL-R2-X-001`: each Gate persists its own immutable execution lock before authority and durable terminal JSON after it; report-write failure cannot authorize retry.

B1–B6 are retained：B1 exact SSH option/destination ordering and now one serialized remote command; B2 opened accepted-A0 FD, shell-free producer, exactly two T1 calls and no pipeline/cat; B3 exact W0 paths, one-component 0700 creation and no reuse of pre-existing task workspace; B4 zero-write R0 before S0 and only exact remote directories; B5 A0 hard-link no-overwrite plus fsync/stat/hash/link proof and exact-temp removal; B6 T1 exclusive temp creation, same-device/inode/link/bytes/SHA proof, hard-link publication and exact-temp removal with no overwrite or foreign cleanup.

## 9. Review sequence, counters and authority separation

Review sequence：

```text
PM Independent Intake — D2-R7B-T0-R3-C1-R1
→ if accepted, fresh PM handoff before broader review
→ focused Reliability rereview of original T0 + repaired T0-R1 + T0-R3 + T0-R3-C1-R1
→ focused Verification review only if Reliability BLOCKER=0
→ PM final transport-planning acceptance
→ Owner authorization of the first W0 normal attempt
```

Data Quality review remains unnecessary because no product-data semantics are introduced. This report is static planning evidence only. It does not establish PM acceptance, PM handoff completion, Reliability rereview PASS, Verification eligibility, W0/A0/R0/S0/T1/L0 execution, transport, remote load, deployment, activation, runtime-loaded, production-fact, rollback or Git truth.

Counters：

```text
Python executed                         = 0 / NO
Docker action                           = 0 / NO
Archive/workspace mutation              = 0 / NO
SSH/network/remote                      = 0 / NO
Deployment/activation/runtime/rollback  = 0 / NO
Git stage/commit/push/tag/reset/restore = 0 / NO
Task-owned report create                = 1
Other files created or modified         = 0
```

Changed files：task-owned changed/created set is exactly this report; cached diff is empty. Pre-existing PM Rules tracked diff, the authority task, authorized predecessor inputs and unrelated untracked paths remain external, excluded and unchanged. No helper, JSON, archive, workspace, backup, checksum, temporary artifact or second report was created.

Final local checks required by this authority are satisfied after creation: report regular/non-symlink/link=1, size within target/hard maximum, exact two matching conclusion fields, all three PM IDs, all eight Reliability IDs, no provisional wording, exact read ledger, diff checks PASS, cached diff empty and frozen input identities unchanged.

Blockers：none for this Architecture / Integration planning correction; PM acceptance and Reliability rereview remain separate later states.
Recommendations：PM independent intake; if accepted, fresh PM handoff, then focused Reliability rereview; Verification only after Reliability blocker count is zero.
Next gate：`PM Independent Intake — D2-R7B-T0-R3-C1-R1`。

## 10. Final conclusion

结论：PASS WITH RECOMMENDATIONS

