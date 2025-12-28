from dataclasses import dataclass, field
from typing import Optional
from domain.entities.company.social_network import CompanySocialNetworks
from domain.entities.company.enum import CompanyStatusEnum
from typing import List
from datetime import datetime
from uuid import uuid4


@dataclass(kw_only=True)
class Company:
    name: str 
    identification_number: str
    domain: str
    created_date: datetime
    updated_date: datetime
    status: CompanyStatusEnum

    social_networks: Optional[List[CompanySocialNetworks]] = None
    digital_menu: Optional[str] = None
    who_we_are: Optional[str] = None
    what_makes_you_awesome: Optional[str] = None

    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):

        if isinstance(self.social_networks, list):
            self.social_networks = [CompanySocialNetworks(** network) for network in self.social_networks]
        
        if isinstance(self.status, str):
            self.status = CompanyStatusEnum(self.status)

        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
            
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)