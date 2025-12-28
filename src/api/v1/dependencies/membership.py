from fastapi import Depends
from infra.repository.membership import MembershipRepository

def get_membership_respository() ->MembershipRepository:
    return MembershipRepository()