from infra.repository_legacy.agent import AgentRepository
from fastapi import Depends

def get_agent_respository(company_id: str) ->AgentRepository:
    return AgentRepository(company_id=company_id)