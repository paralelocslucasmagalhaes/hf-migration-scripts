from __future__ import annotations
from domain.interface.infra.db import IRepository

from domain.entities.agent.agent import Agent

class IAgentRepository(IRepository[Agent]):
    pass