from infra.repository.chat import ChatRepository
from typing import Annotated
from fastapi import Depends
from application.use_cases.chat.chat import ChatService
from api.v1.dependencies.user import get_user_respository
from api.v1.schemas.chat import HandoffRequest


def get_chat_respository(company_id: str) ->ChatRepository:
    return ChatRepository(company_id=company_id)

def get_handoff_payload(payload: HandoffRequest) -> HandoffRequest:
    return payload

def get_chat_repository_from_handoff_payload(
        payload: HandoffRequest = Depends(get_handoff_payload)) -> ChatService:
    return get_chat_respository(company_id=payload.company_id)


def get_handoff_use_case(
        chat_repository= Depends(get_chat_repository_from_handoff_payload),
        user_repository= Depends(get_user_respository)
        
    ) -> ChatService:
    return ChatService(
        chat_repository= chat_repository,
        user_repository= user_repository
    )

def get_chat_use_case(
        chat_repository= Depends(get_chat_respository),
        user_repository= Depends(get_user_respository)
        
    ) -> ChatService:
    return ChatService(
        chat_repository= chat_repository,
        user_repository= user_repository
    )