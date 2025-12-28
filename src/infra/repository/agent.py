from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.agent.agent import Agent

class AgentRepository(AsyncFirestoreCRUD[Agent]):
    def __init__(self, company_id: str):
        self.company_id = company_id
        super().__init__(
            collection=f"companies/{company_id}/agents", 
            entitie=Agent,            
            )