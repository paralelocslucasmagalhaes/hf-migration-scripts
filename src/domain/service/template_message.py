from domain.entities.apps.template import Template
from domain.entities.contact import Contact
from domain.entities.apps.app import App
from domain.entities.campaign import Campaign
from domain.entities.message.message import Message
from domain.entities.message.message import AuthorEnum
from domain.entities.message.message import DirectionEnum
from domain.entities.message.template import Template as TemplateOutgoing
from domain.entities.message.template import TemplateHeader
from domain.entities.message.template import TemplateBody
from domain.entities.message.template import TemplateButtons
from domain.entities.message.template import TemplateParams
from domain.entities.message.template import TypeParams
from domain.entities.whatsapp.template import TemplateComponent
from domain.entities.whatsapp.template import TemplateComponentExample
from typing import List
from domain.interface.template_message_generator import ITemplateMessageGenerator
from domain.entities.chat import Chat
from domain.entities.conversation import Conversation
from domain.entities.store import Store
from jinja2 import Template as Jinja2Template

from domain.entities.whatsapp.template import ComponentType

from datetime import datetime
from domain.entities.root.params import Params
from domain.entities.company import Company
from uuid import uuid4


class TemplateMessageGenerator(ITemplateMessageGenerator):

    def __init__(self):        
        pass

    def _get_dynamic_value(self, path:str,  context: dict):
        parts = path.split('.')
        obj = context.get(parts[0])
        for part in parts[1:]:
            obj = getattr(obj, part)
        return obj
    
    def _get_template_substitution_data(self, 
                                        store: Store,
                                        contact: Contact, 
                                        campaign: Campaign, 
                                        company: Company, 
                                        params: Params) -> dict:
        context = {
            "contact": contact,
            "campaign": campaign,
            "company": company,
            "store": store
        }
        template_data = {}
        for param in params.whatsapp_template:
            parts = param.path_value.split('.')
            obj = context.get(parts[0])
            if obj:
                template_data[param.name] = self._get_dynamic_value(param.path_value, context) 
        return template_data

    def _parse_template_to_text(self, text: str, template_data: dict) -> str:
        
        template = Jinja2Template(text)
        return template.render(**template_data)

    def _generate_whatsapp_message(self, 
                                   store: Store,
                                   template: Template, 
                                   contact: Contact, 
                                   campaign: Campaign, 
                                   company: Company, 
                                   params: Params):
        
        template_data = self._get_template_substitution_data(
            contact=contact,
            campaign=campaign,
            company=company,
            params=params,
            store=store
        )

        text=""
        for component in template.template.components:
            text+= component.text + "\n"
        return self._parse_template_to_text(text=text, template_data=template_data)

    def _get_dynamic_template_params_info(self, template_data: dict, component: TemplateComponent) -> str:
        import re 
        pattern = r"\{\{(.*?)\}\}"

        def group(match):

            clean = match.group().replace("{{","").replace("}}","")
            return template_data.get(clean)

        return re.sub(pattern, group, component.text)
        
    def get_template_params(self, template_data: dict, component_type: ComponentType, component_example: TemplateComponentExample) -> List[TemplateParams]:
        parameters = []
        named_params = []

        if component_type == ComponentType.HEADER:
            named_params.extend(component_example.header_text_named_params)
        if component_type == ComponentType.BODY:
            named_params.extend(component_example.body_text_named_params)

        for item in named_params:
            params_value = template_data.get(item.param_name)
            parameters.append(TemplateParams(
                type=TypeParams.TEXT,
                text=params_value,
                parameter_name=item.param_name

            ))
        return parameters

    def _generate_whatsapp_template(self, 
                                    campaign: Campaign, 
                                    store: Store,
                                    contact: Contact, 
                                    template: Template,  
                                    company: Company, 
                                    params: Params) -> TemplateOutgoing:
        

        headers = TemplateHeader(parameters=None)
        body = TemplateBody(parameters=None)
        buttons = TemplateButtons(parameters=None)

        template_data = self._get_template_substitution_data(
            contact=contact,
            campaign=campaign,
            company=company,
            params=params,
            store=store
        )
        

        for component in template.template.components:
            if component.type == ComponentType.HEADER:
                headers.parameters = self.get_template_params(
                                                template_data=template_data,
                                                component_type=component.type,
                                                component_example=component.example)
            if component.type == ComponentType.BODY:
                body.parameters = self.get_template_params(
                                                template_data=template_data,
                                                component_type=component.type,
                                                component_example=component.example)

        return TemplateOutgoing(
            name= template.template.name,
            language=template.template.language,
            headers=headers,
            body=body,
            buttons = buttons
        )


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
        
        # 2. Troca as variáveis (Lógica de parser)
        # Ex: "Olá {{name}}" -> "Olá João"
        message_template = self._generate_whatsapp_message(
                                template=template,
                                contact=contact,
                                campaign=campaign,
                                company=company,
                                params=params,
                                store=store)

        template_to_send = self._generate_whatsapp_template(
                                template=template,
                                contact=contact,
                                campaign=campaign,
                                company=company,
                                params=params,
                                store=store)
        from_ = Contact(
            id = company.id,
            company_id=company.id,  
            name= company.name,          
            mobile=app.app.phone_number,
            platform_id=app.app.phone_number_id
        )

        return Message(
            id= str(uuid4()),
            author = AuthorEnum.COMPANY,
            company_id = campaign.company_id,
            chat_id  = chat.id,
            conversation_id=conversation.id, ## fazer
            app_id = campaign.app_id,
            agent_id= app.agent_id,
            store_id= app.store_id,
            campaign_id=campaign.id,
            template_id=template.id,
            to = contact,
            from_= from_,
            message = message_template,
            message_type = "template",
            media = None,
            direction = DirectionEnum.OUTGOING,
            platform= app.platform,
            template = template_to_send,
            created_date = datetime.now(),
            updated_date = datetime.now(),
        )

    