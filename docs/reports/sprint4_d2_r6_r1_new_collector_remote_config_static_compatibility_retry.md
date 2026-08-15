# Sprint 4 D2-R6-R1 New Collector Remote-config Static Compatibility Retry

## 报告、任务、Thread、Authority

~~~text
报告名称：
Sprint 4 D2-R6-R1 New Collector Remote-config Static Compatibility Retry

任务名称：
Data-first Gate D2-R6-R1 — Retry the New Collector Remote-config Static Diagnostic without Unfrozen Assertions

执行 Thread：
新的独立 Architecture / Integration Thread

Authority ID：
SPRINT4-D2-R6-R1-REMOTE-CONFIG-STATIC-DIAGNOSTIC-9e0aba2

Authority type：
READ-ONLY / EPHEMERAL STATIC STARTUP DIAGNOSTIC RETRY

Persistent deployment authority：NONE
Compose lifecycle authority：NONE
Active-container lifecycle authority：NONE
Image tag authority：NONE
DB/API/V-PLC authority：NONE
Source/config edit authority：NONE
~~~

本任务只验证新 image 与当前远端 bind-mounted mapping.yaml 的静态 startup compatibility；没有重新激活 Collector。

## D2-R6 intake

原样保留 D2-R6 Thread-local terminal：

~~~text
HOLD / EXECUTION_CONTRACT_VIOLATION / LOCAL_PRESTATE_ASSERTION_DEFECT
~~~

D2-R6 已建立：

~~~text
active safe Collector：MATCHED
old image tag：MATCHED
old and new image objects：EXIST
protected services authority-frozen fields：MATCHED
remote mapping inspection：0
ephemeral docker run：0
remote mutation：0
~~~

D2-R6 准确根因：

~~~text
The diagnostic script incorrectly treated protected-service
Config.Image as a frozen hard-gate field.

Observed PostgreSQL Config.Image：
postgres:16

Incorrect expected value：
postgres
~~~

本次修正：

~~~text
protected-service Config.Image 只捕获并输出；
不与 expected value 比较；
不进入 protected hard-field equality predicate；
不阻止诊断；
不用于声明 protected-service drift。
~~~

不得修改 D2-R6 报告；本报告未修改该文件。

## Required-read and static scope confirmation

已按任务指定顺序读取：

~~~text
docs/thread_handoff/chatgpt_pm_handoff_260723-1244.md
docs/current_status.md Section 0D
docs/current_status.md DB/API/Dashboard Slice 2 write-path summary
docs/roadmap.md Sections 1A、3、5、6、8
docs/thread_handoff/pm_operating_rules.md Sections 12、13、14
docs/reports/sprint4_d2_r3_direct_dd_collector_accepted_fact_deployment.md
docs/reports/sprint4_d2_r4_post_mutation_collector_live_state_recovery.md
docs/reports/sprint4_d2_r5_existing_image_collector_activation.md
docs/reports/sprint4_d2_r6_new_collector_remote_config_compatibility_diagnostic.md
docker-compose.yml Collector service
collector/app/main.py
collector/app/plc/mapping.py
collector/app/services/event_collector.py
collector/app/services/resolved_config_registry.py
collector/app/services/accepted_station_event_fact.py
collector/app/services/storage.py
config/mapping.yaml
~~~

确认的静态边界：

~~~text
Compose Collector 使用 ./config:/app/config:ro；
远端 bind mount source 是 /opt/edge-mes-demo/config；
EventCollectorWorker.__init__() 使用 /app/config/mapping.yaml；
新代码加载 runtime mapping snapshot 并构造 resolved config snapshot；
app.main.main()：未运行；
EventCollectorWorker：未构造；
Storage：未构造；
Snap7 client：未创建；
PostgreSQL/PLC/API/Simulator：未连接；
production fact：未生成。
~~~

## Local Git recovery and hard gate

执行的命令：

~~~bash
cd /Users/chenjie/Documents/MES/edge-mes-demo

git status -sb
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git diff --name-only
git diff --cached --name-only
git diff --quiet HEAD -- collector config api frontend docker-compose.yml
~~~

执行前目标报告 precondition：

~~~text
ABSENT
NON-SYMLINK
UNSTAGED
~~~

执行前 live terminal：

~~~text
branch：main
HEAD：9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
origin/main：9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind：0 / 0
tracked dirty paths：
  .gitignore
  docs/current_status.md
  docs/roadmap.md
  docs/thread_handoff/pm_operating_rules.md
cached：empty
protected source (collector config api frontend docker-compose.yml)：PASS
git diff --quiet protected source：exit 0
target：ABSENT
~~~

既有 untracked reports、handoffs 和 frontend artifacts 保持原样。未执行 restore、clean、stage、commit、push、tag 或任何 source/config 修改。

## Frozen mapping identities

### Current HEAD mapping

~~~text
path：config/mapping.yaml
bytes：7112
SHA-256：d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
Git blob：b46a637f23c761d0a4c3fe048b3b7480a3dec2ce
last change commit：045d21c14436e8fe13a26bc32b7c2956df0cd99f
schema_version：runtime-mapping/v1
config_version：2026.06.26-slice-a
line_id：LINE_001
station count：3
runtime config hash（task-frozen）：0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
~~~

### Known Phase-1 comparison identity

~~~text
bytes：5935
SHA-256：86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3
source commit：54d7d3286c24535f99a02f00e45448ee73d0b895
~~~

Phase-1 identity is comparison-only. No specific historical version was inferred from a remote hash comparison.

## Local diagnostic script gate

只生成一次 repository 外 POSIX script：

~~~text
path：/tmp/edge-mes-d2-r6-r1-remote-config-static.sh
generations：1
first executable statement：set -eu
script bytes：12208
script SHA-256：78ecb8111dcd1c7a4520710579fdf7e5fdafed3ac0b2218dfb1ba464244c3d2f
/bin/sh -n invocations：1
/bin/sh -n exit：0
modified after sh -n：no
deleted before report：yes
~~~

## Frozen active/tag/image prestate

唯一 SSH 在诊断前捕获：

~~~text
ACTIVE_PRE=
5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524|
sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a|
edge-mes-demo-collector|edge-mes-demo|collector|
2026-07-23T12:23:25.124184859Z|
2026-07-23T12:23:25.959624Z|running|0
ACTIVE_PRESTATE=MATCHED

TAG_PRE=
sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a|
linux|arm64|v8|174177688
TAG_PRESTATE=MATCHED_OLD_IMAGE

OLD_IMAGE_PRE=
sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a|
linux|arm64|v8|174177688
OLD_IMAGE_PRESTATE=EXISTS

NEW_IMAGE_PRE=
sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c|
linux|arm64|v8|174329249
NEW_IMAGE_PRESTATE=EXISTS_PLATFORM_MATCHED
~~~

## Protected-service prestate hard-field matrix

每个 protected service prestate 仅 inspect 一次。输出包含完整 9-field tuple；比较只使用 Id、Image、Compose project、Compose service、Created、StartedAt、Status、RestartCount 八个 hard fields。

| Service | Id | Image | Project/service | Created | StartedAt | Status/restart | Hard fields |
| --- | --- | --- | --- | --- | --- | --- | --- |
| edge-mes-postgres | bb3ba0738e692c68b14a62ca64296e484990d3b86b1f6d395c27b200af5cb890 | sha256:f961d097a9cedd37779baef1aab3fe87ef1c63b3b34d361f90a98ea5c9b77e56 | edge-mes-demo/postgres | 2026-06-14T05:57:13.239812435Z | 2026-06-14T05:57:14.263634444Z | running / 0 | MATCHED |
| edge-mes-api | 12e841b4ac33a75c835cee81f0df46e4dbcdb9382b50ca50523f5fad02c57058 | sha256:9f03f370b37fd5fd2ddfd4e4e9e64d4c6b60312910e731157888544371683c11 | edge-mes-demo/api | 2026-07-23T00:32:36.666029032Z | 2026-07-23T00:32:37.955732924Z | running / 0 | MATCHED |
| edge-mes-s7-plc-sim | d21e950b98ae87bbd3ee321074100d0b54b174235ce46df34c5100e1130b785f | sha256:3a28ae38c623d8cb80f775f954315e633b1108112082c37ece698c7562522238 | edge-mes-demo/s7-plc-sim | 2026-06-19T02:05:15.82128338Z | 2026-06-19T02:05:27.378341652Z | running / 0 | MATCHED |
| edge-mes-simulator | 3ebe1e4725af577ac477594afe3046f7e5a197b8162f503ebac036d09b4fcfd5 | sha256:08448d2876c30e9cbbecda4f0ca9a27a5e085a33f14dab2a6d2be3dd06430430 | edge-mes-demo/simulator | 2026-06-14T12:13:00.476282483Z | 2026-06-14T12:13:23.098546695Z | running / 0 | MATCHED |

Diagnostic-only Config.Image values captured but not compared:

~~~text
edge-mes-postgres：postgres:16
edge-mes-api：edge-mes-demo-api
edge-mes-s7-plc-sim：edge-mes-demo-s7-plc-sim
edge-mes-simulator：edge-mes-demo-simulator
~~~

postgres:16 did not block this retry.

## Remote mapping identity

Remote mapping inspection count：1

~~~text
path：/opt/edge-mes-demo/config/mapping.yaml
exists：YES
regular：YES
symlink：NO
realpath：/opt/edge-mes-demo/config/mapping.yaml
bytes：5935
SHA-256：86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3
classification：PHASE1_CONFIG_MATCH
~~~

The remote mapping is not HEAD_CONFIG_MATCH. No file was copied, modified, replaced or deleted.

## SSH terminal

SSH topology used exactly once:

~~~bash
ssh \\
  -T \\
  -o BatchMode=yes \\
  -o IdentitiesOnly=yes \\
  -i /Users/chenjie/.ssh/edge_pi_codex \\
  mari@10.0.0.217 \\
  /usr/bin/env \\
  -i \\
  PATH=/usr/bin:/bin \\
  DOCKER_HOST=unix:///var/run/docker.sock \\
  /bin/sh \\
  -s \\
  < /tmp/edge-mes-d2-r6-r1-remote-config-static.sh
~~~

~~~text
SSH invocation：1
SSH exit：0
outer terminal：complete
second SSH/retry：0
~~~

本次 app terminal 将 SSH stdout/stderr 作为一个 combined terminal 返回；Python traceback 位于该 combined terminal 的 stderr 部分。保留的关键 terminal：

~~~text
D2_R6_R1_PRESTATE=PASS
SOURCE_HASH /app/app/main.py=a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090
SOURCE_HASH /app/app/services/event_collector.py=eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f
SOURCE_HASH /app/app/services/accepted_station_event_fact.py=6545ef67d968ed849be57342ad630b258cd4a09519876efb02955a8c3c6fd911
SOURCE_HASH /app/app/services/storage.py=f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b
DIAGNOSTIC_EXIT=1
EPHEMERAL_RESIDUE=NONE
POSTSTATE=PASS
DIAGNOSTIC_TERMINAL=COMPLETE
STATIC_DIAGNOSTIC=NONZERO
FINAL=DIAGNOSTIC_COMPLETE
~~~

## Single isolated new-image diagnostic

Ephemeral docker run invocation：1

Exact command:

~~~bash
docker run \\
  --rm \\
  --pull=never \\
  --network=none \\
  --read-only \\
  --tmpfs /tmp:rw,nosuid,nodev,noexec,size=4m \\
  --env PYTHONDONTWRITEBYTECODE=1 \\
  --volume /opt/edge-mes-demo/config:/app/config:ro \\
  --entrypoint python \\
  sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c \\
  -c '<fixed static diagnostic code>'
~~~

约束实际满足：

~~~text
network attachment：none
root filesystem：read-only
config mount：read-only
--rm：yes
--pull=never：yes
--name：absent
restart policy：absent
Compose：0
DATABASE_URL/SIMULATOR_URL/SNAP7_HOST：absent
app.main.main()：0
EventCollectorWorker construction：0
Storage construction：0
Snap7 client construction：0
DB/API/PLC/Simulator connection：0
~~~

### Source hashes

四个 source hashes 均与 expected new-image identity MATCHED：

~~~text
/app/app/main.py：
a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090

/app/app/services/event_collector.py：
eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f

/app/app/services/accepted_station_event_fact.py：
6545ef67d968ed849be57342ad630b258cd4a09519876efb02955a8c3c6fd911

/app/app/services/storage.py：
f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b
~~~

### Import and traceback

IMPORTS=PASS 未输出。Import failure 的完整 traceback：

~~~text
Traceback (most recent call last):
  File "<string>", line 14, in <module>
  File "/app/app/main.py", line 6, in <module>
    from app.services.event_detector import EventDetector
  File "/app/app/services/event_detector.py", line 4, in <module>
    from app.services.storage import Storage
  File "/app/app/services/storage.py", line 15, in <module>
    from app.services.accepted_station_event_fact import AcceptedStationEventFact
  File "/app/app/services/accepted_station_event_fact.py", line 7, in <module>
    from app.services.station_event_adapter import AdapterDecision
  File "/app/app/services/station_event_adapter.py", line 7, in <module>
    from common.station_event import (
ModuleNotFoundError: No module named 'common'
~~~

### Mapping/resolved-config diagnostic results

~~~text
mapping load：NOT REACHED
schema_version：NOT REACHED
config_version：NOT REACHED
runtime config hash：NOT REACHED
content-hash result：NOT REACHED
line_id：NOT REACHED
station count：NOT REACHED
resolved-config construction：NOT REACHED
resolved config hash：NOT REACHED
resolved station count：NOT REACHED
STATIC_STARTUP=PASS：NOT REACHED
~~~

The new image source identity matched, but its static import closure failed before any remote mapping or runtime snapshot field was evaluated.

本地只读 Dockerfile observed：

~~~text
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
~~~

This is consistent with the observed container-local absence of importable common, but no source/Dockerfile/image repair was authorized or performed.

## Poststate and residue

~~~text
active Collector poststate：same frozen tuple / UNCHANGED
tag poststate：old image / UNCHANGED
old image poststate：EXISTS / UNCHANGED
new image poststate：EXISTS linux/arm64/v8/174329249 / UNCHANGED
protected services poststate：all eight hard fields UNCHANGED
protected Config.Image：captured again / not compared / non-blocking
ephemeral residue after --rm：NONE
~~~

Post tuples observed：

~~~text
ACTIVE_POST=5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524|sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a|edge-mes-demo-collector|edge-mes-demo|collector|2026-07-23T12:23:25.124184859Z|2026-07-23T12:23:25.959624Z|running|0
TAG_POST=sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a|linux|arm64|v8|174177688
OLD_IMAGE_POST=sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
NEW_IMAGE_POST=sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c|linux|arm64|v8|174329249
PROTECTED_POSTSTATE_HARD_FIELDS=UNCHANGED
~~~

## Terminal classification

严格结论：

~~~text
HOLD / NEW_IMAGE_STATIC_STARTUP_FAILED / IMPORT_PREREQUISITE_FAILED
~~~

说明：

- 新 image source hashes MATCHED；
- isolated diagnostic terminal 完整，docker run exit 1；
- failure 发生在 imports 阶段，明确为 ModuleNotFoundError: No module named common；
- mapping load、runtime mapping content hash 和 resolved-config construction 均未到达；
- remote mapping 是 PHASE1_CONFIG_MATCH，而不是 HEAD_CONFIG_MATCH；
- 因为 imports 没有 PASS，不能满足 REMOTE_CONFIG_RUNTIME_INCOMPATIBILITY_CONFIRMED 的必要条件；
- 因为 static diagnostic 没有 PASS，不能满足 REMOTE_CONFIG_DRIFT_STATICALLY_COMPATIBLE；
- 因为 remote mapping 不是 HEAD，不能把该结果解释成 HEAD mapping 下的 config-specific NEW_IMAGE_STATIC_STARTUP_FAILED；
- 因此本报告使用 image-static import prerequisite HOLD 记录事实，不声明 remote-config incompatibility，也不声明 remote mapping compatibility。

本次没有可用的正向 config root-cause terminal。restart loop 仍未能归因于远端 mapping.yaml。

## Prohibited-action audit

~~~text
SSH：1
second SSH/retry：0
remote mapping inspection：1
remote file mutation：0
ephemeral docker run：1
Docker build：0
Compose：0
active container lifecycle：0
image tag mutation：0
DB query/SQL：0
HTTP/API：0
V-PLC/PLC：0
logs command：0
network attachment：0
production loop/app.main.main()：0
EventCollectorWorker construction：0
Storage construction：0
Snap7 client construction：0
production fact generation：0
source/config edit：0
restore/clean/stage/commit/push/tag：0
~~~

--rm 后 residue 为 NONE；没有执行 cleanup 操作。

## Exactly-once counts

~~~text
SSH：1
remote mapping inspection：1
active Collector pre/post：1 / 1
tag pre/post：1 / 1
old image pre/post：1 / 1
new image pre/post：1 / 1
protected services pre/post：4 / 4
ephemeral docker run：1
Docker build：0
Compose：0
active container lifecycle：0
image tag mutation：0
DB query：0
HTTP/API：0
V-PLC/PLC：0
logs：0
remote file mutation：0
local script generation：1
/bin/sh -n：1，exit 0
~~~

## Blockers

1. New image source identity matched, but the required import closure did not: common.station_event was not importable inside the container.
2. Because imports failed before mapping load, this authority produced no runtime mapping hash, content-hash result or resolved-config result.
3. The remote mapping is a safe regular Phase-1 identity, but the available evidence cannot prove that it caused the restart loop.
4. The supplied terminal matrix has no positive config verdict for the combination “remote mapping is not HEAD and static diagnostic fails before config load”; this report keeps the result as a fail-closed HOLD and does not expand authority.

## Recommendations

~~~text
Do not activate or deploy the new Collector from this evidence.
Do not treat the PHASE1_CONFIG_MATCH hash alone as proof of the D2-R5 restart root cause.
Do not repair source, Dockerfile, image, config or remote deployment under this authority.
A future authority would need to address the image import prerequisite and then
repeat a separately authorized static compatibility diagnostic before any
Collector activation attempt.
~~~

## Next gate

~~~text
D2-R7 exact config/mapping.yaml deployment repair：NOT ELIGIBLE
new Collector activation：NOT ELIGIBLE
runtime logs/D3/DB/API/V-PLC：NOT ELIGIBLE
next action：PM intake and a new independent authority only
~~~

No deployment, configuration repair or activation was performed automatically.

## MVP alignment

~~~text
approved MVP claim：
diagnose the restart loop before another activation attempt

minimum invariant：
remote configuration compatibility must be known before changing the active Collector again

new product capability/infrastructure：none
new threat model/retention/audit platform：none
scope drift：none
classification：MVP-ALIGNED
~~~

This retry directly served the data-first invariant, remained read-only and did not create product capability or infrastructure. The result remains HOLD because the static diagnostic import prerequisite failed before the config contract could be tested.

## Thread/context assessment

~~~text
current Thread continue：no
reason：
the one SSH and one ephemeral docker run authority are consumed;
the diagnostic terminal is complete but inconclusive for remote config;
any further image repair, static retry or activation needs a fresh independent
Architecture / Integration authority.
~~~

## Final Git audit

报告创建后执行：

~~~bash
git status -sb
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git diff --name-only
git diff --cached --name-only
git diff --quiet HEAD -- collector config api frontend docker-compose.yml
~~~

最终审计结果：

~~~text
HEAD：9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
origin/main：9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind：0 / 0
cached：empty
protected source：PASS
tracked dirty paths unchanged：
  .gitignore
  docs/current_status.md
  docs/roadmap.md
  docs/thread_handoff/pm_operating_rules.md
task-created repository path only：
  docs/reports/sprint4_d2_r6_r1_new_collector_remote_config_static_compatibility_retry.md
report：regular / non-symlink / untracked / unstaged / uncommitted
~~~

Final Git audit did not restore or modify any pre-existing dirty artifact.
