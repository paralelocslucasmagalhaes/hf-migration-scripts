# app/api/mappers/whatsapp_mapper.py
from api.v1.schemas.webhook.whatsapp import WhatsAppWebhook
from api.v1.schemas.webhook.whatsapp import Value
from api.v1.schemas.webhook.whatsapp import Change

from api.v1.schemas.webhook.whatsapp import Metadata
from api.v1.schemas.webhook.whatsapp import Contact as WhatsAppContact
from api.v1.schemas.webhook.whatsapp import Message as WhatsAppMessage
from api.v1.schemas.webhook.whatsapp import WhatsAppText
from api.v1.schemas.webhook.whatsapp import WhatsAppMedia
from api.v1.schemas.webhook.whatsapp import Statuses
from domain.entities.message.message import Message
from domain.entities.message.message import MessageStatus

from domain.entities.message.message import AuthorEnum
from domain.entities.message.message import DirectionEnum
from domain.entities.platform import PlatformEnum
from domain.entities.message.message import Media
from domain.entities.message.message import MessageStatusEnum
from domain.entities.chat import Chat
from domain.entities.chat import HandoffEnum

from domain.entities.conversation import Conversation

from domain.entities.event import Event
from domain.entities.contact import Contact
from datetime import datetime
from typing import List
import uuid

class WhatsAppMessageMapper:

    def __init__(self):
        self.MEDIA_TYPE = ["image", "audio", "voice", "document", "sticker", "video"]
    
    def is_message(self, value_payload: Value) -> bool:
        if value_payload.messages and len(value_payload.messages) > 0:
            return True
        return False
        
    def is_event(self, value_payload: Value) -> bool:
        if value_payload.statuses and len(value_payload.statuses) > 0:
            return True
        return False
        
    def _get_from_info(
                self, 
                company_id: str,
                mobile: str,
                whatsapp_contact: WhatsAppContact
                ) -> Contact:
        return Contact(
            name= whatsapp_contact.profile.name,
            mobile= mobile,
            platform_id=whatsapp_contact.wa_id,
            company_id=company_id
        )
        
    def _get_to_info(
                self, 
                app_id: str,
                company_id: str,
                whatsapp_metadata: Metadata
                ) -> Contact:
        return Contact(
            mobile= whatsapp_metadata.display_phone_number,
            platform_id=whatsapp_metadata.phone_number_id,
            id=app_id,
            company_id=company_id,
        )    
    def _get_to_phone_numer(self, metadata: Metadata) -> str:
        return metadata.display_phone_number
        
    def _get_media(self, whatsapp_media: WhatsAppMedia) -> Media:

        return Media(
            id= whatsapp_media.id,
            caption=whatsapp_media.caption,
            filename=whatsapp_media.filename,
            mime_type=whatsapp_media.mime_type,
            url=whatsapp_media.url,
            sha256=whatsapp_media.sha256,
        )
        
    def _get_text_message(self, text_message: WhatsAppText) -> str:
        return text_message.body
        
    def _get_timestamp(self, whatsapp_timestamp: str) -> datetime:
        return datetime.fromtimestamp(int(whatsapp_timestamp))
    
    def _get_status_history(self, whatsapp_message: WhatsAppMessage, message_status: MessageStatusEnum) -> List[MessageStatus]:
        history = []
        status = MessageStatus(
            status=message_status,
            created_date=self._get_timestamp(whatsapp_message.timestamp)
        )
        history.append(status)
        return history
        
    def _get_message(
                self, 
                app_id: str,
                company_id: str,
                agent_id: str,
                store_id: str,
                to: Contact,
                from_: Contact,
                whatsapp_message: WhatsAppMessage,
                message_status: MessageStatusEnum) -> Message:
        media = None
        if whatsapp_message.type in self.MEDIA_TYPE:
            media = self._get_media(getattr(whatsapp_message, whatsapp_message.type))
        
        message = None
        if whatsapp_message.type == "text":
            message = self._get_text_message(whatsapp_message.text)

        return Message(
            id = str(uuid.uuid4()),
            app_id=app_id,
            company_id=company_id,
            agent_id=agent_id,
            store_id=store_id,
            author= AuthorEnum.USER,
            platform_message_id= whatsapp_message.id,
            from_=from_,
            to = to,
            message = message,
            message_type = whatsapp_message.type,
            media = media,
            direction= DirectionEnum.INCOMING,
            platform= PlatformEnum.whatsapp,
            created_date= self._get_timestamp(whatsapp_message.timestamp),
            status= message_status,
            status_history=self._get_status_history(whatsapp_message=whatsapp_message, message_status=message_status)
        )
    
    def _get_change(self, payload: WhatsAppWebhook):
        for entry in payload.entry:
            for change in entry.changes:
                return change


    def get_to_info(self, app_id: str, company_id:str, change: Change) -> Contact:
        return self._get_to_info(app_id=app_id, whatsapp_metadata=change.value.metadata, company_id=company_id)

    def get_from_info(self, company_id:str, change: Change) -> Contact:
        for contact in change.value.contacts:
            return self._get_from_info(company_id=company_id, mobile=change.value.messages[0].from_, whatsapp_contact=contact)

    def get_messages(self, 
                change: Change,
                app_id: str,
                company_id: str,
                agent_id: str,
                store_id: str,
                to: Contact,
                from_: Contact,
                message_status: MessageStatusEnum) -> List[Message]:
        
        messages: List[Message] = []
        for message in change.value.messages:
            whatsapp_message = self._get_message(
                                                app_id=app_id,
                                                company_id=company_id,
                                                agent_id=agent_id,
                                                store_id=store_id,
                                                to=to, 
                                                 from_= from_, 
                                                 whatsapp_message=message, 
                                                 message_status=message_status)
            messages.append(whatsapp_message)
        return messages

    def to_domain_contact(self, 
                        company_id: str,
                        payload: WhatsAppWebhook) -> Contact:
        # Extrai a mensagem bruta (supondo estrutura complexa)
        messages: List[Message] = []
        try:
            for entry in payload.entry:
                for change in entry.changes:
                    from_ = self.get_from_info(company_id=company_id, change=change)
                    
        except (IndexError, AttributeError):
            raise ValueError("Invalid WhatsApp Payload Structure")
        
        # Retorna a Entidade de Domínio pronta
        return from_
    
    def to_domain_message(self, 
                        app_id: str,
                        company_id: str,
                        agent_id: str,
                        store_id: str,                          
                        payload: WhatsAppWebhook, 
                        message_status: MessageStatusEnum) -> List[Message]:
        # Extrai a mensagem bruta (supondo estrutura complexa)
        messages: List[Message] = []
        try:
            for entry in payload.entry:
                for change in entry.changes:
                    to = self.get_to_info(app_id=app_id,company_id=company_id, change=change)
                    from_ = self.get_from_info(company_id=company_id, change=change)
                    messages = self.get_messages(
                        app_id=app_id,
                        company_id=company_id,
                        agent_id = agent_id,
                        store_id=store_id,
                        change=change, 
                        to=to, 
                        from_=from_, 
                        message_status=message_status)

        except (IndexError, AttributeError):
            raise ValueError("Invalid WhatsApp Payload Structure")
        
        # Retorna a Entidade de Domínio pronta
        return messages
    
    def get_chat(self,
                app_id: str,
                company_id: str,
                store_id: str,
                contact: Contact) -> Chat:
        
        return Chat(
            company_id = company_id,
            handoff = HandoffEnum.AI,
            contact = contact,
            platform = PlatformEnum.whatsapp,
            app_id = app_id,
            store_id=store_id
        )
    
    def to_domain_chat(self, company_id:str, app_id:str, store_id: str, payload: WhatsAppWebhook) -> Chat:
        try:
            for entry in payload.entry:
                for change in entry.changes:
                    contact = self.get_from_info(company_id=company_id, change=change)
            chat = self.get_chat(contact=contact, app_id=app_id, company_id=company_id, store_id=store_id)

        except (IndexError, AttributeError):
            raise ValueError("Invalid WhatsApp Payload Structure")
        
        # Retorna a Entidade de Domínio pronta
        return chat
    
    def get_conversation(self,
                company_id: str,
                app_id: str,
                store_id:str,
                contact: Contact) -> Conversation:
        
        return Conversation(
            company_id = company_id,
            contact = contact,
            platform = PlatformEnum.whatsapp,
            app_id = app_id,
            store_id=store_id
        )
    
    def to_domain_conversation(self, company_id:str, app_id:str, store_id:str, payload: WhatsAppWebhook) -> Conversation:
        try:
            for entry in payload.entry:
                for change in entry.changes:
                    contact = self.get_from_info(company_id=company_id, change=change)
            conversation = self.get_conversation(contact=contact, app_id=app_id, company_id=company_id, store_id=store_id)

        except (IndexError, AttributeError):
            raise ValueError("Invalid WhatsApp Payload Structure")
        
        # Retorna a Entidade de Domínio pronta
        return conversation
    
    
    def _get_status_info(self, whatsapp_status: Statuses) -> Event:
        return Event(
            platform_message_id=whatsapp_status.id,
            status= whatsapp_status.status,
            created_date= self._get_timestamp(whatsapp_status.timestamp)
        )
    
    def to_domain_event(self, payload: WhatsAppWebhook) -> List[Event]:
        # Extrai a mensagem bru
        events: List[Event] = []
        try:
            for entry in payload.entry:
                for change in entry.changes:
                    for status in change.value.statuses:
                        event = self._get_status_info(status)
                        events.append(event)

        except (IndexError, AttributeError):
            raise ValueError("Invalid WhatsApp Payload Structure")
        
        # Retorna a Entidade de Domínio pronta
        return events