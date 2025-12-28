import asyncio
import json
import os
from infra.pub_sub.google import GooglePubSubAsyncClient
from domain.interface.publish_message import IPublishMessage

class OutgoingPubSubService(IPublishMessage):

    def __init__(self, pubsub_client: GooglePubSubAsyncClient ):
        self.pubsub_client = pubsub_client        
        self.topic = os.getenv("PUBSUB_TOPIC_OUTGOING_MESSAGE")
   
    async def publish(self, message: dict) -> str:
        return await self.pubsub_client.publish(topic=self.topic, message=message)
