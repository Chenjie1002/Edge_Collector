# Sprint 3 Accepted-events Consumer Truth Hardening Architecture Review

报告名称：Sprint 3 Accepted-events Consumer Truth Hardening Architecture Review

任务名称：Gate A — Accepted-events Consumer Truth Hardening Focused Implementation Review

执行 Thread：Architecture / Integration

日期：2026-07-14

## Conclusion

**PASS WITH RECOMMENDATIONS**

Gate A 的15文件implementation符合Architecture plan Sections 12.1–12.5、17.1。未发现HTTP runtime绕过source-preserving parser、raw numeric false PASS、cross-field遗漏、raw/display语义丢失、不同fact交叉绑定或职责漂移。

本结论只关闭Architecture focused implementation review，不表示Gate A已关闭，也不授权Gate B、runtime或Git write。

## Created/changed files

仅创建：

```text
CREATE docs/reports/sprint3_accepted_events_consumer_truth_hardening_architecture_review.md
```

未修改source、tests、planning reports、status或governance文件。

## Recovery baseline

```text
HEAD: bdda24fd930339b565d0c1894daece42c6039ac7
origin/main: bdda24fd930339b565d0c1894daece42c6039ac7
ahead/behind: 0 0
cached diff: empty
tracked frontend source diff: exact 15 Gate A files
excluded tracked diff: empty
```

## Architecture blockers

**None。**

## Transport/parser ownership assessment

**PASS。** 成功2xx runtime path为：

```text
HTTP Response
-> response.text()
-> parseAcceptedStationEventsEnvelopeJson(rawText)
-> source-preserving JSON parse
-> exact typed/cross-field parser
-> view model
```

`apiClient.ts`不再调用`response.json()`；只负责request、HTTP status mapping、raw text读取和schema parser调用。Endpoint、query、fetch options、single request、no retry、no fallback保持不变。

Malformed response使用稳定消息`Accepted events response was invalid.`；transport failure使用`Accepted events request failed.`。两者均不泄漏raw body、numeric lexeme、origin、DB error或parser细节。

## Source-preserving numeric assessment

**PASS。** Fresh evidence：

```text
Node: v22.23.0
parsed value: 9007199254740991
context.source: "9007199254740991.1"
```

Source gate覆盖`cycle_counter`、`nok_code`、`nok_detail_code`、`page.limit`。Number token必须取得`context.source`，匹配canonical integer regex，并通过`BigInt(source)` safe-range检查；typed parser随后再次执行number与`Number.isSafeInteger`验证。Fraction、exponent、leading-zero JSON form、`-0`和unsafe integer均fail closed。

`9007199254740991.1`不会因JavaScript舍入后变成safe integer而通过。Runtime缺少source context时fail closed，不存在普通JSON.parse fallback、第三方lossless dependency或tsconfig/package修改。

Key-based reviver对当前exact schema不存在false-PASS路径：四个目标均为直接primitive key；未知或嵌套同名字段最终仍由exact-key parser拒绝，只可能更早fail closed。

## Schema/cross-field assessment

**PASS。** `schema.ts`集中负责exact envelope、exact 22 keys、field type/nullability、safe integer、UTC ISO Z、event/result enum、cross-field contract与whole-response fail closed。

`AcceptedStationEventItem`已改为逐字段精确类型。UTC validation拒绝无时区、非Z、非法日期和错误格式，同时接受API的合法Z timestamp。

Cross-field实现与冻结矩阵一致：

- `station_result/nok`：NOK authority完整，detail全null；
- `station_result/non-NOK`：NOK/detail全null；
- `station_nok`：result为null，NOK/detail authority完整；
- cycle：result、NOK、detail全null；
- heartbeat、未知enum和非法组合进入view model前失败。

任一item失败会终止整个`items.map(parseItem)`，不存在bad-row skip或partial rendering。

## Raw/display/view-model assessment

**PASS。** View model保持typed raw item、display text、display kind三层分离。Raw null仍为null，raw empty仍为`""`；display分别为`—`和`Empty string`。Invalid/missing无法进入display层，不再使用泛化`unknown`。

`copyAcceptedItem()`只是同一精确22字段类型的防御性副本，不形成第二套事实authority。Rows、NOK/detail和trace均从同一`sourceItems`集合派生；selected item使用raw `fact_key`比较，三个surface共享同一个source object。

## Renderer/same-fact assessment

**PASS。** 四个components只展示view-model字段，不自行推断production result、NOK authority或DB source。

- `station_nok`显示`Not applicable — NOK detail companion`；
- cycle显示`Not applicable — cycle event`；
- `byResult`只统计`station_result`；
- total统计当前页全部accepted rows；
- summary明确标示`station_result only`；
- NOK/detail panel显示row role和event type；
- trace区分null与empty。

未修改的`page.tsx`继续把第一row `factKey`传给table；view model默认也选择第一source item。Page integration test证明table、detail和trace绑定同一首项fact，summary不会把detail companion计为production result。

## Validation results

```text
Node/context.source: PASS
Focused tests: 8 files, 167 passed
Full tests: 11 files, 237 passed
Typecheck --incremental false: PASS
Next production build: PASS
frontend/src diff check: PASS
```

Tests覆盖fraction、exponent、rounding、unsafe integer、source缺失、exact types/nullability、UTC/enum、cross-field、whole-response failure、raw/display、null/empty、outcome/detail、result-only summary、same-fact、ready/empty/error/no-stale、response.text、no response.json、one request、no retry/no fallback及error leakage。

## Allowlist compliance

**PASS。** Tracked frontend source diff精确为15个Gate A allowlist文件；allowlist外frontend tracked diff为0；cached diff为空。`.gitignore`是既有external tracked modification。未stage、commit或push。

## Generated/external artifacts

Generated：

```text
frontend/.next/
frontend/next-env.d.ts
```

Pre-existing external：

```text
M  .gitignore
?? frontend/node_modules/
?? frontend/tsconfig.tsbuildinfo
?? docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_*.md
?? existing handoff and historical reports
```

均未手工修改、删除、整理或stage。

## Recommendations

1. Reliability review继续验证Node 22.23.0/source-context前提和缺失时fail-closed，禁止兼容fallback。
2. Verification可将每个detail字段的逐项negative permutation作为覆盖率增强；当前静态字段审计与代表性tests已足以支持Architecture PASS，该项不构成blocker。
3. Future BIGINT serialization、real DB-backed Case A/B/C、Pi runtime与Gate B继续留在独立gate。

## Next gate

```text
Architecture focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS
Gate A overall: NOT CLOSED
Next eligible gate: PM安排Reliability focused implementation review
```

本轮完成后停止。
