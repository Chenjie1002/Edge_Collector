# Sprint 4 D2-R7B-I1 R56 Exact-Commit Collector Build/Image Acceptance Gate Planning Report

## 1. 报告身份、authority 与终端结论

- 任务：`D2-R7B-I1 R56 — Plan Exact-Commit Collector Build/Image Acceptance Gate`
- 执行 Thread：`Architecture / Integration`
- Authority ID：`PM-D2-R7B-I1-R56-EXACT-COMMIT-COLLECTOR-BUILD-IMAGE-ACCEPTANCE-PLAN-260730-1815`
- Delivery：`REPOSITORY_DURABLE_REPORT`
- 本轮唯一写入：`docs/reports/sprint4_d2_r7b_i1_r56_exact_commit_collector_build_image_acceptance_plan.md`
- one-shot：本文件首次写入时已消费；不得复用、追加、改名或以此授权任何执行。

```text
PASS / EXACT-COMMIT COLLECTOR BUILD-IMAGE ACCEPTANCE PLAN WRITTEN

PLANNING ONLY
REPORT WRITTEN
NOT REVIEWED BY RELIABILITY
NOT REVIEWED BY DATA QUALITY
NOT REVIEWED BY VERIFICATION
NOT PM-FINAL-ACCEPTED
NOT BUILT
NOT IMAGE-ACCEPTED
NOT LOADED
NOT DEPLOYED
NOT ACTIVATED BY THIS COMMIT
RUNTIME-LOADED = NO
PRODUCTION-ACCEPTED = NO
```

本报告只冻结后续独立 gate 的可审查合同。它不创建 build context、archive、manifest、Docker image、tag、container 或远端事实；不把历史 `IMAGE_LOADED_EXACT` 或历史 `ACTIVATED = YES` 归因给本轮 product source commit。

## 2. 必读输入、fresh recovery 与输入身份

已按 Prompt 顺序读取 PM Rules、PM handoff、status、roadmap、R55/R54/R50/R51/R48/R49/R45/R47、R7A/R31/R32/PM scope-reset/R32-R5-R2，随后读取 Dockerfile、Compose、requirements、mapping、`.gitignore`、三条指定 source、两条指定 test，以及仅来自 exact commit 的 `collector/app/**` 与 `common/**` tracked members。Batch D/E 内容没有打开。

写入前的 fresh recovery：

| 项 | 结果 |
| --- | --- |
| repository root / branch | `/Users/chenjie/Documents/MES/edge-mes-demo` / `main` |
| HEAD / origin/main | `c3acb33bd089eae4d67aec3be64c97fd128aa178` / same |
| ahead / behind | `0 / 0` |
| HEAD parent | `934ced7b9659cb566628b1709cf6d73463a534d8` |
| HEAD subject / changed paths | `Sync post-closeout status and PM handoff` / exactly three: `docs/current_status.md`, `docs/roadmap.md`, `docs/thread_handoff/chatgpt_pm_handoff_260730-1719.md` |
| product source commit | `934ced7b9659cb566628b1709cf6d73463a534d8` — `Accept runtime-loaded observability implementation` |
| product commit changed-path count | `24`; this is the accepted implementation closeout, not a build result |
| product commit ancestry | `934ced7...` is an ancestor of `origin/main` |
| tracked dirty / cached | empty / empty |
| `git diff --check` / cached | PASS / PASS |
| R56 initial path | ABSENT / NON-SYMLINK / UNTRACKED / UNSTAGED |
| `.dockerignore` | ABSENT |
| untracked raw / normalized unique count | `301 / 301`; duplicates `0` |
| untracked classification | Batch D `300` + Batch E `1` (`frontend/next-env.d.ts`); unknown `0`, missing `0` |

R36 authority materialization JSON was used only for exact Batch D/E path membership. Current checkout content is not a source authority. The relevant fresh input bytes/SHA-256 are:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/thread_handoff/chatgpt_pm_handoff_260730-1719.md` | 19862 | `71a252407c24fae6e26045d7789a692e6ac34060eba02af75fc900d6779ddeb4` |
| `docs/current_status.md` | 155406 | `87ea8421c896b202c77ff39d950eba7f9d7c4a6cf34a1dfaca3c9a7ec741a44d` |
| `docs/roadmap.md` | 15912 | `48153ac121e14db8c405db619fc8aca4b57f38a7da2f9e92d669e6dc23c8ef8b` |
| `collector/Dockerfile` | 218 | `e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839` |
| `docker-compose.yml` | 5698 | `c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66` |
| `collector/requirements.txt` | 71 | `eaa0a1bf2e133cdfdff2795f4604fc5fbeb54fe0e2bb1a0b990bf1a41a8f54cc` |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` |

## 3. Source authority 与 canonical clean materialization 决定

唯一 product source authority 是 exact commit `934ced7b9659cb566628b1709cf6d73463a534d8`。`c3acb33...` 仅是三文件 docs-only child；`HEAD`、branch 名和当前 checkout 绝不得替代该 commit。

**Canonical decision：未来 gate 只能使用 `git archive` 从该 exact commit 的 object database materialize 一个新建、空的 bounded build root。** 不选择当前 checkout，也不选择 detached worktree。理由是 archive 的输入直接是 commit tree，可机器证明只含选定 tracked bytes；它天然排除 Batch D/E、当前 docs-only child 和所有工作区状态，而不依赖 `.dockerignore`。

未来执行必须在 Docker 调用前完成以下 terminal：

1. 从 `934ced7...` 只 materialize `collector/Dockerfile`、`collector/requirements.txt`、`collector/app/**`、`common/**`；逻辑 context 仍为 repository root `.`，路径不得扁平化。
2. 使用 `git ls-tree -r -l` 获得 source-side raw inventory；按 repository-relative UTF-8 bytewise sort 得到 normalized unique inventory。记录 raw count、normalized unique count、duplicates、unknown、missing。
3. materialized side必须逐项为 regular non-symlink file，path、mode、bytes、SHA-256 和 Git blob identity 均与 exact tree 匹配；缺失、额外、重复、非 regular 或任意 symlink substitution 一律 `HOLD`。
4. 写入 future source-materialization manifest 前后均重算 inventory 与每文件 bytes/SHA-256；manifest self-excluded。任何 materialization 后的改变、未知输入或当前 checkout 路径进入 context 均 `HOLD`。

此 context 的 current exact-tree closure 是 Dockerfile + requirements + `collector/app/**` + `common/**`（当前 tree inspection 为 38 regular tracked members）。它不是整个 repository，也不是 `config/mapping.yaml`。mapping 通过 Compose read-only mount 在 `/app/config` 使用，必须另建 deployment/runtime config identity；mount compatibility 不会把 mapping bytes 说成 image layer bytes。

## 4. Docker context、COPY、platform 与 base identity 合同

当前 Compose 对 Collector 声明 `context: .` 与 `dockerfile: collector/Dockerfile`。exact Dockerfile 的 COPY contract 是：

| Source authority | Container destination | Required comparison |
| --- | --- | --- |
| `collector/requirements.txt` | `/app/requirements.txt` | exact bytes / SHA-256 |
| `collector/app/**` | `/app/app/**` | per-file mapping |
| `common/**` | `/app/common/**` | per-file mapping |

Dockerfile identity、context inventory、COPY mapping、context transport、base object和最终 image是不同 identities；任一相等关系都必须被单独证明。`.dockerignore` 当前不存在，所以直接把这个含 301 条 untracked path 的 checkout传给 Docker是禁止的 accepted-build 输入，即使 Docker command 成功也为 `HOLD`。

Target platform 固定为 `linux/arm64`。未来 PASS必须分别记录和比较 host OS/architecture、builder OS/architecture、requested target、selected base manifest platform、selected base config platform和最终 image OS/architecture/variant；不得依赖默认平台、tag、Raspberry Pi host或 host/target 名称推断。variant存在时必须 exact match；不存在时记录 `ABSENT`，不得伪造值。

当前 `FROM python:3.12-slim` 是 mutable reference。本报告的唯一决策是：**保持当前 Dockerfile 不变；未来独立 build authority 必须以 build provenance 绑定实际使用的 immutable base object。** 本报告不授权也不建议在这里 pin Dockerfile。future pre-build terminal必须记录 registry/reference authority、index/manifest-list digest、选择的 `linux/arm64` manifest digest、该 image config digest、resolution time、command/tool version、network authority和调用预算。build terminal再记录 BuildKit 实际 resolved base material（reference/digest/platform）；不能证明它等于被冻结的 target object、或 provenance不提供足够 link时一律 `HOLD`。未来若要改成 digest-pinned `FROM`，只能先开独立 source-repair/review/Git authority，不能把它作为本合同的第二条 PASS 路径。

## 5. Dependency、builder 与 exact build contract

顶层 requirements 的 exact bytes如第2节所列，内容为 `httpx==0.28.1`、`psycopg[binary]==3.2.3`、`PyYAML==6.0.2`、`python-snap7==3.0.0`。顶层 pin 不等于完整 closure。未来 build preflight / result必须持久化：

- Python、pip、Docker Engine、BuildKit、buildx（如用）、frontend/syntax、driver和builder instance identities；
- exact argv、effective environment（仅 allowlisted non-secret names/values或 value digest）、cache/pull/network policies、start/end timestamps和exit status；
- package index / mirror authority与network budget；每个 selected wheel/distribution identity（filename、URL/redacted authority、hash）、完整 installed distribution name/version inventory、transitive inventory以及 metadata/`RECORD`-level path/hash strategy；
- build provenance/SBOM options及实际产生与否。缺失不是以“未启用”为由通过；secret、credential、token、registry auth header和完整环境不得写入 evidence。

Chosen cache policy：accepted build uses a fresh named builder with **`--no-cache`**; any cache hit is a `HOLD` for accepted build. Pull/network policy必须在 preflight冻结：base resolution所需的最小 registry call在独立授权预算内，build only可使用该明确 policy；未记录的 pull、side channel network、dependency index drift或 foreign/stale layer都不能形成 PASS。builder identity不等于 image identity，cache miss也不自动证明 source closure。

本轮没有运行 Docker、BuildKit、buildx、package manager或 network；因此没有 builder/base/dependency actual result。

## 6. 三类 image acceptance terminal 与 isolated validation

local image acceptance authority必须是 full immutable top-level `Image` ID/config digest，而非 tag、short ID或 `Config.Image`。三类 terminal相互独立：

| Terminal | Expected / actual / comparison | HOLD |
| --- | --- | --- |
| image config | expected contract与 actual inspect逐 field/type比对：full image ID、OS/architecture/variant、Created、Entrypoint、Cmd、WorkingDir、User、ordered Env、Labels、history/provenance link | missing field、wrong type/order/value、platform ambiguity或 image ID不完整 |
| ordered RootFS | expected and actual diff-ID arrays逐 index比较，记录count、each digest、mismatch indices；顺序是 authority | count相同但任一 index不同、invalid digest、缺失或只比较 count |
| source/package closure | source-to-image exact path/bytes/SHA mappings以及 installed distribution closure分别比较 | missing/extra/mismatch、symlink/non-regular、only import success或 only tag |

Source-to-image mapping必须逐文件证明 `collector/app/** → /app/app/**`、`common/** → /app/common/**`、`collector/requirements.txt → /app/requirements.txt`。source closure 与 installed Python distribution closure不同：前者是 copied product bytes，后者是 pip installed distributions与 metadata/RECORD evidence。任一 extra、missing、mismatch、symlink、hardlink/非 regular substitute或不可读取的 expected/actual为 `HOLD`。

在单独 build/image authority中，可在 no-DB、no-PLC、no-API、no-Compose、no-remote、no-service-activation、no-production-fact 的 isolated context检查：`import app.main`、`import common.station_event`、Collector runtime dependency chain import，及以 exact read-only mapping mount进行 bounded mapping parse/static initialization。mapping mount只证明 compatibility；它不得被计入 image RootFS或 source-to-image copied closure。

## 7. Tag、archive 与 digest 语义分离

| Identity | Meaning / rule |
| --- | --- |
| descriptive / compatibility tag | mutable name；不是 content authority；R56不授权 tag name或 mutation |
| local full image ID / config digest | local accepted image content identity |
| manifest digest / index digest | distribution manifest或 multi-platform index identity；不等于 config/image ID |
| archive SHA-256 | archive file bytes；不等于 image ID |
| archive config / manifest digest | archive-internal distinct identities，必须分别记录 |
| remote loaded Docker object ID | future remote-load fact；不由 archive或 local inspect自动推得 |

历史 `IMAGE_LOADED_EXACT` 仅说明先前 object chain；它不能证明 `934ced7...` 被 build、archive、transport、load、deploy、activate或 runtime-loaded。compatibility tag mutation属于后续独立 activation authority。

## 8. Future bounded artifact schema（仅规划，不创建）

后续 execution Prompt必须在开始前将 `<exact-future-root>` 替换为一个由 PM预先声明的 exact repository path；R56没有创建其中任一文件或目录。固定 filenames、producer和最小 schema如下：

| Exact relative suffix under `<exact-future-root>` | Producer / terminal | Required fields / failure behavior |
| --- | --- | --- |
| `01_source_materialization_manifest.json` | materializer / terminal | commit, raw+normalized inventory, per-file mode/bytes/SHA/blob, unknown/extra/missing/duplicate/symlink; any nonzero discrepancy HOLD |
| `02_base_resolution_terminal.json` | authorized resolver / terminal | authority, reference, index/manifest/config digests, platform, time, tool, budget; unresolved/mutable-only/ambiguous HOLD |
| `03_build_metadata_terminal.json` | builder / terminal | builder identities, argv, allowlisted env, cache/pull/network/provenance policy, times, exit, actual base link; missing actual link HOLD |
| `04_dependency_inventory.json` | image/package inspector / terminal | requirements identity, Python/pip/index, wheel/distribution/RECORD inventory and transitive closure; missing hash/extra package HOLD |
| `05_image_inspect_config_terminal.json` | image inspector / terminal | full ID plus expected/actual typed config comparison; mismatch HOLD |
| `06_rootfs_ordered_terminal.json` | image inspector / terminal | expected/actual ordered diff IDs, counts and indices; mismatch HOLD |
| `07_source_to_image_closure_terminal.json` | closure validator / terminal | source/container path map, bytes/SHA/type; missing/extra/mismatch HOLD |
| `08_isolated_static_validation_terminal.json` | isolated validator / terminal | exact image ID, commands, mapping mount identity/mode, outcomes and zero forbidden-action counters; any external contact HOLD |
| `09_archive_identity_terminal.json` | archive step, only if separately authorized / terminal | archive bytes/SHA, config/manifest identities and binding to local image; absent authorization means `NOT_EXECUTED` |
| `manifest.sha256` | final writer / terminal | self-excluded exact path/bytes/SHA list for all created artifacts; changed-after-validation HOLD |

Every terminal must include producer identity, input authority, schema version, expected/actual/comparison, bytes/SHA for referenced durable files, secret boundary and terminal-versus-diagnostic classification. This is a bounded gate evidence set, not telemetry, a generic audit/forensics system, retention platform or registry.

## 9. Authority separation / non-inheritance matrix

| Phase | Executing Thread / authority | Allowed mutation; remote/network; Git | Output / terminal claim / non-claim |
| --- | --- | --- | --- |
| 1 R56 planning | Architecture / Integration; current one-shot | report only; 0/0; no Git | plan written; not reviewed/built |
| 2 Reliability planning review | new Reliability authority | review report only; 0/0; no Git | review verdict; not execution |
| 3 Data Quality planning review | new Data Quality authority | review report only; 0/0; no Git | review verdict; not execution |
| 4 Verification planning review | new Verification authority | review report only; 0/0; no Git | review verdict; not execution |
| 5 PM final planning acceptance | ChatGPT PM new intake | governance decision only; 0/0; no Git unless separately granted | planning accepted; not build authority |
| 6 materialization/base/dependency/builder preflight | new Architecture/Integration execution authority | exact evidence/work root only; declared network budget; no Git | preflight PASS/HOLD; not built |
| 7 local exact build | new build authority | one declared local build; declared network only; no Git | built candidate only; not image accepted |
| 8 local image/package/config/RootFS acceptance | independent acceptance authority | exact terminals only; no remote; no Git | image accepted only; not archived/deployed |
| 9 archive creation/acceptance | separate authority if needed | one exact archive/evidence; no remote unless separately named; no Git | archive accepted only; not transported |
| 10 transport | separate transport authority | exact transport mutation; declared network; no Git | transferred only; not loaded |
| 11 remote load/reconciliation | separate remote authority | declared single remote load/inspect budget; no Git | loaded object reconciliation only |
| 12 deployment | separate deployment authority | named deployment config mutation; separately declared remote budget; no Git | deployed identity only |
| 13 activation/restart | separate lifecycle authority | named lifecycle mutation; separately declared remote budget; no Git | activation only |
| 14 runtime A–H | separate runtime authority under R45/R47 | bounded read-only observations/evidence; remote as declared; no Git | runtime evidence verdict only |
| 15 PM `RUNTIME-LOADED` acceptance | ChatGPT PM | governance acceptance; no implicit mutation | RUNTIME-LOADED only, never production accepted |
| 16 production accepted-fact | separate planning/validation authority | separately scoped DB/API/PLC actions only if granted | production fact verdict only |

Every row requires a new Prompt, exact paths, fresh recovery, budgets and terminal audit. A prior PASS never grants a later row.

## 10. Runtime A–H and product-state boundary

R45/R47 retain control of runtime A–H. R56 neither chooses an active container nor executes SSH, log collection, Docker inspect, process probe or application validation. Image ID, container ID, `StartedAt`, process PID, container-visible mapping bytes, raw transport/log lines, selected line, application message, payload, parsed record, comparison terminal and final manifest are created only under a later independent runtime authority. Build/image PASS cannot generate, substitute for or imply A–H, `RUNTIME-LOADED` or `PRODUCTION-ACCEPTED`.

Current accepted vocabulary remains:

```text
ACTIVATED                  = YES   (historical chain only)
STATIC_MAPPING_INITIALIZED = YES   (historical chain only)
RUNTIME-LOADED             = NO
PRODUCTION-ACCEPTED        = NO
```

## 11. Fail-closed matrix

| Condition | Required terminal |
| --- | --- |
| wrong commit or docs-only `HEAD` used as product source | HOLD |
| current untracked checkout used as build context / `.dockerignore` absence ignored | HOLD |
| materialization inventory unknown, extra, missing, duplicate, symlink or non-regular | HOLD |
| mutable base tag lacks actual immutable base binding | HOLD |
| target OS/architecture/variant missing or wrong | HOLD |
| builder identity, argv, cache/pull/network policy or actual base linkage absent | HOLD |
| cache provenance stale, foreign, or cache hit used for accepted result | HOLD |
| dependency closure, wheel/distribution/RECORD evidence incomplete | HOLD |
| copied source/container path/bytes/SHA differ | HOLD |
| typed config comparison mismatches | HOLD |
| ordered RootFS differs at any index | HOLD |
| tag used as image authority | HOLD |
| archive file/config/manifest/image/remote object identities conflated | HOLD |
| historical image attributed to `934ced7...` | HOLD |
| build PASS represented as load/deploy/activation/runtime/production PASS | HOLD |
| evidence artifact changes after its validation or self-exclusion failure | HOLD |
| any allowlist, Docker/network/SSH/remote/test/application/Git-mutation violation | HOLD |

`HOLD` means stop: no repair, retry, cleanup, source/Dockerfile/Compose/config change, Git action or next phase. A source change needed for digest pinning is a separate future source-repair gate, not a repair window here.

## 12. MVP alignment, blockers, counters 与 next gate

MVP assessment：`MVP-ALIGNED`。本合同只防止 wrong-source context、stale/foreign image、wrong platform、mutable-base ambiguity、dependency closure gap和 evidence-identity confusion；未增加 API、DB schema、telemetry、generic registry、audit/forensics、retention、SBOM platform、production sync、Oracle/ERP integration或 Dashboard work。

Blockers：none for this planning-write gate. Bounded recommendations：future reviewers must preserve the chosen archive materialization method, no-cache accepted-build rule, actual-base provenance requirement and three-terminal separation; no build execution is recommended until the required independent reviews and PM planning acceptance complete.

Forbidden-action counters for R56:

| Category | Count |
| --- | ---: |
| Docker / BuildKit / buildx / Compose / image/tag/archive mutation | 0 |
| package download/install / network / registry | 0 |
| SSH / remote / deployment / activation / rollback | 0 |
| DB / API / PLC / V-PLC / ACK / `read_done` / production fact | 0 |
| tests / application / runtime A–H | 0 |
| Git add / stage / commit / push / tag / reset / restore / checkout / stash / clean | 0 |
| Batch D/E content operation | 0 |
| extra report/manifest/helper/artifact creation | 0 |

唯一 next gate：

```text
R56 Architecture / Integration planning report
→ ChatGPT PM durable intake
→ independent Reliability planning review under a new one-shot authority
```

不要自动发布 Reliability Prompt，也不得进入 Data Quality、Verification、build、network、Docker、remote、Git、deployment、activation、runtime A–H 或 production accepted-fact。R56 PASS不授予任何后续 authority。

## 13. 写后审计边界

本报告的最终 bytes/SHA-256不能嵌入自身；应在写后以 detached read-only audit测量。该测量只证明本文件 bytes，不构成 review、PM acceptance、build、image、archive、remote、runtime或 production authority。
