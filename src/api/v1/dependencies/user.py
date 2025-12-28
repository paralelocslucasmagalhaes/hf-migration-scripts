from fastapi import Depends
from infra.repository.user import UserRepository

def get_user_respository() ->UserRepository:
    return UserRepository()