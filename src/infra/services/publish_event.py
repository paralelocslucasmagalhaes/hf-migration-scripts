from domain.interface.publish_message import IPublishMessage
from domain.interface.infra.pubsub_async_client import PubSubAsyncClient
import os

class AsyncPublishEvent(IPublishMessage):
    
    def __init__(self, 
                 pubsub_client: PubSubAsyncClient
                 ):
        self.topic_id = os.getenv("PUBSUB_TOPIC_INCOMING_EVENT")

        self.pubsub_client = pubsub_client

    async def publish(self, message):
        return self.pubsub_client.publish(message)