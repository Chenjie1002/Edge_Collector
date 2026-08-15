# Sprint 4 D2-R7B-I1 R65 Exact-Commit Collector Build/Image Execution-Preparation Planning Report

## 1. 报告身份、authority 与结论

- 任务：`D2-R7B-I1 R65 — Exact-Commit Collector Build/Image Execution-Preparation Plan`
- 执行 Thread：`Architecture / Integration`
- Authority ID：`PM-D2-R7B-I1-R65-EXACT-COMMIT-COLLECTOR-BUILD-IMAGE-EXECUTION-PREPARATION-PLAN-260730-2102`
- Delivery：`REPOSITORY_DURABLE_REPORT`
- 本轮唯一 task-owned write：`docs/reports/sprint4_d2_r7b_i1_r65_exact_commit_collector_build_image_execution_preparation_plan.md`
- Authority：`AUTHORIZED ONCE / ARCHITECTURE-INTEGRATION / PLANNING-ONLY / EXACT REPORT WRITE ONLY / NOT REUSABLE`；本文件首次创建时已消费。

```text
PASS / EXACT-COMMIT COLLECTOR BUILD/IMAGE EXECUTION-PREPARATION PLAN WRITTEN

PLANNING ONLY
R65 REPORT WRITTEN
R66 NOT AUTHORIZED
NO FUTURE ATTEMPT ROOT / ARCHIVE / MATERIALIZATION / BUILDER / CANDIDATE / CONTAINER / TERMINAL EXISTS BY THIS TASK
NOT BUILT / NOT IMAGE-ACCEPTED / NOT ARCHIVED / NOT TRANSPORTED
NOT REMOTE-LOADED / NOT DEPLOYED / NOT ACTIVATED / NOT RUNTIME-LOADED / NOT PRODUCTION-ACCEPTED
```

本报告冻结一条且仅一条 future local execution path。它不创建 fixture、helper、harness、archive、evidence、Docker object 或 R66 report；不执行 Docker、BuildKit、buildx、Compose、network、package resolution、test/application、SSH/remote、Git mutation 或 cleanup。`WRITTEN` 不等于 `REVIEWED`、`ACCEPTED`、`VERIFIED`、`STAGED`、`COMMITTED`、`PUSHED` 或 `EXECUTED`。

## 2. Required reading、live recovery 与输入身份

已按 Prompt 顺序读取 PM Rules（含 §§3、4、7、10、11、12、13）、current status、roadmap、R64、handoff、R56、R60、R61、R62、R63、四个构建输入及允许的 exact product tree metadata/content。未读取 Batch D/E 内容，未读取 R57/R58 内容；R59 仅作为 R64/handoff 所述 historical blocker origin，不重新审判。

Fresh read-only recovery：

| 项目 | Live result | 判定 |
| --- | --- | --- |
| repository / branch | `/Users/chenjie/Documents/MES/edge-mes-demo` / `main` | PASS |
| `HEAD` / `origin/main` | 均为 `0e7544a12b00799780d76723ca0de781bc2e8ad7` | PASS |
| ahead / behind | `0 / 0` | PASS |
| HEAD subject / parent | `Add PM handoff for build image execution preparation` / `796c87b395e6e153665a3e58e490490e2f1c1d8b` | PASS |
| HEAD changed paths | only `docs/thread_handoff/chatgpt_pm_handoff_260730-2027.md` | PASS |
| `796c87b...` changed paths | only `docs/current_status.md`、R64、`docs/roadmap.md` | PASS |
| tracked / cached diff；both diff checks | empty / empty；PASS / PASS | PASS |
| product source | `934ced7b9659cb566628b1709cf6d73463a534d8` is current `HEAD` ancestor | PASS |
| R65 initial path | `ABSENT / NON-SYMLINK` | PASS |
| current candidate / remote candidate | `NONE / NOT OBSERVED` | recorded, not an identity substitute |

R36 JSON was accessed only by the fixed Batch D/E `.exact_paths[]` membership expressions. The bytewise UTF-8 stable comparison, before dedup duplicate check, was:

| Observation | Raw | Normalized unique | Unknown | Missing | Duplicate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Batch D | 300 | 300 | — | — | 0 |
| Batch E | 1 | 1 | — | — | 0 |
| expected: Batch D + E + R56–R63 | 309 | 309 | 0 | 0 | 0 |
| live untracked | 309 | 309 | 0 | 0 | 0 |

No Batch D/E member is reproduced here. A later R66 must make the same raw-before-dedup comparison and must treat any unknown, missing or duplicate as `HOLD`.

Relevant static inputs at planning time:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| R56 | 22307 | `09efd1f888c79a28ed246a7babc8ada91966ee1196792842fa854e0a339e8e45` |
| R60 | 22459 | `5bd2abbe7182b2a3c6e879e325d35c075254fcbed308863d8b74a82e961cad68` |
| R61 | 13709 | `e8d21f4294ea867c0b10671de7fa0d17622c28a0be9ec60e88928155b90e3ada` |
| R62 | 19300 | `33978d6470a6852b895ee54e04278c0228e544a37c229731531f175156d520ff` |
| R63 | 30192 | `f012de418752517a7af3eef389ce9e55130d72941ae4c789c1cc757713b78f00` |
| `collector/Dockerfile` | 218 | `e47513aff4980c650928a91b9a9b3a02a2cb5f92e328274cf7c941c43fc71839` |
| `docker-compose.yml` | 5698 | `c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66` |
| `collector/requirements.txt` | 71 | `eaa0a1bf2e133cdfdff2795f4604fc5fbeb54fe0e2bb1a0b990bf1a41a8f54cc` |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` |

These are planning/static observations, not future R66 inputs by themselves. R66 must re-observe all frozen source identities from exact commit `934ced7...`; current checkout and docs-only `HEAD` are never a product source substitute.

## 3. Accepted contract mapping: one rule path only

| Subject | Controlling rule | R65 frozen effect |
| --- | --- | --- |
| exact product source, clean-context exclusion, root-relative Docker layout, `linux/arm64`, base/tag distinction, COPY closure, phase separation | R56 retained clauses | exact source commit and four source scopes only; no checkout context; mapping excluded from image closure |
| unique attempt/builder/candidate, archive/materialization ownership, source lock, evidence publication | R60 §§5–6, 9–10 supersede R56 | one owned attempt and no reuse/cleanup/overwrite; ten R66 terminals |
| deterministic Config expected vs actual; RootFS actual-only identity; dependency expected vs actual | R60 §§7–8 supersede R56 | no precomputed RootFS or transitive lock; no expected/actual alias |
| five accepted R59 risks | R61 closed | not reopened; all five remain enforced through R60 controls |
| lexical digest, path-domain, timestamp grammar; raw/normalized and terminal lineage | R62/R63 carry-forward | finite record grammar below; no generic registry/platform |

There is no R56/R60 dual PASS path and no permissive selection. R59 remains historical origin only. This contract neither requires nor permits a full transitive lock, hash-pinned requirements, SBOM, offline mirror, precomputed RootFS, bit-for-bit reproducibility, malicious-admin resistance, generic audit/forensics/retention platform, Oracle/ERP work or `sync-worker` expansion.

## 4. Frozen R66 identity and ownership table

Future task identity: `D2-R7B-I1 R66 — Exact-Commit Collector Local Build/Image Acceptance Execution`.

| Identity | Frozen value / rule |
| --- | --- |
| `attempt_id` | `d2-r7b-i1-r66-934ced7-a1` |
| product source | `934ced7b9659cb566628b1709cf6d73463a534d8` |
| target / base reference | `linux/arm64` / `python:3.12-slim` |
| attempt root | `/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1` |
| source archive | `/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/source.tar` |
| materialization parent / source root | `/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/materialized` / `/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/materialized/source` |
| runtime-mapping archive / materialization root / file | `/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/runtime-mapping.tar` / `/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/runtime-mapping-materialized` / `/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/runtime-mapping-materialized/config/mapping.yaml` |
| builder / candidate reference | `edge-mes-d2-r7b-i1-r66-934ced7-a1` / `edge-mes-collector:d2-r7b-i1-r66-934ced7-a1` |
| validation container | `edge-mes-d2-r7b-i1-r66-934ced7-a1-validation` |
| IID / build metadata | `/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/candidate.iid` / `/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/build-metadata.json` |
| R66 report / evidence root | `docs/reports/sprint4_d2_r7b_i1_r66_exact_commit_collector_local_build_image_acceptance_execution.md` / `docs/reports/evidence/d2_r7b_i1_r66_exact_commit_collector_local_build_image_acceptance` |

At R66 entry every host path above must be absent; no parent may be a symlink. The attempt root, materialization parent and runtime-mapping materialization root are created only after their individual absence checks and must then be empty directories, non-symlink and attempt-owned. Archives, IID and metadata are initially absent and, once written, must be regular non-symlink files. The builder, candidate reference, validation container and every terminal path must also be absent. Any pre-existing, foreign, non-regular, symlink, non-empty, renamed, overwritten, taken-over or reused object is `HOLD / OUTPUT_PATH_PREEXISTS` or `AUTHORITY_MISMATCH`; R66 has no cleanup authority.

## 5. Exact source and mapping materialization contract

R66 source scope is exactly:

```text
collector/Dockerfile
collector/requirements.txt
collector/app/**
common/**
```

The logical Docker context is `materialized/source`, preserving repository-root-relative layout; Dockerfile stays `collector/Dockerfile`. `config/mapping.yaml` is not in the build context, not copied into RootFS and not counted in source-to-image closure. It is a separate exact product-commit authority, extracted outside the context and mounted read-only only for isolated validation.

| Item | Frozen command and format |
| --- | --- |
| source path-list discovery | executable `/usr/bin/git`; argv `-C /Users/chenjie/Documents/MES/edge-mes-demo ls-tree -r -z --name-only 934ced7b9659cb566628b1709cf6d73463a534d8 -- collector/Dockerfile collector/requirements.txt collector/app common` |
| source archive | executable `/usr/bin/git`; argv `-C /Users/chenjie/Documents/MES/edge-mes-demo archive --format=tar --prefix=source/ 934ced7b9659cb566628b1709cf6d73463a534d8 -- collector/Dockerfile collector/requirements.txt collector/app common`; stdout is the initially absent `source.tar` |
| source extraction | executable `/usr/bin/bsdtar`; argv `-xf /tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/source.tar -C /tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/materialized`; required prefix is exactly `source/` |
| mapping path-list discovery | executable `/usr/bin/git`; argv `-C /Users/chenjie/Documents/MES/edge-mes-demo ls-tree -r -z --name-only 934ced7b9659cb566628b1709cf6d73463a534d8 -- config/mapping.yaml` |
| mapping archive | executable `/usr/bin/git`; argv `-C /Users/chenjie/Documents/MES/edge-mes-demo archive --format=tar --prefix=config/ 934ced7b9659cb566628b1709cf6d73463a534d8 -- config/mapping.yaml`; stdout is the initially absent `runtime-mapping.tar` |
| mapping extraction | executable `/usr/bin/bsdtar`; argv `-xf /tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/runtime-mapping.tar -C /tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/runtime-mapping-materialized`; required member/file is exactly `config/mapping.yaml` |

`/usr/bin/git` and `/usr/bin/bsdtar` must be rechecked as regular non-symlink executables at R66 preflight. Archive member names are normalized after raw NUL-delimited discovery by UTF-8 bytewise stable sort. Before dedup, duplicate member/path detection is mandatory. Raw Git-tree, archive-member and extracted inventories each retain repository-relative path, type, mode, bytes, ordinary file SHA-256 and Git blob ID; all three must exactly agree. Extracted files must be regular, non-symlink. `..`, NUL, absolute members, ambiguous/cross-domain or non-canonical paths, hardlinks, gitlinks, special files, missing, extra, duplicate or any mismatch are `HOLD`.

The source materialization lock is emitted only after these comparisons and a second post-extraction inventory confirms no change. The lock binds source commit, scope list, archive/extract argv, archive file identity, materialized inventory and mapping archive/file identity. From lock publication through build-context consumption, any byte/type/mode/path change is `HOLD`; evidence must never be written under the build context.

## 6. R66 exact Docker/network command budgets

`docker` below is the Docker CLI executable identity; before its first invocation R66 must record its absolute resolved regular non-symlink executable path, SHA-256 and client/buildx version in terminal 03. Failure to resolve that identity is `HOLD` before Docker mutation. The argv below are otherwise exact; angle-bracket values are the single parsed immutable values produced by the immediately preceding declared command and cannot be chosen, edited or retried by an operator.

| # | Exact executable and argv | Count | Network capable | Docker-daemon mutation | Purpose / failure rule |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | `docker buildx imagetools inspect --raw python:3.12-slim` | 1 | 1 | 0 | resolve index/manifest-list; select only `linux/arm64` manifest digest |
| 2 | `docker buildx imagetools inspect --raw python:3.12-slim@<selected-linux-arm64-manifest-digest>` | 1 | 1 | 0 | resolve selected manifest/config digest; malformed or non-OCI digest HOLD |
| 3 | `docker buildx create --name edge-mes-d2-r7b-i1-r66-934ced7-a1 --driver docker-container --platform linux/arm64 --use` | 1 | 1 | 1 | create the one owned builder; pre-existing name or failure HOLD |
| 4 | `docker buildx inspect --builder edge-mes-d2-r7b-i1-r66-934ced7-a1 --bootstrap` | 1 | 1 | 1 | bootstrap/inspect that builder only; record builder identity/platform |
| 5 | `docker buildx build --builder edge-mes-d2-r7b-i1-r66-934ced7-a1 --platform linux/arm64 --no-cache --pull --provenance=mode=max --metadata-file /tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/build-metadata.json --iidfile /tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/candidate.iid --tag edge-mes-collector:d2-r7b-i1-r66-934ced7-a1 --load --file collector/Dockerfile /tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/materialized/source` | 1 | 1 | 1 | the sole build; base pull and package resolution may occur only here |
| 6 | `docker image inspect --format {{json .}} edge-mes-collector:d2-r7b-i1-r66-934ced7-a1` | 1 | 0 | 0 | obtain typed actual full candidate ID/config/RootFS; tag is lookup only |
| 7 | `docker container create --name edge-mes-d2-r7b-i1-r66-934ced7-a1-validation --network none --read-only --mount type=bind,src=/tmp/edge-mes-d2-r7b-i1-r66-934ced7-a1/runtime-mapping-materialized/config/mapping.yaml,dst=/app/config/mapping.yaml,readonly --entrypoint python edge-mes-collector:d2-r7b-i1-r66-934ced7-a1 -c 'from app.plc.mapping import load_edge_mapping; import app.main; import common.station_event; m=load_edge_mapping("/app/config/mapping.yaml"); assert m.mapping_content_sha256 == "<mapping-file-sha256>"'` | 1 | 0 | 1 | create exactly one isolated validation container; the tag must resolve to the full candidate ID recorded by #6 |
| 8 | `docker container start --attach edge-mes-d2-r7b-i1-r66-934ced7-a1-validation` | 1 | 0 | 1 | one validation run; exit 0 required |
| 9 | `docker container inspect --format {{json .}} edge-mes-d2-r7b-i1-r66-934ced7-a1-validation` | 1 | 0 | 0 | record exit/state/mount/network/read-only facts |

The parsed `<selected-linux-arm64-manifest-digest>` and `<mapping-file-sha256>` must meet their own grammar and originate respectively from command 1 and the locked mapping inventory; they are not free argv alternatives. Command 5 must prove its actual base provenance links to the selected immutable index/manifest/config identities. A mutable tag alone, `--no-cache`, a builder name, a tag, `Config.Image`, a historical image/tag, or a `--pull` flag does not pass base provenance.

Exact budgets: registry/base-resolution commands 1–2 each once; builder/bootstrap 3–4 each once; one build (5); candidate inspection once (6); validation create/run/inspect once each (7–9). Network authority is therefore exactly five network-capable invocations, and only those invocations may contact registry/base/package services. No other HTTP, DNS, registry, package-index or side channel is authorized. Any non-zero, timeout, interrupt, cancellation, daemon restart, client loss, unexpected network, over-budget invocation, nonzero validation exit or forbidden action immediately terminalizes the attempt as `HOLD`; every remaining budget becomes invalid. There is no retry, failed-attempt reuse, builder/candidate/container removal or cleanup under R66.

## 7. Build policy and independent expected/actual matrix

The one build is `linux/arm64`, `--no-cache`, explicit `--pull`, exact clean context, exact Dockerfile, candidate reference, IID file, metadata file, provenance and `--load` behavior shown above. It has one successful full candidate image ID at most; `candidate.iid` must contain the full non-abbreviated ID and agree with typed image inspection. `Created`, history, provenance, full candidate ID and RootFS are actual identity only, never fabricated expected values.

| Family | Expected authority | Actual authority | PASS comparison / HOLD boundary |
| --- | --- | --- | --- |
| base | `python:3.12-slim`, target `linux/arm64`, commands 1–2 immutable index/manifest/config selection | resolver/build provenance and metadata | actual build base exactly links; tag-only, wrong platform, manifest/config conflation or missing link HOLD |
| platform | PM target OS/arch; variant expected absent unless explicitly returned by selected platform | base and candidate inspect | OS/arch exact; absent/null/value kept distinct; mismatch/ambiguity HOLD |
| Config | Dockerfile: WorkingDir `/app`; Cmd ordered `["python","-m","app.main"]`; Entrypoint ABSENT; User ABSENT; Env ABSENT; Labels ABSENT | typed image inspect | typed equality; Env/Cmd/Entrypoint order retained; labels canonicalized only by keys; missing/null/empty/absent distinct |
| requirements | locked 71-byte file SHA plus four pins: `httpx==0.28.1`, `psycopg[binary]==3.2.3`, `PyYAML==6.0.2`, `python-snap7==3.0.0` | same-candidate installed inventory | each required distribution exactly once at exact version; actual transitive closure is recorded, not preapproved |
| copied closure | locked materialized source and Dockerfile COPY mapping | candidate filesystem evidence | `collector/requirements.txt → /app/requirements.txt`; `collector/app/** → /app/app/**`; `common/** → /app/common/**`; each path/type/mode/bytes/SHA exact |
| RootFS | no precomputed layer oracle; only binding requirements | same-candidate `RootFS.Layers` | complete `sha256:<64 lowercase hex>` array preserved in original order and bound to attempt/candidate/base/provenance; not layer business correctness |

For copied closure, any missing, extra, link, non-regular or path/type/mode/bytes/SHA mismatch is `HOLD`. Mapping mount is excluded. Actual dependency inventory must contain candidate binding, distribution metadata and `RECORD` details sufficient to state the actual closure; malformed, unreadable, incomplete, conflicting or candidate-unbound evidence is `HOLD`. An unexpected transitive distribution alone is not a HOLD when inventory is complete and all required pins/validation pass.

## 8. Isolated validation and non-claims

Validation is exactly commands 7–9: candidate full ID is the execution authority, even though the immutable candidate reference is the CLI lookup. It has `--network none`, read-only root filesystem and exactly one read-only mapping bind; no writable tmpfs is authorized. The embedded code only imports source and invokes `load_edge_mapping` on the frozen mapping path; it must not call `main()` and must not create DB/API/PLC/V-PLC/Compose/remote/deployment/activation/production actions.

Terminal 09 must report counters `network=0`, `DB=0`, `API=0`, `PLC=0`, `V_PLC=0`, `Compose=0`, `remote=0`, `deployment=0`, `activation=0`, `production_fact=0`, `writable_tmpfs=0`. Any nonzero counter is `HOLD`. The validation container must not use `--rm`; its object is retained after either result awaiting a separately authorized cleanup task.

Even a future R66 PASS establishes at most: `LOCAL CANDIDATE BUILT`; `FULL LOCAL CANDIDATE ID RECORDED`; `DETERMINISTIC CONFIG MATCHED`; `SOURCE-TO-IMAGE CLOSURE MATCHED`; `TOP-LEVEL REQUIREMENTS MATCHED`; `ACTUAL DEPENDENCY CLOSURE RECORDED`; `ORDERED ROOTFS IDENTITY RECORDED`; `ISOLATED VALIDATION PASSED`; `LOCAL IMAGE ACCEPTANCE EVIDENCE COMPLETE`.

It does not establish archive, transport, remote load, deployment, activation, runtime load, production acceptance, reproducible build, preapproved transitive closure, SBOM, supply-chain approval or tamper-proof evidence.

## 9. Ten terminal paths, common schema and lineage

All ten paths are under `docs/reports/evidence/d2_r7b_i1_r66_exact_commit_collector_local_build_image_acceptance/`:

| # | Exact terminal path suffix | Producer / required purpose | Downstream consumer / explicit non-claim |
| ---: | --- | --- | --- |
| 01 | `01_source_materialization_terminal.json` | materializer; commit/archive/extraction inventories and lock | 02–10; not build |
| 02 | `02_attempt_preflight_terminal.json` | R66 preflight; all initial absence/ownership/executable checks | 03–10; not base resolution |
| 03 | `03_base_and_builder_actual_terminal.json` | resolver/builder preflight; selected immutable base and builder identity | 04–10; not base-tag future stability |
| 04 | `04_build_result_terminal.json` | sole build; exact argv, exit, IID/full candidate ID and provenance | 05–10; not image acceptance |
| 05 | `05_deterministic_config_comparison_terminal.json` | typed Config expected/actual comparison | 10; not RootFS/reproducibility |
| 06 | `06_source_to_image_closure_terminal.json` | per-file copied closure comparison | 10; not mapping-mount validation |
| 07 | `07_dependency_candidate_identity_terminal.json` | top-level pins and actual candidate-bound dependency closure | 10; not preapproved transitive lock |
| 08 | `08_rootfs_candidate_identity_terminal.json` | original-order actual RootFS identity | 10; not precomputed RootFS/layer correctness |
| 09 | `09_isolated_validation_terminal.json` | isolated command/mount/counter/outcome evidence | 10; not deployment/runtime acceptance |
| 10 | `10_final_manifest_terminal.json` | last self-excluding complete-publication and rehash audit | PM intake; not generic retention/anti-tamper or production evidence |

Each terminal uses `schema_version: d2-r7b-i1-r66-terminal/v1` and includes: producer identity; authority inputs; `attempt_id`; candidate full image ID where applicable; RFC3339 UTC start/end timestamps; exit status; expected; actual; comparison; verdict; failure class; `terminal` or `diagnostic` classification; downstream consumer; and explicit non-claim. Required terminals may never use `NOT APPLICABLE`; only an unauthorized optional archive would be `NOT APPLICABLE / OUT OF SCOPE`, and no archive terminal is part of this R66 set.

Lineage is mandatory and acyclic:

```text
10 final manifest
→ 05 config / 06 source closure / 07 dependency / 08 RootFS / 09 isolated validation
→ 04 build result and full candidate ID
→ 03 base-builder actual
→ 02 attempt preflight
→ 01 source-materialization lock
→ exact product source 934ced7...
→ PM authority and d2-r7b-i1-r66-934ced7-a1
```

Every edge carries same-attempt identity; every candidate-bearing edge carries the same full candidate ID. A predecessor `HOLD` prevents every dependent terminal. A temp file is non-terminal: producer writes same-directory temp, validates complete schema, then atomically publishes. Terminal 10 is published last, self-excludes, then rehashes all included artifacts. Missing, extra, duplicate, cross-attempt, cross-candidate, malformed, partial, not-last or post-publication-mutated evidence is `HOLD`; no malicious-admin-resistant claim is made.

## 10. Record grammar, PASS/HOLD and authority separation

| Rule | Frozen R66 interpretation |
| --- | --- |
| ordinary file SHA-256 | its own field; complete lowercase 64 hex |
| OCI digest | its own field; `sha256:<64 lowercase hex>` |
| Git commit/blob / candidate ID | separate typed fields; full, never abbreviated; neither exchanges with file/OCI digest |
| path domains | `repository_relative_path`, `container_absolute_path`, `evidence_root_relative_path`; `host_absolute_path` only for PM-frozen paths above |
| timestamps | RFC3339 UTC `YYYY-MM-DDTHH:MM:SSZ`, parsable, same attempt, `start <= end` |
| normalization | retain raw and normalized input; unordered sets UTF-8 bytewise stable sort; detect duplicate before dedup; maps canonicalize keys without dropping fields; do not sort Env/Cmd/Entrypoint/history/RootFS |
| missing semantics | absent, `null`, empty string, empty array/object, `NOT APPLICABLE`, `NOT EXECUTED`, `NOT OBSERVED`, `UNKNOWN`, malformed and unreadable remain distinct |

Paths reject `..`, NUL, ambiguous absolute/relative form, mixed domain and non-canonical representation. Invalid grammar, identity conflation, expected/actual alias, authority mismatch, pre-existing output, cardinality error, materialization drift, base provenance mismatch, build failure, forbidden action, incomplete lineage, post-publication mutation or phase overclaim are terminal `HOLD` classes.

| Phase / budget | R66 authority | Explicit non-inheritance |
| --- | --- | --- |
| source materialization, base/builder preflight, one local build, local inspection, isolated validation, final publication | only as frozen above | a PASS in one row authorizes no later row except declared lineage consumption |
| Git | `0` | no add/stage/commit/push/tag |
| remote / transport / deployment / activation | `0 / 0 / 0 / 0` | no SSH, remote Docker, archive transport, restart, rollback or runtime A–H |
| production acceptance | `0` | no DB/API/PLC/V-PLC/ACK/`read_done` or accepted-fact claim |

R66 has one attempt, one builder, one build, one candidate reference, one successful full candidate ID and no retry/reuse/cleanup. A new attempt requires a new Prompt, new authority, new attempt ID, new roots and new object names. The exact next gate after this report is ChatGPT PM durable intake and a separately authorized R66 decision; no review Prompt, R66 execution or Git action is issued here.

## 11. Blockers, recommendations, MVP alignment and R65 counters

Blockers: none. All PM-owned seeds form one internally consistent R60-controlled execution path; no replacement value is required.

Recommendations: when and only when PM separately authorizes R66, use this report as the exact planning contract and obtain a fresh R66 recovery/absence audit before the first R66 write or Docker invocation. Do not turn R62/R63 grammar into a generic platform or a new blocker.

```text
MVP alignment: MVP-ALIGNED WITH BACKLOG ITEMS
```

| Forbidden action category during R65 | Count |
| --- | ---: |
| Docker / BuildKit / buildx / Compose / image/tag/archive action | 0 |
| network / registry / package resolution or installation | 0 |
| SSH / remote / transport / deployment / activation / rollback | 0 |
| tests / application / DB / API / PLC / V-PLC / ACK / `read_done` / runtime | 0 |
| Git add / stage / commit / push / tag / reset / restore / checkout / stash / clean | 0 |
| Batch D/E content operation | 0 |
| extra report, fixture, helper, manifest, JSON, log, archive, directory or sidecar | 0 |

This report is the only R65 changed path. It is a planning/static artifact only; future commands have not been tested or validated against Docker behavior.
