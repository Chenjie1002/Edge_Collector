# ChatGPT PM Handoff — 260706-1928

Timestamp: 2026-07-06 19:28 UTC+8
Project path: `/Users/chenjie/Documents/MES/edge-mes-demo`

## Live baseline

`HEAD == origin/main == 843e0b5e60adc2f9271dff5f390e8eb925dfeed6`

Latest commit: `843e0b5 Sync Dashboard planning status`

Branch: `main`

Phase-1 tag: `phase1-pass-20260619`

Phase-2 tag: not created

## Current closed gate

Sprint 3 Dashboard/API implementation planning gate is CLOSED / PASS WITH RECOMMENDATIONS.

Planning report commit:

- `4fcdd6623247aaf9d3d3df23fd7cadf49f5d662a Plan Dashboard API implementation`
- changed file: `docs/reports/sprint3_dashboard_api_implementation_plan.md`

Review status:

- Architecture / Integration planning: PASS WITH RECOMMENDATIONS
- Reliability focused planning review: PASS WITH RECOMMENDATIONS
- Data Quality focused planning review: PASS WITH RECOMMENDATIONS
- Verification focused planning review / exact future implementation allowlist audit: PASS WITH RECOMMENDATIONS

Post-push docs/status sync commit:

- `843e0b5e60adc2f9271dff5f390e8eb925dfeed6 Sync Dashboard planning status`
- changed files:
  - `docs/current_status.md`
  - `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
  - `docs/reports/sprint3_collector_ingestion_adapter_plan.md`

## Recent chain closed

The DB/API/Dashboard chain currently closed is:

- accepted fact DB write path
- accepted fact API read path
- DB-backed API validation planning
- DB-backed API validation focused repair
- DB-backed API validation SSH-tunnel rerun
- Dashboard/API implementation planning
- Dashboard/API planning docs/status sync

Important recent commits:

- `97dc4d5 Harden accepted station events API contract`
- `78ce29b Plan DB-backed API validation`
- `1d040a6 Align DB-backed API failure assertion`
- `a0042fb Add PM handoff after DB-backed repair`
- `ba02249 Sync DB-backed API validation rerun status`
- `4fcdd66 Plan Dashboard API implementation`
- `843e0b5 Sync Dashboard planning status`

DB-backed API validation rerun evidence:

- focused pytest: `88 passed in 12.94s`
- exact files:
  - `api/tests/test_accepted_station_events_api.py`
  - `api/tests/test_accepted_station_events_api_db_backed.py`
- masked DSN facts:
  - target host `localhost`
  - target port `5433`
  - target database `edge_mes_test_api_read`
  - maintenance database `postgres`
  - SSH tunnel Mac `localhost:5433` -> Pi `localhost:5432`
- cleanup note: terse `-q` output did not print an explicit cleanup line; no pytest teardown/cleanup error was reported.

## Known external dirty artifacts

Do not stage, commit, clean or use these as authority unless PM explicitly authorizes exact paths:

- `.gitignore` may be modified
- `docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md`
- `docs/reports/phase1_to_sprint2_management_keynote_10p.html`
- `docs/reports/sprint3_db_backed_api_validation_reliability_review.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260624.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260625.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md`
- `docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md`

This handoff file is newly generated and should not be staged unless PM explicitly authorizes exact-path commit/push:

- `docs/thread_handoff/chatgpt_pm_handoff_260706-1928.md`

## Required first reads for next PM

- `docs/thread_handoff/pm_operating_rules.md`
- `docs/thread_handoff/chatgpt_pm_handoff_260706-1928.md`
- `docs/current_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`
- `docs/reports/sprint3_collector_ingestion_adapter_plan.md`
- `docs/contracts/dashboard_api_contract.md`
- `docs/reports/sprint3_dashboard_api_implementation_plan.md`

Optional historical references:

- `docs/reports/sprint3_api_consumer_implementation_plan.md`
- `docs/reports/sprint3_db_api_dashboard_consumer_plan.md`

Do not use `docs/reports/sprint3_db_backed_api_validation_reliability_review.md` as authority unless PM explicitly authorizes it; it is currently an external untracked artifact.

## Not authorized

The following remain not authorized:

- Dashboard/frontend implementation
- API route or contract modification
- DB migration or schema change
- DB-backed test execution
- Postgres connection
- `EDGE_MES_ENABLE_DB_BACKED_TESTS=1` outside an approved gate
- Docker / docker compose
- deploy / tag / rollback
- real PLC pilot
- broad pytest
- optional debug/review diagnostics view
- worker/runtime DB-backed gates
- actual timeout failure induction proof
- stage, commit or push without exact PM authorization

Dashboard implementation is not authorized yet. The planning gate is closed, but implementation requires a new PM-authorized Level 2 branch.

## Carry-forward recommendations

Dashboard/API implementation planning carry-forward:

- Convert category-level future Dashboard implementation allowlist into exact file paths before implementation authorization.
- Add invalid / expired / cross-scope cursor UI negative tests.
- Keep page-level summaries labelled as current page only, not line-wide/global production totals.
- Ensure stale prior data cannot render as fresh production truth during loading/error/unavailable states.
- Keep future implementation Dashboard-only and read-only unless PM opens a separate API/contract gate.
- If implementation discovers existing endpoint/contract insufficiency, stop and open a separate API/contract gate.

DB/API carry-forward:

- Future DB-backed reruns require separate PM authorization.
- Actual timeout failure induction remains separate; timeout statement verification is not proof of timeout failure behavior.
- Do not treat `raw_plc_sample`, `cycle_event`, `station_event`, `production_unit`, `quality_event`, `production_snapshot` or `production_events` as equivalent production fact sources, fallback sources or join-derived field fillers.
- `accepted_at` is an accepted fact timestamp, not collector freshness, ACK time, station freshness or read_done time.

## Recommended next gate

Recommended next gate:

`Sprint 3 Dashboard implementation exact-file allowlist discovery / implementation preparation gate`

Purpose:

- Inspect the repository layout and identify whether a frontend/Dashboard package already exists.
- Convert the planning report's category-level future allowlist into exact file paths.
- Decide whether the implementation should create a new frontend structure or modify existing Dashboard/frontend files.
- Produce a reviewable exact-file implementation allowlist and focused test command proposal.
- Do not implement Dashboard/frontend code yet.

Recommended executing Thread: Architecture / Integration.

This should be followed by Reliability / Data Quality / Verification focused reviews if the allowlist materially shapes implementation authorization.

## Next PM first action

Run read-only recovery first:

- `git status -sb`
- `git log --oneline -8`
- `git log -1 --format='%H %s'`
- `git rev-parse origin/main`
- `git diff --name-only`
- `git diff --cached --name-only`
- `git status --short --untracked-files=all`

Expected at handoff authoring:

- `HEAD == origin/main == 843e0b5e60adc2f9271dff5f390e8eb925dfeed6`
- latest commit: `843e0b5 Sync Dashboard planning status`
- cached diff: empty

## Copyable prompt for next ChatGPT PM

```text
你是 Edge MES Demo 项目的 ChatGPT PM。请接手当前项目。

项目路径：/Users/chenjie/Documents/MES/edge-mes-demo

第一步必须做只读恢复，不要修改文件、不要运行 tests、不要连接 DB、不要 Docker、不要 stage/commit/push：
- git status -sb
- git log --oneline -8
- git log -1 --format='%H %s'
- git rev-parse origin/main
- git diff --name-only
- git diff --cached --name-only
- git status --short --untracked-files=all

预期 live baseline：
- HEAD / origin/main == 843e0b5e60adc2f9271dff5f390e8eb925dfeed6
- Latest commit: 843e0b5 Sync Dashboard planning status

请先阅读：
- docs/thread_handoff/pm_operating_rules.md
- docs/thread_handoff/chatgpt_pm_handoff_260706-1928.md
- docs/current_status.md
- docs/reports/sprint3_collector_ingestion_adapter_gate_status.md
- docs/reports/sprint3_collector_ingestion_adapter_plan.md
- docs/contracts/dashboard_api_contract.md
- docs/reports/sprint3_dashboard_api_implementation_plan.md

当前已闭环：
- DB-backed API validation rerun: PASS WITH RECOMMENDATIONS, focused pytest 88 passed in 12.94s
- DB-backed rerun docs/status sync: committed at ba02249
- Dashboard/API implementation planning gate: CLOSED / PASS WITH RECOMMENDATIONS
- Dashboard planning report committed at 4fcdd66
- Dashboard planning docs/status sync committed at 843e0b5

当前推荐下一步：Sprint 3 Dashboard implementation exact-file allowlist discovery / implementation preparation gate。

目标：只读检查仓库 Dashboard/frontend 结构，把 planning report 里的 category-level future implementation allowlist 转成 exact file paths，生成 implementation preparation/allowlist report。不要实现代码。

必须排除：
- .gitignore
- docs/Edge MES Demo — ChatGPT PM Handoff - 20260623.md
- docs/reports/phase1_to_sprint2_management_keynote_10p.html
- docs/reports/sprint3_db_backed_api_validation_reliability_review.md
- docs/thread_handoff/chatgpt_pm_handoff_20260624.md
- docs/thread_handoff/chatgpt_pm_handoff_20260625.md
- docs/thread_handoff/chatgpt_pm_handoff_20260625_final.md
- docs/thread_handoff/chatgpt_pm_handoff_20260626_slice_a_commit.md

当前仍未授权：Dashboard/frontend implementation、API/contract changes、DB migration/schema、tests、Postgres/DB-backed execution、Docker、deploy/tag/rollback、real PLC pilot、stage/commit/push。

如果 live Git 与预期不一致，先报告差异，不要猜。
```

## Commit note

If PM authorizes exact-path commit/push for this handoff, stage only:

- `docs/thread_handoff/chatgpt_pm_handoff_260706-1928.md`

Do not stage `.gitignore`, old handoff files, Keynote/reporting artifacts, unauthorized reliability report or broad `docs/`.
