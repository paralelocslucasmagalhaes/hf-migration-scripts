from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import BackgroundTasks
import logging

from application.use_cases.outgoing.message import OutgoingMessageService
from api.v1.schemas.outgoing import OutgoingMessageCreate
from api.v1.schemas.pubsub import PubSubCreate
from infra.repository_legacy.message import MessageRepository
from infra.repository_legacy.conversation import ConversationRepository
from infra.pub_sub.google import GooglePubSubAsyncClient
from application.use_cases.chat.conversation import ConversationService
from application.use_cases.chat.message import MessageService
from infra.pub_sub.outgoing import OutgoingPubSubService

from domain.exceptions.domain import DomainException
from domain.exceptions.domain import DomainNotFoundException
from application.mappers.outgoing import OutgoingMapper
from application.mappers.pubsub import PubSubMessageMapper

from api.v1.schemas.pubsub import PubSubRead

router = APIRouter()

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


@router.post("/outgoing/message", 
                            response_model=PubSubCreate,                             
                            status_code=status.HTTP_200_OK)
async def outgoing_message(payload: OutgoingMessageCreate) -> dict:

    try:
        mapper = OutgoingMapper()
        logging.info(payload)

        message = mapper.to_domain_message(message=payload)
        conversation = mapper.to_domain_conversation(message=payload)

        outgoing_service = await get_outgoing_service(company_id=message.company_id)
        
        await outgoing_service.outgoing_message(conversation=conversation, message=message)
    
    except DomainNotFoundException as e:
        {"status": "ignore"}

    except DomainException as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "completed"}



@router.post("/outgoing/response", 
                            response_model=PubSubCreate,                             
                            status_code=status.HTTP_200_OK)
async def outgoing_response(payload: PubSubRead) -> dict:

    try:
        
        mapper = OutgoingMapper()
        outgoing_response = await PubSubMessageMapper.pubsub_to_outgoing_response(payload=payload)
        messages = mapper.to_domain_outgoing_messages_update(outgoing_response=outgoing_response)

        outgoing_service = await get_outgoing_service(company_id=outgoing_response.company_id)
        
        await outgoing_service.outgoing_response(messages=messages)
    
    except DomainNotFoundException as e:
        {"status": "ignore"}

    except DomainException as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "completed"}


    

