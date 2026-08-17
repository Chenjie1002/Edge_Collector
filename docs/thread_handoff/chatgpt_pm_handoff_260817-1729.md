# ChatGPT Mainline PM Handoff — Edge MES Demo — 2026-08-17 17:29 +08

## 1. Handoff objective and terminal state

本 handoff 将 Edge MES Demo 的 ChatGPT Mainline PM 控制权交给下一任 PM。

Owner 当前要求不是结束项目，而是：

1. 接受并冻结刚完成的 FV1B-A-R1 amd64 bundle refresh；
2. 下一任 PM 继续主导 FIELD-VALIDATION-COLLECTOR-DB 调试支线，下一 major gate 为真实 Wyse 3040 的 FV1B-B remote full-stack deployment qualification；
3. 调试支线结束后必须回归 Raspberry Pi / ARM64 正式主线；
4. Edge MES 第一个正式发布/投入应用的平台仍然是 Raspberry Pi / ARM64；只有 Raspberry Pi 版本成功投入实际应用后，才允许重新讨论 x86 正式产品线；
5. Mainline product work remains open；不得因 Wyse packaging PASS 宣称 MVP complete、x86 support、production release 或 platform migration。

交接时 authoritative state：

```text
MAINLINE_PM_INTAKE_FV1B_A_R1          = PASS WITH RECOMMENDATIONS
FV0_EXECUTABLE_DEBUG_CANDIDATE        = CLOSED / PASS
FV1A_LOCAL_READ_DONE_QUALIFICATION     = CLOSED / PASS
FV1A_DEBUG_SCOPE_CORRECTION            = CLOSED / PASS WITH RECOMMENDATIONS
OWNER_DEBUG_SCOPE_UI_OBSERVED          = YES
FV1B_A_AMD64_PACKAGING                 = CLOSED / PASS WITH RECOMMENDATIONS
FV1B_A_R1_AMD64_BUNDLE_REFRESH         = CLOSED / PASS WITH RECOMMENDATIONS
FV1B_B_WYSE_REMOTE_RUNTIME             = NOT STARTED / NEXT FIELD GATE
FV2_PLC_ADDRESS_RECONCILIATION         = NOT STARTED
FV3_REAL_PLC_READ_DONE_SMOKE           = NOT STARTED
OFFICIAL_MAINLINE_PLATFORM             = RASPBERRY_PI_ARM64
WYSE_AMD64_ROLE                         = DEBUG BRANCH ONLY
X86_FORMAL_PRODUCT_LINE                 = NOT AUTHORIZED
MVP_FEATURE_COMPLETE                    = NOT DECLARED
PUSHED                                  = NO
TAGGED                                  = NO
```

本 handoff 本身不授权 FV1B-B remote mutation、真实 PLC write、Raspberry Pi deployment、production DB destructive work、push/tag 或任何后续 Level-2 execution。下一任 PM 必须先完成 read-only takeover，再按 PM Rules 物化新的 exact authority。

---

## 2. Project / repository / live Git baseline

Project root：

`/Users/chenjie/Documents/MES/edge-mes-demo`

Current Devspace checkout workspace at handoff creation：

`ws_d3406061fd`

Live Git baseline immediately before materializing this handoff：

```text
branch      = main
HEAD        = f4494892ded093c126684587080970ce5b1c3f61
origin/main = 6226bf3fb716880a176f9eb642b8139cef3255a6
HEAD ahead  = 25
behind      = 0
staged      = 0
push        = NO
tag         = NO
```

Recent relevant commits：

```text
f449489 build: refresh wyse amd64 debug bundle
6d4f413 fix: support scoped plc debug stations
a7ae6c7 build: prepare wyse amd64 debug deployment bundle
efdd3de feat: add executable real plc debug configuration
40d5aaa feat: migrate station summary charts to echarts
0a1d948 feat: converge dashboard and runtime speed controls
2632aa0 fix: repair owner reacceptance interaction continuity
dcd31d7 fix: close product surface continuity blockers
```

Current staged path count is zero. Do not infer clean working tree from that: known pre-existing governance dirtiness and untracked PM/report corpus remain and are intentionally preserved; see Section 10.

### Current local runtime observation at handoff creation

Read-only `docker ps` showed：

```text
edge-mes-api        = UP / :8000
edge-mes-dashboard  = UP / healthy / host :3001 -> container :3000
edge-mes-collector  = UP
edge-mes-postgres   = UP / healthy / :5432
edge-mes-s7-plc-sim = UP / :1102 + :8200
edge-mes-simulator  = UP / :8100
```

This is local developer runtime only. It is not Raspberry Pi production truth and is not Wyse runtime evidence.

Current protected mapping identities：

```text
config/mapping.yaml
  bytes  = 7112
  sha256 = d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d

data/deployment-config/active/mapping.yaml
  bytes  = 14217
  sha256 = 2b70079ccac4e2293e5a225352f5b4a30d180ed91176c6204d307c53589930a0
```

FV0/FV1A、Debug-Scope、FV1B-A 与 FV1B-A-R1 tasks did not mutate these active mapping bytes.

---

## 3. Governance rules and takeover discipline

New PM must read before authorizing work：

1. this handoff;
2. `docs/thread_handoff/pm_operating_rules.md`;
3. `.agents/skills/edge-mes-pm-governance/SKILL.md`;
4. `AGENTS.md`;
5. `docs/current_status.md` for historical context only, subject to the stale-live-baseline warning in Section 10;
6. task/report files named in the relevant gate sections below.

Current default project mode remains：

```text
CONTINUOUS_LOCAL_MVP = DEFAULT
```

Normal bounded Level-1 local product work can proceed proportionally under one Goal. Hard authority boundaries remain especially important for：

```text
REMOTE DEVICE / PRODUCTION BOUNDARY
REAL PLC WRITE / MACHINE CONTROL
DESTRUCTIVE DB OR HOST MUTATION
PUSH / TAG
MATERIAL SCOPE EXPANSION
OWNER PRODUCT DECISION
```

For Level-2/high-risk repository-backed work, follow the PM Rules fixed 16-section task-file + role-first launcher model. Exact remote identity、mutation surface、budgets、stop conditions and evidence requirements must be frozen before execution.

Do not make exact SHA ceremony a substitute for product work, but do use exact identity where it is authority-bearing：task files、deployment bundles、remote targets and cross-Thread handoffs.

Main PM remains responsible for governance、scope、Owner acceptance orchestration and handoff. Routine implementation should remain delegated to bounded Integration/Shadow/other core Threads as appropriate.

Do not use Playwright/Selenium/browser automation for Owner visual acceptance unless Owner explicitly changes that rule. Owner browser observation is authoritative for product presentation.

---

## 4. Platform strategy — HARD OWNER DECISION

This is a strategic boundary, not a recommendation：

```text
OFFICIAL_MAINLINE_PLATFORM = RASPBERRY_PI_ARM64
FIRST_FORMAL_RELEASE        = RASPBERRY_PI_ARM64
FIRST_REAL_APPLICATION      = RASPBERRY_PI_ARM64

WYSE_3040_AMD64             = DEBUG / FIELD-VALIDATION BRANCH ONLY
FV1B_PASS_PROMOTES_X86      = NO
X86_FORMAL_SUPPORT          = NOT AUTHORIZED
X86_FORMAL_PRODUCT_LINE     = NOT AUTHORIZED
```

Owner explicitly decided：

- Wyse 3040 is being used to rapidly debug/validate the stack on an x86 device.
- Debugging completion must return to the ARM mainline.
- Do not change root project defaults、root Compose、public product claims or roadmap so that amd64/x86 appears to replace ARM.
- Only after the Raspberry Pi release succeeds in real use may a later Owner decision consider an x86 formal version.

Therefore：FV1B-B is not a platform migration project. It is a bounded field-validation branch.

---

## 5. Mainline product state to preserve

### 5.1 Summary

Owner selected Apache ECharts and accepted the current Summary surface for a frozen V1 after saying it was approximately acceptable visually.

Relevant commit：

```text
40d5aaae5fcc09ec24f1a65049c90f51cae74f0b
feat: migrate station summary charts to echarts
```

State：

```text
SUMMARY_V1 = FROZEN
OWNER_ACCEPTANCE_FOR_SUMMARY = ACCEPTED_FOR_FREEZE_WITH_VISUAL_RECOMMENDATIONS
```

Do not casually reopen Summary visual polish while field-validation work is active unless a functional blocker appears.

### 5.2 V-PLC

Functional multiplier behavior was accepted：

```text
1x / 2x / 5x / 10x / 20x
future jobs only
cycle_scale mapping: 1.0 / 0.5 / 0.2 / 0.1 / 0.05
```

Owner considered layout unattractive but explicitly deferred polish.

```text
VPLC_FUNCTIONAL_ACCEPTANCE = PASS
VPLC_LAYOUT_POLISH = DEFERRED
```

Earlier Owner product feedback also requested WS -> Buffer -> WS representation and real progress semantics; later mainline product work must preserve true runtime semantics rather than fake UI progress.

### 5.3 Trace

A separate mainline Trace V2 task exists：

`docs/thread_handoff/shadow_pm_goal_mvp_trace_product_surface_v2_20260817T0814.md`

At this handoff no later Trace commit appears in the current Git log after the Summary/V-PLC work. Do not assume Trace V2 has completed from conversation momentum. Next PM must read-only recover its actual Thread/report state if the Owner supplies a terminal, or inspect live repository/report evidence before deciding whether to relaunch/close it.

Owner's required Trace product behavior remains：recent records above; selected/query trace below; one continuous route timeline per unit; Unit Summary at top; business payload professionally presented; raw JSON under technical details; preserve historical topology/identity correctness.

### 5.4 MVP status

Do not declare MVP feature complete merely because Field Validation progresses. Mainline product and Owner acceptance remain the final authority for MVP closeout.

R4 20WS/multi-PLC remains outside the immediate field-debug path and must not be pulled in as a prerequisite.

---

## 6. FIELD-VALIDATION-COLLECTOR-DB workstream — current accepted chain

This is an independent debugging/field-validation branch, not a replacement for Mainline.

### 6.1 Frozen field-validation plan V2

Durable plan：

`docs/reports/real_plc_debug_field_validation_plan_v2_20260817.md`

Core philosophy：PLC and Edge MES are both under debugging; prioritize fast real-device debug, editable executable mapping and early Read_Done verification. Detailed production ACK protocol can be deferred.

Phase chain：

```text
FV0   executable virtual debug candidate
FV1A  local executable mapping + synthetic Read_Done
FV1B  edge device / Docker deployment validation (Wyse branch)
FV2   PLC program / address reconciliation
FV3   real PLC connection + Read_Done smoke
FV4   real PLC end-to-end cycle smoke
FV5   basic fault debug
FV6   short soak + production protocol decision
```

### 6.2 FV0 + FV1A executable PLC Debug Communication Contract

Accepted commit：

```text
efdd3decb0901ad79ce8e401327438c5b684b5dd
feat: add executable real plc debug configuration
```

Durable report：

`docs/reports/fv0_fv1a_real_plc_debug_config_report_20260817.md`

Implemented product surface `/deployment/plc` now supports：

- PLC connection host/IP、port、rack、slot、timeouts/poll interval;
- station DB/read range;
- signal address/type/direction/unit/description;
- PLANNED / CONFIRMED status;
- engineering export;
- candidate persistence distinct from Active mapping;
- deterministic candidate -> runtime mapping projection;
- fail-closed Edge write policy：`READ_DONE_ONLY`;
- parameter / machine-control / safety / arbitrary DB writes disabled.

Synthetic proof established：

```text
accepted_fact -> persist_cycle -> commit -> Read_Done write
storage failure -> rollback -> zero Read_Done write
```

No real PLC write occurred.

### 6.3 FV1A Debug-Scope correction — Owner UI observed

Owner identified a real debugging usability issue：for a 3WS line, they may initially connect only WS03 and must not be forced to configure WS01/WS02.

Accepted correction commit：

```text
6d4f41365120677e73ce80290b2417ce6da4971e
fix: support scoped plc debug stations
```

Durable report：

`docs/reports/fv1a_debug_scope_correction_report_20260817.md`

Accepted semantics：

```text
Base Line Topology = WS01 -> WS02 -> WS03 (unchanged)
Debug Pilot Scope  = selected subset, e.g. [WS03]
```

For WS03-only：

```text
WS01 config required = NO
WS02 config required = NO
WS03 config required = YES

debug_ready       = true
ready_to_activate = false

projected executable stations = WS03 only
WS01 read plan = 0
WS02 read plan = 0
WS03 read plan = 1
Read_Done allowlist = WS03 only
```

Synthetic proof：DB103 selected; database commit occurs before exactly one WS03 Read_Done; WS01/WS02 writes zero; storage failure writes zero.

Full-line activation remains fail-closed for partial Debug scope. The 3WS Line topology itself is not rewritten into a one-station production line.

Owner rebuilt API + Dashboard locally and explicitly observed the new `Debug Pilot Scope` UI. That Owner observation is accepted product evidence for presence of the UI; it is not real PLC/remote evidence.

### 6.4 FV1B-A original amd64 package

Accepted commit：

```text
a7ae6c71b0d23bd30bf52a7f5cacef8893769d58
build: prepare wyse amd64 debug deployment bundle
```

Durable report：

`docs/reports/fv1b_a_wyse_amd64_branch_packaging_report_20260817.md`

This proved local amd64 packaging only. It predates the Debug-Scope correction and is now historical evidence; do not use its old project image tags as the authoritative FV1B-B bundle.

### 6.5 FV1B-A-R1 amd64 bundle refresh — CURRENT FIELD DEPLOYMENT BUNDLE

Accepted commit and current HEAD：

```text
f4494892ded093c126684587080970ce5b1c3f61
build: refresh wyse amd64 debug bundle
```

Durable report：

`docs/reports/fv1b_a_r1_wyse_amd64_bundle_refresh_report_20260817.md`

Mainline PM intake result：

```text
PASS WITH RECOMMENDATIONS
```

R1 exact source HEAD bound into project images：

```text
6d4f41365120677e73ce80290b2417ce6da4971e
```

Six R1 project images locally built and inspected as `linux/amd64`：

```text
edge-mes-demo-api:fv1b-a-r1-amd64
edge-mes-demo-collector:fv1b-a-r1-amd64
edge-mes-demo-dashboard:fv1b-a-r1-amd64
edge-mes-demo-s7-plc-sim:fv1b-a-r1-amd64
edge-mes-demo-simulator:fv1b-a-r1-amd64
edge-mes-demo-sync-worker:fv1b-a-r1-amd64
```

Four frozen upstream amd64 refs remain exactly those accepted in FV1B-A：PostgreSQL 16、Grafana、Prometheus、node-exporter exact variant digests. Do not silently refresh `latest` during FV1B-B.

R1 artifacts — these are the only FV1B-B package artifacts to use unless PM explicitly publishes a newer bundle：

```text
deploy/wyse/docker-compose.wyse-r1.yml
  bytes  = 7292
  sha256 = 3f50c41311d000e433864ba41ff4f2350a9f176ee23e58f2bc299bf91a360734

deploy/wyse/README-r1.md
  bytes  = 2658
  sha256 = 5160d319034fd7bc62816b43522cebe2031b7f274b0a364e5e8532a25ccefc0b

docs/reports/evidence/fv1b-a-r1/amd64_image_manifest.json
  bytes  = 11181
  sha256 = 5be22b469df44771f2cf39f0f57247c0bc560c07109627ff342a7b5dba2f2bbc

docs/reports/evidence/fv1b-a-r1/manifest.sha256
  bytes  = 320
  sha256 = 13927397b9ccf824c3636987b5d118fa68512313a8d5f106e72a0dfa100d9ba3

docs/reports/fv1b_a_r1_wyse_amd64_bundle_refresh_report_20260817.md
  bytes  = 15613
  sha256 = f04a0746226598c9b045fe98d3d19cb0db234517b340a89c2b608359022e0024
```

Protected ARM root Compose remains：

```text
docker-compose.yml
bytes  = 6191
sha256 = 5e7009a5870919313c4355dd8af7e6f92194b62307bc74d0030f43a47719e483
```

R1 static image proof confirmed Debug-Scope markers in API、Dashboard and Collector/common. This is packaging evidence only：

```text
WYSE_REMOTE_ACTION         = 0
RASPBERRY_PI_REMOTE_ACTION = 0
REAL_PLC_CONNECT           = 0
REAL_PLC_READ              = 0
REAL_PLC_WRITE             = 0
REMOTE_MUTATION            = 0
PROJECT_COMPOSE_LIFECYCLE  = 0
```

Do not claim Wyse runtime PASS from this.

---

## 7. Next Field gate — FV1B-B Wyse 3040 Remote Full-Stack Deployment Qualification

This is the next planned field-validation gate, but it is **NOT YET AUTHORIZED FOR EXECUTION** at handoff creation.

FV1B-B is Level-2 because it will mutate a real remote device and run Docker lifecycle actions.

### 7.1 Required Owner/Wyse facts before PM publishes FV1B-B

Next PM must obtain and freeze exact Wyse identity. At minimum：

```text
WYSE_HOST / IP
WYSE_SSH_USER
WYSE_SSH_PORT
trusted host-key identity / fingerprint or equivalent exact host identity
```

Required preflight facts from the Wyse：

```bash
uname -m
cat /etc/os-release
free -h
df -h
docker --version
docker compose version
ip addr
```

Expected architecture for this branch is `x86_64` / `amd64`, but do not assume it; verify.

Also determine whether the actual OS supports Docker. Do not assume a stock thin-client appliance OS can run the prepared stack.

### 7.2 Remote task must freeze exact transfer/deployment method

R1 project images currently exist locally; no Docker push was performed. FV1B-B must explicitly choose and freeze one bounded transport method, for example exact `docker save` archive transfer/load or another Owner-approved mechanism. Do not invent registry credentials or push images without authority.

The task must bind the transfer source to the R1 manifest and six exact R1 image identities, and must use：

`deploy/wyse/docker-compose.wyse-r1.yml`

not the historical `deploy/wyse/docker-compose.wyse.yml`.

### 7.3 FV1B-B objective

Deploy the complete current logical stack to the Wyse for debugging/platform qualification, not x86 productization：

```text
postgres
simulator
s7-plc-sim
collector
api
dashboard
grafana
prometheus
node-exporter
sync-worker
```

First validation intentionally uses the full stack because Owner wants to observe whether the Wyse can carry the complete Edge MES demo. Do not prematurely trim services before evidence.

Collect at least：

```text
CPU
RAM
swap
disk
container state / health / restart count
PostgreSQL persistence
API health
Dashboard health
Trace availability
V-PLC availability
PLC Deployment page availability
Grafana / Prometheus availability
restart/recreate persistence evidence
```

A successful Compose start is not production readiness. Resource pressure、disk limits and persistence must be reported honestly.

### 7.4 FV1B-B boundaries

Unless a later exact task explicitly grants more：

- do not connect/read/write a real PLC during FV1B-B;
- do not mutate Raspberry Pi deployment;
- do not alter root ARM defaults;
- do not promote x86 to mainline;
- do not push/tag;
- do not perform uncontrolled package installation/cleanup on Wyse;
- do not use destructive Docker prune;
- do not infer FV2/FV3 authority from FV1B-B PASS.

After FV1B-B debugging closes, field work proceeds to FV2 only if Owner continues the real-PLC path; overall product direction returns to ARM mainline after debugging.

---

## 8. FV2 / FV3 future real-PLC path — NOT CURRENT AUTHORITY

### FV2 — PLC Program / Address Reconciliation

PLC engineer compares actual TIA DB layout against the executable Debug Candidate. Candidate fields move PLANNED -> CONFIRMED as addresses are reconciled.

For an initial single-station pilot, WS03-only is valid. No need to force WS01/WS02 configuration.

Before any real Edge write, freeze the actual Read_Done address and ownership semantics.

### FV3 — Real PLC connection + Read_Done smoke

This is a later Level-2 gate.

Owner intentionally prioritizes fast debug and Read_Done verification rather than full production protocol validation.

Expected shape after separate authority：

```text
brief bounded read-only sanity
-> 3-5 cycles
-> DB commit
-> exact Read_Done-only write
```

Current product source uses a whole-byte read-modify-write model for the existing handshake byte when setting Read_Done. Before FV3, confirm exact byte/bit ownership and whether another PLC writer can modify the same byte. Prefer an Edge-owned byte/bit allocation where practical.

Production-grade `ack_valid/ack_counter` remains deferred until later protocol decision; do not force it into the first debug smoke.

No real PLC connection/read/write has occurred in the accepted FV0/FV1A/FV1B chain so far.

---

## 9. Important product semantics that remain frozen

Production semantics must not regress while field work proceeds：

```text
result         = OK | NOK
process_status = PROCESSED | SKIPPED
```

First NOK at WS_i：

```text
origin station:
  NOK / PROCESSED

downstream stations:
  NOK / SKIPPED / UPSTREAM_NOK
```

Accepted downstream production result remains `nok`, never `skip`.

Terminal unit = `COMPLETED_NOK` for a NOK route.

Line Summary cohort remains terminal-completed units in `[start,end)`.

Per-station conservation：

```text
TOTAL = OK + NOK = PROCESSED + SKIPPED
```

All station totals in the same terminal cohort must match.

Do not let Debug Scope semantics overwrite production Line topology semantics. `Debug Pilot Scope=[WS03]` means a scoped debug execution candidate; it does not redefine the authoritative 3WS production topology.

---

## 10. Working-tree dirtiness / governance warning

At handoff creation, the following tracked files remain pre-existing dirty：

```text
 M .agents/skills/edge-mes-pm-governance/SKILL.md
 M AGENTS.md
 M docs/current_status.md
 M docs/thread_handoff/pm_operating_rules.md
```

Do not reset、stash、clean、stage or adopt them by convenience.

There is also a substantial pre-existing untracked PM/report/task corpus. Notable current paths include：

```text
docs/reports/mvp_mainline_product_acceptance_cut_20260816.md
docs/reports/mvp_product_recovery_route_correction_20260816.md
docs/reports/r3_10ws_runtime_architecture_design_20260816.md
docs/reports/real_plc_debug_field_validation_plan_v2_20260817.md
docs/thread_handoff/chatgpt_pm_handoff_260815-2323.md
docs/thread_handoff/chatgpt_pm_handoff_260816-1750.md
docs/thread_handoff/owner_acceptance_mvp_20260816.md
docs/thread_handoff/pm_task_20260817T0104Z_fv0-fv1a_real_plc_debug_config.md
docs/thread_handoff/pm_task_20260817T0212Z_fv1b-a_wyse_amd64_branch_packaging.md
docs/thread_handoff/pm_task_20260817T0236Z_fv1a-debug-scope_station-scope-correction.md
docs/thread_handoff/pm_task_20260817T0302Z_fv1a-debug-scope_station-scope-correction-r1.md
docs/thread_handoff/pm_task_20260817T0854Z_fv1b-a-r1_amd64-bundle-refresh.md
docs/thread_handoff/shadow_pm_goal_mvp_trace_product_surface_v2_20260817T0814.md
```

The older `pm_task_20260817T0236Z_fv1a-debug-scope_station-scope-correction.md` was never dispatched and was superseded by the R1 correction task. It is not execution authority.

### Critical stale-status warning

`docs/current_status.md` currently contains a top live-baseline block around earlier commit `ffa8d5e... / ahead 17`, while live Git is now `f449489... / ahead 25`. The file itself is already dirty.

Therefore next PM must **not** use its historical top baseline to override fresh Git or this handoff. Treat `docs/current_status.md` as historical/status context pending a separately governed reconciliation. Do not stage its pre-existing changes with the handoff or with a future field task unless exact status-sync authority is granted.

This handoff plus fresh read-only recovery is the current cross-PM live baseline.

---

## 11. PM Rule task-file history and supersession

Relevant authority files：

```text
docs/thread_handoff/pm_task_20260817T0104Z_fv0-fv1a_real_plc_debug_config.md
  FV0/FV1A implementation authority

docs/thread_handoff/pm_task_20260817T0212Z_fv1b-a_wyse_amd64_branch_packaging.md
  FV1B-A initial amd64 packaging authority

docs/thread_handoff/pm_task_20260817T0236Z_fv1a-debug-scope_station-scope-correction.md
  SUPERSEDED / NEVER DISPATCHED / NOT AUTHORITY

docs/thread_handoff/pm_task_20260817T0302Z_fv1a-debug-scope_station-scope-correction-r1.md
  executed Debug-Scope correction authority

docs/thread_handoff/pm_task_20260817T0854Z_fv1b-a-r1_amd64-bundle-refresh.md
  executed FV1B-A-R1 refresh authority
```

Do not edit a previously published task file in place after its identity has been dispatched. Corrections require a new unique task file + new launcher unless PM Rules explicitly permit a pre-consumption correction.

FV1B-B must be a new task. Do not reuse or reinterpret an FV1B-A task as remote authority.

---

## 12. Recommended first read-only action for the next PM

The next PM's first action must be takeover/recovery only. Do not immediately publish FV1B-B.

Recommended sequence：

1. mechanically verify this handoff identity from the Owner launcher;
2. verify physical project root and `git rev-parse --show-toplevel`;
3. read PM Rules、PM Skill、AGENTS and this handoff's named FV1B-A-R1 report/artifacts;
4. fresh read-only Git recovery：
   - `git status -sb`
   - `git rev-parse HEAD`
   - `git rev-parse origin/main`
   - `git rev-list --count origin/main..HEAD`
   - `git diff --name-only`
   - `git diff --cached --name-only`
   - recent `git log --oneline`
5. confirm R1 artifact identities and root ARM Compose continuity;
6. confirm no new field/Mainline Thread terminal has landed after this handoff;
7. ask Owner for missing Wyse identity/preflight facts if they have not already been supplied in the new window;
8. only after exact target identity exists, design/publish the Level-2 FV1B-B task with exact transfer/deployment/rollback/stop budgets.

If the Owner instead decides to stop Wyse work, do not manufacture FV1B-B; return to Mainline ARM work under the Owner's stated priority.

---

## 13. Carry-forward recommendations

1. **Keep x86 isolated.** Never describe the Wyse debug branch as the product default.
2. **Use R1 only.** FV1B-B must use `docker-compose.wyse-r1.yml` and R1 image manifest, not the earlier bundle.
3. **Freeze remote identity first.** No host/IP/user/key identity means no remote deployment authority.
4. **One transport plan.** Choose an exact image transfer/load method and budget; do not mix ad-hoc registry push、scp archives and rebuild-on-Wyse approaches.
5. **Do not build on the Wyse unless evidence forces it.** It is a resource-constrained validation target; the accepted route is to prepare amd64 images off-device and transfer/load them.
6. **Observe resources before optimizing.** Owner intentionally wants the full stack first; collect actual CPU/RAM/disk evidence before removing Grafana/Prometheus/simulator services.
7. **Keep Debug Scope.** Initial real-device pilot may be WS03-only. Do not require WS01/WS02 dummy configuration.
8. **No fake activation.** Partial scope can be debug-ready but cannot become full-line activation-ready.
9. **Real PLC later.** FV1B-B should qualify the Wyse platform/runtime without real PLC writes; FV2/FV3 remain separate gates.
10. **Return to ARM.** When debugging objectives are satisfied, resume Raspberry Pi / ARM64 Mainline work.
11. **Do not broaden to 20WS/multi-PLC.** It is not required for this field-debug sequence.
12. **Owner browser acceptance remains manual/authoritative.** Do not waste time on slow browser automation for visual acceptance.

---

## 14. Explicit non-authorized surfaces at handoff

This handoff grants no authority for：

```text
FV1B-B remote SSH / SCP / Docker lifecycle
Wyse package install / host mutation
real PLC connect / read / write / Read_Done
Raspberry Pi deployment / restart / rollback
production DB mutation / destructive cleanup
Candidate activation against a real target
root docker-compose.yml platform mutation
x86 formal release / product support declaration
20WS / multi-PLC expansion
push / tag
broad Git cleanup / reset / stash / clean
```

Any such action requires a new exact authority appropriate to risk.

---

## 15. Handoff file commit policy

Owner explicitly requested a durable PM Handoff. Under PM Rules Section 9, the handoff itself may be exact-staged and committed as part of the current PM handoff flow.

Only this new handoff path is authorized for handoff commit：

`docs/thread_handoff/chatgpt_pm_handoff_260817-1729.md`

Do not stage the four pre-existing dirty governance files、older handoffs、task files、reports or any other untracked file.

Intended handoff commit message：

```text
docs: hand off wyse field validation to next pm
```

Push/tag remain unauthorized.

---

## 16. Copyable prompt for the next ChatGPT Mainline PM

```text
@Devspace

你现在接手 Edge MES Demo，担任新的 ChatGPT Mainline PM。

这是一次 PM takeover，不是直接执行 FV1B-B。第一步必须 read-only recovery。

项目绝对路径：

/Users/chenjie/Documents/MES/edge-mes-demo

首先读取并机械核验新的 authoritative PM handoff：

docs/thread_handoff/chatgpt_pm_handoff_260817-1729.md

Expected identity 以 Owner 在交接窗口发布的 exact regular/non-symlink、bytes、SHA-256 为准。

核验 handoff 后，按顺序读取：

1. docs/thread_handoff/pm_operating_rules.md
2. .agents/skills/edge-mes-pm-governance/SKILL.md
3. AGENTS.md
4. docs/reports/fv1b_a_r1_wyse_amd64_bundle_refresh_report_20260817.md
5. deploy/wyse/README-r1.md
6. docs/reports/evidence/fv1b-a-r1/amd64_image_manifest.json
7. docs/reports/real_plc_debug_field_validation_plan_v2_20260817.md
8. docs/reports/fv1a_debug_scope_correction_report_20260817.md
9. docs/current_status.md（仅作为历史/status context；其顶部 baseline 已过时，live Git 与 handoff 优先）

随后执行 fresh read-only recovery：

- physical cwd + git top-level
- git status -sb
- git rev-parse HEAD
- git rev-parse origin/main
- git rev-list --count origin/main..HEAD
- git diff --name-only
- git diff --cached --name-only
- recent git log --oneline
- verify R1 bundle identities and protected root ARM docker-compose.yml continuity

Expected publication baseline at handoff creation：

branch = main
HEAD = f4494892ded093c126684587080970ce5b1c3f61
origin/main = 6226bf3fb716880a176f9eb642b8139cef3255a6
ahead = 25
staged = 0
push/tag = NO

Strategic Owner boundary：

OFFICIAL_MAINLINE_PLATFORM = RASPBERRY_PI_ARM64
WYSE_3040_AMD64 = DEBUG BRANCH ONLY
X86_FORMAL_PRODUCT_LINE = NOT AUTHORIZED

Current field gate：

FV1B-A-R1 = CLOSED / PASS WITH RECOMMENDATIONS
FV1B-B = NEXT / NOT YET AUTHORIZED

Do not publish or execute FV1B-B until exact Wyse identity is frozen：host/IP、SSH user、SSH port、trusted host-key identity，以及 OS/arch/RAM/swap/disk/Docker/Compose preflight facts。

FV1B-B must use：

deploy/wyse/docker-compose.wyse-r1.yml

and the R1 image manifest. Do not silently fall back to the historical FV1B-A bundle.

Do not infer any real PLC、Raspberry Pi、remote deployment、push/tag、x86 productization or FV2/FV3 authority from this handoff or FV1B-A-R1 PASS。

After read-only takeover, report the recovered live baseline、current gate、missing Wyse prerequisites and your proposed next PM action. Stop before remote mutation unless a separately published Level-2 task grants it.
```

---

## 17. Final outgoing PM statement

The outgoing PM's durable conclusion is：

```text
FV1B_A_R1_MAINLINE_PM_INTAKE = PASS WITH RECOMMENDATIONS
NEXT_FIELD_GATE               = FV1B_B_WYSE_REMOTE_FULL_STACK
NEXT_GATE_EXECUTION_AUTHORITY = NOT YET GRANTED
MISSING_HARD_INPUT             = EXACT WYSE REMOTE IDENTITY + PREFLIGHT
MAINLINE_PLATFORM              = RASPBERRY_PI_ARM64
WYSE_AMD64                     = DEBUG BRANCH ONLY
REAL_PLC_WRITE                 = NOT AUTHORIZED
MVP_COMPLETE                   = NOT DECLARED
```

The next PM should not spend a new window reconstructing the project from historical chats. This handoff, the named durable reports/artifacts and fresh live recovery are intended to be sufficient to resume work without losing the ARM-mainline / x86-debug-branch boundary or the Debug Pilot Scope semantics.
