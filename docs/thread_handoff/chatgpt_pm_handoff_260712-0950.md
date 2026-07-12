# ChatGPT PM Handoff — 2026-07-12 09:50 UTC+8

报告名称：Edge MES Demo ChatGPT PM handoff after Dashboard VER-URL-V1 planning repair

任务名称：Create a durable PM handoff before focused Reliability re-review

执行 Thread：Architecture / Integration

~~~
VER-URL-V1 planning authority repair: committed and pushed
Focused Reliability re-review: not started
Verification: remains HOLD
Implementation: not authorized
~~~
## 1. First action for next PM: read-only recovery

下一位 PM 的第一动作必须是 read-only recovery。不得直接启动 review；先核对 baseline 和 dirty artifacts。

~~~bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git status -sb
printf '\n--- log -16 ---\n' && git log --oneline -16
printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
printf '\n--- origin/main ---\n' && git rev-parse origin/main
printf '\n--- ahead/behind ---\n' && \
git rev-list --left-right --count origin/main...HEAD
printf '\n--- diff name-only ---\n' && git diff --name-only
printf '\n--- cached name-only ---\n' && git diff --cached --name-only
printf '\n--- status all ---\n' && \
git status --short --untracked-files=all
~~~

Expected durable baseline:

~~~text
HEAD == origin/main ==
d75c5477251de1b60f7a16e5d8803fd7c20f5b38
latest commit:
d75c547 Repair Dashboard URL resolution resolver contract
ahead/behind: 0 0
cached diff: empty
~~~

If live Git differs, report actual state and stop. Only a lawful docs/handoff forward move with no changed URL-resolution authorities, frontend, package, config, tests, or gate state may continue. Unknown code/config/package/test/runtime drift is HOLD. Do not pull, fetch, merge, rebase, reset, or self-repair.

## 2. PM rules and required context

Read, in order, before any future gate:

~~~text
docs/thread_handoff/pm_operating_rules.md
docs/current_status.md
docs/contracts/dashboard_api_contract.md
docs/thread_handoff/chatgpt_pm_handoff_260711-1802.md
~~~

Then read:

~~~text
docs/reports/sprint3_dashboard_browser_manual_smoke_plan.md
docs/reports/sprint3_dashboard_same_origin_no_db_mock_capability_plan.md
docs/reports/sprint3_dashboard_production_url_resolution_plan.md
docs/reports/sprint3_dashboard_production_url_resolution_reliability_review.md
docs/reports/sprint3_dashboard_production_url_resolution_reliability_rereview.md
docs/reports/sprint3_dashboard_production_url_resolution_data_quality_review.md
docs/reports/sprint3_dashboard_production_url_resolution_verification_review.md
~~~

Planning, review, implementation, tests, runtime, and commit are separate PM authorizations. Exact allowlists are hard fences; extra needed scope is HOLD.

## 3. Live durable baseline

~~~text
branch: main
HEAD == origin/main: d75c5477251de1b60f7a16e5d8803fd7c20f5b38
latest commit: d75c547 Repair Dashboard URL resolution resolver contract
ahead/behind: 0 0
cached diff: empty
tracked diff: .gitignore only
handoff target before creation: absent
~~~

This handoff is untracked after creation and is not staged, committed, or pushed here.

## 4. Current Dashboard URL-resolution gate state

~~~text
Endpoint:
GET /api/v2/production/accepted-station-events

Query keys only:
line_id
start_time
end_time
limit
cursor

Production fact authority:
production_accepted_station_event_fact
~~~

Forbidden fallback entities:

~~~text
raw_plc_sample
cycle_event
station_event
production_unit
quality_event
production_snapshot
production_events
~~~

Response envelope:

~~~text
outer exact keys: data, page
data exact key: items
page exact keys: next_cursor, limit
~~~

Exact item DTO: 22 own keys:

~~~text
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
~~~

~~~text
explicit null: legal where schema permits
missing required own key: illegal
unknown key: illegal
malformed 2xx: kind: "error"
accepted_at: accepted fact timestamp only
summary: current page only
non-ready state: must not retain stale data
~~~

## 5. Completed planning and review history

~~~text
53ade97 Freeze Dashboard production URL resolution planning
5922b4b Record Dashboard URL resolution Reliability HOLD
f4c24ea Repair Dashboard production URL resolution planning
62e1424 Close Dashboard URL resolution Reliability planning review
bb1935a Record Dashboard URL resolution Data Quality review
7784e54 Record Dashboard URL resolution Verification HOLD
d75c547 Repair Dashboard URL resolution resolver contract
~~~

- 5922b4b records the original Reliability HOLD.
- f4c24ea repairs REL-URL-R1 and REL-URL-R2.
- 62e1424 closes the Reliability planning HOLD.
- bb1935a records the Data Quality review.
- 7784e54 records the Verification HOLD.
- d75c547 repairs only VER-URL-V1 planning authority; it does not close Verification.

## 6. VER-URL-V1 repaired authority

Exact public contract:

~~~ts
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
  | {
      readonly ok: true;
      readonly origin: TrustedAcceptedEventsApiOrigin;
    }
  | {
      readonly ok: false;
      readonly code: OriginConfigurationErrorCode;
      readonly message:
        "Accepted events service is not configured.";
    };

export function resolveTrustedAcceptedEventsApiOrigin(
  environment?: AcceptedEventsApiOriginEnvironment
): AcceptedEventsApiOriginResolution;
~~~

~~~text
Production call: resolveTrustedAcceptedEventsApiOrigin()
Test call: resolveTrustedAcceptedEventsApiOrigin(testEnvironment)
Configuration failures: non-throwing
Success own keys: ok, origin
Failure own keys: ok, code, message
Safe UI message: Accepted events service is not configured.
Brand creator: resolver success path only
Global process.env proxy: forbidden
Production test-only reset/export: forbidden
~~~

Exact-read test seam:

- Use a typed local environment object; its two getters are independently counted.
- Success reads each property once; every failure path reads each property once.
- Snapshot the pair, then make zero source rereads. Request-time reread is proven separately.
- Tests restore process.env exactly; no mutation or proxy of global process.env may observe reads.

### Safe-code precedence

~~~text
1. ORIGIN_MISSING
2. PROFILE_MISSING
3. ORIGIN_EMPTY
4. PROFILE_EMPTY
5. PROFILE_UNSUPPORTED
6. raw safety/canonicality validation
7. profile matching
8. URL parsing
9. parsed-component re-verification
~~~

~~~text
raw noncanonical: ORIGIN_NON_CANONICAL
canonical form for another known profile: ORIGIN_PROFILE_MISMATCH
new URL failure after raw checks: ORIGIN_MALFORMED
parsed/profile identity conflict: ORIGIN_PROFILE_MISMATCH
~~~

### Logging boundary

~~~text
event marker: DASHBOARD_API_ORIGIN_CONFIGURATION_ERROR
dedupe: one log per safe code per process
state: finite Set<OriginConfigurationErrorCode>
raw values: never logged
logging failure: must not alter resolver result
dedupe reset: process restart or Vitest module reset
production reset export: forbidden
~~~

## 7. Remaining findings and carry-forward

### Reliability: PASS WITH RECOMMENDATIONS

~~~text
CLOSED:
REL-URL-R1
REL-URL-R2
REL-URL-R7

CLOSED WITH CARRY-FORWARD:
REL-URL-R3
REL-URL-R4
REL-URL-R5
REL-URL-R6
~~~

VER-URL-V1 repair changes the resolver contract, so focused Reliability re-review is required.

~~~text
REL-URL-R3: single immutable request-time snapshot and test proof
REL-URL-R4: bounded/redacted/non-throwing logging proof
REL-URL-R5: serial exact environment test isolation
REL-URL-R6: future deployment readiness, alerting and diagnostics
~~~

### Data Quality: PASS WITH RECOMMENDATIONS

After Reliability, focused Data Quality re-review is required because repair added the failure union and safe error codes.

~~~text
DQ-URL-D1: transport profile versus business profile_id isolation tests
DQ-URL-D2: transport / synthetic fixture / real production evidence classification
DQ-URL-D3: full schema/query/viewModel/component regression evidence
~~~

### Verification: HOLD

~~~text
BLOCKER:
VER-URL-V1

CARRY-FORWARD:
VER-URL-V2
VER-URL-V3

VER-URL-V1: addressed in planning authority only
VER-URL-V1 closure: pending independent re-review
Verification gate: still HOLD
~~~

VER-URL-V2 is future client/static versus server bundle inspection. VER-URL-V3 is a dedicated runtime capture/fixture planning gate. Before runtime, freeze the exact capture method, request-counter evidence, zero/exactly-one request proof, temporary artifact allowlist, same-artifact hash, PID/port cleanup, /usr/sbin/lsof preflight, and evidence classification.

## 8. Exact future implementation boundary

Future separately authorized implementation may change exactly these six files:

~~~text
Create:
frontend/src/lib/acceptedStationEvents/apiOrigin.ts

Modify:
frontend/src/lib/acceptedStationEvents/apiClient.ts

Modify:
frontend/src/app/accepted-events/page.tsx

Create:
frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts

Modify:
frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts

Modify:
frontend/src/app/accepted-events/__tests__/page.test.tsx
~~~

New dependency: none.

Do not add helper files, logger files, test helper files, runtime fixture files, package.json, package-lock.json, next.config.ts, tsconfig.json, .env.example, docker-compose.yml, README.md, schema.ts, query.ts, viewModel.ts, loading.tsx, or error.tsx. A needed expansion is HOLD.

## 9. Runtime and mock-capability boundary

Original issue:

~~~text
Server Component used a relative fetch URL.
Runtime feasibility probe result: RELATIVE_URL_PRE_HTTP_FAILURE
The request failed before HTTP issuance.
Observed accepted-events API GET count: 0
~~~

A custom server or mock cannot intercept an unissued request. Same-origin no-DB mock-capability planning remains HOLD. Absolute URL resolution is future mock-recovery prerequisite only, not mock implementation.

Current frontend tooling:

~~~text
npm test: vitest run --environment jsdom
npm run typecheck: tsc --noEmit
npm run build: next build

Next: 16.2.10
React: 19.2.7
TypeScript: 6.0.3
Vitest: 4.1.10
jsdom: 28.0.0
~~~

There is no standalone Vitest config. next.config.ts uses output: "standalone". There is no frontend Docker service, no frontend env variables in .env.example, and no capture/fixture runtime helper.

## 10. External dirty artifacts to preserve

Do not stage, delete, rename, clean, or include these external artifacts in a handoff commit:

~~~text
M .gitignore

?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
?? frontend/node_modules/
~~~

## 11. What is not authorized

~~~text
Reliability re-review
Data Quality re-review
Verification re-review
Security/privacy review
implementation
apiOrigin.ts creation
apiClient/page changes
test edits
test execution
typecheck
build
bundle inspection
generated artifact cleanup
runtime planning
runtime validation
capture/fixture
server/browser/mock
API/DB/Postgres/Docker
deployment/config changes
status sync
tag
rollback
~~~

A new exact PM prompt is required for every later gate.

## 12. Recommended next gate sequence

Each step requires separate PM authorization:

~~~text
1. focused Reliability re-review
2. exact-path Reliability re-review authority commit
3. focused Data Quality re-review
4. exact-path Data Quality re-review authority commit
5. Verification re-review
6. exact-path Verification re-review authority commit
7. focused Security/privacy planning review
8. PM implementation authorization decision
9. six-file implementation
10. focused/full tests, typecheck and build
11. implementation cross-functional reviews
12. implementation commit/push
13. dedicated runtime planning gate
14. same-artifact runtime validation
~~~

Next and only recommended action:

~~~text
Focused Reliability re-review of the repaired VER-URL-V1
planning authority at commit d75c547.
~~~

Do not start Data Quality, Verification, or implementation directly.

### Focused Reliability re-review emphasis

Decide only whether:

- the non-throwing result union is reliable;
- eight-code precedence is deterministic and fail closed;
- the typed environment seam preserves the production boundary;
- getter tests prove each property is read once;
- snapshotting gives zero rereads and page/client make zero environment reads;
- logging is finite, redacted, and non-throwing;
- vi.resetModules() isolates dedupe and exact environment restore rules hold;
- the six-file allowlist remains sufficient; and
- VER-URL-V2/VER-URL-V3 stay in later gates.

Do not reopen closed URL canonicalization design unless a direct contradiction is found.

## 13. Handoff commit gate

~~~text
This task creates the handoff only.
The handoff is not staged, committed or pushed.
A new explicit PM exact-path commit authorization is required.
~~~

Future commit allowlist only:

~~~text
docs/thread_handoff/chatgpt_pm_handoff_260712-0950.md
~~~

Suggested message:

~~~text
Add PM handoff after Dashboard resolver planning repair
~~~

This task must not execute that commit.

## 14. Copyable restore prompt for next PM

~~~text
You are the Edge MES Demo ChatGPT PM.

Project path:
/Users/chenjie/Documents/MES/edge-mes-demo

Read this handoff first:
docs/thread_handoff/chatgpt_pm_handoff_260712-0950.md

First action is read-only recovery. Run and report the recovery conclusion before any review:

cd /Users/chenjie/Documents/MES/edge-mes-demo
git status -sb
printf '\n--- log -16 ---\n' && git log --oneline -16
printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
printf '\n--- origin/main ---\n' && git rev-parse origin/main
printf '\n--- ahead/behind ---\n' && git rev-list --left-right --count origin/main...HEAD
printf '\n--- diff name-only ---\n' && git diff --name-only
printf '\n--- cached name-only ---\n' && git diff --cached --name-only
printf '\n--- status all ---\n' && git status --short --untracked-files=all

Expected baseline:
HEAD == origin/main == d75c5477251de1b60f7a16e5d8803fd7c20f5b38
latest commit: d75c547 Repair Dashboard URL resolution resolver contract
ahead/behind: 0 0
cached diff: empty

Preserve external artifacts; do not stage, delete, rename, clean, or include:
M .gitignore
?? docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
?? docs/reports/phase1_to_sprint2_management_keynote_10p.html
?? docs/reports/sprint3_db_backed_api_validation_reliability_review.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260624.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
?? docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md
?? frontend/node_modules/

Verification remains HOLD. VER-URL-V1 is addressed in planning authority only; independent closure is pending. The only next technical gate is focused Reliability re-review of repaired planning authority at d75c547.

This prompt does not authorize Reliability re-review, Data Quality review, Verification review, implementation, tests, typecheck, build, bundle inspection, runtime, server/browser/mock, capture/fixture, API/DB/Postgres/Docker, config/deployment changes, or commit/push. First report recovery conclusion, then wait for PM gate instruction.
~~~

## 15. Thread/context assessment

~~~text
Current PM context: high load but coherent
Reason for handoff: completed durable planning-repair boundary before a new review branch
Recommended next PM window: new
Recommended first technical gate: focused Reliability re-review
Current implementation readiness: no
Current runtime readiness: no
~~~
