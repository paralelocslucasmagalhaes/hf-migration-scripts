
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional
from domain.entities.campaign.enum import StatusCampaignEnum
from domain.entities.campaign.schedule import CampaignSchedule
from domain.exceptions.campaign.schedule import ScheduleCampaignException
from domain.exceptions.campaign.schedule import ScheduleCampaignValueError

from uuid import uuid4
from typing import List

@dataclass(kw_only=True)
class Campaign:
    # --- Campos Obrigatórios ---
    company_id: str
    name: str
    created_date: datetime
    updated_date: datetime

    # --- Campos Opcionais (Com valor padrão ou None) ---
    target_audience: Optional[str] = None
    objective: Optional[str] = None
    menu: Optional[str] = None
    app_id: Optional[str] = None
    template_id: Optional[str] = None
    status: StatusCampaignEnum = StatusCampaignEnum.draft
    schedule: Optional[CampaignSchedule] = None
    
    # Exemplo de ID único da entidade
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        """Validações de Domínio"""
        if not self.name:
            raise ScheduleCampaignValueError("O nome da campanha é obrigatório.")
        
        if isinstance(self.status, str):
            self.status = StatusCampaignEnum(self.status)

        if isinstance(self.schedule, dict):
            self.schedule = CampaignSchedule(** self.schedule)
        
    def validate_for_scheduling(self):
        """Regra de negócio: impede agendamentos inválidos."""
        if not self.schedule:
            raise ScheduleCampaignValueError("Nenhum agendamento realizado.")

        if self.schedule.schedule_date < datetime.now(timezone.utc):
            raise ScheduleCampaignValueError("Data de agendamento não pode ser no passado.")
        
        if self.schedule and self.schedule.schedule_date < self.created_date:
            raise ScheduleCampaignValueError("O agendamento não pode ser anterior à criação.")
        
    def validate_for_changing_schedule(self):
        if self.status in [StatusCampaignEnum.running, StatusCampaignEnum.completed]:
            raise ScheduleCampaignException("Campanha já encerrada ou em execução.")
    
    @property
    def is_scheduling_less_than_thirdy_days(self) -> bool:
        """Regra de negócio: impede agendamentos inválidos."""
        if not self.schedule:
            return False
        
        if self.schedule.schedule_date < (datetime.now(timezone.utc) + timedelta(days=30)):
            return True
        
        return False
        
    def mark_as_pending(self):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""        
        self.schedule.updated_date = datetime.now(timezone.utc)
        self.status = StatusCampaignEnum.pending

    def mark_as_canceled(self,):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""
        self.schedule.task_id      = None
        self.schedule.updated_date = datetime.now(timezone.utc)
        self.status = StatusCampaignEnum.draft
        
    def mark_as_queued(self, task_id: str):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""
        self.schedule.task_id = task_id
        self.schedule.updated_date = datetime.now(timezone.utc)
        self.status = StatusCampaignEnum.queued

    def mark_as_running(self):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""        
        self.status = StatusCampaignEnum.running

    def mark_as_failed(self):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""        
        self.status = StatusCampaignEnum.failed

    def mark_as_done(self):
        """Muda o estado da entidade quando o serviço de task confirma o agendamento."""        
        self.status = StatusCampaignEnum.completed

    @property
    def delay_seconds(self) -> int:
        """Calcula o atraso necessário a partir do momento atual."""
        now = datetime.now(timezone.utc)
        if self.schedule.schedule_date <= now:
            return 0
        
        delta = self.schedule.schedule_date - now
        return int(delta.total_seconds())
    
    @property
    def is_queued(self) -> bool:
        """Regra de negócio: impede agendamentos inválidos."""
        if not self.schedule:
            return False
        if self.schedule.task_id:
            return True
        return False