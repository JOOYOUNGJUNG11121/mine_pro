from fastapi import APIRouter, Depends, HTTPException, Query
from app.db import SessionLocal
from app.models import Consumption, Device, User
from app.schemas import ConsumptionCreate, ConsumptionOut
from typing import List
from datetime import datetime

router = APIRouter()

@router.post('', response_model=ConsumptionOut, status_code=201)
def ingest(payload: ConsumptionCreate, user_id: int = 1):
    db = SessionLocal()
    if payload.device_id and not db.query(Device).filter(Device.id == payload.device_id).first():
        raise HTTPException(status_code=404, detail='device not found')
    c = Consumption(user_id=user_id, device_id=payload.device_id, timestamp=payload.timestamp, energy_kwh=payload.energy_kwh)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get('', response_model=List[ConsumptionOut])
def query_consumption(user_id: int = 1, start: datetime = None, end: datetime = None, limit: int = 100):
    db = SessionLocal()
    qs = db.query(Consumption).filter(Consumption.user_id == user_id)
    if start:
        qs = qs.filter(Consumption.timestamp >= start)
    if end:
        qs = qs.filter(Consumption.timestamp <= end)
    return qs.order_by(Consumption.timestamp.desc()).limit(limit).all()

