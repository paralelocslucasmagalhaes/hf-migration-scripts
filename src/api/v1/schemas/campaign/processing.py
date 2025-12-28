
from pydantic import BaseModel

class ProcessingCampaignRequest(BaseModel):
    company_id: str  # <--- Este campo vai definir qual Repo usar
    campaign_id: str
    app_id: str
    template_id: str