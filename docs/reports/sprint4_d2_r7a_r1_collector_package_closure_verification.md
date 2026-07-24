# D2-R7A-R1 Collector Package-closure Independent Verification

## Task

```text
D2-R7A-R1 — Independently Verify the Existing Collector Package-closure Repair
```

验证目标：

```text
source package closure
+ container import closure
+ static startup compatibility
+ regression gate
```

本报告是 validation-only 结果，不重新实现 D2-R7A，也不授权 repair、deployment 或 activation。

## Thread

```text
Verification
```

任务类型：`Level 2 Gate Verification`

## Authority

本次 authority 来自用户指定的 D2-R7A-R1 独立验证范围，以及：

```text
docs/thread_handoff/pm_operating_rules.md
docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
```

本次无 SSH、remote Docker、remote mapping deployment、Collector activation、Compose lifecycle、DB/API/V-PLC/PLC 操作。发现 blocker 仅记录并输出 `HOLD`。

## Environment

项目根目录：

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

测试与本地验证环境：

```text
Python: .venv/bin/python
PYTHONPATH: collector:.
Docker: local Docker daemon only
```

本轮 live Git truth：

```text
HEAD:        58e6c7e042436f31e1512c64e3ab40a08d14bf27
origin/main: 58e6c7e042436f31e1512c64e3ab40a08d14bf27
ahead/behind: 0/0
cached:      empty
```

本轮开始前验证报告目标文件为 `ABSENT / NON-SYMLINK`；mapping 文件相对当前 HEAD 未修改：`CONFIG_HEAD_MATCH=PASS`。

## Commands Executed

所有 pytest 与本地 validation Python command 均显式使用 `PYTHONPATH=collector:. .venv/bin/python`。

### Required reads

按用户指定顺序读取：

```text
docs/thread_handoff/pm_operating_rules.md
docs/reports/sprint4_d2_r7a_collector_image_package_closure_repair.md
collector/Dockerfile
docker-compose.yml
tests/test_collector_container_packaging.py
config/mapping.yaml
```

### Regression and tests

1. Packaging regression：

```bash
env PYTHONPATH=collector:. .venv/bin/python -m pytest \
  tests/test_collector_container_packaging.py -q
```

结果：exit `0`，`2 passed`。

2. Collector / station-event focused suite：

```bash
env PYTHONPATH=collector:. .venv/bin/python -m pytest \
  tests/test_station_event_model.py \
  tests/test_collector_station_event_adapter.py \
  tests/test_collector_station_event_runtime_source.py \
  tests/test_line_config.py -q
```

结果：exit `0`，`303 passed`，`0 failed`，`0 skipped`。

3. Required broader non-DB pytest：

```bash
env PYTHONPATH=collector:. .venv/bin/python -m pytest \
  -m "not db_backed and not postgres_local" -q
```

结果：exit `2`，collection 阶段 `9 errors`，`7 deselected`，未执行通过/失败测试，`0 skipped`。错误包括 repository 内多个 `app` package 在该强制 Python path 下的导入冲突，例如 `cannot import name 'app' from 'app.main'`、`No module named 'app.control_api'` 以及 `test_reliability` 的 imported module file mismatch。

4. Collector-only broader non-DB 范围：

```bash
env PYTHONPATH=collector:. .venv/bin/python -m pytest \
  collector/tests -m "not db_backed and not postgres_local" -q
```

结果：exit `1`，`78 passed`，`3 failed`，`7 deselected`，`3 subtests passed`，`0 skipped`。失败为：

```text
collector/tests/test_event_collector_reliability.py::EventCollectorReliabilityTest::test_ack_write_failure_is_marked_then_retried_on_same_payload
collector/tests/test_event_collector_reliability.py::EventCollectorReliabilityTest::test_existing_read_done_repairs_database_ack_status_without_second_write
collector/tests/test_snap7_reliability_integration.py::Snap7ReliabilityIntegrationTest::test_collector_reads_db104_persists_cycle_then_writes_ack
```

本 Thread 未修复这些失败，也未修改测试、pytest 配置或 Python source。

### Docker Compose render

```bash
docker compose config
```

结果：exit `0`。Collector rendered build 为：

```text
context: /Users/chenjie/Documents/MES/edge-mes-demo
dockerfile: collector/Dockerfile
```

仅执行 config render；未执行 `up`、`down`、`start`、`stop`、`create` 或其他 Compose lifecycle command。

### Local validation image build

本轮唯一一次 local validation image build：

```bash
docker build --pull=false \
  --file collector/Dockerfile \
  --tag edge-mes-demo-collector:d2-r7a-r1-validation-20260724 .
```

结果：exit `0`，镜像构建并打上临时 tag。image identity：

```text
tag:          edge-mes-demo-collector:d2-r7a-r1-validation-20260724
ID:           sha256:c1657b4ab54b5703ac42e28ac8c894104e18418d65bf0bfab5215a2f014c14b3
OS:           linux
Architecture: arm64
Size:         54425004 bytes
```

Docker inspect 的空 `Variant` 字段模板曾产生一次非 gate 的 template error，随后使用有效字段重新取得上述 identity；不影响 image build 或 container validation 结果。

### Container import closure and static mapping initialization

```bash
docker run --rm --network none --read-only \
  --volume /Users/chenjie/Documents/MES/edge-mes-demo/config:/app/config:ro \
  edge-mes-demo-collector:d2-r7a-r1-validation-20260724 \
  python -c 'import app.main as collector_main; import app.services.event_collector as event_collector; import common.station_event as station_event; from app.plc import build_read_plans, load_edge_mapping; from app.services.resolved_config_registry import build_resolved_config_snapshot_from_mapping; mapping = load_edge_mapping("/app/config/mapping.yaml"); plans = build_read_plans(mapping); snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot); assert mapping.runtime_snapshot is not None; assert snapshot.config_hash == mapping.runtime_snapshot.config_hash; assert plans; print("IMPORT_CLOSURE=PASS"); print(f"COMMON_STATION_EVENT={station_event.__name__}"); print(f"APP_MAIN={collector_main.__name__}"); print(f"EVENT_COLLECTOR={event_collector.__name__}"); print(f"MAPPING_STATIC_INITIALIZATION=PASS line_id={mapping.line_id} plans={len(plans)} config_hash={snapshot.config_hash}")'
```

结果：exit `0`，输出：

```text
IMPORT_CLOSURE=PASS
COMMON_STATION_EVENT=common.station_event
APP_MAIN=app.main
EVENT_COLLECTOR=app.services.event_collector
MAPPING_STATIC_INITIALIZATION=PASS line_id=LINE_001 plans=4 config_hash=0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
```

该命令只导入 runtime modules、解析 mapping 并建立 read plans/resolved snapshot；未调用 `app.main.main()`，未连接 DB，未启动 PLC/Collector。

host local validation 也通过：

```bash
env PYTHONPATH=collector:. .venv/bin/python -c 'import app.main as collector_main; import app.services.event_collector as event_collector; import common.station_event as station_event; from app.plc import build_read_plans, load_edge_mapping; from app.services.resolved_config_registry import build_resolved_config_snapshot_from_mapping; mapping = load_edge_mapping("config/mapping.yaml"); plans = build_read_plans(mapping); snapshot = build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot); assert mapping.runtime_snapshot is not None; assert snapshot.config_hash == mapping.runtime_snapshot.config_hash; assert plans; print("LOCAL_IMPORT_CLOSURE=PASS"); print(f"LOCAL_MAPPING_STATIC_INITIALIZATION=PASS line_id={mapping.line_id} plans={len(plans)} config_hash={snapshot.config_hash}")'
```

结果：exit `0`，`LOCAL_IMPORT_CLOSURE=PASS`，`LOCAL_MAPPING_STATIC_INITIALIZATION=PASS`，`LINE_001`，`4 plans`，hash 与 container validation 一致。

### Validation cleanup

```bash
docker image rm edge-mes-demo-collector:d2-r7a-r1-validation-20260724
```

结果：exit `0`，临时 tag 与本轮创建的 image layers 已删除。

随后确认：

```text
VALIDATION_TAG=ABSENT
```

## Evidence

- `tests/test_collector_container_packaging.py` 真实读取 Compose 与 Dockerfile；其两项断言验证 Collector build context 与 runtime COPY closure。
- Dockerfile source closure 包含 `collector/requirements.txt`、`collector/app` 与 repository-root `common` 的 materialization；root build context 由 Compose render 证明。
- image build 成功，随后 container 内实际导入 `common.station_event`、`app.main` 与 `app.services.event_collector` 成功，未出现 `ModuleNotFoundError: common`。
- current HEAD 对应的 `config/mapping.yaml` 未被修改；host 与 container 两个静态 mapping initialization 均成功。
- package-specific focused tests 通过，但 broader regression gates 未完整通过，故不能发布完整 Level-2 Verification PASS。

## Regression Result

```text
Packaging regression: PASS — 2 passed, 0 failed, 0 skipped
Focused Collector/station-event: PASS — 303 passed, 0 failed, 0 skipped
Repository broader non-DB: HOLD — 9 collection errors, 7 deselected
Collector-only broader non-DB: HOLD — 78 passed, 3 failed, 7 deselected, 0 skipped
```

## Container Validation Result

```text
Local image build: PASS
Compose collector build definition: PASS
Container command execution: PASS
Docker service startup/activation: NOT EXECUTED BY AUTHORITY
```

## Import Closure Result

```text
common.station_event: PASS
collector/app runtime import chain: PASS
ModuleNotFoundError: common: NOT OBSERVED IN VALIDATION IMAGE
```

## Mapping Static Initialization Result

```text
Current HEAD config identity: PASS — config/mapping.yaml unchanged relative to HEAD
Host local static initialization: PASS
Container static initialization: PASS
line_id: LINE_001
read plans: 4
resolved config hash: 0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
DB/API/remote mapping validation: NOT EXECUTED
```

## Allowlist Audit

本 Thread 只新增用户允许的报告文件；未修改实现或测试：

```text
allowed created path:
docs/reports/sprint4_d2_r7a_r1_collector_package_closure_verification.md

thread-created/modified files:
docs/reports/sprint4_d2_r7a_r1_collector_package_closure_verification.md
```

以下 dirty paths 在本 Thread 开始前已存在，作为被验证的 D2-R7A repair 或外部 dirty artifacts 保留，未由本 Thread 修改、stage、覆盖或清理：

```text
.gitignore
collector/Dockerfile
docker-compose.yml
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
tests/test_collector_container_packaging.py
```

其他既有 untracked docs/frontend artifacts 也未触碰。`config/mapping.yaml`、`collector/app/**`、`common/**`、`pytest.ini` 未由本 Thread 修改。

Forbidden-action audit：

```text
SSH / remote Docker / remote mapping deployment: 0
Collector activation / Compose lifecycle mutation: 0
DB query/write / API request: 0
V-PLC / PLC request / production data generation: 0
implementation/test/config/source modification: 0
Git stage / commit / push / tag / clean: 0
temporary validation tag after cleanup: absent
```

## Modified Files

本 Thread 实际新增：

```text
docs/reports/sprint4_d2_r7a_r1_collector_package_closure_verification.md
```

没有修改 `collector/Dockerfile`、`docker-compose.yml`、`tests/test_collector_container_packaging.py`、`collector/app/**`、`common/**`、`config/**` 或 `pytest.ini`。

## Blockers

1. Required repository broader non-DB pytest 未能完成 collection：`9 errors`，主要由 `PYTHONPATH=collector:.` 下多个 repository `app` package 冲突造成。
2. Collector-only broader non-DB suite 有 3 个失败测试，涉及 event collector reliability 与 Snap7 reliability integration。按本 authority 禁止修复，不能将该 regression gate 记为 PASS。

## Recommendations

- 由新的、明确授权的独立任务处理 broader pytest 的 package/import collection boundary 与上述 3 个 reliability test failures；本 Thread 不进入 repair。
- 重新取得完整 broader regression PASS 后，再由 PM 决定是否开启后续 gate；本 HOLD 不授权 D2-R7B、D3、deployment 或 activation。

## Conclusion

```text
HOLD
```

package-specific source closure、container import closure、Compose render、local image build 与 current mapping static initialization 已取得本轮证据；但 required broader regression gates 存在 collection errors 与 3 个 test failures，因此 D2-R7A-R1 的完整独立验证不能 PASS。

## Next Gate

```text
Not eligible for D2-R7B or D3 from this HOLD.
```

下一步只能由 PM 另行授权最小范围的 regression failure/import-boundary repair 或新的 independent re-verification；本 Thread 不自行进入 repair。

## MVP 路径一致性

```text
classification: MVP-ALIGNED WITH BACKLOG ITEMS
approved MVP claim: Collector image package closure and its container/static startup validation
minimum invariant: runtime imports must be materialized in the image and current mapping must parse without remote/runtime mutation
new product capability: none
new deployment/runtime topology: none
scope drift: none
```

本轮 package-closure evidence 直接服务于已批准 MVP；broader regression failures 是当前 gate blocker，但没有借此扩大到 DB/API、remote deployment、PLC/V-PLC、Dashboard 或 D3。

## Thread Output / Context Assessment

```text
本次输出长度: 长
当前 Thread 是否建议继续: no
下一轮是否建议新开 Thread: yes
理由: 本轮已完成独立验证并产生 HOLD；后续 repair 或 re-verification 需要新的明确 authority 与独立 allowlist，不能在本 Thread 中顺势扩大职责。
```
