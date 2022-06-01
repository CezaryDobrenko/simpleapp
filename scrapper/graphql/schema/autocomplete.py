import graphene
from graphene.relay.node import to_global_id
from graphene_django.filter import DjangoFilterConnectionField

from scrapper.graphql.filters.selector_type_filter import SelectorTypeFilter
from scrapper.graphql.schema.interval import IntervalConnection, IntervalNode
from scrapper.graphql.schema.selector_type import SelectorTypeNode
from scrapper.models.utils.intervals import Interval


class Autocomplete(graphene.ObjectType):
    id = graphene.ID()
    health_check = graphene.Boolean()
    selector_types = DjangoFilterConnectionField(
        SelectorTypeNode, filterset_class=SelectorTypeFilter
    )
    intervals = graphene.relay.ConnectionField(IntervalConnection)

    def resolve_health_check(self, info, **args):
        return True

    def resolve_intervals(self, info, **args):
        intervals = {i.name for i in Interval.Options}
        output = []
        for index, interval in enumerate(intervals):
            output.append(
                IntervalNode(id=f"{index}{interval}", interval_value=interval)
            )
        return output


class AutocompleteQuery(graphene.ObjectType):
    autocomplete = graphene.Field(Autocomplete)

    def resolve_autocomplete(self, info):
        return Autocomplete(id=to_global_id("Autocomplete", 1))
