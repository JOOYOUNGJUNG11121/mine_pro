from fastapi import FastAPI
from app.api import auth, users, devices, consumption, recommend, stats
from app.db import init_db

app = FastAPI(title="NineWatt Recommendation API")

@app.on_event("startup")
async def startup():
    init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(devices.router, prefix="/devices", tags=["devices"])
app.include_router(consumption.router, prefix="/consumption", tags=["consumption"])
app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])

@app.get("/health")
async def health():
    return {"status":"ok"}

