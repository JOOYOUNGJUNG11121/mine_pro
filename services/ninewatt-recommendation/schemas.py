from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: str
    display_name: Optional[str]

class DeviceCreate(BaseModel):
    device_name: str
    device_type: Optional[str] = None
    metadata: Optional[Any] = None

class DeviceOut(DeviceCreate):
    id: int
    user_id: int
    created_at: datetime

class ConsumptionCreate(BaseModel):
    device_id: Optional[int] = None
    timestamp: datetime
    energy_kwh: float

class ConsumptionOut(ConsumptionCreate):
    id: int
    user_id: int
    created_at: datetime

class RecommendationOut(BaseModel):
    id: int
    user_id: int
    device_id: Optional[int]
    recommended_action: str
    estimated_saving: Optional[float]
    generated_at: datetime

