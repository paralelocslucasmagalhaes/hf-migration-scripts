from domain.entities.message.message import Message
from domain.entities.chat import Chat
from domain.entities.conversation import Conversation
from domain.entities.contact import Contact
from typing import List
from application.use_cases.chat.chat import ChatService
from application.use_cases.chat.conversation import ConversationService
from application.use_cases.chat.message import MessageService
from application.use_cases.chat.group import GroupMessageService
from application.use_cases.contact.contact import ContactService
from domain.entities.chat import HandoffEnum


class IncomingMessageService():

    def __init__(self,
                    chat_service: ChatService,
                    conversation_service: ConversationService,
                    message_service: MessageService,
                    contact_service: ContactService,
                    group_service: GroupMessageService
                 ):
        self.chat_service = chat_service
        self.conversation_service = conversation_service
        self.message_service = message_service
        self.contact_service = contact_service
        self.group_service = group_service

    async def process_whatsapp(self, 
                                contact: Contact,
                               chat: Chat, 
                               conversation: Conversation,
                               messages: List[Message]) -> None:
        
        contact_data = await self.contact_service.add(contact=contact)
        chat.contact.id = contact_data.id
        chat_data = await self.chat_service.add(chat=chat)
        chat_id = chat_data.id

        conversation.chat_id = chat_id
        conversation.contact.id = contact_data.id
        conversation_data = await self.conversation_service.add(conversation=conversation)
        conversation_id = conversation_data.id
        for message in messages:
            message.chat_id = chat_id
            message.conversation_id = conversation_id
            message.from_.id = contact_data.id
        
        await self.message_service.add(messages=messages)

        if chat_data.handoff == HandoffEnum.AI:
            await self.group_service.add(messages=messages)

        return None
    

    async def process_instagram(self, integration_id: str, message: Message) -> None:
        pass