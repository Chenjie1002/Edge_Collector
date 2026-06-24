# Architecture / Integration Thread Handoff

更新时间：2026-06-23
Thread：Architecture / Integration
当前里程碑：Phase-2 Sprint 2 Generic Station Event Model implementation
当前 Reliability focused Gate：**PASS**
当前 Data Quality targeted Gate：**PASS WITH RECOMMENDATIONS；DQ-F1～DQ-F3 CLOSED**
当前 Verification targeted Gate：**PASS WITH RECOMMENDATIONS；V-DQ1～V-DQ4 PASS**
Remaining Reliability / Data Quality / Verification blocker：**none**
当前活动：Sprint 2 implementation、focused repair、Reliability focused review、Data
Quality targeted re-review 与 Verification targeted sanity check 均已完成，并已通过
commit `17cf5d2 Implement Sprint 2 generic station event model` push 到 `origin/main`。
Collector/API/DB/Dashboard/V-PLC runtime integration 未进入。

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
| HEAD | `17cf5d2 Implement Sprint 2 generic station event model` |
| `origin/main` | `17cf5d2 Implement Sprint 2 generic station event model` |
| Phase-2 tag | 未创建 |
| 远程部署 | 未执行 |
| rollback drill | 未执行 |
| Sprint 2 implementation baseline | `e9abe45` |
| Sprint 2 implementation commit | `17cf5d2 Implement Sprint 2 generic station event model` |
| Sprint 2 package | `common/station_event/` 已创建 |
| Sprint 2 focused tests | `128 passed` |
| Root `tests/` regression | `216 passed` |
| Sprint 2 Reliability focused review | `PASS`；remaining blocker none |
| Sprint 2 Data Quality targeted re-review | `PASS WITH RECOMMENDATIONS`；DQ-F1~DQ-F3 CLOSED |
| Sprint 2 Verification targeted sanity check | `PASS WITH RECOMMENDATIONS`；V-DQ1~V-DQ4 PASS |
| Sprint 2 Verification contract Gate | `PASS WITH RECOMMENDATIONS`；V6/V7/V10 已关闭 |
| Sprint 2 Verification implementation review | `PASS`；B1~B5 CLOSED |
| Sprint 2 | Generic Station Event Model MVP repair + tests 已完成；未集成 runtime |
| 工作树 | tracked diff clean；存在未跟踪 PM handoff doc，未纳入 Sprint 2 closeout |

Sprint 1 已完成 final commit / push。Sprint 2 planning / review gates 已在 `e9abe45`
完成 docs-only commit / push；Reliability、Data Quality、Verification 与 V10/R5 sanity
check 均为 `PASS WITH RECOMMENDATIONS`。PM 随后授权 implementation，本 working tree
已完成独立 package、tests 与 implementation report。Verification implementation review
发现 B1~B5 后，Verification 已完成 B5-final re-review并关闭 B1~B5。Reliability
focused review 已关闭 R-B2/R-B3/R-B4 与 B5 regression。DQ-F1～DQ-F3 repair、
Data Quality targeted re-review 与 Verification targeted sanity check 也已完成，
remaining blocker 为 none。Sprint 2 implementation 已通过 `17cf5d2` commit/push；
尚未进入 Collector/API/DB/Dashboard/V-PLC integration。

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

以下为 planning freeze 时冻结、现已由 implementation 实现的关键决定：

- implementation 路径为 `common/station_event/`，当前 working tree 已创建。
- MVP 为 cycle start/complete、result、NOK、heartbeat。
- 保留独立 `station_nok` 与 `nok_origin`。
- frozen dataclass、UUIDv4 runtime 默认、UUIDv5 test-only、UUIDv7 future。
- 所有有效事件强制 `config_hash`。
- payload/raw payload 上限 16/64 KiB。

这些 planning/contract 决定现已由独立 package 与 tests 实现；仍不代表 runtime
integration 已交付。当前 review blocker 已清零，但 commit/push 仍须 ChatGPT PM
精确 allowlist 授权。

## 6. 历史 Data Quality / Verification 合同修订

> 本节记录 implementation 前的合同修订历史。当前控制状态见文件顶部与第 13 节。

Reliability 结论保持：

1. `validated_nok_detail` 合法正例可构造。
2. Detail 自身 result absent、canonical parent result=nok 的 comparison 唯一。
3. 三个负例均有唯一 reject 结果。
4. N6、N7 与既有 CLOSED items 无回归。

当时 Data Quality R1~R5 focused re-review 已 `PASS WITH RECOMMENDATIONS`，随后
Verification 曾留下：

1. V6 payload/raw error-code mapping。
2. V7 same canonical content + different raw fingerprint final decision。
3. V10 mutually exclusive lifecycle / derived output。

Architecture 后续完成三个最小 docs-only 修订，V6/V7/V10 与 V10/R5 均已关闭；
本节不再代表当前待办。

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

1. 重读本 handoff、context 与三份 review report 的文件末尾当前控制结论。
2. 以 `17cf5d2` 作为 Sprint 2 implementation committed/pushed source of truth。
3. 若需要 closeout hygiene，只做 PM 授权的 docs-only 精确 allowlist。
4. 未获后续 PM 授权前不得 tag、deploy、rollback drill 或进入
   Collector/API/DB/Dashboard/V-PLC integration。

## 9. 工作树与提交边界

当前 docs-only closeout 只允许 PM 明确授权的状态同步；不得扩大修改代码、tests、
runtime、migration 或未授权文档。

未来 docs commit / push 必须使用精确 allowlist，明确不要提交未授权文件，例如：

- `docs/20260620_03_Edge MES Demo — ChatGPT PM Handoff.md`
- `docs/Edge MES Demo 当前进度报告.md`
- `docs/superpowers/`

禁止使用 `git add .`。

## 10. 明确禁止事项

- 不把 Sprint 1 重新描述为 HOLD。
- 不重复执行 Sprint 1 Contract Hardening。
- 不把历史 review 段落误读为当前控制状态。
- 不把 Sprint 2 implementation commit/push 误写成 runtime integration 已开始。
- 不把 review PASS 误写成已获得 tag/deploy/runtime integration 授权。
- 不提前修改 migration、DB、Collector、API、Dashboard 或运行链路。
- 不创建 Phase-2 tag。
- 不远程部署或执行 rollback drill。

## 11. Sprint 2 implementation 状态（更新至 2026-06-23 final targeted reviews）

PM 已在 `e9abe45` 后明确授权 Generic Station Event Model MVP implementation。本轮：

- 创建 `common/station_event/`。
- 新增 `tests/test_station_event_model.py`。
- 新增
  `docs/reports/sprint2_generic_station_event_model_implementation_report.md`。
- focused tests：`128 passed`。
- root `tests/` regression：`216 passed`。
- compileall 与 `git diff --check`：PASS。

本实现仍是独立离线 contract package。Collector、API、DB、Dashboard、Grafana、V-PLC、
migration、deploy、rollback drill 与 tag 均未进入本轮，Phase-1 默认行为未改变。
Sprint 2 implementation 已通过 `17cf5d2` commit/push；本实现仍未接入 runtime。

## 12. Verification implementation repair 状态

已修复：

- B1 historical snapshot station/profile lineage。
- B2 `30003` cross-station/cross-cycle parent isolation。
- B3 primary/secondary 与 secondary/secondary code duplication。
- B4 `validated_nok_detail` accepted canonical NOK parent validation。
- B5 base64/image/blob/file/log-like raw bypass：本轮补齐 WebP、PDF、generic binary
  base64、binary MIME、约 7 KiB 周期性单行片段，以及 binary/base64 超过 string
  limit 时的 `RAW_CONTENT_FORBIDDEN` precedence。

B1~B5 已由 Verification CLOSED。Reliability R-B3 CLOSED；R-B2/R-B4 已完成：

- `30003` skip parent 增加 same `config_hash` relation。
- `validated_nok_detail` canonical parent 增加 authoritative PLC/V-PLC、
  same-config、primary code/origin 与 secondary origin relation。

R-B2/R-B3/B5 已 CLOSED。R-B4 canonical parent 现在强制
`correlation.event_role=production_result`；其他 role、`None` 或缺失均
`UPSTREAM_EVIDENCE_INVALID` 且不投影。

Reliability R-B4 focused re-review 已 PASS；后续 Data Quality DQ-F1～DQ-F3 targeted
re-review 与 Verification targeted sanity check 也已
`PASS WITH RECOMMENDATIONS`。Sprint 2 implementation commit/push 已完成；ChatGPT PM
另行明确授权前不得开始 Collector/API/DB/Dashboard/V-PLC integration。

## 13. Data Quality repair 与最终 targeted Gate（2026-06-23）

Data Quality focused implementation review 曾返回 HOLD，finding 为：

- DQ-F1：parent snapshot lineage 缺 `profile_id`、`station_type`。
- DQ-F2：cited detail 未强制 `event_role=nok_detail` 与 ordinary canonical
  validation。
- DQ-F3：`raw_payload` 在 historical snapshot 无 decoder 时 fail-open。

Architecture 已完成最小 implementation repair：

- parent/detail exact relation 增加 `profile_id`、`station_type`。
- cited detail 必须为 accepted canonical `station_nok` / `nok_detail`，并继续 replay
  accepted canonical NOK parent。
- historical raw evidence 必须有 callable decoder；missing/exception 为
  `RAW_PARSE_ERROR`，raw-only 或 canonical mismatch 为
  `RAW_NORMALIZED_MISMATCH`。
- 所有 reject 均不产生 production outcome、defect detail、compatibility/Pareto
  projection 或 projection eligibility。
- duplicate/conflict/raw_variant 裁决未修改；raw_variant 合法 fixture 现在显式提供
  normalized payload 与 decoder。

当前最终状态：

```text
Reliability focused review: PASS
Data Quality targeted re-review: PASS WITH RECOMMENDATIONS
Verification DQ-F1～DQ-F3 targeted sanity check: PASS WITH RECOMMENDATIONS
Remaining Reliability blocker: no
Remaining Data Quality blocker: no
Remaining Verification blocker: no
focused station_event: 128 passed
broader tests: 216 passed
git diff --check: PASS
```

Sprint 2 implementation 已完成 commit/push；下一步只允许 docs-only closeout hygiene
或 Sprint 3 planning，且必须等待 PM 单独授权后才可进入 runtime integration。
