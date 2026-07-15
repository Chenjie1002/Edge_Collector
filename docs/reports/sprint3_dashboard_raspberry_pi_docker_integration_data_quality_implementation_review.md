# Sprint 3 Dashboard Raspberry Pi Docker Integration Data Quality Implementation Review

报告名称：

`Sprint 3 Dashboard Raspberry Pi Docker Integration Data Quality Implementation Review`

任务名称：

`Gate B — Dashboard Raspberry Pi Docker Integration Data Quality Focused Implementation Review`

执行 Thread：

`Data Quality`

## Conclusion

**PASS WITH RECOMMENDATIONS**

六文件实际 implementation 未发现会改变 accepted-fact authority、错误切换
API origin/profile、把 process health 冒充 data health、污染 Docker build context、
覆盖 `data/`/remote `.env`、重建或改写 PostgreSQL facts、混淆 Case A/B/C、混写
DB/API/Dashboard 三层值，或把 synthetic/static evidence 升级为 real closure 的
Data Quality blocker。

本结论是静态 focused implementation review，不是 Docker build、Compose startup、
Linux ARM64、Raspberry Pi、Dashboard runtime、PostgreSQL real row、API runtime 或真实
Case A/B/C PASS。真实 DB/API/Dashboard 三层闭环仍为 `NOT EXECUTED / NOT CLAIMED`。

## Recovery baseline

本轮第一动作完成 read-only recovery：

```text
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 683a8a0eb9f901dbc5c53c9bef5c4e68acf95ffb
origin/main: 683a8a0eb9f901dbc5c53c9bef5c4e68acf95ffb
ahead/behind: 0 0
latest: 683a8a0 Add PM handoff after Gate A closeout
cached diff: empty
target report before creation: absent
```

六文件状态符合 task baseline：

```text
M  docker-compose.yml
M  docs/deployment/raspberry_pi.md
?? frontend/Dockerfile
?? frontend/.dockerignore
?? frontend/src/app/health/__tests__/route.test.ts
?? frontend/src/app/health/route.ts
```

受保护路径 tracked diff 为空。既有外部/generated artifacts 保持不动，包括 `M
.gitignore`、旧 handoff/reports、旧 runtime-evidence reports、Keynote artifact、
`frontend/.next/`、`frontend/node_modules/`、`frontend/next-env.d.ts` 和
`frontend/tsconfig.tsbuildinfo`。

## Scope

### Reviewed six files

```text
frontend/Dockerfile
frontend/.dockerignore
frontend/src/app/health/route.ts
frontend/src/app/health/__tests__/route.test.ts
docker-compose.yml
docs/deployment/raspberry_pi.md
```

### Read-only authority files

按 PM 指定顺序读取了 PM rules、PM handoff、`docs/current_status.md`、Gate B
Architecture plan、Reliability planning review/re-review、Data Quality planning
review/re-review/round 2、Verification planning review、Reliability implementation
review，以及 accepted-fact consumer/API/DB/Collector authority files：

```text
frontend/src/lib/acceptedStationEvents/schema.ts
frontend/src/lib/acceptedStationEvents/apiClient.ts
frontend/src/lib/acceptedStationEvents/viewModel.ts
frontend/src/app/accepted-events/page.tsx
api/app/routes/accepted_station_events.py
db/migrations/007_accepted_station_event_visibility.sql
collector/app/services/accepted_station_event_fact.py
```

### Created and explicitly not touched

本轮只创建本报告：

```text
docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_implementation_review.md
```

未修改六文件、accepted-events consumer、API、DB、Collector、Grafana、V-PLC、package
或 config 文件，未修改既有报告、handoff、`.gitignore` 或 generated artifacts。

## Data Quality implementation matrix

### Accepted-fact authority

通过。六文件没有引入 legacy table、raw event table、diagnostic endpoint、Grafana
query、browser-side direct DB/API、static JSON、local fixture 或 mock runtime source。
既有 authority 仍为：

```text
PostgreSQL production_accepted_station_event_fact
→ GET /api/v2/production/accepted-station-events
→ strict Dashboard accepted-events consumer
```

只读复核的 `schema.ts`、`apiClient.ts`、`viewModel.ts`、API route、migration 与
Collector fact builder 均未出现 Gate B diff；Gate B 未改变 Gate A 的 exact envelope、
exact 22-field、cross-field、raw/display 或 no-fallback boundary。

### API origin/profile authority

通过。`docker-compose.yml:99-105` 精确注入：

```text
EDGE_MES_DASHBOARD_API_ORIGIN=http://api:8000
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=container
```

两个值位于 runtime `environment`，不是 `ARG`、`NEXT_PUBLIC_*` 或 browser-side config。
Compose 没有 localhost/host port `8000`/relative URL/browser-origin fallback；浏览器
拓扑保持：

```text
browser → http://<Pi-IP>:3001 → Dashboard server → http://api:8000 → API → PostgreSQL
```

Compose 中出现的 `127.0.0.1` 只用于容器内部 Dashboard `/health` healthcheck
（`docker-compose.yml:111-120`），不是 API origin。`depends_on: service_started` 只表示
启动顺序，未被当作 API/data readiness。

### Build context、image 与 secret boundary

通过。`frontend/.dockerignore:1-10` 排除 host `.next`、`node_modules`、
`tsconfig.tsbuildinfo`、`next-env.d.ts`、coverage、logs、`.git`、`.env` 与 `.env.*`，
没有 negation 重新包含 secret。`frontend/Dockerfile:6-17` 只以 tracked
`package.json`/`package-lock.json` 建立 `npm ci` dependency layer，并在 builder 中构建。

`frontend/Dockerfile:19-37` 的 runner 只复制 standalone、static、public，使用 non-root
`node` 和 `node server.js`；没有复制 host build artifact、remote `.env`、DB secret、
raw evidence、历史报告、Git metadata 或业务数据 volume。实际 image build、digest 和
ARM64 证据尚未执行，不能由静态内容推出 runtime PASS。

### Process health 与 data health 分离

通过。`frontend/src/app/health/route.ts:1-9` 只返回固定的：

```json
{"status":"ok","service":"dashboard"}
```

它不读取 API origin、API response、PostgreSQL、accepted facts、lineage、Collector
状态或业务 filesystem。`route.test.ts:10-23` 已有前序 focused PASS 证据，冻结固定
shape、status、无额外字段和 no-fetch/external-dependency independence。

`/health = 200` 只证明 Next HTTP process 可响应；不证明 API、DB、accepted fact、数据
新鲜度、Case A/B/C 或 DB/API/Dashboard 闭环。

### Runtime environment 与 historical lineage

基本通过。`docs/deployment/raspberry_pi.md:455-466` 要求记录 source release
ID/commit、resolved Compose baseline、base image digest/ID、最终 image ID/size 和
实际 `linux/arm64/v8` architecture；`10.9` 又要求保存 `config_hash`、`config_version`、
`event_ts`、`accepted_at` 与 identity fields。历史 row 的 config lineage 继续来自
accepted fact row，不使用当前 config 查询、`latest` tag 或当前 Grafana 显示覆盖。

Compose literal origin/profile 已冻结，未发现 source authority 漂移 blocker。建议在
后续 runtime evidence record 中额外逐项保存实际
`EDGE_MES_DASHBOARD_API_ORIGIN` 与 `EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE`，使运行时
拓扑 identity 可直接复核；这是证据模板建议，不是当前 source/authority blocker。

### `data/` 与 remote `.env` protection

通过。`docs/deployment/raspberry_pi.md:435-453` 将六文件标记为 changed-file scope，
同时要求远端仍保留完整 approved tracked frontend baseline；发布 transport 明确排除
`data/`、remote `.env`、`.git`、host generated artifacts、`node_modules`、`.next`、
`next-env.d.ts`、`tsconfig.tsbuildinfo`、`__pycache__` 与 `*.pyc`。

文档没有授权 destructive sync、复制本地 `.env`、删除 data、初始化新 DB、重放
synthetic facts、修改 Collector 或 migration；Dashboard-only update 也没有数据
volume mount。

### Dashboard-only update 的数据非影响性

通过。文档 `10.7` 将唯一 Dashboard-only 路径固定为：

```bash
docker compose up -d --build --no-deps dashboard
```

并明确 full-stack `docker compose up -d --build` 与 `docker compose down` 不是本 Gate
的 Dashboard-only 操作。`--no-deps`、无 data/DB volume 和六文件 scope 共同保持
PostgreSQL、API、Collector、Grafana、V-PLC、Simulator、Prometheus 与既有 accepted
facts 不被 Dashboard update 主动重建、重启或重写。

### Rollback 的数据真实性

通过。已有上一版 Dashboard 时，文档要求在 build 前保存旧 release files、source
release ID/commit、旧 image tag/ID、resolved Compose baseline 与 service/container
baseline；恢复仅作用于 Dashboard release/image/Compose 定义，缺少 asset 或 post-
rollback evidence 即 `HOLD`。

Rollback 明确禁止恢复/覆盖 PostgreSQL data、volume、DB migration、accepted facts、
Collector/API/PostgreSQL 或其他 core service；`docker compose down`、image prune、
data restore 也被禁止。rollback 后的 bounded accepted-events request 只能证明恢复
Dashboard 的 bounded ready/fail-closed 合同，不能扩大为整页或全库事实正确性。

### First-deployment cancellation 的数据完整性

通过。无旧 Dashboard 路径被准确命名为：

```text
first-deployment cancellation / existing-core-services non-impact validation
```

文档只允许 stop/rm 失败 Dashboard、恢复部署前 Compose/release files、执行
`docker compose config --quiet`，并要求 Dashboard container/port 消失、core
service/container/image baseline 与 health 不变、API/PostgreSQL/Collector/Grafana/
V-PLC 未重建、`data/` 与 remote `.env` 未覆盖或初始化。它明确禁止称为 Dashboard
rollback PASS、Dashboard `/health` PASS、accepted-events PASS 或 Case A/B/C PASS。

这条静态路径没有可见的 DB/data mutation command；后续 runtime record 建议增加 bounded
PostgreSQL identity/fact non-mutation witness，不导出无界生产数据，但当前不构成 blocker。

### Real Case A/B/C classification

通过，且当前没有声称真实证据：

```text
Case A — mandatory: real accepted station_result / production_result=ok
Case B — mandatory: real accepted station_result / production_result=nok,
                   nok_code and nok_origin non-null
Case C — conditional: real accepted station_nok detail companion
```

`docs/deployment/raspberry_pi.md:787-806` 明确 Case C 缺失时只能写
`NOT AVAILABLE / NOT VERIFIED`，不得用 synthetic fixture、mock、API-only fixture、
Case B 或 cycle event 替代；`station_nok` 不会被称为第二个 production result，Case B
也不被称为 detail companion。

### Exact 22-field DB/API/display reconciliation

静态合同通过，真实对账未执行。文档 `10.9` 要求每个真实 case 保存：

```text
PostgreSQL production_accepted_station_event_fact raw row
→ API raw JSON exact 22 fields
→ Dashboard display rule/value
```

逐字段表列包含 `field`、`DB raw value`、`API raw JSON value`、`display rule`、
`Dashboard visible value` 和 `PASS/FAIL`；display placeholder 不得填入 API raw value。
22 fields 为：

```text
line_id, plc_id, station_id, station_type, profile_id,
config_hash, config_version, event_type, production_result, unit_id, dmc,
cycle_counter, source_event_id, event_ts, accepted_at, fact_key,
content_fingerprint, nok_code, nok_origin, nok_detail_code,
nok_detail_source_event_id, nok_detail_evidence_fact_key
```

只读 consumer 复核进一步确认 `schema.ts` 保留 raw string/number/null，`viewModel.ts`
以独立 `DisplayValue.raw/text/kind` 派生显示值，`station_nok`/cycle 的显示规则不被
写回 API raw value。

### `fact_key` 与 identity binding

通过。文档要求每个 case 以 `fact_key` 为主 identity，并同时核对：

```text
source_event_id
content_fingerprint
event_ts
accepted_at
```

`event_ts` 与 `accepted_at` 语义保持分离；`accepted_at` 未被称为 ACK/freshness；
`content_fingerprint` 未被替代为 fact identity。`production_accepted_station_event_fact`
→ API DTO → view model/table/detail/trace 的同一 first item 绑定保持不变。

### `items[0]` claim boundary

通过。文档要求每个 case 用独立 bounded query 让目标 fact 成为 API response 的
`items[0]`，声明范围仅为该 bounded request 的目标第一项，不扩大为整页、全时间窗或
整个数据库。当前没有新增通用 row selection，也没有修改 page 的 first-item 语义。

### Empty、pagination、failure/recovery truth

核心 authority 通过，但 operator evidence template 仍可更精确：

- 当前 Gate A consumer 已有 no-stale/fail-closed 行为；API stopped、503、其他 5xx、
  transport failure 和 malformed 2xx 不会保留旧 production truth，恢复只由新的 page
  request 触发，且同一 render 不 retry/fallback/partial salvage。
- Gate B 文档要求 bounded query、opaque cursor、目标 `items[0]` 与 one request per
  render，但没有在 Section 10.9 再列出 known-empty `items=[]` 清除旧 row/summary/detail/
  trace，以及 page 2 保持 `line_id/start_time/end_time/limit` 不变并独立保存
  `fact_key` 集合的完整 operator record 模板。

这不会改变当前 consumer/API authority，也不会制造 stale truth 或 false real closure；
列为非阻断 recommendation。若 runtime evidence 缺失这些证明，结论仍应保持 `HOLD`，
不得以截图、health 或 container running 替代。

### Synthetic/static/real evidence labels

通过。当前证据标签保持：

```text
focused health test       → synthetic / focused implementation evidence
typecheck / local build   → local source/build evidence
docker compose config     → Compose static parsing evidence
Dashboard /health         → process readiness evidence
image inspect             → image identity evidence
DB row + API raw + UI map → real DB-backed three-layer case evidence
```

当前没有执行 Docker image build、Compose startup、Pi runtime、DB query 或 real Case
A/B/C；这些未被六文件 implementation 或本报告升级为 real closure。

### Sensitive-data boundary

通过。六文件和部署文档要求保存的是 bounded health/status、release/image identity、
exact accepted-fact fields 和 display mapping；没有要求输出 remote `.env` 内容、密码、
完整 secret-bearing URL、完整 raw response body、raw diagnostic payload、parser 内部
错误或不受控 Docker 全量 env。部署文档继续禁止把 credentials 写入 repo/report/log。

## Reliability recommendations impact

Reliability implementation review 的建议均为 non-blocking carry-forward：

| Recommendation | Data Quality judgment |
| --- | --- |
| 将 restart 终局措辞统一为 `RestartCount >= 5` | 不影响 fact authority 或三层数据真实性；carry-forward |
| rollback 的 bounded accepted-events request 增加固定 command/result template | 提高可复核性；当前文档已把该 evidence 设为 PASS 前提；non-blocking |
| first-cancellation 后记录 3001 listener/core baseline | 有助于证明取消只影响 Dashboard；当前保护边界已存在；non-blocking |
| image/cache 统一为 bytes 并给出 growth 算式 | 资源复核精度问题，不改变 data truth；non-blocking |
| 记录 resolved base digest、ARM64、image/runtime identity | 提高历史 lineage 复核性；实际证据仍未执行；carry-forward |

没有一项建议使当前六文件 implementation 的 truthful static adjudication 不可能；不因
“可写得更详细”而 `HOLD`。

## Prior evidence

本轮不重复执行前序验证；使用其作为分层证据，不扩大声明：

```text
focused health test:
PASS — 前序 Reliability implementation review 提供 1 file / 1 test evidence

TypeScript validation:
PASS — PM/前序 Gate B evidence；本轮未重跑

local Next build:
PASS — PM/前序 Gate B evidence；本轮未重跑

docker compose config --quiet:
PASS — PM-provided manual result, exit code 0；本轮未重跑

Reliability implementation review:
PASS WITH RECOMMENDATIONS；无 Reliability blocker

Gate B Verification planning review:
PASS WITH RECOMMENDATIONS；六文件 allowlist necessary/sufficient/exact

Evidence limitation:
以上均不是 Docker build、Compose startup、ARM64/Pi runtime、DB/API/Dashboard
three-layer closure 或 real Case A/B/C evidence。
```

本轮唯一允许的验证为 `git diff --check`，结果为 `PASS`，exit code `0`。

## Blockers

```text
none
```

未发现：

```text
accepted-fact source/consumer authority 被 Gate B 改写
origin/profile 错误 fallback 或 browser/container authority 混用
/health 被升级为 API/DB/data readiness
host/generated/secret artifact 进入 image 的静态路径
release 覆盖 data/或 remote .env
Dashboard-only update 重建 PostgreSQL/API/Collector
rollback 覆盖 DB facts 或 first deployment 被称为 rollback PASS
Case A/B/C 语义混淆或 Case C synthetic replacement
22-field raw/display 列混写
fact_key / event_ts / accepted_at identity 混淆
items[0] evidence 被扩大为整页/全库 closure
failure/empty 状态保留 stale production truth
synthetic/static evidence 被升级为 real closure
必须修改六文件外路径
live Git、cached diff、allowlist 或 protected path 冲突
```

## Recommendations

1. 在 `docs/deployment/raspberry_pi.md` 的 runtime identity record 中增加实际
   `EDGE_MES_DASHBOARD_API_ORIGIN` 与 `EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE` 两项。
2. 为 rollback bounded request、known-empty、pagination page 2 和
   first-deployment cancellation 增加固定 command/result record 模板；保留
   `items[0]`、opaque cursor、scope 参数与每页 `fact_key` 集合边界。
3. 在后续 cancellation runtime evidence 中增加 bounded PostgreSQL identity/fact
   non-mutation witness，不导出无界生产数据。
4. 采集实际 `node:22.23.0-bookworm-slim` resolved digest、native `linux/arm64/v8`
   build/run、final image ID/size、restart terminal outcome；image/cache 记录统一为
   bytes 并给出 growth 算式。
5. 保持 Case C 缺失时的 `NOT AVAILABLE / NOT VERIFIED`，不要用 synthetic data 补齐。

## Authorization boundary

```text
no implementation edits
no Docker build/start
no Compose startup
no PostgreSQL/API/SSH/Raspberry Pi/browser/server runtime
no real Case A/B/C evidence
no Git add/commit/push/tag/restore/reset/clean
```

本轮没有进入 HOLD repair，也没有修改六文件外路径。

## Git status

```text
HEAD == origin/main == 683a8a0eb9f901dbc5c53c9bef5c4e68acf95ffb
six-file implementation state: 2 tracked modifications + 4 untracked implementation files
cached diff: empty before report creation
protected paths tracked diff: empty
external/generated artifacts: preserved and excluded
report-only change:
?? docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_data_quality_implementation_review.md
```

除本报告外没有产生新文件；没有 stage、commit、push、restore、reset 或 clean。

## Next gate

`PASS WITH RECOMMENDATIONS`：

```text
PM intake
→ Verification focused implementation review eligible
```

进入 Verification 前仍需由 PM 单独授权该 review lane；本报告不授权 Docker/Compose
runtime、Raspberry Pi deployment、rollback/cancellation drill、PostgreSQL query、real
Case A/B/C、docs sync、stage、commit 或 push。

## Thread output / context assessment

```text
本次输出长度：长
当前 Thread 是否建议继续：no
下一轮是否建议新开 Thread：yes
理由：Data Quality focused implementation review 已独立闭合；下一步应保持 Verification
focused implementation review 与 runtime/real-evidence lane 隔离，避免把 static PASS
WITH RECOMMENDATIONS 误带入 Docker/Pi/DB authorization。
```
