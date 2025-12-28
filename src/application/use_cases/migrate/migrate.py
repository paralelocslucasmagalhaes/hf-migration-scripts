
from domain.interface.repository.message import IMessageRepository
from domain.interface.repository.product_category import IProductCategoryRepository
from domain.interface.repository.company import ICompanyRepository
from domain.interface.repository.chat import IChatRepository
from domain.interface.repository.conversation import IConversationRepository
from domain.interface.repository.store import IStoreRepository
from domain.interface.repository.contact import IContactRepository
from domain.interface.repository.user import IUserRepository
from domain.interface.repository.app import IAppRepository
from domain.interface.repository.membership import IMembershipRepository
from domain.entities.platform import PlatformEnum
from domain.entities.agent.agent import Agent
from domain.entities.chat import ChatStatus

from domain.entities.chat import Chat
from domain.entities.product.product import Product

from domain.entities.company import Company
from domain.entities.contact import Contact
from domain.entities.product.product_category import ProductCategory

from domain.entities.conversation import Conversation
from domain.entities.message.message import Message
from domain.entities.message.message import MessageStatusEnum
from domain.entities.message.message import MessageStatus


from domain.interface.repository.agent import IAgentRepository
from domain.interface.repository.product import IProductRepository
from datetime import datetime
from dataclasses import asdict
import json
from api.v1.schemas.migrate import CollectionEnum
import asyncio
import os
from pathlib import Path
from domain.entities.company import Company
from domain.entities.user import User
from domain.entities.membership import Membership


from domain.entities.store import Store
from domain.entities.apps.app import App
from domain.entities.apps.whatsapp.app import WhatsAppApp
from domain.entities.apps.whatsapp.app import Status




class ProcessingMigrateUseCase:

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
            message_repository: IMessageRepository,
            user_repository: IUserRepository,
            membership_respository: IMembershipRepository,
            apps_respository: IAppRepository,

    ):
        self.product_repository             = product_repository
        self.product_catalog_repository     = product_catalog_repository
        self.agent_repository               = agent_repository
        self.company_repository             = company_repository
        self.chat_repository                = chat_repository
        self.conversation_repository        = conversation_repository
        self.store_repository               = store_repository
        self.contact_repository             = contact_repository
        self.message_repository             = message_repository
        self.user_repository                = user_repository
        self.apps_respository               = apps_respository
        self.membership_respository         = membership_respository

    def store_data(self, path: str, source_data: dict, data: dict):
        source_data["target"]= data
        full_path = Path("/data") / path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as file:
            json.dump(source_data, file, ensure_ascii=False, indent=4, default=str)
        return None
    
    def read_data(self, source_company_id: str, collection: CollectionEnum, file_name: str, is_root: bool = False):
        if is_root:
            with open(f"/data/{collection.value}/{file_name}", 'r', encoding='utf-8') as file:
                data = json.load(file)    
        else:
            with open(f"/data/{source_company_id}/{collection.value}/{file_name}", 'r', encoding='utf-8') as file:
                data = json.load(file)
        return data
    
    def list_of_file(self, source_company_id: str, collection: CollectionEnum, is_root: bool = False):
        if is_root:
            path = f"{collection.value}"
            folder = Path("/data") / path
        else:
            path = f"{source_company_id}/{collection.value}"
            folder = Path("/data") / path
        return [f for f in folder.iterdir() if f.is_file()]
    
    async def has_migrate(self, data: dict) -> bool:
        migrated = data.get("target")
        if migrated:
            return True
        return False

    async def migrate(self, source_company_id: str, created_date: datetime, collection: CollectionEnum) -> None:

        if collection == CollectionEnum.companies:
            await self.get_companies(source_company_id=source_company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.stores:
            await self.get_stores(source_company_id=source_company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.agents:
            await self.get_agents(source_company_id=source_company_id, collection=collection, created_date=created_date)   

        if collection == CollectionEnum.product_categories:
            await self.get_product_categories(source_company_id=source_company_id, collection=collection, created_date=created_date) 

        if collection == CollectionEnum.products:
            await self.get_products(source_company_id=source_company_id, collection=collection, created_date=created_date)  

        if collection == CollectionEnum.consumers:
            await self.get_consumers(source_company_id=source_company_id, collection=collection, created_date=created_date) 

        if collection == CollectionEnum.apps:
            await self.get_apps(source_company_id=source_company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.users:
            await self.get_users(source_company_id=source_company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.memberships:
            await self.get_memberships(source_company_id=source_company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.chats:
            await self.get_chats(source_company_id=source_company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.messages:
            await self.get_messages(source_company_id=source_company_id, collection=collection, created_date=created_date)

        if collection == CollectionEnum.all:
            await self.get_companies(source_company_id=source_company_id, collection=CollectionEnum.companies, created_date=created_date)
            await self.get_users(source_company_id=source_company_id, collection=CollectionEnum.users, created_date=created_date)
            await self.get_stores(source_company_id=source_company_id, collection=CollectionEnum.stores, created_date=created_date)
            await self.get_memberships(source_company_id=source_company_id, collection=CollectionEnum.memberships, created_date=created_date)
            await self.get_agents(source_company_id=source_company_id, collection=CollectionEnum.agents, created_date=created_date)
            await self.get_apps(source_company_id=source_company_id, collection=CollectionEnum.apps, created_date=created_date)
            await self.get_products(source_company_id=source_company_id, collection=CollectionEnum.products, created_date=created_date)
            await self.get_product_categories(source_company_id=source_company_id, collection=CollectionEnum.product_categories, created_date=created_date)
            await self.get_consumers(source_company_id=source_company_id, collection=CollectionEnum.consumers, created_date=created_date)
            await self.get_chats(source_company_id=source_company_id, collection=CollectionEnum.chats, created_date=created_date)
            await self.get_messages(source_company_id=source_company_id, collection=CollectionEnum.messages, created_date=created_date)


    async def get_companies(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=f"{source_company_id}.json")
        if await self.has_migrate(data=source_data):
            return None
        target_data = await self.company_repository.add(document=Company(** source_data.get("source")))
        path = f"{source_company_id}/{collection.value}/{source_company_id}.json"
        await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))

    async def get_stores(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        files = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=collection)
        for file in files:
            source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=file.name)
            if await self.has_migrate(data=source_data):
                continue
            target_data = await self.store_repository.add(document=Store(** source_data.get("source")))
            source = source_data.get("source")
            path = f"{source_company_id}/{collection.value}/{source.get("id")}.json"
            await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))
        return None
    
    async def get_agents(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        files = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=collection)
        for file in files:
            source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=file.name)
            if await self.has_migrate(data=source_data):
                continue
            target_data = await self.agent_repository.add(document=Agent(** source_data.get("source")))
            source = source_data.get("source")
            path = f"{source_company_id}/{collection.value}/{source.get("id")}.json"
            await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))
        return None
    
    async def get_product_categories(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        files = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=collection)
        for file in files:
            source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=file.name)
            if await self.has_migrate(data=source_data):
                continue
            target_data = await self.product_catalog_repository.add(document=ProductCategory(** source_data.get("source")))
            source = source_data.get("source")
            path = f"{source_company_id}/{collection.value}/{source.get("id")}.json"
            await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))
        return None

            
    async def get_products(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        files = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=collection)
        for file in files:
            source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=file.name)
            if await self.has_migrate(data=source_data):
                continue
            target_data = await self.product_repository.add(document=Product(** source_data.get("source")))
            source = source_data.get("source")
            path = f"{source_company_id}/{collection.value}/{source.get("id")}.json"
            await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))
        return None

    
    def parse_contact(self, data: dict) -> Contact:
        return Contact(
            company_id=data.get("company_id"),
            created_date=data.get("created_date"),
            updated_date=data.get("updated_date"),
            email=None,
            id=data.get("id"),
            instagram=data.get("instagram"),
            mobile=data.get("mobile"),
            name=data.get("name"),
            platform_id=data.get("mobile"),
            status=data.get("status"),
            tiktok=data.get("tiktok")
        )

    async def get_consumers(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        files = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=collection)
        for file in files:
            source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=file.name)
            if await self.has_migrate(data=source_data):
                continue
            target_data = await self.contact_repository.add(document=self.parse_contact(source_data.get("source")))
            source = source_data.get("source")
            path = f"{source_company_id}/{collection.value}/{source.get("id")}.json"
            await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))
        return None
        

    def parse_app(self, data: dict) -> App:

        whats_app = WhatsAppApp(
            app_id=data.get("id"),
            name="WhatsApp App Name",
            waba_id="WhatsApp Waba ID",
            pin=None,
            meta_status=Status.active,
            register_phone_status=Status.active ,
            subscribed_status=Status.active,
            phone_number=data.get("phone_number"),
            phone_number_id=data.get("phone_number_id"),
            verified_token=data.get("verify_token"),
            token=data.get("auth_token"),
        )

        return App(
            id=data.get("id"),
            company_id=data.get("company_id"),
            created_date=data.get("created_date"),
            updated_date=data.get("updated_date"),
            status=data.get("status"),
            app=whats_app,
            agent_id=data.get("agent_id"),
            platform=data.get("platform"),
            platform_id=data.get("phone_number_id"),
            store_id=data.get("store_id")
        )
    

    async def get_apps(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        files = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=collection, is_root=True)
        for file in files:
            source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=file.name, is_root=True)
            if await self.has_migrate(data=source_data):
                continue
            target_data = await self.apps_respository.add(document=self.parse_app(source_data.get("source")))
            source = source_data.get("source")
            path = f"{collection.value}/{source.get("id")}.json"
            await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))
        return None
    
    def parse_user(self, data: dict)-> User:
        return User(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email"),
            mobile=data.get("mobile"),
            photo_url=data.get("photo_url"),
            email_verified=False,
            last_login=data.get("last_login"),
            created_date=data.get("created_date"),
            updated_date=data.get("updated_date"),
            status=data.get("status"),
        )

    async def get_users(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        files = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=collection, is_root=True)
        for file in files:
            source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=file.name, is_root=True)
            if await self.has_migrate(data=source_data):
                continue
            target_data = await self.user_repository.add(document=self.parse_user(source_data.get("source")))
            source = source_data.get("source")
            path = f"{collection.value}/{source.get("id")}.json"
            await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))
        return None
    
    async def get_memberships(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        files = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=collection, is_root=True)
        for file in files:
            source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=file.name, is_root=True)
            if await self.has_migrate(data=source_data):
                continue
            target_data = await self.membership_respository.add(document=Membership(** source_data.get("source")))
            source = source_data.get("source")
            path = f"{collection.value}/{source.get("id")}.json"
            await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))
        return None

    def parse_chat(self, data: dict, contact_id: str = None, user_id: str = None, store_id: str = None ) -> Chat:
        return Chat(
            id=data.get("id"),
            company_id=data.get("company_id"),
            created_date=data.get("created_date"),
            updated_date=data.get("updated_date"),
            status=ChatStatus.active,
            app_id=data.get("integration_id"),
            contact_id=contact_id,
            handoff=data.get("handoff"),
            platform=data.get("last_inbound_channel", PlatformEnum.whatsapp),            
            store_id=store_id,
            user_id=user_id
        )
    
    def parse_conversation(self, chat: Chat) -> Conversation:
        return Conversation(
            company_id=chat.company_id,
            chat_id=chat.id,
            contact_id=chat.contact_id,
            platform=chat.platform,
            app_id=chat.app_id,
            store_id=chat.store_id
        )
    
    async def get_chats(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        files = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=collection)
        for file in files:
            source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=file.name)
            if await self.has_migrate(data=source_data):
                continue
            source = source_data.get("source")
            ## Contact
            consumer_id = source.get("consumer_id")
            ## User
            user_id = source.get("user_id")
            ## App
            store_id = None
            app_id = source.get("integration_id")
            if app_id:
                app = await self.apps_respository.get(id=app_id)
            store_id = app.store_id

            target_data = await self.chat_repository.add(
                    document=self.parse_chat(
                            data=source,
                            contact_id=consumer_id,
                            user_id=user_id,
                            store_id=store_id),
                    
                    )
            source = source_data.get("source")
            path = f"{source_company_id}/{collection.value}/{source.get("id")}.json"
            await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))
            await self.conversation_repository.add(document=self.parse_conversation(chat=target_data))

        return None
    
    def parse_message(self, data: dict, chat: Chat, conversation: Conversation, from_: str, to: str) -> Message:
        return Message(
            id=data.get("id"),
            author=data.get("author"),
            company_id=data.get("company_id"),
            created_date=data.get("created_date"),
            updated_date=data.get("updated_date"),
            status=MessageStatusEnum.delivered,
            status_history=[MessageStatus(status=MessageStatusEnum.delivered, created_date=data.get("created_date"))],
            chat_id=data.get("chat_id"),
            app_id=data.get("integration_id"),
            agent_id=data.get("agent_id"),
            store_id=chat.store_id,
            conversation_id=conversation.id,
            contact_id=chat.contact_id,
            from_=from_,
            to=to,
            message=data.get("message"),
            message_type="text",
            direction=data.get("direction"),
            platform=data.get("channel")
        )
    

    async def get_messages(self, source_company_id: str, created_date: datetime, collection: CollectionEnum):
        chats = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=CollectionEnum.chats)

        datas = {}
        for chat_file in chats:
            source_chat_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=CollectionEnum.chats, file_name=chat_file.name)
            source = source_chat_data.get("source")            
            chat_info = await self.chat_repository.get(id = source.get("id"))
            app = await self.apps_respository.get(id=source.get("integration_id"))
            contact = await self.contact_repository.get(id=source.get("consumer_id"))
            conversation = await self.conversation_repository.get_list_by(field="chat_id", condition="==", value=chat_info.id)
            datas.update({
                chat_info.id: {"chat": chat_info, "app": app, "conversation": conversation[0], "contact": contact}
            })

        files = await asyncio.to_thread(self.list_of_file, source_company_id=source_company_id, collection=collection)
        for file in files:
            source_data = await asyncio.to_thread(self.read_data, source_company_id=source_company_id, collection=collection, file_name=file.name)
            if await self.has_migrate(data=source_data):
                continue
            source = source_data.get("source")
            all_infos = datas.get(source.get("chat_id"))
            chat = all_infos.get("chat")
            contact = all_infos.get("contact")
            app = all_infos.get("app")
            conversation = all_infos.get("conversation")
            direction = source.get("direction")
            from_ = None
            to = None
            if direction == "incoming":
                from_ = contact.platform_id
                to = app.platform_id
            else:
                from_ = app.platform_id
                to = contact.platform_id
            target_data = await self.message_repository.add(
                    document=self.parse_message(
                            data=source,
                            chat=chat,
                            conversation=conversation,
                            to=to,
                            from_=from_
                            )
                    )
            path = f"{source_company_id}/{collection.value}/{source.get("id")}.json"
            await asyncio.to_thread(self.store_data, path=path, source_data=source_data, data=asdict(target_data))
        return None

    
    
    

    
    

    
    

    
    


    
    

    

        

            



