import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token, create_refresh_token
from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User
from materials.models import Product, UserProduct

from .models import Profile


class Profile(DjangoObjectType):
    class Meta:
        model = Profile


class UserProductList(DjangoObjectType):
    class Meta:
        model = UserProduct
        fields = ("user", "product", "added")

class ProductList(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("material", "code", "name")


class CreateProfile(graphene.Mutation):
    username = graphene.String()
    password = graphene.String()
    success = graphene.Boolean()
    token = graphene.String()

    class Arguments:
        username = graphene.String()
        password = graphene.String()

    def mutate(self, info, username, password):
        createdUser = User.objects.create_user(username, None, password)
        currentUser = createdUser.save()
        tokence = get_token(createdUser)
        print(createdUser.profile.products.all())
        return CreateProfile(username=username, password=password, success=True, token=tokence)


class Query(graphene.ObjectType):
    recycled = graphene.List(UserProductList)
    @login_required
    def resolve_recycled(self, info, **kwargs):
        return UserProduct.objects.filter(user=info.context.user.profile)


class Mutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
