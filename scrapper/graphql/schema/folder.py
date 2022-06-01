import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from scrapper.graphql.filters.website_filter import WebsiteFilter
from scrapper.graphql.schema.website import WebsiteNode
from scrapper.models.folder import Folder
from scrapper.models.website import Website


class FolderNode(DjangoObjectType):
    class Meta:
        model = Folder
        interfaces = (graphene.relay.Node,)

    websites = DjangoFilterConnectionField(WebsiteNode, filterset_class=WebsiteFilter)

    def resolve_websites(self, info, **args):
        return Website.objects.filter(folder=self)
