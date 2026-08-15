# Mainline PM A1 VP2-G4 V6 Parent-Independent Intake

## 1. Intake identity

Goal under intake: `A1-VP2-G4-COMMITTED-RUNTIME-PREPARATION-V6`

Historical Goal terminal preserved as written:

`PASS / VP2_G4_COMMITTED_RUNTIME_PREPARATION_COMPLETE`

Mainline independent conclusion:

`HOLD / MAINLINE_PM_REJECTS_V6_OVERALL_PASS_DUE_TO_POST_LOCK_P3_STANDALONE_RETRY_AUTHORITY_VIOLATION`

This intake does not rewrite the V6 historical terminal. It classifies whether Mainline PM may accept that terminal as the parent-level G4 result.

## 2. Durable identities mechanically verified

- Parent Evidence: `10894 / e9a02ec14bbd5c3ae38ab9b1d7ee2cc1aafd66db3f992e4649b3ff1b78bc8451`
- Final Verification report: `10340 / ba09f5c75e7ca7b0281c33754b0cf00dcb373da443dc49254ffda9a4ddfd692e`
- Closeout: `6225 / 5a7ec1ebc7824badf2949d68b814b74c35066b30d8217620c78a558fdd0a2846`
- Ledger: `8993 / 4fb42cf68f54b57859f846f83fc25a247f9549a8ecd557f06afbc0fb20d0d677`
- Owner P2 stdout: `11208 / 9203c81e82e324735b8a634be50e1582f7b4304401da4ff0b78dd7ea42a146b3`
- Owner P2 stderr: `0 / e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Owner P2 result: `1118 / 3670bc27c2fab81cbda9e95a27d01abc21cee72c6556278bb2bfcad6081850dc`
- Final Verification task: `11866 / b8d68218e495b12dbe8264e1919983f5b7b012bb66e0ec8b26a2b727d06a8af2`, 16 sections.

## 3. Fresh repository and local facts

At Mainline intake:

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

No fresh Git/runtime drift was found during this intake.

## 4. V6 P2 facts independently accepted as a bounded sub-result

Owner evidence directly establishes:

```text
GIT_ARCHIVE_RC=0
SSH_RC=0
GIT_ARCHIVE_ATTEMPTS=1
SSH_PROCESS_ATTEMPTS=1
SSH_CONNECTION_ATTEMPTS=1
RETRY_RECONNECT_FALLBACK=0
SECOND_SSH=0
V4:P2:OPENAPI_ROUTES_PRESENT=YES|missing=
V4:P2:COMMITTED_DEPLOYED_BYTES=PASS
V4:P2:REMOTE_HEALTH=PASS
V4:P2:SCOPE_OPTIONS=PASS / REAL_ACTIVE_RUNTIME_MAPPING
V4:P2:PROTECTED_POSTSTATE=PASS / EXACT_PRESTATE_EQUALITY_AND_RUNNING
V4:P2:ROLLBACK_TAG_RESTORE=0
V4:P2:ROLLBACK_API_RECREATE=0
V4:P2:TERMINAL=PASS / COMMITTED_API_RUNTIME_LOADED
```

Forbidden P2 counters are zero. Mainline therefore accepts the factual V6 P2 deployment/runtime evidence as a bounded sub-result. This does not by itself establish overall G4 acceptance.

## 5. P3 smoke and cleanup factual evidence

Parent Evidence records a successful frontend build, one successful owned forwarding tunnel, one successful owned standalone listener, four ordered smoke requests, strict real scope-options, no station/time query submission, zero Quality/Trace/Process Metrics business GETs, and reverse-order owned cleanup. Fresh Mainline checks confirm ports 8000 and 3101 are currently clear.

These are useful factual observations. The decisive issue is not the eventual smoke content or cleanup result; it is the authority path used to obtain the successful standalone after a prior post-lock failure.

## 6. Decisive authority contradiction

The frozen V6 Charter states P3 uses `one Next standalone` and explicitly: `No ... retry`.

The frozen V6 Goal Prompt likewise states P3 uses `one V6-owned Next standalone` and explicitly: `No ... retry`.

The V6 Ledger freezes the execution lock and states that after lock there is no `repair、retry、reconnect、fallback、authority-budget increase`.

PM Rules state:

`After EXECUTION_LOCK, execution helpers and authority-bearing fields are immutable. Any later local failure is HOLD; no further repair, retry or authority-budget increase is allowed.`

However Parent Evidence records:

`The first sandbox-only bind attempt failed before a process/listener was created with EPERM; the identical required command was then launched once with the local bind permission required by the execution environment.`

The Final Verification report repeats that a first standalone bind invocation failed and a later invocation successfully started the standalone.

This is a post-lock local failure followed by a second launch attempt. No durable fresh Owner authority specifically authorizing a standalone retry or increasing that attempt budget was found in the V6 authority set or reports. The explicit Owner authority surfaced in Parent Evidence concerns the forwarding-only tunnel, not a second standalone launch.

The fact that the first attempt created no listener reduces operational contamination risk, but does not erase the frozen no-retry authority rule. Under PM Rules, failure after execution lock is terminal HOLD unless separately re-authorized under a fresh authority path.

## 7. Final Verification limitation

The single local-only Verification child correctly remained read-only/local-only and wrote only its report. Its own action boundary therefore passes.

But its conclusion `PASS` failed to reject the parent authority contradiction above. It treated the first EPERM bind as a non-authority-bearing environment fact even though the parent Charter/Prompt and PM Rules explicitly froze `no retry` after lock.

Therefore the Verification child PASS is not sufficient for Mainline parent acceptance.

## 8. State separation

```text
V6_HISTORICAL_GOAL_TERMINAL = PASS / immutable as historical record
MAINLINE_ACCEPTS_V6_P2_FACTS = YES / bounded sub-result
MAINLINE_ACCEPTS_V6_P3_SMOKE_FACTS = YES / factual observation only
MAINLINE_ACCEPTS_V6_CLEANUP_FACTS = YES
MAINLINE_ACCEPTS_V6_FINAL_VERIFICATION_AS_PARENT_GATE = NO
MAINLINE_ACCEPTS_V6_OVERALL_G4_PASS = NO
PRODUCTION_ACCEPTED = NO new acceptance
OWNER_VISUAL_ACCEPTED = NO
VP2_G5_AUTHORIZED = NO
A1_S2_AUTHORIZED = NO
```

## 9. Recommended successor boundary

Do not redeploy the candidate merely to repair this governance defect. V6 P2 already established committed candidate runtime loading and is accepted here as a bounded factual sub-result.

The minimal fresh successor should be a P3-only recovery/verification Goal that:

1. explicitly reuses the accepted V6 P2 factual evidence without replaying Git archive/SSH deployment/Docker build/recreate;
2. performs a fresh read-only pre-P3 runtime/health continuity gate sufficient to establish the already-loaded candidate is still the intended V6 API runtime before local smoke;
3. freezes local tunnel and standalone execution venues before lock;
4. grants exactly one successful-start attempt per owned process and handles required local bind permission before the first standalone invocation, so a sandbox-denied invocation is not consumed first;
5. runs the same four smoke requests, no business GET/query submission, exact owned cleanup;
6. creates new Parent Evidence and exactly one fresh local-only Verification child;
7. returns to Mainline independent intake before any G5/visual/A1-S2 work.

Suggested next gate:

`OWNER_FRESH_AUTHORITY_FOR_A1_VP2_G4_P3_ONLY_RECOVERY_V1`

No automatic successor is authorized by this intake.
