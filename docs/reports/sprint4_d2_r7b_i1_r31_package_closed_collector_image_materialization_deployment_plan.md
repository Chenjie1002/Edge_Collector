# Sprint 4 D2-R7B-I1 R31 Package-Closed Collector Image Materialization and Deployment Planning

## 1. 报告身份

报告名称：
Sprint 4 D2-R7B-I1 R31 Package-Closed Collector Image Materialization and Deployment Planning

任务名称：
D2-R7B-I1 R31 — Plan the Smallest Bounded Materialization, Transport, Collector-Only Activation and Rollback Gate for a Fresh Package-Closed Collector Image

执行 Thread：
Architecture / Integration

Authority source / ID：
PM-D2-R7B-I1-R31-PACKAGE-CLOSED-IMAGE-PLAN-260729-1435

Report delivery mode：
REPOSITORY_DURABLE_REPORT

Exact report path：
docs/reports/sprint4_d2_r7b_i1_r31_package_closed_collector_image_materialization_deployment_plan.md

本报告只建立 future image materialization、transport/load、Collector-only activation、rollback 和 evidence 的 bounded plan。它不执行或授权 image build、archive、transport、load、tag、restart、recreate、activation、rollback、runtime-loaded validation、production validation 或 Git action。

## 2. 结论

PASS WITH RECOMMENDATIONS

Blockers：none。

Selected mechanism：

A — local arm64 build → local isolated validation → exact image ID → docker save archive → bounded transport → remote docker load → remote exact image-ID verification → later Collector-only activation

Recommended future task split：

先以一个新 PM authority 完成 Phase 1 + Phase 2，其中 Phase 2 仅完成 bounded archive/transport/load 和 exact remote image identity verification，不触碰任何 container lifecycle；完成 durable intake 后，再以新的 PM authority 执行 Phase 3–6，并把 Phase 6 仅作为预定义 terminal failure 的 conditional rollback phase。Phase 7 永远另开为后续 production accepted-fact persistence gate。

选择 A 的理由：当前 committed Dockerfile、Compose root context、package-closure test 和独立 Verification 已证明本地 arm64 package-closed materialization 机制成立；此前的 6e064... 只证明过本地验证 image，已由所属 Verification 删除，不能直接使用，但它证明了这条本地闭环的历史可执行性。A 把 build reproducibility、image identity 和 runtime-host build 负担分开，远端只需要受限的 archive load，不需要远端重新解释 source package 或依赖远端 build network。当前事实没有证明 A 不安全、不闭合或不可执行，因此不选择 B 作为主路径。

## 3. Fresh local recovery and report precondition

### 3.1 Live Git facts

本轮在真实 checkout /Users/chenjie/Documents/MES/edge-mes-demo 执行了用户指定的 read-only recovery。结果：

| Field | Live fact |
| --- | --- |
| pwd | /Users/chenjie/Documents/MES/edge-mes-demo |
| branch | main |
| HEAD | ca68dd4a4913238fc62e9621f1ac632c709a3149 |
| origin/main | ca68dd4a4913238fc62e9621f1ac632c709a3149 |
| HEAD^ | 1fac3ee567f1108e5a18b155e4133e1fecd50246 |
| ahead / behind | 0 / 0 |
| cached index | empty |
| git diff --check | PASS |
| git diff --cached --check | PASS |

最近八个 committed entries：

~~~text
ca68dd4 (HEAD -> main, origin/main, origin/HEAD) Add PM handoff before Collector activation
1fac3ee Add PM handoff after R30 reliability cleanup holds
63d3cc7 Close D2-R7B R29 observation and cleanup documentation
5fe7228 Close D2-R7B R27 local contract gate
8de5edb Sync D2-R7A closeout governance status
34d625c Add PM handoff after D2-R7A closeout
ddf55be Close D2-R7A collector package closure gate
58e6c7e Add PM handoff before D2-R7A verification
~~~

Tracked dirty set 与 prompt 预期完全一致，且均为 pre-existing external dirty artifacts：

~~~text
.gitignore
docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh
docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256
docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py
docs/thread_handoff/pm_operating_rules.md
~~~

本任务没有读取、修改、恢复、格式化、清理、stage 或纳入上述路径。大量 pre-existing untracked reports、evidence、handoffs、frontend dependencies/build output 和其他 external artifacts 只作为排除边界处理；repository-wide untracked count、aggregate path digest 和 cache 不作为本 planning blocker。

### 3.2 Exact report precondition

写入前检查结果：

~~~text
report path: ABSENT
symlink: NO / NON-SYMLINK precondition satisfied by absence
index: UNSTAGED
~~~

唯一允许写入的路径是本报告 exact path。没有创建 artifact、helper、manifest、status、roadmap、handoff 或 source 文件。

### 3.3 Required identity audit

以下 identity 均由 live bytes 和 shasum -a 256 重新核验：

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| docs/thread_handoff/chatgpt_pm_handoff_260729-1417.md | 26632 | 281ccbf21dffe6657d700a101d3069786a6ab48fa105e4bc3757d66abe971e05 |
| docs/reports/sprint4_d2_r7a_r4_r1_collector_package_closure_reverification.md | 16293 | aebf3c38a366e5ef4d1abcbccffba03b9245fc8da026b4bc45278cd5b50451d5 |
| docs/reports/sprint4_d2_r6_r1_new_collector_remote_config_static_compatibility_retry.md | 19443 | 4b0942a624de4ec8bb9e2f360484e6c35165bf14136eb628c7927d66b9bcec86 |
| docs/reports/sprint4_d2_r7b_i1_r30_i1_r8_one_shot_exact_config_only_remote_execution.md | 8429 | 0c1cc78b0a24c9e80ef3ac4538efa8391ff501154b9d18439fa01004679da0ff |
| docs/reports/sprint4_d2_r7b_i1_r30_i1_r9_focused_reliability_final_rereview.md | 17260 | a7542bd7ee7459f56c6671a03198a44245c22aa639a3207b3758cd8676f2ba91 |
| docs/reports/sprint4_d2_r7b_i1_r30_i1_r10_r2_r1_focused_restartcount_schema_correction.md | 6199 | 5538df46f3dfe55cff3981b1370496b3e3740a7362d0e4ed33815b4a36aa42d8 |

Mapping identity：

~~~text
path: config/mapping.yaml
bytes: 7112
SHA-256: d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
HEAD blob: b46a637f23c761d0a4c3fe048b3b7480a3dec2ce
relative to HEAD: clean
regular non-symlink: yes
~~~

## 4. Current authoritative boundary

### 4.1 Accepted prior gates

- package-closure implementation 已 committed，历史 implementation closeout 为 ddf55be。
- D2-R7A-R4-R1 independent Verification：PASS；其 scope 只覆盖 local package closure、non-DB regression、Compose render、temporary validation image、container import/static mapping 和 cleanup，不覆盖 deployment、activation 或 production facts。
- exact new mapping deployment：PASS / PM-VERIFIED / PM-ACCEPTED。
- config deployment Reliability：PASS WITH RECOMMENDATIONS / PM-VERIFIED / PM-ACCEPTED。
- current old-image restart observation：RESTARTCOUNT_ZERO_STABLE，但该 observation 是历史 accepted evidence，不是本轮 fresh remote observation。

### 4.2 Image and runtime facts

当前最近一次权威 Collector observation 是 safe old image：

~~~text
container ID: 5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524
image ID: sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
Config.Image: edge-mes-demo-collector
Compose project/service: edge-mes-demo / collector
status: running
top-level $.RestartCount: 0 -> 0
/app/config: /opt/edge-mes-demo/config -> /app/config, read-only
~~~

这组事实只作为 current safe old-image planning baseline；未来 Phase 2/3 必须 fresh-observe，不能直接继承。

sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c 是历史 known-bad image，曾在 common.station_event import closure 处失败：ModuleNotFoundError: No module named common。它必须永远标记为：

~~~text
HISTORICAL KNOWN-BAD IMAGE
DO NOT ACTIVATE
DO NOT RETAG AS CURRENT
DO NOT USE AS ROLLBACK
DO NOT REPRESENT AS PACKAGE-CLOSED
~~~

sha256:6e064bdc89b39afa1223aca9fbcd18add8c0cb9d0070bce6f227eb1581bba905 只曾是 local validation image，已由 Verification 删除；它不是 current present、transportable 或 deployable image identity。

fresh deployable package-closed image identity：NOT YET MATERIALIZED。

current old process runtime-loaded new mapping：NOT ESTABLISHED；package-closed new Collector active：NO；accepted-fact runtime active、production accepted-fact persistence 和 production acceptance：均 NOT ESTABLISHED。

### 4.3 Authority non-inheritance

前序 PASS、R8 config deployment、R9 Reliability、R10-R2-R1 RestartCount observation 和本 planning PASS 都不授权：

- image build、archive、transport、remote load、tag/retag；
- remote read-only observation；
- Collector restart、recreate、activation 或 rollback；
- logs/events、Docker exec、DB/API/PLC/V-PLC/simulator 操作；
- production data generation、accepted-fact persistence validation；
- cleanup、Git stage、commit、push 或 tag。

R10 observer/old-image-reload chain 已在 PM scope reset 下 CLOSED，不重新打开其 withdrawn RestartCount interpretation、logs/events forensics、repository-wide cache audit 或 aggregate untracked digest blocker。

## 5. Current Docker/Compose/package facts

### 5.1 Compose render

本轮唯一一次 docker compose config 为 static render，exit 0；没有调用 Docker daemon lifecycle。

Rendered Collector facts：

| Field | Rendered fact |
| --- | --- |
| project | edge-mes-demo |
| service | collector |
| build context | /Users/chenjie/Documents/MES/edge-mes-demo（Compose .） |
| Dockerfile | collector/Dockerfile |
| container name | edge-mes-collector |
| explicit image field | absent；当前 Compose 依赖 project/service 默认 image naming |
| restart policy | unless-stopped |
| dependencies | postgres: service_healthy; s7-plc-sim: service_started |
| env | DATABASE_URL, SIMULATOR_URL, SNAP7_HOST, SNAP7_PORT, TZ |
| config mount | host ./config → /app/config, read-only |
| lifecycle command in this task | 0 |

Protected service dependency graph means a future Collector-only operation must not bring up or recreate dependencies. --no-deps and --no-build are mandatory activation properties.

### 5.2 Dockerfile and COPY closure

Current committed collector/Dockerfile：

~~~dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY collector/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY collector/app ./app
COPY common ./common
CMD ["python", "-m", "app.main"]
~~~

Live identity：218 bytes；SHA-256 e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839；HEAD blob 7d89c84349a5e86f673767e25ac52da7013cc456。

没有 .dockerignore。因此 future execution 不得把 live working tree 的 wildcard content 当作 source authority；必须依据 frozen commit 的 exact git ls-tree selection materialize build context。

Current Dockerfile 的 image input closure 是：

1. build instruction：collector/Dockerfile；
2. dependency input：collector/requirements.txt，71 bytes，SHA-256 eaa0a1bf2e133cdfdff2795f4604fc5fbeb54fe0e2bb1a0b990bf1a41a8f54cc；
3. application input：committed collector/app/**，当前 20 个 committed files；
4. shared package input：committed common/**，当前 16 个 committed files；
5. config/mapping.yaml 不在 image COPY closure 内，只通过 read-only /app/config mount 进入 runtime。

tests/test_collector_container_packaging.py 当前为 941 bytes，SHA-256 351e80a76a53f742258e91196b109172de7b43dc3fa359e63ef44c9e7ad9c26e，HEAD blob d13770db1bd7f9edac95aa6e33edab48636ab077。它实际断言 Compose context: .、dockerfile: collector/Dockerfile 以及三条关键 COPY：requirements、app、common。R7A-R4-R1 accepted evidence 为 packaging test 2 passed，并把该 closure 与 container import/static mapping 绑定。

### 5.3 Runtime import closure

从当前 collector/app import graph 实际读取并核对：

- app.main imports app.config、EventDetector、EventCollectorWorker、Storage、Snap7Source 和 SimulatorSource；
- EventCollectorWorker imports app.plc address/decoder/mapping/read-plan closure、reliability、accepted fact、resolved config registry、station adapter、runtime source 和 storage；
- station_event_adapter.py 唯一引入 shared package：common.station_event；
- common.station_event.__init__ 实际 re-exports constants.py、errors.py、fingerprint.py、lifecycle.py、models.py、projection.py、serialization.py 和 validation.py；这些模块互相 import 的文件也均已读取。

实际 Collector runtime-referenced committed common closure：

~~~text
common/__init__.py
common/station_event/__init__.py
common/station_event/constants.py
common/station_event/errors.py
common/station_event/fingerprint.py
common/station_event/lifecycle.py
common/station_event/models.py
common/station_event/projection.py
common/station_event/serialization.py
common/station_event/validation.py
~~~

common/line_config/** 是 committed 且当前 COPY common ./common 的 image closure 成员，但不是从 current Collector runtime import graph 实际引用的 module；它不应被误写成 runtime import prerequisite。common/.DS_Store 是 working-tree external/untracked content，不是 committed build authority，future exact context 必须排除。

### 5.4 Current source behavior relevant to future evidence

- EventCollectorWorker.__init__() 读取默认 /app/config/mapping.yaml，创建 Storage、mapping snapshot、resolved config snapshot、in-memory registry、Snap7 client 和 four read plans。
- build_resolved_config_snapshot_from_mapping() 校验 mapping content hash、decoder registry hash 和 resolved config hash consistency。
- EventCollectorWorker 之后才启动 run_forever thread；main.py 还会构造 simulator/Snap7 source、Storage 和 EventDetector，并进入 snapshot loop。
- accepted station-event fact 只在 adapter decision accepted 后，和 cycle persistence 一起在 transaction 中写入；ACK/read_done 语义保持现有代码边界。
- 当前代码没有在 EventCollectorWorker initialization 或 main.py startup log 中输出 schema_version、config_version、line_id、read-plan count 或 resolved config hash；当前没有 runtime config/hash registry endpoint 或 process-bound startup evidence。

因此，container 内静态 mapping initialization 可以证明 source/mount/config compatibility，但不能单独证明 current running process 实际加载了该 mapping。

## 6. Smallest bounded build-input and identity contract

### 6.1 Frozen execution baseline

future Phase 1 必须在执行开始重新冻结：

1. exact repository root、branch、HEAD、origin/main、ahead/behind 和 index state；
2. execution baseline commit 必须是完整 SHA，而不是 branch name 或短 hash；
3. build-relevant paths 必须 clean relative to execution baseline：collector/Dockerfile、collector/requirements.txt、collector/app/**、common/**、docker-compose.yml、tests/test_collector_container_packaging.py、config/mapping.yaml；
4. six named external dirty paths 和所有 unrelated untracked paths 必须保持 excluded；它们不能被 wildcard context 选入；
5. 任何 build-relevant tracked drift、symlink、missing committed file、working-tree content 与 git show <baseline>:<path> 不一致，均为 Phase 1 HOLD；不 repair、不清理、不继承历史 source hash。

### 6.2 Exact build context

事实层面的 Compose build context 仍是 repository root .；不得修改 Compose 或 Dockerfile。

推荐 future local build 使用一个 task-owned、root-shaped、只含 committed exact inputs 的 temporary build context，保持以下相对路径：

~~~text
collector/Dockerfile
collector/requirements.txt
collector/app/**
common/**
~~~

该 context 目录的绝对路径、parent ownership、mode、non-symlink identity 和 exact basename 必须在 future execution Prompt 中冻结；目录在创建前必须 ABSENT/NON-SYMLINK，创建后只能包含上述 committed selection。它不是新的 repository artifact，也不能由本 planning task 创建。其目的只是把当前 root-context/COPY contract 映射为最小、可审计的 committed projection，避免 .dockerignore 缺失时把 unrelated working-tree content 送入 build。

如果 future Docker toolchain 不接受该 root-shaped projection，执行 gate 必须停止并由 PM 决定是否使用 committed repository root context；不得自动修改 Dockerfile、Compose 或 .dockerignore，也不得静默扩大到 B。

### 6.3 Source selection rule

future selection rule 是：以 frozen full commit 为 source authority，按 git ls-tree -r --name-only <baseline> -- collector/app common 取得 committed file set，再以 git show <baseline>:<path> materialize exact bytes；不使用 working-tree wildcard、不使用 historical report source hash 代替 bytes、不继承 old image 内容。

The current Dockerfile semantics copy whole common/, so the safe current-contract set is all committed common/**, including committed-but-not-imported common/line_config/**；reducing that set further would be a separate Dockerfile/package-contract change and is not part of R31.

### 6.4 Tag and image ID authority

- Local descriptive build tag：edge-mes-demo-collector:r31-pkg-closed-<full-baseline-short>；未来 Prompt 必须填入 exact frozen suffix，并先确认不存在或与本 transaction exact identity一致；不得覆盖未知 tag。
- Image identity authority：local docker image inspect top-level Id，完整 sha256:<64>；不以 tag、Config.Image、size、created time 或 source report hash 代替。
- Architecture authority：image inspect 的 Os=linux、Architecture=arm64；linux/arm64 必须被显式要求并在 local validation 和 remote load 后分别核对。
- remote loaded identity：remote docker image inspect exact Id 必须 byte-for-byte 等于 local fresh image ID；tag 只用于 lookup/transport label。
- Compose compatibility alias：当前 service 没有显式 image:。只有 Phase 4 在 fresh preflight 已证明当前 default alias edge-mes-demo-collector 指向 exact old safe image 后，才可以把 fresh ID tag 到该 alias；这个 alias 是 mutable activation input，不是 identity authority。

## 7. Candidate comparison

| Dimension | A: local arm64 image + archive | B: exact source package + bounded remote arm64 build |
| --- | --- | --- |
| source authority | local frozen committed projection | remote frozen source archive from same commit |
| build location | local Docker daemon, explicit linux/arm64 | remote Docker daemon, explicit linux/arm64 |
| current fact support | historical local arm64 validation passed; current Dockerfile closure is live-verified | Dockerfile/source facts support it, but remote build has not been observed |
| image identity | local exact ID before transport; remote exact ID after load | remote exact ID only after build |
| transport | one exact docker save archive plus one bounded transport | source archive transport plus remote build layers |
| remote mutation surface | load image only before activation | source staging and Docker build/layers before activation |
| architecture/disk dependence | remote architecture and disk needed for load/archive | remote architecture, disk, CPU, base image and build availability needed |
| reproducibility | local output bound by source manifest, Dockerfile identity, platform and archive SHA | output additionally depends on remote builder/base/cache/network state |
| failure residue | archive or loaded image can be retained for diagnosis; no lifecycle impact | source tree, build cache/layers and partial build residue may remain |
| rollback identity | old safe image is retained and can be addressed by exact ID | same rollback identity, but more pre-activation remote mutation |
| verdict | PREFERRED | FALLBACK ONLY WITH NEW PM AUTHORITY |

A is proportionate because the current local package closure is already proven and the fresh deployable image does not exist only because the old validation image was intentionally deleted. B is not rejected as technically impossible; it is rejected as the primary path because it increases remote dependency and build-state ambiguity without a current local fact showing A failure.

## 8. Future phase authority plan

这些 phases 是独立 authority phases，不构成一次性自动执行许可。

### Phase 1 — Fresh local image materialization and isolated validation

Allowed scope：

- fresh local Git/source/build-input gate；
- exact root-shaped committed build context；
- local linux/arm64 image build using current committed Dockerfile；
- exact local image ID、platform、size、tag and source manifest capture；
- isolated image import-closure and static mapping validation。

Validation contract：

- bounded container invocation is read-only/rootfs read-only, network none, exact read-only /app/config mapping mount, PYTHONDONTWRITEBYTECODE=1；
- import app.main、app.services.event_collector、common.station_event and the actual common.station_event re-export closure；
- call only static load_edge_mapping、build_read_plans、build_resolved_config_snapshot_from_mapping；
- do not call app.main.main()、construct Storage/Snap7 client、connect DB/API/PLC/simulator、generate production data or start a long-lived process；
- compare schema_version=runtime-mapping/v1、config_version=2026.06.26-slice-a、line_id=LINE_001、read-plan count 4 and resolved config hash 0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38。

Terminal：LOCAL_PACKAGE_CLOSED_VALIDATION_PASS only when the exact image ID, import closure, static mapping and host/container mapping relation all pass。A local PASS does not establish transport, load, activation or runtime-loaded state。

### Phase 2 — Bounded image archive/transport/load and exact remote image identity verification

Allowed scope：

- fresh load-only remote prerequisite preflight for linux/arm64、exact task-owned remote stage parent and free disk；
- docker save from the Phase-1 exact image ID to one exact local archive path；
- archive byte count and SHA-256 capture；
- one bounded transport to one exact remote stage path；
- one remote docker load and exact post-load docker image inspect ID comparison。

Frozen call budget：

~~~text
load prerequisite SSH read-only call: 1
archive transport call: 1
remote load + exact image-ID verification SSH call: 1
retry/resume/second transport/second load: 0
~~~

The load prerequisite call is not Phase-3 activation preflight; it only proves the remote Docker architecture, sufficient disk for the archive/load, and task-owned stage parent. No Collector or protected service lifecycle may be inspected or mutated by that load-only call unless separately included in the execution Prompt.

Archive ownership contract：

- local archive parent is a task-owned non-symlink directory, exact path and owner/mode frozen before creation；
- archive basename is deterministic from the frozen baseline and transaction identity；
- archive path is ABSENT/NON-SYMLINK before docker save and created once with no overwrite；
- after save, record exact bytes and SHA-256；archive SHA is transport payload authority；
- remote stage parent is a task-owned non-symlink directory owned by the authorized remote user, and remote archive basename is exact；
- transport must preserve bytes；remote received archive must be rechecked before load；
- load ID must equal local exact image ID；mismatch is terminal LOAD_ID_MISMATCH and must not activate or retag；
- archive/image cleanup is not part of Phase 2 unless a separate cleanup authority is granted。

### Phase 3 — Fresh read-only remote activation preflight

Phase 3 is a new read-only gate after Phase 2 exact image load. It freezes the active old state, rollback target, config identity and protected state immediately before any mutable tag or lifecycle action. It must not restart, recreate, tag, retag, load, remove, clean or activate.

### Phase 4 — One controlled Collector-only activation

Activation category only：

- verify the loaded fresh ID is present and the immutable R31 descriptive tag resolves to that ID；
- with a fresh preflight proving edge-mes-collector alias currently resolves to exact old safe ID, assign the fresh ID to that Compose compatibility alias；
- invoke only the collector Compose service with --no-deps、--no-build、--force-recreate、-d properties；
- do not run broad Compose down/up, dependency lifecycle, image build/pull, or any other service action；
- do not generate production data as an activation convenience step。

The mutable alias tag mutation is not needed for identity proof but is needed to make the current Compose service, which has no explicit image: field, consume the exact loaded image without a remote build. It is authorized only in Phase 4 after Phase-3 old-alias identity proof. It must never point to 7b942... or the deleted 6e064... identity.

### Phase 5 — Post-activation source/import/config/lifecycle verification

Phase 5 is a separate read-only postflight. Minimum evidence：

- active container top-level Image equals fresh exact image ID；
- Config.Image equals the expected compatibility alias only as configuration evidence；
- Compose project/service labels are edge-mes-demo / collector；
- container ID is the new container created by Phase 4；Created、StartedAt、status and bounded lifecycle tuple are persisted；
- active state is Running=true、Restarting=false、Dead=false、ExitCode=0、OOMKilled=false、Error empty；
- top-level $.RestartCount remains stable across the bounded interval；
- /app/config source/target/read-only mount is exact；
- active image/source hash manifest proves common.station_event closure and key current source identities；
- exact mapping file is regular/non-symlink, host and container bytes/SHA match the new mapping identity；
- static mapping fields and resolved hash equal the frozen values in Phase 1；
- every non-Collector protected service hard-field tuple is unchanged。

Phase 5 results classify only ACTIVATED when the active image/lifecycle/source/import/config/mount relation passes。They do not establish RUNTIME-LOADED unless a process-bound runtime evidence path exists。

### Phase 6 — Rollback only after predefined activation terminal failure

Phase 6 is conditional and may start only for a predefined terminal activation failure. It is not a diagnostic cleanup phase and is not a generic recovery experiment. If no terminal failure occurs, rollback is NOT EXECUTED。

### Phase 7 — Separate later production accepted-fact persistence gate

After activation PASS, production accepted-fact validation is still a separate Level 2 authority. It must independently freeze production scope, DB/API authority, fact identity, persistence transaction, ACK/read_done relation and acceptance criteria. Phase 1–6 never establish PRODUCTION-ACCEPTED。

## 9. Future fresh remote preflight matrix

The following values must be freshly observed in a new execution authority. The historical endpoint and old-image facts below are planning references only.

| Preflight item | Required authority / terminal use |
| --- | --- |
| SSH endpoint | PM Prompt exact endpoint; historical reference mari@10.0.0.217:22; no endpoint inference from old reports |
| SSH identity | PM Prompt exact identity authority; historical reference /Users/chenjie/.ssh/edge_pi_codex; metadata only, never read private-key content |
| current Collector container ID | top-level inspect exact ID; bind to all later image/lifecycle evidence |
| current Collector image ID | top-level $.Image, full sha256:<64>; rollback candidate source |
| Config.Image | capture configured alias; not image identity authority |
| Compose labels | com.docker.compose.project=edge-mes-demo, com.docker.compose.service=collector |
| Created, StartedAt | current old container identity and rollback relation |
| Running / Restarting / Dead | activation eligibility and postflight terminal fields |
| ExitCode / OOMKilled / Error | startup safety and rollback terminal classification |
| top-level $.RestartCount | fresh integer; bounded post-activation stability only |
| restart policy | must preserve current Collector policy unless separately authorized |
| /app/config mount | exact source /opt/edge-mes-demo/config, target /app/config, read-only true |
| current edge-mes-demo-collector tag | fresh exact ID comparison; tag cannot replace ID authority |
| exact rollback image presence | old safe full image ID must be present and inspectable before alias mutation |
| 7b942... presence | diagnostic-only presence; never eligible/candidate/rollback |
| target mapping identity | path type, bytes, SHA, owner/group/mode and target relation; no assumption from R8 |
| retained backup identity | exact old bytes/SHA/device/inode/ownership if present; fresh evidence only |
| upload sidecar / rollback temp | exact expected task sidecars and absence/presence; no cleanup in this gate |
| protected services | fresh hard-field matrix for every non-Collector Compose service |
| Docker architecture | linux/arm64 remote load compatibility; fresh, not historical inheritance |
| remote free disk | only for A archive staging/load; bounded value, not generic capacity audit |

The old safe image is eligible only when it is freshly observed, exact, present, not known-bad, and can be restored by image ID. A tag name alone never qualifies as rollback.

## 10. Protected-service hard-field matrix

Current Compose non-Collector services are the protected set for a Collector-only activation: postgres、simulator、s7-plc-sim、api、dashboard、grafana、prometheus、node-exporter 和 sync-worker。Future preflight may narrow this to the exact currently active set only if PM names that set; it must not silently omit the four core services postgres、api、s7-plc-sim、simulator。

For each protected service, pre/post equality must cover：

~~~text
Id
top-level Image
com.docker.compose.project
com.docker.compose.service
Created
StartedAt
State.Status
State.Running
State.Restarting
State.Dead
State.ExitCode
State.OOMKilled
State.Error
top-level RestartCount
HostConfig.RestartPolicy
mount source/target/read-only tuple when present
~~~

Config.Image may be captured for diagnosis but is not compared to a guessed short name; the prior postgres:16 versus postgres false assertion is withdrawn and must not return as a blocker. Any actual hard-field change is PROTECTED_SERVICE_DRIFT, a terminal failure that blocks activation and qualifies for rollback only if activation already occurred.

## 11. Activation terminal and failure matrix

| Result | Meaning | Rollback |
| --- | --- | --- |
| IMAGE_LOADED_EXACT | remote load ID equals local exact ID; no Collector lifecycle | no |
| ACTIVATION_ELIGIBLE | fresh old image, alias, target/backup, protected fields, loaded fresh ID and mount facts all pass | no |
| ACTIVATED | one Collector-only recreate completed and Phase-5 exact image/static/lifecycle/protected checks pass | no |
| LOAD_ID_MISMATCH | remote image ID differs from local archive authority | no; activation forbidden |
| IMAGE_ARCH_MISMATCH | local/remote image is not linux/arm64 | no; hold and preserve evidence |
| ARCHIVE_INTEGRITY_FAILED | local or remote archive bytes/SHA mismatch | no; no load/activation |
| TAG_ALIAS_AMBIGUOUS | current alias is absent or not exact old safe ID before mutation | no; no tag mutation |
| ACTIVATION_COMMAND_FAILED | one Collector-only activation command fails before a known active target is established | no automatic second attempt; classify ambiguous state first |
| WRONG_ACTIVE_IMAGE | active top-level image ID is neither fresh exact ID nor the preflight old exact ID | yes if activation was attempted |
| IMPORT_CLOSURE_FAILED | exact active image static import does not include common.station_event closure | yes |
| MAPPING_IDENTITY_FAILED | target/mount/container mapping bytes, SHA, schema or resolved hash mismatch | yes |
| RESTART_LOOP | bounded post-activation lifecycle is not stable, or restart count changes from fresh zero | yes |
| PROTECTED_SERVICE_DRIFT | any protected hard field changes | yes if change followed activation; otherwise HOLD/no mutation |
| AMBIGUOUS_ACTIVE_TARGET | exact active image/container cannot be determined | yes only under a pre-authorized conditional rollback controller; otherwise HOLD |
| diagnostic-only difference | e.g. non-authoritative Config.Image wording, optional telemetry or absent theoretical field combination | no automatic rollback |

No retry, resume, second SSH, second activation or broad forensic chain follows any terminal result. A pre-activation failure leaves the old Collector unchanged and does not require rollback.

## 12. Proportional rollback design

### 12.1 Target and trigger

Rollback target is the exact old safe image ID observed in Phase 3 immediately before Phase 4. The target must be present and inspectable at the moment rollback begins. 7b942... is excluded even if present; 6e064... is excluded because it was deleted and is not a current image object.

Rollback triggers are limited to terminal failures that can leave an unsafe active state：

- startup failure or non-running/restarting/dead Collector；
- exact image ID wrong or ambiguous；
- missing common.station_event import closure；
- exact mapping/mount/config initialization failure；
- bounded restart loop；
- protected service hard-field drift caused by activation；
- inability to prove a safe active target after the one activation。

Do not rollback for diagnostic-only differences that cannot cause false PASS, unsafe active state, stale config truth or protected-object mutation。

### 12.2 Rollback action category and minimum safe poststate

The future rollback controller may only：

1. recheck that the recorded old full image ID is present；
2. restore the edge-mes-demo-collector Compose compatibility alias to that exact old ID；
3. perform the same Collector-only --no-deps --no-build --force-recreate lifecycle category；
4. re-inspect active top-level image ID, container state, mount and protected hard fields。

Rollback completion minimum safe state：

~~~text
active Collector top-level Image == Phase-3 old exact safe image ID
Config.Image == edge-mes-demo-collector as configured alias
Compose labels == edge-mes-demo / collector
Running=true / Restarting=false / Dead=false
ExitCode=0 / OOMKilled=false / Error=empty
/app/config source -> target mount exact and read-only
bounded old-image lifecycle tuple stable
all protected hard fields unchanged from Phase-3 prestate
~~~

Cleanup is not rollback. New image objects, archive, remote stage files, descriptive tags, backup and sidecar residue remain untouched unless a later exact cleanup authority is granted. If rollback itself cannot establish the minimum safe state, terminal is ROLLBACK_FAILED_OR_AMBIGUOUS; stop without retry or cleanup.

## 13. Post-activation evidence and runtime-loaded boundary

### 13.1 Source/import/image evidence

Future Phase 5 must persist a manifest binding：

- execution baseline full commit；
- exact Dockerfile/requirements/app/common input identities；
- local fresh image ID/platform；
- archive bytes/SHA；
- remote loaded image ID；
- active container ID and top-level image ID；
- key active image paths and hashes, at minimum /app/app/main.py、/app/app/services/event_collector.py、/app/app/services/accepted_station_event_fact.py、/app/app/services/storage.py、/app/common/station_event/__init__.py and the committed common station-event closure。

This establishes that the active container is using the fresh package-closed image and that common.station_event exists in the exact image. It does not treat the old image source hashes from R6 as current source authority.

### 13.2 Mapping evidence

The same postflight must prove：

- host /opt/edge-mes-demo/config/mapping.yaml exact regular non-symlink identity equals the PM-approved new mapping bytes/SHA；
- container /app/config/mapping.yaml reads the same bytes/SHA through the read-only bind mount；
- schema_version=runtime-mapping/v1；
- config_version=2026.06.26-slice-a；
- line_id=LINE_001；
- read-plan count 4；
- resolved config hash 0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38；
- host static initialization and container static initialization agree on every above field。

This is STATIC_MAPPING_INITIALIZED/ACTIVATED evidence, not automatically RUNTIME-LOADED evidence.

### 13.3 Current process runtime-load observability

当前 source review found no existing process-bound config/hash log, registry API or runtime status field that exposes the mapping snapshot actually loaded by the current EventCollectorWorker process。resolved_config_snapshot is an in-memory object, and current logs contain only generic Collector/event startup information without the required mapping identity fields。

Therefore：

- container static import and mapping initialization：can establish local/container static compatibility；
- active container exact image + static checks + bounded running：can establish ACTIVATED；
- current code as committed：不能建立 RUNTIME-LOADED；
- a later minimum observation method is a separately authorized source/runtime observability task that emits one process-startup record only after mapping load and resolved snapshot/hash construction, including config_hash、config_version、schema_version、line_id、read-plan count and a time/container correlation。That task must not be smuggled into R31 or activation execution；
- without that later process-bound record, future reports must say NOT RUNTIME-LOADED, even if docker exec or an isolated docker run static check passes。

### 13.4 Lifecycle evidence

Bounded lifecycle proof is limited to exact top-level inspect fields and a small interval. It proves current active container identity and absence of an observed restart loop during that interval; it does not prove historical absence of interruptions, application business health, DB persistence or production truth.

### 13.5 Production evidence boundary

None of the following establishes PRODUCTION-ACCEPTED：local build PASS、archive SHA、remote load ID、active image inspect、common import, static mapping hash, container running, stable RestartCount, current generic startup log or rollback PASS。Production acceptance requires Phase 7 independent evidence for accepted-fact persistence and its exact DB/API/ACK/read_done truth boundary。

## 14. Evidence persistence and classification

The following layout is planned only; no path below was created in R31：

~~~text
docs/reports/sprint4_d2_r7b_i1_r31_image_materialization_execution.md
docs/reports/evidence/d2_r7b_i1_r31/phase1_local_materialization/
docs/reports/evidence/d2_r7b_i1_r31/phase2_archive_transport_load/
docs/reports/evidence/d2_r7b_i1_r31/phase3_remote_preflight/
docs/reports/evidence/d2_r7b_i1_r31/phase4_collector_activation/
docs/reports/evidence/d2_r7b_i1_r31/phase5_post_activation/
docs/reports/evidence/d2_r7b_i1_r31/phase6_rollback/
~~~

Future artifact paths must be exact-authorized before creation. Each persisted terminal/manifest must bind its own bytes, source identity, phase, call count and terminal classification. No helper, shell script, Python orchestrator or complete execution Prompt is included in this report.

R31 evidence classification：

~~~text
PLANNED
WRITTEN: only the exact R31 report path
NOT EXECUTED
NOT BUILT
NOT TRANSPORTED
NOT LOADED
NOT ACTIVATED
NOT ROLLED BACK
NOT RUNTIME-LOADED
NOT PRODUCTION-ACCEPTED
~~~

Future evidence must keep these states distinct：

~~~text
committed source identity
planning assumption
future fresh-preflight requirement
local static validation
remote loaded-image validation
active-container validation
runtime-loaded config evidence
production accepted-fact evidence
~~~

## 15. Authority combination and smallest future execution boundary

### 15.1 Recommended split

Recommended：

~~~text
Task A: Phase 1 + Phase 2
  local arm64 materialization/isolated validation
  archive bytes/SHA
  one transport
  one remote load
  exact remote image-ID verification
  no Collector/protected lifecycle

ChatGPT PM durable intake

Task B: Phase 3 + Phase 4 + Phase 5 + conditional Phase 6
  fresh activation preflight
  one Collector-only activation
  bounded post-activation validation
  rollback only on frozen terminal failure
  no cleanup and no production data

Task C: Phase 7
  separate production accepted-fact persistence gate
~~~

Task A and Task B must not share automatic authority, remote call budget, rollback permission or Git permission. A PASS in Task A establishes only IMAGE_LOADED_EXACT; it cannot become activation eligibility without Phase 3 fresh facts.

### 15.2 When a bounded controller may combine phases

A future bounded controller may combine Phase 3–6 in one PM-authorized activation task only if all of the following are frozen before the first mutation：

- fresh exact endpoint/identity and one SSH budget；
- fresh current Collector old ID, alias ID, container ID, mount, state and top-level RestartCount；
- fresh exact old rollback image present；
- fresh exact loaded R31 ID present and architecture matched；
- Compose project/service labels and default alias semantics matched；
- all protected-service hard fields persisted；
- target mapping, retained backup, upload sidecar and rollback temp identities persisted；
- one activation, one postflight, and at most one conditional rollback are explicit controller terminals；
- rollback target is the preflight old full image ID, never a tag-only or known-bad target；
- --no-deps --no-build --force-recreate collector is the only lifecycle category；
- no cleanup, logs/events forensics, DB/API/PLC/V-PLC/simulator action or production data generation；
- every child/terminal is schema-valid and failure is fail-closed with no retry/resume/second SSH。

Even under those conditions, Phase 7 remains separate. The recommended split retains the image-staging boundary before lifecycle mutation, making the failure boundary proportional to the current MVP claim.

## 16. Checks and non-actions

本轮实际 checks：

- fresh Git baseline and exact tracked dirty classification；
- current HEAD/origin/main/parent/ahead-behind/index/diff checks；
- required handoff/report identities；
- mapping bytes/SHA/blob/clean state；
- Dockerfile, Compose, requirements, packaging test and runtime source reads；
- docker compose config static render exactly once；
- current committed Dockerfile COPY closure and actual common.station_event import closure review；
- build-relevant cleanliness and committed path enumeration；
- report path ABSENT/NON-SYMLINK/UNSTAGED precondition；
- no source/test/config/helper/evidence artifact write before this report；
- no SSH, SCP/SFTP/rsync, network, remote read, remote Docker or Docker daemon mutation；
- no docker build/run/save/load/tag/image rm；
- no Compose lifecycle、DB/API/PLC/V-PLC/simulator、logs/events、Docker exec、cleanup or Git mutation。

## 17. MVP 路径一致性

- 当前任务是否直接服务已批准 MVP：yes。
- 对应 MVP 交付物：fresh package-closed Collector image materialization、exact image identity、最小 Collector-only activation boundary，以及在不制造 production truth 的前提下可回滚的 runtime deployment gate。
- minimum invariant：active Collector 只能由 exact fresh package-closed image ID 驱动；rollback 只能回到 activation 前 fresh-observed exact old safe image；任何 image/config/import/lifecycle/protected-service ambiguity 都不得被写成 PASS。
- 是否引入新产品能力、威胁模型、证据/保留框架或基础设施：no。本报告只冻结与当前 Collector MVP deployment/activation claim直接相关的最小 identity、phase、rollback 和 evidence contract；没有创建 generic deployment platform 或 forensics framework。
- 是否出现 task inflation：no。未重新打开 R10 forensics、repository-wide cache、aggregate digest、production acceptance 或 generic controller implementation。
- classification：MVP-ALIGNED WITH BACKLOG ITEMS。
- backlog/recommendation：current process-bound runtime config observability 需要后续最小 source/runtime gate；它不阻塞本 planning PASS，但没有它不能声称 RUNTIME-LOADED。

## 18. Thread 输出 / 上下文评估

- 本次输出长度：长。完整 planning contract 已持久化到 exact durable report，Chat 只返回 concise manifest。
- 当前 Thread 是否建议继续：no。
- 下一轮是否建议新开 Thread：yes。
- 理由：本轮已完成独立 Level 2 planning、source/package closure recovery、mechanism selection 和 authority split；下一步是 ChatGPT PM durable intake。后续 Phase 1/2 或 Phase 3–6 必须各自使用新 authority 和 fresh context，不得由当前 Thread 继续执行。

## 19. Next gate and stop point

唯一 next gate：

~~~text
D2-R7B-I1 R31 planning report
→ ChatGPT PM durable intake only
~~~

本报告完成后立即停止。不得自动进入 image build、archive、transport、remote load、tag mutation、remote preflight、Collector restart/recreate/activation、rollback、logs/events、runtime-loaded mapping validation、production accepted-fact validation、cleanup 或 Git stage/commit/push/tag。

