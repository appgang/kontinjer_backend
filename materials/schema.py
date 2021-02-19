import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Material


class MaterialList(DjangoObjectType):
    class Meta:
        model = Material
        fields = ("id", "name", "decay")


class Query(graphene.ObjectType):

    all_materials = graphene.List(
        MaterialList, token=graphene.String(required=True))

    material_search = graphene.Field(
        MaterialList, token=graphene.String(required=True), name=graphene.String(),)

    @login_required
    def resolve_all_materials(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("You need to login (;")
        return Material.objects.all()

    @login_required
    def resolve_material_search(self, info, name, **kwargs):
        print(name)
        try:
            material = Material.objects.get(name=name)
        except Material.DoesNotExist:
            material = None
        return material


schema = graphene.Schema(query=Query)
