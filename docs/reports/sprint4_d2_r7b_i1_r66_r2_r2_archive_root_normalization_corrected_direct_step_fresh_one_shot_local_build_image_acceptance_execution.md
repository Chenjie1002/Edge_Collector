# Sprint 4 D2-R7B-I1 R66-R2-R2 Archive Root-Directory Normalization Corrected Direct-Step Fresh One-Shot Local Collector Build/Image Acceptance Execution Report

## Conclusion

`HOLD / DOCKER_COMMAND_01_INVOCATION_FAILURE`

- Task: `D2-R7B-I1 R66-R2-R2`
- Thread: `Architecture / Integration — fresh independent execution Thread`
- Authority: `PM-D2-R7B-I1-R66-R2-R2-ARCHIVE-ROOT-NORMALIZATION-CORRECTED-DIRECT-STEP-FRESH-ONE-SHOT-260731-1801`
- Attempt: `d2-r7b-i1-r66-r2-r2-934ced7-a5`
- Product commit: `934ced7b9659cb566628b1709cf6d73463a534d8`
- Delivery: `REPOSITORY_REPORT_WITH_ARTIFACTS`

The corrected archive-root normalization and exact source/mapping materialization passed. Docker command 1 then failed once with exit `125` and diagnostic `unknown flag: --raw`. The one-shot authority was already consumed; retry, repair, Docker capability discovery, cleanup, commands 2–9, future-phase records, and final manifest are not authorized. Execution stopped immediately.

## Entry gate and preservation

The authoritative task file matched `35347` bytes and SHA-256 `a635c178737c387fa19e03411a67d22002d64e5a0792d002a495691f1c75181f`. The complete reading order and exact Batch D/E membership expressions were read before the first write.

Fresh recovery established:

```text
repository / branch    = /Users/chenjie/Documents/MES/edge-mes-demo / main
HEAD = origin/main     = 0e7544a12b00799780d76723ca0de781bc2e8ad7
ahead / behind         = 0 / 0
tracked / cached       = empty / empty
pre-task membership    = 347 / 347 / 0 / 0 / 0
Batch D/E + non-Batch  = 301 + 46
product ancestry       = PASS
```

A1, A2, and A4 roots remained present, non-symlink, historical, and not reused. Their frozen reports/records matched the task identities. A3 report/evidence/attempt remained absent. SR4-R1 report, producer, test, and lock matched their frozen identities. A5 report/evidence/attempt paths were absent before exclusive creation.

## Archive-normalization smoke and materialization

The pre-write smoke used the exact recursive Git-tree and in-memory archive commands. Results:

| Scope | Recursive blobs | Archive bytes | Archive SHA-256 | Members | Regular | Directories | Bad |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| source | 38 | 296960 | `1848e4f67ee0ca0a7d665d5debacf1c16f457ba1fb2a1660e6ec070c78f0ee3f` | 47 | 38 | 9 | 0 |
| mapping | 1 | 10240 | `7bfb4359b12a0933ae02360a9e64f9069eb649786cc5b7642517406915ab003f` | 2 | 1 | 1 | 0 |

Normalized top-level directory members `source` and `config` were accepted. Directory entries were excluded from ordinary-file inventories. Negative cases for absolute, NUL, dot, dot-dot, empty component, duplicate normalized path, wrong root, symlink, hardlink, character special, and FIFO were rejected.

The Phase 1 archives exactly matched the pre-write byte identities. Archive file bytes recomputed to the recursive Git-tree blob OIDs. Source Git/archive/extracted closure was `38 / 38 / 38`; mapping closure was `1 / 1 / 1`. The extracted mapping was `7112` bytes with SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`. Format-aware Git/archive/extracted mode comparison passed, with all copied inputs non-executable.

Durable Record 01:

- `docs/reports/evidence/d2_r7b_i1_r66_r2_r2_direct_step_local_build_image_acceptance/01_source_materialization.json`
- `5334` bytes
- SHA-256 `b0e257641186f2bfe27e9119af6476ca28ecc8f0572ca2d026b02f4b6b34d92d`
- Verdict `PASS`

## Docker command 1 HOLD

The first and only Docker call was:

```text
docker buildx imagetools inspect --raw python:3.12-slim
```

```text
started = 2026-07-31T10:17:37.338158000Z
ended   = 2026-07-31T10:17:37.399182000Z
exit    = 125
stderr  = unknown flag: --raw
stdout  = 0 bytes / e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

The failure occurred before an immutable base descriptor was observed. No Docker capability/version query was added, because that would exceed the frozen direct execution path after failure. Commands 2–9 are `NOT_EXECUTED`.

Durable Record 02:

- `docs/reports/evidence/d2_r7b_i1_r66_r2_r2_direct_step_local_build_image_acceptance/02_build_and_candidate.json`
- `2633` bytes
- SHA-256 `ce19942dbbbd30af32d0f7f58bde279bf784ab483704fe7eaac723d4b744300f`
- Verdict `HOLD`

Records 03–05 were not created. In particular, no final manifest was fabricated after the Phase 2 HOLD.

## Counters, audits, and non-claims

```text
Docker calls             = 1 / 9 authorized
network-capable calls     = 1 / 5 authorized
daemon-mutating calls     = 0 / 5 authorized
builds                    = 0 / 1 authorized
validation containers     = 0 / 1 authorized
probes                     = 0 / 1 authorized
tags / retries / cleanup  = 0 / 0 / 0
```

The attempt root contains only the two exact archives, the two authorized materialized directory roots, and the command-01 stdout capture. The evidence root contains only Records 01 and 02. No executable harness, script, module, source output, generic parser, sidecar, cache, bytecode, or extra evidence file was created.

Final repository membership after this report is `350 raw / 350 unique / 0 duplicate / 0 unknown / 0 missing`. Tracked, cached, and staged state remains empty. Git stage/commit/push/tag are all `0`.

No immutable base was selected; no builder, build, candidate full ID, candidate config digest, RootFS, 37-source comparison, four-pin comparison, validation container, probe, or isolation topology was observed. Archive transport, remote load, deployment, activation, runtime-loaded, and production-accepted remain unauthorized and unobserved.

## Status matrix

```text
R66-R2-R2 EXECUTION ATTEMPT STARTED = YES
R66-R2-R2 ACCEPTANCE EXECUTED        = NO
SOURCE/MAPPING MATERIALIZED          = YES
LOCAL CANDIDATE BUILT                = NO
LOCAL IMAGE ACCEPTED                 = NO
EXECUTION PACKAGE WRITTEN            = YES (HOLD subset: Records 01–02 + report)
PM ACCEPTED                          = NO
ARCHIVED                             = NO
TRANSPORTED                          = NO
REMOTE LOADED                        = NO
DEPLOYED                             = NO
ACTIVATED                            = NO
RUNTIME-LOADED                       = NO
PRODUCTION-ACCEPTED                  = NO
```

## Blocker, recommendation, and next gate

Blocker: the available `docker` command rejected the frozen command-1 `--raw` invocation before a base index could be observed.

Recommendation: ChatGPT PM should first durable-intake this exact HOLD package. Any Docker CLI/buildx capability diagnosis or corrected fresh execution must receive a new independent authority, attempt ID, roots, command budget, and Thread. A5 must not be retried, repaired, reused, or cleaned up.

Next gate: `R66-R2-R2 direct-step execution package WRITTEN -> ChatGPT PM durable intake only`.

## MVP alignment and Thread assessment

Approved MVP claim remains one concrete local `linux/arm64` Collector candidate build/image acceptance. Phase 1 advanced the exact materialization prerequisite, while the actual build/image claim remains unproven. No new product capability, runtime topology, evidence framework, remote action, or production claim was added. Classification: `MVP-ALIGNED WITH EXECUTION-PROTOCOL WARNING`.

This output is long. The current execution Thread must not continue because the one-shot A5 authority is terminal. Any subsequent work should use a new Thread after PM durable intake.
