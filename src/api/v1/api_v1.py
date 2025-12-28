from fastapi import APIRouter

from api.v1.endpoints import migrate







api_router = APIRouter()
api_router.include_router(migrate.router, tags=["Migrate"])

