import graphene
from graphene import ObjectType


class IntervalNode(ObjectType):
    class Meta:
        interfaces = [graphene.relay.Node]

    interval_value = graphene.String()


class IntervalConnection(graphene.relay.Connection):
    class Meta:
        node = IntervalNode
