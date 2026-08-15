# Mainline PM A1 VP2-G4 V3 Runtime Health HOLD — Parent Independent Intake

报告角色：Mainline PM independent intake

Goal：`A1-VP2-G4-COMMITTED-RUNTIME-PREPARATION-V3`

结论：`PASS / MAINLINE_PM_ACCEPTS_V3_FAIL_CLOSED_TERMINAL`

Historical Goal terminal 保持：`HOLD / G4_COMMITTED_RUNTIME_V3_API_ROLLBACK_FAILED`

Mainline PM root-cause boundary：`RUNTIME_HEALTH_CAUSE_NOT_ESTABLISHED / ROLLBACK_ACTION_IDENTITY_RESTORED_BUT_HEALTH_NOT_VERIFIED`

## 1. Immutable authority and durable outputs

```text
V3 Charter = regular/non-symlink / 28641 / 86a5ea855b65afebe3247423ba4c5c931873532e6a9802a55675961ed2e56926
V3 Goal Prompt = regular/non-symlink / 21934 / 24353273efc60c8caf3e32ed6ad0d90f8a220f4637e3537fe45c7431f03ede94
V3 Ledger = regular/non-symlink / 47935 / 0d61c5f45be1aba4d9a4c46b26d7934b4c168ac34fb06d75d280b2d45ef54b61
V3 Closeout = regular/non-symlink / 8684 / 8812296148893c1d3873f47135418c9b6fc590b45c2912c6af6f4325d337e4f4
V3 Parent Evidence = ABSENT
```

V1/V2 historical Ledger/Closeout identities were rechecked and remain unchanged. No historical terminal is resumed, retried, rewritten or reclassified.

## 2. Fresh local intake baseline

```text
HEAD = 2530721080e4fdcf9ff1e806e06969aa56affdf5
origin/main = 2530721080e4fdcf9ff1e806e06969aa56affdf5
ahead/behind = 0/0
HEAD:api = ffddc637e50e180021116069eb9930c066a37084
staged = EMPTY
tracked dirty continuity = docs/thread_handoff/pm_operating_rules.md only
git diff --check = PASS
git diff --cached --check = PASS
port 8000 = NO_LISTENER
port 3101 = NO_LISTENER
```

## 3. V3 static correction acceptance

The V3 package correction succeeded and is not the blocker:

```text
V2 source transaction = 565 lines / 33456 bytes / 8b7376d4bfdde274ff0b3f6b622029edb61175632c1704136507b81f4c9d0f15
accidental leading-plus contamination = exactly 95 lines / source lines 471..565
corrected no-final-LF transaction = 33361 / 8d3fafbcc6902ee64dcbe8b56cdda82ce87061c4b68ce83b34d3daa00e6759cb
corrected final-LF execution body = 33362 / e448fcd0281ef9673326880a8ef5b5eacc4f3579b03ac0f89fd96c169c2ca7e2
sh -n = PASS / RC 0
remaining leading diff markers = 0
rollback semantic-equivalence static gate = PASS
execution lock = FROZEN
```

The corrected rollback truth remained:

```text
OLD_API_CONFIG_IMAGE = edge-mes-demo-api OR edge-mes-demo-api:latest
prebuild target-tag DIFFERENT/ABSENT alone is non-blocking
rollback truth = fresh active old full image ID + successful full-ID inspectability
```

## 4. Accepted P2 facts before health failure

The one authorized external transaction was consumed. The following evidence is accepted as observed execution fact, not as P2 acceptance:

```text
remote host/arch/Compose preflight = PASS
old API rollback anchor = PASS
old API configured image = edge-mes-demo-api / accepted
old API image = sha256:46c6ff3dd4b5ac5c6d5efd8fb74449623c5614b4d9f9aceae50ffef11cba92cf / inspectable
prebuild target tag relation = SAME
protected Collector/Postgres prestate = complete / running
remote Docker build = 1 / RC 0
new API image = sha256:45938b8e826237bb4c6c595ddecf9f5d28e2709f39710bed905944ef33afe9e0
new platform = linux/arm64/v8
normal API-only recreate = 1 / RC 0
new API poststate image = new image / running=true
committed deployed bytes = PASS / six required paths exact
protected poststate after recreate/runtime = exact prestate equality / running
```

Therefore the V3 blocker is not build failure, source-byte mismatch, rollback-anchor failure, protected-service drift, or API-only Compose command nonzero.

## 5. Health and rollback boundary

Normal health verification:

```text
GET http://127.0.0.1:8000/health attempts = 10/10
HTTP codes = 000,000,000,000,000,000,000,000,000,000
status=ok = not established
OpenAPI GET = 0 / not reached
scope-options GET = 0 / not reached
```

Rollback action then executed under the frozen contract:

```text
old image recheck = PASS
rollback tag restore = 1 / RC 0
rollback API-only recreate = 1 / RC 0
rollback API image = old full image ID
rollback API running = true
protected continuity = exact prestate equality / running
```

Rollback health verification:

```text
GET http://127.0.0.1:8000/health attempts = 10/10
HTTP codes = 000,000,000,000,000,000,000,000,000,000
health PASS = NO
```

The Goal was correct to fail closed under its frozen contract and terminalize as `HOLD / G4_COMMITTED_RUNTIME_V3_API_ROLLBACK_FAILED`.

However, Mainline PM must not reinterpret that umbrella terminal as proof that the Docker tag/recreate rollback action itself failed. The durable evidence proves old-image identity restoration and a running rollback container. What failed was health verification after rollback.

## 6. Root-cause limitation

The current health root cause is NOT ESTABLISHED because V3 did not establish a fresh pre-mutation `/health` baseline for the old runtime. Historical evidence shows the same old image previously passed remote loopback health, but that cannot substitute for a fresh pre-mutation observation on 2026-08-13.

V3 also did not durably preserve the health curl transport return code and stderr for the twenty HTTP-000 attempts. Therefore the durable record cannot distinguish connection refused, timeout, local port-binding absence, rapid restart/listener absence, or another transport failure.

Consequently:

```text
NEW_API_PRODUCT_DEFECT = NOT_ESTABLISHED
ROLLBACK_DOCKER_ACTION_FAILURE = NOT_ESTABLISHED
PREEXISTING_REMOTE_HEALTH_FAILURE = POSSIBLE / NOT ESTABLISHED
HOST_PORT_OR_LISTENER_FAILURE = POSSIBLE / NOT ESTABLISHED
API_PROCESS_STARTUP_OR_RESTART_FAILURE = POSSIBLE / NOT ESTABLISHED
RUNTIME_HEALTH_ROOT_CAUSE = NOT ESTABLISHED
```

## 7. Counters and protected boundaries

```text
Quality business GET = 0
Trace business GET = 0
Process Metrics business GET = 0
DB/SQL/migration = 0
Collector lifecycle = 0
Postgres lifecycle = 0
protected Collector/Postgres exec/logs = 0
retry/reconnect/fallback = 0
second SSH = 0
Git mutation = 0
P3 = NOT_STARTED
final Verification = NOT_STARTED
unauthorized actions = 0
```

## 8. Mainline disposition and next gate

V3 is an immutable historical HOLD and must not be resumed.

Do NOT immediately issue another deployment successor. Current remote API health state is not accepted and root cause is unknown.

Recommended next authority is one fresh, bounded, read-only runtime-health recovery diagnostic. It should use a new one-shot SSH budget and no mutation to establish at minimum:

```text
fresh API container identity/state/restart/OOM/error fields
fresh image/tag identity
fresh Compose project/service identity
fresh host/container published port binding for 8000
fresh host listener observation for 127.0.0.1:8000 / 0.0.0.0:8000 as applicable
bounded curl with exact curl RC, HTTP code and stderr preserved
bounded API container logs sufficient to classify startup/listener failure
protected Collector/Postgres metadata continuity only; no exec/log/lifecycle
no Docker lifecycle, tag, build, recreate or cleanup
no DB/SQL, PLC/V-PLC, business GET, Git mutation or retry/reconnect
```

Only after that diagnostic is independently intaken should Mainline PM decide whether the next step is runtime repair, another committed API deployment attempt, or a narrower infrastructure correction.

```text
NEXT_GATE = OWNER_FRESH_AUTHORITY_FOR_G4_RUNTIME_HEALTH_RECOVERY_DIAGNOSTIC_ONLY
AUTOMATIC_VP2_G5 = NO
AUTOMATIC_OWNER_VISUAL_ACCEPTANCE = NO
AUTOMATIC_A1_S2 = NO
```

## 9. MES Skill insertion recommendation

Do not implement the full Edge MES Skill during this unresolved runtime-health incident. Preserve recovery scope.

Recommended insertion point:

```text
G4 runtime-health root cause resolved
→ G4 committed runtime preparation reaches PASS
→ final independent Verification accepted by Mainline PM
→ PAUSE before VP2-G5
→ build and validate Edge MES Skill v1
→ then begin VP2-G5 under the reusable Skill
```

Reason: at that point the project will possess one complete, corrected end-to-end governance/runtime pattern instead of freezing V1/V2/V3 defects into a reusable Skill.

The Skill v1 validation suite should replay historical V1/V2/V3 failures as negative fixtures, including at minimum:

```text
V1 literal :latest rollback-guard regression
V2 accidental leading diff-marker contamination
V3 missing fresh pre-mutation health baseline
V3 missing curl RC/stderr durability
first-decisive-blocker and one-shot budget preservation
immutable historical Goal separation
```

Until that insertion point, collect these patterns as Skill requirements only; do not allow Skill work to alter the current runtime recovery authority.
