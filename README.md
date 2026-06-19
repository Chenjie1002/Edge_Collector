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

## License

MIT
