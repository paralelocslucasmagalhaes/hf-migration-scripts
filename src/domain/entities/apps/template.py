from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from domain.entities.whatsapp.template import WhatsAppTemplate
from typing import Optional

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive" # Renamed from 'deactive' for consistency
    PENDING = "pending"

@dataclass(kw_only=True)
class Template:
    id: str = field(metadata={"description": "Template id"})
    app_id:str = field(metadata={"description": "App id"})
    company_id: str = field(metadata={"description": "Company ID"})
    status: Status = field(default_factory=Status.ACTIVE, metadata={"description": "Status of the entity, e.g active"})
    waba_id:  str = field(metadata={"description": "WhatsApp Account Id"})
    created_date: datetime = field( metadata={"description": "Timestamp of the message"})
    updated_date: datetime = field( metadata={"description": "Timestamp of the message"})
    template: Optional[WhatsAppTemplate] = None

    def __post_init__(self):
        """Validações de Domínio"""
        if isinstance(self.template, dict):
            self.template = WhatsAppTemplate(** self.template)

        if isinstance(self.status, str):
            self.status = Status(self.status)