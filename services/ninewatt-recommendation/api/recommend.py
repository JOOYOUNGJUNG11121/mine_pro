from fastapi import APIRouter
from app.db import SessionLocal
from app.models import Consumption, Device, Recommendation
from app.schemas import RecommendationOut
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

router = APIRouter()

def simple_recommend_for_user(user_id: int, days: int = 7):
    db = SessionLocal()
    # pull recent consumption for user
    since = datetime.utcnow() - timedelta(days=days)
    rows = db.query(Consumption).filter(Consumption.user_id == user_id, Consumption.timestamp >= since).all()
    if not rows:
        return []
    df = pd.DataFrame([{'device_id': r.device_id, 'ts': r.timestamp, 'kwh': r.energy_kwh} for r in rows])
    # group by device and compute mean consumption
    res = []
    for device_id, g in df.groupby('device_id'):
        mean_kwh = g['kwh'].mean()
        std_kwh = g['kwh'].std() if len(g) > 1 else 0.0
        # naive rule: if mean > threshold, recommend inspection or schedule shift
        threshold = max(0.5, mean_kwh * 0.8)
        if mean_kwh > threshold:
            action = f"Reduce usage during peak hours or tune device settings (mean={mean_kwh:.3f} kWh)"
            est_save = (mean_kwh - threshold) * 24  # rough daily estimate
            res.append({'device_id': int(device_id) if device_id is not None else None, 'action': action, 'est_save': float(est_save)})
    return res

@router.get('/user/{user_id}', response_model=list)
def recommend_user(user_id: int):
    recs = simple_recommend_for_user(user_id)
    # persist recommendations
    db = SessionLocal()
    out = []
    for r in recs:
        rec = Recommendation(user_id=user_id, device_id=r['device_id'], recommended_action=r['action'], estimated_saving=r['est_save'], metadata={})
        db.add(rec)
        db.commit(); db.refresh(rec)
        out.append({'id': rec.id, 'user_id': rec.user_id, 'device_id': rec.device_id, 'recommended_action': rec.recommended_action, 'estimated_saving': rec.estimated_saving, 'generated_at': rec.generated_at})
    return out

