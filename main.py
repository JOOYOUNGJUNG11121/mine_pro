from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path

# Ensure service packages are importable
BASE = Path(__file__).resolve().parent / "services"
sys.path.insert(0, str(BASE))

app = FastAPI(title="Unified FastAPI Backend")

# Import routers from copied services
try:
    from fluent_api import main as fluent_main  # package from fluent-api-starter/app
    app.include_router(fluent_main.app.router, prefix="/fluent", tags=["fluent"])
except Exception as e:
    try:
        from fluent_api.api import auth  # quick check to ensure package exists
        from fluent_api import main as fluent_main2
        app.include_router(fluent_main2.app.router, prefix="/fluent", tags=["fluent"])
    except Exception as e2:
        app.add_api_route("/fluent/health", lambda: {"status": "fluent import failed", "error": str(e)})

try:
    from monitorlab_dashboard import main as monitor_main
    app.include_router(monitor_main.app.router, prefix="/monitor", tags=["monitorlab"])
except Exception as e:
    app.add_api_route("/monitor/health", lambda: {"status": "monitor import failed", "error": str(e)})

try:
    from ninewatt_recommendation import main as nine_main
    app.include_router(nine_main.app.router, prefix="/recommend", tags=["recommendation"])
except Exception as e:
    app.add_api_route("/recommend/health", lambda: {"status": "ninewatt import failed", "error": str(e)})

# ✅ Exodus Calendar (새로운 FastAPI 포팅)
try:
    from exodus_calendar.routers import accounts, events
    app.include_router(accounts.router)
    app.include_router(events.router)
except Exception as e:
    app.add_api_route("/calendar/health", lambda: {"status": "calendar import failed", "error": str(e)})

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
