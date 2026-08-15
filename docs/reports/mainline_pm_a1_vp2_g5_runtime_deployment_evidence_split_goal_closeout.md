# Mainline PM Closeout — A1 VP2-G5 Runtime Deployment + Evidence Split

结论：**PASS / A1_VP2_G5_RUNTIME_DEPLOYMENT_EVIDENCE_SPLIT_COMPLETE**

## 1. Accepted product/runtime state

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

## 2. Final runtime result

```text
RESULT_PATH = docs/reports/mainline_pm_a1_vp2_g5_runtime_deployment_evidence_split_owner_runtime_result_r4.txt
RESULT_BYTES = 5658
RESULT_SHA256 = ff4c4489e58c0b37abba952d94ec2cf8766da4f27157133c6c26ba124d38f4fe
RUNNER_TERMINAL = PASS / DEPLOYMENT_AND_EVIDENCE_CAPTURE_COMPLETE
REMOTE_STATE = STABLE
```

Candidate：

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

## 3. Production proof

WS02：

```text
cycle = 112922
production_result = skip
accepted_at = 2026-08-15T16:48:06.050876+08:00
cycle_event.result = SKIPPED
ack_status = ACK_OK
terminal adapter rejection after fact = 0
runtime last_cycle_counter after observation = 112924
```

WS03：

```text
cycle = 112922
production_result = skip
accepted_at = 2026-08-15T16:48:06.205839+08:00
cycle_event.result = SKIPPED
ack_status = ACK_OK
terminal adapter rejection after fact = 0
runtime last_cycle_counter after observation = 112923
```

因此 accepted exact cause chain 已在远端真实 runtime 中关闭：

```text
V-PLC result code 3
→ mapping SKIPPED
→ repaired runtime source canonicalizes to skip
→ adapter accepts
→ production fact = skip
→ cycle persisted = SKIPPED
→ ACK_OK
→ runtime continues
```

## 4. Historical recovery record

此前所有 HOLD 均保持历史事实，不重写：

1. R1 Reliability：`HOLD / RESULT_SINK_FOREIGN_OBJECT_OVERWRITE_RACE`。
2. 首次 PM-direct runner：本地 Docker Go-template quoting defect，停在 SSH 前。
3. successor：runtime SSH 参数中的 `|` 被远端 shell 解释，停在 lifecycle 前。
4. R2 continuation：projection string mismatch，停在 lifecycle 前。
5. R3 fieldwise：暴露 Docker Desktop/containerd manifest identity 与 Raspberry Pi Docker Engine config identity 差异，停在 lifecycle 前。
6. R4 transport-bound：以 archive manifest/config identity 正确绑定后，完成唯一 Collector forward activation 与 production evidence capture。

这些 HOLD 均未否定 product repair；它们属于 harness/control-plane recovery。最终 R4 没有 rebuild、没有重复 image load，没有 DB/VPLC/PLC mutation。

## 5. Final Verification

```text
FINAL_VERIFICATION_REPORT = docs/reports/mainline_pm_a1_vp2_g5_runtime_deployment_evidence_split_final_verification.md
FINAL_VERIFICATION_ACCEPTED = YES
FINAL_VERIFICATION_TERMINAL = PASS / A1_VP2_G5_RUNTIME_DEPLOYMENT_EVIDENCE_SPLIT_VERIFIED
```

## 6. Goal closeout

```text
GOAL_STATUS = COMPLETE
SHADOW_PM_STOP = YES
PUBLISHED_COMMIT_STILL_HEAD_ORIGIN = YES
OWNER_RUNTIME_TRANSACTION_EXECUTED = YES
DEPLOYMENT_EVIDENCE_CAPTURED = YES
FINAL_VERIFICATION_ACCEPTED = YES
DEPLOYED = YES
RUNTIME_LOADED = YES
REMOTE_VERIFIED = YES
WS02_ACCEPTED_SKIP_POST_ACTIVATION = YES
WS03_ACCEPTED_SKIP_POST_ACTIVATION = YES
PRODUCTION_ACCEPTED_FOR_THIS_REPAIR_PATH = YES
A1_VP2_G5_ACCEPTED = YES
OWNER_VISUAL_ACCEPTED = NO
A1_S2 = NOT_AUTHORIZED
GOAL_TERMINAL = PASS / A1_VP2_G5_RUNTIME_DEPLOYMENT_EVIDENCE_SPLIT_COMPLETE
NEXT_ACTION = RETURN_TO_MAINLINE_PM / DATA_FIRST_NEXT_GATE
```

本 closeout 不授权新的产品、远端、Git 或 UI mutation。下一步由 Mainline PM 根据数据优先路线选择后续 gate。
