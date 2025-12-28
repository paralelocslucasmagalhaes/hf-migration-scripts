from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from typing import List
from domain.entities.contact import Contact
from uuid import uuid4
from domain.entities.campaign.enum import StatusContactCampaignEnum

@dataclass(kw_only=True)
class CampaignContact:
    campaign_id: str
    company_id: str
    contact: Contact
    created_date: datetime
    updated_date: datetime
    status: StatusContactCampaignEnum
    id: str = field(default_factory=lambda: str(uuid4()))


    def __post_init__(self):
        
        if isinstance(self.contact, dict):
            self.contact = Contact(**self.contact)

        if isinstance(self.status, str):
            self.status = StatusContactCampaignEnum(self.status)