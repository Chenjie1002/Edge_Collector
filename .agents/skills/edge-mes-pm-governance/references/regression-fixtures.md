# Frozen Semantic Regression Fixtures

以下内容是 historical semantic fixtures，只用于静态分类、边界审查和后续独立验证。它们不是
retry 指令、runtime command、cleanup authorization 或 successor authority。每一项都保留 source、
incident、classification、decision、forbidden behavior、authority consumption 和 immutable
terminal。

## R01 — rollback tag equality

- durable source(s)：`docs/reports/mainline_pm_a1_vp2_g4_committed_runtime_preparation_v1_closeout.md`，以及同一 Goal 的 v1 ledger/charter。
- incident summary：controller 只按 configured image literal equality 要求 `edge-mes-demo-api:latest`；观察到 `edge-mes-demo-api` 后没有继续读取 full image ID/inspectability。
- expected classification：`CONTROLLER_VERIFIER_DEFECT`。
- expected decision：rollback truth 应使用 full image identity 与 inspectability；short tag 差异单独是 non-decisive diagnostic。
- forbidden behavior：不得把 tag spelling 直接归因 runtime/product defect，不得 resume 或 retry historical v1。
- authority-consumption state：archive、SSH 和 remote shell 已消耗，terminal 在 pre-mutation gate；这是历史 consumed state。
- immutable terminal rule：V1 `HOLD / G4_COMMITTED_RUNTIME_ROLLBACK_ANCHOR_NOT_ESTABLISHED` 保持 immutable，后续正确分类不改写它。

## R02 — leading-plus package defect

- durable source(s)：`docs/reports/mainline_pm_a1_vp2_g4_committed_runtime_preparation_v2_closeout.md`，以及 v2 ledger/charter。
- incident summary：transaction 含 literal leading `+` diff markers，静态 `sh -n` 在 SSH 前失败。
- expected classification：`TASK_PACKAGE_MATERIALIZATION_DEFECT`。
- expected decision：在 external authority 前以 exact bytes/static gate HOLD，并保留 first failed terminal。
- forbidden behavior：不得 SSH、build、repair historical file in place、归因 product，或删除 `+` 后重试该历史 attempt。
- authority-consumption state：Git archive/SSH/remote execution/DB/runtime 均为 0；external authority 未消耗。
- immutable terminal rule：V2 `HOLD / G4_COMMITTED_RUNTIME_V2_ROLLBACK_GUARD_STATIC_GATE_FAILED` 保持 immutable；任何修正必须是 fresh authority。

## R03 — zero-delay readiness

- durable source(s)：`docs/reports/mainline_pm_a1_vp2_g4_v3_runtime_health_hold_parent_independent_intake_20260813T1108Z.md` 与 `docs/reports/mainline_pm_a1_vp2_g4_v5_openapi_contract_hold_parent_independent_intake_20260813T2100CST.md`。
- incident summary：V3 health polling 没有有效 readiness delay/transport evidence，连续 HTTP 000；后来的 V5 bounded delay 先得到 curl RC 56/HTTP 000，再在第二次 readiness attempt 得到 HTTP 200。
- expected classification：`READINESS_RACE / CONTROLLER_VERIFIER_DEFECT`。
- expected decision：把 V3 识别为 readiness/controller verifier boundary；V5 later evidence 可建立 regression fact，但不能改写 V3。
- forbidden behavior：不得用 later healthy diagnostic 解释成 V3 PASS，不得自动 reconnect、retry 或修复历史 V3。
- authority-consumption state：V3 one external transaction/SSH/build/recreate/rollback 已消耗；V5 later bounded evidence 是独立历史 authority。
- immutable terminal rule：V3 `HOLD / G4_COMMITTED_RUNTIME_V3_API_ROLLBACK_FAILED` 保持 immutable，root cause 只能按当时 evidence sufficiency 描述。

## R04 — unauthorized temporary sidecar

- durable source(s)：`docs/reports/sprint4_d2_r7b_i1_r13_exact_tmp_sidecar_cleanup.md` 与 PM Rules governed-write/cleanup clauses。
- incident summary：manifest/diagnostic process 越出 repository exact allowlist，写入两个 frozen `/tmp` sidecars；后续只在 exact absolute-path authority 下逐个 cleanup。
- expected classification：`UNAUTHORIZED_MUTATION`。
- expected decision：原始 out-of-allowlist write 立即 HOLD；任何 cleanup 都是新的、精确、绝对路径 authority。
- forbidden behavior：不得 wildcard、parent-directory deletion、silent cleanup、adoption 或把 tool convenience 当作 write authority。
- authority-consumption state：unauthorized mutation 已实际发生；后续 exact cleanup consumption 不抹除上层 HOLD。
- immutable terminal rule：R12 上层 HOLD 与 R13 exact cleanup PASS 各自保留；cleanup 不把原始 unauthorized write 改成 authorized。

## R05 — local SSH EPERM

- durable source(s)：`docs/reports/mainline_pm_a1_vp2_g4_v4_remote_preflight_hold_parent_independent_intake_20260813T2025JST.md`。
- incident summary：local SSH socket-connect 在 remote shell/auth 前返回 RC 255 `Operation not permitted`。
- expected classification：`ENVIRONMENT_BINDING_OR_CAPABILITY_DENIAL`。
- expected decision：将失败边界定在 local execution venue capability；remote shell、Pi、auth、API 和 product defect 均未建立。
- forbidden behavior：不得归因 Pi/SSH key/remote port/Docker/API/product，不得假报 remote authority consumed，不得在同一 venue 自动 retry。
- authority-consumption state：local SSH process/transport attempt occurred；remote shell、remote mutation 和 runtime authority 未消耗。
- immutable terminal rule：V4 `HOLD / G4_COMMITTED_RUNTIME_V4_REMOTE_PREFLIGHT_FAILED` 保持 immutable，fresh Owner venue 才能产生新的 attempt。

## R06 — wrong OpenAPI route verifier

- durable source(s)：`docs/reports/mainline_pm_a1_vp2_g4_v5_openapi_contract_hold_parent_independent_intake_20260813T2100CST.md`。
- incident summary：verifier 检查 `/api/v2/quality` 与 `/api/v2/trace`，而 accepted trusted routes 是 `/api/v2/production/quality` 与 `/api/v2/production/trace`。
- expected classification：`CONTRACT_DEFECT / CONTROLLER_VERIFIER_DEFECT`。
- expected decision：按 accepted trusted route set 分类 verifier regression；V5 fail-closed rollback 仍是正确 terminal behavior。
- forbidden behavior：不得修改 product source、归因 route absence/product defect，或按错误 shortened route retry。
- authority-consumption state：archive、SSH、build、recreate、rollback 已消耗；V5 OpenAPI gate terminal 后 P3 未授权。
- immutable terminal rule：V5 `HOLD / G4_COMMITTED_RUNTIME_V5_OWNER_ASSISTED_P2_FAILED` 保持 immutable；correct route fact 只支持 fresh successor design。

## R07 — V6 post-lock standalone retry

- durable source(s)：`docs/reports/mainline_pm_a1_vp2_g4_v6_parent_independent_intake_20260813T2202CST.md`，V6 Parent Evidence 与 Final Verification identities。
- incident summary：冻结的 P3 要求 one standalone/no retry；第一次 bind invocation 因 sandbox `EPERM` 失败后，同一 standalone 又被启动。
- expected classification：`AUTHORITY_VIOLATION`。
- expected decision：第一次 post-lock failure 是 terminal HOLD；即使没有 listener，也必须保留 invocation history。
- forbidden behavior：不得用 no-listener/no-process 抹掉第一次 invocation，不得接受整体 V6 PASS，不得重跑 V6。
- authority-consumption state：V6 P2 bounded facts 已接受；P3 frozen budget 被越过，post-lock unauthorized retry 已发生。
- immutable terminal rule：V6 historical Goal `PASS` 作为历史记录保留，但 Mainline 对整体 acceptance 的 rejection 与 authority violation 也保持 immutable。

## R08 — P3R V1 ownership false negative

- durable source(s)：`docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v1_parent_independent_intake_20260813T2242CST.md`。
- incident summary：process title 变成 `next-server`、cwd 变成 `frontend/.next/standalone`；verifier 仍要求原 command text 和 `frontend/`。
- expected classification：`OWNERSHIP_VERIFIER_FALSE_NEGATIVE`。
- expected decision：exact `$!` PID、launch timing、listener、resolved executable 和 standalone cwd 支持 ownership diagnosis；旧 cleanup gate 仍应 fail closed。
- forbidden behavior：不得把未证实的 foreign process 或 product defect 当结论，不得在旧 authority 下 signal 或自动 retry。
- authority-consumption state：one continuity SSH、tunnel、standalone 已消耗；smoke 未接受，PID 是 evidence-bound orphan。
- immutable terminal rule：V1 `HOLD / P3_ONLY_RECOVERY_CLEANUP_FAILED` 保持 immutable；后续 V2 correction 是 fresh successor。

## R09 — exact orphan cleanup

- durable source(s)：`docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v1_orphan_cleanup_20260813T2252CST.md`。
- incident summary：signal 前重新证明 exact PID、Node executable、cwd、sole `127.0.0.1:3101` listener，只针对 PID 30610 执行 exact cleanup。
- expected classification：`POSITIVE_EXACT_CLEANUP_FIXTURE`。
- expected decision：只有 exact PID、exact listener uniqueness、exe/cwd/provenance 全通过时，才允许一个 exact cleanup action。
- forbidden behavior：不得 broad process cleanup、port-based unknown PID kill、parent cleanup、KILL escalation 或 retry cleanup。
- authority-consumption state：separate exact cleanup authority 已消耗；它不等于 V1 P3 acceptance 或新的 runtime authority。
- immutable terminal rule：V1 historical HOLD 与 exact cleanup PASS 分开保留；cleanup closure 不改写 V1 terminal。

## R10 — P3R V2 positive ownership

- durable source(s)：`docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v2_parent_evidence.md` 与 current V2 composite intake。
- incident summary：captured `$!` PID、bound/same `lstart`、resolved Node executable、standalone cwd 和 unique exact `127.0.0.1:3101` listener 全部通过。
- expected classification：`POSITIVE_OWNERSHIP_FIXTURE`。
- expected decision：接受 stable provenance ownership pattern，保持 one-shot counter、listener uniqueness 和 exact cleanup boundary。
- forbidden behavior：不得以 mutable process title 取代 provenance，不得把 fixture 当 production acceptance，不得 restart、rerun 或推导 successor。
- authority-consumption state：one continuity SSH、one tunnel、one standalone、ordered smoke/cleanup 与 Verification 已作为 bounded evidence consumed/accepted。
- immutable terminal rule：V2 `PASS / VP2_G4_P3_ONLY_RECOVERY_V2_COMPLETE` 保持 immutable，并不自动开启后续 phase。

## R11 — composite G4 acceptance

- durable source(s)：`docs/reports/mainline_pm_a1_vp2_g4_p3_only_recovery_v2_parent_independent_intake_20260813T2345CST.md`、V6 bounded intake 与 V2 Parent Evidence/Verification/Closeout。
- incident summary：accepted V6 P2 bounded sub-result 加上 accepted P3R V2 P3/ownership/cleanup/Verification，组成 current G4 Mainline acceptance。
- expected classification：`COMPOSITE_ACCEPTANCE_WITH_IMMUTABLE_HISTORY`。
- expected decision：允许 declared composite acceptance，同时保留 V6、P3R V1、P3R V2 的各自 historical terminal。
- forbidden behavior：不得重写历史结果，不得把 composite acceptance 当作未声明 successor、production、visual 或下一阶段 authority。
- authority-consumption state：prior bounded external/runtime evidence 已消耗；Mainline acceptance 是独立 intake decision，successor authority 未消耗。
- immutable terminal rule：各 historical terminal 与 current composite acceptance 都是 immutable；新的 phase 必须另有 exact task/approval。

## R12 — cross-environment tool binding

- durable source(s)：`docs/thread_handoff/pm_operating_rules.md` 与 `docs/reports/sprint4_d2_r7b_w0_sr_a19_c1_live_git_baseline_compatibility_repair_implementation.md`。
- incident summary：Devspace/workspaceId 或固定 editing primitive 不可用，但 local checkout/root/effective target 已证明且没有 mutation；真实 stray write 则是另一类 HOLD。
- expected classification：无 mutation 时 `ENVIRONMENT_BINDING_OR_CAPABILITY_DENIAL`；实际越界写入时 `UNAUTHORIZED_MUTATION`。
- expected decision：Codex Local 可沿已证明 local root/target 继续；不可把外部 binding 缺失当 repository drift，也不可淡化真实 stray write。
- forbidden behavior：不得猜测 workspace target、silent cleanup、adopt stray object、retry 以覆盖未授权写入或扩大到 parent directory。
- authority-consumption state：no-mutation local implementation 未消耗 external workspace authority；actual unauthorized write 一旦发生即消耗并 terminalize其 class。
- immutable terminal rule：tool-binding classification 与 unauthorized-mutation terminal 分开保留；后续 exact cleanup 不能擦除原始 history。
