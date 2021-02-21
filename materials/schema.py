import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, superuser_required

from .models import Material, Trashcan, Product, UserProduct


class MaterialList(DjangoObjectType):
    class Meta:
        model = Material
        fields = ("id", "name", "decay")


class TrashcanList(DjangoObjectType):
    class Meta:
        model = Trashcan
        fields = ("id", "material", "latitude", "longitude")


class ProductList(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("material", "code", "name", "id")


class UserProductList(DjangoObjectType):
    class Meta:
        model = UserProduct
        fields = ("user", "product", "added", "id")


class AddRecyclingLocation(graphene.Mutation):
    material = graphene.String()
    latitude = graphene.String()
    longitude = graphene.String()
    success = graphene.Boolean()

    class Arguments:
        material = graphene.String()
        latitude = graphene.String()
        longitude = graphene.String()

    @login_required
    @superuser_required
    def mutate(self, info, material, latitude, longitude):
        newLocation = Trashcan(
            material=material, latitude=latitude, longitude=longitude)
        newLocation.save()
        return AddRecyclingLocation(material=material, latitude=latitude, longitude=longitude, success=True)


class AddMaterial(graphene.Mutation):
    name = graphene.String()
    decay = graphene.Int()
    success = graphene.Boolean()

    class Arguments:
        name = graphene.String()
        decay = graphene.Int()

    @login_required
    @superuser_required
    def mutate(self, info, name, decay):
        newMaterial = Material(name=name, decay=decay)
        newMaterial.save()
        return AddMaterial(name=name, decay=decay, success=True)


class AddProduct(graphene.Mutation):
    material_name = graphene.String()
    code = graphene.String()
    name = graphene.String()
    success = graphene.Boolean()
    error = graphene.String(required=False)

    class Arguments:
        material_name = graphene.String(required=False)
        code = graphene.String()
        name = graphene.String()

    def mutate(self, info, code, name, **kwargs):
        print(kwargs.get("material_name", None))
        material_name = kwargs.get("material_name", None)
        if(material_name != None):
            try:
                currentMaterial = Material.objects.get(name=material_name)
            except Material.DoesNotExist:
                return AddProduct(material_name, code, name, False)

            try:
                productFromName = Product.objects.get(name=name)
            except Product.DoesNotExist:
                newProduct = Product(material=Material.objects.get(
                    name=material_name), code=code, name=name)
                newProduct.save()
                return AddProduct(material_name, code, name, True)
            return AddProduct(material_name, code, name, False, "Already Exists")
        return AddProduct(material_name, code, name, False)


class AddRecycledItem(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        product_name = graphene.String()

    def mutate(self, info, **kwargs):
        product_name = kwargs.get("product_name", None)
        if(product_name != None):
            try:
                currentProduct = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                return AddRecycledItem(False)
            newUserProduct = UserProduct(
                user=info.context.user.profile, product=currentProduct)
            newUserProduct.save()
            return AddRecycledItem(True)
        return AddRecycledItem(False)


class Query(graphene.ObjectType):

    all_materials = graphene.List(
        MaterialList)

    material_search = graphene.Field(
        MaterialList, token=graphene.String(required=True), name=graphene.String(),)

    recycling_locations = graphene.List(TrashcanList)

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

    def resolve_recycling_locations(self, info, **kwargs):
        return Trashcan.objects.all()


class Mutation(graphene.ObjectType):
    add_recycling_location = AddRecyclingLocation.Field()
    add_material = AddMaterial.Field()
    add_product = AddProduct.Field()
    add_recycled_item = AddRecycledItem.Field()


schema = graphene.Schema(query=Query)
