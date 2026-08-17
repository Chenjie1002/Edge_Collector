# FV1B-A-R1 Wyse 3040 amd64 Debug Bundle Refresh Report

## 报告名称

FV1B-A-R1 Wyse 3040 amd64 Debug Bundle Refresh Report

## 任务名称

FV1B-A-R1 — Refresh Wyse 3040 amd64 Debug Bundle to FV1A Debug-Scope Source

## 执行 Thread

Integration

## 终端结论

**PASS WITH RECOMMENDATIONS**，仅限本地 `linux/amd64` bundle/image packaging、静态 source-feature verification 与 Compose config evidence。

本轮没有 Wyse runtime/deployment evidence，没有启动 project Compose，没有访问 Raspberry Pi，没有连接真实 PLC，也没有执行 push/tag。该结果明确保持：

```text
OFFICIAL_MAINLINE_PLATFORM = RASPBERRY_PI_ARM64
FV1B_R1_PLATFORM           = WYSE3040_AMD64_DEBUG_BRANCH_ONLY
X86_FORMAL_PRODUCT_LINE   = NOT_AUTHORIZED
```

## 1. Scope 与 authority boundary

本轮只执行 FV1B-A-R1 task file 授权的以下动作：从 exact source HEAD 重建六个 `linux/amd64` project images；复用四个冻结 upstream digest；生成新的 R1 Wyse Compose、README、十镜像 canonical manifest、三文件 SHA manifest 与 durable report；验证 Debug Pilot Scope source 已进入 API/Dashboard/Collector bundle；执行 task-file-defined exact local commit。

没有修改 Dockerfile、application source、dependency、package lock、root Compose、历史 FV1B-A artifact 或运行时配置。没有继承 predecessor task 或其他 Thread 的 authority。FV1B-B、远端 Wyse、Raspberry Pi、真实 PLC、Candidate activation、FV2、FV3、x86 productization、push 与 tag 均不在本轮 authority 内。

## 2. Task identity 与 fresh recovery

Task self-identity gate：**PASS**。

```text
path   = docs/thread_handoff/pm_task_20260817T0854Z_fv1b-a-r1_amd64-bundle-refresh.md
type   = regular / non-symlink
bytes  = 22670
SHA256 = 9323c1931c605fb1674e379b7c8c41cb93f35a214792f2ea8e4a705f0f04658a
```

执行锁与首次 build 前 live facts：

```text
physical cwd  = /Users/chenjie/Documents/MES/edge-mes-demo
git top-level = /Users/chenjie/Documents/MES/edge-mes-demo
branch        = main
HEAD          = 6d4f41365120677e73ce80290b2417ce6da4971e
origin/main   = 6226bf3fb716880a176f9eb642b8139cef3255a6
ahead/behind  = 24 / 0
staged        = 0
```

工作树中预存的 tracked governance dirtiness 为 `.agents/skills/edge-mes-pm-governance/SKILL.md`、`AGENTS.md`、`docs/current_status.md` 与 `docs/thread_handoff/pm_operating_rules.md`；预存 untracked handoff/report/task corpus 保持原样。首次 build 前没有 uncommitted non-doc application/deployment mutation，也没有 staged path。

## 3. Docker/buildx execution lock

```text
host uname            = arm64
Docker server         = linux / aarch64 (arm64), 29.5.2
builder               = colima / docker driver / running
BuildKit              = v0.30.0
supported platforms   = linux/386, linux/amd64, linux/amd64/v2, linux/arm64
```

没有创建 disposable builder，没有改变 global/default builder，没有安装 emulation package。六个 build 均使用已有 Dockerfile/context、`--platform linux/amd64`、`--load` 与新的 R1 tag。

Dashboard 曾有一次命令级路径错误：首次命令在读取 Dockerfile 前以 root-relative `--file Dockerfile` 失败，未产生 image/tag 或 repository mutation；随后使用 `frontend/Dockerfile` + `frontend` context 成功。该命令错误不是 Dockerfile repair，repair count 仍为 `0`。

## 4. 六个 R1 project images

所有成功 tag 在首次成功后只做只读 inspect，未 rebuild/overwrite。

| logical service | exact R1 tag | Dockerfile / context | result | OS / architecture | immutable local image ID / digest | created at |
| --- | --- | --- | --- | --- | --- | --- |
| api | `edge-mes-demo-api:fv1b-a-r1-amd64` | `api/Dockerfile` / `.` | PASS | linux / amd64 | `sha256:b31506cc06461f2631a4637b29834d84be298a0483cfd93cb661fcca23e086e6` | `2026-08-17T17:04:04.224884548+08:00` |
| collector | `edge-mes-demo-collector:fv1b-a-r1-amd64` | `collector/Dockerfile` / `.` | PASS | linux / amd64 | `sha256:d8fcef3f09533962a769dbfb39712728c82f13056093f004266bbcb42f70b816` | `2026-08-17T17:04:12.574722426+08:00` |
| dashboard | `edge-mes-demo-dashboard:fv1b-a-r1-amd64` | `frontend/Dockerfile` / `frontend` | PASS | linux / amd64 | `sha256:9c181e0821f9b720fe4bfe9c6c9c7851a85145251a5c147f4ad4aa1338771a05` | `2026-08-17T17:05:30.891783382+08:00` |
| s7-plc-sim | `edge-mes-demo-s7-plc-sim:fv1b-a-r1-amd64` | `s7_plc_sim/Dockerfile` / `s7_plc_sim` | PASS | linux / amd64 | `sha256:d0037f692ea5e607f4cfdc5e543ee8e2fbb702cc2ae02d6ce19dc18b64e3c98e` | `2026-08-17T10:36:07.567492192+08:00` |
| simulator | `edge-mes-demo-simulator:fv1b-a-r1-amd64` | `simulator/Dockerfile` / `simulator` | PASS | linux / amd64 | `sha256:95d21476a3448f56c3de83dfd2a3ab48b479f9a02198ff8896ebc9c36900833b` | `2026-08-17T10:35:08.364574374+08:00` |
| sync-worker | `edge-mes-demo-sync-worker:fv1b-a-r1-amd64` | `sync_worker/Dockerfile` / `sync_worker` | PASS | linux / amd64 | `sha256:1f12085e5e919b404c2b10dddfb54fb21f85b662b142163bd1b8041501ad38ef` | `2026-08-17T10:36:39.610829244+08:00` |

六个 project build context 在首次 build 前均与 HEAD clean；关键 Debug-Scope source 的 live hash 与 `git show HEAD:<path>` hash 完全一致。没有 Dockerfile/source/dependency repair。

## 5. 四个 frozen upstream amd64 refs

R1 没有刷新 `latest`，没有 pull 新 digest；只对本地已有 exact frozen references 做只读 inspect。四个 Compose ref、amd64 variant 与本地 immutable identity 完全一致：

| logical service | exact frozen Compose ref | OS / architecture | immutable image ID / variant digest | created at | result |
| --- | --- | --- | --- | --- | --- |
| postgres | `postgres:16@sha256:56f243d2355bad7d2016b1e78b80da8ac9e7967b766be2bfbff84fe85ffa30bc` | linux / amd64 | `sha256:56f243d2355bad7d2016b1e78b80da8ac9e7967b766be2bfbff84fe85ffa30bc` | `2026-08-13T19:16:08.705640299Z` | PASS |
| grafana | `grafana/grafana:latest@sha256:e27e68cfd5795c1bea54950766078a02e84dfa3bafe0a4d0e5382f713dfd8e4e` | linux / amd64 | `sha256:e27e68cfd5795c1bea54950766078a02e84dfa3bafe0a4d0e5382f713dfd8e4e` | `2026-08-07T00:43:24Z` | PASS |
| prometheus | `prom/prometheus:latest@sha256:1147c92841726a6fef55fe6124491d6f85480f8de204f7d420304ca5bbd0a8f7` | linux / amd64 | `sha256:1147c92841726a6fef55fe6124491d6f85480f8de204f7d420304ca5bbd0a8f7` | `2026-07-30T12:01:58.514082203Z` | PASS |
| node-exporter | `prom/node-exporter:latest@sha256:da83fae85603c4e47e6c68369a7d746e2dda683dc35ea2e234b4f171e0d92798` | linux / amd64 | `sha256:da83fae85603c4e47e6c68369a7d746e2dda683dc35ea2e234b4f171e0d92798` | `2026-07-14T12:11:16.849376637Z` | PASS |

## 6. R1 Compose bundle

新文件：`deploy/wyse/docker-compose.wyse-r1.yml`。

与 accepted FV1B-A Compose 的 canonical diff 只有：

- 顶部 R1/source-head identification comment；
- 六个 project image 从 `fv1b-a-amd64` 替换为对应 `fv1b-a-r1-amd64`。

其余十服务逻辑栈、service names、ports、volumes、environment、healthcheck、depends_on、`platform: linux/amd64` 与四个 upstream refs 均保持一致。静态审计结果：

```text
services = 10
logical services = api, collector, dashboard, grafana, node-exporter, postgres, prometheus, s7-plc-sim, simulator, sync-worker
project refs = exactly 6 R1 tags
upstream refs = exactly 4 frozen digests
platforms = linux/amd64 for all services
docker compose -f deploy/wyse/docker-compose.wyse-r1.yml config --quiet = PASS
```

没有 `up`、`down`、`restart`、`recreate` 或任何 project Compose lifecycle。

## 7. Debug-Scope feature packaging proof

三个 bounded static image filesystem inspections 已执行，均使用 `docker run --rm --network none --platform linux/amd64`、无 volume/device、无产品进程、无 project network；总 invocation count 为 `3`。

### API image

`edge-mes-demo-api:fv1b-a-r1-amd64` 中发现 `debug_scope`、`debug_ready`、`ready_to_activate` markers。image 内文件 hash 与 build 前 exact HEAD source hash 一致：

```text
/app/app/services/deployment_plc.py          = 26935a630fdb8524cbd4cd2c01ef0544a1daf28b39393696568cb96ea1c99ee5
/app/common/line_config/debug_contract.py    = 2bd8d0ca72839966f936ea77e496b6f9f23a46aa49481f87c045b776bc7f1a96
/app/common/line_config/runtime_projection.py = 1a3dda7d79ebce387e3c84ab99b9454247f968b0ad1b61bf7ae52333df636065
```

### Collector/common image

`edge-mes-demo-collector:fv1b-a-r1-amd64` 中发现 `configured_station_ids`、`expected_scopes`、`debug_scope`、`selected_ids` markers；这绑定了 Collector read-plan scope validation 与 common scoped projection support。image 内 `event_collector.py` hash 为 `628b5869402fe3e3e03f86a443f44d74d435a9c523b290d411808a2bf0983781`，两个 common 文件 hash 与 API image 相同并匹配 HEAD。

### Dashboard image

`edge-mes-demo-dashboard:fv1b-a-r1-amd64` 的 compiled Next standalone/static bundle 中发现 `Debug Pilot Scope`、`debug_ready`、`ready_to_activate` markers。该证据证明 Dashboard scope selector/readiness strings 已进入 R1 compiled image；不是 browser visual acceptance 或 Wyse runtime evidence。

上述 image identity 与 source HEAD 的关系由以下两层证据共同绑定：project build contexts 在 build 前对 HEAD clean；API/Collector image embedded source hashes 与 HEAD source hashes 机械相等；Dashboard compiled bundle 包含当前 HEAD 的 Debug Pilot UI markers。没有 remote container execution。

## 8. New artifact identities

Artifact SHA manifest：`docs/reports/evidence/fv1b-a-r1/manifest.sha256` 按 repository-relative path 排序，并且只覆盖三项新 bundle artifact；durable report 不包含在 SHA manifest 中。

| path | bytes | SHA-256 | role |
| --- | ---: | --- | --- |
| `deploy/wyse/docker-compose.wyse-r1.yml` | 7292 | `3f50c41311d000e433864ba41ff4f2350a9f176ee23e58f2bc299bf91a360734` | R1 ten-service Wyse Compose |
| `deploy/wyse/README-r1.md` | 2658 | `5160d319034fd7bc62816b43522cebe2031b7f274b0a364e5e8532a25ccefc0b` | R1 operator/bundle boundary note |
| `docs/reports/evidence/fv1b-a-r1/amd64_image_manifest.json` | 11181 | `5be22b469df44771f2cf39f0f57247c0bc560c07109627ff342a7b5dba2f2bbc` | canonical ten-image manifest |
| `docs/reports/evidence/fv1b-a-r1/manifest.sha256` | 320 | `13927397b9ccf824c3636987b5d118fa68512313a8d5f106e72a0dfa100d9ba3` | exact three-artifact SHA manifest |

JSON manifest validation：10 images；logical service ascending；all `linux/amd64`；六个 project image 均带 exact source HEAD/tag/build result；四个 upstream `registry_variant_digest` 与 frozen refs 完全一致。`sha256sum -c docs/reports/evidence/fv1b-a-r1/manifest.sha256`：3/3 PASS。

## 9. Protected continuity

首次 build/write 前 entry identities 与最终 audit 均保持一致：

| protected path | bytes | SHA-256 | final |
| --- | ---: | --- | --- |
| `docker-compose.yml` | 6191 | `5e7009a5870919313c4355dd8af7e6f92194b62307bc74d0030f43a47719e483` | unchanged |
| `deploy/wyse/docker-compose.wyse.yml` | 7163 | `e49483a196709390b4b5f1232b8619e8e892be5e8c53a2cc7a0d2bd69a346a98` | unchanged |
| `deploy/wyse/README.md` | 4935 | `b994754e98ea876a6faf3048009157f8153434e6ad211ba11d95a03f9e5f6e7e` | unchanged |
| `docs/reports/evidence/fv1b-a/amd64_image_manifest.json` | 6936 | `0c5339f9a5674b75bc63998ad6926b7c714148ae28870e60ea577578f3ecb694` | unchanged |
| `docs/reports/evidence/fv1b-a/manifest.sha256` | 311 | `8d84d5475cddf0659037a8b84148afd12cfd6915f75ce36287565767d2bc5108` | unchanged |
| `docs/reports/fv1b_a_wyse_amd64_branch_packaging_report_20260817.md` | 17229 | `cfda17809e9a87771caa533ac5cdf47d2b87d5afd6c69eb3034f9ea71a8d315d` | unchanged |

历史 FV1B-A artifact 未覆盖、未刷新、未 stage。root Compose 未添加 `platform: linux/amd64`，Raspberry Pi/ARM64 仍为 mainline/default。

## 10. Changed paths 与 Git closeout

Task-owned changed paths exactly：

```text
deploy/wyse/docker-compose.wyse-r1.yml
deploy/wyse/README-r1.md
docs/reports/evidence/fv1b-a-r1/amd64_image_manifest.json
docs/reports/evidence/fv1b-a-r1/manifest.sha256
docs/reports/fv1b_a_r1_wyse_amd64_bundle_refresh_report_20260817.md
```

在 report/artifact 写入、最终静态审计与 exact stage 之前：

```text
HEAD         = 6d4f41365120677e73ce80290b2417ce6da4971e
origin/main  = 6226bf3fb716880a176f9eb642b8139cef3255a6
ahead/behind = 24 / 0
staged       = 0
```

仅允许上述五个 R1 path 进入 exact stage/commit；authoritative task file、历史 FV1B-A artifacts、治理 dirty files 与 untracked corpus 均排除。commit message：

```text
build: refresh wyse amd64 debug bundle
```

本报告作为最后一个 task-owned file 写入；exact local commit 在本报告/manifest 完成最终 validation 后执行。最终 commit SHA、post-commit HEAD、post-commit staged count 与 ahead count 以当前 Thread closeout 的 live Git evidence 为准；push/tag 保持 `NO`。

## 11. Boundary counters

```text
WYSE_REMOTE_ACTION         = 0
RASPBERRY_PI_REMOTE_ACTION = 0
REAL_PLC_CONNECT           = 0
REAL_PLC_READ              = 0
REAL_PLC_WRITE             = 0
REMOTE_MUTATION            = 0
PROJECT_COMPOSE_LIFECYCLE  = 0
DOCKER_PUSH                = 0
FROZEN_UPSTREAM_REFRESH    = 0
DOCKERFILE_REPAIR_CYCLES   = 0
STATIC_DEBUG_IMAGE_RUNS    = 3
```

## 12. Blockers 与 recommendations

Blockers：none for the authorized local FV1B-A-R1 amd64 bundle claim。

Recommendations：

1. Mainline PM intake 必须把本轮结果限定为 `x86 DEBUG BRANCH ONLY`，不得把 local image inspect、compiled marker 或 Compose config 解释为 Wyse runtime/deployment/production evidence。
2. 后续 FV1B-B 必须使用 `deploy/wyse/docker-compose.wyse-r1.yml`，不得静默回退历史 FV1B-A Compose；开始前另行冻结 Wyse exact identity 与 remote budgets。
3. FV1B-B 应单独采集 health、resource、persistence 与 local HTTP evidence；本轮没有 full-stack start、persistent storage 或 Wyse runtime PASS。
4. Wyse debugging 完成后返回 Raspberry Pi / ARM64 mainline；本任务不产生 x86 formal support 或 productization authority。

## 13. Next gate

single next gate：**Mainline PM intake of FV1B-A-R1**。

若 PM 接受本报告与 exact local commit，才可在新的 Level-2 task 中冻结 Wyse remote identity、remote call/mutation budget，并另行发布 FV1B-B Wyse 3040 Remote Full-Stack Deployment Qualification。FV1B-B 必须绑定本 R1 Compose；不得从 R1 PASS 推断 remote deployment、real PLC、FV2/FV3、Raspberry Pi production acceptance 或 x86 formal release。

## 14. MVP 路径一致性

```text
classification = MVP-ALIGNED WITH BACKLOG ITEMS
```

R1 直接支持已批准的 Wyse amd64 debug-branch packaging 与 FV1A Debug-Scope capability transport，防止旧 project images 与当前 source HEAD 混用。没有引入产品行为、数据库/API 语义、生产威胁模型、审计/保留框架或新 runtime topology。验证强度与 local package claim 相称，未把静态证据升级为现场/生产证据。

## 15. Thread 输出 / 上下文评估

- 本次 durable output：中等长度；完整 evidence 已保存在本 report 与三个 R1 artifacts。
- 当前 Integration Thread 可以完成本轮 closeout，但下一 gate 是新的 remote Level-2 authority，Owner 应手工分发新 top-level Thread。
- task-file sub-agent 计划：`no` / exact scope `none`；实际 sub-agent usage：`no`。六个 image、Compose、manifest、source-feature 与 continuity audit 必须在同一 execution lock 内保持一致，未拆分。
- 本 Thread 未创建、切换或 fork top-level Thread。
