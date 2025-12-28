from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum
from domain.entities.contact import Contact
from domain.entities.platform import PlatformEnum
from uuid import uuid4
from domain.entities.user import User
from typing import Any, Dict

class HandoffEnum(str, Enum):
    AI = "ai"
    WAITING = "waiting"
    ATTENDANT = "attendant"

class ChatStatus(str, Enum):
    active = "active"
    deactive = "inactive"

@dataclass(kw_only=True)
class Chat:
    id: str = field(default_factory=lambda: str(uuid4()))
    company_id: Optional[str] = field(default=None, metadata={"description": "Company id"})
    handoff: HandoffEnum = field(default=HandoffEnum.AI, metadata={"description": "Handoff to Human"})
    # Optional fields (must define default=None)
    contact: Optional[Contact] = field(default=None, metadata={"description": "Consumer information"})
    platform: PlatformEnum = field(metadata={"description": "Platform channel"})
    app_id: str = field(metadata={"description": "App id"})
    store_id: str = field(metadata={"description": "Store id"})
    created_date: datetime = field(default=datetime.now(), metadata={"description": "Timestamp of the message"})
    updated_date: datetime = field(default=datetime.now(), metadata={"description": "Timestamp of the message"})
    user: Optional[User] = field(default=None, metadata={"description": "User when take over"})
    status: Optional[ChatStatus] = field(default=ChatStatus.active, metadata={"description": "Consumer information"})

    def __post_init__(self):
        """Validações de Domínio"""
        
        if isinstance(self.handoff, str):
            self.handoff = HandoffEnum(self.handoff)

        if isinstance(self.status, str):
            self.status = ChatStatus(self.status)

        if isinstance(self.platform, str):
            self.platform = PlatformEnum(self.platform)

        if isinstance(self.user, dict):
            self.user = User( ** self.user)

        if isinstance(self.contact, dict):
            self.contact = Contact( ** self.contact)
        
        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
            
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)


    def take_out(self, user: User):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""        
        self.handoff = HandoffEnum.ATTENDANT
        self.user = user

    def human_handoff(self):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""        
        self.handoff = HandoffEnum.WAITING
        self.user = None

    def closeout(self):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""        
        self.handoff = HandoffEnum.AI
        self.user = None