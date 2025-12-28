from fastapi import Depends
from typing import Annotated
from application.use_cases.campaign import ProcessingCampaignUseCase
from infra.repository_legacy.campaign import CampaignRepository
from infra.repository_legacy.campaign import CampaignContactRepository
from api.v1.dependencies.legacy.message import get_message_respository
from api.v1.dependencies.template import get_template_respository
from api.v1.dependencies.template import get_template_message_generator
from api.v1.dependencies.app import get_app_respository
from api.v1.dependencies.legacy.company import get_company_respository
from api.v1.dependencies.legacy.chat import get_chat_respository
from api.v1.dependencies.conversation import get_conversation_respository
from api.v1.dependencies.legacy.store import get_store_respository
from api.v1.dependencies.params import get_params_respository
from api.v1.dependencies.infra import get_publish_message
from api.v1.schemas.campaign.processing import ProcessingCampaignRequest

def get_processing_campaign_payload(payload: ProcessingCampaignRequest) -> ProcessingCampaignRequest:
    return payload

def get_campaign_repository(company_id: str) ->CampaignRepository:
    return CampaignRepository(company_id=company_id)

def get_campaign_repository_from_payload(
        payload: ProcessingCampaignRequest = Depends(get_processing_campaign_payload)) -> CampaignRepository:
    return CampaignRepository(company_id=payload.company_id)

def get_contact_campaign_repository(company_id: str, campaign_id: str) ->CampaignContactRepository:
    return CampaignContactRepository(company_id=company_id, campaign_id=campaign_id)


def get_contact_campaign_repository_from_payload(
         payload: ProcessingCampaignRequest = Depends(get_processing_campaign_payload)
        ) ->CampaignContactRepository:
    return CampaignContactRepository(company_id=payload.company_id, campaign_id=payload.campaign_id)


def get_message_respository_from_payload(
            payload: ProcessingCampaignRequest = Depends(get_processing_campaign_payload)
            ): 
        return get_message_respository(company_id=payload.company_id)

def get_template_respository_from_payload(
            payload: ProcessingCampaignRequest = Depends(get_processing_campaign_payload)
            ): 
        return get_template_respository(app_id=payload.app_id)

def get_chat_respository_from_payload(
            payload: ProcessingCampaignRequest = Depends(get_processing_campaign_payload)
            ): 
        return get_chat_respository(company_id=payload.company_id)

def get_conversation_respository_from_payload(
            payload: ProcessingCampaignRequest = Depends(get_processing_campaign_payload)
            ): 
        return get_conversation_respository(company_id=payload.company_id)

def get_store_respository_from_payload(
            payload: ProcessingCampaignRequest = Depends(get_processing_campaign_payload)
            ): 
        return get_store_respository(company_id=payload.company_id)

def get_processing_campaign_use_case(
        campaign_repository = Depends(get_campaign_repository_from_payload),
        campaign_contact_repository = Depends(get_contact_campaign_repository_from_payload),
        message_repository = Depends(get_message_respository_from_payload),
        template_repository = Depends(get_template_respository_from_payload),
        app_repository = Depends(get_app_respository),
        company_repository = Depends(get_company_respository),
        chat_repository = Depends(get_chat_respository_from_payload),
        conversation_repository = Depends(get_conversation_respository_from_payload),
        store_repository = Depends(get_store_respository_from_payload), 
        params_repository = Depends(get_params_respository), 
        template_message_generator = Depends(get_template_message_generator),
        publish_template_message = Depends(get_publish_message)

)-> ProcessingCampaignUseCase:
    return ProcessingCampaignUseCase(
        campaign_repository = campaign_repository,
        campaign_contact_repository = campaign_contact_repository,
        template_repository = template_repository,
        app_repository = app_repository,
        company_repository = company_repository,
        chat_repository = chat_repository,
        conversation_repository = conversation_repository,
        store_repository = store_repository,
        params_repository = params_repository,
        template_message_generator = template_message_generator,
        publish_template_message = publish_template_message,
    )
    
ProcessingCampaignUseCaseService = Annotated[ProcessingCampaignUseCase, Depends(get_processing_campaign_use_case)]