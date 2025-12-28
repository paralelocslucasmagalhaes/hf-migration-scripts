
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
from datetime import time
from api.v1.schemas.base import EntityCreate
from api.v1.schemas.base import EntityRead
from api.v1.schemas.base import WorkSchedule
from api.v1.schemas.base import UserRole

class MembershipCreate(EntityCreate):
    company_id: str = Field(..., description="Company id")
    user_id: str = Field(..., description="User id")
    priority: Optional[int] = Field(None, description="User priority")
    store_id: Optional[str] = Field(None, description="Store where the User works")
    work_schedule: Optional[WorkSchedule] = Field(None, description="Weekly work schedule")
    roles: List[UserRole] = Field(default_factory=list, description="Roles for the User, e.g. ['admin', 'attendant']")

class MembershipRead(EntityRead):
    id: str = Field(..., description="Membership ID")
    user_id: str = Field(..., description="User id")
    company_id: str = Field(..., description="Company id")
    priority: Optional[int] = Field(None, description="User priority")
    store_id: Optional[str] = Field(None, description="Store where the User works")
    work_schedule: Optional[WorkSchedule] = Field(None, description="Weekly work schedule")
    roles: List[UserRole] = Field(default_factory=list, description="Roles for the User, e.g. ['admin', 'attendant']")

class MembershipUpdate(EntityRead):
    priority: Optional[int] = Field(None, description="User priority")
    store_id: Optional[str] = Field(None, description="Store where the User works")
    work_schedule: Optional[WorkSchedule] = Field(None, description="Weekly work schedule")
    roles: List[UserRole] = Field(default_factory=list, description="Roles for the User, e.g. ['admin', 'attendant']")