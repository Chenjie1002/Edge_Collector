# Verification Contract

## Parent Evidence freeze

Parent Evidence 必须冻结它实际使用的 authority/input identities、prestate、facts、claims、
counters、terminal、action audit 和 evidence class。每个 fact 要与 claim 分离：观察到的
HTTP、listener、文件或 process fact 不自动证明 product、runtime、DB 或 production claim。

Parent Evidence 是 controller 的 bounded record，不是 self-acceptance。冻结后不得用 mutable
Ledger、后来变更的 source 或 chat summary 追补其 final identity；reviewer 应能用 exact durable
files 重现 frozen input set。

## Independent Verification boundary

Verification 是一个独立、read-only、task-authorized 的 boundary，只检查 frozen Parent Evidence、
declared artifacts、identity、schema、counter、scope、action audit 和 claim sufficiency。除非另
一个独立 task 明确授权，Verification 不得重新运行 runner、runtime、HTTP、SSH、Docker、DB 或
cleanup，也不能因为“重跑更可靠”而消耗新的 authority。

mutable Ledger 可以作为诊断/过程记录，但不能成为最终 SHA race gate，也不能在 Parent Evidence
冻结后改变已冻结的事实。任何 Ledger 与 exact final artifact 的差异都要按 task contract 分类，
不能隐式刷新 terminal。

## Action audit and report identity

Verification report 必须保留：实际读取的 exact paths、每个 source/artifact 的 regular/type、
bytes、SHA-256、root proof、changed-path set、staged/Git state、external action counters、
repair/child count、结论与 next gate。没有 durable identity 的聊天摘录、attachment 或 temporary
path 不能成为跨 Thread evidence。

## Mainline independent intake

Mainline intake 必须从当前 checkout 重新打开实际 durable report/artifact，核对 report existence、
bytes、SHA-256、内容与 manifest 一致性、actual changed paths、allowlist、checks、Git state、
action counters 和 state separation。reported path/hash 或窗口摘要不能替代实际文件读取。

`Verification PASS` 只表示 Verification boundary 通过；不等于 `Mainline acceptance`，也不等于
Skill candidate accepted、runtime loaded、deployment、activation、production acceptance 或 visual
acceptance。每个升级都需要自己的 authority。

## Evidence class separation

| Evidence class | Can support | Cannot silently become |
| --- | --- | --- |
| local/static/synthetic | structure、identity、contract、fixture classification | remote/runtime/DB/production |
| remote read/runtime observation | declared remote/runtime fact | deployment acceptance 或 production truth |
| DB-backed accepted fact | declared data contract/lineage claim | UI/visual acceptance 或 unrelated KPI |
| production acceptance | only its exact accepted claim | visual acceptance 或 successor authority |
| Owner visual inspection | explicitly inspected visual boundary | data truth、runtime load 或 production acceptance |

Verification 应 fail closed 于 insufficiency、identity mismatch、scope expansion、unowned process、
unauthorized mutation 和 evidence-class confusion；diagnostic completeness 若不影响 false PASS 或
safety boundary，应保持 recommendation，不扩大当前 gate。
