# Sprint 4 D2-R7B-I1 R66-R2-R1 Pre-Write Read-Only Git Invocation Corrected Direct-Step Fresh One-Shot Local Collector Build/Image Acceptance Execution Report

## Conclusion

`HOLD / SOURCE_ARCHIVE_MEMBER_PREFIX_VALIDATION_FAILURE`

This fresh A4 authority was consumed when its exclusive temporary and evidence roots were created. The first post-write materialization safety check rejected the top-level `source` directory member in the exact Git source archive because that direct-step parser required every member name to begin `source/`. No repair, alternate parsing, re-archive, re-extraction, retry, cleanup, Docker call, or later phase was performed.

## Authority and corrected pre-write boundary

- Task: `D2-R7B-I1 R66-R2-R1`
- Attempt: `d2-r7b-i1-r66-r2-r1-934ced7-a4`
- Authority: `PM-D2-R7B-I1-R66-R2-R1-PREWRITE-READONLY-GIT-CORRECTED-DIRECT-STEP-FRESH-ONE-SHOT-260731-1740`
- Product commit: `934ced7b9659cb566628b1709cf6d73463a534d8`
- A3: historical pre-write Chat HOLD only; its report, evidence root, and temporary root were confirmed absent before A4 creation.

The correction was used exactly as authorized: normal recovery used direct read-only shell Git calls, and the two recursive smoke commands used one bounded inline Python invocation with `shell=False` and absolute executable `/usr/bin/git`. Its exact argv were:

```text
/usr/bin/git -C /Users/chenjie/Documents/MES/edge-mes-demo ls-tree -r -z --full-tree 934ced7b9659cb566628b1709cf6d73463a534d8 -- collector/Dockerfile collector/requirements.txt collector/app common
/usr/bin/git -C /Users/chenjie/Documents/MES/edge-mes-demo ls-tree -r -z --full-tree 934ced7b9659cb566628b1709cf6d73463a534d8 -- config/mapping.yaml
```

The smoke passed: `38` in-scope regular source blobs and `1` regular mapping blob, no tree/symlink/submodule/duplicate/scope escape accepted. All A4 paths were constructed from complete filenames with `Path / filename`; the direct-step plan contained exactly nine Docker argv, one build, one validation container, one probe, and no planned harness/source output, tag, retry, or cleanup.

## Entry evidence and preservation

Fresh recovery completed before the first task-owned write: `main`, `HEAD = origin/main = 0e7544a12b00799780d76723ca0de781bc2e8ad7`, ahead/behind `0/0`, empty tracked/cached diffs and whitespace checks, and product-source ancestry PASS. Untracked membership was `344 / 344 / 0 / 0 / 0`; Batch D/E exact-path expressions accounted for `301`, with the authorized non-Batch current set accounting for `43`. The A4 report/evidence/attempt paths were absent, non-symlink, and unindexed.

The SR4-R1 report/probe/test/lock identities matched `6894/2eec0e…b1155`, `15785/f09a78…a428b`, `10050/7fd4e9…2a8e7`, and `4428/012df4…c178`. The A1/A2 reports and terminal-01 records matched their frozen identities, and their temporary roots remained present, real directories, and untouched. The exact mapping working-tree identity was `7112` bytes, `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`.

## A4 materialization HOLD

The exact source and mapping `git archive` calls each ran once and wrote only their authorized A4 temporary captures. The phase-local standard-library archive validation then stopped on the initial top-level source archive directory member named `source`; it did not match the parser's required `source/` prefix. The parser had already exclusively created the two authorized materialized directory roots, but it accepted no source file for extraction, did not create the mapping file, and did not establish the required three-way `38 + 1` materialization closure.

Record 01 is direct-final HOLD:

- `docs/reports/evidence/d2_r7b_i1_r66_r2_r1_direct_step_local_build_image_acceptance/01_source_materialization.json`
- `2140` bytes
- SHA-256 `08036b86f12154dda006d63ed7fb233f7eeb1f9d2ac590539e4898d7a790e92a`

Records 02–05 were not created. Commands 1–9 were not executed.

## Docker, Git, and non-claims

```text
Docker calls / network-capable / daemon-mutating = 0 / 0 / 0
Builds / validation containers / probes          = 0 / 0 / 0
Tags / retries / cleanup                         = 0 / 0 / 0
Git stage / commit / push / tag                  = 0 / 0 / 0 / 0
Remote / deployment / activation / runtime       = 0 / 0 / 0 / 0
```

No immutable base, builder, sealed candidate ID, Config digest, RootFS, copied-source closure, dependency-pin comparison, mapping/import/action probe, or container-isolation topology was observed. This report is local attempt evidence only and makes no archive, transport, remote-load, deployment, activation, runtime-loaded, or production-accepted claim.

No executable harness, module, script, source output, extra durable evidence record, or evidence-root sidecar was created. The only repository writes are this report and record 01; the only A4 temporary objects are the two exact archives and the authorized materialized roots created before the HOLD.

## Status, recommendation, and MVP alignment

```text
R66-R2-R1 EXECUTED      = NO
LOCAL CANDIDATE BUILT   = NO
LOCAL IMAGE ACCEPTED    = NO
PM ACCEPTED             = NO
ARCHIVED                = NO
TRANSPORTED             = NO
REMOTE LOADED           = NO
DEPLOYED                = NO
ACTIVATED               = NO
RUNTIME-LOADED          = NO
PRODUCTION-ACCEPTED     = NO
```

Blocker: the authority's sole materialization parser path terminalized on the root-directory prefix check. Recommendation: ChatGPT PM may assess whether a separately authorized, fresh attempt should recognize a safe archive root-directory member while retaining all path/link/special-file checks. No repair is authorized here.

MVP alignment is `MVP-ALIGNED`: the stopped work remained confined to the approved local candidate materialization safety boundary and added no product capability, infrastructure, remote operation, runtime topology, or production assertion.

Next gate: `R66-R2-R1 direct-step execution package WRITTEN -> ChatGPT PM durable intake only`. This task is `WRITTEN` only; it is not reviewed, accepted, staged, committed, pushed, or a grant for any later phase.
