# Sprint 4 D2-R7A Collector Image Package-closure Repair

## 1. Task / authority

```text
Task:
Data-first Gate D2-R7A — Repair the Collector Image Package Closure and Add a Container Regression Gate

Authority ID:
SPRINT4-D2-R7A-COLLECTOR-PACKAGE-CLOSURE-9e0aba2

Authority type:
LOCAL SOURCE IMPLEMENTATION AND CONTAINER VALIDATION

Remote SSH authority: NONE
Remote deployment authority: NONE
DB/schema authority: NONE
V-PLC/PLC authority: NONE
Product-data authority: NONE
```

唯一目标是让 Collector image 包含运行时导入闭包中的仓库根级 `common` package，并通过隔离 container import/static-startup 验证。本次没有 SSH、远端文件、Collector activation、Compose lifecycle、DB/API/V-PLC 或产品数据操作。

## 2. D2-R6-R1 intake

已读取：`docs/reports/sprint4_d2_r6_r1_new_collector_remote_config_static_compatibility_retry.md`。

保留的 intake 结论：

```text
D2-R6-R1:
HOLD / NEW_IMAGE_STATIC_STARTUP_FAILED / IMPORT_PREREQUISITE_FAILED

New image source hashes: MATCHED
Failure: ModuleNotFoundError: No module named 'common'
Remote mapping: PHASE1_CONFIG_MATCH
Mapping validation: NOT REACHED
Remote mutation: 0
```

准确 import chain：

```text
app.main
-> app.services.event_detector
-> app.services.storage
-> app.services.accepted_station_event_fact
-> app.services.station_event_adapter
-> common.station_event
-> ModuleNotFoundError
```

本次没有重新调查远端 mapping 或 D2-R5 logs。

## 3. Confirmed package-closure root cause

`collector/app/services/station_event_adapter.py` 直接导入：

```python
from common.station_event import ...
```

该依赖由 commit `b43a12f7d85d6acb3278a6208cac1c9b1d4d175a` 引入。原边界为 `collector` 子目录，而原 Dockerfile 只 materialize `app`：

```text
docker-compose.yml: build: ./collector
collector/Dockerfile:
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
```

`./collector` build context 无法访问 repository-root `common/`，所以 image 内无法导入 `common.station_event`。repository-root tests 未能暴露该 defect，因为本地 Python import path 包含 repository root/collector path 组合。

## 4. Remote Phase-1 mapping independent incompatibility

本节仅作 source-level、read-only contract classification；未访问远端。

```text
Known Phase-1 identity:
bytes: 5935
SHA-256: 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3

REMOTE_PHASE1_MAPPING_COMPATIBILITY:
INCOMPATIBLE_WITH_CURRENT_RUNTIME_MAPPING_CONTRACT
```

依据是该已知 remote identity 与 Phase-1 mapping 精确匹配，且该文件缺少当前 parser 强制要求的顶层字段：`schema_version`、`config_version`、`authoritative_source`、`hash_algorithm`、`plc_identity_namespace`、`decoder_registry`、`runtime_defaults`。

这不声明 remote config caused the D2-R5 restart loop；D2-R5 首个已证实错误仍是 image import-closure failure。

## 5. Git recovery and hard gate

执行了用户指定的 local Git hard gate：

```text
HEAD:        9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
origin/main: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind: 0 / 0
cached: empty
protected source (collector common config api frontend docker-compose.yml): PASS
```

目标报告执行前状态：`ABSENT / NON-SYMLINK / UNSTAGED`。

既有 tracked dirty artifacts 保持原样：

```text
.gitignore
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
```

既有 untracked docs/frontend artifacts 也未清理、未 stage、未覆盖。

## 6. Exact modified / created paths

本 authority 允许且实际涉及的 repository paths：

```text
modified:
collector/Dockerfile
docker-compose.yml

created:
tests/test_collector_container_packaging.py
docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
```

未修改 `collector/app/**`、`common/**`、`config/**`、`api/**`、`frontend/**`、`db/**`、existing tests 或 existing reports。

## 7. Red regression gate

新增测试真实读取 `docker-compose.yml` 与 `collector/Dockerfile`，并使用结构化 Compose `services.collector.build` equality 以及 non-comment Dockerfile line set membership；没有使用整个 Compose 文件 substring-only 检查。

用户指定的 literal command 首次因当前 shell 没有 `python` executable 而 exit 127：

```text
zsh:1: command not found: python
```

使用已有项目 `.venv` 环境执行同一测试 gate 一次，结果为预期 red：

```bash
.venv/bin/python -m pytest \
  tests/test_collector_container_packaging.py \
  -q
```

```text
exit: 1
2 failed
```

失败准确暴露：`collector_build == './collector'`，以及 Dockerfile 缺少 `COPY collector/requirements.txt ./requirements.txt`、`COPY collector/app ./app`、`COPY common ./common` 中的 required closure lines。

## 8. Dockerfile before / after

Before：

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app

CMD ["python", "-m", "app.main"]
```

After：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY collector/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY collector/app ./app
COPY common ./common

CMD ["python", "-m", "app.main"]
```

未复制整个 repository，未复制 `common` 到 `app`，未引入 editable install、packaging framework、dependency version、shell entrypoint 或 startup wait logic。

## 9. Compose build before / after

Before：

```yaml
collector:
  build: ./collector
```

After：

```yaml
collector:
  build:
    context: .
    dockerfile: collector/Dockerfile
```

Collector 的 service name、container name、environment、volumes、dependencies 和 restart policy 未变更。

## 10. Green regression result

```bash
.venv/bin/python -m pytest \
  tests/test_collector_container_packaging.py \
  -q
```

```text
exit: 0
2 passed in 0.01s
```

## 11. Focused test result

按 authority 限制执行一次：

```bash
.venv/bin/python -m pytest \
  tests/test_station_event_model.py \
  tests/test_collector_station_event_adapter.py \
  tests/test_collector_station_event_runtime_source.py \
  tests/test_line_config.py \
  -q
```

```text
exit: 2
2 errors during collection
ModuleNotFoundError: No module named 'app'
```

该 failure 是现有测试运行环境的 import-path 问题：`pytest.ini` 未配置 `pythonpath`，而既有项目认可的 collector test invocation 使用 `PYTHONPATH=collector:.`。本 authority 不修改测试、pytest 配置或 Python source，也不重试该 exactly-once focused suite。该 gate 因此为 `FAIL / ENVIRONMENT IMPORT-PATH BLOCKER`。

## 12. Non-DB broader suite result

按 authority 限制执行一次：

```bash
.venv/bin/python -m pytest \
  -m "not db_backed and not postgres_local" \
  -q
```

```text
exit: 2
7 deselected, 16 errors during collection
primary error: ModuleNotFoundError: No module named 'app'
```

未连接 PostgreSQL 或任何远端服务。该 gate 同样受现有 import-path 环境阻断。

## 13. Compose render result

执行一次用户指定的 `docker compose -f docker-compose.yml config`，exit 0。Collector rendered build 为：

```text
context: /Users/chenjie/Documents/MES/edge-mes-demo
dockerfile: collector/Dockerfile
```

rendered Collector 仍保留原 container name、environment、config read-only volume、dependencies 和 restart policy。未执行 `up`、`build`、`pull`、`create` 或 `run` 的 Compose lifecycle command。

## 14. Local image build identity

唯一允许的 build command 已执行一次：

```bash
docker build \
  --pull=false \
  --file collector/Dockerfile \
  --tag edge-mes-demo-collector:d2-r7a-package-validation \
  .
```

结果：

```text
exit: 1
failed to connect to the docker API at unix:///var/run/docker.sock
check if the path is correct and if the daemon is running:
dial unix /var/run/docker.sock: connect: no such file or directory
```

因此 image ID、OS、Architecture、Variant、Size 均为 `NOT AVAILABLE`；Docker daemon 不可用导致 image 未创建，不能声称 image build PASS。

## 15. Isolated import-closure terminal

未执行。由于唯一 image build 以 exit 1 结束且没有 validation image，执行指定 `docker run` 不可能产生有效 import evidence；本次不以失败的不存在 image 命令冒充 validation。结果：`NOT REACHED / BLOCKED_BY_LOCAL_DOCKER_DAEMON`。

目标 terminal（未执行）本应为 `IMPORT_CLOSURE=PASS`；本报告不声明 `common.station_event` container import PASS，也不声明 `ModuleNotFoundError` 已在 image 内消失。

## 16. HEAD mapping static terminal

未执行，原因与上一节相同：没有可用的本地 validation image。结果：`NOT REACHED / BLOCKED_BY_LOCAL_DOCKER_DAEMON`。

因此本报告不声明 HEAD mapping static validation PASS，不声明远端 config 已修复，也不声明 remote config 与 current runtime mapping contract 的运行时兼容性。

## 17. Temporary image cleanup

未执行 `docker image rm`：唯一 build 未创建 `edge-mes-demo-collector:d2-r7a-package-validation` tag，且 Docker API 不可用。没有执行 image ID 删除、prune 或 broad cleanup；没有留下由本任务确认创建的临时 tag。

## 18. Prohibited-action audit and invocation counts

```text
SSH: 0
remote host access: 0
remote mutation/file copy/config deployment: 0
Collector activation: 0
Compose lifecycle: 0
DB query/write: 0
API request: 0
V-PLC/PLC request: 0
data generation: 0
Python source/common/config/dependency-version changes: 0
Dashboard/browser/OEE/Quality/Pareto/Trace/D3: 0
Git stage/commit/push/tag/clean: 0

packaging regression red gate: 1 effective .venv invocation
packaging regression green gate: 1
focused test suite: 1
non-DB broader suite: 1
docker compose config: 1
docker build: 1
import-closure docker run: 0, blocked before image existed
HEAD-mapping docker run: 0, blocked before image existed
temporary image-tag removal: 0, no tag was created
remote mutation: 0
```

## 19. Blockers / recommendations

本次实现与静态 packaging regression gate 已完成，但最终 authority verdict 不能为 PASS：

1. focused 与 broader pytest gates 在 collection 阶段被现有 `app.*` import-path 环境阻断；本 authority 不扩大 allowlist 去修改 `pytest.ini`、tests 或 Python source。
2. local Docker daemon 不可用，唯一 build exit 1，因此没有 image identity，也没有 container import/mapping evidence。
3. 不应把 Dockerfile/Compose 静态改动推断成 image build、Collector runtime、remote deployment 或 restart-loop 修复。

建议在新的独立 local validation authority 中提供可用 Docker daemon，并按项目认可的 `PYTHONPATH=collector:. .venv/bin/python` 环境验证 focused/broader tests；随后重新执行本任务要求的 image/container gates。不要在本 authority 下 SSH、部署 config、激活 Collector 或进入 D3。

## 20. Next gate

```text
Current verdict:
HOLD / IMPLEMENTATION_TEST_FAILED
and
HOLD / LOCAL_CONTAINER_PACKAGE_VALIDATION_FAILED

D2-R7B:
NOT ELIGIBLE from this HOLD.
```

在取得新 authority 下的完整 PASS 后，下一 eligible gate 才是：

```text
D2-R7B — deploy the exact HEAD config/mapping.yaml to the
remote read-only config mount source and verify its identity.

D2-R7B must not activate the Collector.
```

## 21. MVP alignment

```text
MVP claim:
repair only the Collector image package closure and add a
container regression gate

product capability/data generation: none
remote deployment/activation: none
DB/API/V-PLC/Dashboard/D3: none
scope drift: none
```

本次 source changes 与 MVP infrastructure invariant 对齐，但由于 local test/Docker validation gates 未完整取得 PASS，不能发布 `PASS WITH RECOMMENDATIONS`。

## 22. Final Git audit

报告创建后执行：

```bash
git status -sb
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git diff --name-only
git diff --cached --name-only
```

最终必须保持：

```text
HEAD == origin/main == 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind: 0 / 0
cached: empty
staged/committed/pushed: no
```

Task-created or modified paths only：

```text
collector/Dockerfile
docker-compose.yml
tests/test_collector_container_packaging.py
docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
```

既有 `.gitignore`、`docs/current_status.md`、`docs/roadmap.md`、`docs/thread_handoff/pm_operating_rules.md` 以及既有 untracked artifacts 保持原样。所有本任务实现与报告保持 unstaged、uncommitted、unpushed。
