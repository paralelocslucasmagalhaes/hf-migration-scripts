from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List, Type, Any
import uuid
from domain.entities.root.enum import Status
from infra.db.firestore_async import FirestoreAsync # Importando sua classe async
from domain.interface.infra.db import IRepository
from dataclasses import asdict
# Definindo o Tipo Genérico que deve ser uma subclasse de BaseModel
T = TypeVar('T')


class AsyncFirestoreCRUD(IRepository[T]):
    def __init__(
        self, 
        collection: str,
        entitie: Type[T]
    ):
        self.collection = collection
        self.db = FirestoreAsync(collection=collection)
        self.entitie = entitie

    async def get(self, id: str) -> Optional[T]:
        data = await self.db.get(id)
        if data:
            return data
        return None
    
    async def get_list_by(self, field: str, condition: str, value: str)-> List[T]:
        data = await self.db.get_list_by(
            field=field, 
            condition=condition, 
            value=value
        )
        return [self.entitie(**doc) for doc in data] if data else []
    async def get_all(
        self, 
        limit: int = 100, 
        offset: int = 0, 
        order_by: str = "created_date", 
        descending: bool = True, 
        wheres: list = []
    ) -> List[T]:
        data = await self.db.get_all(
            limit=limit, 
            offset=offset, 
            order_by=order_by, 
            descending=descending, 
            wheres=wheres
        )
        return [doc for doc in data] if data else []
    
    async def get_all_documents(self) -> List[T]:
        data = await self.db.get_all_documents()
        return [doc for doc in data] if data else []

    async def add(self, document: T) -> T:

        if not document.id:
            document.id = str(uuid.uuid4())
        
        result = await self.db.create(asdict(document))
        return self.entitie(**result)

    async def update(self, id: str, document: dict) -> Optional[T]:
        # Aqui recebemos um dict com os campos parciais para atualizar
        updated = await self.db.update(document_id=id, document=document)
        if updated:
            return self.entitie(**updated)
        return None

    async def delete(self, id: str) -> Optional[T]:
        # Soft delete utilizando o status deactive
        return await self.update(id, {"status": Status.deactive})