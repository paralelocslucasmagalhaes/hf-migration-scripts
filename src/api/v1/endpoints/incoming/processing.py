from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
import logging

from application.use_cases.chat.processing import ProcessingMessageService
from application.use_cases.outgoing.message import OutgoingMessageService
from infra.services.ai_agent import AiAsyncAgentAdapter
from infra.http.httpx import HttpXClient
from infra.pub_sub.google import GooglePubSubAsyncClient
from application.use_cases.chat.conversation import ConversationService
from application.use_cases.chat.message import MessageService
from infra.repository_legacy.conversation import ConversationRepository
from infra.repository_legacy.message import MessageRepository
from infra.pub_sub.outgoing import OutgoingPubSubService
from infra.repository_legacy.grouping import CacheFirestoreRepository

from domain.entities.message.message import Message
from domain.exceptions.domain import DomainException
from domain.exceptions.domain import DomainNotFoundException

router = APIRouter()

async def get_processing_service() -> ProcessingMessageService:

    return ProcessingMessageService(
        cache_repository=CacheFirestoreRepository(),
        agent_service=AiAsyncAgentAdapter(http_async_client=HttpXClient()),
    )

async def get_outgoing_service(company_id: str) -> OutgoingMessageService:

    return OutgoingMessageService(
        conversation_service=ConversationService(
            conversation_repository=ConversationRepository(company_id=company_id)
        ),
        message_service=MessageService(
            message_repository=MessageRepository(
            company_id=company_id
            ),
        ),
        pubsub_service=OutgoingPubSubService(
            pubsub_client=GooglePubSubAsyncClient()
        )
    )

@router.post("/processing/message", 
                            response_model=dict,                             
                            status_code=status.HTTP_200_OK)
async def processing_message(payload_message: Message) -> dict:

    try:
        # logging.info(payload)

        # payload_message = Message(**payload.model_dump())

        processing_service = await get_processing_service()
        outgoing_service = await get_outgoing_service(company_id=payload_message.company_id)

        message_response = await processing_service.processing_message(message=payload_message)

        await outgoing_service.send_message(message=message_response)

    
    except DomainNotFoundException as e:
        {"status": "ignore"}

    except DomainException as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "completed"}