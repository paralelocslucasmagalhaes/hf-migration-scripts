from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from datetime import datetime

class Status(str, Enum):
    active = "active"
    deactive = "inactive"
    pending = "pending"

@dataclass(kw_only=True)
class Contact:
    # '...' in Pydantic means required. Here, we just don't set a default.
    id: Optional[str] = field(default=None, metadata={"description": "Contact id"})
    company_id: Optional[str] = field(default=None, metadata={"description": "Company id"})
    name: Optional[str] = field(default=None,metadata={"description": "Name"})
    # For optional fields with a default of None:
    mobile: Optional[str] = field(default=None, metadata={"description": "Consumer Mobile Phone"})
    platform_id: Optional[str] = field(default=None, metadata={"description": "Platform ID"})
    email: Optional[str] = field(default=None, metadata={"description": "Consumer Email"})
    instagram: Optional[str] = field(default=None, metadata={"description": "Consumer Instagram profile"})
    tiktok: Optional[str] = field(default=None, metadata={"description": "Consumer Tiktok profile"})
    status: Optional[Status] = field(default=Status.active, metadata={"description": "Contact status"})
    created_date: datetime = field(default=datetime.now(), metadata={"description": "Consumer Tiktok profile"})
    updated_date: datetime = field(default=datetime.now(), metadata={"description": "Consumer Tiktok profile"})

    def __post_init__(self):
        """Validações de Domínio"""

        if isinstance(self.status, str):
            self.status = Status(self.status)

        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
            
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)