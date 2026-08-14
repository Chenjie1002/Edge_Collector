# Execution Lock and Budget

## Pre-authority local repair window

repair window 默认 `not authorized`。只有当前 task 明确授权时才可使用，通常最多两个 bounded
cycles；每个 cycle 是 exact task-owned local edit set 加完整 local validation。它只能修复机械
格式、路径引用、schema shape、heading 或 fixture duplicate 等不改变 product、authority、
allowlist、budget、retry、stop condition 或 evidence claim 的 defect。

在任何 external/remote/network、runtime、DB/API、Docker/HTTP、Git mutation、signal、cleanup
或 production-data action 前必须结束 repair window。到达 lock 后不允许再 repair；超出预算
直接 HOLD，不能自创第三个 cycle。

## Lock fields

`EXECUTION_LOCK` 至少冻结：

- task/Goal、Owner approval、authority inputs 及其 exact identities；
- physical root、Git baseline、output prestate、process/port prestate；
- final helper/artifact bytes 与 SHA-256，以及完整 local validation 结果；
- repair-cycle count 和每次 mechanical change 摘要；
- exact read/write/runtime surface、external call budget、mutation budget；
- invocation/start/retry/cleanup/signal semantics、first-terminal rule、stop conditions 与 next gate。

本 Skill materialization 任务无 external execution lock；它在 local validation 后使用
`LOCAL_CANDIDATE_FREEZE`，冻结八个文件的 identity、exact membership、explicit-only policy 和
repair count。

## Post-lock immutability

锁后 authority-bearing fields、helper/artifact 内容、budget、retry、target、port、ownership
predicate 与 cleanup boundary 都 immutable。任何 failure 都是当前 attempt 的 terminal；不得
换 worktree、换 port、重连、fallback、重跑或提高预算。新的 attempt 必须由新的 exact authority
独立 materialize。

## Counter semantics

| Counter/fact | Counts | Does not prove |
| --- | --- | --- |
| `invocation` | 一次命令/runner/attempt 被启动 | listener 或 result 已产生 |
| `start` | 一个目标进程的 start action | ownership 已证明 |
| `listener` | 观察到的 bound listener | invocation 未发生或 PID 属于当前 task |
| `result` | durable result/terminal 已产生 | result 正确或被接受 |
| `cleanup` | 一次 exact owned cleanup action | 可以 broad-clean 或 retry |

失败启动即使没有 listener 也消耗 invocation/start counter；没有 listener 不能抹掉一次
authority consumption。每个 counter 要与 raw fact、normalized fact 和 terminal snapshot 分开。

## Ownership and cleanup

cleanup 只能针对当前 authority 明确允许、且通过 exact PID/对象 identity、executable、cwd、
launch continuity 和 unique listener 等 frozen predicates 证明归属的对象。unknown、foreign、
ambiguous 或仅由 port 推断的 process 必须拒绝 signal、kill、delete、overwrite 或 adopt。精确
cleanup 需要 exact target authority；它不能顺带清理 parent directory、同名对象或其他 listener。

## Canonical unordered discovery

当 claim 是 set membership 或 object identity 时，先保留 raw observation，再以稳定 key 做 sorted
unique canonicalization。container 用 service/full ID，mount 用 type/source/destination/flag，
path、tag、sidecar 用完整字符串，JSON object 按 key 排序但保留 array order。raw order 差异本身
不是 drift；duplicate key、missing/additional object 或 canonical field difference 仍可构成 HOLD。

## Local and remote identity separation

同 basename 的 local path 与 remote/deployed path 是不同对象。各自分别记录 bytes、SHA-256、
type、ownership、mode、topology role 和 authority source；local hash 不是 remote expected hash。
没有 accepted local-to-remote equality，就不能把 commit identity 当作 remote identity。
