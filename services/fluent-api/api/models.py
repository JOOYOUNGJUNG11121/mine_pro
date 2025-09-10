from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import SessionLocal
from app.models import Model as ModelTbl

router = APIRouter()

class ModelIn(BaseModel):
    name: str
    version: str
    endpoint_url: str = None
    metadata: dict = {}

@router.post("", status_code=201)
def create_model(data: ModelIn):
    db = SessionLocal()
    m = ModelTbl(name=data.name, version=data.version, endpoint_url=data.endpoint_url, metadata=data.metadata)
    db.add(m)
    db.commit()
    db.refresh(m)
    return {"id": m.id, "name": m.name, "version": m.version}
