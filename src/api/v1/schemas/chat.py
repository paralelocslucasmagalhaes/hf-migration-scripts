from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import List
from enum import Enum
from api.v1.schemas.base import Filter

class InboundChannel(str, Enum):
    whatsapp = "whatsapp"
    instagram = "instagram"
    tiktok = "tiktok"

class HandoffEnum(str, Enum):
    AI = "ai"
    WAITING = "waiting"
    ATTENDANT = "attendant"

class ChatRequest(BaseModel):
    to: str = Field(..., description="Recipient user ID or username")
    from_: str = Field(..., alias="from", description="Sender user ID or username")
    message: Optional[str] = Field(..., description="Chat message content")    

class ChatCreate(BaseModel):
    company_id: str = Field(..., description="ID of the company")
    consumer_id: str = Field(..., description="User Contact")
    integration_id: str = Field(..., description="Operator Contact")
    handoff: HandoffEnum = Field(..., description="Handoff to Human")
    last_inbound_channel: Optional[InboundChannel] = Field(None, description="Last Inbound Channel e.g. 'whatsapp'")
    available_channels: List[InboundChannel] = Field(default_factory=list, description="Roles for the User, e.g. ['whatsapp', 'instagram']")


class HandoffRequest(BaseModel):
    company_id: str = Field(..., description="Company ID")
    chat_id: str = Field(..., description="Chat ID")
    user_id: Optional[str] = Field(None, description="User Id is handle the handoff chat")



class ChatFilter(Filter):
    company_id: Optional[str] = None