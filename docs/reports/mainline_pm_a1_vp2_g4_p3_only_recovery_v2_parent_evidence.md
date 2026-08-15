# A1-VP2-G4-P3-ONLY-RECOVERY-V2 Parent Evidence

## 1. Report identity

```text
REPORT_NAME=A1-VP2-G4-P3-ONLY-RECOVERY-V2_PARENT_EVIDENCE
REPORT_PATH=docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v2_parent_evidence.md
GOAL=A1-VP2-G4-P3-ONLY-RECOVERY-V2
EXECUTING_THREAD=Owner-started Goal Controller / Mainline intake boundary
CONCLUSION=PASS / P3_ONLY_RECOVERY_V2_RUNTIME_SMOKE_AND_CLEANUP_COMPLETE
PARENT_EVIDENCE_STATE=WRITTEN
OWNER_EVIDENCE_INDEPENDENT_INTAKE=PASS
```

本报告只接受已经完成的 Owner-assisted external one-shot durable evidence；Goal Controller
没有重新执行 runner、continuity、tunnel、standalone、HTTP 或任何 remote/runtime action。
本报告不是 Mainline G4 acceptance、Goal Closeout、G5、A1-S2、visual acceptance 或 Skill
authority。

## 2. Owner evidence identity

三份 evidence 在读取内容前已机械核验为 regular / non-symlink、未 ignored、未 indexed，
并在 stdout → stderr → result 顺序完整读取到 EOF：

| Evidence | bytes | SHA-256 |
| --- | ---: | --- |
| `docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v2_owner_terminal_stdout.txt` | 2513 | `d86fe4160b930d00d36ddbe072b2b93c301d3a5f6a72bd578c26738652f325b1` |
| `docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v2_owner_terminal_stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v2_owner_terminal_result.txt` | 1861 | `428e4a998acae739bf1cfed115939539f3850aa7b6e42f8cc66694526a60a6e1` |

Result-recorded stdout/stderr paths, bytes and SHA-256 exactly equal the actual files. stderr is
an empty regular file; no hidden diagnostic output was accepted.

## 3. Frozen V2 authority binding

The frozen V2 package identities were rechecked before Owner evidence intake:

| Object | bytes | SHA-256 |
| --- | ---: | --- |
| `docs/thread_handoff/mainline_pm_a1_vp2_g4_p3_only_recovery_v2_goal_prompt.md` | 13970 | `d7faf5ddc638d9150efed2163b2a7b77c3c7e6412513412ba8e9da3b93cc60fc` |
| `docs/thread_handoff/mainline_pm_a1_vp2_g4_p3_only_recovery_v2_charter.md` | 13500 | `eda545b3c735a1d90910fb2c18eb00d45ea16311c0efb1965555e8a643373c05` |
| `docs/thread_handoff/mainline_pm_a1_vp2_g4_p3_only_recovery_v2_owner_terminal_runner.zsh` | 27926 | `3e51f9692b4e2ffe5bc17133829b62e9974f604f0b746146e00bc57d340b83d4` |
| `docs/thread_handoff/mainline_pm_a1_vp2_g4_committed_runtime_preparation_v5_local_bootstrap_probe.sh` | 4631 | `d805d7f797e2b12ac3e67398d3b9e7efe3bafbfc4e344068925687e2c9a15821` |
| `docs/reports/mainline_pm_a1_vp2_g4_v6_parent_independent_intake_20260813T2202CST.md` | 7152 | `182d37c123f3ff763ccb96047b11f46e01b0496264d53b03001df0de0c2100b2` |
| `docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v1_parent_independent_intake_20260813T2242CST.md` | 4338 | `49af5fd44ca55c69d69d97ee3ff71f4c541380015675b7491d1d7a2c30885378` |
| `docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v1_orphan_cleanup_20260813T2252CST.md` | 2853 | `3d5e59ad3a9125b7e609003d0a838449feccf49a204c60b886a00b04b16e505f` |
| `frontend/.next/standalone/server.js` | 7076 | `ad9b19004dcd986a44734acc5c3d41e40d139aac202f65793c821f917644b6d9` |
| `docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v2_ledger.md` | 12115 | `59a40364f905b743aefd52406a7da5368bbc20aa4cd0d309203f34ea9450482f` |

`frontend/.next/standalone/.next/static` was rechecked as a present non-symlink directory.

## 4. Repository and candidate continuity

The Owner result binds the execution to the same frozen local baseline and accepted V6
candidate; current local Git facts independently match:

```text
PROJECT_ROOT=/Users/chenjie/Documents/MES/edge-mes-demo
HEAD=2530721080e4fdcf9ff1e806e06969aa56affdf5
ORIGIN_MAIN=2530721080e4fdcf9ff1e806e06969aa56affdf5
HEAD_API_TREE=ffddc637e50e180021116069eb9930c066a37084
ACCEPTED_V6_INTAKE_BYTES=7152
ACCEPTED_V6_INTAKE_SHA256=182d37c123f3ff763ccb96047b11f46e01b0496264d53b03001df0de0c2100b2
V1_MAINLINE_INTAKE_BYTES=4338
V1_MAINLINE_INTAKE_SHA256=49af5fd44ca55c69d69d97ee3ff71f4c541380015675b7491d1d7a2c30885378
V1_ORPHAN_CLEANUP_BYTES=2853
V1_ORPHAN_CLEANUP_SHA256=3d5e59ad3a9125b7e609003d0a838449feccf49a204c60b886a00b04b16e505f
EXPECTED_CANDIDATE_IMAGE=sha256:45938b8e826237bb4c6c595ddecf9f5d28e2709f39710bed905944ef33afe9e0
STANDALONE_SERVER_BYTES=7076
STANDALONE_SERVER_SHA256=ad9b19004dcd986a44734acc5c3d41e40d139aac202f65793c821f917644b6d9
```

The accepted V6 P2 runtime is reused as a bounded factual sub-result. This evidence does not
claim a new deployment, rebuild, image mutation or production acceptance.

## 5. Fresh Owner continuity evidence

The actual Owner stdout and result agree on one read-only continuity SSH role:

```text
CONTINUITY_SSH_ATTEMPTS=1
CONTINUITY_SSH_RC=0
P3R2:CONTINUITY:CONTAINER=image_id=sha256:45938b8e826237bb4c6c595ddecf9f5d28e2709f39710bed905944ef33afe9e0;status=running;running=true
P3R2:CONTINUITY:IMAGE=id=sha256:45938b8e826237bb4c6c595ddecf9f5d28e2709f39710bed905944ef33afe9e0;os=linux;arch=arm64;variant=v8
P3R2:CONTINUITY:HEALTH={"status":"ok"}
P3R2:CONTINUITY=PASS / ACCEPTED_V6_CANDIDATE_IMAGE_AND_HEALTH
```

No second SSH, deployment, Docker mutation, protected service inspection, business GET, DB/SQL
or runtime repair was accepted by this intake.

## 6. Ownership correction evidence

The corrected ownership verifier is independently bound across result and stdout to the same
exact child process provenance:

```text
OWNERSHIP_VERIFIER_VERSION=P3R_V2_PID_LISTENER_EXE_CWD_LSTART
STANDALONE_PID=35424
STANDALONE_LSTART_BOUND=四 8月/13 23:20:43 2026
STANDALONE_OWNERSHIP_PASS=YES
P3R2:STANDALONE_OWNERSHIP=PASS|pid=35424|lstart=四 8月/13 23:20:43 2026|exe=/usr/local/bin/node|cwd=/Users/chenjie/Documents/MES/edge-mes-demo/frontend/.next/standalone|listener=127.0.0.1:3101
```

This proves the required exact `$!` PID binding, lstart continuity, resolved Node executable,
standalone cwd, unique listener PID and exact `127.0.0.1:3101` ownership as recorded by the
Owner runner. Mutable process title/command text is not used as the standalone ownership
predicate.

## 7. One-shot budget reconciliation

```text
TUNNEL_START_ATTEMPTS=1
STANDALONE_START_ATTEMPTS=1
RETRY=0
P3R2:STANDALONE_START_RETRY=FORBIDDEN
STANDALONE_EXECUTION_VENUE=OWNER_NORMAL_MACOS_TERMINAL
```

The Owner result records one tunnel and one standalone only. The Goal Controller did not consume
any additional attempt.

## 8. Ordered P3 smoke evidence

The Owner stdout records the required ordered smoke sequence and the result file records each
counter exactly once:

```text
TUNNEL_HEALTH_GET=1
SCOPE_OPTIONS_GET=1
FRONTEND_HEALTH_GET=1
IDLE_STATION_SUMMARY_GET=1
P3R2:TUNNEL_HEALTH_HTTP=200
P3R2:TUNNEL_HEALTH_BODY={"status":"ok"}
P3R2:SCOPE_HTTP=200
P3R2:SCOPE_TOPOLOGY=[{"line_id":"LINE_001","station_ids":["WS01","WS02","WS03"]}]
P3R2:FRONTEND_HEALTH_HTTP=200
P3R2:FRONTEND_HEALTH_BODY={"status":"ok","service":"dashboard"}
P3R2:IDLE_HTTP=200
P3R2:IDLE_MARKERS=PASS
```

The recorded request order is tunnel health, tunneled scope-options, frontend health and idle
Station Summary. The accepted scope topology is real `LINE_001` with `WS01`, `WS02`, `WS03`.

## 9. Business-query and idle boundary

```text
QUALITY_BUSINESS_GET=0
TRACE_BUSINESS_GET=0
PROCESS_METRICS_BUSINESS_GET=0
P3R2:COUNTER:QUALITY_BUSINESS_GET=0
P3R2:COUNTER:TRACE_BUSINESS_GET=0
P3R2:COUNTER:PROCESS_METRICS_BUSINESS_GET=0
```

The Owner evidence contains no Quality, Trace or Process Metrics business GET. The idle page
markers passed without a line/station/start/end query submission. No KPI value or Full OEE claim
is made here.

## 10. Exact cleanup evidence

```text
STANDALONE_TERM=1
STANDALONE_KILL=0
TUNNEL_TERM=1
TUNNEL_KILL=0
CLEANUP_PASS=YES
P3R2:CLEANUP:STANDALONE_TERM=1
P3R2:CLEANUP:STANDALONE_KILL=0
P3R2:CLEANUP:TUNNEL_TERM=1
P3R2:CLEANUP:TUNNEL_KILL=0
P3R2:CLEANUP:PORT_8000=NO_LISTENER
P3R2:CLEANUP:PORT_3101=NO_LISTENER
```

The Owner evidence records reverse-order owned cleanup. No foreign or unproven PID was signalled;
the Goal Controller has performed no signal or cleanup action.

## 11. Independent intake result

The Goal Controller performed a separate local mechanical reconciliation, not a copy of the
runner terminal string:

- verified all actual Owner file identities and result-recorded hashes;
- verified exact authority bindings and current HEAD/API tree;
- verified one terminal and no contradictory terminal;
- verified PID/lstart/Node/cwd/listener binding across result and stdout;
- verified one-shot counters, four ordered smoke counters, zero business counters, and cleanup;
- verified Parent Evidence and Closeout were absent before this report write;
- used no network, SSH, HTTP, Node, npm, Docker, DB, process signal or Git mutation。

```text
OWNER_EVIDENCE_INDEPENDENT_INTAKE=PASS
OWNER_RUNTIME_TERMINAL=PASS / P3_ONLY_RECOVERY_V2_RUNTIME_SMOKE_AND_CLEANUP_COMPLETE
```

## 12. State separation and next gate

```text
OWNER_EVIDENCE=WRITTEN / PASS
OWNER_EVIDENCE_ACCEPTED_BY_THIS_INTAKE=YES
PARENT_EVIDENCE=WRITTEN / PASS
FINAL_VERIFICATION=NOT_YET_CREATED
CLOSEOUT=NOT_YET_CREATED
G4_MAINLINE_ACCEPTANCE=NOT_DONE
PRODUCTION_ACCEPTED=NO
OWNER_VISUAL_ACCEPTED=NO
VP2_G5_AUTHORIZED=NO
A1_S2_AUTHORIZED=NO
```

This Parent Evidence authorizes only the next exact local step: one fresh PM-Rules-compliant
16-section local-only Verification child. It does not authorize a second runtime attempt,
Closeout creation before that child, G5, visual acceptance, A1-S2 or Skill work.

## 13. MVP 路径一致性

```text
MVP_CLASSIFICATION=MVP-ALIGNED
MVP_DELIVERABLE=可信 Station Summary scope interaction 的最小安全 P3 runtime smoke、ownership 与 cleanup boundary
NEW_PRODUCT_CAPABILITY=NO
NEW_RUNTIME_TOPOLOGY=NO
NEW_EVIDENCE_SUBSYSTEM=NO
SCOPE_DRIFT=NO
```

This Parent Evidence preserves accepted-fact/runtime state separation and prevents false PASS,
unowned process contamination, foreign PID signalling and synthetic production claims. It adds
no product capability or broader audit subsystem.

## 14. Durable delivery state

```text
WRITTEN=YES
REVIEWED=NO_INDEPENDENT_REVIEW_YET
ACCEPTED=NO_MAINLINE_PM_ACCEPTANCE_YET
VERIFIED=NO_FINAL_VERIFICATION_YET
STAGED=NO
COMMITTED=NO
PUSHED=NO
DEPLOYED=NO
ACTIVATED=NO
```

The only current task-owned write is this exact Parent Evidence path. Pre-existing dirty and
untracked artifacts remain excluded and untouched.
