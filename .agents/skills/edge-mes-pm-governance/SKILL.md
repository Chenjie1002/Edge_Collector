---
name: edge-mes-pm-governance
description: Use when explicitly invoked for Edge MES PM takeover, Goal/task packaging, authority reconciliation, Verification packaging, historical governance incident classification, or PM handoff.
---

# Edge MES PM Governance

## 定位

`docs/thread_handoff/pm_operating_rules.md` 是更高层的 durable governance authority。本 Skill
只是把现有规则应用到 Edge MES PM、Goal、task、Verification 和 handoff 工作的可复用 procedure，
不是第二套 PM Rules，也不能产生 Owner approval、Goal authority、runtime authority 或 production
truth。

本 Skill 仅提供 instructions 与 references；没有 executable command catalog、scripts 或隐含的
执行入口。

## Invocation

仅在用户或上层 task 明确选择/提及本 Skill 时使用。没有 explicit invocation 时，本 Skill 必须
保持不激活；不能因项目文件名、关键词、历史上下文或 conversation momentum 自行启动。显式
选择也不能补发缺失的 Owner approval 或扩大 task allowlist。

## 稳定 procedure

按当前 task 的实际 authority 执行以下高层顺序，并在第一个 decisive terminal 停止：

1. 确认 current authority、authority class、Owner approval 与唯一 next gate；
2. 分离 current facts、historical facts 与 immutable terminal，禁止用历史摘要替代 live fact；
3. 取得 fresh root、Git、output prestate 和其他 task 声明的 baseline；
4. 物化 bounded objective、accepted inputs、exact allowlist、outputs 与 exceptions；
5. 在必要的 local validation 通过后冻结 execution lock、budget、retry 和 cleanup semantics；
6. 保留 first decisive terminal，区分事实、claim、Parent Evidence、Verification 与 intake；
7. 只通过 exact durable handoff 交给下一授权边界，不自动继承 successor authority。

## 动态事实

objective、accepted inputs、task/Goal identities、mutation/runtime surface、budgets、retry
semantics、expected outputs、exceptions、Owner approval、evidence class、current gate 和 next
gate 都必须由当前 task/Goal 明确提供。不可从 memory、历史相似任务、旧 report 或默认值补齐；
缺项会阻止安全执行，按 task 的 HOLD 规则处理。

## Reference routing

按请求域加载最小 reference：

| 请求域 | Reference |
| --- | --- |
| authority、current/history、terminal、successor | `references/authority-state-machine.md` |
| lock、budget、counter、retry、ownership、identity | `references/execution-lock-and-budget.md` |
| task 16-section、root、allowlist、output、handoff | `references/task-materialization-contract.md` |
| Parent Evidence、Verification、Mainline intake、evidence class | `references/verification-contract.md` |
| local/remote binding、capability denial、defect taxonomy | `references/environment-binding-taxonomy.md` |
| historical regression classification 与 frozen fixtures | `references/regression-fixtures.md` |

Reference 是 procedure 的 supporting material，不会授权读取未 allowlisted 的 historical
corpus，也不会把其中的事实变成当前 runtime 或 production authority。

## Hard refusals

- task/authority identity、root、type、output prestate 或 exact target 不匹配时 fail closed；
- explicit invocation 缺失时不激活；Owner-only approval 不得推断；
- execution lock 后不得 repair、retry、reconnect、fallback 或增加 budget，除非新的 exact
  authority 明确开启 successor attempt；
- historical PASS/HOLD、later healthy observation 或 composite sub-result 不得改写历史 terminal；
- unknown/foreign/ambiguous process 不得 signal、cleanup、overwrite 或 adopt；
- broad filesystem cleanup、未知 PID action、隐含 successor、runtime retry 和证据升级均拒绝；
- local/static/synthetic evidence 不得升级为 remote、runtime、DB-backed 或 production claim。

## State separation and handoff

以下状态必须逐一记录，任何一个都不蕴含另一个：

`WRITTEN / REVIEWED / ACCEPTED / VERIFIED / STAGED / COMMITTED / PUSHED / DEPLOYED / ACTIVATED / RUNTIME_LOADED / PRODUCTION_ACCEPTED / OWNER_VISUAL_ACCEPTED`

窗口输出只给 concise manifest，包含 report identity、changed paths、checks、allowlist、Git
state、blockers、recommendations 和唯一 next gate；durable report 必须由接收方重新读取实际
文件。完成 candidate 或 report 后停止，等待独立 intake；不得把本 Skill 的自检写成 acceptance。
