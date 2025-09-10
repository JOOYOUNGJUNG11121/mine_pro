from fastapi import FastAPI
from app.api import auth, users, models as models_api, predict
from app.db import init_db

app = FastAPI(title="Fluent AI API")

@app.on_event("startup")
async def startup():
    init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(models_api.router, prefix="/models", tags=["models"])
app.include_router(predict.router, prefix="/predict", tags=["predict"])

@app.get("/health")
async def health():
    return {"status":"ok"}
