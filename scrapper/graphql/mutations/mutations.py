import logging

import graphene

from scrapper.graphql.auth import authenticate_required
from scrapper.graphql.schema.folder import FolderNode
from scrapper.graphql.schema.selector import SelectorNode
from scrapper.graphql.schema.website import WebsiteNode
from scrapper.models.api_key import ApiKey
from scrapper.models.collected_data import CollectedData
from scrapper.models.folder import Folder
from scrapper.models.selector_type import SelectorType
from scrapper.models.selectors import Selector
from scrapper.models.utils.intervals import Interval
from scrapper.models.website import Website

logger = logging.getLogger(__name__)


class DeactivateApiKey(graphene.Mutation):
    is_deactivated = graphene.Boolean()

    @authenticate_required()
    def mutate(self, info, **kwargs):
        api_token = kwargs["api_token"]
        key = ApiKey.objects.get(key=api_token)
        current_user = kwargs["current_user"]
        if current_user.id != key.user_id:
            raise Exception("This api_key cannot be deactivated by given api_key")
        key.is_active = False
        key.save()
        return DeactivateApiKey(is_deactivated=True)


class DeleteFolder(graphene.Mutation):
    is_deleted = graphene.Boolean()

    class Arguments:
        folder_id = graphene.ID(required=True)

    @authenticate_required()
    def mutate(self, info, folder_id: str, **kwargs):
        folder_pk = Folder.retrieve_id(folder_id)
        folder = Folder.objects.get(id=folder_pk)
        current_user = kwargs["current_user"]
        if current_user.id != folder.user_id:
            raise Exception("This folder cannot be edited by given api_key")
        folder.delete()
        return DeleteFolder(is_deleted=True)


class DeleteWebsite(graphene.Mutation):
    is_deleted = graphene.Boolean()

    class Arguments:
        website_id = graphene.ID(required=True)

    @authenticate_required()
    def mutate(self, info, website_id: str, **kwargs):
        website_pk = Website.retrieve_id(website_id)
        website = Website.objects.get(id=website_pk)
        current_user = kwargs["current_user"]
        if current_user.id != website.folder.user_id:
            raise Exception("This website cannot be edited by given api_key")
        website.delete()
        return DeleteWebsite(is_deleted=True)


class DeleteSelector(graphene.Mutation):
    is_deleted = graphene.Boolean()

    class Arguments:
        selector_id = graphene.ID(required=True)

    @authenticate_required()
    def mutate(self, info, selector_id: str, **kwargs):
        selector_pk = Selector.retrieve_id(selector_id)
        selector = Selector.objects.get(id=selector_pk)
        current_user = kwargs["current_user"]
        if current_user.id != selector.website.folder.user_id:
            raise Exception("This selector cannot be edited by given api_key")
        selector.delete()
        return DeleteSelector(is_deleted=True)


class UpdateFolder(graphene.Mutation):
    folder = graphene.Field(FolderNode)

    class Arguments:
        folder_id = graphene.ID(required=True)
        name = graphene.String()
        is_ready = graphene.Boolean()
        scraping_interval = graphene.String()

    @authenticate_required()
    def mutate(self, info, folder_id: str, **kwargs):
        folder_pk = Folder.retrieve_id(folder_id)
        folder = Folder.objects.get(id=folder_pk)
        current_user = kwargs["current_user"]
        if current_user.id != folder.user_id:
            raise Exception("This folder cannot be edited by given api_key")
        update_data = {}
        if "is_ready" in kwargs.keys():
            update_data["is_ready"] = kwargs.get("is_ready")
        if "name" in kwargs.keys():
            update_data["name"] = kwargs.get("name")
        if "scraping_interval" in kwargs.keys():
            update_data["scraping_interval"] = Interval.check_if_interval_exist(
                kwargs.get("scraping_interval")
            )
        folder.update(**update_data)
        return UpdateFolder(folder=folder)


class UpdateWebsite(graphene.Mutation):
    website = graphene.Field(WebsiteNode)

    class Arguments:
        website_id = graphene.ID(required=True)
        description = graphene.String()
        is_ready = graphene.Boolean()
        is_simplified = graphene.Boolean()

    @authenticate_required()
    def mutate(self, info, website_id: str, **kwargs):
        website_pk = Website.retrieve_id(website_id)
        website = Website.objects.get(id=website_pk)
        current_user = kwargs["current_user"]
        if current_user.id != website.folder.user_id:
            raise Exception("This website cannot be edited by given api_key")
        update_data = {}
        if "is_ready" in kwargs.keys():
            update_data["is_ready"] = kwargs.get("is_ready")
        if "description" in kwargs.keys():
            update_data["description"] = kwargs.get("description")
        if "is_simplified" in kwargs.keys():
            update_data["is_simplified"] = kwargs.get("is_simplified")
        website.update(**update_data)
        return UpdateWebsite(website=website)


class UpdateSelector(graphene.Mutation):
    selector = graphene.Field(SelectorNode)

    class Arguments:
        selector_id = graphene.ID(required=True)
        value = graphene.String()
        description = graphene.String()
        selector_type = graphene.ID()

    @authenticate_required()
    def mutate(self, info, selector_id: str, **kwargs):
        selector_pk = Selector.retrieve_id(selector_id)
        selector = Selector.objects.get(id=selector_pk)
        current_user = kwargs["current_user"]
        if current_user.id != selector.website.folder.user_id:
            raise Exception("This selector cannot be edited by given api_key")
        update_data = {}
        if "value" in kwargs.keys():
            update_data["value"] = kwargs.get("value")
        if "description" in kwargs.keys():
            update_data["description"] = kwargs.get("description")
        if "selector_type" in kwargs.keys():
            update_data["selector_type_id"] = SelectorType.retrieve_id(
                kwargs.get("selector_type")
            )
        selector.update(**update_data)
        return UpdateSelector(selector=selector)


class ClearSelectorData(graphene.Mutation):
    selector = graphene.Field(SelectorNode)

    class Arguments:
        selector_id = graphene.ID(required=True)

    @authenticate_required()
    def mutate(self, info, selector_id: str, **kwargs):
        selector_pk = Selector.retrieve_id(selector_id)
        selector = Selector.objects.get(id=selector_pk)
        current_user = kwargs["current_user"]
        if current_user.id != selector.website.folder.user_id:
            raise Exception("This selector cannot be edited by given api_key")
        collected_data = CollectedData.objects.filter(selector_id=selector_pk)
        for data_row in collected_data:
            data_row.delete()
        return UpdateSelector(selector=selector)


class CustomMutation(graphene.ObjectType):
    deactivate_api_key = DeactivateApiKey.Field()

    update_folder = UpdateFolder.Field()
    delete_folder = DeleteFolder.Field()

    update_website = UpdateWebsite.Field()
    delete_website = DeleteWebsite.Field()

    delete_selector = DeleteSelector.Field()
    update_selector = UpdateSelector.Field()
    clear_selector_data = ClearSelectorData.Field()
