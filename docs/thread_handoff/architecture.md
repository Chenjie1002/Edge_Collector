# Architecture / Integration Thread Handoff

更新时间：2026-06-20
Thread：Architecture / Integration
当前里程碑：Phase-2 Sprint 2 Generic Station Event Model planning freeze
当前 Gate：**PASS**
当前活动：Sprint 2 planning + handoff（implementation 尚未开始）

## 1. 当前基线

| 项目 | 当前状态 |
| --- | --- |
| Phase-1 Acceptance | `PASS` |
| Phase-1 tag | `phase1-pass-20260619` |
| Phase-2 Architecture Planning | 已冻结并 push |
| Sprint 1 | Flexible Line Configuration |
| Sprint 1 Gate | `PASS` |
| Sprint 1 commit | `b9f6a69 Phase 2 Sprint 1 flexible line configuration` |
| Docs hygiene commit | `4215b7c Finalize Sprint 1 architecture handoff and review history` |
| HEAD | `4215b7c` |
| `origin/main` | `4215b7c` |
| Phase-2 tag | 未创建 |
| 远程部署 | 未执行 |
| rollback drill | 未执行 |
| Sprint 2 | PM decisions frozen；三方 review 待执行；implementation 未开始 |

Sprint 1 已完成 final commit / push，docs hygiene 也已完成。当前只在工作树中编写
Sprint 2 合同与 planning/handoff 文档；本轮不 commit、不 push。

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

## 5. Sprint 2 planning 产出

本轮新增：

- `docs/contracts/station_event_model.md`
- `docs/reports/sprint2_generic_station_event_model_plan.md`

合同已按 PM 决策冻结统一 event envelope、五类 MVP event type、
result/NOK/nok_origin/source authority、
config hash lineage、payload/raw payload、timestamp/order/idempotency、strict validation
和 canonical serialization。报告准备了 Reliability、Data Quality、Verification 与下一
Architecture Thread 的任务包和 Gate matrix。

已冻结的关键决定包括：

- 后续路径为 `common/station_event/`，本轮未创建。
- MVP 为 cycle start/complete、result、NOK、heartbeat。
- 保留独立 `station_nok` 与 `nok_origin`。
- frozen dataclass、UUIDv4 runtime 默认、UUIDv5 test-only、UUIDv7 future。
- 所有有效事件强制 `config_hash`。
- payload/raw payload 上限 16/64 KiB。

这些产出是 planning freeze，不代表 Sprint 2 package 或 runtime integration 已交付。

## 6. 后续 Architecture Thread 阅读顺序

1. `docs/thread_handoff/architecture.md`
2. `docs/reports/architecture_context_restore.md`
3. `docs/reports/sprint1_independent_gate_review.md`
4. `docs/reports/sprint1_contract_hardening_report.md`
5. `docs/contracts/line_configuration.md`
6. `docs/reports/sprint2_generic_station_event_model_plan.md`
7. `docs/contracts/station_event_model.md`
8. `docs/contracts/dynamic_station_model.md`
9. `docs/reports/phase2_sprint_plan.md`
10. `docs/reports/phase2_thread_task_plan.md`

## 7. 下一 Thread 推荐第一步

1. 重读上述 handoff、context、Sprint 2 plan 和 event contract。
2. PM 决策已关闭，不再重新打开 package、MVP enum、UUID、payload limit、
   `config_hash` 或 `nok_origin` 选择。
3. 按顺序先交 Reliability 风险审计，再交 Data Quality 语义/血缘审计，最后由
   Verification 建 Gate matrix。
4. ChatGPT PM 汇总三方结论并明确授权前，不得编写业务实现、tests 或创建
   `common/station_event/`。

## 8. 明确禁止事项

- 不把 Sprint 1 重新描述为 HOLD。
- 不重复执行 Sprint 1 Contract Hardening。
- 不把当前 planning freeze 误称为已完成实现。
- 不绕过 Reliability → Data Quality → Verification review 顺序。
- 不在未获 PM 授权时创建 station event package 或修改 tests。
- 不提前修改 migration、DB、Collector、API、Dashboard 或运行链路。
- 不创建 Phase-2 tag。
- 不远程部署或执行 rollback drill。
