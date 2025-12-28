
import os
from domain.interface.infra.cache import ICacheAsyncClient
from domain.interface.infra.tasks import ITaskService
from domain.entities.message.message import Message
from dataclasses import asdict
from typing import List
import time

class GroupMessageService():

    def __init__(self,
                    cache_repository: ICacheAsyncClient,
                    tasks_client: ITaskService
                 ):
        self.cache_repository = cache_repository
        self.message_expiration_time:int = int(os.getenv("MESSAGE_EXPIRATION_TIME", 45))
        self.tasks_client = tasks_client

    async def group_message(self, message: Message):
        cache_key = f"buffer:{message.conversation_id}"
        cache_lock = f"lock:{message.conversation_id}"

        await self.cache_repository.append_to_list(key=cache_key, value=asdict(message))
        has_lock = await self.cache_repository.exists(cache_lock)

        if not has_lock:
            await self.cache_repository.set(cache_lock, asdict(message), ttl=self.message_expiration_time)            
            await self.tasks_client.add(
                payload=asdict(message),
                delay_seconds=self.message_expiration_time
            )

    async def add(self, messages: List[Message]) -> None:
        return [await self.group_message(message) for message in messages]

        

