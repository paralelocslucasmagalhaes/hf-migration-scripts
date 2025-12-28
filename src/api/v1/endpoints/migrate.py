from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
import logging

from api.v1.schemas.migrate import MigrateRequest
from domain.exceptions.domain import DomainException
from domain.exceptions.domain import DomainNotFoundException
from api.v1.dependencies.migrate.store import ProcessingMigrateStoreUseCaseService
from api.v1.dependencies.migrate.migrate import ProcessingMigrateUseCaseService


router = APIRouter()


@router.post("/migrate/store", 
                            response_model=dict,                             
                            status_code=status.HTTP_200_OK)
async def processing_store(
        payload: MigrateRequest,
        use_case: ProcessingMigrateStoreUseCaseService
        ) -> dict:

    try:
        logging.info(payload)

        await use_case.store(company_id=payload.company_id, created_date=payload.created_date, collection=payload.collection)

    
    except DomainNotFoundException as e:
        {"status": "ignore"}

    except DomainException as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "completed"}



@router.post("/migrate/migrate", 
                            response_model=dict,                             
                            status_code=status.HTTP_200_OK)
async def processing_migrate(
        payload: MigrateRequest,
        use_case: ProcessingMigrateUseCaseService
        ) -> dict:

    try:
        logging.info(payload)

        await use_case.migrate(source_company_id=payload.company_id, created_date=payload.created_date, collection=payload.collection)

    
    except DomainNotFoundException as e:
        {"status": "ignore"}

    except DomainException as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "completed"}

    

