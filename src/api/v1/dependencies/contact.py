from infra.repository.contact import ContactRepository
from infra.repository.consumers import ConsumerstRepository


def get_contact_respository(company_id: str) ->ContactRepository:
    return ContactRepository(company_id=company_id)

def get_consumer_respository(company_id: str) ->ConsumerstRepository:
    return ConsumerstRepository(company_id=company_id)