from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.campaign import Campaign
from domain.interface.repository.campaign import ICampaignRepository
from dataclasses import asdict

class CampaignRepository(AsyncFirestoreCRUD[Campaign], ICampaignRepository):
    def __init__(self, company_id: str):
        self.company_id = company_id
        super().__init__(
            collection=f"companies/{company_id}/campaigns", 
            entitie=Campaign,            
            )
        
    async def start_running(self, campaign: Campaign) -> Campaign:
        campaign.mark_as_running()
        return await self.update(id= campaign.id, document=asdict(campaign))
    
    async def done(self, campaign: Campaign) -> Campaign:
        campaign.mark_as_done()
        return await self.update(id= campaign.id, document=asdict(campaign))
    
    async def failed(self, campaign: Campaign) -> Campaign:
        campaign.mark_as_failed()
        return await self.update(id= campaign.id, document=asdict(campaign))

        