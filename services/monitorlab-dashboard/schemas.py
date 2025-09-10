from pydantic import BaseModel, Field, Json
from typing import Optional, Any, List
from datetime import datetime

class CustomerCreate(BaseModel):
    name: str
    company: Optional[str] = None
    contact_email: Optional[str] = None

class CustomerOut(CustomerCreate):
    id: int
    created_at: datetime

class EventCreate(BaseModel):
    customer_id: int
    event_type: str
    severity: str = Field(..., regex='^(low|medium|high|critical)$')
    event_time: datetime
    raw_data: Optional[Any] = None

class EventOut(EventCreate):
    id: int
    created_at: datetime

class AlertOut(BaseModel):
    id: int
    event_id: int
    status: str
    notified_at: Optional[datetime] = None
    created_at: datetime

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

