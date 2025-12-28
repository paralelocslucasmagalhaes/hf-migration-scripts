from fastapi import Depends
from infra.repository_legacy.user import UserRepository

def get_user_respository() ->UserRepository:
    return UserRepository()