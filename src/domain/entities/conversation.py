from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum
from domain.entities.contact import Contact
from domain.entities.platform import PlatformEnum
from uuid import uuid4

class HandoffEnum(str, Enum):
    AI = "ai"
    WAITING = "waiting"
    ATTENDANT = "attendant"

@dataclass(kw_only=True)
class Conversation:
    id: str = field(default_factory=lambda: str(uuid4()))
    company_id: Optional[str] = field(default=None, metadata={"description": "Company id"})
    chat_id: Optional[str] = field(default=None, metadata={"description": "Chat id"})
    contact_id: Optional[str] = field(default=None, metadata={"description": "Consumer information"})
    platform: PlatformEnum = field(metadata={"description": "Platform channel"})
    app_id: Optional[str] = field(default=None, metadata={"description": "App id"})
    store_id: Optional[str] = field(default=None, metadata={"description": "Store id"})
    csat: Optional[int] = field(default=None, metadata={"description": "CSAT"})
    end_conversation: Optional[bool] = field(default=False, metadata={"description": "End conversation"})    
    created_date: datetime = field(default=datetime.now(), metadata={"description": "Timestamp of the message"})
    updated_date: datetime = field(default=datetime.now(), metadata={"description": "Timestamp of the message"})

    def __post_init__(self):
        """Validações de Domínio"""

        if isinstance(self.platform, str):
            self.platform = PlatformEnum(self.platform)

        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
            
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)

    def set_chat(self, chat_id: str):
        self.chat_id = chat_id

    def set_contact(self, contact_id: str):
        self.contact_id = contact_id