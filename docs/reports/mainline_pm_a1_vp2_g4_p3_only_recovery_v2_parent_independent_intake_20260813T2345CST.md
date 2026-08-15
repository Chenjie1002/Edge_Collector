# Mainline PM A1 VP2-G4 P3-Only Recovery V2 Parent-Independent Intake

## 1. Intake identity and conclusion

Goal under intake: `A1-VP2-G4-P3-ONLY-RECOVERY-V2`

Historical Goal terminal preserved as written:

`PASS / VP2_G4_P3_ONLY_RECOVERY_V2_COMPLETE`

Mainline independent conclusion:

`PASS / MAINLINE_PM_ACCEPTS_A1_VP2_G4_P3_ONLY_RECOVERY_V2`

Composite G4 conclusion:

`PASS / MAINLINE_PM_ACCEPTS_VP2_G4_COMMITTED_RUNTIME_PREPARATION`

This intake does not rewrite V6, P3R V1 or P3R V2 historical terminals. It determines whether the bounded V2 P3 recovery may be accepted and whether the already-accepted V6 P2 bounded sub-result plus this accepted V2 P3 closure are sufficient to close VP2-G4.

## 2. Durable identities mechanically verified

- V2 Parent Evidence: `10378 / 7ac605c781027c778f6e57363fc85ef58abae25cc810852a550f29a6d9c91e30`
- V2 Final Verification report: `14152 / 173568e47bda9f17a8a515278de9e410d34c661d5ae2ff39b1fefba08153d5c0`
- V2 Closeout: `9717 / 30dde82e3720941f9ffb0e9aee3f0026d30027930a0759d65dbb50d24dd42681`
- V2 Ledger: `12115 / 59a40364f905b743aefd52406a7da5368bbc20aa4cd0d309203f34ea9450482f`
- V2 Owner stdout: `2513 / d86fe4160b930d00d36ddbe072b2b93c301d3a5f6a72bd578c26738652f325b1`
- V2 Owner stderr: `0 / e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- V2 Owner result: `1861 / 428e4a998acae739bf1cfed115939539f3850aa7b6e42f8cc66694526a60a6e1`
- Verification task: `9323 / d69c41763a1733f9222d0f1ff6eede93157c87d79f7eda61e2d3a4460798821e`, exactly 16 sections.
- Verification report: exactly 16 sections.
- Closeout: exactly 16 sections.

The previously accepted V6 P2 Mainline intake remains:

`docs/reports/mainline_pm_a1_vp2_g4_v6_parent_independent_intake_20260813T2202CST.md`

with `MAINLINE_ACCEPTS_V6_P2_FACTS = YES / bounded sub-result` and `V4:P2:TERMINAL=PASS / COMMITTED_API_RUNTIME_LOADED`.

## 3. Fresh repository and local process facts

At this Mainline intake:

```text
HEAD = 2530721080e4fdcf9ff1e806e06969aa56affdf5
origin/main = 2530721080e4fdcf9ff1e806e06969aa56affdf5
ahead/behind = 0/0
HEAD:api = ffddc637e50e180021116069eb9930c066a37084
staged = EMPTY
tracked dirty = docs/thread_handoff/pm_operating_rules.md only
git diff --check = PASS
git diff --cached --check = PASS
port 8000 = NO_LISTENER
port 3101 = NO_LISTENER
```

No fresh source, index or listener contamination was found.

## 4. Direct Owner evidence reconciliation

Mainline directly rechecked the actual V2 Owner stdout/result rather than relying only on Parent Evidence or Closeout summaries.

Exactly one required terminal is present:

`P3R2:TERMINAL=PASS / P3_ONLY_RECOVERY_V2_RUNTIME_SMOKE_AND_CLEANUP_COMPLETE`

Exactly one standalone ownership PASS and exactly one accepted-candidate continuity PASS are present.

Owner result independently reconciles:

```text
CONTINUITY_SSH_ATTEMPTS=1
CONTINUITY_SSH_RC=0
TUNNEL_START_ATTEMPTS=1
STANDALONE_START_ATTEMPTS=1
TUNNEL_HEALTH_GET=1
SCOPE_OPTIONS_GET=1
FRONTEND_HEALTH_GET=1
IDLE_STATION_SUMMARY_GET=1
QUALITY_BUSINESS_GET=0
TRACE_BUSINESS_GET=0
PROCESS_METRICS_BUSINESS_GET=0
RETRY=0
STANDALONE_TERM=1
STANDALONE_KILL=0
TUNNEL_TERM=1
TUNNEL_KILL=0
SMOKE_PASS=YES
CLEANUP_PASS=YES
TERMINAL=PASS / P3_ONLY_RECOVERY_V2_RUNTIME_SMOKE_AND_CLEANUP_COMPLETE
```

No contradiction, second start, retry or second smoke GET was found.

## 5. Candidate continuity and smoke facts

Owner stdout directly records:

```text
P3R2:CONTINUITY=PASS / ACCEPTED_V6_CANDIDATE_IMAGE_AND_HEALTH
P3R2:TUNNEL_HEALTH_HTTP=200
P3R2:SCOPE_HTTP=200
P3R2:SCOPE_TOPOLOGY=[{"line_id":"LINE_001","station_ids":["WS01","WS02","WS03"]}]
P3R2:FRONTEND_HEALTH_HTTP=200
P3R2:IDLE_HTTP=200
P3R2:IDLE_MARKERS=PASS
P3R2:SMOKE_PASS=YES
P3R2:CLEANUP_PASS=YES
P3R2:CLEANUP:PORT_8000=NO_LISTENER
P3R2:CLEANUP:PORT_3101=NO_LISTENER
```

The P3 smoke therefore establishes the intended minimal boundary only: current accepted API candidate continuity, real scope-options topology, frontend health, idle Station Summary shell, no submitted station/time query, and exact owned cleanup. It does not establish Quality/Trace/Process Metrics business values, Full OEE, production acceptance or visual acceptance.

## 6. Ownership verifier correction independently inspected

Mainline inspected the actual V2 runner implementation.

The V1 mutable process-title and `cwd == frontend/` ownership predicates are absent.

The V2 `owned_standalone()` predicate requires:

1. nonempty captured `standalone_pid` from exact `$!`;
2. nonempty captured `standalone_lstart_bound`;
3. exact PID still alive;
4. current normalized `lstart` equals the bound `lstart` token;
5. resolved executable equals the frozen Node binary;
6. cwd equals `frontend/.next/standalone`;
7. TCP 3101 has exactly one listener PID and it equals the captured PID;
8. the captured PID owns exactly one `127.0.0.1:3101` listener.

The actual Owner evidence passed this predicate for:

```text
PID=35424
lstart=四 8月/13 23:20:43 2026
exe=/usr/local/bin/node
cwd=/Users/chenjie/Documents/MES/edge-mes-demo/frontend/.next/standalone
listener=127.0.0.1:3101
```

This resolves the P3R V1 false-negative ownership defect without using mutable process title text and without weakening foreign-process protection.

## 7. P3R V1 historical defect and cleanup closure

P3R V1 historical HOLD remains immutable. Mainline previously established that its ownership verifier was a false negative and classified PID 30610 as an evidence-bound predecessor-owned orphan.

The separately authorized exact cleanup report remains:

`2853 / 3d5e59ad3a9125b7e609003d0a838449feccf49a204c60b886a00b04b16e505f`

and established exact cleanup of PID 30610 after fresh executable/cwd/unique-listener proof. V2 entered with PID 30610 absent and ports clear. No predecessor terminal was rewritten.

## 8. Final Verification acceptance

The V2 final Verification task is repository-backed, exactly 16 sections and scoped to one exact local-only report write.

The Verification report is exactly 16 sections and independently rechecked:

- authority and Owner evidence identities;
- accepted V6 candidate binding;
- PID/lstart/executable/cwd/listener ownership evidence;
- one-shot counters and `RETRY=0`;
- ordered four-request smoke;
- real scope topology;
- idle/no-query and business-GET-zero boundary;
- reverse-order cleanup and final clear ports;
- fresh Git/index facts.

Verification child action audit records:

```text
NETWORK=0
SSH=0
HTTP=0
NODE=0
NPM=0
DOCKER=0
DB=0
SIGNAL=0
GIT_MUTATION=0
CHILD_OF_CHILD=0
REPAIR=0
SECOND_VERIFICATION_CHILD=0
RUNNER_RERUN=0
```

Mainline found no parent-authority contradiction comparable to the V6 standalone retry defect.

## 9. Composite VP2-G4 acceptance

V6 Mainline intake already accepted the P2 deployment/runtime facts as a bounded sub-result while rejecting the V6 overall G4 PASS solely because the V6 P3 path violated its frozen no-retry authority.

P3R V1 correctly fail-closed on a separate ownership-verifier false negative and did not produce accepted P3 evidence.

P3R V2 is a fresh successor with a fresh one-shot P3 authority. It does not replay deployment or alter the accepted P2 facts. Its P3 continuity, smoke, ownership, cleanup and final local Verification now independently PASS.

Therefore the previously missing G4 closure is satisfied by the composite chain:

```text
ACCEPTED_V6_P2 = YES
ACCEPTED_P3R_V2_P3_RUNTIME_SMOKE = YES
ACCEPTED_P3R_V2_OWNERSHIP = YES
ACCEPTED_P3R_V2_CLEANUP = YES
ACCEPTED_P3R_V2_FINAL_VERIFICATION = YES
VP2_G4_ACCEPTED = YES
```

Mainline conclusion:

`PASS / MAINLINE_PM_ACCEPTS_VP2_G4_COMMITTED_RUNTIME_PREPARATION`

## 10. State separation and next authority

```text
V6_HISTORICAL_TERMINAL = immutable
P3R_V1_HISTORICAL_TERMINAL = immutable HOLD
P3R_V2_HISTORICAL_TERMINAL = immutable PASS
MAINLINE_ACCEPTS_P3R_V2 = YES
VP2_G4_ACCEPTED = YES
GIT_STAGE = 0
GIT_COMMIT = 0
GIT_PUSH = 0
PRODUCTION_ACCEPTED = NO new acceptance
OWNER_VISUAL_ACCEPTED = NO
VP2_G5_AUTHORIZED = NO
A1_S2_AUTHORIZED = NO
EDGE_MES_SKILL_AUTHORIZED = NO by this intake
```

This intake opens no automatic successor. Any G5, Owner visual review, A1-S2, Skill implementation, Git publication or other work requires separate Owner/Mainline authority.

Suggested next gate:

`OWNER_DECISION_AFTER_MAINLINE_ACCEPTED_VP2_G4`
