# FV1B-A Wyse 3040 amd64 Debug Branch Packaging Report

## 报告名称

FV1B-A Wyse 3040 amd64 Debug Branch Packaging Report

## 任务名称

FV1B-A — Wyse 3040 amd64 Debug Branch Packaging and Full-Stack Deployment Bundle Preparation

## 执行 Thread

Integration

## 终端结论

PASS WITH RECOMMENDATIONS

本轮结论是 FV1B-A 本地 linux/amd64 packaging 与 full-stack bundle qualification PASS。它不是 Wyse 远程部署 PASS、Wyse runtime PASS、真实 PLC PASS、生产 acceptance、x86 正式产品化或 x86 support commitment。

状态边界：

    FV1B_A_AMD64_PACKAGING = PASS
    WYSE_DEPLOYMENT        = NOT_EXECUTED / NOT_CLAIMED
    WYSE_RUNTIME           = NOT_OBSERVED
    X86_FORMAL_PRODUCT_LINE = NOT_AUTHORIZED

## Scope 与 authority

本轮只执行 task file 授权的六个项目镜像 linux/amd64 构建、四个 exact upstream amd64 variant qualification、Wyse branch Compose/README/manifest/report 产物和本地静态验证。没有修改应用源码、依赖、package lock、root Compose、ARM 默认平台或运行时产品语义。

未继承 FV0/FV1A 之外的隐含 authority；没有执行 Wyse、Raspberry Pi、真实 PLC、SSH、SCP、remote HTTP、remote Docker、Compose lifecycle、数据库运行时或 Git push/tag。

## Task identity 与 fresh recovery

Task self-identity gate：PASS。

    path   = docs/thread_handoff/pm_task_20260817T0212Z_fv1b-a_wyse_amd64_branch_packaging.md
    type   = regular file / non-symlink
    bytes  = 22312
    SHA256 = 90c4b1832d2c77fa0b243b9522451fb1e06c0c03f824b162c311682578fdd56a

执行前 live repository recovery：

    physical cwd   = /Users/chenjie/Documents/MES/edge-mes-demo
    git top-level  = /Users/chenjie/Documents/MES/edge-mes-demo
    branch         = main
    HEAD           = efdd3decb0901ad79ce8e401327438c5b684b5dd
    origin/main    = 6226bf3fb716880a176f9eb642b8139cef3255a6
    ahead/behind   = 22 / 0
    staged count   = 0

执行前 tracked dirty 是预存的治理/状态文件：

    .agents/skills/edge-mes-pm-governance/SKILL.md
    AGENTS.md
    docs/current_status.md
    docs/thread_handoff/pm_operating_rules.md

执行前 untracked corpus 均被保留，未 stage、未删除、未 adoption。task file 本身验证为 untracked、unstaged、not ignored、not indexed。初始 exact untracked set 为：

    docs/reports/mvp_mainline_product_acceptance_cut_20260816.md
    docs/reports/mvp_product_recovery_route_correction_20260816.md
    docs/reports/r3_10ws_runtime_architecture_design_20260816.md
    docs/reports/real_plc_debug_field_validation_plan_v2_20260817.md
    docs/thread_handoff/branch_pm_goal_real_plc_debug_config_fv0_fv1a_20260817T0856.md
    docs/thread_handoff/branch_pm_goal_real_plc_fv0_integration_contract_20260817T0814.md
    docs/thread_handoff/chatgpt_pm_handoff_260815-2323.md
    docs/thread_handoff/chatgpt_pm_handoff_260816-1750.md
    docs/thread_handoff/owner_acceptance_mvp_20260816.md
    docs/thread_handoff/pm_task_20260817T0104Z_fv0-fv1a_real_plc_debug_config.md
    docs/thread_handoff/pm_task_20260817T0212Z_fv1b-a_wyse_amd64_branch_packaging.md
    docs/thread_handoff/r3_architecture_runtime_design_10ws_20260816T1112.md
    docs/thread_handoff/r3_same_goal_trace_history_identity_repair_20260816T1240.md
    docs/thread_handoff/shadow_pm_goal_mvp_mainline_product_acceptance_cut_20260816T1315.md
    docs/thread_handoff/shadow_pm_goal_mvp_owner_acceptance_blocker_repair_20260816T1437.md
    docs/thread_handoff/shadow_pm_goal_mvp_owner_reacceptance_dashboard_vplc_r4_20260816T2140.md
    docs/thread_handoff/shadow_pm_goal_mvp_owner_reacceptance_interaction_repair_r3_20260816T2001.md
    docs/thread_handoff/shadow_pm_goal_mvp_product_surface_continuity_repair_r2_20260816T1830.md
    docs/thread_handoff/shadow_pm_goal_mvp_station_summary_echarts_migration_20260816T2245.md
    docs/thread_handoff/shadow_pm_goal_mvp_trace_product_surface_v2_20260817T0814.md
    docs/thread_handoff/shadow_pm_goal_r1_product_continuity_trace_reintegration_20260816T0056Z.md
    docs/thread_handoff/shadow_pm_goal_r2_field_plc_deployment_configuration_foundation_20260816T0119Z.md
    docs/thread_handoff/shadow_pm_goal_r2b_plc_configuration_activation_and_collector_reload_20260816T0226.md
    docs/thread_handoff/shadow_pm_goal_r3_10ws_runtime_integration_20260816T1130.md

后续只观察到另一个 docs-only untracked handoff path：

    docs/thread_handoff/pm_task_20260817T0236Z_fv1a-debug-scope_station-scope-correction.md

该路径未被采用、修改、stage 或 commit。Git recovery 与 exact changed-path accounting 未发现 non-doc source concurrent mutation；sandbox 对只读 ps process scan 返回 operation not permitted，没有因此扩大任何权限。

## Execution lock inputs

首次仓库写入或 Docker build mutation 前已捕获并在本报告/manifest 中绑定：

- 项目 root、physical cwd、Git top-level、HEAD、origin/main、ahead/behind、staged count。
- task identity 与 task authority boundary。
- root docker-compose.yml entry identity。
- Docker host architecture、Docker server architecture、buildx builder 与 supported platforms。
- pre-existing dirty/untracked path set。

Docker host/buildx live facts：

    host architecture             = arm64
    Docker server                 = aarch64 / linux
    builder                       = colima / docker driver / running
    BuildKit                      = v0.30.0
    supported                   = linux/386, linux/amd64, linux/amd64/v2, linux/arm64

没有创建 disposable builder；没有改变 global/default builder；没有安装 emulation package。

## Platform boundary

    OFFICIAL_MAINLINE_PLATFORM = RASPBERRY_PI_ARM64
    FV1B_PLATFORM               = WYSE3040_AMD64_DEBUG_BRANCH_ONLY
    X86_FORMAL_PRODUCT_LINE    = NOT_AUTHORIZED

Wyse amd64 tag 与 root ARM-oriented Compose tag 分离。root docker-compose.yml 没有加入 platform: linux/amd64，也没有被替换、重命名或默认化。

## 六个项目镜像构建结果

所有项目镜像均使用 --platform linux/amd64、--load 和 FV1B-A-only tag。每个成功 tag 在首次成功后只做只读 inspect，没有 rebuild 或覆盖。

| logical service | tag | Dockerfile / context | result | OS / arch | local image ID |
| --- | --- | --- | --- | --- | --- |
| api | edge-mes-demo-api:fv1b-a-amd64 | api/Dockerfile / . | PASS | linux / amd64 | sha256:3502d5547f60452b7d39112565194eb59a929cd7ff373984f8fc9c052fdec8a1 |
| collector | edge-mes-demo-collector:fv1b-a-amd64 | collector/Dockerfile / . | PASS | linux / amd64 | sha256:b610997b45275a936d187501deae8b0401311db82addea3e9f4b811102f2458f |
| dashboard | edge-mes-demo-dashboard:fv1b-a-amd64 | frontend/Dockerfile / frontend | PASS | linux / amd64 | sha256:d73b87e2bf348bfe5b31ad8d29f12880383f3bf597e3ad89d74d7bf52d912d37 |
| s7-plc-sim | edge-mes-demo-s7-plc-sim:fv1b-a-amd64 | s7_plc_sim/Dockerfile / s7_plc_sim | PASS | linux / amd64 | sha256:6fcab39778d7f0667593e88f9c7eb6fceab6935bffb7ef507adc7f87a77823f1 |
| simulator | edge-mes-demo-simulator:fv1b-a-amd64 | simulator/Dockerfile / simulator | PASS | linux / amd64 | sha256:72b8e0cd642bd6b4ecad3978821abdb11229f48a82acfbc96396b76d4a8690ef |
| sync-worker | edge-mes-demo-sync-worker:fv1b-a-amd64 | sync_worker/Dockerfile / sync_worker | PASS | linux / amd64 | sha256:635d0f87b774a89db745a1f9a7da7586f83df615888e8350e05313de349efad1 |

Dashboard 第一次命令因从项目 root 使用了错误的 --file Dockerfile 路径，在读取 Dockerfile 前失败；没有产生 image 或 repository mutation。随后使用 frontend/Dockerfile 重跑成功。这不是 Dockerfile repair cycle。

## 四个 upstream image qualification

每个 exact ref 先通过 registry manifest inspection 确认 amd64 variant，再按该 variant digest pull 到本地并 inspect；Compose 使用 variant digest，不使用 ARM tag 的本地缓存。

| logical service | Compose image / amd64 variant | index digest | amd64 image ID | result |
| --- | --- | --- | --- | --- |
| postgres | postgres:16@sha256:56f243d2355bad7d2016b1e78b80da8ac9e7967b766be2bfbff84fe85ffa30bc | sha256:e17e86066e5ef83e0952a9347f5c792b7ece00972e2aa787a6986f471b3dd3d5 | sha256:56f243d2355bad7d2016b1e78b80da8ac9e7967b766be2bfbff84fe85ffa30bc | PASS |
| grafana | grafana/grafana:latest@sha256:e27e68cfd5795c1bea54950766078a02e84dfa3bafe0a4d0e5382f713dfd8e4e | sha256:ab5cb380e3ff3172d6c8bd2e7cfd31cce977d2881b260e1f5bc089bf0b759b43 | sha256:e27e68cfd5795c1bea54950766078a02e84dfa3bafe0a4d0e5382f713dfd8e4e | PASS |
| prometheus | prom/prometheus:latest@sha256:1147c92841726a6fef55fe6124491d6f85480f8de204f7d420304ca5bbd0a8f7 | sha256:508729e0e2d18e11fd742a5a5ca70e557b940a93948c3c95fd0123a6fd538b69 | sha256:1147c92841726a6fef55fe6124491d6f85480f8de204f7d420304ca5bbd0a8f7 | PASS |
| node-exporter | prom/node-exporter:latest@sha256:da83fae85603c4e47e6c68369a7d746e2dda683dc35ea2e234b4f171e0d92798 | sha256:1b4e4438faca4dd7e001dd445d161a4a2091b0fededa84093b3a8dfeae1f1be0 | sha256:da83fae85603c4e47e6c68369a7d746e2dda683dc35ea2e234b4f171e0d92798 | PASS |

四个 local variant inspect 均为 OS=linux、Architecture=amd64。没有 rewrite upstream tag，没有 push。

## Wyse Compose bundle

创建 path：

    deploy/wyse/docker-compose.wyse.yml

该文件代表完整的当前逻辑栈：

    api, collector, dashboard, grafana, node-exporter,
    postgres, prometheus, s7-plc-sim, simulator, sync-worker

实现边界：

- 六个项目 service 只消费独立 FV1B-A prebuilt tags，设置 pull_policy: never。
- 四个 upstream service 使用已验证的 amd64 variant digest。
- 所有十个 service 显式声明 platform: linux/amd64；该声明只存在于 deploy/wyse branch file。
- 保留 API、Collector、Dashboard、V-PLC/simulator、Grafana、Prometheus、node-exporter、sync-worker 的逻辑关系、ports、healthcheck、debug/demo credentials 与持久化语义。
- PostgreSQL、deployment-config、V-PLC、Grafana、Prometheus 使用 repository-relative bind paths。
- node-exporter 的 Linux host kernel paths 通过 WYSE_HOST_PROC_PATH、WYSE_HOST_SYS_PATH、WYSE_HOST_ROOT_PATH configurable；没有 Mac-only /Users、/Volumes、/private、Homebrew 或临时目录 source path。
- Compose 不包含 build 字段，不会把 Wyse branch 重新绑定到当前 ARM local tag。

静态验证：

    docker compose -f deploy/wyse/docker-compose.wyse.yml config --quiet = PASS
    Compose lifecycle start/stop/recreate                         = NOT RUN
    MAC_ONLY_ABSOLUTE_PATHS                                      = NONE

## Durable artifacts

| path | bytes | SHA-256 | role |
| --- | ---: | --- | --- |
| deploy/wyse/docker-compose.wyse.yml | 7163 | e49483a196709390b4b5f1232b8619e8e892be5e8c53a2cc7a0d2bd69a346a98 | Wyse full-stack Compose |
| deploy/wyse/README.md | 4935 | b994754e98ea876a6faf3048009157f8153434e6ad211ba11d95a03f9e5f6e7e | FV1B-B prerequisites/operator sequence |
| docs/reports/evidence/fv1b-a/amd64_image_manifest.json | 6936 | 0c5339f9a5674b75bc63998ad6926b7c714148ae28870e60ea577578f3ecb694 | canonical image/architecture manifest |
| docs/reports/evidence/fv1b-a/manifest.sha256 | 311 | 8d84d5475cddf0659037a8b84148afd12cfd6915f75ce36287565767d2bc5108 | sorted SHA manifest for the three exact bundle/manifest artifacts |

manifest.sha256 按 repository-relative path 排序，仅覆盖：

    deploy/wyse/README.md
    deploy/wyse/docker-compose.wyse.yml
    docs/reports/evidence/fv1b-a/amd64_image_manifest.json

JSON manifest 的 images 以 logical_service 排序，包含 source HEAD、platform、project/upstream kind、tag/ref、OS/architecture、immutable image ID、registry index/variant digest、creation time 和 result。

## Repairs、validation 与 continuity

Dockerfile portability repair count：

    Dockerfile repairs = 0 / 2 authorized cycles

Task artifact mechanical repair：

    Compose interpolation quoting correction = 1

该 correction 只把生成 artifact 中错误保留的反斜杠修正为 Compose 需要的 interpolation placeholder syntax，未改变服务、image、platform、credential、volume、authority 或产品语义；不计入 Dockerfile portability repair budget。没有 dependency upgrade、package-lock mutation、application source mutation 或 x86-only shared-mainline hack。

通过的检查：

- task identity gate PASS。
- physical cwd 与 Git top-level PASS。
- Git baseline、ahead/behind、staged count、dirty/untracked accounting PASS。
- Docker host/buildx platform support PASS。
- 六个 project image build 与 post-build inspect PASS。
- 四个 upstream manifest/amd64 variant pull 与 post-pull inspect PASS。
- JSON schema/10-image count/lexicographic logical service order/全 linux-amd64 check PASS。
- docker compose config --quiet PASS。
- MAC-only absolute path scan PASS。
- untracked artifact diff --check PASS。
- git diff --check PASS。
- root docker-compose.yml entry/final identity continuity PASS。

受保护 root Compose：

    entry bytes  = 6191
    entry SHA256 = 5e7009a5870919313c4355dd8af7e6f92194b62307bc74d0030f43a47719e483
    final bytes  = 6191
    final SHA256 = 5e7009a5870919313c4355dd8af7e6f92194b62307bc74d0030f43a47719e483
    result       = unchanged

## Changed paths、Git 与 boundary counters

Task-owned changed paths：

    deploy/wyse/docker-compose.wyse.yml
    deploy/wyse/README.md
    docs/reports/evidence/fv1b-a/amd64_image_manifest.json
    docs/reports/evidence/fv1b-a/manifest.sha256
    docs/reports/fv1b_a_wyse_amd64_branch_packaging_report_20260817.md

六个 Dockerfile、root docker-compose.yml、application source、config/mapping、DB schema、dependency/package-lock 均未改变。预存 tracked dirty files、untracked corpus 和 authoritative task file 均未 stage。

报告写入时、exact optional stage 之前的 Git snapshot：

    branch       = main
    HEAD         = efdd3decb0901ad79ce8e401327438c5b684b5dd
    origin/main  = 6226bf3fb716880a176f9eb642b8139cef3255a6
    ahead/behind = 22 / 0
    staged       = 0
    pushed       = NO
    tag          = NO

Task file 授权在本地 PASS validation 后 exact-path stage 与一次 commit，commit message 必须为：

    build: prepare wyse amd64 debug deployment bundle

本报告写入时尚未消费该 optional Git authority；最终 stage/commit/push/tag 状态由当前 Thread 的 closeout manifest 以 live Git 事实报告。

Boundary counters：

    WYSE_REMOTE_ACTION         = 0
    RASPBERRY_PI_REMOTE_ACTION = 0
    REAL_PLC_CONNECT            = 0
    REAL_PLC_READ               = 0
    REAL_PLC_WRITE              = 0
    REMOTE_MUTATION             = 0
    COMPOSE_LIFECYCLE           = 0
    CONTAINER_START             = 0
    CONTAINER_STOP              = 0
    DOCKER_PUSH                 = 0

## Blockers 与 recommendations

Blockers：none for FV1B-A local amd64 packaging claim。

Recommendations：

1. PM intake 必须把本轮结论限定为 x86 DEBUG BRANCH ONLY；不要把 local image inspect、Compose config 或 image pull 解释为 Wyse runtime/production evidence。
2. 后续 FV1B-B 必须先冻结 Wyse host/IP、SSH user/port、host-key identity、OS/arch、Docker/Compose、resource/ports、remote call budget 与 load/pull source。
3. FV1B-B full-stack start 后必须单独采集 health/resource/persistence evidence；本轮不存在 FULL_COMPOSE_START、PERSISTENT_STORAGE 或 LOCAL_HTTP_SURFACES runtime PASS。
4. 完成 Wyse debugging 后执行返回 Raspberry Pi / ARM64 mainline；本轮不产生 x86 formal product line。

## Next gate

single next gate：

    Mainline PM intake of FV1B-A

之后只有在 Owner 提供并由 PM 冻结 exact Wyse remote identity 与 remote call/mutation budget 后，才可另行发布 Level-2 FV1B-B Wyse 3040 Remote Full-Stack Deployment Qualification。FV1B-A 不授权 remote deployment、FV2、FV3、real PLC Read_Done、FV2 address reconciliation、x86 release、push、tag、merge 或任何后续 phase。

## MVP 路径一致性

    classification = MVP-ALIGNED WITH BACKLOG ITEMS

本轮直接支持已批准的 Wyse debug branch portability/deployment preparation，并防止 ARM mainline image 被误用于 amd64。没有引入产品能力、数据库/API 语义、生产威胁模型、审计/保留框架或新 runtime topology；bundle 只是任务明确要求的 deployment artifact。FV1B-B 的真实设备/remote evidence 是后续独立 Level-2 gate，不在本轮膨胀。

## Thread 输出 / 上下文评估

- 本次输出长度：中。
- 当前 Integration Thread 可以完成本轮 exact artifact、validation 与 Git closeout。
- Owner 是否应把下一轮手工分发到新的 top-level Thread：yes；FV1B-B 是新的 remote Level-2 authority，需新的 exact Wyse identity 与预算。
- task-file sub-agent 计划：yes；原计划为一个 read-only Docker/build specialist 与一个 read-only manifest reviewer。
- task-file sub-agent 实际使用：no；本轮未调用 sub-agent。六个 build、Compose integration、manifest 与 continuity audit 在同一 checkout 内由 parent Thread 连续完成，未扩大 authority。
- executing Thread 没有创建、切换或 fork top-level Thread。
