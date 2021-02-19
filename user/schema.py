import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token, create_refresh_token

from django.contrib.auth.models import User

from .models import Profile


class Profile(DjangoObjectType):
    class Meta:
        model = Profile


class CreateProfile(graphene.Mutation):
    username = graphene.String()
    password = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        usernam = graphene.String()
        passw = graphene.String()

    def mutate(self, info, usernam, passw):
        createdUser = User.objects.create_user(usernam, None, passw)
        createdUser.save()
        return CreateProfile(username=usernam, password=passw, success=True)


class Mutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
