# Sprint 4 D2-R7B-I1 R26 Exact Config-Only Remote Execution

## 1. Task and authority identity

- Report: Sprint 4 D2-R7B-I1 R26 Exact Config-Only Remote Execution
- Task: D2-R7B-I1 R26-R1 — Re-authorized One-Shot Exact Config-Only Remote Deployment After PM Path Repair
- Thread: Architecture / Integration
- Authority ID: PM-R26-R1-260728-0813
- Delivery mode: REPOSITORY_REPORT_WITH_ARTIFACTS
- Conclusion: HOLD
- Previous authority PM-R26-260727-2230 was voided and was not reused.

The new authority was consumed when the single authorized
remote_i1_orchestrator.py --execute parent process started. There was exactly
one parent invocation. No retry, resume, second orchestrator, supplemental
probe, manual postflight, direct helper invocation, rollback, cleanup,
restart, activation, Docker/Compose action, or Git closeout was performed.

## 2. Fresh recovery and pre-mutation gate

Fresh recovery was executed from:

/Users/chenjie/Documents/MES/edge-mes-demo

The live Git facts were:

- branch: main
- HEAD: 8de5edbb504538a233abbcc80102cb714c9cee65
- origin/main: 8de5edbb504538a233abbcc80102cb714c9cee65
- ahead/behind: 0/0
- cached paths: 0
- git diff --check: PASS
- config/mapping.yaml worktree: clean
- HEAD:config/mapping.yaml: b46a637f23c761d0a4c3fe048b3b7480a3dec2ce

The known pre-existing dirty governance inputs (.gitignore,
docs/current_status.md, and docs/thread_handoff/pm_operating_rules.md)
were preserved. Other pre-existing untracked reports, evidence, handoffs,
frontend/cache, management artifacts, and retained stage roots remained
excluded and untouched.

Before authority consumption, all four R26 outputs and the evidence parent
were ABSENT / NON-SYMLINK. No task-owned orchestrator, helper, or SSH
process was active. The effective local SSH configuration was:

- endpoint: mari@10.0.0.217
- port: 22
- identity: ~/.ssh/edge_pi_codex, resolving to
  /Users/chenjie/.ssh/edge_pi_codex
- ControlMaster=false, ControlPersist=no, ForwardAgent=no
- key metadata only: regular non-symlink, owner chenjie, mode 0600

Private-key content was not read, hashed, copied, printed, or persisted.

## 3. Corrected R24, active package, and R25 evidence identities

The corrected R24 inputs matched the frozen authority:

| Path | Bytes | SHA-256 |
|---|---:|---|
| docs/reports/sprint4_d2_r7b_i1_r24_r2_focused_reliability_review.md | 21795 | 0b3a7b34ae546b8dad0554d3fe77a3465720346673286bb85a44b27f1540face |
| docs/reports/sprint4_d2_r7b_i1_r24_r3_focused_verification_review.md | 19774 | 1de905f738292daf00d5bafd47adad49d458df9cee6ca63a9dc810bf3ff4c414 |

The required P2-R2 source identities, P2-R3 source identities, and
config/mapping.yaml identity all matched. Source-byte in-memory compilation
passed for the six persisted Python helpers.

Manifest verification passed:

- P2-R2: 6/6
- P2-R3 composite: 9/9
- R25: 3/3

Each checked manifest was sorted, duplicate-free, and self-excluded.

The R25 durable evidence identities remained unchanged:

- report: 13199 bytes,
  012badd93faad1132d7a714593c64005d79ce34c2d6c4524cabe5a41fc37f149
- preflight.json: 215 bytes,
  9617a68fb0d014db5b5001dd9aaa642ca5ce263ff85283edc3ee0666be701941
- postflight.json: 3162 bytes,
  b1b144ca028673e7e05cd181e537c4478eb527365b6f8b9bb4a48a3fa35333a0
- manifest.sha256: 420 bytes,
  b8dc99f232fbd8b5935abdf1745a7e8bf5668c6061549c89496b72df1e79c9ab

The accepted R25 starting state was confirmed as NO_MUTATION: target
OLD_EXACT at 5935 bytes with SHA-256
86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3,
owner/group mari/mari, mode 0644; upload temp, backup, and rollback temp
were absent. The Collector was running and unchanged. Its frozen identity,
image, mount source/destination/type/RW state, restart count, and
started_at matched; task lifecycle counters were zero.

## 4. Exact invocation and parent result

The only invocation was run from the exact checkout root with a real PTY:

python3 docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py --execute --confirm D2-R7B-I1-CONFIG-ONLY > docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/raw_terminal.ndjson

Parent/orchestrator exit code: 2.

The persisted state machine reached:

LOCAL_SOURCE_GATE -> REMOTE_PREFLIGHT -> REMOTE_UPLOAD -> REMOTE_POSTFLIGHT -> FINAL_TERMINAL

REMOTE_DEPLOY was not started because the upload branch was interrupted.
The remote call count was 3:

| Phase | Exit | Result |
|---|---:|---|
| LOCAL_SOURCE_GATE | 0 | PASS |
| REMOTE_PREFLIGHT | 0 | PASS |
| REMOTE_UPLOAD | 0 | child started and reaped; staged upload observed |
| REMOTE_POSTFLIGHT | 2 | completed read-only postflight; deployment identity not proven |

The authoritative terminal classified the result as:

- status: HOLD_UPLOAD_INTERRUPTED
- phase: REMOTE_UPLOAD
- classification: UPLOAD_STAGED_NO_REPLACEMENT
- message: UPLOAD INTERRUPTED; READ-ONLY POSTFLIGHT COMPLETED
- interruption source: INVALID_CHILD_JSON
- interruption kind: AUTHENTICATION_OR_INTERRUPTION_UNKNOWN
- retry_count: 0
- resume_count: 0
- cleanup_count: 0
- rollback_count: 0
- restart_count_by_task: 0
- activation_count: 0

The postflight child was started and reaped. No deploy, rollback, cleanup,
restart, activation, or lifecycle action followed.

## 5. Raw and authoritative terminal evidence

Raw stdout was preserved byte-for-byte as NDJSON at:

docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/raw_terminal.ndjson

- bytes: 12872
- SHA-256: 4799fc7e9cf27212cd9f696afa40f24c48cf69320bf0700b3ee39b5e7c5be600
- complete JSON records: 1
- invalid JSON records: 0

There was exactly one authoritative candidate: terminal_delivery_attempt=1,
terminal_delivery_authoritative=true, framing NDJSON, delivery status
PRIMARY. It was the unique highest authoritative attempt.

The exact selected object was written without field changes to:

docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/final_terminal.json

- bytes: 12872
- SHA-256: 4799fc7e9cf27212cd9f696afa40f24c48cf69320bf0700b3ee39b5e7c5be600
- semantic equality with the selected raw object: PASS
- terminal status: HOLD_UPLOAD_INTERRUPTED
- terminal phase: REMOTE_UPLOAD
- authoritative attempt: 1

## 6. Observed remote final state

The read-only postflight observed:

- target /opt/edge-mes-demo/config/mapping.yaml:
  OLD_EXACT, 5935 bytes, SHA-256
  86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3,
  owner/group mari/mari, mode 0644, exact realpath true
- upload temp:
  NEW_EXACT, 7112 bytes, SHA-256
  d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d,
  owner/group mari/mari, mode 0644, exact realpath true
- backup: ABSENT
- rollback temp: ABSENT
- Collector: UNCHANGED, running
- Collector restart count: 0
- task lifecycle counters: activation 0, cleanup 0, rollback 0,
  restart-by-task 0

This is a retained staged upload with no target replacement proven. It is not
CONFIG_DEPLOYED_IDENTITY_VERIFIED, and it is not runtime-load, activation,
or production acceptance evidence.

The exact local materializer stage root was retained as required:

/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r2.0mW7V5

It remained a regular directory owned by chenjie with mode 0700 and
contained the materialized config/mapping.yaml only. No cleanup was
authorized or attempted.

## 7. Mutation, process, allowlist, and Git boundary

Authorized mutation-capable phase started: REMOTE_UPLOAD only.
REMOTE_DEPLOY did not start. No unauthorized remote object, process, file,
or lifecycle action was observed. Rollback authority, cleanup authority,
restart authority, activation authority, runtime-load authority, and
Docker/Compose authority were not used.

The exact R26 repository outputs are:

- this durable report
- raw_terminal.ndjson
- final_terminal.json
- manifest.sha256

The evidence parent contains only those three artifacts. No task-owned
orchestrator, helper, or SSH process remained active after terminal emission.
No private-key material, stderr sidecar, exit-code sidecar, alternate parser,
helper copy, extra manifest, or duplicate report was created.

Git closeout was not authorized and was not performed:

- staged: no
- committed: no
- pushed: no
- tagged: no
- HEAD/origin/main: unchanged
- cached index: empty
- git diff --check: PASS

## 8. R26 manifest and delivery boundary

The exact manifest is:

docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/manifest.sha256

It contains exactly three sorted, repository-root-relative, duplicate-free
entries and excludes itself:

docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/final_terminal.json
docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/raw_terminal.ndjson
docs/reports/sprint4_d2_r7b_i1_r26_exact_config_only_remote_execution.md

The manifest was generated after the report and terminal artifacts and was
verified against their final bytes and SHA-256. No other repository path is in
the R26 write allowlist.

## 9. Blocker, recommendation, and next gate

Blocker: upload interruption/invalid child JSON caused the orchestrator to
stop before REMOTE_DEPLOY; postflight proved the target remained old exact
but also observed the exact upload temp as new exact. The result is
HOLD_UPLOAD_INTERRUPTED / UPLOAD_STAGED_NO_REPLACEMENT.

Recommendation: preserve the upload temp, backup absence, rollback-temp
absence, raw terminal, final terminal, and retained stage root for PM-directed
forensics. Do not delete, rename, retry, resume, deploy, or rollback in this
task. Any cleanup or rollback needs separate PM durable intake and new
authority.

The only next gate is:

R26-R1 report/artifacts WRITTEN -> ChatGPT PM durable intake only

This result is MVP-aligned only as a fail-closed exact config-only attempt
record. It does not establish deployed identity, runtime config load,
Collector restart or activation, accepted production facts, production
readiness, Reliability/Verification acceptance, D3, or Git closeout.

## 10. Thread output assessment

- output length: medium
- continue this Thread: no
- open a new Thread for the next action: yes
- reason: R26-R1 authority is one-shot and terminal; the retained staged
  remote state must be handled only through ChatGPT PM durable intake and any
  separately authorized follow-up.
