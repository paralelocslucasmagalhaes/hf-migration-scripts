from domain.interface.publish_message import IPublishMessage
from domain.interface.infra.pubsub_async_client import PubSubAsyncClient

import os

class AsyncPublishMessage(IPublishMessage):
    
    def __init__(self, 
                 pubsub_client: PubSubAsyncClient
                 ):
        self.topic = os.getenv("PUBSUB_TOPIC_INCOMING_MESSAGE")
        self.pubsub_client = pubsub_client

    async def publish(self, message):
        return await self.pubsub_client.publish(topic=self.topic , message=message)