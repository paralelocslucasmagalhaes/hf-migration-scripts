from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from domain.entities.apps.whatsapp.app import WhatsAppApp
from typing import Optional

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive" # Renamed from 'deactive' for consistency
    PENDING = "pending"

class Platform(str, Enum):
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    TWILIO = "twilio"

@dataclass(kw_only=True)
class App:
    id: str = field(metadata={"description": "App id"})
    status: Status = field(metadata={"description": "Status of the entity, e.g active"})
    company_id: str = field(metadata={"description": "Company ID"})
    store_id: str = field(metadata={"description": "Store ID"})
    agent_id: str = field(metadata={"description": "Agent ID"})
    platform: Platform = field(metadata={"description": "Type of integration"})
    platform_id: str = field(metadata={"description": "Platform specific integration ID"})
    app: Optional[WhatsAppApp] = field(default=None, metadata={"description": "Platform specific data"})
    created_date: datetime = field(metadata={"description": "Timestamp of the message"})
    updated_date: datetime = field(metadata={"description": "Timestamp of the message"})

    def __post_init__(self):
        """Validações de Domínio"""

        if isinstance(self.app, dict):
            self.app = WhatsAppApp(** self.app)

        if isinstance(self.status, str):
            self.status = Status(self.status)

        if isinstance(self.platform, str):
            self.platform = Platform(self.platform)

        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
            
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)