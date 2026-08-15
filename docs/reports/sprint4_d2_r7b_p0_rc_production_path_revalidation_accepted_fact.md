# P0-RC Production-Path Revalidation and Accepted-Fact Gate Report

## Terminal manifest

`PASS / P0_RC_PRODUCTION_FACT_GATE_PASS=YES / PRODUCTION_ACCEPTED_CANDIDATE=YES`

This is the disposable specialist report for the one exact task below.  The
parent controller alone performs independent PM intake; this report does not
set `PRODUCTION_ACCEPTED`, `P0_PM_ACCEPTED`, or any later B1 state.

## Authority and task identity

- Task: `docs/thread_handoff/pm_task_20260811T1334Z_p0_rc_production_path_revalidation_accepted_fact.md`
- Task type: regular, non-symlink; bytes `22983`; SHA-256
  `bd597c44590c13e724f0293d62257bc159f09b6364b817a54d82ba1f7cdb3525`.
- Owner clarification read and verified: `docs/thread_handoff/shadow_pm_p0_owner_authority_clarification_20260811_remaining_gate_recalculation.md`; regular/non-symlink; bytes `9210`; SHA-256 `0dceeab191afca7272f7f5bb4b1aa8ff1351436531f67e9b10de0434f3d0dc62`.
- The accepted corrected lineage was frozen as Collector full ID
  `6cab966e18bc1b5b349a0901793ff89ab7bfcde889ff7b2e911746e413eac25e`,
  Docker `Image.Id`
  `sha256:a199e6417c3ed5e42724201122ea4014604b561593a243039aef72d71900b252`,
  Collector start `2026-08-11T04:10:50.714778959Z`, and config
  `0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38` /
  `2026.06.26-slice-a`.

## Ordered reads and entry gate

The complete task was read to EOF before any other repository read.  The
required ordered reads then completed as specified:

1. `docs/thread_handoff/shadow_pm_p0_remote_closure_charter.md`
2. `docs/reports/shadow_pm_p0_remote_closure_ledger.md`
3. `docs/thread_handoff/shadow_pm_p0_owner_authority_clarification_20260811_remaining_gate_recalculation.md`
4. `docs/thread_handoff/shadow_pm_p0_goal_prompt.md`
5. `docs/thread_handoff/pm_operating_rules.md`
6. `docs/current_status.md` targeted current-control, accepted-fact, and
   Collector/ACK transaction sections (the pre-existing dirty tracked file was
   not edited)
7. `docs/reports/sprint4_d2_r7b_p0_rc_r1_r2_existing_script_runtime_loaded_verification.md`
8. `docs/reports/sprint4_d2_r7b_p0_rc_a1_r1_self_identity_mechanics_recovery.md`
9. `docs/thread_handoff/pm_task_20260809T1231Z_d2_r7b_p0_a01_minimal_production_accepted_fact_validation.md`
10. `docs/reports/sprint4_d2_r7b_p0_d2-r7b-p0-d2_minimal_production_path_diagnostic_execution.md`
11. `db/migrations/007_accepted_station_event_visibility.sql`
12. `collector/app/services/accepted_station_event_fact.py`
13. `collector/app/services/storage.py` targeted transaction and accepted-fact
    sections
14. `collector/app/services/event_collector.py` targeted accepted decision,
    transaction, commit, and ACK/read_done sections
15. `docker-compose.yml` targeted `s7-plc-sim`, `collector`, and `postgres`
    definitions
16. `s7_plc_sim/app/pipeline.py` targeted plan/cycle/handshake sections and
    `s7_plc_sim/app/control_api.py` targeted state/start routes
17. `common/station_event/validation.py`,
    `tests/test_station_event_model.py`, and
    `collector/tests/test_event_collector_adapter_gate.py`.

R0 passed before the ordered reads: `pwd -P` and Git root were
`/Users/chenjie/Documents/MES/edge-mes-demo`; branch `main`; HEAD
`dbe5706e4b01387101f2a4666e73f3c13ffeb0e`; `origin/main`
`2a4f9d4ac6a11a3758b00f1e368dbe9484d10d35`; `HEAD...origin/main` was
`1<TAB>0`; cached diff was empty.  The task was untracked, unstaged, not
indexed, and not ignored.  The declared report path was absent and
non-symlink before lock.  SSH config and known_hosts were regular,
non-symlink files and the `edge-pi` stanza was present.

The unchanged reviewed identities passed before lock and had no path-scoped
worktree or cached diff:

| path | bytes | SHA-256 |
| --- | ---: | --- |
| `common/station_event/validation.py` | 41624 | `bb0664bfe8113e7989ca17629a6a8e5072e91d57ecf640f211631f216e51e02e` |
| `tests/test_station_event_model.py` | 58061 | `7b7177fa815834bc174e311acf5cb3b938004bbdc75073ecad2e94d7c91aac27` |
| `collector/tests/test_event_collector_adapter_gate.py` | 26822 | `8e022346f359ec62877b876c618269631a70f2ffa9b66be7da38cb6eefd24080` |

## Script and immutable execution lock

The task contained exactly one begin marker and one end marker.  The in-memory
extraction was not persisted: script bytes `8677`, SHA-256
`1e48fef48486e8249e489089e6e077f016bfdb6a4a3e8f9ad293dd6113af6300`, and
`/bin/sh -n` passed.

Immediately before the remote action, the immutable lock froze the task and
script identities above; the accepted Collector/image/start/config identities;
the exact SSH argv; the exact current-config accepted-fact predicates; one
state GET; at most one conditional `quantity=1` start; one 110-second bounded
wait; one read-only PostgreSQL exec with 3-second statement/idle timeouts and
25-second outer timeout; report path; and all zero-mutation budgets.

Exact SSH argv (one process only):

```text
/usr/bin/ssh
-F /Users/chenjie/.ssh/config
-o BatchMode=yes
-o ControlMaster=no
-o StrictHostKeyChecking=yes
-o UserKnownHostsFile=/Users/chenjie/.ssh/known_hosts
-o ConnectTimeout=10
-o ConnectionAttempts=1
edge-pi
--
/bin/sh -s -- p0-rc-production
```

The SQL was a single `BEGIN READ ONLY` / `SELECT` / `COMMIT` against only
`public.production_accepted_station_event_fact`, constrained to LINE_001,
PLC_001, WS01/WS02/WS03, the frozen config hash/version, `station_result`, a
valid production result, non-empty source identity, canonical `sha256:` fact
key and content fingerprint, and the fresh Collector start through the one
observation end.

## Remote evidence

The one SSH completed with exit 0 and a complete frame:

- Host: `Pi-5b-Li`; machine ID `2084d2f4de24462191e2fcffd5c6aab4`; Linux
  `aarch64`; user `mari` UID/GID `1000/1000`.
- Collector: full ID
  `6cab966e18bc1b5b349a0901793ff89ab7bfcde889ff7b2e911746e413eac25e`;
  running; `/edge-mes-collector`; Image.Id
  `sha256:a199e6417c3ed5e42724201122ea4014604b561593a243039aef72d71900b252`;
  StartedAt `2026-08-11T04:10:50.714778959Z`; restart count `0`.
- V-PLC: full ID
  `d21e950b98ae87bbd3ee321074100d0b54b174235ce46df34c5100e1130b785f`;
  running; `/edge-mes-s7-plc-sim`; image `edge-mes-demo-s7-plc-sim`;
  Image.Id `sha256:3a28ae38c623d8cb80f775f954315e633b1108112082c37ece698c7562522238`;
  restart count `0`.
- PostgreSQL: full ID
  `bb3ba0738e692c68b14a62ca64296e484990d3b86b1f6d395c27b200af5cb890`;
  running; `/edge-mes-postgres`; config image `postgres:16`; Image.Id
  `sha256:f961d097a9cedd37779baef1aab3fe87ef1c63b3b34d361f90a98ea5c9b77e56`;
  restart count `0`.

The exactly-one V-PLC state GET returned 1651 bytes, SHA-256
`9833b386ae9cffb1f97adea5edf66fbc9fdb28b1eff24723643ab93453bf7511`, with
`plan_active=true`.  The conditional start was therefore not issued
(`P0PROD_STIMULUS=0|plan_already_active=true`).  No V-PLC reset, stop, station
edit, force-NOK, or other control call occurred.

The bounded wait was 110 seconds.  The observation window was:

```text
2026-08-11T04:10:50.714778959Z -> 2026-08-11T05:44:30Z
```

The exactly-one read-only PostgreSQL exec returned one qualifying accepted
fact:

```text
station_id=WS01
production_result=ok
cycle_counter=113095
source_event_id=sha256:993ab6991534339db39c14180ebf6d1349a870035db7a3d5ed336147479ded8a
fact_key=sha256:a8c7322bb96a6858aff226d25c23c731bb5cfcfa059a47b2ecefbea78efc8422
content_fingerprint=sha256:36426c0d264fc4a14a531596844751cf13643019658ed4aaee7921f4872181f9
event_ts=2026-08-11T05:44:25.000000Z
accepted_at=2026-08-11T05:44:25.728731Z
config_hash=0038c05d5cf74ff3b8c508a3222ebb426658ad8e657c5034ac88c4ff32efae38
config_version=2026.06.26-slice-a
```

## Counts, classification, and stop boundary

```text
SSH process starts                  = 1
V-PLC state GET                     = 1
V-PLC production/start POST         = 0
V-PLC reset/stop/station/force-NOK  = 0
PostgreSQL docker exec/query        = 1
DB writes                           = 0
Collector/Compose lifecycle         = 0
image load/tag/remove               = 0
remote filesystem writes            = 0
retry/reconnect/fallback/second SSH = 0/0/0/0
report writes                       = 1
Git mutations                       = 0
```

Terminal classification is `PASS / P0_RC_PRODUCTION_FACT_GATE_PASS=YES`:
one exact current-lineage Collector, one running V-PLC and PostgreSQL service,
one successful state GET, no conditional stimulus because the plan was already
active, one successful read-only DB exec, exactly one qualifying canonical
current-config fact, and zero forbidden mutations.  The specialist stops here.
The parent must independently intake this report, decide
`PRODUCTION_ACCEPTED`, and only then consider the separate local/read-only B1
eligibility reassessment.  No review repetition is implied by this report, and
B1 execution remains forbidden.
