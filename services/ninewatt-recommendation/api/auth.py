from fastapi import APIRouter, HTTPException, Depends
from app.db import SessionLocal
from app.models import User
from app.schemas import UserCreate
from passlib.context import CryptContext
from jose import jwt
import os

router = APIRouter()
pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
JWT_SECRET = os.environ.get('JWT_SECRET', 'change_this_secret')

@router.post('/register', status_code=201)
def register(payload: UserCreate):
    db = SessionLocal()
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail='email exists')
    hashed = pwd_ctx.hash(payload.password)
    u = User(email=payload.email, password_hash=hashed, display_name=payload.display_name)
    db.add(u); db.commit(); db.refresh(u)
    return {'id': u.id, 'email': u.email}

@router.post('/token')
def token(payload: UserCreate):
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not pwd_ctx.verify(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='invalid credentials')
    token = jwt.encode({'user_id': user.id}, JWT_SECRET, algorithm='HS256')
    return {'access_token': token, 'token_type': 'bearer'}

