import json
from typing import Any, List, Optional
import redis.asyncio as redis
from domain.interface.infra.cache import ICacheAsyncClient  # Assuming interface is in interface.py

class RedisCacheClient(ICacheAsyncClient):
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: Optional[str] = None):
        self.client = redis.Redis(
            host=host, 
            port=port, 
            db=db, 
            password=password, 
            decode_responses=True
        )

    async def get(self, key: str) -> Optional[Any]:
        value = await self.client.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        serialized_value = json.dumps(value, default=str)
        return await self.client.set(name=key, value=serialized_value, ex=ttl)

    async def delete(self, key: str) -> bool:
        result = await self.client.delete(key)
        return result > 0

    async def exists(self, key: str) -> bool:
        return await self.client.exists(key) > 0

    async def clear(self) -> bool:
        return await self.client.flushdb()

    async def mget(self, keys: List[str]) -> dict:
        values = await self.client.mget(keys)
        result = {}
        for key, val in zip(keys, values):
            if val is not None:
                try:
                    result[key] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    result[key] = val
            else:
                result[key] = None
        return result

    async def mset(self, data: dict, ttl: Optional[int] = None) -> bool:
        # Redis MSET doesn't support TTL natively per key in one command
        # We use a pipeline to ensure atomicity and handle TTLs
        async with self.client.pipeline(transaction=True) as pipe:
            for key, value in data.items():
                serialized_value = json.dumps(value)
                await pipe.set(key, serialized_value, ex=ttl)
            results = await pipe.execute()
            return all(results)
        
    async def append_to_list(self, key: str, value: Any, ttl: Optional[int] = None) -> int:
        """
        Appends a value to a list stored at 'key'. 
        If the key doesn't exist, it is created as an empty list before appending.
        """
        serialized_value = json.dumps(value, default=str)
        # RPUSH adds to the end of the list
        result = await self.client.rpush(key, serialized_value)
        
        if ttl:
            await self.client.expire(key, ttl)
            
        return result # Returns the new length of the list
    
    async def retrieve_and_delete(self, key: str) -> List[str]:
        """
        Appends a value to a list stored at 'key'. 
        If the key doesn't exist, it is created as an empty list before appending.
        """
        async with self.client.pipeline(transaction=True) as pipe:
            pipe.lrange(key, 0, -1)
            pipe.delete(key)
            results = await pipe.execute()
            if len(results) > 0:
                return results[0]
            
        return []


    async def close(self):
        await self.client.close()