
from domain.interface.repository.message import IMessageRepository
from domain.interface.repository.product_category import IProductCategoryRepository
from domain.interface.repository.company import ICompanyRepository
from domain.interface.repository.chat import IChatRepository
from domain.interface.repository.conversation import IConversationRepository
from domain.interface.repository.store import IStoreRepository
from domain.interface.repository.contact import IContactRepository
from domain.interface.repository.user import IUserRepository
from domain.interface.repository.integration import IIntegrationRepository
from domain.interface.repository.membership import IMembershipRepository




from infra.repository_legacy.message_legacy import MessageRepository

from domain.interface.repository.agent import IAgentRepository
from domain.interface.repository.product import IProductRepository
from datetime import datetime
import json
from api.v1.schemas.migrate import CollectionEnum
import asyncio
import os
from pathlib import Path

class ProcessingMigrateStoreUseCase:

    def __init__(
            self,
            company_repository: ICompanyRepository,
            chat_repository: IChatRepository,
            conversation_repository: IConversationRepository,
            store_repository: IStoreRepository,
            product_repository : IProductRepository, 
            product_catalog_repository : IProductCategoryRepository, 
            agent_repository : IAgentRepository, 
            contact_repository : IContactRepository,
            user_repository: IUserRepository,
            integration_respository: IIntegrationRepository,
            membership_respository: IMembershipRepository,



    ):
        self.product_repository             = product_repository
        self.product_catalog_repository     = product_catalog_repository
        self.agent_repository               = agent_repository
        self.company_repository             = company_repository
        self.chat_repository                = chat_repository
        self.conversation_repository        = conversation_repository
        self.store_repository               = store_repository
        self.contact_repository             = contact_repository
        self.user_repository                = user_repository
        self.integration_respository        = integration_respository
        self.membership_respository         = membership_respository

    def store_data(self, path: str, data: dict):
        source = {
            "source": data
            }
        full_path = Path("/data") / path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as file:
            json.dump(source, file, ensure_ascii=False, indent=4, default=str)
        return None
    
    async def list_of_data(self, company_id: str, collection: CollectionEnum, data: dict, is_root: bool = False):
        if is_root:
            path = f"{collection.value}/{data.get("id")}.json"
        else:
            path = f"{company_id}/{collection.value}/{data.get("id")}.json"
        return await asyncio.to_thread(self.store_data, path=path, data=data)

    async def store(self, company_id: str, created_date: datetime, collection: CollectionEnum) -> None:

        if collection == CollectionEnum.companies:
            await self.get_companies(company_id=company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.stores:
            await self.get_stores(company_id=company_id, collection=collection, created_date=created_date) 

        if collection == CollectionEnum.products:
            await self.get_products(company_id=company_id, collection=collection, created_date=created_date)  

        if collection == CollectionEnum.agents:
            await self.get_agents(company_id=company_id, collection=collection, created_date=created_date)   

        if collection == CollectionEnum.product_categories:
            await self.get_product_categories(company_id=company_id, collection=collection, created_date=created_date) 

        if collection == CollectionEnum.consumers:
            await self.get_consumers(company_id=company_id, collection=collection, created_date=created_date) 

        if collection == CollectionEnum.chats:
            await self.get_chats(company_id=company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.messages:
            await self.get_messages(company_id=company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.apps:
            await self.get_apps(company_id=company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.users:
            await self.get_users(company_id=company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.memberships:
            await self.get_memberships(company_id=company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.all:
            await self.get_companies(company_id=company_id, collection=CollectionEnum.companies, created_date=created_date)
            await self.get_stores(company_id=company_id, collection=CollectionEnum.stores, created_date=created_date)
            await self.get_products(company_id=company_id, collection=CollectionEnum.products, created_date=created_date)
            await self.get_agents(company_id=company_id, collection=CollectionEnum.agents, created_date=created_date)
            await self.get_product_categories(company_id=company_id, collection=CollectionEnum.product_categories, created_date=created_date)
            await self.get_consumers(company_id=company_id, collection=CollectionEnum.consumers, created_date=created_date)
            await self.get_chats(company_id=company_id, collection=CollectionEnum.chats, created_date=created_date)
            await self.get_messages(company_id=company_id, collection=CollectionEnum.messages, created_date=created_date)

        return None
    
    async def get_messages(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data_of_chats = await self.chat_repository.get_all_documents()
        for chat in data_of_chats:
            message_repository = MessageRepository(company_id=company_id, chat_id=chat.get("id"))
            data_of_list = await message_repository.get_all_documents()
            [await self.list_of_data(company_id=company_id, collection=collection, data=data) for data in data_of_list]
        return None

    async def get_chats(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data_of_list = await self.chat_repository.get_all_documents()
        return [await self.list_of_data(company_id=company_id, collection=collection, data=data) for data in data_of_list]
    

    async def get_consumers(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data_of_list = await self.contact_repository.get_all_documents()
        return [await self.list_of_data(company_id=company_id, collection=collection, data=data) for data in data_of_list]
    

    async def get_product_categories(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data_of_list = await self.product_catalog_repository.get_all_documents()
        return [await self.list_of_data(company_id=company_id, collection=collection, data=data) for data in data_of_list]
    

    async def get_agents(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data_of_list = await self.agent_repository.get_all_documents()
        return [await self.list_of_data(company_id=company_id, collection=collection, data=data) for data in data_of_list]
    

    async def get_stores(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data_of_list = await self.store_repository.get_all_documents()
        return [await self.list_of_data(company_id=company_id, collection=collection, data=data) for data in data_of_list]
    
    async def get_products(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data_of_list = await self.product_repository.get_all_documents()
        return [await self.list_of_data(company_id=company_id, collection=collection, data=data) for data in data_of_list]
    

    async def get_companies(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data = await self.company_repository.get(id=company_id)
        path = f"{company_id}/{collection.value}/{company_id}.json"
        return await asyncio.to_thread(self.store_data, path=path, data=data)
    
    async def get_apps(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data_of_list = await self.integration_respository.get_all_documents()
        return [await self.list_of_data(company_id=company_id, collection=collection, data=data, is_root=True) for data in data_of_list]

    async def get_users(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data_of_list = await self.user_repository.get_all_documents()
        return [await self.list_of_data(company_id=company_id, collection=collection, data=data, is_root=True) for data in data_of_list]
    
    async def get_memberships(self, company_id: str, created_date: datetime, collection: CollectionEnum):
        data_of_list = await self.membership_respository.get_all_documents()
        return [await self.list_of_data(company_id=company_id, collection=collection, data=data, is_root=True) for data in data_of_list]

        

            



