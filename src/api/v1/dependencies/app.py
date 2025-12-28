from fastapi import Depends
from infra.repository.app import AppRepository

def get_app_respository() ->AppRepository:
    return AppRepository()