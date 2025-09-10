from fastapi import APIRouter, Depends, HTTPException
from app.db import SessionLocal
from app.models import User
from app.schemas import UserOut
from typing import List

router = APIRouter()

@router.get('', response_model=List[UserOut])
def list_users():
    db = SessionLocal()
    return db.query(User).all()

