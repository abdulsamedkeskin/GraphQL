import graphene
from graphene.relay import Node
from .models import User as UserModel
from graphene_mongo import MongoengineObjectType
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)


class User(MongoengineObjectType):
    class Meta:
        model = UserModel
        interfaces = (Node,)


class Auth(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, username, password):
        user = UserModel.objects.get(username=username, password=password)
        if user:
            return Auth(
                access_token=create_access_token(identity=username),
                refresh_token=create_refresh_token(identity=username),
                success=True,
            )
        return Auth(success=False)


class refreshToken(graphene.Mutation):
    new_token = graphene.String()
    success = graphene.Boolean()

    @jwt_required(refresh=True)
    def mutate(self, info):
        current_user = get_jwt_identity()
        return refreshToken(new_token=create_access_token(identity=current_user), success=True)


class createUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    user = graphene.Field(User)
    success = graphene.Boolean()

    def mutate(self, info, username, password):
        user = UserModel(username=username, password=password).save()
        return createUser(user=user, success=True)


class deleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.String()
    success = graphene.Boolean()

    @jwt_required()
    def mutate(self, info, id):
        UserModel.objects.get(pk=id).delete()
        return deleteUser(success=True)


class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.List(User, id=graphene.String(required=True))

    @jwt_required()
    def resolve_users(self, info):
        return list(UserModel.objects.all())

    @jwt_required()
    def resolve_user(self, info, id):
        return [UserModel.objects.get(pk=id)]


class Mutation(graphene.ObjectType):
    createUser = createUser.Field()
    deleteUser = deleteUser.Field()
    auth = Auth.Field()
    refresh = refreshToken.Field()


schema = graphene.Schema(query=Query, types=[User], mutation=Mutation)
