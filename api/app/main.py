from fastapi import FastAPI

from app.routes import events, health, kpi, machines, sync, trace

app = FastAPI(title="Edge MES API")
app.include_router(health.router)
app.include_router(machines.router)
app.include_router(kpi.router)
app.include_router(events.router)
app.include_router(sync.router)
app.include_router(trace.router)
