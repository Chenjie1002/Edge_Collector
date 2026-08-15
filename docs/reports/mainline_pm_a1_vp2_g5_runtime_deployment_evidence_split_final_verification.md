# Mainline PM Final Verification — A1 VP2-G5 Runtime Deployment + Evidence Split

结论：**PASS / A1_VP2_G5_RUNTIME_DEPLOYMENT_EVIDENCE_SPLIT_VERIFIED**

验证角色：Mainline PM direct Final Verification

验证范围：仅验证已发布修复 `6226bf3fb716880a176f9eb642b8139cef3255a6` 在远端 Collector runtime 中对 `result code 3 / SKIPPED -> canonical skip` 路径的实际生产证据。本文不声明整个 Edge MES 全面 production-ready，不建立 Owner Visual Acceptance，不授权 A1-S2。

## 1. Frozen product candidate

```text
PUBLISHED_COMMIT = 6226bf3fb716880a176f9eb642b8139cef3255a6
COMMIT_MESSAGE = fix(collector): canonicalize skipped result token
SOURCE_REPAIR = collector/app/services/station_event_runtime_source.py::_decode_result
EXACT_CAUSE = RESULT_VOCABULARY_NORMALIZATION_MISMATCH
SOURCE_RESULT_CODE = 3
MAPPING_TOKEN = SKIPPED
CANONICAL_TOKEN = skip
```

本地 product repair、focused regression、Reliability/Verification 早前均已接受；产品 commit 已 push，HEAD/origin/main 在本轮 Final Verification 前后仍保持该 commit。

## 2. Runtime evidence authority

最终 runtime evidence：

```text
RESULT_PATH = docs/reports/mainline_pm_a1_vp2_g5_runtime_deployment_evidence_split_owner_runtime_result_r4.txt
RESULT_TYPE = regular / non-symlink
RESULT_BYTES = 5658
RESULT_SHA256 = ff4c4489e58c0b37abba952d94ec2cf8766da4f27157133c6c26ba124d38f4fe
RUNNER_TERMINAL = PASS / DEPLOYMENT_AND_EVIDENCE_CAPTURE_COMPLETE
REMOTE_RUNTIME_RC = 0
REMOTE_STATE = STABLE
DEPLOYMENT_EVIDENCE_CAPTURED = YES
```

R4 使用 transport-bound identity：

```text
LOCAL_MANIFEST_DIGEST = sha256:b8ced083941cdf9b8e39aefb69844a8f4b69e5dda1cbfdba134f35f26130eea6
TRANSPORT_CONFIG_DIGEST = sha256:f51a445aa93ba2d8e526095b9cedfc621ea49e82a70dd726eaebfd0cdac3b901
REMOTE_CANDIDATE_IMAGE_ID = sha256:f51a445aa93ba2d8e526095b9cedfc621ea49e82a70dd726eaebfd0cdac3b901
```

该 identity 关系由本地 `docker save` archive 直接机械建立：OCI/index manifest digest 为 `b8ced...`，archive config digest 为 `f51a...`；树莓派 Docker Engine load 后 `.Id` 为该 config digest。此前 R3 的跨 Docker Engine `.Id` 相等假设属于 harness false-HOLD，不构成 product 或 transport defect。

## 3. Candidate activation / runtime-loaded proof

```text
CANDIDATE_IMAGE_REF = edge-mes-collector:a1-vp2-g5-6226bf3
CANDIDATE_CONTAINER_ID = 5b30fe755991eb64f594232767b1fd68d93b110ec86bcb9b53c10b874b254bc5
CANDIDATE_CONTAINER_IMAGE_ID = sha256:f51a445aa93ba2d8e526095b9cedfc621ea49e82a70dd726eaebfd0cdac3b901
CANDIDATE_CONTAINER_STARTED_AT = 2026-08-15T08:48:05.126654753Z
CANDIDATE_ACTIVATION_FENCE = 2026-08-15T08:48:05.126654753Z
CANDIDATE_COMMAND = ["python","-m","app.main"]
CANDIDATE_CONFIG_MOUNT = YES
FORWARD_LIFECYCLE_COUNT = 1
FORWARD_RC = 0
ROLLBACK_LIFECYCLE_COUNT = 0
ROLLBACK = NOT_ATTEMPTED
```

因此：

```text
DEPLOYED = YES
ACTIVATED = YES
RUNTIME_LOADED = YES
```

## 4. Protected runtime continuity

R4 runtime capture明确给出：

```text
REMOTE_RUNTIME_PROTECTED_CONTINUITY = PASS
DB_WRITES = 0
VPLC_ACTIONS = 0
PLC_ACTIONS = 0
POSTGRES_READ_ONLY_EVIDENCE_GROUP_COUNT = 1
READ_ONLY_SQL_RC = 0
```

本轮仅执行 Collector-only forward lifecycle；未触发 rollback。PostgreSQL 与 s7-plc-sim 在 activation 前、观察后及 SQL 后均按冻结 baseline 做 exact continuity comparison，并保持通过。

因此：

```text
PROTECTED_POSTGRES_CONTINUITY = PASS
PROTECTED_S7_VPLC_CONTINUITY = PASS
UNAUTHORIZED_PRODUCTION_STIMULUS = 0
DB_MUTATION = 0
```

## 5. WS02 accepted-skip proof

候选 activation fence：

```text
2026-08-15T08:48:05.126654753Z
= 2026-08-15 16:48:05.126654753 +08:00
```

WS02 accepted fact：

```text
station_id = WS02
cycle_counter = 112922
fact_id = 11701
production_result = skip
accepted_at = 2026-08-15T16:48:06.050876+08:00
source_event_id = sha256:124fdbb9b29c72abed3aec45d4690df3d4660c8606da611a175baef07f7ddbc6
```

`accepted_at` 严格晚于 candidate activation fence，约晚 0.924 秒。

Exact joined cycle：

```text
station_id = WS02
cycle_counter = 112922
result = SKIPPED
ack_status = ACK_OK
created_at = 2026-08-15T16:48:06.050876+08:00
updated_at = 2026-08-15T16:48:06.195520+08:00
plc_boot_id = 6266e5ac-d8aa-4e8b-b82e-32c9b87fe499
```

此处 `cycle_event.result = SKIPPED` 与冻结语义一致：cycle storage 使用 mapping code-table label；production accepted fact 必须使用 canonical `skip`。二者不是冲突。

同一 exact station/cycle 在 accepted fact 之后的 terminal adapter rejection aggregate：

```text
terminal_error_count_after_fact = 0
terminal_error_types_after_fact = []
terminal_adapter_error_codes_after_fact = []
terminal_adapter_dispositions_after_fact = []
latest_terminal_error_at_after_fact = null
```

结论：

```text
WS02_ACCEPTED_SKIP_POST_ACTIVATION = YES
WS02_EXACT_CYCLE_ACK_OK = YES
WS02_POST_ACCEPT_TERMINAL_ADAPTER_REJECTION = NO
```

## 6. WS03 accepted-skip proof

WS03 accepted fact：

```text
station_id = WS03
cycle_counter = 112922
fact_id = 11702
production_result = skip
accepted_at = 2026-08-15T16:48:06.205839+08:00
source_event_id = sha256:d8cc0224ec76ec7c864911e9f18cc1dda4fd0a0159fd5e9589304855d7bbcc84
```

`accepted_at` 严格晚于 candidate activation fence，约晚 1.079 秒。

Exact joined cycle：

```text
station_id = WS03
cycle_counter = 112922
result = SKIPPED
ack_status = ACK_OK
created_at = 2026-08-15T16:48:06.205839+08:00
updated_at = 2026-08-15T16:48:06.327279+08:00
plc_boot_id = 6266e5ac-d8aa-4e8b-b82e-32c9b87fe499
```

同一 exact station/cycle 在 accepted fact 之后的 terminal adapter rejection aggregate：

```text
terminal_error_count_after_fact = 0
terminal_error_types_after_fact = []
terminal_adapter_error_codes_after_fact = []
terminal_adapter_dispositions_after_fact = []
latest_terminal_error_at_after_fact = null
```

结论：

```text
WS03_ACCEPTED_SKIP_POST_ACTIVATION = YES
WS03_EXACT_CYCLE_ACK_OK = YES
WS03_POST_ACCEPT_TERMINAL_ADAPTER_REJECTION = NO
```

## 7. Runtime progression / freshness

90 秒自然观察后：

WS02：

```text
collector_state = RUNNING
last_cycle_counter = 112924
updated_at = 2026-08-15T16:49:35.595132+08:00
payload_ready = false
read_done = false
ack_timeout = false
last_error_code = null
last_error_message = null
```

WS03：

```text
collector_state = RUNNING
last_cycle_counter = 112923
updated_at = 2026-08-15T16:49:35.081867+08:00
payload_ready = false
read_done = false
ack_timeout = false
last_error_code = null
last_error_message = null
```

两站 runtime 均已从证明 cycle `112922` 向后继续推进，且 runtime row 在观察窗口末期保持 fresh、RUNNING、无 error、无 ack timeout。

当前 `read_done=false / payload_ready=false` 是后续实时状态，不否定 exact 112922 cycle 已在 `cycle_event.ack_status=ACK_OK` 建立完成 ACK 事实。

因此：

```text
RUNTIME_PROGRESSION_AFTER_REPAIR = YES
RUNTIME_FRESHNESS = PASS
ADAPTER_REJECTION_STARVATION_CLEARED_FOR_PROVEN_PATH = YES
```

## 8. event_ts / accepted_at interpretation

WS02/WS03 proof rows的 `event_ts` / `plc_end_time` 来自 V-PLC 原始 cycle 时间（2026-08-11），而 `accepted_at` / cycle DB creation 是本次 candidate activation 后的 2026-08-15 fresh time。

本 Goal 禁止人工 VPLC/PLC stimulus，因此 Final Verification 需要证明的是：**新 Collector candidate 在 activation 后自然读取并接受了此前因 vocabulary defect 被拒绝的 code-3 cycle，并生成 canonical production fact / ACK**。fresh acceptance 由 `accepted_at` 与 activation fence 建立；不要求修改 PLC 原始 event timestamp。

因此原始 event timestamp 较旧不构成本 repair-path production proof blocker。

## 9. Final verdict

证据链完整：

```text
published commit 6226bf3
→ committed-byte arm64 candidate image
→ exact transported image identity established
→ Collector-only activation successful
→ candidate runtime loaded
→ WS02/112922 accepted canonical skip post-activation
→ WS02 exact cycle SKIPPED / ACK_OK
→ WS03/112922 accepted canonical skip post-activation
→ WS03 exact cycle SKIPPED / ACK_OK
→ zero same-cycle terminal adapter rejection after accepted facts
→ WS02/WS03 runtime continues beyond 112922
→ protected services continuous
→ DB/VPLC/PLC mutation zero
```

Final state：

```text
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

Terminal：

```text
PASS / A1_VP2_G5_RUNTIME_DEPLOYMENT_EVIDENCE_SPLIT_VERIFIED
```

## 10. Boundary statement

本 PASS 只接受 `A1 VP2-G5` 的已批准最小修复路径，即 `result code 3 / SKIPPED` vocabulary canonicalization defect 已在真实远端 runtime 中关闭。

它不自动证明：

- 所有 station/result vocabulary 全面生产接受；
- UI/Trusted Station Summary 已修复；
- API data service configuration 已完成；
- A1-S2 已授权；
- Owner Visual Acceptance 已完成；
- 整个 Edge MES 已达到最终 MVP/production completion。
