from infra.repository.message import MessageRepository
from api.v1.schemas.message import MessageChatFilter
from application.use_cases.chat.message import MessageService
from fastapi import Depends

def get_message_respository(company_id: str) ->MessageRepository:
    return MessageRepository(company_id=company_id)




def get_chat_message_payload(payload: MessageChatFilter) -> MessageChatFilter:
    return payload


def get_message_repository_from_chat_message_payload_payload(
        payload: MessageChatFilter = Depends(get_chat_message_payload)) -> MessageRepository:
    return get_message_respository(company_id=payload.company_id)

def get_chat_message_use_case(
        message_repository= Depends(get_message_respository)
    ) -> MessageService:
    return MessageService(
        message_repository= message_repository,
        
    )
