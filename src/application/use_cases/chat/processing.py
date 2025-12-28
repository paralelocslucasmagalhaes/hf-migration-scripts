from domain.interface.infra.cache import ICacheAsyncClient
from domain.entities.message.message import Message
from typing import List
from domain.entities.message.message import MessageStatus
from domain.interface.ai_agent import IAgentAsyncClient
from domain.entities.message.message import AuthorEnum
from domain.entities.message.message import DirectionEnum
from domain.entities.platform import PlatformEnum
from domain.entities.message.message import MessageStatusEnum
from domain.exceptions.message import MessageNotFoundError
import logging

class ProcessingMessageService:

    def __init__(self,
                cache_repository:  ICacheAsyncClient,
                agent_service: IAgentAsyncClient,
                 ):
        self.cache_repository = cache_repository
        self.agent_service = agent_service

    async def parse_agent_message(self, message: dict):
        return message.get("message")
    
    async def _get_status_history(self, status: MessageStatusEnum) -> List[MessageStatus]: 
        status = MessageStatus(
            status=status
        )

        return [status]

    async def processing_message(self, message: Message) -> Message:
        
        conversation_id = f"buffer:{message.conversation_id}" 
        cache_lock = f"lock:{message.conversation_id}"
        messages_from_cache = await self.cache_repository.retrieve_and_delete(key=conversation_id)
        await self.cache_repository.delete(key=cache_lock)

        if len(messages_from_cache) <1:
            raise MessageNotFoundError(conversation_id=message.conversation_id)
        
        clean_message = [await self.parse_agent_message(message=message) for message in messages_from_cache]

        agent_message = {
            "company_id": message.company_id,
            "chat_id": message.chat_id,
            "agent_id": message.agent_id,
            "store_id": message.store_id,
            "conversation_id": message.conversation_id,
            "from": message.from_.mobile,
            "to": message.to.mobile,
            "messages": clean_message
        }

        try:

            agent_response = await self.agent_service.post(message=agent_message)
            agent_message = agent_response.get("message")
        except Exception as e:
            agent_message = "Olá.. Infelizmente tivemos um problema ao processar sua mensagem."
            logging.error(e)
            pass

        status = MessageStatusEnum.pending

        return Message(
            app_id=message.app_id,
            chat_id=message.chat_id,
            conversation_id=message.conversation_id,
            company_id=message.company_id,
            agent_id = message.agent_id,
            store_id=   message.store_id,
            author= AuthorEnum.AI,
            from_=message.to,
            to = message.from_,
            message = agent_message,
            message_type = "text",
            media = None,
            direction= DirectionEnum.OUTGOING,
            platform= PlatformEnum.whatsapp,
            status=status,
            status_history= await self._get_status_history(status=status)
        )






