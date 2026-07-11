# Sprint 3 Dashboard accepted-events item required-key/null contract repair report

Date: 2026-07-10

报告名称：
Sprint 3 Dashboard accepted-events item required-key/null contract repair report

任务名称：
Clarify accepted-station-events item required keys and missing-versus-null semantics

执行 Thread：
Architecture / Integration

风险等级：
Level 2 — docs-only contract repair

结论：PASS

## Baseline

- HEAD: `885a09423997f9dfc3ad597607509fb37372717e`
- origin/main: `885a09423997f9dfc3ad597607509fb37372717e`
- cached diff: empty
- dirty-state assessment: recovery 时 working tree 仅包含本轮可修改的
  `docs/contracts/dashboard_api_contract.md`、此前已授权的两份 untracked planning/
  clarification report，以及 PM 列出的 external dirty exclusions；无 staged file，未发现
  超出授权范围的 dirty artifact。

## Reviewed files

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260710-1659.md`
- `docs/current_status.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md`
- `docs/reports/sprint3_dashboard_accepted_events_envelope_contract_clarification_report.md`
- `frontend/src/lib/acceptedStationEvents/schema.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts`
- `api/app/routes/accepted_station_events.py`

## Changed files

- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_accepted_events_item_required_key_contract_repair_report.md`

## Explicitly not touched

- `docs/reports/sprint3_dashboard_strict_parser_fail_closed_plan.md`
- `docs/reports/sprint3_dashboard_accepted_events_envelope_contract_clarification_report.md`
- `docs/current_status.md`, `docs/thread_handoff/**`
- `frontend/**`, `api/**`, `common/**`, `collector/**`, `tests/**`
- `package*.json`, `docker*`, `.gitignore` 和所有 external dirty exclusions

## Verification blocker

- B1 original finding: item DTO 的 required/optional 与 missing/explicit-null 语义未冻结，
  因而 Verification 不能确认 parser 是否可将 missing key 误归一为 `null`。
- repair decision: PM 选择 A；Response DTO allowlist 的全部 22 个 item key 均 required，
  但 required key presence != non-null value；nullable 值使用显式 JSON `null`。
- blocker status: CLOSED by this docs-only contract repair; parser implementation is not
  performed or claimed by this report.

## Contract repair

- required item key rule: `data.items[]` item 必须是 JSON object，exact own JSON key 集合
  必须与 Response DTO allowlist 的全部 22 个字段完全相等。
- required versus nullable: required 只要求 key presence；不重设计 nullable matrix，允许为
  空的业务值仍以完整 key 和 explicit JSON `null` 返回。
- missing versus explicit null: missing 不等于 explicit `null`；不得用省略 key 表示
  empty、unknown 或 not applicable。
- malformed response classification: 缺失任意 required item key 的 2xx response 为
  malformed successful response；consumer parser 必须 fail closed，Dashboard client 为
  `kind: "error"`，不得映射为空 `items`、`invalid-query` 或 `unavailable`。
- unknown key behavior: allowlist 外 item key unsupported；unknown 或 missing 都使整个
  response 失败，不得返回 partial item/envelope，也不得 salvage unsupported container 中的
  accepted-looking field。
- source/fallback prohibition: missing field 不得由 `?? null`、默认值、compatibility
  mapping 或 normalization 合法化，也不得由其他 table、endpoint、cache、diagnostic、
  legacy、raw 或 current source 补齐。

## Compatibility assessment

- current API route: compatible；`_format_row()` 通过 `{field: row.get(field) for field in
  DTO_FIELDS}` 建立完整 22-key item，nullable DB/Python `None` 以完整 key + JSON `null`
  表示。
- API change required: no；不需要 producer、query、cursor、pagination 或 status 修改。
- frontend implementation performed: no；未修改或执行 frontend parser/API client/tests。
- DTO authority changed: no；DTO 字段列表、production authority、NOK/detail、config lineage、
  identity 与 `accepted_at` 语义均未改变。
- production semantics changed: no。

## Exact diff assessment

本轮修改/创建严格限于两个 allowlist 文件。前序 strict-parser plan、envelope clarification
report、status/handoff 文档及所有 frontend/API/runtime/DB/test surface 均未触及；未 stage。

## Validation performed

- 按 PM 指定顺序完成 read-only Git recovery；HEAD/origin/main 与期望 `885a094` 一致，
  cached diff 为空。
- 仅运行 docs/read-only validation：`git diff --check`、contract diff、changed-name audit、
  cached-name audit、full status audit、untracked repair report direct read，以及 targeted
  `rg` contract assertions。
- 未运行 frontend tests、API pytest、typecheck、build、browser/manual smoke、server/runtime、
  DB/Postgres 或 Docker。

## Blockers

None within this exact docs-only repair allowlist.

## Recommendations

- 后续 Data Quality 与 Verification 必须各自执行 targeted contract re-review；本报告不替代
  re-review。
- Reliability 既有 review 原则继续有效，因为本修复未改变 error classification、fallback、
  request count 或 API availability 语义；若后续审计发现超出该边界，必须先报告 `HOLD`。

## Next gate

1. Data Quality targeted contract re-review；
2. Verification targeted blocker re-review；
3. 两者无 blocker 后，由 PM 重新评估 Level 1 三文件 parser implementation gate。

本轮完成 repair report 后停止；未授权 frontend/API implementation、tests、status sync、
stage、commit 或 push。

## Thread 输出 / 上下文评估

- 本次输出长度：中
- 当前 Thread 是否建议继续：no
- 下一轮是否建议新开 Thread：yes
- 理由：本轮仅关闭 Verification 的合同语义 blocker；后续为独立的 Data Quality 和
  Verification targeted re-review，之后才可能由 PM 重新评估 implementation authorization。
