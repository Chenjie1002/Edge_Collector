# FV1B-A Wyse 3040 amd64 Debug Bundle

本目录是 FV1B-A 的本地打包产物，面向后续、另行授权的 FV1B-B Wyse 3040 全栈部署资格验证。本文只定义部署前提与操作顺序，不构成 SSH、SCP、远程 Docker、Compose 生命周期、真实 PLC 或生产操作授权；FV1B-A 本轮未执行这些动作。

## 部署前必须冻结的 Wyse 事实

在 FV1B-B 任务中，先记录并由 PM 冻结：

- Wyse 3040 主机名/IP、SSH user/port、host-key identity 或等价可信主机身份。
- uname -m 必须为 x86_64，且 /etc/os-release、Docker Engine、Docker Compose plugin 版本可追溯。
- RAM、swap、root/data 文件系统容量与剩余空间。
- 端口 5432、8000、8100、8200、3000、3001、9090、9100 的占用情况。
- 部署 checkout 的实际目录及 data 目录备份/回滚位置。
- 允许的镜像来源（预加载 bundle 或已冻结 registry digest）和 pull/load 预算。

若上述事实缺失，停止在 FV1B-B preflight，不推断 Wyse identity。真实 PLC 连接、读取、写入在本 bundle 中仍均为 0。

## 镜像与持久化前提

Compose 使用以下六个预构建项目镜像，必须以完全相同的本地 tag 提供；这些 tag 是 FV1B-A linux/amd64 debug tag，不是 ARM mainline tag：

    edge-mes-demo-api:fv1b-a-amd64
    edge-mes-demo-collector:fv1b-a-amd64
    edge-mes-demo-dashboard:fv1b-a-amd64
    edge-mes-demo-s7-plc-sim:fv1b-a-amd64
    edge-mes-demo-simulator:fv1b-a-amd64
    edge-mes-demo-sync-worker:fv1b-a-amd64

四个 upstream runtime image 已固定为 amd64 variant digest：

    postgres:16@sha256:56f243d2355bad7d2016b1e78b80da8ac9e7967b766be2bfbff84fe85ffa30bc
    grafana/grafana:latest@sha256:e27e68cfd5795c1bea54950766078a02e84dfa3bafe0a4d0e5382f713dfd8e4e
    prom/prometheus:latest@sha256:1147c92841726a6fef55fe6124491d6f85480f8de204f7d420304ca5bbd0a8f7
    prom/node-exporter:latest@sha256:da83fae85603c4e47e6c68369a7d746e2dda683dc35ea2e234b4f171e0d92798

本仓库不包含二进制镜像 archive。FV1B-B 必须使用已独立授权的 docker load 产物，或从允许的 registry pull 上述精确 digest；不得以 ARM tag 替代，不得把本 README 当作 push 权限。

部署 checkout 应保留以下相对持久化路径，并在启动前确认其备份策略：

    data/postgres
    data/deployment-config
    data/vplc
    data/grafana
    data/prometheus

默认 debug/demo 认证语义保持现状：POSTGRES_DB=edge_mes、POSTGRES_USER=edge_mes、POSTGRES_PASSWORD=edge_mes_password，Grafana admin/admin。若 FV1B-B 需要替换凭据，必须同时提供一致的 POSTGRES_* 与 DATABASE_URL/GRAFANA_* 输入；本 bundle 不生成生产 secret。

## FV1B-B 操作顺序

以下命令只作为后续 FV1B-B 的 operator sequence；本轮未在 Wyse 上执行。

1. 在已冻结身份的 Wyse 上做只读 preflight：确认 uname -m、/etc/os-release、Docker/Compose 版本、RAM/swap、磁盘空间和端口占用；确认当前 checkout 是 bundle 根目录。

2. 准备相对 data 路径并完成备份/回滚记录：

    mkdir -p data/postgres data/deployment-config data/vplc data/grafana data/prometheus

   不删除既有 data，不使用 docker system prune，不改变 root docker-compose.yml。

3. 通过独立授权的 archive load 或 exact registry pull 提供六个项目 tag及四个 upstream digest。随后对每个镜像做只读检查，要求 OS=linux、Architecture=amd64，并确认项目 tag 与 manifest 中的 image ID 一致。

4. 运行 Compose preflight，不启动容器：

    docker compose -f deploy/wyse/docker-compose.wyse.yml config --quiet

   若 preflight 失败，停止并回到 bundle/输入修正，不在 Wyse 上修改应用源、依赖或 root Compose。

5. 在 FV1B-B 明确授权后启动完整逻辑栈：

    docker compose -f deploy/wyse/docker-compose.wyse.yml up -d

6. 做 bounded health/resource check：记录 docker compose ps、各服务启动/health 状态、docker stats --no-stream、磁盘增长和端口可达性；至少检查 API /health（8000）、Dashboard /health（3001）、Grafana /api/health（3000）、Prometheus /-/ready（9090）与 Postgres pg_isready。记录 V-PLC/simulator/collector/sync-worker 的日志摘要，不把 Compose started 误报为 Wyse production readiness。

7. FV1B-B 的 full-stack 结果必须单独区分：本 bundle 只能证明 amd64 packaging/config 资产，不证明真实 PLC、生产部署或产品化。任何真实 PLC connect/read/write 都要等待另一个明确的设备 authority。

8. 停止或回滚时，保留持久化 data，先记录当前 Compose/image identity，再在独立授权下执行：

    docker compose -f deploy/wyse/docker-compose.wyse.yml down

   回滚概念是恢复上一份已核验的 checkout、Compose bundle、镜像 tag/digest 和 data 备份；不得用 down -v、system prune 或未核验的 tag 覆盖证据。
