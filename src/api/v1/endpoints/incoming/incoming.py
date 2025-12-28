from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Query
from fastapi import BackgroundTasks
from fastapi import Depends
import logging

from api.v1.schemas.pubsub import PubSubRead
from api.v1.schemas.pubsub import PubSubCreate

from api.v1.schemas.base import PlatformEnum
# from api.dependencies import get_cache
from api.v1.schemas.incoming import IncomingMessageCreate

from application.use_cases.incoming.event import IncomingEventService
from application.use_cases.incoming.message import IncomingMessageService


from application.mappers.whatsapp import WhatsAppMessageMapper
from application.mappers.pubsub import PubSubMessageMapper
from domain.exceptions.domain import DomainException
from api.v1.dependencies.incoming import get_incoming_message_use_case
from domain.entities.message.message import MessageStatusEnum
from api.v1.dependencies.incoming import get_incoming_event_use_case


router = APIRouter()


@router.post("/incoming/message", 
                            response_model=PubSubCreate,                             
                            status_code=status.HTTP_200_OK)
async def incomming_message(
        payload: PubSubRead ,
        use_case: IncomingMessageService = Depends(get_incoming_message_use_case)
        ) -> PubSubCreate:

    try:
        incoming_message = await PubSubMessageMapper.pubsub_to_incoming_message(payload=payload)
    
        platform = incoming_message.platform
        company_id = incoming_message.company_id
        app_id = incoming_message.app_id
        agent_id = incoming_message.agent_id
        store_id = incoming_message.store_id

        ## TODO: Implementar mapper e logica para tratar instagram quando tiver

        if platform and platform == PlatformEnum.whatsapp:
            whatsapp_mapper = WhatsAppMessageMapper()
            webhook = incoming_message.whatsapp

        ## Message
        if whatsapp_mapper.is_message(webhook.entry[0].changes[0].value):
            # Message
           

            messages = whatsapp_mapper.to_domain_message(
                        company_id=company_id,
                        app_id=app_id,
                        agent_id=agent_id,
                        store_id=store_id,
                        payload=webhook,
                        message_status=MessageStatusEnum.received
                    )
            chat = whatsapp_mapper.to_domain_chat(
                company_id=company_id,
                app_id=app_id,
                store_id=store_id,
                payload=webhook
            )
            conversation = whatsapp_mapper.to_domain_conversation(
                company_id=company_id,
                app_id=app_id,
                store_id=store_id,
                payload=webhook
            )

            contact = whatsapp_mapper.to_domain_contact(company_id=company_id, payload=webhook)
            await use_case.process_whatsapp(messages=messages,chat=chat, conversation=conversation, contact=contact)
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except DomainException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return PubSubCreate(status="completed")



@router.post("/incoming/event", 
                            response_model=PubSubCreate,                             
                            status_code=status.HTTP_200_OK)
async def incomming_event(
    payload: PubSubRead,
    use_case: IncomingEventService = Depends(get_incoming_event_use_case)
                          ) -> PubSubCreate:

    try:
        incoming_message = await PubSubMessageMapper.pubsub_to_incoming_message(payload=payload)
    
        platform = incoming_message.platform
        company_id = incoming_message.company_id
        app_id = incoming_message.app_id
        agent_id = incoming_message.agent_id
        store_id = incoming_message.store_id

        ## TODO: Implementar mapper e logica para tratar instagram quando tiver

        if platform and platform == PlatformEnum.whatsapp:
            whatsapp_mapper = WhatsAppMessageMapper()
            webhook = incoming_message.whatsapp
        
        ## Event
        if whatsapp_mapper.is_event(webhook.entry[0].changes[0].value):
            events = whatsapp_mapper.to_domain_event(payload=webhook)
            await use_case.whatsapp_event(events=events)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except DomainException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return PubSubCreate(status="completed")