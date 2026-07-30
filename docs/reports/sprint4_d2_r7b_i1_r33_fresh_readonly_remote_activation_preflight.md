# Sprint 4 D2-R7B-I1 R33 Fresh Read-Only Remote Activation Preflight

## Report identity

- Task: D2-R7B-I1 R33 — Freshly Observe the Loaded Package-Closed Collector Image, Current Collector Prestate, Compatibility Alias, Protected Services, Config Filesystem State and Exact Rollback Candidate Before Any Activation
- Executing Thread: Architecture / Integration
- Authority: `PM-D2-R7B-I1-R33-FRESH-READONLY-REMOTE-ACTIVATION-PREFLIGHT-260729-2001`
- Delivery mode: `REPOSITORY_REPORT_WITH_ARTIFACTS`
- Conclusion: `PASS`
- Terminal classification: `ACTIVATION_ELIGIBLE`

## Scope and authority boundary

This task performed one freshly authorized, structured, read-only SSH observation only. It created exactly this report and the five declared artifacts. It did not perform Docker tag/retag, image load/save/pull/build/remove, Docker Compose, container lifecycle, filesystem mutation, cleanup, rollback, API/DB/PLC interaction, Git stage/commit/push/tag, or a second SSH call.

`ACTIVATION_ELIGIBLE` is a point-in-time preflight conclusion only. It does not establish `ACTIVATED`, `RUNTIME-LOADED`, or `PRODUCTION-ACCEPTED`.

## Fresh local prerequisite

The live checkout matched the frozen authority baseline: root `/Users/chenjie/Documents/MES/edge-mes-demo`, branch `main`, `HEAD` and `origin/main` `ac33e6bae449ecdd9b77a53daaf7271f14133000`, parent `66563677d3d1129fbc79c2c284b5f6d8b62f1932`, and ahead/behind `0/0`. The cached index was empty; both diff checks passed; `config/mapping.yaml` was clean relative to `HEAD`.

The six expected pre-existing tracked dirty paths remained exactly excluded: `.gitignore`, the two P2-R2 artifacts, the two P2-R3 artifacts, and `docs/thread_handoff/pm_operating_rules.md`. All frozen authority inputs—including untracked R31—were regular non-symlink files with their required byte identities. The SSH private key was checked only as metadata: regular non-symlink, uid `501`, mode `0600`. Before runner launch, no R33-owned runner, probe, or authority process existed.

The persisted runner and probe passed AST parsing without bytecode generation. Their identities before and after the one execution were unchanged; final identities are recorded in the local terminal.

## Fresh remote observation

The sole SSH child exited `0`; stdout was `35092` bytes, stderr was `0` bytes. Strict UTF-8 decoding, JSON parsing, and the remote terminal schema validation passed. The remote probe executed `10` Docker read commands, within the maximum `11`, and its remote mutation audit counters were all zero.

The freshly loaded package-closed object `sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734` exists as `linux/arm64`. `edge-mes-demo-collector:r32-pkg-closed-ca68dd4` resolves exactly to it. The compatibility alias `edge-mes-demo-collector:latest` resolves exactly to the safe rollback image `sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a`; it points neither to the fresh nor known-bad image. The known-bad image does not own either protected tag. No running container uses the fresh image.

The Compose-labelled Collector was exactly one container, `/edge-mes-collector`, on the old safe image with `Config.Image` `edge-mes-demo-collector`. Both snapshots retained the same ID, image, `StartedAt`, restart count `0`, running/non-restarting/non-dead state, `unless-stopped` policy, and exact read-only bind mount `/opt/edge-mes-demo/config` to `/app/config`. The core protected services (`postgres`, `simulator`, `s7-plc-sim`, `api`) were exactly one each, running and stable. Every discovered protected service retained identical hard fields between snapshot A and snapshot B; no unexpected project service or duplicate ownership was observed.

The remote config parent was the expected non-symlink `mari:mari` `0775` directory. `mapping.yaml` was the exact new mapping (`7112` bytes, SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`), and the retained backup was the exact old rollback candidate (`5935` bytes, SHA-256 `86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3`). Both no-follow reads were identity-stable and used distinct inodes. The upload and rollback temporary paths were absent. The exact matching sidecar set contained only the retained backup.

## Evidence classification

- Historical accepted evidence: `IMAGE_LOADED_EXACT` and the frozen image identities from the named R32/R31 evidence.
- Fresh local prerequisite: the R33 local terminal records current Git, authority-input, output, process, key-metadata, helper-syntax, and helper-identity checks.
- Fresh remote observation: the R33 remote terminal records parsed one-call Docker/filesystem observations and snapshot comparisons.
- Diagnostic-only fields: image Created/Cmd/WorkingDir/Env/RootFS, `Config.Image`, and complete mount tuples are retained as diagnostic observations.
- Eligibility assertion: `ACTIVATION_ELIGIBLE`.
- Activation/runtime/production state: not observed or established by this task.

## Durable artifacts and validation

The report and exactly five manifest entries were written. The manifest is repository-root-relative, sorted, unique, and self-excluded. Verification is recorded as `5/5 OK`. Final Git audit confirms an empty index and unchanged tracked dirty set; no Git action occurred.

## Next gate and MVP alignment

The only next gate is `R33 report and artifacts WRITTEN -> ChatGPT PM durable intake only`. A new, explicit authority is required before any compatibility-alias mutation, Collector-only activation, post-activation validation, rollback, runtime-loaded validation, production validation, or Git action.

- Approved MVP claim: a package-closed image may be considered for separately authorized activation only after a fresh safe preflight.
- Minimum invariant: exact fresh image, safe old active Collector and rollback image, stable protected services, stable config identity, and no remote mutation.
- Scope expansion: none.
- Task inflation: none.
- Classification: `MVP-ALIGNED`.
