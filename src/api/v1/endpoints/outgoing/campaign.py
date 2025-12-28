from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
import logging

from api.v1.schemas.campaign.processing import ProcessingCampaignRequest

from domain.exceptions.domain import DomainException
from domain.exceptions.domain import DomainNotFoundException
from api.v1.dependencies.campaign import ProcessingCampaignUseCaseService

router = APIRouter()


@router.post("/processing/campaign", 
                            response_model=dict,                             
                            status_code=status.HTTP_200_OK)
async def processing_campaign(
        payload: ProcessingCampaignRequest,
        use_case: ProcessingCampaignUseCaseService
        ) -> dict:

    try:
        logging.info(payload)

        await use_case.processing(campaign_id=payload.campaign_id)

    
    except DomainNotFoundException as e:
        {"status": "ignore"}

    except DomainException as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "completed"}

    

