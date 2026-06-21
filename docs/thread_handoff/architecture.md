# Architecture / Integration Thread Handoff

更新时间：2026-06-21
Thread：Architecture / Integration
当前里程碑：Phase-2 Sprint 2 Generic Station Event Model contract revision
当前 Reliability Gate：**PASS WITH RECOMMENDATIONS**
当前活动：N8 定向复验已 CLOSED；准备 Data Quality review 与 Verification Gate matrix
（implementation 尚未开始）

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
| Sprint 2 planning freeze commit | `45fa2a8 Freeze Sprint 2 station event planning` |
| HEAD | `45fa2a8` |
| `origin/main` | `45fa2a8` |
| Phase-2 tag | 未创建 |
| 远程部署 | 未执行 |
| rollback drill | 未执行 |
| Sprint 2 Reliability focused re-review | `PASS WITH RECOMMENDATIONS` |
| Sprint 2 | N6/N7/N8 与既有 findings 均 CLOSED；无新 Reliability blocker；implementation 未开始 |
| 工作树 | 有未提交文档修改；最新已 push commit 仍为 `45fa2a8` |

Sprint 1 已完成 final commit / push，Sprint 2 planning freeze 也已在 `45fa2a8`
提交。Reliability N8 定向复验结论为 `PASS WITH RECOMMENDATIONS`；N8 已 CLOSED，
N6、N7 和既有 CLOSED items 均无回归，未发现新 Reliability blocker。Sprint 2
implementation 仍未开始。

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

## 5. Sprint 2 planning 与 N8 定向复验

本轮新增：

- `docs/contracts/station_event_model.md`
- `docs/reports/sprint2_generic_station_event_model_plan.md`

Reliability 历史：

- 文件：`docs/reports/sprint2_station_event_reliability_review.md`
- 首轮：`HOLD / CHANGES REQUIRED`，六个 blocker。
- 第四轮 re-review：`HOLD / CHANGES REQUIRED`。
- N8 定向复验：`PASS WITH RECOMMENDATIONS`。
- CLOSED：N6、N7、N8、UNKNOWN diagnostic context、payload limits、event required
  fields。
- 新 Reliability blocker：无。

本轮 Architecture N8 最小返修：

1. `canonical_station_result` evidence 继续比较 cited result 自身 `result=nok`。
2. `validated_nok_detail` 自身保持 `result` forbidden/absent。
3. Detail evidence 的 `upstream_result=nok` 改为比较其 accepted canonical parent
   `station_result.result`。
4. 增加一个合法正例与三个负例：detail 自带 result、parent result=ok、technical
   failure impersonation。
5. Technical failure 仍不能支持 `30003/UPSTREAM_NOK_SKIPPED`。

未退化的 CLOSED 项：

- N6 cycle-role/content fingerprint 未修改。
- N7 stateful relation/detail-set 未修改。
- UNKNOWN 仍只允许 heartbeat + strict diagnostic context。
- payload/raw 仍保持 16/64 KiB、depth/key/array/string/type/encoding 和超限 reject。
- event required/optional/forbidden、absent/null 与 `profile_id` 规则保持不变。

已冻结的关键决定包括：

- 后续路径为 `common/station_event/`，本轮未创建。
- MVP 为 cycle start/complete、result、NOK、heartbeat。
- 保留独立 `station_nok` 与 `nok_origin`。
- frozen dataclass、UUIDv4 runtime 默认、UUIDv5 test-only、UUIDv7 future。
- 所有有效事件强制 `config_hash`。
- payload/raw payload 上限 16/64 KiB。

这些仍是 planning/contract 文档，不代表 Sprint 2 package、tests 或 runtime
integration 已交付。Reliability findings 已关闭，但 Data Quality、Verification 与
ChatGPT PM implementation authorization 尚未完成。

## 6. 当前后续 Gate

Reliability N8 定向复验已确认：

1. `validated_nok_detail` 合法正例可构造。
2. Detail 自身 result absent、canonical parent result=nok 的 comparison 唯一。
3. 三个负例均有唯一 reject 结果。
4. N6、N7 与既有 CLOSED items 无回归。

下一步可进入 Data Quality review，并由 Verification 建立合同 Gate matrix。两项 review
与 ChatGPT PM 授权完成前，implementation、tests、package、DB/API/Collector/V-PLC/
Dashboard 接入仍全部禁止。

## 7. 后续 Architecture Thread 阅读顺序

1. `docs/thread_handoff/architecture.md`
2. `docs/reports/architecture_context_restore.md`
3. `docs/reports/sprint2_station_event_reliability_review.md`
4. `docs/reports/sprint2_generic_station_event_model_plan.md`
5. `docs/contracts/station_event_model.md`
6. `docs/reports/sprint1_independent_gate_review.md`
7. `docs/reports/sprint1_contract_hardening_report.md`
8. `docs/contracts/line_configuration.md`
9. `docs/contracts/dynamic_station_model.md`
10. `docs/reports/phase2_sprint_plan.md`
11. `docs/reports/phase2_thread_task_plan.md`

## 8. 下一 Thread 接手动作

1. 重读上述 handoff、context、Reliability 报告、返修 plan 和 event contract。
2. 进入 Data Quality review，审计完整性、血缘和重复/迟到语义。
3. 由 Verification 建立合同 Gate matrix。
4. 审计结论汇总并由 ChatGPT PM 明确授权前，不得编写业务实现、tests 或创建
   `common/station_event/`。
5. Reliability recommendations 进入 Verification fixture 与 table-driven tests 设计，
   但不阻塞 N8 关闭。

## 9. 工作树与提交边界

本轮允许修改：

- `docs/contracts/station_event_model.md`
- `docs/reports/sprint2_generic_station_event_model_plan.md`
- `docs/thread_handoff/architecture.md`
- `docs/reports/architecture_context_restore.md`
- 必要时 `docs/DOC_INDEX.md`、`docs/reports/README.md`

Reliability 报告由 Reliability Thread 维护，本轮只读。

未来 docs commit / push 必须使用精确 allowlist，明确不要提交：

- `docs/20260620_03_Edge MES Demo — ChatGPT PM Handoff.md`
- `docs/Edge MES Demo 当前进度报告.md`
- `docs/superpowers/`

禁止使用 `git add .`。

## 10. 明确禁止事项

- 不把 Sprint 1 重新描述为 HOLD。
- 不重复执行 Sprint 1 Contract Hardening。
- 不把当前 planning freeze 误称为已完成实现。
- 不把 Reliability PASS 误写成 Sprint 2 implementation 已授权。
- 不跳过 Data Quality / Verification Gate 与 ChatGPT PM authorization。
- 不在未获 PM 授权时创建 station event package 或修改 tests。
- 不提前修改 migration、DB、Collector、API、Dashboard 或运行链路。
- 不创建 Phase-2 tag。
- 不远程部署或执行 rollback drill。
