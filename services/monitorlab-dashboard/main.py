from fastapi import FastAPI
from app.api import auth, customers, events, alerts, stats
from app.db import init_db

app = FastAPI(title="MonitorLab API")

@app.on_event("startup")
async def startup():
    init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])

@app.get("/health")
async def health():
    return {"status":"ok"}

