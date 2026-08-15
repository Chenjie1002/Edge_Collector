# Mainline PM A1 VP2-G4 P3-Only Recovery V1 Orphan Cleanup

## 1. Authority

Owner explicitly authorized exact cleanup of predecessor-owned orphan PID `30610` only after all of these fresh predicates passed:

- exact PID `30610` resolved executable `/usr/local/bin/node`;
- cwd `/Users/chenjie/Documents/MES/edge-mes-demo/frontend/.next/standalone`;
- exact PID `30610` was the sole listener owner on `127.0.0.1:3101`;
- no other PID could be signalled.

The authorization also permitted V2 package materialization only after cleanup PASS.

## 2. Pre-clean mechanical facts

```text
PRECLEAN_EXE=/usr/local/bin/node
PRECLEAN_CWD=/Users/chenjie/Documents/MES/edge-mes-demo/frontend/.next/standalone
PRECLEAN_EXACT_LISTENER_MATCHES=1
PRECLEAN_UNIQUE_LISTENER_PID_COUNT=1
PRECLEAN_LISTENER_PIDS=30610
PRECLEAN_PREDICATES=PASS
```

These facts are consistent with the P3R V1 Owner evidence binding `STANDALONE_PID=30610`, the V1 start window beginning at `2026-08-13T14:35:21Z`, and the observed process start at local `2026-08-13 22:35:23 +08:00`.

## 3. Exact cleanup action

Exactly one signal was sent:

```text
SIGNAL_SENT=TERM:30610
```

No other PID was signalled. No broad process cleanup, port cleanup, directory cleanup, KILL escalation, restart, retry, reconnect or runtime start was performed.

## 4. Cleanup result

```text
PID_EXITED_AT_CHECK=2
CLEANUP=PASS_PID_ABSENT_AND_3101_NO_LISTENER
```

Post-clean state:

```text
PID_30610=ABSENT
PORT_3101=NO_LISTENER
```

## 5. Root-cause classification preserved

This cleanup does not rewrite the historical V1 terminal:

`HOLD / P3_ONLY_RECOVERY_CLEANUP_FAILED`

Mainline root cause remains:

`STANDALONE_OWNERSHIP_VERIFIER_FALSE_NEGATIVE / OVERSTRICT_POST_START_COMMAND_AND_CWD_IDENTITY_PREDICATE`

The Next standalone process changed its observable process title to `next-server (v16.2.10)` and cwd to `frontend/.next/standalone`, while the V1 verifier incorrectly required the original launch command string to remain visible and cwd to remain `frontend/`.

The V2 correction is therefore limited to ownership verification. It must bind ownership to captured `$!` PID, exact 3101 listener ownership, resolved Node executable, standalone cwd and launch-time continuity; it must not infer ownership from mutable process-title text.

## 6. Repository state

At cleanup intake:

```text
HEAD=2530721080e4fdcf9ff1e806e06969aa56affdf5
origin/main=2530721080e4fdcf9ff1e806e06969aa56affdf5
HEAD:api=ffddc637e50e180021116069eb9930c066a37084
staged=EMPTY
tracked dirty=docs/thread_handoff/pm_operating_rules.md only
```

No Git stage/commit/push, product source mutation, build, deployment, HTTP, Docker or DB action was performed by this cleanup.

## 7. Next gate

Cleanup prerequisite for V2 materialization is satisfied.

`NEXT_GATE=MATERIALIZE_A1_VP2_G4_P3_ONLY_RECOVERY_V2_FRESH_SUCCESSOR_PACKAGE`
