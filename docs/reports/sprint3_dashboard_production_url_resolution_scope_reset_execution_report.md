# Sprint 3 Dashboard Production URL Resolution Scope Reset Execution Report

报告名称：Sprint 3 Dashboard production URL resolution scope reset execution report

任务名称：Reset overgrown runtime-evidence assurance target, repair the real runtime rendering defect, and execute minimal local synthetic validation

执行 Thread：ChatGPT PM / Architecture & Integration implementation

结论：**PASS WITH RECOMMENDATIONS**

## 1. PM scope decision

Dashboard production URL-resolution gate 已从 private-parent / manifest / 57-field summary / 76-field failure relation 的强审计取证目标，重置为与当前产品声明相匹配的 local synthetic URL/request/response/runtime smoke。

当前 authority：

- `docs/reports/sprint3_dashboard_production_url_resolution_scope_reset_design.md`
- `docs/reports/sprint3_dashboard_production_url_resolution_scope_reset_implementation_plan.md`
- `docs/thread_handoff/pm_operating_rules.md` Section 12

旧 `docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_plan.md` 的 Section 14 已明确标记为 historical / superseded，不再可执行。

`DQ-RUNTIME-OPTIONC-D7` 与完整 `DQ-RUNTIME-OPTIONC-D8` relation matrix 不再是本轮 blocker。只有会造成 false PASS、stale/invalid truth、进程/端口污染、未知进程终止、越界文件删除或虚假 production claim 的 finding 才能阻断本 gate。

## 2. Scope

### Frontend implementation reviewed and validated

- `frontend/src/lib/acceptedStationEvents/apiOrigin.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts`
- `frontend/src/lib/acceptedStationEvents/apiClient.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts`
- `frontend/src/app/accepted-events/page.tsx`
- `frontend/src/app/accepted-events/__tests__/page.test.tsx`

### Runtime defect repair

- `frontend/src/components/accepted-events/AcceptedEventsTable.tsx`
- `frontend/src/components/accepted-events/__tests__/AcceptedEventsTable.test.tsx`

### Governance and evidence docs

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_plan.md`
- `docs/reports/sprint3_dashboard_production_url_resolution_scope_reset_design.md`
- `docs/reports/sprint3_dashboard_production_url_resolution_scope_reset_implementation_plan.md`
- `docs/reports/sprint3_dashboard_production_url_resolution_scope_reset_execution_report.md`
- `docs/current_status.md`

### Explicitly not touched

Collector、API、DB、schema、migration、storage、V-PLC、Docker、Grafana、deployment、production config、real PLC、real API/DB connectivity、tag、rollback。

## 3. Real defect found by runtime smoke

第一次 smoke 的 transport/request/response 已经成功，但 Next runtime log 出现：

```text
Event handlers cannot be passed to Client Component props.
```

根因：`AcceptedEventsTable` 是 Server Component，却无条件创建 `onClick` handler。页面没有传入 `onSelect`，所以该按钮既没有真实交互能力，也导致 RSC runtime rendering error。单元测试和 production build 均未捕获该运行时边界问题。

修复：

- 先增加失败测试，要求只读站点单元不是 button；测试按预期失败。
- 删除未使用的 `onSelect` prop 和 `onClick` handler。
- 将站点显示改为普通只读文本。
- 不引入新的 Client Component，不扩大前端状态模型。

## 4. Focused validation evidence

### TDD regression

```text
AcceptedEventsTable RED:
1 failed — station WS01 was still rendered as button

AcceptedEventsTable GREEN:
1 passed
```

### Combined focused tests

```text
Test Files: 4 passed
Tests: 92 passed
```

覆盖：

- trusted API origin resolver：57 tests；
- accepted-events API client：14 tests；
- accepted-events page integration/state：20 tests；
- read-only accepted-events table：1 test。

### Full frontend regression suite

```text
Test Files: 11 passed
Tests: 277 passed
```

### TypeScript and production build

```text
npm run typecheck: PASS
npm run build: PASS
Next.js 16.2.10
/accepted-events: dynamic server-rendered route
```

## 5. Local synthetic runtime evidence

固定拓扑：

```text
capture: 127.0.0.1:3100
Next:    127.0.0.1:3101
profile: local
origin:  http://127.0.0.1:3100
```

Preflight：

```text
PREFLIGHT_PORT_3100=FREE
PREFLIGHT_PORT_3101=FREE
```

Page result：

```text
PAGE_HTTP_STATUS=200
DMC-RUNTIME-001 present
UNIT-RUNTIME-001 present
runtime-response-profile present
NEXT_RUNTIME_LOG=PASS
```

Capture result：

```text
REQUEST_COUNT=1
REQUEST_METHOD=GET
REQUEST_HOST=127.0.0.1:3100
REQUEST_URL=/api/v2/production/accepted-station-events?line_id=LINE_001&start_time=2026-07-05T00%3A00%3A00Z&end_time=2026-07-05T08%3A00%3A00Z&limit=50&cursor=opaque.cursor.value
RESPONSE_BYTES=714
```

Process and port cleanup：

```text
capture wait=0
Next wait=143 after owned-PID TERM
PORT_RELEASE_3100=PASS
PORT_RELEASE_3101=PASS
RUNTIME_SMOKE=PASS
TEMP_ROOT_REMOVED=PASS
```

Only the two recorded task-owned PIDs were terminated. No process was selected by port.

## 6. Generated artifact cleanup

Recovery confirmed these paths were absent before validation. They were created by typecheck/build, checked as current-UID non-symlink task outputs, then removed:

```text
frontend/.next
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo
```

Final state：

```text
ABSENT frontend/.next
ABSENT frontend/next-env.d.ts
ABSENT frontend/tsconfig.tsbuildinfo
ABSENT all three quarantine paths
FREE port 3100
FREE port 3101
```

## 7. Ten-criterion result

| Criterion | Result |
| --- | --- |
| query validation before resolver/request | PASS |
| canonical profile/origin resolution | PASS |
| branded absolute accepted-events GET | PASS |
| exact five query keys, no fallback/credentials/redirect | PASS |
| exactly one runtime target request | PASS |
| strict synthetic response visible in Dashboard | PASS |
| invalid config/response fail closed | PASS by focused tests |
| cleanup only recorded PIDs | PASS |
| final dual-port release and owned artifact cleanup | PASS |
| no production/DB/TLS claim | PASS |

## 8. Gate decision

```text
Dashboard production URL-resolution implementation: PASS WITH RECOMMENDATIONS
Focused tests/typecheck/build: PASS
Full frontend regression suite: PASS, 277 passed
Local synthetic runtime smoke: PASS
Old Option C D7/D8 strong-audit branch: SUPERSEDED / backlog only
Global product gate for this local synthetic branch: PASS WITH RECOMMENDATIONS
Git stage/commit/push: NOT AUTHORIZED / NOT PERFORMED
Production DNS/TLS/egress/API/DB evidence: NOT EXECUTED / NOT CLAIMED
```

## 9. Recommendations

- 可在未来将本轮 minimal smoke 固化为一个小型、独立、可维护的 test harness，但不得重新引入完整 76-field failure framework。
- `DQ-RUNTIME-OPTIONC-D7`、archive uniqueness 与更细 telemetry taxonomy 可保留为低优先级 backlog。
- 下一步应进行 exact allowlist review 与 Git commit planning，而不是继续扩展 runtime evidence assurance。

## 10. Ignored local scratch copies

The initial skill-format copies under `docs/superpowers/` are ignored by the existing `.gitignore` rule and are not project authority. Durable equivalents are the two `docs/reports/...scope_reset_*.md` files listed above. The ignored copies must not be force-staged.

## 11. Thread output / context assessment

- 本次输出长度：长。
- 当前 Thread 是否建议继续：yes，仅适合 PM intake、allowlist audit 和 exact Git gate。
- 下一轮是否建议新开 Thread：implementation/review 若继续扩大则 yes；简单 PM commit gate 可在当前 Thread 完成。
- 理由：目标漂移已纠正，真实 runtime defect 已修复并验证；后续不应重新打开旧 Option C 取证分支。
