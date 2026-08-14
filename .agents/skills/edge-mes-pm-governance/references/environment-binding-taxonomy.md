# Environment Binding Taxonomy

## Classification vocabulary

| Class | Meaning and boundary |
| --- | --- |
| `PRODUCT_DEFECT` | 已有充分 current product/runtime evidence 证明产品行为不满足 contract |
| `CONTRACT_DEFECT` | accepted route/schema/contract 与实际声明不一致，且问题在 contract layer |
| `CONTROLLER_VERIFIER_DEFECT` | verifier/controller predicate、identity check 或 gate literal 错误导致 false HOLD/PASS |
| `TASK_PACKAGE_MATERIALIZATION_DEFECT` | task/transaction/fixture materialization 的 bytes、shape 或 syntax 在执行前错误 |
| `AUTHORITY_VIOLATION` | frozen authority、lock、budget、retry 或 successor boundary 被越过 |
| `ENVIRONMENT_BINDING_OR_CAPABILITY_DENIAL` | local venue、tool binding 或 capability 阻止 action，尚未证明 product/remote defect |
| `REMOTE_RUNTIME_DEFECT` | remote/runtime object 有充分 identity 与 execution evidence 后仍不满足 runtime invariant |
| `READINESS_RACE` | readiness wait/transport evidence 不足或 timing predicate 造成错误 terminal |
| `OWNERSHIP_VERIFIER_FALSE_NEGATIVE` | owned object 存在足够 provenance，但 verifier 使用不稳定 predicate fail-closed |
| `UNAUTHORIZED_MUTATION` | 实际写入、删除、signal 或修改越出 exact allowlist |
| `EVIDENCE_INSUFFICIENCY` | claim 所需的 identity、transport、counter 或 source evidence 不足 |
| `HISTORICAL_STATE_ONLY` | 只存在历史事实，不能作为 current retry 或 successor authority |

分类必须附带事实、claim、authority consumption、first terminal 与 next gate；只写一个类别名称
不足以建立 PASS。

## Local root and effective write target

先证明 physical `cwd` 与 Git top-level 等于 task project root，再解析 repository-relative path。
每个 write 都要证明 effective resolved target 精确属于 task allowlist；`..`、glob、directory
replacement、同名路径或不明 workspace base 都不能替代 proof。actual out-of-allowlist write 是
真实 `UNAUTHORIZED_MUTATION` 和 HOLD，即使工具本身报告成功或对象看起来无害。

## Cross-environment binding

缺失 Devspace、workspaceId 或 environment-specific editing primitive，在 Codex Local 场景中若
local checkout/root/target 已证明且没有 mutation，不是 repository drift；应分类为
`ENVIRONMENT_BINDING_OR_CAPABILITY_DENIAL` 或 non-blocking tool assumption，并选择可证明的
local primitive。不能因为外部工具不可用而猜测 target，也不能把 task 转换成另一种 workspace。

一旦发生实际 stray/out-of-allowlist write，不能降级为工具问题、silent cleanup 或 retry；必须
按 `UNAUTHORIZED_MUTATION` 立即 terminalize，cleanup 需要新的 exact absolute-path authority。

本地 SSH 在 remote shell/auth 之前出现 `EPERM`，只证明 local execution venue 的 capability
boundary；在没有 remote shell evidence 前，不得归因 Pi、SSH key、remote port、Docker、API 或
product。历史成功也不能替代 current reachability。

## No silent cross-class repair

不同 taxonomy class 之间不得自动 repair、retry、fallback 或改写 claim。例如 controller
verifier defect 不自动变成 product source change，readiness race 不自动变成 runtime repair，
evidence insufficiency 不自动以 synthetic fact 填充，historical state 不自动成为 current
authority。需要跨类动作时，停止并要求新的 exact authority。
