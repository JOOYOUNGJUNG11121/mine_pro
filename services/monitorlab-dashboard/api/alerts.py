from fastapi import APIRouter, HTTPException
from app.db import SessionLocal
from app.models import Alert, Event
from app.schemas import AlertOut

router = APIRouter()

@router.post('/trigger/{event_id}', status_code=201)
def trigger(event_id: int):
    db = SessionLocal()
    ev = db.query(Event).filter(Event.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail='event not found')
    a = Alert(event_id=event_id, status='triggered')
    db.add(a); db.commit(); db.refresh(a)
    return {'id': a.id, 'event_id': a.event_id, 'status': a.status}

@router.post('/resolve/{alert_id}')
def resolve(alert_id: int):
    db = SessionLocal()
    a = db.query(Alert).filter(Alert.id == alert_id).first()
    if not a:
        raise HTTPException(status_code=404, detail='alert not found')
    a.status = 'resolved'
    db.commit(); db.refresh(a)
    return {'id': a.id, 'status': a.status}

