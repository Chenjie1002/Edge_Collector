# Edge MES Demo

Offline Raspberry Pi edge MES demo for one simulated production line.

## Services

- `postgres`: local PostgreSQL storage
- `simulator`: business-level production data simulator
- `s7-plc-sim`: three-station Snap7 V-PLC with strict ACK and runtime profiles
- `collector`: polling collector, event detector, outbox writer
- `api`: FastAPI query service
- `grafana`: dashboard
- `sync-worker`: Oracle sync mock worker; Phase-2 out of scope

## Run

```bash
cp .env.example .env
docker compose up -d --build
```

Grafana:

```text
http://<host>:3000
```

Grafana and PostgreSQL credentials are configured through `.env`. The values in
`.env.example` are public Demo defaults, not production secrets. Replace them
before starting a shared or exposed environment, and do not commit the resulting
`.env`.

API:

```text
http://<host>:8000/health
```

V-PLC control:

```text
http://<host>:8200/vplc
```

The default `normal` profile uses the controlled station baseline in
`config/vplc.yaml` and locks runtime cycle-time edits. For an explicitly accelerated
demo:

```bash
VPLC_PROFILE=fast docker compose up -d --build s7-plc-sim
```

## Documentation

- `docs/DOC_INDEX.md`: canonical document map and three-thread collaboration order
- `docs/current_status.md`: current implementation status
- `docs/protocol.md`: protocol implemented by the demo
- `docs/contracts/vplc_runtime_parameters.md`: V-PLC profile, parameter audit, snapshot, and NOK simulation contract
- `docs/plc_edge_integration_guide.md`: reusable field guide for S7-300, S7-1200, and S7-1500 integration
- `docs/edge_expansion_plan.md`: planned SCADA/MES extensions
- `docs/releases/phase1_pass_release_note.md`: frozen Phase-1 PASS release summary

Current development scope is the single-machine offline Demo. Oracle integration
is not part of the current phase; `sync-worker` remains mock-only.

## Development Roadmap and Thread Model

This project is managed as a staged, non-invasive Edge MES demo. PLC remains the
control brain; Edge collects, validates, stores and visualizes data, but does not
replace PLC control logic or decide production flow.

### Phases

| Phase | Goal | Progress model | Current status |
| --- | --- | --- | --- |
| Phase 1: closed-loop demo | Prove the end-to-end V-PLC -> Collector -> PostgreSQL -> FastAPI -> Grafana / Traceability loop on a Raspberry Pi. | Build one stable single-line demo, validate strict ACK behavior, preserve legacy snapshot compatibility and freeze the PASS baseline. | PASS; tag `phase1-pass-20260619`. |
| Phase 2 Sprint 1: flexible line configuration | Make line, station and mapping configuration explicit and bounded. | Freeze architecture, implement configuration loader/validator/resolver, then pass focused review and exact allowlist commit gates. | PASS. |
| Phase 2 Sprint 2: generic station event model | Define normalized station events, lifecycle derivation, lineage, duplicate/conflict handling and production result boundaries. | Contract-first implementation with Reliability, Data Quality and Verification review gates before commit/push. | PASS. |
| Phase 2 Sprint 3: collector ingestion adapter | Bridge Collector source payloads into the shared station event model without breaking ACK, storage or production fact authority. | Advance in small slices: offline adapter, mapping hardening, runtime adapter gate, diagnostics, raw boundary tests, decoder authority, then runtime raw wiring. | Slice D3 runtime raw wiring is completed and committed at `c9e7c22`; DB/API/Dashboard/V-PLC/storage.py/ACK/deploy surfaces remain unchanged unless separately authorized. |
| Future productization | Expand from demo to stronger runtime operations, dashboard UX, data quality visibility and selected real integration pilots. | Only after explicit PM approval for DB/API/Dashboard/V-PLC/deploy/real PLC work; keep non-invasive PLC boundary. | Not authorized by default. |

### How work progresses

Work is intentionally split into small gates. A typical slice moves through:
planning -> implementation authorization -> implementation/tests -> Reliability
review -> Data Quality review -> Verification/allowlist review -> exact path
stage/commit/push -> docs/status sync. Passing one gate does not authorize the
next gate; PM must explicitly approve implementation, staging, commit, push,
deploy, rollback, runtime wiring and any schema or API surface change.

### Project Threads

| Thread | Responsibility |
| --- | --- |
| PM | Owns scope, authorization, gate ordering, allowlists, commit/push/tag/deploy decisions and cross-Thread handoff quality. |
| Architecture / Integration | Owns contracts, boundaries, implementation planning, integration design, docs repair and status sync. |
| Reliability | Reviews runtime safety, ACK/read_done behavior, retry/repair paths, fail-closed behavior and ownership boundaries. |
| Data Quality | Reviews fact authority, lineage, raw/normalized evidence, projection, NOK result/detail and observability naming. |
| Verification | Reviews fixture matrix, negative cases, regression coverage, exact allowlist compliance and final gate evidence. |

The current durable status source is `docs/current_status.md`; the Sprint 3 gate
source is `docs/reports/sprint3_collector_ingestion_adapter_gate_status.md`.
`README.md` is an orientation summary and should not be treated as the live gate
authority when it conflicts with the status documents. D3 proves runtime raw
wiring into the adapter source path only; DB/API/Dashboard/V-PLC/storage.py/ACK
or deploy changes still require separate PM authorization.

## License

MIT
