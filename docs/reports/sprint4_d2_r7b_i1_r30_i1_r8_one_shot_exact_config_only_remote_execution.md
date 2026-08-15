# Sprint 4 D2-R7B-I1 R30-I1-R8 One-Shot Exact Config-Only Remote Execution

## 1. Verdict

`CONFIG_DEPLOYMENT_PASS` / `CONFIG_DEPLOYED_IDENTITY_VERIFIED` / `EXECUTED` / `REMOTE_STATE_OBSERVED` / `WRITTEN`

本报告只建立 exact config file deployment identity 与 backup identity。它不建立 runtime config load、restart、activation、production acceptance 或 accepted-fact 事实。

## 2. Authority and execution boundary

- Task: `D2-R7B-I1 R30-I1-R8`
- Confirmation: `D2-R7B-I1-CONFIG-ONLY`
- Exactly one orchestrator parent was invoked. No retry, resume, second orchestrator, manual SSH, supplemental postflight, cleanup, rollback, restart or activation was performed.
- Exact command:

  ```text
  python3 docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py --execute --confirm D2-R7B-I1-CONFIG-ONLY > docs/reports/evidence/d2_r7b_i1_r30_i1_r8_one_shot_exact_config_only_remote_execution/raw_terminal.ndjson
  ```

- Orchestrator start/end: `2026-07-29T02:45:42Z` / `2026-07-29T02:45:44Z`
- Orchestrator exit: `0`
- One real-TTY gate in the same terminal session: `True`
- Network authority consumed: one orchestrator-owned execution with `REMOTE_CALL_COUNT=4`; no additional network call was made.

## 3. Fresh local pre-execution evidence

Repository root was `/Users/chenjie/Documents/MES/edge-mes-demo` on branch `main`.

- `HEAD=origin/main=1fac3ee567f1108e5a18b155e4133e1fecd50246`
- `HEAD^=63d3cc70e787e0c837079aec0f5924dcbfa6a668`
- Ahead/behind: `0/0`
- Cached diff: empty
- Tracked dirty set: exactly the six pre-existing paths authorized by the prompt; no additional tracked path was written.
- `config/mapping.yaml`: clean relative to HEAD; blob `b46a637f23c761d0a4c3fe048b3b7480a3dec2ce`; 7112 bytes; SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`.
- Initial untracked set: `13775`; canonical `git ls-files --others --exclude-standard -z`, sorted with trailing NUL, SHA-256 `d5edd9bad6a6648c03a55023205cb6b6365b21b49e9baa7a6e554462b399f1d5`.
- Output report, artifact parent and three artifact paths were absent and non-symlink before execution.
- P2-R2 manifest: 6/6, sorted, unique, self-excluded, all referenced hashes matched.
- P2-R3 manifest: 9/9, sorted, unique, self-excluded, all referenced hashes matched.
- Scoped P2-R2/P2-R3 cache: `0 __pycache__`, `0 *.pyc`.
- Bounded task-owned process scan: `0` before execution.
- Protected R30-I1-R5/R6/R7 reports and R30-I1-R7 artifacts matched their frozen bytes/SHA-256 identities.

## 4. Local source, credential and stage-root evidence

The persisted local materializer, orchestrator, phase helpers, tests and manifests matched the frozen package identities. Static checks were limited to `bash -n` for the materializer and `ast.parse(..., mode="exec")` for the persisted Python sources; they were not imported or executed as static checks.

SSH credential inspection was metadata-only: `/Users/chenjie/.ssh/edge_pi_codex` was a regular non-symlink file, uid `501`, mode `0600`. Its contents were not read, hashed, copied, printed or persisted.

The same bare resolution used by the orchestrator was `ssh -G mari@10.0.0.217`:

```text
user mari
hostname 10.0.0.217
port 22
batchmode no
controlmaster false
controlpersist no
identitiesonly yes
identityfile ~/.ssh/edge_pi_codex -> /Users/chenjie/.ssh/edge_pi_codex
forwardagent no
requesttty auto
stricthostkeychecking ask
proxycommand absent
proxyjump absent
```

Historical R26 stage root `/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r2.0mW7V5` remained regular, non-symlink, uid `501`, mode `0700`, realpath-exact and unchanged. Its mapping remained 7112 bytes with SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`. Previously cleaned local paths remained absent.

The orchestrator-created retained stage root was:

```text
/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r2.xb6vyK
```

It was a regular non-symlink directory, uid `501`, mode `0700`, exact system-temp direct child, distinct from the historical root, and was not cleaned. Its only entries were `config/` and `config/mapping.yaml`; the staged mapping was regular non-symlink, uid `501`, mode `0600`, 7112 bytes, SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`.

## 5. Execution and phase evidence

- Phase order: `LOCAL_SOURCE_GATE` → `REMOTE_PREFLIGHT` → `REMOTE_UPLOAD` → `REMOTE_DEPLOY` → `REMOTE_POSTFLIGHT` → `FINAL_TERMINAL`.
- Phase exit codes: all five executed phases `0`.
- Last owned child PID: `55330`; started, reaped, return code `0`, no signal.
- `postflight_attempted=true`, `postflight_call_count=1`, `postflight_completed=true`.
- `retry_count=0`, `resume_count=0`, `rollback_count=0`, `cleanup_count=0`, `restart_count_by_task=0`, `activation_count=0`.
- Terminal delivery: one authoritative `PRIMARY` attempt, NDJSON framing, no fallback, no interruption, no partial prefix.

## 6. Remote final state

Target `/opt/edge-mes-demo/config/mapping.yaml`:

```text
state: NEW_EXACT
bytes: 7112
sha256: d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
device/inode: 2050/550822
owner/group/mode: mari/mari/0644
exact_realpath: true
```

The pre-execution target was OLD_EXACT, 5935 bytes, SHA-256 `86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3`, device/inode `2050/550698`. The retained backup was:

```text
state: OLD_EXACT
path: /opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml
bytes: 5935
sha256: 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3
device/inode: 2050/550916
owner/group/mode: mari/mari/0644
```

The upload temp was `ABSENT`; rollback temp was `ABSENT`. Collector was `UNCHANGED`: ID `5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524`, image `sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a`, running `true`, restart count `0`, started at `2026-07-23T12:23:25.959624Z`, and bind `/opt/edge-mes-demo/config` → `/app/config`, `rw=false`.

## 7. Raw and final terminal evidence

- `raw_terminal.ndjson`: one non-empty line, one valid JSON record, zero invalid/partial lines; 13025 bytes; SHA-256 `f2baa8ca164341286411efea601f94fa4c8d636f2a8ae9c10cbcf2701decf5b0`.
- `final_terminal.json`: exact selected authoritative raw line with exact same 13025-byte identity and SHA-256.
- Terminal status: `CONFIG_DEPLOYED_IDENTITY_VERIFIED`.
- Terminal classification: `DEPLOYED_IDENTITY_VERIFIED`.
- Terminal message: `RUNTIME CONFIG LOAD NOT CLAIMED`.

## 8. Final repository evidence and artifact closure

Post-execution local audit passed: protected package/helper/manifest/mapping identities were unchanged; `HEAD`, `origin/main`, ahead/behind, cached state and exact six-path tracked dirty set were unchanged; scoped cache remained zero; bounded task-owned process count was zero; historical root and prior cleanup paths remained safe.

After raw and final artifacts, before this report and manifest, untracked state was `13777` with SHA-256 `99838dd421a7738645ef2487cbc7775b33641f83794958bbbc0314a61e90e451`. With exactly this report and the three authorized artifacts, the final untracked set is `13779` with SHA-256 `b164e7ef38abfb09be41e079cf6f8139f2f3aa2ef698a92b95ab3157d1af6aa8`.

The exact artifact parent contains only:

```text
docs/reports/evidence/d2_r7b_i1_r30_i1_r8_one_shot_exact_config_only_remote_execution/raw_terminal.ndjson
docs/reports/evidence/d2_r7b_i1_r30_i1_r8_one_shot_exact_config_only_remote_execution/final_terminal.json
docs/reports/evidence/d2_r7b_i1_r30_i1_r8_one_shot_exact_config_only_remote_execution/manifest.sha256
```

The manifest is self-excluded and records these three artifact paths after their final writes. The report is the separate exact report path; its final identity is delivered by the manifest rather than embedded here to avoid self-referential mutation.

## 9. Evidence boundary and next authority

Established: exact config file deployment identity, retained backup identity, four-call execution identity, unchanged Collector identity, and absence of lifecycle/cleanup/rollback actions.

Not established: runtime-loaded config, restart, activation, production runtime behavior, production accepted station event, data quality, or PM acceptance. The terminal's next authority is `PM intake -> focused Reliability final re-review`.
