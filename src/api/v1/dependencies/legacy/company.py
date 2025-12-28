from fastapi import Depends
from infra.repository_legacy.company import CompanyRepository

def get_company_respository() ->CompanyRepository:
    return CompanyRepository()