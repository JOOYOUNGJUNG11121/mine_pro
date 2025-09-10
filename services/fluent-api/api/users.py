from fastapi import APIRouter, Depends
from app.deps import get_current_user

router = APIRouter()

@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"id": user.get("id"), "email": user.get("email")}
