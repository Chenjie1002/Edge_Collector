# UNTRACKED_CORPUS_CANONICAL_CONTINUITY_ADOPTION

任务名称：`UNTRACKED_CORPUS_CANONICAL_CONTINUITY_ADOPTION`

Authority source：Owner 于 2026-08-15 明确回复“批准这个 gate”，承接 Mainline PM 已定义的 gate：对冻结 untracked corpus 中 90 个 strict canonical-reference candidates 与 10 个 2026-08-15 current A1 milestone durable files 做 bounded review、exact allowlist、canonical status sync、stage/commit；不处理其余 untracked corpus；不 push。

项目根目录：`/Users/chenjie/Documents/MES/edge-mes-demo`

基线 authority：
- branch `main`
- expected HEAD = origin/main = `6226bf3fb716880a176f9eb642b8139cef3255a6`
- ahead/behind `0/0`
- staged `0`
- tracked dirty `0` before this gate
- `git diff --check` / cached check PASS

上游 frozen corpus authority：
- `docs/reports/untracked_corpus_reconciliation_and_retention_20260815T1137Z.md`
- frozen prewrite count `1283`
- frozen pathset SHA-256 `ed8be6ed329c1e93ae2c88b5f6b3b771e404656610fff6e3fecfd6666850f331`
- frozen logical recordset SHA-256 `99776a62cca30c18c7a577c70c7da9c1e6b845f4344c8b5942d756789dee1935`

Canonical candidate authority：
- strict tracked-reference set: exactly 90 files reconstructed by applying rule 8 from the upstream compact manifest to the frozen 1283 corpus at expected HEAD;
- current A1 milestone promotion set: exactly 10 paths listed in the upstream compact manifest;
- union count = `100`;
- union bytes = `1294611`;
- candidate record schema: `path<TAB>bytes<TAB>sha256<TAB>reason<TAB>secret_marker<TAB>local_abs_path`;
- candidate recordset SHA-256 = `163ba38c9338957bfc4cc1097bc663db02dbf784be578a3b716e5dc8be0b41bf`;
- candidate duplicate-content groups = `0`;
- high-confidence secret marker files = `0`;
- machine-local `/Users/chenjie/` references = `71` candidate files; treated as historical/environment evidence, not secret by itself;
- conservative repo-reference scan: 29 candidate files contain one or more historical missing/renamed repository references. These are `HISTORICAL_REFERENCE_VARIANCE`; they must not be rewritten in place in this adoption gate because historical reports/handoffs are immutable evidence.

Exact 10 current A1 milestone paths：
1. `docs/reports/a1_station_summary_trusted_origin_real_data_wiring_readonly_diagnosis_r2_20260815T0949Z.md`
2. `docs/reports/a1_station_summary_controlled_local_minimal_stack_bringup_20260815T1037Z.md`
3. `docs/reports/a1_local_minimal_stack_image_materialization_20260815T1047Z.md`
4. `docs/reports/a1_station_summary_controlled_local_minimal_stack_bringup_r2_20260815T1055Z.md`
5. `docs/reports/a1_local_accepted_fact_source_readonly_reconciliation_20260815T1106Z.md`
6. `docs/reports/a1_local_accepted_fact_schema_materialization_20260815T1110Z.md`
7. `docs/reports/a1_local_accepted_fact_data_source_reconciliation_20260815T1117Z.md`
8. `docs/reports/a1_local_formal_producer_image_materialization_20260815T1122Z.md`
9. `docs/reports/a1_local_formal_producer_controlled_bringup_and_accepted_fact_observation_20260815T1132Z.md`
10. `docs/thread_handoff/chatgpt_pm_handoff_260815-1654.md`

Exact gate artifact paths：
- task: `docs/thread_handoff/pm_task_20260815T1203Z_untracked_corpus_canonical_continuity_adoption.md`
- candidate manifest: `docs/reports/untracked_corpus_canonical_continuity_candidates_20260815T1203Z.tsv`
- final report: `docs/reports/untracked_corpus_canonical_continuity_adoption_20260815T1203Z.md`

Exact tracked canonical edit authority：
- `docs/current_status.md` only.
- Allowed edit: prepend one new `0Q` current-state control block and update top-level `更新时间` from 2026-08-12 to 2026-08-15. Do not rewrite `0P` or any older historical section.

Exact Git mutation authority：
- stage only the 100 candidate files whose reconstructed recordset mechanically matches `163ba38c9338957bfc4cc1097bc663db02dbf784be578a3b716e5dc8be0b41bf`;
- stage the three exact gate artifact paths above;
- stage `docs/current_status.md` only as the one tracked canonical edit;
- total intended staged paths after report materialization = exactly `104`;
- commit exactly once with message: `docs: adopt canonical PM continuity evidence`;
- no push, tag, branch creation, archive creation, stash, reset, clean, rename, delete, or broad add.

Explicitly forbidden：
- `git add .`, `git add docs/`, `git add -A`;
- stage/commit any of the remaining untracked corpus outside exact candidate/gate paths;
- modify any historical candidate file;
- delete/archive/move the 516 archive candidates, 668 preserve-pending files, 7 tooling-review files, `frontend/next-env.d.ts`, or the exact duplicate candidate;
- Docker/Compose lifecycle, DB write/query beyond read-only continuity checks already completed, HTTP/SSH/V-PLC/PLC actions;
- push.

Review result required before stage：
- candidate count/bytes/recordset hash exact;
- secret-marker scan = 0 high-confidence hits;
- duplicate content groups = 0;
- historical missing-reference variance recorded, not repaired;
- `docs/current_status.md` 0Q diff passes `git diff --check`;
- task/manifest/report identities frozen;
- no unauthorized tracked dirty files.

Commit terminal rules：
- PASS only if exact 104-path staged allowlist is proven, commit succeeds once, staged becomes empty, HEAD advances by exactly one commit from `6226bf3fb716880a176f9eb642b8139cef3255a6`, and no push occurs.
- HOLD if any candidate hash drifts, staged set differs, unexpected tracked dirty appears, Git commit fails, or exact allowlist cannot be established. No retry without new authority.

Expected post-commit untracked behavior：
- the 100 adopted candidate files and 3 gate artifacts leave untracked status;
- all other historical corpus remains untouched; no claim that the untracked corpus is fully cleaned.

Next gate after PASS：
- choose separately among historical evidence archive, local tooling adoption review, generated-file hygiene, exact duplicate cleanup, preserve-pending semantic reconciliation, or return to product work. No next gate is implicitly authorized.
