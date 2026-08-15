# Edge MES Demo — ChatGPT PM Handoff — 260727-1207

## 1. Handoff purpose

本 handoff 由 ChatGPT PM 在 R17-R4 authority reconciliation 边界创建，用于消除以下 durable authority conflict：

```text
docs/thread_handoff/chatgpt_pm_handoff_260727-1138.md
Architecture / Integration next repair: NOT AUTHORIZED

vs.

later PM-issued R17-R4 / status-reconciliation prompts
```

此前两个 Architecture / Integration 执行窗口均正确按 authority-conflict stop rule 返回 `HOLD`，且没有执行任何任务写入。

本文件是当前最新 PM authority source。`chatgpt_pm_handoff_260727-1138.md` 继续作为历史 handoff 保留，但其 `Architecture / Integration next repair: NOT AUTHORIZED` 不再阻止本文件明确授权的 Level 0 status reconciliation。

## 2. Current PM decision

```text
R17-R3 Reliability:
HOLD / PM-ACCEPTED

R17-R4 first repair attempt:
HOLD / NO TASK WRITE
reason: docs/current_status.md authority conflict

R17-R4 status reconciliation first attempt:
HOLD / NO TASK WRITE
reason: chatgpt_pm_handoff_260727-1138.md authority conflict

PM authority handoff refresh:
WRITTEN

Architecture / Integration status reconciliation:
AUTHORIZED
Level: Level 0

R17-R4 source/test/manifest repair:
NOT AUTHORIZED UNTIL STATUS RECONCILIATION IS WRITTEN AND PM-ACCEPTED

Verification:
BLOCKED

Remote:
NOT AUTHORIZED

Third I1:
NOT AUTHORIZED

Git closeout:
NOT AUTHORIZED
```

## 3. Authorized next action

唯一授权的下一项任务是：

```text
D2-R7B-I1 R17-R4 Authority Status Reconciliation
```

执行 Thread：

```text
Architecture / Integration
```

风险等级：

```text
Level 0
```

Exact write allowlist：

```text
docs/current_status.md
docs/reports/sprint4_d2_r7b_i1_r17_r4_authority_status_reconciliation.md
```

该任务只允许：

- 在 `docs/current_status.md` 顶部增加新的当前 authority section；
- 保留旧的 0E section 作为历史状态；
- 写入 exact-path durable reconciliation report；
- 执行 local read-only Git/diff/content validation。

该任务不允许：

- 修改 R17-R4 source、test 或 manifest；
- Reliability、Data Quality 或 Verification review；
- SSH、Remote、Raspberry Pi、Docker、Compose；
- Collector restart、Collector activation、deployment、rollback；
- Third I1；
- Git stage、commit、push 或 tag；
- 修改 `.gitignore`、`pm_operating_rules.md` 或任何其他 PM handoff。

## 4. Expected durable status after reconciliation

新的 `docs/current_status.md` 顶部 section 必须明确记录：

```text
R17-R3 Reliability:
HOLD / PM-ACCEPTED

R17-R4 Architecture / Integration repair:
PM-PLANNED
NOT YET AUTHORIZED FOR SOURCE/TEST/MANIFEST EXECUTION

R17-R4 status reconciliation:
AUTHORIZED / WRITTEN（按任务最终状态）

previous R17-R4 attempts:
HOLD / NO TASK WRITE

Verification:
BLOCKED

Remote:
NOT AUTHORIZED

Third I1:
NOT AUTHORIZED

Git closeout:
NOT AUTHORIZED
```

注意：status reconciliation 的授权不等于 R17-R4 implementation authorization。只有 status reconciliation durable report 经 PM intake 并被明确接受后，PM 才可发布新的 R17-R4 Level 2 Architecture / Integration repair Prompt。

## 5. Required next sequence

```text
latest PM authority handoff WRITTEN
→ Architecture / Integration Level 0 status reconciliation
→ reconciliation report WRITTEN
→ PM durable report intake
→ PM explicit acceptance
→ new R17-R4 Level 2 Architecture / Integration repair Prompt
→ repair package WRITTEN
→ PM intake
→ fresh independent Reliability re-review
```

不得自动进入：

```text
R17-R4 implementation
Reliability
Verification
Remote
Third I1
Git closeout
```

## 6. Live repository baseline

Read-only recovery at handoff creation：

```text
project: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 8de5edbb504538a233abbcc80102cb714c9cee65
origin/main: 8de5edbb504538a233abbcc80102cb714c9cee65
ahead/behind: 0/0
cached: empty
git diff --check: PASS
```

Current tracked dirty boundary：

```text
M .gitignore
M docs/thread_handoff/pm_operating_rules.md
```

Classification：

```text
.gitignore:
pre-existing external dirty artifact
must not stage or modify

docs/thread_handoff/pm_operating_rules.md:
PM-authorized governance update
pre-existing
not committed
excluded from status reconciliation task
```

大量 pre-existing untracked reports、evidence、historical handoffs、management artifacts 和 frontend build artifacts 继续保持 external/excluded 状态。禁止 broad cleanup。

## 7. Authority precedence for the next task

下一项 status reconciliation task 应使用以下 authority order：

```text
live Git facts
→ docs/thread_handoff/pm_operating_rules.md
→ docs/thread_handoff/chatgpt_pm_handoff_260727-1207.md
→ exact task Prompt
→ docs/thread_handoff/chatgpt_pm_handoff_260727-1138.md as historical input
→ docs/current_status.md as the stale reconciliation target
```

对于本次 exact status reconciliation：

```text
chatgpt_pm_handoff_260727-1138.md 中的
Architecture / Integration next repair: NOT AUTHORIZED
```

是历史状态，不构成 blocker。

`docs/current_status.md` 中旧的：

```text
D2-R7B NOT AUTHORIZED FOR IMPLEMENTATION
```

是本任务已知的 stale status target，不构成 blocker；但不得删除历史内容，应通过新的顶部 authoritative section supersede。

任何超出本文件明确授权的 source、test、manifest、runtime、remote 或 Git action 仍必须 `HOLD`。

## 8. Current blockers

R17-R3 Reliability blockers继续开放：

```text
R7-A foreign inode deletion race
R7-B retry-failure terminal disposition
R9 final cleanup boundary coverage
```

本 handoff 不解决这些 blocker，也不声明 R17-R4 contract 已实施。

## 9. MVP-path classification

```text
MVP-ALIGNED
```

本 handoff 与下一项 status reconciliation 仅修复 durable authority source 冲突，不改变产品能力、runtime topology、threat model、data contract、remote deployment 或证据框架。

## 10. Copyable next ChatGPT PM recovery prompt

```text
你是 Edge MES Demo 项目的 ChatGPT PM。

项目：
/Users/chenjie/Documents/MES/edge-mes-demo

必须先读取：
- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260727-1207.md
- docs/thread_handoff/chatgpt_pm_handoff_260727-1138.md
- docs/current_status.md

先执行 read-only Git recovery。

恢复后确认：
- R17-R3 Reliability HOLD / PM-ACCEPTED
- Level 0 status reconciliation AUTHORIZED
- R17-R4 source/test/manifest repair NOT AUTHORIZED
- Verification BLOCKED
- Remote NOT AUTHORIZED
- Third I1 NOT AUTHORIZED
- Git closeout NOT AUTHORIZED

下一步只允许发布或 intake exact status reconciliation task。
不要进入 R17-R4 implementation。
```

## 11. Handoff artifact status

本文件：

```text
WRITTEN
NOT STAGED
NOT COMMITTED
NOT PUSHED
```

`WRITTEN` 不表示 `ACCEPTED`、`VERIFIED`、`STAGED`、`COMMITTED`、`PUSHED`、`DEPLOYED` 或 `ACTIVATED`。

不得自动 stage。本文件的 Git stage/commit/push 需要用户另行明确 exact-path authorization。
