# Sprint 3 Dashboard Raspberry Pi Docker Integration Data Quality Review

报告名称：`Sprint 3 Dashboard Raspberry Pi Docker Integration Data Quality Review`

任务名称：`Accepted-events Dashboard 树莓派 Docker 集成 Data Quality Planning Review`

执行 Thread：`Data Quality`

日期：`2026-07-14`

## 1. Conclusion

**HOLD**

本轮为 docs-only Data Quality planning review。唯一 accepted-fact source、DB/API
read boundary、`fact_key` identity、NOK/detail DB authority、opaque cursor 和
Dashboard 首项绑定方向正确；但当前 Architecture plan 与既有 frontend consumer
实现之间仍有三个不可绕过的数据质量缺口：

1. strict parser 只强制 exact key set，没有强制每个字段的类型、可空性和
   `cycle_counter` 精度；
2. view model 把 API 的 `null` / 空字符串静默改写成 `"unknown"` 或 `null`，并且
   没有在 consumer boundary 关闭 `event_type`、`production_result`、NOK/detail
   的交叉语义错误；
3. 真实验收矩阵没有明确区分 accepted `station_result` OK、accepted
   `station_result` NOK 与可选的 accepted `station_nok` detail case。

这些缺口会使逐字段三层对账或 NOK/outcome 验收出现 false PASS。当前不能进入
Verification、implementation 或 Raspberry Pi runtime。不得把本轮 planning review
或既有 synthetic/focused test 结果写成 real DB-backed closed-loop PASS。

## 2. Recovery baseline

本轮第一动作完成 read-only recovery：

```text
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: bdda24fd930339b565d0c1894daece42c6039ac7
origin/main: bdda24fd930339b565d0c1894daece42c6039ac7
ahead/behind: 0 0
latest: bdda24f Reset Dashboard URL validation scope
cached diff: empty
target report before this write: absent
```

工作树中存在既有外部 dirty artifacts，包括 `.gitignore`、多份 untracked handoff
与 reports、`frontend/node_modules/` 和 `frontend/tsconfig.tsbuildinfo`。本轮没有
修改、删除、整理、stage、commit、push 或纳入这些 artifacts。

本轮未运行 tests、typecheck、build、Docker、Compose、PostgreSQL、SSH、Raspberry Pi、
browser/server runtime、deployment 或 rollback。

## 3. Scope and evidence

已读取：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/current_status.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_plan.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_reliability_review.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_reliability_rereview.md`
- `docs/contracts/dashboard_api_contract.md`
- `db/migrations/007_accepted_station_event_visibility.sql`
- `collector/app/services/accepted_station_event_fact.py`
- `api/app/routes/accepted_station_events.py`
- `api/tests/test_accepted_station_events_api.py`
- `api/tests/test_accepted_station_events_api_db_backed.py`
- `frontend/src/lib/acceptedStationEvents/schema.ts`
- `frontend/src/lib/acceptedStationEvents/apiClient.ts`
- `frontend/src/lib/acceptedStationEvents/viewModel.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts`
- `frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts`
- `frontend/src/app/accepted-events/page.tsx`

为确认页面是否真的展示错误或跨 fact 值，静态读取了被 `page.tsx` 直接使用的
accepted-events renderer；没有对这些文件做任何修改。

本轮权限仍为 docs-only review。唯一允许创建的文件是本报告。

## 4. Data Quality blockers

### `DQ-DASH-D1`：strict parser 没有 field-level type/nullability closure

**精确位置：** Architecture plan Section 12.2、Section 18；
`frontend/src/lib/acceptedStationEvents/schema.ts:28,62-73`；
`frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts:62-69,233-235`。

`schema.ts` 将 22 个字段统一声明为 `string | number | null`，`parseItem()` 只检查
是否为 string、number 或 null，没有按 DB/API 合同检查：

- DB `NOT NULL` 字段不能为 `null`，包括 `line_id`、配置字段、`cycle_counter`、
  `source_event_id`、`event_ts`、`accepted_at`、`fact_key` 和
  `content_fingerprint`；
- `cycle_counter` 必须保持整数语义；当前 parser 接受字符串，后续
  `nullableNumber()` 还会把字符串重新解析为 number；
- `nok_code` 与 `nok_detail_code` 对应 DB `INTEGER`，不能接受任意字符串；
- `event_ts` / `accepted_at` 必须是 API 的 UTC ISO string，不能接受 number；
- 配置、identity、event type、result 等 string 字段不能接受 number。

现有 schema test 还显式把每一个 required key 的 `null` 都作为合法 parser 输入。
这与“required key presence != non-null value”被错误地扩大为“所有字段均可 null”。
因此 malformed 2xx 可以带有完整 22 keys，却携带 DB 不可能的 null 或错误类型，仍
进入 view model。对 `BIGINT` `cycle_counter`，当前没有 safe-integer 边界或精确保留
规则，存在超过 JavaScript safe integer 时精度丢失的路径。

这违反 Architecture plan 对“错误类型不得接受”、Dashboard API contract 的 DB
字段语义，以及本轮要求的“cycle_counter 不得模糊化或丢失精度”。它不是 Docker
运行问题，也不能由 Dockerfile、Compose 或 `/health` 绕过。

**最小 Architecture docs-only repair 建议：**

- 在 plan Section 12.2/18/19 冻结逐字段 type/nullability matrix，并明确只有 DB
  nullable 字段允许显式 JSON `null`；
- 明确 `cycle_counter` 的精确传输/显示策略；若 consumer 不能无损承载全部
  `BIGINT`，必须在 ready 前 fail closed，不能静默转 number；
- 后续实现前把 `frontend/src/lib/acceptedStationEvents/schema.ts` 及其 focused
  schema tests 纳入最小 repair allowlist；本轮不修改它们。

### `DQ-DASH-D2`：view model 丢失 API null/empty 语义并允许 outcome/detail 混淆

**精确位置：** Architecture plan Section 12.2、Section 12.3；
`frontend/src/lib/acceptedStationEvents/viewModel.ts:65-81,84-113,123-155`；
`frontend/src/app/accepted-events/page.tsx:60-67,90-101`。

当前 view model 有以下不可审计的改写：

- `stringOrUnknown()` 将 `null` 和空字符串都改为 `"unknown"`；
- `nullableString()` 将空字符串改为 `null`；
- `nullableNumber()` 将任意 numeric-looking string 转换为 number；
- `station_nok` 的 DB/API 合法语义是 `production_result: null`，但
  `buildEvidence()` 将它变为字符串 `"unknown"`，页面随后把它显示为
  `Production result`；
- parser/view model 没有关闭 `station_result` 必须有 non-null
  `production_result`、`station_nok` 必须为 null、其他 event type 必须为 null，
  以及 station-result NOK 必须同时具备 accepted `nok_code` / `nok_origin` 的
  交叉语义。

DB migration 的 CHECK constraint 与 Collector accepted decision guard 能保护
producer，但不能替代 Dashboard consumer 对 malformed 2xx 的 fail-closed 语义。
当前实现会让 API 原值无法逐字段回溯：空字符串被消失，显式 null 被替换为业务页
可见的 unknown sentinel，且 station_nok 的 detail row 在 production-result 显示
层没有保留 null/absent distinction。这会使三层对账把 display value 错当 API 原值，
也会使 NOK detail 被误读成第二个 production result。

**最小 Architecture docs-only repair 建议：**

- 在 plan Section 12.2/12.3/18 冻结 raw API value、human-readable display value
  和 display rule 的分离；任何 `null` / empty normalization 必须显式、可审计，
  不得使用未定义的 `"unknown"` 代替业务值；
- 冻结 event/result/NOK-detail cross-field validation 或等价的 fail-closed
  consumer invariant；
- 后续 implementation 至少需要审查并最小修改
  `frontend/src/lib/acceptedStationEvents/schema.ts`、`viewModel.ts` 及其对应
  focused tests；如选择在 renderer 侧表达 absent/null，也只能加入直接承载该
  display rule 的现有 renderer，不得新增 debug view 或业务功能。本轮不修改这些
  文件。

### `DQ-DASH-D3`：真实 OK/NOK/detail 验收矩阵不具备足够的语义区分

**精确位置：** Architecture plan Section 12.1-12.3，尤其是 Section 12.1 的
“一个真实 OK 与一个真实 NOK accepted fact”和 Section 12.2 的泛化“NOK case”。

当前文字没有强制未来真实 Pi evidence 同时覆盖：

1. 一个 accepted `station_result` OK case；
2. 一个 accepted `station_result` NOK case，且核对 `production_result=nok`、
   `nok_code` 与 `nok_origin`；
3. 如果真实数据存在，再单独覆盖一个 accepted `station_nok` detail case；如果
   不存在，必须写 `not available / not verified`，不得用 synthetic detail row
   代替 real evidence。

若用 `station_nok` row 作为“真实 NOK”，它的合法 `production_result` 是 null，
无法证明 `station_result` NOK outcome；若用 cycle event 作为 OK，也不能证明
`station_result` OK。当前矩阵因此允许错误的 case 选择后仍报告 OK/NOK 三层闭环。

**最小 Architecture docs-only repair 建议：** 只修订 plan Section 12.1-12.3，
冻结上述三种 case 的独立命名、逐字段核对和 real/synthetic evidence 标记；不修改
accepted-fact、API、DB、Dashboard 业务合同或 implementation allowlist。

## 5. Authority / lineage assessment

### Production fact source

静态 authority **通过**：

- migration 建立并约束唯一 `production_accepted_station_event_fact`；
- API `_read_rows()` 只从该表 SELECT `DTO_FIELDS`，没有 legacy/raw/diagnostic
  join 或 fallback；
- accepted fact builder 要求 `decision.disposition == "accepted"`，并拒绝缺失
  canonical `fact_key` / `content_fingerprint`；
- migration 排除 heartbeat/非允许 event type，且对 result/NOK/detail authority
  加 CHECK constraint；
- API 和 DB-backed tests 对 source isolation、22-key allowlist、forbidden surface、
  `fact_key` uniqueness、read-only query 与 no ACK/read_done mutation 有静态证据。

Docker/Compose 计划没有改变 accepted-fact writer、API endpoint 或 source authority。
`/health`、container healthy、API `/health` 和 Compose running 仍只能证明 service/
process 状态，不能证明存在 accepted production fact；Architecture plan 的这一点
表达正确。

### Configuration, identity and time lineage

- `line_id`、`plc_id`、`station_id`、`station_type`、`profile_id`、`config_hash`、
  `config_version` 在 migration comments、Collector fact builder 与 API DTO 中保持
  同名传递；没有页面当前选择、legacy table 或 current-config fallback。
- `fact_key` 是 DB unique identity；`source_event_id` 是来源 identity，不能替代
  `fact_key`；`content_fingerprint` 由 API 原样投影。
- API cursor 绑定 `line_id`、`start_time`、`end_time`、`limit`、direction 和
  `(event_ts, accepted_at, fact_key)` order；SQL 继续使用
  `event_ts ASC, accepted_at ASC, fact_key ASC`。
- API 将 `event_ts` 与 `accepted_at` 各自规范化为 UTC ISO string，未互换语义；
  页面分别标记 `Event time` 与 `Accepted fact timestamp`。

这些是 projection/transport lineage 的静态 PASS；它们不等于真实 Pi 上已经证明
历史 config authority 或真实 accepted row。未来 evidence 必须保存 DB 原始值与
API 原值，并将 `config_hash` / `config_version` 作为历史绑定字段核对，不得把当前
配置查询结果当成历史 row 的替代证据。

### Result and NOK/detail lineage

DB migration 与 Collector builder 对 `station_result`、`station_nok`、cycle events
和 accepted upstream detail 的 authority 方向正确；API 只读取已落表字段，不会从
raw、diagnostic 或 legacy source 补 NOK/detail。当前 blocker 在 Dashboard consumer
的 type/null/cross-field preservation，而不是 accepted-fact source authority 本身。

## 6. Three-layer reconciliation assessment

Architecture plan 的三层结构原则上可以唯一定位目标 row：

1. PostgreSQL 从 `production_accepted_station_event_fact` 按 `fact_key` 读取恰好一行；
2. API 使用同一 `line_id`、bounded time window 和 opaque cursor 返回同一 item；
3. 页面 `toAcceptedEventsViewModel()` 默认取 response 第一项，`page.tsx` 将第一项
   `factKey` 传给 table；当前 table 没有跨 row 的 interactive selection，detail/trace
   与该第一项保持同一 `fact_key`。

因此，“目标 fact 被安排为 API 第一项”足以支持**目标第一项**的 table/detail/trace
绑定，不需要新增通用 selection/debug 功能。但它不等于整页所有 row 都完成三层
closed-loop：计划和未来报告必须把声明范围限制为“每个独立 bounded request 的
目标第一项”，不能用第一项证据宣称整页所有 records 已闭环。

分页方向也正确：API 绑定 opaque cursor、稳定排序，view model summary 标记
`Current page only`，empty response 重新生成空 view model；page 的 invalid/error/
unavailable 分支不会继续渲染旧 rows、detail、summary 或 trace。未来 evidence 仍须
保存 page 1/page 2 的完整 query 参数，证明相同 `line_id`、`start_time`、`end_time`
和 `limit`，并逐页独立保存 `fact_key` 集合，不能只保存截图或行号。

本轮没有 DB row、API item 或 Dashboard runtime visible mapping，因此三层闭环结论为：

```text
planning design: HOLD on DQ-DASH-D1/D2/D3
real DB-backed Pi evidence: NOT EXECUTED / NOT CLAIMED
synthetic/focused tests: synthetic evidence only
```

## 7. Allowlist assessment

Docker/Compose integration 本身的六文件 allowlist仍然足够承载 process health、
standalone image、`http://api:8000` runtime env、port `3001`、Dashboard-only update
与 deployment guide；不需要加入 accepted-fact migration、Collector、API route、
API tests、Grafana 或 Dashboard 业务合同。

但对当前三个 Data Quality blocker，现有六文件 allowlist **不足以形成 truthful
implementation closure**：

```text
CREATE frontend/Dockerfile
CREATE frontend/.dockerignore
CREATE frontend/src/app/health/route.ts
CREATE frontend/src/app/health/__tests__/route.test.ts
MODIFY docker-compose.yml
MODIFY docs/deployment/raspberry_pi.md
```

进入 implementation 前，PM 需先完成 Architecture docs-only repair，并单独评估
最小额外路径；至少涉及：

```text
MODIFY frontend/src/lib/acceptedStationEvents/schema.ts
MODIFY frontend/src/lib/acceptedStationEvents/viewModel.ts
MODIFY frontend/src/lib/acceptedStationEvents/__tests__/schema.test.ts
MODIFY frontend/src/lib/acceptedStationEvents/__tests__/viewModel.test.ts
```

以上不是本轮授权，也不表示已授权修改；它们只反映 DQ-DASH-D1/D2 无法通过 Docker
或 Compose 文件绕过。若 Architecture 选择完全在既有 consumer contract 内修复，
应由 PM 重新冻结 exact allowlist 后再进入 implementation review。不得借本轮 HOLD
自行扩大 allowlist。

## 8. Carry-forward recommendations

- Architecture 修复后，重新确认 `production_accepted_station_fact` source、exact
  22-key、field-level type/nullability、raw-vs-display mapping 和 event/NOK cross-field
  invariants；不要把 key-set test 单独当作 schema closure。
- 未来 real report 必须同时保存 DB 原始 22 字段、API item 22 字段、Dashboard 可见
  字段映射、每字段显示规则、逐字段 PASS/FAIL，以及 `real DB-backed` / `synthetic`
  标记。
- 对 page 1/page 2 保存相同 scope 参数与 opaque cursor 的独立请求证据；目标第一项
  的 closed-loop 声明不得扩大为整页全部 row 的闭环声明。
- 若真实 `station_nok` detail 不存在，报告只能写 `not available / not verified`；
  不得把 synthetic fixture、mock server、API response-only、container health、
  Grafana 或 Collector logs 作为 real accepted-fact closure。
- 继续保持 `/health` 仅为 Dashboard process readiness；ARM64 build、restart、资源、
  rollback、端口和 Pi runtime 证据属于后续 Verification/runtime gate，本轮未执行。
- 当前 `apiClient.ts` 会把 caught `Error.message` 传给页面 state；后续 focused
  verification 应确认 transport/parser failure message 不回显 origin、DB error、
  raw payload 或 diagnostic context，但不为此新增 debug surface。

## 9. Next gate

```text
Current gate: Data Quality planning review = HOLD
Required next action: PM-authorized Architecture docs-only repair for DQ-DASH-D1/D2/D3
Then: independent Data Quality planning re-review
After DQ closes: PM-arranged Verification planning review
Implementation: not authorized
Raspberry Pi / Docker / Compose / PostgreSQL / browser runtime: not authorized
stage/commit/push/tag/deploy/rollback: not authorized
```

本轮完成后停止，不进入 Verification、implementation 或 runtime。

## 10. Created / changed files

```text
created:
  docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_review.md
changed existing files: none
cached diff: empty before report creation; final read-only check required after creation
```

## 11. Thread output / context assessment

- 本次输出长度：长。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：no。
- 理由：本轮 DQ planning review 已收敛为三个稳定 blocker；按 PM 指示继续使用既有
  `Data Quality` 角色即可，但必须先由 PM 安排 Architecture docs-only repair 和独立
  Data Quality re-review，不得由当前窗口自行进入下一 Gate。
