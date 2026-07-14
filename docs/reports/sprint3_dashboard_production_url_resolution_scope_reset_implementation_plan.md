# Sprint 3 Dashboard Production URL Resolution Scope Reset Implementation Plan

日期：2026-07-14

状态：COMPLETED / awaiting Git authorization

## Goal

将 Dashboard production URL-resolution gate 从强审计取证框架拉回到 local synthetic URL/request/response/runtime smoke，并验证现有前端实现。

## Global constraints

- 不修改 Collector、DB、API、schema、migration、V-PLC、Docker、Grafana、deployment 或 production config。
- runtime smoke 只使用 synthetic fixture，不连接真实 API/DB。
- 不按端口终止进程，只终止本轮记录的 PID。
- 不 stage、commit、push、tag 或 deploy，除非用户另行明确授权。
- 新 finding 只有可能导致 false PASS、stale truth、进程/端口污染、未知进程终止、越界文件删除或虚假 production claim 时才是 blocker。

## Task 1 — Freeze PM scope and governance

完成：

- 创建 `docs/reports/sprint3_dashboard_production_url_resolution_scope_reset_design.md`。
- 在 `docs/thread_handoff/pm_operating_rules.md` 增加 Section 12 evidence-gate scope control。
- 在旧 `docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_plan.md` 顶部增加 superseded banner，禁止执行 Section 14。

## Task 2 — Validate existing frontend implementation

验证文件：

- `frontend/src/lib/acceptedStationEvents/apiOrigin.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts`
- `frontend/src/lib/acceptedStationEvents/apiClient.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts`
- `frontend/src/app/accepted-events/page.tsx`
- `frontend/src/app/accepted-events/__tests__/page.test.tsx`

执行：

```bash
cd frontend
npm test -- --run \
  src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts \
  src/lib/acceptedStationEvents/__tests__/apiClient.test.ts \
  src/app/accepted-events/__tests__/page.test.tsx
npm run typecheck
EDGE_MES_DASHBOARD_API_ORIGIN=http://127.0.0.1:3100 \
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=local \
npm run build
```

完成结果：resolver/client/page tests PASS，typecheck PASS，build PASS。

## Task 3 — Minimal local synthetic runtime smoke

固定拓扑：

```text
capture: 127.0.0.1:3100
Next: 127.0.0.1:3101
profile: local
origin: http://127.0.0.1:3100
```

步骤：

1. 预检端口；未知 listener 立即 HOLD，不终止它。
2. 使用 `mktemp -d /tmp/edge-mes-dashboard-url-smoke.XXXXXX` 创建私有临时目录。
3. 使用 Node standard library 启动 synthetic capture server，记录 PID。
4. 使用构建后的 `.next/standalone/server.js` 启动 Next，记录 PID。
5. 请求 accepted-events 页面一次。
6. 验证恰好一个 `GET`、精确 host/path、五个冻结 query key/value。
7. 验证 synthetic 22-key fixture 的业务 marker 出现在 HTML。
8. 验证 Next runtime log 不含 rendering error。
9. 仅对记录的两个 PID 发送 TERM，并等待结束。
10. 验证端口 3100/3101 均释放。
11. 仅清理本轮创建且当前 UID 所有、非 symlink 的 `.next`、`next-env.d.ts`、`tsconfig.tsbuildinfo`。

## Task 4 — Runtime defect repair

第一次 runtime smoke 发现：

```text
Event handlers cannot be passed to Client Component props.
```

根因：`AcceptedEventsTable` 是 Server Component，却无条件创建未被页面使用的 `onClick` handler。

TDD 修复：

1. 在 `AcceptedEventsTable.test.tsx` 增加只读站点不得是 button 的断言；确认 RED。
2. 删除 `AcceptedEventsTable` 的 `onSelect` prop 和 `onClick`。
3. 站点列改为普通只读文本。
4. 确认 GREEN，并重新运行全部 focused tests、typecheck、build、runtime smoke。

完成结果：focused tests 92 passed；runtime smoke PASS；Next runtime log PASS。

## Task 5 — Durable reporting and status sync

完成：

- 创建 `docs/reports/sprint3_dashboard_production_url_resolution_scope_reset_execution_report.md`。
- 更新 `docs/current_status.md`。
- 完成 exact diff、whitespace、generated paths、ports、temporary roots 和 cached diff 审计。

## Stop condition

当前停止在 Git write 前：

```text
stage: not authorized / not performed
commit: not authorized / not performed
push: not authorized / not performed
```

下一步仅允许 exact allowlist review，以及用户明确授权后的 exact-path stage/commit/push。
