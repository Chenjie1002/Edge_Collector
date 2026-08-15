# Sprint 4 D2-R7B-I1 R30-I1-R10-R2-R1 Focused RestartCount Schema Correction and Read-Only Confirmation

## Conclusion

```text
RESTARTCOUNT_CONFIRMATION_PASS
RESTARTCOUNT_SCHEMA_CORRECTED_AND_OBSERVED
RESTARTCOUNT_ZERO_STABLE
WRITTEN
```

The prior R10-R2 source contract defect is confirmed: it obtained `RestartCount` from `$.State.RestartCount`, which is not Docker's container-inspect field. This observer obtained the actual value from the top-level `$.RestartCount` in two complete inspect objects. Both values were integer `0`, and the bounded lifecycle tuple was unchanged across the exact six-second interval.

This establishes no Docker restart-count evidence since creation of the currently observed container and current bounded lifecycle stability. It does not establish runtime-loaded mapping, Collector health, production health, root cause, or an absence of interruptions before this container existed.

## Authority, scope, and stop rule

```text
Authority: PM-R30-I1-R10-R2-R1-260729-FOCUSED-RESTARTCOUNT-CORRECTION-01
Thread: Architecture / Integration
Delivery: REPOSITORY_REPORT_WITH_ARTIFACTS
SSH parent / observer execution / retry / resume: 1 / 1 / 0 / 0
Docker operation: inspect only, exactly 2
Wait: exactly 1 × 6 seconds
Remote mutation, restart, rollback, cleanup, logs, events: 0 / 0 / 0 / 0 / 0 / 0
```

Only the report and four declared artifacts were created. No source, test, product, config, prior evidence, Git index, commit, or remote lifecycle surface was modified. The stopping rule was applied immediately after persisting the second valid top-level integer and classifying stability.

## Corrected observer contract and local gates

```text
Old path:     $.State.RestartCount
Correct path: $.RestartCount
Runtime source: TOP_LEVEL_CONTAINER_OBJECT
```

The persisted observer is standard-library-only; its Docker command is the fixed list `/usr/bin/docker --host unix:///var/run/docker.sock inspect edge-mes-collector`, with `shell=False`. Static AST/compile audit passed:

```text
observer bytes/SHA-256: 12386 / 3450f2e7845a79f8077e4f9c24e6258a26d9f86f715a3a16ec675c5d0dd01aa8
AST parse / compile: PASS / PASS
subprocess.run call sites / shell=True: 1 / 0
inspect helper call sites: 2
terminal stdout write sites: 1
top-level raw.get("RestartCount") / State RestartCount reads: 1 / 0
filesystem write calls / retry-resume loops: 0 / 0
```

Fresh local recovery matched the required `main` baseline: HEAD and `origin/main` were both `1fac3ee567f1108e5a18b155e4133e1fecd50246`, parent `63d3cc70e787e0c837079aec0f5924dcbfa6a668`, ahead/behind `0/0`, cached index empty, and the only pre-existing tracked dirty paths were `.gitignore`, the two P2 manifests, `local_materialization.sh`, `remote_i1_orchestrator.py`, and `docs/thread_handoff/pm_operating_rules.md`. The output paths were absent and non-symlink before creation; the task-process gate was zero; the scoped P2 cache count was zero; P2-R2 and P2-R3 manifests verified `6/6` and `9/9` respectively. The SSH key metadata was regular, non-symlink, uid 501, mode 0600; the resolved endpoint was `mari@10.0.0.217:22` with the exact identity file and no proxy configuration.

Prior R10-R2 report/artifact identities were rechecked unchanged, including its report SHA-256 `9509336399b33fd65abf2abc267ce2ff8e4401dc147146207214e46d2d17af7f`, observer SHA-256 `6e3b69d37f5b63b3dad2bfa6d3c0597080dd7ed7ca611a0873baa60760dea9a2`, raw/final SHA-256 `bf3e535b75e06c8fbcf7f36fa4b1afaa078fddec40d362e375fb07eb2827e41f`, and manifest SHA-256 `463c59aa724e5ef6304bf9085160c8879782ccac9183075442b601e4fa5bae2a`.

## Authoritative remote observation

The raw terminal is one complete NDJSON record and the final terminal is its byte-identical selected line. Both samples contain `restart_count_source=TOP_LEVEL_CONTAINER_OBJECT`, `restart_count_json_path=$.RestartCount`, and `restart_count_type=int`.

| Field | Sample 1 | Sample 2 |
| --- | --- | --- |
| Observation UTC | 2026-07-29T06:01:18.083Z | 2026-07-29T06:01:24.096Z |
| Container ID | `5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524` | same |
| Image | `sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a` | same |
| Created / StartedAt | 2026-07-23T12:23:25.124184859Z / 2026-07-23T12:23:25.959624Z | same |
| PID / status | 3365014 / running | same |
| Top-level RestartCount | 0 (`int`) | 0 (`int`) |
| Running / Restarting / Dead | true / false / false | same |
| ExitCode / OOMKilled / Error | 0 / false / empty | same |
| Restart policy | unless-stopped, maximum retry 0 | same |
| `/app/config` mount | bind `/opt/edge-mes-demo/config`, read-only | same |

All compared lifecycle fields were unchanged: `Id`, `Image`, `Created`, `StartedAt`, `FinishedAt`, `Status`, `Running`, `Restarting`, `Dead`, `Pid`, `ExitCode`, `Error`, `OOMKilled`, `RestartCount`, restart policy, and `/app/config` mount. Both samples also match the retained historical identity and timestamps. The lifecycle finding is therefore `RESTARTCOUNT_ZERO_STABLE`.

## Evidence boundary, final controls, and next gate

Facts established by this task are limited to the actual current Docker restart count and the bounded six-second stability tuple. The task does not establish `CONFIG_RUNTIME_LOADED`, `COLLECTOR_HEALTH_ACCEPTED`, `RESTARTED`, `ROLLED_BACK`, `NEW_IMAGE_ACTIVATED`, or `PRODUCTION_ACCEPTED`; it does not infer an underlying cause from the zero count.

The raw terminal counters prove no logs, events, Docker exec, remote write, restart, rollback, cleanup, retry, or resume. `manual_action_required` is false. Git staging, commit, push, and tag actions were not authorized or performed.

MVP alignment remains `MVP-ALIGNED WITH BACKLOG ITEMS`: the approved deliverable was the actual `RestartCount` and present lifecycle stability; it adds no product capability and does not inflate the diagnosis scope. Any runtime reload, restart, mutation, root-cause forensics, or production claim requires a separate authority.

The only next gate is ChatGPT PM durable intake. This PASS does not transfer restart, rollback, recovery, logs/events, image/config action, runtime validation, production acceptance, cleanup, or Git authority.
