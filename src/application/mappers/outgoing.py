from domain.entities.message.message import Message
from domain.entities.message.message import MessageStatus

from domain.entities.conversation import Conversation
from domain.entities.platform import PlatformEnum
from domain.entities.message.message import DirectionEnum
from domain.entities.message.message import MessageStatusEnum
from domain.entities.message.message import MessageOutgoingUpdate
from domain.entities.message.message import MessageStatus
from domain.entities.message.outgoing_response import OutgoingMessageResponse
from domain.entities.whatsapp.outgoing import WhatsAppOutgoingResponse
from typing import List
from api.v1.schemas.outgoing import OutgoingMessageCreate
import uuid

class OutgoingMapper():

    def __init__(self):
        pass

    def _get_status_history(self, status: MessageStatusEnum) -> List[MessageStatus]:

        return [
            MessageStatus(
                status=status
            )
        ]


    def to_domain_message(self, message: OutgoingMessageCreate) -> Message:

        message_dict = Message(** message.model_dump())
        message_dict.id = str(uuid.uuid4())
        message_dict.direction = DirectionEnum.OUTGOING
        message_dict.status_history = self._get_status_history(MessageStatusEnum.pending)

        return message_dict
    def to_domain_conversation(self, message: OutgoingMessageCreate) -> Conversation:
        message_dict = message.model_dump()

        return Conversation(
            company_id = message_dict.get("company_id"),
            chat_id= message_dict.get("chat_id"),
            contact= message_dict.get("to"),
            platform= message_dict.get("platform"),
            app_id= message_dict.get("app_id"),
            store_id= message_dict.get("store_id")
        )
    
    def _get_whatsapp_message_update(self, message_id: str, whatsapp_response: WhatsAppOutgoingResponse) -> List[MessageOutgoingUpdate]:
        messages = []
        for whatsapp_message in whatsapp_response.messages:
            message = MessageOutgoingUpdate(
                id=message_id,
                platform_message_id= whatsapp_message.id,
                status=whatsapp_message.message_status
            )
            messages.append(message)

        return messages

    
    def to_domain_outgoing_messages_update(self, outgoing_response: OutgoingMessageResponse) -> List[MessageOutgoingUpdate]:
        
        if outgoing_response.platform == PlatformEnum.whatsapp:
            whatsapp_response = outgoing_response.whatsapp
            return self._get_whatsapp_message_update(
                    message_id= outgoing_response.message_id, 
                    whatsapp_response=whatsapp_response)

        return [None]


    
    
