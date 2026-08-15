# Sprint 4 D2-R6 New Collector Remote-config Compatibility Diagnostic

## 报告、任务、Thread、Authority

~~~text
报告名称：
Sprint 4 D2-R6 New Collector Remote-config Compatibility Diagnostic

任务名称：
Data-first Gate D2-R6 — Diagnose the New Collector Restart Loop
against the Remote Mounted Configuration

执行 Thread：
新的独立 Architecture / Integration Thread

Authority ID：
SPRINT4-D2-R6-NEW-COLLECTOR-CONFIG-COMPATIBILITY-DIAGNOSTIC-9e0aba2

Authority type：
READ-ONLY / EPHEMERAL STATIC STARTUP DIAGNOSTIC

Persistent deployment authority：NONE
Compose lifecycle authority：NONE
Image tag authority：NONE
DB/API/V-PLC authority：NONE
Source/config edit authority：NONE
~~~

本 authority 只允许判断新 Collector image 与当前远端 mounted
mapping.yaml 的静态 startup compatibility；未重新激活 Collector。

## D2-R5 intake and restart-loop interpretation

~~~text
D2-R5:
HOLD / ACTIVATION_VALIDATION_FAILED / ROLLED_BACK

New image:
sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c

New Collector:
running / RestartCount=3 at the single post-inspect

Source/import:
not reached

Rollback:
PASS

Final active Collector:
old image / old tag / running / 0
~~~

按本 authority 的 PM direction，RestartCount=3 作为 restart-loop
evidence 处理，不作为 harmless historical counter。主要待验证假设是：
远端 bind-mounted mapping.yaml stale 或与新 runtime
mapping/config snapshot construction contract 不兼容。

本次执行没有取得 mapping 或 static startup 结果，因此不确认也不排除该假设。

## Required-read boundary

已按指定顺序读取：

~~~text
docs/thread_handoff/chatgpt_pm_handoff_260723-1244.md
docs/current_status.md Section 0D
docs/current_status.md DB/API/Dashboard Slice 2 DB write-path summary
docs/roadmap.md Sections 1A, 3, 5, 6, 8
docs/thread_handoff/pm_operating_rules.md Sections 12, 13, 14
docs/reports/sprint4_d2_r3_direct_dd_collector_accepted_fact_deployment.md
docs/reports/sprint4_d2_r4_post_mutation_collector_live_state_recovery.md
docs/reports/sprint4_d2_r5_existing_image_collector_activation.md
docker-compose.yml Collector service
collector/app/main.py
collector/app/plc/mapping.py
collector/app/services/event_collector.py
collector/app/services/resolved_config_registry.py
collector/app/services/accepted_station_event_fact.py
collector/app/services/storage.py
config/mapping.yaml
~~~

读取确认：

~~~text
Compose Collector service 使用 ./config:/app/config:ro；
远端对应 bind mount 为 /opt/edge-mes-demo/config:/app/config:ro。

EventCollectorWorker.__init__() 使用 /app/config/mapping.yaml；
load_edge_mapping() 构造 RuntimeMappingSnapshot；
新代码随后调用 content_hash_matches() 并构造
build_resolved_config_snapshot_from_mapping(mapping.runtime_snapshot)。

本 authority 没有运行 app.main.main()；
没有构造 EventCollectorWorker；
没有启动 Collector production loop；
没有构造 Storage 或 Snap7 client；
没有连接 PostgreSQL、PLC、API 或 Simulator；
没有写 production fact。
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

执行前目标报告：

~~~text
ABSENT
NON-SYMLINK
UNSTAGED
~~~

Recovery / hard gate terminal：

~~~text
branch: main
HEAD: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
origin/main: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind: 0 / 0
cached: empty
protected source: PASS
git diff --quiet ...: exit 0
~~~

Expected tracked dirty set remained:

~~~text
.gitignore
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
~~~

Existing untracked reports, handoffs and frontend artifacts were preserved.
No restore, clean, stage, commit, push, tag or repository cleanup was run.

## Frozen mapping identities

### Current HEAD mapping

~~~text
path: config/mapping.yaml
bytes: 7112
SHA-256: d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d
Git blob: b46a637f23c761d0a4c3fe048b3b7480a3dec2ce
last change commit: 045d21c14436e8fe13a26bc32b7c2956df0cd99f
~~~

Task-frozen parsed identity：

~~~text
schema_version: runtime-mapping/v1
config_version: 2026.06.26-slice-a
runtime config hash: 0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
stations: 3
~~~

Local live byte/hash/blob/last-change checks matched the frozen values above.

### Known Phase-1 mapping

~~~text
bytes: 5935
SHA-256: 86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3
source commit: 54d7d3286c24535f99a02f00e45448ee73d0b895
~~~

Phase-1 identity was comparison-only. No remote version was inferred from a
hash comparison because remote mapping inspection was not reached.

## Local diagnostic script gate

Repository外只生成一个临时 POSIX script：

~~~text
path: /tmp/edge-mes-d2-r6-remote-config-compat.sh
generations: 1
first executable statement: set -eu
script bytes: 9101
script SHA-256: 28f2d3ab817bbe47ef33903b1c6948e361834ffc16a2db3cb4d06452c50d9eed
/bin/sh -n invocations: 1
/bin/sh -n exit: 0
local diagnostic syntax: PASS
deleted before report: PASS
~~~

## Exactly-once invocation counts

~~~text
SSH: 1
remote mapping inspection: 0 (prestate guard stopped before it)
active Collector pre-inspect / post-inspect: 1 / 0
tag pre-inspect / post-inspect: 1 / 0
old image pre-inspect / post-inspect: 1 / 0
new image pre-inspect / post-inspect: 1 / 0
protected service pre-inspect / post-inspect: 4 / 0
ephemeral docker run: 0

Docker build: 0
Compose: 0
active container lifecycle: 0
image tag mutation: 0
DB query: 0
HTTP/API: 0
V-PLC/PLC: 0
logs: 0
retry / second SSH: 0
~~~

## SSH terminal

使用的唯一 SSH topology：

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
  < "$local_script"
~~~

~~~text
SSH invocation: 1
SSH exit: 1
remote shell: complete through the local prestate assertion failure
second SSH / retry: 0
background / detached execution: 0
~~~

The outer terminal surfaced the following combined stream. The
ASSERTION_FAILED line was emitted by the script on stderr; the preceding
diagnostic lines were emitted on stdout:

~~~text
D2_R6_REMOTE_PRESTATE_BEGIN
ACTIVE_PRE=5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524|sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a|edge-mes-demo-collector|edge-mes-demo|collector|2026-07-23T12:23:25.124184859Z|2026-07-23T12:23:25.959624Z|running|0
ACTIVE_PRESTATE=MATCHED
TAG_PRE=sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a|linux|arm64|v8|174177688
TAG_PRESTATE=MATCHED_OLD_IMAGE
OLD_IMAGE_PRE=sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a|linux|arm64|v8|174177688
OLD_IMAGE_PRESTATE=EXISTS
NEW_IMAGE_PRE=sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c|linux|arm64|v8|174329249
NEW_IMAGE_PRESTATE=EXISTS
PROTECTED_PRE edge-mes-postgres=bb3ba0738e692c68b14a62ca64296e484990d3b86b1f6d395c27b200af5cb890|sha256:f961d097a9cedd37779baef1aab3fe87ef1c63b3b34d361f90a98ea5c9b77e56|postgres:16|edge-mes-demo|postgres|2026-06-14T05:57:13.239812435Z|2026-06-14T05:57:14.263634444Z|running|0
PROTECTED_PRE edge-mes-api=12e841b4ac33a75c835cee81f0df46e4dbcdb9382b50ca50523f5fad02c57058|sha256:9f03f370b37fd5fd2ddfd4e4e9e64d4c6b60312910e731157888544371683c11|edge-mes-demo-api|edge-mes-demo|api|2026-07-23T00:32:36.666029032Z|2026-07-23T00:32:37.955732924Z|running|0
PROTECTED_PRE edge-mes-s7-plc-sim=d21e950b98ae87bbd3ee321074100d0b54b174235ce46df34c5100e1130b785f|sha256:3a28ae38c623d8cb80f775f954315e633b1108112082c37ece698c7562522238|edge-mes-demo-s7-plc-sim|edge-mes-demo|s7-plc-sim|2026-06-19T02:05:15.82128338Z|2026-06-19T02:05:27.378341652Z|running|0
PROTECTED_PRE edge-mes-simulator=3ebe1e4725af577ac477594afe3046f7e5a197b8162f503ebac036d09b4fcfd5|sha256:08448d2876c30e9cbbecda4f0ca9a27a5e085a33f14dab2a6d2be3dd06430430|edge-mes-demo-simulator|edge-mes-demo|simulator|2026-06-14T12:13:00.476282483Z|2026-06-14T12:13:23.098546695Z|running|0
ASSERTION_FAILED field=3 expected=postgres actual=postgres:16
~~~

The protected service's authority-frozen fields were the container identity,
image digest, Compose project/service and running/0 tuple. The observed
postgres:16 is the actual Config.Image label and was not itself a frozen
drift field. The local script incorrectly asserted it as postgres; this
false local guard stopped before mapping inspection and before the isolated
diagnostic. No remote mutation occurred.

## Active Collector, tag and image prestate

The captured active Collector matched the required safe prestate:

~~~text
Id: 5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524
Image: sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
Config.Image: edge-mes-demo-collector
Compose project/service: edge-mes-demo / collector
Created: 2026-07-23T12:23:25.124184859Z
State.StartedAt: 2026-07-23T12:23:25.959624Z
State.Status / RestartCount: running / 0
prestate: MATCHED
~~~

~~~text
tag edge-mes-demo-collector:
sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
OS/Architecture/Variant/Size: linux / arm64 / v8 / 174177688

old image:
exists, sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a

new image:
exists, sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
OS/Architecture/Variant/Size: linux / arm64 / v8 / 174329249
~~~

## Protected service prestate

All four protected services were inspected exactly once. Their authority
frozen fields matched D2-R5 prestate:

| Service | Id | Image | Project/service | Status/restart |
| --- | --- | --- | --- | --- |
| edge-mes-postgres | bb3ba0738e692c68b14a62ca64296e484990d3b86b1f6d395c27b200af5cb890 | sha256:f961d097a9cedd37779baef1aab3fe87ef1c63b3b34d361f90a98ea5c9b77e56 | edge-mes-demo/postgres | running / 0 |
| edge-mes-api | 12e841b4ac33a75c835cee81f0df46e4dbcdb9382b50ca50523f5fad02c57058 | sha256:9f03f370b37fd5fd2ddfd4e4e9e64d4c6b60312910e731157888544371683c11 | edge-mes-demo/api | running / 0 |
| edge-mes-s7-plc-sim | d21e950b98ae87bbd3ee321074100d0b54b174235ce46df34c5100e1130b785f | sha256:3a28ae38c623d8cb80f775f954315e633b1108112082c37ece698c7562522238 | edge-mes-demo/s7-plc-sim | running / 0 |
| edge-mes-simulator | 3ebe1e4725af577ac477594afe3046f7e5a197b8162f503ebac036d09b4fcfd5 | sha256:08448d2876c30e9cbbecda4f0ca9a27a5e085a33f14dab2a6d2be3dd06430430 | edge-mes-demo/simulator | running / 0 |

Protected prestate: MATCHED on authority-frozen fields. Poststate was not
re-inspected because the only SSH stopped before the diagnostic container.

## Remote mapping identity

~~~text
remote mapping inspection: NOT REACHED
path existence/regularity/symlink: NOT OBSERVED
realpath: NOT OBSERVED
bytes/SHA-256: NOT OBSERVED
classification: NOT CLASSIFIED
~~~

The report therefore does not claim HEAD_CONFIG_MATCH, PHASE1_CONFIG_MATCH,
OTHER_CONFIG or UNSAFE_CONFIG_PATH.

## Isolated new-image diagnostic

The fixed command was present in the validated temporary script but was not
invoked because the prestate guard stopped first:

~~~bash
docker run \
  --rm \
  --pull=never \
  --network=none \
  --read-only \
  --tmpfs /tmp:rw,nosuid,nodev,noexec,size=4m \
  --env PYTHONDONTWRITEBYTECODE=1 \
  --volume /opt/edge-mes-demo/config:/app/config:ro \
  --entrypoint python \
  sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c \
  -c '<fixed static diagnostic code>'
~~~

The fixed code would have hashed the four image source files, imported
app.main, app.services.event_collector, app.services.accepted_station_event_fact
and app.services.storage, loaded /app/config/mapping.yaml, printed
schema/config/runtime hash, content-hash match, line/station count, constructed
the resolved config snapshot and printed STATIC_STARTUP=PASS. It did not
instantiate Storage, EventCollectorWorker or a Snap7 client.

Actual results:

~~~text
ephemeral docker run: NOT INVOKED (0)
source hashes: NOT REACHED
imports: NOT REACHED
mapping load: NOT REACHED
content-hash result: NOT REACHED
resolved-config construction: NOT REACHED
STATIC_STARTUP: NOT REACHED
Python traceback: none; Python was never started
~~~

## Poststate and ephemeral cleanup

~~~text
active Collector poststate: NOT REACHED
tag poststate: NOT REACHED
old/new image poststate: NOT REACHED
protected poststate: NOT REACHED
poststate comparison: NOT OBSERVED
diagnostic container residue check: NOT REACHED
ephemeral cleanup: NOT APPLICABLE; no docker run occurred
~~~

No remote file, active container, image tag or protected service was modified
by this authority.

## Terminal classification

~~~text
HOLD / EXECUTION_CONTRACT_VIOLATION
subclassification:
LOCAL_PRESTATE_ASSERTION_DEFECT / DIAGNOSTIC_NOT_EXECUTED
~~~

This is not REMOTE_CONFIG_RUNTIME_INCOMPATIBILITY_CONFIRMED, not
PASS WITH RECOMMENDATIONS / REMOTE_CONFIG_STATIC_COMPATIBILITY_CONFIRMED,
not REMOTE_CONFIG_DRIFT_STATICALLY_COMPATIBLE, and not
NEW_IMAGE_STATIC_STARTUP_FAILED. There is no valid static compatibility
evidence and no valid remote config root-cause inference.

## Prohibited-action audit

~~~text
second SSH / retry: 0
network attachment: 0
DB/API/V-PLC/PLC: 0
Compose: 0
active container lifecycle: 0
image tag mutation: 0
Docker build: 0
logs: 0
remote file mutation: 0
source/config edit: 0
production loop / app.main.main(): 0
Storage construction: 0
EventCollectorWorker construction: 0
Snap7 client construction: 0
production fact generation: 0
stage / commit / push / tag / git clean: 0
~~~

Only the one repository-external script was generated, validated and deleted;
the task report is the only repository path created by this task.

## Blockers

~~~text
1. The one SSH authority was consumed before remote mapping inspection.
2. The validated script contained a local protected-prestate assertion defect:
   it compared the unfrozen Config.Image "postgres" instead of the observed
   "postgres:16".
3. Therefore the single diagnostic container did not run and all compatibility
   terminal fields remain unknown.
~~~

## Recommendations

Do not deploy or activate the new Collector from this evidence. Open a fresh
independent read-only diagnostic authority with a corrected prestate comparator;
the comparator must compare only authority-frozen protected fields. Preserve
the D2-R5 RestartCount=3 as the primary restart-loop evidence and do not
reclassify it as harmless history.

## Next gate

~~~text
This D2-R6 result:
not eligible for D2-R7 config deployment repair
not eligible for new Collector activation
not eligible for D3

Next eligible action:
fresh independent D2-R6 static diagnostic authority, if PM authorizes it.

If a correctly executed fresh diagnostic confirms mapping incompatibility:
D2-R7 — exact config/mapping.yaml deployment repair followed by static
verification; D2-R7 must not activate Collector in the same gate.
~~~

## MVP alignment

~~~text
approved MVP claim:
diagnose the restart loop before another activation attempt

minimum invariant:
remote configuration compatibility must be known before changing the active
Collector again

new product capability or infrastructure:
none

scope assessment:
the requested work remained data-first, read-only and proportional; no
validation platform or product capability was added

classification:
MVP-ALIGNED
~~~

## Thread/context assessment

~~~text
current Thread continue: no
reason:
the sole SSH authority was consumed and the required diagnostic did not run;
any corrected observation requires a fresh independent authority/thread.
~~~

## Final Git audit

The final audit was executed after report creation and temporary script deletion:

~~~bash
git status -sb
git rev-parse HEAD
git rev-parse origin/main
git rev-list --left-right --count HEAD...origin/main
git diff --name-only
git diff --cached --name-only
git diff --quiet HEAD -- collector config api frontend docker-compose.yml
~~~

Final audit result:

~~~text
HEAD == origin/main == 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind: 0 / 0
cached: empty
protected source: PASS
pre-existing tracked dirty paths unchanged:
  .gitignore
  docs/current_status.md
  docs/roadmap.md
  docs/thread_handoff/pm_operating_rules.md
only task-created repository path:
  docs/reports/sprint4_d2_r6_new_collector_remote_config_compatibility_diagnostic.md
report: regular / non-symlink / untracked / unstaged / uncommitted
~~~
