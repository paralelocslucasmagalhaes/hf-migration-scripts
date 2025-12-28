from domain.interface.repository.contact import IContactRepository
from domain.exceptions.domain import DomainException
from domain.entities.contact import Contact

class ContactService:

    def __init__(self,
                 contact_repository: IContactRepository
                 ):
        self.contact_repository = contact_repository

    async def add(self, contact: Contact) -> Contact:        
        try:
            contact_data = await self.contact_repository.get_list_by(field="platform_id", condition="==", value=contact.platform_id)
            if len(contact_data) > 0:
                return contact_data[0]
            return await self.contact_repository.add(document=contact)
        except DomainException as e:
            raise DomainException(e)       