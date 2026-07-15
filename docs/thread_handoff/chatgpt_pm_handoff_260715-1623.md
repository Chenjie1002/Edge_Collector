# ChatGPT PM Handoff — 2026-07-15 16:23 UTC+8

项目：Edge MES Demo

项目路径：`/Users/chenjie/Documents/MES/edge-mes-demo`

当前 PM Thread 状态：本窗口在 Gate B Raspberry Pi Runtime / Deployment Evidence planning 的 Data Quality `HOLD` intake 后交接。

## 1. Live baseline at handoff authoring time

```text
branch:
main

HEAD:
29f02599447e4510209cd0ad419f70539f034507
Add PM handoff after Gate B closeout

origin/main:
29f02599447e4510209cd0ad419f70539f034507

ahead/behind:
0 0

cached diff:
empty
```

Live Git 是动态 authority。下一位 PM 必须重新执行 read-only recovery，不得把上述 hash 当作永久 current truth。

## 2. Current gate state

### Closed durable implementation gates

```text
Gate A Accepted-events Consumer Truth Hardening:
CLOSED / PASS WITH RECOMMENDATIONS

Gate B Dashboard Raspberry Pi Docker Integration static implementation:
CLOSED / PASS WITH RECOMMENDATIONS
```

Gate B static implementation/review commit：

```text
8ddba3bd547e9e9bd064b002c150b81324833636
Add Dashboard Raspberry Pi Docker integration
```

Gate B status sync commit：

```text
7857be1292cdf5f75d69cd7205ce3058c216a214
Sync Gate B Dashboard Docker integration status
```

上一 PM handoff commit：

```text
29f02599447e4510209cd0ad419f70539f034507
Add PM handoff after Gate B closeout
```

### Current Level 2 planning branch

任务：

```text
Gate B Raspberry Pi Runtime / Deployment Evidence Planning
```

当前阶段状态：

```text
Architecture planning:
PASS WITH RECOMMENDATIONS

Reliability initial planning review:
HOLD on B-R4-1

Architecture negative-growth repair:
PASS

Reliability focused re-review:
B-R4-1 CLOSED
Reliability planning gate: CLOSED / PASS

Data Quality focused planning review:
HOLD

Verification focused planning review:
NOT STARTED / NOT AUTHORIZED

Runtime execution:
NOT EXECUTED / NOT CLAIMED
```

## 3. Current authorized planning reports

以下文件是本 Level 2 planning branch 的当前 untracked authority inputs：

```text
docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md
docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_review.md
docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_rereview.md
docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_data_quality_review.md
```

它们尚未 stage、commit 或 push。

Architecture plan 已覆盖：

- committed release identity；
- `/opt/edge-mes-demo` fixed active path；
- protected staging/archive；
- Branch A existing Dashboard rollback；
- Branch B first-deployment cancellation；
- port `3001` / firewall preflight；
- DockerRootDir/filesystem/image/cache/memory/Swap bytes gates；
- native `linux/arm64/v8` build identity；
- Dashboard-only startup；
- `RestartCount >= 5` terminal；
- process/API/data health separation；
- known-empty、pagination；
- real Case A/B/C；
- exact 22-field DB/API/Dashboard reconciliation；
- rollback/cancellation；
- exact future execution categories and forbidden list。

Reliability `B-R4-1` negative growth blocker 已通过最小 repair 关闭：

```text
raw_image_delta_bytes
raw_cache_delta_bytes

effective_image_growth_bytes = max(0, raw_image_delta_bytes)
effective_cache_growth_bytes = max(0, raw_cache_delta_bytes)
combined_growth_bytes = effective_image_growth_bytes + effective_cache_growth_bytes
```

Negative delta 必须解释并对账；无法解释时 startup 前 `HOLD`；负值不得提供 capacity credit。

## 4. Current Data Quality HOLD

Data Quality report：

```text
docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_data_quality_review.md
```

结论：

```text
HOLD
```

PM 已完成 blocker necessity assessment。只接受以下两个 blocker；报告中 `Recommendations: none`，不得另外创造 carry-forward scope。

### DQ-RUNTIME-EMPTY-1 — accepted as necessary

问题：Phase L 只有 API `items=[]` 和 Dashboard explicit empty，没有冻结同一 bounded production-fact scope 的 PostgreSQL zero-row authority。

这是直接 false-empty PASS 风险，必须最小修复。

允许的最小 repair：

- 只修改 Architecture plan 的 Phase L；
- 必要时同步 Phase P terminal wording；
- source 只能是 `production_accepted_station_event_fact`；
- 使用与 API request 一致的 bounded `line_id/start_time/end_time/limit` record；
- 保存 bounded read-only PostgreSQL zero-row result；
- 同时保留 API `items=[]`、Dashboard explicit empty 和 stale truth clearing；
- claim 只限该 bounded scope；
- 不清空 DB、不插入 fixture、不创建专用 empty dataset。

### DQ-RUNTIME-CASE-C-REL-1 — accepted as necessary but strictly narrowed

问题：Case C 的 `nok_detail_evidence_fact_key` 当前只有 non-null / exact-field evidence，尚未冻结一个可执行的 parent relation proof。若 referenced fact 不存在或不是对应 accepted canonical NOK result，仍可能产生 false Case C PASS。

该 blocker 只允许证明 named Case C detail companion 的直接 parent relation，不得扩展为 relation graph、D7/D8 matrix、route audit、retained archive、forensic framework 或全库 relation completeness。

最小 bounded read-only proof 应只要求：

1. 在同一个 `production_accepted_station_event_fact` authority 中，以
   `fact_key = Case C.nok_detail_evidence_fact_key` 查询 parent；
2. 结果必须恰好解析到一个 accepted fact row；`fact_key` 的 DB unique authority可用于唯一性；
3. parent `event_type = station_result`；
4. parent `production_result = nok`；
5. parent 与 Case C row 必须保持同一 direct companion identity，最小比较：
   - `line_id`；
   - `plc_id`；
   - `station_id`；
   - `cycle_counter`；
   - `config_hash`；
   - `unit_id` / `dmc` 使用 null-safe same-subject comparison；
6. Case C 为 primary detail 时，parent 与 detail 的 `nok_code`、`nok_origin` 必须一致；若当前 runtime evidence 不区分 detail role，则不得在 evidence plan 中额外发明 role taxonomy，应按当前 accepted projection可证明字段保持保守 fail-closed；
7. parent missing、query unavailable、role/result/identity mismatch或无法对账：Case C `HOLD`；
8. real Case C row 本身不存在：仍为 `NOT AVAILABLE / NOT VERIFIED`，不因 relation proof要求把 conditional Case C 变成 mandatory；
9. 不得使用 raw/legacy/diagnostic table、current config、synthetic row 或 API mock补足 relation。

说明：accepted fact projection 当前没有 `parent_event_id`、`plc_boot_id`、`cycle_id` 或 `detail_role` 字段。不得为了这次 runtime planning repair扩大到 schema/API/Collector implementation。只使用当前 22-field production projection能够证明的最小直接关系。

## 5. Recommendation necessity governance update

用户要求把稳定的 recommendation necessity / no-scope-expansion 规则写入 PM Rules。

本窗口已修改：

```text
docs/thread_handoff/pm_operating_rules.md
```

新增规则位于 `Review gate conventions` 的 `PM report intake rule` 下，核心要求：

- PM 不得自动转发 reviewer recommendations；
- 每项 recommendation 必须按当前 product claim 和 gate 评估必要性；
- 分类为 current repair、next-review carry-forward、runtime record、future independent task 或 unnecessary/scope expansion；
- 重复已 mandatory planning/contract 内容不是新任务；
- recommendation 不得未经授权扩大 product claim、threat model、authority fields、retention、runtime topology、allowlist 或 evidence burden；
- 只有能防止 credible false PASS、安全/ownership问题、protected-object mutation或 evidence misclassification 的项才可升级为 blocker/current repair；
- 后续 Prompt 只包含 PM 接受的最小范围；被拒绝、重复或 future-only recommendation 不得成为隐含要求；
- 无必要 recommendation 时写 `Recommendations: none`。

该 PM Rules 修改尚未 stage、commit 或 push。

## 6. Working-tree boundaries

当前 tracked modifications：

```text
M .gitignore
M docs/thread_handoff/pm_operating_rules.md
```

其中：

- `.gitignore` 是 pre-existing external dirty artifact，绝对不得纳入当前 governance/handoff commit；
- `docs/thread_handoff/pm_operating_rules.md` 是本窗口用户明确授权的 governance update。

本窗口新 handoff：

```text
docs/thread_handoff/chatgpt_pm_handoff_260715-1623.md
```

当前 planning reports 和 handoff 均预期为 untracked。

已知其他 external/generated artifacts包括：

```text
frontend/.next/
frontend/node_modules/
frontend/next-env.d.ts
frontend/tsconfig.tsbuildinfo

历史 Dashboard production URL runtime-evidence reports
旧 reports/handoffs
Keynote artifacts
```

不得 clean、restore、删除、整理、broad-stage 或顺手提交。

## 7. Explicitly unexecuted and unclaimed evidence

以下仍全部为：

```text
NOT EXECUTED / NOT CLAIMED
```

- Docker image pull/build；
- base image resolved digest；
- final Dashboard image ID/size；
- native Raspberry Pi `linux/arm64/v8`；
- Compose Dashboard startup；
- port/firewall/resource preflight；
- `RestartCount` runtime gate；
- API-unavailable drill；
- known-empty runtime evidence；
- pagination runtime evidence；
- PostgreSQL real row query；
- API runtime response；
- real Case A；
- real Case B；
- real Case C；
- exact 22-field three-layer reconciliation；
- rollback；
- first-deployment cancellation。

Static/local evidence不得升级为 deployed/native/runtime/DB-backed evidence。

## 8. Recommended next gate sequence

下一位 PM 恢复后应先确认用户授权边界，再按以下顺序推进：

1. Architecture / Integration focused planning repair：只修复
   `DQ-RUNTIME-EMPTY-1` 和严格收窄后的 `DQ-RUNTIME-CASE-C-REL-1`；
2. Data Quality focused planning re-review：只复核两个 blocker closure；
3. Verification focused planning review / exact future execution allowlist audit；
4. PM intake；
5. 用户独立授权后，才可能进入 Raspberry Pi runtime execution。

Reliability gate已经关闭，不应重新打开，除非 DQ repair直接破坏已冻结的 Reliability terminal。

当前不得直接进入 Verification，也不得执行 runtime。

## 9. Current PM task risk classification

```text
Data Quality HOLD repair:
Level 2 focused planning repair

PM Rules governance update:
Level 0 PM-direct docs change, already performed but uncommitted

PM handoff creation:
Level 0 PM-direct governance artifact, already performed but uncommitted

Future stage/commit/push:
not authorized by this handoff
```

## 10. First action for the next ChatGPT PM

必须执行 read-only recovery，不要编辑、不要运行 tests/build、不要连接 Docker/DB/SSH/Pi、不要 stage/commit/push。

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git status -sb

printf '\n--- log -12 ---\n'
git log --oneline -12

printf '\n--- HEAD ---\n'
git rev-parse HEAD

printf '\n--- origin/main ---\n'
git rev-parse origin/main

printf '\n--- ahead/behind ---\n'
git rev-list --left-right --count HEAD...origin/main

printf '\n--- tracked diff ---\n'
git diff --name-only

printf '\n--- cached diff ---\n'
git diff --cached --name-only

printf '\n--- current gate files ---\n'
git status --short -- \
  docs/thread_handoff/pm_operating_rules.md \
  docs/thread_handoff/chatgpt_pm_handoff_260715-1623.md \
  docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md \
  docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_review.md \
  docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_rereview.md \
  docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_data_quality_review.md
```

预期 authoring-time baseline：

```text
HEAD == origin/main == 29f02599447e4510209cd0ad419f70539f034507
ahead/behind = 0 0
cached diff = empty
```

如果只有后续明确授权的 docs-only commit造成 hash漂移，不自动 `HOLD`；按 live Git和 durable authority重新判断。

## 11. Required authority reading order for the next PM

1. `docs/thread_handoff/pm_operating_rules.md`
2. `docs/thread_handoff/chatgpt_pm_handoff_260715-1623.md`
3. `docs/current_status.md`
4. `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_gate_status.md`
5. `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`
6. `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_review.md`
7. `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_rereview.md`
8. `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_data_quality_review.md`
9. `docs/contracts/dashboard_api_contract.md`
10. `db/migrations/007_accepted_station_event_visibility.sql`
11. `collector/app/services/accepted_station_event_fact.py`
12. `docs/contracts/station_event_model.md`，仅用于理解 Case C direct parent relation；不得把完整 stateful relation contract扩大到 runtime Dashboard evidence scope。

## 12. Surfaces not authorized by this handoff

本 handoff 不授权：

- Architecture repair execution；
- Data Quality re-review；
- Verification review；
- implementation或deployment-guide修改；
- tests/typecheck/build；
- Docker/Compose；
- SSH/Raspberry Pi；
- port/firewall/resource inspection；
- API/DB/browser/PostgreSQL query；
- real Case A/B/C；
- rollback/cancellation；
- stage/commit/push/tag；
- status sync；
- deploy。

下一位 PM不得从 handoff 本身推断后续授权。

## 13. Handoff Git boundary

本窗口未 stage、commit 或 push。

未来如用户授权 governance/handoff commit，建议 exact allowlist仅为：

```text
docs/thread_handoff/pm_operating_rules.md
docs/thread_handoff/chatgpt_pm_handoff_260715-1623.md
```

不要把 planning reports与 governance/handoff 自动绑在同一个 commit；它们仍处于未关闭的 Level 2 planning gate，应在 Data Quality和Verification closure后由 PM另行裁决。

不得 stage：

```text
.gitignore
旧 handoffs
历史 reports
Keynote artifacts
frontend generated artifacts
任何 broad docs/ path
```

## 14. Copyable prompt for the next ChatGPT PM window

```markdown
# Edge MES Demo — ChatGPT PM Handoff Restore

你现在接手 Edge MES Demo 项目的 ChatGPT PM 角色。

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

第一优先级：恢复上下文，不要直接推进 Architecture repair、Data Quality re-review、Verification或runtime。

请先读取并遵守：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260715-1623.md`
- `docs/current_status.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_gate_status.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_review.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_rereview.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_data_quality_review.md`

第一动作必须是 read-only recovery：

    git status -sb

    printf '\n--- log -12 ---\n'
    git log --oneline -12

    printf '\n--- HEAD ---\n'
    git rev-parse HEAD

    printf '\n--- origin/main ---\n'
    git rev-parse origin/main

    printf '\n--- ahead/behind ---\n'
    git rev-list --left-right --count HEAD...origin/main

    printf '\n--- tracked diff ---\n'
    git diff --name-only

    printf '\n--- cached diff ---\n'
    git diff --cached --name-only

    printf '\n--- current gate files ---\n'
    git status --short -- \
      docs/thread_handoff/pm_operating_rules.md \
      docs/thread_handoff/chatgpt_pm_handoff_260715-1623.md \
      docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md \
      docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_review.md \
      docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_rereview.md \
      docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_data_quality_review.md

Expected authoring-time baseline：

    HEAD == origin/main == 29f02599447e4510209cd0ad419f70539f034507
    ahead/behind = 0 0
    cached diff = empty

当前真正 gate state：

    Gate A consumer truth:
    CLOSED / PASS WITH RECOMMENDATIONS

    Gate B static Docker integration:
    CLOSED / PASS WITH RECOMMENDATIONS

    Runtime/deployment Architecture planning:
    PASS WITH RECOMMENDATIONS

    Reliability planning:
    CLOSED / PASS

    Data Quality planning:
    HOLD

    Accepted blockers:
    DQ-RUNTIME-EMPTY-1
    DQ-RUNTIME-CASE-C-REL-1

    Verification planning:
    NOT STARTED

    Raspberry Pi runtime evidence:
    NOT EXECUTED / NOT CLAIMED

PM 已评估 blocker和recommendation必要性：

- 两个 blockers 均接受，但必须按 handoff中的 minimal scope修复；
- `Recommendations: none`；
- 不得新增 relation graph、D7/D8、strong-audit、长期 retention、通用取证或额外 runtime topology；
- PM Rules 已新增 recommendation necessity / no-scope-expansion 稳定规则；
- `.gitignore` 是外部 dirty artifact，不能纳入任何当前 commit；
- PM Rules和本 handoff尚未 stage/commit/push。

恢复后请报告：

1. live Git baseline；
2. cached/staged state；
3. 当前四个 planning reports 和 governance/handoff 状态；
4. Data Quality HOLD及两个 accepted minimal blockers；
5. PM Rules governance update是否存在且内容一致；
6. 当前 Thread容量判断；
7. 建议下一步是否为独立 Architecture / Integration focused planning repair。

不要直接修复，不要发出 Thread Prompt，不要 stage/commit/push。完成恢复报告后停止，等待用户明确授权。
```

## 15. Final handoff state

```text
Current Level 2 planning gate:
HOLD at Data Quality

Accepted blockers:
DQ-RUNTIME-EMPTY-1
DQ-RUNTIME-CASE-C-REL-1, strictly narrowed

Reliability planning:
CLOSED / PASS

Recommendations:
none

PM Rules governance update:
created in working tree, uncommitted

New PM handoff:
docs/thread_handoff/chatgpt_pm_handoff_260715-1623.md

Stage/commit/push:
not performed

Next authorized action:
none inferred; next PM must recover and wait for explicit user authorization
```
