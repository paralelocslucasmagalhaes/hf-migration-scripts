
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
from api.v1.schemas.base import EntityCreate
from api.v1.schemas.base import EntityRead
from api.v1.schemas.membership import MembershipRead
from api.v1.schemas.base import WorkSchedule
from api.v1.schemas.base import UserRole


class UserCreate(EntityCreate):    
    name: str = Field(..., description="User name")
    email: str = Field(..., description="User email")
    mobile: Optional[str] = Field(None, description="User Mobile contact")
    photo_url: Optional[str] = Field(None, description="User Photo URL")

class UserRead(EntityRead):
    name: str = Field(..., description="User name")
    email: str = Field(..., description="User email")
    mobile: Optional[str] = Field(None, description="User Mobile contact")
    photo_url: Optional[str] = Field(None, description="User Photo URL")   
    email_verified: Optional[str] = Field(None, description="User Photo URL")
    last_login: Optional[datetime] = Field(None, description="Timestamp of the message")

class UserUpdate(EntityRead):
    name: Optional[str] = Field(..., description="User name")    
    mobile: Optional[str] = Field(None, description="User Mobile contact")
    photo_url: Optional[str] = Field(None, description="User Photo URL")   
    email_verified: Optional[str] = Field(None, description="User Photo URL")
    last_login: Optional[datetime] = Field(None, description="Timestamp of the message")



class UserCreateMembership(UserCreate):
    priority: Optional[int] = Field(None, description="User priority")
    store_id: Optional[str] = Field(None, description="Store where the User works")
    work_schedule: Optional[WorkSchedule] = Field(None, description="Weekly work schedule")
    roles: List[UserRole] = Field(default_factory=list, description="Roles for the User, e.g. ['admin', 'attendant']")
    

class UserReadMembership(UserRead):
    memberships: Optional[List[MembershipRead]] = Field(default_factory=list, description="User Mobile contact")