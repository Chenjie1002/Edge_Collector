# Architecture / Integration Thread Handoff

更新时间：2026-06-20
Thread：Architecture / Integration
当前里程碑：Phase-2 Sprint 1 final closeout
当前 Gate：**PASS**
下一候选方向：Sprint 2 Generic Station Event Model planning（尚未启动）

## 1. 当前基线

| 项目 | 当前状态 |
| --- | --- |
| Phase-1 Acceptance | `PASS` |
| Phase-1 tag | `phase1-pass-20260619` |
| Phase-2 Architecture Planning | 已冻结并 push |
| Sprint 1 | Flexible Line Configuration |
| Sprint 1 Gate | `PASS` |
| Sprint 1 commit | `b9f6a69 Phase 2 Sprint 1 flexible line configuration` |
| HEAD | `b9f6a69` |
| `origin/main` | `b9f6a69` |
| Phase-2 tag | 未创建 |
| 远程部署 | 未执行 |
| rollback drill | 未执行 |
| Sprint 2 | 尚未启动 |

Sprint 1 已完成 final commit / push。当前不需要继续 Contract Hardening，也不需要远程
部署或 rollback drill。

## 2. Sprint 1 已交付

### 配置实现

- `common/line_config/`
  - strict allowed-key 与 enum validation
  - frozen configuration models
  - YAML loader
  - resolved config / canonical JSON / stable SHA-256
  - static load estimate
- `config/lines/demo_3_station.yaml`
- `config/lines/demo_10_station.yaml`
- `config/lines/stress_20_station.yaml`
- `tests/test_line_config.py`

### 合同与报告

- `docs/contracts/line_configuration.md`
- `docs/reports/sprint1_flexible_line_configuration_report.md`
- `docs/reports/sprint1_contract_hardening_report.md`
- `docs/reports/sprint1_independent_gate_review.md`
- `docs/thread_handoff/verification.md`
- `docs/reports/verification_context_restore.md`

### 最终验证

```text
focused tests: 20 passed, 57 deselected
configuration tests: 77 passed
root tests: 88 passed
API tests: 5 passed
Collector tests: 12 passed, 3 subtests passed
V-PLC tests: 27 passed
compileall: PASS
3/10/20 station YAML load/hash/estimate: PASS
git diff --check: PASS
```

## 3. 已关闭的主要问题

- strict unknown-field rejection。
- station、Buffer、Profile、mapping、payload、NOK、scenario、route 和 hardware enum。
- 20 stations / 4 mappings hard limits。
- Profile mode preservation 与 production/simulation timing 分离。
- config version、resolved config 和 stable config hash。
- seed、scenario、global NOK fallback 与 station override。
- 显式 `station.nok_rate: null` fallback。
- Buffer `enabled` / `tracking_mode`。
- mapping load fields、payload layout 和 static load estimate。
- NOK `30003` reserved semantics。
- RouteGraph、disabled station 与 Buffer endpoint 校验。

## 4. 运行链路隔离

Sprint 1 仍是独立配置基础，未接入：

- V-PLC runtime。
- Collector runtime。
- API。
- PostgreSQL schema / migration。
- Dashboard / Grafana。
- Docker / Compose。
- `.env` / volume。

Edge 仍只负责采集、存储、追溯、计算和展示，不主动决定 Hold、Rework 或 Skip。

## 5. 下一候选方向

下一候选方向是：

```text
Sprint 2: Generic Station Event Model
```

但 Sprint 2 尚未启动。进入 Sprint 2 前，应由 ChatGPT PM 单独确认 planning scope、
合同边界、文件 owner、migration/rollback gate 和 Verification 输入。

本 handoff 不授权实施 Sprint 2，不授权修改 DB、Collector、API 或远程环境。

## 6. 后续 Architecture Thread 阅读顺序

1. `docs/thread_handoff/architecture.md`
2. `docs/reports/architecture_context_restore.md`
3. `docs/reports/sprint1_independent_gate_review.md`
4. `docs/reports/sprint1_contract_hardening_report.md`
5. `docs/contracts/line_configuration.md`
6. `docs/reports/phase2_sprint_plan.md`
7. `docs/contracts/dynamic_station_model.md`
8. `docs/reports/phase2_thread_task_plan.md`

## 7. 明确禁止事项

- 不把 Sprint 1 重新描述为 HOLD。
- 不重复执行 Sprint 1 Contract Hardening。
- 不在未获 PM 授权时进入 Sprint 2 实施。
- 不提前修改 migration、DB、Collector、API、Dashboard 或运行链路。
- 不创建 Phase-2 tag。
- 不远程部署或执行 rollback drill。
