from fastapi import FastAPI

from app.routes import (
    accepted_station_events,
    deployment_plc,
    events,
    health,
    kpi,
    line_summary,
    machines,
    process_metrics,
    quality_trace,
    scope_options,
    sync,
    trace,
)

app = FastAPI(title="Edge MES API")
app.include_router(health.router)
app.include_router(machines.router)
app.include_router(kpi.router)
app.include_router(events.router)
app.include_router(sync.router)
app.include_router(trace.router)
app.include_router(accepted_station_events.router)
app.include_router(quality_trace.router)
app.include_router(process_metrics.router)
app.include_router(scope_options.router)
app.include_router(deployment_plc.router)
app.include_router(line_summary.router)
