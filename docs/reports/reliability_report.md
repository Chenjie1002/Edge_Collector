# Reliability Report

日期：2026-06-18  
范围：单机、单产线、单 PLC、三工站 Edge MES Demo

## 1. Scope

本次完成：

- DB104 稳定 PLC runtime identity。
- 严格 ACK、ACK deadline 和 `ack_timeout`。
- ACK 写回失败状态化与后续轮询重试。
- Collector 重启后的幂等补 ACK。
- 同 boot counter reset 检测与阻断。
- `collector_error_log` 和 runtime error status 写入链路。
- reliability schema migration。
- V-PLC、Collector 单元测试和真实 Snap7 集成测试。

未实现真实 Oracle、Dashboard 改造或无关业务功能。

## 2. Commit / Working Tree State

- 当前分支未创建新 commit。
- 开始工作前仓库已有未提交文档修改和新增文档目录；本次保留这些用户改动。
- 本报告只声明本次可靠性范围内的代码、配置、测试、migration 和文档更新。

## 3. Files Changed

核心实现：

- `s7_plc_sim/app/plc_db.py`
- `s7_plc_sim/app/pipeline.py`
- `s7_plc_sim/app/main.py`
- `collector/app/services/reliability.py`
- `collector/app/services/event_collector.py`
- `collector/app/services/storage.py`
- `config/mapping.yaml`
- `docker-compose.yml`

Schema：

- `db/init/003_event_schema.sql`
- `db/migrations/005_reliability_schema.sql`

测试与校验：

- `s7_plc_sim/tests/test_reliability.py`
- `s7_plc_sim/tests/test_pipeline_uid_flow.py`
- `collector/tests/test_reliability.py`
- `collector/tests/test_event_collector_reliability.py`
- `collector/tests/test_snap7_reliability_integration.py`
- `scripts/validate_edge_mapping.py`

文档：

- `docs/protocol.md`
- `docs/current_status.md`
- `docs/thread_handoff/reliability.md`
- `docs/reports/reliability_report.md`

## 4. Commands Executed

```bash
python3 -m venv .venv
.venv/bin/pip install -r collector/requirements.txt -r s7_plc_sim/requirements.txt
PYTHONPATH=s7_plc_sim .venv/bin/python -m unittest discover -s s7_plc_sim/tests -v
PYTHONPATH=collector .venv/bin/python -m unittest discover -s collector/tests -v
PYTHONPATH=collector .venv/bin/python scripts/validate_edge_mapping.py config/mapping.yaml
.venv/bin/python -m compileall -q collector s7_plc_sim scripts
git diff --check
docker --version
psql --version
pg_isready
```

## 5. Evidence and Results

| 检查 | 状态 | 证据 |
| --- | --- | --- |
| V-PLC unit tests | PASS | 8 tests，0 failures |
| Collector unit/integration tests | PASS | 12 tests，0 failures |
| Real Snap7 boundary | PASS | 本地 Snap7 Server/Client 完成 DB104 read、cycle persist 调用和 DB101 `read_done` write |
| Mapping validation | PASS | line plan 为 DB104，read size 53，5 个 runtime 字段；WS01/02/03 plan 正常 |
| Python compileall | PASS | `compileall-ok` |
| Diff whitespace check | PASS | `git diff --check` exit 0 |
| PostgreSQL migration execution | BLOCKED | 本机没有 Docker、`psql`、`pg_isready` |
| Docker Compose restart/fault test | BLOCKED | 本机没有 Docker CLI |

真实 Snap7 测试结束断开连接时，python-snap7 server 输出一条
`Expected COTP DT, got 0x80` 清理期日志，但测试 exit 0，ACK 读回与断言均通过。

## 6. Contract Checks

| Contract | 状态 | 实现 |
| --- | --- | --- |
| DB104 `plc_boot_id` 非空且运行期间稳定 | PASS | UUID 在 runtime identity 对象中生成，DB104 每轮写入 |
| V-PLC 新启动产生新 boot ID | PASS | `load_or_start` 每次启动生成 UUID，restart counter 持久化递增 |
| Collector 不使用自身 UUID 兜底 | PASS | DB104 无效时记录 `PLC_IDENTITY_INVALID`，不读取 station payload、不 ACK |
| 未 ACK payload 不覆盖 | PASS | station 在 `payload_ready` 清除前不能启动下一件 |
| ACK timeout 不释放 payload | PASS | deadline 后仅置 `ack_timeout=TRUE` |
| 数据提交后才能 ACK | PASS | `persist_cycle` 返回后才执行 Snap7 write |
| ACK 写回失败可重试 | PASS | 标记 `ACK_WRITE_FAILED`、增加 `retry_count`；下轮幂等 persist 后重写 |
| Collector 重启补 ACK | PASS | 恢复只依赖 PLC payload 与数据库唯一键，不使用内存 session identity |
| 同一幂等键只有一个 cycle | PASS | 保留唯一键 `(plc_id, station_id, plc_boot_id, cycle_counter)` 和 upsert |
| 同 boot counter reset 阻断 | PASS | 小于数据库 max counter 时记录 `PLC_COUNTER_RESET`，不 persist、不 ACK |
| boot 变化允许 counter 重启 | PASS | counter max 查询按 boot ID 隔离 |
| 错误完整落库 | PASS（代码/单测） | connection、identity、read/decode、storage、ACK、counter reset 均有 error type |

## 7. Final Runtime Contract

DB104：

| 字段 | 地址 |
| --- | --- |
| `protocol_version` | `DB104.DBW0` |
| `heartbeat_counter` | `DB104.DBD4` |
| `plc_restart_counter` | `DB104.DBD8` |
| `plc_boot_id` | `DB104.DBB12 STRING[36]` |
| `ignore_edge` | `DB104.DBX52.3` |

ACK：

- deadline：默认 10 秒。
- 配置：`VPLC_ACK_DEADLINE_SECONDS`。
- 状态：`PENDING`、`ACK_OK`、`ACK_WRITE_FAILED`。
- error types：`PLC_CONNECTION_FAILED`、`PLC_IDENTITY_INVALID`、
  `PLC_READ_DECODE_FAILED`、`STORAGE_WRITE_FAILED`、`ACK_WRITE_FAILED`、
  `PLC_COUNTER_RESET`。

Counter：

- 相同 counter：重复 payload，幂等更新并补 ACK。
- counter 跳跃：正常入库，缺口统计交给 Data Quality。
- counter 下降：阻断并记录 reset。
- boot ID 变化：允许 counter 从 0 或 1 重新开始。

## 8. Known Issues

- PostgreSQL migration 尚未在本机或树莓派实际执行；部署前必须运行
  `db/migrations/005_reliability_schema.sql`。
- 未在本机执行 Docker Compose 级 Collector 进程重启、V-PLC 容器重启和数据库断开
  故障注入；原因是本机没有 Docker CLI。
- `raw_plc_sample` 允许在后续 cycle transaction 失败时独立保留，作为故障诊断证据；
  Collector 不会因此写 ACK。
- ACK 写回失败的真实故障注入目前由测试 fake client 覆盖，控制台尚无专用故障注入按钮。
- `ignore_edge` 地址已稳定在 DB104，但 `data_gap_event` 逻辑仍属于 Data Quality Thread。

## 9. Handoff

树莓派部署与验收：

```bash
cd /opt/edge-mes-demo
docker exec -i edge-mes-postgres \
  psql -U edge_mes -d edge_mes \
  < db/migrations/005_reliability_schema.sql
docker compose up -d --build s7-plc-sim collector
```

部署后由 Verification Thread 执行：

1. 查询 DB104 boot ID，确认同进程稳定、V-PLC 重启后变化。
2. 停止 Collector 超过 10 秒，确认 payload 保留且 `ack_timeout=TRUE`。
3. 启动 Collector，确认同一 cycle 只有一行且最终 `ACK_OK`。
4. 在 ACK 写回路径注入一次失败，确认 `ACK_WRITE_FAILED`、`retry_count` 增加并自动恢复。
5. 重启 Collector，确认当前 ready payload 被补 ACK。
6. 同 boot 强制 counter 下降，确认 `PLC_COUNTER_RESET` 且无 ACK。

## 10. Governance Rule Impact

2026-06-18 新增仓库级变更门禁：

```text
更新 docs/contracts/ → 修改代码、配置或 migration → 在 docs/reports/ 记录影响范围
```

适用范围：

- PLC/S7 协议、ACK、identity、counter 和 mapping 语义。
- PostgreSQL table、column、constraint、index 和 migration。
- Collector、API 或其他模块对外提供的公共接口。

本次 Reliability 交付符合该顺序：先存在并读取
`docs/contracts/ack_protocol.md` 与 `docs/contracts/plc_identity_and_counter.md`，
随后修改实现和 migration，最终由本报告记录影响范围及验证结果。
