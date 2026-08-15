# A1 Local Minimal Stack Image Materialization — Mainline PM Intake

## Conclusion

```text
PASS / A1_LOCAL_MINIMAL_STACK_IMAGE_MATERIALIZATION_COMPLETE
```

Owner-assisted image materialization completed within the frozen authority. The three exact local images required for the later `postgres -> api -> dashboard` runtime gate are now present. No target container was created and no runtime lifecycle was executed.

## Authority / task identity

```text
TASK = docs/thread_handoff/pm_task_20260815T1047Z_a1_local_minimal_stack_image_materialization.md
TASK_TYPE = regular / non-symlink
TASK_BYTES = 15134
TASK_SHA256 = dc6239b9318e617739c88b115989574f17d01992ee976a538f2b1746b57bcae4
AUTHORITY = Owner approval of A1_LOCAL_MINIMAL_STACK_IMAGE_MATERIALIZATION
```

## Entry repository state

```text
BRANCH = main
HEAD = 6226bf3fb716880a176f9eb642b8139cef3255a6
ORIGIN_MAIN = 6226bf3fb716880a176f9eb642b8139cef3255a6
AHEAD_BEHIND = 0/0
STAGED = 0
TRACKED_DIRTY = 0
REPORT_PRESTATE = ABSENT
```

The existing untracked governance/evidence corpus remains preserve/exclude/do-not-adopt.

## Frozen source inputs

Pre-dispatch identities were frozen as:

```text
api/Dockerfile SHA256 = 16a835afb74a7ca571166411aaa55a280eac8147a60fd792d9e516cd7fa5e324
api/requirements.txt SHA256 = 71460751382578276a69d07371036db0949832f9a171189c1d850d9893531b44
frontend/Dockerfile SHA256 = a582c10d9be8fd0f34cb384c68e742e768896a41798c99282c53710a45c48ff8
frontend/package-lock.json SHA256 = 56e2bfc317bf0a432850421da72f18b1768aa150fc8ce85470344a4432ca984b
```

The API build context had no untracked files. `frontend/next-env.d.ts` was the only observed untracked frontend file and was explicitly excluded by `frontend/.dockerignore`, so it did not become an unauthorized build input.

## Materialization result

Owner Terminal returned:

```text
PRECHECK_OK = 1
POSTGRES_PULL_COUNT = 1
POSTGRES_PULL_RC = 0
API_BUILD_COUNT = 1
API_BUILD_RC = 0
DASHBOARD_BUILD_COUNT = 1
DASHBOARD_BUILD_RC = 0
FAILED_TARGET = NONE
CONTAINER_DRIFT = 0
```

Exact resulting image identities:

```text
postgres:16
  ID = sha256:11a9d238fbb48bab14599c57e41123254452b1a2d93c6c8595bce96f346bd082
  ARCH = arm64
  OS = linux
  SIZE = 158864523
  CREATED = 2026-08-13T19:16:24.748185659Z
  REPO_DIGEST = postgres@sha256:11a9d238fbb48bab14599c57e41123254452b1a2d93c6c8595bce96f346bd082

edge-mes-demo-api
  ID = sha256:3e8dd63059df782930016211b39c584a5c6c3a751bbbe385cd2eb85f4dede6e2
  ARCH = arm64
  OS = linux
  SIZE = 63671331
  CREATED = 2026-08-15T18:52:04.914453319+08:00
  REPO_DIGEST = edge-mes-demo-api@sha256:3e8dd63059df782930016211b39c584a5c6c3a751bbbe385cd2eb85f4dede6e2

edge-mes-dashboard:local
  ID = sha256:445f2c100471ec207c020973681f9c02765d05476a1dd9e70999e767822edb5a
  ARCH = arm64
  OS = linux
  SIZE = 91107873
  CREATED = 2026-08-15T18:52:39.928110332+08:00
  REPO_DIGEST = edge-mes-dashboard@sha256:445f2c100471ec207c020973681f9c02765d05476a1dd9e70999e767822edb5a
```

## Runtime boundary

No target containers existed after materialization:

```text
edge-mes-postgres = ABSENT
edge-mes-api = ABSENT
edge-mes-dashboard = ABSENT
```

Therefore:

```text
CONTAINER_LIFECYCLE = 0
POSTGRES_RUNTIME_STARTED = NO
API_RUNTIME_STARTED = NO
DASHBOARD_RUNTIME_STARTED = NO
DB_QUERY = 0
DB_WRITE = 0
SSH = 0
REMOTE_ACTION = 0
VPLC_ACTION = 0
PLC_ACTION = 0
```

This PASS proves local image availability only. It does not establish runtime readiness, API reachability, trusted-origin live binding, scope availability, real-data visibility, or frontend correctness.

## Final Git audit

Owner evidence:

```text
HEAD = 6226bf3fb716880a176f9eb642b8139cef3255a6
ORIGIN_MAIN = 6226bf3fb716880a176f9eb642b8139cef3255a6
STAGED = 0
TRACKED_DIRTY = 0
DIFF_CHECK_RC = 0
CACHED_DIFF_CHECK_RC = 0
```

Repository product state remained unchanged. Docker image/cache state is external local-runtime materialization evidence and is not Git publication.

## MVP alignment

```text
MVP_ALIGNMENT = MVP-ALIGNED
```

This gate removed the exact local environment prerequisite blocking the already-approved A1 Station Summary data-first runtime wiring validation. No UI scope, A1-S2 scope, product source scope, remote scope, or data-generation scope was added.

## Next gate

```text
NEXT_GATE = A1_STATION_SUMMARY_CONTROLLED_LOCAL_MINIMAL_STACK_BRINGUP_R2
```

The next gate should use the frozen image identities above and authorize exactly one no-build/no-pull lifecycle transaction for `postgres`, `api`, and `dashboard`, followed by bounded readiness and trusted real-data-path probes.

This report does not itself grant that successor lifecycle authority. Fresh Mainline PM / Owner authorization remains required. No build, pull, retry, cleanup, source change, DB seeding, remote action, Git publication, or A1-S2 authority is inherited from this PASS.
