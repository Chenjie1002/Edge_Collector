# ChatGPT Mainline PM Handoff — Edge MES Demo — 2026-08-15 16:54 CST

> Handoff objective: transfer Mainline PM control after A1 / VP2-G5 `SKIPPED -> skip` runtime repair has completed local acceptance, Git publication, controlled Raspberry Pi deployment, remote runtime verification and exact production-path acceptance for the repaired result-code-3 path.
>
> Owner direction at handoff: enter PM Handoff now; the next Mainline PM will take over the project and lead the next product gate. This handoff transfers durable context and accepted state only. It does not itself authorize new product mutation, UI mutation, remote/DB/API execution, Docker lifecycle, Git publication, A1-S2, or FIELD workstream changes.

---

## 1. Project identity / outgoing workspace

Project: `Edge MES Demo`

Absolute root:

`/Users/chenjie/Documents/MES/edge-mes-demo`

Outgoing Devspace workspace observed during this handoff:

```text
workspaceId = ws_7b51332f20
mode = checkout
root = /Users/chenjie/Documents/MES/edge-mes-demo
```

The workspaceId is operational context only. The successor must independently open/reuse the checkout and re-establish live repository facts.

Current branch / publication baseline at handoff creation:

```text
branch = main
HEAD = 6226bf3fb716880a176f9eb642b8139cef3255a6
origin/main = 6226bf3fb716880a176f9eb642b8139cef3255a6
ahead/behind = 0/0
staged = EMPTY
tracked dirty = EMPTY
git diff --check = PASS
git diff --cached --check = PASS
```

Recent published commits:

```text
6226bf3 fix(collector): canonicalize skipped result token
1d63d2f feat(pm): publish Edge MES governance Skill v1
2530721 feat(a1): publish trusted station summary scope interaction
4cd48e6 docs(p1): close accepted production truth consumption phase
c361b15 feat(p1): publish process metrics bounded API local MVP
```

The repository has a large long-lived untracked governance/evidence corpus. At pre-handoff recovery, `git ls-files --others --exclude-standard` returned 1263 file-level entries before creating this handoff. `git status` also collapses some untracked directories, so raw status-entry counts may differ. Treat the corpus as external continuity: preserve/exclude it; never broad-clean, reset, stash, stage, adopt or normalize it.

---

## 2. Mandatory successor takeover order

The successor PM's first action must be strict **read-only PM takeover**.

Required order:

1. mechanically verify this handoff path, regular/non-symlink type, byte length and SHA-256 against the Owner takeover launcher;
2. read this handoff to EOF;
3. read `docs/thread_handoff/pm_operating_rules.md` sufficiently to restore current governance;
4. fresh-recover physical cwd, Git root, branch, HEAD, origin/main, ahead/behind, staged names, tracked dirty names, `git diff --check`, `git diff --cached --check`;
5. confirm the untracked corpus remains excluded and no foreign tracked mutation appeared;
6. independently read the G5 Final Verification, G5 closeout and current G5 Ledger listed below;
7. reconcile the accepted G5 state against `docs/current_status.md` and note that `docs/current_status.md` predates the 2026-08-15 G5 closeout;
8. read the current A1 Station Summary source/origin resolver and the already-accepted P1 production/API closeout before deciding the next data-first product gate;
9. report takeover status and wait for Owner direction unless the Owner's new prompt itself grants an exact next action.

No prior Goal/runner/Thread authority is inherited merely by reading this handoff.

---

## 3. PM Rules / governance authority

Authoritative PM Rules:

`docs/thread_handoff/pm_operating_rules.md`

Current identity at handoff creation:

```text
type = regular / non-symlink
bytes = 69697
SHA-256 = 45d4be226d2c4754fb2b21b55fce6f4086cb24e643b170f1ad1ab475a596bf9f
```

Important rules to restore before dispatching work:

- historical terminals are immutable;
- state fields are independent: `WRITTEN / REVIEWED / ACCEPTED / VERIFIED / STAGED / COMMITTED / PUSHED / DEPLOYED / ACTIVATED / RUNTIME_LOADED / PRODUCTION_ACCEPTED / OWNER_VISUAL_ACCEPTED`;
- local/static/synthetic evidence cannot be promoted into runtime/DB/production truth;
- new core tasks are normally unique repository-backed 16-section task files with self-identity as the first hard gate;
- exact allowlists/budgets/outputs/retry semantics must be explicit;
- execution-lock retry/reconnect/fallback is forbidden without fresh authority;
- Owner authority is current, explicit and scope-bounded;
- Goal mode requires Owner manual start; existence of a charter/prompt does not start it;
- no broad Git stage (`git add .`, `git add -A`, `git add docs/`);
- exact-path Git stage/commit/push requires explicit authority and cached-name/check/stat verification;
- preserve unrelated dirty/untracked state;
- runtime/source behavior remains Level 2 and requires proportionate independent review/verification;
- data-first MVP policy remains authoritative; UI-only debt is deferred unless it can display false production truth, hides a data/API defect, or the current deliverable is explicitly UI acceptance;
- `FIELD-VALIDATION-COLLECTOR-DB` remains an isolated workstream.

Published governance Skill v1 exists at `.agents/skills/edge-mes-pm-governance/` and is subordinate to PM Rules. It is explicit-only and grants no authority by existing in the repository.

---

## 4. Current high-level product state

The most important state change since the previous handoff is that the VP2-G5 data-path blocker is now **closed for the accepted repair path**.

Current accepted state:

```text
PUBLISHED_COMMIT = 6226bf3fb716880a176f9eb642b8139cef3255a6
COMMITTED = YES
PUSHED = YES
DEPLOYED = YES
ACTIVATED = YES
RUNTIME_LOADED = YES
REMOTE_VERIFIED = YES
WS02_ACCEPTED_SKIP_POST_ACTIVATION = YES
WS03_ACCEPTED_SKIP_POST_ACTIVATION = YES
PRODUCTION_ACCEPTED_FOR_THIS_REPAIR_PATH = YES
A1_VP2_G5_ACCEPTED = YES
OWNER_VISUAL_ACCEPTED = NO
A1_S2 = NOT_AUTHORIZED
```

Scope warning: `PRODUCTION_ACCEPTED_FOR_THIS_REPAIR_PATH=YES` means the exact result-code-3 / `SKIPPED -> skip` path has real remote production evidence. It is **not** a claim that every station, every historical window or the entire MES is universally production-ready.

---

## 5. P1 production truth / bounded API baseline remains accepted

The previously accepted P1 production-truth phase remains closed. Highest-priority `docs/current_status.md` block is still 0P from 2026-08-12 and records:

```text
P1_G6_PM_ACCEPTANCE = PASS
P1_PM_ACCEPTED = YES
P1_STATUS = COMPLETE / CLOSED
P1_PRODUCTION_TRUTH_TRUSTED_CONSUMPTION = COMPLETE
PRODUCTION_TRUTH_SOURCE_ACCEPTED = YES
QUALITY_SEMANTICS_ACCEPTED = YES
TRACE_SEMANTICS_ACCEPTED = YES
PROCESS_KPI_SEMANTICS_ACCEPTED = YES
BOUNDED_PRODUCTION_API_ACCEPTED = YES
DB_API_RECONCILIATION = PASS
REAL_RUNTIME_VALIDATED = YES
```

Durable P1 closeout:

`docs/reports/p1_g6_pm_acceptance_closeout_20260812T0902Z.md`

```text
bytes = 9284
SHA-256 = 13058397e9faf51f4076af0f45585f1fff7ae81c568b0ed96a26fffd6c2c9473
```

Accepted P1 scope does not claim Performance/Availability/full-OEE numeric authority or all-stations/all-history correctness.

---

## 6. A1 Trusted Station Summary UI state

Published interaction/UI slice commit:

```text
2530721080e4fdcf9ff1e806e06969aa56affdf5
feat(a1): publish trusted station summary scope interaction
```

A1-S1 was accepted as a usable prototype slice. Owner visual observations before the G5 repair included:

- overall page looked like an early product prototype rather than a raw test page;
- Line / Station / Start / End controls were understandable;
- Apply overlapped the End Time control in the observed preview;
- query returned a safe error instead of production values;
- UI finishing/shadcn work was deliberately deferred because Owner chose **data first**;
- `A1-S2 = NOT AUTHORIZED`.

Current Station Summary page source:

`frontend/src/app/station-summary/page.tsx`

```text
bytes = 6123
SHA-256 = 0bd1f057196c78a7496fa19d42e95893a6f2ad9efb8677dba008743216d35003
```

Current data client:

`frontend/src/lib/stationSummary/apiClient.ts`

```text
bytes = 5937
SHA-256 = 6f22988342741930087dbfc38044007e770affce36a6a5633373e11424cc146c
```

It consumes the already-established routes:

```text
GET /api/v2/production/quality
GET /api/v2/process-metrics
```

Scope catalog client:

`frontend/src/lib/stationSummary/scopeCatalog.ts`

```text
bytes = 5338
SHA-256 = 90d6768821fdd25e95b170fd9076d88b3abae0e41c847e879a6e1c6ccc4de29c
```

It consumes:

```text
GET /api/v2/production/scope-options
```

---

## 7. Current visible UI error must not be misclassified

The user-visible failure family previously observed included:

`Accepted events service is not configured.`

That exact safe message originates in:

`frontend/src/lib/acceptedStationEvents/apiOrigin.ts`

Current identity:

```text
bytes = 5667
SHA-256 = a5b07e11063625f868320942ecff401e2389cf02799051d9f798246f22352c61
```

`resolveTrustedAcceptedEventsApiOrigin()` requires both environment values:

```text
EDGE_MES_DASHBOARD_API_ORIGIN
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE
```

Allowed profiles are `local`, `container`, `production`, with strict origin/profile matching.

Important current static fact: committed `docker-compose.yml` already configures the Dashboard container with:

```text
EDGE_MES_DASHBOARD_API_ORIGIN = http://api:8000
EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE = container
```

Therefore the old local-preview error **must not** automatically be classified as “FastAPI route missing” or “backend broken”. A localhost/dev preview can simply lack the required environment binding. The successor should first perform a bounded read-only wiring/runtime diagnosis before authorizing any frontend/API source change.

Recommended diagnostic question:

```text
Is the current Station Summary failure caused by preview/runtime environment binding,
API runtime/deployment reachability, route/data availability, or actual product code?
```

Do not edit `apiOrigin.ts` merely to make local preview convenient unless a later product-level requirement explicitly changes the trusted-origin contract.

---

## 8. G5 exact defect and accepted repair

Accepted root cause:

```text
EXACT_CAUSE = RESULT_VOCABULARY_NORMALIZATION_MISMATCH
VALIDATION_FIELD = result
VALIDATION_CODE = RESULT_COMBINATION_INVALID
SOURCE_RESULT_CODE = 3
MAPPING_TOKEN = SKIPPED
RUNTIME_NORMALIZED_TOKEN = skipped
CANONICAL_TOKEN = skip
PRODUCT_DEFECT = COLLECTOR_RUNTIME_SOURCE_RESULT_CANONICALIZATION_DEFECT
PRIMARY_REPAIR_TARGET = collector/app/services/station_event_runtime_source.py::_decode_result
VALIDATOR_CONTRACT_CHANGE_REQUIRED = NO
VPLC_RESULT_CODE_CHANGE_REQUIRED = NO
```

Accepted source change in commit `6226bf3`:

```diff
-    return str(decoded).lower()
+    normalized = str(decoded).lower()
+    return "skip" if normalized == "skipped" else normalized
```

Current source identity:

`collector/app/services/station_event_runtime_source.py`

```text
bytes = 7790
SHA-256 = ee48d2cedf837d65970a76c618b7dd08748c422c9557b5d60c7ed06336910d2c
```

Current regression-test identity:

`tests/test_collector_station_event_runtime_source.py`

```text
bytes = 37617
SHA-256 = afdadc6f7c1fd6e5f3971a108d5a5d2667763bcef653d4a54bed892691cd059f
```

Local candidate was independently accepted before Git publication; focused GREEN was 6 passed and bounded regression 66 passed.

---

## 9. G5 final remote production evidence

Final accepted runtime result:

`docs/reports/mainline_pm_a1_vp2_g5_runtime_deployment_evidence_split_owner_runtime_result_r4.txt`

```text
bytes = 5658
SHA-256 = ff4c4489e58c0b37abba952d94ec2cf8766da4f27157133c6c26ba124d38f4fe
RUNNER_TERMINAL = PASS / DEPLOYMENT_AND_EVIDENCE_CAPTURE_COMPLETE
REMOTE_STATE = STABLE
```

Transport / candidate identity:

```text
LOCAL_MANIFEST_DIGEST = sha256:b8ced083941cdf9b8e39aefb69844a8f4b69e5dda1cbfdba134f35f26130eea6
TRANSPORT_CONFIG_DIGEST = sha256:f51a445aa93ba2d8e526095b9cedfc621ea49e82a70dd726eaebfd0cdac3b901
CANDIDATE_CONTAINER_ID = 5b30fe755991eb64f594232767b1fd68d93b110ec86bcb9b53c10b874b254bc5
CANDIDATE_ACTIVATION_FENCE = 2026-08-15T08:48:05.126654753Z
FORWARD_LIFECYCLE_COUNT = 1
ROLLBACK_LIFECYCLE_COUNT = 0
PROTECTED_CONTINUITY = PASS
DB_WRITES = 0
VPLC_ACTIONS = 0
PLC_ACTIONS = 0
```

WS02 accepted proof:

```text
station = WS02
cycle_counter = 112922
production_result = skip
accepted_at = 2026-08-15T16:48:06.050876+08:00
cycle_event.result = SKIPPED
ack_status = ACK_OK
terminal adapter rejection after fact = 0
runtime last_cycle_counter after observation = 112924
collector_state = RUNNING
last_error_code = null
ack_timeout = false
```

WS03 accepted proof:

```text
station = WS03
cycle_counter = 112922
production_result = skip
accepted_at = 2026-08-15T16:48:06.205839+08:00
cycle_event.result = SKIPPED
ack_status = ACK_OK
terminal adapter rejection after fact = 0
runtime last_cycle_counter after observation = 112923
collector_state = RUNNING
last_error_code = null
ack_timeout = false
```

Accepted chain:

```text
V-PLC result code 3
-> mapping SKIPPED
-> repaired runtime source canonicalizes to skip
-> adapter accepts
-> production fact = skip
-> cycle persists result = SKIPPED
-> ACK_OK
-> runtime progresses
```

The distinction `accepted fact production_result=skip` versus `cycle_event.result=SKIPPED` is intentional. Storage persists the raw mapping code-table label for the cycle, while the accepted production semantic token is canonical `skip`.

---

## 10. G5 Final Verification / closeout durable authority

Final Verification:

`docs/reports/mainline_pm_a1_vp2_g5_runtime_deployment_evidence_split_final_verification.md`

```text
bytes = 9196
SHA-256 = 970411a834a55ef954b39088f21517058d892c20b72f52abbd7287550425beda
terminal = PASS / A1_VP2_G5_RUNTIME_DEPLOYMENT_EVIDENCE_SPLIT_VERIFIED
```

Closeout:

`docs/reports/mainline_pm_a1_vp2_g5_runtime_deployment_evidence_split_goal_closeout.md`

```text
bytes = 4176
SHA-256 = 3aa2c8fae31d7510bb0a8818aaec5cac91c37a72fb4b59d5c17cecb86c528d1a
terminal = PASS / A1_VP2_G5_RUNTIME_DEPLOYMENT_EVIDENCE_SPLIT_COMPLETE
```

Current Ledger:

`docs/reports/mainline_pm_a1_vp2_g5_runtime_deployment_evidence_split_shadow_pm_ledger.md`

```text
bytes = 15206
SHA-256 = 1ded9646c4f4f2b4b05fbe4820add45eafdac9972a1f244081df0b78b69f9eea
```

These three artifacts were written locally and are part of the untracked durable corpus at handoff. `WRITTEN`/accepted status does not mean these governance reports were committed or pushed.

---

## 11. Historical G5 runner HOLDs — preserve, do not restart

Several control-plane/harness HOLDs occurred before the final R4 success. They are immutable history and should not be restarted merely because they exist:

1. original split R1 Reliability: `HOLD / RESULT_SINK_FOREIGN_OBJECT_OVERWRITE_RACE`;
2. first PM-direct runner: local Docker Go-template quoting defect, stopped before SSH;
3. successor: SSH parameter values containing `|` were reinterpreted by the remote shell, stopped before lifecycle;
4. R2 continuation: projection comparison HOLD before lifecycle;
5. R3 fieldwise: exposed Docker Desktop/containerd versus Raspberry Pi Docker Engine image identity semantics, stopped before lifecycle;
6. R4 transport-bound correctly bound local OCI manifest digest to archive config digest / remote Engine image ID and completed the one Collector forward lifecycle.

Critical transport lesson:

```text
local Docker Desktop image/index/manifest identity = b8ced083...
docker save Config digest                         = f51a445a...
remote Docker Engine load Image.Id                = f51a445a...
```

Do not reintroduce a cross-engine rule requiring local Docker Desktop `.Id` to equal remote Docker Engine `.Id` when the archive explicitly maps manifest digest -> config digest.

The monolithic historical `CONTROLLED-RUNTIME-REPAIR-VERIFICATION` Goal and its R1/R2 runners are superseded. Do not reopen them.

---

## 12. Latest prior handoff / accepted RCA lineage

Previous Mainline handoff:

`docs/thread_handoff/chatgpt_pm_handoff_260814-2303.md`

```text
bytes = 28849
SHA-256 = c1778d493d218d87bf139b94a0f8971ea1ecaee3fe0a5cd5539c222178a88646
```

Accepted cross-station RCA intake:

`docs/reports/mainline_pm_a1_vp2_g5_cross_station_focus_only_db_rca_r3_parent_independent_intake_20260814T1327Z.md`

```text
bytes = 9406
SHA-256 = fe85332451c150b1f26fb338508953cfc757426dff5892710203fd758657ed7a
```

Accepted exact-cause intake:

`docs/reports/mainline_pm_a1_vp2_g5_adapter_result_combination_invalid_cause_isolation_r2_order_unambiguous_dependency_free_parent_independent_intake_20260814T1438Z.md`

```text
bytes = 11015
SHA-256 = 8f5bce19d45e36a7575035e217c11292ac145d60af9c9e9ece634f72d1a176ca
```

Local repair closeout:

`docs/reports/mainline_pm_a1_vp2_g5_local_candidate_independent_closeout_goal_closeout.md`

```text
bytes = 10839
SHA-256 = 53c291c0305b1b55a1aac988ac9ad918d27a69b82f08b1af0b86978c37f57970
```

Focused Reliability:

`docs/reports/mainline_pm_a1_vp2_g5_local_candidate_reliability_focused_review_20260815T0128Z.md`

```text
bytes = 8643
SHA-256 = f8fd9b9eb248c7852d3906dfbd4351f20a1a5e12b5f7896a6cb7afe61f6c88ff
```

Focused Verification:

`docs/reports/mainline_pm_a1_vp2_g5_local_candidate_verification_focused_review_20260815T0142Z.md`

```text
bytes = 10248
SHA-256 = dd08c0fab03bb3709f5d64193d64ca4374a7277fb220a2fe8cbf3aa5356fa8f5
```

A historical closeout typo omitted the final `5` of the Verification SHA in one old document. The actual SHA above is authoritative; do not rerun verification merely to correct that historical typo.

---

## 13. docs/current_status.md synchronization boundary

`docs/current_status.md` current identity at handoff creation:

```text
bytes = 179192
SHA-256 = c74d1e32e76414c0535529889895ab6360e3e2068898472ee6b3f90fa18d6b5c
```

Its highest-priority control block is `0P. 2026-08-12 P1-G6 PM Acceptance`. It correctly captures P1 completion but **does not yet contain the 2026-08-15 A1 VP2-G5 runtime repair closeout**.

Therefore:

```text
LATEST_G5_DURABLE_AUTHORITY = Final Verification + Goal Closeout + current G5 Ledger
CURRENT_STATUS_G5_SYNC = PENDING / NOT PERFORMED IN THIS HANDOFF
```

This handoff explicitly records that pending sync, satisfying the handoff requirement to expose an unfinished docs/status reconciliation rather than silently treating the status file as current.

Do not overwrite historical sections. If the successor/Owner decides to synchronize `docs/current_status.md`, it should be a bounded governance/status action with an exact allowlist and a new highest-priority block, not bundled into unrelated product code or UI work.

---

## 14. Recommended next Mainline product direction — recommendation only

The outgoing PM recommendation is to return to the **data-first A1 product path**, not to continue runtime-harness work.

Recommended decision sequence:

```text
A. read-only successor takeover
B. reconcile latest G5 acceptance with current P1/API + A1 UI state
C. bounded read-only diagnosis of Station Summary trusted-origin / API wiring
D. only after exact cause is established, authorize the smallest product/runtime/config repair if one is actually needed
E. once real Station Summary data is visible and trustworthy, perform minimum proportional Owner visual acceptance/polish
F. A1-S2 remains a separate Owner decision
```

The immediate technical question should be whether the Station Summary's previously observed `Accepted events service is not configured.` / "trusted API not configured" condition is caused by:

- local preview environment variables not being bound;
- dashboard/container runtime environment drift;
- API deployment/reachability;
- scope-options / quality / process-metrics route availability;
- query/window mismatch;
- or a genuine frontend/API product defect.

Do not assume the answer in advance. Static repository facts already show the compose Dashboard profile has the required container origin variables, while ad-hoc localhost preview may not.

---

## 15. Suggested first new gate after takeover — NOT AUTHORIZED BY THIS HANDOFF

Suggested gate name:

`A1_STATION_SUMMARY_TRUSTED_ORIGIN_AND_REAL_DATA_WIRING_READONLY_DIAGNOSIS`

Recommended evidence class: read-only / diagnostic only.

Recommended initial read-only scope:

```text
docs/thread_handoff/pm_operating_rules.md
this handoff
G5 final verification / closeout / ledger
P1 G6 closeout
frontend/src/app/station-summary/page.tsx
frontend/src/lib/acceptedStationEvents/apiOrigin.ts
frontend/src/lib/stationSummary/apiClient.ts
frontend/src/lib/stationSummary/scopeCatalog.ts
api/app/main.py
api/app/routes/quality_trace.py
api/app/routes/process_metrics.py
api/app/routes/scope_options.py
docker-compose.yml
live Git metadata
```

Possible runtime reads, network/SSH, localhost server start or Raspberry Pi API checks are **not** granted by this handoff. If the Owner wants runtime diagnosis, the successor must materialize/receive the appropriate bounded authority first.

The desired diagnostic terminal should classify one concrete boundary, for example:

```text
LOCAL_PREVIEW_ENVIRONMENT_BINDING_MISSING
DASHBOARD_CONTAINER_ENVIRONMENT_DRIFT
API_RUNTIME_UNREACHABLE
SCOPE_CATALOG_UNAVAILABLE
QUALITY_OR_PROCESS_ROUTE_UNAVAILABLE
QUERY_SCOPE_MISMATCH
FRONTEND_PRODUCT_DEFECT
OTHER_EXACT_CAUSE
```

Avoid another broad “everything check” if one exact boundary can answer the user-visible failure.

---

## 16. Takeover read allowlist / non-authorized surfaces

For the successor's initial read-only takeover, the intended read allowlist is:

```text
1. this handoff
2. docs/thread_handoff/pm_operating_rules.md
3. docs/current_status.md
4. exact G5 final verification / closeout / ledger / R4 result referenced above
5. exact P1 G6 closeout referenced above
6. exact A1/frontend/API/docker-compose files referenced in Sections 6, 7 and 15
7. live Git metadata/diffs/status needed for recovery
```

Initial takeover write allowlist:

```text
NONE
```

Initial takeover external/runtime authority:

```text
NETWORK = 0
SSH = 0
REMOTE_FS = 0
DOCKER_LIFECYCLE = 0
DB_QUERY = 0
DB_WRITE = 0
HTTP_RUNTIME = 0
VPLC_ACTION = 0
PLC_ACTION = 0
PRODUCT_WRITE = 0
UI_WRITE = 0
GIT_STAGE = 0
GIT_COMMIT = 0
GIT_PUSH = 0
GIT_TAG = 0
GIT_RESET/STASH/CLEAN = 0
```

The successor may only expand these boundaries when the current Owner instruction or a fresh exact task grants that authority.

---

## 17. Independent FIELD workstream isolation

Parallel workstream:

`FIELD-VALIDATION-COLLECTOR-DB`

Purpose: real-device Collector + PostgreSQL field validation.

It shares the repository directory historically but remains governance-isolated from Mainline. Do not:

- absorb FIELD status into Mainline;
- stage or clean FIELD artifacts;
- use FIELD runtime observations as Mainline production evidence without explicit cross-workstream authority;
- allow Mainline tasks to mutate FIELD-owned files by convenience;
- infer that G5 Mainline acceptance closes FIELD validation.

---

## 18. Current Git / artifact publication state

Published product state:

```text
collector skip canonicalization source/test = COMMITTED + PUSHED at 6226bf3
A1 Station Summary interaction = COMMITTED + PUSHED at 2530721
P1 closeout/status = COMMITTED + PUSHED at 4cd48e6
```

The 2026-08-15 G5 runtime reports, runners, Ledger and this handoff are part of the local untracked durable corpus unless a later exact-path Git publication is separately authorized.

No handoff file is automatically staged. This handoff itself must remain unstaged/uncommitted unless the Owner separately authorizes exact-path stage/commit/push.

---

## 19. MVP path alignment

Current handoff state remains MVP-aligned.

Reasoning:

- the latest completed G5 work restored and proved a blocked real production data path rather than adding speculative capability;
- P1 bounded production API/semantics were already accepted;
- the next recommended work targets getting the already-designed Station Summary to consume real trusted data;
- UI cosmetics/shadcn remain deferred until data wiring is known good;
- no new genealogy, ERP/Oracle, generic observability platform, broad threat model, browser-forensics framework or full-OEE numeric claim is introduced here.

Current explicit out-of-scope / non-authorized expansion includes:

```text
Oracle / real ERP sync
full genealogy
full OEE numeric authority without source authority
all-stations/all-history universal correctness claim
A1-S2
broad Dashboard redesign
new UI framework migration solely for aesthetics
real PLC pilot
FIELD workstream absorption
```

---

## 20. Handoff stopping rule

This handoff is complete when:

- one unique handoff file is written;
- file identity and internal references are audited;
- live Git is rechecked;
- the successor prompt below is copyable;
- no staging/commit/push occurs without separate Owner authorization.

The outgoing PM must not start the suggested diagnosis in this same context after handoff completion.

---

## 21. Copyable next-PM takeover prompt

Copy the prompt below into a new ChatGPT PM window:

```text
你现在接手 Edge MES Demo 主线，担任新的 ChatGPT Mainline PM。

项目绝对路径：
/Users/chenjie/Documents/MES/edge-mes-demo

你的第一项工作是严格 read-only PM takeover。不要继续上一窗口的执行 momentum，也不要自动启动 Goal、task、SSH、Docker、DB/API runtime、测试、代码修改、UI 修改或 Git mutation。

第一硬门：机械核验并完整读取：

docs/thread_handoff/chatgpt_pm_handoff_260815-1654.md

Expected identity 由 Owner launcher 提供；必须先核对 regular/non-symlink、bytes、SHA-256。identity mismatch 立即 HOLD，不得用聊天摘要替代实际文件。

随后按 handoff Section 2 的顺序执行：
1. 读 handoff 到 EOF；
2. 读取 docs/thread_handoff/pm_operating_rules.md；
3. fresh read-only recovery：physical cwd、git root、branch、HEAD、origin/main、ahead/behind、staged、tracked dirty、git diff --check、git diff --cached --check；
4. 保留并排除既有 untracked corpus，禁止 broad clean/reset/stash/stage/adopt；
5. 独立读取 G5 Final Verification、G5 closeout、G5 Ledger 与 R4 runtime result；
6. 确认 6226bf3 是当前 HEAD/origin/main，且 accepted G5 state 是：DEPLOYED/ACTIVATED/RUNTIME_LOADED/REMOTE_VERIFIED=YES，WS02/WS03 accepted skip post-activation=YES，PRODUCTION_ACCEPTED_FOR_THIS_REPAIR_PATH=YES，A1_VP2_G5_ACCEPTED=YES；
7. 读取 P1 G6 closeout 与 A1 Station Summary / trusted-origin / API client / scope catalog 相关文件；
8. 明确 docs/current_status.md 尚未同步 2026-08-15 G5 closeout，不得让旧 status wording 覆盖最新 Final Verification/closeout；
9. 完成 takeover 后向 Owner 汇报 current state、non-authorized surfaces 和你建议的唯一 next gate，等待 Owner 决策。

重要产品方向：
- G5 runtime repair 已关闭，不要继续修旧 harness；
- 下一步回到 data-first A1 主线；
- 之前 UI 出现 “Accepted events service is not configured.” / trusted API not configured，先做 read-only trusted-origin / API wiring diagnosis；
- docker-compose 已为 dashboard container 配置 EDGE_MES_DASHBOARD_API_ORIGIN=http://api:8000 和 EDGE_MES_DASHBOARD_API_ORIGIN_PROFILE=container，因此不要直接假定 FastAPI 缺路由，也不要为了 localhost preview 随意弱化 apiOrigin 安全合同；
- UI/shadcn 视觉完善继续后置，A1-S2 未授权；
- FIELD-VALIDATION-COLLECTOR-DB 继续隔离。

治理原则：产品边界严格，编排机制轻量。不要为了治理再制造无限 runner/Goal 修复循环；真实 blocker 要 fail closed，但控制面机械缺陷应由 Mainline 在规则允许范围内直接、最小处理。

Takeover 期间 write allowlist = NONE，external/runtime/Git mutation authority = NONE。
```

---

## 22. Final handoff state

```text
MAINLINE_PM_HANDOFF = READY
PROJECT_ROOT = /Users/chenjie/Documents/MES/edge-mes-demo
BRANCH = main
HEAD = 6226bf3fb716880a176f9eb642b8139cef3255a6
ORIGIN_MAIN = 6226bf3fb716880a176f9eb642b8139cef3255a6
AHEAD_BEHIND = 0/0
STAGED = EMPTY
TRACKED_DIRTY = EMPTY
UNTRACKED_CORPUS = PRESERVE / EXCLUDE / DO_NOT_ADOPT

P1_STATUS = COMPLETE / CLOSED
A1_VP2_G5_ACCEPTED = YES
PRODUCTION_ACCEPTED_FOR_THIS_REPAIR_PATH = YES
OWNER_VISUAL_ACCEPTED = NO
A1_S2 = NOT_AUTHORIZED
CURRENT_STATUS_G5_SYNC = PENDING / EXPLICITLY RECORDED

NEXT_PM_FIRST_ACTION = READ_ONLY_TAKEOVER
RECOMMENDED_NEXT_PRODUCT_DECISION = A1_STATION_SUMMARY_TRUSTED_ORIGIN_AND_REAL_DATA_WIRING_READONLY_DIAGNOSIS
NEW_EXECUTION_AUTHORITY_GRANTED_BY_HANDOFF = NO
HANDOFF_STAGE_COMMIT_PUSH_AUTHORIZED = NO
```
