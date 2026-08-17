# FV1A Debug-Scope correction R1 report

日期：2026-08-17
项目：Edge MES Demo
线程：独立 Integration Thread
结论：**PASS WITH RECOMMENDATIONS**（仅限本地 source/test/synthetic evidence；不等同于真实 PLC、远端、Docker runtime、Owner 或 production acceptance）

## 1. Authority and identity

本轮唯一 authoritative task file：

`docs/thread_handoff/pm_task_20260817T0302Z_fv1a-debug-scope_station-scope-correction-r1.md`

核验结果：

- type：regular file，non-symlink
- bytes：`23846`
- SHA-256：`a7e54cca1bdabb70471712ce3357d4410b67a45b4444747dacd569ab0ea18789`
- launcher 与 task-file path/type/bytes/SHA-256/authority：一致
- superseded predecessor：`docs/thread_handoff/pm_task_20260817T0236Z_fv1a-debug-scope_station-scope-correction.md` 未作为本轮 authority 使用

本报告只覆盖 FV1A Debug-Scope correction R1：selected-station Debug Pilot、partial-scope candidate/projection/read-only Test Connection、Debug Ready 与 full-line activation 分离、focused local validation 及本地精确 commit。未获得真实 PLC/Wyse/Raspberry Pi、Candidate activation、Collector/API/Dashboard Docker lifecycle、FV1B-B/FV2/FV3、amd64/mainline platform mutation、push 或 tag authority。

## 2. Baseline and bounded change

执行锁定时 repository root 为：

`/Users/chenjie/Documents/MES/edge-mes-demo`

基线：

- branch：`main`
- HEAD：`a7ae6c71b0d23bd30bf52a7f5cacef8893769d58`
- `origin/main`：`6226bf3fb716880a176f9eb642b8139cef3255a6`
- ahead/behind：`23 / 0`
- staged paths：`0`
- pre-existing tracked dirty paths：仅 governance/current-status 文件，未纳入本轮 commit
- pre-existing untracked docs corpus：保留，未 adopt/delete/reset/stash/clean

本轮 source/test/report exact allowlist：

```text
common/line_config/debug_contract.py
common/line_config/runtime_projection.py
api/app/services/deployment_plc.py
api/tests/test_deployment_plc_api.py
collector/tests/test_field_debug_candidate_read_done.py
frontend/src/components/deployment-plc/DeploymentPlcClient.tsx
frontend/src/components/deployment-plc/__tests__/DeploymentPlcClient.test.tsx
frontend/src/lib/deploymentPlc/apiClient.ts
frontend/src/styles/globals.css
docs/reports/fv1a_debug_scope_correction_report_20260817.md
```

未修改 Collector product source、`runtime_layout.py`、active/baseline mapping、root `docker-compose.yml`、FV1B-A artifact/report 或任何 remote/runtime deployment 文件。

## 3. Implemented contract

### 3.1 Scope normalization and validation

- 新增 deterministic `debug_scope.station_ids`，必须为 non-empty、有序、无重复 selected station list。
- omitted scope 保持 backward compatibility：默认当前 enabled selected-line stations/full-line。
- explicit scope 拒绝 unknown、disabled、duplicate station；最终按 trusted line route order canonicalize。
- line/base topology 保留为完整 line topology；Debug Pilot scope 只表示 execution/testing subset。
- candidate、projection、save、hash、engineering export、write allowlist 均只包含 selected stations，不创建 unselected dummy mapping。

### 3.2 Partial projection and readiness

- WS03-only candidate/projection 只生成 WS03 executable station。
- scoped projection 的 `entry_station_id` 与 `terminal_station_id` 均为 `WS03`，route graph 不生成 WS01/WS02 边。
- explicit base topology metadata 仍保留完整 WS01/WS02/WS03 topology，便于工程导出和回到 full-line scope。
- 每个 selected station 保留 signal/range/type/direction/PLANNED/CONFIRMED 以及 Read_Done-only validation。
- 增加 `debug_ready`；partial scope 可以 Debug Ready。
- partial scope 的 `ready_to_activate` 保持 false；full-line activation 与 Debug Ready 是两个独立状态。
- partial save/load status 使用 `NOT ACTIVE / DEBUG PILOT ONLY / FULL-LINE ACTIVATION NOT READY`，不会伪装成 full-line activation-ready。
- partial activation fail-closed：不执行 PLC test 或 mutation，也不把 WS03-only candidate 当作 full 3WS activation。

### 3.3 Read-only Test Connection

- Test Connection 以 `debug_ready` 为准，不以 partial `ready_to_activate` 为准。
- 只读取 selected candidate station 的 `db_number/read_start/read_length`；不从 runtime DB fallback。
- operation sequence 为 connect、每个 selected station 一次 `db_read`、disconnect；不执行写入。
- response 报告 `probed_station_ids`、`probed_ranges`、`read_bytes`，便于确认 selected-station read boundary。

### 3.4 UI and export

- UI 展示所有 enabled station choices，支持 select/deselect。
- 展示 `Debug Pilot Scope: N / total`。
- station editor 只显示 selected station。
- readiness panel 分别展示 Debug Ready 与 Full-line activation；WS03-only 明确显示 full-line `NOT READY`。
- engineering export 同时带出完整 base topology 与 selected Debug Pilot scope。

## 4. Synthetic WS03 qualification

本地 synthetic path 使用 configured WS03 DB103/range，并保留 runtime DB104 作为 fallback-detection guard：

- mapping/plans：仅 WS03；WS01/WS02 station plans 为 zero
- selected read range：DB103, offset `0`, length `346`
- storage commit 成功后，恰好一次 configured WS03 Read_Done write：`(103, 6, 0x0b)`
- event order：storage commit 在前，write 在后
- WS01/WS02 writes：`0`
- storage failure：writes `0`
- contract write allowlist：仅 WS03

该证据是 local synthetic qualification，不是 real PLC/Wyse/Raspberry Pi field evidence。

## 5. Validation evidence

Focused validation results：

```text
api/tests/test_deployment_plc_api.py                         31 passed
collector/tests/test_field_debug_candidate_read_done.py      2 passed
collector/tests/test_r3_runtime_projection.py                4 passed
collector/tests/test_r2b_connection_authority.py             2 passed
frontend/src/components/deployment-plc/__tests__/...         5 passed
npm run typecheck                                            PASS
npm run build                                                PASS
git diff --check                                             PASS
```

Collector synthetic test 使用 local Snap7 loopback-only test path；没有连接真实 PLC 或远端设备。未执行 Docker lifecycle、browser/remote probe、real device read/write、candidate activation、push 或 tag。

## 6. Protected-byte continuity

以下 protected entries 在执行前后保持 exact identity：

| path | bytes | SHA-256 |
|---|---:|---|
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` |
| `data/deployment-config/active/mapping.yaml` | 14217 | `2b70079ccac4e2293e5a225352f5b4a30d180ed91176c6204d307c53589930a0` |
| `docker-compose.yml` | 6191 | `5e7009a5870919313c4355dd8af7e6f92194b62307bc74d0030f43a47719e483` |
| `deploy/wyse/README.md` | 4935 | `b994754e98ea876a6faf3048009157f8153434e6ad211ba11d95a03f9e5f6e7e` |
| `deploy/wyse/docker-compose.wyse.yml` | 7163 | `e49483a196709390b4b5f1232b8619e8e892be5e8c53a2cc7a0d2bd69a346a98` |
| `docs/reports/evidence/fv1b-a/amd64_image_manifest.json` | 6936 | `0c5339f9a5674b75bc63998ad6926b7c714148ae28870e60ea577578f3ecb694` |
| `docs/reports/evidence/fv1b-a/manifest.sha256` | 311 | `8d84d5475cddf0659037a8b84148afd12cfd6915f75ce36287565767d2bc5108` |
| `docs/reports/fv1b_a_wyse_amd64_branch_packaging_report_20260817.md` | 17229 | `cfda17809e9a87771caa533ac5cdf47d2b87d5afd6c69eb3034f9ea71a8d315d` |

## 7. Boundary counters and recommendation

```text
REAL_PLC_CONNECT=0
REAL_PLC_READ=0
REAL_PLC_WRITE=0
WYSE_REMOTE_ACTION=0
RASPBERRY_PI_REMOTE_ACTION=0
REMOTE_MUTATION=0
```

Platform boundary：

```text
OFFICIAL_MAINLINE_PLATFORM=RASPBERRY_PI_ARM64
WYSE_AMD64=DEBUG_BRANCH_ONLY
X86_FORMAL_PRODUCT_LINE=NOT_AUTHORIZED
```

Recommendation：将本轮结果交 Mainline PM intake。只有 PM 接受本报告及 exact local commit 后，Owner 才可在本地按下一 gate 进行 bounded Docker rebuild/preview API + Dashboard 检查；该 preview 不应被表述为 candidate activation、真实设备联调或 production acceptance。

## 8. Exact local closeout

授权的唯一 commit subject：

```text
fix: support scoped plc debug stations
```

本报告随上述 exact allowlist 一并提交；最终 commit SHA、post-commit HEAD/ahead/staged 状态由 closeout evidence 记录在本线程最终回执中。不得 push、tag 或执行任何未授权后续阶段。
