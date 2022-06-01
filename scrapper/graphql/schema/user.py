import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from scrapper.graphql.auth import authenticate_required
from scrapper.graphql.filters.folder_filter import FolderFilter
from scrapper.graphql.schema.folder import FolderNode
from scrapper.models.folder import Folder
from scrapper.models.user import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)

    folders = DjangoFilterConnectionField(FolderNode, filterset_class=FolderFilter)

    def resolve_folders(self, info, **args):
        return Folder.objects.filter(user=self)


class UserQuery:
    me = graphene.Field(UserNode)

    @authenticate_required()
    def resolve_me(self, info, **kwargs):
        return kwargs["current_user"]
