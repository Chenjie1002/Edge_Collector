# Sprint 3 Dashboard Raspberry Pi Runtime Deployment Evidence Reliability Review

报告名称：

`Sprint 3 Dashboard Raspberry Pi Runtime Deployment Evidence Reliability Review`

任务名称：

`Gate B — Raspberry Pi Runtime / Deployment Evidence Reliability Focused Planning Review`

执行 Thread：

`Reliability`

## 1. 结论

**HOLD**

当前 Architecture planning report 已覆盖大部分 runtime/deployment safety boundary，
但 Resource bytes authority 仍有一个直接影响 false runtime PASS 的 blocker：它定义了
`image_growth_bytes`、`cache_growth_bytes` 与 `combined_growth_bytes`，也规定了 required
metric/单位/parser 不可复核时 `HOLD`，却没有规定负增长必须解释并完成前后状态对账。
因此不能确认异常负值不会被当作容量余量，继而绕过 postflight resource gate。

本报告不修改 Architecture planning report、deployment guide、Compose、实现代码或任何
external/generated artifact。结论只适用于 planning review，不表示 Docker、Raspberry Pi、
ARM64、runtime、API/DB、rollback、cancellation 或真实 Case A/B/C 已执行。

## 2. Reviewed baseline

- project: `/Users/chenjie/Documents/MES/edge-mes-demo`
- branch: `main`
- live `HEAD`: `29f02599447e4510209cd0ad419f70539f034507`
- live `origin/main`: `29f02599447e4510209cd0ad419f70539f034507`
- ahead/behind: `0 0`
- cached diff: empty
- tracked diff: `.gitignore` only
- Architecture planning report: present as untracked authorized input
- proposed Reliability report before creation: absent

已知 `M .gitignore`、`frontend/.next/`、`frontend/node_modules/`、
`frontend/next-env.d.ts`、`frontend/tsconfig.tsbuildinfo`、历史 reports/handoffs 与
Keynote artifacts 均按授权作为 external/generated artifacts 保留，未删除、恢复、整理、
stage、commit 或 push。旧 PM handoff 中的 authoring-time baseline 由 live Git supersede，
未形成 task-specific recovery conflict。

## 3. Scope and allowlist compliance

### Reviewed files

按用户指定顺序读取并复核：

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/reliability.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260715-0920.md`
- `docs/current_status.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_gate_status.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_plan.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_reliability_review.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_reliability_rereview.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_reliability_implementation_review.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_verification_review.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_verification_implementation_review.md`
- `docs/deployment/raspberry_pi.md`
- `docker-compose.yml`
- `frontend/Dockerfile`
- `frontend/.dockerignore`
- `frontend/src/app/health/route.ts`
- `frontend/src/app/health/__tests__/route.test.ts`

### Created file

- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_review.md`

### Changed existing files

- none

### Explicitly not touched

Architecture planning report、PM/current-status/handoff docs、deployment guide、Compose、
Dockerfile、`.dockerignore`、health route/test、accepted-events consumer、API、DB、Collector、
Grafana、V-PLC、config/package/dependency files、`.gitignore`、历史/生成 artifacts，以及
Git staged/committed/pushed state。

## 4. R1–R10 Reliability review

### R1 — Branch A / Branch B fail-closed: PASS

Runtime plan Phase B/F 要求 Branch A 同时具备 old Dashboard release files、old Compose、
old image tag/ID、old container/service/image baseline、resolved Compose baseline、port
baseline 与 protected-path proof；缺任一项即 `HOLD`。只有在 previous Dashboard container、
image、release asset 均不存在时才允许 Branch B。

只有 image、停机 container、文件与 image 不一致或无法判断历史可运行状态时明确归入
ambiguous state 并 `HOLD`，不会错误地按 first deployment 处理。Branch B 终局只允许
first-deployment cancellation，不会声明 Dashboard rollback PASS。

### R2 — Protected paths / transport safety: PASS

Runtime plan Phase A/C/F 固定 release source 为 committed `HEAD`，排除 dirty、untracked、
generated、host `node_modules`/`.next`、macOS artifacts 与 credentials。active path 固定为
`/opt/edge-mes-demo`，并区分 protected staging/archive 与 active path。

`data/`、remote `.env`、DB volume/bind data、既有 rollback release/image 均被列为不得
覆盖或删除对象；transport 禁止 destructive `--delete` 与 broad sync，protected-path
identity/metadata 变化会触发 `HOLD`。未见会把 static/image/process evidence 越级成
production data evidence 的路径。

### R3 — Port `3001` / firewall terminal: PASS

Runtime plan Phase D 要求记录 listener owner 至 PID/process/container、published-port
state、实际可用 firewall tool/result 与 Grafana `3000` baseline。owner 或 firewall
boundary 无法确认时 `HOLD`；禁止停止未知 process/listener、临时改 port 或改变 Grafana
`3000`。Branch B cancellation 后还要求固定记录 `3001 released / no listener`。

### R4 — Resource bytes authority / calculations: HOLD

计划已正确要求分别记录 DockerRootDir 与 `/opt/edge-mes-demo` filesystem identity、
total/free bytes、image usage、BuildKit cache、memory/Swap、same-filesystem 关系，并在同一
filesystem 时只计算一次但保留两条 path identity。bytes 公式与门禁也已冻结：

```text
image_growth_bytes = post_image_usage_bytes - pre_image_usage_bytes
cache_growth_bytes = post_buildkit_cache_bytes - pre_buildkit_cache_bytes
combined_growth_bytes = image_growth_bytes + cache_growth_bytes

required_preflight_free_bytes =
max(6 GiB, 2 * rollback_image_size_bytes + 3 GiB)
```

其中增强阈值只适用于 rollback image 存在的 Branch A；postflight 也已要求 filesystem
free `>= 3 GiB`、final Dashboard image `<= 1 GiB`、combined growth `<= 3 GiB`、Swap delta
`<= 256 MiB` 与两个 30 秒 Swap sample 不持续增长。

但计划没有明确以下 terminal predicate：

```text
negative image/cache/combined growth -> must be explained and reconciled;
unexplained or parser/measurement-state-inconsistent negative growth -> HOLD;
negative growth must not be used as capacity credit.
```

在禁止 prune 的前提下，负增长仍可能来自 usage parser、scope、layer/accounting 或
measurement-state 变化。若不要求解释与前后 raw-byte 对账，`combined_growth_bytes` 可能
被异常负值压低，从而在 resource evidence 不可信时继续 startup，直接造成 false runtime
PASS。因此这是本轮唯一 blocker。

### R5 — Native ARM64 / build terminal: PASS

Runtime plan Phase G/H 要求实际 Raspberry Pi host architecture、Docker architecture、final
image OS/architecture/variant 均实际记录为 `linux/arm64/v8`，同时记录
`node:22.23.0-bookworm-slim` RepoDigest/base image ID、final image ID/RepoTags/size、source
release、build timestamps、exit code 与 bounded logs。

build failure、timeout、OOM、non-zero exit 或 incomplete image 都是 terminal stop；failure
后禁止 startup，也禁止 host `node_modules`/`.next`、macOS build、不同 Node image、临时
Dockerfile/Compose override、错误 API origin、root runtime 或其他 fallback。static review、
lockfile 或 registry description 不会被当作 native ARM64 proof。

### R6 — Dashboard-only startup / core non-impact: PASS

Phase I 唯一 startup predicate 是：

```text
docker compose up -d --no-deps dashboard
```

计划禁止 `docker compose down`、full-stack `up -d --build`、volume recreate/delete 与
API/PostgreSQL/Collector/Grafana/V-PLC rebuild。启动前置条件要求 core baseline 已冻结；
启动前后比较 container ID、image ID、`StartedAt`、`RestartCount`、health/running state
以及 project/network/container identity，名称相同不会替代 identity proof。

### R7 — 120-second process terminal: PASS

Phase J 使用统一 predicate：

```text
RestartCount >= 5 -> FAIL
```

同时覆盖 120 秒未 healthy、持续 restarting/unhealthy、crash-loop、log-loop 与
request/retry storm。触发失败后必须执行 `docker compose stop dashboard`，并证明 Dashboard
不再 running、restarting 或持续 unhealthy，bounded logs 停止增长且没有持续 API
request/retry storm。stop 失败或终局无法证明时为 `HOLD`，不得进入 Case/data evidence。

### R8 — API-unavailable reliability boundary: PASS

Phase K 明确分离 Dashboard process health、API health、PostgreSQL readiness、accepted-events
API data 与 page rendering。API-unavailable drill 必须独立、bounded、PM separately authorized；
未授权时只能 `NOT VERIFIED`。

未来 drill 要证明 API unavailable、Dashboard `/health` 仍 healthy、page fail closed、不展示
stale production truth、同一 render 不 retry、API failure 不重启 Dashboard，恢复只由新的
browser/page request 触发，并用 bounded request/log evidence 证明 request/retry count。

### R9 — Branch A rollback safety: PASS

Phase O 要求 build 前冻结 old release files、old Compose、old image identity/tag、resolved
Compose config、old service/container/image baseline、old `3001` state 与 protected-path
proof。rollback 先恢复 approved old files/image，执行 `docker compose config --quiet`，再以
Dashboard-only `--force-recreate` 恢复，验证 Dashboard `/health`、一次 bounded accepted-events
request、core identity/non-impact 与 `data/`/remote `.env` protection。

缺 mandatory asset 或 terminal evidence 即 `HOLD`。rollback 禁止 `docker compose down`、
volume/data restore、DB migration rollback、image/cache prune、core rebuild、停止未知
listener、改 port/firewall。

### R10 — Branch B first-deployment cancellation: PASS

Phase O 要求按顺序 stop Dashboard、remove Dashboard container only、恢复 pre-deployment
Compose/release files、执行 `docker compose config --quiet`，然后证明 Dashboard container
absent、`3001` no longer listening、core baseline unchanged、core healthy、core 未重建，
且 `data/` 与 remote `.env` 未覆盖/删除/初始化。

终局严格为：

```text
first-deployment cancellation / existing-core-services non-impact PASS
或 HOLD
```

不得声明 Dashboard rollback PASS、Dashboard health PASS、accepted-events PASS 或 Case A/B/C
PASS。命令 allowlist 也只允许 Branch B 使用 `docker compose rm -sf dashboard`。

## 5. Blockers

### B-R4-1 — Negative resource growth lacks a fail-closed adjudication

Architecture planning report 的 Phase E/H 需要补充：每个 pre/post usage counter 的 raw bytes
来源、scope、timestamp 与 parser/accounting identity；若 `image_growth_bytes`、
`cache_growth_bytes` 或 `combined_growth_bytes` 为负，必须记录可复核原因并完成前后
状态对账；任何负增长无法解释、单位/scope 不一致或 raw counter 无法复核时，必须在
startup 前 `HOLD`，不得将负值当作可用容量或冲抵其他增长。

这不是要求通用跨版本容量模型、长期 telemetry、签名或 tamper-resistant evidence；只是
当前单次 gate 所需的 resource terminal predicate。

### Minimal Architecture planning repair allowlist

仅需 PM 批准后修改：

- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`
  - Phase E — DockerRootDir/filesystem/image/cache/memory/Swap preflight
  - Phase H — build postflight 与 image identity
  - 必要时同步 Phase P 的 overall PASS/HOLD adjudication wording

本 Reliability Thread 不自行修复，不修改 `docs/deployment/raspberry_pi.md`，不进入 runtime
execution，也不运行 tests/build/Docker/Compose/SSH/API/DB/browser/rollback/cancellation。

## 6. Recommendations

以下不改变当前 `HOLD`，并在 B-R4-1 修复后作为 carry-forward：

1. 为 rollback bounded accepted-events request、first-deployment cancellation 后的
   `3001 released / no listener`、core baseline comparison 与 startup failure 增加固定
   command/result record 模板。
2. 在 future docs-repair lane 中继续把 `docs/deployment/raspberry_pi.md` 的通用 full-stack
   `up`/`down` 命令与 Dashboard-only path 做更醒目的 operator separation；当前 planning
   report 的 forbidden list 与 Section 10 boundary 已足以 fail closed，因此不构成本轮 blocker。
3. Runtime execution 仍需 separately record resolved base digest、final image identity/size、
   actual `linux/arm64/v8`、bytes pre/post metrics、`RestartCount`、bounded logs 与 terminal
   proof；static/local evidence 不得升级为 deployed/native/runtime evidence。

## 7. Terminal predicate audit

| boundary | current result |
| --- | --- |
| Branch A missing/inconsistent rollback asset | `HOLD` |
| Branch B ambiguity | `HOLD` |
| unknown `3001` listener owner | `HOLD` |
| unknown firewall boundary | `HOLD` |
| required bytes/parser/metric unavailable | `HOLD` |
| unexplained negative growth | **not specified — blocker** |
| native architecture/build failure | terminal stop; no startup |
| `RestartCount >= 5` | `FAIL` |
| sustained restart/unhealthy/log/retry storm | `FAIL` + stop |
| stop/terminal proof failure | `HOLD` |
| missing rollback/cancellation evidence | `HOLD` |
| static/process evidence used as API/DB/data PASS | forbidden |

## 8. Protected-path audit

**PASS subject to B-R4-1 repair.** The plan protects `/opt/edge-mes-demo/data/`, remote
`.env`, existing DB volume/bind data, rollback release/image and core runtime identity; release
source is committed `HEAD`; transport excludes generated/secret paths and forbids destructive
sync. No current planning text authorizes overwriting, deleting or recreating protected objects.

## 9. Native ARM64 / build terminal audit

**PASS.** Host, Docker and final image architecture must all independently equal
`linux/arm64/v8`; base digest/ID and final image identity/size/timestamps/exit code are retained.
Build failure, timeout, OOM, non-zero exit or incomplete image stops the sequence before startup;
fallback artifacts and temporary overrides are forbidden.

## 10. Process / restart terminal audit

**PASS.** The plan uses exact `RestartCount >= 5`, bounded 120-second observation, local-only
Dashboard `/health`, bounded logs, explicit `docker compose stop dashboard`, and terminal proof of
stopped/non-restarting/non-sustained-unhealthy/no retry storm. `/health` is not promoted to API/DB/data
health.

## 11. Rollback / cancellation audit

**PASS subject to B-R4-1 repair.** Branch A requires complete old release/image/Compose/baseline
assets and post-rollback health plus one bounded accepted-events request. Branch B is cancellation
only and requires Dashboard removal, `3001` release, restored pre-deployment config, core
non-impact and protected-path proof. Neither path uses `down`, volume deletion, data restore, prune,
core rebuild or unknown listener termination.

## 12. Scope-control audit

**PASS.** The review stayed within Reliability planning scope and did not reopen old Dashboard URL
Option C/strong-audit work. No manifest root identity expansion, D7/D8 relation matrix, retained
archive uniqueness, generic tamper-resistant evidence subsystem or superseded executable literals
was introduced. Data Quality field semantics were referenced only as an evidence boundary; no new
DQ requirements were added.

## 13. Evidence and validation

- checks performed: read-only Git recovery; authority/code/docs reading in the requested order;
  static cross-reference of R1–R10; report-only whitespace/conflict-marker check after creation。
- tests/build/typecheck: not run
- Docker/Compose/SSH/Raspberry Pi/port/firewall/resource/API/DB/browser/rollback/cancellation:
  not run
- allowlist compliance: exactly one authorized report created; no existing file changed
- staged files: none; cached diff remained empty

## 14. Overall conclusion and next gate

**HOLD — B-R4-1 must be repaired and re-reviewed before the next planning gate.**

Eligible for:

- Architecture planning repair only after PM approval;
- Reliability focused planning re-review after the minimal repair.

PM approval is required before Data Quality/Verification planning review, any implementation or
deployment-doc repair, Docker/Compose, SSH/Raspberry Pi, port/firewall/resource inspection,
API-unavailable drill, PostgreSQL query, real Case A/B/C, rollback/cancellation, or Git write.

## 15. Thread context assessment

- 本次输出长度：长；阻断点与最小 repair allowlist 已写入本报告。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：本轮 Reliability planning review 发现一个需 Architecture 最小修复的 resource
  terminal blocker；修复必须与本 Thread、已关闭 Gate B static implementation、旧 Dashboard
  URL strong-audit 分支及后续 runtime execution 隔离。
