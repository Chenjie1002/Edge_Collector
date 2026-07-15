# Sprint 3 Dashboard Raspberry Pi Runtime Deployment Evidence Verification Review

报告名称：

Sprint 3 Dashboard Raspberry Pi Runtime Deployment Evidence Verification Review

任务名称：

Gate B — Raspberry Pi Runtime / Deployment Evidence Verification Focused Planning Review and Exact Future Execution Allowlist Audit

执行 Thread：
Verification

结论：
HOLD

## Reviewed baseline

- HEAD: a21b90ac8952275ef62256954b826d44c94c7045
- origin/main: a21b90ac8952275ef62256954b826d44c94c7045
- ahead/behind: 0 0
- cached diff: empty
- tracked diff: .gitignore only
- target report at recovery: absent
- current planning reports: untracked authorized inputs

Live Git 是本轮 repository authority。M .gitignore、frontend generated artifacts、历史
reports/handoffs 和 Keynote artifacts 均作为 external/generated context 保留，未删除、
restore、clean、修改、stage、commit 或 push。

## Scope

### reviewed files

按用户指定顺序读取并静态复核：

1. docs/thread_handoff/pm_operating_rules.md
2. docs/thread_handoff/chatgpt_pm_handoff_260715-1623.md
3. docs/current_status.md
4. docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_gate_status.md
5. docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md
6. docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_review.md
7. docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_rereview.md
8. docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_data_quality_review.md
9. docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_data_quality_rereview.md
10. docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_verification_review.md
11. docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_verification_implementation_review.md
12. docs/deployment/raspberry_pi.md
13. docker-compose.yml
14. frontend/Dockerfile
15. frontend/.dockerignore
16. frontend/src/app/health/route.ts
17. docs/contracts/dashboard_api_contract.md
18. db/migrations/007_accepted_station_event_visibility.sql

### created file

- docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_verification_review.md

### changed existing files

- none

### explicitly not touched

- all existing planning, reliability, data-quality, verification, status, handoff and PM-rule files;
- docs/deployment/raspberry_pi.md、docker-compose.yml、frontend/**、api/**、collector/**、db/**、config/**；
- .gitignore、历史 Dashboard production URL reports、旧 reports/handoffs、Keynote artifacts；
- frontend/.next/、frontend/node_modules/、frontend/next-env.d.ts、frontend/tsconfig.tsbuildinfo；
- Docker/Compose/SSH/Raspberry Pi/API/DB/PostgreSQL/browser/runtime surfaces；
- staged, committed or pushed Git state。

本轮没有执行 tests、pytest、npm test、typecheck、Next build、Docker/Compose、SSH、
Raspberry Pi、port/firewall/resource command、API request、PostgreSQL query、browser/manual
smoke、rollback 或 cancellation。

## Current gate authority

~~~
Gate A Accepted-events Consumer Truth Hardening: CLOSED / PASS WITH RECOMMENDATIONS
Gate B Dashboard Raspberry Pi Docker Integration static implementation: CLOSED / PASS WITH RECOMMENDATIONS
Gate B Raspberry Pi Runtime / Deployment Architecture planning: PASS WITH RECOMMENDATIONS
Gate B Reliability planning: CLOSED / PASS
B-R4-1: CLOSED
Architecture focused Data Quality repair: CLOSED / PASS
Data Quality planning: CLOSED / PASS
DQ-RUNTIME-EMPTY-1: CLOSED
DQ-RUNTIME-CASE-C-REL-1: CLOSED
Raspberry Pi runtime/deployment execution: NOT EXECUTED / NOT CLAIMED
~~~

旧 Dashboard production URL Option C、D7/D8、manifest root identity strong-audit、retained
archive uniqueness、tamper-resistant evidence subsystem、通用 forensic framework 和已
superseded executable literals 未被重新打开或继承。

## Verification matrix

### V1 — Baseline, scope and evidence hierarchy

PASS（受本报告两个 blocker 影响的 overall gate 除外）。

Live HEAD、origin/main、ahead/behind、cached state 已记录；release authority 固定为
committed HEAD，dirty/untracked/generated files 不得进入 release。计划明确 static、local、
Compose parsing、image identity、Dashboard process、API/DB 和 real three-layer evidence
不可互相升级；当前 Docker、Compose、ARM64、Pi、API/DB、real Case A/B/C、rollback 和
cancellation 全部保持 NOT EXECUTED / NOT CLAIMED。

### V2 — Branch A / Branch B terminal classification

PASS。

Branch A 在 build 前要求 old source release identity、old release/frontend files、old
Compose、resolved Compose checksum、old Dashboard image tag/ID、old container/service/image
baseline、3001 baseline 与 protected-path proof。缺失即 HOLD。Branch B 只有在旧
Dashboard container、image 和 release asset 均不存在时才允许 first deployment；其终局只
能是 first-deployment cancellation / existing-core-services non-impact PASS 或 HOLD。
只有 image、停止 container、文件/image 不匹配或历史状态不明均明确 HOLD，不自动归入
Branch B。

### V3 — Release identity, transport and protected objects

PASS。

计划把 release manifest 绑定到 committed tree、source commit、per-file checksum、archive
checksum 和 /opt/edge-mes-demo；transport 先进入 protected staging，禁止 broad sync 与
destructive --delete。data/、remote .env、DB volume/bind data 和既有 rollback
release/image 均被保护；host generated artifacts、secrets、.git/、host node_modules/
.next、macOS artifacts、__pycache__、*.pyc 和 untracked report/handoff 不得进入
release。无法证明 approved paths、landing checksum 或 protected-path unchanged 即停止。

### V4 — Port, firewall and unknown-process safety

PASS。

计划要求记录 port 3001 listener、owner PID/process/container、Docker published-port
state、实际可用 firewall tool/result 和 Grafana 3000 baseline。unknown listener、owner
无法证明或 firewall boundary 无法确认均为 HOLD；禁止 kill/stop unknown process、改 port、
改 firewall 或修改 Grafana 3000。Branch B cancellation 后要求证明 3001 released / no
listener。

### V5 — Resource, negative growth and startup-before-HOLD

PASS。

B-R4-1 closure 保持完整：

~~~
raw_image_delta_bytes = post_image_usage_bytes - pre_image_usage_bytes
raw_cache_delta_bytes = post_buildkit_cache_bytes - pre_buildkit_cache_bytes
effective_image_growth_bytes = max(0, raw_image_delta_bytes)
effective_cache_growth_bytes = max(0, raw_cache_delta_bytes)
combined_growth_bytes = effective_image_growth_bytes + effective_cache_growth_bytes
~~~

Phase E/H 使用相同 source/scope/unit/parser/accounting method、Docker daemon/context 和
timestamps；raw pre/post values 必须保存。负 delta 必须解释并完成对账，否则 startup 前
HOLD；负值不得提供 capacity credit，也不得抵消另一 counter 的增长。原有 6 GiB、rollback
image formula、3 GiB postflight free-space、1 GiB image、3 GiB combined growth、256 MiB
Swap 和 Swap non-growth thresholds 均保持，未新增或弱化阈值。

### V6 — Native ARM64 build identity

PASS。

计划要求实际 Raspberry Pi host architecture、Docker architecture 和 final image
OS/architecture/variant 均为 linux/arm64/v8，并记录 node:22.23.0-bookworm-slim
resolved RepoDigest、base image ID、final image ID、RepoTags、size bytes、build timestamps、
exit code、bounded logs 和 source release identity。build non-zero、timeout、OOM 或
incomplete image 均 terminal stop，不得 startup 或使用 fallback artifact。

### V7 — Exact Dashboard-only lifecycle allowlist

HOLD — blocker VER-RUNTIME-V7-RM-1。

Startup、failure stop、Branch B cancellation 和 Branch A rollback 的主命令形状已正确冻结：

~~~
docker compose up -d --no-deps dashboard
docker compose stop dashboard
docker compose rm -sf dashboard
docker compose up -d --no-deps --force-recreate dashboard
~~~

但 Future exact execution allowlist category 6 同时写入：

~~~
docker compose rm -sf dashboard 只能用于 first-deployment cancellation 或 PM 明确批准的 Dashboard failure cleanup
~~~

这把 destructive container removal 扩大到 Branch B cancellation 之外；用户当前 exact
allowlist 只授权 Branch B cancellation 使用 docker compose rm -sf dashboard，failure
terminal 只允许 docker compose stop dashboard。该额外 cleanup path 造成 unsafe command
ownership / scope expansion，不能由 PM 的泛化批准替代 category boundary。

最小 blocker：把 category 6 及其相关 future wording 收紧为 rm -sf dashboard 仅限 Branch B
first-deployment cancellation；其他 failure 只能 stop dashboard，需要不同 cleanup 命令时
回 PM，不在本报告中修复。

### V8 — Core-service non-impact

HOLD — blocker VER-RUNTIME-V8-CORE-1。

计划要求在 Dashboard build/start/stop/rollback/cancellation 前后比较 core services 的
container ID、image ID、StartedAt、RestartCount、health/running state、Compose project
identity、network identity 和 container identity，名称相同不能替代 identity proof。这些
comparison fields 足够，但 Phase I/O 与 categories 10/11 没有明确写出以下 terminal predicate：

~~~
任何 core service rebuild、restart、identity drift 或 core status 无法对账 -> HOLD
~~~

如果只记录 comparison 而未把 drift/unavailable 明确 adjudicate 为 HOLD，后续执行者可能
在 core contamination 或无法证明 non-impact 时继续 startup、rollback/cancellation 或
提交整体 PASS。该缺口直接触及 core-service contamination 与 unsafe ownership。

最小 blocker：在 Phase I、Phase O、Phase P 和对应 rollback/cancellation category result 中
补充上述 fail-closed terminal mapping；本报告不修改 plan。

### V9 — 120-second process terminal

PASS。

计划使用统一 terminal：RestartCount >= 5、120 秒未 healthy、持续 restarting/unhealthy、
crash-loop、log-loop 或 request/retry storm -> FAIL。failure 后必须执行
docker compose stop dashboard，并证明 not running、not restarting、not continuously
unhealthy、bounded logs 停止增长且没有持续 API request/retry storm；stop 或 terminal evidence
无法取得即 HOLD，不得继续 data/case evidence。

### V10 — API unavailable drill authorization boundary

PASS。

API-unavailable drill 被限定为独立、bounded、PM separately authorized 的 controlled failure
scenario。未授权时只能 NOT VERIFIED，不得纳入 runtime PASS。未来 drill 的 API unavailable、
Dashboard process health、page fail-closed、no stale truth、same-render no retry、failure 不
重启 Dashboard、恢复后新 request recovery 和 bounded request-count evidence 均已冻结；未要求
本 planning gate 实际执行或新增 fault-injection framework。

### V11 — Known-empty exact evidence

PASS。

line_id/start_time/end_time/limit 同一 bounded scope 已绑定 PostgreSQL、API 和 Dashboard；
source 固定为 production_accepted_station_event_fact，要求 DB zero rows、API
data.items == []、Dashboard explicit empty，并清除 old rows、summary、NOK/detail 和 trace
truth。DB query unavailable、wrong table、scope mismatch、nonzero result、API/UI 不为空、
stale truth 或 scope record 不完整均为 HOLD。禁止 clear DB、fixture、dedicated empty
dataset、schema/API/frontend/Collector change 制造 empty；claim 仅限 named bounded scope。

### V12 — Pagination execution record

PASS。

计划冻结同一 line/time/limit scope、page 1 raw next_cursor、page 1/page 2 fact-key sets、
page 2 unchanged opaque cursor、stable order event_ts, accepted_at, fact_key、bounded DB
authority key set、no duplicate、no omission 和 one request per render。cursor 修改、scope drift、
request count unavailable、key-set 无法对齐或 stale truth 均为 HOLD；没有要求新 filter、
cursor decoder 或 schema field。

### V13 — Real Case A/B/C

PASS（planning only；未执行）。

Case A/B 的 mandatory predicates 与 Case C conditional availability 完整保留。真实 Case C
存在时，parent proof 只在同一 production_accepted_station_event_fact 以
fact_key = Case C.nok_detail_evidence_fact_key 查询，必须 exactly one、event_type=station_result、
production_result=nok，并只比较 line/PLC/station/cycle/config 与 null-safe unit_id/dmc
same-subject identity。parent proof unavailable/mismatch 为 Case C HOLD；真实 Case C row
不存在为 NOT AVAILABLE / NOT VERIFIED。未引入 parent_event_id、plc_boot_id、cycle_id、
detail_role、parent/detail NOK equality、relation graph、D7/D8、archive/forensics 或新
authority fields。

### V14 — Exact 22-field reconciliation

PASS（planning only；未执行）。

每个真实 case 均要求：

~~~
PostgreSQL raw row
-> API raw JSON exact 22-field item
-> Dashboard display mapping
~~~

逐字段记录 DB raw value、API raw JSON value、display rule、Dashboard visible value 和
PASS/FAIL；fact_key 为主 identity，并核对 source_event_id、content_fingerprint、
event_ts、accepted_at。historical config 不被 current config 覆盖，placeholder 不进入
API raw value，station_nok 不成为第二个 production result，Case C parent proof 与 22-field
table 分离。

### V15 — Rollback / cancellation terminal audit

HOLD（由 V7/V8 blockers 传播）。

Branch A 已要求恢复 approved old files/Compose/image、docker compose config --quiet、
Dashboard-only force-recreate、Dashboard /health、一次 bounded accepted-events request、
core comparison 和 data/.env protection。Branch B 已要求 stop、rm dashboard only、恢复
pre-deployment files、config parse、container absent、3001 released、core baseline/health
preserved 和 data/.env unchanged；终局不是 Dashboard rollback PASS。由于 rm 的额外 cleanup
例外和 core drift 的 terminal mapping 尚未收紧，rollback/cancellation 当前不能被审核为
exact fail-closed allowlist。

### V16 — Final evidence classification and overall terminal

PASS（分类层本身）。

计划保持 focused test、TypeScript/Next build、Compose config、image inspect、Dashboard
/health、API /health、DB/API/Dashboard target mapping 各自独立的 evidence meaning；低层
证据不得升级为 high-level PASS。Known-empty、pagination、mandatory Case A/B、Case C
relation、22-field、resource/build/startup、protected-path、core non-impact 或适用
rollback/cancellation 任一 mandatory phase 为 HOLD 时，overall 不得 PASS。本轮 overall
仍因 V7/V8 blockers 为 HOLD。

## Future execution allowlist audit

### Allowed categories

| category | purpose / scope | mutation object | bypass prohibition | terminal / result | audit |
|---|---|---|---|---|---|
| 1. local read-only release identity | committed HEAD manifest/checksum | none | no dirty content | mismatch/missing -> HOLD | PASS |
| 2. remote read-only preflight | host, Compose, ports, resources, protected metadata | none | missing metric/firewall -> HOLD | PASS |
| 3. release transport | approved archive/manifest to protected staging | staging only | no broad sync/--delete/secrets/protected overwrite | checksum/protection failure -> HOLD | PASS |
| 4. Dashboard-only image build | one Dashboard image from approved release context | Dashboard image/build cache only | no other service, no up --build, no fallback | non-zero/timeout/OOM/incomplete -> terminal stop | PASS |
| 5. image inspect | bounded image/base identity evidence | none | no tag-only ARM64 claim | incomplete identity -> HOLD | PASS |
| 6. Dashboard startup/stop/rm | startup/failed stop/Branch B cancellation | Dashboard container only | no core service; rm exception is too broad | mismatch/stop proof failure -> HOLD; category boundary currently unsafe | HOLD |
| 7. bounded health/API/page | Dashboard/API/DB/page evidence, API drill separately authorized | no DB write | no retry/fallback/secret capture | unavailable/scope/request ambiguity -> HOLD or NOT VERIFIED as defined | PASS |
| 8. bounded PostgreSQL read-only | accepted-fact, empty, pagination, Case C parent reads | read-only transaction only | no write/migration/fixture/legacy join | query unavailable/mismatch -> HOLD | PASS |
| 9. bounded logs | bounded Dashboard/API request evidence | none | no unbounded follow/log absence as PASS | missing bounded proof -> HOLD | PASS |
| 10. Branch A rollback | old asset restore and Dashboard-only force recreate | approved old release/image + Dashboard | no core/data/.env mutation | missing asset/evidence/drift -> HOLD | HOLD propagated from V8 |
| 11. Branch B cancellation | stop/rm Dashboard and restore pre-deploy files | Dashboard + approved pre-deploy files | no rollback PASS/core/data/.env mutation | absent/port/core/protection failure -> HOLD | HOLD propagated from V7/V8 |
| 12. final evidence collection | collect approved records and classify terminal | evidence record only | no execution hidden in collection | incomplete mandatory record -> HOLD | PASS |

除 category 6 与 core non-impact terminal mapping 外，12 类 category 均有明确 purpose、scope、
mutation boundary、forbidden bypass 和 terminal result；未覆盖命令必须回 PM，不得由执行 Thread
自行解释。任何 category 都不隐式授权其他 service、DB write、protected-object mutation 或
runtime topology change。

### Forbidden list

当前 plan 已覆盖本 product claim 所需的 forbidden surface：

~~~
docker compose down
full-stack docker compose up -d --build
volume delete/recreate
DB migration/write/fixture/synthetic fact insert
data restore
image/cache/system/builder prune
unknown listener/process termination
port/firewall modification
remote .env modification
data/ overwrite/delete/reinitialize
API/PostgreSQL/Collector/Grafana/V-PLC/core-service rebuild
host node_modules/.next/macOS artifact transport
localhost/127.0.0.1/relative/browser-origin API fallback
NEXT_PUBLIC_* origin
root runtime
temporary Dockerfile/Compose override
package install/upgrade
implementation edit
stage/commit/push/tag
any unlisted command
~~~

但现有 category 6 的 rm -sf dashboard exception 与 Branch B-only requirement 冲突。因此
在 blocker closure 前，Forbidden list audit 结果不是 complete；应补充：docker compose rm -sf
dashboard outside Branch B first-deployment cancellation is forbidden。

### Unlisted-command terminal

PASS。

计划明确：任何未被 exact allowlist 覆盖的 future command 在执行前必须回 PM，不能由执行 Thread
自行解释。该规则不能消除 category 6 已列出的过宽 exception，因此不关闭
VER-RUNTIME-V7-RM-1。

### Result

HOLD。

原因仅为：

1. rm -sf dashboard 的 command ownership 超出 Branch B cancellation；
2. core-service drift/restart/rebuild/status-unreconciled 未明确 terminal HOLD。

## Reliability preservation

- B-R4-1: CLOSED / PRESERVED
- raw/effective image/cache growth、negative-delta reconciliation、no capacity credit、same
  measurement identity、startup-before-HOLD 和原有 resource thresholds 均保持。
- 本轮没有重开 Reliability scope，也没有新增 resource threshold、telemetry、retention 或
  tamper-resistant evidence requirement。

## Data Quality preservation

- DQ-RUNTIME-EMPTY-1: CLOSED / PRESERVED
- DQ-RUNTIME-CASE-C-REL-1: CLOSED / PRESERVED
- known-empty 只允许同一 bounded production-fact scope 的 PostgreSQL zero-row + API empty +
  Dashboard explicit empty；Case C parent proof 仍是同表 fact_key direct relation，缺失/不一致
  为 HOLD，真实 Case C 缺失为 NOT AVAILABLE / NOT VERIFIED。
- 本轮没有新增 relation graph、D7/D8、schema/API/frontend/Collector implementation 或额外
  Data Quality authority field。

## Evidence

- checks run:
  - read-only Git recovery；
  - 指定 1–18 authority order 的完整静态阅读；
  - V1–V16 targeted cross-reference；
  - rg consistency checks for terminal predicates, category allowlist and forbidden list；
  - conflict-marker check；
  - new report git diff --no-index --check /dev/null <new-report> whitespace check。
- tests/build/runtime:
  - not run；没有执行 tests、pytest、npm test、typecheck、Next build、Docker/Compose、SSH、
    Raspberry Pi、port/firewall/resource command、API request、PostgreSQL query、browser/manual
    smoke 或 rollback/cancellation。
- staged files: none
- allowlist compliance:
  - only the new Verification report was created；
  - no existing file was changed；
  - no file was staged, committed or pushed；
  - external/generated artifacts were preserved。

## Blockers

### VER-RUNTIME-V7-RM-1 — rm -sf dashboard exceeds Branch B-only command ownership

- plan section: Future exact execution allowlist, category 6；
- false/safety path: a listed destructive cleanup path permits Dashboard container removal outside
  the exact Branch B first-deployment cancellation terminal；
- minimal repair: restrict docker compose rm -sf dashboard to Branch B first-deployment
  cancellation only；failure terminal remains docker compose stop dashboard；other cleanup command
  requires a new PM-authorized category and is outside this review；
- no repair performed。

### VER-RUNTIME-V8-CORE-1 — core-service drift lacks explicit fail-closed terminal

- plan sections: Phase I、Phase O、Phase P and future categories 10/11；
- false/safety path: core rebuild/restart/identity drift or unreconciled status can be recorded as a
  comparison without an explicit HOLD，allowing contaminated startup/rollback/cancellation or
  overall PASS；
- minimal repair: map any core rebuild、restart、identity drift or unavailable/unreconciled core
  comparison to HOLD in all affected phase/category terminal wording；
- no repair performed。

## Recommendations

~~~
Recommendations:
- none
~~~

没有自动转发 Architecture、Reliability、Data Quality 或旧 Verification report 中的
recommendations；重复 mandatory requirements 不被创建为新 recommendation。

## Overall gate

- Verification planning gate: HOLD
- eligible for: none; return to PM for the two minimal plan repairs and an independent Verification re-review
- PM approval required before: any plan repair, runtime execution, Docker/Compose/SSH/Raspberry Pi/API/DB/PostgreSQL/browser action, rollback/cancellation, implementation/docs repair, stage/commit/push/tag/deploy

## Thread 输出 / 上下文评估

- 本次输出长度：长
- 当前 Thread 是否建议继续：no
- 下一轮是否建议新开 Thread：yes
- 理由：本轮是独立 Verification planning gate；已发现两个必须由 PM 裁决的最小 plan
  blocker，不能顺势进入 runtime execution，也不应重新打开旧 Dashboard URL strong-audit、
  Architecture、Reliability 或 Data Quality 分支。
