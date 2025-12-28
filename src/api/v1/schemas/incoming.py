from pydantic import Field
from typing import List, Optional, Literal
from pydantic import BaseModel
from api.v1.schemas.webhook.whatsapp import WhatsAppWebhook
from api.v1.schemas.webhook.instagram import IntagramWebhook

from api.v1.schemas.base import PlatformEnum

class IncomingMessageCreate(BaseModel):
    company_id: str = Field(..., description="Company ID")
    app_id: str = Field(..., description="Platform Application ID")
    agent_id: Optional[str] = Field(None, description="Agent ID")
    store_id: Optional[str] = Field(None, description="Store ID")
    platform: Optional[PlatformEnum] = Field(None, description="Type of platform")
    whatsapp: Optional[WhatsAppWebhook] = Field(None, description="WhatsApp Webhook")
    instagram: Optional[IntagramWebhook] = Field(None, description="WhatsApp Webhook")