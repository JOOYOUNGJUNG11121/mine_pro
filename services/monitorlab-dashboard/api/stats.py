from fastapi import APIRouter, Query
from app.db import SessionLocal
from app.models import Event
from sqlalchemy import func
from datetime import datetime, timedelta

router = APIRouter()

@router.get('/overview')
def overview(customer_id: int = None, hours: int = 24):
    db = SessionLocal()
    since = datetime.utcnow() - timedelta(hours=hours)
    qs = db.query(Event)
    if customer_id:
        qs = qs.filter(Event.customer_id == customer_id)
    total = qs.filter(Event.event_time >= since).count()
    by_severity = dict(db.query(Event.severity, func.count(Event.id)).filter(Event.event_time >= since).group_by(Event.severity).all())
    top_types = db.query(Event.event_type, func.count(Event.id)).filter(Event.event_time >= since).group_by(Event.event_type).order_by(func.count(Event.id).desc()).limit(5).all()
    return {'total': total, 'by_severity': by_severity, 'top_types': top_types}

