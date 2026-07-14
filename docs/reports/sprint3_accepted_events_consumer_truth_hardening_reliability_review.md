# Sprint 3 Accepted-events Consumer Truth Hardening Reliability Review

报告名称：Sprint 3 Accepted-events Consumer Truth Hardening Reliability Review

任务名称：Gate A — Accepted-events Consumer Truth Hardening Focused Reliability Review

执行 Thread：Reliability

日期：2026-07-14

## Conclusion

**PASS WITH RECOMMENDATIONS**

本轮 Reliability focused implementation review 已关闭，无 Reliability blocker。
结论只关闭本轮 Reliability focused implementation review，不宣布 Gate A 整体关闭，
不授权 Gate B、Docker、Compose、PostgreSQL、Raspberry Pi、runtime 或 Git write。

## Created/changed files

本轮只创建：

```text
docs/reports/sprint3_accepted_events_consumer_truth_hardening_reliability_review.md
```

未修改任何 source、test、planning report、status 或 governance 文件。15 个实现文件
仅作为既有 implementation diff 被审查，未在本轮 repair。

审查的 15 个 Gate A implementation files：

```text
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
```

## Recovery baseline

只读 recovery 结果：

```text
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: bdda24fd930339b565d0c1894daece42c6039ac7
origin/main: bdda24fd930339b565d0c1894daece42c6039ac7
ahead/behind: 0/0
latest: bdda24f Reset Dashboard URL validation scope
cached diff: empty
tracked frontend source diff: exact 15 Gate A files
allowlist-outside frontend tracked diff: empty
```

只读确认以下排除路径均无 status entry：

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

## Reliability blockers

**None。**

未发现 process crash、未捕获 parser exception、partial/stale production truth、第二次
request、retry/fallback/request storm、raw/origin/DB/parser 信息泄漏、合法 null/empty
导致的 renderer crash、source-preserving false PASS 或 15-file allowlist 越界。

## Node/source-context assessment

**PASS。** 当前 fresh runtime 为 `Node v22.23.0`。授权的 source witness 输出为：

```text
{"value":9007199254740991,"source":"9007199254740991.1"}
```

这证明 parsed number 已出现舍入，而 `context.source` 仍保留原始 numeric token。当前
`schema.ts:271-284` 只对 `cycle_counter`、`nok_code`、`nok_detail_code` 与 `limit`
执行 source gate：必须存在 `context.source`、通过 canonical integer regex，并在
`BigInt(source)` 后落入 safe-integer range；之后 `schema.ts:122-132,302-303` 仍执行
typed/safe-integer/`1..500` 验证。

source context 缺失时，`schema.ts:315-323` 将 parser failure 收敛为稳定错误；没有
普通 `JSON.parse` 兼容 fallback、parsed-number fallback 或第三方 lossless JSON dependency。
`apiClient.ts:41-49` 捕获 parser/body/transport failure，因此不会把异常逃逸到 Next
process，也不会形成后续 request loop。nullable numeric 的显式 `null` 在 source gate
中不要求 source，之后由 typed parser 保持 null。

future BIGINT serialization 不属于本 Gate；超出当前 safe-integer contract 的值继续
fail closed，不构成 blocker。

## Request/retry/fallback assessment

**PASS。** `apiClient.ts:21-29` 每次调用只构造一个 trusted absolute endpoint 并发出
一次 `GET`，保持 `cache: "no-store"`、`credentials: "omit"` 与 `redirect: "error"`。
成功 2xx 在 `apiClient.ts:41-45` 只调用一次 `response.text()`，再调用 raw-text parser；
没有 `response.json()`、relative URL、localhost fallback、origin switch 或第二次 body
读取。

HTTP 终局保持确定性：4xx 为 `invalid-query`，503 为 `unavailable`，其他 5xx 为
`error`；4xx/5xx 不读取 body、不 retry、不 fallback。empty body、invalid JSON、malformed
2xx、source-context 缺失、`response.text()` 抛错和 transport exception 均只进入当前
request 的稳定 `error` 终局。focused `apiClient.test.ts` 证明每个路径单 request，且
没有 retry/fallback。

## Failure containment/no-stale assessment

**PASS。** `schema.ts:287-312` 先验证 exact envelope/data/page、`page.limit`，再通过
`items.map(parseItem)` 逐项验证；任一 item 非法、任一 cross-field 组合非法或
`page.limit` 非法都会抛出并由 raw-text parser/client 收敛为整响应失败，不跳过 bad row、
不返回 partial items，也不继续使用前面已经解析的合法 row。

`schema.ts:196-236` 覆盖 `station_result`、`station_nok`、cycle event 的 result/NOK/detail
矩阵；`viewModel.ts:206-236` 从同一个 typed source item 派生 table、summary、detail
与 trace，`byResult` 只统计 `station_result`。合法 null/empty 由
`viewModel.ts:85-117` 转为显式 display rule，不会抛错或伪造 production result。

未修改的 `frontend/src/app/accepted-events/page.tsx:42-68,90-103` 对非-ready state 只
渲染 state message；error、unavailable、invalid-query 不渲染 table、旧 summary、旧
NOK/detail 或旧 trace。empty response 生成当前 page 的零计数 summary，并令 selected
evidence/reference 为 null。页面是 server-rendered request model，没有跨请求 response
cache、client-stored stale truth 或同一 render 内 retry。page focused tests 覆盖 loading、
error、unavailable、invalid-query、empty 与 stale-surface removal。

现有 query boundary 仍由未修改的 `query.ts:29-31,36-45` 限定 `limit` 为 `1..500`，
client 没有新增绕过 bounded API query 的路径。

## Error leakage assessment

**PASS。** raw-text parser 的内部异常在 `schema.ts:315-323` 被统一为
`Invalid accepted events response`；用户可见的 2xx/body/parser failure 在
`apiClient.ts:45` 为 `Accepted events response was invalid.`，transport failure 在
`apiClient.ts:48` 为 `Accepted events request failed.`。这些路径不包含 raw response body、
numeric lexeme、trusted origin、完整 request URL、DB error、parser exception 或 stack trace。

4xx/5xx 只显示允许的 status classification；query validation messages 不携带 raw body、
origin 或诊断 payload。raw body 只存在于当前 parse call 的局部变量，不进入 view model；
`viewModel.ts` 只复制和派生 22-field typed item。测试同时断言 raw secret、numeric lexeme、
origin、parser detail 与 diagnostic surface 不出现在错误或 renderer。

未新增通用日志、debug surface 或 raw-data 取证功能。既有 origin configuration logger
不在本轮 diff，且只记录稳定 error code，不改变 user-visible safe result。

## Parser/resource stability assessment

**PASS。** production parser 使用原生 `JSON.parse` 一次、一次 `items.map` 和固定字段
allowlist；没有显式递归、无界 retry loop、重复 parse、raw body 多份长期复制、view-model
raw-body retention、request storm 或 log storm。`assertExactOwnKeys` 的循环只遍历固定
schema key set；unknown/nested leakage 在 exact-key parser 中 fail closed。

`page.limit` 仍由 raw numeric source gate、typed integer 与 `1..500` 共同限制；query
construction 也保持 `1..500`，没有绕过 accepted-events API 的既有 bounded query 边界。
资源侧未发现现实的 process crash、无限处理或明显无界长期内存保留路径。未来容量优化、
Pi capacity、Docker、真实 DB-backed evidence 与 BIGINT serialization 均不属于本 Gate。

## Validation results

所有授权命令均执行一次并通过，未重试：

```text
node -v
PASS: v22.23.0

node -e 'JSON.parse("{\"value\":9007199254740991.1}", ... context.source ...)'
PASS: {"value":9007199254740991,"source":"9007199254740991.1"}

focused npm test
PASS: 8 files, 167 tests

npm test
PASS: 11 files, 237 tests

npm run typecheck -- --incremental false
PASS

NEXT_TELEMETRY_DISABLED=1 npm run build
PASS: Next.js 16.2.10 production build; /accepted-events remains dynamic/server-rendered
```

## Allowlist compliance

**PASS。** 最终只读审计：

```text
git diff --check -- frontend/src       PASS
git diff --name-only -- frontend/src   exact 15 Gate A files
git diff --cached --name-only          empty
```

未发生 commit、push、tag 或其他 Git write。`.gitignore` 仍是既有 external tracked
modification，不在 Gate A 15-file implementation allowlist 内，也未被 stage。

## Generated/external artifacts

授权 validation 后存在或刷新了 generated artifacts：

```text
frontend/.next/
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
```

这些未被 stage；本轮没有手工编辑、删除、清理或整理它们。既有 external dirty artifacts
包括 `.gitignore`、`frontend/node_modules/`、多份 untracked handoff/report 文件及历史
报告；均保持原状并未纳入本轮报告 allowlist。最终 `git status --short --untracked-files=all`
中除本报告外的这些 entries 均按 external/generated artifact 处理。

## Recommendations

1. 后续 Gate 继续以 `Node v22.23.0` 的 `context.source` 能力作为 runtime prerequisite；
   source-context 缺失必须保持 error/fail-closed，不得引入 compatibility fallback。
2. 当前 safe-integer contract 与 raw/display separation 继续保持；若未来需要 BIGINT
   string serialization，应另开 API serialization/contract gate，不在本 Gate 扩大范围。
3. 15-file implementation 的 Architecture、Reliability、Data Quality、Verification
   focused review 必须继续保持独立；本报告的 PASS WITH RECOMMENDATIONS 不替代其他 review
   或 Gate A overall closure。

## Next gate

```text
Reliability focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS
Gate A overall: NOT CLOSED
Next eligible gate: PM安排 Data Quality focused implementation review
Gate B / Docker / Compose / PostgreSQL / Raspberry Pi / runtime: not authorized
Verification: not entered by this report
Git write: not authorized
```

本轮完成后停止。
