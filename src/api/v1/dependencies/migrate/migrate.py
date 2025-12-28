from fastapi import Depends
from typing import Annotated
from application.use_cases.migrate.migrate import ProcessingMigrateUseCase
from api.v1.dependencies.message import get_message_respository
from api.v1.dependencies.company import get_company_respository
from api.v1.dependencies.chat import get_chat_respository
from api.v1.dependencies.conversation import get_conversation_respository
from api.v1.dependencies.store import get_store_respository
from api.v1.dependencies.agent import get_agent_respository
from api.v1.dependencies.product import get_product_respository
from api.v1.dependencies.product_category import get_product_category_respository
from api.v1.dependencies.contact import get_contact_respository
from api.v1.dependencies.app import get_app_respository

from api.v1.dependencies.user import get_user_respository

from api.v1.dependencies.membership import get_membership_respository



from api.v1.schemas.migrate import MigrateRequest

def get_migrate_payload(payload: MigrateRequest) -> MigrateRequest:
    return payload

def get_message_respository_from_payload(
            payload: MigrateRequest = Depends(get_migrate_payload)
            ): 
        return get_message_respository(company_id=payload.company_id)

def get_chat_respository_from_payload(
            payload: MigrateRequest = Depends(get_migrate_payload)
            ): 
        return get_chat_respository(company_id=payload.company_id)

def get_conversation_respository_from_payload(
            payload: MigrateRequest = Depends(get_migrate_payload)
            ): 
        return get_conversation_respository(company_id=payload.company_id)

def get_store_respository_from_payload(
            payload: MigrateRequest = Depends(get_migrate_payload)
            ): 
        return get_store_respository(company_id=payload.company_id)

####

def get_agent_respository_from_payload(
            payload: MigrateRequest = Depends(get_migrate_payload)
            ): 
        return get_agent_respository(company_id=payload.company_id)

def get_product_respository_from_payload(
            payload: MigrateRequest = Depends(get_migrate_payload)
            ): 
        return get_product_respository(company_id=payload.company_id)

def get_product_category_respository_from_payload(
            payload: MigrateRequest = Depends(get_migrate_payload)
            ): 
        return get_product_category_respository(company_id=payload.company_id)

def get_contact_respository_from_payload(
            payload: MigrateRequest = Depends(get_migrate_payload)
            ): 
        return get_contact_respository(company_id=payload.company_id)

def get_migrate_use_case(
        company_repository = Depends(get_company_respository),
        chat_repository = Depends(get_chat_respository_from_payload),
        conversation_repository = Depends(get_conversation_respository_from_payload),
        store_repository = Depends(get_store_respository_from_payload), 
        product_repository = Depends(get_product_respository_from_payload), 
        product_catalog_repository = Depends(get_product_category_respository_from_payload), 
        agent_repository = Depends(get_agent_respository_from_payload), 
        contact_repository = Depends(get_contact_respository_from_payload), 
        message_repository = Depends(get_message_respository_from_payload), 
        membership_respository=Depends(get_membership_respository), 
        apps_respository=Depends(get_app_respository), 
        user_repository=Depends(get_user_respository), 

)-> ProcessingMigrateUseCase:
    return ProcessingMigrateUseCase(
        company_repository = company_repository,
        chat_repository = chat_repository,
        conversation_repository = conversation_repository,
        store_repository = store_repository,
        product_repository = product_repository,
        product_catalog_repository = product_catalog_repository,
        agent_repository = agent_repository,
        contact_repository = contact_repository,
        message_repository=message_repository,
        membership_respository=membership_respository,
        apps_respository=apps_respository,
        user_repository=user_repository

    )
    
ProcessingMigrateUseCaseService = Annotated[ProcessingMigrateUseCase, Depends(get_migrate_use_case)]