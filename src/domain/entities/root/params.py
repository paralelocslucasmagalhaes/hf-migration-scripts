from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from typing import List
from domain.entities.root.enum import Status
from datetime import datetime

@dataclass(kw_only=True)
class WhatsAppTemplateParams:
    name: str
    path_value: str 

@dataclass(kw_only=True)
class Params:
    id: str
    status: Status
    created_date: datetime
    updated_date: datetime
    whatsapp_template: Optional[List[WhatsAppTemplateParams]]

    def __post_init__(self):

        if isinstance(self.whatsapp_template, list):
            self.whatsapp_template = [WhatsAppTemplateParams(** param) for param in self.whatsapp_template]