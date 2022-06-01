import graphene

from scrapper.graphql.mutations import Mutation
from scrapper.graphql.schema import Query

schema = graphene.Schema(mutation=Mutation, query=Query)
