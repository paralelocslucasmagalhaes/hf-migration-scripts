from fastapi import Depends
from infra.repository_legacy.integrations import IntegrationRepository

def get_integration_respository() ->IntegrationRepository:
    return IntegrationRepository()