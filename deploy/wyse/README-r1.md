# FV1B-A-R1 Wyse 3040 amd64 Debug Bundle

本目录是 FV1B-A-R1 的本地 `linux/amd64` 调试 bundle，所有六个 project image 均从 source HEAD `6d4f41365120677e73ce80290b2417ce6da4971e` 重新构建。边界固定为：`X86_FORMAL_PRODUCT_LINE=NOT_AUTHORIZED`、`FV1B_R1_PLATFORM=WYSE3040_AMD64_DEBUG_BRANCH_ONLY`。官方主线仍是 `OFFICIAL_MAINLINE_PLATFORM=RASPBERRY_PI_ARM64`。

本轮没有 Wyse runtime/deployment evidence：没有 SSH、SCP、remote Docker、Compose lifecycle、远端 HTTP、真实 PLC 或 Raspberry Pi action。R1 只证明本地 amd64 image/package 与静态 Compose 资产，不证明 Wyse 可达、已部署、已启动、持久化或生产 acceptance。

## R1 source 与 project images

R1 bundle source：

    6d4f41365120677e73ce80290b2417ce6da4971e

六个 project image 必须使用以下精确 debug-only tags：

    edge-mes-demo-api:fv1b-a-r1-amd64
    edge-mes-demo-collector:fv1b-a-r1-amd64
    edge-mes-demo-dashboard:fv1b-a-r1-amd64
    edge-mes-demo-s7-plc-sim:fv1b-a-r1-amd64
    edge-mes-demo-simulator:fv1b-a-r1-amd64
    edge-mes-demo-sync-worker:fv1b-a-r1-amd64

## Frozen upstream references

以下四个 upstream amd64 variant digest 从 FV1B-A 原样冻结，R1 不刷新到更新的 `latest`：

    postgres:16@sha256:56f243d2355bad7d2016b1e78b80da8ac9e7967b766be2bfbff84fe85ffa30bc
    grafana/grafana:latest@sha256:e27e68cfd5795c1bea54950766078a02e84dfa3bafe0a4d0e5382f713dfd8e4e
    prom/prometheus:latest@sha256:1147c92841726a6fef55fe6124491d6f85480f8de204f7d420304ca5bbd0a8f7
    prom/node-exporter:latest@sha256:da83fae85603c4e47e6c68369a7d746e2dda683dc35ea2e234b4f171e0d92798

R1 Compose 保留完整十服务逻辑栈与原有 ports、volumes、environment、health dependencies。相对路径以 bundle checkout 为根；本仓库不包含二进制镜像 archive，也不生成生产 secret。

## FV1B-B boundary

后续 FV1B-B 若获 PM 单独授权，**必须使用 `deploy/wyse/docker-compose.wyse-r1.yml`，不得回退到历史 `deploy/wyse/docker-compose.wyse.yml`**。FV1B-B 还必须先冻结 Wyse host/IP、SSH identity、OS/arch、Docker/Compose、资源/端口和 remote budget；本 README 不构成这些 authority。

FV1B-B 的第一步只能是 read-only preflight 与 `docker compose -f deploy/wyse/docker-compose.wyse-r1.yml config --quiet`。只有新的 Level-2 task 明确授权后，才能执行 Wyse Compose lifecycle；任何真实 PLC connect/read/write 仍需独立设备 authority。

R1 完成后，调试工作返回 Raspberry Pi / ARM64 mainline；不从本 bundle 推断 x86 productization、正式支持、FV2、FV3 或整体 release completion。
