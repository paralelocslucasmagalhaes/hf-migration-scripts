import os
import uuid
from google.cloud import firestore
from google.cloud.firestore import AsyncClient
from google.cloud.firestore_v1 import FieldFilter, ArrayUnion, SERVER_TIMESTAMP

class FirestoreAsync:

    def __init__(self, collection: str):
        # Inicializa o cliente assíncrono
        self.firestore_client = AsyncClient(project=os.getenv("PROJECT_ID"))
        self.collection = collection
   
    async def get(self, document_id: str):
        doc_ref = self.firestore_client.collection(self.collection).document(document_id)
        doc_snapshot = await doc_ref.get() # Await necessário
        if doc_snapshot.exists:
            return doc_snapshot.to_dict()
        return None
        
    async def get_by(self, field: str, condition: str, value: str):
        collection_ref = self.firestore_client.collection(self.collection)
        query = collection_ref.where(filter=FieldFilter(field, condition, value))
        # No async, a execução da query retorna um iterador assíncrono
        docs = []
        async for doc in query.stream():
            docs.append(doc)
        
        if len(docs) > 0:
            return docs[0].to_dict()
        return None

    async def get_list_by(self, field: str, condition: str, value: str):
        collection_ref = self.firestore_client.collection(self.collection)
        query = collection_ref.where(filter=FieldFilter(field, condition, value))
        
        docs = []
        async for doc in query.stream():
            docs.append(doc.to_dict())
        
        return docs if docs else None
    
    async def create(self, document: dict):
        doc_ref = self.firestore_client.collection(self.collection).document(document.get("id"))
        
        await doc_ref.create(document)
        # Busca o dado atualizado para retornar
        snapshot = await doc_ref.get()
        return snapshot.to_dict()
    
    async def set(self, document_id: str, document: dict):
        doc_ref = self.firestore_client.collection(self.collection).document(document_id)
        
        await doc_ref.create(document)
        # Busca o dado atualizado para retornar
        snapshot = await doc_ref.get()
        return snapshot.to_dict()
    
    async def get_wheres(self, wheres: list):
        query = self.firestore_client.collection(self.collection)
        for w in wheres:
            query = query.where(filter=FieldFilter(w[0], w[1], w[2]))
        
        docs = []
        async for doc in query.stream():
            docs.append(doc.to_dict())
        return docs
    
    async def add_array(self, document_id: str, document: dict, array_field: str, array_data: str):
        doc_ref = self.firestore_client.collection(self.collection).document(document_id)
        
        if document:
            await doc_ref.update(document)
            
        await doc_ref.update({
            f"{array_field}": ArrayUnion([array_data]),
            "updated_date": SERVER_TIMESTAMP
        })
        
        snapshot = await doc_ref.get()
        return snapshot.to_dict()

    async def get_all(self, limit: int = 100, offset: int = 0, order_by: str = "created_date", descending: bool = True, wheres: list = []):
        collection_ref = self.firestore_client.collection(self.collection)
        
        direction = firestore.Query.DESCENDING if descending else firestore.Query.ASCENDING
        query = collection_ref.order_by(order_by, direction=direction)
        
        for w in wheres:
            query = query.where(filter=FieldFilter(w[0], w[1], w[2]))
        
        query = query.offset(offset).limit(limit)
        
        docs = []
        async for doc in query.stream():
            docs.append(doc.to_dict())
            
        return docs
    
    async def get_all_documents(self):
        collection_ref = self.firestore_client.collection(self.collection)
        docs = []
        async for doc in collection_ref.stream():
            docs.append(doc.to_dict())
        return docs
    
    async def update(self, document_id: str, document: dict):
        doc_ref = self.firestore_client.collection(self.collection).document(document_id)
        document.update(updated_date=SERVER_TIMESTAMP)
        
        await doc_ref.set(document, merge=True)
        doc_snapshot = await doc_ref.get()
        return doc_snapshot.to_dict()
    
    async def delete (self, document_id: str):
        doc_ref = self.firestore_client.collection(self.collection).document(document_id)
        return await doc_ref.delete()