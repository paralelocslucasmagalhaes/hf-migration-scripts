from domain.exceptions.domain import DomainNotFoundException
from domain.exceptions.domain import DomainAlredyExistsException
from domain.exceptions.domain import DomainException

class CampaignException(DomainException):
    def __init__(self, msg: str):
        self.message = msg
        super().__init__(self.message)
        
class CampaignNotFoundError(DomainNotFoundException):
    def __init__(self, campaign_id: str):
        self.message = f"Campanha não encontrada para o ID {campaign_id}."
        super().__init__(self.message)