# ChatGPT PM Handoff — 2026-07-12 13:49 UTC+8

报告名称：Edge MES Demo ChatGPT PM handoff after Dashboard URL resolver cross-functional planning closure

任务名称：Create a durable PM handoff before the focused Security/privacy planning review

执行角色：ChatGPT PM

```text
Dashboard production URL-resolution planning authority: PASS WITH RECOMMENDATIONS
VER-URL-V1-B1 Architecture repair: committed and pushed
Focused Reliability re-review: PASS WITH RECOMMENDATIONS, no blocker
Focused Data Quality re-review: PASS WITH RECOMMENDATIONS, no blocker
Focused Verification re-review: PASS WITH RECOMMENDATIONS, original HOLD closed with carry-forward
Focused Security/privacy planning review: not started; task prompt not issued
Implementation: not authorized
Tests/typecheck/build/runtime: not authorized
```

This handoff is created because the current ChatGPT PM window is context-heavy and the
next task opens a new Security/privacy planning branch. The next PM must recover the
repository first and must not continue from conversational momentum.

## 1. First action for the next PM: read-only recovery

Project path:

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

The next PM's first action must be read-only recovery. Do not issue the Security/privacy
review task, edit files, run tests, start runtime, or perform Git writes before this
recovery.

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
tracked diff before handoff creation: .gitignore only
```

After this handoff is created, it is expected to appear as one additional untracked
file:

```text
docs/thread_handoff/chatgpt_pm_handoff_260712-1349.md
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
docs/thread_handoff/chatgpt_pm_handoff_260712-0950.md
```

Important PM role correction already applied in the current window:

```text
PM owns:
- live baseline recovery;
- task risk classification;
- exact task prompt and allowlist;
- report intake and gate decision;
- explicit authorization boundaries;
- exact-path stage/commit/push after user approval.

Core professional Threads own:
- Architecture / Integration: contract, boundary, ownership, docs repair, status sync;
- Reliability: fail-closed behavior, runtime safety and reliability constraints;
- Data Quality: fact authority, lineage, projection and evidence semantics;
- Verification: negative matrix, testability, regression and final allowlist audit.
```

PM must not execute a professional Thread's technical review itself. Security/privacy is
not a new long-lived Thread. For this task type, the owner is `Architecture /
Integration`, with an independent Level 1 review-only prompt.

## 3. Live repository state at handoff creation

Read-only recovery at 2026-07-12 13:49 UTC+8 confirmed:

```text
branch: main
HEAD: 1ea41b7f132328f461ee9ea92ba5ab7f7ac1be0c
origin/main: 1ea41b7f132328f461ee9ea92ba5ab7f7ac1be0c
ahead/behind: 0 0
cached diff: empty
tracked diff before handoff creation: .gitignore only
```

Recent relevant history:

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

## 4. Known external dirty artifacts

These are pre-existing external artifacts. They are outside the next task allowlist and
must not be edited, cleaned, staged, committed, or used as evidence unless explicitly
authorized:

```text
M  .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
?? frontend/node_modules/
```

`frontend/node_modules/` may expand to thousands of untracked files with
`--untracked-files=all`; use directory-level status for routine recovery and continue
to treat the entire directory as one excluded local dependency artifact.

## 5. Durable status-document caveat

`docs/current_status.md` was last updated on 2026-07-11 and begins from the older
Dashboard frontend typecheck/build validation branch. It does not yet record the
production URL-resolution sequence through `1ea41b7`.

This mismatch is historical staleness, not by itself a `HOLD`, because:

- live Git is authoritative for the repository baseline;
- the URL-resolution plan and committed review reports are later durable authorities;
- no status-sync task has been authorized in the current sequence.

Do not silently update `docs/current_status.md`. A future status sync is a separate
Architecture / Integration task with its own exact allowlist and user-authorized Git
gate.

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

Forbidden fallback/equivalent sources include:

```text
raw_plc_sample
cycle_event
station_event
production_unit
quality_event
production_snapshot
production_events
legacy/current fallback
static fixture or previous result
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
explicit JSON null: legal where schema permits
missing required own key: illegal
unknown own key: illegal
malformed 2xx: kind: "error"
accepted_at: accepted-fact timestamp only
summary: current page only
non-ready states: no stale table, summary, evidence, trace or cursor
transport profile: not business profile_id
```

## 7. URL resolver planning authority

Primary committed authority:

```text
docs/reports/sprint3_dashboard_production_url_resolution_plan.md
commit: 1ea41b7f132328f461ee9ea92ba5ab7f7ac1be0c
```

Public contract remains frozen:

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

Core resolver rules:

```text
production call: resolveTrustedAcceptedEventsApiOrigin()
test call: resolveTrustedAcceptedEventsApiOrigin(typedEnvironment)
configuration invalidity: non-throwing
success exact own keys: ok, origin
failure exact own keys: ok, code, message
safe message: Accepted events service is not configured.
brand creator: resolver success path only
page/client env read: forbidden
global process.env proxy: forbidden
parser injection or URL monkey-patch: forbidden
production test-only constructor/reset/export: forbidden
```

Each invocation reads the two source properties exactly once into one local immutable
snapshot. No import-time/build-time snapshot and no reread in validation, logging, page,
or client are allowed.

Closed precedence:

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

## 8. VER-URL-V1-B1 repair

The original focused Verification review reported `HOLD` because
`ORIGIN_MALFORMED` did not have a frozen public-resolver input-native test vector.

Architecture / Integration repaired the single plan file and committed it as
`1ea41b7`. The frozen vector is:

```ts
{
  EDGE_MES_DASHBOARD_API_ORIGIN: "https://xn--a.example",
  EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: "production",
}
```

The authority states that this value:

- passes the selected production lower-case ASCII dotted-FQDN raw grammar;
- does not first become `ORIGIN_NON_CANONICAL` or
  `ORIGIN_PROFILE_MISMATCH`;
- causes the target Node WHATWG `new URL()` to throw natively;
- returns exact `ORIGIN_MALFORMED` failure keys and fixed message;
- must never be manufactured through a global URL monkey-patch, injected parser,
  production override, synthetic throw, constructor, or reset seam.

The committed plan records Node `v22.23.0` as the repair evidence runtime. The future
implementation/test gate must record its actual Node version and repeat the native
throw proof. If a supported target runtime accepts the vector, the implementation/test
gate is `HOLD` and the issue returns to Architecture authority repair.

The durable negative matrix contains one typed environment input for all eight codes.
Use the repository plan as source of truth. In particular, the committed
`ORIGIN_NON_CANONICAL` vector is:

```text
http://127.0.0.1:08000 with profile local
```

Do not substitute an older chat-summary example such as port `8001`.

## 9. Cross-functional re-review state after 1ea41b7

After `1ea41b7`, three independent Level 1 review-only Threads were run. They changed no
files and produced chat-window reports only.

### Focused Reliability re-review

Accepted by PM as:

```text
PASS WITH RECOMMENDATIONS
VER-URL-V1-B1: CLOSED from Reliability planning perspective
new Reliability blockers: none
```

Reported evidence:

```text
Node: v22.23.0
https://xn--a.example: native TypeError: Invalid URL
https://xn--a.example/: native TypeError: Invalid URL
raw grammar: passes production raw grammar before parser
six-file implementation allowlist: sufficient
```

Carry-forward:

```text
REL-URL-R3: snapshot/read-count and request-time reread implementation evidence
REL-URL-R4: bounded/redacted/non-throwing logging implementation evidence
REL-URL-R5: serial env restoration and module-isolation test evidence
REL-URL-R6: future deployment/config readiness, alerting, DNS/egress ownership
```

### Focused Data Quality re-review

Accepted by PM as:

```text
PASS WITH RECOMMENDATIONS
VER-URL-V1-B1: ACCEPTED WITH CARRY-FORWARD from Data Quality perspective
new Data Quality blockers: none
```

Carry-forward:

```text
DQ-URL-D1: transport profile / response-owned profile_id isolation tests
DQ-URL-D2: three-way runtime evidence classification
DQ-URL-D3: full frontend regression, not focused tests alone
```

Data Quality preserved:

- `ORIGIN_MALFORMED` is transport configuration failure only;
- safe code/origin/profile/parser diagnostics do not enter DTO or view state;
- configuration error is generic `kind: "error"`, not empty or unavailable;
- strict parser, 22-key DTO and production-fact authority remain unchanged;
- synthetic fixtures are not production-fact evidence.

### Focused Verification re-review

Accepted by PM as:

```text
PASS WITH RECOMMENDATIONS
VER-URL-V1-B1: CLOSED WITH CARRY-FORWARD
original Verification HOLD: closed
new Verification blockers: none
```

Reported evidence:

```text
Node: v22.23.0
frozen raw grammar: passes
both malformed variants: native TypeError: Invalid URL
control vectors: accepted by native URL parser
eight-code public-resolver matrix: executable
six-file implementation allowlist: sufficient
```

Carry-forward:

```text
VER-URL-V2: build/static client-bundle evidence
VER-URL-V3: dedicated runtime capture/fixture planning and evidence
```

### Durable-report caveat

The post-`1ea41b7` reviews were intentionally review-only and did not update repository
review reports. Therefore:

```text
docs/reports/sprint3_dashboard_production_url_resolution_reliability_rereview.md
```

contains the earlier focused review of `d75c547`, and:

```text
docs/reports/sprint3_dashboard_production_url_resolution_data_quality_review.md
```

contains the earlier focused review state, while:

```text
docs/reports/sprint3_dashboard_production_url_resolution_verification_review.md
```

still records the historical pre-repair `HOLD` at `7784e54`.

Do not misread that historical report as a new live blocker. This handoff records the
later PM-accepted chat-window re-reviews. A future durable review/status sync is a
separate Architecture / Integration task and has not been authorized.

## 10. Cross-functional planning closure

Current PM intake state:

```text
Architecture / Integration planning authority: PASS WITH RECOMMENDATIONS
Focused Reliability re-review: PASS WITH RECOMMENDATIONS
Focused Data Quality re-review: PASS WITH RECOMMENDATIONS
Focused Verification re-review: PASS WITH RECOMMENDATIONS
VER-URL-V1-B1: cross-functional planning closure achieved
current blockers: none
```

This does not authorize implementation. The committed plan explicitly requires a
focused Security/privacy planning review before any PM implementation decision.

## 11. Next gate

Recommended next gate:

```text
Task: focused Security/privacy planning review
Owner: Architecture / Integration
Risk: Level 1 review-only
Changed files: none
Tests/typecheck/build/runtime: not run
Git writes: forbidden
```

The Security/privacy task prompt was drafted in the previous PM window but was **not
sent** to a professional Thread because the PM context window was judged too long. The
new PM must independently re-check the baseline and then issue a fresh compact prompt.

Review focus:

- server-only operator-controlled environment trust boundary;
- no `NEXT_PUBLIC_*`, browser props, inbound Host/Forwarded/header/query/cookie origin;
- closed local/container/production profile SSRF controls;
- raw syntax before parser and parsed component re-verification;
- TypeScript brand plus runtime validation boundary;
- fixed endpoint composition using `new URL()` and `URLSearchParams`;
- `GET`, `cache: "no-store"`, `credentials: "omit"`, `redirect: "error"`;
- safe error-result privacy;
- bounded eight-code logging with no raw/topology/business-data leak;
- logger-throw containment and attempted/seen dedupe semantics;
- static browser-bundle privacy deferred to `VER-URL-V2`;
- production DNS, egress, readiness, alerting and diagnostics ownership deferred only
  if safely bounded to `REL-URL-R6` deployment/config gate;
- same-origin no-DB mock capability remains `HOLD`;
- six-file implementation allowlist remains sufficient, or return `HOLD`.

Suggested findings:

```text
SEC-URL-S1: SSRF/trust boundary
SEC-URL-S2: secret/browser leakage
SEC-URL-S3: logging privacy
SEC-URL-S4: DNS/egress deployment ownership
```

If Security/privacy returns `PASS WITH RECOMMENDATIONS` and no blocker, PM may then
assess whether to authorize the six-file implementation. Do not infer implementation
authorization from review PASS alone.

## 12. Future implementation allowlist

No implementation is currently authorized. If later explicitly authorized, the exact
six-file allowlist remains:

```text
Create frontend/src/lib/acceptedStationEvents/apiOrigin.ts
Modify frontend/src/lib/acceptedStationEvents/apiClient.ts
Modify frontend/src/app/accepted-events/page.tsx
Create frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
Modify frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
Modify frontend/src/app/accepted-events/__tests__/page.test.tsx
```

No additional files are implied. Specifically excluded unless a future gate explicitly
returns `HOLD` and Architecture repairs authority:

```text
frontend/package.json
frontend/package-lock.json
frontend/next.config.ts
frontend/tsconfig.json
schema.ts
query.ts
viewModel.ts
components
logger/config helper
fixture/runtime helper
middleware
Route Handler
.env.example
Compose
README
API/DB
new dependency
```

Implementation, tests, typecheck, build and runtime are separate authorizations.

## 13. Carry-forward matrix

```text
REL-URL-R3
owner/closure: implementation and focused tests
proof: one pair snapshot, exactly-once getter reads, request-time reread, no import/build snapshot

REL-URL-R4
owner/closure: implementation and focused tests
proof: finite eight-code dedupe, redaction, non-throwing logger containment, logger-throw attempted/seen behavior

REL-URL-R5
owner/closure: focused tests
proof: serial shared-env cases, exact presence/value restore, failure-safe afterEach, module isolation

REL-URL-R6
owner/closure: future deployment/config gate
proof: accepted-events readiness, alerting, diagnostics, DNS and egress ownership

DQ-URL-D1
owner/closure: six-file implementation tests
proof: transport profile absent from DTO/view; response profile_id preserved; no filtering/stale profile data

DQ-URL-D2
owner/closure: VER-URL-V3 runtime evidence gate
proof: transport capture, synthetic strict-contract fixture and real production-fact evidence remain distinct

DQ-URL-D3
owner/closure: full frontend regression
proof: successful full npm test including unchanged schema/query/viewModel/component suites

VER-URL-V2
owner/closure: build/static bundle evidence gate
proof: inspect .next/static separately from .next/server; whole-.next grep is insufficient

VER-URL-V3
owner/closure: dedicated runtime planning then runtime evidence
proof: exact capture method, temporary artifact/PID/port allowlist, zero/exactly-one request, same artifact, cleanup
```

## 14. Non-authorized surfaces

The next PM must not infer authorization for:

```text
Security/privacy task file writes
implementation
frontend source or tests
npm test
typecheck
build
Next server/browser
API/DB/Postgres
Docker
runtime capture/fixture
same-origin mock
package/config/dependency
status sync
stage/commit/push beyond this exact handoff if separately approved
tag
deploy
rollback
real PLC work
```

## 15. Handoff file state

This handoff was created as:

```text
docs/thread_handoff/chatgpt_pm_handoff_260712-1349.md
```

The filename timestamp is China Standard Time / UTC+8. The filename, title timestamp,
internal path references and next-PM prompt below must remain identical.

This task does not stage, commit, or push the handoff. Explicit user authorization is
required for exact-path Git writes.

## 16. Copyable prompt for the next ChatGPT PM window

```markdown
# Edge MES Demo — ChatGPT PM Handoff Restore

你现在接手 Edge MES Demo 项目的 ChatGPT PM 角色。

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

第一优先级：恢复 PM 上下文，不要直接下达 Security/privacy、implementation、tests、build 或 runtime 任务。

请先读取并遵守：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260712-1349.md
- docs/current_status.md
- docs/contracts/dashboard_api_contract.md
- docs/reports/sprint3_dashboard_production_url_resolution_plan.md
- docs/reports/sprint3_dashboard_same_origin_no_db_mock_capability_plan.md
- docs/reports/sprint3_dashboard_production_url_resolution_reliability_review.md
- docs/reports/sprint3_dashboard_production_url_resolution_reliability_rereview.md
- docs/reports/sprint3_dashboard_production_url_resolution_data_quality_review.md
- docs/reports/sprint3_dashboard_production_url_resolution_verification_review.md

第一动作必须是 read-only recovery：

    git status -sb
    printf '\n--- log -12 ---\n' && git log --oneline -12
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git rev-parse origin/main
    printf '\n--- ahead/behind ---\n' && git rev-list --left-right --count HEAD...origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only
    printf '\n--- status normal ---\n' && git status --short --untracked-files=normal

Expected technical baseline before handoff commit：

    HEAD == origin/main == 1ea41b7f132328f461ee9ea92ba5ab7f7ac1be0c
    latest commit: 1ea41b7 Repair Dashboard ORIGIN_MALFORMED authority
    ahead/behind: 0 0
    cached diff: empty

如果 handoff 已经被单独 commit/push，允许 live HEAD 仅因该 handoff commit 前移；必须核对该 commit 只包含：

    docs/thread_handoff/chatgpt_pm_handoff_260712-1349.md

Expected external dirty artifacts：

    M .gitignore
    ?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
    ?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
    ?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
    ?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
    ?? frontend/node_modules/

这些 external artifacts 不得修改、清理、stage 或提交。

当前已关闭状态：

    Architecture planning authority: PASS WITH RECOMMENDATIONS
    Reliability re-review: PASS WITH RECOMMENDATIONS
    Data Quality re-review: PASS WITH RECOMMENDATIONS
    Verification re-review: PASS WITH RECOMMENDATIONS
    VER-URL-V1-B1: cross-functional planning closure achieved
    blockers: none

注意：post-1ea41b7 的三份专业 re-review 是 review-only chat-window reports，没有修改 repository review reports。历史 Verification report 仍显示旧 HOLD；以本 handoff 记录的后续 PM intake 和 live committed plan 为当前恢复依据，不得擅自 status sync。

当前下一 Gate：

    Focused Security/privacy planning review
    Owner: Architecture / Integration
    Risk: Level 1 review-only
    Changed files: none

Security/privacy Prompt 尚未发出。完成 recovery 和 intake 后，由新 PM 生成一个单一可复制 Markdown block，交给新的 Architecture / Integration Thread。PM 自己不得执行专业安全审查。

Implementation、tests、typecheck、build、runtime capture、status sync、stage/commit/push、tag、deploy、rollback 均未授权。
```

## 17. Recommended next PM decision

After recovery:

1. Confirm the handoff-only baseline and external artifacts.
2. Treat post-`1ea41b7` Reliability/Data Quality/Verification reports as PM-accepted
   review-only window evidence recorded here, not as repository report edits.
3. Classify the next task as Level 1 review-only, owner Architecture / Integration.
4. Issue a compact Security/privacy review prompt with `changed files: none`.
5. Intake its result.
6. If `HOLD`, authorize the exact Architecture repair only.
7. If `PASS WITH RECOMMENDATIONS`, pause and obtain a separate PM/user decision before
   any six-file implementation authorization.

Do not combine Security/privacy review, implementation, tests, build, runtime planning,
status sync, or Git writes into one authorization.
