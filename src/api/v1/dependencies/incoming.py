from fastapi import Depends
from application.use_cases.incoming.message import IncomingMessageService
from api.v1.schemas.incoming import IncomingMessageCreate
from application.use_cases.chat.chat import ChatService
from application.use_cases.chat.message import MessageService
from application.use_cases.chat.conversation import ConversationService
from application.use_cases.chat.group import GroupMessageService
from application.use_cases.contact.contact import ContactService
from api.v1.dependencies.legacy.chat import get_chat_respository
from api.v1.dependencies.legacy.contact import get_contact_respository
from api.v1.dependencies.conversation import get_conversation_respository
from api.v1.dependencies.legacy.message import get_message_respository
from api.v1.dependencies.infra import get_cache_repository
from api.v1.dependencies.infra import get_group_message_tasks_service
from api.v1.schemas.pubsub import PubSubCreate
from application.mappers.pubsub import PubSubMessageMapper
from application.use_cases.incoming.event import IncomingEventService


from api.v1.dependencies.legacy.user import get_user_respository


def get_incoming_message_payload(payload: PubSubCreate = Depends(PubSubMessageMapper.pubsub_to_incoming_message)) -> IncomingMessageCreate:
    return payload

def get_chat_service_from_incoming_message_payload(
        payload: PubSubCreate = Depends(get_incoming_message_payload)) -> ChatService:
    return ChatService(
            chat_repository=get_chat_respository(company_id=payload.company_id),
            user_repository=get_user_respository()
        )

def get_contact_service_from_incoming_message_payload(
        payload: PubSubCreate = Depends(get_incoming_message_payload)) -> ContactService:
    return ContactService(
            contact_repository=get_contact_respository(company_id=payload.company_id),            
        )


def get_conversation_service_from_incoming_message_payload(
        payload: PubSubCreate = Depends(get_incoming_message_payload)) -> ConversationService:
    return ConversationService(
            conversation_repository=get_conversation_respository(company_id=payload.company_id),            
        )

def get_message_service_from_incoming_message_payload(
        payload: PubSubCreate = Depends(get_incoming_message_payload)) -> MessageService:
    return MessageService(
            message_repository=get_message_respository(company_id=payload.company_id),            
        )


def get_group_service() -> GroupMessageService:
    return GroupMessageService(
            cache_repository=get_cache_repository(),
            tasks_client=get_group_message_tasks_service()           
        )

def get_incoming_message_use_case(
        chat_service=Depends(get_chat_service_from_incoming_message_payload),
        contact_service=Depends(get_contact_service_from_incoming_message_payload),
        conversation_service=Depends(get_conversation_service_from_incoming_message_payload),
        group_service=Depends(get_group_service),
        message_service=Depends(get_message_service_from_incoming_message_payload),

) -> IncomingMessageService:

    return IncomingMessageService(
        chat_service=chat_service,
        contact_service=contact_service,
        conversation_service=conversation_service,
        group_service=group_service,
        message_service=message_service
    )


def get_incoming_event_use_case(
        message_service=Depends(get_message_service_from_incoming_message_payload)
        
) -> IncomingEventService:
    
    return IncomingEventService(
        message_service=message_service

    )
