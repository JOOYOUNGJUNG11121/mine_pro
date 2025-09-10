from app.db import SessionLocal
from app.models import User
from passlib.context import CryptContext
from jose import jwt
import os
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.environ.get("JWT_SECRET", "change_this_secret")

def create_user(email, password, display_name=None):
    db = SessionLocal()
    hashed = pwd_ctx.hash(password)
    u = User(email=email, password_hash=hashed, display_name=display_name)
    db.add(u)
    try:
        db.commit()
        db.refresh(u)
        return u
    except Exception as e:
        db.rollback()
        return None

def authenticate_user(email, password):
    db = SessionLocal()
    user = db.query(User).filter(User.email==email).first()
    if not user:
        return None
    if not pwd_ctx.verify(password, user.password_hash):
        return None
    return user

def create_access_token(user_id: int):
    return jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm="HS256")

def create_refresh_token(user_id: int):
    return jwt.encode({"user_id": user_id, "type": "refresh"}, JWT_SECRET, algorithm="HS256")
