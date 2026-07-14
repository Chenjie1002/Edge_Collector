# Sprint 3 Dashboard Raspberry Pi Docker Integration Data Quality Re-review

报告名称：Sprint 3 Dashboard Raspberry Pi Docker Integration Data Quality Re-review

任务名称：复验 DQ-DASH-D1/D2/D3 Architecture HOLD Repair

执行 Thread：Data Quality

日期：2026-07-14

## Conclusion

**HOLD**

本轮为 docs-only Data Quality planning re-review。DQ-DASH-D2 与
DQ-DASH-D3 的 Architecture planning blocker 已关闭；DQ-DASH-D1 的
22-field matrix、nullable/null、UTC、enum 和 safe-integer 规则已冻结，但
cycle_counter 的 fraction/no-rounding 规则在当前 JavaScript parsed-value
boundary 下仍存在 false-PASS 风险，因此不能宣称三个 blocker 全部关闭。

本结论不是要求当前支持超出 safe integer 的未来 BIGINT。整型 unsafe value
被 Number.isSafeInteger fail closed 属于当前合同；残留 blocker 是接近
Number.MAX_SAFE_INTEGER 的原始 JSON 小数可能在 JavaScript 数值解析前后
失去小数信息，随后以 safe integer 通过验证。当前 plan 未证明在不读取原始
JSON number lexeme 的情况下能够同时满足“拒绝 fraction”和“不允许舍入”。

现有 frontend 代码仍未修复；本 planning re-review 不授权 Gate A implementation、
Verification、Gate B、runtime 或 Git write。

## Created / changed files

- CREATE docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_rereview.md
- Existing files changed: none by this task。
- Architecture plan、原 Data Quality review、Reliability review/re-review、
  docs/current_status.md、frontend、API、DB、Collector、Docker/Compose、
  deployment guide、.gitignore 均未修改。

## Recovery baseline

    project: /Users/chenjie/Documents/MES/edge-mes-demo
    branch: main
    HEAD: bdda24fd930339b565d0c1894daece42c6039ac7
    origin/main: bdda24fd930339b565d0c1894daece42c6039ac7
    ahead/behind: 0 0
    latest: bdda24f Reset Dashboard URL validation scope
    cached diff: empty before this report creation
    target report before this write: absent

Recovery 同时确认既存 .gitignore tracked modification 与大量 external
untracked artifacts，包括历史 handoff/reports、frontend/node_modules/ 和
frontend/tsconfig.tsbuildinfo。本轮未修改、删除、整理、stage、commit 或
push 这些 artifacts。

本轮未运行 tests、typecheck、build、Docker、Compose、PostgreSQL、SSH、
Raspberry Pi、browser/server runtime、deployment 或 rollback。

## DQ-DASH-D1 status

**HOLD — residual blocker remains。**

已确认 Architecture plan Section 12.1 冻结 exact 22-field consumer contract：

- 13 个 non-null string 字段只允许 string，空字符串保留 raw string 语义；
- cycle_counter 只允许 JSON number 且必须 Number.isSafeInteger；
  numeric-looking string、fraction、NaN、Infinity、unsafe integer 均要求
  整个 malformed 2xx response fail closed，不得舍入、截断或模糊化；
- nullable string 与 nullable safe integer 只允许显式 JSON null，不允许
  错误类型或缺失 key；
- event_ts、accepted_at 必须为带 Z 的有效 UTC ISO string；
- event_type 与 non-null production_result 的 enum allowlist 已冻结，
  heartbeat/未知枚举 fail closed。

上述合同与 DB/API 22-key authority 内部一致。但 schema.ts 当前接收的
是 JavaScript parsed value，Gate A exact allowlist 又排除了 apiClient.ts。
仅依靠 typeof value === "number" 与 Number.isSafeInteger(value) 无法证明
原始 JSON 小数 lexeme 未在数值解析时被舍入成 safe integer；因此当前 plan
尚未满足“fraction + no rounding + fail closed + 不修改 API contract”这一
组合要求。

最小 Architecture docs-only repair：在 plan Section 12.1、17.1、18 中冻结
source-preserving numeric validation 的实现边界，并重新判断 Gate A 是否必须
纳入能在 JavaScript numeric coercion 前取得原始 response text/number lexeme
的最小 transport seam。若选择 API serialization 为 string，则必须另开独立
API serialization contract；本轮不修改该 contract，也不修改 plan。

## DQ-DASH-D2 status

**CLOSED。**

Plan Section 12.2–12.3 已冻结：

- station_result NOK、non-NOK、station_nok detail companion 与 cycle
  events 的完整 cross-field matrix；任何非法组合均使整个 malformed 2xx
  response fail closed，不跳过 bad row 或 partial render；
- typed raw API value、display value、display kind/rule 三层分离；raw
  null、empty string、invalid/missing 的语义不再共用 unknown；
- station_nok 显示为 Not applicable — NOK detail companion，cycle event
  显示为 Not applicable — cycle event；null 与 empty 可区分，placeholder
  不得被称为 production 原值；
- byResult 只统计 event_type=station_result，total accepted fact count
  仍为当前页全部 accepted rows；table、detail、trace 从同一个 raw item
  与同一个 fact_key 派生，target-first-item 不扩大为整页 closure。

该合同足以消除 null/empty 改写、outcome/detail 混淆和 cross-fact binding
风险；当前代码仍需未来 Gate A implementation 才会落实这些规则。

## DQ-DASH-D3 status

**CLOSED。**

Plan Section 12.4–12.5 已冻结独立 real DB-backed acceptance matrix：

- Case A：accepted station_result OK，mandatory；
- Case B：accepted station_result NOK，mandatory；
- Case C：accepted station_nok detail companion，仅在真实 Pi DB row 存在时
  执行；不存在时必须记录 NOT AVAILABLE / NOT VERIFIED；
- synthetic fixture、mock response、Case B、cycle event 均不得替代 Case C、
  Case A 或 Case B；
- 每个 case 只声明独立 bounded request 的 items[0] closure；每个 case
  保存全部 22 fields 的 DB raw value、API raw JSON value、display rule、
  Dashboard visible value 和 PASS/FAIL。

该矩阵不再允许错误 case 选择后宣称 OK/NOK closure。本轮没有执行真实 DB、
Pi 或 Dashboard runtime evidence。

## Gate A allowlist assessment

Architecture plan Section 17.1 的 exact proposed allowlist 与本轮静态 renderer
影响一致：

- schema.ts / schema tests：field type、nullability、enum、UTC、safe-integer
  与 cross-field fail-closed boundary；
- viewModel.ts / viewModel tests：raw/display、row role、result-only summary、
  same-item derivation；
- AcceptedEventsTable.tsx：当前直接承载 unknown 与 outcome display；
- NokDetailEvidencePanel.tsx：当前直接承载 unknown、production-result 与
  detail role display；
- PageSummaryStrip.tsx：当前直接承载全 row byResult summary；
- TraceReferencePanel.tsx：当前直接承载 null/empty 的 unknown display；
- page.test.tsx：只覆盖 ready/error/empty、same-fact 与 display regression，
  不需要修改 page.tsx 生产逻辑。

page.tsx、apiClient.ts、apiClient.test.ts、apiOrigin.ts、query.ts、package
files、API、DB、Collector、Docker/Compose、deployment guide 与 Grafana
仍应排除。四个候选 production component 均有直接显示影响，不存在可因
“仅 recommendation”移除的 component blocker。

但是，因 DQ-DASH-D1 的 source-preserving numeric validation 尚未在当前
allowlist 中形成可执行 seam，Gate A allowlist 目前不能作为无条件 implementation
authorization；需要先完成上述最小 Architecture docs-only repair 和独立 DQ
re-review。此处不自行扩大 allowlist。

## Gate A / Gate B sequencing assessment

**PASS WITH RECOMMENDATIONS — sequencing boundary is correct, but not yet eligible to start。**

- Gate A 只处理 accepted-events Consumer Truth Hardening：schema、view model、
  renderer display semantics 与 focused tests；必须独立完成 Architecture、
  Reliability、Data Quality、Verification focused implementation reviews。
- Gate A planning/review PASS 不授权 implementation、Git write 或 Gate B；本轮
  DQ-DASH-D1 为 HOLD，因此 Gate A 尚未获得 PM implementation authorization。
- Gate B 只能在 Gate A 独立关闭后恢复六文件范围：
  frontend/Dockerfile、frontend/.dockerignore、health route/test、
  docker-compose.yml、docs/deployment/raspberry_pi.md。
- Gate B 不得再次修改 schema、view model、renderer、consumer tests 或业务语义。

该分段能避免数据真实性修复与部署实现混在同一个 implementation gate；当前
不得进入 Gate B。

## Carry-forward recommendations

1. PM 只授权最小 Architecture docs-only repair，补齐 DQ-DASH-D1 的原始
   JSON number lexeme / no-rounding 实现边界；不得借此加入 debug surface、
   新业务字段或 UI 功能。
2. 不把 future BIGINT beyond safe integer 支持重新带入当前 DQ blocker；如需
   string serialization，另开 API contract planning gate。
3. 保留 DQ-DASH-D2 CLOSED 与 DQ-DASH-D3 CLOSED，不要因 D1 repair 重开
   已闭合的 outcome/detail 或 real Case A/B/C matrix，除非新修订改变其 authority。
4. 保持真实 DB-backed evidence、Pi/runtime、Verification、Gate A implementation、
   Gate B implementation 与 stage/commit/push 均未授权的边界。

## Next gate

    Current gate: Data Quality planning re-review = HOLD on DQ-DASH-D1
    Required next action: PM-authorized minimal Architecture docs-only repair for the DQ-DASH-D1 precision seam
    Then: independent Data Quality planning re-review
    Implementation: not authorized
    Verification: not authorized
    Gate B / Raspberry Pi / Docker / Compose / PostgreSQL / runtime: not authorized
    stage/commit/push/tag/deploy/rollback: not authorized

本轮完成后停止。
