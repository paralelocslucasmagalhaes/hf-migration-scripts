from fastapi import Depends
from infra.repository_legacy.params import ParamsRepository

def get_params_respository() ->ParamsRepository:
    return ParamsRepository()