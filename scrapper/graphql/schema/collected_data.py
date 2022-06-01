import graphene
from graphene_django import DjangoObjectType

from scrapper.models.collected_data import CollectedData


class CollectedDataNode(DjangoObjectType):
    class Meta:
        model = CollectedData
        interfaces = (graphene.relay.Node,)
