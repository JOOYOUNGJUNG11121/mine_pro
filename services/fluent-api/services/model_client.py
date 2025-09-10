import time, requests
from app.db import SessionLocal
from app.models import Model as ModelTbl

def call_model(model_id: int, payload: dict):
    db = SessionLocal()
    model = db.query(ModelTbl).filter(ModelTbl.id==model_id).first()
    if not model or not model.endpoint_url:
        # For starter, echo the input
        return {"echo": payload}, 0
    ts = time.time()
    try:
        r = requests.post(model.endpoint_url, json=payload, timeout=30)
        latency = int((time.time()-ts)*1000)
        return r.json(), latency
    except Exception as e:
        return {"error": str(e)}, int((time.time()-ts)*1000)
