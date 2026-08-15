# Mainline PM — A1 VP2-G4 V5 OpenAPI Contract HOLD Parent Independent Intake

报告名称：Mainline PM A1 VP2-G4 V5 OpenAPI Contract HOLD Parent Independent Intake

项目：Edge MES Demo

项目绝对路径：`/Users/chenjie/Documents/MES/edge-mes-demo`

Intake source Goal：`A1-VP2-G4-COMMITTED-RUNTIME-PREPARATION-V5`

Mainline 结论：`PASS / MAINLINE_PM_ACCEPTS_V5_FAIL_CLOSED_TERMINAL`

V5 historical terminal 保持：`HOLD / G4_COMMITTED_RUNTIME_V5_OWNER_ASSISTED_P2_FAILED`

## 1. Independent intake identity

V5 durable evidence identities independently observed：

```text
V5_LEDGER = regular/non-symlink / 13981 / cdfb556b5404d80cb4390562abc6c41164181f70036ce99291d4318937ea9c68
V5_CLOSEOUT = regular/non-symlink / 9583 / 22a62920e0c6c2eeb7de0ca9be6c166cc924d15ce8c403b6f509d3dd7b7d633d
OWNER_STDOUT = regular/non-symlink / 13071 / 72c73b1aa4530d22241fc301eed191cefda281570b64c13db7e13e4751ce29fa
OWNER_STDERR = regular/non-symlink / 0 / e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
OWNER_RESULT = regular/non-symlink / 1120 / c403a59ab371e3dbd44dc6887da519e277ea27a88910f0ff3e2911999f888977
```

Fresh local continuity：

```text
HEAD = 2530721080e4fdcf9ff1e806e06969aa56affdf5
origin/main = 2530721080e4fdcf9ff1e806e06969aa56affdf5
ahead/behind = 0/0
HEAD:api = ffddc637e50e180021116069eb9930c066a37084
staged = EMPTY
tracked dirty continuity = docs/thread_handoff/pm_operating_rules.md only
git diff --check = PASS
git diff --cached --check = PASS
```

## 2. Accepted V5 P2 facts

Owner-assisted normal macOS Terminal execution consumed exactly one Git archive and one SSH attempt. SSH reached the remote transaction and returned RC 50 only after the transaction itself terminalized.

Accepted candidate facts：

```text
PREMUTATION_HEALTH = PASS / attempt 1 / curl_rc 0 / HTTP 200 / status=ok
REMOTE_DOCKER_BUILD = 1 / RC 0
NEW_API_IMAGE_ID = sha256:45938b8e826237bb4c6c595ddecf9f5d28e2709f39710bed905944ef33afe9e0
NEW_API_PLATFORM = linux/arm64/v8
NORMAL_API_RECREATE = 1 / RC 0
COMMITTED_DEPLOYED_BYTES = PASS
NORMAL_HEALTH = PASS / attempt 2
OPENAPI_GET = 1 / curl_rc 0 / HTTP 200
SCOPE_OPTIONS_GET = 0 / blocked behind OpenAPI gate
```

Readiness correction worked as intended: candidate attempt 1 returned curl RC 56 / HTTP 000 / connection reset, then after bounded delay attempt 2 returned HTTP 200/status=ok. This confirms V3 zero-delay polling was a verifier/controller regression and V4/V5 readiness semantics corrected that defect.

Rollback facts：

```text
OLD_API_IMAGE_RECHECK = PASS
ROLLBACK_ELIGIBLE = YES
ROLLBACK_TAG_RESTORE = 1 / RC 0
ROLLBACK_API_RECREATE = 1 / RC 0
ROLLBACK_API_IMAGE_ID = sha256:46c6ff3dd4b5ac5c6d5efd8fb74449623c5614b4d9f9aceae50ffef11cba92cf
ROLLBACK_HEALTH = PASS / attempt 2
Collector continuity = exact prestate equality / running
Postgres continuity = exact prestate equality / running
```

No retry/reconnect/second SSH, DB/SQL, Quality/Trace/Process Metrics business GET, protected exec/log/lifecycle, image cleanup, P3 or Verification occurred.

## 3. Decisive OpenAPI evidence

The V4 remote transaction, reused unchanged by V5, checked this literal required route set：

```text
/api/v2/quality
/api/v2/trace
/api/v2/process-metrics
/api/v2/production/scope-options
```

The remote candidate returned HTTP 200 OpenAPI, but the validator reported：

```text
OPENAPI_CHECK_RC = 1
OPENAPI_ROUTES_PRESENT = NO
missing = /api/v2/quality,/api/v2/trace
```

The missing paths are not the accepted trusted Quality/Trace endpoints.

## 4. Accepted trusted route authority

Independent repository inspection establishes the current committed/trusted endpoints as：

```text
Quality       = GET /api/v2/production/quality
Trace         = GET /api/v2/production/trace
Process       = GET /api/v2/process-metrics
Scope Options = GET /api/v2/production/scope-options
```

Evidence is consistent across current source, API tests, frontend clients, prior PM tasks/reports, and the previously successful controlled API deployment V5 authority/evidence.

Current committed source specifically has：

```text
api/app/routes/quality_trace.py:
  APIRouter(prefix="/api/v2/production")
  @router.get("/quality")
  @router.get("/trace")

api/app/routes/process_metrics.py:
  @router.get("/api/v2/process-metrics")

api/app/routes/scope_options.py:
  APIRouter(prefix="/api/v2/production")
  @router.get("/scope-options")
```

`api/app/main.py` includes the corresponding routers.

A fresh local in-memory route inventory using committed source returned：

```text
/api/v2/production/quality = GET
/api/v2/production/trace = GET
/api/v2/process-metrics = GET
/api/v2/production/scope-options = GET
TRUSTED_OPENAPI_ROUTE_SET = PASS
```

Frontend trusted station-summary code calls `/api/v2/production/quality`, `/api/v2/process-metrics`, and `/api/v2/production/scope-options`; API tests call `/api/v2/production/quality` and `/api/v2/production/trace`.

## 5. Root-cause classification

Established root cause：

```text
V5_DECISIVE_BLOCKER_CLASS = OPENAPI_VERIFIER_CONTRACT_PATH_REGRESSION
V4_TRANSACTION_QUALITY_EXPECTED_PATH = WRONG / /api/v2/quality
V4_TRANSACTION_TRACE_EXPECTED_PATH = WRONG / /api/v2/trace
ACCEPTED_QUALITY_PATH = /api/v2/production/quality
ACCEPTED_TRACE_PATH = /api/v2/production/trace
PRODUCT_ROUTE_ABSENCE = NOT_ESTABLISHED
CANDIDATE_SOURCE_DEFECT = NOT_ESTABLISHED
CANDIDATE_HEALTH_DEFECT = NOT_ESTABLISHED
DOCKER_FAILURE = NOT_ESTABLISHED
ROLLBACK_FAILURE = NOT_ESTABLISHED
```

This is a verifier/controller contract regression introduced in the committed-runtime preparation transaction family. The transaction incorrectly shortened the already-accepted production Quality/Trace paths by removing `/production`.

The V5 fail-closed behavior remains correct: once its frozen verifier failed, it had to rollback and terminalize. Historical V5 must not be rewritten to PASS.

## 6. What V5 did and did not establish

V5 established that the committed candidate：

```text
builds successfully,
loads exact committed bytes,
starts successfully with bounded readiness,
and serves OpenAPI HTTP 200.
```

It did not complete the correct OpenAPI route gate or real scope-options GET because the incorrect verifier stopped P2 first. Since the candidate was rolled back, Mainline cannot promote P2 to PASS from local evidence alone.

Therefore：

```text
P2_ACCEPTED = NO
P3_ELIGIBLE = NO
G4_ACCEPTED = NO
```

## 7. Recommended fresh successor boundary

Do not modify V5 or V4 historical artifacts in place.

Recommended fresh successor：

`A1-VP2-G4-COMMITTED-RUNTIME-PREPARATION-V6`

V6 should preserve V5 Owner-assisted execution venue, V4 readiness/rollback semantics, committed source, budgets, protected surfaces, P3 and Verification semantics.

The sole controller correction should be to derive a fresh immutable remote transaction from V4 by replacing exactly two OpenAPI validator literals：

```text
/api/v2/quality -> /api/v2/production/quality
/api/v2/trace   -> /api/v2/production/trace
```

No product source change is justified by current evidence.

V6 pre-authority static gate should mechanically prove the exact trusted route tuple appears in the transaction and the two wrong shortened literals are absent from the OpenAPI required-route validator.

Because V5 rollback is verified and the current runtime is restored, V6 may receive a fresh one-shot P2 budget only by new Owner authority.

## 8. Mainline stop

```text
MAINLINE_PM_INTAKE = PASS / V5 FAIL-CLOSED TERMINAL ACCEPTED
ROOT_CAUSE = OPENAPI_VERIFIER_CONTRACT_PATH_REGRESSION
HISTORICAL_V5_TERMINAL = IMMUTABLE HOLD
AUTOMATIC_V6 = NO
AUTOMATIC_P3 = NO
AUTOMATIC_G5 = NO
NEXT_GATE = OWNER_FRESH_AUTHORITY_FOR_A1_VP2_G4_COMMITTED_RUNTIME_PREPARATION_V6
```
