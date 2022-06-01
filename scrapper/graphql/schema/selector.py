import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from scrapper.graphql.filters.collected_data_filter import CollectedDataFilter
from scrapper.graphql.schema.collected_data import CollectedDataNode
from scrapper.models.collected_data import CollectedData
from scrapper.models.selectors import Selector


class SelectorNode(DjangoObjectType):
    class Meta:
        model = Selector
        interfaces = (graphene.relay.Node,)

    collected_data = DjangoFilterConnectionField(
        CollectedDataNode, filterset_class=CollectedDataFilter
    )

    def resolve_collected_data(self, info, **args):
        return CollectedData.objects.filter(selector=self)
