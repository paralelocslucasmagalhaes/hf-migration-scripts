from domain.interface.infra.pubsub_async_client import PubSubAsyncClient
from google.cloud import pubsub_v1
import asyncio
import json
import os



class GooglePubSubAsyncClient(PubSubAsyncClient):

    def __init__(self):
        self.project_id = os.getenv("PROJECT_ID")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def _get_topic_path(self, topic: str):
        return self.publisher.topic_path(self.project_id, topic)
    
    def _get_subscription_path(self, subscription_id: str):
        return self.subscriber.subscription_path(self.project_id, subscription_id)

    async def publish(self, topic:str, message: dict) -> str:
        data = json.dumps(message, default=str).encode("utf-8")
        topic_path = self._get_topic_path(topic=topic)
        future = self.publisher.publish(topic_path, data)
        # Blocks until the publish is confirmed, not truly async
        message_id = await asyncio.wrap_future(future)
        return message_id
    
    async def subscribe(self, topic, callback):
        return await super().subscribe(topic, callback)
    
    async def unsubscribe(self, topic, callback):
        return await super().unsubscribe(topic, callback)