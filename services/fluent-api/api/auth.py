from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.services.auth import create_user, authenticate_user, create_access_token, create_refresh_token

router = APIRouter()

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    display_name: str = None

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@router.post("/register", status_code=201)
def register(data: RegisterIn):
    user = create_user(data.email, data.password, data.display_name)
    if not user:
        raise HTTPException(status_code=400, detail="User creation failed")
    return {"id": user.id, "email": user.email}

@router.post("/login", response_model=TokenOut)
def login(data: LoginIn):
    user = authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id)
    }
