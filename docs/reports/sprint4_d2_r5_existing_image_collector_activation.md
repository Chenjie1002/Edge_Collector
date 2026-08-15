# Sprint 4 D2-R5 Existing-image Collector Activation

## 报告、任务、Thread、Authority

~~~text
报告名称：Sprint 4 D2-R5 Existing-image Collector Activation
任务名称：Data-first Gate D2-R5 — Activate the Already-built Collector Image and Verify or Roll Back
执行 Thread：新的独立 Architecture / Integration Thread
Authority ID：SPRINT4-D2-R5-EXISTING-IMAGE-COLLECTOR-ACTIVATION-9e0aba2
Authority type：COLLECTOR-ONLY EXISTING-IMAGE ACTIVATION
Docker build / archive transport / source / DB-schema / V-PLC-PLC / product-data query authority：NONE
~~~

## 结论

~~~text
HOLD / ACTIVATION_VALIDATION_FAILED / ROLLED_BACK
~~~

Preflight、existing-image retag 和唯一 Collector-only recreate 均执行到位。新
Collector 使用了 frozen new image，但 post-inspect 观察到 RestartCount=3，不满足
running / 0 invariant。脚本立即执行且仅执行一次 old-image retag 与 Collector rollback
recreate；rollback inspect 确认 old image、old tag、edge-mes-demo / collector、
running / 0。未声明新 deployment PASS，未生成产品数据，未进入 D3。

## D2-R4 intake and PM operational classification

保留 D2-R4 Thread-local terminal，未修改 D2-R4 报告，也未重新调查 D2-R3 SSH
terminal、archive 或 rollback history：

~~~text
D2-R4:
HOLD / COLLECTOR_RECREATE_PARTIAL_STATE

PM operational classification:
SAFE_OLD_COLLECTOR_ACTIVE / NEW_IMAGE_READY

Current Collector: running on frozen old image
Current container: recreated after D2-R3
Current tag: points to old image
Old image object: exists
D2-R3 new image object: exists
Protected services: unchanged in D2-R4 evidence
Remote D2-R3 archive: absent in D2-R4 evidence
Rollback/equivalent recovery state: operationally established
~~~

## Required-read truth boundary

已按指定顺序读取：

~~~text
docs/thread_handoff/chatgpt_pm_handoff_260723-1244.md
docs/current_status.md Section 0D
docs/current_status.md DB/API/Dashboard Slice 2 DB write path summary
docs/roadmap.md Sections 1A, 3, 5, 6, 8
docs/thread_handoff/pm_operating_rules.md Sections 12, 13, 14
docs/reports/sprint4_d1_r2_existing_accepted_production_fact_db_api_reconciliation.md
docs/reports/sprint4_d2_collector_accepted_fact_write_path_deployment_repair.md
docs/reports/sprint4_d2_r1_collector_accepted_fact_write_path_deployment_retry.md
docs/reports/sprint4_d2_r2_deterministic_collector_accepted_fact_deployment.md
docs/reports/sprint4_d2_r3_direct_dd_collector_accepted_fact_deployment.md
docs/reports/sprint4_d2_r4_post_mutation_collector_live_state_recovery.md
docker-compose.yml Collector service
collector/Dockerfile
collector/app/main.py
collector/app/services/event_collector.py
collector/app/services/accepted_station_event_fact.py
collector/app/services/storage.py
db/migrations/007_accepted_station_event_visibility.sql
~~~

确认：D2-R3 new image provenance 已存在；本 authority 不 build、pull、archive 或
transport。Collector image 用 COPY app ./app 固化源码，Compose 仅挂载
./config:/app/config:ro。accepted fact 与 legacy/current persistence 在同一
Storage.transaction() 中使用 no-commit variants，commit 后才 ACK/read_done；
non-accepted disposition 不写 production_accepted_station_event_fact。

本 authority 没有执行 DB query、SQL write、HTTP/API、V-PLC/PLC、业务函数、测试数据
生成或 logs。

## Local Git recovery and hard gates

~~~text
branch: main
HEAD: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
origin/main: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind: 0 / 0
cached: empty
protected source (collector api frontend docker-compose.yml): PASS
tracked dirty paths preserved:
  .gitignore
  docs/current_status.md
  docs/roadmap.md
  docs/thread_handoff/pm_operating_rules.md
pre-report target: ABSENT / NON-SYMLINK / UNSTAGED / UNCOMMITTED
~~~

所有 pre-existing untracked reports、handoffs 和 frontend artifacts 均保留；未 restore、
clean、stage、commit、push 或修改 source/config/Compose/migration。

## Timeout and local script syntax gate

~~~text
outer tool execution timeout: 180 seconds
SSH wall time: 18.485270958 seconds
shell timeout command: 0
background process: 0
nohup: 0
detached execution: 0

one temporary script: /tmp/edge-mes-d2-r5-activation.sh
script generations: 1
script bytes: 9608
script SHA-256: db5b6afc69a0c141efe2b27fb11485de4adbdce01e6b57f385f25e4de6107607
first executable statement: set -eu
/bin/sh -n invocations: 1
/bin/sh -n exit: 0
modified after sh -n: no
deleted before report: yes
~~~

## SSH and terminal capture

实际唯一 SSH topology：

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
  < /tmp/edge-mes-d2-r5-activation.sh
~~~

~~~text
SSH invocations: 1
remote shell sequence: 1
SSH exit: 1
terminal: complete
second SSH: 0
retry: 0
~~~

The outer tool captured the complete SSH stdout/stderr terminal as one combined stream. The
observed Compose warning lines were:

~~~text
time="2026-07-23T20:23:10+08:00" level=warning msg="Found orphan containers ([edge-mes-dashboard]) for this project."
time="2026-07-23T20:23:25+08:00" level=warning msg="Found orphan containers ([edge-mes-dashboard]) for this project."
~~~

No remove-orphans was executed and Dashboard was not targeted.

## Compose identity and prestate

~~~text
Compose path: /opt/edge-mes-demo/docker-compose.yml
regular: yes
symlink: no
realpath: /opt/edge-mes-demo/docker-compose.yml
SHA-256: a71ab815a34f3c493f38ec572e0cf5892a9a7cdc081d8d3e2e312a380cad9ef0
Compose identity: PASS

Current Collector:
  Id: 90f7ba83914f8e21574f46a3374b824421a9734ca56ddeb518a2a30ed57a5b7a
  Image: sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
  Config.Image: edge-mes-demo-collector
  project/service: edge-mes-demo / collector
  Created: 2026-07-23T11:32:12.386432876Z
  StartedAt: 2026-07-23T11:32:13.22908584Z
  status/restart: running / 0
  result: MATCHED

Old image:
  Id: sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
  exists: yes
  OS/Architecture/Variant/Size: linux / arm64 / v8 / 174177688

New image:
  Id: sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
  exists: yes
  OS/Architecture/Variant/Size: linux / arm64 / v8 / 174329249

Current tag:
  edge-mes-demo-collector -> sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
  OS/Architecture/Variant/Size: linux / arm64 / v8 / 174177688
~~~

## Protected prestate

Each protected service was inspected once before mutation:

| Service | Id | Image | Compose project/service | Created | StartedAt | Restart/status |
| --- | --- | --- | --- | --- | --- | --- |
| edge-mes-postgres | bb3ba0738e692c68b14a62ca64296e484990d3b86b1f6d395c27b200af5cb890 | sha256:f961d097a9cedd37779baef1aab3fe87ef1c63b3b34d361f90a98ea5c9b77e56 | edge-mes-demo/postgres | 2026-06-14T05:57:13.239812435Z | 2026-06-14T05:57:14.263634444Z | 0/running |
| edge-mes-api | 12e841b4ac33a75c835cee81f0df46e4dbcdb9382b50ca50523f5fad02c57058 | sha256:9f03f370b37fd5fd2ddfd4e4e9e64d4c6b60312910e731157888544371683c11 | edge-mes-demo/api | 2026-07-23T00:32:36.666029032Z | 2026-07-23T00:32:37.955732924Z | 0/running |
| edge-mes-s7-plc-sim | d21e950b98ae87bbd3ee321074100d0b54b174235ce46df34c5100e1130b785f | sha256:3a28ae38c623d8cb80f775f954315e633b1108112082c37ece698c7562522238 | edge-mes-demo/s7-plc-sim | 2026-06-19T02:05:15.82128338Z | 2026-06-19T02:05:27.378341652Z | 0/running |
| edge-mes-simulator | 3ebe1e4725af577ac477594afe3046f7e5a197b8162f503ebac036d09b4fcfd5 | sha256:08448d2876c30e9cbbecda4f0ca9a27a5e085a33f14dab2a6d2be3dd06430430 | edge-mes-demo/simulator | 2026-06-14T12:13:00.476282483Z | 2026-06-14T12:13:23.098546695Z | 0/running |
| protected prestate | PASS |  |  |  |  |  |

## Activation

### New tag

唯一正常 retag：

~~~bash
docker image tag \
  sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c \
  edge-mes-demo-collector
~~~

~~~text
new tag retag: 1
new tag post-inspect: 1
tag after retag -> sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
TAG_NEW=PASS
~~~

### Collector-only recreate

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
normal Collector recreate: 1
wait: sleep 3 exactly once
polling: 0
retry: 0
full Compose lifecycle: 0
non-Collector lifecycle: 0
RECREATE_NEW=PASS
~~~

## New Collector verification

~~~text
Id: 92521519e2ef2d9123834a19d4677888c2b37b9b0d017629aad1d21ea1d36af9
Image: sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
Config.Image: edge-mes-demo-collector
project/service: edge-mes-demo / collector
Created: 2026-07-23T12:23:10.896774879Z
StartedAt: 2026-07-23T12:23:24.957031312Z
State.Status: running
RestartCount: 3
~~~

~~~text
.Id different from frozen current Id: PASS
.Image: MATCHED
.Config.Image: MATCHED
.project/service: MATCHED
.State.Status: MATCHED
RestartCount == 0: FAIL (observed 3)
FIRST_FAILED_STEP=NEW_IDENTITY
source-hash verification: 0 / NOT REACHED
import verification: 0 / NOT REACHED
~~~

## Protected poststate

Because NEW_IDENTITY failed first, immediate rollback began before the protected poststate
phase:

~~~text
protected post-inspect: 0
comparison: NOT REACHED
changed fields: not observed by this authority
~~~

No protected-service lifecycle command was issued. This report intentionally does not upgrade
that fact into PROTECTED_POSTSTATE=UNCHANGED.

## Rollback

Rollback was defined before mutation and executed exactly once:

~~~text
ROLLBACK_BEGIN=NEW_IDENTITY
rollback old-image retag: 1
ROLLBACK_RETAG=PASS
rollback Collector recreate: 1
rollback wait: sleep 3 exactly once
rollback Collector inspect: 1
rollback tag inspect: 1
ROLLBACK_INSPECT=PASS
ROLLBACK=PASS
FINAL=HOLD / ACTIVATION_VALIDATION_FAILED / ROLLED_BACK
~~~

Final observed Collector:

~~~text
Id: 5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524
Image: sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
Config.Image: edge-mes-demo-collector
project/service: edge-mes-demo / collector
Created: 2026-07-23T12:23:25.124184859Z
StartedAt: 2026-07-23T12:23:25.959624Z
State.Status: running
RestartCount: 0

Final tag:
edge-mes-demo-collector -> sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
OS/Architecture/Variant/Size: linux / arm64 / v8 / 174177688
~~~

Rollback restored the old Collector/tag invariant. Protected poststate equality was not
independently observed because rollback began before that phase.

## Terminal markers

~~~text
PREFLIGHT=PASS
TAG_NEW=PASS
RECREATE_NEW=PASS
NEW_IDENTITY=FAIL (RestartCount=3)
SOURCE_HASHES=NOT_REACHED
IMPORT=NOT_REACHED
PROTECTED_POSTSTATE=NOT_REACHED
ROLLBACK=PASS
FINAL=HOLD / ACTIVATION_VALIDATION_FAILED / ROLLED_BACK
~~~

## Invocation counts and prohibited-action audit

~~~text
SSH: 1
current Collector pre-inspect: 1
current tag pre-inspect: 1
old image pre-inspect: 1
new image pre-inspect: 1
protected pre-inspect: 4
new-image retag: 1
normal Collector recreate: 1
new Collector post-inspect: 1
new tag post-inspect: 1
source-hash verification: 0
import verification: 0
protected post-inspect: 0
rollback old-image retag: 1
rollback Collector recreate: 1
rollback Collector inspect: 1
rollback tag inspect: 1
normal sleep / rollback sleep: 1 / 1
Docker build/archive: 0 / 0
DB/API/V-PLC: 0
logs/browser/Dashboard: 0
full Compose/non-Collector lifecycle: 0 / 0
pull/buildx/prune/remove-orphans/network/volume mutation: 0
second SSH/retry/second activation: 0
background/detached execution: 0

Prohibited-action audit:
source/test/config/Compose/migration/schema edit: 0
DB/API/V-PLC/data-generation: 0
source transport/archive/build/pull: 0
logs/browser/Dashboard: 0
stage/commit/push/tag/Git cleanup: 0
broad cleanup: 0
~~~

The only remote lifecycle commands were the one normal Collector recreate and the one allowed
rollback Collector recreate. The only repository file created by this authority is this report.

## Blockers

~~~text
Exact blocker: new Collector RestartCount=3; required 0.
Rollback: succeeded for old Collector/tag state.
Protected poststate: not independently observed because rollback began at NEW_IDENTITY.
Product/data defect claim: none.
~~~

## Recommendations

~~~text
PM intake only.
~~~

Do not retry or diagnose with this consumed authority. Any explanation of the restart count,
further live inspection, or a new activation attempt requires a new independent authority.

## Next gate

~~~text
eligible for: PM intake only
PM approval required before: new Collector live-state diagnosis, activation retry or D3
D3: not eligible
~~~

## MVP alignment

~~~text
approved claim: activate the already-built Collector image before fresh production-data validation
minimum invariant: active Collector runs exact frozen source, or old running Collector is restored
new capability/infrastructure: none
scope drift: no
classification: MVP-ALIGNED WITH HOLD
~~~

## Thread/context assessment

~~~text
output length: medium evidence report
current Thread continue: no
new Thread required: yes
reason: sole SSH and activation/rollback sequence consumed; any next action needs a new independent Architecture / Integration authority
~~~

## Final Git audit

Final audit was executed after report creation and temporary script deletion:

~~~text
HEAD == origin/main == 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind: 0 / 0
cached: empty
protected source (collector api frontend docker-compose.yml): PASS
tracked dirty artifacts unchanged:
  .gitignore
  docs/current_status.md
  docs/roadmap.md
  docs/thread_handoff/pm_operating_rules.md
only task-created repository path:
  docs/reports/sprint4_d2_r5_existing_image_collector_activation.md
report: regular / non-symlink / untracked / unstaged / uncommitted
~~~

## Window report

~~~text
报告名称：
Sprint 4 D2-R5 Existing-image Collector Activation

任务名称：
Data-first Gate D2-R5 — Activate the Already-built Collector Image and Verify or Roll Back

执行 Thread：
新的独立 Architecture / Integration Thread

结论：
HOLD / ACTIVATION_VALIDATION_FAILED / ROLLED_BACK

Live baseline:
- HEAD: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
- origin/main: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
- ahead/behind: 0 / 0
- cached: empty
- protected source: PASS

Execution:
- outer timeout: 180 seconds
- script generations: 1
- script bytes/hash: 9608 / db5b6afc69a0c141efe2b27fb11485de4adbdce01e6b57f385f25e4de6107607
- sh -n: 1 / exit 0
- SSH: 1
- SSH exit: 1
- final marker: FINAL=HOLD / ACTIVATION_VALIDATION_FAILED / ROLLED_BACK

Prestate:
- Collector Id/Image: 90f7ba83914f8e21574f46a3374b824421a9734ca56ddeb518a2a30ed57a5b7a / sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
- tag: old image
- old image: exists
- new image: exists, sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c, linux/arm64/v8, 174329249
- protected services: prestate PASS

Activation:
- new tag: PASS
- recreate: PASS
- wait: sleep 3 once

New Collector:
- Id: 92521519e2ef2d9123834a19d4677888c2b37b9b0d017629aad1d21ea1d36af9
- Image: sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
- Config.Image: edge-mes-demo-collector
- project/service: edge-mes-demo / collector
- status/restart: running / 3 — FAIL; required 0
- source hashes: NOT REACHED
- import: NOT REACHED

Protected poststate:
- comparison: NOT REACHED before rollback
- changed fields: not observed

Rollback:
- required: yes, NEW_IDENTITY failed
- retag: PASS, one old-image retag
- recreate: PASS, one Collector-only rollback recreate
- terminal: ROLLBACK=PASS; FINAL=HOLD / ACTIVATION_VALIDATION_FAILED / ROLLED_BACK
- final Collector/tag: old image, old tag, running / 0

Invocation counts:
- build/archive: 0 / 0
- new retag: 1
- normal recreate: 1
- rollback retag: 1
- rollback recreate: 1
- DB/API/V-PLC: 0

Blockers:
- new Collector RestartCount=3; required 0; old state restored by rollback

Recommendations:
- PM intake only

Next gate:
- eligible for: PM intake only
- PM approval required before: new independent Collector diagnosis/activation authority or D3

MVP 路径一致性：
- approved claim: existing-image activation before fresh production-data validation
- minimum invariant: exact frozen new source active, or old running Collector restored
- new capability/infrastructure: none
- scope drift: no
- classification: MVP-ALIGNED WITH HOLD

Thread 输出 / 上下文评估：
- output length: medium
- current Thread continue: no
- new Thread required: yes
- reason: one SSH and one activation/rollback sequence consumed; new authority required
~~
