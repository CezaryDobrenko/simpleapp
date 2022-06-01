from graphene import Node

from scrapper.graphql.schema.autocomplete import AutocompleteQuery
from scrapper.graphql.schema.user import UserQuery


class Query(AutocompleteQuery, UserQuery):
    node = Node.Field()
