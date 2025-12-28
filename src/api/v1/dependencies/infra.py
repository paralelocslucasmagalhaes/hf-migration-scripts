import os

from infra.cache.redis import RedisCacheClient
from infra.pub_sub.outgoing import OutgoingPubSubService
from infra.pub_sub.google import GooglePubSubAsyncClient
from infra.repository_legacy.grouping import CacheFirestoreRepository
from infra.tasks.group_message import TasksGroupMessage
from infra.tasks.google_tasks import GoogleCloudTasksClient

# Instância global (Singleton para o processo)
# No mundo real, use Variáveis de Ambiente aqui
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

redis_instance = RedisCacheClient(host=REDIS_HOST, port=REDIS_PORT)

async def get_cache() -> RedisCacheClient:
    return redis_instance

def get_publish_message() -> OutgoingPubSubService:
    return OutgoingPubSubService(
        pubsub_client=GooglePubSubAsyncClient()
    )

def get_cache_repository() -> CacheFirestoreRepository:
    return CacheFirestoreRepository()

def get_group_message_tasks_service() -> TasksGroupMessage:
    return TasksGroupMessage(
            task_client=GoogleCloudTasksClient()
        )    
