# Sprint 4 D2-R7B-I1 R27-R1 Mutation Helper JSON Contract Repair

## 1. 报告身份与边界

- 任务：D2-R7B-I1 R27-R1 Mutation Helper JSON Contract Repair
- 线程：Architecture / Integration
- Authority ID：PM-R27-R1-260728-0856
- 授权范围：一次性、本地实现与验证
- 当前结论：PASS（本地 contract repair 完成）
- 远端动作：未执行 SSH、upload、deploy、cleanup、restart、activation 或任何远端 mutation
- Git 动作：未 stage、未 commit、未 push、未 tag
- 本报告不把本地 PASS、synthetic fake-SSH PASS 或历史 R26 证据升级为当前远端事实

## 2. Fresh baseline

工作树：

- Git root：/Users/chenjie/Documents/MES/edge-mes-demo
- branch：main
- HEAD：8de5edbb504538a233abbcc80102cb714c9cee65
- origin/main：8de5edbb504538a233abbcc80102cb714c9cee65
- ahead/behind：0/0
- cached changes：空
- git diff --check：PASS
- config/mapping.yaml：clean

Fresh baseline 中已有的 tracked dirty 文件只有：

1. .gitignore
2. docs/current_status.md
3. docs/thread_handoff/pm_operating_rules.md

另有 203 个既有 untracked report/evidence/frontend artifacts；它们属于本次基线中已存在的 external/known artifacts，本任务没有清理、覆盖、重命名或扩大 allowlist。

## 3. 任务文件初始身份

以下 SHA-256 为本地实现前的读取结果：

| 文件 | bytes | 初始 SHA-256 |
|---|---:|---|
| docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py | 10203 | b439a071ceb898f81689331fcba61a87e7825cbd418f899e34c072d599de3ee3 |
| docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py | 13887 | 0faafc3e134a0b7314e0b36238cc687a686304a6ab6c12cf07e371e0ec90937d |
| docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py | 57998 | 71d31523518ef0686fc28cba82f7fe969d8cfc3ecaecb6578bb58e8152508969 |
| docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256 | 528 | 62c4a1d939cc377ead65c9c76e83fea762a2b0fd8d7f2af9e0e1258f2c2cc8d |
| docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py | 81566 | 465c83b02110e39c9fe4d7e5626a083256d3ed8bc86d9d44cf4f942d844b2b09 |
| docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256 | 1122 | 42bf24b9ddd338624ca7e81bad9a924ca0a40c179071cbaa4c6fc1848f37dd90 |

受保护文件 docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py 的初始身份为：

- bytes：45783
- SHA-256：eea3e8778cc94c78a0931b2404f888a78176996cd1a4421a7442667c8b859085

## 4. R26 历史证据边界

R26 evidence 仅作为历史 retained evidence 保留，不作为本次当前远端状态：

| 文件 | bytes | SHA-256 |
|---|---:|---|
| docs/reports/sprint4_d2_r7b_i1_r26_exact_config_only_remote_execution.md | 10314 | dd25adf90cd4c11f3e2611321b3ed4642785021c81e859f31b229f082936f3b2 |
| docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/raw_terminal.ndjson | 12872 | 4799fc7e9cf27212cd9f696afa40f24c48cf69320bf0700b3ee39b5e7c5be600 |
| docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/final_terminal.json | 12872 | 4799fc7e9cf27212cd9f696afa40f24c48cf69320bf0700b3ee39b5e7c5be600 |
| docs/reports/evidence/d2_r7b_i1_r26_exact_config_only_remote_execution/manifest.sha256 | 453 | 257fb2945155d49e40638ea1dfedd4cc95aee127dca6a38fc7d72a8e8f362670 |

R26 retained temp stage：

- /private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r2.0mW7V5
- stage root：regular directory，owner chenjie，mode 0700
- mapping file：regular non-symlink，owner chenjie，mode 0600，bytes 7112
- mapping SHA-256：d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
- cleanup：未执行；parent directory 保留

## 5. Root cause and RED evidence

两个 persisted mutation helper 的内部文件操作已经能够形成验证所需的身份与 digest 数据，但成功路径的 persisted main() 仍输出 legacy plain text，无法满足严格的 machine-readable JSON success contract。问题边界是 helper output contract，不涉及 orchestrator。

修复前按 TDD 先加入 T36/T37 并执行 RED：

- T36：FAIL；returncode=0；stderr 为空；upload stdout 为 legacy plain text；JSONDecodeError
- T37：FAIL；returncode=0；stderr 为空；deploy stdout 为 legacy plain text；JSONDecodeError
- RED matrix：FAIL，37/37

该 RED 结果证明测试实际调用 persisted helper main() 并解析 stdout，而不是只检查静态字符串。

## 6. 实现修复

### remote_upload_exclusive.py

- 增加 stdlib json
- upload() 成功结果保留并返回 path、realpath、bytes、sha256、device、inode、owner、group、mode
- persisted main() 成功时只输出一行 compact、sorted JSON，并以 newline 结束
- 顶层字段包含 status=PASS、phase=REMOTE_UPLOAD 以及上传身份字段
- failure return code 与 stderr contract 保持不变

### remote_deploy.py

- 增加 stdlib json
- 成功路径捕获已验证 upload 的 size、digest、device/inode/owner/group/mode
- 捕获 atomic replace 前的 upload realpath
- 返回 canonical nested object，顶层字段严格为 status、phase、operation、source_upload_temp、target、backup
- source_upload_temp.state=CONSUMED_BY_ATOMIC_REPLACE
- target 同时记录 inode_before 与 inode_after
- persisted main() 成功时只输出一行 compact、sorted JSON，并以 newline 结束
- failure return code 与 stderr contract 保持不变

### orchestrator boundary

docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py 未修改；最终复核仍为：

- bytes：45783
- SHA-256：eea3e8778cc94c78a0931b2404f888a78176996cd1a4421a7442667c8b859085
- identity：UNCHANGED PASS

## 7. P2-R2 contract verification

test_d2_r7b_contract.py 覆盖 T1-T37。新增 T36/T37 均执行 persisted helper main()，使用真实 stdin payload，要求：

- returncode=0
- stderr 为空
- stdout 可被 JSON 解析为 object
- stdout 只有一条 JSON line
- upload success contract 为 canonical fields
- deploy success contract 为 canonical nested fields
- deploy target inode_before 与 inode_after 存在且不同
- source upload temp 明确为 CONSUMED_BY_ATOMIC_REPLACE

最终结果：

- SOURCE_BYTE_COMPILE：PASS，8/8
- T1-T37 matrix：PASS，37/37
- test process exit：0

## 8. P2-R3 execution verification

test_d2_r7b_execution_contract.py 的 fake SSH path 已改为调用实际 persisted helper main()，不再用 synthetic success wrapper。它覆盖：

- success stdout JSON contract
- empty stdout
- legacy plain text
- malformed JSON
- multiple JSON lines
- JSON list
- JSON scalar
- valid object plus trailing text
- upload helper failure
- deploy helper failure
- deploy command failure

新增 E41-E45 对直接 helper invocation 的 failure contract 做了补强，包括 invalid upload payload、deploy 删除 upload temp 后的 helper failure、deploy 特殊 command failure 传播及 no second mutation call 约束。

最终结果：

- E1-E45：PASS，45/45
- test process exit：0
- fake SSH 仅为本地 synthetic execution evidence，不是远端事实

## 9. Manifest and bytecode verification

P2-R2 manifest 最终为 6/6：

- local_materialization：OK
- deploy：657498d42906c260ad12d53c16044a6a272cd1bea1a60ebfd2538b178baf02ff
- preflight：OK
- rollback：OK
- upload：30a02e5bc63545b08b1536e59abc418685cf846fbe2c930847d1f1b983f5ae7b
- test：aa40fa64d8d9cc8508a6e0c480714778381bb2e13c21ffa14bd553205f3e9183

P2-R3 manifest 最终为 9/9；本任务相关 entries 为：

- deploy：657498d42906c260ad12d53c16044a6a272cd1bea1a60ebfd2538b178baf02ff
- upload：30a02e5bc63545b08b1536e59abc418685cf846fbe2c930847d1f1b983f5ae7b
- P2-R2 test：aa40fa64d8d9cc8508a6e0c480714778381bb2e13c21ffa14bd553205f3e9183
- P2-R3 test：d1dc0962995686b171cef0b134036ee5fbe24f3b8055b02b68d1fa5e68a871f5

Manifest identities：

- docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256：bytes 528，SHA-256 2ae13bd6dc17167f98d2d59efd882e8a568d5c0ae6f36cbbb9ecb6f2d21086dd
- docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256：bytes 1122，SHA-256 18edbdc940d1eaef4edbc9dc831dee38716704194b05b564dfc8fb1a6da24714

最终 evidence tree cache audit：

- __pycache__：0
- *.pyc：0

## 10. Final changed-file identities

本次只允许新增或修改以下 7 个文件：

| 文件 | bytes | 最终 SHA-256 |
|---|---:|---|
| docs/reports/evidence/d2_r7b_p2_r2/remote_upload_exclusive.py | 10563 | 30a02e5bc63545b08b1536e59abc418685cf846fbe2c930847d1f1b983f5ae7b |
| docs/reports/evidence/d2_r7b_p2_r2/remote_deploy.py | 15483 | 657498d42906c260ad12d53c16044a6a272cd1bea1a60ebfd2538b178baf02ff |
| docs/reports/evidence/d2_r7b_p2_r2/test_d2_r7b_contract.py | 67695 | aa40fa64d8d9cc8508a6e0c480714778381bb2e13c21ffa14bd553205f3e9183 |
| docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256 | 528 | 2ae13bd6dc17167f98d2d59efd882e8a568d5c0ae6f36cbbb9ecb6f2d21086dd |
| docs/reports/evidence/d2_r7b_p2_r3/test_d2_r7b_execution_contract.py | 89604 | d1dc0962995686b171cef0b134036ee5fbe24f3b8055b02b68d1fa5e68a871f5 |
| docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256 | 1122 | 18edbdc940d1eaef4edbc9dc831dee38716704194b05b564dfc8fb1a6da24714 |
| docs/reports/sprint4_d2_r7b_i1_r27_r1_mutation_helper_json_contract_repair.md | pending final readback |

## 11. Final audit and handoff

- exact task artifact allowlist：仅上述 6 evidence files 加本报告
- remote_i1_orchestrator.py：unchanged
- R26 retained evidence/stage：未触碰
- task-owned process：无
- cached Git paths：无
- git diff --check：PASS
- remote mutation：未执行，当前远端状态不作判断

当前交付是 local implementation and contract verification PASS。它只证明本地 persisted helper、fake SSH execution contract、manifest closure 和 source-byte/cache hygiene 满足本任务约束；不代表 Reliability gate、Verification gate、remote eligibility、deployment、activation 或 production acceptance 已通过。

下一 gate：PM durable intake / handoff。后续若需要 Reliability、Verification 或 remote execution，必须按各自 authority 与 call-budget 重新开启，不得由本报告继承授权。报告自身的 bytes 与 SHA-256 应由 PM intake 在读取后再次记录，本报告不对自身预先自引用 hash。
