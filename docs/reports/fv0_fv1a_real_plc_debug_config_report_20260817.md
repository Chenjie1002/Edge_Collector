# FV0-FV1A Real PLC Debug Configuration Implementation Report

## Terminal conclusion

**PASS WITH RECOMMENDATIONS** — FV0/FV1A is implemented and locally qualified as an executable PLC Debug Communication Contract. The evidence is local/static/synthetic only. It is not real PLC acceptance, Wyse acceptance, field acceptance, Collector production acceptance, or permission for FV1B/FV2/FV3.

Recommendation: keep the current accepted contract range of 344 engineering bytes visible in the candidate. The existing Collector S7 string decoder/read-plan expands the physical WS01/WS02/WS03 read plan to 346 bytes for S7 string framing; this is consumer behavior proven by the mapping/read-plan test and is not an active mapping mutation.

## Authority and fresh recovery

- Authoritative task: `docs/thread_handoff/pm_task_20260817T0104Z_fv0-fv1a_real_plc_debug_config.md`
- Task identity gate: PASS
  - type: regular file / non-symlink
  - bytes: `22753`
  - SHA-256: `b19ac39bb38d6b3d18d29a242320bb0cc28bf37f7eae6a57380951c7600719d9`
- Physical project root and Git top-level matched.
- Entry HEAD: `40d5aaae5fcc09ec24f1a65049c90f51cae74f0b`
- Entry `origin/main`: `6226bf3fb716880a176f9eb642b8139cef3255a6`
- Entry ahead count: `21`
- Entry staged path count: `0`
- No concurrent non-doc source mutation was observed before implementation.

## Implemented contract

- `common/line_config/debug_contract.py` adds `plc-debug-contract/v1` normalization, fail-closed validation, deterministic canonical ordering, semantic candidate/contract hashes, engineering rows, and Markdown export.
- Connection fields remain editable: host, port, rack, slot, timeout, poll interval, and line configuration.
- The initial virtual candidate is seeded from the current effective 3WS mapping with WS01/WS02/WS03 DBs 101/102/103, the accepted range, common cycle/result/identity/handshake fields, NOK fields, and current 3WS process-value fields.
- Every station and signal carries `PLANNED` or `CONFIRMED`; initial virtual values are `PLANNED` unless explicitly confirmed in the submitted candidate.
- Concrete PLC-readable addresses are persisted and rendered, including `DB101.DBD2` and `DB101.DBX6.1`.
- The write authority is explicit and fail-closed:
  - mode: `READ_DONE_ONLY`
  - Edge-to-PLC field: `read_done` only
  - parameter writes: disabled
  - machine-control writes: disabled
  - safety writes: disabled
  - arbitrary DB writes: disabled
- `common/line_config/runtime_projection.py` accepts the candidate contract as an optional projection input. It preserves existing topology/decoder metadata while producing a candidate-only mapping document consumable by the current Collector mapping loader and read-plan builder.
- Candidate persistence remains in the existing deployment-config candidate mechanism. Retrieval stores the complete connection/station/signal/confirmation/allowlist contract plus engineering rows and export text. It does not write either active mapping.
- The `/deployment/plc` surface distinguishes Active read-only state from Candidate editable state and renders station ranges, concrete signal addresses, confirmation controls, and the Read_Done-only allowlist.
- Collector product source was not modified.

## Validation evidence

### API and contract

`api/tests/test_deployment_plc_api.py`: **22 passed**.

Coverage includes:

- default candidate seed and candidate projection readiness;
- complete candidate save/retrieve identity and engineering export;
- deterministic hash stability under station/signal ordering changes;
- hash change for semantic confirmation changes;
- malformed Siemens address rejection;
- extra Edge-to-PLC write rejection;
- active mapping byte continuity during candidate persistence;
- existing read-only connection, overlay, stale-candidate, activation-isolated-temp-store, and rollback regressions.

Projected 3WS evidence: one line plan plus WS01/WS02/WS03 station plans. Candidate engineering range is `0:344`; the existing Collector consumer computes the physical station read plan as `0:346` because S7 strings include two framing bytes.

### Synthetic Collector / Snap7 loopback

- `collector/tests/test_field_debug_candidate_read_done.py`: **2 passed**.
- Existing `collector/tests/test_snap7_reliability_integration.py`: **1 passed**.
- `collector/tests/test_r3_runtime_projection.py` plus `collector/tests/test_r2b_connection_authority.py`: **6 passed**.

The new synthetic success path proves:

1. candidate projection is parsed by the existing Collector mapping/read-plan/decoder path;
2. the accepted WS01 event is inserted and persisted;
3. transaction commit occurs before the only PLC write;
4. the write target is candidate `WS01 / DB101.DBX6.1`, with the existing handshake byte preserved and bit 1 set;
5. storage failure rolls back and emits zero `Read_Done`/ACK writes.

Observed success order: `begin → accepted_fact → persist_cycle → commit → ack_write → ack_ok`.

### Frontend

- Focused deployment UI test: **4 passed**.
- `npm run typecheck`: PASS.
- `npm run build`: PASS.

The focused UI evidence covers Active/Candidate separation, station and signal rendering, concrete address notation, PLANNED/CONFIRMED, Read_Done-only wording, candidate editing, full-contract save payload, retrieval link, validation errors, and the existing controlled-activation boundary display.

### Integrity and protected mapping continuity

| Protected path | Entry bytes | Entry SHA-256 | Final bytes | Final SHA-256 | Result |
| --- | ---: | --- | ---: | --- | --- |
| `config/mapping.yaml` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` | 7112 | `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d` | unchanged |
| `data/deployment-config/active/mapping.yaml` | 14217 | `2b70079ccac4e2293e5a225352f5b4a30d180ed91176c6204d307c53589930a0` | 14217 | `2b70079ccac4e2293e5a225352f5b4a30d180ed91176c6204d307c53589930a0` | unchanged |

`git diff --check`: PASS.

## Changed-path accounting

Task-owned implementation/test/report paths are limited to:

- `common/line_config/debug_contract.py`
- `common/line_config/__init__.py`
- `common/line_config/runtime_projection.py`
- `api/app/services/deployment_plc.py`
- `api/tests/test_deployment_plc_api.py`
- `collector/tests/test_field_debug_candidate_read_done.py`
- `frontend/src/components/deployment-plc/DeploymentPlcClient.tsx`
- `frontend/src/components/deployment-plc/__tests__/DeploymentPlcClient.test.tsx`
- `frontend/src/lib/deploymentPlc/apiClient.ts`
- `frontend/src/styles/globals.css`
- `docs/reports/fv0_fv1a_real_plc_debug_config_report_20260817.md`

The pre-existing governance/document dirty and untracked corpus was preserved. The authoritative task file remains untracked, unstaged, and excluded from the exact stage set. No Collector source, active mapping, baseline mapping, V-PLC, Trace, or unrelated product surface was changed.

## Boundary counters and Git closeout

- `REAL_PLC_CONNECT=0`
- `REAL_PLC_READ=0`
- `REAL_PLC_WRITE=0`
- `WYSE_REMOTE_ACTION=0`
- `REMOTE_MUTATION=0`
- Snap7 activity was loopback-only under the repository-local synthetic test.
- No package install/update was run.
- No push, tag, merge, rebase, reset, stash, clean, branch/worktree creation, Docker lifecycle mutation, active candidate activation, or Collector restart was performed for this proof.
- Authorized commit message: `feat: add executable real plc debug configuration`
- The final local commit SHA, staged-path count, final ahead count, and final `git show --stat --oneline HEAD` are recorded in the Integration Thread closeout after exact-path staging and commit.

## Next gate

Single next gate: Mainline PM intake of the FV0/FV1A result. Only a separately authorized task may proceed to FV1B Wyse `linux/amd64` packaging/deployment, FV2 live address reconciliation, FV3 real PLC connection/Read_Done write, production ACK protocol, push, tag, merge, or any later phase.
