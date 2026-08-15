# Sprint 4 D2-R7B-I1 R65-R6-SR4-R1 Minimal Attempt-ID Parameterization and Fresh-Attempt Re-lock Report

## Conclusion

- Task: `D2-R7B-I1 R65-R6-SR4-R1`
- Thread: `Architecture / Integration` (new isolated implementation Thread)
- Authority: `PM-D2-R7B-I1-R65-R6-SR4-R1-ATTEMPT-ID-PARAMETERIZATION-RELOCK-260731-1610`
- Delivery: `REPOSITORY_REPORT_WITH_ARTIFACTS`
- Conclusion: `PASS / MVP-ALIGNED`

```text
SR4-R1 WRITTEN                 = YES
ATTEMPT-ID PARAMETERIZED       = YES
FOCUSED TEST PASSED            = YES
EXECUTION LOCK REPLACED        = YES
PM ACCEPTED                    = NO
BUILD READY                    = NO
R66-R1 AUTHORIZED              = NO
```

This is local/static/synthetic package evidence only. It does not authorize or execute R66-R1, Docker, network, remote, Git mutation, build, runtime, or production work.

## Entry gates and preserved history

The authoritative task file was read first and matched its required identity: `9062` bytes and SHA-256 `1f5f888d946965f246cb6ae095116b96679e1f5a9171a47185a16691149923c1`. The prescribed reading order was completed before any write.

Fresh read-only recovery established `main`, `HEAD = origin/main = 0e7544a12b00799780d76723ca0de781bc2e8ad7`, ahead/behind `0 / 0`, empty tracked and cached diffs, passing whitespace checks, and product source ancestry from `934ced7b9659cb566628b1709cf6d73463a534d8`. The untracked membership gate was `338 / 338 / 0 / 0 / 0`; Batch D/E were read solely through the two authorized `.exact_paths[]` expressions (`300` and `1` members), without reading their contents. The report path was absent, non-symlink, and not indexed before creation.

The old R66 attempt was retained unchanged and historical only:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| old R66 task | 25364 | `a2e0a44a76bba07114c59f7701f626dcb6f931d076f355d7dd11500d764a3307` |
| old R66 HOLD report | 3457 | `9e59fab8af625283247a36657fec0eb475f485ca3a334fb42b7c89ae8379f74f` |
| old R66 terminal 01 | 620 | `6e93008ed04275851ed6cfff0d84b1135adc45a90e7d01404a035c9290911a4b` |

No old attempt root, report, terminal, or task file was modified, cleaned up, or used as fresh execution authority.

## Parameterized exact binding

`candidate_probe.py` no longer carries the terminalized `d2-r7b-i1-r66-934ced7-a1` module literal. `validate_attempt_id` now requires a nonempty `str` with no NUL, no leading/trailing whitespace, and at most 128 UTF-8 bytes. `validate_probe_record` requires an expected `attempt_id` and compares the record to caller-supplied expected values exactly; missing, null, empty, wrong-type, malformed, or mismatched values reject fail-closed. `build_record` validates and uses only the exact CLI value.

The CLI remains exactly `--attempt-id`, `--candidate-full-id`, `--producer-sha256`, and `--mapping-sha256`; `--attempt-id` is required and has no default. No trimming, fallback, environment lookup, or old-history authority is present. The fresh value `d2-r7b-i1-r66-r1-934ced7-a2` is a test fixture only, not execution authorization.

The focused test proves that a historical matching record can parse and match only caller-supplied historical expectation, while the historical/fresh cross-mismatches both reject. Thus historical syntax is not an embedded reuse authority, and any future execution must provide its own PM-authorized exact expected ID.

## Focused validation and immutable re-lock

The only test suite exercised was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m pytest -p no:cacheprovider docs/reports/evidence/d2_r7b_i1_r65_r6_sr4_minimal_execution_package/test_candidate_probe.py -q
```

Test-first RED initially produced `4 failed, 9 passed`: fresh binding was blocked by the old literal and the strict attempt-ID validator was absent. The minimal implementation then produced `13 passed in 0.04s`, exit `0`, skipped `0`, xfailed `0`. This is one focused suite path and count `13`, within the required `>11` and `<=30` interval. Repair cycles: `0`; the RED-to-GREEN implementation is the initial change, not a post-implementation repair. A transient read-only lock-audit selector used CLI index `5` instead of `4`; it changed no artifact and the corrected closed-key/UTF-8 JSON audit passed, so it is not a repair cycle.

Probe and test identities were captured immediately after the final suite and again after lock creation; both observations match:

| Artifact | Old bytes / SHA-256 | New bytes / SHA-256 |
| --- | --- | --- |
| probe | 15058 / `5bfe166126719347dfabd7507ecf0fb293c26a2377abf0f696458377b1d4bd6a` | 15785 / `f09a78369b8c8ad247dd79c2e4e7afb7147844fa9db4d75d1939b01f674a428b` |
| test | 8594 / `3168a3ecb7a21d21445f9f035f88a0bdb02541dd0368a38aeb32c885109bc55a` | 10050 / `7fd4e93fc09392a706b3ddf3c25dcd29967396cddba7faf3181ac7cabca2a8e7` |
| lock | 4408 / `9522fbfaf27a146daa715b5e332aacf7a5c4032a5cc0dc11e9d8a2dd8aee8c26` | 4428 / `012df4bbcccaf3084d3e79a3f0468eeb9f12e496662dc2e75a2e0f5bb5d1c178` |

The replacement lock keeps schema-v1 and exactly 14 top-level keys. It has contract ID `d2-r7b-i1-r65-r6-sr4-r1-attempt-parameterized-minimal-execution-package-v1`, explicitly supersedes the prior SR4 lock, and records `<pm-authorized-attempt-id>` in the CLI. It states that exact fresh-attempt authority can arise only from a future PM execution Prompt, never a default or module constant. The post-lock closed-key and UTF-8 JSON audit passed; probe, test, and lock are immutable after this point.

## Scope, counters, and boundary

| Budget or boundary | Result |
| --- | --- |
| probe / test / lock bytes | 15785 / 10050 / 4428; all within 24576 / 24576 / 8192 |
| focused collected tests | 13; PASS |
| extra cache, bytecode, helper, sidecar, probe, test, or lock | 0 |
| Docker / network / remote / package installation | 0 / 0 / 0 / 0 |
| Git stage / commit / push / tag | 0 / 0 / 0 / 0 |
| product, Dockerfile, requirements, mapping, status, roadmap, PM Rules, old R66 artifacts | unchanged |

The final required membership target after this exact report is `339 / 339 / 0 / 0 / 0`. Writing this report establishes only `WRITTEN`; it is not PM acceptance, build readiness, or R66-R1 authority.

## MVP alignment and next gate

Approved MVP claim: one concrete local `linux/arm64` Collector candidate build/image acceptance. This repair prevents a concrete false HOLD/reuse error at its minimal local probe boundary while retaining exact caller binding. It adds no product capability, runtime topology, generic authority framework, audit/retention system, or new execution surface. Classification: `MVP-ALIGNED`.

The single next gate is `SR4-R1 attempt-parameterized package WRITTEN -> ChatGPT PM durable intake only`. PM must read and accept the exact report and three artifacts before it can issue any fresh R66-R1 execution authority. No execution, publication, or Docker action is inherited from this result.
