# Sprint 3 Dashboard production URL-resolution Reliability planning review report

报告名称：Sprint 3 Dashboard production URL-resolution Reliability planning review report

任务名称：Review the Dashboard production URL-resolution plan for configuration failure, runtime recovery, deterministic behavior and fail-closed reliability

执行 Thread：Reliability

风险等级：Level 1 review-only；被审查的 future implementation 为 Level 2。

结论：**HOLD**

本报告是只读 Reliability planning review。除本报告外没有修改任何文件；没有运行 tests、typecheck、build、runtime probe、server、browser、API、DB/Postgres、Docker 或 dependency install，且未 stage、commit 或 push。

## 1. Baseline and recovery

| Item | Evidence |
| --- | --- |
| Branch | `main...origin/main` |
| HEAD | `53ade97ed310078d9d52b4e812c72a18392e1e61` |
| origin/main | `53ade97ed310078d9d52b4e812c72a18392e1e61` |
| Latest commit | `53ade97 Freeze Dashboard production URL resolution planning` |
| Cached diff | empty |
| Tracked diff before this report | `.gitignore` only |
| Review target before this report | absent |

已确认既有 external dirty artifacts 为 `.gitignore`、列明的旧 PM handoff、Keynote HTML、DB-backed review 以及 `frontend/node_modules/`；它们均未被修改、stage 或纳入本次 allowlist。

## 2. Reviewed authority and source

按要求只读审计了 PM rules、`chatgpt_pm_handoff_260711-1802.md`、`docs/current_status.md`、Dashboard contract、vertical-validation、stale-data、typecheck/build、browser smoke、same-origin mock-capability 和以下 planning authority：

```text
docs/reports/sprint3_dashboard_production_url_resolution_plan.md
```

也只读审计了指定 `frontend/` package/config/page/loading/error/tests、accepted-events client/query/schema/view-model、`docker-compose.yml`、`.env.example` 与 `README.md`，以及 `fetchAcceptedStationEvents`、`process.env`、error-state、fetch options、standalone/runtime/topology 和现有 test mock/reset 模式。

## 3. Review scope

本 review 只判断 planning authority 是否足以支持可靠实施；不重新设计 URL resolver，不改变 Dashboard/API contract、现有错误分类、mock-capability HOLD 或 browser/manual smoke 的已关闭状态。

## 4. Reliability summary

计划已明确：两项 server-only runtime config、无默认/relative/header/mock fallback、valid query 后才 resolve、configuration failure 为 `kind: "error"` 且零 outbound request、absolute URL + `GET` + `cache: "no-store"` + `credentials: "omit"` + `redirect: "error"`。这些设计本身与当前 query、strict parser、stale-data 清除和 API failure classification 相容。

不过，当前 authority 尚不能让实现者在不临场裁决的情况下完成 deterministic profile matching，也没有把“修复环境变量后重启进程恢复”的完整证据纳入 runtime acceptance。因此不得进入 implementation。

## 5. Configuration availability

**Closed by plan。** Plan sections 7、10、13、15 明确两个变量都必须存在；missing、empty、unknown profile、malformed 或 profile mismatch 都在 fetch 前成为 configuration `error`。没有 relative URL、localhost、`api:8000`、browser host、header 或 mock fallback。当前 `page.tsx` 已先做 query validation，未来 resolver 插入点也被指定在 validation 之后。

所需 invariant：

```text
configuration invalid
-> no fetch
-> visible error
-> no stale production truth
```

与现有 `AcceptedEventsPageView` 的 non-ready branch 和 stale-data tests 相容。

## 6. Configuration snapshot and read timing

计划 section 9 规定 resolver request-time read，section 10 禁止 module-import/build snapshot，且 API client 不应理解环境变量。这足以排除 build-time inline 和 client-side read。

但未明确冻结一次 invocation 内的 single immutable local snapshot：实现必须先读取两项 env 到 local values，再只基于这一对值完成所有 validation/canonicalization；不得在不同 validation 阶段重新读取 `process.env`，API client 也不得再次读取。这是 `REL-URL-R3` carry-forward requirement。

## 7. Failure containment

**Closed by plan。** Plan section 9 要求 resolver 返回 classified configuration failure，section 13 要求 page 将其转为 existing `kind: "error"` 而不调用 client；section 14 禁止将 configuration failure 误标为 `empty`、`invalid-query` 或 `unavailable`。这避免依赖 `error.tsx` 作为正常 configuration control flow，并保证不形成 partial view model、retry、secondary target 或重复 accepted-events request。

## 8. Error classification

**Closed by plan。** Current `apiClient.ts` 的 4xx -> `invalid-query`、503 -> `unavailable`、其余 HTTP/network/parser -> `error` 已被 plan section 6、13、18 明确保留。configuration failure 是独立原因但仍归入 `error`；connection refusal、DNS/TLS failure、redirect rejection 和 strict-parser malformed 2xx 都不应被误标为 configuration failure。`redirect: "error"` 使 redirect 走 generic `error`，`credentials: "omit"` 不改变现有 query/parser authority。

## 9. Runtime recovery

Plan sections 10 和 15 正确区分 request-time read 与 hot reload：允许 process restart 后读入新 server environment，不承诺运行中的环境变量热更新，也不要求 rebuild。

但 section 19 仅要求 standalone reads env at runtime；没有要求一次可复核的 recovery sequence：invalid/missing config fail closed -> operator corrects runtime env -> restart same build artifact -> subsequent valid request resolves/fetches once。该缺口是 `REL-URL-R2` blocker。

## 10. Profile reliability

local、container、production 的安全方向已冻结：local 仅 loopback；container 仅 `http://api:8000` 且不作为 host fallback；production 仅 HTTPS、non-loopback FQDN、default 443、无 IP literal/single-label/localhost，并且没有 profile failover。

但 profile matching 在 canonicalization 边界尚未完整冻结，详见 `REL-URL-R1`。在该项修复前，不能断言不同输入的 profile acceptance 是确定且可重复的。

## 11. Canonicalization determinism

Plan section 10 仅冻结 trailing slash normalization，并拒绝 surrounding whitespace、ASCII controls、non-root/encoded path；section 11 要求使用 platform `URL`。仍未逐项定义 scheme/hostname case、trailing dot（特别是 `localhost.`）、explicit default port、IPv6 bracket/default form、percent-encoded authority/path、Unicode/IDN/punycode、duplicate separators、empty hostname、port overflow 和 `URL` parser normalization 后的 profile comparison/brand value。

平台 `URL` 可作为 parser，但不能替代 policy：planning authority 必须冻结“canonicalize 后比较还是 raw-input 精确比较”、每一种歧义形式的 accept/reject 结果，以及 brand 保存的唯一 root-origin serialization。否则实现、test 和 Node runtime version 之间仍可能各自做不同判断。

## 12. Observability and log behavior

**Sensitive-data redaction is closed by plan。** Plan section 14 限定 `DASHBOARD_API_ORIGIN_CONFIGURATION_ERROR`，只允许 profile/error category/variable names，并禁止 raw origin、hostname、URL、query、credentials、headers 和 body。

未冻结 repeated invalid requests 的 bounded logging 行为，也未要求 logging failure 不影响 error rendering。现有仓库未见 logging abstraction；在 exact allowlist 内由 `apiOrigin.ts` 用无 dependency 的最小 safe `console.error` 可以实现，不需要 package/logger file，但必须保证不会 log raw value 且 logging wrapper 不向 React tree throw。这是 `REL-URL-R4` carry-forward requirement。

## 13. Build/standalone reliability

`frontend/next.config.ts` 当前使用 `output: "standalone"`；plan sections 10、19、20 正确要求 build 不需要 origin、origin 不进入 client bundle、standalone request-time read 要由 future evidence 验证而非假设。Build/startup 不因配置缺失直接失败、无 query 的 page path 不必 resolve，均与 request-level fail-closed 一致。

这会使 process-level readiness 不能自动代表 accepted-events ready。deployment health/readiness endpoint 属于 future deployment gate，不应暗中加入当前 six-file source scope；作为 `REL-URL-R6` recommendation 记录。

## 14. Exact implementation scope assessment

六文件 allowlist 足以实现 resolver、brand、typed failure、page no-fetch integration、absolute URL composition、existing classification preservation、focused unit/page tests 及无 dependency 的 minimal logging：

```text
frontend/src/lib/acceptedStationEvents/apiOrigin.ts
frontend/src/lib/acceptedStationEvents/apiClient.ts
frontend/src/app/accepted-events/page.tsx
frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
frontend/src/app/accepted-events/__tests__/page.test.tsx
```

本 review 未发现必须修改 `package.json`、lockfile、Next/TS config、`.env.example`、Compose、README、schema/query/viewModel、loading/error component 或新增 logger/config utility 的 source blocker。R1/R2 是 planning/test-acceptance authority 缺口，不是扩大 source allowlist 的理由。

## 15. Test and runtime evidence assessment

Plan section 18 已覆盖 valid profiles、many invalid inputs、request-time reread、absolute fixed endpoint/five query keys/fetch options、no fetch/error/no stale surfaces 和 classification regressions。它应补足以下可执行 assertions：

- resolver test 对每个 profile 使用 saved exact env values、`afterEach` precise restore、无开发机 env default、避免 concurrent shared-env mutation；
- single invocation snapshot test：在 resolver 中不得有 second `process.env` read，并验证 branded value/validation 来自同一 local pair；
- canonicalization matrix：R1 指定的所有 ambiguous forms 有固定 accept/reject 与 canonical root assertion；
- page test：invalid query precedes resolver；valid query + resolver failure returns `error` and calls no fetch; resolver failure does not reach error boundary；
- log test：仅安全 code/category/variable name，无 raw config，且 log failure does not alter returned configuration failure。

未来 runtime acceptance 必须补入 R2 的 same-artifact restart recovery；现有 missing/invalid/loopback/build/client-bundle checks 不能单独证明它。

## 16. Findings

### REL-URL-R1

ID: `REL-URL-R1`

Severity: `BLOCKER`

Status: `OPEN`

Area: `Profile`

Finding: Profile policy 的安全方向明确，但 canonicalization/profile matching 没有完整、唯一、可测试的 accept/reject contract；implementation 会被迫决定 case、trailing dot、explicit default port、IPv6、IDN/percent encoding 和 parser-normalized values 如何比较及如何存入 brand。

Evidence: Plan sections 7、10、11 只明确 profile forms、trailing slash 和部分 forbidden components；section 18 也没有 deterministic canonicalization matrix。

Required resolution: `Architecture planning repair` 必须为三个 profile 冻结 parser order、raw precheck、canonical comparison fields、canonical root serialization、每种列明 ambiguity 的 accept/reject matrix，且把对应 resolver tests 写入 section 18。

Gate impact: `HOLD`

### REL-URL-R2

ID: `REL-URL-R2`

Severity: `BLOCKER`

Status: `OPEN`

Area: `Recovery / Runtime`

Finding: “request-time read; restart process; no rebuild” 是设计意图，但 runtime acceptance 未要求证明从 invalid/missing env fail-closed 到修复 env 后 restart 的恢复闭环，也未明确 same artifact/module cache 不保留旧 configuration。

Evidence: Plan sections 10、15 声明 restart contract；section 19 只列 standalone runtime read/no client leakage，未列 restart recovery probe 或 required evidence。

Required resolution: `Architecture planning repair` 必须增加独立授权的 runtime acceptance：同一 build artifact 先以 invalid/missing pair 请求并证明 zero fetch/error，停止 process；注入 valid pair 后 restart；证明 subsequent valid request exactly once uses the corrected absolute origin。该证据不得声称 hot reload。

Gate impact: `HOLD`

### REL-URL-R3

ID: `REL-URL-R3`

Severity: `RECOMMENDATION`

Status: `CARRY FORWARD`

Area: `Configuration`

Finding: Request-time read 已冻结，但 single immutable env-pair snapshot 尚未逐字冻结。

Evidence: Plan section 9 说 resolver reads both variables when called；section 10 没有禁止 invocation 内 repeated reads。

Required resolution: 在 planning repair/implementation acceptance 中要求 resolver invocation 开头读取两值到 immutable local snapshot，所有 validation 与 brand 从该 snapshot 得出，API client 不读 env，并给出 deterministic test。

Gate impact: `PASS WITH RECOMMENDATIONS` after blockers close.

### REL-URL-R4

ID: `REL-URL-R4`

Severity: `RECOMMENDATION`

Status: `CARRY FORWARD`

Area: `Observability`

Finding: Safe logging fields 已定义，但 configuration error 在每个 request 重复记录时可能无界；logging containment 也未明确。

Evidence: Plan section 14 specifies event/redaction only, not rate/dedup policy or non-throw logging behavior。

Required resolution: 在 six-file scope 内冻结 minimum bounded policy（例如 process-local bounded dedupe/rate window，或明确由 deployment log-rate limit 承担并记录）和 `console.error` failure isolation；不得新增 dependency/logger utility。

Gate impact: `PASS WITH RECOMMENDATIONS` after blockers close.

### REL-URL-R5

ID: `REL-URL-R5`

Severity: `RECOMMENDATION`

Status: `CARRY FORWARD`

Area: `Tests`

Finding: Future tests 会改 `process.env`，但 plan 没有明确 exact restore/isolation rule。

Evidence: Plan section 18 includes request-time reread but does not require saved-value restore, serial handling or no-host-env default；当前 page tests 仅 reset `fetchAcceptedStationEvents` mock。

Required resolution: 每个 env-mutating test 保存 property presence/value、`afterEach` exact restore，serialise shared-env cases 或避免 parallel mutation，module cache 不得冻结 env，且 invalid-config tests 不得污染 ready-flow tests。

Gate impact: `PASS WITH RECOMMENDATIONS` after blockers close.

### REL-URL-R6

ID: `REL-URL-R6`

Severity: `RECOMMENDATION`

Status: `CARRY FORWARD`

Area: `Runtime`

Finding: Request-level fail-closed means server startup/readiness can succeed even though valid accepted-events queries will error when config is absent.

Evidence: Plan sections 10 and 19 choose request-level failure and no startup validation/health gate。

Required resolution: Future deployment gate decides explicit accepted-events readiness/alerting semantics; do not add endpoint/config/doc changes to this URL implementation allowlist。

Gate impact: `PASS WITH RECOMMENDATIONS` after blockers close.

### REL-URL-R7

ID: `REL-URL-R7`

Severity: `NOTE`

Status: `CLOSED BY PLAN`

Area: `Failure isolation`

Finding: No retry, timeout, circuit breaker or fallback is added by this bounded repair。

Evidence: Plan sections 5、6、11、13 fix one absolute fetch, `cache: "no-store"`, `redirect: "error"` and no fallback；current client maps thrown transport failures to `error`。

Required resolution: No current expansion. A future upstream-timeout policy may be separately planned if operational evidence shows unacceptable hangs; it is not a URL-resolution source blocker。

Gate impact: `PASS WITH RECOMMENDATIONS` after blockers close.

## 17. Blocking findings

```text
REL-URL-R1
REL-URL-R2
```

## 18. Carry-forward recommendations

```text
REL-URL-R3
REL-URL-R4
REL-URL-R5
REL-URL-R6
REL-URL-R7 (closed-by-plan note; no source expansion)
```

## 19. PASS conditions

本 review 的 future PASS 条件为：R1 的 canonicalization/profile matrix 和 R2 的 restart recovery runtime acceptance 写入 planning authority；implementation 保留 six-file allowlist；R3-R6 作为明确 acceptance requirements；并且后续授权的 implementation/test/runtime evidence 无 package/config/deployment expansion、无 raw env/header/relative fallback、无 client leak、无 unexpected fetch、无 classification/stale-data regression。

## 20. HOLD conditions

在 R1/R2 未修复前本 gate 维持 HOLD。后续仍须 HOLD 的条件包括：missing/invalid config 发出 request；profile implicit failover；resolver throw 交给 generic error boundary；invalid query 被 configuration error 覆盖；需新增 dependency/logger/config/package/deployment file；或 runtime evidence 与 request-time/restart contract 冲突。

## 21. Required next action

下一步只能在 PM 明确授权后由 Architecture / Integration 进行 planning authority repair，且只修复 `REL-URL-R1`、`REL-URL-R2` 及 carry-forward acceptance wording。修复后应重新发起本 Reliability review；不得直接 implementation、tests、build、runtime validation、mock-capability resume、stage、commit 或 push。

## 22. Thread output / context assessment

- 本次输出长度：long durable review report；window report 应保持简洁。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：结论为 HOLD，planning authority repair 与后续 re-review 必须是新的 PM-authorized gate，不能继承本次 review-only 写入权限。
