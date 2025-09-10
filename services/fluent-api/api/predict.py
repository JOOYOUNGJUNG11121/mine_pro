from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.deps import get_db, get_current_user
from app.services.model_client import call_model
from app.db import SessionLocal
from app.models import RequestLog, ResponseLog

router = APIRouter()

class PredictIn(BaseModel):
    input: dict
    input_type: str = "text"
    meta: dict = {}

class PredictOut(BaseModel):
    request_id: int
    response: dict

@router.post("/{model_id}", response_model=PredictOut)
def predict(model_id: int, body: PredictIn, user=Depends(get_current_user)):
    if body.input_type not in ("text","audio","json"):
        raise HTTPException(status_code=400, detail="Unsupported input_type")
    db = SessionLocal()
    req = RequestLog(user_id=user.get("id"), model_id=model_id, request_payload=body.dict(), request_type=body.input_type)
    db.add(req)
    db.commit()
    db.refresh(req)
    resp_data, latency = call_model(model_id, body.dict())
    resp = ResponseLog(request_id=req.id, model_id=model_id, response_payload=resp_data, latency_ms=latency, status_code=200)
    db.add(resp)
    db.commit()
    return {"request_id": req.id, "response": resp_data}
