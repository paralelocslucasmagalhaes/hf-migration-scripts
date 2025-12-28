from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from domain.entities.store.enum import StoreStatusEnum
from domain.entities.store.work_schedule import WorkSchedule
from uuid import uuid4

@dataclass(kw_only=True)
class Store:
    id: str = field(default_factory=lambda: str(uuid4()))
    company_id: str 
    name: str 
    location: str = None
    status: StoreStatusEnum 
    created_date: datetime 
    updated_date: datetime 
    information: Optional[str] = None
    work_schedule: Optional[WorkSchedule]  = None

    def __post_init__(self):
        """Validações de Domínio"""

        if isinstance(self.status, str):
            self.status = StoreStatusEnum(self.status)

        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
            
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)