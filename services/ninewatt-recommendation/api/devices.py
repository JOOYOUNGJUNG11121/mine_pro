from fastapi import APIRouter, Depends, HTTPException
from app.db import SessionLocal
from app.models import Device, User
from app.schemas import DeviceCreate, DeviceOut
from typing import List

router = APIRouter()

@router.post('', response_model=DeviceOut, status_code=201)
def create_device(payload: DeviceCreate, user_id: int = 1):
    db = SessionLocal()
    # starter: assign to provided user_id (in real app, use current_user)
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(status_code=404, detail='user not found')
    d = Device(user_id=user_id, device_name=payload.device_name, device_type=payload.device_type, metadata=payload.metadata)
    db.add(d); db.commit(); db.refresh(d)
    return d

@router.get('', response_model=List[DeviceOut])
def list_devices(user_id: int = 1):
    db = SessionLocal()
    return db.query(Device).filter(Device.user_id == user_id).all()

