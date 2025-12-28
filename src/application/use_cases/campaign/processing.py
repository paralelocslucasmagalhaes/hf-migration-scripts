from domain.interface.repository.campaign.campaign import ICampaignRepository
from domain.interface.repository.campaign.contact import ICampaignContactRepository
from domain.interface.repository.message import IMessageRepository
from domain.interface.publish_message import IPublishMessage
from domain.interface.repository.template import ITemplateRepository
from domain.interface.repository.company import ICompanyRepository
from domain.interface.repository.chat import IChatRepository
from domain.interface.repository.conversation import IConversationRepository
from domain.interface.repository.store import IStoreRepository
from domain.entities.chat import Chat
from domain.entities.apps.app import App
from domain.entities.company import Company
from domain.entities.contact import Contact
from domain.entities.conversation import Conversation
from domain.interface.repository.app import IAppRepository
from domain.interface.repository.params import IParamsRepository
from domain.entities.campaign import Campaign
from domain.entities.message.message import Message
from domain.interface.template_message_generator import ITemplateMessageGenerator
from domain.exceptions.campaign.processing import ProcessingCampaignException
from domain.exceptions.campaign.campaing import CampaignNotFoundError

from dataclasses import asdict


class ProcessingCampaignUseCase:

    def __init__(
            self,
            campaign_repository: ICampaignRepository,
            campaign_contact_repository: ICampaignContactRepository,
            message_repository: IMessageRepository,
            template_repository: ITemplateRepository,
            app_repository: IAppRepository,
            company_repository: ICompanyRepository,
            chat_repository: IChatRepository,
            conversation_repository: IConversationRepository,
            store_repository: IStoreRepository,
            params_repository: IParamsRepository,
            template_message_generator: ITemplateMessageGenerator,
            publish_template_message: IPublishMessage,

    ):
        
        self.campaign_repository            = campaign_repository
        self.campaign_contact_repository    = campaign_contact_repository
        self.message_repository             = message_repository
        self.template_repository            = template_repository
        self.app_repository                 = app_repository
        self.publish_template_message       = publish_template_message
        self.template_message_generator     = template_message_generator
        self.company_repository             = company_repository
        self.chat_repository                = chat_repository
        self.conversation_repository        = conversation_repository
        self.store_repository               = store_repository
        self.params_repository              = params_repository


    async def _get_or_create_conversation(self, 
                                         chat: Chat,
                                         app: App, 
                                         company: Company, 
                                         contact: Contact,
                                           ) -> Conversation:
        where = [
                ["contact.platform_id", "==", contact.platform_id],
                ["end_conversation", "==", False]
            ]
        conversations = await self.conversation_repository.get_all(wheres=where)
        if len(conversations) < 1:
            return await self.conversation_repository.add(
                    document=Conversation(
                        company_id = company.id,
                        chat_id=chat.id,
                        contact=contact,
                        platform = app.platform,
                        app_id=app.id,
                        store_id = app.store_id
                )
                
            )
        return conversations[0]
    
    async def _get_or_create_chat(self, 
                                    app: App, 
                                    company: Company, 
                                    contact: Contact) -> Chat:
                
        chats = await self.chat_repository.get_list_by(field="contact.platform_id", condition="==", value=contact.platform_id)
        if len(chats) < 1:
            return await self.chat_repository.add(
                    document=Chat(
                        company_id = company.id,
                        contact=contact,
                        platform = app.platform,
                        app_id=app.id,
                        store_id = app.store_id
                )
                
            )
        return chats[0] # Busca sempre retorna um array. A consulta deve retorna apenas 1 registro.

    async def processing(self, campaign_id: str) -> Message:

        messages = []
        campaign = await self.campaign_repository.get(id = campaign_id)
        if not campaign:
            raise CampaignNotFoundError(campaign_id=campaign_id)
        
        await self.campaign_repository.start_running(campaign)

        template = await self.template_repository.get(campaign.template_id)
        if not template:
            await self.campaign_repository.failed(campaign)
            raise ProcessingCampaignException(f"Nenhum template encontrado para a campanha {campaign.id}")
        
        app = await self.app_repository.get(campaign.app_id)
        if not app:
            await self.campaign_repository.failed(campaign)
            raise ProcessingCampaignException(f"Nenhum app encontrado para a campanha {campaign.id}")
        
        company = await self.company_repository.get(campaign.company_id)
        store = await self.store_repository.get(app.store_id)
        params = await self.params_repository.get_all_documents() 
        param = params[0] ## Só deve ter apenas um documento na collection
        contacts = await self.campaign_contact_repository.get_all_documents()
        if len(contacts) < 1:
            await self.campaign_repository.failed(campaign)
            raise ProcessingCampaignException(f"Nenhum contato encontrado para a campanha {campaign.id}")
        
        for contact in contacts:
            chat = await self._get_or_create_chat(
                app=app,
                company=company,
                contact=contact.contact
            )
            conversation = await self._get_or_create_conversation(
                chat=chat,
                app=app,
                company=company,
                contact=contact.contact
            )
            try:
                message = self.template_message_generator.generate(
                    campaign=campaign,
                    app=app,
                    chat=chat,
                    conversation=conversation,
                    store=store,
                    contact=contact.contact,
                    template=template,
                    company=company,
                    params=param
                )
            except Exception as e:
                await self.campaign_repository.failed(campaign)
                raise ProcessingCampaignException(f"Não foi possível fazer a montagem da mensagem Campanha: {campaign.id} e Template: {campaign.template_id}")

            await self.message_repository.add(document=message)
            sended = await self.publish_template_message.publish(message= asdict(message))
            messages.append(sended)
        await self.campaign_repository.done(campaign)
        return messages

            



