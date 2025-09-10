from fastapi import Depends, HTTPException
import os
from app.db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user():
    # Placeholder: in real app, decode JWT and fetch user
    # For starter, return a dummy user
    return {"id": 1, "email": "dev@example.com"}
