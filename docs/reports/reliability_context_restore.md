# Thread01-Reliability Context Restore

更新时间：2026-06-19  
恢复范围：Phase-1 Reliability 最终状态  
业务代码修改：无  
Phase-1 最终验收：`PASS`

> 本文件已从早期“实施前上下文恢复报告”更新为最终 handoff 入口。2026-06-18 的
> 未实施、未部署和 `BLOCKED` 判断已经失效。后续 Thread 不应从旧状态重新设计或
> 重复实施 Reliability Sprint。

## 1. Phase-1 已完成内容

Phase-1 已完成以下闭环：

1. DB104 PLC runtime identity、稳定 `plc_boot_id`、heartbeat 和 restart counter。
2. strict ACK、ACK timeout payload 保持、持久化后 ACK 和 ACK 写回重试。
3. Collector 重启补 ACK、事件幂等、counter reset 检测和错误落库。
4. `normal / fast / test` Profile 与受控参数真源 `config/vplc.yaml`。
5. normal Profile Cycle Time guardrail，修复远程约 4–5 秒异常节拍。
6. 参数修改审计、参数快照、PostgreSQL 持久化和只读查询接口。
7. WS01/WS02/WS03 独立 NOK Rate、强制 NOK FIFO 队列、白名单和清除能力。
8. 本机 V-PLC、Collector、Snap7、mapping、compileall 和静态验证。
9. Raspberry Pi migration、定向服务重建、Profile、Cycle Time、NOK、Collector、
   PostgreSQL、API 和 Grafana 基础验收。
10. Phase-1 最终验收结论：`PASS`。

## 2. 本 Thread 负责的关键变更

### Runtime Identity 与 ACK

- DB104 取代 legacy DB100 作为新三工站链路的 runtime identity 来源。
- Collector 不再使用会话 UUID 兜底 PLC identity。
- 未 ACK payload 不会被下一件覆盖。
- ACK deadline 默认 10 秒，超时后 payload 保持可恢复。
- 数据库提交失败不写 ACK；ACK 写失败保留已提交事件并进入重试状态。

### Counter 与恢复

- 幂等键固定为：

  ```text
  plc_id + station_id + plc_boot_id + cycle_counter
  ```

- 同 boot 相同 counter 视为重复 payload，可幂等更新和补 ACK。
- counter 跳跃允许入库，缺口判定交给 Data Quality。
- 同 boot counter 下降记录 `PLC_COUNTER_RESET`，不落 cycle、不 ACK。
- boot ID 变化后 counter 可重新开始。

### Cycle Time 与参数治理

- station 参数从散落 runtime 值收敛到 `config/vplc.yaml`。
- normal Profile 固定 `scale=1.0`，base 受安全范围保护。
- fast/test 通过 scale 加速，不篡改 process baseline。
- 参数 API 要求 reason，并记录 actor、IP、request ID、old/new 和 accepted 状态。
- startup/runtime/reset/periodic snapshot 已接入数据库。

### NOK 模拟

- 单次 pending code 升级为每站 FIFO 队列。
- 支持 `count=1..100`、工站白名单、pending 状态和 clear。
- 随机 NOK 使用 station 独立 RNG。
- 上游 NOK 导致的下游 SKIPPED 不消费下游队列。
- NOK 数据沿 Payload、Collector、Trace 和 Dashboard 现有链路传播。

## 3. 当前稳定状态

### 本机验证

| 检查 | 最终结果 |
| --- | --- |
| V-PLC 全量测试 | PASS，27/27 |
| Collector 单元/集成测试 | PASS，12/12 |
| 真实 Snap7 Server/Client ACK | PASS |
| NOK 专项测试 | PASS，5/5 |
| mapping 校验 | PASS |
| Python compileall | PASS |
| `git diff --check` | PASS |

### Raspberry Pi

| 项目 | 当前状态 |
| --- | --- |
| 部署路径 | `/opt/edge-mes-demo` |
| Git 仓库 | 否 |
| Compose 服务 | 9 个服务运行 |
| PostgreSQL | `healthy` |
| migration 005/006 | 已执行，`COMMIT` |
| Profile | `normal` |
| cycle scale | `1.0` |
| strict ACK | `true` |
| 三站 Cycle Time | 约 29–32 秒 |
| Collector | 持续落库 |
| WS01/WS02/WS03 NOK | 已验证 |
| fast/test Profile | 已验证并恢复 normal |
| API/Grafana health | PASS |

远程部署未覆盖 `.env`、数据库 volume、Grafana volume 或 Prometheus 数据。

## 4. 已知限制

- `/opt/edge-mes-demo` 不是 Git 仓库，不能使用 `git pull` 更新。
- 远程版本追踪依赖发布包 SHA-256、部署报告和部署前备份。
- PostgreSQL 中仍有部署前约 4 秒历史事件和验收生成的 fast/test 数据。
- Dashboard 宽时间范围可能混合历史与当前 Profile，应按时间或 `plc_boot_id` 隔离。
- Grafana 暂无参数审计和 pending NOK 队列专用面板。
- Snap7 测试连接清理日志可能出现 `Expected COTP DT, got 0x80`，当前不影响测试结果。
- Phase-1 不包含：
  - Data Quality 的 `data_gap_event` 与 Ignore Edge 闭环。
  - 真实 PLC 接入。
  - 多产线。
  - Oracle 真实同步。
  - 完整认证授权体系。
  - 图片、视频、归档和 AI。
- SSH 密码、私钥、Token、`.env` 内容及其他敏感凭据不得写入仓库。

## 5. 下一阶段建议

### Data Quality

- 基于 DB104 `ignore_edge`、`plc_boot_id`、counter 和 `cycle_event` 实现 gap 生命周期。
- 不重新实现 ACK、identity 或 counter reset 逻辑。

### Verification

- 将当前自动化测试和远程验收步骤整理为可重复执行的回归套件。
- 重点验证新功能不会破坏 Phase-1 幂等键、strict ACK 和 Profile guardrail。

### Dashboard / Operations

- 增加 Profile、boot ID 或验收时间范围过滤。
- 仅在明确需要时增加参数审计和 pending NOK 运维面板。
- 为非 Git 部署建立版本号、checksum、备份和回滚登记。

### Phase-2

- 真实 PLC、Oracle 或多产线启动前，先新增或更新 `docs/contracts/`。
- 不得直接修改 Phase-1 已冻结的 DB104、ACK、幂等键和 counter 语义。

## 6. 新 Thread 如何恢复上下文

### 最小恢复路径

按顺序阅读：

1. `docs/thread_handoff/reliability.md`
2. `docs/reports/reliability_context_restore.md`
3. `docs/reports/reliability_sprint_report.md`
4. `docs/reports/remote_reliability_deploy_report.md`
5. `docs/reports/nok_simulation_improvement_report.md`
6. `docs/contracts/plc_identity_and_counter.md`
7. `docs/contracts/ack_protocol.md`
8. `docs/contracts/vplc_runtime_parameters.md`
9. `docs/protocol.md`
10. `docs/current_status.md`

### 本地检查

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo
git status --short
```

当前工作树包含 Phase-1 变更和新增文件。不要因文件未提交而判断功能未实现；先读取
上述最终报告并核对实际文件。

### 远程检查

远程实际路径：

```text
/opt/edge-mes-demo
```

只读恢复命令：

```bash
cd /opt/edge-mes-demo
docker compose ps
docker compose logs --tail=80 s7-plc-sim
docker compose logs --tail=80 collector
```

远程目录不是 Git 仓库，不执行 `git pull`。需要更新时遵循：

```text
本地确认变更
→ 远程关键文件备份
→ 定向文件同步
→ 只重建受影响服务
→ Compose、日志、数据库和功能验证
→ 更新部署报告
```

### 新 Thread 工作原则

- Phase-1 已最终验收 `PASS`，不要重新分析、重新设计或重复实施。
- 先定义新 Thread 的边界，再读取对应 contract。
- 公共协议、schema 或 API 发生变化时，必须遵守：

  ```text
  docs/contracts/ → code/config/migration → tests → docs/reports/
  ```

- Reliability 稳定接口可以直接消费；如发现回归，先提供当前运行证据再修改。

## 7. 权威证据

- `docs/thread_handoff/reliability.md`
- `docs/reports/reliability_sprint_report.md`
- `docs/reports/nok_simulation_improvement_report.md`
- `docs/reports/remote_reliability_deploy_report.md`
- `docs/reports/reliability_report.md`
- `docs/reports/cycle_time_rca.md`
- `docs/reports/cycle_time_fix_plan.md`
- `docs/deployment/raspberry_pi.md`
