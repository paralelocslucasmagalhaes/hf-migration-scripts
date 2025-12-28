from fastapi import Depends
from infra.repository.company import CompanyRepository

def get_company_respository() ->CompanyRepository:
    return CompanyRepository()