from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from datetime import datetime
from datetime import time


class Status(str, Enum):
    active = "active"
    deactive = "inactive"

class EntityCreate(BaseModel):
    status: Optional[Status] = Field(Status.active, description="Status of the entity, e.g active")

class EntityRead(BaseModel):
    id: str = Field(..., description="Entity id")
    status: Status = Field(..., description="Status of the entity, e.g active")
    created_date: datetime = Field(..., description="Timestamp of the message")
    updated_date: datetime = Field(..., description="Timestamp of the message")

class EntityDelete(BaseModel):
    status: Optional[Status] = Field(Status.deactive, description="Status of the entity, e.g active")


class WorkDaySchedule(BaseModel):
    start: Optional[time] = Field(None, description="Start time, e.g. 09:00")
    end: Optional[time] = Field(None, description="End time, e.g. 18:00")

class WorkSchedule(BaseModel):
    monday: Optional[WorkDaySchedule] = None
    tuesday: Optional[WorkDaySchedule] = None
    wednesday: Optional[WorkDaySchedule] = None
    thursday: Optional[WorkDaySchedule] = None
    friday: Optional[WorkDaySchedule] = None
    saturday: Optional[WorkDaySchedule] = None
    sunday: Optional[WorkDaySchedule] = None

class UserRole(str, Enum):
    super = "super"
    admin = "admin"
    viewer = "viewer"
    attendant = "attendant"

class PlatformEnum(str, Enum):
    whatsapp = "whatsapp"
    twilio = "twilio"
    instagram = "instagram"
    tiktok = "tiktok"


class Filter(BaseModel):    
    limit: int = Field(50, ge=1, le=100)
    offset: int = Field(0, ge=0)
    order_by: str = Field("created_date")
    descending: bool = Field(True)