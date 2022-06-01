import graphene

from scrapper.graphql.mutations.mutations import CustomMutation


class Mutation(
    CustomMutation,
    graphene.ObjectType,
):
    pass
