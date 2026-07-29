# Sprint 4 D2-R7B-I1 R32-R5-R2 Single-Process SSH JSON Capture and Machine Reconciliation

## 报告身份

- 任务：D2-R7B-I1 R32-R5-R2 — Capture One Remote Docker Inspect Payload Directly into the Same Local Process and Complete the RootFS Machine Reconciliation
- 执行 Thread：Architecture / Integration
- Authority：`PM-D2-R7B-I1-R32-R5-R2-SINGLE-PROCESS-SSH-JSON-MACHINE-RECONCILIATION-260729-1759`
- Delivery mode：`REPOSITORY_REPORT_WITH_ARTIFACTS`
- 结论：`PASS`
- Terminal classification：`REMOTE_LOADED_OBJECT_CONTENT_RECONCILED`

## Scope and process boundary

本任务仅创建本报告及三个授权 artifact。唯一的 `/Users/chenjie/Documents/MES/edge-mes-demo/.venv/bin/python` 本地 comparison process（PID `95912`）以一次 invocation 在内存中依序完成 archive streaming parse、local terminal write、唯一 SSH stdout bytes capture、strict UTF-8 decode、strict JSON parse、schema validation、direct Config/Env/RootFS machine comparison 和 remote terminal write。没有 raw SSH stdout file、temporary helper、第二个 comparison process、manual transcription、Docker/Compose lifecycle、remote filesystem mutation、tag mutation 或 Git mutation。

## Local canonical archive prerequisite

archive identity：`54313984` bytes，SHA-256 `b0fc3d6e4c511cfc1782d5ce15ef3d9cd053ce99a3571622daf165422d65ce2e`。OCI manifest digest 是 `sha256:899082388afebab65844cbc0e49fb69a0f19f8bf23c3c4c989f6533f2f2ce401`；OCI config digest（也是 expected remote Docker object ID）是 `sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734`。Canonical config 为 linux/arm64、Created `2026-07-29T15:43:02.675492291+08:00`、Cmd `['python', '-m', 'app.main']`、WorkingDir `/app`、Env count `5`、RootFS count `9`，且九项 digest format 均有效。

## SSH capture and direct reconciliation

SSH return code：`0`；stdout：`11688` bytes / `088b142f82badde45e0e274b334a3d2a5db3340827b92c2e898fb07bb90ea887`；stderr：`0` bytes / `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。Captured stdout was decoded with strict UTF-8 and parsed directly with `json.loads`; no displayed or copied array was used as comparison input.

Remote object ID、platform、Created、Cmd、WorkingDir、ordered Env and ordered RootFS results are fully persisted in `docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/remote_reconciliation_terminal.json`. RootFS comparison has canonical/remote count `9` / `9`, ordered equality `True`, mismatch indices `[]` and mismatch count `0`.

## Tag state and non-actions

Descriptive tag must resolve to `sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734`; compatibility tag must remain `sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a`; known-bad `sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c` must not own the descriptive tag. Full structured inspect results and zero mutation counters are persisted in the remote terminal artifact. This evidence establishes at most `IMAGE_LOADED_EXACT`; it does not establish activation eligibility, activation, runtime load or production acceptance.

## Durable artifacts

| Path | Bytes | SHA-256 | Role |
| --- | ---: | --- | --- |
| `docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/local_prerequisite_terminal.json` | 8415 | `98e1dce7ba947e99b7c9e81ce3ac3431cc951abe4f8c0b3d104adf48e25cbd5d` | local canonical archive prerequisite |
| `docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/remote_reconciliation_terminal.json` | 32190 | `629dfda5d8c1b8e1096ccbc64625154c3778d80d239522bdb0652295c3586997` | same-process SSH capture and machine comparison |
| `docs/reports/evidence/d2_r7b_i1_r32_r5_r2_single_process_ssh_json_capture_machine_reconciliation/manifest.sha256` | computed after report | `computed after report` | self-excluded three-entry manifest |

## MVP 路径一致性

- 是否直接服务批准 MVP：yes。
- minimum invariant：archive canonical config and directly captured remote Docker object fields must be machine-compared without manual transcription before an exact loaded-image claim.
- 是否扩大产品能力、威胁模型、证据平台或基础设施：no。
- 是否 task inflation：no；本轮只关闭 RootFS false-PASS risk。
- classification：`MVP-ALIGNED`。

## Next gate

唯一 next gate：`R32-R5-R2 single-process SSH JSON machine reconciliation → ChatGPT PM durable intake`。本报告仅为 `WRITTEN`；未授权 activation preflight、tag mutation、Collector lifecycle、runtime validation、rollback、cleanup 或 Git closeout。

## Thread 输出 / 上下文评估

- 输出长度：中；机器可读完整证据位于两份 terminal JSON。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：唯一 SSH budget 已消耗，后续任何不同 scope 都需要新的 authority。
