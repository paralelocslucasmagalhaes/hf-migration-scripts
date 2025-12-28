from domain.interface.infra import ITasksClient
from domain.interface.infra import ITaskService

import os

class TasksGroupMessage(ITaskService):

    def __init__(self,                 
                 task_client: ITasksClient
                 ):
        self.task_client = task_client
        self.url = os.getenv("BATCH_PROCESSING_URL")
        self.audience = os.getenv("BATCH_PROCESSING_URL")
        self.queue = os.getenv("MESSAGE_QUEUE")
        self.service_account = os.getenv("TASK_SERVICE_ACCOUNT")
        self.path = "api/v1/processing/message"
    
    async def add(self, payload: dict, delay_seconds: int) -> dict:
        return await self.task_client.add(
            url=f"{self.url}/{self.path}",
            audience=self.audience,
            payload=payload,
            delay_seconds=delay_seconds,
            queue=self.queue,
            service_account=self.service_account
        )
    
    async def delete(self, task_id: str) -> dict:
        return await self.task_client.delete(
            task_id=task_id
        )
    
    async def put(self, 
                    task_id: str,
                    payload: dict, 
                    delay_seconds: int ) -> dict:
        return await self.task_client.put(
            task_id=task_id,
            url=f"{self.url}/{self.path}",
            audience=self.audience,
            payload=payload,
            delay_seconds=delay_seconds,
            queue=self.queue,
            service_account=self.service_account
        )