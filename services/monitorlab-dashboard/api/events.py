from fastapi import APIRouter, Depends, HTTPException, Query
from app.db import SessionLocal
from app.models import Event, Customer
from app.schemas import EventCreate, EventOut
from typing import List
from datetime import datetime

router = APIRouter()

@router.post('', response_model=EventOut, status_code=201)
def create_event(payload: EventCreate):
    db = SessionLocal()
    if not db.query(Customer).filter(Customer.id == payload.customer_id).first():
        raise HTTPException(status_code=404, detail='customer not found')
    e = Event(customer_id=payload.customer_id, event_type=payload.event_type, severity=payload.severity, event_time=payload.event_time, raw_data=payload.raw_data)
    db.add(e); db.commit(); db.refresh(e)
    return e

@router.get('', response_model=List[EventOut])
def list_events(customer_id: int = None, start: datetime = None, end: datetime = None, limit: int = 100):
    db = SessionLocal()
    qs = db.query(Event)
    if customer_id:
        qs = qs.filter(Event.customer_id == customer_id)
    if start:
        qs = qs.filter(Event.event_time >= start)
    if end:
        qs = qs.filter(Event.event_time <= end)
    return qs.order_by(Event.event_time.desc()).limit(limit).all()

