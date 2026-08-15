# Sprint 4 D2-R3 Direct-DD Collector Accepted-fact Deployment

## 报告、任务、Thread、Authority

~~~text
报告名称：Sprint 4 D2-R3 Direct-DD Collector Accepted-fact Deployment
任务名称：Data-first Gate D2-R3 — Deploy the Frozen Collector through Shell-free Archive Transport
执行 Thread：新的独立 Architecture / Integration Thread

Authority ID：SPRINT4-D2-R3-DIRECT-DD-COLLECTOR-DEPLOYMENT-9e0aba2
Authority type：COLLECTOR-ONLY DEPLOYMENT RETRY
Source implementation authority：NONE
DB/schema authority：NONE
V-PLC/PLC authority：NONE
Product-data query authority：NONE
~~~

## 结论

~~~text
HOLD / EXECUTION_CONTRACT_VIOLATION / SSH2_TERMINAL_INCOMPLETE
~~~

SSH #1 的 direct /usr/bin/dd transport 返回 0。SSH #2 通过了远端 archive identity、Compose identity、Collector prestate、protected prestate，并完成唯一 Docker build 的 ID/platform validation；其 Collector-only Compose command 已输出 Container edge-mes-collector Recreate。但本地 SSH 执行终端在该行之后没有返回 SSH #2 exit，也没有返回 new Collector identity、protected poststate、source hashes、import verification、rollback 或 remote archive cleanup terminal。由于 D2-R3 的唯一 SSH #2 已消费，第三次 SSH、retry 或外部补偿 mutation 均禁止。

因此本报告不声明 Collector 已部署，不声明 accepted production fact 已生成，不声明 Collector-to-DB product path PASS，也不进入 D3。

## D2 系列 intake

~~~text
D2：HOLD / REMOTE_EXECUTION_COMMAND_SYNTAX_FAILED / NO_DEPLOYMENT
D2-R1：HOLD / ARCHIVE_TRANSPORT_OR_INTEGRITY_FAILED
D2-R2：HOLD / ARCHIVE_TRANSPORT_OR_INTEGRITY_FAILED
~~~

保留的根因序列：

~~~text
D2：Python -c / nested quoting 在 controller initialization 前失败。
D2-R1：没有固定 mtime 的 git archive identity 不确定。
D2-R2：transport remote command 未建立；tar stdin 被 remote login shell 当作 shell input。
D2-R3：改用两个独立 stdin 与 direct executable 边界；SSH #2 在 Recreate 输出后未产生完整 terminal evidence。
~~~

累计已观察远端产品 mutation / 尝试：

~~~text
Docker build：1（本 authority 唯一 build，ID/platform validation PASS）
Collector normal recreate：1 invocation（已输出 Recreate；完成与最终 identity 未证实）
rollback：0 observed；未进入 captured rollback terminal
DB/API/V-PLC：0
~~~

## Architecture reset

~~~text
remote sh -c：0 explicit invocation
remote bash -c：0 explicit invocation
Python SSH/deployment controller：0
transport script in SSH command string：0
archive and script sharing stdin：0

SSH #1 stdin：archive bytes only
SSH #1 remote executable：/usr/bin/dd
SSH #2 stdin：validated POSIX deployment script only
SSH #2 remote executable：/usr/bin/env -i ... /bin/sh -s
~~~

本 task 没有处理 D2-R2 的旧路径 /tmp/edge-mes-collector-9e0aba2-d2r2.tar。

## Required-read truth boundary

已按指定顺序读取 PM handoff、current status Section 0D 与 DB/API/Dashboard Slice 2 DB write-path summary、roadmap Sections 1A/3/5/6/8、PM operating rules Sections 12/13/14、D1-R2 报告、三份 D2 报告、Collector Compose service、Dockerfile、requirements、main、config、event_collector、accepted_station_event_fact、storage 与 migration 007。

读取确认：

~~~text
accepted decision 先构造 AcceptedStationEventFact；
accepted fact 与 legacy persistence 在同一 Storage.transaction() 中写入；
transaction commit 成功后才进入 ACK/read_done；
non-accepted disposition 在该事务前返回，不写 production fact；
Collector 没有源码 bind mount，仅有 ./config:/app/config:ro；
production_accepted_station_event_fact 是 accepted-only production landing surface；
本 task 未生成数据、未查询 DB、未调用 API、未操作 V-PLC。
~~~

## Read-only Git recovery and local hard gates

执行的 recovery command：

~~~bash
git status -sb
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git log -8 --oneline --decorate
git diff --name-only
git diff --cached --name-only
git diff --quiet HEAD -- collector api frontend docker-compose.yml
~~~

~~~text
branch：main
HEAD：9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
origin/main：9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind：0 / 0
cached：empty
protected source：PASS（collector api frontend docker-compose.yml）
~~~

Tracked dirty paths 保持原样：

~~~text
.gitignore
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
~~~

其他 untracked handoffs、reports、frontend artifacts 保持原样。目标报告在创建前为：

~~~text
ABSENT
NON-SYMLINK
UNTRACKED
UNSTAGED
~~~

本 task 未执行 restore、clean、stage、commit、push、tag 或 broad cleanup。

## Frozen source identities

~~~text
HEAD：9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
HEAD:collector tree：d6d2c1a9fcca23b7f4e6bf87c7ec669ee404e9c4

collector/Dockerfile
bytes：161
SHA-256：829b23cba1d01844c095140200f8a9e769527603cb2dbb445db50edca53169dc

collector/requirements.txt
bytes：71
SHA-256：eaa0a1bf2e133cdfdff2795f4604fc5fbeb54fe0e2bb1a0b990bf1a41a8f54cc

collector/app/main.py
bytes：2073
SHA-256：a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090

collector/app/services/event_collector.py
bytes：16342
SHA-256：eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f

collector/app/services/accepted_station_event_fact.py
bytes：5053
SHA-256：6545ef67d968ed849be57342ad630b258cd4a09519876efb02955a8c3c6fd911

collector/app/services/storage.py
bytes：38319
SHA-256：f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b
~~~

## Deterministic archive

Archive generation exactly once，使用的唯一 command：

~~~bash
git archive \
  --format=tar \
  --mtime='@1784115110' \
  --output="$local_archive" \
  HEAD:collector \
  Dockerfile \
  requirements.txt \
  app
~~~

~~~text
archive generations：1
fixed mtime：1784115110（2026-07-15T19:31:50+08:00）
regular：yes
symlink：no
bytes：163840
SHA-256：29947e8c7e3d2c8cbb642a503a37916a4068df8ac4b9cd694aba76871ce3a91d
local archive identity：PASS
~~~

Entry audit：

~~~text
entries：26
allowlist：Dockerfile、requirements.txt、app/、app/**
tests/docs/.git/working-tree source/untracked source/root project files：0
symlink entries：0
entry audit：PASS
~~~

同一个 local archive file 用于 local identity verification、entry audit 与 SSH #1 stdin；未重新生成传输 archive。

## Local deployment script

Repository 外只生成一个 deployment script。第一行/第一个 executable statement：

~~~sh
set -eu
~~~

~~~text
script generations：1
script bytes：13885
script SHA-256：68b10ae866cdf500d69fda14f35c77f3870001a466a3c28c02667f20e56891ba
/bin/sh -n invocations：1
/bin/sh -n exit：0
local script syntax：PASS
~~~

/bin/sh -n 后未修改 script；SSH #2 接收的 bytes 与该已验证 script 相同。

## SSH #1 direct-dd transport

实际执行 command：

~~~bash
ssh \
  -T \
  -o BatchMode=yes \
  -o IdentitiesOnly=yes \
  -i /Users/chenjie/.ssh/edge_pi_codex \
  mari@10.0.0.217 \
  /usr/bin/dd \
  of=/tmp/edge-mes-collector-9e0aba2-d2r3.tar \
  bs=65536 \
  conv=excl \
  status=none \
  < "$local_archive"
~~~

~~~text
SSH #1 invocation：1
SSH #1 exit：0
explicit remote sh -c：0
explicit remote bash -c：0
remote env/command substitution/variables/semicolon/pipe/redirection：0
remote archive path：/tmp/edge-mes-collector-9e0aba2-d2r3.tar
~~~

SSH #1 exit 0 只证明 direct dd 返回成功；archive identity 由 SSH #2 首段验证。

## SSH #2 direct env/sh deployment

实际执行 command：

~~~bash
ssh \
  -T \
  -o BatchMode=yes \
  -o IdentitiesOnly=yes \
  -i /Users/chenjie/.ssh/edge_pi_codex \
  mari@10.0.0.217 \
  /usr/bin/env \
  -i \
  PATH=/usr/bin:/bin \
  DOCKER_HOST=unix:///var/run/docker.sock \
  /bin/sh \
  -s \
  -- \
  /tmp/edge-mes-collector-9e0aba2-d2r3.tar \
  < "$local_script"
~~~

~~~text
SSH #2 invocation：1
SSH #2 exit：NOT CAPTURED；本地 SSH 执行终端在 Recreate 输出后结束，未返回 shell exit line
third SSH：0
retry：0
~~~

SSH #2 已输出的最后确定 terminal 为：

~~~text
BUILD=PASS
time="2026-07-23T19:31:59+08:00" level=warning msg="Found orphan containers ([edge-mes-dashboard]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag."
 Container edge-mes-collector  Recreate
~~~

该 orphan warning 仅为 Compose diagnostic output；没有执行 remove-orphans，也没有操作 Dashboard。

## Remote archive identity and cleanup

SSH #2 首段在任何 Docker operation 前输出：

~~~text
path：/tmp/edge-mes-collector-9e0aba2-d2r3.tar
regular：yes（由 -f 验证）
symlink：no（由 -L 验证）
bytes：163840
SHA-256：29947e8c7e3d2c8cbb642a503a37916a4068df8ac4b9cd694aba76871ce3a91d
remote archive identity：PASS
~~~

验证成功后 script 安装了只允许处理该 exact path 的 cleanup trap。由于 SSH #2 在 trap 的最终输出前没有返回完整 terminal，remote archive cleanup 为：

~~~text
remote cleanup：NOT OBSERVED
remote old D2-R2 archive path：未读取、未删除、未处理
~~~

不得把未观察到的 cleanup 推断为 PASS。

## Compose identity

SSH #2 在 Docker build 前输出：

~~~text
path：/opt/edge-mes-demo/docker-compose.yml
regular：yes
symlink：no
realpath：/opt/edge-mes-demo/docker-compose.yml
SHA-256：a71ab815a34f3c493f38ec572e0cf5892a9a7cdc081d8d3e2e312a380cad9ef0
rendered Compose/service-subtree hash：未计算
Compose identity：PASS
~~~

## Old Collector prestate

~~~text
Id：5fc9ca04be90a4b61c036f131ae0a5456069ff8b64d5f67748578d1c416f2330
Image：sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
Config.Image：edge-mes-demo-collector
Compose project/service：edge-mes-demo / collector
Created：2026-06-19T02:00:56.084936668Z
StartedAt：2026-06-19T02:01:08.375589781Z
State.Status：running
RestartCount：0
prestate：MATCHED
~~~

## Critical protected prestate

SSH #2 在 build 前捕获的完整 tuple（Id、Image、Compose project/service、Created、StartedAt、RestartCount、Status）：

~~~text
edge-mes-postgres
Id：bb3ba0738e692c68b14a62ca64296e484990d3b86b1f6d395c27b200af5cb890
Image：sha256:f961d097a9cedd37779baef1aab3fe87ef1c63b3b34d361f90a98ea5c9b77e56
Compose project/service：edge-mes-demo / postgres
Created：2026-06-14T05:57:13.239812435Z
StartedAt：2026-06-14T05:57:14.263634444Z
RestartCount：0
State.Status：running

edge-mes-api
Id：12e841b4ac33a75c835cee81f0df46e4dbcdb9382b50ca50523f5fad02c57058
Image：sha256:9f03f370b37fd5fd2ddfd4e4e9e64d4c6b60312910e731157888544371683c11
Compose project/service：edge-mes-demo / api
Created：2026-07-23T00:32:36.666029032Z
StartedAt：2026-07-23T00:32:37.955732924Z
RestartCount：0
State.Status：running

edge-mes-s7-plc-sim
Id：d21e950b98ae87bbd3ee321074100d0b54b174235ce46df34c5100e1130b785f
Image：sha256:3a28ae38c623d8cb80f775f954315e633b1108112082c37ece698c7562522238
Compose project/service：edge-mes-demo / s7-plc-sim
Created：2026-06-19T02:05:15.82128338Z
StartedAt：2026-06-19T02:05:27.378341652Z
RestartCount：0
State.Status：running

edge-mes-simulator
Id：3ebe1e4725af577ac477594afe3046f7e5a197b8162f503ebac036d09b4fcfd5
Image：sha256:08448d2876c30e9cbbecda4f0ca9a27a5e085a33f14dab2a6d2be3dd06430430
Compose project/service：edge-mes-demo / simulator
Created：2026-06-14T12:13:00.476282483Z
StartedAt：2026-06-14T12:13:23.098546695Z
RestartCount：0
State.Status：running

protected prestate：PASS
~~~

## Build result

唯一允许的 build command 在 remote archive stdin 上执行：

~~~bash
docker build \
  --quiet \
  --file Dockerfile \
  --tag edge-mes-demo-collector \
  - < "$archive_path"
~~~

~~~text
Docker build invocations：1
build output image ID：sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
post-build tag-resolution image ID：sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
created-ID/tag-ID equality：PASS
new image != old Collector image：PASS
OS：linux
Architecture：arm64
Variant：v8
Size：174329249
build/tag/platform validation：PASS
~~~

## Normal Collector-only recreate

唯一 normal lifecycle command：

~~~bash
docker compose \
  -p edge-mes-demo \
  -f /opt/edge-mes-demo/docker-compose.yml \
  up -d \
  --no-deps \
  --no-build \
  --force-recreate \
  collector
~~~

~~~text
normal Collector recreate invocation：1
fixed wait：script contained exactly one sleep 2 after normal recreate
polling：0
retry：0
observed terminal：Container edge-mes-collector Recreate
normal recreate completion：NOT OBSERVED
~~~

未执行 full Compose lifecycle、down、restart、stop/start、remove-orphans、Compose build、pull、buildx、network/volume mutation 或 broad logs。

## New Collector verification

因 SSH #2 terminal 在 Recreate 输出后未完成，以下均为未到达/未证实：

~~~text
new .Id：NOT REACHED
new .Image：NOT REACHED
new .Config.Image：NOT REACHED
new Compose project/service：NOT REACHED
new status/restart：NOT REACHED
Collector source verification：0
source hashes：NOT REACHED
import verification：0
import verification exit：NOT REACHED
~~~

不得用 build output image ID 代替 new Collector .Image，不得用 Recreate 日志代替 new identity。

## Protected poststate

~~~text
protected poststate：NOT REACHED
protected pre/post comparison：NOT REACHED
protected services unchanged：NOT CLAIMED
~~~

## Rollback

~~~text
rollback required：yes, because normal lifecycle terminal/validation was incomplete
rollback image retag invocation：0 observed
rollback Collector recreate invocation：0 observed
rollback status：NOT COMPLETED / NOT VERIFIED
final live state：UNKNOWN; no SSH retry is authorized
~~~

本 authority 不能安全声明 rollback succeeded 或 failed，因为 rollback function 的 terminal 没有被观察到；这正是本报告的 execution-contract blocker。

## Exact invocation counts

~~~text
local archive generation：1
local deployment script generation：1
local /bin/sh -n：1
SSH #1 direct-dd transport：1
SSH #2 direct env/sh deployment：1
total SSH：2
Docker build：1
normal Collector recreate：1 invocation
rollback image retag：0 observed
rollback Collector recreate：0 observed
Collector source verification：0
Collector import verification：0
DB query：0
HTTP/API request：0
V-PLC request：0
retry：0
third SSH：0
second archive：0
second build：0
~~~

## Cleanup

~~~text
local archive cleanup：PASS
local deployment script cleanup：PASS
local temporary files remaining：0
remote archive cleanup：NOT OBSERVED
remote broad cleanup：0
~~~

本地 cleanup 仅处理本 authority 生成且已核验 regular/non-symlink 的两个 exact temporary paths；未处理其他 temporary、repository 或 D2-R2 remote path。

## Prohibited-action audit

~~~text
remote sh -c：0
remote bash -c：0
Python SSH/deployment controller：0
generic deployment framework/evidence platform：0
source/config/test/Compose/migration/schema edit：0
working-tree/untracked source in archive：0
DB query/write：0
HTTP/API/Dashboard request：0
V-PLC/PLC request or mutation：0
data generation：0
full Compose lifecycle：0
non-Collector recreate：0 observed
pull/buildx/prune/network/volume mutation：0
remove-orphans：0
second archive：0
second build：0
third SSH：0
stage/commit/push/tag/git clean：0
broad cleanup：0
~~~

## Blockers

~~~text
Exact blocker：SSH #2 execution terminal stopped being observable after the normal Collector Recreate output.
Missing terminal fields：SSH #2 exit, new Collector identity, source hashes, import result, protected poststate, rollback, remote cleanup.
Product defect claim：none.
Data generation claim：none.
Live remote state：unknown and intentionally not inferred.
~~~

This is an execution-boundary failure, not evidence of a Collector source defect, Docker image defect, DB/API defect or product-data result.

## Recommendations

~~~text
PM intake only。
~~~

由于本 authority 的两次 SSH 上限已消费，任何 live-state re-observation、rollback repair、deployment retry 或 new transport authority 都需要新的独立 PM authority；不得继续本 Thread 的 SSH sequence。

## Next gate

~~~text
eligible for：PM intake only
PM approval required before：new independent deployment authority to re-establish live Collector identity/rollback status
D3：not eligible
~~~

D3 — controlled fresh accepted-result generation and exact PostgreSQL/API reconciliation — 只能在新的独立 authority 下、且 Collector deployment status 被重新建立后进入。此报告不授权 D3、DB/API reconciliation、V-PLC、Dashboard、Full Runtime 或 Git operation。

## MVP 路径一致性

~~~text
approved claim：Collector accepted production fact write path is deployed before fresh data generation
minimum invariant：active Collector may be changed only from an exact deterministic archive, with complete post-mutation identity/source/import/protected-state evidence
new capability/infrastructure：none
scope drift：none
classification：MVP-ALIGNED
~~~

Architecture reset 直接服务于 deploy-before-data-generation 的最小安全边界；没有建设通用 transport/deployment framework。唯一的 scope problem 是本次执行终端没有完成证据闭环，因此不能把 partial mutation evidence 提升为产品 PASS。

## Thread/context assessment

~~~text
output length：long evidence report
current Thread continue：no
new Thread required：yes
reason：SSH #1 and SSH #2 exactly-once authority consumed；SSH #2 terminal incomplete and remote live-state verification requires a fresh independent authority。
~~~

## Window report

~~~text
报告名称：Sprint 4 D2-R3 Direct-DD Collector Accepted-fact Deployment
任务名称：Data-first Gate D2-R3 — Deploy the Frozen Collector through Shell-free Archive Transport
执行 Thread：新的独立 Architecture / Integration Thread

结论：HOLD / EXECUTION_CONTRACT_VIOLATION / SSH2_TERMINAL_INCOMPLETE

Live baseline:
- HEAD: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
- origin/main: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
- ahead/behind: 0 / 0
- cached: empty
- protected source: PASS

Architecture reset:
- remote sh/bash -c: 0 explicit invocation
- Python controller: 0
- transport executable: /usr/bin/dd
- deployment executable: /usr/bin/env -i ... /bin/sh -s

Archive:
- generations: 1
- fixed mtime: 1784115110
- local bytes/hash: 163840 / 29947e8c7e3d2c8cbb642a503a37916a4068df8ac4b9cd694aba76871ce3a91d
- entry audit: PASS（26 entries，allowlist exact）
- local cleanup: PASS

Script:
- generations: 1
- bytes/hash: 13885 / 68b10ae866cdf500d69fda14f35c77f3870001a466a3c28c02667f20e56891ba
- sh -n: PASS，invocation 1，exit 0

Transport:
- exact executable: SSH #1 direct /usr/bin/dd; SSH #2 direct /usr/bin/env -i ... /bin/sh -s
- SSH #1 exit: 0
- remote archive bytes/hash: 163840 / 29947e8c7e3d2c8cbb642a503a37916a4068df8ac4b9cd694aba76871ce3a91d（PASS）
- remote cleanup: NOT OBSERVED

Old Collector:
- Id: 5fc9ca04be90a4b61c036f131ae0a5456069ff8b64d5f67748578d1c416f2330
- Image: sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
- Config.Image: edge-mes-demo-collector
- created: 2026-06-19T02:00:56.084936668Z
- status/restart: running / 0

Execution counts:
- SSH transport: 1
- SSH deployment: 1（exit not captured）
- build: 1（PASS）
- normal recreate: 1 invocation（completion not observed）
- rollback retag: 0 observed
- rollback recreate: 0 observed
- DB/API/V-PLC: 0

New Collector:
- Id: NOT REACHED
- Image: NOT REACHED
- Config.Image: NOT REACHED
- status/restart: NOT REACHED
- source hashes: NOT REACHED
- import verification: NOT REACHED

Protected services:
- prestate: PASS（postgres/api/s7-plc-sim/simulator all running, labels matched）
- poststate: NOT REACHED
- comparison: NOT REACHED

Rollback:
- failed / not reached; final live state unknown and not safely claimable

Blockers:
- SSH #2 terminal incomplete immediately after Collector Recreate output; no third SSH or retry permitted

Recommendations:
- PM intake only

Next gate:
- eligible for: new independent deployment authority / PM intake only
- PM approval required before: any live-state re-observation, rollback repair, deployment retry or D3

MVP 路径一致性：
- approved claim: deploy frozen Collector accepted production fact write path before fresh data generation
- minimum invariant: complete post-mutation identity/source/import/protected-state evidence is required before deployment PASS
- new capability/infrastructure: none
- scope drift: none
- classification: MVP-ALIGNED

Thread 输出 / 上下文评估：
- output length: long
- current Thread continue: no
- new Thread required: yes
- reason: exact two-SSH authority consumed; SSH #2 terminal incomplete; new authority required
~~~

## Final Git audit

报告创建后执行最终只读审计：

~~~bash
git status -sb
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git diff --name-only
git diff --cached --name-only
git diff --quiet HEAD -- collector api frontend docker-compose.yml
~~~

最终要求：

~~~text
HEAD == origin/main == 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind：0 / 0
cached：empty
protected source：PASS
target：regular / non-symlink / untracked / unstaged / uncommitted
only task-created repository path：docs/reports/sprint4_d2_r3_direct_dd_collector_accepted_fact_deployment.md
既有 dirty artifacts 与 D1/D2 reports：保持原样
~~~

