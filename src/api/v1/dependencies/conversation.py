from infra.repository.conversation import ConversationRepository
from pydantic import BaseModel
from fastapi import Depends

def get_conversation_respository(company_id: str) ->ConversationRepository:
    return ConversationRepository(company_id=company_id)