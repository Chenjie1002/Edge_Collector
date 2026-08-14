# Task Materialization Contract

## Repository-backed 16-section discipline

每个新 task 必须是一个唯一 repository-backed authority record，按固定顺序包含：

1. report identity；
2. task identity；
3. executing Thread；
4. project/root convention 与 PM workload/sub-agent assessment；
5. delivery mode 与 exact output authority；
6. authority source/ID；
7. required reading order；
8. fresh recovery/live facts；
9. current gate/authority boundary；
10. exact task scope/execution steps；
11. read/write/runtime/Git/remote allowlist 与 budgets；
12. explicit exclusions/forbidden operations；
13. PASS/HOLD/stop criteria；
14. validation/evidence；
15. window manifest format；
16. single next gate/non-inheritance statement。

task file 是 first required reading。执行 Thread 必须先机械核验 exact path、regular/non-symlink、
bytes、SHA-256，再读取其他 repository content 或执行 task action。launcher 只是指针，不能扩张、
缩减、摘要替代或重新发布 authority；launcher mismatch 必须 HOLD。

## Root and repository-relative paths

task 只在 dedicated project-root field 声明 absolute root；其余 repository-internal paths 使用
relative path。解析第一个 relative path 或 mutation 前，read-only 证明 physical `cwd` 与
`git rev-parse --show-toplevel` 都等于该 root。禁止 `..`、traversal、glob write target、
directory-level replacement 和 inferred output path。

每次 write 的 effective target 必须机械等于一个 exact allowlisted path。若 mutation primitive
的 base 不可证明，停止并 HOLD；不能用模糊 redirection、temporary patch、sidecar 或 convenience
workspace 代替 target proof。

## Allowlist and dynamic Goal/task facts

task 必须分别冻结 read、write、runtime、remote、network、DB/API、process/signal、cleanup 和
Git allowlist；任何未列出的 command/action 都不因“验证需要”自动获得权限。dynamic facts 至少
包括：

- objective 与要证明的 terminal claim；
- accepted inputs、source/report identities、current/historical boundaries；
- task/Goal/object、root、remote/runtime object 的 type、bytes、hash 与 ownership；
- exact mutation/runtime surface；
- archive、SSH、HTTP、process-start、retry、cleanup、signal、Git 等 budgets；
- invocation 计数、retry 语义、lock 后 rule 与 first decisive terminal；
- exact report/artifact outputs、schema、prestate 与异常路径；
- Owner approval text、authority ID、target、budget、stop conditions；
- evidence class：local/static/synthetic、remote/runtime、DB 或 production；
- current gate、handoff receiver 与唯一 next gate。

Skill 可以检查字段存在和形状，但不能从历史相似度、memory 或默认值填充缺失事实。

## Output prestate and changed-path accounting

首次写入前逐项证明 exact output 为 absent/non-symlink，或按 task 明确的 existing-state contract
处理；意外 pre-existing、wrong type 或 symlink 是 HOLD。只允许 task 声明的最小 parent
directories。首写后立即审计 exact changed-path set，保留 pre-existing dirty/untracked paths，
不 broad clean、adopt、stage 或删除以制造干净证据。

report、artifact、helper、fixture、manifest、script 和 sidecar 都必须有显式 exact path；没有
声明的第二个 report 或辅助文件不属于“方便的输出”。最终 identity 计算后，任何 candidate 内容
变化都必须消耗 task 明确授权的 repair cycle 并重跑完整 validation；报告写入后通常不可 repair。

## Sub-agent boundary

task 必须声明是否建议 sub-agent、exact independently delegable scope 或 `none`、理由和整合
责任。sub-agent 不继承 task 之外的 authority，不得自行创建 child-of-child、扩展 allowlist、
写非授权路径、stage/commit/push 或替代 parent/Mainline intake。没有明确授权时不调用 sub-agent。

## Durable report and state separation

durable report 只在 candidate/local validation terminalize 后写入 exact path。它必须记录 authority
identities、prestate、created scaffold、membership、每个文件 identity、checks、repair count、
changed-path audit、external action counters、MVP alignment 和 single next gate。

写 report 只建立 `WRITTEN` 或 task 声明的 `MATERIALIZED_CANDIDATE`；不建立 `REVIEWED`、
`ACCEPTED`、`VERIFIED`、`STAGED`、`COMMITTED`、`PUSHED`、`DEPLOYED`、`ACTIVATED`、
`PRODUCTION_ACCEPTED` 或 `OWNER_VISUAL_ACCEPTED`。接收方必须读取实际 durable file，而不是只信聊天摘要。
