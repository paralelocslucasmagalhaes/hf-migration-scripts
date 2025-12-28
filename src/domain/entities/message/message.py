from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum
from domain.entities.contact import Contact
from domain.entities.platform import PlatformEnum
import uuid
from typing import List
from domain.entities.message.template import Template


class MessageStatusEnum(str, Enum):
    received = "received"
    sent = "sent"
    readed = "readed"
    failed = "failed"
    pending = "pending"
    requested = "requested"
    delivered = "delivered"
    read = "read"
    accepted = "accepted"
    deleted = "deleted"

@dataclass(kw_only=True)
class MessageStatus:
    status: Optional[MessageStatusEnum] = field(default=MessageStatusEnum.pending, metadata={"description": "Status"})
    created_date: datetime = field(default=datetime.now(), metadata={"description": "Timestamp of the message"})

    def __post_init__(self):
        """Validações de Domínio"""              

        if isinstance(self.status, str):
            self.status = MessageStatusEnum(self.status)

        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)       

# Defining the Enums
class AuthorEnum(str, Enum):
    USER = "user"
    AI = "ai"
    ATTENDANT = "attendant"
    COMPANY   = "company"

class DirectionEnum(str, Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"


@dataclass(kw_only=True)
class Media:
    id: Optional[str] = field(default=None, metadata={"description": "Media id"})
    caption: Optional[str] = field(default=None, metadata={"description": "Media id"})
    filename: Optional[str] = field(default=None, metadata={"description": "Media id"})
    mime_type: Optional[str] = field(default=None, metadata={"description": "Media id"})
    url: Optional[str] = field(default=None, metadata={"description": "Media id"})
    sha256: Optional[str] = field(default=None, metadata={"description": "Media id"})


@dataclass(kw_only=True)
class Message:
    id: Optional[str] = field(default=None, metadata={"description": "Message id"})
    author: AuthorEnum = field(metadata={"description": "Author of the message"})
    platform_message_id: Optional[str] = field(default=None, metadata={"description": "Platform message id"})
    company_id: Optional[str] = field(default=None, metadata={"description": "Company id"})
    chat_id: Optional[str] = field(default=None, metadata={"description": "Chat id"})
    app_id: Optional[str] = field(default=None, metadata={"description": "App id"})
    agent_id: Optional[str] = field(default=None, metadata={"description": "Agent id"})
    store_id: Optional[str] = field(default=None, metadata={"description": "Store id"})
    campaign_id: Optional[str] = field(default=None, metadata={"description": "Store id"})
    template_id: Optional[str] = field(default=None, metadata={"description": "Store id"})
    conversation_id: Optional[str] = field(default=None, metadata={"description": "Conversation id"})
    contact: Optional[Contact] = field(default=None, metadata={"description": "Consumer information"})
    # Optional fields (must define default=None)
    from_: Optional[Contact] = field(default=None, metadata={"description": "Consumer information"})
    to: Optional[Contact] = field(default=None, metadata={"description": "Consumer information"})
    message: str = field(metadata={"description": "Message content"})
    message_type: str = field(default=None, metadata={"description": "Consumer information"})
    media: Optional[Media] = field(default=None, metadata={"description": "Media"})
    direction: Optional[DirectionEnum] = field(default=None, metadata={"description": "Message direction"})
    platform: PlatformEnum = field(metadata={"description": "Platform Message channel"})
    status: Optional[MessageStatusEnum] = field(default=None, metadata={"description": "Message status"})
    status_history: Optional[List[MessageStatus]] = field(default=None, metadata={"description": "Message status"})
    template: Optional[Template] = field(default=None, metadata={"description": "Template data"})
    created_date: datetime = field(default=datetime.now(), metadata={"description": "Timestamp of the message"})
    updated_date: datetime = field(default=datetime.now(), metadata={"description": "Timestamp of the message"})


    def __post_init__(self):
        """Validações de Domínio"""
        if not self.status:
            self.status = MessageStatusEnum.pending

        if not self.status_history:
            self.status_history = [MessageStatus(status=MessageStatusEnum.pending)]

        if isinstance(self.author, str):
            self.author = AuthorEnum(self.author)
        
        if isinstance(self.direction, str):
            self.direction = DirectionEnum(self.direction)

        if isinstance(self.platform, str):
            self.platform = PlatformEnum(self.platform)

        if isinstance(self.status, str):
            self.status = MessageStatusEnum(self.status)
        
        if isinstance(self.from_, dict):
            self.from_ = Contact(** self.from_)

        if isinstance(self.to, dict):
            self.to = Contact(** self.to)
        
        if isinstance(self.media, dict):
            self.media = Media(** self.media)

        if isinstance(self.template, dict):
            self.template = Template(** self.template)

        if isinstance(self.status_history, list):
            self.status_history = [MessageStatus(** status) if isinstance(status, dict) else status for status in self.status_history]

        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
            
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)


    def update_status(self, status: MessageStatusEnum, created_date: datetime = datetime.now()):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""        
        self.status = status
        self.status_history.append(MessageStatus(status=status, created_date=created_date))

    def update_platform_message_id(self, platform_message_id: str):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""        
        self.platform_message_id = platform_message_id

@dataclass(kw_only=True)
class MessageOutgoingUpdate:
    id: Optional[str] = field(default=None, metadata={"description": "Message id"})
    platform_message_id: Optional[str] = field(default=None, metadata={"description": "Platform message id"})
    status: Optional[MessageStatusEnum] = field(default=MessageStatusEnum.requested, metadata={"description": "Message status"})