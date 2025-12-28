import json
import os
import asyncio
from datetime import datetime, timedelta, timezone
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
from typing import Any, Optional
from domain.interface.infra.tasks import ITasksClient

class GoogleCloudTasksClient(ITasksClient):
    def __init__(self):
        self.project_id = os.getenv("PROJECT_ID")
        self.location = os.getenv("LOCATION")
        self.client = tasks_v2.CloudTasksClient()

    def _get_queue_path(self, queue: Optional[str] = None) -> str:
        """Helper para resolver o path da fila (usando a default do env ou uma específica)."""
        target_queue = queue or os.getenv("CAMPAIGN_QUEUE")
        return self.client.queue_path(self.project_id, self.location, target_queue)

    async def add(
        self, 
        url: str, 
        audience: str,
        payload: dict, 
        delay_seconds: int = 0,
        service_account: str = None, 
        task_name: Optional[str] = None,
        queue: Optional[str] = None
    ) -> str:
        parent = self._get_queue_path(queue)
        body = json.dumps(payload, default=str).encode()

        task = {
            "http_request": {
                "http_method": tasks_v2.HttpMethod.POST,
                "url": url,
                "headers": {"Content-Type": "application/json"},
                "body": body,
                "oidc_token": tasks_v2.OidcToken(
                    service_account_email=service_account,
                    audience=audience
                ) 
            },
        }

        if delay_seconds > 0:
            d = datetime.now(timezone.utc) + timedelta(seconds=delay_seconds)
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)
            task["schedule_time"] = timestamp

        if task_name:
            task["name"] = f"{parent}/tasks/{task_name}"

        # Executa a chamada síncrona do SDK em uma thread separada para não bloquear o loop async
        response = await asyncio.to_thread(
            self.client.create_task, 
            parent=parent, 
            task=task
        )
        return response.name

    async def delete(self, task_id: str) -> None:
        """
        Exclui uma tarefa. 
        task_full_name deve ser o caminho completo: projects/.../locations/.../queues/.../tasks/...
        """
        try:
            await asyncio.to_thread(self.client.delete_task, name=task_id)
        except Exception as e:
            # No Cloud Tasks, se a tarefa já executou ou foi excluída, ele lança erro.
            # No Clean Arch, você pode logar isso ou silenciar se não for crítico.
            print(f"Erro ao deletar task ou task já inexistente: {e}")

    async def put(
        self,
        task_id: str,
        url: str,
        audience: str,
        payload: dict,
        delay_seconds: int = 0,
        service_account: str = None,
        queue: Optional[str] = None
    ) -> str:
        """
        Atualiza uma tarefa (Delete + Create). 
        Retorna o nome da nova tarefa criada.
        """
        # 1. Tenta deletar a antiga
        await self.delete(task_id)

        # 2. Cria a nova (Opcional: extrair o task_name original se quiser manter o ID)
        # Note que o Cloud Tasks tem um "tombstone" de IDs excluídos por alguns minutos.
        # É recomendável gerar um novo ID ou deixar o Google gerar.
        return await self.add(
            url=url,
            audience=audience,
            payload=payload,
            delay_seconds=delay_seconds,
            queue=queue,
            service_account=service_account
        )