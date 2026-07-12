# ChatGPT PM Handoff — 2026-07-12 17:50 UTC+8

报告名称：Edge MES Demo ChatGPT PM handoff after Dashboard URL-resolution regression/build/bundle closeout

任务名称：Transfer PM ownership before the new Level 2 runtime-evidence planning branch

执行角色：ChatGPT PM

```text
Dashboard production URL-resolution six-file implementation: completed, uncommitted
Direct https://api1.example production-positive test repair: PASS
Focused apiOrigin test execution: PASS, 57/57 tests passed
Focused Verification test-completeness review: PASS WITH RECOMMENDATIONS
Original focused-test completeness HOLD: CLOSED
Full frontend regression: PASS, 11/11 files and 277/277 tests passed
DQ-URL-D3: CLOSED
Frontend TypeScript typecheck: PASS
Frontend Next.js build: PASS
Static browser bundle leakage inspection: PASS
Server bundle classification: PASS
VER-URL-V2: CLOSED
Generated build artifacts: cleaned
VER-URL-V3 / DQ-URL-D2 runtime evidence planning: not started, not authorized
REL-URL-R6: carry-forward
same-origin no-DB mock capability: independent HOLD
Current global gate: HOLD
Implementation staged/committed/pushed: no / no / no
```

This handoff is created at a natural phase boundary. The current PM window recovered the
repository, resolved the single focused-test completeness HOLD, completed the focused
execution/review chain, closed the full frontend regression gate, completed typecheck,
build and static bundle inspection, and cleaned all build artifacts. The next task opens
a new Level 2 runtime-evidence branch with capture, ports, PIDs, same-artifact identity,
strict fixture and cleanup design. It must be started by a fresh PM rather than continued
from conversational momentum.

## 1. First action for the next PM: read-only recovery

Project path:

```text
/Users/chenjie/Documents/MES/edge-mes-demo
```

The next PM must begin with read-only recovery. Do not create the runtime plan, run tests,
run typecheck/build, start Next or a capture service, bind ports, create temporary files,
update docs/status, or perform Git writes before this recovery.

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
printf '\n--- generated artifacts ---\n'
for artifact_path in \
  frontend/.next \
  frontend/next-env.d.ts \
  frontend/tsconfig.tsbuildinfo
do
  if [ -e "$artifact_path" ]; then
    printf 'PRESENT %s\n' "$artifact_path"
  else
    printf 'ABSENT  %s\n' "$artifact_path"
  fi
done
```

Expected committed baseline at handoff creation:

```text
branch:
main

HEAD == origin/main ==
20b9446d7cdd27811281db4c81528d64279d9c12

latest commit:
20b9446 Add PM handoff at Dashboard URL test HOLD

ahead/behind:
0 0

cached diff:
empty
```

Expected generated-artifact state:

```text
ABSENT frontend/.next
ABSENT frontend/next-env.d.ts
ABSENT frontend/tsconfig.tsbuildinfo
```

If this handoff is later committed and pushed, a lawful handoff-only forward commit is
acceptable only after exact-path verification. Unknown source, test, package, config,
runtime, DB, Docker, deployment or Git drift is `HOLD`.

Do not pull, fetch, merge, rebase, reset, restore or clean during recovery.

## 2. PM authority and status precedence

Read first:

```text
docs/thread_handoff/pm_operating_rules.md
docs/thread_handoff/chatgpt_pm_handoff_260712-1750.md
docs/thread_handoff/chatgpt_pm_handoff_260712-1551.md
docs/current_status.md
docs/contracts/dashboard_api_contract.md
docs/reports/sprint3_dashboard_production_url_resolution_plan.md
docs/reports/sprint3_dashboard_production_url_resolution_reliability_rereview.md
docs/reports/sprint3_dashboard_production_url_resolution_data_quality_review.md
docs/reports/sprint3_dashboard_production_url_resolution_verification_review.md
```

The latest direct PM authority is this file:

```text
docs/thread_handoff/chatgpt_pm_handoff_260712-1750.md
```

`docs/current_status.md` does not contain the latest URL-resolution implementation,
focused repair, full regression, typecheck, build or bundle-closeout state. When it
differs, use this precedence:

```text
live Git
+ latest PM handoff
+ committed URL-resolution authority/review documents
+ accepted PM intake reports recorded in this handoff
```

Do not silently update `docs/current_status.md`. Status sync remains a separate future
Architecture / Integration task.

PM owns:

```text
live recovery
risk classification
exact task prompts and allowlists
professional report intake
gate decisions
authorization boundaries
exact-path Git writes only after explicit user approval
```

Professional Threads own:

```text
Architecture / Integration:
planning, implementation, integration boundaries, repair and docs/status sync

Reliability:
fail-closed behavior, operational resilience, PID/port/recovery and deployment constraints

Data Quality:
fact authority, evidence classification, strict fixture semantics and projection

Verification:
test completeness, regression, build/bundle/runtime evidence and exact allowlist audit
```

No PASS automatically authorizes a later review, runtime, deployment, docs sync, stage,
commit or push.

## 3. Live repository state at handoff creation

Read-only recovery at 2026-07-12 17:50 UTC+8 confirmed:

```text
branch: main
HEAD: 20b9446d7cdd27811281db4c81528d64279d9c12
origin/main: 20b9446d7cdd27811281db4c81528d64279d9c12
ahead/behind: 0 0
cached diff: empty
```

Recent committed history:

```text
20b9446 Add PM handoff at Dashboard URL test HOLD
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
```

No implementation file has been staged, committed or pushed in the current URL-resolution
implementation sequence.

## 4. Current six-file implementation

Exact implementation set:

```text
M  frontend/src/app/accepted-events/__tests__/page.test.tsx
M  frontend/src/app/accepted-events/page.tsx
M  frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
M  frontend/src/lib/acceptedStationEvents/apiClient.ts
?? frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
?? frontend/src/lib/acceptedStationEvents/apiOrigin.ts
```

Current status:

```text
implementation completed: yes
implementation staged: no
implementation committed: no
implementation pushed: no
```

Implementation summary:

```text
apiOrigin.ts:
- server-process environment only;
- one origin read and one profile read per resolver invocation;
- closed local/container/production grammar;
- production numeric-IP/IP-literal rejection before native URL parsing;
- native ORIGIN_MALFORMED path;
- success-only origin brand creation;
- bounded redacted once-per-code logging with logger-throw containment.

apiClient.ts:
- accepts validated query and TrustedAcceptedEventsApiOrigin;
- fixed absolute accepted-events endpoint;
- URLSearchParams query authority;
- GET, cache no-store, credentials omit, redirect error;
- one request, no retry, no fallback.

page.tsx:
- query validation before resolver;
- resolver before client/fetch;
- configuration failure before outbound request;
- safe fixed browser error;
- no stale ready/table/summary/NOK/trace/cursor surfaces.
```

Files explicitly outside the implementation:

```text
frontend/src/lib/acceptedStationEvents/query.ts
frontend/src/lib/acceptedStationEvents/schema.ts
frontend/src/lib/acceptedStationEvents/viewModel.ts
frontend/src/components/accepted-events/**
frontend/package.json
frontend/package-lock.json
frontend/next.config.ts
frontend/tsconfig.json
API / DB / Docker / Compose / deployment
```

## 5. Known external dirty artifacts

These are pre-existing external artifacts. Their presence is not unknown drift. They must
remain excluded from all current implementation, planning, validation and Git allowlists
unless separately authorized:

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
?? docs/thread_handoff/chatgpt_pm_handoff_260712-1750.md
```

Do not edit, delete, clean, stage or commit these artifacts as part of the URL-resolution
branch. Treat `frontend/node_modules/` as one local dependency directory; do not expand it
with full untracked output during routine recovery.

## 6. Dashboard frozen consumer contract

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

Response envelope:

```text
outer exact own keys:
data
page

data exact own key:
items

page exact own keys:
next_cursor
limit
```

Every item contains exactly the frozen 22 required own keys:

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

Must preserve:

```text
explicit permitted null: legal
missing required key: illegal
unknown key: illegal
malformed 2xx: generic error
accepted_at: accepted-fact timestamp only
summary: current page only
non-ready state: no stale table/summary/NOK/trace/cursor
transport profile: never response-owned business profile_id
```

Forbidden fallback/substitution behavior:

```text
raw/candidate/review event substitution
legacy/current endpoint fallback
static fixture as production truth
previous ready-result reuse
relative/default/fallback API URL
transport-profile-based fact selection or filtering
```

## 7. Frozen resolver contract

Public error codes:

```text
ORIGIN_MISSING
PROFILE_MISSING
ORIGIN_EMPTY
PROFILE_EMPTY
PROFILE_UNSUPPORTED
ORIGIN_NON_CANONICAL
ORIGIN_PROFILE_MISMATCH
ORIGIN_MALFORMED
```

Failure message:

```text
Accepted events service is not configured.
```

Success exact own keys:

```text
ok
origin
```

Failure exact own keys:

```text
ok
code
message
```

Must preserve:

```text
raw grammar before new URL()
one origin read per invocation
one profile read per invocation
request-time snapshot
bounded once-per-code logging
raw-value redaction
logger throw containment
resolver-only brand creation
fixed absolute endpoint
GET
cache: no-store
credentials: omit
redirect: error
one request
no retry
no fallback
```

Production IP-like vectors remain `ORIGIN_NON_CANONICAL`:

```text
https://127.0.0.1
https://127.1
https://0177.0.0.1
https://0x7f.0.0.1
https://[::1]
```

Native malformed vector remains:

```text
https://xn--a.example -> ORIGIN_MALFORMED
```

## 8. Focused test HOLD repair and closure

Original blocker at the start of this PM window:

```text
frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts

missing direct production-positive resolver assertion:
https://api1.example / production
```

Architecture / Integration added exactly this direct matrix case:

```text
["https://api1.example", "production"]
```

At handoff creation it is present at line 68 and uses the public resolver:

```text
resolveTrustedAcceptedEventsApiOrigin(...)
```

The existing matrix assertions prove:

```text
success exact own keys
ok === true
canonical origin === new URL(origin).origin
```

No source repair was required. `apiOrigin.ts` already accepted this FQDN.

### Focused execution evidence

Accepted Verification evidence:

```text
Node: v22.23.0
Exact command:
npm test -- src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts --reporter=verbose
Exit code: 0
Test files: 1 passed
Tests: 57 passed
Failed: 0
Skipped: 0
Unhandled errors/rejections: none
```

Direct verbose case:

```text
accepts the exact https://api1.example origin under its selected profile
```

Result:

```text
PASS
```

### Focused Verification re-review

Accepted conclusion:

```text
PASS WITH RECOMMENDATIONS
Original focused-test completeness blocker: CLOSED
Verification focused implementation conformance: PASS
Verification focused-test completeness: PASS
```

The following existing coverage remained intact:

```text
https://accepted-api.example
https://accepted-api.example/
https://xn--bcher-kva.example
https://1.api.example
local/container/production positive matrix
production IP-like negative matrix
native malformed vector
error precedence
exact environment read counts
bounded logging
redaction
logger-throw containment
success/failure exact own keys
```

## 9. Full frontend regression — DQ-URL-D3

Accepted Verification execution evidence:

```text
Node: v22.23.0
Exact command: npm test
Exit code: 0
Test files: 11 total / 11 passed / 0 failed
Tests: 277 total / 277 passed / 0 failed
Skipped: none reported
Unhandled errors/rejections: none reported by Vitest
Duration: 942ms
```

The unfiltered suite included:

```text
query
schema
viewModel
apiClient
apiOrigin
accepted-events page
accepted-events components
```

The regression protected:

```text
fixed endpoint and five query keys
opaque cursor
exact envelope and 22-key DTO
explicit null versus missing/unknown
malformed 2xx and non-2xx/network classification
one request/no retry/no fallback
stale-state removal
current-page-only summary
accepted_at semantics
response-owned profile_id isolation
forbidden raw/candidate/debug/legacy leakage
https://api1.example production-positive coverage
```

Gate state:

```text
DQ-URL-D3: CLOSED
Full frontend regression: PASS
```

## 10. TypeScript typecheck

Accepted Verification execution evidence:

```text
Node: v22.23.0
Exact command: npm run typecheck
Exit code: 0
TypeScript errors: 0
Warnings: 0 in command output
Tracked file changes: none
```

`frontend/tsconfig.tsbuildinfo` was absent before typecheck, generated by typecheck, and
removed through the exact authorized path. `frontend/.next` and `frontend/next-env.d.ts`
were not generated.

Final typecheck artifact state:

```text
ABSENT frontend/tsconfig.tsbuildinfo
ABSENT frontend/next-env.d.ts
ABSENT frontend/.next
```

Gate state:

```text
Frontend TypeScript typecheck: PASS
VER-URL-V2 typecheck component: PASS
```

Operational note: the execution Thread initially used zsh-reserved variable names
`status` and later `path` in command wrappers. The authorized typecheck was rerun with a
valid wrapper and produced exit code 0; read-only audit confirmed no source or Git drift.
Future shell tasks should use names such as `command_rc` and `artifact_path`.

## 11. Frontend build

Accepted Verification execution evidence:

```text
Node: v22.23.0
Next.js: 16.2.10 (Turbopack)
Exact command:
/usr/bin/env -u EDGE_MES_DASHBOARD_API_ORIGIN \
  -u EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE \
  npm run build
Exit code: 0
Compile: success
Build: success
Accepted-events route: ƒ /accepted-events
Warnings/errors/unhandled errors: none in build output
Raw origin/profile output: none
```

Both URL configuration variables were absent before the forced-unset build. Build output
showed no API/network request error, but this is not runtime zero-request evidence.

Build artifact identity:

```text
BUILD_ID:
nrtuEYYirxmutGEkb0OVv

frontend/.next/standalone/server.js SHA-256:
ad9b19004dcd986a44734acc5c3d41e40d139aac202f65793c821f917644b6d9
```

Build generated:

```text
frontend/.next/
frontend/next-env.d.ts
```

It did not generate:

```text
frontend/tsconfig.tsbuildinfo
```

Build-sensitive tracked files remained unchanged:

```text
frontend/tsconfig.json
frontend/next.config.ts
frontend/package.json
frontend/package-lock.json
```

Gate state:

```text
Frontend Next.js build: PASS
VER-URL-V2 build component: PASS
```

## 12. Static client/server bundle inspection — VER-URL-V2 closeout

The bundle Thread inspected the same preserved build artifact and rechecked both identity
values before cleanup.

Artifact counts:

```text
frontend/.next/static/** files: 12
frontend/.next/server/** files: 109
```

Browser static bundle markers all returned no matches:

```text
EDGE_MES_DASHBOARD_API_ORIGIN: NONE
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: NONE
resolveTrustedAcceptedEventsApiOrigin: NONE
acceptedStationEvents/apiOrigin: NONE
NEXT_PUBLIC_EDGE_MES_DASHBOARD_API_ORIGIN: NONE
NEXT_PUBLIC_EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE: NONE
```

Server artifacts were present:

```text
frontend/.next/server/app/accepted-events/page.js
frontend/.next/server/app/accepted-events/page.js.map
```

Resolver/config markers were found in server-side chunks/source maps. This is expected
server-residency evidence and is not browser leakage.

Build-sensitive tracked status and diff remained empty. Cached diff remained empty.

Only the two build-created paths were removed:

```text
frontend/.next
frontend/next-env.d.ts
```

Final state:

```text
ABSENT frontend/.next
ABSENT frontend/next-env.d.ts
ABSENT frontend/tsconfig.tsbuildinfo
```

Gate state:

```text
Static browser bundle leakage inspection: PASS
Server bundle classification: PASS
VER-URL-V2 static bundle component: PASS
VER-URL-V2: CLOSED
```

## 13. Current gate state

Current global state:

```text
Dashboard production URL-resolution branch: HOLD
```

Closed in this PM window:

```text
Original https://api1.example focused-test blocker: CLOSED
Focused resolver execution: PASS
Focused Verification completeness: PASS
DQ-URL-D3: CLOSED
Frontend typecheck: PASS
Frontend build: PASS
Static client/server bundle inspection: PASS
VER-URL-V2: CLOSED
```

Still open or carried forward:

```text
VER-URL-V3:
OPEN — dedicated runtime capture/request-count/same-artifact/cleanup evidence

DQ-URL-D2:
OPEN — transport/synthetic/real-production evidence classification

REL-URL-R6:
CARRY FORWARD — deployment/config/DNS/egress/readiness/diagnostics

same-origin no-DB mock capability:
independent HOLD
```

No current source/test repair blocker is known. The global `HOLD` now means the branch is
not eligible for status sync, Git writes, runtime or deployment until the remaining
separate gates are planned, reviewed and authorized.

## 14. Recommended next branch: runtime evidence planning

The next task has not been issued or executed.

Classification:

```text
Risk: Level 2
Owner: Architecture / Integration
Mode: planning-only / docs-only
```

Recommended exact edit allowlist:

```text
docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_plan.md
```

The path did not exist at the time this handoff was prepared. The next PM must recheck
before authorizing creation.

The planning task must freeze, without executing runtime:

```text
exact capture method and executable
exact Next and capture ports
/tmp run root and exact temporary-file allowlist
strict synthetic 22-key fixture
request counter and request log format
Phase A active-listener zero-request evidence
Phase B exactly-one-request evidence
one-build/same-artifact identity checkpoints
owned PID recording and TERM-only cleanup
/usr/sbin/lsof listener preflight and final release proof
failure evidence retention and cleanup/recovery order
DQ-URL-D2 three-way evidence classification
REL-URL-R6 boundary
future exact command/path/network/environment allowlist
```

Required phase semantics:

```text
Phase A:
origin/profile unset
capture listener active
one /accepted-events page request
safe configuration error
accepted-events capture count remains 0
no stale ready/table/summary/NOK/trace/cursor

Phase B:
same build artifact
new Next process after restart
one complete accepted origin/profile pair
one /accepted-events page request
capture count changes from 0 to exactly 1
GET fixed accepted-events endpoint
only frozen query keys
strict synthetic fixture consumed
no retry/fallback/second request
```

A local loopback capture may prove request-time resolver/client/SSR transport wiring, but
must not be claimed as production FQDN, DNS, TLS, egress or deployment evidence.

Future runtime report must separate:

```text
A. transport evidence
B. synthetic strict-contract fixture evidence
C. real production-fact evidence
```

For a local capture run, section C must state:

```text
Real production-fact evidence:
NOT EXECUTED / NOT CLAIMED
```

The planning Thread must not run build, Next, capture service, curl, port binding, tests,
typecheck, API/DB/Docker or create `/tmp` runtime files.

## 15. Required review and execution sequence after the runtime plan

Do not combine these gates:

```text
1. Architecture / Integration runtime-evidence planning
2. Reliability planning review
3. Data Quality planning review
4. Verification planning review / exact future-run allowlist audit
5. PM runtime execution authorization decision
6. Architecture / Integration runtime execution
7. Reliability runtime evidence review
8. Data Quality runtime evidence review
9. Verification runtime evidence / cleanup review
10. REL-URL-R6 deployment/config readiness planning and reviews
11. status/docs sync
12. exact-path implementation stage/commit/push
```

No planning PASS authorizes runtime. No runtime PASS authorizes deployment or Git writes.

## 16. REL-URL-R6 boundary

The next runtime branch must not close:

```text
REL-URL-R6
```

The later deployment/config readiness gate must separately cover:

```text
production environment ownership
production DNS
HTTPS/TLS
network egress/firewall
accepted-events API readiness
frontend service readiness
alerting
operator diagnostics
restart/config-correction procedure
production config/secret ownership
```

Local runtime evidence may provide input to that review but does not replace it.

## 17. Non-authorized surfaces

Until separately authorized, do not:

```text
run tests/typecheck/build
start Next or any capture service
bind ports or create PID/log/fixture/temp files
issue browser/curl requests
connect to API/DB/Docker/real services
modify frontend source/tests/package/config
modify API/DB/Docker/Compose/deployment
modify docs/current_status.md or README.md
stage/commit/push/tag/deploy/rollback
reset/restore/clean
```

The next task may create only the exact planning report after a fresh PM authorization.

## 18. Git safety for this handoff file

This handoff creation is authorized. Staging, committing and pushing it are not included
in the current authorization.

Created file:

```text
docs/thread_handoff/chatgpt_pm_handoff_260712-1750.md
```

Do not automatically stage it.

If the user later authorizes handoff Git writes, use exact-path staging only:

```bash
git add -- docs/thread_handoff/chatgpt_pm_handoff_260712-1750.md
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

The staged set must contain exactly:

```text
docs/thread_handoff/chatgpt_pm_handoff_260712-1750.md
```

Do not stage:

```text
.gitignore
six URL-resolution implementation files
old handoffs
reports/HTML external artifacts
frontend/node_modules/
```

## 19. Copyable prompt for the next ChatGPT PM window

```markdown
# Edge MES Demo — ChatGPT PM Handoff Restore

你现在接手 **Edge MES Demo** 项目的 ChatGPT PM 角色。

项目路径：

    /Users/chenjie/Documents/MES/edge-mes-demo

第一优先级：恢复上下文。不要直接创建 runtime plan，不要运行 runtime。

请先读取并遵守：

- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260712-1750.md
- docs/thread_handoff/chatgpt_pm_handoff_260712-1551.md
- docs/current_status.md
- docs/contracts/dashboard_api_contract.md
- docs/reports/sprint3_dashboard_production_url_resolution_plan.md
- docs/reports/sprint3_dashboard_production_url_resolution_reliability_rereview.md
- docs/reports/sprint3_dashboard_production_url_resolution_data_quality_review.md
- docs/reports/sprint3_dashboard_production_url_resolution_verification_review.md

最新、最直接的 PM authority：

    docs/thread_handoff/chatgpt_pm_handoff_260712-1750.md

`docs/current_status.md` 对 URL-resolution 分支滞后。差异时以 live Git、最新 handoff 和 URL authority/review documents 为准。

## 1. 第一动作：read-only recovery

不要编辑、不要运行 tests/typecheck/build、不要启动 Next/capture、不要 bind port、不要创建临时文件、不要 stage/commit/push。

执行：

    git status -sb
    printf '\n--- log -12 ---\n' && git log --oneline -12
    printf '\n--- HEAD ---\n' && git log -1 --format='%H %s'
    printf '\n--- origin/main ---\n' && git rev-parse origin/main
    printf '\n--- ahead/behind ---\n' && git rev-list --left-right --count HEAD...origin/main
    printf '\n--- diff name-only ---\n' && git diff --name-only
    printf '\n--- cached name-only ---\n' && git diff --cached --name-only
    printf '\n--- status normal ---\n' && git status --short --untracked-files=normal
    printf '\n--- generated artifacts ---\n'
    for artifact_path in frontend/.next frontend/next-env.d.ts frontend/tsconfig.tsbuildinfo; do
      if [ -e "$artifact_path" ]; then printf 'PRESENT %s\n' "$artifact_path"; else printf 'ABSENT  %s\n' "$artifact_path"; fi
    done

Expected pre-handoff-commit baseline：

    HEAD == origin/main ==
    20b9446d7cdd27811281db4c81528d64279d9c12

    latest commit:
    20b9446 Add PM handoff at Dashboard URL test HOLD

    ahead/behind:
    0 0

    cached diff:
    empty

Expected six-file implementation：

    M frontend/src/app/accepted-events/__tests__/page.test.tsx
    M frontend/src/app/accepted-events/page.tsx
    M frontend/src/lib/acceptedStationEvents/__tests__/apiClient.test.ts
    M frontend/src/lib/acceptedStationEvents/apiClient.ts
    ?? frontend/src/lib/acceptedStationEvents/__tests__/apiOrigin.test.ts
    ?? frontend/src/lib/acceptedStationEvents/apiOrigin.ts

Expected generated artifacts：

    ABSENT frontend/.next
    ABSENT frontend/next-env.d.ts
    ABSENT frontend/tsconfig.tsbuildinfo

If the handoff was committed/pushed, a later handoff-only HEAD is acceptable only after exact-path verification. Unknown source/test/package/config/runtime/DB/Docker/deployment drift is HOLD.

## 2. Current gate state

    https://api1.example focused repair: PASS
    focused apiOrigin tests: 57 passed
    focused-test completeness: CLOSED
    full frontend regression: 11 files / 277 tests passed
    DQ-URL-D3: CLOSED
    typecheck: PASS
    build: PASS
    static browser bundle leakage: PASS
    server bundle classification: PASS
    VER-URL-V2: CLOSED
    generated artifacts: cleaned

Remaining:

    VER-URL-V3: OPEN
    DQ-URL-D2: OPEN
    REL-URL-R6: CARRY FORWARD
    same-origin no-DB mock capability: HOLD
    global gate: HOLD

## 3. Next recommended task

After successful recovery, authorize a new Architecture / Integration Level 2 planning-only Thread.

Exact new-file allowlist：

    docs/reports/sprint3_dashboard_production_url_resolution_runtime_evidence_plan.md

The planning Thread must freeze exact capture method, ports, temp-root files, strict synthetic fixture, zero/exactly-one request evidence, one-build/same-artifact hashes, PID ownership, lsof preflight/release proof, failure recovery, DQ evidence classification and future run allowlist.

It must not run build, Next, capture, curl, port binding, tests, typecheck, API/DB/Docker or create runtime temp files.

After the plan, separately authorize Reliability, Data Quality and Verification planning reviews. Do not authorize runtime from planning PASS alone.

## 4. Git boundary

Implementation and this handoff are uncommitted. Do not stage/commit/push without explicit user authorization. External artifacts and node_modules remain excluded.
```

## 20. Final handoff state

At handoff creation:

```text
handoff file created:
docs/thread_handoff/chatgpt_pm_handoff_260712-1750.md

handoff staged: no
handoff committed: no
handoff pushed: no

implementation staged: no
implementation committed: no
implementation pushed: no

focused blocker: CLOSED
DQ-URL-D3: CLOSED
VER-URL-V2: CLOSED
VER-URL-V3 / DQ-URL-D2 planning: not started
runtime execution: not authorized
REL-URL-R6: carry-forward
same-origin no-DB mock capability: HOLD
current global gate: HOLD
```

The next PM must recover the live repository first and must not infer planning, runtime,
deployment, status-sync or Git authorization from this handoff alone.
