# Sprint 4 D2-R4 Post-mutation Collector Live-state Recovery

## 报告、任务、Thread、Authority

\`\`\`text
报告名称：
Sprint 4 D2-R4 Post-mutation Collector Live-state Recovery

任务名称：
Data-first Gate D2-R4 — Re-establish Collector Deployment State after the Incomplete SSH Terminal

执行 Thread：
新的独立 Architecture / Integration Thread

Authority ID：
SPRINT4-D2-R4-POST-MUTATION-LIVE-STATE-RECOVERY-9e0aba2

Authority type：
READ-ONLY POST-MUTATION STATE RECOVERY

Docker build authority：NONE
Container lifecycle authority：NONE
Rollback authority：NONE
DB/API/V-PLC authority：NONE
\`\`\`

## 结论

\`\`\`text
HOLD / COLLECTOR_RECREATE_PARTIAL_STATE
\`\`\`

Recovery 重新建立了以下 live state：

- Collector 当前存在且 running，但当前 container ID 已不是 D2-R3 old Collector ID；
- 当前 Collector 使用 old image，image tag 也仍指向 old image，而不是 D2-R3 newly built image；
- D2-R3 new image object 仍存在；
- 当前容器内 source hash 与 frozen new source 不一致，accepted-fact module 文件缺失；
- import verification 失败；
- PostgreSQL、API、S7 PLC simulator、simulator 与 D2-R3 protected prestate 精确一致；
- D2-R3 remote archive 当前观察为 ABSENT。

这不是 \`OLD_COLLECTOR_ACTIVE_NEW_IMAGE_READY\`：当前 Collector ID 已变化且 tag 未指向 new image。也不是 deployment confirmed。不得自动 rollback、recreate、retry 或进入 D3。

## D2-R3 intake

D2-R3 thread-local terminal 原样保留：

\`\`\`text
HOLD / EXECUTION_CONTRACT_VIOLATION / SSH2_TERMINAL_INCOMPLETE
\`\`\`

D2-R3 已建立：

\`\`\`text
deterministic archive：PASS
remote archive identity before build：PASS
Compose identity：PASS
old Collector prestate：MATCHED
critical protected prestate：PASS
new image build：PASS
new built image ID：
sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
normal Collector recreate：1 invocation
last visible terminal：
Container edge-mes-collector Recreate
\`\`\`

D2-R3 未建立：

\`\`\`text
Compose recreate completion
current Collector identity
current Collector source hashes
current Collector import result
protected poststate
rollback disposition
remote archive cleanup
SSH #2 exit
\`\`\`

累计 D2-R3 mutation evidence 只作为 intake 保留，不在本 authority 重复或推断：

\`\`\`text
Docker build：1
normal Collector recreate invocation：1
rollback observed：0
DB/API/V-PLC：0
\`\`\`

## PM rollback correction

D2-R3 report 中的 provisional rollback wording 由本 authority 的 PM intake correction 覆盖：

\`\`\`text
rollback：NOT AUTOMATICALLY REQUIRED
rollback eligibility：depends on the newly observed live state
\`\`\`

本次观察到的是 mixed live tuple（new container identity + old image/tag + failed frozen-new source/import validation）。本 authority 没有 rollback authority，也没有执行 rollback。

## Required-read truth boundary

已按任务指定顺序读取：

\`\`\`text
docs/thread_handoff/chatgpt_pm_handoff_260723-1244.md
docs/current_status.md Section 0D
docs/current_status.md DB/API/Dashboard Slice 2 DB write path summary
docs/roadmap.md Sections 1A, 3, 5, 6, 8
docs/thread_handoff/pm_operating_rules.md Sections 12, 13, 14
docs/reports/sprint4_d1_r2_existing_accepted_production_fact_db_api_reconciliation.md
D2, D2-R1, D2-R2 and D2-R3 reports
docker-compose.yml Collector service
collector/Dockerfile
collector/app/main.py
collector/app/services/event_collector.py
collector/app/services/accepted_station_event_fact.py
collector/app/services/storage.py
\`\`\`

读取确认：

- accepted decision 先构造 \`AcceptedStationEventFact\`；
- accepted fact 与 legacy persistence 在同一 \`Storage.transaction()\` 中使用 no-commit writes；
- transaction commit 成功后才进入 ACK/read_done handling；
- non-accepted disposition 不写 accepted production fact；
- Collector image 通过 \`COPY app ./app\` 固化源码，Compose 仅挂载 \`./config:/app/config:ro\`；
- \`production_accepted_station_event_fact\` 是 accepted-only production landing surface；
- 本任务只恢复 live state，不执行 DB query、HTTP/API、V-PLC、PLC request、测试数据生成或业务函数。

## Local Git recovery and hard gates

执行了 authority 指定 recovery commands。

\`\`\`text
branch：main
HEAD：9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
origin/main：9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind：0 / 0
cached：empty
protected source (collector api frontend docker-compose.yml)：PASS
\`\`\`

Recovery 时 tracked dirty set 为：

\`\`\`text
.gitignore
docs/current_status.md
docs/roadmap.md
docs/thread_handoff/pm_operating_rules.md
\`\`\`

这些 dirty artifacts、既有 reports、handoffs 和 frontend generated artifacts 均保持原样。目标报告在 SSH 前为：

\`\`\`text
ABSENT
NON-SYMLINK
UNTRACKED
UNSTAGED
\`\`\`

未执行 restore、clean、stage、commit、push、tag 或 source/config/test/Compose/migration edit。

## Recovery script

\`\`\`text
script generations：1
script bytes：7205
script SHA-256：294a47ef4f998990e6c7db93224bb9054cdca3068b037d1638d4b98fc04ae2c9
first executable statement：set -eu
/bin/sh -n invocations：1
/bin/sh -n exit：0
local script syntax：PASS
script cleanup before report：PASS
\`\`\`

唯一 temporary script 在报告创建前已删除；没有保留其他 repository 外 task script。

## Exact invocation counts

\`\`\`text
SSH：1
Collector container inspect：1
Collector image-tag inspect：1
old image existence inspect：1
new image existence inspect：1
Collector source-hash verification：1
Collector import verification：1
protected-service inspect：4
remote archive inspection：1

Docker build：0
Compose command：0
container lifecycle：0
image tag mutation：0
remote file deletion：0
DB query：0
HTTP/API：0
V-PLC/PLC：0
logs：0
retry / second SSH：0
\`\`\`

## SSH terminal

使用了任务指定的唯一 SSH topology：

\`\`\`bash
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
\`\`\`

\`\`\`text
SSH invocation：1
SSH exit：0
remote shell sequence：1
remote shell terminal：complete
\`\`\`

No second SSH, retry, timeout wrapper, background process, remote sh -c, remote bash -c or Python SSH controller was used.

## Current Collector tuple

\`\`\`text
Id：
90f7ba83914f8e21574f46a3374b824421a9734ca56ddeb518a2a30ed57a5b7a

Image：
sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a

Config.Image：
edge-mes-demo-collector

Compose project/service：
edge-mes-demo / collector

Created：
2026-07-23T11:32:12.386432876Z

State.StartedAt：
2026-07-23T11:32:13.22908584Z

State.Status / RestartCount：
running / 0
\`\`\`

Comparison:

\`\`\`text
current Id == D2-R3 old Collector Id：NO
current Image == frozen old image：YES
current Image == frozen new image：NO
project/service：MATCHED
status/restart：running / 0
\`\`\`

The current identity is fully observed, but it is a mixed state: the container ID is new relative to the old prestate while the image remains old.

## Current image-tag tuple

\`\`\`text
reference：
edge-mes-demo-collector

Id：
sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a

Os / Architecture / Variant：
linux / arm64 / v8

Size：
174177688
\`\`\`

\`\`\`text
expected new tag target：
sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c

observed tag target：
sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a

tag resolves to new image：NO
\`\`\`

## Old/new image existence

\`\`\`text
old image:
sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
inspect invocations：1
inspect exit：0
exists：YES

new image:
sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
inspect invocations：1
inspect exit：0
exists：YES
\`\`\`

No pull, tag, remove or prune was executed.

## Source-hash verification terminal

The single permitted source verification command exited nonzero:

\`\`\`text
command：
docker exec edge-mes-collector sha256sum
  /app/app/main.py
  /app/app/services/event_collector.py
  /app/app/services/accepted_station_event_fact.py
  /app/app/services/storage.py

exit：1
\`\`\`

Observed stdout:

\`\`\`text
a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090  /app/app/main.py
ee1a4267af0633db2b5a8c4163d760bb8d37093b3b84405d14c226f89303184d  /app/app/services/event_collector.py
c620c30641cff25a535cdc067df316ab4c66f73b75f34447898823f60b7396c0  /app/app/services/storage.py
\`\`\`

Observed stderr:

\`\`\`text
sha256sum: /app/app/services/accepted_station_event_fact.py: No such file or directory
\`\`\`

Comparison with frozen new source hashes:

| Path | Observed | Frozen new | Result |
| --- | --- | --- | --- |
| \`/app/app/main.py\` | \`a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090\` | \`a81b5427d682f3ad2678ba81c1a08f61c839fcebef87964db71d44ee18a60090\` | MATCH |
| \`/app/app/services/event_collector.py\` | \`ee1a4267af0633db2b5a8c4163d760bb8d37093b3b84405d14c226f89303184d\` | \`eb647af15e51d32c2af0c2f3defce8e8421f629afd722bd35828253e2718958f\` | MISMATCH |
| \`/app/app/services/accepted_station_event_fact.py\` | absent | \`6545ef67d968ed849be57342ad630b258cd4a09519876efb02955a8c3c6fd911\` | MISSING |
| \`/app/app/services/storage.py\` | \`c620c30641cff25a535cdc067df316ab4c66f73b75f34447898823f60b7396c0\` | \`f3ab8cdc18ec7725a1b863014c698f9cb24f212773b36ead38be7545b2808d0b\` | MISMATCH |

The source terminal is retained as observed evidence; no retry or alternate command was used.

## Import verification terminal

Collector existed and was \`running\`, so the single import verification ran:

\`\`\`text
command：
docker exec edge-mes-collector python -c
'import app.main; import app.services.event_collector; import app.services.accepted_station_event_fact; import app.services.storage'

exit：1
stdout：empty
\`\`\`

stderr:

\`\`\`text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'app.services.accepted_station_event_fact'
\`\`\`

No business function, database call, test or data generation was invoked by the import command.

## Protected-service poststate matrix

The four protected services were each inspected exactly once.

| Service | Id | Image | Compose project/service | Created | StartedAt | RestartCount/status | Comparison |
| --- | --- | --- | --- | --- | --- | --- | --- |
| edge-mes-postgres | \`bb3ba0738e692c68b14a62ca64296e484990d3b86b1f6d395c27b200af5cb890\` | \`sha256:f961d097a9cedd37779baef1aab3fe87ef1c63b3b34d361f90a98ea5c9b77e56\` | \`edge-mes-demo / postgres\` | \`2026-06-14T05:57:13.239812435Z\` | \`2026-06-14T05:57:14.263634444Z\` | \`0 / running\` | UNCHANGED |
| edge-mes-api | \`12e841b4ac33a75c835cee81f0df46e4dbcdb9382b50ca50523f5fad02c57058\` | \`sha256:9f03f370b37fd5fd2ddfd4e4e9e64d4c6b60312910e731157888544371683c11\` | \`edge-mes-demo / api\` | \`2026-07-23T00:32:36.666029032Z\` | \`2026-07-23T00:32:37.955732924Z\` | \`0 / running\` | UNCHANGED |
| edge-mes-s7-plc-sim | \`d21e950b98ae87bbd3ee321074100d0b54b174235ce46df34c5100e1130b785f\` | \`sha256:3a28ae38c623d8cb80f775f954315e633b1108112082c37ece698c7562522238\` | \`edge-mes-demo / s7-plc-sim\` | \`2026-06-19T02:05:15.82128338Z\` | \`2026-06-19T02:05:27.378341652Z\` | \`0 / running\` | UNCHANGED |
| edge-mes-simulator | \`3ebe1e4725af577ac477594afe3046f7e5a197b8162f503ebac036d09b4fcfd5\` | \`sha256:08448d2876c30e9cbbecda4f0ca9a27a5e085a33f14dab2a6d2be3dd06430430\` | \`edge-mes-demo / simulator\` | \`2026-06-14T12:13:00.476282483Z\` | \`2026-06-14T12:13:23.098546695Z\` | \`0 / running\` | UNCHANGED |
\`\`\`

Changed fields: none observed.

## Remote archive state

\`\`\`text
path：
/tmp/edge-mes-collector-9e0aba2-d2r3.tar

state：ABSENT
bytes：N/A
SHA-256：N/A
remote archive cleanup：not executed by D2-R4
cleanup debt：none asserted beyond observed absence
\`\`\`

The archive inspection was one read-only inspection. No remote file was deleted or modified. The observed absence does not establish a cleanup history claim.

## Terminal classification

\`\`\`text
HOLD / COLLECTOR_RECREATE_PARTIAL_STATE
\`\`\`

Reason:

- the active Collector exists and is running;
- its ID differs from the D2-R3 old Collector ID;
- its image and tag are old, not the frozen new image;
- the new image object exists but is not active through the observed tag;
- frozen-new source verification failed and import verification failed;
- protected services are unchanged;
- the observed tuple is neither a confirmed new deployment nor the defined old-active/new-ready state.

No product defect, data-generation result or rollback outcome is inferred.

## Prohibited-action audit

\`\`\`text
second SSH / retry：0
Docker build：0
Compose command：0
Collector/protected lifecycle：0
image tag mutation / pull / remove / prune：0
remote archive deletion or modification：0
DB query / SQL write / migration：0
HTTP/API/Dashboard：0
V-PLC/PLC request or mutation：0
logs / browser / data generation：0
source/config/test/Compose edit：0
stage / commit / push / tag / git clean：0
\`\`\`

Authorized local cleanup only:

\`\`\`text
D2-R4 temporary script cleanup：1
repository report creation：1
\`\`\`

No other repository path was modified.

## Blockers

Exact blocker:

\`\`\`text
The observed live tuple is mixed and does not satisfy either
NEW_DEPLOYMENT_CONFIRMED or OLD_COLLECTOR_ACTIVE_NEW_IMAGE_READY.
Current Collector source/import validation also fails:
accepted_station_event_fact.py is absent and import exits 1.
\`\`\`

This is a live-state classification blocker, not a product defect claim. The task intentionally does not repair it.

## Recommendations

\`\`\`text
PM intake only.
\`\`\`

PM should adjudicate the observed mixed state before authorizing any lifecycle action. No automatic rollback is recommended or executed by this authority.

## Next gate

\`\`\`text
eligible for：
PM intake only

not eligible for：
D2-R5 OLD_COLLECTOR_ACTIVE_NEW_IMAGE_READY path
D3 controlled fresh accepted-result generation
rollback or Collector recreate under this authority

PM approval required before：
a new independent Collector-only lifecycle/rollback authority,
any deployment retry,
D3 controlled fresh accepted-result generation,
DB/API reconciliation or V-PLC action
\`\`\`

D3 requires a separate independent authority and a confirmed active Collector deployment.

## MVP 路径一致性

\`\`\`text
approved claim：
establish the actual deployed Collector state before rollback, retry or data generation

minimum invariant：
no post-mutation repair is authorized until the active container, image,
source and protected-service state are known

new capability/infrastructure：none
scope drift：none
classification：MVP-ALIGNED
\`\`\`

This recovery directly supports the data-first MVP path. It does not add a product capability, evidence platform, infrastructure layer, DB/API surface or runtime topology.

## Thread 输出 / 上下文评估

\`\`\`text
output length：long evidence report
current Thread continue：no
new Thread required：yes
reason：
the single D2-R4 SSH authority is consumed; any lifecycle, rollback,
retry or D3 work requires a fresh independent authority
\`\`\`

## Window report

\`\`\`text
报告名称：
Sprint 4 D2-R4 Post-mutation Collector Live-state Recovery

任务名称：
Data-first Gate D2-R4 — Re-establish Collector Deployment State after the Incomplete SSH Terminal

执行 Thread：
新的独立 Architecture / Integration Thread

结论：
HOLD / COLLECTOR_RECREATE_PARTIAL_STATE

Live baseline:
- HEAD: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
- origin/main: 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
- ahead/behind: 0 / 0
- cached: empty
- protected source: PASS

Recovery script:
- generations: 1
- bytes/hash: 7205 / 294a47ef4f998990e6c7db93224bb9054cdca3068b037d1638d4b98fc04ae2c9
- sh -n: invocation 1 / exit 0

Invocation counts:
- SSH: 1
- Collector inspect: 1
- tag inspect: 1
- old/new image inspect: 1 / 1
- source verification: 1
- import verification: 1
- protected-service inspect: 4
- archive inspect: 1
- build/Compose/lifecycle: 0
- DB/API/V-PLC: 0

Collector:
- Id: 90f7ba83914f8e21574f46a3374b824421a9734ca56ddeb518a2a30ed57a5b7a
- Image: sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a
- Config.Image: edge-mes-demo-collector
- project/service: edge-mes-demo / collector
- Created: 2026-07-23T11:32:12.386432876Z
- StartedAt: 2026-07-23T11:32:13.22908584Z
- status/restart: running / 0

Images:
- tag target: observed old sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a; expected new sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c
- old image exists: YES
- new image exists: YES

Source/import:
- source hashes: main MATCH; event_collector MISMATCH; accepted_station_event_fact MISSING; storage MISMATCH
- source command exit: 1
- import exit: 1
- import stderr: ModuleNotFoundError: No module named 'app.services.accepted_station_event_fact'

Protected services:
- comparison: UNCHANGED for all four services
- changed fields: none

Remote archive:
- state: ABSENT
- bytes/hash: N/A / N/A
- cleanup debt: none asserted beyond observed absence

Blockers:
- mixed active Collector tuple is neither confirmed new deployment nor old-active/new-ready; frozen-new source/import validation fails

Recommendations:
- PM intake only

Next gate:
- eligible for: PM intake only
- PM approval required before: new independent Collector lifecycle/rollback/retry authority or D3

MVP 路径一致性：
- approved claim: actual deployed Collector state is established before rollback, retry or data generation
- minimum invariant: active container, image, source and protected-service state must be known before post-mutation repair
- new capability/infrastructure: none
- scope drift: none
- classification: MVP-ALIGNED

Thread 输出 / 上下文评估：
- output length: long evidence report
- current Thread continue: no
- new Thread required: yes
- reason: one SSH authority consumed; any next mutation or D3 requires a new independent authority
\`\`\`

## Final Git audit

The final audit was executed after report creation using the authority-specified commands.

\`\`\`text
HEAD == origin/main == 9e0aba2ec7b4e1e15e1d3eedda129b4ea9d74148
ahead / behind：0 / 0
cached：empty
protected source (collector api frontend docker-compose.yml)：PASS
tracked dirty artifacts：unchanged
target：
docs/reports/sprint4_d2_r4_post_mutation_collector_live_state_recovery.md
target：regular / non-symlink / untracked / unstaged / uncommitted
only task-created repository path：target report
既有 reports 和 dirty artifacts：保持原样
\`\`\`

