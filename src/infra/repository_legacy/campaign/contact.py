from infra.db.base_async_no_model import AsyncFirestoreCRUD
from domain.entities.campaign.contact import CampaignContact

class CampaignContactRepository(AsyncFirestoreCRUD[CampaignContact]):
    def __init__(self, company_id: str, campaign_id: str):
        self.company_id = company_id
        self.campaign_id = campaign_id
        super().__init__(
            collection=f"companies/{company_id}/campaigns/{campaign_id}/contacts", 
            entitie=CampaignContact,            
            )
