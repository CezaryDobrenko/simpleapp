import graphene
from graphene_django import DjangoObjectType

from scrapper.models.selector_type import SelectorType


class SelectorTypeNode(DjangoObjectType):
    class Meta:
        model = SelectorType
        interfaces = (graphene.relay.Node,)
