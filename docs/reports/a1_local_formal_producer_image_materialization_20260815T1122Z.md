# A1 Local Formal Producer Image Materialization

## Conclusion

```text
PASS / A1_LOCAL_FORMAL_PRODUCER_IMAGE_MATERIALIZATION_COMPLETE
```

The three local formal-producer images required by the previously accepted `LOCAL_FORMAL_PRODUCER_PATH` were materialized successfully. No producer container was created or started, no accepted fact was generated, and the existing PostgreSQL/API/Dashboard runtime remained running throughout this gate.

## Authority / task identity

```text
TASK = docs/thread_handoff/pm_task_20260815T1122Z_a1_local_formal_producer_image_materialization.md
TASK_TYPE = regular / non-symlink
TASK_BYTES = 9821
TASK_SHA256 = 81dee2f0d28c1c7f7754575eb785d069283896e66176a75fdde3204e3fc54dbc
AUTHORITY = OWNER-A1-LOCAL-FORMAL-PRODUCER-IMAGE-MATERIALIZATION-20260815T1922+0800
```

Owner authority allowed only the exact three producer image builds, implicit Docker build dependency/base retrieval, image identity capture and this durable report. Container lifecycle, DB writes, data generation, source repair, Git mutation and remote actions were not authorized.

## Entry repository state

```text
BRANCH = main
HEAD = 6226bf3fb716880a176f9eb642b8139cef3255a6
ORIGIN_MAIN = 6226bf3fb716880a176f9eb642b8139cef3255a6
AHEAD_BEHIND = 0/0
STAGED = 0
TRACKED_DIRTY = 0
GIT_DIFF_CHECK = PASS
GIT_DIFF_CACHED_CHECK = PASS
```

Target images were absent before execution:

```text
edge-mes-demo-simulator = ABSENT
edge-mes-demo-s7-plc-sim = ABSENT
edge-mes-demo-collector = ABSENT
```

Target producer containers were also absent:

```text
edge-mes-simulator = ABSENT
edge-mes-s7-plc-sim = ABSENT
edge-mes-collector = ABSENT
```

## Frozen source identities

```text
simulator/Dockerfile
  SHA256 = 8e878f1c2880192e3cf26c162404e831db408e2fb775046261decf12983bacda
simulator/requirements.txt
  SHA256 = 33e4ec5a915abf260b08a1fdacbdacaea5d3f2f1171ba3c6d90eb7cc53e891a7
s7_plc_sim/Dockerfile
  SHA256 = b427258c7df8e04ded3fb2e7ab50ea283f563b07ecf0c39b8d53a0d8714dcf7e
s7_plc_sim/requirements.txt
  SHA256 = 565dfa31c849afb1966727a30f6fdcac57774ecf9fb559567b9c7da284ee5dba
collector/Dockerfile
  SHA256 = e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839
collector/requirements.txt
  SHA256 = eaa0a1bf2e133cdfdff2795f4604fc5fbeb54fe0e2bb1a0b990bf1a41a8f54cc
```

Committed tree identities:

```text
simulator = ab681a4e9c37ec342edcae981d17fc9b131ea10f
s7_plc_sim = ca73e6107666510e1ebd477ab8af628f01187ec3
collector = 29d17f171b1c53d8abb72462ce71350fdee5b3cf
common = 8d138b899eb0c4532358b812a73e26168e2d8b1b
```

Each of `simulator/`, `s7_plc_sim/`, `collector/`, and `common/` had zero untracked files at the execution lock.

## Build transaction

Execution was strictly sequential and fail-stop:

```text
BUILD_1_TARGET = edge-mes-demo-simulator
BUILD_1_COMMAND = docker build -t edge-mes-demo-simulator ./simulator
BUILD_1_COUNT = 1/1
BUILD_1_RC = 0

BUILD_2_TARGET = edge-mes-demo-s7-plc-sim
BUILD_2_COMMAND = docker build -t edge-mes-demo-s7-plc-sim ./s7_plc_sim
BUILD_2_COUNT = 1/1
BUILD_2_RC = 0

BUILD_3_TARGET = edge-mes-demo-collector
BUILD_3_CONTEXT = committed HEAD archive containing only collector + common
BUILD_3_COMMAND_CLASS = git archive HEAD collector common | docker build -t edge-mes-demo-collector -f collector/Dockerfile -
BUILD_3_COUNT = 1/1
BUILD_3_RC = 0
```

Collector intentionally did not use live repository root `.` as its build context. This prevented the large root untracked governance/evidence corpus from entering the Docker context. Docker reused existing cached layers for the Collector build, but the build input was still the frozen committed `HEAD` archive. No retry occurred.

## Final image identities

```text
TAG = edge-mes-demo-simulator
ID = sha256:e27022b07ae46639ca19b090613a90f839aa112de2dc514ef0a5705ca8c189a0
ARCH = arm64
OS = linux
SIZE = 58515261
CREATED = 2026-08-15T19:25:00.438543761+08:00
REPO_DIGEST = edge-mes-demo-simulator@sha256:e27022b07ae46639ca19b090613a90f839aa112de2dc514ef0a5705ca8c189a0

TAG = edge-mes-demo-s7-plc-sim
ID = sha256:551cfe8f71d150949a212af7c6e4723c82c24fc73017e5b08f1dbe4f8a64a815
ARCH = arm64
OS = linux
SIZE = 58383331
CREATED = 2026-08-15T19:25:48.86577605+08:00
REPO_DIGEST = edge-mes-demo-s7-plc-sim@sha256:551cfe8f71d150949a212af7c6e4723c82c24fc73017e5b08f1dbe4f8a64a815

TAG = edge-mes-demo-collector
ID = sha256:3a7ec1f2bcc6811508e43b0765f177d89aa6f5011bba86f1152ff458a50e8df9
ARCH = arm64
OS = linux
SIZE = 54302489
CREATED = 2026-08-15T15:27:54.399837919+08:00
REPO_DIGEST = edge-mes-demo-collector@sha256:3a7ec1f2bcc6811508e43b0765f177d89aa6f5011bba86f1152ff458a50e8df9
```

The Collector image's older `Created` timestamp is compatible with Docker cache reuse and is not used as source authority. The authoritative build-source evidence for this gate is the committed `HEAD` archive/tree identity plus the successful exact build command and resulting final tag/image ID.

## Runtime / container boundary

Final producer container state remained:

```text
edge-mes-simulator = ABSENT
edge-mes-s7-plc-sim = ABSENT
edge-mes-collector = ABSENT
```

Protected existing runtime remained running:

```text
edge-mes-postgres = running / healthy
edge-mes-api = running
edge-mes-dashboard = running / healthy
```

This task therefore establishes image materialization only. It does not establish producer activation, Collector acceptance, V-PLC production, DB accepted-fact generation, or production acceptance.

## Allowlist accounting

```text
PRODUCER_IMAGE_BUILDS = 3
BUILD_RETRY = 0
INDEPENDENT_DOCKER_PULL = 0
PRODUCER_CONTAINER_LIFECYCLE = 0
DB_QUERY = 0
DB_WRITE = 0
HTTP = 0
VPLC_ACTION = 0
PLC_ACTION = 0
SSH = 0
REMOTE_FS = 0
SOURCE_WRITE = 0
COMPOSE_WRITE = 0
GIT_STAGE = 0
GIT_COMMIT = 0
GIT_PUSH = 0
GIT_TAG = 0
GIT_RESET_STASH_CLEAN = 0
UNAUTHORIZED_ACTION = 0
```

Docker build-network use was limited to base-image/dependency retrieval naturally performed by the three authorized Dockerfiles. No independent network probe or package repair was performed.

## Final Git audit

```text
HEAD = 6226bf3fb716880a176f9eb642b8139cef3255a6
ORIGIN_MAIN = 6226bf3fb716880a176f9eb642b8139cef3255a6
AHEAD_BEHIND = 0/0
STAGED = 0
TRACKED_DIRTY = 0
GIT_DIFF_CHECK = PASS
GIT_DIFF_CACHED_CHECK = PASS
```

The task/report remain untracked and unstaged. Existing untracked governance/evidence content remains preserved and excluded.

## MVP alignment

```text
MVP_ALIGNMENT = MVP-ALIGNED
SOURCE_PATH = LOCAL_FORMAL_PRODUCER_PATH
SYNTHETIC_DB_SEED = NO
REMOTE_FACT_COPY = NO
SYNC_WORKER_IMPORT = NO
```

The images prepare the already-selected formal local production path without manufacturing database rows outside the product acceptance path.

## Next gate

```text
NEXT_GATE = A1_LOCAL_FORMAL_PRODUCER_CONTROLLED_BRINGUP_AND_ACCEPTED_FACT_OBSERVATION
```

That successor requires separate Owner authority for producer container lifecycle and the intrinsic product-runtime DB writes/ACK behavior that occur when V-PLC + Collector run. This PASS does not authorize that successor automatically.
