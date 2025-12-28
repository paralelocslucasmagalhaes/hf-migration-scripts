# domain/interfaces/message_generator.py
from abc import ABC, abstractmethod
from domain.entities.campaign import Campaign
from domain.entities.contact import Contact
from domain.entities.chat import Chat
from domain.entities.conversation import Conversation
from domain.entities.store import Store
from domain.entities.message.message import Message
from domain.entities.company import Company
from domain.entities.root.params import Params
from domain.entities.apps.app   import App
from domain.entities.apps.template   import Template

class ITemplateMessageGenerator(ABC):
    @abstractmethod
    def generate(self,                  
                campaign: Campaign, 
                app: App, 
                chat: Chat,
                conversation: Conversation,
                store: Store,
                contact: Contact, 
                template: Template, 
                company: Company, 
                params: Params) -> Message:
        """Contrato para transformar campanha + contato em uma mensagem."""
        pass