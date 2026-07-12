# ChatGPT PM Handoff — 2026-07-12 15:51 UTC+8

报告名称：Edge MES Demo ChatGPT PM handoff at Dashboard production URL-resolution focused-test completeness HOLD

任务名称：Create a durable PM handoff before the exact tests-only HOLD repair and remaining validation gates

执行角色：ChatGPT PM

```text
Dashboard production URL-resolution planning authority: PASS WITH RECOMMENDATIONS
Security/privacy planning review: PASS WITH RECOMMENDATIONS
Six-file implementation: completed, uncommitted
Focused no-DB Verification rerun: PASS WITH RECOMMENDATIONS, 90/90 tests passed
Reliability implementation review: PASS WITH RECOMMENDATIONS
Data Quality implementation review: PASS WITH RECOMMENDATIONS
Verification implementation conformance: PASS
Verification focused-test completeness: HOLD
Current exact blocker: apiOrigin.test.ts lacks direct positive coverage for https://api1.example / production
Tests-only HOLD repair: not yet authorized in a new Thread
Full regression/typecheck/build/runtime/Git writes: not authorized
```

This handoff is created because the current ChatGPT PM window has become context-heavy
after a long Level 2 workflow. The current HOLD is narrow and well-defined, but the
remaining branch still contains multiple independent validation and runtime gates. The
next PM must recover the repository first and must not continue from conversational
momentum.

## 1. First action for the next PM: read-only recovery

Project path:

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

The next PM's first action must be read-only recovery. Do not edit the missing test,
run tests, run typecheck/build, start runtime, update docs/status, or perform Git writes
before this recovery.

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git status -sb
printf '\n--- log -12 ---\n' && git log --oneline -12
printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
printf '\n--- origin/main ---\n' && git rev-parse origin/main
printf '\n--- ahead/behind ---\n' && git rev-list --left-right --count HEAD...origin/main
printf '\n--- diff name-only ---\n' && git diff --name-only
printf '\n--- cached name-only ---\n' && git diff --cached --name-only
printf '\n--- status normal ---\n' && git status --short --untracked-files=normal
```

Expected live baseline before this handoff is committed:

```text
branch: main
HEAD == origin/main == 1ea41b7f132328f461ee9ea92ba5ab7f7ac1be0c
latest commit: 1ea41b7 Repair Dashboard ORIGIN_MALFORMED authority
ahead/behind: 0 0
cached diff: empty
```

Expected uncommitted six-file implementation:

```text
M  frontend/src/app/accepted-events/__tests__/page.test.tsx
M  frontend/src/app/accepted-events/page.tsx
M  frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
M  frontend/src/lib/acceptedStationEvents/apiClient.ts
?? frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
?? frontend/src/lib/acceptedStationEvents/apiOrigin.ts
```

After this handoff is created, it is expected to appear as one additional untracked
file:

```text
docs/thread_handoff/chatgpt_pm_handoff_260712-1551.md
```

If this handoff is later committed and pushed, the next PM must use the new live HEAD
rather than treating `1ea41b7` as immutable. A lawful handoff-only forward commit is not
a blocker. Unknown source/test/package/config/runtime/gate drift is `HOLD`.

Do not pull, fetch, merge, rebase, reset, restore, clean, or self-repair during recovery.

## 2. PM rules and role boundary

Read first:

```text
docs/thread_handoff/pm_operating_rules.md
docs/current_status.md
docs/thread_handoff/chatgpt_pm_handoff_260712-1349.md
docs/thread_handoff/chatgpt_pm_handoff_260712-1551.md
```

PM owns:

```text
- live baseline recovery;
- task risk classification;
- exact task prompt and allowlist;
- report intake and gate decision;
- explicit authorization boundaries;
- exact-path stage/commit/push only after explicit user approval.
```

Professional Threads own:

```text
Architecture / Integration:
contract, implementation, integration boundaries, docs repair and status sync

Reliability:
fail-closed behavior, bounded diagnostics and operational resilience

Data Quality:
fact authority, strict DTO semantics, lineage and evidence classification

Verification:
test completeness, negative matrix, full regression, build/static audit and final allowlist audit
```

The next PM must not perform a professional Thread's review itself. A review report is
an intake event; `PASS` does not automatically authorize the next task, tests, Git
writes, runtime or deployment.

## 3. Live repository state at handoff creation

Read-only recovery at 2026-07-12 15:51 UTC+8 confirmed:

```text
branch: main
HEAD: 1ea41b7f132328f461ee9ea92ba5ab7f7ac1be0c
origin/main: 1ea41b7f132328f461ee9ea92ba5ab7f7ac1be0c
ahead/behind: 0 0
cached diff: empty
```

Recent relevant committed history:

```text
1ea41b7 Repair Dashboard ORIGIN_MALFORMED authority
bba8648 Re-review Dashboard resolver contract data quality
2483f2b Re-review Dashboard resolver contract reliability
6482e64 Add PM handoff after Dashboard resolver planning repair
d75c547 Repair Dashboard URL resolution resolver contract
7784e54 Record Dashboard URL resolution Verification HOLD
bb1935a Record Dashboard URL resolution Data Quality review
62e1424 Close Dashboard URL resolution Reliability planning review
f4c24ea Repair Dashboard production URL resolution planning
5922b4b Record Dashboard URL resolution Reliability HOLD
53ade97 Freeze Dashboard production URL resolution planning
4715456 Record Dashboard mock capability planning HOLD
```

No implementation file has been staged, committed or pushed in the current URL resolver
implementation sequence.

## 4. Known external dirty artifacts

These are pre-existing external artifacts. They are outside the current implementation,
repair and validation allowlists and must not be edited, cleaned, staged, committed or
used as evidence unless separately authorized:

```text
M  .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
?? docs/thread_handoff/chatgpt_pm_handoff_260712-1349.md
?? frontend/node_modules/
```

After this handoff creation, also expect:

```text
?? docs/thread_handoff/chatgpt_pm_handoff_260712-1551.md
```

`frontend/node_modules/` expands to thousands of files under
`--untracked-files=all`. Treat the whole directory as one excluded local dependency
artifact and use directory-level status for routine recovery.

## 5. Durable status-document caveat

`docs/current_status.md` does not yet record the full Dashboard production
URL-resolution sequence through the current implementation and review state. It is
historically stale for this branch.

This is not by itself a `HOLD`, because:

```text
- live Git is authoritative for the repository baseline;
- the committed URL-resolution plan is the resolver authority;
- subsequent chat-window review reports have been accepted by PM;
- status sync has not been authorized in this sequence.
```

Do not silently update `docs/current_status.md`. Future status sync is a separate
Architecture / Integration task with an exact allowlist and a separate Git gate.

## 6. Dashboard accepted-events contract invariants

Endpoint:

```text
GET /api/v2/production/accepted-station-events
```

Only query keys:

```text
line_id
start_time
end_time
limit
cursor
```

`cursor` remains API-owned and opaque.

Only consumer-facing fact authority:

```text
production_accepted_station_event_fact
```

Exact response envelope:

```text
outer own keys: data, page
data own key: items
page own keys: next_cursor, limit
```

Exact item DTO remains 22 required own keys:

```text
line_id
plc_id
station_id
station_type
profile_id
config_hash
config_version
event_type
production_result
unit_id
dmc
cycle_counter
source_event_id
event_ts
accepted_at
fact_key
content_fingerprint
nok_code
nok_origin
nok_detail_code
nok_detail_source_event_id
nok_detail_evidence_fact_key
```

Contract semantics:

```text
explicit JSON null: legal only where schema permits
missing required own key: illegal
unknown own key: illegal
malformed 2xx: kind "error"
accepted_at: accepted-fact timestamp only
summary: current page only
non-ready states: no stale table, summary, NOK evidence, trace or cursor
transport profile: never business profile_id
```

Forbidden source/fallback behavior includes:

```text
raw/candidate/review event substitution
legacy/current endpoint fallback
static fixture as production truth
previous ready result reuse
relative/default/fallback API URL
transport-profile-specific fact selection
```

## 7. Frozen resolver public contract

The public resolver contract remains:

```ts
export type AcceptedEventsApiOriginEnvironment = Readonly<{
  EDGE_MES_DASHBOARD_API_ORIGIN?: string;
  EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE?: string;
}>;

declare const trustedAcceptedEventsApiOriginBrand: unique symbol;

export type TrustedAcceptedEventsApiOrigin = string & {
  readonly [trustedAcceptedEventsApiOriginBrand]:
    "TrustedAcceptedEventsApiOrigin";
};

export type OriginConfigurationErrorCode =
  | "ORIGIN_MISSING"
  | "PROFILE_MISSING"
  | "ORIGIN_EMPTY"
  | "PROFILE_EMPTY"
  | "PROFILE_UNSUPPORTED"
  | "ORIGIN_NON_CANONICAL"
  | "ORIGIN_PROFILE_MISMATCH"
  | "ORIGIN_MALFORMED";

export type AcceptedEventsApiOriginResolution =
  | { readonly ok: true; readonly origin: TrustedAcceptedEventsApiOrigin }
  | {
      readonly ok: false;
      readonly code: OriginConfigurationErrorCode;
      readonly message: "Accepted events service is not configured.";
    };

export function resolveTrustedAcceptedEventsApiOrigin(
  environment?: AcceptedEventsApiOriginEnvironment
): AcceptedEventsApiOriginResolution;
```

Frozen error precedence:

```text
1. ORIGIN_MISSING
2. PROFILE_MISSING
3. ORIGIN_EMPTY
4. PROFILE_EMPTY
5. PROFILE_UNSUPPORTED
6. raw safety/canonicality validation
7. profile matching
8. native URL parsing
9. parsed-component re-verification
```

Expected invalid configuration is non-throwing. Result shapes, safe message, brand
boundary, request-time environment snapshot and finite safe-code logging must remain
unchanged.

## 8. Current six-file implementation

Exact implementation set:

```text
frontend/src/lib/acceptedStationEvents/apiOrigin.ts
frontend/src/lib/acceptedStationEvents/apiClient.ts
frontend/src/app/accepted-events/page.tsx
frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
frontend/src/app/accepted-events/__tests__/page.test.tsx
```

Implementation summary:

```text
apiOrigin.ts:
- server-process environment only;
- one read per origin/profile property per invocation;
- closed local/container/production raw grammar;
- production numeric-IP/IP-literal guard before native new URL();
- real native ORIGIN_MALFORMED path;
- success-only brand creation;
- bounded once-per-code redacted logging with logger-throw containment.

apiClient.ts:
- accepts validated query plus TrustedAcceptedEventsApiOrigin;
- fixed absolute accepted-events endpoint;
- URLSearchParams query authority;
- GET, cache no-store, credentials omit, redirect error;
- no retry, no fallback, no second request.

page.tsx:
- query validation -> resolver -> client;
- invalid query before resolver;
- configuration failure before client/fetch;
- fixed safe browser message;
- no stale ready surfaces in non-ready states.
```

Files explicitly not changed:

```text
frontend/src/lib/acceptedStationEvents/query.ts
frontend/src/lib/acceptedStationEvents/schema.ts
frontend/src/lib/acceptedStationEvents/viewModel.ts
frontend/src/components/accepted-events/**
frontend/package.json
frontend/package-lock.json
frontend/next.config.ts
frontend/tsconfig.json
API/DB/Docker/Compose/docs/status
```

## 9. Cross-functional gate history after implementation

### 9.1 Security/privacy planning review

```text
Conclusion: PASS WITH RECOMMENDATIONS
Blockers: none
Six-file allowlist sufficient: yes
```

Key accepted boundaries:

```text
server-only origin/profile configuration
no NEXT_PUBLIC_*
no Host/Forwarded/cookie/query/browser-origin derivation
brand does not replace runtime validation
credentials omitted
redirects rejected
no raw topology in UI/log/result
DNS/egress ownership remains REL-URL-R6
same-origin no-DB mock remains HOLD
```

### 9.2 Initial focused Verification execution

Initial result was `HOLD` because:

```text
- production resolver accepted https://127.0.0.1;
- DQ-URL-D1 three-profile isolation evidence was incomplete.
```

Architecture / Integration repaired only:

```text
frontend/src/lib/acceptedStationEvents/apiOrigin.ts
frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
frontend/src/app/accepted-events/__tests__/page.test.tsx
```

The repair added raw-stage numeric-IP/IP-literal rejection and parameterized
local/container/production profile-isolation evidence.

### 9.3 Focused Verification rerun

Accepted evidence:

```text
Node version: v22.23.0
https://xn--a.example: native TypeError Invalid URL
https://xn--a.example/: native TypeError Invalid URL

apiOrigin.test.ts: 56 passed
apiClient.test.ts: 14 passed
page.test.tsx: 20 passed

total: 90 passed
failed: 0
skipped: 0
unhandled errors: none
```

Confirmed production IP-like rejection:

```text
https://127.0.0.1        -> ORIGIN_NON_CANONICAL
https://127.1            -> ORIGIN_NON_CANONICAL
https://0177.0.0.1       -> ORIGIN_NON_CANONICAL
https://0x7f.0.0.1       -> ORIGIN_NON_CANONICAL
https://[::1]            -> ORIGIN_NON_CANONICAL
```

Confirmed transport/business isolation:

```text
transport profiles: local / container / production
response-owned profile_id: accepted-fact-profile-42
client argument count: exactly 2
item filtering: none
trace preserves response profile_id
```

### 9.4 Reliability implementation review

```text
Conclusion: PASS WITH RECOMMENDATIONS
REL-URL-R3: CLOSED
REL-URL-R4: CLOSED
REL-URL-R5: CLOSED
Blockers: none
```

`REL-URL-R6` remains open for deployment/config readiness, DNS/egress, accepted-events
service readiness, alerting, operator diagnostics and restart/config-correction
ownership.

### 9.5 Data Quality implementation review

```text
Conclusion: PASS WITH RECOMMENDATIONS
DQ-URL-D1: CLOSED
DQ-URL-D2: CARRY FORWARD
DQ-URL-D3: CARRY FORWARD
Blockers: none
```

Focused test evidence is synthetic transport/strict-contract evidence. It is not
DB-backed production-fact evidence, production readiness evidence or full frontend
regression evidence.

### 9.6 Verification implementation review — current HOLD

```text
Conclusion: HOLD
Focused implementation conformance: PASS
Focused test completeness: HOLD
DQ-URL-D1: CLOSED
Authority conflicts: none
Allowlist expansion required: no
```

The sole blocker is:

```text
frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts

Missing required direct production-positive assertion:
https://api1.example
```

The implementation's production FQDN grammar already accepts this value. The HOLD is
for required test completeness, not for a known production source defect.

Current file evidence at handoff creation:

```text
https://accepted-api.example       present
https://accepted-api.example/      present
https://xn--bcher-kva.example      present
https://1.api.example              present
https://api1.example               missing
```

## 10. Current gate state

Global current state:

```text
Dashboard production URL-resolution implementation branch: HOLD
```

Current blocker count:

```text
1
```

Current blocker classification:

```text
Owner: Architecture / Integration
Task type: tests-only implementation repair
Risk: Level 1
Source runtime behavior change: no
Exact edit allowlist: one existing test file
```

Current closed findings:

```text
REL-URL-R3: CLOSED
REL-URL-R4: CLOSED
REL-URL-R5: CLOSED
DQ-URL-D1: CLOSED
```

Current carry-forward findings:

```text
REL-URL-R6: deployment/config readiness
DQ-URL-D2: runtime evidence classification
DQ-URL-D3: full frontend regression
VER-URL-V2: typecheck/build/static bundle evidence
VER-URL-V3: dedicated runtime capture/cleanup evidence
```

Current separate capability state:

```text
same-origin no-DB mock capability: HOLD
```

The URL resolver implementation does not close or change the mock-capability HOLD.

## 11. Recommended next task: exact tests-only HOLD repair

After successful read-only recovery, the next PM should issue a new Architecture /
Integration Thread with this exact scope:

```text
Task size: small
Risk: Level 1
Task type: tests-only repair
Exact edit allowlist:
frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
```

Required repair:

```text
Add https://api1.example with profile production to the existing direct resolver
positive matrix and assert resolver success with canonical origin
https://api1.example.
```

The repair must preserve the existing positive cases and all existing negative,
logging, read-count, malformed-vector and IP-literal tests.

Explicitly forbidden during the repair:

```text
editing apiOrigin.ts
editing apiClient.ts
editing page.tsx
editing apiClient.test.ts
editing page.test.tsx
editing query/schema/viewModel/components
package/config/dependency changes
running tests
running typecheck/build/runtime
status/docs edits
stage/commit/push
```

The repair Thread should perform only source/test diff inspection and whitespace checks,
then stop for PM intake.

## 12. Required validation sequence after repair

Do not combine these steps into the repair authorization.

### Gate A — focused resolver test execution

After repair intake, authorize a new Verification commands-only Thread to run at least:

```bash
cd /Users/chenjie/Documents/MES/edge-mes-demo/frontend
npm test -- src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
```

The evidence must explicitly confirm that `https://api1.example` executed and passed.
Do not rely only on total test count.

### Gate B — renewed focused Verification implementation review

After the focused resolver test passes, authorize a new review-only Verification Thread
to close the exact focused-test completeness HOLD. It must not rerun tests or edit files.

### Gate C — DQ-URL-D3 full frontend regression

Only after the focused HOLD closes, authorize full frontend regression separately:

```bash
npm test
```

This gate must cover query, schema, viewModel, components, page and all focused URL
resolver/client tests. It must audit generated artifacts and working-tree drift.

### Gate D — VER-URL-V2 typecheck/build/static bundle evidence

Authorize separately:

```bash
npm run typecheck
npm run build
```

Before issuing this Gate, freeze exact temporary/generated artifact handling for `.next`
and any TypeScript incremental cache. The Gate must separately inspect:

```text
.next/static/**
.next/server/**
```

It must prove that raw origin/profile configuration does not enter browser bundles and
must not confuse server bundle references with browser leakage.

### Gate E — VER-URL-V3 / DQ-URL-D2 runtime planning and evidence

This remains a separate planning and runtime branch. It requires exact capture method,
owned PID/port cleanup, same-artifact hash, zero-versus-one request evidence and clear
classification of:

```text
transport evidence
synthetic strict-contract fixture evidence
real production-fact evidence
```

Do not infer runtime authorization from build success.

### Gate F — REL-URL-R6 deployment/config readiness

This remains separate from application source validation and includes:

```text
environment ownership
DNS behavior
egress/firewall
accepted-events readiness
Next readiness versus API readiness
alerting
operator diagnostics
restart/config-correction procedure
```

## 13. Non-authorized surfaces

Until separately authorized, do not:

```text
modify production source beyond an exact repair allowlist
modify schema/query/viewModel/components
modify package/lock/config
modify API/DB/Docker/Compose
start Next/API/DB/Docker
connect to real services
create runtime fixtures or mock routes
update docs/current_status.md
update README.md
stage/commit/push/tag/deploy/rollback
perform real PLC or Raspberry Pi deployment work
```

No `PASS` report automatically authorizes any of the above.

## 14. Git safety for the handoff file

This handoff creation is authorized. Staging, committing and pushing it are not included
in the current authorization.

Do not automatically stage:

```text
docs/thread_handoff/chatgpt_pm_handoff_260712-1551.md
```

If the user later authorizes handoff Git writes, use exact-path staging only:

```bash
git add -- docs/thread_handoff/chatgpt_pm_handoff_260712-1551.md
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

The staged set must contain exactly:

```text
docs/thread_handoff/chatgpt_pm_handoff_260712-1551.md
```

Do not stage `.gitignore`, old handoffs, reports, HTML artifacts, `frontend/node_modules/`
or any of the six uncommitted implementation files as part of a handoff-only commit.

## 15. Copyable prompt for the next ChatGPT PM window

```markdown
# Edge MES Demo — ChatGPT PM Handoff Restore

你现在接手 Edge MES Demo 项目的 ChatGPT PM 角色。

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

第一优先级：恢复上下文，不要直接修复测试。

请先读取并遵守：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260712-1551.md
- docs/thread_handoff/chatgpt_pm_handoff_260712-1349.md
- docs/current_status.md
- docs/contracts/dashboard_api_contract.md
- docs/reports/sprint3_dashboard_production_url_resolution_plan.md
- docs/reports/sprint3_dashboard_production_url_resolution_data_quality_review.md
- docs/reports/sprint3_dashboard_production_url_resolution_verification_review.md

## 1. 第一动作：read-only recovery

不要编辑、不要运行 tests、不要运行 Node proof、不要 typecheck/build、不要启动 runtime、不要 stage、不要 commit、不要 push。

执行：

    git status -sb
    printf '\n--- log -12 ---\n' && git log --oneline -12
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git rev-parse origin/main
    printf '\n--- ahead/behind ---\n' && git rev-list --left-right --count HEAD...origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only
    printf '\n--- status normal ---\n' && git status --short --untracked-files=normal

Expected pre-handoff-commit baseline：

    HEAD == origin/main == 1ea41b7f132328f461ee9ea92ba5ab7f7ac1be0c
    latest commit: 1ea41b7 Repair Dashboard ORIGIN_MALFORMED authority
    ahead/behind: 0 0
    cached diff: empty

Expected uncommitted implementation：

    M frontend/src/app/accepted-events/__tests__/page.test.tsx
    M frontend/src/app/accepted-events/page.tsx
    M frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
    M frontend/src/lib/acceptedStationEvents/apiClient.ts
    ?? frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
    ?? frontend/src/lib/acceptedStationEvents/apiOrigin.ts

If the handoff has been committed and pushed, a later handoff-only HEAD is acceptable only after exact-path verification. Unknown source/test/package/config/runtime drift is HOLD.

## 2. Current gate state

    Security/privacy planning review: PASS WITH RECOMMENDATIONS
    focused Verification rerun: PASS WITH RECOMMENDATIONS, 90/90 passed
    Reliability implementation review: PASS WITH RECOMMENDATIONS
    Data Quality implementation review: PASS WITH RECOMMENDATIONS
    Verification implementation conformance: PASS
    Verification focused-test completeness: HOLD

唯一 blocker：

    frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts

缺少 direct resolver positive assertion：

    origin: https://api1.example
    profile: production
    expected: success with origin https://api1.example

这是 required test completeness 缺口，不是已知 production source defect。

## 3. PM intake 后的建议动作

完成 read-only recovery 后，先报告：

- live HEAD / origin/main；
- six-file working tree 是否符合预期；
- external dirty artifacts 是否未变；
- cached diff 是否为空；
- 当前唯一 HOLD 是否仍为缺少 `https://api1.example` positive assertion。

若状态一致，签发新的 Architecture / Integration Level 1 tests-only repair Thread。

Exact edit allowlist：

    frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts

只允许：

- 将 `https://api1.example` / `production` 加入现有 positive matrix；
- 断言 resolver success 和 canonical origin；
- read-only diff/status/whitespace audit。

不得：

- 修改 apiOrigin.ts、apiClient.ts、page.tsx、apiClient.test.ts、page.test.tsx；
- 修改 query/schema/viewModel/components；
- 修改 package/config/dependency；
- 运行 tests、typecheck、build、runtime；
- 修改 docs/status；
- stage、commit、push。

repair intake 后，再分别授权：

1. focused apiOrigin test execution；
2. renewed focused Verification review；
3. full frontend regression（DQ-URL-D3）；
4. typecheck/build/static bundle audit（VER-URL-V2）；
5. runtime evidence planning/execution（VER-URL-V3 / DQ-URL-D2）；
6. deployment/config readiness（REL-URL-R6）。

不要把这些 Gate 合并授权，也不要从 PASS 自动推导 Git 或 runtime 权限。

## 4. Current carry-forward

    REL-URL-R6: CARRY FORWARD
    DQ-URL-D2: CARRY FORWARD
    DQ-URL-D3: CARRY FORWARD
    VER-URL-V2: CARRY FORWARD
    VER-URL-V3: CARRY FORWARD
    same-origin no-DB mock capability: HOLD

## 5. PM role boundary

PM 不执行 Architecture、Reliability、Data Quality 或 Verification 的专业判断。PM 负责 recovery、风险分类、allowlist、报告 intake、Gate 决策和明确授权边界。
```

## 16. Final handoff state

At handoff creation:

```text
handoff file created:
docs/thread_handoff/chatgpt_pm_handoff_260712-1551.md

handoff staged: no
handoff committed: no
handoff pushed: no

implementation staged: no
implementation committed: no
implementation pushed: no

current global gate: HOLD
current exact blocker: missing https://api1.example direct production-positive resolver test
```

The next PM should begin with read-only recovery and must not infer repair, test,
runtime, status-sync or Git authorization from this handoff alone.
