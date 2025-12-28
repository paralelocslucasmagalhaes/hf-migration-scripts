from pydantic import BaseModel, Field
from typing import Optional
from domain.entities.contact import Contact
# Importações mantidas conforme seu original
from domain.entities.platform import PlatformEnum
from domain.entities.message.message import Media
from domain.entities.message.message import AuthorEnum


class OutgoingMessageCreate(BaseModel):
    # Pydantic v2 valida a ordem: campos obrigatórios primeiro, opcionais depois
    company_id: Optional[str] = Field(default=None, description="Company id")
    author: AuthorEnum = Field(description="Author of the message")
    chat_id: Optional[str] = Field(default=None, description="Chat id")
    app_id: Optional[str] = Field(default=None, description="App id")
    agent_id: Optional[str] = Field(default=None, description="Agent id")
    store_id: Optional[str] = Field(default=None, description="Store id")
    from_: Optional[Contact] = Field(default=None, description="Consumer information")
    to: Optional[Contact] = Field(default=None, description="Consumer information")
    message: str = Field(description="Message content")
    message_type: Optional[str] = Field(default=None, description="Message type")
    media: Optional[Media] = Field(default=None, description="Media")
    platform: PlatformEnum = Field(description="Platform Message channel")        
    