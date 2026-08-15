# Edge MES Demo — ChatGPT PM Handoff — 2026-07-31 11:45 CST

## 1. Handoff identity

- Project: Edge MES Demo
- Project absolute path: `/Users/chenjie/Documents/MES/edge-mes-demo`
- Handoff file: `docs/thread_handoff/chatgpt_pm_handoff_260731-1145.md`
- Handoff time basis: China Standard Time / UTC+8
- Trigger: the user explicitly requested entry into the ChatGPT PM handoff workflow and instructed that the next Gate be managed by a new ChatGPT PM window.
- Current handoff status: `WRITTEN / UNSTAGED / UNCOMMITTED / UNPUSHED`

This handoff records the completed planning/review chain and the next eligible development Gate. It does not itself authorize Architecture / Integration, Reliability, Data Quality, Verification, producer/parser implementation, tests, execution lock, Docker, R66, Git mutation, remote, deployment, runtime or production work.

No task authority remains active from the previous PM window. Every previously issued one-shot Thread authority has been consumed and terminalized.

## 2. Live Git baseline

Fresh read-only recovery immediately before this handoff established:

```text
repository:
/Users/chenjie/Documents/MES/edge-mes-demo

branch:
main

HEAD:
0e7544a12b00799780d76723ca0de781bc2e8ad7

origin/main:
0e7544a12b00799780d76723ca0de781bc2e8ad7

ahead / behind:
0 / 0

tracked diff:
empty

cached diff:
empty

git diff --check:
PASS

git diff --cached --check:
PASS

product source ancestry:
934ced7b9659cb566628b1709cf6d73463a534d8 is an ancestor of HEAD
```

Recent committed history:

```text
0e7544a Add PM handoff for build image execution preparation
796c87b Accept build image planning contract
c3acb33 Sync post-closeout status and PM handoff
934ced7 Accept runtime-loaded observability implementation
4a733d7 Add PM handoff before runtime-loaded implementation
ce22ca7 Add ChatGPT PM handoff after authority-chain closeout
35c50b1 Materialize current Collector activation authority chain
2d7ff45 Materialize repository governance and hygiene inventory
```

Commit `0e7544a12b00799780d76723ca0de781bc2e8ad7` is pushed to `origin/main` and contains the earlier PM handoff:

```text
docs/thread_handoff/chatgpt_pm_handoff_260730-2027.md
```

The docs/governance HEAD is not the product source and must not be used as a Docker build context authority. Exact Collector product source authority remains:

```text
934ced7b9659cb566628b1709cf6d73463a534d8
```

## 3. Last committed planning closeout

The latest committed and pushed build/image planning closeout remains:

```text
docs/reports/sprint4_d2_r7b_i1_r64_final_planning_acceptance_and_status_sync.md

commit:
796c87b395e6e153665a3e58e490490e2f1c1d8b

message:
Accept build image planning contract
```

R64 recorded:

```text
Architecture / Integration planning = PASS
Reliability review                   = PASS
Data Quality review                  = PASS WITH RECOMMENDATIONS
Verification review                  = PASS WITH RECOMMENDATIONS
PM final planning acceptance         = YES
static review stopping rule          = REACHED
```

`docs/current_status.md` and `docs/roadmap.md` remain committed governance snapshots from that closeout. They do not yet contain the later untracked R65-R6-SR2 authority chain described below. They must not be silently edited or treated as if they already record the newer gates.

## 4. Current uncommitted active planning contract

The current active external planning contract is the combined authority:

```text
R65-R6-SR1
+ accepted SR2-R1 limited candidate-bound producer/topology supersession
+ accepted SR2-R4 limited strict JSON/action/status grammar supersession
```

### 4.1 Base scope-reset contract

```text
path:
docs/reports/sprint4_d2_r7b_i1_r65_r6_sr1_scope_reset_minimal_external_build_image_acceptance_contract.md

bytes:
23402

SHA-256:
e2108e4e870e6681d2594e5832113b7032355e2274effc82d7acea2c3172872d

state:
WRITTEN
regular / non-symlink
untracked / unstaged / uncommitted / unpushed
```

SR1 remains controlling for exact product source/materialization, attempt ownership, predecessor gates, Docker budget, required terminals `01–10`, stop/no-retry/no-cleanup rules and local-only truth boundary.

### 4.2 Candidate-bound producer/topology repair

```text
path:
docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r1_corrected_product_source_package_path_candidate_probe_binding_repair.md

bytes:
15975

SHA-256:
aec7cefe779e39abeeac7db747b91f8a236ce6ea544f875164520398cebb66cf

state:
WRITTEN
PM ACCEPTED
regular / non-symlink
untracked / unstaged / uncommitted / unpushed
```

SR2-R1 closes the original missing candidate-bound actual producer gap. It establishes one read-only mounted, execution-locked producer, one validation container, one command-8 producer invocation/probe, one stdout JSON document and direct candidate actual inputs for terminals 06, 07 and 09.

### 4.3 Strict record-grammar repair

```text
path:
docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r4_minimal_probe_record_grammar_repair.md

bytes:
17288

SHA-256:
c0ee5bb04c989954e80e089816b72287f60c5b18671077bc4e883eb933b8d31a

state:
WRITTEN
PM ACCEPTED
regular / non-symlink
untracked / unstaged / uncommitted / unpushed
```

SR2-R4 adds only the finite fail-closed external record grammar required by the Data Quality review:

- strict UTF-8, no BOM, one root JSON object;
- recursive duplicate-key rejection before materialization;
- exact integer schema version `1`;
- exact closed 14-key root;
- closed nested source/distribution/mapping/import/action records;
- exact ten-key zero-only `action_observations`;
- explicit `verdict == "PASS" AND probe_exit == 0` success predicate plus complete grammar/binding/semantic checks;
- one parse and one immutable logical object consumed by terminals 06/07/09.

SR2-R4 does not add a schema registry, required sidecar, terminal 11, second producer, second probe or additional Docker call.

## 5. Accepted independent review chain

All review reports below are durable review authority but remain untracked and uncommitted. They do not replace the active execution contract.

### 5.1 Reliability review

```text
path:
docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r2_r1_corrected_utf8_prewrite_audit_focused_reliability_review.md

bytes:
13032

SHA-256:
87cb8d69a429278f1b1c9ec81243a7e7c61dccafdecc00e63fc74f416d740601

state:
RELIABILITY REVIEWED
RELIABILITY PM ACCEPTED
REL-001 through REL-009 CLOSED
regular / non-symlink
untracked / unstaged / uncommitted / unpushed
```

Reliability Gate:

```text
PASS / CLOSED
```

### 5.2 Initial Data Quality HOLD review

```text
path:
docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r3_focused_data_quality_review_of_candidate_probe_binding_contract.md

bytes:
26581

SHA-256:
b7a991c45c369827669967542f9e1a70d6f09f7d92413702b3bfc04ad28e7449

state:
INITIAL DATA QUALITY REVIEWED
HOLD findings PM ACCEPTED
regular / non-symlink
untracked / unstaged / uncommitted / unpushed
```

This report identified the three finite record-grammar blockers later repaired by SR2-R4:

```text
PM-R65-R6-SR2-R3-DQ-001
STRICT_PROBE_JSON_RECORD_GRAMMAR_ABSENT

PM-R65-R6-SR2-R3-DQ-002
ACTION_OBSERVATION_COMPLETENESS_GRAMMAR_ABSENT

PM-R65-R6-SR2-R3-DQ-003
PROBE_SUCCESS_TRUTH_TABLE_ABSENT
```

### 5.3 Focused Data Quality rereview

```text
path:
docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r5_focused_data_quality_rereview_of_minimal_probe_record_grammar_repair.md

bytes:
17002

SHA-256:
b715c8678a8af1eacc0b6281ab78df231f604a63cd6b25fbeb5d2f1a7b54b3d4

state:
DATA QUALITY REREVIEWED
DATA QUALITY REREVIEW PM ACCEPTED
regular / non-symlink
untracked / unstaged / uncommitted / unpushed
```

The three original blockers are closed and the original eight `NO ISSUE` findings are preserved.

Data Quality Gate:

```text
PASS / CLOSED
```

### 5.4 Focused Verification review

```text
path:
docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r6_focused_verification_review_of_candidate_probe_contract.md

bytes:
27983

SHA-256:
9c4b74a49e86d6f989e845f5afd6255b250f77b7313bc33f4a3ac3d255192426

state:
VERIFICATION REVIEWED
VERIFICATION PM ACCEPTED
V-001 through V-012 VERIFIABLE
regular / non-symlink
untracked / unstaged / uncommitted / unpushed
```

Verification confirms:

- the SR1/SR2-R1/SR2-R4 supersession chain is uniquely resolvable;
- producer/parser/test/execution-lock identities can be frozen without another contract repair;
- strict parser, source/distribution, action/status, command 7/8/9, terminal 06/07/09, terminal 10 and failure/no-reuse invariants have finite deterministic conceptual fixtures;
- expected and actual oracles remain independent;
- command 7/8/9 fit the retained Docker budget `9 / 5 / 5`;
- no `docker run`, `docker exec`, `docker cp`, second container, second probe or tenth Docker call is required;
- implementation/test responsibility and later R66-only execution responsibility are separable.

Verification Gate:

```text
PASS / CLOSED
```

## 6. Current PM-accepted state

The latest PM durable intake state is:

```text
R65-R6-SR2-R1 WRITTEN / PM ACCEPTED = YES / YES
RELIABILITY REVIEWED / PM ACCEPTED   = YES / YES
DATA QUALITY GATE                    = PASS / CLOSED
VERIFICATION REVIEWED / PM ACCEPTED  = YES / YES
VERIFICATION GATE                    = PASS / CLOSED

PRODUCER IMPLEMENTED                 = NO
PRODUCER TESTED                      = NO
PARSER IMPLEMENTED                   = NO
PARSER TESTED                        = NO
FIXTURES IMPLEMENTED                 = NO
TESTS EXECUTED                       = NO
EXECUTION LOCKED                     = NO
BUILD READY                          = NO
R66 AUTHORIZED                       = NO
BUILT                                = NO
LOCAL IMAGE ACCEPTED                 = NO
REMOTE / RUNTIME / PRODUCTION CLAIM  = NO
```

Most recent PM acceptance ID:

```text
PM-D2-R7B-I1-R65-R6-SR2-R6-INTAKE-ACCEPTED-260731-1140
```

There are no open Reliability, Data Quality or Verification blockers in the accepted planning contract.

## 7. Recommended next development Gate

The single recommended next Gate is:

```text
Independent producer/parser implementation,
unit/static fixture testing,
and execution-lock materialization
```

This is a new implementation/test Gate. It was not dispatched from the previous PM window and has no active authority.

Recommended responsibility:

- materialize the exact project-specific candidate evidence producer;
- materialize its exact tests and any minimum parser/fixture artifact explicitly authorized by the new PM;
- implement the strict SR2-R4 external record grammar;
- implement candidate source inventory, complete installed-distribution inventory, mapping/import/action observations and the finite status truth table;
- implement pure unit/static fixtures for byte framing, duplicate keys, root/nested cardinality, types, missing/default rejection, distribution canonicalization, ten-action completeness, status combinations, command-shape/budget, terminal suppression, terminal 10 closure and no-reuse behavior;
- run only explicitly authorized non-Docker implementation tests;
- prove source/test/executed implementation identity;
- freeze producer/parser/test bytes and command representation in an execution-lock record before any later R66 authority.

Previously reserved future producer/test paths are currently absent:

```text
docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/candidate_evidence_producer.py

docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/test_candidate_evidence_producer.py
```

The next PM must independently decide the exact report/artifact paths, implementation boundary, test command, execution-lock record and allowlist before issuing the Gate. Do not infer write authority merely from these reserved paths.

The implementation/test Gate must not authorize Docker or R66. The following remain later R66-only observations under a separate authority:

- actual candidate filesystem inventory;
- actual candidate installed distributions;
- actual mapping mount/import/action observation inside the validation container;
- command-9 inspect topology and actual exit;
- full Docker external-call budget and terminal publication;
- candidate build/image acceptance.

## 8. Retained scope and stopping rules

The next PM must preserve the accepted MVP boundary:

```text
MVP claim:
one concrete local linux/arm64 Collector candidate build/image acceptance

minimum invariant:
terminals 06/07 actual evidence must be mechanically candidate-bound,
fail-closed and mechanically testable
```

Retained external constraints:

- exact product source `934ced7b9659cb566628b1709cf6d73463a534d8`;
- exactly one producer;
- exactly one validation container;
- exactly one producer invocation/probe;
- exactly one stdout JSON document;
- exactly one authority-bearing parser policy;
- Docker external budget `9 / 5 / 5`;
- one build;
- tag/reference calls `0`;
- retry `0`;
- cleanup `0`;
- required durable terminals exactly `01–10`;
- terminal 10 audits `01–09` and self-excludes;
- no terminal 11;
- no required raw/normalized durable sidecars;
- no P/H/C invocation ledger;
- no fixed internal helper/parser/function call counts;
- no generic schema registry or evidence framework;
- no SBOM, offline mirror, hash-lock, reproducibility, forensics or retention expansion;
- no archive, transport, remote load, deployment, activation, runtime or production claim.

Future implementation style, internal class/function names, parser library and test framework are not current contract authority. They may be chosen minimally by the new PM Gate as long as external invariants and exact locked bytes remain testable.

## 9. Exact dirty and external-artifact boundary

Before this handoff was written, the exact expected/live untracked set was:

```text
323 raw / 323 unique
= Batch D 300
+ Batch E 1
+ R56–R65-R6-SR1 reports 15
+ previous current handoff 1
+ SR2-R1 / Reliability / initial Data Quality / SR2-R4 / SR2-R5 / SR2-R6 6

duplicate / unknown / missing:
0 / 0 / 0
```

After this handoff is written, the expected exact untracked set is:

```text
324 raw / 324 unique
= previous 323
+ this handoff 1

duplicate / unknown / missing:
0 / 0 / 0
```

Batch D/E membership may be read only through the fixed expressions in:

```text
docs/reports/evidence/d2_r7b_i1_r36_working_tree_hygiene_authority_materialization/authority_materialization_plan.json

.batches[] | select(.batch_id == "D") | .exact_paths[]
.batches[] | select(.batch_id == "E") | .exact_paths[]
```

Batch D/E contents must not be read. All untracked paths remain external to future tasks unless explicitly named in a new exact allowlist.

In particular:

- Batch D/E content must not be read, modified, deleted, staged or committed;
- R56–SR2-R6 reports must not be absorbed through broad staging;
- this handoff must not be staged automatically;
- old handoffs, `.gitignore`, Keynote/reporting artifacts, frontend generated artifacts and unrelated files remain excluded;
- `git add .`, `git add -A` and `git add docs/` are forbidden.

## 10. Surfaces not authorized by this handoff

This handoff does not authorize:

- modifying product source, tests, Dockerfile, requirements, Compose or mapping;
- modifying `docs/current_status.md`, `docs/roadmap.md`, PM Rules or any existing report;
- creating producer, parser, helper, fixture, test, manifest, terminal or execution-lock artifacts;
- running application, producer, parser or fixture tests;
- source/mapping archive creation or extraction;
- attempt/evidence-root creation;
- Docker daemon access, BuildKit, buildx, pull, build, inspect, container create/start/inspect, save, load, tag or cleanup;
- package resolution or installation;
- network, registry, SSH or remote operations;
- DB, API, Dashboard, PLC, V-PLC, ACK or `read_done` operations;
- archive transport, deployment, restart, activation, rollback or runtime validation;
- retry, cleanup, takeover or deletion;
- Git stage, commit, push or tag;
- BUILD READY, R66 AUTHORIZED, BUILT, LOCAL IMAGE ACCEPTED, remote-loaded, runtime-loaded or production-accepted claims.

## 11. Recommended first action for the next ChatGPT PM

1. Read `docs/thread_handoff/pm_operating_rules.md`, especially Sections 9–13.
2. Read `docs/current_status.md` and `docs/roadmap.md`, while recognizing that they predate the later untracked SR2 chain.
3. Read R60, R64, SR1, accepted SR2-R1, Reliability, initial Data Quality, accepted SR2-R4, accepted SR2-R5, accepted SR2-R6 and this handoff.
4. Run fresh read-only recovery and independently verify live `HEAD`, `origin/main`, ahead/behind, tracked/cached diffs and exact untracked membership.
5. Verify the exact bytes/SHA-256 and untracked/unstaged state of SR1, SR2-R1, SR2-R4, SR2-R5, SR2-R6 and this handoff.
6. Confirm future producer/test paths remain absent.
7. Confirm all prior one-shot authorities are terminal and no implementation/test authority was inherited.
8. Report PM takeover state only: current closed gates, 324-path dirty baseline, no active authority and the recommended single next Gate.
9. Do not issue the implementation/test Prompt until the user gives a fresh explicit instruction in the new PM window.
10. When instructed, reread PM Rules Section 10 immediately before dispatch and issue one complete self-contained Prompt with exact report/artifact paths, test allowlist, execution-lock fields and explicit `Docker calls = 0`.

## 12. Copyable prompt for the next ChatGPT PM window

```text
你是 Edge MES Demo 项目的新任 ChatGPT PM。

项目绝对路径：
/Users/chenjie/Documents/MES/edge-mes-demo

你的第一项工作只是完成PM接管与read-only recovery。不要自动发布或执行implementation、test、Docker、R66、Git、remote、runtime或production任务。

必须先按顺序读取：
1. docs/thread_handoff/pm_operating_rules.md
2. docs/current_status.md
3. docs/roadmap.md
4. docs/reports/sprint4_d2_r7b_i1_r60_scope_reset_minimal_exact_commit_collector_build_image_planning_repair.md
5. docs/reports/sprint4_d2_r7b_i1_r64_final_planning_acceptance_and_status_sync.md
6. docs/reports/sprint4_d2_r7b_i1_r65_r6_sr1_scope_reset_minimal_external_build_image_acceptance_contract.md
7. docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r1_corrected_product_source_package_path_candidate_probe_binding_repair.md
8. docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r2_r1_corrected_utf8_prewrite_audit_focused_reliability_review.md
9. docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r3_focused_data_quality_review_of_candidate_probe_binding_contract.md
10. docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r4_minimal_probe_record_grammar_repair.md
11. docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r5_focused_data_quality_rereview_of_minimal_probe_record_grammar_repair.md
12. docs/reports/sprint4_d2_r7b_i1_r65_r6_sr2_r6_focused_verification_review_of_candidate_probe_contract.md
13. docs/thread_handoff/chatgpt_pm_handoff_260731-1145.md

随后执行fresh read-only recovery：
- git status -sb
- git log -8 --oneline --decorate
- git rev-parse --show-toplevel
- git rev-parse --abbrev-ref HEAD
- git rev-parse HEAD
- git rev-parse origin/main
- git rev-list --left-right --count HEAD...origin/main
- git diff --name-only
- git diff --cached --name-only
- git diff --check
- git diff --cached --check
- git -c core.quotePath=false ls-files --others --exclude-standard
- git merge-base --is-ancestor 934ced7b9659cb566628b1709cf6d73463a534d8 HEAD

当前预期live baseline：
- branch: main
- HEAD == origin/main: 0e7544a12b00799780d76723ca0de781bc2e8ad7
- ahead/behind: 0/0
- tracked diff: empty
- cached diff: empty
- untracked after handoff: 324 raw / 324 unique
- duplicate / unknown / missing: 0 / 0 / 0

Product source authority：
934ced7b9659cb566628b1709cf6d73463a534d8

Active external planning contract：
- SR1 base scope-reset contract
- accepted SR2-R1 candidate-bound producer/topology supersession
- accepted SR2-R4 strict JSON/action/status grammar supersession

Accepted review state：
- Reliability Gate: PASS / CLOSED
- Data Quality Gate: PASS / CLOSED
- Verification Gate: PASS / CLOSED
- V-001 through V-012: VERIFIABLE
- remaining planning blockers: none

Current implementation/execution state：
- PRODUCER IMPLEMENTED / TESTED: NO / NO
- PARSER IMPLEMENTED / TESTED: NO / NO
- FIXTURES IMPLEMENTED: NO
- TESTS EXECUTED: NO
- EXECUTION LOCKED: NO
- BUILD READY: NO
- R66 AUTHORIZED: NO
- BUILT / LOCAL IMAGE ACCEPTED: NO / NO
- REMOTE / RUNTIME / PRODUCTION CLAIM: NO

所有SR1至SR2-R6报告均为当前checkout中的untracked、unstaged、uncommitted durable authority。不得误称为committed，也不得通过broad Git add吸收。

推荐的单一next Gate：
Independent producer/parser implementation, unit/static fixture testing, and execution-lock materialization.

该Gate尚未下发，没有active authority。它必须与later R66分开：implementation/test Gate不得运行Docker；actual candidate filesystem、installed distributions、container inspect和Docker预算只能在后续独立R66 authority下执行。

future producer/test reserved paths当前应为ABSENT：
- docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/candidate_evidence_producer.py
- docs/reports/evidence/d2_r7b_i1_r65_r3_candidate_evidence_producer_implementation/test_candidate_evidence_producer.py

完成接管后，只汇报：
1. live Git baseline；
2. handoff和key reports身份；
3. Reliability/Data Quality/Verification Gate状态；
4. 324-path membership；
5. no active authority；
6. recommended next Gate。

不要从本handoff自动发布下一Prompt。等待用户在新PM窗口中的明确指令。后续任何Thread Prompt必须重新读取PM Rules Section 10，并使用一个完整可复制Markdown块，明确exact outputs、allowlist、test budget、execution-lock fields、Git权限和Docker calls = 0。
```

## 13. Handoff Git closeout

This handoff is intentionally left:

```text
UNSTAGED
UNCOMMITTED
UNPUSHED
```

PM Rules require separate explicit exact-path authorization before staging it.

If the user later authorizes handoff Git closeout, the only default staged path is:

```text
docs/thread_handoff/chatgpt_pm_handoff_260731-1145.md
```

Suggested commit message:

```text
Add PM handoff before producer implementation gate
```

Before commit, verify:

```text
git diff --cached --name-only
git diff --cached --check
git diff --cached --stat
```

Do not stage SR1–SR2-R6 reports, Batch D/E, `.gitignore`, old handoffs, reporting artifacts, frontend generated files or unrelated paths.
