# P1 Process KPI + Bounded API — Accepted State Capsule

Status: `MAINLINE_PM_ACCEPTED_BASELINE / READ_ONLY_CONTEXT`

Goal consumer: `P1-SHADOW-PM-PROCESS-KPI-BOUNDED-API-LOCAL-V1`

This capsule compresses the accepted facts required by the next Goal. It is context, not executable authority. PM Rules + the new Goal Charter + each exact repository-backed task govern actions. Old repair/recovery history is intentionally omitted unless a fresh failure makes it causally relevant.

## 1. Genesis Git baseline

```text
branch = main
HEAD = cf4eac54d3f365b0addfaae13f5e7292e3233641
parent = dbe5706e4b01387101f2a4666e73f3c13ffeb0e9
commit message = feat(p1): publish accepted-fact quality and trace local MVP
origin/main = 2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35
origin/main...HEAD = 0<TAB>2
cached/staged = empty
tracked dirty = docs/current_status.md, docs/thread_handoff/pm_operating_rules.md
```

The two tracked-dirty docs above are protected external continuity state and are not part of the next Goal mutation allowlist. The large pre-existing untracked corpus is also external unless a fresh exact task names a path.

## 2. Closed predecessor Goal

```text
GOAL_ID = P1-SHADOW-PM-QUALITY-TRACE-LOCAL-MVP-V1
GOAL_STATUS = COMPLETE
GOAL_TERMINAL = PASS / P1_QUALITY_TRACE_LOCAL_MVP_AUTONOMOUS_GOAL_COMPLETE
G2_IMPLEMENTATION_ACCEPTED = YES
RELIABILITY_ACCEPTED = YES
DATA_QUALITY_ACCEPTED = YES
VERIFICATION_ACCEPTED = YES
FINAL_CANDIDATE_REVIEWS_BIND_SAME_STATE = YES
```

Closeout:

```text
path = docs/reports/p1_quality_trace_local_mvp_goal_closeout.md
bytes = 8778
SHA-256 = 5368aa3bb436841f0f9bfbbdcf0aefcce7982fc9b5184d5f08d85791b0c20010
```

Published accepted candidate:

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `api/app/routes/quality_trace.py` | 9538 | `6137c06b10952bdea493ba1a20ec37186c8aad1b0dfe01ea4d5134723886c46a` |
| `api/app/main.py` | 464 | `2bdc34c1950654ca81d0041171a3c17d646c87e9655e79c3bac120baf47438ed` |
| `api/tests/test_quality_trace_api.py` | 13296 | `bea0afed1aac1c502b340984b431a7890e76ec3a38b59fd17beddeea888daf9c` |
| `docs/contracts/production_metrics_contract.md` | 8229 | `2bdff1aa017577b973f8c6358a42fe5d9ad0275949dbad2fe5e6dba6a8925c4e` |

These objects are predecessor accepted truth. The next Goal may modify `api/app/main.py` only if a fresh exact G4 task requires route registration; it must not silently rewrite Quality/Trace semantics or predecessor contract claims.

## 3. Production truth authority

Accepted production authority remains:

```text
production_accepted_station_event_fact = sole P1 accepted station-business PRODUCTION_AUTHORITY
```

New P1 production semantics may not silently read, join or fallback to:

```text
production_snapshot
cycle_event
station_event
production_unit
quality_event
raw_plc_sample
adapter diagnostics
```

No raw payload, ACK/read_done, adapter reason/disposition or current runtime health may be promoted into a business production fact.

## 4. Accepted semantic boundary entering G3

```text
station-scoped Quality = SUPPORTED
accepted event timeline = SUPPORTED
unit_id Trace = PARTIAL
dmc Trace = PARTIAL
historical route/order/terminal = PARTIAL
throughput/output = PARTIAL
station cycle time = PARTIAL
ideal cycle time = PARTIAL
Performance = UNSUPPORTED
Availability = UNSUPPORTED
Full OEE = UNSUPPORTED
```

These are lower bounds on honesty, not a demand that G3 upgrade every item. G3 may preserve `PARTIAL` / `UNSUPPORTED` and still PASS when the product contract makes insufficiency explicit.

Important causal reasons:

- historical terminal/order/ideal CT require exact immutable historical config resolution by accepted `config_hash + config_version`; current YAML is not historical authority;
- station cycle time lacks an accepted producer-authoritative start/complete cycle-instance pairing key; adjacent rows, counter-only or time proximity are forbidden;
- Performance lacks historical ideal CT plus an authoritative operating/run-time denominator;
- Availability lacks planned production time, planned downtime and an authoritative run/stop/unknown state timeline;
- Full OEE cannot be numeric while required A/P component authority is absent.

## 5. Existing Quality + Trace product behavior

The published product registers `quality_trace.router` in `api/app/main.py` and exposes local production endpoints under `/api/v2/production` for Quality and Trace. They read `production_accepted_station_event_fact`, use bounded half-open windows and preserve accepted-fact-only/no-fallback semantics.

The next Goal must treat this as an accepted neighboring module, not as a reason to append unrelated Process KPI logic into the same file. A fresh G4 design should prefer a focused Process KPI route/test module when G3 contract warrants implementation.

## 6. G3/G4 product principle

The accepted P1 plan requires:

> 能算的必须算对；不能算的必须明确说不能算；不得为了 Dashboard 完整度制造业务真值。

G3 must freeze semantics before G4 implementation. It must explicitly distinguish an observed calendar-window/event rate from OEE `Performance`; a numeric rate derived from accepted events and query-window duration must never be relabeled as authoritative operating Performance.

G3 must decide, at minimum:

```text
station accepted-result event count / counting unit
station observed output-rate semantics, if any
line/terminal output sufficiency
station cycle-time sufficiency
ideal CT sufficiency
Quality component reuse
Performance sufficiency
Availability sufficiency
Full OEE sufficiency
mixed-config window behavior
empty window behavior
unsupported/unavailable response semantics
source-unavailable behavior
```

Endpoint names and DTO shape are not frozen by this capsule; G3 owns that contract decision.

## 7. Explicit next-Goal exclusions

The next local Goal does not authorize:

```text
historical config registry implementation
DB migration/schema redesign
Collector/config/decoder changes
PLC/V-PLC
Docker/Compose
remote/SSH/Raspberry Pi
production stimulus
frontend/dashboard
legacy /kpi cleanup
legacy /trace cleanup
Full Genealogy
Performance fabrication
Availability fabrication
Full OEE numeric claim
Git stage/commit/push/tag
P1-G5 remote reconciliation
parallel FIELD-VALIDATION-COLLECTOR-DB interaction
```

If one becomes necessary for truthful Goal success, stop for Owner review rather than expanding scope.

## 8. Runtime authority continuity

Control plane remains frozen to:

```text
CONTROL_PLANE_PYTHON = /opt/homebrew/opt/python@3.14/bin/python3.14
version = Python 3.14.6
architecture = arm64
resolved bytes = 52448
resolved SHA-256 = b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf
```

For the new Goal, Owner has pre-authorized the existing project test runtime for exact local compile/import/test commands only, subject to fresh identity checks in each task:

```text
PROJECT_TEST_RUNTIME = <project-root>/.venv/bin/python
Python = 3.13.3
architecture = arm64
resolved base = /Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13
resolved base bytes = 119328
resolved base SHA-256 = f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5
pytest = 9.1.1
fastapi = 0.115.6
psycopg = 3.2.3
```

The project test runtime never replaces control-plane Python and may not be installed, upgraded, recreated or mutated by the Goal.

## 9. Carry-forward recommendation

Exactly one predecessor Verification recommendation remains non-blocking:

```text
NEXT_REVIEW_CARRY_FORWARD:
future test maintenance may add explicit parameterized focused cases for duplicate query keys,
neither identity, and limit=0/non-numeric limit.
```

It is not a G3/G4 blocker, grants no mutation authority, and must not be promoted into work unless directly necessary for a fresh changed-path claim.

## 10. Reading-efficiency rule

This capsule is the default historical context for all new Goal children. A child must not re-read predecessor capability tasks, syntax/test repair reports, old Goal prompt/bootstrap or the full predecessor Ledger merely to reconstruct facts already frozen here. Read old evidence only when a fresh contradiction or causal investigation specifically requires it.
