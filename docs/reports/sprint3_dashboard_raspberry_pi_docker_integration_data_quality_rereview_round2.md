# Sprint 3 Dashboard Raspberry Pi Docker Integration Data Quality Re-review Round 2

报告名称：Sprint 3 Dashboard Raspberry Pi Docker Integration Data Quality Re-review Round 2

任务名称：复验 DQ-DASH-D1 Numeric Source-preservation Repair

执行 Thread：Data Quality

日期：2026-07-14

## Conclusion

**PASS WITH RECOMMENDATIONS**

本轮为 docs-only Data Quality planning re-review round 2。Architecture plan
已冻结足以关闭上一轮 residual numeric source-preservation false-PASS 风险的
runtime seam：

    HTTP Response
    -> response.text()
    -> source-preserving JSON parse
    -> exact envelope / exact 22-field typed parser
    -> cross-field validation
    -> view model

结论明确为：

- DQ-DASH-D1 CLOSED
- DQ-DASH-D2 remains CLOSED
- DQ-DASH-D3 remains CLOSED

这是 planning closure，不是 implementation closure。现有 frontend 仍使用旧的
response.json() 和 parsed-object parser，未在本轮执行或修改。下一 Gate 只能由
PM 决定是否授权 Gate A implementation。

## Created/changed files

- CREATE docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_rereview_round2.md
- Existing files changed: none by this task。
- Architecture plan、原 Data Quality review/re-review、Reliability reports、
  frontend、API、DB、Collector、Docker/Compose、deployment guide、status、
  PM rules 与 .gitignore 均未修改。
- 本轮未运行 tests、typecheck、build、Docker、Compose、PostgreSQL、Raspberry Pi
  或 runtime。

## Recovery baseline

    project: /Users/chenjie/Documents/MES/edge-mes-demo
    branch: main
    HEAD: bdda24fd930339b565d0c1894daece42c6039ac7
    origin/main: bdda24fd930339b565d0c1894daece42c6039ac7
    ahead/behind: 0 0
    latest: bdda24f Reset Dashboard URL validation scope
    cached diff: empty before this report creation
    target report before this write: absent

既存 .gitignore tracked modification 与大量 external untracked artifacts 均被识别
并保留未动，包括历史 reports/handoff、frontend/node_modules/ 和
frontend/tsconfig.tsbuildinfo。

## DQ-DASH-D1 status

**CLOSED。**

Architecture plan Section 12.1 已把 HTTP runtime authority 从当前
await response.json() 修订为 response.text() 后的 source-preserving parser。
普通 JSON.parse(rawText) 后再检查 parsed number 被明确禁止；parsed-object parser
仅可用于 synthetic/internal typed-object tests，不能作为 HTTP response authority。

## DQ-DASH-D2/D3 preserved status

**DQ-DASH-D2 remains CLOSED。**

**DQ-DASH-D3 remains CLOSED。**

本轮 D1 repair 未改变 cross-field/raw-display/outcome-detail contract，
也未改变 real Case A/B/C matrix；按 authority 不重新审查或重新打开这两项。

## Source-preservation assessment

该方案足以关闭上一轮 false-PASS 路径，理由如下：

1. 对 cycle_counter、nok_code、nok_detail_code 和 page.limit，raw-text parser
   必须从 JSON.parse reviver context.source 取得原始 numeric token。
2. source context 缺失时整个 response fail closed，不退回普通 JSON.parse 或
   parsed-object validation。
3. 原始 token 必须匹配 canonical decimal integer：

       ^(?:0|-?[1-9][0-9]*)$

   因此 fraction、exponent、leading-zero 变体和 -0 均被拒绝。
4. 词法通过后使用 BigInt(context.source) 检查 Number.MIN_SAFE_INTEGER 到
   Number.MAX_SAFE_INTEGER；超出范围整体 fail closed。
5. raw-token gate 后仍执行 typed parser 的 typeof number、
   Number.isSafeInteger、field nullability、page.limit 1..500 和 cross-field
   validation。
6. 对 9007199254740991.1，context.source 保留小数 token，canonical integer
   regex 在任何 parsed safe integer 被信任前拒绝它，因此不会发生 rounded
   fraction false PASS。
7. 任一 item 或 page.limit 非法都会使整个 malformed 2xx response 失败，不会
   partial rendering。

Runtime compatibility boundary 已明确：Node 22.23.0 的 reviver context.source
是实现前提；当前 tsconfig 的 ES2022 lib 不需要修改，schema.ts 可使用
module-local type wrapper/type narrowing；不需要第三方 dependency。实际没有
source context 时必须 fail closed。未来 BIGINT string serialization 不属于本
轮 blocker。

Error/security boundary 也已冻结：raw-text syntax、numeric token、exact parser
或 cross-field failure 映射现有 client kind: error，使用稳定通用安全消息，不
回显 raw body、numeric lexeme、trusted origin、DB error 或 parser 内部信息；
request URL、fetch options、status mapping、single-request、no-retry、
no-fallback 保持不变。

Focused test contract 已覆盖：

- 拒绝 cycle_counter 1.0、1e0、9007199254740991.1、9007199254740992、
  "12"；
- 拒绝 nok_code 10.0、nok_detail_code 2e0、page.limit 50.0 和 -0；
- 接受 cycle_counter 0、9007199254740991、-9007199254740991、
  nullable numeric null 和 page.limit 50；
- 证明非法 item、source context 缺失、raw body/lexeme leakage、response.text()
  runtime authority、single request、no retry、no fallback 与 kind: error。

## Gate A allowlist assessment

**PASS — 15-file allowlist is necessary and sufficient for the frozen Gate A scope。**

Section 17.1 的 15-file allowlist 与 source-preservation seam 和当前静态
renderer impact 一致：

    MODIFY frontend/src/lib/acceptedStationEvents/schema.ts
    MODIFY frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts
    MODIFY frontend/src/lib/acceptedStationEvents/apiClient.ts
    MODIFY frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
    MODIFY frontend/src/lib/acceptedStationEvents/viewModel.ts
    MODIFY frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts
    MODIFY frontend/src/components/accepted-events/AcceptedEventsTable.tsx
    MODIFY frontend/src/components/accepted-events/__tests__/AcceptedEventsTable.test.tsx
    MODIFY frontend/src/components/accepted-events/NokDetailEvidencePanel.tsx
    MODIFY frontend/src/components/accepted-events/__tests__/NokDetailEvidencePanel.test.tsx
    MODIFY frontend/src/components/accepted-events/PageSummaryStrip.tsx
    MODIFY frontend/src/components/accepted-events/__tests__/PageSummaryStrip.test.tsx
    MODIFY frontend/src/components/accepted-events/TraceReferencePanel.tsx
    MODIFY frontend/src/components/accepted-events/__tests__/TraceReferencePanel.test.tsx
    MODIFY frontend/src/app/accepted-events/__tests__/page.test.tsx

apiClient.ts 和 apiClient.test.ts 是不可绕过的最小 transport seam：只有它们能
把 response.json() 替换为 response.text() 并证明 HTTP runtime 使用 raw-text
authority。schema-only 13-file allowlist 无法恢复已经丢失的 numeric lexeme。

继续排除 page.tsx、apiOrigin.ts、query.ts、package files、tsconfig.json、
next.config.ts、API、DB、Collector、Docker/Compose、deployment guide、
Grafana、第三方 lossless JSON library、API serialization change、debug view、
raw-data page 和新业务功能。

## Carry-forward recommendations

1. PM 如授权 Gate A implementation，严格使用上述 15-file allowlist；先实现并
   验证 response.text() 与 raw-text parser，再进入完整 Consumer Truth Hardening
   focused review。
2. implementation/runtime 必须保持 Node 22.23.0 source-context 前提；source
   context 缺失只能 error，不得启用兼容 fallback。
3. DQ-DASH-D2/D3 保持 CLOSED；除非 Gate A 实现改变其 authority，否则不得
   重开 cross-field contract 或 Case A/B/C matrix。
4. 不把 future BIGINT、Pi/runtime evidence、Docker/Compose 或 Verification
   未执行作为本轮 blocker；这些仍属于后续独立授权边界。

## Next gate

    Current gate: Data Quality planning re-review round 2 = PASS WITH RECOMMENDATIONS
    DQ-DASH-D1: CLOSED
    DQ-DASH-D2: remains CLOSED
    DQ-DASH-D3: remains CLOSED
    Next eligible gate: PM decision on Gate A implementation authorization
    Gate A implementation/tests: not authorized by this report
    Verification / Gate B / Raspberry Pi / Docker / Compose / runtime: not authorized
    stage/commit/push/tag/deploy/rollback: not authorized

本轮完成后停止。
