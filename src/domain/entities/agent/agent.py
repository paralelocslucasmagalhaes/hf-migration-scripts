from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from domain.entities.agent.enum import AgentStatus

@dataclass(kw_only=True)
class Agent:
    company_id: str
    name: str
    id: str
    status: AgentStatus
    created_date: datetime
    updated_date: datetime
    # Campos opcionais com default precisam ficar por último na herança
    avatar: Optional[str] = None
    personality: Optional[str] = None
    restriction: Optional[str] = None
    tone: Optional[str] = None
    general_information: Optional[str] = None
    end_conversation: Optional[str] = None
    service_rules: Optional[str] = None
    handoff_to_human: Optional[str] = None

    def __post_init__(self):

        # 1. Executa a conversão de Status e Datas da classe pai
        if isinstance(self.status, str):
            self.status = AgentStatus(self.status)
        
        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
            
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)