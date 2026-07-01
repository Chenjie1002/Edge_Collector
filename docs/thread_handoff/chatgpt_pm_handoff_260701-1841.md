# ChatGPT PM Handoff - 2026-07-01 18:41 UTC+8

## 1. Project path

`/Users/chenjie/Documents/MES/edge-mes-demo`

## 2. New PM first action

The next PM must start with read-only recovery. Do not continue implementation, tests, staging, commit or push before recovery and explicit PM authorization.

Run first:

    git status -sb
    printf '\n--- log -12 ---\n' && git log --oneline -12
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git show-ref --hash refs/remotes/origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only

## 3. Live Git baseline at handoff creation

    HEAD == origin/main == 11cf077889dcf528ce91995e0acf183b74c31540
    latest commit:
    11cf077 Freeze Sprint 3 production fact visibility boundary

Live Git facts are authoritative. Durable docs may contain historical authoring baselines such as `ed9a61e`, `1c15afd` or `9135011`; those are audit markers unless they conflict with current gate state, scope, allowlist or authorization boundary.

## 4. Current working tree external artifacts

These dirty / untracked artifacts are external history artifacts. Do not stage, commit, clean up or rewrite them unless the user explicitly authorizes exact paths.

    M .gitignore
    ?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
    ?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

Forbidden broad staging:

    git add .
    git add -A
    git add docs/

## 5. Current closed gate state

    Sprint 3 raw_policy station-level rollout checkpoint: CLOSED / PASS WITH RECOMMENDATIONS
    Sprint 3 post-raw_policy docs/status sync: CLOSED, commit 414c9a8
    Sprint 3 Slice J downstream planning-only gate: CLOSED / PASS WITH RECOMMENDATIONS
    Sprint 3 Slice J docs/contracts boundary freeze: CLOSED, commit c899e6e
    Sprint 3 Slice J Reliability docs boundary review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    Sprint 3 Slice J Data Quality docs boundary review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    Sprint 3 Slice J Verification docs boundary review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    PM handoff after Slice J boundary freeze: CLOSED, commit 14baabe
    Sprint 3 Slice J implementation planning: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    Sprint 3 Slice J tests-only implementation: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    Sprint 3 Slice J Reliability focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    Sprint 3 Slice J Data Quality focused implementation review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    Sprint 3 Slice J Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    Sprint 3 Slice J exact tests-only commit/push: PASS, commit ed9a61e
    Sprint 3 Slice J tests-only docs/status sync: CLOSED / PASS WITH RECOMMENDATIONS, commit 1c15afd
    PM handoff after Slice J tests-only sync: CLOSED, commit 9135011
    Sprint 3 accepted production-fact visibility boundary docs/contracts freeze: CLOSED / PASS WITH RECOMMENDATIONS
    Sprint 3 accepted production-fact visibility boundary Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    Sprint 3 accepted production-fact visibility boundary Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    Sprint 3 accepted production-fact visibility boundary Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    Sprint 3 production-fact visibility boundary exact docs/status/PM-rule commit/push: PASS, commit 11cf077

There is no pending review gate, commit gate or status sync gate at this handoff.

## 6. Latest commit contents

Commit `11cf077 Freeze Sprint 3 production fact visibility boundary` submitted and pushed:

    docs/contracts/collector_ingestion_adapter.md
    docs/current_status.md
    docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
    docs/reports/sprint3_collector_ingestion_adapter_plan.md
    docs/thread_handoff/pm_operating_rules.md

## 7. Production-fact visibility boundary summary

- Future production visibility is limited to accepted station-event business facts after immutable config authority, `raw_policy` / decoder authority, shared validation, duplicate/conflict checks and adapter decision `accepted`.
- Adapter disposition, reason code, candidate context and raw/normalized comparison context remain diagnostic/review/debug only.
- `raw_payload` / `raw_hex` is evidence, not a production fact; review-only/audit-only candidate only.
- Decoded/source normalized payloads remain candidates until accepted; non-accepted candidates stay diagnostic-only.
- Non-accepted dispositions do not write defect detail; NOK/detail visibility must bind to accepted upstream business evidence.
- DB/API/Dashboard schema/API/UI/DB work remains deferred.
- Future DB/API/Dashboard gate must restate exact allowlist, review gates and production-fact leakage negative tests.
- ACK/read_done ownership remains unchanged.
- Preserve: `no ACK/read_done mutation for the current non-accepted payload`.
- Future hardening backlog: duplicate/conflict precedence, historical config replay, exact-byte canonical fixture vectors, raw error taxonomy and production-fact leakage negative tests.

## 8. PM operating rules update summary

`docs/thread_handoff/pm_operating_rules.md` now requires Thread prompt bodies to be returned as one complete copyable Markdown block.

PM may write intake, judgment or explanation before or after the prompt, but the Thread prompt body itself must remain a single copyable Markdown block so the user can copy it directly into the target Thread.

## 9. Non-authorized surfaces

The following remain unauthorized unless the user explicitly grants a separate exact-path task:

    tests
    implementation
    config/mapping.yaml
    raw_required
    line-wide runtime_defaults.raw_policy
    storage.py
    DB schema / migration / DB write path
    FastAPI / API
    Dashboard / frontend / Trace UI
    V-PLC behavior
    Docker / deploy
    ACK/read_done ownership
    real PLC pilot
    tag
    rollback
    stage / commit / push without explicit exact-path authorization
    external dirty artifacts

## 10. Carry-forward recommendations

- Before actual DB/API/Dashboard implementation, tighten any remaining `candidate visible facts` wording to `candidate future production-visible facts` if still present.
- Future DB/API/Dashboard gate must include production-fact leakage negative tests before implementation.
- Keep duplicate/conflict precedence and `raw_variant` modeling explicit in future tests.
- Do not convert diagnostic visibility or review-only evidence into ACK/read_done, retry, projection, defect-detail or production-outcome authority.
- The next technical branch should start with planning, not direct DB/API/Dashboard implementation.

## 11. Recommended next PM action

Start a new PM window, perform read-only recovery, then decide the next separately authorized downstream planning gate.

Candidate next planning directions only, not authorization:

- DB/API/Dashboard production visibility planning gate.
- Narrower Collector adapter hardening planning gate.
- Production-fact leakage negative tests planning.
- Duplicate/conflict precedence or historical config replay hardening planning.

## 12. Copyable prompt for the next ChatGPT PM window

Copy the entire block below into the next ChatGPT PM window as the first message.

    # Edge MES Demo — New ChatGPT PM recovery after production-fact visibility boundary closeout

    你的角色是一位 ChatGPT PM，接手 Edge MES Demo 项目。请先执行 read-only recovery，不要直接继续 implementation、tests、stage、commit 或 push。

    项目路径：
    /Users/chenjie/Documents/MES/edge-mes-demo

    必读文件：
    - docs/thread_handoff/chatgpt_pm_handoff_260701-1841.md
    - docs/thread_handoff/pm_operating_rules.md
    - docs/current_status.md
    - docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
    - docs/reports/sprint3_collector_ingestion_adapter_plan.md
    - docs/contracts/collector_ingestion_adapter.md

    第一动作必须执行：
        git status -sb
        printf '\n--- log -12 ---\n' && git log --oneline -12
        printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
        printf '\n--- origin/main ---\n' && git show-ref --hash refs/remotes/origin/main
        printf '\n--- diff name-only ---\n' && git diff --name-only
        printf '\n--- cached name-only ---\n' && git diff --cached --name-only

    当前 handoff baseline：
    HEAD == origin/main == 11cf077889dcf528ce91995e0acf183b74c31540
    latest commit: 11cf077 Freeze Sprint 3 production fact visibility boundary

    如果 live Git 与上述 baseline 不一致，先报告差异并停止，不要猜测继续。

    当前剩余 dirty 是 external artifacts，不要处理：
    - M .gitignore
    - ?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
    - ?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
    - ?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
    - ?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
    - ?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
    - ?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

    严禁：
    - git add .
    - git add -A
    - git add docs/
    - 未授权 implementation
    - 未授权 tests
    - 未授权 stage / commit / push
    - 未授权 DB/API/Dashboard/V-PLC/deploy/storage.py/ACK ownership work

    当前 closed 状态：
    - Sprint 3 accepted production-fact visibility boundary docs/contracts freeze: CLOSED / PASS WITH RECOMMENDATIONS
    - Reliability focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    - Data Quality focused review: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    - Verification focused review / exact allowlist audit: CLOSED / PASS WITH RECOMMENDATIONS, no blocker
    - Exact docs/status/PM-rule commit/push: PASS, commit 11cf077

    当前没有挂起的 review gate、commit gate 或 status sync gate。

    生产事实可见性边界：
    - future production visibility is limited to accepted station-event business facts after immutable config authority, raw_policy / decoder authority, shared validation, duplicate/conflict checks and adapter decision accepted;
    - diagnostic artifacts, raw evidence and non-accepted candidates remain diagnostic/review/debug only;
    - DB/API/Dashboard schema/API/UI/DB work remains deferred;
    - future DB/API/Dashboard gate must restate exact allowlist, review gates and production-fact leakage negative tests;
    - ACK/read_done ownership remains unchanged;
    - preserve: no ACK/read_done mutation for the current non-accepted payload.

    PM 规则提醒：
    给 Thread 的任务 prompt 本体必须是一个完整可复制 Markdown 块。PM 可以在 prompt 前后写 intake / 判断，但 Thread prompt 本体不能拆成多个代码块。

    下一步请先做 PM intake：确认 live baseline、closed gate、external artifacts 和非授权 surfaces。然后判断下一条技术主线应该是 DB/API/Dashboard production visibility planning、narrower Collector hardening planning、production-fact leakage negative tests planning，还是 duplicate/conflict precedence / historical config replay hardening planning。

    不要直接启动 implementation。

## 13. Handoff commit note

This handoff file is not staged automatically.

If committing this file, use exact path only:

    docs/thread_handoff/chatgpt_pm_handoff_260701-1841.md

Suggested commit message:

    Add PM handoff after production fact visibility boundary
