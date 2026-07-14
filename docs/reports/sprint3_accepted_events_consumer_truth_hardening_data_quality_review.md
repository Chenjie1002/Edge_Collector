# Sprint 3 Accepted-events Consumer Truth Hardening Data Quality Review

报告名称：`Sprint 3 Accepted-events Consumer Truth Hardening Data Quality Review`

任务名称：`Gate A — Accepted-events Consumer Truth Hardening Focused Data Quality Review`

执行 Thread：`Data Quality`

日期：`2026-07-14`

## Conclusion

**PASS WITH RECOMMENDATIONS**

本轮 Data Quality focused implementation review 已关闭，无 Data Quality blocker。
结论只关闭本轮 Data Quality review，不宣布 Gate A 整体关闭，不授权 Gate B、Docker、
Compose、PostgreSQL、Raspberry Pi、real runtime 或 Git write。

当前证据仍严格标记为 `synthetic / focused implementation evidence`，不是
`real DB-backed`、Raspberry Pi closed-loop 或 Case A/B/C runtime PASS。

## Created/changed files

本轮只创建：

```text
docs/reports/sprint3_accepted_events_consumer_truth_hardening_data_quality_review.md
```

未修改任何 source、test、planning report、status 或 governance 文件。Gate A 15 个
implementation files 仅作为既有 working-tree diff 被审查；本轮没有 source repair。

审查范围包括：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_plan.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_review.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_rereview.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_rereview_round2.md`
- `docs/reports/sprint3_accepted_events_consumer_truth_hardening_architecture_review.md`
- `docs/reports/sprint3_accepted_events_consumer_truth_hardening_reliability_review.md`
- `db/migrations/007_accepted_station_event_visibility.sql`
- `api/app/routes/accepted_station_events.py`
- Gate A exact 15 frontend implementation/test files

为确认 stale/error 与 excluded surface 的只读边界，另外静态读取了未修改的
`frontend/src/app/accepted-events/page.tsx`、`frontend/src/lib/acceptedStationEvents/query.ts`
和 `frontend/src/lib/acceptedStationEvents/apiOrigin.ts`；没有对它们做任何修改。

## Recovery baseline

第一动作已完成 read-only recovery：

```text
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: bdda24fd930339b565d0c1894daece42c6039ac7
origin/main: bdda24fd930339b565d0c1894daece42c6039ac7
ahead/behind: 0/0
cached diff: empty
tracked frontend source diff: exact 15 Gate A files
```

只读确认以下排除路径没有 tracked diff/status entry：

```text
frontend/src/app/accepted-events/page.tsx
frontend/src/lib/acceptedStationEvents/apiOrigin.ts
frontend/src/lib/acceptedStationEvents/query.ts
frontend/package.json
frontend/package-lock.json
frontend/tsconfig.json
frontend/next.config.ts
api/
collector/
db/
docker-compose.yml
docs/deployment/raspberry_pi.md
```

`.gitignore` 是既有 external tracked modification，不属于 Gate A allowlist。本轮没有
commit、push、tag、stage 或其他 Git write。

## Data Quality blockers

**None。**

没有发现以下 blocker：accepted-fact source leakage、22-field type/nullability 或 raw
value 丢失、numeric false PASS、config/identity/time lineage 改写、outcome/detail 混淆、
null/empty/not-applicable 混淆、table/detail/trace 跨 fact 绑定、partial/stale truth、
synthetic evidence 被称为 real closure、fresh validation failure 或 15-file allowlist
越界。

## Accepted-fact authority assessment

**PASS。** `production_accepted_station_event_fact` 仍是唯一 production source。
`api/app/routes/accepted_station_events.py` 的 `DTO_FIELDS` 逐字段从该表读取，SQL 没有
legacy、raw、diagnostic、Collector log、Grafana 或其他 endpoint fallback。Migration 的
accepted-only table/comment、event-type/result/NOK/detail constraints 与 API read path
authority保持不变。

Consumer 只接受 endpoint 的 exact envelope：外层 `data` / `page`，`data.items`，
`page.next_cursor` / `limit`，以及 item exact 22-key set。unknown key、missing key、
wrong type 或 cross-field violation 会使整个 2xx response 进入 stable `kind: "error"`，
不会进入 partial ready state。frontend 没有自行创建、合并或推断 accepted fact，也没有
把 duplicate、conflict、rejected、diagnostic disposition 投影为 production UI fact。

`raw_payload`、`raw_hex`、candidate/normalized payload、adapter reason、diagnostic
context、`ack_status`、`read_done`、`quality_pareto_input`、`dashboard_state`、
`work_order`、`product` 等 forbidden surfaces 没有进入 production consumer model。

## Exact 22-field assessment

**PASS。** `AcceptedStationEventItem` 与 API `DTO_FIELDS` 保持以下 exact key set：

```text
line_id
plc_id
station_id
station_type
profile_id
config_hash
config_version
event_type
production_result
unit_id
dmc
cycle_counter
source_event_id
event_ts
accepted_at
fact_key
content_fingerprint
nok_code
nok_origin
nok_detail_code
nok_detail_source_event_id
nok_detail_evidence_fact_key
```

`schema.ts` 同时执行 outer/data/page/item exact own-key 检查和 required own-property
检查。13 个 required string fields 不能为 `null` 或错误类型；nullable string 只接受
string 或显式 JSON `null`；numeric fields 只接受合同允许的 safe-integer number 或
显式 `null`；numeric-looking string 会被拒绝。`event_type` 和 non-null
`production_result` 仅接受冻结枚举；`event_ts` 与 `accepted_at` 分别保持 UTC `Z`
时间语义。任一 item 非法都会终止整个 `items.map(parseItem)`，不产生 partial ready
state。

## Numeric source-preservation assessment

**PASS。** runtime path 在 `apiClient.ts` 使用 `response.text()`，随后调用
`parseAcceptedStationEventsEnvelopeJson(rawText)`。reviver 对以下字段在信任 parsed
number 前读取 `context.source`：

```text
cycle_counter
nok_code
nok_detail_code
page.limit
```

`context.source` 缺失时 fail closed；canonical integer regex
`^(?:0|-?[1-9][0-9]*)$` 拒绝 fraction、exponent、leading zero 和 `-0`；随后使用
`BigInt(source)` 检查 `Number.MIN_SAFE_INTEGER` 到 `Number.MAX_SAFE_INTEGER`，typed
parser 再执行 `Number.isSafeInteger` 与 `page.limit` `1..500` 检查。显式 nullable numeric
`null` 不会被改写。

fresh witness：

```text
Node: v22.23.0
parsed value: 9007199254740991
context.source: "9007199254740991.1"
```

因此 `9007199254740991.1` 不会在舍入后错误通过；raw lexeme 不进入 error message。
当前合同仍是 safe-integer number contract，future BIGINT serialization 不属于本 Gate。

## Lineage assessment

**PASS。**

- Configuration lineage：`line_id`、`plc_id`、`station_id`、`station_type`、`profile_id`、
  `config_hash`、`config_version` 均由 accepted item 原样保留；页面 current selection、
  命名规则或 current config 不会补值或覆盖历史 row。
- Identity lineage：`fact_key` 是 table/detail/trace 的主 identity；`source_event_id`
  没有替代它；`content_fingerprint` 不会被重新计算、缩短或重新格式化；
  `copyAcceptedItem()` 保持所有 22 个 raw fields 不变。
- Time lineage：`event_ts` 仍为 source event time；`accepted_at` 仍为 accepted fact
  timestamp。renderer label 没有互换，display formatting 没有回写 raw timestamp。

## NOK/detail assessment

**PASS。** parser cross-field contract与renderer语义保持一致：

- `station_result` + `nok`：result、`nok_code`、`nok_origin` 非null，三个 detail
  fields 全null。
- `station_result` + `ok` / `skip` / `not_applicable`：result 非null，NOK 与 detail
  fields 全null。
- `station_nok`：`production_result=null`，NOK 与三个 detail authority fields 全部
  非null，显示为 `station_nok detail companion`，不显示为第二个 production outcome。
- cycle event：production result、NOK 与 detail fields 全部为null。

unknown event/result、heartbeat 与 malformed combination 在 view model 前被拒绝。
`byResult` 只统计 `station_result`；`station_nok` 与 cycle event 不进入 production-result
分布。NOK panel 展示 row role、event type、NOK code/origin、detail code、detail source
event 和 evidence fact reference，且均从同一 typed source item 派生。

## Raw/display assessment

**PASS。** view model 保持 `raw`、`text`、`kind` 分层：

- raw `null` 保持 `null`，display 为 `—` / 对应 not-applicable rule；
- raw empty string 保持 `""`，display 为 `Empty string`；
- raw number 保持原 number，display 只做文本化；
- `—`、`Empty string`、`Not applicable` 仅属于 display layer；
- invalid、missing、unsupported 和 malformed 不会变成 display state；
- 没有使用 `unknown` 混淆 null、empty、invalid、missing 或 not applicable。

`sourceItem`、`AcceptedEventRow`、`NokDetailEvidence` 与 `TraceReference` 均保留同一
typed raw item。table、NOK/detail、trace 都从同一 `sourceItems` 派生；防御性
`copyAcceptedItem()` 只是复制 22 个 accepted fields，不创建第二事实 authority。Trace
panel 可见地映射 unit、DMC、cycle counter、source event、event time、accepted time、
fact key、content fingerprint、line/PLC/station、profile、config version、config hash。

## Same-fact and stale-truth assessment

**PASS。** `selectedItem` 以 raw `fact_key` 比较；selected key 不存在时使用冻结的
first-item fallback，empty response 时 evidence/reference 均为 `null`。table 首项、
selected evidence 与 selected trace reference 共享同一个 `sourceItem` 和 `fact_key`；
当前证据范围只支持目标 `items[0]` 的三层绑定，不扩展为整页所有 rows 的 closed-loop
claim。

未修改的 `page.tsx` 保持 `dynamic = "force-dynamic"`，只在 client result 为 ready 时
构造 production surfaces。invalid-query、transport error、503、其他 5xx、malformed
2xx 和 source-parser failure 均不渲染 table、summary、detail 或 trace。empty response
生成当前页零计数 summary，不保留上一请求的 row 或 selected evidence/reference。当前
server-rendered page 没有跨请求 production-state cache；本轮不重新审查 Reliability 已
关闭的 request-loop 语义。

## Synthetic/real evidence assessment

**PASS WITH BOUNDARY PRESERVED。** 当前 focused tests、typecheck 和 build 只能标记为：

```text
synthetic / focused implementation evidence
```

它们不能被解释为 `real DB-backed`、Raspberry Pi closed-loop、Case A/B/C runtime PASS，
也不能替代 PostgreSQL raw row、API raw JSON item 与 Dashboard visible-value 的三层对账。
Synthetic fixtures 没有从 raw、legacy、diagnostic 或 Collector log 补值，并明确区分
station-result OK、station-result NOK、station-nok detail companion 与 cycle event；没有
使用 cycle event 替代 OK outcome，也没有使用 station-nok detail 替代 NOK outcome。

真实 Case A/B/C 仍留给后续独立 runtime gate；真实 `station_nok` 不存在时必须记录
`NOT AVAILABLE / NOT VERIFIED`，不能用 synthetic fixture 宣布 closure。

## Validation results

所有授权 validation 命令均执行一次并通过：

```text
node -v
PASS: v22.23.0

node -e 'JSON.parse("{\"value\":9007199254740991.1}", (key, value, context) => { if (key === "value") console.log(JSON.stringify({ value, source: context?.source })); })'
PASS: {"value":9007199254740991,"source":"9007199254740991.1"}

Focused npm test:
  npm test -- src/lib/acceptedStationEvents/__tests__/schema.test.ts src/lib/acceptedStationEvents/__tests__/apiClient.test.ts src/lib/acceptedStationEvents/__tests__/viewModel.test.ts src/components/accepted-events/__tests__/AcceptedEventsTable.test.tsx src/components/accepted-events/__tests__/NokDetailEvidencePanel.test.tsx src/components/accepted-events/__tests__/PageSummaryStrip.test.tsx src/components/accepted-events/__tests__/TraceReferencePanel.test.tsx src/app/accepted-events/__tests__/page.test.tsx
PASS: 8 files, 167 tests

npm test
PASS: 11 files, 237 tests

npm run typecheck -- --incremental false
PASS: tsc --noEmit --incremental false

NEXT_TELEMETRY_DISABLED=1 npm run build
PASS: Next.js 16.2.10; /accepted-events is dynamic/server-rendered
```

本轮没有运行 Docker、Compose、PostgreSQL、SSH、Raspberry Pi、browser/server runtime、
DB-backed Case A/B/C 或 Gate B action。

## Allowlist compliance

**PASS。** 完成的只读审计结果：

```text
git diff --check -- frontend/src       PASS
git diff --name-only -- frontend/src   exact 15 Gate A files
git diff --cached --name-only          empty
```

frontend allowlist 外没有 tracked source diff；`.gitignore` 是已知 external modification，
不在 Gate A 15-file implementation allowlist 内。report 文件是本轮唯一获准创建的文件，
未被 stage。没有发生 commit、push、tag 或其他 Git write。

## Generated/external artifacts

validation/build 后可见的 generated artifacts：

```text
frontend/.next/
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
```

既有 external dirty artifacts 包括：

```text
M  .gitignore
?? frontend/node_modules/
?? existing docs/thread_handoff/*.md
?? existing docs/reports/*.md and historical HTML/report artifacts
```

这些 artifacts 均未被本轮手工修改、删除、清理、整理或 stage；`.next/`、
`next-env.d.ts`、`node_modules/`、`tsconfig.tsbuildinfo` 与其他 reports 均不属于本轮
allowlist。

## Recommendations

1. PM 安排下一步 Verification focused implementation review；保持 Architecture、
   Reliability、Data Quality、Verification 四个结论独立，不因本轮 PASS WITH
   RECOMMENDATIONS 宣布 Gate A overall closure。
2. Verification 可补充 selected key 不存在时 first-item fallback、`skip` /
   `not_applicable` 的直接代表性 fixture，以及每个 detail field 的排列组合 negative
   tests；这些是覆盖率增强，不是本轮 blocker。
3. 后续 real runtime gate 必须逐字段保存 DB raw 22 fields、API raw JSON 22 fields、
   Dashboard display rule/visible value，并把声明范围限制为每个 bounded request 的
   目标第一项；不得用 build、health、mock 或截图代替真实 accepted-fact evidence。
4. 超出 JavaScript safe integer 的 future BIGINT serialization 需要单独 API/contract
   gate，不得在当前 consumer 中静默舍入、截断或改用模糊文本。

## Next gate

```text
Data Quality focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS
Gate A overall: NOT CLOSED
Next eligible gate: PM安排 Verification focused implementation review
Gate B / Docker / Compose / PostgreSQL / Raspberry Pi / runtime: not authorized
Git stage/commit/push/tag: not authorized
```

本轮完成后停止，不进入 Verification、Gate B 或 Git write。

## Thread 输出 / 上下文评估

- 本次输出长度：长。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：no。
- 理由：本轮 Data Quality focused implementation review 已完成；后续只在 PM 明确安排
  的 Verification focused implementation review 中继续，不在当前 Data Quality 结论上
  自动串行进入下一 Gate。
