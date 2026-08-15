# Sprint 4 D2-R7B-I1 R30-I1-R10 Existing-Image Controlled Collector Restart and Runtime Config Reload Validation

## 结论

~~~
status: HOLD
conclusion: RUNTIME_RELOAD_HOLD
classification: PROCESS_GATE_UNAVAILABLE / PRE_CONTROLLER_CACHE_DRIFT
phase: PRE_CONTROLLER_LOCAL_GATE
delivery: WRITTEN
~~~

本轮在本地 controller/static/network 前置门禁停止。未创建 runtime_controller.py，未执行 controller，未启动 SSH，未观察远端，未执行 Collector restart、rollback 或 recovery restart。

本报告不能建立以下 claim：

~~~
EXISTING_IMAGE_RUNTIME_CONFIG_LOADED
PACKAGE_CLOSED_NEW_COLLECTOR_ACTIVATED
ACCEPTED_FACT_RUNTIME_ACTIVE
PRODUCTION-ACCEPTED
~~~

## Authority and scope

~~~
authority: PM-R30-I1-R10-260729-CONTROLLED-RUNTIME-RELOAD-01
execution thread: fresh replacement Architecture / Integration task
checkout: /Users/chenjie/Documents/MES/edge-mes-demo
report delivery mode: REPOSITORY_REPORT_WITH_ARTIFACTS
~~~

附件规定的 30 项材料已按序读取，PM Rules Section 10、11、12、13 已在 fresh recovery 前二次读取。授权范围仅包括 exact R10 report、四个 exact artifacts、一次 persisted controller/SSH 及受限 Collector restart/recovery；本轮因本地门禁失败，后续权限未消费。

Existing-image boundary remains unchanged：即使未来独立授权并通过，最多只能建立 existing safe image 读取 exact new mapping 的 claim；不得推导 package-closed new Collector activation、accepted-fact runtime active 或 production acceptance。

## Fresh local baseline

~~~
pwd: /Users/chenjie/Documents/MES/edge-mes-demo
branch: main
HEAD: 1fac3ee567f1108e5a18b155e4133e1fecd50246
origin/main: 1fac3ee567f1108e5a18b155e4133e1fecd50246
HEAD^: 63d3cc70e787e0c837079aec0f5924dcbfa6a668
ahead/behind: 0/0
cached: empty
~~~

Tracked dirty set 在本轮开始时精确为 6 项，未修改：

~~~
.gitignore
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
docs/thread_handoff/pm_operating_rules.md
~~~

Initial untracked set：

~~~
count: 13780
sorted NUL-delimited SHA-256: b369a85075747fdc964753be4edfb6ac3b4c076e30b126ebcf837276153f117c
~~~

## Exact output collision gate

在创建 artifact parent 前 fresh lstat 确认以下路径均为 ABSENT；无 symlink、overwrite 或 alternative output path。随后仅创建了 exact artifact parent 目录和本报告，未创建四个 evidence artifact。

~~~
docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_controlled_collector_restart_runtime_validation.md: ABSENT before write
docs/reports/evidence/d2_r7b_i1_r30_i1_r10_controlled_collector_restart_runtime_validation: ABSENT before write
docs/reports/evidence/d2_r7b_i1_r30_i1_r10_controlled_collector_restart_runtime_validation/runtime_controller.py: ABSENT
docs/reports/evidence/d2_r7b_i1_r30_i1_r10_controlled_collector_restart_runtime_validation/raw_terminal.ndjson: ABSENT
docs/reports/evidence/d2_r7b_i1_r30_i1_r10_controlled_collector_restart_runtime_validation/final_terminal.json: ABSENT
docs/reports/evidence/d2_r7b_i1_r30_i1_r10_controlled_collector_restart_runtime_validation/manifest.sha256: ABSENT
~~~

## Existing evidence and source identities

这些 identity 仅证明本地文件状态和历史 evidence identity，不替代本轮远端或 runtime evidence。

~~~
R9 report: 17260 bytes, a7542bd7ee7459f56c6671a03198a44245c22aa639a3207b3758cd8676f2ba91
R8 report: 8429 bytes, 0c1cc78b0a24c9e80ef3ac4538efa8391ff501154b9d18439fa01004679da0ff
R8 raw: 13025 bytes, f2baa8ca164341286411efea601f94fa4c8d636f2a8ae9c10cbcf2701decf5b0
R8 final: 13025 bytes, f2baa8ca164341286411efea601f94fa4c8d636f2a8ae9c10cbcf2701decf5b0
R8 manifest: 498 bytes, d60c0bbe99821a629df2137c365b3f6c1d494fdcb58dfcba150020f7dee95658; 3/3 OK
rollback helper: 13248 bytes, e2690ef991827ad8107430ee0449be913afa65dbf166fe2c1cf19fec0b7736ff
config/mapping.yaml: 7112 bytes, d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
~~~

Current local runtime-semantic source identities：

~~~
collector/app/main.py: 2073 bytes, a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090
collector/app/config.py: 764 bytes, 4f01689a34fb494f7ea84cf74b303ce8aed0957d1dd9c05fc7773563cd577afc
collector/app/plc/mapping.py: 17433 bytes, c834c43b2bbb4cf8a20a2119053dbcd2970260d7e9a87d4fced995e73c13a098
collector/app/services/event_collector.py: 16342 bytes, eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f
collector/app/services/resolved_config_registry.py: 17337 bytes, 1844449a3f99e9ca53bddc8063c151fb0f889920597bccb170f5e62f3715db2c
~~~

P2-R2/P2-R3 historical manifests were read as 6/6 OK and 9/9 OK respectively. They are historical local evidence only and do not authorize R10 execution.

## Blocking local gates

### Process gate

本机没有 /proc。按本轮指令改用 bounded /usr/bin/pgrep -af 对以下四个 token 做只读扫描，并排除 scanner、direct parent 与 pgrep child：

~~~
runtime_controller.py
R30-I1-R10
edge-mes-collector
remote_rollback.py
~~~

四次调用均无法取得进程列表：

~~~
PROCESS_COUNT: 0 (not authoritative)
PROCESS_SCAN_ERRORS: 4
each returncode: 3
stderr: sysmon request failed with error: sysmond service not found
        pgrep: Cannot get process list
~~~

因此 PROCESS_COUNT=0 不被解释为无进程；进程 gate 是 UNAVAILABLE，必须 fail closed。未启动 controller，因此没有 task-owned process 可 reap，也没有任何远端进程证据。

### Cache gate

fresh read-only scan of collector observed 41 cache entries（__pycache__ directories and *.pyc files），而附件要求 P2-R2/P2-R3 scoped cache 均为 0。未执行 cleanup、删除、覆盖或 bytecode repair；cache attribution remains NOT_ESTABLISHED。

### Stage roots

两个 historical stage roots 均保持 regular non-symlink directory、uid 501、mode 0700；其 config/mapping.yaml 均为 7112 bytes、SHA-256 d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d。本轮未复用、未清理、未修改 stage roots。

## SSH identity and network boundary

仅执行 local-only key metadata 与 ssh -G -F /dev/null 解析，未读取、hash、copy、print 或 persist private-key contents：

~~~
key: /Users/chenjie/.ssh/edge_pi_codex
regular: true
symlink: false
uid: 501
mode: 0600
resolved hostname: 10.0.0.217
resolved user: mari
resolved port: 22
resolved identityfile: /Users/chenjie/.ssh/edge_pi_codex
proxycommand: none
proxyjump: none
SSH parent count: 0
network calls: 0
~~~

## Controller, remote state, and lifecycle

~~~
runtime_controller.py: NOT CREATED
controller static gate: NOT RUN / N/A
embedded rollback identity: NOT EMBEDDED / N/A
remote preflight: NOT_OBSERVED
pre-restart compatibility probe: NOT RUN
normal restart count: 0
rollback count: 0
recovery restart count: 0
retry count: 0
resume count: 0
~~~

因此以下字段必须保持 NOT_OBSERVED，不能由历史 R8/R9 evidence 继承：target、backup、sidecars、Collector container/image/StartedAt/RestartCount/mount、active-image source profile、protected service tuples、post-restart samples、logs、post-probe。

raw_terminal.ndjson、final_terminal.json、manifest.sha256 均未创建；不存在 terminal candidate，也不存在可安全建立的 final-terminal binding。

## Prohibited-action audit

本轮确认未执行：

~~~
controller execution: 0
SSH: 0
Docker/Compose: 0
Collector restart: 0
rollback/recovery: 0
image build/transport/load/pull/retag: 0
DB/API/PLC/Simulator calls: 0
pytest/P2 tests: 0
source/config/Compose edits: 0
Git stage/commit/push/tag/reset/restore/checkout/stash/clean: 0
manual cleanup: 0
private-key content access: 0
~~~

## Final local state and delivery

除 exact report 和其授权 parent directory 外，没有本轮有意创建的路径。报告写入后，四个 evidence artifact 仍为 ABSENT；cached index、HEAD、origin/main、ahead/behind 与 tracked dirty set 未改变。最终 untracked set 为 13781，sorted NUL-delimited SHA-256 为 595f85aa114743b85797a625b7147e2ef4cea3862637c58baabb33312335784e（仅比 initial set 多本报告一项）；本轮未执行 Git mutation。

Evidence classification：LOCAL_PRE_CONTROLLER_HOLD_ONLY。本报告是 durable HOLD 记录，不是 remote execution terminal、runtime reload proof 或 product acceptance。

## Blockers and recommendation

Blockers：

1. bounded process enumeration unavailable: /proc absent and pgrep returned Cannot get process list for all four required tokens.
2. scoped local cache gate observed 41 entries instead of required 0；no attribution or cleanup is authorized in this task.

唯一下一步是 ChatGPT PM durable intake of this exact HOLD。不得在本 Thread retry、resume、请求 elevation、手工执行 SSH、清理 cache/stage roots 或补做 controller/network。

## MVP alignment and non-inheritance

~~~
classification: MVP-ALIGNED WITH BACKLOG ITEMS
approved deliverable: existing safe-image config reload
new image activation: no
production acceptance: no
task inflation: no
~~~

本 HOLD 不继承、也不授权 new image deployment/build/transport/retag/recreate、accepted-fact validation、production acceptance、cleanup 或 Git closeout。下一次若要继续，必须由 PM 提供新的独立 authority，并先解决 process enumeration 与 cache gate。

~~~
current Thread continue: no
next Thread: yes, only under fresh PM authority
next gate: ChatGPT PM durable intake only
~~~
