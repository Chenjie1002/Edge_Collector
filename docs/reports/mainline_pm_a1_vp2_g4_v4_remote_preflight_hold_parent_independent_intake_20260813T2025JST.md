# Mainline PM — A1 VP2-G4 V4 Remote Preflight HOLD Parent Independent Intake

Intake object: `A1-VP2-G4-COMMITTED-RUNTIME-PREPARATION-V4`

Conclusion: `PASS / MAINLINE_PM_ACCEPTS_V4_FAIL_CLOSED_TERMINAL`

Historical terminal remains immutable: `HOLD / G4_COMMITTED_RUNTIME_V4_REMOTE_PREFLIGHT_FAILED`

## Independent facts

V4 package identities, local bootstrap, remote transaction static gate and execution lock all passed. The sole external attempt consumed one Git archive and one SSH client launch. The client returned RC 255 with `Operation not permitted` before any remote shell started. Remote transaction, remote preflight, Docker, HTTP, rollback, P3 and Verification were not reached. No retry, reconnect or second SSH occurred.

Fresh Mainline intake continuity remains: HEAD and origin/main at `2530721080e4fdcf9ff1e806e06969aa56affdf5`, HEAD:api `ffddc637e50e180021116069eb9930c066a37084`, ahead/behind 0/0, staged empty, only the existing PM Rules tracked-dirty continuity, local ports 8000 and 3101 without listeners.

## Mainline classification

`MAINLINE_BLOCKER_CLASS = LOCAL_EXECUTION_ENVIRONMENT_NETWORK_CAPABILITY_DENIAL`

The failure happened at the local SSH socket-connect boundary before authentication or remote-shell startup. It does not establish Pi host/Compose drift, SSH authentication failure, remote port refusal, Docker/API/rollback failure, candidate-health failure, product defect or V4 package defect.

Accepted Diagnostic V2 evidence previously used the same project endpoint/identity contract and completed one SSH connection/remote shell successfully, so V4's EPERM cannot by itself be promoted to an intrinsic endpoint/key defect. Historical success does not prove current reachability; it only constrains the classification.

## State separation

V4 runtime preparation remains unaccepted. V4 did not deploy or activate anything because the remote shell never started. Diagnostic V2 `CURRENTLY_HEALTHY` remains bounded historical evidence and is not a substitute for a fresh pre-mutation baseline.

## Recommended next authority

Do not spend another fresh Goal by attempting the identical external transaction from the same restricted Goal execution venue.

Recommended successor: `A1-VP2-G4-COMMITTED-RUNTIME-PREPARATION-V5`, preserving V4 deployment/readiness/rollback semantics but changing the external P2 execution venue to an Owner-assisted normal macOS Terminal with an exact immutable one-shot command and durable capture/return protocol. P3 remains forbidden until that P2 evidence is independently accepted.

`NEXT_GATE = OWNER_FRESH_AUTHORITY_FOR_A1_VP2_G4_COMMITTED_RUNTIME_PREPARATION_V5_OWNER_ASSISTED_P2`
