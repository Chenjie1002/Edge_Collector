# Sprint 4 D2-R7B-T0 Accepted Local-Image Transport Planning Report

结论：`PASS WITH RECOMMENDATIONS`

## 1. Report identity and authority boundary

- 报告名称：`Sprint 4 D2-R7B T0 Accepted Local-Image Transport Planning Report`
- 任务名称：`D2-R7B-T0 — Accepted Local-Image Transport Planning`
- Authority ID：`PM-D2-R7B-T0-ACCEPTED-LOCAL-IMAGE-TRANSPORT-PLANNING-260801-1504`
- Executing Thread：`Architecture / Integration`
- Report delivery mode：`REPOSITORY_DURABLE_REPORT`
- Exact report path：`docs/reports/sprint4_d2_r7b_t0_accepted_local_image_transport_plan.md`
- Exact artifact paths for T0：`none`
- Docs write authority：仅限上述 exact report path；Git stage/commit/push/tag 均未授权。

本报告只冻结最小 identity/transport contract。T0 仅建立 `TRANSPORT PLAN WRITTEN = YES`，
不建立 PM acceptance 或任何 A0+ truth，亦不授权 A0 及其后的 Gate。

最终 report bytes/SHA-256 由窗口 manifest 记录；不嵌入 self-hash。
T0 不创建 archive/checksum/JSON/helper/staging/extraction root/log/second report。

## 2. Fresh authority and live baseline

### 2.1 Task-file launcher identity

已先读取本 task file 至 EOF（658 行），并核验：

```text
path        = docs/thread_handoff/pm_task_20260801T0704Z_d2_r7b_t0_accepted_local_image_transport_planning.md
type        = regular file
symlink     = no
bytes       = 27120
SHA-256     = 07aae9bded474e3b6d5942e0e6516aa13d9e70e8d3ceab3014692b39b1e0c2c3
git status  = ?? <exact task path> (one membership)
indexed     = no
ignored     = no
unstaged    = no (untracked, not staged)
```

`git check-ignore` 与 exact-path index 查询均无结果；identity mismatch 为 terminal
`HOLD / TASK_FILE_LAUNCHER_IDENTITY_OR_AUTHORITY_MISMATCH`。

### 2.2 Fresh Git recovery before this write

```text
repository   = /Users/chenjie/Documents/MES/edge-mes-demo
branch       = main
HEAD         = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
origin/main  = 0bbfef9f787515a7f8f0a8f1709492d6f1e47b8c
ahead/behind = 0/0
git status -sb header = ## main...origin/main
tracked diff = docs/thread_handoff/pm_operating_rules.md only
cached diff  = empty
git diff --check = PASS
git diff --cached --check = PASS
status entries = 337 total / 336 untracked
exact report path before write = ABSENT
report parent docs/reports = EXISTS
```

PM Rules、dispatched task file 与其它 untracked paths 是 external state；未改动、staged、cleaned
或吸收。最终 changed/created set 排除它们，仅含 exact report path。

### 2.3 Allowed fresh Docker observations

The only Docker observations in this T0 were exactly one `/opt/homebrew/bin/docker context show`
and exactly one exact-candidate image inspect. Context returned `colima`, exit `0`. The inspect
returned exit `0` and matched:

```text
Id / image digest = sha256:8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013
Os                = linux
Architecture      = arm64
WorkingDir        = /app
Cmd               = ["python", "-m", "app.main"]
RepoTags          = [] (descriptive only; not authority)
RepoDigests       = [] (descriptive only; not authority)
```

Fresh ordered RootFS `diff_ids` (9 layers), which later A0/L0 must bind without reordering:

```text
1  sha256:4e6fee325600a0377566ca159a4da9833f6e35e04eaa4194c47dd3b2fe901717
2  sha256:1f6945ab3a1b6c4a2410d7a0a7384e91af9b5356cdbd63d725454651b14b2818
3  sha256:92e43e3934d11abe153198ffb0401027d24a6aa365d456f65b8c070caef41156
4  sha256:f52241bd08541c775533109caf6be52a9160f5000537b8dd0148bbce15dee151
5  sha256:ef8089cf4be9aa3c8fd9f8beb2b7806ad039dcad6a4f5ffb371557745839c22d
6  sha256:07e28daf7c3c9afe211a27c78de2376e316915ffebd9d60fd049f846b44dc949
7  sha256:ae135f728d53b2ddba4892270efe8d569b62083fbad619ddb338f1c3cf68ed4e
8  sha256:4cf702a8b1bd12ece59b57059476250644d15babebf65b7c0f44284cc66bb75b
9  sha256:f57ebb371247880c6d5182b83abe8767cdc8505fba3a717c82f04d8313632d16
```

No build/buildx/save/export/tag/pull/load/container/image mutation、network/SSH/SCP/rsync 或
host control-plane Python was run。

## 3. Claim, phase model and non-inheritance

Claim under planning:

> Produce a Docker image archive from the accepted local full image ID, prove that the archive contains that exact image, transfer the exact accepted archive bytes to the verified Raspberry Pi target, and load a remote Docker object whose full image ID and immutable config/RootFS identity match the accepted local candidate.

Frozen phase sequence:

```text
T0  Accepted Local-Image Transport Planning
A0  Local Archive Generation and Acceptance
R0  Remote Target Read-Only Preflight
T1  Archive Transport and Integrity Acceptance
L0  Remote Docker Load and Exact Object Identity Acceptance
C0  Deployment / Config Compatibility Read-Only Preflight
D0  Deployment Execution
B0  Pre-Activation Rollback Readiness
A1  Activation / Restart
R1  Runtime-Loaded Validation
P0  Production-Fact Validation
B1  Rollback Drill / Rollback Acceptance
C1  Final D2-R7B Closeout and Status Sync
```

There is no automatic authority inheritance. A failed phase does not consume the next phase. A
tag, filename, archive, remote file, remote image, service or runtime cannot inherit acceptance
from the accepted local full image ID, source commit, history or command output.

## 4. Frozen local candidate identity

```text
Git product-source commit = 934ced7b9659cb566628b1709cf6d73463a534d8
accepted local image ID   = sha256:8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013
platform                  = linux/arm64
Docker context            = colima
image Config identity     = Docker inspect Id/Descriptor digest above; A0 must hash Config JSON
WorkingDir                = /app
Cmd                       = ["python", "-m", "app.main"]
```

The full candidate ID is the sole archive input authority. It must never be shortened and no tag
may be substituted. The fresh inspect also showed the exact ordered RootFS list in Section 2.3.
The product-source Git SHA, ordinary file SHA-256, OCI/image digest, config JSON SHA-256 and
archive SHA-256 are different evidence fields and must not be conflated.

## 5. A0 local archive format, paths and publication contract

### 5.1 Exact proposed paths (future A0 only)

以下均为 future A0 proposal、非 T0 write authority；都在 Git checkout 外且必须同一 filesystem：

```text
local parent:
/Users/chenjie/Documents/MES/edge-mes-transport/d2-r7b-t0

temporary archive:
/Users/chenjie/Documents/MES/edge-mes-transport/d2-r7b-t0/.accepted-local-image-8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013.tar.tmp

final accepted archive:
/Users/chenjie/Documents/MES/edge-mes-transport/d2-r7b-t0/accepted-local-image-8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013.tar

future A0 report:
/Users/chenjie/Documents/MES/edge-mes-transport/d2-r7b-t0/a0_archive_acceptance.md

future A0 bounded JSON (only if required for independent review):
/Users/chenjie/Documents/MES/edge-mes-transport/d2-r7b-t0/a0_archive_acceptance.json
```

Parent 必须已存在为 non-symlink directory，由授权用户拥有且可 search/write；A0 检查 parent、
device、ownership、两路径 initial absence 与 final collision，但不创建/修复 parent。路径仅在
独立 A0 创建后属于 task-owned；禁止 broad cleanup。

### 5.2 One archive mechanism and state transitions

The only allowed future mechanism is Docker image-save TAR, using the full ID directly:

```text
/opt/homebrew/bin/docker image save --output <exact-temporary-archive-path> sha256:8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013
```

A0 command budget 是 read-only preconditions 后 exactly one `docker image save`；禁止 alias、
export、build/buildx/pull/tag/load/fallback。temp/final 必须 mode `0600`、one-link、regular、
non-symlink；restrictive umask，mode/ownership drift、overwrite 均 HOLD。

Save 只写 exact temp。验证后记录 temp bytes/lowercase SHA-256，并用同 filesystem、no-replace、
atomic publication（如 verified `renameat2(RENAME_NOREPLACE)`；禁止 `os.replace`/overwrite）到
final；再 re-stat/re-hash，要求 bytes/SHA 相等，成功后保留 final、temp absent。collision、
race、rename failure 或 post-publication mismatch 均 terminal HOLD。

At T0 only:

```text
ARCHIVE BYTES    = TO BE MEASURED IN A0
ARCHIVE SHA256   = TO BE MEASURED IN A0
ARCHIVE ACCEPTED = NO
```

### 5.3 A0 deterministic archive identity acceptance

Future A0 must use the frozen host control-plane runtime from PM Rules Section 10 for TAR/JSON/
hash validation:

```text
formula          = homebrew/core/python@3.14
formula version  = 3.14.6
entrypoint       = /opt/homebrew/opt/python@3.14/bin/python3.14
resolved target  = /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14
version          = Python 3.14.6
architecture     = arm64
resolved bytes   = 52448
resolved SHA-256 = b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf
```

Before A0 write，该 interpreter 必须通过 executable/link/bytes/hash 及 `tarfile`、safe members、
`pathlib`、UTF-8 JSON、`hashlib.sha256`、`os.lstat`/`stat`、atomic no-replace primitive smoke。
其它 interpreter/PATH 禁止；T0 未运行 Python/validator。

The A0 validator must, without extracting the archive:

1. require archive regular/non-symlink/one-link identity, exact bytes and lowercase SHA-256;
2. audit every outer TAR member: safe normalized POSIX names only; reject absolute/`..` path,
   duplicate name, device/FIFO, symlink, hardlink or unsupported link. Identity members regular；
   no extraction root is authorized, and extraction outside a task-owned root is HOLD;
3. parse exactly one `manifest.json` image entry and never depend on `RepoTags`;
4. require one exact regular Config JSON member named by the manifest, and require SHA-256 of its
   raw JSON bytes to equal the accepted image ID suffix, with no `sha256:` prefix mismatch;
5. require Config `os=linux`, `architecture=arm64`, `config.WorkingDir=/app`,
   `config.Cmd=["python","-m","app.main"]`, `rootfs.type=layers`, and the exact ordered 9
   `rootfs.diff_ids` from Section 2.3;
6. require manifest layer count/order to equal RootFS；hash each raw outer `layer.tar` member and
   require equality to `RootFS.diff_ids[i]`; tag/name-only checks are not PASS；
7. re-check temp, publish no-replace, re-check final bytes/SHA；separate Git SHA, image/config
   digest and archive SHA-256 in evidence。

Only after all seven checks may A0 report `ARCHIVE ACCEPTED = YES`. Actual archive bytes and hash
remain unmeasured at T0. SBOM, signing, registry, generic supply-chain, anti-tamper, forensics
and long-term retention subsystems are out of scope.

## 6. R0 remote target read-only preflight

`10.0.0.217` is historical locator hint；`/opt/edge-mes-demo` is only deployment-root expectation。
Future R0 must receive Owner/PM-bound current SSH config alias/user；missing exact locator is HOLD，
not a historical inference。

Frozen connection shape and host-key policy (one SSH invocation total):

```text
/usr/bin/ssh -F /Users/chenjie/.ssh/config \
  -o BatchMode=yes -o ControlMaster=no \
  -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile=/Users/chenjie/.ssh/known_hosts \
  -o ConnectTimeout=10 -o ConnectionAttempts=1 \
  <owner-bound-user>@<owner-bound-current-ssh-host> -- /bin/sh -c <fixed-read-only-probe>
```

Placeholders are mandatory future inputs, never defaults。Options bind to the exact config/known-hosts
paths；unknown/missing/mismatched key、prompt、timeout、nonzero exit or identity drift fail closed。
Call consumption 后不得 retry 或换 IP。

Fixed read-only probe records hostname、machine-id/stable identity、kernel/`linux/arm64`、user、
Docker client/server/daemon、deployment-root/staging-parent lstat、device、ownership/permissions
及 `df` bytes。Required free bytes：

```text
accepted A0 archive bytes + max(512 MiB, ceil(10% of accepted A0 archive bytes))
```

Probe 还 observes full IDs/RepoTags、exact candidate full-ID inspect，以及唯一 current Collector
service/container 的 ID/name/image/labels/state/restart/mount/network/deployment identity。零或
多重 ambiguous match 均 HOLD；tags descriptive only。

R0 zero remote writes：禁止 `mkdir`/upload/`dd`/`mv`/`rm`、load/tag、Compose/config、restart、
activation、lifecycle、cleanup。R0 PASS 只建立 `REMOTE TARGET VERIFIED = YES`，不建立 transport
或 remote image acceptance。

## 7. T1 staging and transport contract

Proposed exact remote staging paths, under a bounded location distinct from active deployment files:

```text
remote staging parent:
/opt/edge-mes-demo/.transport/d2-r7b-t0

remote temporary:
/opt/edge-mes-demo/.transport/d2-r7b-t0/accepted-local-image-8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013.tar.uploading

remote final:
/opt/edge-mes-demo/.transport/d2-r7b-t0/accepted-local-image-8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013.tar
```

R0 必须观察 parent 已存在、non-symlink、verified user 可写/搜索且与 active files 分离，并检查
两路径 absent、device。R0/T1 不创建 parent；collision、foreign inode、owner/device/space 错误 HOLD。

One transport mechanism is frozen: an SSH byte stream from the accepted local final archive into
remote Linux `dd` with exclusive creation, not SCP/rsync/SFTP:

```text
/usr/bin/ssh <same exact R0 options> <verified-r0-target> -- \
  /bin/dd of=<exact-remote-temporary> bs=1048576 conv=excl status=none
```

stdin 仅来自已 recheck regular/non-symlink/one-link、bytes/SHA 的 A0 final；`conv=excl` 防覆盖。
T1 exactly two SSH calls：stream 后 verify/publish；后者校验 type/link/device、bytes/SHA，以
same-filesystem no-replace `mv -n`（或 verified equivalent）发布，要求 temp absent 并 recheck
final。`mv -n` 不可用、skip 或无法证明 no-overwrite 均 HOLD。

Interruption、stream/hash failure、parent/path race 或 post-rename mismatch terminalize T1；不得
retry，必须 new attempt ID/authority。T1 不删除任何 remote object；cleanup 需 separate exact-object
Gate 证明 path/inode ownership。禁止 remote load/tag/deployment/activation/lifecycle/config mutation。

T1 PASS may establish only:

```text
TRANSPORTED = YES
REMOTE STAGED ARCHIVE ACCEPTED = YES
```

It cannot establish `REMOTE LOADED OBJECT`, `DEPLOYED` or any later state. Proposed T1 local
durable paths (future task only) are the matching `t1_archive_transport_acceptance.md` and one
bounded `t1_archive_transport_acceptance.json` under the Section 5 parent.

## 8. L0 remote Docker load and exact object identity

L0 只消费 T1-accepted final archive 与 PASS R0 identity；one SSH invocation 内含 pre-load exact-ID
inspect、one load、post-load exact-ID inspect；remote Docker mutation exactly one：

```text
/usr/bin/docker image load --input /opt/edge-mes-demo/.transport/d2-r7b-t0/accepted-local-image-8008cacf46229f5465bb71013db0177696b08b9307d56fcb30512d0670f2f013.tar
```

Before load recheck final bytes/SHA/path。若 exact candidate 已存在，L0 inspect immutable identity，
不覆盖并 terminalize
`HOLD / PRE_EXISTING_EXACT_IMAGE_REQUIRES_EXPLICIT_REUSE_AUTHORITY`. A Docker inspect error other
than a proven absent-image result is also HOLD.

After load 以 full candidate ID 做 `docker image inspect`，不使用 tag/output。PASS 要求 full ID、
`linux/arm64`、Config、WorkingDir/Cmd、ordered RootFS 全等。tags 仅 diagnostic；禁止 `docker tag`。
unexpected ID、mismatch、partial/ambiguous object 均 HOLD，foreign/ambiguous 不删除。

L0 不做 Compose/config、deployment、restart、activation、runtime、production 或 cleanup。local
final 与 remote final 保留；删除需 separate exact-object authority。L0 PASS 只可建立：

```text
REMOTE IMAGE ACCEPTED = YES
REMOTE LOADED OBJECT  = YES
```

Proposed L0 local durable paths (future task only) are `l0_remote_load_identity_acceptance.md` and
one bounded `l0_remote_load_identity_acceptance.json` under the Section 5 parent.

## 9. Phase matrix and later separation

| Gate | Sole possible claim | Explicitly not inherited |
|---|---|---|
| T0 | `TRANSPORT PLAN WRITTEN = YES` | all A0+ claims; PM acceptance |
| A0 | `ARCHIVE ACCEPTED = YES` | remote target, transport, load, deployment |
| R0 | `REMOTE TARGET VERIFIED = YES` | upload, transport, image/load, deployment |
| T1 | `TRANSPORTED = YES`; `REMOTE STAGED ARCHIVE ACCEPTED = YES` | remote loaded object and all lifecycle claims |
| L0 | `REMOTE IMAGE ACCEPTED = YES`; `REMOTE LOADED OBJECT = YES` | deployment, activation, runtime, production, rollback |
| C0 | read-only config/compatibility PASS | deployment or activation |
| D0 | separately accepted deployment only; does not activate | activation, runtime, production |
| B0 | pre-activation rollback readiness | activation or rollback drill |
| A1 | separately accepted activation/restart | runtime-loaded or production |
| R1 | runtime-loaded validation | production-fact or rollback acceptance |
| P0 | production-fact validation | rollback drill/closeout |
| B1 | rollback drill/rollback acceptance | final closeout unless explicitly accepted |
| C1 | explicit final status sync plus PM acceptance | none inferred from written commands |

C0 is read-only. D0 must not activate. B0 must close before A1. A1 and R1 are separate. P0 and
B1 are separate from runtime acceptance; a written rollback command is not a rollback drill. All
later work preserves PLC/HMI control authority and the Edge read-only collection boundary.

## 10. Failure, retry, cleanup and attempt identity

Each future A0/R0/T1/L0 receives new Owner-bound ID
`d2-r7b-t0-<gate>-<UTC RFC3339 minute>-<unique nonce>`，写入 report/JSON/command ledger/object
decision；无 default/reuse/fallback。T0 Authority ID 不是 execution attempt。

| Gate | Terminal HOLD examples | Retry/cleanup boundary | Next authority |
|---|---|---|---|
| A0 | context/ID drift, parent collision, save failure, TAR/config/layer mismatch, publication race | no retry; retain ambiguous task-owned temp for separate exact cleanup; never overwrite/clean foreign path | none; PM issues new A0 only |
| R0 | host-key/identity drift, daemon failure, non-arm64 target, path collision, low space, ambiguous Collector | zero writes; no retry after one SSH call; no cleanup | none; new R0 authority |
| T1 | stream/SSH failure, bytes/SHA mismatch, no-replace failure, interruption | retain exact partial/foreign-ambiguous object; no same-Gate delete; new attempt ID plus cleanup authority if needed | none; new T1 authority |
| L0 | pre-existing exact image, load failure, post-load ID/config/RootFS mismatch, unexpected object | no image removal/tag cleanup; retain archive/object for review; separate exact-object cleanup | none; new L0 authority |

All phases fixed-budget、fail-closed、无 fallback/ predecessor reuse；无 global Docker/image/container/
filesystem cleanup。失败 phase 不消费 next phase；evidence/accepted archives 保留至 separate cleanup
decision。

## 11. Durable evidence contract

Each future Gate may use one concise report plus one bounded JSON only when needed；T0 creates neither。
Common fields：schema/authority/attempt/phase、expected-vs-actual local/remote identity、candidate
full ID、Git SHA、RFC3339 UTC、exact argv or masked remote identity、exits、stdout/stderr hashes、
bytes/SHA、mutation counters、terminal PASS/HOLD、next Gate；不记录 secrets/keys。

- A0: local context, candidate inspect, save argv, parent/path lstat and device, temp/final mode,
  link count, bytes, archive SHA, manifest entry, Config member/name/SHA, OS/arch/WorkingDir/Cmd,
  ordered RootFS and every layer member/content digest; Docker mutation count exactly one save.
- R0: SSH locator source and host-key source, hostname/machine-id/kernel/arch/user, Docker client/
  server/daemon fields, deployment/staging lstat and ownership, device/free-space calculation,
  image ID/tag collision observations, Collector identity, SSH exit; all mutation counts zero.
- T1: A0 evidence identity, local expected bytes/SHA, remote temporary/final lstat/device/bytes/SHA,
  stream and verify/publish exits, rename result, exactly two SSH calls, exact remote mutation
  counters (temporary create and same-file publication only), no Docker/lifecycle action.
- L0: T1 evidence identity, pre/post archive bytes/SHA, pre-existing image result, load argv/exit,
  load output hash, full-ID discovery, Config/OS/arch/WorkingDir/Cmd/RootFS comparison, one load,
  zero tag/deployment/lifecycle/cleanup actions.

## 12. Proposed future exact allowlists (not execution authority)

以下仅是 review-ready proposals；PM intake T0、Owner 分别授权 future task 后才可执行。

### A0

- Local: Section 5 exact parent/temp/final、A0 report/JSON；Python entrypoint read-only；无 Git write。
- Remote paths/network: none.
- Docker: one context show、one exact inspect、one `docker image save --output <temp> <full-ID>`；无其它。
- Writes: temp、no-replace final、report、最多 one JSON；不 mkdir/overwrite/cleanup。
- Forbidden: tag/export/build/load/remote/SSH/source/config/status/PM Rules/Git mutation。
- PASS/HOLD: Section 5 全部 PASS，否则 HOLD；next R0；no inheritance。

### R0

- Local: future R0 report/最多 one JSON；remote: read-only `/opt/edge-mes-demo` 与 exact staging
  parent、Docker metadata；无其它 path。
- Docker: version/info、bounded full-ID/tag list、candidate inspect、container/Collector inspect，均 read-only。
- Network: frozen options/source exactly one SSH；writes/mutations zero。
- Forbidden: mkdir/upload/load/tag/Compose/config/restart/cleanup/lifecycle。
- PASS/HOLD: target/parent/free-space/collision/Collector invariants 全 PASS，否则 HOLD；next T1；no inheritance。

### T1

- Local: A0 final read-only、future T1 report/JSON；remote: exact temp/final only。
- Network: same verified target/options exactly 2 SSH（exclusive stream；hash/no-replace/recheck）；无 SCP/rsync/SFTP。
- Writes: exact temp creation与same-filesystem final publication；无目录/Docker/deployment/lifecycle。
- Forbidden: overwrite/fallback/tag/load/restart/cleanup/foreign deletion。
- PASS/HOLD: A0 bytes/SHA 与 final recheck 全 PASS，否则 HOLD；next L0；no inheritance。

### L0

- Local: T1 identity、future L0 report/JSON；remote: exact final archive与Docker image state only；无 local archive mutation。
- Network: exactly one SSH（pre-inspect、one load、post full-ID inspect）。
- Docker: exactly one `docker image load --input <exact-final>` plus exact-ID inspect；零 tag/remove/restart/Compose。
- Writes: exact ID absent 时 one load-created object；无 archive cleanup/foreign mutation。
- PASS/HOLD: full ID、immutable Config/RootFS 全等，否则 HOLD；next C0；no inheritance。

## 13. Review sequence, MVP alignment and T0 counters

Recommended smallest review chain:

```text
PM intake of T0
→ focused Reliability planning review
→ focused Verification exact-identity / allowlist review
→ PM final planning acceptance
→ Owner authorization of A0
```

Data Quality review is not automatic for pure archive/transport identity。classification=`MVP-ALIGNED`：
服务 accepted-local-image → verified archive/transport/remote-object claim，以 full-ID/config/RootFS
equality 防 false inheritance；无 product capability、runtime topology、generic evidence framework、
SBOM/signing/forensics 或 retention model。Scope drift=`NO`。

Actual T0 action counters:

```text
archive creation      = 0
Docker mutation       = 0
Docker read-only obs  = 2 (one context show, one exact image inspect)
host Python execution  = 0
network/SSH/SCP/rsync = 0
remote mutation       = 0
deployment            = 0
service lifecycle     = 0
Git stage/commit/push  = 0
```

Final T0 checks must confirm this exact report is regular/non-symlink, within target `<=24576`
bytes and hard maximum `32768`, `git diff --check` and cached check PASS, cached diff empty,
the task file and report each have one status membership, and no archive/helper/second report was
created. A0/R0/T1/L0 remain proposals until PM independently reads and accepts this report.

Single next Gate: `PM Independent Intake — D2-R7B-T0 Accepted Local-Image Transport Planning`.
