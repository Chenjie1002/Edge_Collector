# P1-G3 Process KPI + OEE Data-Sufficiency Contract Report

## 1. Durable identity and conclusion

报告名称：P1-G3 Process KPI + OEE Data-Sufficiency Contract Report

任务名称：P1_G3_PROCESS_KPI_CONTRACT_20260811T1505Z

执行 Thread：Data Quality（一次性 disposable contract specialist）

结论：PASS WITH RECOMMENDATIONS

本报告与 contract 只证明本 task-owned outputs 已 WRITTEN 并完成 local static semantic checks；不证明 ACCEPTED、VERIFIED、G4 ready、API implementation、DB-backed、runtime、remote、deployed、activated 或 production acceptance。

### 1.1 Task identity

    path = docs/thread_handoff/pm_task_20260811T1505Z_p1_g3_process_kpi_contract.md
    type = regular / non-symlink
    bytes = 21068
    SHA-256 = 78f0a6c80cb465a84ed2485c551139c22dffd01e209270aa9d9c314fc908aca7
    authority = exact launcher-matching task; no inherited authority

### 1.2 Read-only authority inputs

    docs/thread_handoff/shadow_pm_p1_process_kpi_bounded_api_local_charter.md
      regular/non-symlink; bytes=20025; SHA-256=cfc05c53ef03f890cf5be2228f47369c2042457294384b82db9bd85b8c348dd3

    docs/reports/p1_process_kpi_bounded_api_accepted_state_capsule.md
      regular/non-symlink; bytes=8201; SHA-256=643b2c39e1e37da542cf077be71d511e75035c0da08e6471f86a610e290a2b3a

    docs/contracts/production_metrics_contract.md
      regular/non-symlink; bytes=8229; SHA-256=2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e

    api/app/routes/quality_trace.py
      regular/non-symlink; bytes=9538; SHA-256=6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a

    api/app/main.py
      regular/non-symlink; bytes=464; SHA-256=2bdc34c1950654ca81d0041171a3c17d646c87e9655e79c3bac120baf47438ed

docs/thread_handoff/pm_operating_rules.md was read only at the task-relevant authority, durable-delivery, evidence-gate and MVP-alignment sections. It and all listed predecessor/neighbor inputs remained protected and unmodified.

### 1.3 Output identity

    artifact path = docs/contracts/production_process_kpi_contract.md
    artifact type = regular / non-symlink
    artifact bytes = 28427
    artifact SHA-256 = 776e744314f9ec33884765c20f8d88dab45afeda74354cf7e10e7fc226809252
    artifact role = accepted G3 contract candidate; WRITTEN only

    report path = docs/reports/p1_g3_process_kpi_contract_20260811T1505Z.md
    report type = regular / non-symlink
    report bytes = 020348
    report SHA-256 = 7167ca3f0df3facaffb2e05083040fe0e0a1f6cbba2a08f7a08ff217703e039b
    report SHA-256 scope = normalized self-identity: hash of the final report bytes after replacing both report normalized self-identity 64-hex fields with 64 ASCII zeroes; full-file SHA-256 is supplied in the Section 15 window manifest because a file cannot contain its own full-file hash without changing its bytes
    report role = durable G3 report; WRITTEN only

Report bytes and normalized self-identity are finalized mechanically after this draft is written and before the window manifest. This is identity finalization, not a semantic repair cycle.

## 2. Scope and evidence boundary

本 task 消费 accepted Capsule 与 predecessor Quality + Trace contract，只冻结 additive Process KPI/OEE data-sufficiency semantics。唯一 task-owned writes 是：

    docs/contracts/production_process_kpi_contract.md
    docs/reports/p1_g3_process_kpi_contract_20260811T1505Z.md

明确未触碰：production_metrics_contract.md、quality_trace.py、main.py、其他 source/test/docs、DB/schema/runtime/API execution、remote/SSH/Docker/PLC/V-PLC/frontend、Git mutation、Ledger/counter/gate、successor task。

本报告的证据类别是 local static semantic evidence。它不建立 DB-backed behavior、API HTTP behavior、runtime load、remote identity、production stimulus 或 P1-G5。

## 3. Fresh live facts before first write

    physical cwd = /Users/chenjie/Documents/MES/edge-mes-demo
    git root = /Users/chenjie/Documents/MES/edge-mes-demo
    branch = main
    HEAD = cf4eac54d3f365b0addfaae13f5e7292e3233641
    origin/main = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
    origin/main...HEAD = 0<TAB>2
    cached/staged sorted set = empty
    cached/staged normalized SHA-256 = 01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b
    tracked dirty sorted set = docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
    tracked dirty / diff normalized SHA-256 = 23bd287bbe2c67be880534ee9a77a1a57a5e5d105434dafede168b5bc2e2592d
    pre-write status sorted unique line count = 870
    pre-write status sorted unique SHA-256 = d8307d31c192494aad6d3580ced6a654b2a9da4c18328bc8a06a3be7eb58097a
    pre-write untracked line count = 868

Pre-existing tracked dirty docs and the large untracked corpus were treated as external continuity. No cleanup, adoption, broad staging or untracked-order drift classification was performed. After final publication, the status set with exactly the two task-owned output entries removed must reproduce the pre-write status hash.

## 4. Host control-plane evidence

The frozen exact entrypoint and primitive smoke were run before the first task-owned write:

    entrypoint = /opt/homebrew/opt/python@3.14/bin/python3.14
    resolved = /opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14
    version = Python 3.14.6
    architecture = arm64
    resolved type = regular / non-symlink
    resolved bytes = 52448
    resolved SHA-256 = b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf
    primitive smoke = PASS: pathlib.read_bytes, UTF-8 read_text, hashlib.sha256, json.dumps(sort_keys=True, ensure_ascii=False), UTF-8 encoding
    bytecode = not produced (-B)

No project runtime, project import, pytest, API request, DB query runtime, Docker, network, SSH or external call was run.

## 5. Frozen contract decisions

### 5.1 Accepted production truth and lineage

production_accepted_station_event_fact is the sole accepted production truth source. The accepted-result predicate is an accepted source row with event_type='station_result', exact line_id/station_id, half-open event timestamp, non-null unique fact_key, and an allowed result value. skip and not_applicable count as accepted station-result events but are excluded from the reused Quality denominator.

No numeric output reads, joins or falls back to production_snapshot, cycle_event, station_event, production_unit, quality_event, raw sample, normalized candidate, adapter diagnostics, ACK/read_done or legacy objects. fact_key is the deterministic identity and (event_ts, accepted_at, fact_key) is the deterministic order. Duplicate, conflicting or missing fact identity fails closed; no DISTINCT de-duplication, first/last selection or row-proximity repair.

Historical config semantics require exact accepted (config_hash, config_version) plus an independently accepted immutable historical profile. Current YAML is never historical authority. Mixed/unresolved config blocks terminal/order/line output, ideal CT, Performance, Availability and Full OEE numeric aggregation, while station event count, accepted Quality and calendar-window event rate may remain metric-level usable.

### 5.2 Metric decision matrix

| metric | source / lineage | counting unit | normal status | numeric rule | empty/source-unavailable |
| --- | --- | --- | --- | --- | --- |
| accepted_event_count | accepted station_result facts; unique fact_key | event-count | SUPPORTED | fact-row count only | valid empty 0; source/identity failure UNAVAILABLE, no value |
| observed_accepted_event_rate | accepted event count / calendar window duration | event-count | SUPPORTED | exact count / duration_seconds; not Performance | valid empty 0; never operating-time denominator |
| accepted_unit_count | no accepted one-to-one unit authority | unit-count | UNSUPPORTED | forbidden | never zero fallback |
| quality_good_event_count, quality_nok_event_count, quality_denominator_event_count | predecessor accepted Quality semantics | event-count | SUPPORTED | counts allowed; skip/not_applicable excluded from denominator | valid empty count zero; source failure no value |
| quality_rate | predecessor good/denominator | unavailable | SUPPORTED or PARTIAL | value only denominator > 0; PARTIAL value only for missing NOK detail/distribution | empty denominator UNAVAILABLE, no value |
| station_cycle_time | producer-authoritative shared cycle-instance start/complete key | unavailable | PARTIAL | forbidden without pairing authority | no zero; no adjacent/time/counter/legacy fallback |
| ideal_cycle_time | exact historical hash/version/profile lineage | unavailable | PARTIAL | forbidden without historical authority | no current-YAML/default fallback |
| line_accepted_event_count | no accepted line-output authority | unavailable | UNSUPPORTED | forbidden; station scope is not line aggregate | no zero |
| terminal_accepted_event_count | no accepted historical terminal lineage | unavailable | UNSUPPORTED | forbidden; no WS03 | no zero |
| performance | historical ideal CT + authoritative operating/run-time denominator | unavailable | UNSUPPORTED | forbidden; observed rate is not Performance | no zero |
| availability | planned time/downtime + authoritative run/stop/unknown timeline | unavailable | UNSUPPORTED | forbidden; query duration is not operating time | no zero |
| full_oee | independently accepted Quality + Performance + Availability authorities | unavailable | UNSUPPORTED | forbidden; no partial A/P multiplication | no zero |

### 5.3 Status/reason/source behavior

Metric/top-level statuses are exactly SUPPORTED, PARTIAL, UNAVAILABLE, UNSUPPORTED. value is omitted unless numeric_value_allowed=true; non-success metrics do not use null/zero/string fallback. Top-level aggregation is defined in contract section 5.3: source failure/identity failure is UNAVAILABLE; usable accepted-event/Quality metrics plus unsupported components is PARTIAL; unsupported metrics remain visible rather than being omitted.

Stable reason taxonomy includes ACCEPTED_FACT_QUERY_OK, CALENDAR_WINDOW_EVENT_RATE, EMPTY_ACCEPTED_WINDOW, QUALITY_DENOMINATOR_EMPTY, QUALITY_NOK_DETAIL_INCOMPLETE, FACT_IDENTITY_MISSING, FACT_IDENTITY_DUPLICATE_OR_CONFLICT, CYCLE_INSTANCE_PAIRING_AUTHORITY_MISSING, HISTORICAL_CONFIG_AUTHORITY_MISSING, MIXED_HISTORICAL_CONFIG_WINDOW, LINE_OUTPUT_AUTHORITY_NOT_ACCEPTED, HISTORICAL_TERMINAL_LINEAGE_UNAVAILABLE, PERFORMANCE_AUTHORITIES_NOT_ACCEPTED, AVAILABILITY_AUTHORITIES_NOT_ACCEPTED, FULL_OEE_REQUIRED_COMPONENTS_NOT_ACCEPTED, ACCEPTED_FACT_SOURCE_UNAVAILABLE, ACCEPTED_FACT_QUERY_FAILED and AUTHORITY_RESOLUTION_FAILED.

### 5.4 Exact endpoint/DTO

    GET /api/v2/process-metrics
    query = line_id, station_id, from, to; each exactly once
    from inclusive / to exclusive / RFC3339 timezone-aware UTC / max 31 days
    body = forbidden
    POST, PUT, PATCH, DELETE = forbidden
    unknown, duplicate, terminal/group/aggregate/metric/limit/scope query params = HTTP 422
    method violation = HTTP 405
    base accepted-fact/query failure = HTTP 503

The success DTO is contract_version, scope{line_id,station_id,aggregation=station}, window{from,to,interval=[from,to),duration_seconds}, top-level status, reason, source{authority,identity,config_window_state,fallback=none}, and a fixed metrics array. Each metric has name, unit, counting_unit, status, reason, source, numeric_value_allowed and optional numeric value. The fixed matrix is not shortened to hide unsupported claims.

Exact contract-only case fragments (all values are placeholders, not production evidence):

    supported count: name=accepted_event_count, unit=events, counting_unit=event-count, status=SUPPORTED, reason=ACCEPTED_FACT_QUERY_OK, source=production_accepted_station_event_fact/fact_key, numeric_value_allowed=true, value=<source-derived-integer>
    valid empty: accepted_event_count status=SUPPORTED value=0; observed_accepted_event_rate status=SUPPORTED value=0; quality_rate status=UNAVAILABLE reason=QUALITY_DENOMINATOR_EMPTY no value; full_oee status=UNSUPPORTED reason=FULL_OEE_REQUIRED_COMPONENTS_NOT_ACCEPTED no value
    unsupported OEE component: performance status=UNSUPPORTED reason=PERFORMANCE_AUTHORITIES_NOT_ACCEPTED no value
    mixed config: source.config_window_state=MIXED; accepted_event_count may be SUPPORTED with source-derived value; ideal_cycle_time is PARTIAL reason=MIXED_HISTORICAL_CONFIG_WINDOW with no value
    source unavailable: HTTP 503, status=UNAVAILABLE, reason=ACCEPTED_FACT_SOURCE_UNAVAILABLE, metrics=[] and no numeric value

Full field names, HTTP/error envelopes, and the distinction between the 503 metrics=[] and a valid HTTP 200 empty window are frozen in production_process_kpi_contract.md section 7; the snippets above do not assert any observed production value.

## 6. Validation and continuity evidence

### 6.1 Checks performed

    PASS task self-identity gate before any other repository read/action
    PASS required-reading identity checks for charter, capsule, predecessor and neighbors
    PASS physical cwd / git root / branch / HEAD / origin/main / ahead-behind
    PASS cached/staged empty and sorted dirty/untracked continuity capture
    PASS exact output prestate absent, non-symlink and untracked
    PASS frozen control-plane Python identity and primitive smoke
    PASS contract final regular/non-symlink, UTF-8 and SHA-256
    PASS report final regular/non-symlink, UTF-8 and normalized self-identity
    PASS static Markdown/semantic checks: required sections, endpoint, status enum, reason taxonomy, sole authority, counting-unit distinctions, mixed/empty/source-unavailable rules, forbidden fallback flags and DTO examples
    NOT RUN: project pytest, API runtime, DB/runtime query, product import, Docker, network/SSH/remote, PLC/V-PLC/frontend

No test source, fixture, API route, DB or runtime was created or modified. The only Python was the frozen control-plane interpreter with -B; no bytecode was produced.

### 6.2 Final protected identities

At final audit, these protected objects must remain equal to the entry identities in section 1.2:

    docs/contracts/production_metrics_contract.md = 8229 / 2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e
    api/app/routes/quality_trace.py = 9538 / 6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a
    api/app/main.py = 464 / 2bdc34c1950654ca81d0041171a3c17d646c87e9655e79c3bac120baf47438ed

The exact task-owned changed-path set is the two output paths only. Existing tracked dirty files, existing untracked corpus and the task file remain external/pre-existing continuity. Cached/staged set remains empty.

## 7. State distinctions

    WRITTEN   = this report and the contract candidate exist at the exact paths
    REVIEWED  = this child performed the bounded local static semantic review
    ACCEPTED   = no; only parent independent G3 intake can establish this
    VERIFIED   = no; no successor review or runtime/API verification was authorized
    STAGED     = no
    COMMITTED  = no
    PUSHED     = no
    DEPLOYED   = no
    ACTIVATED  = no

The report and artifact are uncommitted local outputs. A hash in this report or window manifest is an identity check, not a phase promotion.

## 8. Allowlist, prohibited actions and counts

    allowed reads = task, PM Rules relevant sections, Charter, Capsule, predecessor contract, quality_trace.py, main.py, live Git metadata
    allowed writes = docs/contracts/production_process_kpi_contract.md; docs/reports/p1_g3_process_kpi_contract_20260811T1505Z.md
    source/product/API/DB/runtime mutation count = 0
    remote/SSH/network/Docker/PLC/V-PLC/frontend count = 0
    Git mutation count = 0
    sub-agent count = 0
    repair/retry count = 0
    Ledger/counter/gate/successor/self-advance count = 0

No out-of-allowlist write, external call, project test, repair, retry, cleanup, rollback, predecessor semantic change or scope expansion occurred. The Data Analytics data-quality skill was used only as a review lens for grain, lineage, identity, completeness and false numeric claims; it did not authorize extra files or checks.

## 9. Blockers

None for this bounded G3 writing task. The contract deliberately preserves unsupported/partial states instead of inventing missing authorities.

## 10. Recommendations

1. Parent independent intake should re-read both exact outputs, recompute their identities, verify the two-path changed set and protected continuity, then decide whether to accept G3. This is the only next gate and does not grant G4 authority.
2. If G4 is later authorized, its implementation/tests should bind exactly to /api/v2/process-metrics, the fixed metric matrix, fact_key integrity fail-closed behavior, and the empty/source-unavailable DTO distinctions. This is a carry-forward implementation requirement, not a current repair or successor task created by this Thread.

## 11. Next gate

唯一 next gate：PARENT_INDEPENDENT_G3_INTAKE only。

This child does not report G3_PROCESS_KPI_CONTRACT_ACCEPTED = YES, does not update Ledger, and does not generate a G4 task.

## 12. MVP 路径一致性

    classification = MVP-ALIGNED
    approved MVP deliverable supported = local P1 Process KPI semantics and the bounded read-only production-metrics API candidate
    minimum truth invariant = accepted-fact-only numeric output; unsupported claims fail closed; synthetic/local/static evidence is not production evidence
    new product capability introduced = no; endpoint is only contract-frozen for the already-approved G4 boundary
    new threat/audit/forensics/retention/infrastructure framework = no
    scope/task inflation = no; no runtime/API/DB/remote work was pulled into G3
    next smallest MVP action = parent independent G3 intake

## 13. Thread 输出 / 上下文评估

    本次输出长度 = long durable report, concise window manifest
    当前 Thread 是否建议继续承载后续任务 = no; disposable child should terminate after manifest
    Owner 是否应在下一轮手工分发到新的 top-level Thread = yes, if a later gate is authorized
    task-file sub-agent plan = yes; one disposable Data Quality child, exact two-output scope
    sub-agent actual usage = no additional sub-agent; this assigned child performed the work directly
    理由 = developer/task boundary forbids spawning subagents; parent retains independent intake and any later G4 dispatch authority

## 14. Final audit placeholder

The following values are populated mechanically after the report body is finalized and before returning the Section 15 manifest:

    report_bytes = 020348
    report_sha256_normalized_self_identity = 7167ca3f0df3facaffb2e05083040fe0e0a1f6cbba2a08f7a08ff217703e039b
    full_report_sha256 = returned only in the concise window manifest; parent must independently recompute it

## 15. Child durable manifest

    报告名称：P1-G3 Process KPI + OEE Data-Sufficiency Contract Report
    任务名称：P1_G3_PROCESS_KPI_CONTRACT_20260811T1505Z
    执行 Thread：Data Quality（一次性 disposable contract specialist）
    结论：PASS WITH RECOMMENDATIONS
    Report delivery mode：REPOSITORY_REPORT_WITH_ARTIFACTS
    Report path：docs/reports/p1_g3_process_kpi_contract_20260811T1505Z.md
    Report bytes：020348
    Report SHA-256：full-file SHA-256 in final chat manifest
    Artifacts:
    - path: docs/contracts/production_process_kpi_contract.md
      bytes: 28427
      SHA-256: 776e744314f9ec33884765c20f8d88dab45afeda74354cf7e10e7fc226809252
      role: accepted G3 contract candidate; WRITTEN only
    Changed files：exactly the two task-owned output paths; pre-existing external dirty/untracked continuity retained
    Tests/checks：control-plane Python 3.14.6 identity/primitive smoke and docs-only static semantic checks; no project pytest/API/DB/runtime
    Allowlist compliance：PASS; no out-of-allowlist write or action
    Git staged：no
    Git committed：no
    Git pushed：no
    Blockers：none
    Recommendations：parent independent intake; later G4 must consume exact endpoint/DTO and fail-closed matrix
    Next gate：PARENT_INDEPENDENT_G3_INTAKE only
    MVP 路径一致性：MVP-ALIGNED
    Thread 输出 / 上下文评估：long durable output; terminate disposable child; no sub-agent spawned
