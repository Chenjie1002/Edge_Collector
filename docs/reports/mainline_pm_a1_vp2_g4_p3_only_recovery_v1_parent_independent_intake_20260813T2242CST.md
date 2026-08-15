# Mainline PM A1 VP2-G4 P3-only Recovery V1 Parent-Independent Intake

## 1. Intake result

Historical Goal terminal remains immutable:

`HOLD / P3_ONLY_RECOVERY_CLEANUP_FAILED`

Mainline diagnostic classification:

`PASS / MAINLINE_PM_ACCEPTS_FAIL_CLOSED_TERMINAL_AND_ESTABLISHES_STANDALONE_OWNERSHIP_VERIFIER_FALSE_NEGATIVE`

This PASS is only for intake/root-cause classification. P3, cleanup, Parent Evidence, final Verification and G4 are not accepted.

## 2. Durable identities

- V1 Closeout: `6883 / a0736e384c2f23f8c0af88dd22f926f925fd7c697efdcfd68a936eb8ae719b3e`
- Owner result: `1430 / c4d27a2c964d97f35f52de3a81e1dc20d871264e77347c87ca439406acff3043`

Fresh Git remains:

```text
HEAD=2530721080e4fdcf9ff1e806e06969aa56affdf5
origin/main=2530721080e4fdcf9ff1e806e06969aa56affdf5
staged=EMPTY
```

## 3. V1 bounded facts

The Owner evidence records exactly one continuity SSH, one tunnel start, one standalone start and zero retry. Accepted V6 candidate continuity passed. No P3 smoke GET was issued because the runner stopped at standalone ownership verification. The tunnel was cleaned. PID `30610` remained on port 3101 because the frozen ownership predicate did not pass and the runner correctly failed closed without signalling an unproven PID.

## 4. Evidence-bound process provenance

The immutable runner captured `standalone_pid=$!` and durably emitted:

```text
P3R:STANDALONE_PID=30610
P3R:STANDALONE_READY_ATTEMPT=2
STANDALONE_START_ATTEMPTS=1
RETRY=0
```

Fresh read-only facts for exact PID `30610`:

```text
start=2026-08-13 22:35:23 local
runner start=2026-08-13 22:35:21 local
executable=/usr/local/bin/node
cwd=/Users/chenjie/Documents/MES/edge-mes-demo/frontend/.next/standalone
listener=127.0.0.1:3101 owned by PID 30610
process title=next-server (v16.2.10)
```

These facts, especially exact `$!` PID binding, two-second launch timing, exact 3101 listener ownership and expected Next standalone cwd, establish PID `30610` as an evidence-bound predecessor-owned standalone process rather than an unrelated foreign listener.

## 5. Root cause

The V1 runner required post-start ownership to preserve both:

```text
command contains: node .next/standalone/server.js
cwd equals: frontend/
```

Actual Next standalone runtime behavior changes those observations:

```text
process title becomes: next-server (v16.2.10)
cwd becomes: frontend/.next/standalone
```

Prior V6 successful evidence had already recorded the standalone cwd as `frontend/.next/standalone`.

Therefore the first decisive blocker is:

`STANDALONE_OWNERSHIP_VERIFIER_FALSE_NEGATIVE`

More precisely:

`OVERSTRICT_POST_START_COMMAND_AND_CWD_IDENTITY_PREDICATE`

Not established: foreign process, second standalone start, retry, candidate runtime drift, tunnel cleanup failure or product defect.

## 6. Historical HOLD remains correct

The V1 Goal must remain terminal HOLD because its frozen ownership predicate failed. The runner correctly did not act on a PID that it could not prove under its own frozen authority. Mainline diagnosis of a verifier defect does not rewrite that historical terminal.

## 7. Successor correction

A fresh P3-only Recovery V2 should correct the ownership predicate to use stable provenance: exact captured child PID, exact listener ownership on 3101, preflight-resolved Node executable, expected standalone cwd and launch-time continuity. It must not require the process title to preserve the original launch command string.

V2 should remain P3-only: no redeploy, no frontend rebuild, no business endpoint GET, no DB/SQL, no source repair. It may reuse Mainline-accepted V6 P2, perform fresh read-only runtime continuity, then one tunnel, one standalone, four smoke requests, exact cleanup, fresh Parent Evidence and one local-only Verification.

## 8. State separation

```text
P3R_V1_HISTORICAL_TERMINAL=HOLD
MAINLINE_ACCEPTS_FAIL_CLOSED_BEHAVIOR=YES
ROOT_CAUSE=OWNERSHIP_VERIFIER_FALSE_NEGATIVE
PID_30610=EVIDENCE_BOUND_PREDECESSOR_OWNED_ORPHAN
P3_ACCEPTED=NO
G4_ACCEPTED=NO
PARENT_EVIDENCE=ABSENT
FINAL_VERIFICATION=NOT_RUN
G5_AUTHORIZED=NO
```

## 9. Next gate

`OWNER_EXACT_CLEANUP_OF_P3R_V1_PID_30610_AND_FRESH_A1_VP2_G4_P3_ONLY_RECOVERY_V2_PACKAGE`

Cleanup authority and V2 execution authority must be fresh. V2 must not start until the residual 3101 listener is cleared and mechanically rechecked.
