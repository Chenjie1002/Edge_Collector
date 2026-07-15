# Sprint 3 Dashboard Raspberry Pi Runtime Deployment Evidence Reliability Re-review

报告名称：

`Sprint 3 Dashboard Raspberry Pi Runtime Deployment Evidence Reliability Re-review`

任务名称：

`Gate B — Negative Resource Growth Fail-closed Reliability Focused Re-review`

执行 Thread：

`Reliability`

## 1. 结论

**PASS**

`B-R4-1 CLOSED`

`Reliability planning gate: CLOSED / PASS`

`eligible for: Data Quality focused planning review`

本结论仅关闭 `B-R4-1` 的 Reliability planning blocker，不表示 Docker、Compose、Raspberry
Pi、ARM64、runtime、API/DB、rollback、cancellation 或真实 Case A/B/C 已执行或通过。

## 2. Reviewed baseline

- project: `/Users/chenjie/Documents/MES/edge-mes-demo`
- branch: `main`
- live `HEAD`: `29f02599447e4510209cd0ad419f70539f034507`
- live `origin/main`: `29f02599447e4510209cd0ad419f70539f034507`
- ahead/behind: `0 0`
- cached diff: empty
- recovery 时 Architecture planning report 与原 Reliability review 均存在且为既有
  untracked authority inputs。
- proposed re-review report 在 recovery 时不存在。

已知 `M .gitignore`、`frontend/.next/`、`frontend/node_modules/`、
`frontend/next-env.d.ts`、`frontend/tsconfig.tsbuildinfo`、历史 reports/handoffs 与
Keynote artifacts 均按授权作为 external/generated artifacts 保留，未删除、clean、restore、
整理、修改、stage、commit 或 push。

## 3. Exact re-review scope

本轮只复核 `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`
中对 `B-R4-1` 的 negative image/cache growth fail-closed repair，按 `RR1–RR6` 逐项核对。

Authority 阅读顺序已遵守：

1. `docs/thread_handoff/pm_operating_rules.md`
2. `docs/thread_handoff/reliability.md`
3. `docs/thread_handoff/chatgpt_pm_handoff_260715-0920.md`
4. `docs/current_status.md`
5. `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_gate_status.md`
6. `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_review.md`
7. `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`

原 Reliability review 的已 PASS `R1–R3`、`R5–R10` 不重新审查；本轮未新增 assurance
scope，也未把原三项 Recommendations 作为当前 gate 条件。

## 4. Scope and allowlist compliance

### Reviewed files

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/reliability.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260715-0920.md`
- `docs/current_status.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_docker_integration_gate_status.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_review.md`
- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_plan.md`

### Created file

- `docs/reports/sprint3_dashboard_raspberry_pi_runtime_deployment_evidence_reliability_rereview.md`

### Changed existing files

- none

### Explicitly not touched

- Architecture planning report、原 Reliability review、deployment guide、current status、Gate B
  status、PM handoff、PM operating rules；
- Compose、Dockerfile、frontend/API/DB/Collector/Grafana/V-PLC、`.gitignore`；
- 任何历史、生成或 external artifacts；
- staged、committed、pushed Git state。

## 5. B-R4-1 re-review: RR1–RR6

### RR1 — Raw counters: PASS

Architecture plan Phase E 保留并区分以下四个 raw byte counters：

```text
pre_image_usage_bytes
post_image_usage_bytes
pre_buildkit_cache_bytes
post_buildkit_cache_bytes
```

并明确：

```text
raw_image_delta_bytes = post_image_usage_bytes - pre_image_usage_bytes
raw_cache_delta_bytes = post_buildkit_cache_bytes - pre_buildkit_cache_bytes
```

Phase H 要求重新取得相同的 post counters，并保留原始 pre/post bytes、raw deltas 与状态
对账记录。

### RR2 — Measurement identity: PASS

Phase E/H 冻结并复用同一：

```text
command/source
metric scope
unit
parser/accounting method
Docker daemon/context
relevant timestamps
```

任一 raw counter、单位、scope、parser/accounting identity、Docker context 或 relevant
timestamp 无法可靠核对时，明确要求在 startup 前 `HOLD`。计划没有引入通用 measurement
framework、签名、长期 telemetry 或新工具要求。

### RR3 — Negative delta reconciliation: PASS

任一 raw delta `< 0` 时，计划要求保存原始 pre/post bytes、记录可复核原因，并完成前后
measurement-state 对账。无法解释或无法完成对账，或 measurement identity 不一致时，在
startup 前 `HOLD`。

计划同时明确：

- 负值不得作为 capacity credit；
- 负 image delta 不得抵消 cache growth；
- 负 cache delta 不得抵消 image growth。

### RR4 — Conservative effective growth: PASS

计划明确使用：

```text
effective_image_growth_bytes = max(0, raw_image_delta_bytes)
effective_cache_growth_bytes = max(0, raw_cache_delta_bytes)
combined_growth_bytes = effective_image_growth_bytes + effective_cache_growth_bytes
```

即使负 delta 有合理且可复核原因，也只能按对应 effective growth `0` 进入 terminal
calculation。

### RR5 — Existing thresholds preserved: PASS

repair 未改变既有 resource terminal：

```text
combined_growth_bytes <= 3 GiB
relevant filesystem free >= 3 GiB
final Dashboard image size <= 1 GiB
Swap delta <= 256 MiB
two 30-second Swap samples not continuously increasing
```

原有 preflight free-space thresholds 仍保留：project filesystem free `>= 6 GiB`、
DockerRootDir filesystem free `>= 6 GiB`；存在 rollback image 时，DockerRootDir free 仍须
满足 `max(6 GiB, 2 * rollback_image_size_bytes + 3 GiB)`。required metric 或算式无法可靠
完成时为 `HOLD`。

### RR6 — Phase consistency: PASS

- Phase E 定义 raw counters、raw deltas、negative reconciliation 与 effective growth；
- Phase H 使用同一 measurement identity，保留 pre/post/raw/effective 计算，并在 startup
  前对 unreconciled negative delta `HOLD`；
- Phase P 重申负值、无法解释或无法完成状态对账均为 startup 前 `HOLD`，且 terminal
  calculation 只能使用两个非负 `effective_*_growth_bytes`；
- Phase P 明确任一 mandatory phase 为 `HOLD` 时，overall 不得 `PASS`；
- 本次 repair 只收紧 `B-R4-1`，未与原 Reliability review 已 PASS 的 `R1–R3`、`R5–R10`
  结论冲突。

## 6. B-R4-1 closure decision

`B-R4-1 CLOSED`。

Architecture plan 现在同时具备 raw counter authority、measurement identity freeze、negative
delta reconciliation、conservative effective growth、原有 thresholds 与跨 Phase E/H/P 的
一致 terminal predicate；未发现新的 false-PASS 路径。

## 7. Evidence and validation

- checks run:
  - read-only Git recovery；
  - 指定 authority/report 顺序的静态阅读；
  - Architecture plan Phase E/H/P 与原 Reliability `B-R4-1` 的 focused static cross-reference；
  - 新 report conflict-marker check；
  - 新 report `git diff --no-index --check /dev/null <file>` whitespace check。
- tests/typecheck/build: not run
- Docker/Compose/SSH/Raspberry Pi/port/firewall/resource/API/DB/browser/rollback/cancellation:
  not run
- allowlist compliance: exactly one new report created；no existing file changed
- staged files: none；cached diff remained empty

## 8. Blockers

- none

## 9. Recommendations

- none

原 Reliability review 的 fixed command/result templates、deployment guide operator separation
与 runtime evidence detail recommendations 不属于本轮 `B-R4-1` closure 条件，按 PM 分类留给
后续独立 gate，不携带为当前 blocker 或 recommendation。

## 10. Overall conclusion and next gate

**PASS — Reliability planning gate: CLOSED / PASS**

Eligible for：

- `Data Quality focused planning review`

不得自行启动下一 gate；等待 PM intake。任何 implementation/docs repair、runtime、Docker、
Compose、SSH/Pi、API/DB、tests/build 或 Git stage/commit/push 仍需独立授权。

## 11. Thread context assessment

- 本次输出长度：中；focused re-review 结论已写入本 report。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：原 Reliability review 已产生 `HOLD`，本轮只完成 Architecture 最小 repair 的独立
  Reliability re-review；下一 gate 应与本 Thread、Architecture repair Thread、已 PASS 的
  Gate B static implementation、旧 Dashboard URL Option C/strong-audit 分支保持隔离。
