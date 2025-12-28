from __future__ import annotations
from domain.interface.infra.db import IRepository
from abc import ABC, abstractmethod
from domain.entities.campaign.campaign import Campaign

class ICampaignRepository(IRepository[Campaign]):
    pass

    @abstractmethod
    async def start_running(self, campanha: Campaign):
        pass

    @abstractmethod
    async def done(self, campanha: Campaign):
        pass

    @abstractmethod
    async def failed(self, campanha: Campaign):
        pass