from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ==== USER ====
class UserBase(BaseModel):
    email: str
    username: str
    profile_image: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True


# ==== EVENT ====
class EventBase(BaseModel):
    title: str
    description: Optional[str] = ""
    start_time: datetime
    end_time: datetime
    all_day: bool = False
    location: Optional[str] = ""
    recurrence: Optional[str] = None
    reminders: Optional[str] = ""


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: int
    owner_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
