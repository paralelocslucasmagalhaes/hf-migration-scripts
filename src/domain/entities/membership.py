from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

# --- Enums ---

class UserRole(str, Enum):
    super = "super"
    admin = "admin"
    viewer = "viewer"
    attendant = "attendant"

class Status(str, Enum):
    active = "active"
    inactive = "inactive" # Corrigido para bater com o valor string "inactive"
    pending = "pending"

# --- Classes de Suporte ---

@dataclass
class WorkDaySchedule:
    start_time: str
    end_time: str
    # Adicione outros campos de WorkDaySchedule conforme sua necessidade

@dataclass
class WorkSchedule:
    monday: Optional[WorkDaySchedule] = None
    tuesday: Optional[WorkDaySchedule] = None
    wednesday: Optional[WorkDaySchedule] = None
    thursday: Optional[WorkDaySchedule] = None
    friday: Optional[WorkDaySchedule] = None
    saturday: Optional[WorkDaySchedule] = None
    sunday: Optional[WorkDaySchedule] = None

    def __post_init__(self):
        # Converte dicts em WorkDaySchedule para cada dia da semana
        for day in self.__dataclass_fields__:
            value = getattr(self, day)
            if isinstance(value, dict):
                setattr(self, day, WorkDaySchedule(**value))

# --- Entidades Principais ---


@dataclass(kw_only=True)
class Membership:
    id: str
    user_id: str
    company_id: str
    status: Status
    created_date: datetime
    updated_date: datetime
    
    # Campos opcionais ou com default_factory
    priority: Optional[int] = None
    store_id: Optional[str] = None
    work_schedule: Optional[WorkSchedule] = None
    roles: List[UserRole] = field(default_factory=list)

    def __post_init__(self):

        # 2. Inicializa WorkSchedule se vier como dict
        if isinstance(self.work_schedule, dict):
            self.work_schedule = WorkSchedule(**self.work_schedule)

        # 3. Inicializa Lista de Enums (converte strings para UserRole)
        if isinstance(self.roles, list):
            self.roles = [
                UserRole(r) if isinstance(r, str) else r 
                for r in self.roles
            ]
        
        if isinstance(self.status, str):
            self.status = Status(self.status)
        
        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
            
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)