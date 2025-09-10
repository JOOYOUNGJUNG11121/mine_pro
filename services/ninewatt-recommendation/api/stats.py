from fastapi import APIRouter, Query
from app.db import SessionLocal
from app.models import Consumption
from sqlalchemy import func
from datetime import datetime, timedelta

router = APIRouter()

@router.get('/overview')
def overview(user_id: int = 1, days: int = 7):
    db = SessionLocal()
    since = datetime.utcnow() - timedelta(days=days)
    total = db.query(func.sum(Consumption.energy_kwh)).filter(Consumption.user_id == user_id, Consumption.timestamp >= since).scalar() or 0.0
    avg_daily = (total / days) if days > 0 else 0.0
    return {'total_kwh': float(total), 'avg_daily_kwh': float(avg_daily)}

