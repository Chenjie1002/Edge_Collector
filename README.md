# Edge MES Demo

Offline Raspberry Pi edge MES demo for one simulated production line.

## Services

- `postgres`: local PostgreSQL storage
- `simulator`: business-level production data simulator
- `collector`: polling collector, event detector, outbox writer
- `api`: FastAPI query service
- `grafana`: dashboard
- `sync-worker`: Oracle sync mock worker

## Run

```bash
cp .env.example .env
docker compose up -d --build
```

Grafana:

```text
http://<host>:3000
admin / admin
```

API:

```text
http://<host>:8000/health
```

