from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4
from typing import Any
from typing import Dict


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass(kw_only=True)
class User:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str
    email: str
    status: UserStatus
    mobile: Optional[str] = None
    photo_url: Optional[str] = None
    email_verified: Optional[bool] = False  # Ajustado para bool se fizer sentido
    last_login: Optional[datetime] = None
    created_date: datetime = field(default_factory=datetime.now())
    updated_date: datetime = field(default_factory=datetime.now())

    def __post_init__(self):
        """Validações de Domínio"""

        if isinstance(self.status, str):
            self.status = UserStatus(self.status)
    
        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
            
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)