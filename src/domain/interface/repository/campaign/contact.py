from __future__ import annotations
from domain.interface.infra.db import IRepository

from domain.entities.campaign.contact import CampaignContact

class ICampaignContactRepository(IRepository[CampaignContact]):
    pass