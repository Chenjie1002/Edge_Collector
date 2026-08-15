# Sprint 4 D2-R7B-I1 R30-I1-R10-R1 Corrected Existing-Image Controlled Collector Restart Runtime Validation

## Verdict

**HOLD — `REMOTE_PRESTATE_MISMATCH`**

唯一一次授权 SSH 已完成。远端控制器在 `REMOTE_PREFLIGHT` 发现冻结前置条件不成立：Collector `restart_count` 不等于要求的 `0`。控制器在正常重启之前停止；本任务未执行 Collector restart、rollback 或 recovery restart。

## Authority and claim boundary

- Task: `D2-R7B-I1-R30-I1-R10-R1`。
- Checkout: `/Users/chenjie/Documents/MES/edge-mes-demo`。
- Endpoint: `mari@10.0.0.217`；固定 host `Pi-5b-Li`、principal `mari`、Docker socket `unix:///var/run/docker.sock`。
- SSH parent count: `1`；controller execution count: `1`；retry/resume: `0/0`。
- Frozen Collector: container `5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524`，service `collector`，project `edge-mes-demo`，expected existing image `sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a`。
- Authorized mutation path, if preflight had passed, was only the existing-image runtime config reload. This task never reached that path, so it establishes no `EXISTING_IMAGE_RUNTIME_CONFIG_LOADED`, package-closed new Collector activation, accepted-fact runtime, production fact, deployment, or acceptance claim.
- No Compose, build, pull, tag, remove, prune, recreate, manual SSH, second SSH, retry, resume, Git stage, commit, push, or tag was performed.

## Corrected preflight evidence

The historical R10 report was preserved unchanged: `9593` bytes, SHA-256 `92595578a084e07429c508b5a1d0cce8608e276a233a06752ad0cb26320d7713`. Its old evidence parent remained a regular non-symlink empty directory, and its controller/evidence artifacts remained absent before this task.

- Corrected process gate: direct `/bin/ps -axo pid=,ppid=,command=`; exit `0`; stderr empty; `1058` parsed records; `0` parse errors; full scanner ancestor chain and scanner `ps` child excluded; task-token matches `0`.
- Corrected cache gate: only `docs/reports/evidence/d2_r7b_p2_r2` and `docs/reports/evidence/d2_r7b_p2_r3` were in scope; both had `0` `__pycache__` directories and `0` `*.pyc` files. P2-R2 manifest verification was `6/6 OK`; P2-R3 was `9/9 OK`. Collector, tests, common, `.venv`, and repo-wide caches were excluded and non-blocking.
- SSH key metadata: `/Users/chenjie/.ssh/edge_pi_codex` regular non-symlink, uid `501`, mode `0600`; `ssh -T -G -F /dev/null` resolved user `mari`, host `10.0.0.217`, port `22`, and the exact identity file, with no proxy command/jump configured.
- Stage roots were regular non-symlink directories with the expected ownership/modes; each nested `config/mapping.yaml` was `7112` bytes, SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`.
- `config/mapping.yaml` was clean relative to `HEAD`; expected blob `b46a637f23c761d0a4c3fe048b3b7480a3dec2ce`, `7112` bytes, SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`. Runtime config hash: `0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38`; schema `runtime-mapping/v1`; version `2026.06.26-slice-a`; line `LINE_001`; stations `WS01/WS02/WS03`; plan count `4`.
- Fresh Git baseline before controller creation: branch `main`; `HEAD=origin/main=1fac3ee567f1108e5a18b155e4133e1fecd50246`; ahead/behind `0/0`; cached diff empty; `git diff --check` and cached check passed. The six pre-existing tracked dirty artifacts were preserved and excluded from this task: `.gitignore`, `docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh`, `docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256`, `docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256`, `docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py`, and `docs/thread_handoff/pm_operating_rules.md`. Pre-task untracked-set count/digest: `13781` / `595f85aa114743b85797a625b7147e2ef4cea3862637c58baabb33312335784e`.

## Controller identity and static audit

Controller: `docs/reports/evidence/d2_r7b_i1_r30_i1_r10_r1_corrected_controlled_collector_restart_runtime_validation/runtime_controller.py`; `50012` bytes; SHA-256 `4d21b637a0b30a335bb0ef904847743706e7344b39e305f141a060da4fbdb668`.

Static audit passed after the startup-marker comparison correction: AST parse and compile passed; one `subprocess.run` call with a validated `list[str]` and `shell=False`; Docker verbs were limited to `inspect`, `exec`, `logs`, and `restart`; no Compose/build/pull/tag/remove/prune command path; signal handlers covered `SIGHUP`, `SIGINT`, and `SIGTERM`; terminal stdout was one JSON write followed by flush. The embedded rollback helper was decoded and verified as `13248` bytes, SHA-256 `e2690ef991827ad8107430ee0449be913afa65dbf166fe2c1cf19fec0b7736ff`, compiled as namespace `__name__="r10_r1_remote_rollback"`, and was not called because preflight failed.

## Remote terminal result

SSH process exit: `2` (controller HOLD). The persisted terminal was exactly one complete NDJSON line:

```json
{"body":{"error":"collector prestate mismatch: restart_count"},"classification":"REMOTE_PRESTATE_MISMATCH","conclusion":"RUNTIME_RELOAD_HOLD","controller_execution_count":1,"interrupt_signal":null,"manual_action_required":false,"message":"collector prestate mismatch: restart_count","normal_restart_count":0,"phase":"REMOTE_PREFLIGHT","recovery_restart_count":0,"remote_command_count":2,"resume_count":0,"retry_count":0,"rollback_count":0,"ssh_parent_count":1,"status":"HOLD","task":"D2-R7B-I1-R30-I1-R10-R1"}
```

The controller emitted no structured `prestate` or `pre_probe` because the frozen Collector prestate gate failed before those records were committed. `remote_command_count=2` is the controller-observed preflight command count. There was no normal restart (`0`), no rollback (`0`), and no recovery restart (`0`).

## Historical/source context retained for the boundary

Expected current source identities were retained for later independent comparison: `main.py` SHA-256 `a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090`; `config.py` `4f01689a34fb494f7ea84cf74b303ce8aed0957d1dd9c05fc7773563cd577afc`; `mapping.py` `c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098`; `event_collector.py` `eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f`; `resolved_config_registry.py` `1844449a3f99e9ca53bddc8063c151fb0f889920597bccb170f5e62f3715db2c`.

The existing-image compatibility profile remained a boundary only: `/app/app/main.py` expected `a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090`; `/app/app/services/event_collector.py` expected `ee1a4267af0633db2b5a8c4163d760bb8d37093b3b84405d14c226f89303184d`; `/app/app/services/accepted_station_event_fact.py` expected `ABSENT`; `/app/app/services/storage.py` expected `c620c30641cff25a535cdc067df316ab4c66f73b75f34447898823f60b7396c0`. The compatibility probe was not reached.

## Evidence manifest and next gate

- Raw terminal: `raw_terminal.ndjson`, `572` bytes, SHA-256 `6fa6f8541b9a260446aa596e8260b03a419552e2f38e56ff0369ee2ffbf6a83a`.
- Final terminal: `final_terminal.json` is a byte-for-byte copy of the selected raw terminal line; identity is the same `572` bytes and SHA-256 `6fa6f8541b9a260446aa596e8260b03a419552e2f38e56ff0369ee2ffbf6a83a`.
- The controller, raw terminal, final terminal, this report, and `manifest.sha256` are the only newly authorized paths. The manifest binds exactly these four report/evidence artifacts and excludes itself.
- This is a terminal HOLD, not a retryable in-task state. PM/Owner review must resolve the `restart_count` mismatch and issue a fresh frozen prestate/authorization before any future runtime action. No manual SSH or continuation is authorized by this report.
