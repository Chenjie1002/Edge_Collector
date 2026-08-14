# Authority State Machine

## Authority hierarchy and classes

权威按以下顺序解释，低层对象不能改写高层 policy 或当前 task：

1. `docs/thread_handoff/pm_operating_rules.md`：durable governance law；
2. 当前 repository-backed task/Goal 与 Owner 的 exact approval：本轮 objective、identity、
   allowlist、budget、exceptions、outputs 和 stop conditions；
3. 当前 handoff、Mainline intake 与已接受的 bounded facts：current context，不自动开启 successor；
4. historical report、ledger、charter 与 fixture：只提供 semantic input 和 immutable history；
5. Skill candidate：应用以上规则的 reusable procedure，不是新的 authority source。

按 authority class 区分：`AUTHORITY_HARD_GATE` 需要 exact path/type/bytes/SHA-256；
`PROTECTED_CONTINUITY` 需要 entry/final identity 不漂移；`HISTORICAL_OR_SEMANTIC_READ` 需要
exact path、regular/non-symlink 与 task-relevant fact，不因诊断性 hash 差异自动改变当前 gate。

## Current, historical and immutable facts

fresh live facts 可以更新 current repository/process baseline，但不能重写 historical terminal。
历史 `PASS`、`HOLD`、retry、counter、authority consumption 和 cleanup result 都是 immutable
records。later healthy observation 只能作为 later diagnostic fact；不能把 earlier failure 变成
成功，也不能抹掉一次已经发生的 invocation。

`accepted sub-result` 只接受它声明的边界。多个 accepted bounded facts 可以在一个新的
composite acceptance 中组合，但组合不重写任一历史 terminal，也不自动创建下一阶段 authority。

## State labels

| Label | Meaning | Does not imply |
| --- | --- | --- |
| `WRITTEN` | exact file 已写入 | review、acceptance 或 verification |
| `REVIEWED` | 独立 review 已完成 | Mainline acceptance 或 commit |
| `ACCEPTED` | 指定 intake 接受了声明边界 | verification、deploy 或 production |
| `VERIFIED` | 独立 Verification 通过 | Mainline acceptance 或 successor |
| `STAGED` | exact path 已进入 Git index | commit 或 push |
| `COMMITTED` | 已建立 commit | push、deploy 或 activation |
| `PUSHED` | 已发布到指定 remote | deploy、runtime load 或 production |
| `DEPLOYED` | 指定对象已部署 | loaded、healthy 或 accepted |
| `ACTIVATED` | 指定 runtime lifecycle 已激活 | production truth |
| `RUNTIME_LOADED` | evidence 证明指定 runtime 读取了对象 | production acceptance |
| `PRODUCTION_ACCEPTED` | 明确的 production gate 已通过 | visual acceptance |
| `OWNER_VISUAL_ACCEPTED` | Owner 明确接受 visual boundary | production truth 或其他 gate |

任何状态只能由它自己的 authority/evidence 建立。Skill self-check 只能证明 local/static
compliance，不得把状态向右侧或上层升级。

## First decisive terminal

在冻结 attempt 中，第一 decisive failure 或 HOLD 是当前 attempt 的 terminal。记录它的
authority、counter、input identity、事实/claim 分层与 stop condition。没有 fresh successor
authority 时，不得用 retry、reconnect、repair、fallback、later success 或“没有造成污染”
覆盖该 terminal。

## Successor non-inheritance and Owner approval

新的 Goal、task、attempt、cleanup、runtime、Git 或 phase 必须有自己的 exact authority。历史
task 的 unused-looking budget、旧 prompt、聊天意图或 composite PASS 都不是 successor approval。
Owner-only approval 必须以当前 authority 的明确文本、目标、budget 与 stop conditions 读取；
不能从“应该可以”“前一步通过”或文件存在推断。

## Composite acceptance

Parent Evidence、bounded sub-result、独立 Verification 和 Mainline intake 是不同对象。新的
Mainline composite acceptance 可以引用已接受的子结果，但必须保留每个子结果的 identity、
scope、consumed authority 与 historical terminal。组合结果不授予未声明的 successor、runtime、
production 或 visual authority。
