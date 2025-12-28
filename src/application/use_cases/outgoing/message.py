
from domain.entities.message.message import Message
from domain.entities.conversation import Conversation
from domain.interface.publish_message import IPublishMessage
from application.use_cases.chat.conversation import ConversationService
from application.use_cases.chat.message import MessageService
from domain.entities.message.message import MessageOutgoingUpdate
from typing import List

from dataclasses import asdict

class OutgoingMessageService():

    def __init__(self,
                conversation_service: ConversationService,
                message_service: MessageService,
                pubsub_service: IPublishMessage,
                 ):
        self.message_service = message_service
        self.conversation_service = conversation_service
        self.pubsub_service = pubsub_service       

    
    async def send_message(self, message: Message):

        messages = await self.message_service.add(messages=[message])

        return [await self.pubsub_service.publish(message=asdict(stored_message)) for stored_message in messages]
    
    async def outgoing_message(self, conversation: Conversation, message: Message):
        conversation_data = await self.conversation_service.add(conversation=conversation)

        message.conversation_id = conversation_data.id

        return await self.send_message(message=message)
    
    async def outgoing_response(self, messages: List[MessageOutgoingUpdate]):
        return await self.message_service.update_outgoing_response(messages=messages)