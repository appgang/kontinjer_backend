import graphene
from graphene_django import DjangoObjectType

from .models import Material


class MaterialList(DjangoObjectType):
    class Meta:
        model = Material
        fields = ("id", "name", "decay")


class Query(graphene.ObjectType):
    all_materials = graphene.List(MaterialList)

    def resolve_all_materials(root, info):
        # We can easily optimize query count in the resolve method
        return Material.objects.all()


schema = graphene.Schema(query=Query)
