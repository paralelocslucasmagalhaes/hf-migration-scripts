from api.v1.schemas.pubsub import PubSubRead
from api.v1.schemas.incoming import IncomingMessageCreate
from domain.entities.message.outgoing_response import OutgoingMessageResponse

import base64
import json

class PubSubMessageMapper:

    def __init__(self):
        pass
    
    
    async def handle_push_subscription(self, payload: PubSubRead):
        # Assumes request is a Flask or FastAPI request object with .data attribute
        try:
            data = payload.message.data
            if data:
                decoded_bytes = base64.b64decode(data)
                payload = decoded_bytes.decode("utf-8")
                # Process the message as needed
                return json.loads(payload)
            else:
                raise ValueError("Invalid Pub/Sub message format")
        except Exception as e:
            raise RuntimeError(f"Failed to handle push subscription: {e}")

    async def pubsub_to_dict(self, payload: PubSubRead) -> dict:
        return await self.handle_push_subscription(payload=payload)
    
    @staticmethod
    async def pubsub_to_incoming_message(payload: PubSubRead) -> IncomingMessageCreate:
        webhook = await PubSubMessageMapper.handle_push_subscription(PubSubMessageMapper, payload=payload)
        return IncomingMessageCreate(**webhook)
    
    @staticmethod
    async def pubsub_to_outgoing_response(payload: PubSubRead) -> OutgoingMessageResponse:
        webhook = await PubSubMessageMapper.handle_push_subscription(PubSubMessageMapper, payload=payload)
        return OutgoingMessageResponse(**webhook)
        