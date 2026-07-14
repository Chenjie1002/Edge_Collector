# Sprint 3 Accepted-events Consumer Truth Hardening Verification Review

报告名称：Sprint 3 Accepted-events Consumer Truth Hardening Verification Review
任务名称：Gate A — Accepted-events Consumer Truth Hardening Focused Verification Review
执行 Thread：Verification
日期：2026-07-14

## Conclusion

**PASS WITH RECOMMENDATIONS**

本轮 Verification focused implementation review 已关闭，无 Verification blocker。结论只关闭本轮 focused implementation review，不宣布 Gate A overall 关闭，不授权 Gate B、Docker、Compose、PostgreSQL、Raspberry Pi、browser/server runtime、real DB-backed Case A/B/C 或 Git write。

当前证据严格为：

~~~
synthetic / focused implementation evidence
~~~

不能解释为真实 DB/API/Dashboard 三层闭环、Raspberry Pi runtime PASS 或 Gate B deployment PASS。

## Created/changed files

本轮只创建：

~~~
docs/reports/sprint3_accepted_events_consumer_truth_hardening_verification_review.md
~~~

未修改 source、tests、planning/review reports、status 或 governance 文件；未执行 source/test repair。

## Recovery baseline

第一动作已完成 read-only recovery：

~~~
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: bdda24fd930339b565d0c1894daece42c6039ac7
origin/main: bdda24fd930339b565d0c1894daece42c6039ac7
ahead/behind: 0/0
cached diff: empty
tracked frontend source diff: exact 15 Gate A files
target report before recovery: absent
~~~

live tracked diff 另有既有 .gitignore 一项；它不属于 Gate A implementation allowlist。以下排除路径只读确认无 tracked diff/status entry：

~~~
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
~~~

## Verification blockers

**None。**

实现存在完整的 source-preserving runtime seam、exact envelope/22-field parser、typed and cross-field fail-closed boundary、raw/display separation、same-fact derivation 和 non-ready no-stale page boundary；全部授权 fresh validation 均 exit 0。未发现需要修改 source/test 或排除路径才能保证冻结合同的真实缺口。

## Contract-to-test matrix assessment

| Architecture requirement | Production implementation location | Focused test location | Result |
| --- | --- | --- | --- |
| Accepted-fact source boundary / exact DTO authority | api/app/routes/accepted_station_events.py:18-41,211-217；schema.ts:1-24 | schema.test.ts:294-323；viewModel.test.ts:143-162 | PASS；只保留 accepted-fact 22-field allowlist，不接 raw/diagnostic/legacy fallback |
| Source-preserving HTTP seam | apiClient.ts:41-48；schema.ts:315-323 | apiClient.test.ts:91-108,158-194,213-219；schema.test.ts:136-180 | PASS；response.text → context.source parser；single fetch/no retry/no fallback |
| Exact envelope/data/page/item keys | schema.ts:71-104,238-268,287-312 | schema.test.ts:294-310,325-331；apiClient.test.ts:141-156 | PASS；unknown/missing item key、outer/data/page extra key fail closed；通用 helper 同时检查 missing key |
| 22-field type/nullability | schema.ts:112-132,242-265 | schema.test.ts:212-250,306-310 | PASS；required string、nullable string、safe integer 和 explicit null 按类型解析 |
| Numeric lexeme / safe-range | schema.ts:74-77,271-284；122-132,302-303 | schema.test.ts:98-134,136-189,238-250,329-331；apiClient.test.ts:158-175 | PASS；fraction/exponent/rounded fraction/unsafe/-0/string/source-missing/page-limit negative paths fail closed |
| UTC / enum | schema.ts:134-185 | schema.test.ts:252-273 | PASS；UTC Z、fraction、日期有效性和 event/result enum 均由 helper 与 focused tests 覆盖 |
| Cross-field authority | schema.ts:188-236,267-268 | schema.test.ts:193-201,275-292 | PASS；station result、station_nok detail companion、cycle 非法组合不会部分返回 |
| Whole-response atomicity / empty | schema.ts:295-312 的 items.map(parseItem) | schema.test.ts:182-189,203-210,329-331；apiClient.test.ts:147-175 | PASS；合法 item + 非法第二 item 整体 error；empty items 合法；malformed 2xx 不降级 |
| Raw/display separation | viewModel.ts:85-118,153-203 | viewModel.test.ts:68-97；renderer tests | PASS；raw null、空字符串、normal value 与 display kind 分离；无 unknown |
| Summary / four renderers | viewModel.ts:206-236；四个 renderer | 四个 component tests；page.test.tsx:293-314 | PASS；total 为当前页全部 rows，byResult 只统计 station_result，四个 surface 来源一致 |
| Same-fact selected key | viewModel.ts:206-236；unchanged page.tsx:63-67 | viewModel.test.ts:110-133；page.test.tsx:293-314 | PASS；存在 key、first-item、empty null、相同 fact_key 均成立 |
| Error/empty/no-stale | unchanged page.tsx:42-68,73-103；apiClient.ts:31-49 | page.test.tsx:205-329,331-387；apiClient.test.ts:117-219 | PASS；invalid query、transport/error、503、5xx、malformed 2xx、empty、ready 分层 |
| Allowlist / excluded boundary | live Git diff | git diff --check -- frontend/src and final audit | PASS；frontend tracked diff exact 15，excluded tracked diff 0，cached empty |

联合判断：未直接机械穷举的项目均有明确通用 parser/helper 静态条件和代表性 focused test；剩余直接样例增强列为 recommendation，不构成当前真实 blocker。

## Numeric source verification

成功 2xx runtime path 已确认严格为：

~~~
response.text()
→ parseAcceptedStationEventsEnvelopeJson(rawText)
→ JSON.parse(rawText, reviver context.source)
→ parseAcceptedStationEventsEnvelope(parsed)
→ exact typed/cross-field parser
~~~

静态审计结果：

- apiClient.ts production code 不存在 response.json；每次成功调用只执行一次 response.text；未发现第二次 body read、retry、fallback endpoint 或 ordinary parsed-object HTTP path。
- schema.ts:271-284 在信任 number 前读取 context.source，对 cycle_counter、nok_code、nok_detail_code、page.limit 执行 canonical integer regex 和 BigInt(source) safe-range；schema.ts:122-132,302-303 随后执行 typed Number.isSafeInteger 与 page 1..500 检查。
- source context 缺失由 schema.test.ts:136-160 证明整体 fail closed；不存在普通 JSON.parse fallback。parseAcceptedStationEventsEnvelope(value) 仅作为 typed/synthetic parser，HTTP runtime 不直接调用它。
- package、lockfile、tsconfig 无 diff；未发现第三方 lossless JSON dependency。production JSON.parse 只有带 reviver 的 raw-text authority，测试 fixture 普通 parse 不构成 runtime fallback。

fresh Node witness：

~~~
node: v22.23.0
input token: 9007199254740991.1
parsed value: 9007199254740991
context.source: "9007199254740991.1"
~~~

focused evidence 直接覆盖：

~~~
cycle_counter: 1.0, 1e0, 9007199254740991.1, 9007199254740992, -0
nok_code: 10.0
nok_detail_code: 2e0
page.limit: 50.0, 0, 501
numeric-looking string: "12"
source context missing
~~~

合法 cycle_counter 直接覆盖 0、Number.MAX_SAFE_INTEGER、Number.MIN_SAFE_INTEGER；nullable nok_code/nok_detail_code=null 和 canonical page limit 50；typed parser 另覆盖 string/fraction/unsafe integer rejection。任一 numeric/source/parser 错误均收敛为 kind:error，raw body、origin、numeric lexeme 和 parser detail 不进入消息。

## Exact field/cross-field verification

acceptedStationEventFields 与 API DTO_FIELDS 均为冻结的 22-field exact set：

~~~
line_id, plc_id, station_id, station_type, profile_id, config_hash,
config_version, event_type, production_result, unit_id, dmc, cycle_counter,
source_event_id, event_ts, accepted_at, fact_key, content_fingerprint,
nok_code, nok_origin, nok_detail_code, nok_detail_source_event_id,
nok_detail_evidence_fact_key
~~~

assertExactOwnKeys 同时拒绝 unknown key 和 missing required key；required string helper 拒绝 null、number、boolean、object、array，nullable string 只接受 string 或显式 null，numeric helper 只接受合同允许的 safe integer 或 explicit null。event_type 与 production_result unknown enum fail closed；UTC helper 只接受有效 Z timestamp，拒绝无 Z、offset、非法日期和 number。

Cross-field 矩阵结论：

- station_result + ok：NOK/detail 全 null；station_result + nok：result、nok_code、nok_origin 非 null，detail 全 null。
- station_nok：production_result=null，NOK 与三个 detail authority 均非 null，作为 station_nok detail companion。
- cycle start/complete：result、NOK、detail 全 null。
- negative matrix 直接覆盖 result 缺失、NOK 缺 code/origin、station result 携带 detail 或非-NOK 携带 NOK、station_nok 携带 production result、station_nok 缺 detail authority、cycle 携带 result/NOK/detail。hasAnyDetailValue 对三个 detail field 采用同一 fail-closed 判断。
- skip 与 not_applicable 已纳入 frozen enum 和 station-result typed path；当前没有单独 fixture，列为覆盖增强 recommendation。

UTC direct evidence 包含无 fraction、合法 fraction 和 invalid date；calendar round-trip 静态拒绝非法月份/日期/时分秒。闰年 valid sample、page limit 1/500、负向 unsafe lexeme -9007199254740992 和各 numeric nullable code 的 boundary sample可补为直接 fixture，但没有发现当前实现的 false-PASS 或 authority 漏项。

## Whole-response atomicity

schema.ts:307 使用 items.map(parseItem)；任何 item parse/type/cross-field exception 都会终止整个 response，不跳过前面已解析的合法 item。focused test 构造了合法 item + 非法第二 item，并确认整体抛出；apiClient.test.ts 确认 malformed 2xx 统一为：

~~~
{ ok: false, kind: "error", message: "Accepted events response was invalid." }
~~~

invalid page.limit、invalid cross-field item 和 exact envelope failure 均不能变成 partial ready。items=[] 是合法 empty；malformed envelope 不降级为 empty；page empty ready 只展示当前页零计数和 empty state，不保留上一 ready fact。

## Raw/display and renderer verification

view model 保留 typed sourceItem 与 display layer：

- raw null 保持 null，display 为 —、kind:"null"；
- raw empty string 保持 ""，display 为 Empty string、kind:"empty-string"；
- normal string/number 保留原 raw value，display 只做文本化、kind:"value"；
- station_nok 为 Not applicable — NOK detail companion；cycle 为 Not applicable — cycle event；placeholder 不回写 raw 字段；无 unknown；
- copyAcceptedItem 保留全部 22 个 typed raw fields；invalid/missing item 在 view model 前被拒绝。

四个 renderer 静态/测试结论：

- AcceptedEventsTable 显示 station、event type、event/outcome、event time、accepted fact timestamp、unit、DMC；component tests覆盖 station_nok 与 cycle not-applicable。
- NokDetailEvidencePanel 显示 row role、event type、result、NOK code/origin、detail code、detail source event、evidence fact 和 fact reference；不自行推断 production authority。
- PageSummaryStrip 明确显示 Production result mix (station_result only)；total 统计当前页全部 accepted rows，station_nok/cycle 不进入 result mix，skip/not_applicable 的 station-result path可进入 mix。
- TraceReferencePanel 映射 identity、configuration、time 和 trace fields；null 与 empty string显示不同，不重新解析 raw number。

## Same-fact/no-stale verification

toAcceptedEventsViewModel 先从同一 envelope.items 建立 sourceItems，rows、selected evidence、selected reference均从该集合派生；selected key 使用 raw fact_key exact comparison，不使用 display normalization。指定存在的 key 选择对应 item，否则使用确定性的 sourceItems[0]；empty items 时 evidence/reference 为 null。viewModel.test.ts:110-133 与 page.test.tsx:293-314 证明 table 首项、detail 和 trace共享同一 object/fact key；未发现跨 fact 风险。

未单独执行 selected-key-missing fixture；当前 fallback 为单一 find(...) ?? sourceItems[0] ?? null，无额外分支，列为 recommendation 而非 blocker。

页面 non-ready branch 在 page.tsx:42-49 只渲染 state message；focused page tests 覆盖 loading、error、unavailable、invalid-query、empty、ready 及 ready→non-ready stale truth removal。API client tests覆盖 transport error、503、其他 5xx、malformed 2xx、no retry/no fallback；因此 accepted-events table、production summary、NOK/detail value、trace value 和上一 ready fact key不会进入非 ready页面。empty ready保留当前页 zero summary和当前 empty message，但不保留 evidence/reference production value。

## Synthetic/real evidence boundary

本轮仅执行本地 synthetic/focused implementation evidence：source review、Vitest、TypeScript typecheck、Next production build 和 Git/static audit。未执行：

~~~
real DB-backed Case A/B/C
PostgreSQL / API / Dashboard three-layer reconciliation
Raspberry Pi runtime
Docker / Compose / browser/server runtime
Gate B deployment
~~~

本报告不把 synthetic station_result、station_nok 或 cycle fixture解释为真实 accepted-fact closure；真实 Case A/B/C 和 Pi evidence仍属于后续独立 runtime gate。

## Fresh validation results

在 frontend/按用户授权命令各执行一次，全部 exit 0：

~~~
node -v
PASS: v22.23.0

node -e JSON.parse witness
PASS: {"value":9007199254740991,"source":"9007199254740991.1"}

focused npm test -- [8 named files]
PASS: 8 files, 167 tests

npm test
PASS: 11 files, 237 tests

npm run typecheck -- --incremental false
PASS: tsc --noEmit --incremental false

NEXT_TELEMETRY_DISABLED=1 npm run build
PASS: Next.js 16.2.10; /accepted-events is dynamic/server-rendered
~~~

## Allowlist compliance

live git diff --name-only -- frontend/src 精确为以下 15 个文件：

~~~
frontend/src/lib/acceptedStationEvents/schema.ts
frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts
frontend/src/lib/acceptedStationEvents/apiClient.ts
frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
frontend/src/lib/acceptedStationEvents/viewModel.ts
frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts
frontend/src/components/accepted-events/AcceptedEventsTable.tsx
frontend/src/components/accepted-events/__tests__/AcceptedEventsTable.test.tsx
frontend/src/components/accepted-events/NokDetailEvidencePanel.tsx
frontend/src/components/accepted-events/__tests__/NokDetailEvidencePanel.test.tsx
frontend/src/components/accepted-events/PageSummaryStrip.tsx
frontend/src/components/accepted-events/__tests__/PageSummaryStrip.test.tsx
frontend/src/components/accepted-events/TraceReferencePanel.tsx
frontend/src/components/accepted-events/__tests__/TraceReferencePanel.test.tsx
frontend/src/app/accepted-events/__tests__/page.test.tsx
~~~

只读审计结果：

~~~
git diff --check -- frontend/src       PASS
git diff --name-only -- frontend/src   exact 15 Gate A files
git diff --cached --name-only          empty
~~~

allowlist 外 frontend tracked diff 为 0；排除路径无 diff；.gitignore 为既有 external tracked modification。未发生 stage、commit、push、tag。

## Generated/external artifacts

本轮授权 build 后存在或刷新了 generated artifacts：

~~~
frontend/.next/
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
~~~

既有 external artifacts 包括 frontend/node_modules/、.gitignore、existing docs/thread_handoff/*.md、existing docs/reports/*.md and historical HTML/report artifacts。均未被手工修改、删除、清理、整理或 stage；本轮只新增本报告文件，保持 untracked 状态。

## Recommendations

1. 后续若需要提高 direct matrix 可读性，补充 -9007199254740992、numeric 1/-1 与 safe boundaries、page.limit=1/500、闰年 valid timestamp、outer/data/page missing-key、skip/not_applicable 直接 fixture，以及 explicit selected-key-missing fallback fixture。当前 generic helper、代表性 negative matrix 和 fresh validation 已足以避免本轮 blocker。
2. 保持 Node 22.23.0 context.source 为 runtime prerequisite；source context 缺失必须继续 fail closed，禁止 ordinary JSON fallback、parsed-number fallback 或 third-party lossless dependency。
3. 真实 DB-backed Case A/B/C、Pi runtime、三层 raw/display 对账和 Gate B 继续由 PM 单独授权，不得从本轮 synthetic/focused PASS 推导 closure。

## Next gate

~~~
Verification focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS
Gate A overall: NOT CLOSED
Next action: PM进行Gate A整体关闭与后续Git/action决策
Gate B / Docker / Compose / PostgreSQL / Raspberry Pi / runtime: not authorized
Git stage/commit/push/tag: not authorized
~~~

本轮完成后停止，不进入 Gate B、runtime 或 Git write。
