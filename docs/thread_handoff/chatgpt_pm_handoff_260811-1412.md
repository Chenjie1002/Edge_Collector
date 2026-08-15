# Edge MES Demo — Mainline ChatGPT PM Handoff — 2026-08-11 14:12 UTC+8

## 0. Handoff purpose and successor role

This is the durable Mainline PM handoff after the bounded Shadow Mainline PM P0 Remote Closure Goal completed and Mainline PM independently accepted the terminal state.

Accepted terminal:

`PASS / P0_REMOTE_CLOSURE_AUTONOMOUS_GOAL_COMPLETE`

Mainline acceptance state:

```text
P0_PM_ACCEPTED = YES
PRODUCTION_ACCEPTED = YES
B1_ELIGIBILITY_REASSESSED = YES
B1_ELIGIBLE = NO / fail-closed terminal from the one allowed reassessment
B1_EXECUTION_AUTHORIZED = NO
SHADOW_PM_STOP = YES
```

Successor role:

```text
Mainline ChatGPT PM
Project: Edge MES Demo
Repository root: /Users/chenjie/Documents/MES/edge-mes-demo
Branch: main
Current closed Level 2: P0 Remote Closure
Next mainline phase: NOT YET AUTHORIZED / Owner decision required
```

The successor PM owns mainline planning, report intake, roadmap/gate decisions, MVP-path control and future Owner handoff. This handoff grants **read-only takeover only**. It grants no SSH, remote Docker, deployment, lifecycle, V-PLC/PLC, DB write, production stimulus, B1 execution, C1+, Git stage/commit/push/tag, or parallel-branch authority.

Do not resume the completed P0 Shadow Goal. Do not automatically execute B1 merely because P0 closed. The accepted B1 outcome is currently `NO`, B1 execution remains forbidden, and any next mainline phase requires a new Owner decision and fresh planning authority.

---

## 1. First-read authority and takeover order

After mechanically verifying this handoff's exact launcher identity, the successor PM should perform a **read-only takeover** in this order:

1. this handoff through EOF;
2. `docs/thread_handoff/pm_operating_rules.md` through EOF;
3. `docs/reports/shadow_pm_p0_remote_closure_ledger.md` current-state block and final history rows;
4. `docs/reports/sprint4_d2_r7b_p0_rc_production_path_revalidation_accepted_fact.md`;
5. `docs/reports/sprint4_d2_r7b_p0_b1_eligibility_reassessment_local_readonly.md`;
6. `docs/reports/sprint4_d2_r7b_p0_rc_r1_r2_existing_script_runtime_loaded_verification.md`;
7. `docs/reports/sprint4_d2_r7b_p0_rc_a1_r1_self_identity_mechanics_recovery.md`;
8. `docs/reports/sprint4_d2_r7b_p0_rc_b0_pre_activation_rollback_readiness.md`;
9. `docs/reports/sprint4_d2_r7b_p0_rc_f0_r3_post_drift_minimal_payload_recovery.md`;
10. `docs/reports/sprint4_d2_r7b_p0_rc_l0_r6_format_aware_readonly_lineage_reconciliation.md`;
11. `docs/reports/sprint4_d2_r7b_p0_rc_t1_r5_current_turn_exact_reauthorization.md`;
12. accepted focused Reliability / Data Quality / Verification reports named in Section 7;
13. `docs/current_status.md` only as historical/status context; do not treat stale wording as stronger than final accepted P0 reports/ledger and live Git;
14. live Git/repository recovery: `git status -sb`, recent log, live HEAD/origin, worktree diff names and cached diff names.

Current PM Rules identity at handoff creation:

```text
path      = docs/thread_handoff/pm_operating_rules.md
type      = regular / non-symlink
bytes     = 69697
SHA-256   = 45d4be226d2c4754fb2b21b55fce6f4086cb24e643b170f1ad1ab475a596bf9f
Git state = tracked dirty / preserve
```

Current `docs/current_status.md` identity:

```text
path      = docs/current_status.md
type      = regular / non-symlink
bytes     = 173596
SHA-256   = f50635357c2afa9b9f649ed5f80cc210d4323b0bb0868f370eef13de0ae25b99
Git state = tracked dirty / preserve
```

Do not rewrite either protected governance file merely to make the wording look current. Any status/rules sync is a separate exact Owner-authorized governance task.

---

## 2. Operating rules the successor must preserve

1. Repository-backed task files remain the default authority for Architecture / Integration, Reliability, Data Quality and Verification work.
2. Task self-identity protects the exact authoritative file: exact path, regular/non-symlink semantics, bytes and full SHA-256 before broader task action.
3. Do not turn literal shell formatting, report cosmetics or redundant validators into stronger security properties than the actual identity/mutation safety contract.
4. Physical cwd and Git top-level must equal the declared repository root before repository-relative work.
5. Remote, lifecycle, production, DB, PLC/V-PLC and Git authorities are separate and never inherited merely from an accepted predecessor PASS.
6. Existing dirty/untracked corpus must be preserved unless a fresh task grants exact-path mutation authority.
7. Broad staging is forbidden. Stage/commit/push/tag require fresh exact Owner authority and a verified cached allowlist.
8. PM intake must inspect durable artifacts and live facts independently; specialist chat summaries are candidate evidence only.
9. Distinguish `WRITTEN / REVIEWED / ACCEPTED / VERIFIED / BUILT / TRANSPORTED / REMOTE_IMAGE_ACCEPTED / ACTIVATED / RUNTIME_LOADED / PRODUCTION_ACCEPTED / P0_PM_ACCEPTED`.
10. Evidence must remain proportional to the product claim. Validation/governance machinery must not replace product delivery.
11. A control-plane, shell, report-formatting or task-contract defect is not a Collector/product defect unless fresh evidence actually establishes a product defect.
12. Do not rename/repackage one root cause to evade retry limits.
13. Do not automatically repeat accepted focused reviews when the reviewed lineage is unchanged; reopen only when a dependent source/contract/runtime claim materially changes or fresh evidence creates a credible false-PASS risk.
14. Parallel workstream `FIELD-VALIDATION-COLLECTOR-DB` remains independent and must not be absorbed into Mainline without explicit Owner authority.
15. The completed Shadow P0 dual-budget counters are historical closure evidence, not a standing budget model automatically governing every future mainline phase.

MVP-path classification remains mandatory for future Level 2 work.

---

## 3. Live Git baseline at transfer

Fresh read-only recovery at handoff creation established:

```text
branch       = main
HEAD         = dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
origin/main  = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
ahead/behind = 1/0
cached diff  = empty
```

Recent committed baseline:

```text
dbe5706 fix: accept canonical raw_hex collector payloads
2a4f9d4 Sync accepted D2-R7B-W0 governance status  # origin/main
```

The local accepted corrected source commit is still one commit ahead of origin and has **not been pushed**.

HEAD contains the accepted three-path source/test repair:

```text
collector/tests/test_event_collector_adapter_gate.py
common/station_event/validation.py
tests/test_station_event_model.py
```

Pre-existing tracked dirty paths:

```text
docs/current_status.md
docs/thread_handoff/pm_operating_rules.md
```

A very large historical untracked task/report corpus remains, including the complete Shadow P0 closure artifacts and this handoff. Do not clean, stash, broad-stage, adopt or rewrite that corpus by convenience.

At handoff creation, `git diff --cached --name-only` was empty. This handoff itself must remain unstaged until the Owner gives explicit exact-path stage/commit/push authority.

---

## 4. Accepted corrected source and local image lineage

Accepted corrected source commit:

```text
dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
```

Reviewed source/test identities remain:

```text
common/station_event/validation.py
41624 / bb0664bfe8113e7989ca17629a6a8e5072e91d57ecf640f211631f216e51e02e

tests/test_station_event_model.py
58061 / 7b7177fa815834bc174e311acf5cb3b938004bbdc75073ecad2e94d7c91aac27

collector/tests/test_event_collector_adapter_gate.py
26822 / 8e022346f359ec62877b876c618269631a70f2ffa9b66be7da38cb6eefd24080
```

Root cause repaired by this source:

`RAW_HEX_SHARED_VALIDATION_CONTRACT_MISMATCH`

Accepted local corrected image/OCI lineage:

```text
local accepted OCI descriptor = sha256:cef401fcfb19f50aacb3d5ac6d6c73f9aeb582811a85c14eeb5fdec03eed0ad0
image tag                     = edge-mes-demo-collector:p0-r1-dbe5706
platform                      = linux/arm64
source commit                 = dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
```

The OCI descriptor and Docker Engine object are different identity layers. Do not collapse them into one ID.

---

## 5. Remote transport and OCI-to-Docker identity acceptance

Accepted transport report:

```text
path    = docs/reports/sprint4_d2_r7b_p0_rc_t1_r5_current_turn_exact_reauthorization.md
bytes   = 13511
SHA-256 = ac31953ccd088943b3530ff7a07306596e9f8eebd83d0f2f6ffac033d64e6a69
terminal = PASS / CORRECTED_IMAGE_TRANSPORTED_AND_REMOTE_ARCHIVE_STAGED
```

Accepted remote archive:

```text
path = /opt/edge-mes-demo/.transport/d2-r7b-t0/accepted-corrected-image-cef401fcfb19f50aacb3d5ac6d6c73f9aeb582811a85c14eeb5fdec03eed0ad0.tar
bytes = 54321664
SHA-256 = 8553f9dd71f60de686810b51364461d5898372e9560db4c6ed4325f7f76e524c
```

Accepted format-aware reconciliation report:

```text
path    = docs/reports/sprint4_d2_r7b_p0_rc_l0_r6_format_aware_readonly_lineage_reconciliation.md
bytes   = 14952
SHA-256 = 69af87275e41b9e21d9550f9ae4ecee20dd2edd04c92b4ff319eb27191b1b1de
terminal = PASS / FORMAT_AWARE_ARCHIVE_TO_REMOTE_CONFIG_LINEAGE_EXACT
```

Accepted three-layer mapping:

```text
OCI descriptor
sha256:cef401fcfb19f50aacb3d5ac6d6c73f9aeb582811a85c14eeb5fdec03eed0ad0
  -> linux/arm64 manifest
sha256:2695127d11b723a30964b14c201a41fd26290a27c18162f66d299ff78e3ec730
  -> remote Docker config/tag object
sha256:a199e6417c3ed5e42724201122ea4014604b561593a243039aef72d71900b252
```

Accepted flags:

```text
REMOTE_IMAGE_ACCEPTED = YES / EXACT_OCI_DESCRIPTOR_TO_PLATFORM_CONFIG_MAPPING
REMOTE_LOADED_OBJECT = YES / EXACT_PLATFORM_CONFIG_AND_TAG_OBJECT
```

The accepted remote Docker object identity is `a199...`; this does not replace the accepted OCI descriptor `cef...`.

---

## 6. Forward descriptor, rollback readiness, activation and runtime

### Forward descriptor

```text
report  = docs/reports/sprint4_d2_r7b_p0_rc_f0_r3_post_drift_minimal_payload_recovery.md
bytes   = 12446
SHA-256 = 649641da5b3b56ff13efb927c322d9c85f2e4d03a674e4fcd36ace5017d83f9c
state   = PASS / PM ACCEPTED
remote descriptor = /opt/edge-mes-demo/docker-compose.p0-rc-f0.corrected-image.override.yml
remote descriptor bytes/SHA = 106 / c96ccdd17ee70b15d93189733f9baab5075e520347a98324c4be5df827979811
```

### Rollback readiness

```text
report  = docs/reports/sprint4_d2_r7b_p0_rc_b0_pre_activation_rollback_readiness.md
bytes   = 13767
SHA-256 = b0c1a936bd78845c976c9c7f5041478dd27efeadbb8c1dd8a886a074df1d7739
state   = PASS / PM ACCEPTED
rollback descriptor = /opt/edge-mes-demo/docker-compose.p0-rc-b0.rollback.override.yml
rollback descriptor bytes/SHA = 106 / 3c2c4f9aecc9a868a9fc7ce5616fe4d9d83af243d3b76728a084eee2b42c4177
rollback Image.Id = sha256:b10d8253638ebd80a413fff9b6924e39e04a38e34a8718663c1a23eeff0aac78
PRE_ACTIVATION_ROLLBACK_READY = YES
```

### Controlled activation

```text
report  = docs/reports/sprint4_d2_r7b_p0_rc_a1_r1_self_identity_mechanics_recovery.md
bytes   = 11857
SHA-256 = b4b3e76998e789664ed6c1edb38134166b02488399bba062ca86f2551beeb643
terminal = PASS / P0_RC_A1_CONTROLLED_COLLECTOR_ACTIVATED
```

Accepted current Collector runtime object:

```text
Collector full ID = 6cab966e18bc1b5b349a0901793ff89ab7bfcde889ff7b2e911746e413eac25e
Image.Id          = sha256:a199e6417c3ed5e42724201122ea4014604b561593a243039aef72d71900b252
ACTIVATED         = YES
```

### Runtime-loaded verification

```text
report  = docs/reports/sprint4_d2_r7b_p0_rc_r1_r2_existing_script_runtime_loaded_verification.md
bytes   = 9703
SHA-256 = 36411688aa261616a094bfc64ef5c9e36d2603b7783d01b089ca031972a63908
terminal = PASS / P0_RC_R1_R2_EXISTING_SCRIPT_RUNTIME_LOADED
RUNTIME_LOADED = YES
```

R1-R2 verified current Collector/image/process/config mount/mapping/canonical runtime startup record/time relation with one read-only SSH and zero remote mutation.

---

## 7. Accepted focused review chain remains valid for unchanged lineage

These reports were reverified as unchanged during final production closure and remain accepted. Do not rerun them just because a new PM takes over.

### Reliability

```text
path    = docs/reports/sprint4_d2_r7b_p0_r1_rel_r1_focused_reliability_review.md
bytes   = 5416
SHA-256 = ce614a39898e0a0aa7368346d704106e4ebddbb00ba2224984e7189779a4a626
terminal = PASS
```

### Data Quality

```text
path    = docs/reports/sprint4_d2_r7b_p0_r1_dq_r1_focused_data_quality_review.md
bytes   = 8478
SHA-256 = 4bda92e517a853b12315ef2b0af5c1a7d2888c43cec3cf3e6e81268f71d0a655
terminal = PASS
```

### Verification

```text
path    = docs/reports/sprint4_d2_r7b_p0_r1_v1_r1_focused_verification.md
bytes   = 12274
SHA-256 = 5591708ec60389402285c64f5b8979b9c87c701d6b6ad4aefb27ffab1abae9fa
terminal = PASS
```

They remain applicable because the reviewed three-path source/test lineage stayed byte-identical and path-scoped worktree/cached diffs were empty at final closure.

Reopen a review only when a dependent source/contract/authority semantic changes, or fresh production evidence establishes a credible false-PASS risk.

---

## 8. Accepted production truth — P0 is closed

Production report:

```text
path    = docs/reports/sprint4_d2_r7b_p0_rc_production_path_revalidation_accepted_fact.md
bytes   = 8766
SHA-256 = 458339beb9e835a2d1e703b6da22ccdb583be979ff3f80920dc83fdd70950253
terminal = PASS / P0_RC_PRODUCTION_FACT_GATE_PASS=YES / PRODUCTION_ACCEPTED_CANDIDATE=YES
```

Parent independent intake accepted:

```text
PRODUCTION_ACCEPTED = YES
P0_PM_ACCEPTED = YES
```

The production Gate used one SSH, one V-PLC state GET and one read-only PostgreSQL query. `plan_active=true`, so no production/start POST was required. DB writes, lifecycle, remote filesystem mutation, retry and reconnect were all zero.

Accepted current-lineage production fact:

```text
station_id        = WS01
production_result = ok
cycle_counter     = 113095
source_event_id   = sha256:993ab6991534339db39c14180ebf6d1349a870035db7a3d5ed336147479ded8a
fact_key          = sha256:a8c7322bb96a6858aff226d25c23c731bb5cfcfa059a47b2ecefbea78efc8422
content_fingerprint = sha256:36426c0d264fc4a14a531596844751cf13643019658ed4aaee7921f4872181f9
event_ts          = 2026-08-11T05:44:25.000000Z
accepted_at       = 2026-08-11T05:44:25.728731Z
config_hash       = 0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
config_version    = 2026.06.26-slice-a
```

This is the decisive P0 product truth: the accepted corrected Collector lineage is active/runtime-loaded and produced a canonical accepted production fact under the current config.

Do not reopen P0 Remote Closure without a fresh contradiction to these accepted facts.

---

## 9. B1 eligibility reassessment — accepted result and exact nuance

B1 reassessment report:

```text
path    = docs/reports/sprint4_d2_r7b_p0_b1_eligibility_reassessment_local_readonly.md
bytes   = 6668
SHA-256 = f377bf64771f5a0e7fdc5d2a2abe2c7e19f77922dd3022878085372d65290985
attempt = 1 / exactly one reassessment
terminal = HOLD / B1_ELIGIBLE=NO / B1_PREREQUISITE_FACT_OR_MVP_ALIGNMENT_MISSING
```

Accepted parent flags:

```text
B1_ELIGIBILITY_REASSESSED = YES
B1_ELIGIBLE = NO / B1_PREREQUISITE_FACT_OR_MVP_ALIGNMENT_MISSING
B1_EXECUTION_AUTHORIZED = NO
SHADOW_PM_STOP = YES
NO B1 EXECUTION TASK CREATED
```

Important nuance: pre-lock evidence in the B1 task had already reverified the accepted P0 lineage, production fact, three focused PASS reviews, source/test no-drift and `MVP_ALIGNMENT=YES`. The reassessment then encountered a local report-construction mechanics failure after its immutable lock. The task contract required fail-closed terminalization and prohibited retry, so the only allowed B1 eligibility result was `NO`.

Therefore the current `B1_ELIGIBLE=NO` is a valid governance terminal and must be obeyed, but it must **not** be misrepresented as proof that the underlying P0 production fact disappeared or that the corrected product lineage failed.

Do not repeat the B1 reassessment inside the completed Shadow Goal. If the Owner later wants B1 work, open a fresh mainline planning decision that explicitly addresses the accepted `B1_ELIGIBLE=NO` baseline and obtains new authority before any B1 execution.

---

## 10. Final Shadow P0 ledger and terminal counters

Final ledger:

```text
path    = docs/reports/shadow_pm_p0_remote_closure_ledger.md
bytes   = 64881
SHA-256 = 9a5e934f12e94cba9a0fb0811f0d6a4599ac5092bd3821bdee957375f253cf73
```

Final accepted state:

```text
GOAL_STATUS = COMPLETE
P0_PM_ACCEPTED = YES
PRODUCTION_ACCEPTED = YES
REMOTE_IMAGE_ACCEPTED = YES
REMOTE_LOADED_OBJECT = YES
ACTIVATED = YES
RUNTIME_LOADED = YES
B1_ELIGIBILITY_REASSESSED = YES
B1_ELIGIBLE = NO
B1_EXECUTION_AUTHORIZED = NO
SHADOW_PM_STOP = YES
GOAL_TERMINAL = PASS / P0_REMOTE_CLOSURE_AUTONOMOUS_GOAL_COMPLETE
NEXT_ACTION = STOP / NO_B1_EXECUTION_TASK / SHADOW_PM_STOP
```

Final Shadow P0 dual-budget counters:

```text
P0_PROGRESS_GATES_USED = 11 / 12
P0_CONTROL_PLANE_RECOVERY_GATES_USED = 17 / 17
P0_TOTAL_DISPATCHED_GATES_USED = 27 / 29
B1 local reassessment = not counted as a P0 execution Gate
```

Treat these counters as historical evidence of this completed autonomous Goal. They do not automatically grant, deny or define budgets for a future independent mainline phase.

---

## 11. Governance/control-plane lessons from P0 closure

The P0 Goal succeeded, but a large fraction of recovery Gates were consumed by execution/governance mechanics rather than product defects. Preserve these lessons so the next phase does not repeat them:

1. **Semantic identity over literal formatter text.** Exact type/non-symlink semantics, bytes and SHA are the security properties. A different `stat` formatting string that proves the same object should not become a false product blocker unless a task specifically needs command identity for a real safety reason.
2. **Do not assume executable paths.** Repeated `/usr/bin/test` assumptions created false HOLDs. Freeze actual executable identities only when needed.
3. **Do not add redundant payload formatting gates.** A trailing newline/base64 formatter discrepancy caused governance inflation without changing payload byte-roundtrip truth.
4. **Do not repeat focused reviews automatically.** The attempted “four remaining Gates” calculation incorrectly counted Reliability/DQ/Verification again despite unchanged reviewed lineage. Owner clarification rejected that inflation; the production Gate alone was sufficient before PM acceptance.
5. **Keep immutable locks tied to mutation/authority safety, not ordinary report cosmetics.** The one B1 eligibility attempt fail-closed because a report patch was malformed after lock. Future designs should avoid making non-safety-critical report construction mechanics irrecoverable unless the task truly requires that property.
6. **Separate product progress from control-plane recovery.** The dual-budget reset was useful because many HOLDs occurred before command start/remote action. Future PMs should diagnose this distinction rather than equating recovery count with product instability.
7. **No attempt-family laundering.** R1/L0/F0 historical counters were explicitly carried across renamed tasks where causal continuity existed.
8. **When evidence work exceeds product work, run the MVP/governance inflation check before adding another validator/reconciliation layer.**

These are carry-forward PM lessons. This handoff does not authorize modifying `pm_operating_rules.md`. A stable rule change requires a separate governance task and Owner authority.

---

## 12. Shadow authority artifacts — historical controls, not future executable authority

Important historical authority/control documents:

```text
docs/thread_handoff/shadow_pm_p0_remote_closure_charter.md
16624 / 2d947d6a1cebff4e770086f0822dad21962a6682bdf8b63f26e23142647caa0e

docs/thread_handoff/shadow_pm_p0_owner_authority_amendment_20260811_budget_scope_reset.md
12199 / 5bf1ccb12ff846c047ca76dc0656a95f01a1cf4cc9ff52187a648477de6f6e04

docs/thread_handoff/shadow_pm_p0_owner_authority_clarification_20260811_oci_descriptor_config_mapping.md
7655 / ef87e1bab28b9e62ef0b61d54e2ee1f51b88c6b670999797606ac765633ff453

docs/thread_handoff/shadow_pm_p0_owner_authority_amendment_20260811_runtime_recovery_budget_plus_one.md
6908 / e9ee622cdac1a98c6fb7fcca5a69bd60ea9c0fa12f9f0593f0a85a7433dca518

docs/thread_handoff/shadow_pm_p0_owner_authority_clarification_20260811_remaining_gate_recalculation.md
9210 / 0dceeab191afca7272f7f5bb4b1aa8ff1351436531f67e9b10de0434f3d0dc62
```

The prepared `remaining_gate_budget_plus_one` amendment was explicitly rejected and never became effective:

```text
docs/thread_handoff/shadow_pm_p0_owner_authority_amendment_20260811_remaining_gate_budget_plus_one.md
5050 / 735d5c08335f63071488ca59609019bfd6331f28ce1b37f497392839e5861223
status = REJECTED / NOT EFFECTIVE
```

Do not reuse any of these completed-Goal authority documents as executable authority for a new phase. They are historical context only.

---

## 13. Parallel workstream isolation

Independent branch/workstream remains:

`FIELD-VALIDATION-COLLECTOR-DB`

Branch handoff:

```text
docs/thread_handoff/chatgpt_pm_handoff_real_device_collector_db_branch_260808-0832.md
15447 / d71174ad454ea75c2a0bb721182dfc49ef66635235a351670cb939c572773389
```

Branch plan:

```text
docs/reports/branch_real_device_collector_db_field_validation_plan.md
22245 / d885ff5b2e41f938b95dec3a8238bdd0148a11116028527d71726562bdac3d02
```

Mainline PM must not mutate, absorb, stage, clean, rebase, merge or repurpose that workstream without explicit Owner instruction. Do not infer branch authority from the fact that both workflows may reference the same physical repository root.

---

## 14. Current non-authorized surfaces and recommended next decision

At transfer, **no next mainline implementation phase is authorized**.

Not authorized merely by this handoff:

- B1 execution;
- a second B1 eligibility reassessment;
- C1+;
- SSH/remote Docker/Compose/filesystem activity;
- Collector restart/activation/rollback;
- V-PLC/PLC production stimulus or control writes;
- DB/API writes or schema migration;
- dashboard/frontend expansion;
- architecture redesign/MVP redefinition;
- parallel branch mutation/merge;
- Git stage/commit/push/tag/release;
- cleanup/stash/reset/restore/rebase/merge/checkout.

Recommended successor decision after takeover:

1. confirm P0 closure baseline and stop reopening it;
2. report `P0_PM_ACCEPTED=YES` and accepted `B1_ELIGIBLE=NO` baseline;
3. ask/receive the Owner's desired next mainline objective if not already supplied;
4. if Owner wants B1, first create a fresh planning/reconciliation slice explaining the exact accepted `B1_ELIGIBLE=NO` terminal and what prerequisite/authority would be required before execution;
5. if Owner wants another roadmap branch, classify it independently against the current MVP and existing P0 production truth;
6. do not carry the completed Shadow Goal's recovery machinery into the new phase by default.

The correct immediate next state is **PM takeover / planning**, not runtime execution.

---

## 15. Copyable successor Mainline PM takeover prompt

Copy the following into a fresh ChatGPT PM window. The launcher should also provide this handoff's exact bytes/SHA-256 measured after creation.

```text
你现在接手 Edge MES Demo 主线，担任新的 Mainline ChatGPT PM。

项目绝对路径：
`/Users/chenjie/Documents/MES/edge-mes-demo`

你的第一项工作是严格 read-only Mainline PM takeover。不要执行任何 SSH、Docker/Compose remote action、Collector lifecycle、V-PLC/PLC action、DB write、B1 execution、Git mutation 或并行分支 mutation。

首先机械核验并完整读取：

`docs/thread_handoff/chatgpt_pm_handoff_260811-1412.md`

Expected identity 由 Owner/上一任 PM launcher 提供：
- regular / non-symlink
- exact bytes
- exact SHA-256

身份 PASS 后，按照 handoff Section 1 的顺序进行只读恢复，并完整读取 `docs/thread_handoff/pm_operating_rules.md`。

随后机械核验 live Git：
- physical cwd / Git top-level
- branch
- HEAD
- origin/main
- `HEAD...origin/main` ahead/behind
- `git status -sb`
- worktree diff name-only
- cached diff name-only

Expected transfer baseline：
- branch = `main`
- HEAD = `dbe5706e4b01387101f2a4666e73f3c13ffeb0e9`
- origin/main = `2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35`
- ahead/behind = `1/0`
- cached/staged = empty
- protected tracked dirty = `docs/current_status.md`, `docs/thread_handoff/pm_operating_rules.md`
- large historical untracked task/report corpus = preserve

必须确认最终主线状态：
- `P0_PM_ACCEPTED = YES`
- `PRODUCTION_ACCEPTED = YES`
- accepted production fact = `WS01 / ok / cycle 113095`
- `REMOTE_IMAGE_ACCEPTED = YES`
- `ACTIVATED = YES`
- `RUNTIME_LOADED = YES`
- `B1_ELIGIBILITY_REASSESSED = YES`
- `B1_ELIGIBLE = NO / B1_PREREQUISITE_FACT_OR_MVP_ALIGNMENT_MISSING`
- `B1_EXECUTION_AUTHORIZED = NO`
- `SHADOW_PM_STOP = YES`
- Shadow P0 Goal terminal = `PASS / P0_REMOTE_CLOSURE_AUTONOMOUS_GOAL_COMPLETE`

特别注意：B1 的 `NO` 是唯一一次 post-P0 eligibility reassessment 的有效 fail-closed terminal；不得把它改写成 P0 产品失败，也不得自动执行或重复 B1。任何后续 B1 工作必须是新的 Owner-authorized planning decision。

不要自动重跑既有 Reliability / Data Quality / Verification focused reviews，除非 reviewed lineage/contract 改变或 fresh evidence 建立可信 false-PASS 风险。

不要恢复或继续已完成的 Shadow P0 Goal。它的 dual-budget counters 和 authority amendments 只作为历史 closure evidence，不是新阶段的 executable authority。

并行 workstream `FIELD-VALIDATION-COLLECTOR-DB` 保持隔离；禁止吸收、清理、stage、merge 或变更。

完成 read-only takeover 后，只输出：
1. TAKEOVER PASS/HOLD；
2. live Git baseline；
3. P0 accepted terminal summary；
4. B1 accepted eligibility/authority boundary；
5. dirty/untracked preservation status；
6. 当前没有自动授权的下一执行 Gate；
7. 基于 Owner 当前目标给出下一最小 planning recommendation；如果 Owner 尚未给出下一目标，则停在 planning boundary，不要自行启动 B1/C1/remote/Git work。
```

---

## 16. Handoff terminal state

Mainline transfer state:

```text
HANDOFF_REASON = P0_REMOTE_CLOSURE_COMPLETED_AND_MAINLINE_BASELINE_RESET
SHADOW_P0_GOAL = COMPLETE / DO_NOT_RESUME
SOURCE_COMMIT = dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
LOCAL_ACCEPTED_OCI_DESCRIPTOR = sha256:cef401fcfb19f50aacb3d5ac6d6c73f9aeb582811a85c14eeb5fdec03eed0ad0
REMOTE_ACCEPTED_DOCKER_CONFIG_ID = sha256:a199e6417c3ed5e42724201122ea4014604b561593a243039aef72d71900b252
CURRENT_COLLECTOR_FULL_ID = 6cab966e18bc1b5b349a0901793ff89ab7bfcde889ff7b2e911746e413eac25e
ACTIVATED = YES
RUNTIME_LOADED = YES
PRODUCTION_ACCEPTED = YES
PRODUCTION_FACT = WS01 / ok / cycle 113095
P0_PM_ACCEPTED = YES
B1_ELIGIBILITY_REASSESSED = YES
B1_ELIGIBLE = NO / B1_PREREQUISITE_FACT_OR_MVP_ALIGNMENT_MISSING
B1_EXECUTION_AUTHORIZED = NO
SHADOW_PM_STOP = YES
MVP_ALIGNMENT = YES
NEXT_MAINLINE_EXECUTION_GATE = NONE / OWNER DECISION REQUIRED
GIT_STAGE_COMMIT_PUSH_TAG_AUTHORITY = NO
```

This handoff authorizes read-only successor takeover only. It must not be treated as executable authority for B1, C1+, remote action, production mutation, Git mutation, or the parallel field-validation workstream.
