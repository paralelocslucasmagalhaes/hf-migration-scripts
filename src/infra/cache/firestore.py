from infra.db.firestore_async import FirestoreAsync
from api.v1.schemas.base import Status
from typing import List
from typing import Optional

import uuid
from domain.interface.infra.cache import ICacheAsyncClient  # Assuming interface is in interface.py
import asyncio

class CacheFirestoreAsync(ICacheAsyncClient):
    def __init__(self, 
                collection: str                
                ):
        self.collection = collection
        self.db = FirestoreAsync(collection=collection)

    async def get(self, key: str) -> dict | None:
        data = await self.db.get(document_id=key)
        if data:
            return data
        return None

    async def set(self, key: str, value: dict, ttl: Optional[int] = None) -> bool:
        result = await self.db.set(document_id=key, document=value)
        return True
    
    async def delete(self, key: str) -> bool:
        result = await self.db.delete(document_id=key)
        return True

    async def exists(self, key: str) -> bool:
        data = await self.get(key)
        if data:
            return True
        return False

    async def clear(self) -> bool:
        pass

    async def mget(self, keys: List[str]) -> dict:
        pass

    async def mset(self, data: dict, ttl: Optional[int] = None) -> bool:
        pass
        
    async def append_to_list(self, key: str, value: dict, ttl: Optional[int] = None) -> int:
        if not await self.exists(key):
            await self.set(key=key, value={"id": key})
        added = await self.db.add_array( document_id=key, 
                    document=None, 
                    array_field="messages", 
                    array_data=value)

        messages = added.get("messages")
        return len(messages) # Returns the new length of the list

    
    async def retrieve_and_delete(self, key: str) -> List[dict]:
        """
        Appends a value to a list stored at 'key'. 
        If the key doesn't exist, it is created as an empty list before appending.
        """
        data = await self.get(key=key)
        await self.delete(key=key)
        return data.get("messages")


    async def close(self):
        return True