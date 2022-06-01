import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from scrapper.graphql.filters.selector_filter import SelectorFilter
from scrapper.graphql.schema.selector import SelectorNode
from scrapper.models.selectors import Selector
from scrapper.models.website import Website


class WebsiteNode(DjangoObjectType):
    class Meta:
        model = Website
        interfaces = (graphene.relay.Node,)

    selectors = DjangoFilterConnectionField(
        SelectorNode, filterset_class=SelectorFilter
    )

    def resolve_selectors(self, info, **args):
        return Selector.objects.filter(website=self)
